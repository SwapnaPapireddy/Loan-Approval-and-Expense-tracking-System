from pydantic import BaseModel
from datetime import date
from typing import Optional


# ==========================================
# LOGIN SCHEMA
# ==========================================
class LoginSchema(BaseModel):
    employee_name: str
    account_number: str


# ==========================================
# EMPLOYEE SCHEMA
# ==========================================
class EmployeeCreate(BaseModel):
    employee_name: str
    account_number: str
    monthly_income: float
    credit_score: int


class EmployeeResponse(BaseModel):
    id: int
    employee_name: str
    account_number: str
    monthly_income: float
    credit_score: int

    class Config:
        from_attributes = True


# ==========================================
# BANK DATA SCHEMA  (maps to bank_data table)
# ==========================================
class BankDataCreate(BaseModel):
    name: str
    account_number: str
    amount: float


class BankDataResponse(BaseModel):
    id: int
    name: str
    account_number: str
    amount: float

    class Config:
        from_attributes = True


# ==========================================
# LOAN APPLY SCHEMA
# ==========================================
class LoanCreate(BaseModel):
    account_number: str
    employee_name: str
    loan_amount: float
    loan_type: str
    monthly_income: float
    credit_score: int
    date: date


# ==========================================
# LOAN UPDATE SCHEMA
# ==========================================
class LoanUpdate(BaseModel):
    loan_amount: Optional[float] = None
    loan_type: Optional[str] = None
    monthly_income: Optional[float] = None
    credit_score: Optional[int] = None
    date: Optional[date] = None
    status: Optional[str] = None


# ==========================================
# MANAGER APPROVE / REJECT SCHEMA
# ==========================================
class LoanStatusUpdate(BaseModel):
    status: str


# ==========================================
# LOAN RESPONSE SCHEMA
# ==========================================
class LoanResponse(BaseModel):
    id: int
    account_number: str
    employee_name: str
    loan_amount: float
    loan_type: str
    monthly_income: float
    credit_score: int
    date: date
    status: str

    class Config:
        from_attributes = True