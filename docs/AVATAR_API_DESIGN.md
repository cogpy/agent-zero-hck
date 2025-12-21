# Live2D Avatar API Design Document

## Overview

This document details the FastAPI endpoints needed for Live2D avatar communication and their integration with the existing Agent-Zero backend.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Live2D Avatar Frontend                       │
│  (web/avatar/ - TypeScript/PIXI.js/pixi-live2d-display)         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Avatar Server                         │
│  (python/api/avatar/ - New endpoints)                           │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ REST API    │  │ WebSocket   │  │ Server-Sent Events      │  │
│  │ Endpoints   │  │ Handler     │  │ (SSE) for streaming     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Agent-Zero Core Services                       │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ AgentContext│  │ NPU         │  │ Toga Personality        │  │
│  │ Manager     │  │ Coprocessor │  │ Engine                  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Transform   │  │ Security    │  │ AtomSpace               │  │
│  │ Quirk       │  │ Tester      │  │ Integration             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints

### 1. Session Management

#### `POST /api/avatar/session/create`
Create a new avatar session with Toga personality.

**Request:**
```json
{
  "user_id": "optional-user-identifier",
  "personality_config": {
    "chaos_level": 0.7,
    "playfulness": 0.9,
    "curiosity": 0.85
  }
}
```

**Response:**
```json
{
  "session_id": "uuid-session-id",
  "context_id": "agent-context-id",
  "personality": {
    "name": "Toga",
    "current_emotion": "excited",
    "energy_level": 0.8
  },
  "created_at": "2025-12-21T00:00:00Z",
  "expires_at": "2025-12-22T00:00:00Z"
}
```

#### `GET /api/avatar/session/{session_id}`
Get current session state.

#### `DELETE /api/avatar/session/{session_id}`
End avatar session and cleanup resources.

---

### 2. Chat & Communication

#### `POST /api/avatar/chat`
Send a message and receive Toga's response with emotion data.

**Request:**
```json
{
  "session_id": "uuid-session-id",
  "message": "Hello Toga!",
  "attachments": [],
  "request_emotion": true,
  "request_voice": true
}
```

**Response:**
```json
{
  "response": {
    "text": "Hey hey! *bounces excitedly* Oh, a new friend! I'm Toga! What fun things should we do today?",
    "emotion": {
      "primary": "excited",
      "secondary": "curious",
      "intensity": 0.85,
      "valence": 0.9,
      "arousal": 0.8
    },
    "animation_triggers": [
      {"type": "bounce", "intensity": 0.7, "duration": 500},
      {"type": "head_tilt", "direction": "right", "duration": 300}
    ],
    "voice": {
      "text": "Hey hey! Oh, a new friend! I'm Toga! What fun things should we do today?",
      "emotion": "excited",
      "pitch_modifier": 1.1,
      "rate_modifier": 1.15
    }
  },
  "context": {
    "turn_count": 1,
    "relationship_level": 0.1,
    "topics_discussed": ["greeting"]
  }
}
```

#### `POST /api/avatar/chat/stream`
Stream response with Server-Sent Events for real-time text generation.

**Request:** Same as `/api/avatar/chat`

**Response (SSE):**
```
event: token
data: {"token": "Hey", "emotion": "excited"}

event: token
data: {"token": " hey", "emotion": "excited"}

event: animation
data: {"type": "bounce", "intensity": 0.7}

event: complete
data: {"full_response": "...", "emotion": {...}}
```

---

### 3. Emotion & Animation

#### `GET /api/avatar/emotion/{session_id}`
Get current emotional state.

**Response:**
```json
{
  "current": {
    "primary": "curious",
    "secondary": "playful",
    "intensity": 0.6,
    "valence": 0.7,
    "arousal": 0.5
  },
  "history": [
    {"emotion": "excited", "timestamp": "...", "trigger": "greeting"},
    {"emotion": "curious", "timestamp": "...", "trigger": "question"}
  ],
  "available_emotions": [
    "neutral", "happy", "excited", "curious", 
    "mischievous", "thoughtful", "surprised", "affectionate"
  ]
}
```

#### `POST /api/avatar/emotion/trigger`
Manually trigger an emotion change (for testing/admin).

**Request:**
```json
{
  "session_id": "uuid-session-id",
  "emotion": "excited",
  "intensity": 0.8,
  "duration_ms": 3000,
  "transition": "smooth"
}
```

#### `GET /api/avatar/animation/queue/{session_id}`
Get pending animation triggers.

**Response:**
```json
{
  "queue": [
    {"type": "idle_blink", "scheduled_at": "..."},
    {"type": "head_tilt", "direction": "left", "scheduled_at": "..."}
  ],
  "current_animation": "idle_breathe",
  "loop_animations": ["idle_breathe", "idle_blink"]
}
```

---

### 4. Voice & Speech

#### `POST /api/avatar/voice/synthesize`
Generate speech audio from text with Toga's voice characteristics.

**Request:**
```json
{
  "session_id": "uuid-session-id",
  "text": "Hello there!",
  "emotion": "excited",
  "voice_config": {
    "pitch": 1.1,
    "rate": 1.0,
    "voice_id": "toga-default"
  }
}
```

**Response:**
```json
{
  "audio_url": "/api/avatar/audio/abc123.mp3",
  "duration_ms": 1500,
  "phonemes": [
    {"phoneme": "HH", "start_ms": 0, "end_ms": 100},
    {"phoneme": "EH", "start_ms": 100, "end_ms": 200},
    {"phoneme": "L", "start_ms": 200, "end_ms": 300}
  ],
  "lip_sync": [
    {"viseme": "A", "start_ms": 0, "end_ms": 150},
    {"viseme": "E", "start_ms": 150, "end_ms": 300}
  ]
}
```

#### `GET /api/avatar/audio/{audio_id}`
Retrieve generated audio file.

---

### 5. Personality & Configuration

#### `GET /api/avatar/personality/{session_id}`
Get Toga's current personality configuration.

**Response:**
```json
{
  "name": "Toga Himiko",
  "traits": {
    "chaos_level": 0.7,
    "playfulness": 0.9,
    "curiosity": 0.85,
    "affection_tendency": 0.8,
    "mischief_factor": 0.75
  },
  "quirks": [
    "uses_nicknames",
    "bouncy_speech",
    "blood_fascination",
    "transformation_interest"
  ],
  "speech_patterns": {
    "exclamations": ["Hey hey!", "Ooh!", "Yay!"],
    "affectionate_terms": ["cutie", "sweetie", "friend"],
    "verbal_tics": ["~", "!"]
  },
  "relationship": {
    "familiarity": 0.3,
    "trust_level": 0.5,
    "interaction_count": 15
  }
}
```

#### `PATCH /api/avatar/personality/{session_id}`
Update personality parameters.

**Request:**
```json
{
  "traits": {
    "playfulness": 0.95
  }
}
```

---

### 6. Transform Quirk Integration

#### `POST /api/avatar/transform/taste`
Trigger Toga's transform quirk to analyze a target.

**Request:**
```json
{
  "session_id": "uuid-session-id",
  "target": {
    "type": "code",
    "content": "def hello(): print('world')",
    "source": "user_input"
  }
}
```

**Response:**
```json
{
  "analysis": {
    "tastiness": 0.7,
    "complexity": 0.3,
    "patterns_detected": ["function_definition", "print_statement"],
    "absorption_potential": 0.65
  },
  "toga_reaction": {
    "text": "Ooh, this code looks yummy! Simple but sweet~",
    "emotion": "curious",
    "animation": "lick_lips"
  }
}
```

#### `POST /api/avatar/transform/absorb`
Absorb and learn from analyzed content.

---

### 7. WebSocket Endpoint

#### `WS /api/avatar/ws/{session_id}`
Real-time bidirectional communication.

**Client → Server Messages:**
```json
{"type": "chat", "message": "Hello!"}
{"type": "emotion_query"}
{"type": "animation_ack", "animation_id": "..."}
{"type": "voice_start"}
{"type": "voice_end"}
{"type": "heartbeat"}
```

**Server → Client Messages:**
```json
{"type": "chat_response", "data": {...}}
{"type": "emotion_update", "emotion": {...}}
{"type": "animation_trigger", "animation": {...}}
{"type": "voice_data", "audio_chunk": "base64..."}
{"type": "typing_indicator", "is_typing": true}
{"type": "error", "message": "..."}
```

---

### 8. Health & Status

#### `GET /api/avatar/health`
Check avatar service health.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "npu": {"status": "online", "backend": "openai", "model": "gpt-4.1-mini"},
    "personality_engine": {"status": "online"},
    "voice_synthesis": {"status": "online"},
    "atomspace": {"status": "offline", "reason": "not_configured"}
  },
  "active_sessions": 5,
  "uptime_seconds": 3600
}
```

#### `GET /api/avatar/stats`
Get usage statistics.

---

## Data Models

### EmotionState
```python
class EmotionState(BaseModel):
    primary: str  # neutral, happy, excited, curious, mischievous, thoughtful, surprised, affectionate
    secondary: Optional[str]
    intensity: float  # 0.0 - 1.0
    valence: float  # -1.0 (negative) to 1.0 (positive)
    arousal: float  # 0.0 (calm) to 1.0 (excited)
```

### AnimationTrigger
```python
class AnimationTrigger(BaseModel):
    type: str  # bounce, head_tilt, blink, wave, etc.
    intensity: float
    duration_ms: int
    parameters: Dict[str, Any]
```

### VoiceConfig
```python
class VoiceConfig(BaseModel):
    pitch: float  # 0.5 - 2.0
    rate: float  # 0.5 - 2.0
    volume: float  # 0.0 - 1.0
    voice_id: str
    emotion_modifiers: Dict[str, float]
```

### ChatMessage
```python
class ChatMessage(BaseModel):
    role: str  # user, assistant, system
    content: str
    timestamp: datetime
    emotion: Optional[EmotionState]
    attachments: List[str]
```

---

## Integration Points

### 1. Agent-Zero Context
- Use existing `AgentContext` for session management
- Leverage `AgentContextType.USER` for avatar sessions
- Integrate with existing chat history and logging

### 2. NPU Coprocessor
- Use enhanced NPU with OpenAI backend for response generation
- Inject Toga personality via system prompts
- Support streaming responses for real-time chat

### 3. Toga Personality Engine
- Use `TogaPersonality` class for trait management
- Use `TogaPersonalityTensor` for emotional state
- Integrate with `EmotionalState` for animation triggers

### 4. Transform Quirk
- Use `TogaTransformQuirk` for code analysis
- Integrate absorption mechanics with avatar reactions
- Track absorbed patterns for personality evolution

### 5. Security Tester
- Use `TogaSecurityTester` for ethical constraints
- Validate user inputs before processing
- Monitor for inappropriate content

---

## Authentication & Security

### API Key Authentication
```python
# Header: X-API-Key: your-api-key
# Or: Authorization: Bearer your-api-key
```

### Session Tokens
```python
# JWT tokens for session management
# Refresh tokens for long-lived sessions
```

### Rate Limiting
- 60 requests/minute for chat endpoints
- 10 requests/minute for voice synthesis
- 100 requests/minute for emotion queries

### CORS Configuration
```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "https://your-domain.com"
]
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "The specified session does not exist",
    "details": {
      "session_id": "invalid-id"
    }
  },
  "request_id": "req-uuid"
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `SESSION_NOT_FOUND` | 404 | Session doesn't exist |
| `SESSION_EXPIRED` | 410 | Session has expired |
| `INVALID_INPUT` | 400 | Request validation failed |
| `RATE_LIMITED` | 429 | Too many requests |
| `NPU_UNAVAILABLE` | 503 | NPU service unavailable |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## Implementation Priority

### Phase 1 (Core)
1. Session management endpoints
2. Basic chat endpoint
3. Emotion state endpoint
4. Health check

### Phase 2 (Enhanced)
1. Streaming chat (SSE)
2. WebSocket connection
3. Animation triggers
4. Voice synthesis

### Phase 3 (Advanced)
1. Transform quirk integration
2. Personality customization
3. Analytics & stats
4. Admin endpoints

---

## File Structure

```
python/api/avatar/
├── __init__.py
├── main.py              # FastAPI app initialization
├── router.py            # Main router combining all endpoints
├── dependencies.py      # Shared dependencies (auth, session)
├── models/
│   ├── __init__.py
│   ├── session.py       # Session models
│   ├── chat.py          # Chat request/response models
│   ├── emotion.py       # Emotion models
│   ├── animation.py     # Animation models
│   └── voice.py         # Voice models
├── endpoints/
│   ├── __init__.py
│   ├── session.py       # Session management
│   ├── chat.py          # Chat endpoints
│   ├── emotion.py       # Emotion endpoints
│   ├── animation.py     # Animation endpoints
│   ├── voice.py         # Voice endpoints
│   ├── transform.py     # Transform quirk endpoints
│   └── health.py        # Health & status
├── services/
│   ├── __init__.py
│   ├── session_manager.py
│   ├── chat_service.py
│   ├── emotion_engine.py
│   ├── animation_controller.py
│   └── voice_synthesizer.py
└── websocket/
    ├── __init__.py
    ├── handler.py       # WebSocket connection handler
    └── events.py        # Event definitions
```

---

*Document Version: 1.0*
*Last Updated: December 21, 2025*
