"""
Virtual Hardware Device Orchestrator
Manages lifecycle and communication for multiple virtual hardware devices
"""

import asyncio
from typing import Dict, List, Optional, Any, Type
from datetime import datetime
import json

from .device import VirtualHardwareDevice, DeviceType, DeviceState
from .dte_device import DTEBareMetalDevice


class DeviceOrchestrator:
    """
    Orchestrates multiple virtual hardware devices
    Handles device spawning, communication, and resource management
    """
    
    def __init__(self):
        self.devices: Dict[str, VirtualHardwareDevice] = {}
        self.device_registry: Dict[DeviceType, Type[VirtualHardwareDevice]] = {
            DeviceType.BARE_METAL_DTE: DTEBareMetalDevice
        }
        
        # Global metrics
        self.total_devices_created = 0
        self.total_inferences = 0
        self.orchestrator_start_time = datetime.now()
        
        # Event hooks
        self.on_device_created: Optional[callable] = None
        self.on_device_terminated: Optional[callable] = None
        
    def register_device_type(
        self,
        device_type: DeviceType,
        device_class: Type[VirtualHardwareDevice]
    ):
        """Register a new device type"""
        self.device_registry[device_type] = device_class
    
    async def spawn_device(
        self,
        device_type: DeviceType,
        device_id: Optional[str] = None,
        **kwargs
    ) -> Optional[VirtualHardwareDevice]:
        """Spawn a new virtual hardware device"""
        if device_type not in self.device_registry:
            raise ValueError(f"Unknown device type: {device_type}")
        
        device_class = self.device_registry[device_type]
        device = device_class(device_id=device_id, **kwargs)
        
        # Initialize device
        success = await device.initialize()
        if not success:
            return None
        
        # Register device
        self.devices[device.device_id] = device
        self.total_devices_created += 1
        
        # Set up event handlers
        device.on_state_change = lambda state: self._on_device_state_change(device.device_id, state)
        device.on_error = lambda error: self._on_device_error(device.device_id, error)
        
        # Start device
        await device.start()
        
        # Notify
        if self.on_device_created:
            await self.on_device_created(device)
        
        return device
    
    async def spawn_dte_device(
        self,
        device_id: Optional[str] = None,
        cpu_cores: int = 64,
        memory_gb: int = 128,
        model_path: Optional[str] = None,
        **kwargs
    ) -> Optional[DTEBareMetalDevice]:
        """Convenience method to spawn DTE bare-metal device"""
        return await self.spawn_device(
            DeviceType.BARE_METAL_DTE,
            device_id=device_id,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            model_path=model_path,
            **kwargs
        )
    
    async def terminate_device(self, device_id: str) -> bool:
        """Terminate a device"""
        if device_id not in self.devices:
            return False
        
        device = self.devices[device_id]
        await device.terminate()
        
        del self.devices[device_id]
        
        if self.on_device_terminated:
            await self.on_device_terminated(device)
        
        return True
    
    async def send_to_device(
        self,
        device_id: str,
        message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send message to a specific device"""
        if device_id not in self.devices:
            return {"error": f"Device not found: {device_id}"}
        
        device = self.devices[device_id]
        return await device.send_message(message)
    
    async def broadcast(
        self,
        message: Dict[str, Any],
        device_type: Optional[DeviceType] = None
    ) -> Dict[str, Any]:
        """Broadcast message to all devices or devices of specific type"""
        results = {}
        
        for device_id, device in self.devices.items():
            if device_type is None or device.device_type == device_type:
                response = await device.send_message(message.copy())
                results[device_id] = response
        
        return results
    
    async def parallel_inference(
        self,
        prompt: str,
        device_ids: Optional[List[str]] = None,
        **inference_params
    ) -> Dict[str, Any]:
        """
        Run inference on multiple devices in parallel
        Useful for ensemble methods or load balancing
        """
        if device_ids is None:
            # Use all DTE devices
            device_ids = [
                d.device_id for d in self.devices.values()
                if d.device_type == DeviceType.BARE_METAL_DTE
                and d.state == DeviceState.RUNNING
            ]
        
        if not device_ids:
            return {"error": "No available devices for inference"}
        
        # Create inference messages
        message = {
            "type": "inference",
            "prompt": prompt,
            "expect_response": True,
            **inference_params
        }
        
        # Send to all devices in parallel
        tasks = [
            self.send_to_device(device_id, message.copy())
            for device_id in device_ids
        ]
        
        start_time = datetime.now()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Aggregate results
        self.total_inferences += len(device_ids)
        
        return {
            "status": "success",
            "device_count": len(device_ids),
            "responses": dict(zip(device_ids, responses)),
            "elapsed_ms": elapsed_ms
        }
    
    def get_device(self, device_id: str) -> Optional[VirtualHardwareDevice]:
        """Get device by ID"""
        return self.devices.get(device_id)
    
    def get_devices_by_type(self, device_type: DeviceType) -> List[VirtualHardwareDevice]:
        """Get all devices of a specific type"""
        return [
            device for device in self.devices.values()
            if device.device_type == device_type
        ]
    
    def get_all_devices(self) -> List[VirtualHardwareDevice]:
        """Get all devices"""
        return list(self.devices.values())
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get overall orchestrator status"""
        uptime = (datetime.now() - self.orchestrator_start_time).total_seconds()
        
        devices_by_type = {}
        devices_by_state = {}
        
        for device in self.devices.values():
            # Count by type
            type_name = device.device_type.value
            devices_by_type[type_name] = devices_by_type.get(type_name, 0) + 1
            
            # Count by state
            state_name = device.state.value
            devices_by_state[state_name] = devices_by_state.get(state_name, 0) + 1
        
        return {
            "uptime_seconds": uptime,
            "total_devices": len(self.devices),
            "total_devices_created": self.total_devices_created,
            "total_inferences": self.total_inferences,
            "devices_by_type": devices_by_type,
            "devices_by_state": devices_by_state,
            "registered_device_types": [dt.value for dt in self.device_registry.keys()]
        }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics from all devices"""
        return {
            device_id: device.get_metrics()
            for device_id, device in self.devices.items()
        }
    
    async def _on_device_state_change(self, device_id: str, new_state: DeviceState):
        """Handle device state change"""
        pass  # Can be extended for logging or monitoring
    
    async def _on_device_error(self, device_id: str, error: Exception):
        """Handle device error"""
        pass  # Can be extended for error handling
    
    async def shutdown_all(self):
        """Shutdown all devices"""
        tasks = [
            device.terminate()
            for device in self.devices.values()
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.devices.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize orchestrator state"""
        return {
            "status": self.get_orchestrator_status(),
            "devices": {
                device_id: device.to_dict()
                for device_id, device in self.devices.items()
            }
        }
    
    def __repr__(self) -> str:
        return f"DeviceOrchestrator(devices={len(self.devices)}, types={len(self.device_registry)})"


# Global orchestrator instance
_global_orchestrator: Optional[DeviceOrchestrator] = None


def get_orchestrator() -> DeviceOrchestrator:
    """Get the global device orchestrator instance"""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = DeviceOrchestrator()
    return _global_orchestrator
