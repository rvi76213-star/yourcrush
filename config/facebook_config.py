#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📘 Facebook Configuration
Facebook-specific settings and API configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== FACEBOOK AUTHENTICATION ====================
FACEBOOK_AUTH = {
    # Method 1: Cookie-based authentication (Recommended)
    "use_cookies": True,
    "cookie_file": "data/cookies/master_cookies.json",
    "backup_cookie_file": "data/cookies/backup_cookies.json",
    
    # Method 2: Email/Password authentication (Fallback)
    "use_email_password": False,
    "facebook_email": os.getenv("FACEBOOK_EMAIL", ""),
    "facebook_password": os.getenv("FACEBOOK_PASSWORD", ""),
    
    # User identification
    "user_id": os.getenv("FACEBOOK_USER_ID", "1000123456789"),
    "profile_url": "https://www.facebook.com/share/17gEJAipcr/",
    
    # Session management
    "session_timeout": 3600,  # 1 hour
    "auto_refresh": True,
    "refresh_interval": 1800,  # 30 minutes
}

# ==================== MESSENGER API SETTINGS ====================
MESSENGER_API = {
    # API endpoints
    "base_url": "https://www.facebook.com",
    "api_url": "https://www.facebook.com/api/graphqlbatch/",
    "messaging_url": "https://www.facebook.com/messaging/send/",
    "upload_url": "https://upload.facebook.com/ajax/mercury/upload.php",
    
    # GraphQL queries
    "queries": {
        "thread_list": "3336392669271570",
        "messages": "3581520540577349",
        "user_info": "3605774528086779",
        "send_message": "1969164063020179"
    },
    
    # Request headers
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    },
    
    # Form data templates
    "form_data": {
        "send_message": {
            "action_type": "ma-type:user-generated-message",
            "ephemeral_ttl_mode": "0",
            "has_attachment": "false",
            "source": "source:chat:web",
            "ui_push_phase": "C3"
        },
        "upload_photo": {
            "recipient_map[0][id]": "{thread_id}",
            "recipient_map[0][type]": "thread",
            "voice_clip": "false",
            "send_method": "messenger_composer",
            "image_height": "1024",
            "image_width": "1024",
            "image_type": "FILE_ATTACHMENT",
            "source": "source:chat:web"
        }
    }
}

# ==================== RATE LIMITING ====================
RATE_LIMITING = {
    "enabled": True,
    
    # Message limits
    "messages_per_minute": 10,
    "messages_per_hour": 100,
    "messages_per_day": 1000,
    
    # Command limits
    "commands_per_minute": 20,
    "commands_per_hour": 200,
    
    # API call limits
    "api_calls_per_minute": 30,
    "api_calls_per_hour": 300,
    
    # Delays (in seconds)
    "delay_between_messages": 2,
    "delay_between_commands": 1,
    "delay_between_api_calls": 0.5,
    
    # Burst handling
    "allow_burst": True,
    "burst_limit": 5,
    "burst_window": 10,  # seconds
}

# ==================== MESSAGE POLLING ====================
MESSAGE_POLLING = {
    "enabled": True,
    "polling_interval": 2,  # seconds between checks
    "long_polling": False,
    "long_poll_timeout": 30,  # seconds
    
    # Batch settings
    "batch_size": 20,
    "max_retries": 3,
    "retry_delay": 5,  # seconds
    
    # Filtering
    "ignore_self_messages": True,
    "ignore_old_messages": True,
    "max_message_age": 300,  # seconds (5 minutes)
    
    # Processing
    "process_in_background": True,
    "max_concurrent_messages": 5,
    "queue_size": 100,
}

# ==================== GROUP SETTINGS ====================
GROUP_SETTINGS = {
    # Group joining
    "auto_join_groups": False,
    "accept_group_invites": True,
    "max_groups_joined": 50,
    
    # Group behavior
    "reply_in_groups": True,
    "reply_only_when_mentioned": True,
    "send_welcome_messages": True,
    "send_goodbye_messages": True,
    
    # Group limits
    "max_messages_per_group_per_hour": 10,
    "max_members_to_process": 100,
    
    # Admin features
    "detect_group_admins": True,
    "obey_group_admins": True,
    "log_group_activity": True,
}

# ==================== FRIEND MANAGEMENT ====================
FRIEND_MANAGEMENT = {
    "enabled": True,
    
    # Friend requests
    "auto_accept_friend_requests": False,
    "auto_reject_friend_requests": False,
    "notify_on_friend_request": True,
    
    # Friend list
    "max_friends": 5000,
    "auto_remove_inactive": False,
    "inactive_days": 90,
    
    # Friend categorization
    "categorize_friends": True,
    "categories": ["close_friends", "friends", "acquaintances", "restricted"],
    
    # Friend activity
    "track_friend_activity": True,
    "notify_friend_activity": False,
}

# ==================== MEDIA HANDLING ====================
MEDIA_HANDLING = {
    # Photo sending
    "allow_photo_sending": True,
    "max_photo_size": 10 * 1024 * 1024,  # 10MB
    "auto_resize_photos": True,
    "max_photo_dimensions": [2048, 2048],
    
    # Video sending
    "allow_video_sending": False,
    "max_video_size": 50 * 1024 * 1024,  # 50MB
    "max_video_duration": 60,  # seconds
    
    # File sending
    "allow_file_sending": False,
    "max_file_size": 20 * 1024 * 1024,  # 20MB
    "allowed_file_types": [".pdf", ".doc", ".docx", ".txt", ".zip"],
    
    # Media storage
    "cache_media": True,
    "cache_duration": 3600,  # 1 hour
    "max_cache_size": 100 * 1024 * 1024,  # 100MB
}

# ==================== SECURITY SETTINGS ====================
SECURITY_SETTINGS = {
    # Cookie security
    "encrypt_cookies": True,
    "cookie_encryption_key": os.getenv("COOKIE_ENCRYPTION_KEY", "default_key_change_me"),
    "auto_backup_cookies": True,
    "cookie_backup_interval": 86400,  # 24 hours
    
    # Session security
    "validate_session": True,
    "session_validation_interval": 300,  # 5 minutes
    "auto_reconnect": True,
    "reconnection_attempts": 3,
    
    # Request security
    "validate_requests": True,
    "check_request_origin": True,
    "sanitize_inputs": True,
    
    # Privacy
    "log_personal_data": False,
    "encrypt_user_data": True,
    "auto_delete_old_logs": True,
    "log_retention_days": 30,
}

# ==================== ERROR HANDLING ====================
ERROR_HANDLING = {
    "log_all_errors": True,
    "error_log_file": "data/logs/facebook_errors.log",
    
    # Recovery settings
    "auto_recover_errors": True,
    "max_recovery_attempts": 3,
    "recovery_delay": 10,  # seconds
    
    # Specific error handling
    "handle_network_errors": True,
    "handle_api_errors": True,
    "handle_rate_limit_errors": True,
    "handle_login_errors": True,
    
    # Notification
    "notify_on_critical_errors": True,
    "critical_error_threshold": 5,  # errors per minute
    "notification_method": "log",  # log, email, telegram
}

# ==================== PERFORMANCE OPTIMIZATION ====================
PERFORMANCE_OPTIMIZATION = {
    # Caching
    "enable_caching": True,
    "cache_ttl": 300,  # 5 minutes
    "max_cache_size": 50 * 1024 * 1024,  # 50MB
    
    # Connection pooling
    "use_connection_pool": True,
    "pool_size": 10,
    "pool_maxsize": 20,
    
    # Compression
    "compress_responses": True,
    "compress_requests": True,
    
    # Timeouts
    "connection_timeout": 30,  # seconds
    "read_timeout": 30,  # seconds
    "write_timeout": 30,  # seconds
}

# ==================== DEBUGGING & LOGGING ====================
DEBUGGING = {
    "debug_mode": False,
    "log_level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    
    # Log files
    "log_to_file": True,
    "log_to_console": True,
    
    # Specific logging
    "log_messages": True,
    "log_commands": True,
    "log_errors": True,
    "log_performance": False,
    
    # Debug features
    "dump_responses": False,
    "save_raw_data": False,
    "trace_requests": False,
}

# ==================== BOT PERSONALIZATION ====================
BOT_PERSONALIZATION = {
    # Bot identity
    "bot_name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
    "bot_gender": "female",
    "bot_age": 20,
    "bot_location": "Digital World",
    
    # Response style
    "response_delay": 2,  # seconds
    "typing_indicator": True,
    "typing_duration": 1,  # seconds
    
    # Language
    "primary_language": "bengali",
    "secondary_language": "english",
    "code_mixing": True,
    "use_emojis": True,
    
    # Personality traits
    "friendliness": "high",
    "humor": "medium",
    "romantic_level": "high",
    "helpfulness": "high",
}

# ==================== EXPORT CONFIG ====================
def get_facebook_config() -> dict:
    """Get complete Facebook configuration"""
    return {
        "facebook_auth": FACEBOOK_AUTH,
        "messenger_api": MESSENGER_API,
        "rate_limiting": RATE_LIMITING,
        "message_polling": MESSAGE_POLLING,
        "group_settings": GROUP_SETTINGS,
        "friend_management": FRIEND_MANAGEMENT,
        "media_handling": MEDIA_HANDLING,
        "security_settings": SECURITY_SETTINGS,
        "error_handling": ERROR_HANDLING,
        "performance_optimization": PERFORMANCE_OPTIMIZATION,
        "debugging": DEBUGGING,
        "bot_personalization": BOT_PERSONALIZATION
    }

def save_facebook_config():
    """Save Facebook configuration to file"""
    import json
    config = get_facebook_config()
    
    with open("config/facebook_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Facebook configuration saved to config/facebook_config.json")

def load_facebook_config() -> dict:
    """Load Facebook configuration from file"""
    try:
        with open("config/facebook_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Facebook config file not found, using default configuration")
        return get_facebook_config()

# ==================== VALIDATION ====================
def validate_facebook_config() -> bool:
    """Validate Facebook configuration"""
    errors = []
    
    # Check required environment variables
    if FACEBOOK_AUTH["use_cookies"] and not os.path.exists(FACEBOOK_AUTH["cookie_file"]):
        errors.append(f"Cookie file not found: {FACEBOOK_AUTH['cookie_file']}")
    
    if FACEBOOK_AUTH["use_email_password"]:
        if not FACEBOOK_AUTH["facebook_email"]:
            errors.append("Facebook email not configured")
        if not FACEBOOK_AUTH["facebook_password"]:
            errors.append("Facebook password not configured")
    
    # Check rate limiting values
    if RATE_LIMITING["messages_per_minute"] <= 0:
        errors.append("messages_per_minute must be positive")
    
    if RATE_LIMITING["delay_between_messages"] < 0:
        errors.append("delay_between_messages cannot be negative")
    
    if errors:
        print("❌ Facebook configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Facebook configuration validated successfully")
    return True

# ==================== INITIALIZATION ====================
if __name__ == "__main__":
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Create default config file if it doesn't exist
    if not os.path.exists("config/facebook_config.json"):
        save_facebook_config()
        print("📁 Created default facebook_config.json file")
    
    # Validate configuration
    validate_facebook_config()