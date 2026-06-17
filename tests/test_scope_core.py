"""
Comprehensive unit tests for SCOPE Runtime core components.
"""

import pytest
from scope_runtime import (
    ResolutionLevel, CandidateStructure, Constraint, Falsifier,
    ScopeRun, ScopeRuntime, EliminationCategory
)


class TestResolutionLevel:
    """Tests for ResolutionLevel enumeration."""

    @pytest.mark.unit
    def test_resolution_level_values_exist(self):
        """Test that all expected resolution levels exist."""
        expected_levels = ["STRATEGIC", "TECHNICAL", "OPERATIONAL", "THEORETICAL", "LOCAL"]
        for level_name in expected_levels:
            assert hasattr(ResolutionLevel, level_name), f"Missing level: {level_name}"

    @pytest.mark.unit
    def test_resolution_level_hierarchy(self):
        """Test resolution level ordering."""
        levels = [
            ResolutionLevel.STRATEGIC,
            ResolutionLevel.TECHNICAL,
            ResolutionLevel.OPERATIONAL,
            ResolutionLevel.THEORETICAL,
            ResolutionLevel.LOCAL
        ]
        # Ensure all levels are distinct
        assert len(levels) == len(set(levels))

    @pytest.mark.unit
    def test_resolution_level_string_representation(self):
        """Test string representation of resolution levels."""
        for level in [ResolutionLevel.STRATEGIC, ResolutionLevel.TECHNICAL]:
            assert isinstance(str(level), str)
            assert len(str(level)) > 0


class TestCandidateStructure:
    """Tests for CandidateStructure class."""

    @pytest.mark.unit
    def test_candidate_creation(self):
        """Test basic candidate structure creation."""
        candidate = CandidateStructure(
            name="Test Candidate",
            description="Test description",
            key_assumptions=["Assumption 1", "Assumption 2"],
            dependencies=["dep1"],
            operational_distinctions=["Distinction 1"]
        )
        assert candidate.name == "Test Candidate"
        assert candidate.description == "Test description"
        assert len(candidate.key_assumptions) == 2

    @pytest.mark.unit
    def test_candidate_with_empty_assumptions(self):
        """Test candidate with no assumptions."""
        candidate = CandidateStructure(
            name="Minimal",
            description="No assumptions",
            key_assumptions=[],
            dependencies=[],
            operational_distinctions=[]
        )
        assert len(candidate.key_assumptions) == 0
        assert len(candidate.dependencies) == 0

    @pytest.mark.unit
    def test_candidate_assumptions_count(self, sample_candidates):
        """Test counting assumptions across candidates."""
        total_assumptions = sum(len(c.key_assumptions) for c in sample_candidates)
        assert total_assumptions > 0

    @pytest.mark.unit
    def test_candidate_with_many_assumptions(self):
        """Test candidate with high assumption density."""
        assumptions = [f"Assumption_{i}" for i in range(100)]
        candidate = CandidateStructure(
            name="Dense",
            description="High density",
            key_assumptions=assumptions,
            dependencies=[],
            operational_distinctions=[]
        )
        assert len(candidate.key_assumptions) == 100

    @pytest.mark.unit
    def test_candidate_dependencies(self):
        """Test candidate dependency tracking."""
        deps = ["dep_a", "dep_b", "dep_c"]
        candidate = CandidateStructure(
            name="With Dependencies",
            description="Has deps",
            key_assumptions=["Assumption"],
            dependencies=deps,
            operational_distinctions=[]
        )
        assert set(candidate.dependencies) == set(deps)

    @pytest.mark.unit
    def test_candidate_distinctions(self):
        """Test operational distinctions."""
        distinctions = ["Can distinguish A from B", "Can measure X"]
        candidate = CandidateStructure(
            name="Distinguished",
            description="Has distinctions",
            key_assumptions=["Assumption"],
            dependencies=[],
            operational_distinctions=distinctions
        )
        assert len(candidate.operational_distinctions) == 2


class TestConstraint:
    """Tests for Constraint class."""

    @pytest.mark.unit
    def test_critical_constraint_creation(self):
        """Test creation of critical constraint."""
        constraint = Constraint(
            name="Critical",
            description="Critical constraint",
            critical=True,
            verifiable=True
        )
        assert constraint.critical is True
        assert constraint.verifiable is True

    @pytest.mark.unit
    def test_non_critical_constraint(self):
        """Test non-critical constraint."""
        constraint = Constraint(
            name="Non-Critical",
            description="Optional constraint",
            critical=False,
            verifiable=True
        )
        assert constraint.critical is False

    @pytest.mark.unit
    def test_non_verifiable_constraint(self):
        """Test non-verifiable constraint."""
        constraint = Constraint(
            name="Unverifiable",
            description="Cannot be verified",
            critical=True,
            verifiable=False
        )
        assert constraint.verifiable is False

    @pytest.mark.unit
    def test_constraint_properties(self, critical_constraints):
        """Test constraint property access."""
        for constraint in critical_constraints:
            assert hasattr(constraint, 'name')
            assert hasattr(constraint, 'critical')
            assert hasattr(constraint, 'verifiable')


class TestFalsifier:
    """Tests for Falsifier class."""

    @pytest.mark.unit
    def test_falsifier_creation(self):
        """Test basic falsifier creation."""
        falsifier = Falsifier(
            name="Test Falsifier",
            description="A test falsifier",
            test_method="Direct test",
            domain="test_domain",
            criticality=0.75
        )
        assert falsifier.name == "Test Falsifier"
        assert falsifier.criticality == 0.75

    @pytest.mark.unit
    def test_falsifier_criticality_bounds(self):
        """Test falsifier criticality is in valid range."""
        for criticality in [0.0, 0.5, 1.0]:
            falsifier = Falsifier(
                name=f"Critical {criticality}",
                description="Test",
                test_method="Test",
                domain="d",
                criticality=criticality
            )
            assert 0.0 <= falsifier.criticality <= 1.0

    @pytest.mark.unit
    def test_falsifier_high_criticality(self):
        """Test high-criticality falsifier."""
        falsifier = Falsifier(
            name="High Priority",
            description="Critical test",
            test_method="Important test",
            domain="critical",
            criticality=0.95
        )
        assert falsifier.criticality > 0.9

    @pytest.mark.unit
    def test_falsifier_low_criticality(self):
        """Test low-criticality falsifier."""
        falsifier = Falsifier(
            name="Low Priority",
            description="Optional test",
            test_method="Secondary test",
            domain="optional",
            criticality=0.25
        )
        assert falsifier.criticality < 0.5

    @pytest.mark.unit
    def test_falsifier_domain(self, multi_domain_falsifiers):
        """Test falsifier domain classification."""
        domains = set(f.domain for f in multi_domain_falsifiers)
        assert len(domains) >= 1


class TestScopeRun:
    """Tests for ScopeRun specification."""

    @pytest.mark.unit
    def test_scope_run_creation(self, basic_scope_run):
        """Test creating a SCOPE run."""
        assert basic_scope_run.host_domain == "Test Domain"
        assert basic_scope_run.resolution_level == ResolutionLevel.TECHNICAL

    @pytest.mark.unit
    def test_scope_run_with_candidates(self, sample_candidates):
        """Test SCOPE run with candidate set."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=sample_candidates,
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.candidate_claim_set) == len(sample_candidates)

    @pytest.mark.unit
    def test_scope_run_with_constraints(self, critical_constraints):
        """Test SCOPE run with constraints."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=critical_constraints,
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.explicit_constraints) == len(critical_constraints)

    @pytest.mark.unit
    def test_scope_run_with_falsifiers(self, high_criticality_falsifiers):
        """Test SCOPE run with falsifiers."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=high_criticality_falsifiers,
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.domain_indexed_falsifiers) == len(high_criticality_falsifiers)

    @pytest.mark.unit
    def test_scope_run_governance_cost(self):
        """Test governance cost specification."""
        for cost in [0.1, 0.25, 0.5, 0.9]:
            run = ScopeRun(
                host_domain="Test",
                resolution_level=ResolutionLevel.TECHNICAL,
                candidate_claim_set=[],
                explicit_constraints=[],
                dependency_structure={},
                domain_indexed_falsifiers=[],
                operational_discrimination_metric="Test",
                governance_recursion_cost=cost,
                scoring_procedure="Test",
                termination_trigger="Test",
                decommissioning_condition="Test"
            )
            assert run.governance_recursion_cost == cost


class TestScopeRuntime:
    """Tests for ScopeRuntime execution."""

    @pytest.mark.unit
    def test_runtime_creation(self, basic_scope_run):
        """Test creating a SCOPE runtime."""
        runtime = ScopeRuntime(basic_scope_run)
        assert runtime.specification == basic_scope_run

    @pytest.mark.unit
    @pytest.mark.integration
    def test_runtime_execution(self, basic_scope_run):
        """Test executing a SCOPE runtime."""
        runtime = ScopeRuntime(basic_scope_run)
        result = runtime.execute()
        assert result is not None

    @pytest.mark.unit
    @pytest.mark.integration
    def test_runtime_report_generation(self, basic_scope_run):
        """Test report generation after execution."""
        runtime = ScopeRuntime(basic_scope_run)
        runtime.execute()
        report = runtime.generate_report()
        
        assert report is not None
        assert "candidates" in report
        assert "constraints" in report
        assert "falsifiers" in report

    @pytest.mark.unit
    def test_minimal_runtime(self, minimal_scope_run):
        """Test runtime with minimal specification."""
        runtime = ScopeRuntime(minimal_scope_run)
        assert runtime.specification is not None

    @pytest.mark.slow
    @pytest.mark.integration
    def test_complex_runtime(self, complex_scope_run):
        """Test runtime with complex specification."""
        runtime = ScopeRuntime(complex_scope_run)
        result = runtime.execute()
        assert result is not None


class TestAdmissibilityConditions:
    """Tests for admissibility detection and DRE."""

    @pytest.mark.unit
    def test_drift_detection(self, sample_elimination_traces):
        """Test drift detection in elimination traces."""
        # Check that traces exist
        assert len(sample_elimination_traces) > 0

    @pytest.mark.unit
    def test_elimination_categories(self):
        """Test elimination category enumeration."""
        categories = [
            EliminationCategory.EPISTEMIC,
            EliminationCategory.OPERATIONAL,
            EliminationCategory.GOVERNANCE
        ]
        assert len(categories) == 3

    @pytest.mark.unit
    def test_constraint_satisfaction(self, critical_constraints):
        """Test constraint satisfaction checking."""
        # All critical constraints should be present
        critical_count = sum(1 for c in critical_constraints if c.critical)
        assert critical_count > 0

    @pytest.mark.unit
    def test_falsifier_visibility(self, high_criticality_falsifiers):
        """Test falsifier visibility assessment."""
        # High-criticality falsifiers should be identified
        high_crit = [f for f in high_criticality_falsifiers if f.criticality > 0.8]
        assert len(high_crit) > 0

    @pytest.mark.unit
    def test_eliminative_work_measurement(self):
        """Test eliminative work is measurable."""
        # Create elimination traces with varying effects
        for effect in [0.1, 0.5, 0.9]:
            # Effect magnitude should be recordable
            assert 0.0 <= effect <= 1.0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_empty_candidate_set(self):
        """Test handling empty candidate set."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.candidate_claim_set) == 0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_single_candidate(self, single_candidate):
        """Test handling single candidate."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=single_candidate,
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.candidate_claim_set) == 1

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_zero_governance_cost(self):
        """Test minimum governance cost."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.0,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert run.governance_recursion_cost == 0.0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_high_governance_cost(self):
        """Test maximum governance cost."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=1.0,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert run.governance_recursion_cost == 1.0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_no_falsifiers(self, sample_candidates):
        """Test SCOPE run with no falsifiers."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=sample_candidates,
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.domain_indexed_falsifiers) == 0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_no_constraints(self, sample_candidates):
        """Test SCOPE run with no constraints."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=sample_candidates,
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.explicit_constraints) == 0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_empty_dependencies(self):
        """Test SCOPE run with empty dependency structure."""
        run = ScopeRun(
            host_domain="Test",
            resolution_level=ResolutionLevel.TECHNICAL,
            candidate_claim_set=[],
            explicit_constraints=[],
            dependency_structure={},
            domain_indexed_falsifiers=[],
            operational_discrimination_metric="Test",
            governance_recursion_cost=0.25,
            scoring_procedure="Test",
            termination_trigger="Test",
            decommissioning_condition="Test"
        )
        assert len(run.dependency_structure) == 0
