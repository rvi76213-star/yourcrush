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

@echo off
chcp 65001 >nul
echo.
echo 🤖 YOUR CRUSH AI BOT - START SCRIPT
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Install Python 3.8+ first.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

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
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Check requirements
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    echo Creating minimal requirements...
    (
    echo requests>=2.28.0
    echo browser-cookie3>=0.19.0
    echo cryptography>=40.0.0
    echo Pillow>=9.5.0
    echo emoji>=2.0.0
    echo python-dotenv>=1.0.0
    echo colorama>=0.4.6
    ) > requirements.txt
)

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
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)
echo.

REM Check configuration
if not exist "config.json" (
    echo ⚠️ config.json not found. Creating default...
    python -c "
import json
config = {
    'bot': {
        'name': 'YOUR CRUSH ⟵o_0',
        'author': 'MAR PD',
        'version': '1.0.0'
    }
}
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
"
)

REM Check cookies
if not exist "data\cookies\master_cookies.json" (
    echo ⚠️ Facebook cookies not found.
    echo.
    echo IMPORTANT: You need to extract Facebook cookies first!
    echo.
    echo Step-by-step guide:
    echo 1. Login to Facebook in your browser
    echo 2. Make sure you're logged in
    echo 3. Then extract cookies
    echo.
    set /p choice="Extract cookies now? (y/n): "
    if /i "%choice%"=="y" (
        echo Extracting cookies...
        python scripts\extract_cookies.py
        if errorlevel 1 (
            echo ❌ Failed to extract cookies.
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Cookies required to run bot.
        pause
        exit /b 1
    )
)

echo ✅ All checks passed!
echo.

REM Start the bot
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
echo    • Phone: 01847634486
echo.
echo ====================================
echo.

REM Run the bot
python run.py --start

REM If bot stops
echo.
echo Bot stopped.
pause