#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 Media Handling System
Photo, video, and file handling
"""

import os
import json
import time
import mimetypes
from datetime import datetime
from typing import Dict, List, Optional, Any, BinaryIO
import requests
from PIL import Image
import io

from utils.logger import setup_logger
from utils.file_handler import FileHandler


class MediaHandler:
    """🎭 Media Handling System"""
    
    def __init__(self):
        self.logger = setup_logger("media_handler", "data/logs/media_handler.log")
        self.file_handler = FileHandler()
        
        # Media storage configuration
        self.media_dir = "data/media"
        self.cache_dir = "data/media/cache"
        self.temp_dir = "temp/uploads"
        
        # Supported media types
        self.supported_formats = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "videos": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
            "documents": [".pdf", ".doc", ".docx", ".txt", ".zip", ".rar"]
        }
        
        # Max file sizes (in bytes)
        self.max_sizes = {
            "images": 10 * 1024 * 1024,      # 10MB
            "videos": 50 * 1024 * 1024,      # 50MB
            "documents": 20 * 1024 * 1024    # 20MB
        }
        
        # Initialize
        self.initialize()
    
    def initialize(self):
        """Initialize media handler"""
        try:
            self.logger.info("🎭 Initializing Media Handler...")
            
            # Create media directories
            self._create_media_directories()
            
            # Load media database
            self.media_db = self._load_media_database()
            
            self.logger.info("✅ Media Handler initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing media handler: {e}")
    
    def _create_media_directories(self):
        """Create media directories"""
        directories = [
            self.media_dir,
            os.path.join(self.media_dir, "images"),
            os.path.join(self.media_dir, "videos"),
            os.path.join(self.media_dir, "documents"),
            os.path.join(self.media_dir, "thumbnails"),
            self.cache_dir,
            self.temp_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_media_database(self) -> Dict:
        """Load media database"""
        try:
            db_file = os.path.join(self.media_dir, "media_database.json")
            if os.path.exists(db_file):
                with open(db_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return {
                    "images": {},
                    "videos": {},
                    "documents": {},
                    "total_files": 0,
                    "total_size": 0,
                    "last_updated": datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.error(f"Error loading media database: {e}")
            return {}
    
    def _save_media_database(self):
        """Save media database"""
        try:
            db_file = os.path.join(self.media_dir, "media_database.json")
            self.media_db["last_updated"] = datetime.now().isoformat()
            self.file_handler.write_json(db_file, self.media_db)
        except Exception as e:
            self.logger.error(f"Error saving media database: {e}")
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in self.supported_formats.items():
            if ext in extensions:
                return file_type
        
        return "unknown"
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        file_type = self.get_file_type(filename)
        return file_type != "unknown"
    
    def validate_file_size(self, file_path: str, file_type: str = None) -> bool:
        """Validate file size"""
        try:
            if file_type is None:
                file_type = self.get_file_type(file_path)
            
            if file_type not in self.max_sizes:
                return False
            
            file_size = os.path.getsize(file_path)
            max_size = self.max_sizes.get(file_type, 0)
            
            return file_size <= max_size
            
        except Exception as e:
            self.logger.error(f"Error validating file size: {e}")
            return False
    
    def save_media(self, file_path: str, media_type: str = None, metadata: Dict = None) -> Optional[str]:
        """Save media file to storage"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return None
            
            # Get file info
            filename = os.path.basename(file_path)
            file_type = media_type or self.get_file_type(filename)
            
            if file_type == "unknown":
                self.logger.error(f"Unsupported file format: {filename}")
                return None
            
            # Validate file size
            if not self.validate_file_size(file_path, file_type):
                self.logger.error(f"File too large: {filename}")
                return None
            
            # Generate unique filename
            timestamp = int(time.time())
            unique_id = f"{timestamp}_{os.urandom(4).hex()}"
            new_filename = f"{unique_id}{os.path.splitext(filename)[1]}"
            
            # Determine save directory
            save_dir = os.path.join(self.media_dir, file_type + "s")  # images, videos, documents
            save_path = os.path.join(save_dir, new_filename)
            
            # Copy file
            import shutil
            shutil.copy2(file_path, save_path)
            
            # Get file stats
            file_size = os.path.getsize(save_path)
            created_time = datetime.fromtimestamp(os.path.getctime(save_path))
            
            # Create thumbnail for images
            thumbnail_path = None
            if file_type == "images":
                thumbnail_path = self.create_thumbnail(save_path, new_filename)
            
            # Prepare metadata
            file_metadata = {
                "original_filename": filename,
                "stored_filename": new_filename,
                "file_type": file_type,
                "file_size": file_size,
                "mime_type": mimetypes.guess_type(filename)[0] or "application/octet-stream",
                "created_at": created_time.isoformat(),
                "saved_at": datetime.now().isoformat(),
                "thumbnail": thumbnail_path,
                "file_path": save_path,
                "access_count": 0,
                "last_accessed": datetime.now().isoformat()
            }
            
            # Add custom metadata if provided
            if metadata:
                file_metadata.update(metadata)
            
            # Add to database
            if file_type not in self.media_db:
                self.media_db[file_type] = {}
            
            self.media_db[file_type][unique_id] = file_metadata
            self.media_db["total_files"] = self.media_db.get("total_files", 0) + 1
            self.media_db["total_size"] = self.media_db.get("total_size", 0) + file_size
            
            # Save database
            self._save_media_database()
            
            self.logger.info(f"Saved media: {filename} -> {new_filename} ({file_size} bytes)")
            
            return unique_id
            
        except Exception as e:
            self.logger.error(f"❌ Error saving media: {e}")
            return None
    
    def create_thumbnail(self, image_path: str, output_name: str = None, size: tuple = (200, 200)) -> Optional[str]:
        """Create thumbnail for image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                thumb_dir = os.path.join(self.media_dir, "thumbnails")
                os.makedirs(thumb_dir, exist_ok=True)
                
                if output_name is None:
                    output_name = os.path.basename(image_path)
                
                thumb_name = f"thumb_{output_name}"
                thumb_path = os.path.join(thumb_dir, thumb_name)
                
                # Save as JPEG for consistency
                if not thumb_path.lower().endswith('.jpg'):
                    thumb_path = os.path.splitext(thumb_path)[0] + '.jpg'
                
                img.save(thumb_path, "JPEG", quality=85)
                
                self.logger.debug(f"Created thumbnail: {thumb_path}")
                return thumb_path
                
        except Exception as e:
            self.logger.error(f"❌ Error creating thumbnail: {e}")
            return None
    
    def get_media_info(self, media_id: str) -> Optional[Dict]:
        """Get media information by ID"""
        try:
            for file_type in ["images", "videos", "documents"]:
                if file_type in self.media_db and media_id in self.media_db[file_type]:
                    # Update access stats
                    self.media_db[file_type][media_id]["access_count"] += 1
                    self.media_db[file_type][media_id]["last_accessed"] = datetime.now().isoformat()
                    self._save_media_database()
                    
                    return self.media_db[file_type][media_id]
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting media info: {e}")
            return None
    
    def get_media_path(self, media_id: str) -> Optional[str]:
        """Get file path by media ID"""
        media_info = self.get_media_info(media_id)
        if media_info:
            return media_info.get("file_path")
        return None
    
    def download_media(self, url: str, filename: str = None) -> Optional[str]:
        """Download media from URL"""
        try:
            self.logger.info(f"Downloading media from URL: {url}")
            
            # Send request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            # Determine filename
            if filename is None:
                # Try to get filename from URL
                filename = os.path.basename(url.split("?")[0])
                if not filename:
                    filename = f"downloaded_{int(time.time())}"
            
            # Save to temp file
            temp_path = os.path.join(self.temp_dir, filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Downloaded media: {filename} ({os.path.getsize(temp_path)} bytes)")
            
            return temp_path
            
        except Exception as e:
            self.logger.error(f"❌ Error downloading media: {e}")
            return None
    
    def download_and_save(self, url: str, metadata: Dict = None) -> Optional[str]:
        """Download media from URL and save to storage"""
        try:
            # Download to temp file
            temp_path = self.download_media(url)
            if not temp_path or not os.path.exists(temp_path):
                return None
            
            # Save to media storage
            media_id = self.save_media(temp_path, metadata=metadata)
            
            # Cleanup temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            return media_id
            
        except Exception as e:
            self.logger.error(f"❌ Error downloading and saving media: {e}")
            return None
    
    def resize_image(self, image_path: str, max_width: int = 800, max_height: int = 800) -> Optional[str]:
        """Resize image to specified dimensions"""
        try:
            with Image.open(image_path) as img:
                # Calculate new dimensions
                width, height = img.size
                
                if width <= max_width and height <= max_height:
                    return image_path  # No resize needed
                
                # Calculate new size maintaining aspect ratio
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save resized image
                resized_path = os.path.join(self.cache_dir, f"resized_{os.path.basename(image_path)}")
                resized_img.save(resized_path, quality=85)
                
                self.logger.debug(f"Resized image: {width}x{height} -> {new_width}x{new_height}")
                
                return resized_path
                
        except Exception as e:
            self.logger.error(f"❌ Error resizing image: {e}")
            return None
    
    def convert_image_format(self, image_path: str, target_format: str = "JPEG") -> Optional[str]:
        """Convert image to different format"""
        try:
            if target_format.upper() not in ["JPEG", "PNG", "WEBP"]:
                self.logger.error(f"Unsupported target format: {target_format}")
                return None
            
            with Image.open(image_path) as img:
                # Convert to RGB if converting to JPEG
                if target_format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Save in new format
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                converted_path = os.path.join(self.cache_dir, f"{base_name}.{target_format.lower()}")
                
                img.save(converted_path, target_format.upper(), quality=85)
                
                self.logger.debug(f"Converted image to {target_format}: {converted_path}")
                
                return converted_path
                
        except Exception as e:
            self.logger.error(f"❌ Error converting image: {e}")
            return None
    
    def extract_image_metadata(self, image_path: str) -> Dict:
        """Extract metadata from image"""
        try:
            metadata = {
                "format": None,
                "size": None,
                "mode": None,
                "exif": {}
            }
            
            with Image.open(image_path) as img:
                metadata["format"] = img.format
                metadata["size"] = img.size
                metadata["mode"] = img.mode
                
                # Try to extract EXIF data
                try:
                    exif_data = img._getexif()
                    if exif_data:
                        # Convert EXIF tags to readable names
                        from PIL.ExifTags import TAGS
                        for tag_id, value in exif_data.items():
                            tag_name = TAGS.get(tag_id, tag_id)
                            metadata["exif"][tag_name] = value
                except:
                    pass
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting image metadata: {e}")
            return {}
    
    def search_media(self, query: str, media_type: str = None, limit: int = 20) -> List[Dict]:
        """Search for media"""
        try:
            results = []
            query_lower = query.lower()
            
            # Determine which media types to search
            if media_type:
                media_types = [media_type]
            else:
                media_types = ["images", "videos", "documents"]
            
            for m_type in media_types:
                if m_type in self.media_db:
                    for media_id, media_info in self.media_db[m_type].items():
                        original_name = media_info.get("original_filename", "").lower()
                        
                        if query_lower in original_name:
                            results.append({
                                "media_id": media_id,
                                "original_filename": media_info.get("original_filename"),
                                "file_type": m_type,
                                "file_size": media_info.get("file_size"),
                                "created_at": media_info.get("created_at"),
                                "access_count": media_info.get("access_count", 0)
                            })
                        
                        if len(results) >= limit:
                            break
                
                if len(results) >= limit:
                    break
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching media: {e}")
            return []
    
    def delete_media(self, media_id: str) -> bool:
        """Delete media file"""
        try:
            # Find media in database
            media_info = None
            media_type = None
            
            for file_type in ["images", "videos", "documents"]:
                if file_type in self.media_db and media_id in self.media_db[file_type]:
                    media_info = self.media_db[file_type][media_id]
                    media_type = file_type
                    break
            
            if not media_info:
                self.logger.warning(f"Media not found: {media_id}")
                return False
            
            # Delete main file
            file_path = media_info.get("file_path")
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                self.logger.debug(f"Deleted file: {file_path}")
            
            # Delete thumbnail if exists
            thumbnail_path = media_info.get("thumbnail")
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                self.logger.debug(f"Deleted thumbnail: {thumbnail_path}")
            
            # Remove from database
            del self.media_db[media_type][media_id]
            self.media_db["total_files"] = max(0, self.media_db.get("total_files", 0) - 1)
            self.media_db["total_size"] = max(0, self.media_db.get("total_size", 0) - media_info.get("file_size", 0))
            
            # Save database
            self._save_media_database()
            
            self.logger.info(f"Deleted media: {media_id} ({media_info.get('original_filename')})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting media: {e}")
            return False
    
    def cleanup_cache(self, max_age_hours: int = 24) -> int:
        """Cleanup old cache files"""
        try:
            current_time = time.time()
            cutoff_time = current_time - (max_age_hours * 3600)
            deleted_count = 0
            
            # Clean cache directory
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    file_path = os.path.join(self.cache_dir, filename)
                    try:
                        file_time = os.path.getmtime(file_path)
                        if file_time < cutoff_time:
                            os.remove(file_path)
                            deleted_count += 1
                            self.logger.debug(f"Cleaned cache file: {filename}")
                    except Exception as e:
                        self.logger.error(f"Error cleaning cache file {filename}: {e}")
            
            # Clean temp directory
            if os.path.exists(self.temp_dir):
                for filename in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, filename)
                    try:
                        file_time = os.path.getmtime(file_path)
                        if file_time < cutoff_time:
                            os.remove(file_path)
                            deleted_count += 1
                            self.logger.debug(f"Cleaned temp file: {filename}")
                    except Exception as e:
                        self.logger.error(f"Error cleaning temp file {filename}: {e}")
            
            self.logger.info(f"Cleaned up {deleted_count} cache/temp files")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning cache: {e}")
            return 0
    
    def get_media_stats(self) -> Dict:
        """Get media statistics"""
        try:
            total_files = self.media_db.get("total_files", 0)
            total_size = self.media_db.get("total_size", 0)
            
            # Count by type
            type_counts = {}
            type_sizes = {}
            
            for file_type in ["images", "videos", "documents"]:
                if file_type in self.media_db:
                    count = len(self.media_db[file_type])
                    type_counts[file_type] = count
                    
                    # Calculate total size for this type
                    size = sum(
                        media_info.get("file_size", 0)
                        for media_info in self.media_db[file_type].values()
                    )
                    type_sizes[file_type] = size
            
            # Most accessed files
            all_media = []
            for file_type in ["images", "videos", "documents"]:
                if file_type in self.media_db:
                    for media_id, media_info in self.media_db[file_type].items():
                        all_media.append({
                            "media_id": media_id,
                            "original_filename": media_info.get("original_filename"),
                            "file_type": file_type,
                            "access_count": media_info.get("access_count", 0),
                            "last_accessed": media_info.get("last_accessed")
                        })
            
            # Sort by access count (descending)
            all_media.sort(key=lambda x: x.get("access_count", 0), reverse=True)
            most_accessed = all_media[:10] if len(all_media) > 10 else all_media
            
            return {
                "total_files": total_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "type_counts": type_counts,
                "type_sizes_mb": {k: round(v / (1024 * 1024), 2) for k, v in type_sizes.items()},
                "most_accessed_files": most_accessed,
                "cache_dir_size": self._get_directory_size(self.cache_dir),
                "temp_dir_size": self._get_directory_size(self.temp_dir),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting media stats: {e}")
            return {}
    
    def _get_directory_size(self, directory: str) -> int:
        """Get total size of directory"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
            return total_size
        except:
            return 0
    
    def backup_media_database(self) -> str:
        """Backup media database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/media/backups/media_db_{timestamp}.json"
            
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            
            # Copy database file
            db_file = os.path.join(self.media_dir, "media_database.json")
            if os.path.exists(db_file):
                import shutil
                shutil.copy2(db_file, backup_file)
                
                self.logger.info(f"Media database backed up: {backup_file}")
                return backup_file
            
            return ""
            
        except Exception as e:
            self.logger.error(f"❌ Error backing up media database: {e}")
            return ""