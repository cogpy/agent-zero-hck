"""
SelfMonitor - System State Observation and Pattern Detection

Responsible for continuous observation of system states, behaviors, and performance.
Detects patterns, anomalies, and trends in agent behavior.
"""

import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque
import statistics


class SelfMonitor:
    """
    Monitors agent system states and behaviors in real-time.
    """
    
    def __init__(self, history_size: int = 100):
        """
        Initialize the self-monitor.
        
        Args:
            history_size: Number of historical observations to maintain
        """
        self.history_size = history_size
        self.observations = deque(maxlen=history_size)
        self.patterns = []
        self.anomalies = []
        self.start_time = time.time()
        
    def observe_system(self, agent) -> Dict[str, Any]:
        """
        Observe current system state and behaviors.
        
        Args:
            agent: The agent instance to observe
            
        Returns:
            Dict containing observation data
        """
        observation = {
            "timestamp": datetime.now().isoformat(),
            "agent_number": agent.number,
            "agent_name": agent.agent_name,
            "history_length": len(agent.history.messages),
            "intervention_status": agent.intervention is not None,
            "data_keys": list(agent.data.keys()) if hasattr(agent, 'data') else [],
            "uptime_seconds": time.time() - self.start_time,
        }
        
        # Track context information if available
        if hasattr(agent, 'context'):
            observation["context_id"] = agent.context.id
            observation["context_paused"] = agent.context.paused
            if hasattr(agent.context, 'streaming_agent'):
                observation["streaming_active"] = agent.context.streaming_agent is not None
        
        # Track loop data if available
        if hasattr(agent, 'loop_data'):
            observation["iterations"] = getattr(agent.loop_data, 'iterations', 0)
            observation["consecutive_tools"] = getattr(agent.loop_data, 'consecutive_tools', 0)
        
        self.observations.append(observation)
        return observation
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """
        Detect behavioral patterns in historical observations.
        
        Returns:
            List of detected patterns
        """
        if len(self.observations) < 5:
            return []
        
        patterns = []
        
        # Pattern: Increasing history length
        recent_lengths = [obs.get("history_length", 0) for obs in list(self.observations)[-10:]]
        if len(recent_lengths) >= 5:
            if all(recent_lengths[i] <= recent_lengths[i+1] for i in range(len(recent_lengths)-1)):
                patterns.append({
                    "type": "increasing_history",
                    "description": "Agent history is consistently growing",
                    "severity": "low",
                    "data": {"current_length": recent_lengths[-1]}
                })
        
        # Pattern: High iteration count
        recent_iterations = [obs.get("iterations", 0) for obs in list(self.observations)[-5:]]
        if recent_iterations and max(recent_iterations) > 10:
            patterns.append({
                "type": "high_iterations",
                "description": "Agent performing many iterations",
                "severity": "medium",
                "data": {"max_iterations": max(recent_iterations)}
            })
        
        # Pattern: Consistent tool usage
        recent_consecutive = [obs.get("consecutive_tools", 0) for obs in list(self.observations)[-5:]]
        if recent_consecutive and statistics.mean(recent_consecutive) > 3:
            patterns.append({
                "type": "consistent_tool_usage",
                "description": "Agent consistently using tools",
                "severity": "low",
                "data": {"avg_consecutive": statistics.mean(recent_consecutive)}
            })
        
        self.patterns = patterns
        return patterns
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        Identify anomalies in system behavior.
        
        Returns:
            List of detected anomalies
        """
        if len(self.observations) < 10:
            return []
        
        anomalies = []
        
        # Anomaly: Sudden spike in history length
        recent_lengths = [obs.get("history_length", 0) for obs in list(self.observations)[-10:]]
        if len(recent_lengths) >= 2:
            if recent_lengths[-1] > recent_lengths[-2] * 2:
                anomalies.append({
                    "type": "history_spike",
                    "description": "Sudden doubling in history length",
                    "severity": "medium",
                    "data": {
                        "previous": recent_lengths[-2],
                        "current": recent_lengths[-1]
                    }
                })
        
        # Anomaly: Paused state detected
        if self.observations and self.observations[-1].get("context_paused"):
            anomalies.append({
                "type": "paused_state",
                "description": "Agent context is paused",
                "severity": "high",
                "data": {}
            })
        
        self.anomalies = anomalies
        return anomalies
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistical summary of observations.
        
        Returns:
            Dict containing statistical data
        """
        if not self.observations:
            return {}
        
        history_lengths = [obs.get("history_length", 0) for obs in self.observations]
        iterations = [obs.get("iterations", 0) for obs in self.observations]
        
        stats = {
            "total_observations": len(self.observations),
            "uptime_seconds": time.time() - self.start_time,
            "avg_history_length": statistics.mean(history_lengths) if history_lengths else 0,
            "max_history_length": max(history_lengths) if history_lengths else 0,
            "avg_iterations": statistics.mean(iterations) if iterations else 0,
            "max_iterations": max(iterations) if iterations else 0,
            "pattern_count": len(self.patterns),
            "anomaly_count": len(self.anomalies),
        }
        
        return stats
