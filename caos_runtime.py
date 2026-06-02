import hashlib
import json
from datetime import datetime, UTC
from typing import Dict, List, Optional
import dspy
from pydantic import BaseModel

# ==========================================================
# UTILITIES
# ==========================================================
def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def now() -> str:
    return datetime.now(UTC).isoformat()

# ==========================================================
# CONSTITUTION
# ==========================================================
class ConstitutionalIntent(BaseModel):
    intent_id: str
    actor_id: str
    action: str
    target: str
    payload: Dict

# ==========================================================
# INVARIANT REGISTRY
# ==========================================================
class InvariantSeverity:
    ADVISORY = "advisory"
    STANDARD = "standard"
    CRITICAL = "critical"
    CONSTITUTIONAL = "constitutional"

class ConstitutionalInvariant(BaseModel):
    invariant_id: str
    name: str
    description: str
    severity: str
    verification_method: str
    scope: List[str] = ["*"]  # Tag-based scoping (e.g., "asset:*", "governance:vote")
    enabled: bool = True

class ConstitutionalInvariantRegistry:
    def __init__(self):
        self.invariants: Dict[str, ConstitutionalInvariant] = {}

    def register(self, invariant: ConstitutionalInvariant):
        self.invariants[invariant.invariant_id] = invariant

    def list_enabled(self):
        return [
            inv
            for inv in self.invariants.values()
            if inv.enabled
        ]

# ==========================================================
# IHIR
# ==========================================================
class IHIRPredicate(BaseModel):
    predicate_id: str
    invariant_id: str
    expression: str
    severity: str

class IHIRCompiler:
    def _matches_scope(self, scope_pattern: str, action: str, target: str) -> bool:
        if scope_pattern == "*":
            return True

        # Simple glob-like matching for "category:action"
        if ":" in scope_pattern:
            pattern_cat, pattern_act = scope_pattern.split(":", 1)

            # Extract category from target (handles "CAT:ID" or "CAT-ID")
            if ":" in target:
                target_cat = target.split(":", 1)[0].lower()
            elif "-" in target:
                target_cat = target.split("-", 1)[0].lower()
            else:
                target_cat = target.lower()

            # Match category and action
            cat_match = (pattern_cat == "*" or pattern_cat.lower() == target_cat)
            act_match = (pattern_act == "*" or pattern_act.lower() == action.lower())

            return cat_match and act_match

        return scope_pattern.lower() in [action.lower(), target.lower()]

    def compile(
        self,
        intent: ConstitutionalIntent,
        registry: ConstitutionalInvariantRegistry
    ) -> List[IHIRPredicate]:
        predicates = []
        for inv in registry.list_enabled():
            # Check if any scope pattern matches the intent
            is_relevant = any(
                self._matches_scope(s, intent.action, intent.target)
                for s in inv.scope
            )

            if is_relevant:
                predicates.append(
                    IHIRPredicate(
                        predicate_id=f"PRED-{inv.invariant_id}",
                        invariant_id=inv.invariant_id,
                        expression=inv.description,
                        severity=inv.severity
                    )
                )
        return predicates

# ==========================================================
# FORMAL VALIDATORS
# ==========================================================
class ValidationArtifact(BaseModel):
    predicate_id: str
    passed: bool
    confidence_score: float
    verifier_type: str
    notes: str

class FormalValidator:
    def validate(
        self,
        predicate: IHIRPredicate,
        context: Dict
    ) -> ValidationArtifact:
        # Placeholder deterministic logic
        passed = True
        return ValidationArtifact(
            predicate_id=predicate.predicate_id,
            passed=passed,
            confidence_score=1.0,
            verifier_type="deterministic",
            notes="Skeleton validator"
        )

# ==========================================================
# DSPY CONSTITUTIONAL ASSESSMENT
# ==========================================================
class ConstitutionalAssessment(BaseModel):
    risk_score: float
    anomaly_score: float
    recommendation: str
    explanation: str

class ConstitutionalAssessmentSignature(dspy.Signature):
    """Assess the constitutional risk and anomalies based on validations and context."""
    validations = dspy.InputField(desc="Summary of formal validations")
    context = dspy.InputField(desc="Transaction context/payload")
    assessment: ConstitutionalAssessment = dspy.OutputField()

class DSPyAssessmentLayer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(
            ConstitutionalAssessmentSignature
        )

    def forward(
        self,
        validations: List[ValidationArtifact],
        context: Dict
    ):
        # Serialize artifacts into a scannable context string
        validation_summary = "\n".join([
            f"- Predicate: {v.predicate_id} | Passed: {v.passed} | Notes: {v.notes}"
            for v in validations
        ])
        context_str = json.dumps(context, indent=2)

        # In a real scenario, we would call the predictor.
        # Since we don't have an LLM configured here, we'll simulate the response
        # if dspy.settings.lm is None.

        try:
            prediction = self.predictor(
                validations=validation_summary,
                context=context_str
            )
            return prediction.assessment
        except Exception as e:
            # Fallback for environment without LLM setup
            return ConstitutionalAssessment(
                risk_score=0.10,
                anomaly_score=0.01,
                recommendation="APPROVE",
                explanation=f"Simulated assessment (Error: {str(e)})"
            )

# ==========================================================
# WITNESS GENERATION
# ==========================================================
class ConstitutionalWitness(BaseModel):
    witness_id: str
    intent_hash: str
    validation_hash: str
    assessment_hash: str
    timestamp: str

class WitnessGenerator:
    def generate(
        self,
        intent: ConstitutionalIntent,
        validations: List[ValidationArtifact],
        assessment: ConstitutionalAssessment
    ) -> ConstitutionalWitness:
        intent_hash = sha256(
            intent.model_dump_json()
        )
        validation_hash = sha256(
            json.dumps(
                [v.model_dump() for v in validations],
                sort_keys=True
            )
        )
        assessment_hash = sha256(
            assessment.model_dump_json()
        )
        return ConstitutionalWitness(
            witness_id=f"WIT-{intent.intent_id}",
            intent_hash=intent_hash,
            validation_hash=validation_hash,
            assessment_hash=assessment_hash,
            timestamp=now()
        )

# ==========================================================
# MERKLE WITNESS TREE
# ==========================================================
class MerkleWitnessTree:
    @staticmethod
    def build(
        witnesses: List[ConstitutionalWitness]
    ) -> str:
        leaves = [
            sha256(w.model_dump_json())
            for w in witnesses
        ]
        if not leaves:
            return sha256("empty")
        while len(leaves) > 1:
            next_level = []
            for i in range(0, len(leaves), 2):
                left = leaves[i]
                right = (
                    leaves[i + 1]
                    if i + 1 < len(leaves)
                    else left
                )
                next_level.append(
                    sha256(left + right)
                )
            leaves = next_level
        return leaves[0]

# ==========================================================
# CONSTITUTIONAL COURT
# ==========================================================
class CourtDecision(BaseModel):
    decision: str
    rationale: str
    timestamp: str

class ConstitutionalCourt:
    def review(
        self,
        validations: List[ValidationArtifact],
        assessment: ConstitutionalAssessment
    ):
        failed = any(
            not v.passed
            for v in validations
        )
        if failed:
            return CourtDecision(
                decision="DENY",
                rationale="Invariant violation.",
                timestamp=now()
            )
        return CourtDecision(
            decision=assessment.recommendation,
            rationale=assessment.explanation,
            timestamp=now()
        )

# ==========================================================
# LEDGER
# ==========================================================
class ConstitutionalLedgerEntry(BaseModel):
    entry_id: str
    witness_root: str
    decision: str
    previous_root: str
    new_root: str
    timestamp: str

class ConstitutionalLedger:
    def __init__(self):
        self.entries: List[
            ConstitutionalLedgerEntry
        ] = []
        self.current_root = sha256(
            "genesis"
        )

    def append(
        self,
        witness_root: str,
        decision: CourtDecision
    ):
        previous = self.current_root
        self.current_root = sha256(
            previous +
            witness_root +
            decision.decision
        )
        entry = ConstitutionalLedgerEntry(
            entry_id=f"LEDGER-{len(self.entries)+1}",
            witness_root=witness_root,
            decision=decision.decision,
            previous_root=previous,
            new_root=self.current_root,
            timestamp=now()
        )
        self.entries.append(entry)
        return entry

# ==========================================================
# STATE ROOT UPDATE
# ==========================================================
class ConstitutionalStateRoot(BaseModel):
    state_root: str
    timestamp: str

# ==========================================================
# CAOS EXECUTION FLOW
# ==========================================================
class CAOSRuntime:
    def __init__(self):
        self.registry = ConstitutionalInvariantRegistry()
        self.registry.register(
            ConstitutionalInvariant(
                invariant_id="INV-001",
                name="Asset Conservation",
                description="Asset conservation check",
                severity=InvariantSeverity.CRITICAL,
                verification_method="formal",
                scope=["asset:*"]
            )
        )
        self.registry.register(
            ConstitutionalInvariant(
                invariant_id="INV-002",
                name="Governance Integrity",
                description="Governance vote integrity check",
                severity=InvariantSeverity.CRITICAL,
                verification_method="formal",
                scope=["governance:*"]
            )
        )
        self.compiler = IHIRCompiler()
        self.validator = FormalValidator()
        self.assessor = DSPyAssessmentLayer()
        self.witness_gen = WitnessGenerator()
        self.court = ConstitutionalCourt()
        self.ledger = ConstitutionalLedger()

    def execute(
        self,
        intent: ConstitutionalIntent
    ):
        predicates = self.compiler.compile(
            intent,
            self.registry
        )
        validations = [
            self.validator.validate(
                p,
                intent.payload
            )
            for p in predicates
        ]
        assessment = self.assessor(
            validations,
            intent.payload
        )
        witness = self.witness_gen.generate(
            intent,
            validations,
            assessment
        )
        witness_root = (
            MerkleWitnessTree.build(
                [witness]
            )
        )
        decision = self.court.review(
            validations,
            assessment
        )
        ledger_entry = self.ledger.append(
            witness_root,
            decision
        )
        state_root = ConstitutionalStateRoot(
            state_root=self.ledger.current_root,
            timestamp=now()
        )
        return {
            "decision": decision,
            "witness": witness,
            "ledger_entry": ledger_entry,
            "state_root": state_root
        }

if __name__ == "__main__":
    runtime = CAOSRuntime()

    print("--- Test Case 1: Asset Transfer ---")
    intent1 = ConstitutionalIntent(
        intent_id="INT-001",
        actor_id="ACTOR-001",
        action="TRANSFER",
        target="ASSET-001",
        payload={"amount": 100}
    )
    result1 = runtime.execute(intent1)
    # Check that only INV-001 was processed
    print(f"Witness ID: {result1['witness'].witness_id}")
    print(f"Decision: {result1['decision'].decision}")

    print("\n--- Test Case 2: Governance Vote ---")
    intent2 = ConstitutionalIntent(
        intent_id="INT-002",
        actor_id="ACTOR-002",
        action="VOTE",
        target="GOVERNANCE-001",
        payload={"proposal_id": "PROP-42", "vote": "YES"}
    )
    result2 = runtime.execute(intent2)
    # Check that only INV-002 was processed
    print(f"Witness ID: {result2['witness'].witness_id}")
    print(f"Decision: {result2['decision'].decision}")

    print(f"\nFinal Ledger Root: {runtime.ledger.current_root}")
    print(f"Total Ledger Entries: {len(runtime.ledger.entries)}")
