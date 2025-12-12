"""
👑 Admin Configuration Module
"""

ADMIN_CONFIG = {
    # Admin Users
    "admins": {
        "super_admins": ["61578706761898"],  # Your Facebook ID
        "admins": [],  # Additional admin IDs
        "moderators": [],  # Moderator IDs
        "trusted_users": []  # Trusted user IDs
    },
    
    # Permission Levels
    "permissions": {
        "super_admin": {
            "level": 100,
            "permissions": [
                "all_commands",
                "manage_admins",
                "system_control",
                "view_logs",
                "modify_config",
                "emergency_stop",
                "data_management",
                "bot_restart",
                "user_management",
                "group_management",
                "security_override",
                "backup_restore",
                "monitor_all"
            ],
            "description": "Full system control"
        },
        "admin": {
            "level": 80,
            "permissions": [
                "most_commands",
                "user_management",
                "group_management",
                "view_logs",
                "moderate_content",
                "command_control",
                "bot_pause_resume",
                "view_stats",
                "manage_chats"
            ],
            "description": "Administrative control"
        },
        "moderator": {
            "level": 60,
            "permissions": [
                "basic_commands",
                "moderate_chats",
                "warn_users",
                "remove_spam",
                "view_reports",
                "manage_flood",
                "temporary_actions"
            ],
            "description": "Moderation capabilities"
        },
        "trusted": {
            "level": 40,
            "permissions": [
                "extended_commands",
                "priority_access",
                "bypass_cooldown",
                "special_features"
            ],
            "description": "Trusted user privileges"
        },
        "user": {
            "level": 20,
            "permissions": [
                "basic_commands",
                "normal_access",
                "standard_features"
            ],
            "description": "Regular user"
        },
        "restricted": {
            "level": 10,
            "permissions": [
                "limited_commands",
                "restricted_access"
            ],
            "description": "Restricted user"
        }
    },
    
    # Admin Commands
    "admin_commands": {
        "user_management": {
            "add_user": {
                "permission": "admin",
                "syntax": "add user @mention",
                "description": "Add user to group/system",
                "log_action": True,
                "confirmation": False
            },
            "delete_user": {
                "permission": "admin",
                "syntax": "delete user @mention",
                "description": "Remove user from group/system",
                "log_action": True,
                "confirmation": True
            },
            "ban_user": {
                "permission": "admin",
                "syntax": "ban @mention [reason]",
                "description": "Ban user from interacting",
                "log_action": True,
                "confirmation": True,
                "duration_options": ["1h", "24h", "7d", "30d", "permanent"]
            },
            "unban_user": {
                "permission": "admin",
                "syntax": "unban @mention",
                "description": "Unban user",
                "log_action": True,
                "confirmation": False
            },
            "warn_user": {
                "permission": "moderator",
                "syntax": "warn @mention [reason]",
                "description": "Warn user for behavior",
                "log_action": True,
                "confirmation": False,
                "max_warnings": 3
            },
            "mute_user": {
                "permission": "moderator",
                "syntax": "mute @mention [duration]",
                "description": "Mute user in chat",
                "log_action": True,
                "confirmation": False,
                "default_duration": "1h"
            }
        },
        
        "group_management": {
            "add_to_group": {
                "permission": "admin",
                "syntax": "add @mention to group",
                "description": "Add user to specific group",
                "log_action": True,
                "confirmation": False
            },
            "remove_from_group": {
                "permission": "admin",
                "syntax": "remove @mention from group",
                "description": "Remove user from group",
                "log_action": True,
                "confirmation": True
            },
            "kick_from_group": {
                "permission": "admin",
                "syntax": "kick @mention from group",
                "description": "Kick user from group",
                "log_action": True,
                "confirmation": True
            },
            "promote_to_admin": {
                "permission": "super_admin",
                "syntax": "promote @mention to admin",
                "description": "Promote user to group admin",
                "log_action": True,
                "confirmation": True
            },
            "demote_admin": {
                "permission": "super_admin",
                "syntax": "demote @mention from admin",
                "description": "Demote user from admin",
                "log_action": True,
                "confirmation": True
            },
            "group_settings": {
                "permission": "admin",
                "syntax": "group settings [option] [value]",
                "description": "Change group settings",
                "log_action": True,
                "confirmation": False
            }
        },
        
        "bot_control": {
            "start_bot": {
                "permission": "super_admin",
                "syntax": "start bot",
                "description": "Start the bot",
                "log_action": True,
                "confirmation": False
            },
            "stop_bot": {
                "permission": "super_admin",
                "syntax": "stop bot",
                "description": "Stop the bot",
                "log_action": True,
                "confirmation": True
            },
            "restart_bot": {
                "permission": "super_admin",
                "syntax": "restart bot",
                "description": "Restart the bot",
                "log_action": True,
                "confirmation": True
            },
            "pause_bot": {
                "permission": "admin",
                "syntax": "pause bot",
                "description": "Pause bot activities",
                "log_action": True,
                "confirmation": False
            },
            "resume_bot": {
                "permission": "admin",
                "syntax": "resume bot",
                "description": "Resume bot activities",
                "log_action": True,
                "confirmation": False
            },
            "bot_status": {
                "permission": "admin",
                "syntax": "bot status",
                "description": "Check bot status",
                "log_action": False,
                "confirmation": False
            }
        },
        
        "system_control": {
            "view_logs": {
                "permission": "admin",
                "syntax": "view logs [type] [lines]",
                "description": "View system logs",
                "log_action": True,
                "confirmation": False,
                "max_lines": 100
            },
            "clear_logs": {
                "permission": "super_admin",
                "syntax": "clear logs [type]",
                "description": "Clear system logs",
                "log_action": True,
                "confirmation": True
            },
            "backup_data": {
                "permission": "super_admin",
                "syntax": "backup data",
                "description": "Create data backup",
                "log_action": True,
                "confirmation": False
            },
            "restore_data": {
                "permission": "super_admin",
                "syntax": "restore data [backup_id]",
                "description": "Restore from backup",
                "log_action": True,
                "confirmation": True
            },
            "system_stats": {
                "permission": "admin",
                "syntax": "system stats",
                "description": "Show system statistics",
                "log_action": False,
                "confirmation": False
            },
            "update_config": {
                "permission": "super_admin",
                "syntax": "update config [section] [key] [value]",
                "description": "Update configuration",
                "log_action": True,
                "confirmation": True
            }
        },
        
        "command_control": {
            "enable_command": {
                "permission": "admin",
                "syntax": "enable command [command_name]",
                "description": "Enable a command",
                "log_action": True,
                "confirmation": False
            },
            "disable_command": {
                "permission": "admin",
                "syntax": "disable command [command_name]",
                "description": "Disable a command",
                "log_action": True,
                "confirmation": True
            },
            "command_stats": {
                "permission": "admin",
                "syntax": "command stats [command_name]",
                "description": "Show command statistics",
                "log_action": False,
                "confirmation": False
            },
            "reload_commands": {
                "permission": "admin",
                "syntax": "reload commands",
                "description": "Reload command files",
                "log_action": True,
                "confirmation": False
            },
            "add_command": {
                "permission": "super_admin",
                "syntax": "add command [type] [name] [config]",
                "description": "Add new command",
                "log_action": True,
                "confirmation": True
            },
            "remove_command": {
                "permission": "super_admin",
                "syntax": "remove command [name]",
                "description": "Remove command",
                "log_action": True,
                "confirmation": True
            }
        },
        
        "emergency": {
            "emergency_stop": {
                "permission": "super_admin",
                "syntax": "emergency stop",
                "description": "Immediately stop all bot activities",
                "log_action": True,
                "confirmation": True,
                "requires_password": True
            },
            "lockdown_mode": {
                "permission": "super_admin",
                "syntax": "lockdown [enable/disable]",
                "description": "Enable/disable lockdown mode",
                "log_action": True,
                "confirmation": True
            },
            "wipe_data": {
                "permission": "super_admin",
                "syntax": "wipe data [type]",
                "description": "Wipe sensitive data",
                "log_action": True,
                "confirmation": True,
                "requires_password": True
            },
            "recovery_mode": {
                "permission": "super_admin",
                "syntax": "recovery mode",
                "description": "Enter recovery mode",
                "log_action": True,
                "confirmation": True
            }
        }
    },
    
    # Admin Interface Settings
    "interface": {
        "admin_prefix": "!",
        "command_prefix": ".",
        "notification_enabled": True,
        "notify_on_errors": True,
        "notify_on_warnings": True,
        "notify_on_admin_actions": False,
        "admin_dashboard": False,
        "web_interface": False,
        "telegram_notifications": False,
        "email_notifications": False
    },
    
    # Security Settings
    "security": {
        "require_confirmation": True,
        "confirm_destructive": True,
        "log_all_actions": True,
        "encrypt_admin_logs": True,
        "admin_activity_monitoring": True,
        "suspicious_activity_alerts": True,
        "two_factor_admin": False,
        "admin_session_timeout": 7200,  # 2 hours
        "ip_whitelist_admin": False,
        "admin_command_cooldown": 2  # seconds
    },
    
    # Logging & Auditing
    "logging": {
        "admin_action_log": "data/logs/admin_actions.log",
        "admin_error_log": "data/logs/admin_errors.log",
        "admin_audit_log": "data/logs/admin_audit.log",
        "log_retention_days": 90,
        "log_rotation_size_mb": 10,
        "log_compression": True,
        "real_time_logging": True,
        "detailed_logging": True
    },
    
    # Performance
    "performance": {
        "admin_command_timeout": 30,
        "max_concurrent_admin_actions": 5,
        "admin_queue_size": 50,
        "cache_admin_data": True,
        "async_admin_processing": True,
        "admin_stats_refresh_interval": 60  # seconds
    }
}

class AdminManager:
    """Admin management system"""
    
    def __init__(self):
        self.admins = set(ADMIN_CONFIG["admins"]["super_admins"] + 
                         ADMIN_CONFIG["admins"]["admins"])
        self.moderators = set(ADMIN_CONFIG["admins"]["moderators"])
        self.trusted_users = set(ADMIN_CONFIG["admins"]["trusted_users"])
        
        self.admin_log = []
        self.admin_actions = []
        
    def get_user_permission_level(self, user_id):
        """Get user's permission level"""
        if user_id in ADMIN_CONFIG["admins"]["super_admins"]:
            return "super_admin"
        elif user_id in ADMIN_CONFIG["admins"]["admins"]:
            return "admin"
        elif user_id in ADMIN_CONFIG["admins"]["moderators"]:
            return "moderator"
        elif user_id in ADMIN_CONFIG["admins"]["trusted_users"]:
            return "trusted"
        else:
            return "user"
    
    def has_permission(self, user_id, permission_name):
        """Check if user has specific permission"""
        user_level = self.get_user_permission_level(user_id)
        permissions = ADMIN_CONFIG["permissions"][user_level]["permissions"]
        
        # Super admin has all permissions
        if user_level == "super_admin":
            return True
        
        # Check specific permission
        if permission_name in permissions:
            return True
        
        # Check for "all" or "most" permissions
        if "all_commands" in permissions:
            return True
        if "most_commands" in permissions and "command" in permission_name:
            return True
        
        return False
    
    def can_execute_command(self, user_id, command_category, command_name):
        """Check if user can execute specific command"""
        if command_category not in ADMIN_CONFIG["admin_commands"]:
            return False
        
        if command_name not in ADMIN_CONFIG["admin_commands"][command_category]:
            return False
        
        command_config = ADMIN_CONFIG["admin_commands"][command_category][command_name]
        required_permission = command_config["permission"]
        
        return self.has_permission(user_id, required_permission)
    
    def log_admin_action(self, user_id, action, details=None, success=True):
        """Log admin action"""
        import time
        from datetime import datetime
        
        log_entry = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details or {},
            "success": success,
            "permission_level": self.get_user_permission_level(user_id)
        }
        
        self.admin_log.append(log_entry)
        self.admin_actions.append(log_entry)
        
        # Write to file
        try:
            import json
            log_file = ADMIN_CONFIG["logging"]["admin_action_log"]
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except:
            pass
        
        return log_entry
    
    def get_recent_actions(self, limit=50, user_id=None):
        """Get recent admin actions"""
        actions = self.admin_actions.copy()
        
        if user_id:
            actions = [a for a in actions if a["user_id"] == user_id]
        
        actions.sort(key=lambda x: x["timestamp"], reverse=True)
        return actions[:limit]
    
    def add_admin(self, current_admin_id, new_admin_id, admin_type="admin"):
        """Add new admin"""
        # Check if current admin has permission
        if not self.has_permission(current_admin_id, "manage_admins"):
            return False, "Permission denied"
        
        # Validate admin type
        if admin_type not in ["super_admin", "admin", "moderator", "trusted"]:
            return False, f"Invalid admin type: {admin_type}"
        
        # Add to appropriate list
        if admin_type == "super_admin":
            ADMIN_CONFIG["admins"]["super_admins"].append(new_admin_id)
            self.admins.add(new_admin_id)
        elif admin_type == "admin":
            ADMIN_CONFIG["admins"]["admins"].append(new_admin_id)
            self.admins.add(new_admin_id)
        elif admin_type == "moderator":
            ADMIN_CONFIG["admins"]["moderators"].append(new_admin_id)
            self.moderators.add(new_admin_id)
        elif admin_type == "trusted":
            ADMIN_CONFIG["admins"]["trusted_users"].append(new_admin_id)
            self.trusted_users.add(new_admin_id)
        
        # Log action
        self.log_admin_action(
            current_admin_id,
            "add_admin",
            {"new_admin_id": new_admin_id, "admin_type": admin_type},
            success=True
        )
        
        return True, f"Added {new_admin_id} as {admin_type}"
    
    def remove_admin(self, current_admin_id, admin_to_remove_id):
        """Remove admin"""
        # Check if current admin has permission
        if not self.has_permission(current_admin_id, "manage_admins"):
            return False, "Permission denied"
        
        # Cannot remove yourself if you're the only super admin
        if (admin_to_remove_id in ADMIN_CONFIG["admins"]["super_admins"] and 
            len(ADMIN_CONFIG["admins"]["super_admins"]) == 1):
            return False, "Cannot remove the only super admin"
        
        # Remove from all lists
        removed_from = []
        
        if admin_to_remove_id in ADMIN_CONFIG["admins"]["super_admins"]:
            ADMIN_CONFIG["admins"]["super_admins"].remove(admin_to_remove_id)
            removed_from.append("super_admins")
        
        if admin_to_remove_id in ADMIN_CONFIG["admins"]["admins"]:
            ADMIN_CONFIG["admins"]["admins"].remove(admin_to_remove_id)
            removed_from.append("admins")
        
        if admin_to_remove_id in ADMIN_CONFIG["admins"]["moderators"]:
            ADMIN_CONFIG["admins"]["moderators"].remove(admin_to_remove_id)
            removed_from.append("moderators")
        
        if admin_to_remove_id in ADMIN_CONFIG["admins"]["trusted_users"]:
            ADMIN_CONFIG["admins"]["trusted_users"].remove(admin_to_remove_id)
            removed_from.append("trusted_users")
        
        # Update sets
        self.admins.discard(admin_to_remove_id)
        self.moderators.discard(admin_to_remove_id)
        self.trusted_users.discard(admin_to_remove_id)
        
        # Log action
        self.log_admin_action(
            current_admin_id,
            "remove_admin",
            {"removed_admin_id": admin_to_remove_id, "removed_from": removed_from},
            success=True
        )
        
        return True, f"Removed {admin_to_remove_id} from {', '.join(removed_from)}"
    
    def get_admin_stats(self):
        """Get admin statistics"""
        stats = {
            "total_super_admins": len(ADMIN_CONFIG["admins"]["super_admins"]),
            "total_admins": len(ADMIN_CONFIG["admins"]["admins"]),
            "total_moderators": len(ADMIN_CONFIG["admins"]["moderators"]),
            "total_trusted_users": len(ADMIN_CONFIG["admins"]["trusted_users"]),
            "total_admin_actions": len(self.admin_actions),
            "recent_actions_24h": len([a for a in self.admin_actions 
                                      if time.time() - a["timestamp"] < 86400]),
            "success_rate": 0
        }
        
        # Calculate success rate
        if self.admin_actions:
            successful = sum(1 for a in self.admin_actions if a["success"])
            stats["success_rate"] = (successful / len(self.admin_actions)) * 100
        
        return stats
    
    def cleanup_old_logs(self):
        """Clean up old admin logs"""
        import time
        import os
        
        retention_days = ADMIN_CONFIG["logging"]["log_retention_days"]
        cutoff_time = time.time() - (retention_days * 86400)
        
        # Clean in-memory logs
        self.admin_actions = [a for a in self.admin_actions if a["timestamp"] > cutoff_time]
        
        # Clean log files if they get too large
        log_files = [
            ADMIN_CONFIG["logging"]["admin_action_log"],
            ADMIN_CONFIG["logging"]["admin_error_log"],
            ADMIN_CONFIG["logging"]["admin_audit_log"]
        ]
        
        max_size_mb = ADMIN_CONFIG["logging"]["log_rotation_size_mb"]
        max_size_bytes = max_size_mb * 1024 * 1024
        
        for log_file in log_files:
            if os.path.exists(log_file) and os.path.getsize(log_file) > max_size_bytes:
                # Rotate log file
                try:
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = f"{log_file}.{timestamp}.bak"
                    os.rename(log_file, backup_file)
                    
                    # Compress if enabled
                    if ADMIN_CONFIG["logging"]["log_compression"]:
                        import gzip
                        with open(backup_file, 'rb') as f_in:
                            with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
                                f_out.write(f_in.read())
                        os.remove(backup_file)
                        
                except Exception as e:
                    print(f"Error rotating log file {log_file}: {e}")

if __name__ == "__main__":
    print("Admin Configuration Module Loaded")
    
    # Test admin manager
    admin_mgr = AdminManager()
    
    print("\nAdmin Statistics:")
    stats = admin_mgr.get_admin_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nPermission Tests:")
    test_user = "1000123456789"  # Super admin
    
    permissions_to_check = [
        "manage_admins",
        "system_control",
        "view_logs",
        "user_management"
    ]
    
    for perm in permissions_to_check:
        has_perm = admin_mgr.has_permission(test_user, perm)
        print(f"  {test_user} has '{perm}': {'✅ Yes' if has_perm else '❌ No'}")
    
    print("\nCommand Permission Tests:")
    commands_to_check = [
        ("user_management", "add_user"),
        ("bot_control", "stop_bot"),
        ("emergency", "emergency_stop")
    ]
    
    for category, command in commands_to_check:
        can_execute = admin_mgr.can_execute_command(test_user, category, command)
        print(f"  {test_user} can execute '{category}.{command}': {'✅ Yes' if can_execute else '❌ No'}")
