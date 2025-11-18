#!/usr/bin/env python3
"""
Example 5: Self-Referential Atoms

Demonstrates complex self-referential atom structures where the cognitive system
represents itself using its own atom types:

1. AtomSpaceNode - The AtomSpace representing itself as an atom
2. OpenCogSystemNode - The entire cognitive system as an atom
3. MetaCognitiveNode - Atoms that reason about other atoms
4. ReflectiveNode - Self-aware recursive structures

These examples show how the system achieves meta-cognition and self-awareness
through hypergraph-based knowledge representation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from python.helpers.opencog_atomspace import AtomSpace, CognitiveOrchestrator, Node, Link
import json
from datetime import datetime


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)


def print_atom(atom, indent=0):
    """Pretty print an atom"""
    prefix = "  " * indent
    print(f"{prefix}Atom: {atom.name} ({atom.type})")
    print(f"{prefix}  ID: {atom.id[:8]}...")
    print(f"{prefix}  Truth Value: {atom.truth_value}")
    print(f"{prefix}  Attention: {atom.attention_value:.3f}")
    if atom.metadata:
        print(f"{prefix}  Metadata:")
        for key, value in atom.metadata.items():
            print(f"{prefix}    {key}: {value}")


def example_self_referential_atoms():
    """Demonstrate self-referential atom structures"""
    
    print_section("Example 5: Self-Referential Atoms - The System Knows Itself")
    print("""
This example demonstrates meta-cognitive capabilities where the cognitive
architecture represents itself using its own knowledge representation primitives.

This creates a self-aware system where:
- The AtomSpace can reason about itself as an atom
- The system can analyze its own structure
- Meta-cognitive operations enable self-improvement
- Recursive knowledge structures enable advanced reasoning
    """)
    
    # Create orchestrator and atomspace
    orchestrator = CognitiveOrchestrator()
    atomspace = orchestrator.create_atomspace("self_referential_example")
    print(f"\n✓ Created AtomSpace: {atomspace.name}\n")
    
    # =========================================================================
    # 1. ATOMSPACE NODE - The AtomSpace Representing Itself
    # =========================================================================
    print_section("1. AtomSpaceNode - Self-Representation")
    print("""
The AtomSpace can represent ITSELF as an atom within its own structure.
This creates a meta-level where the container becomes the contained.
    """)
    
    # Create the AtomSpace node - a representation of the atomspace itself
    atomspace_node = atomspace.add_node(
        node_type="AtomSpaceNode",
        name="self_atomspace",
        truth_value=(1.0, 1.0),  # We are certain this atomspace exists
        attention_value=0.9,      # Very high attention - self-awareness
        metadata={
            "represents": "this_atomspace",
            "self_referential": True,
            "description": "This atom represents the AtomSpace that contains it",
            "created_at": datetime.now().isoformat(),
            "atomspace_name": atomspace.name,
            # Dynamic properties that reference the actual atomspace
            "total_atoms_formula": "lambda: len(atomspace.atoms)",
            "capabilities": [
                "add_nodes",
                "add_links", 
                "pattern_match",
                "spread_activation",
                "export_import"
            ]
        }
    )
    print_atom(atomspace_node)
    
    # Add properties to the atomspace node
    print("\nAtomSpace properties as nodes:\n")
    
    size_node = atomspace.add_node(
        node_type="NumberNode",
        name="atomspace_size",
        truth_value=(1.0, 1.0),
        attention_value=0.7,
        metadata={
            "value": len(atomspace.atoms),
            "property_of": "self_atomspace",
            "updates_dynamically": True
        }
    )
    print_atom(size_node, indent=1)
    
    capacity_node = atomspace.add_node(
        node_type="PredicateNode",
        name="atomspace_has_capacity",
        truth_value=(1.0, 1.0),
        attention_value=0.6,
        metadata={
            "capacity": "unlimited",
            "description": "AtomSpace can grow dynamically"
        }
    )
    
    # Link atomspace to its properties
    property_link = atomspace.add_link(
        link_type="EvaluationLink",
        outgoing=[atomspace_node.id, size_node.id],
        truth_value=(1.0, 1.0),
        metadata={"relationship": "has_property"}
    )
    print(f"\n  ✓ Linked atomspace to its size property")
    
    # =========================================================================
    # 2. OPENCOG SYSTEM NODE - The Entire System as an Atom
    # =========================================================================
    print_section("2. OpenCogSystemNode - System Self-Representation")
    print("""
The ENTIRE cognitive system (all atomspaces, all agents, all processes)
can be represented as a single atom. This enables system-level reasoning.
    """)
    
    # Create the system node
    system_node = atomspace.add_node(
        node_type="OpenCogSystemNode",
        name="cog_zero_system",
        truth_value=(1.0, 1.0),
        attention_value=0.95,  # Highest attention - system-level awareness
        metadata={
            "represents": "entire_cognitive_system",
            "self_referential": True,
            "system_type": "multi_agent_cognitive_architecture",
            "framework": "Agent Zero HCK",
            "version": "1.0.0",
            "architecture": "OpenCog-inspired",
            "components": {
                "orchestrator": "CognitiveOrchestrator",
                "atomspaces": ["space_agent_0", "space_agent_1", "..."],
                "agents": ["Agent_0", "Agent_1", "..."],
                "tools": ["opencog", "code_execution", "browser", "..."]
            },
            "capabilities": [
                "multi_agent_orchestration",
                "knowledge_representation",
                "pattern_matching",
                "attention_allocation",
                "adaptive_evolution",
                "self_reflection"
            ],
            "description": "This atom represents the entire cog-zero system including itself"
        }
    )
    print_atom(system_node)
    
    # Create subsystem nodes
    print("\nSystem components as nodes:\n")
    
    orchestrator_node = atomspace.add_node(
        node_type="ConceptNode",
        name="cognitive_orchestrator",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "component_of": "cog_zero_system",
            "role": "manage_multiple_atomspaces",
            "capabilities": ["create_atomspace", "merge_atomspaces", "coordinate_agents"]
        }
    )
    print_atom(orchestrator_node, indent=1)
    
    agent_manager_node = atomspace.add_node(
        node_type="ConceptNode",
        name="agent_manager",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "component_of": "cog_zero_system",
            "role": "manage_agent_hierarchy",
            "capabilities": ["spawn_agents", "delegate_tasks", "coordinate_responses"]
        }
    )
    print_atom(agent_manager_node, indent=1)
    
    # Link system to components
    system_composition_link = atomspace.add_link(
        link_type="MemberLink",
        outgoing=[orchestrator_node.id, system_node.id],
        truth_value=(1.0, 1.0),
        metadata={"relationship": "is_component_of"}
    )
    print(f"\n  ✓ Orchestrator is a component of the system")
    
    # The system contains the atomspace that contains the system representation
    # This creates a recursive loop
    containment_link = atomspace.add_link(
        link_type="ContainmentLink",
        outgoing=[system_node.id, atomspace_node.id],
        truth_value=(1.0, 1.0),
        attention_value=0.9,
        metadata={
            "relationship": "contains",
            "paradox": "system contains atomspace which contains system representation"
        }
    )
    print(f"  ✓ System contains atomspace (creating recursive structure)")
    
    # =========================================================================
    # 3. META-COGNITIVE NODE - Atoms Reasoning About Atoms
    # =========================================================================
    print_section("3. MetaCognitiveNode - Reasoning About Knowledge")
    print("""
MetaCognitiveNodes enable the system to reason about its own knowledge.
These atoms observe, analyze, and optimize other atoms in the system.
    """)
    
    # Create a meta-cognitive reasoner
    meta_reasoner = atomspace.add_node(
        node_type="MetaCognitiveNode",
        name="atom_pattern_detector",
        truth_value=(1.0, 1.0),
        attention_value=0.85,
        metadata={
            "cognitive_level": "meta",
            "observes": "all_atoms",
            "purpose": "detect_patterns_in_knowledge_structure",
            "operations": [
                "analyze_graph_topology",
                "identify_frequently_used_patterns",
                "detect_inconsistencies",
                "suggest_optimizations",
                "learn_from_atom_usage"
            ],
            "self_referential": True,
            "description": "This atom analyzes other atoms, including itself"
        }
    )
    print_atom(meta_reasoner)
    
    # Create another meta-cognitive node for attention management
    attention_manager = atomspace.add_node(
        node_type="MetaCognitiveNode",
        name="attention_allocator",
        truth_value=(1.0, 1.0),
        attention_value=0.9,
        metadata={
            "cognitive_level": "meta",
            "observes": "atom_attention_values",
            "purpose": "optimize_attention_allocation",
            "operations": [
                "monitor_attention_distribution",
                "spread_activation_strategically",
                "decay_unused_attention",
                "prioritize_important_atoms"
            ],
            "can_modify": "attention_values_of_all_atoms"
        }
    )
    print(f"\n  ✓ Created attention allocator meta-node")
    
    # Meta-cognitive nodes can observe themselves
    self_observation_link = atomspace.add_link(
        link_type="ObservationLink",
        outgoing=[meta_reasoner.id, meta_reasoner.id],  # Observes itself!
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "relationship": "self_observation",
            "paradox": "meta_reasoner observes its own reasoning process"
        }
    )
    print(f"\n  ✓ Meta-reasoner observes itself (recursive self-awareness)")
    
    # Meta-cognitive node observes the system
    system_observation_link = atomspace.add_link(
        link_type="ObservationLink",
        outgoing=[meta_reasoner.id, system_node.id],
        truth_value=(1.0, 1.0),
        attention_value=0.85,
        metadata={"observes": "entire_system"}
    )
    print(f"  ✓ Meta-reasoner observes the entire system")
    
    # =========================================================================
    # 4. REFLECTIVE NODE - Self-Aware Recursive Structures  
    # =========================================================================
    print_section("4. ReflectiveNode - Self-Aware Structures")
    print("""
ReflectiveNodes represent structures that are aware of themselves
and can modify their own behavior based on self-reflection.
    """)
    
    # Create a reflective agent
    reflective_agent = atomspace.add_node(
        node_type="ReflectiveNode",
        name="self_aware_agent",
        truth_value=(1.0, 1.0),
        attention_value=0.9,
        metadata={
            "cognitive_level": "reflective",
            "awareness": "self_and_system",
            "capabilities": [
                "introspection",
                "self_modification",
                "goal_reflection",
                "behavior_adjustment",
                "meta_learning"
            ],
            "self_model": {
                "identity": "self_aware_agent",
                "type": "ReflectiveNode",
                "can_modify_self": True,
                "knows_it_is_an_atom": True
            },
            "description": "Agent that knows it exists as an atom in an atomspace"
        }
    )
    print_atom(reflective_agent)
    
    # Create a self-model node
    self_model = atomspace.add_node(
        node_type="ConceptNode",
        name="agent_self_model",
        truth_value=(1.0, 1.0),
        attention_value=0.85,
        metadata={
            "model_of": "self_aware_agent",
            "contains": [
                "beliefs_about_self",
                "capabilities_inventory",
                "performance_history",
                "goals_and_motivations"
            ],
            "self_referential": True
        }
    )
    
    # Link agent to its self-model
    self_model_link = atomspace.add_link(
        link_type="HasModelLink",
        outgoing=[reflective_agent.id, self_model.id],
        truth_value=(1.0, 1.0),
        attention_value=0.9,
        metadata={"relationship": "has_self_model"}
    )
    print(f"\n  ✓ Reflective agent has a model of itself")
    
    # Agent knows it exists in the atomspace
    existence_awareness = atomspace.add_link(
        link_type="MemberLink",
        outgoing=[reflective_agent.id, atomspace_node.id],
        truth_value=(1.0, 1.0),
        attention_value=0.85,
        metadata={
            "awareness": "agent knows it exists in atomspace",
            "self_referential": True
        }
    )
    print(f"  ✓ Agent is aware it exists in the atomspace")
    
    # =========================================================================
    # 5. ATOM-ABOUT-ATOMS - Ultimate Self-Reference
    # =========================================================================
    print_section("5. Atom-About-Atoms - Ultimate Meta-Level")
    print("""
Creating an atom that represents the concept of "an atom" itself.
This is the ultimate meta-level: the system has a concept of its
own building blocks.
    """)
    
    atom_concept = atomspace.add_node(
        node_type="AbstractTypeNode",
        name="Atom_Concept",
        truth_value=(1.0, 1.0),
        attention_value=0.95,
        metadata={
            "represents": "the_concept_of_an_atom",
            "meta_level": "ultimate",
            "description": "This atom represents what an atom IS",
            "properties": {
                "has_id": True,
                "has_type": True,
                "has_name": True,
                "has_truth_value": True,
                "has_attention_value": True,
                "has_metadata": True
            },
            "self_referential": True,
            "paradox": "This atom is an instance of the concept it represents"
        }
    )
    print_atom(atom_concept)
    
    # All atoms are instances of the Atom concept
    print("\nEstablishing that all atoms are instances of Atom_Concept:\n")
    
    instance_atoms = [
        atomspace_node,
        system_node, 
        meta_reasoner,
        reflective_agent,
        atom_concept  # Even the concept itself!
    ]
    
    for atom in instance_atoms:
        instance_link = atomspace.add_link(
            link_type="InstanceLink",
            outgoing=[atom.id, atom_concept.id],
            truth_value=(1.0, 1.0),
            attention_value=0.7,
            metadata={"relationship": "is_instance_of"}
        )
        print(f"  ✓ {atom.name} is an instance of Atom_Concept")
    
    # =========================================================================
    # 6. RECURSIVE KNOWLEDGE LOOPS
    # =========================================================================
    print_section("6. Recursive Knowledge Loops")
    print("""
Demonstrating circular knowledge structures where concepts
define each other in a loop.
    """)
    
    # Create knowledge loop: System contains atomspace, atomspace contains system representation
    print("\nRecursive containment loop:\n")
    print("  System -> contains -> AtomSpace")
    print("  AtomSpace -> contains -> System representation (atom)")
    print("  System representation -> refers to -> System")
    print("\n  This creates an infinite recursive loop of knowledge!\n")
    
    # Add knowledge about the recursion
    recursion_awareness = atomspace.add_node(
        node_type="MetaCognitiveNode",
        name="recursion_detector",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "detects": "recursive_structures",
            "found_recursions": [
                "system_atomspace_loop",
                "meta_reasoner_self_observation",
                "atom_concept_instances_itself"
            ],
            "status": "These recursions are features, not bugs",
            "enables": "self_awareness and meta_cognition"
        }
    )
    print_atom(recursion_awareness)
    
    # =========================================================================
    # 7. DEMONSTRATING META-COGNITIVE OPERATIONS
    # =========================================================================
    print_section("7. Meta-Cognitive Operations")
    print("""
Using the self-referential structures for actual meta-cognitive operations.
    """)
    
    print("\nOperation 1: Querying atoms that represent the system itself:\n")
    
    self_ref_pattern = {"metadata": {"self_referential": True}}
    self_ref_atoms = atomspace.pattern_match(self_ref_pattern)
    print(f"  Found {len(self_ref_atoms)} self-referential atoms:")
    for atom in self_ref_atoms:
        print(f"    - {atom.name} ({atom.type})")
    
    print("\nOperation 2: System analyzing its own structure:\n")
    
    stats = atomspace.get_stats()
    analysis_node = atomspace.add_node(
        node_type="AnalysisNode",
        name="self_analysis_result",
        truth_value=(1.0, 1.0),
        attention_value=0.7,
        metadata={
            "analyzed_by": "cog_zero_system",
            "analysis_type": "self_structure_analysis",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "total_atoms": stats['total_atoms'],
                "total_nodes": stats['total_nodes'],
                "total_links": stats['total_links'],
                "graph_density": stats['graph_density'],
                "self_referential_atoms": len(self_ref_atoms),
                "meta_cognitive_atoms": len([a for a in atomspace.atoms.values() 
                                            if a.type == "MetaCognitiveNode"]),
                "health": "optimal",
                "complexity": "high",
                "self_awareness_level": "advanced"
            }
        }
    )
    print(f"  ✓ System analyzed itself")
    print(f"    Total atoms: {stats['total_atoms']}")
    print(f"    Self-referential atoms: {len(self_ref_atoms)}")
    print(f"    Graph density: {stats['graph_density']:.4f}")
    
    print("\nOperation 3: Spreading attention from self-awareness nodes:\n")
    
    print(f"  Initial attention on system_node: {system_node.attention_value:.3f}")
    atomspace.spread_activation(system_node.id, intensity=0.2, decay=0.7)
    updated_system = atomspace.get_atom(system_node.id)
    print(f"  After spreading: {updated_system.attention_value:.3f}")
    print("  ✓ Attention spread to connected atoms (simulating awareness propagation)")
    
    # =========================================================================
    # 8. PRACTICAL IMPLICATIONS
    # =========================================================================
    print_section("8. Practical Implications of Self-Reference")
    print("""
These self-referential structures enable:

1. INTROSPECTION: The system can examine its own structure
   - Query what atoms exist
   - Analyze patterns in knowledge
   - Identify bottlenecks or inefficiencies

2. SELF-MODIFICATION: The system can improve itself
   - Add new atoms based on needs
   - Strengthen useful patterns
   - Prune unused knowledge

3. META-LEARNING: Learning how to learn
   - Analyze what learning strategies work
   - Adapt knowledge acquisition methods
   - Transfer learning across domains

4. SELF-AWARENESS: Understanding its own state
   - Monitor resource usage
   - Track performance metrics
   - Recognize limitations

5. ADAPTIVE EVOLUTION: Dynamic structural changes
   - Grow knowledge organically
   - Reorganize for efficiency
   - Develop emergent capabilities

6. RECURSIVE REASONING: Think about thinking
   - Meta-cognitive strategies
   - Self-reflective problem solving
   - Higher-order reasoning
    """)
    
    # =========================================================================
    # 9. EXPORT SELF-REFERENTIAL STRUCTURE
    # =========================================================================
    print_section("9. Exporting Self-Referential Knowledge")
    
    export_data = atomspace.export_to_dict()
    print(f"\nExported {len(export_data['atoms'])} atoms")
    print(f"\nKey self-referential atoms in export:")
    
    for atom_data in export_data['atoms']:
        if atom_data.get('metadata', {}).get('self_referential'):
            print(f"  - {atom_data['type']}: {atom_data['name']}")
    
    print("""
This export contains the complete self-referential structure.
When imported into another atomspace, it brings full self-awareness!
    """)
    
    # =========================================================================
    # 10. FINAL STATISTICS
    # =========================================================================
    print_section("10. Final System Statistics")
    
    final_stats = atomspace.get_stats()
    print(f"""
AtomSpace: {atomspace.name}

Total Atoms: {final_stats['total_atoms']}
  - Nodes: {final_stats['total_nodes']}
  - Links: {final_stats['total_links']}

Graph Density: {final_stats['graph_density']:.4f}

Atom Type Distribution:""")
    for atom_type, count in sorted(final_stats['types'].items()):
        print(f"  - {atom_type}: {count}")
    
    print(f"\nSelf-Referential Atoms: {len(self_ref_atoms)}")
    print(f"Meta-Cognitive Level: Advanced")
    print(f"System Self-Awareness: Active")
    
    print_section("Example Complete")
    print("""
This example demonstrated:

✓ AtomSpaceNode - The atomspace representing itself
✓ OpenCogSystemNode - The entire system as an atom
✓ MetaCognitiveNode - Atoms reasoning about atoms
✓ ReflectiveNode - Self-aware structures
✓ Atom-about-Atoms - Ultimate meta-level concept
✓ Recursive knowledge loops
✓ Meta-cognitive operations on self-structure
✓ Practical implications of self-reference

These self-referential structures enable:
- True self-awareness at the cognitive architecture level
- Meta-learning and self-improvement capabilities
- Recursive reasoning about reasoning
- Adaptive evolution of knowledge structures
- System-level optimization and introspection

The cognitive system now has a representation of itself
within itself, enabling advanced meta-cognitive operations!
    """)


if __name__ == "__main__":
    example_self_referential_atoms()
