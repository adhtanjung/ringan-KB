@echo off
REM Ringan Mental Health Knowledge Base Launcher for Windows
REM This script provides a simple way to run the Ringan KB application

REM Set text colors
set GREEN=92m
set CYAN=96m
set YELLOW=93m
set NC=0m

REM Display header
echo.
echo [%CYAN%==========================================================[%NC%]
echo [%CYAN%       RINGAN MENTAL HEALTH KNOWLEDGE BASE[%NC%]
echo [%CYAN%==========================================================[%NC%]
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%YELLOW%]Python is not installed or not in PATH. Please install Python 3.8 or higher.[%NC%]
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo [%YELLOW%]Virtual environment not found. Would you like to create one? (y/n)[%NC%]
    set /p create_venv=
    if /i "%create_venv%"=="y" (
        echo Creating virtual environment...
        python -m venv venv
        echo [%GREEN%]Virtual environment created.[%NC%]
    ) else (
        echo Proceeding without virtual environment.
    )
)

REM Activate virtual environment if it exists
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo [%GREEN%]Virtual environment activated.[%NC%]
)

REM Check if requirements are installed
echo Checking installation...
python check_installation.py

REM Display menu
echo.
echo [%CYAN%]Choose an option:[%NC%]
echo   [%GREEN%]1[%NC%]. Setup database and vector store
echo   [%GREEN%]2[%NC%]. Start interactive chat
echo   [%GREEN%]3[%NC%]. Generate knowledge base report
echo   [%GREEN%]4[%NC%]. Start API server (Uvicorn)
echo   [%GREEN%]5[%NC%]. Start frontend server
echo   [%GREEN%]6[%NC%]. Run all components (setup, verify, demo, report)
echo   [%GREEN%]7[%NC%]. Exit

set /p choice=Enter your choice (1-7): 

if "%choice%"=="1" (
    echo Setting up database and vector store...
    python ringan_kb.py --setup
) else if "%choice%"=="2" (
    echo Starting interactive chat...
    python ringan_kb.py --chat
) else if "%choice%"=="3" (
    echo Generating knowledge base report...
    python ringan_kb.py --report
) else if "%choice%"=="4" (
    echo Starting API server (Uvicorn)...
    uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
) else if "%choice%"=="5" (
    echo Starting frontend server...
    python ringan_kb.py --frontend
) else if "%choice%"=="6" (
    echo Running all components...
    python ringan_kb.py --all
) else if "%choice%"=="7" (
    echo Exiting...
    exit /b 0
) else (
    echo [%YELLOW%]Invalid choice. Please run the script again.[%NC%]
    exit /b 1
)

REM Deactivate virtual environment if it was activated
if exist venv (
    call venv\Scripts\deactivate.bat 2>nul
)

echo.
echo [%GREEN%]Done![%NC%]
pause