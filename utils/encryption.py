#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Encryption System
Handles encryption and decryption of sensitive data
"""

import base64
import hashlib
import json
import os
import secrets
from typing import Any, Dict, Optional, Union

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random


class Encryption:
    """🔐 Encryption handler for sensitive data"""
    
    def __init__(self, key: Optional[str] = None):
        """
        Initialize encryption handler
        
        Args:
            key: Encryption key (if None, will try to load from env)
        """
        self.key = key or self._get_encryption_key()
        self.block_size = AES.block_size
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key from environment or generate new"""
        # Try to get from environment variable
        env_key = os.getenv("ENCRYPTION_KEY")
        
        if env_key:
            # Use environment key
            return hashlib.sha256(env_key.encode()).digest()
        else:
            # Try to load from file
            key_file = "config/encryption.key"
            
            if os.path.exists(key_file):
                try:
                    with open(key_file, "rb") as f:
                        return f.read()
                except:
                    pass
            
            # Generate new key
            new_key = secrets.token_bytes(32)  # 256-bit key
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            
            with open(key_file, "wb") as f:
                f.write(new_key)
            
            # Also save to environment file for reference
            env_file = ".env"
            if os.path.exists(env_file):
                with open(env_file, "a") as f:
                    f.write(f"\n# Encryption key (base64)\n")
                    f.write(f"ENCRYPTION_KEY={base64.b64encode(new_key).decode()}\n")
            
            return new_key
    
    def encrypt(self, plaintext: Union[str, bytes]) -> bytes:
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext: Text to encrypt
        
        Returns:
            Encrypted bytes
        """
        try:
            # Convert string to bytes if needed
            if isinstance(plaintext, str):
                plaintext = plaintext.encode('utf-8')
            
            # Generate random IV
            iv = Random.new().read(self.block_size)
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Pad and encrypt
            padded_data = pad(plaintext, self.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            
            # Combine IV and encrypted data
            return iv + encrypted_data
            
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {e}")
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using AES-256-CBC
        
        Args:
            ciphertext: Encrypted bytes
        
        Returns:
            Decrypted bytes
        """
        try:
            # Extract IV from beginning
            iv = ciphertext[:self.block_size]
            actual_ciphertext = ciphertext[self.block_size:]
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Decrypt and unpad
            decrypted_padded = cipher.decrypt(actual_ciphertext)
            decrypted = unpad(decrypted_padded, self.block_size)
            
            return decrypted
            
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {e}")
    
    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypt string and return base64 encoded result
        
        Args:
            plaintext: String to encrypt
        
        Returns:
            Base64 encoded encrypted string
        """
        encrypted_bytes = self.encrypt(plaintext)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    
    def decrypt_string(self, encrypted_text: str) -> str:
        """
        Decrypt base64 encoded string
        
        Args:
            encrypted_text: Base64 encoded encrypted string
        
        Returns:
            Decrypted string
        """
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted_bytes = self.decrypt(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')
    
    def encrypt_data(self, data: Any) -> str:
        """
        Encrypt any JSON-serializable data
        
        Args:
            data: Data to encrypt
        
        Returns:
            Encrypted string
        """
        # Convert data to JSON string
        json_str = json.dumps(data, ensure_ascii=False)
        
        # Encrypt the string
        return self.encrypt_string(json_str)
    
    def decrypt_data(self, encrypted_data: str) -> Any:
        """
        Decrypt data and parse as JSON
        
        Args:
            encrypted_data: Encrypted data string
        
        Returns:
            Decrypted data
        """
        # Decrypt string
        json_str = self.decrypt_string(encrypted_data)
        
        # Parse JSON
        return json.loads(json_str)
    
    def encrypt_file(self, input_file: str, output_file: Optional[str] = None):
        """
        Encrypt a file
        
        Args:
            input_file: Path to input file
            output_file: Path to output file (if None, input_file.enc)
        """
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            if output_file is None:
                output_file = input_file + ".enc"
            
            # Read input file
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            
            # Encrypt
            ciphertext = self.encrypt(plaintext)
            
            # Write output file
            with open(output_file, 'wb') as f:
                f.write(ciphertext)
            
            return output_file
            
        except Exception as e:
            raise EncryptionError(f"File encryption failed: {e}")
    
    def decrypt_file(self, input_file: str, output_file: Optional[str] = None):
        """
        Decrypt a file
        
        Args:
            input_file: Path to input file
            output_file: Path to output file (if None, input_file.dec)
        """
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            if output_file is None:
                # Remove .enc extension if present
                if input_file.endswith('.enc'):
                    output_file = input_file[:-4]
                else:
                    output_file = input_file + ".dec"
            
            # Read input file
            with open(input_file, 'rb') as f:
                ciphertext = f.read()
            
            # Decrypt
            plaintext = self.decrypt(ciphertext)
            
            # Write output file
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            return output_file
            
        except Exception as e:
            raise EncryptionError(f"File decryption failed: {e}")
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        """
        Hash a password using PBKDF2
        
        Args:
            password: Password to hash
            salt: Salt bytes (if None, generates new)
        
        Returns:
            Dictionary with hash and salt
        """
        try:
            if salt is None:
                salt = secrets.token_bytes(16)
            
            # Use PBKDF2 with SHA256
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000,  # 100,000 iterations
                dklen=32  # 32 bytes = 256 bits
            )
            
            return {
                'hash': base64.b64encode(key).decode('utf-8'),
                'salt': base64.b64encode(salt).decode('utf-8'),
                'algorithm': 'PBKDF2-SHA256'
            }
            
        except Exception as e:
            raise EncryptionError(f"Password hashing failed: {e}")
    
    def verify_password(self, password: str, stored_hash: str, stored_salt: str) -> bool:
        """
        Verify a password against stored hash
        
        Args:
            password: Password to verify
            stored_hash: Stored hash (base64)
            stored_salt: Stored salt (base64)
        
        Returns:
            True if password matches
        """
        try:
            # Decode stored hash and salt
            stored_hash_bytes = base64.b64decode(stored_hash)
            stored_salt_bytes = base64.b64decode(stored_salt)
            
            # Hash the provided password
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                stored_salt_bytes,
                100000,
                dklen=32
            )
            
            # Compare (constant-time comparison)
            return secrets.compare_digest(new_hash, stored_hash_bytes)
            
        except Exception as e:
            raise EncryptionError(f"Password verification failed: {e}")
    
    def generate_token(self, length: int = 32) -> str:
        """
        Generate a secure random token
        
        Args:
            length: Token length in bytes
        
        Returns:
            Base64 encoded token
        """
        token = secrets.token_bytes(length)
        return base64.b64encode(token).decode('utf-8')
    
    def secure_delete(self, file_path: str, passes: int = 3):
        """
        Securely delete a file by overwriting
        
        Args:
            file_path: Path to file
            passes: Number of overwrite passes
        """
        try:
            if not os.path.exists(file_path):
                return
            
            file_size = os.path.getsize(file_path)
            
            for pass_num in range(passes):
                # Generate random data
                random_data = secrets.token_bytes(file_size)
                
                # Write random data
                with open(file_path, 'wb') as f:
                    f.write(random_data)
                
                # Sync to disk
                os.fsync(f.fileno())
            
            # Delete the file
            os.remove(file_path)
            
        except Exception as e:
            raise EncryptionError(f"Secure delete failed: {e}")


class EncryptionError(Exception):
    """Encryption related error"""
    pass


# Helper functions for common operations
def encrypt_cookies(cookies: list, key: Optional[str] = None) -> str:
    """Encrypt cookies list"""
    encryptor = Encryption(key)
    return encryptor.encrypt_data(cookies)


def decrypt_cookies(encrypted_cookies: str, key: Optional[str] = None) -> list:
    """Decrypt cookies list"""
    encryptor = Encryption(key)
    return encryptor.decrypt_data(encrypted_cookies)


def create_secure_backup(data: Any, backup_file: str, key: Optional[str] = None):
    """Create encrypted backup of data"""
    encryptor = Encryption(key)
    encrypted = encryptor.encrypt_data(data)
    
    with open(backup_file, 'w') as f:
        f.write(encrypted)


def restore_secure_backup(backup_file: str, key: Optional[str] = None) -> Any:
    """Restore data from encrypted backup"""
    encryptor = Encryption(key)
    
    with open(backup_file, 'r') as f:
        encrypted = f.read()
    
    return encryptor.decrypt_data(encrypted)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Encryption Module - Secure data encryption and decryption
"""

import os
import base64
import hashlib
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("⚠️ cryptography not installed. Install with: pip install cryptography")

class Encryption:
    """Encryption and decryption utilities"""
    
    def __init__(self, key_file: str = "data/encryption_key.key"):
        self.key_file = key_file
        self.key = None
        self.fernet = None
        
        # Initialize encryption
        self.initialize_encryption()
    
    def initialize_encryption(self):
        """Initialize encryption system"""
        if not CRYPTOGRAPHY_AVAILABLE:
            self.log_warning("Cryptography library not available")
            return
        
        try:
            # Load or generate key
            self.key = self.load_or_generate_key()
            
            # Create Fernet instance
            self.fernet = Fernet(self.key)
            
            self.log_info("Encryption system initialized")
            
        except Exception as e:
            self.log_error(f"Failed to initialize encryption: {e}")
    
    def load_or_generate_key(self) -> bytes:
        """Load existing key or generate new one"""
        # Try to load existing key
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                
                # Validate key
                if len(key) == 44:  # Fernet keys are 44 bytes
                    self.log_info(f"Loaded encryption key from {self.key_file}")
                    return key
            
            except Exception as e:
                self.log_error(f"Error loading key: {e}")
        
        # Generate new key
        self.log_info("Generating new encryption key...")
        key = Fernet.generate_key()
        
        # Save key
        try:
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            
            self.log_info(f"Generated and saved new key to {self.key_file}")
            
            # Set secure permissions (Unix-like systems)
            try:
                os.chmod(self.key_file, 0o600)
            except:
                pass
            
        except Exception as e:
            self.log_error(f"Error saving key: {e}")
        
        return key
    
    def encrypt_data(self, data: Any) -> str:
        """
        Encrypt any serializable data
        
        Args:
            data: Data to encrypt (will be JSON serialized)
        
        Returns:
            Base64 encoded encrypted string
        """
        if not self.fernet:
            self.log_warning("Encryption not available, returning plain data")
            return self.serialize_data(data)
        
        try:
            # Serialize data to JSON string
            json_str = self.serialize_data(data)
            
            # Encrypt
            encrypted_bytes = self.fernet.encrypt(json_str.encode('utf-8'))
            
            # Encode for storage
            encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
            
            return encrypted_b64
            
        except Exception as e:
            self.log_error(f"Encryption error: {e}")
            # Fallback to serialized data (not encrypted)
            return self.serialize_data(data)
    
    def decrypt_data(self, encrypted_b64: str) -> Any:
        """
        Decrypt data
        
        Args:
            encrypted_b64: Base64 encoded encrypted string
        
        Returns:
            Decrypted and deserialized data
        """
        if not self.fernet:
            self.log_warning("Decryption not available, assuming plain data")
            return self.deserialize_data(encrypted_b64)
        
        try:
            # Decode from base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_b64.encode('utf-8'))
            
            # Decrypt
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            
            # Deserialize
            json_str = decrypted_bytes.decode('utf-8')
            data = self.deserialize_data(json_str)
            
            return data
            
        except Exception as e:
            self.log_error(f"Decryption error: {e}")
            # Try to deserialize as plain data
            try:
                return self.deserialize_data(encrypted_b64)
            except:
                raise ValueError(f"Failed to decrypt or deserialize data: {e}")
    
    def serialize_data(self, data: Any) -> str:
        """Serialize data to JSON string"""
        try:
            return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        except Exception as e:
            self.log_error(f"Serialization error: {e}")
            return json.dumps({"error": "Serialization failed", "data": str(data)})
    
    def deserialize_data(self, json_str: str) -> Any:
        """Deserialize data from JSON string"""
        try:
            return json.loads(json_str)
        except Exception as e:
            self.log_error(f"Deserialization error: {e}")
            # Try to handle non-JSON strings
            if json_str.startswith('{') or json_str.startswith('['):
                raise
            return {"raw_data": json_str}
    
    def encrypt_file(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """
        Encrypt a file
        
        Args:
            input_file: Path to input file
            output_file: Path to output file (optional, defaults to input_file.enc)
        
        Returns:
            True if successful
        """
        if not self.fernet:
            self.log_warning("Encryption not available")
            return False
        
        if not os.path.exists(input_file):
            self.log_error(f"Input file not found: {input_file}")
            return False
        
        if not output_file:
            output_file = f"{input_file}.enc"
        
        try:
            # Read file
            with open(input_file, 'rb') as f:
                file_data = f.read()
            
            # Encrypt
            encrypted_data = self.fernet.encrypt(file_data)
            
            # Write encrypted file
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            
            self.log_info(f"Encrypted {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            self.log_error(f"File encryption error: {e}")
            return False
    
    def decrypt_file(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """
        Decrypt a file
        
        Args:
            input_file: Path to encrypted file
            output_file: Path to output file (optional)
        
        Returns:
            True if successful
        """
        if not self.fernet:
            self.log_warning("Decryption not available")
            return False
        
        if not os.path.exists(input_file):
            self.log_error(f"Input file not found: {input_file}")
            return False
        
        if not output_file:
            # Remove .enc extension if present
            if input_file.endswith('.enc'):
                output_file = input_file[:-4]
            else:
                output_file = f"{input_file}.dec"
        
        try:
            # Read encrypted file
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Write decrypted file
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            self.log_info(f"Decrypted {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            self.log_error(f"File decryption error: {e}")
            return False
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        """
        Hash a password using PBKDF2
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
        
        Returns:
            Dict with hash and salt
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            self.log_warning("Using simple hash (cryptography not available)")
            return self.simple_hash(password)
        
        try:
            # Generate salt if not provided
            if not salt:
                salt = os.urandom(16)
            
            # Create PBKDF2 key derivation function
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # Derive key
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            return {
                'hash': key.decode('utf-8'),
                'salt': base64.urlsafe_b64encode(salt).decode('utf-8'),
                'algorithm': 'pbkdf2_sha256',
                'iterations': 100000
            }
            
        except Exception as e:
            self.log_error(f"Password hashing error: {e}")
            return self.simple_hash(password)
    
    def verify_password(self, password: str, hash_data: Dict) -> bool:
        """
        Verify a password against stored hash
        
        Args:
            password: Password to verify
            hash_data: Dict containing hash, salt, and algorithm info
        
        Returns:
            True if password matches
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            self.log_warning("Using simple verification")
            return self.simple_verify(password, hash_data)
        
        try:
            algorithm = hash_data.get('algorithm', '')
            
            if algorithm == 'pbkdf2_sha256':
                # Decode salt
                salt = base64.urlsafe_b64decode(hash_data['salt'].encode('utf-8'))
                
                # Hash the password with the same salt
                new_hash_data = self.hash_password(password, salt)
                
                # Compare hashes
                return new_hash_data['hash'] == hash_data['hash']
            
            elif algorithm == 'simple_sha256':
                return self.simple_verify(password, hash_data)
            
            else:
                self.log_error(f"Unknown hash algorithm: {algorithm}")
                return False
                
        except Exception as e:
            self.log_error(f"Password verification error: {e}")
            return False
    
    def simple_hash(self, password: str) -> Dict[str, str]:
        """Simple SHA256 hash (less secure fallback)"""
        # Generate salt
        salt = os.urandom(16).hex()
        
        # Hash password with salt
        hash_obj = hashlib.sha256()
        hash_obj.update(f"{password}{salt}".encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return {
            'hash': password_hash,
            'salt': salt,
            'algorithm': 'simple_sha256'
        }
    
    def simple_verify(self, password: str, hash_data: Dict) -> bool:
        """Simple password verification"""
        try:
            salt = hash_data['salt']
            stored_hash = hash_data['hash']
            
            # Compute hash
            hash_obj = hashlib.sha256()
            hash_obj.update(f"{password}{salt}".encode('utf-8'))
            computed_hash = hash_obj.hexdigest()
            
            return computed_hash == stored_hash
            
        except Exception as e:
            self.log_error(f"Simple verification error: {e}")
            return False
    
    def generate_secure_string(self, length: int = 32) -> str:
        """Generate a secure random string"""
        try:
            random_bytes = os.urandom(length)
            return base64.urlsafe_b64encode(random_bytes).decode('utf-8')[:length]
        except Exception as e:
            self.log_error(f"Secure string generation error: {e}")
            # Fallback to less secure method
            import random
            import string
            chars = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(chars) for _ in range(length))
    
    def encrypt_cookies(self, cookies: List[Dict], output_file: Optional[str] = None) -> bool:
        """
        Encrypt Facebook cookies
        
        Args:
            cookies: List of cookie dictionaries
            output_file: Output file path
        
        Returns:
            True if successful
        """
        if not output_file:
            output_file = "data/cookies/encrypted_cookies.json"
        
        try:
            # Prepare cookie data
            cookie_data = {
                'metadata': {
                    'encrypted_at': datetime.now().isoformat(),
                    'total_cookies': len(cookies),
                    'encryption': 'fernet_aes'
                },
                'cookies': cookies
            }
            
            # Encrypt
            encrypted = self.encrypt_data(cookie_data)
            
            # Save to file
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({'encrypted': True, 'data': encrypted}, f, indent=2)
            
            self.log_info(f"Encrypted {len(cookies)} cookies to {output_file}")
            return True
            
        except Exception as e:
            self.log_error(f"Cookie encryption error: {e}")
            return False
    
    def decrypt_cookies(self, input_file: str) -> Optional[List[Dict]]:
        """
        Decrypt Facebook cookies
        
        Args:
            input_file: Path to encrypted cookie file
        
        Returns:
            List of cookies or None if failed
        """
        if not os.path.exists(input_file):
            self.log_error(f"Cookie file not found: {input_file}")
            return None
        
        try:
            # Read file
            with open(input_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # Check if data is encrypted
            if not file_data.get('encrypted', False):
                self.log_warning(f"Cookie file not encrypted: {input_file}")
                return file_data.get('cookies', file_data.get('data', []))
            
            # Decrypt
            encrypted_data = file_data['data']
            decrypted = self.decrypt_data(encrypted_data)
            
            # Extract cookies
            if isinstance(decrypted, dict) and 'cookies' in decrypted:
                cookies = decrypted['cookies']
                self.log_info(f"Decrypted {len(cookies)} cookies from {input_file}")
                return cookies
            else:
                # Assume decrypted data is the cookies list
                self.log_info(f"Decrypted {len(decrypted) if isinstance(decrypted, list) else 1} items")
                return decrypted if isinstance(decrypted, list) else [decrypted]
                
        except Exception as e:
            self.log_error(f"Cookie decryption error: {e}")
            return None
    
    def get_encryption_status(self) -> Dict:
        """Get encryption system status"""
        return {
            'cryptography_available': CRYPTOGRAPHY_AVAILABLE,
            'key_loaded': self.key is not None,
            'fernet_initialized': self.fernet is not None,
            'key_file': self.key_file,
            'key_exists': os.path.exists(self.key_file) if self.key_file else False
        }
    
    def log_info(self, message: str):
        """Log info message"""
        print(f"[ENCRYPTION INFO] {message}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        print(f"[ENCRYPTION WARNING] {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"[ENCRYPTION ERROR] {message}")

if __name__ == "__main__":
    print("Encryption Module Loaded")
    
    # Test encryption
    print("\n🧪 Testing Encryption:")
    print("="*50)
    
    try:
        enc = Encryption("test_key.key")
        
        # Test status
        status = enc.get_encryption_status()
        print(f"Encryption Status: {status}")
        
        # Test data encryption
        print("\n🔐 Testing data encryption:")
        test_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'timestamp': datetime.now().isoformat()
        }
        
        encrypted = enc.encrypt_data(test_data)
        print(f"Original: {test_data}")
        print(f"Encrypted (first 50 chars): {encrypted[:50]}...")
        
        decrypted = enc.decrypt_data(encrypted)
        print(f"Decrypted: {decrypted}")
        
        # Test password hashing
        print("\n🔑 Testing password hashing:")
        password = "MySecurePassword123!"
        hash_data = enc.hash_password(password)
        print(f"Password hash generated")
        print(f"Algorithm: {hash_data.get('algorithm')}")
        
        # Test password verification
        verify_result = enc.verify_password(password, hash_data)
        print(f"Password verification: {'✅ Success' if verify_result else '❌ Failed'}")
        
        wrong_result = enc.verify_password("WrongPassword", hash_data)
        print(f"Wrong password verification: {'❌ Should fail' if not wrong_result else '⚠️ Unexpected success'}")
        
        # Test secure string generation
        print("\n🎲 Testing secure string generation:")
        secure_str = enc.generate_secure_string(16)
        print(f"Secure string: {secure_str}")
        
        # Test cookie encryption
        print("\n🍪 Testing cookie encryption:")
        test_cookies = [
            {'name': 'c_user', 'value': '1234567890', 'domain': '.facebook.com'},
            {'name': 'xs', 'value': 'abcdef123456', 'domain': '.facebook.com'}
        ]
        
        enc.encrypt_cookies(test_cookies, "test_cookies.json")
        print("Cookies encrypted to test_cookies.json")
        
        decrypted_cookies = enc.decrypt_cookies("test_cookies.json")
        print(f"Decrypted {len(decrypted_cookies) if decrypted_cookies else 0} cookies")
        
        # Cleanup test files
        import os
        for file in ["test_key.key", "test_cookies.json"]:
            if os.path.exists(file):
                os.remove(file)
                print(f"Cleaned up: {file}")
        
        print("\n✅ Encryption tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
