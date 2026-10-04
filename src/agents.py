from __future__ import annotations

from .llm import LLMClient
from .schemas import Critique


class TranslatorAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, source_en: str) -> str:
        return self.llm.chat(
            "You are an expert English-to-Burmese medical translator. "
            "Preserve meaning, numbers, units, drug names and named entities. "
            "Return only the Burmese translation.",
            source_en,
        ).strip()


class CriticAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, source_en: str, translation_my: str) -> Critique:
        data = self.llm.chat_json(
            "You are a strict translation quality critic. Score every dimension from 0 to 1. "
            "Return JSON with adequacy, fluency, consistency, terminology, error_free, errors.",
            f"SOURCE ENGLISH:\n{source_en}\n\nBURMESE TRANSLATION:\n{translation_my}",
        )
        return Critique.model_validate(data)


class ReflectionAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, source_en: str, translation_my: str, critique: Critique) -> str:
        return self.llm.chat(
            "You revise English-to-Burmese translations. Fix only genuine errors identified "
            "by the critic while preserving correct content. Return only the revised Burmese.",
            f"SOURCE:\n{source_en}\n\nCURRENT:\n{translation_my}\n\n"
            f"CRITIQUE:\n{critique.model_dump_json(indent=2)}",
        ).strip()


class JudgeAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, source_en: str, candidates: list[str]) -> str:
        numbered = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(candidates))
        return self.llm.chat(
            "Choose the best Burmese translation for the English source. "
            "Return only the chosen Burmese translation.",
            f"SOURCE:\n{source_en}\n\nCANDIDATES:\n{numbered}",
        ).strip()
