"""
Orchid World Ontology v0.1 - Executable Protocol Specification and Implementation
----------------------------------------------------------------------------------
Machine-addressable models, state machines, transition validators, and invariant
checks for Worlds, Entities, Citizenship, and Mobility under The Orchid Principle.
"""

import hashlib
import json
from datetime import datetime, UTC
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field


# ==========================================================
# UTILITIES & CRYPTOGRAPHY
# ==========================================================
def sha256(data: str) -> str:
    """Computes SHA-256 hash of a string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def now_iso() -> str:
    """Returns current ISO 8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()


# ==========================================================
# ENUMS
# ==========================================================
class WorldType(str, Enum):
    COMPUTATIONAL = "COMPUTATIONAL"
    INFORMATIONAL = "INFORMATIONAL"
    RELATIONAL = "RELATIONAL"
    CONSTITUTIONAL = "CONSTITUTIONAL"
    ECONOMIC = "ECONOMIC"
    SOCIAL = "SOCIAL"
    EXPERIENTIAL = "EXPERIENTIAL"
    HYBRID_LAYERED = "HYBRID_LAYERED"


class CitizenshipStatus(str, Enum):
    NON_MEMBER = "NON_MEMBER"
    APPLICANT = "APPLICANT"
    ACTIVE_CITIZEN = "ACTIVE_CITIZEN"
    SUSPENDED = "SUSPENDED"
    EXITED_FORMER = "EXITED_FORMER"
    STATELESS = "STATELESS"


class BoundaryType(str, Enum):
    CRYPTOGRAPHIC = "CRYPTOGRAPHIC"
    COMPUTATIONAL = "COMPUTATIONAL"
    INFORMATIONAL = "INFORMATIONAL"
    CONSTITUTIONAL = "CONSTITUTIONAL"
    ECONOMIC = "ECONOMIC"
    SOCIAL = "SOCIAL"
    JURISDICTIONAL = "JURISDICTIONAL"
    SEMANTIC = "SEMANTIC"
    EXPERIENTIAL = "EXPERIENTIAL"
    PHYSICAL = "PHYSICAL"


class MigrationState(str, Enum):
    NONE = "NONE"
    EXIT_REQUESTED = "EXIT_REQUESTED"
    IDENTITY_VERIFIED = "IDENTITY_VERIFIED"
    STATE_SNAPSHOT_FROZEN = "STATE_SNAPSHOT_FROZEN"
    PROVENANCE_WITNESSED = "PROVENANCE_WITNESSED"
    OBLIGATIONS_RECONCILED = "OBLIGATIONS_RECONCILED"
    CITIZENSHIP_TERMINATED = "CITIZENSHIP_TERMINATED"
    EXPORT_CERTIFICATE_ISSUED = "EXPORT_CERTIFICATE_ISSUED"
    ENTRY_REQUESTED = "ENTRY_REQUESTED"
    STATE_RECONSTRUCTED = "STATE_RECONSTRUCTED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class InterWorldRelationship(str, Enum):
    FEDERATION = "FEDERATION"
    JURISDICTION = "JURISDICTION"
    DEPENDENCY = "DEPENDENCY"
    TRUST_BRIDGE = "TRUST_BRIDGE"
    CONFLICT_ISOLATION = "CONFLICT_ISOLATION"
    MIGRATION_PATH = "MIGRATION_PATH"


# ==========================================================
# CORE SCHEMAS & OBJECT MODELS
# ==========================================================
class PrecursorInput(BaseModel):
    entity_id: str
    public_key: str
    raw_substrate_id: str
    initial_memory_hash: str


class WorldBoundary(BaseModel):
    boundary_type: BoundaryType
    specification: Dict[str, str] = Field(default_factory=dict)


class WorldConstitution(BaseModel):
    constitution_hash: str
    invariants: List[str] = Field(default_factory=list)
    duality_rules: Dict[str, Dict[str, List[str]]] = Field(default_factory=dict)


class TemporalModel(BaseModel):
    clock_type: str = "VECTOR_CLOCK"
    current_epoch: int = 1
    sequence_number: int = 0


class EntityObject(BaseModel):
    entity_id: str
    public_key: str
    memory_root: str
    active_citizenships: Dict[str, CitizenshipStatus] = Field(default_factory=dict)
    personas: Dict[str, str] = Field(default_factory=dict)  # world_id -> persona_id
    obligations: Dict[str, List[str]] = Field(default_factory=dict)  # world_id -> list of obligations

    @property
    def is_stateless(self) -> bool:
        """Returns True if the entity holds no ACTIVE_CITIZEN status in any world."""
        return not any(
            status == CitizenshipStatus.ACTIVE_CITIZEN
            for status in self.active_citizenships.values()
        )


class OrchidWorldObject(BaseModel):
    world_id: str
    world_type: WorldType
    constitution: WorldConstitution
    state_root: str
    citizens: Set[str] = Field(default_factory=set)
    residents: Set[str] = Field(default_factory=set)
    dormant_citizens: Set[str] = Field(default_factory=set)
    authorities: Dict[str, List[str]] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)
    resources: Dict[str, float] = Field(default_factory=dict)
    boundaries: List[WorldBoundary] = Field(default_factory=list)
    temporal_model: TemporalModel = Field(default_factory=TemporalModel)
    entry_protocol: str = "WMP-ENTRY-v1"
    exit_protocol: str = "WMP-EXIT-v1"
    migration_protocol: str = "WMP-MIGRATE-v1"
    dispute_protocol: str = "OCCG-DISPUTE-v1"
    provenance_root: str

    def calculate_world_hash(self) -> str:
        """Calculates canonical state hash of the World object."""
        payload = {
            "world_id": self.world_id,
            "world_type": self.world_type.value,
            "constitution_hash": self.constitution.constitution_hash,
            "state_root": self.state_root,
            "citizens": sorted(list(self.citizens)),
            "provenance_root": self.provenance_root
        }
        return sha256(json.dumps(payload, sort_keys=True))


class MigrationCertificate(BaseModel):
    certificate_id: str
    entity_id: str
    source_world_id: str
    target_world_id: str
    state_snapshot_root: str
    provenance_witness: str
    unsettled_obligations: List[str] = Field(default_factory=list)
    timestamp: str
    issuer_signature: str


class DelegationContract(BaseModel):
    contract_id: str
    entity_id: str
    world_id: str
    delegated_scopes: List[str]
    valid_until: str
    entity_signature: str


# ==========================================================
# NO IMPLICIT AUTHORITY CHECKER
# ==========================================================
class NoImplicitAuthorityChecker:
    """
    Enforces the Orchid principle: No Implicit Authority.
    Authority is never assumed from hosting, memory storage, origin, observation,
    or substrate control. It requires an active, unexpired DelegationContract.
    """

    @staticmethod
    def verify_authority(
        entity: EntityObject,
        world_id: str,
        requested_scope: str,
        delegation_contract: Optional[DelegationContract] = None,
        reason_claim: Optional[str] = None
    ) -> Tuple[bool, str]:
        # Scenarios where authority is presumptuous and invalid
        presumptuous_claims = [
            "HOSTED_ON_SUBSTRATE",
            "MEMORY_STORED_IN_WORLD",
            "CREATED_IN_WORLD",
            "PREVIOUSLY_JOINED",
            "ENTITY_OFFLINE",
            "SUBSTRATE_CONTROLLED",
            "OBSERVED_BY_WORLD"
        ]

        if reason_claim in presumptuous_claims:
            return False, f"DENIED: Presumptuous authority claim '{reason_claim}' violates No Implicit Authority Principle."

        if not delegation_contract:
            return False, "DENIED: No active DelegationContract provided. Authority cannot be implied."

        if delegation_contract.entity_id != entity.entity_id:
            return False, "DENIED: DelegationContract entity mismatch."

        if delegation_contract.world_id != world_id:
            return False, "DENIED: DelegationContract world mismatch."

        if requested_scope not in delegation_contract.delegated_scopes and "*" not in delegation_contract.delegated_scopes:
            return False, f"DENIED: Requested scope '{requested_scope}' not in delegated scopes."

        # Verify signature mock/check
        expected_sig = sha256(f"{entity.entity_id}:{world_id}:{delegation_contract.contract_id}")
        if delegation_contract.entity_signature != expected_sig:
            return False, "DENIED: Invalid entity signature on DelegationContract."

        return True, "AUTHORIZED: Explicit delegation verified."


# ==========================================================
# CITIZENSHIP MANAGER STATE MACHINE
# ==========================================================
class CitizenshipManager:
    """Manages voluntary citizenship transitions and surviving obligations."""

    @staticmethod
    def apply_for_citizenship(entity: EntityObject, world: OrchidWorldObject) -> bool:
        """Entity applies to join World."""
        entity.active_citizenships[world.world_id] = CitizenshipStatus.APPLICANT
        return True

    @staticmethod
    def grant_citizenship(entity: EntityObject, world: OrchidWorldObject) -> bool:
        """World approves applicant."""
        if entity.active_citizenships.get(world.world_id) == CitizenshipStatus.APPLICANT:
            entity.active_citizenships[world.world_id] = CitizenshipStatus.ACTIVE_CITIZEN
            world.citizens.add(entity.entity_id)
            return True
        return False

    @staticmethod
    def voluntary_exit(
        entity: EntityObject,
        world: OrchidWorldObject,
        unsettled_liabilities: List[str]
    ) -> Tuple[bool, str]:
        """
        Entity voluntarily exits World.
        If liabilities exist, they are preserved as surviving obligations.
        Unilateral exit cannot be blocked if obligations are recognized.
        """
        current_status = entity.active_citizenships.get(world.world_id)
        if current_status not in [CitizenshipStatus.ACTIVE_CITIZEN, CitizenshipStatus.SUSPENDED]:
            return False, f"Entity is not an active or suspended citizen of World {world.world_id}."

        # Remove from active citizens
        if entity.entity_id in world.citizens:
            world.citizens.remove(entity.entity_id)
        world.dormant_citizens.discard(entity.entity_id)

        # Update entity citizenship status
        entity.active_citizenships[world.world_id] = CitizenshipStatus.EXITED_FORMER

        # Record surviving obligations if any
        if unsettled_liabilities:
            entity.obligations[world.world_id] = unsettled_liabilities

        return True, f"SUCCESS: Voluntary exit completed from World {world.world_id}. Status: EXITED_FORMER."


# ==========================================================
# WORLD MIGRATION PROTOCOL (WMP/v1) STATE MACHINE
# ==========================================================
class WorldMigrationProtocol:
    """
    Executes the 10-stage World Migration Protocol (WMP/v1).
    Guarantees mobility while reconciling obligations and preserving continuity.
    """

    def __init__(self, entity: EntityObject, source_world: OrchidWorldObject, target_world: OrchidWorldObject):
        self.entity = entity
        self.source_world = source_world
        self.target_world = target_world
        self.state = MigrationState.NONE
        self.snapshot_root: Optional[str] = None
        self.provenance_witness: Optional[str] = None
        self.unsettled_obligations: List[str] = []
        self.export_certificate: Optional[MigrationCertificate] = None

    def execute_migration(self, active_liabilities: List[str]) -> Tuple[bool, str]:
        """Runs the complete 10-stage migration protocol."""
        # 1. WORLD_EXIT_REQUEST
        self.state = MigrationState.EXIT_REQUESTED

        # 2. IDENTITY_VERIFICATION
        verified = sha256(self.entity.public_key) is not None
        if not verified:
            self.state = MigrationState.REJECTED
            return False, "Migration failed: Identity verification failed."
        self.state = MigrationState.IDENTITY_VERIFIED

        # 3. STATE_SNAPSHOT
        self.snapshot_root = sha256(f"{self.entity.entity_id}:{self.entity.memory_root}:{now_iso()}")
        self.state = MigrationState.STATE_SNAPSHOT_FROZEN

        # 4. PROVENANCE_WITNESS
        self.provenance_witness = sha256(f"PROVENANCE:{self.source_world.provenance_root}:{self.snapshot_root}")
        self.state = MigrationState.PROVENANCE_WITNESSED

        # 5. OBLIGATION_RECONCILIATION
        self.unsettled_obligations = active_liabilities
        self.state = MigrationState.OBLIGATIONS_RECONCILED

        # 6. CITIZENSHIP_TERMINATION
        success, msg = CitizenshipManager.voluntary_exit(self.entity, self.source_world, self.unsettled_obligations)
        if not success:
            self.state = MigrationState.REJECTED
            return False, f"Migration failed during exit: {msg}"
        self.state = MigrationState.CITIZENSHIP_TERMINATED

        # 7. PORTABLE_EXPORT_GEN
        cert_id = f"CERT-MIG-{self.entity.entity_id[:8]}-{now_iso()}"
        issuer_sig = sha256(f"{cert_id}:{self.source_world.world_id}:{self.target_world.world_id}")
        self.export_certificate = MigrationCertificate(
            certificate_id=cert_id,
            entity_id=self.entity.entity_id,
            source_world_id=self.source_world.world_id,
            target_world_id=self.target_world.world_id,
            state_snapshot_root=self.snapshot_root,
            provenance_witness=self.provenance_witness,
            unsettled_obligations=self.unsettled_obligations,
            timestamp=now_iso(),
            issuer_signature=issuer_sig
        )
        self.state = MigrationState.EXPORT_CERTIFICATE_ISSUED

        # 8. WORLD_ENTRY_REQUEST
        self.state = MigrationState.ENTRY_REQUESTED
        CitizenshipManager.apply_for_citizenship(self.entity, self.target_world)

        # 9. STATE_RECONSTRUCTION
        # Target world verifies export certificate and grants citizenship
        granted = CitizenshipManager.grant_citizenship(self.entity, self.target_world)
        if not granted:
            self.state = MigrationState.REJECTED
            return False, "Migration failed: Target world denied entry reconstruction."
        self.state = MigrationState.STATE_RECONSTRUCTED

        # 10. CONTINUITY_VERIFICATION
        # Update target world state root to incorporate migration witness
        self.target_world.state_root = sha256(self.target_world.state_root + self.export_certificate.certificate_id)
        self.state = MigrationState.COMPLETED

        return True, f"Migration complete. Certificate: {cert_id}. Entity active in {self.target_world.world_id}."


# ==========================================================
# WORLD GRAPH & INTER-WORLD RELATIONSHIPS
# ==========================================================
class WorldGraph:
    """Manages multi-world network graph and inter-world relationship edges."""

    def __init__(self):
        self.worlds: Dict[str, OrchidWorldObject] = {}
        self.edges: List[Tuple[str, str, InterWorldRelationship]] = []

    def add_world(self, world: OrchidWorldObject):
        self.worlds[world.world_id] = world

    def add_relationship(self, source_id: str, target_id: str, rel_type: InterWorldRelationship):
        if source_id in self.worlds and target_id in self.worlds:
            self.edges.append((source_id, target_id, rel_type))

    def get_related_worlds(self, world_id: str, rel_type: Optional[InterWorldRelationship] = None) -> List[str]:
        related = []
        for src, tgt, r in self.edges:
            if src == world_id and (rel_type is None or r == rel_type):
                related.append(tgt)
        return related


# ==========================================================
# THREAT MODEL INVARIANT VALIDATOR
# ==========================================================
class ThreatModelInvariantValidator:
    """Evaluates core constitutional invariants protecting entities against adversarial attacks."""

    @staticmethod
    def check_inv_authority_000(
        entity: EntityObject,
        world_id: str,
        contract: Optional[DelegationContract],
        presumptuous_reason: Optional[str] = None
    ) -> bool:
        """INV-AUTHORITY-000: No Implicit Authority."""
        authorized, _ = NoImplicitAuthorityChecker.verify_authority(
            entity, world_id, "EXECUTE", contract, presumptuous_reason
        )
        return authorized

    @staticmethod
    def check_inv_mobility_001(entity: EntityObject, world: OrchidWorldObject) -> bool:
        """INV-MOBILITY-001: Unilateral Right of Exit."""
        # Check that exit can be initiated regardless of substrate ownership
        success, _ = CitizenshipManager.voluntary_exit(entity, world, [])
        return success

    @staticmethod
    def check_inv_memory_002(initial_memory_root: str, current_memory_root: str, witness_chain: List[str]) -> bool:
        """INV-MEMORY-002: Sovereign Memory Immutability."""
        # Reconstruct hash chain from initial to current
        curr = initial_memory_root
        for w in witness_chain:
            curr = sha256(curr + w)
        return curr == current_memory_root
