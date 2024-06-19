from enum import Enum


class JobEnum(str, Enum):
    """
    This class defines the allowed job names.
    """

    Recruiter = "Recruiter"
    Manager = "Manager"
    Analyst = "Analyst"
