from pydantic import BaseModel
from pydantic import model_validator

class StudentMarksCreate(BaseModel):
    student_id: int
    subject_id: int
    exam_id: int
    marks_obtained: float
    max_marks: float
    remarks: str | None = None
    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def validate_marks(self):
        if self.marks_obtained > self.max_marks:
            raise ValueError("marks_obtained cannot exceed max_marks")
        return self


class StudentMarksResponse(StudentMarksCreate):
    mark_id: int
    is_pass: bool | None

    class Config:
        from_attributes = True

