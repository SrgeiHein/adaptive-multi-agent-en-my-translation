from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("LLM_PROVIDER", "openai_compatible")
    api_base: str = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
    api_key: str = os.getenv("LLM_API_KEY", "")
    model: str = os.getenv("LLM_MODEL", "")
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.80"))
    max_reflections: int = int(os.getenv("MAX_REFLECTIONS", "2"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))


settings = Settings()
