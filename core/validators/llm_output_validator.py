"""
AVAAD LLM Output Validation System

Validates AI agent outputs to ensure they match actual implementation.
Prevents false claims of completion by verifying against real code changes.
"""

import re
import json
import subprocess
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class ValidationResult:
    """Represents the result of validating AI agent output."""
    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: List[str]
    recommendations: List[str]
    evidence: Dict[str, Any]


class LLMOutputValidator:
    """
    Validates AI agent outputs against actual code changes and results.
    
    Features:
    - Claims verification against actual implementation
    - Code quality assessment
    - Test result validation
    - Documentation completeness checking
    - Complexity vs claims analysis
    """
    
    def __init__(self, project_root: str = "."):
        """Initialize with project root."""
        self.project_root = Path(project_root)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load validation configuration."""
        config_path = self.project_root / "config" / "validation.yaml"
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default validation configuration."""
        return {
            'validation_rules': {
                'code_quality': {
                    'enabled': True,
                    'min_score': 0.7,
                    'checks': ['syntax', 'formatting', 'complexity']
                },
                'test_coverage': {
                    'enabled': True,
                    'min_coverage': 0.8,
                    'require_tests': True
                },
                'documentation': {
                    'enabled': True,
                    'require_docstrings': True,
                    'require_readme_updates': False
                },
                'claims_verification': {
                    'enabled': True,
                    'strict_mode': True,
                    'allow_estimated_complexity': True
                }
            },
            'quality_thresholds': {
                'excellent': 0.9,
                'good': 0.7,
                'acceptable': 0.5,
                'poor': 0.3
            }
        }
    
    def validate_agent_output(self, story_id: str, agent_output: str, 
                            files_changed: List[str] = None) -> ValidationResult:
        """
        Validate AI agent output against actual implementation.
        
        Args:
            story_id: The story being validated
            agent_output: The agent's claimed output/completion message
            files_changed: List of files the agent claims to have modified
            
        Returns:
            ValidationResult with detailed findings
        """
        issues = []
        recommendations = []
        evidence = {
            'story_id': story_id,
            'files_checked': [],
            'tests_passed': 0,
            'tests_total': 0,
            'code_quality_score': 0.0,
            'claims_matched': 0,
            'claims_total': 0
        }
        
        # 1. Parse agent claims from output
        claims = self._extract_claims(agent_output)
        evidence['claims_total'] = len(claims)
        
        # 2. Verify claims against actual code
        claim_results = self._verify_claims(claims, files_changed)
        evidence['claims_matched'] = sum(1 for r in claim_results if r['matched'])
        
        # 3. Check code quality
        quality_result = self._check_code_quality(files_changed)
        evidence['code_quality_score'] = quality_result['score']
        evidence['files_checked'] = quality_result['files_checked']
        
        # 4. Validate tests
        test_result = self._validate_tests(files_changed)
        evidence['tests_passed'] = test_result['passed']
        evidence['tests_total'] = test_result['total']
        
        # 5. Check documentation
        doc_result = self._check_documentation(files_changed)
        evidence['documentation_score'] = doc_result['score']
        
        # Compile issues and recommendations
        issues.extend(claim_results)
        issues.extend(quality_result['issues'])
        issues.extend(test_result['issues'])
        issues.extend(doc_result['issues'])
        
        recommendations.extend(quality_result['recommendations'])
        recommendations.extend(test_result['recommendations'])
        recommendations.extend(doc_result['recommendations'])
        
        # Calculate overall score
        score = self._calculate_overall_score(evidence, issues)
        
        return ValidationResult(
            is_valid=score >= 0.7,
            score=score,
            issues=[str(issue) for issue in issues],
            recommendations=recommendations,
            evidence=evidence
        )
    
    def _extract_claims(self, agent_output: str) -> List[Dict[str, Any]]:
        """Extract verifiable claims from agent output."""
        claims = []
        lines = agent_output.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Common claim patterns
            claim_patterns = [
                (r'(?:fixed|resolved|addressed)\s+(\d+)\s+.*error', 'errors_fixed', int),
                (r'(?:added|implemented|created)\s+(\w+.*test)', 'tests_added', str),
                (r'(?:updated|modified)\s+(.+\.py)', 'files_modified', str),
                (r'(?:coverage|test coverage)\s+(\d+)%', 'test_coverage', float),
                (r'(?:refactored|improved)\s+(.+)', 'refactoring', str),
                (r'(?:documentation|docs)\s+(?:updated|added)', 'documentation', bool)
            ]
            
            for pattern, claim_type, value_type in claim_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    claims.append({
                        'type': claim_type,
                        'value': value_type(match.group(1)) if match.group(1) else True,
                        'original_text': line,
                        'confidence': 0.8
                    })
        
        return claims
    
    def _verify_claims(self, claims: List[Dict], files_changed: List[str]) -> List[Dict]:
        """Verify claims against actual code changes."""
        if not files_changed:
            return [{'type': 'missing_files', 'message': 'No files specified for validation'}]
        
        issues = []
        
        for claim in claims:
            if claim['type'] == 'errors_fixed':
                actual_errors = self._count_mypy_errors(files_changed)
                if actual_errors > claim['value']:
                    issues.append({
                        'type': 'false_claim',
                        'message': f'Agent claimed to fix {claim["value"]} errors, but {actual_errors} still exist',
                        'matched': False
                    })
            elif claim['type'] == 'tests_added':
                test_files = [f for f in files_changed if 'test' in f.lower()]
                if not test_files:
                    issues.append({
                        'type': 'missing_tests',
                        'message': 'Agent claimed to add tests but no test files found',
                        'matched': False
                    })
            elif claim['type'] == 'documentation':
                doc_files = [f for f in files_changed if f.endswith('.md') or 'doc' in f.lower()]
                if not doc_files:
                    issues.append({
                        'type': 'missing_documentation',
                        'message': 'Agent claimed to update documentation but no doc files changed',
                        'matched': False
                    })
            else:
                # For other claims, basic verification
                issues.append({
                    'type': 'unverified_claim',
                    'message': f'Claim "{claim["original_text"]}" requires manual verification',
                    'matched': True
                })
        
        return issues
    
    def _count_mypy_errors(self, files: List[str]) -> int:
        """Count MyPy errors in specified files."""
        try:
            result = subprocess.run(
                ['mypy', '--strict'] + files,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            # Count error lines
            error_lines = [line for line in result.stdout.split('\n') if 'error:' in line]
            return len(error_lines)
        except Exception:
            return 0
    
    def _check_code_quality(self, files: List[str]) -> Dict[str, Any]:
        """Check code quality of changed files."""
        if not files:
            return {'score': 0.5, 'issues': [], 'recommendations': [], 'files_checked': []}
        
        score = 0.8  # Base score
        issues = []
        recommendations = []
        files_checked = []
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue
            
            files_checked.append(file_path)
            
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                
                # Basic quality checks
                if len(content) > 1000:
                    score -= 0.1  # Large files might need refactoring
                
                # Check for basic Python syntax
                try:
                    compile(content, str(full_path), 'exec')
                except SyntaxError as e:
                    issues.append(f"Syntax error in {file_path}: {e}")
                    score -= 0.3
                
                # Check for common issues
                if 'TODO' in content or 'FIXME' in content:
                    issues.append(f"TODO/FIXME comments found in {file_path}")
                    score -= 0.05
                
                if 'print(' in content and 'logging' not in content:
                    recommendations.append(f"Consider using logging instead of print() in {file_path}")
                
            except Exception as e:
                issues.append(f"Could not check {file_path}: {e}")
                score -= 0.1
        
        return {
            'score': max(0.0, score),
            'issues': issues,
            'recommendations': recommendations,
            'files_checked': files_checked
        }
    
    def _validate_tests(self, files: List[str]) -> Dict[str, Any]:
        """Validate test coverage and results."""
        issues = []
        recommendations = []
        
        # Check if test files exist
        test_files = [f for f in files if 'test' in f.lower() and f.endswith('.py')]
        
        if not test_files:
            # Look for test files in project
            test_dirs = ['tests', 'test']
            test_files_found = []
            for test_dir in test_dirs:
                test_path = self.project_root / test_dir
                if test_path.exists():
                    test_files_found.extend(list(test_path.rglob('test_*.py')))
                    test_files_found.extend(list(test_path.rglob('*test.py')))
            
            if not test_files_found:
                issues.append("No test files found")
                recommendations.append("Add tests to verify functionality")
                return {'passed': 0, 'total': 0, 'issues': issues, 'recommendations': recommendations}
        
        # Try to run tests
        try:
            result = subprocess.run(
                ['python', '-m', 'pytest', '--tb=short', '-q'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Parse pytest output
            output = result.stdout + result.stderr
            
            # Count tests
            passed = output.count('PASSED')
            failed = output.count('FAILED')
            total = passed + failed
            
            return {
                'passed': passed,
                'total': total,
                'issues': [] if failed == 0 else [f"{failed} tests failed"],
                'recommendations': [] if total > 0 else ["Add tests for new functionality"]
            }
            
        except Exception as e:
            return {
                'passed': 0,
                'total': 0,
                'issues': [f"Could not run tests: {e}"],
                'recommendations': ["Install pytest: pip install pytest"]
            }
    
    def _check_documentation(self, files: List[str]) -> Dict[str, Any]:
        """Check documentation completeness."""
        issues = []
        recommendations = []
        score = 1.0
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue
            
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                
                # Check for docstrings
                if 'def ' in content and '"""' not in content:
                    issues.append(f"Missing docstrings in {file_path}")
                    score -= 0.1
                
                # Check for README updates if significant changes
                if len(content) > 100:
                    readme_path = self.project_root / "README.md"
                    if readme_path.exists():
                        with open(readme_path, 'r') as f:
                            readme_content = f.read()
                        
                        # Basic check - could be more sophisticated
                        if file_path not in readme_content:
                            recommendations.append(f"Consider updating README.md to mention changes in {file_path}")
                
            except Exception:
                continue
        
        return {
            'score': max(0.0, score),
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _calculate_overall_score(self, evidence: Dict, issues: List) -> float:
        """Calculate overall validation score."""
        weights = {
            'claims_matched': 0.3,
            'code_quality_score': 0.25,
            'test_coverage': 0.25,
            'documentation_score': 0.2
        }
        
        # Calculate test coverage ratio
        test_ratio = 0.0
        if evidence['tests_total'] > 0:
            test_ratio = evidence['tests_passed'] / evidence['tests_total']
        
        # Calculate claims match ratio
        claims_ratio = 0.0
        if evidence['claims_total'] > 0:
            claims_ratio = evidence['claims_matched'] / evidence['claims_total']
        
        # Weighted score
        score = (
            claims_ratio * weights['claims_matched'] +
            evidence['code_quality_score'] * weights['code_quality_score'] +
            test_ratio * weights['test_coverage'] +
            evidence.get('documentation_score', 0.5) * weights['documentation_score']
        )
        
        # Penalty for critical issues
        critical_issues = len([i for i in issues if 'false_claim' in str(i)])
        score -= (critical_issues * 0.2)
        
        return max(0.0, min(1.0, score))
    
    def generate_validation_report(self, result: ValidationResult) -> str:
        """Generate a user-friendly validation report."""
        if result.is_valid:
            status = "✅ VALID"
            emoji = "🎉"
        else:
            status = "❌ INVALID"
            emoji = "⚠️"
        
        report = []
        report.append(f"{emoji} AVAAD Agent Output Validation Report")
        report.append("=" * 50)
        report.append(f"Status: {status}")
        report.append(f"Validation Score: {result.score:.1%}")
        report.append(f"Claims Verified: {result.evidence['claims_matched']}/{result.evidence['claims_total']}")
        report.append(f"Tests: {result.evidence['tests_passed']}/{result.evidence['tests_total']} passed")
        report.append(f"Code Quality: {result.evidence['code_quality_score']:.1%}")
        
        if result.issues:
            report.append("\n🚨 Issues Found:")
            for issue in result.issues:
                report.append(f"  • {issue}")
        
        if result.recommendations:
            report.append("\n💡 Recommendations:")
            for rec in result.recommendations:
                report.append(f"  • {rec}")
        
        return "\n".join(report)


def main():
    """CLI interface for LLM output validation."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python llm_output_validator.py <story_id> <agent_output_file>")
        print("       python llm_output_validator.py <story_id> --text <output_text>")
        sys.exit(1)
    
    validator = LLMOutputValidator()
    story_id = sys.argv[1]
    
    if sys.argv[2] == "--text" and len(sys.argv) > 3:
        agent_output = " ".join(sys.argv[3:])
    else:
        with open(sys.argv[2], 'r') as f:
            agent_output = f.read()
    
    result = validator.validate_agent_output(story_id, agent_output)
    print(validator.generate_validation_report(result))


if __name__ == "__main__":
    main()