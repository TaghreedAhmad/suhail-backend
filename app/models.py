import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def new_id() -> str:
    return str(uuid.uuid4())


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Clip(Base):
    __tablename__ = "clips"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    filename: Mapped[str] = mapped_column(String)
    claim: Mapped[str | None] = mapped_column(Text, nullable=True)
    # الجواب المعروف مسبقاً للمقاطع التجريبية: real | fake | out_of_context
    ground_truth: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    clip_id: Mapped[str] = mapped_column(ForeignKey("clips.id"))
    # queued | processing | done | failed
    job_status: Mapped[str] = mapped_column(String, default="queued")
    # authentic | suspicious | inconclusive | likely_fake
    verdict: Mapped[str | None] = mapped_column(String, nullable=True)
    authenticity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # low | medium | high
    certainty: Mapped[str | None] = mapped_column(String, nullable=True)
    segments: Mapped[list] = mapped_column(JSON, default=list)
    modules: Mapped[dict] = mapped_column(JSON, default=dict)
    reasons: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    model_version: Mapped[str | None] = mapped_column(String, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    report_id: Mapped[str] = mapped_column(ForeignKey("reports.id"))
    # رمز المشارك (مثل P1) وليس اسمه
    participant_code: Mapped[str | None] = mapped_column(String, nullable=True)
    with_suhail: Mapped[bool] = mapped_column(Boolean, default=True)
    # publish | hold
    decision: Mapped[str | None] = mapped_column(String, nullable=True)
    time_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)  # من 1 إلى 5
    # accept | edit
    action: Mapped[str | None] = mapped_column(String, nullable=True)
    new_verdict: Mapped[str | None] = mapped_column(String, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)