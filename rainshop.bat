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

REM === Info akses ===
echo.
echo ============================================
echo   Rainshop HTTPS sudah berjalan!
echo ============================================
echo   PC / Lokal  : https://127.0.0.1:8080
echo   Handphone   : https://%LOCAL_IP%:8080
echo.
echo   PERTAMA KALI di HP:
echo   1. Buka https://%LOCAL_IP%:8080
echo   2. Ketuk "Lanjutkan" / "Advanced - Proceed"
echo   3. Lakukan hal yang sama di https://%LOCAL_IP%:8000
echo ============================================
echo.

REM === Tunggu server siap ===
timeout /t 45 >nul

REM === Buka Edge di PC ===
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-tab https://127.0.0.1:8080/#/item-input

pause
