@echo off
echo 🤖 YOUR CRUSH AI BOT - COMPLETE PROJECT SETUP
echo ==============================================

echo Step 1: Creating project structure...
call create_structure.bat

echo.
echo Step 2: Installing dependencies...
call install_dependencies.bat

echo.
echo Step 3: Running bot setup...
python scripts/setup_bot.py --full

echo.
echo Step 4: Creating configuration files...
if not exist ".env" (
    copy .env.example .env
    echo ⚠️ Please edit .env file with your details!
)

echo.
echo Step 5: Setup Complete!
echo.
echo Next steps:
echo 1. Add your photos to data/photos/ folder
echo 2. Edit .env file with your Facebook details
echo 3. Extract cookies: python scripts/extract_cookies.py
echo 4. Start bot: python run.py
echo.
echo 📞 Support: ranaeditz333@gmail.com
pause