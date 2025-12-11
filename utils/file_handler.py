#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 File Handling Utilities
File operations, reading, writing, and management
"""

import json
import os
import shutil
import zipfile
import pickle
import csv
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging


class FileHandler:
    """📁 File Handling and Management"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()
        self.logger = logging.getLogger(__name__)
    
    def ensure_directory(self, directory: str) -> bool:
        """
        Ensure directory exists, create if it doesn't
        
        Args:
            directory: Directory path
        
        Returns:
            True if directory exists or was created
        """
        try:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Error creating directory {directory}: {e}")
            return False
    
    def read_json(self, file_path: str, default: Any = None) -> Any:
        """
        Read JSON file
        
        Args:
            file_path: Path to JSON file
            default: Default value if file doesn't exist
        
        Returns:
            Parsed JSON data
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                if default is not None:
                    return default
                raise FileNotFoundError(f"File not found: {full_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON file {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error reading JSON file {file_path}: {e}")
            raise
    
    def write_json(self, file_path: str, data: Any, indent: int = 2, ensure_ascii: bool = False) -> bool:
        """
        Write data to JSON file
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            indent: JSON indentation
            ensure_ascii: Ensure ASCII encoding
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    def read_text(self, file_path: str, default: str = "") -> str:
        """
        Read text file
        
        Args:
            file_path: Path to text file
            default: Default value if file doesn't exist
        
        Returns:
            File content as string
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return default
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error reading text file {file_path}: {e}")
            return default
    
    def write_text(self, file_path: str, content: str, mode: str = 'w') -> bool:
        """
        Write text to file
        
        Args:
            file_path: Path to text file
            content: Content to write
            mode: Write mode ('w' for write, 'a' for append)
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing text file {file_path}: {e}")
            return False
    
    def read_lines(self, file_path: str, strip: bool = True) -> List[str]:
        """
        Read file as list of lines
        
        Args:
            file_path: Path to text file
            strip: Whether to strip whitespace from lines
        
        Returns:
            List of lines
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return []
            
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if strip:
                lines = [line.strip() for line in lines]
            
            return lines
            
        except Exception as e:
            self.logger.error(f"Error reading lines from {file_path}: {e}")
            return []
    
    def write_lines(self, file_path: str, lines: List[str], mode: str = 'w') -> bool:
        """
        Write list of lines to file
        
        Args:
            file_path: Path to text file
            lines: List of lines to write
            mode: Write mode
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, mode, encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing lines to {file_path}: {e}")
            return False
    
    def read_yaml(self, file_path: str, default: Any = None) -> Any:
        """
        Read YAML file
        
        Args:
            file_path: Path to YAML file
            default: Default value if file doesn't exist
        
        Returns:
            Parsed YAML data
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                if default is not None:
                    return default
                raise FileNotFoundError(f"File not found: {full_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
                
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error reading YAML file {file_path}: {e}")
            raise
    
    def write_yaml(self, file_path: str, data: Any) -> bool:
        """
        Write data to YAML file
        
        Args:
            file_path: Path to YAML file
            data: Data to write
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing YAML file {file_path}: {e}")
            return False
    
    def read_csv(self, file_path: str, delimiter: str = ',') -> List[List[str]]:
        """
        Read CSV file
        
        Args:
            file_path: Path to CSV file
            delimiter: CSV delimiter
        
        Returns:
            List of rows
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return []
            
            with open(full_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                return [row for row in reader]
                
        except Exception as e:
            self.logger.error(f"Error reading CSV file {file_path}: {e}")
            return []
    
    def write_csv(self, file_path: str, data: List[List[str]], delimiter: str = ',') -> bool:
        """
        Write data to CSV file
        
        Args:
            file_path: Path to CSV file
            data: List of rows to write
            delimiter: CSV delimiter
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerows(data)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file {file_path}: {e}")
            return False
    
    def read_pickle(self, file_path: str, default: Any = None) -> Any:
        """
        Read pickle file
        
        Args:
            file_path: Path to pickle file
            default: Default value if file doesn't exist
        
        Returns:
            Unpickled data
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                if default is not None:
                    return default
                raise FileNotFoundError(f"File not found: {full_path}")
            
            with open(full_path, 'rb') as f:
                return pickle.load(f)
                
        except Exception as e:
            self.logger.error(f"Error reading pickle file {file_path}: {e}")
            raise
    
    def write_pickle(self, file_path: str, data: Any) -> bool:
        """
        Write data to pickle file
        
        Args:
            file_path: Path to pickle file
            data: Data to pickle
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            # Ensure directory exists
            self.ensure_directory(os.path.dirname(full_path))
            
            with open(full_path, 'wb') as f:
                pickle.dump(data, f)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing pickle file {file_path}: {e}")
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists
        
        Args:
            file_path: Path to check
        
        Returns:
            True if file exists
        """
        full_path = os.path.join(self.base_dir, file_path)
        return os.path.exists(full_path)
    
    def directory_exists(self, directory: str) -> bool:
        """
        Check if directory exists
        
        Args:
            directory: Directory path
        
        Returns:
            True if directory exists
        """
        full_path = os.path.join(self.base_dir, directory)
        return os.path.exists(full_path) and os.path.isdir(full_path)
    
    def list_files(self, directory: str, pattern: str = "*") -> List[str]:
        """
        List files in directory
        
        Args:
            directory: Directory path
            pattern: File pattern (e.g., "*.txt")
        
        Returns:
            List of file names
        """
        try:
            full_path = os.path.join(self.base_dir, directory)
            
            if not os.path.exists(full_path):
                return []
            
            files = []
            for file in os.listdir(full_path):
                if os.path.isfile(os.path.join(full_path, file)):
                    if pattern == "*" or file.endswith(pattern.replace("*", "")):
                        files.append(file)
            
            return sorted(files)
            
        except Exception as e:
            self.logger.error(f"Error listing files in {directory}: {e}")
            return []
    
    def list_directories(self, directory: str) -> List[str]:
        """
        List subdirectories in directory
        
        Args:
            directory: Directory path
        
        Returns:
            List of directory names
        """
        try:
            full_path = os.path.join(self.base_dir, directory)
            
            if not os.path.exists(full_path):
                return []
            
            dirs = []
            for item in os.listdir(full_path):
                if os.path.isdir(os.path.join(full_path, item)):
                    dirs.append(item)
            
            return sorted(dirs)
            
        except Exception as e:
            self.logger.error(f"Error listing directories in {directory}: {e}")
            return []
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes
        
        Args:
            file_path: Path to file
        
        Returns:
            File size in bytes, or -1 if error
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return -1
            
            return os.path.getsize(full_path)
            
        except Exception as e:
            self.logger.error(f"Error getting file size for {file_path}: {e}")
            return -1
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file information
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary with file info
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return {"error": "File not found"}
            
            stat = os.stat(full_path)
            
            return {
                "path": full_path,
                "size_bytes": stat.st_size,
                "size_mb": stat.st_size / (1024 * 1024),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "is_file": os.path.isfile(full_path),
                "is_dir": os.path.isdir(full_path),
                "extension": os.path.splitext(full_path)[1],
                "filename": os.path.basename(full_path),
                "directory": os.path.dirname(full_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {e}")
            return {"error": str(e)}
    
    def copy_file(self, source: str, destination: str, overwrite: bool = True) -> bool:
        """
        Copy file
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Overwrite if exists
        
        Returns:
            True if successful
        """
        try:
            source_path = os.path.join(self.base_dir, source)
            dest_path = os.path.join(self.base_dir, destination)
            
            if not os.path.exists(source_path):
                self.logger.error(f"Source file not found: {source_path}")
                return False
            
            if os.path.exists(dest_path) and not overwrite:
                self.logger.error(f"Destination file exists: {dest_path}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory(os.path.dirname(dest_path))
            
            shutil.copy2(source_path, dest_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Error copying file {source} to {destination}: {e}")
            return False
    
    def move_file(self, source: str, destination: str, overwrite: bool = True) -> bool:
        """
        Move/rename file
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Overwrite if exists
        
        Returns:
            True if successful
        """
        try:
            source_path = os.path.join(self.base_dir, source)
            dest_path = os.path.join(self.base_dir, destination)
            
            if not os.path.exists(source_path):
                self.logger.error(f"Source file not found: {source_path}")
                return False
            
            if os.path.exists(dest_path) and not overwrite:
                self.logger.error(f"Destination file exists: {dest_path}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory(os.path.dirname(dest_path))
            
            shutil.move(source_path, dest_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file {source} to {destination}: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file
        
        Args:
            file_path: Path to file
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(full_path):
                return True  # Already doesn't exist
            
            os.remove(full_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def delete_directory(self, directory: str, recursive: bool = True) -> bool:
        """
        Delete directory
        
        Args:
            directory: Directory path
            recursive: Delete recursively
        
        Returns:
            True if successful
        """
        try:
            full_path = os.path.join(self.base_dir, directory)
            
            if not os.path.exists(full_path):
                return True  # Already doesn't exist
            
            if recursive:
                shutil.rmtree(full_path)
            else:
                os.rmdir(full_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting directory {directory}: {e}")
            return False
    
    def create_zip(self, source_dir: str, zip_file: str, include_base_dir: bool = False) -> bool:
        """
        Create zip archive
        
        Args:
            source_dir: Source directory
            zip_file: Output zip file path
            include_base_dir: Include base directory in zip
        
        Returns:
            True if successful
        """
        try:
            source_path = os.path.join(self.base_dir, source_dir)
            zip_path = os.path.join(self.base_dir, zip_file)
            
            if not os.path.exists(source_path):
                self.logger.error(f"Source directory not found: {source_path}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory(os.path.dirname(zip_path))
            
            if include_base_dir:
                base_dir = os.path.basename(source_path.rstrip('/\\'))
                shutil.make_archive(zip_path.replace('.zip', ''), 'zip', source_path, base_dir)
            else:
                shutil.make_archive(zip_path.replace('.zip', ''), 'zip', source_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating zip {zip_file}: {e}")
            return False
    
    def extract_zip(self, zip_file: str, extract_dir: str) -> bool:
        """
        Extract zip archive
        
        Args:
            zip_file: Zip file path
            extract_dir: Extraction directory
        
        Returns:
            True if successful
        """
        try:
            zip_path = os.path.join(self.base_dir, zip_file)
            extract_path = os.path.join(self.base_dir, extract_dir)
            
            if not os.path.exists(zip_path):
                self.logger.error(f"Zip file not found: {zip_path}")
                return False
            
            # Ensure extraction directory exists
            self.ensure_directory(extract_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting zip {zip_file}: {e}")
            return False
    
    def search_files(self, directory: str, search_term: str, recursive: bool = True) -> List[str]:
        """
        Search for files containing search term
        
        Args:
            directory: Directory to search
            search_term: Term to search for
            recursive: Search recursively
        
        Returns:
            List of matching file paths
        """
        try:
            search_path = os.path.join(self.base_dir, directory)
            
            if not os.path.exists(search_path):
                return []
            
            matches = []
            
            if recursive:
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if search_term.lower() in file.lower():
                            rel_path = os.path.relpath(os.path.join(root, file), self.base_dir)
                            matches.append(rel_path)
            else:
                for file in os.listdir(search_path):
                    if os.path.isfile(os.path.join(search_path, file)):
                        if search_term.lower() in file.lower():
                            rel_path = os.path.relpath(os.path.join(search_path, file), self.base_dir)
                            matches.append(rel_path)
            
            return sorted(matches)
            
        except Exception as e:
            self.logger.error(f"Error searching files in {directory}: {e}")
            return []
    
    def backup_file(self, file_path: str, backup_dir: str = "backups") -> Optional[str]:
        """
        Create backup of file
        
        Args:
            file_path: File to backup
            backup_dir: Backup directory
        
        Returns:
            Backup file path or None if failed
        """
        try:
            source_path = os.path.join(self.base_dir, file_path)
            
            if not os.path.exists(source_path):
                self.logger.error(f"File not found for backup: {source_path}")
                return None
            
            # Create backup directory
            backup_path = os.path.join(self.base_dir, backup_dir)
            self.ensure_directory(backup_path)
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            backup_file = f"{filename}.{timestamp}.bak"
            backup_file_path = os.path.join(backup_path, backup_file)
            
            # Copy file
            shutil.copy2(source_path, backup_file_path)
            
            # Return relative path
            return os.path.relpath(backup_file_path, self.base_dir)
            
        except Exception as e:
            self.logger.error(f"Error backing up file {file_path}: {e}")
            return None