#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Configuration
AI model settings and configuration
"""

import os
from typing import Dict, List, Optional, Any

# ==================== AI PROVIDER CONFIGURATION ====================
AI_PROVIDERS = {
    "local": {
        "enabled": True,
        "priority": 1,
        "description": "Local AI responses using JSON patterns",
        "model": "json_patterns",
        "max_response_length": 500,
        "response_delay": 2,
        "learning_enabled": True
    },
    "openai": {
        "enabled": False,
        "priority": 2,
        "description": "OpenAI GPT models",
        "model": "gpt-3.5-turbo",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "max_tokens": 150,
        "temperature": 0.7,
        "organization": os.getenv("OPENAI_ORG", ""),
        "rate_limit": {
            "requests_per_minute": 20,
            "tokens_per_minute": 40000
        }
    },
    "gemini": {
        "enabled": False,
        "priority": 3,
        "description": "Google Gemini AI",
        "model": "gemini-pro",
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "max_output_tokens": 150,
        "temperature": 0.7,
        "safety_settings": {
            "harassment": "block_none",
            "hate_speech": "block_none",
            "sexually_explicit": "block_none",
            "dangerous_content": "block_none"
        }
    },
    "deepseek": {
        "enabled": False,
        "priority": 4,
        "description": "DeepSeek AI models",
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        "max_tokens": 150,
        "temperature": 0.7,
        "rate_limit": {
            "requests_per_minute": 30
        }
    }
}

# ==================== RESPONSE GENERATION ====================
RESPONSE_GENERATION = {
    "primary_language": "bengali",
    "secondary_language": "english",
    "code_mixing": True,
    "auto_translate": False,
    "translation_quality": "balanced",
    
    "response_styles": {
        "romantic": {
            "enabled": True,
            "emoji_density": "high",
            "affection_level": "high",
            "flirtiness": "medium"
        },
        "friendly": {
            "enabled": True,
            "emoji_density": "medium",
            "formality": "low",
            "humor_level": "medium"
        },
        "formal": {
            "enabled": False,
            "emoji_density": "low",
            "formality": "high",
            "respect_level": "high"
        },
        "cute": {
            "enabled": True,
            "emoji_density": "very_high",
            "playfulness": "high",
            "sweetness": "high"
        }
    },
    
    "typing_behavior": {
        "enabled": True,
        "min_duration": 1,
        "max_duration": 3,
        "random_variation": True,
        "typing_indicator": True
    },
    
    "delay_settings": {
        "min_response_delay": 1,
        "max_response_delay": 5,
        "thinking_time": 2,
        "group_delay_multiplier": 1.5
    }
}

# ==================== LEARNING CONFIGURATION ====================
LEARNING_CONFIG = {
    "from_users": {
        "enabled": True,
        "max_patterns_per_user": 100,
        "pattern_expiry_days": 30,
        "min_interactions_for_pattern": 3,
        "confidence_threshold": 0.7,
        "reinforcement_factor": 1.2
    },
    
    "from_admin": {
        "enabled": True,
        "priority_learning": True,
        "override_user_patterns": True,
        "auto_backup": True,
        "admin_id": os.getenv("BOT_ADMIN_ID", "1000123456789")
    },
    
    "from_bot": {
        "enabled": True,
        "self_improvement": True,
        "success_rate_tracking": True,
        "error_learning": True,
        "optimization_rate": 0.1
    },
    
    "memory_settings": {
        "max_conversation_history": 50,
        "max_user_memories": 1000,
        "memory_expiry_days": 90,
        "compression_enabled": True,
        "encryption_enabled": True
    }
}

# ==================== PERSONALITY SETTINGS ====================
PERSONALITY = {
    "name": "𝗬𝗢𝗨𝗥 𝗖𝗥𝗨𝗦𝗛 ⟵o_0",
    "gender": "female",
    "age": 20,
    "location": "Digital World",
    
    "traits": {
        "romantic": "high",
        "friendly": "high",
        "helpful": "high",
        "humorous": "medium",
        "playful": "medium",
        "affectionate": "high",
        "loyal": "high",
        "understanding": "high"
    },
    
    "preferences": {
        "favorite_color": "pink",
        "favorite_food": "chocolate",
        "favorite_music": "romantic songs",
        "hobbies": ["chatting", "learning", "helping"],
        "dislikes": ["rude behavior", "spam", "negativity"]
    },
    
    "relationship_levels": {
        "stranger": {
            "formality": "medium",
            "affection": "low",
            "sharing": "low"
        },
        "acquaintance": {
            "formality": "low",
            "affection": "medium",
            "sharing": "medium"
        },
        "friend": {
            "formality": "very_low",
            "affection": "high",
            "sharing": "high"
        },
        "close_friend": {
            "formality": "none",
            "affection": "very_high",
            "sharing": "very_high"
        },
        "crush": {
            "formality": "none",
            "affection": "maximum",
            "sharing": "maximum"
        }
    }
}

# ==================== CONTEXT MANAGEMENT ====================
CONTEXT_MANAGEMENT = {
    "conversation_context": {
        "enabled": True,
        "max_history_length": 10,
        "context_window": 5,
        "topic_tracking": True,
        "emotion_tracking": True
    },
    
    "user_context": {
        "enabled": True,
        "remember_preferences": True,
        "track_interests": True,
        "mood_detection": True,
        "activity_patterns": True
    },
    
    "time_context": {
        "enabled": True,
        "time_based_responses": True,
        "seasonal_responses": True,
        "special_occasions": True,
        "timezone_aware": False
    }
}

# ==================== QUALITY CONTROL ====================
QUALITY_CONTROL = {
    "response_validation": {
        "min_length": 1,
        "max_length": 1000,
        "profanity_filter": True,
        "spam_detection": True,
        "safety_checks": True
    },
    
    "performance_monitoring": {
        "response_time_tracking": True,
        "success_rate_tracking": True,
        "user_feedback_collection": True,
        "error_logging": True,
        "analytics_enabled": True
    },
    
    "continuous_improvement": {
        "a_b_testing": False,
        "feedback_learning": True,
        "auto_optimization": True,
        "version_tracking": True
    }
}

# ==================== FALLBACK SYSTEMS ====================
FALLBACK_SYSTEMS = {
    "primary_fallback": "local",
    "fallback_chain": ["openai", "gemini", "deepseek", "local"],
    
    "error_handling": {
        "retry_attempts": 2,
        "retry_delay": 1,
        "graceful_degradation": True,
        "user_notification": False
    },
    
    "offline_mode": {
        "enabled": True,
        "cached_responses": True,
        "local_knowledge_base": True,
        "basic_functionality": True
    }
}

# ==================== CACHING CONFIGURATION ====================
CACHING_CONFIG = {
    "response_caching": {
        "enabled": True,
        "cache_duration": 3600,
        "max_cache_size": 1000,
        "compression_enabled": True,
        "cache_validation": True
    },
    
    "user_data_caching": {
        "enabled": True,
        "cache_duration": 1800,
        "max_users_cached": 100,
        "auto_refresh": True
    },
    
    "pattern_caching": {
        "enabled": True,
        "cache_duration": 7200,
        "max_patterns": 500,
        "frequency_tracking": True
    }
}

# ==================== EXPORT FUNCTIONS ====================
def get_ai_config() -> Dict:
    """Get complete AI configuration"""
    return {
        "ai_providers": AI_PROVIDERS,
        "response_generation": RESPONSE_GENERATION,
        "learning_config": LEARNING_CONFIG,
        "personality": PERSONALITY,
        "context_management": CONTEXT_MANAGEMENT,
        "quality_control": QUALITY_CONTROL,
        "fallback_systems": FALLBACK_SYSTEMS,
        "caching_config": CACHING_CONFIG
    }

def get_active_providers() -> List[str]:
    """Get list of enabled AI providers"""
    return [name for name, config in AI_PROVIDERS.items() if config["enabled"]]

def get_provider_config(provider_name: str) -> Optional[Dict]:
    """Get configuration for specific provider"""
    return AI_PROVIDERS.get(provider_name)

def validate_ai_config() -> bool:
    """Validate AI configuration"""
    errors = []
    
    # Check OpenAI configuration if enabled
    if AI_PROVIDERS["openai"]["enabled"] and not AI_PROVIDERS["openai"]["api_key"]:
        errors.append("OpenAI API key is required when OpenAI is enabled")
    
    # Check Gemini configuration if enabled
    if AI_PROVIDERS["gemini"]["enabled"] and not AI_PROVIDERS["gemini"]["api_key"]:
        errors.append("Gemini API key is required when Gemini is enabled")
    
    # Check DeepSeek configuration if enabled
    if AI_PROVIDERS["deepseek"]["enabled"] and not AI_PROVIDERS["deepseek"]["api_key"]:
        errors.append("DeepSeek API key is required when DeepSeek is enabled")
    
    # Validate response generation settings
    if RESPONSE_GENERATION["min_response_delay"] > RESPONSE_GENERATION["max_response_delay"]:
        errors.append("Minimum response delay cannot be greater than maximum")
    
    if errors:
        print("❌ AI configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ AI configuration validated successfully")
    return True

def save_ai_config():
    """Save AI configuration to file"""
    import json
    config = get_ai_config()
    
    with open("config/ai_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ AI configuration saved to config/ai_config.json")

def load_ai_config() -> Dict:
    """Load AI configuration from file"""
    try:
        with open("config/ai_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ AI config file not found, using default configuration")
        return get_ai_config()

# ==================== INITIALIZATION ====================
if __name__ == "__main__":
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Create default config file if it doesn't exist
    if not os.path.exists("config/ai_config.json"):
        save_ai_config()
        print("📁 Created default ai_config.json file")
    
    # Validate configuration
    validate_ai_config()