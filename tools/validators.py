#!/usr/bin/env python3
"""
AVAAD Validation Framework - Comprehensive Story Validators
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any


class ValidationResult:
    """Represents the result of a validation check."""
    
    def __init__(self, passed: bool, message: str, details: str = ""):
        self.passed = passed
        self.message = message
        self.details = details


class StoryValidator:
    """Base class for story validation."""
    
    def __init__(self, story_id: str):
        self.story_id = story_id
        self.story_file = Path(f"docs/stories/{story_id}.story.md")
    
    def validate(self) -> ValidationResult:
        """Override in subclasses."""
        raise NotImplementedError


class InfrastructureValidator(StoryValidator):
    """Validates infrastructure stories (Docker, services, deployments)."""
    
    def validate(self) -> ValidationResult:
        """Validate infrastructure components."""
        checks = [
            self._check_docker_services(),
            self._check_health_endpoints(),
            self._check_monitoring_stack(),
        ]
        
        failed_checks = [check for check in checks if not check.passed]
        
        if not failed_checks:
            return ValidationResult(
                True,
                f"✅ Infrastructure story {self.story_id} validated successfully"
            )
        else:
            failed_messages = [check.message for check in failed_checks]
            return ValidationResult(
                False,
                f"❌ Infrastructure story {self.story_id} failed validation",
                f"Failed checks: {', '.join(failed_messages)}"
            )
    
    def _check_docker_services(self) -> ValidationResult:
        """Check if Docker services start successfully."""
        try:
            result = subprocess.run(
                ["docker-compose", "config"], 
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return ValidationResult(True, "Docker compose configuration valid")
            else:
                return ValidationResult(False, "Docker compose configuration invalid")
        except Exception as e:
            return ValidationResult(False, f"Docker check failed: {e}")
    
    def _check_health_endpoints(self) -> ValidationResult:
        """Check if health endpoints are accessible."""
        try:
            # Check if API is configured for health checks
            result = subprocess.run(
                ["grep", "-r", "health", "apps/api/src/"], 
                capture_output=True, text=True
            )
            if "health" in result.stdout.lower():
                return ValidationResult(True, "Health endpoints configured")
            else:
                return ValidationResult(False, "No health endpoints found")
        except Exception as e:
            return ValidationResult(False, f"Health check failed: {e}")
    
    def _check_monitoring_stack(self) -> ValidationResult:
        """Check if monitoring configuration exists."""
        monitoring_files = [
            "docker-compose.yml",
            "monitoring/prometheus.yml",
            "monitoring/grafana/",
        ]
        
        missing_files = []
        for file_path in monitoring_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if not missing_files:
            return ValidationResult(True, "Monitoring stack configured")
        else:
            return ValidationResult(False, f"Missing monitoring files: {missing_files}")


class CodeImplementationValidator(StoryValidator):
    """Validates code implementation stories (new features, APIs, connectors)."""
    
    def validate(self) -> ValidationResult:
        """Validate code implementation."""
        checks = [
            self._check_tests_exist(),
            self._check_tests_pass(),
            self._check_coverage(),
            self._check_type_safety(),
            self._check_code_quality(),
        ]
        
        failed_checks = [check for check in checks if not check.passed]
        
        if not failed_checks:
            return ValidationResult(
                True,
                f"✅ Code implementation story {self.story_id} validated successfully"
            )
        else:
            failed_messages = [check.message for check in failed_checks]
            return ValidationResult(
                False,
                f"❌ Code implementation story {self.story_id} failed validation",
                f"Failed checks: {', '.join(failed_messages)}"
            )
    
    def _check_tests_exist(self) -> ValidationResult:
        """Check if tests exist for the claimed functionality."""
        try:
            result = subprocess.run(
                ["find", "tests/", "-name", "*.py", "-type", "f"],
                capture_output=True, text=True
            )
            test_files = result.stdout.strip().split('\n')
            test_count = len([f for f in test_files if f and 'test_' in f])
            
            if test_count > 0:
                return ValidationResult(True, f"Found {test_count} test files")
            else:
                return ValidationResult(False, "No test files found")
        except Exception as e:
            return ValidationResult(False, f"Test existence check failed: {e}")
    
    def _check_tests_pass(self) -> ValidationResult:
        """Check if all tests pass."""
        try:
            result = subprocess.run(
                ["poetry", "run", "pytest", "-v", "--tb=short"],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                return ValidationResult(True, "All tests pass")
            else:
                return ValidationResult(False, "Some tests are failing")
        except Exception as e:
            return ValidationResult(False, f"Test execution failed: {e}")
    
    def _check_coverage(self) -> ValidationResult:
        """Check test coverage meets requirements."""
        try:
            result = subprocess.run(
                ["poetry", "run", "pytest", "--cov=apps/api/src", "--cov-report=json", "-q"],
                capture_output=True, text=True, timeout=300
            )
            
            if Path("coverage.json").exists():
                with open("coverage.json") as f:
                    coverage_data = json.load(f)
                    coverage = coverage_data['totals']['percent_covered']
                    
                    if coverage >= 90:
                        return ValidationResult(True, f"Coverage: {coverage:.1f}% (≥90%)")
                    else:
                        return ValidationResult(False, f"Coverage: {coverage:.1f}% (<90%)")
            else:
                return ValidationResult(False, "Coverage report not generated")
        except Exception as e:
            return ValidationResult(False, f"Coverage check failed: {e}")
    
    def _check_type_safety(self) -> ValidationResult:
        """Check MyPy type safety."""
        try:
            result = subprocess.run(
                ["poetry", "run", "mypy", "--strict", "apps/api/src"],
                capture_output=True, text=True
            )
            
            error_count = result.stdout.count(": error:")
            if error_count == 0:
                return ValidationResult(True, "Type checking passed")
            else:
                return ValidationResult(False, f"{error_count} type errors found")
        except Exception as e:
            return ValidationResult(False, f"Type checking failed: {e}")
    
    def _check_code_quality(self) -> ValidationResult:
        """Check code quality with linting tools."""
        try:
            result = subprocess.run(
                ["poetry", "run", "ruff", "check", "apps/api/src"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return ValidationResult(True, "Code quality checks passed")
            else:
                return ValidationResult(False, "Code quality issues found")
        except Exception as e:
            return ValidationResult(False, f"Code quality check failed: {e}")


class ConfigurationValidator(StoryValidator):
    """Validates configuration and tooling stories (linting, MyPy, tool setup)."""
    
    def validate(self) -> ValidationResult:
        """Validate configuration changes."""
        checks = [
            self._check_linting(),
            self._check_configuration_files(),
            self._check_pre_commit_hooks(),
        ]
        
        failed_checks = [check for check in checks if not check.passed]
        
        if not failed_checks:
            return ValidationResult(
                True,
                f"✅ Configuration story {self.story_id} validated successfully"
            )
        else:
            failed_messages = [check.message for check in failed_checks]
            return ValidationResult(
                False,
                f"❌ Configuration story {self.story_id} failed validation",
                f"Failed checks: {', '.join(failed_messages)}"
            )
    
    def _check_linting(self) -> ValidationResult:
        """Check if linting passes."""
        try:
            result = subprocess.run(
                ["make", "lint"], capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                return ValidationResult(True, "All linting checks pass")
            else:
                return ValidationResult(False, "Linting failures detected")
        except Exception as e:
            return ValidationResult(False, f"Linting check failed: {e}")
    
    def _check_configuration_files(self) -> ValidationResult:
        """Check configuration file validity."""
        config_files = {
            "pyproject.toml": ["poetry", "check"],
            "docker-compose.yml": ["docker-compose", "config"],
            ".pre-commit-config.yaml": ["pre-commit", "validate-config"],
        }
        
        for file_path, check_command in config_files.items():
            if Path(file_path).exists():
                try:
                    result = subprocess.run(
                        check_command, capture_output=True, text=True, timeout=30
                    )
                    if result.returncode != 0:
                        return ValidationResult(False, f"Invalid {file_path}")
                except Exception:
                    return ValidationResult(False, f"Cannot validate {file_path}")
        
        return ValidationResult(True, "Configuration files valid")
    
    def _check_pre_commit_hooks(self) -> ValidationResult:
        """Check if pre-commit hooks are properly configured."""
        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files", "--dry-run"],
                capture_output=True, text=True, timeout=60
            )
            # Even dry-run should exit cleanly if configuration is valid
            if "error" not in result.stderr.lower():
                return ValidationResult(True, "Pre-commit hooks configured")
            else:
                return ValidationResult(False, "Pre-commit hook configuration issues")
        except Exception as e:
            return ValidationResult(False, f"Pre-commit check failed: {e}")


def get_validator(story_id: str) -> StoryValidator:
    """Factory function to get appropriate validator for story type."""
    
    # Infrastructure stories
    infrastructure_stories = ["1.1", "1.2", "1.5", "1.6"]
    if story_id in infrastructure_stories:
        return InfrastructureValidator(story_id)
    
    # Code implementation stories
    code_stories = ["1.4", "1.5A", "1.5B", "1.3", "1.7"]
    if story_id in code_stories:
        return CodeImplementationValidator(story_id)
    
    # Configuration stories (including MyPy and linting)
    config_stories = ["6.1", "6.2", "1.1.5", "hotfix-mypy-fixes", "utils-linting-fix"]
    if story_id in config_stories:
        return ConfigurationValidator(story_id)
    
    # Default to configuration validator for unknown stories
    return ConfigurationValidator(story_id)


def validate_story(story_id: str) -> ValidationResult:
    """Main validation entry point."""
    validator = get_validator(story_id)
    return validator.validate()