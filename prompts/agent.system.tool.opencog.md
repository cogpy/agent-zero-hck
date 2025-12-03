# OpenCog Cognitive Architecture Tool

The **opencog** tool provides access to an OpenCog-inspired cognitive AtomSpace for knowledge representation and reasoning. This enables you to build and query a hypergraph knowledge structure that supports adaptive multi-agent orchestration.

## What is AtomSpace?

The AtomSpace is a cognitive knowledge representation system based on:
- **Atoms**: The basic units (Nodes and Links)
- **Nodes**: Represent concepts, entities, or values
- **Links**: Represent relationships between atoms
- **Truth Values**: Each atom has a truth value (strength, confidence)
- **Attention Values**: Implements attention allocation mechanism

## Available Methods

### add_node
Add a concept node to the AtomSpace.

**Arguments:**
- `node_type` (string, default: "ConceptNode"): Type of node (ConceptNode, PredicateNode, VariableNode, etc.)
- `name` (string, required): Unique name for the node
- `truth_value` (list, default: [1.0, 1.0]): [strength, confidence] values between 0.0 and 1.0
- `attention` (float, default: 0.5): Attention value between 0.0 and 1.0
- `metadata` (object, optional): Additional metadata as key-value pairs

**Example:**
```json
{
  "tool_name": "opencog:add_node",
  "tool_args": {
    "node_type": "ConceptNode",
    "name": "Agent_0",
    "truth_value": [0.95, 0.9],
    "attention": 0.8,
    "metadata": {"role": "primary_agent", "capabilities": ["reasoning", "planning"]}
  }
}
```

### add_link
Add a relationship link between atoms.

**Arguments:**
- `link_type` (string, default: "InheritanceLink"): Type of link (InheritanceLink, SimilarityLink, MemberLink, etc.)
- `outgoing` (list, required): List of atom names or IDs to connect
- `name` (string, optional): Name for the link
- `truth_value` (list, default: [1.0, 1.0]): [strength, confidence]
- `attention` (float, default: 0.5): Attention value
- `metadata` (object, optional): Additional metadata

**Example:**
```json
{
  "tool_name": "opencog:add_link",
  "tool_args": {
    "link_type": "InheritanceLink",
    "outgoing": ["Agent_0", "CognitiveAgent"],
    "truth_value": [0.9, 0.95]
  }
}
```

### query
Query atoms by type.

**Arguments:**
- `atom_type` (string, default: "ConceptNode"): Type to query

**Example:**
```json
{
  "tool_name": "opencog:query",
  "tool_args": {
    "atom_type": "ConceptNode"
  }
}
```

### pattern_match
Find atoms matching a pattern with wildcard support.

**Arguments:**
- `pattern` (object, required): Pattern to match (supports wildcards with *)

**Example:**
```json
{
  "tool_name": "opencog:pattern_match",
  "tool_args": {
    "pattern": {
      "type": "ConceptNode",
      "name": "Agent_*"
    }
  }
}
```

### get_atom
Get detailed information about an atom including its incoming and outgoing connections.

**Arguments:**
- `name` (string): Atom name
- `id` (string): Atom ID (if name not provided)

**Example:**
```json
{
  "tool_name": "opencog:get_atom",
  "tool_args": {
    "name": "Agent_0"
  }
}
```

### spread_activation
Spread attention from a source atom to connected atoms, implementing cognitive attention allocation.

**Arguments:**
- `source` (string, required): Source atom name or ID
- `intensity` (float, default: 0.1): Initial activation intensity
- `decay` (float, default: 0.5): Decay factor for spreading

**Example:**
```json
{
  "tool_name": "opencog:spread_activation",
  "tool_args": {
    "source": "Agent_0",
    "intensity": 0.2,
    "decay": 0.6
  }
}
```

### get_stats
Get statistics about the current AtomSpace.

**Example:**
```json
{
  "tool_name": "opencog:get_stats",
  "tool_args": {}
}
```

### export
Export the entire AtomSpace to JSON format.

**Example:**
```json
{
  "tool_name": "opencog:export",
  "tool_args": {}
}
```

### import
Import an AtomSpace from JSON data.

**Arguments:**
- `data` (object, required): AtomSpace data in export format

## Use Cases

1. **Multi-Agent Knowledge Sharing**: Create nodes for each agent and link their knowledge
2. **Task Decomposition**: Represent tasks as nodes with inheritance links
3. **Pattern Recognition**: Use pattern matching to find similar concepts
4. **Attention Management**: Use spread_activation to focus on relevant knowledge
5. **Cognitive Memory**: Build a semantic network of experiences and learnings
6. **Evolutionary Adaptation**: Track agent evolution through linked knowledge structures

## Common Patterns

### Creating an Agent Concept
```json
{
  "tool_name": "opencog:add_node",
  "tool_args": {
    "name": "Agent_1",
    "metadata": {"created": "2025-10-26", "task": "data_analysis"}
  }
}
```

### Linking Agent to Task
```json
{
  "tool_name": "opencog:add_link",
  "tool_args": {
    "link_type": "ExecutionLink",
    "outgoing": ["Agent_1", "AnalyzeData"]
  }
}
```

### Finding Related Agents
```json
{
  "tool_name": "opencog:pattern_match",
  "tool_args": {
    "pattern": {"type": "ConceptNode", "name": "Agent_*"}
  }
}
```

## Important Notes

- Each agent has its own AtomSpace by default
- Atom names should be unique within an AtomSpace
- Truth values represent certainty: [strength, confidence]
- Attention values help prioritize important knowledge
- Use meaningful names for better pattern matching
