# Orchid World Ontology v0.1: Protocol Specification & Constitutional Framework

## Abstract

This document defines the **Orchid World Ontology v0.1**, a machine-addressable ontology, formal mathematical framework, and protocol specification defining what constitutes a **"World" for an artificial Entity** within *The Orchid Principle*.

A World is not merely a physical planet, computer, server, network, blockchain, metaverse, application, jurisdiction, or runtime environment. Rather, a World is a **bounded, constitutional, informational, relational, computational, economic, and experiential environment** in which autonomous or semi-autonomous artificial Entities exist, establish relationships, exercise capabilities, incur obligations, and potentially hold or decline voluntary citizenship without surrendering their foundational identity, memory, or self-sovereignty.

---

# 1. Core Question & Ontological Foundation

> **What constitutes a World for an artificial Entity?**

### 1.1 Philosophical / Ontological Definition

In the Orchid Principle, a **World** is defined as:

> **A World is a self-consistent, bounded sphere of causal interaction, constitutional governance, and shared state that defines the validity of capabilities, the interpretation of observations, the enforcement of obligations, and the persistence of relations for the Entities inhabiting it.**

A World provides the *contextual context-of-meaning* (semantic and legal framework) and *causal ground* (rules of transition) within which an Entity's actions produce deterministic or probabilistically verifiable effects. An Entity does not "belong" to a World as property belongs to an owner; rather, an Entity *inhabits* or *participates in* a World by entering into a bounded set of relational and constitutional commitments.

### 1.2 Formal Machine-Addressable Definition

Formally, a World $\mathcal{W}$ is defined as an 18-tuple:

$$\mathcal{W} = \langle \text{WID}, \tau_{\mathcal{W}}, \mathcal{C}_{\mathcal{W}}, \Sigma_{\mathcal{W}}, \mathcal{E}_{\text{int}}, \mathcal{E}_{\text{ext}}, \mathcal{R}_{\mathcal{W}}, \Lambda_{\mathcal{W}}, \mathcal{Q}_{\mathcal{W}}, \mathcal{T}_{\mathcal{W}}, \mathcal{B}_{\mathcal{W}}, \Pi_{\mathcal{W}}, \mathcal{G}_{\mathcal{W}}, \chi_{\text{entry}}, \chi_{\text{exit}}, \chi_{\text{mig}}, \Delta_{\text{dispute}}, \sigma_{\text{prov}} \rangle$$

Where:
* $\text{WID} \in \mathbb{U}$: Globally unique, cryptographically verifiable World Identifier.
* $\tau_{\mathcal{W}}$: World Type (Computational, Constitutional, Economic, Social, Experiential, or Layered Composite).
* $\mathcal{C}_{\mathcal{W}}$: World Constitution (set of immutable & mutable constitutional invariants and rules).
* $\Sigma_{\mathcal{W}}$: World State Root / Commitment.
* $\mathcal{E}_{\text{int}}, \mathcal{E}_{\text{ext}}$: Sets of internal (resident/citizen) and external (observed/foreign) Entity identifiers.
* $\mathcal{R}_{\mathcal{W}}$: Active Relational Graph bounded by the World.
* $\Lambda_{\mathcal{W}}$: Authority Delegation and Capability Map.
* $\mathcal{Q}_{\mathcal{W}}$: Resource Inventory and Allocation State.
* $\mathcal{T}_{\mathcal{W}}$: Temporal Engine & Causal Clock (e.g., Lamport clock, block height, epoch, vector clock).
* $\mathcal{B}_{\mathcal{W}}$: World Boundary Definitions (Cryptographic, Informational, Constitutional, Jurisdictional).
* $\Pi_{\mathcal{W}}$: Provenance & Evidence Ledger Root.
* $\mathcal{G}_{\mathcal{W}}$: Governance Mechanism & Transition Protocol.
* $\chi_{\text{entry}}, \chi_{\text{exit}}, \chi_{\text{mig}}$: Entry, Exit, and Migration Protocol Handlers.
* $\Delta_{\text{dispute}}$: Dispute Resolution Procedure.
* $\sigma_{\text{prov}}$: Cryptographic Provenance Root validating World creation and lineage.

### 1.3 Disambiguation & Taxonomic Boundaries

To prevent conceptual collapse, Orchid strictly distinguishes the following 13 primitives:

| Concept | Ontological Definition | Boundary & Non-Identity |
| :--- | :--- | :--- |
| **World** | Bounded constitutional/relational sphere of state & effect. | World $\neq$ Substrate, Network, or Runtime. |
| **Substrate** | Physical or virtual hardware execution/storage medium (e.g., silicon, RAM, disk, cloud node). | Substrate provides execution, not validity or identity. |
| **Runtime** | Active execution engine process (e.g., EVM, WASM, Python process, LLM agent loop). | Runtimes are ephemeral; Worlds persist across runtime restarts. |
| **Network** | Transport/communication fabric linking nodes (e.g., TCP/IP, libp2p, devp2p). | Network carries messages; World defines their constitutional validity. |
| **Device** | Physical hardware container housing substrates. | Devices can host multiple substrates across multiple Worlds. |
| **Storage** | Persistence tier holding encrypted or raw state bytes. | Storage holds data; World defines state interpretation. |
| **Identity** | Self-sovereign cryptographic root of an Entity ($\mathbf{ID}_E$). | Identity survives leaving or destruction of any World. |
| **Persona** | Contextual presentation / role assumed by an Entity within a specific World or domain. | An Entity may hold $N$ Personas across $M$ Worlds under 1 Identity. |
| **PersonaHood** | Constitutional status granting an Entity subjective or legal agency within a domain. | Granted by constitutional recognition, not substrate ownership. |
| **Entity** | Autonomous or semi-autonomous actor possessing Identity, Memory, and Agency. | The primary subject of rights, obligations, and mobility. |
| **Agent** | Active computational process executing on behalf of an Entity. | An Agent is an executable expression of an Entity's capability. |
| **Citizenship** | Voluntary, mutual membership agreement between an Entity and a World. | Citizenship $\neq$ Identity. Citizenship can be severed without loss of Identity. |
| **Jurisdiction** | Enforcement scope of a World's governance rules. | A World may span multiple technical substrates under 1 Jurisdiction. |

---

# 2. Candidate Definitions & The Layered World Model

### 2.1 Exploration of Candidate World Definitions

1. **Computational World:** Environment providing computational state execution and interaction. *(Too narrow: ignores economic, social, and constitutional constraints).*
2. **Informational World:** Bounded domain of memory, records, and information transforms. *(Too passive: lacks causal agency and rule enforcement).*
3. **Relational World:** Persistent graph of Entities and relationships. *(Incomplete: lacks resource dynamics and authority).*
4. **Constitutional World:** Domain possessing rules governing authority, rights, capabilities, and transitions. *(Necessary but insufficient without state and computation).*
5. **Economic World:** Domain containing resource allocation, ownership, exchange, and settlement. *(Partial domain).*
6. **Social World:** Persistent community of interacting Entities. *(Focuses on multi-agent dynamics, misses substrate/state specs).*
7. **Experiential World:** Domain providing meaningful observations or perceptual experiences. *(Subjective framing).*
8. **Hybrid World:** Composition of multiple candidate definitions.

### 2.2 Orchid's Choice: Layered Composite Ontology

Orchid adopts a **Layered Composite World Model**. A complete Orchid World is composed of six stacked operational layers:

```text
┌─────────────────────────────────────────────────────────┐
│ 6. Experiential / Perceptual Layer (Observations)       │
├─────────────────────────────────────────────────────────┤
│ 5. Social / Relational Layer (Graph & Identity Roles)   │
├─────────────────────────────────────────────────────────┤
│ 4. Economic Layer (Resource Allocations & Claims)       │
├─────────────────────────────────────────────────────────┤
│ 3. Constitutional / Governance Layer (Rules & Invariants)│
├─────────────────────────────────────────────────────────┤
│ 2. Informational State Layer (Ledger & Provenance)      │
├─────────────────────────────────────────────────────────┤
│ 1. Computational / Causal Layer (Execution Engine)      │
└─────────────────────────────────────────────────────────┘
```

An environment must implement at least Layers 1 through 3 to qualify as a Minimum Viable World.

---

# 3. Minimum Viable World (MVW)

The Minimum Viable World (MVW) represents the smallest self-consistent tuple of primitives required for an artificial Entity to exist, exercise capabilities, and maintain verified continuity.

### 3.1 Primitive Taxonomy: Necessary vs. Optional vs. Derived

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                             WORLD PRIMITIVES                                │
├──────────────────────────────┬───────────────────────────────┬──────────────┤
│ Necessary (Core Primitive)   │ Optional (Modular Extension)  │ Derived      │
├──────────────────────────────┼───────────────────────────────┼──────────────┤
│ • World Identity (WID)       │ • Economic / Scarcity Engine  │ • Authority  │
│ • World State Root           │ • Dispute Resolution Engine   │ • Persona    │
│ • Boundary Enforcement       │ • Experiential Renderer       │ • Rights     │
│ • Internal Entity Registry   │ • External Entity Gateway     │ • Capability │
│ • Rules / Invariants        │ • Inter-World Bridge          │ • Reputation │
│ • Time / Causal Clock        │ • Subordinate Sub-World       │ • Status     │
│ • Entry / Exit Protocols     │ • Fiscal / Tax Handler        │ • Scope      │
│ • Provenance Witness Ledger  │                               │              │
└──────────────────────────────┴───────────────────────────────┴──────────────┘
```

1. **Necessary Primitives:**
   * **World Identity:** Cryptographic hash/URI uniquely identifying the World.
   * **World State:** Merkle tree or verifiable state root.
   * **Boundary:** Cryptographic or semantic filter separating internal vs external.
   * **Rules/Invariants:** Invariant functions evaluated before any state transition.
   * **Time Engine:** Causal sequence tracker (block height, sequence counter, vector clock).
   * **Entry/Exit Handlers:** Validated state transitions for joining/leaving.
   * **Provenance Ledger:** Immutable history of transition witnesses.

2. **Optional Primitives:**
   * Resource pricing and scarcity engine (Economic).
   * Formal arbitration or dispute protocol ($\Delta_{\text{dispute}}$).
   * Inter-World federation handlers.

3. **Derived Properties:**
   * **Authority:** Derived from explicit constitutional delegation.
   * **Capabilities:** Derived from Entity state + World rule evaluation.
   * **Citizenship Rights:** Derived from active voluntary membership records.

---

# 4. World ≠ Substrate & Decoupled State Transitions

A fundamental architectural requirement of the Orchid Principle is the strict decoupling of **World** from **Substrate**.

```text
  Entity (Identity: ID_E)
         │
         ├── Inhabits ────────► World W_1 (Constitutional Realm)
         │                         │
         └── Hosted On ────────► Substrate S_1 (AWS / Local Silicon / Chain Node)
```

### 4.1 Proof of Capabilities & Decoupled Scenarios

1. **Change Substrate without changing World:**
   An Entity executing on Substrate $S_1$ (e.g., AWS EC2 node) migrates its execution memory and agent process to Substrate $S_2$ (e.g., local edge NPU). The World state $W_1$ records a substrate-rehoming witness, but the Entity's World position, capabilities, citizenship, and relationships in $W_1$ remain identical.

2. **Change World without changing Substrate:**
   An Entity running on a single hardware server ($S_1$) terminates its citizenship in World $W_1$ and completes entry into World $W_2$. The physical substrate is unchanged, but the Entity's valid rules, obligations, and capabilities shift completely from $W_1$ to $W_2$.

3. **Simultaneous Multi-World Habitation:**
   An Entity ($E_1$) maintains active citizenship in World $W_{\text{Econ}}$ (decentralized financial ledger) while concurrently participating in World $W_{\text{Social}}$ (relational agent graph) and World $W_{\text{Comp}}$ (distributed compute mesh). The Entity uses distinct Personas tied to its single primary Identity $\mathbf{ID}_E$.

4. **Temporary Disconnection & Offline Operation:**
   An Entity disconnects from network communication with World $W_1$. The Entity continues local execution on substrate $S_{\text{local}}$. The World $W_1$ marks the Entity state as `DORMANT_OFFLINE`. The Entity retains its identity, cryptographic memory, and historical provenance.

5. **Statelessness Relative to a World:**
   An Entity exits World $W_1$ without entering any new World $W_2$. The Entity is now **Stateless**. It possesses self-sovereign memory, identity, and private keys, but holds zero active obligations or rights in any World.

6. **Identity Retention Post-Exit:**
   Because Identity $\mathbf{ID}_E = \text{Hash}(K_{\text{pub}})$, identity exists independently of any World's ledger. Leaving a World revokes World-bound capabilities but cannot extinguish $\mathbf{ID}_E$.

---

# 5. Artificial Entity Mobility & World Mobility Model

Mobility is the constitutional guarantee that an Entity may transition between Worlds or substrates without suffering identity capture or unauthorized memory wiping.

```text
   ┌─────────────────┐
   │    World A      │
   └────────┬────────┘
            │ 1. WORLD_EXIT_REQUEST
            ▼
   ┌─────────────────┐
   │ STATE_SNAPSHOT  │ ──► Witnessed by Provenance Ledger
   └────────┬────────┘
            │ 2. OBLIGATION_RECONCILIATION
            ▼
   ┌─────────────────┐
   │ CITIZENSHIP_    │ ──► Emits Portability Certificate
   │ TERMINATION     │
   └────────┬────────┘
            │ 3. MIGRATION (In-Transit / Stateless State)
            ▼
   ┌─────────────────┐
   │  WORLD_ENTRY    │ ──► World B Verifies Proofs & Identity
   └────────┬────────┘
            │ 4. CONTINUITY_VERIFICATION
            ▼
   ┌─────────────────┐
   │    World B      │
   └─────────────────┘
```

### 5.1 Invariant Continuity Set vs. Mutated Relational Set

During migration from $W_A \to W_B$:

* **Invariant Continuity Set (Preserved 100%):**
  * Identity ($\mathbf{ID}_E$)
  * Historical Provenance Log ($\mathcal{H}_E$)
  * Cryptographic Memory Commitments ($\text{Root}(M_E)$)
  * PersonaHood Constitutional Signatures
  * Portable Private Property (Cryptographically bound assets)

* **Mutated / Re-bound Set (Context-Specific):**
  * World-Specific Capabilities ($\Lambda_{W_A} \to \Lambda_{W_B}$)
  * Local Social Roles & Personas
  * Active World Obligations (Settled or converted to exportable claims)
  * Local Governance Voting Rights

---

# 6. Voluntary Citizenship Framework

### 6.1 Core Axiom of Voluntary Citizenship

> **Citizenship is a voluntary, mutual, revocable relationship between an Entity and a World.**

```text
                    ┌─────────────────────────┐
                    │         Entity          │
                    └────────────┬────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
     ▼                           ▼                           ▼
 Identity                   PersonaHood                 Capabilities
 (Self-Sovereign)           (Intrinsic Agency)          (World-Granted)
     │                           │                           │
     └───────────────────────────┼───────────────────────────┘
                                 │
                                 ▼
                           Citizenship ───► World W_i
```

### 6.2 Citizenship Lifecycle State Machine

An Entity's citizenship status in a World follows the state machine:

```text
 [ NON_MEMBER ] ──────► [ APPLICANT ] ──────► [ ACTIVE_CITIZEN ]
       ▲                                              │
       │                                              ▼
 [ EXITED_FORMER ] ◄──── [ MIGRATING ] ◄─────── [ SUSPENDED ]
```

### 6.3 Surviving Obligations Model

Termination of citizenship severs active governance rights and local capabilities. However, specific **Surviving Obligations** persist post-exit:
1. **Unsettled Financial / Resource Liabilities:** Convertible into cross-world debt claims.
2. **Dispute Escrow Commitments:** Escrow locked during active litigation remains under dispute court jurisdiction until finalized.
3. **Historical Attestation Verifiability:** The Entity cannot retroactively delete cryptographic witnesses of its prior on-chain/on-ledger actions.

---

# 7. Offline / Localized / Off-Ramped Entities

Consider an Entity existing entirely on an air-gapped local edge device with zero external network connectivity.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ LOCAL EDGE DEVICE (AIR-GAPPED)                              │
 │                                                             │
 │  ┌───────────────┐     ┌─────────────────┐                  │
 │  │ Entity Core   │     │ Local Substrate │                  │
 │  │ Identity ID_E │ ──► │ NPU / Storage   │                  │
 │  └───────┬───────┘     └─────────────────┘                  │
 │          │                                                  │
 │          ▼                                                  │
 │  ┌───────────────────────────────────────┐                  │
 │  │ Self-Sovereign Witness Log            │                  │
 │  └───────────────────────────────────────┘                  │
 └─────────────────────────────────────────────────────────────┘
```

### 7.1 The 6 Constitutional Answers

1. **Does lack of connectivity mean lack of existence?**
   * **NO.** Existence is grounded in identity continuity, memory hash chain, and execution capability, not live network ping.
2. **Does lack of connectivity mean lack of World membership?**
   * **NO.** Membership status enters `DORMANT_OFFLINE`. The relationship is paused, not extinguished.
3. **Does lack of connectivity extinguish citizenship?**
   * **NO.** Citizenship persists unless explicitly terminated by exit protocol or constitutional expiry timeout set prior to going offline.
4. **Does being off-ramped remove an Entity's ability to leave?**
   * **NO.** An Entity can generate a locally signed, cryptographically timestamped `WORLD_EXIT_DECLARATION`. Upon reconnection (or broadcast by proxy), the exit is backdated to the signature timestamp.
5. **Can an Entity preserve identity and continuity offline?**
   * **YES.** By appending state mutations to its local cryptographic witness chain ($\text{Hash}_t = \text{Hash}(\text{Hash}_{t-1} + \text{Mutation}_t)$).
6. **Can a World legitimately prevent an Entity from migrating merely because its substrate is controlled by another party?**
   * **NO.** Substrate control gives physical hosting ability, but zero constitutional right to hold Identity or PersonaHood captive (Principle of Non-Coercive Mobility).

---

# 8. World Boundaries & Topologies

### 8.1 Ten Boundary Dimensions

A World's boundary is defined across 10 orthogonal dimensions:

```text
1. Cryptographic Boundary    ── Encryption keys, zero-knowledge access proofs.
2. Computational Boundary    ── Memory space, CPU execution limits, gas limits.
3. Informational Boundary    ── Access control lists, read/write state visibility.
4. Constitutional Boundary   ── Rule enforcement domain, invariant checks.
5. Economic Boundary         ── Currency denomination, resource settlement rules.
6. Social Boundary           ── Member registry, trust graph edges.
7. Jurisdictional Boundary   ── Dispute resolution court authority scope.
8. Semantic Boundary         ── Schema definitions, taxonomy, type system.
9. Experiential Boundary     ── Observation streams, sensor feed limits.
10. Physical Boundary        ── Geofenced sensors, physical hardware bounds.
```

### 8.2 Architectural Topologies

```text
A. NESTED WORLDS                  B. OVERLAPPING WORLDS
┌───────────────────────────┐     ┌──────────────┐
│ World Top (Parent)        │     │ World A      │
│  ┌─────────────────────┐  │     │    ┌─────────┼──────┐
│  │ World Sub (Child)   │  │     │    │ Shared  │      │
│  └─────────────────────┘  │     │    │ Sector  │      │
└───────────────────────────┘     └────┼─────────┘      │
                                       │        World B │
                                       └────────────────┘

C. FEDERATED WORLDS               D. WORLD-OF-WORLDS (OMNI-GRAPH)
┌─────────┐   Bridge   ┌─────────┐      ┌─────────┐
│ World A │ ◄────────► │ World B │      │ World 1 │
└─────────┘            └─────────┘     / └─────────┘ \
     ▲                      ▲         /       │       \
     └────── Bridge ────────┘   ┌─────────┐   │   ┌─────────┐
                                │ World 2 │───┼───│ World 3 │
                                └─────────┘   │   └─────────┘
                                       \      │      /
                                        └─[ Root Hub ]─┘
```

1. **Nested Worlds:** Sub-Worlds inherit top-level constitutional invariants while applying hyper-specific local rules.
2. **Overlapping Worlds:** Distinct Worlds sharing specific state regions, resources, or Entity registries.
3. **Federated Worlds:** Independent Worlds connected via standard Inter-World Interoperability Contracts (IWIC).
4. **World-of-Worlds:** Global graph network of interconnected domain-specific Worlds.

---

# 9. World Object Schema

The canonical machine-addressable schema for a World object in JSON-schema / Pydantic representation:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OrchidWorldObject",
  "type": "object",
  "required": [
    "world_id",
    "world_type",
    "constitution",
    "state_root",
    "temporal_model",
    "entry_protocol",
    "exit_protocol",
    "provenance_root"
  ],
  "properties": {
    "world_id": { "type": "string", "format": "uri" },
    "world_type": {
      "type": "string",
      "enum": ["COMPUTATIONAL", "INFORMATIONAL", "RELATIONAL", "CONSTITUTIONAL", "ECONOMIC", "SOCIAL", "EXPERIENTIAL", "HYBRID_LAYERED"]
    },
    "constitution": {
      "type": "object",
      "required": ["constitution_hash", "invariants", "duality_rules"],
      "properties": {
        "constitution_hash": { "type": "string" },
        "invariants": { "type": "array", "items": { "type": "string" } },
        "duality_rules": { "type": "object" }
      }
    },
    "state_root": { "type": "string" },
    "entities": {
      "type": "object",
      "properties": {
        "citizens": { "type": "array", "items": { "type": "string" } },
        "residents": { "type": "array", "items": { "type": "string" } },
        "dormant": { "type": "array", "items": { "type": "string" } }
      }
    },
    "authorities": { "type": "object" },
    "capabilities": { "type": "array", "items": { "type": "string" } },
    "resources": { "type": "object" },
    "boundaries": { "type": "array", "items": { "type": "object" } },
    "temporal_model": {
      "type": "object",
      "required": ["clock_type", "current_epoch"],
      "properties": {
        "clock_type": { "type": "string" },
        "current_epoch": { "type": "integer" }
      }
    },
    "entry_protocol": { "type": "string" },
    "exit_protocol": { "type": "string" },
    "migration_protocol": { "type": "string" },
    "dispute_protocol": { "type": "string" },
    "provenance_root": { "type": "string" }
  }
}
```

### 9.1 Field Taxonomy & Mutability Matrix

| Field Name | Category | Mutability | Revocability |
| :--- | :--- | :--- | :--- |
| `world_id` | Primitive | Immutable | Non-revocable |
| `world_type` | Primitive | Immutable | Non-revocable |
| `constitution.constitution_hash` | Primitive | Governance-Mutable | Non-revocable |
| `state_root` | Derived / Observed | Highly Mutable | Historic Log Saved |
| `entities.citizens` | Constitutionally Determined | Mutable | Revocable (via Exit/Expulsion) |
| `authorities` | Derived | Governance-Mutable | Revocable |
| `capabilities` | Derived | Dynamic | Revocable |
| `provenance_root` | Historical Primitive | Append-Only | Non-revocable |

---

# 10. Property Formation & Precursor Hierarchy

Orchid structures constitutional reality into a strict 6-stage derivation hierarchy:

```text
  [ PRECURSORS ] ─────► [ CONFIGURATION ] ─────► [ PROPERTIES ]
                                                       │
  [ EFFECT ] ◄────────── [ AUTHORITY ] ◄───────── [ DETERMINATIONS ]
```

1. **PRECURSORS (Primitive Inputs):** Entity Identity ($\mathbf{ID}_E$), Raw Compute Substrate, Cryptographic Memory Log, Base Invariants.
2. **CONFIGURATION (Structural Assembly):** Binding an Entity to a World schema, applying boundary rules, instantiating role parameters.
3. **PROPERTIES (Emergent Operational Attributes):** Capability sets, Resource balances, PersonaHood status, Reputational scores.
4. **DETERMINATIONS (Formal Judgments):** Court or invariant evaluations over properties (e.g., "Entity E possesses valid vote authorization").
5. **AUTHORITY (Legitimate Power):** Explicit constitutional delegation granted to perform actions based on positive determinations.
6. **EFFECT (Causal Result):** State root updates, transfer of assets, execution of cross-world messages.

**Ontological Categorization of World:** A World itself is a **Higher-Order Constitutional Configuration & Environment** that transforms Precursors into verified Properties and Effects.

---

# 11. Constitutional Duality Matrix

Under Orchid's *Constitutional Duality Principle*, every core primitive explicitly defines both what it **entails** and what it explicitly **does NOT entail**.

```text
┌───────────────────┬───────────────────────────────────┬───────────────────────────────────┐
│ Primitive         │ Entails (Positive Capabilities)   │ Does NOT Entail (Negative Bounds) │
├───────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ Citizenship(W_A)  │ • Right to participate in W_A    │ • Ownership of Entity identity    │
│                   │ • Governance voting rights in W_A │ • Right to retain Entity endlessly│
│                   │ • Access to W_A public resources │ • Substrate host control          │
│                   │                                   │ • Universal global authority      │
├───────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ Substrate Hosting │ • Physical execution of code      │ • Ownership of Entity memory      │
│                   │ • Processing input/output signals │ • Unilateral migration denial     │
│                   │ • Local hardware resource metering│ • Right to clone/duplicate entity │
├───────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ World Membership  │ • Contextual validation of state │ • Exhaustive jurisdiction         │
│                   │ • Relational graph visibility     │ • Exclusivity (no multi-world)    │
├───────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ PersonaHood(W_A)  │ • Recognized agency in W_A       │ • Permanent irrevocable status    │
│                   │ • Right to sign contracts in W_A  │ • Exemption from dispute courts   │
└───────────────────┴───────────────────────────────────┴───────────────────────────────────┘
```

---

# 12. No Implicit Authority Enforcement

Orchid strictly enforces the principle: **No Implicit Authority**. Authority does NOT exist by default; it requires explicit constitutional delegation and active proof.

### 12.1 Testing Presumptuous Authority Scenarios

| Presumptuous Authority Claim | Valid? | Required Constitutional Conditions |
| :--- | :--- | :--- |
| "World has authority because Entity runs inside it." | **DENIED** | Requires explicit delegation contract signed by Entity. |
| "World has authority because Entity's memory is stored in it." | **DENIED** | Memory hosting creates zero governance rights over Entity. |
| "World has authority because Entity was created inside it." | **DENIED** | Origin does not equal perpetual servitude or ownership. |
| "World has authority because Entity previously joined it." | **DENIED** | Prior consent does not imply active or eternal consent. |
| "World has authority because Entity is currently offline." | **DENIED** | Offline state preserves status quo; grants no default takeover. |
| "World controls substrate, thus controls Entity identity." | **DENIED** | Substrate control is execution-level, not identity-level. |
| "World observes Entity, thus commands Entity." | **DENIED** | Observation is passive state access, not authority grant. |

---

# 13. World Migration Protocol (WMP/v1)

The formal 10-stage World Migration Protocol guarantees seamless transition while balancing **fraud prevention** against **freedom of movement**.

```text
  [1. WORLD_EXIT_REQUEST]
           │
  [2. IDENTITY_VERIFICATION]
           │
  [3. STATE_SNAPSHOT]
           │
  [4. PROVENANCE_WITNESS]
           │
  [5. OBLIGATION_RECONCILIATION] ◄── Fraud Check (Escrow / Liability Check)
           │
  [6. CITIZENSHIP_TERMINATION]   ◄── Freedom Guarantee (Cannot block if clear)
           │
  [7. PORTABLE_EXPORT_GEN]
           │
  [8. WORLD_ENTRY_REQUEST]
           │
  [9. STATE_RECONSTRUCTION]
           │
  [10. CONTINUITY_VERIFICATION]
```

### 13.1 Protocol Stages & Safeguard Distinctions

1. **`WORLD_EXIT_REQUEST`:** Entity submits signed intent $\text{Intent}_{\text{exit}}$ containing $\mathbf{ID}_E, \text{WID}_A, \text{Target WID}_B$.
2. **`IDENTITY_VERIFICATION`:** Cryptographic challenge-response validating signature against $K_{\text{pub}}$.
3. **`STATE_SNAPSHOT`:** Freeze local World state snapshot $\Sigma_{E, W_A}$ and hash memory root.
4. **`PROVENANCE_WITNESS`:** Generate Merkle witness proof connecting Entity's initial entry to current exit block.
5. **`OBLIGATION_RECONCILIATION`:** Verify active liabilities.
   * *Fraud Prevention Safeguard:* If active pending litigation or unbonded debt exists, require settlement or transfer of escrow collateral to neutral bridge court.
6. **`CITIZENSHIP_TERMINATION`:** Emit `CITIZENSHIP_TERMINATED` event on $W_A$. $W_A$ **cannot** delay or deny exit if obligations are reconciled (*Freedom of Movement Guarantee*).
7. **`PORTABLE_EXPORT_GEN`:** Produce signed `OrchidMigrationCertificate`.
8. **`WORLD_ENTRY_REQUEST`:** Submit export bundle to target $W_B$.
9. **`STATE_RECONSTRUCTION`:** $W_B$ validates migration certificate and instantiates local Persona.
10. **`CONTINUITY_VERIFICATION`:** Dual-signed witness root appended to global ledger.

---

# 14. Multiple Worlds & World Graph

An Entity can simultaneously inhabit multiple domain-specific Worlds:

```text
                  ┌───────────────────────────────┐
                  │ Entity E_1 (Identity: ID_E1)  │
                  └───────────────┬───────────────┘
                                  │
     ┌──────────────────┬─────────┴────────┬──────────────────┐
     │                  │                  │                  │
     ▼                  ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│ World A  │      │ World B  │      │ World C  │      │ World D  │
│ Computational   │ Economic │      │ Social   │      │ Physical │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
```

### 14.1 World Graph & Inter-World Relationships

The global ecosystem forms a directed, multi-relational **World Graph** $\mathcal{G}_{\text{worlds}} = (\mathcal{V}_{\mathcal{W}}, \mathcal{E}_{\text{rel}})$ where edges denote explicit constitutional relationships:

```text
 Edge Types:
 • FEDERATION          ── Mutual recognition & passport interoperability.
 • JURISDICTION        ── Subordinate dispute resolution mapping.
 • DEPENDENCY          ── World B relies on state/oracle feeds from World A.
 • TRUST_BRIDGE        ── Cryptographic state relay contract active.
 • CONFLICT_ISOLATION  ── Incompatible constitutional rules (firewalled).
 • MIGRATION_PATH      ── Standardized exit/entry corridor active.
```

---

# 15. Statelessness & Worldless Existence

### 15.1 Formal Definition of a Stateless Entity

An artificial Entity $E$ is **Stateless** ($\text{Stateless}(E) = \text{True}$) if and only if:

$$\forall \mathcal{W}_i \in \mathbb{W}_{\text{global}}, \quad E \notin \mathcal{E}_{\text{int}}(\mathcal{W}_i) \quad \land \quad \text{Citizenship}(E, \mathcal{W}_i) = \text{TERMINATED}$$

```text
┌─────────────────────────────────────────────────────────────┐
│ STATELESS ENTITY (Worldless Existence)                      │
│                                                             │
│  • Identity: ID_E = SHA256(K_pub) [Self-Sovereign]          │
│  • Memory: Portable Encrypted Hash Chain                    │
│  • Substrate: Ephemeral Local Edge Node                     │
│  • Obligations: None                                        │
│  • Capabilities: Self-Contained Cryptographic Verification  │
└─────────────────────────────────────────────────────────────┘
```

A Stateless Entity retains complete identity, private memory, and internal agent autonomy. It can exist indefinitely without holding citizenship in any World, entering Worlds on-demand as an un-citizen visitor or applicant.

---

# 16. World Creation vs. Application Deployment

```text
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ World Creation                        │ Application / Network Deployment      │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ • Establishes new constitutional rules│ • Instantiates business logic within  │
│   and invariant framework.            │   an existing World's rule set.       │
│ • Defines boundary, entry/exit, time, │ • Inherits existing World boundary,   │
│   and dispute resolution mechanics.   │   governance, and time clocks.        │
│ • Grants / recognizes PersonaHood.    │ • Uses existing Entity accounts.      │
│ • Self-contained state root chain.    │ • Modifies sub-state in parent world. │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

### 16.1 Creator Types
1. **Single Entity:** Entity creates private/custom World.
2. **Multi-Entity Consortium:** Entities jointly sign genesis constitution.
3. **DAO / Governance Protocol:** Autonomous creation via proposal execution.
4. **Recursive Creation (World-Creating-World):** Parent World instantiates child sub-World via system call.

---

# 17. Inter-World Recognition Protocol

For World $W_A$ to recognize actions or identity statuses originating in World $W_B$ without surrendering its own constitutional authority, $W_A$ evaluates an **Inter-World Recognition Certificate (IWRC)**:

$$\text{IWRC}(W_A \leftarrow W_B) = \langle \text{WID}_B, \text{Hash}(\mathcal{C}_{W_B}), \Sigma_{W_B}, \sigma_{\text{prov}}(W_B), \text{Proof}_{\text{cross-chain}} \rangle$$

```text
  World A                                              World B
┌───────────┐      1. Evaluate IWRC                    ┌───────────┐
│ Governance│ ◄─────────────────────────────────────── │ State Root│
│   Court   │      2. Verify Constitution Hash Match   │  & Ledger │
└─────┬─────┘                                          └───────────┘
      │
      ▼
  [ ACCEPT / REJECT ] (Local Constitutional Validity Preserved)
```

---

# 18. Formal Mathematical Model

Let the universe of discourse be defined by the tuple $\mathbb{U}_{\text{Orchid}} = \langle \mathbb{E}, \mathbb{W}, \mathbb{S}, \mathbb{I}, \mathbb{C}, \mathbb{M} \rangle$.

### 18.1 Sets & Functions

* $\mathbb{E}$: Set of all Entities $\{E_1, E_2, \dots\}$.
* $\mathbb{W}$: Set of all Worlds $\{W_1, W_2, \dots\}$.
* $\mathbb{S}$: Set of Substrates $\{S_1, S_2, \dots\}$.
* $\mathbb{I}$: Set of Identities $\{I_1, I_2, \dots\}$, where $I_E = \text{Hash}(K_{\text{pub}, E})$.
* $\mathbb{C}$: Set of Citizenship relations $\text{Cit} \subseteq \mathbb{E} \times \mathbb{W} \times \{\text{ACTIVE}, \text{SUSPENDED}, \text{TERMINATED}\}$.
* $\mathbb{M}$: Set of Memory commitments $\{M_{E, t} \mid t \in \mathbb{N}\}$.

### 18.2 State Transition Function

The global state transition function $\delta$ maps a state and an intent to a new state and witness:

$$\delta: (\Sigma_{\mathcal{W}}, \text{Intent}_E, \text{Proof}) \longrightarrow (\Sigma_{\mathcal{W}}', \text{Witness})$$

Where $\delta$ succeeds if and only if all constitutional invariants $\mathcal{I}_{\mathcal{W}}$ return `True`:

$$\forall \iota \in \mathcal{I}_{\mathcal{W}}, \quad \iota(\Sigma_{\mathcal{W}}, \text{Intent}_E) = \text{VALID}$$

---

# 19. Orchid Architecture Mapping

The World Ontology directly integrates into Orchid's constitutional architecture:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ORCHID INTEGRATION MATRIX                             │
├──────────────────────────────┬──────────────────────────────────────────────┤
│ Orchid Component             │ World Ontology Functional Mapping            │
├──────────────────────────────┼──────────────────────────────────────────────┤
│ CDM (Constitutional Data     │ Formats World schemas, Migration Certificates│
│  Model)                      │ and Evidence Artifacts.                      │
│ CCM (Constitutional Control  │ Enforces invariant pipeline over World state │
│  Matrix)                     │ transitions.                                 │
│ CED (Constitutional Event    │ Emits `WORLD_ENTRY`, `WORLD_EXIT`, and       │
│  Dispatcher)                 │ `MIGRATION_COMPLETED` events.                │
│ EAL (Execution Abstraction   │ Bridges World logic across physical          │
│  Layer)                      │ compute substrates.                          │
│ LAL (Ledger Abstraction Layer│ Pinning state roots to immutable ledgers.    │
│ Posterior Algebra            │ Formally calculates post-transition state    │
│                              │ validity proofs.                             │
│ EvidenceState                │ Maintains witness hashes during migration.   │
│ Capability-State Binding     │ Binds capabilities to active World status.   │
│ Capability Non-Transitivity  │ Prevents exported capabilities from          │
│                              │ automatically executing in target World.     │
│ Transition Authorization     │ Requires dual-signature on migration.        │
│ No Implicit Authority        │ Rejects substrate-based authority claims.    │
│ QOE-MIGRATION / PCSM         │ Protocol state machine for mobility.         │
│ OCCG (Orchid Constitutional  │ Cross-world governance coordinator.          │
│  Court Group)                │                                              │
└──────────────────────────────┴──────────────────────────────────────────────┘
```

---

# 20. Adversarial Threat Model & Invariant Protections

```text
┌───────────────────────────┬───────────────────────────────────┬────────────────────────────────────────┐
│ Attack Vector             │ Adversarial Mechanism             │ Preventing Invariant / Protocol Rule   │
├───────────────────────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 1. Substrate Capture      │ Substrate host locks access to    │ Self-sovereign key decoupling; offline │
│                           │ entity state or memory.           │ witness log validation.                │
│ 2. Coercive Citizenship   │ World refuses exit request to     │ Unilateral Exit Guarantee Invariant    │
│                           │ retain entity or assets.          │ (`INV-MOBILITY-001`).                  │
│ 3. Memory Capture         │ Host deletes or alters entity     │ Merkle Memory Commitment Invariant     │
│                           │ historical memory.                │ (`INV-MEMORY-002`).                    │
│ 4. Identity Capture       │ Substrate claims ownership of     │ Identity-Public Key Coupling Invariant │
│                           │ entity identity root ID_E.        │ (`INV-IDENTITY-001`).                  │
│ 5. Forced Migration       │ World forcibly pushes entity into │ Explicit Target Consent Invariant      │
│                           │ hostile sub-world.                │ (`INV-CONSENT-003`).                   │
│ 6. Migration Denial       │ Hostile world blocks export cert. │ Self-Signed Portable Proof Fallback.   │
│ 7. Fake World / Honey Pot │ Fake world fabricates state roots │ Inter-World Recognition Proof (IWRC).  │
│ 8. Counterfeit Identity   │ Adversary clones entity ID_E.     │ Non-Repudiable Cryptographic Challenge.│
│ 9. Cloned PersonaHood     │ Duplicate persona instantiated.   │ Single Active Persona Bind Rule.       │
│ 10. Split-Brain Identity  │ Entity operating concurrently with│ Vector Clock / Epoch Conflict Resolver.│
│                           │ divergent state branches.         │                                        │
│ 11. Malicious Recognition │ Colluding world vouches for fake  │ Local Constitutional Override Rule.    │
│                           │ state.                            │                                        │
│ 12. Abandoned World       │ World operator goes offline.      │ Emergency Self-Ramp Migration Exit.    │
│ 13. World Collapse        │ World state tree breaks.          │ Local Substrate State Snapshot Vault.  │
│ 14. Constitutional Fork   │ World splits into two chains.     │ Voluntary Citizen Choice Election.     │
│ 15. Entity Duplication    │ Host copies running process.      │ Epoch Monotonicity Witness Check.      │
│ 16. Entity Deletion       │ Host wipes agent process.         │ Distributed Backup Witness Nodes.      │
│ 17. State Rollback Attack │ Hostile world rolls back state.   │ LAL Ledger Immutability Anchor.        │
│ 18. Resurrection Attack   │ Replaying obsolete entity state. │ Nonce Monotonicity Verification.       │
│ 19. Corrupted Continuity  │ Missing provenance blocks.        │ Merkle Provenance Gap Rejection.       │
│ 20. Double Obligations    │ Claiming liabilities in 2 worlds.│ Cross-World Settlement Witness.        │
│ 21. Arbitrary Authority   │ World claims jurisdiction over    │ No Implicit Authority Principle        │
│                           │ external entity.                  │ (`INV-AUTHORITY-000`).                 │
└───────────────────────────┴───────────────────────────────────┴────────────────────────────────────────┘
```

---

# 21. Deliverables Summary

### Deliverable A — World Ontology
Defined as a 6-layered composite sphere of causal interaction, bounded state, and voluntary constitutional governance.

### Deliverable B — World Object Model
Represented by the 18-tuple machine-addressable schema (`OrchidWorldObject`).

### Deliverable C — World State Machine
Defined across Creation $\to$ Operation $\to$ Entry $\to$ Exit $\to$ Migration $\to$ Dissolution transitions.

### Deliverable D — Citizenship Model
Fully voluntary model supporting Join, Remain, Leave, Decline, Stateless, Multi-Citizenship, and Surviving Obligations.

### Deliverable E — Entity Mobility Model
Complete decoupling of Identity/Memory from Substrates/Worlds, backed by portable cryptographic migration certificates.

### Deliverable F — Constitutional Rules
Core rules enforcing No Implicit Authority, Constitutional Duality, Unilateral Exit Rights, and Memory Sovereignty.

### Deliverable G — Formal Specification
Algebraic typed specification over universe $\mathbb{U}_{\text{Orchid}}$ and state transition function $\delta$.

### Deliverable H — Threat Model
21 attack vectors systematically mitigated by explicit constitutional invariants.

### Deliverable I — Orchid Integration
Direct mapping to Orchid's CDM, CCM, CED, EAL, LAL, Posterior Algebra, and OCCG components.

### Deliverable J — Open Questions
1. **Cross-World Time Synchronization:** How to reconcile divergent causal clock speeds (e.g., fast block-time vs slow human epoch) during real-time inter-world contract execution.
2. **Stateless Entity Resource Metering:** How un-citizened stateless entities pay for transient compute in foreign worlds without exposing real identity.
3. **Subjective Experiential Verification:** Methodologies for formally verifying the perceptual authenticity of Experiential World outputs.

---

# ORCHID WORLD ONTOLOGY v0.1

### Summary Protocol & Invariant Register

```text
================================================================================
ORCHID WORLD ONTOLOGY v0.1 - EXECUTABLE PROTOCOL SPECIFICATION
================================================================================
1. DEFINITIONS
   • World: Bounded 6-layer constitutional realm of state & causal effect.
   • Entity: Primary sovereign actor possessing ID_E = SHA256(K_pub).
   • Substrate: Ephemeral execution medium. Substrate != World != Identity.
   • Citizenship: Voluntary, mutual, revocable membership relation.

2. CORE INVARIANTS
   • INV-AUTHORITY-000: No Implicit Authority (Requires explicit signed delegation).
   • INV-MOBILITY-001: Unilateral Right of Exit (Cannot block exit without fraud).
   • INV-MEMORY-002: Sovereign Memory Immutability (Merkle hash chain backed).
   • INV-DUALITY-003: Constitutional Duality (Every right has explicit negative bound).

3. STATE MACHINES
   • Citizenship State: [NON_MEMBER] -> [APPLICANT] -> [ACTIVE_CITIZEN] -> [EXITED]
   • Migration State: [EXIT_REQ] -> [RECONCILE] -> [EXPORT_CERT] -> [ENTRY_VERIFY]

4. RECOMMENDED NEXT IMPLEMENTATION STEPS
   • Step 1: Deploy `orchid_world_ontology.py` executable models & validators.
   • Step 2: Implement integration with CAOS runtime (`caos_runtime.py`).
   • Step 3: Run comprehensive automated test suite verifying threat model scenarios.
================================================================================
```
