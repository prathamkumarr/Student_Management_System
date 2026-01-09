from pydantic import BaseModel
from decimal import Decimal
from Backends.Shared.enums.result_enums import ResultStatus

class ResultGenerateRequest(BaseModel):
    student_id: int
    exam_id: int
    class Config:
        from_attributes = True

class ResultResponse(BaseModel):
    result_id: int
    student_id: int
    exam_id: int
    total_marks: Decimal
    obtained_marks: Decimal
    percentage: Decimal
    grade: str
    result_status: ResultStatus

    class Config:
        from_attributes = True

class StudentForResultResponse(BaseModel):
    student_id: int
    full_name: str
    class_id: int

    class Config:
        from_attributes = True
