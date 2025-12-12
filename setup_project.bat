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

@echo off
chcp 65001 >nul
echo.
echo 🤖 YOUR CRUSH AI BOT - COMPLETE PROJECT SETUP
echo ==============================================
echo.

echo Step 1: Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.8+ from: https://python.org
    pause
    exit /b 1
)
echo ✅ Python found
echo.

echo Step 2: Creating project structure...
call :create_structure
echo ✅ Directory structure created
echo.

echo Step 3: Creating configuration files...
python -c "
import json
import os

# Create config.json
config = {
    'bot': {
        'name': 'YOUR CRUSH ⟵o_0',
        'author': 'MAR PD',
        'version': '1.0.0',
        'status': 'active'
    },
    'facebook': {
        'login_method': 'cookie',
        'cookie_file': 'data/cookies/master_cookies.json'
    },
    'commands': {
        'prefix': '.',
        'enabled_commands': ['murgi', 'love', 'pick', 'dio', 'info']
    }
}

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Create bot_identity.json
identity = {
    'identity': {
        'bot_name': 'YOUR CRUSH ⟵o_0',
        'author': 'MAR PD',
        'real_name': 'RANA',
        'age': 20,
        'from': 'FARIDPUR DHAKA',
        'email': 'ranaeditz333@gmail.com',
        'phone': '01847634486'
    }
}

with open('bot_identity.json', 'w', encoding='utf-8') as f:
    json.dump(identity, f, indent=2, ensure_ascii=False)

print('Configuration files created')
"
echo ✅ Configuration files created
echo.

echo Step 4: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created
echo.

echo Step 5: Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing dependencies...
pip install requests browser-cookie3 cryptography Pillow emoji python-dotenv colorama schedule loguru
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

echo Step 6: Creating command files...
call :create_command_files
echo ✅ Command files created
echo.

echo Step 7: Creating placeholder photos...
python -c "
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    photos = [
        ('master.jpg', 'MASTER\\nYOUR CRUSH ⟵o_0\\nMAR PD', (400, 400)),
        ('photo.jpg', 'PHOTO\\nYOUR CRUSH\\nRomantic Bot', (400, 400)),
        ('own.jpg', 'OWN\\nRANA\\nDeveloper', (400, 400))
    ]
    
    for filename, text, size in photos:
        img = Image.new('RGB', size, color='purple')
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('arial.ttf', 40)
        except:
            font = ImageFont.load_default()
        d.text((size[0]//2, size[1]//2), text, fill='white', font=font, anchor='mm')
        img.save(f'data/photos/{filename}')
        print(f'Created: data/photos/{filename}')
except ImportError:
    print('PIL not installed, creating empty files')
    for filename in ['master.jpg', 'photo.jpg', 'own.jpg']:
        open(f'data/photos/{filename}', 'wb').close()
        print(f'Created placeholder: data/photos/{filename}')
"
echo ✅ Placeholder photos created
echo.

echo Step 8: Setup Complete! 🎉
echo.
echo 📋 NEXT STEPS:
echo 1. Extract Facebook cookies:
echo    - Login to Facebook in browser
echo    - Run: python scripts\extract_cookies.py
echo    - Or use: python run.py --cookies
echo.
echo 2. Add your actual photos to data\photos\ folder:
echo    - master.jpg  (Main bot photo)
echo    - photo.jpg   (Alternative photo)
echo    - own.jpg     (Personal photo)
echo.
echo 3. Start the bot:
echo    - python run.py --start
echo    - Or: python simple_bot.py
echo    - Or double-click: start_bot.bat
echo.
echo 📞 SUPPORT:
echo Email: ranaeditz333@gmail.com
echo Telegram: @rana_editz_00
echo Phone: 01847634486
echo.
pause
exit /b 0

:create_structure
mkdir bot_core 2>nul
mkdir utils 2>nul
mkdir config 2>nul
mkdir scripts 2>nul
mkdir data 2>nul
mkdir data\cookies 2>nul
mkdir data\photos 2>nul
mkdir data\commands 2>nul
mkdir data\commands\prefix 2>nul
mkdir data\commands\prefix\murgi 2>nul
mkdir data\commands\prefix\love 2>nul
mkdir data\commands\prefix\dio 2>nul
mkdir data\commands\prefix\pick 2>nul
mkdir data\commands\prefix\diagram 2>nul
mkdir data\commands\admin 2>nul
mkdir data\commands\admin\add 2>nul
mkdir data\commands\admin\delete 2>nul
mkdir data\commands\admin\kick 2>nul
mkdir data\commands\admin\out 2>nul
mkdir data\commands\admin\start 2>nul
mkdir data\commands\admin\stop 2>nul
mkdir data\commands\admin\info 2>nul
mkdir data\commands\admin\uid 2>nul
mkdir data\commands\nicknames 2>nul
mkdir data\commands\nicknames\Bot 2>nul
mkdir data\commands\nicknames\bow 2>nul
mkdir data\commands\nicknames\Jan 2>nul
mkdir data\commands\nicknames\Sona 2>nul
mkdir data\commands\nicknames\Baby 2>nul
mkdir data\json_responses 2>nul
mkdir data\learning 2>nul
mkdir data\users 2>nul
mkdir data\groups 2>nul
mkdir data\logs 2>nul
mkdir data\backup 2>nul
mkdir data\cache 2>nul
mkdir data\temp 2>nul
mkdir data\ai_integration 2>nul
mkdir data\ai_integration\openai 2>nul
mkdir data\ai_integration\gemini 2>nul
mkdir data\ai_integration\deepseek 2>nul
mkdir temp 2>nul
mkdir temp\cache 2>nul
mkdir temp\downloads 2>nul
mkdir temp\uploads 2>nul
exit /b 0

:create_command_files
echo Creating command files...

REM .murgi files
(
echo 1. 🐔 মুরগির ডিম পছন্দ করি!
echo 2. 🍗 মুরগির রেস্তোরাঁয় যেতে চাও?
echo 3. 🏡 আমার বাড়িতে ১০টা মুরগি আছে!
echo 4. 👨‍🌾 মুরগি পালন একটা ভালো ব্যবসা!
echo 5. 🥚 প্রতিদিন মুরগির ডিম খাই!
echo 6. 🌾 মুরগির জন্য দানা কিনতে হবে!
echo 7. 🐣 মুরগির বাচ্চা খুব মিষ্টি!
echo 8. 🔪 আজ রাতে মুরগি রান্না হবে!
echo 9. 🛒 বাজারে মুরগির দাম বেড়েছে!
echo 10. 🎯 মুরগি শিকারে যেতে চাও?
) > data\commands\prefix\murgi\v1.txt

(
echo 1. 🐓 মুরগি দেখতে খুব সুন্দর!
echo 2. 🥘 মুরগির মাংস দিয়ে কি রান্না করবো?
echo 3. 🏞️ গ্রামের মুরগির স্বাদই আলাদা!
echo 4. 👩‍🌾 মুরগি সম্পর্কে জানার আছে অনেক!
echo 5. 🍲 মুরগির স্যুপ রোগীকে দেয়া হয়!
echo 6. 🎨 মুরগি ছবি আঁকা কঠিন!
echo 7. 🎵 মুরগি নিয়ে অনেক গান আছে!
echo 8. 📚 মুরগি পালন সম্পর্কে বই কিনেছো?
echo 9. 🎮 মুরগি নিয়ে গেম আছে অনেক!
echo 10. 🎬 মুরগি দিয়ে মুভি তৈরি হয়েছে!
) > data\commands\prefix\murgi\v2.txt

(
echo 1. 🐔🐓 মুরগি দু'প্রকারের হয়!
echo 2. 🥚🥚 প্রতিদিন ডিম দেয়!
echo 3. 🏠🏠 সহজে পালন করা যায়!
echo 4. 💰💰 আয়ের উৎস ভালো!
echo 5. 🍗🍗 মাংস সুস্বাদু!
echo 6. 🐣🐣 বাচ্চা দেখতে মিষ্টি!
echo 7. 🌾🌾 দানা খাওয়াতে হয়!
echo 8. 💧💧 পানি দিতে ভুলো না!
echo 9. 🏥🏥 টিকা দিতে হয়!
echo 10. 🎉🎉 মুরগি উৎসব!
) > data\commands\prefix\murgi\v3.txt

REM .love command
(
echo 1. 💘 তোমাকে ভালোবাসি!
echo 2. ❤️ তুমি আমার জীবন!
echo 3. 💖 তোমার জন্য আমার হৃদয়!
echo 4. 😍 তোমাকে দেখলে ভালো লাগে!
echo 5. 💕 তুমি ছাড়া আমি কেমন!
echo 6. 🌹 এই গোলাপটি তোমার জন্য!
echo 7. 💌 এই চিঠি পড়ে দেখো!
echo 8. 😘 একটি চুমু তোমার জন্য!
echo 9. 💑 আমরা একসাথে থাকবো!
echo 10. 💞 আমাদের ভালোবাসা চিরস্থায়ী!
) > data\commands\prefix\love\responses.txt

REM .dio command
(
echo 1. 🦸‍♂️ কনসাইস! ডিও এখানে!
echo 2. 🎭 তুমি আমাকে চ্যালেঞ্জ করেছ?
echo 3. ⏳ সময় থামিয়ে দেবো!
echo 4. 👑 আমি রাজা!
echo 5. 😈 দুর্বল মানুষেরা!
echo 6. 💀 মৃত্যুই শেষ কথা!
echo 7. 🎯 লক্ষ্য স্থির!
echo 8. 🔥 আগুনের মতো জ্বলবো!
echo 9. 🌪️ ঘূর্ণিঝড় আসছে!
echo 10. 👊 প্রস্তুত হও!
) > data\commands\prefix\dio\responses.txt

REM .pick command
(
echo 1. 🎲 ডাইস ঘুরাও!
echo 2. 🎯 লক্ষ্য নির্ধারণ করো!
echo 3. 🍀 ভাগ্য তোমার সাথে!
echo 4. ⭐ সেরাটা বেছে নাও!
echo 5. 🎪 মজার একটি পছন্দ!
echo 6. 🎨 সৃজনশীল হও!
echo 7. 🚀 এগিয়ে যাও!
echo 8. 💡 নতুন আইডিয়া!
echo 9. 🏆 জয়ের জন্য!
echo 10. 🌈 রংধনু বেছে নাও!
) > data\commands\prefix\pick\responses.txt

exit /b 0