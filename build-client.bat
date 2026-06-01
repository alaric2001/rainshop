@echo off
echo === Build Frontend Client ===
cd /d "%~dp0client"
call npm run build
if %errorlevel% neq 0 (
    echo BUILD GAGAL!
    pause
    exit /b 1
)
echo.
echo === Copy ke webapp/ ===
xcopy /E /Y /I dist\* ..\webapp\
echo.
echo === Selesai! File webapp/ sudah diperbarui ===
pause
