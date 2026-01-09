from enum import Enum

class BillingType(str, Enum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"


class FeeFrequency(str, Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    HALF_YEARLY = "HALF_YEARLY"
    YEARLY = "YEARLY"


class ChargeTrigger(str, Enum):
    ADMISSION = "ADMISSION"
    ACADEMIC_CYCLE = "ACADEMIC_CYCLE"


class FeeGeneratedBy(str, Enum):
    SYSTEM = "SYSTEM"   
    ADMIN = "ADMIN"   