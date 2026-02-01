from typing import Optional, Any, Dict
from pydantic import BaseModel  # type: ignore


class AuditResponse(BaseModel):
    decision: str
    audit: Dict[str, Any]
    explanation: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: str
    detail: str
