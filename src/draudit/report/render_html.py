from typing import Dict, Any


def render_audit_report_html(report_dict: Dict[str, Any]) -> str:
    """
    Render an audit report dictionary into a standalone HTML document.
    """

    decision = report_dict["decision"].upper()
    summary = report_dict["summary"]

    def section(title: str, body: str) -> str:
        return "<section>" f"<h2>{title}</h2>" f"{body}" "</section>"

    # ---- Build Unassessed Risks HTML ----
    if report_dict["unassessed_risks"]:
        unassessed_html = ""
        for r in report_dict["unassessed_risks"]:
            unassessed_html += (
                "<div class='risk'>"
                f"<strong>{r['category']}</strong><br/>"
                f"{r['description']}"
                "</div>"
            )
    else:
        unassessed_html = "<p>No unassessed risks.</p>"

    # ---- Build Structural Risks HTML ----
    if report_dict["structural_risks"]:
        structural_html = ""
        for r in report_dict["structural_risks"]:
            affected = ", ".join(r["affected_columns"] or [])
            structural_html += (
                "<div class='risk'>"
                f"<strong class='{r['severity']}'>{r['risk_id']}</strong><br/>"
                f"{r['description']}<br/>"
                f"<em>Severity:</em> {r['severity']} | "
                f"<em>Confidence:</em> {r['confidence']}<br/>"
                f"<em>Affected columns:</em> {affected}<br/>"
                f"<em>Evidence:</em> {r['evidence']}"
                "</div>"
            )
    else:
        structural_html = "<p>No structural risks detected.</p>"

    # ---- Final HTML ----
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Data Reliability Audit Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}
        h1 {{
            border-bottom: 2px solid #333;
        }}
        h2 {{
            margin-top: 30px;
        }}
        .decision {{
            font-size: 1.2em;
            font-weight: bold;
            padding: 10px;
            background-color: #f2f2f2;
            display: inline-block;
        }}
        table {{
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 6px 10px;
            text-align: left;
        }}
        th {{
            background-color: #eee;
        }}
        .risk {{
            margin-bottom: 15px;
        }}
        .high {{
            color: darkred;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<h1>Data Reliability Audit Report</h1>

<p><strong>Audit ID:</strong> {report_dict["audit_id"]}</p>
<p><strong>Generated At:</strong> {report_dict["generated_at"]}</p>

<div class="decision">
    Final Recommendation: {decision}
</div>

{section(
    "Summary",
    f"<ul>"
    f"<li>Total unassessed risks: {summary['total_unassessed_risks']}</li>"
    f"<li>Total structural risks: {summary['total_structural_risks']}</li>"
    f"<li>High severity risks: {summary['high_severity_risks']}</li>"
    f"</ul>"
)}

{section(
    "Dataset Snapshot",
    f"<table>"
    f"<tr><th>File Path</th><td>{report_dict['dataset_snapshot']['file_path']}</td></tr>"
    f"<tr><th>Rows</th><td>{report_dict['dataset_snapshot']['row_count']}</td></tr>"
    f"<tr><th>Columns</th><td>{report_dict['dataset_snapshot']['column_count']}</td></tr>"
    f"<tr><th>File Size (bytes)</th><td>{report_dict['dataset_snapshot']['file_size_bytes']}</td></tr>"
    f"</table>"
)}

{section("Unassessed (Epistemic) Risks", unassessed_html)}
{section("Structural Risks", structural_html)}

</body>
</html>
"""

    return html
