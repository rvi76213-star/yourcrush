#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Learning System
Learns from users, admin, and bot interactions
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from utils.logger import setup_logger
from utils.file_handler import FileHandler


class LearningSystem:
    """🧠 AI Learning System"""
    
    def __init__(self):
        self.logger = setup_logger("learning_system", "data/logs/learning_log.log")
        self.file_handler = FileHandler()
        
        # Learning data storage
        self.user_patterns = {}
        self.admin_knowledge = {}
        self.bot_memories = {}
        self.conversation_history = {}
        
        # Learning configuration
        self.config = {
            "learn_from_users": True,
            "learn_from_admin": True,
            "learn_from_bot": True,
            "max_memory_per_user": 100,
            "min_confidence": 0.7,
            "save_interval": 300  # seconds
        }
        
        # Initialize
        self.initialize()
    
    def initialize(self):
        """Initialize learning system"""
        try:
            self.logger.info("🧠 Initializing Learning System...")
            
            # Load learning data
            self._load_all_data()
            
            self.logger.info(f"✅ Learning System initialized")
            self.logger.info(f"📊 Stats: {self.get_stats()}")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing learning system: {e}")
    
    def _load_all_data(self):
        """Load all learning data from files"""
        try:
            # User patterns
            user_file = "data/learning/user_patterns.json"
            if os.path.exists(user_file):
                with open(user_file, "r", encoding="utf-8") as f:
                    self.user_patterns = json.load(f)
            else:
                self.user_patterns = {}
                self._save_data(user_file, self.user_patterns)
            
            # Admin knowledge
            admin_file = "data/learning/admin_knowledge.json"
            if os.path.exists(admin_file):
                with open(admin_file, "r", encoding="utf-8") as f:
                    self.admin_knowledge = json.load(f)
            else:
                self.admin_knowledge = {}
                self._save_data(admin_file, self.admin_knowledge)
            
            # Bot memories
            bot_file = "data/learning/bot_memories.json"
            if os.path.exists(bot_file):
                with open(bot_file, "r", encoding="utf-8") as f:
                    self.bot_memories = json.load(f)
            else:
                self.bot_memories = {}
                self._save_data(bot_file, self.bot_memories)
            
            # Conversation history
            conv_file = "data/learning/conversation_history.json"
            if os.path.exists(conv_file):
                with open(conv_file, "r", encoding="utf-8") as f:
                    self.conversation_history = json.load(f)
            else:
                self.conversation_history = {}
                self._save_data(conv_file, self.conversation_history)
            
            self.logger.info(f"✅ Loaded learning data")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading learning data: {e}")
    
    def _save_data(self, file_path: str, data: Dict):
        """Save data to file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"✅ Saved data to {file_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
    
    def learn_interaction(self, user_id: str, user_message: str, bot_response: str, intent: Dict):
        """Learn from a user interaction"""
        try:
            if not self.config["learn_from_users"]:
                return
            
            timestamp = time.time()
            intent_type = intent.get("type", "unknown")
            confidence = intent.get("confidence", 0)
            
            # Create interaction record
            interaction = {
                "user_message": user_message,
                "bot_response": bot_response,
                "intent": intent_type,
                "confidence": confidence,
                "timestamp": timestamp,
                "date": datetime.fromtimestamp(timestamp).isoformat()
            }
            
            # Add to user patterns
            if user_id not in self.user_patterns:
                self.user_patterns[user_id] = {
                    "interactions": [],
                    "preferences": {},
                    "behavior_patterns": {},
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "interaction_count": 0
                }
            
            user_data = self.user_patterns[user_id]
            user_data["interactions"].append(interaction)
            user_data["last_seen"] = timestamp
            user_data["interaction_count"] += 1
            
            # Analyze and update preferences
            self._analyze_user_preferences(user_id, interaction)
            
            # Limit interactions per user
            max_interactions = self.config["max_memory_per_user"]
            if len(user_data["interactions"]) > max_interactions:
                user_data["interactions"] = user_data["interactions"][-max_interactions:]
            
            # Add to conversation history
            conv_key = f"{user_id}_{int(timestamp)}"
            self.conversation_history[conv_key] = interaction
            
            # Save periodically
            if user_data["interaction_count"] % 10 == 0:
                self.save_data()
            
            self.logger.debug(f"🧠 Learned from interaction with {user_id}: {intent_type}")
            
        except Exception as e:
            self.logger.error(f"❌ Error learning interaction: {e}")
    
    def _analyze_user_preferences(self, user_id: str, interaction: Dict):
        """Analyze and update user preferences"""
        try:
            user_data = self.user_patterns[user_id]
            
            # Initialize preferences if not exists
            if "preferences" not in user_data:
                user_data["preferences"] = {
                    "topics": {},
                    "response_types": {},
                    "mood_patterns": {},
                    "active_hours": {}
                }
            
            preferences = user_data["preferences"]
            message = interaction["user_message"].lower()
            intent = interaction["intent"]
            confidence = interaction["confidence"]
            
            # Update topic preferences
            topics = self._extract_topics(message)
            for topic in topics:
                if topic not in preferences["topics"]:
                    preferences["topics"][topic] = 0
                preferences["topics"][topic] += confidence
            
            # Update response type preferences
            if intent not in preferences["response_types"]:
                preferences["response_types"][intent] = 0
            preferences["response_types"][intent] += confidence
            
            # Update mood patterns
            mood = self._detect_mood(message)
            if mood not in preferences["mood_patterns"]:
                preferences["mood_patterns"][mood] = 0
            preferences["mood_patterns"][mood] += 1
            
            # Update active hours
            hour = datetime.fromtimestamp(interaction["timestamp"]).hour
            hour_key = f"{hour:02d}:00"
            if hour_key not in preferences["active_hours"]:
                preferences["active_hours"][hour_key] = 0
            preferences["active_hours"][hour_key] += 1
            
            # Normalize counts
            for pref_type in ["topics", "response_types", "mood_patterns", "active_hours"]:
                total = sum(preferences[pref_type].values())
                if total > 0:
                    for key in preferences[pref_type]:
                        preferences[pref_type][key] /= total
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing preferences: {e}")
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message"""
        topics = []
        message_lower = message.lower()
        
        # Topic keywords
        topic_keywords = {
            "food": ["খাবার", "খিদে", "রান্না", "ভাত", "বিরিয়ানি", "খাই", "food", "eat", "hungry"],
            "music": ["গান", "সঙ্গীত", "মিউজিক", "গায়ক", "সুর", "music", "song", "singer"],
            "movies": ["সিনেমা", "মুভি", "অভিনেতা", "অভিনেত্রী", "movie", "film", "actor"],
            "sports": ["খেলা", "স্পোর্টস", "ফুটবল", "ক্রিকেট", "sports", "game", "football"],
            "study": ["পড়াশুনা", "স্টাডি", "স্কুল", "কলেজ", "study", "school", "college"],
            "work": ["কাজ", "জব", "অফিস", "work", "job", "office"],
            "love": ["ভালোবাসা", "প্রেম", "লাভ", "crush", "love", "romantic"],
            "family": ["পরিবার", "বাবা", "মা", "ভাই", "বোন", "family", "parents"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _detect_mood(self, message: str) -> str:
        """Detect mood from message"""
        message_lower = message.lower()
        
        happy_words = ["খুশি", "আনন্দ", "হাসি", "মজা", "ভালো", "happy", "joy", "smile", "fun"]
        sad_words = ["দুঃখ", "কষ্ট", "কান্না", "বিষণ্ণ", "খারাপ", "sad", "cry", "unhappy"]
        angry_words = ["রাগ", "ক্রোধ", "ঝগড়া", "angry", "mad", "fight", "hate"]
        
        happy_count = sum(1 for word in happy_words if word in message_lower)
        sad_count = sum(1 for word in sad_words if word in message_lower)
        angry_count = sum(1 for word in angry_words if word in message_lower)
        
        if angry_count > happy_count and angry_count > sad_count:
            return "angry"
        elif sad_count > happy_count:
            return "sad"
        elif happy_count > 0:
            return "happy"
        else:
            return "neutral"
    
    def learn_from_admin(self, admin_id: str, command: str, response: str, context: Dict = None):
        """Learn from admin commands and responses"""
        try:
            if not self.config["learn_from_admin"]:
                return
            
            timestamp = time.time()
            
            if admin_id not in self.admin_knowledge:
                self.admin_knowledge[admin_id] = {
                    "commands": {},
                    "responses": {},
                    "patterns": {},
                    "first_seen": timestamp,
                    "last_seen": timestamp
                }
            
            admin_data = self.admin_knowledge[admin_id]
            admin_data["last_seen"] = timestamp
            
            # Store command-response pair
            cmd_key = command[:50]  # Limit key length
            
            if cmd_key not in admin_data["commands"]:
                admin_data["commands"][cmd_key] = {
                    "command": command,
                    "responses": [],
                    "count": 0,
                    "last_used": timestamp
                }
            
            cmd_data = admin_data["commands"][cmd_key]
            cmd_data["responses"].append({
                "response": response,
                "timestamp": timestamp,
                "context": context or {}
            })
            cmd_data["count"] += 1
            cmd_data["last_used"] = timestamp
            
            # Limit stored responses
            if len(cmd_data["responses"]) > 10:
                cmd_data["responses"] = cmd_data["responses"][-10:]
            
            # Save to file
            self._save_data("data/learning/admin_knowledge.json", self.admin_knowledge)
            
            self.logger.info(f"🧠 Learned from admin {admin_id}: {command[:30]}...")
            
        except Exception as e:
            self.logger.error(f"❌ Error learning from admin: {e}")
    
    def learn_from_bot(self, user_id: str, message: str, response: str, success: bool = True):
        """Learn from bot's own interactions"""
        try:
            if not self.config["learn_from_bot"]:
                return
            
            timestamp = time.time()
            
            if "self_learning" not in self.bot_memories:
                self.bot_memories["self_learning"] = {
                    "interactions": [],
                    "success_rate": 0,
                    "total_interactions": 0,
                    "successful_interactions": 0
                }
            
            bot_data = self.bot_memories["self_learning"]
            
            # Record interaction
            interaction = {
                "user_id": user_id,
                "user_message": message,
                "bot_response": response,
                "success": success,
                "timestamp": timestamp
            }
            
            bot_data["interactions"].append(interaction)
            bot_data["total_interactions"] += 1
            
            if success:
                bot_data["successful_interactions"] += 1
            
            # Update success rate
            if bot_data["total_interactions"] > 0:
                bot_data["success_rate"] = bot_data["successful_interactions"] / bot_data["total_interactions"]
            
            # Limit stored interactions
            if len(bot_data["interactions"]) > 100:
                bot_data["interactions"] = bot_data["interactions"][-100:]
            
            # Save periodically
            if bot_data["total_interactions"] % 20 == 0:
                self.save_data()
            
            self.logger.debug(f"🧠 Bot learned from self-interaction: {success}")
            
        except Exception as e:
            self.logger.error(f"❌ Error in bot self-learning: {e}")
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user preferences"""
        try:
            if user_id in self.user_patterns:
                user_data = self.user_patterns[user_id]
                
                # Calculate favorite topics
                topics = user_data.get("preferences", {}).get("topics", {})
                favorite_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
                
                # Calculate preferred response types
                response_types = user_data.get("preferences", {}).get("response_types", {})
                preferred_responses = sorted(response_types.items(), key=lambda x: x[1], reverse=True)[:3]
                
                # Calculate active hours
                active_hours = user_data.get("preferences", {}).get("active_hours", {})
                most_active = sorted(active_hours.items(), key=lambda x: x[1], reverse=True)[:3]
                
                return {
                    "user_id": user_id,
                    "interaction_count": user_data.get("interaction_count", 0),
                    "first_seen": user_data.get("first_seen"),
                    "last_seen": user_data.get("last_seen"),
                    "favorite_topics": [t[0] for t in favorite_topics],
                    "preferred_responses": [r[0] for r in preferred_responses],
                    "most_active_hours": [h[0] for h in most_active],
                    "mood_patterns": user_data.get("preferences", {}).get("mood_patterns", {})
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user preferences: {e}")
            return None
    
    def predict_response(self, user_id: str, message: str) -> Optional[str]:
        """Predict response based on learned patterns"""
        try:
            if user_id not in self.user_patterns:
                return None
            
            user_data = self.user_patterns[user_id]
            interactions = user_data.get("interactions", [])
            
            if not interactions:
                return None
            
            # Find similar past messages
            similar_interactions = []
            message_lower = message.lower()
            
            for interaction in interactions[-20:]:  # Check last 20 interactions
                past_message = interaction["user_message"].lower()
                
                # Simple similarity check (can be improved)
                similarity = self._calculate_similarity(message_lower, past_message)
                
                if similarity > 0.5:  # 50% similarity threshold
                    similar_interactions.append((similarity, interaction))
            
            if similar_interactions:
                # Get the most similar interaction
                similar_interactions.sort(key=lambda x: x[0], reverse=True)
                best_match = similar_interactions[0][1]
                
                # Return the bot's response from that interaction
                return best_match.get("bot_response")
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error predicting response: {e}")
            return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simple implementation)"""
        try:
            # Convert to sets of words
            words1 = set(text1.split())
            words2 = set(text2.split())
            
            if not words1 or not words2:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            return intersection / union if union > 0 else 0.0
            
        except:
            return 0.0
    
    def save_data(self):
        """Save all learning data to files"""
        try:
            # Save user patterns
            self._save_data("data/learning/user_patterns.json", self.user_patterns)
            
            # Save admin knowledge
            self._save_data("data/learning/admin_knowledge.json", self.admin_knowledge)
            
            # Save bot memories
            self._save_data("data/learning/bot_memories.json", self.bot_memories)
            
            # Save conversation history (limited)
            limited_history = {}
            history_items = list(self.conversation_history.items())
            for key, value in history_items[-1000:]:  # Keep last 1000
                limited_history[key] = value
            
            self._save_data("data/learning/conversation_history.json", limited_history)
            
            self.logger.info("💾 Learning data saved successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving learning data: {e}")
    
    def get_stats(self) -> Dict:
        """Get learning system statistics"""
        return {
            "total_users": len(self.user_patterns),
            "total_interactions": sum(
                user_data.get("interaction_count", 0) 
                for user_data in self.user_patterns.values()
            ),
            "admin_knowledge_entries": sum(
                len(admin_data.get("commands", {})) 
                for admin_data in self.admin_knowledge.values()
            ),
            "bot_self_learning": self.bot_memories.get("self_learning", {}).get("total_interactions", 0),
            "bot_success_rate": self.bot_memories.get("self_learning", {}).get("success_rate", 0),
            "conversation_history_count": len(self.conversation_history)
        }
    
    def clear_user_data(self, user_id: str) -> bool:
        """Clear learning data for a specific user"""
        try:
            if user_id in self.user_patterns:
                del self.user_patterns[user_id]
                
                # Also remove from conversation history
                keys_to_remove = [
                    key for key in self.conversation_history.keys() 
                    if key.startswith(f"{user_id}_")
                ]
                
                for key in keys_to_remove:
                    del self.conversation_history[key]
                
                self.save_data()
                self.logger.info(f"🧹 Cleared learning data for user {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error clearing user data: {e}")
            return False
    
    def export_learning_data(self, format_type: str = "json") -> Optional[str]:
        """Export learning data"""
        try:
            all_data = {
                "user_patterns": self.user_patterns,
                "admin_knowledge": self.admin_knowledge,
                "bot_memories": self.bot_memories,
                "conversation_history": self.conversation_history,
                "stats": self.get_stats(),
                "export_timestamp": time.time(),
                "export_date": datetime.now().isoformat()
            }
            
            if format_type == "json":
                return json.dumps(all_data, indent=2, ensure_ascii=False)
            elif format_type == "minified":
                return json.dumps(all_data, separators=(',', ':'), ensure_ascii=False)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error exporting learning data: {e}")
            return None
    
    def import_learning_data(self, data_str: str) -> bool:
        """Import learning data"""
        try:
            data = json.loads(data_str)
            
            if "user_patterns" in data:
                self.user_patterns.update(data["user_patterns"])
            
            if "admin_knowledge" in data:
                self.admin_knowledge.update(data["admin_knowledge"])
            
            if "bot_memories" in data:
                self.bot_memories.update(data["bot_memories"])
            
            if "conversation_history" in data:
                self.conversation_history.update(data["conversation_history"])
            
            self.save_data()
            self.logger.info("✅ Learning data imported successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error importing learning data: {e}")
            return False

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Learning System - AI learning from users, admin, and bot itself
"""

import json
import time
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
from collections import defaultdict, Counter

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

class LearningSystem:
    """AI learning system that learns from interactions"""
    
    def __init__(self, bot_core):
        self.bot = bot_core
        self.logger = bot_core.logger
        self.config = bot_core.config.get('learning', {})
        
        # Learning sources
        self.enabled = self.config.get('enabled', True)
        self.learn_from_users = self.config.get('learn_from_users', True)
        self.learn_from_admin = self.config.get('learn_from_admin', True)
        self.learn_from_bot = self.config.get('learn_from_bot', True)
        self.max_memory = self.config.get('max_memory', 1000)
        
        # Learning data storage
        self.data_dir = Path("data/learning")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Knowledge bases
        self.user_patterns = self.load_knowledge("user_patterns.json")
        self.admin_knowledge = self.load_knowledge("admin_knowledge.json")
        self.bot_memories = self.load_knowledge("bot_memories.json")
        self.conversation_history = self.load_knowledge("conversation_history.json")
        self.learned_responses = self.load_knowledge("learned_responses.json")
        
        # Learning statistics
        self.stats = {
            'total_learned': 0,
            'user_patterns_learned': 0,
            'admin_knowledge_learned': 0,
            'bot_memories_created': 0,
            'responses_learned': 0,
            'last_learning': None
        }
        
        # Pattern recognition
        self.pattern_cache = {}
        self.response_cache = {}
        
        # Initialize with default knowledge
        self.initialize_default_knowledge()
        
        self.logger.info("LearningSystem initialized")
    
    def load_knowledge(self, filename: str) -> Dict:
        """Load knowledge from JSON file"""
        file_path = self.data_dir / filename
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading {filename}: {e}")
        
        # Return empty structure
        if filename == "user_patterns.json":
            return {'patterns': {}, 'user_stats': {}}
        elif filename == "admin_knowledge.json":
            return {'commands': {}, 'responses': {}, 'preferences': {}}
        elif filename == "bot_memories.json":
            return {'memories': [], 'lessons': {}}
        elif filename == "conversation_history.json":
            return {'conversations': [], 'topics': {}}
        elif filename == "learned_responses.json":
            return {'responses': {}, 'contexts': {}}
        else:
            return {}
    
    def save_knowledge(self, data: Dict, filename: str):
        """Save knowledge to JSON file"""
        if not self.enabled:
            return
        
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving {filename}: {e}")
    
    def initialize_default_knowledge(self):
        """Initialize with default knowledge if empty"""
        # Default user patterns
        if not self.user_patterns.get('patterns'):
            self.user_patterns['patterns'] = {
                'greeting_patterns': {
                    'responses': ['হ্যালো!', 'হাই!', 'কেমন আছো?'],
                    'triggers': ['hi', 'hello', 'হাই', 'হ্যালো', 'সালাম']
                },
                'farewell_patterns': {
                    'responses': ['বিদায়!', 'বাই!', 'আবার দেখা হবে!'],
                    'triggers': ['bye', 'goodbye', 'বিদায়', 'বাই']
                }
            }
            self.save_knowledge(self.user_patterns, "user_patterns.json")
        
        # Default admin knowledge
        if not self.admin_knowledge.get('responses'):
            self.admin_knowledge['responses'] = {
                'greeting': ['ওয়েলকাম মাস্টার!', 'হ্যালো এডমিন!', 'স্যার কীভাবে সাহায্য করতে পারি?'],
                'command_confirmation': ['রoger that!', 'ডান!', 'কাজ করছি...']
            }
            self.save_knowledge(self.admin_knowledge, "admin_knowledge.json")
        
        # Default bot memories
        if not self.bot_memories.get('memories'):
            self.bot_memories['memories'] = [
                {
                    'memory': 'Users often ask for photos',
                    'context': 'photo_requests',
                    'learned_from': 'user_patterns',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'memory': '.murgi command is popular',
                    'context': 'command_usage',
                    'learned_from': 'user_interactions',
                    'timestamp': datetime.now().isoformat()
                }
            ]
            self.save_knowledge(self.bot_memories, "bot_memories.json")
        
        # Default learned responses
        if not self.learned_responses.get('responses'):
            self.learned_responses['responses'] = {
                'greeting': {
                    'responses': ['হ্যালো! কেমন আছো? 😊', 'হাই! আজকে কেমন যাচ্ছে?'],
                    'confidence': 0.9,
                    'usage_count': 0
                },
                'photo_request': {
                    'responses': ['📸 তোমার জন্য ছবি!', '🤖 এই নাও ফটো!'],
                    'confidence': 0.8,
                    'usage_count': 0
                }
            }
            self.save_knowledge(self.learned_responses, "learned_responses.json")
    
    def learn_from_interaction(self, message: str, response: str, user_id: str, 
                              context: Dict = None):
        """
        Learn from a single interaction
        
        Args:
            message: User message
            response: Bot response
            user_id: User ID
            context: Additional context (chat type, timestamp, etc.)
        """
        if not self.enabled:
            return
        
        context = context or {}
        timestamp = context.get('timestamp', datetime.now().isoformat())
        chat_type = context.get('chat_type', 'private')
        
        # Learn from user (message patterns)
        if self.learn_from_users:
            self.learn_from_user(message, user_id, timestamp, chat_type)
        
        # Learn from admin (if user is admin)
        if self.learn_from_admin and self.is_admin_user(user_id):
            self.learn_from_admin_interaction(message, response, user_id, timestamp)
        
        # Learn from bot (self-improvement)
        if self.learn_from_bot:
            self.learn_from_bot_response(message, response, user_id, timestamp)
        
        # Update conversation history
        self.update_conversation_history(message, response, user_id, timestamp, chat_type)
        
        # Update statistics
        self.stats['total_learned'] += 1
        self.stats['last_learning'] = timestamp
        
        # Save knowledge periodically
        if self.stats['total_learned'] % 10 == 0:
            self.save_all_knowledge()
    
    def learn_from_user(self, message: str, user_id: str, timestamp: str, chat_type: str):
        """Learn patterns from user messages"""
        # Extract patterns from message
        patterns = self.extract_patterns(message)
        
        # Update user statistics
        if 'user_stats' not in self.user_patterns:
            self.user_patterns['user_stats'] = {}
        
        if user_id not in self.user_patterns['user_stats']:
            self.user_patterns['user_stats'][user_id] = {
                'message_count': 0,
                'last_message': None,
                'common_words': {},
                'preferences': {}
            }
        
        user_stats = self.user_patterns['user_stats'][user_id]
        user_stats['message_count'] += 1
        user_stats['last_message'] = timestamp
        
        # Update common words
        words = self.extract_words(message)
        word_counts = Counter(words)
        
        for word, count in word_counts.items():
            if word in user_stats['common_words']:
                user_stats['common_words'][word] += count
            else:
                user_stats['common_words'][word] = count
        
        # Keep only top 50 words
        top_words = dict(sorted(
            user_stats['common_words'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:50])
        user_stats['common_words'] = top_words
        
        # Learn message patterns
        for pattern_type, pattern_data in patterns.items():
            if pattern_type not in self.user_patterns['patterns']:
                self.user_patterns['patterns'][pattern_type] = {
                    'examples': [],
                    'count': 0,
                    'users': set()
                }
            
            pattern_entry = self.user_patterns['patterns'][pattern_type]
            pattern_entry['count'] += 1
            pattern_entry['users'].add(user_id)
            
            # Add example if not too similar to existing ones
            example = {
                'message': message,
                'user_id': user_id,
                'timestamp': timestamp,
                'chat_type': chat_type
            }
            
            if not self.is_similar_example(example, pattern_entry['examples']):
                pattern_entry['examples'].append(example)
                
                # Limit examples
                if len(pattern_entry['examples']) > 20:
                    pattern_entry['examples'] = pattern_entry['examples'][-20:]
        
        self.stats['user_patterns_learned'] += 1
    
    def learn_from_admin_interaction(self, message: str, response: str, 
                                    user_id: str, timestamp: str):
        """Learn from admin interactions"""
        # Learn admin commands
        if message.startswith('.') or message.startswith('!'):
            command = message.split()[0]
            
            if 'commands' not in self.admin_knowledge:
                self.admin_knowledge['commands'] = {}
            
            if command not in self.admin_knowledge['commands']:
                self.admin_knowledge['commands'][command] = {
                    'usage_count': 0,
                    'last_used': None,
                    'responses': []
                }
            
            cmd_entry = self.admin_knowledge['commands'][command]
            cmd_entry['usage_count'] += 1
            cmd_entry['last_used'] = timestamp
            
            # Store response pattern
            response_pattern = self.extract_response_pattern(response)
            if response_pattern and response_pattern not in cmd_entry['responses']:
                cmd_entry['responses'].append(response_pattern)
        
        # Learn admin response preferences
        response_key = self.generate_response_key(message)
        
        if 'responses' not in self.admin_knowledge:
            self.admin_knowledge['responses'] = {}
        
        if response_key not in self.admin_knowledge['responses']:
            self.admin_knowledge['responses'][response_key] = {
                'admin_response': response,
                'usage_count': 0,
                'last_used': timestamp
            }
        else:
            resp_entry = self.admin_knowledge['responses'][response_key]
            resp_entry['usage_count'] += 1
            resp_entry['last_used'] = timestamp
            
            # Update response if admin uses a better one
            if len(response) > len(resp_entry['admin_response']):
                resp_entry['admin_response'] = response
        
        self.stats['admin_knowledge_learned'] += 1
    
    def learn_from_bot_response(self, message: str, response: str, 
                               user_id: str, timestamp: str):
        """Learn from bot's own responses (self-improvement)"""
        # Create memory of this interaction
        memory = {
            'user_message': message,
            'bot_response': response,
            'user_id': user_id,
            'timestamp': timestamp,
            'effectiveness': 0.5  # Initial neutral effectiveness
        }
        
        if 'memories' not in self.bot_memories:
            self.bot_memories['memories'] = []
        
        self.bot_memories['memories'].append(memory)
        
        # Limit memories
        if len(self.bot_memories['memories']) > self.max_memory:
            self.bot_memories['memories'] = self.bot_memories['memories'][-self.max_memory:]
        
        # Learn response patterns
        response_key = self.generate_response_key(message)
        
        if 'responses' not in self.learned_responses:
            self.learned_responses['responses'] = {}
        
        if response_key not in self.learned_responses['responses']:
            self.learned_responses['responses'][response_key] = {
                'responses': [response],
                'confidence': 0.7,
                'usage_count': 1,
                'last_used': timestamp,
                'effectiveness_sum': 0.5
            }
        else:
            resp_entry = self.learned_responses['responses'][response_key]
            
            # Add response if not already present
            if response not in resp_entry['responses']:
                resp_entry['responses'].append(response)
                
                # Limit number of responses
                if len(resp_entry['responses']) > 5:
                    # Remove least used response
                    resp_entry['responses'] = resp_entry['responses'][-5:]
            
            resp_entry['usage_count'] += 1
            resp_entry['last_used'] = timestamp
        
        self.stats['responses_learned'] += 1
        self.stats['bot_memories_created'] += 1
    
    def update_conversation_history(self, message: str, response: str, 
                                   user_id: str, timestamp: str, chat_type: str):
        """Update conversation history"""
        conversation = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': timestamp,
            'chat_type': chat_type
        }
        
        if 'conversations' not in self.conversation_history:
            self.conversation_history['conversations'] = []
        
        self.conversation_history['conversations'].append(conversation)
        
        # Limit history
        if len(self.conversation_history['conversations']) > 1000:
            self.conversation_history['conversations'] = \
                self.conversation_history['conversations'][-1000:]
        
        # Extract and update topics
        topics = self.extract_topics(message)
        for topic in topics:
            if 'topics' not in self.conversation_history:
                self.conversation_history['topics'] = {}
            
            if topic not in self.conversation_history['topics']:
                self.conversation_history['topics'][topic] = {
                    'count': 0,
                    'last_mentioned': None,
                    'users': set()
                }
            
            topic_entry = self.conversation_history['topics'][topic]
            topic_entry['count'] += 1
            topic_entry['last_mentioned'] = timestamp
            topic_entry['users'].add(user_id)
    
    def extract_patterns(self, message: str) -> Dict[str, Any]:
        """Extract patterns from message"""
        patterns = {}
        
        # Check for greetings
        greeting_words = ['hi', 'hello', 'হাই', 'হ্যালো', 'সালাম', 'নমস্কার']
        if any(word in message.lower() for word in greeting_words):
            patterns['greeting'] = {'type': 'greeting', 'confidence': 0.8}
        
        # Check for questions
        if '?' in message or any(word in message.lower() for word in 
                               ['কী', 'কেন', 'কিভাবে', 'কখন', 'কোথায়', 'কে']):
            patterns['question'] = {'type': 'question', 'confidence': 0.7}
        
        # Check for photo requests
        photo_words = ['ছবি', 'ফটো', 'photo', 'pic', 'picture']
        if any(word in message.lower() for word in photo_words):
            patterns['photo_request'] = {'type': 'photo_request', 'confidence': 0.9}
        
        # Check for commands
        if message.startswith('.') or message.startswith('!'):
            patterns['command'] = {'type': 'command', 'confidence': 1.0}
        
        # Check for romantic content
        romantic_words = ['ভালোবাস', 'লাভ', 'love', 'প্রেম', 'ক্রাশ']
        if any(word in message.lower() for word in romantic_words):
            patterns['romantic'] = {'type': 'romantic', 'confidence': 0.8}
        
        return patterns
    
    def extract_words(self, text: str) -> List[str]:
        """Extract words from text"""
        # Simple word extraction
        words = re.findall(r'[\w\u0980-\u09FF]+', text.lower())
        return [word for word in words if len(word) > 1]
    
    def is_similar_example(self, example: Dict, existing_examples: List[Dict]) -> bool:
        """Check if example is similar to existing examples"""
        if not existing_examples:
            return False
        
        # Simple similarity check based on message length and word overlap
        message = example['message'].lower()
        message_words = set(self.extract_words(message))
        
        for existing in existing_examples[-5:]:  # Check last 5 examples
            existing_msg = existing['message'].lower()
            existing_words = set(self.extract_words(existing_msg))
            
            # Calculate similarity
            if message_words and existing_words:
                similarity = len(message_words & existing_words) / len(message_words | existing_words)
                if similarity > 0.7:  # 70% similar
                    return True
        
        return False
    
    def extract_response_pattern(self, response: str) -> Dict:
        """Extract pattern from response"""
        return {
            'text': response,
            'length': len(response),
            'word_count': len(response.split()),
            'has_emoji': any(c in response for c in ['😊', '❤️', '✨', '🎯', '📸']),
            'language': self.detect_language(response)
        }
    
    def generate_response_key(self, message: str) -> str:
        """Generate a key for categorizing responses"""
        message_lower = message.lower()
        
        # Categorize by intent/type
        if any(word in message_lower for word in ['hi', 'hello', 'হাই', 'হ্যালো']):
            return 'greeting'
        elif any(word in message_lower for word in ['ছবি', 'ফটো', 'photo']):
            return 'photo_request'
        elif '?' in message_lower:
            return 'question'
        elif any(word in message_lower for word in ['ভালোবাস', 'love', 'প্রেম']):
            return 'romantic'
        elif message_lower.startswith('.murgi'):
            return 'command_murgi'
        elif message_lower.startswith('.love'):
            return 'command_love'
        elif message_lower.startswith('.pick'):
            return 'command_pick'
        else:
            # Use first few words as key
            words = message_lower.split()[:3]
            return '_'.join(words) if words else 'other'
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        # Simple detection based on character ranges
        bengali_chars = set('\u0980-\u09FF')
        english_chars = set('abcdefghijklmnopqrstuvwxyz')
        
        bengali_count = sum(1 for c in text if c in bengali_chars)
        english_count = sum(1 for c in text.lower() if c in english_chars)
        
        if bengali_count > english_count:
            return 'bengali'
        elif english_count > bengali_count:
            return 'english'
        else:
            return 'mixed'
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        topics = []
        text_lower = text.lower()
        
        # Define topic keywords
        topic_keywords = {
            'photo': ['ছবি', 'ফটো', 'photo', 'pic', 'picture'],
            'love': ['ভালোবাস', 'লাভ', 'love', 'প্রেম', 'ক্রাশ'],
            'bot': ['বট', 'bot', 'রোবট', 'robot'],
            'admin': ['এডমিন', 'admin', 'মাস্টার', 'master'],
            'facebook': ['ফেসবুক', 'facebook'],
            'murgi': ['মুরগি', 'murgi', 'chicken'],
            'music': ['গান', 'music', 'সঙ্গীত', 'song'],
            'game': ['গেম', 'game', 'খেলা']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def is_admin_user(self, user_id: str) -> bool:
        """Check if user is admin"""
        admin_ids = self.bot.config.get('admins', [])
        return user_id in admin_ids or 'admin' in user_id.lower()
    
    def get_learned_response(self, message: str, user_id: str = None) -> Optional[str]:
        """Get a learned response for message"""
        if not self.enabled or not self.learned_responses.get('responses'):
            return None
        
        response_key = self.generate_response_key(message)
        
        if response_key in self.learned_responses['responses']:
            resp_entry = self.learned_responses['responses'][response_key]
            
            # Check confidence threshold
            if resp_entry['confidence'] < 0.5:
                return None
            
            # Get most appropriate response
            responses = resp_entry['responses']
            
            # Consider user preferences if available
            if user_id and user_id in self.user_patterns.get('user_stats', {}):
                user_prefs = self.user_patterns['user_stats'][user_id].get('preferences', {})
                
                # Check if user has response preferences
                if 'preferred_responses' in user_prefs and response_key in user_prefs['preferred_responses']:
                    preferred = user_prefs['preferred_responses'][response_key]
                    if preferred in responses:
                        return preferred
            
            # Return random response (weighted by effectiveness if available)
            if responses:
                return random.choice(responses)
        
        return None
    
    def improve_response(self, original_response: str, message: str, 
                        user_id: str = None) -> str:
        """Improve a response using learned knowledge"""
        if not self.enabled:
            return original_response
        
        # Get learned response
        learned_response = self.get_learned_response(message, user_id)
        
        if learned_response and learned_response != original_response:
            # Sometimes use learned response instead
            if random.random() < 0.3:  # 30% chance to use learned response
                return learned_response
            
            # Sometimes combine with learned response
            if random.random() < 0.2:  # 20% chance to combine
                return f"{original_response} {learned_response}"
        
        # Apply learned improvements
        improved_response = self.apply_improvements(original_response, user_id)
        
        return improved_response
    
    def apply_improvements(self, response: str, user_id: str = None) -> str:
        """Apply learned improvements to response"""
        # Add emojis based on learned preferences
        if user_id and user_id in self.user_patterns.get('user_stats', {}):
            user_stats = self.user_patterns['user_stats'][user_id]
            
            # Check if user likes emojis
            if user_stats.get('preferences', {}).get('likes_emojis', True):
                # Add appropriate emoji based on response content
                if any(word in response.lower() for word in ['হ্যালো', 'হাই', 'hello', 'hi']):
                    response = f"{response} 😊"
                elif any(word in response.lower() for word in ['ভালোবাস', 'লাভ', 'love']):
                    response = f"{response} ❤️"
                elif any(word in response.lower() for word in ['ছবি', 'ফটো', 'photo']):
                    response = f"{response} 📸"
        
        # Personalize for returning users
        if user_id and user_id in self.user_patterns.get('user_stats', {}):
            user_stats = self.user_patterns['user_stats'][user_id]
            if user_stats['message_count'] > 5:
                # Add personal touch for frequent users
                if random.random() < 0.1:  # 10% chance
                    name_part = user_id[-4:]  # Use last 4 digits as identifier
                    response = f"{response} (User#{name_part})"
        
        return response
    
    def update_response_effectiveness(self, message: str, response: str, 
                                     user_id: str, effectiveness: float):
        """Update effectiveness score for a response"""
        response_key = self.generate_response_key(message)
        
        if response_key in self.learned_responses.get('responses', {}):
            resp_entry = self.learned_responses['responses'][response_key]
            
            # Update effectiveness
            if 'effectiveness_sum' not in resp_entry:
                resp_entry['effectiveness_sum'] = 0
            
            resp_entry['effectiveness_sum'] += effectiveness
            resp_entry['confidence'] = resp_entry['effectiveness_sum'] / resp_entry['usage_count']
            
            # If response has low effectiveness, consider replacing it
            if resp_entry['confidence'] < 0.3 and len(resp_entry['responses']) > 1:
                # Find the least effective response
                resp_entry['responses'] = resp_entry['responses'][1:]  # Remove first
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics"""
        return {
            **self.stats,
            'user_patterns_count': len(self.user_patterns.get('patterns', {})),
            'admin_knowledge_count': len(self.admin_knowledge.get('responses', {})),
            'bot_memories_count': len(self.bot_memories.get('memories', [])),
            'learned_responses_count': len(self.learned_responses.get('responses', {})),
            'conversation_history_count': len(self.conversation_history.get('conversations', [])),
            'unique_users_learned': len(self.user_patterns.get('user_stats', {})),
            'topics_learned': len(self.conversation_history.get('topics', {}))
        }
    
    def save_all_knowledge(self):
        """Save all knowledge bases"""
        self.save_knowledge(self.user_patterns, "user_patterns.json")
        self.save_knowledge(self.admin_knowledge, "admin_knowledge.json")
        self.save_knowledge(self.bot_memories, "bot_memories.json")
        self.save_knowledge(self.conversation_history, "conversation_history.json")
        self.save_knowledge(self.learned_responses, "learned_responses.json")
        
        self.logger.info("All knowledge bases saved")
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old learning data"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cutoff_iso = cutoff_date.isoformat()
        
        # Clean old conversations
        if 'conversations' in self.conversation_history:
            self.conversation_history['conversations'] = [
                conv for conv in self.conversation_history['conversations']
                if conv['timestamp'] > cutoff_iso
            ]
        
        # Clean old memories
        if 'memories' in self.bot_memories:
            self.bot_memories['memories'] = [
                mem for mem in self.bot_memories['memories']
                if mem['timestamp'] > cutoff_iso
            ]
        
        # Clean old user stats (inactive users)
        if 'user_stats' in self.user_patterns:
            active_users = {}
            for user_id, stats in self.user_patterns['user_stats'].items():
                if stats.get('last_message', '') > cutoff_iso:
                    active_users[user_id] = stats
            self.user_patterns['user_stats'] = active_users
        
        self.save_all_knowledge()
        self.logger.info(f"Cleaned up data older than {days_old} days")

if __name__ == "__main__":
    print("Learning System Module Loaded")
    
    # Test with mock bot
    from unittest.mock import Mock
    
    mock_bot = Mock()
    mock_bot.logger = Mock()
    mock_bot.logger.info = print
    mock_bot.logger.error = print
    mock_bot.config = {
        'learning': {
            'enabled': True,
            'learn_from_users': True,
            'learn_from_admin': True,
            'learn_from_bot': True,
            'max_memory': 1000
        },
        'admins': ['admin_123']
    }
    
    print("\n🧪 Testing Learning System:")
    print("="*50)
    
    try:
        learning_system = LearningSystem(mock_bot)
        
        # Test learning from interactions
        test_interactions = [
            ("হাই", "হ্যালো! কেমন আছো?", "user_123", {}),
            ("ছবি দাও", "📸 তোমার জন্য ছবি!", "user_456", {}),
            ("তুমি কেমন আছো?", "আমি ভালো আছি!", "admin_123", {}),
            ("আমি তোমাকে ভালোবাসি", "💖 আমিও তোমাকে ভালোবাসি!", "user_789", {}),
            (".murgi", "🐔 Starting murgi sequence...", "user_123", {})
        ]
        
        print("\n📚 Testing learning from interactions:")
        for message, response, user_id, context in test_interactions:
            learning_system.learn_from_interaction(message, response, user_id, context)
            print(f"💬 Learned from: '{message}' -> '{response[:20]}...'")
        
        # Test getting learned response
        print("\n🤖 Testing learned responses:")
        test_messages = ["হাই", "ছবি চাই", "কেমন আছো?"]
        for msg in test_messages:
            learned = learning_system.get_learned_response(msg)
            print(f"💭 '{msg}' -> Learned response: {learned[:30] if learned else 'None'}")
        
        # Test response improvement
        print("\n✨ Testing response improvement:")
        test_improvements = [
            ("হ্যালো", "user_123"),
            ("ধন্যবাদ", "user_456"),
            ("বিদায়", "admin_123")
        ]
        
        for original, user_id in test_improvements:
            improved = learning_system.improve_response(original, original, user_id)
            print(f"📝 '{original}' -> Improved: '{improved}'")
        
        # Test statistics
        print("\n📊 Testing learning statistics:")
        stats = learning_system.get_learning_stats()
        for key, value in stats.items():
            if isinstance(value, (int, float, str)):
                print(f"  {key}: {value}")
        
        # Test cleanup
        print("\n🧹 Testing data cleanup:")
        learning_system.cleanup_old_data(0)  # Clean all old data for testing
        print("Cleanup completed")
        
        print("\n✅ Learning System tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()