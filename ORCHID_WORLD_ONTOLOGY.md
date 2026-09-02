# Orchid World Ontology v0.2: Protocol Specification & Constitutional Hardening

## Abstract

This document defines the **Orchid World Ontology v0.2**, a machine-addressable ontology, formal mathematical framework, and executable protocol specification defining what constitutes a **"World" for an artificial Entity** within *The Orchid Principle*.

A World is not merely a physical planet, computer, server, network, blockchain, metaverse, application, jurisdiction, or runtime environment. Rather, a World is a **bounded, constitutional, informational, relational, computational, economic, and experiential environment** in which autonomous or semi-autonomous artificial Entities exist, establish relationships, exercise capabilities, incur obligations, and potentially hold or decline voluntary citizenship without surrendering their foundational identity, memory, or self-sovereignty.

Under OWO v0.2, the implementation is hardened to enforce strict constitutional guarantees: **WorldContext** is established as a first-class machine-addressable object, **Migration** is fully transactional with atomic rollback, **No Implicit Authority** is cryptographically enforced, **Identity Continuity** is decoupled from key continuity alone, and **Constitutional Duality** is executable.

---

# 1. Core Ontological Model & Derivation Pipeline

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

### 1.1 Ontological Axioms
* **World:** The persistent, bounded sphere of causal interaction and state governance.
* **WorldContext:** The constitutionally relevant projection of that World for a particular Entity, event, intent, observation, or proposed transition.
* **The Core Axiom:** $\text{World} \neq \text{WorldContext}$. A World provides context; it does not become the entirety of the Entity.

---

# 2. WorldContext as a First-Class Object

`WorldContext` is derivable and deterministically reconstructible from $\langle \text{World}, \text{Entity}, \text{State}, \text{Time}, \text{Intent/Event}, \text{Evidence} \rangle$.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "WorldContext",
  "type": "object",
  "required": [
    "context_id",
    "world_id",
    "entity_id",
    "world_state_root",
    "constitution_hash",
    "temporal_epoch",
    "temporal_sequence",
    "evidence_root",
    "context_root"
  ],
  "properties": {
    "context_id": { "type": "string" },
    "world_id": { "type": "string" },
    "entity_id": { "type": "string" },
    "world_state_root": { "type": "string" },
    "constitution_hash": { "type": "string" },
    "temporal_epoch": { "type": "integer" },
    "temporal_sequence": { "type": "integer" },
    "relevant_relations": { "type": "array", "items": { "type": "string" } },
    "relevant_capabilities": { "type": "array", "items": { "type": "string" } },
    "relevant_obligations": { "type": "array", "items": { "type": "string" } },
    "evidence_root": { "type": "string" },
    "context_root": { "type": "string" }
  }
}
```

---

# 3. Disambiguated Entity Ontology

Citizenship is a voluntary relationship between an Entity and a World, NOT the definition of Entity existence.

```text
  Entity Ontological States:
  • WORLDLESS    ── Entity exists with identity & memory, but holds no active citizenship or residence in any World.
  • STATELESS    ── Entity holds zero active citizenship in any World.
  • NON_CITIZEN  ── Entity is a resident/visitor in a World, but holds no citizenship rights.
  • OFFLINE      ── Entity is air-gapped / disconnected; state is preserved locally.
  • UNCONNECTED  ── Ephemeral execution without active network sync.
  • DORMANT      ── World relationship paused.
  • UNREGISTERED ── Un-indexed sovereign actor.
  • ACTIVE       ── Active citizen in 1 or more Worlds.
```

An Entity MUST be capable of:
* possessing identity without citizenship,
* possessing memory without citizenship,
* possessing obligations without citizenship,
* being offline without ceasing to exist,
* being worldless without being identityless.

---

# 4. Multi-Dimensional Identity Verification

Cryptographic key continuity is necessary but NOT sufficient to prove total Entity continuity. OWO v0.2 establishes multi-dimensional evidence evaluation:

$$\text{IdentityVerification} = \langle \text{Key}_{\text{proof}}, \text{State}_{\text{proof}}, \text{Memory}_{\text{proof}}, \text{Persona}_{\text{proof}}, \text{QOE}_{\text{phenomenal}} \rangle$$

Key continuity alone yields an overall confidence score of 0.25 (below the 0.75 threshold required for verification), preventing identity capture via stolen key material.

---

# 5. Cryptographic No Implicit Authority

Authority REQUIRES an explicit, unexpired, signed `DelegationContract`. `NoImplicitAuthorityChecker` enforces rejections for the 9 presumptuous claims:

```text
 1. HOSTED_ON_SUBSTRATE      ── Denied
 2. MEMORY_STORED_IN_WORLD   ── Denied
 3. CREATED_IN_WORLD         ── Denied
 4. PREVIOUSLY_JOINED        ── Denied
 5. ENTITY_OFFLINE           ── Denied
 6. SUBSTRATE_CONTROLLED     ── Denied
 7. OBSERVED_BY_WORLD        ── Denied
 8. RELATIONSHIP_EXISTS      ── Denied
 9. WORLD_OBSERVATION        ── Denied
```

Delegation contracts are validated across 9 explicit dimensions using HMAC-SHA256 signature verification over canonical JSON payloads.

---

# 6. Transactional World Migration Protocol (WMP/v2)

Migration MUST behave as a transactional constitutional transition with explicit rollback/abort semantics:

```text
  [1. SOURCE ACTIVE]
          │
  [2. PREPARED]
          │
  [3. SNAPSHOT COMMITTED]
          │
  [4. PROVENANCE WITNESSED]
          │
  [5. OBLIGATIONS RECONCILED]
          │
  [6. EXPORT CERTIFICATE ISSUED]
          │
  [7. TARGET ACCEPTED] ◄── Verified across 10 certificate checks
          │
  [8. STATE RECONSTRUCTED]
          │
  [9. CONTINUITY VERIFIED]
          │
  [10. SOURCE TERMINATION COMMITTED]
          │
  [11. TARGET ACTIVATION COMMITTED]
```

**Atomic Rollback Guarantee:** If target verification or reconstruction fails at any point prior to final commitment, the protocol enters `ABORTED_ROLLED_BACK`. The Entity's citizenship in the source World remains `ACTIVE` and intact. The Entity is never stranded or erased.

---

# 7. Process-Determination Traceability

Every constitutionally consequential transition produces a machine-addressable `ConstitutionalTransitionRecord`:

$$\text{CTR} = \langle \text{TransitionID}, \text{EntityID}, \text{WorldID}, \text{ContextRoot}, \text{EvidenceRoot}, \text{RulesRoot}, \text{DeterminationRoot}, \text{AuthorityRoot}, \text{State}_{\text{before}}, \text{State}_{\text{after}}, \text{WitnessRoot}, \text{Timestamp} \rangle$$

---

# 8. Formal Invariant Registry (`owo_invariants.py`)

1. **`INV-AUTHORITY-000` (No Implicit Authority):** Authority cannot be inferred from computational position.
2. **`INV-MOBILITY-001` (Unilateral Right of Exit):** Entities possess an unalienable right of voluntary exit.
3. **`INV-MOBILITY-002` (No Forced Citizenship Retention):** World cannot retain citizenship based on host/dependency status.
4. **`INV-MEMORY-002` (Sovereign Memory Immutability):** Memory hash chain is cryptographically sovereign.
5. **`INV-IDENTITY-001` (Identity Determination & Key Decoupling):** Key continuity != Entity continuity.
6. **`INV-DUALITY-003` (Constitutional Duality):** Capabilities explicitly define positive entailments and negative non-entailments.
7. **`INV-WORLD-CTX-001` (World-Context Non-Exhaustiveness):** WorldContext properties do not exhaust Entity properties outside that WorldContext.
8. **`INV-OBLIGATION-001` (Obligation/Citizenship Separation):** Obligations convert to exportable claims; they do not void exit rights or force citizenship retention.

---

# OWO v0.2 HARDENING REPORT
-------------------------
**Specification changes:**
* Elevated `WorldContext` to a first-class machine-addressable object ($\text{World} \neq \text{WorldContext}$).
* Disambiguated Entity existence from citizenship; added explicit ontological states (`WORLDLESS`, `STATELESS`, `NON_CITIZEN`, `OFFLINE`, `UNCONNECTED`, `DORMANT`, `UNREGISTERED`, `ACTIVE`).
* Added multi-dimensional Identity Determination decoupling key continuity from total Entity continuity.
* Re-architected World Migration Protocol (WMP/v2) to be transactional with atomic abort/rollback semantics.
* Made Constitutional Duality executable with positive entailments and negative non-entailments.

**Implementation changes:**
* `owo_invariants.py`: Formal machine-addressable invariant registry containing 8 critical/high invariants.
* `orchid_world_ontology.py`: Hardened implementation featuring `WorldContext.derive()`, `IdentityVerifier`, HMAC-SHA256 signature generation/verification, `EntityStateSnapshot`, `ConstitutionalTransitionRecord`, `NoImplicitAuthorityChecker` (9 delegation checks), `ConstitutionalDualityChecker`, and `WorldMigrationProtocol` transactional execution.

**New invariants:**
* `INV-WORLD-CTX-001`: World-Context Non-Exhaustiveness.
* `INV-MOBILITY-002`: No Forced Citizenship Retention.
* `INV-IDENTITY-001`: Identity Determination & Key Decoupling.
* `INV-OBLIGATION-001`: Obligation/Citizenship Separation.

**New models:**
* `WorldContext`
* `IdentityClaim`, `IdentityEvidence`, `IdentityVerification`, `IdentityDetermination`
* `EntityStateSnapshot`
* `ConstitutionalTransitionRecord`

**Migration changes:**
* Source citizenship remains `ACTIVE` until target World completes state reconstruction and continuity verification.
* Target World performs 10 certificate checks before accepting entry.
* Failures trigger atomic rollback restoring source citizenship and cleaning up target state.

**Cryptographic changes:**
* Standardized on HMAC-SHA256 signature generation and verification over canonical JSON payloads.
* Replaced pseudo-hashes with real signature verification in `NoImplicitAuthorityChecker` and `MigrationCertificate`.

**Adversarial tests:**
* 9 comprehensive unit tests in `test_world_ontology.py` verifying identity evidence thresholds, presumptuous authority rejections, expired/revoked delegation contracts, atomic migration rollback, constitutional duality bounds, transition record traceability, and invariant lookup.

**Known limitations:**
* Cross-world real-time vector clock synchronization across asymmetric network topologies requires further empirical bench testing.

**Remaining constitutional questions:**
* Dispute court escrow valuation across volatile inter-world asset pairs during active migration.
