import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import os
import sys

class RainshopFastAPIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RainshopFastAPI"
    _svc_display_name_ = "Rainshop FastAPI Service"
    _svc_description_ = "Service to run Rainshop FastAPI server using uvicorn"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def start(self):

        project_path = r"C:\\Users\\testl\\Documents\\RainShop\\rainshopGitHub\\rainshop\\rainshop_fastapi"
        venv_python = sys.executable
        log_path = os.path.join(project_path, "rainshop_service.log")

        # 👇 Ini log untuk memastikan Python mana yang dipakai
        with open(log_path, "a") as log:
            log.write(f"[LOG] Using Python Executable: {venv_python}\n")
            log.write(f"[LOG] Current Working Directory: {project_path}\n")
            log.write(f"[LOG] Exists? {os.path.exists(project_path)}\n")


        # 👇 Jalankan uvicorn dari venv
        with open(log_path, "a") as log:
            self.process = subprocess.Popen([
                venv_python,
                "-m", "uvicorn",
                "app.main:app",
                "--host", "127.0.0.1",
                "--port", "8000"
            ], cwd=project_path, stdout=log, stderr=log)