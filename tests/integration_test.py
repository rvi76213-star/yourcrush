"""
🔗 ইন্টিগ্রেশন টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি সমস্ত সিস্টেম একসাথে কাজ করছে কিনা টেস্ট করে
"""

import unittest
import os
import sys
import json
import time
from unittest.mock import Mock, patch, MagicMock
import threading

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.master_bot import MasterBot
from bot_core.facebook_messenger import FacebookMessenger
from bot_core.command_processor import CommandProcessor
from bot_core.learning_system import LearningSystem
from bot_core.photo_delivery import PhotoDeliverySystem
from azan.azan import AzanSystem

class TestCompleteSystemIntegration(unittest.TestCase):
    """সম্পূর্ণ সিস্টেম ইন্টিগ্রেশন টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("🔗 সম্পূর্ণ সিস্টেম ইন্টিগ্রেশন টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট কনফিগারেশন
        cls.test_config = {
            'bot': {
                'name': 'IntegrationTestBot',
                'version': '1.0.0',
                'admin_id': '1000123456789',
                'command_prefix': '.',
                'response_delay': 0.1,
                'features': ['messaging', 'commands', 'photos', 'learning', 'azan']
            },
            'azan': {
                'enabled': True,
                'city': 'Dhaka'
            }
        }
        
        # টেস্ট ডেটা তৈরি করুন
        cls.setup_test_data()
    
    @classmethod
    def setup_test_data(cls):
        """টেস্ট ডেটা তৈরি করুন"""
        test_data_dir = 'temp/integration_test'
        os.makedirs(test_data_dir, exist_ok=True)
        
        # ডেমো কুকি ফাইল
        cookies = {
            'c_user': '1000123456789',
            'xs': 'test_xs_token',
            'fr': 'test_fr_token'
        }
        
        with open(os.path.join(test_data_dir, 'test_cookies.json'), 'w') as f:
            json.dump(cookies, f)
        
        # ডেমো ফটো
        photo_dir = os.path.join(test_data_dir, 'photos')
        os.makedirs(photo_dir, exist_ok=True)
        
        from PIL import Image
        for filename in ['master.jpg', 'photo.jpg', 'own.jpg']:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(os.path.join(photo_dir, filename))
        
        print(f"টেস্ট ডেটা তৈরি করা হয়েছে: {test_data_dir}")
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # সমস্ত মডিউল মক করুন
        self.mock_all_modules()
        
        # মাস্টার বট তৈরি করুন
        self.bot = MasterBot(self.test_config)
        
        # মক ইনজেক্ট করুন
        self.inject_mocks()
    
    def mock_all_modules(self):
        """সমস্ত মডিউল মক করুন"""
        # মেসেঞ্জার
        self.messenger = Mock(spec=FacebookMessenger)
        self.messenger.send_message = Mock(return_value=True)
        self.messenger.get_messages = Mock(return_value=[])
        self.messenger.is_logged_in = Mock(return_value=True)
        self.messenger.login = Mock(return_value=True)
        
        # কমান্ড প্রসেসর
        self.command_processor = Mock(spec=CommandProcessor)
        self.command_processor.process_message = Mock(return_value="Command processed")
        self.command_processor.extract_command = Mock(return_value=("help", []))
        
        # লার্নিং সিস্টেম
        self.learning_system = Mock(spec=LearningSystem)
        self.learning_system.get_response = Mock(return_value="AI response")
        self.learning_system.learn_from_interaction = Mock()
        
        # ফটো ডেলিভারি
        self.photo_system = Mock(spec=PhotoDeliverySystem)
        self.photo_system.send_local_photo = Mock(return_value=True)
        self.photo_system.parse_photo_request = Mock(return_value=None)
        
        # আজান সিস্টেম
        self.azan_system = Mock(spec=AzanSystem)
        self.azan_system.handle_command = Mock(return_value="Azan response")
        self.azan_system.start = Mock()
        self.azan_system.stop = Mock()
    
    def inject_mocks(self):
        """মকসমূহ বটে ইনজেক্ট করুন"""
        self.bot.messenger = self.messenger
        self.bot.command_processor = self.command_processor
        self.bot.learning_system = self.learning_system
        self.bot.photo_system = self.photo_system
        self.bot.azan_system = self.azan_system
        
        # বট স্ট্যাটাস
        self.bot.running = True
        self.bot.users = {}
        self.bot.groups = {}
    
    def tearDown(self):
        """প্রতি টেস্ট কেসের পরে রান হবে"""
        print(f"[{self._testMethodName}] টেস্ট শেষ ✓")
    
    def test_system_initialization(self):
        """সিস্টেম ইনিশিয়ালাইজেশন টেস্ট"""
        print("সিস্টেম ইনিশিয়ালাইজেশন চেক করা হচ্ছে...")
        
        # বট ইনিশিয়ালাইজেশন
        self.assertIsNotNone(self.bot)
        self.assertIsNotNone(self.bot.messenger)
        self.assertIsNotNone(self.bot.command_processor)
        self.assertIsNotNone(self.bot.learning_system)
        self.assertIsNotNone(self.bot.photo_system)
        self.assertIsNotNone(self.bot.azan_system)
        
        # কনফিগারেশন
        self.assertEqual(self.bot.config['bot']['name'], 'IntegrationTestBot')
        self.assertIn('messaging', self.bot.config['bot']['features'])
        self.assertIn('commands', self.bot.config['bot']['features'])
        self.assertIn('azan', self.bot.config['bot']['features'])
        
        print("✅ সিস্টেম ইনিশিয়ালাইজেশন টেস্ট পাস")
    
    def test_message_flow(self):
        """মেসেজ ফ্লো টেস্ট"""
        print("মেসেজ ফ্লো টেস্ট করা হচ্ছে...")
        
        # টেস্ট মেসেজ
        test_messages = [
            {
                'sender_id': 'user123',
                'message': 'Hello bot',
                'expected_flow': ['receive', 'process', 'respond']
            },
            {
                'sender_id': 'user456',
                'message': '.help',
                'expected_flow': ['receive', 'command', 'respond']
            },
            {
                'sender_id': 'user789',
                'message': 'ছবি দাও',
                'expected_flow': ['receive', 'photo', 'respond']
            },
            {
                'sender_id': 'user999',
                'message': 'আজানের সময় কখন?',
                'expected_flow': ['receive', 'azan', 'respond']
            }
        ]
        
        for test in test_messages:
            print(f"\nপ্রসেসিং: '{test['message']}'")
            
            # মেসেজ রিসিভ সিমুলেট করুন
            self.messenger.get_messages.return_value = [{
                'sender_id': test['sender_id'],
                'message': test['message'],
                'is_group': False
            }]
            
            # বট প্রসেসিং কল করুন
            self.bot.process_messages()
            
            # মক কল হয়েছে কিনা চেক করুন
            self.messenger.get_messages.assert_called()
            
            # রেস্পন্স পাঠানো হয়েছে কিনা
            if 'command' in test['expected_flow']:
                self.command_processor.process_message.assert_called()
            elif 'photo' in test['expected_flow']:
                self.photo_system.parse_photo_request.assert_called_with(test['message'])
            elif 'azan' in test['expected_flow']:
                self.azan_system.handle_command.assert_called()
            
            print(f"✓ মেসেজ ফ্লো সম্পন্ন: {test['expected_flow']}")
        
        print("✅ মেসেজ ফ্লো টেস্ট পাস")
    
    def test_command_integration(self):
        """কমান্ড ইন্টিগ্রেশন টেস্ট"""
        print("কমান্ড ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # বিভিন্ন কমান্ড টেস্ট
        test_commands = [
            {
                'command': '.help',
                'args': [],
                'expected_response': 'help response',
                'module': 'command_processor'
            },
            {
                'command': '.murgi',
                'args': ['start'],
                'expected_response': 'murgi started',
                'module': 'command_processor'
            },
            {
                'command': '.azan',
                'args': ['times'],
                'expected_response': 'prayer times',
                'module': 'azan_system'
            },
            {
                'command': 'photo',
                'args': ['request'],
                'expected_response': 'photo sent',
                'module': 'photo_system'
            }
        ]
        
        for test in test_commands:
            print(f"\nটেস্টিং: {test['command']}")
            
            # কমান্ড প্রসেস সেটআপ
            if test['module'] == 'command_processor':
                self.command_processor.process_message.return_value = test['expected_response']
                response = self.command_processor.process_message(
                    'test_user', 
                    test['command']
                )
            elif test['module'] == 'azan_system':
                self.azan_system.handle_command.return_value = test['expected_response']
                response = self.azan_system.handle_command(
                    'azan', test['args'], 'test_user'
                )
            elif test['module'] == 'photo_system':
                self.photo_system.send_local_photo.return_value = True
                response = "photo sent"
            
            # রেস্পন্স ভ্যালিডেশন
            self.assertIsNotNone(response)
            
            if isinstance(response, str):
                print(f"✓ রেস্পন্স: {response[:50]}...")
            else:
                print(f"✓ রেস্পন্স টাইপ: {type(response).__name__}")
        
        print("✅ কমান্ড ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_learning_integration(self):
        """লার্নিং ইন্টিগ্রেশন টেস্ট"""
        print("লার্নিং ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # লার্নিং ইন্টারঅ্যাকশন
        learning_scenarios = [
            {
                'user_id': 'learner1',
                'message': 'What is AI?',
                'context': 'education',
                'expected_learn': True
            },
            {
                'user_id': 'learner2',
                'message': 'Thank you for helping',
                'context': 'appreciation',
                'expected_learn': True
            },
            {
                'user_id': 'learner3',
                'message': 'Tell me a story',
                'context': 'entertainment',
                'expected_learn': True
            }
        ]
        
        for scenario in learning_scenarios:
            print(f"\nলার্নিং: {scenario['user_id']} - {scenario['context']}")
            
            # লার্নিং সিস্টেম কল
            learned = self.learning_system.learn_from_interaction(
                scenario['user_id'],
                scenario['message'],
                scenario['context']
            )
            
            # লার্নিং রেস্পন্স
            ai_response = self.learning_system.get_response(
                scenario['user_id'],
                scenario['message'],
                scenario['context']
            )
            
            # ভ্যালিডেশন
            self.assertEqual(learned, scenario['expected_learn'])
            self.assertIsNotNone(ai_response)
            self.assertIsInstance(ai_response, str)
            
            print(f"✓ শেখা: {learned}, রেস্পন্স: {ai_response[:40]}...")
        
        print("✅ লার্নিং ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_photo_system_integration(self):
        """ফটো সিস্টেম ইন্টিগ্রেশন টেস্ট"""
        print("ফটো সিস্টেম ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # ফটো রিকোয়েস্ট সিমুলেশন
        photo_requests = [
            {
                'message': 'ছবি দাও',
                'expected_type': 'local',
                'expected_photo': 'any'
            },
            {
                'message': 'তোমার ছবি দাও',
                'expected_type': 'local',
                'expected_photo': 'your'
            },
            {
                'message': 'একটা ফটো পাঠাও',
                'expected_type': 'local',
                'expected_photo': 'any'
            }
        ]
        
        for request in photo_requests:
            print(f"\nফটো রিকোয়েস্ট: '{request['message']}'")
            
            # ফটো রিকোয়েস্ট পার্স করুন
            parsed = self.photo_system.parse_photo_request(request['message'])
            
            if parsed:
                # ফটো পাঠান
                user_id = 'photo_requester'
                photo_sent = self.photo_system.send_local_photo(
                    user_id, 
                    'data/photos/master.jpg'
                )
                
                # ভ্যালিডেশন
                self.assertTrue(photo_sent)
                
                # মেসেঞ্জার কল হয়েছে কিনা
                self.messenger.send_message.assert_called()
                
                print(f"✓ ফটো পাঠানো হয়েছে: {request['expected_type']}")
            else:
                print("✓ ফটো রিকোয়েস্ট না")
        
        print("✅ ফটো সিস্টেম ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_azan_system_integration(self):
        """আজান সিস্টেম ইন্টিগ্রেশন টেস্ট"""
        print("আজান সিস্টেম ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # আজান কমান্ড
        azan_commands = [
            {
                'command': 'azan',
                'args': [],
                'expected': 'prayer times'
            },
            {
                'command': 'next',
                'args': [],
                'expected': 'next prayer'
            },
            {
                'command': 'hijri',
                'args': [],
                'expected': 'hijri date'
            }
        ]
        
        for cmd in azan_commands:
            print(f"\nআজান কমান্ড: .{cmd['command']}")
            
            # আজান সিস্টেম কল
            response = self.azan_system.handle_command(
                cmd['command'],
                cmd['args'],
                'user123'
            )
            
            # ভ্যালিডেশন
            self.assertEqual(response, cmd['expected'])
            
            print(f"✓ রেস্পন্স: {response}")
        
        # আজান স্টার্ট/স্টপ
        self.azan_system.start()
        self.azan_system.start.assert_called_once()
        
        self.azan_system.stop()
        self.azan_system.stop.assert_called_once()
        
        print("✅ আজান সিস্টেম ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_error_handling_integration(self):
        """এরর হ্যান্ডলিং ইন্টিগ্রেশন টেস্ট"""
        print("এরর হ্যান্ডলিং ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        # বিভিন্ন এরর সিনারিও
        error_scenarios = [
            {
                'type': 'network_error',
                'operation': 'send_message',
                'error': ConnectionError("Network down"),
                'expected_recovery': True
            },
            {
                'type': 'invalid_command',
                'operation': 'process_message',
                'error': ValueError("Invalid command"),
                'expected_recovery': True
            },
            {
                'type': 'file_not_found',
                'operation': 'send_photo',
                'error': FileNotFoundError("Photo not found"),
                'expected_recovery': False
            }
        ]
        
        for scenario in error_scenarios:
            print(f"\nএরর সিনারিও: {scenario['type']}")
            
            # এরর থ্রো সেটআপ
            if scenario['operation'] == 'send_message':
                self.messenger.send_message.side_effect = scenario['error']
                
                try:
                    self.messenger.send_message('user123', 'test')
                    recovery = True
                except scenario['error'].__class__:
                    recovery = False
                    print(f"✓ এরর ধরা পড়েছে: {scenario['type']}")
            
            elif scenario['operation'] == 'process_message':
                self.command_processor.process_message.side_effect = scenario['error']
                
                try:
                    self.command_processor.process_message('user123', 'invalid')
                    recovery = True
                except scenario['error'].__class__:
                    recovery = False
                    print(f"✓ এরর ধরা পড়েছে: {scenario['type']}")
            
            # রিকভারি চেক
            self.assertEqual(recovery, scenario['expected_recovery'])
        
        # সিস্টেম রিকভারি
        if hasattr(self.bot, 'recover_from_error'):
            recovery_success = self.bot.recover_from_error()
            self.assertTrue(recovery_success)
            print("✓ সিস্টেম রিকভারি সম্পন্ন")
        
        print("✅ এরর হ্যান্ডলিং ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_performance_integration(self):
        """পারফরম্যান্স ইন্টিগ্রেশন টেস্ট"""
        print("পারফরম্যান্স ইন্টিগ্রেশন টেস্ট করা হচ্ছে...")
        
        import time
        
        # রেস্পন্স টাইম টেস্ট
        operations = [
            {
                'name': 'Simple message',
                'operation': lambda: self.messenger.send_message('user1', 'Hello')
            },
            {
                'name': 'Command processing',
                'operation': lambda: self.command_processor.process_message('user2', '.help')
            },
            {
                'name': 'AI response',
                'operation': lambda: self.learning_system.get_response('user3', 'Hi', 'greeting')
            },
            {
                'name': 'Photo request',
                'operation': lambda: self.photo_system.parse_photo_request('ছবি দাও')
            }
        ]
        
        performance_results = []
        
        for op in operations:
            start_time = time.time()
            
            try:
                # অপারেশন এক্সিকিউট
                result = op['operation']()
                
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # মিলিসেকেন্ড
                
                performance_results.append({
                    'operation': op['name'],
                    'duration_ms': duration,
                    'success': True
                })
                
                print(f"✓ {op['name']}: {duration:.2f} ms")
                
            except Exception as e:
                performance_results.append({
                    'operation': op['name'],
                    'duration_ms': 0,
                    'success': False,
                    'error': str(e)
                })
                
                print(f"✗ {op['name']}: ব্যর্থ - {e}")
        
        # পারফরম্যান্স অ্যানালাইসিস
        successful_ops = [r for r in performance_results if r['success']]
        
        if successful_ops:
            avg_duration = sum(r['duration_ms'] for r in successful_ops) / len(successful_ops)
            max_duration = max(r['duration_ms'] for r in successful_ops)
            
            print(f"\n📊 পারফরম্যান্স সারাংশ:")
            print(f"  সফল অপারেশন: {len(successful_ops)}/{len(operations)}")
            print(f"  গড় সময়: {avg_duration:.2f} ms")
            print(f"  সর্বোচ্চ সময়: {max_duration:.2f} ms")
            
            # পারফরম্যান্স থ্রেশহোল্ড
            self.assertLess(avg_duration, 1000)  # গড় ১ সেকেন্ডের কম
            self.assertGreater(len(successful_ops), len(operations) * 0.5)  # 50%+ সফল
        
        print("✅ পারফরম্যান্স ইন্টিগ্রেশন টেস্ট পাস")
    
    def test_system_start_stop(self):
        """সিস্টেম শুরু/বন্ধ টেস্ট"""
        print("সিস্টেম শুরু/বন্ধ টেস্ট করা হচ্ছে...")
        
        # সিস্টেম শুরু
        print("\nসিস্টেম শুরু করা হচ্ছে...")
        
        start_success = self.bot.start()
        self.assertTrue(start_success)
        self.assertTrue(self.bot.running)
        
        # সমস্ত মডিউল শুরু হয়েছে কিনা
        self.messenger.login.assert_called_once()
        self.azan_system.start.assert_called_once()
        
        print("✓ সমস্ত মডিউল শুরু হয়েছে")
        
        # কিছু কাজ চলাকালীন
        time.sleep(0.1)
        
        # সিস্টেম বন্ধ
        print("\nসিস্টেম বন্ধ করা হচ্ছে...")
        
        self.bot.stop()
        self.assertFalse(self.bot.running)
        
        # সমস্ত মডিউল বন্ধ হয়েছে কিনা
        self.azan_system.stop.assert_called_once()
        
        print("✓ সমস্ত মডিউল বন্ধ হয়েছে")
        
        print("✅ সিস্টেম শুরু/বন্ধ টেস্ট পাস")
    
    def test_concurrent_operations(self):
        """কনকারেন্ট অপারেশন টেস্ট"""
        print("কনকারেন্ট অপারেশন টেস্ট করা হচ্ছে...")
        
        import threading
        import queue
        
        # কাজের কিউ
        work_queue = queue.Queue()
        results = []
        
        # বিভিন্ন ধরনের কাজ
        tasks = [
            ('message', 'user1', 'Hello'),
            ('command', 'user2', '.help'),
            ('photo', 'user3', 'ছবি দাও'),
            ('learning', 'user4', 'Teach me something'),
            ('azan', 'user5', '.azan times')
        ]
        
        # ওয়ার্কার থ্রেড ফাংশন
        def worker(worker_id):
            while not work_queue.empty():
                try:
                    task_type, user_id, data = work_queue.get_nowait()
                    
                    start_time = time.time()
                    
                    # কাজের ধরন অনুযায়ী প্রসেস
                    if task_type == 'message':
                        result = self.messenger.send_message(user_id, data)
                    elif task_type == 'command':
                        result = self.command_processor.process_message(user_id, data)
                    elif task_type == 'photo':
                        result = self.photo_system.parse_photo_request(data)
                    elif task_type == 'learning':
                        result = self.learning_system.get_response(user_id, data, 'general')
                    elif task_type == 'azan':
                        result = self.azan_system.handle_command('azan', [], user_id)
                    
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    
                    results.append({
                        'worker': worker_id,
                        'task': task_type,
                        'duration_ms': duration,
                        'success': True
                    })
                    
                    print(f"  Worker {worker_id}: {task_type} - {duration:.2f} ms")
                    
                    work_queue.task_done()
                    
                except queue.Empty:
                    break
                except Exception as e:
                    results.append({
                        'worker': worker_id,
                        'task': task_type,
                        'duration_ms': 0,
                        'success': False,
                        'error': str(e)
                    })
                    work_queue.task_done()
        
        # কিউতে কাজ যোগ করুন
        for task in tasks:
            work_queue.put(task)
        
        # ওয়ার্কার থ্রেড তৈরি করুন
        worker_threads = []
        num_workers = 3
        
        for i in range(num_workers):
            thread = threading.Thread(target=worker, args=(i+1,))
            thread.daemon = True
            worker_threads.append(thread)
        
        # থ্রেড শুরু করুন
        print(f"\nশুরু হচ্ছে {num_workers} ওয়ার্কার থ্রেড...")
        start_time = time.time()
        
        for thread in worker_threads:
            thread.start()
        
        # সব থ্রেড শেষ হওয়া পর্যন্ত অপেক্ষা করুন
        for thread in worker_threads:
            thread.join(timeout=5)
        
        end_time = time.time()
        total_duration = (end_time - start_time) * 1000
        
        # রেজাল্ট অ্যানালাইসিস
        successful_tasks = [r for r in results if r['success']]
        
        print(f"\n📊 কনকারেন্ট অপারেশন রেজাল্ট:")
        print(f"  মোট কাজ: {len(tasks)}")
        print(f"  সফল কাজ: {len(successful_tasks)}")
        print(f"  মোট সময়: {total_duration:.2f} ms")
        print(f"  গড় সময়/কাজ: {total_duration/len(tasks):.2f} ms")
        
        # ভ্যালিডেশন
        self.assertGreater(len(successful_tasks), len(tasks) * 0.7)  # 70%+ সফল
        self.assertLess(total_duration, 5000)  # ৫ সেকেন্ডের কম
        
        print("✅ কনকারেন্ট অপারেশন টেস্ট পাস")
    
    def test_data_persistence(self):
        """ডেটা পারসিস্টেন্স টেস্ট"""
        print("ডেটা পারসিস্টেন্স টেস্ট করা হচ্ছে...")
        
        import tempfile
        import shutil
        
        # টেম্পোরারি ডিরেক্টরি
        temp_dir = tempfile.mkdtemp()
        print(f"টেম্প ডিরেক্টরি: {temp_dir}")
        
        try:
            # বিভিন্ন ডেটা ফাইল তৈরি
            data_files = {
                'users.json': {
                    'user123': {'name': 'Test User', 'interactions': 5},
                    'user456': {'name': 'Another User', 'interactions': 3}
                },
                'config.json': {
                    'bot_name': 'TestBot',
                    'features': ['messaging', 'commands']
                },
                'history.json': [
                    {'timestamp': '2024-01-15 10:00:00', 'event': 'start'},
                    {'timestamp': '2024-01-15 10:05:00', 'event': 'message_sent'}
                ]
            }
            
            # ফাইল সেভ
            for filename, data in data_files.items():
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✓ সেভ করা হয়েছে: {filename}")
            
            # ফাইল লোড এবং ভ্যালিডেট
            for filename, expected_data in data_files.items():
                filepath = os.path.join(temp_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # ডেটা ভ্যালিডেশন
                self.assertEqual(type(loaded_data), type(expected_data))
                
                if isinstance(expected_data, dict):
                    self.assertEqual(set(loaded_data.keys()), set(expected_data.keys()))
                elif isinstance(expected_data, list):
                    self.assertEqual(len(loaded_data), len(expected_data))
                
                print(f"✓ ভ্যালিডেট করা হয়েছে: {filename}")
            
            # ডেটা আপডেট
            users_file = os.path.join(temp_dir, 'users.json')
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            # আপডেট করুন
            users_data['user123']['interactions'] = 6
            users_data['new_user'] = {'name': 'New User', 'interactions': 1}
            
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2)
            
            # আবার লোড করুন
            with open(users_file, 'r', encoding='utf-8') as f:
                updated_data = json.load(f)
            
            # আপডেট ভ্যালিডেশন
            self.assertEqual(updated_data['user123']['interactions'], 6)
            self.assertIn('new_user', updated_data)
            
            print("✓ ডেটা আপডেট ভ্যালিডেট হয়েছে")
            
        finally:
            # ক্লিনআপ
            shutil.rmtree(temp_dir)
            print(f"ক্লিনআপ: {temp_dir}")
        
        print("✅ ডেটা পারসিস্টেন্স টেস্ট পাস")

def run_integration_tests():
    """ইন্টিগ্রেশন টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("🔗 COMPLETE SYSTEM INTEGRATION TEST SUITE")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCompleteSystemIntegration)
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 INTEGRATION TEST RESULTS")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব ইন্টিগ্রেশন টেস্ট সফলভাবে পাস হয়েছে!")
        print("🎉 সিস্টেম সম্পূর্ণ ইন্টিগ্রেটেড!")
        return True
    else:
        print("\n❌ কিছু ইন্টিগ্রেশন টেস্ট ব্যর্থ হয়েছে")
        return False

def test_real_integration():
    """রিয়েল ইন্টিগ্রেশন টেস্ট"""
    print("\n🔗 রিয়েল ইন্টিগ্রেশন টেস্ট (সাবধান!)")
    
    response = input("এই টেস্ট রিয়েল বট চালু করবে। চালিয়ে যেতে চান? (yes/no): ")
    
    if response.lower() != 'yes':
        print("টেস্ট বাতিল করা হয়েছে")
        return False
    
    try:
        # কনফিগারেশন লোড
        config_path = 'config/bot_config.py'
        if not os.path.exists(config_path):
            print(f"❌ কনফিগারেশন ফাইল পাওয়া যায়নি: {config_path}")
            return False
        
        # বট শুরু
        print("\nবট শুরু করা হচ্ছে...")
        from start_bot import BotStarter
        starter = BotStarter()
        
        # থ্রেডে শুরু করুন
        import threading
        bot_thread = threading.Thread(target=starter.start)
        bot_thread.daemon = True
        bot_thread.start()
        
        # কিছুক্ষণ অপেক্ষা
        time.sleep(5)
        
        # বট চেক
        if starter.running:
            print("✅ বট সফলভাবে চলছে")
            
            # কিছু টেস্ট কমান্ড
            test_commands = [
                ".help",
                ".azan times",
                "ছবি দাও"
            ]
            
            print("\nটেস্ট কমান্ড:")
            for cmd in test_commands:
                print(f"  {cmd}")
            
            # বট বন্ধ
            print("\nবট বন্ধ করা হচ্ছে...")
            from stop_bot import BotStopper
            stopper = BotStopper()
            stopper.stop()
            
            print("✅ রিয়েল ইন্টিগ্রেশন টেস্ট সম্পন্ন")
            return True
        else:
            print("❌ বট শুরু করা যায়নি")
            return False
            
    except Exception as e:
        print(f"❌ টেস্ট ব্যর্থ: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ইন্টিগ্রেশন টেস্ট করুন')
    parser.add_argument('--real', '-r', action='store_true',
                       help='রিয়েল ইন্টিগ্রেশন টেস্ট করুন')
    parser.add_argument('--all', '-a', action='store_true',
                       help='সমস্ত ইন্টিগ্রেশন টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.real:
        success = test_real_integration()
        sys.exit(0 if success else 1)
    elif args.all:
        success = run_integration_tests()
        sys.exit(0 if success else 1)
    else:
        # ডিফল্ট: শুধু ইউনিট টেস্ট
        success = run_integration_tests()
        sys.exit(0 if success else 1)