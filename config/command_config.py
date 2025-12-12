"""
⚙️ Command Configuration Module
"""

COMMAND_CONFIG = {
    # Prefix Commands
    "prefix_commands": {
        ".murgi": {
            "enabled": True,
            "type": "sequential",
            "delay_between_lines": 2.0,
            "delay_between_files": 5.0,
            "files": ["v1.txt", "v2.txt", "v3.txt"],
            "stop_command": "stop!",
            "pause_command": "pause!",
            "resume_command": "resume!",
            "max_lines_per_file": 10
        },
        ".love": {
            "enabled": True,
            "type": "sequential",
            "responses_file": "responses.txt",
            "max_responses": 10
        },
        ".pick": {
            "enabled": True,
            "type": "random",
            "picks_file": "picks.txt",
            "default_picks": [
                "🍀 ভাগ্য তোমার সাথে!",
                "🎯 লক্ষ্য স্থির কর!",
                "⭐ সেরাটা বেছে নাও!",
                "🚀 এগিয়ে যাও!"
            ]
        },
        ".dio": {
            "enabled": True,
            "type": "sequential",
            "lines_file": "dio_lines.txt",
            "delay": 1.5,
            "signature": "🦸‍♂️ DIO"
        },
        ".diagram": {
            "enabled": True,
            "type": "special",
            "diagram_types": ["flowchart", "sequence", "mindmap"],
            "default_type": "flowchart"
        },
        ".info": {
            "enabled": True,
            "type": "info",
            "show_identity": True,
            "show_stats": True,
            "show_commands": True
        },
        ".uid": {
            "enabled": True,
            "type": "utility",
            "response_format": "👤 {user_name}'s UID: {user_id}"
        },
        ".Ln": {
            "enabled": True,
            "type": "utility",
            "max_lines": 100,
            "line_format": "📜 Line {number}: {content}"
        }
    },
    
    # Admin Commands
    "admin_commands": {
        "add": {
            "user": {
                "enabled": True,
                "permission": "admin",
                "response": "✅ @mention কে সফলভাবে এড করা হয়েছে!",
                "log_action": True
            },
            "pick": {
                "enabled": True,
                "permission": "admin",
                "format": "text",
                "max_length": 100
            },
            "url": {
                "enabled": True,
                "permission": "admin",
                "validate_url": True,
                "max_urls": 50
            }
        },
        "delete": {
            "user": {
                "enabled": True,
                "permission": "admin",
                "response": "🗑️ @mention কে ডিলিট করা হয়েছে!",
                "confirm": True
            }
        },
        "kick": {
            "enabled": True,
            "permission": "admin",
            "response": "👢 @mention কে কিক করা হয়েছে!",
            "reason_required": False
        },
        "out": {
            "group": {
                "enabled": True,
                "permission": "admin",
                "response": "👋 বিদায় সবাই!",
                "remove_admin": False
            },
            "admin": {
                "enabled": True,
                "permission": "super_admin",
                "response": "👑 এডমিন হিসেবে বিদায়!",
                "remove_permissions": True
            }
        },
        "start": {
            "live": {
                "enabled": True,
                "permission": "admin",
                "response": "📡 লাইভ শুরু হচ্ছে!",
                "auto_join": True
            }
        },
        "stop": {
            "bot": {
                "enabled": True,
                "permission": "admin",
                "response": "⏹️ বট স্টপ করা হয়েছে!",
                "graceful_shutdown": True
            },
            "command": {
                "enabled": True,
                "permission": "user",
                "response": "🛑 কমান্ড স্টপ করা হয়েছে!",
                "stop_all": False
            }
        },
        "info": {
            "user": {
                "enabled": True,
                "permission": "admin",
                "show_sensitive": False,
                "format": "detailed"
            },
            "bot": {
                "enabled": True,
                "permission": "user",
                "show_identity": True
            }
        },
        "uid": {
            "enabled": True,
            "permission": "admin",
            "show_all": False
        }
    },
    
    # Nickname Commands
    "nickname_commands": {
        "Bot": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0
        },
        "bow": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0
        },
        "Jan": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0
        },
        "Sona": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0
        },
        "Baby": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0,
            "romantic_mode": True
        },
        "Etc": {
            "enabled": True,
            "responses_file": "responses.txt",
            "response_type": "random",
            "delay": 1.0
        }
    },
    
    # Command System Settings
    "system": {
        "command_prefix": ".",
        "admin_prefix": "!",
        "nickname_prefix": "",
        "max_command_length": 200,
        "command_timeout": 30,
        "cooldown_per_user": 3,
        "cooldown_per_command": 2,
        "enable_command_logging": True,
        "command_history_size": 1000,
        "auto_complete_commands": True,
        "spell_check_commands": False
    },
    
    # Validation Rules
    "validation": {
        "allow_special_chars": True,
        "allow_emojis": True,
        "max_emojis_per_message": 10,
        "blocked_words": [],
        "allowed_mentions": 5,
        "max_urls_per_message": 3
    },
    
    # Performance Settings
    "performance": {
        "parallel_processing": True,
        "max_threads": 5,
        "queue_size": 100,
        "cache_size": 1000,
        "cleanup_interval": 3600
    }
}

def get_command_config(command_type, command_name=None):
    """Get configuration for specific command"""
    if command_type == "prefix":
        return COMMAND_CONFIG["prefix_commands"].get(command_name, {})
    elif command_type == "admin":
        if command_name:
            return COMMAND_CONFIG["admin_commands"].get(command_name, {})
        return COMMAND_CONFIG["admin_commands"]
    elif command_type == "nickname":
        return COMMAND_CONFIG["nickname_commands"].get(command_name, {})
    return {}

def is_command_enabled(command_type, command_name):
    """Check if a command is enabled"""
    config = get_command_config(command_type, command_name)
    if not config:
        return False
    return config.get("enabled", False)

def get_command_permission(command_type, command_name):
    """Get permission level required for command"""
    config = get_command_config(command_type, command_name)
    return config.get("permission", "user")

def validate_command_input(command_type, command_name, user_input):
    """Validate command input"""
    config = get_command_config(command_type, command_name)
    
    if not config:
        return False, "Command not found"
    
    # Check length
    max_len = COMMAND_CONFIG["system"]["max_command_length"]
    if len(user_input) > max_len:
        return False, f"Input too long (max {max_len} characters)"
    
    return True, "Valid"

if __name__ == "__main__":
    print("Command Configuration Module Loaded")
    print(f"Total Prefix Commands: {len(COMMAND_CONFIG['prefix_commands'])}")
    print(f"Total Admin Commands: {len(COMMAND_CONFIG['admin_commands'])}")
    print(f"Total Nickname Commands: {len(COMMAND_CONFIG['nickname_commands'])}")