from typing import List

import pandas as pd

from draudit.diagnostics.types import (
    StructuralRisk,
    RiskSeverity,
    RiskConfidence,
)


def detect_dataset_level_risks(df: pd.DataFrame) -> List[StructuralRisk]:
    """
    Detect dataset-level structural risks.

    These checks are deterministic and model-agnostic.
    They do not inspect semantics or distributions.
    """

    risks: List[StructuralRisk] = []

    # 1. Empty dataset
    if df.shape[0] == 0:
        risks.append(
            StructuralRisk(
                risk_id="EMPTY_DATASET",
                description="Dataset contains zero rows.",
                affected_columns=None,
                severity=RiskSeverity.HIGH,
                confidence=RiskConfidence.HIGH,
                evidence="Row count is 0.",
            )
        )
        return risks  # No further checks make sense

    # 2. Duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        ratio = duplicate_count / len(df)
        risks.append(
            StructuralRisk(
                risk_id="DUPLICATE_ROWS",
                description="Dataset contains duplicate rows.",
                affected_columns=None,
                severity=RiskSeverity.MEDIUM,
                confidence=RiskConfidence.HIGH,
                evidence=(
                    f"{duplicate_count} duplicate rows " f"({ratio:.2%} of dataset)."
                ),
            )
        )

    # 3. Zero-variance columns
    constant_columns = [col for col in df.columns if df[col].nunique(dropna=False) == 1]

    if constant_columns:
        risks.append(
            StructuralRisk(
                risk_id="CONSTANT_COLUMNS",
                description="One or more columns have zero variance.",
                affected_columns=constant_columns,
                severity=RiskSeverity.MEDIUM,
                confidence=RiskConfidence.HIGH,
                evidence=(
                    f"{len(constant_columns)} columns have a single unique value."
                ),
            )
        )

    return risks
