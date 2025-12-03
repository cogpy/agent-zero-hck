"""
OpenCog Tool for Agent Zero
Allows agents to interact with the cognitive AtomSpace
"""

import json
from python.helpers.tool import Tool, Response
from python.helpers import opencog_atomspace
from python.helpers.print_style import PrintStyle


class OpenCog(Tool):
    """Tool for interacting with OpenCog AtomSpace"""
    
    async def execute(self, **kwargs) -> Response:
        """
        Execute OpenCog operations on the AtomSpace
        
        Supported methods:
        - add_node: Add a concept node to the AtomSpace
        - add_link: Add a relationship link between nodes
        - query: Query atoms by pattern
        - get_stats: Get AtomSpace statistics
        - spread_activation: Spread attention from a node
        - get_atom: Get atom by name or ID
        """
        
        method = self.method or "query"
        orchestrator = opencog_atomspace.get_orchestrator()
        
        # Get or create agent's AtomSpace
        agent_id = f"agent_{self.agent.number}"
        atomspace = orchestrator.get_agent_space(agent_id)
        
        if not atomspace:
            # Create default atomspace for this agent
            space_name = kwargs.get("atomspace", f"space_{agent_id}")
            atomspace = orchestrator.create_atomspace(space_name)
            orchestrator.assign_agent_space(agent_id, space_name)
        
        try:
            if method == "add_node":
                result = self._add_node(atomspace, **kwargs)
            elif method == "add_link":
                result = self._add_link(atomspace, **kwargs)
            elif method == "query":
                result = self._query(atomspace, **kwargs)
            elif method == "get_stats":
                result = self._get_stats(atomspace, **kwargs)
            elif method == "spread_activation":
                result = self._spread_activation(atomspace, **kwargs)
            elif method == "get_atom":
                result = self._get_atom(atomspace, **kwargs)
            elif method == "pattern_match":
                result = self._pattern_match(atomspace, **kwargs)
            elif method == "merge_spaces":
                result = self._merge_spaces(orchestrator, **kwargs)
            elif method == "export":
                result = self._export(atomspace, **kwargs)
            elif method == "import":
                result = self._import(atomspace, **kwargs)
            else:
                result = f"Unknown method: {method}. Available methods: add_node, add_link, query, get_stats, spread_activation, get_atom, pattern_match, merge_spaces, export, import"
                
            return Response(message=result, break_loop=False)
            
        except Exception as e:
            error_msg = f"OpenCog operation failed: {str(e)}"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
    
    def _add_node(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Add a concept node to the AtomSpace"""
        node_type = kwargs.get("node_type", "ConceptNode")
        name = kwargs.get("name", "")
        truth_value = kwargs.get("truth_value", (1.0, 1.0))
        attention = kwargs.get("attention", 0.5)
        metadata = kwargs.get("metadata", {})
        
        if isinstance(truth_value, list):
            truth_value = tuple(truth_value)
        
        node = atomspace.add_node(
            node_type=node_type,
            name=name,
            truth_value=truth_value,
            attention_value=attention,
            metadata=metadata
        )
        
        return json.dumps({
            "status": "success",
            "operation": "add_node",
            "node": node.to_dict()
        }, indent=2)
    
    def _add_link(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Add a link between atoms"""
        link_type = kwargs.get("link_type", "InheritanceLink")
        outgoing = kwargs.get("outgoing", [])
        name = kwargs.get("name", "")
        truth_value = kwargs.get("truth_value", (1.0, 1.0))
        attention = kwargs.get("attention", 0.5)
        metadata = kwargs.get("metadata", {})
        
        if isinstance(truth_value, list):
            truth_value = tuple(truth_value)
        
        # If outgoing contains names instead of IDs, resolve them
        resolved_outgoing = []
        for item in outgoing:
            if isinstance(item, str):
                # Try to find atom by name
                atom = atomspace.get_atom_by_name(item)
                if atom:
                    resolved_outgoing.append(atom.id)
                else:
                    # Assume it's already an ID
                    resolved_outgoing.append(item)
        
        link = atomspace.add_link(
            link_type=link_type,
            outgoing=resolved_outgoing,
            name=name,
            truth_value=truth_value,
            attention_value=attention,
            metadata=metadata
        )
        
        return json.dumps({
            "status": "success",
            "operation": "add_link",
            "link": link.to_dict()
        }, indent=2)
    
    def _query(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Query atoms by type"""
        atom_type = kwargs.get("atom_type", "ConceptNode")
        atoms = atomspace.get_atoms_by_type(atom_type)
        
        return json.dumps({
            "status": "success",
            "operation": "query",
            "count": len(atoms),
            "atoms": [atom.to_dict() for atom in atoms[:50]]  # Limit to 50
        }, indent=2)
    
    def _get_stats(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Get AtomSpace statistics"""
        stats = atomspace.get_stats()
        
        return json.dumps({
            "status": "success",
            "operation": "get_stats",
            "stats": stats
        }, indent=2)
    
    def _spread_activation(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Spread activation from a source atom"""
        source = kwargs.get("source", "")
        intensity = kwargs.get("intensity", 0.1)
        decay = kwargs.get("decay", 0.5)
        
        # Resolve source
        atom = atomspace.get_atom_by_name(source)
        if not atom:
            atom = atomspace.get_atom(source)
        
        if not atom:
            return json.dumps({
                "status": "error",
                "message": f"Source atom not found: {source}"
            }, indent=2)
        
        atomspace.spread_activation(atom.id, intensity, decay)
        
        return json.dumps({
            "status": "success",
            "operation": "spread_activation",
            "source": atom.to_dict()
        }, indent=2)
    
    def _get_atom(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Get atom by name or ID"""
        name = kwargs.get("name", "")
        atom_id = kwargs.get("id", "")
        
        atom = None
        if name:
            atom = atomspace.get_atom_by_name(name)
        elif atom_id:
            atom = atomspace.get_atom(atom_id)
        
        if not atom:
            return json.dumps({
                "status": "error",
                "message": "Atom not found"
            }, indent=2)
        
        # Get incoming and outgoing
        incoming = atomspace.get_incoming(atom.id)
        outgoing = atomspace.get_outgoing(atom.id)
        
        return json.dumps({
            "status": "success",
            "operation": "get_atom",
            "atom": atom.to_dict(),
            "incoming": [a.to_dict() for a in incoming],
            "outgoing": [a.to_dict() for a in outgoing]
        }, indent=2)
    
    def _pattern_match(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Pattern matching in the AtomSpace"""
        pattern = kwargs.get("pattern", {})
        
        matches = atomspace.pattern_match(pattern)
        
        return json.dumps({
            "status": "success",
            "operation": "pattern_match",
            "pattern": pattern,
            "count": len(matches),
            "matches": [atom.to_dict() for atom in matches[:50]]  # Limit to 50
        }, indent=2)
    
    def _merge_spaces(self, orchestrator: opencog_atomspace.CognitiveOrchestrator, **kwargs) -> str:
        """Merge two AtomSpaces"""
        target = kwargs.get("target", "")
        source = kwargs.get("source", "")
        
        if not target or not source:
            return json.dumps({
                "status": "error",
                "message": "Both target and source atomspace names required"
            }, indent=2)
        
        orchestrator.merge_atomspaces(target, source)
        
        return json.dumps({
            "status": "success",
            "operation": "merge_spaces",
            "target": target,
            "source": source
        }, indent=2)
    
    def _export(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Export AtomSpace to JSON"""
        data = atomspace.export_to_dict()
        
        return json.dumps({
            "status": "success",
            "operation": "export",
            "data": data
        }, indent=2)
    
    def _import(self, atomspace: opencog_atomspace.AtomSpace, **kwargs) -> str:
        """Import AtomSpace from JSON"""
        data = kwargs.get("data", {})
        
        if not data:
            return json.dumps({
                "status": "error",
                "message": "No data provided for import"
            }, indent=2)
        
        atomspace.import_from_dict(data)
        
        return json.dumps({
            "status": "success",
            "operation": "import",
            "stats": atomspace.get_stats()
        }, indent=2)
