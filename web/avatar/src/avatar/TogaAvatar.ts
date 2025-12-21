/**
 * TogaAvatar - Live2D Avatar Controller
 * 
 * Manages the Live2D model rendering and animations for Agent-Toga.
 * Uses pixi-live2d-display for WebGL rendering.
 */

import * as PIXI from 'pixi.js';
import { Live2DModel } from 'pixi-live2d-display';

// Register Live2D with PIXI
window.PIXI = PIXI;

export interface MotionConfig {
  name: string;
  priority: number;
  loop: boolean;
}

export interface AvatarConfig {
  modelPath: string;
  scale: number;
  position: { x: number; y: number };
  idleMotion: string;
}

const DEFAULT_CONFIG: AvatarConfig = {
  modelPath: '/assets/models/toga/toga.model3.json',
  scale: 0.4,
  position: { x: 0.5, y: 0.7 },
  idleMotion: 'idle',
};

export class TogaAvatar {
  private canvas: HTMLCanvasElement;
  private app: PIXI.Application | null = null;
  private model: Live2DModel | null = null;
  private config: AvatarConfig;
  private isPlaying: boolean = false;
  private currentMotion: string = '';
  
  // Motion definitions for Toga's personality
  private motions: Record<string, MotionConfig> = {
    idle: { name: 'Idle', priority: 1, loop: true },
    wave: { name: 'Wave', priority: 2, loop: false },
    talk: { name: 'Talk', priority: 2, loop: false },
    excited: { name: 'Excited', priority: 3, loop: false },
    think: { name: 'Think', priority: 2, loop: false },
    laugh: { name: 'Laugh', priority: 3, loop: false },
    curious: { name: 'Curious', priority: 2, loop: false },
    mischievous: { name: 'Mischievous', priority: 3, loop: false },
    blush: { name: 'Blush', priority: 2, loop: false },
  };
  
  constructor(canvas: HTMLCanvasElement, config: Partial<AvatarConfig> = {}) {
    this.canvas = canvas;
    this.config = { ...DEFAULT_CONFIG, ...config };
  }
  
  /**
   * Initialize the avatar and PIXI application
   */
  async initialize(): Promise<void> {
    console.log('🎨 Initializing PIXI application...');
    
    // Create PIXI application
    this.app = new PIXI.Application({
      view: this.canvas,
      resizeTo: window,
      backgroundColor: 0x1a1a2e,
      backgroundAlpha: 0,
      antialias: true,
      autoDensity: true,
      resolution: window.devicePixelRatio || 1,
    });
    
    // Initialize PIXI application
    await this.app.init();
    
    console.log('📦 Loading Live2D model...');
    
    try {
      // Try to load the model
      this.model = await Live2DModel.from(this.config.modelPath, {
        autoInteract: true,
        autoUpdate: true,
      });
      
      // Configure model
      this.setupModel();
      
      // Add to stage
      this.app.stage.addChild(this.model as unknown as PIXI.Container);
      
      console.log('✅ Live2D model loaded successfully');
    } catch (error) {
      console.warn('⚠️ Could not load Live2D model, using placeholder:', error);
      this.createPlaceholderAvatar();
    }
  }
  
  /**
   * Set up the Live2D model properties
   */
  private setupModel(): void {
    if (!this.model || !this.app) return;
    
    // Scale and position
    const { width, height } = this.app.screen;
    this.model.scale.set(this.config.scale);
    this.model.x = width * this.config.position.x;
    this.model.y = height * this.config.position.y;
    
    // Center anchor
    this.model.anchor.set(0.5, 0.5);
    
    // Enable interaction
    this.model.interactive = true;
    
    // Set up mouse tracking for eye movement
    this.setupMouseTracking();
    
    // Set up tap interaction
    this.model.on('pointerdown', () => {
      this.playMotion('wave');
    });
  }
  
  /**
   * Create a placeholder avatar when Live2D model is not available
   */
  private createPlaceholderAvatar(): void {
    if (!this.app) return;
    
    const { width, height } = this.app.screen;
    
    // Create a simple placeholder
    const container = new PIXI.Container();
    
    // Background circle
    const bg = new PIXI.Graphics();
    bg.beginFill(0x6c5ce7);
    bg.drawCircle(0, 0, 100);
    bg.endFill();
    container.addChild(bg);
    
    // Face
    const face = new PIXI.Graphics();
    // Eyes
    face.beginFill(0xffffff);
    face.drawCircle(-30, -20, 15);
    face.drawCircle(30, -20, 15);
    face.endFill();
    // Pupils
    face.beginFill(0x2d3436);
    face.drawCircle(-30, -20, 8);
    face.drawCircle(30, -20, 8);
    face.endFill();
    // Smile
    face.lineStyle(4, 0xffffff);
    face.arc(0, 10, 40, 0.2, Math.PI - 0.2);
    container.addChild(face);
    
    // Add text
    const text = new PIXI.Text('Toga', {
      fontFamily: 'Arial',
      fontSize: 24,
      fill: 0xffffff,
      align: 'center',
    });
    text.anchor.set(0.5);
    text.y = 130;
    container.addChild(text);
    
    // Position
    container.x = width * 0.5;
    container.y = height * 0.4;
    
    this.app.stage.addChild(container);
    
    // Animate the placeholder
    this.animatePlaceholder(container, face);
  }
  
  /**
   * Animate the placeholder avatar
   */
  private animatePlaceholder(container: PIXI.Container, face: PIXI.Graphics): void {
    if (!this.app) return;
    
    let time = 0;
    this.app.ticker.add((delta) => {
      time += delta.deltaTime * 0.02;
      
      // Bobbing animation
      container.y = (this.app?.screen.height || 600) * 0.4 + Math.sin(time) * 10;
      
      // Slight rotation
      container.rotation = Math.sin(time * 0.5) * 0.05;
    });
  }
  
  /**
   * Set up mouse tracking for eye movement
   */
  private setupMouseTracking(): void {
    if (!this.model || !this.app) return;
    
    this.app.stage.interactive = true;
    this.app.stage.hitArea = this.app.screen;
    
    this.app.stage.on('pointermove', (event: PIXI.FederatedPointerEvent) => {
      if (!this.model) return;
      
      // Calculate focus point relative to model
      const modelX = this.model.x;
      const modelY = this.model.y;
      
      // Normalize to -1 to 1 range
      const focusX = (event.global.x - modelX) / 200;
      const focusY = (event.global.y - modelY) / 200;
      
      // Apply to model (if supported)
      try {
        this.model.focus(focusX, focusY);
      } catch {
        // Focus not supported by this model
      }
    });
  }
  
  /**
   * Play a motion animation
   */
  playMotion(motionName: string): void {
    if (!this.model) {
      console.log(`🎬 Motion requested: ${motionName} (placeholder mode)`);
      return;
    }
    
    const motion = this.motions[motionName];
    if (!motion) {
      console.warn(`Unknown motion: ${motionName}`);
      return;
    }
    
    console.log(`🎬 Playing motion: ${motionName}`);
    this.currentMotion = motionName;
    
    try {
      // Start the motion
      this.model.motion(motion.name, undefined, motion.priority);
      
      // Return to idle after non-looping motions
      if (!motion.loop) {
        setTimeout(() => {
          if (this.currentMotion === motionName) {
            this.playMotion('idle');
          }
        }, 2000);
      }
    } catch (error) {
      console.warn(`Failed to play motion ${motionName}:`, error);
    }
  }
  
  /**
   * Set expression
   */
  setExpression(expressionName: string): void {
    if (!this.model) return;
    
    try {
      this.model.expression(expressionName);
    } catch (error) {
      console.warn(`Failed to set expression ${expressionName}:`, error);
    }
  }
  
  /**
   * Start the animation loop
   */
  startAnimationLoop(): void {
    this.isPlaying = true;
    this.playMotion('idle');
  }
  
  /**
   * Pause animations
   */
  pause(): void {
    this.isPlaying = false;
    if (this.app) {
      this.app.ticker.stop();
    }
  }
  
  /**
   * Resume animations
   */
  resume(): void {
    this.isPlaying = true;
    if (this.app) {
      this.app.ticker.start();
    }
  }
  
  /**
   * Handle window resize
   */
  resize(): void {
    if (!this.app || !this.model) return;
    
    const { width, height } = this.app.screen;
    this.model.x = width * this.config.position.x;
    this.model.y = height * this.config.position.y;
  }
  
  /**
   * Clean up resources
   */
  destroy(): void {
    if (this.model) {
      this.model.destroy();
      this.model = null;
    }
    if (this.app) {
      this.app.destroy(true);
      this.app = null;
    }
  }
  
  /**
   * Get current playing state
   */
  get playing(): boolean {
    return this.isPlaying;
  }
  
  /**
   * Get the PIXI application
   */
  get application(): PIXI.Application | null {
    return this.app;
  }
}
