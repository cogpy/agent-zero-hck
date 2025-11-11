"""
HierarchicalSelfModeler - Multi-Level Self-Image Construction

Builds hierarchical self-images at multiple cognitive levels, from direct observation
to meta-cognitive analysis. Each level models the level below with confidence scoring.
"""

import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional


class SelfImage:
    """Represents a self-image at a specific hierarchical level."""
    
    def __init__(self, level: int):
        """
        Initialize a self-image.
        
        Args:
            level: Hierarchical level (0 = direct observation, higher = meta-cognitive)
        """
        self.level = level
        self.timestamp = datetime.now()
        self.confidence = 1.0 - (level * 0.1)  # Confidence decreases with level
        self.component_states = {}
        self.behavioral_patterns = []
        self.performance_metrics = {}
        self.meta_reflections = []
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID for this self-image."""
        content = f"{self.level}_{self.timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def add_component_state(self, component: str, state: Dict[str, Any]):
        """Add state information for a component."""
        self.component_states[component] = state
    
    def add_behavioral_pattern(self, pattern: Dict[str, Any]):
        """Add a detected behavioral pattern."""
        self.behavioral_patterns.append(pattern)
    
    def add_performance_metric(self, name: str, value: Any):
        """Add a performance metric."""
        self.performance_metrics[name] = value
    
    def add_meta_reflection(self, reflection: str):
        """Add a meta-cognitive reflection."""
        self.meta_reflections.append(reflection)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "level": self.level,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "component_states": self.component_states,
            "behavioral_patterns": self.behavioral_patterns,
            "performance_metrics": self.performance_metrics,
            "meta_reflections": self.meta_reflections,
            "reflection_count": len(self.meta_reflections),
        }


class HierarchicalSelfModeler:
    """
    Builds hierarchical self-images at multiple cognitive levels.
    """
    
    def __init__(self, max_levels: int = 5):
        """
        Initialize the hierarchical self-modeler.
        
        Args:
            max_levels: Maximum number of hierarchical levels to build
        """
        self.max_levels = max_levels
        self.current_images = {}  # level -> SelfImage
    
    async def build_self_image(
        self, 
        level: int, 
        monitor, 
        agent
    ) -> SelfImage:
        """
        Build self-image at specified hierarchical level.
        
        Args:
            level: Hierarchical level to build
            monitor: SelfMonitor instance with observations
            agent: Agent instance being modeled
            
        Returns:
            SelfImage at requested level
        """
        if level < 0 or level >= self.max_levels:
            raise ValueError(f"Level must be between 0 and {self.max_levels-1}")
        
        image = SelfImage(level)
        
        if level == 0:
            # Level 0: Direct observation
            await self._build_level_0(image, monitor, agent)
        elif level == 1:
            # Level 1: Pattern analysis
            await self._build_level_1(image, monitor, agent)
        else:
            # Level 2+: Meta-cognitive analysis
            await self._build_level_n(image, level, monitor, agent)
        
        self.current_images[level] = image
        return image
    
    async def _build_level_0(self, image: SelfImage, monitor, agent):
        """Build Level 0: Direct observation."""
        
        # Get current observation
        current_obs = monitor.observe_system(agent)
        image.add_component_state("agent", current_obs)
        
        # Add statistics
        stats = monitor.get_statistics()
        for key, value in stats.items():
            image.add_performance_metric(key, value)
        
        # Simple reflection
        if stats.get("total_observations", 0) > 0:
            image.add_meta_reflection(
                f"System has {stats['total_observations']} observations over "
                f"{stats.get('uptime_seconds', 0):.1f} seconds"
            )
    
    async def _build_level_1(self, image: SelfImage, monitor, agent):
        """Build Level 1: Pattern analysis."""
        
        # Detect patterns
        patterns = monitor.detect_patterns()
        for pattern in patterns:
            image.add_behavioral_pattern(pattern)
        
        # Detect anomalies
        anomalies = monitor.detect_anomalies()
        for anomaly in anomalies:
            image.add_behavioral_pattern({
                **anomaly,
                "is_anomaly": True
            })
        
        # Statistics-based metrics
        stats = monitor.get_statistics()
        image.add_performance_metric("pattern_count", len(patterns))
        image.add_performance_metric("anomaly_count", len(anomalies))
        
        # Meta-reflections
        if patterns:
            image.add_meta_reflection(
                f"Detected {len(patterns)} behavioral patterns in recent activity"
            )
        if anomalies:
            image.add_meta_reflection(
                f"Identified {len(anomalies)} anomalies requiring attention"
            )
        
        # Behavioral stability assessment
        if len(patterns) == 0 and len(anomalies) == 0:
            image.add_meta_reflection("System showing stable, predictable behavior")
        elif len(anomalies) > 2:
            image.add_meta_reflection("System showing unusual behavior patterns")
    
    async def _build_level_n(self, image: SelfImage, level: int, monitor, agent):
        """Build Level 2+: Meta-cognitive analysis."""
        
        # Analyze lower-level self-images
        lower_levels_analyzed = 0
        total_lower_reflections = 0
        
        for lower_level in range(level):
            if lower_level in self.current_images:
                lower_image = self.current_images[lower_level]
                lower_levels_analyzed += 1
                total_lower_reflections += len(lower_image.meta_reflections)
                
                # Add meta-cognitive reflection about lower level
                image.add_meta_reflection(
                    f"Level {lower_level} self-understanding has confidence "
                    f"{lower_image.confidence:.2f} with {len(lower_image.meta_reflections)} reflections"
                )
        
        # Meta-cognitive complexity metrics
        image.add_performance_metric("recursive_depth", level)
        image.add_performance_metric("lower_levels_analyzed", lower_levels_analyzed)
        image.add_performance_metric("total_lower_reflections", total_lower_reflections)
        
        # Self-awareness assessment
        if lower_levels_analyzed > 0:
            avg_lower_confidence = sum(
                self.current_images[l].confidence 
                for l in range(level) 
                if l in self.current_images
            ) / lower_levels_analyzed
            
            image.add_performance_metric("avg_lower_confidence", avg_lower_confidence)
            
            if avg_lower_confidence > 0.7:
                image.add_meta_reflection(
                    "Strong self-understanding at lower cognitive levels"
                )
            else:
                image.add_meta_reflection(
                    "Uncertain self-understanding at lower levels, confidence limited"
                )
    
    def get_all_images(self) -> Dict[int, SelfImage]:
        """Get all current self-images."""
        return self.current_images.copy()
    
    def get_self_awareness_score(self) -> float:
        """
        Calculate overall self-awareness score based on all levels.
        
        Returns:
            Score between 0 and 1
        """
        if not self.current_images:
            return 0.0
        
        # Weighted average with higher levels having more weight
        total_weight = 0
        weighted_sum = 0
        
        for level, image in self.current_images.items():
            weight = level + 1  # Higher levels get more weight
            weighted_sum += image.confidence * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
