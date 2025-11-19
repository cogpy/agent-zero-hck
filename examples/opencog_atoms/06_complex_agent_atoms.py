#!/usr/bin/env python3
"""
Example 6: Complex Agent Atoms

Demonstrates advanced agent atom patterns including:
- Nested agent hierarchies
- Agent swarms and collectives
- Temporal agent states
- Evolutionary agent patterns
- Cross-agent knowledge sharing
- Agent specialization and roles

These complex patterns show how sophisticated multi-agent systems
can be represented in the AtomSpace.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from python.helpers.opencog_atomspace import AtomSpace, CognitiveOrchestrator
from datetime import datetime, timedelta
import json


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)


def print_atom(atom, indent=0):
    """Pretty print an atom"""
    prefix = "  " * indent
    print(f"{prefix}{atom.name} ({atom.type})")
    print(f"{prefix}  Truth: {atom.truth_value}, Attention: {atom.attention_value:.3f}")


def example_complex_agent_atoms():
    """Demonstrate complex agent atom patterns"""
    
    print_section("Example 6: Complex Agent Atoms")
    print("""
This example demonstrates advanced patterns for representing complex
multi-agent systems using cognitive atoms.
    """)
    
    orchestrator = CognitiveOrchestrator()
    atomspace = orchestrator.create_atomspace("complex_agents")
    print(f"\n✓ Created AtomSpace: {atomspace.name}\n")
    
    # =========================================================================
    # 1. NESTED AGENT HIERARCHIES
    # =========================================================================
    print_section("1. Nested Agent Hierarchies")
    print("\nCreating a deep hierarchical agent structure:\n")
    
    # Root agent
    root_agent = atomspace.add_node(
        node_type="AgentNode",
        name="CEO_Agent",
        truth_value=(1.0, 1.0),
        attention_value=0.9,
        metadata={
            "level": 0,
            "role": "chief_executive",
            "authority": "highest",
            "manages": "entire_system"
        }
    )
    print_atom(root_agent)
    
    # Level 1: Department heads
    departments = ["Engineering", "Research", "Operations"]
    dept_agents = []
    for dept in departments:
        agent = atomspace.add_node(
            node_type="AgentNode",
            name=f"{dept}_Head",
            truth_value=(1.0, 1.0),
            attention_value=0.7,
            metadata={
                "level": 1,
                "role": "department_head",
                "department": dept,
                "reports_to": "CEO_Agent"
            }
        )
        dept_agents.append(agent)
        
        # Create supervision link
        atomspace.add_link(
            link_type="SupervisionLink",
            outgoing=[root_agent.id, agent.id],
            truth_value=(1.0, 1.0),
            metadata={"relationship": "supervises"}
        )
        print_atom(agent, indent=1)
    
    # Level 2: Team leads
    print("\nTeam leads:\n")
    for dept_agent in dept_agents:
        for i in range(2):
            team_agent = atomspace.add_node(
                node_type="AgentNode",
                name=f"{dept_agent.metadata['department']}_Team_{i}",
                truth_value=(1.0, 1.0),
                attention_value=0.5,
                metadata={
                    "level": 2,
                    "role": "team_lead",
                    "reports_to": dept_agent.name
                }
            )
            atomspace.add_link(
                link_type="SupervisionLink",
                outgoing=[dept_agent.id, team_agent.id],
                truth_value=(1.0, 1.0)
            )
            print_atom(team_agent, indent=2)
    
    # =========================================================================
    # 2. AGENT SWARMS AND COLLECTIVES
    # =========================================================================
    print_section("2. Agent Swarms and Collectives")
    print("\nCreating swarm of homogeneous agents for parallel processing:\n")
    
    # Create swarm coordinator
    swarm_coordinator = atomspace.add_node(
        node_type="SwarmCoordinatorNode",
        name="DataProcessing_Swarm_Coordinator",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "swarm_type": "data_processing",
            "coordination_strategy": "distributed",
            "load_balancing": "dynamic"
        }
    )
    print_atom(swarm_coordinator)
    
    # Create swarm members
    print("\nSwarm members:\n")
    swarm_size = 10
    swarm_members = []
    for i in range(swarm_size):
        member = atomspace.add_node(
            node_type="SwarmMemberNode",
            name=f"Worker_{i:03d}",
            truth_value=(1.0, 1.0),
            attention_value=0.3,
            metadata={
                "swarm": "DataProcessing_Swarm_Coordinator",
                "status": "idle",
                "capabilities": ["map", "reduce", "filter", "process"],
                "performance": 0.95 + (i % 10) * 0.005  # Slight variation
            }
        )
        swarm_members.append(member)
        
        # Link to coordinator
        atomspace.add_link(
            link_type="MemberLink",
            outgoing=[member.id, swarm_coordinator.id],
            truth_value=(1.0, 1.0),
            metadata={"member_of": "swarm"}
        )
    
    print(f"  ✓ Created {swarm_size} swarm members")
    
    # Create swarm collective intelligence node
    collective_intelligence = atomspace.add_node(
        node_type="CollectiveNode",
        name="Swarm_Collective_Intelligence",
        truth_value=(1.0, 1.0),
        attention_value=0.75,
        metadata={
            "emerges_from": "swarm_interactions",
            "capabilities": [
                "distributed_problem_solving",
                "parallel_processing",
                "fault_tolerance",
                "adaptive_load_balancing"
            ],
            "performance_multiplier": swarm_size * 0.95
        }
    )
    print(f"\n  ✓ Swarm exhibits collective intelligence")
    
    # =========================================================================
    # 3. AGENT ROLES AND SPECIALIZATIONS
    # =========================================================================
    print_section("3. Agent Roles and Specializations")
    print("\nDefining specialized agent roles:\n")
    
    roles = [
        ("Analyst", "data_analysis", ["analyze", "visualize", "report"], 0.92),
        ("Executor", "task_execution", ["execute", "monitor", "retry"], 0.95),
        ("Researcher", "research", ["search", "synthesize", "document"], 0.88),
        ("Coordinator", "coordination", ["schedule", "delegate", "integrate"], 0.90),
        ("Guardian", "security", ["monitor", "protect", "audit"], 0.98)
    ]
    
    specialized_agents = []
    for role_name, specialization, capabilities, performance in roles:
        agent = atomspace.add_node(
            node_type="SpecializedAgentNode",
            name=f"{role_name}_Agent",
            truth_value=(performance, 0.9),
            attention_value=0.6,
            metadata={
                "role": role_name,
                "specialization": specialization,
                "capabilities": capabilities,
                "expertise_level": performance,
                "training_complete": True
            }
        )
        specialized_agents.append(agent)
        print_atom(agent, indent=1)
        
        # Create capability nodes and links
        for cap in capabilities:
            cap_node = atomspace.add_node(
                node_type="CapabilityNode",
                name=f"Capability_{cap}",
                truth_value=(1.0, 1.0),
                attention_value=0.4
            )
            atomspace.add_link(
                link_type="HasCapabilityLink",
                outgoing=[agent.id, cap_node.id],
                truth_value=(performance, 0.9)
            )
    
    # =========================================================================
    # 4. TEMPORAL AGENT STATES
    # =========================================================================
    print_section("4. Temporal Agent States and Evolution")
    print("\nTracking agent state changes over time:\n")
    
    evolving_agent = atomspace.add_node(
        node_type="EvolvingAgentNode",
        name="Learning_Agent_Alpha",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "current_state": "learning",
            "evolution_stage": "growth",
            "creation_time": datetime.now().isoformat()
        }
    )
    print_atom(evolving_agent)
    
    # Create temporal state sequence
    print("\nAgent lifecycle states:\n")
    states = [
        ("Initialization", 0, "just_created"),
        ("Learning", 1, "acquiring_knowledge"),
        ("Competent", 2, "performing_tasks"),
        ("Expert", 3, "high_performance"),
        ("Mentor", 4, "teaching_others")
    ]
    
    prev_state_node = None
    for state_name, stage, description in states:
        state_node = atomspace.add_node(
            node_type="TemporalStateNode",
            name=f"State_{state_name}_{evolving_agent.name}",
            truth_value=(1.0, 1.0),
            attention_value=0.6 if stage == 1 else 0.4,  # Current state higher
            metadata={
                "state": state_name,
                "stage": stage,
                "description": description,
                "timestamp": (datetime.now() + timedelta(days=stage)).isoformat()
            }
        )
        
        # Link agent to state
        atomspace.add_link(
            link_type="TemporalLink",
            outgoing=[evolving_agent.id, state_node.id],
            truth_value=(0.8 if stage == 1 else 0.3, 0.9),  # Current state stronger
            metadata={"temporal_order": stage}
        )
        
        # Link consecutive states
        if prev_state_node:
            atomspace.add_link(
                link_type="SequenceLink",
                outgoing=[prev_state_node.id, state_node.id],
                truth_value=(1.0, 1.0),
                metadata={"transition": f"{prev_state_node.metadata['state']}_to_{state_name}"}
            )
        
        prev_state_node = state_node
        print_atom(state_node, indent=1)
    
    # =========================================================================
    # 5. AGENT COLLABORATION PATTERNS
    # =========================================================================
    print_section("5. Agent Collaboration Patterns")
    print("\nComplex collaboration structures:\n")
    
    # Create project team
    project_team = atomspace.add_node(
        node_type="TeamNode",
        name="Project_Quantum_Team",
        truth_value=(1.0, 1.0),
        attention_value=0.85,
        metadata={
            "project": "Quantum",
            "team_type": "cross_functional",
            "formation_date": datetime.now().isoformat()
        }
    )
    print_atom(project_team)
    
    # Add specialized agents to team
    print("\nTeam composition:\n")
    for agent in specialized_agents[:3]:  # First 3 specialized agents
        atomspace.add_link(
            link_type="MemberLink",
            outgoing=[agent.id, project_team.id],
            truth_value=(1.0, 1.0),
            metadata={"role_in_team": agent.metadata["role"]}
        )
        print(f"  ✓ {agent.name} joined team")
    
    # Create collaboration channels
    print("\nCollaboration channels:\n")
    channels = ["Planning", "Execution", "Review"]
    for channel in channels:
        channel_node = atomspace.add_node(
            node_type="CommunicationChannelNode",
            name=f"{channel}_Channel",
            truth_value=(1.0, 1.0),
            attention_value=0.6,
            metadata={
                "purpose": channel.lower(),
                "participants": [a.name for a in specialized_agents[:3]]
            }
        )
        
        # Link team to channel
        atomspace.add_link(
            link_type="UsesChannelLink",
            outgoing=[project_team.id, channel_node.id],
            truth_value=(1.0, 1.0)
        )
        print_atom(channel_node, indent=1)
    
    # =========================================================================
    # 6. AGENT KNOWLEDGE DOMAINS
    # =========================================================================
    print_section("6. Agent Knowledge Domains")
    print("\nMapping agents to knowledge domains:\n")
    
    # Create knowledge domains
    domains = [
        ("MachineLearning", ["neural_networks", "optimization", "training"]),
        ("WebDevelopment", ["html", "css", "javascript", "frameworks"]),
        ("DataScience", ["statistics", "visualization", "analysis"]),
        ("CloudInfrastructure", ["kubernetes", "docker", "aws"])
    ]
    
    domain_nodes = []
    for domain_name, topics in domains:
        domain_node = atomspace.add_node(
            node_type="KnowledgeDomainNode",
            name=f"Domain_{domain_name}",
            truth_value=(1.0, 1.0),
            attention_value=0.5,
            metadata={
                "domain": domain_name,
                "topics": topics,
                "complexity": "high"
            }
        )
        domain_nodes.append(domain_node)
        print_atom(domain_node, indent=1)
        
        # Create topic nodes
        for topic in topics:
            topic_node = atomspace.add_node(
                node_type="TopicNode",
                name=f"Topic_{topic}",
                truth_value=(1.0, 1.0),
                attention_value=0.3
            )
            atomspace.add_link(
                link_type="ContainmentLink",
                outgoing=[domain_node.id, topic_node.id],
                truth_value=(1.0, 1.0)
            )
    
    # Assign domains to specialized agents
    print("\nAgent expertise mapping:\n")
    for i, agent in enumerate(specialized_agents):
        domain = domain_nodes[i % len(domain_nodes)]
        expertise_level = 0.7 + (i % 3) * 0.1
        
        atomspace.add_link(
            link_type="ExpertiseLink",
            outgoing=[agent.id, domain.id],
            truth_value=(expertise_level, 0.9),
            metadata={"expertise_level": expertise_level}
        )
        print(f"  ✓ {agent.name} → {domain.name} (expertise: {expertise_level:.1%})")
    
    # =========================================================================
    # 7. AGENT PERFORMANCE TRACKING
    # =========================================================================
    print_section("7. Agent Performance and Metrics")
    print("\nTracking agent performance over time:\n")
    
    performance_tracker = atomspace.add_node(
        node_type="PerformanceTrackerNode",
        name="System_Performance_Tracker",
        truth_value=(1.0, 1.0),
        attention_value=0.7,
        metadata={
            "tracks": "all_agent_performance",
            "metrics": ["success_rate", "response_time", "quality_score"]
        }
    )
    print_atom(performance_tracker)
    
    print("\nIndividual agent metrics:\n")
    for agent in [root_agent] + dept_agents:
        metric_node = atomspace.add_node(
            node_type="MetricNode",
            name=f"Metrics_{agent.name}",
            truth_value=(1.0, 1.0),
            attention_value=0.4,
            metadata={
                "agent": agent.name,
                "success_rate": 0.85 + (hash(agent.name) % 15) / 100,
                "tasks_completed": 100 + (hash(agent.name) % 50),
                "average_response_time": 1.5 + (hash(agent.name) % 10) / 10,
                "quality_score": 0.88 + (hash(agent.name) % 12) / 100
            }
        )
        
        atomspace.add_link(
            link_type="HasMetricsLink",
            outgoing=[agent.id, metric_node.id],
            truth_value=(1.0, 1.0)
        )
        
        print(f"  {agent.name}:")
        print(f"    Success rate: {metric_node.metadata['success_rate']:.1%}")
        print(f"    Tasks: {metric_node.metadata['tasks_completed']}")
    
    # =========================================================================
    # 8. CROSS-AGENT KNOWLEDGE SHARING
    # =========================================================================
    print_section("8. Cross-Agent Knowledge Sharing")
    print("\nKnowledge transfer between agents:\n")
    
    # Create shared knowledge base
    shared_kb = atomspace.add_node(
        node_type="KnowledgeBaseNode",
        name="Shared_Knowledge_Base",
        truth_value=(1.0, 1.0),
        attention_value=0.8,
        metadata={
            "type": "shared",
            "access": "all_agents",
            "contains": "collective_learnings"
        }
    )
    print_atom(shared_kb)
    
    # Create knowledge items
    print("\nShared knowledge items:\n")
    knowledge_items = [
        ("BestPractice_CodeReview", "Code review guidelines", 0.95),
        ("Pattern_ErrorHandling", "Error handling patterns", 0.92),
        ("Strategy_Optimization", "Optimization strategies", 0.88)
    ]
    
    for item_name, description, confidence in knowledge_items:
        item_node = atomspace.add_node(
            node_type="KnowledgeItemNode",
            name=item_name,
            truth_value=(1.0, confidence),
            attention_value=0.6,
            metadata={"description": description}
        )
        
        # Link to shared KB
        atomspace.add_link(
            link_type="ContainmentLink",
            outgoing=[shared_kb.id, item_node.id],
            truth_value=(1.0, 1.0)
        )
        
        # Multiple agents can access
        for agent in specialized_agents[:2]:
            atomspace.add_link(
                link_type="AccessLink",
                outgoing=[agent.id, item_node.id],
                truth_value=(1.0, 0.9),
                metadata={"access_type": "read_write"}
            )
        
        print_atom(item_node, indent=1)
    
    # =========================================================================
    # 9. AGENT EVOLUTION AND ADAPTATION
    # =========================================================================
    print_section("9. Agent Evolution and Adaptation")
    print("\nDemonstrating agent learning and evolution:\n")
    
    # Create evolution tracker
    evolution_tracker = atomspace.add_node(
        node_type="EvolutionTrackerNode",
        name="Agent_Evolution_System",
        truth_value=(1.0, 1.0),
        attention_value=0.75,
        metadata={
            "tracks": "agent_capability_evolution",
            "mechanism": "reinforcement_learning",
            "adaptation_rate": "dynamic"
        }
    )
    print_atom(evolution_tracker)
    
    # Show capability evolution
    print("\nCapability evolution for Learning_Agent_Alpha:\n")
    
    capabilities_timeline = [
        ("Initial", ["basic_reasoning"], 0.6),
        ("After_Training", ["basic_reasoning", "pattern_recognition"], 0.75),
        ("Current", ["basic_reasoning", "pattern_recognition", "advanced_analysis"], 0.88),
        ("Projected", ["basic_reasoning", "pattern_recognition", "advanced_analysis", "creative_synthesis"], 0.95)
    ]
    
    for stage, caps, performance in capabilities_timeline:
        stage_node = atomspace.add_node(
            node_type="EvolutionStageNode",
            name=f"Evolution_{stage}_{evolving_agent.name}",
            truth_value=(performance, 0.9),
            attention_value=0.5 if stage == "Current" else 0.3,
            metadata={
                "stage": stage,
                "capabilities": caps,
                "performance": performance,
                "capability_count": len(caps)
            }
        )
        
        atomspace.add_link(
            link_type="EvolutionLink",
            outgoing=[evolving_agent.id, stage_node.id],
            truth_value=(1.0, 1.0),
            metadata={"evolution_stage": stage}
        )
        
        print(f"  {stage}: {len(caps)} capabilities, {performance:.0%} performance")
    
    # =========================================================================
    # 10. STATISTICS AND SUMMARY
    # =========================================================================
    print_section("10. Complex Agent System Statistics")
    
    stats = atomspace.get_stats()
    
    # Count different agent types
    agent_types = {}
    for atom in atomspace.atoms.values():
        if "Agent" in atom.type or atom.type in ["SwarmCoordinatorNode", "SwarmMemberNode"]:
            agent_types[atom.type] = agent_types.get(atom.type, 0) + 1
    
    print(f"""
AtomSpace: {atomspace.name}

Total Atoms: {stats['total_atoms']}
  - Nodes: {stats['total_nodes']}
  - Links: {stats['total_links']}

Agent Type Distribution:""")
    for agent_type, count in sorted(agent_types.items()):
        print(f"  - {agent_type}: {count}")
    
    print(f"\nGraph Density: {stats['graph_density']:.4f}")
    
    print(f"""
System Complexity Metrics:
  - Hierarchical Levels: 3 (CEO → Dept Heads → Team Leads)
  - Swarm Size: {swarm_size} members
  - Specialized Roles: {len(specialized_agents)}
  - Knowledge Domains: {len(domain_nodes)}
  - Collaboration Teams: 1
  - Communication Channels: {len(channels)}
    """)
    
    print_section("Example Complete")
    print("""
This example demonstrated:

✓ Nested agent hierarchies (3 levels deep)
✓ Agent swarms and collective intelligence
✓ Specialized agent roles and capabilities
✓ Temporal agent states and evolution
✓ Complex collaboration patterns
✓ Knowledge domain mapping
✓ Performance tracking and metrics
✓ Cross-agent knowledge sharing
✓ Agent evolution and adaptation

These complex patterns enable:
- Large-scale multi-agent coordination
- Emergent collective behaviors
- Dynamic role assignment
- Knowledge-based specialization
- Continuous learning and improvement
- Fault-tolerant distributed processing

The cognitive architecture can represent arbitrarily complex
agent organizations and their emergent behaviors!
    """)


if __name__ == "__main__":
    example_complex_agent_atoms()
