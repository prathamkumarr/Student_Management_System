from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
import io
import zipfile
from decimal import Decimal, ROUND_HALF_UP

from Backends.Shared.connection import get_db
from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.schemas.result_schemas import ResultResponse
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.schemas.result_schemas import StudentForResultResponse

router = APIRouter(
    prefix="/admin/results",
    tags=["Result Generation"] 
)


# endpoint to GENERATE FINAL RESULT of a STUDENT
@router.get("/final/{student_id}")
def generate_final_result(student_id: int, db: Session = Depends(get_db)):

    results = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id
    ).all()

    if not results:
        raise HTTPException(404, "No results found for this student")

    total_marks_obtained = Decimal("0.00")
    total_max_marks = Decimal("0.00")
    exam_details = []

    for r in results:
        exam_details.append({
            "exam_id": r.exam_id,
            "obtained_marks": r.obtained_marks,
            "max_marks": r.total_marks,
            "grade": r.grade
        })

        total_marks_obtained += r.obtained_marks
        total_max_marks += r.total_marks

    if total_max_marks == 0:
        raise HTTPException(400, "Invalid total marks configuration")

    percentage = (
        (total_marks_obtained / total_max_marks) * Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    final_grade = calculate_grade(percentage)

    return {
        "student_id": student_id,
        "exam_count": len(results),
        "total_marks": total_marks_obtained,
        "max_marks": total_max_marks,
        "percentage": percentage,
        "final_grade": final_grade,
        "exam_wise_details": exam_details
    }


def calculate_grade(percentage: Decimal) -> str:
    if percentage >= Decimal("90"):
        return "A+"
    if percentage >= Decimal("80"):
        return "A"
    if percentage >= Decimal("70"):
        return "B"
    if percentage >= Decimal("60"):
        return "C"
    if percentage >= Decimal("50"):
        return "D"
    return "F"


# endpoint to download Final(yearly) result of a student
@router.get("/final/download/{student_id}")
def download_final_result(student_id: int, db: Session = Depends(get_db)):

    results = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id
    ).all()

    if not results:
        raise HTTPException(404, "No results found")

    total_marks_obtained = Decimal("0.00")
    total_max_marks = Decimal("0.00")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 760, "Final Year Result Summary")

    pdf.setFont("Helvetica", 12)
    y = 720

    pdf.drawString(50, y, f"Student ID: {student_id}")
    y -= 30

    pdf.drawString(50, y, "Exam-wise Results:")
    y -= 20

    for r in results:
        pdf.drawString(
            60,
            y,
            f"Exam {r.exam_id} → Obtained: {r.obtained_marks}/{r.total_marks}, Grade: {r.grade}"
        )
        y -= 18

        total_marks_obtained += r.obtained_marks
        total_max_marks += r.total_marks

    if total_max_marks == 0:
        raise HTTPException(400, "Invalid total marks configuration")

    percentage = (
        (total_marks_obtained / total_max_marks) * Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    final_grade = calculate_grade(percentage)

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        50,
        y,
        f"Total Marks: {total_marks_obtained}/{total_max_marks}"
    )
    y -= 25

    pdf.drawString(50, y, f"Percentage: {percentage}%")
    y -= 25

    pdf.drawString(50, y, f"Final Grade: {final_grade}")

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=student_{student_id}_final_result.pdf"
        }
    )


# endpoint to VIEW RESULT 
@router.get("/student/{student_id}/{exam_id}", response_model=ResultResponse)
def get_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    # Optional clarity: student existence
    student_exists = db.query(StudentMaster.student_id).filter(
        StudentMaster.student_id == student_id
    ).first()

    if not student_exists:
        raise HTTPException(404, "Student not found")

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not found for this student and exam"
        )

    return result


# endpoint to VIEW ALL RESULTS FOR EXAM 
@router.get("/exam/{exam_id}", response_model=list[ResultResponse])
def get_all_results(exam_id: int, db: Session = Depends(get_db)):

    exam_exists = db.query(ExamMaster.exam_id).filter(
        ExamMaster.exam_id == exam_id
    ).first()

    if not exam_exists:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    results = db.query(ResultMaster).filter(
        ResultMaster.exam_id == exam_id
    ).all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Results not generated for this exam yet"
        )

    return results


# endpoint to Download result of a student for a particular exam
@router.get("/student/{student_id}/{exam_id}/download")
def download_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    # Check student exists
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found")

    # Check exam exists
    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == exam_id
    ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    # Fetch result
    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not generated yet")

    # Generate PDF IN-MEMORY
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 760, "Student Result Sheet")

    pdf.setFont("Helvetica", 12)
    y = 720

    pdf.drawString(50, y, f"Student ID   : {student.student_id}")
    y -= 20
    pdf.drawString(50, y, f"Student Name : {student.full_name}")
    y -= 20
    pdf.drawString(50, y, f"Exam ID      : {exam.exam_id}")
    y -= 20
    pdf.drawString(50, y, f"Exam Name    : {exam.exam_name}")
    y -= 30

    pdf.drawString(50, y, f"Marks Obtained : {result.obtained_marks}")
    y -= 20
    pdf.drawString(50, y, f"Total Marks    : {result.total_marks}")
    y -= 20
    pdf.drawString(50, y, f"Percentage     : {result.percentage}%")
    y -= 20
    pdf.drawString(50, y, f"Grade          : {result.grade}")

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


# endpoint to view and download results of students of a class for a particular exam
@router.get("/download/class/{class_id}/{exam_id}")
def download_all_results(class_id: int, exam_id: int, db: Session = Depends(get_db)):

    # Check class exists
    class_obj = db.query(ClassMaster).filter(
        ClassMaster.class_id == class_id
    ).first()

    if not class_obj:
        raise HTTPException(404, "Class not found")

    # Check exam exists
    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == exam_id
    ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    # Fetch active students
    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMaster.is_active == True
    ).all()

    if not students:
        raise HTTPException(404, "No active students found for this class")

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    added_files = 0

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for student in students:
            result = db.query(ResultMaster).filter(
                ResultMaster.student_id == student.student_id,
                ResultMaster.exam_id == exam_id
            ).first()

            if not result:
                continue

            pdf_buffer = io.BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(180, 760, "Student Result Sheet")

            pdf.setFont("Helvetica", 12)
            y = 720

            pdf.drawString(50, y, f"Student ID   : {student.student_id}")
            y -= 20
            pdf.drawString(50, y, f"Student Name : {student.full_name}")
            y -= 20
            pdf.drawString(50, y, f"Class        : {class_obj.class_name}")
            y -= 20
            pdf.drawString(50, y, f"Exam         : {exam.exam_name}")
            y -= 30

            pdf.drawString(50, y, f"Marks Obtained : {result.obtained_marks}")
            y -= 20
            pdf.drawString(50, y, f"Total Marks    : {result.total_marks}")
            y -= 20
            pdf.drawString(50, y, f"Percentage     : {result.percentage}%")
            y -= 20
            pdf.drawString(50, y, f"Grade          : {result.grade}")

            pdf.save()
            pdf_buffer.seek(0)

            zip_file.writestr(
                f"{student.student_id}_exam_{exam_id}_result.pdf",
                pdf_buffer.read()
            )

            added_files += 1

    if added_files == 0:
        raise HTTPException(
            status_code=404,
            detail="Results not generated yet for this exam"
        )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": (
                f"attachment; class_{class_id}_exam_{exam_id}_results.zip"
            )
        }
    )


# endpoint to download final result of all students of a class
@router.get("/final/download/class/{class_id}")
def download_all_final_results_for_class(class_id: int, db: Session = Depends(get_db)):

    # Validate class
    class_obj = db.query(ClassMaster).filter(
        ClassMaster.class_id == class_id
    ).first()

    if not class_obj:
        raise HTTPException(404, "Class not found")

    # Fetch active students
    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMaster.is_active == True
    ).all()

    if not students:
        raise HTTPException(404, "No active students found for this class")

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for student in students:

            results = db.query(ResultMaster).filter(
                ResultMaster.student_id == student.student_id
            ).order_by(ResultMaster.exam_id.asc()).all()

            pdf_buffer = io.BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
            y = 760

            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(170, 780, "Final Year Result Summary")

            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, y, f"Student ID   : {student.student_id}")
            y -= 20
            pdf.drawString(50, y, f"Student Name : {student.full_name}")
            y -= 20
            pdf.drawString(50, y, f"Class        : {class_obj.class_name}")
            y -= 30

            if not results:
                pdf.drawString(50, y, "No results available for this student.")
                pdf.save()
                pdf_buffer.seek(0)

                zip_file.writestr(
                    f"student_{student.student_id}_final_result.pdf",
                    pdf_buffer.read()
                )
                continue

            pdf.drawString(50, y, "Exam-wise Scores:")
            y -= 20

            total_obtained = Decimal("0.00")
            total_max = Decimal("0.00")

            for r in results:
                pdf.drawString(
                    60, y,
                    f"Exam {r.exam_id}: {r.obtained_marks}/{r.total_marks}  Grade {r.grade}"
                )
                y -= 20

                total_obtained += Decimal(r.obtained_marks)
                total_max += Decimal(r.total_marks)

            percentage = (
                (total_obtained / total_max) * Decimal("100")
            ).quantize(Decimal("0.01"))

            final_grade = calculate_grade(percentage)

            y -= 30
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(50, y, f"Total Marks: {total_obtained}/{total_max}")
            y -= 25
            pdf.drawString(50, y, f"Percentage : {percentage}%")
            y -= 25
            pdf.drawString(50, y, f"Final Grade: {final_grade}")

            pdf.save()
            pdf_buffer.seek(0)

            zip_file.writestr(
                f"student_{student.student_id}_final_result.pdf",
                pdf_buffer.read()
            )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": (
                f"attachment; filename=class_{class_id}_final_results.zip"
            )
        }
    )


@router.get(
    "/students/{student_id}",
    response_model=StudentForResultResponse
)
def get_student_for_results(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(StudentMaster)
        .filter(
            StudentMaster.student_id == student_id,
            StudentMaster.is_active == True
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Active student not found"
        )

    return student
