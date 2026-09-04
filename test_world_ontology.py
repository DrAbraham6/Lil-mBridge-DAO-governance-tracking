"""
Test Suite & Adversarial Threat Harness for Orchid World Ontology (OWO) v0.2
"""

import unittest
import uuid
from datetime import datetime, timezone

from owo_invariants import OWO_INVARIANTS, get_invariant
from orchid_world_ontology import (
    CryptoEngine,
    Entity,
    EntityState,
    EntityStateSnapshot,
    World,
    WorldContext,
    Delegation,
    NoImplicitAuthorityChecker,
    IdentityClaim,
    IdentityEvidence,
    IdentityVerification,
    IdentityDetermination,
    MigrationTransaction,
    MigrationPhase,
    ConstitutionalDuality,
    DEFAULT_CITIZENSHIP_DUALITY,
    ObligationRecord,
)


class TestOWOIdentity(unittest.TestCase):
    def setUp(self):
        self.entity = Entity(
            entity_id="entity_001",
            public_key="pubkey_abc123",
            secret_key="secret_xyz789",
            state=EntityState.ACTIVE,
            memories=["memory_1", "memory_2"],
            persona={"name": "Alice", "role": "Explorer"},
        )

    def test_key_continuity_does_not_equal_automatic_entity_continuity(self):
        """Test that cryptographic key continuity alone != total entity continuity if memory or state breaks."""
        evidence_broken_mem = IdentityEvidence(
            evidence_id="ev_001",
            claim_id="claim_001",
            key_proof=CryptoEngine.sign_payload(CryptoEngine.canonical_hash("ev_001"), "secret_xyz789"),
            state_proof=CryptoEngine.canonical_hash(EntityState.ACTIVE.value),
            memory_proof="CORRUPTED_MEMORY_HASH",
            persona_proof=CryptoEngine.canonical_hash({"name": "Alice", "role": "Explorer"}),
            qoe_proof="qoe_valid",
        )

        determination = self.entity.evaluate_identity(evidence_broken_mem)
        self.assertTrue(determination.is_identity_valid)
        self.assertFalse(determination.total_continuity_established)
        self.assertFalse(determination.verification.memory_continuity)

    def test_valid_identity_evidence(self):
        """Test complete valid identity determination."""
        evidence_valid = IdentityEvidence(
            evidence_id="ev_002",
            claim_id="claim_002",
            key_proof=CryptoEngine.sign_payload(CryptoEngine.canonical_hash("ev_002"), "secret_xyz789"),
            state_proof=CryptoEngine.canonical_hash(EntityState.ACTIVE.value),
            memory_proof=CryptoEngine.canonical_hash(["memory_1", "memory_2"]),
            persona_proof=CryptoEngine.canonical_hash({"name": "Alice", "role": "Explorer"}),
            qoe_proof="qoe_valid",
        )

        determination = self.entity.evaluate_identity(evidence_valid)
        self.assertTrue(determination.is_identity_valid)
        self.assertTrue(determination.total_continuity_established)
        self.assertTrue(determination.verification.cryptographic_key_continuity)
        self.assertTrue(determination.verification.memory_continuity)


class TestOWOAuthority(unittest.TestCase):
    def setUp(self):
        self.entity_id = "entity_001"
        self.world_id = "world_alpha"
        self.secret_key = "world_secret_key"
        self.current_time = 1000

        self.valid_delegation = Delegation(
            delegation_id="del_001",
            entity_id=self.entity_id,
            world_id=self.world_id,
            scope="EXECUTE",
            granted_at=500,
            expires_at=1500,
            signature="",
        )
        self.valid_delegation.signature = CryptoEngine.sign_payload(
            self.valid_delegation.compute_hash(), self.secret_key
        )

    def test_expired_delegation_rejected(self):
        valid, reason = NoImplicitAuthorityChecker.validate_delegation(
            delegation=self.valid_delegation,
            entity_id=self.entity_id,
            world_id=self.world_id,
            requested_scope="EXECUTE",
            current_time=2000,
            signing_secret=self.secret_key,
            constitution_rules=["EXECUTE"],
        )
        self.assertFalse(valid)
        self.assertIn("Temporal invalidity", reason)

    def test_wrong_entity_rejected(self):
        valid, reason = NoImplicitAuthorityChecker.validate_delegation(
            delegation=self.valid_delegation,
            entity_id="entity_999",
            world_id=self.world_id,
            requested_scope="EXECUTE",
            current_time=1000,
            signing_secret=self.secret_key,
            constitution_rules=["EXECUTE"],
        )
        self.assertFalse(valid)
        self.assertIn("Entity binding mismatch", reason)

    def test_wrong_world_rejected(self):
        valid, reason = NoImplicitAuthorityChecker.validate_delegation(
            delegation=self.valid_delegation,
            entity_id=self.entity_id,
            world_id="world_beta",
            requested_scope="EXECUTE",
            current_time=1000,
            signing_secret=self.secret_key,
            constitution_rules=["EXECUTE"],
        )
        self.assertFalse(valid)
        self.assertIn("World binding mismatch", reason)

    def test_wrong_scope_rejected(self):
        valid, reason = NoImplicitAuthorityChecker.validate_delegation(
            delegation=self.valid_delegation,
            entity_id=self.entity_id,
            world_id=self.world_id,
            requested_scope="ADMIN_DELETE",
            current_time=1000,
            signing_secret=self.secret_key,
            constitution_rules=["EXECUTE", "ADMIN_DELETE"],
        )
        self.assertFalse(valid)
        self.assertIn("Scope mismatch", reason)

    def test_revoked_delegation_rejected(self):
        revoked_del = self.valid_delegation.model_copy()
        revoked_del.is_revoked = True
        revoked_del.signature = CryptoEngine.sign_payload(
            revoked_del.compute_hash(), self.secret_key
        )

        valid, reason = NoImplicitAuthorityChecker.validate_delegation(
            delegation=revoked_del,
            entity_id=self.entity_id,
            world_id=self.world_id,
            requested_scope="EXECUTE",
            current_time=1000,
            signing_secret=self.secret_key,
            constitution_rules=["EXECUTE"],
        )
        self.assertFalse(valid)
        self.assertIn("revoked", reason)

    def test_prohibited_implicit_grounds_rejected(self):
        """Adversarial test: Rejects claims based on hosting, storage, observation, substrate control, etc."""
        prohibited_grounds = [
            "OBSERVATION", "HOSTING", "STORAGE", "CREATION",
            "PREVIOUS_MEMBERSHIP", "OFFLINE_STATUS", "SUBSTRATE_CONTROL",
            "RELATIONSHIP", "WORLD_OBSERVATION"
        ]

        for ground in prohibited_grounds:
            valid, reason = NoImplicitAuthorityChecker.validate_delegation(
                delegation=self.valid_delegation,
                entity_id=self.entity_id,
                world_id=self.world_id,
                requested_scope="EXECUTE",
                current_time=1000,
                signing_secret=self.secret_key,
                constitution_rules=["EXECUTE"],
                ground_of_authority=ground,
            )
            self.assertFalse(valid, f"Ground '{ground}' should have been rejected!")
            self.assertIn("implicit non-authoritative ground", reason)


class TestOWOCitizenshipAndMobility(unittest.TestCase):
    def test_voluntary_join_and_exit(self):
        world = World(world_id="world_1")
        entity = Entity(entity_id="entity_1", public_key="pk_1", state=EntityState.WORLDLESS)

        rec = world.grant_citizenship(entity)
        self.assertTrue(world.has_citizen("entity_1"))
        self.assertEqual(entity.state, EntityState.ACTIVE)

        world.revoke_citizenship("entity_1")
        self.assertFalse(world.has_citizen("entity_1"))

    def test_exit_with_and_without_obligations(self):
        world = World(world_id="world_1")
        entity = Entity(
            entity_id="entity_2",
            public_key="pk_2",
            state=EntityState.ACTIVE,
            obligations=[
                ObligationRecord(
                    obligation_id="obl_1",
                    entity_id="entity_2",
                    world_id="world_1",
                    description="Unsettled Tax",
                    is_settled=False,
                    survives_exit=True,
                )
            ]
        )

        world.grant_citizenship(entity)
        world.revoke_citizenship("entity_2")
        self.assertFalse(world.has_citizen("entity_2"))
        self.assertEqual(len(entity.obligations), 1)
        self.assertFalse(entity.obligations[0].is_settled)

    def test_non_citizen_with_identity_and_worldless_entity(self):
        entity = Entity(entity_id="entity_3", public_key="pk_3", state=EntityState.WORLDLESS)
        self.assertEqual(entity.state, EntityState.WORLDLESS)
        self.assertIsNotNone(entity.public_key)

        entity.state = EntityState.NON_CITIZEN
        self.assertEqual(entity.state, EntityState.NON_CITIZEN)

    def test_multi_world_citizenship(self):
        world_a = World(world_id="world_a")
        world_b = World(world_id="world_b")
        entity = Entity(entity_id="entity_4", public_key="pk_4")

        world_a.grant_citizenship(entity)
        world_b.grant_citizenship(entity)

        self.assertTrue(world_a.has_citizen("entity_4"))
        self.assertTrue(world_b.has_citizen("entity_4"))


class TestOWOMigration(unittest.TestCase):
    def setUp(self):
        self.source_world = World(world_id="world_source", world_secret_key="src_secret")
        self.target_world = World(world_id="world_target", world_secret_key="tgt_secret")
        self.entity = Entity(
            entity_id="entity_migrant",
            public_key="pk_migrant",
            secret_key="sk_migrant",
            memories=["mem1"],
            state=EntityState.ACTIVE,
        )
        self.source_world.grant_citizenship(self.entity)

    def test_successful_migration(self):
        tx = MigrationTransaction(self.entity, self.source_world, self.target_world)

        self.assertTrue(tx.prepare())
        snapshot = tx.commit_snapshot()
        self.assertIsNotNone(snapshot.snapshot_root)

        prov_root = tx.witness_provenance()
        self.assertIsNotNone(prov_root)

        self.assertTrue(tx.reconcile_obligations())

        cert = tx.issue_export_certificate("src_secret")
        self.assertIsNotNone(cert.source_world_signature)

        valid, msg = tx.verify_certificate_at_target("src_secret")
        self.assertTrue(valid, msg)

        self.assertTrue(tx.reconstruct_state_at_target())

        evidence = IdentityEvidence(
            evidence_id="ev_mig",
            claim_id="claim_mig",
            key_proof=CryptoEngine.sign_payload(CryptoEngine.canonical_hash("ev_mig"), "sk_migrant"),
            state_proof=CryptoEngine.canonical_hash(EntityState.ACTIVE.value),
            memory_proof=CryptoEngine.canonical_hash(["mem1"]),
            persona_proof=CryptoEngine.canonical_hash({}),
            qoe_proof="valid_qoe",
        )
        determination = self.entity.evaluate_identity(evidence)

        self.assertTrue(tx.verify_continuity(determination))
        self.assertTrue(tx.commit_transition())

        self.assertTrue(self.target_world.has_citizen("entity_migrant"))
        self.assertFalse(self.source_world.has_citizen("entity_migrant"))
        self.assertEqual(tx.phase, MigrationPhase.SOURCE_TERMINATION_COMMITTED)

    def test_migration_failure_triggers_rollback(self):
        """Adversarial test: Target certificate verification fails, source citizenship remains intact."""
        tx = MigrationTransaction(self.entity, self.source_world, self.target_world)

        tx.prepare()
        tx.commit_snapshot()
        tx.witness_provenance()
        tx.reconcile_obligations()
        tx.issue_export_certificate("src_secret")

        valid, msg = tx.verify_certificate_at_target("WRONG_SECRET")
        self.assertFalse(valid)

        tx.rollback("Target certificate signature failed")

        self.assertEqual(tx.phase, MigrationPhase.ROLLED_BACK)
        self.assertTrue(self.source_world.has_citizen("entity_migrant"))
        self.assertFalse(self.target_world.has_citizen("entity_migrant"))

    def test_tampered_snapshot_rejected(self):
        tx = MigrationTransaction(self.entity, self.source_world, self.target_world)
        tx.prepare()
        tx.commit_snapshot()
        tx.witness_provenance()
        tx.reconcile_obligations()
        cert = tx.issue_export_certificate("src_secret")

        # Tamper snapshot root in certificate and resign with source secret
        cert.snapshot_root = "TAMPERED_ROOT"
        cert.source_world_signature = CryptoEngine.sign_payload(cert.compute_hash(), "src_secret")

        valid, msg = tx.verify_certificate_at_target("src_secret")
        self.assertFalse(valid)
        self.assertIn("Snapshot root mismatch", msg)


class TestConstitutionalDualityAndTraceability(unittest.TestCase):
    def test_constitutional_duality_enforcement(self):
        duality = DEFAULT_CITIZENSHIP_DUALITY

        valid, msg = duality.validate_claim("voting")
        self.assertTrue(valid)

        valid, msg = duality.validate_claim("identity_ownership")
        self.assertFalse(valid)
        self.assertIn("explicitly DOES NOT entail", msg)

        valid, msg = duality.validate_claim("god_mode_authority")
        self.assertFalse(valid)
        self.assertIn("not explicitly entailed", msg)

    def test_process_determination_traceability(self):
        world = World(world_id="world_tr", world_secret_key="secret_tr")
        entity = Entity(entity_id="entity_tr", public_key="pk_tr", state=EntityState.ACTIVE)
        world.grant_citizenship(entity)

        delegation = Delegation(
            delegation_id="del_tr",
            entity_id="entity_tr",
            world_id="world_tr",
            scope="EXECUTE",
            granted_at=0,
            expires_at=2000000000,
            signature="",
        )
        delegation.signature = CryptoEngine.sign_payload(delegation.compute_hash(), "secret_tr")

        success, msg, record = world.execute_transition(
            entity=entity,
            action="EXECUTE",
            delegation=delegation,
            signing_secret="secret_tr"
        )

        self.assertTrue(success, msg)
        self.assertIsNotNone(record)
        self.assertIsNotNone(record.transition_id)
        self.assertEqual(record.entity_id, "entity_tr")
        self.assertEqual(record.world_id, "world_tr")
        self.assertIsNotNone(record.context_root)
        self.assertIsNotNone(record.state_before_root)
        self.assertIsNotNone(record.state_after_root)


if __name__ == "__main__":
    unittest.main()
