# Cog-Zero: OpenCog Multi-Agent Orchestration

This fork implements OpenCog-inspired cognitive architecture for Agent Zero, creating **cog-zero**: an autonomous multi-agent orchestration workbench embedded in living dynamical systems.

## What's New

### OpenCog Integration
- **AtomSpace**: Hypergraph-based knowledge representation
- **Cognitive Orchestration**: Multi-agent cognitive state management
- **Pattern Matching**: Advanced query and reasoning capabilities
- **Attention Allocation**: Cognitive resource management
- **Adaptive Evolution**: Dynamic knowledge structure evolution

## Quick Start

### Installation

1. Install additional dependencies:
```bash
pip install networkx==3.2.1 hyperon==0.2.8
```

2. Follow the standard Agent Zero installation from the [main README](./README.md)

### Using OpenCog Features

Agents can now use the `opencog` tool for cognitive operations:

```json
{
  "tool_name": "opencog:add_node",
  "tool_args": {
    "node_type": "ConceptNode",
    "name": "MyAgent",
    "truth_value": [0.95, 0.9],
    "metadata": {"role": "reasoning"}
  }
}
```

### Demo

Run the OpenCog demo to see all features:

```json
{
  "tool_name": "code_execution_tool",
  "tool_args": {
    "code": "bash /a0/instruments/default/opencog_demo/demo.sh",
    "runtime": "terminal"
  }
}
```

## Documentation

- [OpenCog Integration Guide](./docs/opencog_integration.md) - Complete documentation
- [Architecture Overview](./docs/architecture.md) - System design
- [Usage Guide](./docs/usage.md) - How to use Agent Zero

## Key Features

### 1. Cognitive Knowledge Representation
- **Nodes**: Represent concepts, predicates, and values
- **Links**: Represent relationships between atoms
- **Truth Values**: Probabilistic certainty (strength, confidence)
- **Attention Values**: Resource allocation mechanism

### 2. Multi-Agent Orchestration
- Each agent maintains its own AtomSpace
- Agents can share knowledge through export/import
- Cognitive states track agent evolution
- Automatic interaction monitoring

### 3. Adaptive Evolution
- Knowledge structures grow organically
- Truth values evolve with experience
- Attention spreads through the knowledge graph
- Graph topology adapts to usage patterns

### 4. Living Dynamical Systems
- Temporal dynamics with attention decay
- Spreading activation for associative reasoning
- Self-organizing knowledge structures
- Closed-loop cognitive feedback

## Example Use Cases

### Multi-Agent Collaboration
```python
# Agent 0 creates knowledge
{
  "tool_name": "opencog:add_node",
  "tool_args": {"name": "SharedKnowledge"}
}

# Export to share with Agent 1
{
  "tool_name": "opencog:export",
  "tool_args": {}
}
```

### Pattern-Based Reasoning
```python
# Find all agents matching a pattern
{
  "tool_name": "opencog:pattern_match",
  "tool_args": {
    "pattern": {"type": "ConceptNode", "name": "Agent_*"}
  }
}
```

### Attention Management
```python
# Focus on important concepts
{
  "tool_name": "opencog:spread_activation",
  "tool_args": {
    "source": "ImportantTask",
    "intensity": 0.3,
    "decay": 0.6
  }
}
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Cognitive Orchestrator           │
│  (Manages Multiple AtomSpaces)          │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   ┌────▼────┐      ┌────▼────┐
   │AtomSpace│      │AtomSpace│
   │ Agent 0 │      │ Agent 1 │
   └─────────┘      └─────────┘
        │                 │
   ┌────▼────────────────▼────┐
   │    Knowledge Graph        │
   │  (Nodes + Links)          │
   │  • Truth Values           │
   │  • Attention Values       │
   │  • Pattern Matching       │
   └───────────────────────────┘
```

## Technical Implementation

### Core Modules
- `python/helpers/opencog_atomspace.py` - AtomSpace implementation
- `python/tools/opencog.py` - OpenCog tool for agents
- `python/extensions/message_loop_start/10_opencog_integration.py` - Auto-integration
- `prompts/default/agent.system.tool.opencog.md` - Tool documentation

### Dependencies
- `networkx>=3.2.1` - Graph operations for hypergraph structure
- `hyperon>=0.2.8` - Reserved for future symbolic reasoning extensions

## Contributing

This is a fork of [Agent Zero](https://github.com/frdel/agent-zero) with OpenCog integration. 

For the base framework:
- See the main [Contributing Guide](./docs/contribution.md)

For OpenCog features:
- Submit issues or PRs related to cognitive architecture
- Share use cases and patterns
- Help improve documentation

## License

Same as Agent Zero - see [LICENSE](./LICENSE)

## Acknowledgments

- **Agent Zero**: Original framework by [frdel](https://github.com/frdel)
- **OpenCog**: Cognitive architecture inspiration
- **cogpy**: This implementation fork

---

**Ready to build cognitive multi-agent systems?** Start with the [OpenCog Integration Guide](./docs/opencog_integration.md)!
