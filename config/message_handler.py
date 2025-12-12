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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📨 Message Handler - Process incoming messages
"""

import re
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

class MessageHandler:
    """Handles message processing and routing"""
    
    def __init__(self, bot_core):
        self.bot = bot_core
        self.logger = bot_core.logger
        self.config = bot_core.config
        
        # Command patterns
        self.command_patterns = {
            'prefix': re.compile(r'^\.(\w+)(?:\s+(.*))?$'),
            'admin': re.compile(r'^!(\w+)(?:\s+(.*))?$'),
            'stop': re.compile(r'^stop!$', re.IGNORECASE),
            'pause': re.compile(r'^pause!$', re.IGNORECASE),
            'resume': re.compile(r'^resume!$', re.IGNORECASE)
        }
        
        # Photo request keywords
        self.photo_keywords = {
            'bengali': ['ছবি', 'ফটো', 'চিত্র', 'ছবিটা', 'ফটোগ্রাফ'],
            'english': ['photo', 'pic', 'picture', 'image', 'img'],
            'request': ['দাও', 'চাই', 'পাঠাও', 'দেখাও', 'send', 'show', 'give']
        }
        
        # Greeting patterns
        self.greeting_patterns = [
            r'^(hi|hello|hey|hola|namaste|salam|salut)$',
            r'^(হাই|হ্যালো|হেলো|সালাম|নমস্কার|অভিবাদন)$',
            r'^(good\s+(morning|afternoon|evening|night))$',
            r'^(সুপ্রভাত|শুভ সকাল|শুভ দুপুর|শুভ সন্ধ্যা|শুভ রাত্রি)$'
        ]
        
        # Load response patterns
        self.response_patterns = self.load_response_patterns()
        
        self.logger.info("MessageHandler initialized")
    
    def load_response_patterns(self) -> Dict:
        """Load response patterns from JSON files"""
        patterns = {}
        json_dir = "data/json_responses"
        
        if not Path(json_dir).exists():
            return patterns
        
        for file in Path(json_dir).glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    key = file.stem
                    patterns[key] = {
                        'responses': data.get('responses', []),
                        'triggers': data.get('triggers', [])
                    }
            except Exception as e:
                self.logger.error(f"Error loading {file}: {e}")
        
        return patterns
    
    def process_message(self, message: str, user_id: str, chat_type: str = "private") -> Dict:
        """
        Process incoming message and return response
        
        Returns:
            Dict with keys: 'response', 'type', 'action', 'media_path'
        """
        message = message.strip()
        if not message:
            return self.create_response("Empty message received", "text")
        
        # Log message
        self.log_message(message, user_id, chat_type)
        
        # Check for stop/pause/resume commands first
        if self.is_control_command(message):
            return self.handle_control_command(message)
        
        # Check if it's a command
        if self.is_command(message):
            return self.handle_command(message, user_id, chat_type)
        
        # Check for photo request
        photo_type = self.detect_photo_request(message)
        if photo_type:
            return self.handle_photo_request(photo_type, user_id)
        
        # Check for greeting
        if self.is_greeting(message):
            return self.handle_greeting(message, user_id)
        
        # Check for farewell
        if self.is_farewell(message):
            return self.handle_farewell(message, user_id)
        
        # Check for question
        if self.is_question(message):
            return self.handle_question(message, user_id)
        
        # Check for romantic content
        if self.is_romantic(message):
            return self.handle_romantic(message, user_id)
        
        # Check for angry content
        if self.is_angry(message):
            return self.handle_angry(message, user_id)
        
        # Default response
        return self.handle_default(message, user_id)
    
    def is_control_command(self, message: str) -> bool:
        """Check if message is a control command"""
        message_lower = message.lower().strip()
        
        control_commands = ['stop!', 'pause!', 'resume!']
        return message_lower in control_commands
    
    def handle_control_command(self, message: str) -> Dict:
        """Handle control commands (stop, pause, resume)"""
        message_lower = message.lower().strip()
        
        if message_lower == 'stop!':
            if self.bot.sequential_active:
                self.bot.sequential_stop = True
                response = "🛑 Sequential command stopped!"
                action = "stop_sequence"
            else:
                response = "ℹ️ No active sequence to stop"
                action = None
        
        elif message_lower == 'pause!':
            if self.bot.sequential_active and not self.bot.sequential_pause:
                self.bot.sequential_pause = True
                response = "⏸️ Sequential command paused!"
                action = "pause_sequence"
            else:
                response = "ℹ️ No active sequence to pause"
                action = None
        
        elif message_lower == 'resume!':
            if self.bot.sequential_active and self.bot.sequential_pause:
                self.bot.sequential_pause = False
                response = "▶️ Sequential command resumed!"
                action = "resume_sequence"
            else:
                response = "ℹ️ No active sequence to resume"
                action = None
        
        else:
            response = "❌ Unknown control command"
            action = None
        
        return self.create_response(response, "text", action)
    
    def is_command(self, message: str) -> bool:
        """Check if message is a command"""
        message_stripped = message.strip()
        return message_stripped.startswith('.') or message_stripped.startswith('!')
    
    def handle_command(self, message: str, user_id: str, chat_type: str) -> Dict:
        """Handle command messages"""
        message_stripped = message.strip()
        
        # Parse command
        if message_stripped.startswith('.'):
            command_type = 'prefix'
            match = self.command_patterns['prefix'].match(message_stripped)
        else:  # starts with '!'
            command_type = 'admin'
            match = self.command_patterns['admin'].match(message_stripped)
        
        if not match:
            return self.create_response("❌ Invalid command format", "text")
        
        command = match.group(1).lower()
        args = match.group(2) if match.group(2) else ""
        
        # Check if command is enabled
        if not self.is_command_enabled(command, command_type):
            return self.create_response(f"❌ Command '{command}' is disabled", "text")
        
        # Check user permissions
        if not self.check_permissions(command, command_type, user_id, chat_type):
            return self.create_response("❌ Permission denied", "text")
        
        # Process command
        if command_type == 'prefix':
            return self.handle_prefix_command(command, args, user_id)
        else:  # admin command
            return self.handle_admin_command(command, args, user_id, chat_type)
    
    def is_command_enabled(self, command: str, command_type: str) -> bool:
        """Check if command is enabled in config"""
        if command_type == 'prefix':
            enabled_commands = self.config.get('commands', {}).get('enabled_commands', [])
            return command in enabled_commands
        else:  # admin command
            admin_commands = self.config.get('commands', {}).get('admin_commands', [])
            return command in admin_commands
    
    def check_permissions(self, command: str, command_type: str, user_id: str, chat_type: str) -> bool:
        """Check if user has permission to use command"""
        # For now, allow all prefix commands
        if command_type == 'prefix':
            return True
        
        # For admin commands, check if user is admin
        # In real implementation, check against admin list
        admin_ids = self.config.get('admins', [])
        
        # For testing, allow if user_id contains "admin" or is in list
        if 'admin' in user_id.lower() or user_id in admin_ids:
            return True
        
        # Allow certain admin commands for everyone in groups
        if chat_type == 'group' and command in ['add', 'kick']:
            return True
        
        return False
    
    def handle_prefix_command(self, command: str, args: str, user_id: str) -> Dict:
        """Handle prefix commands (starting with .)"""
        # Add user to recent users
        self.add_user_interaction(user_id, command)
        
        # Process specific commands
        if command == 'murgi':
            return self.handle_murgi_command(user_id)
        
        elif command == 'love':
            return self.handle_love_command(user_id)
        
        elif command == 'pick':
            return self.handle_pick_command(args, user_id)
        
        elif command == 'dio':
            return self.handle_dio_command(user_id)
        
        elif command == 'info':
            return self.handle_info_command(user_id)
        
        elif command == 'uid':
            return self.handle_uid_command(user_id)
        
        elif command == 'diagram':
            return self.handle_diagram_command(args, user_id)
        
        elif command == 'ln':
            return self.handle_ln_command(args, user_id)
        
        else:
            return self.create_response(f"❌ Unknown command: .{command}", "text")
    
    def handle_murgi_command(self, user_id: str) -> Dict:
        """Handle .murgi command"""
        # Start sequential murgi in background
        self.bot.sequential_active = True
        self.bot.sequential_stop = False
        self.bot.sequential_pause = False
        
        # Import threading here to avoid circular import
        import threading
        
        def run_murgi_sequence():
            """Run murgi sequence in background"""
            try:
                # Get murgi lines
                murgi_lines = self.bot.responses.get('murgi', [])
                
                if not murgi_lines:
                    self.logger.error("No murgi lines found")
                    return
                
                # Split into groups of 10
                groups = [murgi_lines[i:i+10] for i in range(0, len(murgi_lines), 10)]
                
                for group_num, group in enumerate(groups, 1):
                    if self.bot.sequential_stop:
                        break
                    
                    self.logger.info(f"Processing murgi group {group_num}")
                    
                    # Send each line with delay
                    for line_num, line in enumerate(group, 1):
                        if self.bot.sequential_stop:
                            break
                        
                        # Check for pause
                        while self.bot.sequential_pause and not self.bot.sequential_stop:
                            time.sleep(0.5)
                        
                        if self.bot.sequential_stop:
                            break
                        
                        # Simulate sending line (in real bot, send to Facebook)
                        self.logger.info(f"[MURGI {group_num}.{line_num}] {line}")
                        
                        # Delay between lines
                        time.sleep(2.0)
                    
                    # Delay between groups
                    if group_num < len(groups) and not self.bot.sequential_stop:
                        time.sleep(5.0)
                
                self.bot.sequential_active = False
                self.logger.info("Murgi sequence completed")
                
            except Exception as e:
                self.logger.error(f"Error in murgi sequence: {e}")
                self.bot.sequential_active = False
        
        # Start thread
        thread = threading.Thread(target=run_murgi_sequence, daemon=True)
        thread.start()
        
        return self.create_response(
            "🐔 Starting .murgi sequence...\n"
            "🛑 Use 'stop!' to stop\n"
            "⏸️ Use 'pause!' to pause\n"
            "▶️ Use 'resume!' to resume",
            "text",
            "start_sequence"
        )
    
    def handle_love_command(self, user_id: str) -> Dict:
        """Handle .love command"""
        responses = self.bot.responses.get('love', [])
        if not responses:
            response = "💖 তোমাকে অনেক ভালোবাসি!"
        else:
            response = random.choice(responses)
        
        return self.create_response(response, "text")
    
    def handle_pick_command(self, args: str, user_id: str) -> Dict:
        """Handle .pick command"""
        items = []
        
        if args:
            # Split by comma or space
            if ',' in args:
                items = [item.strip() for item in args.split(',') if item.strip()]
            else:
                items = [item.strip() for item in args.split() if item.strip()]
        
        # If no items provided, use default
        if not items:
            items = ["রেড", "ব্লু", "গ্রিন", "ইয়েলো", "পিঙ্ক", "পার্পল", "অরেঞ্জ"]
        
        # Pick random item
        choice = random.choice(items)
        
        # Get response templates
        templates = self.bot.responses.get('pick', [])
        if templates:
            template = random.choice(templates)
            response = template.replace('{}', choice)
        else:
            response = f"🎯 আমার পছন্দ: {choice}!"
        
        return self.create_response(response, "text")
    
    def handle_dio_command(self, user_id: str) -> Dict:
        """Handle .dio command"""
        responses = self.bot.responses.get('dio', [])
        if not responses:
            response = "🦸‍♂️ কনসাইস! ডিও এখানে!"
        else:
            response = random.choice(responses)
        
        return self.create_response(response, "text")
    
    def handle_info_command(self, user_id: str) -> Dict:
        """Handle .info command"""
        responses = self.bot.responses.get('info', [])
        if not responses:
            response = f"🤖 বট নাম: {self.bot.name}\n👑 ডেভেলপার: {self.bot.author}"
        else:
            response = random.choice(responses)
        
        return self.create_response(response, "text")
    
    def handle_uid_command(self, user_id: str) -> Dict:
        """Handle .uid command"""
        return self.create_response(f"👤 Your User ID: {user_id}", "text")
    
    def handle_diagram_command(self, args: str, user_id: str) -> Dict:
        """Handle .diagram command"""
        diagram_types = ['flowchart', 'sequence', 'mindmap', 'pie', 'bar']
        
        if args and args.lower() in diagram_types:
            diagram_type = args.lower()
        else:
            diagram_type = random.choice(diagram_types)
        
        diagrams = {
            'flowchart': "📊 ফ্লোচার্ট ডায়াগ্রাম তৈরি করা হলো!",
            'sequence': "🔄 সিকোয়েন্স ডায়াগ্রাম তৈরি করা হলো!",
            'mindmap': "🧠 মাইন্ডম্যাপ তৈরি করা হলো!",
            'pie': "🥧 পাই চার্ট তৈরি করা হলো!",
            'bar': "📈 বার চার্ট তৈরি করা হলো!"
        }
        
        response = diagrams.get(diagram_type, "📊 ডায়াগ্রাম তৈরি করা হলো!")
        return self.create_response(response, "text")
    
    def handle_ln_command(self, args: str, user_id: str) -> Dict:
        """Handle .Ln command"""
        try:
            if args:
                line_num = int(args)
                if 1 <= line_num <= 100:
                    response = f"📜 Line {line_num}: This is line number {line_num}"
                else:
                    response = f"❌ Line number must be between 1 and 100"
            else:
                response = "📜 Usage: .Ln <line_number>\nExample: .Ln 5"
        except ValueError:
            response = "❌ Invalid line number"
        
        return self.create_response(response, "text")
    
    def handle_admin_command(self, command: str, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle admin commands (starting with !)"""
        admin_commands = {
            'add': self.handle_add_command,
            'delete': self.handle_delete_command,
            'kick': self.handle_kick_command,
            'out': self.handle_out_command,
            'start': self.handle_start_command,
            'stop': self.handle_stop_admin_command
        }
        
        handler = admin_commands.get(command)
        if handler:
            return handler(args, user_id, chat_type)
        else:
            return self.create_response(f"❌ Unknown admin command: !{command}", "text")
    
    def handle_add_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !add command"""
        if chat_type == 'group' and args:
            response = f"✅ Added {args} to the group!"
        else:
            response = "➕ Add command executed!"
        
        return self.create_response(response, "text")
    
    def handle_delete_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !delete command"""
        if chat_type == 'group' and args:
            response = f"🗑️ Deleted {args} from the group!"
        else:
            response = "🗑️ Delete command executed!"
        
        return self.create_response(response, "text")
    
    def handle_kick_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !kick command"""
        if chat_type == 'group' and args:
            response = f"👢 Kicked {args} from the group!"
        else:
            response = "👢 Kick command executed!"
        
        return self.create_response(response, "text")
    
    def handle_out_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !out command"""
        if args == 'admin':
            response = "👑 Admin mode: Leaving group as admin!"
        else:
            response = "👋 Leaving the group!"
        
        return self.create_response(response, "text")
    
    def handle_start_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !start command"""
        if args == 'live':
            response = "📡 Live stream started!"
        else:
            response = "🚀 Bot started!"
        
        return self.create_response(response, "text")
    
    def handle_stop_admin_command(self, args: str, user_id: str, chat_type: str) -> Dict:
        """Handle !stop command"""
        if args == 'bot':
            response = "⏹️ Bot stopping..."
            action = "stop_bot"
        else:
            response = "🛑 Command stopped!"
            action = "stop_command"
        
        return self.create_response(response, "text", action)
    
    def detect_photo_request(self, message: str) -> Optional[str]:
        """Detect photo request in message"""
        message_lower = message.lower()
        
        # Check for photo keywords
        has_photo_word = any(word in message_lower for word in 
                           self.photo_keywords['bengali'] + self.photo_keywords['english'])
        
        has_request_word = any(word in message_lower for word in self.photo_keywords['request'])
        
        if not (has_photo_word or has_request_word):
            return None
        
        # Determine photo type
        if 'তোমার' in message_lower or 'your' in message_lower:
            return 'personal'
        elif 'বটের' in message_lower or 'bot' in message_lower:
            return 'bot'
        elif 'এডমিন' in message_lower or 'admin' in message_lower or 'মাস্টার' in message_lower:
            return 'admin'
        elif 'ফেসবুক' in message_lower or 'facebook' in message_lower:
            return 'facebook'
        else:
            return 'general'
    
    def handle_photo_request(self, photo_type: str, user_id: str) -> Dict:
        """Handle photo request"""
        # Get photo path based on type
        photo_path = None
        
        if photo_type == 'personal':
            photo_path = self.bot.get_photo_path('own')
            response = "👤 তোমার জন্য আমার ব্যক্তিগত ছবি!"
        elif photo_type == 'bot':
            photo_path = self.bot.get_photo_path('master')
            response = "🤖 এই নাও বটের ছবি!"
        elif photo_type == 'admin':
            photo_path = self.bot.get_photo_path('photo')
            response = "👑 এডমিনের ছবি পাঠাচ্ছি!"
        elif photo_type == 'facebook':
            response = "📘 ফেসবুক প্রোফাইল থেকে ছবি নেওয়া হচ্ছে!"
            # In real implementation, fetch from Facebook
        else:
            photo_path = self.bot.get_photo_path()
            response = "📸 তোমার জন্য একটি ছবি!"
        
        if photo_path and Path(photo_path).exists():
            return self.create_response(response, "photo", "send_photo", photo_path)
        else:
            return self.create_response("😔 দুঃখিত, এখন কোনো ছবি নেই!", "text")
    
    def is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        message_lower = message.lower().strip()
        
        for pattern in self.greeting_patterns:
            if re.match(pattern, message_lower, re.IGNORECASE):
                return True
        
        return False
    
    def handle_greeting(self, message: str, user_id: str) -> Dict:
        """Handle greeting messages"""
        # Use pattern-based responses if available
        if 'greetings' in self.response_patterns:
            responses = self.response_patterns['greetings']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        # Default greeting responses
        greetings = [
            "হ্যালো! 😊",
            "কেমন আছো? ✨",
            "হাই! আজকে কেমন যাচ্ছে? 💖",
            "নমস্কার! আমি তোমার ক্রাশ বট! 😘",
            "সালাম! সব ভালো? 🙏"
        ]
        
        response = random.choice(greetings)
        return self.create_response(response, "text")
    
    def is_farewell(self, message: str) -> bool:
        """Check if message is a farewell"""
        message_lower = message.lower()
        
        farewell_words = ['bye', 'goodbye', 'বিদায়', 'বাই', 'শুভ রাত্রি', 'good night', 'চললাম', 'যাই']
        return any(word in message_lower for word in farewell_words)
    
    def handle_farewell(self, message: str, user_id: str) -> Dict:
        """Handle farewell messages"""
        if 'farewells' in self.response_patterns:
            responses = self.response_patterns['farewells']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        farewells = [
            "বিদায়! খেয়াল রাখবে! 👋",
            "বাই! আবার কথা বলব! ✨",
            "শুভ রাত্রি! ভালো ঘুম! 🌙",
            "টাটা! কথা হবে! 💖",
            "যাও! আবার দেখা হবে! 🚀"
        ]
        
        response = random.choice(farewells)
        return self.create_response(response, "text")
    
    def is_question(self, message: str) -> bool:
        """Check if message is a question"""
        return '?' in message or any(word in message.lower() for word in 
                                   ['কী', 'কেন', 'কিভাবে', 'কখন', 'কোথায়', 'কে', 'কি',
                                    'what', 'why', 'how', 'when', 'where', 'who'])
    
    def handle_question(self, message: str, user_id: str) -> Dict:
        """Handle question messages"""
        if 'questions' in self.response_patterns:
            responses = self.response_patterns['questions']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        questions = [
            "ভালো প্রশ্ন! 🤔",
            "জানি না, তুমি কি মনে কর? 💭",
            "এটা জটিল প্রশ্ন! 🧠",
            "আমি ভাবতে হবে... ⏳",
            "তোমার মতামত কি? 👂"
        ]
        
        response = random.choice(questions)
        return self.create_response(response, "text")
    
    def is_romantic(self, message: str) -> bool:
        """Check if message has romantic content"""
        message_lower = message.lower()
        
        romantic_words = ['ভালোবাস', 'লাভ', 'love', 'প্রেম', 'ক্রাশ', 'মিস', 'miss', 
                         'হৃদয়', 'heart', 'রোমান্টিক', 'romantic', 'চুমু', 'kiss']
        
        return any(word in message_lower for word in romantic_words)
    
    def handle_romantic(self, message: str, user_id: str) -> Dict:
        """Handle romantic messages"""
        if 'romantic' in self.response_patterns:
            responses = self.response_patterns['romantic']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        romantic = [
            "তুমি আমার বিশেষ মানুষ! 💘",
            "তোমার কথা ভাবলে হাসি পায়! 😊",
            "তুমি ছাড়া জীবন অসম্পূর্ণ! 💔",
            "তোমার চোখে আকাশ দেখি! ✨",
            "তুমি আমার স্বপ্নের রানি/রাজা! 👑"
        ]
        
        response = random.choice(romantic)
        return self.create_response(response, "text")
    
    def is_angry(self, message: str) -> bool:
        """Check if message has angry content"""
        message_lower = message.lower()
        
        angry_words = ['রাগ', 'খারাপ', 'বিরক্ত', 'angry', 'bad', 'hate', 'ঘৃণা', 
                      'অসন্তুষ্ট', 'নিরাশ', 'frustrated', 'annoyed']
        
        return any(word in message_lower for word in angry_words)
    
    def handle_angry(self, message: str, user_id: str) -> Dict:
        """Handle angry messages"""
        if 'angry' in self.response_patterns:
            responses = self.response_patterns['angry']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        angry = [
            "এটা মেনে নেওয়া কঠিন! 😠",
            "আমি মন খারাপ করছি! 😞",
            "এটা ঠিক না! 🚫",
            "আমি রেগে গেছি! 🔥",
            "এটা বন্ধ করো! ✋"
        ]
        
        response = random.choice(angry)
        return self.create_response(response, "text")
    
    def handle_default(self, message: str, user_id: str) -> Dict:
        """Handle default/fallback messages"""
        if 'neutral' in self.response_patterns:
            responses = self.response_patterns['neutral']['responses']
            if responses:
                response = random.choice(responses)
                return self.create_response(response, "text")
        
        defaults = [
            "বলো! কি বলতে চাও? 💬",
            "আমি শুনছি... 👂",
            "আরো বলো... ✨",
            "বুঝলাম! কি করতে চাও? 🤔",
            "মজার কথা! 😄",
            "তোমার সাথে কথা বলে ভালো লাগছে! 💖",
            "আচ্ছা! এরপর? 🔄",
            "জানি না! 🤷",
            "চলতে থাকো! 🚶"
        ]
        
        response = random.choice(defaults)
        return self.create_response(response, "text")
    
    def create_response(self, text: str, response_type: str = "text", 
                       action: Optional[str] = None, media_path: Optional[str] = None) -> Dict:
        """Create a standardized response dictionary"""
        return {
            'response': text,
            'type': response_type,
            'action': action,
            'media_path': media_path,
            'timestamp': datetime.now().isoformat()
        }
    
    def log_message(self, message: str, user_id: str, chat_type: str):
        """Log message for learning and statistics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'chat_type': chat_type,
            'message': message,
            'length': len(message)
        }
        
        # Save to recent messages
        self.bot.command_history.append(log_entry)
        
        # Limit history size
        if len(self.bot.command_history) > 1000:
            self.bot.command_history = self.bot.command_history[-1000:]
        
        # Log to file
        self.logger.info(f"Message from {user_id} ({chat_type}): {message[:100]}...")
    
    def add_user_interaction(self, user_id: str, interaction_type: str):
        """Add user interaction for learning"""
        if user_id not in self.bot.user_data:
            self.bot.user_data[user_id] = {
                'interaction_count': 0,
                'last_interaction': datetime.now().isoformat(),
                'preferences': {},
                'command_usage': {}
            }
        
        user_data = self.bot.user_data[user_id]
        user_data['interaction_count'] += 1
        user_data['last_interaction'] = datetime.now().isoformat()
        
        # Track command usage
        if interaction_type:
            if 'command_usage' not in user_data:
                user_data['command_usage'] = {}
            
            user_data['command_usage'][interaction_type] = \
                user_data['command_usage'].get(interaction_type, 0) + 1

if __name__ == "__main__":
    print("Message Handler Module Loaded")
    
    # Test the handler
    from unittest.mock import Mock
    
    mock_bot = Mock()
    mock_bot.logger = Mock()
    mock_bot.logger.info = print
    mock_bot.logger.error = print
    mock_bot.config = {
        'commands': {
            'enabled_commands': ['murgi', 'love', 'pick', 'dio', 'info', 'uid'],
            'admin_commands': ['add', 'delete', 'kick', 'out', 'start', 'stop']
        }
    }
    mock_bot.responses = {
        'love': ['💖 Test love response'],
        'pick': ['🎯 Test pick response: {}'],
        'dio': ['🦸‍♂️ Test dio response'],
        'info': ['🤖 Test info response']
    }
    mock_bot.sequential_active = False
    mock_bot.sequential_stop = False
    mock_bot.sequential_pause = False
    mock_bot.command_history = []
    mock_bot.user_data = {}
    
    handler = MessageHandler(mock_bot)
    
    test_messages = [
        ".murgi",
        ".love",
        ".pick red,blue,green",
        "ছবি দাও",
        "হাই",
        "বিদায়",
        "তুমি কেমন আছো?",
        "আমি তোমাকে ভালোবাসি",
        "আমি রেগে আছি",
        "হ্যালো ওয়ার্ল্ড"
    ]
    
    print("\n🧪 Testing Message Handler:")
    print("="*50)
    
    for msg in test_messages:
        result = handler.process_message(msg, "test_user_123")
        print(f"💬 Input: {msg}")
        print(f"🤖 Response: {result['response'][:50]}...")
        print()