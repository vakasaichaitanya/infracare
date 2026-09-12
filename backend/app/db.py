import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env located at project root (two levels up from this file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(dotenv_path=os.path.join(project_root, ".env"))

# Core configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")

# Duplicate detection configuration
DUPLICATE_RADIUS_M = float(os.getenv("DUPLICATE_RADIUS_M", "50"))

# Map tile URLs
SATELLITE_TILE_URL = os.getenv(
    "SATELLITE_TILE_URL",
    "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
)
STANDARD_TILE_URL = os.getenv(
    "STANDARD_TILE_URL", "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
)

# SQLAlchemy engine setup
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
