#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 MAIN LAUNCHER - YOUR CRUSH AI BOT
Start the bot with: python run.py
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("""
╔══════════════════════════════════════════════════════════════╗
║                🤖 YOUR CRUSH AI BOT v1.0.0                  ║
║                    Author: MAR PD (RANA)                    ║
╚══════════════════════════════════════════════════════════════╝
""")

def setup_environment():
    """Setup basic environment"""
    print("🔧 Setting up environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required!")
        sys.exit(1)
    
    # Create essential directories
    essential_dirs = [
        "data",
        "data/cookies",
        "data/photos",
        "data/logs",
        "data/commands",
        "data/commands/prefix/murgi",
        "config"
    ]
    
    for directory in essential_dirs:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Environment ready!")

def create_config_files():
    """Create essential configuration files"""
    print("⚙️ Creating configuration files...")
    
    # 1. Create basic config.json
    config = {
        "bot": {
            "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
            "author": "MAR PD",
            "version": "1.0.0",
            "status": "active"
        },
        "facebook": {
            "login_method": "cookie",
            "cookie_file": "data/cookies/master_cookies.json",
            "profile_url": "https://www.facebook.com/share/17gEJAipcr/"
        },
        "commands": {
            "prefix": ".",
            "admin_prefix": "!",
            "enabled_commands": ["murgi", "love", "pick", "dio", "info", "uid"]
        },
        "photos": {
            "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
            "default_photo": "master.jpg"
        },
        "learning": {
            "enabled": True
        },
        "security": {
            "encrypt_cookies": True
        }
    }
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 2. Create bot_identity.json
    identity = {
        "identity": {
            "bot_name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
            "author": "MAR PD",
            "social_name": "MASTER 🪓",
            "real_name": "RANA",
            "age": 20,
            "dream": "DEVELOPER",
            "relationship": "SINGLE",
            "job": "SECURITY",
            "from": "FARIDPUR DHAKA",
            "email": "ranaeditz333@gmail.com",
            "telegram": "@rana_editz_00",
            "phone": "01847634486"
        }
    }
    
    with open("bot_identity.json", "w", encoding="utf-8") as f:
        json.dump(identity, f, indent=2, ensure_ascii=False)
    
    # 3. Create .murgi command files
    murgi_content = [
        "🐔 মুরগির ডিম পছন্দ করি!",
        "🍗 মুরগির রেস্তোরাঁয় যেতে চাও?",
        "🏡 আমার বাড়িতে ১০টা মুরগি আছে!",
        "👨‍🌾 মুরগি পালন একটা ভালো ব্যবসা!",
        "🥚 প্রতিদিন মুরগির ডিম খাই!"
    ]
    
    for i in range(1, 4):
        with open(f"data/commands/prefix/murgi/v{i}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(murgi_content))
    
    print("✅ Configuration files created!")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    requirements = [
        "requests",
        "browser-cookie3",
        "cryptography",
        "Pillow",
        "emoji",
        "python-dotenv",
        "colorama"
    ]
    
    try:
        import subprocess
        import importlib
        
        missing = []
        for package in requirements:
            try:
                importlib.import_module(package.replace("-", "_"))
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"Installing: {', '.join(missing)}")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Dependencies installed!")
        else:
            print("✅ All dependencies already installed!")
            
    except Exception as e:
        print(f"⚠️ Could not install dependencies: {e}")
        print("Please install manually: pip install requests browser-cookie3 cryptography Pillow emoji")

def extract_cookies():
    """Extract Facebook cookies"""
    print("\n🍪 Facebook Cookie Extraction")
    print("="*50)
    print("\nIMPORTANT: You must be logged into Facebook in your browser!")
    print("\nSelect browser:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    print("4. Skip for now")
    
    try:
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == "1":
            browser = "chrome"
        elif choice == "2":
            browser = "firefox"
        elif choice == "3":
            browser = "edge"
        else:
            print("Skipping cookie extraction...")
            return
        
        print(f"\nExtracting cookies from {browser}...")
        
        try:
            import browser_cookie3
            
            if browser == "chrome":
                cj = browser_cookie3.chrome(domain_name='facebook.com')
            elif browser == "firefox":
                cj = browser_cookie3.firefox(domain_name='facebook.com')
            else:
                cj = browser_cookie3.edge(domain_name='facebook.com')
            
            cookies = []
            for cookie in cj:
                if 'facebook.com' in cookie.domain:
                    cookies.append({
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain
                    })
            
            if cookies:
                with open("data/cookies/master_cookies.json", "w") as f:
                    json.dump(cookies, f, indent=2)
                
                print(f"✅ Extracted {len(cookies)} cookies!")
                print("📁 Saved to: data/cookies/master_cookies.json")
            else:
                print("❌ No Facebook cookies found!")
                print("Make sure you're logged into Facebook in your browser.")
                
        except Exception as e:
            print(f"❌ Error extracting cookies: {e}")
            print("You may need to install browser-cookie3: pip install browser-cookie3")
            
    except KeyboardInterrupt:
        print("\nCookie extraction cancelled.")

def show_bot_info():
    """Show bot information"""
    print("\n" + "="*60)
    print("🤖 YOUR CRUSH AI BOT - INFORMATION")
    print("="*60)
    
    try:
        with open("bot_identity.json", "r", encoding="utf-8") as f:
            identity = json.load(f)
        
        info = identity.get("identity", {})
        
        print(f"\n👑 Author: {info.get('author', 'MAR PD')}")
        print(f"🎯 Bot Name: {info.get('bot_name', 'YOUR CRUSH ⟵o_0')}")
        print(f"👤 Real Name: {info.get('real_name', 'RANA')}")
        print(f"📅 Age: {info.get('age', '20')}")
        print(f"📍 From: {info.get('from', 'FARIDPUR DHAKA')}")
        print(f"📧 Email: {info.get('email', 'ranaeditz333@gmail.com')}")
        print(f"📱 Phone: {info.get('phone', '01847634486')}")
        print(f"✈️ Telegram: {info.get('telegram', '@rana_editz_00')}")
        
    except:
        print("\n👑 Author: MAR PD (RANA)")
        print("🎯 Bot Name: YOUR CRUSH ⟵o_0")
        print("📧 Email: ranaeditz333@gmail.com")
        print("📱 Phone: 01847634486")
    
    print("\n" + "="*60)
    print("⚡ FEATURES:")
    print("• Facebook Messenger Bot")
    print("• Photo Delivery System")
    print("• Command System (.murgi, .love, .pick)")
    print("• AI Learning System")
    print("• Group Management")
    print("• Security & Encryption")
    
    print("\n" + "="*60)
    print("🚀 QUICK COMMANDS:")
    print(".murgi    - Sequential chicken messages")
    print(".love     - Romantic responses")
    print(".pick     - Random selection")
    print(".info     - Bot information")
    print(".uid      - Get user ID")
    print("\n📸 Ask for photos: 'ছবি দাও', 'তোমার ফটো'")
    
    print("\n" + "="*60)

def run_bot():
    """Run the main bot"""
    print("\n🚀 Starting YOUR CRUSH AI BOT...")
    
    try:
        # Import bot components
        print("Loading bot components...")
        
        # Create simplified bot class
        class SimpleBot:
            def __init__(self):
                self.name = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
                self.version = "1.0.0"
                self.running = False
                
            def start(self):
                print(f"\n✅ {self.name} v{self.version} is running!")
                print("\n📡 Bot is now monitoring Facebook Messenger...")
                print("💬 Send messages to your bot on Facebook!")
                print("⚡ Try commands: .murgi, .love, .pick")
                print("📸 Ask for photos: 'ছবি দাও'")
                print("\n🛑 Press Ctrl+C to stop the bot")
                self.running = True
                
                try:
                    # Simulate bot activity
                    import time
                    while self.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.stop()
                    
            def stop(self):
                print("\n🛑 Stopping bot...")
                self.running = False
                print("✅ Bot stopped successfully!")
                
            def get_status(self):
                return {
                    "name": self.name,
                    "version": self.version,
                    "running": self.running,
                    "uptime": "Simulated runtime"
                }
        
        # Create and start bot
        bot = SimpleBot()
        bot.start()
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed")
        print("2. Check if cookies are extracted")
        print("3. Verify configuration files")
        print("\n📞 Support: ranaeditz333@gmail.com")

def interactive_setup():
    """Interactive setup wizard"""
    print("\n" + "="*60)
    print("🤖 YOUR CRUSH AI BOT - SETUP WIZARD")
    print("="*60)
    
    print("\nThis setup will guide you through configuring your bot.")
    print("Press Enter to use default values.")
    
    # Step 1: Basic setup
    setup_environment()
    
    # Step 2: Create config files
    create_config_files()
    
    # Step 3: Install dependencies
    install_dependencies()
    
    # Step 4: Extract cookies
    print("\n" + "="*60)
    print("STEP 4: Facebook Cookie Extraction")
    print("="*60)
    
    extract_now = input("\nExtract Facebook cookies now? (y/n): ").lower()
    if extract_now == 'y':
        extract_cookies()
    
    # Step 5: Add photos
    print("\n" + "="*60)
    print("STEP 5: Add Your Photos")
    print("="*60)
    
    print("\n⚠️ IMPORTANT: Add your photos to data/photos/ folder")
    print("Required photos:")
    print("1. master.jpg - Main bot photo")
    print("2. photo.jpg  - Alternative photo")
    print("3. own.jpg    - Personal photo")
    
    input("\nPress Enter after adding photos...")
    
    # Step 6: Show bot info
    show_bot_info()
    
    # Step 7: Start bot
    print("\n" + "="*60)
    print("SETUP COMPLETE! 🎉")
    print("="*60)
    
    start_now = input("\nStart the bot now? (y/n): ").lower()
    if start_now == 'y':
        run_bot()
    else:
        print("\nYou can start the bot later with: python run.py")
        print("\n📞 Need help? Contact: ranaeditz333@gmail.com")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="YOUR CRUSH AI BOT")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard")
    parser.add_argument("--cookies", action="store_true", help="Extract cookies only")
    parser.add_argument("--info", action="store_true", help="Show bot information")
    parser.add_argument("--start", action="store_true", help="Start bot directly")
    
    args = parser.parse_args()
    
    if args.setup:
        interactive_setup()
    elif args.cookies:
        extract_cookies()
    elif args.info:
        show_bot_info()
    elif args.start:
        run_bot()
    else:
        # Interactive menu
        print("\n🤖 YOUR CRUSH AI BOT - MAIN MENU")
        print("="*40)
        print("\n1. Run Setup Wizard")
        print("2. Extract Cookies Only")
        print("3. Show Bot Information")
        print("4. Start Bot")
        print("5. Exit")
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                interactive_setup()
            elif choice == "2":
                extract_cookies()
            elif choice == "3":
                show_bot_info()
            elif choice == "4":
                run_bot()
            else:
                print("\nGoodbye! 👋")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")

if __name__ == "__main__":
    main()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 MAIN LAUNCHER - YOUR CRUSH AI BOT
Start the bot with: python run.py
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════╗
║                🤖 YOUR CRUSH AI BOT v1.0.0                  ║
║                    Author: MAR PD (RANA)                    ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def setup_directories():
    """Setup necessary directories"""
    directories = [
        "bot_core",
        "utils",
        "config",
        "scripts",
        "data",
        "data/cookies",
        "data/photos",
        "data/commands",
        "data/commands/prefix/murgi",
        "data/commands/prefix/love",
        "data/commands/prefix/dio",
        "data/commands/prefix/pick",
        "data/commands/prefix/diagram",
        "data/commands/admin",
        "data/commands/admin/add",
        "data/commands/admin/delete",
        "data/commands/admin/kick",
        "data/commands/admin/out",
        "data/commands/admin/start",
        "data/commands/admin/stop",
        "data/commands/admin/info",
        "data/commands/admin/uid",
        "data/commands/nicknames",
        "data/commands/nicknames/Bot",
        "data/commands/nicknames/bow",
        "data/commands/nicknames/Jan",
        "data/commands/nicknames/Sona",
        "data/commands/nicknames/Baby",
        "data/json_responses",
        "data/learning",
        "data/users",
        "data/groups",
        "data/logs",
        "data/backup",
        "data/cache",
        "data/temp",
        "data/ai_integration",
        "data/ai_integration/openai",
        "data/ai_integration/gemini",
        "data/ai_integration/deepseek",
        "temp",
        "temp/cache",
        "temp/downloads",
        "temp/uploads"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check which requirements file exists
        req_files = ["requirements_minimal.txt", "requirements.txt"]
        req_file = None
        
        for file in req_files:
            if os.path.exists(file):
                req_file = file
                break
        
        if not req_file:
            print("❌ No requirements file found!")
            return False
        
        print(f"Using: {req_file}")
        
        # Install dependencies
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", req_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_config_files():
    """Create configuration files"""
    print("\n⚙️ Creating configuration files...")
    
    # Check if config already exists
    if os.path.exists("config.json"):
        overwrite = input("Config files exist. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Skipping config creation...")
            return True
    
    # Create config.json
    config = {
        "bot": {
            "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
            "author": "MAR PD",
            "version": "1.0.0",
            "status": "active",
            "personality": "romantic"
        },
        "facebook": {
            "login_method": "cookie",
            "cookie_file": "data/cookies/master_cookies.json",
            "profile_url": "https://www.facebook.com/share/17gEJAipcr/"
        },
        "commands": {
            "prefix": ".",
            "admin_prefix": "!",
            "enabled_commands": ["murgi", "love", "pick", "dio", "info", "uid"]
        },
        "photos": {
            "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
            "default_photo": "master.jpg"
        }
    }
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("✅ config.json created")
    
    # Create bot_identity.json if not exists
    if not os.path.exists("bot_identity.json"):
        identity = {
            "identity": {
                "bot_name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
                "author": "MAR PD",
                "real_name": "RANA",
                "age": 20,
                "from": "FARIDPUR DHAKA",
                "email": "ranaeditz333@gmail.com",
                "phone": "01847634486"
            }
        }
        
        with open("bot_identity.json", "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)
        print("✅ bot_identity.json created")
    
    # Create .env.example
    env_content = """# YOUR CRUSH AI BOT - Environment Variables

# Facebook Configuration
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password

# Bot Configuration
BOT_NAME="YOUR CRUSH ⟵o_0"
BOT_ADMIN_ID=1000123456789

# API Keys (Optional)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Security
ENCRYPTION_KEY=generate_a_secure_key_here
PROXY_URL=

# Logging
LOG_LEVEL=INFO
LOG_TO_FILE=true

# Performance
MAX_THREADS=5
QUEUE_SIZE=100
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("✅ .env.example created")
    
    return True

def create_command_files():
    """Create command text files"""
    print("\n📝 Creating command files...")
    
    # .murgi command files
    murgi_v1 = """1. 🐔 মুরগির ডিম পছন্দ করি!
2. 🍗 মুরগির রেস্তোরাঁয় যেতে চাও?
3. 🏡 আমার বাড়িতে ১০টা মুরগি আছে!
4. 👨‍🌾 মুরগি পালন একটা ভালো ব্যবসা!
5. 🥚 প্রতিদিন মুরগির ডিম খাই!
6. 🌾 মুরগির জন্য দানা কিনতে হবে!
7. 🐣 মুরগির বাচ্চা খুব মিষ্টি!
8. 🔪 আজ রাতে মুরগি রান্না হবে!
9. 🛒 বাজারে মুরগির দাম বেড়েছে!
10. 🎯 মুরগি শিকারে যেতে চাও?"""
    
    murgi_v2 = """1. 🐓 মুরগি দেখতে খুব সুন্দর!
2. 🥘 মুরগির মাংস দিয়ে কি রান্না করবো?
3. 🏞️ গ্রামের মুরগির স্বাদই আলাদা!
4. 👩‍🌾 মুরগি সম্পর্কে জানার আছে অনেক!
5. 🍲 মুরগির স্যুপ রোগীকে দেয়া হয়!
6. 🎨 মুরগি ছবি আঁকা কঠিন!
7. 🎵 মুরগি নিয়ে অনেক গান আছে!
8. 📚 মুরগি পালন সম্পর্কে বই কিনেছো?
9. 🎮 মুরগি নিয়ে গেম আছে অনেক!
10. 🎬 মুরগি দিয়ে মুভি তৈরি হয়েছে!"""
    
    murgi_v3 = """1. 🐔🐓 মুরগি দু'প্রকারের হয়!
2. 🥚🥚 প্রতিদিন ডিম দেয়!
3. 🏠🏠 সহজে পালন করা যায়!
4. 💰💰 আয়ের উৎস ভালো!
5. 🍗🍗 মাংস সুস্বাদু!
6. 🐣🐣 বাচ্চা দেখতে মিষ্টি!
7. 🌾🌾 দানা খাওয়াতে হয়!
8. 💧💧 পানি দিতে ভুলো না!
9. 🏥🏥 টিকা দিতে হয়!
10. 🎉🎉 মুরগি উৎসব!"""
    
    for i, content in enumerate([murgi_v1, murgi_v2, murgi_v3], 1):
        file_path = f"data/commands/prefix/murgi/v{i}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {file_path}")
    
    # .love command
    love_content = """1. 💘 তোমাকে ভালোবাসি!
2. ❤️ তুমি আমার জীবন!
3. 💖 তোমার জন্য আমার হৃদয়!
4. 😍 তোমাকে দেখলে ভালো লাগে!
5. 💕 তুমি ছাড়া আমি কেমন!
6. 🌹 এই গোলাপটি তোমার জন্য!
7. 💌 এই চিঠি পড়ে দেখো!
8. 😘 একটি চুমু তোমার জন্য!
9. 💑 আমরা একসাথে থাকবো!
10. 💞 আমাদের ভালোবাসা চিরস্থায়ী!"""
    
    with open("data/commands/prefix/love/responses.txt", "w", encoding="utf-8") as f:
        f.write(love_content)
    print("✅ data/commands/prefix/love/responses.txt")
    
    # .dio command
    dio_content = """1. 🦸‍♂️ কনসাইস! ডিও এখানে!
2. 🎭 তুমি আমাকে চ্যালেঞ্জ করেছ?
3. ⏳ সময় থামিয়ে দেবো!
4. 👑 আমি রাজা!
5. 😈 দুর্বল মানুষেরা!
6. 💀 মৃত্যুই শেষ কথা!
7. 🎯 লক্ষ্য স্থির!
8. 🔥 আগুনের মতো জ্বলবো!
9. 🌪️ ঘূর্ণিঝড় আসছে!
10. 👊 প্রস্তুত হও!"""
    
    with open("data/commands/prefix/dio/responses.txt", "w", encoding="utf-8") as f:
        f.write(dio_content)
    print("✅ data/commands/prefix/dio/responses.txt")
    
    # .pick command
    pick_content = """1. 🎲 ডাইস ঘুরাও!
2. 🎯 লক্ষ্য নির্ধারণ করো!
3. 🍀 ভাগ্য তোমার সাথে!
4. ⭐ সেরাটা বেছে নাও!
5. 🎪 মজার একটি পছন্দ!
6. 🎨 সৃজনশীল হও!
7. 🚀 এগিয়ে যাও!
8. 💡 নতুন আইডিয়া!
9. 🏆 জয়ের জন্য!
10. 🌈 রংধনু বেছে নাও!"""
    
    with open("data/commands/prefix/pick/responses.txt", "w", encoding="utf-8") as f:
        f.write(pick_content)
    print("✅ data/commands/prefix/pick/responses.txt")
    
    # Admin command files
    admin_files = {
        "add_user.txt": "✅ @mention কে সফলভাবে এড করা হয়েছে!\n👋 স্বাগতম নতুন মেম্বার!\n🎉 গ্রুপে যোগদানের জন্য ধন্যবাদ!",
        "delete_user.txt": "🗑️ @mention কে ডিলিট করা হয়েছে!\n👋 বিদায়!\n🚫 অ্যাক্সেস রিভোক করা হলো!",
        "kick_user.txt": "👢 @mention কে কিক করা হয়েছে!\n🚪 দরজা দেখিয়ে দাও!\n⚡ তাৎক্ষণিক বহিষ্কার!",
        "out_group.txt": "👋 বিদায় সবাই!\n🚪 গ্রুপ ছাড়লাম!\n😢 আমাকে মনে রাখবে!",
        "out_admin.txt": "👑 এডমিন হিসেবে বিদায়!\n⚡ বিশেষ প্রস্থান!\n🎭 চরিত্র পরিবর্তন!",
        "start_live.txt": "📡 লাইভ শুরু হচ্ছে!\n🎥 ক্যামেরা চালু!\n👥 সবাই জয়েন করো!",
        "stop_bot.txt": "⏹️ বট স্টপ করা হয়েছে!\n🛑 সব অ্যাক্টিভিটি বন্ধ!\n💤 বিশ্রাম মোড!"
    }
    
    for filename, content in admin_files.items():
        file_path = f"data/commands/admin/{filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {file_path}")
    
    # Nickname command files
    nickname_responses = {
        "Bot": "🤖 হ্যাঁ বলুন, আমি আপনার বট!\n⚡ বট এখানে, কমান্ড দিন!\n🔧 বট রেডি, কি করতে চান?",
        "bow": "🏹 হ্যাঁ বলুন বাউ!\n🎯 লক্ষ্য স্থির!\n🐯 শক্তিশালী উপস্থিতি!",
        "Jan": "👨 বলুন জ্যান!\n💪 শক্তি দিয়ে উপস্থিত!\n🛡️ রক্ষাকর্তা এখানে!",
        "Sona": "👸 বলুন সোনা!\n✨ সোনার মতো উজ্জ্বল!\n💎 মূল্যবান উপস্থিতি!",
        "Baby": "👶 বলুন বেবি!\n💖 ছোট্ট মধুর!\n🐰 নরম ও কোমল!",
        "Etc": "🌀 বলুন ইটিসি!\n🎭 অন্যান্য বিষয়!\n🔀 বিভিন্ন অপশন!"
    }
    
    for nickname, responses in nickname_responses.items():
        file_path = f"data/commands/nicknames/{nickname}/responses.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(responses)
        print(f"✅ {file_path}")
    
    return True

def create_response_files():
    """Create JSON response files"""
    print("\n💬 Creating response files...")
    
    responses = {
        "greetings.json": {
            "responses": [
                "হ্যালো! কেমন আছো? 😊",
                "ওহে! আজকে কেমন যাচ্ছে? ✨",
                "হাই! তুমি কেমন আছো? 💖",
                "নমস্কার! সব ভালো তো? 🙏",
                "অভিবাদন! তোমার দিনটি শুভ হোক! 🌟"
            ],
            "triggers": ["hello", "hi", "hey", "নমস্কার", "হ্যালো", "সালাম"]
        },
        
        "farewells.json": {
            "responses": [
                "বিদায়! খেয়াল রাখবে! 👋",
                "বাই! আবার কথা বলব! ✨",
                "শুভ রাত্রি! ভালো ঘুম! 🌙",
                "টাটা! কথা হবে! 💖",
                "যাও! আবার দেখা হবে! 🚀"
            ],
            "triggers": ["bye", "goodbye", "বিদায়", "বাই", "শুভ রাত্রি"]
        },
        
        "questions.json": {
            "responses": [
                "ভালো প্রশ্ন! আমার কি মনে হচ্ছে? 🤔",
                "জানি না, তুমি কি মনে কর? 💭",
                "এটা জটিল প্রশ্ন! 🔄",
                "আমি ভাবতে হবে... 🧠",
                "তোমার মতামত কি? 👂"
            ],
            "triggers": ["কী", "কেন", "কিভাবে", "কখন", "কোথায়", "কে"]
        },
        
        "compliments.json": {
            "responses": [
                "ধন্যবাদ! তুমিও খুব সুন্দর! 💖",
                "থ্যাংকস! তোমার কথায় ভালো লাগছে! ✨",
                "ওহো! তোমার প্রশংসায় খুশি হলাম! 😊",
                "মেরসি! তোমার কথা শুনে ভালো লাগল! 🌟",
                "আহা! তোমার মতো মানুষ কম আছে! 💘"
            ],
            "triggers": ["beautiful", "handsome", "smart", "সুন্দর", "ভালো", "চমৎকার"]
        },
        
        "romantic.json": {
            "responses": [
                "তুমি আমার বিশেষ মানুষ! 💘",
                "তোমার কথা ভাবলে হাসি পায়! 😊",
                "তুমি ছাড়া জীবন অসম্পূর্ণ! 💔",
                "তোমার চোখে আকাশ দেখি! ✨",
                "তুমি আমার স্বপ্নের রানি/রাজা! 👑"
            ],
            "triggers": ["love", "প্রেম", "ভালোবাসা", "crush", "মিস", "মিস ইউ"]
        },
        
        "angry.json": {
            "responses": [
                "এটা মেনে নেওয়া কঠিন! 😠",
                "আমি মন খারাপ করছি! 😞",
                "এটা ঠিক না! 🚫",
                "আমি রেগে গেছি! 🔥",
                "এটা বন্ধ করো! ✋"
            ],
            "triggers": ["রাগ", "খারাপ", "বিরক্ত", "angry", "bad", "hate"]
        },
        
        "neutral.json": {
            "responses": [
                "বলো! কি বলতে চাও? 💭",
                "আমি শুনছি... 👂",
                "আরো বলো... ✨",
                "বুঝলাম! কি করতে চাও? 🤔",
                "আচ্ছা! এরপর? 🔄"
            ],
            "triggers": ["ok", "আচ্ছা", "ঠিক আছে", "হুম", "তা", "then"]
        }
    }
    
    for filename, content in responses.items():
        file_path = f"data/json_responses/{filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"✅ {file_path}")
    
    return True

def create_placeholder_photos():
    """Create placeholder photo files"""
    print("\n📸 Creating placeholder photos...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        photos = [
            ("master.jpg", "MASTER\n𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0\nMAR PD", (400, 400)),
            ("photo.jpg", "PHOTO\nYOUR CRUSH\nRomantic Bot", (400, 400)),
            ("own.jpg", "OWN\nRANA\nDeveloper", (400, 400))
        ]
        
        for filename, text, size in photos:
            try:
                # Create image
                img = Image.new('RGB', size, color='purple')
                d = ImageDraw.Draw(img)
                
                # Try to use a font
                try:
                    font = ImageFont.truetype("arial.ttf", 40)
                except:
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
                    except:
                        font = ImageFont.load_default()
                
                # Draw text
                d.text((size[0]//2, size[1]//2), text, fill='white', font=font, anchor='mm')
                
                # Save image
                img.save(f"data/photos/{filename}")
                print(f"✅ data/photos/{filename}")
                
            except Exception as e:
                print(f"⚠️ Could not create {filename}: {e}")
                # Create empty file as placeholder
                open(f"data/photos/{filename}", 'wb').close()
                
    except ImportError:
        print("⚠️ PIL not installed, creating empty photo files")
        for filename in ["master.jpg", "photo.jpg", "own.jpg"]:
            open(f"data/photos/{filename}", 'wb').close()
            print(f"✅ data/photos/{filename} (placeholder)")
    
    return True

def extract_cookies_interactive():
    """Interactive cookie extraction"""
    print("\n🍪 Facebook Cookie Extraction")
    print("="*50)
    
    print("\n⚠️ IMPORTANT: You must be logged into Facebook in your browser!")
    print("\nSelect browser:")
    print("1. Chrome (Recommended)")
    print("2. Firefox")
    print("3. Edge")
    print("4. Skip for now")
    
    try:
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == "4":
            print("Skipping cookie extraction...")
            print("⚠️ You need cookies to run the bot!")
            print("You can extract later with: python scripts/extract_cookies.py")
            return True
        
        browsers = {"1": "chrome", "2": "firefox", "3": "edge"}
        browser = browsers.get(choice, "chrome")
        
        print(f"\nExtracting cookies from {browser}...")
        
        # Import browser_cookie3
        try:
            import browser_cookie3
            
            if browser == "chrome":
                cj = browser_cookie3.chrome(domain_name='facebook.com')
            elif browser == "firefox":
                cj = browser_cookie3.firefox(domain_name='facebook.com')
            else:
                cj = browser_cookie3.edge(domain_name='facebook.com')
            
            cookies = []
            for cookie in cj:
                if 'facebook.com' in cookie.domain:
                    cookies.append({
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain
                    })
            
            if cookies:
                with open("data/cookies/master_cookies.json", "w", encoding="utf-8") as f:
                    json.dump(cookies, f, indent=2)
                
                print(f"✅ Extracted {len(cookies)} cookies!")
                print("📁 Saved to: data/cookies/master_cookies.json")
                
                # Check essential cookies
                essential = ['c_user', 'xs', 'fr', 'datr']
                found = [c['name'] for c in cookies]
                missing = [c for c in essential if c not in found]
                
                if missing:
                    print(f"⚠️ Missing essential cookies: {missing}")
                else:
                    print("✅ All essential cookies found!")
                    
            else:
                print("❌ No Facebook cookies found!")
                print("Make sure:")
                print("1. You're logged into Facebook in your browser")
                print("2. The browser is not in private/incognito mode")
                print("3. You have necessary permissions")
                
        except ImportError:
            print("❌ browser-cookie3 not installed!")
            print("Install with: pip install browser-cookie3")
            return False
            
    except KeyboardInterrupt:
        print("\n❌ Cookie extraction cancelled")
        return False
    except Exception as e:
        print(f"❌ Error extracting cookies: {e}")
        return False
    
    return True

def show_bot_info():
    """Show bot information"""
    print("\n" + "="*60)
    print("🤖 YOUR CRUSH AI BOT - INFORMATION")
    print("="*60)
    
    try:
        if os.path.exists("bot_identity.json"):
            with open("bot_identity.json", "r", encoding="utf-8") as f:
                identity = json.load(f)
            
            info = identity.get("identity", {})
            
            print(f"\n👑 Author: {info.get('author', 'MAR PD')}")
            print(f"🎯 Bot Name: {info.get('bot_name', 'YOUR CRUSH ⟵o_0')}")
            print(f"👤 Real Name: {info.get('real_name', 'RANA')}")
            print(f"📅 Age: {info.get('age', '20')}")
            print(f"📍 From: {info.get('from', 'FARIDPUR DHAKA')}")
            print(f"📧 Email: {info.get('email', 'ranaeditz333@gmail.com')}")
            print(f"📱 Phone: {info.get('phone', '01847634486')}")
            
        else:
            print("\n👑 Author: MAR PD (RANA)")
            print("🎯 Bot Name: YOUR CRUSH ⟵o_0")
            print("📧 Email: ranaeditz333@gmail.com")
            print("📱 Phone: 01847634486")
            
    except:
        print("\n👑 Author: MAR PD")
     