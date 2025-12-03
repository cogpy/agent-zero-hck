# Agent Zero daedalOS Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying Agent Zero within the daedalOS virtual desktop environment. The integration enables Agent Zero to run as an operational environment within daedalOS, providing a unified interface for AI-powered automation.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Accessing Services](#accessing-services)
6. [API Documentation](#api-documentation)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2)
- **Docker**: 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Git**: 2.30+ ([Install Git](https://git-scm.com/downloads))
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk Space**: Minimum 5GB free space

### Software Verification

```bash
# Verify Docker installation
docker --version
# Expected: Docker version 20.10.0 or higher

# Verify Docker Compose installation
docker-compose --version
# Expected: Docker Compose version 2.0.0 or higher

# Verify Git installation
git --version
# Expected: git version 2.30.0 or higher
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/cogpy/agent-zero-hck.git
cd agent-zero-hck
```

### 2. Run Deployment Script

```bash
# Make script executable
chmod +x scripts/deploy-daedalos.sh

# Run deployment
./scripts/deploy-daedalos.sh
```

### 3. Access Services

- **daedalOS Desktop**: http://localhost:3000
- **Agent Zero API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Configuration

### Environment Setup

1. **Copy configuration template**:
   ```bash
   cp .env.daedalos.example .env.daedalos
   ```

2. **Edit configuration** (optional):
   ```bash
   nano .env.daedalos
   ```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_ZERO_API_URL` | `http://localhost:8000` | API server URL |
| `AGENT_ZERO_WS_URL` | `ws://localhost:8000` | WebSocket server URL |
| `AGENT_ZERO_PORT` | `8000` | API server port |
| `DAEDALOS_PORT` | `3000` | daedalOS port |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `ENABLE_MEMORY_PERSISTENCE` | `true` | Enable memory persistence |
| `ENABLE_KNOWLEDGE_BASE` | `true` | Enable knowledge base |
| `ENABLE_FILE_OPERATIONS` | `true` | Enable file operations |

## Deployment

### Manual Deployment

#### Step 1: Build Docker Images

```bash
cd agent-zero-hck
docker-compose -f docker-compose.daedalos.yml build
```

#### Step 2: Start Services

```bash
docker-compose -f docker-compose.daedalos.yml up -d
```

#### Step 3: Verify Services

```bash
# Check running containers
docker-compose -f docker-compose.daedalos.yml ps

# View logs
docker-compose -f docker-compose.daedalos.yml logs -f
```

### Automated Deployment

```bash
./scripts/deploy-daedalos.sh
```

The script will:
1. Check prerequisites
2. Create necessary directories
3. Build Docker images
4. Start services
5. Wait for services to be ready
6. Display access information

## Accessing Services

### daedalOS Desktop

**URL**: http://localhost:3000

The daedalOS desktop provides:
- File explorer with virtual file system
- Terminal emulator
- Text editor
- Browser
- Various applications

### Agent Zero API

**URL**: http://localhost:8000

**API Documentation**: http://localhost:8000/docs (Swagger UI)

**Alternative Docs**: http://localhost:8000/redoc (ReDoc)

### WebSocket Connection

**URL**: `ws://localhost:8000/ws/agent/{agent_id}`

Example WebSocket connection:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/agent/default');

ws.onopen = () => {
    console.log('Connected to Agent Zero');
    ws.send(JSON.stringify({
        type: 'message',
        content: 'Hello Agent Zero!'
    }));
};

ws.onmessage = (event) => {
    console.log('Message from agent:', event.data);
};
```

## API Documentation

### File Operations

#### List Files
```bash
curl http://localhost:8000/api/files/list?path=.
```

#### Read File
```bash
curl http://localhost:8000/api/files/read?path=prompts/default.md
```

#### Create File
```bash
curl -X POST http://localhost:8000/api/files/create \
  -H "Content-Type: application/json" \
  -d '{
    "path": "test.txt",
    "content": "Hello World"
  }'
```

#### Delete File
```bash
curl -X DELETE http://localhost:8000/api/files/delete?path=test.txt
```

### Memory Management

#### Get Memory
```bash
curl http://localhost:8000/api/memory
```

#### Save Memory
```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Content-Type: application/json" \
  -d '{
    "key": "value"
  }'
```

### Knowledge Base

#### Get Knowledge
```bash
curl http://localhost:8000/api/knowledge
```

#### Save Knowledge
```bash
curl -X POST http://localhost:8000/api/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "information"
  }'
```

### Configuration

#### Get Config
```bash
curl http://localhost:8000/api/config
```

#### Save Config
```bash
curl -X POST http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "setting": "value"
  }'
```

### System Information

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Storage Info
```bash
curl http://localhost:8000/api/storage
```

#### Active Agents
```bash
curl http://localhost:8000/agents
```

## Troubleshooting

### Services Won't Start

**Problem**: Docker containers fail to start

**Solution**:
```bash
# Check Docker daemon
docker ps

# Check logs
docker-compose -f docker-compose.daedalos.yml logs

# Rebuild images
docker-compose -f docker-compose.daedalos.yml build --no-cache
```

### Port Already in Use

**Problem**: Port 3000 or 8000 is already in use

**Solution**:
```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different ports in docker-compose.daedalos.yml
```

### Connection Refused

**Problem**: Cannot connect to services

**Solution**:
```bash
# Wait for services to start
sleep 10

# Check if services are running
docker-compose -f docker-compose.daedalos.yml ps

# Restart services
docker-compose -f docker-compose.daedalos.yml restart
```

### Memory Issues

**Problem**: Out of memory errors

**Solution**:
```bash
# Increase Docker memory limit
# Edit Docker Desktop settings or docker daemon.json

# Clean up unused containers and images
docker system prune -a
```

### WebSocket Connection Failed

**Problem**: Cannot connect to WebSocket

**Solution**:
```bash
# Check if API is running
curl http://localhost:8000/health

# Check WebSocket endpoint
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
  http://localhost:8000/ws/agent/default
```

## Advanced Configuration

### Custom Port Mapping

Edit `docker-compose.daedalos.yml`:

```yaml
services:
  daedalos:
    ports:
      - "3001:3000"  # Map to port 3001
  
  agent-zero-api:
    ports:
      - "8001:8000"  # Map to port 8001
```

### Enable Redis Caching

Redis is optional but recommended for production:

```bash
# Verify Redis is running
docker-compose -f docker-compose.daedalos.yml ps redis

# Connect to Redis
docker exec -it agent-zero-redis redis-cli
```

### Custom Storage Backend

Modify `daedalos-integration/filesystem/adapter.py` to support:
- Cloud storage (S3, Azure Blob)
- Database backends
- Network file systems

### SSL/TLS Configuration

For production deployment:

1. Generate certificates:
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```

2. Update docker-compose to use certificates

3. Configure HTTPS in FastAPI

### Monitoring and Logging

View real-time logs:
```bash
# All services
docker-compose -f docker-compose.daedalos.yml logs -f

# Specific service
docker-compose -f docker-compose.daedalos.yml logs -f agent-zero-api

# Follow logs with timestamps
docker-compose -f docker-compose.daedalos.yml logs -f --timestamps
```

### Performance Optimization

1. **Increase resource limits**:
   ```yaml
   services:
     agent-zero-api:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

2. **Enable caching**:
   - Redis for session caching
   - File system caching for frequently accessed files

3. **Optimize database queries**:
   - Add indexes to frequently queried fields
   - Use connection pooling

## Maintenance

### Regular Tasks

```bash
# Daily: Check service health
docker-compose -f docker-compose.daedalos.yml ps

# Weekly: Clean up logs
docker system prune

# Monthly: Update images
docker-compose -f docker-compose.daedalos.yml pull
docker-compose -f docker-compose.daedalos.yml up -d
```

### Backup and Restore

```bash
# Backup data volumes
docker run --rm -v agent-zero-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/agent-zero-backup.tar.gz -C /data .

# Restore from backup
docker run --rm -v agent-zero-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/agent-zero-backup.tar.gz -C /data
```

### Stopping Services

```bash
# Stop all services
docker-compose -f docker-compose.daedalos.yml down

# Stop and remove volumes
docker-compose -f docker-compose.daedalos.yml down -v

# Stop and remove everything
docker-compose -f docker-compose.daedalos.yml down -v --remove-orphans
```

## Security Considerations

### Production Deployment

1. **Use environment variables** for sensitive data
2. **Enable CORS restrictions** for API access
3. **Implement authentication** for API endpoints
4. **Use HTTPS/WSS** for encrypted communication
5. **Regular security updates** for dependencies
6. **Monitor access logs** for suspicious activity

### Network Security

```yaml
# Restrict network access
networks:
  agent-zero-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-agent-zero
```

## Support and Resources

- **Documentation**: See `DAEDALOS_INTEGRATION.md`
- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: https://github.com/cogpy/agent-zero-hck/issues
- **daedalOS**: https://github.com/DustinBrett/daedalOS

## Next Steps

1. **Explore daedalOS**: Open http://localhost:3000
2. **Test API**: Visit http://localhost:8000/docs
3. **Create Agent**: Initialize your first agent
4. **Configure Memory**: Set up agent memory persistence
5. **Deploy Applications**: Add custom applications to daedalOS

---

**Document Version**: 1.0
**Last Updated**: December 3, 2025
**Status**: Production Ready
