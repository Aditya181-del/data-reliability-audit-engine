from datetime import datetime
from typing import Optional

from draudit.audit_log.model import AuditLogEntry, HumanOverride  # type: ignore


def record_audit_log_entry(
    *,
    audit_id: str,
    system_decision: str,
    override: Optional[HumanOverride],
) -> AuditLogEntry:
    """
    Create an immutable audit log entry.

    No validation.
    No inference.
    No modification of system output.
    """

    effective_decision = override.action.value if override else system_decision

    return AuditLogEntry(
        audit_id=audit_id,
        system_decision=system_decision,
        override=override,
        effective_decision=effective_decision,
        recorded_at=datetime.utcnow(),
    )
