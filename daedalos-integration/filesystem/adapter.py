"""
daedalOS File System Adapter

Provides an adapter layer between Agent Zero and daedalOS BrowserFS.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class DaedalOSFileSystemAdapter:
    """
    Adapter for file system operations in daedalOS environment.
    
    Bridges Agent Zero file operations with daedalOS BrowserFS.
    """
    
    def __init__(self, base_path: str = "/home/agent-zero"):
        """
        Initialize the file system adapter.
        
        Args:
            base_path: Base path for agent files in daedalOS
        """
        self.base_path = Path(base_path)
        self.ensure_base_path()
    
    def ensure_base_path(self) -> None:
        """Ensure base path exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def resolve_path(self, file_path: str) -> Path:
        """
        Resolve a file path within the base path.
        
        Args:
            file_path: Relative or absolute file path
            
        Returns:
            Resolved Path object
            
        Raises:
            ValueError: If path is outside base path
        """
        resolved = (self.base_path / file_path).resolve()
        
        # Security check: ensure path is within base_path
        try:
            resolved.relative_to(self.base_path)
        except ValueError:
            raise ValueError(f"Path {file_path} is outside base path")
        
        return resolved
    
    def read_file(self, file_path: str) -> str:
        """
        Read file contents.
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents as string
        """
        path = self.resolve_path(file_path)
        return path.read_text()
    
    def write_file(self, file_path: str, content: str) -> None:
        """
        Write content to file.
        
        Args:
            file_path: Path to file
            content: Content to write
        """
        path = self.resolve_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    
    def append_file(self, file_path: str, content: str) -> None:
        """
        Append content to file.
        
        Args:
            file_path: Path to file
            content: Content to append
        """
        path = self.resolve_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'a') as f:
            f.write(content)
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Path to file
        """
        path = self.resolve_path(file_path)
        if path.exists():
            path.unlink()
    
    def create_directory(self, dir_path: str) -> None:
        """
        Create a directory.
        
        Args:
            dir_path: Path to directory
        """
        path = self.resolve_path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
    
    def list_directory(self, dir_path: str = ".") -> List[Dict[str, Any]]:
        """
        List directory contents.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            List of file/directory information
        """
        path = self.resolve_path(dir_path)
        
        if not path.is_dir():
            return []
        
        items = []
        for item in path.iterdir():
            stat = item.stat()
            items.append({
                'name': item.name,
                'path': str(item.relative_to(self.base_path)),
                'type': 'directory' if item.is_dir() else 'file',
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
        
        return sorted(items, key=lambda x: (x['type'] != 'directory', x['name']))
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file exists
        """
        try:
            path = self.resolve_path(file_path)
            return path.exists()
        except ValueError:
            return False
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get file information.
        
        Args:
            file_path: Path to file
            
        Returns:
            File information dictionary
        """
        try:
            path = self.resolve_path(file_path)
            if not path.exists():
                return None
            
            stat = path.stat()
            return {
                'name': path.name,
                'path': str(path.relative_to(self.base_path)),
                'type': 'directory' if path.is_dir() else 'file',
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'readable': os.access(path, os.R_OK),
                'writable': os.access(path, os.W_OK),
            }
        except (ValueError, OSError):
            return None
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Read JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        content = self.read_file(file_path)
        return json.loads(content)
    
    def write_json(self, file_path: str, data: Dict[str, Any]) -> None:
        """
        Write JSON file.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
        """
        content = json.dumps(data, indent=2)
        self.write_file(file_path, content)
    
    def copy_file(self, src: str, dst: str) -> None:
        """
        Copy a file.
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        src_path = self.resolve_path(src)
        dst_path = self.resolve_path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        dst_path.write_bytes(src_path.read_bytes())
    
    def move_file(self, src: str, dst: str) -> None:
        """
        Move a file.
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        src_path = self.resolve_path(src)
        dst_path = self.resolve_path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        src_path.rename(dst_path)
    
    def search_files(self, pattern: str, dir_path: str = ".") -> List[str]:
        """
        Search for files matching pattern.
        
        Args:
            pattern: File name pattern (supports *)
            dir_path: Directory to search in
            
        Returns:
            List of matching file paths
        """
        path = self.resolve_path(dir_path)
        matches = []
        
        for item in path.rglob(pattern):
            if item.is_file():
                matches.append(str(item.relative_to(self.base_path)))
        
        return sorted(matches)
