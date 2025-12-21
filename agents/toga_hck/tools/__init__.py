"""
Agent-Zero-HCK Tools Package.

Provides Agent-Zero compatible tools for Toga's capabilities:
- Transform Quirk: Code absorption and system mimicry
- Security Testing: Ethical penetration testing and vulnerability assessment
"""

from .transform_quirk import (
    TransformQuirkTool,
    register_tool as register_transform_quirk,
)
from .security_test import SecurityTestTool, register_tool as register_security_test

__all__ = [
    "TransformQuirkTool",
    "SecurityTestTool",
    "register_transform_quirk",
    "register_security_test",
]


def register_all_tools(agent):
    """
    Register all Toga-HCK tools with an agent.

    Args:
        agent: The Agent-Zero agent to register tools with

    Returns:
        Dictionary of registered tools
    """
    tools = {}

    # Register Transform Quirk tool
    if hasattr(agent, "hck_config"):
        if agent.hck_config.enable_transform_quirk:
            tools["transform_quirk"] = register_transform_quirk(agent)

        if agent.hck_config.enable_security_testing:
            tools["security_test"] = register_security_test(agent)
    else:
        # Register all by default
        tools["transform_quirk"] = register_transform_quirk(agent)
        tools["security_test"] = register_security_test(agent)

    return tools
