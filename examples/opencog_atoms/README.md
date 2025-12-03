# OpenCog Agent Atoms Examples

This directory contains comprehensive examples of different types of agent atoms in the Agent Zero HCK cognitive architecture.

## Overview

The Agent Zero HCK framework uses OpenCog-inspired AtomSpace for knowledge representation. This examples directory demonstrates various atom types, including simple agent concepts and complex self-referential structures.

## Example Categories

### 1. Basic Agent Atoms (`01_basic_agent_atoms.py`)
- **ConceptNode**: Represents agent concepts and entities
- **PredicateNode**: Represents agent capabilities and properties
- **NumberNode**: Represents numeric values and metrics
- **GroundedPredicateNode**: Represents executable procedures

### 2. Multi-Agent Coordination (`02_multiagent_atoms.py`)
- Agent hierarchy atoms
- Communication channel atoms
- Task delegation atoms
- Shared knowledge atoms

### 3. Agent State and Lifecycle (`03_agent_state_atoms.py`)
- Agent lifecycle states (initialized, active, idle, terminated)
- State transitions
- Resource usage tracking
- Performance metrics

### 4. Agent Capabilities and Tools (`04_agent_capabilities.py`)
- Tool availability atoms
- Capability inheritance
- Skill development tracking
- Dynamic capability acquisition

### 5. Self-Referential Atoms (`05_self_referential_atoms.py`)
- **AtomSpaceNode**: The AtomSpace representing itself as an atom
- **OpenCogSystemNode**: The entire cognitive system as an atom
- **MetaCognitiveNode**: Atoms reasoning about atoms
- **ReflectiveNode**: Self-aware structures

### 6. Complex Agent Atoms (`06_complex_agent_atoms.py`)
- Nested agent structures
- Recursive knowledge representation
- Evolutionary atom patterns
- Temporal reasoning atoms

## Running the Examples

Each example file is standalone and can be executed directly:

```bash
cd /home/runner/work/agent-zero-hck/agent-zero-hck
python3 examples/opencog_atoms/01_basic_agent_atoms.py
```

Or run all examples:

```bash
python3 examples/opencog_atoms/run_all_examples.py
```

## Key Concepts

### Atom Types

#### Nodes
Nodes represent concepts, entities, or values:
- `ConceptNode`: Abstract concepts (e.g., "Agent_0", "Task", "Goal")
- `PredicateNode`: Properties or capabilities (e.g., "CanReason", "HasTool")
- `NumberNode`: Numeric values (e.g., iteration counts, metrics)
- `VariableNode`: Pattern matching variables
- `GroundedPredicateNode`: Executable code references

#### Links
Links represent relationships between atoms:
- `InheritanceLink`: "is-a" relationships (e.g., Agent_0 is-a CognitiveAgent)
- `EvaluationLink`: Property evaluations (e.g., Agent_0 has capability X)
- `ExecutionLink`: Action invocations
- `StateLink`: State assignments
- `SimilarityLink`: Similarity relationships
- `MemberLink`: Set membership

### Truth Values
Each atom has a truth value `(strength, confidence)`:
- **Strength**: Probability that the statement is true (0.0 to 1.0)
- **Confidence**: Certainty in the strength value (0.0 to 1.0)

Example: `(0.9, 0.85)` means "90% likely to be true with 85% confidence"

### Attention Values
Attention values (0.0 to 1.0) represent cognitive focus:
- High attention: Currently important or being actively processed
- Low attention: Background knowledge
- Attention spreading: Focus propagates through connected atoms

## Self-Referential Examples Explained

### AtomSpaceNode
The AtomSpace can represent itself as an atom within its own structure:

```python
atomspace_node = atomspace.add_node(
    node_type="AtomSpaceNode",
    name="self_atomspace",
    metadata={
        "represents": "this_atomspace",
        "total_atoms": lambda: len(atomspace.atoms)
    }
)
```

This creates a meta-level representation where:
- The AtomSpace is both the container and a contained element
- Enables self-reflection and introspection
- Allows the system to reason about its own structure

### OpenCogSystemNode
The entire cognitive system represented as a single atom:

```python
system_node = atomspace.add_node(
    node_type="OpenCogSystemNode",
    name="cog_zero_system",
    metadata={
        "version": "1.0",
        "agents": ["agent_0", "agent_1"],
        "atomspaces": ["space_agent_0", "space_agent_1"]
    }
)
```

This enables:
- System-level reasoning and optimization
- Cross-atomspace coordination
- Emergent system behaviors
- Self-awareness at the system level

### MetaCognitiveNode
Atoms that reason about other atoms:

```python
meta_node = atomspace.add_node(
    node_type="MetaCognitiveNode",
    name="atom_reasoner",
    metadata={
        "observes": "all_atoms",
        "purpose": "pattern_detection"
    }
)
```

Creates recursive reasoning capability:
- Atoms can analyze patterns in other atoms
- Enables meta-learning and self-improvement
- Supports adaptive cognitive architectures

## Integration with Agent Zero

These atoms integrate seamlessly with Agent Zero's multi-agent framework:

1. **Agent Initialization**: Each agent gets a ConceptNode
2. **Task Processing**: Tasks become ConceptNodes with ExecutionLinks
3. **Tool Usage**: Tools are PredicateNodes with capability links
4. **Knowledge Sharing**: Agents export/import AtomSpaces
5. **Attention Management**: Important concepts get higher attention

## Advanced Topics

### Temporal Dynamics
Atoms evolve over time:
- Truth values strengthen with confirmation
- Attention decays without use
- New connections form through learning

### Pattern Mining
Pattern matching enables:
- Finding similar concepts
- Discovering relationships
- Identifying knowledge gaps
- Emergent pattern recognition

### Evolutionary Adaptation
The cognitive structure adapts:
- Successful patterns strengthen
- Failed attempts weaken
- New structures emerge organically
- Graph topology optimizes for tasks

## Further Reading

- [OpenCog Integration Guide](../../docs/opencog_integration.md)
- [AtomSpace Implementation](../../python/helpers/opencog_atomspace.py)
- [OpenCog Tool](../../python/tools/opencog.py)
- [Demo Instrument](../../instruments/default/opencog_demo/demo.sh)

## Contributing

To add new examples:
1. Create a new Python file with a descriptive name
2. Include comprehensive comments explaining the atom types
3. Demonstrate both creation and usage
4. Add to `run_all_examples.py`
5. Update this README with the new example

## License

MIT License - See [LICENSE](../../LICENSE)
