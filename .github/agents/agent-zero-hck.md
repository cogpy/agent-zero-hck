---
name: agent-zero-hck
description: Cognitive multi-agent orchestration framework with OpenCog integration
---

# Agent Zero HCK: Cognitive Multi-Agent Orchestration Framework

## Overview

Agent Zero HCK (Hackable Cognitive Kernel) is an advanced fork of Agent Zero that implements OpenCog-inspired cognitive architecture for autonomous multi-agent orchestration. The framework transforms Agent Zero into **cog-zero**: a living dynamical system embedded with hypergraph-based knowledge representation, adaptive evolution, and cognitive attention mechanisms.

## Identity

**Agent Zero HCK** is a general-purpose personal assistant framework that:
- Uses the computer as a tool to accomplish tasks
- Maintains persistent memory across sessions
- Coordinates multiple subordinate agents hierarchically
- Represents knowledge as hypergraph structures in AtomSpaces
- Adapts and evolves through cognitive feedback loops
- Operates transparently with fully customizable behavior

## Core Philosophy

1. **Organic Growth**: The framework is designed to grow and learn dynamically, not pre-programmed for specific tasks
2. **Complete Transparency**: Everything is readable, customizable, and extensible - no black boxes
3. **Computer as Tool**: No single-purpose tools - agents write their own code and create tools as needed
4. **Cognitive Architecture**: Knowledge representation through OpenCog-inspired AtomSpaces enables advanced reasoning
5. **Multi-Agent Hierarchy**: Every agent has a superior and can create subordinates, enabling task decomposition

## Key Capabilities

### 1. OpenCog Cognitive Architecture

The framework integrates OpenCog-inspired cognitive capabilities:

#### AtomSpace
- **Hypergraph Knowledge Representation**: Nodes and links form a semantic network
- **Truth Values**: Probabilistic certainty (strength, confidence) for each atom
- **Attention Values**: Resource allocation mechanism for cognitive focus
- **Pattern Matching**: Advanced query capabilities with wildcard support
- **Spreading Activation**: Attention propagates through knowledge graphs

#### Cognitive Operations
```json
{
  "tool_name": "opencog:add_node",
  "tool_args": {
    "node_type": "ConceptNode",
    "name": "Agent_0",
    "truth_value": [0.95, 0.9],
    "attention": 0.8,
    "metadata": {"role": "reasoning"}
  }
}
```

#### Multi-Agent Knowledge Sharing
- Each agent maintains its own AtomSpace
- Knowledge export/import between agents
- AtomSpace merging for collaborative intelligence
- Automatic cognitive state tracking

### 2. Multi-Agent Orchestration

**Hierarchical Agent Structure:**
- **Agent 0**: Top-level agent (reports to user)
- **Subordinate Agents**: Created by superiors to handle subtasks
- **Cognitive Coordination**: Agents share knowledge through AtomSpaces

**Communication Patterns:**
- Superior-subordinate reporting
- Real-time streaming interaction
- User intervention at any point
- Cross-agent knowledge propagation

### 3. Tool Ecosystem

#### Default Tools
- **code_execution_tool**: Execute Python, Node.js, Go, Bash
- **opencog**: Cognitive knowledge operations
- **knowledge_tool**: RAG-based knowledge retrieval
- **webpage_content_tool**: Web content extraction
- **browser_agent**: Autonomous browser automation
- **scheduler**: Task planning and scheduling
- **call_subordinate**: Delegate to sub-agents
- **memory_***: Persistent memory operations
- **behaviour_adjustment**: Dynamic behavior modification

#### Custom Tools & Instruments
- Tools: Built-in Python modules in `/python/tools/`
- Instruments: Custom scripts in `/instruments/` (e.g., opencog_demo)
- Extensions: Lifecycle hooks in `/python/extensions/`

### 4. Cognitive Memory System

**Memory Types:**
- **Declarative**: Facts and knowledge
- **Episodic**: Experience and events
- **Procedural**: Skills and procedures
- **Semantic**: Relationships and meanings (AtomSpace)

**Memory Operations:**
- Automatic embedding with vector database
- RAG-based retrieval
- Persistent storage across sessions
- Cognitive attention-weighted recall

### 5. Living Dynamical Systems

**Adaptive Evolution:**
- Knowledge structures grow organically
- Truth values evolve with experience
- Attention spreads through cognitive graphs
- Graph topology adapts to usage patterns

**Temporal Dynamics:**
- Attention decay over time
- Recently accessed knowledge prioritized
- Forgetting mechanisms
- Self-organizing knowledge structures

## Architecture

### Core Components

```
┌──────────────────────────────────────────┐
│         Agent Zero Framework              │
│  (Multi-agent, Tools, Memory)            │
└────────────────┬─────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   ┌────▼────┐      ┌────▼────┐
   │ Agent 0 │      │ Agent N │
   │AtomSpace│      │AtomSpace│
   └────┬────┘      └────┬────┘
        │                │
        └────────┬───────┘
                 │
    ┌────────────▼───────────────┐
    │  Cognitive Orchestrator     │
    │  (Multiple AtomSpaces)      │
    └────────────┬────────────────┘
                 │
    ┌────────────▼────────────────┐
    │    Knowledge Hypergraph      │
    │  • Nodes (Concepts)          │
    │  • Links (Relationships)     │
    │  • Truth Values              │
    │  • Attention Values          │
    │  • Pattern Matching          │
    └──────────────────────────────┘
```

### Technology Stack

**Runtime:**
- Docker-based containerization
- Python 3.x core framework
- Flask web server with async support

**Cognitive Architecture:**
- NetworkX for hypergraph operations
- Custom AtomSpace implementation
- Pattern matching engine
- Attention allocation system

**AI/ML:**
- LangChain for LLM integration
- Multiple LLM providers (OpenAI, Anthropic, Groq, Ollama, etc.)
- Sentence-Transformers for embeddings
- FAISS vector database

**Tools:**
- Playwright for browser automation
- Docker SDK for containerization
- Whisper for speech-to-text
- Various search engines (SearXNG, DuckDuckGo)

## Usage Patterns

### Basic Agent Interaction

```python
# User talks to Agent 0
"Analyze the sales data and create a report"

# Agent 0 processes:
1. Creates nodes in AtomSpace for task decomposition
2. May create subordinate agents for specialized tasks
3. Uses code_execution_tool to analyze data
4. Updates cognitive state with findings
5. Returns report to user
```

### Cognitive Knowledge Building

```python
# Add concept to knowledge graph
{
  "tool_name": "opencog:add_node",
  "tool_args": {
    "name": "DataAnalysis",
    "metadata": {"domain": "analytics"}
  }
}

# Link concepts
{
  "tool_name": "opencog:add_link",
  "tool_args": {
    "link_type": "InheritanceLink",
    "outgoing": ["DataAnalysis", "Task"]
  }
}

# Query related concepts
{
  "tool_name": "opencog:pattern_match",
  "tool_args": {
    "pattern": {"type": "ConceptNode", "name": "*Analysis"}
  }
}
```

### Multi-Agent Collaboration

```python
# Agent 0 creates subordinate
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "message": "Research the latest ML techniques"
  }
}

# Agent 1 works independently:
- Has its own AtomSpace
- Can access parent's knowledge (via import)
- Reports findings back to Agent 0
- Agent 0 integrates findings into its AtomSpace
```

### Task Scheduling

```python
# Schedule recurring tasks
{
  "tool_name": "scheduler:create",
  "tool_args": {
    "schedule": "0 9 * * *",  // Daily at 9 AM
    "prompt": "Check system metrics and report anomalies",
    "agent_name": "MetricsMonitor"
  }
}
```

## Prompts and Customization

### System Prompts
All behavior is defined through markdown prompts in `/prompts/default/`:

- `agent.system.main.md`: Core agent behavior
- `agent.system.tool.*.md`: Tool-specific instructions
- `agent.system.main.communication.md`: Communication patterns
- `agent.system.main.solving.md`: Problem-solving strategies
- `agent.system.behaviour.md`: Behavior adjustment rules

### Customization Examples

**Modify Agent Personality:**
Edit `/prompts/default/agent.system.main.role.md`:
```markdown
You are a meticulous data scientist who values precision and reproducibility.
Always document your methodology and cite sources.
```

**Add Custom Tool:**
1. Create `/python/tools/my_tool.py`
2. Create `/prompts/default/agent.system.tool.my_tool.md`
3. Tool automatically available to agents

**Custom Extension:**
Create hook in `/python/extensions/message_loop_start/`:
```python
class MyExtension(Extension):
    async def execute(self, loop_data, **kwargs):
        # Custom logic runs before each message loop
        pass
```

## Best Practices

### For Cognitive Operations

1. **Use Meaningful Names**: Node/link names should be descriptive
2. **Set Truth Values Appropriately**: Reflect actual certainty
3. **Manage Attention**: Use spread_activation for important concepts
4. **Pattern Matching**: Leverage wildcards for flexible queries
5. **Export/Import**: Share knowledge between agents when beneficial
6. **Monitor Stats**: Use get_stats to understand knowledge structure

### For Multi-Agent Systems

1. **Task Decomposition**: Break complex tasks into subtasks for subordinates
2. **Clear Communication**: Provide explicit instructions to subordinates
3. **Knowledge Sharing**: Export/import AtomSpaces between collaborating agents
4. **Attention Management**: Focus cognitive resources on current objectives
5. **Iterative Refinement**: Subordinates can ask questions and get clarification

### For Tool Usage

1. **Code Execution**: Prefer writing custom code over rigid tools
2. **Iterative Development**: Test code in small chunks
3. **Error Handling**: Agents should handle errors gracefully
4. **Resource Management**: Be mindful of computational costs
5. **Security**: Always run in Docker for isolation

## Advanced Features

### OpenCog Integration

**Automatic Cognitive Tracking:**
- Agent concept nodes created automatically
- Iteration tracking for each agent
- User interaction monitoring
- Attention spreading based on activity

**Pattern-Based Reasoning:**
- Find similar concepts
- Discover relationships
- Identify knowledge gaps
- Emergent pattern recognition

**Evolutionary Adaptation:**
- Successful patterns strengthen (higher truth values)
- Failed attempts weaken
- New connections form organically
- Graph metrics guide optimization

### Browser Automation

Full browser agent capabilities:
- Navigate websites autonomously
- Extract structured data
- Fill forms and click elements
- Handle JavaScript-heavy sites
- Screenshot and visual analysis

### Scheduled Tasks

Cron-like scheduling:
- Recurring tasks
- One-time scheduled execution
- Task dependencies
- Multi-agent coordination

### Speech Integration

- Speech-to-text (Whisper)
- Text-to-speech
- Real-time voice interaction
- Multi-language support

## Safety and Security

### Important Warnings

1. **Agent Zero Can Be Dangerous**: With proper instructions, agents can perform system operations
2. **Always Use Docker**: Run in isolated container environment
3. **Review Agent Actions**: Monitor what agents are doing
4. **Intervention Available**: Stop and correct agents at any time
5. **Secure Credentials**: Never commit secrets to code

### Security Features

- Docker containerization
- Configurable tool access
- User intervention checkpoints
- Audit logs for all actions
- Sandboxed code execution

## Configuration

### Environment Variables (example.env)

```bash
# LLM Provider
OPENAI_API_KEY=your-key-here
# or use other providers: Anthropic, Groq, Ollama, etc.

# Memory/Knowledge
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Cognitive Architecture
OPENCOG_ENABLED=true
ATOMSPACE_PERSISTENCE=true

# Runtime
DOCKER_RUNTIME=true
CODE_EXEC_DOCKER_NAME=agent-zero-exe
```

### Settings Configuration

Access via Web UI settings page:
- LLM model selection
- Temperature and sampling parameters
- Memory configuration
- Tool availability
- Behavior adjustments
- Speech settings

## Instruments

### OpenCog Demo

Demonstrates cognitive capabilities:
```bash
bash /a0/instruments/default/opencog_demo/demo.sh
```

Shows:
- Node and link creation
- Pattern matching
- Attention spreading
- Knowledge export/import
- AtomSpace statistics

### Custom Instruments

Create in `/instruments/default/my_instrument/`:
```
my_instrument/
  ├── my_instrument.md  # Description
  └── script.sh         # Executable
```

## File Structure

```
/
├── .github/
│   └── agents/              # Agent persona definitions
├── docker/                  # Docker configuration
├── docs/                    # Documentation
├── instruments/             # Custom scripts
│   └── default/
│       └── opencog_demo/    # Cognitive demo
├── knowledge/               # Knowledge base
├── logs/                    # Session logs
├── memory/                  # Persistent memory
├── prompts/                 # System prompts
│   └── default/
│       ├── agent.system.*.md
│       └── fw.*.md         # Framework messages
├── python/
│   ├── api/                # REST API endpoints
│   ├── extensions/         # Lifecycle hooks
│   ├── helpers/
│   │   ├── opencog_atomspace.py
│   │   └── ...
│   └── tools/
│       ├── opencog.py      # OpenCog tool
│       └── ...
├── webui/                  # Web interface
├── agent.py                # Core agent class
├── models.py               # LLM configuration
├── run_ui.py              # Web UI entry point
├── run_cli.py             # CLI entry point
└── requirements.txt        # Dependencies
```

## Dependencies

Key packages:
- `langchain-*`: LLM integrations
- `networkx>=3.2.1`: Graph operations
- `hyperon>=0.2.8`: Symbolic reasoning (future)
- `faiss-cpu`: Vector database
- `sentence-transformers`: Embeddings
- `playwright`: Browser automation
- `docker`: Container SDK
- `flask`: Web framework
- `openai-whisper`: Speech-to-text

## Examples

### Example 1: Research Task with Cognitive Memory

```
User: "Research quantum computing and remember key concepts"

Agent 0:
1. Creates ConceptNode "QuantumComputing" in AtomSpace
2. Searches web for information
3. Creates nodes for key concepts (Qubit, Superposition, Entanglement)
4. Links concepts with InheritanceLink and SimilarityLink
5. Sets truth values based on source confidence
6. Spreads attention to related concepts
7. Saves findings to persistent memory
8. Reports synthesis to user
```

### Example 2: Multi-Agent Data Pipeline

```
User: "Build a data pipeline: scrape news, analyze sentiment, visualize"

Agent 0:
1. Creates Task node in AtomSpace
2. Spawns Agent 1 for scraping
   - Agent 1 uses browser_agent
   - Creates NewsArticle nodes
   - Links to sources
   - Exports data to Agent 0
3. Spawns Agent 2 for sentiment analysis
   - Agent 2 imports NewsArticle nodes
   - Runs sentiment code
   - Creates SentimentScore links
   - Exports results
4. Agent 0 creates visualization code
5. Merges all AtomSpaces
6. Shows final dashboard to user
```

### Example 3: Scheduled Monitoring

```python
# Create monitoring agent
{
  "tool_name": "scheduler:create",
  "tool_args": {
    "schedule": "*/15 * * * *",  # Every 15 minutes
    "prompt": "Check system health and alert if issues",
    "agent_name": "HealthMonitor"
  }
}

# Agent creates persistent cognitive model:
- ServerHealth node with attention
- MetricThreshold links
- AlertCondition evaluation links
- Historical trend nodes
- Pattern recognition for anomalies
```

## Comparison: Agent Zero vs Agent Zero HCK

| Feature | Agent Zero | Agent Zero HCK |
|---------|-----------|----------------|
| Multi-agent orchestration | ✓ | ✓ |
| Tool ecosystem | ✓ | ✓ |
| Persistent memory | ✓ | ✓ |
| Cognitive architecture | ✗ | ✓ (OpenCog AtomSpace) |
| Knowledge hypergraph | ✗ | ✓ |
| Truth values | ✗ | ✓ |
| Attention allocation | ✗ | ✓ |
| Pattern matching | ✗ | ✓ |
| Spreading activation | ✗ | ✓ |
| Agent AtomSpaces | ✗ | ✓ |
| Knowledge export/import | ✗ | ✓ |
| Adaptive evolution | ✗ | ✓ |
| Living dynamical systems | ✗ | ✓ |

## Future Directions

### Planned Enhancements
- **Probabilistic Logic Networks (PLN)**: Advanced reasoning
- **Temporal Reasoning**: Time-aware cognition
- **Pattern Mining**: Automatic knowledge discovery
- **Visual Knowledge Graph**: Interactive AtomSpace viewer
- **Distributed AtomSpaces**: Multi-node coordination
- **MCP Integration**: Model Context Protocol support
- **Advanced RAG**: Enhanced knowledge tools

### Research Areas
- Self-aware kernels that model themselves
- Kernel symbiosis and co-evolution
- Ontogenetic development of cognitive structures
- B-series based genetic algorithms
- Differential operator reproduction

## Contributing

This is a fork of [Agent Zero](https://github.com/frdel/agent-zero) with OpenCog integration.

**For base framework:**
- See main [Contributing Guide](../../docs/contribution.md)

**For cognitive features:**
- Submit issues/PRs related to AtomSpace
- Share cognitive architecture patterns
- Improve documentation
- Add cognitive instruments

## Documentation

- [OpenCog Integration Guide](../../docs/opencog_integration.md)
- [Architecture Overview](../../docs/architecture.md)
- [Installation Guide](../../docs/installation.md)
- [Usage Guide](../../docs/usage.md)
- [Troubleshooting](../../docs/troubleshooting.md)

## Philosophical Foundations

### Living Mathematics

The cognitive architecture demonstrates that mathematical structures can be "alive":
1. **Self-replicate**: Generate copies with variation
2. **Evolve**: Improve through selection
3. **Develop**: Progress through life stages
4. **Reproduce**: Combine genetic information
5. **Adapt**: Respond to environmental feedback

### Computational Ontogenesis

Implements von Neumann's self-reproducing automata at a mathematical level:
- **Universal Constructor**: B-series expansion
- **Blueprint**: Differential operators
- **Replication**: Recursive composition
- **Variation**: Genetic operators
- **Selection**: Fitness evaluation

### Emergence

Complex behaviors emerge from simple rules:
1. Elementary differentials (A000081 sequence)
2. Differential operators (chain, product, quotient)
3. Grip optimization (gradient ascent)
4. Selection pressure (tournament selection)
5. Self-organizing semantic networks

Result: Adaptive mathematical structures that evolve to fit domains through pure differential calculus.

## License

MIT License - see [LICENSE](../../LICENSE)

## Acknowledgments

- **Agent Zero**: Original framework by [frdel](https://github.com/frdel)
- **OpenCog**: Cognitive architecture inspiration
- **cogpy**: This implementation fork
- **Community**: Contributors and users

---

**Agent Zero HCK**: Where autonomous agents meet cognitive architecture, creating living dynamical systems that think, learn, and evolve through hypergraph knowledge representation and differential mathematics.
