from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid
import math

from .. import db, models, utils
from ..utils import duplicate as duplicate_util
from ..utils import priority as priority_util

router = APIRouter()

# Dependency to get DB session
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/reports", response_model=List[dict])
def list_reports(db_session: Session = Depends(get_db)):
    reports = db_session.query(models.Report).order_by(models.Report.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "category": r.category.value if hasattr(r.category, "value") else str(r.category),
            "severity": r.severity.value if hasattr(r.severity, "value") else str(r.severity),
            "latitude": r.latitude,
            "longitude": r.longitude,
            "status": r.status.value if hasattr(r.status, "value") else str(r.status),
            "priority": r.priority,
            "priority_reason": r.priority_reason,
            "support_count": r.support_count or 0,
            "is_duplicate": r.is_duplicate,
            "duplicate_of_id": r.duplicate_of_id,
            "image_url": f"/uploads/{os.path.basename(r.image_path)}" if r.image_path else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in reports
    ]

# Allowed status transitions
ALLOWED_TRANSITIONS = {
    models.ReportStatus.reported: [models.ReportStatus.verified],
    models.ReportStatus.verified: [models.ReportStatus.assigned],
    models.ReportStatus.assigned: [models.ReportStatus.in_progress],
    models.ReportStatus.in_progress: [models.ReportStatus.resolved],
}

# Helper to create notification
def create_notification(db_session: Session, user_id: int, message: str):
    notif = models.Notification(user_id=user_id, message=message)
    db_session.add(notif)
    db_session.commit()

@router.post("/reports", response_model=dict)
async def create_report(
    title: str = Form(...),
    description: str = Form(...),
    category: models.ReportCategory = Form(...),
    severity: models.ReportSeverity = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    image: Optional[UploadFile] = File(None),
    db_session: Session = Depends(get_db),
):
    # Image handling
    image_path = None
    if image:
        if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Only JPEG/PNG/WebP allowed")
        contents = await image.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image exceeds 5 MB limit")
        filename = f"{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
        upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploaded_images")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        image_path = file_path

    report = models.Report(
        title=title,
        description=description,
        category=category,
        severity=severity,
        latitude=latitude,
        longitude=longitude,
        image_path=image_path,
    )
    db_session.add(report)
    db_session.flush()  # get ID for duplicate check

    # Duplicate detection
    dup = duplicate_util.detect_duplicate(db_session, report)
    if dup:
        report.is_duplicate = True
        report.duplicate_of_id = dup.id
        dup.is_duplicate = False  # ensure original flag stays false
        db_session.add(dup)

    # Compute priority
    priority_label, reason = priority_util.compute_priority(report)
    report.priority = priority_label
    report.priority_reason = reason

    db_session.commit()
    db_session.refresh(report)
    return {
        "id": report.id,
        "priority": report.priority,
        "reason": report.priority_reason,
        "is_duplicate": report.is_duplicate,
        "duplicate_of_id": report.duplicate_of_id,
        "status": report.status.value if hasattr(report.status, "value") else str(report.status),
        "image_url": f"/uploads/{os.path.basename(report.image_path)}" if report.image_path else None,
    }

@router.get("/reports/{report_id}", response_model=dict)
def get_report(report_id: int, db_session: Session = Depends(get_db)):
    report = db_session.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "title": report.title,
        "description": report.description,
        "category": report.category.value if hasattr(report.category, "value") else str(report.category),
        "severity": report.severity.value if hasattr(report.severity, "value") else str(report.severity),
        "latitude": report.latitude,
        "longitude": report.longitude,
        "status": report.status.value if hasattr(report.status, "value") else str(report.status),
        "priority": report.priority,
        "priority_reason": report.priority_reason,
        "support_count": report.support_count or 0,
        "is_duplicate": report.is_duplicate,
        "duplicate_of_id": report.duplicate_of_id,
        "image_url": f"/uploads/{os.path.basename(report.image_path)}" if report.image_path else None,
    }

@router.get("/reports/{report_id}/duplicates", response_model=List[dict])
def get_duplicates(report_id: int, db_session: Session = Depends(get_db)):
    report = db_session.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    dup = duplicate_util.detect_duplicate(db_session, report)
    if not dup:
        return []
    return [{"id": dup.id, "title": dup.title, "distance": "<50m"}]

@router.post("/reports/{report_id}/support", response_model=dict)
def support_report(report_id: int, user_id: int = Query(...), db_session: Session = Depends(get_db)):
    # Simple demo: prevent same user supporting same report multiple times via a check table is omitted.
    report = db_session.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.support_count += 1
    # Recompute priority
    priority_label, reason = priority_util.compute_priority(report)
    report.priority = priority_label
    report.priority_reason = reason
    db_session.commit()
    # Notify admin (hardcoded admin user id 1 for demo)
    create_notification(db_session, user_id=1, message=f"Report {report.id} received new support.")
    return {"support_count": report.support_count, "priority": report.priority}

@router.put("/reports/{report_id}/status", response_model=dict)
def update_status(report_id: int, new_status: models.ReportStatus = Query(...), db_session: Session = Depends(get_db)):
    report = db_session.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    allowed = ALLOWED_TRANSITIONS.get(report.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition from {report.status.value} to {new_status.value}",
        )
    # Record history
    hist = models.StatusHistory(
        report_id=report.id,
        previous_status=report.status,
        new_status=new_status,
    )
    report.status = new_status
    db_session.add(hist)
    db_session.commit()
    # Notify reporter (demo: assume reporter user id 2)
    create_notification(db_session, user_id=2, message=f"Report {report.id} status changed to {new_status.value}.")
    return {"status": report.status.value}

@router.post("/reports/{report_id}/assign", response_model=dict)
def assign_report(report_id: int, officer_id: int = Query(...), db_session: Session = Depends(get_db)):
    report = db_session.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    # Create assignment record
    assignment = models.Assignment(report_id=report.id, officer_id=officer_id)
    db_session.add(assignment)
    # Transition to Assigned if currently Verified
    if report.status == models.ReportStatus.verified:
        report.status = models.ReportStatus.assigned
        hist = models.StatusHistory(
            report_id=report.id,
            previous_status=models.ReportStatus.verified,
            new_status=models.ReportStatus.assigned,
        )
        db_session.add(hist)
    db_session.commit()
    # Notify officer
    create_notification(db_session, user_id=officer_id, message=f"You have been assigned report {report.id}.")
    return {"assigned": True, "status": report.status.value}

@router.get("/notifications", response_model=List[dict])
def get_notifications(user_id: int = Query(...), db_session: Session = Depends(get_db)):
    notifs = (
        db_session.query(models.Notification)
        .filter(models.Notification.user_id == user_id, models.Notification.read == False)
        .all()
    )
    # Mark as read
    for n in notifs:
        n.read = True
    db_session.commit()
    return [{"id": n.id, "message": n.message, "created_at": n.created_at} for n in notifs]

# Simple dashboard statistics endpoint
@router.get("/dashboard/stats", response_model=dict)
def dashboard_stats(db_session: Session = Depends(get_db)):
    total = db_session.query(models.Report).count()
    pending = db_session.query(models.Report).filter(models.Report.status != models.ReportStatus.resolved).count()
    high_priority = (
        db_session.query(models.Report)
        .filter(models.Report.priority != None)
        .order_by(models.Report.priority.desc())
        .limit(5)
        .all()
    )
    return {
        "total_reports": total,
        "pending_reports": pending,
        "top_high_priority": [{"id": r.id, "priority": r.priority} for r in high_priority],
    }

# Route optimization (simple nearest‑neighbor for demo)
@router.get("/route", response_model=dict)
def get_route(officer_id: int = Query(...), db_session: Session = Depends(get_db)):
    # Get reports assigned to officer that are not resolved
    assigned_reports = (
        db_session.query(models.Report)
        .join(models.Assignment, models.Assignment.report_id == models.Report.id)
        .filter(models.Assignment.officer_id == officer_id)
        .filter(models.Report.status != models.ReportStatus.resolved)
        .all()
    )
    if not assigned_reports:
        return {"route": [], "total_distance": 0}
    # For demo, sort by distance from first report (or 0,0 if none)
    start_lat = assigned_reports[0].latitude
    start_lng = assigned_reports[0].longitude
    def dist(r):
        return (r.latitude - start_lat) ** 2 + (r.longitude - start_lng) ** 2
    ordered = sorted(assigned_reports, key=dist)
    route = [{"id": r.id, "lat": r.latitude, "lng": r.longitude} for r in ordered]
    total_distance = sum(
        math.sqrt((ordered[i].latitude - ordered[i - 1].latitude) ** 2 + (ordered[i].longitude - ordered[i - 1].longitude) ** 2)
        for i in range(1, len(ordered))
    )
    return {"route": route, "total_distance": total_distance}
