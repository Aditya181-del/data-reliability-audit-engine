from draudit.audit_log.model import AuditLogEntry  # type: ignore


def resolve_effective_decision(entry: AuditLogEntry) -> str:
    """
    Resolve the final decision applied in practice.

    System decision always remains visible.
    """

    return entry.effective_decision
