from dataclasses import dataclass
from typing import List

from draudit.core.types import DatasetSnapshot
from draudit.metadata.types import DatasetMetadata, TrustLevel


@dataclass(frozen=True)
class UnassessedRisk:
    """
    Represents a risk that cannot be evaluated due to missing
    or weakly trusted metadata.

    These are epistemic risks, not statistical ones.
    """

    category: str  # e.g. "label_provenance"
    description: str  # Human-readable explanation
    affected_component: str  # e.g. "target_column"


def resolve_metadata_and_unknowns(
    snapshot: DatasetSnapshot, metadata: DatasetMetadata
) -> List[UnassessedRisk]:
    """
    Resolve dataset metadata against required knowledge
    and extract epistemic unknowns.

    This function does NOT:
    - validate correctness
    - infer missing values
    - assign severity

    It only surfaces what cannot be assessed safely.
    """

    unknowns: List[UnassessedRisk] = []

    # Target column is foundational for ML
    if metadata.target_column.trust != TrustLevel.VERIFIED:
        unknowns.append(
            UnassessedRisk(
                category="label_provenance",
                description=(
                    "Target column is not verified. "
                    "Label correctness, noise, and policy bias cannot be assessed."
                ),
                affected_component="target_column",
            )
        )

    # Time column governs leakage and temporal validity
    if metadata.time_column.trust == TrustLevel.MISSING:
        unknowns.append(
            UnassessedRisk(
                category="temporal_context",
                description=(
                    "No time column provided. "
                    "Temporal leakage and non-stationarity cannot be evaluated."
                ),
                affected_component="time_column",
            )
        )

    # Problem type affects downstream evaluation assumptions
    if metadata.problem_type.trust == TrustLevel.MISSING:
        unknowns.append(
            UnassessedRisk(
                category="problem_definition",
                description=(
                    "Problem type is missing. "
                    "Appropriate evaluation metrics and assumptions are unclear."
                ),
                affected_component="problem_type",
            )
        )

    return unknowns
