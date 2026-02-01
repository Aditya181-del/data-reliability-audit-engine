from collections import Counter


def summarize_structural_risks(structural_risks):
    if not structural_risks:
        return {
            "total_structural_risks": 0,
            "risk_type_counts": {},
            "highest_severity": "none",
        }

    risk_type_counts = Counter(r.risk_id for r in structural_risks)

    severity_rank = {"low": 1, "medium": 2, "high": 3}
    highest_severity = max(
        structural_risks,
        key=lambda r: severity_rank.get(r.severity, 0),
    ).severity

    return {
        "total_structural_risks": len(structural_risks),
        "risk_type_counts": dict(risk_type_counts),
        "highest_severity": highest_severity,
    }
