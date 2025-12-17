from sqlalchemy import Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base


class EmployeeSalary(Base):
    __tablename__ = "employee_salary"

    employee_salary_id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    employee_type = mapped_column(String(10), nullable=False)   # 'teacher' or 'staff'
    employee_id = mapped_column(Integer, nullable=False)        # will map to teacher_id or staff_id (NOT FK here)
    salary_id = mapped_column(Integer, ForeignKey("salary_master.salary_id"), nullable=False)
    effective_from = mapped_column(Date, nullable=False)
    effective_to = mapped_column(Date, nullable=True)
    is_active = mapped_column(Boolean, default=True)

    # relationship 
    salary = relationship("SalaryMaster", back_populates="assigned_employees")
