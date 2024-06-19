from enum import Enum


class DeparmentEnum(str, Enum):
    """
    This class defines the allowed deparment names
    """

    SupplyChain = "Supply Chain"
    Maintenance = "Maintenance"
    Staff = "Staff"
