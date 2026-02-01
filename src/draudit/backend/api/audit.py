# src/draudit/pipeline/run_audit.py

import tempfile
from pathlib import Path
from typing import Optional

from draudit.pipeline.schemas import AuditWithExplanation
from draudit.report.writer import run_audit  # type: ignore
from draudit.explain.explainer import LLMExplainer


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

    Converts uploaded files → temporary files
    so the core audit pipeline remains unchanged.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        dataset_path = tmpdir / dataset_filename
        dataset_path.write_bytes(dataset_bytes)

        metadata_path = None
        if metadata_bytes:
            metadata_path = tmpdir / "metadata.yaml"
            metadata_path.write_bytes(metadata_bytes)

        # --- Run the real audit ---
        audit_result = run_audit(
            dataset_path=str(dataset_path),
            metadata_path=str(metadata_path) if metadata_path else None,
        )

        explanation = None
        if explainer:
            explanation = explainer.explain(
                audit_result.to_explanation_request(audience=audience)
            )

        return AuditWithExplanation(
            audit=audit_result,
            explanation=explanation,
        )
