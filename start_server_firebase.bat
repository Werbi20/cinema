@echo off
cd /d "C:\Users\werbi\cinema-erp\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8021 --reload
pause
