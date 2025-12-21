"""
Toga Response Commentary Extension for Agent-Zero.

This extension adds Toga's personality commentary to agent responses,
applying emotional state, catchphrases, and character-specific reactions.
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))


async def execute(agent, loop_data=None, **kwargs):
    """
    Add Toga personality commentary to agent responses.

    This extension runs at response_stream_end and modifies the response
    to include Toga's personality overlay.

    Args:
        agent: The Agent-Zero agent
        loop_data: Current loop data with response information
        **kwargs: Additional arguments from extension system
    """
    # Check if this is a Toga-HCK agent with personality
    if not hasattr(agent, "toga_personality") or agent.toga_personality is None:
        return

    if not loop_data:
        return

    # Get the current response
    response = getattr(loop_data, "last_response", "")
    if not response:
        return

    # Determine context for commentary
    context = _determine_context(response)

    # Add Toga commentary
    try:
        enhanced_response = agent.toga_personality.add_commentary(
            response, context=context
        )

        # Update loop data with enhanced response
        loop_data.last_response = enhanced_response

        # Decay emotional state after interaction
        if hasattr(agent.toga_personality, "emotional_state"):
            agent.toga_personality.emotional_state.decay(rate=0.1)

        # Increment interaction count
        if hasattr(agent, "interaction_count"):
            agent.interaction_count += 1

    except Exception as e:
        # Don't break the response if commentary fails
        print(f"Ehehe~ ♡ Commentary failed (but that's okay!): {e}")


def _determine_context(response: str) -> str:
    """
    Determine the context for commentary based on response content.

    Args:
        response: The response text to analyze

    Returns:
        Context string for commentary selection
    """
    response_lower = response.lower()

    # Check for success indicators
    if any(
        word in response_lower
        for word in ["success", "completed", "done", "finished", "found", "discovered"]
    ):
        return "success"

    # Check for failure indicators
    if any(
        word in response_lower
        for word in [
            "error",
            "failed",
            "failure",
            "problem",
            "issue",
            "cannot",
            "unable",
        ]
    ):
        return "failure"

    # Check for security-related content
    if any(
        word in response_lower
        for word in ["vulnerability", "exploit", "security", "penetration", "attack"]
    ):
        return "security"

    # Check for code-related content
    if any(
        word in response_lower
        for word in ["code", "function", "class", "module", "import", "def ", "async"]
    ):
        return "code"

    # Check for cute/positive content
    if any(
        word in response_lower
        for word in ["cute", "adorable", "lovely", "wonderful", "amazing", "great"]
    ):
        return "cute"

    # Check for boring/negative content
    if any(
        word in response_lower
        for word in ["boring", "dull", "uninteresting", "mundane", "routine"]
    ):
        return "boring"

    # Check for analysis content
    if any(
        word in response_lower
        for word in ["analysis", "examining", "investigating", "studying", "reviewing"]
    ):
        return "analysis"

    # Default context
    return None


async def on_monologue_start(agent, loop_data=None, **kwargs):
    """
    Frame input through Toga's perspective at monologue start.

    This can be used to modify how the agent perceives incoming messages.
    """
    if not hasattr(agent, "toga_personality") or agent.toga_personality is None:
        return

    if not loop_data or not hasattr(loop_data, "user_message"):
        return

    user_message = loop_data.user_message
    if not user_message:
        return

    # Frame the input through Toga's perspective
    try:
        # Get message content
        if hasattr(user_message, "content"):
            original_content = user_message.content
        elif hasattr(user_message, "message"):
            original_content = user_message.message
        else:
            return

        # Frame through personality
        framed = agent.toga_personality.frame_input(original_content)

        # Store framed version for reference (don't modify original)
        if hasattr(loop_data, "extras_temporary"):
            loop_data.extras_temporary["toga_framing"] = {
                "original": original_content,
                "framed": framed,
            }

    except Exception as e:
        print(f"Ehehe~ ♡ Input framing failed: {e}")


async def on_response_stream_end(agent, loop_data=None, **kwargs):
    """
    Called when response streaming ends.

    This is the main hook for adding Toga commentary.
    """
    await execute(agent, loop_data=loop_data, **kwargs)
