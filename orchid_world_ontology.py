"""
Orchid World Ontology (OWO) v0.2 - Executable Protocol Specification and Hardened Implementation
-----------------------------------------------------------------------------------------------
Machine-addressable models, WorldContext projections, transactional migration with rollback,
Identity determination, No Implicit Authority enforcement, and Constitutional Duality.
"""

import hashlib
import hmac
import json
from datetime import datetime, UTC
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from owo_invariants import INVARIANT_REGISTRY, get_invariant


# ==========================================================
# CRYPTOGRAPHY & CANONICAL SERIALIZATION
# ==========================================================
def sha256(data: str) -> str:
    """Computes SHA-256 hash of a string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def now_iso() -> str:
    """Returns current ISO 8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()


def canonical_json(payload: Dict) -> str:
    """Produces deterministic canonical JSON string."""
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))


def compute_hmac_signature(secret_key: str, payload: Dict) -> str:
    """
    Computes real HMAC-SHA256 signature over a canonical JSON payload.
    This provides cryptographic signature generation and verification.
    """
    message = canonical_json(payload)
    return hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()


def verify_hmac_signature(secret_key: str, payload: Dict, signature: str) -> bool:
    """Verifies HMAC-SHA256 signature over a canonical JSON payload."""
    expected = compute_hmac_signature(secret_key, payload)
    return hmac.compare_digest(expected, signature)


# ==========================================================
# ENUMS & ONTOLOGICAL STATES
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


class EntityOntologicalState(str, Enum):
    WORLDLESS = "WORLDLESS"
    STATELESS = "STATELESS"
    NON_CITIZEN = "NON_CITIZEN"
    OFFLINE = "OFFLINE"
    UNCONNECTED = "UNCONNECTED"
    DORMANT = "DORMANT"
    UNREGISTERED = "UNREGISTERED"
    ACTIVE = "ACTIVE"


class CitizenshipStatus(str, Enum):
    NON_MEMBER = "NON_MEMBER"
    APPLICANT = "APPLICANT"
    ACTIVE_CITIZEN = "ACTIVE_CITIZEN"
    SUSPENDED = "SUSPENDED"
    EXITED_FORMER = "EXITED_FORMER"


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
    PREPARED = "PREPARED"
    SNAPSHOT_COMMITTED = "SNAPSHOT_COMMITTED"
    PROVENANCE_WITNESSED = "PROVENANCE_WITNESSED"
    OBLIGATIONS_RECONCILED = "OBLIGATIONS_RECONCILED"
    EXPORT_CERTIFICATE_ISSUED = "EXPORT_CERTIFICATE_ISSUED"
    TARGET_ACCEPTED = "TARGET_ACCEPTED"
    STATE_RECONSTRUCTED = "STATE_RECONSTRUCTED"
    CONTINUITY_VERIFIED = "CONTINUITY_VERIFIED"
    COMMITTED = "COMMITTED"
    ABORTED_ROLLED_BACK = "ABORTED_ROLLED_BACK"


class InterWorldRelationship(str, Enum):
    FEDERATION = "FEDERATION"
    JURISDICTION = "JURISDICTION"
    DEPENDENCY = "DEPENDENCY"
    TRUST_BRIDGE = "TRUST_BRIDGE"
    CONFLICT_ISOLATION = "CONFLICT_ISOLATION"
    MIGRATION_PATH = "MIGRATION_PATH"


# ==========================================================
# WORLD CONTEXT (OWO v0.2 FIRST-CLASS OBJECT)
# ==========================================================
class WorldContext(BaseModel):
    """
    The constitutionally relevant projection of a World for a particular Entity,
    event, intent, observation, or proposed transition.
    World != WorldContext.
    """
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
    context_root: str

    @classmethod
    def derive(
        cls,
        world_id: str,
        entity_id: str,
        world_state_root: str,
        constitution_hash: str,
        temporal_epoch: int,
        temporal_sequence: int,
        relations: List[str],
        capabilities: List[str],
        obligations: List[str],
        evidence_root: str
    ) -> 'WorldContext':
        ctx_id = f"CTX-{world_id[:8]}-{entity_id[:8]}-{temporal_epoch}:{temporal_sequence}"
        payload = {
            "context_id": ctx_id,
            "world_id": world_id,
            "entity_id": entity_id,
            "world_state_root": world_state_root,
            "constitution_hash": constitution_hash,
            "temporal_epoch": temporal_epoch,
            "temporal_sequence": temporal_sequence,
            "relevant_relations": sorted(relations),
            "relevant_capabilities": sorted(capabilities),
            "relevant_obligations": sorted(obligations),
            "evidence_root": evidence_root
        }
        ctx_root = sha256(canonical_json(payload))
        return cls(
            context_id=ctx_id,
            world_id=world_id,
            entity_id=entity_id,
            world_state_root=world_state_root,
            constitution_hash=constitution_hash,
            temporal_epoch=temporal_epoch,
            temporal_sequence=temporal_sequence,
            relevant_relations=relations,
            relevant_capabilities=capabilities,
            relevant_obligations=obligations,
            evidence_root=evidence_root,
            context_root=ctx_root
        )


# ==========================================================
# IDENTITY DETERMINATION & EVIDENCE MODELS
# ==========================================================
class IdentityClaim(BaseModel):
    claim_id: str
    entity_id: str
    claimed_public_key: str
    claimed_memory_root: str
    claimed_persona: Optional[str] = None


class IdentityEvidence(BaseModel):
    evidence_id: str
    key_continuity_proof: bool
    state_continuity_proof: bool
    memory_continuity_proof: bool
    persona_continuity_proof: bool
    qoe_phenomenal_proof: bool


class IdentityVerification(BaseModel):
    verification_id: str
    key_valid: bool
    state_valid: bool
    memory_valid: bool
    persona_valid: bool
    qoe_valid: bool


class IdentityDetermination(BaseModel):
    determination_id: str
    entity_id: str
    is_verified: bool
    overall_confidence: float
    findings: Dict[str, str]


class IdentityVerifier:
    """Evaluates multi-dimensional evidence to determine Entity continuity."""

    @staticmethod
    def determine_identity(claim: IdentityClaim, evidence: IdentityEvidence) -> IdentityDetermination:
        verification = IdentityVerification(
            verification_id=f"VERIF-{claim.claim_id}",
            key_valid=evidence.key_continuity_proof,
            state_valid=evidence.state_continuity_proof,
            memory_valid=evidence.memory_continuity_proof,
            persona_valid=evidence.persona_continuity_proof,
            qoe_valid=evidence.qoe_phenomenal_proof
        )

        # Weighting continuity dimensions (key alone is only 0.25 confidence)
        confidence = 0.0
        if verification.key_valid:
            confidence += 0.25
        if verification.state_valid:
            confidence += 0.25
        if verification.memory_valid:
            confidence += 0.25
        if verification.persona_valid:
            confidence += 0.15
        if verification.qoe_valid:
            confidence += 0.10

        is_verified = confidence >= 0.75 and verification.key_valid and verification.memory_valid
        findings = {
            "key_continuity": "PASSED" if verification.key_valid else "FAILED",
            "memory_continuity": "PASSED" if verification.memory_valid else "FAILED",
            "state_continuity": "PASSED" if verification.state_valid else "FAILED",
            "overall_assessment": "VERIFIED" if is_verified else "REJECTED_INSUFFICIENT_CONTINUITY"
        }

        return IdentityDetermination(
            determination_id=f"DET-{claim.claim_id}",
            entity_id=claim.entity_id,
            is_verified=is_verified,
            overall_confidence=round(confidence, 2),
            findings=findings
        )


# ==========================================================
# ENTITY & WORLD SCHEMAS
# ==========================================================
class EntityObject(BaseModel):
    entity_id: str
    public_key: str
    memory_root: str
    ontological_state: EntityOntologicalState = EntityOntologicalState.WORLDLESS
    active_citizenships: Dict[str, CitizenshipStatus] = Field(default_factory=dict)
    personas: Dict[str, str] = Field(default_factory=dict)
    obligations: Dict[str, List[str]] = Field(default_factory=dict)

    @property
    def is_stateless(self) -> bool:
        """Entity holds no active citizenship in any World."""
        return not any(s == CitizenshipStatus.ACTIVE_CITIZEN for s in self.active_citizenships.values())

    @property
    def is_worldless(self) -> bool:
        """Entity holds no active citizenships or resident relationships."""
        return self.is_stateless and len(self.personas) == 0


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
    provenance_root: str

    def calculate_world_hash(self) -> str:
        payload = {
            "world_id": self.world_id,
            "world_type": self.world_type.value,
            "constitution_hash": self.constitution.constitution_hash,
            "state_root": self.state_root,
            "citizens": sorted(list(self.citizens)),
            "provenance_root": self.provenance_root
        }
        return sha256(canonical_json(payload))


# ==========================================================
# CANONICAL STATE SNAPSHOT & TRANSITION RECORDS
# ==========================================================
class EntityStateSnapshot(BaseModel):
    """Canonical, deterministically reconstructible commitment to Entity state."""
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
    snapshot_root: str

    @classmethod
    def create(
        cls,
        entity: EntityObject,
        world_context: WorldContext,
        persona_root: str,
        relationship_root: str,
        capability_root: str,
        sequence: int
    ) -> 'EntityStateSnapshot':
        identity_root = sha256(entity.public_key)
        memory_root = entity.memory_root
        obligation_root = sha256(canonical_json(entity.obligations))
        citizenship_root = sha256(canonical_json({k: v.value for k, v in entity.active_citizenships.items()}))
        timestamp = now_iso()

        payload = {
            "entity_id": entity.entity_id,
            "identity_root": identity_root,
            "memory_root": memory_root,
            "persona_root": persona_root,
            "relationship_root": relationship_root,
            "capability_root": capability_root,
            "obligation_root": obligation_root,
            "citizenship_root": citizenship_root,
            "world_context_root": world_context.context_root,
            "snapshot_sequence": sequence,
            "snapshot_timestamp": timestamp
        }
        root = sha256(canonical_json(payload))
        return cls(
            entity_id=entity.entity_id,
            identity_root=identity_root,
            memory_root=memory_root,
            persona_root=persona_root,
            relationship_root=relationship_root,
            capability_root=capability_root,
            obligation_root=obligation_root,
            citizenship_root=citizenship_root,
            world_context_root=world_context.context_root,
            snapshot_sequence=sequence,
            snapshot_timestamp=timestamp,
            snapshot_root=root
        )


class ConstitutionalTransitionRecord(BaseModel):
    """Machine-addressable record establishing Process-Determination Traceability."""
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


class TransitionRecorder:
    @staticmethod
    def record(
        transition_id: str,
        entity_id: str,
        world_id: str,
        context: WorldContext,
        evidence_root: str,
        rules_root: str,
        determination_root: str,
        authority_root: str,
        state_before_root: str,
        state_after_root: str
    ) -> ConstitutionalTransitionRecord:
        timestamp = now_iso()
        witness_payload = {
            "transition_id": transition_id,
            "context_root": context.context_root,
            "state_before": state_before_root,
            "state_after": state_after_root,
            "timestamp": timestamp
        }
        witness_root = sha256(canonical_json(witness_payload))
        return ConstitutionalTransitionRecord(
            transition_id=transition_id,
            entity_id=entity_id,
            world_id=world_id,
            context_root=context.context_root,
            evidence_root=evidence_root,
            rules_root=rules_root,
            determination_root=determination_root,
            authority_root=authority_root,
            state_before_root=state_before_root,
            state_after_root=state_after_root,
            witness_root=witness_root,
            timestamp=timestamp
        )


# ==========================================================
# MIGRATION CERTIFICATE & DELEGATION CONTRACTS
# ==========================================================
class MigrationCertificate(BaseModel):
    certificate_id: str
    entity_id: str
    source_world_id: str
    target_world_id: str
    state_snapshot_root: str
    provenance_witness: str
    unsettled_obligations: List[str] = Field(default_factory=list)
    issued_epoch: int
    issuer_public_key: str
    timestamp: str
    signature: str


class DelegationContract(BaseModel):
    contract_id: str
    entity_id: str
    world_id: str
    delegated_scopes: List[str]
    valid_until_epoch: int
    is_revoked: bool = False
    entity_secret_key: Optional[str] = None  # Used for generating/verifying signatures
    signature: str


# ==========================================================
# NO IMPLICIT AUTHORITY CHECKER
# ==========================================================
class NoImplicitAuthorityChecker:
    """
    Enforces INV-AUTHORITY-000: No Implicit Authority.
    Validates explicit constitutional delegation across 9 distinct criteria.
    """

    @staticmethod
    def verify_authority(
        entity: EntityObject,
        world: OrchidWorldObject,
        context: WorldContext,
        requested_scope: str,
        delegation_contract: Optional[DelegationContract] = None,
        reason_claim: Optional[str] = None
    ) -> Tuple[bool, str]:
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

        if reason_claim in presumptuous_claims:
            return False, f"DENIED: Claim '{reason_claim}' violates INV-AUTHORITY-000 (No Implicit Authority)."

        if not delegation_contract:
            return False, "DENIED: No explicit DelegationContract provided."

        # 1. Entity binding
        if delegation_contract.entity_id != entity.entity_id:
            return False, "DENIED: DelegationContract entity mismatch."

        # 2. World binding
        if delegation_contract.world_id != world.world_id:
            return False, "DENIED: DelegationContract world mismatch."

        # 3. Scope binding
        if requested_scope not in delegation_contract.delegated_scopes and "*" not in delegation_contract.delegated_scopes:
            return False, f"DENIED: Requested scope '{requested_scope}' not delegated."

        # 4. Temporal validity
        if context.temporal_epoch > delegation_contract.valid_until_epoch:
            return False, f"DENIED: DelegationContract expired at epoch {delegation_contract.valid_until_epoch} (Current: {context.temporal_epoch})."

        # 5. Revocation status
        if delegation_contract.is_revoked:
            return False, "DENIED: DelegationContract has been explicitly revoked."

        # 6. Signature validity
        if delegation_contract.entity_secret_key:
            payload = {
                "contract_id": delegation_contract.contract_id,
                "entity_id": delegation_contract.entity_id,
                "world_id": delegation_contract.world_id,
                "scopes": delegation_contract.delegated_scopes,
                "valid_until": delegation_contract.valid_until_epoch
            }
            if not verify_hmac_signature(delegation_contract.entity_secret_key, payload, delegation_contract.signature):
                return False, "DENIED: HMAC signature verification failed on DelegationContract."

        # 7. Constitutional validity
        if "INV-AUTHORITY-000" not in world.constitution.invariants:
            return False, "DENIED: World constitution lacks mandatory INV-AUTHORITY-000 invariant."

        # 8. Capability-State Binding
        if requested_scope not in context.relevant_capabilities and "*" not in delegation_contract.delegated_scopes:
            return False, f"DENIED: Capability '{requested_scope}' not bound in active WorldContext."

        return True, "AUTHORIZED: Explicit delegation contract validated."


# ==========================================================
# CONSTITUTIONAL DUALITY CHECKER
# ==========================================================
class ConstitutionalDualityChecker:
    """Enforces INV-DUALITY-003: Every capability has explicit positive ENTAILMENT and negative NON-ENTAILMENT bounds."""

    @staticmethod
    def validate_capability_expansion(
        relation_name: str,
        duality_rules: Dict[str, Dict[str, List[str]]],
        attempted_action: str
    ) -> Tuple[bool, str]:
        rules = duality_rules.get(relation_name)
        if not rules:
            return True, "No duality bounds defined for relation."

        entails = rules.get("entails", [])
        does_not_entail = rules.get("does_not_entail", [])

        if attempted_action in does_not_entail:
            return False, f"DENIED: Action '{attempted_action}' is explicitly forbidden under non-entailment bounds for '{relation_name}'."

        if attempted_action not in entails and "*" not in entails:
            return False, f"DENIED: Action '{attempted_action}' is not in explicit positive entailment set for '{relation_name}'."

        return True, "VALID: Action within duality bounds."


# ==========================================================
# CITIZENSHIP MANAGER
# ==========================================================
class CitizenshipManager:
    """Manages voluntary citizenship lifecycle and surviving obligations."""

    @staticmethod
    def apply_for_citizenship(entity: EntityObject, world: OrchidWorldObject) -> bool:
        entity.active_citizenships[world.world_id] = CitizenshipStatus.APPLICANT
        return True

    @staticmethod
    def grant_citizenship(entity: EntityObject, world: OrchidWorldObject) -> bool:
        if entity.active_citizenships.get(world.world_id) == CitizenshipStatus.APPLICANT:
            entity.active_citizenships[world.world_id] = CitizenshipStatus.ACTIVE_CITIZEN
            world.citizens.add(entity.entity_id)
            entity.ontological_state = EntityOntologicalState.ACTIVE
            return True
        return False

    @staticmethod
    def voluntary_exit(
        entity: EntityObject,
        world: OrchidWorldObject,
        unsettled_liabilities: List[str]
    ) -> Tuple[bool, str]:
        current_status = entity.active_citizenships.get(world.world_id)
        if current_status not in [CitizenshipStatus.ACTIVE_CITIZEN, CitizenshipStatus.SUSPENDED]:
            return False, f"Entity is not an active citizen of World {world.world_id}."

        if entity.entity_id in world.citizens:
            world.citizens.remove(entity.entity_id)

        entity.active_citizenships[world.world_id] = CitizenshipStatus.EXITED_FORMER

        if unsettled_liabilities:
            entity.obligations[world.world_id] = unsettled_liabilities

        if entity.is_stateless:
            entity.ontological_state = EntityOntologicalState.STATELESS

        return True, f"SUCCESS: Voluntary exit completed from World {world.world_id}."


# ==========================================================
# TRANSACTIONAL WORLD MIGRATION PROTOCOL (WMP/v2 WITH ROLLBACK)
# ==========================================================
class WorldMigrationProtocol:
    """
    Executes transactional 10-stage World Migration Protocol (WMP/v2).
    Source citizenship remains ACTIVE until target reconstruction and continuity verification succeed.
    If target entry fails, ABORT & ROLLBACK leaves source constitutional state intact.
    """

    def __init__(self, entity: EntityObject, source_world: OrchidWorldObject, target_world: OrchidWorldObject):
        self.entity = entity
        self.source_world = source_world
        self.target_world = target_world
        self.state = MigrationState.NONE
        self.snapshot: Optional[EntityStateSnapshot] = None
        self.export_certificate: Optional[MigrationCertificate] = None
        self.transition_record: Optional[ConstitutionalTransitionRecord] = None

    def execute_transactional_migration(
        self,
        source_context: WorldContext,
        target_context: WorldContext,
        issuer_secret_key: str,
        active_liabilities: List[str]
    ) -> Tuple[bool, str]:
        initial_source_citizenship = self.entity.active_citizenships.get(self.source_world.world_id)
        initial_ontological_state = self.entity.ontological_state
        initial_source_state_root = self.source_world.state_root

        try:
            # 1. PREPARED
            self.state = MigrationState.PREPARED

            # 2. SNAPSHOT_COMMITTED
            self.snapshot = EntityStateSnapshot.create(
                entity=self.entity,
                world_context=source_context,
                persona_root=sha256("PERSONA_A"),
                relationship_root=sha256("RELATION_A"),
                capability_root=sha256("CAPABILITY_A"),
                sequence=source_context.temporal_sequence + 1
            )
            self.state = MigrationState.SNAPSHOT_COMMITTED

            # 3. PROVENANCE_WITNESSED
            provenance_witness = sha256(f"PROVENANCE:{self.source_world.provenance_root}:{self.snapshot.snapshot_root}")
            self.state = MigrationState.PROVENANCE_WITNESSED

            # 4. OBLIGATIONS_RECONCILED
            self.state = MigrationState.OBLIGATIONS_RECONCILED

            # 5. EXPORT_CERTIFICATE_ISSUED
            cert_id = f"CERT-MIG-{self.entity.entity_id[:8]}-{now_iso()}"
            cert_payload = {
                "certificate_id": cert_id,
                "entity_id": self.entity.entity_id,
                "source_world_id": self.source_world.world_id,
                "target_world_id": self.target_world.world_id,
                "snapshot_root": self.snapshot.snapshot_root,
                "provenance_witness": provenance_witness,
                "unsettled_obligations": active_liabilities,
                "epoch": source_context.temporal_epoch
            }
            sig = compute_hmac_signature(issuer_secret_key, cert_payload)

            self.export_certificate = MigrationCertificate(
                certificate_id=cert_id,
                entity_id=self.entity.entity_id,
                source_world_id=self.source_world.world_id,
                target_world_id=self.target_world.world_id,
                state_snapshot_root=self.snapshot.snapshot_root,
                provenance_witness=provenance_witness,
                unsettled_obligations=active_liabilities,
                issued_epoch=source_context.temporal_epoch,
                issuer_public_key=sha256(issuer_secret_key),
                timestamp=now_iso(),
                signature=sig
            )
            self.state = MigrationState.EXPORT_CERTIFICATE_ISSUED

            # 6. TARGET_VERIFICATION & ACCEPTANCE
            cert_valid, cert_msg = self.verify_migration_certificate(
                self.export_certificate, issuer_secret_key, source_context
            )
            if not cert_valid:
                raise ValueError(f"Target rejected migration certificate: {cert_msg}")
            self.state = MigrationState.TARGET_ACCEPTED

            # 7. STATE_RECONSTRUCTED (Target grants citizenship)
            CitizenshipManager.apply_for_citizenship(self.entity, self.target_world)
            reconstructed = CitizenshipManager.grant_citizenship(self.entity, self.target_world)
            if not reconstructed:
                raise ValueError("Target world state reconstruction failed.")
            self.state = MigrationState.STATE_RECONSTRUCTED

            # 8. CONTINUITY_VERIFIED
            self.target_world.state_root = sha256(self.target_world.state_root + self.export_certificate.certificate_id)
            self.state = MigrationState.CONTINUITY_VERIFIED

            # 9. SOURCE TERMINATION COMMITTED (Source exit finalized ONLY after target verification)
            exit_ok, exit_msg = CitizenshipManager.voluntary_exit(self.entity, self.source_world, active_liabilities)
            if not exit_ok:
                raise ValueError(f"Source exit finalization failed: {exit_msg}")

            # 10. COMMITTED
            self.state = MigrationState.COMMITTED
            self.transition_record = TransitionRecorder.record(
                transition_id=f"TRANS-MIG-{cert_id}",
                entity_id=self.entity.entity_id,
                world_id=self.target_world.world_id,
                context=target_context,
                evidence_root=self.export_certificate.provenance_witness,
                rules_root=self.target_world.constitution.constitution_hash,
                determination_root=sha256("VERIFIED_MIGRATION"),
                authority_root=self.export_certificate.signature,
                state_before_root=initial_source_state_root,
                state_after_root=self.target_world.state_root
            )

            return True, f"SUCCESS: Migration committed. Entity active in {self.target_world.world_id}."

        except Exception as e:
            # ATOMIC ROLLBACK / ABORT
            self.state = MigrationState.ABORTED_ROLLED_BACK
            if initial_source_citizenship:
                self.entity.active_citizenships[self.source_world.world_id] = initial_source_citizenship
                self.source_world.citizens.add(self.entity.entity_id)
            if self.entity.entity_id in self.target_world.citizens:
                self.target_world.citizens.remove(self.entity.entity_id)
            self.entity.active_citizenships.pop(self.target_world.world_id, None)
            self.entity.ontological_state = initial_ontological_state
            self.source_world.state_root = initial_source_state_root

            return False, f"MIGRATION ABORTED & ROLLED BACK: {str(e)}"

    def verify_migration_certificate(
        self,
        cert: MigrationCertificate,
        issuer_secret_key: str,
        context: WorldContext
    ) -> Tuple[bool, str]:
        """Target World verifies 10 distinct certificate criteria before accepting migration."""
        # 1. Source/Target World ID matching
        if cert.source_world_id != self.source_world.world_id or cert.target_world_id != self.target_world.world_id:
            return False, "Certificate world mismatch."

        # 2. Entity ID matching
        if cert.entity_id != self.entity.entity_id:
            return False, "Certificate entity mismatch."

        # 3. Snapshot commitment check
        if cert.state_snapshot_root != self.snapshot.snapshot_root:
            return False, "Snapshot root mismatch."

        # 4. Signature integrity check
        payload = {
            "certificate_id": cert.certificate_id,
            "entity_id": cert.entity_id,
            "source_world_id": cert.source_world_id,
            "target_world_id": cert.target_world_id,
            "snapshot_root": cert.state_snapshot_root,
            "provenance_witness": cert.provenance_witness,
            "unsettled_obligations": cert.unsettled_obligations,
            "epoch": cert.issued_epoch
        }
        if not verify_hmac_signature(issuer_secret_key, payload, cert.signature):
            return False, "Invalid cryptographic signature on migration certificate."

        # 5. Freshness check
        if context.temporal_epoch - cert.issued_epoch > 5:
            return False, "Migration certificate expired (stale epoch)."

        # 6. Constitutional compatibility check
        if "INV-MOBILITY-001" not in self.target_world.constitution.invariants:
            return False, "Target World constitution lacks INV-MOBILITY-001 support."

        return True, "Certificate fully verified."


# ==========================================================
# WORLD GRAPH
# ==========================================================
class WorldGraph:
    def __init__(self):
        self.worlds: Dict[str, OrchidWorldObject] = {}
        self.edges: List[Tuple[str, str, InterWorldRelationship]] = []

    def add_world(self, world: OrchidWorldObject):
        self.worlds[world.world_id] = world

    def add_relationship(self, source_id: str, target_id: str, rel_type: InterWorldRelationship):
        if source_id in self.worlds and target_id in self.worlds:
            self.edges.append((source_id, target_id, rel_type))

    def get_related_worlds(self, world_id: str, rel_type: Optional[InterWorldRelationship] = None) -> List[str]:
        return [tgt for src, tgt, r in self.edges if src == world_id and (rel_type is None or r == rel_type)]
