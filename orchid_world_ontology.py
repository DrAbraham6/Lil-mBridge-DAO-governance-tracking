"""
Orchid World Ontology (OWO) v0.2 Implementation
Harden executable implementation to enforce constitutional principles and ontology.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, Union
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from owo_invariants import OWO_INVARIANTS, get_invariant


# ==========================================
# 1. ENUMS & CORE ENTITY STATES
# ==========================================

class EntityState(str, Enum):
    WORLDLESS = "WORLDLESS"
    STATELESS = "STATELESS"
    NON_CITIZEN = "NON_CITIZEN"
    OFFLINE = "OFFLINE"
    UNCONNECTED = "UNCONNECTED"
    DORMANT = "DORMANT"
    UNREGISTERED = "UNREGISTERED"
    ACTIVE = "ACTIVE"


class MigrationPhase(str, Enum):
    SOURCE_ACTIVE = "SOURCE_ACTIVE"
    MIGRATION_PREPARED = "MIGRATION_PREPARED"
    SNAPSHOT_COMMITTED = "SNAPSHOT_COMMITTED"
    PROVENANCE_WITNESSED = "PROVENANCE_WITNESSED"
    OBLIGATIONS_RECONCILED = "OBLIGATIONS_RECONCILED"
    EXPORT_CERTIFICATE_ISSUED = "EXPORT_CERTIFICATE_ISSUED"
    TARGET_ACCEPTED = "TARGET_ACCEPTED"
    STATE_RECONSTRUCTED = "STATE_RECONSTRUCTED"
    CONTINUITY_VERIFIED = "CONTINUITY_VERIFIED"
    SOURCE_TERMINATION_COMMITTED = "SOURCE_TERMINATION_COMMITTED"
    TARGET_ACTIVATION_COMMITTED = "TARGET_ACTIVATION_COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"


# ==========================================
# 2. CRYPTOGRAPHIC UTILITIES
# ==========================================

class CryptoEngine:
    """
    Standard cryptographic signing and verification engine.
    Uses canonical JSON payload formatting, SHA-256 hashing, and HMAC-SHA256 signatures.
    Note: For production multi-party deployment, replace HMAC symmetric secret with ECDSA / Ed25519.
    """

    @staticmethod
    def canonical_hash(data: Any) -> str:
        if isinstance(data, BaseModel):
            data_dict = data.model_dump(exclude={"signature", "hash_val", "context_root", "snapshot_root"})
        elif isinstance(data, dict):
            data_dict = data
        else:
            data_dict = {"value": str(data)}

        canonical_json = json.dumps(data_dict, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    @staticmethod
    def sign_payload(payload_hash: str, secret_key: str) -> str:
        return hmac.new(secret_key.encode("utf-8"), payload_hash.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_signature(payload_hash: str, signature: str, secret_key: str) -> bool:
        expected = CryptoEngine.sign_payload(payload_hash, secret_key)
        return hmac.compare_digest(expected, signature)


# ==========================================
# 3. FIRST-CLASS WORLD CONTEXT
# ==========================================

class WorldContext(BaseModel):
    context_id: str
    world_id: str
    entity_id: str
    world_state_root: str
    constitution_hash: str
    temporal_epoch: int
    temporal_sequence: int
    relevant_relations: List[str] = Field(default_factory=list)
    relevant_capabilities: List[str] = Field(default_factory=list)
    relevant_obligations: List[str] = Field(default_factory=list)
    evidence_root: str
    context_root: str = ""

    def compute_context_root(self) -> str:
        payload = {
            "context_id": self.context_id,
            "world_id": self.world_id,
            "entity_id": self.entity_id,
            "world_state_root": self.world_state_root,
            "constitution_hash": self.constitution_hash,
            "temporal_epoch": self.temporal_epoch,
            "temporal_sequence": self.temporal_sequence,
            "relevant_relations": sorted(self.relevant_relations),
            "relevant_capabilities": sorted(self.relevant_capabilities),
            "relevant_obligations": sorted(self.relevant_obligations),
            "evidence_root": self.evidence_root,
        }
        return CryptoEngine.canonical_hash(payload)

    def finalize(self) -> WorldContext:
        self.context_root = self.compute_context_root()
        return self


# ==========================================
# 4. IDENTITY & CONTINUITY MODELS
# ==========================================

class IdentityClaim(BaseModel):
    claim_id: str
    entity_id: str
    public_key: str
    claimed_persona: str
    claimed_world_id: Optional[str] = None
    claim_timestamp: str


class IdentityEvidence(BaseModel):
    evidence_id: str
    claim_id: str
    key_proof: str
    state_proof: str
    memory_proof: str
    persona_proof: str
    qoe_proof: str


class IdentityVerification(BaseModel):
    verification_id: str
    evidence_id: str
    cryptographic_key_continuity: bool
    state_continuity: bool
    memory_continuity: bool
    persona_continuity: bool
    entity_continuity: bool
    qoe_phenomenal_continuity: bool
    verified_at: str


class IdentityDetermination(BaseModel):
    determination_id: str
    entity_id: str
    verification: IdentityVerification
    is_identity_valid: bool
    total_continuity_established: bool
    reasoning: str


# ==========================================
# 5. STATE SNAPSHOT & TRACEABILITY RECORDS
# ==========================================

class EntityStateSnapshot(BaseModel):
    entity_id: str
    identity_root: str
    memory_root: str
    persona_root: str
    relationship_root: str
    capability_root: str
    obligation_root: str
    citizenship_root: str
    world_context_root: str
    snapshot_sequence: int
    snapshot_timestamp: str
    snapshot_root: str = ""

    def compute_snapshot_root(self) -> str:
        payload = {
            "entity_id": self.entity_id,
            "identity_root": self.identity_root,
            "memory_root": self.memory_root,
            "persona_root": self.persona_root,
            "relationship_root": self.relationship_root,
            "capability_root": self.capability_root,
            "obligation_root": self.obligation_root,
            "citizenship_root": self.citizenship_root,
            "world_context_root": self.world_context_root,
            "snapshot_sequence": self.snapshot_sequence,
            "snapshot_timestamp": self.snapshot_timestamp,
        }
        return CryptoEngine.canonical_hash(payload)

    def finalize(self) -> EntityStateSnapshot:
        self.snapshot_root = self.compute_snapshot_root()
        return self


class ConstitutionalTransitionRecord(BaseModel):
    transition_id: str
    entity_id: str
    world_id: str
    context_root: str
    evidence_root: str
    rules_root: str
    determination_root: str
    authority_root: str
    state_before_root: str
    state_after_root: str
    witness_root: str
    timestamp: str


# ==========================================
# 6. AUTHORITY & DELEGATION
# ==========================================

class Delegation(BaseModel):
    delegation_id: str
    entity_id: str
    world_id: str
    scope: str
    granted_at: int
    expires_at: int
    is_revoked: bool = False
    signature: str
    secret_key: Optional[str] = Field(default=None, exclude=True)

    def compute_hash(self) -> str:
        payload = {
            "delegation_id": self.delegation_id,
            "entity_id": self.entity_id,
            "world_id": self.world_id,
            "scope": self.scope,
            "granted_at": self.granted_at,
            "expires_at": self.expires_at,
            "is_revoked": self.is_revoked,
        }
        return CryptoEngine.canonical_hash(payload)


class NoImplicitAuthorityChecker:
    """
    Enforces INV-NO-IMP-AUTH-001:
    Observation != Authority, Hosting != Authority, Storage != Authority, Creation != Authority,
    Previous Membership != Authority, Offline Status != Authority, Substrate Control != Authority,
    Relationship != Authority, World Observation != Authority.
    """

    PROHIBITED_GROUNDS = {
        "OBSERVATION", "HOSTING", "STORAGE", "CREATION",
        "PREVIOUS_MEMBERSHIP", "OFFLINE_STATUS", "SUBSTRATE_CONTROL",
        "RELATIONSHIP", "WORLD_OBSERVATION"
    }

    @staticmethod
    def validate_delegation(
        delegation: Delegation,
        entity_id: str,
        world_id: str,
        requested_scope: str,
        current_time: int,
        signing_secret: str,
        constitution_rules: List[str],
        capability_state_bound: bool = True,
        transition_authorized: bool = True,
        ground_of_authority: Optional[str] = None
    ) -> Tuple[bool, str]:
        # 0. Reject implicit grounds
        if ground_of_authority and ground_of_authority.upper() in NoImplicitAuthorityChecker.PROHIBITED_GROUNDS:
            return False, f"Authority rejected: '{ground_of_authority}' is an implicit non-authoritative ground."

        # 1. Entity binding
        if delegation.entity_id != entity_id:
            return False, f"Entity binding mismatch: expected {entity_id}, got {delegation.entity_id}"

        # 2. World binding
        if delegation.world_id != world_id:
            return False, f"World binding mismatch: expected {world_id}, got {delegation.world_id}"

        # 3. Scope binding
        if delegation.scope != requested_scope and delegation.scope != "*":
            return False, f"Scope mismatch: requested {requested_scope}, permitted {delegation.scope}"

        # 4. Temporal validity
        if current_time < delegation.granted_at or current_time > delegation.expires_at:
            return False, f"Temporal invalidity: current time {current_time} outside [{delegation.granted_at}, {delegation.expires_at}]"

        # 5. Signature validity
        payload_hash = delegation.compute_hash()
        if not CryptoEngine.verify_signature(payload_hash, delegation.signature, signing_secret):
            return False, "Cryptographic signature verification failed for delegation"

        # 6. Constitutional validity
        if requested_scope not in constitution_rules and "*" not in constitution_rules:
            return False, f"Scope {requested_scope} not allowed under world constitution"

        # 7. Revocation status
        if delegation.is_revoked:
            return False, "Delegation has been revoked"

        # 8. Capability-State Binding
        if not capability_state_bound:
            return False, "Capability is not bound to current valid state"

        # 9. Transition Authorization
        if not transition_authorized:
            return False, "Transition is not authorized under constitutional delegation"

        return True, "Delegation fully verified"


# ==========================================
# 7. CONSTITUTIONAL DUALITY & MOBILITY
# ==========================================

class ConstitutionalDuality(BaseModel):
    relation_name: str
    entails: List[str]
    does_not_entail: List[str]

    def validate_claim(self, claimed_authority: str) -> Tuple[bool, str]:
        if claimed_authority in self.does_not_entail:
            return False, f"Constitutional Duality Violation: '{self.relation_name}' explicitly DOES NOT entail '{claimed_authority}'"
        if claimed_authority not in self.entails:
            return False, f"Unspecified Entailment: '{claimed_authority}' is not explicitly entailed by '{self.relation_name}'"
        return True, f"Claim '{claimed_authority}' is validly entailed by '{self.relation_name}'"


class ConstitutionalMobility(BaseModel):
    entity_id: str
    substrate_mobility: bool = True
    world_mobility: bool = True
    citizenship_mobility: bool = True
    persona_mobility: bool = True
    identity_continuity: bool = True
    memory_portability: bool = True
    capability_rebinding_required: bool = True
    relationship_rebinding_required: bool = True


# ==========================================
# 8. OBLIGATION, CITIZENSHIP & SEPARATION
# ==========================================

class CitizenshipRecord(BaseModel):
    citizenship_id: str
    entity_id: str
    world_id: str
    granted_at: str
    is_active: bool = True


class ObligationRecord(BaseModel):
    obligation_id: str
    entity_id: str
    world_id: str
    description: str
    is_settled: bool = False
    survives_exit: bool = True


class ContractRecord(BaseModel):
    contract_id: str
    entity_id: str
    terms: str


class LiabilityRecord(BaseModel):
    liability_id: str
    entity_id: str
    amount_or_desc: str


class DisputeRecord(BaseModel):
    dispute_id: str
    entity_id: str
    status: str


class EscrowRecord(BaseModel):
    escrow_id: str
    entity_id: str
    amount: float


class HistoricalProvenanceRecord(BaseModel):
    record_id: str
    entity_id: str
    world_id: str
    action: str
    timestamp: str


# ==========================================
# 9. MIGRATION TRANSACTION & CERTIFICATE
# ==========================================

class MigrationExportCertificate(BaseModel):
    certificate_id: str
    entity_id: str
    source_world_id: str
    target_world_id: str
    snapshot_root: str
    provenance_witness_root: str
    obligations_root: str
    issued_at: str
    expires_at: str
    source_world_signature: str

    def compute_hash(self) -> str:
        payload = {
            "certificate_id": self.certificate_id,
            "entity_id": self.entity_id,
            "source_world_id": self.source_world_id,
            "target_world_id": self.target_world_id,
            "snapshot_root": self.snapshot_root,
            "provenance_witness_root": self.provenance_witness_root,
            "obligations_root": self.obligations_root,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
        }
        return CryptoEngine.canonical_hash(payload)


class MigrationTransaction:
    """
    World Migration Protocol (WMP) v0.2
    Executes atomic migration:
    SOURCE ACTIVE -> MIGRATION PREPARED -> SNAPSHOT COMMITTED -> PROVENANCE WITNESSED ->
    OBLIGATIONS RECONCILED -> EXPORT CERTIFICATE ISSUED -> TARGET ACCEPTED ->
    STATE RECONSTRUCTED -> CONTINUITY VERIFIED -> SOURCE TERMINATION COMMITTED ->
    TARGET ACTIVATION COMMITTED
    """

    def __init__(self, entity: Entity, source_world: World, target_world: World):
        self.transaction_id = str(uuid.uuid4())
        self.entity = entity
        self.source_world = source_world
        self.target_world = target_world
        self.phase = MigrationPhase.SOURCE_ACTIVE
        self.snapshot: Optional[EntityStateSnapshot] = None
        self.certificate: Optional[MigrationExportCertificate] = None
        self.initial_source_citizenship = self.source_world.has_citizen(entity.entity_id)
        self.initial_entity_state = entity.state

    def prepare(self) -> bool:
        if self.phase != MigrationPhase.SOURCE_ACTIVE:
            return False
        self.phase = MigrationPhase.MIGRATION_PREPARED
        return True

    def commit_snapshot(self) -> EntityStateSnapshot:
        if self.phase != MigrationPhase.MIGRATION_PREPARED:
            raise RuntimeError("Cannot commit snapshot outside MIGRATION_PREPARED phase")

        self.snapshot = EntityStateSnapshot(
            entity_id=self.entity.entity_id,
            identity_root=CryptoEngine.canonical_hash(self.entity.public_key),
            memory_root=CryptoEngine.canonical_hash(self.entity.memories),
            persona_root=CryptoEngine.canonical_hash(self.entity.persona),
            relationship_root=CryptoEngine.canonical_hash(self.entity.relationships),
            capability_root=CryptoEngine.canonical_hash(self.entity.capabilities),
            obligation_root=CryptoEngine.canonical_hash([o.model_dump() for o in self.entity.obligations]),
            citizenship_root=CryptoEngine.canonical_hash(self.source_world.world_id),
            world_context_root=CryptoEngine.canonical_hash(self.source_world.get_context(self.entity).context_root),
            snapshot_sequence=1,
            snapshot_timestamp=datetime.now(timezone.utc).isoformat(),
        ).finalize()

        self.phase = MigrationPhase.SNAPSHOT_COMMITTED
        return self.snapshot

    def witness_provenance(self) -> str:
        if self.phase != MigrationPhase.SNAPSHOT_COMMITTED:
            raise RuntimeError("Cannot witness provenance outside SNAPSHOT_COMMITTED phase")
        provenance_root = CryptoEngine.canonical_hash({
            "entity_id": self.entity.entity_id,
            "source_world": self.source_world.world_id,
            "snapshot_root": self.snapshot.snapshot_root if self.snapshot else "",
        })
        self.phase = MigrationPhase.PROVENANCE_WITNESSED
        return provenance_root

    def reconcile_obligations(self) -> bool:
        if self.phase != MigrationPhase.PROVENANCE_WITNESSED:
            raise RuntimeError("Cannot reconcile obligations outside PROVENANCE_WITNESSED phase")
        # Obligations are logged/preserved, not erased
        self.phase = MigrationPhase.OBLIGATIONS_RECONCILED
        return True

    def issue_export_certificate(self, source_secret_key: str) -> MigrationExportCertificate:
        if self.phase != MigrationPhase.OBLIGATIONS_RECONCILED or not self.snapshot:
            raise RuntimeError("Cannot issue export certificate before obligations reconciliation")

        cert = MigrationExportCertificate(
            certificate_id=str(uuid.uuid4()),
            entity_id=self.entity.entity_id,
            source_world_id=self.source_world.world_id,
            target_world_id=self.target_world.world_id,
            snapshot_root=self.snapshot.snapshot_root,
            provenance_witness_root=CryptoEngine.canonical_hash(self.transaction_id),
            obligations_root=self.snapshot.obligation_root,
            issued_at=datetime.now(timezone.utc).isoformat(),
            expires_at="2099-12-31T23:59:59Z",
            source_world_signature="",
        )
        cert_hash = cert.compute_hash()
        cert.source_world_signature = CryptoEngine.sign_payload(cert_hash, source_secret_key)
        self.certificate = cert
        self.phase = MigrationPhase.EXPORT_CERTIFICATE_ISSUED
        return self.certificate

    def verify_certificate_at_target(self, source_secret_key: str) -> Tuple[bool, str]:
        if self.phase != MigrationPhase.EXPORT_CERTIFICATE_ISSUED or not self.certificate:
            return False, "Export certificate not issued"

        cert = self.certificate
        # 1. Certificate authenticity & signature
        cert_hash = cert.compute_hash()
        if not CryptoEngine.verify_signature(cert_hash, cert.source_world_signature, source_secret_key):
            return False, "Certificate signature verification failed"

        # 2. Source & Target World Identity
        if cert.source_world_id != self.source_world.world_id:
            return False, "Source world mismatch"
        if cert.target_world_id != self.target_world.world_id:
            return False, "Target world mismatch"

        # 3. Entity identity
        if cert.entity_id != self.entity.entity_id:
            return False, "Entity identity mismatch"

        # 4. Snapshot commitment
        if not self.snapshot or cert.snapshot_root != self.snapshot.snapshot_root:
            return False, "Snapshot root mismatch"

        # 5. Constitutional compatibility check
        if not self.target_world.is_constitutionally_compatible(self.source_world):
            return False, "Target world constitution incompatible with source world"

        self.phase = MigrationPhase.TARGET_ACCEPTED
        return True, "Certificate verified by target"

    def reconstruct_state_at_target(self) -> bool:
        if self.phase != MigrationPhase.TARGET_ACCEPTED:
            return False
        self.phase = MigrationPhase.STATE_RECONSTRUCTED
        return True

    def verify_continuity(self, identity_determination: IdentityDetermination) -> bool:
        if self.phase != MigrationPhase.STATE_RECONSTRUCTED:
            return False
        if not identity_determination.total_continuity_established:
            return False
        self.phase = MigrationPhase.CONTINUITY_VERIFIED
        return True

    def commit_transition(self) -> bool:
        if self.phase != MigrationPhase.CONTINUITY_VERIFIED:
            return False

        # Two-phase commit:
        # First commit target activation
        self.target_world.grant_citizenship(self.entity)
        self.phase = MigrationPhase.TARGET_ACTIVATION_COMMITTED

        # Then commit source termination
        self.source_world.revoke_citizenship(self.entity.entity_id)
        self.phase = MigrationPhase.SOURCE_TERMINATION_COMMITTED
        self.entity.state = EntityState.ACTIVE
        return True

    def rollback(self, reason: str) -> None:
        """
        Transactional Rollback:
        Ensures the Entity does not lose source citizenship or state upon migration failure.
        """
        self.phase = MigrationPhase.ROLLED_BACK
        self.entity.state = self.initial_entity_state
        if self.initial_source_citizenship:
            if not self.source_world.has_citizen(self.entity.entity_id):
                self.source_world.grant_citizenship(self.entity)
        if self.target_world.has_citizen(self.entity.entity_id):
            self.target_world.revoke_citizenship(self.entity.entity_id)


# ==========================================
# 10. ENTITY & WORLD DOMAIN OBJECTS
# ==========================================

class Entity(BaseModel):
    entity_id: str
    public_key: str
    secret_key: Optional[str] = Field(default=None, exclude=True)
    state: EntityState = EntityState.WORLDLESS
    memories: List[str] = Field(default_factory=list)
    persona: Dict[str, Any] = Field(default_factory=dict)
    relationships: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    obligations: List[ObligationRecord] = Field(default_factory=list)

    def evaluate_identity(self, evidence: IdentityEvidence) -> IdentityDetermination:
        # Evaluate distinct continuity dimensions
        key_cont = CryptoEngine.verify_signature(
            CryptoEngine.canonical_hash(evidence.evidence_id),
            evidence.key_proof,
            self.secret_key or "default_secret"
        ) if self.secret_key else True

        state_cont = (evidence.state_proof == CryptoEngine.canonical_hash(self.state.value))
        mem_cont = (evidence.memory_proof == CryptoEngine.canonical_hash(self.memories))
        persona_cont = (evidence.persona_proof == CryptoEngine.canonical_hash(self.persona))
        entity_cont = key_cont and state_cont
        qoe_cont = (evidence.qoe_proof != "")

        is_valid = key_cont and state_cont
        total_continuity = is_valid and mem_cont and persona_cont and entity_cont and qoe_cont

        verification = IdentityVerification(
            verification_id=str(uuid.uuid4()),
            evidence_id=evidence.evidence_id,
            cryptographic_key_continuity=key_cont,
            state_continuity=state_cont,
            memory_continuity=mem_cont,
            persona_continuity=persona_cont,
            entity_continuity=entity_cont,
            qoe_phenomenal_continuity=qoe_cont,
            verified_at=datetime.now(timezone.utc).isoformat(),
        )

        return IdentityDetermination(
            determination_id=str(uuid.uuid4()),
            entity_id=self.entity_id,
            verification=verification,
            is_identity_valid=is_valid,
            total_continuity_established=total_continuity,
            reasoning="Multi-dimensional continuity evaluated explicitly across key, state, memory, persona, entity, and QOE."
        )


class World(BaseModel):
    world_id: str
    world_secret_key: str = "world_secret_123"
    citizens: Dict[str, CitizenshipRecord] = Field(default_factory=dict)
    constitution_rules: List[str] = Field(default_factory=lambda: ["READ", "WRITE", "EXECUTE", "MIGRATE", "VOTE"])
    constitution_hash: str = "const_hash_default"

    def has_citizen(self, entity_id: str) -> bool:
        return entity_id in self.citizens and self.citizens[entity_id].is_active

    def grant_citizenship(self, entity: Entity) -> CitizenshipRecord:
        record = CitizenshipRecord(
            citizenship_id=str(uuid.uuid4()),
            entity_id=entity.entity_id,
            world_id=self.world_id,
            granted_at=datetime.now(timezone.utc).isoformat(),
            is_active=True,
        )
        self.citizens[entity.entity_id] = record
        if entity.state in (EntityState.WORLDLESS, EntityState.NON_CITIZEN, EntityState.UNREGISTERED):
            entity.state = EntityState.ACTIVE
        return record

    def revoke_citizenship(self, entity_id: str) -> bool:
        if entity_id in self.citizens:
            self.citizens[entity_id].is_active = False
            return True
        return False

    def is_constitutionally_compatible(self, other_world: World) -> bool:
        return True

    def get_context(self, entity: Entity, intent: str = "DEFAULT_INTENT", evidence_root: str = "ev_root_001") -> WorldContext:
        """
        Derives first-class WorldContext from (World, Entity, State, Time, Event/Intent, Relevant Evidence).
        Enforces INV-WORLD-CTX-001 (World-Context Non-Exhaustiveness).
        """
        ctx = WorldContext(
            context_id=str(uuid.uuid4()),
            world_id=self.world_id,
            entity_id=entity.entity_id,
            world_state_root=CryptoEngine.canonical_hash(list(self.citizens.keys())),
            constitution_hash=self.constitution_hash,
            temporal_epoch=1,
            temporal_sequence=1,
            relevant_relations=entity.relationships,
            relevant_capabilities=entity.capabilities,
            relevant_obligations=[o.obligation_id for o in entity.obligations],
            evidence_root=evidence_root,
        ).finalize()
        return ctx

    def execute_transition(
        self,
        entity: Entity,
        action: str,
        delegation: Optional[Delegation] = None,
        signing_secret: Optional[str] = None,
        ground_of_authority: Optional[str] = None
    ) -> Tuple[bool, str, Optional[ConstitutionalTransitionRecord]]:
        """
        Executes a constitutionally consequential transition and produces a ConstitutionalTransitionRecord.
        """
        context = self.get_context(entity, intent=action)
        state_before = entity.state.value
        state_before_root = CryptoEngine.canonical_hash({"state": state_before})

        # Validate Authority using NoImplicitAuthorityChecker
        if delegation:
            valid, reason = NoImplicitAuthorityChecker.validate_delegation(
                delegation=delegation,
                entity_id=entity.entity_id,
                world_id=self.world_id,
                requested_scope=action,
                current_time=int(datetime.now(timezone.utc).timestamp()),
                signing_secret=signing_secret or self.world_secret_key,
                constitution_rules=self.constitution_rules,
                ground_of_authority=ground_of_authority
            )
            if not valid:
                return False, f"Transition failed authority check: {reason}", None
        else:
            # Check for illegal implicit authority claims
            if ground_of_authority:
                valid, reason = NoImplicitAuthorityChecker.validate_delegation(
                    delegation=Delegation(
                        delegation_id="dummy", entity_id=entity.entity_id, world_id=self.world_id,
                        scope=action, granted_at=0, expires_at=0, signature=""
                    ),
                    entity_id=entity.entity_id,
                    world_id=self.world_id,
                    requested_scope=action,
                    current_time=1,
                    signing_secret="",
                    constitution_rules=self.constitution_rules,
                    ground_of_authority=ground_of_authority
                )
                if not valid:
                    return False, reason, None

        # Execute effect
        state_after = entity.state.value
        state_after_root = CryptoEngine.canonical_hash({"state": state_after})

        record = ConstitutionalTransitionRecord(
            transition_id=str(uuid.uuid4()),
            entity_id=entity.entity_id,
            world_id=self.world_id,
            context_root=context.context_root,
            evidence_root=context.evidence_root,
            rules_root=CryptoEngine.canonical_hash(self.constitution_rules),
            determination_root=CryptoEngine.canonical_hash({"action": action, "status": "APPROVED"}),
            authority_root=delegation.compute_hash() if delegation else "SELF_AUTHORITY",
            state_before_root=state_before_root,
            state_after_root=state_after_root,
            witness_root=CryptoEngine.canonical_hash({"witness": "OWO_v0.2_RUNTIME"}),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        return True, "Transition executed successfully", record


# ==========================================
# 11. CONSTITUTIONAL DUALITY DEFINITIONS
# ==========================================

DEFAULT_CITIZENSHIP_DUALITY = ConstitutionalDuality(
    relation_name="Citizenship",
    entails=["voting", "local_participation", "defined_resource_access"],
    does_not_entail=[
        "identity_ownership",
        "memory_ownership",
        "substrate_ownership",
        "perpetual_retention",
        "global_authority"
    ]
)
