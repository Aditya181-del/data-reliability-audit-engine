'''
# src/draudit/pipeline/run_audit.py

import tempfile
from pathlib import Path
from typing import Optional

from draudit.pipeline.schemas import AuditWithExplanation
from draudit.report.writer import run_audit
from draudit.explain.explainer import LLMExplainer
from draudit.explain.schemas import ExplanationRequest
from draudit.explain.risk_summary import summarize_structural_risks


def run_audit_pipeline(
    *,
    dataset_bytes: bytes,
    dataset_filename: str,
    metadata_bytes: Optional[bytes] = None,
    explainer: Optional[LLMExplainer] = None,
    audience: str = "engineer",
) -> AuditWithExplanation:
    """
    Adapter-safe audit runner.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        dataset_path = tmpdir / dataset_filename
        dataset_path.write_bytes(dataset_bytes)

        metadata_path = None
        if metadata_bytes:
            metadata_path = tmpdir / "metadata.yaml"
            metadata_path.write_bytes(metadata_bytes)

        # ---------------------------
        # Run authoritative audit
        # ---------------------------
        audit_result = run_audit(
            dataset_path=str(dataset_path),
            metadata_path=str(metadata_path) if metadata_path else None,
        )

        # ---------------------------
        # Non-authoritative explanation
        # ---------------------------
        audit_dict = audit_result.to_dict()

        audit_dict["structural_risk_summary"] = summarize_structural_risks(
            audit_result.structural_risks
        )

        # Optional: prevent raw explosion
        audit_dict.pop("structural_risks", None)

        explanation = explainer.explain(
            ExplanationRequest(
                audit_json=audit_dict,
                audience=audience,
                mode="overview",
            )
        )

        # ---------------------------
        # HARD GUARANTEE: never return None
        # ---------------------------
        result = AuditWithExplanation(
            audit=audit_result,
            explanation=explanation,
        )

        if result.audit is None:
            raise RuntimeError("Audit pipeline returned no audit result")

        return result
'''

# src/draudit/pipeline/run_audit.py

import tempfile
from pathlib import Path
from typing import Optional

from draudit.pipeline.schemas import AuditWithExplanation
from draudit.report.writer import run_audit
from draudit.explain.explainer import LLMExplainer
from draudit.explain.schemas import ExplanationRequest
from draudit.explain.risk_summary import summarize_structural_risks


def run_audit_pipeline(
    *,
    dataset_bytes: bytes,
    dataset_filename: str,
    metadata_bytes: Optional[bytes] = None,
    explainer: Optional[LLMExplainer] = None,
    audience: str = "engineer",
) -> AuditWithExplanation:
    """
    Adapter-safe audit runner.

    Enhancements applied:
    1. Structural risk summarization (prevents LLM overload)
    2. Dataset-size-aware explanation mode (fast for large datasets)
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # ---------------------------
        # Persist uploaded files
        # ---------------------------
        dataset_path = tmpdir / dataset_filename
        dataset_path.write_bytes(dataset_bytes)

        metadata_path = None
        if metadata_bytes:
            metadata_path = tmpdir / "metadata.yaml"
            metadata_path.write_bytes(metadata_bytes)

        # ---------------------------
        # Run authoritative audit
        # ---------------------------
        audit_result = run_audit(
            dataset_path=str(dataset_path),
            metadata_path=str(metadata_path) if metadata_path else None,
        )

        # ---------------------------
        # Prepare explanation input
        # ---------------------------
        audit_dict = audit_result.to_dict()

        # Enhancement 1: summarize structural risks
        audit_dict["structural_risk_summary"] = summarize_structural_risks(
            audit_result.structural_risks
        )

        # Prevent raw explosion in LLM context
        audit_dict.pop("structural_risks", None)

        # Enhancement 2: dataset-scale-aware mode
        row_count = audit_result.dataset_snapshot.row_count
        mode = "high_level" if row_count > 50_000 else "overview"

        # ---------------------------
        # Non-authoritative explanation
        # ---------------------------
        explanation = None
        if explainer:
            explanation = explainer.explain(
                ExplanationRequest(
                    audit_json=audit_dict,
                    audience=audience,
                    mode=mode,
                )
            )

        # ---------------------------
        # HARD GUARANTEE: audit must exist
        # ---------------------------
        result = AuditWithExplanation(
            audit=audit_result,
            explanation=explanation,
        )

        if result.audit is None:
            raise RuntimeError("Audit pipeline returned no audit result")

        return result
