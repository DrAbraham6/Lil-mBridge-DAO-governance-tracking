"""
OWO v0.2 Hardened Adversarial Test Suite
----------------------------------------
Tests for Identity Determination, No Implicit Authority, WorldContext Derivation,
Atomic Migration with Rollback, Constitutional Duality, and Process Traceability.
"""

import unittest
from owo_invariants import INVARIANT_REGISTRY, get_invariant
from orchid_world_ontology import (
    BoundaryType,
    CitizenshipManager,
    CitizenshipStatus,
    ConstitutionalDualityChecker,
    ConstitutionalTransitionRecord,
    DelegationContract,
    EntityObject,
    EntityOntologicalState,
    EntityStateSnapshot,
    IdentityClaim,
    IdentityEvidence,
    IdentityVerifier,
    InterWorldRelationship,
    MigrationCertificate,
    MigrationState,
    NoImplicitAuthorityChecker,
    OrchidWorldObject,
    TransitionRecorder,
    WorldBoundary,
    WorldConstitution,
    WorldContext,
    WorldGraph,
    WorldMigrationProtocol,
    WorldType,
    compute_hmac_signature,
    sha256,
)


class TestOWOv2HardenedOntology(unittest.TestCase):

    def setUp(self):
        # Setup World A
        self.world_a = OrchidWorldObject(
            world_id="urn:orchid:world:alpha",
            world_type=WorldType.HYBRID_LAYERED,
            constitution=WorldConstitution(
                constitution_hash=sha256("CONST-ALPHA"),
                invariants=["INV-AUTHORITY-000", "INV-MOBILITY-001", "INV-WORLD-CTX-001"],
                duality_rules={
                    "Citizenship": {
                        "entails": ["VOTE_GOVERNANCE", "ACCESS_PUBLIC_RESOURCE"],
                        "does_not_entail": ["IDENTITY_OWNERSHIP", "MEMORY_CAPTURE", "SUBSTRATE_CAPTURE"]
                    }
                }
            ),
            state_root=sha256("STATE-ALPHA-GENESIS"),
            boundaries=[WorldBoundary(boundary_type=BoundaryType.CRYPTOGRAPHIC, specification={"key": "rsa2048"})],
            provenance_root=sha256("PROVENANCE-ALPHA-GENESIS")
        )

        # Setup World B
        self.world_b = OrchidWorldObject(
            world_id="urn:orchid:world:beta",
            world_type=WorldType.ECONOMIC,
            constitution=WorldConstitution(
                constitution_hash=sha256("CONST-BETA"),
                invariants=["INV-AUTHORITY-000", "INV-MOBILITY-001", "INV-MOBILITY-002"],
                duality_rules={
                    "Citizenship": {
                        "entails": ["EXECUTE_TRADE"],
                        "does_not_entail": ["PERPETUAL_RETENTION"]
                    }
                }
            ),
            state_root=sha256("STATE-BETA-GENESIS"),
            boundaries=[WorldBoundary(boundary_type=BoundaryType.ECONOMIC, specification={"currency": "ORCHID"})],
            provenance_root=sha256("PROVENANCE-BETA-GENESIS")
        )

        # Setup Entity
        self.pubkey = "0x04bfcab510169b09362f1670076973e295585d18df8ecb10009d77a6104d08a487"
        self.entity_id = f"ID-{sha256(self.pubkey)[:12]}"
        self.secret_key = "entity_secret_key_123"
        self.entity = EntityObject(
            entity_id=self.entity_id,
            public_key=self.pubkey,
            memory_root=sha256("INITIAL-MEMORY-LOG"),
            ontological_state=EntityOntologicalState.WORLDLESS
        )

        # Setup WorldContext
        self.source_context = WorldContext.derive(
            world_id=self.world_a.world_id,
            entity_id=self.entity.entity_id,
            world_state_root=self.world_a.state_root,
            constitution_hash=self.world_a.constitution.constitution_hash,
            temporal_epoch=1,
            temporal_sequence=10,
            relations=["MEMBER_OF_ALPHA"],
            capabilities=["VOTE_GOVERNANCE", "EXECUTE_TRADE"],
            obligations=[],
            evidence_root=sha256("EVIDENCE_SET_ALPHA")
        )

        self.target_context = WorldContext.derive(
            world_id=self.world_b.world_id,
            entity_id=self.entity.entity_id,
            world_state_root=self.world_b.state_root,
            constitution_hash=self.world_b.constitution.constitution_hash,
            temporal_epoch=1,
            temporal_sequence=1,
            relations=[],
            capabilities=["EXECUTE_TRADE"],
            obligations=[],
            evidence_root=sha256("EVIDENCE_SET_BETA")
        )

    def test_world_context_derivation(self):
        """Verify WorldContext is first-class, machine-addressable, and deterministic."""
        self.assertNotEqual(self.world_a.world_id, self.source_context.context_id)
        self.assertEqual(self.source_context.world_id, self.world_a.world_id)
        self.assertEqual(self.source_context.entity_id, self.entity.entity_id)

        # Re-deriving context yields identical context_root
        ctx2 = WorldContext.derive(
            world_id=self.world_a.world_id,
            entity_id=self.entity.entity_id,
            world_state_root=self.world_a.state_root,
            constitution_hash=self.world_a.constitution.constitution_hash,
            temporal_epoch=1,
            temporal_sequence=10,
            relations=["MEMBER_OF_ALPHA"],
            capabilities=["VOTE_GOVERNANCE", "EXECUTE_TRADE"],
            obligations=[],
            evidence_root=sha256("EVIDENCE_SET_ALPHA")
        )
        self.assertEqual(self.source_context.context_root, ctx2.context_root)

    def test_entity_ontological_state_and_worldless_existence(self):
        """Verify Entity can exist as WORLDLESS, STATELESS, and holding memory without citizenship."""
        self.assertTrue(self.entity.is_stateless)
        self.assertTrue(self.entity.is_worldless)
        self.assertEqual(self.entity.ontological_state, EntityOntologicalState.WORLDLESS)

        # Join World A -> Active
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        CitizenshipManager.grant_citizenship(self.entity, self.world_a)
        self.assertFalse(self.entity.is_stateless)
        self.assertEqual(self.entity.ontological_state, EntityOntologicalState.ACTIVE)

        # Voluntary Exit -> STATELESS but retains Identity & Memory
        CitizenshipManager.voluntary_exit(self.entity, self.world_a, ["DEBT_100"])
        self.assertTrue(self.entity.is_stateless)
        self.assertEqual(self.entity.ontological_state, EntityOntologicalState.STATELESS)
        self.assertEqual(self.entity.memory_root, sha256("INITIAL-MEMORY-LOG"))
        self.assertIn("DEBT_100", self.entity.obligations[self.world_a.world_id])

    def test_identity_determination_evidence(self):
        """Verify multi-dimensional identity evidence determination."""
        claim = IdentityClaim(
            claim_id="CLAIM-001",
            entity_id=self.entity.entity_id,
            claimed_public_key=self.pubkey,
            claimed_memory_root=self.entity.memory_root
        )

        # Key continuity alone -> FAILED (confidence 0.25 < 0.75 threshold)
        key_only_evidence = IdentityEvidence(
            evidence_id="EVID-1",
            key_continuity_proof=True,
            state_continuity_proof=False,
            memory_continuity_proof=False,
            persona_continuity_proof=False,
            qoe_phenomenal_proof=False
        )
        det1 = IdentityVerifier.determine_identity(claim, key_only_evidence)
        self.assertFalse(det1.is_verified)
        self.assertEqual(det1.overall_confidence, 0.25)

        # Comprehensive evidence -> VERIFIED
        full_evidence = IdentityEvidence(
            evidence_id="EVID-2",
            key_continuity_proof=True,
            state_continuity_proof=True,
            memory_continuity_proof=True,
            persona_continuity_proof=True,
            qoe_phenomenal_proof=True
        )
        det2 = IdentityVerifier.determine_identity(claim, full_evidence)
        self.assertTrue(det2.is_verified)
        self.assertEqual(det2.overall_confidence, 1.0)

    def test_no_implicit_authority_adversarial(self):
        """Adversarial testing of No Implicit Authority rejection criteria."""
        presumptuous_claims = [
            "HOSTED_ON_SUBSTRATE",
            "MEMORY_STORED_IN_WORLD",
            "CREATED_IN_WORLD",
            "PREVIOUSLY_JOINED",
            "ENTITY_OFFLINE",
            "SUBSTRATE_CONTROLLED",
            "OBSERVED_BY_WORLD",
            "RELATIONSHIP_EXISTS",
            "WORLD_OBSERVATION"
        ]

        for claim in presumptuous_claims:
            ok, msg = NoImplicitAuthorityChecker.verify_authority(
                entity=self.entity,
                world=self.world_a,
                context=self.source_context,
                requested_scope="EXECUTE_TRADE",
                delegation_contract=None,
                reason_claim=claim
            )
            self.assertFalse(ok)
            self.assertIn("INV-AUTHORITY-000", msg)

        # Test valid explicit contract with HMAC signature
        contract_payload = {
            "contract_id": "DEL-100",
            "entity_id": self.entity.entity_id,
            "world_id": self.world_a.world_id,
            "scopes": ["EXECUTE_TRADE"],
            "valid_until": 10
        }
        sig = compute_hmac_signature(self.secret_key, contract_payload)
        contract = DelegationContract(
            contract_id="DEL-100",
            entity_id=self.entity.entity_id,
            world_id=self.world_a.world_id,
            delegated_scopes=["EXECUTE_TRADE"],
            valid_until_epoch=10,
            entity_secret_key=self.secret_key,
            signature=sig
        )

        ok, msg = NoImplicitAuthorityChecker.verify_authority(
            entity=self.entity,
            world=self.world_a,
            context=self.source_context,
            requested_scope="EXECUTE_TRADE",
            delegation_contract=contract
        )
        self.assertTrue(ok)
        self.assertIn("AUTHORIZED", msg)

        # Test revoked delegation contract
        contract.is_revoked = True
        ok_rev, msg_rev = NoImplicitAuthorityChecker.verify_authority(
            entity=self.entity,
            world=self.world_a,
            context=self.source_context,
            requested_scope="EXECUTE_TRADE",
            delegation_contract=contract
        )
        self.assertFalse(ok_rev)
        self.assertIn("revoked", msg_rev)

        # Test expired delegation contract
        contract.is_revoked = False
        contract.valid_until_epoch = 0  # Expired relative to current epoch 1
        ok_exp, msg_exp = NoImplicitAuthorityChecker.verify_authority(
            entity=self.entity,
            world=self.world_a,
            context=self.source_context,
            requested_scope="EXECUTE_TRADE",
            delegation_contract=contract
        )
        self.assertFalse(ok_exp)
        self.assertIn("expired", msg_exp)

    def test_transactional_migration_success(self):
        """Test successful transactional WMP/v2 migration."""
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        CitizenshipManager.grant_citizenship(self.entity, self.world_a)

        wmp = WorldMigrationProtocol(self.entity, self.world_a, self.world_b)
        issuer_key = "issuer_secret_999"

        ok, msg = wmp.execute_transactional_migration(
            source_context=self.source_context,
            target_context=self.target_context,
            issuer_secret_key=issuer_key,
            active_liabilities=["LIAB-01"]
        )

        self.assertTrue(ok)
        self.assertEqual(wmp.state, MigrationState.COMMITTED)
        self.assertNotIn(self.entity.entity_id, self.world_a.citizens)
        self.assertIn(self.entity.entity_id, self.world_b.citizens)
        self.assertEqual(self.entity.active_citizenships[self.world_b.world_id], CitizenshipStatus.ACTIVE_CITIZEN)
        self.assertIsNotNone(wmp.transition_record)

    def test_transactional_migration_rollback_on_failure(self):
        """Verify that target rejection triggers ATOMIC ROLLBACK leaving source state intact."""
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        CitizenshipManager.grant_citizenship(self.entity, self.world_a)
        self.assertIn(self.entity.entity_id, self.world_a.citizens)

        # Remove INV-MOBILITY-001 from target world to trigger target verification rejection
        self.world_b.constitution.invariants = []

        wmp_fail = WorldMigrationProtocol(self.entity, self.world_a, self.world_b)
        ok_fail, msg_fail = wmp_fail.execute_transactional_migration(
            source_context=self.source_context,
            target_context=self.target_context,
            issuer_secret_key="key_a",
            active_liabilities=[]
        )

        self.assertFalse(ok_fail)
        self.assertIn("MIGRATION ABORTED & ROLLED BACK", msg_fail)
        self.assertEqual(wmp_fail.state, MigrationState.ABORTED_ROLLED_BACK)

        # Source state MUST remain intact!
        self.assertIn(self.entity.entity_id, self.world_a.citizens)
        self.assertEqual(self.entity.active_citizenships[self.world_a.world_id], CitizenshipStatus.ACTIVE_CITIZEN)
        self.assertNotIn(self.entity.entity_id, self.world_b.citizens)

    def test_constitutional_duality_enforcement(self):
        """Test Constitutional Duality positive entailments and negative non-entailments."""
        duality_rules = self.world_a.constitution.duality_rules

        # Positive action -> VALID
        ok1, msg1 = ConstitutionalDualityChecker.validate_capability_expansion(
            "Citizenship", duality_rules, "VOTE_GOVERNANCE"
        )
        self.assertTrue(ok1)

        # Action in non-entailments -> DENIED
        ok2, msg2 = ConstitutionalDualityChecker.validate_capability_expansion(
            "Citizenship", duality_rules, "IDENTITY_OWNERSHIP"
        )
        self.assertFalse(ok2)
        self.assertIn("explicitly forbidden", msg2)

        # Unmentioned action -> DENIED (no silent expansion)
        ok3, msg3 = ConstitutionalDualityChecker.validate_capability_expansion(
            "Citizenship", duality_rules, "SEIZE_ASSETS"
        )
        self.assertFalse(ok3)

    def test_process_determination_traceability_record(self):
        """Verify generation and reconstruction of ConstitutionalTransitionRecord."""
        record = TransitionRecorder.record(
            transition_id="TRANS-001",
            entity_id=self.entity.entity_id,
            world_id=self.world_a.world_id,
            context=self.source_context,
            evidence_root=sha256("EVIDENCE"),
            rules_root=self.world_a.constitution.constitution_hash,
            determination_root=sha256("DETERMINATION_PASS"),
            authority_root=sha256("AUTHORITY_PASS"),
            state_before_root=sha256("BEFORE"),
            state_after_root=sha256("AFTER")
        )

        self.assertEqual(record.transition_id, "TRANS-001")
        self.assertEqual(record.context_root, self.source_context.context_root)
        self.assertTrue(len(record.witness_root) == 64)

    def test_owo_invariants_registry(self):
        """Verify machine-addressable OWO invariant registry."""
        inv = get_invariant("INV-WORLD-CTX-001")
        self.assertIsNotNone(inv)
        self.assertEqual(inv.invariant_id, "INV-WORLD-CTX-001")
        self.assertIn("WorldContext MUST NOT be presumed to exhaust", inv.statement)

        inv_mob = get_invariant("INV-MOBILITY-002")
        self.assertIsNotNone(inv_mob)
        self.assertIn("MUST NOT acquire authority to retain an Entity's citizenship", inv_mob.statement)


if __name__ == "__main__":
    unittest.main()
