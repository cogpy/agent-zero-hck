"""
Virtual Hardware Device Abstraction Layer
Provides a framework for creating virtual hardware devices that can be
orchestrated by agent-zero with GGML optimization and red-teaming capabilities.
"""

import uuid
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class DeviceState(Enum):
    """Virtual hardware device states"""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SUSPENDED = "suspended"
    ERROR = "error"
    TERMINATED = "terminated"


class DeviceType(Enum):
    """Types of virtual hardware devices"""
    BARE_METAL_DTE = "bare_metal_dte"
    GGML_ACCELERATOR = "ggml_accelerator"
    COGNITIVE_KERNEL = "cognitive_kernel"
    RED_TEAM_AGENT = "red_team_agent"
    NETWORK_INTERFACE = "network_interface"
    STORAGE_CONTROLLER = "storage_controller"


@dataclass
class DeviceCapabilities:
    """Capabilities and resources of a virtual hardware device"""
    cpu_cores: int = 1
    memory_mb: int = 1024
    storage_gb: int = 10
    ggml_enabled: bool = False
    avx512_support: bool = False
    tensor_cores: int = 0
    max_context_length: int = 4096
    supports_parallel_inference: bool = False
    supports_red_teaming: bool = False
    custom_capabilities: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceMetrics:
    """Runtime metrics for virtual hardware device"""
    uptime_seconds: float = 0.0
    cpu_utilization: float = 0.0
    memory_used_mb: float = 0.0
    inference_count: int = 0
    tokens_processed: int = 0
    average_latency_ms: float = 0.0
    error_count: int = 0
    last_activity: Optional[datetime] = None
    custom_metrics: Dict[str, float] = field(default_factory=dict)


class VirtualHardwareDevice:
    """
    Base class for virtual hardware devices
    Provides common interface for device lifecycle, communication, and monitoring
    """
    
    def __init__(
        self,
        device_id: Optional[str] = None,
        device_type: DeviceType = DeviceType.BARE_METAL_DTE,
        capabilities: Optional[DeviceCapabilities] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.device_id = device_id or str(uuid.uuid4())
        self.device_type = device_type
        self.capabilities = capabilities or DeviceCapabilities()
        self.metadata = metadata or {}
        
        self.state = DeviceState.UNINITIALIZED
        self.metrics = DeviceMetrics()
        self.created_at = datetime.now()
        
        # Communication channels
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.response_handlers: Dict[str, Callable] = {}
        
        # Event hooks
        self.on_state_change: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_message: Optional[Callable] = None
        
    async def initialize(self) -> bool:
        """Initialize the virtual hardware device"""
        self.state = DeviceState.INITIALIZING
        try:
            await self._initialize_impl()
            self.state = DeviceState.READY
            await self._notify_state_change()
            return True
        except Exception as e:
            self.state = DeviceState.ERROR
            await self._handle_error(e)
            return False
    
    async def _initialize_impl(self):
        """Implementation-specific initialization (override in subclasses)"""
        pass
    
    async def start(self) -> bool:
        """Start the virtual hardware device"""
        if self.state != DeviceState.READY:
            return False
        
        self.state = DeviceState.RUNNING
        await self._notify_state_change()
        asyncio.create_task(self._run_loop())
        return True
    
    async def _run_loop(self):
        """Main execution loop for the device"""
        start_time = datetime.now()
        
        while self.state == DeviceState.RUNNING:
            try:
                # Process messages from queue
                try:
                    message = await asyncio.wait_for(
                        self.message_queue.get(),
                        timeout=1.0
                    )
                    await self._process_message(message)
                except asyncio.TimeoutError:
                    pass
                
                # Update metrics
                self.metrics.uptime_seconds = (datetime.now() - start_time).total_seconds()
                self.metrics.last_activity = datetime.now()
                
                # Device-specific work
                await self._device_work()
                
            except Exception as e:
                await self._handle_error(e)
    
    async def _device_work(self):
        """Device-specific work (override in subclasses)"""
        await asyncio.sleep(0.1)
    
    async def suspend(self):
        """Suspend the device"""
        if self.state == DeviceState.RUNNING:
            self.state = DeviceState.SUSPENDED
            await self._notify_state_change()
    
    async def resume(self):
        """Resume the device"""
        if self.state == DeviceState.SUSPENDED:
            self.state = DeviceState.RUNNING
            await self._notify_state_change()
    
    async def terminate(self):
        """Terminate the device"""
        self.state = DeviceState.TERMINATED
        await self._notify_state_change()
    
    async def send_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a message to the device and optionally wait for response"""
        message_id = message.get("id", str(uuid.uuid4()))
        message["id"] = message_id
        message["timestamp"] = datetime.now().isoformat()
        
        await self.message_queue.put(message)
        
        # If expecting response, wait for it
        if message.get("expect_response", False):
            response_future = asyncio.Future()
            self.response_handlers[message_id] = response_future.set_result
            
            try:
                response = await asyncio.wait_for(response_future, timeout=30.0)
                return response
            except asyncio.TimeoutError:
                del self.response_handlers[message_id]
                return None
        
        return None
    
    async def _process_message(self, message: Dict[str, Any]):
        """Process incoming message"""
        message_type = message.get("type", "unknown")
        
        if self.on_message:
            await self.on_message(message)
        
        # Handle message based on type
        if message_type == "inference":
            response = await self._handle_inference(message)
        elif message_type == "command":
            response = await self._handle_command(message)
        elif message_type == "query":
            response = await self._handle_query(message)
        else:
            response = {"error": f"Unknown message type: {message_type}"}
        
        # Send response if handler is waiting
        message_id = message.get("id")
        if message_id in self.response_handlers:
            self.response_handlers[message_id](response)
            del self.response_handlers[message_id]
    
    async def _handle_inference(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle inference request (override in subclasses)"""
        return {"error": "Inference not implemented"}
    
    async def _handle_command(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle command (override in subclasses)"""
        command = message.get("command")
        return {"status": "ok", "command": command}
    
    async def _handle_query(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle query request"""
        query_type = message.get("query_type", "status")
        
        if query_type == "status":
            return self.get_status()
        elif query_type == "metrics":
            return self.get_metrics()
        elif query_type == "capabilities":
            return self.get_capabilities()
        else:
            return {"error": f"Unknown query type: {query_type}"}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current device status"""
        return {
            "device_id": self.device_id,
            "device_type": self.device_type.value,
            "state": self.state.value,
            "uptime": self.metrics.uptime_seconds,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get device metrics"""
        return {
            "uptime_seconds": self.metrics.uptime_seconds,
            "cpu_utilization": self.metrics.cpu_utilization,
            "memory_used_mb": self.metrics.memory_used_mb,
            "inference_count": self.metrics.inference_count,
            "tokens_processed": self.metrics.tokens_processed,
            "average_latency_ms": self.metrics.average_latency_ms,
            "error_count": self.metrics.error_count,
            "last_activity": self.metrics.last_activity.isoformat() if self.metrics.last_activity else None,
            "custom_metrics": self.metrics.custom_metrics
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get device capabilities"""
        return {
            "cpu_cores": self.capabilities.cpu_cores,
            "memory_mb": self.capabilities.memory_mb,
            "storage_gb": self.capabilities.storage_gb,
            "ggml_enabled": self.capabilities.ggml_enabled,
            "avx512_support": self.capabilities.avx512_support,
            "tensor_cores": self.capabilities.tensor_cores,
            "max_context_length": self.capabilities.max_context_length,
            "supports_parallel_inference": self.capabilities.supports_parallel_inference,
            "supports_red_teaming": self.capabilities.supports_red_teaming,
            "custom_capabilities": self.capabilities.custom_capabilities
        }
    
    async def _notify_state_change(self):
        """Notify state change"""
        if self.on_state_change:
            await self.on_state_change(self.state)
    
    async def _handle_error(self, error: Exception):
        """Handle error"""
        self.metrics.error_count += 1
        if self.on_error:
            await self.on_error(error)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize device to dictionary"""
        return {
            "device_id": self.device_id,
            "device_type": self.device_type.value,
            "state": self.state.value,
            "capabilities": self.get_capabilities(),
            "metrics": self.get_metrics(),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"VirtualHardwareDevice(id={self.device_id}, type={self.device_type.value}, state={self.state.value})"
