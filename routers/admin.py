from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/admin",
    tags=["Manager"]
)


# ==========================
# Database Dependency
# ==========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# View All Loan Requests
# ==========================
@router.get(
    "/loans",
    response_model=list[schemas.LoanResponse]
)
def get_all_loans(
    db: Session = Depends(get_db)
):
    return db.query(models.Loan).all()


# ==========================
# Approve Loan
# ==========================
@router.put(
    "/approve/{loan_id}",
    response_model=schemas.LoanResponse
)
def approve_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    result = crud.approve_loan(db, loan_id)

    if isinstance(result, dict):
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


# ==========================
# Reject Loan
# ==========================
@router.put(
    "/reject/{loan_id}",
    response_model=schemas.LoanResponse
)
def reject_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    result = crud.reject_loan(db, loan_id)

    if isinstance(result, dict):
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result