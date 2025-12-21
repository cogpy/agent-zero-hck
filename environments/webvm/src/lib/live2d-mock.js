/**
 * Mock Live2D Renderer
 * 
 * This is a demonstration implementation that simulates Live2D functionality
 * without requiring the actual Live2D SDK. It provides a visual representation
 * of the avatar with emotion and animation support.
 */

export class MockLive2DModel {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.parameters = {
      ParamMouthForm: 0,
      ParamEyeSmile: 0,
      ParamBodyAngleX: 0,
      ParamBodyAngleY: 0,
      ParamEyeBallX: 0,
      ParamEyeBallY: 0,
      ParamBrowLY: 0,
      ParamBrowRY: 0,
    };
    this.currentEmotion = 'neutral';
    this.currentAnimation = null;
    this.animationProgress = 0;
    this.isAnimating = false;
  }

  /**
   * Load the model (mock implementation)
   */
  async load(modelPath) {
    console.log('🎨 Loading mock Live2D model from:', modelPath);
    // Simulate loading delay
    await new Promise(resolve => setTimeout(resolve, 500));
    console.log('✅ Mock model loaded');
    return this;
  }

  /**
   * Set a parameter value
   */
  setParameter(name, value) {
    if (this.parameters.hasOwnProperty(name)) {
      this.parameters[name] = Math.max(-1, Math.min(1, value));
    }
  }

  /**
   * Get a parameter value
   */
  getParameter(name) {
    return this.parameters[name] || 0;
  }

  /**
   * Update the model (called each frame)
   */
  update(deltaTime) {
    // Update animation if playing
    if (this.isAnimating && this.currentAnimation) {
      this.animationProgress += deltaTime / 1000;
      
      if (this.animationProgress >= this.currentAnimation.duration) {
        this.isAnimating = false;
        this.currentAnimation = null;
        this.animationProgress = 0;
      }
    }

    // Add subtle breathing animation
    const breathe = Math.sin(Date.now() / 1000) * 0.1;
    this.setParameter('ParamBodyAngleY', breathe);
  }

  /**
   * Render the model
   */
  render() {
    const ctx = this.ctx;
    const width = this.canvas.width;
    const height = this.canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Draw background gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, '#667eea');
    gradient.addColorStop(1, '#764ba2');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    // Center position
    const centerX = width / 2;
    const centerY = height / 2;

    // Apply body angle
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(this.parameters.ParamBodyAngleX * 0.1);
    ctx.translate(this.parameters.ParamBodyAngleY * 20, 0);

    // Draw character silhouette
    this.drawCharacter(ctx, 0, 0);

    ctx.restore();

    // Draw emotion label
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`Emotion: ${this.currentEmotion}`, centerX, 30);

    // Draw animation label if animating
    if (this.isAnimating && this.currentAnimation) {
      ctx.fillText(`Animation: ${this.currentAnimation.name}`, centerX, 55);
    }
  }

  /**
   * Draw the character
   */
  drawCharacter(ctx, x, y) {
    // Head
    ctx.fillStyle = '#FFE0BD';
    ctx.beginPath();
    ctx.ellipse(x, y - 50, 80, 100, 0, 0, Math.PI * 2);
    ctx.fill();

    // Eyes
    const eyeSmile = this.parameters.ParamEyeSmile;
    const eyeBallX = this.parameters.ParamEyeBallX;
    const eyeBallY = this.parameters.ParamEyeBallY;
    
    ctx.fillStyle = '#000';
    
    // Left eye
    ctx.beginPath();
    if (eyeSmile > 0.5) {
      // Smiling eye (arc)
      ctx.arc(x - 30, y - 60, 8, 0, Math.PI);
    } else {
      // Normal eye (circle)
      ctx.arc(x - 30 + eyeBallX * 5, y - 60 + eyeBallY * 5, 8, 0, Math.PI * 2);
    }
    ctx.fill();

    // Right eye
    ctx.beginPath();
    if (eyeSmile > 0.5) {
      // Smiling eye (arc)
      ctx.arc(x + 30, y - 60, 8, 0, Math.PI);
    } else {
      // Normal eye (circle)
      ctx.arc(x + 30 + eyeBallX * 5, y - 60 + eyeBallY * 5, 8, 0, Math.PI * 2);
    }
    ctx.fill();

    // Eyebrows
    const browY = this.parameters.ParamBrowLY;
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    
    // Left eyebrow
    ctx.beginPath();
    ctx.moveTo(x - 50, y - 80 + browY * 10);
    ctx.lineTo(x - 10, y - 85 + browY * 10);
    ctx.stroke();

    // Right eyebrow
    ctx.beginPath();
    ctx.moveTo(x + 10, y - 85 + browY * 10);
    ctx.lineTo(x + 50, y - 80 + browY * 10);
    ctx.stroke();

    // Mouth
    const mouthForm = this.parameters.ParamMouthForm;
    ctx.beginPath();
    if (mouthForm > 0) {
      // Smile
      ctx.arc(x, y - 20, 30, 0.2, Math.PI - 0.2);
    } else if (mouthForm < 0) {
      // Frown
      ctx.arc(x, y - 50, 30, Math.PI + 0.2, Math.PI * 2 - 0.2);
    } else {
      // Neutral
      ctx.moveTo(x - 20, y - 30);
      ctx.lineTo(x + 20, y - 30);
    }
    ctx.stroke();

    // Body
    ctx.fillStyle = '#FF69B4';
    ctx.beginPath();
    ctx.ellipse(x, y + 100, 100, 120, 0, 0, Math.PI * 2);
    ctx.fill();

    // Arms
    ctx.strokeStyle = '#FFE0BD';
    ctx.lineWidth = 20;
    
    // Left arm
    ctx.beginPath();
    ctx.moveTo(x - 80, y + 50);
    ctx.lineTo(x - 120, y + 100);
    ctx.stroke();

    // Right arm
    ctx.beginPath();
    ctx.moveTo(x + 80, y + 50);
    ctx.lineTo(x + 120, y + 100);
    ctx.stroke();
  }

  /**
   * Play an animation
   */
  playAnimation(name, intensity = 1.0, duration = 1000) {
    console.log(`🎬 Playing animation: ${name} (intensity: ${intensity})`);
    
    this.currentAnimation = {
      name,
      intensity,
      duration: duration / 1000, // Convert to seconds
    };
    this.animationProgress = 0;
    this.isAnimating = true;

    // Apply animation effects
    switch (name) {
      case 'wave':
        this.animateWave(intensity);
        break;
      case 'bounce':
        this.animateBounce(intensity);
        break;
      case 'nod':
        this.animateNod(intensity);
        break;
      case 'shake_head':
        this.animateShakeHead(intensity);
        break;
      default:
        console.log('Unknown animation:', name);
    }
  }

  /**
   * Animation: Wave
   */
  animateWave(intensity) {
    const animate = () => {
      if (!this.isAnimating) return;
      
      const progress = this.animationProgress / this.currentAnimation.duration;
      this.setParameter('ParamBodyAngleX', Math.sin(progress * Math.PI * 4) * intensity * 0.3);
      
      requestAnimationFrame(animate);
    };
    animate();
  }

  /**
   * Animation: Bounce
   */
  animateBounce(intensity) {
    const animate = () => {
      if (!this.isAnimating) return;
      
      const progress = this.animationProgress / this.currentAnimation.duration;
      this.setParameter('ParamBodyAngleY', Math.abs(Math.sin(progress * Math.PI * 3)) * intensity * 0.5);
      
      requestAnimationFrame(animate);
    };
    animate();
  }

  /**
   * Animation: Nod
   */
  animateNod(intensity) {
    const animate = () => {
      if (!this.isAnimating) return;
      
      const progress = this.animationProgress / this.currentAnimation.duration;
      this.setParameter('ParamBodyAngleX', Math.sin(progress * Math.PI * 2) * intensity * 0.4);
      
      requestAnimationFrame(animate);
    };
    animate();
  }

  /**
   * Animation: Shake Head
   */
  animateShakeHead(intensity) {
    const animate = () => {
      if (!this.isAnimating) return;
      
      const progress = this.animationProgress / this.currentAnimation.duration;
      this.setParameter('ParamBodyAngleY', Math.sin(progress * Math.PI * 4) * intensity * 0.3);
      
      requestAnimationFrame(animate);
    };
    animate();
  }
}

/**
 * Emotion to parameter mapping
 */
export const EMOTION_MAPPINGS = {
  happy: {
    ParamMouthForm: 1.0,
    ParamEyeSmile: 1.0,
    ParamBrowLY: 0.2,
    ParamBrowRY: 0.2,
  },
  sad: {
    ParamMouthForm: -0.8,
    ParamEyeSmile: -0.5,
    ParamBrowLY: -0.5,
    ParamBrowRY: -0.5,
  },
  excited: {
    ParamMouthForm: 1.0,
    ParamEyeSmile: 0.8,
    ParamBrowLY: 0.5,
    ParamBrowRY: 0.5,
    ParamBodyAngleX: 0.2,
  },
  angry: {
    ParamMouthForm: -0.5,
    ParamEyeSmile: -0.8,
    ParamBrowLY: -0.8,
    ParamBrowRY: -0.8,
  },
  surprised: {
    ParamMouthForm: 0.5,
    ParamEyeSmile: -0.5,
    ParamBrowLY: 0.8,
    ParamBrowRY: 0.8,
  },
  neutral: {
    ParamMouthForm: 0,
    ParamEyeSmile: 0,
    ParamBrowLY: 0,
    ParamBrowRY: 0,
  },
  playful: {
    ParamMouthForm: 0.7,
    ParamEyeSmile: 0.6,
    ParamBrowLY: 0.3,
    ParamBrowRY: 0.3,
    ParamBodyAngleX: 0.1,
  },
  shy: {
    ParamMouthForm: 0.3,
    ParamEyeSmile: 0.4,
    ParamBrowLY: -0.2,
    ParamBrowRY: -0.2,
    ParamEyeBallX: 0.5,
  },
};

/**
 * Apply an emotion to the model
 */
export function applyEmotion(model, emotion, intensity = 1.0) {
  const mapping = EMOTION_MAPPINGS[emotion] || EMOTION_MAPPINGS.neutral;
  
  model.currentEmotion = emotion;
  
  Object.entries(mapping).forEach(([param, value]) => {
    model.setParameter(param, value * intensity);
  });
}
