
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Autonomous Driving Perception Stack",
    description=(
        "Computer vision pipeline for autonomous-driving "
        "experiments and simulation."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    return {
        "message": "Autonomous Driving Perception Stack API",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "perception-backend",
        "pipeline_ready": False,
    }
