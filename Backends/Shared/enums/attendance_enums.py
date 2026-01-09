from enum import Enum

class AttendanceStatus(str, Enum):
    P  = "P"
    A  = "A"
    L  = "L"
    LE = "LE"

