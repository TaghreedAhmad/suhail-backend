
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .auth import verify_invite_code
import os
import uuid
from pathlib import Path

from fastapi import UploadFile, File

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

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_MEDIA_TYPES = {
    "image/jpeg": "image",
    "image/png": "image",
    "image/webp": "image",
    "video/mp4": "video",
    "video/webm": "video",
    "audio/mpeg": "audio",
    "audio/wav": "audio",
    "audio/ogg": "audio",
}

async def save_upload(file: UploadFile) -> tuple[str, int]:
    extension = Path(file.filename or "").suffix.lower()

    if file.content_type not in ALLOWED_MEDIA_TYPES:
        raise HTTPException(
            status_code=415,
            detail="نوع الملف غير مدعوم",
        )

    allowed_extensions = {
        "image/jpeg": {".jpg", ".jpeg"},
        "image/png": {".png"},
        "image/webp": {".webp"},
        "video/mp4": {".mp4"},
        "video/webm": {".webm"},
        "audio/mpeg": {".mp3"},
        "audio/wav": {".wav"},
        "audio/ogg": {".ogg"},
    }

    if extension not in allowed_extensions[file.content_type]:
        raise HTTPException(
            status_code=415,
            detail="امتداد الملف لا يتوافق مع نوعه",
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename
    total_size = 0

    try:
        with destination.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="حجم الملف يتجاوز الحد المسموح (100MB)",
                    )

                output.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="الملف فارغ",
            )

        return str(destination), total_size

    except Exception:
        destination.unlink(missing_ok=True)
        raise

    finally:
        await file.close()


@app.post("/upload", status_code=201)
async def upload_clip(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    invite_code: str = Depends(verify_invite_code),
):
    storage_path, file_size = await save_upload(file)

    try:
        clip = models.Clip(
            filename=Path(file.filename or "unknown").name,
            storage_path=storage_path,
            media_type=ALLOWED_MEDIA_TYPES[file.content_type],
            file_size=file_size,
        )

        db.add(clip)
        db.flush()

        report = models.Report(
            clip_id=clip.id,
            job_status="queued",
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "report_id": report.id,
            "clip_id": clip.id,
            "filename": clip.filename,
            "media_type": clip.media_type,
            "file_size": clip.file_size,
            "job_status": report.job_status,
            "is_demo": False,
        }

    except Exception:
        db.rollback()
        Path(storage_path).unlink(missing_ok=True)
        raise

def fixture_response(fixture):
    return {
        **fixture,
        "filename": f'{fixture["clip_id"]}.mock',
        "media_type": fixture.get("media_type", "unknown"),
        "created_at": None,
        "is_demo": True,
    }


def database_report_response(report, db):
    clip = db.get(models.Clip, report.clip_id)

    return {
        "report_id": report.id,
        "clip_id": report.clip_id,
        "filename": clip.filename if clip else "غير معروف",
        "media_type": clip.media_type if clip and clip.media_type else "unknown",
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
def get_fixtures(
    invite_code: str = Depends(verify_invite_code),
):
    fixtures = {
        key: fixture_response(value)
        for key, value in FIXTURES.items()
    }
    return {"count": len(fixtures), "fixtures": fixtures}


@app.get("/reports", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    invite_code: str = Depends(verify_invite_code),
):
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
def get_stats(
    db: Session = Depends(get_db),
    invite_code: str = Depends(verify_invite_code),
):
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
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    invite_code: str = Depends(verify_invite_code),
):
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
    invite_code: str = Depends(verify_invite_code),
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
