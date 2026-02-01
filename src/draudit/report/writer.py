from draudit.ingestion.loader import load_dataset
from draudit.ingestion.schema import infer_schema
from draudit.ingestion.snapshot import create_snapshot

from draudit.metadata.loader import load_metadata
from draudit.metadata.resolution import resolve_metadata_and_unknowns

from draudit.diagnostics.structural import detect_dataset_level_risks
from draudit.diagnostics.columns import detect_column_level_risks
from draudit.diagnostics.statistical import (
    detect_missingness_risks,
    detect_target_distribution_risks,
    detect_feature_target_signal_dominance,
    detect_probabilistic_dependency_risks,
)
from draudit.metadata.defaults import build_default_metadata
from draudit.diagnostics.decision import make_audit_decision
from draudit.report.assemble import assemble_audit_report


def run_audit(*, dataset_path: str, metadata_path: str | None = None):
    """
    Canonical audit execution entry point.

    This function is deterministic and side-effect free.
    It is the ONLY place where the full audit pipeline is orchestrated.
    """

    # ---- Ingestion ----
    df, _ = load_dataset(dataset_path)
    schema = infer_schema(df)
    snapshot = create_snapshot(df, dataset_path, schema)

    # ---- Metadata ----
    # ---- Metadata ----
    metadata = (
        load_metadata(metadata_path) if metadata_path else build_default_metadata()
    )

    unassessed = resolve_metadata_and_unknowns(snapshot, metadata)

    # ---- Diagnostics ----
    structural_risks = []
    structural_risks.extend(detect_dataset_level_risks(df))
    structural_risks.extend(detect_column_level_risks(df))
    structural_risks.extend(detect_missingness_risks(df, metadata=metadata))
    structural_risks.extend(detect_target_distribution_risks(df, metadata=metadata))
    structural_risks.extend(
        detect_feature_target_signal_dominance(df, metadata=metadata)
    )
    structural_risks.extend(
        detect_probabilistic_dependency_risks(df, metadata=metadata)
    )

    # ---- Decision ----
    decision = make_audit_decision(
        unassessed_risks=unassessed,
        structural_risks=structural_risks,
    )

    # ---- Report ----
    return assemble_audit_report(
        snapshot=snapshot,
        unassessed_risks=unassessed,
        structural_risks=structural_risks,
        decision=decision,
    )
