from sqlalchemy import  Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base


class SalaryMaster(Base):
    __tablename__ = "salary_master"

    salary_id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    role = mapped_column(String(100), nullable=False)
    base_salary = mapped_column(DECIMAL(10, 2), nullable=False)
    bonus_percentage = mapped_column(DECIMAL(5, 2), nullable=True)
    is_active = mapped_column(Boolean, default=True)

    # relationship
    assigned_employees = relationship("EmployeeSalary", back_populates="salary")

