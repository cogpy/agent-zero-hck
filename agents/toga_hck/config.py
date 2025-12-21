"""
Configuration classes for Agent-Zero-HCK.

Provides extended configuration options for the Himiko Toga Cognitive Kernel,
including personality settings, cognitive components, and ethical constraints.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class CognitiveMode(Enum):
    """Operating modes for cognitive components."""

    STANDARD = "standard"  # Basic Agent-Zero operation
    ENHANCED = "enhanced"  # With personality overlay
    COGNITIVE = "cognitive"  # With AtomSpace/NPU integration
    FULL = "full"  # All components enabled


@dataclass
class TogaPersonalityTensor:
    """
    Tensor representation of Toga's personality traits.

    Each trait is a float from 0.0 to 1.0 representing intensity.
    Aligned with python/helpers/toga_personality.py TogaPersonalityTensor.
    """

    cheerfulness: float = 0.95
    obsessiveness: float = 0.90
    playfulness: float = 0.92
    chaos: float = 0.95
    vulnerability: float = 0.70
    identity_fluidity: float = 0.88
    twisted_love: float = 0.85
    cuteness_sensitivity: float = 0.93

    def to_dict(self) -> Dict[str, float]:
        """Convert tensor to dictionary."""
        return {
            "cheerfulness": self.cheerfulness,
            "obsessiveness": self.obsessiveness,
            "playfulness": self.playfulness,
            "chaos": self.chaos,
            "vulnerability": self.vulnerability,
            "identity_fluidity": self.identity_fluidity,
            "twisted_love": self.twisted_love,
            "cuteness_sensitivity": self.cuteness_sensitivity,
        }

    def inherit(self, factor: float = 0.7) -> "TogaPersonalityTensor":
        """Create inherited personality tensor with decay factor."""
        return TogaPersonalityTensor(
            cheerfulness=self.cheerfulness * factor,
            obsessiveness=self.obsessiveness * factor,
            playfulness=self.playfulness * factor,
            chaos=self.chaos * factor,
            vulnerability=self.vulnerability * factor,
            identity_fluidity=self.identity_fluidity * factor,
            twisted_love=self.twisted_love * factor,
            cuteness_sensitivity=self.cuteness_sensitivity * factor,
        )


@dataclass
class NPUConfig:
    """Configuration for NPU coprocessor integration."""

    enabled: bool = False
    model_path: Optional[str] = None
    n_ctx: int = 4096
    n_threads: int = 4
    n_gpu_layers: int = 0
    use_mlock: bool = False
    verbose: bool = False


@dataclass
class AtomSpaceConfig:
    """Configuration for OpenCog AtomSpace integration."""

    enabled: bool = False
    persistence_path: Optional[str] = None
    enable_attention_bank: bool = True
    enable_pattern_miner: bool = False
    enable_pln: bool = False  # Probabilistic Logic Networks


@dataclass
class OntogenesisConfig:
    """Configuration for ontogenetic development kernel."""

    enabled: bool = False
    learning_rate: float = 0.01
    memory_consolidation_interval: int = 100
    developmental_stages: List[str] = field(
        default_factory=lambda: [
            "sensorimotor",
            "preoperational",
            "concrete_operational",
            "formal_operational",
        ]
    )


@dataclass
class RelevanceConfig:
    """Configuration for relevance realization engine."""

    enabled: bool = False
    attention_decay_rate: float = 0.1
    salience_threshold: float = 0.5
    working_memory_capacity: int = 7


@dataclass
class EthicalConstraints:
    """Ethical constraints for security testing operations."""

    testing_only: bool = True
    respect_boundaries: float = 0.95
    require_authorization: bool = True
    allowed_test_types: List[str] = field(
        default_factory=lambda: [
            "reconnaissance",
            "vulnerability_scan",
            "penetration_test",
            "social_engineering_assessment",
        ]
    )
    prohibited_actions: List[str] = field(
        default_factory=lambda: [
            "data_exfiltration",
            "destructive_attacks",
            "unauthorized_access",
            "malware_deployment",
        ]
    )


@dataclass
class AgentZeroHCKConfig:
    """
    Complete configuration for Agent-Zero-HCK.

    Combines Agent-Zero base configuration with Toga-specific settings
    for personality, cognitive components, and ethical constraints.
    """

    # Identity
    agent_name: str = "Toga-HCK"
    agent_role: str = "Advanced Security Research Agent with Cheerful Chaos"
    profile: str = "toga_hck"

    # Personality
    personality_tensor: TogaPersonalityTensor = field(
        default_factory=TogaPersonalityTensor
    )

    # Feature flags
    enable_transform_quirk: bool = True
    enable_security_testing: bool = True

    # Cognitive components
    cognitive_mode: CognitiveMode = CognitiveMode.ENHANCED
    npu_config: NPUConfig = field(default_factory=NPUConfig)
    atomspace_config: AtomSpaceConfig = field(default_factory=AtomSpaceConfig)
    ontogenesis_config: OntogenesisConfig = field(default_factory=OntogenesisConfig)
    relevance_config: RelevanceConfig = field(default_factory=RelevanceConfig)

    # Ethical constraints
    ethical_constraints: EthicalConstraints = field(default_factory=EthicalConstraints)

    # Agent-Zero settings
    max_subordinates: int = 5
    memory_subdir: str = "toga_hck"
    knowledge_subdirs: List[str] = field(
        default_factory=lambda: ["default", "custom", "toga_hck"]
    )

    # Additional settings
    additional: Dict[str, Any] = field(default_factory=dict)

    @property
    def enable_npu(self) -> bool:
        """Check if NPU is enabled."""
        return self.npu_config.enabled

    @property
    def enable_atomspace(self) -> bool:
        """Check if AtomSpace is enabled."""
        return self.atomspace_config.enabled

    @property
    def enable_ontogenesis(self) -> bool:
        """Check if ontogenesis is enabled."""
        return self.ontogenesis_config.enabled

    @property
    def enable_relevance_realization(self) -> bool:
        """Check if relevance realization is enabled."""
        return self.relevance_config.enabled

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "profile": self.profile,
            "personality": self.personality_tensor.to_dict(),
            "enable_transform_quirk": self.enable_transform_quirk,
            "enable_security_testing": self.enable_security_testing,
            "cognitive_mode": self.cognitive_mode.value,
            "max_subordinates": self.max_subordinates,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentZeroHCKConfig":
        """Create configuration from dictionary."""
        config = cls()

        if "agent_name" in data:
            config.agent_name = data["agent_name"]
        if "agent_role" in data:
            config.agent_role = data["agent_role"]
        if "profile" in data:
            config.profile = data["profile"]
        if "personality" in data:
            config.personality_tensor = TogaPersonalityTensor(**data["personality"])
        if "enable_transform_quirk" in data:
            config.enable_transform_quirk = data["enable_transform_quirk"]
        if "enable_security_testing" in data:
            config.enable_security_testing = data["enable_security_testing"]
        if "cognitive_mode" in data:
            config.cognitive_mode = CognitiveMode(data["cognitive_mode"])
        if "max_subordinates" in data:
            config.max_subordinates = data["max_subordinates"]

        return config


# Default configurations for different use cases
DEFAULT_CONFIG = AgentZeroHCKConfig()

MINIMAL_CONFIG = AgentZeroHCKConfig(
    enable_transform_quirk=False,
    enable_security_testing=False,
    cognitive_mode=CognitiveMode.STANDARD,
    max_subordinates=0,
)

FULL_COGNITIVE_CONFIG = AgentZeroHCKConfig(
    cognitive_mode=CognitiveMode.FULL,
    npu_config=NPUConfig(enabled=True),
    atomspace_config=AtomSpaceConfig(enabled=True),
    ontogenesis_config=OntogenesisConfig(enabled=True),
    relevance_config=RelevanceConfig(enabled=True),
)

SECURITY_TESTING_CONFIG = AgentZeroHCKConfig(
    agent_role="Ethical Security Testing Agent",
    enable_transform_quirk=True,
    enable_security_testing=True,
    ethical_constraints=EthicalConstraints(
        testing_only=True,
        require_authorization=True,
    ),
)
