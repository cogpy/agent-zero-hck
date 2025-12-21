"""
AtomSpace Integration Module for Agent-Zero-HCK.

Provides integration with OpenCog's AtomSpace for cognitive
architecture capabilities including knowledge representation,
pattern mining, and probabilistic logic.
"""

from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class AtomSpaceConfig:
    """Configuration for AtomSpace integration."""

    persistence_path: Optional[str] = None
    enable_attention_bank: bool = True
    enable_pattern_miner: bool = False
    enable_pln: bool = False
    default_truth_value: Tuple[float, float] = (1.0, 1.0)  # (strength, confidence)


class AtomSpaceIntegration:
    """
    AtomSpace integration for cognitive architecture.

    Provides a bridge between Agent-Zero-HCK and OpenCog's AtomSpace,
    enabling knowledge representation, reasoning, and learning.
    """

    def __init__(self, config: Optional[AtomSpaceConfig] = None):
        """
        Initialize AtomSpace integration.

        Args:
            config: AtomSpace configuration options
        """
        self.config = config or AtomSpaceConfig()
        self.atomspace = None
        self.available = False
        self._initialize()

    def _initialize(self):
        """Initialize the AtomSpace."""
        try:
            from opencog.atomspace import AtomSpace, TruthValue
            from opencog.type_constructors import set_default_atomspace

            self.atomspace = AtomSpace()
            set_default_atomspace(self.atomspace)
            self.TruthValue = TruthValue
            self.available = True
            print("AtomSpace: Cognitive architecture initialized")

        except ImportError:
            print("AtomSpace: OpenCog not installed, running in stub mode")
            self.available = False
            self._init_stub()

    def _init_stub(self):
        """Initialize stub mode for testing without OpenCog."""
        self.atoms = {}  # Simple dict-based atom storage
        self.links = []  # Simple list-based link storage

    def add_node(
        self,
        node_type: str,
        name: str,
        truth_value: Optional[Tuple[float, float]] = None,
    ) -> Any:
        """
        Add a node to the AtomSpace.

        Args:
            node_type: Type of node (e.g., "ConceptNode", "PredicateNode")
            name: Name of the node
            truth_value: Optional (strength, confidence) tuple

        Returns:
            The created node
        """
        tv = truth_value or self.config.default_truth_value

        if self.available:
            from opencog.type_constructors import ConceptNode, PredicateNode

            if node_type == "ConceptNode":
                node = ConceptNode(name)
            elif node_type == "PredicateNode":
                node = PredicateNode(name)
            else:
                node = ConceptNode(name)  # Default

            node.tv = self.TruthValue(tv[0], tv[1])
            return node
        else:
            # Stub mode
            node_id = f"{node_type}:{name}"
            self.atoms[node_id] = {"type": node_type, "name": name, "truth_value": tv}
            return node_id

    def add_link(
        self,
        link_type: str,
        atoms: List[Any],
        truth_value: Optional[Tuple[float, float]] = None,
    ) -> Any:
        """
        Add a link between atoms.

        Args:
            link_type: Type of link (e.g., "InheritanceLink", "EvaluationLink")
            atoms: List of atoms to link
            truth_value: Optional (strength, confidence) tuple

        Returns:
            The created link
        """
        tv = truth_value or self.config.default_truth_value

        if self.available:
            from opencog.type_constructors import (
                InheritanceLink,
                EvaluationLink,
                ListLink,
            )

            if link_type == "InheritanceLink":
                link = InheritanceLink(*atoms)
            elif link_type == "EvaluationLink":
                link = EvaluationLink(*atoms)
            elif link_type == "ListLink":
                link = ListLink(*atoms)
            else:
                link = ListLink(*atoms)  # Default

            link.tv = self.TruthValue(tv[0], tv[1])
            return link
        else:
            # Stub mode
            link_id = f"{link_type}:{len(self.links)}"
            self.links.append({"type": link_type, "atoms": atoms, "truth_value": tv})
            return link_id

    def query(self, pattern: str) -> List[Any]:
        """
        Query the AtomSpace with a pattern.

        Args:
            pattern: Query pattern

        Returns:
            List of matching atoms
        """
        if self.available:
            # Use pattern matcher
            # This is a simplified implementation
            results = []
            for atom in self.atomspace.get_atoms_by_type(0):  # All types
                if pattern.lower() in str(atom).lower():
                    results.append(atom)
            return results
        else:
            # Stub mode
            results = []
            for node_id, node in self.atoms.items():
                if pattern.lower() in node["name"].lower():
                    results.append(node_id)
            return results

    def get_attention(self, atom: Any) -> float:
        """
        Get attention value for an atom.

        Args:
            atom: The atom to check

        Returns:
            Attention value (0.0 to 1.0)
        """
        if self.available and self.config.enable_attention_bank:
            try:
                return atom.av.sti / 100.0  # Normalize STI
            except:
                return 0.5
        else:
            return 0.5  # Default attention

    def set_attention(self, atom: Any, attention: float):
        """
        Set attention value for an atom.

        Args:
            atom: The atom to update
            attention: Attention value (0.0 to 1.0)
        """
        if self.available and self.config.enable_attention_bank:
            try:
                sti = int(attention * 100)
                atom.av = {"sti": sti, "lti": 0, "vlti": False}
            except:
                pass

    def get_status(self) -> Dict[str, Any]:
        """Get AtomSpace status information."""
        if self.available:
            return {
                "available": True,
                "atom_count": len(self.atomspace),
                "attention_bank": self.config.enable_attention_bank,
                "pattern_miner": self.config.enable_pattern_miner,
                "pln": self.config.enable_pln,
            }
        else:
            return {
                "available": False,
                "stub_atoms": len(self.atoms),
                "stub_links": len(self.links),
            }


def initialize_atomspace(
    config: Optional[Dict[str, Any]] = None,
) -> AtomSpaceIntegration:
    """
    Initialize AtomSpace integration with configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Configured AtomSpaceIntegration instance
    """
    if config:
        as_config = AtomSpaceConfig(**config)
    else:
        as_config = AtomSpaceConfig()

    return AtomSpaceIntegration(as_config)


# Standalone testing
if __name__ == "__main__":
    atomspace = initialize_atomspace()
    print(f"AtomSpace Status: {atomspace.get_status()}")

    # Test node creation
    node1 = atomspace.add_node("ConceptNode", "Toga")
    node2 = atomspace.add_node("ConceptNode", "Security")

    # Test link creation
    link = atomspace.add_link("InheritanceLink", [node1, node2])

    # Test query
    results = atomspace.query("Toga")
    print(f"Query results: {results}")
