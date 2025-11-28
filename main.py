import subprocess
import sys
import time
from multiprocessing import Process

# ------- CONFIG --------
BACKEND_PATH = "Backends.admin_main:app"
FRONTEND_FILE = "Frontends/Frontend_admin/admin_main.py"

# ------------------------
def start_backend():
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", BACKEND_PATH, "--reload"]
    )

def start_frontend():
    subprocess.Popen(
        [sys.executable, FRONTEND_FILE]
    )

if __name__ == "__main__":
    print("LAUNCHING ADMIN DASHBOARD")
    print("--------------------------------")

    backend_proc = Process(target=start_backend)
    frontend_proc = Process(target=start_frontend)

    backend_proc.start()
    time.sleep(1)   # for clean logs

    frontend_proc.start()

    print("--------------------------------")
    print("School ERP is live!")

    backend_proc.join()
    frontend_proc.join()
