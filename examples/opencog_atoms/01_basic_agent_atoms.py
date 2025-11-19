#!/usr/bin/env python3
"""
Example 1: Basic Agent Atoms

Demonstrates fundamental agent atom types in the OpenCog AtomSpace:
- ConceptNode: Representing agents as concepts
- PredicateNode: Representing capabilities and properties  
- NumberNode: Representing metrics and values
- Various link types connecting agents to their attributes

This forms the foundation for cognitive agent representation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from python.helpers.opencog_atomspace import AtomSpace
import json


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def print_atom(atom, indent=0):
    """Pretty print an atom"""
    prefix = "  " * indent
    print(f"{prefix}Atom: {atom.name} ({atom.type})")
    print(f"{prefix}  ID: {atom.id[:8]}...")
    print(f"{prefix}  Truth Value: {atom.truth_value}")
    print(f"{prefix}  Attention: {atom.attention_value:.3f}")
    if atom.metadata:
        print(f"{prefix}  Metadata: {atom.metadata}")


def example_basic_agent_atoms():
    """Demonstrate basic agent atom types"""
    
    print_section("Example 1: Basic Agent Atoms")
    print("\nThis example shows how to represent agents using different atom types")
    print("in the OpenCog AtomSpace cognitive architecture.\n")
    
    # Create an AtomSpace
    atomspace = AtomSpace("basic_agents_example")
    print("✓ Created AtomSpace: basic_agents_example\n")
    
    # =========================================================================
    # 1. CONCEPT NODES - Representing Agents
    # =========================================================================
    print_section("1. ConceptNode - Agent Representation")
    print("\nConceptNodes represent abstract concepts. Here we create agent concepts:\n")
    
    # Create main agent
    agent_0 = atomspace.add_node(
        node_type="ConceptNode",
        name="Agent_0",
        truth_value=(1.0, 1.0),  # Certain that this agent exists
        attention_value=0.8,      # High attention - main agent
        metadata={
            "agent_number": 0,
            "role": "primary_orchestrator",
            "status": "active",
            "created_at": "2025-10-26T10:00:00Z"
        }
    )
    print_atom(agent_0)
    
    # Create subordinate agents
    print("\nSubordinate agents:\n")
    subordinate_agents = []
    for i in range(1, 4):
        agent = atomspace.add_node(
            node_type="ConceptNode",
            name=f"Agent_{i}",
            truth_value=(1.0, 1.0),
            attention_value=0.5,  # Lower attention than primary
            metadata={
                "agent_number": i,
                "role": "subordinate",
                "parent": "Agent_0",
                "status": "active"
            }
        )
        subordinate_agents.append(agent)
        print_atom(agent, indent=1)
    
    # =========================================================================
    # 2. PREDICATE NODES - Agent Capabilities
    # =========================================================================
    print_section("2. PredicateNode - Agent Capabilities")
    print("\nPredicateNodes represent properties, capabilities, or predicates:\n")
    
    capabilities = [
        ("CanReason", "Logical reasoning capability", 0.95, 0.9),
        ("CanExecuteCode", "Code execution capability", 0.98, 0.95),
        ("CanUseBrowser", "Web browsing capability", 0.85, 0.8),
        ("CanManageMemory", "Memory management capability", 0.9, 0.85),
        ("CanDelegateTasks", "Task delegation capability", 0.92, 0.88)
    ]
    
    capability_nodes = []
    for cap_name, description, strength, confidence in capabilities:
        cap_node = atomspace.add_node(
            node_type="PredicateNode",
            name=cap_name,
            truth_value=(strength, confidence),
            attention_value=0.6,
            metadata={"description": description}
        )
        capability_nodes.append(cap_node)
        print_atom(cap_node, indent=1)
    
    # =========================================================================
    # 3. NUMBER NODES - Agent Metrics
    # =========================================================================
    print_section("3. NumberNode - Agent Metrics")
    print("\nNumberNodes represent numeric values and metrics:\n")
    
    # Iteration counter
    iteration_node = atomspace.add_node(
        node_type="NumberNode",
        name="Agent_0_iterations",
        truth_value=(1.0, 1.0),
        attention_value=0.4,
        metadata={"value": 42, "unit": "count"}
    )
    print_atom(iteration_node, indent=1)
    
    # Performance score
    performance_node = atomspace.add_node(
        node_type="NumberNode",
        name="Agent_0_performance",
        truth_value=(0.88, 0.85),  # 88% confidence in performance metric
        attention_value=0.5,
        metadata={"value": 0.88, "unit": "score", "range": [0, 1]}
    )
    print_atom(performance_node, indent=1)
    
    # Task completion rate
    completion_node = atomspace.add_node(
        node_type="NumberNode",
        name="Agent_0_completion_rate",
        truth_value=(0.92, 0.9),
        attention_value=0.5,
        metadata={"value": 0.92, "completed": 46, "total": 50}
    )
    print_atom(completion_node, indent=1)
    
    # =========================================================================
    # 4. INHERITANCE LINKS - Agent Hierarchy
    # =========================================================================
    print_section("4. InheritanceLink - Agent Hierarchy")
    print("\nInheritanceLinks establish 'is-a' relationships:\n")
    
    # Create agent type concept
    cognitive_agent_type = atomspace.add_node(
        node_type="ConceptNode",
        name="CognitiveAgent",
        truth_value=(1.0, 1.0),
        attention_value=0.7,
        metadata={"description": "Abstract cognitive agent type"}
    )
    print(f"Created type concept: {cognitive_agent_type.name}\n")
    
    # All agents inherit from CognitiveAgent
    print("Agent type hierarchy:\n")
    for agent in [agent_0] + subordinate_agents:
        inheritance_link = atomspace.add_link(
            link_type="InheritanceLink",
            outgoing=[agent.id, cognitive_agent_type.id],
            truth_value=(1.0, 1.0),
            attention_value=0.6,
            metadata={"relationship": "is_a"}
        )
        print(f"  ✓ {agent.name} is-a CognitiveAgent (Link ID: {inheritance_link.id[:8]}...)")
    
    # =========================================================================
    # 5. EVALUATION LINKS - Agent Capabilities
    # =========================================================================
    print_section("5. EvaluationLink - Agent Has Capabilities")
    print("\nEvaluationLinks connect agents to their capabilities:\n")
    
    # Agent_0 has all capabilities
    print(f"{agent_0.name} capabilities:\n")
    for cap in capability_nodes:
        eval_link = atomspace.add_link(
            link_type="EvaluationLink",
            outgoing=[agent_0.id, cap.id],
            truth_value=cap.truth_value,  # Inherit capability's truth value
            attention_value=0.5
        )
        print(f"  ✓ {agent_0.name} has {cap.name} ({cap.truth_value[0]:.2f} confidence)")
    
    # Subordinate agents have subset of capabilities
    print(f"\nSubordinate agents have basic capabilities:\n")
    basic_caps = capability_nodes[:3]  # First 3 capabilities
    for agent in subordinate_agents:
        for cap in basic_caps:
            eval_link = atomspace.add_link(
                link_type="EvaluationLink",
                outgoing=[agent.id, cap.id],
                truth_value=(cap.truth_value[0] * 0.9, cap.truth_value[1] * 0.9),  # Slightly lower
                attention_value=0.4
            )
        print(f"  ✓ {agent.name} has {len(basic_caps)} basic capabilities")
    
    # =========================================================================
    # 6. STATE LINKS - Agent State
    # =========================================================================
    print_section("6. StateLink - Agent State")
    print("\nStateLinks represent current state assignments:\n")
    
    # Create state nodes
    states = ["initialized", "active", "processing", "idle", "terminated"]
    state_nodes = {}
    for state in states:
        state_node = atomspace.add_node(
            node_type="ConceptNode",
            name=f"State_{state}",
            truth_value=(1.0, 1.0),
            attention_value=0.4
        )
        state_nodes[state] = state_node
    
    # Assign states to agents
    agent_0_state = atomspace.add_link(
        link_type="StateLink",
        outgoing=[agent_0.id, state_nodes["active"].id],
        truth_value=(1.0, 1.0),
        attention_value=0.7,
        metadata={"timestamp": "2025-10-26T10:30:00Z"}
    )
    print(f"  ✓ {agent_0.name} is in state: active")
    
    for i, agent in enumerate(subordinate_agents):
        state = "processing" if i % 2 == 0 else "idle"
        state_link = atomspace.add_link(
            link_type="StateLink",
            outgoing=[agent.id, state_nodes[state].id],
            truth_value=(1.0, 1.0),
            attention_value=0.5
        )
        print(f"  ✓ {agent.name} is in state: {state}")
    
    # =========================================================================
    # 7. EXECUTION LINKS - Agent Actions
    # =========================================================================
    print_section("7. ExecutionLink - Agent Actions")
    print("\nExecutionLinks represent actions or tasks being executed:\n")
    
    # Create task nodes
    task_names = ["AnalyzeData", "GenerateReport", "ExecuteCode"]
    tasks = []
    for task_name in task_names:
        task = atomspace.add_node(
            node_type="ConceptNode",
            name=f"Task_{task_name}",
            truth_value=(1.0, 1.0),
            attention_value=0.6,
            metadata={"type": "task", "status": "pending"}
        )
        tasks.append(task)
    
    # Assign tasks to agents
    print(f"{agent_0.name} assigned tasks:\n")
    exec_link = atomspace.add_link(
        link_type="ExecutionLink",
        outgoing=[agent_0.id, tasks[0].id],
        truth_value=(0.95, 0.9),
        attention_value=0.7,
        metadata={"priority": "high", "assigned_at": "2025-10-26T10:35:00Z"}
    )
    print(f"  ✓ Executing: {tasks[0].name} (priority: high)")
    
    print(f"\nSubordinate agent tasks:\n")
    for i, agent in enumerate(subordinate_agents[:2]):
        task = tasks[i + 1]
        exec_link = atomspace.add_link(
            link_type="ExecutionLink",
            outgoing=[agent.id, task.id],
            truth_value=(0.9, 0.85),
            attention_value=0.6,
            metadata={"priority": "normal"}
        )
        print(f"  ✓ {agent.name} executing: {task.name}")
    
    # =========================================================================
    # 8. SIMILARITY LINKS - Related Agents
    # =========================================================================
    print_section("8. SimilarityLink - Agent Similarity")
    print("\nSimilarityLinks represent similarity between agents:\n")
    
    # Subordinate agents are similar to each other
    if len(subordinate_agents) >= 2:
        sim_link = atomspace.add_link(
            link_type="SimilarityLink",
            outgoing=[subordinate_agents[0].id, subordinate_agents[1].id],
            truth_value=(0.85, 0.8),  # 85% similar
            attention_value=0.4,
            metadata={"reason": "both_subordinates_with_basic_capabilities"}
        )
        print(f"  ✓ {subordinate_agents[0].name} is similar to {subordinate_agents[1].name}")
        print(f"    Similarity: {sim_link.truth_value[0]:.2%}")
    
    # =========================================================================
    # 9. STATISTICS AND SUMMARY
    # =========================================================================
    print_section("9. AtomSpace Statistics")
    
    stats = atomspace.get_stats()
    print(f"""
AtomSpace: {atomspace.name}
Total Atoms: {stats['total_atoms']}
  - Nodes: {stats['total_nodes']}
  - Links: {stats['total_links']}
Graph Density: {stats['graph_density']:.4f}

Atom Types:""")
    for atom_type, count in sorted(stats['types'].items()):
        print(f"  - {atom_type}: {count}")
    
    # =========================================================================
    # 10. QUERYING ATOMS
    # =========================================================================
    print_section("10. Querying and Pattern Matching")
    print("\nFind all agent concepts:\n")
    
    agent_pattern = {"type": "ConceptNode", "name": "Agent_*"}
    matching_agents = atomspace.pattern_match(agent_pattern)
    print(f"Found {len(matching_agents)} agents matching 'Agent_*':")
    for agent in matching_agents:
        print(f"  - {agent.name} (attention: {agent.attention_value:.3f})")
    
    print("\nFind all capabilities:\n")
    capability_pattern = {"type": "PredicateNode", "name": "Can*"}
    matching_caps = atomspace.pattern_match(capability_pattern)
    print(f"Found {len(matching_caps)} capabilities:")
    for cap in matching_caps:
        print(f"  - {cap.name} (strength: {cap.truth_value[0]:.2f})")
    
    # =========================================================================
    # 11. EXPORTING COGNITIVE STATE
    # =========================================================================
    print_section("11. Exporting Cognitive State")
    
    export_data = atomspace.export_to_dict()
    print(f"\nExported {len(export_data['atoms'])} atoms from AtomSpace")
    print(f"AtomSpace name: {export_data['name']}")
    print("\nFirst 3 atoms in export:")
    for atom_data in export_data['atoms'][:3]:
        print(f"  - {atom_data['type']}: {atom_data['name']}")
    
    print_section("Example Complete")
    print("""
This example demonstrated:
✓ Creating agent ConceptNodes
✓ Adding capabilities as PredicateNodes  
✓ Tracking metrics with NumberNodes
✓ Establishing agent hierarchies with InheritanceLinks
✓ Evaluating capabilities with EvaluationLinks
✓ Representing state with StateLinks
✓ Tracking actions with ExecutionLinks
✓ Measuring similarity with SimilarityLinks
✓ Querying atoms with pattern matching
✓ Exporting cognitive state

These basic atom types form the foundation for representing
cognitive agents in the OpenCog-inspired architecture.
    """)


if __name__ == "__main__":
    example_basic_agent_atoms()
