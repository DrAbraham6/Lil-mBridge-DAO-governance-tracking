# i-Agent Abstraction & Runtime Architecture

The **i-agent** architecture shifts agentic computing from raw non-deterministic LLM output to safe, deterministic delegation. Analogous to how iOS abstracted phone capabilities into touch primitives, sandboxes, and permission prompts, `i-agent` abstracts messy model reasoning behind structured execution envelopes and trust roots.

---

## 1. Core Abstractions

| iOS Abstraction | i-Agent Analogue | Architectural Meaning |
|---|---|---|
| Touch & Gestures | Declarative Intent (`Intent`) | Replaces prompt engineering with structured goal primitives. |
| Permission Prompts & Sandbox | Scoped Capability Grants (`CapabilityGrant`) | Enforces default-deny capability envelopes with budget, expiry, and revocation handles. |
| Secure Enclave | Isolated Trust Root (`TrustRoot`) | Keeps key management, policy verification, and signing completely isolated from the untrusted model. |
| App Store & SDK | Attested Skill Contract (`Skill`) | Exposes narrow, versioned contracts via `SkillManifest` rather than granting raw API or socket access. |
| Apple ID | Principal Identity (`Principal`) | Root of identity linking every delegated action to the delegating authority. |
| Continuity & State | Cryptographic Audit Receipts (`Receipt`) | Generates signed, verifiable execution records for state changes and side effects. |

---

## 2. Planner-Verifier Isolation Architecture

To ensure safety in autonomous delegation, the model is treated as an **untrusted co-processor** (like an un-sandboxed third-party application). The runtime enforces policy completely outside the model's context.

```
       +-------------------------------------------------------+
       |                   AGENT RUNTIME                       |
       |  +-------------------+         +-------------------+  |
       |  |   Principal ID    |         |    Trust Root     |  |
       |  +---------+---------+---------+---------+---------+  |
       |            |                             |            |
       |            v                             v            |
       |  +-----------------------------------------------+    |
       |  |      Policy Engine / Capability Envelope      |    |
       |  +----+-------------------------------------+----+    |
       |       |                                     |         |
       |       | 1. Intent / Context                 | 3. Signed Plan / Action
       |       v                                     v         |
       |  +----------+                         +----------+    |
       |  |  Model   |                         |  Skill   |    |
       |  | (Planner)| -- 2. Proposed Plan --> | Execution|    |
       |  +----------+                         +----------+    |
       +-------------------------------------------------------+
```

### Execution Phases

1. **Planning (Untrusted Model):** The model receives a structured `Intent` and produces a proposed `Plan` (a sequence of `Step`s). It has no direct access to network, storage, or secrets.
2. **Verification (Trusted Enclave):** `AgentRuntime` intercepts the proposed `Plan` and queries `TrustRoot::verify_policy`. The policy checks constraints such as expiration time, monetary budget limits, and scope match.
3. **Execution & Auditing (Scoped Skill):** If approved, `AgentRuntime` passes each step and `CapabilityGrant` to `Skill::execute`. The skill performs the side effect and returns signed `Receipt`s which are recorded in the immutable audit log.

---

## 3. Rust Interface Contract

The primitives and traits implemented in `src/lib.rs` provide the narrow interface for `i-agent`:

```rust
pub struct Principal(pub String);
pub struct Intent { pub goal: String, pub parameters: HashMap<String, String> };
pub struct CapabilityGrant { pub id: GrantId, pub scope: String, pub budget: u64, pub expiry: u64, pub revocation_handle: String };
pub struct Receipt { pub id: String, pub principal: Principal, pub grant_id: GrantId, pub action: Action, pub outcome: String, pub signature: Signature };

pub trait TrustRoot: Send + Sync {
    fn sign(&self, payload: &[u8]) -> Signature;
    fn verify_policy(&self, grant: &CapabilityGrant, action: &Action, current_time: u64) -> Verdict;
}

pub trait Skill: Send + Sync {
    fn manifest(&self) -> SkillManifest;
    fn plan(&self, intent: &Intent) -> Result<Plan, SkillError>;
    fn execute(&self, step: &Step, grant: &CapabilityGrant) -> Result<Receipt, SkillError>;
}

pub trait AgentRuntime {
    fn delegate(&self, who: &Principal, intent: Intent) -> Result<Vec<Receipt>, RuntimeError>;
    fn grant(&mut self, who: &Principal, grant: CapabilityGrant) -> GrantId;
    fn revoke(&mut self, id: GrantId);
    fn audit(&self, who: &Principal) -> Vec<Receipt>;
}
```
