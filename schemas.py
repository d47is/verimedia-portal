from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


MediaKind = Literal["image", "audio", "video", "unknown"]
RiskLevel = Literal["low", "medium", "high"]


class Signal(BaseModel):
    name: str
    score: float = Field(ge=0, le=1, description="0 = authentic-leaning, 1 = synthetic-leaning")
    detail: str


class Provenance(BaseModel):
    first_seen: str
    watermark: str
    credibility: str
    source_url: str | None = None
    c2pa_present: bool = False
    exif_summary: dict[str, Any] = Field(default_factory=dict)
    perceptual_hash: str | None = None
    notes: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    job_id: str
    mode: str
    filename: str
    media_type: MediaKind
    synthetic_probability: int = Field(ge=0, le=100)
    risk: RiskLevel
    label: str
    visual_title: str
    evidence: list[str]
    explanation: str
    signals: list[Signal]
    provenance: Provenance
    preview_data_url: str | None = None
    heatmap_data_url: str | None = None
    disclaimer: str = (
        "This is a decision-support assessment, not legal proof. "
        "Combine it with human review, original-source checks, and on-the-record confirmation."
    )
