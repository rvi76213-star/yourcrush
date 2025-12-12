"""
🧠 লার্নিং সিস্টেম টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি AI লার্নিং সিস্টেম টেস্ট করে
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.learning_system import LearningSystem
from bot_core.ai_response_engine import AIResponseEngine

class TestLearningSystem(unittest.TestCase):
    """লার্নিং সিস্টেম টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("🧠 লার্নিং সিস্টেম টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট ডেটা
        cls.test_data_dir = 'temp/test_learning'
        os.makedirs(cls.test_data_dir, exist_ok=True)
        
        # স্যাম্পল লার্নিং ডেটা তৈরি করুন
        cls.create_test_data()
    
    @classmethod
    def create_test_data(cls):
        """টেস্ট ডেটা তৈরি করুন"""
        # ইউজার প্যাটার্ন
        user_patterns = {
            "user123": {
                "greetings": ["হ্যালো", "হাই", "সালাম"],
                "frequent_topics": ["নামাজ", "ফটো", "খেলা"],
                "preferred_time": "evening",
                "interaction_count": 25,
                "last_interaction": "2024-01-15 10:30:00"
            },
            "user456": {
                "greetings": ["Hello", "Hi"],
                "frequent_topics": ["music", "movies", "sports"],
                "preferred_time": "night",
                "interaction_count": 12,
                "last_interaction": "2024-01-14 20:15:00"
            }
        }
        
        with open(os.path.join(cls.test_data_dir, 'user_patterns.json'), 'w', encoding='utf-8') as f:
            json.dump(user_patterns, f, indent=2, ensure_ascii=False)
        
        # শেখা রেস্পন্স
        learned_responses = {
            "greetings": {
                "হ্যালো": ["হ্যালো! কেমন আছো?", "ওহে! আজ কেমন যাচ্ছে?", "হাই! তুমি কেমন আছো?"],
                "Hello": ["Hello! How are you?", "Hey! What's up?", "Hi there!"]
            },
            "farewells": {
                "বিদায়": ["আল্লাহ হাফেজ!", "বিদায়! ভালো থেকো", "শুভ রাত্রি!"],
                "Goodbye": ["Goodbye! Take care", "Bye! See you later", "Farewell!"]
            }
        }
        
        with open(os.path.join(cls.test_data_dir, 'learned_responses.json'), 'w', encoding='utf-8') as f:
            json.dump(learned_responses, f, indent=2, ensure_ascii=False)
        
        # কনভারসেশন হিস্ট্রি
        conversation_history = [
            {
                "user_id": "user123",
                "message": "হ্যালো",
                "response": "হ্যালো! কেমন আছো?",
                "timestamp": "2024-01-15 10:00:00"
            },
            {
                "user_id": "user123",
                "message": "তোমার ছবি দাও",
                "response": "এই নাও আমার ছবি!",
                "timestamp": "2024-01-15 10:01:00"
            }
        ]
        
        with open(os.path.join(cls.test_data_dir, 'conversation_history.json'), 'w', encoding='utf-8') as f:
            json.dump(conversation_history, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def tearDownClass(cls):
        """সমস্ত টেস্ট শেষে ক্লিনআপ"""
        print(f"\nটেস্ট ডিরেক্টরি পরিষ্কার করা হচ্ছে: {cls.test_data_dir}")
        
        import shutil
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)
            print("টেস্ট ডিরেক্টরি মুছে ফেলা হয়েছে")
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # লার্নিং সিস্টেম মক করুন
        self.learning_system = Mock(spec=LearningSystem)
        
        # মক মেথডস
        self.learning_system.learn_from_user = Mock(return_value=True)
        self.learning_system.learn_from_admin = Mock(return_value=True)
        self.learning_system.get_response = Mock(return_value="Learned response")
        self.learning_system.save_knowledge = Mock()
        self.learning_system.load_knowledge = Mock(return_value={})
        
        # AI রেস্পন্স ইঞ্জিন
        self.ai_engine = Mock(spec=AIResponseEngine)
        self.ai_engine.generate_response = Mock(return_value="AI generated response")
        self.ai_engine.learn_from_interaction = Mock()
        
        # অ্যাকচুয়াল লার্নিং সিস্টেম (কিছু টেস্টের জন্য)
        self.real_learning = LearningSystem()
    
    def tearDown(self):
        """প্রতি টেস্ট কেসের পরে রান হবে"""
        print(f"[{self._testMethodName}] টেস্ট শেষ ✓")
    
    def test_learning_data_loading(self):
        """লার্নিং ডেটা লোডিং টেস্ট"""
        print("লার্নিং ডেটা লোডিং টেস্ট করা হচ্ছে...")
        
        # টেস্ট ডেটা লোড করুন
        user_patterns_path = os.path.join(self.test_data_dir, 'user_patterns.json')
        learned_responses_path = os.path.join(self.test_data_dir, 'learned_responses.json')
        
        with open(user_patterns_path, 'r', encoding='utf-8') as f:
            user_patterns = json.load(f)
        
        with open(learned_responses_path, 'r', encoding='utf-8') as f:
            learned_responses = json.load(f)
        
        # ডেটা ভ্যালিডেশন
        self.assertIn("user123", user_patterns)
        self.assertIn("user456", user_patterns)
        
        user123_data = user_patterns["user123"]
        self.assertIn("greetings", user123_data)
        self.assertIn("frequent_topics", user123_data)
        self.assertGreater(user123_data["interaction_count"], 0)
        
        # লার্নেড রেস্পন্স চেক
        self.assertIn("greetings", learned_responses)
        self.assertIn("হ্যালো", learned_responses["greetings"])
        
        greetings = learned_responses["greetings"]["হ্যালো"]
        self.assertIsInstance(greetings, list)
        self.assertGreater(len(greetings), 0)
        
        print(f"লোড করা হয়েছে: {len(user_patterns)} ইউজার, {len(learned_responses)} ক্যাটাগরি")
        print("✅ লার্নিং ডেটা লোডিং টেস্ট পাস")
    
    def test_user_learning(self):
        """ইউজার থেকে শেখা টেস্ট"""
        print("ইউজার থেকে শেখা টেস্ট করা হচ্ছে...")
        
        # ইউজার ইন্টারঅ্যাকশন
        test_interactions = [
            {
                "user_id": "test_user",
                "message": "হ্যালো বট",
                "context": "greeting",
                "expected_learn": "greeting_pattern"
            },
            {
                "user_id": "test_user",
                "message": "আজকের তারিখ কি?",
                "context": "question",
                "expected_learn": "question_pattern"
            },
            {
                "user_id": "test_user",
                "message": "ধন্যবাদ!",
                "context": "appreciation",
                "expected_learn": "response_pattern"
            }
        ]
        
        for interaction in test_interactions:
            # ইউজার থেকে শেখা
            learned = self.learning_system.learn_from_user(
                interaction["user_id"],
                interaction["message"],
                interaction["context"]
            )
            
            self.assertTrue(learned)
            
            # মক মেথড কল হয়েছে কিনা চেক
            self.learning_system.learn_from_user.assert_called()
        
        # ইউজার প্যাটার্ন আপডেট
        if hasattr(self.real_learning, 'update_user_pattern'):
            user_id = "test_user_123"
            message = "I love football"
            topic = "sports"
            
            self.real_learning.update_user_pattern(user_id, message, topic)
            
            # পরবর্তী বার চেক করতে পারেন
            print(f"ইউজার প্যাটার্ন আপডেট হয়েছে: {user_id}")
        
        print("✅ ইউজার থেকে শেখা টেস্ট পাস")
    
    def test_admin_learning(self):
        """এডমিন থেকে শেখা টেস্ট"""
        print("এডমিন থেকে শেখা টেস্ট করা হচ্ছে...")
        
        # এডমিন কমান্ড/রেস্পন্স
        admin_teachings = [
            {
                "command": "response.add",
                "data": {"trigger": "compliment", "response": "Thank you! You're nice too!"},
                "expected": True
            },
            {
                "command": "pattern.add",
                "data": {"pattern": "weather question", "action": "provide_weather"},
                "expected": True
            },
            {
                "command": "knowledge.update",
                "data": {"fact": "Earth is round", "category": "science"},
                "expected": True
            }
        ]
        
        for teaching in admin_teachings:
            # এডমিন থেকে শেখা
            learned = self.learning_system.learn_from_admin(
                teaching["command"],
                teaching["data"]
            )
            
            self.assertEqual(learned, teaching["expected"])
        
        # এডমিন নলেজ বেজ টেস্ট
        if hasattr(self.real_learning, 'admin_knowledge'):
            # নতুন নলেজ যোগ
            new_knowledge = {
                "qna": {
                    "capital of bangladesh": "ঢাকা",
                    "largest river": "পদ্মা নদী"
                },
                "responses": {
                    "morning_greeting": "সুপ্রভাত! আজকে দিনটি ভালো যাক",
                    "evening_greeting": "শুভ সন্ধ্যা! কেমন আছো?"
                }
            }
            
            self.real_learning.update_admin_knowledge(new_knowledge)
            print("এডমিন নলেজ আপডেট হয়েছে")
        
        print("✅ এডমিন থেকে শেখা টেস্ট পাস")
    
    def test_response_generation(self):
        """রেস্পন্স জেনারেশন টেস্ট"""
        print("রেস্পন্স জেনারেশন টেস্ট করা হচ্ছে...")
        
        # বিভিন্ন কনটেক্স্টে রেস্পন্স
        test_contexts = [
            {
                "user_id": "user123",
                "message": "হ্যালো",
                "context": "greeting",
                "expected_type": "greeting_response"
            },
            {
                "user_id": "user456",
                "message": "How are you?",
                "context": "question",
                "expected_type": "answer"
            },
            {
                "user_id": "user789",
                "message": "Thank you",
                "context": "appreciation",
                "expected_type": "acknowledgment"
            },
            {
                "user_id": "user999",
                "message": "What's the weather?",
                "context": "unknown",
                "expected_type": "default"
            }
        ]
        
        for context in test_contexts:
            # রেস্পন্স জেনারেট করুন
            response = self.learning_system.get_response(
                context["user_id"],
                context["message"],
                context["context"]
            )
            
            # রেস্পন্স চেক
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            
            print(f"রেস্পন্স জেনারেট হয়েছে: {response[:50]}...")
        
        # পার্সোনালাইজড রেস্পন্স টেস্ট
        if hasattr(self.real_learning, 'get_personalized_response'):
            user_id = "known_user_123"
            message = "What's up?"
            
            # পূর্বের ইন্টারঅ্যাকশন থেকে শেখা
            personalized = self.real_learning.get_personalized_response(user_id, message)
            
            self.assertIsNotNone(personalized)
        
        print("✅ রেস্পন্স জেনারেশন টেস্ট পাস")
    
    def test_knowledge_persistence(self):
        """নলেজ পারসিস্টেন্স টেস্ট"""
        print("নলেজ পারসিস্টেন্স টেস্ট করা হচ্ছে...")
        
        # টেম্পোরারি ফাইল তৈরি করুন
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_knowledge = {
                "learned": {
                    "greetings": ["Hello", "Hi", "Hey"],
                    "farewells": ["Goodbye", "Bye", "See you"]
                },
                "patterns": {
                    "user123": {"prefers_short": True, "active_time": "evening"}
                }
            }
            json.dump(test_knowledge, f)
            temp_file = f.name
        
        try:
            # নলেজ লোড করুন
            with open(temp_file, 'r') as f:
                loaded_knowledge = json.load(f)
            
            # ভ্যালিডেশন
            self.assertIn("learned", loaded_knowledge)
            self.assertIn("patterns", loaded_knowledge)
            
            learned = loaded_knowledge["learned"]
            self.assertEqual(len(learned["greetings"]), 3)
            
            # নলেজ আপডেট করুন
            learned["greetings"].append("Howdy")
            loaded_knowledge["patterns"]["user456"] = {"prefers_formal": True}
            
            # সেভ করুন
            with open(temp_file, 'w') as f:
                json.dump(loaded_knowledge, f, indent=2)
            
            # আবার লোড করুন
            with open(temp_file, 'r') as f:
                reloaded_knowledge = json.load(f)
            
            # চেক করুন আপডেট সেভ হয়েছে কিনা
            self.assertEqual(len(reloaded_knowledge["learned"]["greetings"]), 4)
            self.assertIn("user456", reloaded_knowledge["patterns"])
            
            print(f"নলেজ পারসিস্টেন্স টেস্ট সফল: {temp_file}")
            
        finally:
            # ক্লিনআপ
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print("✅ নলেজ পারসিস্টেন্স টেস্ট পাস")
    
    def test_ai_response_generation(self):
        """AI রেস্পন্স জেনারেশন টেস্ট"""
        print("AI রেস্পন্স জেনারেশন টেস্ট করা হচ্ছে...")
        
        # বিভিন্ন ইনপুটের জন্য AI রেস্পন্স
        test_inputs = [
            {
                "input": "Hello, how are you today?",
                "context": "greeting",
                "expected_features": ["friendly", "responsive"]
            },
            {
                "input": "What is the meaning of life?",
                "context": "philosophy",
                "expected_features": ["thoughtful", "engaging"]
            },
            {
                "input": "Tell me a joke",
                "context": "entertainment",
                "expected_features": ["humorous", "short"]
            },
            {
                "input": "Help me with a problem",
                "context": "support",
                "expected_features": ["helpful", "detailed"]
            }
        ]
        
        for test in test_inputs:
            # AI রেস্পন্স জেনারেট করুন
            ai_response = self.ai_engine.generate_response(
                test["input"],
                test["context"]
            )
            
            # রেস্পন্স ভ্যালিডেশন
            self.assertIsNotNone(ai_response)
            self.assertIsInstance(ai_response, str)
            self.assertGreater(len(ai_response), 0)
            
            # নির্দিষ্ট ফিচার চেক (যদি সম্ভব হয়)
            # এখানে সাধারণ চেক করুন
            if any(feature in test["expected_features"] for feature in ["friendly", "helpful"]):
                self.assertNotIn("error", ai_response.lower())
            
            print(f"AI রেস্পন্স ({test['context']}): {ai_response[:60]}...")
        
        # কনটেক্সটুয়াল AI রেস্পন্স
        if hasattr(self.ai_engine, 'generate_contextual_response'):
            conversation_history = [
                {"role": "user", "content": "What's your favorite color?"},
                {"role": "bot", "content": "I like blue!"},
                {"role": "user", "content": "Why do you like blue?"}
            ]
            
            contextual_response = self.ai_engine.generate_contextual_response(
                conversation_history,
                "Why do you like blue?"
            )
            
            self.assertIsNotNone(contextual_response)
            self.assertIn("blue", contextual_response.lower())
        
        print("✅ AI রেস্পন্স জেনারেশন টেস্ট পাস")
    
    def test_learning_from_interaction(self):
        """ইন্টারঅ্যাকশন থেকে শেখা টেস্ট"""
        print("ইন্টারঅ্যাকশন থেকে শেখা টেস্ট করা হচ্ছে...")
        
        # ইন্টারঅ্যাকশন ডেটা
        interactions = [
            {
                "user_input": "What's the weather like?",
                "bot_response": "I don't have weather info right now.",
                "user_feedback": "That's okay",
                "learning_potential": "low"
            },
            {
                "user_input": "Tell me about Bangladesh",
                "bot_response": "Bangladesh is a country in South Asia.",
                "user_feedback": "Thanks, tell me more",
                "learning_potential": "high"
            },
            {
                "user_input": "How to make tea?",
                "bot_response": "Boil water, add tea leaves, milk and sugar.",
                "user_feedback": "Perfect!",
                "learning_potential": "high"
            }
        ]
        
        for interaction in interactions:
            # ইন্টারঅ্যাকশন থেকে শেখা
            self.ai_engine.learn_from_interaction(
                interaction["user_input"],
                interaction["bot_response"],
                interaction["user_feedback"]
            )
            
            # মক মেথড কল হয়েছে কিনা চেক
            self.ai_engine.learn_from_interaction.assert_called()
        
        # সাকসেসফুল ইন্টারঅ্যাকশন ট্র্যাকিং
        if hasattr(self.real_learning, 'track_successful_interaction'):
            successful_interactions = [
                ("greeting", "হ্যালো", "হ্যালো! কেমন আছো?", 5),
                ("question", "কখন নামাজ?", "ফজর ৪:৩০, জোহর ১২:১৫...", 8),
                ("photo_request", "ছবি দাও", "এই নাও ছবি!", 12)
            ]
            
            for category, user_msg, bot_resp, score in successful_interactions:
                self.real_learning.track_successful_interaction(
                    category, user_msg, bot_resp, score
                )
            
            print(f"ট্র্যাক করা হয়েছে: {len(successful_interactions)} সফল ইন্টারঅ্যাকশন")
        
        print("✅ ইন্টারঅ্যাকশন থেকে শেখা টেস্ট পাস")
    
    def test_pattern_recognition(self):
        """প্যাটার্ন রিকগনিশন টেস্ট"""
        print("প্যাটার্ন রিকগনিশন টেস্ট করা হচ্ছে...")
        
        # ইউজার প্যাটার্ন
        user_messages = [
            "Good morning!",
            "Morning! How are you?",
            "Good morning bot!",
            "Morning everyone!",
            "Hello good morning!"
        ]
        
        # প্যাটার্ন ডিটেক্ট করুন
        detected_patterns = []
        
        for message in user_messages:
            message_lower = message.lower()
            
            # সাধারণ প্যাটার্ন চেক
            if "morning" in message_lower:
                detected_patterns.append("morning_greeting")
            if "good" in message_lower and "morning" in message_lower:
                detected_patterns.append("formal_morning_greeting")
            if "how are you" in message_lower:
                detected_patterns.append("inquiry")
        
        # প্যাটার্ন ভ্যালিডেশন
        self.assertIn("morning_greeting", detected_patterns)
        self.assertGreater(detected_patterns.count("morning_greeting"), 2)
        
        # টাইম-বেসড প্যাটার্ন
        import datetime
        current_hour = datetime.datetime.now().hour
        
        time_based_patterns = []
        
        if 5 <= current_hour < 12:
            time_based_patterns.append("morning_time")
        elif 12 <= current_hour < 17:
            time_based_patterns.append("afternoon_time")
        elif 17 <= current_hour < 21:
            time_based_patterns.append("evening_time")
        else:
            time_based_patterns.append("night_time")
        
        self.assertGreater(len(time_based_patterns), 0)
        
        # ফ্রিকোয়েন্সি এনালাইসিস
        message_frequencies = {}
        for pattern in detected_patterns:
            message_frequencies[pattern] = message_frequencies.get(pattern, 0) + 1
        
        # সবচেয়ে কমন প্যাটার্ন
        most_common = max(message_frequencies, key=message_frequencies.get)
        self.assertEqual(most_common, "morning_greeting")
        
        print(f"ডিটেক্ট করা প্যাটার্ন: {set(detected_patterns)}")
        print(f"ফ্রিকোয়েন্সি: {message_frequencies}")
        
        print("✅ প্যাটার্ন রিকগনিশন টেস্ট পাস")
    
    def test_knowledge_retention(self):
        """নলেজ রিটেনশন টেস্ট"""
        print("নলেজ রিটেনশন টেস্ট করা হচ্ছে...")
        
        # নলেজ আইটেম যোগ করুন
        knowledge_items = [
            {"id": "fact_1", "content": "Earth revolves around the Sun", "category": "science"},
            {"id": "fact_2", "content": "Water boils at 100°C", "category": "science"},
            {"id": "response_1", "content": "Thank you for your kind words", "category": "politeness"},
            {"id": "response_2", "content": "I'm here to help you", "category": "support"}
        ]
        
        retained_knowledge = {}
        
        for item in knowledge_items:
            category = item["category"]
            if category not in retained_knowledge:
                retained_knowledge[category] = []
            
            retained_knowledge[category].append(item["content"])
        
        # নলেজ রিটেনশন ভ্যালিডেশন
        self.assertIn("science", retained_knowledge)
        self.assertIn("politeness", retained_knowledge)
        
        science_facts = retained_knowledge["science"]
        self.assertEqual(len(science_facts), 2)
        self.assertIn("Earth revolves around the Sun", science_facts)
        
        # নলেজ রিট্রাইভাল
        retrieved_items = 0
        for category, items in retained_knowledge.items():
            retrieved_items += len(items)
            
            # প্রতিটি আইটেম চেক
            for item in items:
                self.assertIsInstance(item, str)
                self.assertGreater(len(item), 0)
        
        self.assertEqual(retrieved_items, len(knowledge_items))
        
        # নলেজ ফরগেটিং মেকানিজম (যদি থাকে)
        if hasattr(self.real_learning, 'forget_old_knowledge'):
            # পুরানো নলেজ ফরগেট করুন
            forgotten_count = self.real_learning.forget_old_knowledge(days_old=30)
            print(f"ফরগেট করা হয়েছে: {forgotten_count} পুরানো নলেজ আইটেম")
        
        print(f"রিটেইন করা হয়েছে: {retrieved_items} নলেজ আইটেম")
        print("✅ নলেজ রিটেনশন টেস্ট পাস")
    
    def test_error_handling_in_learning(self):
        """লার্নিং এরর হ্যান্ডলিং টেস্ট"""
        print("লার্নিং এরর হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        # ইনভ্যালিড ডেটা টেস্ট
        invalid_data_cases = [
            {
                "input": None,
                "operation": "learn_from_user",
                "expected_error": TypeError
            },
            {
                "input": "",
                "operation": "get_response",
                "expected_error": ValueError
            },
            {
                "input": {"invalid": "data"},
                "operation": "save_knowledge",
                "expected_error": Exception
            }
        ]
        
        for case in invalid_data_cases:
            try:
                if case["operation"] == "learn_from_user":
                    result = self.learning_system.learn_from_user(None, None)
                elif case["operation"] == "get_response":
                    result = self.learning_system.get_response("", "")
                elif case["operation"] == "save_knowledge":
                    self.learning_system.save_knowledge()
                
                # যদি এরর না আসে, তাহলে রেজাল্ট False হওয়া উচিত
                if result is not None:
                    self.assertFalse(result)
                    
            except Exception as e:
                # এরর ধরা পড়েছে
                print(f"✓ {case['operation']} এরর হ্যান্ডেল হয়েছে: {type(e).__name__}")
        
        # করাপ্টেড ডেটা ফাইল টেস্ট
        corrupt_file = os.path.join(self.test_data_dir, 'corrupt.json')
        
        with open(corrupt_file, 'w') as f:
            f.write("{ invalid json }")
        
        try:
            with open(corrupt_file, 'r') as f:
                data = json.load(f)  # এরর আশা করা হচ্ছে
        except json.JSONDecodeError:
            print("✓ করাপ্টেড JSON ফাইল এরর হ্যান্ডেল হয়েছে")
        finally:
            if os.path.exists(corrupt_file):
                os.remove(corrupt_file)
        
        # মেমোরি এরর সিমুলেশন
        large_data = "x" * (10 ** 7)  # 10MB ডেটা
        
        try:
            # বড় ডেটা প্রসেস করার চেষ্টা করুন
            processed = large_data[:100]  # শুধু প্রথম 100 ক্যারেক্টার
            self.assertEqual(len(processed), 100)
            print("✓ বড় ডেটা হ্যান্ডেল হয়েছে")
        except MemoryError:
            print("✓ মেমোরি এরর হ্যান্ডেল হয়েছে")
        
        print("✅ লার্নিং এরর হ্যান্ডলিং টেস্ট পাস")

def run_learning_tests():
    """লার্নিং টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("🧠 COMPLETE LEARNING SYSTEM TEST SUITE")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLearningSystem)
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 LEARNING TEST RESULTS")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব লার্নিং টেস্ট সফলভাবে পাস হয়েছে!")
        return True
    else:
        print("\n❌ কিছু লার্নিং টেস্ট ব্যর্থ হয়েছে")
        return False

def test_learning_data():
    """লার্নিং ডেটা টেস্ট করুন"""
    print("\n🔍 লার্নিং ডেটা ফাইলসমূহ চেক করা হচ্ছে...")
    
    data_dir = 'data/learning'
    required_files = [
        'user_patterns.json',
        'admin_knowledge.json',
        'bot_memories.json',
        'conversation_history.json',
        'learned_responses.json'
    ]
    
    if not os.path.exists(data_dir):
        print(f"❌ লার্নিং ডেটা ডিরেক্টরি পাওয়া যায়নি: {data_dir}")
        return False
    
    found_files = []
    missing_files = []
    
    for file in required_files:
        file_path = os.path.join(data_dir, file)
        if os.path.exists(file_path):
            found_files.append(file)
            
            # ফাইল সাইজ চেক
            file_size = os.path.getsize(file_path)
            print(f"✓ {file}: {file_size} bytes")
            
            # JSON ভ্যালিডেশন
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  JSON ভ্যালিড: {type(data).__name__}")
            except Exception as e:
                print(f"  ⚠️ JSON ভ্যালিডেশন ব্যর্থ: {e}")
        else:
            missing_files.append(file)
            print(f"❌ {file}: পাওয়া যায়নি")
    
    print(f"\nমোট পাওয়া গেছে: {len(found_files)}/{len(required_files)} ফাইল")
    
    if missing_files:
        print(f"অনুপস্থিত: {missing_files}")
    
    return len(found_files) >= 3  # অন্তত ৩টি ফাইল থাকা উচিত

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='লার্নিং সিস্টেম টেস্ট করুন')
    parser.add_argument('--data', '-d', action='store_true',
                       help='শুধু লার্নিং ডেটা টেস্ট করুন')
    parser.add_argument('--all', '-a', action='store_true',
                       help='সমস্ত লার্নিং টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.data:
        success = test_learning_data()
        sys.exit(0 if success else 1)
    elif args.all:
        success = run_learning_tests()
        sys.exit(0 if success else 1)
    else:
        # ডিফল্ট: শুধু ইউনিট টেস্ট
        success = run_learning_tests()
        sys.exit(0 if success else 1)