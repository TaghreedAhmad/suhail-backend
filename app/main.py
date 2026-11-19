
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


def fixture_response(fixture):
    return {
        **fixture,
        "filename": f'{fixture["clip_id"]}.mock',
        "media_type": "unknown",
        "created_at": None,
        "is_demo": True,
    }


def database_report_response(report, db):
    clip = db.get(models.Clip, report.clip_id)

    return {
        "report_id": report.id,
        "clip_id": report.clip_id,
        "filename": clip.filename if clip else "غير معروف",
        "media_type": "unknown",
        "created_at": report.created_at,
        "is_demo": False,
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/fixtures")
def get_fixtures():
    fixtures = {
        key: fixture_response(value)
        for key, value in FIXTURES.items()
    }
    return {"count": len(fixtures), "fixtures": fixtures}


@app.get("/reports", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    demo_ids = {item["report_id"] for item in FIXTURES.values()}

    results = [
        fixture_response(item)
        for item in FIXTURES.values()
    ]

    reports = db.query(models.Report).all()

    results.extend(
        database_report_response(report, db)
        for report in reports
        if report.id not in demo_ids
    )

    return results


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    demo_ids = {item["report_id"] for item in FIXTURES.values()}
    reports = db.query(models.Report).all()

    counts = {
        "authentic": 0,
        "suspicious": 0,
        "inconclusive": 0,
        "likely_fake": 0,
    }

    total = len(FIXTURES)

    for item in FIXTURES.values():
        if item["verdict"] in counts:
            counts[item["verdict"]] += 1

    for report in reports:
        if report.id in demo_ids:
            continue
        total += 1
        if report.verdict in counts:
            counts[report.verdict] += 1

    return {
        "total": total,
        **counts,
        "weekly": [],
    }


@app.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, db: Session = Depends(get_db)):
    for fixture in FIXTURES.values():
        if fixture["report_id"] == report_id:
            return fixture_response(fixture)

    report = db.get(models.Report, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return database_report_response(report, db)


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
