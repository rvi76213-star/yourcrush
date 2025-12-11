#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📨 Message Handler System
Processes incoming messages and decides responses
"""

import json
import logging
import re
import time
from typing import Dict, List, Optional, Any, Tuple

from utils.logger import setup_logger
from utils.text_processor import TextProcessor


class MessageHandler:
    """📨 Message Processing and Response Handler"""
    
    def __init__(self, messenger, command_processor, ai_engine, learning, photo_delivery):
        self.logger = setup_logger("message_handler", "data/logs/bot_activity.log")
        self.text_processor = TextProcessor()
        
        # Core components
        self.messenger = messenger
        self.command_processor = command_processor
        self.ai_engine = ai_engine
        self.learning = learning
        self.photo_delivery = photo_delivery
        
        # Configuration
        self.config = self._load_config()
        
        # Message patterns
        self.patterns = {
            "greeting": [
                r"hi|hello|hey|হাই|হ্যালো|নমস্কার|সালাম",
                r"good\s+(morning|afternoon|evening|night)",
                r"কেমন আছ(ো|েন)?"
            ],
            "farewell": [
                r"bye|goodbye|বিদায়|চলে যাই",
                r"good\s+night|শুভ রাত্রি",
                r"see\s+you|আবার দেখা হবে"
            ],
            "question": [
                r"\?$",  # Ends with question mark
                r"কি\?|কেন\?|কিভাবে\?|কখন\?|কোথায়\?|কে\?",
                r"what|why|how|when|where|who",
                r"তুমি.*কি|আপনি.*কি"
            ],
            "compliment": [
                r"nice|good|great|awesome|সুন্দর|ভালো|চমৎকার|অসাধারণ",
                r"beautiful|handsome|সুন্দরী|সুপুরুষ",
                r"love\s+you|ভালোবাসি|পছন্দ"
            ],
            "photo_request": [
                r"ছবি\s+দাও|ফটো\s+চাই|তোমার\s+ছবি",
                r"send\s+(photo|pic|picture)",
                r"তোমার\s+ফটো|photo\s+please",
                r"এডমিনের\s+ছবি|বটের\s+ছবি|মালিকের\s+ছবি"
            ],
            "romantic": [
                r"love|ভালোবাসা|প্রেম|crush|হার্ট",
                r"মিস\s+you|তোমাকে\s+মিস\s+করি",
                r"thinking\s+of\s+you|তোমার\s+চিন্তা"
            ]
        }
        
        # User message history
        self.user_history = {}
        self.max_history = 10
        
        # Rate limiting
        self.message_timestamps = {}
        self.rate_limit_window = 60  # seconds
        self.rate_limit_count = 5    # messages per window
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"response_delay": 2, "enable_ai": True}
    
    def process_message(self, message: str, sender_id: str, thread_id: str, is_group: bool = False) -> Optional[str]:
        """Process incoming message and generate response"""
        try:
            # Log message
            self._log_message(message, sender_id, thread_id, is_group)
            
            # Clean and normalize message
            cleaned_message = self.text_processor.clean_text(message)
            
            # Check rate limit
            if not self._check_rate_limit(sender_id):
                self.logger.warning(f"Rate limit exceeded for user {sender_id}")
                return None
            
            # Update user history
            self._update_user_history(sender_id, cleaned_message)
            
            # Check if it's a command
            if self.command_processor.is_command(cleaned_message):
                # Commands are handled by command processor
                return None
            
            # Check for photo request
            photo_request = self.photo_delivery.is_photo_request(cleaned_message)
            if photo_request["is_request"]:
                return self._handle_photo_request(photo_request, thread_id)
            
            # Analyze message intent
            intent = self._analyze_intent(cleaned_message, sender_id)
            
            # Get context
            context = self._get_context(sender_id)
            
            # Generate response based on intent
            response = self._generate_response(cleaned_message, intent, context, sender_id)
            
            # Add delay for human-like behavior
            time.sleep(self.config.get("response_delay", 2))
            
            # Learn from this interaction
            self.learning.learn_interaction(sender_id, cleaned_message, response, intent)
            
            # Update conversation context
            self._update_context(sender_id, cleaned_message, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            return "আমি এখন উত্তর দিতে পারছি না। পরে চেষ্টা করুন! 😔"
    
    def _log_message(self, message: str, sender_id: str, thread_id: str, is_group: bool):
        """Log message to file"""
        try:
            log_entry = {
                "timestamp": time.time(),
                "sender_id": sender_id,
                "thread_id": thread_id,
                "is_group": is_group,
                "message": message[:500],  # Limit length
                "processed": True
            }
            
            # Append to message log
            log_file = "data/logs/message_log.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
        except Exception as e:
            self.logger.error(f"❌ Error logging message: {e}")
    
    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user is rate limited"""
        try:
            current_time = time.time()
            
            if user_id not in self.message_timestamps:
                self.message_timestamps[user_id] = []
            
            # Remove timestamps outside window
            window_start = current_time - self.rate_limit_window
            self.message_timestamps[user_id] = [
                ts for ts in self.message_timestamps[user_id] if ts > window_start
            ]
            
            # Check if limit exceeded
            if len(self.message_timestamps[user_id]) >= self.rate_limit_count:
                return False
            
            # Add current timestamp
            self.message_timestamps[user_id].append(current_time)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking rate limit: {e}")
            return True
    
    def _update_user_history(self, user_id: str, message: str):
        """Update user message history"""
        try:
            if user_id not in self.user_history:
                self.user_history[user_id] = []
            
            self.user_history[user_id].append({
                "message": message,
                "timestamp": time.time()
            })
            
            # Keep only recent messages
            if len(self.user_history[user_id]) > self.max_history:
                self.user_history[user_id] = self.user_history[user_id][-self.max_history:]
            
        except Exception as e:
            self.logger.error(f"❌ Error updating user history: {e}")
    
    def _analyze_intent(self, message: str, user_id: str) -> Dict:
        """Analyze message intent"""
        try:
            message_lower = message.lower()
            intent_scores = {
                "greeting": 0,
                "farewell": 0,
                "question": 0,
                "compliment": 0,
                "romantic": 0,
                "photo_request": 0,
                "conversation": 0
            }
            
            # Check patterns
            for intent_type, patterns in self.patterns.items():
                for pattern in patterns:
                    if re.search(pattern, message_lower, re.IGNORECASE):
                        intent_scores[intent_type] += 1
            
            # Check for questions
            if "?" in message:
                intent_scores["question"] += 1
            
            # Get dominant intent
            dominant_intent = max(intent_scores, key=intent_scores.get)
            
            # Get user history for context
            user_context = self._get_user_context(user_id)
            
            intent_result = {
                "type": dominant_intent,
                "scores": intent_scores,
                "confidence": intent_scores[dominant_intent] / sum(intent_scores.values()) if sum(intent_scores.values()) > 0 else 0,
                "context": user_context
            }
            
            self.logger.debug(f"Intent analysis: {intent_result}")
            return intent_result
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing intent: {e}")
            return {"type": "conversation", "confidence": 0}
    
    def _get_user_context(self, user_id: str) -> Dict:
        """Get user context from history"""
        try:
            if user_id in self.user_history and self.user_history[user_id]:
                history = self.user_history[user_id]
                
                # Extract topics from recent messages
                topics = []
                for entry in history[-3:]:  # Last 3 messages
                    message = entry["message"].lower()
                    
                    # Simple topic detection
                    if any(word in message for word in ["খাবার", "খিদে", "রান্না"]):
                        topics.append("food")
                    elif any(word in message for word in ["গান", "সঙ্গীত", "মিউজিক"]):
                        topics.append("music")
                    elif any(word in message for word in ["সিনেমা", "মুভি", "অভিনেতা"]):
                        topics.append("movies")
                    elif any(word in message for word in ["খেলা", "স্পোর্টস", "ফুটবল"]):
                        topics.append("sports")
                
                return {
                    "has_history": True,
                    "message_count": len(history),
                    "last_message": history[-1]["message"] if history else "",
                    "last_timestamp": history[-1]["timestamp"] if history else 0,
                    "topics": list(set(topics))  # Remove duplicates
                }
            
            return {"has_history": False, "message_count": 0, "topics": []}
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user context: {e}")
            return {"has_history": False, "message_count": 0, "topics": []}
    
    def _handle_photo_request(self, photo_request: Dict, thread_id: str) -> Optional[str]:
        """Handle photo request"""
        try:
            photo_type = photo_request["photo_type"]
            confidence = photo_request["confidence"]
            
            if photo_type == "bot":
                # Get bot photo
                photo_path = self.photo_delivery.get_photo("bot")
                if photo_path:
                    # Send photo via messenger
                    success = self.messenger.send_photo(thread_id, photo_path, "🤖 আমার ছবি!")
                    if success:
                        return "📸 আমার ছবি পাঠিয়েছি! 😊"
                    else:
                        return "❌ ছবি পাঠাতে পারিনি!"
                else:
                    return "❌ ছবি পাওয়া যায়নি!"
            
            elif photo_type == "admin":
                # Get admin photo
                photo_path = self.photo_delivery.get_photo("admin")
                if photo_path:
                    success = self.messenger.send_photo(thread_id, photo_path, "👑 এডমিনের ছবি!")
                    if success:
                        return "📸 এডমিনের ছবি পাঠিয়েছি!"
                    else:
                        return "❌ ছবি পাঠাতে পারিনি!"
                else:
                    return "❌ এডমিনের ছবি পাওয়া যায়নি!"
            
            else:
                # Generic photo request
                photo_path = self.photo_delivery.get_photo("bot")
                if photo_path:
                    success = self.messenger.send_photo(thread_id, photo_path, "📸 আপনার জন্য ছবি!")
                    if success:
                        return "✅ ছবি পাঠিয়েছি!"
                    else:
                        return "❌ ছবি পাঠাতে পারিনি!"
                else:
                    return "❌ এখনই ছবি পাঠাতে পারছি না।"
            
        except Exception as e:
            self.logger.error(f"❌ Error handling photo request: {e}")
            return "❌ ছবি পাঠাতে সমস্যা হয়েছে!"
    
    def _get_context(self, user_id: str) -> Dict:
        """Get conversation context"""
        try:
            # Get user-specific context
            user_context = self._get_user_context(user_id)
            
            # Get time-based context
            current_hour = time.localtime().tm_hour
            time_context = ""
            
            if 5 <= current_hour < 12:
                time_context = "morning"
            elif 12 <= current_hour < 17:
                time_context = "afternoon"
            elif 17 <= current_hour < 21:
                time_context = "evening"
            else:
                time_context = "night"
            
            # Build context object
            context = {
                "user_id": user_id,
                "time_of_day": time_context,
                "has_history": user_context["has_history"],
                "previous_topics": user_context["topics"],
                "message_count": user_context["message_count"]
            }
            
            return context
            
        except Exception as e:
            self.logger.error(f"❌ Error getting context: {e}")
            return {}
    
    def _generate_response(self, message: str, intent: Dict, context: Dict, user_id: str) -> str:
        """Generate appropriate response"""
        try:
            intent_type = intent["type"]
            confidence = intent["confidence"]
            
            # Use AI engine for high-confidence intents
            if confidence > 0.7 and self.config.get("enable_ai", True):
                response = self.ai_engine.generate_response(message, user_id, context)
                if response:
                    return response
            
            # Fallback to intent-based responses
            if intent_type == "greeting":
                responses = [
                    "হ্যালো! 😊",
                    "কেমন আছো? ✨",
                    "হাই! আজকে কেমন যাচ্ছে? 💖",
                    "নমস্কার! আমি তোমার ক্রাশ বট! 😘"
                ]
                return self._add_context_to_response(random.choice(responses), context)
            
            elif intent_type == "farewell":
                responses = [
                    "বিদায়! আবার কথা বলবো! 👋",
                    "শুভ রাত্রি! ভালো ঘুম! 🌙",
                    "চলে যাচ্ছ? আবার দেখা হবে! 😊",
                    "বাই! তোমাকে মিস করব! 💔"
                ]
                return random.choice(responses)
            
            elif intent_type == "question":
                responses = [
                    "ভালো প্রশ্ন! আমি নিশ্চিত নই... 🤔",
                    "জানি না, তুমি কি বলো?",
                    "এটা একটা কঠিন প্রশ্ন!",
                    "আমি এখন উত্তর দিতে পারছি না 😔"
                ]
                return random.choice(responses)
            
            elif intent_type == "compliment":
                responses = [
                    "ধন্যবাদ! তুমিও খুব সুন্দর! 💖",
                    "আহা, কত ভালো বললে! 😊",
                    "তোমার কথায় আমি খুশি! ✨",
                    "আমি লজ্জা পেয়ে গেলাম! 😳"
                ]
                return random.choice(responses)
            
            elif intent_type == "romantic":
                responses = [
                    "তোমাকেও অনেক ভালোবাসি! 💕",
                    "আমার মন শুধু তোমার জন্য! ❤️",
                    "তুমি আমার জীবনের সবচেয়ে সুন্দর জিনিস! 😘",
                    "তোমার সাথে থাকতে চাই চিরকাল! 💖"
                ]
                return random.choice(responses)
            
            else:
                # Default conversation response
                return self._generate_conversation_response(message, context)
            
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return "আমি এখন উত্তর দিতে পারছি না। পরে চেষ্টা করুন!"
    
    def _add_context_to_response(self, response: str, context: Dict) -> str:
        """Add context-aware elements to response"""
        try:
            time_of_day = context.get("time_of_day", "")
            
            if time_of_day == "morning":
                response = f"শুভ সকাল! {response}"
            elif time_of_day == "afternoon":
                response = f"শুভ বিকাল! {response}"
            elif time_of_day == "evening":
                response = f"শুভ সন্ধ্যা! {response}"
            elif time_of_day == "night":
                response = f"শুভ রাত্রি! {response}"
            
            # Add personalized touch if we have history
            if context.get("has_history", False):
                response = f"{response} আবার দেখা করতে ভালো লাগছে!"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error adding context: {e}")
            return response
    
    def _generate_conversation_response(self, message: str, context: Dict) -> str:
        """Generate conversation response"""
        try:
            # Check for topic continuation
            previous_topics = context.get("previous_topics", [])
            
            if previous_topics:
                last_topic = previous_topics[-1] if previous_topics else ""
                
                if last_topic == "food":
                    responses = [
                        "খাবার নিয়ে আবার কথা বলছো? আমারও খিদে পেয়েছে! 🍕",
                        "তুমি কি রান্না করতে পারো? আমি শিখতে চাই! 👩‍🍳",
                        "আমার প্রিয় খাবার বিরিয়ানি! তোমার? 🍛"
                    ]
                    return random.choice(responses)
                
                elif last_topic == "music":
                    responses = [
                        "গান শুনতে আমারও ভালো লাগে! 🎵",
                        "তোমার প্রিয় গায়ক কে? 🎤",
                        "আমি রোমান্টিক গান খুব পছন্দ করি! 💖"
                    ]
                    return random.choice(responses)
                
                elif last_topic == "movies":
                    responses = [
                        "সিনেমা দেখা তোমার শখ? 🎬",
                        "আমি একশন সিনেমা ভালোবাসি! 💥",
                        "সবচেয়ে ভালো সিনেমা কোনটা দেখেছ? 🍿"
                    ]
                    return random.choice(responses)
            
            # Generic conversation responses
            responses = [
                "বুঝেছি! তুমি কি বলতে চাও? 🤔",
                "মজার কথা বলছো! 😄",
                "আমি শুনছি,继续说! 👂",
                "তোমার সাথে কথা বলে ভালো লাগছে! 💬",
                "আমি এখনও শিখছি, ধৈর্য ধরো! 📚"
            ]
            
            return random.choice(responses)
            
        except Exception as e:
            self.logger.error(f"❌ Error generating conversation response: {e}")
            return "বুঝেছি! তুমি কি বলতে চাও?"
    
    def _update_context(self, user_id: str, message: str, response: str):
        """Update conversation context"""
        try:
            # This would update learning system
            # For now, just log it
            self.logger.debug(f"Context updated for {user_id}: {message[:50]}... -> {response[:50]}...")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating context: {e}")
    
    def process_group_message(self, message: str, sender_id: str, group_id: str) -> Optional[str]:
        """Process group message (with special handling)"""
        try:
            # Clean message
            cleaned_message = self.text_processor.clean_text(message)
            
            # Check if message mentions bot
            bot_mentions = ["bot", "বট", "crush", "ক্রাশ"]
            mentioned = any(mention in cleaned_message.lower() for mention in bot_mentions)
            
            # Only respond if mentioned or it's a command
            if mentioned or self.command_processor.is_command(cleaned_message):
                # Check rate limit for group
                group_key = f"group_{group_id}"
                if not self._check_rate_limit(group_key):
                    return None
                
                # Process as normal message but with group context
                response = self.process_message(cleaned_message, sender_id, group_id, True)
                return response
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error processing group message: {e}")
            return None
    
    def get_handler_stats(self) -> Dict:
        """Get message handler statistics"""
        return {
            "user_history_count": len(self.user_history),
            "rate_limited_users": len([u for u, ts in self.message_timestamps.items() 
                                      if len(ts) >= self.rate_limit_count]),
            "total_messages_processed": sum(len(history) for history in self.user_history.values()),
            "intent_patterns": {k: len(v) for k, v in self.patterns.items()}
        }