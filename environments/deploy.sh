#!/bin/bash
# Agent-Toga Environment Deployment Script
# Deploys DaedalOS and/or WebVM environments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PINK='\033[1;35m'
NC='\033[0m' # No Color

# Print banner
print_banner() {
    echo -e "${PINK}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║   ████████╗ ██████╗  ██████╗  █████╗                        ║"
    echo "║   ╚══██╔══╝██╔═══██╗██╔════╝ ██╔══██╗                       ║"
    echo "║      ██║   ██║   ██║██║  ███╗███████║                       ║"
    echo "║      ██║   ██║   ██║██║   ██║██╔══██║                       ║"
    echo "║      ██║   ╚██████╔╝╚██████╔╝██║  ██║                       ║"
    echo "║      ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝                       ║"
    echo "║                                                              ║"
    echo "║   Agent-Toga Environment Deployment                          ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print usage
usage() {
    echo "Usage: $0 [OPTIONS] [ENVIRONMENT]"
    echo ""
    echo "Environments:"
    echo "  daedalos    Deploy DaedalOS desktop environment"
    echo "  webvm       Deploy WebVM virtual machine environment"
    echo "  all         Deploy all environments"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help message"
    echo "  -d, --dev       Run in development mode"
    echo "  -p, --prod      Build for production"
    echo "  -c, --clean     Clean build artifacts before building"
    echo "  --port PORT     Specify port (default: 3000 for daedalos, 5173 for webvm)"
    echo ""
    echo "Examples:"
    echo "  $0 daedalos -d           # Run DaedalOS in dev mode"
    echo "  $0 webvm -p              # Build WebVM for production"
    echo "  $0 all -c -p             # Clean and build all for production"
}

# Deploy DaedalOS
deploy_daedalos() {
    local mode=$1
    local port=${2:-3000}
    
    echo -e "${PINK}[Toga]${NC} Deploying DaedalOS environment..."
    cd "$SCRIPT_DIR/daedalos"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing dependencies...${NC}"
        yarn install
    fi
    
    if [ "$mode" == "dev" ]; then
        echo -e "${GREEN}Starting DaedalOS in development mode on port $port...${NC}"
        yarn dev -p $port
    else
        echo -e "${GREEN}Building DaedalOS for production...${NC}"
        yarn build
        echo -e "${GREEN}Build complete! Output in 'out' directory.${NC}"
    fi
}

# Deploy WebVM
deploy_webvm() {
    local mode=$1
    local port=${2:-5173}
    
    echo -e "${PINK}[Toga]${NC} Deploying WebVM environment..."
    cd "$SCRIPT_DIR/webvm"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing dependencies...${NC}"
        npm install
    fi
    
    if [ "$mode" == "dev" ]; then
        echo -e "${GREEN}Starting WebVM in development mode on port $port...${NC}"
        npm run dev -- --port $port
    else
        echo -e "${GREEN}Building WebVM for production...${NC}"
        npm run build
        echo -e "${GREEN}Build complete! Output in 'build' directory.${NC}"
    fi
}

# Clean build artifacts
clean() {
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    
    # Clean DaedalOS
    if [ -d "$SCRIPT_DIR/daedalos" ]; then
        rm -rf "$SCRIPT_DIR/daedalos/.next"
        rm -rf "$SCRIPT_DIR/daedalos/out"
        rm -rf "$SCRIPT_DIR/daedalos/node_modules"
    fi
    
    # Clean WebVM
    if [ -d "$SCRIPT_DIR/webvm" ]; then
        rm -rf "$SCRIPT_DIR/webvm/build"
        rm -rf "$SCRIPT_DIR/webvm/node_modules"
    fi
    
    echo -e "${GREEN}Clean complete!${NC}"
}

# Main
main() {
    print_banner
    
    local environment=""
    local mode="prod"
    local port=""
    local do_clean=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -d|--dev)
                mode="dev"
                shift
                ;;
            -p|--prod)
                mode="prod"
                shift
                ;;
            -c|--clean)
                do_clean=true
                shift
                ;;
            --port)
                port="$2"
                shift 2
                ;;
            daedalos|webvm|all)
                environment="$1"
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                usage
                exit 1
                ;;
        esac
    done
    
    # Default to all if no environment specified
    if [ -z "$environment" ]; then
        environment="all"
    fi
    
    # Clean if requested
    if [ "$do_clean" = true ]; then
        clean
    fi
    
    # Deploy based on environment
    case $environment in
        daedalos)
            deploy_daedalos "$mode" "$port"
            ;;
        webvm)
            deploy_webvm "$mode" "$port"
            ;;
        all)
            if [ "$mode" == "dev" ]; then
                echo -e "${YELLOW}Note: Running both in dev mode. DaedalOS on 3000, WebVM on 5173${NC}"
                # Start both in background
                deploy_daedalos "$mode" "3000" &
                deploy_webvm "$mode" "5173" &
                wait
            else
                deploy_daedalos "$mode"
                deploy_webvm "$mode"
            fi
            ;;
    esac
    
    echo -e "${PINK}[Toga]${NC} Deployment complete! Have fun~ 💕"
}

main "$@"
