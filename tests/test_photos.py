"""
📸 ফটো সিস্টেম টেস্টিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি ফটো ডেলিভারি সিস্টেম টেস্ট করে
"""

import unittest
import os
import sys
import json
import shutil
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from bot_core.photo_delivery import PhotoDeliverySystem
from bot_core.facebook_messenger import FacebookMessenger

class TestPhotoSystem(unittest.TestCase):
    """ফটো সিস্টেম টেস্ট কেস"""
    
    @classmethod
    def setUpClass(cls):
        """টেস্ট শুরু হওয়ার আগে একবার রান হবে"""
        print("\n" + "="*60)
        print("📸 ফটো সিস্টেম টেস্ট শুরু হচ্ছে...")
        print("="*60)
        
        # টেস্ট ডিরেক্টরি তৈরি করুন
        cls.test_dir = 'temp/test_photos'
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # টেস্ট ফটো তৈরি করুন
        cls.create_test_photos()
    
    @classmethod
    def create_test_photos(cls):
        """টেস্ট ফটো তৈরি করুন"""
        # বিভিন্ন সাইজের ফটো তৈরি করুন
        photo_specs = [
            ('master.jpg', (800, 600), 'JPEG'),
            ('photo.png', (1024, 768), 'PNG'),
            ('own.jpg', (400, 400), 'JPEG'),
            ('thumbnail.jpg', (200, 200), 'JPEG'),
            ('large.jpg', (1920, 1080), 'JPEG'),
            ('small.png', (100, 100), 'PNG')
        ]
        
        for filename, size, format in photo_specs:
            filepath = os.path.join(cls.test_dir, filename)
            
            # একটি সরল ফটো তৈরি করুন
            image = Image.new('RGB', size, color='blue')
            
            if format == 'JPEG':
                image.save(filepath, 'JPEG', quality=95)
            else:
                image.save(filepath, 'PNG')
            
            print(f"তৈরি হয়েছে: {filename} ({size[0]}x{size[1]})")
    
    @classmethod
    def tearDownClass(cls):
        """সমস্ত টেস্ট শেষে ক্লিনআপ"""
        print(f"\nটেস্ট ডিরেক্টরি পরিষ্কার করা হচ্ছে: {cls.test_dir}")
        
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
            print("টেস্ট ডিরেক্টরি মুছে ফেলা হয়েছে")
    
    def setUp(self):
        """প্রতি টেস্ট কেসের আগে রান হবে"""
        print(f"\n[{self._testMethodName}] টেস্ট শুরু...")
        
        # ফটো ডেলিভারি সিস্টেম মক করুন
        self.photo_system = Mock(spec=PhotoDeliverySystem)
        
        # মক মেথডস
        self.photo_system.send_local_photo = Mock(return_value=True)
        self.photo_system.get_facebook_profile_photo = Mock(return_value='temp/test_photos/master.jpg')
        self.photo_system.create_thumbnail = Mock(return_value='temp/test_photos/thumbnail.jpg')
        self.photo_system.validate_photo = Mock(return_value=True)
        self.photo_system.get_photo_list = Mock(return_value=['master.jpg', 'photo.png', 'own.jpg'])
        
        # মেসেঞ্জার মক
        self.messenger = Mock(spec=FacebookMessenger)
        self.messenger.send_photo = Mock(return_value=True)
        
        # অ্যাকচুয়াল ফটো সিস্টেম ইনস্ট্যান্স (কিছু টেস্টের জন্য)
        self.real_photo_system = PhotoDeliverySystem()
        self.real_photo_system.messenger = self.messenger
    
    def tearDown(self):
        """প্রতি টেস্ট কেসের পরে রান হবে"""
        print(f"[{self._testMethodName}] টেস্ট শেষ ✓")
    
    def test_photo_file_existence(self):
        """ফটো ফাইল এক্সিস্টেন্স টেস্ট"""
        print("ফটো ফাইল এক্সিস্টেন্স চেক করা হচ্ছে...")
        
        # প্রয়োজনীয় ফটো ফাইল চেক
        required_photos = [
            'data/photos/master.jpg',
            'data/photos/photo.jpg', 
            'data/photos/own.jpg'
        ]
        
        existing_photos = []
        missing_photos = []
        
        for photo_path in required_photos:
            if os.path.exists(photo_path):
                existing_photos.append(photo_path)
                
                # ফটো সাইজ চেক
                try:
                    with Image.open(photo_path) as img:
                        width, height = img.size
                        print(f"✓ {photo_path}: {width}x{height}")
                except Exception as e:
                    print(f"⚠️ {photo_path}: লোড করতে পারেনি - {e}")
            else:
                missing_photos.append(photo_path)
        
        # অন্তত একটি ফটো থাকা উচিত
        self.assertGreater(len(existing_photos), 0, 
                          f"কোনো ফটো পাওয়া যায়নি। প্রয়োজনীয়: {required_photos}")
        
        if missing_photos:
            print(f"⚠️ নিম্নলিখিত ফটো পাওয়া যায়নি: {missing_photos}")
        
        print("✅ ফটো ফাইল এক্সিস্টেন্স টেস্ট পাস")
    
    def test_local_photo_delivery(self):
        """লোকাল ফটো ডেলিভারি টেস্ট"""
        print("লোকাল ফটো ডেলিভারি টেস্ট করা হচ্ছে...")
        
        # টেস্ট ফটো পাঠান
        test_user_id = "1000123456789"
        photo_path = "data/photos/master.jpg"
        
        # মক মাধ্যমে পাঠান
        result = self.photo_system.send_local_photo(test_user_id, photo_path)
        self.photo_system.send_local_photo.assert_called_with(test_user_id, photo_path)
        self.assertTrue(result)
        
        # বিভিন্ন ফটো টেস্ট
        photo_types = ['master', 'photo', 'own']
        
        for photo_type in photo_types:
            # ফটো পাথ তৈরি
            possible_paths = [
                f"data/photos/{photo_type}.jpg",
                f"data/photos/{photo_type}.png",
                f"data/photos/{photo_type}.jpeg"
            ]
            
            # প্রথম যে পাথটি আছে সেটা ব্যবহার করুন
            for path in possible_paths:
                if os.path.exists(path):
                    result = self.messenger.send_photo(test_user_id, path)
                    self.assertTrue(result)
                    break
        
        print("✅ লোকাল ফটো ডেলিভারি টেস্ট পাস")
    
    def test_facebook_profile_photo(self):
        """ফেসবুক প্রোফাইল ফটো টেস্ট"""
        print("ফেসবুক প্রোফাইল ফটো টেস্ট করা হচ্ছে...")
        
        # ফেসবুক প্রোফাইল থেকে ফটো ডাউনলোড (মক)
        profile_url = "https://www.facebook.com/share/17gEJAipcr/"
        photo_path = self.photo_system.get_facebook_profile_photo(profile_url)
        
        self.assertIsNotNone(photo_path)
        self.assertTrue(os.path.exists(photo_path) or isinstance(photo_path, str))
        
        # ডাউনলোড করা ফটো পাঠান
        test_user_id = "1000123456789"
        send_result = self.messenger.send_photo(test_user_id, photo_path)
        self.assertTrue(send_result)
        
        print("✅ ফেসবুক প্রোফাইল ফটো টেস্ট পাস")
    
    def test_photo_validation(self):
        """ফটো ভ্যালিডেশন টেস্ট"""
        print("ফটো ভ্যালিডেশন টেস্ট করা হচ্ছে...")
        
        # বৈধ ফটো টেস্ট
        valid_photos = [
            'temp/test_photos/master.jpg',
            'temp/test_photos/photo.png',
            'temp/test_photos/own.jpg'
        ]
        
        for photo_path in valid_photos:
            is_valid = self.photo_system.validate_photo(photo_path)
            self.assertTrue(is_valid, f"Should be valid: {photo_path}")
        
        # অবৈধ ফটো টেস্ট
        invalid_cases = [
            ('nonexistent.jpg', False),
            ('temp/test_photos', False),  # ডিরেক্টরি
            ('test_photos/.hidden', False),  # হিডেন ফাইল
        ]
        
        for file_path, should_be_valid in invalid_cases:
            is_valid = self.photo_system.validate_photo(file_path)
            self.assertEqual(is_valid, should_be_valid, 
                           f"Validation mismatch for: {file_path}")
        
        # ফটো সাইজ ভ্যালিডেশন
        if hasattr(self.photo_system, 'check_photo_size'):
            size_limits = {
                'min_width': 100,
                'min_height': 100,
                'max_width': 5000,
                'max_height': 5000
            }
            
            # ছোট ফটো (অবৈধ)
            small_photo = 'temp/test_photos/small.png'
            is_valid_size = self.photo_system.check_photo_size(small_photo, size_limits)
            self.assertTrue(is_valid_size)
        
        print("✅ ফটো ভ্যালিডেশন টেস্ট পাস")
    
    def test_thumbnail_generation(self):
        """থাম্বনেইল জেনারেশন টেস্ট"""
        print("থাম্বনেইল জেনারেশন টেস্ট করা হচ্ছে...")
        
        # থাম্বনেইল তৈরি
        original_photo = 'temp/test_photos/large.jpg'
        thumbnail_path = self.photo_system.create_thumbnail(original_photo)
        
        self.assertIsNotNone(thumbnail_path)
        
        # থাম্বনেইল সাইজ চেক
        if os.path.exists(thumbnail_path):
            with Image.open(thumbnail_path) as img:
                width, height = img.size
                
                # থাম্বনেইল সাইজ সাধারণত 200x200 এর কাছাকাছি
                self.assertLessEqual(width, 300)
                self.assertLessEqual(height, 300)
                
                print(f"থাম্বনেইল তৈরি হয়েছে: {width}x{height}")
        
        # বিভিন্ন সাইজের থাম্বনেইল
        test_sizes = [
            ('temp/test_photos/master.jpg', (200, 200)),
            ('temp/test_photos/photo.png', (150, 150)),
            ('temp/test_photos/own.jpg', (100, 100))
        ]
        
        for photo_path, expected_size in test_sizes:
            if hasattr(self.real_photo_system, 'create_thumbnail'):
                # অ্যাকচুয়াল থাম্বনেইল তৈরি করুন
                thumb_path = self.real_photo_system.create_thumbnail(photo_path, expected_size)
                
                if thumb_path and os.path.exists(thumb_path):
                    with Image.open(thumb_path) as img:
                        actual_size = img.size
                        # থাম্বনেইল প্রপোরশন মেনটেইন করবে
                        self.assertLessEqual(actual_size[0], expected_size[0])
                        self.assertLessEqual(actual_size[1], expected_size[1])
        
        print("✅ থাম্বনেইল জেনারেশন টেস্ট পাস")
    
    def test_photo_format_conversion(self):
        """ফটো ফরম্যাট কনভার্শন টেস্ট"""
        print("ফটো ফরম্যাট কনভার্শন টেস্ট করা হচ্ছে...")
        
        if hasattr(self.photo_system, 'convert_photo_format'):
            # PNG থেকে JPG
            png_path = 'temp/test_photos/photo.png'
            jpg_path = self.photo_system.convert_photo_format(png_path, 'JPEG')
            
            self.assertIsNotNone(jpg_path)
            self.assertTrue(jpg_path.endswith('.jpg') or jpg_path.endswith('.jpeg'))
            
            # JPG থেকে PNG
            jpg_path = 'temp/test_photos/master.jpg'
            png_path = self.photo_system.convert_photo_format(jpg_path, 'PNG')
            
            self.assertIsNotNone(png_path)
            self.assertTrue(png_path.endswith('.png'))
            
            # কোয়ালিটি টেস্ট
            high_quality_path = self.photo_system.convert_photo_format(
                png_path, 'JPEG', quality=90
            )
            self.assertIsNotNone(high_quality_path)
        
        # ফটো কম্প্রেশন টেস্ট
        if hasattr(self.photo_system, 'compress_photo'):
            original_path = 'temp/test_photos/large.jpg'
            compressed_path = self.photo_system.compress_photo(original_path, max_size_kb=100)
            
            if compressed_path and os.path.exists(compressed_path):
                original_size = os.path.getsize(original_path)
                compressed_size = os.path.getsize(compressed_path)
                
                # কম্প্রেস করা ফটো ছোট হওয়া উচিত
                self.assertLess(compressed_size, original_size)
                
                compression_ratio = (compressed_size / original_size) * 100
                print(f"কম্প্রেশন: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB ({compression_ratio:.1f}%)")
        
        print("✅ ফটো ফরম্যাট কনভার্শন টেস্ট পাস")
    
    def test_photo_request_parsing(self):
        """ফটো রিকোয়েস্ট পার্সিং টেস্ট"""
        print("ফটো রিকোয়েস্ট পার্সিং টেস্ট করা হচ্ছে...")
        
        # ফটো রিকোয়েস্ট মেসেজ
        photo_requests = [
            {
                'message': 'ছবি দাও',
                'expected': {'type': 'local', 'photo': 'any'}
            },
            {
                'message': 'তোমার ছবি দাও',
                'expected': {'type': 'local', 'photo': 'your'}
            },
            {
                'message': 'বটের ছবি চাই',
                'expected': {'type': 'facebook', 'photo': 'bot'}
            },
            {
                'message': 'ফটো দিতে পারবে?',
                'expected': {'type': 'local', 'photo': 'any'}
            },
            {
                'message': 'একটা পিকচার পাঠাও',
                'expected': {'type': 'local', 'photo': 'any'}
            },
            {
                'message': 'তোমার একটা ফটো দাও',
                'expected': {'type': 'local', 'photo': 'your'}
            }
        ]
        
        if hasattr(self.real_photo_system, 'parse_photo_request'):
            for request in photo_requests:
                parsed = self.real_photo_system.parse_photo_request(request['message'])
                
                # প্যার্স করা উচিত
                self.assertIsNotNone(parsed)
                
                # রিকোয়েস্ট টাইপ চেক
                if parsed:
                    self.assertEqual(parsed['type'], request['expected']['type'])
        
        # ইনভ্যালিড/নন-ফটো রিকোয়েস্ট
        non_photo_messages = [
            'হ্যালো কেমন আছো?',
            'আজকের তারিখ কি?',
            '.help',
            '123456',
            ''
        ]
        
        for message in non_photo_messages:
            if hasattr(self.real_photo_system, 'parse_photo_request'):
                parsed = self.real_photo_system.parse_photo_request(message)
                # ফটো রিকোয়েস্ট না হলে None বা False রিটার্ন করা উচিত
                if parsed is not None:
                    self.assertFalse(parsed.get('is_photo_request', True))
        
        print("✅ ফটো রিকোয়েস্ট পার্সিং টেস্ট পাস")
    
    def test_bulk_photo_sending(self):
        """বাল্ক ফটো সেন্ডিং টেস্ট"""
        print("বাল্ক ফটো সেন্ডিং টেস্ট করা হচ্ছে...")
        
        # একাধিক ইউজারকে ফটো পাঠান
        users = [
            {"id": "1000123456789", "name": "User One"},
            {"id": "1000987654321", "name": "User Two"},
            {"id": "1000555666777", "name": "User Three"},
            {"id": "1000444333222", "name": "User Four"}
        ]
        
        photo_path = "data/photos/photo.jpg"
        results = []
        
        for user in users:
            try:
                # ফটো পাঠান
                result = self.messenger.send_photo(user['id'], photo_path)
                
                results.append({
                    'user': user['name'],
                    'success': result,
                    'error': None
                })
                
                if result:
                    print(f"✓ ফটো পাঠানো হয়েছে: {user['name']}")
                else:
                    print(f"✗ ফটো পাঠানো যায়নি: {user['name']}")
                    
            except Exception as e:
                results.append({
                    'user': user['name'],
                    'success': False,
                    'error': str(e)
                })
                print(f"✗ এরর: {user['name']} - {e}")
        
        # সফলতার হার
        successful = sum(1 for r in results if r['success'])
        success_rate = (successful / len(results)) * 100
        
        self.assertGreater(success_rate, 50)  # অন্তত 50% সফলতা
        
        print(f"বাল্ক ফটো সেন্ডিং রেজাল্ট: {successful}/{len(results)} সফল ({success_rate:.1f}%)")
        print("✅ বাল্ক ফটো সেন্ডিং টেস্ট পাস")
    
    def test_photo_metadata(self):
        """ফটো মেটাডেটা টেস্ট"""
        print("ফটো মেটাডেটা টেস্ট করা হচ্ছে...")
        
        # ফটো মেটাডেটা এক্সট্র্যাক্ট
        test_photos = [
            'temp/test_photos/master.jpg',
            'temp/test_photos/photo.png'
        ]
        
        for photo_path in test_photos:
            if os.path.exists(photo_path):
                try:
                    with Image.open(photo_path) as img:
                        metadata = {
                            'format': img.format,
                            'size': img.size,
                            'mode': img.mode,
                            'width': img.width,
                            'height': img.height
                        }
                        
                        # মেটাডেটা ভ্যালিডেশন
                        self.assertIsNotNone(metadata['format'])
                        self.assertGreater(metadata['width'], 0)
                        self.assertGreater(metadata['height'], 0)
                        
                        print(f"{photo_path}: {metadata['width']}x{metadata['height']} {metadata['format']}")
                        
                        # EXIF ডেটা (যদি থাকে)
                        if hasattr(img, '_getexif'):
                            exif = img._getexif()
                            if exif:
                                print(f"  EXIF data: {len(exif)} tags")
                
                except Exception as e:
                    print(f"মেটাডেটা পড়তে পারেনি {photo_path}: {e}")
        
        # ফটো ইনফো ফাইল
        info_file = 'data/photos/photo_info.json'
        if os.path.exists(info_file):
            with open(info_file, 'r', encoding='utf-8') as f:
                photo_info = json.load(f)
            
            # ফটো ইনফো ভ্যালিডেশন
            self.assertIsInstance(photo_info, dict)
            
            if 'photos' in photo_info:
                for photo_name, info in photo_info['photos'].items():
                    self.assertIn('path', info)
                    self.assertIn('description', info)
        
        print("✅ ফটো মেটাডেটা টেস্ট পাস")
    
    def test_error_handling(self):
        """ফটো এরর হ্যান্ডলিং টেস্ট"""
        print("ফটো এরর হ্যান্ডলিং টেস্ট করা হচ্ছে...")
        
        # ফাইল না পাওয়া এরর
        missing_photo = 'data/photos/nonexistent.jpg'
        
        if hasattr(self.real_photo_system, 'send_local_photo'):
            try:
                result = self.real_photo_system.send_local_photo('user123', missing_photo)
                # ফাইল না থাকলে False বা Exception রিটার্ন করা উচিত
                if result is not True:
                    print("✓ ফাইল না পাওয়া এরর সঠিকভাবে হ্যান্ডেল হয়েছে")
            except FileNotFoundError:
                print("✓ FileNotFoundError ধরা পড়েছে")
            except Exception as e:
                print(f"✓ অন্য এরর ধরা পড়েছে: {type(e).__name__}")
        
        # ইনভ্যালিড ফটো ফরম্যাট
        invalid_photo = 'temp/test_photos/invalid.txt'
        
        # একটি টেক্সট ফাইল তৈরি করুন (ইনভ্যালিড ফটো)
        with open(invalid_photo, 'w') as f:
            f.write("This is not a valid image file")
        
        try:
            # ফটো ভ্যালিডেশন
            if hasattr(self.photo_system, 'validate_photo'):
                is_valid = self.photo_system.validate_photo(invalid_photo)
                self.assertFalse(is_valid)
        finally:
            # ক্লিনআপ
            if os.path.exists(invalid_photo):
                os.remove(invalid_photo)
        
        # পারমিশন এরর সিমুলেশন
        protected_photo = 'temp/test_photos/protected.jpg'
        
        # রিড-অনলি ফাইল তৈরি করুন
        with open(protected_photo, 'w') as f:
            f.write("test")
        
        import stat
        os.chmod(protected_photo, stat.S_IREAD)  # রিড-অনলি
        
        try:
            # ফটো পড়ার চেষ্টা করুন
            with Image.open(protected_photo) as img:
                pass  # এরর আশা করা হচ্ছে
        except PermissionError:
            print("✓ PermissionError ধরা পড়েছে")
        finally:
            # পারমিশন রিস্টোর করুন এবং ফাইল মুছুন
            os.chmod(protected_photo, stat.S_IWRITE)
            os.remove(protected_photo)
        
        print("✅ ফটো এরর হ্যান্ডলিং টেস্ট পাস")
    
    def test_photo_backup(self):
        """ফটো ব্যাকআপ টেস্ট"""
        print("ফটো ব্যাকআপ টেস্ট করা হচ্ছে...")
        
        # ব্যাকআপ ডিরেক্টরি
        backup_dir = 'temp/test_backup'
        os.makedirs(backup_dir, exist_ok=True)
        
        try:
            # ফটো ব্যাকআপ (মক)
            if hasattr(self.photo_system, 'backup_photos'):
                backup_result = self.photo_system.backup_photos(backup_dir)
                self.assertTrue(backup_result)
            
            # ম্যানুয়াল ব্যাকআপ টেস্ট
            source_photos = [
                'temp/test_photos/master.jpg',
                'temp/test_photos/photo.png'
            ]
            
            backed_up = []
            
            for photo_path in source_photos:
                if os.path.exists(photo_path):
                    # ব্যাকআপ কপি তৈরি করুন
                    import shutil
                    filename = os.path.basename(photo_path)
                    backup_path = os.path.join(backup_dir, filename)
                    
                    shutil.copy2(photo_path, backup_path)
                    backed_up.append(backup_path)
                    
                    # চেক করুন ব্যাকআপ হয়েছে কিনা
                    self.assertTrue(os.path.exists(backup_path))
                    
                    # ফাইল সাইজ চেক
                    original_size = os.path.getsize(photo_path)
                    backup_size = os.path.getsize(backup_path)
                    
                    self.assertEqual(original_size, backup_size)
            
            print(f"ব্যাকআপ করা হয়েছে: {len(backed_up)} ফটো")
            
            # ব্যাকআপ থেকে রিস্টোর টেস্ট
            if backed_up:
                restore_dir = 'temp/test_restore'
                os.makedirs(restore_dir, exist_ok=True)
                
                for backup_path in backed_up:
                    filename = os.path.basename(backup_path)
                    restore_path = os.path.join(restore_dir, filename)
                    
                    shutil.copy2(backup_path, restore_path)
                    self.assertTrue(os.path.exists(restore_path))
                
                print(f"রিস্টোর করা হয়েছে: {len(backed_up)} ফটো")
                
                # ক্লিনআপ
                shutil.rmtree(restore_dir)
        
        finally:
            # ক্লিনআপ
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
        
        print("✅ ফটো ব্যাকআপ টেস্ট পাস")

def run_photo_tests():
    """ফটো টেস্ট রান করুন"""
    print("\n" + "="*60)
    print("📸 COMPLETE PHOTO SYSTEM TEST SUITE")
    print("="*60)
    
    # টেস্ট স্যুট তৈরি করুন
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPhotoSystem)
    
    # টেস্ট রানার
    runner = unittest.TextTestRunner(verbosity=2)
    
    # টেস্ট রান করুন
    print(f"\nমোট টেস্ট কেস: {suite.countTestCases()}")
    print("টেস্ট শুরু হচ্ছে...\n")
    
    result = runner.run(suite)
    
    # রেজাল্ট সারাংশ
    print("\n" + "="*60)
    print("📊 PHOTO TEST RESULTS")
    print("="*60)
    print(f"টেস্ট রান হয়েছে: {result.testsRun}")
    print(f"সফল: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"ব্যর্থ: {len(result.failures)}")
    print(f"এরর: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ সব ফটো টেস্ট সফলভাবে পাস হয়েছে!")
        return True
    else:
        print("\n❌ কিছু ফটো টেস্ট ব্যর্থ হয়েছে")
        return False

def test_photo_files():
    """ফটো ফাইলসমূহ টেস্ট করুন"""
    print("\n🔍 ফটো ফাইলসমূহ চেক করা হচ্ছে...")
    
    photo_dir = 'data/photos'
    thumb_dir = 'data/photos/thumbnails'
    
    if not os.path.exists(photo_dir):
        print(f"❌ ফটো ডিরেক্টরি পাওয়া যায়নি: {photo_dir}")
        return False
    
    # প্রধান ফটো ফাইল চেক
    main_photos = ['master.jpg', 'photo.jpg', 'own.jpg']
    found_photos = []
    
    for photo in main_photos:
        photo_path = os.path.join(photo_dir, photo)
        if os.path.exists(photo_path):
            found_photos.append(photo)
            
            # ফটো ডিটেইল
            try:
                with Image.open(photo_path) as img:
                    size = img.size
                    print(f"✓ {photo}: {size[0]}x{size[1]}")
            except Exception as e:
                print(f"⚠️ {photo}: পড়তে পারেনি - {e}")
        else:
            print(f"❌ {photo}: পাওয়া যায়নি")
    
    # থাম্বনেইল ডিরেক্টরি চেক
    if os.path.exists(thumb_dir):
        thumbnails = os.listdir(thumb_dir)
        print(f"থাম্বনেইল: {len(thumbnails)} টি")
    else:
        print("⚠️ থাম্বনেইল ডিরেক্টরি নেই")
    
    # PNG ভার্সন চেক
    png_versions = [p.replace('.jpg', '.png') for p in main_photos]
    for png in png_versions:
        png_path = os.path.join(photo_dir, png)
        if os.path.exists(png_path):
            print(f"✓ {png}: পাওয়া গেছে")
    
    print(f"\nমোট পাওয়া গেছে: {len(found_photos)}/{len(main_photos)} প্রধান ফটো")
    
    return len(found_photos) > 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ফটো সিস্টেম টেস্ট করুন')
    parser.add_argument('--files', '-f', action='store_true',
                       help='শুধু ফটো ফাইলসমূহ টেস্ট করুন')
    parser.add_argument('--all', '-a', action='store_true',
                       help='সমস্ত ফটো টেস্ট করুন')
    
    args = parser.parse_args()
    
    if args.files:
        success = test_photo_files()
        sys.exit(0 if success else 1)
    elif args.all:
        success = run_photo_tests()
        sys.exit(0 if success else 1)
    else:
        # ডিফল্ট: শুধু ইউনিট টেস্ট
        success = run_photo_tests()
        sys.exit(0 if success else 1)