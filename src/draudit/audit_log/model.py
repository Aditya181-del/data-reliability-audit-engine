from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class OverrideAction(Enum):
    PROCEED_ANYWAY = "proceed_anyway"
    FIX_LATER = "fix_later"
    ABORT_ANYWAY = "abort_anyway"


@dataclass(frozen=True)
class HumanOverride:
    """
    Human decision that explicitly overrides the system recommendation.
    """

    action: OverrideAction
    justification: str
    reviewer_id: str
    reviewed_at: datetime


@dataclass(frozen=True)
class AuditLogEntry:
    """
    Immutable audit log entry.
    """

    audit_id: str
    system_decision: str
    override: Optional[HumanOverride]
    effective_decision: str
    recorded_at: datetime
