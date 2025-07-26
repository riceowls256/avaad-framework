# Python Migration Plan: From Bash to Bulletproof

## 🎯 Objective
Migrate all brittle bash validation scripts to a robust Python framework that non-technical users can trust and AI agents can't game.

---

## 🚨 Why This Migration is Critical

### Current Problems with Bash Scripts
1. **Cryptic Error Messages**: `"line 45: [: too many arguments"` means nothing to non-coders
2. **Platform Inconsistency**: Works on Linux, breaks on Mac, who knows on Windows
3. **Silent Failures**: Scripts can fail without clear indication
4. **Hard to Debug**: AI agents struggle with bash syntax errors
5. **No Recovery Guidance**: When it breaks, users are stuck

### Python Advantages
1. **Clear Error Handling**: Try/except with human-readable messages
2. **Cross-Platform**: Same behavior everywhere
3. **Better AI Understanding**: Agents work better with Python
4. **Rich Ecosystem**: Libraries for everything we need
5. **Easy Testing**: Unit tests ensure reliability

---

## 📋 Migration Priority Order

### Phase 1: Core Validators (Week 1)
Critical scripts that must be rock-solid:

1. **story-completion-validator.sh** → `avaad.py validate`
   - Entry point for all validation
   - Must have --explain mode
   - Clear success/failure indication

2. **technical-debt-gate-check.sh** → `avaad.py check-debt`
   - Compares against baselines
   - Prevents regression
   - Simple pass/fail output

3. **mypy-story-validator.sh** → `validators/mypy_strict.py`
   - Most complex validation logic
   - File-by-file checking
   - Error extraction and reporting

### Phase 2: Specialized Validators (Week 2)
Story-type specific validators:

4. **database-story-validator.sh** → `validators/database.py`
5. **configuration-story-validator.sh** → `validators/configuration.py`
6. **infrastructure-story-validator.sh** → `validators/infrastructure.py`
7. **generic-story-validator.sh** → `validators/generic.py`

### Phase 3: Utilities & Reporting (Week 3)
Supporting scripts:

8. **validate-all-complete-stories.sh** → `avaad.py validate-all`
9. **completion-report-generator.py** → Enhanced Python version
10. **demo-validation-framework.sh** → `avaad.py demo`

---

## 🏗️ Architecture Design

### Core Structure
```python
avaad/
├── __init__.py
├── avaad.py              # Main CLI entry point
├── core/
│   ├── __init__.py
│   ├── validator.py      # Base validator class
│   ├── artifacts.py      # Proof-of-work system
│   ├── errors.py         # Custom exceptions
│   └── utils.py          # Shared utilities
├── validators/
│   ├── __init__.py
│   ├── mypy_strict.py    # MyPy validation
│   ├── tests.py          # Test runner validation
│   ├── database.py       # Database validation
│   ├── configuration.py  # Config file validation
│   └── infrastructure.py # Docker/CI validation
├── ui/
│   ├── __init__.py
│   ├── cli.py            # Command-line interface
│   ├── explain.py        # Natural language explanations
│   └── dashboard.py      # Terminal dashboard
└── agents/
    ├── __init__.py
    ├── tracker.py        # Agent performance tracking
    └── profiles.py       # Agent profile management
```

### Base Validator Pattern
```python
# core/validator.py
class BaseValidator(ABC):
    """Base class for all validators"""

    def __init__(self, story_id: str, explain_mode: bool = False):
        self.story_id = story_id
        self.explain_mode = explain_mode
        self.errors = []
        self.warnings = []

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Run validation and return result"""
        pass

    def explain(self, message: str) -> None:
        """Output explanation in plain English"""
        if self.explain_mode:
            print(f"🔍 {message}")

    def add_error(self, error: str, suggestion: str = None) -> None:
        """Add error with optional fix suggestion"""
        self.errors.append({
            'message': error,
            'suggestion': suggestion,
            'technical_details': self._get_technical_details()
        })
```

---

## 🔧 Implementation Examples

### 1. Main Entry Point (`avaad.py`)
```python
#!/usr/bin/env python3
"""AVAAD - Automated Verification for AI-Assisted Development"""

import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version='2.0.0')
def cli():
    """AVAAD - Verify AI agent work with confidence"""
    pass

@cli.command()
@click.argument('story_id')
@click.option('--explain', is_flag=True, help='Explain what is being checked')
@click.option('--fix-suggestions', is_flag=True, help='Show how to fix failures')
def validate(story_id, explain, fix_suggestions):
    """Validate a story is actually complete"""

    if explain:
        console.print(f"[blue]Checking if Story {story_id} is really complete...[/blue]")

    # Run validation
    validator = StoryValidator(story_id, explain_mode=explain)
    result = validator.validate()

    # Display results
    if result.passed:
        console.print(f"[green]✅ Story {story_id}: VERIFIED COMPLETE[/green]")
        return 0
    else:
        console.print(f"[red]❌ Story {story_id}: NOT COMPLETE[/red]")
        console.print(f"[yellow]Found {len(result.errors)} issues:[/yellow]")

        for error in result.errors:
            console.print(f"  • {error.message}")
            if fix_suggestions and error.suggestion:
                console.print(f"    [dim]Fix: {error.suggestion}[/dim]")

        return 1
```

### 2. MyPy Validator (`validators/mypy_strict.py`)
```python
class MypyValidator(BaseValidator):
    """Validates MyPy strict mode compliance"""

    def validate(self) -> ValidationResult:
        self.explain("Running MyPy in strict mode on claimed files...")

        # Get files from story
        files = self._get_claimed_files()

        # Check each file
        total_errors = 0
        for file in files:
            self.explain(f"Checking {file}...")
            errors = self._run_mypy_on_file(file)

            if errors:
                self.add_error(
                    f"{file} has {len(errors)} MyPy errors",
                    f"Run 'poetry run mypy {file} --strict' to see details"
                )
                total_errors += len(errors)

        # Check against baseline
        baseline = self._get_baseline()
        if total_errors > baseline:
            self.add_error(
                f"MyPy errors increased from {baseline} to {total_errors}",
                "Fix the new errors before marking complete"
            )

        return ValidationResult(
            passed=len(self.errors) == 0,
            errors=self.errors,
            artifacts=self._generate_artifacts()
        )
```

### 3. Error Handling Example
```python
# core/errors.py
class AVAADError(Exception):
    """Base exception for AVAAD"""

    def __init__(self, message: str, suggestion: str = None, technical: str = None):
        self.message = message
        self.suggestion = suggestion
        self.technical = technical
        super().__init__(self.message)

    def display(self, console: Console):
        """Display error in user-friendly format"""
        console.print(f"[red]Error:[/red] {self.message}")

        if self.suggestion:
            console.print(f"[yellow]Try:[/yellow] {self.suggestion}")

        if self.technical and console.is_verbose:
            console.print(f"[dim]Technical: {self.technical}[/dim]")

class DependencyError(AVAADError):
    """Raised when required tools are missing"""
    pass

class ValidationError(AVAADError):
    """Raised when validation fails"""
    pass

# Usage
try:
    result = subprocess.run(['poetry', 'run', 'mypy'], capture_output=True)
except FileNotFoundError:
    raise DependencyError(
        "Poetry is not installed",
        "Install Poetry from https://python-poetry.org/docs/#installation",
        "FileNotFoundError: [Errno 2] No such file or directory: 'poetry'"
    )
```

---

## 🛡️ Reliability Features

### 1. Self-Test Command
```python
@cli.command()
def self_test():
    """Verify AVAAD is working correctly"""
    console.print("[blue]Running AVAAD self-test...[/blue]")

    tests = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File permissions", check_permissions),
        ("Tool availability", check_tools),
        ("Configuration", check_configuration)
    ]

    all_passed = True
    for name, test_func in tests:
        try:
            test_func()
            console.print(f"✅ {name}")
        except Exception as e:
            console.print(f"❌ {name}: {e}")
            all_passed = False

    if all_passed:
        console.print("[green]All tests passed! AVAAD is ready.[/green]")
    else:
        console.print("[red]Some tests failed. Run 'avaad fix' for solutions.[/red]")
```

### 2. Automatic Recovery
```python
def check_and_fix_poetry():
    """Check if Poetry is available and working"""
    try:
        subprocess.run(['poetry', '--version'], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("[yellow]Poetry not found. Installing...[/yellow]")

        # Try to install Poetry
        install_script = "https://install.python-poetry.org"
        subprocess.run(['curl', '-sSL', install_script, '|', 'python3'], shell=True)

        # Verify installation
        if shutil.which('poetry'):
            console.print("[green]Poetry installed successfully![/green]")
        else:
            raise DependencyError(
                "Could not install Poetry automatically",
                "Please install manually from https://python-poetry.org"
            )
```

---

## 🧪 Testing Strategy

### Unit Tests for Each Validator
```python
# tests/test_mypy_validator.py
def test_mypy_validator_detects_errors():
    """Test that validator correctly identifies MyPy errors"""
    validator = MypyValidator("test-story")

    # Mock file with errors
    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = "file.py:10: error: Missing type annotation"

        result = validator.validate()

        assert not result.passed
        assert len(result.errors) == 1
        assert "Missing type annotation" in result.errors[0].message
```

### Integration Tests
```python
def test_full_validation_flow():
    """Test complete validation process"""
    # Create test story file
    # Run validation
    # Check artifacts generated
    # Verify correct output
    pass
```

---

## 📊 Migration Metrics

Track progress with these metrics:
1. **Scripts Migrated**: X/10 complete
2. **Test Coverage**: Aim for 90%+
3. **Error Clarity**: User feedback on messages
4. **Cross-Platform**: Test on Linux/Mac/Windows
5. **Agent Success**: Do agents work better with Python?

---

## 🚀 Rollout Plan

### Week 1: Core Migration
- Day 1-2: Set up Python project structure
- Day 3-4: Migrate main validator
- Day 5: Migrate MyPy validator
- Day 6-7: Testing and refinement

### Week 2: Complete Migration
- Migrate remaining validators
- Add explain mode to all
- Implement self-test
- Create fallback validators

### Week 3: Polish & Release
- Enhanced error messages
- Agent instruction templates
- Documentation
- Community release

---

## ✅ Success Criteria

The migration is successful when:
1. **All bash scripts replaced** with Python equivalents
2. **Error messages** are clear to non-technical users
3. **Cross-platform** tests pass on all OS types
4. **AI agents** can use the tools without assistance
5. **Self-test** catches and fixes common issues
6. **Users report** increased confidence in validation

This migration transforms AVAAD from a brittle bash framework into a bulletproof Python system that non-technical users can trust.
