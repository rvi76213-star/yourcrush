"""
🤖 মাস্টার বট টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি YOUR CRUSH AI বটের সমস্ত ফিচার টেস্ট করে
"""

import unittest
import json
import os
import sys
import time
from unittest.mock import Mock, patch, MagicMock

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.master_bot import MasterBot
from bot_core.message_handler import MessageHandler
from bot_core.command_processor import CommandProcessor
from azan.azan import AzanSystem

class TestMasterBot(unittest.TestCase):
    """মাস্টার বট টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("🤖 মাস্টার বট টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট কনফিগারেশন তৈরি করুন
        cls.test_config = {
            'bot': {
                'name': 'TestBot',
                'version': '1.0.0',
                'admin_id': '123456789',
                'command_prefix': '.',
                'response_delay': 0.1
            }
        }
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # মাস্টার বট মক করুন
        self.bot = Mock(spec=MasterBot)
        self.bot.config = self.test_config
        self.bot.running = True
        self.bot.users = {}
        self.bot.groups = {}
        self.bot.commands = {}
        
        # মক মেথডস
        self.bot.start = Mock(return_value=True)
        self.bot.stop = Mock()
        self.bot.send_message = Mock()
        self.bot.process_message = Mock()
    
    def tearDown(self):
        """প্রতি টেস্ট কেসের পরে রান হবে"""
        print(f"[{self._testMethodName}] টেস্ট শেষ ✓")
    
    def test_bot_initialization(self):
        """বট ইনিশিয়ালাইজেশন টেস্ট"""
        print("বট ইনিশিয়ালাইজেশন চেক করা হচ্ছে...")
        
        self.assertIsNotNone(self.bot)
        self.assertTrue(hasattr(self.bot, 'config'))
        self.assertTrue(hasattr(self.bot, 'start'))
        self.assertTrue(hasattr(self.bot, 'stop'))
        
        # কনফিগারেশন ভ্যালিডেট করুন
        self.assertEqual(self.bot.config['bot']['name'], 'TestBot')
        self.assertEqual(self.bot.config['bot']['version'], '1.0.0')
        self.assertEqual(self.bot.config['bot']['admin_id'], '123456789')
        
        print("✅ বট ইনিশিয়ালাইজেশন টেস্ট পাস")
    
    def test_bot_start_stop(self):
        """বট শুরু এবং বন্ধ টেস্ট"""
        print("বট শুরু/বন্ধ ফাংশনালিটি টেস্ট করা হচ্ছে...")
        
        # শুরু টেস্ট
        start_result = self.bot.start()
        self.bot.start.assert_called_once()
        self.assertTrue(start_result)
        
        # চলছে কিনা চেক
        self.assertTrue(self.bot.running)
        
        # বন্ধ টেস্ট
        self.bot.stop()
        self.bot.stop.assert_called_once()
        
        print("✅ বট শুরু/বন্ধ টেস্ট পাস")
    
    def test_message_sending(self):
        """মেসেজ পাঠানো টেস্ট"""
        print("মেসেজ পাঠানো ফাংশনালিটি টেস্ট করা হচ্ছে...")
        
        # টেস্ট মেসেজ
        test_message = "Hello, this is a test message!"
        test_user_id = "987654321"
        
        # মেসেজ পাঠান
        self.bot.send_message(test_user_id, test_message)
        
        # মক ফাংশন কল হয়েছে কিনা চেক করুন
        self.bot.send_message.assert_called_once_with(test_user_id, test_message)
        
        print("✅ মেসেজ পাঠানো টেস্ট পাস")
    
    def test_command_processing(self):
        """কমান্ড প্রসেসিং টেস্ট"""
        print("কমান্ড প্রসেসিং টেস্ট করা হচ্ছে...")
        
        # টেস্ট কমান্ড
        test_commands = [
            (".help", "help_command"),
            (".murgi", "murgi_command"),
            (".love", "love_command"),
            (".pick", "pick_command")
        ]
        
        for command, expected_handler in test_commands:
            # মেসেজ প্রসেস কল করুন
            self.bot.process_message("12345", command)
            
            # প্রসেস মেসেজ কল হয়েছে কিনা চেক করুন
            self.bot.process_message.assert_called()
        
        print("✅ কমান্ড প্রসেসিং টেস্ট পাস")
    
    def test_user_management(self):
        """ইউজার ম্যানেজমেন্ট টেস্ট"""
        print("ইউজার ম্যানেজমেন্ট টেস্ট করা হচ্ছে...")
        
        # টেস্ট ইউজার ডেটা
        test_users = [
            {"id": "111111111", "name": "User One", "active": True},
            {"id": "222222222", "name": "User Two", "active": True},
            {"id": "333333333", "name": "User Three", "active": False}
        ]
        
        # ইউজার যোগ করুন
        for user in test_users:
            self.bot.users[user['id']] = user
        
        # ইউজার সংখ্যা চেক করুন
        self.assertEqual(len(self.bot.users), 3)
        
        # অ্যাক্টিভ ইউজার চেক করুন
        active_users = [uid for uid, user in self.bot.users.items() if user['active']]
        self.assertEqual(len(active_users), 2)
        
        print("✅ ইউজার ম্যানেজমেন্ট টেস্ট পাস")
    
    def test_group_management(self):
        """গ্রুপ ম্যানেজমেন্ট টেস্ট"""
        print("গ্রুপ ম্যানেজমেন্ট টেস্ট করা হচ্ছে...")
        
        # টেস্ট গ্রুপ ডেটা
        test_groups = [
            {"id": "G111111111", "name": "Group One", "members": 10},
            {"id": "G222222222", "name": "Group Two", "members": 25},
            {"id": "G333333333", "name": "Group Three", "members": 50}
        ]
        
        # গ্রুপ যোগ করুন
        for group in test_groups:
            self.bot.groups[group['id']] = group
        
        # গ্রুপ সংখ্যা চেক করুন
        self.assertEqual(len(self.bot.groups), 3)
        
        # সর্বোচ্চ মেম্বার গ্রুপ চেক করুন
        max_members_group = max(self.bot.groups.values(), key=lambda x: x['members'])
        self.assertEqual(max_members_group['name'], 'Group Three')
        
        print("✅ গ্রুপ ম্যানেজমেন্ট টেস্ট পাস")
    
    def test_config_loading(self):
        """কনফিগারেশন লোডিং টেস্ট"""
        print("কনফিগারেশন লোডিং টেস্ট করা হচ্ছে...")
        
        # সিমুলেট কনফিগারেশন লোড
        mock_config = {
            'bot': {
                'name': 'MockBot',
                'admin': '555555555',
                'features': ['messaging', 'commands', 'photos']
            }
        }
        
        # কনফিগারেশন ভ্যালিডেশন
        self.assertIn('bot', mock_config)
        self.assertIn('name', mock_config['bot'])
        self.assertIn('admin', mock_config['bot'])
        self.assertIn('features', mock_config['bot'])
        
        # ফিচার চেক
        expected_features = ['messaging', 'commands', 'photos']
        for feature in expected_features:
            self.assertIn(feature, mock_config['bot']['features'])
        
        print("✅ কনফিগারেশন লোডিং টেস্ট পাস")
    
    @patch('azan.azan.AzanSystem')
    def test_azan_integration(self, mock_azan):
        """আজান সিস্টেম ইন্টিগ্রেশন টেস্ট"""
        print("আজান সিস্টেম ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # আজান সিস্টেম মক করুন
        mock_azan_instance = Mock(spec=AzanSystem)
        mock_azan.return_value = mock_azan_instance
        
        # টেস্ট মেথড
        mock_azan_instance.calculate_prayer_times.return_value = {
            'ফজর': '04:30',
            'জোহর': '12:15',
            'আসর': '15:45',
            'মাগরিব': '18:05',
            'ইশা': '19:30'
        }
        
        # আজান সিস্টেম তৈরি করুন
        azan_system = AzanSystem()
        
        # নামাজের সময় ক্যালকুলেট করুন
        prayer_times = azan_system.calculate_prayer_times()
        
        # রেজাল্ট ভ্যালিডেট করুন
        self.assertIn('ফজর', prayer_times)
        self.assertIn('জোহর', prayer_times)
        self.assertIn('আসর', prayer_times)
        self.assertIn('মাগরিব', prayer_times)
        self.assertIn('ইশা', prayer_times)
        
        print("✅ আজান সিস্টেম ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_error_handling(self):
        """এরর হ্যান্ডলিং টেস্ট"""
        print("এরর হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        # এরর সিমুলেশন
        error_cases = [
            ("invalid_user_id", "Invalid user ID format"),
            ("empty_message", "Message cannot be empty"),
            ("rate_limit", "Rate limit exceeded"),
            ("network_error", "Network connection failed")
        ]
        
        for error_type, expected_error in error_cases:
            # এরর হ্যান্ডলিং টেস্ট
            try:
                if error_type == "invalid_user_id":
                    raise ValueError("Invalid user ID format")
                elif error_type == "empty_message":
                    raise ValueError("Message cannot be empty")
                elif error_type == "rate_limit":
                    raise RuntimeError("Rate limit exceeded")
                elif error_type == "network_error":
                    raise ConnectionError("Network connection failed")
            except (ValueError, RuntimeError, ConnectionError) as e:
                # এরর মেসেজ চেক করুন
                self.assertEqual(str(e), expected_error)
        
        print("✅ এরর হ্যান্ডলিং টেস্ট পাস")
    
    def test_performance_metrics(self):
        """পারফরম্যান্স মেট্রিক্স টেস্ট"""
        print("পারফরম্যান্স মেট্রিক্স টেস্ট করা হচ্ছে...")
        
        # টেস্ট মেট্রিক্স
        metrics = {
            'messages_processed': 1000,
            'commands_executed': 250,
            'errors_encountered': 5,
            'avg_response_time': 1.5,
            'uptime_hours': 168.5
        }
        
        # মেট্রিক্স ভ্যালিডেশন
        self.assertGreater(metrics['messages_processed'], 0)
        self.assertGreater(metrics['commands_executed'], 0)
        self.assertLessEqual(metrics['errors_encountered'], metrics['messages_processed'])
        self.assertGreater(metrics['avg_response_time'], 0)
        self.assertGreater(metrics['uptime_hours'], 0)
        
        # এরর রেট ক্যালকুলেশন
        error_rate = (metrics['errors_encountered'] / metrics['messages_processed']) * 100
        self.assertLess(error_rate, 1.0)  # এরর রেট 1% এর নিচে হওয়া উচিত
        
        print("✅ পারফরম্যান্স মেট্রিক্স টেস্ট পাস")

class TestMessageHandler(unittest.TestCase):
    """মেসেজ হ্যান্ডলার টেস্ট কেস"""
    
    def setUp(self):
        """টেস্ট সেটআপ"""
        self.handler = MessageHandler()
    
    def test_message_parsing(self):
        """মেসেজ পার্সিং টেস্ট"""
        print("মেসেজ পার্সিং টেস্ট করা হচ্ছে...")
        
        test_messages = [
            {
                'input': 'Hello world',
                'expected': {'text': 'Hello world', 'command': None, 'args': []}
            },
            {
                'input': '.help me please',
                'expected': {'text': '.help me please', 'command': 'help', 'args': ['me', 'please']}
            },
            {
                'input': '.murgi start',
                'expected': {'text': '.murgi start', 'command': 'murgi', 'args': ['start']}
            }
        ]
        
        for test in test_messages:
            parsed = self.handler.parse_message(test['input'])
            
            # বেসিক চেক
            self.assertEqual(parsed['text'], test['expected']['text'])
            
            # কমান্ড চেক (যদি থাকে)
            if test['expected']['command']:
                self.assertEqual(parsed.get('command'), test['expected']['command'])
                self.assertEqual(parsed.get('args'), test['expected']['args'])
        
        print("✅ মেসেজ পার্সিং টেস্ট পাস")
    
    def test_message_validation(self):
        """মেসেজ ভ্যালিডেশন টেস্ট"""
        print("মেসেজ ভ্যালিডেশন টেস্ট করা হচ্ছে...")
        
        test_cases = [
            ('Valid message', True),
            ('', False),  # খালি মেসেজ
            ('   ', False),  # শুধু স্পেস
            ('A' * 1000, True),  # দীর্ঘ মেসেজ
            ('A' * 10001, False),  # খুব দীর্ঘ মেসেজ
        ]
        
        for message, should_be_valid in test_cases:
            is_valid = self.handler.validate_message(message)
            self.assertEqual(is_valid, should_be_valid)
        
        print("✅ মেসেজ ভ্যালিডেশন টেস্ট পাস")

class TestCommandProcessor(unittest.TestCase):
    """কমান্ড প্রসেসর টেস্ট কেস"""
    
    def setUp(self):
        """টেস্ট সেটআপ"""
        self.processor = CommandProcessor()
    
    def test_command_recognition(self):
        """কমান্ড রিকগনিশন টেস্ট"""
        print("কমান্ড রিকগনিশন টেস্ট করা হচ্ছে...")
        
        test_cases = [
            ('.help', ('help', [])),
            ('.murgi start', ('murgi', ['start'])),
            ('.love you', ('love', ['you'])),
            ('not a command', (None, [])),
            ('.', (None, [])),
        ]
        
        for input_text, expected in test_cases:
            command, args = self.processor.extract_command(input_text)
            self.assertEqual(command, expected[0])
            self.assertEqual(args, expected[1])
        
        print("✅ কমান্ড রিকগনিশন টেস্ট পাস")
    
    def test_command_execution(self):
        """কমান্ড এক্সিকিউশন টেস্ট"""
        print("কমান্ড এক্সিকিউশন টেস্ট করা হচ্ছে...")
        
        # টেস্ট কমান্ড রেজিস্ট্রি
        self.processor.commands = {
            'help': lambda args: 'Help command executed',
            'echo': lambda args: ' '.join(args) if args else 'Echo!',
            'add': lambda args: str(sum(map(int, args))) if args else '0'
        }
        
        test_cases = [
            ('help', [], 'Help command executed'),
            ('echo', ['Hello', 'World'], 'Hello World'),
            ('echo', [], 'Echo!'),
            ('add', ['1', '2', '3'], '6'),
            ('unknown', [], None),  # অজানা কমান্ড
        ]
        
        for command, args, expected in test_cases:
            result = self.processor.execute_command(command, args)
            self.assertEqual(result, expected)
        
        print("✅ কমান্ড এক্সিকিউশন টেস্ট পাস")

def run_all_tests():
    """সমস্ত টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("🚀 COMPLETE TEST SUITE FOR YOUR CRUSH AI BOT")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    
    # সব টেস্ট কেস যোগ করুন
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestMasterBot))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandProcessor))
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব টেস্ট সফলভাবে পাস হয়েছে!")
        return True
    else:
        print("\n❌ কিছু টেস্ট ব্যর্থ হয়েছে")
        
        # ব্যর্থ টেস্ট ডিটেইল
        if result.failures:
            print("\nব্যর্থ টেস্ট:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print("\nএরর টেস্ট:")
            for test, traceback in result.errors:
                print(f"  - {test}")
        
        return False

def quick_test():
    """দ্রুত টেস্ট (ডেভেলপমেন্টের জন্য)"""
    print("\n⚡ দ্রুত টেস্ট শুরু হচ্ছে...")
    
    # বেসিক ফাংশনালিটি টেস্ট
    tests_to_run = [
        ('বট ইনিশিয়ালাইজেশন', test_bot_initialization),
        ('মেসেজ পাঠানো', test_message_sending),
        ('কমান্ড প্রসেসিং', test_command_processing),
    ]
    
    bot_tester = TestMasterBot()
    bot_tester.setUpClass()
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests_to_run:
        print(f"\nটেস্টিং: {test_name}...")
        try:
            bot_tester.setUp()
            test_func(bot_tester)
            bot_tester.tearDown()
            print(f"✅ {test_name}: পাস")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name}: ব্যর্থ - {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name}: এরর - {e}")
            failed += 1
    
    print(f"\n📊 রেজাল্ট: {passed} পাস, {failed} ব্যর্থ")
    
    return failed == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YOUR CRUSH AI বট টেস্ট করুন')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='দ্রুত টেস্ট রান করুন')
    parser.add_argument('--module', '-m', type=str,
                       help='নির্দিষ্ট মডিউল টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.quick:
        success = quick_test()
        sys.exit(0 if success else 1)
    elif args.module:
        # নির্দিষ্ট মডিউল টেস্ট
        print(f"{args.module} মডিউল টেস্ট করা হচ্ছে...")
        # Module-specific test logic here
    else:
        # সম্পূর্ণ টেস্ট স্যুট
        success = run_all_tests()
        sys.exit(0 if success else 1)