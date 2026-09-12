import math
from typing import Optional
from sqlalchemy.orm import Session
from .. import models

# Haversine distance between two lat/lng points in meters
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Jaccard similarity on tokenised lower‑cased description strings
def jaccard_similarity(text1: str, text2: str) -> float:
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    if not set1 and not set2:
        return 1.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def detect_duplicate(session: Session, new_report: "models.Report") -> Optional["models.Report"]:
    """Return the most similar existing report within the configured radius.
    Uses the DUPLICATE_RADIUS_M from the db module and Jaccard threshold 0.4.
    """
    from .. import db
    radius = db.DUPLICATE_RADIUS_M
    threshold = 0.4
    candidates = (
        session.query(models.Report)
        .filter(models.Report.id != new_report.id)
        .filter(models.Report.category == new_report.category)
        .all()
    )
    best_match = None
    best_score = 0.0
    for report in candidates:
        distance = haversine(
            new_report.latitude,
            new_report.longitude,
            report.latitude,
            report.longitude,
        )
        if distance > radius:
            continue
        sim = jaccard_similarity(new_report.description, report.description)
        if sim >= threshold and sim > best_score:
            best_score = sim
            best_match = report
    return best_match
