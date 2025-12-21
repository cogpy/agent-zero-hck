"""
NPU Coprocessor Module for Agent-Zero-HCK.

Provides local LLM inference capabilities using llama.cpp,
allowing the agent to run models locally without external API calls.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class NPUConfig:
    """Configuration for NPU coprocessor."""

    model_path: Optional[str] = None
    n_ctx: int = 4096
    n_threads: int = 4
    n_gpu_layers: int = 0
    use_mlock: bool = False
    verbose: bool = False
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    repeat_penalty: float = 1.1


class NPUCoprocessor:
    """
    NPU Coprocessor for local LLM inference.

    Uses llama.cpp via llama-cpp-python for efficient local inference.
    Supports various GGUF model formats.
    """

    def __init__(self, config: Optional[NPUConfig] = None):
        """
        Initialize NPU coprocessor.

        Args:
            config: NPU configuration options
        """
        self.config = config or NPUConfig()
        self.model = None
        self.available = False
        self._initialize()

    def _initialize(self):
        """Initialize the llama.cpp model."""
        if not self.config.model_path:
            print("NPU: No model path specified, running in stub mode")
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
            print(f"NPU: Model loaded from {self.config.model_path}")

        except ImportError:
            print("NPU: llama-cpp-python not installed")
            self.available = False
        except Exception as e:
            print(f"NPU: Failed to load model: {e}")
            self.available = False

    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        stop: Optional[List[str]] = None,
        **kwargs,
    ) -> str:
        """
        Generate text using the local model.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            stop: Stop sequences
            **kwargs: Additional generation parameters

        Returns:
            Generated text
        """
        if not self.available or not self.model:
            return f"[NPU Stub] Would generate response for: {prompt[:50]}..."

        try:
            output = self.model(
                prompt,
                max_tokens=max_tokens,
                stop=stop or [],
                temperature=kwargs.get("temperature", self.config.temperature),
                top_p=kwargs.get("top_p", self.config.top_p),
                top_k=kwargs.get("top_k", self.config.top_k),
                repeat_penalty=kwargs.get("repeat_penalty", self.config.repeat_penalty),
            )

            return output["choices"][0]["text"]

        except Exception as e:
            return f"[NPU Error] Generation failed: {e}"

    def embed(self, text: str) -> List[float]:
        """
        Generate embeddings for text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        if not self.available or not self.model:
            # Return dummy embedding
            return [0.0] * 384

        try:
            embeddings = self.model.embed(text)
            return embeddings
        except Exception as e:
            print(f"NPU: Embedding failed: {e}")
            return [0.0] * 384

    def get_status(self) -> Dict[str, Any]:
        """Get NPU status information."""
        return {
            "available": self.available,
            "model_path": self.config.model_path,
            "n_ctx": self.config.n_ctx,
            "n_threads": self.config.n_threads,
            "n_gpu_layers": self.config.n_gpu_layers,
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
        npu_config = NPUConfig(**config)
    else:
        npu_config = NPUConfig()

    return NPUCoprocessor(npu_config)


# Standalone testing
if __name__ == "__main__":
    npu = initialize_npu()
    print(f"NPU Status: {npu.get_status()}")

    result = npu.generate("Hello, world!")
    print(f"Generation: {result}")
