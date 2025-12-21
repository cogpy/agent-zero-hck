"""
Ontogenetic Kernel Module for Agent-Zero-HCK.

Implements developmental learning capabilities inspired by
biological ontogenesis - the development of an individual
organism from embryo to adult.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import time


class DevelopmentalStage(Enum):
    """Developmental stages inspired by Piaget's theory."""

    SENSORIMOTOR = "sensorimotor"  # Basic perception and action
    PREOPERATIONAL = "preoperational"  # Symbolic thinking
    CONCRETE_OPERATIONAL = "concrete"  # Logical operations
    FORMAL_OPERATIONAL = "formal"  # Abstract reasoning


@dataclass
class OntogenesisConfig:
    """Configuration for ontogenetic kernel."""

    learning_rate: float = 0.01
    memory_consolidation_interval: int = 100  # Interactions
    initial_stage: DevelopmentalStage = DevelopmentalStage.SENSORIMOTOR
    enable_stage_progression: bool = True
    stage_progression_threshold: int = 1000  # Interactions per stage


@dataclass
class DevelopmentalMemory:
    """Memory structure for developmental learning."""

    experiences: List[Dict[str, Any]] = field(default_factory=list)
    schemas: Dict[str, Any] = field(default_factory=dict)
    skills: Dict[str, float] = field(default_factory=dict)
    last_consolidation: float = field(default_factory=time.time)


class OntogeneticKernel:
    """
    Ontogenetic Kernel for developmental learning.

    Implements a developmental approach to learning where the agent
    progresses through stages of increasing cognitive sophistication.
    """

    def __init__(self, config: Optional[OntogenesisConfig] = None):
        """
        Initialize ontogenetic kernel.

        Args:
            config: Ontogenesis configuration options
        """
        self.config = config or OntogenesisConfig()
        self.stage = self.config.initial_stage
        self.memory = DevelopmentalMemory()
        self.interaction_count = 0
        self.stage_interaction_count = 0

        print(f"Ontogenesis: Initialized at {self.stage.value} stage")

    def process_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an experience through the developmental lens.

        Args:
            experience: Experience data with input, output, context

        Returns:
            Processed experience with developmental annotations
        """
        self.interaction_count += 1
        self.stage_interaction_count += 1

        # Add developmental context
        processed = {
            **experience,
            "stage": self.stage.value,
            "interaction": self.interaction_count,
            "timestamp": time.time(),
        }

        # Store in memory
        self.memory.experiences.append(processed)

        # Check for memory consolidation
        if self.interaction_count % self.config.memory_consolidation_interval == 0:
            self._consolidate_memory()

        # Check for stage progression
        if self.config.enable_stage_progression:
            self._check_stage_progression()

        return processed

    def _consolidate_memory(self):
        """Consolidate recent experiences into schemas."""
        recent = self.memory.experiences[-self.config.memory_consolidation_interval :]

        # Extract patterns from recent experiences
        patterns = self._extract_patterns(recent)

        # Update schemas
        for pattern_name, pattern_data in patterns.items():
            if pattern_name in self.memory.schemas:
                # Strengthen existing schema
                self.memory.schemas[pattern_name][
                    "strength"
                ] += self.config.learning_rate
            else:
                # Create new schema
                self.memory.schemas[pattern_name] = {
                    "data": pattern_data,
                    "strength": self.config.learning_rate,
                    "stage_created": self.stage.value,
                }

        self.memory.last_consolidation = time.time()
        print(f"Ontogenesis: Consolidated {len(patterns)} patterns")

    def _extract_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Extract patterns from experiences."""
        patterns = {}

        # Simple pattern extraction based on experience types
        type_counts = {}
        for exp in experiences:
            exp_type = exp.get("type", "unknown")
            type_counts[exp_type] = type_counts.get(exp_type, 0) + 1

        # Create patterns for frequent types
        for exp_type, count in type_counts.items():
            if count >= 3:  # Threshold for pattern
                patterns[f"pattern_{exp_type}"] = {
                    "type": exp_type,
                    "frequency": count / len(experiences),
                }

        return patterns

    def _check_stage_progression(self):
        """Check if agent should progress to next developmental stage."""
        if self.stage_interaction_count < self.config.stage_progression_threshold:
            return

        # Progress to next stage
        stages = list(DevelopmentalStage)
        current_idx = stages.index(self.stage)

        if current_idx < len(stages) - 1:
            self.stage = stages[current_idx + 1]
            self.stage_interaction_count = 0
            print(f"Ontogenesis: Progressed to {self.stage.value} stage!")

    def learn_skill(self, skill_name: str, success: bool):
        """
        Learn or reinforce a skill.

        Args:
            skill_name: Name of the skill
            success: Whether the skill was used successfully
        """
        current = self.memory.skills.get(skill_name, 0.0)

        if success:
            # Reinforce skill
            new_value = current + self.config.learning_rate * (1.0 - current)
        else:
            # Slight decay on failure
            new_value = current - self.config.learning_rate * 0.1

        self.memory.skills[skill_name] = max(0.0, min(1.0, new_value))

    def get_skill_level(self, skill_name: str) -> float:
        """Get current skill level."""
        return self.memory.skills.get(skill_name, 0.0)

    def get_capabilities(self) -> Dict[str, bool]:
        """
        Get capabilities available at current developmental stage.

        Returns:
            Dictionary of capability names to availability
        """
        capabilities = {
            "perception": True,
            "action": True,
            "memory": True,
        }

        if self.stage in [
            DevelopmentalStage.PREOPERATIONAL,
            DevelopmentalStage.CONCRETE_OPERATIONAL,
            DevelopmentalStage.FORMAL_OPERATIONAL,
        ]:
            capabilities["symbolic_thinking"] = True
            capabilities["language"] = True

        if self.stage in [
            DevelopmentalStage.CONCRETE_OPERATIONAL,
            DevelopmentalStage.FORMAL_OPERATIONAL,
        ]:
            capabilities["logical_operations"] = True
            capabilities["conservation"] = True

        if self.stage == DevelopmentalStage.FORMAL_OPERATIONAL:
            capabilities["abstract_reasoning"] = True
            capabilities["hypothetical_thinking"] = True
            capabilities["metacognition"] = True

        return capabilities

    def get_status(self) -> Dict[str, Any]:
        """Get ontogenetic kernel status."""
        return {
            "stage": self.stage.value,
            "interaction_count": self.interaction_count,
            "stage_interactions": self.stage_interaction_count,
            "schemas_count": len(self.memory.schemas),
            "skills_count": len(self.memory.skills),
            "experiences_count": len(self.memory.experiences),
            "capabilities": self.get_capabilities(),
        }


def initialize_ontogenesis(
    config: Optional[Dict[str, Any]] = None,
) -> OntogeneticKernel:
    """
    Initialize ontogenetic kernel with configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Configured OntogeneticKernel instance
    """
    if config:
        onto_config = OntogenesisConfig(**config)
    else:
        onto_config = OntogenesisConfig()

    return OntogeneticKernel(onto_config)


# Standalone testing
if __name__ == "__main__":
    kernel = initialize_ontogenesis()
    print(f"Status: {kernel.get_status()}")

    # Simulate experiences
    for i in range(10):
        exp = kernel.process_experience(
            {
                "type": "interaction",
                "input": f"Test input {i}",
                "output": f"Test output {i}",
            }
        )

    # Learn skills
    kernel.learn_skill("code_analysis", True)
    kernel.learn_skill("security_testing", True)

    print(f"Final Status: {kernel.get_status()}")
