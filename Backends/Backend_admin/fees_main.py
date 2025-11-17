# Backends/Backend_admin/fees_main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from Backends.Shared.connection import engine
from Backends.Shared.base import Base
from Backends.Backend_admin.routers import fees_router
from Backends.Backend_admin.routers.payment_method_router import router as payment_method_router

app = FastAPI(
    title="Admin Fees Management API",
    description="Handles fee structure creation, assignment, and exam fee automation for admin dashboard",
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
app.include_router(payment_method_router)

@app.get("/")
def root():
    return JSONResponse(
        content={"message": "Admin Fees Management API is live "},
        status_code=200
    )


