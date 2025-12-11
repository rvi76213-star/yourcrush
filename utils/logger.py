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