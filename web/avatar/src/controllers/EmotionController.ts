/**
 * EmotionController - Manages avatar emotional expressions
 * 
 * Controls the avatar's facial expressions and animations
 * based on the current emotional state.
 */

import { TogaAvatar } from '../avatar/TogaAvatar';
import { TogaPersonality, EmotionalState } from '../personality/TogaPersonality';

export interface EmotionMapping {
  expression: string;
  motion: string;
  intensity: number;
}

export class EmotionController {
  private avatar: TogaAvatar;
  private personality: TogaPersonality;
  private currentEmotion: EmotionalState = EmotionalState.Cheerful;
  private transitionDuration: number = 500; // ms
  
  // Callback for emotion changes
  public onEmotionChange: ((emotion: EmotionalState) => void) | null = null;
  
  // Mapping of emotions to avatar expressions and motions
  private emotionMappings: Record<EmotionalState, EmotionMapping> = {
    [EmotionalState.Cheerful]: {
      expression: 'happy',
      motion: 'idle',
      intensity: 0.8,
    },
    [EmotionalState.Excited]: {
      expression: 'excited',
      motion: 'excited',
      intensity: 1.0,
    },
    [EmotionalState.Thinking]: {
      expression: 'thinking',
      motion: 'think',
      intensity: 0.6,
    },
    [EmotionalState.Mischievous]: {
      expression: 'mischievous',
      motion: 'mischievous',
      intensity: 0.9,
    },
    [EmotionalState.Curious]: {
      expression: 'curious',
      motion: 'curious',
      intensity: 0.7,
    },
    [EmotionalState.Chaotic]: {
      expression: 'excited',
      motion: 'excited',
      intensity: 1.0,
    },
    [EmotionalState.Affectionate]: {
      expression: 'love',
      motion: 'blush',
      intensity: 0.85,
    },
    [EmotionalState.Neutral]: {
      expression: 'neutral',
      motion: 'idle',
      intensity: 0.5,
    },
  };
  
  constructor(avatar: TogaAvatar, personality: TogaPersonality) {
    this.avatar = avatar;
    this.personality = personality;
    
    // Initialize with personality's current emotion
    this.currentEmotion = personality.getCurrentEmotion();
  }
  
  /**
   * Set the current emotion and update avatar
   */
  setEmotion(emotion: EmotionalState): void {
    if (emotion === this.currentEmotion) return;
    
    console.log(`🎭 Emotion change: ${this.currentEmotion} -> ${emotion}`);
    
    const previousEmotion = this.currentEmotion;
    this.currentEmotion = emotion;
    
    // Update personality
    this.personality.setEmotion(emotion);
    
    // Get mapping for new emotion
    const mapping = this.emotionMappings[emotion];
    
    // Apply expression
    this.avatar.setExpression(mapping.expression);
    
    // Play associated motion
    this.avatar.playMotion(mapping.motion);
    
    // Notify listeners
    if (this.onEmotionChange) {
      this.onEmotionChange(emotion);
    }
  }
  
  /**
   * Get the current emotion
   */
  getEmotion(): EmotionalState {
    return this.currentEmotion;
  }
  
  /**
   * Transition smoothly between emotions
   */
  async transitionTo(emotion: EmotionalState, duration?: number): Promise<void> {
    const transitionTime = duration || this.transitionDuration;
    
    // Start transition
    this.setEmotion(emotion);
    
    // Wait for transition to complete
    await new Promise(resolve => setTimeout(resolve, transitionTime));
  }
  
  /**
   * React to a stimulus with appropriate emotion
   */
  react(stimulus: string): EmotionalState {
    const emotion = this.personality.analyzeMessageEmotion(stimulus);
    this.setEmotion(emotion);
    return emotion;
  }
  
  /**
   * Return to default cheerful state
   */
  resetToDefault(): void {
    this.setEmotion(EmotionalState.Cheerful);
  }
  
  /**
   * Get emotion intensity (0-1)
   */
  getIntensity(): number {
    return this.emotionMappings[this.currentEmotion].intensity;
  }
  
  /**
   * Set transition duration
   */
  setTransitionDuration(duration: number): void {
    this.transitionDuration = duration;
  }
}
