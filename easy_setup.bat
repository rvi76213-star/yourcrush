@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════╗
echo ║          🤖 YOUR CRUSH AI BOT v1.0.0            ║
echo ║            COMPLETE SETUP SCRIPT                ║
echo ╚═══════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected

:: Create directory structure
echo.
echo 📁 Creating folder structure...
if not exist "data" mkdir data
if not exist "data\cookies" mkdir data\cookies
if not exist "data\photos" mkdir data\photos
if not exist "data\commands" mkdir data\commands
if not exist "data\commands\prefix" mkdir data\commands\prefix
if not exist "data\commands\prefix\murgi" mkdir data\commands\prefix\murgi
if not exist "data\logs" mkdir data\logs
if not exist "config" mkdir config

echo ✅ Folders created

:: Create essential files
echo.
echo ⚙️ Creating configuration files...

:: Create config.json
echo {
echo   "bot": {
echo     "name": "\uD835\uDD1F\uD835\uDD28\uD835\uDD30\uD835\uDD2F \uD835\uDD0C\uD835\uDD2B\uD835\uDD34\uD835\uDD2C\uD835\uDD21\uD835\uDD24 \u27F5o_0",
echo     "author": "MAR PD",
echo     "version": "1.0.0",
echo     "status": "active"
echo   },
echo   "facebook": {
echo     "login_method": "cookie",
echo     "cookie_file": "data/cookies/master_cookies.json",
echo     "profile_url": "https://www.facebook.com/share/17gEJAipcr/"
echo   },
echo   "commands": {
echo     "prefix": ".",
echo     "admin_prefix": "!",
echo     "enabled_commands": ["murgi", "love", "pick", "dio", "info", "uid"]
echo   },
echo   "photos": {
echo     "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
echo     "default_photo": "master.jpg"
echo   }
echo } > config.json

:: Create .murgi files
echo 🐔 মুরগির ডিম পছন্দ করি! > data\commands\prefix\murgi\v1.txt
echo 🍗 মুরগির রেস্তোরাঁয় যেতে চাও? >> data\commands\prefix\murgi\v1.txt
echo 🏡 আমার বাড়িতে ১০টা মুরগি আছে! >> data\commands\prefix\murgi\v1.txt

echo 🐣 মুরগির বাচ্চা খুব মিষ্টি! > data\commands\prefix\murgi\v2.txt
echo 🌾 মুরগির জন্য দানা কিনতে হবে! >> data\commands\prefix\murgi\v2.txt
echo 🔪 আজ রাতে মুরগি রান্না হবে! >> data\commands\prefix\murgi\v2.txt

echo 🏆 মুরগি প্রতিযোগিতা দেখেছো? > data\commands\prefix\murgi\v3.txt
echo 🎨 মুরগির ছবি আঁকতে পারো? >> data\commands\prefix\murgi\v3.txt
echo 📚 মুরগি নিয়ে বই পড়েছো? >> data\commands\prefix\murgi\v3.txt

echo ✅ Configuration created

:: Install dependencies
echo.
echo 📦 Installing Python dependencies...
pip install requests browser-cookie3 cryptography Pillow emoji python-dotenv colorama --quiet

if errorlevel 1 (
    echo ⚠️ Some dependencies may have failed to install
    echo You can install manually: pip install requests browser-cookie3 cryptography
) else (
    echo ✅ Dependencies installed
)

:: Show instructions
echo.
echo ============================================
echo 🎉 SETUP COMPLETE! Your bot is ready!
echo ============================================
echo.
echo 📋 NEXT STEPS:
echo.
echo 1. ADD YOUR PHOTOS:
echo    Copy your photos to: data\photos\
echo    Required: master.jpg, photo.jpg, own.jpg
echo.
echo 2. EXTRACT FACEBOOK COOKIES:
echo    python run.py --cookies
echo    (Make sure Facebook is logged in browser)
echo.
echo 3. START YOUR BOT:
echo    python run.py
echo    OR: python simple_bot.py (for quick test)
echo.
echo ============================================
echo 📱 BOT INFORMATION:
echo Name: YOUR CRUSH ⟵o_0
echo Author: MAR PD (RANA)
echo Email: ranaeditz333@gmail.com
echo Phone: 01847634486
echo ============================================
echo.
echo ⚡ QUICK COMMANDS IN CHAT:
echo .murgi - Chicken messages
echo .love  - Romantic responses
echo .pick  - Random selection
echo .info  - Bot information
echo.
echo 📸 Ask for photos: 'ছবি দাও', 'তোমার ফটো'
echo.
pause