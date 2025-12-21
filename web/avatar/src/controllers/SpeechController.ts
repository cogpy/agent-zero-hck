/**
 * SpeechController - Text-to-Speech and Lip Sync Controller
 * 
 * Manages speech synthesis and lip sync animations for the avatar.
 * Uses Web Speech API for TTS and syncs mouth movements.
 */

import { TogaAvatar } from '../avatar/TogaAvatar';

export interface SpeechConfig {
  voice: string | null;
  rate: number;
  pitch: number;
  volume: number;
}

const DEFAULT_CONFIG: SpeechConfig = {
  voice: null, // Use default voice
  rate: 1.1,   // Slightly faster for energetic personality
  pitch: 1.2,  // Higher pitch for cheerful tone
  volume: 1.0,
};

export class SpeechController {
  private avatar: TogaAvatar;
  private config: SpeechConfig;
  private synth: SpeechSynthesis | null = null;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  private isSpeaking: boolean = false;
  private lipSyncInterval: number | null = null;
  
  constructor(avatar: TogaAvatar, config: Partial<SpeechConfig> = {}) {
    this.avatar = avatar;
    this.config = { ...DEFAULT_CONFIG, ...config };
    
    // Initialize speech synthesis if available
    if ('speechSynthesis' in window) {
      this.synth = window.speechSynthesis;
    } else {
      console.warn('Speech synthesis not supported in this browser');
    }
  }
  
  /**
   * Speak text with lip sync animation
   */
  async speak(text: string): Promise<void> {
    if (!this.synth) {
      console.log('📢 Speech (no TTS):', text);
      // Simulate speaking with lip sync only
      await this.simulateSpeaking(text);
      return;
    }
    
    // Cancel any ongoing speech
    this.stop();
    
    return new Promise((resolve, reject) => {
      const utterance = new SpeechSynthesisUtterance(text);
      
      // Configure utterance
      utterance.rate = this.config.rate;
      utterance.pitch = this.config.pitch;
      utterance.volume = this.config.volume;
      
      // Set voice if specified
      if (this.config.voice) {
        const voices = this.synth!.getVoices();
        const voice = voices.find(v => v.name === this.config.voice);
        if (voice) {
          utterance.voice = voice;
        }
      }
      
      // Event handlers
      utterance.onstart = () => {
        console.log('🎤 Speaking:', text.substring(0, 50) + '...');
        this.isSpeaking = true;
        this.startLipSync();
      };
      
      utterance.onend = () => {
        this.isSpeaking = false;
        this.stopLipSync();
        resolve();
      };
      
      utterance.onerror = (event) => {
        this.isSpeaking = false;
        this.stopLipSync();
        console.error('Speech error:', event);
        reject(event);
      };
      
      // Store reference and speak
      this.currentUtterance = utterance;
      this.synth!.speak(utterance);
    });
  }
  
  /**
   * Simulate speaking when TTS is not available
   */
  private async simulateSpeaking(text: string): Promise<void> {
    // Estimate speaking duration based on text length
    // Average speaking rate is about 150 words per minute
    const words = text.split(/\s+/).length;
    const duration = (words / 150) * 60 * 1000; // Convert to milliseconds
    const minDuration = 1000; // Minimum 1 second
    const maxDuration = 10000; // Maximum 10 seconds
    
    const speakDuration = Math.min(maxDuration, Math.max(minDuration, duration));
    
    this.isSpeaking = true;
    this.startLipSync();
    
    await new Promise(resolve => setTimeout(resolve, speakDuration));
    
    this.isSpeaking = false;
    this.stopLipSync();
  }
  
  /**
   * Start lip sync animation
   */
  private startLipSync(): void {
    // Play talking motion
    this.avatar.playMotion('talk');
    
    // Start lip sync interval for mouth movement
    this.lipSyncInterval = window.setInterval(() => {
      if (this.isSpeaking) {
        // Trigger mouth movement
        // This would typically update mouth parameters
        // For now, we rely on the talk motion
      }
    }, 100);
  }
  
  /**
   * Stop lip sync animation
   */
  private stopLipSync(): void {
    if (this.lipSyncInterval !== null) {
      clearInterval(this.lipSyncInterval);
      this.lipSyncInterval = null;
    }
    
    // Return to idle
    this.avatar.playMotion('idle');
  }
  
  /**
   * Stop current speech
   */
  stop(): void {
    if (this.synth) {
      this.synth.cancel();
    }
    this.isSpeaking = false;
    this.stopLipSync();
    this.currentUtterance = null;
  }
  
  /**
   * Pause current speech
   */
  pause(): void {
    if (this.synth && this.isSpeaking) {
      this.synth.pause();
    }
  }
  
  /**
   * Resume paused speech
   */
  resume(): void {
    if (this.synth) {
      this.synth.resume();
    }
  }
  
  /**
   * Check if currently speaking
   */
  get speaking(): boolean {
    return this.isSpeaking;
  }
  
  /**
   * Get available voices
   */
  getVoices(): SpeechSynthesisVoice[] {
    if (!this.synth) return [];
    return this.synth.getVoices();
  }
  
  /**
   * Set voice by name
   */
  setVoice(voiceName: string): void {
    this.config.voice = voiceName;
  }
  
  /**
   * Set speech rate (0.1 - 10)
   */
  setRate(rate: number): void {
    this.config.rate = Math.max(0.1, Math.min(10, rate));
  }
  
  /**
   * Set pitch (0 - 2)
   */
  setPitch(pitch: number): void {
    this.config.pitch = Math.max(0, Math.min(2, pitch));
  }
  
  /**
   * Set volume (0 - 1)
   */
  setVolume(volume: number): void {
    this.config.volume = Math.max(0, Math.min(1, volume));
  }
}
