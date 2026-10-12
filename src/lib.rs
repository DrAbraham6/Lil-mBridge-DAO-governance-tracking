//! `i-agent`: Integrated trust and execution runtime abstractions for safe autonomous delegation.

use std::collections::HashMap;
use std::sync::Mutex;

/// Identity root representing the principal who delegates tasks.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Principal(pub String);

/// Structured goal primitive (not a raw prompt).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Intent {
    pub goal: String,
    pub parameters: HashMap<String, String>,
}

/// Grant ID uniquely identifying a capability allocation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct GrantId(pub u64);

/// Scoped capability grant with budget, expiry, and revocation controls.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CapabilityGrant {
    pub id: GrantId,
    pub scope: String,
    pub budget: u64,
    pub expiry: u64,
    pub revocation_handle: String,
}

/// Action to be performed by a skill.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Action {
    pub name: String,
    pub target: String,
    pub cost: u64,
}

/// Individual step within a proposed execution plan.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Step {
    pub skill: String,
    pub action: Action,
}

/// Structured plan proposed by a skill or model planner.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Plan {
    pub steps: Vec<Step>,
}

/// Cryptographic signature payload.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Signature(pub Vec<u8>);

/// Signed audit record of an executed action.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Receipt {
    pub id: String,
    pub principal: Principal,
    pub grant_id: GrantId,
    pub action: Action,
    pub outcome: String,
    pub signature: Signature,
}

/// Policy evaluation verdict.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Verdict {
    Allow,
    Deny(String),
}

/// Declared skill metadata and attestation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkillManifest {
    pub name: String,
    pub declared_capabilities: Vec<String>,
    pub version: String,
    pub attestation: String,
}

/// Error type for skill planning and execution operations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SkillError {
    PlanningFailed(String),
    ExecutionFailed(String),
    Unauthorized(String),
}

impl std::fmt::Display for SkillError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SkillError::PlanningFailed(msg) => write!(f, "Planning failed: {}", msg),
            SkillError::ExecutionFailed(msg) => write!(f, "Execution failed: {}", msg),
            SkillError::Unauthorized(msg) => write!(f, "Unauthorized: {}", msg),
        }
    }
}

impl std::error::Error for SkillError {}

/// Error type for runtime orchestration and policy enforcement.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RuntimeError {
    NoActiveGrant(Principal),
    PolicyViolation(String),
    SkillNotFound(String),
    ExecutionError(String),
    GrantRevoked(GrantId),
}

impl std::fmt::Display for RuntimeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RuntimeError::NoActiveGrant(p) => write!(f, "No active grant for principal {:?}", p),
            RuntimeError::PolicyViolation(msg) => write!(f, "Policy violation: {}", msg),
            RuntimeError::SkillNotFound(s) => write!(f, "Skill not found: {}", s),
            RuntimeError::ExecutionError(msg) => write!(f, "Execution error: {}", msg),
            RuntimeError::GrantRevoked(id) => write!(f, "Grant revoked: {:?}", id),
        }
    }
}

impl std::error::Error for RuntimeError {}

/// Isolated trust root for signature generation and policy evaluation.
pub trait TrustRoot: Send + Sync {
    fn sign(&self, payload: &[u8]) -> Signature;
    fn verify_policy(&self, grant: &CapabilityGrant, action: &Action, current_time: u64) -> Verdict;
}

/// Attested skill contract for planning and execution.
pub trait Skill: Send + Sync {
    fn manifest(&self) -> SkillManifest;
    fn plan(&self, intent: &Intent) -> Result<Plan, SkillError>;
    fn execute(&self, step: &Step, grant: &CapabilityGrant) -> Result<Receipt, SkillError>;
}

/// Orchestration runtime managing delegation, capability grants, and audit trails.
pub trait AgentRuntime {
    fn delegate(&self, who: &Principal, intent: Intent) -> Result<Vec<Receipt>, RuntimeError>;
    fn grant(&mut self, who: &Principal, grant: CapabilityGrant) -> GrantId;
    fn revoke(&mut self, id: GrantId);
    fn audit(&self, who: &Principal) -> Vec<Receipt>;
}

/// Reference implementation of `TrustRoot` performing policy enforcement outside the model.
pub struct EnclaveTrustRoot {
    secret_key: Vec<u8>,
}

impl EnclaveTrustRoot {
    pub fn new(secret_key: Vec<u8>) -> Self {
        Self { secret_key }
    }
}

impl TrustRoot for EnclaveTrustRoot {
    fn sign(&self, payload: &[u8]) -> Signature {
        let mut sig = self.secret_key.clone();
        sig.extend_from_slice(payload);
        Signature(sig)
    }

    fn verify_policy(&self, grant: &CapabilityGrant, action: &Action, current_time: u64) -> Verdict {
        if current_time > grant.expiry {
            return Verdict::Deny(format!("Grant expired at {}, current time {}", grant.expiry, current_time));
        }

        if action.cost > grant.budget {
            return Verdict::Deny(format!("Action cost {} exceeds grant budget {}", action.cost, grant.budget));
        }

        if grant.scope != "*" && grant.scope != action.name && grant.scope != action.target {
            return Verdict::Deny(format!("Action scope {:?} does not match grant scope {:?}", action.name, grant.scope));
        }

        Verdict::Allow
    }
}

/// Reference implementation of `AgentRuntime` enforcing Planner-Verifier isolation.
pub struct IsolatedAgentRuntime<T: TrustRoot> {
    trust_root: T,
    current_time: u64,
    skills: Mutex<HashMap<String, Box<dyn Skill>>>,
    grants: Mutex<HashMap<Principal, Vec<CapabilityGrant>>>,
    revoked_grants: Mutex<Vec<GrantId>>,
    audit_log: Mutex<Vec<Receipt>>,
}

impl<T: TrustRoot> IsolatedAgentRuntime<T> {
    pub fn new(trust_root: T, current_time: u64) -> Self {
        Self {
            trust_root,
            current_time,
            skills: Mutex::new(HashMap::new()),
            grants: Mutex::new(HashMap::new()),
            revoked_grants: Mutex::new(Vec::new()),
            audit_log: Mutex::new(Vec::new()),
        }
    }

    pub fn register_skill(&self, skill: Box<dyn Skill>) {
        let name = skill.manifest().name;
        self.skills.lock().unwrap().insert(name, skill);
    }

    pub fn set_time(&mut self, time: u64) {
        self.current_time = time;
    }
}

impl<T: TrustRoot> AgentRuntime for IsolatedAgentRuntime<T> {
    fn grant(&mut self, who: &Principal, grant: CapabilityGrant) -> GrantId {
        let id = grant.id;
        let mut grants = self.grants.lock().unwrap();
        grants.entry(who.clone()).or_default().push(grant);
        id
    }

    fn revoke(&mut self, id: GrantId) {
        let mut revoked = self.revoked_grants.lock().unwrap();
        if !revoked.contains(&id) {
            revoked.push(id);
        }
    }

    fn audit(&self, who: &Principal) -> Vec<Receipt> {
        let audit_log = self.audit_log.lock().unwrap();
        audit_log
            .iter()
            .filter(|r| &r.principal == who)
            .cloned()
            .collect()
    }

    fn delegate(&self, who: &Principal, intent: Intent) -> Result<Vec<Receipt>, RuntimeError> {
        // Retrieve active grant without holding lock indefinitely
        let active_grant = {
            let grants_guard = self.grants.lock().unwrap();
            let revoked_guard = self.revoked_grants.lock().unwrap();

            let principal_grants = grants_guard
                .get(who)
                .ok_or_else(|| RuntimeError::NoActiveGrant(who.clone()))?;

            principal_grants
                .iter()
                .find(|g| !revoked_guard.contains(&g.id))
                .cloned()
                .ok_or_else(|| RuntimeError::NoActiveGrant(who.clone()))?
        };

        let target_skill_name = intent
            .parameters
            .get("skill")
            .cloned()
            .unwrap_or_else(|| "default".to_string());

        // Planner step: propose plan
        let plan = {
            let skills_guard = self.skills.lock().unwrap();
            let skill = skills_guard
                .get(&target_skill_name)
                .ok_or_else(|| RuntimeError::SkillNotFound(target_skill_name.clone()))?;

            skill
                .plan(&intent)
                .map_err(|e| RuntimeError::ExecutionError(e.to_string()))?
        };

        if plan.steps.is_empty() {
            return Err(RuntimeError::ExecutionError("Empty plan proposed".to_string()));
        }

        // Verifier step: verify every step in the proposed plan against the trust root policy
        for step in &plan.steps {
            match self.trust_root.verify_policy(&active_grant, &step.action, self.current_time) {
                Verdict::Allow => {},
                Verdict::Deny(reason) => return Err(RuntimeError::PolicyViolation(reason)),
            }
        }

        // Executor step: execute steps using the scoped capability grant and collect receipts
        let mut receipts = Vec::new();

        for step in &plan.steps {
            let receipt = {
                let skills_guard = self.skills.lock().unwrap();
                let skill = skills_guard
                    .get(&step.skill)
                    .ok_or_else(|| RuntimeError::SkillNotFound(step.skill.clone()))?;

                skill
                    .execute(step, &active_grant)
                    .map_err(|e| RuntimeError::ExecutionError(e.to_string()))?
            };

            receipts.push(receipt);
        }

        // Record receipts in audit log
        let mut audit_guard = self.audit_log.lock().unwrap();
        for receipt in &receipts {
            audit_guard.push(receipt.clone());
        }

        Ok(receipts)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct MockTransferSkill;

    impl Skill for MockTransferSkill {
        fn manifest(&self) -> SkillManifest {
            SkillManifest {
                name: "transfer".to_string(),
                declared_capabilities: vec!["transfer".to_string()],
                version: "1.0.0".to_string(),
                attestation: "attested_by_store".to_string(),
            }
        }

        fn plan(&self, intent: &Intent) -> Result<Plan, SkillError> {
            let recipient = intent
                .parameters
                .get("recipient")
                .cloned()
                .unwrap_or_else(|| "unknown".to_string());
            let amount: u64 = intent
                .parameters
                .get("amount")
                .and_then(|v| v.parse().ok())
                .unwrap_or(0);

            Ok(Plan {
                steps: vec![Step {
                    skill: "transfer".to_string(),
                    action: Action {
                        name: "transfer".to_string(),
                        target: recipient,
                        cost: amount,
                    },
                }],
            })
        }

        fn execute(&self, step: &Step, grant: &CapabilityGrant) -> Result<Receipt, SkillError> {
            Ok(Receipt {
                id: "rcpt_001".to_string(),
                principal: Principal("user_123".to_string()),
                grant_id: grant.id,
                action: step.action.clone(),
                outcome: "success".to_string(),
                signature: Signature(vec![1, 2, 3, 4]),
            })
        }
    }

    #[test]
    fn test_successful_delegation_and_audit() {
        let trust_root = EnclaveTrustRoot::new(vec![9, 9, 9]);
        let mut runtime = IsolatedAgentRuntime::new(trust_root, 100);

        runtime.register_skill(Box::new(MockTransferSkill));

        let user = Principal("user_123".to_string());
        let grant = CapabilityGrant {
            id: GrantId(1),
            scope: "transfer".to_string(),
            budget: 500,
            expiry: 200,
            revocation_handle: "handle_1".to_string(),
        };

        runtime.grant(&user, grant);

        let mut params = HashMap::new();
        params.insert("skill".to_string(), "transfer".to_string());
        params.insert("recipient".to_string(), "alice".to_string());
        params.insert("amount".to_string(), "200".to_string());

        let intent = Intent {
            goal: "Send 200 credits to Alice".to_string(),
            parameters: params,
        };

        let receipts = runtime.delegate(&user, intent).expect("Delegation should succeed");
        assert_eq!(receipts.len(), 1);
        assert_eq!(receipts[0].action.cost, 200);
        assert_eq!(receipts[0].outcome, "success");

        let audit = runtime.audit(&user);
        assert_eq!(audit.len(), 1);
        assert_eq!(audit[0].id, "rcpt_001");
    }

    #[test]
    fn test_budget_exceeded_policy_violation() {
        let trust_root = EnclaveTrustRoot::new(vec![9, 9, 9]);
        let mut runtime = IsolatedAgentRuntime::new(trust_root, 100);

        runtime.register_skill(Box::new(MockTransferSkill));

        let user = Principal("user_123".to_string());
        let grant = CapabilityGrant {
            id: GrantId(1),
            scope: "transfer".to_string(),
            budget: 100, // Budget is 100
            expiry: 200,
            revocation_handle: "handle_1".to_string(),
        };

        runtime.grant(&user, grant);

        let mut params = HashMap::new();
        params.insert("skill".to_string(), "transfer".to_string());
        params.insert("recipient".to_string(), "alice".to_string());
        params.insert("amount".to_string(), "500".to_string()); // Attempting to send 500

        let intent = Intent {
            goal: "Send 500 credits to Alice".to_string(),
            parameters: params,
        };

        let result = runtime.delegate(&user, intent);
        assert!(matches!(result, Err(RuntimeError::PolicyViolation(_))));
    }

    #[test]
    fn test_grant_revocation() {
        let trust_root = EnclaveTrustRoot::new(vec![9, 9, 9]);
        let mut runtime = IsolatedAgentRuntime::new(trust_root, 100);

        runtime.register_skill(Box::new(MockTransferSkill));

        let user = Principal("user_123".to_string());
        let grant_id = GrantId(42);
        let grant = CapabilityGrant {
            id: grant_id,
            scope: "transfer".to_string(),
            budget: 500,
            expiry: 200,
            revocation_handle: "handle_42".to_string(),
        };

        runtime.grant(&user, grant);
        runtime.revoke(grant_id);

        let mut params = HashMap::new();
        params.insert("skill".to_string(), "transfer".to_string());

        let intent = Intent {
            goal: "Send 100 credits".to_string(),
            parameters: params,
        };

        let result = runtime.delegate(&user, intent);
        assert!(matches!(result, Err(RuntimeError::NoActiveGrant(_))));
    }
}
