"""
Virtual Hardware Framework for Agent Zero
Enables spawning and orchestration of virtual hardware devices with GGML optimization
"""

from .device import (
    VirtualHardwareDevice,
    DeviceState,
    DeviceType,
    DeviceCapabilities,
    DeviceMetrics
)

from .dte_device import DTEBareMetalDevice

from .orchestrator import DeviceOrchestrator, get_orchestrator

__all__ = [
    "VirtualHardwareDevice",
    "DeviceState",
    "DeviceType",
    "DeviceCapabilities",
    "DeviceMetrics",
    "DTEBareMetalDevice",
    "DeviceOrchestrator",
    "get_orchestrator"
]
