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