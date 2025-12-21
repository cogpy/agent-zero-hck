# Agent-Toga Environments

This directory contains pre-configured deployment environments for Agent-Toga, providing both a desktop environment (DaedalOS) and a virtual machine environment (WebVM).

## Overview

| Environment | Description | Port | Use Case |
|-------------|-------------|------|----------|
| **DaedalOS** | Web-based desktop environment | 3000 | Full desktop experience with Live2D avatar |
| **WebVM** | Browser-based Linux VM | 5173 | Terminal-based interaction with full Linux |

## Quick Start

### Using the Deploy Script

```bash
# Deploy DaedalOS in development mode
./deploy.sh daedalos -d

# Deploy WebVM in development mode
./deploy.sh webvm -d

# Build all environments for production
./deploy.sh all -p

# Clean and rebuild everything
./deploy.sh all -c -p
```

### Using Docker Compose

```bash
# Start all services
docker compose up -d

# Start with Traefik proxy
docker compose --profile with-proxy up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## DaedalOS Environment

DaedalOS provides a complete web-based desktop environment with:

- **File Explorer** - Browse and manage files
- **Terminal** - Command-line interface
- **Browser** - Built-in web browser
- **Toga Chat** - Chat with Agent-Toga
- **Transform Quirk** - Code absorption interface
- **Security Tester** - Ethical security testing tools

### Configuration

Edit `daedalos/toga.config.js` to customize:

```javascript
module.exports = {
  agent: {
    name: "Toga",
    personality: "cheerful, playful, curious, mischievous",
  },
  desktop: {
    theme: {
      primary: "#FFB6C1",
      secondary: "#FF69B4",
    },
  },
  avatar: {
    enabled: true,
    position: "bottom-right",
  },
};
```

### Directory Structure

```
daedalos/
├── public/
│   ├── System/
│   │   └── Toga/
│   │       ├── Live2D/      # Live2D model files
│   │       ├── icons/       # Custom icons
│   │       ├── sounds/      # Sound effects
│   │       └── wallpapers/  # Wallpaper images
│   └── Users/
│       └── Toga/
│           ├── Documents/
│           ├── Projects/
│           └── Absorbed/    # Absorbed code storage
├── components/              # React components
├── contexts/                # React contexts
└── toga.config.js           # Toga configuration
```

## WebVM Environment

WebVM provides a full Linux virtual machine running in the browser:

- **Alpine Linux** - Lightweight Linux distribution
- **Terminal** - Full terminal emulator with xterm.js
- **Python/Node.js** - Pre-installed development tools
- **Agent-Toga CLI** - Command-line tools for Toga interaction

### Configuration

Edit `webvm/toga.config.js` to customize:

```javascript
export default {
  vm: {
    image: "toga-alpine",
    memory: 512,
    cpuCores: 2,
  },
  terminal: {
    theme: {
      background: "#1a1a2e",
      foreground: "#ffffff",
      cursor: "#FF69B4",
    },
  },
  avatar: {
    enabled: true,
    showInTerminal: true,
  },
};
```

### Pre-installed Tools

| Tool | Description |
|------|-------------|
| `toga-chat` | Chat with Agent-Toga from terminal |
| `toga-transform` | Transform quirk CLI interface |
| `toga-security` | Security testing tools |
| `toga-npu` | NPU status and control |

### Directory Structure

```
webvm/
├── assets/
│   └── toga/
│       ├── Live2D/      # Live2D model files
│       ├── icons/       # Custom icons
│       └── sounds/      # Sound effects
├── src/                 # Svelte source files
├── dockerfiles/         # Docker configurations
└── toga.config.js       # Toga configuration
```

## Integration with Agent-Zero

Both environments connect to the Agent-Zero backend API:

```
┌─────────────────┐     ┌─────────────────┐
│    DaedalOS     │     │     WebVM       │
│  (Desktop UI)   │     │  (Terminal UI)  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │    Agent-Zero API     │
         │   (FastAPI Backend)   │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  NPU Coprocessor│     │ Toga Personality│
└─────────────────┘     └─────────────────┘
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/avatar/chat/message` | Send message to Toga |
| `GET /api/v1/avatar/emotion/{id}/state` | Get current emotion |
| `POST /api/v1/avatar/transform/{id}/absorb` | Absorb code |
| `WS /api/v1/avatar/ws/{id}` | Real-time WebSocket |

## Live2D Avatar

Both environments support the Live2D avatar. To add your custom Toga model:

1. Export your Live2D model (model3.json format)
2. Place files in the appropriate directory:
   - DaedalOS: `daedalos/public/System/Toga/Live2D/`
   - WebVM: `webvm/assets/toga/Live2D/`
3. Update the configuration to point to your model

### Required Files

```
Live2D/
├── toga_model.model3.json    # Main model file
├── toga_model.moc3           # Motion data
├── toga_model.physics3.json  # Physics settings
├── textures/                 # Texture files
│   └── texture_00.png
└── motions/                  # Animation files
    ├── idle.motion3.json
    ├── happy.motion3.json
    └── ...
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENT_ZERO_API_URL` | Backend API URL | `http://localhost:8000` |
| `AGENT_ZERO_WS_URL` | WebSocket URL | `ws://localhost:8000/api/v1/avatar/ws` |
| `OPENAI_API_KEY` | OpenAI API key for NPU | Required |
| `NODE_ENV` | Environment mode | `development` |

## Deployment Options

### Local Development

```bash
# Terminal 1: Start Agent-Zero backend
cd .. && uvicorn python.api.avatar.main:app --reload --port 8000

# Terminal 2: Start DaedalOS
./deploy.sh daedalos -d

# Terminal 3: Start WebVM
./deploy.sh webvm -d
```

### Docker Production

```bash
# Build and start all services
docker compose up -d --build

# With Traefik for domain routing
docker compose --profile with-proxy up -d
```

### Cloud Deployment

Both environments can be deployed to:

- **Vercel** - DaedalOS (Next.js)
- **Netlify** - WebVM (Static)
- **Cloudflare Pages** - Both environments
- **AWS/GCP/Azure** - Docker containers

## Troubleshooting

### DaedalOS won't start

```bash
# Clear cache and reinstall
cd daedalos
rm -rf node_modules .next
yarn install
yarn dev
```

### WebVM build fails

```bash
# Clear cache and reinstall
cd webvm
rm -rf node_modules build
npm install
npm run dev
```

### Avatar not showing

1. Check that Live2D model files exist
2. Verify model path in configuration
3. Check browser console for errors
4. Ensure CORS is configured correctly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

- **DaedalOS**: MIT License (Dustin Brett)
- **WebVM**: Apache 2.0 License (Leaning Technologies)
- **Agent-Toga Integration**: MIT License
