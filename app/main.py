import codecs
import csv

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud import batch_insert
from app.database import SessionLocal
from app.models.models import Deparment, Employee, Job

app = FastAPI()


def get_db() -> Session:
    """
    Get a DB connection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload")
def upload(file: UploadFile, file_type: str, db: Session = Depends(get_db)):
    """
    This endpoint will allow the user to upload a csv file with either one
    of the employees, deparments or jobs information
    """
    if file_type == "employee":
        csvReader = csv.DictReader(
            codecs.iterdecode(file.file, "utf-8"),
            fieldnames=["id", "name", "datetime", "department_id", "job_id"],
        )
        batch = []
        for row in csvReader:
            batch.append(Employee(**row))
            batch_insert(db, batch)
            return {"employees": len(batch)}

    if file_type == "job":
        csvReader = csv.DictReader(
            codecs.iterdecode(file.file, "utf-8"), fieldnames=["id", "job"]
        )
        batch = []
        for row in csvReader:
            batch.append(Job(**row))
            batch_insert(db, batch)
            return {"jobs": len(batch)}

    if file_type == "department":
        csvReader = csv.DictReader(
            codecs.iterdecode(file.file, "utf-8"), fieldnames=["id", "deparment"]
        )
        batch = []
        for row in csvReader:
            batch.append(Deparment(**row))
            batch_insert(db, batch)
            return {"deparments": len(batch)}

    raise HTTPException(
        status_code=400,
        detail="File type must be one of ['job', 'deparment', 'employee']",
    )
