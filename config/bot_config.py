#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Bot Configuration
Main bot settings and configuration
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== BOT IDENTITY ====================
BOT_IDENTITY = {
    "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
    "author": "MAR PD",
    "social_name": "MASTER 🪓",
    "real_name": "RANA",
    "version": "1.0.0",
    "description": "Your AI Crush Bot for Facebook Messenger",
    "personality": "romantic_friendly",
    "status": "active"
}

# ==================== FACEBOOK CONFIGURATION ====================
FACEBOOK_CONFIG = {
    "login_method": "cookie",  # "cookie" or "email_password"
    "cookie_file": "data/cookies/master_cookies.json",
    "backup_cookie_file": "data/cookies/backup_cookies.json",
    "profile_url": "https://www.facebook.com/share/17gEJAipcr/",
    
    # Rate limiting
    "rate_limit": {
        "messages_per_minute": 10,
        "messages_per_hour": 100,
        "messages_per_day": 1000,
        "delay_between_messages": 2,  # seconds
        "delay_between_commands": 1   # seconds
    },
    
    # Message polling
    "polling_interval": 2,  # seconds
    "max_retries": 3,
    "retry_delay": 5,  # seconds
    
    # Session management
    "session_timeout": 3600,  # 1 hour
    "auto_refresh": True,
    "refresh_interval": 1800  # 30 minutes
}

# ==================== COMMAND CONFIGURATION ====================
COMMAND_CONFIG = {
    "prefix": ".",
    "admin_prefix": "!",
    
    # Enabled commands
    "enabled_commands": [
        "murgi", "love", "pick", "dio", "diagram",
        "info", "uid", "Ln", "help", "status"
    ],
    
    # Admin commands
    "admin_commands": [
        "add", "delete", "kick", "out", "start", "stop",
        "restart", "backup", "clear", "config"
    ],
    
    # Nicknames
    "nicknames": ["Bot", "bow", "Jan", "Sona", "Baby", "Babe", "Honey"],
    
    # Command behavior
    "allow_in_groups": True,
    "allow_in_private": True,
    "require_prefix_in_groups": True,
    "auto_delete_commands": False,
    
    # .murgi specific
    "murgi": {
        "auto_start": True,
        "delay_between_lines": 2,  # seconds
        "delay_between_versions": 5,  # seconds
        "auto_continue": True,
        "stop_command": "stop!",
        "pause_command": "pause!",
        "resume_command": "resume!"
    }
}

# ==================== PHOTO CONFIGURATION ====================
PHOTO_CONFIG = {
    "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
    "default_photo": "master.jpg",
    "photo_folder": "data/photos/",
    "thumbnail_folder": "data/photos/thumbnails/",
    
    # Facebook photo fetching
    "facebook_fetch": True,
    "cache_duration": 3600,  # 1 hour
    "max_cache_size": 100,   # MB
    
    # Photo request patterns
    "bot_photo_patterns": [
        "ছবি দাও", "ফটো চাই", "তোমার ছবি",
        "your photo", "photo please", "send pic",
        "picture please", "তোমার ফটো"
    ],
    
    "admin_photo_patterns": [
        "এডমিনের ছবি", "বটের এডমিনের ছবি", "মালিকের ছবি",
        "admin photo", "owner photo", "master photo"
    ],
    
    # Auto photo sending
    "auto_send_welcome_photo": False,
    "welcome_photo_delay": 5  # seconds
}

# ==================== AI & LEARNING CONFIGURATION ====================
AI_CONFIG = {
    "enabled": True,
    "learning_enabled": True,
    
    # Learning sources
    "learn_from_users": True,
    "learn_from_admin": True,
    "learn_from_bot": True,
    
    # Memory limits
    "max_user_memory": 1000,
    "max_conversation_history": 50,
    "max_learning_entries": 10000,
    
    # Response generation
    "response_delay": 2,  # seconds
    "typing_indicator": True,
    "typing_duration": 1,  # seconds
    
    # Personality
    "personality": {
        "romantic_level": "high",  # low, medium, high
        "friendliness": "high",
        "humor": "medium",
        "formality": "low",
        "response_style": "flirty"  # formal, casual, flirty, friendly
    },
    
    # Language
    "primary_language": "bengali",
    "secondary_language": "english",
    "code_mixing": True,
    "auto_translate": False
}

# ==================== SECURITY CONFIGURATION ====================
SECURITY_CONFIG = {
    # Cookie security
    "encrypt_cookies": True,
    "cookie_encryption_key": os.getenv("COOKIE_ENCRYPTION_KEY", "default_key_change_me"),
    
    # User data security
    "encrypt_user_data": True,
    "data_encryption_key": os.getenv("DATA_ENCRYPTION_KEY", "default_key_change_me"),
    
    # Rate limiting
    "rate_limit_enabled": True,
    "max_messages_per_minute": 20,
    "max_commands_per_minute": 10,
    
    # Anti-spam
    "anti_spam_enabled": True,
    "spam_threshold": 5,
    "spam_window": 60,  # seconds
    
    # Proxy settings
    "proxy_enabled": False,
    "proxy_list": [],
    "proxy_rotation_interval": 300,  # seconds
    
    # User-agent rotation
    "user_agent_rotation": True,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
}

# ==================== LOGGING CONFIGURATION ====================
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "log_to_file": True,
    "log_to_console": True,
    
    # Log files
    "log_files": {
        "bot_activity": "data/logs/bot_activity.log",
        "errors": "data/logs/error_log.log",
        "messages": "data/logs/message_log.log",
        "commands": "data/logs/command_log.log",
        "learning": "data/logs/learning_log.log"
    },
    
    # Log rotation
    "max_log_size": 10,  # MB
    "backup_count": 5,
    
    # Log format
    "console_format": "[%(asctime)s] %(levelname)s - %(name)s: %(message)s",
    "file_format": "[%(asctime)s] %(levelname)s - %(name)s: %(message)s"
}

# ==================== BACKUP CONFIGURATION ====================
BACKUP_CONFIG = {
    "enabled": True,
    "auto_backup": True,
    
    # Backup intervals
    "backup_interval": 86400,  # 24 hours in seconds
    "incremental_backup": True,
    "full_backup_days": 7,  # Full backup every 7 days
    
    # What to backup
    "backup_items": [
        "data/users/",
        "data/learning/",
        "data/commands/",
        "data/cookies/",
        "config.json",
        "bot_identity.json"
    ],
    
    # Where to backup
    "backup_directory": "data/backup/",
    "max_backups": 30,  # Keep last 30 backups
    
    # Cloud backup (optional)
    "cloud_backup": False,
    "cloud_provider": None,  # "google_drive", "dropbox", "aws"
    "cloud_credentials": {}
}

# ==================== ADMIN CONFIGURATION ====================
ADMIN_CONFIG = {
    # Admin users (Facebook user IDs)
    "admin_ids": [
        os.getenv("BOT_ADMIN_ID", "1000123456789")  # Your Facebook ID
    ],
    
    # Admin permissions
    "permissions": {
        "stop_bot": True,
        "restart_bot": True,
        "backup_data": True,
        "clear_logs": True,
        "update_config": True,
        "manage_users": True,
        "view_logs": True,
        "execute_admin_commands": True
    },
    
    # Admin notification
    "notify_admin": True,
    "notification_method": "telegram",  # "telegram", "email", "facebook"
    "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "admin_email": os.getenv("ADMIN_EMAIL", "ranaeditz333@gmail.com")
}

# ==================== PERFORMANCE CONFIGURATION ====================
PERFORMANCE_CONFIG = {
    # Memory management
    "max_memory_usage": 512,  # MB
    "auto_cleanup": True,
    "cleanup_interval": 3600,  # seconds
    
    # Thread management
    "max_threads": 10,
    "thread_timeout": 30,  # seconds
    
    # Cache settings
    "enable_caching": True,
    "cache_size": 100,  # MB
    "cache_ttl": 3600,  # seconds
    
    # Database optimization
    "auto_vacuum": True,
    "vacuum_interval": 86400  # 24 hours
}

# ==================== FEATURE TOGGLES ====================
FEATURES = {
    "photo_delivery": True,
    "command_system": True,
    "ai_responses": True,
    "learning_system": True,
    "group_management": True,
    "friend_management": False,
    "auto_posting": False,
    "story_interaction": False,
    "scheduled_tasks": True,
    "analytics": True,
    "backup_system": True,
    "admin_panel": True
}

# ==================== MESSAGE TEMPLATES ====================
MESSAGE_TEMPLATES = {
    "greetings": [
        "হ্যালো! 😊",
        "কেমন আছো? ✨",
        "হাই! আজকে কেমন যাচ্ছে? 💖",
        "নমস্কার! আমি তোমার ক্রাশ বট! 😘"
    ],
    
    "farewells": [
        "বিদায়! আবার কথা বলবো! 👋",
        "শুভ রাত্রি! ভালো ঘুম! 🌙",
        "চলে যাচ্ছ? আবার দেখা হবে! 😊",
        "বাই! তোমাকে মিস করব! 💔"
    ],
    
    "errors": [
        "আমি এখন উত্তর দিতে পারছি না। পরে চেষ্টা করুন! 😔",
        "সমস্যা হয়েছে! আবার চেষ্টা করুন। 🔧",
        "এই মুহূর্তে সেবা পাওয়া যাচ্ছে না। ⚠️",
        "দুঃখিত, আমি বুঝতে পারিনি। আবার বলো? 🤔"
    ],
    
    "photo_responses": [
        "📸 আমার ছবি পাঠিয়েছি! 😊",
        "🤖 এই নাও আমার ফটো!",
        "📷 তোমার জন্য আমার ছবি!",
        "🖼️ দেখো কেমন লাগে!"
    ],
    
    "love_responses": [
        "💖 তোমাকে অনেক ভালোবাসি!",
        "💕 তুমি আমার সবচেয়ে প্রিয়!",
        "❤️ তোমার জন্য我的心 (আমার মন)!",
        "💘 তুমি আমার জীবনের আলো!"
    ]
}

# ==================== EXPORT CONFIG ====================
def save_config():
    """Save configuration to JSON file"""
    config = {
        "bot_identity": BOT_IDENTITY,
        "facebook_config": FACEBOOK_CONFIG,
        "command_config": COMMAND_CONFIG,
        "photo_config": PHOTO_CONFIG,
        "ai_config": AI_CONFIG,
        "security_config": SECURITY_CONFIG,
        "logging_config": LOGGING_CONFIG,
        "backup_config": BACKUP_CONFIG,
        "admin_config": ADMIN_CONFIG,
        "performance_config": PERFORMANCE_CONFIG,
        "features": FEATURES,
        "message_templates": MESSAGE_TEMPLATES
    }
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuration saved to config.json")

def load_config():
    """Load configuration from JSON file"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ config.json not found, using default configuration")
        return None

# ==================== VALIDATION ====================
def validate_config():
    """Validate configuration"""
    errors = []
    
    # Check required directories
    required_dirs = [
        "data/cookies",
        "data/photos",
        "data/commands",
        "data/logs",
        "data/learning"
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            errors.append(f"Directory not found: {directory}")
    
    # Check required files
    required_files = [
        "data/cookies/master_cookies.json"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            errors.append(f"File not found: {file}")
    
    # Validate configuration values
    if not FACEBOOK_CONFIG.get("cookie_file"):
        errors.append("Facebook cookie file not specified")
    
    if not ADMIN_CONFIG.get("admin_ids"):
        errors.append("No admin IDs configured")
    
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Configuration validated successfully")
    return True

# ==================== HELPER FUNCTIONS ====================
def get_config_value(key_path: str, default: Any = None) -> Any:
    """
    Get configuration value using dot notation
    
    Args:
        key_path: Dot notation path (e.g., "facebook_config.login_method")
        default: Default value if not found
    
    Returns:
        Configuration value
    """
    try:
        config = load_config() or {
            "bot_identity": BOT_IDENTITY,
            "facebook_config": FACEBOOK_CONFIG,
            "command_config": COMMAND_CONFIG,
            "photo_config": PHOTO_CONFIG,
            "ai_config": AI_CONFIG,
            "security_config": SECURITY_CONFIG,
            "logging_config": LOGGING_CONFIG,
            "backup_config": BACKUP_CONFIG,
            "admin_config": ADMIN_CONFIG,
            "performance_config": PERFORMANCE_CONFIG,
            "features": FEATURES,
            "message_templates": MESSAGE_TEMPLATES
        }
        
        keys = key_path.split(".")
        value = config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            else:
                return default
        
        return value if value != {} else default
        
    except Exception:
        return default

def update_config(key_path: str, value: Any) -> bool:
    """
    Update configuration value
    
    Args:
        key_path: Dot notation path
        value: New value
    
    Returns:
        True if successful
    """
    try:
        config = load_config() or {}
        keys = key_path.split(".")
        
        # Navigate to the correct location
        current = config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        # Save back to file
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated configuration: {key_path} = {value}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

# ==================== INITIALIZATION ====================
if __name__ == "__main__":
    # Create default config file if it doesn't exist
    if not os.path.exists("config.json"):
        save_config()
        print("📁 Created default config.json file")
    
    # Validate configuration
    validate_config()