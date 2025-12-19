from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.models.student_marks_models import StudentMarks
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(prefix="/student/result", tags=["Marks and Results"])


@router.get("/{student_id}/{exam_id}")
def get_exam_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not found")

    return {
        "student_id": result.student_id,
        "exam_id": result.exam_id,
        "total_marks": result.total_marks,
        "percentage": result.percentage,
        "grade": result.grade
    }


@router.get("/final/{student_id}")
def get_final_year_result(student_id: int, db: Session = Depends(get_db)):

    results = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id
    ).all()

    if not results:
        raise HTTPException(404, "No results found")

    exam_info = []
    total_obt = 0
    total_max = 0

    for r in results:
        exam_info.append({
            "exam_id": r.exam_id,
            "total_marks": r.total_marks,
            "grade": r.grade
        })

        total_obt += r.total_marks
        total_max += 100  # standard exam max

    percentage = round((total_obt / total_max) * 100, 2)

    # grade calculator
    def calc(percentage):
        if percentage >= 90: return "A+"
        if percentage >= 80: return "A"
        if percentage >= 70: return "B"
        if percentage >= 60: return "C"
        if percentage >= 50: return "D"
        return "F"

    return {
        "student_id": student_id,
        "exam_count": len(results),
        "total_marks": total_obt,
        "max_marks": total_max,
        "percentage": percentage,
        "final_grade": calc(percentage),
        "exam_wise_details": exam_info
    }


@router.get("/download/{student_id}/{exam_id}")
def download_exam_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not found")

    file_path = f"student_{student_id}_exam_{exam_id}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    text = c.beginText(50, 750)

    text.textLine("Student Result Sheet")
    text.textLine("-------------------------------")
    text.textLine(f"Student ID: {result.student_id}")
    text.textLine(f"Exam ID: {result.exam_id}")
    text.textLine(f"Total Marks: {result.total_marks}")
    text.textLine(f"Percentage: {result.percentage}%")
    text.textLine(f"Grade: {result.grade}")

    c.drawText(text)
    c.save()

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=file_path
    )

@router.get("/marks/{student_id}/{subject_id}")
def get_subject_wise_marks(
    student_id: int,
    subject_id: int,
    db: Session = Depends(get_db)
):
    marks = (
        db.query(StudentMarks)
        .filter(
            StudentMarks.student_id == student_id,
            StudentMarks.subject_id == subject_id
        )
        .order_by(StudentMarks.exam_id)
        .all()
    )

    if not marks:
        raise HTTPException(status_code=404, detail="No marks found")

    return [
        {
            "exam_id": m.exam_id,
            "marks_obtained": m.marks_obtained,
            "max_marks": m.max_marks
        }
        for m in marks
    ]
