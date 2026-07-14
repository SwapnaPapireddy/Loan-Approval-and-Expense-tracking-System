from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
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
# Apply Loan
# ==========================
@router.post(
    "/apply-loan",
    response_model=schemas.LoanResponse
)
def apply_loan(
    loan: schemas.LoanCreate,
    db: Session = Depends(get_db)
):
    result = crud.apply_loan(db, loan)

    if isinstance(result, dict):
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


# ==========================
# View My Loan Status
# ==========================
@router.get(
    "/status/{account_number}",
    response_model=list[schemas.LoanResponse]
)
def view_status(
    account_number: str,
    db: Session = Depends(get_db)
):
    return crud.get_my_status(db, account_number)


# ==========================
# Update Loan
# ==========================
@router.put(
    "/update/{loan_id}",
    response_model=schemas.LoanResponse
)
def update_loan(
    loan_id: int,
    loan: schemas.LoanUpdate,
    db: Session = Depends(get_db)
):
    result = crud.update_loan(db, loan_id, loan)

    if isinstance(result, dict):
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


# ==========================
# Delete Loan
# ==========================
@router.delete("/delete/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    result = crud.delete_loan(db, loan_id)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result