"""
AutognosisOrchestrator - Coordinates the Autognosis System

Orchestrates all autognosis components to run complete self-awareness cycles.
Manages self-monitoring, hierarchical modeling, meta-cognitive processing, and reporting.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .self_monitor import SelfMonitor
from .hierarchical_modeler import HierarchicalSelfModeler, SelfImage
from .meta_cognitive import MetaCognitiveProcessor, MetaCognitiveInsight


class AutognosisOrchestrator:
    """
    Coordinates the complete autognosis system for hierarchical self-image building.
    """
    
    def __init__(self, max_levels: int = 5):
        """
        Initialize the autognosis orchestrator.
        
        Args:
            max_levels: Maximum number of hierarchical levels to maintain
        """
        self.max_levels = max_levels
        self.monitor = SelfMonitor()
        self.modeler = HierarchicalSelfModeler(max_levels=max_levels)
        self.processor = MetaCognitiveProcessor()
        self.initialized = False
        self.cycle_count = 0
        self.last_cycle_time = None
    
    async def initialize(self, agent):
        """
        Initialize the autognosis system for an agent.
        
        Args:
            agent: Agent instance to monitor
        """
        # Perform initial observation
        self.monitor.observe_system(agent)
        self.initialized = True
    
    async def run_autognosis_cycle(self, agent) -> Dict[str, Any]:
        """
        Run a complete autognosis cycle: observe, model, analyze, report.
        
        Args:
            agent: Agent instance to analyze
            
        Returns:
            Dict containing cycle results including self-images and insights
        """
        if not self.initialized:
            await self.initialize(agent)
        
        cycle_start = datetime.now()
        
        # Step 1: Observe current system state
        observation = self.monitor.observe_system(agent)
        
        # Step 2: Detect patterns and anomalies
        patterns = self.monitor.detect_patterns()
        anomalies = self.monitor.detect_anomalies()
        
        # Step 3: Build hierarchical self-images
        self_images = {}
        for level in range(self.max_levels):
            self_images[level] = await self.modeler.build_self_image(
                level, self.monitor, agent
            )
        
        # Step 4: Generate meta-cognitive insights
        insights = await self.processor.process_all_images(self_images)
        
        # Step 5: Calculate self-awareness score
        self_awareness_score = self.modeler.get_self_awareness_score()
        
        # Update cycle metadata
        self.cycle_count += 1
        self.last_cycle_time = datetime.now()
        cycle_duration = (self.last_cycle_time - cycle_start).total_seconds()
        
        # Compile results
        results = {
            "cycle_number": self.cycle_count,
            "timestamp": self.last_cycle_time.isoformat(),
            "duration_seconds": cycle_duration,
            "observation": observation,
            "patterns": patterns,
            "anomalies": anomalies,
            "self_images": {
                level: image.to_dict() for level, image in self_images.items()
            },
            "insights": [insight.to_dict() for insight in insights],
            "self_awareness_score": self_awareness_score,
            "statistics": self.monitor.get_statistics(),
        }
        
        return results
    
    def get_autognosis_status(self) -> Dict[str, Any]:
        """
        Get current status of the autognosis system.
        
        Returns:
            Dict containing status information
        """
        status = {
            "initialized": self.initialized,
            "cycle_count": self.cycle_count,
            "last_cycle_time": self.last_cycle_time.isoformat() if self.last_cycle_time else None,
            "max_levels": self.max_levels,
            "current_level_count": len(self.modeler.current_images),
            "total_insights": len(self.processor.insights),
            "insight_history_count": len(self.processor.insight_history),
            "self_awareness_score": self.modeler.get_self_awareness_score(),
        }
        
        return status
    
    def get_self_awareness_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive self-awareness report.
        
        Returns:
            Dict containing detailed self-awareness analysis
        """
        images = self.modeler.get_all_images()
        
        # Calculate self-awareness assessment
        self_awareness_assessment = {}
        
        if images:
            # Pattern recognition capability
            total_patterns = sum(
                len(img.behavioral_patterns) 
                for img in images.values()
            )
            pattern_recognition_score = min(total_patterns / 10.0, 1.0)
            self_awareness_assessment["pattern_recognition"] = pattern_recognition_score
            
            # Performance awareness
            images_with_metrics = sum(
                1 for img in images.values() 
                if img.performance_metrics
            )
            performance_awareness_score = images_with_metrics / len(images)
            self_awareness_assessment["performance_awareness"] = performance_awareness_score
            
            # Meta-reflection depth
            total_reflections = sum(
                len(img.meta_reflections) 
                for img in images.values()
            )
            meta_reflection_score = min(total_reflections / 15.0, 1.0)
            self_awareness_assessment["meta_reflection_depth"] = meta_reflection_score
            
            # Cognitive complexity (based on max level)
            max_level = max(images.keys()) if images else 0
            cognitive_complexity_score = min((max_level + 1) / self.max_levels, 1.0)
            self_awareness_assessment["cognitive_complexity"] = cognitive_complexity_score
        
        overall_score = self.modeler.get_self_awareness_score()
        
        # Categorize self-awareness level
        if overall_score >= 0.8:
            awareness_level = "Highly Self-Aware"
        elif overall_score >= 0.6:
            awareness_level = "Moderately Self-Aware"
        elif overall_score >= 0.4:
            awareness_level = "Developing Self-Awareness"
        else:
            awareness_level = "Limited Self-Awareness"
        
        report = {
            "overall_self_awareness_score": overall_score,
            "awareness_level": awareness_level,
            "self_awareness_assessment": self_awareness_assessment,
            "hierarchical_self_images": {
                level: {
                    "confidence": img.confidence,
                    "reflection_count": len(img.meta_reflections),
                    "pattern_count": len(img.behavioral_patterns),
                    "metric_count": len(img.performance_metrics),
                    "id": img.id,
                }
                for level, img in images.items()
            },
            "recent_insights": [
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "severity": insight.severity,
                }
                for insight in self.processor.insights[-10:]  # Last 10 insights
            ],
            "statistics": self.monitor.get_statistics(),
        }
        
        return report
    
    def get_current_self_images(self) -> Dict[int, SelfImage]:
        """Get current hierarchical self-images."""
        return self.modeler.get_all_images()
    
    def get_insights(self) -> List[MetaCognitiveInsight]:
        """Get current meta-cognitive insights."""
        return self.processor.insights
    
    def format_status_output(self) -> str:
        """
        Format autognosis status as human-readable string.
        
        Returns:
            Formatted status string
        """
        status = self.get_autognosis_status()
        report = self.get_self_awareness_report()
        
        output = []
        output.append("🧠 Autognosis - Hierarchical Self-Image Building System")
        output.append(f"Status: {'running' if status['initialized'] else 'not initialized'}")
        output.append(f"Self-Image Levels: {status['current_level_count']}")
        output.append(f"Total Insights Generated: {status['total_insights']}")
        output.append(f"Cycle Count: {status['cycle_count']}")
        output.append("")
        
        # Hierarchical self-images
        if report['hierarchical_self_images']:
            output.append(f"Hierarchical Self-Images ({len(report['hierarchical_self_images'])} levels):")
            for level, data in sorted(report['hierarchical_self_images'].items()):
                output.append(
                    f"  Level {level}: Confidence {data['confidence']:.2f}, "
                    f"{data['reflection_count']} reflections [{data['id']}]"
                )
            output.append("")
        
        # Recent insights
        if report['recent_insights']:
            output.append("Recent Meta-Cognitive Insights:")
            for insight in report['recent_insights'][:5]:  # Top 5
                output.append(f"  • [{insight['type']}] {insight['description']}")
            output.append("")
        
        # Self-awareness assessment
        if report['self_awareness_assessment']:
            output.append("Self-Awareness Assessment:")
            for metric, score in report['self_awareness_assessment'].items():
                bar_length = int(score * 20)
                bar = "█" * bar_length + " " * (20 - bar_length)
                metric_name = metric.replace("_", " ").title()
                output.append(f"  {metric_name:25s} {bar} {score:.3f}")
            output.append("")
        
        output.append(
            f"Overall Self-Awareness Score: {report['overall_self_awareness_score']:.3f} "
            f"({report['awareness_level']})"
        )
        
        return "\n".join(output)
