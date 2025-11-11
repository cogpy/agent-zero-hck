"""
MetaCognitiveProcessor - Higher-Order Reasoning and Insight Generation

Generates meta-cognitive insights from self-images, performing higher-order reasoning
about the agent's own cognitive processes and behaviors.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class MetaCognitiveInsight:
    """Represents a meta-cognitive insight about system functioning."""
    
    def __init__(
        self,
        insight_type: str,
        description: str,
        severity: str = "low",
        confidence: float = 1.0,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a meta-cognitive insight.
        
        Args:
            insight_type: Type of insight (e.g., 'high_self_awareness', 'resource_underutilization')
            description: Human-readable description
            severity: Severity level ('low', 'medium', 'high')
            confidence: Confidence in the insight (0.0 to 1.0)
            data: Additional data associated with insight
        """
        self.insight_type = insight_type
        self.description = description
        self.severity = severity
        self.confidence = confidence
        self.data = data or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "insight_type": self.insight_type,
            "description": self.description,
            "severity": self.severity,
            "confidence": self.confidence,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


class MetaCognitiveProcessor:
    """
    Generates meta-cognitive insights from hierarchical self-images.
    """
    
    def __init__(self):
        """Initialize the meta-cognitive processor."""
        self.insights = []
        self.insight_history = []
    
    async def process_self_image(self, self_image) -> List[MetaCognitiveInsight]:
        """
        Process a self-image and generate insights.
        
        Args:
            self_image: SelfImage instance to process
            
        Returns:
            List of generated insights
        """
        new_insights = []
        
        # Analyze confidence level
        if self_image.confidence > 0.8:
            new_insights.append(MetaCognitiveInsight(
                insight_type="high_confidence",
                description=f"Level {self_image.level} self-image shows high confidence ({self_image.confidence:.2f})",
                severity="low",
                confidence=self_image.confidence,
                data={"level": self_image.level, "confidence": self_image.confidence}
            ))
        elif self_image.confidence < 0.5:
            new_insights.append(MetaCognitiveInsight(
                insight_type="low_confidence",
                description=f"Level {self_image.level} self-image has limited confidence ({self_image.confidence:.2f})",
                severity="medium",
                confidence=self_image.confidence,
                data={"level": self_image.level, "confidence": self_image.confidence}
            ))
        
        # Analyze behavioral patterns
        if self_image.behavioral_patterns:
            pattern_count = len(self_image.behavioral_patterns)
            anomaly_count = sum(
                1 for p in self_image.behavioral_patterns 
                if p.get("is_anomaly", False)
            )
            
            if anomaly_count > 0:
                new_insights.append(MetaCognitiveInsight(
                    insight_type="behavioral_anomalies",
                    description=f"Detected {anomaly_count} behavioral anomalies",
                    severity="high" if anomaly_count > 2 else "medium",
                    confidence=0.8,
                    data={
                        "total_patterns": pattern_count,
                        "anomaly_count": anomaly_count,
                        "anomalies": [p for p in self_image.behavioral_patterns if p.get("is_anomaly")]
                    }
                ))
            else:
                new_insights.append(MetaCognitiveInsight(
                    insight_type="behavioral_stability",
                    description=f"System showing stable behavioral patterns",
                    severity="low",
                    confidence=0.7,
                    data={"pattern_count": pattern_count}
                ))
        
        # Analyze performance metrics
        if self_image.performance_metrics:
            # Resource utilization analysis
            avg_iterations = self_image.performance_metrics.get("avg_iterations", 0)
            if avg_iterations > 0:
                if avg_iterations < 5:
                    new_insights.append(MetaCognitiveInsight(
                        insight_type="efficient_operation",
                        description=f"Agent operating efficiently with low iteration count ({avg_iterations:.1f})",
                        severity="low",
                        confidence=0.7,
                        data={"avg_iterations": avg_iterations}
                    ))
                elif avg_iterations > 15:
                    new_insights.append(MetaCognitiveInsight(
                        insight_type="high_iteration_count",
                        description=f"Agent requiring many iterations ({avg_iterations:.1f}), may indicate complex tasks",
                        severity="medium",
                        confidence=0.7,
                        data={"avg_iterations": avg_iterations}
                    ))
            
            # Self-awareness depth
            recursive_depth = self_image.performance_metrics.get("recursive_depth", 0)
            if recursive_depth > 0:
                new_insights.append(MetaCognitiveInsight(
                    insight_type="meta_reflection_depth",
                    description=f"Meta-cognitive reflection at depth {recursive_depth}",
                    severity="low",
                    confidence=0.9,
                    data={"recursive_depth": recursive_depth}
                ))
        
        # Analyze meta-reflections
        if len(self_image.meta_reflections) > 0:
            new_insights.append(MetaCognitiveInsight(
                insight_type="active_self_reflection",
                description=f"System generating {len(self_image.meta_reflections)} meta-reflections",
                severity="low",
                confidence=0.8,
                data={
                    "reflection_count": len(self_image.meta_reflections),
                    "reflections": self_image.meta_reflections
                }
            ))
        
        self.insights.extend(new_insights)
        self.insight_history.extend(new_insights)
        return new_insights
    
    async def process_all_images(self, images: Dict[int, Any]) -> List[MetaCognitiveInsight]:
        """
        Process all hierarchical self-images and generate comprehensive insights.
        
        Args:
            images: Dictionary mapping level to SelfImage
            
        Returns:
            List of all generated insights
        """
        all_insights = []
        
        # Process each level
        for level in sorted(images.keys()):
            insights = await self.process_self_image(images[level])
            all_insights.extend(insights)
        
        # Generate holistic insights
        holistic_insights = await self._generate_holistic_insights(images)
        all_insights.extend(holistic_insights)
        
        return all_insights
    
    async def _generate_holistic_insights(
        self, 
        images: Dict[int, Any]
    ) -> List[MetaCognitiveInsight]:
        """Generate insights about the overall hierarchical structure."""
        insights = []
        
        if not images:
            return insights
        
        # Overall self-awareness assessment
        avg_confidence = sum(img.confidence for img in images.values()) / len(images)
        total_reflections = sum(len(img.meta_reflections) for img in images.values())
        
        if avg_confidence > 0.7 and total_reflections > 5:
            insights.append(MetaCognitiveInsight(
                insight_type="high_self_awareness",
                description=f"System demonstrates high self-awareness (score: {avg_confidence:.2f})",
                severity="low",
                confidence=avg_confidence,
                data={
                    "avg_confidence": avg_confidence,
                    "total_reflections": total_reflections,
                    "levels": len(images)
                }
            ))
        elif avg_confidence < 0.5:
            insights.append(MetaCognitiveInsight(
                insight_type="limited_self_awareness",
                description=f"System has limited self-awareness (score: {avg_confidence:.2f})",
                severity="medium",
                confidence=0.8,
                data={
                    "avg_confidence": avg_confidence,
                    "total_reflections": total_reflections,
                    "levels": len(images)
                }
            ))
        
        # Hierarchical coherence
        if len(images) > 2:
            insights.append(MetaCognitiveInsight(
                insight_type="hierarchical_coherence",
                description=f"Maintaining {len(images)} levels of self-understanding",
                severity="low",
                confidence=0.9,
                data={"level_count": len(images)}
            ))
        
        return insights
    
    def get_insights_by_type(self, insight_type: str) -> List[MetaCognitiveInsight]:
        """Get all insights of a specific type."""
        return [i for i in self.insights if i.insight_type == insight_type]
    
    def get_insights_by_severity(self, severity: str) -> List[MetaCognitiveInsight]:
        """Get all insights of a specific severity."""
        return [i for i in self.insights if i.severity == severity]
    
    def clear_insights(self):
        """Clear current insights (history is preserved)."""
        self.insights = []
