from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Deparment(Base):
    """
    This class implements the deparment model.
    """

    __tablename__ = "deparment"

    id = Column(Integer, primary_key=True, nullable=False)
    deparment = Column(String(20), nullable=False)


class Job(Base):
    """
    This class implements the job model.
    """

    __tablename__ = "job"

    id = Column(Integer, primary_key=True, nullable=False)
    job = Column(String(20), primary_key=True, nullable=False)


class Employee(Base):
    """
    This class implements the employee model.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=True)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("deparment.id"))
    job_id = Column(Integer, ForeignKey("job.id"))

    deparment = relationship("Deparment")
    job = relationship("Job")
