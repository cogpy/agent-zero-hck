/**
 * Agent-Toga Configuration for WebVM
 * 
 * This configuration customizes WebVM to serve as the
 * Agent-Toga virtual machine environment with full Linux capabilities.
 */

export default {
  // Agent-Toga Identity
  agent: {
    name: "Toga",
    fullName: "Himiko Toga",
    version: "1.0.0",
    personality: "cheerful, playful, curious, mischievous",
  },

  // VM Configuration
  vm: {
    // Base image configuration
    image: "toga-alpine",
    
    // Memory allocation (in MB)
    memory: 512,
    
    // CPU cores
    cpuCores: 2,
    
    // Network configuration
    network: {
      enabled: true,
      hostname: "toga-vm",
    },
  },

  // Terminal Configuration
  terminal: {
    // Custom prompt for Toga
    prompt: "\\[\\033[1;35m\\]toga\\[\\033[0m\\]@\\[\\033[1;31m\\]vm\\[\\033[0m\\]:\\w$ ",
    
    // Theme colors
    theme: {
      background: "#1a1a2e",
      foreground: "#ffffff",
      cursor: "#FF69B4",
      selection: "#FFB6C1",
      colors: {
        black: "#1a1a2e",
        red: "#DC143C",
        green: "#98FB98",
        yellow: "#FFD700",
        blue: "#87CEEB",
        magenta: "#FF69B4",
        cyan: "#00CED1",
        white: "#ffffff",
      },
    },
    
    // Font settings
    font: {
      family: "JetBrains Mono, monospace",
      size: 14,
    },
  },

  // Agent-Zero Backend Integration
  backend: {
    apiUrl: import.meta.env?.VITE_AGENT_ZERO_API_URL || "http://localhost:8000",
    wsUrl: import.meta.env?.VITE_AGENT_ZERO_WS_URL || "ws://localhost:8000/api/v1/avatar/ws",
    endpoints: {
      chat: "/api/v1/avatar/chat/message",
      emotion: "/api/v1/avatar/emotion",
      transform: "/api/v1/avatar/transform",
      session: "/api/v1/avatar/session",
    },
  },

  // Live2D Avatar Integration
  avatar: {
    enabled: true,
    modelPath: "/assets/toga/Live2D/toga_model.json",
    position: "bottom-right",
    size: {
      width: 250,
      height: 350,
    },
    defaultEmotion: "happy",
    idleAnimations: true,
    
    // Show avatar in terminal mode
    showInTerminal: true,
  },

  // Pre-installed Tools
  tools: {
    // Agent-Zero CLI tools
    agentZero: {
      installed: true,
      commands: [
        "toga-chat",      // Chat with Toga
        "toga-transform", // Transform quirk CLI
        "toga-security",  // Security testing tools
        "toga-npu",       // NPU status and control
      ],
    },
    
    // Development tools
    development: {
      python: true,
      nodejs: true,
      git: true,
      vim: true,
    },
    
    // Security tools (ethical)
    security: {
      nmap: true,
      curl: true,
      openssl: true,
    },
  },

  // Startup Configuration
  startup: {
    // Custom MOTD (Message of the Day)
    motd: `
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ████████╗ ██████╗  ██████╗  █████╗                        ║
║   ╚══██╔══╝██╔═══██╗██╔════╝ ██╔══██╗                       ║
║      ██║   ██║   ██║██║  ███╗███████║                       ║
║      ██║   ██║   ██║██║   ██║██╔══██║                       ║
║      ██║   ╚██████╔╝╚██████╔╝██║  ██║                       ║
║      ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝                       ║
║                                                              ║
║   Agent-Toga VM - Himiko Toga Cognitive Kernel               ║
║   Type 'toga-help' for available commands                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
`,
    
    // Auto-run commands on startup
    autoRun: [
      "export PS1='\\[\\033[1;35m\\]toga\\[\\033[0m\\]@\\[\\033[1;31m\\]vm\\[\\033[0m\\]:\\w$ '",
    ],
    
    // Show greeting
    showGreeting: true,
    greetingMessage: "Hey~ Welcome to my VM! Let's have some fun! 💕",
  },

  // Security Settings
  security: {
    // Ethical constraints
    ethicalConstraints: true,
    
    // Sandbox mode
    sandboxMode: true,
    
    // Network restrictions
    networkRestrictions: {
      allowOutbound: true,
      allowInbound: false,
      blockedPorts: [22, 23, 25],
    },
  },

  // Persistence Configuration
  persistence: {
    // Enable persistent storage
    enabled: true,
    
    // Storage location
    storageKey: "toga-vm-storage",
    
    // Auto-save interval (ms)
    autoSaveInterval: 30000,
  },
};
