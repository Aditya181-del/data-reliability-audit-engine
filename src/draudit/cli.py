import sys

from draudit.ingestion.loader import load_dataset
from draudit.ingestion.schema import infer_schema
from draudit.ingestion.snapshot import create_snapshot


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m draudit.cli <path_to_dataset>")
        sys.exit(1)

    dataset_path = sys.argv[1]

    # 1. Load dataset (no mutation)
    df, warnings = load_dataset(dataset_path)

    # 2. Observe schema
    schema = infer_schema(df)

    # 3. Create deterministic snapshot
    snapshot = create_snapshot(df, dataset_path, schema)

    # 4. Human-readable output
    print("\n=== DATASET SNAPSHOT ===")
    print(f"Snapshot ID        : {snapshot.snapshot_id}")
    print(f"File Path          : {snapshot.file_path}")
    print(f"File Type          : {snapshot.file_type}")
    print(f"File Size (bytes)  : {snapshot.file_size_bytes}")
    print(f"Rows               : {snapshot.row_count}")
    print(f"Columns            : {snapshot.column_count}")

    if warnings:
        print("\n=== INGESTION WARNINGS ===")
        for w in warnings:
            print(f"[{w.code}] {w.message}")


if __name__ == "__main__":
    main()
