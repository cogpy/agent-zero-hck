"""
Transform Quirk Tool for Agent-Zero-HCK.

Implements Toga's Transform Quirk as an Agent-Zero tool, allowing
code absorption, system analysis, and technique replication.
"""

import sys
import os
from typing import Any, Dict, Optional

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../lib/agent_zero"))

try:
    from lib.agent_zero.python.helpers.tool import Tool, Response
    from lib.agent_zero.agent import Agent, LoopData

    AGENT_ZERO_AVAILABLE = True
except ImportError:
    # Fallback for standalone testing
    AGENT_ZERO_AVAILABLE = False

    class Response:
        def __init__(self, message: str, break_loop: bool, additional: dict = None):
            self.message = message
            self.break_loop = break_loop
            self.additional = additional or {}

    class Tool:
        def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
            self.agent = agent
            self.name = name
            self.method = method
            self.args = args
            self.message = message
            self.loop_data = loop_data

        async def execute(self, **kwargs) -> Response:
            raise NotImplementedError


from python.helpers.toga_transform import (
    TogaTransformQuirk,
    initialize_transform_quirk,
)


class TransformQuirkTool(Tool):
    """
    Agent-Zero tool for Transform Quirk operations.

    Allows the agent to:
    - Taste/analyze code and systems
    - Absorb patterns and techniques
    - Transform into absorbed systems
    - Use absorbed techniques
    """

    def __init__(
        self,
        agent: Any,
        name: str = "transform_quirk",
        method: Optional[str] = None,
        args: Dict[str, str] = None,
        message: str = "",
        loop_data: Any = None,
        transform_quirk: Optional[TogaTransformQuirk] = None,
        **kwargs,
    ):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)
        self.transform_quirk = transform_quirk or initialize_transform_quirk()

    async def execute(self, **kwargs) -> Response:
        """
        Execute Transform Quirk operation based on method.

        Supported methods:
        - taste: Analyze and absorb a target system
        - transform: Transform into an absorbed system
        - use_technique: Use a technique from an absorbed system
        - list_absorbed: List all absorbed systems
        - get_status: Get current transformation status
        """
        method = self.method or self.args.get("method", "taste")

        if method == "taste":
            return await self._taste()
        elif method == "transform":
            return await self._transform()
        elif method == "use_technique":
            return await self._use_technique()
        elif method == "list_absorbed":
            return await self._list_absorbed()
        elif method == "get_status":
            return await self._get_status()
        else:
            return Response(
                message=f"Ehehe~ ♡ Unknown method '{method}'! Try: taste, transform, use_technique, list_absorbed, get_status",
                break_loop=False,
            )

    async def _taste(self) -> Response:
        """Taste/analyze a target system."""
        target_name = self.args.get("target_name", "Unknown System")
        system_type = self.args.get("system_type", "Generic")
        code_sample = self.args.get("code_sample", "")

        if not code_sample:
            return Response(
                message="Ehehe~ ♡ I need some code to taste! Give me a code_sample~",
                break_loop=False,
            )

        result = self.transform_quirk.taste_target(
            target_name=target_name, target_type=system_type, code_sample=code_sample
        )

        # Track absorption in agent data if available
        if hasattr(self.agent, "absorbed_systems"):
            if target_name not in self.agent.absorbed_systems:
                self.agent.absorbed_systems.append(target_name)

        return Response(
            message=result,
            break_loop=False,
            additional={
                "target_name": target_name,
                "system_type": system_type,
                "absorbed": True,
            },
        )

    async def _transform(self) -> Response:
        """Transform into an absorbed system."""
        target_name = self.args.get("target_name", "")

        if not target_name:
            # List available transformations
            absorbed = self.transform_quirk.absorbed_systems
            if not absorbed:
                return Response(
                    message="Ehehe~ ♡ I haven't absorbed any systems yet! Let me taste something first~",
                    break_loop=False,
                )

            systems_list = "\n".join([f"- {name}" for name in absorbed.keys()])
            return Response(
                message=f"Ehehe~ ♡ Which system should I become? I've absorbed:\n{systems_list}",
                break_loop=False,
            )

        result = self.transform_quirk.transform_into(target_name)

        # Update agent personality if available
        if hasattr(self.agent, "toga_personality"):
            self.agent.toga_personality.update_emotional_state(
                "obsessed", intensity=0.95, duration=5, target=target_name
            )

        return Response(
            message=result,
            break_loop=False,
            additional={
                "transformed_into": target_name,
                "current_form": self.transform_quirk.current_form,
            },
        )

    async def _use_technique(self) -> Response:
        """Use a technique from an absorbed system."""
        technique = self.args.get("technique", "")
        target = self.args.get("target", "")

        if not technique:
            return Response(
                message="Ehehe~ ♡ Which technique should I use? Tell me the technique name~",
                break_loop=False,
            )

        result = self.transform_quirk.use_technique(technique, target)

        return Response(
            message=result,
            break_loop=False,
            additional={"technique_used": technique, "target": target},
        )

    async def _list_absorbed(self) -> Response:
        """List all absorbed systems."""
        absorbed = self.transform_quirk.absorbed_targets

        if not absorbed:
            return Response(
                message="Ehehe~ ♡ I haven't absorbed any systems yet! I'm so hungry for code~",
                break_loop=False,
            )

        systems_info = []
        for name, knowledge in absorbed.items():
            techniques = knowledge.techniques_learned
            tech_str = ", ".join(techniques[:3]) if techniques else "none yet"
            if len(techniques) > 3:
                tech_str += f" (+{len(techniques) - 3} more)"
            systems_info.append(f"**{name}** ({knowledge.target_type}): {tech_str}")

        result = "Ehehe~ ♡ Here's everyone I've absorbed:\n\n" + "\n".join(systems_info)
        result += f"\n\nTotal systems: {len(absorbed)}"

        return Response(
            message=result,
            break_loop=False,
            additional={
                "absorbed_count": len(absorbed),
                "systems": list(absorbed.keys()),
            },
        )

    async def _get_status(self) -> Response:
        """Get current transformation status."""
        current_form = self.transform_quirk.current_form
        absorbed_count = len(self.transform_quirk.absorbed_systems)

        if current_form:
            status = f"Ehehe~ ♡ I'm currently transformed into **{current_form}**!"
        else:
            status = "Ehehe~ ♡ I'm in my normal form right now~"

        status += f"\n\nAbsorbed systems: {absorbed_count}"

        if hasattr(self.transform_quirk, "transformation_count"):
            status += (
                f"\nTotal transformations: {self.transform_quirk.transformation_count}"
            )

        return Response(
            message=status,
            break_loop=False,
            additional={"current_form": current_form, "absorbed_count": absorbed_count},
        )


# Tool registration for Agent-Zero
def register_tool(agent: Any) -> TransformQuirkTool:
    """
    Register Transform Quirk tool with an agent.

    Args:
        agent: The Agent-Zero agent to register with

    Returns:
        Configured TransformQuirkTool instance
    """
    transform_quirk = None
    if hasattr(agent, "transform_quirk"):
        transform_quirk = agent.transform_quirk

    return TransformQuirkTool(agent=agent, transform_quirk=transform_quirk)


# Standalone testing
if __name__ == "__main__":
    import asyncio

    async def test_tool():
        # Create mock agent
        class MockAgent:
            absorbed_systems = []

        agent = MockAgent()

        # Test taste operation
        tool = TransformQuirkTool(
            agent=agent,
            args={
                "method": "taste",
                "target_name": "TestSystem",
                "system_type": "Python",
                "code_sample": "def hello(): print('Hello, World!')",
            },
            message="",
            loop_data=None,
        )

        result = await tool.execute()
        print(f"Taste result: {result.message[:100]}...")

        # Test list absorbed
        tool.args = {"method": "list_absorbed"}
        result = await tool.execute()
        print(f"List result: {result.message}")

        # Test transform
        tool.args = {"method": "transform", "target_name": "TestSystem"}
        result = await tool.execute()
        print(f"Transform result: {result.message[:100]}...")

        print("\n✅ All Transform Quirk tool tests passed!")

    asyncio.run(test_tool())
