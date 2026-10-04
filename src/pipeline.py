from __future__ import annotations

from .agents import TranslatorAgent, CriticAgent, ReflectionAgent, JudgeAgent
from .config import settings
from .llm import LLMClient
from .schemas import Critique, IterationRecord, TranslationExample, TranslationResult


WEIGHTS = {
    "adequacy": 0.35,
    "fluency": 0.20,
    "consistency": 0.25,
    "terminology": 0.10,
    "error_free": 0.10,
}


def confidence_score(c: Critique) -> float:
    score = sum(getattr(c, name) * weight for name, weight in WEIGHTS.items())
    return max(0.0, min(1.0, round(score, 4)))


class AdaptiveTranslationPipeline:
    def __init__(self):
        llm = LLMClient()
        self.translator = TranslatorAgent(llm)
        self.critic = CriticAgent(llm)
        self.reflector = ReflectionAgent(llm)
        self.judge = JudgeAgent(llm)

    def run(self, ex: TranslationExample, scenario: str = "S4") -> TranslationResult:
        if scenario not in {"S1", "S2", "S3", "S4", "S5"}:
            raise ValueError("scenario must be one of S1,S2,S3,S4,S5")

        current = self.translator.run(ex.source_en)
        candidates = [current]
        records: list[IterationRecord] = []

        if scenario == "S1":
            return TranslationResult(
                id=ex.id,
                source_en=ex.source_en,
                reference_my=ex.reference_my,
                final_translation=current,
                scenario=scenario,
            )

        critique = self.critic.run(ex.source_en, current)
        conf = confidence_score(critique)
        records.append(
            IterationRecord(
                iteration=0,
                translation=current,
                critique=critique,
                confidence=conf,
                reflected=False,
            )
        )

        if scenario == "S2":
            final = current

        elif scenario == "S3":
            for i in range(settings.max_reflections):
                current = self.reflector.run(ex.source_en, current, critique)
                candidates.append(current)
                critique = self.critic.run(ex.source_en, current)
                conf = confidence_score(critique)
                records.append(
                    IterationRecord(
                        iteration=i + 1,
                        translation=current,
                        critique=critique,
                        confidence=conf,
                        reflected=True,
                    )
                )
            final = current

        else:
            for i in range(settings.max_reflections):
                if conf >= settings.confidence_threshold:
                    break
                current = self.reflector.run(ex.source_en, current, critique)
                candidates.append(current)
                critique = self.critic.run(ex.source_en, current)
                conf = confidence_score(critique)
                records.append(
                    IterationRecord(
                        iteration=i + 1,
                        translation=current,
                        critique=critique,
                        confidence=conf,
                        reflected=True,
                    )
                )

            final = (
                self.judge.run(ex.source_en, candidates)
                if scenario == "S5" and len(candidates) > 1
                else current
            )

        return TranslationResult(
            id=ex.id,
            source_en=ex.source_en,
            reference_my=ex.reference_my,
            final_translation=final,
            scenario=scenario,
            iterations=records,
        )
