import os
from typing import List, Tuple

import pandas as pd

from draudit.core.types import IngestionWarning


def load_dataset(file_path: str) -> Tuple[pd.DataFrame, List[IngestionWarning]]:
    """
    Load a dataset from disk without mutating it.

    Responsibilities:
    - Verify file exists
    - Load CSV or Parquet
    - Surface non-fatal ingestion warnings
    - Return raw DataFrame as-is

    This function MUST NOT:
    - modify values
    - coerce dtypes
    - fill missing data
    - drop rows or columns
    """

    warnings: List[IngestionWarning] = []

    # 1. File existence is non-negotiable
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # 2. Determine file type
    file_ext = os.path.splitext(file_path)[1].lower()

    # 3. Load without interpretation
    if file_ext == ".csv":
        df = pd.read_csv(file_path)
    elif file_ext == ".parquet":
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

    # 4. Non-fatal warnings
    if df.empty:
        warnings.append(
            IngestionWarning(
                code="EMPTY_DATASET", message="Dataset contains zero rows."
            )
        )

    return df, warnings
