import requests
import json


class OllamaClient:
    """
    Minimal, reliable Ollama client for local explanations.
    """

    def __init__(self, model: str = "mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def is_available(self) -> bool:
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"{system_prompt}\n\n{user_prompt}"

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                # 🔽 critical: cap generation
                "options": {
                    "temperature": 0.2,
                    "num_predict": 200,
                },
            },
            # 🔽 critical: give CPU models time
            timeout=180,
        )

        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()
