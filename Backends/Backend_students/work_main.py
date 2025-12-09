from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from Backends.Shared.connection import engine
from Backends.Shared.base import Base
from Backends.Backend_students.routers import work_router

app = FastAPI(title="Student Work API")

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

app.include_router(work_router.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(500, {"message": str(exc)})

@app.get("/")
def root():
    return {"message": "Work API is live"}
