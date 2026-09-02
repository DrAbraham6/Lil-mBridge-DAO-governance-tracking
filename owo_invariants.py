"""
Orchid World Ontology (OWO) v0.2 - Formal Invariant Registry
------------------------------------------------------------
Machine-addressable invariant definitions, identifiers, statements, and rules.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class InvariantSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class OWOInvariant(BaseModel):
    invariant_id: str
    name: str
    statement: str
    corollary: Optional[str] = None
    severity: InvariantSeverity
    scope: List[str] = Field(default_factory=list)


# ==========================================================
# MACHINE-ADDRESSABLE INVARIANT REGISTRY
# ==========================================================
INVARIANT_REGISTRY: Dict[str, OWOInvariant] = {
    "INV-AUTHORITY-000": OWOInvariant(
        invariant_id="INV-AUTHORITY-000",
        name="No Implicit Authority",
        statement="Authority MUST NOT be inferred or derived from hosting, memory storage, origin, offline status, substrate control, relationship, or observation. Authority REQUIRES explicit, signed, constitutionally valid delegation.",
        corollary="No entity, world, substrate, runtime, observer, or intermediary may acquire effective control merely because it occupies a privileged position in the compute stack.",
        severity=InvariantSeverity.CRITICAL,
        scope=["authority:*", "governance:*", "delegation:*"]
    ),
    "INV-MOBILITY-001": OWOInvariant(
        invariant_id="INV-MOBILITY-001",
        name="Unilateral Right of Exit",
        statement="An Entity possesses an unalienable, unilateral right to exit any World. Exit MUST NOT be blocked, delayed, or denied if obligations are reconciled.",
        corollary="Freedom of movement is a constitutional primitive; host worlds cannot hold entities captive.",
        severity=InvariantSeverity.CRITICAL,
        scope=["mobility:*", "migration:*", "citizenship:*"]
    ),
    "INV-MOBILITY-002": OWOInvariant(
        invariant_id="INV-MOBILITY-002",
        name="No Forced Citizenship Retention",
        statement="A World MUST NOT acquire authority to retain an Entity's citizenship solely because the Entity is hosted by, dependent upon, observed by, or materially connected to that World.",
        corollary="Obligations may survive exit, but citizenship itself remains voluntarily terminable subject to constitutional process.",
        severity=InvariantSeverity.CRITICAL,
        scope=["citizenship:*", "mobility:*"]
    ),
    "INV-MEMORY-002": OWOInvariant(
        invariant_id="INV-MEMORY-002",
        name="Sovereign Memory Immutability",
        statement="An Entity's cryptographic memory hash chain is sovereign. Substrates and Worlds MUST NOT alter, wipe, or forge memory blocks.",
        corollary="Memory continuity is cryptographically verified independently of substrate hosts.",
        severity=InvariantSeverity.CRITICAL,
        scope=["memory:*", "state:*"]
    ),
    "INV-IDENTITY-001": OWOInvariant(
        invariant_id="INV-IDENTITY-001",
        name="Identity Determination & Key Decoupling",
        statement="Cryptographic key continuity is necessary but NOT sufficient to prove total Entity continuity. Identity determination requires multi-dimensional evidence verification.",
        corollary="Identity survives key rotation, migration, and world exit.",
        severity=InvariantSeverity.CRITICAL,
        scope=["identity:*", "evidence:*"]
    ),
    "INV-DUALITY-003": OWOInvariant(
        invariant_id="INV-DUALITY-003",
        name="Constitutional Duality",
        statement="Every constitutionally meaningful relationship, property, or capability MUST explicitly state both what it ENTAILS and what it explicitly DOES NOT ENTAIL.",
        corollary="Positive capabilities cannot silently expand into un-granted authority or negative bounds.",
        severity=InvariantSeverity.HIGH,
        scope=["constitution:*", "capability:*", "duality:*"]
    ),
    "INV-WORLD-CTX-001": OWOInvariant(
        invariant_id="INV-WORLD-CTX-001",
        name="World-Context Non-Exhaustiveness",
        statement="The properties, rights, capabilities, obligations, relationships, identity claims, and continuity claims recognized within a WorldContext MUST NOT be presumed to exhaust the corresponding properties of the Entity outside that WorldContext.",
        corollary="World membership != total jurisdiction; World observation != total knowledge; World substrate != Entity ownership.",
        severity=InvariantSeverity.CRITICAL,
        scope=["context:*", "world:*", "jurisdiction:*"]
    ),
    "INV-OBLIGATION-001": OWOInvariant(
        invariant_id="INV-OBLIGATION-001",
        name="Obligation/Citizenship Separation",
        statement="The existence of an obligation MUST NOT automatically imply citizenship retention, substrate retention, identity capture, or migration prohibition.",
        corollary="Unsettled liabilities convert to exportable debt claims or dispute escrows; they do not void voluntary exit rights.",
        severity=InvariantSeverity.HIGH,
        scope=["obligation:*", "citizenship:*", "migration:*"]
    )
}


def get_invariant(invariant_id: str) -> Optional[OWOInvariant]:
    """Retrieves an invariant by ID from the global registry."""
    return INVARIANT_REGISTRY.get(invariant_id)


def list_invariants() -> List[OWOInvariant]:
    """Returns all registered invariants."""
    return list(INVARIANT_REGISTRY.values())
