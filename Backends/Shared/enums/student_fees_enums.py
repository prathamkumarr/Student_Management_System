from enum import Enum

class StudentFeeStatus(str, Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    DEACTIVATED = "DEACTIVATED"

