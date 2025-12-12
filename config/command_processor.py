#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Command Processor System
Handles all bot commands (.murgi, .love, .pick, etc.)
"""

import json
import logging
import os
import random
import re
import time
import threading
from typing import Dict, List, Optional, Any, Callable

from utils.logger import setup_logger
from utils.file_handler import FileHandler


class CommandProcessor:
    """⚡ Command Processor"""
    
    def __init__(self):
        self.logger = setup_logger("command_processor", "data/logs/command_log.log")
        self.file_handler = FileHandler()
        
        # Load command registry
        self.command_registry = self._load_command_registry()
        
        # Active command threads
        self.active_commands = {}
        
        # Command history
        self.command_history = []
        self.max_history = 1000
        
        # .murgi sequential execution tracking
        self.murgi_execution = {
            "active": False,
            "current_file": None,
            "current_line": 0,
            "total_lines": 0,
            "thread": None,
            "paused": False,
            "target_user_id": None,
            "target_username": None,
            "original_sender": None,
            "mention_target": "user"
        }
        
        # Command cooldowns
        self.cooldowns = {}
        self.command_stats = {}
        
        # Initialize commands
        self._initialize_commands()
    
    def _load_command_registry(self) -> Dict:
        """Load command registry from file"""
        try:
            registry_file = "data/commands/command_registry.json"
            
            if os.path.exists(registry_file):
                with open(registry_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Create default registry
                default_registry = {
                    "prefix_commands": {
                        ".murgi": {
                            "type": "sequential",
                            "description": "Send sequential chicken messages",
                            "category": "fun",
                            "enabled": True,
                            "cooldown": 60,
                            "admin_only": False
                        },
                        ".love": {
                            "type": "response",
                            "description": "Send romantic messages",
                            "category": "romantic",
                            "enabled": True,
                            "cooldown": 30,
                            "admin_only": False
                        },
                        ".pick": {
                            "type": "random",
                            "description": "Make a random selection",
                            "category": "fun",
                            "enabled": True,
                            "cooldown": 10,
                            "admin_only": False
                        },
                        ".dio": {
                            "type": "response",
                            "description": "Send DIO-themed messages",
                            "category": "fun",
                            "enabled": True,
                            "cooldown": 120,
                            "admin_only": False
                        },
                        ".info": {
                            "type": "info",
                            "description": "Show bot information",
                            "category": "utility",
                            "enabled": True,
                            "cooldown": 5,
                            "admin_only": False
                        },
                        ".uid": {
                            "type": "utility",
                            "description": "Get user ID",
                            "category": "utility",
                            "enabled": True,
                            "cooldown": 5,
                            "admin_only": False
                        },
                        ".diagram": {
                            "type": "special",
                            "description": "Create diagrams",
                            "category": "utility",
                            "enabled": True,
                            "cooldown": 30,
                            "admin_only": False
                        },
                        ".Ln": {
                            "type": "utility",
                            "description": "Line number system",
                            "category": "utility",
                            "enabled": True,
                            "cooldown": 5,
                            "admin_only": False
                        }
                    },
                    "admin_commands": {
                        "!add": {
                            "type": "management",
                            "description": "Add user to group",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 10,
                            "admin_only": True
                        },
                        "!delete": {
                            "type": "management",
                            "description": "Delete user",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 10,
                            "admin_only": True
                        },
                        "!kick": {
                            "type": "management",
                            "description": "Kick user from group",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 10,
                            "admin_only": True
                        },
                        "!out": {
                            "type": "management",
                            "description": "Leave group",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 30,
                            "admin_only": True
                        },
                        "!start": {
                            "type": "control",
                            "description": "Start bot/live stream",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 60,
                            "admin_only": True
                        },
                        "!stop": {
                            "type": "control",
                            "description": "Stop bot/command",
                            "category": "admin",
                            "enabled": True,
                            "cooldown": 5,
                            "admin_only": False
                        }
                    },
                    "nickname_commands": {
                        "Bot": {
                            "type": "response",
                            "description": "Respond to Bot nickname",
                            "category": "nickname",
                            "enabled": True,
                            "cooldown": 5
                        },
                        "bow": {
                            "type": "response",
                            "description": "Respond to bow nickname",
                            "category": "nickname",
                            "enabled": True,
                            "cooldown": 5
                        },
                        "Jan": {
                            "type": "response",
                            "description": "Respond to Jan nickname",
                            "category": "nickname",
                            "enabled": True,
                            "cooldown": 5
                        },
                        "Sona": {
                            "type": "response",
                            "description": "Respond to Sona nickname",
                            "category": "nickname",
                            "enabled": True,
                            "cooldown": 5
                        },
                        "Baby": {
                            "type": "response",
                            "description": "Respond to Baby nickname",
                            "category": "nickname",
                            "enabled": True,
                            "cooldown": 5
                        }
                    },
                    "command_stats": {},
                    "last_updated": time.time()
                }
                
                # Save default registry
                os.makedirs(os.path.dirname(registry_file), exist_ok=True)
                with open(registry_file, "w", encoding="utf-8") as f:
                    json.dump(default_registry, f, indent=2)
                
                return default_registry
                
        except Exception as e:
            self.logger.error(f"❌ Error loading command registry: {e}")
            return {}
    
    def _initialize_commands(self):
        """Initialize all command handlers"""
        # Prefix command handlers
        self.prefix_handlers = {
            ".murgi": self._handle_murgi_command,
            ".love": self._handle_love_command,
            ".pick": self._handle_pick_command,
            ".dio": self._handle_dio_command,
            ".diagram": self._handle_diagram_command,
            ".info": self._handle_info_command,
            ".uid": self._handle_uid_command,
            ".Ln": self._handle_ln_command
        }
        
        # Admin command handlers
        self.admin_handlers = {
            "add": self._handle_add_command,
            "delete": self._handle_delete_command,
            "kick": self._handle_kick_command,
            "out": self._handle_out_command,
            "start": self._handle_start_command,
            "stop": self._handle_stop_command
        }
        
        # Nickname handlers
        self.nickname_handlers = {
            "Bot": self._handle_nickname_bot,
            "bow": self._handle_nickname_bow,
            "Jan": self._handle_nickname_jan,
            "Sona": self._handle_nickname_sona,
            "Baby": self._handle_nickname_baby
        }
    
    def is_command(self, message: str) -> bool:
        """Check if message is a command"""
        if not message:
            return False
        
        message = message.strip()
        
        # Check for prefix commands
        if message.startswith("."):
            cmd = message.split()[0].lower()
            return cmd in self.prefix_handlers
        
        # Check for admin commands
        if message.startswith("!"):
            cmd = message.split()[0][1:].lower()
            return cmd in self.admin_handlers
        
        # Check for nicknames
        words = message.split()
        for word in words:
            if word in self.nickname_handlers:
                return True
        
        return False
    
    def execute_command(self, message: str, sender_id: str, thread_id: str, is_group: bool = False) -> Optional[str]:
        """Execute a command"""
        try:
            message = message.strip()
            
            # Check control commands first
            if message.lower() in ["stop!", "pause!", "resume!"]:
                return self._handle_control_command(message, sender_id)
            
            # Parse command type and name
            command_type, command_name = self._parse_command_type(message)
            
            if not command_type:
                return f"❌ Unknown command: {message}"
            
            # Check if command exists
            if not self._command_exists(command_type, command_name):
                return f"❌ Command not found: {message}"
            
            # Check if command is enabled
            if not self._is_command_enabled(command_type, command_name):
                return f"❌ Command is disabled: {message}"
            
            # Check cooldown
            cooldown_status = self._check_cooldown(command_type, command_name, sender_id)
            if not cooldown_status['allowed']:
                return f"⏳ Please wait {cooldown_status['remaining']:.1f}s before using {message} again"
            
            # Check permissions
            if not self._check_permissions(command_type, command_name, sender_id, is_group):
                return "❌ Permission denied"
            
            # Add to command history
            self._add_to_history(command_type, command_name, sender_id, thread_id, is_group, message)
            
            # Execute command based on type
            if command_type == "prefix":
                return self._handle_prefix_command(message, sender_id, thread_id, is_group)
            elif command_type == "admin":
                return self._handle_admin_command(message, sender_id, thread_id, is_group)
            elif command_type == "nickname":
                return self._handle_nickname_command(message, sender_id, thread_id, is_group)
            else:
                return f"❌ Unknown command type: {command_type}"
            
        except Exception as e:
            self.logger.error(f"❌ Error executing command: {e}")
            return f"❌ Command error: {str(e)}"
    
    def _parse_command_type(self, message: str):
        """Parse command type and name"""
        if message.startswith("."):
            return "prefix", message[1:].split()[0] if len(message) > 1 else ""
        elif message.startswith("!"):
            return "admin", message[1:].split()[0] if len(message) > 1 else ""
        else:
            # Check for nicknames
            words = message.split()
            for word in words:
                if word in self.nickname_handlers:
                    return "nickname", word
            return None, message
    
    def _command_exists(self, command_type: str, command_name: str) -> bool:
        """Check if command exists"""
        if command_type == "prefix":
            return f".{command_name}" in self.prefix_handlers
        elif command_type == "admin":
            return command_name in self.admin_handlers
        elif command_type == "nickname":
            return command_name in self.nickname_handlers
        return False
    
    def _is_command_enabled(self, command_type: str, command_name: str) -> bool:
        """Check if command is enabled"""
        registry_key = f"{command_type}_commands"
        if command_type == "prefix":
            cmd_key = f".{command_name}"
        elif command_type == "admin":
            cmd_key = f"!{command_name}"
        else:
            cmd_key = command_name
        
        cmd_info = self.command_registry.get(registry_key, {}).get(cmd_key, {})
        return cmd_info.get("enabled", True)
    
    def _check_cooldown(self, command_type: str, command_name: str, user_id: str) -> Dict:
        """Check command cooldown"""
        if command_type == "prefix":
            key = f".{command_name}"
        elif command_type == "admin":
            key = f"!{command_name}"
        else:
            key = command_name
        
        full_key = f"{user_id}_{key}"
        current_time = time.time()
        
        # Get cooldown duration
        registry_key = f"{command_type}_commands"
        cmd_info = self.command_registry.get(registry_key, {}).get(key, {})
        cooldown_duration = cmd_info.get("cooldown", 5)
        
        if full_key in self.cooldowns:
            last_used = self.cooldowns[full_key]
            elapsed = current_time - last_used
            
            if elapsed < cooldown_duration:
                return {
                    "allowed": False,
                    "remaining": cooldown_duration - elapsed,
                    "last_used": last_used
                }
        
        return {"allowed": True, "remaining": 0}
    
    def _check_permissions(self, command_type: str, command_name: str, 
                          user_id: str, is_group: bool) -> bool:
        """Check command permissions"""
        if command_type == "prefix":
            key = f".{command_name}"
        elif command_type == "admin":
            key = f"!{command_name}"
        else:
            key = command_name
        
        registry_key = f"{command_type}_commands"
        cmd_info = self.command_registry.get(registry_key, {}).get(key, {})
        
        # Check if admin only
        if cmd_info.get("admin_only", False):
            return self._check_admin_permission(user_id)
        
        # Check group restrictions
        if is_group:
            # Some commands might be restricted in groups
            restricted_in_groups = ["!out", "!kick"]
            if key in restricted_in_groups:
                return self._check_admin_permission(user_id)
        
        return True
    
    def _add_to_history(self, command_type: str, command_name: str, user_id: str,
                       thread_id: str, is_group: bool, message: str):
        """Add command to history"""
        history_entry = {
            "timestamp": time.time(),
            "command_type": command_type,
            "command_name": command_name,
            "user_id": user_id,
            "thread_id": thread_id,
            "is_group": is_group,
            "message": message,
            "murgi_active": self.murgi_execution["active"]
        }
        
        self.command_history.append(history_entry)
        
        # Limit history size
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
        
        # Update command stats
        self._update_command_stats(command_type, command_name, user_id)
    
    def _update_command_stats(self, command_type: str, command_name: str, user_id: str):
        """Update command statistics"""
        if command_type == "prefix":
            key = f".{command_name}"
        elif command_type == "admin":
            key = f"!{command_name}"
        else:
            key = command_name
        
        # Update cooldown
        full_key = f"{user_id}_{key}"
        self.cooldowns[full_key] = time.time()
        
        # Update command stats in registry
        stats_key = f"{command_type}_{command_name}"
        if "command_stats" not in self.command_registry:
            self.command_registry["command_stats"] = {}
        
        if stats_key not in self.command_registry["command_stats"]:
            self.command_registry["command_stats"][stats_key] = {
                "total_uses": 0,
                "last_used": None,
                "users": []
            }
        
        self.command_registry["command_stats"][stats_key]["total_uses"] += 1
        self.command_registry["command_stats"][stats_key]["last_used"] = time.time()
        
        if user_id not in self.command_registry["command_stats"][stats_key]["users"]:
            self.command_registry["command_stats"][stats_key]["users"].append(user_id)
        
        # Save registry
        self._save_command_registry()
        
        # Clean old cooldowns
        current_time = time.time()
        self.cooldowns = {
            k: v for k, v in self.cooldowns.items() 
            if current_time - v < 3600
        }
    
    def _save_command_registry(self):
        """Save command registry to file"""
        try:
            registry_file = "data/commands/command_registry.json"
            self.command_registry["last_updated"] = time.time()
            
            with open(registry_file, "w", encoding="utf-8") as f:
                json.dump(self.command_registry, f, indent=2)
        except Exception as e:
            self.logger.error(f"❌ Error saving command registry: {e}")
    
    def _handle_control_command(self, message: str, sender_id: str) -> str:
        """Handle control commands (stop!, pause!, resume!)"""
        command = message.lower()
        
        if command == "stop!":
            if self.murgi_execution["active"]:
                self.murgi_execution["active"] = False
                return "🛑 Murgi sequence stopped!"
            else:
                return "ℹ️ No active sequence to stop"
        
        elif command == "pause!":
            if self.murgi_execution["active"] and not self.murgi_execution["paused"]:
                self.murgi_execution["paused"] = True
                return "⏸️ Murgi sequence paused!"
            else:
                return "ℹ️ No active sequence to pause"
        
        elif command == "resume!":
            if self.murgi_execution["active"] and self.murgi_execution["paused"]:
                self.murgi_execution["paused"] = False
                return "▶️ Murgi sequence resumed!"
            else:
                return "ℹ️ No active sequence to resume"
        
        return f"❌ Unknown control command: {message}"
    
    def _handle_prefix_command(self, message: str, sender_id: str, thread_id: str, is_group: bool) -> Optional[str]:
        """Handle prefix commands starting with ."""
        try:
            parts = message.split()
            if not parts:
                return None
            
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Check if command exists
            if cmd in self.prefix_handlers:
                # Execute command
                response = self.prefix_handlers[cmd](args, sender_id, thread_id, is_group)
                return response
            else:
                return f"❌ Unknown command: {cmd}\n✅ Available: {', '.join(self.prefix_handlers.keys())}"
                
        except Exception as e:
            self.logger.error(f"❌ Error in prefix command: {e}")
            return f"❌ Command error: {str(e)}"
    
    def _handle_admin_command(self, message: str, sender_id: str, thread_id: str, is_group: bool) -> Optional[str]:
        """Handle admin commands starting with !"""
        try:
            parts = message.split()
            if not parts:
                return None
            
            cmd = parts[0][1:].lower()  # Remove ! prefix
            args = parts[1:] if len(parts) > 1 else []
            
            # Check if command exists
            if cmd in self.admin_handlers:
                # Execute command
                response = self.admin_handlers[cmd](args, sender_id, thread_id, is_group)
                return response
            else:
                return f"❌ Unknown admin command: {cmd}"
                
        except Exception as e:
            self.logger.error(f"❌ Error in admin command: {e}")
            return f"❌ Admin command error: {str(e)}"
    
    def _handle_nickname_command(self, message: str, sender_id: str, thread_id: str, is_group: bool) -> Optional[str]:
        """Handle nickname mentions"""
        try:
            words = message.split()
            
            for word in words:
                if word in self.nickname_handlers:
                    # Execute nickname handler
                    response = self.nickname_handlers[word](sender_id, thread_id, is_group)
                    return response
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error in nickname command: {e}")
            return None
    
    # ==================== PREFIX COMMAND HANDLERS ====================
    
    def _handle_murgi_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .murgi command with sequential execution and mentions"""
        try:
            # Check if murgi is already running
            if self.murgi_execution["active"]:
                return "🐔 Murgi command is already running! Use 'stop!' to stop."
            
            # Parse target user from mention
            target_user_id = sender_id  # Default to sender
            target_username = None
            
            # Check if there's a mention in args
            if args:
                # Try to extract user ID from mention
                for arg in args:
                    if arg.startswith('@'):
                        # This is a mention, extract user ID
                        mentioned_user = arg[1:]  # Remove @
                        # In real implementation, you would map username to user ID
                        # For now, we'll use a placeholder
                        target_username = mentioned_user
                        break
            
            # Get bot configuration
            from config.bot_config import get_config_value
            murgi_config = get_config_value("command_config.murgi", {})
            
            # Determine mention target
            mention_target = murgi_config.get("mention_target", "user")
            
            # Start murgi execution in separate thread
            self.murgi_execution["active"] = True
            self.murgi_execution["paused"] = False
            self.murgi_execution["target_user_id"] = target_user_id
            self.murgi_execution["target_username"] = target_username
            self.murgi_execution["original_sender"] = sender_id
            self.murgi_execution["mention_target"] = mention_target
            
            # Start execution thread
            thread = threading.Thread(
                target=self._execute_murgi_sequence_with_mentions,
                args=(sender_id, thread_id, target_user_id, target_username, mention_target),
                daemon=True
            )
            
            self.murgi_execution["thread"] = thread
            thread.start()
            
            if target_username:
                return f"🐔 Starting murgi sequence for @{target_username}... (Type 'stop!' to stop)"
            else:
                return "🐔 Starting murgi sequence... (Type 'stop!' to stop)"
            
        except Exception as e:
            self.murgi_execution["active"] = False
            self.logger.error(f"❌ Error in murgi command: {e}")
            return f"❌ Murgi command error: {str(e)}"
    
    def _execute_murgi_sequence_with_mentions(self, sender_id: str, thread_id: str, 
                                            target_user_id: str, target_username: str,
                                            mention_target: str):
        """Execute murgi sequence with mentions"""
        try:
            murgi_folder = "data/commands/prefix/murgi/"
            
            # Version files to execute
            version_files = ["v1.txt", "v2.txt", "v3.txt"]
            
            for version_file in version_files:
                file_path = os.path.join(murgi_folder, version_file)
                
                if not os.path.exists(file_path):
                    self.logger.warning(f"⚠️ Murgi file not found: {file_path}")
                    continue
                
                # Read lines from file
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                
                if not lines:
                    continue
                
                # Update execution info
                self.murgi_execution["current_file"] = version_file
                self.murgi_execution["total_lines"] = len(lines)
                
                # Send each line with delay and mention
                for i, line in enumerate(lines):
                    # Check if stopped
                    if not self.murgi_execution["active"]:
                        break
                    
                    # Check if paused
                    while self.murgi_execution["paused"] and self.murgi_execution["active"]:
                        time.sleep(1)
                    
                    if not self.murgi_execution["active"]:
                        break
                    
                    # Update current line
                    self.murgi_execution["current_line"] = i + 1
                    
                    # Format message with mention
                    final_message = self._format_murgi_message(
                        line, 
                        target_username, 
                        mention_target,
                        i + 1,
                        len(lines)
                    )
                    
                    # Send line (in real implementation, you would send via messenger)
                    self.logger.info(f"🐔 Murgi line {i+1}/{len(lines)}: {final_message}")
                    
                    # In actual implementation, send via messenger
                    # self.messenger.send_message(thread_id, final_message)
                    
                    # Wait before next line
                    time.sleep(2)  # 2 second delay between lines
                
                # Wait between versions
                if self.murgi_execution["active"] and version_file != version_files[-1]:
                    time.sleep(5)  # 5 second delay between versions
            
            # Reset execution state
            self.murgi_execution["active"] = False
            self.murgi_execution["current_file"] = None
            self.murgi_execution["current_line"] = 0
            self.murgi_execution["total_lines"] = 0
            self.murgi_execution["target_user_id"] = None
            self.murgi_execution["target_username"] = None
            
            self.logger.info("✅ Murgi sequence completed!")
            
        except Exception as e:
            self.logger.error(f"❌ Error in murgi execution: {e}")
            self.murgi_execution["active"] = False
    
    def _format_murgi_message(self, line: str, target_username: str, 
                             mention_target: str, current_line: int, 
                             total_lines: int) -> str:
        """Format murgi message with mention"""
        try:
            from config.bot_config import get_config_value
            
            murgi_config = get_config_value("command_config.murgi", {})
            mention_format = murgi_config.get("mention_format", "@{user} {message}")
            mention_in_every = murgi_config.get("mention_in_every_message", True)
            
            # Add line number if configured
            show_line_numbers = murgi_config.get("show_line_numbers", False)
            if show_line_numbers:
                line = f"{current_line}/{total_lines}. {line}"
            
            # Format based on mention target
            if mention_target == "user" and target_username and mention_in_every:
                return mention_format.format(user=target_username, message=line)
            elif mention_target == "admin":
                # Mention admin instead
                admin_name = self._get_admin_name()
                return mention_format.format(user=admin_name, message=line)
            elif mention_target == "both" and target_username:
                # Mention both user and admin
                admin_name = self._get_admin_name()
                return f"@{target_username} @{admin_name} {line}"
            else:
                # No mention
                return line
                
        except Exception as e:
            self.logger.error(f"❌ Error formatting murgi message: {e}")
            return line
    
    def _get_admin_name(self) -> str:
        """Get admin name for mention"""
        try:
            # Load admin config
            admin_file = "config/admin_config.py"
            if os.path.exists(admin_file):
                import config.admin_config as admin_config
                admin_name = getattr(admin_config, "ADMIN_NAME", "Admin")
                return admin_name
            return "Admin"
        except:
            return "Admin"
    
    def _handle_love_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .love command"""
        try:
            responses_file = "data/commands/prefix/love/responses.txt"
            
            if os.path.exists(responses_file):
                with open(responses_file, "r", encoding="utf-8") as f:
                    responses = [line.strip() for line in f.readlines() if line.strip()]
                
                if responses:
                    response = random.choice(responses)
                    return f"💖 {response}"
                else:
                    return "💖 I love you too!"
            else:
                # Default responses
                love_responses = [
                    "💖 তোমাকে অনেক ভালোবাসি!",
                    "💕 তুমি আমার সবচেয়ে প্রিয়!",
                    "❤️ তোমার জন্য我的心 (আমার মন)!",
                    "💘 তুমি আমার জীবনের আলো!",
                    "💝 তোমার সাথে থাকতে চাই চিরকাল!"
                ]
                return random.choice(love_responses)
                
        except Exception as e:
            self.logger.error(f"❌ Error in love command: {e}")
            return "💖 I love you!"
    
    def _handle_pick_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .pick command"""
        try:
            picks_file = "data/commands/prefix/pick/picks.txt"
            
            if os.path.exists(picks_file):
                with open(picks_file, "r", encoding="utf-8") as f:
                    picks = [line.strip() for line in f.readlines() if line.strip()]
                
                if picks:
                    if args:
                        # Pick specific number of items
                        try:
                            count = min(int(args[0]), len(picks), 10)  # Max 10 picks
                            selected = random.sample(picks, count)
                            return "🎯 Selected:\n" + "\n".join([f"• {item}" for item in selected])
                        except:
                            pick = random.choice(picks)
                            return f"🎯 {pick}"
                    else:
                        pick = random.choice(picks)
                        return f"🎯 {pick}"
                else:
                    return "🎯 Nothing to pick from!"
            else:
                return "🎯 Pick list is empty!"
                
        except Exception as e:
            self.logger.error(f"❌ Error in pick command: {e}")
            return "🎯 Pick error!"
    
    def _handle_dio_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .dio command"""
        try:
            dio_file = "data/commands/prefix/dio/dio_lines.txt"
            
            if os.path.exists(dio_file):
                with open(dio_file, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                
                if lines:
                    line = random.choice(lines)
                    return f"🦸‍♂️ {line}"
                else:
                    return "🦸‍♂️ WRYYYYYYYY!"
            else:
                return "🦸‍♂️ You thought it was Dio, but it was me!"
                
        except Exception as e:
            self.logger.error(f"❌ Error in dio command: {e}")
            return "🦸‍♂️ KONO DIO DA!"
    
    def _handle_diagram_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .diagram command"""
        try:
            types_file = "data/commands/prefix/diagram/types.txt"
            
            if os.path.exists(types_file):
                with open(types_file, "r", encoding="utf-8") as f:
                    types = [line.strip() for line in f.readlines() if line.strip()]
                
                if types:
                    diagram_type = random.choice(types)
                    return f"📊 Creating {diagram_type} diagram..."
                else:
                    return "📊 Available diagrams: flowchart, sequence, class"
            else:
                return "📊 Diagram system ready!"
                
        except Exception as e:
            self.logger.error(f"❌ Error in diagram command: {e}")
            return "📊 Diagram error!"
    
    def _handle_info_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .info command"""
        try:
            info_text = """
            🤖 𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0 - INFORMATION
            
            👑 Author: MAR PD (RANA)
            📅 Version: 1.0.0
            🎯 Purpose: Your AI Crush Bot
            
            💖 Features:
            • AI-powered responses
            • Photo delivery system
            • Learning from users
            • Multiple commands
            • Group management
            
            ⚡ Commands:
            • .murgi - Sequential chicken messages
            • .love - Romantic messages
            • .pick - Random picks
            • .dio - DIO character lines
            • .info - This information
            
            📞 Contact:
            • Telegram: @rana_editz_00
            • Phone: 01847634486
            
            💾 Status: Active and ready to chat!
            """
            
            return info_text
            
        except Exception as e:
            self.logger.error(f"❌ Error in info command: {e}")
            return "🤖 Bot information"
    
    def _handle_uid_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .uid command"""
        try:
            if args:
                # Get UID for mentioned user
                mention = args[0]
                # In real implementation, extract UID from mention
                return f"🔢 User ID for {mention}: {sender_id} (placeholder)"
            else:
                return f"🔢 Your ID: {sender_id}"
                
        except Exception as e:
            self.logger.error(f"❌ Error in uid command: {e}")
            return f"🔢 ID: {sender_id}"
    
    def _handle_ln_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle .Ln command (Line number system)"""
        try:
            if args:
                line_num = int(args[0])
                return f"📝 Line {line_num}: This is a sample line"
            else:
                return "📝 Line number system. Usage: .Ln [number]"
                
        except Exception as e:
            self.logger.error(f"❌ Error in Ln command: {e}")
            return "📝 Line command error"
    
    # ==================== ADMIN COMMAND HANDLERS ====================
    
    def _handle_add_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle add command"""
        try:
            if not args:
                return "➕ Usage: !add [user/pick/url]"
            
            add_type = args[0].lower()
            
            if add_type == "user" and len(args) > 1:
                user = args[1]
                return f"👤 Added user: {user}"
            
            elif add_type == "pick" and len(args) > 1:
                pick_text = " ".join(args[1:])
                return f"🎯 Added pick: {pick_text}"
            
            elif add_type == "url" and len(args) > 1:
                url = args[1]
                return f"🔗 Added URL: {url}"
            
            else:
                return "➕ Usage: !add [user @mention | pick text | url link]"
                
        except Exception as e:
            self.logger.error(f"❌ Error in add command: {e}")
            return f"❌ Add error: {str(e)}"
    
    def _handle_delete_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle delete command"""
        try:
            if not args:
                return "🗑️ Usage: !delete [user/id]"
            
            delete_type = args[0].lower()
            
            if delete_type == "user" and len(args) > 1:
                user = args[1]
                return f"👤 Deleted user: {user}"
            
            elif delete_type == "pick" and len(args) > 1:
                pick_id = args[1]
                return f"🎯 Deleted pick ID: {pick_id}"
            
            else:
                return "🗑️ Usage: !delete [user @mention | pick id]"
                
        except Exception as e:
            self.logger.error(f"❌ Error in delete command: {e}")
            return f"❌ Delete error: {str(e)}"
    
    def _handle_kick_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle kick command"""
        try:
            if not args:
                return "👢 Usage: !kick @mention"
            
            user = args[0]
            return f"👢 Kicked user: {user}"
            
        except Exception as e:
            self.logger.error(f"❌ Error in kick command: {e}")
            return f"❌ Kick error: {str(e)}"
    
    def _handle_out_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle out command"""
        try:
            if args and args[0].lower() == "admin":
                return "👑 Bot leaving as admin..."
            else:
                return "🚪 Bot leaving group..."
                
        except Exception as e:
            self.logger.error(f"❌ Error in out command: {e}")
            return f"❌ Out error: {str(e)}"
    
    def _handle_start_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle start command"""
        try:
            if args and "live" in " ".join(args).lower():
                return "🚀 Starting live stream..."
            else:
                return "🚀 Bot starting..."
                
        except Exception as e:
            self.logger.error(f"❌ Error in start command: {e}")
            return f"❌ Start error: {str(e)}"
    
    def _handle_stop_command(self, args: List[str], sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle stop command - stops active commands"""
        try:
            # Stop murgi execution
            if self.murgi_execution["active"]:
                self.murgi_execution["active"] = False
                return "⏹️ Stopped active command!"
            
            # Stop other active commands
            stopped = False
            for cmd_id, cmd_data in self.active_commands.items():
                if cmd_data.get("active", False):
                    cmd_data["active"] = False
                    stopped = True
            
            if stopped:
                return "⏹️ Stopped all active commands!"
            else:
                return "⏹️ No active commands to stop!"
                
        except Exception as e:
            self.logger.error(f"❌ Error in stop command: {e}")
            return f"❌ Stop error: {str(e)}"
    
    # ==================== NICKNAME HANDLERS ====================
    
    def _handle_nickname_bot(self, sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle 'Bot' nickname"""
        responses = [
            "🤖 Yes, I am your Bot!",
            "🤖 বট এখানে আছি!",
            "🤖 হ্যাঁ বলুন!",
            "🤖 কি বলছেন?",
            "🤖 আমি শুনছি!"
        ]
        return random.choice(responses)
    
    def _handle_nickname_bow(self, sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle 'bow' nickname"""
        responses = [
            "🏹 Yes boss?",
            "🏹 বলুন বস!",
            "🏹 কি হুকুম?",
            "🏹 হ্যাঁ বলুন!"
        ]
        return random.choice(responses)
    
    def _handle_nickname_jan(self, sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle 'Jan' nickname"""
        responses = [
            "👨 Yes Jan?",
            "👨 হ্যাঁ জান?",
            "👨 কি বলছ জান?",
            "👨 শুনছি জান!"
        ]
        return random.choice(responses)
    
    def _handle_nickname_sona(self, sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle 'Sona' nickname"""
        responses = [
            "👸 Yes Sona?",
            "👸 হ্যাঁ সোনা?",
            "👸 কি বলছ সোনা?",
            "👸 শুনছি সোনা!"
        ]
        return random.choice(responses)
    
    def _handle_nickname_baby(self, sender_id: str, thread_id: str, is_group: bool) -> str:
        """Handle 'Baby' nickname"""
        responses = [
            "👶 Yes Baby?",
            "👶 হ্যাঁ বেবি?",
            "👶 কি বলছ বেবি?",
            "👶 শুনছি বেবি!"
        ]
        return random.choice(responses)
    
    # ==================== HELPER METHODS ====================
    
    def _check_admin_permission(self, user_id: str) -> bool:
        """Check if user has admin permission"""
        try:
            admin_file = "config/admin_config.py"
            
            if os.path.exists(admin_file):
                # Load admin list
                import config.admin_config as admin_config
                admin_ids = getattr(admin_config, "ADMIN_IDS", [])
                
                return user_id in admin_ids
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error checking admin permission: {e}")
            return False
    
    def stop_murgi(self):
        """Stop murgi execution"""
        if self.murgi_execution["active"]:
            self.murgi_execution["active"] = False
            self.logger.info("⏹️ Murgi execution stopped")
            return True
        return False
    
    def pause_murgi(self):
        """Pause murgi execution"""
        if self.murgi_execution["active"] and not self.murgi_execution["paused"]:
            self.murgi_execution["paused"] = True
            self.logger.info("⏸️ Murgi execution paused")
            return True
        return False
    
    def resume_murgi(self):
        """Resume murgi execution"""
        if self.murgi_execution["active"] and self.murgi_execution["paused"]:
            self.murgi_execution["paused"] = False
            self.logger.info("▶️ Murgi execution resumed")
            return True
        return False
    
    def get_command_status(self) -> Dict:
        """Get command processor status"""
        return {
            "active_commands": len(self.active_commands),
            "murgi_active": self.murgi_execution["active"],
            "murgi_paused": self.murgi_execution["paused"],
            "murgi_progress": f"{self.murgi_execution['current_line']}/{self.murgi_execution['total_lines']}",
            "command_history_count": len(self.command_history),
            "total_commands_executed": sum(self.command_registry.get("command_stats", {}).values()),
            "cooldown_count": len(self.cooldowns)
        }
    
    def get_available_commands(self, user_id: str, is_group: bool = False) -> List[Dict]:
        """Get list of available commands for user"""
        available = []
        
        # Prefix commands
        for cmd_key, cmd_info in self.command_registry.get("prefix_commands", {}).items():
            if cmd_info.get("enabled", True):
                command_name = cmd_key[1:]  # Remove .
                if self._check_permissions("prefix", command_name, user_id, is_group):
                    available.append({
                        "command": cmd_key,
                        "description": cmd_info.get("description", "No description"),
                        "type": "prefix",
                        "category": cmd_info.get("category", "general"),
                        "cooldown": cmd_info.get("cooldown", 5)
                    })
        
        # Admin commands (if user is admin)
        if self._check_admin_permission(user_id):
            for cmd_key, cmd_info in self.command_registry.get("admin_commands", {}).items():
                if cmd_info.get("enabled", True):
                    command_name = cmd_key[1:]  # Remove !
                    available.append({
                        "command": cmd_key,
                        "description": cmd_info.get("description", "No description"),
                        "type": "admin",
                        "category": cmd_info.get("category", "admin"),
                        "cooldown": cmd_info.get("cooldown", 10)
                    })
        
        # Nickname commands
        for nickname, cmd_info in self.command_registry.get("nickname_commands", {}).items():
            if cmd_info.get("enabled", True):
                available.append({
                    "command": nickname,
                    "description": cmd_info.get("description", "No description"),
                    "type": "nickname",
                    "category": cmd_info.get("category", "nickname"),
                    "cooldown": cmd_info.get("cooldown", 5)
                })
        
        return available


# Test the CommandProcessor
if __name__ == "__main__":
    print("⚡ Command Processor Clean Version")
    print("=" * 50)
    
    # Create instance
    processor = CommandProcessor()
    
    # Test basic functionality
    test_commands = [
        ".info",
        ".love",
        ".pick red blue green",
        "Bot",
        "stop!"
    ]
    
    print("\n🧪 Testing commands:")
    for cmd in test_commands:
        result = processor.execute_command(cmd, "test_user_123", "test_thread_456", False)
        print(f"💬 {cmd} -> {result}")
    
    # Show status
    status = processor.get_command_status()
    print(f"\n📊 Status: {status}")
    
    print("\n✅ Command Processor is ready!")