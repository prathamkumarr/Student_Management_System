from pydantic import BaseModel

class StudentMarksCreate(BaseModel):
    student_id: int
    subject_id: int
    exam_id: int
    marks_obtained: float
    max_marks: float
    remarks: str | None = None
    class Config:
        from_attributes = True


class StudentMarksResponse(StudentMarksCreate):
    mark_id: int
    is_pass: bool | None

    class Config:
        from_attributes = True

