"""
Telegram Bot API ইন্টিগ্রেশন (ঐচ্ছিক)
"""

import telebot
import json
import os
from typing import Optional, Dict, List
import logging
from threading import Thread

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    """Telegram Bot হ্যান্ডলার"""
    
    def __init__(self, token: str = None):
        """
        Telegram Bot হ্যান্ডলার ইনিশিয়ালাইজ
        
        Args:
            token: Telegram Bot Token (ঐচ্ছিক, .env থেকে নেবে)
        """
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not self.token:
            raise ValueError("Telegram Bot Token not found. Set TELEGRAM_BOT_TOKEN in .env")
        
        self.bot = telebot.TeleBot(self.token)
        self.running = False
        
        # কমান্ড হ্যান্ডলার
        self.command_handlers = {}
        self.message_handlers = []
        
        # স্টেট ম্যানেজমেন্ট
        self.user_states = {}
        
        logger.info("Telegram Bot handler initialized")
    
    def start_polling(self):
        """বট পোলিং শুরু করুন"""
        if self.running:
            logger.warning("Bot is already running")
            return
        
        self.running = True
        
        # বেসিক কমান্ড রেজিস্টার
        self.register_basic_commands()
        
        # পোলিং থ্রেড শুরু
        polling_thread = Thread(target=self._polling_thread, daemon=True)
        polling_thread.start()
        
        logger.info("Telegram Bot polling started")
    
    def stop_polling(self):
        """বট পোলিং বন্ধ করুন"""
        self.running = False
        logger.info("Telegram Bot polling stopped")
    
    def _polling_thread(self):
        """পোলিং থ্রেড"""
        try:
            self.bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            self.running = False
    
    def register_basic_commands(self):
        """বেসিক কমান্ড রেজিস্টার করুন"""
        # /start কমান্ড
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            welcome_text = """
🤖 *Welcome to YOUR CRUSH AI BOT!* 🤖

I'm your AI-powered companion. Here's what I can do:

🎯 *Commands:*
/help - Show all commands
/chat [message] - Chat with AI
/photo - Get a photo
/prayer - Prayer times
/status - Bot status

💖 *Features:*
- AI Chat (Bangla/English)
- Photo sharing
- Prayer time notifications
- Learning from interactions

📱 *Connect:*
Facebook Messenger: @YourCrushBot
Developer: @rana_editz_00

Type /help for more info!
            """
            self.bot.reply_to(message, welcome_text, parse_mode='Markdown')
        
        # /help কমান্ড
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            help_text = """
🆘 *Available Commands:* 🆘

🤖 *Basic:*
/start - Start the bot
/help - Show this help
/status - Bot status
/settings - Bot settings

💬 *Chat:*
/chat [message] - Chat with AI
/ask [question] - Ask anything
/tell [joke/story] - Tell something

📸 *Media:*
/photo - Get a random photo
/sendphoto - Send specific photo

🕌 *Islamic:*
/prayer - Today's prayer times
/hijri - Hijri date
/azan - Next prayer time

🔧 *Admin:*
/broadcast [msg] - Broadcast message
/stats - Bot statistics
/logs - View logs

📞 *Contact:*
/contact - Contact developer
/report - Report issue
/suggest - Suggest feature

⚙️ *Settings:*
/language [en/bn] - Change language
/notifications [on/off] - Toggle notifications
/reset - Reset settings

Type command to use. Example: /chat Hello!
            """
            self.bot.reply_to(message, help_text, parse_mode='Markdown')
        
        # /chat কমান্ড
        @self.bot.message_handler(commands=['chat'])
        def handle_chat(message):
            try:
                # মেসেজ থেকে টেক্সট এক্সট্র্যাক্ট
                text = message.text.split('/chat', 1)[1].strip()
                
                if not text:
                    self.bot.reply_to(message, "Please provide a message. Example: /chat Hello!")
                    return
                
                # AI রেস্পন্স জেনারেট (এখানে আপনার AI ইন্টিগ্রেশন যোগ করুন)
                response = self.generate_ai_response(text, message.from_user.id)
                
                self.bot.reply_to(message, response)
                
            except IndexError:
                self.bot.reply_to(message, "Usage: /chat [your message]")
            except Exception as e:
                logger.error(f"Chat error: {e}")
                self.bot.reply_to(message, "Sorry, I encountered an error. Please try again.")
        
        # /photo কমান্ড
        @self.bot.message_handler(commands=['photo'])
        def handle_photo(message):
            try:
                # লোডিং মেসেজ
                self.bot.send_chat_action(message.chat.id, 'upload_photo')
                
                # ফটো পাঠান (এখানে আপনার ফটো লজিক যোগ করুন)
                photo_path = self.get_random_photo()
                
                if os.path.exists(photo_path):
                    with open(photo_path, 'rb') as photo:
                        self.bot.send_photo(message.chat.id, photo, caption="Here's your photo! 📸")
                else:
                    self.bot.reply_to(message, "Sorry, no photos available right now.")
                    
            except Exception as e:
                logger.error(f"Photo error: {e}")
                self.bot.reply_to(message, "Failed to send photo. Please try again.")
        
        # /prayer কমান্ড
        @self.bot.message_handler(commands=['prayer'])
        def handle_prayer(message):
            try:
                # আজানের সময় (এখানে আপনার আজান লজিক যোগ করুন)
                prayer_times = self.get_prayer_times()
                
                response = f"""
🕌 *Today's Prayer Times* 🕌

📍 *City:* Dhaka, Bangladesh

⏰ *Prayer Times:*
• Fajr: {prayer_times.get('fajr', '04:30')}
• Dhuhr: {prayer_times.get('dhuhr', '12:15')}
• Asr: {prayer_times.get('asr', '15:45')}
• Maghrib: {prayer_times.get('maghrib', '18:05')}
• Isha: {prayer_times.get('isha', '19:30')}

🌙 *Sunrise:* {prayer_times.get('sunrise', '06:00')}

📅 *Hijri Date:* {prayer_times.get('hijri', '15 Ramadan 1445')}

*May Allah accept our prayers.* 🤲
                """
                
                self.bot.reply_to(message, response, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"Prayer error: {e}")
                self.bot.reply_to(message, "Failed to get prayer times. Please try again.")
    
    def generate_ai_response(self, text: str, user_id: int) -> str:
        """
        AI রেস্পন্স জেনারেট করুন
        
        Args:
            text: ইউজার ইনপুট
            user_id: ইউজার আইডি
            
        Returns:
            AI রেস্পন্স
        """
        # এখানে আপনার AI ইন্টিগ্রেশন যোগ করুন
        # উদাহরণ:
        responses = [
            f"Hey! You said: {text} 😊",
            "That's interesting! Tell me more. 💫",
            "I understand. How can I help you? 🤖",
            "Great point! I'll remember that. 🧠",
            "Thanks for sharing! ❤️"
        ]
        
        import random
        return random.choice(responses)
    
    def get_random_photo(self) -> str:
        """র্যান্ডম ফটো পাথ পান"""
        # এখানে আপনার ফটো লজিক যোগ করুন
        # উদাহরণ:
        photo_dir = "data/photos/"
        
        if os.path.exists(photo_dir):
            photos = [f for f in os.listdir(photo_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if photos:
                import random
                return os.path.join(photo_dir, random.choice(photos))
        
        return "data/photos/default.jpg"
    
    def get_prayer_times(self) -> Dict:
        """আজানের সময় পান"""
        # এখানে আপনার আজান লজিক যোগ করুন
        return {
            'fajr': '04:30',
            'dhuhr': '12:15',
            'asr': '15:45',
            'maghrib': '18:05',
            'isha': '19:30',
            'sunrise': '06:00',
            'hijri': '15 Ramadan 1445'
        }
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = None):
        """
        মেসেজ পাঠান
        
        Args:
            chat_id: চ্যাট আইডি
            text: মেসেজ টেক্সট
            parse_mode: পার্স মোড (Markdown/HTML)
        """
        try:
            self.bot.send_message(chat_id, text, parse_mode=parse_mode)
            return True
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False
    
    def send_photo(self, chat_id: int, photo_path: str, caption: str = None):
        """
        ফটো পাঠান
        
        Args:
            chat_id: চ্যাট আইডি
            photo_path: ফটো পাথ
            caption: ক্যাপশন
        """
        try:
            with open(photo_path, 'rb') as photo:
                self.bot.send_photo(chat_id, photo, caption=caption)
            return True
        except Exception as e:
            logger.error(f"Send photo error: {e}")
            return False
    
    def broadcast_message(self, text: str, user_ids: List[int] = None):
        """
        ব্রডকাস্ট মেসেজ
        
        Args:
            text: মেসেজ টেক্সট
            user_ids: ইউজার আইডি লিস্ট (ঐচ্ছিক)
        """
        if user_ids is None:
            # ডাটাবেস থেকে সব ইউজার আইডি লোড করুন
            user_ids = self.get_all_user_ids()
        
        success_count = 0
        fail_count = 0
        
        for user_id in user_ids:
            try:
                self.send_message(user_id, text)
                success_count += 1
            except Exception as e:
                logger.error(f"Broadcast to {user_id} failed: {e}")
                fail_count += 1
        
        return {
            "success": success_count,
            "failed": fail_count,
            "total": success_count + fail_count
        }
    
    def get_all_user_ids(self) -> List[int]:
        """সমস্ত ইউজার আইডি পান"""
        # এখানে আপনার ডাটাবেস থেকে ইউজার আইডি লোড করুন
        # উদাহরণ:
        try:
            with open('data/telegram_users.json', 'r') as f:
                users = json.load(f)
                return [user['id'] for user in users]
        except:
            return []
    
    def get_bot_info(self) -> Dict:
        """বট তথ্য পান"""
        try:
            info = self.bot.get_me()
            return {
                "id": info.id,
                "username": info.username,
                "first_name": info.first_name,
                "is_bot": info.is_bot
            }
        except Exception as e:
            logger.error(f"Get bot info error: {e}")
            return {}

# Singleton instance
_telegram_instance = None

def get_telegram_handler(token: str = None) -> TelegramBotHandler:
    """Telegram হ্যান্ডলার ইনস্ট্যান্স পান"""
    global _telegram_instance
    
    if _telegram_instance is None:
        _telegram_instance = TelegramBotHandler(token)
    
    return _telegram_instance

# ইউটিলিটি ফাংশন
def is_telegram_available() -> bool:
    """Telegram Bot উপলব্ধ কিনা চেক করুন"""
    try:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        return bool(token and len(token) > 30)
    except:
    except:
        return False

def test_telegram_connection() -> bool:
    """Telegram কানেকশন টেস্ট"""
    try:
        handler = get_telegram_handler()
        info = handler.get_bot_info()
        return bool(info and info.get('id'))
    except:
        return False

if __name__ == "__main__":
    # টেস্ট কোড
    if is_telegram_available():
        print("✅ Telegram Bot available")
        
        handler = get_telegram_handler()
        
        # বট তথ্য
        info = handler.get_bot_info()
        print(f"Bot Info: {info}")
        
        # বট শুরু
        print("Starting bot... (Ctrl+C to stop)")
        handler.start_polling()
        
        # চালু রাখুন
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping bot...")
            handler.stop_polling()
        
    else:
        print("❌ Telegram Bot not available. Set TELEGRAM_BOT_TOKEN in .env")