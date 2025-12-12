#!/usr/bin/env python3
"""
⏹️ বট বন্ধ করার স্ক্রিপ্ট
এই স্ক্রিপ্টটি YOUR CRUSH AI বট বন্ধ করে
"""

import os
import sys
import json
import time
import signal
import psutil
from datetime import datetime

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.logger import setup_logger

class BotStopper:
    def __init__(self):
        self.logger = setup_logger('bot_stopper')
        self.pid_file = 'temp/bot.pid'
        self.lock_file = 'temp/bot.lock'
        
    def print_banner(self):
        """শুরুতে ব্যানার প্রিন্ট করুন"""
        banner = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║      ⏹️ YOUR CRUSH AI BOT - STOPPING SYSTEM        ║
║                                                      ║
║       Version: 2.0.0       Developer: MAR PD        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def get_bot_pid(self):
        """বটের PID পান"""
        if not os.path.exists(self.pid_file):
            self.logger.error("PID ফাইল খুঁজে পাওয়া যায়নি")
            return None
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            return pid
        except (ValueError, IOError) as e:
            self.logger.error(f"PID পড়তে সমস্যা: {e}")
            return None
    
    def stop_by_pid(self, pid):
        """PID ব্যবহার করে প্রক্রিয়া বন্ধ করুন"""
        try:
            # প্রক্রিয়াটির অস্তিত্ব চেক করুন
            process = psutil.Process(pid)
            
            # প্রক্রিয়াটির তথ্য সংগ্রহ করুন
            proc_info = {
                'name': process.name(),
                'status': process.status(),
                'create_time': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent()
            }
            
            self.logger.info(f"প্রক্রিয়াটি পাওয়া গেছে: {proc_info}")
            
            # SIGTERM পাঠান (নিয়মিত বন্ধ)
            process.terminate()
            
            # 5 সেকেন্ড অপেক্ষা করুন
            time.sleep(5)
            
            if process.is_running():
                self.logger.warning("প্রক্রিয়াটি এখনও চলছে, SIGKILL পাঠানো হচ্ছে...")
                process.kill()
                time.sleep(2)
            
            # চেক করুন প্রক্রিয়াটি বন্ধ হয়েছে কিনা
            if not process.is_running():
                self.logger.info(f"প্রক্রিয়াটি সফলভাবে বন্ধ হয়েছে (PID: {pid})")
                return True
            else:
                self.logger.error(f"প্রক্রিয়াটি বন্ধ করা যায়নি (PID: {pid})")
                return False
                
        except psutil.NoSuchProcess:
            self.logger.warning(f"প্রক্রিয়াটি খুঁজে পাওয়া যায়নি (PID: {pid})")
            return True
        except psutil.AccessDenied:
            self.logger.error(f"প্রক্রিয়াটি বন্ধ করার অনুমতি নেই (PID: {pid})")
            return False
        except Exception as e:
            self.logger.error(f"প্রক্রিয়াটি বন্ধ করতে ত্রুটি: {e}")
            return False
    
    def stop_by_name(self):
        """নাম দ্বারা বট প্রক্রিয়া খুঁজে বন্ধ করুন"""
        bot_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # বট প্রক্রিয়া খুঁজুন
                cmdline = proc.info['cmdline']
                if cmdline and any('master_bot' in str(arg) for arg in cmdline):
                    bot_processes.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not bot_processes:
            self.logger.warning("কোনো বট প্রক্রিয়া খুঁজে পাওয়া যায়নি")
            return True
        
        self.logger.info(f"{len(bot_processes)} টি বট প্রক্রিয়া পাওয়া গেছে")
        
        success = True
        for pid in bot_processes:
            if not self.stop_by_pid(pid):
                success = False
        
        return success
    
    def cleanup_files(self):
        """টেম্পোরারি ফাইলগুলি মুছুন"""
        files_to_remove = [
            self.pid_file,
            self.lock_file,
            'temp/bot.lock',
            'temp/cache/bot_cache.db'
        ]
        
        dirs_to_clean = [
            'temp/cache',
            'temp/downloads',
            'temp/uploads'
        ]
        
        # ফাইল মুছুন
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.logger.info(f"ফাইল মুছে ফেলা হয়েছে: {file_path}")
                except Exception as e:
                    self.logger.warning(f"ফাইল মুছতে পারেনি {file_path}: {e}")
        
        # ডিরেক্টরি পরিষ্কার করুন (কিন্তু মুছবেন না)
        for dir_path in dirs_to_clean:
            if os.path.exists(dir_path):
                try:
                    # .tmp ফাইলগুলো মুছুন
                    for file in os.listdir(dir_path):
                        if file.endswith('.tmp') or file.endswith('.temp'):
                            os.remove(os.path.join(dir_path, file))
                    self.logger.info(f"ডিরেক্টরি পরিষ্কার করা হয়েছে: {dir_path}")
                except Exception as e:
                    self.logger.warning(f"ডিরেক্টরি পরিষ্কার করতে পারেনি {dir_path}: {e}")
        
        return True
    
    def backup_before_stop(self):
        """বন্ধ করার আগে ব্যাকআপ তৈরি করুন"""
        try:
            from utils.backup_tool import BackupTool
            
            self.logger.info("বন্ধ করার আগে ব্যাকআপ তৈরি করা হচ্ছে...")
            
            backup_tool = BackupTool()
            backup_file = backup_tool.create_backup('manual_stop')
            
            if backup_file:
                self.logger.info(f"ব্যাকআপ তৈরি করা হয়েছে: {backup_file}")
                return True
            else:
                self.logger.warning("ব্যাকআপ তৈরি করা যায়নি")
                return False
                
        except Exception as e:
            self.logger.error(f"ব্যাকআপ তৈরি করতে ত্রুটি: {e}")
            return False
    
    def stop(self, force=False):
        """বট বন্ধ করুন"""
        self.print_banner()
        
        # ব্যাকআপ তৈরি করুন (যদি জোর করে না হয়)
        if not force:
            self.backup_before_stop()
        
        # PID দ্বারা বন্ধ করার চেষ্টা করুন
        pid = self.get_bot_pid()
        if pid:
            self.logger.info(f"PID দ্বারা বট বন্ধ করা হচ্ছে: {pid}")
            success = self.stop_by_pid(pid)
        else:
            # নাম দ্বারা খুঁজে বন্ধ করুন
            self.logger.info("নাম দ্বারা বট প্রক্রিয়া খোঁজা হচ্ছে...")
            success = self.stop_by_name()
        
        # ফাইল পরিষ্কার করুন
        self.cleanup_files()
        
        # স্টপ কনফার্মেশন
        if success:
            self.logger.info("✅ বট সফলভাবে বন্ধ হয়েছে")
            print("\n" + "="*50)
            print("✅ YOUR CRUSH AI BOT সফলভাবে বন্ধ হয়েছে")
            print("="*50)
            return True
        else:
            self.logger.error("❌ বট বন্ধ করতে সমস্যা হয়েছে")
            print("\n" + "="*50)
            print("❌ বট বন্ধ করতে সমস্যা হয়েছে")
            print("জোর করে বন্ধ করতে: python stop_bot.py --force")
            print("="*50)
            return False
    
    def status(self):
        """বটের অবস্থা দেখান"""
        pid = self.get_bot_pid()
        
        if pid:
            try:
                process = psutil.Process(pid)
                
                print("\n" + "="*50)
                print("🤖 YOUR CRUSH AI BOT - STATUS")
                print("="*50)
                print(f"✅ বট বর্তমানে চলছে")
                print(f"📊 PID: {pid}")
                print(f"🏷️ নাম: {process.name()}")
                print(f"📈 অবস্থা: {process.status()}")
                print(f"🚀 শুরু হয়েছে: {datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"💻 CPU ব্যবহার: {process.cpu_percent()}%")
                print(f"💾 মেমোরি ব্যবহার: {process.memory_percent():.2f}%")
                
                # চলমান সময় গণনা করুন
                uptime_seconds = time.time() - process.create_time()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                print(f"⏱️ চলমান সময়: {hours} ঘণ্টা {minutes} মিনিট")
                
                print("="*50)
                return True
                
            except psutil.NoSuchProcess:
                print(f"\n❌ বট প্রক্রিয়াটি পাওয়া যায়নি (PID: {pid})")
                print("বট সম্ভবত ক্র্যাশ করেছে বা ম্যানুয়ালি বন্ধ করা হয়েছে")
                return False
        else:
            print("\n❌ বট বর্তমানে চলছে না")
            print("বট শুরু করতে: python start_bot.py")
            return False

def main():
    """মেইন ফাংশন"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YOUR CRUSH AI বট বন্ধ করুন')
    parser.add_argument('--force', '-f', action='store_true',
                       help='জোর করে বন্ধ করুন (ব্যাকআপ ছাড়া)')
    parser.add_argument('--status', '-s', action='store_true',
                       help='বটের অবস্থা দেখান')
    parser.add_argument('--kill-all', '-k', action='store_true',
                       help='সমস্ত বট প্রক্রিয়া বন্ধ করুন')
    
    args = parser.parse_args()
    
    stopper = BotStopper()
    
    if args.status:
        stopper.status()
    elif args.kill_all:
        # সমস্ত বট প্রক্রিয়া বন্ধ করুন
        stopper.stop_by_name()
        stopper.cleanup_files()
        print("✅ সমস্ত বট প্রক্রিয়া বন্ধ করা হয়েছে")
    else:
        stopper.stop(force=args.force)

if __name__ == "__main__":
    main()