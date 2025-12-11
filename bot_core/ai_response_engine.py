#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AI Response Engine
Generates intelligent responses using learning system
"""

import json
import logging
import random
import re
from typing import Dict, List, Optional, Any

from utils.logger import setup_logger
from utils.text_processor import TextProcessor


class AIResponseEngine:
    """🧠 AI Response Engine"""
    
    def __init__(self):
        self.logger = setup_logger("ai_response_engine", "data/logs/bot_activity.log")
        self.text_processor = TextProcessor()
        
        # Load JSON responses
        self.responses = self._load_responses()
        
        # Response templates
        self.templates = {
            "greeting": ["হ্যালো!", "কেমন আছো?", "আপনি কেমন আছেন?"],
            "farewell": ["বিদায়!", "শুভ রাত্রি!", "আবার দেখা হবে!"],
            "question": ["জানি না", "আমি নিশ্চিত নই", "এটা ভালো প্রশ্ন"],
            "compliment": ["ধন্যবাদ!", "তুমিও খুব সুন্দর!", "আমি খুশি!"],
            "romantic": ["তোমাকে ভালোবাসি!", "তুমি আমার বিশেষ!", "তোমার জন্য আমার মন কাঁদে!"],
            "neutral": ["বুঝেছি", "ওহ", "হুম"]
        }
        
        # Personality settings
        self.personality = {
            "romantic_level": "high",
            "friendliness": "high",
            "humor": "medium",
            "formality": "low"
        }
        
        # Context memory
        self.context_memory = {}
    
    def _load_responses(self) -> Dict:
        """Load JSON responses from files"""
        responses = {}
        
        response_files = {
            "greetings": "data/json_responses/greetings.json",
            "farewells": "data/json_responses/farewells.json",
            "questions": "data/json_responses/questions.json",
            "compliments": "data/json_responses/compliments.json",
            "romantic": "data/json_responses/romantic.json",
            "neutral": "data/json_responses/neutral.json"
        }
        
        for category, file_path in response_files.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    responses[category] = json.load(f)
            except FileNotFoundError:
                self.logger.warning(f"⚠️ Response file not found: {file_path}")
                responses[category] = {"responses": [], "triggers": []}
            except json.JSONDecodeError:
                self.logger.error(f"❌ Error parsing JSON: {file_path}")
                responses[category] = {"responses": [], "triggers": []}
        
        return responses
    
    def generate_response(self, message: str, user_id: str, context: Dict = None) -> str:
        """Generate AI response for a message"""
        try:
            message_lower = message.lower().strip()
            
            # Get user context
            if context is None:
                context = self._get_user_context(user_id)
            
            # Check for specific patterns first
            response = self._check_specific_patterns(message_lower, user_id)
            if response:
                return response
            
            # Check JSON responses
            response = self._check_json_responses(message_lower)
            if response:
                return response
            
            # Generate context-aware response
            response = self._generate_context_response(message, user_id, context)
            
            # Add personality flavor
            response = self._add_personality(response)
            
            # Update context
            self._update_context(user_id, message, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return self._get_fallback_response()
    
    def _check_specific_patterns(self, message: str, user_id: str) -> Optional[str]:
        """Check for specific message patterns"""
        # Greetings
        greetings = ["হাই", "হ্যালো", "hello", "hi", "hey", "নমস্কার", "সালাম", "কেমন আছো", "কেমন আছেন"]
        for greeting in greetings:
            if greeting in message:
                return random.choice(self.templates["greeting"])
        
        # Farewells
        farewells = ["বিদায়", "bye", "goodbye", "see you", "চলে যাই", "শুভ রাত্রি", "good night"]
        for farewell in farewells:
            if farewell in message:
                return random.choice(self.templates["farewell"])
        
        # Questions
        question_words = ["কি", "কেন", "কিভাবে", "কখন", "কোথায়", "কে", "what", "why", "how", "when", "where", "who"]
        if any(word in message for word in question_words) and "?" in message:
            return random.choice(self.templates["question"])
        
        # Compliments
        compliments = ["সুন্দর", "ভালো", "চমৎকার", "অসাধারণ", "beautiful", "good", "nice", "awesome", "great"]
        for compliment in compliments:
            if compliment in message:
                return random.choice(self.templates["compliment"])
        
        # Romantic
        romantic_words = ["ভালোবাসা", "লাভ", "প্রেম", "crush", "love", "romantic", "heart"]
        for word in romantic_words:
            if word in message:
                return random.choice(self.templates["romantic"])
        
        return None
    
    def _check_json_responses(self, message: str) -> Optional[str]:
        """Check JSON responses for matches"""
        try:
            for category, data in self.responses.items():
                if "triggers" in data and data["triggers"]:
                    for trigger in data["triggers"]:
                        if trigger.lower() in message:
                            if "responses" in data and data["responses"]:
                                return random.choice(data["responses"])
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error checking JSON responses: {e}")
            return None
    
    def _generate_context_response(self, message: str, user_id: str, context: Dict) -> str:
        """Generate context-aware response"""
        try:
            # Get last conversation
            last_message = context.get("last_message", "")
            last_response = context.get("last_response", "")
            
            # Simple context continuation
            if last_message and last_response:
                # Check if this is a follow-up
                follow_up_words = ["হ্যাঁ", "না", "ঠিক আছে", "ওকে", "yes", "no", "ok", "okay"]
                if any(word in message.lower() for word in follow_up_words):
                    return self._generate_followup_response(message, context)
            
            # Check for topic continuation
            topics = context.get("topics", [])
            if topics:
                last_topic = topics[-1] if topics else ""
                if last_topic and last_topic in message.lower():
                    return self._continue_topic(last_topic)
            
            # Generate new response based on message content
            return self._generate_based_on_content(message)
            
        except Exception as e:
            self.logger.error(f"❌ Error generating context response: {e}")
            return self._get_fallback_response()
    
    def _generate_followup_response(self, message: str, context: Dict) -> str:
        """Generate follow-up response"""
        responses = [
            "বুঝেছি!",
            "ওকে!",
            "ভালো!",
            "চমৎকার!",
            "আমি খুশি!",
            "জানি!"
        ]
        return random.choice(responses)
    
    def _continue_topic(self, topic: str) -> str:
        """Continue a topic"""
        topic_responses = {
            "খাবার": ["খাবার নিয়ে কথা বলতে ভালো লাগে!", "তুমি কি রান্না করতে জানো?", "আমি বিরিয়ানি ভালোবাসি!"],
            "গান": ["গান শুনতে আমারও ভালো লাগে!", "তোমার প্রিয় গান কি?", "আমি রোমান্টিক গান পছন্দ করি!"],
            "সিনেমা": ["সিনেমা দেখা তোমার প্রিয়?", "তোমার প্রিয় সিনেমা কি?", "আমি একশন সিনেমা পছন্দ করি!"],
            "খেলা": ["তুমি কি খেলা খেলতে পছন্দ করো?", "ফুটবল নাকি ক্রিকেট?", "আমি গেমিং ভালোবাসি!"]
        }
        
        if topic in topic_responses:
            return random.choice(topic_responses[topic])
        else:
            return f"{topic} নিয়ে আরো বলো!"
    
    def _generate_based_on_content(self, message: str) -> str:
        """Generate response based on message content"""
        # Simple keyword matching
        keywords = {
            "খাবার": ["আমি খিদে পেয়েছে!", "তুমি কি খেয়েছ?", "খাবার কথা বললে আমার খিদে পায়!"],
            "ঘুম": ["ঘুম আসছে!", "তুমি কি ঘুমিয়েছ?", "গভীর ঘুম খুব গুরুত্বপূর্ণ!"],
            "কাজ": ["কাজ করছি!", "তোমার কাজ কি?", "আমি সব সময় কাজ করতে পছন্দ করি!"],
            "মনে": ["আমি তোমাকে মনে রাখবো!", "তুমি আমার মনে আছো!", "সব সময় তোমাকে মনে পড়ে!"],
            "সময়": ["সময় দ্রুত চলে যায়!", "সময়ের গুরুত্ব আছে!", "সময়ের সাথে সব পরিবর্তন হয়!"]
        }
        
        for keyword, responses in keywords.items():
            if keyword in message:
                return random.choice(responses)
        
        # Default responses based on message length
        if len(message) < 10:
            responses = ["হুম", "ওহ", "বুঝেছি", "জানি"]
        elif len(message) < 50:
            responses = ["তুমি ঠিক বলেছ!", "আমি একমত!", "ভালো বলেছ!", "আমি শুনছি!"]
        else:
            responses = ["তুমি অনেক কিছু বললে!", "বিস্তারিত বলার জন্য ধন্যবাদ!", "আমি সব শুনেছি!", "বুঝতে পারছি!"]
        
        return random.choice(responses)
    
    def _add_personality(self, response: str) -> str:
        """Add personality to response"""
        # Add romantic flavor if enabled
        if self.personality["romantic_level"] == "high":
            romantic_phrases = ["💖", "❤️", "😘", "💕"]
            if random.random() > 0.7:  # 30% chance
                response = f"{response} {random.choice(romantic_phrases)}"
        
        # Add friendly tone
        if self.personality["friendliness"] == "high":
            friendly_words = ["প্রিয়", "ভাই", "বন্ধু", "শুভাকাঙ্ক্ষী"]
            if random.random() > 0.8:  # 20% chance
                word = random.choice(friendly_words)
                response = f"{word}, {response}"
        
        # Add humor
        if self.personality["humor"] == "medium" and random.random() > 0.9:  # 10% chance
            funny_emojis = ["😄", "😂", "😁", "🤣"]
            response = f"{response} {random.choice(funny_emojis)}"
        
        return response
    
    def _get_user_context(self, user_id: str) -> Dict:
        """Get user context from memory"""
        if user_id in self.context_memory:
            return self.context_memory[user_id]
        else:
            return {
                "last_message": "",
                "last_response": "",
                "topics": [],
                "mood": "neutral",
                "interaction_count": 0
            }
    
    def _update_context(self, user_id: str, message: str, response: str):
        """Update user context"""
        if user_id not in self.context_memory:
            self.context_memory[user_id] = {
                "last_message": "",
                "last_response": "",
                "topics": [],
                "mood": "neutral",
                "interaction_count": 0
            }
        
        context = self.context_memory[user_id]
        context["last_message"] = message
        context["last_response"] = response
        context["interaction_count"] += 1
        
        # Extract topics from message
        topics = self._extract_topics(message)
        if topics:
            context["topics"].extend(topics)
            # Keep only last 5 topics
            context["topics"] = context["topics"][-5:]
        
        # Update mood
        context["mood"] = self._detect_mood(message)
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message"""
        topics = []
        
        # Simple keyword matching for topics
        topic_keywords = {
            "খাবার": ["খাবার", "খিদে", "রান্না", "ভাত", "বিরিয়ানি"],
            "গান": ["গান", "সঙ্গীত", "মিউজিক", "গায়ক"],
            "সিনেমা": ["সিনেমা", "মুভি", "অভিনেতা", "অভিনেত্রী"],
            "খেলা": ["খেলা", "স্পোর্টস", "ফুটবল", "ক্রিকেট", "গেম"],
            "পড়াশুনা": ["পড়াশুনা", "স্টাডি", "স্কুল", "কলেজ", "বিশ্ববিদ্যালয়"],
            "কাজ": ["কাজ", "জব", "অফিস", "প্রোজেক্ট"]
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    topics.append(topic)
                    break
        
        return list(set(topics))  # Remove duplicates
    
    def _detect_mood(self, message: str) -> str:
        """Detect mood from message"""
        message_lower = message.lower()
        
        happy_words = ["খুশি", "আনন্দ", "হাসি", "মজা", "ভালো", "happy", "joy", "smile", "fun", "good"]
        sad_words = ["দুঃখ", "কষ্ট", "কান্না", "বিষণ্ণ", "খারাপ", "sad", "cry", "unhappy", "bad"]
        angry_words = ["রাগ", "ক্রোধ", "ঝগড়া", "angry", "mad", "fight", "hate"]
        
        happy_count = sum(1 for word in happy_words if word in message_lower)
        sad_count = sum(1 for word in sad_words if word in message_lower)
        angry_count = sum(1 for word in angry_words if word in message_lower)
        
        if angry_count > 0:
            return "angry"
        elif sad_count > happy_count:
            return "sad"
        elif happy_count > 0:
            return "happy"
        else:
            return "neutral"
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when all else fails"""
        fallback_responses = [
            "বুঝেছি!",
            "ওকে!",
            "হুম!",
            "আমি শুনছি!",
            "তুমি ঠিক বলেছ!",
            "ভালো!",
            "চমৎকার!"
        ]
        return random.choice(fallback_responses)
    
    def learn_from_response(self, user_id: str, user_message: str, bot_response: str, was_good: bool = True):
        """Learn from a response interaction"""
        try:
            # Store in learning data
            learning_file = "data/learning/learned_responses.json"
            
            # Load existing data
            try:
                with open(learning_file, "r", encoding="utf-8") as f:
                    learning_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                learning_data = {"responses": []}
            
            # Add new learning
            learning_entry = {
                "user_id": user_id,
                "user_message": user_message,
                "bot_response": bot_response,
                "was_good": was_good,
                "timestamp": time.time()
            }
            
            learning_data["responses"].append(learning_entry)
            
            # Keep only last 1000 entries
            if len(learning_data["responses"]) > 1000:
                learning_data["responses"] = learning_data["responses"][-1000:]
            
            # Save back
            with open(learning_file, "w", encoding="utf-8") as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Learned from response: {user_message[:50]}...")
            
        except Exception as e:
            self.logger.error(f"❌ Error learning from response: {e}")
    
    def get_engine_stats(self) -> Dict:
        """Get AI engine statistics"""
        return {
            "response_categories": len(self.responses),
            "context_memory_size": len(self.context_memory),
            "personality": self.personality,
            "total_templates": sum(len(templates) for templates in self.templates.values())
        }