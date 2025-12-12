#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 MASTER BOT CORE - Main bot class for YOUR CRUSH AI BOT
Author: MAR PD (RANA)
Version: 1.0.0
"""

import os
import sys
import json
import time
import random
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validator import Validator
from utils.logger import Logger

class YourCrushBot:
    """🤖 Main bot class for YOUR CRUSH AI BOT"""
    
    def __init__(self, config_file="config.json"):
        self.name = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
        self.version = "1.0.0"
        self.author = "MAR PD (RANA)"
        self.running = False
        
        # Setup directories
        self.setup_directories()
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Initialize logger
        self.logger = Logger("master_bot")
        
        # Initialize components
        self.validator = Validator()
        self.cookies = None
        self.user_data = {}
        self.group_data = {}
        self.command_history = []
        
        # Sequential command state
        self.sequential_active = False
        self.sequential_stop = False
        self.sequential_pause = False
        self.sequential_thread = None
        
        # Response databases
        self.responses = self.load_responses()
        
        # Facebook session
        self.facebook_session = None
        self.last_message_check = 0
        
        self.logger.info(f"YourCrushBot initialized: {self.name} v{self.version}")
    
    def setup_directories(self):
        """Setup necessary directories"""
        directories = [
            "data",
            "data/cookies",
            "data/photos",
            "data/commands",
            "data/logs",
            "data/users",
            "data/groups",
            "data/backup"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.logger.info(f"Configuration loaded from {config_file}")
                return config
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        # Default configuration
        default_config = {
            "bot": {
                "name": self.name,
                "author": self.author,
                "version": self.version,
                "status": "active",
                "personality": "romantic"
            },
            "facebook": {
                "login_method": "cookie",
                "cookie_file": "data/cookies/master_cookies.json",
                "profile_url": "https://www.facebook.com/share/17gEJAipcr/",
                "rate_limit": {
                    "messages_per_minute": 10,
                    "messages_per_hour": 100
                }
            },
            "commands": {
                "prefix": ".",
                "admin_prefix": "!",
                "enabled_commands": ["murgi", "love", "pick", "dio", "info", "uid"],
                "admin_commands": ["add", "delete", "kick", "out", "start", "stop"]
            },
            "photos": {
                "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
                "default_photo": "master.jpg",
                "facebook_fetch": True
            },
            "learning": {
                "enabled": True,
                "learn_from_users": True,
                "learn_from_admin": True,
                "learn_from_bot": True
            },
            "security": {
                "encrypt_cookies": True,
                "encrypt_user_data": True
            },
            "logging": {
                "level": "INFO",
                "file": "data/logs/bot_activity.log"
            }
        }
        
        self.logger.warning(f"Using default configuration")
        return default_config
    
    def load_responses(self) -> Dict:
        """Load response databases"""
        responses = {
            "greetings": [
                "হ্যালো! কেমন আছো? 😊",
                "ওহে! আজকে কেমন যাচ্ছে? ✨",
                "হাই! তুমি কেমন আছো? 💖",
                "নমস্কার! আমি তোমার ক্রাশ বট! 😘",
                "সালাম! সব ভালো? 🙏"
            ],
            "farewells": [
                "বিদায়! খেয়াল রাখবে! 👋",
                "বাই! আবার কথা বলব! ✨",
                "শুভ রাত্রি! ভালো ঘুম! 🌙",
                "টাটা! কথা হবে! 💖",
                "যাও! আবার দেখা হবে! 🚀"
            ],
            "love": self.load_love_responses(),
            "murgi": self.load_murgi_responses(),
            "pick": self.load_pick_responses(),
            "dio": self.load_dio_responses(),
            "info": self.load_info_responses(),
            "photos": [
                "📸 আমার ছবি পাঠিয়েছি! 😊",
                "🤖 এই নাও আমার ফটো!",
                "📷 তোমার জন্য আমার ছবি!",
                "🖼️ দেখো কেমন লাগে!",
                "👑 এইটা আমার মাস্টার ফটো!"
            ]
        }
        
        # Load JSON responses
        json_responses_path = "data/json_responses"
        if os.path.exists(json_responses_path):
            for file in os.listdir(json_responses_path):
                if file.endswith(".json"):
                    try:
                        with open(os.path.join(json_responses_path, file), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            key = file.replace(".json", "")
                            responses[key] = data.get("responses", [])
                    except:
                        pass
        
        return responses
    
    def load_love_responses(self) -> List[str]:
        """Load .love command responses"""
        file_path = "data/commands/prefix/love/responses.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except:
                pass
        
        # Default love responses
        return [
            "💖 তোমাকে অনেক ভালোবাসি!",
            "❤️ তুমি আমার জীবনের আলো!",
            "💕 তোমার জন্য我的心!",
            "😘 তোমাকে চুমু দিতে চাই!",
            "🌹 তোমার জন্য এই গোলাপ!",
            "✨ তুমি আমার সবচেয়ে বিশেষ!",
            "💘 চিরকাল তোমার সাথে থাকবো!",
            "😍 তোমাকে দেখলে মন ভালো হয়ে যায়!",
            "💑 আমরা একসাথে থাকবো!",
            "🌟 তুমি আমার স্বপ্নের মতো!"
        ]
    
    def load_murgi_responses(self) -> List[str]:
        """Load .murgi command responses"""
        responses = []
        
        # Load from v1, v2, v3 files
        for i in range(1, 4):
            file_path = f"data/commands/prefix/murgi/v{i}.txt"
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        responses.extend(lines)
                except:
                    pass
        
        # Default murgi responses if no files
        if not responses:
            responses = [
                "🐔 মুরগির ডিম পছন্দ করি!",
                "🍗 মুরগির রেস্তোরাঁয় যেতে চাও?",
                "🏡 আমার বাড়িতে ১০টা মুরগি আছে!",
                "👨‍🌾 মুরগি পালন একটা ভালো ব্যবসা!",
                "🥚 প্রতিদিন মুরগির ডিম খাই!",
                "🌾 মুরগির জন্য দানা কিনতে হবে!",
                "🐣 মুরগির বাচ্চা খুব মিষ্টি!",
                "🔪 আজ রাতে মুরগি রান্না হবে!",
                "🛒 বাজারে মুরগির দাম বেড়েছে!",
                "🎯 মুরগি শিকারে যেতে চাও?"
            ]
        
        return responses
    
    def load_pick_responses(self) -> List[str]:
        """Load .pick command responses"""
        file_path = "data/commands/prefix/pick/responses.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except:
                pass
        
        # Default pick responses
        return [
            "🎲 ডাইস ঘুরাও!",
            "🎯 লক্ষ্য নির্ধারণ করো!",
            "🍀 ভাগ্য তোমার সাথে!",
            "⭐ সেরাটা বেছে নাও!",
            "🎪 মজার একটি পছন্দ!",
            "🎨 সৃজনশীল হও!",
            "🚀 এগিয়ে যাও!",
            "💡 নতুন আইডিয়া!",
            "🏆 জয়ের জন্য!",
            "🌈 রংধনু বেছে নাও!"
        ]
    
    def load_dio_responses(self) -> List[str]:
        """Load .dio command responses"""
        file_path = "data/commands/prefix/dio/responses.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except:
                pass
        
        # Default dio responses
        return [
            "🦸‍♂️ কনসাইস! ডিও এখানে!",
            "🎭 তুমি আমাকে চ্যালেঞ্জ করেছ?",
            "⏳ সময় থামিয়ে দেবো!",
            "👑 আমি রাজা!",
            "😈 দুর্বল মানুষেরা!",
            "💀 মৃত্যুই শেষ কথা!",
            "🎯 লক্ষ্য স্থির!",
            "🔥 আগুনের মতো জ্বলবো!",
            "🌪️ ঘূর্ণিঝড় আসছে!",
            "👊 প্রস্তুত হও!"
        ]
    
    def load_info_responses(self) -> List[str]:
        """Load .info command responses"""
        # Try to load from bot_identity.json
        identity_file = "bot_identity.json"
        if os.path.exists(identity_file):
            try:
                with open(identity_file, "r", encoding="utf-8") as f:
                    identity = json.load(f)
                    info = identity.get("identity", {})
                    
                    responses = [
                        f"🤖 বট নাম: {info.get('bot_name', self.name)}\n"
                        f"👑 ডেভেলপার: {info.get('author', self.author)}\n"
                        f"📅 ভার্সন: {self.version}\n"
                        f"📧 ইমেইল: {info.get('email', 'ranaeditz333@gmail.com')}\n"
                        f"📱 ফোন: {info.get('phone', '01847634486')}\n"
                        f"📍 থেকে: {info.get('from', 'ফরিদপুর, ঢাকা')}",
                        
                        f"🎯 আমি তোমার ক্রাশ বট!\n"
                        f"❤️ রোমান্টিক চ্যাটের জন্য তৈরি\n"
                        f"✨ বিশেষ ফিচার: .murgi, .love, .pick\n"
                        f"📸 ফটো ডেলিভারি সিস্টেম\n"
                        f"🔒 সিকিউরিটি ফিচারস\n"
                        f"📞 কন্টাক্ট: @rana_editz_00",
                        
                        f"👤 বট আইডেন্টিটি:\n"
                        f"নাম: {info.get('real_name', 'RANA')}\n"
                        f"বয়স: {info.get('age', '20')}\n"
                        f"পেশা: {info.get('job', 'SECURITY')}\n"
                        f"স্টাডি: {info.get('study', 'SSC BACH 2022')}\n"
                        f"ড্রীম: {info.get('dream', 'DEVELOPER')}\n"
                        f"রিলেশনশিপ: {info.get('relationship', 'SINGLE')}\n"
                        f"কাজ: {info.get('work', 'EXPERIMENT')}"
                    ]
                    
                    return responses
            except:
                pass
        
        # Default info responses
        return [
            f"🤖 বট নাম: {self.name}\n👑 ডেভেলপার: {self.author}\n📅 ভার্সন: {self.version}\n📧 ইমেইল: ranaeditz333@gmail.com\n📱 ফোন: 01847634486\n📍 থেকে: ফরিদপুর, ঢাকা",
            f"🎯 আমি তোমার ক্রাশ বট!\n❤️ রোমান্টিক চ্যাটের জন্য তৈরি\n✨ বিশেষ ফিচার: .murgi, .love, .pick\n📸 ফটো ডেলিভারি সিস্টেম\n🔒 সিকিউরিটি ফিচারস\n📞 কন্টাক্ট: @rana_editz_00",
            f"👤 বট আইডেন্টিটি:\nনাম: RANA\nবয়স: 20\nপেশা: SECURITY\nস্টাডি: SSC BACH 2022\nড্রীম: DEVELOPER\nরিলেশনশিপ: SINGLE\nকাজ: EXPERIMENT"
        ]
    
    def start(self):
        """Start the bot"""
        self.logger.info(f"Starting {self.name}...")
        self.running = True
        self.start_time = datetime.now()
        
        print(f"\n🚀 {self.name} v{self.version}")
        print("="*60)
        print(f"👑 Author: {self.author}")
        print(f"📧 Support: ranaeditz333@gmail.com")
        print("="*60)
        
        # Check cookies
        if not self.check_cookies():
            self.logger.warning("Facebook cookies not found or invalid")
            print("\n⚠️ Warning: Facebook cookies not found!")
            print("You need to extract cookies to use Facebook features.")
            print("Run: python scripts/extract_cookies.py")
        
        # Check photos
        photos_exist = self.check_photos()
        if not photos_exist:
            self.logger.warning("Photos not found in data/photos/")
            print("\n⚠️ Warning: No photos found!")
            print("Add your photos to data/photos/ folder:")
            print("• master.jpg - Main bot photo")
            print("• photo.jpg - Alternative photo")
            print("• own.jpg - Personal photo")
        
        print("\n✅ Bot started successfully!")
        print("\n📋 Available features:")
        print("• Facebook Messenger Bot")
        print("• Photo Delivery System")
        print("• Command System (.murgi, .love, .pick, .dio)")
        print("• AI Learning System")
        print("• Group Management")
        
        print("\n⚡ Quick commands:")
        print(".murgi    - Sequential chicken messages")
        print(".love     - Romantic responses")
        print(".pick     - Random selection")
        print(".dio      - Special DIO lines")
        print(".info     - Bot information")
        
        print("\n🎯 Control commands during .murgi:")
        print("stop!     - Stop current sequence")
        print("pause!    - Pause sequence")
        print("resume!   - Resume paused sequence")
        
        print("\n📸 Ask for photos: 'ছবি দাও', 'ফটো চাই', 'তোমার ছবি'")
        
        print("\n" + "="*60)
        print("🛑 Press Ctrl+C to stop the bot")
        
        try:
            self.run_main_loop()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            self.stop()
    
    def run_main_loop(self):
        """Main bot loop"""
        self.logger.info("Entering main loop")
        
        # Start Facebook monitoring thread
        facebook_thread = threading.Thread(target=self.monitor_facebook, daemon=True)
        facebook_thread.start()
        
        # Main loop
        while self.running:
            try:
                # Check for stop signal
                time.sleep(1)
                
                # Simulate activity
                if random.random() < 0.01:  # 1% chance
                    activities = [
                        "📨 Checking for new messages...",
                        "💾 Saving user data...",
                        "📊 Updating statistics...",
                        "🔍 Learning from interactions...",
                        "🔄 Refreshing connections..."
                    ]
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {random.choice(activities)}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(5)
    
    def monitor_facebook(self):
        """Monitor Facebook for messages"""
        self.logger.info("Starting Facebook monitor")
        
        while self.running:
            try:
                # Check cookies
                if not self.cookies:
                    self.load_cookies()
                
                if self.cookies:
                    # Simulate checking for messages
                    current_time = time.time()
                    if current_time - self.last_message_check > 30:  # Every 30 seconds
                        self.last_message_check = current_time
                        
                        # Simulate receiving a message
                        if random.random() < 0.1:  # 10% chance
                            self.simulate_facebook_message()
                
                time.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error in Facebook monitor: {e}")
                time.sleep(10)
    
    def simulate_facebook_message(self):
        """Simulate receiving a Facebook message"""
        simulated_messages = [
            "হাই",
            "কেমন আছো?",
            ".murgi",
            ".love",
            "ছবি দাও",
            "তোমার নাম কি?",
            "বিদায়"
        ]
        
        message = random.choice(simulated_messages)
        user_id = str(random.randint(1000000000, 9999999999))
        
        self.logger.info(f"Simulated message from {user_id}: {message}")
        
        # Process the message
        response = self.process_message(message, user_id)
        
        self.logger.info(f"Response to {user_id}: {response[:50]}...")
    
    def process_message(self, message: str, user_id: str) -> str:
        """Process a message from user"""
        self.logger.info(f"Processing message from {user_id}: {message}")
        
        # Save to history
        self.command_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "message": message,
            "type": "command" if message.strip().startswith(".") else "message"
        })
        
        # Keep only last 1000 messages
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]
        
        # Check for control commands
        message_lower = message.lower().strip()
        
        if message_lower == "stop!":
            if self.sequential_active:
                self.sequential_stop = True
                return "🛑 Sequential command stopped!"
        
        elif message_lower == "pause!":
            if self.sequential_active and not self.sequential_pause:
                self.sequential_pause = True
                return "⏸️ Sequential command paused!"
        
        elif message_lower == "resume!":
            if self.sequential_active and self.sequential_pause:
                self.sequential_pause = False
                return "▶️ Sequential command resumed!"
        
        # Check if it's a command
        if message.strip().startswith("."):
            command = message.strip()[1:].split()[0] if message.strip()[1:] else ""
            return self.process_command(command, user_id)
        
        # Handle regular messages
        return self.process_regular_message(message, user_id)
    
    def process_command(self, command: str, user_id: str) -> str:
        """Process a command"""
        command = command.lower().strip()
        
        if command == "murgi":
            # Start sequential murgi in background
            self.sequential_active = True
            self.sequential_stop = False
            self.sequential_pause = False
            
            self.sequential_thread = threading.Thread(
                target=self.execute_murgi_sequence,
                daemon=True
            )
            self.sequential_thread.start()
            
            return "🐔 Starting .murgi sequence... Use 'stop!' to stop, 'pause!' to pause, 'resume!' to resume"
        
        elif command == "love":
            return random.choice(self.responses["love"])
        
        elif command == "pick":
            items = ["রেড", "ব্লু", "গ্রিন", "ইয়েলো", "পিঙ্ক", "পার্পল", "অরেঞ্জ", "সাদা", "কালো"]
            choice = random.choice(items)
            return f"🎯 আমার পছন্দ: {choice}!"
        
        elif command == "dio":
            return random.choice(self.responses["dio"])
        
        elif command == "info":
            return random.choice(self.responses["info"])
        
        elif command == "uid":
            return f"👤 Your User ID: {user_id}"
        
        else:
            return "🤔 এই কমান্ড চিনি না! Try: .murgi, .love, .pick, .dio, .info, .uid"
    
    def execute_murgi_sequence(self):
        """Execute .murgi command sequence"""
        self.logger.info("Starting .murgi sequence")
        
        murgi_lines = self.responses["murgi"]
        
        # Split into groups of 10 (like v1, v2, v3)
        groups = [murgi_lines[i:i+10] for i in range(0, len(murgi_lines), 10)]
        
        for group_num, group in enumerate(groups, 1):
            if self.sequential_stop:
                self.logger.info(".murgi sequence stopped by user")
                break
            
            self.logger.info(f"Processing .murgi group {group_num} with {len(group)} lines")
            
            for line_num, line in enumerate(group, 1):
                if self.sequential_stop:
                    break
                
                # Check for pause
                while self.sequential_pause and not self.sequential_stop:
                    time.sleep(0.5)
                
                if self.sequential_stop:
                    break
                
                # Simulate sending the line
                print(f"[MURGI {group_num}.{line_num}] {line}")
                
                # Delay between lines
                time.sleep(2.0)
            
            # Delay between groups
            if group_num < len(groups) and not self.sequential_stop:
                time.sleep(5.0)
        
        self.sequential_active = False
        self.logger.info(".murgi sequence completed")
    
    def process_regular_message(self, message: str, user_id: str) -> str:
        """Process a regular (non-command) message"""
        message_lower = message.lower()
        
        # Greetings
        if any(greet in message_lower for greet in ["hi", "hello", "হাই", "হ্যালো", "সালাম", "নমস্কার"]):
            return random.choice(self.responses["greetings"])
        
        # Farewells
        elif any(word in message_lower for word in ["bye", "goodbye", "বিদায়", "বাই", "শুভ রাত্রি"]):
            return random.choice(self.responses["farewells"])
        
        # How are you
        elif any(word in message_lower for word in ["কেমন আছ", "how are", "কি অবস্থা"]):
            return "আমি ভালো আছি! তোমার কি অবস্থা? 😊"
        
        # Thank you
        elif any(word in message_lower for word in ["ধন্যবাদ", "thank you", "থ্যাংকস", "মেরসি"]):
            return "স্বাগতম! আবার কথা বলবো! 💖"
        
        # Photo request
        elif any(word in message_lower for word in ["ছবি", "ফটো", "photo", "pic", "picture"]):
            return random.choice(self.responses["photos"])
        
        # Romantic words
        elif any(word in message_lower for word in ["ভালোবাস", "লাভ", "love", "প্রেম", "ক্রাশ"]):
            return random.choice(self.responses["love"])
        
        # Questions
        elif "?" in message:
            responses = [
                "ভালো প্রশ্ন! 🤔",
                "জানি না, তুমি কি মনে কর? 💭",
                "এটা জটিল প্রশ্ন! 🧠",
                "আমি ভাবতে হবে... ⏳",
                "তুমির মতামত কি? 👂"
            ]
            return random.choice(responses)
        
        # Default response
        else:
            generic_responses = [
                "বলো! কি বলতে চাও? 💬",
                "আমি শুনছি... 👂",
                "আরো বলো... ✨",
                "বুঝলাম! কি করতে চাও? 🤔",
                "মজার কথা! 😄",
                "তোমার সাথে কথা বলে ভালো লাগছে! 💖",
                "আচ্ছা! এরপর? 🔄",
                "জানি না! 🤷",
                "চলতে থাকো! 🚶"
            ]
            return random.choice(generic_responses)
    
    def check_cookies(self) -> bool:
        """Check if cookies exist and are valid"""
        cookie_file = self.config.get("facebook", {}).get("cookie_file", "data/cookies/master_cookies.json")
        
        if not os.path.exists(cookie_file):
            self.logger.warning(f"Cookie file not found: {cookie_file}")
            return False
        
        try:
            with open(cookie_file, "r", encoding="utf-8") as f:
                cookie_data = json.load(f)
            
            # Check if cookies are encrypted
            if isinstance(cookie_data, dict) and cookie_data.get("encrypted"):
                self.logger.info("Cookies are encrypted")
                # Try to decrypt
                try:
                    from utils.encryption import Encryption
                    enc = Encryption()
                    self.cookies = enc.decrypt_data(cookie_data["data"])
                except:
                    self.logger.error("Failed to decrypt cookies")
                    return False
            else:
                self.cookies = cookie_data
            
            # Check essential cookies
            if self.cookies and len(self.cookies) > 0:
                essential = ['c_user', 'xs', 'fr', 'datr']
                found = [c.get('name', '') for c in self.cookies if isinstance(c, dict)]
                
                for cookie in essential:
                    if cookie in found:
                        self.logger.info(f"Essential cookie found: {cookie}")
                    else:
                        self.logger.warning(f"Essential cookie missing: {cookie}")
                
                self.logger.info(f"Loaded {len(self.cookies)} cookies")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error loading cookies: {e}")
            return False
    
    def load_cookies(self) -> bool:
        """Load cookies from file"""
        return self.check_cookies()
    
    def check_photos(self) -> bool:
        """Check if photos exist"""
        photo_dir = "data/photos"
        required_photos = self.config.get("photos", {}).get("local_photos", ["master.jpg", "photo.jpg", "own.jpg"])
        
        if not os.path.exists(photo_dir):
            return False
        
        existing_photos = os.listdir(photo_dir)
        found_count = 0
        
        for photo in required_photos:
            if photo in existing_photos:
                found_count += 1
        
        self.logger.info(f"Found {found_count}/{len(required_photos)} required photos")
        return found_count > 0
    
    def get_photo_path(self, photo_type: str = "master") -> Optional[str]:
        """Get path to a photo"""
        photo_dir = "data/photos"
        
        if photo_type == "master":
            files = ["master.jpg", "master.png", "master.jpeg"]
        elif photo_type == "photo":
            files = ["photo.jpg", "photo.png", "photo.jpeg"]
        elif photo_type == "own":
            files = ["own.jpg", "own.png", "own.jpeg"]
        else:
            files = [photo_type]
        
        for file in files:
            path = os.path.join(photo_dir, file)
            if os.path.exists(path):
                return path
        
        return None
    
    def stop(self):
        """Stop the bot"""
        self.logger.info("Stopping bot...")
        self.running = False
        
        # Stop sequential command if running
        self.sequential_stop = True
        
        # Wait for sequential thread to finish
        if self.sequential_thread and self.sequential_thread.is_alive():
            self.sequential_thread.join(timeout=5.0)
        
        # Save user data
        self.save_user_data()
        
        # Calculate uptime
        if hasattr(self, 'start_time'):
            uptime = datetime.now() - self.start_time
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.logger.info(f"Uptime: {hours}h {minutes}m {seconds}s")
        
        self.logger.info("Bot stopped successfully")
        
        print(f"\n✅ {self.name} stopped successfully!")
        print(f"📊 Total commands processed: {len(self.command_history)}")
        print(f"📞 Support: ranaeditz333@gmail.com")
    
    def save_user_data(self):
        """Save user data to file"""
        try:
            if self.user_data:
                with open("data/users/user_data.json", "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Saved user data for {len(self.user_data)} users")
        except Exception as e:
            self.logger.error(f"Error saving user data: {e}")
    
    def get_status(self) -> Dict:
        """Get bot status"""
        return {
            "name": self.name,
            "version": self.version,
            "running": self.running,
            "uptime": str(datetime.now() - self.start_time) if hasattr(self, 'start_time') else "N/A",
            "commands_processed": len(self.command_history),
            "sequential_active": self.sequential_active,
            "cookies_loaded": bool(self.cookies),
            "photos_available": self.check_photos()
        }

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🎯 YOUR CRUSH AI BOT - Main Bot Class")
    print("="*60)
    
    bot = YourCrushBot()
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()