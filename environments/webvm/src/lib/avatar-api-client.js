/**
 * Agent-Toga Live2D Avatar API Client
 *
 * A comprehensive wrapper for interacting with the Avatar API.
 */

export class AvatarApiClient {
  constructor(apiKey, baseUrl = "/api/avatar") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.sessionId = null;
    this.ws = null;
    this.pingInterval = null;
    this.messageHandlers = new Map();
  }

  /**
   * Create a new avatar session
   */
  async createSession(initialEmotion = "playful") {
    const response = await this._fetch("/session", {
      method: "POST",
      body: { initial_emotion: initialEmotion },
    });
    this.sessionId = response.session_id;
    return this.sessionId;
  }

  /**
   * Get session information
   */
  async getSession() {
    if (!this.sessionId) {
      throw new Error("Session not created. Call createSession() first.");
    }
    return await this._fetch(`/session/${this.sessionId}`);
  }

  /**
   * Delete the current session
   */
  async deleteSession() {
    if (!this.sessionId) return;
    
    await this._fetch(`/session/${this.sessionId}`, {
      method: "DELETE",
    });
    this.sessionId = null;
  }

  /**
   * Connect to the WebSocket
   */
  connectWebSocket(onMessage) {
    if (!this.sessionId) {
      throw new Error("Session not created. Call createSession() first.");
    }

    const url = new URL(this.baseUrl + `/ws/${this.sessionId}`, window.location.href);
    url.protocol = url.protocol.replace("http", "ws");
    url.searchParams.set("api_key", this.apiKey);

    this.ws = new WebSocket(url.href);

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      // Call registered handlers
      const handlers = this.messageHandlers.get(message.type) || [];
      handlers.forEach(handler => handler(message.data));
      
      // Call the main handler
      if (onMessage) {
        onMessage(message);
      }
    };

    this.ws.onopen = () => {
      console.log("WebSocket connected");
      
      // Start ping interval
      this.pingInterval = setInterval(() => {
        this.sendMessage("ping");
      }, 30000);
      
      // Call connected handlers
      const handlers = this.messageHandlers.get("connected") || [];
      handlers.forEach(handler => handler());
    };

    this.ws.onclose = () => {
      console.log("WebSocket disconnected");
      clearInterval(this.pingInterval);
      
      // Call disconnected handlers
      const handlers = this.messageHandlers.get("disconnected") || [];
      handlers.forEach(handler => handler());
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  /**
   * Register a message handler
   */
  on(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type).push(handler);
  }

  /**
   * Unregister a message handler
   */
  off(type, handler) {
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  /**
   * Send a message over WebSocket
   */
  sendMessage(type, data = {}) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          type,
          data,
          session_id: this.sessionId,
        })
      );
    }
  }

  /**
   * Send a chat message
   */
  sendChat(message) {
    this.sendMessage("chat", { message });
  }

  /**
   * Close the WebSocket connection
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  /**
   * Internal fetch wrapper
   */
  async _fetch(endpoint, options = {}) {
    const response = await fetch(this.baseUrl + endpoint, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": this.apiKey,
        ...options.headers,
      },
      body: options.body ? JSON.stringify(options.body) : null,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "API request failed");
    }

    return response.json();
  }
}
