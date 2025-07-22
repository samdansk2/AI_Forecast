@echo off
echo.
echo AI Progress Tracker - UV Setup (Windows)
echo =========================================
echo.

REM Check if UV is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo UV not found. Installing UV...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    echo Please restart this script after UV installation is complete.
    pause
    exit /b
)

echo UV is installed. Setting up project...
echo.

REM Install dependencies
echo Installing project dependencies...
uv sync
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Installing development dependencies...
uv sync --extra dev
if %errorlevel% neq 0 (
    echo Warning: Failed to install development dependencies
)

echo Installing notebook dependencies...
uv sync --extra notebook
if %errorlevel% neq 0 (
    echo Warning: Failed to install notebook dependencies
)

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Activate virtual environment: .venv\Scripts\activate
echo 2. Run application: uv run ai-tracker
echo 3. Start dashboard: uv run streamlit run dashboard/streamlit_app.py
echo 4. Start Jupyter: uv run jupyter lab
echo.
pause
