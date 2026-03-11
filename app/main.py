import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import Employee, Attendance  # noqa: F401 – ensure models are registered
from app.routes import employees_router, attendance_router, dashboard_router

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="Human Resource Management System – Employee & Attendance tracking",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(employees_router)
app.include_router(attendance_router)
app.include_router(dashboard_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "version": "2.0.0"}
