from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .db import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    officer = "officer"
    citizen = "citizen"
    demo = "demo"

class ReportStatus(str, enum.Enum):
    reported = "Reported"
    verified = "Verified"
    assigned = "Assigned"
    in_progress = "In_Progress"
    resolved = "Resolved"

class ReportSeverity(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"

class ReportCategory(str, enum.Enum):
    road = "Road"
    bridge = "Bridge"
    lighting = "Lighting"
    other = "Other"

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ReportCategory), nullable=False)
    severity = Column(Enum(ReportSeverity), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(Enum(ReportStatus), default=ReportStatus.reported, nullable=False)
    priority = Column(String, nullable=True)
    priority_reason = Column(String, nullable=True)
    support_count = Column(Integer, default=0)
    duplicate_of_id = Column(Integer, ForeignKey("reports.id"), nullable=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = relationship("Report", remote_side=[id], backref="duplicates")
    assignments = relationship("Assignment", back_populates="report")
    status_history = relationship("StatusHistory", back_populates="report")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    report = relationship("Report", back_populates="assignments")
    officer = relationship("User", back_populates="assignments")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # plaintext for demo only
    role = Column(Enum(UserRole), nullable=False)
    assignments = relationship("Assignment", back_populates="officer")

class StatusHistory(Base):
    __tablename__ = "status_history"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    previous_status = Column(Enum(ReportStatus), nullable=False)
    new_status = Column(Enum(ReportStatus), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)
    report = relationship("Report", back_populates="status_history")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
