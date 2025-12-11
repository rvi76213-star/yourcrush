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