"""
✓ Validator Module for input validation and sanitization
"""

import re
import json
from urllib.parse import urlparse

class Validator:
    """Input validator class"""
    
    @staticmethod
    def validate_facebook_url(url):
        """Validate Facebook URL"""
        facebook_patterns = [
            r'https?://(www\.)?facebook\.com/.*',
            r'https?://(www\.)?fb\.com/.*',
            r'https?://(www\.)?m\.facebook\.com/.*',
            r'https?://(www\.)?facebook\.com/share/.*'
        ]
        
        for pattern in facebook_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (Bangladeshi)"""
        # Bangladeshi phone number patterns
        patterns = [
            r'^01[3-9]\d{8}$',  # 01XXXXXXXXX
            r'^\+8801[3-9]\d{8}$',  # +8801XXXXXXXXX
            r'^8801[3-9]\d{8}$'  # 8801XXXXXXXXX
        ]
        
        for pattern in patterns:
            if re.match(pattern, phone):
                return True
        return False
    
    @staticmethod
    def sanitize_input(text, max_length=1000):
        """Sanitize user input"""
        if not text:
            return ""
        
        # Trim and limit length
        text = text.strip()
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remove dangerous characters
        dangerous = ['<', '>', '&', '"', "'", ';', '|', '`', '$', '(', ')', '{', '}']
        for char in dangerous:
            text = text.replace(char, '')
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @staticmethod
    def validate_json(data):
        """Validate JSON data"""
        try:
            if isinstance(data, str):
                json.loads(data)
            else:
                json.dumps(data)
            return True
        except:
            return False
    
    @staticmethod
    def validate_command_syntax(command):
        """Validate command syntax"""
        # Command patterns
        patterns = {
            'prefix': r'^\.\w+',
            'admin': r'^!\w+',
            'nickname': r'^(Bot|bow|Jan|Sona|Baby|Etc)$'
        }
        
        for cmd_type, pattern in patterns.items():
            if re.match(pattern, command, re.IGNORECASE):
                return cmd_type
        return None
    
    @staticmethod
    def validate_user_id(user_id):
        """Validate Facebook user ID"""
        # Facebook IDs are usually numeric and 10-16 digits
        if not user_id:
            return False
        
        # Remove any non-numeric characters
        clean_id = re.sub(r'\D', '', str(user_id))
        
        # Check if it's a reasonable Facebook ID
        if len(clean_id) < 10 or len(clean_id) > 16:
            return False
        
        # Check if it's numeric
        return clean_id.isdigit()
    
    @staticmethod
    def validate_file_path(file_path, allowed_extensions=None):
        """Validate file path"""
        import os
        from pathlib import Path
        
        if not file_path:
            return False, "Empty file path"
        
        try:
            path = Path(file_path)
            
            # Check if path exists
            if not path.exists():
                return False, "File does not exist"
            
            # Check if it's a file
            if not path.is_file():
                return False, "Not a file"
            
            # Check file size
            max_size_mb = 10
            if path.stat().st_size > max_size_mb * 1024 * 1024:
                return False, f"File too large (max {max_size_mb}MB)"
            
            # Check extension if specified
            if allowed_extensions:
                if path.suffix.lower() not in allowed_extensions:
                    return False, f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    @staticmethod
    def validate_image_file(file_path):
        """Validate image file"""
        try:
            from PIL import Image
            allowed_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            
            is_valid, message = Validator.validate_file_path(file_path, allowed_ext)
            if not is_valid:
                return False, message
            
            # Try to open as image
            try:
                with Image.open(file_path) as img:
                    img.verify()
                return True, "Valid image"
            except Exception as e:
                return False, f"Invalid image: {e}"
                
        except ImportError:
            # PIL not available, do basic validation
            return Validator.validate_file_path(file_path, ['.jpg', '.jpeg', '.png', '.gif'])
    
    @staticmethod
    def validate_cookie_data(cookies):
        """Validate cookie data"""
        if not cookies:
            return False, "No cookies provided"
        
        # Check if it's a list
        if not isinstance(cookies, list):
            return False, "Cookies should be a list"
        
        # Check each cookie
        required_fields = ['name', 'value', 'domain']
        for i, cookie in enumerate(cookies):
            if not isinstance(cookie, dict):
                return False, f"Cookie {i} is not a dictionary"
            
            for field in required_fields:
                if field not in cookie:
                    return False, f"Cookie {i} missing '{field}' field"
            
            # Check domain
            if 'facebook.com' not in cookie['domain']:
                return False, f"Cookie {i} has invalid domain: {cookie['domain']}"
        
        return True, "Valid cookie data"
    
    @staticmethod
    def validate_config(config_dict):
        """Validate configuration dictionary"""
        required_sections = ['bot', 'facebook', 'commands', 'photos']
        
        for section in required_sections:
            if section not in config_dict:
                return False, f"Missing section: {section}"
        
        # Bot section validation
        bot_fields = ['name', 'author', 'version']
        for field in bot_fields:
            if field not in config_dict['bot']:
                return False, f"bot section missing '{field}'"
        
        # Facebook section validation
        if 'cookie_file' not in config_dict['facebook']:
            return False, "facebook section missing 'cookie_file'"
        
        return True, "Valid configuration"

if __name__ == "__main__":
    print("Validator Module Loaded")
    
    # Test validation functions
    validator = Validator()
    
    test_cases = [
        ("Facebook URL", "https://www.facebook.com/share/17gEJAipcr/", validator.validate_facebook_url),
        ("Email", "ranaeditz333@gmail.com", validator.validate_email),
        ("Phone", "01847634486", validator.validate_phone),
        ("User ID", "1000123456789", validator.validate_user_id),
        ("Command", ".murgi", validator.validate_command_syntax),
        ("JSON", '{"key": "value"}', validator.validate_json)
    ]
    
    print("\nValidation Tests:")
    for test_name, test_value, test_func in test_cases:
        try:
            result = test_func(test_value)
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status} -> {test_value}")
        except Exception as e:
            print(f"  {test_name}: ❌ ERROR -> {e}")