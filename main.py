import os
import sys
import subprocess
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multiprocessing import Process

BACKEND_FILE = "Backends.Backend_main:app"

def start_backend():
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", BACKEND_FILE, "--reload"]
    )

def start_login():
    subprocess.Popen(
        [sys.executable, "-m", "Frontends.login.login_main"]
    )

if __name__ == "__main__":
    start_backend()
    time.sleep(1)
    start_login()
