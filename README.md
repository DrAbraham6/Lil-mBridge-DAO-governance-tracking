# Orchid World Ontology & Protocol Specification (OWO v0.2)

This repository contains the specification, executable models, formal invariant registry, and test suite for the **Orchid World Ontology v0.2** under *The Orchid Principle*.

## Overview

The Orchid World Ontology defines a machine-addressable, formal mathematical model and executable protocol specification for what constitutes a **"World" for an artificial Entity**.

A World is not merely a physical planet, server, network, or AI runtime. Rather, a World is a **bounded, constitutional, informational, relational, computational, economic, and experiential environment** in which autonomous or semi-autonomous artificial Entities exist, establish relationships, exercise capabilities, incur obligations, and hold or decline voluntary citizenship without surrendering their self-sovereign identity or memory.

## Key Features in OWO v0.2 Hardening

1. **First-Class WorldContext:** Establishes `WorldContext` as a machine-addressable object ($\text{World} \neq \text{WorldContext}$).
2. **Disambiguated Entity Ontology:** Disambiguates citizenship from Entity existence; supports explicit ontological states (`WORLDLESS`, `STATELESS`, `NON_CITIZEN`, `OFFLINE`, `UNCONNECTED`, `DORMANT`, `UNREGISTERED`, `ACTIVE`).
3. **Multi-Dimensional Identity Determination:** Decouples key continuity from total Entity continuity through `IdentityVerifier` evaluating multi-dimensional evidence.
4. **Transactional Migration Protocol (WMP/v2):** 10-stage state machine with atomic abort/rollback semantics—an Entity is never stranded or erased if target entry fails.
5. **Cryptographic No Implicit Authority:** Rejects 9 presumptuous authority claims (hosting, storage, creation, offline status, observation, substrate control) using HMAC-SHA256 signature verification over delegation contracts.
6. **Executable Constitutional Duality:** Validates positive ENTAILMENT and negative NON-ENTAILMENT capability bounds.
7. **Process-Determination Traceability:** Produces reconstructible `ConstitutionalTransitionRecord` artifacts for every state transition.
8. **Formal Invariant Registry (`owo_invariants.py`):** Machine-addressable registry including `INV-WORLD-CTX-001`, `INV-MOBILITY-002`, `INV-AUTHORITY-000`, `INV-MOBILITY-001`, `INV-MEMORY-002`, `INV-IDENTITY-001`, `INV-DUALITY-003`, and `INV-OBLIGATION-001`.

## File Structure

* `ORCHID_WORLD_ONTOLOGY.md`: The complete OWO v0.2 specification document and Hardening Report.
* `owo_invariants.py`: Formal machine-addressable invariant registry.
* `orchid_world_ontology.py`: Executable Python module containing Pydantic data models, `WorldContext`, `IdentityVerifier`, `NoImplicitAuthorityChecker`, `ConstitutionalDualityChecker`, `WorldMigrationProtocol` (WMP/v2), `TransitionRecorder`, and `WorldGraph`.
* `test_world_ontology.py`: Hardened unit test suite with comprehensive adversarial tests.

## Execution & Testing

To run the unit test suite:

```bash
python3 test_world_ontology.py
```

To import and use the ontology in Python:

```python
from orchid_world_ontology import (
    OrchidWorldObject, EntityObject, WorldType, WorldContext,
    WorldMigrationProtocol, CitizenshipManager, NoImplicitAuthorityChecker,
    IdentityVerifier, ConstitutionalDualityChecker
)
```

## License

MIT License. See [LICENSE](LICENSE) for details.
