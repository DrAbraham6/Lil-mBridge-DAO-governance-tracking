import unittest
import json
from caos_runtime import (
    CAOSRuntime,
    ConstitutionalIntent,
    ConstitutionalInvariant,
    InvariantSeverity,
    ValidationArtifact
)

class TestCAOSRuntime(unittest.TestCase):
    def setUp(self):
        self.runtime = CAOSRuntime()

    def test_asset_scope_matching(self):
        intent = ConstitutionalIntent(
            intent_id="INT-ASSET",
            actor_id="ACTOR-1",
            action="TRANSFER",
            target="ASSET-1",
            payload={"amount": 100}
        )

        # We need to peek into the execute flow or mock parts to verify which predicates were generated
        predicates = self.runtime.compiler.compile(intent, self.runtime.registry)

        # Should match INV-001 (asset:*) but not INV-002 (governance:*)
        predicate_ids = [p.predicate_id for p in predicates]
        self.assertIn("PRED-INV-001", predicate_ids)
        self.assertNotIn("PRED-INV-002", predicate_ids)

    def test_governance_scope_matching(self):
        intent = ConstitutionalIntent(
            intent_id="INT-GOV",
            actor_id="ACTOR-2",
            action="VOTE",
            target="GOVERNANCE-1",
            payload={"proposal_id": "P1"}
        )

        predicates = self.runtime.compiler.compile(intent, self.runtime.registry)

        # Should match INV-002 (governance:*) but not INV-001 (asset:*)
        predicate_ids = [p.predicate_id for p in predicates]
        self.assertIn("PRED-INV-002", predicate_ids)
        self.assertNotIn("PRED-INV-001", predicate_ids)

    def test_global_scope_matching(self):
        # Register a global invariant
        self.runtime.registry.register(
            ConstitutionalInvariant(
                invariant_id="INV-GLOBAL",
                name="Global Check",
                description="Global invariant",
                severity=InvariantSeverity.STANDARD,
                verification_method="formal",
                scope=["*"]
            )
        )

        intent = ConstitutionalIntent(
            intent_id="INT-ANY",
            actor_id="ACTOR-3",
            action="SOMETHING",
            target="OTHER",
            payload={}
        )

        predicates = self.runtime.compiler.compile(intent, self.runtime.registry)
        predicate_ids = [p.predicate_id for p in predicates]
        self.assertIn("PRED-INV-GLOBAL", predicate_ids)

    def test_court_deny_on_failed_validation(self):
        # Mocking a failed validation is hard without mocking the validator,
        # but we can test the court review directly.

        validations = [
            ValidationArtifact(
                predicate_id="P1",
                passed=False,
                confidence_score=1.0,
                verifier_type="deterministic",
                notes="Failed"
            )
        ]

        # We need a dummy assessment
        from caos_runtime import ConstitutionalAssessment
        assessment = ConstitutionalAssessment(
            risk_score=0.1,
            anomaly_score=0.1,
            recommendation="APPROVE",
            explanation="Everything else is fine"
        )

        decision = self.runtime.court.review(validations, assessment)
        self.assertEqual(decision.decision, "DENY")
        self.assertEqual(decision.rationale, "Invariant violation.")

    def test_ledger_updates(self):
        initial_root = self.runtime.ledger.current_root

        intent = ConstitutionalIntent(
            intent_id="INT-L1",
            actor_id="ACTOR-1",
            action="TRANSFER",
            target="ASSET-1",
            payload={"amount": 50}
        )

        self.runtime.execute(intent)

        self.assertNotEqual(self.runtime.ledger.current_root, initial_root)
        self.assertEqual(len(self.runtime.ledger.entries), 1)

if __name__ == "__main__":
    unittest.main()
