from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DatasetSnapshot:
    """
    Immutable, forensic representation of a dataset at ingestion time.
    """

    snapshot_id: str
    file_path: str
    file_type: str
    file_size_bytes: int

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

    code: str
    message: str
