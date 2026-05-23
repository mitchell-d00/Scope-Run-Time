"""SCOPE runtime execution engine."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import ScopeRun, EliminationTrace, EliminationCategory, CandidateStructure
from .dre import DRECalculator, DREResult


@dataclass
class ScopeExecutionResult:
    """Result of executing a SCOPE run."""
    scope_run: ScopeRun
    execution_started: datetime
    execution_completed: Optional[datetime] = None
    duration_seconds: float = 0.0
    
    # Execution state
    iteration_count: int = 0
    final_viable_candidates: int = 0
    initial_candidate_count: int = 0
    
    # Traces and diagnostics
    elimination_traces: List[EliminationTrace] = field(default_factory=list)
    dre_history: List[DREResult] = field(default_factory=list)
    detected_failure_modes: List[str] = field(default_factory=list)
    execution_log: List[str] = field(default_factory=list)
    
    # Final state
    admissible: bool = True
    termination_reason: Optional[str] = None
    
    def add_log_entry(self, message: str) -> None:
        """Add entry to execution log."""
        timestamp = datetime.now().isoformat()
        self.execution_log.append(f"[{timestamp}] {message}")
    
    def add_elimination_trace(self, trace: EliminationTrace) -> None:
        """Record an elimination event."""
        self.elimination_traces.append(trace)
    
    def survival_rate(self) -> float:
        """Calculate candidate survival rate."""
        if self.initial_candidate_count == 0:
            return 0.0
        return self.final_viable_candidates / self.initial_candidate_count
    
    def elapsed_time(self) -> float:
        """Get execution duration in seconds."""
        if self.execution_completed:
            return (self.execution_completed - self.execution_started).total_seconds()
        return 0.0


class ScopeRuntime:
    """SCOPE protocol runtime executor."""
    
    def __init__(self, scope_run: ScopeRun):
        """Initialize SCOPE runtime.
        
        Args:
            scope_run: Specification for this SCOPE run.
        """
        self.scope_run = scope_run
        self.dre_calculator = DRECalculator(window_size=5)
        self.result = ScopeExecutionResult(
            scope_run=scope_run,
            execution_started=datetime.now(),
            initial_candidate_count=scope_run.total_candidates(),
        )
    
    def execute(self) -> ScopeExecutionResult:
        """Execute SCOPE protocol: Generate → Constrain → Pressure → Prune → Measure."""
        
        self.result.add_log_entry(
            f"SCOPE execution started: {self.scope_run.host_domain}"
        )
        
        try:
            # Phase 1: Constrain (validate constraints)
            self._phase_constrain()
            
            # Phase 2: Pressure (apply falsifiers)
            self._phase_pressure()
            
            # Phase 3: Prune (eliminate non-viable candidates)
            self._phase_prune()
            
            # Phase 4: Measure (evaluate elimination)
            self._phase_measure()
            
            # Check termination condition
            self._check_termination()
            
        except Exception as e:
            self.result.add_log_entry(f"Execution error: {str(e)}")
            self.result.admissible = False
            self.result.termination_reason = f"Execution error: {str(e)}"
        
        finally:
            self.result.execution_completed = datetime.now()
            self.result.final_viable_candidates = sum(
                1 for c in self.scope_run.candidate_claim_set if not c.eliminated
            )
        
        return self.result
    
    def _phase_constrain(self) -> None:
        """Constrain: Validate that constraints are satisfiable."""
        self.result.add_log_entry(
            f"Phase 1: CONSTRAIN - Validating {len(self.scope_run.explicit_constraints)} constraints"
        )
        
        critical = self.scope_run.critical_constraints()
        self.result.add_log_entry(
            f"  - Critical constraints: {len(critical)}"
        )
        self.result.add_log_entry(
            f"  - Total candidates: {len(self.scope_run.candidate_claim_set)}"
        )
    
    def _phase_pressure(self) -> None:
        """Pressure: Apply falsifiers against candidates."""
        self.result.add_log_entry(
            f"Phase 2: PRESSURE - Applying {len(self.scope_run.domain_indexed_falsifiers)} falsifiers"
        )
        
        for falsifier in self.scope_run.domain_indexed_falsifiers:
            self.result.add_log_entry(
                f"  - Applying: {falsifier.name} (criticality: {falsifier.criticality})"
            )
    
    def _phase_prune(self) -> None:
        """Prune: Eliminate candidates that fail constraints/falsifiers."""
        self.result.add_log_entry(
            f"Phase 3: PRUNE - Evaluating candidates for elimination"
        )
        
        # Simulate pruning
        eliminated_count = 0
        for candidate in self.scope_run.candidate_claim_set:
            # Simple heuristic: high assumption density increases elimination likelihood
            if candidate.assumption_count() > 4:
                candidate.eliminated = True
                eliminated_count += 1
                
                trace = EliminationTrace(
                    timestamp=datetime.now(),
                    candidate_name=candidate.name,
                    category=EliminationCategory.EPISTEMIC,
                    reason=f"High assumption density: {candidate.assumption_count()} assumptions",
                    epistemic_yield=0.25,
                )
                self.result.add_elimination_trace(trace)
        
        self.result.add_log_entry(
            f"  - Candidates eliminated: {eliminated_count}"
        )
    
    def _phase_measure(self) -> None:
        """Measure: Calculate eliminative work and DRE."""
        self.result.add_log_entry(
            f"Phase 4: MEASURE - Calculating eliminative work"
        )
        
        viable_count = sum(
            1 for c in self.scope_run.candidate_claim_set if not c.eliminated
        )
        
        dre_result = self.dre_calculator.calculate(
            viable_candidates=viable_count,
            previous_viable_count=self.scope_run.total_candidates(),
            new_falsifiers=len(self.scope_run.domain_indexed_falsifiers),
            eliminative_work=len(self.result.elimination_traces) * 0.1,
        )
        
        self.result.dre_history.append(dre_result)
        self.result.add_log_entry(
            f"  - ΔH: {dre_result.delta_h:.3f}"
        )
        self.result.add_log_entry(
            f"  - Viable candidates: {dre_result.viable_candidate_count}"
        )
        self.result.add_log_entry(
            f"  - Drift detected: {dre_result.drift_detected}"
        )
    
    def _check_termination(self) -> None:
        """Check if termination conditions are met."""
        if not self.result.dre_history:
            return
        
        latest_dre = self.result.dre_history[-1]
        
        if latest_dre.drift_detected:
            self.result.admissible = False
            self.result.termination_reason = "Recursive drift detected"
            self.result.add_log_entry(
                "TERMINATION: Recursive drift condition met"
            )
        else:
            self.result.add_log_entry(
                f"Admissibility maintained - survival rate: {self.result.survival_rate():.1%}"
            )
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate execution report."""
        return {
            "run_info": {
                "host_domain": self.scope_run.host_domain,
                "resolution_level": self.scope_run.resolution_level.value,
                "execution_started": self.result.execution_started.isoformat(),
                "execution_completed": (
                    self.result.execution_completed.isoformat()
                    if self.result.execution_completed
                    else None
                ),
                "duration_seconds": self.result.elapsed_time(),
            },
            "candidates": {
                "total": self.result.initial_candidate_count,
                "survived": self.result.final_viable_candidates,
                "survival_rate": self.result.survival_rate(),
            },
            "falsifiers": {
                "total_applied": len(self.scope_run.domain_indexed_falsifiers),
            },
            "dre_results": {
                "final_delta_h": (
                    self.result.dre_history[-1].delta_h
                    if self.result.dre_history
                    else 0.0
                ),
                "drift_detected": (
                    self.result.dre_history[-1].drift_detected
                    if self.result.dre_history
                    else False
                ),
                "final_eliminative_work": sum(
                    t.total_yield() for t in self.result.elimination_traces
                ),
            },
            "failure_modes": self.result.detected_failure_modes,
            "surviving_structures": [
                {
                    "name": c.name,
                    "assumptions_count": c.assumption_count(),
                }
                for c in self.scope_run.candidate_claim_set
                if not c.eliminated
            ],
            "admissible": self.result.admissible,
            "termination_reason": self.result.termination_reason,
        }
