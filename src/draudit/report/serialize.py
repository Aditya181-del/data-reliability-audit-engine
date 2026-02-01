import json
from typing import Any, Dict

from draudit.report.model import AuditReport


def audit_report_to_dict(report: AuditReport) -> Dict[str, Any]:
    """
    Convert an AuditReport into a JSON-serializable dictionary.
    """

    return {
        "audit_id": report.audit_id,
        "generated_at": report.generated_at.isoformat(),
        "dataset_snapshot": {
            "snapshot_id": report.dataset_snapshot.snapshot_id,
            "file_path": report.dataset_snapshot.file_path,
            "file_type": report.dataset_snapshot.file_type,
            "file_size_bytes": report.dataset_snapshot.file_size_bytes,
            "row_count": report.dataset_snapshot.row_count,
            "column_count": report.dataset_snapshot.column_count,
            "columns": report.dataset_snapshot.columns,
            "dtypes": report.dataset_snapshot.dtypes,
        },
        "unassessed_risks": [
            {
                "category": r.category,
                "description": r.description,
                "affected_component": r.affected_component,
            }
            for r in report.unassessed_risks
        ],
        "structural_risks": [
            {
                "risk_id": r.risk_id,
                "description": r.description,
                "affected_columns": r.affected_columns,
                "severity": r.severity.value,
                "confidence": r.confidence.value,
                "evidence": r.evidence,
            }
            for r in report.structural_risks
        ],
        "decision": report.decision.value,
        "summary": {
            "decision": report.summary.decision.value,
            "total_unassessed_risks": report.summary.total_unassessed_risks,
            "total_structural_risks": report.summary.total_structural_risks,
            "high_severity_risks": report.summary.high_severity_risks,
        },
        "notes": report.notes,
    }


def audit_report_to_json(report: AuditReport, *, indent: int = 2) -> str:
    """
    Serialize an AuditReport to a JSON string.
    """

    return json.dumps(audit_report_to_dict(report), indent=indent)
