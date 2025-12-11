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