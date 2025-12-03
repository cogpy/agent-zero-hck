#!/bin/bash

# Deployment script for Agent Zero daedalOS Integration
# This script sets up and deploys the Agent Zero environment within daedalOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DAEDALOS_ENV="$PROJECT_ROOT/daedalos-env"
INTEGRATION_DIR="$PROJECT_ROOT/daedalos-integration"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    
    log_success "All prerequisites are installed"
}

# Setup directories
setup_directories() {
    log_info "Setting up directories..."
    
    mkdir -p "$PROJECT_ROOT/data/agent-zero"
    mkdir -p "$PROJECT_ROOT/data/daedalos"
    mkdir -p "$PROJECT_ROOT/logs"
    
    log_success "Directories created"
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."
    
    cd "$PROJECT_ROOT"
    
    docker-compose -f docker-compose.daedalos.yml build --no-cache
    
    log_success "Docker images built successfully"
}

# Start services
start_services() {
    log_info "Starting services..."
    
    cd "$PROJECT_ROOT"
    
    docker-compose -f docker-compose.daedalos.yml up -d
    
    log_success "Services started"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for daedalOS
    log_info "Waiting for daedalOS (port 3000)..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null; then
            log_success "daedalOS is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "daedalOS failed to start"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for Agent Zero API
    log_info "Waiting for Agent Zero API (port 8000)..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            log_success "Agent Zero API is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Agent Zero API failed to start"
            exit 1
        fi
        sleep 2
    done
}

# Display information
display_info() {
    log_info "Deployment complete!"
    
    echo ""
    echo -e "${BLUE}=== Service URLs ===${NC}"
    echo -e "daedalOS Desktop:     ${GREEN}http://localhost:3000${NC}"
    echo -e "Agent Zero API:       ${GREEN}http://localhost:8000${NC}"
    echo -e "API Documentation:    ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "WebSocket Endpoint:   ${GREEN}ws://localhost:8000/ws/agent/{agent_id}${NC}"
    echo ""
    
    echo -e "${BLUE}=== Useful Commands ===${NC}"
    echo "View logs:            docker-compose -f docker-compose.daedalos.yml logs -f"
    echo "Stop services:        docker-compose -f docker-compose.daedalos.yml down"
    echo "Restart services:     docker-compose -f docker-compose.daedalos.yml restart"
    echo ""
}

# Main execution
main() {
    log_info "Starting Agent Zero daedalOS deployment..."
    
    check_prerequisites
    setup_directories
    build_images
    start_services
    wait_for_services
    display_info
    
    log_success "Deployment completed successfully!"
}

# Run main function
main "$@"
