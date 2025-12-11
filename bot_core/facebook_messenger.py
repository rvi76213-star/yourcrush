#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📘 Facebook Messenger Integration
Handles Facebook authentication and messaging
"""

import json
import logging
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from utils.encryption import Encryption
from utils.logger import setup_logger


class FacebookMessenger:
    """💬 Facebook Messenger API Integration"""
    
    def __init__(self):
        self.logger = setup_logger("facebook_messenger", "data/logs/bot_activity.log")
        self.encryption = Encryption()
        self.session = requests.Session()
        self.user_id = None
        self.connected = False
        
        # Load configuration
        self.config = self._load_config()
        
        # Headers to mimic browser
        self.headers = {
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
        }
        
        self.session.headers.update(self.headers)
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    
    def login(self) -> bool:
        """Login to Facebook using cookies"""
        try:
            self.logger.info("🔑 Logging in to Facebook...")
            
            # Load cookies
            cookies = self._load_cookies()
            if not cookies:
                self.logger.error("❌ No cookies found!")
                return False
            
            # Add cookies to session
            for cookie in cookies:
                self.session.cookies.set(cookie["name"], cookie["value"])
            
            # Test login by accessing home page
            response = self.session.get("https://www.facebook.com/")
            
            if "login" in response.url or "checkpoint" in response.url:
                self.logger.error("❌ Login failed - Redirected to login page")
                return False
            
            # Extract user ID from page
            self.user_id = self._extract_user_id(response.text)
            
            if self.user_id:
                self.connected = True
                self.logger.info(f"✅ Logged in as user: {self.user_id}")
                return True
            else:
                self.logger.error("❌ Could not extract user ID")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Login error: {e}")
            return False
    
    def _load_cookies(self) -> List[Dict]:
        """Load cookies from file"""
        try:
            with open("data/cookies/master_cookies.json", "r", encoding="utf-8") as f:
                cookies_data = json.load(f)
                
            # Decrypt if encrypted
            if isinstance(cookies_data, dict) and "encrypted" in cookies_data:
                cookies_data = self.encryption.decrypt_data(cookies_data)
            
            return cookies_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load cookies: {e}")
            return []
    
    def _extract_user_id(self, html_content: str) -> Optional[str]:
        """Extract user ID from Facebook page"""
        try:
            # Method 1: Look for user ID in page
            import re
            
            # Pattern for user ID
            patterns = [
                r'"userID":"(\d+)"',
                r'"actorID":"(\d+)"',
                r'{"id":"(\d+)"',
                r'profile_id=(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html_content)
                if match:
                    return match.group(1)
            
            # Method 2: Try to get from GraphQL
            graphql_pattern = r'{"viewer":"(\d+)"'
            match = re.search(graphql_pattern, html_content)
            if match:
                return match.group(1)
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract user ID: {e}")
            return None
    
    def get_unread_messages(self) -> List[Dict]:
        """Get unread messages from Facebook"""
        try:
            if not self.connected:
                self.logger.warning("Not connected to Facebook")
                return []
            
            # Facebook API endpoint for messages
            url = "https://www.facebook.com/api/graphqlbatch/"
            
            # GraphQL query for messages
            query = {
                "av": self.user_id,
                "__user": self.user_id,
                "__a": 1,
                "__req": 1,
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "MessengerThreadlistQuery",
                "variables": json.dumps({
                    "limit": 20,
                    "before": None,
                    "tags": ["INBOX"],
                    "includeDeliveryReceipts": True,
                    "includeSeqID": False
                }),
                "doc_id": "3336392669271570"  # Messenger query ID
            }
            
            response = self.session.post(url, data=query)
            
            if response.status_code == 200:
                messages = self._parse_messages_response(response.text)
                return messages
            else:
                self.logger.error(f"❌ Failed to get messages: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Error getting messages: {e}")
            return []
    
    def _parse_messages_response(self, response_text: str) -> List[Dict]:
        """Parse Facebook GraphQL response"""
        try:
            messages = []
            
            # Remove Facebook's JSON wrapper
            if response_text.startswith("for (;;);"):
                response_text = response_text[9:]
            
            data = json.loads(response_text)
            
            # Navigate through GraphQL response
            # This is simplified - actual Facebook response is complex
            # You'll need to adjust based on actual response structure
            
            # Placeholder logic - replace with actual parsing
            # Check for messages in response
            if "data" in data:
                thread_list = data["data"].get("viewer", {}).get("message_threads", {}).get("nodes", [])
                
                for thread in thread_list:
                    last_message = thread.get("last_message")
                    if last_message:
                        message = {
                            "thread_id": thread.get("thread_key", {}).get("thread_fbid"),
                            "sender_id": last_message.get("message_sender", {}).get("id"),
                            "sender_name": last_message.get("message_sender", {}).get("name"),
                            "text": last_message.get("message", {}).get("text"),
                            "timestamp": last_message.get("timestamp_precise"),
                            "is_unread": thread.get("unread_count", 0) > 0,
                            "is_group": thread.get("thread_type") == "GROUP"
                        }
                        
                        if message["is_unread"] and message["text"]:
                            messages.append(message)
            
            return messages
            
        except Exception as e:
            self.logger.error(f"❌ Error parsing messages: {e}")
            return []
    
    def send_message(self, thread_id: str, message: str) -> bool:
        """Send message to Facebook thread"""
        try:
            if not self.connected:
                self.logger.warning("Not connected to Facebook")
                return False
            
            # Add human-like delay
            time.sleep(self.config.get("response_delay", 2))
            
            # Facebook send message endpoint
            url = "https://www.facebook.com/messaging/send/"
            
            # Prepare form data
            form_data = {
                "action_type": "ma-type:user-generated-message",
                "body": message,
                "ephemeral_ttl_mode": "0",
                "has_attachment": "false",
                "message_id": self._generate_message_id(),
                "offline_threading_id": self._generate_message_id(),
                "source": "source:chat:web",
                "specific_to_list[0]": "fbid:" + thread_id,
                "timestamp": str(int(time.time() * 1000)),
                "ui_push_phase": "C3"
            }
            
            # Add required Facebook parameters
            fb_dtsg = self._get_fb_dtsg()
            if fb_dtsg:
                form_data["fb_dtsg"] = fb_dtsg
            
            form_data["__user"] = self.user_id
            form_data["__a"] = "1"
            form_data["__req"] = "1"
            
            # Send message
            response = self.session.post(url, data=form_data)
            
            if response.status_code == 200:
                self.logger.info(f"✅ Message sent to {thread_id}")
                return True
            else:
                self.logger.error(f"❌ Failed to send message: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending message: {e}")
            return False
    
    def send_photo(self, thread_id: str, photo_path: str, caption: str = "") -> bool:
        """Send photo to Facebook thread"""
        try:
            if not self.connected:
                self.logger.warning("Not connected to Facebook")
                return False
            
            # Upload photo endpoint
            upload_url = "https://upload.facebook.com/ajax/mercury/upload.php"
            
            # Read photo file
            with open(photo_path, "rb") as f:
                photo_data = f.read()
            
            # Prepare multipart form data
            files = {
                "upload_1024": (os.path.basename(photo_path), photo_data, "image/jpeg")
            }
            
            data = {
                "recipient_map[0][id]": thread_id,
                "recipient_map[0][type]": "thread",
                "voice_clip": "false",
                "send_method": "messenger_composer",
                "image_height": "1024",
                "image_width": "1024",
                "image_type": "FILE_ATTACHMENT",
                "source": "source:chat:web",
                "__user": self.user_id,
                "__a": "1",
                "__req": "1"
            }
            
            # Add fb_dtsg
            fb_dtsg = self._get_fb_dtsg()
            if fb_dtsg:
                data["fb_dtsg"] = fb_dtsg
            
            # Upload photo
            response = self.session.post(upload_url, files=files, data=data)
            
            if response.status_code == 200:
                self.logger.info(f"✅ Photo sent to {thread_id}")
                return True
            else:
                self.logger.error(f"❌ Failed to send photo: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending photo: {e}")
            return False
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        import random
        import string
        
        timestamp = str(int(time.time() * 1000))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"mid.{timestamp}:{random_str}"
    
    def _get_fb_dtsg(self) -> Optional[str]:
        """Get Facebook fb_dtsg token"""
        try:
            # Get homepage to extract fb_dtsg
            response = self.session.get("https://www.facebook.com/")
            
            # Extract fb_dtsg from page
            import re
            pattern = r'"token":"([^"]+)"'
            match = re.search(pattern, response.text)
            
            if match:
                return match.group(1)
            
            # Alternative pattern
            pattern2 = r'name="fb_dtsg" value="([^"]+)"'
            match2 = re.search(pattern2, response.text)
            
            if match2:
                return match2.group(1)
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get fb_dtsg: {e}")
            return None
    
    def logout(self):
        """Logout from Facebook"""
        try:
            self.session.get("https://www.facebook.com/logout.php")
            self.connected = False
            self.user_id = None
            self.logger.info("✅ Logged out from Facebook")
            
        except Exception as e:
            self.logger.error(f"❌ Logout error: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to Facebook"""
        return self.connected
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        try:
            if not self.connected:
                return None
            
            # Facebook profile endpoint
            url = f"https://www.facebook.com/{user_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                # Parse user info from page
                import re
                
                user_info = {}
                
                # Extract name
                name_pattern = r'<title>([^<]+)</title>'
                name_match = re.search(name_pattern, response.text)
                if name_match:
                    user_info["name"] = name_match.group(1).split("|")[0].strip()
                
                # Extract profile picture URL
                pic_pattern = r'profilePicLarge":{"uri":"([^"]+)"'
                pic_match = re.search(pic_pattern, response.text)
                if pic_match:
                    user_info["profile_pic"] = pic_match.group(1)
                
                return user_info
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error getting user info: {e}")
            return None