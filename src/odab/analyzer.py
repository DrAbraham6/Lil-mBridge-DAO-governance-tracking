import dataclasses
import hashlib
import json
import math
from collections import Counter
from typing import Any

from .contracts import DatasetEnvelope, Finding


def _to_json_compatible(value: Any) -> Any:
    """Recursively convert dataclasses, tuples, and custom structures into JSON-serializable primitives."""
    if dataclasses.is_dataclass(value):
        return _to_json_compatible(dataclasses.asdict(value))
    elif isinstance(value, dict):
        return {str(k): _to_json_compatible(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [_to_json_compatible(v) for v in value]
    return value


def canonical_bytes(value: Any) -> bytes:
    """Canonicalize supported JSON values for repeatable hashing."""
    serializable = _to_json_compatible(value)
    return json.dumps(
        serializable,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def profile_dataset(
    dataset: DatasetEnvelope,
) -> tuple[Finding, ...]:
    rows = list(dataset.rows)

    if not rows:
        return (
            Finding(
                claim="Dataset is empty.",
                method="profile_dataset.v1",
                evidence_refs=(dataset.source_ref,),
                limitations=("No statistical conclusions possible.",),
            ),
        )

    columns = sorted({key for row in rows for key in row})
    findings = []

    for column in columns:
        values = [row.get(column) for row in rows]
        missing = sum(value is None for value in values)
        observed = [value for value in values if value is not None]

        findings.append(
            Finding(
                claim=(
                    f"Column {column!r}: {len(observed)} observed "
                    f"values; {missing} missing."
                ),
                method="profile_dataset.v1",
                evidence_refs=(dataset.source_ref,),
                limitations=(
                    "Profiling is descriptive, not causal.",
                ),
            )
        )

        numeric = (
            bool(observed)
            and all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and math.isfinite(value)
                for value in observed
            )
        )

        if numeric:
            mean = sum(observed) / len(observed)
            findings.append(
                Finding(
                    claim=f"Column {column!r} mean: {mean:.12g}.",
                    method="arithmetic_mean.v1",
                    evidence_refs=(dataset.source_ref,),
                    limitations=(
                        "Mean excludes null values.",
                        "Interpretation depends on data quality.",
                    ),
                )
            )
        else:
            counts = Counter(
                canonical_bytes(value).decode("utf-8")
                for value in observed
            )
            findings.append(
                Finding(
                    claim=(
                        f"Column {column!r} has "
                        f"{len(counts)} distinct observed values."
                    ),
                    method="distinct_count.v1",
                    evidence_refs=(dataset.source_ref,),
                    limitations=("Null values are excluded.",),
                )
            )

    return tuple(findings)
