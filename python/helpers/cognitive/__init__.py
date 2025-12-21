"""
Cognitive Components Package for Agent-Zero-HCK.

Provides optional cognitive architecture integrations:
- NPU Coprocessor: Local LLM inference via llama.cpp
- AtomSpace: OpenCog cognitive architecture
- Ontogenesis: Developmental learning kernel
- Relevance Realization: Attention and salience engine
"""

from .npu import NPUCoprocessor, initialize_npu
from .atomspace_integration import AtomSpaceIntegration, initialize_atomspace
from .ontogenesis import OntogeneticKernel, initialize_ontogenesis
from .relevance import RelevanceEngine, initialize_relevance

__all__ = [
    "NPUCoprocessor",
    "initialize_npu",
    "AtomSpaceIntegration",
    "initialize_atomspace",
    "OntogeneticKernel",
    "initialize_ontogenesis",
    "RelevanceEngine",
    "initialize_relevance",
]
