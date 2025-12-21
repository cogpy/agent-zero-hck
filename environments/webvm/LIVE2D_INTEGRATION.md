# Live2D Avatar Integration Guide

## Overview

This document describes the integration of the Agent-Toga Live2D Avatar into the WebVM environment.

## Components

### 1. TogaAvatar.svelte

The main Svelte component that renders the Live2D avatar and handles API communication.

**Features:**
- WebSocket connection to Avatar API
- Real-time emotion updates
- Animation playback
- Chat integration
- Responsive positioning

**Usage:**

```svelte
<script>
  import TogaAvatar from '$lib/TogaAvatar.svelte';
  
  let avatarRef;
  
  function sendMessage() {
    avatarRef.sendChat("Hello Toga!");
  }
</script>

<TogaAvatar 
  bind:this={avatarRef}
  apiKey="your-api-key"
  apiBaseUrl="/api/avatar"
  position="bottom-right"
  visible={true}
/>
```

### 2. avatar-api-client.js

A JavaScript client for interacting with the Avatar API.

**Features:**
- Session management
- WebSocket connection handling
- Event-based message handling
- Automatic reconnection

**Usage:**

```javascript
import { AvatarApiClient } from '$lib/avatar-api-client.js';

const client = new AvatarApiClient('your-api-key');

// Create session
await client.createSession();

// Register handlers
client.on('emotion_update', (data) => {
  console.log('Emotion:', data.emotion);
});

// Connect WebSocket
client.connectWebSocket((message) => {
  console.log('Message:', message);
});

// Send chat
client.sendChat('Hello!');
```

## Live2D SDK Integration

### Current Status

The components are ready for Live2D SDK integration. The following placeholders need to be implemented:

1. **Model Loading**: Load the Live2D model from a .model3.json file
2. **Parameter Updates**: Map emotion data to Live2D parameters
3. **Animation Playback**: Trigger Live2D motions based on API events
4. **Rendering Loop**: Implement the WebGL rendering loop

### Required Steps

1. **Add Live2D Cubism SDK**

   Download the Cubism SDK for Web from the Live2D website and add it to the project:

   ```bash
   # Option 1: Add as npm dependency (if available)
   npm install @live2d/cubism-framework
   
   # Option 2: Add as static files
   # Copy the SDK files to public/live2d/
   ```

2. **Initialize the Model**

   In `TogaAvatar.svelte`, replace the `initializeLive2D()` placeholder:

   ```javascript
   import * as LIVE2DCUBISMCORE from '@live2d/cubism-core';
   import { Live2DModel } from '@live2d/cubism-framework';
   
   async function initializeLive2D() {
     // Initialize Cubism Core
     await LIVE2DCUBISMCORE.initialize();
     
     // Load model
     const model = await Live2DModel.loadModel('/models/toga/toga.model3.json');
     
     // Set up renderer
     const renderer = new Live2DRenderer(canvas);
     renderer.setModel(model);
     
     // Start render loop
     startRenderLoop(model, renderer);
   }
   ```

3. **Map Emotions to Parameters**

   Update the `updateAvatarEmotion()` function:

   ```javascript
   function updateAvatarEmotion(emotionData) {
     const { emotion, intensity } = emotionData;
     
     // Map emotions to Live2D parameters
     const parameterMap = {
       happy: { ParamMouthForm: 1.0, ParamEyeSmile: 1.0 },
       sad: { ParamMouthForm: -1.0, ParamEyeSmile: -1.0 },
       excited: { ParamMouthForm: 1.0, ParamEyeSmile: 1.0, ParamBodyAngleX: 10 },
       // ... more mappings
     };
     
     const params = parameterMap[emotion] || {};
     Object.entries(params).forEach(([key, value]) => {
       model.setParameterValue(key, value * intensity);
     });
   }
   ```

4. **Implement Animation Playback**

   Update the `playAnimation()` function:

   ```javascript
   function playAnimation(animationData) {
     const { animation, intensity, duration_ms } = animationData;
     
     // Load and play motion
     model.startMotion('motions', animation, intensity);
   }
   ```

## API Endpoints

The Avatar API provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/session` | POST | Create a new session |
| `/session/{id}` | GET | Get session info |
| `/session/{id}` | DELETE | Delete session |
| `/ws/{id}` | WebSocket | Real-time communication |

## WebSocket Messages

### Client → Server

```json
{
  "type": "chat",
  "data": { "message": "Hello!" },
  "session_id": "sess-123"
}
```

### Server → Client

```json
{
  "type": "emotion_update",
  "data": {
    "emotion": "happy",
    "intensity": 0.8
  }
}
```

## Configuration

The avatar can be configured through the `toga.config.js` file:

```javascript
export default {
  avatar: {
    enabled: true,
    defaultEmotion: 'playful',
    position: 'bottom-right',
    modelPath: '/models/toga/toga.model3.json',
  },
  api: {
    baseUrl: '/api/avatar',
    apiKey: process.env.AVATAR_API_KEY,
  },
};
```

## Next Steps

1. Obtain a Live2D model (`.model3.json` and associated files)
2. Add the Live2D Cubism SDK to the project
3. Implement the model loading and rendering
4. Test the integration with the Avatar API
5. Fine-tune emotion mappings and animations

## Resources

- [Live2D Cubism SDK for Web](https://www.live2d.com/en/sdk/download/cubism/)
- [Live2D Documentation](https://docs.live2d.com/)
- [Avatar API Documentation](../../../python/api/avatar/README.md)
