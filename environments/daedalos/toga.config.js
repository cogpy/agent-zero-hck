/**
 * Agent-Toga Configuration for DaedalOS
 * 
 * This configuration customizes DaedalOS to serve as the
 * Agent-Toga desktop environment with Live2D avatar integration.
 */

module.exports = {
  // Agent-Toga Identity
  agent: {
    name: "Toga",
    fullName: "Himiko Toga",
    version: "1.0.0",
    personality: "cheerful, playful, curious, mischievous",
  },

  // Desktop Environment Settings
  desktop: {
    // Custom wallpaper for Toga theme
    wallpaper: "/System/Toga/wallpaper.png",
    
    // Theme colors (Toga-inspired)
    theme: {
      primary: "#FFB6C1",      // Light pink
      secondary: "#FF69B4",    // Hot pink
      accent: "#DC143C",       // Crimson (blood red)
      background: "#1a1a2e",   // Dark background
      text: "#ffffff",
    },

    // Default applications to show
    defaultApps: [
      "Terminal",
      "FileExplorer",
      "Browser",
      "TogaChat",
      "TransformQuirk",
      "SecurityTester",
    ],
  },

  // Live2D Avatar Integration
  avatar: {
    enabled: true,
    modelPath: "/System/Toga/Live2D/toga_model.json",
    position: "bottom-right",
    size: {
      width: 300,
      height: 400,
    },
    defaultEmotion: "happy",
    idleAnimations: true,
  },

  // Agent-Zero Backend Integration
  backend: {
    apiUrl: process.env.AGENT_ZERO_API_URL || "http://localhost:8000",
    wsUrl: process.env.AGENT_ZERO_WS_URL || "ws://localhost:8000/api/v1/avatar/ws",
    endpoints: {
      chat: "/api/v1/avatar/chat/message",
      emotion: "/api/v1/avatar/emotion",
      animation: "/api/v1/avatar/animation",
      transform: "/api/v1/avatar/transform",
      session: "/api/v1/avatar/session",
    },
  },

  // Custom Applications for Toga
  customApps: {
    TogaChat: {
      name: "Toga Chat",
      icon: "/System/Toga/icons/chat.png",
      component: "TogaChatApp",
      description: "Chat with Agent-Toga",
    },
    TransformQuirk: {
      name: "Transform Quirk",
      icon: "/System/Toga/icons/transform.png",
      component: "TransformQuirkApp",
      description: "Toga's code absorption ability",
    },
    SecurityTester: {
      name: "Security Tester",
      icon: "/System/Toga/icons/security.png",
      component: "SecurityTesterApp",
      description: "Ethical security testing tools",
    },
    NPUMonitor: {
      name: "NPU Monitor",
      icon: "/System/Toga/icons/npu.png",
      component: "NPUMonitorApp",
      description: "Neural Processing Unit status",
    },
  },

  // File System Customizations
  fileSystem: {
    // Custom folders for Toga
    customFolders: [
      { path: "/System/Toga", name: "Toga System" },
      { path: "/Users/Toga/Documents", name: "Documents" },
      { path: "/Users/Toga/Projects", name: "Projects" },
      { path: "/Users/Toga/Absorbed", name: "Absorbed Code" },
    ],
  },

  // Startup Configuration
  startup: {
    // Show Toga greeting on startup
    showGreeting: true,
    greetingMessage: "Hey there! I'm Toga~ Ready to have some fun? 💕",
    
    // Auto-start applications
    autoStart: ["TogaChat"],
    
    // Play startup sound
    playSound: true,
    startupSound: "/System/Toga/sounds/startup.mp3",
  },

  // Security Settings
  security: {
    // Ethical constraints for Transform Quirk
    ethicalConstraints: true,
    
    // Require confirmation for sensitive operations
    confirmSensitiveOps: true,
    
    // Sandbox mode for security testing
    sandboxMode: true,
  },
};
