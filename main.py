from fastapi import FastAPI
from database import Base, engine
from routers import auth, employee, admin

app = FastAPI(
    title="Loan Approval System",
    version="1.0.0"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Welcome to Loan Approval System API"
    }


app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(admin.router)