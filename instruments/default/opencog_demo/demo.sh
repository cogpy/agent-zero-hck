#!/bin/bash

# OpenCog Cognitive Architecture Demo Script
# Demonstrates the cognitive capabilities of cog-zero

echo "=========================================="
echo "OpenCog Cognitive Architecture Demo"
echo "Cog-Zero Multi-Agent Orchestration"
echo "=========================================="
echo ""

# Note: This script demonstrates OpenCog usage through the Python API
# In practice, agents would use the opencog tool directly

python3 << 'PYTHON_SCRIPT'
import sys
sys.path.append('/a0')

from python.helpers import opencog_atomspace
import json

print("1. Initializing Cognitive Orchestrator...")
orchestrator = opencog_atomspace.get_orchestrator()

print("   ✓ Creating AtomSpace for multi-agent system")
atomspace = orchestrator.create_atomspace("demo_space")
print(f"   ✓ AtomSpace created: {atomspace.name}")
print()

print("2. Creating Agent Concept Nodes...")
agents = []
for i in range(3):
    agent_node = atomspace.add_node(
        node_type="ConceptNode",
        name=f"CognitiveAgent_{i}",
        truth_value=(0.9, 0.95),
        attention_value=0.6,
        metadata={
            "role": "autonomous_agent",
            "capabilities": ["reasoning", "planning", "execution"],
            "created": "2025-10-26"
        }
    )
    agents.append(agent_node)
    print(f"   ✓ Created: {agent_node.name} (ID: {agent_node.id[:8]}...)")
print()

print("3. Creating Capability Nodes...")
capabilities = []
capability_names = ["Reasoning", "Planning", "Execution", "Learning"]
for cap_name in capability_names:
    cap_node = atomspace.add_node(
        node_type="PredicateNode",
        name=cap_name,
        truth_value=(1.0, 1.0),
        attention_value=0.5
    )
    capabilities.append(cap_node)
    print(f"   ✓ Created capability: {cap_name}")
print()

print("4. Creating Inheritance Links (Agent -> Capability)...")
for agent in agents:
    for cap in capabilities[:3]:  # Each agent has first 3 capabilities
        link = atomspace.add_link(
            link_type="InheritanceLink",
            outgoing=[agent.id, cap.id],
            truth_value=(0.85, 0.9)
        )
        print(f"   ✓ Linked {agent.name} -> {cap.name}")
print()

print("5. Creating Task Nodes...")
task_node = atomspace.add_node(
    node_type="ConceptNode",
    name="ComplexTask",
    truth_value=(1.0, 1.0),
    attention_value=0.8,
    metadata={"priority": "high", "status": "active"}
)
print(f"   ✓ Created task: {task_node.name}")
print()

print("6. Assigning Task to Agent...")
execution_link = atomspace.add_link(
    link_type="ExecutionLink",
    outgoing=[agents[0].id, task_node.id],
    truth_value=(0.9, 0.85)
)
print(f"   ✓ Assigned {task_node.name} to {agents[0].name}")
print()

print("7. Pattern Matching - Finding All Agents...")
pattern = {"type": "ConceptNode", "name": "CognitiveAgent_*"}
matches = atomspace.pattern_match(pattern)
print(f"   ✓ Found {len(matches)} agents matching pattern")
for match in matches:
    print(f"     - {match.name}")
print()

print("8. Spreading Attention from ComplexTask...")
print(f"   Initial attention on {task_node.name}: {task_node.attention_value:.3f}")
atomspace.spread_activation(task_node.id, intensity=0.3, decay=0.6)
# Check updated attention
updated_task = atomspace.get_atom(task_node.id)
print(f"   Updated attention on {task_node.name}: {updated_task.attention_value:.3f}")
print()

print("9. Getting AtomSpace Statistics...")
stats = atomspace.get_stats()
print(f"   Total Atoms: {stats['total_atoms']}")
print(f"   Total Nodes: {stats['total_nodes']}")
print(f"   Total Links: {stats['total_links']}")
print(f"   Graph Density: {stats['graph_density']:.4f}")
print(f"   Atom Types:")
for atom_type, count in stats['types'].items():
    print(f"     - {atom_type}: {count}")
print()

print("10. Exporting Cognitive State...")
export_data = atomspace.export_to_dict()
print(f"    ✓ Exported {len(export_data['atoms'])} atoms")
print(f"    ✓ AtomSpace name: {export_data['name']}")
print()

print("11. Demonstrating Atom Retrieval...")
agent_0 = atomspace.get_atom_by_name("CognitiveAgent_0")
if agent_0:
    print(f"    ✓ Retrieved: {agent_0.name}")
    print(f"      Truth Value: {agent_0.truth_value}")
    print(f"      Attention: {agent_0.attention_value:.3f}")
    print(f"      Metadata: {agent_0.metadata}")
    
    # Get connections
    incoming = atomspace.get_incoming(agent_0.id)
    outgoing = atomspace.get_outgoing(agent_0.id)
    print(f"      Incoming links: {len(incoming)}")
    print(f"      Outgoing links: {len(outgoing)}")
print()

print("12. Global Orchestrator Statistics...")
global_stats = orchestrator.get_global_stats()
print(f"    Total AtomSpaces: {global_stats['total_atomspaces']}")
for space_name, space_stats in global_stats['atomspaces'].items():
    print(f"    Space '{space_name}':")
    print(f"      - Atoms: {space_stats['total_atoms']}")
    print(f"      - Density: {space_stats['graph_density']:.4f}")
print()

print("========================================")
print("Demo Complete!")
print("========================================")
print()
print("The OpenCog cognitive architecture provides:")
print("  • Knowledge representation via hypergraphs")
print("  • Multi-agent cognitive orchestration")
print("  • Pattern-based reasoning and matching")
print("  • Attention allocation mechanisms")
print("  • Adaptive evolutionary knowledge structures")
print()
print("Agents can use the 'opencog' tool to interact")
print("with the AtomSpace for cognitive operations.")
print("========================================")

PYTHON_SCRIPT

exit 0
