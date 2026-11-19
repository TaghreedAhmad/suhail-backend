from typing import Any, Literal

from pydantic import BaseModel, Field


JobStatus = Literal["queued", "processing", "done", "failed"]

Verdict = Literal[
    "authentic",
    "suspicious",
    "inconclusive",
    "likely_fake",
]

Certainty = Literal["low", "medium", "high"]


class Segment(BaseModel):
    start_sec: float = Field(ge=0)
    end_sec: float = Field(ge=0)
    media_type: Literal["audio", "vision"]
    reason: str


class ReportResponse(BaseModel):
    report_id: str
    clip_id: str | None = None

    job_status: JobStatus
    verdict: Verdict | None = None

    authenticity_score: int | None = Field(
        default=None, ge=0, le=100
    )
    certainty: Certainty | None = None

    segments: list[Segment] = Field(default_factory=list)
    modules: dict[str, Any] = Field(
        default_factory=lambda: {"source": None}
    )

    reasons: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    model_version: str | None = None
    error: str | None = None


class FeedbackCreate(BaseModel):
    report_id: str
    action: Literal["accept", "edit"]
    new_verdict: Verdict | None = None
    reason: str = Field(min_length=1, max_length=2000)

    participant_code: str | None = None


class ParticipantDecisionCreate(BaseModel):
    report_id: str
    participant_code: str
    with_suhail: bool
    decision: Literal["publish", "hold"]
    time_sec: int = Field(ge=0)
    confidence: int = Field(ge=1, le=5)
    comment: str | None = None