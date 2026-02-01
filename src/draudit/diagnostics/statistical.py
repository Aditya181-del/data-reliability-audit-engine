import numpy as np
import pandas as pd
from typing import List, Optional
from sklearn.metrics import mutual_info_score
from scipy.stats import ks_2samp, chi2_contingency

from draudit.diagnostics.types import (
    StructuralRisk,
    RiskSeverity,
    RiskConfidence,
)
from draudit.metadata.types import DatasetMetadata, TrustLevel


def detect_missingness_risks(
    df: pd.DataFrame,
    *,
    metadata: Optional[DatasetMetadata] = None,
) -> List[StructuralRisk]:
    """
    Detect statistical risks related to missingness and sparsity.

    Deterministic, descriptive diagnostics only.
    """

    risks: List[StructuralRisk] = []
    n_rows = len(df)

    if n_rows == 0:
        return risks

    # ---- Column-level missingness ----
    for col in df.columns:
        missing_ratio = df[col].isna().mean()

        if missing_ratio >= 0.5:
            risks.append(
                StructuralRisk(
                    risk_id="HIGH_MISSINGNESS_COLUMN",
                    description=(
                        "Column has a high proportion of missing values, "
                        "which may distort learning or require heavy imputation."
                    ),
                    affected_columns=[col],
                    severity=RiskSeverity.MEDIUM,
                    confidence=RiskConfidence.HIGH,
                    evidence=f"{missing_ratio:.2%} of values are missing.",
                )
            )

    # ---- Row-level sparsity ----
    row_missing_ratio = df.isna().mean(axis=1)
    sparse_rows_ratio = (row_missing_ratio >= 0.5).mean()

    if sparse_rows_ratio >= 0.1:
        risks.append(
            StructuralRisk(
                risk_id="SPARSE_ROWS",
                description=(
                    "A significant fraction of rows contain many missing values."
                ),
                affected_columns=None,
                severity=RiskSeverity.MEDIUM,
                confidence=RiskConfidence.HIGH,
                evidence=f"{sparse_rows_ratio:.2%} of rows have ≥50% missing values.",
            )
        )

    # ---- Missingness–target dependence (only if VERIFIED) ----
    if (
        metadata
        and metadata.target_column.trust == TrustLevel.VERIFIED
        and metadata.target_column.value in df.columns
    ):
        target = metadata.target_column.value

        for col in df.columns:
            if col == target:
                continue

            missing_mask = df[col].isna()
            if not missing_mask.any():
                continue

            rate_diff = (
                df.loc[missing_mask, target].mean()
                - df.loc[~missing_mask, target].mean()
            )

            if abs(rate_diff) >= 0.2:
                risks.append(
                    StructuralRisk(
                        risk_id="MISSINGNESS_TARGET_DEPENDENCE",
                        description=(
                            "Missingness in a feature is strongly associated "
                            "with the target, which may indicate leakage or "
                            "systematic data collection bias."
                        ),
                        affected_columns=[col],
                        severity=RiskSeverity.HIGH,
                        confidence=RiskConfidence.MEDIUM,
                        evidence=(
                            f"Target mean difference when missing vs present: "
                            f"{rate_diff:.2f}"
                        ),
                    )
                )

    return risks


def detect_target_distribution_risks(
    df: pd.DataFrame,
    *,
    metadata: DatasetMetadata,
) -> List[StructuralRisk]:
    """
    Detect risks related to target distribution and imbalance.

    Deterministic, descriptive diagnostics.
    No probabilistic inference is performed.
    """

    risks: List[StructuralRisk] = []

    # ---- Preconditions ----
    if metadata.target_column.trust == TrustLevel.MISSING:
        return risks

    target_col = metadata.target_column.value
    if target_col not in df.columns:
        return risks

    problem_type = metadata.problem_type.value
    if problem_type not in {"classification", "regression"}:
        return risks

    y = df[target_col].dropna()
    n = len(y)

    if n == 0:
        return risks

    # ---- Classification ----
    if problem_type == "classification":
        value_counts = y.value_counts(normalize=False)
        proportions = value_counts / n

        minority_prop = proportions.min()
        minority_count = value_counts.min()
        num_classes = len(value_counts)

        # Extreme imbalance
        if minority_prop < 0.05:
            confidence = (
                RiskConfidence.HIGH if minority_count >= 50 else RiskConfidence.MEDIUM
            )

            risks.append(
                StructuralRisk(
                    risk_id="EXTREME_CLASS_IMBALANCE",
                    description=(
                        "Target classes are highly imbalanced. "
                        "In multiclass settings, rare classes may lead to "
                        "unstable learning and misleading metrics."
                    ),
                    affected_columns=[target_col],
                    severity=RiskSeverity.HIGH,
                    confidence=confidence,
                    evidence=(
                        f"Minority class proportion: {minority_prop:.2%} "
                        f"({minority_count} samples, {num_classes} classes)."
                    ),
                )
            )

        # Rare-event regime
        if minority_count < 30:
            risks.append(
                StructuralRisk(
                    risk_id="RARE_EVENT_TARGET",
                    description=(
                        "Minority target class has very few samples, "
                        "making validation and generalization unreliable."
                    ),
                    affected_columns=[target_col],
                    severity=RiskSeverity.HIGH,
                    confidence=RiskConfidence.HIGH,
                    evidence=f"Minority class count: {minority_count}.",
                )
            )

    # ---- Regression ----
    elif problem_type == "regression":
        mean = y.mean()
        std = y.std()

        if std == 0:
            risks.append(
                StructuralRisk(
                    risk_id="DEGENERATE_TARGET",
                    description=(
                        "Target variable has zero variance. "
                        "Learning meaningful relationships is impossible."
                    ),
                    affected_columns=[target_col],
                    severity=RiskSeverity.HIGH,
                    confidence=RiskConfidence.HIGH,
                    evidence="Target standard deviation is 0.",
                )
            )
            return risks

        skewness = ((y - mean) ** 3).mean() / (std**3)

        if abs(skewness) > 2:
            risks.append(
                StructuralRisk(
                    risk_id="HIGHLY_SKEWED_TARGET",
                    description=(
                        "Target distribution is highly skewed, "
                        "which may destabilize learning and evaluation."
                    ),
                    affected_columns=[target_col],
                    severity=RiskSeverity.MEDIUM,
                    confidence=(
                        RiskConfidence.HIGH if n >= 100 else RiskConfidence.MEDIUM
                    ),
                    evidence=f"Estimated skewness: {skewness:.2f}.",
                )
            )

    return risks


def detect_feature_target_signal_dominance(
    df: pd.DataFrame,
    *,
    metadata: DatasetMetadata,
) -> List[StructuralRisk]:
    """
    Detect suspicious feature–target relationships that may indicate
    leakage or signal dominance.

    Deterministic, pre-ML diagnostics only.
    """

    risks: List[StructuralRisk] = []

    # ---- Preconditions ----
    if metadata.target_column.trust == TrustLevel.MISSING:
        return risks

    target_col = metadata.target_column.value
    if target_col not in df.columns:
        return risks

    problem_type = metadata.problem_type.value
    if problem_type not in {"classification", "regression"}:
        return risks

    y = df[target_col]
    n = len(y)

    if n < 50:
        return risks  # insufficient data for reliable dominance checks

    # Numeric features only (initial conservative scope)
    feature_cols = [
        c
        for c in df.columns
        if c != target_col and pd.api.types.is_numeric_dtype(df[c])
    ]

    if not feature_cols:
        return risks

    # ---- 1. Correlation dominance (linear) ----
    for col in feature_cols:
        x = df[col]

        if x.nunique() <= 1:
            continue

        corr = x.corr(y)

        if corr is not None and abs(corr) >= 0.95:
            risks.append(
                StructuralRisk(
                    risk_id="NEAR_DETERMINISTIC_CORRELATION",
                    description=(
                        "Feature has near-perfect correlation with the target. "
                        "This may indicate leakage or a post-outcome artifact."
                    ),
                    affected_columns=[col],
                    severity=RiskSeverity.HIGH,
                    confidence=(
                        RiskConfidence.HIGH if n >= 200 else RiskConfidence.MEDIUM
                    ),
                    evidence=f"Pearson correlation with target: {corr:.3f}.",
                )
            )

    # ---- 2. Mutual information dominance (non-linear) ----
    mi_scores = {}

    for col in feature_cols:
        x = df[col]

        if x.nunique() <= 1:
            continue

        try:
            mi = mutual_info_score(
                pd.qcut(x, q=10, duplicates="drop"),
                (
                    pd.qcut(y, q=10, duplicates="drop")
                    if problem_type == "regression"
                    else y
                ),
            )
            mi_scores[col] = mi
        except Exception:
            continue

    if mi_scores:
        max_mi = max(mi_scores.values())
        total_mi = sum(mi_scores.values())

        if total_mi > 0:
            dominant_col, dominant_mi = max(mi_scores.items(), key=lambda x: x[1])
            dominance_ratio = dominant_mi / total_mi

            if dominance_ratio >= 0.7:
                risks.append(
                    StructuralRisk(
                        risk_id="SINGLE_FEATURE_SIGNAL_DOMINANCE",
                        description=(
                            "A single feature accounts for most of the observed "
                            "feature–target mutual information."
                        ),
                        affected_columns=[dominant_col],
                        severity=RiskSeverity.HIGH,
                        confidence=(
                            RiskConfidence.HIGH if n >= 200 else RiskConfidence.MEDIUM
                        ),
                        evidence=(
                            f"Feature accounts for {dominance_ratio:.2%} "
                            f"of total mutual information."
                        ),
                    )
                )

    return risks


def detect_probabilistic_dependency_risks(
    df: pd.DataFrame,
    *,
    metadata: DatasetMetadata,
) -> List[StructuralRisk]:
    """
    Detect probabilistic evidence of strong feature–target dependence.

    IMPORTANT:
    - These are probabilistic signals, not deterministic proof.
    - Results must be interpreted by humans.
    """

    risks: List[StructuralRisk] = []

    # ---- Preconditions ----
    if metadata.target_column.trust != TrustLevel.DECLARED:
        return risks

    target_col = metadata.target_column.value
    if target_col not in df.columns:
        return risks

    y = df[target_col].dropna()
    n = len(y)

    if n < 50:
        return risks  # insufficient statistical power

    # -----------------------
    # Continuous features → KS test
    # -----------------------
    for col in df.columns:
        if col == target_col:
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            continue

        x = df[col].dropna()
        if x.nunique() < 10:
            continue

        try:
            stat, p_value = ks_2samp(x, y)

            if p_value < 0.001:
                confidence = RiskConfidence.HIGH if n >= 500 else RiskConfidence.MEDIUM

                risks.append(
                    StructuralRisk(
                        risk_id="PROBABILISTIC_DEPENDENCE_KS",
                        description=(
                            "Statistical test suggests strong distributional "
                            "difference between feature and target."
                        ),
                        affected_columns=[col],
                        severity=RiskSeverity.MEDIUM,
                        confidence=confidence,
                        evidence=(
                            f"KS statistic={stat:.3f}, p-value={p_value:.2e}. "
                            "This is probabilistic evidence, not proof."
                        ),
                    )
                )
        except Exception:
            continue

    # -----------------------
    # Categorical features → Chi-square
    # -----------------------
    for col in df.columns:
        if col == target_col:
            continue

        if not pd.api.types.is_object_dtype(df[col]):
            continue

        contingency = pd.crosstab(df[col], y)

        if contingency.size == 0 or contingency.shape[0] < 2:
            continue

        try:
            chi2, p_value, _, _ = chi2_contingency(contingency)

            if p_value < 0.001:
                confidence = RiskConfidence.HIGH if n >= 500 else RiskConfidence.MEDIUM

                risks.append(
                    StructuralRisk(
                        risk_id="PROBABILISTIC_DEPENDENCE_CHI2",
                        description=(
                            "Categorical feature shows strong statistical "
                            "dependence with the target."
                        ),
                        affected_columns=[col],
                        severity=RiskSeverity.MEDIUM,
                        confidence=confidence,
                        evidence=(
                            f"Chi²={chi2:.2f}, p-value={p_value:.2e}. "
                            "This is probabilistic evidence, not proof."
                        ),
                    )
                )
        except Exception:
            continue

    return risks
