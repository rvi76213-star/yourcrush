#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👥 User Management System
User profiles, preferences, and management
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set

from utils.logger import setup_logger
from utils.file_handler import FileHandler
from utils.encryption import Encryption


class UserManager:
    """👥 User Management System"""
    
    def __init__(self):
        self.logger = setup_logger("user_manager", "data/logs/user_management.log")
        self.file_handler = FileHandler()
        self.encryption = Encryption()
        
        # User data storage
        self.user_profiles = {}  # user_id -> profile
        self.user_settings = {}  # user_id -> settings
        self.user_activity = {}  # user_id -> activity log
        
        # User groups and relationships
        self.user_groups = {}    # group_name -> [user_ids]
        self.user_relationships = {}  # user_id -> {friends: [], blocked: []}
        
        # Initialize
        self.initialize()
    
    def initialize(self):
        """Initialize user management system"""
        try:
            self.logger.info("👥 Initializing User Management System...")
            
            # Load user data
            self._load_all_user_data()
            
            # Create default admin user if not exists
            self._create_default_admin()
            
            self.logger.info(f"✅ User Management initialized: {self.get_user_count()} users")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing user management: {e}")
    
    def _load_all_user_data(self):
        """Load all user data from files"""
        try:
            # User profiles
            profiles_file = "data/users/user_profiles.json"
            if os.path.exists(profiles_file):
                with open(profiles_file, "r", encoding="utf-8") as f:
                    self.user_profiles = json.load(f)
            else:
                self.user_profiles = {}
            
            # User settings
            settings_file = "data/users/user_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, "r", encoding="utf-8") as f:
                    self.user_settings = json.load(f)
            else:
                self.user_settings = {}
            
            # User activity
            activity_file = "data/users/user_activity.json"
            if os.path.exists(activity_file):
                with open(activity_file, "r", encoding="utf-8") as f:
                    self.user_activity = json.load(f)
            else:
                self.user_activity = {}
            
            # User groups
            groups_file = "data/users/user_groups.json"
            if os.path.exists(groups_file):
                with open(groups_file, "r", encoding="utf-8") as f:
                    self.user_groups = json.load(f)
            else:
                self.user_groups = {
                    "admins": [],
                    "premium": [],
                    "regular": [],
                    "blocked": []
                }
            
            # User relationships
            relationships_file = "data/users/user_relationships.json"
            if os.path.exists(relationships_file):
                with open(relationships_file, "r", encoding="utf-8") as f:
                    self.user_relationships = json.load(f)
            else:
                self.user_relationships = {}
            
            self.logger.info(f"✅ Loaded user data: {len(self.user_profiles)} profiles")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading user data: {e}")
    
    def _save_user_data(self, data_type: str, data: Dict):
        """Save user data to file"""
        try:
            filename = f"data/users/user_{data_type}.json"
            self.file_handler.write_json(filename, data)
            self.logger.debug(f"Saved user {data_type}")
        except Exception as e:
            self.logger.error(f"Error saving user {data_type}: {e}")
    
    def _create_default_admin(self):
        """Create default admin user"""
        try:
            admin_id = "1000123456789"  # Default admin ID
            
            if admin_id not in self.user_profiles:
                admin_profile = {
                    "user_id": admin_id,
                    "username": "admin",
                    "display_name": "Administrator",
                    "role": "admin",
                    "permissions": ["all"],
                    "created_at": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                    "status": "active"
                }
                
                self.user_profiles[admin_id] = admin_profile
                self._add_user_to_group(admin_id, "admins")
                
                self.logger.info("Created default admin user")
                self.save_all_user_data()
                
        except Exception as e:
            self.logger.error(f"Error creating default admin: {e}")
    
    def get_or_create_user(self, user_id: str, username: str = None, extra_data: Dict = None) -> Dict:
        """Get or create user profile"""
        try:
            if user_id in self.user_profiles:
                # Update last seen
                self.user_profiles[user_id]["last_seen"] = datetime.now().isoformat()
                self.update_activity(user_id, "seen")
                return self.user_profiles[user_id]
            
            # Create new user
            user_profile = {
                "user_id": user_id,
                "username": username or f"user_{user_id[-6:]}",
                "display_name": username or f"User {user_id[-6:]}",
                "role": "user",
                "permissions": ["basic"],
                "created_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "status": "active",
                "interaction_count": 0,
                "first_interaction": datetime.now().isoformat()
            }
            
            # Add extra data if provided
            if extra_data:
                user_profile.update(extra_data)
            
            # Add to user profiles
            self.user_profiles[user_id] = user_profile
            
            # Create default settings
            self.user_settings[user_id] = self._get_default_settings()
            
            # Create activity log
            self.user_activity[user_id] = {
                "activities": [],
                "total_activities": 0,
                "last_activity": datetime.now().isoformat()
            }
            
            # Add to regular users group
            self._add_user_to_group(user_id, "regular")
            
            # Create relationships entry
            self.user_relationships[user_id] = {
                "friends": [],
                "blocked": [],
                "pending_requests": [],
                "favorite_users": []
            }
            
            # Save all data
            self.save_all_user_data()
            
            self.logger.info(f"Created new user: {user_id} ({username or 'no name'})")
            
            return user_profile
            
        except Exception as e:
            self.logger.error(f"❌ Error creating user: {e}")
            return {}
    
    def _get_default_settings(self) -> Dict:
        """Get default user settings"""
        return {
            "notifications": {
                "message_notifications": True,
                "photo_notifications": True,
                "command_notifications": True,
                "group_notifications": False
            },
            "privacy": {
                "profile_visible": True,
                "activity_visible": True,
                "allow_friend_requests": True,
                "allow_messages": True
            },
            "preferences": {
                "language": "bengali",
                "theme": "dark",
                "response_style": "normal",
                "auto_download_photos": False
            },
            "chat_settings": {
                "typing_indicator": True,
                "read_receipts": True,
                "auto_reply": False,
                "response_delay": 2
            }
        }
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile"""
        return self.user_profiles.get(user_id)
    
    def update_user_profile(self, user_id: str, updates: Dict) -> bool:
        """Update user profile"""
        try:
            if user_id not in self.user_profiles:
                self.logger.warning(f"User not found: {user_id}")
                return False
            
            # Update profile
            self.user_profiles[user_id].update(updates)
            self.user_profiles[user_id]["last_updated"] = datetime.now().isoformat()
            
            # Save to file
            self._save_user_data("profiles", self.user_profiles)
            
            self.logger.debug(f"Updated profile for user: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error updating user profile: {e}")
            return False
    
    def get_user_settings(self, user_id: str) -> Dict:
        """Get user settings"""
        if user_id in self.user_settings:
            return self.user_settings[user_id]
        else:
            # Return default settings
            return self._get_default_settings()
    
    def update_user_settings(self, user_id: str, category: str, setting: str, value: Any) -> bool:
        """Update user setting"""
        try:
            if user_id not in self.user_settings:
                self.user_settings[user_id] = self._get_default_settings()
            
            # Update setting
            if category in self.user_settings[user_id]:
                if setting in self.user_settings[user_id][category]:
                    self.user_settings[user_id][category][setting] = value
                else:
                    # Create new setting
                    self.user_settings[user_id][category][setting] = value
            else:
                # Create new category
                self.user_settings[user_id][category] = {setting: value}
            
            # Save to file
            self._save_user_data("settings", self.user_settings)
            
            self.logger.debug(f"Updated settings for user: {user_id} - {category}.{setting} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error updating user settings: {e}")
            return False
    
    def update_activity(self, user_id: str, activity_type: str, details: str = "", metadata: Dict = None):
        """Update user activity"""
        try:
            if user_id not in self.user_activity:
                self.user_activity[user_id] = {
                    "activities": [],
                    "total_activities": 0,
                    "last_activity": datetime.now().isoformat()
                }
            
            # Create activity record
            activity_record = {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "type": activity_type,
                "details": details,
                "metadata": metadata or {}
            }
            
            # Add to activity log
            self.user_activity[user_id]["activities"].append(activity_record)
            self.user_activity[user_id]["total_activities"] += 1
            self.user_activity[user_id]["last_activity"] = datetime.now().isoformat()
            
            # Keep only last 100 activities
            if len(self.user_activity[user_id]["activities"]) > 100:
                self.user_activity[user_id]["activities"] = self.user_activity[user_id]["activities"][-100:]
            
            # Also update profile interaction count
            if user_id in self.user_profiles:
                self.user_profiles[user_id]["interaction_count"] = self.user_profiles[user_id].get("interaction_count", 0) + 1
                self.user_profiles[user_id]["last_seen"] = datetime.now().isoformat()
            
            # Save periodically
            if self.user_activity[user_id]["total_activities"] % 10 == 0:
                self.save_all_user_data()
            
        except Exception as e:
            self.logger.error(f"❌ Error updating activity: {e}")
    
    def get_user_activity(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user activity log"""
        if user_id in self.user_activity:
            activities = self.user_activity[user_id]["activities"]
            return activities[-limit:] if limit > 0 else activities
        return []
    
    def get_recent_active_users(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """Get recently active users"""
        try:
            cutoff_time = time.time() - (hours * 3600)
            active_users = []
            
            for user_id, activity_data in self.user_activity.items():
                last_activity = activity_data.get("last_activity")
                if last_activity:
                    try:
                        last_time = datetime.fromisoformat(last_activity).timestamp()
                        if last_time > cutoff_time:
                            profile = self.user_profiles.get(user_id, {})
                            active_users.append({
                                "user_id": user_id,
                                "username": profile.get("username", "Unknown"),
                                "last_activity": last_activity,
                                "interaction_count": activity_data.get("total_activities", 0)
                            })
                    except:
                        continue
            
            # Sort by last activity (newest first)
            active_users.sort(key=lambda x: x.get("last_activity", ""), reverse=True)
            
            return active_users[:limit] if limit > 0 else active_users
            
        except Exception as e:
            self.logger.error(f"❌ Error getting active users: {e}")
            return []
    
    def _add_user_to_group(self, user_id: str, group_name: str) -> bool:
        """Add user to group"""
        try:
            if group_name not in self.user_groups:
                self.user_groups[group_name] = []
            
            if user_id not in self.user_groups[group_name]:
                self.user_groups[group_name].append(user_id)
                self.logger.debug(f"Added user {user_id} to group {group_name}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error adding user to group: {e}")
            return False
    
    def remove_user_from_group(self, user_id: str, group_name: str) -> bool:
        """Remove user from group"""
        try:
            if group_name in self.user_groups and user_id in self.user_groups[group_name]:
                self.user_groups[group_name].remove(user_id)
                self.logger.debug(f"Removed user {user_id} from group {group_name}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error removing user from group: {e}")
            return False
    
    def get_user_groups(self, user_id: str) -> List[str]:
        """Get groups user belongs to"""
        groups = []
        for group_name, user_list in self.user_groups.items():
            if user_id in user_list:
                groups.append(group_name)
        return groups
    
    def get_group_members(self, group_name: str) -> List[str]:
        """Get members of a group"""
        return self.user_groups.get(group_name, [])
    
    def is_user_in_group(self, user_id: str, group_name: str) -> bool:
        """Check if user is in group"""
        return group_name in self.user_groups and user_id in self.user_groups[group_name]
    
    def add_friend(self, user_id: str, friend_id: str) -> bool:
        """Add friend relationship"""
        try:
            if user_id not in self.user_relationships:
                self.user_relationships[user_id] = {
                    "friends": [],
                    "blocked": [],
                    "pending_requests": [],
                    "favorite_users": []
                }
            
            if friend_id not in self.user_relationships[user_id]["friends"]:
                self.user_relationships[user_id]["friends"].append(friend_id)
                self.logger.debug(f"Added friend: {user_id} -> {friend_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error adding friend: {e}")
            return False
    
    def remove_friend(self, user_id: str, friend_id: str) -> bool:
        """Remove friend relationship"""
        try:
            if user_id in self.user_relationships and friend_id in self.user_relationships[user_id]["friends"]:
                self.user_relationships[user_id]["friends"].remove(friend_id)
                self.logger.debug(f"Removed friend: {user_id} -> {friend_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error removing friend: {e}")
            return False
    
    def block_user(self, user_id: str, block_id: str) -> bool:
        """Block a user"""
        try:
            if user_id not in self.user_relationships:
                self.user_relationships[user_id] = {
                    "friends": [],
                    "blocked": [],
                    "pending_requests": [],
                    "favorite_users": []
                }
            
            if block_id not in self.user_relationships[user_id]["blocked"]:
                self.user_relationships[user_id]["blocked"].append(block_id)
                
                # Also remove from friends if exists
                if block_id in self.user_relationships[user_id]["friends"]:
                    self.user_relationships[user_id]["friends"].remove(block_id)
                
                self.logger.debug(f"Blocked user: {user_id} -> {block_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error blocking user: {e}")
            return False
    
    def unblock_user(self, user_id: str, unblock_id: str) -> bool:
        """Unblock a user"""
        try:
            if user_id in self.user_relationships and unblock_id in self.user_relationships[user_id]["blocked"]:
                self.user_relationships[user_id]["blocked"].remove(unblock_id)
                self.logger.debug(f"Unblocked user: {user_id} -> {unblock_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error unblocking user: {e}")
            return False
    
    def is_user_blocked(self, user_id: str, target_id: str) -> bool:
        """Check if user has blocked target"""
        if user_id in self.user_relationships:
            return target_id in self.user_relationships[user_id]["blocked"]
        return False
    
    def get_friends_list(self, user_id: str) -> List[str]:
        """Get user's friends list"""
        if user_id in self.user_relationships:
            return self.user_relationships[user_id]["friends"]
        return []
    
    def get_blocked_list(self, user_id: str) -> List[str]:
        """Get user's blocked list"""
        if user_id in self.user_relationships:
            return self.user_relationships[user_id]["blocked"]
        return []
    
    def search_users(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for users"""
        try:
            results = []
            query_lower = query.lower()
            
            for user_id, profile in self.user_profiles.items():
                username = profile.get("username", "").lower()
                display_name = profile.get("display_name", "").lower()
                
                if query_lower in username or query_lower in display_name:
                    results.append({
                        "user_id": user_id,
                        "username": profile.get("username", ""),
                        "display_name": profile.get("display_name", ""),
                        "role": profile.get("role", "user"),
                        "last_seen": profile.get("last_seen", ""),
                        "interaction_count": profile.get("interaction_count", 0)
                    })
                
                if len(results) >= limit:
                    break
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user and all their data"""
        try:
            # Remove from profiles
            if user_id in self.user_profiles:
                del self.user_profiles[user_id]
            
            # Remove from settings
            if user_id in self.user_settings:
                del self.user_settings[user_id]
            
            # Remove from activity
            if user_id in self.user_activity:
                del self.user_activity[user_id]
            
            # Remove from all groups
            for group_name in list(self.user_groups.keys()):
                if user_id in self.user_groups[group_name]:
                    self.user_groups[group_name].remove(user_id)
            
            # Remove from relationships
            if user_id in self.user_relationships:
                del self.user_relationships[user_id]
            
            # Remove from other users' relationships
            for other_id, relationships in list(self.user_relationships.items()):
                for rel_type in ["friends", "blocked", "pending_requests", "favorite_users"]:
                    if rel_type in relationships and user_id in relationships[rel_type]:
                        relationships[rel_type].remove(user_id)
            
            # Save all data
            self.save_all_user_data()
            
            self.logger.info(f"Deleted user: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting user: {e}")
            return False
    
    def save_all_user_data(self):
        """Save all user data to files"""
        try:
            self._save_user_data("profiles", self.user_profiles)
            self._save_user_data("settings", self.user_settings)
            self._save_user_data("activity", self.user_activity)
            self._save_user_data("groups", self.user_groups)
            self._save_user_data("relationships", self.user_relationships)
            
            self.logger.debug("Saved all user data")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving user data: {e}")
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        return len(self.user_profiles)
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        try:
            total_users = len(self.user_profiles)
            
            # Count by role
            roles_count = {}
            for profile in self.user_profiles.values():
                role = profile.get("role", "user")
                roles_count[role] = roles_count.get(role, 0) + 1
            
            # Count by group
            groups_count = {}
            for group_name, user_list in self.user_groups.items():
                groups_count[group_name] = len(user_list)
            
            # Active users (last 7 days)
            week_ago = time.time() - (7 * 86400)
            active_users = 0
            total_interactions = 0
            
            for user_id, activity_data in self.user_activity.items():
                last_activity = activity_data.get("last_activity")
                if last_activity:
                    try:
                        last_time = datetime.fromisoformat(last_activity).timestamp()
                        if last_time > week_ago:
                            active_users += 1
                    except:
                        pass
                
                total_interactions += activity_data.get("total_activities", 0)
            
            return {
                "total_users": total_users,
                "active_users_7days": active_users,
                "total_interactions": total_interactions,
                "roles_distribution": roles_count,
                "groups_distribution": groups_count,
                "average_interactions_per_user": total_interactions / max(total_users, 1),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user stats: {e}")
            return {}
    
    def backup_user_data(self) -> str:
        """Create backup of user data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"data/users/backups/users_{timestamp}"
            
            os.makedirs(backup_dir, exist_ok=True)
            
            # Files to backup
            files_to_backup = [
                "data/users/user_profiles.json",
                "data/users/user_settings.json",
                "data/users/user_activity.json",
                "data/users/user_groups.json",
                "data/users/user_relationships.json"
            ]
            
            import shutil
            for source in files_to_backup:
                if os.path.exists(source):
                    shutil.copy2(source, backup_dir)
            
            # Compress backup
            backup_zip = f"{backup_dir}.zip"
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            shutil.rmtree(backup_dir)  # Remove uncompressed version
            
            self.logger.info(f"User backup created: {backup_zip}")
            return backup_zip
            
        except Exception as e:
            self.logger.error(f"❌ Error backing up user data: {e}")
            return ""
    
    def cleanup_inactive_users(self, days_inactive: int = 90) -> int:
        """Cleanup users inactive for specified days"""
        try:
            cutoff_time = time.time() - (days_inactive * 86400)
            removed_count = 0
            
            users_to_remove = []
            
            for user_id, activity_data in self.user_activity.items():
                last_activity = activity_data.get("last_activity")
                if last_activity:
                    try:
                        last_time = datetime.fromisoformat(last_activity).timestamp()
                        if last_time < cutoff_time:
                            # Check if user is admin or special
                            profile = self.user_profiles.get(user_id, {})
                            role = profile.get("role", "user")
                            
                            if role not in ["admin", "system"]:
                                users_to_remove.append(user_id)
                    except:
                        continue
            
            # Remove inactive users
            for user_id in users_to_remove:
                if self.delete_user(user_id):
                    removed_count += 1
            
            self.logger.info(f"Cleaned up {removed_count} inactive users ({days_inactive} days)")
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning up inactive users: {e}")
            return 0