@echo off

REM === Jalankan Backend (FastAPI) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop && uvicorn app.main:app --reload"

REM === Jalankan Frontend (static webapp) ===
start cmd /k "cd /d C:\Users\Rain Shop\Documents\SistemRainShop\rainshop\webapp && http-server -p 8080 --host 0.0.0.0"

REM === Tunggu sebentar supaya server siap ===
timeout /t 45 >nul

REM === Buka Microsoft Edge ===
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-tab http://127.0.0.1:8080/#/item-list

pause
