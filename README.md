# Session 21 — DevOps Final Capstone: BugBoard (Python)

## 1. What we are building

BugBoard is an intelligent, automated bug tracking and code analysis SaaS application:

- React + Vite frontend
- Responsive HTML/JSX + CSS UI
- FastAPI Python backend
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- REST APIs
- Pytest automated tests
- Docker containers
- GitHub Actions CI/CD
- Trivy container security scanning *(Pending)*
- GitHub Container Registry
- Docker Hub Registry
- Terraform for AWS infrastructure *(Pending)*
- AWS VPC + EKS *(Pending)*
- Kubernetes *(Pending)*
- Helm *(Pending)*
- Ingress *(Pending)*
- HPA *(Pending)*
- Prometheus + Grafana *(Pending)*
- Health/readiness endpoints
- Troubleshooting exercises *(Pending)*

The point is to show how a real application travels from a developer laptop to a monitored Kubernetes environment.

```text
Developer
   |
   v
Git / GitHub
   |
   v
GitHub Actions
   |-- pytest
   |-- frontend build
   |-- Docker build
   |-- Trivy scan
   `-- push images to GHCR
              |
              v
        Terraform
              |
       AWS VPC + EKS
              |
              v
            Helm
              |
      +-------+--------+
      |                |
   Frontend          Backend
    React            FastAPI
      |                |
      +-------> PostgreSQL
              |
       Prometheus
              |
           Grafana
```

---

## 2. Repository structure

```text
bugboard/
├── frontend/                 # React application and CSS
├── backend/                  # FastAPI application
│   ├── app/                  # API, models, schemas, DB config
│   ├── tests/                # Pytest tests
│   └── alembic/              # DB migrations
├── docker-compose.yml        # Full local stack
├── terraform/                # AWS VPC + EKS infrastructure (To be built)
├── helm/bugboard/            # Kubernetes package (To be built)
├── k8s/                      # namespace/bootstrap manifests (To be built)
├── monitoring/               # Prometheus/Grafana values (To be built)
├── troubleshooting/          # deliberately broken manifests (To be built)
└── .github/workflows/        # CI/CD (To be built)
```

---

# PART A — UNDERSTAND THE APPLICATION

## 3. Frontend

The frontend is an intelligent code analysis dashboard. 

It contains:
- modern dark-mode aesthetic
- interactive project upload area
- dynamic task/bug table
- automated code analysis modal
- status filters
- priority badges
- responsive CSS
- loading and backend-error states

The browser calls `/api/projects`, `/api/projects/{id}/bugs`, `/api/bugs/{id}`, and `/api/bugs/{id}/analyze`.

The browser does **not** need to know the internal backend hostname. Nginx and Kubernetes Ingress handle routing.

## 4. Backend

FastAPI exposes:

```text
GET    /health

GET    /api/projects
POST   /api/projects
GET    /api/projects/{id}
DELETE /api/projects/{id}

GET    /api/projects/{id}/bugs
POST   /api/projects/{id}/bugs

GET    /api/bugs/{id}
PUT    /api/bugs/{id}
DELETE /api/bugs/{id}

POST   /api/bugs/{id}/analyze
GET    /api/bugs/{id}/analysis
```

Swagger documentation is available at `/docs` when the backend is running.

### Why `/health`?

A container can be alive while its application is unhealthy. `/health` gives Kubernetes a cheap liveness check.

---

# PART B — RUN IT LOCALLY

## 5. Fastest method: Docker Compose

Requirements:

- Docker Desktop / Docker Engine
- Docker Compose

Run:

```bash
cd bugboard
docker compose up -d --build
```

Open:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000/docs
http://localhost:8000/health
```

Stop:

```bash
docker compose down
```

Delete database volume too:

```bash
docker compose down -v
```

---

## 6. Run components individually

Requirements:

- Python 3.11+
- Node.js
- PostgreSQL (Via Docker)

**1. Spin up Database:**
```powershell
cd bugboard
docker compose up -d postgres
```

**2. Start FastAPI Backend:**
```powershell
cd bugboard/backend
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt

# Set local database URL
$env:DATABASE_URL="postgresql://bugboard_user:bugboard_pass@localhost:5432/bugboard_db"

alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**3. Start React Frontend:**
```powershell
cd bugboard/frontend
npm install

# Point proxy to local backend
$env:VITE_API_URL="http://localhost:8000"

npm run dev
```

---

# PART C — TESTING

## 7. Pytest

```powershell
cd bugboard/backend
pytest --cov=app --cov-report=term-missing
flake8 app
```

Tests happen **before Docker images are pushed**.

```text
Bad code
  ↓
pytest fails
  ↓
Pipeline stops
  ↓
No broken image is promoted
```

This is the first quality gate. We have implemented Test Hardening utilizing a dynamically created SQLite in-memory database to prevent test pollution in our core database.

---

# PART D — GIT AND GITHUB

## 8. Git Management

Git version control ensures immutable checkpoints and remote collaboration. We are tracking this project on GitHub.

*(Note: We have successfully added `.gitignore` and `.dockerignore` filters for optimal push management).*

---

# PART E — DOCKER

## 9. Backend Dockerfile

The backend image:
1. starts from Python 3.11-slim
2. installs dependencies
3. copies Alembic and Application Code
4. exposes port 8000
5. runs migrations and Uvicorn at startup

## 10. Frontend Dockerfile

The frontend uses a multi-stage build:

```text
Node
  ↓
npm build
  ↓
static dist/
  ↓
Nginx runtime image
```

This keeps build tooling out of the final runtime image.

---

# PART F — CI/CD

## 11. GitHub Actions pipeline

The workflow has three conceptual stages:

```text
TEST
 ↓
BUILD + PUSH
 ↓
DEPLOY (Pending)
```

### Test job (`test-backend`)
- Runs Pytest quality gate. Aborts the pipeline if tests fail.

### Build/Push job (`build-and-push-images`)
- Builds the optimized frontend and backend images.
- Pushes to **GitHub Container Registry (GHCR)** and **Docker Hub**.
- Tags images immutably with the Git commit SHA.

---

*(Sections G through O: Trivy, Terraform, Kubernetes, Helm, Ingress, HPA, Prometheus, and Troubleshooting are pending development).*
