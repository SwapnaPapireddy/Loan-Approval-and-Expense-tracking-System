from sqlalchemy.orm import Session
import models
import schemas


# ==========================================
# LOGIN (via BankData table)
# ==========================================
def login(db: Session, name: str, account_number: str):

    record = (
        db.query(models.BankData)
        .filter(models.BankData.name == name)
        .first()
    )

    if not record:
        return {"error": "Record not found"}

    if account_number != record.account_number:
        return {"error": "Invalid Account Number"}

    return record


# ==========================================
# CREATE BANK DATA RECORD
# ==========================================
def create_bank_data(db: Session, data: schemas.BankDataCreate):

    existing_record = (
        db.query(models.BankData)
        .filter(models.BankData.account_number == data.account_number)
        .first()
    )

    if existing_record:
        return {"error": "Account Number already exists"}

    new_record = models.BankData(
        name=data.name,
        account_number=data.account_number,
        amount=data.amount
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# ==========================================
# APPLY LOAN
# ==========================================
def apply_loan(db: Session, loan: schemas.LoanCreate):

    record = (
        db.query(models.BankData)
        .filter(models.BankData.name == loan.employee_name)
        .first()
    )

    if not record:
        return {"error": "Record not found"}

    if loan.account_number != record.account_number:
        return {"error": "Invalid Account Number"}

    new_loan = models.Loan(
        employee_name=loan.employee_name,
        account_number=loan.account_number,
        loan_amount=loan.loan_amount,
        loan_type=loan.loan_type,
        monthly_income=loan.monthly_income,
        credit_score=loan.credit_score,
        date=loan.date,
        status="Pending"
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan


# ==========================================
# VIEW MY LOAN STATUS
# ==========================================
def get_my_status(db: Session, account_number: str):

    loans = (
        db.query(models.Loan)
        .filter(models.Loan.account_number == account_number)
        .all()
    )

    return loans


# ==========================================
# UPDATE LOAN
# ==========================================
def update_loan(db: Session, loan_id: int, loan: schemas.LoanUpdate):

    existing_loan = (
        db.query(models.Loan)
        .filter(models.Loan.id == loan_id)
        .first()
    )

    if not existing_loan:
        return {"error": "Loan not found"}

    if existing_loan.status != "Pending":
        return {"error": "Only Pending Loans can be updated"}

    if loan.loan_amount is not None:
        existing_loan.loan_amount = loan.loan_amount

    if loan.loan_type is not None:
        existing_loan.loan_type = loan.loan_type

    if loan.monthly_income is not None:
        existing_loan.monthly_income = loan.monthly_income

    if loan.credit_score is not None:
        existing_loan.credit_score = loan.credit_score

    if loan.date is not None:
        existing_loan.date = loan.date

    db.commit()
    db.refresh(existing_loan)

    return existing_loan


# ==========================================
# DELETE LOAN
# ==========================================
def delete_loan(db: Session, loan_id: int):

    loan = (
        db.query(models.Loan)
        .filter(models.Loan.id == loan_id)
        .first()
    )

    if not loan:
        return {"error": "Loan not found"}

    if loan.status != "Pending":
        return {"error": "Only Pending Loans can be deleted"}

    db.delete(loan)
    db.commit()

    return {"message": "Loan Deleted Successfully"}


# ==========================================
# APPROVE LOAN
# ==========================================
def approve_loan(db: Session, loan_id: int):

    loan = (
        db.query(models.Loan)
        .filter(models.Loan.id == loan_id)
        .first()
    )

    if not loan:
        return {"error": "Loan not found"}

    if loan.status != "Pending":
        return {"error": "Loan already processed"}

    loan.status = "Approved"

    db.commit()
    db.refresh(loan)

    return loan


# ==========================================
# REJECT LOAN
# ==========================================
def reject_loan(db: Session, loan_id: int):

    loan = (
        db.query(models.Loan)
        .filter(models.Loan.id == loan_id)
        .first()
    )

    if not loan:
        return {"error": "Loan not found"}

    if loan.status != "Pending":
        return {"error": "Loan already processed"}

    loan.status = "Rejected"

    db.commit()
    db.refresh(loan)

    return loan