#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📸 Photo Delivery System
Handles sending bot photos and admin photos
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from utils.logger import setup_logger
from utils.file_handler import FileHandler


class PhotoDelivery:
    """📸 Photo Delivery System"""
    
    def __init__(self):
        self.logger = setup_logger("photo_delivery", "data/logs/bot_activity.log")
        self.file_handler = FileHandler()
        self.photos_sent = 0
        
        # Load configuration
        self.config = self._load_config()
        
        # Photo cache
        self.photo_cache = {}
        self.cache_duration = 3600  # 1 hour
        
        # Photo request patterns
        self.bot_photo_patterns = [
            "ছবি দাও", "ফটো চাই", "তোমার ছবি", 
            "your photo", "photo please", "send pic",
            "picture please", "তোমার ফটো", "তোমার ফটো দাও"
        ]
        
        self.admin_photo_patterns = [
            "এডমিনের ছবি", "বটের এডমিনের ছবি", "মালিকের ছবি",
            "admin photo", "owner photo", "master photo",
            "তোমার মালিকের ছবি", "তোমার এডমিনের ছবি"
        ]
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"photos": {"local_photos": ["master.jpg", "photo.jpg", "own.jpg"]}}
    
    def is_photo_request(self, message: str) -> Dict:
        """Check if message is requesting a photo"""
        message_lower = message.lower()
        
        # Check for bot photo requests
        for pattern in self.bot_photo_patterns:
            if pattern.lower() in message_lower:
                return {
                    "is_request": True,
                    "photo_type": "bot",
                    "confidence": 0.9
                }
        
        # Check for admin photo requests
        for pattern in self.admin_photo_patterns:
            if pattern.lower() in message_lower:
                return {
                    "is_request": True,
                    "photo_type": "admin",
                    "confidence": 0.9
                }
        
        # Check for generic photo requests
        photo_keywords = ["ছবি", "ফটো", "photo", "pic", "picture", "img", "image"]
        request_keywords = ["দাও", "চাই", "পাঠাও", "send", "show", "give"]
        
        has_photo_word = any(keyword in message_lower for keyword in photo_keywords)
        has_request_word = any(keyword in message_lower for keyword in request_keywords)
        
        if has_photo_word and has_request_word:
            return {
                "is_request": True,
                "photo_type": "unknown",
                "confidence": 0.7
            }
        
        return {
            "is_request": False,
            "photo_type": None,
            "confidence": 0.0
        }
    
    def get_photo(self, photo_type: str = "bot") -> Optional[str]:
        """Get photo path based on type"""
        try:
            if photo_type == "bot":
                return self._get_bot_photo()
            elif photo_type == "admin":
                return self._get_admin_photo()
            else:
                # Default to bot photo
                return self._get_bot_photo()
                
        except Exception as e:
            self.logger.error(f"❌ Error getting photo: {e}")
            return None
    
    def _get_bot_photo(self) -> Optional[str]:
        """Get bot's photo from local files"""
        try:
            photos_folder = "data/photos/"
            
            # List of possible photo files
            photo_files = [
                "master.jpg", "master.png",
                "photo.jpg", "photo.png",
                "own.jpg", "own.png"
            ]
            
            # Check for existing photos
            for photo_file in photo_files:
                photo_path = os.path.join(photos_folder, photo_file)
                if os.path.exists(photo_path):
                    # Check file size (avoid empty files)
                    if os.path.getsize(photo_path) > 1024:  # At least 1KB
                        self.logger.info(f"✅ Found bot photo: {photo_file}")
                        return photo_path
            
            # If no photo found, use default or download
            self.logger.warning("⚠️ No bot photos found! Using default...")
            
            # Create a default photo
            default_photo = self._create_default_photo()
            return default_photo
            
        except Exception as e:
            self.logger.error(f"❌ Error getting bot photo: {e}")
            return None
    
    def _get_admin_photo(self) -> Optional[str]:
        """Get admin's photo from Facebook or cache"""
        try:
            # Check cache first
            cache_key = "admin_photo"
            if cache_key in self.photo_cache:
                cached_data = self.photo_cache[cache_key]
                if datetime.now().timestamp() - cached_data["timestamp"] < self.cache_duration:
                    self.logger.info("✅ Using cached admin photo")
                    return cached_data["path"]
            
            # Download from Facebook
            facebook_url = "https://www.facebook.com/share/17gEJAipcr/"
            
            self.logger.info(f"📥 Downloading admin photo from Facebook...")
            
            # Download profile picture
            photo_path = self._download_facebook_photo(facebook_url)
            
            if photo_path and os.path.exists(photo_path):
                # Cache the photo
                self.photo_cache[cache_key] = {
                    "path": photo_path,
                    "timestamp": datetime.now().timestamp(),
                    "source": "facebook"
                }
                
                self.logger.info(f"✅ Admin photo downloaded: {photo_path}")
                return photo_path
            else:
                # Fallback to bot photo
                self.logger.warning("⚠️ Failed to download admin photo, using bot photo")
                return self._get_bot_photo()
                
        except Exception as e:
            self.logger.error(f"❌ Error getting admin photo: {e}")
            return self._get_bot_photo()
    
    def _download_facebook_photo(self, profile_url: str) -> Optional[str]:
        """Download profile photo from Facebook"""
        try:
            # This is a simplified version
            # In reality, you need to parse Facebook page and extract profile picture URL
            
            # For now, return a placeholder
            return self._create_default_photo("admin")
            
            # Actual implementation would involve:
            # 1. Loading the profile page
            # 2. Extracting profile picture URL from HTML
            # 3. Downloading the image
            # 4. Saving to local file
            
        except Exception as e:
            self.logger.error(f"❌ Error downloading Facebook photo: {e}")
            return None
    
    def _create_default_photo(self, photo_type: str = "bot") -> str:
        """Create a default photo"""
        try:
            photos_folder = "data/photos/"
            os.makedirs(photos_folder, exist_ok=True)
            
            if photo_type == "bot":
                photo_path = os.path.join(photos_folder, "default_bot.jpg")
                text = "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0"
            else:
                photo_path = os.path.join(photos_folder, "default_admin.jpg")
                text = "ADMIN"
            
            # Create a simple image with PIL
            try:
                from PIL import Image, ImageDraw, ImageFont
                
                # Create image
                img = Image.new('RGB', (500, 500), color=(0, 0, 0))
                d = ImageDraw.Draw(img)
                
                # Add text
                try:
                    font = ImageFont.truetype("arial.ttf", 40)
                except:
                    font = ImageFont.load_default()
                
                d.text((150, 230), text, fill=(255, 255, 255), font=font)
                
                # Save image
                img.save(photo_path, "JPEG")
                
                self.logger.info(f"✅ Created default photo: {photo_path}")
                return photo_path
                
            except ImportError:
                # If PIL not available, create empty file
                with open(photo_path, 'wb') as f:
                    f.write(b'')
                
                self.logger.warning(f"⚠️ PIL not available, created empty photo file")
                return photo_path
                
        except Exception as e:
            self.logger.error(f"❌ Error creating default photo: {e}")
            return ""
    
    def save_photo(self, photo_path: str, photo_type: str = "user") -> bool:
        """Save a photo to the bot's collection"""
        try:
            if not os.path.exists(photo_path):
                self.logger.error(f"❌ Photo file not found: {photo_path}")
                return False
            
            photos_folder = "data/photos/"
            os.makedirs(photos_folder, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{photo_type}_{timestamp}.jpg"
            save_path = os.path.join(photos_folder, filename)
            
            # Copy photo
            import shutil
            shutil.copy2(photo_path, save_path)
            
            # Create thumbnail
            self._create_thumbnail(save_path)
            
            self.logger.info(f"✅ Photo saved: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving photo: {e}")
            return False
    
    def _create_thumbnail(self, photo_path: str, size: tuple = (200, 200)) -> bool:
        """Create thumbnail for photo"""
        try:
            from PIL import Image
            
            img = Image.open(photo_path)
            img.thumbnail(size)
            
            # Save thumbnail
            thumb_folder = "data/photos/thumbnails/"
            os.makedirs(thumb_folder, exist_ok=True)
            
            thumb_name = os.path.basename(photo_path)
            thumb_path = os.path.join(thumb_folder, f"thumb_{thumb_name}")
            
            img.save(thumb_path, "JPEG")
            
            self.logger.info(f"✅ Thumbnail created: {thumb_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creating thumbnail: {e}")
            return False
    
    def get_photo_list(self, photo_type: str = "all") -> List[str]:
        """Get list of available photos"""
        try:
            photos_folder = "data/photos/"
            
            if not os.path.exists(photos_folder):
                return []
            
            photo_files = []
            for file in os.listdir(photos_folder):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    if photo_type == "all":
                        photo_files.append(file)
                    elif photo_type in file:
                        photo_files.append(file)
            
            return sorted(photo_files)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting photo list: {e}")
            return []
    
    def delete_photo(self, photo_name: str) -> bool:
        """Delete a photo"""
        try:
            photo_path = os.path.join("data/photos/", photo_name)
            thumb_path = os.path.join("data/photos/thumbnails/", f"thumb_{photo_name}")
            
            deleted = False
            
            if os.path.exists(photo_path):
                os.remove(photo_path)
                self.logger.info(f"✅ Deleted photo: {photo_path}")
                deleted = True
            
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
                self.logger.info(f"✅ Deleted thumbnail: {thumb_path}")
            
            return deleted
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting photo: {e}")
            return False
    
    def clear_cache(self):
        """Clear photo cache"""
        self.photo_cache = {}
        self.logger.info("✅ Photo cache cleared")
    
    def get_stats(self) -> Dict:
        """Get photo delivery statistics"""
        try:
            photos_folder = "data/photos/"
            thumb_folder = "data/photos/thumbnails/"
            
            total_photos = 0
            total_size = 0
            
            if os.path.exists(photos_folder):
                for file in os.listdir(photos_folder):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        total_photos += 1
                        file_path = os.path.join(photos_folder, file)
                        total_size += os.path.getsize(file_path)
            
            return {
                "photos_sent": self.photos_sent,
                "total_photos": total_photos,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_size": len(self.photo_cache),
                "last_photo_sent": self.photos_sent
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting stats: {e}")
            return {}