"""
⚡ কমান্ড সিস্টেম টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি সমস্ত কমান্ড ফিচার টেস্ট করে
"""

import unittest
import json
import os
import sys
from unittest.mock import Mock, patch

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.command_processor import CommandProcessor
from bot_core.master_bot import MasterBot

class TestCommandSystem(unittest.TestCase):
    """কমান্ড সিস্টেম টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("⚡ কমান্ড সিস্টেম টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট ডেটা তৈরি করুন
        cls.test_commands_data = {
            'prefix': {
                'murgi': {
                    'v1.txt': ['Line 1', 'Line 2', 'Line 3'],
                    'config': {'delay': 2, 'auto_proceed': True}
                },
                'love': {
                    'responses.txt': ['I love you!', 'You are special!', 'Thinking of you!'],
                    'config': {'cooldown': 5}
                }
            },
            'admin': {
                'add': {
                    'add_user.txt': 'User added successfully!',
                    'config': {'permission': 'admin'}
                }
            }
        }
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # কমান্ড প্রসেসর তৈরি করুন
        self.processor = CommandProcessor()
        self.processor.bot = Mock(spec=MasterBot)
        
        # ডেমো কমান্ড রেজিস্টার করুন
        self.register_test_commands()
    
    def register_test_commands(self):
        """টেস্ট কমান্ড রেজিস্টার করুন"""
        self.processor.register_command('test', self.cmd_test)
        self.processor.register_command('echo', self.cmd_echo)
        self.processor.register_command('add', self.cmd_add)
        self.processor.register_command('help', self.cmd_help)
    
    def cmd_test(self, args, user_id, group_id=None):
        """টেস্ট কমান্ড"""
        return f"Test command executed with args: {args}"
    
    def cmd_echo(self, args, user_id, group_id=None):
        """ইকো কমান্ড"""
        return ' '.join(args) if args else 'Echo!'
    
    def cmd_add(self, args, user_id, group_id=None):
        """যোগ কমান্ড"""
        try:
            numbers = list(map(float, args))
            return f"Sum: {sum(numbers)}"
        except ValueError:
            return "Invalid numbers"
    
    def cmd_help(self, args, user_id, group_id=None):
        """হেল্প কমান্ড"""
        return "Available commands: test, echo, add, help"
    
    def test_command_registration(self):
        """কমান্ড রেজিস্ট্রেশন টেস্ট"""
        print("কমান্ড রেজিস্ট্রেশন চেক করা হচ্ছে...")
        
        # রেজিস্টার্ড কমান্ড চেক
        self.assertIn('test', self.processor.commands)
        self.assertIn('echo', self.processor.commands)
        self.assertIn('add', self.processor.commands)
        self.assertIn('help', self.processor.commands)
        
        # কমান্ড ফাংশন চেক
        self.assertEqual(self.processor.commands['test'], self.cmd_test)
        self.assertEqual(self.processor.commands['echo'], self.cmd_echo)
        
        print("✅ কমান্ড রেজিস্ট্রেশন টেস্ট পাস")
    
    def test_command_extraction(self):
        """কমান্ড এক্সট্রাকশন টেস্ট"""
        print("কমান্ড এক্সট্রাকশন টেস্ট করা হচ্ছে...")
        
        test_cases = [
            ('.test arg1 arg2', ('test', ['arg1', 'arg2'])),
            ('!echo hello world', ('echo', ['hello', 'world'])),
            ('no command here', (None, [])),
            ('.', (None, [])),
            ('..test', (None, [])),  # একাধিক prefix
            ('.test', ('test', [])),  # কোনো আর্গুমেন্ট নেই
        ]
        
        for input_text, expected in test_cases:
            command, args = self.processor.extract_command(input_text)
            self.assertEqual(command, expected[0])
            self.assertEqual(args, expected[1])
        
        print("✅ কমান্ড এক্সট্রাকশন টেস্ট পাস")
    
    def test_command_execution(self):
        """কমান্ড এক্সিকিউশন টেস্ট"""
        print("কমান্ড এক্সিকিউশন টেস্ট করা হচ্ছে...")
        
        test_cases = [
            ('test', ['arg1', 'arg2'], 'Test command executed with args: [\'arg1\', \'arg2\']'),
            ('echo', ['Hello', 'World'], 'Hello World'),
            ('echo', [], 'Echo!'),
            ('add', ['1', '2', '3'], 'Sum: 6.0'),
            ('add', ['1.5', '2.5'], 'Sum: 4.0'),
            ('help', [], 'Available commands: test, echo, add, help'),
            ('unknown', [], None),  # অজানা কমান্ড
        ]
        
        for command, args, expected in test_cases:
            result = self.processor.execute_command(command, args, 'user123')
            self.assertEqual(result, expected)
        
        print("✅ কমান্ড এক্সিকিউশন টেস্ট পাস")
    
    def test_prefix_commands(self):
        """প্রিফিক্স কমান্ড টেস্ট (.commands)"""
        print("প্রিফিক্স কমান্ড টেস্ট করা হচ্ছে...")
        
        # .murgi কমান্ড সিমুলেশন
        murgi_responses = []
        
        def mock_murgi_command(args, user_id, group_id=None):
            responses = self.test_commands_data['prefix']['murgi']['v1.txt']
            if not hasattr(mock_murgi_command, 'index'):
                mock_murgi_command.index = 0
            
            if mock_murgi_command.index < len(responses):
                response = responses[mock_murgi_command.index]
                mock_murgi_command.index += 1
                murgi_responses.append(response)
                return response
            return "Murgi sequence completed"
        
        self.processor.register_command('murgi', mock_murgi_command)
        
        # .murgi সিকোয়েন্স টেস্ট
        expected_responses = ['Line 1', 'Line 2', 'Line 3']
        
        for i, expected in enumerate(expected_responses):
            result = self.processor.execute_command('murgi', [], 'user123')
            self.assertEqual(result, expected)
            self.assertEqual(len(murgi_responses), i + 1)
        
        # শেষ রেস্পন্স
        result = self.processor.execute_command('murgi', [], 'user123')
        self.assertEqual(result, "Murgi sequence completed")
        
        print("✅ প্রিফিক্স কমান্ড টেস্ট পাস")
    
    def test_love_command(self):
        """লাভ কমান্ড টেস্ট"""
        print("লাভ কমান্ড টেস্ট করা হচ্ছে...")
        
        love_responses = self.test_commands_data['prefix']['love']['responses.txt']
        
        def mock_love_command(args, user_id, group_id=None):
            import random
            return random.choice(love_responses)
        
        self.processor.register_command('love', mock_love_command)
        
        # একাধিকবার টেস্ট করুন
        test_count = 10
        results = []
        
        for _ in range(test_count):
            result = self.processor.execute_command('love', [], 'user123')
            results.append(result)
        
        # সব রেস্পন্স লিস্টে আছে কিনা চেক করুন
        for result in results:
            self.assertIn(result, love_responses)
        
        # অন্তত ২টি ভিন্ন রেস্পন্স পান (র‍্যান্ডমনেস চেক)
        unique_results = set(results)
        self.assertGreater(len(unique_results), 1)
        
        print("✅ লাভ কমান্ড টেস্ট পাস")
    
    def test_admin_commands(self):
        """এডমিন কমান্ড টেস্ট"""
        print("এডমিন কমান্ড টেস্ট করা হচ্ছে...")
        
        # এডমিন কমান্ড মক করুন
        def mock_add_user(args, user_id, group_id=None):
            if not args:
                return "Usage: .add user @mention"
            
            if user_id != 'admin123':  # শুধু এডমিন পারবে
                return "Permission denied"
            
            return f"User {args[0]} added successfully!"
        
        def mock_kick_user(args, user_id, group_id=None):
            if user_id != 'admin123':
                return "Permission denied"
            
            return f"User {args[0]} kicked!"
        
        self.processor.register_command('add', mock_add_user)
        self.processor.register_command('kick', mock_kick_user)
        
        # পারমিশন টেস্ট
        admin_result = self.processor.execute_command('add', ['@user1'], 'admin123')
        user_result = self.processor.execute_command('add', ['@user1'], 'regular_user')
        
        self.assertEqual(admin_result, "User @user1 added successfully!")
        self.assertEqual(user_result, "Permission denied")
        
        # কিক কমান্ড টেস্ট
        kick_result = self.processor.execute_command('kick', ['@user2'], 'admin123')
        self.assertEqual(kick_result, "User @user2 kicked!")
        
        print("✅ এডমিন কমান্ড টেস্ট পাস")
    
    def test_command_cooldown(self):
        """কমান্ড কুলডাউন টেস্ট"""
        print("কমান্ড কুলডাউন টেস্ট করা হচ্ছে...")
        
        cooldown_commands = {}
        last_executed = {}
        
        def cooldown_command(args, user_id, group_id=None):
            current_time = time.time()
            
            if user_id in last_executed:
                elapsed = current_time - last_executed[user_id]
                if elapsed < 5:  # 5 সেকেন্ড কুলডাউন
                    remaining = 5 - elapsed
                    return f"Please wait {remaining:.1f} seconds before using this command again"
            
            last_executed[user_id] = current_time
            return "Command executed successfully"
        
        self.processor.register_command('cooldown', cooldown_command)
        
        # প্রথম বার এক্সিকিউট
        import time
        result1 = self.processor.execute_command('cooldown', [], 'user1')
        self.assertEqual(result1, "Command executed successfully")
        
        # দ্বিতীয় বার খুব দ্রুত (কুলডাউনে)
        result2 = self.processor.execute_command('cooldown', [], 'user1')
        self.assertIn("Please wait", result2)
        
        # ভিন্ন ইউজার এক্সিকিউট
        result3 = self.processor.execute_command('cooldown', [], 'user2')
        self.assertEqual(result3, "Command executed successfully")
        
        # কুলডাউন শেষ হওয়ার পর
        time.sleep(5.1)
        result4 = self.processor.execute_command('cooldown', [], 'user1')
        self.assertEqual(result4, "Command executed successfully")
        
        print("✅ কমান্ড কুলডাউন টেস্ট পাস")
    
    def test_error_handling_in_commands(self):
        """কমান্ডে এরর হ্যান্ডলিং টেস্ট"""
        print("কমান্ড এরর হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        def error_prone_command(args, user_id, group_id=None):
            if not args:
                raise ValueError("Arguments required")
            
            if args[0] == 'divide':
                if len(args) < 3:
                    return "Need two numbers to divide"
                
                try:
                    num1 = float(args[1])
                    num2 = float(args[2])
                    
                    if num2 == 0:
                        return "Cannot divide by zero"
                    
                    return f"Result: {num1 / num2}"
                except ValueError:
                    return "Invalid numbers"
            
            return "Command executed"
        
        self.processor.register_command('error_test', error_prone_command)
        
        test_cases = [
            ([], "Arguments required"),
            (['divide'], "Need two numbers to divide"),
            (['divide', '10', '0'], "Cannot divide by zero"),
            (['divide', '10', '2'], "Result: 5.0"),
            (['divide', 'ten', 'two'], "Invalid numbers"),
            (['normal'], "Command executed"),
        ]
        
        for args, expected in test_cases:
            result = self.processor.execute_command('error_test', args, 'user123')
            self.assertEqual(result, expected)
        
        print("✅ কমান্ড এরর হ্যান্ডলিং টেস্ট পাস")
    
    def test_command_permissions(self):
        """কমান্ড পারমিশন টেস্ট"""
        print("কমান্ড পারমিশন টেস্ট করা হচ্ছে...")
        
        # পারমিশন লেভেল ডিফাইন করুন
        PERMISSIONS = {
            'user': ['help', 'echo', 'love'],
            'admin': ['help', 'echo', 'love', 'add', 'kick', 'ban'],
            'owner': ['*']  # সব কমান্ড
        }
        
        def check_permission(user_id, command):
            # ডেমো: user_id এর উপর ভিত্তি করে পারমিশন দিন
            if user_id == 'owner123':
                return 'owner'
            elif user_id == 'admin123':
                return 'admin'
            else:
                return 'user'
        
        # পারমিশন চেক সহ কমান্ড এক্সিকিউটর
        def permission_wrapper(command_func):
            def wrapper(args, user_id, group_id=None):
                command_name = command_func.__name__.replace('cmd_', '')
                user_permission = check_permission(user_id, command_name)
                
                allowed_commands = PERMISSIONS.get(user_permission, [])
                
                if '*' in allowed_commands or command_name in allowed_commands:
                    return command_func(args, user_id, group_id)
                else:
                    return f"You don't have permission to use .{command_name} command"
            return wrapper
        
        # টেস্ট কমান্ড
        @permission_wrapper
        def cmd_admin_only(args, user_id, group_id=None):
            return "Admin command executed"
        
        @permission_wrapper
        def cmd_user_only(args, user_id, group_id=None):
            return "User command executed"
        
        self.processor.register_command('admincmd', cmd_admin_only)
        self.processor.register_command('usercmd', cmd_user_only)
        
        # পারমিশন টেস্ট
        # Owner সব করতে পারে
        owner_result = self.processor.execute_command('admincmd', [], 'owner123')
        self.assertEqual(owner_result, "Admin command executed")
        
        # Admin শুধু admincmd করতে পারে
        admin_result = self.processor.execute_command('admincmd', [], 'admin123')
        self.assertEqual(admin_result, "Admin command executed")
        
        # Regular user admincmd করতে পারে না
        user_result = self.processor.execute_command('admincmd', [], 'user123')
        self.assertEqual(user_result, "You don't have permission to use .admincmd command")
        
        # সবাই usercmd করতে পারে
        user_result2 = self.processor.execute_command('usercmd', [], 'user123')
        self.assertEqual(user_result2, "User command executed")
        
        print("✅ কমান্ড পারমিশন টেস্ট পাস")
    
    def test_batch_command_processing(self):
        """ব্যাচ কমান্ড প্রসেসিং টেস্ট"""
        print("ব্যাচ কমান্ড প্রসেসিং টেস্ট করা হচ্ছে...")
        
        execution_log = []
        
        def logging_command(args, user_id, group_id=None):
            execution_log.append({
                'command': 'logging',
                'args': args,
                'user': user_id,
                'timestamp': time.time()
            })
            return f"Logged: {' '.join(args) if args else 'No args'}"
        
        self.processor.register_command('log', logging_command)
        
        import time
        
        # একাধিক কমান্ড একসাথে প্রসেস করুন
        test_commands = [
            ('.log test1', 'user1'),
            ('.log test2', 'user2'),
            ('not a command', 'user1'),
            ('.log', 'user3'),
            ('.log final test', 'user1'),
        ]
        
        for command_text, user_id in test_commands:
            self.processor.process_message(user_id, command_text)
        
        # চেক করুন লগ করা হয়েছে কিনা
        self.assertEqual(len(execution_log), 4)  # 4টি লগ কমান্ড
        
        # ইউজার অনুযায়ী গ্রুপ করুন
        user_counts = {}
        for log in execution_log:
            user_counts[log['user']] = user_counts.get(log['user'], 0) + 1
        
        # user1 এর ২টি লগ থাকা উচিত
        self.assertEqual(user_counts.get('user1', 0), 2)
        
        print("✅ ব্যাচ কমান্ড প্রসেসিং টেস্ট পাস")
    
    def test_command_alias(self):
        """কমান্ড এলিয়াস টেস্ট"""
        print("কমান্ড এলিয়াস টেস্ট করা হচ্ছে...")
        
        # এলিয়াস ডিকশনারি
        command_aliases = {
            'h': 'help',
            '?': 'help',
            'l': 'love',
            'm': 'murgi',
            'p': 'pick'
        }
        
        # আসল কমান্ডগুলোর জন্য মক ফাংশন
        def mock_help(args, user_id, group_id=None):
            return "Help command"
        
        def mock_love(args, user_id, group_id=None):
            return "Love command"
        
        self.processor.register_command('help', mock_help)
        self.processor.register_command('love', mock_love)
        
        # এলিয়াস হ্যান্ডলিং
        def execute_with_alias(command, args, user_id, group_id=None):
            # এলিয়াস চেক
            actual_command = command_aliases.get(command, command)
            
            if actual_command in self.processor.commands:
                return self.processor.commands[actual_command](args, user_id, group_id)
            return None
        
        # এলিয়াস টেস্ট
        test_cases = [
            ('h', [], 'Help command'),
            ('?', [], 'Help command'),
            ('l', [], 'Love command'),
            ('help', [], 'Help command'),  # আসল কমান্ড
            ('unknown', [], None),  # এলিয়াসও নেই
        ]
        
        for alias, args, expected in test_cases:
            result = execute_with_alias(alias, args, 'user123')
            self.assertEqual(result, expected)
        
        print("✅ কমান্ড এলিয়াস টেস্ট পাস")

def run_command_tests():
    """কমান্ড টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("⚡ COMPLETE COMMAND SYSTEM TEST SUITE")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCommandSystem)
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 COMMAND TEST RESULTS")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব কমান্ড টেস্ট সফলভাবে পাস হয়েছে!")
        return True
    else:
        print("\n❌ কিছু কমান্ড টেস্ট ব্যর্থ হয়েছে")
        return False

def test_specific_command(command_name):
    """নির্দিষ্ট কমান্ড টেস্ট করুন"""
    print(f"\n🔍 টেস্টিং: .{command_name} কমান্ড")
    
    processor = CommandProcessor()
    
    # বট মক করুন
    processor.bot = Mock(spec=MasterBot)
    
    # কমান্ড ফাইল লোড করুন
    command_path = f"data/commands/prefix/{command_name}"
    
    if os.path.exists(command_path):
        print(f"কমান্ড ফাইল পাওয়া গেছে: {command_path}")
        
        # কনফিগ ফাইল চেক
        config_file = os.path.join(command_path, 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"কনফিগ: {config}")
        
        # রেস্পন্স ফাইল চেক
        response_files = [f for f in os.listdir(command_path) if f.endswith('.txt')]
        for resp_file in response_files:
            resp_path = os.path.join(command_path, resp_file)
            with open(resp_path, 'r', encoding='utf-8') as f:
                responses = [line.strip() for line in f if line.strip()]
            print(f"{resp_file}: {len(responses)} responses loaded")
        
        return True
    else:
        print(f"❌ কমান্ড ফাইল পাওয়া যায়নি: {command_path}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='কমান্ড সিস্টেম টেস্ট করুন')
    parser.add_argument('--command', '-c', type=str,
                       help='নির্দিষ্ট কমান্ড টেস্ট করুন')
    parser.add_argument('--all', '-a', action='store_true',
                       help='সমস্ত কমান্ড টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.command:
        success = test_specific_command(args.command)
        sys.exit(0 if success else 1)
    elif args.all:
        success = run_command_tests()
        sys.exit(0 if success else 1)
    else:
        # ডিফল্ট: শুধু ইউনিট টেস্ট
        success = run_command_tests()
        sys.exit(0 if success else 1)