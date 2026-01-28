@echo off
title AI Internship Diary Assistant
cd /d %~dp0

echo ==========================================
echo   AI Internship Diary Assistant
echo ==========================================
echo.

REM -------------------------------
REM Check virtual environment
REM -------------------------------
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found.
    echo Using system Python...
)

echo.
echo Launching application...
echo.

python gui\app.py

echo.
echo Application closed.
pause
