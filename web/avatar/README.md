# Agent-Toga Live2D Avatar

Interactive Live2D avatar interface for Agent-Toga, the cheerfully chaotic AI companion from Agent-Zero-HCK.

## Features

- **Live2D Integration**: Full Live2D Cubism SDK support via pixi-live2d-display
- **Personality-Driven Animations**: Emotions and expressions based on Toga's personality traits
- **Text-to-Speech**: Web Speech API integration with lip sync
- **Interactive Chat**: Real-time conversation with the avatar
- **Responsive Design**: Works on desktop and mobile devices
- **Fallback Mode**: Placeholder avatar when Live2D model is not available

## Quick Start

```bash
# Navigate to avatar directory
cd web/avatar

# Install dependencies
npm install

# Start development server
npm run dev
```

Open http://localhost:3000 to see the avatar.

## Project Structure

```
web/avatar/
├── src/
│   ├── main.ts                 # Application entry point
│   ├── avatar/
│   │   └── TogaAvatar.ts       # Live2D avatar controller
│   ├── controllers/
│   │   ├── EmotionController.ts # Emotion management
│   │   └── SpeechController.ts  # TTS and lip sync
│   ├── personality/
│   │   └── TogaPersonality.ts   # Personality engine
│   ├── ui/
│   │   └── ChatInterface.ts     # Chat UI controller
│   ├── api/
│   │   └── AgentZeroClient.ts   # Backend API client
│   └── types/
│       └── pixi-live2d-display.d.ts
├── assets/
│   ├── models/                  # Live2D model files
│   └── motions/                 # Motion data
├── public/                      # Static assets
├── index.html                   # HTML entry point
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Personality Traits

Toga's personality is defined by these traits:

| Trait | Value | Description |
|-------|-------|-------------|
| Cheerfulness | 0.95 | Extremely positive and happy |
| Chaos | 0.85 | Unpredictable and spontaneous |
| Obsessiveness | 0.90 | Intensely focused on interests |
| Curiosity | 0.88 | Always eager to learn |
| Affection | 0.80 | Caring and emotionally expressive |

## Emotional States

The avatar can express these emotions:

- 😊 **Cheerful** - Default happy state
- 🎉 **Excited** - High energy enthusiasm
- 🤔 **Thinking** - Contemplative mode
- 😈 **Mischievous** - Playful scheming
- 🧐 **Curious** - Inquisitive interest
- 🌀 **Chaotic** - Maximum chaos energy
- 💕 **Affectionate** - Loving and caring
- 😐 **Neutral** - Calm baseline

## Adding a Live2D Model

1. Export your model from Live2D Cubism Editor
2. Place model files in `assets/models/toga/`
3. Update the model path in `TogaAvatar.ts`

Required files:
- `toga.model3.json` - Model configuration
- `toga.moc3` - Model data
- `toga.*.png` - Texture files
- `toga.physics3.json` - Physics settings (optional)
- Motion files in `motions/` folder

## API Integration

The avatar can connect to the Agent-Zero-HCK backend:

```typescript
import { AgentZeroClient } from './api/AgentZeroClient';

const client = new AgentZeroClient({
  baseUrl: 'http://localhost:8000/api',
});

const response = await client.sendMessage('Hello!');
```

## Controls

| Button | Action |
|--------|--------|
| 👋 Wave | Play wave animation |
| 🎉 Excited | Trigger excited emotion |
| 🤔 Think | Enter thinking mode |
| 😂 Laugh | Play laugh animation |

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 14+
- Edge 80+

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Run tests
npm run test
```

## License

MIT License - See LICENSE file for details.

## Credits

- Live2D Cubism SDK: https://www.live2d.com/
- pixi-live2d-display: https://github.com/guansss/pixi-live2d-display
- PIXI.js: https://pixijs.com/
