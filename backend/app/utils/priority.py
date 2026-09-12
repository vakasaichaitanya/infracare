from typing import Tuple
from .. import db
from .. import models

# Weight constants (approved defaults)
SEVERITY_WEIGHT = 4
SUPPORT_WEIGHT = 2
DUPLICATE_WEIGHT = 1
SAFETY_WEIGHT = 3  # placeholder, not used currently

CATEGORY_WEIGHTS = {
    models.ReportCategory.road: 3,
    models.ReportCategory.bridge: 4,
    models.ReportCategory.lighting: 2,
    models.ReportCategory.other: 1,
}

# Map severity enum to numeric value
SEVERITY_VALUES = {
    models.ReportSeverity.low: 1,
    models.ReportSeverity.medium: 2,
    models.ReportSeverity.high: 3,
    models.ReportSeverity.critical: 4,
}

def compute_priority(report: "models.Report") -> Tuple[str, str]:
    """Calculate priority string and human‑readable reason.

    Returns a tuple ``(priority_label, reason)`` where ``priority_label`` is a
    simple string (numeric score) and ``reason`` explains the contribution of
    each factor.
    """
    # Basic factors
    severity_score = SEVERITY_VALUES.get(report.severity, 0) * SEVERITY_WEIGHT
    support_score = (report.support_count or 0) * SUPPORT_WEIGHT
    duplicate_score = (len(report.duplicates) or 0) * DUPLICATE_WEIGHT
    # Safety impact placeholder – not present in model; treat as 0
    safety_score = 0 * SAFETY_WEIGHT
    category_score = CATEGORY_WEIGHTS.get(report.category, 1)

    total = (
        severity_score
        + support_score
        + duplicate_score
        + safety_score
        + category_score
    )

    # Map total score to priority tier (P1 Critical -> P4 Low)
    if total >= 16:
        priority_label = "P1"
    elif total >= 12:
        priority_label = "P2"
    elif total >= 8:
        priority_label = "P3"
    else:
        priority_label = "P4"

    reason_parts = [
        f"Score {total} [Tier {priority_label}]",
        f"severity({report.severity.value})*{SEVERITY_WEIGHT}={severity_score}",
        f"support({report.support_count})*{SUPPORT_WEIGHT}={support_score}",
        f"duplicates({len(report.duplicates)})*{DUPLICATE_WEIGHT}={duplicate_score}",
        f"category({report.category.value})={category_score}",
    ]
    reason = ", ".join(reason_parts)
    return priority_label, reason
