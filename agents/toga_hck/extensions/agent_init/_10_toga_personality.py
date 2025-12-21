"""
Toga Personality Initialization Extension for Agent-Zero.

This extension initializes the Toga personality overlay when an agent is created,
setting up emotional state, personality traits, and Transform Quirk capabilities.
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from python.helpers.toga_personality import (
    TogaPersonality,
    initialize_toga_personality,
)
from python.helpers.toga_transform import (
    TogaTransformQuirk,
    initialize_transform_quirk,
)
from python.helpers.toga_security import (
    TogaSecurityTester,
    initialize_toga_security_tester,
)


async def execute(agent, **kwargs):
    """
    Initialize Toga personality components for the agent.

    This extension runs during agent_init and sets up:
    - Toga personality with emotional state
    - Transform Quirk for code absorption
    - Security tester for vulnerability assessment
    - Tracking variables for absorbed systems and findings

    Args:
        agent: The Agent-Zero agent being initialized
        **kwargs: Additional arguments from extension system
    """
    # Check if this is a Toga-HCK agent
    if not hasattr(agent, "hck_config"):
        # Not a Toga-HCK agent, skip initialization
        return

    config = agent.hck_config

    # Initialize Toga personality
    personality_config = None
    if hasattr(config, "personality_tensor") and config.personality_tensor:
        personality_config = config.personality_tensor.to_dict()

    agent.toga_personality = initialize_toga_personality(personality_config)

    # Initialize Transform Quirk
    if config.enable_transform_quirk:
        agent.transform_quirk = initialize_transform_quirk()
        agent.absorbed_systems = []  # Track absorbed system names
    else:
        agent.transform_quirk = None
        agent.absorbed_systems = []

    # Initialize Security Tester
    if config.enable_security_testing:
        agent.security_tester = initialize_toga_security_tester()
        agent.security_findings = []  # Track security findings
    else:
        agent.security_tester = None
        agent.security_findings = []

    # Initialize cognitive components (if enabled)
    if hasattr(config, "enable_npu") and config.enable_npu:
        agent.npu = _initialize_npu(config)
    else:
        agent.npu = None

    if hasattr(config, "enable_atomspace") and config.enable_atomspace:
        agent.atomspace = _initialize_atomspace(config)
    else:
        agent.atomspace = None

    if hasattr(config, "enable_ontogenesis") and config.enable_ontogenesis:
        agent.ontogenetic_kernel = _initialize_ontogenesis(config)
    else:
        agent.ontogenetic_kernel = None

    if (
        hasattr(config, "enable_relevance_realization")
        and config.enable_relevance_realization
    ):
        agent.relevance_engine = _initialize_relevance_realization(config)
    else:
        agent.relevance_engine = None

    # Initialize interaction tracking
    agent.interaction_count = 0

    # Log initialization
    print(f"Ehehe~ ♡ {config.agent_name} personality initialized!")
    print(
        f"  - Transform Quirk: {'enabled' if config.enable_transform_quirk else 'disabled'}"
    )
    print(
        f"  - Security Testing: {'enabled' if config.enable_security_testing else 'disabled'}"
    )


def _initialize_npu(config):
    """Initialize NPU coprocessor for local LLM inference."""
    try:
        from llama_cpp import Llama

        npu_config = config.npu_config if hasattr(config, "npu_config") else None
        if not npu_config or not npu_config.model_path:
            print("Ehehe~ ♡ NPU enabled but no model path specified!")
            return None

        npu = Llama(
            model_path=npu_config.model_path,
            n_ctx=npu_config.n_ctx,
            n_threads=npu_config.n_threads,
            n_gpu_layers=npu_config.n_gpu_layers,
            use_mlock=npu_config.use_mlock,
            verbose=npu_config.verbose,
        )
        print(f"Ehehe~ ♡ NPU coprocessor initialized with {npu_config.model_path}!")
        return npu

    except ImportError:
        print("Ehehe~ ♡ llama-cpp-python not installed, NPU disabled")
        return None
    except Exception as e:
        print(f"Ehehe~ ♡ NPU initialization failed: {e}")
        return None


def _initialize_atomspace(config):
    """Initialize OpenCog AtomSpace for cognitive architecture."""
    try:
        from opencog.atomspace import AtomSpace

        atomspace = AtomSpace()
        print("Ehehe~ ♡ AtomSpace cognitive architecture initialized!")
        return atomspace

    except ImportError:
        print("Ehehe~ ♡ OpenCog not installed, AtomSpace disabled")
        return None
    except Exception as e:
        print(f"Ehehe~ ♡ AtomSpace initialization failed: {e}")
        return None


def _initialize_ontogenesis(config):
    """Initialize ontogenetic development kernel."""
    # Placeholder for ontogenesis implementation
    print("Ehehe~ ♡ Ontogenetic kernel initialization (placeholder)")
    return {"enabled": True, "stage": "initial"}


def _initialize_relevance_realization(config):
    """Initialize relevance realization engine."""
    # Placeholder for relevance realization implementation
    print("Ehehe~ ♡ Relevance realization engine initialization (placeholder)")
    return {"enabled": True, "attention_focus": None}
