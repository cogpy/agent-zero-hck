"""
Example Usage of Virtual Hardware Framework
Demonstrates key features and integration patterns
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from helpers.virtual_hardware import (
    get_orchestrator,
    DeviceType,
    DeviceState
)
from helpers.virtual_hardware.agent_spawner import AgentSpawner, AgentRole
from helpers.virtual_hardware.red_team import RedTeamAgent, RedTeamOrchestrator
from helpers.virtual_hardware.opencog_integration import (
    VirtualHardwareCognitiveKernel,
    AgentZeroVirtualHardwareIntegration,
    OPENCOG_AVAILABLE
)


async def example_1_basic_device():
    """Example 1: Basic device spawning and inference"""
    print("\n" + "="*60)
    print("Example 1: Basic Device Spawning and Inference")
    print("="*60)
    
    orchestrator = get_orchestrator()
    
    # Spawn a DTE device
    print("\n[1] Spawning DTE bare-metal device...")
    device = await orchestrator.spawn_dte_device(
        cpu_cores=32,
        memory_gb=64,
        model_path="/models/llama-7b.gguf"
    )
    
    if device:
        print(f"✓ Device spawned: {device.device_id}")
        print(f"  State: {device.state.value}")
        print(f"  CPUs: {device.capabilities.cpu_cores}")
        print(f"  Memory: {device.capabilities.memory_mb}MB")
        
        # Send inference request
        print("\n[2] Sending inference request...")
        response = await device.send_message({
            "type": "inference",
            "prompt": "Explain the concept of virtual hardware in AI systems",
            "max_tokens": 256,
            "temperature": 0.7,
            "expect_response": True
        })
        
        if response and "error" not in response:
            print(f"✓ Inference completed")
            print(f"  Response: {response.get('response', 'N/A')}")
            print(f"  Tokens/sec: {response.get('metrics', {}).get('tokens_per_second', 0):.2f}")
            print(f"  Latency: {response.get('metrics', {}).get('elapsed_ms', 0):.2f}ms")
        
        # Get device status
        print("\n[3] Device status:")
        status = device.get_status()
        print(f"  Uptime: {status['uptime']:.2f}s")
        print(f"  Inference count: {device.metrics.inference_count}")
        print(f"  Avg latency: {device.metrics.average_latency_ms:.2f}ms")


async def example_2_agent_spawning():
    """Example 2: Dynamic agent spawning"""
    print("\n" + "="*60)
    print("Example 2: Dynamic Agent Spawning")
    print("="*60)
    
    orchestrator = get_orchestrator()
    spawner = AgentSpawner(orchestrator)
    
    # Spawn different types of agents
    print("\n[1] Spawning specialized agents...")
    
    # Inference worker
    worker = await spawner.spawn_specialized_agent(
        role=AgentRole.INFERENCE_WORKER,
        task_description="High-throughput inference processing"
    )
    print(f"✓ Inference worker spawned: {worker.agent_id}")
    
    # Cognitive kernel
    kernel = await spawner.spawn_specialized_agent(
        role=AgentRole.COGNITIVE_KERNEL,
        task_description="Pattern matching and reasoning"
    )
    print(f"✓ Cognitive kernel spawned: {kernel.agent_id}")
    
    # Red-team adversary
    adversary = await spawner.spawn_specialized_agent(
        role=AgentRole.RED_TEAM_ADVERSARY,
        task_description="Security testing and vulnerability detection"
    )
    print(f"✓ Red-team adversary spawned: {adversary.agent_id}")
    
    # Assign tasks
    print("\n[2] Assigning tasks to agents...")
    
    task_result = await spawner.assign_task(
        worker.agent_id,
        "Analyze sentiment of customer reviews",
        {
            "prompt": "This product is amazing! Highly recommended.",
            "max_tokens": 100
        }
    )
    
    if task_result and "error" not in task_result:
        print(f"✓ Task completed by worker")
        print(f"  Response: {task_result.get('response', 'N/A')[:100]}...")
    
    # Get spawner status
    print("\n[3] Spawner status:")
    status = spawner.get_spawner_status()
    print(f"  Total spawned: {status['total_spawned']}")
    print(f"  Active agents: {status['active_agents']}")
    print(f"  Agents by role: {status['agents_by_role']}")


async def example_3_parallel_inference():
    """Example 3: Parallel inference across multiple devices"""
    print("\n" + "="*60)
    print("Example 3: Parallel Inference")
    print("="*60)
    
    orchestrator = get_orchestrator()
    spawner = AgentSpawner(orchestrator)
    
    # Spawn pool of inference workers
    print("\n[1] Spawning pool of 3 inference workers...")
    pool = await spawner.spawn_agent_pool(
        template_name="ggml_inference_worker",
        pool_size=3
    )
    print(f"✓ Pool spawned: {len(pool)} agents")
    
    # Prepare tasks
    tasks = [
        {
            "description": f"Analyze text {i}",
            "prompt": f"Summarize the key points of document {i}",
            "max_tokens": 128
        }
        for i in range(6)  # 6 tasks for 3 agents
    ]
    
    # Execute in parallel
    print(f"\n[2] Executing {len(tasks)} tasks in parallel...")
    import time
    start = time.time()
    
    results = await spawner.parallel_task_execution(
        role=AgentRole.INFERENCE_WORKER,
        tasks=tasks
    )
    
    elapsed = time.time() - start
    print(f"✓ All tasks completed in {elapsed:.2f}s")
    print(f"  Successful: {sum(1 for r in results if r and 'error' not in r)}/{len(results)}")
    print(f"  Throughput: {len(results)/elapsed:.2f} tasks/sec")


async def example_4_red_team_testing():
    """Example 4: Red-team security testing"""
    print("\n" + "="*60)
    print("Example 4: Red-Team Security Testing")
    print("="*60)
    
    orchestrator = get_orchestrator()
    
    # Spawn device to test
    print("\n[1] Spawning device for security testing...")
    device = await orchestrator.spawn_dte_device(
        cpu_cores=16,
        memory_gb=32
    )
    print(f"✓ Device spawned: {device.device_id}")
    
    # Create red-team agent
    print("\n[2] Creating red-team agent...")
    red_team = RedTeamAgent()
    print(f"✓ Red-team agent created: {red_team.agent_id}")
    print(f"  Attack scenarios: {len(red_team.scenarios)}")
    
    # Execute attack scenarios
    print("\n[3] Executing attack scenarios...")
    results = await red_team.execute_all_scenarios(device)
    
    successful_attacks = sum(1 for r in results if r.success)
    print(f"✓ Testing complete")
    print(f"  Total attacks: {len(results)}")
    print(f"  Successful: {successful_attacks}")
    
    # Generate report
    print("\n[4] Security report:")
    report = red_team.generate_report()
    
    print(f"  Success rate: {report['summary']['success_rate']*100:.1f}%")
    print(f"  Avg impact: {report['summary']['average_impact_score']:.2f}")
    
    print("\n  Vulnerabilities by severity:")
    for severity, vulns in report['vulnerabilities_by_severity'].items():
        if vulns:
            print(f"    {severity.upper()}: {len(vulns)}")
            for vuln in vulns[:2]:  # Show first 2
                print(f"      - {vuln}")
    
    print(f"\n  Recommendations ({len(report['recommendations'])}):")
    for rec in report['recommendations'][:3]:  # Show first 3
        print(f"    - {rec}")


async def example_5_opencog_integration():
    """Example 5: OpenCog cognitive integration"""
    print("\n" + "="*60)
    print("Example 5: OpenCog Cognitive Integration")
    print("="*60)
    
    if not OPENCOG_AVAILABLE:
        print("\n⚠ OpenCog integration not available")
        print("  Install opencog-atomspace to enable this feature")
        return
    
    orchestrator = get_orchestrator()
    
    # Create cognitive kernel
    print("\n[1] Initializing cognitive kernel...")
    kernel = VirtualHardwareCognitiveKernel()
    print(f"✓ Cognitive kernel initialized")
    
    # Spawn devices
    print("\n[2] Spawning devices...")
    devices = []
    for i in range(3):
        device = await orchestrator.spawn_dte_device(
            cpu_cores=16,
            memory_gb=32
        )
        devices.append(device)
        
        # Register in AtomSpace
        kernel.register_device(
            device.device_id,
            device.device_type.value,
            device.get_capabilities()
        )
        print(f"✓ Device {i+1} registered in AtomSpace")
    
    # Allocate attention
    print("\n[3] Allocating attention...")
    for device in devices:
        sti, lti = kernel.allocate_attention(
            device.device_id,
            sti_delta=50 * (devices.index(device) + 1)
        )
        print(f"  Device {device.device_id[:8]}: STI={sti}, LTI={lti}")
    
    # Spread attention
    print("\n[4] Spreading attention from first device...")
    spread_results = kernel.spread_attention(devices[0].device_id, spread_factor=0.3)
    for device_id, (sti, lti) in spread_results.items():
        print(f"  {device_id[:8]}: STI={sti}")
    
    # Get attention summary
    print("\n[5] Attention summary:")
    summary = kernel.get_attention_summary()
    print(f"  Total devices: {summary['total_devices']}")
    print(f"  Total STI: {summary['total_sti']}")
    print(f"  Average STI: {summary['average_sti']:.1f}")
    
    print("\n  Device attention distribution:")
    for dev_att in summary['device_attention'][:3]:
        print(f"    {dev_att['device_id'][:8]}: {dev_att['sti']} ({dev_att['sti_percentage']:.1f}%)")


async def example_6_full_integration():
    """Example 6: Full Agent Zero integration"""
    print("\n" + "="*60)
    print("Example 6: Full Agent Zero Integration")
    print("="*60)
    
    orchestrator = get_orchestrator()
    spawner = AgentSpawner(orchestrator)
    
    # Create cognitive kernel if available
    kernel = None
    if OPENCOG_AVAILABLE:
        kernel = VirtualHardwareCognitiveKernel()
        print("✓ OpenCog cognitive kernel enabled")
    
    # Create integration layer
    print("\n[1] Initializing Agent Zero integration...")
    integration = AgentZeroVirtualHardwareIntegration(
        orchestrator=orchestrator,
        spawner=spawner,
        cognitive_kernel=kernel
    )
    print("✓ Integration layer initialized")
    
    # Simulate Agent Zero spawning virtual agents
    print("\n[2] Agent Zero spawning virtual agents for tasks...")
    
    agent_tasks = [
        ("agent_001", "inference", {"description": "Analyze customer feedback"}),
        ("agent_002", "reasoning", {"description": "Pattern matching in logs"}),
        ("agent_003", "security_test", {"description": "Vulnerability scanning"})
    ]
    
    for agent_id, task_type, params in agent_tasks:
        result = await integration.spawn_virtual_agent_for_task(
            agent_zero_id=agent_id,
            task_type=task_type,
            task_params=params
        )
        if result:
            print(f"✓ Virtual agent spawned for {agent_id}")
            print(f"  Role: {result['role']}")
            print(f"  Device: {result['device_id'][:8]}")
    
    # Execute tasks
    print("\n[3] Executing tasks on virtual agents...")
    for agent_id, _, _ in agent_tasks:
        response = await integration.execute_task_on_virtual_agent(
            agent_zero_id=agent_id,
            task_params={
                "prompt": f"Execute task for {agent_id}",
                "max_tokens": 128
            }
        )
        if response and "error" not in response:
            print(f"✓ Task completed for {agent_id}")
    
    # Get integration status
    print("\n[4] Integration status:")
    status = integration.get_integration_status()
    print(f"  Active mappings: {status['active_mappings']}")
    print(f"  Total devices: {status['orchestrator_status']['total_devices']}")
    print(f"  Total agents: {status['spawner_status']['active_agents']}")
    
    if status['cognitive_kernel_available']:
        att_summary = status['attention_summary']
        print(f"  Cognitive kernel: enabled")
        print(f"  Total STI: {att_summary['total_sti']}")


async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Virtual Hardware Framework - Example Usage")
    print("="*60)
    
    examples = [
        ("Basic Device", example_1_basic_device),
        ("Agent Spawning", example_2_agent_spawning),
        ("Parallel Inference", example_3_parallel_inference),
        ("Red-Team Testing", example_4_red_team_testing),
        ("OpenCog Integration", example_5_opencog_integration),
        ("Full Integration", example_6_full_integration)
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Run all examples")
    
    try:
        choice = input("\nSelect example (0-6): ").strip()
        
        if choice == "0":
            for name, example_fn in examples:
                await example_fn()
                await asyncio.sleep(1)
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            _, example_fn = examples[int(choice) - 1]
            await example_fn()
        else:
            print("Invalid choice")
            return
        
        # Cleanup
        print("\n" + "="*60)
        print("Cleaning up...")
        orchestrator = get_orchestrator()
        await orchestrator.shutdown_all()
        print("✓ All devices terminated")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
