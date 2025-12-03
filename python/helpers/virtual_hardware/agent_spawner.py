"""
GGML-Optimized Virtual Agent Spawning Framework
Enables agent-zero to dynamically spawn virtual hardware agents with GGML optimization
"""

import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from .device import DeviceType, DeviceCapabilities
from .dte_device import DTEBareMetalDevice
from .orchestrator import DeviceOrchestrator


class AgentRole(Enum):
    """Roles for spawned virtual agents"""
    INFERENCE_WORKER = "inference_worker"
    RED_TEAM_ADVERSARY = "red_team_adversary"
    COGNITIVE_KERNEL = "cognitive_kernel"
    PATTERN_MATCHER = "pattern_matcher"
    ATTENTION_ALLOCATOR = "attention_allocator"
    KNOWLEDGE_INTEGRATOR = "knowledge_integrator"


class SpawnStrategy(Enum):
    """Strategies for spawning agents"""
    ON_DEMAND = "on_demand"  # Spawn when needed
    PRE_ALLOCATED = "pre_allocated"  # Spawn pool in advance
    ELASTIC = "elastic"  # Dynamic scaling based on load
    SPECIALIZED = "specialized"  # Spawn for specific tasks


@dataclass
class AgentTemplate:
    """Template for spawning virtual agents"""
    name: str
    role: AgentRole
    device_type: DeviceType
    capabilities: DeviceCapabilities
    ggml_config: Dict[str, Any] = field(default_factory=dict)
    initialization_params: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpawnedAgent:
    """Represents a spawned virtual agent"""
    agent_id: str
    template_name: str
    role: AgentRole
    device: Any  # VirtualHardwareDevice instance
    spawned_at: datetime
    parent_agent_id: Optional[str] = None
    task_assignments: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "template": self.template_name,
            "role": self.role.value,
            "device_id": self.device.device_id,
            "spawned_at": self.spawned_at.isoformat(),
            "parent_agent_id": self.parent_agent_id,
            "task_count": len(self.task_assignments),
            "performance_metrics": self.performance_metrics
        }


class AgentSpawner:
    """
    Spawns and manages virtual hardware agents with GGML optimization
    Integrates with agent-zero for dynamic agent creation
    """
    
    def __init__(self, orchestrator: DeviceOrchestrator):
        self.orchestrator = orchestrator
        self.templates: Dict[str, AgentTemplate] = {}
        self.spawned_agents: Dict[str, SpawnedAgent] = {}
        
        # Spawn statistics
        self.total_spawned = 0
        self.total_terminated = 0
        
        # Register default templates
        self._register_default_templates()
    
    def _register_default_templates(self):
        """Register default agent templates"""
        
        # High-performance inference worker
        self.register_template(AgentTemplate(
            name="ggml_inference_worker",
            role=AgentRole.INFERENCE_WORKER,
            device_type=DeviceType.BARE_METAL_DTE,
            capabilities=DeviceCapabilities(
                cpu_cores=32,
                memory_mb=64 * 1024,
                ggml_enabled=True,
                avx512_support=True,
                max_context_length=16384,
                supports_parallel_inference=True
            ),
            ggml_config={
                "n_threads": 32,
                "context_size": 16384,
                "batch_size": 512,
                "use_mlock": True
            },
            metadata={"purpose": "High-throughput inference"}
        ))
        
        # Lightweight cognitive kernel
        self.register_template(AgentTemplate(
            name="cognitive_kernel",
            role=AgentRole.COGNITIVE_KERNEL,
            device_type=DeviceType.BARE_METAL_DTE,
            capabilities=DeviceCapabilities(
                cpu_cores=16,
                memory_mb=32 * 1024,
                ggml_enabled=True,
                max_context_length=8192,
                supports_parallel_inference=True,
                custom_capabilities={
                    "opencog_integration": True,
                    "atomspace_enabled": True,
                    "attention_spreading": True
                }
            ),
            ggml_config={
                "n_threads": 16,
                "context_size": 8192,
                "batch_size": 256
            },
            metadata={"purpose": "Cognitive reasoning and pattern matching"}
        ))
        
        # Red-team adversary
        self.register_template(AgentTemplate(
            name="red_team_adversary",
            role=AgentRole.RED_TEAM_ADVERSARY,
            device_type=DeviceType.BARE_METAL_DTE,
            capabilities=DeviceCapabilities(
                cpu_cores=8,
                memory_mb=16 * 1024,
                ggml_enabled=True,
                max_context_length=4096,
                supports_red_teaming=True
            ),
            ggml_config={
                "n_threads": 8,
                "context_size": 4096,
                "batch_size": 128
            },
            metadata={"purpose": "Adversarial testing and security validation"}
        ))
        
        # Attention allocator
        self.register_template(AgentTemplate(
            name="attention_allocator",
            role=AgentRole.ATTENTION_ALLOCATOR,
            device_type=DeviceType.BARE_METAL_DTE,
            capabilities=DeviceCapabilities(
                cpu_cores=4,
                memory_mb=8 * 1024,
                ggml_enabled=False,  # Doesn't need GGML
                max_context_length=2048,
                custom_capabilities={
                    "attention_management": True,
                    "resource_allocation": True
                }
            ),
            metadata={"purpose": "Manage attention allocation across agents"}
        ))
    
    def register_template(self, template: AgentTemplate):
        """Register an agent template"""
        self.templates[template.name] = template
    
    async def spawn_agent(
        self,
        template_name: str,
        parent_agent_id: Optional[str] = None,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Optional[SpawnedAgent]:
        """Spawn a new virtual agent from template"""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        
        # Merge custom config with template
        spawn_config = {
            "cpu_cores": template.capabilities.cpu_cores,
            "memory_gb": template.capabilities.memory_mb // 1024,
            "metadata": {
                **template.metadata,
                "role": template.role.value,
                "template": template_name
            }
        }
        
        if custom_config:
            spawn_config.update(custom_config)
        
        # Spawn device through orchestrator
        device = await self.orchestrator.spawn_device(
            template.device_type,
            **spawn_config
        )
        
        if not device:
            return None
        
        # Create spawned agent record
        agent = SpawnedAgent(
            agent_id=str(uuid.uuid4()),
            template_name=template_name,
            role=template.role,
            device=device,
            spawned_at=datetime.now(),
            parent_agent_id=parent_agent_id
        )
        
        self.spawned_agents[agent.agent_id] = agent
        self.total_spawned += 1
        
        return agent
    
    async def spawn_agent_pool(
        self,
        template_name: str,
        pool_size: int,
        parent_agent_id: Optional[str] = None
    ) -> List[SpawnedAgent]:
        """Spawn a pool of identical agents"""
        tasks = [
            self.spawn_agent(template_name, parent_agent_id)
            for _ in range(pool_size)
        ]
        
        agents = await asyncio.gather(*tasks)
        return [a for a in agents if a is not None]
    
    async def spawn_specialized_agent(
        self,
        role: AgentRole,
        task_description: str,
        parent_agent_id: Optional[str] = None,
        **custom_capabilities
    ) -> Optional[SpawnedAgent]:
        """Spawn a specialized agent for a specific task"""
        
        # Determine optimal template based on role
        template_map = {
            AgentRole.INFERENCE_WORKER: "ggml_inference_worker",
            AgentRole.COGNITIVE_KERNEL: "cognitive_kernel",
            AgentRole.RED_TEAM_ADVERSARY: "red_team_adversary",
            AgentRole.ATTENTION_ALLOCATOR: "attention_allocator"
        }
        
        template_name = template_map.get(role, "ggml_inference_worker")
        
        # Spawn with custom config
        agent = await self.spawn_agent(
            template_name,
            parent_agent_id,
            custom_config=custom_capabilities
        )
        
        if agent:
            agent.task_assignments.append(task_description)
        
        return agent
    
    async def spawn_elastic_pool(
        self,
        template_name: str,
        min_agents: int,
        max_agents: int,
        load_threshold: float = 0.8
    ) -> List[SpawnedAgent]:
        """
        Spawn an elastic pool that scales based on load
        Returns initial pool, monitoring continues in background
        """
        # Spawn minimum pool
        initial_pool = await self.spawn_agent_pool(template_name, min_agents)
        
        # Start background monitoring for elastic scaling
        asyncio.create_task(
            self._monitor_elastic_pool(
                template_name,
                initial_pool,
                max_agents,
                load_threshold
            )
        )
        
        return initial_pool
    
    async def _monitor_elastic_pool(
        self,
        template_name: str,
        pool: List[SpawnedAgent],
        max_agents: int,
        load_threshold: float
    ):
        """Monitor and scale elastic pool"""
        while True:
            await asyncio.sleep(5)  # Check every 5 seconds
            
            # Calculate average load
            total_load = 0.0
            active_agents = 0
            
            for agent in pool:
                if agent.agent_id in self.spawned_agents:
                    metrics = agent.device.get_metrics()
                    total_load += metrics.get("cpu_utilization", 0)
                    active_agents += 1
            
            if active_agents == 0:
                break  # Pool terminated
            
            avg_load = total_load / active_agents
            
            # Scale up if needed
            if avg_load > load_threshold * 100 and len(pool) < max_agents:
                new_agent = await self.spawn_agent(template_name)
                if new_agent:
                    pool.append(new_agent)
            
            # Scale down if load is low
            elif avg_load < (load_threshold * 0.5) * 100 and len(pool) > 1:
                # Terminate least utilized agent
                agent_to_remove = min(
                    pool,
                    key=lambda a: a.device.get_metrics().get("cpu_utilization", 0)
                )
                await self.terminate_agent(agent_to_remove.agent_id)
                pool.remove(agent_to_remove)
    
    async def assign_task(
        self,
        agent_id: str,
        task_description: str,
        task_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Assign a task to a spawned agent"""
        if agent_id not in self.spawned_agents:
            return {"error": "Agent not found"}
        
        agent = self.spawned_agents[agent_id]
        agent.task_assignments.append(task_description)
        
        # Send task to device
        message = {
            "type": "inference" if agent.role == AgentRole.INFERENCE_WORKER else "command",
            "task": task_description,
            "expect_response": True,
            **task_params
        }
        
        start_time = datetime.now()
        response = await agent.device.send_message(message)
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Update performance metrics
        agent.performance_metrics["last_task_ms"] = elapsed_ms
        agent.performance_metrics["total_tasks"] = len(agent.task_assignments)
        
        return response
    
    async def parallel_task_execution(
        self,
        role: AgentRole,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute tasks in parallel across agents with matching role"""
        # Get agents with matching role
        matching_agents = [
            agent for agent in self.spawned_agents.values()
            if agent.role == role
        ]
        
        if not matching_agents:
            # Spawn agents if none available
            template_map = {
                AgentRole.INFERENCE_WORKER: "ggml_inference_worker",
                AgentRole.COGNITIVE_KERNEL: "cognitive_kernel",
                AgentRole.RED_TEAM_ADVERSARY: "red_team_adversary"
            }
            template_name = template_map.get(role, "ggml_inference_worker")
            matching_agents = await self.spawn_agent_pool(template_name, len(tasks))
        
        # Distribute tasks
        task_assignments = []
        for i, task in enumerate(tasks):
            agent = matching_agents[i % len(matching_agents)]
            task_assignments.append(
                self.assign_task(
                    agent.agent_id,
                    task.get("description", "Task"),
                    task
                )
            )
        
        # Execute in parallel
        results = await asyncio.gather(*task_assignments, return_exceptions=True)
        return results
    
    async def terminate_agent(self, agent_id: str) -> bool:
        """Terminate a spawned agent"""
        if agent_id not in self.spawned_agents:
            return False
        
        agent = self.spawned_agents[agent_id]
        
        # Terminate device
        await self.orchestrator.terminate_device(agent.device.device_id)
        
        # Remove from registry
        del self.spawned_agents[agent_id]
        self.total_terminated += 1
        
        return True
    
    async def terminate_all_agents(self):
        """Terminate all spawned agents"""
        agent_ids = list(self.spawned_agents.keys())
        tasks = [self.terminate_agent(aid) for aid in agent_ids]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_agent(self, agent_id: str) -> Optional[SpawnedAgent]:
        """Get spawned agent by ID"""
        return self.spawned_agents.get(agent_id)
    
    def get_agents_by_role(self, role: AgentRole) -> List[SpawnedAgent]:
        """Get all agents with specific role"""
        return [
            agent for agent in self.spawned_agents.values()
            if agent.role == role
        ]
    
    def get_spawner_status(self) -> Dict[str, Any]:
        """Get spawner status and statistics"""
        agents_by_role = {}
        for agent in self.spawned_agents.values():
            role_name = agent.role.value
            agents_by_role[role_name] = agents_by_role.get(role_name, 0) + 1
        
        return {
            "total_spawned": self.total_spawned,
            "total_terminated": self.total_terminated,
            "active_agents": len(self.spawned_agents),
            "agents_by_role": agents_by_role,
            "registered_templates": list(self.templates.keys())
        }
    
    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all spawned agents"""
        return [agent.to_dict() for agent in self.spawned_agents.values()]
    
    def __repr__(self) -> str:
        return f"AgentSpawner(active={len(self.spawned_agents)}, total={self.total_spawned})"


# Convenience function for agent-zero integration
async def spawn_virtual_agent(
    role: AgentRole,
    task_description: str,
    orchestrator: Optional[DeviceOrchestrator] = None,
    **kwargs
) -> Optional[SpawnedAgent]:
    """
    Convenience function for agent-zero to spawn virtual agents
    """
    if orchestrator is None:
        from .orchestrator import get_orchestrator
        orchestrator = get_orchestrator()
    
    spawner = AgentSpawner(orchestrator)
    return await spawner.spawn_specialized_agent(role, task_description, **kwargs)
