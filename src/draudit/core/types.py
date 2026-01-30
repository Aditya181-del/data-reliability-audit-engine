from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DatasetSnapshot:
    """
    Immutable, forensic representation of a dataset at ingestion time.

    This object must be sufficient to:
    - uniquely identify a dataset version
    - reproduce audit results
    - support post-mortem analysis months later
    """

    snapshot_id: str  # Deterministic hash of raw file bytes
    file_path: str  # Original dataset path
    file_type: str  # .csv / .parquet
    file_size_bytes: int  # Raw file size on disk

    row_count: int
    column_count: int
    columns: List[str]
    dtypes: Dict[str, str]


@dataclass(frozen=True)
class IngestionWarning:
    """
    Non-fatal issues detected during ingestion.
    These do NOT block the pipeline, but must be surfaced to humans.
    """

    code: str  # Stable machine-readable identifier
    message: str  # Human-readable explanation
