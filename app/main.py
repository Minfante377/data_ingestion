import codecs
import csv
from typing import List

from dateutil import parser
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.crud import batch_insert
from app.database import SessionLocal
from app.models.models import Department, Employee, Job
from app.schemas.responses import EmployeesByQuarter

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
            if row["datetime"]:
                row["datetime"] = parser.parse(row["datetime"])
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
            codecs.iterdecode(file.file, "utf-8"), fieldnames=["id", "department"]
        )
        batch = []
        for row in csvReader:
            batch.append(Department(**row))
        batch_insert(db, batch)
        return {"departments": len(batch)}

    raise HTTPException(
        status_code=400,
        detail="File type must be one of ['job', 'deparment', 'employee']",
    )


@app.get("/employees_by_quarter")
def get_employees_by_quarter(db: Session = Depends(get_db)) -> List[EmployeesByQuarter]:
    query = """
    WITH employees_2021 AS (
      SELECT
        e.datetime AS hired_dt,
        d.department,
        j.job
      FROM
        employees e
        INNER JOIN department d ON d.id = e.department_id
        INNER JOIN job j ON j.id = e.job_id
      WHERE
        strftime('%Y', e.datetime) = '2021'
    )
    SELECT
      department,
      job,
      SUM(
        CASE WHEN CAST(strftime('%m', hired_dt) AS INTEGER) < 4
            THEN 1 ELSE 0 END
      ) AS q1,
      SUM(
        CASE WHEN CAST(strftime('%m',hired_dt) AS INTEGER) > 3
            AND CAST(strftime('%m',hired_dt) AS INTEGER) < 7 THEN 1 ELSE 0 END
      ) AS q2,
      SUM(
        CASE WHEN CAST(strftime('%m',hired_dt) AS INTEGER) > 6
            AND CAST(strftime('%m',hired_dt) AS INTEGER) < 10 THEN 1 ELSE 0 END
      ) AS q3,
      SUM(
        CASE WHEN CAST(strftime('%m',hired_dt) AS INTEGER) > 9
            THEN 1 ELSE 0 END
      ) AS q4
    FROM
      employees_2021
    GROUP BY
      department,
      job
    ORDER BY
      department ASC,
      job ASC
    """
    result = db.execute(text(query))
    data = [
        EmployeesByQuarter(
            department=r[0],
            job=r[1],
            q1=r[2],
            q2=r[3],
            q3=r[4],
            q4=r[5],
        )
        for r in result.fetchall()
    ]

    return data
