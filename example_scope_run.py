"""
Worked Example: Bureaucratic Metric Gaming
Based on the SCOPE README Section 22
"""

import json
from datetime import datetime
from scope_runtime import (
    ScopeRun, ResolutionLevel, CandidateStructure, Constraint,
    Falsifier, ScopeRuntime, EliminationTrace, EliminationCategory
)
from scope_utils import (
    DependencyAnalyzer, ConstraintValidator, FalsifierAnalyzer,
    EliminationTracer, GovernanceCostAnalyzer, DecommissioningPlanner
)


def create_bureaucratic_metric_gaming_run() -> ScopeRun:
    """
    Host Domain: Institutional performance evaluation
    
    Candidate Structures:
    1. KPI-driven review system
    2. Hybrid review system (metrics + adversarial audit)
    3. Distributed peer-evaluation model
    
    Constraints:
    - Accountability must remain measurable
    - Review overhead must remain affordable
    - Metrics must retain falsifier exposure
    - Governance complexity must not exceed correction yield
    """
    
    # Define candidates
    candidates = [
        CandidateStructure(
            name="KPI-Driven Review",
            description="Traditional Key Performance Indicator-based performance evaluation",
            key_assumptions=[
                "High KPI scores indicate operational success",
                "Metrics are objective and gaming-resistant",
                "Incentive coupling to KPIs drives improvement",
                "Reviewers interpret metrics correctly"
            ],
            dependencies=["institutional_trust", "metric_stability"],
            operational_distinctions=[
                "Clear quantitative benchmarks",
                "Automated scoring possible"
            ]
        ),
        CandidateStructure(
            name="Hybrid Review System",
            description="Combination of limited metrics and adversarial audit",
            key_assumptions=[
                "Metrics + adversarial pressure reduces gaming",
                "Audit expertise is available",
                "Auditors can identify operational failures",
                "Hybrid overhead remains manageable"
            ],
            dependencies=["expert_availability", "institutional_trust"],
            operational_distinctions=[
                "Operational failures detected despite metric scores",
                "Falsifier resistance measured directly"
            ]
        ),
        CandidateStructure(
            name="Distributed Peer Evaluation",
            description="Decentralized evaluation by peer departments",
            key_assumptions=[
                "Peers have adequate operational visibility",
                "Peer incentives align with organizational health",
                "Distributed review prevents institutional capture",
                "Coordination overhead remains bounded"
            ],
            dependencies=["organizational_culture", "peer_incentive_alignment"],
            operational_distinctions=[
                "Independent evaluators reduce bias",
                "Multiple failure modes visible simultaneously"
            ]
        )
    ]
    
    # Define constraints
    constraints = [
        Constraint(
            name="Accountability Measurability",
            description="Accountability must remain measurable and externally verifiable",
            critical=True,
            verifiable=True
        ),
        Constraint(
            name="Review Affordability",
            description="Review overhead must remain affordable relative to organizational size",
            critical=True,
            verifiable=True
        ),
        Constraint(
            name="Falsifier Exposure",
            description="Metrics must retain falsifier exposure; gaming resistance must remain testable",
            critical=True,
            verifiable=True
        ),
        Constraint(
            name="Governance Proportionality",
            description="Governance complexity must not exceed operational correction yield",
            critical=True,
            verifiable=True
        ),
        Constraint(
            name="Institutional Survivorship",
            description="System must remain compatible with existing institutional structures",
            critical=False,
            verifiable=False
        )
    ]
    
    # Define dependency structure
    dependency_structure = {
        "institutional_trust": ["metric_stability", "peer_incentive_alignment"],
        "metric_stability": ["review_process"],
        "expert_availability": ["audit_quality"],
        "organizational_culture": ["peer_incentive_alignment"],
        "peer_incentive_alignment": ["operational_correction"]
    }
    
    # Define falsifiers
    falsifiers = [
        Falsifier(
            name="High Metrics with Poor Operations",
            description="High metric scores paired with poor operational outcomes",
            test_method="Compare department KPI scores to failure rate; correlate inversely",
            domain="institutional_performance",
            criticality=0.9
        ),
        Falsifier(
            name="Administrative Growth Without Improvement",
            description="Administrative staffing grows without corresponding performance improvement",
            test_method="Track overhead vs. operational metrics over time; compare slopes",
            domain="governance_cost",
            criticality=0.8
        ),
        Falsifier(
            name="Audit Compliance Gaming",
            description="Departments pass audits repeatedly while experiencing recurring operational failures",
            test_method="Track audit passes vs. failure frequency; measure contradiction",
            domain="audit_integrity",
            criticality=0.85
        ),
        Falsifier(
            name="Negative Control Improvement",
            description="Negative-control departments show same improvement as treatment departments from reporting intensity alone",
            test_method="Run control experiment; measure improvement without intervention",
            domain="causal_integrity",
            criticality=0.95
        ),
        Falsifier(
            name="Distributed Review Consensus Failure",
            description="Peers consistently disagree on performance assessment",
            test_method="Measure inter-rater agreement coefficient; threshold < 0.6",
            domain="peer_reliability",
            criticality=0.75
        )
    ]
    
    # Create SCOPE run
    run = ScopeRun(
        host_domain="Institutional Performance Evaluation",
        resolution_level=ResolutionLevel.TECHNICAL,
        candidate_claim_set=candidates,
        explicit_constraints=constraints,
        dependency_structure=dependency_structure,
        domain_indexed_falsifiers=falsifiers,
        operational_discrimination_metric="Reduction in false-positive performance classifications; increased detection of operational failure; reduced governance overhead per review cycle",
        governance_recursion_cost=0.35,
        scoring_procedure="Track three elimination categories: epistemic (false-positive reduction), operational (failure detection), governance (overhead reduction). Sum normalized scores. Threshold > 0.5 for admissibility.",
        termination_trigger="No added oversight layer improves fault detection or falsifier visibility for two consecutive review cycles",
        decommissioning_condition="If recursive oversight resumes without measurable operational gain, SCOPE intervention terminates and rollback becomes mandatory"
    )
    
    return run


def run_analysis():
    """Execute full SCOPE run with analysis"""
    
    print("\n" + "="*80)
    print("SCOPE RUNTIME: BUREAUCRATIC METRIC GAMING CASE STUDY")
    print("="*80 + "\n")
    
    # Create the run specification
    scope_run = create_bureaucratic_metric_gaming_run()
    
    # Pre-execution analysis
    print("PRE-EXECUTION ANALYSIS")
    print("-" * 80)
    
    # Dependency analysis
    print("\n1. DEPENDENCY STRUCTURE ANALYSIS")
    cycles = DependencyAnalyzer.find_cycles(scope_run.dependency_structure)
    print(f"   Cycles found: {len(cycles)}")
    if cycles:
        for cycle in cycles:
            print(f"     - {' → '.join(cycle)}")
    
    critical_path = DependencyAnalyzer.find_critical_path(scope_run.dependency_structure)
    print(f"   Critical path ({len(critical_path)} nodes): {' → '.join(critical_path)}")
    
    assumption_analysis = DependencyAnalyzer.analyze_assumption_density(scope_run.candidate_claim_set)
    print(f"   Total assumptions: {assumption_analysis['total_assumptions']}")
    print(f"   Avg per candidate: {assumption_analysis['average_per_candidate']:.1f}")
    if assumption_analysis['density_concern']:
        print(f"   ⚠ High-density candidates: {', '.join(assumption_analysis['candidates_high_density'])}")
    
    # Constraint analysis
    print("\n2. CONSTRAINT COVERAGE ANALYSIS")
    domains = list(set([f.domain for f in scope_run.domain_indexed_falsifiers]))
    coverage = ConstraintValidator.check_constraint_coverage(scope_run.explicit_constraints, domains)
    print(f"   Domain coverage: {coverage['coverage']:.1%}")
    print(f"   Constraints per domain: {coverage['constraints_per_domain']}")
    
    criticality = ConstraintValidator.validate_criticality_distribution(scope_run.explicit_constraints)
    print(f"   Critical constraints: {criticality['critical_constraints']}/{criticality['total_constraints']}")
    
    conflicts = ConstraintValidator.check_constraint_conflict(scope_run.explicit_constraints)
    if conflicts:
        print(f"   ⚠ Potential conflicts: {len(conflicts)}")
    
    # Falsifier analysis
    print("\n3. FALSIFIER COVERAGE ANALYSIS")
    falsifier_coverage = FalsifierAnalyzer.analyze_coverage(scope_run.domain_indexed_falsifiers, domains)
    print(f"   Domains covered: {falsifier_coverage['domains_covered']}/{falsifier_coverage['total_domains']}")
    print(f"   Falsifiers per domain: {falsifier_coverage['falsifiers_per_domain']}")
    
    criticality_dist = FalsifierAnalyzer.criticality_distribution(scope_run.domain_indexed_falsifiers)
    print(f"   High criticality: {criticality_dist['high_criticality_count']}")
    print(f"   Medium criticality: {criticality_dist['medium_criticality_count']}")
    print(f"   Low criticality: {criticality_dist['low_criticality_count']}")
    print(f"   Average criticality: {criticality_dist['average_criticality']:.2f}")
    
    redundancy = FalsifierAnalyzer.detect_redundancy(scope_run.domain_indexed_falsifiers)
    if redundancy:
        print(f"   ⚠ Potential redundancy: {len(redundancy)} pairs")
    
    # Governance analysis
    print("\n4. GOVERNANCE COST ANALYSIS")
    overhead = GovernanceCostAnalyzer.estimate_recursion_overhead(scope_run)
    print(f"   Estimated overhead: {overhead['total_estimated_overhead']:.2%}")
    print(f"   Overhead factors: {overhead['overhead_factors']}")
    
    # EXECUTE SCOPE RUNTIME
    print("\n" + "="*80)
    print("EXECUTING SCOPE PROTOCOL")
    print("="*80)
    
    runtime = ScopeRuntime(scope_run)
    result = runtime.execute()
    
    # Post-execution analysis
    print("\n" + "="*80)
    print("POST-EXECUTION ANALYSIS")
    print("="*80)
    
    # Generate report
    print("\nGENERATING EXECUTION REPORT")
    report = runtime.generate_report()
    
    print(f"\nCandidates: {report['candidates']['total']} → {report['candidates']['survived']} (survival rate: {report['candidates']['survival_rate']:.1%})")
    print(f"Falsifiers applied: {report['falsifiers']['total_applied']}")
    print(f"DRE Results:")
    print(f"  Δ H: {report['dre_results']['final_delta_h']:.3f}")
    print(f"  Drift detected: {report['dre_results']['drift_detected']}")
    print(f"  Eliminative work: {report['dre_results']['final_eliminative_work']:.3f}")
    
    if report['failure_modes']:
        print(f"\nFailure modes detected: {len(report['failure_modes'])}")
        for mode in report['failure_modes']:
            print(f"  - {mode}")
    
    print(f"\nSurviving structures:")
    for survivor in report['surviving_structures']:
        print(f"  - {survivor['name']} ({survivor['assumptions_count']} assumptions)")
    
    # Elimination analysis
    print("\n5. ELIMINATION EFFICIENCY ANALYSIS")
    elim_efficiency = EliminationTracer.analyze_elimination_efficiency(result.elimination_traces)
    print(f"   Total elimination traces: {elim_efficiency['total_elimination_traces']}")
    print(f"   Governance cost reduction: {elim_efficiency['total_governance_cost_reduction']:.2%}")
    print(f"   Average efficiency: {elim_efficiency['average_efficiency']:.2%}")
    
    # Decommissioning assessment
    print("\n6. DECOMMISSIONING READINESS")
    is_drift = report['dre_results']['drift_detected']
    readiness = DecommissioningPlanner.readiness_assessment(
        result, 
        is_drift, 
        result.detected_failure_modes
    )
    print(f"   Ready to decommission: {readiness['ready_to_decommission']}")
    print(f"   Recommendation: {readiness['recommendation']}")
    
    if readiness['ready_to_decommission']:
        decom_log = DecommissioningPlanner.decommissioning_log(result)
        print(f"   Decommissioning log prepared")
    
    # Export full report
    report_filename = f"scope_run_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n✓ Full report exported to: {report_filename}")
    
    # Export execution log
    log_filename = f"scope_execution_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_filename, 'w') as f:
        f.write("\n".join(result.execution_log))
    print(f"✓ Execution log exported to: {log_filename}")
    
    print("\n" + "="*80)
    print("SCOPE EXECUTION COMPLETE")
    print("="*80 + "\n")
    
    return result, report


if __name__ == "__main__":
    result, report = run_analysis()
