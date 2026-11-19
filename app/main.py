
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db
from .fixtures import FIXTURES
from .schemas import FeedbackCreate, ReportResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Suhail API",
    description="Arabic AI-assisted journalism verification API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/fixtures")
def get_fixtures():
    return {
        "count": len(FIXTURES),
        "fixtures": FIXTURES,
    }


@app.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, db: Session = Depends(get_db)):
    # Check test fixtures first
    for fixture in FIXTURES.values():
        if fixture["report_id"] == report_id:
            return fixture

    # Then check database
    report = db.get(models.Report, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "report_id": report.id,
        "clip_id": report.clip_id,
        "job_status": report.job_status,
        "verdict": report.verdict,
        "authenticity_score": report.authenticity_score,
        "certainty": report.certainty,
        "segments": report.segments or [],
        "modules": report.modules or {"source": None},
        "reasons": report.reasons or [],
        "recommendations": report.recommendations or [],
        "model_version": report.model_version,
        "error": report.error,
    }


@app.post("/feedback", status_code=201)
def create_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
):
    report = db.get(models.Report, payload.report_id)

    # Save a fixture report in the database if needed
    if report is None:
        fixture = next(
            (
                item
                for item in FIXTURES.values()
                if item["report_id"] == payload.report_id
            ),
            None,
        )

        if fixture is None:
            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

        clip = db.get(models.Clip, fixture["clip_id"])

        if clip is None:
            clip = models.Clip(
                id=fixture["clip_id"],
                filename=f'{fixture["clip_id"]}.mock',
            )
            db.add(clip)

        report = models.Report(
            id=fixture["report_id"],
            clip_id=fixture["clip_id"],
            job_status=fixture["job_status"],
            verdict=fixture["verdict"],
            authenticity_score=fixture["authenticity_score"],
            certainty=fixture["certainty"],
            segments=fixture["segments"],
            modules=fixture["modules"],
            reasons=fixture["reasons"],
            recommendations=fixture["recommendations"],
            model_version=fixture["model_version"],
            error=fixture["error"],
        )
        db.add(report)
        db.flush()

    feedback = models.Feedback(
        report_id=payload.report_id,
        participant_code=payload.participant_code,
        action=payload.action,
        new_verdict=payload.new_verdict,
        comment=payload.reason,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "status": "saved",
        "feedback_id": feedback.id,
        "report_id": feedback.report_id,
        "action": feedback.action,
        "new_verdict": feedback.new_verdict,
        "reason": feedback.comment,
    }
