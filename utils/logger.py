#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Logging System
Handles all logging operations
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = self.COLORS[record.levelname] + record.levelname + Style.RESET_ALL
            record.msg = self.COLORS[record.levelname.replace(Style.RESET_ALL, '')] + str(record.msg) + Style.RESET_ALL
        
        return super().format(record)


def setup_logger(name: str, log_file: str = None, level: str = "INFO") -> logging.Logger:
    """
    Setup a logger with console and file handlers
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
    
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Set level
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    console_format = ColoredFormatter(
        '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if log_file provided)
    if log_file:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    return logger


def log_bot_start():
    """Log bot startup banner"""
    banner = f"""
    {'='*60}
    🤖 YOUR CRUSH AI BOT - STARTING
    {'='*60}
    Author: MAR PD (RANA)
    Version: 1.0.0
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    {'='*60}
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)


def log_bot_stop():
    """Log bot shutdown banner"""
    banner = f"""
    {'='*60}
    🤖 YOUR CRUSH AI BOT - STOPPING
    {'='*60}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    {'='*60}
    """
    print(Fore.YELLOW + banner + Style.RESET_ALL)


def log_error(error_msg: str, exception: Exception = None):
    """Log error with details"""
    logger = logging.getLogger("error_logger")
    
    error_details = f"ERROR: {error_msg}"
    if exception:
        error_details += f"\nException: {type(exception).__name__}: {str(exception)}"
        import traceback
        error_details += f"\nTraceback:\n{traceback.format_exc()}"
    
    logger.error(error_details)
    
    # Also print to console in red
    print(Fore.RED + f"[ERROR] {error_msg}" + Style.RESET_ALL)
    if exception:
        print(Fore.RED + f"[EXCEPTION] {type(exception).__name__}: {str(exception)}" + Style.RESET_ALL)


def log_success(message: str):
    """Log success message"""
    logger = logging.getLogger("success_logger")
    logger.info(message)
    print(Fore.GREEN + f"[SUCCESS] {message}" + Style.RESET_ALL)


def log_warning(message: str):
    """Log warning message"""
    logger = logging.getLogger("warning_logger")
    logger.warning(message)
    print(Fore.YELLOW + f"[WARNING] {message}" + Style.RESET_ALL)


def log_info(message: str):
    """Log info message"""
    logger = logging.getLogger("info_logger")
    logger.info(message)
    print(Fore.CYAN + f"[INFO] {message}" + Style.RESET_ALL)


def log_debug(message: str):
    """Log debug message"""
    logger = logging.getLogger("debug_logger")
    logger.debug(message)
    print(Fore.MAGENTA + f"[DEBUG] {message}" + Style.RESET_ALL)


def get_log_file_stats(log_file: str) -> dict:
    """
    Get statistics about log file
    
    Args:
        log_file: Path to log file
    
    Returns:
        Dictionary with log statistics
    """
    stats = {
        "exists": False,
        "size_bytes": 0,
        "size_mb": 0,
        "last_modified": None,
        "line_count": 0
    }
    
    try:
        if os.path.exists(log_file):
            stats["exists"] = True
            stats["size_bytes"] = os.path.getsize(log_file)
            stats["size_mb"] = stats["size_bytes"] / (1024 * 1024)
            stats["last_modified"] = datetime.fromtimestamp(
                os.path.getmtime(log_file)
            ).strftime('%Y-%m-%d %H:%M:%S')
            
            # Count lines
            with open(log_file, 'r', encoding='utf-8') as f:
                stats["line_count"] = sum(1 for _ in f)
    
    except Exception as e:
        stats["error"] = str(e)
    
    return stats


def clean_old_logs(log_dir: str, days_to_keep: int = 7):
    """
    Clean log files older than specified days
    
    Args:
        log_dir: Directory containing log files
        days_to_keep: Number of days to keep logs
    """
    import glob
    import time
    
    try:
        if not os.path.exists(log_dir):
            return
        
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
        
        log_files = glob.glob(os.path.join(log_dir, "*.log"))
        log_files.extend(glob.glob(os.path.join(log_dir, "*.log.*")))  # Rotated logs
        
        deleted_count = 0
        for log_file in log_files:
            try:
                file_time = os.path.getmtime(log_file)
                if file_time < cutoff_time:
                    os.remove(log_file)
                    deleted_count += 1
                    log_info(f"Deleted old log file: {log_file}")
            except Exception as e:
                log_warning(f"Could not delete {log_file}: {e}")
        
        log_success(f"Cleaned {deleted_count} old log files")
        
    except Exception as e:
        log_error(f"Error cleaning old logs: {e}")


def setup_global_logging(level: str = "INFO"):
    """
    Setup global logging configuration
    
    Args:
        level: Global logging level
    """
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler for root
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = ColoredFormatter(
        '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    
    log_info(f"Global logging configured with level: {level}")


# Create default loggers for quick use
bot_logger = setup_logger("bot", "data/logs/bot_activity.log")
error_logger = setup_logger("errors", "data/logs/error_log.log")
command_logger = setup_logger("commands", "data/logs/command_log.log")
learning_logger = setup_logger("learning", "data/logs/learning_log.log")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Logger Module - Advanced logging system
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class Logger:
    """Advanced logging system for YOUR CRUSH AI BOT"""
    
    def __init__(self, name: str, log_dir: str = "data/logs", 
                 level: str = "INFO", max_size_mb: int = 10, 
                 backup_count: int = 5):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_size_mb: Maximum log file size in MB
            backup_count: Number of backup files to keep
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.max_size_mb = max_size_mb
        self.backup_count = backup_count
        
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.propagate = False
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self.setup_handlers()
        
        # Log initialization
        self.info(f"Logger initialized: {name} (level: {level})")
    
    def setup_handlers(self):
        """Setup logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (rotating by size)
        log_file = self.log_dir / f"{self.name}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_size_mb * 1024 * 1024,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler (errors only)
        error_file = self.log_dir / f"{self.name}_error.log"
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=self.max_size_mb * 1024 * 1024,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, extra: Optional[Dict] = None):
        """Log debug message"""
        self._log(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict] = None):
        """Log info message"""
        self._log(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict] = None):
        """Log warning message"""
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict] = None):
        """Log error message"""
        self._log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict] = None):
        """Log critical message"""
        self._log(logging.CRITICAL, message, extra)
    
    def _log(self, level: int, message: str, extra: Optional[Dict] = None):
        """Internal logging method"""
        if extra:
            self.logger.log(level, message, extra=extra)
        else:
            self.logger.log(level, message)
    
    def log_command(self, user_id: str, command: str, success: bool = True, 
                   details: Optional[Dict] = None):
        """Log command execution"""
        extra = {
            'user_id': user_id,
            'command': command,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            extra.update(details)
        
        level = logging.INFO if success else logging.WARNING
        message = f"Command: {command} by {user_id} - {'Success' if success else 'Failed'}"
        
        self._log(level, message, {'extra': extra})
    
    def log_message(self, user_id: str, message: str, chat_type: str = "private"):
        """Log message receipt"""
        extra = {
            'user_id': user_id,
            'message_preview': message[:100],
            'message_length': len(message),
            'chat_type': chat_type,
            'timestamp': datetime.now().isoformat()
        }
        
        self.info(f"Message from {user_id} ({chat_type}): {message[:50]}...", 
                 {'extra': extra})
    
    def log_photo_request(self, user_id: str, photo_type: str, success: bool = True):
        """Log photo request"""
        extra = {
            'user_id': user_id,
            'photo_type': photo_type,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        level = logging.INFO if success else logging.WARNING
        message = f"Photo request: {photo_type} by {user_id} - {'Success' if success else 'Failed'}"
        
        self._log(level, message, {'extra': extra})
    
    def log_learning(self, action: str, details: Dict):
        """Log learning activity"""
        extra = {
            'action': action,
            'timestamp': datetime.now().isoformat(),
            **details
        }
        
        self.info(f"Learning: {action}", {'extra': extra})
    
    def log_security(self, event: str, severity: str = "medium", details: Optional[Dict] = None):
        """Log security event"""
        severity_levels = {
            'low': logging.INFO,
            'medium': logging.WARNING,
            'high': logging.ERROR,
            'critical': logging.CRITICAL
        }
        
        level = severity_levels.get(severity.lower(), logging.WARNING)
        
        extra = {
            'event': event,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            extra.update(details)
        
        self._log(level, f"Security: {event} ({severity})", {'extra': extra})
    
    def log_performance(self, operation: str, duration_ms: float, details: Optional[Dict] = None):
        """Log performance metrics"""
        extra = {
            'operation': operation,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            extra.update(details)
        
        # Log as INFO for normal operations, WARNING for slow operations
        level = logging.WARNING if duration_ms > 1000 else logging.INFO
        message = f"Performance: {operation} took {duration_ms:.2f}ms"
        
        self._log(level, message, {'extra': extra})
    
    def get_log_file_path(self, log_type: str = "main") -> Path:
        """Get path to log file"""
        if log_type == "main":
            return self.log_dir / f"{self.name}.log"
        elif log_type == "error":
            return self.log_dir / f"{self.name}_error.log"
        else:
            return self.log_dir / f"{self.name}_{log_type}.log"
    
    def get_recent_logs(self, lines: int = 100, log_type: str = "main") -> list:
        """Get recent log entries"""
        log_file = self.get_log_file_path(log_type)
        
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.error(f"Error reading log file: {e}")
            return []
    
    def analyze_logs(self, hours: int = 24) -> Dict:
        """Analyze logs from specified time period"""
        cutoff_time = time.time() - (hours * 3600)
        cutoff_datetime = datetime.fromtimestamp(cutoff_time)
        
        stats = {
            'total_entries': 0,
            'by_level': {},
            'by_hour': {},
            'errors': 0,
            'warnings': 0,
            'unique_users': set(),
            'commands_executed': 0,
            'photo_requests': 0
        }
        
        log_files = [
            self.get_log_file_path("main"),
            self.get_log_file_path("error")
        ]
        
        for log_file in log_files:
            if not log_file.exists():
                continue
            
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        # Parse log line
                        try:
                            # Extract timestamp
                            parts = line.split(' - ', 3)
                            if len(parts) >= 3:
                                timestamp_str = parts[0]
                                log_datetime = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                                
                                # Check if within time period
                                if log_datetime >= cutoff_datetime:
                                    stats['total_entries'] += 1
                                    
                                    # Count by level
                                    level = parts[2]
                                    stats['by_level'][level] = stats['by_level'].get(level, 0) + 1
                                    
                                    # Count by hour
                                    hour = log_datetime.strftime('%H:00')
                                    stats['by_hour'][hour] = stats['by_hour'].get(hour, 0) + 1
                                    
                                    # Count errors and warnings
                                    if 'ERROR' in level:
                                        stats['errors'] += 1
                                    elif 'WARNING' in level:
                                        stats['warnings'] += 1
                                    
                                    # Extract additional info from message
                                    message = parts[3] if len(parts) > 3 else ""
                                    
                                    if 'user_id' in message:
                                        # Extract user ID
                                        import re
                                        user_match = re.search(r'user_id[\'": ]+([\w-]+)', message)
                                        if user_match:
                                            stats['unique_users'].add(user_match.group(1))
                                    
                                    if 'Command:' in message:
                                        stats['commands_executed'] += 1
                                    
                                    if 'Photo request:' in message:
                                        stats['photo_requests'] += 1
                        
                        except Exception as e:
                            # Skip lines that can't be parsed
                            continue
            
            except Exception as e:
                self.error(f"Error analyzing log file {log_file}: {e}")
        
        # Convert set to count
        stats['unique_users_count'] = len(stats['unique_users'])
        del stats['unique_users']
        
        return stats
    
    def cleanup_old_logs(self, days: int = 30):
        """Clean up log files older than specified days"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        for log_file in self.log_dir.glob("*.log*"):
            try:
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    self.info(f"Cleaned up old log file: {log_file.name}")
            except Exception as e:
                self.error(f"Error cleaning up log file {log_file}: {e}")
    
    def export_logs(self, output_file: str, hours: int = 24, 
                   include_types: list = None):
        """
        Export logs to JSON file
        
        Args:
            output_file: Output JSON file path
            hours: Number of hours to include
            include_types: List of log types to include
        """
        if include_types is None:
            include_types = ['main', 'error']
        
        cutoff_time = time.time() - (hours * 3600)
        cutoff_datetime = datetime.fromtimestamp(cutoff_time)
        
        exported_logs = []
        
        for log_type in include_types:
            log_file = self.get_log_file_path(log_type)
            
            if not log_file.exists():
                continue
            
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            parts = line.split(' - ', 3)
                            if len(parts) >= 4:
                                timestamp_str = parts[0]
                                log_datetime = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                                
                                if log_datetime >= cutoff_datetime:
                                    log_entry = {
                                        'timestamp': timestamp_str,
                                        'logger': parts[1],
                                        'level': parts[2],
                                        'message': parts[3].strip(),
                                        'type': log_type,
                                        'iso_timestamp': log_datetime.isoformat()
                                    }
                                    exported_logs.append(log_entry)
                        
                        except Exception as e:
                            continue
            
            except Exception as e:
                self.error(f"Error exporting log file {log_file}: {e}")
        
        # Sort by timestamp
        exported_logs.sort(key=lambda x: x['iso_timestamp'])
        
        # Export to JSON
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'exported_at': datetime.now().isoformat(),
                    'hours_covered': hours,
                    'total_entries': len(exported_logs),
                    'logs': exported_logs
                }, f, indent=2, ensure_ascii=False)
            
            self.info(f"Exported {len(exported_logs)} log entries to {output_file}")
            
        except Exception as e:
            self.error(f"Error exporting logs to {output_file}: {e}")
    
    def set_level(self, level: str):
        """Set logging level"""
        new_level = getattr(logging, level.upper(), None)
        if new_level:
            self.level = new_level
            self.logger.setLevel(new_level)
            for handler in self.logger.handlers:
                handler.setLevel(new_level)
            self.info(f"Logging level changed to {level}")

def setup_logger(name: str, log_file: str = None, level: str = "INFO") -> Logger:
    """
    Setup and return a logger instance
    
    Args:
        name: Logger name
        log_file: Custom log file path (optional)
        level: Logging level
    
    Returns:
        Logger instance
    """
    if log_file:
        log_dir = os.path.dirname(log_file)
        logger_name = os.path.basename(log_file).replace('.log', '')
    else:
        log_dir = "data/logs"
        logger_name = name
    
    return Logger(logger_name, log_dir, level)

if __name__ == "__main__":
    print("Logger Module Loaded")
    
    # Test the logger
    print("\n🧪 Testing Logger:")
    print("="*50)
    
    try:
        # Create test logger
        test_logger = Logger("test_logger", "test_logs", "DEBUG")
        
        # Test different log levels
        print("\n📝 Testing log levels:")
        test_logger.debug("This is a debug message")
        test_logger.info("This is an info message")
        test_logger.warning("This is a warning message")
        test_logger.error("This is an error message")
        test_logger.critical("This is a critical message")
        
        # Test specialized logging
        print("\n🎯 Testing specialized logging:")
        test_logger.log_command("user_123", ".murgi", success=True)
        test_logger.log_message("user_456", "হ্যালো, কেমন আছো?", "private")
        test_logger.log_photo_request("user_789", "personal", success=True)
        test_logger.log_learning("pattern_learned", {"pattern": "greeting", "confidence": 0.8})
        test_logger.log_security("multiple_login_attempts", "medium", {"ip": "192.168.1.1"})
        test_logger.log_performance("message_processing", 125.5, {"message_length": 150})
        
        # Test log analysis
        print("\n📊 Testing log analysis:")
        stats = test_logger.analyze_logs(1)  # Last hour
        print(f"Log stats: {stats}")
        
        # Test log export
        print("\n📤 Testing log export:")
        test_logger.export_logs("test_export.json", hours=1)
        print("Logs exported to test_export.json")
        
        # Test recent logs
        print("\n📄 Testing recent logs:")
        recent = test_logger.get_recent_logs(5)
        print(f"Recent logs ({len(recent)} lines):")
        for line in recent:
            print(f"  {line.strip()}")
        
        # Test cleanup
        print("\n🧹 Testing cleanup:")
        test_logger.cleanup_old_logs(0)  # Clean all old logs for testing
        print("Cleanup completed")
        
        # Cleanup test directory
        import shutil
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
            print("Cleaned up test_logs directory")
        
        if os.path.exists("test_export.json"):
            os.remove("test_export.json")
            print("Cleaned up test_export.json")
        
        print("\n✅ Logger tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()