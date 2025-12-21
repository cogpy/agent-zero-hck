<script>
  import TogaAvatar from '$lib/TogaAvatar.svelte';
  
  let avatarRef;
  let chatInput = '';
  
  function sendMessage() {
    if (chatInput.trim()) {
      avatarRef.sendChat(chatInput);
      chatInput = '';
    }
  }
  
  function handleKeyPress(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  }
</script>

<svelte:head>
  <title>Agent-Toga Live2D Avatar Demo</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-purple-100 to-pink-100 p-8">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-purple-900 mb-4">
      🎭 Agent-Toga Live2D Avatar Demo
    </h1>
    
    <div class="bg-white rounded-lg shadow-xl p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">Welcome!</h2>
      <p class="text-gray-700 mb-4">
        This is a demonstration of the Agent-Toga Live2D Avatar integration. 
        The avatar is currently running in <strong>mock mode</strong>, which means 
        it's using a simplified renderer instead of the full Live2D SDK.
      </p>
      
      <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
        <p class="text-sm text-blue-900">
          <strong>Note:</strong> The avatar will appear in the bottom-right corner. 
          You can interact with it using the demo controls or by sending chat messages below.
        </p>
      </div>
      
      <h3 class="text-xl font-semibold mb-2">Features</h3>
      <ul class="list-disc list-inside text-gray-700 space-y-2 mb-4">
        <li>Real-time emotion updates</li>
        <li>Animated responses to user input</li>
        <li>WebSocket integration with Avatar API</li>
        <li>Interactive demo controls</li>
        <li>Fallback to demo mode when API is unavailable</li>
      </ul>
      
      <h3 class="text-xl font-semibold mb-2">Try It Out</h3>
      <div class="flex gap-2">
        <input
          type="text"
          bind:value={chatInput}
          on:keypress={handleKeyPress}
          placeholder="Type a message to Toga..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <button
          on:click={sendMessage}
          class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          Send
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-xl p-6">
      <h2 class="text-2xl font-semibold mb-4">Technical Details</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 class="font-semibold text-purple-900 mb-2">Backend</h3>
          <ul class="text-sm text-gray-700 space-y-1">
            <li>✅ Avatar API with session management</li>
            <li>✅ WebSocket for real-time communication</li>
            <li>✅ Emotion and animation endpoints</li>
            <li>✅ Toga personality integration</li>
          </ul>
        </div>
        
        <div>
          <h3 class="font-semibold text-purple-900 mb-2">Frontend</h3>
          <ul class="text-sm text-gray-700 space-y-1">
            <li>✅ Svelte component architecture</li>
            <li>✅ Mock Live2D renderer</li>
            <li>✅ Emotion mapping system</li>
            <li>✅ Animation playback</li>
          </ul>
        </div>
      </div>
      
      <div class="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-500">
        <h3 class="font-semibold text-yellow-900 mb-2">Next Steps</h3>
        <p class="text-sm text-yellow-900">
          To enable the full Live2D experience, you'll need to:
        </p>
        <ol class="text-sm text-yellow-900 list-decimal list-inside mt-2 space-y-1">
          <li>Obtain a Live2D model (.model3.json)</li>
          <li>Integrate the Live2D Cubism SDK</li>
          <li>Replace the mock renderer with the real SDK</li>
        </ol>
      </div>
    </div>
  </div>
</div>

<!-- Avatar Component -->
<TogaAvatar 
  bind:this={avatarRef}
  apiKey="demo-key"
  apiBaseUrl="/api/avatar"
  position="bottom-right"
  visible={true}
  enableMockRenderer={true}
/>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
