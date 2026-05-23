# Mitchell D. McPhetridge Prior Work & References

This SCOPE implementation builds on the following peer-reviewed and published research:

## Core Publications

### 1. Dynamic Recursive Entropy Framework
- **"Using Recursive Entropy as a Tool to Break Recursive Entropy Loops"** (2026)
  - Published: PhilArchive, Academia.edu
  - Core contribution: DRE diagnostic for detecting recursive non-admissibility
  - Key insight: Recursive entropy loops occur when ΔH fails to contract across bounded intervals
  - Application: Forms the basis for SCOPE's admissibility detection in `dre_calculator.py`
  - URL: https://philarchive.org/rec/MCPURE
  - URL: https://www.academia.edu/165488193/Using_Recursive_Entropy_as_a_Tool_to_Break_Recursive_Entropy_Loops

### 2. Recursion Under Constraint Theory
- **"Recursion of Representation Under Constraint"** (2025+)
  - Published: PhilPapers
  - Core contribution: Formal account of how recursion behaves under enforced constraints
  - Key distinction: Self-sealing narrative inflation vs. invariant convergence
  - Application: Foundation for SCOPE's constraint validation framework
  - URL: https://philpapers.org/rec/MCPROR-2

### 3. Unified Epistemology-Ontology Framework
- **"Epistemology as Constraint Selection and Ontology as Operational Persistence: A Unified Constraint-First Account of Recursive Epistemic Systems"**
  - Core contribution: Merges epistemology and ontology under constraint-first paradigm
  - Application: Philosophical justification for constraint sovereignty in SCOPE
  - URL: PhilPeople publications profile

### 4. Dynamic Entropy Models (DREM, DEM)
- **Dynamic Recursive Entropy Model with PyTorch Implementation**
  - Published: Medium essay and technical documentation
  - Core contribution: Practical entropy calculation for recursive open systems
  - Key insight: Entropy collapse and emergent probabilities in recursive architectures
  - Application: PyTorch-backed entropy calculations for production DRE monitoring
  - URL: https://medium.com/@mitchmcphetridge/dynamic-recursive-entropy-model-drem-with-math-and-pytorch-a23bab8152f0

## Architectural Stack (From Prior Work)

The SCOPE implementation reflects the mature recursive admissibility stack developed across these publications:

```
Layer 1: Generative Systems (Candidate production)
Layer 2: Bridge Language (Host-domain transport & constraint forcing)
Layer 3: REM-Evo (Recursive Eliminative Mechanisms - Evolutionary)
Layer 4: DRE (Dynamic Recursive Entropy diagnostics)
Layer 5: Straight-Line Boundary (Termination enforcement)
Layer 6: SCOPE (Structured pruning & adjudication protocol)
```

## Key Conceptual Dependencies

### From "Using Recursive Entropy as a Tool to Break Recursive Entropy Loops"
- Non-admissibility condition: ∀k ∈ [t-n,t], ΔH_k ≥ 0 ∧ F^new_{k,d}=0 ∧ E_{k,d}=0
- Recursive drift detection as primary admissibility failure mode
- Process-level monitoring vs. system-level termination

### From "Recursion of Representation Under Constraint"
- Constraint-first epistemology as operational necessity
- Pruning via constraint leads to stable, persistent structures
- Host-domain resistance as epistemic anchoring mechanism

### From DREM Papers
- Entropy measurement in open recursive systems
- Emergent probability distributions under constraint pressure
- Practical calculation methods for ΔH estimation

## Scholar Profiles

- Google Scholar: https://scholar.google.com/citations?user=MnHx6eYAAAAJ
- PhilArchive: https://philarchive.org/rec/MCPURE
- Academia.edu: Research collection on recursive admissibility
- PhilPeople: Comprehensive publication index

## Implementation Connections

| Prior Work | SCOPE Component | Implementation File |
|---|---|---|
| DRE diagnostics | Admissibility monitoring | `dre_calculator.py` |
| Constraint theory | Constraint validation | `constraint_engine.py` |
| Elimination frameworks | Elimination tracking | `elimination_tracer.py` |
| Entropy models | DRE calculations | `dre_calculator.py` with PyTorch |
| Host-domain binding | Bridge language enforcement | `scope_runtime.py` |
| Termination discipline | Decommissioning protocols | `decommissioning_planner.py` |

## Citation Format

When referencing this SCOPE implementation, cite both the framework and the underlying research:

```
SCOPE Runtime Implementation (2026). GitHub: mitchell-d00/Scope-Run-Time
Based on: McPhetridge, M.D. (2026). Using Recursive Entropy as a Tool to Break 
Recursive Entropy Loops. PhilArchive.
```

## Future Work Integration

This repository will expand to include:
- Full implementation of DREM with PyTorch backends
- Extended constraint-first epistemology documentation
- Practical case studies linking to published examples
- Adversarial replication protocols from peer review processes
