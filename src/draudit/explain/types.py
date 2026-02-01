from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Zone2Explanation:
    audience: str
    summary: str
    key_findings: List[str]
    decision_rationale: str
    next_steps: List[str]
    disclaimer: str
