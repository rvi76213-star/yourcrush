#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Learning System Configuration
Learning from users, admin, and bot interactions
"""

import os
from typing import Dict, List, Optional, Any

# ==================== LEARNING SOURCES ====================
LEARNING_SOURCES = {
    "from_users": {
        "enabled": True,
        "description": "Learn from user interactions",
        "max_patterns_per_user": 100,
        "pattern_expiry_days": 30,
        "min_confidence": 0.7,
        "learn_topics": True,
        "learn_preferences": True,
        "learn_behavior": True,
        "privacy_respect": True
    },
    
    "from_admin": {
        "enabled": True,
        "description": "Learn from admin commands and responses",
        "admin_id": os.getenv("BOT_ADMIN_ID", "1000123456789"),
        "priority_learning": True,
        "override_user_patterns": True,
        "learn_commands": True,
        "learn_responses": True,
        "learn_style": True,
        "auto_backup": True
    },
    
    "from_bot": {
        "enabled": True,
        "description": "Self-learning from bot interactions",
        "self_improvement": True,
        "success_tracking": True,
        "error_learning": True,
        "pattern_optimization": True,
        "response_refinement": True,
        "learning_rate": 0.1
    }
}

# ==================== PATTERN LEARNING ====================
PATTERN_LEARNING = {
    "conversation_patterns": {
        "enabled": True,
        "extract_intent": True,
        "detect_emotion": True,
        "identify_topics": True,
        "track_context": True,
        "learn_response_style": True,
        "max_pattern_length": 100,
        "min_pattern_occurrence": 3
    },
    
    "user_behavior_patterns": {
        "enabled": True,
        "active_hours": True,
        "response_timing": True,
        "preferred_topics": True,
        "communication_style": True,
        "mood_patterns": True,
        "interaction_frequency": True
    },
    
    "preference_learning": {
        "enabled": True,
        "language_preference": True,
        "response_style": True,
        "topic_interests": True,
        "humor_preference": True,
        "romantic_level": True,
        "formality_preference": True
    }
}

# ==================== MEMORY MANAGEMENT ====================
MEMORY_MANAGEMENT = {
    "short_term_memory": {
        "enabled": True,
        "max_conversations": 50,
        "conversation_expiry": 86400,  # 24 hours
        "context_window": 10,
        "auto_summarize": True
    },
    
    "long_term_memory": {
        "enabled": True,
        "max_users": 1000,
        "max_patterns_per_user": 100,
        "memory_expiry_days": 90,
        "compression_enabled": True,
        "encryption_enabled": True
    },
    
    "user_profiles": {
        "enabled": True,
        "store_demographics": False,
        "store_preferences": True,
        "store_behavior": True,
        "store_relationships": True,
        "privacy_compliant": True
    }
}

# ==================== RESPONSE OPTIMIZATION ====================
RESPONSE_OPTIMIZATION = {
    "personalization": {
        "enabled": True,
        "use_user_name": True,
        "reference_history": True,
        "adapt_to_mood": True,
        "match_communication_style": True,
        "consider_preferences": True
    },
    
    "quality_improvement": {
        "enabled": True,
        "feedback_learning": True,
        "success_rate_tracking": True,
        "a_b_testing": False,
        "auto_correction": True,
        "continuous_refinement": True
    },
    
    "context_awareness": {
        "enabled": True,
        "conversation_context": True,
        "time_context": True,
        "relationship_context": True,
        "topic_context": True,
        "emotional_context": True
    }
}

# ==================== KNOWLEDGE BASE ====================
KNOWLEDGE_BASE = {
    "static_knowledge": {
        "enabled": True,
        "json_responses": True,
        "command_responses": True,
        "factual_information": False,
        "conversation_starters": True,
        "default_responses": True
    },
    
    "dynamic_knowledge": {
        "enabled": True,
        "learned_responses": True,
        "user_patterns": True,
        "conversation_templates": True,
        "contextual_responses": True,
        "personalized_content": True
    },
    
    "external_knowledge": {
        "enabled": False,
        "web_search": False,
        "api_integration": False,
        "database_query": False,
        "file_processing": False
    }
}

# ==================== ANALYTICS & MONITORING ====================
ANALYTICS = {
    "learning_analytics": {
        "enabled": True,
        "track_pattern_learning": True,
        "measure_success_rate": True,
        "monitor_improvement": True,
        "user_engagement": True,
        "response_effectiveness": True
    },
    
    "performance_metrics": {
        "response_time": True,
        "accuracy_rate": True,
        "user_satisfaction": True,
        "conversation_length": True,
        "error_rate": True,
        "learning_speed": True
    },
    
    "reporting": {
        "daily_reports": False,
        "weekly_summaries": False,
        "monthly_analytics": False,
        "real_time_monitoring": True,
        "alert_system": True
    }
}

# ==================== PRIVACY & SECURITY ====================
PRIVACY_SECURITY = {
    "data_protection": {
        "encrypt_user_data": True,
        "anonymize_identifiers": True,
        "secure_storage": True,
        "access_control": True,
        "audit_logging": True
    },
    
    "privacy_compliance": {
        "user_consent": False,
        "data_retention_days": 90,
        "right_to_forget": True,
        "data_export": True,
        "privacy_policy": True
    },
    
    "security_measures": {
        "input_validation": True,
        "output_sanitization": True,
        "rate_limiting": True,
        "abuse_detection": True,
        "emergency_shutdown": True
    }
}

# ==================== BACKUP & RECOVERY ====================
BACKUP_RECOVERY = {
    "auto_backup": {
        "enabled": True,
        "interval": 86400,  # 24 hours
        "max_backups": 30,
        "compression": True,
        "encryption": True,
        "cloud_backup": False
    },
    
    "recovery_system": {
        "enabled": True,
        "auto_recovery": True,
        "point_in_time": True,
        "data_integrity": True,
        "test_restores": False
    },
    
    "version_control": {
        "enabled": True,
        "version_history": True,
        "change_tracking": True,
        "rollback_capability": True,
        "migration_tools": True
    }
}

# ==================== EXPORT FUNCTIONS ====================
def get_learning_config() -> Dict:
    """Get complete learning configuration"""
    return {
        "learning_sources": LEARNING_SOURCES,
        "pattern_learning": PATTERN_LEARNING,
        "memory_management": MEMORY_MANAGEMENT,
        "response_optimization": RESPONSE_OPTIMIZATION,
        "knowledge_base": KNOWLEDGE_BASE,
        "analytics": ANALYTICS,
        "privacy_security": PRIVACY_SECURITY,
        "backup_recovery": BACKUP_RECOVERY
    }

def get_active_learning_sources() -> List[str]:
    """Get list of active learning sources"""
    return [name for name, config in LEARNING_SOURCES.items() if config["enabled"]]

def validate_learning_config() -> bool:
    """Validate learning configuration"""
    errors = []
    
    # Check memory limits
    if MEMORY_MANAGEMENT["short_term_memory"]["max_conversations"] < 1:
        errors.append("Short term memory must store at least 1 conversation")
    
    if MEMORY_MANAGEMENT["long_term_memory"]["max_users"] < 1:
        errors.append("Long term memory must support at least 1 user")
    
    # Check learning rates
    if LEARNING_SOURCES["from_bot"]["learning_rate"] <= 0 or LEARNING_SOURCES["from_bot"]["learning_rate"] > 1:
        errors.append("Bot learning rate must be between 0 and 1")
    
    # Check privacy settings
    if PRIVACY_SECURITY["privacy_compliance"]["data_retention_days"] < 1:
        errors.append("Data retention days must be at least 1")
    
    if errors:
        print("❌ Learning configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Learning configuration validated successfully")
    return True

def save_learning_config():
    """Save learning configuration to file"""
    import json
    config = get_learning_config()
    
    with open("config/learning_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Learning configuration saved to config/learning_config.json")

def load_learning_config() -> Dict:
    """Load learning configuration from file"""
    try:
        with open("config/learning_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Learning config file not found, using default configuration")
        return get_learning_config()

# ==================== INITIALIZATION ====================
if __name__ == "__main__":
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Create default config file if it doesn't exist
    if not os.path.exists("config/learning_config.json"):
        save_learning_config()
        print("📁 Created default learning_config.json file")
    
    # Validate configuration
    validate_learning_config()