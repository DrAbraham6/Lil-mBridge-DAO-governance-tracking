# Orchid World Ontology (OWO) v0.2 Specification

## Executive Summary & Core Governing Principle

Orchid World Ontology (OWO) v0.2 hardens the executable ontological and constitutional specifications for sovereign entities, worlds, contexts, identity, authority, and mobility within the Orchid ecosystem.

The fundamental governing principle of OWO v0.2 is:

> **The implementation MUST NOT be weaker than the ontology it claims to implement.**

Furthermore:
* **No implicit authority:** No entity, world, substrate, runtime, observer, intermediary, or authority may acquire effective control merely because it happens to occupy a privileged position in the causal or computational stack.
* **WorldContext Non-Exhaustiveness:** A World provides context; it does not become the entirety of the Entity.
* **Citizenship Separation:** Citizenship is a relationship with a World, not the ontological source of an Entity's existence, identity, continuity, memory, or personhood.

---

# 1. Formal Ontological Pipeline

OWO v0.2 formalizes the complete causal and constitutional transition pipeline:

```text
PRECURSORS
(Entity, Identity, Substrate, Memory, Persona, Relationships, Capabilities)
        ↓
WORLD CONTEXT
(World + State + Time + Relations + Rules + Evidence)
        ↓
CONFIGURATION
        ↓
PROPERTIES
        ↓
DETERMINATIONS
        ↓
AUTHORITY
        ↓
EFFECT
```

### Definitions:
1. **World:** The persistent bounded environment.
2. **WorldContext:** The constitutionally relevant projection of that World for a particular Entity, event, intent, observation, or proposed transition. `World != WorldContext`.
3. **WorldContext Derivation:** WorldContext is dynamically reconstructible from:
   $$\text{World} + \text{Entity} + \text{State} + \text{Time} + \text{Event/Intent} + \text{Relevant Evidence}$$

---

# 2. First-Class WorldContext Schema

WorldContext is a machine-addressable Pydantic model:

```python
class WorldContext(BaseModel):
    context_id: str
    world_id: str
    entity_id: str
    world_state_root: str
    constitution_hash: str
    temporal_epoch: int
    temporal_sequence: int
    relevant_relations: List[str]
    relevant_capabilities: List[str]
    relevant_obligations: List[str]
    evidence_root: str
    context_root: str
```

`context_root` is deterministically computed from the canonical hash of all contextual properties.

---

# 3. Corrected Entity State Ontology

Entity existence is decoupled from citizenship. Entity statefulness is categorized into explicitly distinguishable concepts:

* **WORLDLESS:** Possesses identity and memory without association to any World.
* **STATELESS:** Lacks persistent local state binding.
* **NON_CITIZEN:** Interacts with or resides within a World without holding citizenship status.
* **OFFLINE:** Inactive in runtime execution without ceasing to exist.
* **UNCONNECTED:** Lacks active network/inter-entity connectivity.
* **DORMANT:** Suspended operational state.
* **UNREGISTERED:** Present but not registered in World context registries.
* **ACTIVE:** Fully active operating state.

An Entity is explicitly capable of:
* possessing identity without citizenship
* possessing memory without citizenship
* possessing obligations without citizenship
* being offline without ceasing to exist
* being worldless without being identityless
* being non-citizen without being nonexistent

---

# 4. Multi-Dimensional Identity & Continuity

Cryptographic key continuity alone does **NOT** prove total Entity continuity. OWO v0.2 establishes explicit determinations across six continuity dimensions:

1. **Cryptographic Key Continuity:** Verification of active key signatures.
2. **State Continuity:** Verification of consistent state evolution.
3. **Memory Continuity:** Integrity and preservation of episodic/semantic memory roots.
4. **Persona Continuity:** Consistency of behavioral and value profiles.
5. **Entity Continuity:** Unbroken self-same identity assertion over time.
6. **QOE / Phenomenal Continuity:** Verification of qualitative observational/experiential continuity.

### Models:
* `IdentityClaim`
* `IdentityEvidence`
* `IdentityVerification`
* `IdentityDetermination`

---

# 5. Strict No Implicit Authority (`NoImplicitAuthorityChecker`)

No implicit authority may be derived from positional or observational facts. OWO v0.2 explicitly rejects:

$$\begin{aligned}
\text{Observation} &\neq \text{Authority} \\
\text{Hosting} &\neq \text{Authority} \\
\text{Storage} &\neq \text{Authority} \\
\text{Creation} &\neq \text{Authority} \\
\text{Previous Membership} &\neq \text{Authority} \\
\text{Offline Status} &\neq \text{Authority} \\
\text{Substrate Control} &\neq \text{Authority} \\
\text{Relationship} &\neq \text{Authority} \\
\text{World Observation} &\neq \text{Authority}
\end{aligned}$$

Authority requires explicit constitutional delegation checked across 9 strict parameters:
1. Entity binding
2. World binding
3. Scope binding
4. Temporal validity
5. Signature validity
6. Constitutional validity
7. Revocation status
8. Capability-State Binding
9. Transition Authorization

---

# 6. Real Cryptographic Signatures

All cryptographic operations use canonical JSON hashing (SHA-256) and standard cryptographic HMAC-SHA256 signature verification over canonical payload digests. Placeholder hashes are strictly forbidden.

---

# 7. World Migration Protocol (WMP) v0.2 Transactional Semantics

Migration behaves as an atomic two-phase transactional state transition:

```text
SOURCE ACTIVE
      ↓
MIGRATION PREPARED
      ↓
SNAPSHOT COMMITTED
      ↓
PROVENANCE WITNESSED
      ↓
OBLIGATIONS RECONCILED
      ↓
EXPORT CERTIFICATE ISSUED
      ↓
TARGET ACCEPTED
      ↓
STATE RECONSTRUCTED
      ↓
CONTINUITY VERIFIED
      ↓
SOURCE TERMINATION COMMITTED
      ↓
TARGET ACTIVATION COMMITTED
```

If target entry or verification fails at any stage:
$$\text{ROLLBACK / ABORT}$$
is executed, leaving source citizenship and state fully intact. Source termination is committed **only after** target activation succeeds.

---

# 8. Migration Certificate Verification

Target Worlds MUST verify:
1. Certificate authenticity (source world signature)
2. Source World identity
3. Target World identity
4. Entity identity
5. Snapshot commitment (`snapshot_root`)
6. Provenance witness (`provenance_witness_root`)
7. Obligation state (`obligations_root`)
8. Certificate freshness & expiration
9. Certificate integrity
10. Constitutional compatibility

---

# 9. Real Canonical State Snapshots

Snapshots commit to canonical entity states using deterministic Merkle root calculations:

```python
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
    snapshot_root: str
```

---

# 10. Process-Determination Traceability

Every constitutionally consequential transition produces a machine-addressable `ConstitutionalTransitionRecord`:

```python
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
```

---

# 11. Constitutional Duality

For every relation or privilege, both **ENTAILMENT** and **NON-ENTAILMENT** are explicitly modeled.

Example (`Citizenship`):
* **Entails:** voting, local participation, defined resource access.
* **Does NOT Entail:** identity ownership, memory ownership, substrate ownership, perpetual retention, global authority.

---

# 12. Constitutional Mobility

Promotes mobility into first-class ontology:
* Substrate Mobility
* World Mobility
* Citizenship Mobility
* Persona Mobility
* Identity Continuity
* Memory Portability
* Capability Rebinding
* Relationship Rebinding

Leaving a World does NOT imply identity, memory, or persona deletion or historical erasure.

---

# 13. Formal Invariant Registry (`owo_invariants.py`)

* **INV-WORLD-CTX-001 (World-Context Non-Exhaustiveness):** Properties within a WorldContext do not exhaust entity properties outside it.
* **INV-MOBILITY-002 (No Forced Citizenship Retention):** World cannot retain citizenship due to hosting, dependence, or observation.
* **INV-NO-IMP-AUTH-001 (No Implicit Authority):** Implicit grounds yield zero authority.
* **INV-ENTITY-EXISTENCE-001 (Citizenship Separation):** Existence is decoupled from citizenship.
* **INV-IDENTITY-CONTINUITY-001 (Multi-Dimensional Identity):** Key continuity alone is insufficient.
* **INV-MIGRATION-ATOMICITY-001 (Transactional Migration):** Migration failures trigger full state rollbacks.
* **INV-DUALITY-001 (Constitutional Duality):** Entailment bounds are strictly enforced.
* **INV-TRACEABILITY-001 (Process Traceability):** Every transition produces a verifiable transition record.
* **INV-OBLIGATION-SEPARATION-001 (Obligation Separation):** Obligations survive exit without forcing citizenship retention.
