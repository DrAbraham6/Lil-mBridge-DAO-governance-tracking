from .analyzer import profile_dataset, sha256_digest
from .contracts import AnalysisIntent, DatasetEnvelope, EvidenceArtifact


def generate_evidence_artifact(
    intent: AnalysisIntent,
    dataset: DatasetEnvelope,
    artifact_version: str = "1.0.0",
) -> EvidenceArtifact:
    """Generate a governed, verifiable evidence artifact from an analysis intent and dataset."""
    if not intent.authorization_ref:
        raise PermissionError("External authorization required: authorization_ref is missing.")

    if dataset.source_ref not in intent.source_refs:
        raise PermissionError(
            f"Dataset source_ref '{dataset.source_ref}' is not permitted by intent source_refs."
        )

    required_operations = {"inspect_data", "compute_statistics"}
    if not required_operations.issubset(set(intent.allowed_operations)):
        missing_ops = sorted(required_operations - set(intent.allowed_operations))
        raise PermissionError(
            f"Operation(s) {missing_ops} not authorized by analysis intent."
        )

    input_digest = sha256_digest(dataset)
    findings = profile_dataset(dataset)

    # Aggregate limitations from findings and intent bounds
    finding_limitations = tuple(
        lim for finding in findings for lim in finding.limitations
    )
    limitations = tuple(dict.fromkeys(finding_limitations))

    # Construct draft artifact dictionary to compute output digest
    partial_artifact = {
        "artifact_version": artifact_version,
        "entity_id": "odab.reference.v0.1",
        "intent_id": intent.intent_id,
        "input_digest": input_digest,
        "findings": [
            {
                "claim": f.claim,
                "method": f.method,
                "evidence_refs": list(f.evidence_refs),
                "limitations": list(f.limitations),
            }
            for f in findings
        ],
        "status": "completed",
        "limitations": list(limitations),
    }

    output_digest = sha256_digest(partial_artifact)

    return EvidenceArtifact(
        artifact_version=artifact_version,
        entity_id="odab.reference.v0.1",
        intent_id=intent.intent_id,
        input_digest=input_digest,
        findings=findings,
        status="completed",
        limitations=limitations,
        output_digest=output_digest,
    )
