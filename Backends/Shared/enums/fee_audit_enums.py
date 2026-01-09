from enum import Enum

class FeeAuditEntity(str, Enum):
    INVOICE = "INVOICE"
    PAYMENT = "PAYMENT"
    FEE_MASTER = "FEE_MASTER"

class FeeAuditAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    STATUS_CHANGE = "STATUS_CHANGE"
    PAYMENT_ADDED = "PAYMENT_ADDED"
    PAYMENT_REVERSED = "PAYMENT_REVERSED"
    AUTO_GENERATED = "AUTO_GENERATED"

class AuditActorRole(str, Enum):
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"
    STUDENT = "STUDENT"
    PARENT = "PARENT"

class AuditSource(str, Enum):
    UI = "UI"
    API = "API"
    SYSTEM_JOB = "SYSTEM_JOB"
