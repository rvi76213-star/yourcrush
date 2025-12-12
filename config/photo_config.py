"""
📸 Photo Configuration Module
"""

import os
from pathlib import Path

PHOTO_CONFIG = {
    # Photo Storage
    "storage": {
        "photos_directory": "data/photos",
        "thumbnails_directory": "data/photos/thumbnails",
        "cache_directory": "data/cache/photos",
        "backup_directory": "data/backup/photos",
        "temp_directory": "temp/uploads"
    },
    
    # Photo Files
    "photo_files": {
        "master": ["master.jpg", "master.png", "master.jpeg"],
        "regular": ["photo.jpg", "photo.png", "photo.jpeg"],
        "personal": ["own.jpg", "own.png", "own.jpeg"],
        "additional": ["extra1.jpg", "extra2.jpg", "extra3.jpg"]
    },
    
    # Photo Delivery Settings
    "delivery": {
        "default_photo": "master.jpg",
        "rotation_enabled": True,
        "rotation_interval": 24,  # hours
        "smart_selection": True,
        "user_preferences": True,
        "context_aware": True
    },
    
    # Facebook Photos
    "facebook": {
        "fetch_enabled": True,
        "profile_url": "https://www.facebook.com/share/17gEJAipcr/",
        "cache_duration": 3600,  # seconds
        "max_size": "1080x1080",
        "quality": "high",
        "fallback_to_local": True
    },
    
    # Photo Processing
    "processing": {
        "auto_resize": True,
        "max_width": 1080,
        "max_height": 1080,
        "quality_percentage": 85,
        "add_watermark": False,
        "watermark_text": "YOUR CRUSH ⟵o_0",
        "optimize_for_messenger": True,
        "convert_to_jpg": True
    },
    
    # Thumbnail Settings
    "thumbnails": {
        "create_thumbnails": True,
        "thumbnail_size": "200x200",
        "keep_aspect_ratio": True,
        "thumbnail_quality": 70,
        "cache_thumbnails": True
    },
    
    # Request Detection
    "request_detection": {
        "keywords": {
            "photo": ["ছবি", "ফটো", "picture", "pic", "image", "img"],
            "your_photo": ["তোমার ছবি", "your photo", "তোমার ফটো", "your pic"],
            "bot_photo": ["বটের ছবি", "bot photo", "বটের ফটো"],
            "admin_photo": ["এডমিনের ছবি", "admin photo", "মাস্টারের ছবি"],
            "send_photo": ["দাও", "send", "পাঠাও", "show", "দেখাও"]
        },
        "priority_order": ["your_photo", "bot_photo", "admin_photo", "photo"],
        "fuzzy_matching": True,
        "min_confidence": 0.6
    },
    
    # Response Messages
    "responses": {
        "sending_photo": [
            "📸 এই নাও আমার ছবি! 😊",
            "🤖 তোমার জন্য একটি ছবি!",
            "🖼️ এই ফটোটি তোমার জন্য!",
            "📷 দেখো কেমন লাগে!"
        ],
        "no_photo_found": [
            "😔 এখন কোনো ছবি নেই!",
            "📭 ফটো খুঁজে পাচ্ছি না!",
            "🕵️‍♂️ ছবি পাওয়া যায়নি!",
            "📂 ফটো ফোল্ডার খালি!"
        ],
        "multiple_photos": [
            "🖼️ একাধিক ছবি পাঠাচ্ছি!",
            "📸 কিছু ফটো তোমার জন্য!",
            "🎞️ ফটো কালেকশন!",
            "📚 ফটো অ্যালবাম!"
        ],
        "facebook_photo": [
            "🔗 ফেসবুক প্রোফাইল থেকে নেওয়া!",
            "📘 ফেসবুক প্রোফাইল ছবি!",
            "👤 প্রোফাইল ফটো!",
            "🌐 অনলাইন থেকে!"
        ]
    },
    
    # Security & Limits
    "security": {
        "max_photos_per_day": 100,
        "max_photos_per_user": 20,
        "max_photo_size_mb": 10,
        "allowed_formats": [".jpg", ".jpeg", ".png", ".gif"],
        "scan_for_malware": False,
        "encrypt_local_photos": False
    },
    
    # Performance
    "performance": {
        "cache_enabled": True,
        "cache_size": 100,
        "preload_popular": True,
        "async_processing": True,
        "compression_enabled": True
    }
}

def get_photo_path(photo_type="master"):
    """Get path for photo type"""
    storage_dir = PHOTO_CONFIG["storage"]["photos_directory"]
    photo_files = PHOTO_CONFIG["photo_files"].get(photo_type, [])
    
    for filename in photo_files:
        path = Path(storage_dir) / filename
        if path.exists():
            return str(path)
    
    # Fallback to default
    default = PHOTO_CONFIG["delivery"]["default_photo"]
    default_path = Path(storage_dir) / default
    
    if default_path.exists():
        return str(default_path)
    
    return None

def get_all_photos():
    """Get list of all available photos"""
    storage_dir = Path(PHOTO_CONFIG["storage"]["photos_directory"])
    photos = []
    
    if not storage_dir.exists():
        return photos
    
    allowed_ext = tuple(PHOTO_CONFIG["security"]["allowed_formats"])
    
    for file in storage_dir.iterdir():
        if file.is_file() and file.suffix.lower() in allowed_ext:
            photos.append(str(file))
    
    return sorted(photos)

def detect_photo_request(text):
    """Detect photo request from text"""
    text_lower = text.lower()
    keywords = PHOTO_CONFIG["request_detection"]["keywords"]
    
    detected_type = None
    confidence = 0
    
    for photo_type, word_list in keywords.items():
        for word in word_list:
            if word in text_lower:
                detected_type = photo_type
                confidence += 0.3
    
    # Check for send/request words
    for send_word in keywords["send_photo"]:
        if send_word in text_lower:
            confidence += 0.2
    
    return detected_type, min(confidence, 1.0)

def create_thumbnail(photo_path, size="200x200"):
    """Create thumbnail for photo"""
    try:
        from PIL import Image
        import os
        
        thumb_dir = Path(PHOTO_CONFIG["storage"]["thumbnails_directory"])
        thumb_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse size
        width, height = map(int, size.split('x'))
        
        # Open image
        with Image.open(photo_path) as img:
            # Resize
            img.thumbnail((width, height))
            
            # Save thumbnail
            thumb_name = f"thumb_{Path(photo_path).stem}.jpg"
            thumb_path = thumb_dir / thumb_name
            img.save(thumb_path, "JPEG", quality=PHOTO_CONFIG["thumbnails"]["thumbnail_quality"])
            
            return str(thumb_path)
            
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None

def validate_photo_file(file_path):
    """Validate photo file"""
    try:
        path = Path(file_path)
        
        # Check if exists
        if not path.exists():
            return False, "File does not exist"
        
        # Check file size
        max_size = PHOTO_CONFIG["security"]["max_photo_size_mb"] * 1024 * 1024
        if path.stat().st_size > max_size:
            return False, f"File too large (max {PHOTO_CONFIG['security']['max_photo_size_mb']}MB)"
        
        # Check file extension
        allowed = PHOTO_CONFIG["security"]["allowed_formats"]
        if path.suffix.lower() not in allowed:
            return False, f"Invalid file format. Allowed: {', '.join(allowed)}"
        
        # Try to open as image
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                img.verify()
        except:
            return False, "Invalid image file"
        
        return True, "Valid"
        
    except Exception as e:
        return False, f"Validation error: {e}"

if __name__ == "__main__":
    print("Photo Configuration Module Loaded")
    print(f"Photo Directory: {PHOTO_CONFIG['storage']['photos_directory']}")
    print(f"Default Photo: {PHOTO_CONFIG['delivery']['default_photo']}")
    
    # Test functions
    test_path = get_photo_path("master")
    if test_path:
        print(f"Master photo found: {test_path}")
    else:
        print("Master photo not found")
    
    all_photos = get_all_photos()
    print(f"Total photos available: {len(all_photos)}")