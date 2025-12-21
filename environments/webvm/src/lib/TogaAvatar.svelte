<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { MockLive2DModel, applyEmotion } from './live2d-mock.js';
  
  // Props
  export let apiKey = 'dev-key';
  export let apiBaseUrl = '/api/avatar';
  export let visible = true;
  export let position = 'bottom-right'; // bottom-right, bottom-left, top-right, top-left
  export let enableMockRenderer = true; // Use mock renderer for demonstration
  
  // State
  let sessionId = null;
  let ws = null;
  let currentEmotion = 'playful';
  let isConnected = false;
  let isSpeaking = false;
  let chatHistory = [];
  let currentResponse = '';
  
  // Avatar container
  let avatarContainer;
  let canvas;
  let live2dModel = null;
  let animationFrameId = null;
  let lastFrameTime = 0;
  
  /**
   * Initialize the Avatar API session
   */
  async function initializeSession() {
    try {
      const response = await fetch(`${apiBaseUrl}/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({
          initial_emotion: 'playful',
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to create session: ${response.statusText}`);
      }
      
      const data = await response.json();
      sessionId = data.session_id;
      console.log('✅ Session created:', sessionId);
      
      // Connect WebSocket
      connectWebSocket();
    } catch (error) {
      console.error('❌ Failed to create session:', error);
      // Continue with mock mode even if API is unavailable
      console.log('📝 Running in demo mode without API');
    }
  }
  
  /**
   * Connect to the Avatar API WebSocket
   */
  function connectWebSocket() {
    if (!sessionId) return;
    
    try {
      const wsUrl = new URL(`${apiBaseUrl}/ws/${sessionId}`, window.location.href);
      wsUrl.protocol = wsUrl.protocol.replace('http', 'ws');
      wsUrl.searchParams.set('api_key', apiKey);
      
      ws = new WebSocket(wsUrl.href);
      
      ws.onopen = () => {
        console.log('🔌 WebSocket connected');
        isConnected = true;
        
        // Start ping interval
        pingInterval = setInterval(() => {
          sendMessage('ping', {});
        }, 30000);
      };
      
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleWebSocketMessage(message);
      };
      
      ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        isConnected = false;
        clearInterval(pingInterval);
      };
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
      };
    } catch (error) {
      console.error('❌ Failed to connect WebSocket:', error);
    }
  }
  
  /**
   * Handle incoming WebSocket messages
   */
  function handleWebSocketMessage(message) {
    switch (message.type) {
      case 'connected':
        console.log('✅ Connected to avatar session');
        break;
        
      case 'chat_token':
        // Append token to current response
        currentResponse += message.data.token;
        isSpeaking = true;
        break;
        
      case 'chat_response':
        // Complete response received
        chatHistory = [...chatHistory, {
          sender: 'Toga',
          text: message.data.response,
        }];
        currentResponse = '';
        isSpeaking = false;
        break;
        
      case 'emotion_update':
        // Update emotion
        currentEmotion = message.data.emotion;
        updateAvatarEmotion(message.data);
        break;
        
      case 'animation_play':
        // Play animation
        playAnimation(message.data);
        break;
        
      case 'pong':
        // Heartbeat response
        break;
        
      case 'error':
        console.error('❌ Server error:', message.data.error);
        break;
    }
  }
  
  /**
   * Send a message over WebSocket
   */
  function sendMessage(type, data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type,
        data,
        session_id: sessionId,
      }));
    }
  }
  
  /**
   * Send a chat message
   */
  export function sendChat(message) {
    if (!message || !message.trim()) return;
    
    chatHistory = [...chatHistory, {
      sender: 'User',
      text: message,
    }];
    
    if (isConnected) {
      sendMessage('chat', { message });
    } else {
      // Demo mode: simulate response
      simulateDemoResponse(message);
    }
  }
  
  /**
   * Simulate a demo response (when API is unavailable)
   */
  function simulateDemoResponse(message) {
    setTimeout(() => {
      const responses = [
        "Hey hey! I'm Toga! This is a demo mode!",
        "Wow, that's so cool! I love it!",
        "Hehe, you're making me blush! 💕",
        "Let's have some fun together!",
        "I'm so excited to talk to you!",
      ];
      
      const response = responses[Math.floor(Math.random() * responses.length)];
      
      chatHistory = [...chatHistory, {
        sender: 'Toga',
        text: response,
      }];
      
      // Trigger random emotion
      const emotions = ['happy', 'excited', 'playful', 'shy'];
      const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
      updateAvatarEmotion({ emotion: randomEmotion, intensity: 0.8 });
      
      // Trigger random animation
      const animations = ['wave', 'bounce', 'nod'];
      const randomAnimation = animations[Math.floor(Math.random() * animations.length)];
      playAnimation({ animation: randomAnimation, intensity: 0.7 });
    }, 500);
  }
  
  /**
   * Update avatar emotion
   */
  function updateAvatarEmotion(emotionData) {
    const { emotion, intensity = 0.8 } = emotionData;
    
    console.log('😊 Emotion update:', emotion, intensity);
    
    if (live2dModel) {
      applyEmotion(live2dModel, emotion, intensity);
    }
  }
  
  /**
   * Play an animation
   */
  function playAnimation(animationData) {
    const { animation, intensity = 0.7, duration_ms = 1000 } = animationData;
    
    console.log('🎬 Animation:', animation, intensity);
    
    if (live2dModel) {
      live2dModel.playAnimation(animation, intensity, duration_ms);
    }
  }
  
  /**
   * Initialize the Live2D model
   */
  async function initializeLive2D() {
    if (!canvas) {
      console.error('Canvas not ready');
      return;
    }
    
    console.log('🎨 Initializing Live2D...');
    
    if (enableMockRenderer) {
      // Use mock renderer for demonstration
      live2dModel = new MockLive2DModel(canvas);
      await live2dModel.load('/models/toga/toga.model3.json');
      
      // Set initial emotion
      applyEmotion(live2dModel, currentEmotion, 0.8);
      
      // Start render loop
      startRenderLoop();
      
      console.log('✅ Mock Live2D initialized');
    } else {
      // TODO: Implement actual Live2D SDK integration
      console.warn('⚠️ Real Live2D SDK not implemented yet');
    }
  }
  
  /**
   * Start the rendering loop
   */
  function startRenderLoop() {
    const render = (timestamp) => {
      if (!live2dModel) return;
      
      const deltaTime = timestamp - lastFrameTime;
      lastFrameTime = timestamp;
      
      // Update model
      live2dModel.update(deltaTime);
      
      // Render model
      live2dModel.render();
      
      // Continue loop
      animationFrameId = requestAnimationFrame(render);
    };
    
    animationFrameId = requestAnimationFrame(render);
  }
  
  let pingInterval;
  
  onMount(() => {
    if (browser) {
      initializeSession();
      initializeLive2D();
    }
  });
  
  onDestroy(() => {
    if (ws) {
      ws.close();
    }
    if (pingInterval) {
      clearInterval(pingInterval);
    }
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
    }
  });
  
  // Position classes
  const positionClasses = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
  };
  
  // Demo controls
  function testEmotion(emotion) {
    updateAvatarEmotion({ emotion, intensity: 0.8 });
  }
  
  function testAnimation(animation) {
    playAnimation({ animation, intensity: 0.7, duration_ms: 1000 });
  }
</script>

{#if visible}
  <div 
    class="toga-avatar fixed {positionClasses[position]} z-50"
    bind:this={avatarContainer}
  >
    <!-- Live2D Canvas -->
    <div class="avatar-canvas-container relative">
      <canvas 
        bind:this={canvas}
        width="400"
        height="600"
        class="rounded-lg shadow-2xl"
      ></canvas>
      
      <!-- Status indicator -->
      <div class="absolute top-2 right-2">
        <div 
          class="w-3 h-3 rounded-full {isConnected ? 'bg-green-500' : 'bg-yellow-500'}"
          title={isConnected ? 'Connected' : 'Demo Mode'}
        ></div>
      </div>
      
      <!-- Emotion indicator -->
      <div class="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-xs">
        {currentEmotion}
      </div>
      
      <!-- Speaking indicator -->
      {#if isSpeaking}
        <div class="absolute bottom-2 right-2 bg-pink-500 text-white px-2 py-1 rounded text-xs animate-pulse">
          Speaking...
        </div>
      {/if}
    </div>
    
    <!-- Demo Controls -->
    <div class="mt-2 bg-white rounded-lg shadow-lg p-3 max-w-sm">
      <div class="text-xs font-bold mb-2">Demo Controls</div>
      
      <div class="mb-2">
        <div class="text-xs mb-1">Emotions:</div>
        <div class="flex flex-wrap gap-1">
          <button on:click={() => testEmotion('happy')} class="px-2 py-1 bg-yellow-200 rounded text-xs">Happy</button>
          <button on:click={() => testEmotion('excited')} class="px-2 py-1 bg-pink-200 rounded text-xs">Excited</button>
          <button on:click={() => testEmotion('playful')} class="px-2 py-1 bg-purple-200 rounded text-xs">Playful</button>
          <button on:click={() => testEmotion('shy')} class="px-2 py-1 bg-blue-200 rounded text-xs">Shy</button>
        </div>
      </div>
      
      <div>
        <div class="text-xs mb-1">Animations:</div>
        <div class="flex flex-wrap gap-1">
          <button on:click={() => testAnimation('wave')} class="px-2 py-1 bg-green-200 rounded text-xs">Wave</button>
          <button on:click={() => testAnimation('bounce')} class="px-2 py-1 bg-orange-200 rounded text-xs">Bounce</button>
          <button on:click={() => testAnimation('nod')} class="px-2 py-1 bg-teal-200 rounded text-xs">Nod</button>
        </div>
      </div>
    </div>
    
    <!-- Current response bubble (if speaking) -->
    {#if currentResponse}
      <div class="mt-2 bg-white rounded-lg shadow-lg p-3 max-w-sm">
        <p class="text-sm">{currentResponse}</p>
      </div>
    {/if}
  </div>
{/if}

<style>
  .toga-avatar {
    pointer-events: auto;
  }
  
  .avatar-canvas-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 0.5rem;
    padding: 0.5rem;
  }
  
  canvas {
    display: block;
    background: rgba(255, 255, 255, 0.1);
  }
  
  button {
    transition: transform 0.1s;
  }
  
  button:hover {
    transform: scale(1.05);
  }
  
  button:active {
    transform: scale(0.95);
  }
</style>
