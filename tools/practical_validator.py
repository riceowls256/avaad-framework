#!/usr/bin/env python3
"""
AVAAD Practical Validator - Tests what stories actually claim to deliver
"""

import subprocess
import time
from pathlib import Path


def validate_story_practical(story_id: str) -> tuple[bool, str]:
    """Practical validation that tests what the story actually claims."""
    
    print(f"🔍 Practical validation for Story {story_id}")
    
    if story_id == "1.1":
        return validate_containerization()
    elif story_id == "1.4":
        return validate_databento_connector()
    elif story_id == "1.1.5":
        return validate_structured_logging()
    elif story_id in ["6.1", "6.2"]:
        return validate_mypy_and_inventory()
    else:
        return False, f"Validation not implemented for story {story_id}"


def validate_containerization() -> tuple[bool, str]:
    """Story 1.1: Check if Docker containers actually start and work."""
    
    print("📦 Testing if containers start...")
    
    try:
        # Check if docker-compose.yml exists
        if not Path("docker-compose.yml").exists():
            return False, "docker-compose.yml missing"
        
        # Try to validate docker-compose config
        result = subprocess.run(
            ["docker-compose", "config"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode != 0:
            return False, f"docker-compose config invalid: {result.stderr}"
        
        # Try to start services (but don't leave them running)
        print("🚀 Testing if containers can start...")
        start_result = subprocess.run(
            ["docker-compose", "up", "-d", "--no-deps", "api"],
            capture_output=True, text=True, timeout=60
        )
        
        if start_result.returncode == 0:
            # Clean up
            subprocess.run(["docker-compose", "down"], capture_output=True, timeout=30)
            return True, "Containers can start successfully"
        else:
            return False, f"Containers failed to start: {start_result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "Container startup timed out"
    except Exception as e:
        return False, f"Container test failed: {e}"


def validate_databento_connector() -> tuple[bool, str]:
    """Story 1.4: Check if DataBento connector code actually works."""
    
    print("🔌 Testing DataBento connector...")
    
    try:
        # Check if connector file exists
        connector_file = Path("apps/api/src/services/connectors/databento_connector.py")
        if not connector_file.exists():
            return False, "DataBento connector file missing"
        
        # Try to import the connector
        import_test = subprocess.run([
            "python", "-c", 
            "import sys; sys.path.append('apps/api/src'); "
            "from services.connectors.databento_connector import DataBentoConnector; "
            "print('Import successful')"
        ], capture_output=True, text=True, timeout=10)
        
        if import_test.returncode != 0:
            return False, f"Connector import failed: {import_test.stderr}"
        
        # Check if tests exist for the connector
        test_files = list(Path("tests").glob("**/test*databento*"))
        if not test_files:
            return False, "No tests found for DataBento connector"
        
        # Run connector-specific tests
        test_result = subprocess.run([
            "poetry", "run", "pytest", "-v", "-k", "databento", "--tb=short"
        ], capture_output=True, text=True, timeout=60)
        
        if test_result.returncode == 0:
            return True, "DataBento connector tests pass"
        else:
            return False, f"DataBento connector tests fail: {test_result.stdout}"
            
    except Exception as e:
        return False, f"DataBento connector validation failed: {e}"


def validate_structured_logging() -> tuple[bool, str]:
    """Story 1.1.5: Check if structured logging actually works."""
    
    print("📝 Testing structured logging...")
    
    try:
        # Check if logging module exists
        logging_file = Path("apps/api/src/core/logging.py")
        if not logging_file.exists():
            return False, "Logging module missing"
        
        # Try to import and use logging
        logging_test = subprocess.run([
            "python", "-c",
            "import sys; sys.path.append('apps/api/src'); "
            "from core.logging import get_logger; "
            "logger = get_logger('test'); "
            "logger.info('Test message'); "
            "print('Logging works')"
        ], capture_output=True, text=True, timeout=10)
        
        if logging_test.returncode != 0:
            return False, f"Logging import/usage failed: {logging_test.stderr}"
        
        # Check if pre-commit/linting passes (required for story completion)
        lint_result = subprocess.run([
            "poetry", "run", "ruff", "check", "apps/api/src/core/logging.py"
        ], capture_output=True, text=True, timeout=30)
        
        if lint_result.returncode == 0:
            return True, "Structured logging works and passes linting"
        else:
            return False, f"Logging has linting issues: {lint_result.stdout}"
            
    except Exception as e:
        return False, f"Structured logging validation failed: {e}"


def validate_mypy_and_inventory() -> tuple[bool, str]:
    """Stories 6.1/6.2: Check if MyPy strict mode actually works."""
    
    print("🔍 Testing MyPy strict mode...")
    
    try:
        # Check pyproject.toml has strict = true
        with open("pyproject.toml", "r") as f:
            content = f.read()
            if "strict = true" not in content:
                return False, "MyPy strict mode not enabled in pyproject.toml"
        
        # Run MyPy and check for errors
        mypy_result = subprocess.run([
            "poetry", "run", "mypy", "--strict", "apps/api/src", "packages/db"
        ], capture_output=True, text=True, timeout=120)
        
        error_count = mypy_result.stdout.count(": error:")
        
        if error_count == 0:
            return True, "MyPy strict mode enabled with 0 errors"
        else:
            return False, f"MyPy has {error_count} errors in strict mode"
            
    except Exception as e:
        return False, f"MyPy validation failed: {e}"


def main():
    """Test the practical validator."""
    if len(sys.argv) != 2:
        print("Usage: python practical_validator.py STORY_ID")
        sys.exit(1)
    
    story_id = sys.argv[1]
    is_valid, message = validate_story_practical(story_id)
    
    if is_valid:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()