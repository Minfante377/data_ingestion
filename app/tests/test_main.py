import datetime as dt

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db
from app.models.models import Department, Employee, Job

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_upload_employee(init_db):
    """
    Test for /upload for uploading employee records.
    """
    db = TestingSessionLocal()
    db.add(Department(id=1, department="fake department"))
    db.add(Job(id=1, job="fake job"))
    db.commit()

    with open("app/tests/test_files/employees.csv", "rb") as f:
        response = client.post(
            "/upload?file_type=employee",
            files={"file": f},
        )

    assert response.json() == {"employees": 1}

    employees = db.query(Employee).all()

    assert len(employees) == 1
    assert employees[0].id == 1


def test_upload_job(init_db):
    """
    Test for /upload for uploading job records.
    """
    db = TestingSessionLocal()

    with open("app/tests/test_files/jobs.csv", "rb") as f:
        response = client.post(
            "/upload?file_type=job",
            files={"file": f},
        )

    assert response.json() == {"jobs": 1}

    jobs = db.query(Job).all()

    assert len(jobs) == 1
    assert jobs[0].id == 1


def test_upload_department(init_db):
    """
    Test for /upload for uploading department records.
    """
    db = TestingSessionLocal()

    with open("app/tests/test_files/departments.csv", "rb") as f:
        response = client.post(
            "/upload?file_type=department",
            files={"file": f},
        )

    assert response.json() == {"departments": 1}

    departments = db.query(Department).all()

    assert len(departments) == 1
    assert departments[0].id == 1


def test_upload_wrong_file_type(init_db):
    """
    Test for /upload for trying to upload a not supported file type.
    """
    with open("app/tests/test_files/departments.csv", "rb") as f:
        response = client.post(
            "/upload?file_type=fake",
            files={"file": f},
        )

    assert response.status_code == 400


def test_employees_by_department(init_db):
    """
    Test for /employees_by_department endpoint.
    """
    db = TestingSessionLocal()
    db.add(Department(id=1, department="fake department"))
    db.add(Department(id=2, department="fake department"))
    db.add(Job(id=1, job="fake job"))
    for i in range(5):
        db.add(
            Employee(
                id=i,
                name="fake name",
                datetime=dt.datetime(2021, 1, 1),
                department_id=1,
                job_id=1,
            )
        )
    db.add(
        Employee(
            id=6,
            name="fake name",
            datetime=dt.datetime(2022, 2, 2),
            department_id=1,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=7,
            name="fake name",
            datetime=dt.datetime(2021, 2, 2),
            department_id=2,
            job_id=1,
        )
    )

    db.commit()

    response = client.get("/employees_by_department")

    assert response.json() == [{"id": 1, "department": "fake department", "hired": 5}]


def test_employees_by_quarter(init_db):
    """
    Test for /employees_by_quarter endpoint.
    """
    db = TestingSessionLocal()
    db.add(Department(id=1, department="fake department"))
    db.add(Department(id=2, department="fake department 2"))
    db.add(Job(id=1, job="fake job 1"))
    db.add(Job(id=2, job="fake job 2"))
    db.add(
        Employee(
            id=1,
            name="fake name",
            datetime=dt.datetime(2021, 1, 1),
            department_id=1,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=2,
            name="fake name",
            datetime=dt.datetime(2021, 4, 1),
            department_id=1,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=3,
            name="fake name",
            datetime=dt.datetime(2021, 9, 1),
            department_id=1,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=4,
            name="fake name",
            datetime=dt.datetime(2021, 12, 1),
            department_id=1,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=5,
            name="fake name",
            datetime=dt.datetime(2021, 12, 1),
            department_id=2,
            job_id=1,
        )
    )
    db.add(
        Employee(
            id=6,
            name="fake name",
            datetime=dt.datetime(2021, 12, 1),
            department_id=1,
            job_id=2,
        )
    )
    db.add(
        Employee(
            id=7,
            name="fake name",
            datetime=dt.datetime(2022, 1, 1),
            department_id=1,
            job_id=1,
        )
    )

    db.commit()

    response = client.get("/employees_by_quarter")

    assert response.json() == [
        {
            "department": "fake department",
            "job": "fake job 1",
            "q1": 1,
            "q2": 1,
            "q3": 1,
            "q4": 1,
        },
        {
            "department": "fake department",
            "job": "fake job 2",
            "q1": 0,
            "q2": 0,
            "q3": 0,
            "q4": 1,
        },
        {
            "department": "fake department 2",
            "job": "fake job 1",
            "q1": 0,
            "q2": 0,
            "q3": 0,
            "q4": 1,
        },
    ]
