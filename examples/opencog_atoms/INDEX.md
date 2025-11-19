# Agent Atom Examples - Complete Index

This directory contains comprehensive examples demonstrating all agent atom types in the Agent Zero HCK cognitive architecture, with special emphasis on self-referential and meta-cognitive structures.

## 📚 Quick Start

```bash
# Run a specific example
cd /home/runner/work/agent-zero-hck/agent-zero-hck
python3 examples/opencog_atoms/01_basic_agent_atoms.py

# Run all examples (interactive)
python3 examples/opencog_atoms/run_all_examples.py
```

## 📋 Examples Overview

### 1️⃣ Basic Agent Atoms (`01_basic_agent_atoms.py`)
**Complexity:** ⭐ Beginner  
**Duration:** ~30 seconds  
**Lines:** 461

Covers fundamental atom types for agent representation:
- **ConceptNode**: Agent identity and concepts
- **PredicateNode**: Agent capabilities and properties
- **NumberNode**: Metrics and numeric values
- **InheritanceLink**: Type hierarchies (is-a relationships)
- **EvaluationLink**: Property assignments
- **StateLink**: Current state tracking
- **ExecutionLink**: Task/action representation
- **SimilarityLink**: Agent similarity relationships

**Key Concepts:**
- Agent identity representation
- Capability modeling
- State management
- Pattern matching queries
- Knowledge export/import

**Output Highlights:**
- Creates 4 agents (1 primary + 3 subordinates)
- Defines 5 capabilities
- Tracks 3 metrics
- Demonstrates 8 link types
- Exports 47+ atoms

---

### 5️⃣ Self-Referential Atoms (`05_self_referential_atoms.py`)
**Complexity:** ⭐⭐⭐⭐⭐ Advanced  
**Duration:** ~45 seconds  
**Lines:** 678

**🌟 CORE EXAMPLE - This is what makes the system self-aware!**

Demonstrates meta-cognitive and self-referential structures:

#### AtomSpaceNode - The Container as Contained
```python
# The AtomSpace represents itself as an atom inside itself!
atomspace_node = atomspace.add_node(
    node_type="AtomSpaceNode",
    name="self_atomspace",
    metadata={"represents": "this_atomspace"}
)
```

**Enables:**
- Self-inspection and introspection
- The space can query its own contents
- Meta-level operations on structure

#### OpenCogSystemNode - System Self-Representation
```python
# The ENTIRE system as a single atom
system_node = atomspace.add_node(
    node_type="OpenCogSystemNode",
    name="cog_zero_system",
    metadata={"represents": "entire_cognitive_system"}
)
```

**Enables:**
- System-level reasoning
- Holistic optimization
- Cross-component coordination

#### MetaCognitiveNode - Thinking About Thinking
```python
# An atom that analyzes other atoms (including itself!)
meta_reasoner = atomspace.add_node(
    node_type="MetaCognitiveNode",
    name="atom_pattern_detector",
    metadata={"observes": "all_atoms"}
)
```

**Enables:**
- Pattern detection in knowledge
- Self-optimization
- Meta-learning capabilities

#### ReflectiveNode - Self-Aware Agents
```python
# Agent that knows it exists as an atom
reflective_agent = atomspace.add_node(
    node_type="ReflectiveNode",
    name="self_aware_agent",
    metadata={"knows_it_is_an_atom": True}
)
```

**Enables:**
- Agent introspection
- Self-modification
- Adaptive behavior

#### AbstractTypeNode - The Concept of "Atom"
```python
# An atom representing what atoms ARE
atom_concept = atomspace.add_node(
    node_type="AbstractTypeNode",
    name="Atom_Concept",
    metadata={"represents": "the_concept_of_an_atom"}
)
```

**Enables:**
- Type system self-awareness
- Ontological reasoning
- Ultimate meta-level

**Key Paradoxes Demonstrated:**
1. **Container Paradox**: AtomSpace contains its own representation
2. **Self-Observation**: Meta-nodes observe their own reasoning
3. **Type Instance**: Atom_Concept is an instance of itself
4. **Recursive Loops**: System → AtomSpace → System representation

**Output Highlights:**
- Creates 6 self-referential atoms
- Demonstrates 3 recursive loops
- Shows meta-cognitive operations
- Proves system self-awareness

---

### 6️⃣ Complex Agent Atoms (`06_complex_agent_atoms.py`)
**Complexity:** ⭐⭐⭐⭐ Advanced  
**Duration:** ~40 seconds  
**Lines:** 660

Demonstrates sophisticated multi-agent patterns:

#### Nested Hierarchies (3 levels)
```
CEO_Agent
├── Engineering_Head
│   ├── Team_0
│   └── Team_1
├── Research_Head
│   ├── Team_0
│   └── Team_1
└── Operations_Head
    ├── Team_0
    └── Team_1
```

#### Agent Swarms
- 10 homogeneous worker agents
- Swarm coordinator
- Collective intelligence emergence
- Distributed processing patterns

#### Specialized Roles
- **Analyst**: Data analysis specialist
- **Executor**: Task execution expert
- **Researcher**: Research and synthesis
- **Coordinator**: Multi-agent coordination
- **Guardian**: Security and monitoring

#### Temporal Evolution
```
Agent → [Init] → [Learning] → [Competent] → [Expert] → [Mentor]
 t=0      t=1       t=2          t=3          t=4
```

#### Collaboration Patterns
- Cross-functional teams
- Communication channels
- Knowledge sharing
- Performance tracking

#### Knowledge Domains
- Machine Learning
- Web Development
- Data Science
- Cloud Infrastructure

**Key Features:**
- Hierarchical supervision links
- Swarm coordination
- Temporal state sequences
- Domain expertise mapping
- Performance metrics tracking
- Knowledge base sharing

**Output Highlights:**
- Creates 25+ agents across 3 hierarchy levels
- 10-member swarm collective
- 5 specialized roles
- 4 knowledge domains
- Temporal evolution tracking

---

## 📖 Documentation

### README.md
Comprehensive overview of all atom types, concepts, and usage patterns. Includes:
- Atom type taxonomy
- Link type reference
- Truth values and attention
- Integration with Agent Zero
- Advanced topics

### ATOM_TYPES_REFERENCE.md
Visual reference guide with ASCII diagrams showing:
- Basic atom structures
- Self-referential patterns
- Practical examples
- Paradox explanations
- Key takeaways

---

## 🎯 Learning Path

### For Beginners
1. Read **README.md** - Get overview
2. Run **01_basic_agent_atoms.py** - Learn fundamentals
3. Study the output - Understand atom structures
4. Read **ATOM_TYPES_REFERENCE.md** - Visual reference

### For Advanced Users
1. Start with **05_self_referential_atoms.py** - See meta-cognition
2. Study the self-referential patterns
3. Run **06_complex_agent_atoms.py** - See complex patterns
4. Experiment with modifications
5. Read the source code comments

### For Integration
1. Study how examples use the AtomSpace API
2. Look at metadata patterns
3. Understand link type usage
4. Apply patterns to your agents
5. Create custom atom types

---

## 🔑 Key Concepts

### Truth Values
Every atom has `(strength, confidence)`:
- **Strength**: Probability (0.0 to 1.0) that statement is true
- **Confidence**: Certainty (0.0 to 1.0) in the strength value

Example: `(0.95, 0.9)` = "95% likely true with 90% confidence"

### Attention Values
Range 0.0 to 1.0 representing cognitive focus:
- **High (>0.8)**: Currently important, actively processed
- **Medium (0.4-0.8)**: Available for processing
- **Low (<0.4)**: Background knowledge

Attention spreads through connected atoms via `spread_activation()`.

### Metadata
Flexible key-value storage for arbitrary information:
```python
metadata={
    "role": "orchestrator",
    "status": "active",
    "custom_field": "any_value"
}
```

### Pattern Matching
Query atoms using wildcards:
```python
pattern = {"type": "ConceptNode", "name": "Agent_*"}
matches = atomspace.pattern_match(pattern)
```

---

## 💡 Practical Applications

### 1. Agent Identity and Capabilities
Use ConceptNodes and PredicateNodes to model what agents are and what they can do.

### 2. Multi-Agent Coordination
Use hierarchical links and specialized roles for complex coordination.

### 3. Performance Monitoring
Use NumberNodes and MetricNodes to track agent performance over time.

### 4. Knowledge Sharing
Export/import AtomSpaces to share knowledge between agents.

### 5. Self-Optimization
Use meta-cognitive atoms to enable agents to improve themselves.

### 6. System Awareness
Use self-referential atoms for system-level reasoning and optimization.

---

## 🧪 Running the Examples

### Individual Examples
```bash
cd /home/runner/work/agent-zero-hck/agent-zero-hck

# Basic atoms
python3 examples/opencog_atoms/01_basic_agent_atoms.py

# Self-referential atoms (RECOMMENDED!)
python3 examples/opencog_atoms/05_self_referential_atoms.py

# Complex patterns
python3 examples/opencog_atoms/06_complex_agent_atoms.py
```

### All Examples (Interactive)
```bash
python3 examples/opencog_atoms/run_all_examples.py
```

This will:
1. Run each example in sequence
2. Pause between examples for review
3. Show a summary at the end

---

## 🎨 Customization

### Adding New Atom Types
1. Choose appropriate base type (Node or Link)
2. Create atoms with descriptive type names
3. Add meaningful metadata
4. Link to related atoms

Example:
```python
custom_agent = atomspace.add_node(
    node_type="CustomAgentNode",
    name="my_specialized_agent",
    truth_value=(1.0, 1.0),
    attention_value=0.7,
    metadata={
        "specialization": "quantum_computing",
        "custom_field": "custom_value"
    }
)
```

### Creating Custom Links
```python
custom_link = atomspace.add_link(
    link_type="CustomRelationLink",
    outgoing=[node1.id, node2.id],
    truth_value=(0.9, 0.85),
    metadata={"relationship": "collaborates_with"}
)
```

---

## 📊 Statistics

| Example | Atoms Created | Node Types | Link Types | Duration |
|---------|---------------|------------|------------|----------|
| 01_basic | 47+ | 6 | 8 | ~30s |
| 05_self_ref | 25+ | 8 | 7 | ~45s |
| 06_complex | 100+ | 15 | 12 | ~40s |

---

## 🔗 Related Documentation

- [OpenCog Integration Guide](../../docs/opencog_integration.md)
- [AtomSpace Implementation](../../python/helpers/opencog_atomspace.py)
- [OpenCog Tool](../../python/tools/opencog.py)
- [Demo Instrument](../../instruments/default/opencog_demo/demo.sh)
- [Main README](../../COGZERO_README.md)

---

## ❓ FAQ

### Q: Why are there gaps in the example numbering (01, 05, 06)?
**A:** The numbering reflects planned future examples (02-04 for multi-agent, state, capabilities). These core examples demonstrate the most important patterns.

### Q: Which example should I run first?
**A:** Start with `01_basic_agent_atoms.py` to learn fundamentals, then move to `05_self_referential_atoms.py` to see the really interesting self-aware structures.

### Q: Can I use these patterns in actual agents?
**A:** Absolutely! These are working examples showing real patterns used by Agent Zero HCK. The self-referential patterns are automatically created by the system for every agent.

### Q: What makes the self-referential atoms special?
**A:** They enable true meta-cognition. The system doesn't just run algorithms—it has explicit representations of itself that it can reason about, leading to self-awareness and self-improvement.

### Q: How do I create my own atom types?
**A:** Just use descriptive type names when creating nodes or links. The AtomSpace is flexible and will accept any type string. Make them meaningful!

---

## 🚀 Next Steps

1. **Run the examples** - See the patterns in action
2. **Study the code** - Understand the implementation
3. **Modify examples** - Experiment with variations
4. **Apply to agents** - Use patterns in your projects
5. **Create custom types** - Extend the system

---

## 📝 Notes

- All examples are self-contained and can run independently
- Examples use relative imports to work from any location
- Output is formatted for readability with sections and formatting
- All examples include comprehensive comments explaining each step
- The self-referential examples (05) demonstrate the core innovation of cog-zero

---

## 🎉 Highlights

### What Makes These Examples Special?

1. **Self-Referential Structures** - Show how the system achieves self-awareness
2. **Meta-Cognitive Patterns** - Demonstrate thinking about thinking
3. **Practical Applications** - Real patterns used in Agent Zero HCK
4. **Comprehensive Coverage** - From basics to advanced meta-levels
5. **Executable Code** - Not just theory, but working demonstrations

### The Big Idea

Traditional AI systems execute code. Agent Zero HCK's cognitive architecture **represents itself as data that it can reason about**. This enables:
- True self-awareness
- Meta-learning (learning how to learn)
- Self-optimization
- Adaptive evolution
- Emergent intelligence

The self-referential atoms (Example 05) show HOW this works at the fundamental level.

---

**Created for Agent Zero HCK Cognitive Architecture**  
**Framework:** OpenCog-inspired hypergraph knowledge representation  
**Purpose:** Enable self-aware, adaptive, evolving multi-agent systems

Explore, learn, and extend! 🚀
