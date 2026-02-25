from fastapi import FastAPI
from routes import analyze, reports, health

app = FastAPI(title="PyDetonator API")

app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(reports.router)