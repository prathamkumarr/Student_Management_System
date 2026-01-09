from enum import Enum

class FeePaymentStatus(str, Enum):
    INITIATED = "initiated"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentSource(str, Enum):
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"

class PaymentReceivedBy(str, Enum):
    ONLINE = "ONLINE"
    CASH_COUNTER = "CASH_COUNTER"
    CHEQUE = "CHEQUE"
    SYSTEM = "SYSTEM"
