import subprocess
import sys
import time
from multiprocessing import Process

# ---- CONFIG ----
BACKEND_FILE = "Backends.Backend_main:app"

FRONTENDS = {
    "admin": "Frontends/Frontend_admin/admin_main.py",
    "teacher": "Frontends/Frontend_teacher/teacher_main.py",
    "student": "Frontends/Frontend_student/student_main.py"
}

# ---- START BACKEND ----
def start_backend():
    print("[BOOT] Starting backend...")
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", BACKEND_FILE, "--reload"]
    )

# ---- START FRONTEND ----
def start_frontend(name, file):
    print(f"[BOOT] Starting frontend: {name}")
    subprocess.Popen(
        [sys.executable, file]
    )

if __name__ == "__main__":

    print("Launching School ERP FULL SYSTEM")
    print("=====================================\n")

    # START BACKEND
    backend_proc = Process(target=start_backend)
    backend_proc.start()

    # giving backend time to start
    time.sleep(1)

    # STARTING ALL FRONTENDS
    frontend_procs = [
        Process(target=start_frontend, args=(name, file))
        for name, file in FRONTENDS.items()
    ]

    for p in frontend_procs:
        p.start()

    print("\nALL SYSTEMS LIVE!")
    print("Admin / Teacher / Student dashboards are now running.\n")

    # KEEP RUNNING
    backend_proc.join()
    for p in frontend_procs:
        p.join()
