"""
Demonstration that the patched SCOPE runtime actually eliminates
candidates via real, executable falsifiers -- using the same
Bureaucratic Metric Gaming scenario from the original example,
but with `check` callables attached instead of description-only
falsifiers.
"""
from scope_runtime import (
    ScopeRun, ResolutionLevel, CandidateStructure, Constraint,
    Falsifier, ScopeRuntime
)

candidates = [
    CandidateStructure(
        name="KPI-Driven Review",
        description="Traditional KPI-based performance evaluation",
        key_assumptions=[
            "High KPI scores indicate operational success",
            "Metrics are objective and gaming-resistant",
            "Incentive coupling to KPIs drives improvement",
            "Reviewers interpret metrics correctly"
        ],
        dependencies=["institutional_trust", "metric_stability"],
        operational_distinctions=["Clear quantitative benchmarks", "Automated scoring possible"]
    ),
    CandidateStructure(
        name="Hybrid Review System",
        description="Metrics + adversarial audit",
        key_assumptions=[
            "Metrics + adversarial pressure reduces gaming",
            "Audit expertise is available",
            "Auditors can identify operational failures",
            "Hybrid overhead remains manageable"
        ],
        dependencies=["expert_availability", "institutional_trust"],
        operational_distinctions=["Operational failures detected despite metric scores"]
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
        operational_distinctions=["Independent evaluators reduce bias"]
    )
]

# --- REAL, EXECUTABLE FALSIFIER CHECKS ---
# Each check inspects the candidate's own declared assumptions/distinctions
# (a stand-in for real data in a demo) and returns True if the candidate's
# core claim is contradicted -- i.e. the falsifier actually fires.

def gaming_resistance_check(candidate: CandidateStructure) -> bool:
    """Triggers if a candidate CLAIMS gaming-resistant metrics but has no
    adversarial/audit mechanism among its operational distinctions --
    i.e. the claim is asserted, not backed by any actual mechanism."""
    claims_resistance = any("gaming-resistant" in a.lower() for a in candidate.key_assumptions)
    has_adversarial_mechanism = any(
        "audit" in d.lower() or "falsifier" in d.lower() or "adversarial" in d.lower()
        for d in candidate.operational_distinctions
    )
    return claims_resistance and not has_adversarial_mechanism


def unbounded_overhead_check(candidate: CandidateStructure) -> bool:
    """Triggers if a candidate depends on coordination/expert overhead
    without declaring any bound on that overhead."""
    mentions_overhead_dependency = any(
        "overhead" in a.lower() or "coordination" in a.lower()
        for a in candidate.key_assumptions
    )
    declares_bound = any("bounded" in a.lower() for a in candidate.key_assumptions)
    return mentions_overhead_dependency and not declares_bound


falsifiers = [
    Falsifier(
        name="High Metrics with Poor Operations",
        description="Candidate claims metrics are gaming-resistant with no audit mechanism to back it",
        test_method="gaming_resistance_check(candidate)",
        domain="institutional_performance",
        criticality=0.9,
        check=gaming_resistance_check,
    ),
    Falsifier(
        name="Unbounded Coordination Overhead",
        description="Candidate depends on overhead/coordination without a declared bound",
        test_method="unbounded_overhead_check(candidate)",
        domain="governance_cost",
        criticality=0.6,
        check=unbounded_overhead_check,
    ),
]

scope_run = ScopeRun(
    host_domain="Institutional performance evaluation",
    resolution_level=ResolutionLevel.OPERATIONAL,
    candidate_claim_set=candidates,
    explicit_constraints=[
        Constraint(name="Falsifier Exposure",
                   description="Gaming resistance must remain testable",
                   critical=True, verifiable=True)
    ],
    dependency_structure={},
    domain_indexed_falsifiers=falsifiers,
    operational_discrimination_metric="survival under falsifier pressure",
    governance_recursion_cost=0.35,
    scoring_procedure="executable falsifier checks",
    termination_trigger="RWR/DRE drift or full convergence",
    decommissioning_condition="all falsifiers exhausted with survivors remaining",
)

runtime = ScopeRuntime(scope_run)
result = runtime.execute()

print("=" * 70)
print("PATCHED SCOPE RUN -- falsifiers actually wired to elimination")
print("=" * 70)
for line in result.execution_log:
    print(line)

print("\nFINAL REPORT")
report = runtime.generate_report()
print(f"Candidates: {report['candidates']['total']} -> "
      f"{report['candidates']['survived']} "
      f"(survival rate {report['candidates']['survival_rate']:.1%})")
print(f"Iterations run: {result.iteration_count}")
print(f"Eliminative work total: {report['dre_results']['final_eliminative_work']:.3f}")
print(f"Drift detected: {report['dre_results']['drift_detected']}")
print("\nSurvivors:")
for s in report["surviving_structures"]:
    print(f"  - {s['name']}")
print("\nEliminated:")
for c in scope_run.candidate_claim_set:
    if c.eliminated:
        print(f"  - {c.name}: {c.elimination_reason}")
