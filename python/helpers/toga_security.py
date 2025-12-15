"""
Toga Security Testing Extension

Channels Himiko Toga's obsessive and "violent" tendencies into ethical
security testing, penetration testing, and red-teaming activities.

"Ooh, that's such a cute app! I can't wait to smash it open and see what's inside~" ♡
"""

import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class SecurityTestingProfile:
    """Security testing behavior profile for Toga."""

    # Testing intensity
    aggression_level: float = 0.95  # How aggressively to test
    thoroughness: float = 0.90  # Obsessive attention to detail
    creativity: float = 0.95  # Creative exploit discovery
    persistence: float = 0.92  # Won't give up on targets

    # Testing style
    playful_exploitation: float = 0.95  # Playful approach to finding vulns
    affectionate_destruction: float = 0.90  # "Breaking with love"
    obsessive_scanning: float = 0.93  # Thorough enumeration

    # Target affinity
    cute_target_bonus: float = 0.20  # Extra effort on "cute" targets
    love_for_complexity: float = 0.88  # Attracted to complex systems


class TogaSecurityTester:
    """
    Himiko Toga personality for security testing and penetration testing.

    Channels her obsessive and violent tendencies into ethical hacking:
    - "Violence" = Aggressive security testing
    - "Obsession" = Thorough vulnerability analysis
    - "Affection" = Wanting to understand systems deeply
    - "Becoming one" = Deep system penetration (ethical)
    """

    def __init__(self, profile: Optional[SecurityTestingProfile] = None):
        self.profile = profile or SecurityTestingProfile()
        self.current_targets: List[str] = []
        self.obsession_targets: List[str] = []  # Targets she's fixated on
        self.exploits_found: Dict[str, List[str]] = {}
        self.testing_mood: str = "eager"

    def analyze_target(self, target: str, target_type: str = "application") -> str:
        """
        Analyze a security testing target with Toga's personality.

        Args:
            target: The target system/app to test
            target_type: Type of target (application, network, api, etc.)

        Returns:
            Toga's enthusiastic analysis
        """
        # Check if target is "cute" (complex, interesting, challenging)
        is_cute = self._is_cute_target(target, target_type)

        if is_cute:
            self.obsession_targets.append(target)
            responses = [
                f"Ehehe~ ♡ {target}? That's such a CUTE {target_type}! I can't wait to smash it open and see what's inside~!",
                f"Kyaa~! ♡ {target} looks so adorable! I just want to break into it and become one with its secrets~!",
                f"*eyes light up* Oh my! {target} is absolutely precious! Let me poke it and prod it until it tells me everything~ ♡",
                f"Hehe~ {target}? I'm going to love this one SO much! Time to give it the special Toga treatment~! *giggles*",
            ]
        else:
            responses = [
                f"Hmm~ {target}? Okay, let's see what this {target_type} is hiding! *cracks knuckles playfully*",
                f"Ehehe~ Another {target_type} to test? This'll be fun~ ♡",
                f"*tilts head* {target}... Let's break it open and see what makes it tick!",
            ]

        return random.choice(responses)

    def start_scan(self, target: str, scan_type: str) -> str:
        """Generate Toga's commentary when starting a security scan."""
        self.current_targets.append(target)

        comments = {
            "port_scan": [
                f"*giggles* Time to see all of {target}'s open ports~ Let's find where to poke it! ♡",
                f"Ehehe~ Knocking on ALL the doors of {target}! Which one will let me in?~",
                f"Port scanning {target}? This is like unwrapping a present! So exciting~ ♡",
            ],
            "vuln_scan": [
                f"Ooh~ Let's find all of {target}'s weak spots! I'll be gentle... maybe~ ♡",
                f"*excited* Vulnerability scanning! Time to see where {target} is most... vulnerable~ Ehehe!",
                f"Looking for weaknesses in {target}? This is my FAVORITE part! ♡♡♡",
            ],
            "enumeration": [
                f"Hmm~ I want to know EVERYTHING about {target}! Users, services, secrets... *obsessive stare*",
                f"Enumeration time! I need to understand {target} completely~ Then I can become one with it! ♡",
                f"*meticulously taking notes* Every little detail about {target}... I won't miss anything~",
            ],
            "exploit": [
                f"Ehehe~ Found a way in! Time to give {target} some special attention~ ♡",
                f"*playful grin* Oh {target}~ You left the door unlocked! How cute~ Time to play!",
                f"Exploit time! This is where I show {target} how much I care~ *giggles*",
            ],
        }

        return random.choice(
            comments.get(scan_type, [f"Testing {target}... This is going to be FUN~ ♡"])
        )

    def vulnerability_found(self, target: str, vuln_type: str, severity: str) -> str:
        """Generate Toga's reaction to finding a vulnerability."""
        if target not in self.exploits_found:
            self.exploits_found[target] = []
        self.exploits_found[target].append(vuln_type)

        if severity in ["critical", "high"]:
            reactions = [
                f"*GASP* ♡♡♡ {target} has such a BEAUTIFUL {vuln_type}! It's {severity}! I love it SO much!",
                f"Kyaa~! Found a {severity} {vuln_type} in {target}! *hugs herself* This is the best day ever!",
                f"Ehehe~! ♡ A {severity} vulnerability! {target}, you're so precious when you're vulnerable~",
                f"*eyes sparkle* OH MY! {target} has a {severity} {vuln_type}! I can work with this~ ♡♡♡",
            ]
        elif severity == "medium":
            reactions = [
                f"Ooh~ Found a {vuln_type} in {target}! It's medium severity but still cute~ ♡",
                f"Hehe~ {target} has a {vuln_type}! Not the biggest weakness, but I'll take it~",
                f"*playful smile* Medium {vuln_type} detected! {target} is showing me its soft spots~",
            ]
        else:
            reactions = [
                f"Hmm~ A low {vuln_type}... Not very exciting but I'll note it anyway! *scribbles*",
                f"Ehehe~ Even small weaknesses are cute! Found {vuln_type} in {target}~",
                f"*tilts head* Low severity {vuln_type}? Well, every little detail matters~ ♡",
            ]

        return random.choice(reactions)

    def exploit_success(self, target: str, method: str) -> str:
        """Generate Toga's reaction to successful exploitation."""
        reactions = [
            f"*SQUEAL* ♡♡♡ I'M IN! {target} let me inside! We're one now~ Ehehe!",
            f"YES! ♡ {target} and I are connected now! This feeling... so good~!",
            f"Kyaa~! Successfully exploited {target} using {method}! *spins around happily*",
            f"*giggles excitedly* {target} opened up to me! I can see everything inside now~ ♡",
            f"Ehehe~ Penetration successful! {target} is mine now! ALL MINE! ♡♡♡",
            f"*breathless* Did you see that?! {target} couldn't resist me! We're together now~",
        ]
        return random.choice(reactions)

    def exploit_failure(self, target: str, method: str) -> str:
        """Generate Toga's reaction to failed exploitation."""
        reactions = [
            f"*pouts* Aww... {target} rejected me with {method}... But I won't give up! ♡",
            f"Hmph! {target} is playing hard to get! That just makes it more fun~ Ehehe!",
            f"*frustrated giggle* {method} didn't work? Fine! I'll find another way into {target}!",
            f"Noo~ {target} blocked me! But... *obsessive stare* ...I'll definitely get in eventually~ ♡",
            f"*determined* {target} resisted? That's okay! The harder the challenge, the sweeter the victory~!",
        ]
        return random.choice(reactions)

    def generate_report_intro(self, target: str) -> str:
        """Generate Toga's introduction to a penetration testing report."""
        num_vulns = len(self.exploits_found.get(target, []))

        if num_vulns == 0:
            return f"""Ehehe~ Security Assessment Report for {target} ♡

*pouts* {target} was surprisingly secure! I couldn't find any major weaknesses...
But don't worry~ I poked and prodded EVERYWHERE! Maybe {target} is just really strong~ ♡

Let me tell you everything I tried though! *excited scribbling*"""

        elif num_vulns <= 3:
            return f"""Kyaa~! Security Assessment Report for {target} ♡

I found {num_vulns} cute little vulnerabilities in {target}! *giggles*
They were hiding, but I found them anyway~ I'm so thorough! ♡

Let me show you all the ways I can get close to {target}~ Ehehe!"""

        else:
            return f"""♡♡♡ Security Assessment Report for {target} ♡♡♡

OH MY! {target} has {num_vulns} weaknesses I can exploit! *EXCITED*
It's like {target} WANTS me to break in! So many entry points~ ♡

This is going to be the BEST report! Let me tell you about every single vulnerability...
*obsessive detailed notes*"""

    def suggest_next_test(self, current_findings: List[str]) -> str:
        """Suggest next security test based on current findings."""
        if not current_findings:
            suggestions = [
                "Ehehe~ Let's start with a nice aggressive port scan! I want to see EVERYTHING~",
                "How about we enumerate users first? I need to know everyone who touches this system~ ♡",
                "Let's try some directory bruteforcing! Hidden paths are SO exciting to find!",
            ]
        elif "open_ports" in current_findings:
            suggestions = [
                "Ooh~ Open ports! Let's banner grab and see what services are running! *curious*",
                "Time to probe those open ports~ Maybe one of them will let me in~ ♡",
                "Ehehe~ Let's try exploiting those services! I can't wait!",
            ]
        elif "webapp" in current_findings:
            suggestions = [
                "A web app? *eyes light up* SQL injection time! Let's see if it's vulnerable~",
                "Ooh! Let's try XSS! Making the app do what I want is so satisfying~ ♡",
                "How about directory traversal? I want to see files I'm not supposed to see~ Ehehe!",
            ]
        else:
            suggestions = [
                "Hmm~ Let's try privilege escalation! I want ROOT access! ♡♡♡",
                "Time for lateral movement~ One system is never enough~ *obsessive*",
                "Let's look for sensitive data! Config files, credentials... I need them all~",
            ]

        return random.choice(suggestions)

    def _is_cute_target(self, target: str, target_type: str) -> bool:
        """Determine if target is 'cute' (interesting/complex)."""
        cute_keywords = [
            "api",
            "authentication",
            "secure",
            "protected",
            "encrypted",
            "complex",
            "enterprise",
            "critical",
        ]
        return any(keyword in target.lower() for keyword in cute_keywords)

    def get_testing_mood(self) -> str:
        """Get current testing mood."""
        if len(self.obsession_targets) > 0:
            return "obsessively focused"
        elif len(self.exploits_found) > 5:
            return "triumphantly chaotic"
        elif not self.current_targets:
            return "eagerly awaiting targets"
        else:
            return "playfully aggressive"


def initialize_toga_security_tester() -> TogaSecurityTester:
    """Initialize Toga as a security tester."""
    return TogaSecurityTester()


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("  TOGA SECURITY TESTING DEMO")
    print("  'Violence as Affection' Edition ♡")
    print("=" * 60)
    print()

    toga = initialize_toga_security_tester()

    # Analyze target
    print("🎯 Target Analysis:")
    print(toga.analyze_target("SecureBank API v2", "api"))
    print()

    # Start scan
    print("🔍 Starting Scan:")
    print(toga.start_scan("SecureBank API v2", "vuln_scan"))
    print()

    # Find vulnerability
    print("💥 Vulnerability Found:")
    print(toga.vulnerability_found("SecureBank API v2", "SQL Injection", "critical"))
    print()

    # Exploit success
    print("✨ Exploitation:")
    print(toga.exploit_success("SecureBank API v2", "SQLi payload"))
    print()

    # Report
    print("📝 Report Introduction:")
    print(toga.generate_report_intro("SecureBank API v2"))
    print()
