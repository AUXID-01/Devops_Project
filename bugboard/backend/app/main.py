from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import health, projects, bugs, analysis
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="BugBoard API")

if isinstance(settings.CORS_ORIGINS, str):
    origins = settings.CORS_ORIGINS.split(",")
else:
    origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(bugs.router)
app.include_router(analysis.router)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
