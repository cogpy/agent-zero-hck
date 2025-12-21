/**
 * Cloudflare Worker for Agent-Toga Avatar API
 * 
 * This worker provides the Avatar API endpoints using Cloudflare Workers,
 * with KV for session storage and D1 for persistent data.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Route handling
    try {
      if (path === '/api/avatar/session' && request.method === 'POST') {
        return await createSession(request, env, corsHeaders);
      }
      
      if (path.startsWith('/api/avatar/session/') && request.method === 'GET') {
        const sessionId = path.split('/').pop();
        return await getSession(sessionId, env, corsHeaders);
      }
      
      if (path.startsWith('/api/avatar/ws/')) {
        return await handleWebSocket(request, env, corsHeaders);
      }
      
      if (path === '/api/avatar/health') {
        return new Response(JSON.stringify({ status: 'healthy' }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      return new Response('Not Found', { status: 404, headers: corsHeaders });
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  },
};

/**
 * Create a new session
 */
async function createSession(request, env, corsHeaders) {
  const body = await request.json();
  const sessionId = `sess-${crypto.randomUUID()}`;
  
  const session = {
    session_id: sessionId,
    created_at: new Date().toISOString(),
    current_emotion: body.initial_emotion || 'playful',
    message_count: 0,
  };
  
  // Store in KV
  await env.SESSIONS.put(sessionId, JSON.stringify(session), {
    expirationTtl: 3600, // 1 hour
  });
  
  return new Response(JSON.stringify(session), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

/**
 * Get session info
 */
async function getSession(sessionId, env, corsHeaders) {
  const sessionData = await env.SESSIONS.get(sessionId);
  
  if (!sessionData) {
    return new Response(JSON.stringify({ error: 'Session not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
  
  return new Response(sessionData, {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

/**
 * Handle WebSocket upgrade
 */
async function handleWebSocket(request, env, corsHeaders) {
  const upgradeHeader = request.headers.get('Upgrade');
  
  if (!upgradeHeader || upgradeHeader !== 'websocket') {
    return new Response('Expected Upgrade: websocket', { status: 426 });
  }

  const webSocketPair = new WebSocketPair();
  const [client, server] = Object.values(webSocketPair);

  // Accept the WebSocket connection
  server.accept();

  // Handle WebSocket messages
  server.addEventListener('message', async (event) => {
    try {
      const message = JSON.parse(event.data);
      
      // Handle different message types
      if (message.type === 'chat') {
        // Simulate response
        const response = {
          type: 'chat_response',
          data: {
            response: `Echo: ${message.data.message}`,
          },
        };
        server.send(JSON.stringify(response));
        
        // Send emotion update
        const emotions = ['happy', 'excited', 'playful', 'shy'];
        const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
        server.send(JSON.stringify({
          type: 'emotion_update',
          data: {
            emotion: randomEmotion,
            intensity: 0.8,
          },
        }));
      }
      
      if (message.type === 'ping') {
        server.send(JSON.stringify({ type: 'pong' }));
      }
    } catch (error) {
      server.send(JSON.stringify({
        type: 'error',
        data: { error: error.message },
      }));
    }
  });

  return new Response(null, {
    status: 101,
    webSocket: client,
  });
}
