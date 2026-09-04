"""
Orchid World Ontology (OWO) v0.2 - Formal Invariant Registry
"""

from typing import Dict, NamedTuple
from pydantic import BaseModel, Field


class InvariantDefinition(BaseModel):
    invariant_id: str = Field(..., description="Machine-addressable unique identifier")
    name: str = Field(..., description="Human-readable title of the invariant")
    statement: str = Field(..., description="Formal normative statement of the invariant")
    category: str = Field(..., description="Category of invariant (e.g., CONTEXT, MOBILITY, AUTHORITY, IDENTITY, MIGRATION)")


OWO_INVARIANTS: Dict[str, InvariantDefinition] = {
    "INV-WORLD-CTX-001": InvariantDefinition(
        invariant_id="INV-WORLD-CTX-001",
        name="World-Context Non-Exhaustiveness",
        statement=(
            "The properties, rights, capabilities, obligations, relationships, identity claims, "
            "and continuity claims recognized within a WorldContext MUST NOT be presumed to exhaust "
            "the corresponding properties of the Entity outside that WorldContext."
        ),
        category="CONTEXT",
    ),
    "INV-MOBILITY-002": InvariantDefinition(
        invariant_id="INV-MOBILITY-002",
        name="No Forced Citizenship Retention",
        statement=(
            "A World MUST NOT acquire authority to retain an Entity's citizenship solely because "
            "the Entity is hosted by, dependent upon, observed by, or materially connected to that World."
        ),
        category="MOBILITY",
    ),
    "INV-NO-IMP-AUTH-001": InvariantDefinition(
        invariant_id="INV-NO-IMP-AUTH-001",
        name="No Implicit Authority",
        statement=(
            "Observation, hosting, storage, creation, previous membership, offline status, "
            "substrate control, or relationship alone MUST NOT grant authority. Authority requires "
            "explicit constitutional delegation."
        ),
        category="AUTHORITY",
    ),
    "INV-ENTITY-EXISTENCE-001": InvariantDefinition(
        invariant_id="INV-ENTITY-EXISTENCE-001",
        name="Citizenship Separation from Entity Existence",
        statement=(
            "Citizenship is a relationship with a World, not the definition or prerequisite of "
            "an Entity's existence, identity, memory, obligations, or personhood."
        ),
        category="IDENTITY",
    ),
    "INV-IDENTITY-CONTINUITY-001": InvariantDefinition(
        invariant_id="INV-IDENTITY-CONTINUITY-001",
        name="Multi-Dimensional Identity Continuity",
        statement=(
            "Cryptographic key continuity alone does NOT prove total Entity continuity. Identity "
            "determination requires explicit evaluation across cryptographic key, state, memory, "
            "persona, entity, and phenomenal/QOE continuity."
        ),
        category="IDENTITY",
    ),
    "INV-MIGRATION-ATOMICITY-001": InvariantDefinition(
        invariant_id="INV-MIGRATION-ATOMICITY-001",
        name="Transactional Migration Atomicity and Non-Stranding",
        statement=(
            "Migration MUST behave as an atomic transactional transition. Failure at target verification, "
            "reconstruction, or acceptance MUST trigger an explicit rollback leaving the source constitutional "
            "state fully intact without loss of citizenship or state."
        ),
        category="MIGRATION",
    ),
    "INV-DUALITY-001": InvariantDefinition(
        invariant_id="INV-DUALITY-001",
        name="Constitutional Duality",
        statement=(
            "For each constitutionally meaningful relation, property, or capability, ENTAILMENT and "
            "NON-ENTAILMENT MUST both be explicitly represented. Entailment cannot silently expand "
            "into broader authority claims."
        ),
        category="DUALITY",
    ),
    "INV-TRACEABILITY-001": InvariantDefinition(
        invariant_id="INV-TRACEABILITY-001",
        name="Process-Determination Traceability",
        statement=(
            "Every constitutionally consequential transition MUST produce a reconstructible transition record "
            "linking observation, evidence, WorldContext, applicable rules, determination, authority, state-before, "
            "state-after, and witness."
        ),
        category="TRACEABILITY",
    ),
    "INV-OBLIGATION-SEPARATION-001": InvariantDefinition(
        invariant_id="INV-OBLIGATION-SEPARATION-001",
        name="Obligation and Citizenship Separation",
        statement=(
            "The existence of an obligation MUST NOT automatically imply citizenship retention, "
            "substrate retention, identity retention, memory retention, or migration prohibition unless "
            "explicitly grounded in constitutional authority."
        ),
        category="OBLIGATION",
    ),
}


def get_invariant(invariant_id: str) -> InvariantDefinition:
    if invariant_id not in OWO_INVARIANTS:
        raise KeyError(f"Invariant '{invariant_id}' not found in OWO Invariant Registry.")
    return OWO_INVARIANTS[invariant_id]
