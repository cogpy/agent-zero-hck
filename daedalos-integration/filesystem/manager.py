"""
File System Manager for daedalOS Integration

Manages file system operations and provides high-level file management.
"""

from typing import Optional, List, Dict, Any
from .adapter import DaedalOSFileSystemAdapter


class FileSystemManager:
    """
    High-level file system manager for Agent Zero in daedalOS.
    """
    
    def __init__(self, base_path: str = "/home/agent-zero"):
        """
        Initialize file system manager.
        
        Args:
            base_path: Base path for agent files
        """
        self.adapter = DaedalOSFileSystemAdapter(base_path)
        self._initialize_directories()
    
    def _initialize_directories(self) -> None:
        """Initialize standard directories."""
        directories = [
            "memory",
            "knowledge",
            "prompts",
            "logs",
            "config",
            "cache",
            "tmp",
        ]
        
        for dir_name in directories:
            self.adapter.create_directory(dir_name)
    
    def save_memory(self, memory_data: Dict[str, Any]) -> None:
        """
        Save agent memory.
        
        Args:
            memory_data: Memory data to save
        """
        self.adapter.write_json("memory/data.json", memory_data)
    
    def load_memory(self) -> Dict[str, Any]:
        """
        Load agent memory.
        
        Returns:
            Memory data
        """
        try:
            return self.adapter.read_json("memory/data.json")
        except (FileNotFoundError, ValueError):
            return {}
    
    def save_knowledge(self, knowledge_data: Dict[str, Any]) -> None:
        """
        Save knowledge base.
        
        Args:
            knowledge_data: Knowledge data to save
        """
        self.adapter.write_json("knowledge/base.json", knowledge_data)
    
    def load_knowledge(self) -> Dict[str, Any]:
        """
        Load knowledge base.
        
        Returns:
            Knowledge data
        """
        try:
            return self.adapter.read_json("knowledge/base.json")
        except (FileNotFoundError, ValueError):
            return {}
    
    def save_config(self, config_data: Dict[str, Any]) -> None:
        """
        Save agent configuration.
        
        Args:
            config_data: Configuration data
        """
        self.adapter.write_json("config/agent.json", config_data)
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load agent configuration.
        
        Returns:
            Configuration data
        """
        try:
            return self.adapter.read_json("config/agent.json")
        except (FileNotFoundError, ValueError):
            return {}
    
    def save_prompt(self, name: str, content: str) -> None:
        """
        Save a prompt file.
        
        Args:
            name: Prompt name
            content: Prompt content
        """
        self.adapter.write_file(f"prompts/{name}.md", content)
    
    def load_prompt(self, name: str) -> Optional[str]:
        """
        Load a prompt file.
        
        Args:
            name: Prompt name
            
        Returns:
            Prompt content or None
        """
        try:
            return self.adapter.read_file(f"prompts/{name}.md")
        except FileNotFoundError:
            return None
    
    def list_prompts(self) -> List[str]:
        """
        List all prompts.
        
        Returns:
            List of prompt names
        """
        files = self.adapter.search_files("*.md", "prompts")
        return [f.split('/')[-1].replace('.md', '') for f in files]
    
    def write_log(self, message: str, level: str = "INFO") -> None:
        """
        Write to log file.
        
        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}\n"
        self.adapter.append_file("logs/agent.log", log_entry)
    
    def get_file_tree(self, dir_path: str = ".", max_depth: int = 3) -> Dict[str, Any]:
        """
        Get file tree structure.
        
        Args:
            dir_path: Directory path
            max_depth: Maximum depth to traverse
            
        Returns:
            File tree dictionary
        """
        def build_tree(path: str, depth: int) -> Dict[str, Any]:
            if depth <= 0:
                return {}
            
            items = self.adapter.list_directory(path)
            tree = {}
            
            for item in items:
                if item['type'] == 'directory':
                    tree[item['name']] = build_tree(item['path'], depth - 1)
                else:
                    tree[item['name']] = {
                        'size': item['size'],
                        'modified': item['modified'],
                    }
            
            return tree
        
        return build_tree(dir_path, max_depth)
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get storage information.
        
        Returns:
            Storage information
        """
        import os
        
        total_size = 0
        file_count = 0
        
        for dirpath, dirnames, filenames in os.walk(self.adapter.base_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except OSError:
                    pass
        
        return {
            'total_size': total_size,
            'file_count': file_count,
            'base_path': str(self.adapter.base_path),
        }
    
    def cleanup_cache(self) -> None:
        """Clean up cache directory."""
        import shutil
        cache_path = self.adapter.resolve_path("cache")
        if cache_path.exists():
            shutil.rmtree(cache_path)
        self.adapter.create_directory("cache")
    
    def cleanup_tmp(self) -> None:
        """Clean up temporary directory."""
        import shutil
        tmp_path = self.adapter.resolve_path("tmp")
        if tmp_path.exists():
            shutil.rmtree(tmp_path)
        self.adapter.create_directory("tmp")
