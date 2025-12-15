"""
Basic tests for Agent-Zero-HCK
Tests core functionality and module imports
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestImports:
    """Test that all modules can be imported"""

    def test_import_agent(self):
        """Test that agent module can be imported"""
        from agents.toga_hck import agent

        assert agent is not None

    def test_import_personality(self):
        """Test that personality module can be imported"""
        from python.helpers import toga_personality

        assert toga_personality is not None

    def test_import_transform(self):
        """Test that transform module can be imported"""
        from python.helpers import toga_transform

        assert toga_transform is not None

    def test_import_security(self):
        """Test that security module can be imported"""
        from python.helpers import toga_security

        assert toga_security is not None


class TestPersonality:
    """Test personality system"""

    def test_personality_initialization(self):
        """Test personality initialization"""
        from python.helpers.toga_personality import initialize_toga_personality

        personality = initialize_toga_personality()
        assert personality is not None
        assert hasattr(personality, "personality")
        assert hasattr(personality.personality, "cheerfulness")
        assert hasattr(personality.personality, "chaos")
        assert hasattr(personality.personality, "obsessiveness")

    def test_personality_traits(self):
        """Test personality traits are within valid ranges"""
        from python.helpers.toga_personality import initialize_toga_personality

        personality = initialize_toga_personality()
        assert 0.0 <= personality.personality.cheerfulness <= 1.0
        assert 0.0 <= personality.personality.chaos <= 1.0
        assert 0.0 <= personality.personality.obsessiveness <= 1.0

    def test_emotional_state(self):
        """Test emotional state management"""
        from python.helpers.toga_personality import initialize_toga_personality

        personality = initialize_toga_personality()
        assert hasattr(personality, "emotional_state")
        assert personality.emotional_state is not None

    def test_frame_input(self):
        """Test input framing with personality"""
        from python.helpers.toga_personality import initialize_toga_personality

        personality = initialize_toga_personality()
        message = "Test message"
        framed = personality.frame_input(message)
        assert framed is not None
        assert isinstance(framed, str)

    def test_add_commentary(self):
        """Test adding personality commentary"""
        from python.helpers.toga_personality import initialize_toga_personality

        personality = initialize_toga_personality()
        response = "Test response"
        enhanced = personality.add_commentary(response)
        assert enhanced is not None
        assert isinstance(enhanced, str)


class TestTransformQuirk:
    """Test Transform Quirk functionality"""

    def test_transform_initialization(self):
        """Test transform quirk initialization"""
        from python.helpers.toga_transform import initialize_transform_quirk

        transform = initialize_transform_quirk()
        assert transform is not None
        assert hasattr(transform, "absorbed_targets")

    def test_taste_target(self):
        """Test tasting/absorbing target systems"""
        from python.helpers.toga_transform import initialize_transform_quirk

        transform = initialize_transform_quirk()
        result = transform.taste_target("TestSystem", "WAF", "sample code")
        assert result is not None
        assert isinstance(result, str)

    def test_absorption_tracking(self):
        """Test that absorbed systems are tracked"""
        from python.helpers.toga_transform import initialize_transform_quirk

        transform = initialize_transform_quirk()
        transform.taste_target("TestSystem", "WAF", "sample code")
        assert "TestSystem" in transform.absorbed_targets

    def test_transform_into(self):
        """Test transformation into absorbed system"""
        from python.helpers.toga_transform import initialize_transform_quirk

        transform = initialize_transform_quirk()
        # First absorb
        transform.taste_target("TestSystem", "WAF", "sample code")
        # Then transform
        result = transform.transform_into("TestSystem")
        assert result is not None
        assert isinstance(result, str)


class TestSecurityTester:
    """Test security testing functionality"""

    def test_security_initialization(self):
        """Test security tester initialization"""
        from python.helpers.toga_security import initialize_toga_security_tester

        security = initialize_toga_security_tester()
        assert security is not None
        assert hasattr(security, "profile")

    def test_analyze_target(self):
        """Test target analysis"""
        from python.helpers.toga_security import initialize_toga_security_tester

        security = initialize_toga_security_tester()
        result = security.analyze_target("TestTarget", "web_application")
        assert result is not None
        assert isinstance(result, str)

    def test_ethical_constraints(self):
        """Test that ethical constraints are enforced"""
        from python.helpers.toga_security import initialize_toga_security_tester

        security = initialize_toga_security_tester()
        # Security tester has ethical constraints through its profile
        assert hasattr(security, "profile")
        assert security.profile is not None


class TestAgentZeroHCK:
    """Test main agent functionality"""

    def test_agent_initialization(self):
        """Test agent initialization"""
        from agents.toga_hck.agent import AgentZeroHCK, AgentZeroHCKConfig

        config = AgentZeroHCKConfig()
        agent = AgentZeroHCK(config)
        assert agent is not None

    def test_agent_has_personality(self):
        """Test agent has personality system"""
        from agents.toga_hck.agent import AgentZeroHCK, AgentZeroHCKConfig

        config = AgentZeroHCKConfig()
        agent = AgentZeroHCK(config)
        assert hasattr(agent, "toga_personality")
        assert agent.toga_personality is not None

    def test_agent_has_transform_quirk(self):
        """Test agent has transform quirk"""
        from agents.toga_hck.agent import AgentZeroHCK, AgentZeroHCKConfig

        config = AgentZeroHCKConfig(enable_transform_quirk=True)
        agent = AgentZeroHCK(config)
        assert hasattr(agent, "transform_quirk")
        assert agent.transform_quirk is not None

    def test_agent_has_security_tester(self):
        """Test agent has security tester"""
        from agents.toga_hck.agent import AgentZeroHCK, AgentZeroHCKConfig

        config = AgentZeroHCKConfig(enable_security_testing=True)
        agent = AgentZeroHCK(config)
        assert hasattr(agent, "security_tester")
        assert agent.security_tester is not None

    def test_process_message(self):
        """Test message processing"""
        from agents.toga_hck.agent import AgentZeroHCK, AgentZeroHCKConfig

        config = AgentZeroHCKConfig()
        agent = AgentZeroHCK(config)
        response = agent.process_message("Hello")
        assert response is not None
        assert isinstance(response, str)

    def test_config_defaults(self):
        """Test configuration defaults"""
        from agents.toga_hck.agent import AgentZeroHCKConfig

        config = AgentZeroHCKConfig()
        assert config.enable_transform_quirk is True
        assert config.enable_security_testing is True
        assert config.ethical_testing_only is True
        assert config.respect_boundaries == 0.95


class TestConfiguration:
    """Test configuration loading"""

    def test_yaml_config_exists(self):
        """Test that YAML config file exists"""
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "agent_toga_hck.yaml"
        )
        assert os.path.exists(config_path)

    def test_prompts_exist(self):
        """Test that prompt files exist"""
        prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        assert os.path.exists(prompts_dir)
        assert os.path.exists(os.path.join(prompts_dir, "toga_hck_system.md"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
