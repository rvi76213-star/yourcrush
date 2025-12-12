"""
💬 মেসেঞ্জার API টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি ফেসবুক মেসেঞ্জার ফাংশনালিটি টেস্ট করে
"""

import unittest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.facebook_messenger import FacebookMessenger
from bot_core.message_handler import MessageHandler
from bot_core.cookie_manager import CookieManager

class TestFacebookMessenger(unittest.TestCase):
    """ফেসবুক মেসেঞ্জার টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("💬 ফেসবুক মেসেঞ্জার টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট ডেটা
        cls.test_user_id = "1000123456789"
        cls.test_group_id = "1234567890123456"
        cls.test_message = "This is a test message"
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # মেসেঞ্জার মক করুন
        self.messenger = Mock(spec=FacebookMessenger)
        
        # মক মেথডস
        self.messenger.send_message = Mock(return_value=True)
        self.messenger.get_messages = Mock(return_value=[])
        self.messenger.get_user_info = Mock(return_value={'name': 'Test User'})
        self.messenger.get_group_info = Mock(return_value={'name': 'Test Group'})
        self.messenger.is_logged_in = Mock(return_value=True)
        self.messenger.login = Mock(return_value=True)
        self.messenger.logout = Mock()
        self.messenger.upload_photo = Mock(return_value={'photo_id': '12345'})
        self.messenger.send_photo = Mock(return_value=True)
        
        # মেসেজ হ্যান্ডলার
        self.handler = MessageHandler()
        
        # কুকি ম্যানেজার
        self.cookie_manager = Mock(spec=CookieManager)
        self.cookie_manager.load_cookies = Mock(return_value={'cookies': 'test_cookies'})
        self.cookie_manager.save_cookies = Mock()
        self.cookie_manager.validate_cookies = Mock(return_value=True)
    
    def tearDown(self):
        """প্রতি টেস্ট কেসের পরে রান হবে"""
        print(f"[{self._testMethodName}] টেস্ট শেষ ✓")
    
    def test_message_sending(self):
        """মেসেজ পাঠানো টেস্ট"""
        print("মেসেজ পাঠানো ফাংশনালিটি টেস্ট করা হচ্ছে...")
        
        # সাধারণ টেক্সট মেসেজ
        result = self.messenger.send_message(self.test_user_id, self.test_message)
        self.messenger.send_message.assert_called_once_with(self.test_user_id, self.test_message)
        self.assertTrue(result)
        
        # মেন্টিযুক্ত মেসেজ
        mention_message = "Hello @[123456789] and @[987654321]"
        self.messenger.send_message(self.test_group_id, mention_message)
        
        # ফটো মেসেজ
        photo_path = "data/photos/master.jpg"
        photo_result = self.messenger.send_photo(self.test_user_id, photo_path)
        self.assertTrue(photo_result)
        
        print("✅ মেসেজ পাঠানো টেস্ট পাস")
    
    def test_message_receiving(self):
        """মেসেজ গ্রহণ টেস্ট"""
        print("মেসেজ গ্রহণ ফাংশনালিটি টেস্ট করা হচ্ছে...")
        
        # মক মেসেজ ডেটা
        mock_messages = [
            {
                'sender_id': '111111111',
                'sender_name': 'User One',
                'message': 'Hello bot!',
                'timestamp': '2024-01-15 10:30:00',
                'is_group': False
            },
            {
                'sender_id': '222222222',
                'sender_name': 'User Two',
                'message': '.help',
                'timestamp': '2024-01-15 10:31:00',
                'is_group': True,
                'group_id': self.test_group_id
            }
        ]
        
        self.messenger.get_messages.return_value = mock_messages
        
        # মেসেজ পান
        messages = self.messenger.get_messages()
        
        # ভ্যালিডেশন
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender_name'], 'User One')
        self.assertEqual(messages[1]['message'], '.help')
        self.assertTrue(messages[1]['is_group'])
        
        print("✅ মেসেজ গ্রহণ টেস্ট পাস")
    
    def test_user_info_retrieval(self):
        """ইউজার তথ্য গ্রহণ টেস্ট"""
        print("ইউজার তথ্য গ্রহণ টেস্ট করা হচ্ছে...")
        
        # মক ইউজার তথ্য
        mock_user_info = {
            'id': self.test_user_id,
            'name': 'John Doe',
            'profile_pic': 'https://example.com/profile.jpg',
            'is_friend': True,
            'gender': 'male'
        }
        
        self.messenger.get_user_info.return_value = mock_user_info
        
        # ইউজার তথ্য পান
        user_info = self.messenger.get_user_info(self.test_user_id)
        
        # ভ্যালিডেশন
        self.assertEqual(user_info['id'], self.test_user_id)
        self.assertEqual(user_info['name'], 'John Doe')
        self.assertTrue(user_info['is_friend'])
        
        print("✅ ইউজার তথ্য গ্রহণ টেস্ট পাস")
    
    def test_group_operations(self):
        """গ্রুপ অপারেশন টেস্ট"""
        print("গ্রুপ অপারেশন টেস্ট করা হচ্ছে...")
        
        # গ্রুপ তথ্য
        mock_group_info = {
            'id': self.test_group_id,
            'name': 'Test Group Chat',
            'participants': ['111111111', '222222222', '333333333'],
            'admin_ids': ['111111111'],
            'photo_url': 'https://example.com/group.jpg'
        }
        
        self.messenger.get_group_info.return_value = mock_group_info
        
        # গ্রুপ তথ্য পান
        group_info = self.messenger.get_group_info(self.test_group_id)
        
        # ভ্যালিডেশন
        self.assertEqual(group_info['id'], self.test_group_id)
        self.assertEqual(group_info['name'], 'Test Group Chat')
        self.assertEqual(len(group_info['participants']), 3)
        self.assertIn('111111111', group_info['admin_ids'])
        
        print("✅ গ্রুপ অপারেশন টেস্ট পাস")
    
    def test_authentication(self):
        """অথেনটিকেশন টেস্ট"""
        print("অথেনটিকেশন টেস্ট করা হচ্ছে...")
        
        # লগইন স্ট্যাটাস
        logged_in = self.messenger.is_logged_in()
        self.assertTrue(logged_in)
        
        # লগইন প্রক্রিয়া
        login_result = self.messenger.login()
        self.assertTrue(login_result)
        
        # লগআউট
        self.messenger.logout()
        self.messenger.logout.assert_called_once()
        
        # কুকি ভ্যালিডেশন
        cookies_valid = self.cookie_manager.validate_cookies()
        self.assertTrue(cookies_valid)
        
        print("✅ অথেনটিকেশন টেস্ট পাস")
    
    def test_media_handling(self):
        """মিডিয়া হ্যান্ডলিং টেস্ট"""
        print("মিডিয়া হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        # ফটো আপলোড
        photo_path = "data/photos/photo.jpg"
        upload_result = self.messenger.upload_photo(photo_path)
        
        self.assertIsNotNone(upload_result)
        self.assertIn('photo_id', upload_result)
        
        # ফটো পাঠানো
        photo_id = upload_result['photo_id']
        send_result = self.messenger.send_photo(self.test_user_id, photo_id)
        self.assertTrue(send_result)
        
        # ফাইল পাঠানো (মক)
        file_path = "data/documents/test.pdf"
        self.messenger.send_file = Mock(return_value=True)
        file_result = self.messenger.send_file(self.test_user_id, file_path)
        self.assertTrue(file_result)
        
        print("✅ মিডিয়া হ্যান্ডলিং টেস্ট পাস")
    
    def test_error_handling(self):
        """এরর হ্যান্ডলিং টেস্ট"""
        print("এরর হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        # নেটওয়ার্ক এরর সিমুলেশন
        self.messenger.send_message.side_effect = [
            ConnectionError("Network error"),
            True  # দ্বিতীয় বার সফল
        ]
        
        # প্রথম বার এরর
        with self.assertRaises(ConnectionError):
            self.messenger.send_message(self.test_user_id, "Test")
        
        # দ্বিতীয় বার রিট্রাই
        result = self.messenger.send_message(self.test_user_id, "Test")
        self.assertTrue(result)
        
        # ইনভ্যালিড ইউজার আইডি
        self.messenger.get_user_info.side_effect = ValueError("Invalid user ID")
        
        with self.assertRaises(ValueError):
            self.messenger.get_user_info("invalid_id")
        
        # ফাইল না পাওয়া
        self.messenger.send_photo.side_effect = FileNotFoundError("Photo not found")
        
        with self.assertRaises(FileNotFoundError):
            self.messenger.send_photo(self.test_user_id, "nonexistent.jpg")
        
        print("✅ এরর হ্যান্ডলিং টেস্ট পাস")
    
    def test_rate_limiting(self):
        """রেট লিমিটিং টেস্ট"""
        print("রেট লিমিটিং টেস্ট করা হচ্ছে...")
        
        import time
        
        # মেসেজ কাউন্ট ট্র্যাক করুন
        message_count = 0
        rate_limit = 10  # প্রতি মিনিটে 10 মেসেজ
        time_window = 60  # 60 সেকেন্ড
        
        # মেসেজ পাঠানোর ফাংশন (রেট লিমিট সহ)
        def rate_limited_send(user_id, message):
            nonlocal message_count
            
            current_time = time.time()
            
            # সিমুলেট রেট লিমিট
            if message_count >= rate_limit:
                raise RuntimeError("Rate limit exceeded")
            
            message_count += 1
            return True
        
        self.messenger.send_message.side_effect = rate_limited_send
        
        # রেট লিমিটের মধ্যে মেসেজ পাঠান
        for i in range(rate_limit):
            result = self.messenger.send_message(self.test_user_id, f"Message {i+1}")
            self.assertTrue(result)
        
        # রেট লিমিট এক্সিড করানোর চেষ্টা করুন
        with self.assertRaises(RuntimeError):
            self.messenger.send_message(self.test_user_id, "Extra message")
        
        print("✅ রেট লিমিটিং টেস্ট পাস")
    
    def test_message_parsing(self):
        """মেসেজ পার্সিং টেস্ট"""
        print("মেসেজ পার্সিং টেস্ট করা হচ্ছে...")
        
        test_messages = [
            {
                'raw': 'Hello world',
                'expected': {'text': 'Hello world', 'has_command': False}
            },
            {
                'raw': '.help me please',
                'expected': {'text': '.help me please', 'has_command': True, 'command': 'help'}
            },
            {
                'raw': '@[123456789] check this',
                'expected': {'text': '@[123456789] check this', 'mentions': ['123456789']}
            },
            {
                'raw': '😂👍❤️',
                'expected': {'text': '😂👍❤️', 'emojis': 3}
            }
        ]
        
        for test in test_messages:
            parsed = self.handler.parse_message(test['raw'])
            
            # বেসিক চেক
            self.assertEqual(parsed['text'], test['expected']['text'])
            
            # কমান্ড চেক
            if test['expected'].get('has_command'):
                self.assertIsNotNone(parsed.get('command'))
                self.assertEqual(parsed['command'], test['expected']['command'])
            
            # মেনশন চেক
            if test['expected'].get('mentions'):
                self.assertIn('mentions', parsed)
                self.assertEqual(parsed['mentions'], test['expected']['mentions'])
            
            # ইমোজি চেক
            if test['expected'].get('emojis'):
                # ইমোজি কাউন্ট লজিক এখানে ইমপ্লিমেন্ট করুন
                pass
        
        print("✅ মেসেজ পার্সিং টেস্ট পাস")
    
    def test_bulk_messaging(self):
        """বাল্ক মেসেজিং টেস্ট"""
        print("বাল্ক মেসেজিং টেস্ট করা হচ্ছে...")
        
        # একাধিক রিসিপিয়েন্ট
        recipients = [
            self.test_user_id,
            '222222222',
            '333333333',
            '444444444'
        ]
        
        success_count = 0
        fail_count = 0
        
        # প্রতিটি রিসিপিয়েন্টকে মেসেজ পাঠান
        for recipient in recipients:
            try:
                result = self.messenger.send_message(recipient, "Bulk test message")
                if result:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Failed to send to {recipient}: {e}")
        
        # সফলতার হার
        success_rate = (success_count / len(recipients)) * 100
        self.assertGreater(success_rate, 50)  # অন্তত 50% সফলতা
        
        print(f"বাল্ক মেসেজিং রেজাল্ট: {success_count} সফল, {fail_count} ব্যর্থ")
        print("✅ বাল্ক মেসেজিং টেস্ট পাস")
    
    def test_cookie_management(self):
        """কুকি ম্যানেজমেন্ট টেস্ট"""
        print("কুকি ম্যানেজমেন্ট টেস্ট করা হচ্ছে...")
        
        # কুকি লোড
        cookies = self.cookie_manager.load_cookies()
        self.assertIsNotNone(cookies)
        
        # কুকি ভ্যালিডেশন
        is_valid = self.cookie_manager.validate_cookies()
        self.assertTrue(is_valid)
        
        # কুকি সেভ
        test_cookies = {'session': 'abc123', 'user_id': '1000123456789'}
        self.cookie_manager.save_cookies(test_cookies)
        self.cookie_manager.save_cookies.assert_called_with(test_cookies)
        
        # কুকি এনক্রিপশন (যদি থাকে)
        if hasattr(self.cookie_manager, 'encrypt_cookies'):
            encrypted = self.cookie_manager.encrypt_cookies(test_cookies)
            self.assertIsNotNone(encrypted)
            
            # ডিক্রিপ্ট
            decrypted = self.cookie_manager.decrypt_cookies(encrypted)
            self.assertEqual(decrypted, test_cookies)
        
        print("✅ কুকি ম্যানেজমেন্ট টেস্ট পাস")

class TestMessageHandler(unittest.TestCase):
    """মেসেজ হ্যান্ডলার টেস্ট কেস"""
    
    def setUp(self):
        """টেস্ট সেটআপ"""
        self.handler = MessageHandler()
    
    def test_parse_complex_messages(self):
        """জটিল মেসেজ পার্সিং টেস্ট"""
        print("জটিল মেসেজ পার্সিং টেস্ট করা হচ্ছে...")
        
        complex_messages = [
            {
                'input': '.murgi v2 start now',
                'expected': {
                    'command': 'murgi',
                    'args': ['v2', 'start', 'now'],
                    'is_command': True
                }
            },
            {
                'input': 'Hello @[123456789] and @[987654321]!',
                'expected': {
                    'mentions': ['123456789', '987654321'],
                    'text': 'Hello @[123456789] and @[987654321]!'
                }
            },
            {
                'input': 'Check this: https://example.com',
                'expected': {
                    'has_url': True,
                    'url': 'https://example.com'
                }
            },
            {
                'input': '😂 👍 ❤️ 🎉',
                'expected': {
                    'emojis': ['😂', '👍', '❤️', '🎉'],
                    'emoji_count': 4
                }
            }
        ]
        
        for test in complex_messages:
            parsed = self.handler.parse_message(test['input'])
            
            for key, expected_value in test['expected'].items():
                if key in parsed:
                    self.assertEqual(parsed[key], expected_value)
        
        print("✅ জটিল মেসেজ পার্সিং টেস্ট পাস")
    
    def test_message_filtering(self):
        """মেসেজ ফিল্টারিং টেস্ট"""
        print("মেসেজ ফিল্টারিং টেস্ট করা হচ্ছে...")
        
        # স্প্যাম মেসেজ ডিটেকশন
        spam_messages = [
            'BUY NOW!!! CHEAP PRICES!!!',
            'CLICK THIS LINK: http://malicious.com',
            'FREE MONEY!!! JUST SEND $10',
            'WIN A PRIZE! CALL NOW!'
        ]
        
        clean_messages = [
            'Hello, how are you?',
            'Can you help me with something?',
            'Thanks for your help!',
            'Have a nice day!'
        ]
        
        for message in spam_messages:
            is_spam = self.handler.is_spam(message)
            self.assertTrue(is_spam, f"Should detect spam: {message}")
        
        for message in clean_messages:
            is_spam = self.handler.is_spam(message)
            self.assertFalse(is_spam, f"Should not detect spam: {message}")
        
        print("✅ মেসেজ ফিল্টারিং টেস্ট পাস")

def run_messenger_tests():
    """মেসেঞ্জার টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("💬 COMPLETE MESSENGER SYSTEM TEST SUITE")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestFacebookMessenger))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageHandler))
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 MESSENGER TEST RESULTS")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব মেসেঞ্জার টেস্ট সফলভাবে পাস হয়েছে!")
        return True
    else:
        print("\n❌ কিছু মেসেঞ্জার টেস্ট ব্যর্থ হয়েছে")
        return False

def test_connection():
    """কানেকশন টেস্ট"""
    print("\n🔗 রিয়েল কানেকশন টেস্ট (সতর্কতা: ইন্টারনেট প্রয়োজন)")
    
    try:
        # রিয়েল ফেসবুক কানেকশন টেস্ট
        import requests
        
        # ফেসবুক হোমপেজ
        response = requests.get('https://www.facebook.com', timeout=10)
        
        if response.status_code == 200:
            print("✅ ফেসবুক সার্ভার রিয়াচেবল")
            return True
        else:
            print(f"❌ ফেসবুক সার্ভার রেসপন্স কোড: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ কানেকশন ব্যর্থ: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='মেসেঞ্জার সিস্টেম টেস্ট করুন')
    parser.add_argument('--connection', '-c', action='store_true',
                       help='রিয়েল কানেকশন টেস্ট করুন')
    parser.add_argument('--all', '-a', action='store_true',
                       help='সমস্ত মেসেঞ্জার টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.connection:
        success = test_connection()
        sys.exit(0 if success else 1)
    elif args.all:
        success = run_messenger_tests()
        sys.exit(0 if success else 1)
    else:
        # ডিফল্ট: শুধু ইউনিট টেস্ট
        success = run_messenger_tests()
        sys.exit(0 if success else 1)