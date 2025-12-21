<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  
  // Props
  export let apiKey = 'dev-key';
  export let apiBaseUrl = '/api/avatar';
  export let visible = true;
  export let position = 'bottom-right'; // bottom-right, bottom-left, top-right, top-left
  
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
      
      const data = await response.json();
      sessionId = data.session_id;
      console.log('✅ Session created:', sessionId);
      
      // Connect WebSocket
      connectWebSocket();
    } catch (error) {
      console.error('❌ Failed to create session:', error);
    }
  }
  
  /**
   * Connect to the Avatar API WebSocket
   */
  function connectWebSocket() {
    if (!sessionId) return;
    
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
    
    sendMessage('chat', { message });
  }
  
  /**
   * Update avatar emotion
   */
  function updateAvatarEmotion(emotionData) {
    // This would update the Live2D model parameters
    // For now, we'll just log it
    console.log('😊 Emotion update:', emotionData);
    
    // TODO: Implement Live2D parameter updates
    // Example:
    // live2dModel.setParameterValue('ParamMouthForm', emotionData.parameters.ParamMouthForm);
  }
  
  /**
   * Play an animation
   */
  function playAnimation(animationData) {
    // This would trigger a Live2D animation
    console.log('🎬 Animation:', animationData);
    
    // TODO: Implement Live2D animation playback
    // Example:
    // live2dModel.playMotion(animationData.animation, animationData.intensity);
  }
  
  /**
   * Initialize the Live2D model
   */
  function initializeLive2D() {
    // TODO: Implement Live2D model loading
    // This is a placeholder for the actual Live2D integration
    
    console.log('🎨 Live2D initialization placeholder');
    
    // Example implementation would be:
    // 1. Load Live2D Cubism Core
    // 2. Load the model JSON
    // 3. Initialize the renderer
    // 4. Start the update loop
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
  });
  
  // Position classes
  const positionClasses = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
  };
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
          class="w-3 h-3 rounded-full {isConnected ? 'bg-green-500' : 'bg-red-500'}"
          title={isConnected ? 'Connected' : 'Disconnected'}
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
</style>
