@echo off
echo 🤖 YOUR CRUSH AI BOT - START SCRIPT
echo ====================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "venv\Scripts\python.exe" (
    echo ⚠️ Virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Check requirements
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

echo ✅ Python environment ready.

REM Check dependencies
echo Checking dependencies...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo ✅ Dependencies installed.

REM Check configuration
if not exist "config.json" (
    echo ⚠️ config.json not found. Creating default...
    python scripts/setup_bot.py --fix
)

REM Check cookies
if not exist "data\cookies\master_cookies.json" (
    echo ⚠️ Facebook cookies not found.
    echo.
    echo IMPORTANT: You need to extract Facebook cookies first!
    echo.
    choice /c yn /m "Extract cookies now?"
    if errorlevel 2 (
        echo ❌ Cookies required to run bot.
        pause
        exit /b 1
    )
    python scripts\extract_cookies.py
    if errorlevel 1 (
        echo ❌ Failed to extract cookies.
        pause
        exit /b 1
    )
)

echo ✅ All checks passed!

REM Start the bot
echo.
echo 🚀 Starting YOUR CRUSH AI BOT...
echo ====================================
echo.
echo 📋 Bot Information:
echo    Name: YOUR CRUSH ⟵o_0
echo    Author: MAR PD (RANA)
echo    Version: 1.0.0
echo.
echo ⚡ Features:
echo    • Facebook Messenger Bot
echo    • AI Learning System  
echo    • Photo Delivery
echo    • Command System
echo.
echo 📞 Support:
echo    • Email: ranaeditz333@gmail.com
echo    • Telegram: @rana_editz_00
echo.
echo ====================================
echo.

REM Run the bot
python run.py --mode interactive

REM If bot stops
echo.
echo Bot stopped.
pause