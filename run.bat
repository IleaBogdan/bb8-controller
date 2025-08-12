@echo off
set PYTHON_SCRIPT=main.py
set PYTHON_ARGS=--local

REM echo Running %PYTHON_SCRIPT% with arguments: %PYTHON_ARGS%
python -O %PYTHON_SCRIPT% %PYTHON_ARGS% 2>&1

if %errorlevel% neq 0 (
    echo.
    echo Python script failed with errorlevel %errorlevel%
    pause
)