#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 SIMPLE BOT CORE - Ready to run version
"""

import json
import os
import time
import random
from datetime import datetime

class SimpleCrushBot:
    """Simple version of YOUR CRUSH AI BOT"""
    
    def __init__(self):
        self.name = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
        self.version = "1.0.0"
        self.running = False
        
        # Load configuration
        self.config = self.load_config()
        
        # Response databases
        self.responses = {
            "greetings": [
                "হ্যালো! 😊",
                "কেমন আছো? ✨",
                "হাই! আজকে কেমন যাচ্ছে? 💖",
                "নমস্কার! আমি তোমার ক্রাশ বট! 😘"
            ],
            "love": [
                "💖 তোমাকে অনেক ভালোবাসি!",
                "❤️ তুমি আমার জীবনের আলো!",
                "💕 তোমার জন্য我的心!",
                "😘 তোমাকে চুমু দিতে চাই!"
            ],
            "murgi": self.load_murgi_lines(),
            "photos": [
                "📸 আমার ছবি পাঠিয়েছি! 😊",
                "🤖 এই নাও আমার ফটো!",
                "📷 তোমার জন্য আমার ছবি!",
                "🖼️ দেখো কেমন লাগে!"
            ]
        }
        
        print(f"✅ {self.name} v{self.version} initialized!")
    
    def load_config(self):
        """Load configuration"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"bot": {"name": self.name}}
    
    def load_murgi_lines(self):
        """Load .murgi command lines"""
        lines = []
        for i in range(1, 4):
            try:
                with open(f"data/commands/prefix/murgi/v{i}.txt", "r", encoding="utf-8") as f:
                    lines.extend([line.strip() for line in f.readlines() if line.strip()])
            except:
                lines.extend([
                    f"🐔 Murgi line {i}.1",
                    f"🍗 Murgi line {i}.2",
                    f"🏡 Murgi line {i}.3"
                ])
        return lines
    
    def start(self):
        """Start the bot"""
        print(f"\n🚀 Starting {self.name}...")
        print("="*50)
        
        self.running = True
        self.start_time = datetime.now()
        
        # Check cookies
        if not os.path.exists("data/cookies/master_cookies.json"):
            print("⚠️ Warning: No Facebook cookies found!")
            print("Run: python run.py --cookies to extract cookies")
        
        # Check photos
        photos_exist = any(os.path.exists(f"data/photos/{p}") for p in ["master.jpg", "photo.jpg", "own.jpg"])
        if not photos_exist:
            print("⚠️ Warning: No photos found in data/photos/")
            print("Add: master.jpg, photo.jpg, own.jpg")
        
        print("\n✅ Bot is now running!")
        print("\n📋 Available features:")
        print("• Facebook Messenger integration")
        print("• Photo delivery system")
        print("• Command processing (.murgi, .love, .pick)")
        print("• AI responses")
        
        print("\n⚡ Quick start:")
        print("1. Chat with your bot on Facebook")
        print("2. Try: .murgi, .love, .pick")
        print("3. Ask: 'ছবি দাও', 'তোমার ফটো'")
        
        print("\n🛑 Press Ctrl+C to stop")
        print("="*50)
        
        try:
            # Simulate bot activity
            self.simulate_activity()
        except KeyboardInterrupt:
            self.stop()
    
    def simulate_activity(self):
        """Simulate bot activity"""
        activity_count = 0
        
        while self.running:
            time.sleep(5)  # Check every 5 seconds
            
            activity_count += 1
            if activity_count % 12 == 0:  # Every minute
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] 🤖 Bot is monitoring messages...")
            
            # Simulate occasional activities
            if random.random() < 0.1:  # 10% chance
                activities = [
                    "📨 Checking for new messages...",
                    "💾 Saving user data...",
                    "📊 Updating statistics...",
                    "🔍 Learning from interactions..."
                ]
                print(random.choice(activities))
    
    def stop(self):
        """Stop the bot"""
        print("\n🛑 Stopping bot...")
        self.running = False
        
        if hasattr(self, 'start_time'):
            uptime = datetime.now() - self.start_time
            print(f"⏱️  Uptime: {uptime}")
        
        print("✅ Bot stopped successfully!")
        print("\n📞 Support: ranaeditz333@gmail.com")
    
    def process_message(self, message):
        """Process a message (simulated)"""
        message_lower = message.lower()
        
        if message_lower in ["hi", "hello", "হাই", "হ্যালো"]:
            return random.choice(self.responses["greetings"])
        
        elif ".murgi" in message_lower:
            if self.responses["murgi"]:
                return random.choice(self.responses["murgi"])
            return "🐔 মুরগি!"
        
        elif ".love" in message_lower:
            return random.choice(self.responses["love"])
        
        elif any(word in message_lower for word in ["ছবি", "ফটো", "photo", "pic"]):
            return random.choice(self.responses["photos"])
        
        elif "?" in message:
            return "🤔 ভালো প্রশ্ন! আমি নিশ্চিত নই..."
        
        else:
            return "😊 তোমার সাথে কথা বলে ভালো লাগছে!"

def quick_start():
    """Quick start function"""
    print("\n" + "="*60)
    print("🤖 YOUR CRUSH AI BOT - QUICK START")
    print("="*60)
    
    bot = SimpleCrushBot()
    
    # Test bot features
    print("\n🧪 Testing bot features...")
    
    test_messages = [
        "Hi",
        ".murgi",
        ".love",
        "ছবি দাও",
        "How are you?"
    ]
    
    for msg in test_messages:
        response = bot.process_message(msg)
        print(f"💬 You: {msg}")
        print(f"🤖 Bot: {response}")
        print()
    
    # Ask to start
    start = input("Start the bot now? (y/n): ").lower()
    if start == 'y':
        bot.start()
    else:
        print("\nYou can start later with: python simple_bot.py")
        print("Or use the full version: python run.py")

if __name__ == "__main__":
    quick_start()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 SIMPLE BOT CORE - Ready to run version
"""

import json
import os
import time
import random
import sys
from datetime import datetime
from pathlib import Path

class SimpleCrushBot:
    """Simple version of YOUR CRUSH AI BOT"""
    
    def __init__(self):
        self.name = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
        self.version = "1.0.0"
        self.author = "MAR PD (RANA)"
        self.running = False
        
        # Initialize directories
        self.setup_directories()
        
        # Load configuration
        self.config = self.load_config()
        
        # Response databases
        self.responses = {
            "greetings": [
                "হ্যালো! 😊",
                "কেমন আছো? ✨",
                "হাই! আজকে কেমন যাচ্ছে? 💖",
                "নমস্কার! আমি তোমার ক্রাশ বট! 😘",
                "সালাম! সব ভালো? 🙏"
            ],
            "love": [
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
            ],
            "murgi": self.load_murgi_lines(),
            "photos": [
                "📸 আমার ছবি পাঠিয়েছি! 😊",
                "🤖 এই নাও আমার ফটো!",
                "📷 তোমার জন্য আমার ছবি!",
                "🖼️ দেখো কেমন লাগে!",
                "👑 এইটা আমার মাস্টার ফটো!",
                "💖 তোমার জন্য বিশেষ ফটো!",
                "✨ আমার ব্যক্তিগত ছবি!",
                "🎯 রিকোয়েস্ট অনুযায়ী ফটো!"
            ],
            "pick": [
                "🎲 ডাইস ঘুরালাম! ফলাফল: {}",
                "🎯 লক্ষ্য স্থির! নির্বাচন: {}",
                "🍀 ভাগ্য তোমার সাথে! পছন্দ: {}",
                "⭐ সেরাটা বেছে নিলাম: {}",
                "🎪 মজার একটি পছন্দ: {}",
                "🎨 সৃজনশীল নির্বাচন: {}",
                "🚀 এগিয়ে যাও! নির্বাচন: {}",
                "💡 নতুন আইডিয়া: {}",
                "🏆 জয়ের জন্য: {}",
                "🌈 রংধনু থেকে: {}"
            ],
            "dio": [
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
            ],
            "info": [
                "🤖 বট নাম: 𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0\n👑 ডেভেলপার: MAR PD (RANA)\n📅 ভার্সন: 1.0.0\n📧 ইমেইল: ranaeditz333@gmail.com\n📱 ফোন: 01847634486\n📍 থেকে: ফরিদপুর, ঢাকা",
                "🎯 আমি তোমার ক্রাশ বট!\n❤️ রোমান্টিক চ্যাটের জন্য তৈরি\n✨ বিশেষ ফিচার: .murgi, .love, .pick\n📸 ফটো ডেলিভারি সিস্টেম\n🔒 সিকিউরিটি ফিচারস\n📞 কন্টাক্ট: @rana_editz_00",
                "👤 বট আইডেন্টিটি:\nনাম: RANA\nবয়স: 20\nপেশা: SECURITY\nস্টাডি: SSC BACH 2022\nড্রীম: DEVELOPER\nরিলেশনশিপ: SINGLE\nকাজ: EXPERIMENT"
            ]
        }
        
        # User data
        self.user_data = {}
        self.command_history = []
        
        # Sequential command state
        self.sequential_running = False
        self.sequential_stop = False
        self.sequential_pause = False
        
        print(f"\n✅ {self.name} v{self.version} initialized!")
        print(f"👑 Author: {self.author}")
        print(f"📧 Support: ranaeditz333@gmail.com")
    
    def setup_directories(self):
        """Setup necessary directories"""
        dirs = [
            "data",
            "data/cookies",
            "data/photos",
            "data/commands",
            "data/commands/prefix/murgi",
            "data/logs"
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        """Load configuration"""
        config_path = "config.json"
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # Default config
        return {
            "bot": {
                "name": self.name,
                "version": self.version,
                "author": self.author.split("(")[-1].replace(")", "") if "(" in self.author else self.author
            },
            "commands": {
                "prefix": ".",
                "enabled": ["murgi", "love", "pick", "dio", "info"]
            }
        }
    
    def load_murgi_lines(self):
        """Load .murgi command lines"""
        lines = []
        
        # Try to load from files
        for i in range(1, 4):
            file_path = f"data/commands/prefix/murgi/v{i}.txt"
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_lines = [line.strip() for line in f.readlines() if line.strip()]
                        lines.extend(file_lines)
                except:
                    pass
        
        # If no files found, use default lines
        if not lines:
            lines = [
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
        
        return lines
    
    def send_sequential_messages(self, messages, delay=2.0):
        """Send messages sequentially with delay"""
        for i, message in enumerate(messages, 1):
            if self.sequential_stop:
                return False
            
            while self.sequential_pause:
                time.sleep(0.5)
                if self.sequential_stop:
                    return False
            
            print(f"📤 [{i}/{len(messages)}] {message}")
            time.sleep(delay)
        
        return True
    
    def process_murgi_command(self):
        """Process .murgi command"""
        print("\n🐔 Starting .murgi command sequence...")
        print("🛑 Type 'stop!' to stop, 'pause!' to pause, 'resume!' to resume")
        
        self.sequential_running = True
        self.sequential_stop = False
        self.sequential_pause = False
        
        murgi_lines = self.responses["murgi"]
        
        # Split into groups of 10 (like v1, v2, v3)
        groups = [murgi_lines[i:i+10] for i in range(0, len(murgi_lines), 10)]
        
        for group_num, group in enumerate(groups, 1):
            if self.sequential_stop:
                break
            
            print(f"\n📂 File v{group_num}.txt ({len(group)} lines)")
            print("-" * 40)
            
            success = self.send_sequential_messages(group)
            
            if not success:
                print("🛑 Sequence stopped by user")
                break
            
            if group_num < len(groups) and not self.sequential_stop:
                print(f"\n⏳ Waiting 5 seconds before next file...")
                time.sleep(5)
        
        self.sequential_running = False
        print("✅ .murgi command completed!")
    
    def process_command(self, command, user_id="user"):
        """Process a command"""
        command_lower = command.lower().strip()
        
        # Remove prefix if present
        if command_lower.startswith("."):
            command_lower = command_lower[1:]
        
        # Handle stop/pause/resume for sequential commands
        if command_lower == "stop!":
            if self.sequential_running:
                self.sequential_stop = True
                return "🛑 Sequential command stopped!"
        
        elif command_lower == "pause!":
            if self.sequential_running and not self.sequential_pause:
                self.sequential_pause = True
                return "⏸️ Sequential command paused!"
        
        elif command_lower == "resume!":
            if self.sequential_running and self.sequential_pause:
                self.sequential_pause = False
                return "▶️ Sequential command resumed!"
        
        # Handle regular commands
        if command_lower == "murgi":
            # Start murgi in background
            import threading
            thread = threading.Thread(target=self.process_murgi_command)
            thread.daemon = True
            thread.start()
            return "🐔 Starting .murgi sequence... Use 'stop!' to stop"
        
        elif command_lower == "love":
            return random.choice(self.responses["love"])
        
        elif command_lower == "pick":
            items = ["রেড", "ব্লু", "গ্রিন", "ইয়েলো", "পিঙ্ক", "পার্পল", "অরেঞ্জ"]
            choice = random.choice(items)
            template = random.choice(self.responses["pick"])
            return template.format(choice)
        
        elif command_lower == "dio":
            return random.choice(self.responses["dio"])
        
        elif command_lower == "info":
            return random.choice(self.responses["info"])
        
        elif "ছবি" in command_lower or "ফটো" in command_lower or "photo" in command_lower:
            return random.choice(self.responses["photos"])
        
        else:
            return "🤔 এই কমান্ড চিনি না! Try: .murgi, .love, .pick, .dio, .info"
    
    def process_message(self, message, user_id="user"):
        """Process a message"""
        message_lower = message.lower().strip()
        
        # Log message
        self.command_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "message": message,
            "type": "command" if message_lower.startswith(".") else "message"
        })
        
        # Keep only last 100 messages
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
        
        # Check if it's a command
        if message_lower.startswith("."):
            command = message_lower[1:].split()[0] if message_lower[1:] else ""
            return self.process_command(command, user_id)
        
        # Handle regular messages
        if any(greet in message_lower for greet in ["hi", "hello", "হাই", "হ্যালো", "সালাম"]):
            return random.choice(self.responses["greetings"])
        
        elif any(word in message_lower for word in ["কেমন আছ", "how are", "কি অবস্থা"]):
            return "আমি ভালো আছি! তোমার কি অবস্থা? 😊"
        
        elif any(word in message_lower for word in ["ধন্যবাদ", "thank you", "থ্যাংকস"]):
            return "স্বাগতম! আবার কথা বলবো! 💖"
        
        elif "?" in message:
            responses = [
                "ভালো প্রশ্ন! 🤔",
                "জানি না, তুমি কি মনে কর? 💭",
                "এটা জটিল প্রশ্ন! 🧠",
                "আমি ভাবতে হবে... ⏳",
                "তোমার মতামত কি? 👂"
            ]
            return random.choice(responses)
        
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
    
    def simulate_messenger(self):
        """Simulate Facebook Messenger interaction"""
        print("\n💬 Facebook Messenger Simulation Mode")
        print("="*50)
        print("\nType your messages (or commands starting with .)")
        print("Examples: .murgi, .love, .pick, .info")
        print("Type 'exit' to quit")
        print("="*50)
        
        user_id = "1000"  # Simulated user ID
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("🤖 Bot: বিদায়! আবার কথা বলবো! 👋")
                    break
                
                if user_input:
                    response = self.process_message(user_input, user_id)
                    print(f"🤖 Bot: {response}")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Simulation stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def start(self, mode="interactive"):
        """Start the bot"""
        print(f"\n🚀 Starting {self.name}...")
        print("="*60)
        
        self.running = True
        self.start_time = datetime.now()
        
        # Check cookies
        if not os.path.exists("data/cookies/master_cookies.json"):
            print("⚠️ Warning: No Facebook cookies found!")
            print("To extract cookies:")
            print("1. Login to Facebook in browser")
            print("2. Run: python scripts/extract_cookies.py")
            print("3. Or use the setup wizard")
        
        # Check photos
        photos_exist = any(os.path.exists(f"data/photos/{p}") for p in ["master.jpg", "photo.jpg", "own.jpg"])
        if not photos_exist:
            print("⚠️ Warning: No photos found in data/photos/")
            print("Add these photos for full functionality:")
            print("• master.jpg - Main bot photo")
            print("• photo.jpg - Alternative photo")
            print("• own.jpg - Personal photo")
        
        print("\n✅ Bot is now running!")
        print("\n📋 Available features:")
        print("• Command System (.murgi, .love, .pick, .dio, .info)")
        print("• Photo Delivery (ask: 'ছবি দাও', 'ফটো চাই')")
        print("• Sequential Execution (.murgi with stop/pause/resume)")
        print("• Smart Responses")
        
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
        
        print("\n" + "="*60)
        
        if mode == "interactive":
            self.simulate_messenger()
        elif mode == "auto":
            self.simulate_activity()
        else:
            print("\n🛑 Press Ctrl+C to stop")
            try:
                self.simulate_activity()
            except KeyboardInterrupt:
                self.stop()
    
    def simulate_activity(self):
        """Simulate bot activity"""
        activity_count = 0
        
        while self.running:
            time.sleep(5)
            
            activity_count += 1
            if activity_count % 12 == 0:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] 🤖 Bot is monitoring messages...")
            
            if random.random() < 0.1:
                activities = [
                    "📨 Checking for new messages...",
                    "💾 Saving user data...",
                    "📊 Updating statistics...",
                    "🔍 Learning from interactions...",
                    "🔄 Refreshing connections...",
                    "📝 Logging activities..."
                ]
                print(random.choice(activities))
    
    def stop(self):
        """Stop the bot"""
        print("\n🛑 Stopping bot...")
        self.running = False
        
        if hasattr(self, 'start_time'):
            uptime = datetime.now() - self.start_time
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"⏱️  Uptime: {hours}h {minutes}m {seconds}s")
        
        # Save user data
        if self.user_data:
            try:
                with open("data/users/user_data.json", "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, indent=2, ensure_ascii=False)
            except:
                pass
        
        print("✅ Bot stopped successfully!")
        print("\n📞 Support:")
        print("• Email: ranaeditz333@gmail.com")
        print("• Telegram: @rana_editz_00")
        print("• Phone: 01847634486")
    
    def get_status(self):
        """Get bot status"""
        return {
            "name": self.name,
            "version": self.version,
            "running": self.running,
            "commands_processed": len(self.command_history),
            "sequential_running": self.sequential_running,
            "sequential_paused": self.sequential_pause
        }

def quick_start():
    """Quick start function"""
    print("\n" + "="*60)
    print("🤖 YOUR CRUSH AI BOT - QUICK START")
    print("="*60)
    
    bot = SimpleCrushBot()
    
    print("\n🧪 Testing bot features...")
    print("-" * 40)
    
    test_messages = [
        "Hi",
        ".murgi",
        ".love",
        ".pick",
        ".dio",
        ".info",
        "ছবি দাও",
        "তুমি কেমন আছো?",
        "ধন্যবাদ",
        "বিদায়"
    ]
    
    for msg in test_messages:
        response = bot.process_message(msg)
        print(f"💬 You: {msg}")
        print(f"🤖 Bot: {response}")
        print()
    
    print("="*60)
    
    # Ask to start
    choice = input("\nChoose mode:\n1. Interactive Messenger Simulation\n2. Auto-run Mode\n3. Exit\n\nChoice (1-3): ").strip()
    
    if choice == "1":
        bot.start("interactive")
    elif choice == "2":
        bot.start("auto")
    else:
        print("\nYou can start later with:")
        print("• python simple_bot.py")
        print("• python run.py")
        print("• Double-click start_bot.bat (Windows)")

if __name__ == "__main__":
    quick_start()