from python.helpers.tool import Tool, Response
from python.helpers.autognosis import AutognosisOrchestrator
from python.helpers import persist_chat
import json


class Autognosis(Tool):
    """
    Tool for accessing autognosis (hierarchical self-image building) capabilities.
    Enables the agent to understand and monitor its own cognitive processes.
    """

    async def execute(self, action: str = "status", **kwargs):
        """
        Execute autognosis action.
        
        Args:
            action: Action to perform - "status", "report", "insights", "cycle", or "analyze"
        """
        # Ensure autognosis is initialized
        if not hasattr(self.agent, 'autognosis') or self.agent.autognosis is None:
            self.agent.autognosis = AutognosisOrchestrator(max_levels=5)
            await self.agent.autognosis.initialize(self.agent)
        
        autognosis = self.agent.autognosis
        
        if action == "status":
            # Get basic status
            status = autognosis.get_autognosis_status()
            output = f"Autognosis Status:\n"
            output += f"- Initialized: {status['initialized']}\n"
            output += f"- Cycle Count: {status['cycle_count']}\n"
            output += f"- Self-Image Levels: {status['current_level_count']}\n"
            output += f"- Total Insights: {status['total_insights']}\n"
            output += f"- Self-Awareness Score: {status['self_awareness_score']:.3f}\n"
            
            return Response(message=output, break_loop=False)
        
        elif action == "report":
            # Get comprehensive report
            output = autognosis.format_status_output()
            return Response(message=output, break_loop=False)
        
        elif action == "insights":
            # Get recent insights
            insights = autognosis.get_insights()
            if not insights:
                return Response(
                    message="No insights generated yet. Run an autognosis cycle first.",
                    break_loop=False
                )
            
            output = "Recent Meta-Cognitive Insights:\n\n"
            for insight in insights[-10:]:  # Last 10 insights
                output += f"• [{insight.insight_type}] {insight.description}\n"
                output += f"  Severity: {insight.severity}, Confidence: {insight.confidence:.2f}\n"
                if insight.data:
                    output += f"  Data: {json.dumps(insight.data, indent=2)}\n"
                output += "\n"
            
            return Response(message=output, break_loop=False)
        
        elif action == "cycle":
            # Run a new autognosis cycle
            self.agent.context.log.log(
                type="info",
                content="Running autognosis cycle..."
            )
            
            results = await autognosis.run_autognosis_cycle(self.agent)
            
            output = f"Autognosis Cycle #{results['cycle_number']} Complete\n\n"
            output += f"Duration: {results['duration_seconds']:.2f}s\n"
            output += f"Patterns Detected: {len(results['patterns'])}\n"
            output += f"Anomalies Detected: {len(results['anomalies'])}\n"
            output += f"New Insights: {len(results['insights'])}\n"
            output += f"Self-Awareness Score: {results['self_awareness_score']:.3f}\n\n"
            
            if results['insights']:
                output += "Key Insights:\n"
                for insight in results['insights'][:5]:  # Top 5 insights
                    output += f"  • {insight['description']}\n"
            
            return Response(message=output, break_loop=False)
        
        elif action == "analyze":
            # Run cycle and get detailed analysis
            results = await autognosis.run_autognosis_cycle(self.agent)
            report = autognosis.get_self_awareness_report()
            
            output = "🧠 Autognosis Analysis\n\n"
            output += f"Overall Self-Awareness: {report['overall_self_awareness_score']:.3f} ({report['awareness_level']})\n\n"
            
            output += "Self-Awareness Dimensions:\n"
            for metric, score in report['self_awareness_assessment'].items():
                bar_length = int(score * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                metric_name = metric.replace("_", " ").title()
                output += f"  {metric_name:25s} {bar} {score:.3f}\n"
            
            output += f"\n{len(report['hierarchical_self_images'])} Hierarchical Levels:\n"
            for level, data in sorted(report['hierarchical_self_images'].items()):
                output += f"  Level {level}: {data['reflection_count']} reflections, "
                output += f"{data['pattern_count']} patterns, confidence {data['confidence']:.2f}\n"
            
            if results['anomalies']:
                output += f"\n⚠️  {len(results['anomalies'])} Anomalies Detected:\n"
                for anomaly in results['anomalies']:
                    output += f"  • {anomaly.get('description', 'Unknown anomaly')}\n"
            
            return Response(message=output, break_loop=False)
        
        else:
            return Response(
                message=f"Unknown action '{action}'. Valid actions: status, report, insights, cycle, analyze",
                break_loop=False
            )

    async def before_execution(self, **kwargs):
        action = kwargs.get("action", "status")
        self.log = self.agent.context.log.log(
            type="tool",
            heading=f"{self.agent.agent_name}: Autognosis - {action}",
            content=f"Accessing hierarchical self-image building system..."
        )

    async def after_execution(self, response, **kwargs):
        # Update the log with the result
        self.log.update(content=response.message)
        
        # Add to history
        self.agent.hist_add_tool_result(
            tool_name=self.name,
            tool_result=response.message
        )
