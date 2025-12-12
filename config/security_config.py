"""
🔒 Security Configuration Module
"""

SECURITY_CONFIG = {
    # Encryption Settings
    "encryption": {
        "enabled": True,
        "algorithm": "AES-256-GCM",
        "key_derivation": "pbkdf2",
        "iterations": 100000,
        "salt_size": 32,
        "encrypt_cookies": True,
        "encrypt_user_data": True,
        "encrypt_logs": False,
        "encrypt_backups": True
    },
    
    # Authentication
    "authentication": {
        "require_admin_auth": True,
        "two_factor_auth": False,
        "session_timeout": 86400,  # seconds (24 hours)
        "max_login_attempts": 5,
        "lockout_duration": 300,  # seconds (5 minutes)
        "password_min_length": 12,
        "require_complex_password": True
    },
    
    # Cookie Security
    "cookies": {
        "secure_cookies": True,
        "http_only": True,
        "same_site": "Lax",
        "max_age": 2592000,  # 30 days
        "encrypt_storage": True,
        "backup_encryption": True,
        "auto_cleanup": True,
        "cleanup_interval": 604800  # 7 days
    },
    
    # Network Security
    "network": {
        "use_https": True,
        "verify_ssl": True,
        "timeout": 30,
        "max_redirects": 5,
        "user_agent_rotation": True,
        "proxy_support": False,
        "ip_whitelist": [],
        "ip_blacklist": []
    },
    
    # Rate Limiting
    "rate_limiting": {
        "enabled": True,
        "messages_per_minute": 15,
        "messages_per_hour": 100,
        "commands_per_minute": 10,
        "api_calls_per_minute": 30,
        "per_user_limits": True,
        "per_command_limits": True,
        "adaptive_limits": True,
        "penalty_duration": 300  # 5 minutes
    },
    
    # Anti-Detection
    "anti_detection": {
        "human_behavior": True,
        "random_delays": True,
        "min_delay": 1.0,
        "max_delay": 5.0,
        "typing_indicator": True,
        "typing_duration": 2.0,
        "activity_patterns": True,
        "rest_periods": True,
        "daily_rest_hours": [3, 6],  # 3 AM to 6 AM
        "vary_response_times": True
    },
    
    # Input Validation
    "input_validation": {
        "sanitize_input": True,
        "max_input_length": 1000,
        "block_sql_injection": True,
        "block_xss": True,
        "block_command_injection": True,
        "validate_urls": True,
        "validate_emails": True,
        "block_malicious_patterns": True
    },
    
    # File Security
    "file_security": {
        "validate_file_types": True,
        "max_file_size_mb": 10,
        "scan_uploads": True,
        "quarantine_suspicious": True,
        "secure_file_storage": True,
        "encrypt_sensitive_files": True,
        "backup_files": True,
        "access_logging": True
    },
    
    # Privacy
    "privacy": {
        "collect_minimal_data": True,
        "anonymous_statistics": False,
        "data_retention_days": 90,
        "auto_delete_old_data": True,
        "encrypt_personal_data": True,
        "user_consent_required": False,
        "gdpr_compliant": False
    },
    
    # Monitoring & Alerts
    "monitoring": {
        "log_security_events": True,
        "alert_on_suspicious": True,
        "alert_on_multiple_failures": True,
        "alert_on_new_device": True,
        "alert_on_admin_actions": True,
        "security_report_interval": 86400,  # Daily
        "auto_block_suspicious": False,
        "notify_admin_on_breach": True
    },
    
    # Backup & Recovery
    "backup": {
        "auto_backup": True,
        "backup_interval": 3600,  # 1 hour
        "max_backups": 30,
        "encrypt_backups": True,
        "offsite_backup": False,
        "test_restore_periodically": True,
        "backup_verification": True
    },
    
    # Emergency Protocols
    "emergency": {
        "kill_switch": True,
        "kill_switch_command": "!emergency_stop",
        "auto_shutdown_on_breach": True,
        "wipe_sensitive_data": False,
        "lockdown_mode": True,
        "lockdown_duration": 3600,  # 1 hour
        "recovery_mode": True
    }
}

def validate_security_settings():
    """Validate all security settings"""
    errors = []
    
    # Check encryption settings
    if SECURITY_CONFIG["encryption"]["enabled"]:
        if SECURITY_CONFIG["encryption"]["iterations"] < 10000:
            errors.append("Encryption iterations too low (min 10000)")
    
    # Check authentication settings
    auth = SECURITY_CONFIG["authentication"]
    if auth["password_min_length"] < 8:
        errors.append("Password minimum length too low (min 8)")
    
    if auth["max_login_attempts"] > 10:
        errors.append("Max login attempts too high")
    
    # Check rate limiting
    rate = SECURITY_CONFIG["rate_limiting"]
    if rate["messages_per_minute"] > 60:
        errors.append("Messages per minute too high")
    
    # Check input validation
    val = SECURITY_CONFIG["input_validation"]
    if val["max_input_length"] > 5000:
        errors.append("Max input length too high")
    
    return len(errors) == 0, errors

def get_security_level():
    """Calculate overall security level"""
    score = 0
    max_score = 100
    
    # Encryption (20 points)
    if SECURITY_CONFIG["encryption"]["enabled"]:
        score += 10
    if SECURITY_CONFIG["encryption"]["encrypt_cookies"]:
        score += 5
    if SECURITY_CONFIG["encryption"]["encrypt_user_data"]:
        score += 5
    
    # Authentication (20 points)
    auth = SECURITY_CONFIG["authentication"]
    if auth["require_admin_auth"]:
        score += 5
    if auth["two_factor_auth"]:
        score += 10
    if auth["require_complex_password"]:
        score += 5
    
    # Rate limiting (15 points)
    rate = SECURITY_CONFIG["rate_limiting"]
    if rate["enabled"]:
        score += 10
    if rate["adaptive_limits"]:
        score += 5
    
    # Anti-detection (15 points)
    anti = SECURITY_CONFIG["anti_detection"]
    if anti["human_behavior"]:
        score += 5
    if anti["random_delays"]:
        score += 5
    if anti["typing_indicator"]:
        score += 5
    
    # Input validation (15 points)
    val = SECURITY_CONFIG["input_validation"]
    if val["sanitize_input"]:
        score += 5
    if val["block_sql_injection"]:
        score += 5
    if val["block_xss"]:
        score += 5
    
    # Monitoring (15 points)
    mon = SECURITY_CONFIG["monitoring"]
    if mon["log_security_events"]:
        score += 5
    if mon["alert_on_suspicious"]:
        score += 5
    if mon["auto_block_suspicious"]:
        score += 5
    
    percentage = (score / max_score) * 100
    
    if percentage >= 80:
        level = "🔐 HIGH"
    elif percentage >= 60:
        level = "🛡️ MEDIUM"
    elif percentage >= 40:
        level = "⚠️ LOW"
    else:
        level = "🔴 VERY LOW"
    
    return level, percentage

def generate_security_report():
    """Generate security report"""
    level, percentage = get_security_level()
    is_valid, errors = validate_security_settings()
    
    report = {
        "security_level": level,
        "security_score": f"{percentage:.1f}%",
        "settings_valid": is_valid,
        "validation_errors": errors,
        "recommendations": []
    }
    
    # Add recommendations
    if percentage < 80:
        report["recommendations"].append("Enable two-factor authentication")
    
    if not SECURITY_CONFIG["encryption"]["enabled"]:
        report["recommendations"].append("Enable encryption")
    
    if not SECURITY_CONFIG["rate_limiting"]["enabled"]:
        report["recommendations"].append("Enable rate limiting")
    
    if not SECURITY_CONFIG["anti_detection"]["human_behavior"]:
        report["recommendations"].append("Enable human behavior simulation")
    
    return report

def check_input_safety(input_text):
    """Check if input text is safe"""
    import re
    
    # SQL Injection patterns
    sql_patterns = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
        r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
        r"((\%27)|(\'))union"
    ]
    
    # XSS patterns
    xss_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"onclick=",
        r"onload=",
        r"onerror=",
        r"<iframe.*?>",
        r"<img.*?src=.*?>"
    ]
    
    # Command injection patterns
    cmd_patterns = [
        r";\s*\w+",
        r"\|\s*\w+",
        r"&&\s*\w+",
        r"`.*?`",
        r"\$\(.*?\)"
    ]
    
    for pattern in sql_patterns + xss_patterns + cmd_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return False, "Malicious pattern detected"
    
    # Check length
    max_len = SECURITY_CONFIG["input_validation"]["max_input_length"]
    if len(input_text) > max_len:
        return False, f"Input too long (max {max_len} characters)"
    
    return True, "Safe"

if __name__ == "__main__":
    print("Security Configuration Module Loaded")
    
    # Generate report
    report = generate_security_report()
    print(f"Security Level: {report['security_level']}")
    print(f"Security Score: {report['security_score']}")
    print(f"Settings Valid: {report['settings_valid']}")
    
    if report["validation_errors"]:
        print("Validation Errors:")
        for error in report["validation_errors"]:
            print(f"  - {error}")
    
    if report["recommendations"]:
        print("Recommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
    
    # Test input safety
    test_inputs = [
        "Hello World!",
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --"
    ]
    
    print("\nInput Safety Tests:")
    for test in test_inputs:
        is_safe, reason = check_input_safety(test)
        print(f"  '{test[:20]}...': {'✅ Safe' if is_safe else f'❌ {reason}'}")