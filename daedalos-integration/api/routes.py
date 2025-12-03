"""
API Routes for daedalOS Integration

Defines REST endpoints for Agent Zero operations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging

from ..filesystem import FileSystemManager

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize file system manager
fs_manager = FileSystemManager()


# Request/Response Models
class MessageRequest(BaseModel):
    """Message request model."""
    content: str
    agent_id: Optional[str] = "default"


class FileCreateRequest(BaseModel):
    """File creation request model."""
    path: str
    content: str


class FileReadResponse(BaseModel):
    """File read response model."""
    path: str
    content: str
    size: int


# File Management Endpoints
@router.get("/files/list")
async def list_files(path: str = Query(".")):
    """
    List files in directory.
    
    Args:
        path: Directory path
        
    Returns:
        List of files
    """
    try:
        files = fs_manager.adapter.list_directory(path)
        return {"files": files}
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/files/read")
async def read_file(path: str):
    """
    Read file contents.
    
    Args:
        path: File path
        
    Returns:
        File contents
    """
    try:
        content = fs_manager.adapter.read_file(path)
        return {
            "path": path,
            "content": content,
            "size": len(content),
        }
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/files/create")
async def create_file(request: FileCreateRequest):
    """
    Create or update file.
    
    Args:
        request: File creation request
        
    Returns:
        Success response
    """
    try:
        fs_manager.adapter.write_file(request.path, request.content)
        return {
            "status": "success",
            "path": request.path,
            "size": len(request.content),
        }
    except Exception as e:
        logger.error(f"Error creating file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/files/delete")
async def delete_file(path: str):
    """
    Delete file.
    
    Args:
        path: File path
        
    Returns:
        Success response
    """
    try:
        fs_manager.adapter.delete_file(path)
        return {"status": "success", "path": path}
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Memory Management Endpoints
@router.get("/memory")
async def get_memory():
    """
    Get agent memory.
    
    Returns:
        Memory data
    """
    try:
        memory = fs_manager.load_memory()
        return {"memory": memory}
    except Exception as e:
        logger.error(f"Error loading memory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/memory")
async def save_memory(data: Dict[str, Any]):
    """
    Save agent memory.
    
    Args:
        data: Memory data
        
    Returns:
        Success response
    """
    try:
        fs_manager.save_memory(data)
        return {"status": "success", "message": "Memory saved"}
    except Exception as e:
        logger.error(f"Error saving memory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Knowledge Base Endpoints
@router.get("/knowledge")
async def get_knowledge():
    """
    Get knowledge base.
    
    Returns:
        Knowledge data
    """
    try:
        knowledge = fs_manager.load_knowledge()
        return {"knowledge": knowledge}
    except Exception as e:
        logger.error(f"Error loading knowledge: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/knowledge")
async def save_knowledge(data: Dict[str, Any]):
    """
    Save knowledge base.
    
    Args:
        data: Knowledge data
        
    Returns:
        Success response
    """
    try:
        fs_manager.save_knowledge(data)
        return {"status": "success", "message": "Knowledge saved"}
    except Exception as e:
        logger.error(f"Error saving knowledge: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Configuration Endpoints
@router.get("/config")
async def get_config():
    """
    Get agent configuration.
    
    Returns:
        Configuration data
    """
    try:
        config = fs_manager.load_config()
        return {"config": config}
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/config")
async def save_config(data: Dict[str, Any]):
    """
    Save agent configuration.
    
    Args:
        data: Configuration data
        
    Returns:
        Success response
    """
    try:
        fs_manager.save_config(data)
        return {"status": "success", "message": "Configuration saved"}
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Prompt Management Endpoints
@router.get("/prompts")
async def list_prompts():
    """
    List all prompts.
    
    Returns:
        List of prompt names
    """
    try:
        prompts = fs_manager.list_prompts()
        return {"prompts": prompts}
    except Exception as e:
        logger.error(f"Error listing prompts: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/prompts/{name}")
async def get_prompt(name: str):
    """
    Get prompt content.
    
    Args:
        name: Prompt name
        
    Returns:
        Prompt content
    """
    try:
        content = fs_manager.load_prompt(name)
        if content is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return {"name": name, "content": content}
    except Exception as e:
        logger.error(f"Error loading prompt: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/prompts/{name}")
async def save_prompt(name: str, content: str):
    """
    Save prompt.
    
    Args:
        name: Prompt name
        content: Prompt content
        
    Returns:
        Success response
    """
    try:
        fs_manager.save_prompt(name, content)
        return {"status": "success", "name": name}
    except Exception as e:
        logger.error(f"Error saving prompt: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# System Endpoints
@router.get("/storage")
async def get_storage_info():
    """
    Get storage information.
    
    Returns:
        Storage information
    """
    try:
        info = fs_manager.get_storage_info()
        return {"storage": info}
    except Exception as e:
        logger.error(f"Error getting storage info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tree")
async def get_file_tree(path: str = Query(".")):
    """
    Get file tree structure.
    
    Args:
        path: Root path
        
    Returns:
        File tree
    """
    try:
        tree = fs_manager.get_file_tree(path)
        return {"tree": tree}
    except Exception as e:
        logger.error(f"Error getting file tree: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/logs")
async def write_log(message: str, level: str = Query("INFO")):
    """
    Write log entry.
    
    Args:
        message: Log message
        level: Log level
        
    Returns:
        Success response
    """
    try:
        fs_manager.write_log(message, level)
        return {"status": "success", "message": "Log entry written"}
    except Exception as e:
        logger.error(f"Error writing log: {e}")
        raise HTTPException(status_code=400, detail=str(e))
