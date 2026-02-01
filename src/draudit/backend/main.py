from fastapi import FastAPI, UploadFile, File, Form  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from enum import Enum

from draudit.backend.schemas.responses import AuditResponse, ErrorResponse
from draudit.pipeline.run_audit import run_audit_pipeline
from draudit.explain.ollama_client import OllamaClient
from draudit.explain.explainer import LLMExplainer

app = FastAPI(
    title="Data Reliability Audit",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 SINGLE explainer instance
ollama = OllamaClient(model="mistral")
explainer = LLMExplainer(llm_client=ollama)


def serialize_audit_report(audit):
    def _normalize(v):
        if isinstance(v, Enum):
            return v.value
        if isinstance(v, list):
            return [_normalize(i) for i in v]
        if hasattr(v, "__dict__"):
            return {k: _normalize(val) for k, val in vars(v).items()}
        return v

    return {k: _normalize(v) for k, v in vars(audit).items()}


@app.post("/audit", response_model=AuditResponse)
async def run_audit(
    dataset: UploadFile = File(...),
    metadata: UploadFile | None = File(None),
    audience: str = Form("engineer"),
):
    try:
        dataset_bytes = await dataset.read()
        metadata_bytes = await metadata.read() if metadata else None

        result = run_audit_pipeline(
            dataset_bytes=dataset_bytes,
            dataset_filename=dataset.filename,
            metadata_bytes=metadata_bytes,
            explainer=explainer,
            audience=audience,
        )

        return AuditResponse(
            decision=result.audit.decision.value,
            audit=serialize_audit_report(result.audit),
            explanation=result.explanation.__dict__,
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Audit execution failed",
                detail=str(e),
            ).dict(),
        )
