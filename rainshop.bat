@echo off
setlocal

REM === Dapatkan IP lokal ===
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"IPv4.*192\." /C:"IPv4.*10\." /C:"IPv4.*172\."') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%

REM === Jalankan Backend (FastAPI - HTTPS) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop && uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload"

REM === Jalankan Frontend (static webapp - HTTPS) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop\webapp && http-server -p 8080 --host 0.0.0.0 -S -C ..\cert.pem -K ..\key.pem"

REM === Jalankan ngrok (expose backend ke internet) ===
set NGROK=%LOCALAPPDATA%\ngrok\ngrok.exe
start cmd /k ""%NGROK%" http --domain=cube-judicial-amber.ngrok-free.dev https://localhost:8000"

REM === Info akses ===
echo.
echo ============================================================
echo   Rainshop sudah berjalan!
echo ============================================================
echo   [LAN]      PC     : https://127.0.0.1:8080
echo   [LAN]      HP     : https://%LOCAL_IP%:8080
echo   [INTERNET] Demo   : https://alaric2001.github.io/rainshop/
echo   [INTERNET] API    : https://cube-judicial-amber.ngrok-free.dev
echo.
echo   PERTAMA KALI akses LAN dari HP:
echo   1. Buka https://%LOCAL_IP%:8000  -> Advanced -> Proceed
echo   2. Buka https://%LOCAL_IP%:8080  -> Advanced -> Proceed
echo ============================================================
echo.

REM === Tunggu server siap lalu buka browser ===
timeout /t 10 >nul
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-tab https://127.0.0.1:8080/#/item-input

pause
