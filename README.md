# Devops_Project - BugBoard

BugBoard is an intelligent, automated bug tracking and code analysis system.

## Module 1 (M1) - Application Foundation

The foundation of the BugBoard application has been successfully implemented and verified. It includes a modern React frontend, a FastAPI backend, and a PostgreSQL database all orchestrated via Docker Compose.

### Grading Criteria Completion Checklist:
- [x] **FastAPI backend starts and responds to `/health`**: Returns `{ "status": "healthy", "database": "connected" }`.
- [x] **Minimum 4 REST API endpoints implemented**: Covers `GET`, `POST`, `PUT`, and `DELETE` across `/api/projects`, `/api/bugs`, and `/api/bugs/{id}/analyze`.
- [x] **PostgreSQL database managed by Alembic**: Tables for `projects`, `bugs`, and `bug_analyses` created via initial migration `0001_initial_schema.py`.
- [x] **React/HTML frontend renders and makes API calls**: Uses Vite and Axios to interface with the backend.
- [x] **Responsive and usable UI**: Modern dark-themed CSS layout with dynamic modals and interactive components.

### Quickstart (Docker Compose)
To run the entire application stack:
```bash
cd bugboard
docker-compose up -d --build
```
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: PostgreSQL on port 5432

### Included Artifacts for M1
- `backend/app/` — All backend Python source files
- `backend/alembic/versions/` — Alembic migrations
- `backend/requirements.txt` — Python dependencies
- `frontend/` — React frontend source code
- `docker-compose.yml` — Stack orchestration

### Running Individually (Local Development)

If you prefer to run the components individually outside of Docker for debugging or development:

#### 1. Database
You must have the database running. You can spin up just the PostgreSQL container:
```powershell
cd bugboard
docker compose up -d postgres
```

#### 2. Backend (FastAPI)
Open a terminal and run:
```powershell
cd bugboard/backend

# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Set local database URL (since you are connecting from the host machine)
$env:DATABASE_URL="postgresql://bugboard_user:bugboard_pass@localhost:5432/bugboard_db"

# Run migrations and start the server
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### 3. Frontend (React / Vite)
Open a new, separate terminal and run:
```powershell
cd bugboard/frontend

# Install dependencies
npm install

# Set local API URL (tells Vite to proxy to localhost instead of the Docker backend)
$env:VITE_API_URL="http://localhost:8000"

# Start the development server
npm run dev
```
