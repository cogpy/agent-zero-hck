<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import togaConfig from '../../toga.config.js';
  
  // Import xterm only on client side to avoid SSR issues
  let Terminal, FitAddon, WebLinksAddon;
  if (browser) {
    import('@xterm/xterm').then(m => Terminal = m.Terminal);
    import('@xterm/addon-fit').then(m => FitAddon = m.FitAddon);
    import('@xterm/addon-web-links').then(m => WebLinksAddon = m.WebLinksAddon);
    import('@xterm/xterm/css/xterm.css');
  }
  
  export let configObj;
  export let processCallback = null;
  export let cacheId = "blocks_terminal";
  
  let terminalContainer;
  let avatarContainer;
  let terminal;
  let fitAddon;
  let processCount = 0;
  let avatarVisible = togaConfig.avatar.enabled;
  let currentEmotion = togaConfig.avatar.defaultEmotion;
  let wsConnection = null;
  
  // Avatar state management
  let avatarState = {
    emotion: 'happy',
    expression: 'default',
    isThinking: false,
    isSpeaking: false,
  };
  
  // Initialize terminal
  onMount(async () => {
    // Wait for xterm modules to load
    if (!Terminal || !FitAddon || !WebLinksAddon) {
      await new Promise(resolve => setTimeout(resolve, 100));
      if (!Terminal || !FitAddon || !WebLinksAddon) {
        console.error('Failed to load xterm modules');
        return;
      }
    }
    
    // Create terminal instance
    terminal = new Terminal({
      cursorBlink: true,
      fontSize: togaConfig.terminal.font.size,
      fontFamily: togaConfig.terminal.font.family,
      theme: {
        background: togaConfig.terminal.theme.background,
        foreground: togaConfig.terminal.theme.foreground,
        cursor: togaConfig.terminal.theme.cursor,
        selection: togaConfig.terminal.theme.selection,
        black: togaConfig.terminal.theme.colors.black,
        red: togaConfig.terminal.theme.colors.red,
        green: togaConfig.terminal.theme.colors.green,
        yellow: togaConfig.terminal.theme.colors.yellow,
        blue: togaConfig.terminal.theme.colors.blue,
        magenta: togaConfig.terminal.theme.colors.magenta,
        cyan: togaConfig.terminal.theme.colors.cyan,
        white: togaConfig.terminal.theme.colors.white,
      },
      allowProposedApi: true,
    });
    
    // Add addons
    fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.loadAddon(new WebLinksAddon());
    
    // Open terminal in container
    terminal.open(terminalContainer);
    fitAddon.fit();
    
    // Display MOTD
    displayMotd();
    
    // Initialize CheerpX if available
    if (typeof CheerpX !== 'undefined') {
      await initializeCheerpX();
    } else {
      // Fallback: display demo terminal
      initializeDemoTerminal();
    }
    
    // Initialize avatar WebSocket connection
    if (avatarVisible) {
      initializeAvatarConnection();
    }
    
    // Handle window resize
    window.addEventListener('resize', handleResize);
  });
  
  onDestroy(() => {
    if (terminal) {
      terminal.dispose();
    }
    if (wsConnection) {
      wsConnection.close();
    }
    window.removeEventListener('resize', handleResize);
  });
  
  function displayMotd() {
    terminal.writeln(togaConfig.startup.motd);
    terminal.writeln('');
    if (togaConfig.startup.showGreeting) {
      terminal.writeln(`\x1b[1;35m${togaConfig.startup.greetingMessage}\x1b[0m`);
      terminal.writeln('');
    }
  }
  
  async function initializeCheerpX() {
    try {
      // Initialize CheerpX WebVM
      const cx = await CheerpX.Linux.create({
        mounts: [
          { type: "ext2", url: "/images/debian_large.ext2", path: "/" },
          { type: "dir", path: "/tmp", name: "tmp" },
          { type: "dir", path: "/home/user", name: "home" },
        ],
        networkInterface: togaConfig.vm.network.enabled,
      });
      
      // Set up terminal I/O
      terminal.onData((data) => {
        cx.input(data);
      });
      
      cx.setCustomConsole(terminal.write.bind(terminal));
      
      // Run startup commands
      for (const cmd of togaConfig.startup.autoRun) {
        await cx.run("/bin/sh", ["-c", cmd]);
      }
      
      // Start shell
      await cx.run("/bin/bash", ["--login"], {
        env: [
          "HOME=/home/user",
          "USER=toga",
          "TERM=xterm-256color",
          `PS1=${togaConfig.terminal.prompt}`,
        ],
      });
      
      // Track process creation
      processCount++;
      if (processCallback) {
        processCallback(processCount);
      }
      
    } catch (error) {
      console.error("CheerpX initialization failed:", error);
      terminal.writeln(`\x1b[1;31mError: Failed to initialize VM: ${error.message}\x1b[0m`);
      initializeDemoTerminal();
    }
  }
  
  function initializeDemoTerminal() {
    // Demo terminal for development/testing
    terminal.writeln('\x1b[1;33mDemo Mode: CheerpX not available\x1b[0m');
    terminal.writeln('');
    terminal.write('$ ');
    
    let currentLine = '';
    
    terminal.onData((data) => {
      const code = data.charCodeAt(0);
      
      // Handle Enter key
      if (code === 13) {
        terminal.writeln('');
        if (currentLine.trim()) {
          handleDemoCommand(currentLine.trim());
          processCount++;
          if (processCallback) {
            processCallback(processCount);
          }
        }
        currentLine = '';
        terminal.write('$ ');
      }
      // Handle Backspace
      else if (code === 127) {
        if (currentLine.length > 0) {
          currentLine = currentLine.slice(0, -1);
          terminal.write('\b \b');
        }
      }
      // Handle printable characters
      else if (code >= 32) {
        currentLine += data;
        terminal.write(data);
      }
    });
  }
  
  function handleDemoCommand(cmd) {
    const commands = {
      'help': 'Available commands: help, toga-chat, toga-transform, toga-security, clear, ls, pwd',
      'toga-chat': '💕 Toga: Hey~ What do you want to talk about?',
      'toga-transform': '🔄 Transform Quirk Status: Ready to absorb!',
      'toga-security': '🔒 Security Testing Mode: Ethical constraints enabled',
      'clear': () => terminal.clear(),
      'ls': 'bin  etc  home  lib  tmp  usr  var',
      'pwd': '/home/toga',
      'whoami': 'toga',
      'uname': 'Linux toga-vm 5.15.0 #1 SMP x86_64 GNU/Linux',
    };
    
    if (cmd === 'clear') {
      terminal.clear();
      return;
    }
    
    const output = commands[cmd] || `bash: ${cmd}: command not found`;
    terminal.writeln(output);
    
    // Update avatar emotion based on command
    updateAvatarEmotion(cmd);
  }
  
  function initializeAvatarConnection() {
    try {
      wsConnection = new WebSocket(togaConfig.backend.wsUrl);
      
      wsConnection.onopen = () => {
        console.log('Avatar WebSocket connected');
        sendAvatarMessage({ type: 'init', config: togaConfig.avatar });
      };
      
      wsConnection.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleAvatarMessage(data);
      };
      
      wsConnection.onerror = (error) => {
        console.error('Avatar WebSocket error:', error);
      };
      
      wsConnection.onclose = () => {
        console.log('Avatar WebSocket disconnected');
        // Attempt reconnection after 5 seconds
        setTimeout(() => {
          if (avatarVisible) {
            initializeAvatarConnection();
          }
        }, 5000);
      };
    } catch (error) {
      console.error('Failed to initialize avatar connection:', error);
    }
  }
  
  function sendAvatarMessage(message) {
    if (wsConnection && wsConnection.readyState === WebSocket.OPEN) {
      wsConnection.send(JSON.stringify(message));
    }
  }
  
  function handleAvatarMessage(data) {
    switch (data.type) {
      case 'emotion':
        avatarState.emotion = data.emotion;
        currentEmotion = data.emotion;
        break;
      case 'expression':
        avatarState.expression = data.expression;
        break;
      case 'speak':
        avatarState.isSpeaking = true;
        setTimeout(() => {
          avatarState.isSpeaking = false;
        }, data.duration || 2000);
        break;
      case 'think':
        avatarState.isThinking = data.active;
        break;
    }
  }
  
  function updateAvatarEmotion(command) {
    let emotion = 'happy';
    
    if (command.includes('error') || command.includes('fail')) {
      emotion = 'sad';
    } else if (command.includes('toga')) {
      emotion = 'excited';
    } else if (command.includes('security') || command.includes('transform')) {
      emotion = 'curious';
    }
    
    sendAvatarMessage({ type: 'emotion', emotion });
  }
  
  function handleResize() {
    if (fitAddon) {
      fitAddon.fit();
    }
  }
  
  function toggleAvatar() {
    avatarVisible = !avatarVisible;
    if (avatarVisible && !wsConnection) {
      initializeAvatarConnection();
    }
  }
</script>

<style>
  .webvm-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    background: var(--bg-color, #1a1a2e);
    position: relative;
    overflow: hidden;
  }
  
  .terminal-wrapper {
    flex: 1;
    padding: 1rem;
    overflow: hidden;
  }
  
  .terminal-container {
    width: 100%;
    height: 100%;
  }
  
  .avatar-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 250px;
    height: 350px;
    z-index: 1000;
    pointer-events: none;
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  
  .avatar-container.hidden {
    opacity: 0;
    transform: translateY(100%);
  }
  
  .avatar-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(255, 105, 180, 0.3);
    pointer-events: auto;
  }
  
  .avatar-content {
    text-align: center;
    color: white;
    padding: 1rem;
  }
  
  .avatar-name {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .avatar-status {
    font-size: 0.9rem;
    opacity: 0.9;
  }
  
  .emotion-indicator {
    margin-top: 1rem;
    font-size: 2rem;
  }
  
  .avatar-toggle {
    position: fixed;
    bottom: 20px;
    left: 20px;
    padding: 0.5rem 1rem;
    background: #FF69B4;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    z-index: 1001;
    font-weight: 600;
    transition: background 0.2s ease;
  }
  
  .avatar-toggle:hover {
    background: #DC143C;
  }
  
  .slot-content {
    padding: 1rem;
    text-align: center;
    color: #FFB6C1;
  }
  
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>

<div class="webvm-container">
  <div class="terminal-wrapper">
    <div class="terminal-container" bind:this={terminalContainer}></div>
  </div>
  
  {#if togaConfig.avatar.showInTerminal}
    <div class="avatar-container" class:hidden={!avatarVisible} bind:this={avatarContainer}>
      <div class="avatar-placeholder">
        <div class="avatar-content">
          <div class="avatar-name">Toga</div>
          <div class="avatar-status">
            {avatarState.isThinking ? 'Thinking...' : avatarState.isSpeaking ? 'Speaking...' : 'Ready'}
          </div>
          <div class="emotion-indicator">
            {#if currentEmotion === 'happy'}
              😊
            {:else if currentEmotion === 'excited'}
              🤩
            {:else if currentEmotion === 'curious'}
              🤔
            {:else if currentEmotion === 'sad'}
              😢
            {:else}
              💕
            {/if}
          </div>
        </div>
      </div>
    </div>
    
    <button class="avatar-toggle" on:click={toggleAvatar}>
      {avatarVisible ? 'Hide' : 'Show'} Toga
    </button>
  {/if}
  
  <div class="slot-content">
    <slot></slot>
  </div>
</div>
