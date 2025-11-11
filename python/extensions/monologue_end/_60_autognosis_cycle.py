"""
Autognosis Extension - Periodic Self-Awareness Cycles

Runs autognosis cycles at the end of monologue to maintain hierarchical self-images
and generate meta-cognitive insights about agent behavior.
"""

from python.helpers.extension import Extension
from python.helpers.autognosis import AutognosisOrchestrator


class AutognosisCycle(Extension):
    """Extension to run autognosis cycles periodically."""
    
    async def execute(self, **kwargs):
        """
        Execute autognosis cycle at end of monologue.
        
        Args:
            **kwargs: Keyword arguments including loop_data
        """
        loop_data = kwargs.get('loop_data')
        
        # Only run for Agent 0 to avoid overhead on subordinates
        if self.agent.number != 0:
            return
        
        # Initialize autognosis if needed
        if not hasattr(self.agent, 'autognosis') or self.agent.autognosis is None:
            self.agent.autognosis = AutognosisOrchestrator(max_levels=5)
            await self.agent.autognosis.initialize(self.agent)
        
        # Run autognosis cycle every 5 monologues to avoid excessive overhead
        cycle_count = self.agent.autognosis.cycle_count
        
        # Run initial cycle, then every 5th iteration
        should_run = cycle_count == 0
        if loop_data and hasattr(loop_data, 'iterations'):
            should_run = should_run or (loop_data.iterations % 5 == 0)
        
        if should_run:
            try:
                # Run silent autognosis cycle in background
                await self.agent.autognosis.run_autognosis_cycle(self.agent)
                
                # Optionally log high-severity insights
                insights = self.agent.autognosis.get_insights()
                high_severity = [i for i in insights if i.severity == "high"]
                
                if high_severity:
                    self.agent.context.log.log(
                        type="info",
                        heading="Autognosis Alert",
                        content=f"Detected {len(high_severity)} high-severity self-awareness insights"
                    )
            except Exception as e:
                # Don't let autognosis failures interrupt agent operation
                self.agent.context.log.log(
                    type="warning",
                    content=f"Autognosis cycle failed: {str(e)}"
                )
