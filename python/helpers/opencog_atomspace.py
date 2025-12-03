"""
OpenCog AtomSpace Integration for Agent Zero
Provides cognitive architecture capabilities through knowledge representation
"""

import json
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
import networkx as nx
from dataclasses import dataclass, field


@dataclass
class Atom:
    """Base class for atoms in the AtomSpace"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "Atom"
    name: str = ""
    truth_value: Tuple[float, float] = (1.0, 1.0)  # (strength, confidence)
    attention_value: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert atom to dictionary representation"""
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "truth_value": self.truth_value,
            "attention_value": self.attention_value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Node(Atom):
    """Node atom representing concepts"""
    type: str = "ConceptNode"
    
    def __post_init__(self):
        if not self.name:
            self.name = f"node_{self.id[:8]}"


@dataclass
class Link(Atom):
    """Link atom representing relationships"""
    type: str = "InheritanceLink"
    outgoing: List[str] = field(default_factory=list)  # List of atom IDs
    
    def __post_init__(self):
        if not self.name:
            self.name = f"link_{self.id[:8]}"


class AtomSpace:
    """
    OpenCog-inspired AtomSpace for cognitive knowledge representation
    Manages atoms (nodes and links) in a hypergraph structure
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.atoms: Dict[str, Atom] = {}
        self.graph = nx.MultiDiGraph()
        self.type_index: Dict[str, Set[str]] = {}
        self.name_index: Dict[str, str] = {}
        
    def add_node(
        self,
        node_type: str = "ConceptNode",
        name: str = "",
        truth_value: Tuple[float, float] = (1.0, 1.0),
        attention_value: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Node:
        """Add a node to the AtomSpace"""
        # Check if node with same name already exists
        if name and name in self.name_index:
            existing_id = self.name_index[name]
            return self.atoms[existing_id]
        
        node = Node(
            type=node_type,
            name=name,
            truth_value=truth_value,
            attention_value=attention_value,
            metadata=metadata or {}
        )
        
        self.atoms[node.id] = node
        self.graph.add_node(node.id, atom=node)
        
        # Update indices
        if node_type not in self.type_index:
            self.type_index[node_type] = set()
        self.type_index[node_type].add(node.id)
        
        if name:
            self.name_index[name] = node.id
            
        return node
    
    def add_link(
        self,
        link_type: str = "InheritanceLink",
        outgoing: List[str] = None,
        name: str = "",
        truth_value: Tuple[float, float] = (1.0, 1.0),
        attention_value: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Link:
        """Add a link to the AtomSpace"""
        outgoing = outgoing or []
        
        link = Link(
            type=link_type,
            name=name,
            outgoing=outgoing,
            truth_value=truth_value,
            attention_value=attention_value,
            metadata=metadata or {}
        )
        
        self.atoms[link.id] = link
        self.graph.add_node(link.id, atom=link)
        
        # Add edges in the graph
        for i, target_id in enumerate(outgoing):
            if target_id in self.atoms:
                self.graph.add_edge(link.id, target_id, order=i)
        
        # Update type index
        if link_type not in self.type_index:
            self.type_index[link_type] = set()
        self.type_index[link_type].add(link.id)
        
        if name:
            self.name_index[name] = link.id
            
        return link
    
    def get_atom(self, atom_id: str) -> Optional[Atom]:
        """Get atom by ID"""
        return self.atoms.get(atom_id)
    
    def get_atom_by_name(self, name: str) -> Optional[Atom]:
        """Get atom by name"""
        atom_id = self.name_index.get(name)
        if atom_id:
            return self.atoms.get(atom_id)
        return None
    
    def get_atoms_by_type(self, atom_type: str) -> List[Atom]:
        """Get all atoms of a specific type"""
        atom_ids = self.type_index.get(atom_type, set())
        return [self.atoms[aid] for aid in atom_ids if aid in self.atoms]
    
    def get_incoming(self, atom_id: str) -> List[Atom]:
        """Get atoms that link to this atom"""
        if atom_id not in self.graph:
            return []
        predecessors = list(self.graph.predecessors(atom_id))
        return [self.atoms[pid] for pid in predecessors if pid in self.atoms]
    
    def get_outgoing(self, atom_id: str) -> List[Atom]:
        """Get atoms that this atom links to"""
        atom = self.atoms.get(atom_id)
        if isinstance(atom, Link):
            return [self.atoms[oid] for oid in atom.outgoing if oid in self.atoms]
        return []
    
    def pattern_match(self, pattern: Dict[str, Any]) -> List[Atom]:
        """
        Simple pattern matching in the AtomSpace
        Pattern format: {"type": "ConceptNode", "name": "agent_*", ...}
        """
        matches = []
        for atom in self.atoms.values():
            if self._match_atom(atom, pattern):
                matches.append(atom)
        return matches
    
    def _match_atom(self, atom: Atom, pattern: Dict[str, Any]) -> bool:
        """Check if atom matches pattern"""
        for key, value in pattern.items():
            if key == "type":
                if not self._match_value(atom.type, value):
                    return False
            elif key == "name":
                if not self._match_value(atom.name, value):
                    return False
            elif key == "metadata":
                if not self._match_metadata(atom.metadata, value):
                    return False
        return True
    
    def _match_value(self, actual: str, pattern: str) -> bool:
        """Match value with wildcard support"""
        if pattern == "*":
            return True
        if "*" in pattern:
            # Simple wildcard matching
            import re
            regex_pattern = pattern.replace("*", ".*")
            return bool(re.match(f"^{regex_pattern}$", actual))
        return actual == pattern
    
    def _match_metadata(self, actual: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Match metadata fields"""
        for key, value in pattern.items():
            if key not in actual or actual[key] != value:
                return False
        return True
    
    def update_attention(self, atom_id: str, delta: float):
        """Update attention value of an atom"""
        atom = self.atoms.get(atom_id)
        if atom:
            atom.attention_value = max(0.0, min(1.0, atom.attention_value + delta))
    
    def spread_activation(self, source_id: str, intensity: float = 0.1, decay: float = 0.5):
        """
        Spread activation from a source atom to connected atoms
        Implements basic attention allocation mechanism
        """
        if source_id not in self.atoms:
            return
        
        # BFS to spread activation
        visited = set()
        queue = [(source_id, intensity)]
        
        while queue:
            current_id, current_intensity = queue.pop(0)
            if current_id in visited or current_intensity < 0.01:
                continue
                
            visited.add(current_id)
            self.update_attention(current_id, current_intensity)
            
            # Spread to connected atoms
            successors = list(self.graph.successors(current_id))
            predecessors = list(self.graph.predecessors(current_id))
            
            next_intensity = current_intensity * decay
            for neighbor_id in successors + predecessors:
                if neighbor_id not in visited:
                    queue.append((neighbor_id, next_intensity))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the AtomSpace"""
        return {
            "total_atoms": len(self.atoms),
            "total_nodes": sum(1 for a in self.atoms.values() if isinstance(a, Node)),
            "total_links": sum(1 for a in self.atoms.values() if isinstance(a, Link)),
            "types": {t: len(ids) for t, ids in self.type_index.items()},
            "graph_density": nx.density(self.graph) if self.graph.number_of_nodes() > 0 else 0
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export AtomSpace to dictionary"""
        return {
            "name": self.name,
            "atoms": [atom.to_dict() for atom in self.atoms.values()],
            "stats": self.get_stats()
        }
    
    def import_from_dict(self, data: Dict[str, Any]):
        """Import AtomSpace from dictionary"""
        self.name = data.get("name", self.name)
        for atom_data in data.get("atoms", []):
            if atom_data.get("type", "").endswith("Node"):
                self.add_node(
                    node_type=atom_data.get("type", "ConceptNode"),
                    name=atom_data.get("name", ""),
                    truth_value=tuple(atom_data.get("truth_value", [1.0, 1.0])),
                    attention_value=atom_data.get("attention_value", 0.5),
                    metadata=atom_data.get("metadata", {})
                )
            elif "outgoing" in atom_data:
                self.add_link(
                    link_type=atom_data.get("type", "InheritanceLink"),
                    outgoing=atom_data.get("outgoing", []),
                    name=atom_data.get("name", ""),
                    truth_value=tuple(atom_data.get("truth_value", [1.0, 1.0])),
                    attention_value=atom_data.get("attention_value", 0.5),
                    metadata=atom_data.get("metadata", {})
                )


class CognitiveOrchestrator:
    """
    Orchestrates multiple AtomSpaces for multi-agent cognitive architecture
    Implements adaptive evolutionary mechanisms
    """
    
    def __init__(self):
        self.atomspaces: Dict[str, AtomSpace] = {}
        self.agent_spaces: Dict[str, str] = {}  # agent_id -> atomspace_name
        
    def create_atomspace(self, name: str) -> AtomSpace:
        """Create a new AtomSpace"""
        if name not in self.atomspaces:
            self.atomspaces[name] = AtomSpace(name)
        return self.atomspaces[name]
    
    def get_atomspace(self, name: str) -> Optional[AtomSpace]:
        """Get an AtomSpace by name"""
        return self.atomspaces.get(name)
    
    def assign_agent_space(self, agent_id: str, atomspace_name: str):
        """Assign an agent to an AtomSpace"""
        self.agent_spaces[agent_id] = atomspace_name
    
    def get_agent_space(self, agent_id: str) -> Optional[AtomSpace]:
        """Get the AtomSpace for an agent"""
        space_name = self.agent_spaces.get(agent_id)
        if space_name:
            return self.atomspaces.get(space_name)
        return None
    
    def merge_atomspaces(self, target_name: str, source_name: str):
        """Merge source AtomSpace into target AtomSpace"""
        target = self.get_atomspace(target_name)
        source = self.get_atomspace(source_name)
        
        if not target or not source:
            return
        
        # Import all atoms from source to target
        data = source.export_to_dict()
        target.import_from_dict(data)
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Get statistics across all AtomSpaces"""
        return {
            "total_atomspaces": len(self.atomspaces),
            "atomspaces": {
                name: space.get_stats()
                for name, space in self.atomspaces.items()
            }
        }


# Global orchestrator instance
_global_orchestrator: Optional[CognitiveOrchestrator] = None


def get_orchestrator() -> CognitiveOrchestrator:
    """Get the global cognitive orchestrator instance"""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = CognitiveOrchestrator()
    return _global_orchestrator
