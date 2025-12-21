"""
Relevance Realization Engine for Agent-Zero-HCK.

Implements attention and salience mechanisms inspired by
John Vervaeke's theory of relevance realization.
"""

from typing import Optional, Dict, Any, List, Set
from dataclasses import dataclass, field
import time
import math


@dataclass
class RelevanceConfig:
    """Configuration for relevance realization engine."""

    attention_decay_rate: float = 0.1
    salience_threshold: float = 0.5
    working_memory_capacity: int = 7  # Miller's magic number
    recency_weight: float = 0.3
    frequency_weight: float = 0.3
    importance_weight: float = 0.4


@dataclass
class AttentionObject:
    """An object in the attention field."""

    name: str
    salience: float = 0.5
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 1
    importance: float = 0.5
    context: Dict[str, Any] = field(default_factory=dict)


class RelevanceEngine:
    """
    Relevance Realization Engine for attention and salience.

    Implements mechanisms for:
    - Attention allocation and decay
    - Salience computation
    - Working memory management
    - Relevance filtering
    """

    def __init__(self, config: Optional[RelevanceConfig] = None):
        """
        Initialize relevance engine.

        Args:
            config: Relevance configuration options
        """
        self.config = config or RelevanceConfig()
        self.attention_field: Dict[str, AttentionObject] = {}
        self.working_memory: List[str] = []
        self.focus: Optional[str] = None

        print("Relevance: Engine initialized")

    def attend(self, name: str, importance: float = 0.5, context: Dict = None) -> float:
        """
        Attend to an object, updating its salience.

        Args:
            name: Name of the object to attend to
            importance: Importance rating (0.0 to 1.0)
            context: Optional context information

        Returns:
            Updated salience value
        """
        now = time.time()

        if name in self.attention_field:
            obj = self.attention_field[name]
            obj.last_accessed = now
            obj.access_count += 1
            obj.importance = max(obj.importance, importance)
            if context:
                obj.context.update(context)
        else:
            obj = AttentionObject(
                name=name,
                salience=importance,
                last_accessed=now,
                importance=importance,
                context=context or {},
            )
            self.attention_field[name] = obj

        # Compute new salience
        obj.salience = self._compute_salience(obj)

        # Update working memory
        self._update_working_memory(name)

        # Set focus if salience is high enough
        if obj.salience > self.config.salience_threshold:
            self.focus = name

        return obj.salience

    def _compute_salience(self, obj: AttentionObject) -> float:
        """
        Compute salience based on recency, frequency, and importance.

        Args:
            obj: The attention object

        Returns:
            Computed salience value
        """
        now = time.time()

        # Recency factor (exponential decay)
        time_delta = now - obj.last_accessed
        recency = math.exp(-self.config.attention_decay_rate * time_delta)

        # Frequency factor (logarithmic scaling)
        frequency = math.log(obj.access_count + 1) / math.log(100)  # Normalize
        frequency = min(1.0, frequency)

        # Importance factor
        importance = obj.importance

        # Weighted combination
        salience = (
            self.config.recency_weight * recency
            + self.config.frequency_weight * frequency
            + self.config.importance_weight * importance
        )

        return min(1.0, max(0.0, salience))

    def _update_working_memory(self, name: str):
        """Update working memory with attended object."""
        # Remove if already present
        if name in self.working_memory:
            self.working_memory.remove(name)

        # Add to front
        self.working_memory.insert(0, name)

        # Trim to capacity
        while len(self.working_memory) > self.config.working_memory_capacity:
            removed = self.working_memory.pop()
            # Decay salience of removed item
            if removed in self.attention_field:
                self.attention_field[removed].salience *= 0.5

    def decay(self):
        """Apply decay to all attention objects."""
        now = time.time()
        to_remove = []

        for name, obj in self.attention_field.items():
            obj.salience = self._compute_salience(obj)

            # Remove if salience is too low
            if obj.salience < 0.01:
                to_remove.append(name)

        for name in to_remove:
            del self.attention_field[name]
            if name in self.working_memory:
                self.working_memory.remove(name)

    def get_salient(self, threshold: Optional[float] = None) -> List[str]:
        """
        Get all salient objects above threshold.

        Args:
            threshold: Salience threshold (uses config default if None)

        Returns:
            List of salient object names
        """
        threshold = threshold or self.config.salience_threshold

        salient = [
            name
            for name, obj in self.attention_field.items()
            if obj.salience >= threshold
        ]

        # Sort by salience
        salient.sort(key=lambda n: self.attention_field[n].salience, reverse=True)

        return salient

    def get_focus(self) -> Optional[str]:
        """Get current focus of attention."""
        return self.focus

    def set_focus(self, name: str):
        """Explicitly set focus of attention."""
        if name in self.attention_field:
            self.focus = name
            self.attend(name, importance=1.0)

    def filter_relevant(
        self, items: List[str], context: Optional[Dict] = None
    ) -> List[str]:
        """
        Filter items by relevance to current attention state.

        Args:
            items: List of items to filter
            context: Optional context for relevance computation

        Returns:
            Filtered list of relevant items
        """
        relevant = []

        for item in items:
            # Check if in attention field
            if item in self.attention_field:
                if (
                    self.attention_field[item].salience
                    >= self.config.salience_threshold
                ):
                    relevant.append(item)
            # Check if in working memory
            elif item in self.working_memory:
                relevant.append(item)
            # Check context match
            elif context and self._context_match(item, context):
                relevant.append(item)

        return relevant

    def _context_match(self, item: str, context: Dict) -> bool:
        """Check if item matches context."""
        # Simple keyword matching
        item_lower = item.lower()
        for key, value in context.items():
            if isinstance(value, str) and item_lower in value.lower():
                return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get relevance engine status."""
        return {
            "focus": self.focus,
            "working_memory": self.working_memory.copy(),
            "attention_field_size": len(self.attention_field),
            "salient_count": len(self.get_salient()),
            "config": {
                "decay_rate": self.config.attention_decay_rate,
                "threshold": self.config.salience_threshold,
                "capacity": self.config.working_memory_capacity,
            },
        }

    def get_attention_map(self) -> Dict[str, float]:
        """Get map of all objects and their salience."""
        return {name: obj.salience for name, obj in self.attention_field.items()}


def initialize_relevance(config: Optional[Dict[str, Any]] = None) -> RelevanceEngine:
    """
    Initialize relevance engine with configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Configured RelevanceEngine instance
    """
    if config:
        rel_config = RelevanceConfig(**config)
    else:
        rel_config = RelevanceConfig()

    return RelevanceEngine(rel_config)


# Standalone testing
if __name__ == "__main__":
    engine = initialize_relevance()
    print(f"Status: {engine.get_status()}")

    # Attend to various objects
    engine.attend("security_vulnerability", importance=0.9)
    engine.attend("code_pattern", importance=0.7)
    engine.attend("user_request", importance=0.8)

    print(f"Salient: {engine.get_salient()}")
    print(f"Focus: {engine.get_focus()}")
    print(f"Working Memory: {engine.working_memory}")

    # Apply decay
    engine.decay()
    print(f"After decay: {engine.get_attention_map()}")
