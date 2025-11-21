# fees_main.py
from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Backends.Shared.connection import engine
from Backends.Shared.base import Base
from Backends.Backend_students.routers import fees_router
from apscheduler.schedulers.background import BackgroundScheduler
from Backends.Backend_students.routers.exam_fee_auto import auto_activate_exam_fees

scheduler = BackgroundScheduler()
scheduler.add_job(auto_activate_exam_fees, "cron", day=1)   # runs every month 1st
scheduler.start()

app = FastAPI(
    title="School Fees Management API",
    description="Handles student fee management, payments, receipts, and exam fee automation.",
    version="1.0.0"
)

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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    )
app.include_router(fees_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the School Fees Management System!"}

