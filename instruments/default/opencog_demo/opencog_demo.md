# OpenCog Cognitive Architecture Demo

This instrument demonstrates the OpenCog cognitive architecture capabilities integrated into Agent Zero.

## Purpose

Showcase how to use the OpenCog AtomSpace for:
- Multi-agent knowledge representation
- Cognitive state management
- Pattern-based reasoning
- Attention allocation mechanisms
- Adaptive evolution tracking

## Usage

Call this instrument to run a demonstration of OpenCog features:

```json
{
  "tool_name": "code_execution_tool",
  "tool_args": {
    "code": "bash /a0/instruments/default/opencog_demo/demo.sh",
    "runtime": "terminal"
  }
}
```

## Features Demonstrated

1. **AtomSpace Creation**: Creating nodes and links for knowledge representation
2. **Multi-Agent Orchestration**: Managing multiple agents with shared knowledge
3. **Pattern Matching**: Finding related concepts using patterns
4. **Attention Spreading**: Cognitive attention allocation mechanism
5. **Knowledge Export/Import**: Serializing and sharing cognitive state

## Example Output

The script will:
- Create agent concept nodes
- Link agents with their capabilities
- Demonstrate pattern matching
- Show attention spreading
- Export the cognitive state
- Display statistics about the AtomSpace
