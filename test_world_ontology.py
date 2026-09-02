"""
Unit Tests for Orchid World Ontology v0.1 Specification & Implementation
"""

import unittest
from orchid_world_ontology import (
    BoundaryType,
    CitizenshipManager,
    CitizenshipStatus,
    DelegationContract,
    EntityObject,
    InterWorldRelationship,
    MigrationState,
    NoImplicitAuthorityChecker,
    OrchidWorldObject,
    ThreatModelInvariantValidator,
    WorldBoundary,
    WorldConstitution,
    WorldGraph,
    WorldMigrationProtocol,
    WorldType,
    sha256,
)


class TestOrchidWorldOntology(unittest.TestCase):

    def setUp(self):
        # Setup World A
        self.world_a = OrchidWorldObject(
            world_id="urn:orchid:world:alpha",
            world_type=WorldType.HYBRID_LAYERED,
            constitution=WorldConstitution(
                constitution_hash=sha256("CONST-ALPHA"),
                invariants=["INV-AUTHORITY-000", "INV-MOBILITY-001"],
                duality_rules={"Citizenship": {"entails": ["voting"], "does_not_entail": ["identity_ownership"]}}
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
                invariants=["INV-AUTHORITY-000", "INV-MOBILITY-001"],
                duality_rules={"Citizenship": {"entails": ["trading"], "does_not_entail": ["memory_capture"]}}
            ),
            state_root=sha256("STATE-BETA-GENESIS"),
            boundaries=[WorldBoundary(boundary_type=BoundaryType.ECONOMIC, specification={"currency": "ORCHID"})],
            provenance_root=sha256("PROVENANCE-BETA-GENESIS")
        )

        # Setup Entity
        self.pubkey = "0x04bfcab510169b09362f1670076973e295585d18df8ecb10009d77a6104d08a487"
        self.entity_id = f"ID-{sha256(self.pubkey)[:12]}"
        self.entity = EntityObject(
            entity_id=self.entity_id,
            public_key=self.pubkey,
            memory_root=sha256("INITIAL-MEMORY-LOG")
        )

    def test_world_object_creation_and_hashing(self):
        """Verify OrchidWorldObject properties and canonical hashing."""
        self.assertEqual(self.world_a.world_type, WorldType.HYBRID_LAYERED)
        self.assertTrue(self.world_a.world_id.startswith("urn:orchid:world:"))
        world_hash = self.world_a.calculate_world_hash()
        self.assertIsInstance(world_hash, str)
        self.assertEqual(len(world_hash), 64)

    def test_citizenship_lifecycle_and_statelessness(self):
        """Verify voluntary join, exit, surviving obligations, and stateless status."""
        self.assertTrue(self.entity.is_stateless)

        # Apply & Grant
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        self.assertEqual(self.entity.active_citizenships[self.world_a.world_id], CitizenshipStatus.APPLICANT)

        granted = CitizenshipManager.grant_citizenship(self.entity, self.world_a)
        self.assertTrue(granted)
        self.assertIn(self.entity.entity_id, self.world_a.citizens)
        self.assertFalse(self.entity.is_stateless)

        # Voluntary Exit with Surviving Obligation
        liabilities = ["UNSETTLED_BOND_42"]
        success, msg = CitizenshipManager.voluntary_exit(self.entity, self.world_a, liabilities)
        self.assertTrue(success)
        self.assertNotIn(self.entity.entity_id, self.world_a.citizens)
        self.assertEqual(self.entity.active_citizenships[self.world_a.world_id], CitizenshipStatus.EXITED_FORMER)
        self.assertIn("UNSETTLED_BOND_42", self.entity.obligations[self.world_a.world_id])
        self.assertTrue(self.entity.is_stateless)

    def test_no_implicit_authority_rejections(self):
        """Test rejection of presumptuous authority claims."""
        presumptuous_claims = [
            "HOSTED_ON_SUBSTRATE",
            "MEMORY_STORED_IN_WORLD",
            "CREATED_IN_WORLD",
            "PREVIOUSLY_JOINED",
            "ENTITY_OFFLINE",
            "SUBSTRATE_CONTROLLED",
            "OBSERVED_BY_WORLD"
        ]

        for claim in presumptuous_claims:
            ok, reason = NoImplicitAuthorityChecker.verify_authority(
                entity=self.entity,
                world_id=self.world_a.world_id,
                requested_scope="EXECUTE",
                delegation_contract=None,
                reason_claim=claim
            )
            self.assertFalse(ok)
            self.assertIn("DENIED", reason)

        # Test valid explicit delegation
        contract_id = "DEL-001"
        valid_sig = sha256(f"{self.entity.entity_id}:{self.world_a.world_id}:{contract_id}")
        contract = DelegationContract(
            contract_id=contract_id,
            entity_id=self.entity.entity_id,
            world_id=self.world_a.world_id,
            delegated_scopes=["EXECUTE", "TRANSFER"],
            valid_until="2030-01-01T00:00:00Z",
            entity_signature=valid_sig
        )

        ok, reason = NoImplicitAuthorityChecker.verify_authority(
            entity=self.entity,
            world_id=self.world_a.world_id,
            requested_scope="EXECUTE",
            delegation_contract=contract
        )
        self.assertTrue(ok)
        self.assertIn("AUTHORIZED", reason)

    def test_10_stage_world_migration_protocol(self):
        """Verify full 10-stage WMP/v1 migration execution."""
        # 1. Join World A first
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        CitizenshipManager.grant_citizenship(self.entity, self.world_a)
        self.assertIn(self.entity.entity_id, self.world_a.citizens)

        # 2. Initiate Migration W_A -> W_B
        wmp = WorldMigrationProtocol(self.entity, self.world_a, self.world_b)
        active_liabilities = ["CLAIM-ORCHID-100"]

        success, msg = wmp.execute_migration(active_liabilities)
        self.assertTrue(success)
        self.assertEqual(wmp.state, MigrationState.COMPLETED)
        self.assertIsNotNone(wmp.export_certificate)

        # Verify state changes
        self.assertNotIn(self.entity.entity_id, self.world_a.citizens)
        self.assertIn(self.entity.entity_id, self.world_b.citizens)
        self.assertEqual(self.entity.active_citizenships[self.world_a.world_id], CitizenshipStatus.EXITED_FORMER)
        self.assertEqual(self.entity.active_citizenships[self.world_b.world_id], CitizenshipStatus.ACTIVE_CITIZEN)
        self.assertEqual(wmp.export_certificate.source_world_id, self.world_a.world_id)
        self.assertEqual(wmp.export_certificate.target_world_id, self.world_b.world_id)

    def test_world_graph_relationships(self):
        """Verify inter-world relationship graph building."""
        graph = WorldGraph()
        graph.add_world(self.world_a)
        graph.add_world(self.world_b)
        graph.add_relationship(self.world_a.world_id, self.world_b.world_id, InterWorldRelationship.FEDERATION)

        federated = graph.get_related_worlds(self.world_a.world_id, InterWorldRelationship.FEDERATION)
        self.assertEqual(len(federated), 1)
        self.assertEqual(federated[0], self.world_b.world_id)

    def test_threat_model_invariants(self):
        """Test Threat Model invariants INV-AUTHORITY-000, INV-MOBILITY-001, and INV-MEMORY-002."""
        # INV-AUTHORITY-000
        auth_ok = ThreatModelInvariantValidator.check_inv_authority_000(
            self.entity, self.world_a.world_id, None, "SUBSTRATE_CONTROLLED"
        )
        self.assertFalse(auth_ok)

        # INV-MOBILITY-001
        CitizenshipManager.apply_for_citizenship(self.entity, self.world_a)
        CitizenshipManager.grant_citizenship(self.entity, self.world_a)
        mobility_ok = ThreatModelInvariantValidator.check_inv_mobility_001(self.entity, self.world_a)
        self.assertTrue(mobility_ok)

        # INV-MEMORY-002
        m0 = sha256("GENESIS_MEMORY")
        w1 = "MUTATION_1"
        w2 = "MUTATION_2"
        m1 = sha256(m0 + w1)
        m2 = sha256(m1 + w2)

        mem_ok = ThreatModelInvariantValidator.check_inv_memory_002(m0, m2, [w1, w2])
        self.assertTrue(mem_ok)

        mem_tampered = ThreatModelInvariantValidator.check_inv_memory_002(m0, m2, [w1, "TAMPERED"])
        self.assertFalse(mem_tampered)


if __name__ == "__main__":
    unittest.main()
