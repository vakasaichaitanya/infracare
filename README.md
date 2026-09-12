# InfraCare

**Smart Infrastructure Damage Reporting & Management System**

## Overview
InfraCare is a civic‑tech application that lets citizens report damaged public infrastructure (with photos and location) and enables authorities to prioritize, assign workers, and track resolution.

### Tech Stack
- **Frontend**: Flutter (mobile & web) – modern UI, animations, map integration.
- **Backend**: Python FastAPI – REST API.
- **Database**: PostgreSQL (SQL).
- **Mapping**: Google Maps (or Leaflet/OpenStreetMap) for location selection & dashboard.
- **Optimization**: Google OR‑Tools for worker‑route and priority calculation.
- **Containerisation**: Docker‑Compose for local development.

### Features
- Damage reporting with image upload and description.
- Automatic severity classification & priority calculation.
- Map dashboard visualising reports with severity colour‑coding.
- Worker assignment and route optimisation.
- Issue tracking from "Pending" → "In‑Progress" → "Resolved".

### Quick Start (Local Development)
1. **Prerequisites** – Docker Desktop, Flutter SDK, Python 3.11.
2. Clone the repo and `cd infra_care`.
3. Run `docker-compose up -d` to start PostgreSQL.
4. Activate the Python virtual environment and install deps:
   ```bash
   python -m venv venv
   . venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r backend/requirements.txt
   uvicorn backend/app/main:app --reload --host 0.0.0.0 --port 8000
   ```
5. In another terminal, launch the Flutter web app:
   ```bash
   cd frontend
   flutter run -d chrome
   ```
6. Open the web app at `http://localhost:8080` and start reporting!

### Credits Note
The project is built to stay within a single credit for later testing; no CI pipelines or external API calls that incur extra cost are enabled by default.

### License
MIT – feel free to adapt and extend.
