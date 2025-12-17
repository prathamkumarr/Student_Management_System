from pydantic import BaseModel

class ResultGenerateRequest(BaseModel):
    student_id: int
    exam_id: int
    class Config:
        from_attributes = True

class ResultResponse(BaseModel):
    result_id: int
    student_id: int
    exam_id: int
    total_marks: float
    obtained_marks: float
    percentage: float
    grade: str
    result_status: str

    class Config:
        from_attributes = True
