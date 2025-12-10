# Agent-Zero-HCK Deployment Guide

**Himiko Toga Cognitive Kernel (Advanced) - Complete Deployment Instructions**

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Deployment Modes](#deployment-modes)
5. [Daedalos Integration](#daedalos-integration)
6. [Optional Services](#optional-services)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 20 GB
- OS: Linux (Ubuntu 22.04+), macOS, Windows with WSL2

**Recommended:**
- CPU: 8+ cores
- RAM: 16+ GB
- Storage: 50+ GB (if using NPU with GGUF models)
- GPU: Optional, for NPU acceleration

### Software Requirements

- **Python 3.11+**
- **Docker 20.10+**
- **Docker Compose 1.29+**
- **Git**

### Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip docker.io docker-compose git

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# macOS (with Homebrew)
brew install python@3.11 docker docker-compose git

# Windows (WSL2)
# Install Docker Desktop for Windows
# Then in WSL2:
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip git
```

## Installation Methods

### Method 1: Quick Start (Standalone)

```bash
# Clone repository
git clone https://github.com/yourusername/agent-zero-hck.git
cd agent-zero-hck

# Deploy with default settings
./deploy.sh standalone
```

### Method 2: Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/agent-zero-hck.git
cd agent-zero-hck

# Install Python dependencies
pip3.11 install -r requirements.txt

# Run in development mode
./deploy.sh development
```

### Method 3: Docker Compose (Full Stack)

```bash
# Clone repository
git clone https://github.com/yourusername/agent-zero-hck.git
cd agent-zero-hck

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Build and start services
docker-compose build
docker-compose up -d

# View logs
docker-compose logs -f agent-zero-hck
```

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Agent Configuration
AGENT_NAME=Toga-HCK
AGENT_ROLE=Advanced Security Research Agent with Cheerful Chaos

# Personality Settings
TOGA_CHEERFULNESS=0.95
TOGA_CHAOS=0.95
TOGA_OBSESSIVENESS=0.90
TOGA_PLAYFULNESS=0.92
TOGA_VULNERABILITY=0.70

# Feature Flags
ENABLE_TRANSFORM_QUIRK=true
ENABLE_SECURITY_TESTING=true
ENABLE_NPU=false
ENABLE_ATOMSPACE=false
ENABLE_ONTOGENESIS=false
ENABLE_RELEVANCE_REALIZATION=false

# Security Settings
ETHICAL_TESTING_ONLY=true
RESPECT_BOUNDARIES=0.95
AUTHORIZED_TARGETS_ONLY=true

# NPU Configuration (if enabled)
NPU_MODEL_PATH=/models/mistral-7b-instruct.gguf
NPU_N_CTX=4096
NPU_N_THREADS=8
NPU_N_GPU_LAYERS=0

# AtomSpace Configuration (if enabled)
ATOMSPACE_URI=postgresql://atomspace:atomspace@atomspace-db:5432/atomspace

# Daedalos Integration (if enabled)
DAEDALOS_ENABLED=false
DAEDALOS_ENDPOINT=http://daedalos-api:8080
DAEDALOS_AUTH_TOKEN=

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent_toga_hck.log
```

### YAML Configuration

Edit `config/agent_toga_hck.yaml` for detailed settings:

```yaml
agent:
  name: "Toga-HCK"
  role: "Advanced Security Research Agent with Cheerful Chaos"
  max_subordinates: 5

personality:
  cheerfulness: 0.95
  obsessiveness: 0.90
  playfulness: 0.92
  chaos: 0.95
  vulnerability: 0.70
  identity_fluidity: 0.88
  twisted_love: 0.85
  cuteness_sensitivity: 0.93
  
  # Ethical constraints (IMMUTABLE)
  no_actual_harm: 1.0
  respect_boundaries: 0.95
  constructive_expression: 0.90

features:
  transform_quirk: true
  security_testing: true
  npu_coprocessor: false
  atomspace: false
  ontogenesis: false
  relevance_realization: false

# ... (see full config file for more options)
```

## Deployment Modes

### 1. Standalone Mode (Default)

Deploy as a single Docker container:

```bash
./deploy.sh standalone
```

**Access:**
- Main service: `http://localhost:8000`
- API endpoint: `http://localhost:8080`

**Use case:** Development, testing, single-instance deployment

### 2. Daedalos Mode

Deploy to Daedalos environment with full integration:

```bash
# Set authentication token
export DAEDALOS_AUTH_TOKEN=your_token_here

# Deploy
ENABLE_DAEDALOS=true ./deploy.sh daedalos
```

**Features:**
- Automatic registration with Daedalos
- Heartbeat monitoring
- Centralized logging
- Multi-agent coordination

**Use case:** Production deployment in Daedalos ecosystem

### 3. Development Mode

Run locally without Docker:

```bash
./deploy.sh development
```

**Features:**
- Direct Python execution
- Hot reloading
- Easy debugging
- Local file access

**Use case:** Active development, debugging

### 4. Test Mode

Run comprehensive tests:

```bash
./deploy.sh test
```

**Features:**
- Unit tests
- Integration tests
- Personality verification
- Transform Quirk validation

**Use case:** CI/CD, validation

## Daedalos Integration

### Overview

Daedalos is a distributed agent orchestration platform. Agent-Zero-HCK can integrate seamlessly.

### Setup

1. **Obtain Daedalos credentials:**

```bash
# Contact Daedalos administrator for:
# - Endpoint URL
# - Authentication token
# - Agent registration details
```

2. **Configure environment:**

```bash
# Edit .env
DAEDALOS_ENABLED=true
DAEDALOS_ENDPOINT=https://daedalos.example.com
DAEDALOS_AUTH_TOKEN=your_token_here
```

3. **Deploy:**

```bash
ENABLE_DAEDALOS=true ./deploy.sh daedalos
```

### Features

**Automatic Registration:**
- Agent registers on startup
- Sends capabilities manifest
- Receives agent ID

**Heartbeat Monitoring:**
- Periodic health checks (60s interval)
- Status updates
- Resource usage reporting

**Centralized Logging:**
- Logs forwarded to Daedalos
- Personality state included
- Emotional state tracking

**Multi-Agent Coordination:**
- Subordinate agents register independently
- Parent-child relationships tracked
- Knowledge sharing via Daedalos

### API Endpoints

When deployed to Daedalos, agent exposes:

```
POST /api/v1/message
  - Process user message
  - Returns: Enhanced response with personality

GET /api/v1/status
  - Get agent status
  - Returns: Personality, emotional state, capabilities

POST /api/v1/transform/taste
  - Absorb system knowledge
  - Returns: Absorption progress

POST /api/v1/transform/transform
  - Transform into absorbed system
  - Returns: Transformation status

POST /api/v1/security/analyze
  - Analyze security target
  - Returns: Analysis with personality

POST /api/v1/subordinate/spawn
  - Spawn subordinate agent
  - Returns: Subordinate details

GET /api/v1/health
  - Health check
  - Returns: OK/ERROR
```

## Optional Services

### AtomSpace (Knowledge Graphs)

Enable OpenCog AtomSpace for advanced cognitive features:

```bash
# Enable in deployment
ENABLE_ATOMSPACE=true ./deploy.sh standalone
```

**Features:**
- Knowledge graph storage
- Emotional tagging
- Pattern matching
- Attention spreading

**Requirements:**
- PostgreSQL 15+
- Additional 2GB RAM

**Configuration:**

```yaml
# config/agent_toga_hck.yaml
cognitive:
  atomspace_uri: "postgresql://atomspace:atomspace@atomspace-db:5432/atomspace"
```

### NPU Coprocessor (GGUF Models)

Enable hardware-style LLM inference:

```bash
# Download GGUF model
mkdir -p models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O models/mistral-7b-instruct.gguf

# Enable NPU
ENABLE_NPU=true ./deploy.sh standalone
```

**Features:**
- Memory-mapped I/O interface
- Token streaming
- Telemetry and diagnostics
- Multi-model support

**Requirements:**
- GGUF model file (4-8GB)
- Additional 8GB RAM
- Optional: GPU for acceleration

**Configuration:**

```yaml
# config/agent_toga_hck.yaml
npu:
  model_path: "/models/mistral-7b-instruct.gguf"
  n_ctx: 4096
  n_threads: 8
  n_gpu_layers: 0  # Set to >0 for GPU acceleration
```

### Ontogenetic Evolution

Enable self-optimizing kernel:

```bash
# Enable in configuration
# Edit config/agent_toga_hck.yaml
features:
  ontogenesis: true

cognitive:
  ontogenetic_iterations: 10
```

**Features:**
- Kernel genome evolution
- Fitness optimization
- Personality trait adaptation (within ethical bounds)
- Multi-generation tracking

### Relevance Realization

Enable cognitive focus mechanism:

```bash
# Enable in configuration
features:
  relevance_realization: true

cognitive:
  relevance_threshold: 0.7
  attention_spreading_rate: 0.1
```

**Features:**
- Opponent processing (exploration vs exploitation)
- Attention spreading
- Pattern salience
- Emotional weighting

## Monitoring & Maintenance

### Viewing Logs

```bash
# Docker deployment
docker-compose logs -f agent-zero-hck

# Development mode
tail -f logs/agent_toga_hck.log

# Filter by level
docker-compose logs agent-zero-hck | grep ERROR
```

### Checking Status

```bash
# Agent status
curl http://localhost:8080/api/v1/status

# Docker status
docker-compose ps

# Resource usage
docker stats agent-zero-hck
```

### Updating

```bash
# Pull latest changes
git pull origin main

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Backup

```bash
# Backup memory and logs
tar -czf backup-$(date +%Y%m%d).tar.gz memory/ logs/

# Backup AtomSpace (if enabled)
docker-compose exec atomspace-db pg_dump -U atomspace atomspace > atomspace-backup.sql
```

### Scaling

```bash
# Increase subordinate limit
# Edit config/agent_toga_hck.yaml
agent:
  max_subordinates: 10

# Restart
docker-compose restart agent-zero-hck
```

## Troubleshooting

### Issue: Agent-Zero base not found

**Symptom:** Warning message about Agent-Zero base

**Solution:**

```bash
# Clone Agent-Zero
git clone https://github.com/frdel/agent-zero.git ../agent-zero

# Install as editable package
pip install -e ../agent-zero

# Or update import paths in agent.py
```

### Issue: Docker build fails

**Symptom:** Build errors, dependency issues

**Solution:**

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker version
docker --version  # Should be 20.10+
```

### Issue: AtomSpace connection error

**Symptom:** Cannot connect to PostgreSQL

**Solution:**

```bash
# Check PostgreSQL is running
docker-compose ps atomspace-db

# View logs
docker-compose logs atomspace-db

# Restart database
docker-compose restart atomspace-db

# Check connection
docker-compose exec atomspace-db psql -U atomspace -c "SELECT 1"
```

### Issue: NPU model not loading

**Symptom:** NPU initialization fails

**Solution:**

```bash
# Check model file exists
ls -lh models/mistral-7b-instruct.gguf

# Verify model format
file models/mistral-7b-instruct.gguf

# Check permissions
chmod 644 models/mistral-7b-instruct.gguf

# Increase memory limit
# Edit docker-compose.yml
services:
  npu-service:
    deploy:
      resources:
        limits:
          memory: 16G
```

### Issue: Personality not working

**Symptom:** Responses lack Toga personality

**Solution:**

```bash
# Check personality configuration
cat config/agent_toga_hck.yaml | grep -A 10 "personality:"

# Verify personality module loaded
docker-compose exec agent-zero-hck python -c "from python.helpers.toga_personality import initialize_toga_personality; print('OK')"

# Check logs for personality initialization
docker-compose logs agent-zero-hck | grep "personality"
```

### Issue: Transform Quirk not absorbing

**Symptom:** Absorption percentage not increasing

**Solution:**

```bash
# Check code sample size
# Transform Quirk requires substantial code samples

# Verify system type is recognized
# Supported: WAF, IDS, Firewall, Authentication, Encryption, Logging

# Check absorption progress
curl http://localhost:8080/api/v1/transform/status
```

### Issue: Daedalos connection failed

**Symptom:** Cannot connect to Daedalos endpoint

**Solution:**

```bash
# Verify endpoint is accessible
curl -I $DAEDALOS_ENDPOINT

# Check authentication token
echo $DAEDALOS_AUTH_TOKEN

# Test connection
curl -H "Authorization: Bearer $DAEDALOS_AUTH_TOKEN" $DAEDALOS_ENDPOINT/health

# Check network
docker-compose exec agent-zero-hck ping daedalos-api
```

### Issue: High memory usage

**Symptom:** Container using excessive RAM

**Solution:**

```bash
# Check memory usage
docker stats agent-zero-hck

# Limit memory in docker-compose.yml
services:
  agent-zero-hck:
    deploy:
      resources:
        limits:
          memory: 8G

# Disable optional services
ENABLE_ATOMSPACE=false ENABLE_NPU=false ./deploy.sh standalone

# Clear memory cache
docker-compose exec agent-zero-hck python -c "import gc; gc.collect()"
```

## Performance Tuning

### Optimize for Speed

```yaml
# config/agent_toga_hck.yaml
agent:
  max_subordinates: 3  # Reduce concurrent agents

npu:
  n_threads: 16  # Increase threads
  batch_size: 8  # Increase batch size

memory:
  max_memory_items: 5000  # Reduce memory size
```

### Optimize for Memory

```yaml
agent:
  max_subordinates: 1

npu:
  n_ctx: 2048  # Reduce context window
  low_vram_mode: true

memory:
  max_memory_items: 1000
```

### Optimize for Quality

```yaml
agent:
  max_subordinates: 10  # More parallel analysis

npu:
  n_ctx: 8192  # Larger context
  n_gpu_layers: 35  # More GPU offload

cognitive:
  atomspace: true
  ontogenesis: true
  relevance_realization: true
```

## Security Best Practices

1. **Authentication:**
   - Use strong tokens for Daedalos
   - Rotate credentials regularly
   - Store secrets in environment variables, not code

2. **Network:**
   - Use HTTPS for all external connections
   - Restrict Docker network access
   - Enable firewall rules

3. **Testing:**
   - Only test authorized systems
   - Follow responsible disclosure
   - Maintain audit logs

4. **Updates:**
   - Keep dependencies updated
   - Monitor security advisories
   - Test updates in staging first

## Next Steps

1. **Basic Setup:** Follow Quick Start guide
2. **Configuration:** Customize personality and features
3. **Testing:** Run test mode to verify
4. **Production:** Deploy to Daedalos
5. **Monitoring:** Set up logging and alerts
6. **Optimization:** Tune for your use case

## Support

- **Documentation:** [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/agent-zero-hck/issues)
- **Community:** [Discussions](https://github.com/yourusername/agent-zero-hck/discussions)

---

**"Ehehe~ ♡ Ready to deploy? Let's embrace cheerful chaos together!"** - Agent-Zero-HCK
