# Backends/Backend_admin/attendance_main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from Backends.Shared.connection import engine
from Backends.Shared.base import Base
from Backends.Backend_admin.routers.admission_router import router as admission_router

app = FastAPI(
    title="Admin Admission Management API",
    description="Handles new admissions of student.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(admission_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    )

@app.get("/")
def root():
    return {"message": "Admin Admission API is Live "}
