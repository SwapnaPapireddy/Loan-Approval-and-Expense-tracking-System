from sqlalchemy import Column, Integer, String, Float, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

from database import Base


# ==========================================
# Loan Table
# ==========================================
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    account_number = Column(
        String(20),
        ForeignKey("bankdata.account_number"),
        nullable=False
    )

    employee_name = Column(String(100), nullable=False)

    loan_amount = Column(Float, nullable=False)
    loan_type = Column(String(100), nullable=False)

    monthly_income = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)

    date = Column(Date, default=date.today)

    status = Column(String(20), default="Pending")

    bank_data = relationship(
        "BankData",
        back_populates="loans"
    )


# ==========================================
# Bank Data Table
# ==========================================
class BankData(Base):
    __tablename__ = "bankdata"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    loans = relationship(
        "Loan",
        back_populates="bank_data",
        cascade="all, delete-orphan"
    )