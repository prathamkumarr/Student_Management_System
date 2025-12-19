# ===========================
# LOGIN CONSTANTS
# ===========================

# ---- DOMAIN CONFIG ----
STUDENT_DOMAIN = "student.school.in"
TEACHER_DOMAIN = "teacher.school.in"
STAFF_DOMAIN   = "staff.school.in"

# ---- ADMIN LOGIN ----
ADMIN_EMAIL = "admin@school.in"
ADMIN_PASSWORD = "admin123"

# ---- ROLE IDENTIFIERS ----
ROLE_STUDENT = "student"
ROLE_TEACHER = "teacher"
ROLE_STAFF   = "staff"
ROLE_ADMIN   = "admin"

# ---- REGEX PARTS ----
# Example valid IDs:
# 7rahul@student.school.in
# 12abc@teacher.school.in
# 3x@staff.school.in

ID_NAME_REGEX = r"^(\d+)[a-zA-Z]+$"

# ---- FULL EMAIL REGEX (used internally later) ----
EMAIL_REGEX = rf"^(\d+)[a-zA-Z]+@({'|'.join([STUDENT_DOMAIN, TEACHER_DOMAIN, STAFF_DOMAIN])})$"
