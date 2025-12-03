from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from Backends.Shared.connection import engine
from Backends.Shared.base import Base
from Backends.Backend_admin.routers import fees_router
from Backends.Backend_admin.routers.payment_method_router import router as payment_method_router
from Backends.Backend_admin.routers import attendance_router
from Backends.Backend_admin.routers.admission_router import router as admission_router
from Backends.Backend_admin.routers.tc_router import router as tc_router
from Backends.Backend_students.routers.fees_router import router as fees_router_students
from Backends.Backend_students.routers.attendance_router import router as attendance_router_students
from Backends.Backend_teachers.routers.attendance_router import router as attendance_router_teachers

app = FastAPI(
    title="ERP's Backend",
    description="Admissions, Fees, Attendance Management area!",
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
app.include_router(attendance_router.router)
app.include_router(admission_router)
app.include_router(tc_router)
app.include_router(fees_router_students)
app.include_router(attendance_router_students)
app.include_router(attendance_router_teachers)

@app.get("/")
def root():
    return JSONResponse(
        content={"message": "ERP-API is live "},
        status_code=200
    )