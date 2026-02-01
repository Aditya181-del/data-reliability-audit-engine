import json
from pathlib import Path
from typing import Optional

from draudit.persistence.hash_chain import compute_record_hash  # type: ignore
from draudit.persistence.ruleset import (  # type: ignore
    RULESET_VERSION,
    compute_ruleset_fingerprint,
)


AUDIT_LOG_PATH = Path("audit_history.jsonl")


def append_audit_record(
    *,
    audit_payload: dict,
    previous_hash: Optional[str],
) -> str:
    """
    Append a single audit record to disk.

    Returns the hash of the written record.
    """

    audit_payload["ruleset_version"] = RULESET_VERSION
    audit_payload["ruleset_fingerprint"] = compute_ruleset_fingerprint()
    audit_payload["previous_hash"] = previous_hash

    record_hash = compute_record_hash(audit_payload, previous_hash)
    audit_payload["record_hash"] = record_hash

    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_payload, sort_keys=True))
        f.write("\n")

    return record_hash
