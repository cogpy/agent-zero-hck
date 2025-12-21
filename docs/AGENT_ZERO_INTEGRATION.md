# Agent-Zero Base Framework Integration Architecture

## Overview

This document describes the architecture for integrating the Agent-Zero base framework with the Himiko Toga Cognitive Kernel (HCK), replacing all stub implementations with real functionality.

## Current State Analysis

### Stub Implementations to Replace

The current `agents/toga_hck/agent.py` contains several stub implementations that need to be replaced:

1. **Agent Base Class Stub** (lines 26-42)
   - Fallback `Agent` class when base not found
   - Fallback `AgentConfig`, `Tool`, `Response` classes

2. **NPU Coprocessor Stub** (lines 154-158)
   - `_initialize_npu()` returns `None`

3. **AtomSpace Stub** (lines 160-164)
   - `_initialize_atomspace()` returns `None`

4. **Ontogenesis Stub** (lines 166-170)
   - `_initialize_ontogenesis()` returns `None`

5. **Relevance Realization Stub** (lines 172-176)
   - `_initialize_relevance_realization()` returns `None`

6. **Agent-Zero Process Stub** (lines 343-354)
   - `_agent_zero_process()` returns simple string instead of using real orchestration

## Integration Architecture

### Layer 1: Base Framework Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    AgentZeroHCK (Extended Agent)                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ TogaPersonality │  │ TransformQuirk  │  │ SecurityTester  │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           └────────────────────┼────────────────────┘           │
│                                │                                │
│  ┌─────────────────────────────┴─────────────────────────────┐  │
│  │              Agent-Zero Base Framework                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │  │
│  │  │ History  │  │  Tools   │  │ Context  │  │Extensions│   │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 2: Cognitive Extensions

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cognitive Extension Layer                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  NPU Coprocessor│  │    AtomSpace    │  │   Ontogenesis   │  │
│  │  (llama.cpp)    │  │   (OpenCog)     │  │    Kernel       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Relevance Realization Engine                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Dependency Management

### Required Dependencies

```python
# requirements.txt additions
agent-zero @ git+https://github.com/agent0ai/agent-zero.git
langchain-core>=0.1.0
langchain-openai>=0.0.5
nest-asyncio>=1.5.0

# Optional cognitive dependencies
# opencog-atomspace>=5.0.0  # For AtomSpace integration
# llama-cpp-python>=0.2.0   # For NPU coprocessor
```

### Conditional Imports

The integration uses conditional imports to handle optional dependencies gracefully:

```python
# Core Agent-Zero (required)
try:
    from agent import Agent, AgentConfig, AgentContext
    from python.helpers.tool import Tool, Response
    from python.helpers.history import History
    AGENT_ZERO_AVAILABLE = True
except ImportError:
    AGENT_ZERO_AVAILABLE = False
    # Minimal fallback for testing only

# Optional: NPU Coprocessor
try:
    from llama_cpp import Llama
    NPU_AVAILABLE = True
except ImportError:
    NPU_AVAILABLE = False

# Optional: AtomSpace
try:
    from opencog.atomspace import AtomSpace, TruthValue
    from opencog.type_constructors import *
    ATOMSPACE_AVAILABLE = True
except ImportError:
    ATOMSPACE_AVAILABLE = False
```

## Implementation Plan

### Phase 1: Base Framework Integration

1. **Copy Agent-Zero base to repository** (as submodule or vendored)
2. **Update import structure** to properly resolve Agent-Zero modules
3. **Extend Agent class** instead of using stub
4. **Implement proper AgentConfig** with Toga-specific settings

### Phase 2: Tool Integration

1. **Create Toga-specific tools** extending Agent-Zero Tool class
2. **Implement Transform Quirk tool** for code absorption
3. **Implement Security Testing tool** for vulnerability analysis
4. **Register tools** with Agent-Zero tool ecosystem

### Phase 3: Extension Integration

1. **Create agent_init extension** for Toga personality initialization
2. **Create monologue_start extension** for personality framing
3. **Create response_stream_end extension** for Toga commentary
4. **Register extensions** with Agent-Zero extension system

### Phase 4: Cognitive Components (Optional)

1. **NPU Coprocessor** - Local LLM inference via llama.cpp
2. **AtomSpace** - Cognitive architecture integration
3. **Ontogenesis** - Developmental learning kernel
4. **Relevance Realization** - Attention and salience engine

## File Structure

```
agent-zero-hck/
├── agents/
│   └── toga_hck/
│       ├── __init__.py
│       ├── agent.py              # Main AgentZeroHCK class
│       ├── config.py             # Configuration classes
│       ├── extensions/           # Agent-Zero extensions
│       │   ├── __init__.py
│       │   ├── agent_init/
│       │   │   └── _10_toga_personality.py
│       │   └── response/
│       │       └── _10_toga_commentary.py
│       ├── tools/                # Agent-Zero tools
│       │   ├── __init__.py
│       │   ├── transform_quirk.py
│       │   ├── security_test.py
│       │   └── response.py
│       └── prompts/              # Toga-specific prompts
│           ├── agent.system.main.role.md
│           └── agent.system.tool.transform.md
├── python/
│   └── helpers/
│       ├── toga_personality.py   # Personality system
│       ├── toga_transform.py     # Transform Quirk
│       ├── toga_security.py      # Security testing
│       └── toga_cognitive.py     # NEW: Cognitive components
├── lib/
│   └── agent_zero/               # Vendored Agent-Zero base
│       ├── agent.py
│       ├── models.py
│       └── python/
│           └── helpers/
└── requirements.txt
```

## API Design

### AgentZeroHCK Class

```python
class AgentZeroHCK(Agent):
    """
    Extended Agent-Zero with Toga personality overlay.
    
    Inherits from Agent-Zero base and adds:
    - Toga personality system
    - Transform Quirk capabilities
    - Security testing tools
    - Optional cognitive components
    """
    
    def __init__(
        self,
        number: int,
        config: AgentConfig,
        context: AgentContext | None = None,
        hck_config: AgentZeroHCKConfig | None = None
    ):
        # Initialize base Agent-Zero
        super().__init__(number, config, context)
        
        # Initialize Toga components
        self.hck_config = hck_config or AgentZeroHCKConfig()
        self.toga_personality = initialize_toga_personality(...)
        self.transform_quirk = initialize_transform_quirk()
        self.security_tester = initialize_toga_security_tester()
        
        # Initialize optional cognitive components
        self._init_cognitive_components()
    
    async def process_message(
        self,
        message: str,
        context: dict | None = None
    ) -> str:
        """
        Process message through Toga personality and Agent-Zero orchestration.
        """
        # Frame through Toga personality
        framed = self.toga_personality.frame_input(message, context)
        
        # Use Agent-Zero's monologue for processing
        response = await self.monologue()
        
        # Add Toga commentary
        return self.toga_personality.add_commentary(response)
```

### Tool Integration

```python
class TransformQuirkTool(Tool):
    """
    Agent-Zero tool for Transform Quirk operations.
    """
    
    async def execute(self, **kwargs) -> Response:
        target = self.args.get("target", "")
        operation = self.args.get("operation", "taste")
        
        if operation == "taste":
            result = self.agent.transform_quirk.taste_target(target, ...)
        elif operation == "transform":
            result = self.agent.transform_quirk.transform_into(target)
        else:
            result = "Unknown operation"
        
        return Response(message=result, break_loop=False)
```

## Configuration

### AgentZeroHCKConfig

```python
@dataclass
class AgentZeroHCKConfig:
    """Extended configuration for Agent-Zero-HCK."""
    
    # Personality settings
    personality_tensor: TogaPersonalityTensor | None = None
    enable_transform_quirk: bool = True
    enable_security_testing: bool = True
    
    # Cognitive settings
    enable_npu: bool = False
    npu_model_path: str | None = None
    enable_atomspace: bool = False
    enable_ontogenesis: bool = False
    enable_relevance_realization: bool = False
    
    # Ethical constraints
    ethical_testing_only: bool = True
    respect_boundaries: float = 0.95
```

## Testing Strategy

### Unit Tests

1. **Import tests** - Verify all modules can be imported
2. **Initialization tests** - Verify AgentZeroHCK initializes correctly
3. **Tool tests** - Verify tools execute correctly
4. **Extension tests** - Verify extensions are called

### Integration Tests

1. **Message processing** - End-to-end message handling
2. **Tool invocation** - Verify tools are invoked by Agent-Zero
3. **Personality overlay** - Verify Toga personality is applied
4. **Cognitive components** - Verify optional components work

### Compatibility Tests

1. **Agent-Zero base** - Verify compatibility with upstream
2. **Fallback mode** - Verify graceful degradation without base
3. **Optional dependencies** - Verify behavior without optional deps

## Migration Path

### Step 1: Vendor Agent-Zero Base

```bash
# Add Agent-Zero as vendored dependency
mkdir -p lib/agent_zero
cp -r /path/to/agent-zero-main/* lib/agent_zero/
```

### Step 2: Update Imports

```python
# Before
try:
    from agent import Agent, AgentConfig
except ImportError:
    class Agent: ...  # stub

# After
import sys
sys.path.insert(0, "lib/agent_zero")
from agent import Agent, AgentConfig, AgentContext
```

### Step 3: Extend Agent Class

```python
# Before
class AgentZeroHCK(Agent):
    def __init__(self, config=None):
        super().__init__()  # stub

# After
class AgentZeroHCK(Agent):
    def __init__(self, number, config, context=None, hck_config=None):
        super().__init__(number, config, context)
        # Initialize Toga components
```

### Step 4: Implement Tools

Create proper Agent-Zero tools in `agents/toga_hck/tools/`.

### Step 5: Implement Extensions

Create Agent-Zero extensions in `agents/toga_hck/extensions/`.

## Success Criteria

1. ✅ No stub implementations in production code
2. ✅ Full Agent-Zero tool ecosystem available
3. ✅ Toga personality applied to all responses
4. ✅ Transform Quirk works as Agent-Zero tool
5. ✅ Security testing works as Agent-Zero tool
6. ✅ All tests pass with real implementations
7. ✅ Optional cognitive components work when enabled
8. ✅ Graceful degradation when optional deps missing

## Next Steps

1. **Implement base framework integration** (Phase 3)
2. **Create Toga-specific tools** (Phase 3)
3. **Create Toga-specific extensions** (Phase 3)
4. **Update test suite** (Phase 4)
5. **Validate integration** (Phase 5)
6. **Commit and verify CI/CD** (Phase 6)
