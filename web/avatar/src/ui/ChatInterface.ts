/**
 * ChatInterface - User Chat Interface Controller
 * 
 * Manages the chat input and message handling for user interaction.
 */

export type MessageHandler = (message: string) => Promise<void>;

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'toga';
  timestamp: Date;
}

export class ChatInterface {
  private inputElement: HTMLInputElement | null = null;
  private messageHandler: MessageHandler;
  private messageHistory: ChatMessage[] = [];
  private maxHistory: number = 100;
  private isProcessing: boolean = false;
  
  constructor(messageHandler: MessageHandler) {
    this.messageHandler = messageHandler;
    this.initialize();
  }
  
  /**
   * Initialize the chat interface
   */
  private initialize(): void {
    this.inputElement = document.getElementById('chat-input') as HTMLInputElement;
    
    if (!this.inputElement) {
      console.warn('Chat input element not found');
      return;
    }
    
    // Set up event listeners
    this.inputElement.addEventListener('keypress', this.handleKeyPress.bind(this));
    this.inputElement.addEventListener('focus', this.handleFocus.bind(this));
    this.inputElement.addEventListener('blur', this.handleBlur.bind(this));
    
    console.log('💬 Chat interface initialized');
  }
  
  /**
   * Handle key press events
   */
  private async handleKeyPress(event: KeyboardEvent): Promise<void> {
    if (event.key !== 'Enter') return;
    if (!this.inputElement) return;
    
    const message = this.inputElement.value.trim();
    if (!message) return;
    
    // Prevent double-processing
    if (this.isProcessing) return;
    
    // Clear input
    this.inputElement.value = '';
    
    // Add to history
    this.addMessage(message, 'user');
    
    // Process message
    this.isProcessing = true;
    this.setInputState('processing');
    
    try {
      await this.messageHandler(message);
    } catch (error) {
      console.error('Error processing message:', error);
    } finally {
      this.isProcessing = false;
      this.setInputState('ready');
    }
  }
  
  /**
   * Handle input focus
   */
  private handleFocus(): void {
    // Could trigger avatar attention animation
    console.log('Chat input focused');
  }
  
  /**
   * Handle input blur
   */
  private handleBlur(): void {
    // Could trigger avatar idle animation
    console.log('Chat input blurred');
  }
  
  /**
   * Add a message to history
   */
  addMessage(text: string, sender: 'user' | 'toga'): ChatMessage {
    const message: ChatMessage = {
      id: this.generateId(),
      text,
      sender,
      timestamp: new Date(),
    };
    
    this.messageHistory.push(message);
    
    // Trim history if needed
    if (this.messageHistory.length > this.maxHistory) {
      this.messageHistory.shift();
    }
    
    return message;
  }
  
  /**
   * Generate a unique message ID
   */
  private generateId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  /**
   * Set input state (visual feedback)
   */
  private setInputState(state: 'ready' | 'processing'): void {
    if (!this.inputElement) return;
    
    if (state === 'processing') {
      this.inputElement.disabled = true;
      this.inputElement.placeholder = 'Toga is thinking...';
    } else {
      this.inputElement.disabled = false;
      this.inputElement.placeholder = 'Say something to Toga...';
    }
  }
  
  /**
   * Get message history
   */
  getHistory(): ChatMessage[] {
    return [...this.messageHistory];
  }
  
  /**
   * Clear message history
   */
  clearHistory(): void {
    this.messageHistory = [];
  }
  
  /**
   * Send a message programmatically
   */
  async sendMessage(text: string): Promise<void> {
    this.addMessage(text, 'user');
    await this.messageHandler(text);
  }
  
  /**
   * Focus the input element
   */
  focus(): void {
    this.inputElement?.focus();
  }
  
  /**
   * Blur the input element
   */
  blur(): void {
    this.inputElement?.blur();
  }
  
  /**
   * Check if currently processing
   */
  get processing(): boolean {
    return this.isProcessing;
  }
}
