"""
OpenCog Cognitive Architecture Integration
Connects virtual hardware devices with OpenCog AtomSpace for cognitive reasoning
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

# Import OpenCog AtomSpace helper
try:
    from ..opencog_atomspace import AtomSpaceManager, AtomType
    OPENCOG_AVAILABLE = True
except ImportError:
    OPENCOG_AVAILABLE = False
    AtomSpaceManager = None
    AtomType = None


class VirtualHardwareCognitiveKernel:
    """
    Cognitive kernel that bridges virtual hardware devices with OpenCog
    Enables attention spreading, pattern matching, and knowledge integration
    """
    
    def __init__(self, atomspace_manager: Optional[Any] = None):
        if not OPENCOG_AVAILABLE:
            raise RuntimeError("OpenCog integration not available")
        
        self.atomspace = atomspace_manager or AtomSpaceManager()
        self.device_nodes: Dict[str, Any] = {}  # device_id -> Node
        self.attention_values: Dict[str, Tuple[int, int]] = {}  # device_id -> (sti, lti)
        
    def register_device(
        self,
        device_id: str,
        device_type: str,
        capabilities: Dict[str, Any]
    ) -> Any:
        """Register a virtual hardware device in AtomSpace"""
        # Create device node
        device_node = self.atomspace.add_node(
            AtomType.CONCEPT,
            f"VirtualDevice:{device_id}"
        )
        
        # Create device type node
        type_node = self.atomspace.add_node(
            AtomType.CONCEPT,
            f"DeviceType:{device_type}"
        )
        
        # Link device to type
        self.atomspace.add_link(
            AtomType.INHERITANCE,
            [device_node, type_node]
        )
        
        # Add capability nodes
        for cap_name, cap_value in capabilities.items():
            cap_node = self.atomspace.add_node(
                AtomType.PREDICATE,
                f"Capability:{cap_name}"
            )
            
            # Create evaluation link
            value_node = self.atomspace.add_node(
                AtomType.CONCEPT,
                str(cap_value)
            )
            
            self.atomspace.add_link(
                AtomType.EVALUATION,
                [
                    cap_node,
                    self.atomspace.add_link(
                        AtomType.LIST,
                        [device_node, value_node]
                    )
                ]
            )
        
        # Set initial attention values
        self.atomspace.set_attention(device_node, sti=100, lti=50)
        self.attention_values[device_id] = (100, 50)
        
        self.device_nodes[device_id] = device_node
        return device_node
    
    def allocate_attention(
        self,
        device_id: str,
        sti_delta: int = 0,
        lti_delta: int = 0
    ) -> Tuple[int, int]:
        """Allocate attention to a device"""
        if device_id not in self.device_nodes:
            return (0, 0)
        
        device_node = self.device_nodes[device_id]
        current_sti, current_lti = self.attention_values.get(device_id, (100, 50))
        
        new_sti = max(0, min(1000, current_sti + sti_delta))
        new_lti = max(0, min(1000, current_lti + lti_delta))
        
        self.atomspace.set_attention(device_node, sti=new_sti, lti=new_lti)
        self.attention_values[device_id] = (new_sti, new_lti)
        
        return (new_sti, new_lti)
    
    def spread_attention(
        self,
        source_device_id: str,
        spread_factor: float = 0.5
    ) -> Dict[str, Tuple[int, int]]:
        """
        Spread attention from source device to related devices
        Implements attention spreading mechanism
        """
        if source_device_id not in self.device_nodes:
            return {}
        
        source_node = self.device_nodes[source_device_id]
        source_sti, source_lti = self.attention_values.get(source_device_id, (100, 50))
        
        # Find related devices through links
        related_devices = self._find_related_devices(source_device_id)
        
        results = {}
        spread_amount = int(source_sti * spread_factor / len(related_devices)) if related_devices else 0
        
        for device_id in related_devices:
            new_sti, new_lti = self.allocate_attention(device_id, sti_delta=spread_amount)
            results[device_id] = (new_sti, new_lti)
        
        # Reduce source attention
        self.allocate_attention(source_device_id, sti_delta=-spread_amount * len(related_devices))
        
        return results
    
    def _find_related_devices(self, device_id: str) -> List[str]:
        """Find devices related through AtomSpace links"""
        # Simplified: return other devices
        # In full implementation, would traverse AtomSpace links
        return [did for did in self.device_nodes.keys() if did != device_id]
    
    def pattern_match_devices(
        self,
        pattern: Dict[str, Any]
    ) -> List[str]:
        """
        Find devices matching a pattern using OpenCog pattern matching
        """
        matching_devices = []
        
        for device_id, device_node in self.device_nodes.items():
            # Check if device matches pattern
            matches = True
            for key, value in pattern.items():
                # Simplified matching - in full implementation would use
                # OpenCog's pattern matcher
                if key == "min_sti":
                    sti, _ = self.attention_values.get(device_id, (0, 0))
                    if sti < value:
                        matches = False
                        break
                elif key == "device_type":
                    # Would check inheritance links
                    pass
            
            if matches:
                matching_devices.append(device_id)
        
        return matching_devices
    
    def create_device_inference_link(
        self,
        device_id: str,
        inference_result: str,
        confidence: float = 0.8
    ):
        """Create a link between device and inference result"""
        if device_id not in self.device_nodes:
            return None
        
        device_node = self.device_nodes[device_id]
        result_node = self.atomspace.add_node(
            AtomType.CONCEPT,
            f"InferenceResult:{inference_result}"
        )
        
        # Create implication link with truth value
        link = self.atomspace.add_link(
            AtomType.IMPLICATION,
            [device_node, result_node]
        )
        
        self.atomspace.set_truth_value(link, strength=confidence, confidence=0.9)
        
        return link
    
    def get_device_knowledge_graph(
        self,
        device_id: str,
        depth: int = 2
    ) -> Dict[str, Any]:
        """
        Extract knowledge graph for a device
        Returns nodes and links up to specified depth
        """
        if device_id not in self.device_nodes:
            return {}
        
        device_node = self.device_nodes[device_id]
        
        # Get incoming and outgoing links
        incoming = self.atomspace.get_incoming(device_node)
        
        graph = {
            "device_id": device_id,
            "node": str(device_node),
            "attention": self.attention_values.get(device_id, (0, 0)),
            "incoming_links": len(incoming),
            "related_concepts": []
        }
        
        # Extract related concepts (simplified)
        for link in incoming[:10]:  # Limit to 10 for brevity
            graph["related_concepts"].append({
                "link_type": str(link.type),
                "targets": [str(target) for target in link.out]
            })
        
        return graph
    
    def cognitive_task_allocation(
        self,
        task_description: str,
        required_capabilities: Dict[str, Any]
    ) -> List[str]:
        """
        Allocate a cognitive task to most suitable devices
        Uses attention values and capability matching
        """
        # Find devices with required capabilities
        candidate_devices = []
        
        for device_id in self.device_nodes.keys():
            # Check capabilities (simplified)
            sti, lti = self.attention_values.get(device_id, (0, 0))
            
            # Devices with high attention are prioritized
            if sti > 50:
                candidate_devices.append((device_id, sti))
        
        # Sort by attention value
        candidate_devices.sort(key=lambda x: x[1], reverse=True)
        
        # Return top candidates
        return [device_id for device_id, _ in candidate_devices[:3]]
    
    def update_device_performance(
        self,
        device_id: str,
        success: bool,
        latency_ms: float
    ):
        """
        Update device performance metrics in AtomSpace
        Adjusts attention based on performance
        """
        if device_id not in self.device_nodes:
            return
        
        # Adjust attention based on performance
        if success:
            # Reward successful inference
            sti_delta = 10
            if latency_ms < 100:  # Fast response
                sti_delta += 5
        else:
            # Penalize failures
            sti_delta = -20
        
        self.allocate_attention(device_id, sti_delta=sti_delta)
    
    def get_attention_summary(self) -> Dict[str, Any]:
        """Get summary of attention allocation across devices"""
        if not self.attention_values:
            return {}
        
        total_sti = sum(sti for sti, _ in self.attention_values.values())
        total_lti = sum(lti for _, lti in self.attention_values.values())
        
        device_attention = [
            {
                "device_id": device_id,
                "sti": sti,
                "lti": lti,
                "sti_percentage": (sti / total_sti * 100) if total_sti > 0 else 0
            }
            for device_id, (sti, lti) in self.attention_values.items()
        ]
        
        # Sort by STI
        device_attention.sort(key=lambda x: x["sti"], reverse=True)
        
        return {
            "total_devices": len(self.device_nodes),
            "total_sti": total_sti,
            "total_lti": total_lti,
            "average_sti": total_sti / len(self.device_nodes) if self.device_nodes else 0,
            "device_attention": device_attention
        }
    
    def __repr__(self) -> str:
        return f"VirtualHardwareCognitiveKernel(devices={len(self.device_nodes)})"


class AgentZeroVirtualHardwareIntegration:
    """
    Integration layer between agent-zero and virtual hardware framework
    Enables agent-zero to spawn and manage virtual hardware agents
    """
    
    def __init__(
        self,
        orchestrator: Any,
        spawner: Any,
        cognitive_kernel: Optional[VirtualHardwareCognitiveKernel] = None
    ):
        self.orchestrator = orchestrator
        self.spawner = spawner
        self.cognitive_kernel = cognitive_kernel
        
        # Track agent-zero to virtual hardware mappings
        self.agent_mappings: Dict[str, str] = {}  # agent_zero_id -> virtual_device_id
    
    async def spawn_virtual_agent_for_task(
        self,
        agent_zero_id: str,
        task_type: str,
        task_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Spawn a virtual hardware agent for an agent-zero task
        """
        # Determine role based on task type
        from .agent_spawner import AgentRole
        
        role_map = {
            "inference": AgentRole.INFERENCE_WORKER,
            "reasoning": AgentRole.COGNITIVE_KERNEL,
            "security_test": AgentRole.RED_TEAM_ADVERSARY,
            "pattern_matching": AgentRole.PATTERN_MATCHER
        }
        
        role = role_map.get(task_type, AgentRole.INFERENCE_WORKER)
        
        # Spawn agent
        spawned_agent = await self.spawner.spawn_specialized_agent(
            role=role,
            task_description=task_params.get("description", "Task"),
            parent_agent_id=agent_zero_id
        )
        
        if not spawned_agent:
            return None
        
        # Register in cognitive kernel if available
        if self.cognitive_kernel:
            self.cognitive_kernel.register_device(
                spawned_agent.device.device_id,
                spawned_agent.device.device_type.value,
                spawned_agent.device.get_capabilities()
            )
        
        # Track mapping
        self.agent_mappings[agent_zero_id] = spawned_agent.device.device_id
        
        return {
            "agent_id": spawned_agent.agent_id,
            "device_id": spawned_agent.device.device_id,
            "role": role.value,
            "status": "spawned"
        }
    
    async def execute_task_on_virtual_agent(
        self,
        agent_zero_id: str,
        task_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Execute a task on the virtual agent associated with agent-zero"""
        if agent_zero_id not in self.agent_mappings:
            return {"error": "No virtual agent associated with this agent-zero instance"}
        
        device_id = self.agent_mappings[agent_zero_id]
        
        # Send task to device
        response = await self.orchestrator.send_to_device(device_id, {
            "type": "inference",
            "expect_response": True,
            **task_params
        })
        
        # Update cognitive kernel if available
        if self.cognitive_kernel and response:
            success = "error" not in response
            latency = response.get("metrics", {}).get("elapsed_ms", 0)
            self.cognitive_kernel.update_device_performance(
                device_id,
                success,
                latency
            )
        
        return response
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of agent-zero integration"""
        return {
            "active_mappings": len(self.agent_mappings),
            "orchestrator_status": self.orchestrator.get_orchestrator_status(),
            "spawner_status": self.spawner.get_spawner_status(),
            "cognitive_kernel_available": self.cognitive_kernel is not None,
            "attention_summary": self.cognitive_kernel.get_attention_summary() if self.cognitive_kernel else None
        }
