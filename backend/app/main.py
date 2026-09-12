from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
from . import db
from .routers import reports

app = FastAPI(title="InfraCare API", version="1.0.0")

# Open CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup():
    db.init_db()

# API routes
app.include_router(reports.router, prefix="/api")

# Root → /app
@app.get("/")
def root():
    return RedirectResponse(url="/app")

# Serve uploaded images at /uploads
_upload_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "uploaded_images")
)
os.makedirs(_upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=_upload_dir), name="uploads")

# Serve frontend at /app
_frontend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
)
if os.path.isdir(_frontend_dir):
    app.mount("/app", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
