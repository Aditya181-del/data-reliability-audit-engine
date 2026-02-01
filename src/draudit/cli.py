import sys
from typing import Optional

from draudit.pipeline import run_audit_pipeline


def main(argv: Optional[list[str]] = None) -> None:
    """
    CLI entrypoint for Data Reliability Audit.

    This is a thin wrapper around the authoritative
    engine pipeline function.
    """
    args = argv if argv is not None else sys.argv[1:]

    if len(args) != 1:
        print("Usage: python -m draudit.cli <path_to_dataset>")
        sys.exit(1)

    dataset_path = args[0]

    # Delegate to the engine-owned pipeline
    report = run_audit_pipeline(dataset_path)

    # Human-readable CLI output (temporary)
    # This will later be aligned with the HTML/JSON report
    print("\n=== DATA RELIABILITY AUDIT COMPLETED ===")
    print(f"Decision : {report.decision}")
    print(f"Snapshot : {report.snapshot.snapshot_id}")
    print(f"Risks    : {len(report.risks)}")


if __name__ == "__main__":
    main()
