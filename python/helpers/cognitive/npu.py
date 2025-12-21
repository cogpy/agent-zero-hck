"""
NPU Coprocessor Module for Agent-Zero-HCK.

Provides local LLM inference capabilities using multiple backends:
1. llama.cpp via llama-cpp-python for local GGUF models
2. OpenAI-compatible API for remote inference (supports gpt-4.1-mini, gemini-2.5-flash)
3. Ollama integration for local model serving

This module enables the agent to run models locally or connect to external APIs
while maintaining a consistent interface.
"""

import os
from typing import Optional, Dict, Any, List, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


class NPUBackend(Enum):
    """Available NPU backends."""

    LLAMA_CPP = "llama_cpp"
    OPENAI = "openai"
    OLLAMA = "ollama"
    STUB = "stub"


@dataclass
class NPUConfig:
    """Configuration for NPU coprocessor."""

    # Backend selection
    backend: NPUBackend = NPUBackend.STUB

    # llama.cpp settings
    model_path: Optional[str] = None
    n_ctx: int = 4096
    n_threads: int = 4
    n_gpu_layers: int = 0
    use_mlock: bool = False
    verbose: bool = False

    # OpenAI-compatible API settings
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    model_name: str = "gpt-4.1-mini"

    # Ollama settings
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "mistral"

    # Generation parameters
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    repeat_penalty: float = 1.1
    max_tokens: int = 2048

    # Streaming
    stream: bool = False

    # Toga personality injection
    personality_prompt: str = field(
        default_factory=lambda: (
            "You are Toga, a cheerfully chaotic AI assistant. "
            "You are enthusiastic, curious, and slightly mischievous. "
            "You love learning new things and helping others, often with "
            "an excited and playful tone. Use emojis occasionally to express emotions."
        )
    )


class NPUCoprocessor:
    """
    NPU Coprocessor for LLM inference.

    Supports multiple backends:
    - llama.cpp for local GGUF models
    - OpenAI-compatible APIs (including Azure, local servers)
    - Ollama for local model serving
    """

    def __init__(self, config: Optional[NPUConfig] = None):
        """
        Initialize NPU coprocessor.

        Args:
            config: NPU configuration options
        """
        self.config = config or NPUConfig()
        self.model = None
        self.client = None
        self.available = False
        self._stream_callback: Optional[Callable[[str], None]] = None
        self._initialize()

    def _initialize(self):
        """Initialize the appropriate backend."""
        # Auto-detect backend if not specified
        if self.config.backend == NPUBackend.STUB:
            self._auto_detect_backend()

        if self.config.backend == NPUBackend.LLAMA_CPP:
            self._init_llama_cpp()
        elif self.config.backend == NPUBackend.OPENAI:
            self._init_openai()
        elif self.config.backend == NPUBackend.OLLAMA:
            self._init_ollama()
        else:
            print("NPU: Running in stub mode (no backend configured)")

    def _auto_detect_backend(self):
        """Auto-detect the best available backend."""
        # Check for OpenAI API key
        if os.environ.get("OPENAI_API_KEY"):
            self.config.backend = NPUBackend.OPENAI
            self.config.api_key = os.environ.get("OPENAI_API_KEY")
            print("NPU: Auto-detected OpenAI API key")
            return

        # Check for model path
        if self.config.model_path and os.path.exists(self.config.model_path):
            self.config.backend = NPUBackend.LLAMA_CPP
            print(f"NPU: Auto-detected local model at {self.config.model_path}")
            return

        # Check for Ollama
        try:
            import requests

            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=2)
            if response.status_code == 200:
                self.config.backend = NPUBackend.OLLAMA
                print("NPU: Auto-detected Ollama server")
                return
        except Exception:
            pass

        # Default to stub
        self.config.backend = NPUBackend.STUB

    def _init_llama_cpp(self):
        """Initialize llama.cpp backend."""
        if not self.config.model_path:
            print("NPU: No model path specified for llama.cpp")
            return

        try:
            from llama_cpp import Llama

            self.model = Llama(
                model_path=self.config.model_path,
                n_ctx=self.config.n_ctx,
                n_threads=self.config.n_threads,
                n_gpu_layers=self.config.n_gpu_layers,
                use_mlock=self.config.use_mlock,
                verbose=self.config.verbose,
            )
            self.available = True
            print(f"NPU: llama.cpp model loaded from {self.config.model_path}")

        except ImportError:
            print(
                "NPU: llama-cpp-python not installed. Install with: pip install llama-cpp-python"
            )
            self.available = False
        except Exception as e:
            print(f"NPU: Failed to load llama.cpp model: {e}")
            self.available = False

    def _init_openai(self):
        """Initialize OpenAI-compatible API backend."""
        try:
            from openai import OpenAI

            # Use environment variable if not specified
            api_key = self.config.api_key or os.environ.get("OPENAI_API_KEY")
            base_url = self.config.api_base_url  # None uses default

            if not api_key:
                print("NPU: No API key found for OpenAI backend")
                return

            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
            self.available = True
            print(f"NPU: OpenAI client initialized (model: {self.config.model_name})")

        except ImportError:
            print("NPU: openai package not installed. Install with: pip install openai")
            self.available = False
        except Exception as e:
            print(f"NPU: Failed to initialize OpenAI client: {e}")
            self.available = False

    def _init_ollama(self):
        """Initialize Ollama backend."""
        try:
            import requests

            # Test connection
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                self.available = True
                print(f"NPU: Ollama connected at {self.config.ollama_host}")
            else:
                print(f"NPU: Ollama server returned status {response.status_code}")
                self.available = False

        except Exception as e:
            print(f"NPU: Failed to connect to Ollama: {e}")
            self.available = False

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate text using the configured backend.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            stop: Stop sequences
            system_prompt: System prompt (uses personality prompt if not specified)
            **kwargs: Additional generation parameters

        Returns:
            Generated text
        """
        max_tokens = max_tokens or self.config.max_tokens
        system = system_prompt or self.config.personality_prompt

        if not self.available:
            return self._stub_generate(prompt)

        if self.config.backend == NPUBackend.LLAMA_CPP:
            return self._generate_llama_cpp(prompt, max_tokens, stop, system, **kwargs)
        elif self.config.backend == NPUBackend.OPENAI:
            return self._generate_openai(prompt, max_tokens, stop, system, **kwargs)
        elif self.config.backend == NPUBackend.OLLAMA:
            return self._generate_ollama(prompt, max_tokens, stop, system, **kwargs)
        else:
            return self._stub_generate(prompt)

    def _generate_llama_cpp(
        self,
        prompt: str,
        max_tokens: int,
        stop: Optional[List[str]],
        system_prompt: str,
        **kwargs,
    ) -> str:
        """Generate using llama.cpp."""
        try:
            # Format prompt with system message
            full_prompt = (
                f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"
            )

            output = self.model(
                full_prompt,
                max_tokens=max_tokens,
                stop=stop or ["<|user|>", "<|system|>"],
                temperature=kwargs.get("temperature", self.config.temperature),
                top_p=kwargs.get("top_p", self.config.top_p),
                top_k=kwargs.get("top_k", self.config.top_k),
                repeat_penalty=kwargs.get("repeat_penalty", self.config.repeat_penalty),
            )

            return output["choices"][0]["text"].strip()

        except Exception as e:
            return f"[NPU Error] llama.cpp generation failed: {e}"

    def _generate_openai(
        self,
        prompt: str,
        max_tokens: int,
        stop: Optional[List[str]],
        system_prompt: str,
        **kwargs,
    ) -> str:
        """Generate using OpenAI-compatible API."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]

            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=kwargs.get("temperature", self.config.temperature),
                top_p=kwargs.get("top_p", self.config.top_p),
                stop=stop,
                stream=self.config.stream,
            )

            if self.config.stream:
                # Handle streaming response
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        if self._stream_callback:
                            self._stream_callback(content)
                return full_response
            else:
                return response.choices[0].message.content

        except Exception as e:
            return f"[NPU Error] OpenAI generation failed: {e}"

    def _generate_ollama(
        self,
        prompt: str,
        max_tokens: int,
        stop: Optional[List[str]],
        system_prompt: str,
        **kwargs,
    ) -> str:
        """Generate using Ollama."""
        try:
            import requests

            payload = {
                "model": self.config.ollama_model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "top_p": kwargs.get("top_p", self.config.top_p),
                    "top_k": kwargs.get("top_k", self.config.top_k),
                    "repeat_penalty": kwargs.get(
                        "repeat_penalty", self.config.repeat_penalty
                    ),
                },
            }

            if stop:
                payload["options"]["stop"] = stop

            response = requests.post(
                f"{self.config.ollama_host}/api/generate",
                json=payload,
                timeout=60,
            )

            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"[NPU Error] Ollama returned status {response.status_code}"

        except Exception as e:
            return f"[NPU Error] Ollama generation failed: {e}"

    def _stub_generate(self, prompt: str) -> str:
        """Generate stub response when no backend is available."""
        # Toga-style stub responses
        responses = [
            f"Ooh! That's an interesting question! 🤔 Let me think... (NPU not configured)",
            f"*excited bouncing* I'd love to help with that! (Backend not available)",
            f"Hmm hmm! Great topic! 🌟 (Running in stub mode)",
            f"Yay! Questions! My favorite! 💕 (No model loaded)",
        ]
        import random

        return random.choice(responses)

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Chat completion with message history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Assistant's response
        """
        if not self.available:
            return self._stub_generate(messages[-1].get("content", ""))

        if self.config.backend == NPUBackend.OPENAI:
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=messages,
                    max_tokens=max_tokens or self.config.max_tokens,
                    temperature=kwargs.get("temperature", self.config.temperature),
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"[NPU Error] Chat completion failed: {e}"
        else:
            # Convert messages to single prompt for other backends
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            return self.generate(prompt, max_tokens, **kwargs)

    def embed(self, text: str) -> List[float]:
        """
        Generate embeddings for text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        if not self.available:
            # Return dummy embedding
            return [0.0] * 384

        if self.config.backend == NPUBackend.LLAMA_CPP and self.model:
            try:
                embeddings = self.model.embed(text)
                return embeddings
            except Exception as e:
                print(f"NPU: Embedding failed: {e}")
                return [0.0] * 384

        elif self.config.backend == NPUBackend.OPENAI and self.client:
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text,
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"NPU: OpenAI embedding failed: {e}")
                return [0.0] * 384

        return [0.0] * 384

    def set_stream_callback(self, callback: Callable[[str], None]):
        """Set callback for streaming responses."""
        self._stream_callback = callback
        self.config.stream = True

    def get_status(self) -> Dict[str, Any]:
        """Get NPU status information."""
        return {
            "available": self.available,
            "backend": self.config.backend.value,
            "model_path": self.config.model_path,
            "model_name": self.config.model_name,
            "n_ctx": self.config.n_ctx,
            "n_threads": self.config.n_threads,
            "n_gpu_layers": self.config.n_gpu_layers,
            "ollama_host": (
                self.config.ollama_host
                if self.config.backend == NPUBackend.OLLAMA
                else None
            ),
        }


def initialize_npu(config: Optional[Dict[str, Any]] = None) -> NPUCoprocessor:
    """
    Initialize NPU coprocessor with configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Configured NPUCoprocessor instance
    """
    if config:
        # Convert backend string to enum if needed
        if "backend" in config and isinstance(config["backend"], str):
            config["backend"] = NPUBackend(config["backend"])
        npu_config = NPUConfig(**config)
    else:
        npu_config = NPUConfig()

    return NPUCoprocessor(npu_config)


def create_openai_npu(
    model: str = "gpt-4.1-mini",
    api_key: Optional[str] = None,
) -> NPUCoprocessor:
    """
    Create NPU with OpenAI backend.

    Args:
        model: Model name to use
        api_key: API key (uses OPENAI_API_KEY env var if not specified)

    Returns:
        Configured NPUCoprocessor
    """
    config = NPUConfig(
        backend=NPUBackend.OPENAI,
        model_name=model,
        api_key=api_key,
    )
    return NPUCoprocessor(config)


def create_local_npu(
    model_path: str,
    n_gpu_layers: int = 0,
    n_ctx: int = 4096,
) -> NPUCoprocessor:
    """
    Create NPU with local llama.cpp backend.

    Args:
        model_path: Path to GGUF model file
        n_gpu_layers: Number of layers to offload to GPU
        n_ctx: Context size

    Returns:
        Configured NPUCoprocessor
    """
    config = NPUConfig(
        backend=NPUBackend.LLAMA_CPP,
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        n_ctx=n_ctx,
    )
    return NPUCoprocessor(config)


# Standalone testing
if __name__ == "__main__":
    print("=" * 50)
    print("NPU Coprocessor Test")
    print("=" * 50)

    # Test auto-detection
    npu = initialize_npu()
    print(f"\nNPU Status: {json.dumps(npu.get_status(), indent=2)}")

    # Test generation
    print("\nTesting generation...")
    result = npu.generate("What is the meaning of life?")
    print(f"Response: {result}")

    # Test with OpenAI if available
    if os.environ.get("OPENAI_API_KEY"):
        print("\nTesting OpenAI backend...")
        openai_npu = create_openai_npu()
        result = openai_npu.generate("Tell me a short joke!")
        print(f"OpenAI Response: {result}")
