"""
daedalOS File System Integration Module

Provides file system operations for Agent Zero within daedalOS environment.
"""

from .adapter import DaedalOSFileSystemAdapter
from .manager import FileSystemManager

__all__ = [
    'DaedalOSFileSystemAdapter',
    'FileSystemManager',
]
