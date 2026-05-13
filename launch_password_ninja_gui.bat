@echo off
setlocal

python "%~dp0password_ninja_gui.py"

if errorlevel 1 (
    echo.
    echo If Python is not installed or not on PATH, install Python 3 and try again.
    pause
)
