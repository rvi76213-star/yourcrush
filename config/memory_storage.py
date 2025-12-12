#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 Memory Storage System
Permanent and temporary memory storage with advanced features
"""

import json
import os
import pickle
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
import threading
import hashlib

from utils.logger import setup_logger
from utils.file_handler import FileHandler
from utils.encryption import Encryption


class MemoryStorage:
    """💾 Advanced Memory Storage System with SQLite backend"""
    
    def __init__(self):
        self.logger = setup_logger("memory_storage", "data/logs/memory.log")
        self.file_handler = FileHandler()
        self.encryption = Encryption()
        
        # Database connection
        self.db_path = "data/memory/memory.db"
        self.conn = None
        self.cursor = None
        
        # Cache system
        self.cache = {}
        self.cache_lock = threading.Lock()
        
        # Configuration
        self.config = {
            "max_cache_size": 100,  # MB
            "cache_expiry": 3600,   # 1 hour
            "auto_cleanup_interval": 300,  # 5 minutes
            "backup_interval": 86400,  # 24 hours
            "encrypt_sensitive": True,
            "compression": True,
            "use_sqlite": True
        }
        
        # Initialize
        self.initialize()
    
    def initialize(self):
        """Initialize memory storage system"""
        try:
            self.logger.info("💾 Initializing Advanced Memory Storage...")
            
            # Create directories
            os.makedirs("data/memory", exist_ok=True)
            os.makedirs("data/memory/backups", exist_ok=True)
            os.makedirs("data/memory/cache", exist_ok=True)
            
            # Initialize database
            self._init_database()
            
            # Start cleanup thread
            self._start_cleanup_thread()
            
            # Start backup thread
            self._start_backup_thread()
            
            self.logger.info("✅ Memory Storage initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing memory storage: {e}")
            raise
    
    def _init_database(self):
        """Initialize SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            
            # Create tables
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS permanent_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value BLOB NOT NULL,
                    metadata TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    UNIQUE(category, key)
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS temporary_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cache_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    hit_count INTEGER DEFAULT 0
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_memories (
                    user_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    PRIMARY KEY (user_id, memory_type, key)
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_memories (
                    conversation_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    messages TEXT NOT NULL,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_permanent_category ON permanent_memory(category)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_permanent_expires ON permanent_memory(expires_at)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_memories ON user_memories(user_id)')
            
            self.conn.commit()
            self.logger.info("📊 Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing database: {e}")
            raise
    
    def store(self, category: str, key: str, value: Any, 
              memory_type: str = "permanent", expire_seconds: int = None,
              metadata: Dict = None) -> bool:
        """
        Store data in memory
        
        Args:
            category: Memory category
            key: Unique key
            value: Data to store
            memory_type: Type of memory (permanent/temporary/cache)
            expire_seconds: Expiration time in seconds
            metadata: Additional metadata
        
        Returns:
            bool: True if successful
        """
        try:
            # Prepare data
            serialized_value = self._serialize_value(value)
            expires_at = None
            if expire_seconds:
                expires_at = datetime.now() + timedelta(seconds=expire_seconds)
            
            metadata_json = json.dumps(metadata or {})
            
            if memory_type == "permanent":
                # Store in permanent memory
                self.cursor.execute('''
                    INSERT OR REPLACE INTO permanent_memory 
                    (category, key, value, metadata, expires_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (category, key, serialized_value, metadata_json, expires_at))
                
            elif memory_type == "temporary":
                # Store in temporary memory
                if not expires_at:
                    expires_at = datetime.now() + timedelta(hours=1)
                
                self.cursor.execute('''
                    INSERT OR REPLACE INTO temporary_memory 
                    (key, value, expires_at)
                    VALUES (?, ?, ?)
                ''', (key, serialized_value, expires_at))
                
            elif memory_type == "cache":
                # Store in cache
                if not expires_at:
                    expires_at = datetime.now() + timedelta(seconds=self.config["cache_expiry"])
                
                self.cursor.execute('''
                    INSERT OR REPLACE INTO cache_memory 
                    (key, value, expires_at)
                    VALUES (?, ?, ?)
                ''', (key, serialized_value, expires_at))
            
            self.conn.commit()
            
            # Update in-memory cache
            cache_key = f"{memory_type}_{category}_{key}" if memory_type == "permanent" else f"{memory_type}_{key}"
            with self.cache_lock:
                self.cache[cache_key] = {
                    "value": value,
                    "timestamp": time.time(),
                    "expires_at": expires_at.timestamp() if expires_at else None
                }
            
            self.logger.debug(f"💾 Stored {memory_type}:{category}:{key}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error storing memory: {e}")
            return False
    
    def retrieve(self, category: str, key: str, 
                memory_type: str = "permanent") -> Optional[Any]:
        """
        Retrieve data from memory
        
        Args:
            category: Memory category
            key: Unique key
            memory_type: Type of memory (permanent/temporary/cache)
        
        Returns:
            Any: Retrieved value or None
        """
        try:
            # Check in-memory cache first
            cache_key = f"{memory_type}_{category}_{key}" if memory_type == "permanent" else f"{memory_type}_{key}"
            with self.cache_lock:
                if cache_key in self.cache:
                    cached = self.cache[cache_key]
                    if cached["expires_at"] and time.time() > cached["expires_at"]:
                        del self.cache[cache_key]
                    else:
                        # Update access time
                        cached["timestamp"] = time.time()
                        return cached["value"]
            
            # Retrieve from database
            if memory_type == "permanent":
                self.cursor.execute('''
                    SELECT value, expires_at FROM permanent_memory 
                    WHERE category = ? AND key = ? 
                    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                ''', (category, key))
                
                result = self.cursor.fetchone()
                if result:
                    # Update access count
                    self.cursor.execute('''
                        UPDATE permanent_memory 
                        SET access_count = access_count + 1,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE category = ? AND key = ?
                    ''', (category, key))
                    self.conn.commit()
                    
                    value = self._deserialize_value(result["value"])
                    
                    # Cache in memory
                    with self.cache_lock:
                        self.cache[cache_key] = {
                            "value": value,
                            "timestamp": time.time(),
                            "expires_at": result["expires_at"]
                        }
                    
                    return value
            
            elif memory_type == "temporary":
                self.cursor.execute('''
                    SELECT value FROM temporary_memory 
                    WHERE key = ? AND expires_at > CURRENT_TIMESTAMP
                ''', (key,))
                
                result = self.cursor.fetchone()
                if result:
                    value = self._deserialize_value(result["value"])
                    
                    # Cache in memory
                    with self.cache_lock:
                        self.cache[cache_key] = {
                            "value": value,
                            "timestamp": time.time()
                        }
                    
                    return value
            
            elif memory_type == "cache":
                self.cursor.execute('''
                    SELECT value, expires_at FROM cache_memory 
                    WHERE key = ? AND expires_at > CURRENT_TIMESTAMP
                ''', (key,))
                
                result = self.cursor.fetchone()
                if result:
                    # Update hit count
                    self.cursor.execute('''
                        UPDATE cache_memory 
                        SET hit_count = hit_count + 1
                        WHERE key = ?
                    ''', (key,))
                    self.conn.commit()
                    
                    value = self._deserialize_value(result["value"])
                    
                    # Cache in memory
                    with self.cache_lock:
                        self.cache[cache_key] = {
                            "value": value,
                            "timestamp": time.time(),
                            "expires_at": result["expires_at"]
                        }
                    
                    return value
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving memory: {e}")
            return None
    
    def remember_conversation(self, user_id: str, messages: List[Dict], 
                             summary: str = None) -> str:
        """
        Remember conversation with user
        
        Args:
            user_id: User ID
            messages: List of messages
            summary: Conversation summary
        
        Returns:
            str: Conversation ID
        """
        try:
            conversation_id = hashlib.md5(f"{user_id}_{time.time()}".encode()).hexdigest()[:12]
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO conversation_memories 
                (conversation_id, user_id, messages, summary, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (conversation_id, user_id, json.dumps(messages), summary))
            
            self.conn.commit()
            
            # Also store in user memories
            self.store(
                category="users",
                key=f"conversation_{conversation_id}",
                value={
                    "messages": messages,
                    "summary": summary,
                    "timestamp": time.time()
                },
                memory_type="permanent",
                expire_seconds=86400 * 7  # 7 days
            )
            
            self.logger.debug(f"💾 Remembered conversation {conversation_id} with {user_id}")
            return conversation_id
            
        except Exception as e:
            self.logger.error(f"❌ Error remembering conversation: {e}")
            return ""
    
    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's recent conversations"""
        try:
            self.cursor.execute('''
                SELECT * FROM conversation_memories 
                WHERE user_id = ? 
                ORDER BY updated_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            conversations = []
            for row in self.cursor.fetchall():
                conversations.append({
                    "conversation_id": row["conversation_id"],
                    "messages": json.loads(row["messages"]),
                    "summary": row["summary"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                })
            
            return conversations
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user conversations: {e}")
            return []
    
    def store_user_memory(self, user_id: str, memory_type: str, 
                         key: str, value: Any, expire_seconds: int = None) -> bool:
        """Store user-specific memory"""
        try:
            serialized_value = self._serialize_value(value)
            expires_at = None
            if expire_seconds:
                expires_at = datetime.now() + timedelta(seconds=expire_seconds)
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_memories 
                (user_id, memory_type, key, value, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, memory_type, key, serialized_value, expires_at))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error storing user memory: {e}")
            return False
    
    def get_user_memories(self, user_id: str, memory_type: str = None) -> Dict:
        """Get all memories for a user"""
        try:
            if memory_type:
                self.cursor.execute('''
                    SELECT * FROM user_memories 
                    WHERE user_id = ? AND memory_type = ?
                    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                ''', (user_id, memory_type))
            else:
                self.cursor.execute('''
                    SELECT * FROM user_memories 
                    WHERE user_id = ?
                    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                ''', (user_id,))
            
            memories = {}
            for row in self.cursor.fetchall():
                mem_type = row["memory_type"]
                if mem_type not in memories:
                    memories[mem_type] = {}
                
                memories[mem_type][row["key"]] = self._deserialize_value(row["value"])
            
            return memories
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user memories: {e}")
            return {}
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for storage"""
        try:
            if self.config["compression"]:
                return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                return json.dumps(value, ensure_ascii=False).encode('utf-8')
        except:
            return str(value).encode('utf-8')
    
    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from storage"""
        try:
            if self.config["compression"]:
                return pickle.loads(data)
            else:
                return json.loads(data.decode('utf-8'))
        except:
            return data.decode('utf-8')
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        def cleanup():
            while True:
                time.sleep(self.config["auto_cleanup_interval"])
                self.cleanup_expired_memories()
        
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()
    
    def _start_backup_thread(self):
        """Start background backup thread"""
        def backup():
            while True:
                time.sleep(self.config["backup_interval"])
                self.backup_memory()
        
        thread = threading.Thread(target=backup, daemon=True)
        thread.start()
    
    def cleanup_expired_memories(self):
        """Clean up expired memories"""
        try:
            deleted_count = 0
            
            # Clean temporary memory
            self.cursor.execute('DELETE FROM temporary_memory WHERE expires_at <= CURRENT_TIMESTAMP')
            deleted_count += self.cursor.rowcount
            
            # Clean cache memory
            self.cursor.execute('DELETE FROM cache_memory WHERE expires_at <= CURRENT_TIMESTAMP')
            deleted_count += self.cursor.rowcount
            
            # Clean user memories
            self.cursor.execute('DELETE FROM user_memories WHERE expires_at <= CURRENT_TIMESTAMP')
            deleted_count += self.cursor.rowcount
            
            # Clean permanent memory
            self.cursor.execute('DELETE FROM permanent_memory WHERE expires_at <= CURRENT_TIMESTAMP')
            deleted_count += self.cursor.rowcount
            
            # Clean in-memory cache
            current_time = time.time()
            with self.cache_lock:
                keys_to_delete = []
                for key, data in self.cache.items():
                    if data.get("expires_at") and current_time > data["expires_at"]:
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self.cache[key]
                    deleted_count += 1
            
            self.conn.commit()
            
            if deleted_count > 0:
                self.logger.info(f"🧹 Cleaned {deleted_count} expired memories")
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning expired memories: {e}")
    
    def backup_memory(self) -> str:
        """Create backup of all memory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"data/memory/backups/{timestamp}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup database
            backup_db_path = f"{backup_dir}/memory.db"
            import shutil
            shutil.copy2(self.db_path, backup_db_path)
            
            # Backup statistics
            stats = self.get_statistics()
            stats_file = f"{backup_dir}/statistics.json"
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            # Compress backup
            backup_zip = f"{backup_dir}.zip"
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            shutil.rmtree(backup_dir)
            
            self.logger.info(f"💾 Memory backup created: {backup_zip}")
            return backup_zip
            
        except Exception as e:
            self.logger.error(f"❌ Error backing up memory: {e}")
            return ""
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        try:
            stats = {}
            
            # Permanent memory stats
            self.cursor.execute('SELECT COUNT(*) as count FROM permanent_memory')
            stats["permanent_entries"] = self.cursor.fetchone()["count"]
            
            # Temporary memory stats
            self.cursor.execute('SELECT COUNT(*) as count FROM temporary_memory')
            stats["temporary_entries"] = self.cursor.fetchone()["count"]
            
            # Cache stats
            self.cursor.execute('SELECT COUNT(*) as count, SUM(hit_count) as total_hits FROM cache_memory')
            cache_result = self.cursor.fetchone()
            stats["cache_entries"] = cache_result["count"] or 0
            stats["cache_hits"] = cache_result["total_hits"] or 0
            
            # User memories stats
            self.cursor.execute('SELECT COUNT(DISTINCT user_id) as users FROM user_memories')
            stats["users_with_memories"] = self.cursor.fetchone()["users"]
            
            # Conversation stats
            self.cursor.execute('SELECT COUNT(*) as count FROM conversation_memories')
            stats["conversations"] = self.cursor.fetchone()["count"]
            
            # Database size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            stats["database_size_mb"] = round(db_size / (1024 * 1024), 2)
            
            # Cache size
            with self.cache_lock:
                stats["memory_cache_entries"] = len(self.cache)
            
            stats["last_cleanup"] = datetime.now().isoformat()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Error getting statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
                self.logger.info("✅ Memory storage closed")
        except Exception as e:
            self.logger.error(f"❌ Error closing memory storage: {e}")


# Singleton instance
memory_storage = None

def get_memory_storage() -> MemoryStorage:
    """Get memory storage instance (singleton)"""
    global memory_storage
    if memory_storage is None:
        memory_storage = MemoryStorage()
    return memory_storage