from pydantic import BaseModel, Field
from pydantic import model_validator
from typing import List

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


class StudentMarksBulkItem(BaseModel):
    student_id: int
    marks_obtained: float
    class Config:
        from_attributes = True


class StudentMarksBulkCreate(BaseModel):
    class_id: int
    subject_id: int
    exam_id: int
    max_marks: float
    marks: List[StudentMarksBulkItem]
    remarks: str | None = None
    class Config:
        from_attributes = True


class StudentMarksUpdate(BaseModel):
    marks_obtained: float = Field(..., ge=0)
    max_marks: float = Field(..., gt=0)
    remarks: str | None = None
    class Config:
        from_attributes = True
