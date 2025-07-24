@echo off
set PYTHON_PATH=...
set SCRIPT_PATH=...\train\train.py

schtasks /Create /SC DAILY /TN "Schedule" /TR "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" /ST 02:00 /F

if %ERRORLEVEL% EQU 0 (
    echo 작업 스케줄러 등록 성공
) else (
    echo 작업 스케줄러 등록 실패
)
pause
