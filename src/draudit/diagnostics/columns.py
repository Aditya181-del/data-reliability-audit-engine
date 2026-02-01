from typing import List

import pandas as pd

from draudit.diagnostics.types import (
    StructuralRisk,
    RiskSeverity,
    RiskConfidence,
)


def detect_column_level_risks(df: pd.DataFrame) -> List[StructuralRisk]:
    """
    Detect column-level structural risks.

    These checks are deterministic and explainable.
    They do not rely on labels or problem type.
    """

    risks: List[StructuralRisk] = []
    n_rows = len(df)

    if n_rows == 0:
        return risks

    for col in df.columns:
        series = df[col]

        # 1. Fully missing column
        if series.isna().all():
            risks.append(
                StructuralRisk(
                    risk_id="FULLY_MISSING_COLUMN",
                    description="Column contains only missing values.",
                    affected_columns=[col],
                    severity=RiskSeverity.HIGH,
                    confidence=RiskConfidence.HIGH,
                    evidence="100% values are missing.",
                )
            )
            continue

        # 2. Near-constant column (>= 99% same value)
        value_counts = series.value_counts(dropna=False)
        top_ratio = value_counts.iloc[0] / n_rows

        if top_ratio >= 0.99:
            risks.append(
                StructuralRisk(
                    risk_id="NEAR_CONSTANT_COLUMN",
                    description="Column has near-zero variance.",
                    affected_columns=[col],
                    severity=RiskSeverity.MEDIUM,
                    confidence=RiskConfidence.HIGH,
                    evidence=f"Top value accounts for {top_ratio:.2%} of rows.",
                )
            )

        # 3. High-cardinality categorical (potential ID-like)
        if series.dtype == object:
            unique_ratio = series.nunique(dropna=True) / n_rows

            if unique_ratio >= 0.9:
                risks.append(
                    StructuralRisk(
                        risk_id="HIGH_CARDINALITY_CATEGORICAL",
                        description=(
                            "Categorical column has extremely high cardinality "
                            "and may behave like an identifier."
                        ),
                        affected_columns=[col],
                        severity=RiskSeverity.MEDIUM,
                        confidence=RiskConfidence.MEDIUM,
                        evidence=(
                            f"{series.nunique(dropna=True)} unique values "
                            f"({unique_ratio:.2%} of rows)."
                        ),
                    )
                )

        # 4. Explicit ID-like pattern (name + uniqueness)
        if col.lower().endswith("id"):
            unique_ratio = series.nunique(dropna=True) / n_rows

            if unique_ratio >= 0.9:
                risks.append(
                    StructuralRisk(
                        risk_id="ID_LIKE_COLUMN",
                        description=(
                            "Column appears to be an identifier and may "
                            "cause leakage or memorization."
                        ),
                        affected_columns=[col],
                        severity=RiskSeverity.HIGH,
                        confidence=RiskConfidence.HIGH,
                        evidence=(
                            f"Column name ends with 'id' and has "
                            f"{unique_ratio:.2%} unique values."
                        ),
                    )
                )

    return risks
