from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
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
# Login (Bank Data)
# ==========================
@router.post("/login")
def login(
    user: schemas.LoginSchema,
    db: Session = Depends(get_db)
):
    result = crud.login(
        db,
        user.employee_name,
        user.account_number
    )

    if isinstance(result, dict):
        raise HTTPException(
            status_code=401,
            detail=result["error"]
        )

    return {
        "message": "Login Successful",
        "name": result.name,
        "account_number": result.account_number
    }


# ==========================
# Register Bank Data Record
# ==========================
@router.post(
    "/register",
    response_model=schemas.BankDataResponse
)
def register_bank_data(
    data: schemas.BankDataCreate,
    db: Session = Depends(get_db)
):
    return crud.create_bank_data(db, data)