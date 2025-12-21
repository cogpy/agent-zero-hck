/**
 * Type declarations for pixi-live2d-display
 */

declare module 'pixi-live2d-display' {
  import * as PIXI from 'pixi.js';
  
  export interface Live2DModelOptions {
    autoInteract?: boolean;
    autoUpdate?: boolean;
  }
  
  export class Live2DModel extends PIXI.Container {
    static from(
      source: string | object,
      options?: Live2DModelOptions
    ): Promise<Live2DModel>;
    
    anchor: PIXI.ObservablePoint;
    scale: PIXI.ObservablePoint;
    x: number;
    y: number;
    interactive: boolean;
    
    motion(
      group: string,
      index?: number,
      priority?: number
    ): Promise<boolean>;
    
    expression(name: string): void;
    
    focus(x: number, y: number): void;
    
    on(event: string, handler: (...args: any[]) => void): this;
    
    destroy(): void;
  }
}

// Extend Window interface for PIXI global
declare global {
  interface Window {
    PIXI: typeof import('pixi.js');
  }
}
