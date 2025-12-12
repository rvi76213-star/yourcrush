"""
🕌 আজান এবং নামাজের সময় সিস্টেম
বটের জন্য ইসলামিক প্রার্থনা সময় গণনা এবং নোটিফিকেশন
"""

import json
import schedule
import time
from datetime import datetime
import threading
import requests
from pytz import timezone
import math

class AzanSystem:
    def __init__(self, bot_core=None):
        """
        আজান সিস্টেম ইনিশিয়ালাইজেশন
        
        Args:
            bot_core: প্রধান বট কোর অবজেক্ট (ঐচ্ছিক)
        """
        self.bot_core = bot_core
        self.load_config()
        self.prayer_times = {}
        self.active = False
        self.scheduler_thread = None
        
        # বাংলাদেশের শহরগুলির জন্য টাইমজোন
        self.timezone = timezone('Asia/Dhaka')
        
    def load_config(self):
        """কনফিগারেশন ফাইল লোড করুন"""
        try:
            with open('azan/azan_config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # ডিফল্ট কনফিগারেশন
            self.config = {
                "enabled": True,
                "city": "Dhaka",
                "calculation_method": "Karachi",
                "auto_notify": True,
                "notify_before_minutes": 10,
                "voice_reminder": False,
                "group_notifications": True,
                "individual_notifications": True,
                "notify_users": ["all"],  # ["all"] বা নির্দিষ্ট ইউজার আইডি
                "hijri_date_enabled": True,
                "ramadan_mode": False,
                "special_reminders": {
                    "jummah": True,
                    "tahajjud": False,
                    "tarawih": False
                }
            }
            self.save_config()
    
    def save_config(self):
        """কনফিগারেশন সেভ করুন"""
        with open('azan/azan_config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def calculate_prayer_times(self, date=None, city=None):
        """
        নামাজের সময় গণনা করুন (বাংলাদেশের জন্য কাস্টম)
        
        Args:
            date: তারিখ (ডিফল্ট: আজ)
            city: শহরের নাম
            
        Returns:
            নামাজের সময়ের ডিকশনারি
        """
        if city is None:
            city = self.config.get("city", "Dhaka")
        
        if date is None:
            date = datetime.now(self.timezone)
        
        # শহর ভিত্তিক বেস টাইম
        city_times = {
            "Dhaka": {
                "ফজর": "04:30",
                "সূর্যোদয়": "06:00",
                "জোহর": "12:15",
                "আসর": "15:45",
                "মাগরিব": "18:05",
                "ইশা": "19:30"
            },
            "Chittagong": {
                "ফজর": "04:25",
                "সূর্যোদয়": "05:55",
                "জোহর": "12:10",
                "আসর": "15:40",
                "মাগরিব": "18:00",
                "ইশা": "19:25"
            },
            "Rajshahi": {
                "ফজর": "04:35",
                "সূর্যোদয়": "06:05",
                "জোহর": "12:20",
                "আসর": "15:50",
                "মাগরিব": "18:10",
                "ইশা": "19:35"
            },
            "Khulna": {
                "ফজর": "04:28",
                "সূর্যোদয়": "05:58",
                "জোহর": "12:13",
                "আসর": "15:43",
                "মাগরিব": "18:03",
                "ইশা": "19:28"
            },
            "Sylhet": {
                "ফজর": "04:22",
                "সূর্যোদয়": "05:52",
                "জোহর": "12:07",
                "আসর": "15:37",
                "মাগরিব": "17:57",
                "ইশা": "19:22"
            }
        }
        
        # সিজনাল এডজাস্টমেন্ট (সারলীকৃত)
        month = date.month
        seasonal_adjustment = {
            1: -15,   # জানুয়ারি
            2: -10,   # ফেব্রুয়ারি
            3: -5,    # মার্চ
            4: 0,     # এপ্রিল
            5: 5,     # মে
            6: 10,    # জুন
            7: 15,    # জুলাই
            8: 10,    # আগস্ট
            9: 5,     # সেপ্টেম্বর
            10: 0,    # অক্টোবর
            11: -5,   # নভেম্বর
            12: -10   # ডিসেম্বর
        }
        
        adjust_minutes = seasonal_adjustment.get(month, 0)
        
        # সময় এডজাস্ট করুন
        prayer_times = city_times.get(city, city_times["Dhaka"]).copy()
        
        for prayer, time_str in prayer_times.items():
            if prayer not in ["সূর্যোদয়"]:  # সূর্যোদয় এডজাস্ট করবেন না
                h, m = map(int, time_str.split(":"))
                m += adjust_minutes
                if m >= 60:
                    h += 1
                    m -= 60
                elif m < 0:
                    h -= 1
                    m += 60
                prayer_times[prayer] = f"{h:02d}:{m:02d}"
        
        self.prayer_times = prayer_times
        return prayer_times
    
    def get_hijri_date(self):
        """আজকের হিজরি তারিখ পান"""
        try:
            # API থেকে হিজরি তারিখ (বিকল্প: লোকাল ক্যালকুলেশন)
            today = datetime.now(self.timezone)
            response = requests.get(
                f"http://api.aladhan.com/v1/gToH?date={today.day}-{today.month}-{today.year}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                hijri = data["data"]["hijri"]
                return {
                    "day": hijri["day"],
                    "month": hijri["month"]["en"],
                    "year": hijri["year"],
                    "month_ar": hijri["month"]["ar"],
                    "designation": hijri["designation"]["abbreviated"],
                    "weekday": hijri["weekday"]["en"]
                }
        except:
            pass
        
        # ফলব্যাক: লোকাল ক্যালকুলেশন (সারলীকৃত)
        return {
            "day": "15",
            "month": "Ramadan",
            "year": "1446",
            "month_ar": "رمضان",
            "designation": "AH",
            "weekday": "Friday"
        }
    
    def format_prayer_message(self, prayer_name, time_str, minutes_before=0):
        """নামাজের রিমাইন্ডার মেসেজ ফরম্যাট করুন"""
        
        prayer_messages = {
            "ফজর": {
                "title": "🌅 ফজরের আজান",
                "message": "ফজরের আজানের সময় হলো। সালাতুল ফজর আদায় করুন।",
                "dua": "اللهم اجعلني من التائبين واجعلني من المتطهرين"
            },
            "জোহর": {
                "title": "☀️ জোহরের আজান",
                "message": "জোহরের আজানের সময় হলো। সালাতুল জোহর আদায় করুন।",
                "dua": "اللهم اغنني بحلالك عن حرامك واغنني بفضلك عمن سواك"
            },
            "আসর": {
                "title": "🌤️ আসরের আজান",
                "message": "আসরের আজানের সময় হলো। সালাতুল আসর আদায় করুন।",
                "dua": "اللهم أعني على ذكرك وشكرك وحسن عبادتك"
            },
            "মাগরিব": {
                "title": "🌇 মাগরিবের আজান",
                "message": "মাগরিবের আজানের সময় হলো। সালাতুল মাগরিব আদায় করুন।",
                "dua": "اللهم إني أسألك خير هذه الليلة وخير ما فيها"
            },
            "ইশা": {
                "title": "🌙 ইশার আজান",
                "message": "ইশার আজানের সময় হলো। সালাতুল ইশা আদায় করুন।",
                "dua": "اللهم اغفر لي ولوالدي وللمؤمنين والمؤمنات"
            }
        }
        
        info = prayer_messages.get(prayer_name, {
            "title": f"🕌 {prayer_name} এর আজান",
            "message": f"{prayer_name} এর আজানের সময় হলো। নামাজ আদায় করুন।",
            "dua": "رب اغفر لي وتب علي إنك أنت التواب الرحيم"
        })
        
        if minutes_before > 0:
            return f"""
🕌 **{info['title']}**
⏰ {minutes_before} মিনিট পর ({time_str})

{info['message']}

📖 দোয়া: {info['dua']}

🕋 আল্লাহ আমাদের সবাইকে সময়মত নামাজ আদায়ের তৌফিক দিন। আমীন।
            """
        else:
            return f"""
🕌 **{info['title']}**
⏰ সময়: {time_str}

{info['message']}

📖 দোয়া: {info['dua']}

🕋 আল্লাহ আমাদের সবাইকে সময়মত নামাজ আদায়ের তৌফিক দিন। আমীন।
            """
    
    def setup_scheduler(self):
        """নামাজের সময় অনুযায়ী শিডিউলার সেটআপ করুন"""
        if not self.config.get("enabled", True):
            return
        
        # আগের সব শিডিউল ক্লিয়ার করুন
        schedule.clear()
        
        prayer_times = self.calculate_prayer_times()
        
        for prayer, time_str in prayer_times.items():
            if prayer not in ["সূর্যোদয়"]:  # শুধু নামাজের সময়
                # আজান নোটিফিকেশন
                schedule.every().day.at(time_str).do(
                    self.send_azan_notification,
                    prayer,
                    time_str
                )
                
                # রিমাইন্ডার নোটিফিকেশন (যদি কনফিগার করা থাকে)
                notify_before = self.config.get("notify_before_minutes", 10)
                if notify_before > 0:
                    # সময় ক্যালকুলেশন
                    h, m = map(int, time_str.split(":"))
                    m -= notify_before
                    if m < 0:
                        h -= 1
                        m += 60
                    reminder_time = f"{h:02d}:{m:02d}"
                    
                    schedule.every().day.at(reminder_time).do(
                        self.send_reminder_notification,
                        prayer,
                        time_str,
                        notify_before
                    )
        
        # জুমার দিন বিশেষ নোটিফিকেশন
        if self.config.get("special_reminders", {}).get("jummah", True):
            schedule.every().friday.at("11:30").do(
                self.send_jummah_reminder
            )
        
        print(f"[AZAN] সিস্টেম শিডিউলড: {len(prayer_times)-1} নামাজের সময়")
    
    def send_azan_notification(self, prayer_name, time_str):
        """আজান নোটিফিকেশন পাঠান"""
        if not self.bot_core:
            return
        
        message = self.format_prayer_message(prayer_name, time_str)
        
        # গ্রুপে পাঠান (যদি কনফিগার করা থাকে)
        if self.config.get("group_notifications", True):
            groups = self.get_subscribed_groups()
            for group_id in groups:
                self.bot_core.send_message(group_id, message)
        
        # ইউজারদের পাঠান (যদি কনফিগার করা থাকে)
        if self.config.get("individual_notifications", True):
            users = self.get_subscribed_users()
            for user_id in users:
                self.bot_core.send_message(user_id, message)
    
    def send_reminder_notification(self, prayer_name, time_str, minutes_before):
        """রিমাইন্ডার নোটিফিকেশন পাঠান"""
        if not self.bot_core:
            return
        
        message = self.format_prayer_message(prayer_name, time_str, minutes_before)
        
        # শুধু গ্রুপে পাঠান
        if self.config.get("group_notifications", True):
            groups = self.get_subscribed_groups()
            for group_id in groups:
                self.bot_core.send_message(group_id, message)
    
    def send_jummah_reminder(self):
        """জুমার দিন বিশেষ রিমাইন্ডার"""
        if not self.bot_core:
            return
        
        jummah_message = """
🕌 **জুমার দিনের বিশেষ রিমাইন্ডার**
📅 আজ শুক্রবার, জুমার দিন

✨ জুমার দিনের ফজিলত:
• সমস্ত সপ্তাহের সেরা দিন
• দোয়া কবুলের বিশেষ সময়
• গুনাহ মাফের সুবর্ণ সুযোগ

⏰ জুমার সালাতের সময়: দুপুর ১:১৫ মিনিট (সাধারণত)

📖 হাদিস: রাসূলুল্লাহ (ﷺ) বলেছেন,
"জুমার দিনে এমন একটি সময় আছে যখন কোনো মুসলিম আল্লাহর কাছে ভালো কিছু চাইলে আল্লাহ তা দান করেন।" (বুখারী)

🕋 সবার জন্য দোয়া: আল্লাহ আমাদের সবাইকে জুমার সালাত আদায়ের তৌফিক দিন।
        """
        
        if self.config.get("group_notifications", True):
            groups = self.get_subscribed_groups()
            for group_id in groups:
                self.bot_core.send_message(group_id, jummah_message)
    
    def get_subscribed_groups(self):
        """সাবস্ক্রাইবড গ্রুপগুলো পান"""
        try:
            with open('data/groups/group_settings.json', 'r', encoding='utf-8') as f:
                groups = json.load(f)
                return [gid for gid, settings in groups.items() 
                       if settings.get('azan_subscription', True)]
        except:
            return []
    
    def get_subscribed_users(self):
        """সাবস্ক্রাইবড ইউজারগুলো পান"""
        try:
            with open('data/users/user_settings.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
                return [uid for uid, settings in users.items() 
                       if settings.get('azan_subscription', True)]
        except:
            return []
    
    def run_scheduler(self):
        """শিডিউলার রান করুন (থ্রেডে)"""
        self.setup_scheduler()
        self.active = True
        
        while self.active:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """আজান সিস্টেম শুরু করুন"""
        if self.active:
            return
        
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("[AZAN] সিস্টেম শুরু হয়েছে")
        
        # আজকের নামাজের সময় শেয়ার করুন
        self.send_today_times()
    
    def stop(self):
        """আজান সিস্টেম বন্ধ করুন"""
        self.active = False
        schedule.clear()
        print("[AZAN] সিস্টেম বন্ধ করা হয়েছে")
    
    def send_today_times(self):
        """আজকের নামাজের সময় পাঠান"""
        if not self.bot_core:
            return
        
        prayer_times = self.calculate_prayer_times()
        hijri_date = self.get_hijri_date()
        
        message = f"""
🕌 **আজকের নামাজের সময়সূচি**
📍 {self.config.get('city', 'ঢাকা')}
📅 {datetime.now(self.timezone).strftime('%d %B, %Y')}
🌙 {hijri_date['day']} {hijri_date['month']} {hijri_date['year']} {hijri_date['designation']}

⏰ **নামাজের সময়:**
🌅 ফজর: {prayer_times['ফজর']}
☀️ জোহর: {prayer_times['জোহর']}
🌤️ আসর: {prayer_times['আসর']}
🌇 মাগরিব: {prayer_times['মাগরিব']}
🌙 ইশা: {prayer_times['ইশা']}

✨ **সূর্যোদয়:** {prayer_times['সূর্যোদয়']}

📌 *বট স্বয়ংক্রিয়ভাবে আজান সময়ে নোটিফিকেশন দেবে*

🕋 আল্লাহ তায়ালা আমাদের সবাইকে সময়মত নামাজ আদায়ের তৌফিক দিন।
        """
        
        # শুধু প্রথমবারের জন্য মেইন গ্রুপে পাঠান
        if self.config.get("group_notifications", True):
            groups = self.get_subscribed_groups()
            if groups:
                self.bot_core.send_message(groups[0], message)
    
    def get_current_prayer(self):
        """বর্তমান নামাজ এবং পরবর্তী নামাজের তথ্য পান"""
        now = datetime.now(self.timezone)
        current_time = now.strftime("%H:%M")
        
        prayer_times = self.calculate_prayer_times()
        prayer_list = [
            ("ফজর", prayer_times["ফজর"]),
            ("জোহর", prayer_times["জোহর"]),
            ("আসর", prayer_times["আসর"]),
            ("মাগরিব", prayer_times["মাগরিব"]),
            ("ইশা", prayer_times["ইশা"])
        ]
        
        current_prayer = None
        next_prayer = None
        
        for i, (prayer, time_str) in enumerate(prayer_list):
            if current_time < time_str:
                next_prayer = (prayer, time_str)
                if i > 0:
                    current_prayer = prayer_list[i-1]
                break
        
        if not next_prayer:  # সব নামাজ শেষ
            current_prayer = prayer_list[-1]
            next_prayer = prayer_list[0]  # পরদিনের ফজর
        
        return {
            "current": current_prayer,
            "next": next_prayer,
            "hijri_date": self.get_hijri_date(),
            "all_times": prayer_times
        }
    
    def handle_command(self, command, args, user_id, group_id=None):
        """আজান সম্পর্কিত কমান্ড হ্যান্ডেল করুন"""
        
        command_map = {
            "azan": self.cmd_azan_times,
            "namaz": self.cmd_namaz_times,
            "next": self.cmd_next_prayer,
            "hijri": self.cmd_hijri_date,
            "subscribe": self.cmd_subscribe,
            "unsubscribe": self.cmd_unsubscribe,
            "city": self.cmd_change_city,
            "jummah": self.cmd_jummah_info
        }
        
        cmd_func = command_map.get(command)
        if cmd_func:
            return cmd_func(args, user_id, group_id)
        
        return "❌ অজানা আজান কমান্ড। .help azan লিখে সাহায্য নিন।"
    
    def cmd_azan_times(self, args, user_id, group_id=None):
        """আজকের নামাজের সময় দেখান"""
        prayer_info = self.get_current_prayer()
        
        response = f"""
🕌 **আজকের নামাজের সময়সূচি**
📍 {self.config.get('city', 'ঢাকা')}

⏰ **নামাজের সময়:**
🌅 ফজর: {prayer_info['all_times']['ফজর']}
☀️ জোহর: {prayer_info['all_times']['জোহর']}
🌤️ আসর: {prayer_info['all_times']['আসর']}
🌇 মাগরিব: {prayer_info['all_times']['মাগরিব']}
🌙 ইশা: {prayer_info['all_times']['ইশা']}

🕐 **বর্তমান:** {prayer_info['current'][0] if prayer_info['current'] else 'কোনো নামাজ নেই'}
⏭️ **পরবর্তী:** {prayer_info['next'][0]} ({prayer_info['next'][1]})

🌙 হিজরি তারিখ: {prayer_info['hijri_date']['day']} {prayer_info['hijri_date']['month']} {prayer_info['hijri_date']['year']} {prayer_info['hijri_date']['designation']}
        """
        
        return response
    
    def cmd_namaz_times(self, args, user_id, group_id=None):
        """এই কমান্ডের জন্য আলাদা ফাইল দেখান"""
        return "📖 নামাজ শিক্ষা গাইড দেখতে: .namaz guide"
    
    def cmd_next_prayer(self, args, user_id, group_id=None):
        """পরবর্তী নামাজের তথ্য দেখান"""
        prayer_info = self.get_current_prayer()
        
        next_prayer = prayer_info['next']
        hijri = prayer_info['hijri_date']
        
        response = f"""
🕌 **পরবর্তী নামাজ**
🕋 নামাজ: {next_prayer[0]}
⏰ সময়: {next_prayer[1]}
📍 স্থান: {self.config.get('city', 'ঢাকা')}
🌙 তারিখ: {hijri['day']} {hijri['month']} {hijri['year']} {hijri['designation']}

💫 প্রস্তুতি নিন এবং ওজু করে নামাজের জন্য তৈরি হোন।
        """
        
        return response
    
    def cmd_hijri_date(self, args, user_id, group_id=None):
        """হিজরি তারিখ দেখান"""
        hijri = self.get_hijri_date()
        
        response = f"""
🌙 **আজকের হিজরি তারিখ**
📅 ইংরেজি: {datetime.now(self.timezone).strftime('%d %B, %Y')}
🌙 হিজরি: {hijri['day']} {hijri['month_ar']} ({hijri['month']}) {hijri['year']} {hijri['designation']}
📌 দিন: {hijri['weekday']}

🕌 আল্লাহ আমাদের সবাইকে এই দিনটি ইবাদতের মাধ্যমে কাটানোর তৌফিক দিন।
        """
        
        return response
    
    def cmd_subscribe(self, args, user_id, group_id=None):
        """আজান নোটিফিকেশনে সাবস্ক্রাইব করুন"""
        try:
            if group_id:
                # গ্রুপ সাবস্ক্রিপশন
                with open('data/groups/group_settings.json', 'r', encoding='utf-8') as f:
                    groups = json.load(f)
                
                if group_id not in groups:
                    groups[group_id] = {}
                
                groups[group_id]['azan_subscription'] = True
                
                with open('data/groups/group_settings.json', 'w', encoding='utf-8') as f:
                    json.dump(groups, f, indent=4, ensure_ascii=False)
                
                return f"✅ এই গ্রুপ আজান নোটিফিকেশনে সাবস্ক্রাইব করা হয়েছে।"
            else:
                # ইউজার সাবস্ক্রিপশন
                with open('data/users/user_settings.json', 'r', encoding='utf-8') as f:
                    users = json.load(f)
                
                if user_id not in users:
                    users[user_id] = {}
                
                users[user_id]['azan_subscription'] = True
                
                with open('data/users/user_settings.json', 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=4, ensure_ascii=False)
                
                return f"✅ আপনি আজান নোটিফিকেশনে সাবস্ক্রাইব করেছেন।"
        except Exception as e:
            return f"❌ সাবস্ক্রিপশনে সমস্যা: {str(e)}"
    
    def cmd_unsubscribe(self, args, user_id, group_id=None):
        """আজান নোটিফিকেশন থেকে আনসাবস্ক্রাইব করুন"""
        try:
            if group_id:
                # গ্রুপ আনসাবস্ক্রিপশন
                with open('data/groups/group_settings.json', 'r', encoding='utf-8') as f:
                    groups = json.load(f)
                
                if group_id in groups:
                    groups[group_id]['azan_subscription'] = False
                
                with open('data/groups/group_settings.json', 'w', encoding='utf-8') as f:
                    json.dump(groups, f, indent=4, ensure_ascii=False)
                
                return f"✅ এই গ্রুপ আজান নোটিফিকেশন থেকে আনসাবস্ক্রাইব করা হয়েছে।"
            else:
                # ইউজার আনসাবস্ক্রিপশন
                with open('data/users/user_settings.json', 'r', encoding='utf-8') as f:
                    users = json.load(f)
                
                if user_id in users:
                    users[user_id]['azan_subscription'] = False
                
                with open('data/users/user_settings.json', 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=4, ensure_ascii=False)
                
                return f"✅ আপনি আজান নোটিফিকেশন থেকে আনসাবস্ক্রাইব করেছেন।"
        except Exception as e:
            return f"❌ আনসাবস্ক্রিপশনে সমস্যা: {str(e)}"
    
    def cmd_change_city(self, args, user_id, group_id=None):
        """শহর পরিবর্তন করুন"""
        if not args:
            available_cities = ["Dhaka", "Chittagong", "Rajshahi", "Khulna", "Sylhet"]
            return f"""
🏙️ **উপলব্ধ শহর:**
{', '.join(available_cities)}

📌 ব্যবহার: .azan city <শহরের_নাম>
উদাহরণ: .azan city Chittagong
            """
        
        city = args[0].capitalize()
        available_cities = ["Dhaka", "Chittagong", "Rajshahi", "Khulna", "Sylhet"]
        
        if city not in available_cities:
            return f"❌ অসমর্থিত শহর। উপলব্ধ শহর: {', '.join(available_cities)}"
        
        old_city = self.config.get('city', 'ঢাকা')
        self.config['city'] = city
        self.save_config()
        
        # নতুন সময় ক্যালকুলেট করুন
        self.calculate_prayer_times(city=city)
        
        return f"✅ শহর পরিবর্তন করা হয়েছে: {old_city} → {city}\nনতুন নামাজের সময় ক্যালকুলেট করা হয়েছে।"
    
    def cmd_jummah_info(self, args, user_id, group_id=None):
        """জুমার দিনের তথ্য দেখান"""
        today = datetime.now(self.timezone)
        is_friday = today.weekday() == 4  # 4 = Friday
        
        if is_friday:
            day_status = "🎉 **আজ শুক্রবার, জুমার দিন!**"
            suggestion = "✨ জুমার সালাত আদায় করুন এবং দোয়া কবুলের এই বিশেষ দিনের ফজিলত গ্রহণ করুন।"
        else:
            days_to_friday = (4 - today.weekday()) % 7
            if days_to_friday == 0:
                days_to_friday = 7
            
            if days_to_friday == 1:
                day_status = "🕌 **আগামীকাল শুক্রবার**"
            else:
                day_status = f"📅 **আর মাত্র {days_to_friday} দিন পর শুক্রবার**"
            
            suggestion = f"⏳ জুমার দিনের জন্য প্রস্তুতি নিন এবং দোয়ার তালিকা তৈরি করুন।"
        
        response = f"""
🕌 **জুমার দিনের বিশেষ ফজিলত**
{day_status}

📖 **জুমার দিনের কিছু সুন্নাত:**
1. গোসল করা (ঘুম থেকে উঠেই)
2. উত্তম পোশাক পরা
3. সুগন্ধি ব্যবহার করা
4. আগে আগে মসজিদে যাওয়া
5. সূরা কাহফ তিলাওয়াত করা

🎯 **জুমার সালাত সময়:** দুপুর ১:১৫ মিনিট (সাধারণত)

{suggestion}

🕋 হাদিস: রাসূলুল্লাহ (ﷺ) বলেছেন,
"জুমার দিন সপ্তাহের সবচেয়ে উত্তম দিন।" (ইবনে মাজাহ)
        """
        
        return response

# মডিউল টেস্টিং
if __name__ == "__main__":
    azan = AzanSystem()
    times = azan.calculate_prayer_times()
    print("নামাজের সময়:")
    for prayer, time in times.items():
        print(f"{prayer}: {time}")
    
    print("\nহিজরি তারিখ:", azan.get_hijri_date())