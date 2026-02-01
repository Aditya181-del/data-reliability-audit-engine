import hashlib
import inspect

from draudit.diagnostics import decision


RULESET_VERSION = "v1.0.0"


def compute_ruleset_fingerprint() -> str:
    """
    Compute a deterministic fingerprint of the decision logic.
    """

    source = inspect.getsource(decision.make_audit_decision)
    return hashlib.sha256(source.encode("utf-8")).hexdigest()
