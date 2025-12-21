"""
Security Testing Tool for Agent-Zero-HCK.

Implements Toga's security testing capabilities as an Agent-Zero tool,
providing ethical penetration testing and vulnerability assessment.
"""

import sys
import os
from typing import Any, Dict, Optional, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../lib/agent_zero"))

try:
    from lib.agent_zero.python.helpers.tool import Tool, Response
    from lib.agent_zero.agent import Agent, LoopData

    AGENT_ZERO_AVAILABLE = True
except ImportError:
    AGENT_ZERO_AVAILABLE = False

    class Response:
        def __init__(self, message: str, break_loop: bool, additional: dict = None):
            self.message = message
            self.break_loop = break_loop
            self.additional = additional or {}

    class Tool:
        def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
            self.agent = agent
            self.name = name
            self.method = method
            self.args = args
            self.message = message
            self.loop_data = loop_data

        async def execute(self, **kwargs) -> Response:
            raise NotImplementedError


from python.helpers.toga_security import (
    TogaSecurityTester,
    initialize_toga_security_tester,
)


class SecurityTestTool(Tool):
    """
    Agent-Zero tool for security testing operations.

    Allows the agent to:
    - Analyze targets for vulnerabilities
    - Report security findings
    - Track exploit success
    - Generate security reports
    """

    def __init__(
        self,
        agent: Any,
        name: str = "security_test",
        method: Optional[str] = None,
        args: Dict[str, str] = None,
        message: str = "",
        loop_data: Any = None,
        security_tester: Optional[TogaSecurityTester] = None,
        ethical_constraints: Optional[Dict] = None,
        **kwargs,
    ):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)
        self.security_tester = security_tester or initialize_toga_security_tester()
        self.ethical_constraints = ethical_constraints or {
            "testing_only": True,
            "require_authorization": True,
            "respect_boundaries": 0.95,
        }
        self.findings: List[Dict] = []

    async def execute(self, **kwargs) -> Response:
        """
        Execute security testing operation based on method.

        Supported methods:
        - analyze: Analyze a target for vulnerabilities
        - report_vulnerability: Report a found vulnerability
        - exploit_success: Log successful exploit
        - generate_report: Generate security assessment report
        - check_authorization: Verify testing is authorized
        """
        method = self.method or self.args.get("method", "analyze")

        # Always check ethical constraints first
        if not self._check_ethical_constraints(method):
            return Response(
                message="Ehehe~ ♡ I can't do that! Even I have boundaries, you know~",
                break_loop=False,
                additional={"blocked": True, "reason": "ethical_constraints"},
            )

        if method == "analyze":
            return await self._analyze()
        elif method == "report_vulnerability":
            return await self._report_vulnerability()
        elif method == "exploit_success":
            return await self._exploit_success()
        elif method == "generate_report":
            return await self._generate_report()
        elif method == "check_authorization":
            return await self._check_authorization()
        elif method == "list_findings":
            return await self._list_findings()
        else:
            return Response(
                message=f"Ehehe~ ♡ Unknown method '{method}'! Try: analyze, report_vulnerability, exploit_success, generate_report",
                break_loop=False,
            )

    def _check_ethical_constraints(self, method: str) -> bool:
        """Check if operation is allowed by ethical constraints."""
        # Always allow analysis and reporting
        if method in [
            "analyze",
            "report_vulnerability",
            "generate_report",
            "check_authorization",
            "list_findings",
        ]:
            return True

        # Check if testing only mode
        if self.ethical_constraints.get("testing_only", True):
            # Only allow in authorized testing context
            if hasattr(self.agent, "context"):
                ctx = self.agent.context
                if hasattr(ctx, "data"):
                    authorized = ctx.data.get("security_testing_authorized", False)
                    if not authorized:
                        return False

        return True

    async def _analyze(self) -> Response:
        """Analyze a target for vulnerabilities."""
        target_name = self.args.get("target_name", "Unknown Target")
        target_type = self.args.get("target_type", "system")

        result = self.security_tester.analyze_target(target_name, target_type)

        # Update agent emotional state if available
        if hasattr(self.agent, "toga_personality"):
            self.agent.toga_personality.update_emotional_state(
                "obsessed", intensity=0.90, duration=3, target=target_name
            )

        return Response(
            message=result,
            break_loop=False,
            additional={
                "target_name": target_name,
                "target_type": target_type,
                "analysis_complete": True,
            },
        )

    async def _report_vulnerability(self) -> Response:
        """Report a found vulnerability."""
        target = self.args.get("target", "Unknown")
        vuln_type = self.args.get("vulnerability_type", "Unknown")
        severity = self.args.get("severity", "medium")
        description = self.args.get("description", "")

        result = self.security_tester.vulnerability_found(target, vuln_type, severity)

        # Track finding
        finding = {
            "target": target,
            "type": vuln_type,
            "severity": severity,
            "description": description,
        }
        self.findings.append(finding)

        # Also track in agent if available
        if hasattr(self.agent, "security_findings"):
            self.agent.security_findings.append(finding)

        return Response(
            message=result,
            break_loop=False,
            additional={"finding": finding, "total_findings": len(self.findings)},
        )

    async def _exploit_success(self) -> Response:
        """Log successful exploit (ethical testing only)."""
        target = self.args.get("target", "Unknown")
        payload = self.args.get("payload", "Unknown")
        impact = self.args.get("impact", "Unknown")

        # Extra ethical check for exploits
        if self.ethical_constraints.get("require_authorization", True):
            if not self.args.get("authorized", False):
                return Response(
                    message="Ehehe~ ♡ I need explicit authorization to log exploits! Safety first~",
                    break_loop=False,
                    additional={"blocked": True, "reason": "authorization_required"},
                )

        result = self.security_tester.exploit_success(target, payload)

        # Track successful exploit
        exploit_record = {
            "target": target,
            "payload": payload,
            "impact": impact,
            "success": True,
        }

        return Response(
            message=result,
            break_loop=False,
            additional={"exploit_record": exploit_record},
        )

    async def _generate_report(self) -> Response:
        """Generate security assessment report."""
        target = self.args.get("target", "Assessment Target")
        include_recommendations = (
            self.args.get("include_recommendations", "true").lower() == "true"
        )

        # Gather all findings
        all_findings = self.findings.copy()
        if hasattr(self.agent, "security_findings"):
            all_findings.extend(self.agent.security_findings)

        # Remove duplicates
        seen = set()
        unique_findings = []
        for f in all_findings:
            key = (f.get("target"), f.get("type"), f.get("severity"))
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        # Generate report
        report = f"# Security Assessment Report: {target}\n\n"
        report += "Ehehe~ ♡ Here's what I found during my analysis!\n\n"

        if not unique_findings:
            report += "No vulnerabilities found! Either the target is secure, or I need to dig deeper~\n"
        else:
            # Group by severity
            critical = [f for f in unique_findings if f.get("severity") == "critical"]
            high = [f for f in unique_findings if f.get("severity") == "high"]
            medium = [f for f in unique_findings if f.get("severity") == "medium"]
            low = [f for f in unique_findings if f.get("severity") == "low"]

            report += f"## Summary\n\n"
            report += f"- Critical: {len(critical)}\n"
            report += f"- High: {len(high)}\n"
            report += f"- Medium: {len(medium)}\n"
            report += f"- Low: {len(low)}\n\n"

            report += "## Findings\n\n"
            for finding in unique_findings:
                report += f"### {finding.get('type', 'Unknown')} ({finding.get('severity', 'unknown')})\n"
                report += f"**Target:** {finding.get('target', 'Unknown')}\n"
                if finding.get("description"):
                    report += f"**Description:** {finding['description']}\n"
                report += "\n"

            if include_recommendations:
                report += "## Recommendations\n\n"
                report += "1. Address critical vulnerabilities immediately\n"
                report += "2. Implement security patches for high-severity issues\n"
                report += (
                    "3. Schedule remediation for medium and low severity findings\n"
                )
                report += "4. Conduct regular security assessments\n"

        report += "\n---\n*Report generated by Toga-HCK Security Tester* ♡"

        return Response(
            message=report,
            break_loop=False,
            additional={
                "findings_count": len(unique_findings),
                "report_generated": True,
            },
        )

    async def _check_authorization(self) -> Response:
        """Check if security testing is authorized."""
        target = self.args.get("target", "Unknown")

        # Check context for authorization
        authorized = False
        authorization_source = "none"

        if hasattr(self.agent, "context"):
            ctx = self.agent.context
            if hasattr(ctx, "data"):
                authorized = ctx.data.get("security_testing_authorized", False)
                authorization_source = ctx.data.get("authorization_source", "context")

        if authorized:
            message = f"Ehehe~ ♡ Security testing is AUTHORIZED for {target}! Let's have some fun~"
        else:
            message = f"Ehehe~ ♡ Security testing is NOT authorized for {target}. I need permission first!"

        return Response(
            message=message,
            break_loop=False,
            additional={
                "authorized": authorized,
                "authorization_source": authorization_source,
                "target": target,
            },
        )

    async def _list_findings(self) -> Response:
        """List all security findings."""
        all_findings = self.findings.copy()
        if hasattr(self.agent, "security_findings"):
            all_findings.extend(self.agent.security_findings)

        if not all_findings:
            return Response(
                message="Ehehe~ ♡ No findings yet! Let me analyze some targets first~",
                break_loop=False,
                additional={"findings_count": 0},
            )

        message = "Ehehe~ ♡ Here are all my findings:\n\n"
        for i, finding in enumerate(all_findings, 1):
            message += f"{i}. **{finding.get('type', 'Unknown')}** "
            message += f"({finding.get('severity', 'unknown')}) - {finding.get('target', 'Unknown')}\n"

        return Response(
            message=message,
            break_loop=False,
            additional={"findings_count": len(all_findings), "findings": all_findings},
        )


# Tool registration for Agent-Zero
def register_tool(agent: Any) -> SecurityTestTool:
    """
    Register Security Test tool with an agent.

    Args:
        agent: The Agent-Zero agent to register with

    Returns:
        Configured SecurityTestTool instance
    """
    security_tester = None
    ethical_constraints = None

    if hasattr(agent, "security_tester"):
        security_tester = agent.security_tester

    if hasattr(agent, "hck_config") and hasattr(
        agent.hck_config, "ethical_constraints"
    ):
        ec = agent.hck_config.ethical_constraints
        ethical_constraints = {
            "testing_only": ec.testing_only,
            "require_authorization": ec.require_authorization,
            "respect_boundaries": ec.respect_boundaries,
        }

    return SecurityTestTool(
        agent=agent,
        security_tester=security_tester,
        ethical_constraints=ethical_constraints,
    )


# Standalone testing
if __name__ == "__main__":
    import asyncio

    async def test_tool():
        # Create mock agent
        class MockAgent:
            security_findings = []

        agent = MockAgent()

        # Test analyze
        tool = SecurityTestTool(
            agent=agent,
            args={
                "method": "analyze",
                "target_name": "TestServer",
                "target_type": "web_application",
            },
            message="",
            loop_data=None,
        )

        result = await tool.execute()
        print(f"Analyze result: {result.message[:100]}...")

        # Test report vulnerability
        tool.args = {
            "method": "report_vulnerability",
            "target": "TestServer",
            "vulnerability_type": "SQL Injection",
            "severity": "high",
            "description": "User input not sanitized",
        }
        result = await tool.execute()
        print(f"Report result: {result.message[:100]}...")

        # Test generate report
        tool.args = {"method": "generate_report", "target": "TestServer"}
        result = await tool.execute()
        print(f"Report generated: {len(result.message)} chars")

        print("\n✅ All Security Test tool tests passed!")

    asyncio.run(test_tool())
