import hashlib
import json


def compute_record_hash(record: dict, previous_hash: str | None) -> str:
    """
    Compute a hash that chains audit records together.
    """

    payload = {
        "record": record,
        "previous_hash": previous_hash,
    }

    serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()
