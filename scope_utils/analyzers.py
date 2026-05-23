"""SCOPE analysis utilities."""

from typing import Dict, List, Tuple, Any
from scope_runtime.models import CandidateStructure, Constraint, Falsifier, ScopeRun


class DependencyAnalyzer:
    """Analyze dependency structures."""
    
    @staticmethod
    def find_cycles(dependency_structure: Dict[str, List[str]]) -> List[List[str]]:
        """Find circular dependencies."""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in dependency_structure.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack and neighbor in path:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            
            rec_stack.discard(node)
        
        for node in dependency_structure:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    @staticmethod
    def find_critical_path(dependency_structure: Dict[str, List[str]]) -> List[str]:
        """Find longest dependency chain."""
        def max_depth(node: str, visited: set) -> Tuple[int, List[str]]:
            if node in visited:
                return 0, []
            visited.add(node)
            
            max_len = 0
            max_path = [node]
            
            for neighbor in dependency_structure.get(node, []):
                length, path = max_depth(neighbor, visited.copy())
                if length + 1 > max_len:
                    max_len = length + 1
                    max_path = [node] + path
            
            return max_len, max_path
        
        longest_path = []
        for node in dependency_structure:
            _, path = max_depth(node, set())
            if len(path) > len(longest_path):
                longest_path = path
        
        return longest_path
    
    @staticmethod
    def analyze_assumption_density(candidates: List[CandidateStructure]) -> Dict[str, Any]:
        """Analyze assumption density across candidates."""
        total_assumptions = sum(c.assumption_count() for c in candidates)
        high_density = [c.name for c in candidates if c.assumption_count() > 4]
        
        return {
            "total_assumptions": total_assumptions,
            "average_per_candidate": total_assumptions / len(candidates) if candidates else 0,
            "candidates_high_density": high_density,
            "density_concern": len(high_density) > 0,
        }


class ConstraintValidator:
    """Validate constraint coverage and conflicts."""
    
    @staticmethod
    def check_constraint_coverage(constraints: List[Constraint], domains: List[str]) -> Dict[str, Any]:
        """Check constraint coverage across domains."""
        covered_domains = set(c.domain for c in constraints if c.domain)
        domain_set = set(domains)
        coverage = len(covered_domains & domain_set) / len(domain_set) if domain_set else 0
        
        constraints_per_domain = {}
        for domain in domains:
            constraints_per_domain[domain] = sum(1 for c in constraints if c.domain == domain)
        
        return {
            "coverage": coverage,
            "constraints_per_domain": constraints_per_domain,
        }
    
    @staticmethod
    def validate_criticality_distribution(constraints: List[Constraint]) -> Dict[str, int]:
        """Check distribution of critical vs non-critical constraints."""
        critical = sum(1 for c in constraints if c.critical)
        return {
            "critical_constraints": critical,
            "total_constraints": len(constraints),
        }
    
    @staticmethod
    def check_constraint_conflict(constraints: List[Constraint]) -> List[Tuple[str, str]]:
        """Detect potential constraint conflicts."""
        conflicts = []
        # Simplified: would need domain-specific logic for real conflict detection
        return conflicts


class FalsifierAnalyzer:
    """Analyze falsifier coverage and redundancy."""
    
    @staticmethod
    def analyze_coverage(falsifiers: List[Falsifier], domains: List[str]) -> Dict[str, Any]:
        """Analyze falsifier coverage across domains."""
        falsifiers_per_domain = {}
        for domain in domains:
            falsifiers_per_domain[domain] = sum(1 for f in falsifiers if f.domain == domain)
        
        covered = sum(1 for count in falsifiers_per_domain.values() if count > 0)
        
        return {
            "domains_covered": covered,
            "total_domains": len(domains),
            "falsifiers_per_domain": falsifiers_per_domain,
        }
    
    @staticmethod
    def criticality_distribution(falsifiers: List[Falsifier]) -> Dict[str, Any]:
        """Analyze criticality distribution."""
        high = sum(1 for f in falsifiers if f.criticality >= 0.8)
        medium = sum(1 for f in falsifiers if 0.5 <= f.criticality < 0.8)
        low = sum(1 for f in falsifiers if f.criticality < 0.5)
        avg = sum(f.criticality for f in falsifiers) / len(falsifiers) if falsifiers else 0
        
        return {
            "high_criticality_count": high,
            "medium_criticality_count": medium,
            "low_criticality_count": low,
            "average_criticality": avg,
        }
    
    @staticmethod
    def detect_redundancy(falsifiers: List[Falsifier]) -> List[Tuple[int, int]]:
        """Detect redundant falsifiers."""
        redundant_pairs = []
        # Simplified: would need similarity metrics for real redundancy detection
        return redundant_pairs


class GovernanceCostAnalyzer:
    """Analyze governance and recursion costs."""
    
    @staticmethod
    def estimate_recursion_overhead(scope_run: ScopeRun) -> Dict[str, Any]:
        """Estimate overhead from recursion."""
        total_constraints = scope_run.total_constraints()
        total_falsifiers = scope_run.total_falsifiers()
        total_candidates = scope_run.total_candidates()
        
        # Simple heuristic
        overhead = scope_run.governance_recursion_cost * (
            (total_constraints + total_falsifiers) / max(1, total_candidates)
        )
        
        return {
            "total_estimated_overhead": min(overhead, 1.0),
            "overhead_factors": {
                "governance_cost_coefficient": scope_run.governance_recursion_cost,
                "constraints_per_candidate": total_constraints / total_candidates,
                "falsifiers_per_candidate": total_falsifiers / total_candidates,
            },
        }
