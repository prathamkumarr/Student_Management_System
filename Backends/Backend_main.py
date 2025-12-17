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

from Backends.Backend_admin.routers.timetable_router import router as admin_timetable_router
from Backends.Backend_admin.routers.work_router import router as admin_work_router

from Backends.Backend_students.routers.timetable_router import router as student_timetable_router
from Backends.Backend_students.routers.work_router import router as student_work_router
from Backends.Backend_students.routers.activity_router import router as student_activity_router


from Backends.Backend_teachers.routers.timetable_router import router as teacher_timetable_router
from Backends.Backend_teachers.routers.work_router import router as teacher_work_router


from Backends.Backend_admin.routers.teacher_router import router as teacher_details_router
from Backends.Backend_admin.routers.classes_router import router as classes_details_router
from Backends.Backend_admin.routers.subjects_router import router as subjects_details_router
from Backends.Backend_admin.routers.students_router import router as students_details_router

from Backends.Backend_admin.routers.activity_router import router as admin_activity_router


from Backends.Backend_admin.routers.teacher_onboarding_router import router as teacher_onboarding_router
from Backends.Backend_admin.routers.staff_onboarding_router import router as staff_onboarding_router

from Backends.Backend_admin.routers.teacher_separation_router import router as teacher_separation_router
from Backends.Backend_admin.routers.teacher_transfer_router import router as teacher_transfer_router

from Backends.Backend_admin.routers.staff_separation_router import router as staff_separation_router
from Backends.Backend_admin.routers.staff_transfer_router import router as staff_transfer_router
from Backends.Backend_staff.routers.attendance_router import router as staff_attendance_router

from Backends.Backend_teachers.routers.marks_router import router as marks_router
from Backends.Backend_admin.routers.exam_router import router as admin_exam_router
from Backends.Backend_admin.routers.result_generation_router import router as result_generation_router

from Backends.Backend_students.routers.result_router import router as result_router
from Backends.Backend_admin.routers.master_router import router as master_router

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
app.include_router(teacher_onboarding_router)
app.include_router(staff_onboarding_router)
app.include_router(teacher_separation_router)
app.include_router(teacher_transfer_router)
app.include_router(staff_separation_router)
app.include_router(staff_transfer_router)
app.include_router(staff_attendance_router)
app.include_router(marks_router)
app.include_router(admin_exam_router)
app.include_router(result_generation_router)
app.include_router(result_router)
app.include_router(master_router)

app.include_router(admin_timetable_router)
app.include_router(admin_work_router)
app.include_router(admin_activity_router)

app.include_router(student_timetable_router)
app.include_router(student_work_router)
app.include_router(student_activity_router)

app.include_router(teacher_timetable_router)
app.include_router(teacher_work_router)

app.include_router(teacher_details_router)
app.include_router(classes_details_router)
app.include_router(subjects_details_router)
app.include_router(students_details_router)





@app.get("/")
def root():
    return JSONResponse(
        content={"message": "ERP-API is live "},
        status_code=200
    )