from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analyze, reports, health
import os

app = FastAPI(title="PyDetonator API")

allowed_origins = os.getenv(
    "PYDETONATOR_CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(reports.router)
