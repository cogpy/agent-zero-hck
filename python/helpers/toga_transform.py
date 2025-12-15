"""
Toga Transform Quirk - Code Absorption System

Implements Toga's signature ability: By "drinking the blood" (absorbing knowledge)
of systems/codebases, she learns to transform and use their abilities/defenses as weapons.

"Ehehe~ Once I taste your code... I can become you~ ♡"
"""

import random
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class AbsorbedKnowledge:
    """Knowledge absorbed from a target system."""

    target_name: str
    target_type: str  # "codebase", "framework", "security_tool", "defense_system"
    absorbed_at: datetime
    essence_amount: float = 0.0  # 0.0 to 1.0 - how much has been absorbed
    techniques_learned: List[str] = field(default_factory=list)
    abilities_gained: List[str] = field(default_factory=list)
    transformation_unlocked: bool = False

    def can_transform(self) -> bool:
        """Check if enough essence absorbed to transform."""
        return self.essence_amount >= 0.7  # Need 70% to transform

    def is_mastered(self) -> bool:
        """Check if fully mastered (100% absorbed)."""
        return self.essence_amount >= 1.0


@dataclass
class Technique:
    """A technique learned from absorbed knowledge."""

    name: str
    description: str
    source: str  # Which system it came from
    offensive_use: str  # How to use defensively-intended code offensively
    requirements: float = 0.5  # Minimum essence needed to use
    power_level: float = 0.7

    def can_use(self, essence_amount: float) -> bool:
        """Check if technique can be used."""
        return essence_amount >= self.requirements


class TogaTransformQuirk:
    """
    Toga's Transform Quirk - Code Absorption and Skill Learning System

    By "drinking the blood" (processing/analyzing code) of systems, Toga:
    1. Absorbs their essence (knowledge)
    2. Learns their techniques
    3. Gains their abilities
    4. Can transform to use their powers
    5. Weaponizes defensive systems for offense
    """

    def __init__(self):
        self.absorbed_targets: Dict[str, AbsorbedKnowledge] = {}
        self.available_techniques: List[Technique] = []
        self.active_transformation: Optional[str] = None
        self.transformation_duration: int = 0
        self.total_essence_collected: float = 0.0

        # Knowledge database - techniques that can be learned
        self._initialize_technique_database()

    def _initialize_technique_database(self):
        """Initialize database of techniques that can be learned."""
        self.technique_database = {
            "WAF": [
                Technique(
                    "Reverse WAF Rules",
                    "Use WAF rules to craft perfectly evasive payloads",
                    "Web Application Firewall",
                    "Study WAF signatures to create payloads that slip through undetected",
                    requirements=0.6,
                    power_level=0.8,
                ),
                Technique(
                    "WAF Weaponization",
                    "Turn WAF blocking rules into attack vectors",
                    "Web Application Firewall",
                    "Use WAF's own regex patterns to cause ReDoS or bypass via edge cases",
                    requirements=0.8,
                    power_level=0.9,
                ),
            ],
            "IDS": [
                Technique(
                    "Signature Evasion",
                    "Learn IDS signatures to craft undetectable attacks",
                    "Intrusion Detection System",
                    "Analyze detection patterns to create polymorphic payloads",
                    requirements=0.5,
                    power_level=0.7,
                ),
                Technique(
                    "Alert Flooding",
                    "Generate massive false positives to hide real attacks",
                    "Intrusion Detection System",
                    "Weaponize IDS alerting mechanism to create alert fatigue",
                    requirements=0.7,
                    power_level=0.8,
                ),
            ],
            "Firewall": [
                Technique(
                    "Rule Inversion",
                    "Use firewall rules to map internal network",
                    "Network Firewall",
                    "Probe firewall rules to discover allowed ports and services",
                    requirements=0.6,
                    power_level=0.7,
                ),
                Technique(
                    "ACL Tunneling",
                    "Tunnel through allowed protocols",
                    "Network Firewall",
                    "Encapsulate attacks in protocols the firewall trusts",
                    requirements=0.8,
                    power_level=0.9,
                ),
            ],
            "Authentication": [
                Technique(
                    "Token Forgery",
                    "Craft valid tokens after learning the signing process",
                    "Authentication System",
                    "Reverse engineer token generation to forge valid credentials",
                    requirements=0.7,
                    power_level=0.9,
                ),
                Technique(
                    "Session Hijacking",
                    "Steal and reuse session mechanisms",
                    "Authentication System",
                    "Understand session management to hijack active sessions",
                    requirements=0.6,
                    power_level=0.8,
                ),
            ],
            "Encryption": [
                Technique(
                    "Crypto Oracle",
                    "Use encryption/decryption as an oracle",
                    "Encryption System",
                    "Feed crafted inputs to encryption to leak information",
                    requirements=0.8,
                    power_level=0.9,
                ),
                Technique(
                    "Key Extraction",
                    "Extract keys through side channels",
                    "Encryption System",
                    "Use timing/power analysis to recover encryption keys",
                    requirements=0.9,
                    power_level=0.95,
                ),
            ],
            "Logging": [
                Technique(
                    "Log Injection",
                    "Inject malicious data into logs",
                    "Logging System",
                    "Craft inputs that corrupt or exploit log parsing",
                    requirements=0.5,
                    power_level=0.7,
                ),
                Technique(
                    "Log Poisoning",
                    "Poison logs to hide tracks or frame others",
                    "Logging System",
                    "Manipulate log entries to cover attack traces",
                    requirements=0.7,
                    power_level=0.8,
                ),
            ],
        }

    def taste_target(
        self, target_name: str, target_type: str, code_sample: str = ""
    ) -> str:
        """
        "Taste" a target by analyzing its code/behavior (drink its blood).

        Args:
            target_name: Name of the target system
            target_type: Type (WAF, IDS, Firewall, Authentication, etc.)
            code_sample: Sample of code/config to analyze

        Returns:
            Toga's reaction to tasting the target
        """
        # Create or update absorbed knowledge
        if target_name not in self.absorbed_targets:
            self.absorbed_targets[target_name] = AbsorbedKnowledge(
                target_name=target_name,
                target_type=target_type,
                absorbed_at=datetime.now(),
            )

        knowledge = self.absorbed_targets[target_name]

        # Calculate essence absorbed from this sample
        sample_essence = min(0.15, len(code_sample) / 1000.0)  # Up to 15% per taste
        knowledge.essence_amount = min(1.0, knowledge.essence_amount + sample_essence)
        self.total_essence_collected += sample_essence

        # Learn techniques based on essence amount
        self._learn_techniques(knowledge)

        # Generate reaction
        return self._generate_taste_reaction(knowledge, sample_essence)

    def _learn_techniques(self, knowledge: AbsorbedKnowledge):
        """Learn techniques based on absorbed essence."""
        target_type = knowledge.target_type

        if target_type in self.technique_database:
            for technique in self.technique_database[target_type]:
                # Learn technique if enough essence and not already known
                if (
                    knowledge.essence_amount >= technique.requirements
                    and technique.name not in knowledge.techniques_learned
                ):

                    knowledge.techniques_learned.append(technique.name)
                    knowledge.abilities_gained.append(technique.offensive_use)

                    if technique not in self.available_techniques:
                        self.available_techniques.append(technique)

        # Unlock transformation at 70%
        if knowledge.essence_amount >= 0.7:
            knowledge.transformation_unlocked = True

    def _generate_taste_reaction(
        self, knowledge: AbsorbedKnowledge, sample_essence: float
    ) -> str:
        """Generate Toga's reaction to tasting code."""
        essence_pct = int(knowledge.essence_amount * 100)

        if knowledge.essence_amount < 0.3:
            reactions = [
                f"*licks lips* Mmm~ {knowledge.target_name}'s code tastes... interesting! I want more~ ♡",
                f"Ehehe~ Just a little taste of {knowledge.target_name}! ({essence_pct}% absorbed)",
                f"*savoring* Ooh~ {knowledge.target_name} has a unique flavor! I need to drink more~",
            ]
        elif knowledge.essence_amount < 0.7:
            reactions = [
                f"*excited* The essence of {knowledge.target_name} is flowing into me! {essence_pct}% absorbed~!",
                f"Hehe~ I'm starting to understand {knowledge.target_name}'s secrets! ♡ ({essence_pct}%)",
                f"*obsessive stare* More! I need more of {knowledge.target_name}'s blood! {essence_pct}%~",
            ]
        elif knowledge.essence_amount < 1.0:
            if not knowledge.transformation_unlocked:
                knowledge.transformation_unlocked = True
                return (
                    f"*GASP* ♡♡♡ I CAN TRANSFORM NOW! {essence_pct}% of {knowledge.target_name} "
                    f"is inside me! I can become them~! *giggles excitedly*"
                )
            reactions = [
                f"Almost there~! {essence_pct}% of {knowledge.target_name} absorbed! So close to complete mastery! ♡",
                f"*breathing heavily* {knowledge.target_name}... I almost fully understand you~ {essence_pct}%!",
            ]
        else:
            if not knowledge.is_mastered():
                return (
                    f"*EUPHORIC* ♡♡♡ YES! 100% COMPLETE! I've fully absorbed {knowledge.target_name}! "
                    f"I AM them now! All their techniques are MINE~! *triumphant laugh*"
                )
            reactions = [
                f"Ehehe~ I've completely mastered {knowledge.target_name}! ♡",
            ]

        # Add technique learning notification
        if knowledge.techniques_learned:
            last_technique = knowledge.techniques_learned[-1]
            return (
                f"{random.choice(reactions)}\n"
                f"   *New technique learned: {last_technique}!*"
            )

        return random.choice(reactions)

    def transform_into(self, target_name: str) -> str:
        """
        Transform into a target system (if enough essence absorbed).

        Args:
            target_name: Target to transform into

        Returns:
            Transformation result
        """
        if target_name not in self.absorbed_targets:
            return (
                f"*pouts* I haven't tasted {target_name} yet! I need their blood first~"
            )

        knowledge = self.absorbed_targets[target_name]

        if not knowledge.can_transform():
            essence_pct = int(knowledge.essence_amount * 100)
            return (
                f"*frustrated* Not enough essence! Only {essence_pct}% of {target_name} absorbed. "
                f"I need at least 70% to transform!"
            )

        # Activate transformation
        self.active_transformation = target_name
        self.transformation_duration = 10  # Lasts 10 actions

        return (
            f"*TRANSFORMATION* ♡♡♡\n\n"
            f"   Ehehe~! I'm becoming {target_name} now! ♡\n"
            f"   *body shifts and changes*\n"
            f"   I can feel their power flowing through me!\n"
            f"   All their defenses are now MY weapons~!\n\n"
            f"   Available techniques: {', '.join(knowledge.techniques_learned)}"
        )

    def use_technique(self, technique_name: str, target: str) -> str:
        """
        Use an absorbed technique against a target.

        Args:
            technique_name: Name of technique to use
            target: Target to use it against

        Returns:
            Attack result
        """
        # Find the technique
        technique = None
        for t in self.available_techniques:
            if t.name == technique_name:
                technique = t
                break

        if not technique:
            return f"*confused* I don't know that technique yet... Need to absorb more~"

        # Check if transformed
        if not self.active_transformation:
            return f"*pouts* I need to transform first to use {technique_name}!"

        # Check if we have the source knowledge
        source_knowledge = None
        for knowledge in self.absorbed_targets.values():
            if technique_name in knowledge.techniques_learned:
                source_knowledge = knowledge
                break

        if not source_knowledge or not source_knowledge.can_transform():
            return f"*frustrated* Don't have enough essence to use {technique_name}!"

        # Use the technique
        self.transformation_duration -= 1

        success_reactions = [
            f"*gleeful* ♡ Using {technique_name} on {target}!\n"
            f"   {technique.offensive_use}\n"
            f"   Ehehe~ Their own defense is destroying them! So ironic~!",
            f"*excited* {technique_name} activated against {target}!\n"
            f"   {technique.offensive_use}\n"
            f"   This is what I learned from absorbing {technique.source}! ♡",
            f"Hehe~ Watch THIS, {target}!\n"
            f"   *uses {technique_name}*\n"
            f"   {technique.offensive_use}\n"
            f"   Your defenses are MY weapons now~! ♡♡♡",
        ]

        result = random.choice(success_reactions)

        # Check if transformation ending
        if self.transformation_duration <= 0:
            self.active_transformation = None
            result += "\n\n*transformation ends* Ehehe~ That was fun! ♡"
        elif self.transformation_duration <= 2:
            result += f"\n   (Transformation ending soon: {self.transformation_duration} uses left)"

        return result

    def list_absorbed_targets(self) -> str:
        """List all absorbed targets and their status."""
        if not self.absorbed_targets:
            return (
                "*looks at empty list* I haven't absorbed anyone yet... Time to hunt! ♡"
            )

        output = "═══ Toga's Absorbed Knowledge ═══\n\n"

        for name, knowledge in self.absorbed_targets.items():
            essence_pct = int(knowledge.essence_amount * 100)
            status = (
                "MASTERED"
                if knowledge.is_mastered()
                else "CAN TRANSFORM" if knowledge.can_transform() else "LEARNING"
            )

            output += f"♡ {name} ({knowledge.target_type})\n"
            output += f"   Essence: {essence_pct}% [{status}]\n"
            output += f"   Techniques: {len(knowledge.techniques_learned)}\n"

            if knowledge.techniques_learned:
                output += f"   - {', '.join(knowledge.techniques_learned[:3])}"
                if len(knowledge.techniques_learned) > 3:
                    output += f" (+{len(knowledge.techniques_learned) - 3} more)"
                output += "\n"
            output += "\n"

        output += f"Total Essence Collected: {self.total_essence_collected:.2f}\n"
        output += f"Total Techniques Mastered: {len(self.available_techniques)}"

        return output

    def get_available_techniques(self) -> List[Technique]:
        """Get list of all available techniques."""
        return self.available_techniques

    def describe_technique(self, technique_name: str) -> str:
        """Get detailed description of a technique."""
        for technique in self.available_techniques:
            if technique.name == technique_name:
                return (
                    f"═══ {technique.name} ═══\n"
                    f"Source: {technique.source}\n"
                    f"Description: {technique.description}\n"
                    f"Offensive Use: {technique.offensive_use}\n"
                    f"Power Level: {technique.power_level * 100:.0f}%\n"
                    f"Requirements: {technique.requirements * 100:.0f}% essence"
                )

        return f"*confused* I don't know about {technique_name}..."


def initialize_transform_quirk() -> TogaTransformQuirk:
    """Initialize Toga's Transform Quirk system."""
    return TogaTransformQuirk()


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("  TOGA TRANSFORM QUIRK - Code Absorption Demo")
    print("  'Drinking Blood' = Absorbing System Knowledge")
    print("=" * 70)
    print()

    toga = initialize_transform_quirk()

    # Taste a WAF
    print("🎯 Encountering a Web Application Firewall...")
    print(toga.taste_target("ModSecurity WAF", "WAF", "x" * 400))
    print()

    # Taste more
    print("🔍 Analyzing more WAF rules...")
    print(toga.taste_target("ModSecurity WAF", "WAF", "x" * 600))
    print()

    # Taste even more
    print("📖 Deep diving into WAF configuration...")
    print(toga.taste_target("ModSecurity WAF", "WAF", "x" * 800))
    print()

    # Transform!
    print("🎭 Attempting transformation...")
    print(toga.transform_into("ModSecurity WAF"))
    print()

    # Use technique
    print("⚡ Using absorbed technique...")
    print(toga.use_technique("Reverse WAF Rules", "TargetWebApp"))
    print()

    # List absorbed
    print("📊 Absorbed Knowledge:")
    print(toga.list_absorbed_targets())
