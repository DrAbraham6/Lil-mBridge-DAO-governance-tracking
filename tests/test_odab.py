import pytest

from odab.analyzer import (
    canonical_bytes,
    profile_dataset,
    sha256_digest,
)
from odab.contracts import AnalysisIntent, DatasetEnvelope
from odab.evidence import generate_evidence_artifact


def test_digest_is_stable():
    assert sha256_digest({"a": 1, "b": 2}) == (
        sha256_digest({"b": 2, "a": 1})
    )


def test_empty_dataset_is_explicit():
    dataset = DatasetEnvelope(
        source_ref="fixture:empty",
        schema_version="1",
        rows=(),
    )
    findings = profile_dataset(dataset)
    assert findings
    assert "empty" in findings[0].claim.lower()


def test_missing_values_are_reported():
    dataset = DatasetEnvelope(
        source_ref="fixture:missing",
        schema_version="1",
        rows=(
            {"amount": 10},
            {"amount": None},
        ),
    )
    findings = profile_dataset(dataset)
    assert any("1 missing" in f.claim for f in findings)


def test_non_finite_digest_values_are_rejected():
    with pytest.raises(ValueError):
        canonical_bytes({"value": float("nan")})


def test_boolean_is_not_treated_as_a_number():
    dataset = DatasetEnvelope(
        source_ref="fixture:boolean",
        schema_version="1",
        rows=({"flag": True}, {"flag": False}),
    )
    findings = profile_dataset(dataset)
    assert not any("mean:" in f.claim for f in findings)


def test_generate_evidence_artifact_success():
    intent = AnalysisIntent(
        intent_id="intent-001",
        purpose="produce_reproducible_data_findings",
        allowed_operations=("inspect_data", "compute_statistics"),
        source_refs=("fixture:dataset1",),
        authorization_ref="auth-ref-123",
    )
    dataset = DatasetEnvelope(
        source_ref="fixture:dataset1",
        schema_version="1.0",
        rows=(
            {"val": 10},
            {"val": 20},
            {"val": 30},
        ),
    )

    artifact = generate_evidence_artifact(intent, dataset)

    assert artifact.entity_id == "odab.reference.v0.1"
    assert artifact.intent_id == "intent-001"
    assert artifact.status == "completed"
    assert artifact.input_digest == sha256_digest(dataset)
    assert len(artifact.findings) > 0
    assert len(artifact.output_digest) == 64


def test_evidence_artifact_requires_authorization_ref():
    intent = AnalysisIntent(
        intent_id="intent-002",
        purpose="produce_reproducible_data_findings",
        allowed_operations=("inspect_data", "compute_statistics"),
        source_refs=("fixture:dataset1",),
        authorization_ref=None,
    )
    dataset = DatasetEnvelope(
        source_ref="fixture:dataset1",
        schema_version="1.0",
        rows=({"val": 10},),
    )

    with pytest.raises(PermissionError, match="authorization_ref is missing"):
        generate_evidence_artifact(intent, dataset)


def test_evidence_artifact_requires_allowed_operations():
    intent = AnalysisIntent(
        intent_id="intent-003",
        purpose="produce_reproducible_data_findings",
        allowed_operations=("inspect_data",),
        source_refs=("fixture:dataset1",),
        authorization_ref="auth-ref-123",
    )
    dataset = DatasetEnvelope(
        source_ref="fixture:dataset1",
        schema_version="1.0",
        rows=({"val": 10},),
    )

    with pytest.raises(PermissionError, match="compute_statistics"):
        generate_evidence_artifact(intent, dataset)


def test_evidence_artifact_requires_valid_source_ref():
    intent = AnalysisIntent(
        intent_id="intent-004",
        purpose="produce_reproducible_data_findings",
        allowed_operations=("inspect_data", "compute_statistics"),
        source_refs=("fixture:authorized_source",),
        authorization_ref="auth-ref-123",
    )
    dataset = DatasetEnvelope(
        source_ref="fixture:unauthorized_source",
        schema_version="1.0",
        rows=({"val": 10},),
    )

    with pytest.raises(PermissionError, match="not permitted"):
        generate_evidence_artifact(intent, dataset)
