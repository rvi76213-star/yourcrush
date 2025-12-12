"""
⏱️ Rate Limit Configuration Module
"""

import time
from collections import defaultdict
from datetime import datetime, timedelta

RATE_LIMIT_CONFIG = {
    # Global Rate Limits
    "global_limits": {
        "messages": {
            "per_second": 2,
            "per_minute": 30,
            "per_hour": 500,
            "per_day": 5000
        },
        "commands": {
            "per_minute": 20,
            "per_hour": 300,
            "per_day": 2000
        },
        "api_calls": {
            "per_minute": 60,
            "per_hour": 1000,
            "per_day": 10000
        },
        "photos": {
            "per_minute": 5,
            "per_hour": 50,
            "per_day": 200
        }
    },
    
    # Per-User Rate Limits
    "user_limits": {
        "messages": {
            "per_minute": 10,
            "per_hour": 100,
            "per_day": 500
        },
        "commands": {
            "per_minute": 5,
            "per_hour": 50,
            "per_day": 200
        },
        "photos": {
            "per_minute": 2,
            "per_hour": 20,
            "per_day": 50
        }
    },
    
    # Per-Group Rate Limits
    "group_limits": {
        "messages": {
            "per_minute": 20,
            "per_hour": 300,
            "per_day": 2000
        },
        "commands": {
            "per_minute": 10,
            "per_hour": 150,
            "per_day": 1000
        }
    },
    
    # Special Limits for Commands
    "command_specific_limits": {
        ".murgi": {
            "per_user_per_day": 10,
            "cooldown_seconds": 60,
            "max_concurrent": 1
        },
        ".love": {
            "per_user_per_hour": 20,
            "cooldown_seconds": 30
        },
        ".pick": {
            "per_user_per_minute": 5,
            "cooldown_seconds": 10
        },
        ".dio": {
            "per_user_per_hour": 10,
            "cooldown_seconds": 120
        }
    },
    
    # Adaptive Rate Limiting
    "adaptive_limits": {
        "enabled": True,
        "adjust_based_on_load": True,
        "increase_threshold": 0.7,  # 70% usage
        "decrease_threshold": 0.3,  # 30% usage
        "min_adjustment": 0.5,  # 50% of original
        "max_adjustment": 2.0,  # 200% of original
        "check_interval": 300  # 5 minutes
    },
    
    # Penalty System
    "penalties": {
        "enabled": True,
        "violation_levels": {
            "minor": {
                "threshold": 3,
                "penalty_seconds": 30,
                "action": "delay"
            },
            "medium": {
                "threshold": 5,
                "penalty_seconds": 300,
                "action": "temp_block"
            },
            "severe": {
                "threshold": 10,
                "penalty_seconds": 3600,
                "action": "block_24h"
            }
        },
        "reset_interval": 3600,  # 1 hour
        "forgive_after": 86400  # 24 hours
    },
    
    # Monitoring & Logging
    "monitoring": {
        "log_rate_limit_hits": True,
        "log_penalties": True,
        "alert_on_major_violation": True,
        "stats_interval": 3600,  # 1 hour
        "cleanup_interval": 86400  # 24 hours
    },
    
    # Whitelist/Blacklist
    "access_lists": {
        "whitelist_enabled": False,
        "whitelist": [],  # User IDs that bypass limits
        "blacklist_enabled": True,
        "blacklist": [],  # User IDs that are blocked
        "admin_bypass": True
    }
}

class RateLimiter:
    """Rate limiter implementation"""
    
    def __init__(self):
        self.user_activity = defaultdict(lambda: defaultdict(list))
        self.group_activity = defaultdict(lambda: defaultdict(list))
        self.global_activity = defaultdict(list)
        self.penalties = defaultdict(list)
        self.stats = defaultdict(int)
        
    def check_rate_limit(self, user_id, action_type, action_subtype=None, group_id=None):
        """Check if action is allowed"""
        current_time = time.time()
        
        # Check blacklist
        if user_id in RATE_LIMIT_CONFIG["access_lists"]["blacklist"]:
            return False, "User is blacklisted"
        
        # Check whitelist/admin bypass
        if (user_id in RATE_LIMIT_CONFIG["access_lists"]["whitelist"] or 
            RATE_LIMIT_CONFIG["access_lists"]["admin_bypass"] and self._is_admin(user_id)):
            return True, "Allowed (whitelist/admin)"
        
        # Check penalties
        if self._has_active_penalty(user_id):
            penalty_end = self.penalties[user_id][-1]["end_time"]
            remaining = penalty_end - current_time
            return False, f"Rate limited. Try again in {int(remaining)} seconds"
        
        # Check global limits
        global_key = action_type
        if action_subtype:
            global_key = f"{action_type}_{action_subtype}"
        
        if not self._check_global_limit(global_key, current_time):
            return False, "Global rate limit exceeded"
        
        # Check user limits
        if not self._check_user_limit(user_id, action_type, action_subtype, current_time):
            # Record violation
            self._record_violation(user_id, action_type)
            return False, "User rate limit exceeded"
        
        # Check group limits
        if group_id and not self._check_group_limit(group_id, action_type, current_time):
            return False, "Group rate limit exceeded"
        
        # Check command-specific limits
        if action_type == "command" and action_subtype:
            if not self._check_command_limit(user_id, action_subtype, current_time):
                return False, "Command rate limit exceeded"
        
        # Record activity
        self._record_activity(user_id, action_type, action_subtype, group_id, current_time)
        
        return True, "Allowed"
    
    def _check_global_limit(self, action_key, current_time):
        """Check global rate limits"""
        if action_key not in self.global_activity:
            return True
        
        activity = self.global_activity[action_key]
        limits = RATE_LIMIT_CONFIG["global_limits"]
        
        # Clean old entries
        self._clean_old_entries(activity, current_time)
        
        # Get appropriate limits based on action_key
        if "message" in action_key:
            action_limits = limits["messages"]
        elif "command" in action_key:
            action_limits = limits["commands"]
        elif "api" in action_key:
            action_limits = limits["api_calls"]
        elif "photo" in action_key:
            action_limits = limits["photos"]
        else:
            return True  # No specific limit
        
        # Check per-second limit
        last_second = [t for t in activity if current_time - t < 1]
        if len(last_second) >= action_limits.get("per_second", 1000):
            return False
        
        # Check per-minute limit
        last_minute = [t for t in activity if current_time - t < 60]
        if len(last_minute) >= action_limits.get("per_minute", 1000):
            return False
        
        # Check per-hour limit
        last_hour = [t for t in activity if current_time - t < 3600]
        if len(last_hour) >= action_limits.get("per_hour", 10000):
            return False
        
        # Check per-day limit
        last_day = [t for t in activity if current_time - t < 86400]
        if len(last_day) >= action_limits.get("per_day", 100000):
            return False
        
        return True
    
    def _check_user_limit(self, user_id, action_type, action_subtype, current_time):
        """Check user-specific limits"""
        user_key = f"{action_type}"
        if action_subtype:
            user_key = f"{action_type}_{action_subtype}"
        
        if user_key not in self.user_activity[user_id]:
            return True
        
        activity = self.user_activity[user_id][user_key]
        limits = RATE_LIMIT_CONFIG["user_limits"]
        
        # Clean old entries
        self._clean_old_entries(activity, current_time)
        
        # Get appropriate limits
        if action_type == "message":
            action_limits = limits["messages"]
        elif action_type == "command":
            action_limits = limits["commands"]
        elif action_type == "photo":
            action_limits = limits["photos"]
        else:
            return True
        
        # Check per-minute limit
        last_minute = [t for t in activity if current_time - t < 60]
        if len(last_minute) >= action_limits.get("per_minute", 100):
            return False
        
        # Check per-hour limit
        last_hour = [t for t in activity if current_time - t < 3600]
        if len(last_hour) >= action_limits.get("per_hour", 1000):
            return False
        
        # Check per-day limit
        last_day = [t for t in activity if current_time - t < 86400]
        if len(last_day) >= action_limits.get("per_day", 5000):
            return False
        
        return True
    
    def _check_command_limit(self, user_id, command_name, current_time):
        """Check command-specific limits"""
        if command_name not in RATE_LIMIT_CONFIG["command_specific_limits"]:
            return True
        
        limits = RATE_LIMIT_CONFIG["command_specific_limits"][command_name]
        command_key = f"command_{command_name}"
        
        if command_key not in self.user_activity[user_id]:
            return True
        
        activity = self.user_activity[user_id][command_key]
        
        # Clean old entries
        self._clean_old_entries(activity, current_time)
        
        # Check cooldown
        if activity:
            last_time = activity[-1]
            cooldown = limits.get("cooldown_seconds", 0)
            if current_time - last_time < cooldown:
                return False
        
        # Check per-day limit
        last_day = [t for t in activity if current_time - t < 86400]
        if len(last_day) >= limits.get("per_user_per_day", 100):
            return False
        
        # Check per-hour limit
        last_hour = [t for t in activity if current_time - t < 3600]
        if len(last_hour) >= limits.get("per_user_per_hour", 50):
            return False
        
        # Check max concurrent
        max_concurrent = limits.get("max_concurrent", 1)
        if len(activity) >= max_concurrent:
            return False
        
        return True
    
    def _check_group_limit(self, group_id, action_type, current_time):
        """Check group-specific limits"""
        if action_type not in self.group_activity[group_id]:
            return True
        
        activity = self.group_activity[group_id][action_type]
        limits = RATE_LIMIT_CONFIG["group_limits"]
        
        # Clean old entries
        self._clean_old_entries(activity, current_time)
        
        # Get appropriate limits
        if action_type == "message":
            action_limits = limits["messages"]
        elif action_type == "command":
            action_limits = limits["commands"]
        else:
            return True
        
        # Check per-minute limit
        last_minute = [t for t in activity if current_time - t < 60]
        if len(last_minute) >= action_limits.get("per_minute", 50):
            return False
        
        # Check per-hour limit
        last_hour = [t for t in activity if current_time - t < 3600]
        if len(last_hour) >= action_limits.get("per_hour", 500):
            return False
        
        return True
    
    def _record_violation(self, user_id, action_type):
        """Record rate limit violation"""
        current_time = time.time()
        
        # Clean old violations
        if user_id in self.penalties:
            self.penalties[user_id] = [
                p for p in self.penalties[user_id] 
                if current_time - p["time"] < RATE_LIMIT_CONFIG["penalties"]["forgive_after"]
            ]
        
        # Add new violation
        self.penalties[user_id].append({
            "time": current_time,
            "action": action_type,
            "level": "minor"
        })
        
        # Check violation levels
        violations = self.penalties[user_id]
        recent_violations = [
            v for v in violations 
            if current_time - v["time"] < RATE_LIMIT_CONFIG["penalties"]["reset_interval"]
        ]
        
        violation_count = len(recent_violations)
        levels = RATE_LIMIT_CONFIG["penalties"]["violation_levels"]
        
        # Apply penalty if threshold reached
        for level_name, level_config in levels.items():
            if violation_count >= level_config["threshold"]:
                penalty_end = current_time + level_config["penalty_seconds"]
                self.penalties[user_id].append({
                    "time": current_time,
                    "action": action_type,
                    "level": level_name,
                    "end_time": penalty_end
                })
                break
        
        # Log violation
        self.stats["violations"] += 1
    
    def _has_active_penalty(self, user_id):
        """Check if user has active penalty"""
        if user_id not in self.penalties:
            return False
        
        current_time = time.time()
        active_penalties = [
            p for p in self.penalties[user_id] 
            if "end_time" in p and p["end_time"] > current_time
        ]
        
        return len(active_penalties) > 0
    
    def _record_activity(self, user_id, action_type, action_subtype, group_id, timestamp):
        """Record activity for rate limiting"""
        # Global activity
        global_key = action_type
        if action_subtype:
            global_key = f"{action_type}_{action_subtype}"
        self.global_activity[global_key].append(timestamp)
        
        # User activity
        user_key = f"{action_type}"
        if action_subtype:
            user_key = f"{action_type}_{action_subtype}"
        self.user_activity[user_id][user_key].append(timestamp)
        
        # Group activity
        if group_id:
            self.group_activity[group_id][action_type].append(timestamp)
        
        # Command-specific activity
        if action_type == "command" and action_subtype:
            command_key = f"command_{action_subtype}"
            self.user_activity[user_id][command_key].append(timestamp)
    
    def _clean_old_entries(self, activity_list, current_time):
        """Clean old entries from activity list"""
        # Keep only entries from last 24 hours
        cutoff = current_time - 86400
        while activity_list and activity_list[0] < cutoff:
            activity_list.pop(0)
    
    def _is_admin(self, user_id):
        """Check if user is admin (simplified)"""
        # This should be replaced with actual admin check
        admin_ids = ["1000123456789"]  # Add your admin IDs here
        return user_id in admin_ids
    
    def get_stats(self):
        """Get rate limiting statistics"""
        stats = {
            "total_checks": self.stats.get("total_checks", 0),
            "allowed": self.stats.get("allowed", 0),
            "blocked": self.stats.get("blocked", 0),
            "violations": self.stats.get("violations", 0),
            "active_penalties": sum(1 for user_penalties in self.penalties.values() 
                                  for p in user_penalties if "end_time" in p and p["end_time"] > time.time()),
            "unique_users_today": len(self.user_activity),
            "unique_groups_today": len(self.group_activity)
        }
        
        # Calculate rates
        if stats["total_checks"] > 0:
            stats["allow_rate"] = (stats["allowed"] / stats["total_checks"]) * 100
            stats["block_rate"] = (stats["blocked"] / stats["total_checks"]) * 100
        else:
            stats["allow_rate"] = 0
            stats["block_rate"] = 0
        
        return stats
    
    def cleanup(self):
        """Clean up old data"""
        current_time = time.time()
        
        # Clean old activity data
        for user_id in list(self.user_activity.keys()):
            for action_key in list(self.user_activity[user_id].keys()):
                self._clean_old_entries(self.user_activity[user_id][action_key], current_time)
                if not self.user_activity[user_id][action_key]:
                    del self.user_activity[user_id][action_key]
            if not self.user_activity[user_id]:
                del self.user_activity[user_id]
        
        # Clean old penalties
        for user_id in list(self.penalties.keys()):
            self.penalties[user_id] = [
                p for p in self.penalties[user_id] 
                if current_time - p.get("time", 0) < RATE_LIMIT_CONFIG["penalties"]["forgive_after"]
            ]
            if not self.penalties[user_id]:
                del self.penalties[user_id]

if __name__ == "__main__":
    print("Rate Limit Configuration Module Loaded")
    
    # Test the rate limiter
    limiter = RateLimiter()
    
    # Simulate some activity
    test_user = "12345"
    test_group = "group1"
    
    print("\nTesting Rate Limiter:")
    
    # Test 1: Normal message
    allowed, reason = limiter.check_rate_limit(test_user, "message", group_id=test_group)
    print(f"Message 1: {'✅ Allowed' if allowed else f'❌ Blocked: {reason}'}")
    
    # Test 2: Command
    allowed, reason = limiter.check_rate_limit(test_user, "command", ".murgi", test_group)
    print(f"Command .murgi: {'✅ Allowed' if allowed else f'❌ Blocked: {reason}'}")
    
    # Test 3: Photo
    allowed, reason = limiter.check_rate_limit(test_user, "photo", group_id=test_group)
    print(f"Photo: {'✅ Allowed' if allowed else f'❌ Blocked: {reason}'}")
    
    # Get stats
    stats = limiter.get_stats()
    print(f"\nStats: {stats}")