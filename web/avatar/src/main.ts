/**
 * Agent-Toga Live2D Avatar
 * 
 * Main entry point for the Live2D avatar interface.
 * Integrates with Agent-Zero-HCK for personality-driven animations.
 */

import { TogaAvatar } from './avatar/TogaAvatar';
import { EmotionController } from './controllers/EmotionController';
import { SpeechController } from './controllers/SpeechController';
import { ChatInterface } from './ui/ChatInterface';
import { TogaPersonality, EmotionalState } from './personality/TogaPersonality';

// Global application state
interface AppState {
  avatar: TogaAvatar | null;
  emotionController: EmotionController | null;
  speechController: SpeechController | null;
  chatInterface: ChatInterface | null;
  personality: TogaPersonality;
  isInitialized: boolean;
}

const state: AppState = {
  avatar: null,
  emotionController: null,
  speechController: null,
  chatInterface: null,
  personality: new TogaPersonality(),
  isInitialized: false,
};

/**
 * Initialize the avatar application
 */
async function initializeApp(): Promise<void> {
  console.log('🎭 Initializing Agent-Toga Avatar...');
  
  const loadingScreen = document.getElementById('loading-screen');
  const canvas = document.getElementById('avatar-canvas') as HTMLCanvasElement;
  
  if (!canvas) {
    throw new Error('Avatar canvas not found');
  }
  
  try {
    // Initialize the avatar
    state.avatar = new TogaAvatar(canvas);
    await state.avatar.initialize();
    
    // Initialize controllers
    state.emotionController = new EmotionController(state.avatar, state.personality);
    state.speechController = new SpeechController(state.avatar);
    state.chatInterface = new ChatInterface(handleUserMessage);
    
    // Set up UI event handlers
    setupEventHandlers();
    
    // Start the animation loop
    state.avatar.startAnimationLoop();
    
    // Hide loading screen
    if (loadingScreen) {
      loadingScreen.classList.add('hidden');
    }
    
    // Show welcome message
    showSpeechBubble("Hello! I'm Toga, your cheerfully chaotic AI companion! 🎉");
    
    state.isInitialized = true;
    console.log('✅ Agent-Toga Avatar initialized successfully!');
    
  } catch (error) {
    console.error('❌ Failed to initialize avatar:', error);
    if (loadingScreen) {
      loadingScreen.innerHTML = `
        <p style="color: #ff6b6b;">Failed to load avatar</p>
        <p style="font-size: 12px; margin-top: 10px;">${error}</p>
      `;
    }
  }
}

/**
 * Handle user messages from the chat interface
 */
async function handleUserMessage(message: string): Promise<void> {
  if (!state.avatar || !state.emotionController) return;
  
  console.log('📝 User message:', message);
  
  // Analyze message sentiment and update emotion
  const emotion = state.personality.analyzeMessageEmotion(message);
  state.emotionController.setEmotion(emotion);
  
  // Generate response based on personality
  const response = state.personality.generateResponse(message);
  
  // Show response in speech bubble
  showSpeechBubble(response);
  
  // Trigger appropriate animation
  if (emotion === EmotionalState.Excited) {
    state.avatar.playMotion('excited');
  } else if (emotion === EmotionalState.Thinking) {
    state.avatar.playMotion('think');
  } else {
    state.avatar.playMotion('talk');
  }
  
  // Speak the response if speech synthesis is available
  if (state.speechController) {
    await state.speechController.speak(response);
  }
}

/**
 * Show a message in the speech bubble
 */
function showSpeechBubble(message: string): void {
  const bubble = document.getElementById('speech-bubble');
  const text = document.getElementById('speech-text');
  
  if (bubble && text) {
    text.textContent = message;
    bubble.classList.add('visible');
    
    // Auto-hide after a delay based on message length
    const displayTime = Math.max(3000, message.length * 50);
    setTimeout(() => {
      bubble.classList.remove('visible');
    }, displayTime);
  }
}

/**
 * Update the emotion indicator UI
 */
function updateEmotionIndicator(emotion: EmotionalState): void {
  const indicator = document.getElementById('current-emotion');
  if (!indicator) return;
  
  const emotionMap: Record<EmotionalState, string> = {
    [EmotionalState.Cheerful]: '😊 Cheerful',
    [EmotionalState.Excited]: '🎉 Excited',
    [EmotionalState.Thinking]: '🤔 Thinking',
    [EmotionalState.Mischievous]: '😈 Mischievous',
    [EmotionalState.Curious]: '🧐 Curious',
    [EmotionalState.Chaotic]: '🌀 Chaotic',
    [EmotionalState.Affectionate]: '💕 Affectionate',
    [EmotionalState.Neutral]: '😐 Neutral',
  };
  
  indicator.textContent = emotionMap[emotion] || '😊 Cheerful';
}

/**
 * Set up UI event handlers
 */
function setupEventHandlers(): void {
  // Control buttons
  const btnWave = document.getElementById('btn-wave');
  const btnExcited = document.getElementById('btn-excited');
  const btnThink = document.getElementById('btn-think');
  const btnLaugh = document.getElementById('btn-laugh');
  
  btnWave?.addEventListener('click', () => {
    state.avatar?.playMotion('wave');
    showSpeechBubble("*waves enthusiastically* Hi there! 👋");
  });
  
  btnExcited?.addEventListener('click', () => {
    state.avatar?.playMotion('excited');
    state.emotionController?.setEmotion(EmotionalState.Excited);
    showSpeechBubble("Ooh! This is so exciting! 🎉✨");
  });
  
  btnThink?.addEventListener('click', () => {
    state.avatar?.playMotion('think');
    state.emotionController?.setEmotion(EmotionalState.Thinking);
    showSpeechBubble("Hmm, let me think about that... 🤔");
  });
  
  btnLaugh?.addEventListener('click', () => {
    state.avatar?.playMotion('laugh');
    state.emotionController?.setEmotion(EmotionalState.Cheerful);
    showSpeechBubble("Ahaha! That's hilarious! 😂");
  });
  
  // Chat input
  const chatInput = document.getElementById('chat-input') as HTMLInputElement;
  chatInput?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && chatInput.value.trim()) {
      handleUserMessage(chatInput.value.trim());
      chatInput.value = '';
    }
  });
  
  // Listen for emotion changes
  if (state.emotionController) {
    state.emotionController.onEmotionChange = updateEmotionIndicator;
  }
  
  // Handle window resize
  window.addEventListener('resize', () => {
    state.avatar?.resize();
  });
  
  // Handle visibility change (pause when tab is hidden)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      state.avatar?.pause();
    } else {
      state.avatar?.resume();
    }
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}

// Export for external access
export { state, handleUserMessage, showSpeechBubble };
