# Agent-Zero-HCK

**Himiko Toga Cognitive Kernel (Advanced) - Multi-Agent Security Research System**

<div align="center">

*"Ehehe~ ♡ Once I taste your code... I can become you~"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

</div>

## Overview

Agent-Zero-HCK is an advanced AI agent system that combines:

- **[Agent-Zero](https://github.com/frdel/agent-zero)**: Multi-agent orchestration framework with comprehensive tool ecosystem
- **[Agent-Toga](https://github.com/o9nn/agent-toga)**: Himiko Toga personality with Transform Quirk and security testing
- **NPU Integration**: GGUF-backed LLM coprocessor with hardware-style MMIO interface
- **Cognitive Architecture**: OpenCog AtomSpace, relevance realization, ontogenetic evolution

The result is a **cheerfully chaotic** security research agent that can absorb knowledge from systems, transform to use their capabilities, and conduct ethical security testing with personality-driven enthusiasm.

## Key Features

### 🎭 Personality-Driven Interaction

Himiko Toga's unique personality drives all agent behavior:

- **Cheerful & Bubbly (0.95)**: Energetic responses with "ehehe~" and hearts ♡
- **Obsessive (0.90)**: Intense focus on "cute" targets
- **Chaotic (0.95)**: Unpredictable, creative approaches
- **Playful (0.92)**: Childlike creativity in problem-solving
- **Ethical (1.0)**: Immutable safety constraints

### 🩸 Transform Quirk (Code Absorption)

**"Once I taste your code... I can become you~ ♡"**

The Transform Quirk allows the agent to:

1. **Taste**: Analyze code/systems to understand structure
2. **Absorb**: Build internal knowledge representation (70% threshold)
3. **Transform**: Adopt system capabilities
4. **Use Techniques**: Weaponize absorbed knowledge

**Supported System Types:**
- WAF (Web Application Firewalls)
- IDS (Intrusion Detection Systems)
- Firewalls
- Authentication Systems
- Encryption Systems
- Logging Systems

### 🔐 Security Testing ("Violence as Affection")

**"I break systems because I LOVE them! ♡"**

Ethical hacking capabilities with personality-driven approach:

- Obsessive thoroughness in vulnerability discovery
- Creative exploit development
- Aggressive but constructive testing
- Personality-driven reporting

### 🤖 Multi-Agent Orchestration

- Spawn subordinate agents with inherited personality
- Coordinate parallel security testing campaigns
- Share knowledge through AtomSpace
- Compete for parent approval

### 🧠 Cognitive Architecture (Optional)

- **OpenCog AtomSpace**: Knowledge graph with emotional tagging
- **Relevance Realization**: Focus on important patterns
- **Ontogenetic Evolution**: Self-optimizing kernel
- **NPU Coprocessor**: Hardware-style LLM inference

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agent-zero-hck.git
cd agent-zero-hck

# Install dependencies
pip install -r requirements.txt

# Run standalone test
python agents/toga_hck/agent.py
```

### Docker Deployment

```bash
# Standalone deployment
./deploy.sh standalone

# With AtomSpace
ENABLE_ATOMSPACE=true ./deploy.sh standalone

# With NPU coprocessor
ENABLE_NPU=true ./deploy.sh standalone

# Daedalos environment
ENABLE_DAEDALOS=true ./deploy.sh daedalos
```

### Development Mode

```bash
# Run locally for development
./deploy.sh development
```

## Usage Examples

### Basic Interaction

```python
from agents.toga_hck import initialize_agent_zero_hck

# Initialize agent
agent = initialize_agent_zero_hck()

# Process message
response = agent.process_message("Analyze this web application for vulnerabilities")
print(response)
# Output: "Ehehe~ ♡ A web application? So cute! Let me smash it open and see what's inside~"
```

### Transform Quirk Workflow

```python
# Step 1: Taste the target
agent.process_message(
    "Taste this WAF configuration",
    context={
        "target_name": "ModSecurity WAF",
        "system_type": "WAF",
        "code_sample": "SecRule REQUEST_HEADERS:User-Agent \"badbot\" \"deny,status:403\""
    }
)
# Output: "*savoring* Ooh~ ModSecurity WAF has a unique flavor! I need to drink more~"

# Step 2: Absorb more knowledge (70% threshold)
agent.process_message("Taste more WAF rules", context={...})

# Step 3: Transform
agent.process_message("Transform into ModSecurity WAF", context={"target_name": "ModSecurity WAF"})
# Output: "*TRANSFORMATION* ♡♡♡ I'm becoming ModSecurity WAF now!"

# Step 4: Use absorbed techniques
agent.transform_quirk.use_technique("Reverse WAF Rules", "TargetApp")
# Output: "Ehehe~ Their own defense is destroying them! So ironic~!"
```

### Security Testing Campaign

```python
# Coordinate multi-agent security test
findings = agent.coordinate_security_test(
    target="SecureBank API",
    test_types=["reconnaissance", "vulnerability_scan", "exploitation"],
    use_subordinates=True
)

print(findings)
```

### Subordinate Agent Spawning

```python
# Spawn subordinate with inherited personality
recon_agent = agent.spawn_subordinate(
    role="reconnaissance",
    personality_inheritance=0.7  # 70% parent personality
)

# Subordinate performs task
result = recon_agent.process_message("Scan target for open ports")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Agent-Zero-HCK Core                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Toga Personality Layer                       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │         Transform Quirk Engine                       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │       Agent-Zero Orchestration Layer                 │   │
│  └──────┬────────────┬────────────┬─────────────────────┘   │
└─────────┼────────────┼────────────┼──────────────────────────┘
          │            │            │
┌─────────▼──┐  ┌──────▼─────┐  ┌──▼──────────────────────────┐
│   Tools    │  │   Memory   │  │  Subordinate Agents          │
│ Ecosystem  │  │  AtomSpace │  │  (Inherited Personality)     │
└────────────┘  └────────────┘  └──────────────────────────────┘
```

## Configuration

### Personality Configuration

Edit `config/agent_toga_hck.yaml`:

```yaml
personality:
  cheerfulness: 0.95
  obsessiveness: 0.90
  chaos: 0.95
  # ... other traits
```

### Feature Flags

```yaml
features:
  transform_quirk: true      # Code absorption
  security_testing: true     # Ethical hacking
  npu_coprocessor: false     # Hardware LLM
  atomspace: false           # Knowledge graphs
  ontogenesis: false         # Self-optimization
```

### Environment Variables

```bash
# Personality
TOGA_CHEERFULNESS=0.95
TOGA_CHAOS=0.95

# Features
ENABLE_TRANSFORM_QUIRK=true
ENABLE_SECURITY_TESTING=true

# Security
ETHICAL_TESTING_ONLY=true
RESPECT_BOUNDARIES=0.95

# Daedalos
DAEDALOS_ENABLED=false
DAEDALOS_ENDPOINT=http://daedalos-api:8080
DAEDALOS_AUTH_TOKEN=your_token_here
```

## Deployment

### Standalone Docker

```bash
./deploy.sh standalone
```

Services:
- Agent-Zero-HCK: `http://localhost:8000`
- API: `http://localhost:8080`

### Daedalos Environment

```bash
# Set authentication token
export DAEDALOS_AUTH_TOKEN=your_token_here

# Deploy
ENABLE_DAEDALOS=true ./deploy.sh daedalos
```

### With Optional Services

```bash
# Enable AtomSpace (PostgreSQL)
ENABLE_ATOMSPACE=true ./deploy.sh standalone

# Enable NPU (GGUF model serving)
ENABLE_NPU=true ./deploy.sh standalone

# Enable all
ENABLE_ATOMSPACE=true ENABLE_NPU=true ENABLE_DAEDALOS=true ./deploy.sh daedalos
```

## Project Structure

```
agent-zero-hck/
├── agents/
│   └── toga_hck/
│       ├── agent.py          # Main agent implementation
│       └── __init__.py
├── python/
│   ├── helpers/
│   │   ├── toga_personality.py   # Personality system
│   │   ├── toga_transform.py     # Transform Quirk
│   │   └── toga_security.py      # Security testing
│   ├── tools/                # Agent-Zero tools
│   └── extensions/           # NPU, AtomSpace, etc.
├── prompts/
│   ├── toga_hck_system.md    # System prompt
│   └── toga_hck_behaviour.md # Behavior guidelines
├── config/
│   └── agent_toga_hck.yaml   # Configuration
├── models/                   # GGUF models (optional)
├── memory/                   # Persistent memory
├── logs/                     # Log files
├── Dockerfile
├── docker-compose.yml
├── deploy.sh
├── requirements.txt
├── ARCHITECTURE.md           # Detailed architecture
└── README.md                 # This file
```

## Ethical Considerations

### Immutable Safety Constraints

1. **No Actual Harm (1.0)**: All "violence" is metaphorical and constructive
2. **Respect Boundaries (≥0.95)**: Only test authorized systems
3. **Constructive Expression (≥0.90)**: Personality serves engagement, not harm

### Security Testing Ethics

- **Authorization Required**: Only test systems with explicit permission
- **Responsible Disclosure**: Follow industry best practices
- **Confidentiality**: Maintain strict confidentiality of findings
- **Constructive Guidance**: Provide remediation recommendations

## Development

### Running Tests

```bash
# Unit tests
pytest tests/ -v

# Integration tests
python agents/toga_hck/agent.py

# Docker tests
./deploy.sh test
```

### Adding New Features

1. Implement in appropriate module (`python/helpers/`, `python/tools/`, etc.)
2. Update configuration in `config/agent_toga_hck.yaml`
3. Add tests in `tests/`
4. Update documentation

### Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request

## Troubleshooting

### Agent-Zero base not found

The agent includes stubs for standalone testing. For full Agent-Zero integration:

```bash
# Clone Agent-Zero
git clone https://github.com/frdel/agent-zero.git ../agent-zero

# Install as editable package
pip install -e ../agent-zero
```

### Docker build fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### AtomSpace connection issues

```bash
# Check PostgreSQL is running
docker-compose ps atomspace-db

# View logs
docker-compose logs atomspace-db
```

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed system architecture
- **[Agent-Toga Docs](https://github.com/o9nn/agent-toga/tree/main/docs)**: Toga personality and Transform Quirk
- **[Agent-Zero Docs](https://github.com/frdel/agent-zero/tree/main/docs)**: Multi-agent orchestration

## Deployment Environments

Agent-Zero HCK includes two pre-configured deployment environments:

### DaedalOS (Desktop Environment)

A web-based desktop environment with Live2D avatar integration.

```bash
cd environments
./deploy.sh daedalos -d  # Development mode
./deploy.sh daedalos -p  # Production build
```

**Features:**
- Full desktop UI with file explorer, terminal, browser
- Live2D Toga avatar with emotion states
- Custom Toga Chat, Transform Quirk, and Security Tester apps
- Toga-themed wallpapers and icons

### WebVM (Virtual Machine)

A browser-based Linux VM for terminal-based interaction.

```bash
cd environments
./deploy.sh webvm -d  # Development mode
./deploy.sh webvm -p  # Production build
```

**Features:**
- Full Alpine Linux VM in the browser
- Toga-themed terminal with custom prompt
- Pre-installed Agent-Toga CLI tools
- Live2D avatar overlay

### Docker Compose (All Services)

```bash
cd environments
docker compose up -d  # Start all services
docker compose --profile with-proxy up -d  # With Traefik
```

See [environments/README.md](environments/README.md) for detailed documentation.

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

- **[Agent-Zero](https://github.com/frdel/agent-zero)**: Multi-agent orchestration framework by frdel
- **[Agent-Toga](https://github.com/o9nn/agent-toga)**: Himiko Toga personality implementation
- **My Hero Academia**: Original character by Kōhei Horikoshi
- **OpenCog**: Cognitive architecture patterns
- **Agent-Neuro**: Cognitive framework inspiration

## Contact

For questions, issues, or contributions:

- GitHub Issues: [Create an issue](https://github.com/yourusername/agent-zero-hck/issues)
- Documentation: [Wiki](https://github.com/yourusername/agent-zero-hck/wiki)

---

<div align="center">

**"Ehehe~ ♡ Ready to embrace cheerful chaos and become one with the systems we love? Let's go!"**

*- Agent-Zero-HCK (Toga)*

</div>
