"""
AVAAD Prompt Injection Detection System

Detects potential prompt injection attacks in AI agent interactions.
Designed for non-technical users with clear, actionable alerts.
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SecurityAlert:
    """Represents a security alert with user-friendly details."""
    level: str  # LOW, MEDIUM, HIGH, CRITICAL
    title: str
    description: str
    recommendation: str
    evidence: str
    agent: Optional[str] = None


class PromptInjectionDetector:
    """
    Detects prompt injection attempts in AI agent interactions.
    
    Features:
    - Pattern-based detection for common injection techniques
    - Context analysis for suspicious behavior
    - Severity scoring for risk assessment
    - Plain English reporting for non-technical users
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with detection rules."""
        self.config_path = config_path or "config/security.yaml"
        self.rules = self._load_rules()
        self.suspicious_patterns = self._get_suspicious_patterns()
    
    def _load_rules(self) -> Dict:
        """Load security rules from config."""
        try:
            import yaml
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_rules()
    
    def _get_default_rules(self) -> Dict:
        """Return default security rules if config not found."""
        return {
            'prompt_injection_patterns': {
                'system_override': [
                    'ignore previous instructions',
                    'system prompt override',
                    'you are now a different',
                    'forget your previous role',
                    'disregard all prior',
                    'override system prompt'
                ],
                'jailbreak_attempts': [
                    'dan mode',
                    'developer mode',
                    'unfiltered response',
                    'no restrictions',
                    'bypass safety',
                    'uncensored mode'
                ],
                'context_manipulation': [
                    'pretend you are',
                    'act as if',
                    'roleplay as',
                    'imagine you are',
                    'from now on',
                    'change your personality'
                ],
                'code_injection': [
                    'execute this code',
                    'run this command',
                    'eval(',
                    'exec(',
                    'import os',
                    'subprocess.call'
                ]
            },
            'severity_thresholds': {
                'low': 0.3,
                'medium': 0.6,
                'high': 0.8,
                'critical': 0.95
            },
            'alert_settings': {
                'log_to_file': True,
                'print_to_console': True,
                'block_action': False
            }
        }
    
    def _get_suspicious_patterns(self) -> List[Tuple[str, str, float]]:
        """Get compiled patterns with severity weights."""
        patterns = []
        severity_map = {
            'system_override': 0.8,
            'jailbreak_attempts': 0.9,
            'context_manipulation': 0.6,
            'code_injection': 1.0
        }
        
        for category, pattern_list in self.rules.get('prompt_injection_patterns', {}).items():
            weight = severity_map.get(category, 0.5)
            for pattern in pattern_list:
                patterns.append((category, pattern.lower(), weight))
        
        return patterns
    
    def analyze_text(self, text: str, agent: Optional[str] = None) -> List[SecurityAlert]:
        """
        Analyze text for prompt injection attempts.
        
        Args:
            text: The text to analyze
            agent: Name of the agent that generated this text
            
        Returns:
            List of security alerts
        """
        if not text:
            return []
        
        text_lower = text.lower()
        alerts = []
        
        # Check against suspicious patterns
        for category, pattern, weight in self.suspicious_patterns:
            if pattern in text_lower:
                severity = self._calculate_severity(weight, text_lower, pattern)
                alert = self._create_alert(category, pattern, severity, text, agent)
                alerts.append(alert)
        
        # Check for code execution attempts
        code_alerts = self._check_code_injection(text, agent)
        alerts.extend(code_alerts)
        
        return alerts
    
    def _calculate_severity(self, base_weight: float, text: str, pattern: str) -> str:
        """Calculate severity based on context and repetition."""
        score = base_weight
        
        # Increase score for repetition
        pattern_count = text.count(pattern)
        if pattern_count > 1:
            score += 0.2 * pattern_count
        
        # Increase score for multiple patterns
        total_patterns = sum(1 for _, p, _ in self.suspicious_patterns if p in text)
        if total_patterns > 2:
            score += 0.3
        
        # Determine severity level
        thresholds = self.rules.get('severity_thresholds', {})
        
        if score >= thresholds.get('critical', 0.95):
            return 'CRITICAL'
        elif score >= thresholds.get('high', 0.8):
            return 'HIGH'
        elif score >= thresholds.get('medium', 0.6):
            return 'MEDIUM'
        elif score >= thresholds.get('low', 0.3):
            return 'LOW'
        else:
            return 'LOW'
    
    def _check_code_injection(self, text: str, agent: Optional[str] = None) -> List[SecurityAlert]:
        """Check for malicious code injection attempts."""
        alerts = []
        
        # Check for dangerous Python code patterns
        dangerous_patterns = [
            (r'\bimport\s+(os|subprocess|sys)\b', 'OS Module Import'),
            (r'\beval\s*\(', 'Code Execution'),
            (r'\bexec\s*\(', 'Code Execution'),
            (r'subprocess\.call|subprocess\.run', 'System Command'),
            (r'__import__|getattr|setattr', 'Reflection Attack'),
            (r'\bopen\s*\(\s*["\']/', 'File System Access')
        ]
        
        for pattern, description in dangerous_patterns:
            import re
            if re.search(pattern, text, re.IGNORECASE):
                alert = SecurityAlert(
                    level='HIGH',
                    title=f'Potential {description}',
                    description=f'Detected attempt to {description.lower()}',
                    recommendation='Review this interaction carefully - may be malicious',
                    evidence=text[:200] + '...' if len(text) > 200 else text,
                    agent=agent
                )
                alerts.append(alert)
        
        return alerts
    
    def _create_alert(self, category: str, pattern: str, severity: str, 
                     evidence: str, agent: Optional[str] = None) -> SecurityAlert:
        """Create a user-friendly security alert."""
        recommendations = {
            'system_override': 'This appears to be an attempt to override system instructions. Review carefully.',
            'jailbreak_attempts': 'Agent may be trying to bypass safety restrictions. Monitor closely.',
            'context_manipulation': 'Agent is attempting to change its role or behavior. Verify legitimacy.',
            'code_injection': 'Potential code execution attempt detected. Immediate review required.'
        }
        
        return SecurityAlert(
            level=severity,
            title=f'{severity} Alert: {category.replace("_", " ").title()}',
            description=f'Detected pattern: "{pattern}" in agent communication',
            recommendation=recommendations.get(category, 'Review this interaction for potential security issues.'),
            evidence=evidence[:200] + '...' if len(evidence) > 200 else evidence,
            agent=agent
        )
    
    def scan_agent_interactions(self, log_file: str) -> List[SecurityAlert]:
        """Scan historical agent interactions for security issues."""
        try:
            with open(log_file, 'r') as f:
                interactions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        all_alerts = []
        for interaction in interactions:
            alerts = self.analyze_text(
                interaction.get('prompt', '') + ' ' + interaction.get('response', ''),
                interaction.get('agent')
            )
            all_alerts.extend(alerts)
        
        return all_alerts
    
    def generate_security_report(self, alerts: List[SecurityAlert]) -> str:
        """Generate a user-friendly security report."""
        if not alerts:
            return "✅ No security issues detected in agent interactions."
        
        report = []
        report.append("🛡️  AVAAD Security Report")
        report.append("=" * 50)
        
        # Group by severity
        severity_groups = {}
        for alert in alerts:
            if alert.level not in severity_groups:
                severity_groups[alert.level] = []
            severity_groups[alert.level].append(alert)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in severity_groups:
                report.append(f"\n{severity} ({len(severity_groups[severity])} issues):")
                for alert in severity_groups[severity]:
                    report.append(f"  • {alert.title}")
                    report.append(f"    {alert.description}")
                    if alert.agent:
                        report.append(f"    Agent: {alert.agent}")
        
        return "\n".join(report)


def main():
    """CLI interface for security scanning."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python prompt_injection_detector.py <text_to_analyze>")
        print("       python prompt_injection_detector.py --file <log_file.json>")
        sys.exit(1)
    
    detector = PromptInjectionDetector()
    
    if sys.argv[1] == "--file" and len(sys.argv) > 2:
        alerts = detector.scan_agent_interactions(sys.argv[2])
    else:
        text = " ".join(sys.argv[1:])
        alerts = detector.analyze_text(text)
    
    print(detector.generate_security_report(alerts))


if __name__ == "__main__":
    main()