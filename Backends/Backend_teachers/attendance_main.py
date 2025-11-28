# Backends/Backend_teachers/attendance_main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Backends.Shared.connection import engine
from Backends.Backend_teachers.routers import attendance_router
from Backends.Shared.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Teacher Attendance Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(attendance_router.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    )

@app.get("/")
def root():
    return {"message": "Teacher Attendance Management API is Live"}
