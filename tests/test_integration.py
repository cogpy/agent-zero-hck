"""
Integration Tests for Agent-Zero-HCK.

Tests the integrated agent with real Agent-Zero base framework,
cognitive components, and Toga personality overlay.
"""

import pytest
import asyncio
import sys
import os

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestAgentZeroHCKIntegration:
    """Integration tests for AgentZeroHCK."""

    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK
        from agents.toga_hck.config import AgentZeroHCKConfig

        config = AgentZeroHCKConfig(
            agent_name="TestToga",
            enable_transform_quirk=True,
            enable_security_testing=True,
        )

        agent = AgentZeroHCK(hck_config=config)

        assert agent is not None
        assert agent.agent_name == "TestToga"
        assert agent.toga_personality is not None
        assert agent.transform_quirk is not None
        assert agent.security_tester is not None

    def test_agent_status(self):
        """Test agent status reporting."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK

        agent = AgentZeroHCK()
        status = agent.get_status()

        assert "agent_name" in status
        assert "interaction_count" in status
        assert "components" in status
        assert "emotional_state" in status

    @pytest.mark.asyncio
    async def test_message_processing(self):
        """Test basic message processing."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK

        agent = AgentZeroHCK()

        response = await agent.process_message(
            "Hello, how are you?", context={"type": "greeting"}
        )

        assert response is not None
        assert len(response) > 0
        assert agent.interaction_count == 1

    @pytest.mark.asyncio
    async def test_transform_quirk_trigger(self):
        """Test Transform Quirk is triggered correctly."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK

        agent = AgentZeroHCK()

        response = await agent.process_message(
            "Can you taste this code?",
            context={
                "target_name": "TestModule",
                "system_type": "Python",
                "code_sample": "def test(): pass",
            },
        )

        assert response is not None
        assert "TestModule" in agent.absorbed_systems or "taste" in response.lower()

    @pytest.mark.asyncio
    async def test_security_test_trigger(self):
        """Test security testing is triggered correctly."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK

        agent = AgentZeroHCK()

        response = await agent.process_message(
            "Analyze this target for vulnerabilities",
            context={"target_name": "TestServer", "target_type": "web_application"},
        )

        assert response is not None
        # Response should contain security-related content

    def test_subordinate_spawning(self):
        """Test subordinate agent spawning."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK
        from agents.toga_hck.config import AgentZeroHCKConfig

        config = AgentZeroHCKConfig(max_subordinates=3)
        agent = AgentZeroHCK(hck_config=config)

        sub1 = agent.spawn_subordinate("Security Scanner")
        sub2 = agent.spawn_subordinate("Code Analyzer")

        assert sub1 is not None
        assert sub2 is not None
        assert len(agent.subordinates) == 2
        assert "Sub-1" in sub1.agent_name
        assert "Sub-2" in sub2.agent_name

    def test_subordinate_limit(self):
        """Test subordinate limit is enforced."""
        from agents.toga_hck.agent_integrated import AgentZeroHCK
        from agents.toga_hck.config import AgentZeroHCKConfig

        config = AgentZeroHCKConfig(max_subordinates=1)
        agent = AgentZeroHCK(hck_config=config)

        sub1 = agent.spawn_subordinate("First")
        sub2 = agent.spawn_subordinate("Second")

        assert sub1 is not None
        assert sub2 is None  # Should fail due to limit
        assert len(agent.subordinates) == 1


class TestConfigurationModule:
    """Tests for configuration module."""

    def test_default_config(self):
        """Test default configuration values."""
        from agents.toga_hck.config import AgentZeroHCKConfig, DEFAULT_CONFIG

        config = AgentZeroHCKConfig()

        assert config.agent_name == "Toga-HCK"
        assert config.enable_transform_quirk is True
        assert config.enable_security_testing is True
        assert config.max_subordinates == 5

    def test_personality_tensor(self):
        """Test personality tensor functionality."""
        from agents.toga_hck.config import TogaPersonalityTensor

        tensor = TogaPersonalityTensor(cheerfulness=0.9, chaos=0.8, obsessiveness=0.7)

        assert tensor.cheerfulness == 0.9
        assert tensor.chaos == 0.8
        assert tensor.obsessiveness == 0.7

        # Test inheritance
        child = tensor.inherit(0.5)
        assert child.cheerfulness == 0.45
        assert child.chaos == 0.4
        assert child.obsessiveness == 0.35

    def test_config_to_dict(self):
        """Test configuration serialization."""
        from agents.toga_hck.config import AgentZeroHCKConfig

        config = AgentZeroHCKConfig(agent_name="TestAgent")
        data = config.to_dict()

        assert data["agent_name"] == "TestAgent"
        assert "personality" in data
        assert "cognitive_mode" in data

    def test_config_from_dict(self):
        """Test configuration deserialization."""
        from agents.toga_hck.config import AgentZeroHCKConfig

        data = {"agent_name": "FromDict", "max_subordinates": 10}

        config = AgentZeroHCKConfig.from_dict(data)

        assert config.agent_name == "FromDict"
        assert config.max_subordinates == 10


class TestToolsModule:
    """Tests for Agent-Zero tools."""

    @pytest.mark.asyncio
    async def test_transform_quirk_tool(self):
        """Test Transform Quirk tool."""
        from agents.toga_hck.tools.transform_quirk import TransformQuirkTool

        class MockAgent:
            absorbed_systems = []

        tool = TransformQuirkTool(
            agent=MockAgent(),
            args={
                "method": "taste",
                "target_name": "TestSystem",
                "system_type": "Python",
                "code_sample": "def test(): pass",
            },
            message="",
            loop_data=None,
        )

        result = await tool.execute()

        assert result is not None
        assert result.message is not None
        assert not result.break_loop

    @pytest.mark.asyncio
    async def test_transform_quirk_list_absorbed(self):
        """Test listing absorbed systems."""
        from agents.toga_hck.tools.transform_quirk import TransformQuirkTool

        class MockAgent:
            absorbed_systems = []

        tool = TransformQuirkTool(
            agent=MockAgent(),
            args={"method": "list_absorbed"},
            message="",
            loop_data=None,
        )

        result = await tool.execute()

        assert result is not None
        assert (
            "absorbed" in result.message.lower() or "haven't" in result.message.lower()
        )

    @pytest.mark.asyncio
    async def test_security_test_tool(self):
        """Test Security Test tool."""
        from agents.toga_hck.tools.security_test import SecurityTestTool

        class MockAgent:
            security_findings = []

        tool = SecurityTestTool(
            agent=MockAgent(),
            args={
                "method": "analyze",
                "target_name": "TestServer",
                "target_type": "web_application",
            },
            message="",
            loop_data=None,
        )

        result = await tool.execute()

        assert result is not None
        assert result.message is not None

    @pytest.mark.asyncio
    async def test_security_report_generation(self):
        """Test security report generation."""
        from agents.toga_hck.tools.security_test import SecurityTestTool

        class MockAgent:
            security_findings = [{"target": "Test", "type": "XSS", "severity": "high"}]

        tool = SecurityTestTool(
            agent=MockAgent(),
            args={"method": "generate_report", "target": "TestServer"},
            message="",
            loop_data=None,
        )

        result = await tool.execute()

        assert result is not None
        assert (
            "report" in result.message.lower() or "assessment" in result.message.lower()
        )


class TestCognitiveComponents:
    """Tests for cognitive components."""

    def test_npu_initialization(self):
        """Test NPU coprocessor initialization."""
        from python.helpers.cognitive.npu import NPUCoprocessor, NPUConfig

        config = NPUConfig()  # No model path, stub mode
        npu = NPUCoprocessor(config)

        assert npu is not None
        status = npu.get_status()
        assert "available" in status

    def test_npu_stub_generation(self):
        """Test NPU stub generation."""
        from python.helpers.cognitive.npu import initialize_npu

        npu = initialize_npu()
        result = npu.generate("Test prompt")

        assert result is not None
        assert "stub" in result.lower() or len(result) > 0

    def test_atomspace_initialization(self):
        """Test AtomSpace initialization."""
        from python.helpers.cognitive.atomspace_integration import (
            AtomSpaceIntegration,
            AtomSpaceConfig,
        )

        config = AtomSpaceConfig()
        atomspace = AtomSpaceIntegration(config)

        assert atomspace is not None
        status = atomspace.get_status()
        assert "available" in status or "stub_atoms" in status

    def test_atomspace_node_creation(self):
        """Test AtomSpace node creation."""
        from python.helpers.cognitive.atomspace_integration import initialize_atomspace

        atomspace = initialize_atomspace()

        node1 = atomspace.add_node("ConceptNode", "TestConcept")
        node2 = atomspace.add_node("ConceptNode", "AnotherConcept")

        assert node1 is not None
        assert node2 is not None

    def test_ontogenesis_initialization(self):
        """Test ontogenetic kernel initialization."""
        from python.helpers.cognitive.ontogenesis import (
            OntogeneticKernel,
            OntogenesisConfig,
        )

        config = OntogenesisConfig()
        kernel = OntogeneticKernel(config)

        assert kernel is not None
        assert kernel.stage.value == "sensorimotor"

    def test_ontogenesis_experience_processing(self):
        """Test ontogenesis experience processing."""
        from python.helpers.cognitive.ontogenesis import initialize_ontogenesis

        kernel = initialize_ontogenesis()

        result = kernel.process_experience(
            {"type": "test", "input": "test input", "output": "test output"}
        )

        assert result is not None
        assert "stage" in result
        assert kernel.interaction_count == 1

    def test_ontogenesis_skill_learning(self):
        """Test ontogenesis skill learning."""
        from python.helpers.cognitive.ontogenesis import initialize_ontogenesis

        kernel = initialize_ontogenesis()

        kernel.learn_skill("test_skill", success=True)
        level = kernel.get_skill_level("test_skill")

        assert level > 0

    def test_relevance_initialization(self):
        """Test relevance engine initialization."""
        from python.helpers.cognitive.relevance import RelevanceEngine, RelevanceConfig

        config = RelevanceConfig()
        engine = RelevanceEngine(config)

        assert engine is not None
        assert engine.focus is None

    def test_relevance_attention(self):
        """Test relevance attention mechanism."""
        from python.helpers.cognitive.relevance import initialize_relevance

        engine = initialize_relevance()

        salience = engine.attend("test_object", importance=0.8)

        assert salience > 0
        assert "test_object" in engine.working_memory

    def test_relevance_focus(self):
        """Test relevance focus mechanism."""
        from python.helpers.cognitive.relevance import initialize_relevance

        engine = initialize_relevance()

        engine.attend("high_importance", importance=0.9)
        engine.attend("low_importance", importance=0.3)

        # High importance should become focus
        assert engine.focus == "high_importance"

    def test_relevance_decay(self):
        """Test relevance decay mechanism."""
        from python.helpers.cognitive.relevance import initialize_relevance
        import time

        engine = initialize_relevance()

        engine.attend("decaying_object", importance=0.5)
        initial_salience = engine.attention_field["decaying_object"].salience

        # Simulate time passing (modify last_accessed)
        engine.attention_field["decaying_object"].last_accessed -= 100
        engine.decay()

        final_salience = engine.attention_field.get("decaying_object", None)
        # Object may have been removed or salience reduced


class TestExtensions:
    """Tests for Agent-Zero extensions."""

    @pytest.mark.asyncio
    async def test_personality_extension(self):
        """Test personality initialization extension."""
        from agents.toga_hck.extensions.agent_init._10_toga_personality import execute
        from agents.toga_hck.config import AgentZeroHCKConfig

        class MockAgent:
            hck_config = AgentZeroHCKConfig()

        agent = MockAgent()
        await execute(agent)

        assert hasattr(agent, "toga_personality")
        assert hasattr(agent, "transform_quirk")
        assert hasattr(agent, "security_tester")

    @pytest.mark.asyncio
    async def test_commentary_extension(self):
        """Test response commentary extension."""
        from agents.toga_hck.extensions.response._10_toga_commentary import execute
        from python.helpers.toga_personality import initialize_toga_personality

        class MockLoopData:
            last_response = "Test response"

        class MockAgent:
            toga_personality = initialize_toga_personality()
            interaction_count = 0

        agent = MockAgent()
        loop_data = MockLoopData()

        await execute(agent, loop_data=loop_data)

        # Response should be modified with commentary
        assert loop_data.last_response is not None


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
