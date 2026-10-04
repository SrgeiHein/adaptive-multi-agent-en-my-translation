from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class TranslationExample(BaseModel):
    id: str
    source_en: str
    reference_my: Optional[str] = None
    domain: str = "medical"


class Critique(BaseModel):
    adequacy: float = Field(ge=0.0, le=1.0)
    fluency: float = Field(ge=0.0, le=1.0)
    consistency: float = Field(ge=0.0, le=1.0)
    terminology: float = Field(ge=0.0, le=1.0)
    error_free: float = Field(ge=0.0, le=1.0)
    errors: List[str] = Field(default_factory=list)


class IterationRecord(BaseModel):
    iteration: int
    translation: str
    critique: Critique
    confidence: float
    reflected: bool = False


class TranslationResult(BaseModel):
    id: str
    source_en: str
    reference_my: Optional[str] = None
    final_translation: str
    scenario: Literal["S1", "S2", "S3", "S4", "S5"]
    iterations: List[IterationRecord] = Field(default_factory=list)
