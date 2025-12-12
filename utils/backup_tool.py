"""
💾 Backup Tool Module for data backup and restoration
"""

import os
import json
import shutil
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path

class BackupTool:
    """Backup and restoration tool"""
    
    def __init__(self, backup_dir="data/backup"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup configuration
        self.config = {
            "auto_backup": True,
            "backup_interval": 3600,  # 1 hour
            "max_backups": 30,
            "compress_backups": True,
            "encrypt_backups": False,
            "include_logs": True,
            "include_cookies": True,
            "include_photos": True,
            "include_config": True,
            "include_data": True
        }
        
        self.backup_history = []
        self.load_history()
    
    def create_backup(self, backup_name=None, description=""):
        """Create a new backup"""
        try:
            # Generate backup name
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}"
            
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)
            
            # Files and directories to backup
            backup_items = []
            
            if self.config["include_cookies"]:
                backup_items.append("data/cookies")
            
            if self.config["include_photos"]:
                backup_items.append("data/photos")
            
            if self.config["include_config"]:
                backup_items.extend(["config.json", "bot_identity.json"])
            
            if self.config["include_data"]:
                backup_items.extend([
                    "data/commands",
                    "data/learning",
                    "data/json_responses",
                    "data/users",
                    "data/groups"
                ])
            
            if self.config["include_logs"]:
                backup_items.append("data/logs")
            
            # Copy files
            copied_files = []
            for item in backup_items:
                source_path = Path(item)
                if source_path.exists():
                    dest_path = backup_path / item
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if source_path.is_file():
                        shutil.copy2(source_path, dest_path)
                        copied_files.append(str(source_path))
                    else:
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                        copied_files.append(f"{item}/ (directory)")
            
            # Create backup info
            backup_info = {
                "name": backup_name,
                "timestamp": datetime.now().isoformat(),
                "description": description,
                "file_count": len(copied_files),
                "files": copied_files,
                "size_bytes": self.get_directory_size(backup_path),
                "checksum": self.calculate_checksum(backup_path)
            }
            
            # Save backup info
            info_file = backup_path / "backup_info.json"
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            # Compress if enabled
            if self.config["compress_backups"]:
                self.compress_backup(backup_path)
            
            # Add to history
            self.backup_history.append(backup_info)
            self.save_history()
            
            # Clean old backups
            self.clean_old_backups()
            
            return True, backup_info
            
        except Exception as e:
            return False, f"Backup failed: {e}"
    
    def compress_backup(self, backup_path):
        """Compress backup directory"""
        try:
            zip_path = backup_path.with_suffix(".zip")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(backup_path.parent)
                        zipf.write(file_path, arcname)
            
            # Remove original directory
            shutil.rmtree(backup_path)
            
            return True, str(zip_path)
            
        except Exception as e:
            return False, f"Compression failed: {e}"
    
    def restore_backup(self, backup_name, restore_path="."):
        """Restore from backup"""
        try:
            backup_path = self.backup_dir / backup_name
            
            # Check if backup exists
            if not backup_path.exists():
                # Try compressed version
                zip_path = backup_path.with_suffix(".zip")
                if zip_path.exists():
                    backup_path = zip_path
                else:
                    return False, f"Backup not found: {backup_name}"
            
            # Restore from zip
            if str(backup_path).endswith('.zip'):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(restore_path)
                return True, f"Restored from {backup_name}.zip"
            
            # Restore from directory
            else:
                # Read backup info
                info_file = backup_path / "backup_info.json"
                if info_file.exists():
                    with open(info_file, "r", encoding="utf-8") as f:
                        backup_info = json.load(f)
                
                # Copy files
                for item in os.listdir(backup_path):
                    if item == "backup_info.json":
                        continue
                    
                    source = backup_path / item
                    destination = Path(restore_path) / item
                    
                    if source.is_file():
                        shutil.copy2(source, destination)
                    else:
                        shutil.copytree(source, destination, dirs_exist_ok=True)
                
                return True, f"Restored {len(backup_info.get('files', []))} files"
                
        except Exception as e:
            return False, f"Restore failed: {e}"
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        
        # Scan backup directory
        for item in self.backup_dir.iterdir():
            backup_info = {}
            
            if item.is_dir():
                info_file = item / "backup_info.json"
                if info_file.exists():
                    try:
                        with open(info_file, "r", encoding="utf-8") as f:
                            backup_info = json.load(f)
                    except:
                        backup_info = {"name": item.name, "error": "Invalid info file"}
            elif item.suffix == '.zip':
                backup_info = {
                    "name": item.stem,
                    "compressed": True,
                    "size_bytes": item.stat().st_size
                }
            
            if backup_info:
                backups.append(backup_info)
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return backups
    
    def get_backup_info(self, backup_name):
        """Get detailed backup information"""
        backup_path = self.backup_dir / backup_name
        
        # Check directory
        if backup_path.is_dir():
            info_file = backup_path / "backup_info.json"
            if info_file.exists():
                try:
                    with open(info_file, "r", encoding="utf-8") as f:
                        return json.load(f)
                except:
                    pass
        
        # Check zip file
        zip_path = backup_path.with_suffix(".zip")
        if zip_path.exists():
            return {
                "name": backup_name,
                "compressed": True,
                "size_bytes": zip_path.stat().st_size,
                "exists": True
            }
        
        return {"name": backup_name, "exists": False}
    
    def clean_old_backups(self):
        """Clean old backups based on retention policy"""
        backups = self.list_backups()
        
        if len(backups) <= self.config["max_backups"]:
            return
        
        # Sort by timestamp (oldest first)
        backups.sort(key=lambda x: x.get("timestamp", ""))
        
        # Remove oldest backups
        to_remove = backups[:len(backups) - self.config["max_backups"]]
        
        for backup in to_remove:
            backup_name = backup["name"]
            self.delete_backup(backup_name)
    
    def delete_backup(self, backup_name):
        """Delete a backup"""
        try:
            # Try directory
            backup_path = self.backup_dir / backup_name
            if backup_path.exists():
                if backup_path.is_dir():
                    shutil.rmtree(backup_path)
                else:
                    backup_path.unlink()
            
            # Try zip file
            zip_path = backup_path.with_suffix(".zip")
            if zip_path.exists():
                zip_path.unlink()
            
            # Remove from history
            self.backup_history = [b for b in self.backup_history if b["name"] != backup_name]
            self.save_history()
            
            return True, f"Deleted backup: {backup_name}"
            
        except Exception as e:
            return False, f"Delete failed: {e}"
    
    def calculate_checksum(self, path):
        """Calculate checksum for directory"""
        if path.is_file():
            return self.calculate_file_checksum(path)
        
        # For directories, combine checksums of all files
        checksums = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = Path(root) / file
                checksums.append(self.calculate_file_checksum(file_path))
        
        if not checksums:
            return ""
        
        # Combine all checksums
        combined = "".join(checksums)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def calculate_file_checksum(self, file_path):
        """Calculate MD5 checksum for file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return ""
    
    def get_directory_size(self, path):
        """Get size of directory in bytes"""
        if path.is_file():
            return path.stat().st_size
        
        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
        
        return total_size
    
    def load_history(self):
        """Load backup history"""
        history_file = self.backup_dir / "backup_history.json"
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    self.backup_history = json.load(f)
            except:
                self.backup_history = []
    
    def save_history(self):
        """Save backup history"""
        history_file = self.backup_dir / "backup_history.json"
        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.backup_history, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def verify_backup(self, backup_name):
        """Verify backup integrity"""
        backup_info = self.get_backup_info(backup_name)
        
        if not backup_info.get("exists", False):
            return False, "Backup not found"
        
        if backup_info.get("compressed", False):
            # Verify zip file
            zip_path = (self.backup_dir / backup_name).with_suffix(".zip")
            if not zipfile.is_zipfile(zip_path):
                return False, "Invalid zip file"
            return True, "Zip file verified"
        else:
            # Verify directory
            backup_path = self.backup_dir / backup_name
            if not backup_path.exists():
                return False, "Backup directory not found"
            
            # Verify checksum
            current_checksum = self.calculate_checksum(backup_path)
            original_checksum = backup_info.get("checksum", "")
            
            if current_checksum and original_checksum:
                if current_checksum == original_checksum:
                    return True, "Checksum verified"
                else:
                    return False, "Checksum mismatch"
            
            return True, "Backup exists (checksum not available)"

if __name__ == "__main__":
    print("Backup Tool Module Loaded")
    
    # Test backup tool
    backup_tool = BackupTool()
    
    print("\nBackup Tool Test:")
    
    # Create test backup
    success, result = backup_tool.create_backup("test_backup", "Test backup")
    if success:
        print(f"✅ Backup created: {result['name']}")
        print(f"  Size: {result['size_bytes']:,} bytes")
        print(f"  Files: {result['file_count']}")
    else:
        print(f"❌ Backup failed: {result}")
    
    # List backups
    backups = backup_tool.list_backups()
    print(f"\n📂 Total backups: {len(backups)}")
    
    if backups:
        latest = backups[0]
        print(f"Latest backup: {latest.get('name', 'N/A')}")
        print(f"Timestamp: {latest.get('timestamp', 'N/A')}")
    
    # Test verification
    if backups:
        backup_name = backups[0]["name"]
        verified, message = backup_tool.verify_backup(backup_name)
        print(f"\n🔍 Verification for '{backup_name}': {message}")