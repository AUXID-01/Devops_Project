# 🐞 BugBoard — DevOps Bug Tracking & Static Code Analysis Platform

> **Demo_Video**
[Drive_Link](https://drive.google.com/drive/folders/1vHt7K9VRzrrRtSBW2B7hOA_pMUuuvtRN?usp=drive_link)

> **Scaler DevOps Capstone Project | Final Submission (100 / 100 Points)**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=githubactions&logoColor=white)
![Trivy](https://img.shields.io/badge/Trivy-Security_Gate-1904DA?logo=aquasecurity&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-AWS_IaC-844FBA?logo=terraform&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-Charts-0F1689?logo=helm&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white)

**Repository:** [https://github.com/AUXID-01/Devops_Project](https://github.com/AUXID-01/Devops_Project)

---

## 1. Executive Summary

BugBoard is an intelligent, automated bug tracking and static code analysis SaaS platform designed to demonstrate a complete, production-grade DevOps lifecycle. Engineers upload a project archive (`.zip`), inspect the extracted source code structure (file counts, Python module breakdown, test coverage metrics), create bug tickets tied to specific source files and line numbers, and trigger deterministic root-cause analysis that generates structured evidence and remediation suggestions.

The platform is built with a **React 18 + Vite** frontend delivering a modern dark-mode dashboard, a **FastAPI** backend exposing a comprehensive REST API with automated code intelligence, and a **PostgreSQL 16** database managed through **Alembic** migrations. The entire stack is containerized with **Docker**, continuously tested and deployed through **GitHub Actions**, security-scanned by **Trivy**, infrastructure-provisioned via **Terraform**, orchestrated on **Kubernetes** with **Helm**, and monitored in real-time using **Prometheus** and **Grafana**.

This repository represents the end-to-end journey of a real application — from a developer's laptop to a fully monitored, high-availability Kubernetes environment.

---

## 2. End-to-End Architecture

```text
  Developer Push
       |
       v
  +-----------------------+
  |   GitHub Actions CI   |
  |                       |
  |  1. Pytest            |
  |  2. Frontend Build    |
  |  3. Docker Build      |
  |  4. Trivy Scan Gate   |
  |  5. Push to Registry  |
  +-----------+-----------+
              |
     +--------+--------+
     |                  |
   GHCR           Docker Hub
  (ghcr.io)       (docker.io)
     |                  |
     +--------+---------+
              |
              v
  +-----------------------+
  |   Terraform AWS IaC   |
  |                       |
  |  VPC (Multi-AZ)       |
  |  Public + Private     |
  |  Subnets              |
  |  Internet + NAT GW    |
  |  EKS Cluster          |
  +-----------+-----------+
              |
              v
  +-----------------------+
  |   Helm Chart Deploy   |
  |                       |
  |  bugboard namespace   |
  |  2x Frontend Replicas |
  |  2x Backend Replicas  |
  |  PostgreSQL + PVC     |
  |  NGINX Ingress        |
  |   / -> Frontend       |
  |   /api -> Backend     |
  +-----------+-----------+
              |
              v
  +-----------------------+
  |   Observability       |
  |                       |
  |  Prometheus (Pull)    |
  |  /metrics every 15s   |
  |         |             |
  |      Grafana          |
  |  HTTP Rate | P95 Lat  |
  |  5xx Error Rate       |
  +-----------------------+
```

---

## 3. Module Documentation Index (100 / 100 Points)

| Module | Title | Points | Status | Documentation |
| :---: | :--- | :---: | :---: | :--- |
| M1 | Application (Frontend + Backend + Database) | 10 / 10 | ✅ | [docs/M1.md](docs/M1.md) |
| M2 | Testing (Pytest + Code Quality) | 10 / 10 | ✅ | [docs/M2.md](docs/M2.md) |
| M3 | Git & GitHub | 5 / 5 | ✅ | [docs/M3.md](docs/M3.md) |
| M4 | Docker (Dockerfile + Compose) | 10 / 10 | ✅ | [docs/M4.md](docs/M4.md) |
| M5 | CI/CD Pipeline (GitHub Actions) | 15 / 15 | ✅ | [docs/M5.md](docs/M5.md) |
| M6 | DevSecOps (Trivy Security Scanning) | 5 / 5 | ✅ | [docs/M6.md](docs/M6.md) |
| M7 | Terraform (AWS Infrastructure as Code) | 15 / 15 | ✅ | [docs/M7.md](docs/M7.md) |
| M8 | Kubernetes + Helm (Declarative Orchestration) | 15 / 15 | ✅ | [docs/M8.md](docs/M8.md) |
| M9 | Observability (Prometheus + Grafana) | 10 / 10 | ✅ | [docs/M9.md](docs/M9.md) |
| M10 | Final Documentation & Presentation | 5 / 5 | ✅ | [README.md](README.md) |

---

## 4. Repository Structure

```text
Devops_Final_Project/
├── bugboard/
│   ├── frontend/                 # React 18 + Vite application
│   │   ├── src/                  # Components, pages, CSS
│   │   ├── Dockerfile            # Multi-stage: Node build -> Nginx unprivileged
│   │   └── package.json
│   ├── backend/                  # FastAPI Python application
│   │   ├── app/                  # Routes, models, schemas, config, analyzer
│   │   ├── alembic/              # Database migration scripts
│   │   ├── alembic.ini           # Migration configuration
│   │   ├── tests/                # Pytest test suite
│   │   ├── Dockerfile            # Python 3.11-slim, non-root user
│   │   └── requirements.txt
│   └── docker-compose.yml        # Full local development stack
├── terraform/                    # AWS VPC + EKS infrastructure
│   ├── main.tf                   # Provider + backend configuration
│   ├── vpc.tf                    # VPC, subnets, gateways, route tables
│   ├── eks.tf                    # EKS cluster + managed node group
│   ├── variables.tf              # Parameterized inputs
│   ├── outputs.tf                # Cluster endpoint, VPC ID exports
│   └── terraform.tfvars.example  # Safe credential template (no secrets)
├── helm/bugboard/                # Complete Helm chart
│   ├── Chart.yaml                # Chart metadata
│   ├── values.yaml               # Configurable deployment values
│   └── templates/                # K8s manifests (deployments, services, ingress)
├── k8s/
│   └── namespace.yaml            # Namespace isolation manifest
├── monitoring/
│   ├── prometheus-values.yaml    # Prometheus Helm overrides
│   ├── grafana-values.yaml       # Grafana Helm overrides + datasource
│   └── bugboard-dashboard.json   # Pre-built Grafana dashboard (3 panels)
├── .github/workflows/
│   └── ci.yml                    # Complete CI/CD pipeline
├── .trivyignore                  # CVE risk-acceptance register
├── .gitignore                    # Repository exclusion filters
├── docs/                         # Module documentation + evidence screenshots
└── README.md                     # This file (M10)
```

---

## 5. Quickstart: Running Locally

### Prerequisites

- Docker Desktop / Docker Engine
- Docker Compose

### Start the Full Stack

```bash
git clone https://github.com/AUXID-01/Devops_Project.git
cd Devops_Project/bugboard
docker compose up -d --build
```

### Verify

| Service | URL |
| :--- | :--- |
| Frontend (React Dashboard) | [http://localhost:3000](http://localhost:3000) |
| Backend (Swagger Docs) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Health Check | [http://localhost:8000/health](http://localhost:8000/health) |

### Teardown

```bash
# Stop all containers
docker compose down

# Stop and delete database volume
docker compose down -v
```

### Run Components Individually

**1. Database:**
```powershell
cd bugboard
docker compose up -d postgres
```

**2. Backend:**
```powershell
cd bugboard/backend
cp .env.example .env          # Copy the environment template
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**3. Frontend:**
```powershell
cd bugboard/frontend
npm install
$env:VITE_API_URL="http://localhost:8000"
npm run dev
```

---

## 6. API & Health Specification

```text
GET    /health                          # Liveness probe (DB connectivity check)
GET    /metrics                         # Prometheus-formatted telemetry

GET    /api/projects                    # List all projects
POST   /api/projects                    # Upload .zip archive + create project
GET    /api/projects/{id}               # Get project details
DELETE /api/projects/{id}               # Delete project and artifacts

GET    /api/projects/{id}/bugs          # List bugs for a project
POST   /api/projects/{id}/bugs          # Create a new bug ticket

GET    /api/bugs/{id}                   # Get bug details
PUT    /api/bugs/{id}                   # Update bug (status, priority, etc.)
DELETE /api/bugs/{id}                   # Delete bug

POST   /api/bugs/{id}/analyze           # Trigger deterministic code analysis
GET    /api/bugs/{id}/analysis          # Retrieve analysis results
```

Swagger documentation is available at `/docs` when the backend is running.

### Why `/health`?

A container can be alive while its application is unhealthy. The `/health` endpoint provides Kubernetes a cheap liveness check that verifies database connectivity, enabling automatic pod restarts when the application enters a degraded state.

---

## 7. DevOps Engineering Highlights

### 7.1 Quality Gate — Pytest

Tests execute **before** Docker images are built, acting as the first quality gate in the CI pipeline. If any test fails, the pipeline halts immediately and no broken image is ever promoted to the registry.

- **Isolated Test Engine:** A dynamically created SQLite in-memory database prevents test pollution in the production PostgreSQL instance.
- **Coverage Reporting:** `pytest --cov=app --cov-report=term-missing` provides line-level visibility into untested code paths.
- **Linting:** `flake8` enforces PEP 8 code style standards.

```text
Bad code → pytest fails → Pipeline stops → No broken image is promoted
```

### 7.2 Containerization — Docker

Both services follow container security best practices:

- **Backend (`python:3.11-slim`):** Creates a dedicated non-root `bugboard` user. All application files are owned by this user. No shell access is granted to root at runtime.
- **Frontend (Multi-stage Build):** Stage 1 compiles React with Node 20. Stage 2 serves static assets via `nginxinc/nginx-unprivileged:alpine`, keeping build tooling completely out of the final runtime image.
- **Compose:** Orchestrates PostgreSQL (with health checks), backend (with migration auto-run), and frontend in a single command.

### 7.3 CI/CD Automation — GitHub Actions

The pipeline (`ci.yml`) triggers on every push to `main` with three jobs:

| Job | Purpose |
| :--- | :--- |
| `test-backend` | Runs Pytest quality gate. Aborts pipeline on failure. |
| `build-frontend` | Validates React build compiles cleanly. |
| `build-and-push-images` | Builds Docker images → Trivy security scan → Dual push to GHCR and Docker Hub. |

Images are tagged immutably with the Git commit SHA (`ghcr.io/auxid-01/devops_project/backend:<sha>`) alongside the rolling `latest` tag.

### 7.4 DevSecOps — Trivy Security Scanning

Trivy is embedded directly into the CI/CD pipeline as an automated security gate:

- Images are built locally first (`load: true`) and scanned before any registry push.
- Scans filter for `HIGH` and `CRITICAL` severity vulnerabilities with `exit-code: 1`.
- Unfixed upstream CVEs are tracked in `.trivyignore` as an explicit risk-acceptance register.
- Both backend (Debian-based) and frontend (Alpine-based) images are independently scanned.

### 7.5 Infrastructure as Code — Terraform

The complete AWS cloud infrastructure is defined declaratively using HashiCorp Terraform:

| Resource | Configuration |
| :--- | :--- |
| **VPC** | `10.0.0.0/16` CIDR with DNS hostnames and support enabled |
| **Public Subnets** | Multi-AZ (`us-east-1a`, `us-east-1b`) for Ingress controllers |
| **Private Subnets** | Multi-AZ for managed EKS workloads |
| **Internet Gateway** | Public internet access for load balancers |
| **NAT Gateway** | Private subnet egress for pulling container images |
| **EKS Cluster** | Managed Kubernetes control plane |
| **Node Group** | `t3.medium` instances, auto-scaling 1–3 nodes |

The infrastructure is strictly modularized into `main.tf`, `vpc.tf`, `eks.tf`, `variables.tf`, and `outputs.tf`. A `terraform.tfvars.example` template enforces a zero-secret-in-repo policy.

### 7.6 Orchestration — Kubernetes & Helm

The application workloads are fully declarative and orchestrated via Kubernetes, packaged into a Helm chart (`helm/bugboard/`):

- **Namespace (`bugboard`):** Strict resource boundary isolation.
- **Deployments:** High-availability sets with 2 replicas each for frontend and backend.
- **Services:** `ClusterIP` internal load balancing for stable pod-to-pod communication.
- **Ingress:** NGINX ingress controller routing `/` to the frontend and `/api` to the backend.
- **Secrets:** Database credentials managed via Kubernetes Secret objects.
- **PVC:** Persistent Volume Claim for PostgreSQL data durability.
- **Health Probes:** Liveness and readiness probes on the `/health` endpoint ensure automatic recovery.

All static Kubernetes object structures are separated from dynamic configuration values (`values.yaml`), enabling environment-specific overrides without modifying templates.

### 7.7 Observability — Prometheus & Grafana

The cluster is fully instrumented for deep operational visibility:

- **Instrumentation:** `prometheus-fastapi-instrumentator` automatically captures HTTP traffic metrics on the `/metrics` endpoint.
- **Prometheus:** Scrapes backend pods every 15 seconds using `prometheus.io/scrape` annotations. 24-hour retention with resource-capped server deployment.
- **Grafana:** Pre-configured datasource pointing to Prometheus. Ships with a custom dashboard (`bugboard-dashboard.json`) containing 3 panels:

| Panel | PromQL Query |
| :--- | :--- |
| Total HTTP Requests Rate | `sum(rate(http_requests_total[1m])) by (handler, status)` |
| P95 Request Latency | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))` |
| Application Error Rate (5xx) | `sum(rate(http_requests_total{status=~"5.."}[1m]))` |

---

## 8. Evaluator Demo Runbook

A concise 4-step walkthrough to verify the complete DevOps lifecycle:

### Step 1 — Launch the Stack

**Option A: Docker Compose (Fastest)**
```bash
cd bugboard
docker compose up -d --build
```

**Option B: Kubernetes via Helm**
```bash
kubectl apply -f k8s/namespace.yaml
helm upgrade --install bugboard ./helm/bugboard -n bugboard
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8000:80
```

### Step 2 — Explore the Application

1. Open [http://localhost:3000](http://localhost:3000) (Docker Compose) or [http://localhost](http://localhost) (Kubernetes).
2. Upload `examples/sample-project.zip` (included in the repository) and observe the extracted file analysis.
3. Navigate to the project and view the file breakdown (total files, Python files, test files).

### Step 3 — Create and Analyze a Bug

1. Click **"Create Bug"** on any project.
2. Fill in the bug title, assign it to a specific file (e.g., `app/users.py`) at a specific line number (e.g., line 18).
3. Click **"Run Automated Code Analysis"** and inspect the deterministic evidence and remediation suggestions generated by the analysis engine.

### Step 4 — Verify the CI/CD Pipeline

1. Make a small code change (e.g., update a comment in `bugboard/backend/app/main.py`).
2. Commit and push to `main`:
   ```bash
   git add .
   git commit -m "test: verify CI/CD pipeline execution"
   git push origin main
   ```
3. Navigate to the **Actions** tab on GitHub and observe the green pipeline run.
4. Verify the newly published image tag on the **Packages** page (GHCR).

---

## 9. Testing

```powershell
cd bugboard/backend
pytest --cov=app --cov-report=term-missing -v
flake8 app
```

Tests are executed in an isolated SQLite in-memory database to prevent pollution of the production PostgreSQL instance.

---

## 10. License

This project is developed as part of the Scaler DevOps curriculum. All rights reserved.
