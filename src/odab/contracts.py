from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnalysisIntent:
    intent_id: str
    purpose: str
    allowed_operations: tuple[str, ...]
    source_refs: tuple[str, ...]
    authorization_ref: str | None = None


@dataclass(frozen=True)
class DatasetEnvelope:
    source_ref: str
    schema_version: str
    rows: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class Finding:
    claim: str
    method: str
    evidence_refs: tuple[str, ...]
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceArtifact:
    artifact_version: str
    entity_id: str
    intent_id: str
    input_digest: str
    findings: tuple[Finding, ...]
    status: str
    limitations: tuple[str, ...]
    output_digest: str
