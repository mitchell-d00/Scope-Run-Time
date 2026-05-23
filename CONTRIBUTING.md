# Contributing to SCOPE Runtime

## Development Principles

This project implements a constraint-first, recursively-admissible framework. Contributions should follow these principles:

### 1. **Constraint-First Design**
- All new features must declare explicit operational constraints
- Constraints should be verifiable and externally testable
- No unconstrained recursion

### 2. **Eliminative Work**
- New code should purchase measurable eliminative work
- Each change should reduce ambiguity, improve operational discrimination, or reduce governance overhead
- Visible pruning without measurable yield is not accepted

### 3. **Evaluator Transparency**
- Design choices and trade-offs must be documented
- Hidden discretion is treated as governance drift
- Rejected alternatives should be recorded with rationale

## Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/mitchell-d00/Scope-Run-Time
cd Scope-Run-Time

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[pytorch]"

# Install development dependencies
pip install -r requirements.txt
```

## Code Standards

### Type Hints
All functions must include type hints:
```python
def check_admissibility(self, delta_h: float, falsifiers: int) -> tuple[bool, str]:
    """Check recursive admissibility."""
    pass
```

### Documentation
Docstrings follow Google style:
```python
def calculate_overhead(scope_run: ScopeRun) -> float:
    """Calculate governance overhead.
    
    Args:
        scope_run: SCOPE run specification.
    
    Returns:
        Overhead coefficient (0.0 to 1.0).
    
    Raises:
        ValueError: If constraints are unsatisfiable.
    """
    pass
```

### Testing
```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scope_runtime --cov=scope_utils

# Check code quality
flake8 scope_runtime scope_utils
mypy scope_runtime scope_utils
black scope_runtime scope_utils
```

## Pull Request Process

1. **Reference Prior Work**
   - Cite relevant papers from RESEARCH_REFERENCES.md
   - Link to README sections that apply

2. **Document Constraints**
   - List explicit constraints on the change
   - Declare any new dependencies or recursion layers

3. **Measure Eliminative Work**
   - Show reduced candidate multiplicity or improved discrimination
   - Provide metrics or test results
   - Include governance cost analysis

4. **Evaluator Transparency**
   - Document design choices
   - Record rejected approaches
   - Expose any remaining ambiguity

5. **Tests & Validation**
   - All new code must have tests
   - Tests must verify constraint satisfaction
   - Include adversarial test cases

## Core Modules

### `scope_runtime/models.py`
Data models for SCOPE protocol. Extends with caution—constraint violations here propagate.

### `scope_runtime/dre.py`
Dynamic Recursive Entropy calculator. Based on McPhetridge (2026). Changes require theoretical justification.

### `scope_runtime/runtime.py`
Execution engine. Protocol order is critical: Generate → Constrain → Pressure → Prune → Measure.

### `scope_utils/`
Analysis utilities. Should remain modular and pluggable.

## Reporting Issues

Use constraint-first language:
- What constraint is violated?
- What eliminative work is missing?
- What failure mode is this instance of?
- Is this a drift detection problem?

## Research Grounding

See RESEARCH_REFERENCES.md for connections between implementation and peer-reviewed theory.
