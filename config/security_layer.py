#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 Security Layer
Security, encryption, and protection systems
"""

import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

from utils.logger import setup_logger
from utils.encryption import Encryption


class SecurityLayer:
    """🔒 Security and Protection System"""
    
    def __init__(self):
        self.logger = setup_logger("security_layer", "data/logs/security.log")
        self.encryption = Encryption()
        
        # Security configuration
        self.config = self._load_security_config()
        
        # Security state
        self.suspicious_activities = []
        self.blocked_ips = set()
        self.failed_logins = {}
        
        # Rate limiting
        self.request_counts = {}
        self.activity_log = []
        
        # Security rules
        self.rules = {
            "max_login_attempts": 5,
            "login_lockout_minutes": 15,
            "max_requests_per_minute": 60,
            "suspicious_patterns": [
                r"password.*change",
                r"login.*now",
                r"admin.*access",
                r"root.*privilege",
                r"system.*control"
            ]
        }
        
        # Initialize
        self.initialize()
    
    def _load_security_config(self) -> Dict:
        """Load security configuration"""
        try:
            config_file = "config/security_config.py"
            if os.path.exists(config_file):
                import importlib.util
                spec = importlib.util.spec_from_file_location("security_config", config_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module.SECURITY_CONFIG
            else:
                # Default configuration
                return {
                    "encryption_enabled": True,
                    "rate_limiting_enabled": True,
                    "ip_blocking_enabled": True,
                    "activity_monitoring": True,
                    "log_security_events": True,
                    "auto_block_suspicious": True
                }
        except Exception as e:
            self.logger.error(f"❌ Error loading security config: {e}")
            return {}
    
    def initialize(self):
        """Initialize security system"""
        try:
            self.logger.info("🔒 Initializing Security Layer...")
            
            # Create security directories
            self._create_security_directories()
            
            # Load blocked IPs
            self._load_blocked_ips()
            
            # Load security logs
            self._load_security_logs()
            
            # Generate security keys if needed
            self._generate_security_keys()
            
            self.logger.info("✅ Security Layer initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing security: {e}")
    
    def _create_security_directories(self):
        """Create security directories"""
        directories = [
            "data/security",
            "data/security/logs",
            "data/security/backups",
            "data/security/keys"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_blocked_ips(self):
        """Load blocked IPs from file"""
        try:
            blocked_file = "data/security/blocked_ips.json"
            if os.path.exists(blocked_file):
                with open(blocked_file, "r") as f:
                    blocked_data = json.load(f)
                    self.blocked_ips = set(blocked_data.get("blocked_ips", []))
                    self.logger.info(f"Loaded {len(self.blocked_ips)} blocked IPs")
        except Exception as e:
            self.logger.error(f"Error loading blocked IPs: {e}")
    
    def _load_security_logs(self):
        """Load security logs"""
        try:
            logs_file = "data/security/security_logs.json"
            if os.path.exists(logs_file):
                with open(logs_file, "r") as f:
                    logs_data = json.load(f)
                    self.suspicious_activities = logs_data.get("activities", [])
                    self.failed_logins = logs_data.get("failed_logins", {})
        except Exception as e:
            self.logger.error(f"Error loading security logs: {e}")
    
    def _generate_security_keys(self):
        """Generate security keys if not exists"""
        try:
            keys_dir = "data/security/keys"
            os.makedirs(keys_dir, exist_ok=True)
            
            # Generate API key for bot
            api_key_file = os.path.join(keys_dir, "api_key.txt")
            if not os.path.exists(api_key_file):
                api_key = secrets.token_urlsafe(32)
                with open(api_key_file, "w") as f:
                    f.write(api_key)
                self.logger.info("Generated API key")
            
            # Generate encryption salt
            salt_file = os.path.join(keys_dir, "encryption_salt.bin")
            if not os.path.exists(salt_file):
                salt = secrets.token_bytes(32)
                with open(salt_file, "wb") as f:
                    f.write(salt)
                self.logger.info("Generated encryption salt")
            
        except Exception as e:
            self.logger.error(f"Error generating security keys: {e}")
    
    def encrypt_sensitive_data(self, data: Any) -> str:
        """Encrypt sensitive data"""
        if not self.config.get("encryption_enabled", True):
            return json.dumps(data) if not isinstance(data, str) else data
        
        try:
            if isinstance(data, dict) or isinstance(data, list):
                data_str = json.dumps(data)
            else:
                data_str = str(data)
            
            encrypted = self.encryption.encrypt_string(data_str)
            return encrypted
            
        except Exception as e:
            self.logger.error(f"❌ Error encrypting data: {e}")
            return str(data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Any:
        """Decrypt sensitive data"""
        if not self.config.get("encryption_enabled", True):
            try:
                return json.loads(encrypted_data)
            except:
                return encrypted_data
        
        try:
            decrypted_str = self.encryption.decrypt_string(encrypted_data)
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted_str)
            except:
                return decrypted_str
                
        except Exception as e:
            self.logger.error(f"❌ Error decrypting data: {e}")
            return encrypted_data
    
    def check_rate_limit(self, user_id: str, action: str = "request") -> bool:
        """Check if user has exceeded rate limit"""
        if not self.config.get("rate_limiting_enabled", True):
            return True
        
        try:
            current_time = time.time()
            minute_key = f"{user_id}_{action}_{int(current_time // 60)}"
            
            # Initialize count
            if minute_key not in self.request_counts:
                self.request_counts[minute_key] = 0
            
            # Get rate limit
            max_requests = self.rules.get("max_requests_per_minute", 60)
            
            if self.request_counts[minute_key] >= max_requests:
                # Log rate limit violation
                self.log_suspicious_activity(
                    user_id=user_id,
                    activity_type="rate_limit",
                    details=f"Exceeded {max_requests} requests per minute",
                    severity="medium"
                )
                return False
            
            # Increment count
            self.request_counts[minute_key] += 1
            
            # Clean old entries
            self._clean_old_rate_limits()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking rate limit: {e}")
            return True
    
    def _clean_old_rate_limits(self):
        """Clean old rate limit entries"""
        try:
            current_time = time.time()
            minute_window = int(current_time // 60)
            
            # Keep only entries from last 5 minutes
            keys_to_delete = []
            for key in self.request_counts:
                try:
                    key_minute = int(key.split("_")[-1])
                    if minute_window - key_minute > 5:
                        keys_to_delete.append(key)
                except:
                    continue
            
            for key in keys_to_delete:
                del self.request_counts[key]
                
        except Exception as e:
            self.logger.error(f"Error cleaning rate limits: {e}")
    
    def check_ip_block(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        if not self.config.get("ip_blocking_enabled", True):
            return True
        
        try:
            if ip_address in self.blocked_ips:
                self.logger.warning(f"Blocked IP attempted access: {ip_address}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking IP block: {e}")
            return True
    
    def block_ip(self, ip_address: str, reason: str = "suspicious activity", duration_minutes: int = 60):
        """Block an IP address"""
        try:
            self.blocked_ips.add(ip_address)
            
            # Save blocked IPs
            self._save_blocked_ips()
            
            # Log the block
            self.log_suspicious_activity(
                user_id=f"IP:{ip_address}",
                activity_type="ip_blocked",
                details=f"IP blocked: {reason}",
                severity="high"
            )
            
            self.logger.warning(f"Blocked IP {ip_address}: {reason}")
            
            # Schedule unblock if duration specified
            if duration_minutes > 0:
                self._schedule_ip_unblock(ip_address, duration_minutes)
            
        except Exception as e:
            self.logger.error(f"❌ Error blocking IP: {e}")
    
    def _save_blocked_ips(self):
        """Save blocked IPs to file"""
        try:
            blocked_file = "data/security/blocked_ips.json"
            blocked_data = {
                "blocked_ips": list(self.blocked_ips),
                "last_updated": datetime.now().isoformat()
            }
            
            with open(blocked_file, "w") as f:
                json.dump(blocked_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving blocked IPs: {e}")
    
    def _schedule_ip_unblock(self, ip_address: str, delay_minutes: int):
        """Schedule IP unblock"""
        try:
            import threading
            
            def unblock_ip():
                time.sleep(delay_minutes * 60)
                if ip_address in self.blocked_ips:
                    self.blocked_ips.remove(ip_address)
                    self._save_blocked_ips()
                    self.logger.info(f"Auto-unblocked IP: {ip_address}")
            
            thread = threading.Thread(target=unblock_ip, daemon=True)
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Error scheduling IP unblock: {e}")
    
    def check_login_attempt(self, user_id: str, password_hash: str) -> Tuple[bool, str]:
        """Check login attempt"""
        try:
            # Check if account is locked
            if user_id in self.failed_logins:
                lockout_time = self.failed_logins[user_id].get("lockout_until")
                if lockout_time and time.time() < lockout_time:
                    remaining = int((lockout_time - time.time()) / 60)
                    return False, f"Account locked. Try again in {remaining} minutes."
            
            # Here you would verify the password hash
            # This is a placeholder - implement your own authentication
            is_valid = self._verify_password_hash(user_id, password_hash)
            
            if not is_valid:
                # Record failed attempt
                self.record_failed_login(user_id)
                return False, "Invalid credentials"
            
            # Clear failed attempts on successful login
            if user_id in self.failed_logins:
                del self.failed_logins[user_id]
                self._save_security_logs()
            
            return True, "Login successful"
            
        except Exception as e:
            self.logger.error(f"❌ Error checking login: {e}")
            return False, "Authentication error"
    
    def _verify_password_hash(self, user_id: str, password_hash: str) -> bool:
        """Verify password hash (placeholder)"""
        # In a real implementation, you would:
        # 1. Retrieve stored hash for the user
        # 2. Compare with provided hash
        # 3. Use secure comparison (secrets.compare_digest)
        
        # This is a dummy implementation
        return False
    
    def record_failed_login(self, user_id: str):
        """Record a failed login attempt"""
        try:
            current_time = time.time()
            
            if user_id not in self.failed_logins:
                self.failed_logins[user_id] = {
                    "attempts": [],
                    "lockout_until": None
                }
            
            user_data = self.failed_logins[user_id]
            user_data["attempts"].append(current_time)
            
            # Keep only recent attempts (last 1 hour)
            hour_ago = current_time - 3600
            user_data["attempts"] = [
                t for t in user_data["attempts"] if t > hour_ago
            ]
            
            # Check if lockout is needed
            max_attempts = self.rules.get("max_login_attempts", 5)
            lockout_minutes = self.rules.get("login_lockout_minutes", 15)
            
            if len(user_data["attempts"]) >= max_attempts:
                lockout_until = current_time + (lockout_minutes * 60)
                user_data["lockout_until"] = lockout_until
                
                # Log the lockout
                self.log_suspicious_activity(
                    user_id=user_id,
                    activity_type="account_lockout",
                    details=f"Account locked after {max_attempts} failed attempts",
                    severity="high"
                )
                
                self.logger.warning(f"Account locked: {user_id}")
            
            # Save security logs
            self._save_security_logs()
            
        except Exception as e:
            self.logger.error(f"❌ Error recording failed login: {e}")
    
    def detect_suspicious_pattern(self, text: str) -> List[str]:
        """Detect suspicious patterns in text"""
        try:
            import re
            
            detected_patterns = []
            text_lower = text.lower()
            
            for pattern in self.rules.get("suspicious_patterns", []):
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_patterns.append(pattern)
            
            return detected_patterns
            
        except Exception as e:
            self.logger.error(f"❌ Error detecting suspicious patterns: {e}")
            return []
    
    def log_suspicious_activity(self, user_id: str, activity_type: str, details: str, severity: str = "low"):
        """Log suspicious activity"""
        if not self.config.get("log_security_events", True):
            return
        
        try:
            activity = {
                "timestamp": time.time(),
                "date": datetime.now().isoformat(),
                "user_id": user_id,
                "activity_type": activity_type,
                "details": details,
                "severity": severity,
                "ip_address": self._get_client_ip()  # You need to implement this
            }
            
            self.suspicious_activities.append(activity)
            
            # Keep only last 1000 activities
            if len(self.suspicious_activities) > 1000:
                self.suspicious_activities = self.suspicious_activities[-1000:]
            
            # Log to file
            self._log_to_security_file(activity)
            
            # Auto-block if high severity and enabled
            if severity == "high" and self.config.get("auto_block_suspicious", True):
                ip_address = activity.get("ip_address")
                if ip_address:
                    self.block_ip(ip_address, f"Suspicious activity: {activity_type}", 1440)  # 24 hours
            
            self.logger.warning(f"Suspicious activity: {activity_type} - {details}")
            
        except Exception as e:
            self.logger.error(f"❌ Error logging suspicious activity: {e}")
    
    def _log_to_security_file(self, activity: Dict):
        """Log activity to security file"""
        try:
            log_file = "data/security/security_events.log"
            
            log_entry = json.dumps(activity, default=str) + "\n"
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error writing to security log: {e}")
    
    def _get_client_ip(self) -> str:
        """Get client IP address (placeholder)"""
        # In a real implementation, you would get the IP from request headers
        # This is a simplified version
        try:
            import socket
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"
    
    def _save_security_logs(self):
        """Save security logs to file"""
        try:
            logs_file = "data/security/security_logs.json"
            logs_data = {
                "activities": self.suspicious_activities[-500:],  # Keep last 500
                "failed_logins": self.failed_logins,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(logs_file, "w") as f:
                json.dump(logs_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving security logs: {e}")
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    def hash_data(self, data: str, salt: bytes = None) -> Dict:
        """Hash data with salt"""
        try:
            if salt is None:
                salt = secrets.token_bytes(16)
            
            # Use PBKDF2 for key derivation
            key = hashlib.pbkdf2_hmac(
                'sha256',
                data.encode('utf-8'),
                salt,
                100000,  # Number of iterations
                dklen=32  # Derived key length
            )
            
            return {
                'hash': key.hex(),
                'salt': salt.hex(),
                'algorithm': 'PBKDF2-SHA256'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error hashing data: {e}")
            return {}
    
    def verify_hash(self, data: str, stored_hash: str, stored_salt: str) -> bool:
        """Verify hashed data"""
        try:
            salt = bytes.fromhex(stored_salt)
            
            # Hash the data with the same salt
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                data.encode('utf-8'),
                salt,
                100000,
                dklen=32
            )
            
            # Compare securely
            return hmac.compare_digest(new_hash.hex(), stored_hash)
            
        except Exception as e:
            self.logger.error(f"❌ Error verifying hash: {e}")
            return False
    
    def sanitize_input(self, input_text: str, allowed_chars: str = None) -> str:
        """Sanitize user input"""
        try:
            import html
            
            # Decode HTML entities
            sanitized = html.unescape(input_text)
            
            # Remove potentially dangerous characters
            dangerous_patterns = [
                r'<script.*?>.*?</script>',
                r'<iframe.*?>.*?</iframe>',
                r'javascript:',
                r'onload=',
                r'onerror=',
                r'onclick='
            ]
            
            import re
            for pattern in dangerous_patterns:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
            
            # Escape HTML if needed
            sanitized = html.escape(sanitized)
            
            # Remove unwanted characters if specified
            if allowed_chars:
                sanitized = ''.join(c for c in sanitized if c in allowed_chars)
            
            return sanitized.strip()
            
        except Exception as e:
            self.logger.error(f"❌ Error sanitizing input: {e}")
            return input_text
    
    def get_security_report(self) -> Dict:
        """Get security report"""
        try:
            current_time = time.time()
            hour_ago = current_time - 3600
            day_ago = current_time - 86400
            
            # Count recent activities
            recent_activities = [
                a for a in self.suspicious_activities 
                if a.get("timestamp", 0) > hour_ago
            ]
            
            daily_activities = [
                a for a in self.suspicious_activities 
                if a.get("timestamp", 0) > day_ago
            ]
            
            # Count by severity
            severity_counts = {"low": 0, "medium": 0, "high": 0}
            for activity in daily_activities:
                severity = activity.get("severity", "low")
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            return {
                "blocked_ips_count": len(self.blocked_ips),
                "failed_logins_count": len(self.failed_logins),
                "recent_suspicious_activities": len(recent_activities),
                "daily_suspicious_activities": len(daily_activities),
                "severity_distribution": severity_counts,
                "rate_limit_entries": len(self.request_counts),
                "security_status": self._get_security_status(severity_counts),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error generating security report: {e}")
            return {"error": str(e)}
    
    def _get_security_status(self, severity_counts: Dict) -> str:
        """Get overall security status"""
        high_count = severity_counts.get("high", 0)
        medium_count = severity_counts.get("medium", 0)
        
        if high_count > 5:
            return "CRITICAL"
        elif high_count > 0 or medium_count > 10:
            return "WARNING"
        elif medium_count > 0:
            return "CAUTION"
        else:
            return "SECURE"
    
    def backup_security_data(self) -> bool:
        """Backup security data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"data/security/backups/security_{timestamp}"
            
            os.makedirs(backup_dir, exist_ok=True)
            
            # Files to backup
            files_to_backup = [
                "data/security/blocked_ips.json",
                "data/security/security_logs.json",
                "data/security/security_events.log",
                "data/security/keys/"
            ]
            
            import shutil
            for source in files_to_backup:
                if os.path.exists(source):
                    if os.path.isdir(source):
                        dest_dir = os.path.join(backup_dir, os.path.basename(source))
                        shutil.copytree(source, dest_dir)
                    else:
                        shutil.copy2(source, backup_dir)
            
            # Compress backup
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            shutil.rmtree(backup_dir)  # Remove uncompressed version
            
            self.logger.info(f"Security backup created: {backup_dir}.zip")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error backing up security data: {e}")
            return False
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Cleanup old security data"""
        try:
            import glob
            
            current_time = time.time()
            cutoff_time = current_time - (days_to_keep * 86400)
            
            # Clean old backups
            backup_files = glob.glob("data/security/backups/*.zip")
            for backup_file in backup_files:
                try:
                    file_time = os.path.getmtime(backup_file)
                    if file_time < cutoff_time:
                        os.remove(backup_file)
                        self.logger.debug(f"Removed old backup: {backup_file}")
                except Exception as e:
                    self.logger.error(f"Error removing backup {backup_file}: {e}")
            
            # Clean old security events log
            log_file = "data/security/security_events.log"
            if os.path.exists(log_file) and os.path.getsize(log_file) > 10 * 1024 * 1024:  # 10MB
                # Keep last 10000 lines
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                if len(lines) > 10000:
                    with open(log_file, "w", encoding="utf-8") as f:
                        f.writelines(lines[-10000:])
                    
                    self.logger.debug("Trimmed security events log")
            
            self.logger.info(f"Security cleanup completed (keeping {days_to_keep} days)")
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning up security data: {e}")