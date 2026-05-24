# SCOPE Runtime Test Suite Documentation

## Overview

This document describes the comprehensive test suite for the SCOPE Runtime project. The test suite is organized into multiple categories and can be executed in various configurations.

## Test Structure

```
tests/
├── test_scope_core.py       # Core SCOPE runtime classes and logic
├── test_scope_utils.py       # Utility functions and analyzers
├── test_integration.py       # End-to-end workflow tests
├── test_markers.py           # Tests organized by pytest markers
├── conftest.py              # Pytest configuration and fixtures
└── README.md                # This file
```

## Test Categories

### Core Tests (`test_scope_core.py`)

Tests for fundamental SCOPE components:

- **ResolutionLevel**: Enum values and hierarchy
- **CandidateStructure**: Creation, assumptions, dependencies
- **Constraint**: Critical/non-critical constraints
- **Falsifier**: Criticality levels, domains
- **ScopeRun**: Full specification creation
- **ScopeRuntime**: Execution and report generation
- **Admissibility Conditions**: Drift detection, constraint satisfaction

### Utility Tests (`test_scope_utils.py`)

Tests for utility modules:

- **DependencyAnalyzer**: Cycle detection, critical path analysis
- **ConstraintValidator**: Coverage validation, conflict detection
- **FalsifierAnalyzer**: Coverage analysis, redundancy detection
- **EliminationTracer**: Efficiency tracking
- **GovernanceCostAnalyzer**: Overhead estimation
- **DecommissioningPlanner**: Decommissioning readiness assessment

### Integration Tests (`test_integration.py`)

End-to-end workflow tests:

- **Bureaucratic Metric Gaming**: Complete case study workflow
- **Multi-Candidate Scenarios**: Complex candidate interactions
- **Edge Cases**: Empty sets, single candidates, no falsifiers
- **Resolution Levels**: Different resolution levels
- **Dependency Complexity**: Cyclic/acyclic structures
- **Report Generation**: Required report structure

### Marked Tests (`test_markers.py`)

Tests organized with pytest markers for flexible execution:

- **@pytest.mark.unit**: Fast, isolated unit tests
- **@pytest.mark.integration**: Workflow integration tests
- **@pytest.mark.slow**: Long-running tests (optional)

## Fixtures

Available fixtures in `conftest.py`:

- `sample_dependencies`: Standard dependency structure
- `acyclic_dependencies`: Acyclic dependency graph
- `cyclic_dependencies`: Cyclic dependency graph
- `high_density_assumptions`: Candidates with many assumptions
- `critical_constraints`: Critical constraint set
- `high_criticality_falsifiers`: High-criticality falsifier set
- `mixed_resolution_candidates`: Candidates at different levels
- `empty_structures`: Empty test structures
- `minimal_structures`: Minimal test structures

## Running Tests

### Linux/Mac

```bash
# Run all tests
./run_tests.sh all

# Run unit tests only
./run_tests.sh unit

# Run integration tests
./run_tests.sh integration

# Run fast tests (skip slow)
./run_tests.sh fast

# Run with coverage report
./run_tests.sh coverage

# Show available markers
./run_tests.sh markers

# Show help
./run_tests.sh help
```

### Windows

```cmd
# Run all tests
run_tests.bat all

# Run unit tests only
run_tests.bat unit

# Run integration tests
run_tests.bat integration

# Run fast tests (skip slow)
run_tests.bat fast

# Run with coverage report
run_tests.bat coverage

# Show available markers
run_tests.bat markers

# Show help
run_tests.bat help
```

### Manual pytest Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scope_core.py -v

# Run specific test class
pytest tests/test_scope_core.py::TestCandidateStructure -v

# Run specific test
pytest tests/test_scope_core.py::TestCandidateStructure::test_candidate_creation -v

# Run unit tests only
pytest tests/ -v -m unit

# Run integration tests only
pytest tests/ -v -m integration

# Run excluding slow tests
pytest tests/ -v -m "not slow"

# Run with coverage report
pytest tests/ --cov=scope_runtime --cov=scope_utils --cov-report=html -v

# Run with parallel execution (requires pytest-xdist)
pytest tests/ -v -n auto

# Run with verbose output
pytest tests/ -vv

# Run with detailed failure information
pytest tests/ -vv --tb=long

# Stop on first failure
pytest tests/ -v -x

# Stop after N failures
pytest tests/ -v --maxfail=3

# Run tests matching pattern
pytest tests/ -v -k "bureaucratic"
```

## Coverage Report

The test suite generates coverage reports showing code coverage:

```bash
./run_tests.sh coverage
```

This generates:
- Terminal report with line coverage details
- HTML report in `htmlcov/index.html`

Minimum coverage targets:
- Core modules: 85%+
- Utility modules: 80%+
- Overall: 80%+

## Test Organization by Purpose

### Unit Tests (Fast)

These tests verify individual components in isolation:

- Component initialization and configuration
- Individual function behavior
- Error handling
- Enum values

**Run with**: `./run_tests.sh unit`

### Integration Tests (Medium)

These tests verify workflows and interactions:

- Complete SCOPE runs
- Multi-component interactions
- Report generation
- Case study execution

**Run with**: `./run_tests.sh integration`

### Slow Tests (Optional)

These tests run computationally intensive operations:

- Large dependency graph analysis
- High-complexity SCOPE runs
- Exhaustive cycle detection

**Run with**: `pytest tests/ -v -m slow`

## Continuous Integration

GitHub Actions workflow (`.github/workflows/test.yml`) runs:

1. **Test Matrix**:
   - Python 3.8, 3.9, 3.10, 3.11
   - Ubuntu, macOS, Windows

2. **Stages**:
   - Unit tests
   - Integration tests
   - Coverage report generation
   - Linting (Black, Flake8, MyPy)

3. **Upload**:
   - Coverage reports to Codecov

## Test Maintenance

### Adding New Tests

1. Choose appropriate test file or create new `test_*.py`
2. Use descriptive test names: `test_<component>_<behavior>`
3. Add appropriate markers: `@pytest.mark.unit` or `@pytest.mark.integration`
4. Use fixtures from `conftest.py` when applicable
5. Add docstrings explaining what is being tested

### Updating Existing Tests

1. Keep test names consistent with functionality
2. Update docstrings if behavior changes
3. Ensure tests still pass with changes
4. Update coverage targets if needed

### Debugging Failed Tests

```bash
# Run failed test with verbose output
pytest tests/test_file.py::TestClass::test_method -vv

# Run with print statements displayed
pytest tests/test_file.py::TestClass::test_method -vv -s

# Run with detailed traceback
pytest tests/test_file.py::TestClass::test_method -vv --tb=long

# Run with debugger on failure
pytest tests/test_file.py::TestClass::test_method -vv --pdb
```

## Code Quality Standards

Tests should:

- Use clear, descriptive names
- Include docstrings
- Test one concept per test
- Use fixtures for common setup
- Include edge cases and error conditions
- Be maintainable and readable
- Run in isolation without side effects

## Performance Benchmarks

Expected test execution times:

- Unit tests: < 5 seconds
- Integration tests: < 10 seconds
- Coverage generation: < 15 seconds
- Full suite: < 30 seconds

## Dependencies

Test dependencies are listed in `requirements-test.txt`:

```
pytest>=6.2.5
pytest-cov>=2.12.1
pytest-xdist>=2.3.0
black>=21.9b0
flake8>=3.9.2
mypy>=0.910
```

Install with:

```bash
pip install -r requirements-test.txt
```

## Troubleshooting

### pytest not found

```bash
pip install pytest pytest-cov
```

### ImportError in tests

Ensure SCOPE modules are importable:

```bash
# From project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

### Coverage report not generated

Ensure dependencies are installed:

```bash
pip install pytest-cov
```

### Tests pass locally but fail in CI

Check Python version matches CI configuration in `.github/workflows/test.yml`

## Contributing

When contributing:

1. Write tests for new features
2. Ensure all tests pass: `./run_tests.sh all`
3. Generate coverage report: `./run_tests.sh coverage`
4. Verify coverage targets are met
5. Update this documentation if adding new test categories
