from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.schemas.deparment import DeparmentEnum
from app.schemas.job import JobEnum


class Department(Base):
    """
    This class implements the deparment model.
    """

    __tablename__ = "department"

    id = Column(Integer, primary_key=True, nullable=False)
    department = Column(Enum(DeparmentEnum), nullable=False)


class Job(Base):
    """
    This class implements the job model.
    """

    __tablename__ = "job"

    id = Column(Integer, primary_key=True, nullable=False)
    job = Column(Enum(JobEnum), primary_key=True, nullable=False)


class Employee(Base):
    """
    This class implements the employee model.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=True)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"))
    job_id = Column(Integer, ForeignKey("job.id"))

    department = relationship("Department")
    job = relationship("Job")
