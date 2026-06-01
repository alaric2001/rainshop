@echo off

REM === Dapatkan IP lokal (WiFi/LAN) ===
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"IPv4.*192\." /C:"IPv4.*10\." /C:"IPv4.*172\."') do (
    set LOCAL_IP=%%a
    goto :found
)
:found
set LOCAL_IP=%LOCAL_IP: =%

REM === Jalankan Backend (FastAPI) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM === Jalankan Frontend (static webapp) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop\webapp && http-server -p 8080 --host 0.0.0.0"

REM === Tampilkan info akses ===
echo.
echo ============================================
echo   Rainshop sudah berjalan!
echo ============================================
echo   PC / Lokal  : http://127.0.0.1:8080
echo   Handphone   : http://%LOCAL_IP%:8080
echo ============================================
echo.

REM === Tunggu sebentar supaya server siap ===
timeout /t 45 >nul

REM === Buka Microsoft Edge di PC ===
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-tab http://127.0.0.1:8080/#/item-list

pause
