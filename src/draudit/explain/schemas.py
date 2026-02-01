from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ExplanationRequest:
    audit_json: dict
    audience: str
    mode: str = "overview"


@dataclass(frozen=True)
class ExplanationResponse:
    """
    Non-authoritative, human-readable explanation of an audit.
    """

    headline: Optional[str]
    summary: str
    key_insights: List[str]
    limitations: Optional[str]
    disclaimer: str
