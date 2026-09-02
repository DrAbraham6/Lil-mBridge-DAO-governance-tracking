# Orchid World Ontology & Protocol Specification

This repository contains the specification, executable models, and test suite for the **Orchid World Ontology v0.1** under *The Orchid Principle*.

## Overview

The Orchid World Ontology defines a machine-addressable, formal mathematical model and protocol specification for what constitutes a **"World" for an artificial Entity**.

A World is not merely a physical planet, server, network, or AI runtime. Rather, a World is a **bounded, constitutional, informational, relational, computational, economic, and experiential environment** in which autonomous or semi-autonomous artificial Entities exist, establish relationships, exercise capabilities, incur obligations, and hold or decline voluntary citizenship without surrendering their self-sovereign identity or memory.

## Key Features

1. **Decoupled Architecture:** Formal separation between *World*, *Substrate*, *Runtime*, *Entity*, *Identity*, *Persona*, and *Citizenship*.
2. **Voluntary Citizenship:** Entities can voluntarily join, leave, decline citizenship, hold multiple citizenships, or remain stateless while preserving identity.
3. **World Migration Protocol (WMP/v1):** A 10-stage state machine enabling non-coercive entity mobility between Worlds while reconciling obligations.
4. **No Implicit Authority:** Authority cannot be implied from hosting, memory storage, origin, observation, or substrate control—it requires explicit, signed delegation contracts.
5. **Layered Composite Ontology:** Integrates Computational, Informational, Relational, Constitutional, Economic, Social, and Experiential world layers.
6. **21-Vector Threat Model:** Invariant defenses against substrate capture, coercive citizenship, memory tampering, identity cloning, and split-brain attacks.

## File Structure

* `ORCHID_WORLD_ONTOLOGY.md`: The complete specification document covering Sections 1-21, Deliverables A-J, and the `ORCHID WORLD ONTOLOGY v0.1` summary block.
* `orchid_world_ontology.py`: Python module containing Pydantic data models, the 10-stage `WorldMigrationProtocol` state machine, `CitizenshipManager`, `NoImplicitAuthorityChecker`, `ThreatModelInvariantValidator`, and `WorldGraph`.
* `test_world_ontology.py`: Complete unit test suite verifying schema validation, state transitions, migration workflows, and invariant checks.

## Execution & Testing

To run the test suite:

```bash
python3 test_world_ontology.py
```

To import and use the ontology in Python:

```python
from orchid_world_ontology import (
    OrchidWorldObject, EntityObject, WorldType,
    WorldMigrationProtocol, CitizenshipManager, NoImplicitAuthorityChecker
)
```

## License

MIT License. See [LICENSE](LICENSE) for details.
