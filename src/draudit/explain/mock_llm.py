# src/draudit/explain/mock_llm.py


class MockLLMClient:
    """
    Deterministic mock LLM for testing and CI.
    """

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return (
            "The audit indicates that the dataset should not be used as-is. "
            "Key risks relate to potential data leakage and missing temporal context. "
            "These issues may compromise model reliability if ignored."
        )
