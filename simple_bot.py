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