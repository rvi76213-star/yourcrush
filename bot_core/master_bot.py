#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 YOUR CRUSH AI BOT - Main Bot Class
Author: MAR PD (RANA)
Version: 1.0.0
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from .facebook_messenger import FacebookMessenger
from .message_handler import MessageHandler
from .cookie_manager import CookieManager
from .photo_delivery import PhotoDelivery
from .ai_response_engine import AIResponseEngine
from .learning_system import LearningSystem
from .command_processor import CommandProcessor
from .user_manager import UserManager
from .group_handler import GroupHandler
from .security_layer import SecurityLayer
from utils.logger import setup_logger
from utils.file_handler import FileHandler


class YourCrushBot:
    """🤖 Main Bot Class - Controls all bot operations"""
    
    def __init__(self):
        """Initialize the bot with all components"""
        self.bot_name = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
        self.version = "1.0.0"
        self.is_running = False
        self.active_commands = {}
        
        # Setup logger
        self.logger = setup_logger("your_crush_bot", "data/logs/bot_activity.log")
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.logger.info("🚀 Initializing YOUR CRUSH AI BOT...")
        
        # Security Layer (First)
        self.security = SecurityLayer()
        
        # Cookie Manager
        self.cookie_manager = CookieManager()
        
        # Facebook Messenger
        self.messenger = FacebookMessenger()
        
        # Photo Delivery System
        self.photo_delivery = PhotoDelivery()
        
        # Learning System
        self.learning = LearningSystem()
        
        # AI Response Engine
        self.ai_engine = AIResponseEngine()
        
        # Command Processor
        self.command_processor = CommandProcessor()
        
        # User Manager
        self.user_manager = UserManager()
        
        # Group Handler
        self.group_handler = GroupHandler()
        
        # Message Handler
        self.message_handler = MessageHandler(
            messenger=self.messenger,
            command_processor=self.command_processor,
            ai_engine=self.ai_engine,
            learning=self.learning,
            photo_delivery=self.photo_delivery
        )
        
        # Statistics
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "commands_executed": 0,
            "photos_sent": 0,
            "errors": 0,
            "start_time": None
        }
        
        self.logger.info("✅ Bot initialization complete!")
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Configuration file not found!")
            return {}
    
    def start(self):
        """Start the bot"""
        if self.is_running:
            self.logger.warning("Bot is already running!")
            return
        
        self.logger.info(f"🚀 Starting {self.bot_name} v{self.version}...")
        self.is_running = True
        self.stats["start_time"] = datetime.now()
        
        try:
            # Step 1: Setup security
            self.security.initialize()
            
            # Step 2: Load cookies
            cookies_loaded = self.cookie_manager.load_cookies()
            if not cookies_loaded:
                self.logger.error("❌ Failed to load cookies!")
                return False
            
            # Step 3: Login to Facebook
            login_success = self.messenger.login()
            if not login_success:
                self.logger.error("❌ Facebook login failed!")
                return False
            
            # Step 4: Initialize learning system
            self.learning.initialize()
            
            # Step 5: Start message monitoring
            self._start_message_monitor()
            
            # Step 6: Start scheduled tasks
            self._start_scheduled_tasks()
            
            self.logger.info("✅ Bot started successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start bot: {e}")
            self.is_running = False
            return False
    
    def stop(self):
        """Stop the bot"""
        if not self.is_running:
            self.logger.warning("Bot is not running!")
            return
        
        self.logger.info("🛑 Stopping bot...")
        self.is_running = False
        
        # Stop all active commands
        self._stop_all_commands()
        
        # Save learning data
        self.learning.save_data()
        
        # Logout from Facebook
        self.messenger.logout()
        
        # Save statistics
        self._save_statistics()
        
        self.logger.info("✅ Bot stopped successfully!")
    
    def _start_message_monitor(self):
        """Start monitoring for new messages"""
        def monitor():
            while self.is_running:
                try:
                    # Check for new messages
                    new_messages = self.messenger.get_unread_messages()
                    
                    for message in new_messages:
                        self._process_message(message)
                    
                    # Sleep to avoid rate limiting
                    time.sleep(self.config.get("polling_interval", 2))
                    
                except Exception as e:
                    self.logger.error(f"Error in message monitor: {e}")
                    time.sleep(5)
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        self.logger.info("📡 Message monitor started!")
    
    def _process_message(self, message: Dict):
        """Process a single message"""
        try:
            self.stats["messages_received"] += 1
            
            # Get message details
            sender_id = message.get("sender_id")
            message_text = message.get("text", "").strip()
            thread_id = message.get("thread_id")
            is_group = message.get("is_group", False)
            
            # Update user activity
            self.user_manager.update_activity(sender_id)
            
            # Check if message is a command
            if self.command_processor.is_command(message_text):
                response = self.command_processor.execute_command(
                    message_text, 
                    sender_id, 
                    thread_id, 
                    is_group
                )
                
                if response:
                    self.messenger.send_message(thread_id, response)
                    self.stats["commands_executed"] += 1
                    
            else:
                # Generate AI response
                response = self.message_handler.process_message(
                    message_text, 
                    sender_id, 
                    thread_id, 
                    is_group
                )
                
                if response:
                    # Add delay for human-like behavior
                    time.sleep(self.config.get("response_delay", 2))
                    
                    # Send response
                    self.messenger.send_message(thread_id, response)
                    self.stats["messages_sent"] += 1
                    
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            self.stats["errors"] += 1
    
    def _stop_all_commands(self):
        """Stop all active commands"""
        for cmd_id, cmd_thread in self.active_commands.items():
            if cmd_thread and cmd_thread.is_alive():
                cmd_thread.stop()
        
        self.active_commands.clear()
        self.logger.info("All active commands stopped!")
    
    def _start_scheduled_tasks(self):
        """Start scheduled background tasks"""
        # Auto-backup task
        def auto_backup():
            while self.is_running:
                time.sleep(3600)  # Every hour
                self._backup_data()
        
        # Health check task
        def health_check():
            while self.is_running:
                time.sleep(300)  # Every 5 minutes
                self._perform_health_check()
        
        # Start tasks
        backup_thread = threading.Thread(target=auto_backup, daemon=True)
        health_thread = threading.Thread(target=health_check, daemon=True)
        
        backup_thread.start()
        health_thread.start()
        
        self.logger.info("✅ Scheduled tasks started!")
    
    def _backup_data(self):
        """Backup bot data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/backup/backup_{timestamp}.zip"
            
            # Backup important files
            files_to_backup = [
                "data/users/",
                "data/learning/",
                "data/commands/",
                "config.json",
                "bot_identity.json"
            ]
            
            # Create backup
            import zipfile
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                for file in files_to_backup:
                    if os.path.exists(file):
                        if os.path.isdir(file):
                            for root, dirs, files in os.walk(file):
                                for f in files:
                                    zipf.write(os.path.join(root, f))
                        else:
                            zipf.write(file)
            
            self.logger.info(f"✅ Backup created: {backup_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Backup failed: {e}")
    
    def _perform_health_check(self):
        """Perform health check"""
        try:
            # Check Facebook connection
            if not self.messenger.is_connected():
                self.logger.warning("⚠️ Facebook connection lost! Reconnecting...")
                self.messenger.login()
            
            # Check cookie health
            cookie_health = self.cookie_manager.check_health()
            if not cookie_health["is_valid"]:
                self.logger.warning("⚠️ Cookies expired! Refreshing...")
                self.cookie_manager.refresh_cookies()
            
            # Check disk space
            import shutil
            total, used, free = shutil.disk_usage(".")
            if free < 100 * 1024 * 1024:  # Less than 100MB
                self.logger.warning("⚠️ Low disk space!")
            
            self.logger.info("✅ Health check passed!")
            
        except Exception as e:
            self.logger.error(f"❌ Health check failed: {e}")
    
    def _save_statistics(self):
        """Save bot statistics"""
        try:
            stats_file = "data/logs/bot_statistics.json"
            stats_data = {
                "bot_name": self.bot_name,
                "version": self.version,
                "start_time": self.stats["start_time"].isoformat() if self.stats["start_time"] else None,
                "end_time": datetime.now().isoformat(),
                "total_runtime": (datetime.now() - self.stats["start_time"]).total_seconds() if self.stats["start_time"] else 0,
                "messages_sent": self.stats["messages_sent"],
                "messages_received": self.stats["messages_received"],
                "commands_executed": self.stats["commands_executed"],
                "photos_sent": self.photo_delivery.photos_sent,
                "errors": self.stats["errors"]
            }
            
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats_data, f, indent=2, default=str)
            
            self.logger.info("📊 Statistics saved!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save statistics: {e}")
    
    def get_status(self) -> Dict:
        """Get bot status"""
        return {
            "bot_name": self.bot_name,
            "version": self.version,
            "is_running": self.is_running,
            "uptime": str(datetime.now() - self.stats["start_time"]) if self.stats["start_time"] else "Not running",
            "statistics": self.stats,
            "facebook_connected": self.messenger.is_connected(),
            "active_commands": len(self.active_commands)
        }
    
    def execute_admin_command(self, command: str, args: List[str] = None) -> str:
        """Execute admin command"""
        try:
            if not args:
                args = []
            
            admin_commands = {
                "status": lambda: json.dumps(self.get_status(), indent=2),
                "stop": lambda: self.stop() or "🛑 Bot stopped!",
                "restart": lambda: (self.stop(), time.sleep(2), self.start()) or "🔄 Bot restarted!",
                "backup": lambda: self._backup_data() or "💾 Backup created!",
                "stats": lambda: json.dumps(self.stats, indent=2),
                "users": lambda: f"📊 Total users: {self.user_manager.get_user_count()}",
                "clear_logs": lambda: self._clear_logs() or "🧹 Logs cleared!",
                "help": lambda: self._get_admin_help()
            }
            
            if command in admin_commands:
                return admin_commands[command]()
            else:
                return f"❌ Unknown admin command: {command}"
                
        except Exception as e:
            return f"❌ Error executing command: {e}"
    
    def _clear_logs(self):
        """Clear log files"""
        try:
            log_files = [
                "data/logs/bot_activity.log",
                "data/logs/error_log.log",
                "data/logs/command_log.log"
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    open(log_file, 'w').close()
            
            self.logger.info("Logs cleared!")
            
        except Exception as e:
            self.logger.error(f"Failed to clear logs: {e}")
    
    def _get_admin_help(self) -> str:
        """Get admin command help"""
        help_text = """
        👑 ADMIN COMMANDS:
        
        • !status - Show bot status
        • !stop - Stop the bot
        • !restart - Restart the bot
        • !backup - Create backup
        • !stats - Show statistics
        • !users - Show user count
        • !clear_logs - Clear log files
        • !help - Show this help
        
        Usage: !command
        """
        return help_text


# Singleton instance
bot_instance = None

def get_bot() -> YourCrushBot:
    """Get bot instance (singleton)"""
    global bot_instance
    if bot_instance is None:
        bot_instance = YourCrushBot()
    return bot_instance