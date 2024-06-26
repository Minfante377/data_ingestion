from pydantic import BaseModel


class EmployeesByQuarter(BaseModel):
    """
    This class defines the schema for
    the hired employees by job, department and quarter.
    """

    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int


class MostHiresByDepartment(BaseModel):
    """
    This class defines the schema for the greatest
    number of employees hired by deparment
    """

    id: int
    department: str
    hired: int
