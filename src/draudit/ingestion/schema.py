from typing import Dict

import pandas as pd


def infer_schema(df: pd.DataFrame) -> Dict[str, str]:
    """
    Observe the dataset schema exactly as loaded.

    This function:
    - Records column names
    - Records pandas-inferred dtypes
    - Makes NO assumptions about correctness

    This function MUST NOT:
    - Cast types
    - Normalize names
    - Parse dates
    - Validate against expectations
    """

    return {column: str(dtype) for column, dtype in df.dtypes.items()}
