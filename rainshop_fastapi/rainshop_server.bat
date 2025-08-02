@echo off
REM Aktifkan virtual environment jika pakai venv
REM call .venvScriptsactivate

REM Jalankan uvicorn
uvicorn app.main:app --reload

pause
