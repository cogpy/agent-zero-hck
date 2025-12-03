"""
OpenCog Cognitive Integration Extension
Automatically manages cognitive state and knowledge representation during agent operation
"""

from python.helpers.extension import Extension
from python.helpers import opencog_atomspace
from python.helpers.print_style import PrintStyle


class OpenCogIntegration(Extension):
    """Extension that integrates OpenCog cognitive architecture into agent operations"""
    
    async def execute(self, loop_data, **kwargs):
        """
        Execute cognitive integration:
        - Initialize agent's AtomSpace if needed
        - Create concept node for the agent
        - Track agent state and evolution
        """
        
        orchestrator = opencog_atomspace.get_orchestrator()
        agent_id = f"agent_{self.agent.number}"
        
        # Get or create agent's AtomSpace
        atomspace = orchestrator.get_agent_space(agent_id)
        
        if not atomspace:
            # Create new AtomSpace for this agent
            space_name = f"space_{agent_id}"
            atomspace = orchestrator.create_atomspace(space_name)
            orchestrator.assign_agent_space(agent_id, space_name)
            
            # Create concept node for this agent
            agent_node = atomspace.add_node(
                node_type="ConceptNode",
                name=agent_id,
                truth_value=(1.0, 1.0),
                attention_value=0.8,
                metadata={
                    "agent_number": self.agent.number,
                    "agent_name": self.agent.agent_name,
                    "role": "autonomous_agent"
                }
            )
            
            # Create iteration tracking node
            iteration_node = atomspace.add_node(
                node_type="NumberNode",
                name=f"{agent_id}_iteration",
                truth_value=(1.0, 1.0),
                metadata={"value": 0}
            )
            
            # Link agent to iteration
            atomspace.add_link(
                link_type="StateLink",
                outgoing=[agent_node.id, iteration_node.id],
                name=f"{agent_id}_state"
            )
            
            # PrintStyle(font_color="cyan", padding=False).print(
            #     f"OpenCog: Initialized cognitive space for {self.agent.agent_name}"
            # )
        
        # Update iteration count
        iteration = loop_data.iteration
        iteration_node = atomspace.get_atom_by_name(f"{agent_id}_iteration")
        if iteration_node:
            iteration_node.metadata["value"] = iteration
            # Increase attention as iterations progress
            atomspace.update_attention(iteration_node.id, 0.01)
        
        # Track if this is a user message
        if loop_data.user_message:
            # Create node for user interaction
            interaction_node = atomspace.add_node(
                node_type="ConceptNode",
                name=f"{agent_id}_interaction_{iteration}",
                truth_value=(1.0, 1.0),
                attention_value=0.7,
                metadata={
                    "iteration": iteration,
                    "type": "user_interaction"
                }
            )
            
            # Link agent to interaction
            agent_node = atomspace.get_atom_by_name(agent_id)
            if agent_node:
                atomspace.add_link(
                    link_type="EvaluationLink",
                    outgoing=[agent_node.id, interaction_node.id],
                    name=f"{agent_id}_eval_{iteration}"
                )
                
                # Spread activation from the interaction
                atomspace.spread_activation(interaction_node.id, intensity=0.15, decay=0.7)
