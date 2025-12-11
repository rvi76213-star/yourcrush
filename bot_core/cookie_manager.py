#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍪 Cookie Management System
Handles Facebook cookie extraction, encryption, and management
"""

import json
import logging
import os
import time
import browser_cookie3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from utils.encryption import Encryption
from utils.logger import setup_logger


class CookieManager:
    """🍪 Facebook Cookie Manager"""
    
    def __init__(self):
        self.logger = setup_logger("cookie_manager", "data/logs/bot_activity.log")
        self.encryption = Encryption()
        self.cookies = []
        self.cookie_file = "data/cookies/master_cookies.json"
        self.backup_file = "data/cookies/backup_cookies.json"
        
    def extract_cookies(self, browser: str = "chrome") -> bool:
        """Extract cookies from browser"""
        try:
            self.logger.info(f"🍪 Extracting cookies from {browser}...")
            
            cookies_list = []
            
            # Extract cookies based on browser
            if browser.lower() == "chrome":
                cj = browser_cookie3.chrome(domain_name='facebook.com')
            elif browser.lower() == "firefox":
                cj = browser_cookie3.firefox(domain_name='facebook.com')
            elif browser.lower() == "edge":
                cj = browser_cookie3.edge(domain_name='facebook.com')
            else:
                self.logger.error(f"❌ Unsupported browser: {browser}")
                return False
            
            # Convert cookies to list of dicts
            for cookie in cj:
                if 'facebook.com' in cookie.domain:
                    cookie_dict = {
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path,
                        'expires': cookie.expires,
                        'secure': cookie.secure,
                        'httpOnly': cookie.has_nonstandard_attr('HttpOnly'),
                        'extracted_at': datetime.now().isoformat(),
                        'browser': browser
                    }
                    cookies_list.append(cookie_dict)
            
            if not cookies_list:
                self.logger.error("❌ No Facebook cookies found!")
                return False
            
            # Save cookies
            self.cookies = cookies_list
            self._save_cookies(cookies_list)
            
            # Create backup
            self._create_backup(cookies_list)
            
            # Check cookie health
            health = self.check_health()
            
            if health['is_valid']:
                self.logger.info(f"✅ Successfully extracted {len(cookies_list)} cookies")
                self.logger.info(f"📅 Expires: {health['expires_in']}")
                return True
            else:
                self.logger.warning(f"⚠️ Cookies extracted but may be invalid: {health['message']}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Error extracting cookies: {e}")
            return False
    
    def _save_cookies(self, cookies: List[Dict], encrypt: bool = True) -> bool:
        """Save cookies to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.cookie_file), exist_ok=True)
            
            if encrypt:
                # Encrypt cookies before saving
                encrypted_data = self.encryption.encrypt_data(cookies)
                cookies_data = {"encrypted": True, "data": encrypted_data}
            else:
                cookies_data = {"encrypted": False, "data": cookies}
            
            # Save to file
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies_data, f, indent=2)
            
            # Update cookie health
            self._update_cookie_health()
            
            self.logger.info(f"✅ Cookies saved to {self.cookie_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving cookies: {e}")
            return False
    
    def load_cookies(self) -> bool:
        """Load cookies from file"""
        try:
            if not os.path.exists(self.cookie_file):
                self.logger.error(f"❌ Cookie file not found: {self.cookie_file}")
                return False
            
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
            
            if cookies_data.get("encrypted", False):
                # Decrypt cookies
                self.cookies = self.encryption.decrypt_data(cookies_data["data"])
            else:
                self.cookies = cookies_data.get("data", [])
            
            if not self.cookies:
                self.logger.error("❌ No cookies loaded from file")
                return False
            
            # Check health
            health = self.check_health()
            
            if health['is_valid']:
                self.logger.info(f"✅ Loaded {len(self.cookies)} cookies")
                self.logger.info(f"📅 Expires in: {health['expires_in']}")
                return True
            else:
                self.logger.warning(f"⚠️ Loaded cookies may be invalid: {health['message']}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error loading cookies: {e}")
            return False
    
    def check_health(self) -> Dict:
        """Check cookie health and validity"""
        try:
            if not self.cookies:
                return {
                    'is_valid': False,
                    'message': 'No cookies available',
                    'expires_in': 'N/A',
                    'cookie_count': 0
                }
            
            # Check for essential Facebook cookies
            essential_cookies = ['c_user', 'xs', 'fr', 'datr']
            found_cookies = [c['name'] for c in self.cookies]
            
            missing_cookies = [c for c in essential_cookies if c not in found_cookies]
            
            if missing_cookies:
                return {
                    'is_valid': False,
                    'message': f'Missing essential cookies: {missing_cookies}',
                    'expires_in': 'N/A',
                    'cookie_count': len(self.cookies)
                }
            
            # Check expiration
            now = time.time()
            expires_times = []
            
            for cookie in self.cookies:
                if cookie.get('expires'):
                    expires_times.append(cookie['expires'])
            
            if expires_times:
                min_expires = min(expires_times)
                expires_in = min_expires - now
                
                if expires_in <= 0:
                    return {
                        'is_valid': False,
                        'message': 'Cookies have expired',
                        'expires_in': '0 days',
                        'cookie_count': len(self.cookies)
                    }
                elif expires_in < 86400:  # Less than 1 day
                    return {
                        'is_valid': True,
                        'message': 'Cookies expire soon',
                        'expires_in': f'{int(expires_in/3600)} hours',
                        'cookie_count': len(self.cookies)
                    }
                else:
                    return {
                        'is_valid': True,
                        'message': 'Cookies are valid',
                        'expires_in': f'{int(expires_in/86400)} days',
                        'cookie_count': len(self.cookies)
                    }
            else:
                return {
                    'is_valid': True,
                    'message': 'Cookies loaded (no expiration info)',
                    'expires_in': 'Unknown',
                    'cookie_count': len(self.cookies)
                }
                
        except Exception as e:
            return {
                'is_valid': False,
                'message': f'Error checking health: {e}',
                'expires_in': 'N/A',
                'cookie_count': 0
            }
    
    def refresh_cookies(self) -> bool:
        """Refresh cookies by re-extracting from browser"""
        try:
            self.logger.info("🔄 Refreshing cookies...")
            
            # Try different browsers
            browsers = ['chrome', 'firefox', 'edge']
            
            for browser in browsers:
                success = self.extract_cookies(browser)
                if success:
                    self.logger.info(f"✅ Cookies refreshed from {browser}")
                    return True
            
            self.logger.error("❌ Failed to refresh cookies from any browser")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error refreshing cookies: {e}")
            return False
    
    def _create_backup(self, cookies: List[Dict]) -> bool:
        """Create backup of cookies"""
        try:
            os.makedirs(os.path.dirname(self.backup_file), exist_ok=True)
            
            backup_data = {
                'backup_time': datetime.now().isoformat(),
                'cookies': cookies,
                'cookie_count': len(cookies)
            }
            
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2)
            
            self.logger.info(f"✅ Backup created: {self.backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creating backup: {e}")
            return False
    
    def restore_backup(self) -> bool:
        """Restore cookies from backup"""
        try:
            if not os.path.exists(self.backup_file):
                self.logger.error(f"❌ Backup file not found: {self.backup_file}")
                return False
            
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            cookies = backup_data.get('cookies', [])
            
            if not cookies:
                self.logger.error("❌ No cookies in backup")
                return False
            
            self.cookies = cookies
            self._save_cookies(cookies)
            
            self.logger.info(f"✅ Restored {len(cookies)} cookies from backup")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error restoring backup: {e}")
            return False
    
    def _update_cookie_health(self):
        """Update cookie health information"""
        try:
            health_file = "data/cookies/cookie_health.txt"
            health = self.check_health()
            
            health_info = f"""
            🍪 COOKIE HEALTH REPORT
            ======================
            Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            Status: {'✅ VALID' if health['is_valid'] else '❌ INVALID'}
            Message: {health['message']}
            Expires in: {health['expires_in']}
            Cookie count: {health['cookie_count']}
            
            Essential Cookies Check:
            • c_user: {'✅ Found' if 'c_user' in [c['name'] for c in self.cookies] else '❌ Missing'}
            • xs: {'✅ Found' if 'xs' in [c['name'] for c in self.cookies] else '❌ Missing'}
            • fr: {'✅ Found' if 'fr' in [c['name'] for c in self.cookies] else '❌ Missing'}
            • datr: {'✅ Found' if 'datr' in [c['name'] for c in self.cookies] else '❌ Missing'}
            
            Last Extraction: {self.cookies[0].get('extracted_at', 'Unknown') if self.cookies else 'N/A'}
            ======================
            """
            
            with open(health_file, 'w', encoding='utf-8') as f:
                f.write(health_info)
            
            self.logger.info("✅ Cookie health updated")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating cookie health: {e}")
    
    def get_cookie_dict(self) -> Dict:
        """Get cookies as dictionary for requests"""
        cookie_dict = {}
        for cookie in self.cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict
    
    def delete_cookies(self):
        """Delete all stored cookies"""
        try:
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
            
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
            
            self.cookies = []
            self.logger.info("✅ All cookies deleted")
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting cookies: {e}")
    
    def export_cookies(self, format_type: str = "json") -> Optional[str]:
        """Export cookies in specified format"""
        try:
            if format_type.lower() == "json":
                return json.dumps(self.cookies, indent=2)
            elif format_type.lower() == "text":
                lines = []
                for cookie in self.cookies:
                    lines.append(f"{cookie['name']}={cookie['value']}")
                return "\n".join(lines)
            elif format_type.lower() == "netscape":
                # Netscape cookie format
                lines = []
                for cookie in self.cookies:
                    domain = cookie.get('domain', '.facebook.com')
                    path = cookie.get('path', '/')
                    secure = "TRUE" if cookie.get('secure', False) else "FALSE"
                    expires = cookie.get('expires', int(time.time()) + 86400)
                    name = cookie['name']
                    value = cookie['value']
                    
                    lines.append(f"{domain}\tTRUE\t{path}\t{secure}\t{expires}\t{name}\t{value}")
                return "\n".join(lines)
            else:
                self.logger.error(f"❌ Unsupported format: {format_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error exporting cookies: {e}")
            return None