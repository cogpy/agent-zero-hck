/**
 * AgentZeroClient - API Client for Agent-Zero Backend
 * 
 * Handles communication with the Agent-Zero-HCK backend
 * for AI-powered responses and personality data.
 */

export interface AgentResponse {
  text: string;
  emotion: string;
  confidence: number;
  metadata?: Record<string, unknown>;
}

export interface AgentConfig {
  baseUrl: string;
  timeout: number;
  apiKey?: string;
}

const DEFAULT_CONFIG: AgentConfig = {
  baseUrl: '/api',
  timeout: 30000,
};

export class AgentZeroClient {
  private config: AgentConfig;
  private isConnected: boolean = false;
  
  constructor(config: Partial<AgentConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }
  
  /**
   * Send a message to the agent and get a response
   */
  async sendMessage(message: string): Promise<AgentResponse> {
    try {
      const response = await this.fetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message }),
      });
      
      return response as AgentResponse;
    } catch (error) {
      console.warn('Agent API not available, using local response');
      return this.generateLocalResponse(message);
    }
  }
  
  /**
   * Get agent personality configuration
   */
  async getPersonality(): Promise<Record<string, number>> {
    try {
      const response = await this.fetch('/personality');
      return response as Record<string, number>;
    } catch {
      // Return default personality
      return {
        cheerfulness: 0.95,
        chaos: 0.85,
        obsessiveness: 0.90,
        curiosity: 0.88,
        affection: 0.80,
      };
    }
  }
  
  /**
   * Update agent personality traits
   */
  async updatePersonality(traits: Record<string, number>): Promise<void> {
    await this.fetch('/personality', {
      method: 'PUT',
      body: JSON.stringify(traits),
    });
  }
  
  /**
   * Check connection to backend
   */
  async checkConnection(): Promise<boolean> {
    try {
      await this.fetch('/health');
      this.isConnected = true;
      return true;
    } catch {
      this.isConnected = false;
      return false;
    }
  }
  
  /**
   * Make a fetch request to the API
   */
  private async fetch(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<unknown> {
    const url = `${this.config.baseUrl}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    if (this.config.apiKey) {
      headers['Authorization'] = `Bearer ${this.config.apiKey}`;
    }
    
    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      this.config.timeout
    );
    
    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } finally {
      clearTimeout(timeoutId);
    }
  }
  
  /**
   * Generate a local response when API is not available
   */
  private generateLocalResponse(message: string): AgentResponse {
    // Simple local response generation
    const responses = [
      { text: "Ooh, interesting! Tell me more! 🤔", emotion: "curious" },
      { text: "Hehe, I like the way you think! 😊", emotion: "cheerful" },
      { text: "That's so cool! *excited bouncing*", emotion: "excited" },
      { text: "Hmm hmm, fascinating! 🌟", emotion: "thinking" },
    ];
    
    const index = Math.floor(Math.random() * responses.length);
    const selected = responses[index];
    
    return {
      text: selected.text,
      emotion: selected.emotion,
      confidence: 0.8,
    };
  }
  
  /**
   * Get connection status
   */
  get connected(): boolean {
    return this.isConnected;
  }
}
