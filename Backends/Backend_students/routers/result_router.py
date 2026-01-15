from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.models.student_marks_models import StudentMarks
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.academic_session import AcademicSession
from Backends.Shared.dependencies.session_context import get_current_session

router = APIRouter(
    prefix="/student/result", tags=["Marks and Results"],
    dependencies=[Depends(get_current_session)]
)

@router.get("/{student_id}/{exam_id}")
def get_exam_result(
    student_id: int,
    exam_id: int,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id,
        ResultMaster.academic_session_id == session.session_id
    ).first()

    if not result:
        raise HTTPException(
            404,
            "Result not found for this exam in current academic session"
        )

    return {
        "student_id": result.student_id,
        "exam_id": result.exam_id,
        "total_marks": result.total_marks,
        "percentage": result.percentage,
        "grade": result.grade
    }

@router.get("/download/{student_id}/{exam_id}")
def download_exam_result(
    student_id: int,
    exam_id: int,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id,
        ResultMaster.academic_session_id == session.session_id,
        ResultMaster.is_active == True
    ).first()

    if not result:
        raise HTTPException(404, "Result not found for current academic session")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(160, 760, "Student Result Sheet")

    pdf.setFont("Helvetica", 12)
    y = 720

    pdf.drawString(50, y, f"Student ID      : {student.student_id}")
    y -= 20
    pdf.drawString(50, y, f"Student Name    : {student.full_name}")
    y -= 20
    pdf.drawString(50, y, f"Exam ID         : {result.exam_id}")
    y -= 20
    pdf.drawString(50, y, f"Academic Session: {session.session_name}")
    y -= 30

    pdf.drawString(50, y, f"Marks Obtained  : {result.obtained_marks}")
    y -= 20
    pdf.drawString(50, y, f"Total Marks     : {result.total_marks}")
    y -= 20
    pdf.drawString(50, y, f"Percentage      : {result.percentage}%")
    y -= 20
    pdf.drawString(50, y, f"Grade           : {result.grade}")

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f"attachment; "
                f"filename=student_{student_id}_exam_{exam_id}_result.pdf"
            )
        }
    )

# ----------------------------------------------
@router.get("/marks/{student_id}/{subject_id}")
def get_subject_wise_marks(
    student_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    marks = (
        db.query(StudentMarks)
        .filter(
            StudentMarks.student_id == student_id,
            StudentMarks.subject_id == subject_id,
            StudentMarks.academic_session_id == session.session_id
        )
        .order_by(StudentMarks.exam_id.asc())
        .all()
    )

    if not marks:
        raise HTTPException(
            status_code=404,
            detail="No marks found for this subject in current academic session"
        )

    return [
        {
            "exam_id": m.exam_id,
            "marks_obtained": m.marks_obtained,
            "max_marks": m.max_marks
        }
        for m in marks
    ]


@router.get("/exam/{student_id}/{exam_id}")
def get_exam_result(
    student_id: int,
    exam_id: int,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id,
        ResultMaster.academic_session_id == session.session_id,
        ResultMaster.is_active == True
    ).first()

    if not result:
        raise HTTPException(
            404,
            "Result not found for this exam in current academic session"
        )

    marks = db.query(StudentMarks).filter(
        StudentMarks.student_id == student_id,
        StudentMarks.exam_id == exam_id,
        StudentMarks.academic_session_id == session.session_id
    ).all()

    return {
        "student_id": student_id,
        "exam_id": exam_id,
        "academic_session": session.session_name,
        "total_marks": result.total_marks,
        "percentage": result.percentage,
        "grade": result.grade,
        "subject_wise_marks": [
            {
                "subject_id": m.subject_id,
                "marks_obtained": m.marks_obtained,
                "max_marks": m.max_marks,
                "is_pass": m.is_pass
            }
            for m in marks
        ]
    }
