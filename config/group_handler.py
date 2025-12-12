#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👥 Group Management System
Facebook group handling and management
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Set

from utils.logger import setup_logger
from utils.file_handler import FileHandler


class GroupHandler:
    """👥 Group Management System"""
    
    def __init__(self, messenger=None):
        self.logger = setup_logger("group_handler", "data/logs/group_management.log")
        self.file_handler = FileHandler()
        self.messenger = messenger
        
        # Group data storage
        self.group_list = {}           # group_id -> group_info
        self.group_settings = {}       # group_id -> settings
        self.group_members = {}        # group_id -> [member_ids]
        self.group_messages = {}       # group_id -> [message_history]
        
        # Group state
        self.joined_groups = set()     # Currently joined groups
        self.group_admins = {}         # group_id -> [admin_ids]
        
        # Initialize
        self.initialize()
    
    def initialize(self):
        """Initialize group management system"""
        try:
            self.logger.info("👥 Initializing Group Management System...")
            
            # Load group data
            self._load_all_group_data()
            
            self.logger.info(f"✅ Group Management initialized: {len(self.group_list)} groups")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing group management: {e}")
    
    def _load_all_group_data(self):
        """Load all group data from files"""
        try:
            # Group list
            groups_file = "data/groups/group_list.json"
            if os.path.exists(groups_file):
                with open(groups_file, "r", encoding="utf-8") as f:
                    self.group_list = json.load(f)
            else:
                self.group_list = {}
            
            # Group settings
            settings_file = "data/groups/group_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, "r", encoding="utf-8") as f:
                    self.group_settings = json.load(f)
            else:
                self.group_settings = {}
            
            # Group members
            members_file = "data/groups/group_members.json"
            if os.path.exists(members_file):
                with open(members_file, "r", encoding="utf-8") as f:
                    self.group_members = json.load(f)
            else:
                self.group_members = {}
            
            # Group admins
            admins_file = "data/groups/group_admins.json"
            if os.path.exists(admins_file):
                with open(admins_file, "r", encoding="utf-8") as f:
                    self.group_admins = json.load(f)
            else:
                self.group_admins = {}
            
            # Load joined groups
            joined_file = "data/groups/joined_groups.json"
            if os.path.exists(joined_file):
                with open(joined_file, "r", encoding="utf-8") as f:
                    joined_data = json.load(f)
                    self.joined_groups = set(joined_data.get("joined_groups", []))
            
            self.logger.info(f"✅ Loaded group data: {len(self.group_list)} groups")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading group data: {e}")
    
    def _save_group_data(self, data_type: str, data: Dict):
        """Save group data to file"""
        try:
            filename = f"data/groups/group_{data_type}.json"
            self.file_handler.write_json(filename, data)
            self.logger.debug(f"Saved group {data_type}")
        except Exception as e:
            self.logger.error(f"Error saving group {data_type}: {e}")
    
    def join_group(self, group_id: str, group_name: str = None, invite_link: str = None) -> bool:
        """Join a Facebook group"""
        try:
            if group_id in self.joined_groups:
                self.logger.warning(f"Already joined group: {group_id}")
                return True
            
            self.logger.info(f"Joining group: {group_id}")
            
            # Add to joined groups
            self.joined_groups.add(group_id)
            self._save_joined_groups()
            
            # Create group entry if not exists
            if group_id not in self.group_list:
                group_info = {
                    "group_id": group_id,
                    "name": group_name or f"Group {group_id[-6:]}",
                    "invite_link": invite_link,
                    "joined_at": datetime.now().isoformat(),
                    "last_activity": datetime.now().isoformat(),
                    "message_count": 0,
                    "member_count": 0,
                    "status": "joined"
                }
                self.group_list[group_id] = group_info
            else:
                # Update existing entry
                self.group_list[group_id]["status"] = "joined"
                self.group_list[group_id]["last_activity"] = datetime.now().isoformat()
            
            # Create default settings if not exists
            if group_id not in self.group_settings:
                self.group_settings[group_id] = self._get_default_group_settings()
            
            # Initialize members list if not exists
            if group_id not in self.group_members:
                self.group_members[group_id] = []
            
            # Initialize admins list if not exists
            if group_id not in self.group_admins:
                self.group_admins[group_id] = []
            
            # Save all data
            self.save_all_group_data()
            
            self.logger.info(f"✅ Joined group: {group_name or group_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error joining group: {e}")
            return False
    
    def leave_group(self, group_id: str) -> bool:
        """Leave a Facebook group"""
        try:
            if group_id not in self.joined_groups:
                self.logger.warning(f"Not joined to group: {group_id}")
                return True
            
            self.logger.info(f"Leaving group: {group_id}")
            
            # Remove from joined groups
            self.joined_groups.remove(group_id)
            self._save_joined_groups()
            
            # Update group status
            if group_id in self.group_list:
                self.group_list[group_id]["status"] = "left"
                self.group_list[group_id]["left_at"] = datetime.now().isoformat()
            
            # Save data
            self.save_all_group_data()
            
            self.logger.info(f"✅ Left group: {group_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error leaving group: {e}")
            return False
    
    def _save_joined_groups(self):
        """Save joined groups list"""
        try:
            joined_data = {
                "joined_groups": list(self.joined_groups),
                "last_updated": datetime.now().isoformat()
            }
            self.file_handler.write_json("data/groups/joined_groups.json", joined_data)
        except Exception as e:
            self.logger.error(f"Error saving joined groups: {e}")
    
    def _get_default_group_settings(self) -> Dict:
        """Get default group settings"""
        return {
            "bot_behavior": {
                "auto_reply": True,
                "reply_to_mentions": True,
                "reply_to_all": False,
                "send_welcome_message": True,
                "send_goodbye_message": True,
                "share_content": False,
                "auto_react": False
            },
            "message_settings": {
                "response_delay": 3,
                "max_messages_per_hour": 20,
                "min_message_interval": 10,
                "allow_commands": True,
                "allow_photos": True,
                "allow_links": True
            },
            "content_filter": {
                "filter_profanity": True,
                "filter_spam": True,
                "filter_links": False,
                "require_admin_approval": False
            },
            "admin_settings": {
                "admin_commands_only": False,
                "notify_admins": True,
                "log_all_messages": False
            }
        }
    
    def get_group_info(self, group_id: str) -> Optional[Dict]:
        """Get group information"""
        return self.group_list.get(group_id)
    
    def update_group_info(self, group_id: str, updates: Dict) -> bool:
        """Update group information"""
        try:
            if group_id not in self.group_list:
                self.logger.warning(f"Group not found: {group_id}")
                return False
            
            self.group_list[group_id].update(updates)
            self.group_list[group_id]["last_updated"] = datetime.now().isoformat()
            
            self._save_group_data("list", self.group_list)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error updating group info: {e}")
            return False
    
    def get_group_settings(self, group_id: str) -> Dict:
        """Get group settings"""
        if group_id in self.group_settings:
            return self.group_settings[group_id]
        else:
            return self._get_default_group_settings()
    
    def update_group_settings(self, group_id: str, category: str, setting: str, value: Any) -> bool:
        """Update group setting"""
        try:
            if group_id not in self.group_settings:
                self.group_settings[group_id] = self._get_default_group_settings()
            
            # Update setting
            if category in self.group_settings[group_id]:
                if setting in self.group_settings[group_id][category]:
                    self.group_settings[group_id][category][setting] = value
                else:
                    # Create new setting
                    self.group_settings[group_id][category][setting] = value
            else:
                # Create new category
                self.group_settings[group_id][category] = {setting: value}
            
            self._save_group_data("settings", self.group_settings)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error updating group settings: {e}")
            return False
    
    def add_group_member(self, group_id: str, user_id: str, role: str = "member") -> bool:
        """Add member to group"""
        try:
            if group_id not in self.group_members:
                self.group_members[group_id] = []
            
            # Check if already exists
            for member in self.group_members[group_id]:
                if member.get("user_id") == user_id:
                    # Update role
                    member["role"] = role
                    member["last_seen"] = datetime.now().isoformat()
                    return True
            
            # Add new member
            member_info = {
                "user_id": user_id,
                "role": role,
                "joined_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "message_count": 0
            }
            
            self.group_members[group_id].append(member_info)
            
            # Update member count
            if group_id in self.group_list:
                self.group_list[group_id]["member_count"] = len(self.group_members[group_id])
            
            # Add to admins list if role is admin
            if role == "admin":
                self.add_group_admin(group_id, user_id)
            
            self.logger.debug(f"Added member to group {group_id}: {user_id} ({role})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error adding group member: {e}")
            return False
    
    def remove_group_member(self, group_id: str, user_id: str) -> bool:
        """Remove member from group"""
        try:
            if group_id not in self.group_members:
                return False
            
            # Find and remove member
            for i, member in enumerate(self.group_members[group_id]):
                if member.get("user_id") == user_id:
                    self.group_members[group_id].pop(i)
                    
                    # Update member count
                    if group_id in self.group_list:
                        self.group_list[group_id]["member_count"] = len(self.group_members[group_id])
                    
                    # Remove from admins if exists
                    if user_id in self.group_admins.get(group_id, []):
                        self.remove_group_admin(group_id, user_id)
                    
                    self.logger.debug(f"Removed member from group {group_id}: {user_id}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error removing group member: {e}")
            return False
    
    def get_group_members(self, group_id: str) -> List[Dict]:
        """Get group members"""
        return self.group_members.get(group_id, [])
    
    def get_group_member(self, group_id: str, user_id: str) -> Optional[Dict]:
        """Get specific group member"""
        if group_id in self.group_members:
            for member in self.group_members[group_id]:
                if member.get("user_id") == user_id:
                    return member
        return None
    
    def update_member_activity(self, group_id: str, user_id: str):
        """Update member last seen"""
        try:
            member = self.get_group_member(group_id, user_id)
            if member:
                member["last_seen"] = datetime.now().isoformat()
                member["message_count"] = member.get("message_count", 0) + 1
                
                # Update group last activity
                if group_id in self.group_list:
                    self.group_list[group_id]["last_activity"] = datetime.now().isoformat()
                    self.group_list[group_id]["message_count"] = self.group_list[group_id].get("message_count", 0) + 1
        except Exception as e:
            self.logger.error(f"Error updating member activity: {e}")
    
    def add_group_admin(self, group_id: str, user_id: str) -> bool:
        """Add admin to group"""
        try:
            if group_id not in self.group_admins:
                self.group_admins[group_id] = []
            
            if user_id not in self.group_admins[group_id]:
                self.group_admins[group_id].append(user_id)
                self.logger.debug(f"Added admin to group {group_id}: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error adding group admin: {e}")
            return False
    
    def remove_group_admin(self, group_id: str, user_id: str) -> bool:
        """Remove admin from group"""
        try:
            if group_id in self.group_admins and user_id in self.group_admins[group_id]:
                self.group_admins[group_id].remove(user_id)
                self.logger.debug(f"Removed admin from group {group_id}: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error removing group admin: {e}")
            return False
    
    def get_group_admins(self, group_id: str) -> List[str]:
        """Get group admins"""
        return self.group_admins.get(group_id, [])
    
    def is_group_admin(self, group_id: str, user_id: str) -> bool:
        """Check if user is group admin"""
        return group_id in self.group_admins and user_id in self.group_admins[group_id]
    
    def log_group_message(self, group_id: str, sender_id: str, message: str, message_type: str = "text"):
        """Log group message"""
        try:
            # Initialize message history if not exists
            if "group_messages" not in locals():
                self.group_messages = self._load_group_messages()
            
            if group_id not in self.group_messages:
                self.group_messages[group_id] = []
            
            # Create message record
            message_record = {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "sender_id": sender_id,
                "message": message[:500],  # Limit length
                "message_type": message_type,
                "bot_replied": False
            }
            
            # Add to history
            self.group_messages[group_id].append(message_record)
            
            # Keep only last 100 messages per group
            if len(self.group_messages[group_id]) > 100:
                self.group_messages[group_id] = self.group_messages[group_id][-100:]
            
            # Update member activity
            self.update_member_activity(group_id, sender_id)
            
            # Save periodically
            if len(self.group_messages[group_id]) % 10 == 0:
                self._save_group_messages()
            
        except Exception as e:
            self.logger.error(f"❌ Error logging group message: {e}")
    
    def _load_group_messages(self) -> Dict:
        """Load group messages from file"""
        try:
            messages_file = "data/groups/group_messages.json"
            if os.path.exists(messages_file):
                with open(messages_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Error loading group messages: {e}")
            return {}
    
    def _save_group_messages(self):
        """Save group messages to file"""
        try:
            messages_file = "data/groups/group_messages.json"
            self.file_handler.write_json(messages_file, self.group_messages)
        except Exception as e:
            self.logger.error(f"Error saving group messages: {e}")
    
    def get_group_message_history(self, group_id: str, limit: int = 20) -> List[Dict]:
        """Get group message history"""
        if group_id in self.group_messages:
            return self.group_messages[group_id][-limit:] if limit > 0 else self.group_messages[group_id]
        return []
    
    def get_active_groups(self, hours: int = 24, limit: int = 20) -> List[Dict]:
        """Get recently active groups"""
        try:
            cutoff_time = time.time() - (hours * 3600)
            active_groups = []
            
            for group_id, group_info in self.group_list.items():
                last_activity = group_info.get("last_activity")
                if last_activity:
                    try:
                        last_time = datetime.fromisoformat(last_activity).timestamp()
                        if last_time > cutoff_time:
                            active_groups.append({
                                "group_id": group_id,
                                "name": group_info.get("name", "Unknown"),
                                "last_activity": last_activity,
                                "member_count": group_info.get("member_count", 0),
                                "message_count": group_info.get("message_count", 0),
                                "status": group_info.get("status", "unknown")
                            })
                    except:
                        continue
            
            # Sort by last activity (newest first)
            active_groups.sort(key=lambda x: x.get("last_activity", ""), reverse=True)
            
            return active_groups[:limit] if limit > 0 else active_groups
            
        except Exception as e:
            self.logger.error(f"❌ Error getting active groups: {e}")
            return []
    
    def get_joined_groups(self) -> List[Dict]:
        """Get list of joined groups"""
        joined_groups = []
        for group_id in self.joined_groups:
            group_info = self.group_list.get(group_id, {})
            joined_groups.append({
                "group_id": group_id,
                "name": group_info.get("name", "Unknown"),
                "joined_at": group_info.get("joined_at"),
                "member_count": group_info.get("member_count", 0),
                "message_count": group_info.get("message_count", 0)
            })
        return joined_groups
    
    def search_groups(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for groups"""
        try:
            results = []
            query_lower = query.lower()
            
            for group_id, group_info in self.group_list.items():
                name = group_info.get("name", "").lower()
                
                if query_lower in name:
                    results.append({
                        "group_id": group_id,
                        "name": group_info.get("name", ""),
                        "member_count": group_info.get("member_count", 0),
                        "message_count": group_info.get("message_count", 0),
                        "status": group_info.get("status", "unknown"),
                        "last_activity": group_info.get("last_activity", "")
                    })
                
                if len(results) >= limit:
                    break
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching groups: {e}")
            return []
    
    def save_all_group_data(self):
        """Save all group data to files"""
        try:
            self._save_group_data("list", self.group_list)
            self._save_group_data("settings", self.group_settings)
            self._save_group_data("members", self.group_members)
            self._save_group_data("admins", self.group_admins)
            self._save_joined_groups()
            
            self.logger.debug("Saved all group data")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving group data: {e}")
    
    def get_group_stats(self) -> Dict:
        """Get group statistics"""
        try:
            total_groups = len(self.group_list)
            joined_groups = len(self.joined_groups)
            
            # Count by status
            status_count = {}
            for group_info in self.group_list.values():
                status = group_info.get("status", "unknown")
                status_count[status] = status_count.get(status, 0) + 1
            
            # Total members across all groups
            total_members = 0
            total_messages = 0
            
            for group_info in self.group_list.values():
                total_members += group_info.get("member_count", 0)
                total_messages += group_info.get("message_count", 0)
            
            # Active groups (last 7 days)
            week_ago = time.time() - (7 * 86400)
            active_groups = 0
            
            for group_info in self.group_list.values():
                last_activity = group_info.get("last_activity")
                if last_activity:
                    try:
                        last_time = datetime.fromisoformat(last_activity).timestamp()
                        if last_time > week_ago:
                            active_groups += 1
                    except:
                        pass
            
            return {
                "total_groups": total_groups,
                "joined_groups": joined_groups,
                "active_groups_7days": active_groups,
                "total_members": total_members,
                "total_messages": total_messages,
                "status_distribution": status_count,
                "average_members_per_group": total_members / max(total_groups, 1),
                "average_messages_per_group": total_messages / max(total_groups, 1),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting group stats: {e}")
            return {}
    
    def backup_group_data(self) -> str:
        """Create backup of group data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"data/groups/backups/groups_{timestamp}"
            
            os.makedirs(backup_dir, exist_ok=True)
            
            # Files to backup
            files_to_backup = [
                "data/groups/group_list.json",
                "data/groups/group_settings.json",
                "data/groups/group_members.json",
                "data/groups/group_admins.json",
                "data/groups/joined_groups.json",
                "data/groups/group_messages.json"
            ]
            
            import shutil
            for source in files_to_backup:
                if os.path.exists(source):
                    shutil.copy2(source, backup_dir)
            
            # Compress backup
            backup_zip = f"{backup_dir}.zip"
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            shutil.rmtree(backup_dir)  # Remove uncompressed version
            
            self.logger.info(f"Group backup created: {backup_zip}")
            return backup_zip
            
        except Exception as e:
            self.logger.error(f"❌ Error backing up group data: {e}")
            return ""