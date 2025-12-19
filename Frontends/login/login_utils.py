import re
from Frontends.login.login_constants import (
    STUDENT_DOMAIN,
    TEACHER_DOMAIN,
    STAFF_DOMAIN,
    ADMIN_EMAIL,
    ROLE_STUDENT,
    ROLE_TEACHER,
    ROLE_STAFF,
    ROLE_ADMIN
)

from Frontends.login.login_constants import ADMIN_EMAIL, ADMIN_PASSWORD

def validate_admin(email, password):
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD


class LoginError(Exception):
    """Custom exception for login related errors"""
    pass


def parse_login_email(email: str) -> dict:
    """
    Parses login email and returns role + user_id

    Returns:
    {
        "role": "student" | "teacher" | "staff" | "admin",
        "user_id": int | None
    }

    Raises:
        LoginError with proper message
    """

    if not email:
        raise LoginError("Login ID cannot be empty")

    email = email.strip().lower()

    # ---- ADMIN LOGIN ----
    if email == ADMIN_EMAIL:
        return {
            "role": ROLE_ADMIN,
            "user_id": None
        }

    # ---- BASIC FORMAT CHECK ----
    if "@" not in email:
        raise LoginError("Invalid login ID format")

    local_part, domain = email.split("@", 1)

    # ---- DOMAIN VALIDATION ----
    if domain == STUDENT_DOMAIN:
        role = ROLE_STUDENT
    elif domain == TEACHER_DOMAIN:
        role = ROLE_TEACHER
    elif domain == STAFF_DOMAIN:
        role = ROLE_STAFF
    else:
        raise LoginError("Invalid domain in login ID")

    # ---- LOCAL PART VALIDATION ----
    # Expected: <id><name>  e.g. 7rahul
    match = re.match(r"^(\d+)[a-zA-Z]+$", local_part)
    if not match:
        raise LoginError("Invalid login ID format")

    user_id = int(match.group(1))

    if user_id <= 0:
        raise LoginError("Invalid user ID")

    return {
        "role": role,
        "user_id": user_id
    }
