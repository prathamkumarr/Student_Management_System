from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.models.student_marks_models import StudentMarks
from Backends.Shared.models.students_master import StudentMaster

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

    results = (
        db.query(ResultMaster)
        .filter(
            ResultMaster.student_id == student_id,
            ResultMaster.is_active == True
        )
        .all()
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No results found"
        )

    exam_info = []
    total_obtained = 0.0
    total_max = 0.0

    for r in results:
        exam_info.append({
            "exam_id": r.exam_id,
            "obtained_marks": float(r.obtained_marks),
            "total_marks": float(r.total_marks),
            "percentage": float(r.percentage),
            "grade": r.grade,
            "status": r.result_status.value
        })

        total_obtained += float(r.obtained_marks)
        total_max += float(r.total_marks)

    overall_percentage = (
        round((total_obtained / total_max) * 100, 2)
        if total_max > 0 else 0.0
    )

    # ---- FINAL GRADE CALCULATION ----
    def calc_grade(p):
        if p >= 90: return "A+"
        if p >= 80: return "A"
        if p >= 70: return "B"
        if p >= 60: return "C"
        if p >= 50: return "D"
        return "F"

    return {
        "student_id": student_id,
        "exam_count": len(results),
        "total_obtained_marks": round(total_obtained, 2),
        "total_max_marks": round(total_max, 2),
        "overall_percentage": overall_percentage,
        "final_grade": calc_grade(overall_percentage),
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


@router.get("/exam/{student_id}/{exam_id}")
def get_exam_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id
    ).first()
    if not student:
        raise HTTPException(404, "Student not found")

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not found")

    marks = db.query(StudentMarks).filter(
        StudentMarks.student_id == student_id,
        StudentMarks.exam_id == exam_id
    ).all()

    return {
        "student_id": student_id,
        "exam_id": exam_id,
        "total_marks": result.total_marks,
        "percentage": result.percentage,
        "grade": result.grade,
        "subject_wise_marks": [
            {
                "subject_id": m.subject_id,
                "marks_obtained": m.marks_obtained,
                "max_marks": m.max_marks,
                "is_pass": m.is_pass
            } for m in marks
        ]
    }
