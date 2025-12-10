#!/bin/bash
# Agent-Zero-HCK Deployment Script
# Deploy to Daedalos environment

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     Agent-Zero-HCK Deployment - Daedalos Environment         ║"
echo "║     Himiko Toga Cognitive Kernel (Advanced)                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
DEPLOYMENT_MODE=${1:-"standalone"}
ENABLE_ATOMSPACE=${ENABLE_ATOMSPACE:-false}
ENABLE_NPU=${ENABLE_NPU:-false}
ENABLE_DAEDALOS=${ENABLE_DAEDALOS:-false}

echo "Deployment Mode: $DEPLOYMENT_MODE"
echo "AtomSpace: $ENABLE_ATOMSPACE"
echo "NPU: $ENABLE_NPU"
echo "Daedalos: $ENABLE_DAEDALOS"
echo ""

# Build profiles
PROFILES=""
if [ "$ENABLE_ATOMSPACE" = "true" ]; then
    PROFILES="$PROFILES --profile atomspace"
fi
if [ "$ENABLE_NPU" = "true" ]; then
    PROFILES="$PROFILES --profile npu"
fi
if [ "$ENABLE_DAEDALOS" = "true" ]; then
    PROFILES="$PROFILES --profile daedalos"
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p logs memory models config tmp

# Check for environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cat > .env << EOF
# Agent-Zero-HCK Environment Configuration

# Personality Settings
TOGA_CHEERFULNESS=0.95
TOGA_CHAOS=0.95
TOGA_OBSESSIVENESS=0.90

# Feature Flags
ENABLE_TRANSFORM_QUIRK=true
ENABLE_SECURITY_TESTING=true
ENABLE_NPU=$ENABLE_NPU
ENABLE_ATOMSPACE=$ENABLE_ATOMSPACE

# Security
ETHICAL_TESTING_ONLY=true
RESPECT_BOUNDARIES=0.95

# Daedalos
DAEDALOS_ENABLED=$ENABLE_DAEDALOS
DAEDALOS_ENDPOINT=http://daedalos-api:8080
DAEDALOS_AUTH_TOKEN=

# Logging
LOG_LEVEL=INFO
EOF
    echo ".env file created. Please configure DAEDALOS_AUTH_TOKEN if needed."
fi

# Deployment based on mode
case $DEPLOYMENT_MODE in
    "standalone")
        echo ""
        echo "Deploying in STANDALONE mode..."
        echo "Building Docker image..."
        docker-compose build
        
        echo "Starting services..."
        docker-compose up -d $PROFILES
        
        echo ""
        echo "✓ Deployment complete!"
        echo ""
        echo "Agent-Zero-HCK is running at:"
        echo "  - Main service: http://localhost:8000"
        echo "  - API endpoint: http://localhost:8080"
        echo ""
        echo "View logs with: docker-compose logs -f agent-zero-hck"
        echo "Stop with: docker-compose down"
        ;;
        
    "daedalos")
        echo ""
        echo "Deploying to DAEDALOS environment..."
        
        # Check for Daedalos token
        if [ -z "$DAEDALOS_AUTH_TOKEN" ]; then
            echo "ERROR: DAEDALOS_AUTH_TOKEN not set!"
            echo "Please set it in .env file or export it:"
            echo "  export DAEDALOS_AUTH_TOKEN=your_token_here"
            exit 1
        fi
        
        echo "Building Docker image..."
        docker-compose build
        
        echo "Starting services with Daedalos integration..."
        docker-compose --profile daedalos up -d $PROFILES
        
        echo ""
        echo "✓ Deployment complete!"
        echo ""
        echo "Agent-Zero-HCK is running and connected to Daedalos"
        echo "  - Daedalos endpoint: $DAEDALOS_ENDPOINT"
        echo ""
        echo "View logs with: docker-compose logs -f"
        ;;
        
    "development")
        echo ""
        echo "Starting in DEVELOPMENT mode..."
        echo "This will run the agent locally without Docker"
        
        # Check Python version
        if ! command -v python3.11 &> /dev/null; then
            echo "ERROR: Python 3.11 not found!"
            exit 1
        fi
        
        # Install dependencies
        echo "Installing dependencies..."
        pip3.11 install -r requirements.txt
        
        # Run agent
        echo "Starting agent..."
        python3.11 agents/toga_hck/agent.py
        ;;
        
    "test")
        echo ""
        echo "Running TESTS..."
        
        # Build image
        docker-compose build
        
        # Run tests
        echo "Running unit tests..."
        docker-compose run --rm agent-zero-hck python3.11 -m pytest tests/ -v
        
        echo ""
        echo "Running integration tests..."
        docker-compose run --rm agent-zero-hck python3.11 agents/toga_hck/agent.py
        
        echo ""
        echo "✓ Tests complete!"
        ;;
        
    *)
        echo "ERROR: Unknown deployment mode: $DEPLOYMENT_MODE"
        echo ""
        echo "Usage: $0 [MODE]"
        echo ""
        echo "Modes:"
        echo "  standalone   - Deploy as standalone Docker container (default)"
        echo "  daedalos     - Deploy to Daedalos environment"
        echo "  development  - Run locally for development"
        echo "  test         - Run tests"
        echo ""
        echo "Environment variables:"
        echo "  ENABLE_ATOMSPACE=true   - Enable OpenCog AtomSpace"
        echo "  ENABLE_NPU=true         - Enable NPU coprocessor"
        echo "  ENABLE_DAEDALOS=true    - Enable Daedalos integration"
        exit 1
        ;;
esac

echo ""
echo "Ehehe~ ♡ Agent-Zero-HCK is ready to embrace cheerful chaos!"
