# src/draudit/explain/explainer.py

from draudit.explain.schemas import ExplanationResponse
from draudit.explain.prompts import SYSTEM_PROMPT, build_user_prompt


class LLMExplainer:
    """
    Non-authoritative explanation generator.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def explain(self, request):
        fallback = ExplanationResponse(
            headline="Audit completed with unresolved risks",
            summary=(
                "The audit completed successfully, but an AI-generated explanation "
                "could not be produced. Please review the detected risks directly."
            ),
            key_insights=[],
            limitations="Explanation engine unavailable.",
            disclaimer="This explanation is AI-generated and non-authoritative.",
        )

        if not self.llm or not self.llm.is_available():
            print("⚠️ Ollama not available — using fallback")
            return fallback

        try:
            print("🔥 Calling Ollama LLM")

            text = self.llm.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_user_prompt(
                    audit_json=request.audit_json,
                    audience=request.audience,
                    mode=request.mode,
                ),
            )

            if not text or len(text.strip()) < 40:
                return fallback

            return ExplanationResponse(
                headline="Audit explanation summary",
                summary=text.strip(),
                key_insights=[],
                limitations=(
                    "This explanation summarizes audit outputs only and does not "
                    "replace review of the full audit report."
                ),
                disclaimer=(
                    "This explanation is AI-generated and non-authoritative. "
                    "The audit report remains the sole source of truth."
                ),
            )

        except Exception as e:
            print("❌ LLM explanation failed:", e)
            return fallback
