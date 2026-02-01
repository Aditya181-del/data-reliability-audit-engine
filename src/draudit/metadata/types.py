from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TrustLevel(Enum):
    """
    Represents how trustworthy a piece of metadata is.

    This is NOT a confidence score.
    It is a provenance and verification indicator.
    """

    VERIFIED = "verified"  # Backed by documentation or data contract
    DECLARED = "declared"  # User-asserted, not independently verified
    MISSING = "missing"  # Unknown or not provided


@dataclass(frozen=True)
class MetadataField:
    """
    A single metadata field with an explicit trust boundary.

    value:
        The declared value (may be None if missing)

    trust:
        How trustworthy this value is
    """

    value: Optional[str]
    trust: TrustLevel


@dataclass(frozen=True)
class DatasetMetadata:
    """
    Collection of metadata describing the intended semantics of a dataset.

    All fields are OPTIONAL by design.
    Absence is meaningful and must be surfaced as uncertainty.
    """

    target_column: MetadataField
    time_column: MetadataField
    problem_type: MetadataField  # classification / regression
    label_description: MetadataField  # free-text description
    data_source: MetadataField  # where the data came from
