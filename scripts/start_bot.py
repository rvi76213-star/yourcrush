#!/usr/bin/env python3
"""
🚀 বট শুরু করার স্ক্রিপ্ট
এই স্ক্রিপ্টটি YOUR CRUSH AI বট শুরু করে
"""

import os
import sys
import json
import time
import signal
import subprocess
from datetime import datetime
import threading

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.master_bot import MasterBot
from utils.logger import setup_logger
from utils.file_handler import ensure_directories

class BotStarter:
    def __init__(self):
        self.logger = setup_logger('bot_starter')
        self.bot = None
        self.running = False
        self.pid_file = 'temp/bot.pid'
        
    def check_prerequisites(self):
        """সকল প্রয়োজনীয় ফাইল এবং ডিরেক্টরি চেক করুন"""
        
        prerequisites = {
            'config/bot_config.py': 'বট কনফিগারেশন ফাইল',
            'data/cookies/master_cookies.json': 'কুকি ফাইল',
            'bot_core/master_bot.py': 'মাস্টার বট ফাইল',
            'azan/azan_config.json': 'আজান কনফিগারেশন'
        }
        
        missing = []
        for file, description in prerequisites.items():
            if not os.path.exists(file):
                missing.append(f"{description} ({file})")
        
        if missing:
            self.logger.error("নিম্নলিখিত ফাইল গুলো খুঁজে পাওয়া যায়নি:")
            for item in missing:
                self.logger.error(f"  - {item}")
            return False
        
        # প্রয়োজনীয় ডিরেক্টরি তৈরি করুন
        required_dirs = [
            'temp',
            'temp/cache',
            'temp/downloads',
            'temp/uploads',
            'logs',
            'backup'
        ]
        
        for directory in required_dirs:
            os.makedirs(directory, exist_ok=True)
        
        return True
    
    def load_config(self):
        """কনফিগারেশন লোড করুন"""
        try:
            # বট কনফিগারেশন
            sys.path.insert(0, 'config')
            from bot_config import BOT_CONFIG
            
            # আজান কনফিগারেশন
            with open('azan/azan_config.json', 'r', encoding='utf-8') as f:
                azan_config = json.load(f)
            
            # মেইন কনফিগারেশন
            with open('azan/config.json', 'r', encoding='utf-8') as f:
                main_config = json.load(f)
            
            return {
                'bot': BOT_CONFIG,
                'azan': azan_config,
                'main': main_config
            }
        except Exception as e:
            self.logger.error(f"কনফিগারেশন লোড করতে সমস্যা: {e}")
            return None
    
    def save_pid(self):
        """প্রক্রিয়া আইডি সেভ করুন"""
        pid = os.getpid()
        with open(self.pid_file, 'w') as f:
            f.write(str(pid))
        self.logger.info(f"PID সেভ করা হয়েছে: {pid}")
    
    def remove_pid(self):
        """PID ফাইল মুছুন"""
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
            self.logger.info("PID ফাইল মুছে ফেলা হয়েছে")
    
    def check_running(self):
        """চেক করুন যে বট ইতিমধ্যে চলছে কিনা"""
        if os.path.exists(self.pid_file):
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # চেক করুন প্রক্রিয়াটি সক্রিয় আছে কিনা
                os.kill(pid, 0)
                return True
            except (OSError, ValueError):
                # প্রক্রিয়াটি সক্রিয় নয়
                self.remove_pid()
        
        return False
    
    def setup_signal_handlers(self):
        """সিগন্যাল হ্যান্ডলার সেটআপ করুন"""
        def signal_handler(signum, frame):
            self.logger.info(f"সিগন্যাল পেয়েছে: {signum}")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # উইন্ডোজে SIGBREAK সাপোর্ট
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, signal_handler)
    
    def start_bot_core(self):
        """বট কোর শুরু করুন"""
        try:
            self.logger.info("মাস্টার বট শুরু হচ্ছে...")
            
            # কনফিগারেশন লোড করুন
            config = self.load_config()
            if not config:
                self.logger.error("কনফিগারেশন লোড করতে পারেনি")
                return False
            
            # মাস্টার বট তৈরি করুন
            self.bot = MasterBot(config)
            
            # বট শুরু করুন
            success = self.bot.start()
            
            if success:
                self.logger.info("মাস্টার বট সফলভাবে শুরু হয়েছে")
                self.running = True
                return True
            else:
                self.logger.error("মাস্টার বট শুরু করতে পারেনি")
                return False
                
        except Exception as e:
            self.logger.error(f"বট শুরু করতে ত্রুটি: {e}")
            return False
    
    def monitor_bot(self):
        """বট মনিটর করুন"""
        while self.running:
            try:
                # বটের স্ট্যাটাস চেক করুন
                if self.bot and hasattr(self.bot, 'is_alive'):
                    if not self.bot.is_alive():
                        self.logger.warning("বট স্টপ হয়ে গেছে, পুনরায় শুরু হচ্ছে...")
                        self.bot.start()
                
                # সিস্টেম রিসোর্স চেক করুন
                self.check_system_resources()
                
                # 30 সেকেন্ড অপেক্ষা করুন
                time.sleep(30)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"মনিটরিং ত্রুটি: {e}")
                time.sleep(60)
    
    def check_system_resources(self):
        """সিস্টেম রিসোর্স চেক করুন"""
        try:
            import psutil
            
            # CPU ব্যবহার
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 80:
                self.logger.warning(f"CPU ব্যবহার বেশি: {cpu_percent}%")
            
            # মেমোরি ব্যবহার
            memory = psutil.virtual_memory()
            if memory.percent > 85:
                self.logger.warning(f"মেমোরি ব্যবহার বেশি: {memory.percent}%")
            
            # ডিস্ক ব্যবহার
            disk = psutil.disk_usage('.')
            if disk.percent > 90:
                self.logger.warning(f"ডিস্ক স্পেস কম: {disk.percent}%")
                
        except ImportError:
            # psutil না থাকলে শুধু লগ
            pass
        except Exception as e:
            self.logger.debug(f"রিসোর্স চেক ত্রুটি: {e}")
    
    def start(self):
        """বট শুরু করুন"""
        
        # প্রিন্ট ব্যানার
        self.print_banner()
        
        # চেক করুন বট ইতিমধ্যে চলছে কিনা
        if self.check_running():
            self.logger.error("বট ইতিমধ্যে চলছে!")
            return False
        
        # প্রয়োজনীয়তা চেক করুন
        if not self.check_prerequisites():
            self.logger.error("প্রয়োজনীয় ফাইল গুলো খুঁজে পাওয়া যায়নি!")
            return False
        
        # কনফিগারেশন লোড করুন
        config = self.load_config()
        if not config:
            return False
        
        # সিগন্যাল হ্যান্ডলার সেটআপ করুন
        self.setup_signal_handlers()
        
        # PID সেভ করুন
        self.save_pid()
        
        # বট শুরু করুন
        if not self.start_bot_core():
            self.remove_pid()
            return False
        
        # মনিটরিং থ্রেড শুরু করুন
        monitor_thread = threading.Thread(target=self.monitor_bot, daemon=True)
        monitor_thread.start()
        
        self.logger.info("বট সফলভাবে শুরু হয়েছে! Ctrl+C চাপলে বন্ধ হবে")
        
        # মূল থ্রেড চালু রাখুন
        try:
            while self.running and self.bot and self.bot.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("বন্ধ করার নির্দেশ পেয়েছে")
        
        # পরিষ্কার করুন
        self.stop()
        return True
    
    def stop(self):
        """বট বন্ধ করুন"""
        self.logger.info("বট বন্ধ করা হচ্ছে...")
        
        # বট স্টপ করুন
        if self.bot:
            try:
                self.bot.stop()
            except Exception as e:
                self.logger.error(f"বট স্টপ করতে ত্রুটি: {e}")
        
        # PID ফাইল মুছুন
        self.remove_pid()
        
        self.running = False
        self.logger.info("বট সফলভাবে বন্ধ হয়েছে")
    
    def print_banner(self):
        """শুরুতে ব্যানার প্রিন্ট করুন"""
        banner = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║      🚀 YOUR CRUSH AI BOT - STARTING SYSTEM         ║
║                                                      ║
║       Version: 2.0.0       Developer: MAR PD        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def show_status(self):
        """বটের অবস্থা দেখান"""
        if self.check_running():
            print("✅ বট বর্তমানে চলছে")
            
            # আরো তথ্য দেখান
            try:
                with open(self.pid_file, 'r') as f:
                    pid = f.read().strip()
                print(f"📊 PID: {pid}")
                
                # আপটাইম চেক করুন
                if os.path.exists('logs/bot_activity.log'):
                    import subprocess
                    result = subprocess.run(
                        ['tail', '-n', '5', 'logs/bot_activity.log'],
                        capture_output=True, text=True
                    )
                    print("📝 সর্বশেষ লগ:")
                    print(result.stdout)
            except:
                pass
        else:
            print("❌ বট বর্তমানে চলছে না")
    
    def restart(self):
        """বট রিস্টার্ট করুন"""
        self.logger.info("বট পুনরায় শুরু করা হচ্ছে...")
        self.stop()
        time.sleep(2)
        return self.start()

def main():
    """মেইন ফাংশন"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YOUR CRUSH AI বট শুরু করুন')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'],
                       nargs='?', default='start',
                       help='কর্ম (ডিফল্ট: start)')
    parser.add_argument('--daemon', action='store_true',
                       help='ডেমন মোডে চলুক')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='বিশদ লগ দেখান')
    parser.add_argument('--config', '-c', default='config/bot_config.py',
                       help='কনফিগারেশন ফাইল পাথ')
    
    args = parser.parse_args()
    
    # লগ লেভেল সেট করুন
    if args.verbose:
        os.environ['LOG_LEVEL'] = 'DEBUG'
    
    starter = BotStarter()
    
    if args.action == 'start':
        if args.daemon:
            # ডেমন মোডে চলুক
            import daemon
            with daemon.DaemonContext():
                starter.start()
        else:
            starter.start()
    
    elif args.action == 'stop':
        starter.stop()
    
    elif args.action == 'restart':
        starter.restart()
    
    elif args.action == 'status':
        starter.show_status()

if __name__ == "__main__":
    main()