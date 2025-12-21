"""
Agent-Zero-HCK: Himiko Toga Cognitive Kernel (Integrated)

Full integration with Agent-Zero base framework, replacing all stub
implementations with real functionality.
"""

import sys
import os
from typing import Optional, Dict, Any, List
import asyncio

# Add paths for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.join(_current_dir, "../..")
_lib_path = os.path.join(_project_root, "lib/agent_zero")

sys.path.insert(0, _project_root)
sys.path.insert(0, _lib_path)

# Import Agent-Zero base framework
AGENT_ZERO_AVAILABLE = False
try:
    from lib.agent_zero.agent import Agent, AgentConfig, AgentContext, LoopData
    from lib.agent_zero.python.helpers.tool import Tool, Response
    from lib.agent_zero.python.helpers import history

    AGENT_ZERO_AVAILABLE = True
    print("Agent-Zero base framework loaded successfully")
except ImportError as e:
    print(f"Warning: Agent-Zero base not found ({e}), using compatibility layer")

    # Compatibility layer for standalone operation
    class Agent:
        """Compatibility Agent class for standalone operation."""

        DATA_NAME_SUPERIOR = "_superior"
        DATA_NAME_SUBORDINATE = "_subordinate"

        def __init__(self, number: int = 0, config=None, context=None):
            self.number = number
            self.config = config
            self.context = context
            self.agent_name = f"A{number}"
            self.data = {}
            self.history = []
            self.intervention = None

        async def monologue(self):
            """Stub monologue for compatibility."""
            return "Agent-Zero base not available"

        def get_data(self, field: str):
            return self.data.get(field)

        def set_data(self, field: str, value):
            self.data[field] = value

    class AgentConfig:
        """Compatibility AgentConfig class."""

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class AgentContext:
        """Compatibility AgentContext class."""

        def __init__(self, config=None, **kwargs):
            self.config = config
            self.data = {}
            self.id = "standalone"

    class LoopData:
        """Compatibility LoopData class."""

        def __init__(self, **kwargs):
            self.iteration = 0
            self.last_response = ""
            for k, v in kwargs.items():
                setattr(self, k, v)

    class Tool:
        """Compatibility Tool class."""

        def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
            self.agent = agent
            self.name = name
            self.method = method
            self.args = args
            self.message = message
            self.loop_data = loop_data

        async def execute(self, **kwargs):
            raise NotImplementedError

    class Response:
        """Compatibility Response class."""

        def __init__(self, message: str, break_loop: bool, additional: dict = None):
            self.message = message
            self.break_loop = break_loop
            self.additional = additional or {}


# Import Toga components
from python.helpers.toga_personality import (
    TogaPersonality,
    initialize_toga_personality,
)
from python.helpers.toga_transform import (
    TogaTransformQuirk,
    initialize_transform_quirk,
)
from python.helpers.toga_security import (
    TogaSecurityTester,
    initialize_toga_security_tester,
)

# Import configuration
from agents.toga_hck.config import (
    AgentZeroHCKConfig,
    TogaPersonalityTensor,
    CognitiveMode,
)

# Import cognitive components
from python.helpers.cognitive import (
    NPUCoprocessor,
    initialize_npu,
    AtomSpaceIntegration,
    initialize_atomspace,
    OntogeneticKernel,
    initialize_ontogenesis,
    RelevanceEngine,
    initialize_relevance,
)


class AgentZeroHCK(Agent):
    """
    Agent-Zero-HCK: Advanced multi-agent system with Toga personality.

    Fully integrated with Agent-Zero base framework, providing:
    - Agent-Zero's orchestration and tool ecosystem
    - Toga's personality, Transform Quirk, and security testing
    - Optional NPU coprocessor integration
    - Optional cognitive architecture enhancements (AtomSpace, etc.)
    """

    def __init__(
        self,
        number: int = 0,
        config: Optional[AgentConfig] = None,
        context: Optional[AgentContext] = None,
        hck_config: Optional[AgentZeroHCKConfig] = None,
    ):
        """
        Initialize Agent-Zero-HCK with Toga personality overlay.

        Args:
            number: Agent number in hierarchy
            config: Agent-Zero configuration
            context: Agent-Zero context
            hck_config: Toga-HCK specific configuration
        """
        # Initialize HCK config first (needed for base init)
        self.hck_config = hck_config or AgentZeroHCKConfig()

        # Initialize base Agent-Zero
        super().__init__(number, config, context)

        # Override agent name with Toga name
        self.agent_name = self.hck_config.agent_name

        # Initialize Toga personality
        personality_dict = None
        if self.hck_config.personality_tensor:
            personality_dict = self.hck_config.personality_tensor.to_dict()
        self.toga_personality = initialize_toga_personality(personality_dict)

        # Initialize Transform Quirk
        if self.hck_config.enable_transform_quirk:
            self.transform_quirk = initialize_transform_quirk()
        else:
            self.transform_quirk = None

        # Initialize Security Tester
        if self.hck_config.enable_security_testing:
            self.security_tester = initialize_toga_security_tester()
        else:
            self.security_tester = None

        # Initialize cognitive components based on mode
        self._initialize_cognitive_components()

        # Tracking variables
        self.subordinates: List["AgentZeroHCK"] = []
        self.interaction_count = 0
        self.absorbed_systems: List[str] = []
        self.security_findings: List[Dict] = []

        print(f"Ehehe~ ♡ {self.agent_name} initialized!")
        print(
            f"  Agent-Zero Base: {'Available' if AGENT_ZERO_AVAILABLE else 'Compatibility Mode'}"
        )
        print(f"  Transform Quirk: {'Enabled' if self.transform_quirk else 'Disabled'}")
        print(
            f"  Security Testing: {'Enabled' if self.security_tester else 'Disabled'}"
        )
        print(f"  Cognitive Mode: {self.hck_config.cognitive_mode.value}")

    def _initialize_cognitive_components(self):
        """Initialize cognitive components based on configuration."""
        mode = self.hck_config.cognitive_mode

        # NPU Coprocessor
        if mode in [CognitiveMode.COGNITIVE, CognitiveMode.FULL]:
            if self.hck_config.npu_config.enabled:
                self.npu = initialize_npu(vars(self.hck_config.npu_config))
            else:
                self.npu = None
        else:
            self.npu = None

        # AtomSpace
        if mode in [CognitiveMode.COGNITIVE, CognitiveMode.FULL]:
            if self.hck_config.atomspace_config.enabled:
                self.atomspace = initialize_atomspace(
                    vars(self.hck_config.atomspace_config)
                )
            else:
                self.atomspace = None
        else:
            self.atomspace = None

        # Ontogenesis
        if mode == CognitiveMode.FULL:
            if self.hck_config.ontogenesis_config.enabled:
                self.ontogenetic_kernel = initialize_ontogenesis(
                    vars(self.hck_config.ontogenesis_config)
                )
            else:
                self.ontogenetic_kernel = None
        else:
            self.ontogenetic_kernel = None

        # Relevance Realization
        if mode in [
            CognitiveMode.ENHANCED,
            CognitiveMode.COGNITIVE,
            CognitiveMode.FULL,
        ]:
            if self.hck_config.relevance_config.enabled:
                self.relevance_engine = initialize_relevance(
                    vars(self.hck_config.relevance_config)
                )
            else:
                self.relevance_engine = None
        else:
            self.relevance_engine = None

    async def process_message(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process message through Toga personality and Agent-Zero orchestration.

        Args:
            message: User message
            context: Optional context dictionary

        Returns:
            Enhanced response with Toga personality
        """
        self.interaction_count += 1

        # Step 1: Update relevance engine
        if self.relevance_engine:
            self.relevance_engine.attend("user_message", importance=0.9)

        # Step 2: Frame input through Toga's perspective
        framed_message = self.toga_personality.frame_input(message, context)

        # Step 3: Check for Transform Quirk triggers
        if self.transform_quirk and self._is_code_absorption_request(message):
            return await self._handle_transform_quirk(message, context)

        # Step 4: Check for security testing triggers
        if self.security_tester and self._is_security_test_request(message):
            return await self._handle_security_test(message, context)

        # Step 5: Process through Agent-Zero orchestration
        if AGENT_ZERO_AVAILABLE:
            response = await self._agent_zero_process(framed_message, context)
        else:
            response = self._standalone_process(framed_message, context)

        # Step 6: Process through ontogenetic kernel
        if self.ontogenetic_kernel:
            self.ontogenetic_kernel.process_experience(
                {
                    "type": "interaction",
                    "input": message,
                    "output": response,
                    "context": context,
                }
            )

        # Step 7: Add Toga commentary
        enhanced_response = self.toga_personality.add_commentary(
            response, context=self._determine_context(response)
        )

        # Step 8: Emotional state decay
        self.toga_personality.emotional_state.decay(rate=0.1)

        return enhanced_response

    def _is_code_absorption_request(self, message: str) -> bool:
        """Check if message is requesting code absorption."""
        triggers = [
            "taste",
            "absorb",
            "transform",
            "become",
            "analyze code",
            "learn from",
            "study system",
        ]
        return any(trigger in message.lower() for trigger in triggers)

    def _is_security_test_request(self, message: str) -> bool:
        """Check if message is requesting security testing."""
        triggers = [
            "security test",
            "penetration test",
            "vulnerability",
            "exploit",
            "hack",
            "assess security",
            "find vulnerabilities",
        ]
        return any(trigger in message.lower() for trigger in triggers)

    async def _handle_transform_quirk(
        self, message: str, context: Optional[Dict] = None
    ) -> str:
        """Handle Transform Quirk operations."""
        context = context or {}

        if "taste" in message.lower():
            target_name = context.get("target_name", "Unknown System")
            system_type = context.get("system_type", "Generic")
            code_sample = context.get("code_sample", "")

            result = self.transform_quirk.taste_target(
                target_name, system_type, code_sample
            )

            if target_name not in self.absorbed_systems:
                self.absorbed_systems.append(target_name)

            # Update relevance
            if self.relevance_engine:
                self.relevance_engine.attend(target_name, importance=0.95)

            return result

        elif "transform" in message.lower():
            target_name = context.get("target_name", "")

            if not target_name and self.absorbed_systems:
                target_name = self.absorbed_systems[-1]

            result = self.transform_quirk.transform_into(target_name)

            self.toga_personality.update_emotional_state(
                "obsessed", intensity=0.95, duration=5, target=target_name
            )

            return result

        elif "use technique" in message.lower():
            technique = context.get("technique", "")
            target = context.get("target", "")
            return self.transform_quirk.use_technique(technique, target)

        return "Ehehe~ ♡ I need more details about what you want me to do with my Transform Quirk!"

    async def _handle_security_test(
        self, message: str, context: Optional[Dict] = None
    ) -> str:
        """Handle security testing operations."""
        context = context or {}

        if "analyze" in message.lower() or "target" in message.lower():
            target_name = context.get("target_name", "Unknown Target")
            target_type = context.get("target_type", "system")

            result = self.security_tester.analyze_target(target_name, target_type)

            self.toga_personality.update_emotional_state(
                "obsessed", intensity=0.90, duration=3, target=target_name
            )

            # Update relevance
            if self.relevance_engine:
                self.relevance_engine.attend(f"security:{target_name}", importance=0.9)

            return result

        elif "vulnerability" in message.lower():
            target = context.get("target", "Unknown")
            vuln_type = context.get("vulnerability_type", "Unknown")
            severity = context.get("severity", "medium")

            result = self.security_tester.vulnerability_found(
                target, vuln_type, severity
            )

            self.security_findings.append(
                {"target": target, "type": vuln_type, "severity": severity}
            )

            return result

        elif "exploit" in message.lower():
            target = context.get("target", "Unknown")
            payload = context.get("payload", "Unknown")
            return self.security_tester.exploit_success(target, payload)

        return "Ehehe~ ♡ Tell me what system you want me to test! I promise to be thorough~"

    async def _agent_zero_process(
        self, message: str, context: Optional[Dict] = None
    ) -> str:
        """
        Process message through Agent-Zero orchestration.

        Uses the real Agent-Zero monologue loop when available.
        """
        if not AGENT_ZERO_AVAILABLE:
            return self._standalone_process(message, context)

        try:
            # Use Agent-Zero's monologue
            response = await self.monologue()
            return response if response else f"[Processed] {message}"
        except Exception as e:
            print(f"Agent-Zero processing error: {e}")
            return self._standalone_process(message, context)

    def _standalone_process(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Standalone processing when Agent-Zero base is not available.

        Provides basic functionality without the full orchestration.
        """
        # Use NPU if available
        if self.npu and self.npu.available:
            return self.npu.generate(message, max_tokens=256)

        # Basic response
        return f"[Standalone Mode] Processing: {message}"

    def _determine_context(self, response: str) -> str:
        """Determine context for commentary based on response content."""
        response_lower = response.lower()

        if any(word in response_lower for word in ["success", "completed", "done"]):
            return "success"
        elif any(word in response_lower for word in ["error", "failed", "problem"]):
            return "failure"
        elif any(word in response_lower for word in ["vulnerability", "security"]):
            return "security"
        elif any(word in response_lower for word in ["code", "function", "class"]):
            return "code"
        else:
            return None

    def spawn_subordinate(
        self,
        role: str,
        personality_inheritance: float = 0.7,
        config_override: Optional[Dict] = None,
    ) -> Optional["AgentZeroHCK"]:
        """
        Spawn a subordinate agent with inherited personality.

        Args:
            role: Role/purpose of subordinate
            personality_inheritance: How much personality to inherit (0-1)
            config_override: Optional config overrides

        Returns:
            New subordinate agent or None if limit reached
        """
        if len(self.subordinates) >= self.hck_config.max_subordinates:
            return None

        # Inherit personality
        child_tensor = self.hck_config.personality_tensor.inherit(
            personality_inheritance
        )

        # Create config for child
        child_config = AgentZeroHCKConfig(
            personality_tensor=child_tensor,
            enable_transform_quirk=self.hck_config.enable_transform_quirk,
            enable_security_testing=self.hck_config.enable_security_testing,
            agent_name=f"{self.hck_config.agent_name}-Sub-{len(self.subordinates)+1}",
            agent_role=role,
            max_subordinates=0,
        )

        # Apply overrides
        if config_override:
            for key, value in config_override.items():
                if hasattr(child_config, key):
                    setattr(child_config, key, value)

        # Create subordinate
        subordinate = AgentZeroHCK(
            number=self.number + len(self.subordinates) + 1,
            config=self.config,
            context=self.context,
            hck_config=child_config,
        )

        self.subordinates.append(subordinate)
        return subordinate

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        status = {
            "agent_name": self.agent_name,
            "agent_zero_available": AGENT_ZERO_AVAILABLE,
            "interaction_count": self.interaction_count,
            "subordinates": len(self.subordinates),
            "absorbed_systems": len(self.absorbed_systems),
            "security_findings": len(self.security_findings),
            "cognitive_mode": self.hck_config.cognitive_mode.value,
            "components": {
                "transform_quirk": self.transform_quirk is not None,
                "security_tester": self.security_tester is not None,
                "npu": self.npu is not None and getattr(self.npu, "available", False),
                "atomspace": self.atomspace is not None,
                "ontogenesis": self.ontogenetic_kernel is not None,
                "relevance": self.relevance_engine is not None,
            },
        }

        # Add emotional state
        if self.toga_personality:
            status["emotional_state"] = {
                "current": self.toga_personality.emotional_state.type,
                "intensity": self.toga_personality.emotional_state.intensity,
            }

        return status


def main():
    """Main entry point for Agent-Zero-HCK."""
    print("=" * 60)
    print("Agent-Zero-HCK: Himiko Toga Cognitive Kernel")
    print("=" * 60)

    # Create agent with default configuration
    agent = AgentZeroHCK()

    print("\nAgent Status:")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Test message processing
    async def test():
        print("\n--- Testing Message Processing ---")

        response = await agent.process_message(
            "Hello! Can you help me analyze some code?", context={"type": "greeting"}
        )
        print(f"\nResponse: {response}")

        print("\n--- Testing Transform Quirk ---")
        response = await agent.process_message(
            "Can you taste this Python code?",
            context={
                "target_name": "TestModule",
                "system_type": "Python",
                "code_sample": "def hello(): print('Hello!')",
            },
        )
        print(f"\nResponse: {response[:200]}...")

        print("\n--- Testing Security Analysis ---")
        response = await agent.process_message(
            "Analyze this target for vulnerabilities",
            context={"target_name": "TestServer", "target_type": "web_application"},
        )
        print(f"\nResponse: {response[:200]}...")

    asyncio.run(test())

    print("\n" + "=" * 60)
    print("Agent-Zero-HCK test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
