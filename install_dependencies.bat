@echo off
echo 🤖 YOUR CRUSH AI BOT - DEPENDENCY INSTALLATION
echo ==============================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b 1
)

echo ✅ Virtual environment created and activated.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ Failed to upgrade pip. Continuing anyway...
)

REM Install dependencies
echo Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo ❌ requirements.txt not found!
    echo Creating basic requirements...
    
    echo requests>=2.28.0 > requirements.txt
    echo browser-cookie3>=0.19.0 >> requirements.txt
    echo cryptography>=40.0.0 >> requirements.txt
    echo Pillow>=9.5.0 >> requirements.txt
    echo emoji>=2.0.0 >> requirements.txt
    echo python-dotenv>=1.0.0 >> requirements.txt
    
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install basic dependencies.
        pause
        exit /b 1
    )
)

echo ✅ All dependencies installed successfully!

REM Install AI dependencies (optional)
echo.
choice /c yn /m "Install optional AI dependencies (OpenAI, transformers, etc.)?"
if errorlevel 2 (
    echo Skipping AI dependencies.
    goto :success
)

echo Installing AI dependencies...
if exist "requirements_ai.txt" (
    pip install -r requirements_ai.txt
    if errorlevel 1 (
        echo ⚠️ Failed to install some AI dependencies. Continuing...
    )
) else (
    echo ❌ requirements_ai.txt not found. Creating basic AI requirements...
    
    echo openai>=0.27.0 > requirements_ai.txt
    echo transformers>=4.28.0 >> requirements_ai.txt
    echo torch>=2.0.0 >> requirements_ai.txt
    echo numpy>=1.24.0 >> requirements_ai.txt
    echo nltk>=3.8.0 >> requirements_ai.txt
    
    pip install -r requirements_ai.txt
    if errorlevel 1 (
        echo ⚠️ Failed to install some AI dependencies. Continuing...
    )
)

:success
echo.
echo 🎉 DEPENDENCY INSTALLATION COMPLETE!
echo.
echo Next steps:
echo 1. Run setup: python scripts\setup_bot.py
echo 2. Extract cookies: python scripts\extract_cookies.py
echo 3. Start bot: python run.py
echo.
pause