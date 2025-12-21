#!/usr/bin/env python3
"""
Test suite for OpenCog AtomSpace integration in Agent Zero
Validates cognitive architecture functionality
"""

import sys
import os

# Add python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

from helpers.opencog_atomspace import (
    AtomSpace, 
    CognitiveOrchestrator, 
    get_orchestrator,
    Node,
    Link
)


def test_atomspace_creation():
    """Test basic AtomSpace creation"""
    print("Testing AtomSpace creation...")
    atomspace = AtomSpace('test')
    assert atomspace.name == 'test'
    assert len(atomspace.atoms) == 0
    print("✓ AtomSpace creation passed")


def test_node_operations():
    """Test node creation and retrieval"""
    print("Testing node operations...")
    atomspace = AtomSpace('test_nodes')
    
    # Create node
    node = atomspace.add_node('ConceptNode', 'TestConcept', (0.9, 0.8))
    assert node.name == 'TestConcept'
    assert node.type == 'ConceptNode'
    assert node.truth_value == (0.9, 0.8)
    
    # Retrieve by ID
    retrieved = atomspace.get_atom(node.id)
    assert retrieved is not None
    assert retrieved.name == 'TestConcept'
    
    # Retrieve by name
    retrieved_by_name = atomspace.get_atom_by_name('TestConcept')
    assert retrieved_by_name is not None
    assert retrieved_by_name.id == node.id
    
    # Test duplicate prevention
    node2 = atomspace.add_node('ConceptNode', 'TestConcept')
    assert node2.id == node.id  # Should return existing node
    
    print("✓ Node operations passed")


def test_link_operations():
    """Test link creation and relationships"""
    print("Testing link operations...")
    atomspace = AtomSpace('test_links')
    
    # Create nodes
    node1 = atomspace.add_node('ConceptNode', 'Parent')
    node2 = atomspace.add_node('ConceptNode', 'Child')
    
    # Create link
    link = atomspace.add_link(
        'InheritanceLink',
        [node1.id, node2.id],
        'ParentChildLink'
    )
    
    assert link.type == 'InheritanceLink'
    assert len(link.outgoing) == 2
    
    # Test outgoing
    outgoing = atomspace.get_outgoing(link.id)
    assert len(outgoing) == 2
    assert outgoing[0].name == 'Parent'
    assert outgoing[1].name == 'Child'
    
    # Test incoming
    incoming = atomspace.get_incoming(node2.id)
    assert len(incoming) == 1
    assert incoming[0].id == link.id
    
    print("✓ Link operations passed")


def test_pattern_matching():
    """Test pattern matching capabilities"""
    print("Testing pattern matching...")
    atomspace = AtomSpace('test_patterns')
    
    # Create test data
    atomspace.add_node('ConceptNode', 'Agent_0')
    atomspace.add_node('ConceptNode', 'Agent_1')
    atomspace.add_node('ConceptNode', 'Agent_2')
    atomspace.add_node('PredicateNode', 'IsActive')
    
    # Match by type
    agents = atomspace.pattern_match({'type': 'ConceptNode'})
    assert len(agents) == 3
    
    # Match by wildcard
    agent_nodes = atomspace.pattern_match({'type': 'ConceptNode', 'name': 'Agent_*'})
    assert len(agent_nodes) == 3
    
    # Match specific
    specific = atomspace.pattern_match({'type': 'PredicateNode', 'name': 'IsActive'})
    assert len(specific) == 1
    
    print("✓ Pattern matching passed")


def test_attention_mechanisms():
    """Test attention allocation and spreading"""
    print("Testing attention mechanisms...")
    atomspace = AtomSpace('test_attention')
    
    # Create connected nodes
    node1 = atomspace.add_node('ConceptNode', 'Source', attention_value=0.5)
    node2 = atomspace.add_node('ConceptNode', 'Target1', attention_value=0.3)
    node3 = atomspace.add_node('ConceptNode', 'Target2', attention_value=0.3)
    
    link1 = atomspace.add_link('InheritanceLink', [node1.id, node2.id])
    link2 = atomspace.add_link('InheritanceLink', [node1.id, node3.id])
    
    # Test attention update
    initial_attention = node1.attention_value
    atomspace.update_attention(node1.id, 0.2)
    assert node1.attention_value == initial_attention + 0.2
    
    # Test spreading activation
    atomspace.spread_activation(node1.id, intensity=0.3, decay=0.5)
    
    # Check that attention spread to connected nodes
    assert node2.attention_value > 0.3
    assert node3.attention_value > 0.3
    
    print("✓ Attention mechanisms passed")


def test_statistics():
    """Test statistics generation"""
    print("Testing statistics...")
    atomspace = AtomSpace('test_stats')
    
    # Create test data
    atomspace.add_node('ConceptNode', 'Node1')
    atomspace.add_node('ConceptNode', 'Node2')
    atomspace.add_node('PredicateNode', 'Pred1')
    
    node1 = atomspace.get_atom_by_name('Node1')
    node2 = atomspace.get_atom_by_name('Node2')
    atomspace.add_link('InheritanceLink', [node1.id, node2.id])
    
    stats = atomspace.get_stats()
    
    assert stats['total_atoms'] == 4
    assert stats['total_nodes'] == 3
    assert stats['total_links'] == 1
    assert 'ConceptNode' in stats['types']
    assert stats['types']['ConceptNode'] == 2
    
    print("✓ Statistics passed")


def test_export_import():
    """Test export and import functionality"""
    print("Testing export/import...")
    atomspace1 = AtomSpace('test_export')
    
    # Create data
    node1 = atomspace1.add_node('ConceptNode', 'ExportNode', (0.9, 0.8))
    node2 = atomspace1.add_node('ConceptNode', 'ExportNode2')
    link = atomspace1.add_link('InheritanceLink', [node1.id, node2.id])
    
    # Export
    exported = atomspace1.export_to_dict()
    assert exported['name'] == 'test_export'
    assert len(exported['atoms']) == 3
    
    # Import to new space
    atomspace2 = AtomSpace('test_import')
    atomspace2.import_from_dict(exported)
    
    # Verify import
    imported_node = atomspace2.get_atom_by_name('ExportNode')
    assert imported_node is not None
    assert imported_node.truth_value == (0.9, 0.8)
    
    print("✓ Export/import passed")


def test_cognitive_orchestrator():
    """Test multi-agent orchestration"""
    print("Testing cognitive orchestrator...")
    orchestrator = CognitiveOrchestrator()
    
    # Create multiple spaces
    space1 = orchestrator.create_atomspace('agent_0')
    space2 = orchestrator.create_atomspace('agent_1')
    
    assert space1.name == 'agent_0'
    assert space2.name == 'agent_1'
    
    # Assign agents
    orchestrator.assign_agent_space('agent_0_id', 'agent_0')
    orchestrator.assign_agent_space('agent_1_id', 'agent_1')
    
    # Retrieve agent space
    retrieved = orchestrator.get_agent_space('agent_0_id')
    assert retrieved.name == 'agent_0'
    
    # Add data to spaces
    space1.add_node('ConceptNode', 'Agent0Knowledge')
    space2.add_node('ConceptNode', 'Agent1Knowledge')
    
    # Test merge
    orchestrator.merge_atomspaces('agent_0', 'agent_1')
    merged_node = space1.get_atom_by_name('Agent1Knowledge')
    assert merged_node is not None
    
    # Test global stats
    global_stats = orchestrator.get_global_stats()
    assert global_stats['total_atomspaces'] == 2
    
    print("✓ Cognitive orchestrator passed")


def test_global_orchestrator():
    """Test global orchestrator singleton"""
    print("Testing global orchestrator...")
    
    orch1 = get_orchestrator()
    orch2 = get_orchestrator()
    
    assert orch1 is orch2  # Should be same instance
    
    print("✓ Global orchestrator passed")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*60)
    print("OpenCog AtomSpace Integration Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_atomspace_creation,
        test_node_operations,
        test_link_operations,
        test_pattern_matching,
        test_attention_mechanisms,
        test_statistics,
        test_export_import,
        test_cognitive_orchestrator,
        test_global_orchestrator,
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed.append((test.__name__, e))
    
    print("\n" + "="*60)
    if not failed:
        print("✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        return 0
    else:
        print(f"❌ {len(failed)} TEST(S) FAILED:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("="*60 + "\n")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
