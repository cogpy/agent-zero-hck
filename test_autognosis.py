#!/usr/bin/env python3
"""
Test script for autognosis functionality.
Demonstrates hierarchical self-image building and meta-cognitive insights.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent, AgentConfig, ModelConfig
from models import ModelProvider
from python.helpers.autognosis import AutognosisOrchestrator


async def test_autognosis():
    """Test the autognosis system."""
    print("=" * 80)
    print("AUTOGNOSIS - Hierarchical Self-Image Building System")
    print("=" * 80)
    print()
    
    # Create a simple agent config with minimal model configuration
    chat_model = ModelConfig(
        provider=ModelProvider.OPENAI,
        name="gpt-4",
        ctx_length=8000,
    )
    
    config = AgentConfig(
        chat_model=chat_model,
        utility_model=chat_model,
        embeddings_model=chat_model,
        browser_model=chat_model,
    )
    
    # Create an agent
    print("Creating agent...")
    agent = Agent(0, config)
    print(f"Agent created: {agent.agent_name}")
    print()
    
    # Initialize autognosis
    print("Initializing autognosis system...")
    agent.autognosis = AutognosisOrchestrator(max_levels=5)
    await agent.autognosis.initialize(agent)
    print("✓ Autognosis initialized")
    print()
    
    # Get initial status
    print("Initial Status:")
    print("-" * 80)
    status = agent.autognosis.get_autognosis_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    # Run a few observation cycles
    print("Running autognosis cycles...")
    print("-" * 80)
    for i in range(3):
        results = await agent.autognosis.run_autognosis_cycle(agent)
        print(f"\nCycle #{results['cycle_number']}:")
        print(f"  Duration: {results['duration_seconds']:.3f}s")
        print(f"  Patterns detected: {len(results['patterns'])}")
        print(f"  Anomalies detected: {len(results['anomalies'])}")
        print(f"  Insights generated: {len(results['insights'])}")
        print(f"  Self-awareness score: {results['self_awareness_score']:.3f}")
        
        # Simulate some activity for pattern detection
        # Note: In a real scenario, the agent would accumulate history naturally
    
    print()
    
    # Get comprehensive report
    print("Comprehensive Self-Awareness Report:")
    print("=" * 80)
    print(agent.autognosis.format_status_output())
    print()
    
    # Get detailed insights
    insights = agent.autognosis.get_insights()
    if insights:
        print("\nDetailed Insights:")
        print("-" * 80)
        for insight in insights[:10]:
            print(f"\n  Type: {insight.insight_type}")
            print(f"  Description: {insight.description}")
            print(f"  Severity: {insight.severity}")
            print(f"  Confidence: {insight.confidence:.2f}")
            if insight.data:
                print(f"  Data: {insight.data}")
    
    print()
    print("=" * 80)
    print("Autognosis test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_autognosis())
