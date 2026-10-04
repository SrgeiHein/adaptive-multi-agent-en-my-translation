from __future__ import annotations

import json
import httpx
from .config import settings


class LLMClient:
    """Minimal OpenAI-compatible chat client."""

    def __init__(self):
        if not settings.api_key:
            raise RuntimeError("LLM_API_KEY is not set")
        if not settings.model:
            raise RuntimeError("LLM_MODEL is not set")

    def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        payload = {
            "model": settings.model,
            "temperature": settings.temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {settings.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=120) as client:
            response = client.post(
                f"{settings.api_base.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def chat_json(self, system: str, user: str) -> dict:
        return json.loads(self.chat(system, user, json_mode=True))
