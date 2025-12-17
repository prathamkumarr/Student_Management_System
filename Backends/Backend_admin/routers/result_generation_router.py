from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
import io
import zipfile

from Backends.Shared.connection import get_db
from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.schemas.result_schemas import ResultResponse
from Backends.Shared.models.students_master import StudentMaster

router = APIRouter(
    prefix="/admin/results",
    tags=["Result Generation"] 
)


# endpoint to GENERATE FINAL RESULT of a STUDENT
@router.get("/final/{student_id}")
def generate_final_result(student_id: int, db: Session = Depends(get_db)):
    # Fetch all exam results for this student
    results = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id
    ).all()

    if not results:
        raise HTTPException(404, "No results found for this student")

    # Summaries
    total_marks_obtained = 0
    total_max_marks = 0
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

    percentage = round((total_marks_obtained / total_max_marks) * 100, 2)
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


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
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

    # Basic summary (same as Generate endpoint)
    total_marks_obtained = 0
    total_max_marks = 0

    # PDF buffer
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
        pdf.drawString(60, y, f"Exam {r.exam_id} → Marks: {r.total_marks}, Grade: {r.grade}")
        y -= 18

        total_marks_obtained += r.total_marks
        total_max_marks += 100  # adjust based on your logic

    percentage = round((total_marks_obtained / total_max_marks) * 100, 2)
    final_grade = calculate_grade(percentage)

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, f"Total Marks: {total_marks_obtained}/{total_max_marks}")
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
    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not found")

    return result


# endpoint to VIEW ALL RESULTS FOR EXAM 
@router.get("/exam/{exam_id}")
def get_all_results(exam_id: int, db: Session = Depends(get_db)):
    return db.query(ResultMaster).filter(
        ResultMaster.exam_id == exam_id
    ).all()


# endpoint to Download result of a student for a particular exam
@router.get("/student/{student_id}/{exam_id}/download")
def download_result(student_id: int, exam_id: int, db: Session = Depends(get_db)):

    result = db.query(ResultMaster).filter(
        ResultMaster.student_id == student_id,
        ResultMaster.exam_id == exam_id
    ).first()

    if not result:
        raise HTTPException(404, "Result not found")

    # ---- PDF FILE PATH ----
    file_path = f"result_{student_id}_{exam_id}.pdf"

    # ---- GENERATE PDF ----
    c = canvas.Canvas(file_path, pagesize=letter)
    text = c.beginText(50, 750)

    text.textLine(f"Student Result")
    text.textLine(f"-----------------------")
    text.textLine(f"Student ID : {result.student_id}")
    text.textLine(f"Exam ID    : {result.exam_id}")
    text.textLine(f"Total Marks: {result.total_marks}")
    text.textLine(f"Percentage : {result.percentage}%")
    text.textLine(f"Grade      : {result.grade}")

    c.drawText(text)
    c.save()

    # ---- RETURN FILE ----
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=file_path
    )


# endpoint to view and download results of students of a class for a particular exam
@router.get("/download/class/{class_id}/{exam_id}")
def download_all_results(class_id: int, exam_id: int, db: Session = Depends(get_db)):

    # Fetch all students of this class
    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id
    ).all()

    if not students:
        raise HTTPException(404, detail="No students found for this class")

    # In-memory ZIP file
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for student in students:
            
            # Fetch this student's result for this exam
            result = db.query(ResultMaster).filter(
                ResultMaster.student_id == student.student_id,
                ResultMaster.exam_id == exam_id
            ).first()

            if not result:
                continue  # Skip student if no result exists

            # Create a PDF in memory
            pdf_buffer = io.BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(200, 750, "Student Result Sheet")

            pdf.setFont("Helvetica", 12)
            pdf.drawString(50, 700, f"Student ID: {student.student_id}")
            pdf.drawString(50, 680, f"Student Name: {student.full_name}")
            pdf.drawString(50, 660, f"Exam ID: {exam_id}")
            pdf.drawString(50, 630, f"Total Marks: {result.total_marks}")
            pdf.drawString(50, 610, f"Grade: {result.grade}")

            pdf.save()

            # Move pointer to beginning
            pdf_buffer.seek(0)

            # Add PDF to zip
            filename = f"{student.student_id}_exam_{exam_id}_result.pdf"
            zip_file.writestr(filename, pdf_buffer.read())

    zip_buffer.seek(0)

    # Return ZIP File
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=class_{class_id}_exam_{exam_id}_results.zip"
        }
    )


# endpoint to download final result of all students of a class
@router.get("/final/download/class/{class_id}")
def download_all_final_results_for_class(class_id: int, db: Session = Depends(get_db)):

    # Fetch all students of this class
    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMaster.is_active == True
    ).all()

    if not students:
        raise HTTPException(404, "No active students found for this class")

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED)

    for student in students:
        results = db.query(ResultMaster).filter(
            ResultMaster.student_id == student.student_id
        ).all()

        if not results:
            # Put an empty PDF saying "No Results"
            pdf_buffer = io.BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(100, 750, f"Final Result - Student {student.student_id}")
            pdf.drawString(100, 720, "No results available for this student.")
            pdf.save()
            pdf_buffer.seek(0)

            zip_file.writestr(f"student_{student.student_id}_result.pdf", pdf_buffer.read())
            continue

        # Compute final result summary
        total_obtained = 0
        total_max = 0

        # New PDF for student
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
        y = 760

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(180, 780, "Final Year Result Summary")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Student ID: {student.student_id}")
        y -= 30

        pdf.drawString(50, y, "Exam-wise Scores:")
        y -= 20

        for r in results:
            pdf.drawString(60, y, f"Exam {r.exam_id}:  Marks {r.total_marks},  Grade {r.grade}")
            y -= 20

            total_obtained += r.total_marks
            total_max += 100  # Change if exam total differs

        percentage = round((total_obtained / total_max) * 100, 2)
        final_grade = calculate_grade(percentage)

        y -= 30
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, f"Total Marks: {total_obtained}/{total_max}")
        y -= 25

        pdf.drawString(50, y, f"Percentage: {percentage}%")
        y -= 25

        pdf.drawString(50, y, f"Final Grade: {final_grade}")

        pdf.save()
        pdf_buffer.seek(0)

        # Add the PDF to ZIP file
        zip_file.writestr(
            f"student_{student.student_id}_final_result.pdf",
            pdf_buffer.read()
        )

    zip_file.close()
    zip_buffer.seek(0)

    # Return ZIP as download
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename=class_{class_id}_final_results.zip"
        }
    )


@router.get("/students/{student_id}")
def get_student_for_results(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(StudentMaster)
        .filter(StudentMaster.student_id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "student_id": student.student_id,
        "full_name": student.full_name,
        "class_id": student.class_id
    }