import hashlib
import os

import pandas as pd

from draudit.core.types import DatasetSnapshot


def compute_snapshot_id(file_path: str) -> str:
    """
    Compute a deterministic hash of the raw dataset file bytes.

    Why raw bytes?
    - DataFrames can reorder rows
    - Pandas may normalize values
    - File bytes are the only ground truth

    Same file bytes -> same snapshot ID
    """

    hasher = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def create_snapshot(df: pd.DataFrame, file_path: str, schema: dict) -> DatasetSnapshot:
    """
    Create an immutable snapshot describing the dataset at ingestion time.
    """

    snapshot_id = compute_snapshot_id(file_path)

    return DatasetSnapshot(
        snapshot_id=snapshot_id,
        file_path=file_path,
        file_type=os.path.splitext(file_path)[1].lower(),
        file_size_bytes=os.path.getsize(file_path),
        row_count=len(df),
        column_count=len(df.columns),
        columns=list(df.columns),
        dtypes=schema,
    )
