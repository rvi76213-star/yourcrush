#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Bot Setup Script
Setup and configure YOUR CRUSH AI BOT
"""

import os
import sys
import json
import shutil
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger, log_success, log_error, log_warning, log_info
from utils.file_handler import FileHandler


class BotSetup:
    """⚡ Bot Setup and Configuration"""
    
    def __init__(self):
        self.logger = setup_logger("setup", "data/logs/setup.log")
        self.file_handler = FileHandler()
        
        # Setup steps
        self.steps = [
            self.check_requirements,
            self.create_directories,
            self.create_config_files,
            self.setup_photos,
            self.setup_commands,
            self.setup_learning,
            self.setup_logging,
            self.test_setup
        ]
    
    def check_requirements(self) -> bool:
        """Check system requirements"""
        log_info("🔧 Checking system requirements...")
        
        requirements = [
            ("Python 3.8+", self._check_python_version),
            ("Required directories", self._check_directories),
            ("Dependencies", self._check_dependencies),
            ("Write permissions", self._check_permissions)
        ]
        
        all_ok = True
        for req_name, check_func in requirements:
            try:
                if check_func():
                    log_success(f"✅ {req_name}: OK")
                else:
                    log_warning(f"⚠️ {req_name}: FAILED")
                    all_ok = False
            except Exception as e:
                log_error(f"❌ {req_name}: ERROR - {e}")
                all_ok = False
        
        return all_ok
    
    def _check_python_version(self) -> bool:
        """Check Python version"""
        import platform
        version = platform.python_version_tuple()
        return int(version[0]) >= 3 and int(version[1]) >= 8
    
    def _check_directories(self) -> bool:
        """Check if required directories exist"""
        base_dir = os.getcwd()
        required = [
            base_dir,
            os.path.join(base_dir, "bot_core"),
            os.path.join(base_dir, "utils")
        ]
        
        for directory in required:
            if not os.path.exists(directory):
                log_warning(f"Directory not found: {directory}")
                return False
        
        return True
    
    def _check_dependencies(self) -> bool:
        """Check if required packages are installed"""
        required_packages = [
            "requests",
            "browser_cookie3",
            "cryptography",
            "pillow",
            "emoji"
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing.append(package)
        
        if missing:
            log_warning(f"Missing packages: {', '.join(missing)}")
            log_info("Run: pip install -r requirements.txt")
            return False
        
        return True
    
    def _check_permissions(self) -> bool:
        """Check write permissions"""
        test_file = "data/test_permissions.tmp"
        try:
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            log_warning("No write permission in data/ directory")
            return False
    
    def create_directories(self) -> bool:
        """Create required directories"""
        log_info("📁 Creating directories...")
        
        directories = [
            "data",
            "data/cookies",
            "data/photos",
            "data/photos/thumbnails",
            "data/commands",
            "data/commands/prefix",
            "data/commands/admin",
            "data/commands/nicknames",
            "data/learning",
            "data/json_responses",
            "data/ai_integration",
            "data/users",
            "data/groups",
            "data/logs",
            "data/backup",
            "config",
            "utils",
            "scripts",
            "tests",
            "docs",
            "templates",
            "examples",
            "temp",
            "temp/cache",
            "temp/downloads",
            "temp/uploads",
            "external"
        ]
        
        created_count = 0
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                created_count += 1
                self.logger.debug(f"Created directory: {directory}")
            except Exception as e:
                log_error(f"Failed to create {directory}: {e}")
                return False
        
        log_success(f"✅ Created {created_count} directories")
        return True
    
    def create_config_files(self) -> bool:
        """Create configuration files"""
        log_info("⚙️ Creating configuration files...")
        
        config_files = [
            ("config.json", self._create_main_config),
            ("bot_identity.json", self._create_bot_identity),
            (".env.example", self._create_env_example),
            ("requirements.txt", self._create_requirements),
            ("README.md", self._create_readme),
            ("run.py", self._create_run_script)
        ]
        
        created_count = 0
        for filename, create_func in config_files:
            try:
                if create_func():
                    created_count += 1
                    self.logger.debug(f"Created file: {filename}")
                else:
                    log_warning(f"Failed to create: {filename}")
            except Exception as e:
                log_error(f"Error creating {filename}: {e}")
        
        log_success(f"✅ Created {created_count} configuration files")
        return created_count > 0
    
    def _create_main_config(self) -> bool:
        """Create main config.json file"""
        config = {
            "bot": {
                "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
                "author": "MAR PD",
                "version": "1.0.0",
                "status": "active",
                "personality": "romantic"
            },
            "facebook": {
                "login_method": "cookie",
                "cookie_file": "data/cookies/master_cookies.json",
                "profile_url": "https://www.facebook.com/share/17gEJAipcr/",
                "rate_limit": {
                    "messages_per_minute": 10,
                    "messages_per_hour": 100
                }
            },
            "commands": {
                "prefix": ".",
                "admin_prefix": "!",
                "enabled_commands": ["murgi", "love", "pick", "dio", "info", "uid"],
                "admin_commands": ["add", "delete", "kick", "out", "start", "stop"]
            },
            "photos": {
                "local_photos": ["master.jpg", "photo.jpg", "own.jpg"],
                "default_photo": "master.jpg",
                "facebook_fetch": True,
                "cache_duration": 3600
            },
            "learning": {
                "enabled": True,
                "learn_from_users": True,
                "learn_from_admin": True,
                "learn_from_bot": True,
                "max_memory": 1000
            },
            "security": {
                "encrypt_cookies": True,
                "encrypt_user_data": True,
                "proxy_rotation": False,
                "human_behavior": True
            },
            "logging": {
                "level": "INFO",
                "file": "data/logs/bot_activity.log",
                "max_size_mb": 10,
                "backup_count": 5
            }
        }
        
        return self.file_handler.write_json("config.json", config)
    
    def _create_bot_identity(self) -> bool:
        """Create bot_identity.json file"""
        identity = {
            "identity": {
                "bot_name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
                "author": "MAR PD",
                "social_name": "MASTER 🪓",
                "real_name": "RANA",
                "age": 20,
                "dream": "DEVELOPER",
                "relationship": "SINGLE",
                "job": "SECURITY",
                "work": "EXPERIMENT",
                "experience": [
                    "VIDEO EDIT",
                    "PHOTO EDIT", 
                    "MOBILE TECHNICIAN",
                    "BIULING",
                    "SPAMMER"
                ],
                "training": "CYBER SECURITY",
                "study": "SSC BACH 2022",
                "from": "FARIDPUR DHAKA",
                "email": "ranaeditz333@gmail.com",
                "telegram_bot": "@black_lovers1_bot",
                "telegram_profile": "@rana_editz_00",
                "telegram_channel": "https://t.me/master_account_remover_channel",
                "phone": "01847634486",
                "website": "Under Construction"
            },
            "personality": {
                "romantic_level": "high",
                "friendliness": "high",
                "helpfulness": "high",
                "humor": "medium",
                "seriousness": "low",
                "response_style": "flirty",
                "language": "banglish"
            }
        }
        
        return self.file_handler.write_json("bot_identity.json", identity)
    
    def _create_env_example(self) -> bool:
        """Create .env.example file"""
        env_content = """# Facebook Configuration
FACEBOOK_EMAIL=your_email@gmail.com
FACEBOOK_PASSWORD=your_password
FACEBOOK_USER_ID=1000123456789

# Bot Configuration
BOT_NAME="YOUR CRUSH ⟵o_0"
BOT_ADMIN_ID=1000123456789
BOT_COMMAND_PREFIX=.
BOT_RESPONSE_DELAY=2

# Cookie Configuration
COOKIE_PATH=data/cookies/master_cookies.json
COOKIE_ENCRYPTION_KEY=your_encryption_key_here

# Photo Configuration
PHOTO_FOLDER=data/photos/
DEFAULT_PHOTO=master.jpg
FACEBOOK_PROFILE_URL=https://www.facebook.com/share/17gEJAipcr/

# AI Configuration (Optional)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
DEEPSEEK_API_KEY=sk-...

# Security Configuration
ENCRYPTION_KEY=your_encryption_key
PROXY_ENABLED=false
RATE_LIMIT_PER_MINUTE=10

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=data/logs/bot_activity.log

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24

# Server Configuration
HOST=127.0.0.1
PORT=8080
DEBUG_MODE=false
"""
        
        return self.file_handler.write_text(".env.example", env_content)
    
    def _create_requirements(self) -> bool:
        """Create requirements.txt file"""
        requirements = """# Core Dependencies
requests>=2.28.0
requests-toolbelt>=0.10.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
cryptography>=40.0.0
browser-cookie3>=0.19.0
python-dotenv>=1.0.0
PyYAML>=6.0
colorama>=0.4.6
tqdm>=4.65.0

# Asynchronous
aiohttp>=3.8.0
asyncio>=3.4.3
websockets>=11.0.0

# AI & NLP
openai>=0.27.0
transformers>=4.28.0
torch>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.2.0
nltk>=3.8.0
gensim>=4.3.0

# Image Processing
Pillow>=9.5.0
opencv-python>=4.7.0
imageio>=2.31.0

# Utilities
pyfiglet>=0.8.post1
rich>=13.0.0
loguru>=0.7.0
schedule>=1.2.0
APScheduler>=3.10.0
psutil>=5.9.0
humanize>=4.6.0
python-dateutil>=2.8.0

# Facebook Specific
facebook-scraper>=0.3.0
fbchat>=2.0.0

# Security
pycryptodome>=3.17.0
hashlib
secrets

# Development
pytest>=7.3.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
"""
        
        return self.file_handler.write_text("requirements.txt", requirements)
    
    def _create_readme(self) -> bool:
        """Create README.md file"""
        readme = """# 🤖 YOUR CRUSH AI BOT

A sophisticated Facebook Messenger bot with AI capabilities, photo delivery system, and command processing.

## 🚀 Quick Start

```bash
# 1. Install Python 3.8+
# 2. Clone this repository
# 3. Run setup:
python scripts/setup_bot.py

# 4. Install dependencies:
pip install -r requirements.txt

# 5. Configure your bot:
#    - Add photos to data/photos/
#    - Update config.json
#    - Copy .env.example to .env and fill your details

# 6. Extract Facebook cookies:
python scripts/extract_cookies.py

# 7. Run the bot:
python run.py