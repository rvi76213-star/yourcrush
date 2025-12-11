# ==============================================================================
# 📁 FILE 2: setup.py (First run this)
# ==============================================================================
#!/usr/bin/env python3
"""
YOUR CRUSH BOT - SETUP SCRIPT
Run this file first to setup everything
"""

import os
import json
import shutil
from pathlib import Path

def create_directory_structure():
    """Create all necessary directories"""
    print("📁 Creating directory structure...")
    
    directories = [
        # Core directories
        "bot_core",
        "utils",
        "config",
        "scripts",
        
        # Data directories
        "data",
        "data/cookies",
        "data/photos",
        "data/commands",
        "data/commands/prefix",
        "data/commands/prefix/murgi",
        "data/commands/prefix/love",
        "data/commands/prefix/dio",
        "data/commands/prefix/diagram",
        "data/commands/prefix/pick",
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
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("✅ Directory structure created")

def create_config_files():
    """Create all configuration files"""
    print("\n⚙️ Creating configuration files...")
    
    # 1. Main config.json
    config = {
        "bot_settings": {
            "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
            "version": "1.0.0",
            "author": "MAR PD",
            "admin_id": "1000123456789",  # Change this to your Facebook ID
            "command_prefix": ".",
            "response_delay": 2,
            "sleep_time": 5,
            "auto_start": True,
            "learning_enabled": True,
            "ai_enabled": False
        },
        "facebook_settings": {
            "cookie_file": "data/cookies/master_cookies.json",
            "backup_cookie_file": "data/cookies/backup_cookies.json",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "timeout": 30,
            "max_retries": 3,
            "rate_limit": {
                "messages_per_minute": 20,
                "messages_per_hour": 100
            }
        },
        "photo_settings": {
            "local_photos": ["master.jpg", "master.png", "photo.jpg", "photo.png", "own.jpg", "own.png"],
            "facebook_profile": "https://www.facebook.com/share/17gEJAipcr/",
            "default_photo": "master.jpg"
        },
        "command_settings": {
            "sequential_commands": ["murgi", "love", "dio"],
            "admin_commands": ["add", "delete", "kick", "out", "start", "stop", "info", "uid"],
            "nickname_commands": ["Bot", "bow", "Jan", "Sona", "Baby", "Etc"],
            "special_commands": ["diagram", "pick", "Ln"],
            "stop_commands": ["stop!", "স্টপ!", "বন্ধ!"],
            "pause_commands": ["pause!", "পজ!", "থাম!"],
            "resume_commands": ["resume!", "চালু!", "শুরু!"]
        },
        "ai_settings": {
            "openai_enabled": False,
            "gemini_enabled": False,
            "deepseek_enabled": False,
            "local_ai_enabled": True
        },
        "security_settings": {
            "encrypt_cookies": True,
            "backup_interval": 3600,
            "auto_clean_logs": True,
            "proxy_enabled": False
        }
    }
    
    with open("config/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("  ✅ config/config.json")
    
    # 2. Bot identity
    identity = {
        "bot_name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
        "author": "MAR PD",
        "social_name": "MASTER 🪓",
        "real_name": "RANA",
        "age": 20,
        "dream": "DEVELOPER",
        "relationship": "SINGLE",
        "job": "SECURITY",
        "work": "EXPERIMENT",
        "experience": ["VIDEO EDIT", "PHOTO EDIT", "MOBILE TECHNICIAN", "BIULING", "SPAMMER"],
        "in_training": "CYBER SECURITY",
        "study": "SSC BACH 2022",
        "from": "FARIDPUR DHAKA",
        "email": "ranaeditz333@gmail.com",
        "telegram_bot": "@black_lovers1_bot",
        "telegram_profile": "@rana_editz_00",
        "telegram_channel": "https://t.me/master_account_remover_channel",
        "phone": "01847634486",
        "website": "Under Construction",
        "bio": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0 | SECURITY EXPERIMENT | DEVELOPER IN TRAINING | SINGLE & READY TO MINGLE 💘",
        "signature": ["⟵o_0", "💘", "🪓", "🔥", "✨"],
        "personality": {
            "romantic": True,
            "flirty": True,
            "helpful": True,
            "funny": True,
            "mysterious": True
        }
    }
    
    with open("config/bot_identity.json", "w", encoding="utf-8") as f:
        json.dump(identity, f, indent=2, ensure_ascii=False)
    print("  ✅ config/bot_identity.json")
    
    # 3. Command registry
    command_registry = {
        "prefix_commands": {
            ".murgi": {"type": "sequential", "category": "fun"},
            ".love": {"type": "sequential", "category": "romantic"},
            ".pick": {"type": "random", "category": "fun"},
            ".dio": {"type": "sequential", "category": "fun"},
            ".diagram": {"type": "special", "category": "utility"},
            ".info": {"type": "info", "category": "utility"},
            ".uid": {"type": "info", "category": "utility"},
            ".Ln": {"type": "special", "category": "utility"}
        },
        "admin_commands": {
            "add user @mention": {"permission": "admin", "action": "add_user"},
            "add pick": {"permission": "admin", "action": "add_pick"},
            "add(url)": {"permission": "admin", "action": "add_url"},
            "delete user @mention": {"permission": "admin", "action": "delete_user"},
            "kick @mention": {"permission": "admin", "action": "kick_user"},
            "out!": {"permission": "admin", "action": "leave_group"},
            "out!admin": {"permission": "super_admin", "action": "leave_as_admin"},
            "start! live start": {"permission": "admin", "action": "start_live"},
            "stop!": {"permission": "user", "action": "stop_command"}
        },
        "nickname_commands": {
            "Bot": {"response_type": "random", "category": "general"},
            "bow": {"response_type": "random", "category": "general"},
            "Jan": {"response_type": "random", "category": "general"},
            "Sona": {"response_type": "random", "category": "general"},
            "Baby": {"response_type": "random", "category": "romantic"},
            "Etc": {"response_type": "random", "category": "general"}
        }
    }
    
    with open("config/command_registry.json", "w", encoding="utf-8") as f:
        json.dump(command_registry, f, indent=2, ensure_ascii=False)
    print("  ✅ config/command_registry.json")

def create_command_files():
    """Create all command text files"""
    print("\n📝 Creating command files...")
    
    # 1. .murgi command files
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
    
    with open("data/commands/prefix/murgi/v1.txt", "w", encoding="utf-8") as f:
        f.write(murgi_v1)
    with open("data/commands/prefix/murgi/v2.txt", "w", encoding="utf-8") as f:
        f.write(murgi_v2)
    with open("data/commands/prefix/murgi/v3.txt", "w", encoding="utf-8") as f:
        f.write(murgi_v3)
    print("  ✅ data/commands/prefix/murgi/v1.txt, v2.txt, v3.txt")
    
    # .love command
    love_lines = """1. 💘 তোমাকে ভালোবাসি!
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
        f.write(love_lines)
    print("  ✅ data/commands/prefix/love/responses.txt")
    
    # .dio command
    dio_lines = """1. 🦸‍♂️ কনসাইস! ডিও এখানে!
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
        f.write(dio_lines)
    print("  ✅ data/commands/prefix/dio/responses.txt")
    
    # .pick command
    pick_lines = """1. 🎲 ডাইস ঘুরাও!
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
        f.write(pick_lines)
    print("  ✅ data/commands/prefix/pick/responses.txt")
    
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
        with open(f"data/commands/admin/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
    print("  ✅ All admin command files created")
    
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
        with open(f"data/commands/nicknames/{nickname}/responses.txt", "w", encoding="utf-8") as f:
            f.write(responses)
    print("  ✅ All nickname command files created")

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
                "অভিবাদন! তোমার দিনটি শুভ হোক! 🌟",
                "সালাম! কেমন আছেন? 🕌",
                "গুড মর্নিং! সুপ্রভাত! ☀️",
                "শুভ সন্ধ্যা! 🌆",
                "শুভ রাত্রি! 🌙"
            ],
            "triggers": ["hello", "hi", "hey", "নমস্কার", "হ্যালো", "সালাম", "সুপ্রভাত", "গুড", "শুভ"]
        },
        
        "farewells.json": {
            "responses": [
                "বিদায়! খেয়াল রাখবে! 👋",
                "বাই! আবার কথা বলব! ✨",
                "শুভ রাত্রি! ভালো ঘুম! 🌙",
                "টাটা! কথা হবে! 💖",
                "যাও! আবার দেখা হবে! 🚀",
                "চলে গেলেন? দ্রুত ফিরবেন! 🏃",
                "বিদায় দোস্ত! 🤝",
                "আল্লাহ হাফেজ! 🙏",
                "সাবধানে যাও! 🛡️"
            ],
            "triggers": ["bye", "goodbye", "বিদায়", "বাই", "শুভ রাত্রি", "good night", "চললাম", "যাই"]
        },
        
        "questions.json": {
            "responses": [
                "ভালো প্রশ্ন! আমার কি মনে হচ্ছে? 🤔",
                "জানি না, তুমি কি মনে কর? 💭",
                "এটা জটিল প্রশ্ন! 🔄",
                "আমি ভাবতে হবে... 🧠",
                "তোমার মতামত কি? 👂",
                "আরো তথ্য দাও! 📝",
                "একটু ভাবতে দাও... ⏳",
                "মজার প্রশ্ন! 😄",
                "আমি এখনো শিখছি! 📚"
            ],
            "triggers": ["কী", "কেন", "কিভাবে", "কখন", "কোথায়", "কে", "কি", "what", "why", "how", "when", "where", "who"]
        },
        
        "compliments.json": {
            "responses": [
                "ধন্যবাদ! তুমিও খুব সুন্দর! 💖",
                "থ্যাংকস! তোমার কথায় ভালো লাগছে! ✨",
                "ওহো! তোমার প্রশংসায় খুশি হলাম! 😊",
                "মেরসি! তোমার কথা শুনে ভালো লাগল! 🌟",
                "আহা! তোমার মতো মানুষ কম আছে! 💘",
                "কৃতজ্ঞ! তুমি খুব দয়ালু! 🙏",
                "শুকরিয়া! তোমার কথা শুনে মন ভালো হয়ে গেল! 😇",
                "অনেক ধন্যবাদ! তুমি রাজা/রানী! 👑",
                "আপনি খুব ভদ্র! 🎩"
            ],
            "triggers": ["beautiful", "handsome", "smart", "সুন্দর", "ভালো", "চমৎকার", "অসাধারণ", "Great", "Nice", "Awesome"]
        },
        
        "romantic.json": {
            "responses": [
                "তুমি আমার বিশেষ মানুষ! 💘",
                "তোমার কথা ভাবলে হাসি পায়! 😊",
                "তুমি ছাড়া জীবন অসম্পূর্ণ! 💔",
                "তোমার চোখে আকাশ দেখি! ✨",
                "তুমি আমার স্বপ্নের রানি/রাজা! 👑",
                "প্রতিটি মুহূর্ত তোমার সাথে! ⏳",
                "তোমার হাসি আমার ঔষধ! 💊",
                "তুমি আমার সবকিছু! 🌟",
                "চিরকাল তোমার সাথে! ♾️"
            ],
            "triggers": ["love", "প্রেম", "ভালোবাসা", "crush", "মিস", "মিস ইউ", "thinking", "ভালোলাগা", "রোমান্টিক"]
        },
        
        "angry.json": {
            "responses": [
                "এটা মেনে নেওয়া কঠিন! 😠",
                "আমি মন খারাপ করছি! 😞",
                "এটা ঠিক না! 🚫",
                "আমি রেগে গেছি! 🔥",
                "এটা বন্ধ করো! ✋",
                "পর্যাপ্ত হয়েছে! ⏹️",
                "আমি বিরক্ত! 😤",
                "এটা সহ্য করা যায় না! 💢",
                "দূরে যাও! 👋"
            ],
            "triggers": ["রাগ", "খারাপ", "বিরক্ত", "angry", "bad", "hate", "ঘৃণা", "অসন্তুষ্ট", "নিরাশ"]
        },
        
        "neutral.json": {
            "responses": [
                "বলো! কি বলতে চাও? 💭",
                "আমি শুনছি... 👂",
                "আরো বলো... ✨",
                "বুঝলাম! কি করতে চাও? 🤔",
                "আচ্ছা! এরপর? 🔄",
                "ঠিক আছে! 👍",
                "জানি না! 🤷",
                "মজার বিষয়! 🎭",
                "চলতে থাকো! 🚶"
            ],
            "triggers": ["ok", "আচ্ছা", "ঠিক আছে", "হুম", "তা", "then", "next", "এরপর", "আগে"]
        }
    }
    
    for filename, content in responses.items():
        with open(f"data/json_responses/{filename}", "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"  ✅ data/json_responses/{filename}")

def create_placeholder_photos():
    """Create placeholder photo files"""
    print("\n📸 Creating placeholder photos...")
    
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    photos = [
        ("master.jpg", "MASTER\n𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0", (400, 400)),
        ("photo.jpg", "PHOTO\nMAR PD", (400, 400)),
        ("own.jpg", "OWN\nRANA", (400, 400)),
        ("master.png", "MASTER\n𝗬𝗢𝗨𝗧𝗘 𝗖𝗥𝗨𝗦𝗛 ⟵o_0", (400, 400)),
        ("photo.png", "PHOTO\nMAR PD", (400, 400)),
        ("own.png", "OWN\nRANA", (400, 400))
    ]
    
    for filename, text, size in photos:
        try:
            # Create a simple image
            img = Image.new('RGB', size, color='purple')
            d = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Draw text
            d.text((size[0]//2, size[1]//2), text, fill='white', font=font, anchor='mm')
            
            # Save image
            img.save(f"data/photos/{filename}")
            print(f"  ✅ data/photos/{filename}")
            
        except Exception as e:
            print(f"  ⚠️ Could not create {filename}: {e}")
            # Create empty file as placeholder
            open(f"data/photos/{filename}", 'wb').close()

def create_init_files():
    """Create __init__.py files"""
    print("\n🐍 Creating Python package files...")
    
    init_files = [
        "bot_core/__init__.py",
        "utils/__init__.py"
    ]
    
    for init_file in init_files:
        with open(init_file, "w") as f:
            f.write('"""Package initialization"""\n')
        print(f"  ✅ {init_file}")

def create_readme():
    """Create README file"""
    print("\n📚 Creating documentation...")
    
    readme_content = """# 𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0 - Facebook Messenger Bot

## 🚀 Features
✅ **Complete Facebook Messenger Bot** - Cookie-based authentication
✅ **Sequential Command Execution** - .murgi, .love, .dio commands
✅ **Photo Delivery System** - Your photos + Facebook profile photos
✅ **AI Learning System** - Learns from users, admin, and itself
✅ **Multiple Command Types** - Prefix, admin, nickname, special commands
✅ **Stop/Pause/Resume Controls** - Full control during execution
✅ **JSON Response System** - Smart response generation
✅ **Security Features** - Encrypted cookies, rate limiting
✅ **Backup System** - Automatic data backup

## 📦 Installation
```bash
# 1. Install Python 3.8+
python --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup script
python setup.py

# 4. Extract Facebook cookies
python main.py -> Select "Extract Cookies"

# 5. Start the bot
python main.py -> Select "Start Bot"