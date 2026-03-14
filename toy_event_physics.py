"""Discrete event-network toy model.

Core ontology:
- Reality is an evolving network of events and influence relations.
- Stable objects are persistent self-maintaining patterns in that network.
- Space is inferred from influence neighborhoods and signal delays.
- Duration is local update count along a pattern's history.
- Measurement is durable record formation, not conscious observation.

Toy primitives:
- Event e: a local change.
- Link e -> e': an allowed influence relation.
- delta(e,e'): local delay.
- k(e,e'): local compatibility weight.
- History h: an ordered chain of linked events.
- R: a durable record state.
- S: a stable self-maintaining pattern.
- tau_S(h): internal update count along a history.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
import cmath
import heapq
import itertools
import math
import random
from typing import Callable, DefaultDict


@dataclass
class BoundaryArrival:
    y: int
    free_arrival: float
    distorted_arrival: float


@dataclass
class GeodesicComparison:
    target_y: int
    free_action: float
    distorted_action: float
    free_path_y: str
    distorted_path_y: str


@dataclass
class SymmetryCandidate:
    name: str
    max_boost_drift: float


@dataclass
class PatternSample:
    node: tuple[int, int]
    occupancy: float
    persistence_support: float
    field_strength: float


@dataclass
class RuleCandidate:
    seed_node: tuple[int, int]
    survive_counts: frozenset[int]
    birth_counts: frozenset[int]
    persistent_nodes: frozenset[tuple[int, int]]
    occupancy: dict[tuple[int, int], float]
    orbit_sizes: list[int]
    support_sum: float
    occupancy_mean: float
    density: float
    boundary_touch: int
    area: int


@dataclass
class RobustnessResult:
    scenario_name: str
    rule_family: str
    seed_node: tuple[int, int]
    rule_signature: str
    rule_breadth: int
    fallback_used: bool
    persistent_nodes: int
    center_gap: float
    arrival_span: float
    centroid_y: float
    occupancy_mean: float
    density: float
    total_trials: int
    empty_patterns: int
    disconnected_rejections: int
    size_rejections: int
    boundary_rejections: int
    accepted_candidates: int
    dominant_rejection: str
    survived: bool
    status: str


@dataclass
class FamilyDiagnostic:
    rule_family: str
    survives: int
    mixed: int
    fragile: int
    no_pattern: int
    avg_rule_breadth: float
    avg_nodes: float
    avg_center_gap: float
    avg_arrival_span: float
    dominant_rule: str


@dataclass
class SearchDiagnostics:
    total_trials: int
    empty_patterns: int
    disconnected_rejections: int
    size_rejections: int
    boundary_rejections: int
    accepted_candidates: int
    dominant_rejection: str


@dataclass
class FocusedComparison:
    label: str
    rule_signature: str
    center_gap: float
    arrival_span: float
    status: str


@dataclass
class AblationResult:
    removed_option: str
    survives: int
    mixed: int
    fragile: int
    no_pattern: int
    failed_scenarios: str


@dataclass
class MechanismAblationResult:
    label: str
    action_mode: str
    field_mode: str
    survives: int
    mixed: int
    fragile: int
    no_pattern: int
    avg_center_gap: float
    avg_arrival_span: float
    failed_scenarios: str


@dataclass
class ActionDiscriminatorResult:
    label: str
    survives: int
    min_response: float
    min_wrapped_response: float
    failed_scenarios: str


@dataclass
class ActionFamilyResult:
    retained_weight: float
    survives: int
    mixed: int
    fragile: int
    no_pattern: int
    avg_center_gap: float
    avg_arrival_span: float
    min_response: float
    min_wrapped_response: float


@dataclass
class ActionPackResult:
    pack_name: str
    retained_weight: float
    survives: int
    mixed: int
    fragile: int
    no_pattern: int
    min_response: float
    min_wrapped_response: float
    pack_pass: bool


@dataclass
class ProperTimeConsistencyResult:
    retained_weight: float
    survives: int
    min_margin: float
    min_wrapped_margin: float
    worst_case: str
    pass_all: bool


@dataclass
class CriticalWeightCase:
    pack_name: str
    scenario_name: str
    target_y: int
    critical_weight: float
    margin_at_one: float
    delay_penalty: float
    retained_total: float


@dataclass
class WeightBranchScanRow:
    retained_weight: float
    rule_signature: str
    source_y: int
    worst_target_y: int
    min_margin: float
    critical_weight: float


@dataclass
class RuleSelectionDiagnosticRow:
    retained_weight: float
    fallback_rule: str
    fallback_center_gap: float
    fallback_arrival_span: float
    fallback_status: str
    rescue_rule: str
    rescue_center_gap: float
    rescue_arrival_span: float
    rescue_status: str
    final_rule: str
    switched: bool


@dataclass
class FixedBranchCompetitionRow:
    retained_weight: float
    branch_label: str
    rule_signature: str
    center_gap: float
    arrival_span: float
    status: str
    min_margin: float


@dataclass
class CenterGapGeometryRow:
    branch_label: str
    rule_signature: str
    source_y_start: int
    source_y_end: int
    stable_paths: bool
    center_action_start: float
    center_action_end: float
    side_avg_start: float
    side_avg_end: float
    gap_start: float
    gap_end: float


@dataclass
class FocusMetricComparisonRow:
    retained_weight: float
    fallback_action_gap: float
    rescue_action_gap: float
    fallback_geometric_gap: float
    rescue_geometric_gap: float
    fallback_stiffness: float
    rescue_stiffness: float
    action_winner: str
    geometric_winner: str
    stiffness_winner: str


@dataclass
class SelectorPolicyRow:
    retained_weight: float
    fallback_rule: str
    fallback_status: str
    fallback_quality: float
    rescue_rule: str
    rescue_status: str
    rescue_quality: float
    gated_final_rule: str
    ungated_final_rule: str
    differs: bool


@dataclass
class SelectorSweepCase:
    pack_name: str
    scenario_name: str
    retained_weight: float
    gated_rule: str
    gated_status: str
    ungated_rule: str
    ungated_status: str
    differs: bool


@dataclass
class EvaluatedCandidate:
    rule_family: str
    pack_name: str
    scenario_name: str
    retained_weight: float
    candidate_identity: tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ]
    search_sources: str
    seed_node: tuple[int, int]
    survive_counts: frozenset[int]
    birth_counts: frozenset[int]
    rule_signature: str
    persistent_nodes: int
    occupancy_mean: float
    density: float
    center_gap: float
    arrival_span: float
    centroid_y: float
    status: str
    status_rank: int
    min_margin: float
    min_wrapped_margin: float
    geometric_focus_gap: float
    stiffness: float
    focus_score: float
    current_selected: bool = False
    pc1_score: float = 0.0
    pc2_score: float = 0.0
    pc3_score: float = 0.0
    on_robustness: bool = False
    on_proper_time: bool = False
    on_geometry: bool = False
    on_mixed: bool = False


@dataclass
class FrontierScenarioRow:
    pack_name: str
    scenario_name: str
    rule_family: str
    retained_weight: float
    pool_size: int
    selected_rule: str
    selected_on_robustness: bool
    selected_on_proper_time: bool
    selected_on_geometry: bool
    selected_on_mixed: bool
    robustness_count: int
    proper_time_count: int
    geometry_count: int
    mixed_count: int
    robustness_rules: str
    proper_time_rules: str
    geometry_rules: str
    mixed_rules: str


@dataclass
class FrontierAggregateRow:
    rule_family: str
    rule_signature: str
    case_hits: int
    selected_hits: int
    robustness_hits: int
    proper_time_hits: int
    geometry_hits: int
    mixed_hits: int


@dataclass
class DerivedAxisLoadingRow:
    component: str
    eigenvalue: float
    center_gap: float
    arrival_span: float
    min_margin: float
    geometric_focus_gap: float
    focus_score: float


@dataclass
class DerivedAxisScenarioRow:
    pack_name: str
    scenario_name: str
    rule_family: str
    retained_weight: float
    selected_rule: str
    selected_on_pc1: bool
    selected_on_pc12: bool
    selected_on_pc123: bool
    pc1_count: int
    pc12_count: int
    pc123_count: int
    pc1_rules: str
    pc12_rules: str
    pc123_rules: str


@dataclass
class DerivedAxisAggregateRow:
    rule_family: str
    rule_signature: str
    case_hits: int
    selected_hits: int
    pc1_hits: int
    pc12_hits: int
    pc123_hits: int


@dataclass
class DerivedBasisAblationRow:
    basis_name: str
    metrics: str
    dimension: int
    cases: int
    selected_on_pc1: int
    selected_on_pc12: int
    selected_on_pc123: int
    pc123_overlap_with_full: int
    compact_top_rule: str
    compact_top_pc123: int
    extended_top_rule: str
    extended_top_pc123: int


@dataclass
class DerivedBootstrapBasisRow:
    basis_name: str
    basis_type: str
    dimension: int
    cases: int
    selected_on_pc123: int
    pc123_overlap_with_full: int
    compact_top_rule: str
    compact_top_pc123: int
    extended_top_rule: str
    extended_top_pc123: int


@dataclass
class DerivedBootstrapStabilityRow:
    rule_family: str
    rule_signature: str
    basis_hits: int
    subset_basis_hits: int
    linear_random_hits: int
    nonlinear_basis_hits: int
    case_basis_hits: int
    top_basis_hits: int


@dataclass
class DerivedTransformBreakRow:
    mode: str
    direct_transform_break_strength: float | None
    projected_transform_break_strength: float | None
    weakest_basis_name: str
    weakest_overlap: int
    weakest_selected_on_pc123: int


@dataclass
class DerivedTransformStrengthRow:
    basis_name: str
    mode: str
    strength: float
    variant_name: str
    selected_on_pc123: int
    pc123_overlap_with_full: int
    compact_top_rule: str
    compact_top_pc123: int
    extended_top_rule: str
    extended_top_pc123: int


@dataclass
class DerivedTransformStabilityRow:
    rule_family: str
    rule_signature: str
    basis_hits: int
    direct_hits: int
    projected_hits: int
    top_hits: int


@dataclass
class DerivedProjectionBootstrapRow:
    mode: str
    strength: float
    projections: int
    overlap_min: int
    overlap_avg: float
    selected_min: int
    selected_avg: float
    compact_dominant_rule: str
    compact_dominant_basis_hits: int
    compact_dominant_top_hits: int
    extended_dominant_rule: str
    extended_dominant_basis_hits: int
    extended_dominant_top_hits: int


@dataclass
class DerivedProjectionStabilityRow:
    rule_family: str
    rule_signature: str
    basis_hits: int
    top_hits: int


@dataclass
class ProjectionGeneratorAblationRow:
    generator: str
    bases: int
    weakest_basis_name: str
    overlap_min: int
    overlap_avg: float
    selected_min: int
    selected_avg: float
    compact_dominant_rule: str
    compact_dominant_basis_hits: int
    compact_dominant_top_hits: int
    extended_dominant_rule: str
    extended_dominant_basis_hits: int
    extended_dominant_top_hits: int


@dataclass
class ProjectionDimensionAblationRow:
    dimension: int
    bases: int
    weakest_basis_name: str
    overlap_min: int
    overlap_avg: float
    selected_min: int
    selected_avg: float
    compact_dominant_rule: str
    compact_dominant_basis_hits: int
    compact_dominant_top_hits: int
    extended_dominant_rule: str
    extended_dominant_basis_hits: int
    extended_dominant_top_hits: int


@dataclass
class ProjectionFamilyBasisRow:
    basis_name: str
    mode: str
    strength: float
    selected_on_pc123: int
    pc123_overlap_with_full: int
    compact_top_rule: str
    compact_top_pc123: int
    extended_top_rule: str
    extended_top_pc123: int


@dataclass
class ProjectionFamilyStabilityRow:
    rule_family: str
    rule_signature: str
    basis_hits: int
    case_hits: int
    top_hits: int


@dataclass
class ProjectionFamilyCaseCoreRow:
    pack_name: str
    scenario_name: str
    rule_family: str
    retained_weight: float
    selected_rule: str
    selected_in_core: bool
    core_count: int
    union_count: int
    core_rules: str
    union_rules: str


@dataclass
class ProjectionFamilyCoreAggregateRow:
    rule_family: str
    rule_signature: str
    core_hits: int
    union_hits: int
    selected_core_hits: int


@dataclass
class ProjectionCoreMechanismRow:
    regime: str
    cases: int
    selected_in_core_cases: int
    wrap_cases: int
    rect_cases: int
    taper_cases: int
    skew_cases: int
    crossing_cases: int
    avg_nodes: float
    avg_center_range: float
    avg_center_variation: float
    avg_span_range: float


@dataclass
class ProjectionCoreMechanismCaseRow:
    pack_name: str
    scenario_name: str
    rule_family: str
    retained_weight: float
    regime: str
    selected_rule: str
    selected_in_core: bool
    core_count: int
    union_count: int
    wrap_y: bool
    crosses_midline: bool
    nodes: int
    center_range: float
    center_variation: float
    span_range: float


@dataclass
class RoughnessCoreSweepRow:
    alpha: float
    rule_family: str
    retained_weight: float
    regime: str
    selected_rule: str
    selected_in_core: bool
    core_count: int
    union_count: int
    center_range: float
    center_variation: float
    span_range: float
    crosses_midline: bool


@dataclass
class RoughnessCoreAggregateRow:
    alpha: float
    rule_family: str
    cases: int
    selected_in_core_cases: int
    empty_cases: int
    single_selected_cases: int
    single_other_cases: int
    multi_selected_cases: int
    multi_other_cases: int
    avg_core_count: float
    center_range: float
    center_variation: float
    span_range: float
    crosses_midline: bool


@dataclass
class CenterlineModeSweepRow:
    mode: str
    amplitude: float
    rule_family: str
    retained_weight: float
    signature: str
    turning_points: int
    max_step_fraction: float
    regime: str
    selected_rule: str
    selected_in_core: bool
    core_count: int
    union_count: int
    center_range: float
    center_variation: float
    span_range: float
    crosses_midline: bool


@dataclass
class CenterlineModeAggregateRow:
    mode: str
    amplitude: float
    rule_family: str
    signature: str
    cases: int
    selected_in_core_cases: int
    empty_cases: int
    single_selected_cases: int
    single_other_cases: int
    multi_selected_cases: int
    multi_other_cases: int
    avg_core_count: float
    center_range: float
    center_variation: float
    span_range: float
    crosses_midline: bool


@dataclass
class CenterlineInvariantAggregateRow:
    rule_family: str
    signature: str
    crosses_midline: bool
    cases: int
    selected_in_core_cases: int
    empty_cases: int
    avg_core_count: float
    avg_center_variation: float


@dataclass
class CenterlineInvariantComparisonRow:
    rule_family: str
    center_variation: float
    signature: str
    crosses_midline: bool
    cases: int
    selected_in_core_cases: int
    empty_cases: int
    avg_core_count: float


@dataclass
class FrontierTraceRow:
    retained_weight: float
    rule_signature: str
    search_sources: str
    current_selected: bool
    on_robustness: bool
    on_proper_time: bool
    on_geometry: bool
    on_mixed: bool
    status: str
    center_gap: float
    arrival_span: float
    min_margin: float
    min_wrapped_margin: float


@dataclass
class PerturbationCaseRow:
    rule_family: str
    pack_name: str
    scenario_name: str
    variant_name: str
    node_delta: int
    base_selected_rule: str
    perturbed_selected_rule: str
    perturbed_status: str
    selected_matches_base: bool
    base_selected_alive: bool
    robustness_overlap: bool
    proper_time_overlap: bool
    geometry_overlap: bool
    mixed_overlap: bool


@dataclass
class PerturbationAggregateRow:
    rule_family: str
    variant_name: str
    cases: int
    survives: int
    selected_retained: int
    base_selected_alive: int
    robustness_overlap: int
    proper_time_overlap: int
    geometry_overlap: int
    mixed_overlap: int


@dataclass
class PerturbationWeightCaseRow:
    rule_family: str
    pack_name: str
    scenario_name: str
    variant_name: str
    low_weight: float
    high_weight: float
    low_selected_rule: str
    high_selected_rule: str
    low_status: str
    high_status: str
    same_selected: bool
    survives_both: bool
    base_alive_both: bool
    robustness_both: bool
    proper_time_both: bool
    geometry_both: bool
    mixed_both: bool


@dataclass
class PerturbationWeightAggregateRow:
    rule_family: str
    variant_name: str
    cases: int
    survives_both: int
    same_selected: int
    base_alive_both: int
    robustness_both: int
    proper_time_both: int
    geometry_both: int
    mixed_both: int


@dataclass
class PerturbationWeightLadderCaseRow:
    rule_family: str
    pack_name: str
    scenario_name: str
    variant_name: str
    weights: tuple[float, ...]
    selected_rules: tuple[str, ...]
    statuses: tuple[str, ...]
    same_selected_all: bool
    survives_all: bool
    base_alive_all: bool
    robustness_all: bool
    proper_time_all: bool
    geometry_all: bool
    mixed_all: bool


@dataclass
class PerturbationWeightLadderAggregateRow:
    rule_family: str
    variant_name: str
    cases: int
    survives_all: int
    same_selected_all: int
    base_alive_all: int
    robustness_all: int
    proper_time_all: int
    geometry_all: int
    mixed_all: int


@dataclass
class RediscoveryLimitAggregateRow:
    rediscovery_limit: int
    rule_family: str
    cases: int
    survives: int
    selected_retained: int
    base_selected_alive: int
    robustness_overlap: int
    proper_time_overlap: int
    geometry_overlap: int
    mixed_overlap: int


@dataclass
class ProceduralFailureDiagnosticRow:
    scenario_name: str
    variant_name: str
    selected_rule: str
    status: str
    mixed_overlap: bool
    center_gap: float
    arrival_span: float
    mean_center: float
    center_range: float
    center_total_variation: float
    crosses_midline: bool
    span_range: int


@dataclass
class ContourSensitivityRow:
    alpha: float
    selected_rule: str
    status: str
    mixed_overlap: bool
    center_gap: float
    arrival_span: float
    mean_center: float
    center_range: float
    center_total_variation: float
    crosses_midline: bool


@dataclass
class SelectedMetricCaseRow:
    dataset: str
    rule_family: str
    pack_name: str
    scenario_name: str
    variant_name: str
    selected_rule: str
    status: str
    center_gap: float
    arrival_span: float


@dataclass
class FocusObservableBenchmarkRow:
    observable: str
    core_preserved: int
    core_cases: int
    geometry_preserved: int
    geometry_survive_cases: int
    geometry_promoted: int
    geometry_non_survive_cases: int
    procedural_preserved: int
    procedural_survive_cases: int
    procedural_promoted: int
    procedural_non_survive_cases: int
    contour_survive_preserved: int
    contour_survive_cases: int
    contour_miss_status: str
    contour_miss_score: float


@dataclass
class FrontierObservableAblationRow:
    observable: str
    rule_family: str
    cases: int
    selected_changes: int
    selected_survives: int
    baseline_selected_survives: int
    selected_on_robustness: int
    selected_on_proper_time: int
    selected_on_geometry: int
    selected_on_mixed: int
    baseline_on_robustness: int
    baseline_on_proper_time: int
    baseline_on_geometry: int
    baseline_on_mixed: int


@dataclass
class FrontierObservableChangeRow:
    pack_name: str
    scenario_name: str
    rule_family: str
    retained_weight: float
    baseline_selected_rule: str
    observable_selected_rule: str
    baseline_selected_status: str
    observable_selected_status: str
    baseline_on_robustness: bool
    baseline_on_proper_time: bool
    baseline_on_geometry: bool
    baseline_on_mixed: bool
    observable_on_robustness: bool
    observable_on_proper_time: bool
    observable_on_geometry: bool
    observable_on_mixed: bool


@dataclass
class RawFrontierPool:
    selector_candidates: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        RuleCandidate,
    ]
    primary_selector_identity: tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ] | None
    fallback_selector_identity: tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ] | None
    rescue_selector_identities: tuple[
        tuple[
            frozenset[int],
            frozenset[int],
            frozenset[tuple[int, int]],
        ],
        ...,
    ]
    pooled_candidates: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        RuleCandidate,
    ]
    candidate_sources: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        str,
    ]
    primary_best_identity: tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ] | None
    fallback_best_identity: tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ] | None
    rescue_identities: tuple[
        tuple[
            frozenset[int],
            frozenset[int],
            frozenset[tuple[int, int]],
        ],
        ...,
    ]


@dataclass
class FrontierCandidateProfile:
    field: dict[tuple[int, int], float]
    centroid_y: float
    source_y: int
    target_ys: tuple[int, ...]
    center_target: int
    distorted_arrivals: dict[tuple[int, int], float]


@dataclass
class FrontierMetricSnapshot:
    centroid_y: float
    center_gap: float
    arrival_span: float
    status: str
    status_rank: int
    min_margin: float
    min_wrapped_margin: float
    geometric_focus_gap: float
    stiffness: float


@dataclass
class FrontierEvaluationCache:
    min_x: int
    max_x: int
    left_boundary_ys: tuple[int, ...]
    right_boundary_ys: tuple[int, ...]
    free_field: dict[tuple[int, int], float]
    free_arrivals_by_source: dict[int, dict[tuple[int, int], float]] = field(default_factory=dict)
    free_action_trees: dict[
        tuple[int, float],
        tuple[
            dict[tuple[int, int], float],
            dict[tuple[int, int], tuple[int, int]],
        ],
    ] = field(default_factory=dict)
    candidate_profiles: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        FrontierCandidateProfile,
    ] = field(default_factory=dict)
    distorted_action_trees: dict[
        tuple[
            tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
            float,
        ],
        tuple[
            dict[tuple[int, int], float],
            dict[tuple[int, int], tuple[int, int]],
        ],
    ] = field(default_factory=dict)
    metric_snapshots: dict[
        tuple[
            tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
            float,
        ],
        FrontierMetricSnapshot,
    ] = field(default_factory=dict)


@dataclass(frozen=True)
class LocalRule:
    persistent_nodes: frozenset[tuple[int, int]]
    phase_wavenumber: float
    attenuation_power: float = 1.0
    action_mode: str = "spent_delay"
    field_mode: str = "relaxed"
    action_retained_weight: float = 1.0


@dataclass(frozen=True)
class RulePostulates:
    phase_per_action: float
    attenuation_power: float = 1.0
    action_mode: str = "spent_delay"
    field_mode: str = "relaxed"
    action_retained_weight: float = 1.0


COMPACT_COUNT_OPTIONS = (
    frozenset({1}),
    frozenset({2}),
    frozenset({3}),
    frozenset({4}),
    frozenset({1, 2}),
    frozenset({1, 3}),
    frozenset({2, 3}),
    frozenset({3, 4}),
    frozenset({1, 2, 3}),
    frozenset({2, 3, 4}),
    frozenset({1, 2, 3, 4}),
)

EXTENDED_COUNT_OPTIONS = COMPACT_COUNT_OPTIONS + (
    frozenset({5}),
    frozenset({4, 5}),
    frozenset({3, 5}),
    frozenset({2, 3, 5}),
    frozenset({1, 2, 3, 4, 5}),
)

LEGACY_SWEEP_COMPACT_COUNT_OPTIONS = (
    frozenset({1}),
    frozenset({2}),
    frozenset({3}),
    frozenset({1, 2}),
    frozenset({2, 3}),
    frozenset({3, 4}),
)

REPAIRED_COMPACT_COUNT_OPTIONS = (
    frozenset({3}),
    frozenset({1, 3}),
    frozenset({2, 3}),
    frozenset({3, 4}),
)

MINIMAL_COMPACT_COUNT_OPTIONS = (
    frozenset({1, 3}),
    frozenset({2, 3}),
    frozenset({3, 4}),
)

SWEEP_COMPACT_COUNT_OPTIONS = MINIMAL_COMPACT_COUNT_OPTIONS

SWEEP_EXTENDED_COUNT_OPTIONS = SWEEP_COMPACT_COUNT_OPTIONS + (
    frozenset({1, 2, 3}),
    frozenset({2, 3, 4}),
    frozenset({1, 2, 3, 4}),
)

WINNER_RULE_PAIRS = (
    (frozenset({2, 3}), frozenset({3})),
    (frozenset({1}), frozenset({1, 3})),
    (frozenset({3, 4}), frozenset({1, 3})),
    (frozenset({2, 3, 4}), frozenset({1})),
    (frozenset({1, 2, 3}), frozenset({1, 3})),
)


def derive_local_rule(
    persistent_nodes: frozenset[tuple[int, int]],
    postulates: RulePostulates,
) -> LocalRule:
    """Translate simple postulates into the shared local edge rule."""

    return LocalRule(
        persistent_nodes=persistent_nodes,
        phase_wavenumber=postulates.phase_per_action,
        attenuation_power=postulates.attenuation_power,
        action_mode=postulates.action_mode,
        field_mode=postulates.field_mode,
        action_retained_weight=postulates.action_retained_weight,
    )


def proper_time_deficit(delay: float, link_length: float) -> float:
    """Positive action-like cost from local delay and retained proper update."""

    retained_update = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    return delay - retained_update


def action_increment_for_mode(
    delay: float,
    link_length: float,
    action_mode: str,
    retained_weight: float,
) -> float:
    retained_update = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    if action_mode == "spent_delay":
        return delay - retained_update
    if action_mode == "retained_mix":
        return delay - retained_weight * retained_update
    if action_mode == "coordinate_delay":
        return delay
    if action_mode == "link_length":
        return link_length
    raise ValueError(f"Unknown action mode: {action_mode}")


def lorentz_boost(delay: float, dx: float, velocity: float) -> tuple[float, float]:
    """Boost-like frame mixing with signal speed normalized to one."""

    gamma = 1.0 / math.sqrt(1.0 - velocity * velocity)
    return (
        gamma * (delay - velocity * dx),
        gamma * (dx - velocity * delay),
    )


def retained_update_symmetry_test() -> list[SymmetryCandidate]:
    """Check which local scalar survives boost-like frame mixing."""

    samples = [
        (1.4, 0.8),
        (1.8, 1.0),
        (2.2, 1.3),
    ]
    velocities = [-0.6, -0.3, 0.3, 0.6]
    candidates = {
        "coordinate delay dt": lambda dt, dx: dt,
        "euclidean norm sqrt(dt^2 + dx^2)": lambda dt, dx: math.sqrt(dt * dt + dx * dx),
        "retained update sqrt(dt^2 - dx^2)": lambda dt, dx: math.sqrt(max(dt * dt - dx * dx, 0.0)),
        "spent delay dt - sqrt(dt^2 - dx^2)": lambda dt, dx: dt - math.sqrt(
            max(dt * dt - dx * dx, 0.0)
        ),
    }

    rows: list[SymmetryCandidate] = []
    for name, candidate in candidates.items():
        max_drift = 0.0
        for delay, dx in samples:
            baseline = candidate(delay, dx)
            for velocity in velocities:
                boosted_delay, boosted_dx = lorentz_boost(delay, dx, velocity)
                boosted_value = candidate(boosted_delay, boosted_dx)
                max_drift = max(max_drift, abs(boosted_value - baseline))
        rows.append(SymmetryCandidate(name=name, max_boost_drift=max_drift))
    return rows


def point_seed(
    center: tuple[int, int],
) -> frozenset[tuple[int, int]]:
    return frozenset({center})


def point_seed_builder(
    center: tuple[int, int],
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> frozenset[tuple[int, int]]:
    del nodes, wrap_y
    return point_seed(center)


def clamped_offsets(center_y: int, offsets: list[int], height: int) -> list[int]:
    values = [max(-height, min(height, center_y + offset)) for offset in offsets]
    unique_values: list[int] = []
    for value in values:
        if value not in unique_values:
            unique_values.append(value)
    return unique_values


def outer_boundary_nodes(nodes: set[tuple[int, int]]) -> set[tuple[int, int]]:
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    min_y = min(y for _x, y in nodes)
    max_y = max(y for _x, y in nodes)
    return {
        node
        for node in nodes
        if node[0] in {min_x, max_x} or node[1] in {min_y, max_y}
    }


def boundary_nodes(
    nodes: set[tuple[int, int]],
    wrap_y: bool = False,
) -> set[tuple[int, int]]:
    if not wrap_y:
        return outer_boundary_nodes(nodes)

    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    return {node for node in nodes if node[0] in {min_x, max_x}}


def derive_persistence_support(
    nodes: set[tuple[int, int]],
    persistent_nodes: frozenset[tuple[int, int]],
    wrap_y: bool = False,
) -> dict[tuple[int, int], float]:
    support = {node: 0.0 for node in nodes}
    active_nodes = persistent_nodes & nodes
    for node in active_nodes:
        neighbors = graph_neighbors(node, nodes, wrap_y=wrap_y)
        support[node] = sum(neighbor in active_nodes for neighbor in neighbors) / len(neighbors)
    return support


def evolve_self_maintaining_pattern(
    nodes: set[tuple[int, int]],
    seed_nodes: frozenset[tuple[int, int]],
    survive_counts: frozenset[int] = frozenset({3, 4}),
    birth_counts: frozenset[int] = frozenset({3, 4}),
    steps: int = 12,
    wrap_y: bool = False,
) -> list[frozenset[tuple[int, int]]]:
    """Run a local self-maintenance rule and keep the full orbit."""

    active_nodes = set(seed_nodes & nodes)
    history: list[frozenset[tuple[int, int]]] = []

    for _ in range(steps):
        history.append(frozenset(active_nodes))
        neighbor_counts: Counter[tuple[int, int]] = Counter({node: 0 for node in active_nodes})
        for node in active_nodes:
            for neighbor in graph_neighbors(node, nodes, wrap_y=wrap_y):
                neighbor_counts[neighbor] += 1

        active_nodes = {
            node
            for node, count in neighbor_counts.items()
            if (node in active_nodes and count in survive_counts)
            or (node not in active_nodes and count in birth_counts)
        }

    return history


def derive_emergent_persistent_nodes(
    nodes: set[tuple[int, int]],
    seed_nodes: frozenset[tuple[int, int]],
    survive_counts: frozenset[int] = frozenset({3, 4}),
    birth_counts: frozenset[int] = frozenset({3, 4}),
    steps: int = 12,
    sample_window: int = 6,
    occupancy_threshold: float = 2 / 3,
    wrap_y: bool = False,
) -> tuple[frozenset[tuple[int, int]], dict[tuple[int, int], float], list[int]]:
    """Turn a local orbit into a time-thick persistent pattern."""

    history = evolve_self_maintaining_pattern(
        nodes,
        seed_nodes=seed_nodes,
        survive_counts=survive_counts,
        birth_counts=birth_counts,
        steps=steps,
        wrap_y=wrap_y,
    )
    late_window = history[-sample_window:]
    occupancy = {node: 0.0 for node in nodes}
    for active_nodes in late_window:
        for node in active_nodes:
            occupancy[node] += 1.0 / len(late_window)

    persistent_nodes = frozenset(
        node for node, fraction in occupancy.items() if fraction >= occupancy_threshold
    )
    orbit_sizes = [len(active_nodes) for active_nodes in history]
    return persistent_nodes, occupancy, orbit_sizes


def connected_components(
    active_nodes: frozenset[tuple[int, int]],
    nodes: set[tuple[int, int]],
    wrap_y: bool = False,
) -> list[frozenset[tuple[int, int]]]:
    remaining = set(active_nodes)
    components: list[frozenset[tuple[int, int]]] = []

    while remaining:
        start = remaining.pop()
        component = {start}
        frontier = [start]
        while frontier:
            node = frontier.pop()
            for neighbor in graph_neighbors(node, nodes, wrap_y=wrap_y):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.add(neighbor)
                    frontier.append(neighbor)
        components.append(frozenset(component))

    return components


def component_density(component: frozenset[tuple[int, int]]) -> float:
    xs = [x for x, _y in component]
    ys = [y for _x, y in component]
    area = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)
    return len(component) / area


def boundary_touch_count(
    component: frozenset[tuple[int, int]],
    nodes: set[tuple[int, int]],
    wrap_y: bool = False,
) -> int:
    boundaries = boundary_nodes(nodes, wrap_y=wrap_y)
    return sum(node in boundaries for node in component)


def component_area(component: frozenset[tuple[int, int]]) -> int:
    xs = [x for x, _y in component]
    ys = [y for _x, y in component]
    return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)


def format_rule_signature(
    survive_counts: frozenset[int],
    birth_counts: frozenset[int],
) -> str:
    return f"S{sorted(survive_counts)}/B{sorted(birth_counts)}"


def parse_rule_signature(
    signature: str,
) -> tuple[frozenset[int], frozenset[int]]:
    survive_label, birth_label = signature.split("/B")
    survive_counts = frozenset(
        int(value.strip())
        for value in survive_label.removeprefix("S[").removesuffix("]").split(",")
        if value.strip()
    )
    birth_counts = frozenset(
        int(value.strip())
        for value in birth_label.removeprefix("[").removesuffix("]").split(",")
        if value.strip()
    )
    return survive_counts, birth_counts


def count_option_sort_key(counts: frozenset[int]) -> tuple[int, tuple[int, ...]]:
    return len(counts), tuple(sorted(counts))


def format_count_options(
    count_options: tuple[frozenset[int], ...],
) -> str:
    return ", ".join(f"{sorted(counts)}" for counts in count_options)


def format_single_count_option(counts: frozenset[int]) -> str:
    return str(sorted(counts))


def dominant_rejection_label(counts: Counter[str]) -> str:
    if not any(counts.values()):
        return "none"
    return max(sorted(counts), key=lambda label: counts[label])


def ordered_rule_pairs(
    count_options: tuple[frozenset[int], ...],
    preferred_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] = (),
) -> list[tuple[frozenset[int], frozenset[int]]]:
    all_pairs = [
        (survive_counts, birth_counts)
        for survive_counts in count_options
        for birth_counts in count_options
    ]
    preferred = [
        pair
        for pair in preferred_rule_pairs
        if pair[0] in count_options and pair[1] in count_options
    ]
    remaining = [pair for pair in all_pairs if pair not in preferred]
    return [*preferred, *remaining]


def filter_rule_pairs(
    count_options: tuple[frozenset[int], ...],
    exact_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] | None,
) -> list[tuple[frozenset[int], frozenset[int]]]:
    if exact_rule_pairs is None:
        return []
    return [
        pair
        for pair in exact_rule_pairs
        if pair[0] in count_options and pair[1] in count_options
    ]


def merge_search_diagnostics(*diagnostics: SearchDiagnostics) -> SearchDiagnostics:
    counts = Counter(
        {
            "empty": sum(diag.empty_patterns for diag in diagnostics),
            "disconnected": sum(diag.disconnected_rejections for diag in diagnostics),
            "size": sum(diag.size_rejections for diag in diagnostics),
            "boundary": sum(diag.boundary_rejections for diag in diagnostics),
        }
    )
    return SearchDiagnostics(
        total_trials=sum(diag.total_trials for diag in diagnostics),
        empty_patterns=counts["empty"],
        disconnected_rejections=counts["disconnected"],
        size_rejections=counts["size"],
        boundary_rejections=counts["boundary"],
        accepted_candidates=sum(diag.accepted_candidates for diag in diagnostics),
        dominant_rejection=dominant_rejection_label(counts),
    )


def candidate_identity_key(
    candidate: RuleCandidate,
) -> tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]]:
    return (
        candidate.survive_counts,
        candidate.birth_counts,
        candidate.persistent_nodes,
    )


def candidate_search_key(
    candidate: RuleCandidate,
    graph_center: tuple[float, float],
    preferred_set: set[tuple[frozenset[int], frozenset[int]]],
    preferred_bonus: float,
) -> tuple[float, ...]:
    preferred_score = (
        preferred_bonus
        if (candidate.survive_counts, candidate.birth_counts) in preferred_set
        else 0.0
    )
    orbit_variation = max(candidate.orbit_sizes[-4:]) - min(candidate.orbit_sizes[-4:])
    seed_distance_sq = (
        (candidate.seed_node[0] - graph_center[0]) ** 2
        + (candidate.seed_node[1] - graph_center[1]) ** 2
    )
    return (
        round(candidate.occupancy_mean, 12),
        round(candidate.density, 12),
        round(candidate.support_sum, 12),
        round(preferred_score, 12),
        -float(candidate.area),
        -float(orbit_variation),
        -float(seed_distance_sq),
        -float(candidate.seed_node[0]),
        -float(candidate.seed_node[1]),
    )


def collect_self_maintenance_candidates(
    nodes: set[tuple[int, int]],
    count_options: tuple[frozenset[int], ...] = COMPACT_COUNT_OPTIONS,
    wrap_y: bool = False,
    evolution_steps: int = 10,
    sample_window: int = 4,
    occupancy_threshold: float = 0.75,
    min_component_fraction: float = 1.0,
    preferred_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] = (),
    exact_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] | None = None,
    preferred_bonus: float = 0.0,
    seed_builders: tuple[
        Callable[[tuple[int, int], set[tuple[int, int]], bool], frozenset[tuple[int, int]]],
        ...,
    ] = (point_seed_builder,),
) -> tuple[list[RuleCandidate], SearchDiagnostics]:
    """Search over seeds and local rules, returning all accepted compact patterns plus rejection stats."""

    graph_boundaries = boundary_nodes(nodes, wrap_y=wrap_y)
    interior_nodes = sorted(node for node in nodes if node not in graph_boundaries)
    xs = [x for x, _y in nodes]
    ys = [y for _x, y in nodes]
    graph_center = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    preferred_set = set(preferred_rule_pairs)
    rule_pairs = filter_rule_pairs(count_options, exact_rule_pairs)
    if not rule_pairs:
        rule_pairs = ordered_rule_pairs(count_options, preferred_rule_pairs)

    total_trials = 0
    rejection_counts: Counter[str] = Counter()
    accepted_candidates = 0
    best_by_identity: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        RuleCandidate,
    ] = {}
    best_key_by_identity: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        tuple[float, ...],
    ] = {}

    for seed_node in interior_nodes:
        for seed_builder in seed_builders:
            seed_nodes = seed_builder(seed_node, nodes, wrap_y)
            for survive_counts, birth_counts in rule_pairs:
                total_trials += 1
                persistent_nodes, occupancy, orbit_sizes = derive_emergent_persistent_nodes(
                    nodes,
                    seed_nodes=seed_nodes,
                    survive_counts=survive_counts,
                    birth_counts=birth_counts,
                    steps=evolution_steps,
                    sample_window=sample_window,
                    occupancy_threshold=occupancy_threshold,
                    wrap_y=wrap_y,
                )
                if not persistent_nodes:
                    rejection_counts["empty"] += 1
                    continue

                largest_component = max(
                    connected_components(persistent_nodes, nodes, wrap_y=wrap_y),
                    key=len,
                )
                component_fraction = len(largest_component) / len(persistent_nodes)
                if component_fraction < min_component_fraction:
                    rejection_counts["disconnected"] += 1
                    continue
                if not 4 <= len(largest_component) <= 16:
                    rejection_counts["size"] += 1
                    continue

                density = component_density(largest_component)
                boundary_count = boundary_touch_count(largest_component, nodes, wrap_y=wrap_y)
                if boundary_count:
                    rejection_counts["boundary"] += 1
                    continue

                accepted_candidates += 1
                area = component_area(largest_component)
                support = derive_persistence_support(nodes, largest_component, wrap_y=wrap_y)
                support_sum = sum(support[node] for node in largest_component)
                average_occupancy = sum(occupancy[node] for node in largest_component) / len(
                    largest_component
                )
                component_occupancy = {
                    node: occupancy[node] if node in largest_component else 0.0
                    for node in nodes
                }

                candidate = RuleCandidate(
                    seed_node=seed_node,
                    survive_counts=survive_counts,
                    birth_counts=birth_counts,
                    persistent_nodes=largest_component,
                    occupancy=component_occupancy,
                    orbit_sizes=orbit_sizes,
                    support_sum=support_sum,
                    occupancy_mean=average_occupancy,
                    density=density,
                    boundary_touch=boundary_count,
                    area=area,
                )
                identity = candidate_identity_key(candidate)
                search_key = candidate_search_key(
                    candidate,
                    graph_center=graph_center,
                    preferred_set=preferred_set,
                    preferred_bonus=preferred_bonus,
                )
                if identity not in best_key_by_identity or search_key > best_key_by_identity[identity]:
                    best_key_by_identity[identity] = search_key
                    best_by_identity[identity] = candidate

    diagnostics = SearchDiagnostics(
        total_trials=total_trials,
        empty_patterns=rejection_counts["empty"],
        disconnected_rejections=rejection_counts["disconnected"],
        size_rejections=rejection_counts["size"],
        boundary_rejections=rejection_counts["boundary"],
        accepted_candidates=accepted_candidates,
        dominant_rejection=dominant_rejection_label(rejection_counts),
    )

    sorted_candidates = [
        best_by_identity[identity]
        for identity in sorted(
            best_by_identity,
            key=lambda current_identity: best_key_by_identity[current_identity],
            reverse=True,
        )
    ]
    return sorted_candidates, diagnostics


def scan_self_maintenance_rules(
    nodes: set[tuple[int, int]],
    count_options: tuple[frozenset[int], ...] = COMPACT_COUNT_OPTIONS,
    wrap_y: bool = False,
    evolution_steps: int = 10,
    sample_window: int = 4,
    occupancy_threshold: float = 0.75,
    min_component_fraction: float = 1.0,
    preferred_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] = (),
    exact_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] | None = None,
    preferred_bonus: float = 0.0,
    seed_builders: tuple[
        Callable[[tuple[int, int], set[tuple[int, int]], bool], frozenset[tuple[int, int]]],
        ...,
    ] = (point_seed_builder,),
) -> tuple[RuleCandidate | None, SearchDiagnostics]:
    """Search over seeds and local rules, returning the best pattern plus rejection stats."""

    candidates, diagnostics = collect_self_maintenance_candidates(
        nodes,
        count_options=count_options,
        wrap_y=wrap_y,
        evolution_steps=evolution_steps,
        sample_window=sample_window,
        occupancy_threshold=occupancy_threshold,
        min_component_fraction=min_component_fraction,
        preferred_rule_pairs=preferred_rule_pairs,
        exact_rule_pairs=exact_rule_pairs,
        preferred_bonus=preferred_bonus,
        seed_builders=seed_builders,
    )
    best_candidate = candidates[0] if candidates else None
    return best_candidate, diagnostics


def select_self_maintenance_rule(
    nodes: set[tuple[int, int]],
    count_options: tuple[frozenset[int], ...] = COMPACT_COUNT_OPTIONS,
    wrap_y: bool = False,
    evolution_steps: int = 10,
    sample_window: int = 4,
    occupancy_threshold: float = 0.75,
    preferred_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] = (),
    preferred_bonus: float = 0.0,
) -> RuleCandidate:
    """Search over seeds and local rules for a compact localized persistent pattern."""
    best_candidate, _diagnostics = scan_self_maintenance_rules(
        nodes,
        count_options=count_options,
        wrap_y=wrap_y,
        evolution_steps=evolution_steps,
        sample_window=sample_window,
        occupancy_threshold=occupancy_threshold,
        preferred_rule_pairs=preferred_rule_pairs,
        preferred_bonus=preferred_bonus,
    )
    if best_candidate is None:
        raise RuntimeError("No compact self-maintenance rule produced a persistent pattern.")

    return best_candidate


def derive_node_field(
    nodes: set[tuple[int, int]],
    rule: LocalRule,
    tolerance: float = 1e-8,
    max_iterations: int = 400,
    wrap_y: bool = False,
) -> dict[tuple[int, int], float]:
    """Derive a local slowing field from a persistent subgraph."""

    support = derive_persistence_support(nodes, rule.persistent_nodes, wrap_y=wrap_y)
    if rule.field_mode == "none":
        return {node: 0.0 for node in nodes}
    if not any(support.values()):
        return support
    if rule.field_mode == "support_only":
        return support
    if rule.field_mode != "relaxed":
        raise ValueError(f"Unknown field mode: {rule.field_mode}")

    field = dict(support)
    graph_boundaries = boundary_nodes(nodes, wrap_y=wrap_y)

    for _ in range(max_iterations):
        updated: dict[tuple[int, int], float] = {}
        max_change = 0.0
        for node in nodes:
            if node in graph_boundaries:
                new_value = 0.0
            else:
                neighbors = graph_neighbors(node, nodes, wrap_y=wrap_y)
                average_neighbor_field = (
                    sum(field[neighbor] for neighbor in neighbors) / len(neighbors)
                )
                new_value = support[node] + (1.0 - support[node]) * average_neighbor_field
            updated[node] = new_value
            max_change = max(max_change, abs(new_value - field[node]))
        field = updated
        if max_change < tolerance:
            break
    return field


def field_centroid(field: dict[tuple[int, int], float]) -> tuple[float, float]:
    total_weight = sum(field.values())
    if total_weight == 0.0:
        return 0.0, 0.0
    return (
        sum(x * weight for (x, _y), weight in field.items()) / total_weight,
        sum(y * weight for (_x, y), weight in field.items()) / total_weight,
    )


def sample_pattern(
    occupancy: dict[tuple[int, int], float],
    support: dict[tuple[int, int], float],
    field: dict[tuple[int, int], float],
    sample_nodes: list[tuple[int, int]],
) -> list[PatternSample]:
    return [
        PatternSample(
            node=node,
            occupancy=occupancy[node],
            persistence_support=support[node],
            field_strength=field[node],
        )
        for node in sample_nodes
    ]


def local_edge_properties(
    start: tuple[float, float],
    end: tuple[float, float],
    rule: LocalRule,
    node_field: dict[tuple[int, int], float],
) -> tuple[float, float, complex]:
    """Return the shared local delay, action increment, and amplitude."""

    link_length = math.dist(start, end)
    local_field = 0.5 * (node_field[start] + node_field[end])
    delay = link_length * (1.0 + local_field)
    action_increment = action_increment_for_mode(
        delay,
        link_length,
        rule.action_mode,
        rule.action_retained_weight,
    )

    amplitude = cmath.exp(1j * rule.phase_wavenumber * action_increment) / (
        delay ** rule.attenuation_power
    )
    return delay, action_increment, amplitude


def infer_causal_arrival_times(
    width: int,
    height: int,
    source: tuple[int, int],
    rule: LocalRule,
    wrap_y: bool = False,
) -> dict[tuple[int, int], float]:
    """Infer causal order from positive local delays on a graph."""

    nodes = build_rectangular_nodes(width=width, height=height)
    node_field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    neighbor_offsets = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    arrival_times: dict[tuple[int, int], float] = {source: 0.0}
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, source)]

    while frontier:
        current_time, node = heapq.heappop(frontier)
        if current_time != arrival_times[node]:
            continue

        for dx, dy in neighbor_offsets:
            neighbor = (node[0] + dx, node[1] + dy)
            if neighbor not in nodes:
                continue

            local_delay, _action_increment, _amplitude = local_edge_properties(
                node,
                neighbor,
                rule,
                node_field,
            )
            neighbor_time = current_time + local_delay

            if neighbor_time < arrival_times.get(neighbor, math.inf):
                arrival_times[neighbor] = neighbor_time
                heapq.heappush(frontier, (neighbor_time, neighbor))

    return arrival_times


def build_rectangular_nodes(
    width: int,
    height: int,
    blocked_nodes: frozenset[tuple[int, int]] = frozenset(),
) -> set[tuple[int, int]]:
    return {
        (x, y)
        for x in range(width + 1)
        for y in range(-height, height + 1)
        if (x, y) not in blocked_nodes
    }


def build_tapered_nodes(width: int, height: int) -> set[tuple[int, int]]:
    mid_x = width / 2
    nodes: set[tuple[int, int]] = set()
    for x in range(width + 1):
        pinch = max(0, 2 - round(abs(x - mid_x) / max(mid_x, 1)))
        y_limit = max(2, height - pinch)
        for y in range(-y_limit, y_limit + 1):
            nodes.add((x, y))
    return nodes


def build_skewed_nodes(width: int, height: int) -> set[tuple[int, int]]:
    nodes = build_rectangular_nodes(width, height)
    removed = {
        (x, y)
        for x, y in nodes
        if (x >= width - 2 and y >= height - 1) or (x <= 2 and y <= -height + 1)
    }
    return nodes - removed


def graph_neighbors(
    node: tuple[int, int],
    nodes: set[tuple[int, int]],
    wrap_y: bool = False,
) -> list[tuple[int, int]]:
    x, y = node
    offsets = (
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    if not wrap_y:
        return [
            (x + dx, y + dy)
            for dx, dy in offsets
            if (x + dx, y + dy) in nodes
        ]

    min_y = min(node_y for _x, node_y in nodes)
    max_y = max(node_y for _x, node_y in nodes)
    neighbors: set[tuple[int, int]] = set()
    for dx, dy in offsets:
        neighbor_x = x + dx
        neighbor_y = y + dy
        if wrap_y:
            if neighbor_y < min_y:
                neighbor_y = max_y
            elif neighbor_y > max_y:
                neighbor_y = min_y
        neighbor = (neighbor_x, neighbor_y)
        if neighbor in nodes:
            neighbors.add(neighbor)
    return sorted(neighbors)


def cluster_seed_builder(
    center: tuple[int, int],
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> frozenset[tuple[int, int]]:
    """A slightly richer local seed biased toward dense nearby directions."""

    neighbors = graph_neighbors(center, nodes, wrap_y=wrap_y)
    ranked_neighbors = sorted(
        neighbors,
        key=lambda neighbor: (-len(graph_neighbors(neighbor, nodes, wrap_y=wrap_y)), neighbor),
    )
    return frozenset([center, *ranked_neighbors[:2]])


def infer_arrival_times_from_source(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule: LocalRule,
    wrap_y: bool = False,
) -> dict[tuple[int, int], float]:
    node_field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    return infer_arrival_times_with_field(
        nodes,
        source,
        rule,
        node_field,
        wrap_y=wrap_y,
    )


def infer_arrival_times_with_field(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule: LocalRule,
    node_field: dict[tuple[int, int], float],
    wrap_y: bool = False,
) -> dict[tuple[int, int], float]:
    arrival_times: dict[tuple[int, int], float] = {source: 0.0}
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, source)]

    while frontier:
        current_time, node = heapq.heappop(frontier)
        if current_time != arrival_times[node]:
            continue

        for neighbor in graph_neighbors(node, nodes, wrap_y=wrap_y):
            local_delay, _action_increment, _amplitude = local_edge_properties(
                node,
                neighbor,
                rule,
                node_field,
            )
            neighbor_time = current_time + local_delay
            if neighbor_time < arrival_times.get(neighbor, math.inf):
                arrival_times[neighbor] = neighbor_time
                heapq.heappush(frontier, (neighbor_time, neighbor))

    return arrival_times


def build_causal_dag(
    nodes: set[tuple[int, int]],
    arrival_times: dict[tuple[int, int], float],
    wrap_y: bool = False,
    epsilon: float = 1e-9,
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    dag: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for node in nodes:
        if node not in arrival_times:
            continue
        dag[node] = [
            neighbor
            for neighbor in graph_neighbors(node, nodes, wrap_y=wrap_y)
            if neighbor in arrival_times
            and arrival_times[neighbor] > arrival_times[node] + epsilon
        ]
    return dag


def closest_value(values: list[int], target: float) -> int:
    return min(values, key=lambda value: (abs(value - target), value))


def select_target_rows(boundary_ys: list[int], center_y: float) -> list[int]:
    sorted_ys = sorted(boundary_ys)
    center = closest_value(sorted_ys, center_y)
    lower_candidates = [y for y in sorted_ys if y < center]
    upper_candidates = [y for y in sorted_ys if y > center]

    lower = lower_candidates[-1] if lower_candidates else sorted_ys[0]
    upper = upper_candidates[0] if upper_candidates else sorted_ys[-1]

    if lower == center and len(sorted_ys) >= 2:
        lower = sorted_ys[0]
    if upper == center and len(sorted_ys) >= 2:
        upper = sorted_ys[-1]

    selected = []
    for y in (lower, center, upper):
        if y not in selected:
            selected.append(y)

    if len(selected) < 3:
        for y in sorted_ys:
            if y not in selected:
                selected.append(y)
            if len(selected) == 3:
                break

    return sorted(selected)


def stationary_action_path_on_nodes(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    target: tuple[int, int],
    rule: LocalRule,
    wrap_y: bool = False,
) -> tuple[float, list[tuple[int, int]]]:
    node_field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    action_cost, previous = stationary_action_tree_on_nodes(
        nodes,
        source,
        rule,
        wrap_y=wrap_y,
        node_field=node_field,
    )
    path = reconstruct_path(source, target, previous)
    return action_cost[target], path


def stationary_action_tree_on_nodes(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule: LocalRule,
    wrap_y: bool = False,
    node_field: dict[tuple[int, int], float] | None = None,
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], tuple[int, int]]]:
    if node_field is None:
        node_field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    action_cost: dict[tuple[int, int], float] = {source: 0.0}
    previous: dict[tuple[int, int], tuple[int, int]] = {}
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, source)]

    while frontier:
        current_action, node = heapq.heappop(frontier)
        if current_action != action_cost[node]:
            continue

        for neighbor in graph_neighbors(node, nodes, wrap_y=wrap_y):
            _delay, action_increment, _amplitude = local_edge_properties(
                node,
                neighbor,
                rule,
                node_field,
            )
            neighbor_action = current_action + action_increment
            if neighbor_action < action_cost.get(neighbor, math.inf):
                action_cost[neighbor] = neighbor_action
                previous[neighbor] = node
                heapq.heappush(frontier, (neighbor_action, neighbor))

    return action_cost, previous


def reconstruct_path(
    source: tuple[int, int],
    target: tuple[int, int],
    previous: dict[tuple[int, int], tuple[int, int]],
) -> list[tuple[int, int]]:
    path = [target]
    current = target
    while current != source:
        current = previous[current]
        path.append(current)
    path.reverse()
    return path


def stationary_action_path(
    width: int,
    height: int,
    source: tuple[int, int],
    target: tuple[int, int],
    rule: LocalRule,
    blocked_nodes: frozenset[tuple[int, int]] = frozenset(),
) -> tuple[float, list[tuple[int, int]]]:
    nodes = build_rectangular_nodes(
        width=width,
        height=height,
        blocked_nodes=blocked_nodes,
    )
    return stationary_action_path_on_nodes(nodes, source, target, rule)


def compare_geodesics(
    width: int,
    height: int,
    source: tuple[int, int],
    target_ys: list[int],
    free_rule: LocalRule,
    distorted_rule: LocalRule,
) -> list[GeodesicComparison]:
    comparisons: list[GeodesicComparison] = []
    for target_y in target_ys:
        target = (width, target_y)
        free_action, free_path = stationary_action_path(
            width=width,
            height=height,
            source=source,
            target=target,
            rule=free_rule,
        )
        distorted_action, distorted_path = stationary_action_path(
            width=width,
            height=height,
            source=source,
            target=target,
            rule=distorted_rule,
        )
        comparisons.append(
            GeodesicComparison(
                target_y=target_y,
                free_action=free_action,
                distorted_action=distorted_action,
                free_path_y=str([y for _x, y in free_path]),
                distorted_path_y=str([y for _x, y in distorted_path]),
            )
        )
    return comparisons


def evaluate_rule_candidate(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    chosen_rule: RuleCandidate,
    postulates: RulePostulates,
) -> tuple[float, float, float, bool, str]:
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)

    distorted_rule = derive_local_rule(
        persistent_nodes=chosen_rule.persistent_nodes,
        postulates=postulates,
    )
    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=postulates,
    )
    field = derive_node_field(nodes, distorted_rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(field)
    source_y = closest_value(left_boundary_ys, centroid_y)
    target_ys = select_target_rows(right_boundary_ys, source_y)

    distorted_actions: list[tuple[int, float]] = []
    for target_y in target_ys:
        action, _path = stationary_action_path_on_nodes(
            nodes,
            source=(min_x, source_y),
            target=(max_x, target_y),
            rule=distorted_rule,
            wrap_y=wrap_y,
        )
        distorted_actions.append((target_y, action))

    center_target = min(target_ys, key=lambda y: (abs(y - source_y), y))
    center_action = next(action for y, action in distorted_actions if y == center_target)
    side_actions = [action for y, action in distorted_actions if y != center_target]
    center_gap = sum(side_actions) / len(side_actions) - center_action

    free_arrivals = infer_arrival_times_from_source(
        nodes,
        source=(min_x, source_y),
        rule=free_rule,
        wrap_y=wrap_y,
    )
    distorted_arrivals = infer_arrival_times_from_source(
        nodes,
        source=(min_x, source_y),
        rule=distorted_rule,
        wrap_y=wrap_y,
    )
    arrival_shifts = [
        distorted_arrivals[(max_x, y)] - free_arrivals[(max_x, y)]
        for y in right_boundary_ys
        if (max_x, y) in free_arrivals and (max_x, y) in distorted_arrivals
    ]
    arrival_span = max(arrival_shifts) - min(arrival_shifts)
    survived, status = classify_robustness(center_gap, arrival_span)
    return center_gap, arrival_span, centroid_y, survived, status


def robustness_rank(status: str) -> int:
    return {
        "survives": 3,
        "mixed": 2,
        "fragile": 1,
        "no pattern": 0,
    }[status]


def candidate_quality_key(
    candidate: RuleCandidate,
    metrics: tuple[float, float, float, bool, str],
) -> tuple[float, ...]:
    center_gap, arrival_span, _centroid_y, _survived, status = metrics
    return (
        robustness_rank(status),
        center_gap + arrival_span,
        arrival_span,
        center_gap,
        candidate.occupancy_mean,
        candidate.density,
    )


def quality_rescue_rule(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    postulates: RulePostulates,
    winner_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...] = WINNER_RULE_PAIRS,
) -> tuple[RuleCandidate | None, SearchDiagnostics, tuple[float, float, float, bool, str] | None]:
    """Search a small winner-rule set and choose by robustness quality, not just pattern compactness."""

    best_rule: RuleCandidate | None = None
    best_metrics: tuple[float, float, float, bool, str] | None = None
    best_key: tuple[float, ...] | None = None
    diagnostics_parts: list[SearchDiagnostics] = []

    for rule_pair in winner_rule_pairs:
        if rule_pair[0] not in count_options or rule_pair[1] not in count_options:
            continue
        candidate, diagnostics = scan_self_maintenance_rules(
            nodes,
            count_options=count_options,
            wrap_y=wrap_y,
            evolution_steps=10,
            sample_window=4,
            occupancy_threshold=0.6,
            min_component_fraction=0.7,
            exact_rule_pairs=(rule_pair,),
            preferred_rule_pairs=winner_rule_pairs,
            preferred_bonus=0.2,
            seed_builders=(point_seed_builder, cluster_seed_builder),
        )
        diagnostics_parts.append(diagnostics)
        if candidate is None:
            continue

        metrics = evaluate_rule_candidate(
            nodes,
            wrap_y=wrap_y,
            chosen_rule=candidate,
            postulates=postulates,
        )
        quality_key = candidate_quality_key(candidate, metrics)
        if best_key is None or quality_key > best_key:
            best_key = quality_key
            best_rule = candidate
            best_metrics = metrics

    if not diagnostics_parts:
        empty_diagnostics = SearchDiagnostics(
            total_trials=0,
            empty_patterns=0,
            disconnected_rejections=0,
            size_rejections=0,
            boundary_rejections=0,
            accepted_candidates=0,
            dominant_rejection="none",
        )
        return None, empty_diagnostics, None

    return best_rule, merge_search_diagnostics(*diagnostics_parts), best_metrics


def resolve_robust_rule_candidate(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    postulates: RulePostulates,
    selector_mode: str = "always_compare",
) -> tuple[
    RuleCandidate | None,
    SearchDiagnostics,
    tuple[float, float, float, bool, str] | None,
    bool,
]:
    chosen_rule, diagnostics = scan_self_maintenance_rules(
        nodes,
        count_options=count_options,
        wrap_y=wrap_y,
        evolution_steps=8,
        sample_window=3,
        occupancy_threshold=2 / 3,
        min_component_fraction=0.9,
        preferred_rule_pairs=WINNER_RULE_PAIRS,
        preferred_bonus=0.05,
        seed_builders=(point_seed_builder,),
    )
    fallback_used = False
    if chosen_rule is None:
        fallback_rule, fallback_diagnostics = scan_self_maintenance_rules(
            nodes,
            count_options=count_options,
            wrap_y=wrap_y,
            evolution_steps=10,
            sample_window=4,
            occupancy_threshold=0.6,
            min_component_fraction=0.7,
            preferred_rule_pairs=WINNER_RULE_PAIRS,
            preferred_bonus=0.08,
            seed_builders=(point_seed_builder, cluster_seed_builder),
        )
        diagnostics = merge_search_diagnostics(diagnostics, fallback_diagnostics)
        chosen_rule = fallback_rule
        fallback_used = chosen_rule is not None
    if chosen_rule is None:
        return None, diagnostics, None, False

    metrics = evaluate_rule_candidate(
        nodes,
        wrap_y=wrap_y,
        chosen_rule=chosen_rule,
        postulates=postulates,
    )
    _center_gap, _arrival_span, _centroid_y, _survived, status = metrics
    should_consult_rescue = (
        selector_mode == "always_compare"
        or (selector_mode == "gated" and status != "survives")
    )
    if should_consult_rescue:
        rescue_rule, rescue_diagnostics, rescue_metrics = quality_rescue_rule(
            nodes,
            wrap_y=wrap_y,
            count_options=count_options,
            postulates=postulates,
        )
        diagnostics = merge_search_diagnostics(diagnostics, rescue_diagnostics)
        if rescue_rule is not None and rescue_metrics is not None:
            rescue_key = candidate_quality_key(rescue_rule, rescue_metrics)
            current_key = candidate_quality_key(chosen_rule, metrics)
            if rescue_key > current_key:
                chosen_rule = rescue_rule
                metrics = rescue_metrics
                fallback_used = True

    return chosen_rule, diagnostics, metrics, fallback_used


def scan_self_maintaining_rules_fallback_only(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    postulates: RulePostulates,
) -> tuple[RuleCandidate | None, SearchDiagnostics]:
    del postulates
    return scan_self_maintenance_rules(
        nodes,
        count_options=SWEEP_COMPACT_COUNT_OPTIONS,
        wrap_y=wrap_y,
        evolution_steps=10,
        sample_window=4,
        occupancy_threshold=0.6,
        min_component_fraction=0.7,
        preferred_rule_pairs=WINNER_RULE_PAIRS,
        preferred_bonus=0.08,
        seed_builders=(point_seed_builder, cluster_seed_builder),
    )


def focused_skew_wrap_diagnosis(postulates: RulePostulates) -> list[FocusedComparison]:
    """Compare the legacy, repaired, minimal, and full compact families on skew-wrap."""

    nodes = build_skewed_nodes(6, 4)
    rows: list[FocusedComparison] = []

    legacy_rule, _legacy_diag, legacy_metrics = quality_rescue_rule(
        nodes,
        wrap_y=True,
        count_options=LEGACY_SWEEP_COMPACT_COUNT_OPTIONS,
        postulates=postulates,
    )
    if legacy_rule is not None and legacy_metrics is not None:
        rows.append(
            FocusedComparison(
                label="legacy reduced",
                rule_signature=format_rule_signature(
                    legacy_rule.survive_counts,
                    legacy_rule.birth_counts,
                ),
                center_gap=legacy_metrics[0],
                arrival_span=legacy_metrics[1],
                status=legacy_metrics[4],
            )
        )

    repaired_rule, _repaired_diag, repaired_metrics = quality_rescue_rule(
        nodes,
        wrap_y=True,
        count_options=REPAIRED_COMPACT_COUNT_OPTIONS,
        postulates=postulates,
    )
    if repaired_rule is not None and repaired_metrics is not None:
        rows.append(
            FocusedComparison(
                label="four-option repair",
                rule_signature=format_rule_signature(
                    repaired_rule.survive_counts,
                    repaired_rule.birth_counts,
                ),
                center_gap=repaired_metrics[0],
                arrival_span=repaired_metrics[1],
                status=repaired_metrics[4],
            )
        )

    minimal_rule, _minimal_diag, minimal_metrics = quality_rescue_rule(
        nodes,
        wrap_y=True,
        count_options=SWEEP_COMPACT_COUNT_OPTIONS,
        postulates=postulates,
    )
    if minimal_rule is not None and minimal_metrics is not None:
        rows.append(
            FocusedComparison(
                label="minimal three",
                rule_signature=format_rule_signature(
                    minimal_rule.survive_counts,
                    minimal_rule.birth_counts,
                ),
                center_gap=minimal_metrics[0],
                arrival_span=minimal_metrics[1],
                status=minimal_metrics[4],
            )
        )

    full_rule, _full_diag, full_metrics = quality_rescue_rule(
        nodes,
        wrap_y=True,
        count_options=COMPACT_COUNT_OPTIONS,
        postulates=postulates,
    )
    if full_rule is not None and full_metrics is not None:
        rows.append(
            FocusedComparison(
                label="compact full",
                rule_signature=format_rule_signature(
                    full_rule.survive_counts,
                    full_rule.birth_counts,
                ),
                center_gap=full_metrics[0],
                arrival_span=full_metrics[1],
                status=full_metrics[4],
            )
        )

    return rows


def evaluate_robustness_scenario(
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    rule_family: str,
    postulates: RulePostulates,
) -> RobustnessResult:
    chosen_rule, diagnostics, metrics, fallback_used = resolve_robust_rule_candidate(
        nodes,
        wrap_y=wrap_y,
        count_options=count_options,
        postulates=postulates,
    )
    if chosen_rule is None or metrics is None:
        return RobustnessResult(
            scenario_name=scenario_name,
            rule_family=rule_family,
            seed_node=(-1, -1),
            rule_signature="-",
            rule_breadth=0,
            fallback_used=False,
            persistent_nodes=0,
            center_gap=float("nan"),
            arrival_span=float("nan"),
            centroid_y=float("nan"),
            occupancy_mean=float("nan"),
            density=float("nan"),
            total_trials=diagnostics.total_trials,
            empty_patterns=diagnostics.empty_patterns,
            disconnected_rejections=diagnostics.disconnected_rejections,
            size_rejections=diagnostics.size_rejections,
            boundary_rejections=diagnostics.boundary_rejections,
            accepted_candidates=diagnostics.accepted_candidates,
            dominant_rejection=diagnostics.dominant_rejection,
            survived=False,
            status="no pattern",
        )
    center_gap, arrival_span, centroid_y, survived, status = metrics

    return RobustnessResult(
        scenario_name=scenario_name,
        rule_family=rule_family,
        seed_node=chosen_rule.seed_node,
        rule_signature=format_rule_signature(
            chosen_rule.survive_counts,
            chosen_rule.birth_counts,
        ),
        rule_breadth=len(chosen_rule.survive_counts) + len(chosen_rule.birth_counts),
        fallback_used=fallback_used,
        persistent_nodes=len(chosen_rule.persistent_nodes),
        center_gap=center_gap,
        arrival_span=arrival_span,
        centroid_y=centroid_y,
        occupancy_mean=chosen_rule.occupancy_mean,
        density=chosen_rule.density,
        total_trials=diagnostics.total_trials,
        empty_patterns=diagnostics.empty_patterns,
        disconnected_rejections=diagnostics.disconnected_rejections,
        size_rejections=diagnostics.size_rejections,
        boundary_rejections=diagnostics.boundary_rejections,
        accepted_candidates=diagnostics.accepted_candidates,
        dominant_rejection=diagnostics.dominant_rejection,
        survived=survived,
        status=status,
    )


def robustness_scenarios() -> tuple[tuple[str, set[tuple[int, int]], bool], ...]:
    return (
        ("rect-hard", build_rectangular_nodes(6, 4), False),
        ("rect-wrap", build_rectangular_nodes(6, 4), True),
        ("taper-hard", build_tapered_nodes(6, 4), False),
        ("taper-wrap", build_tapered_nodes(6, 4), True),
        ("skew-hard", build_skewed_nodes(6, 4), False),
        ("skew-wrap", build_skewed_nodes(6, 4), True),
    )


def mirrored_nodes(nodes: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return {(x, -y) for x, y in nodes}


def benchmark_packs() -> tuple[tuple[str, tuple[tuple[str, set[tuple[int, int]], bool], ...]], ...]:
    return (
        ("base", robustness_scenarios()),
        (
            "large",
            (
                ("rect-wrap-large", build_rectangular_nodes(8, 5), True),
                ("taper-hard-large", build_tapered_nodes(8, 5), False),
                ("taper-wrap-large", build_tapered_nodes(8, 5), True),
                ("skew-wrap-large", build_skewed_nodes(8, 5), True),
            ),
        ),
        (
            "mirror",
            (
                ("skew-hard-mirror", mirrored_nodes(build_skewed_nodes(6, 4)), False),
                ("skew-wrap-mirror", mirrored_nodes(build_skewed_nodes(6, 4)), True),
                ("rect-hard-large", build_rectangular_nodes(8, 5), False),
            ),
        ),
    )


def perturbation_graph_center(nodes: set[tuple[int, int]]) -> tuple[float, float]:
    xs = [x for x, _y in nodes]
    ys = [y for _x, y in nodes]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)


def removable_perturbation_nodes(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> list[tuple[int, int]]:
    protected_nodes = outer_boundary_nodes(nodes)
    removable_nodes: list[tuple[int, int]] = []
    for node in sorted(nodes):
        if node in protected_nodes:
            continue
        perturbed_nodes = set(nodes)
        perturbed_nodes.remove(node)
        if len(connected_components(frozenset(perturbed_nodes), perturbed_nodes, wrap_y=wrap_y)) == 1:
            removable_nodes.append(node)
    return removable_nodes


def addable_perturbation_nodes(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> list[tuple[int, int]]:
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    min_y = min(y for _x, y in nodes)
    max_y = max(y for _x, y in nodes)
    addable_nodes: list[tuple[int, int]] = []
    for x in range(min_x + 1, max_x):
        for y in range(min_y + 1, max_y):
            candidate = (x, y)
            if candidate in nodes:
                continue
            augmented_nodes = set(nodes)
            augmented_nodes.add(candidate)
            if len(graph_neighbors(candidate, augmented_nodes, wrap_y=wrap_y)) >= 4:
                addable_nodes.append(candidate)
    return addable_nodes


def deterministic_topology_perturbations(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> tuple[tuple[str, set[tuple[int, int]], int], ...]:
    center_x, center_y = perturbation_graph_center(nodes)
    removable_nodes = removable_perturbation_nodes(nodes, wrap_y)
    addable_nodes = addable_perturbation_nodes(nodes, wrap_y)

    def center_remove_key(node: tuple[int, int]) -> tuple[float, float, int, int]:
        return (
            (node[0] - center_x) ** 2 + (node[1] - center_y) ** 2,
            abs(node[1] - center_y),
            node[0],
            node[1],
        )

    def upper_remove_key(node: tuple[int, int]) -> tuple[float, float, int, int]:
        return (
            -float(node[1]),
            abs(node[0] - center_x),
            (node[0] - center_x) ** 2 + (node[1] - center_y) ** 2,
            node[0],
        )

    def lower_remove_key(node: tuple[int, int]) -> tuple[float, float, int, int]:
        return (
            float(node[1]),
            abs(node[0] - center_x),
            (node[0] - center_x) ** 2 + (node[1] - center_y) ** 2,
            node[0],
        )

    def pocket_add_key(node: tuple[int, int]) -> tuple[float, float, int, int]:
        augmented_nodes = set(nodes)
        augmented_nodes.add(node)
        return (
            -float(len(graph_neighbors(node, augmented_nodes, wrap_y=wrap_y))),
            (node[0] - center_x) ** 2 + (node[1] - center_y) ** 2,
            node[0],
            node[1],
        )

    variants: list[tuple[str, set[tuple[int, int]], int]] = []
    if removable_nodes:
        center_remove = min(removable_nodes, key=center_remove_key)
        upper_remove = min(removable_nodes, key=upper_remove_key)
        lower_remove = min(removable_nodes, key=lower_remove_key)
        variants.append(("center-punch", set(nodes) - {center_remove}, -1))
        if addable_nodes:
            pocket_add = min(addable_nodes, key=pocket_add_key)
            variants.append(
                (
                    "center-shift",
                    (set(nodes) - {center_remove}) | {pocket_add},
                    0,
                )
            )
        variants.extend(
            (
                ("upper-punch", set(nodes) - {upper_remove}, -1),
                ("lower-punch", set(nodes) - {lower_remove}, -1),
            )
        )

    deduped_variants: list[tuple[str, set[tuple[int, int]], int]] = []
    seen_node_sets: set[frozenset[tuple[int, int]]] = set()
    for variant_name, perturbed_nodes, node_delta in variants:
        identity = frozenset(perturbed_nodes)
        if identity in seen_node_sets:
            continue
        seen_node_sets.add(identity)
        deduped_variants.append((variant_name, perturbed_nodes, node_delta))
    return tuple(deduped_variants[:2])


def stable_random_seed(*parts: str) -> int:
    seed = 0
    for part in parts:
        for character in part:
            seed = ((seed * 131) + ord(character)) % (2**32)
    return seed


def random_topology_perturbations(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    variant_limit: int = 2,
) -> tuple[tuple[str, set[tuple[int, int]], int], ...]:
    removable_nodes = removable_perturbation_nodes(nodes, wrap_y)
    addable_nodes = addable_perturbation_nodes(nodes, wrap_y)
    if not removable_nodes:
        return ()

    rng = random.Random(
        stable_random_seed(
            pack_name,
            scenario_name,
            "wrap" if wrap_y else "hard",
        )
    )
    shuffled_removals = list(removable_nodes)
    rng.shuffle(shuffled_removals)
    shuffled_additions = list(addable_nodes)
    rng.shuffle(shuffled_additions)

    variants: list[tuple[str, set[tuple[int, int]], int]] = []
    removal_index = 0
    addition_index = 0
    variant_index = 0
    while len(variants) < variant_limit and removal_index < len(shuffled_removals):
        remove_node = shuffled_removals[removal_index]
        variants.append(
            (
                f"random-punch-{chr(ord('a') + variant_index)}",
                set(nodes) - {remove_node},
                -1,
            )
        )
        removal_index += 1
        variant_index += 1
        if len(variants) >= variant_limit:
            break
        if addition_index < len(shuffled_additions):
            shift_remove = (
                shuffled_removals[removal_index]
                if removal_index < len(shuffled_removals)
                else remove_node
            )
            variants.append(
                (
                    f"random-shift-{chr(ord('a') + addition_index)}",
                    (set(nodes) - {shift_remove}) | {shuffled_additions[addition_index]},
                    0,
                )
            )
            addition_index += 1
            if removal_index < len(shuffled_removals):
                removal_index += 1
        elif removal_index < len(shuffled_removals):
            variants.append(
                (
                    f"random-punch-{chr(ord('a') + variant_index)}",
                    set(nodes) - {shuffled_removals[removal_index]},
                    -1,
                )
            )
            removal_index += 1
        variant_index += 1

    deduped_variants: list[tuple[str, set[tuple[int, int]], int]] = []
    seen_node_sets: set[frozenset[tuple[int, int]]] = set()
    for variant_name, perturbed_nodes, node_delta in variants:
        identity = frozenset(perturbed_nodes)
        if identity in seen_node_sets:
            continue
        seen_node_sets.add(identity)
        deduped_variants.append((variant_name, perturbed_nodes, node_delta))
    return tuple(deduped_variants)


def column_interval_profile(
    nodes: set[tuple[int, int]],
) -> dict[int, tuple[int, int]]:
    return {
        x: (
            min(y for node_x, y in nodes if node_x == x),
            max(y for node_x, y in nodes if node_x == x),
        )
        for x in sorted({x for x, _y in nodes})
    }


def build_nodes_from_interval_profile(
    profile: dict[int, tuple[int, int]],
) -> set[tuple[int, int]]:
    return {
        (x, y)
        for x, (low_y, high_y) in profile.items()
        for y in range(low_y, high_y + 1)
    }


def randomized_geometry_variants(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    variant_limit: int = 2,
) -> tuple[tuple[str, set[tuple[int, int]], int], ...]:
    del wrap_y  # geometry generation itself is independent of wrap mode
    base_profile = column_interval_profile(nodes)
    xs = sorted(base_profile)
    base_spans = [high_y - low_y for low_y, high_y in base_profile.values()]
    min_span = max(4, min(base_spans) - 1)
    max_shift = 2 if max(base_spans) >= 8 else 1

    deduped_variants: list[tuple[str, set[tuple[int, int]], int]] = []
    seen_node_sets: set[frozenset[tuple[int, int]]] = {frozenset(nodes)}

    for attempt_index in range(variant_limit * 6):
        rng = random.Random(
            stable_random_seed(
                pack_name,
                scenario_name,
                "geometry",
                str(attempt_index),
            )
        )
        new_profile: dict[int, tuple[int, int]] = {}
        prev_center_delta = 0
        prev_span_delta = 0

        for x in xs:
            base_low, base_high = base_profile[x]
            base_center = (base_low + base_high) / 2
            base_span = base_high - base_low

            prev_center_delta = max(
                -max_shift,
                min(max_shift, prev_center_delta + rng.choice((-1, 0, 1))),
            )
            prev_span_delta = max(
                -1,
                min(1, prev_span_delta + rng.choice((-1, 0, 1))),
            )

            new_center = base_center + prev_center_delta
            new_span = max(min_span, base_span + prev_span_delta)
            low_y = math.floor(new_center - new_span / 2)
            high_y = low_y + new_span

            if new_profile:
                prev_x = xs[xs.index(x) - 1]
                prev_low, prev_high = new_profile[prev_x]
                if low_y > prev_high + 1:
                    shift = low_y - (prev_high + 1)
                    low_y -= shift
                    high_y -= shift
                if high_y < prev_low - 1:
                    shift = (prev_low - 1) - high_y
                    low_y += shift
                    high_y += shift

            new_profile[x] = (low_y, high_y)

        perturbed_nodes = build_nodes_from_interval_profile(new_profile)
        identity = frozenset(perturbed_nodes)
        if identity in seen_node_sets:
            continue
        if len(connected_components(identity, perturbed_nodes, wrap_y=False)) != 1:
            continue
        seen_node_sets.add(identity)
        variant_name = f"geometry-{chr(ord('a') + len(deduped_variants))}"
        deduped_variants.append(
            (
                variant_name,
                perturbed_nodes,
                len(perturbed_nodes) - len(nodes),
            )
        )
        if len(deduped_variants) >= variant_limit:
            break

    return tuple(deduped_variants)


def procedural_geometry_variants(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    variant_limit: int = 2,
) -> tuple[tuple[str, set[tuple[int, int]], int], ...]:
    del wrap_y  # profile generation itself is independent of wrap mode
    xs = sorted({x for x, _y in nodes})
    min_y = min(y for _x, y in nodes)
    max_y = max(y for _x, y in nodes)
    full_span = max_y - min_y
    min_span = max(4, full_span - 2)
    max_span = max(min_span, full_span + 1)
    low_floor = min_y - 1
    high_ceiling = max_y + 1
    max_center_shift = max(1, (high_ceiling - low_floor) // 4)

    deduped_variants: list[tuple[str, set[tuple[int, int]], int]] = []
    seen_node_sets: set[frozenset[tuple[int, int]]] = {frozenset(nodes)}

    for attempt_index in range(variant_limit * 8):
        rng = random.Random(
            stable_random_seed(
                pack_name,
                scenario_name,
                "procedural-geometry",
                str(attempt_index),
            )
        )
        profile: dict[int, tuple[int, int]] = {}
        center_shift = rng.randint(-1, 1)
        span = rng.randint(min_span, max_span)

        for index, x in enumerate(xs):
            if index > 0:
                center_shift = max(
                    -max_center_shift,
                    min(max_center_shift, center_shift + rng.choice((-1, 0, 1))),
                )
                span = max(
                    min_span,
                    min(max_span, span + rng.choice((-1, 0, 1))),
                )

            center = center_shift + rng.choice((0.0, 0.0, -0.5, 0.5))
            low_y = math.floor(center - span / 2)
            high_y = low_y + span

            if low_y < low_floor:
                shift = low_floor - low_y
                low_y += shift
                high_y += shift
            if high_y > high_ceiling:
                shift = high_y - high_ceiling
                low_y -= shift
                high_y -= shift

            if index > 0:
                prev_low, prev_high = profile[xs[index - 1]]
                if low_y > prev_high + 1:
                    shift = low_y - (prev_high + 1)
                    low_y -= shift
                    high_y -= shift
                if high_y < prev_low - 1:
                    shift = (prev_low - 1) - high_y
                    low_y += shift
                    high_y += shift

            profile[x] = (low_y, high_y)

        perturbed_nodes = build_nodes_from_interval_profile(profile)
        identity = frozenset(perturbed_nodes)
        if identity in seen_node_sets:
            continue
        if len(connected_components(identity, perturbed_nodes, wrap_y=False)) != 1:
            continue
        seen_node_sets.add(identity)
        variant_name = f"procedural-{chr(ord('a') + len(deduped_variants))}"
        deduped_variants.append(
            (
                variant_name,
                perturbed_nodes,
                len(perturbed_nodes) - len(nodes),
            )
        )
        if len(deduped_variants) >= variant_limit:
            break

    return tuple(deduped_variants)


def column_profile_geometry_metrics(
    nodes: set[tuple[int, int]],
) -> tuple[float, float, float, bool, int]:
    profile = column_interval_profile(nodes)
    xs = sorted(profile)
    centers = [(profile[x][0] + profile[x][1]) / 2 for x in xs]
    spans = [profile[x][1] - profile[x][0] for x in xs]
    mean_center = sum(centers) / len(centers)
    center_range = max(centers) - min(centers)
    center_total_variation = sum(
        abs(centers[index + 1] - centers[index])
        for index in range(len(centers) - 1)
    )
    crosses_midline = min(centers) < 0.0 < max(centers)
    span_range = max(spans) - min(spans)
    return (
        mean_center,
        center_range,
        center_total_variation,
        crosses_midline,
        span_range,
    )


def ordered_profile_centers_and_spans(
    nodes: set[tuple[int, int]],
) -> tuple[tuple[int, ...], tuple[float, ...], tuple[int, ...]]:
    profile = column_interval_profile(nodes)
    xs = tuple(sorted(profile))
    centers = tuple((profile[x][0] + profile[x][1]) / 2 for x in xs)
    spans = tuple(profile[x][1] - profile[x][0] for x in xs)
    return xs, centers, spans


def build_profile_from_centers_and_spans(
    xs: tuple[int, ...],
    centers: tuple[float, ...],
    spans: tuple[int, ...],
) -> dict[int, tuple[int, int]]:
    profile: dict[int, tuple[int, int]] = {}
    for index, x in enumerate(xs):
        center = centers[index]
        span = spans[index]
        low_y = math.floor(center - span / 2)
        high_y = low_y + span
        if index > 0:
            prev_low, prev_high = profile[xs[index - 1]]
            if low_y > prev_high + 1:
                shift = low_y - (prev_high + 1)
                low_y -= shift
                high_y -= shift
            if high_y < prev_low - 1:
                shift = (prev_low - 1) - high_y
                low_y += shift
                high_y += shift
        profile[x] = (low_y, high_y)
    return profile


def run_family_sweep(
    count_options: tuple[frozenset[int], ...],
    rule_family: str,
    postulates: RulePostulates,
) -> list[RobustnessResult]:
    results: list[RobustnessResult] = []
    for scenario_name, nodes, wrap_y in robustness_scenarios():
        results.append(
            evaluate_robustness_scenario(
                scenario_name=scenario_name,
                nodes=nodes,
                wrap_y=wrap_y,
                count_options=count_options,
                rule_family=rule_family,
                postulates=postulates,
            )
        )
    return results


def run_robustness_sweep(postulates: RulePostulates) -> list[RobustnessResult]:
    rule_families = (
        ("compact", SWEEP_COMPACT_COUNT_OPTIONS),
        ("extended", SWEEP_EXTENDED_COUNT_OPTIONS),
    )

    results: list[RobustnessResult] = []
    for rule_family, count_options in rule_families:
        results.extend(
            run_family_sweep(
                count_options=count_options,
                rule_family=rule_family,
                postulates=postulates,
            )
        )
    return results


def derive_motif_preserving_compact_subset(
    postulates: RulePostulates,
) -> tuple[tuple[frozenset[int], ...], list[RobustnessResult]]:
    hard_rows: list[RobustnessResult] = []
    required_counts: set[frozenset[int]] = set()

    for scenario_name, nodes, wrap_y in robustness_scenarios():
        if not scenario_name.startswith("skew"):
            continue
        row = evaluate_robustness_scenario(
            scenario_name=scenario_name,
            nodes=nodes,
            wrap_y=wrap_y,
            count_options=COMPACT_COUNT_OPTIONS,
            rule_family="compact full",
            postulates=postulates,
        )
        hard_rows.append(row)
        survive_counts, birth_counts = parse_rule_signature(row.rule_signature)
        required_counts.update((survive_counts, birth_counts))

    subset = tuple(sorted(required_counts, key=count_option_sort_key))
    return subset, hard_rows


def derive_smallest_surviving_subset(
    candidate_options: tuple[frozenset[int], ...],
    postulates: RulePostulates,
) -> tuple[tuple[frozenset[int], ...], list[RobustnessResult]]:
    for size in range(1, len(candidate_options) + 1):
        for subset in itertools.combinations(candidate_options, size):
            rows = run_family_sweep(subset, "compact minimal", postulates)
            if all(row.status == "survives" for row in rows):
                return tuple(sorted(subset, key=count_option_sort_key)), rows
    raise RuntimeError("No surviving compact subset found inside the candidate family.")


def ablate_compact_subset(
    count_options: tuple[frozenset[int], ...],
    postulates: RulePostulates,
) -> list[AblationResult]:
    rows: list[AblationResult] = []
    for removed_option in count_options:
        ablated = tuple(option for option in count_options if option != removed_option)
        sweep_rows = run_family_sweep(ablated, "compact ablation", postulates)
        failed_rows = [row for row in sweep_rows if row.status != "survives"]
        rows.append(
            AblationResult(
                removed_option=format_single_count_option(removed_option),
                survives=sum(row.status == "survives" for row in sweep_rows),
                mixed=sum(row.status == "mixed" for row in sweep_rows),
                fragile=sum(row.status == "fragile" for row in sweep_rows),
                no_pattern=sum(row.status == "no pattern" for row in sweep_rows),
                failed_scenarios=", ".join(
                    f"{row.scenario_name}:{row.status}"
                    for row in failed_rows
                )
                or "-",
            )
        )
    return rows


def mechanism_ablation_results() -> list[MechanismAblationResult]:
    variants = (
        ("baseline", "spent_delay", "relaxed"),
        ("coordinate-delay action", "coordinate_delay", "relaxed"),
        ("link-length action", "link_length", "relaxed"),
        ("support-only field", "spent_delay", "support_only"),
        ("no field", "spent_delay", "none"),
    )

    rows: list[MechanismAblationResult] = []
    for label, action_mode, field_mode in variants:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode=action_mode,
            field_mode=field_mode,
        )
        sweep_rows = run_family_sweep(SWEEP_COMPACT_COUNT_OPTIONS, label, postulates)
        failed_rows = [row for row in sweep_rows if row.status != "survives"]
        rows.append(
            MechanismAblationResult(
                label=label,
                action_mode=action_mode,
                field_mode=field_mode,
                survives=sum(row.status == "survives" for row in sweep_rows),
                mixed=sum(row.status == "mixed" for row in sweep_rows),
                fragile=sum(row.status == "fragile" for row in sweep_rows),
                no_pattern=sum(row.status == "no pattern" for row in sweep_rows),
                avg_center_gap=sum(row.center_gap for row in sweep_rows) / len(sweep_rows),
                avg_arrival_span=sum(row.arrival_span for row in sweep_rows) / len(sweep_rows),
                failed_scenarios=", ".join(
                    f"{row.scenario_name}:{row.status}"
                    for row in failed_rows
                )
                or "-",
            )
        )
    return rows


def average_side_path_response(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    chosen_rule: RuleCandidate,
    postulates: RulePostulates,
) -> float:
    distorted_rule = derive_local_rule(
        persistent_nodes=chosen_rule.persistent_nodes,
        postulates=postulates,
    )
    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=postulates,
    )
    distorted_field = derive_node_field(nodes, distorted_rule, wrap_y=wrap_y)
    free_field = derive_node_field(nodes, free_rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(distorted_field)
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)
    source_y = closest_value(left_boundary_ys, centroid_y)
    target_ys = select_target_rows(right_boundary_ys, source_y)
    center_target = min(target_ys, key=lambda y: (abs(y - source_y), y))
    _free_costs, free_previous = stationary_action_tree_on_nodes(
        nodes,
        source=(min_x, source_y),
        rule=free_rule,
        wrap_y=wrap_y,
        node_field=free_field,
    )
    _distorted_costs, distorted_previous = stationary_action_tree_on_nodes(
        nodes,
        source=(min_x, source_y),
        rule=distorted_rule,
        wrap_y=wrap_y,
        node_field=distorted_field,
    )

    responses: list[float] = []
    for target_y in target_ys:
        if target_y == center_target:
            continue
        free_path = reconstruct_path(
            (min_x, source_y),
            (max_x, target_y),
            free_previous,
        )
        distorted_path = reconstruct_path(
            (min_x, source_y),
            (max_x, target_y),
            distorted_previous,
        )
        free_path_y = {x: y for x, y in free_path}
        distorted_path_y = {x: y for x, y in distorted_path}
        all_xs = sorted(set(free_path_y) | set(distorted_path_y))
        responses.append(
            sum(
                abs(distorted_path_y.get(x, free_path_y.get(x, 0)) - free_path_y.get(x, 0))
                for x in all_xs
            )
        )

    return sum(responses) / len(responses)


def action_discriminator_results() -> list[ActionDiscriminatorResult]:
    variants = (
        ("baseline", "spent_delay", "relaxed"),
        ("coordinate-delay action", "coordinate_delay", "relaxed"),
        ("link-length action", "link_length", "relaxed"),
        ("support-only field", "spent_delay", "support_only"),
        ("no field", "spent_delay", "none"),
    )

    rows: list[ActionDiscriminatorResult] = []
    for label, action_mode, field_mode in variants:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode=action_mode,
            field_mode=field_mode,
        )
        responses: list[tuple[str, float, bool]] = []
        statuses: list[str] = []
        failed_scenarios: list[str] = []
        for scenario_name, nodes, wrap_y in robustness_scenarios():
            chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
                nodes,
                wrap_y=wrap_y,
                count_options=SWEEP_COMPACT_COUNT_OPTIONS,
                postulates=postulates,
            )
            if chosen_rule is None or metrics is None:
                statuses.append("no pattern")
                failed_scenarios.append(f"{scenario_name}:no pattern")
                responses.append((scenario_name, 0.0, wrap_y))
                continue

            _center_gap, _arrival_span, _centroid_y, _survived, status = metrics
            statuses.append(status)
            if status != "survives":
                failed_scenarios.append(f"{scenario_name}:{status}")
            responses.append(
                (
                    scenario_name,
                    average_side_path_response(
                        nodes,
                        wrap_y=wrap_y,
                        chosen_rule=chosen_rule,
                        postulates=postulates,
                    ),
                    wrap_y,
                )
            )

        rows.append(
            ActionDiscriminatorResult(
                label=label,
                survives=sum(status == "survives" for status in statuses),
                min_response=min(response for _name, response, _wrap in responses),
                min_wrapped_response=min(
                    response for _name, response, wrap in responses if wrap
                ),
                failed_scenarios=", ".join(failed_scenarios) or "-",
            )
        )
    return rows


def action_family_results(
    retained_weights: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> list[ActionFamilyResult]:
    rows: list[ActionFamilyResult] = []
    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        sweep_rows = run_family_sweep(
            SWEEP_COMPACT_COUNT_OPTIONS,
            f"retained={retained_weight:.2f}",
            postulates,
        )
        responses: list[tuple[float, bool]] = []
        for scenario_name, nodes, wrap_y in robustness_scenarios():
            chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
                nodes,
                wrap_y=wrap_y,
                count_options=SWEEP_COMPACT_COUNT_OPTIONS,
                postulates=postulates,
            )
            if chosen_rule is None or metrics is None:
                responses.append((0.0, wrap_y))
                continue
            responses.append(
                (
                    average_side_path_response(
                        nodes,
                        wrap_y=wrap_y,
                        chosen_rule=chosen_rule,
                        postulates=postulates,
                    ),
                    wrap_y,
                )
            )

        rows.append(
            ActionFamilyResult(
                retained_weight=retained_weight,
                survives=sum(row.status == "survives" for row in sweep_rows),
                mixed=sum(row.status == "mixed" for row in sweep_rows),
                fragile=sum(row.status == "fragile" for row in sweep_rows),
                no_pattern=sum(row.status == "no pattern" for row in sweep_rows),
                avg_center_gap=sum(row.center_gap for row in sweep_rows) / len(sweep_rows),
                avg_arrival_span=sum(row.arrival_span for row in sweep_rows) / len(sweep_rows),
                min_response=min(response for response, _wrap in responses),
                min_wrapped_response=min(
                    response for response, wrap in responses if wrap
                ),
            )
        )
    return rows


def action_family_pack_results(
    retained_weights: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> list[ActionPackResult]:
    rows: list[ActionPackResult] = []
    for pack_name, scenarios in benchmark_packs():
        for retained_weight in retained_weights:
            postulates = RulePostulates(
                phase_per_action=4.0,
                attenuation_power=1.0,
                action_mode="retained_mix",
                field_mode="relaxed",
                action_retained_weight=retained_weight,
            )
            statuses: list[str] = []
            responses: list[tuple[float, bool]] = []
            for _scenario_name, nodes, wrap_y in scenarios:
                chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
                    nodes,
                    wrap_y=wrap_y,
                    count_options=SWEEP_COMPACT_COUNT_OPTIONS,
                    postulates=postulates,
                )
                if chosen_rule is None or metrics is None:
                    statuses.append("no pattern")
                    responses.append((0.0, wrap_y))
                    continue
                statuses.append(metrics[4])
                responses.append(
                    (
                        average_side_path_response(
                            nodes,
                            wrap_y=wrap_y,
                            chosen_rule=chosen_rule,
                            postulates=postulates,
                        ),
                        wrap_y,
                    )
                )

            min_response = min(response for response, _wrap in responses)
            min_wrapped_response = min(
                response for response, wrap in responses if wrap
            )
            rows.append(
                ActionPackResult(
                    pack_name=pack_name,
                    retained_weight=retained_weight,
                    survives=sum(status == "survives" for status in statuses),
                    mixed=sum(status == "mixed" for status in statuses),
                    fragile=sum(status == "fragile" for status in statuses),
                    no_pattern=sum(status == "no pattern" for status in statuses),
                    min_response=min_response,
                    min_wrapped_response=min_wrapped_response,
                    pack_pass=(
                        all(status == "survives" for status in statuses)
                        and min_wrapped_response > 0.0
                    ),
                )
            )
    return rows


def path_delay_total(
    path: list[tuple[int, int]],
    rule: LocalRule,
    node_field: dict[tuple[int, int], float],
) -> float:
    total_delay = 0.0
    for start, end in zip(path, path[1:]):
        delay, _action_increment, _amplitude = local_edge_properties(
            start,
            end,
            rule,
            node_field,
        )
        total_delay += delay
    return total_delay


def path_retained_total(
    path: list[tuple[int, int]],
    rule: LocalRule,
    node_field: dict[tuple[int, int], float],
) -> float:
    total_retained = 0.0
    for start, end in zip(path, path[1:]):
        delay, _action_increment, _amplitude = local_edge_properties(
            start,
            end,
            rule,
            node_field,
        )
        link_length = math.dist(start, end)
        total_retained += math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    return total_retained


def all_off_center_targets(boundary_ys: list[int], source_y: int) -> list[int]:
    return [y for y in sorted(boundary_ys) if y != source_y]


def scenario_by_name(
    pack_name: str,
    scenario_name: str,
) -> tuple[set[tuple[int, int]], bool]:
    for current_pack_name, scenarios in benchmark_packs():
        if current_pack_name != pack_name:
            continue
        for current_scenario_name, nodes, wrap_y in scenarios:
            if current_scenario_name == scenario_name:
                return nodes, wrap_y
    raise KeyError(f"Unknown benchmark scenario: {pack_name}:{scenario_name}")


def scenario_target_margins(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    chosen_rule: RuleCandidate,
    postulates: RulePostulates,
) -> list[CriticalWeightCase]:
    distorted_rule = derive_local_rule(
        persistent_nodes=chosen_rule.persistent_nodes,
        postulates=postulates,
    )
    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=postulates,
    )
    distorted_field = derive_node_field(nodes, distorted_rule, wrap_y=wrap_y)
    free_field = derive_node_field(nodes, free_rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(distorted_field)
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)
    source_y = closest_value(left_boundary_ys, centroid_y)

    free_costs, free_previous = stationary_action_tree_on_nodes(
        nodes,
        source=(min_x, source_y),
        rule=free_rule,
        wrap_y=wrap_y,
        node_field=free_field,
    )
    distorted_costs, distorted_previous = stationary_action_tree_on_nodes(
        nodes,
        source=(min_x, source_y),
        rule=distorted_rule,
        wrap_y=wrap_y,
        node_field=distorted_field,
    )

    rows: list[CriticalWeightCase] = []
    for target_y in all_off_center_targets(right_boundary_ys, source_y):
        free_action = free_costs[(max_x, target_y)]
        distorted_action = distorted_costs[(max_x, target_y)]
        free_path = reconstruct_path(
            (min_x, source_y),
            (max_x, target_y),
            free_previous,
        )
        distorted_path = reconstruct_path(
            (min_x, source_y),
            (max_x, target_y),
            distorted_previous,
        )
        free_delay = path_delay_total(free_path, free_rule, free_field)
        distorted_delay = path_delay_total(
            distorted_path,
            distorted_rule,
            distorted_field,
        )
        retained_total = path_retained_total(
            distorted_path,
            distorted_rule,
            distorted_field,
        )
        delay_penalty = distorted_delay - free_delay
        rows.append(
            CriticalWeightCase(
                pack_name="",
                scenario_name="",
                target_y=target_y,
                critical_weight=(
                    (2.0 * delay_penalty / retained_total)
                    if retained_total > 0.0
                    else math.inf
                ),
                margin_at_one=retained_total - 2.0 * delay_penalty,
                delay_penalty=delay_penalty,
                retained_total=retained_total,
            )
        )
    return rows


def minimum_proper_time_margin(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    chosen_rule: RuleCandidate,
    postulates: RulePostulates,
) -> tuple[float, float]:
    margins = [
        row.margin_at_one
        + (postulates.action_retained_weight - 1.0) * row.retained_total
        for row in scenario_target_margins(
            nodes,
            wrap_y,
            chosen_rule,
            postulates,
        )
    ]
    scenario_min_margin = min(margins)
    return scenario_min_margin, scenario_min_margin


def proper_time_consistency_results(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[ProperTimeConsistencyResult]:
    rows: list[ProperTimeConsistencyResult] = []
    total_scenarios = sum(len(scenarios) for _pack_name, scenarios in benchmark_packs())
    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        survives = 0
        worst_case = ""
        min_margin = math.inf
        min_wrapped_margin = math.inf

        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
                    nodes,
                    wrap_y=wrap_y,
                    count_options=SWEEP_COMPACT_COUNT_OPTIONS,
                    postulates=postulates,
                )
                if chosen_rule is None or metrics is None or metrics[4] != "survives":
                    worst_case = f"{pack_name}:{scenario_name}:no pattern"
                    min_margin = -math.inf
                    if wrap_y:
                        min_wrapped_margin = -math.inf
                    continue

                survives += 1
                scenario_min_margin, scenario_min_wrapped_margin = minimum_proper_time_margin(
                    nodes,
                    wrap_y=wrap_y,
                    chosen_rule=chosen_rule,
                    postulates=postulates,
                )
                if scenario_min_margin < min_margin:
                    min_margin = scenario_min_margin
                    worst_case = f"{pack_name}:{scenario_name}"
                if wrap_y:
                    min_wrapped_margin = min(min_wrapped_margin, scenario_min_wrapped_margin)

        rows.append(
            ProperTimeConsistencyResult(
                retained_weight=retained_weight,
                survives=survives,
                min_margin=min_margin,
                min_wrapped_margin=min_wrapped_margin,
                worst_case=worst_case or "-",
                pass_all=(
                    survives == total_scenarios
                    and min_margin > 0.0
                    and min_wrapped_margin > 0.0
                ),
            )
        )
    return rows


def critical_weight_cases(
    retained_weight: float = 1.0,
) -> list[CriticalWeightCase]:
    postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
        action_mode="retained_mix",
        field_mode="relaxed",
        action_retained_weight=retained_weight,
    )
    rows: list[CriticalWeightCase] = []

    for pack_name, scenarios in benchmark_packs():
        for scenario_name, nodes, wrap_y in scenarios:
            chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
                nodes,
                wrap_y=wrap_y,
                count_options=SWEEP_COMPACT_COUNT_OPTIONS,
                postulates=postulates,
            )
            if chosen_rule is None or metrics is None or metrics[4] != "survives":
                continue

            for target_row in scenario_target_margins(
                nodes,
                wrap_y,
                chosen_rule,
                postulates,
            ):
                rows.append(
                    CriticalWeightCase(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        target_y=target_row.target_y,
                        critical_weight=target_row.critical_weight,
                        margin_at_one=target_row.margin_at_one,
                        delay_penalty=target_row.delay_penalty,
                        retained_total=target_row.retained_total,
                    )
                )
    return sorted(
        rows,
        key=lambda row: (
            row.critical_weight,
            row.delay_penalty,
            row.retained_total,
            row.pack_name,
            row.scenario_name,
            row.target_y,
        ),
        reverse=True,
    )


def weight_branch_scan(
    pack_name: str,
    scenario_name: str,
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[WeightBranchScanRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    rows: list[WeightBranchScanRow] = []

    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        chosen_rule, _diagnostics, metrics, _fallback_used = resolve_robust_rule_candidate(
            nodes,
            wrap_y=wrap_y,
            count_options=SWEEP_COMPACT_COUNT_OPTIONS,
            postulates=postulates,
        )
        if chosen_rule is None or metrics is None or metrics[4] != "survives":
            rows.append(
                WeightBranchScanRow(
                    retained_weight=retained_weight,
                    rule_signature="no pattern",
                    source_y=0,
                    worst_target_y=0,
                    min_margin=-math.inf,
                    critical_weight=math.inf,
                )
            )
            continue

        distorted_rule = derive_local_rule(
            persistent_nodes=chosen_rule.persistent_nodes,
            postulates=postulates,
        )
        distorted_field = derive_node_field(nodes, distorted_rule, wrap_y=wrap_y)
        _centroid_x, centroid_y = field_centroid(distorted_field)
        min_x = min(x for x, _y in nodes)
        left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
        source_y = closest_value(left_boundary_ys, centroid_y)
        target_rows = scenario_target_margins(
            nodes,
            wrap_y,
            chosen_rule,
            postulates,
        )
        worst_target_row = min(
            target_rows,
            key=lambda row: (row.margin_at_one + (retained_weight - 1.0) * row.retained_total, row.target_y),
        )
        rows.append(
            WeightBranchScanRow(
                retained_weight=retained_weight,
                rule_signature=format_rule_signature(
                    chosen_rule.survive_counts,
                    chosen_rule.birth_counts,
                ),
                source_y=source_y,
                worst_target_y=worst_target_row.target_y,
                min_margin=worst_target_row.margin_at_one
                + (retained_weight - 1.0) * worst_target_row.retained_total,
                critical_weight=worst_target_row.critical_weight,
            )
        )

    return rows


def rule_selection_diagnostics(
    pack_name: str,
    scenario_name: str,
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[RuleSelectionDiagnosticRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    rows: list[RuleSelectionDiagnosticRow] = []

    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        fallback_rule, _fallback_diag = scan_self_maintaining_rules_fallback_only(
            nodes,
            wrap_y,
            postulates,
        )
        rescue_rule, _rescue_diag, rescue_metrics = quality_rescue_rule(
            nodes,
            wrap_y,
            SWEEP_COMPACT_COUNT_OPTIONS,
            postulates,
        )
        final_rule, _diag, final_metrics, _fallback_used = resolve_robust_rule_candidate(
            nodes,
            wrap_y,
            SWEEP_COMPACT_COUNT_OPTIONS,
            postulates,
        )

        fallback_metrics = (
            evaluate_rule_candidate(nodes, wrap_y, fallback_rule, postulates)
            if fallback_rule is not None
            else None
        )
        rows.append(
            RuleSelectionDiagnosticRow(
                retained_weight=retained_weight,
                fallback_rule=(
                    format_rule_signature(
                        fallback_rule.survive_counts,
                        fallback_rule.birth_counts,
                    )
                    if fallback_rule is not None
                    else "none"
                ),
                fallback_center_gap=(
                    fallback_metrics[0] if fallback_metrics is not None else float("nan")
                ),
                fallback_arrival_span=(
                    fallback_metrics[1] if fallback_metrics is not None else float("nan")
                ),
                fallback_status=(
                    fallback_metrics[4] if fallback_metrics is not None else "no pattern"
                ),
                rescue_rule=(
                    format_rule_signature(
                        rescue_rule.survive_counts,
                        rescue_rule.birth_counts,
                    )
                    if rescue_rule is not None
                    else "none"
                ),
                rescue_center_gap=(
                    rescue_metrics[0] if rescue_metrics is not None else float("nan")
                ),
                rescue_arrival_span=(
                    rescue_metrics[1] if rescue_metrics is not None else float("nan")
                ),
                rescue_status=(
                    rescue_metrics[4] if rescue_metrics is not None else "no pattern"
                ),
                final_rule=(
                    format_rule_signature(
                        final_rule.survive_counts,
                        final_rule.birth_counts,
                    )
                    if final_rule is not None
                    else "none"
                ),
                switched=(
                    final_rule is not None
                    and fallback_rule is not None
                    and (
                        final_rule.survive_counts != fallback_rule.survive_counts
                        or final_rule.birth_counts != fallback_rule.birth_counts
                    )
                ),
            )
        )

    return rows


def fixed_branch_competition(
    pack_name: str,
    scenario_name: str,
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[FixedBranchCompetitionRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    baseline_postulates = RulePostulates(phase_per_action=4.0)
    fallback_candidate, _fallback_diag = scan_self_maintaining_rules_fallback_only(
        nodes,
        wrap_y,
        baseline_postulates,
    )
    rescue_candidate, _rescue_diag, _rescue_metrics = quality_rescue_rule(
        nodes,
        wrap_y,
        SWEEP_COMPACT_COUNT_OPTIONS,
        RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=1.0,
        ),
    )

    candidates = [
        ("fallback-fixed", fallback_candidate),
        ("rescue-fixed", rescue_candidate),
    ]
    rows: list[FixedBranchCompetitionRow] = []

    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        for branch_label, candidate in candidates:
            if candidate is None:
                rows.append(
                    FixedBranchCompetitionRow(
                        retained_weight=retained_weight,
                        branch_label=branch_label,
                        rule_signature="none",
                        center_gap=float("nan"),
                        arrival_span=float("nan"),
                        status="no pattern",
                        min_margin=float("nan"),
                    )
                )
                continue

            metrics = evaluate_rule_candidate(
                nodes,
                wrap_y,
                candidate,
                postulates,
            )
            min_margin, _min_wrapped = minimum_proper_time_margin(
                nodes,
                wrap_y,
                candidate,
                postulates,
            )
            rows.append(
                FixedBranchCompetitionRow(
                    retained_weight=retained_weight,
                    branch_label=branch_label,
                    rule_signature=format_rule_signature(
                        candidate.survive_counts,
                        candidate.birth_counts,
                    ),
                    center_gap=metrics[0],
                    arrival_span=metrics[1],
                    status=metrics[4],
                    min_margin=min_margin,
                )
            )

    return rows


def center_gap_path_summary(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    candidate: RuleCandidate,
    postulates: RulePostulates,
) -> tuple[int, float, float, float, tuple[tuple[int, ...], ...]]:
    rule = derive_local_rule(
        persistent_nodes=candidate.persistent_nodes,
        postulates=postulates,
    )
    field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(field)
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)
    source_y = closest_value(left_boundary_ys, centroid_y)
    target_ys = select_target_rows(right_boundary_ys, source_y)
    center_target = min(target_ys, key=lambda y: (abs(y - source_y), y))

    actions: list[tuple[int, float]] = []
    path_shapes: list[tuple[int, ...]] = []
    for target_y in target_ys:
        action, path = stationary_action_path_on_nodes(
            nodes,
            source=(min_x, source_y),
            target=(max_x, target_y),
            rule=rule,
            wrap_y=wrap_y,
        )
        actions.append((target_y, action))
        path_shapes.append(tuple(y for _x, y in path))

    center_action = next(action for target_y, action in actions if target_y == center_target)
    side_actions = [action for target_y, action in actions if target_y != center_target]
    side_average = sum(side_actions) / len(side_actions)
    return (
        source_y,
        center_action,
        side_average,
        side_average - center_action,
        tuple(path_shapes),
    )


def geometric_focus_summary(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    candidate: RuleCandidate,
    postulates: RulePostulates,
) -> tuple[int, float, float, float, tuple[tuple[int, ...], ...]]:
    rule = derive_local_rule(
        persistent_nodes=candidate.persistent_nodes,
        postulates=postulates,
    )
    field = derive_node_field(nodes, rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(field)
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)
    source_y = closest_value(left_boundary_ys, centroid_y)
    target_ys = select_target_rows(right_boundary_ys, source_y)
    center_target = min(target_ys, key=lambda y: (abs(y - source_y), y))

    path_distances: list[tuple[int, float]] = []
    path_shapes: list[tuple[int, ...]] = []
    for target_y in target_ys:
        _action, path = stationary_action_path_on_nodes(
            nodes,
            source=(min_x, source_y),
            target=(max_x, target_y),
            rule=rule,
            wrap_y=wrap_y,
        )
        path_shapes.append(tuple(y for _x, y in path))
        path_distances.append(
            (
                target_y,
                sum(abs(y - centroid_y) for _x, y in path) / len(path),
            )
        )

    center_distance = next(distance for target_y, distance in path_distances if target_y == center_target)
    side_average = sum(distance for target_y, distance in path_distances if target_y != center_target) / 2
    return (
        source_y,
        center_distance,
        side_average,
        side_average - center_distance,
        tuple(path_shapes),
    )


def center_gap_geometry_diagnostics(
    pack_name: str,
    scenario_name: str,
    start_weight: float = 0.75,
    end_weight: float = 1.0,
) -> list[CenterGapGeometryRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    baseline_postulates = RulePostulates(phase_per_action=4.0)
    fallback_candidate, _fallback_diag = scan_self_maintaining_rules_fallback_only(
        nodes,
        wrap_y,
        baseline_postulates,
    )
    rescue_candidate, _rescue_diag, _rescue_metrics = quality_rescue_rule(
        nodes,
        wrap_y,
        SWEEP_COMPACT_COUNT_OPTIONS,
        RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=end_weight,
        ),
    )

    rows: list[CenterGapGeometryRow] = []
    for branch_label, candidate in (
        ("fallback-fixed", fallback_candidate),
        ("rescue-fixed", rescue_candidate),
    ):
        if candidate is None:
            continue
        start_postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=start_weight,
        )
        end_postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=end_weight,
        )
        start_summary = center_gap_path_summary(
            nodes,
            wrap_y,
            candidate,
            start_postulates,
        )
        end_summary = center_gap_path_summary(
            nodes,
            wrap_y,
            candidate,
            end_postulates,
        )
        rows.append(
            CenterGapGeometryRow(
                branch_label=branch_label,
                rule_signature=format_rule_signature(
                    candidate.survive_counts,
                    candidate.birth_counts,
                ),
                source_y_start=start_summary[0],
                source_y_end=end_summary[0],
                stable_paths=start_summary[4] == end_summary[4],
                center_action_start=start_summary[1],
                center_action_end=end_summary[1],
                side_avg_start=start_summary[2],
                side_avg_end=end_summary[2],
                gap_start=start_summary[3],
                gap_end=end_summary[3],
            )
        )

    return rows


def focus_metric_comparison(
    pack_name: str,
    scenario_name: str,
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[FocusMetricComparisonRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    baseline_postulates = RulePostulates(phase_per_action=4.0)
    fallback_candidate, _fallback_diag = scan_self_maintaining_rules_fallback_only(
        nodes,
        wrap_y,
        baseline_postulates,
    )
    rescue_candidate, _rescue_diag, _rescue_metrics = quality_rescue_rule(
        nodes,
        wrap_y,
        SWEEP_COMPACT_COUNT_OPTIONS,
        RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=1.0,
        ),
    )
    rows: list[FocusMetricComparisonRow] = []

    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        fallback_action = center_gap_path_summary(nodes, wrap_y, fallback_candidate, postulates)
        rescue_action = center_gap_path_summary(nodes, wrap_y, rescue_candidate, postulates)
        fallback_geom = geometric_focus_summary(nodes, wrap_y, fallback_candidate, postulates)
        rescue_geom = geometric_focus_summary(nodes, wrap_y, rescue_candidate, postulates)
        fallback_stiffness = (
            fallback_action[3] / fallback_geom[3]
            if fallback_geom[3] != 0.0
            else math.inf
        )
        rescue_stiffness = (
            rescue_action[3] / rescue_geom[3]
            if rescue_geom[3] != 0.0
            else math.inf
        )
        rows.append(
            FocusMetricComparisonRow(
                retained_weight=retained_weight,
                fallback_action_gap=fallback_action[3],
                rescue_action_gap=rescue_action[3],
                fallback_geometric_gap=fallback_geom[3],
                rescue_geometric_gap=rescue_geom[3],
                fallback_stiffness=fallback_stiffness,
                rescue_stiffness=rescue_stiffness,
                action_winner=(
                    "rescue"
                    if rescue_action[3] > fallback_action[3]
                    else "fallback"
                ),
                geometric_winner=(
                    "rescue"
                    if rescue_geom[3] > fallback_geom[3]
                    else "fallback"
                ),
                stiffness_winner=(
                    "rescue"
                    if rescue_stiffness > fallback_stiffness
                    else "fallback"
                ),
            )
        )

    return rows


def selector_policy_diagnostics(
    pack_name: str,
    scenario_name: str,
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[SelectorPolicyRow]:
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    rows: list[SelectorPolicyRow] = []
    for retained_weight in retained_weights:
        postulates = RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
            action_mode="retained_mix",
            field_mode="relaxed",
            action_retained_weight=retained_weight,
        )
        fallback_rule, _fallback_diag = scan_self_maintaining_rules_fallback_only(
            nodes,
            wrap_y,
            postulates,
        )
        fallback_metrics = evaluate_rule_candidate(nodes, wrap_y, fallback_rule, postulates)
        rescue_rule, _rescue_diag, rescue_metrics = quality_rescue_rule(
            nodes,
            wrap_y,
            SWEEP_COMPACT_COUNT_OPTIONS,
            postulates,
        )
        gated_rule, _diag, _metrics, _fallback_used = resolve_robust_rule_candidate(
            nodes,
            wrap_y,
            SWEEP_COMPACT_COUNT_OPTIONS,
            postulates,
            selector_mode="gated",
        )
        ungated_rule, _diag2, _metrics2, _fallback_used2 = resolve_robust_rule_candidate(
            nodes,
            wrap_y,
            SWEEP_COMPACT_COUNT_OPTIONS,
            postulates,
            selector_mode="always_compare",
        )

        fallback_quality = fallback_metrics[0] + fallback_metrics[1]
        rescue_quality = rescue_metrics[0] + rescue_metrics[1]
        rows.append(
            SelectorPolicyRow(
                retained_weight=retained_weight,
                fallback_rule=format_rule_signature(
                    fallback_rule.survive_counts,
                    fallback_rule.birth_counts,
                ),
                fallback_status=fallback_metrics[4],
                fallback_quality=fallback_quality,
                rescue_rule=format_rule_signature(
                    rescue_rule.survive_counts,
                    rescue_rule.birth_counts,
                ),
                rescue_status=rescue_metrics[4],
                rescue_quality=rescue_quality,
                gated_final_rule=format_rule_signature(
                    gated_rule.survive_counts,
                    gated_rule.birth_counts,
                ),
                ungated_final_rule=format_rule_signature(
                    ungated_rule.survive_counts,
                    ungated_rule.birth_counts,
                ),
                differs=(
                    gated_rule.survive_counts != ungated_rule.survive_counts
                    or gated_rule.birth_counts != ungated_rule.birth_counts
                ),
            )
        )

    return rows


def selector_policy_sweep_cases(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> list[SelectorSweepCase]:
    rows: list[SelectorSweepCase] = []
    for pack_name, scenarios in benchmark_packs():
        for scenario_name, nodes, wrap_y in scenarios:
            for retained_weight in retained_weights:
                postulates = RulePostulates(
                    phase_per_action=4.0,
                    attenuation_power=1.0,
                    action_mode="retained_mix",
                    field_mode="relaxed",
                    action_retained_weight=retained_weight,
                )
                gated_rule, _diag, gated_metrics, _fallback_used = resolve_robust_rule_candidate(
                    nodes,
                    wrap_y,
                    SWEEP_COMPACT_COUNT_OPTIONS,
                    postulates,
                    selector_mode="gated",
                )
                ungated_rule, _diag2, ungated_metrics, _fallback_used2 = resolve_robust_rule_candidate(
                    nodes,
                    wrap_y,
                    SWEEP_COMPACT_COUNT_OPTIONS,
                    postulates,
                    selector_mode="always_compare",
                )
                rows.append(
                    SelectorSweepCase(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        retained_weight=retained_weight,
                        gated_rule=(
                            format_rule_signature(gated_rule.survive_counts, gated_rule.birth_counts)
                            if gated_rule is not None
                            else "none"
                        ),
                        gated_status=(gated_metrics[4] if gated_metrics is not None else "no pattern"),
                        ungated_rule=(
                            format_rule_signature(ungated_rule.survive_counts, ungated_rule.birth_counts)
                            if ungated_rule is not None
                            else "none"
                        ),
                        ungated_status=(ungated_metrics[4] if ungated_metrics is not None else "no pattern"),
                        differs=(
                            gated_rule is None
                            or ungated_rule is None
                            or gated_rule.survive_counts != ungated_rule.survive_counts
                            or gated_rule.birth_counts != ungated_rule.birth_counts
                            or (gated_metrics is not None and ungated_metrics is not None and gated_metrics[4] != ungated_metrics[4])
                        ),
                    )
                )
    return rows


def merge_candidate_sources(
    current_sources: str,
    new_source: str,
) -> str:
    source_parts = set(filter(None, current_sources.split("+"))) if current_sources else set()
    source_parts.update(filter(None, new_source.split("+")))
    return "+".join(sorted(source_parts))


def family_count_options() -> tuple[tuple[str, tuple[frozenset[int], ...]], ...]:
    return (
        ("compact", SWEEP_COMPACT_COUNT_OPTIONS),
        ("extended", SWEEP_EXTENDED_COUNT_OPTIONS),
    )


def build_frontier_evaluation_cache(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
) -> FrontierEvaluationCache:
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    free_rule = LocalRule(
        persistent_nodes=frozenset(),
        phase_wavenumber=4.0,
        field_mode="relaxed",
    )
    return FrontierEvaluationCache(
        min_x=min_x,
        max_x=max_x,
        left_boundary_ys=tuple(sorted(y for x, y in nodes if x == min_x)),
        right_boundary_ys=tuple(sorted(y for x, y in nodes if x == max_x)),
        free_field=derive_node_field(nodes, free_rule, wrap_y=wrap_y),
    )


def frontier_candidate_profile(
    candidate: RuleCandidate,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    evaluation_cache: FrontierEvaluationCache,
) -> FrontierCandidateProfile:
    identity = candidate_identity_key(candidate)
    cached_profile = evaluation_cache.candidate_profiles.get(identity)
    if cached_profile is not None:
        return cached_profile

    distorted_rule = LocalRule(
        persistent_nodes=candidate.persistent_nodes,
        phase_wavenumber=4.0,
        field_mode="relaxed",
    )
    field = derive_node_field(nodes, distorted_rule, wrap_y=wrap_y)
    _centroid_x, centroid_y = field_centroid(field)
    source_y = closest_value(list(evaluation_cache.left_boundary_ys), centroid_y)
    target_ys = tuple(select_target_rows(list(evaluation_cache.right_boundary_ys), source_y))
    center_target = min(target_ys, key=lambda y: (abs(y - source_y), y))
    distorted_arrivals = infer_arrival_times_with_field(
        nodes,
        source=(evaluation_cache.min_x, source_y),
        rule=distorted_rule,
        node_field=field,
        wrap_y=wrap_y,
    )
    profile = FrontierCandidateProfile(
        field=field,
        centroid_y=centroid_y,
        source_y=source_y,
        target_ys=target_ys,
        center_target=center_target,
        distorted_arrivals=distorted_arrivals,
    )
    evaluation_cache.candidate_profiles[identity] = profile
    return profile


def frontier_free_arrivals(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    source_y: int,
    evaluation_cache: FrontierEvaluationCache,
) -> dict[tuple[int, int], float]:
    cached_arrivals = evaluation_cache.free_arrivals_by_source.get(source_y)
    if cached_arrivals is not None:
        return cached_arrivals

    free_rule = LocalRule(
        persistent_nodes=frozenset(),
        phase_wavenumber=4.0,
        field_mode="relaxed",
    )
    arrivals = infer_arrival_times_with_field(
        nodes,
        source=(evaluation_cache.min_x, source_y),
        rule=free_rule,
        node_field=evaluation_cache.free_field,
        wrap_y=wrap_y,
    )
    evaluation_cache.free_arrivals_by_source[source_y] = arrivals
    return arrivals


def frontier_free_action_tree(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    source_y: int,
    postulates: RulePostulates,
    evaluation_cache: FrontierEvaluationCache,
) -> tuple[
    dict[tuple[int, int], float],
    dict[tuple[int, int], tuple[int, int]],
]:
    cache_key = (source_y, postulates.action_retained_weight)
    cached_tree = evaluation_cache.free_action_trees.get(cache_key)
    if cached_tree is not None:
        return cached_tree

    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=postulates,
    )
    action_tree = stationary_action_tree_on_nodes(
        nodes,
        source=(evaluation_cache.min_x, source_y),
        rule=free_rule,
        wrap_y=wrap_y,
        node_field=evaluation_cache.free_field,
    )
    evaluation_cache.free_action_trees[cache_key] = action_tree
    return action_tree


def frontier_distorted_action_tree(
    candidate: RuleCandidate,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    postulates: RulePostulates,
    profile: FrontierCandidateProfile,
    evaluation_cache: FrontierEvaluationCache,
) -> tuple[
    dict[tuple[int, int], float],
    dict[tuple[int, int], tuple[int, int]],
]:
    identity = candidate_identity_key(candidate)
    cache_key = (identity, postulates.action_retained_weight)
    cached_tree = evaluation_cache.distorted_action_trees.get(cache_key)
    if cached_tree is not None:
        return cached_tree

    distorted_rule = derive_local_rule(
        persistent_nodes=candidate.persistent_nodes,
        postulates=postulates,
    )
    action_tree = stationary_action_tree_on_nodes(
        nodes,
        source=(evaluation_cache.min_x, profile.source_y),
        rule=distorted_rule,
        wrap_y=wrap_y,
        node_field=profile.field,
    )
    evaluation_cache.distorted_action_trees[cache_key] = action_tree
    return action_tree


def frontier_metric_snapshot(
    candidate: RuleCandidate,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    postulates: RulePostulates,
    evaluation_cache: FrontierEvaluationCache,
) -> FrontierMetricSnapshot:
    identity = candidate_identity_key(candidate)
    cache_key = (identity, postulates.action_retained_weight)
    cached_snapshot = evaluation_cache.metric_snapshots.get(cache_key)
    if cached_snapshot is not None:
        return cached_snapshot

    profile = frontier_candidate_profile(
        candidate,
        nodes,
        wrap_y,
        evaluation_cache,
    )
    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=postulates,
    )
    distorted_rule = derive_local_rule(
        persistent_nodes=candidate.persistent_nodes,
        postulates=postulates,
    )
    free_arrivals = frontier_free_arrivals(
        nodes,
        wrap_y,
        profile.source_y,
        evaluation_cache,
    )
    free_costs, free_previous = frontier_free_action_tree(
        nodes,
        wrap_y,
        profile.source_y,
        postulates,
        evaluation_cache,
    )
    distorted_costs, distorted_previous = frontier_distorted_action_tree(
        candidate,
        nodes,
        wrap_y,
        postulates,
        profile,
        evaluation_cache,
    )

    center_action = distorted_costs[(evaluation_cache.max_x, profile.center_target)]
    side_actions = [
        distorted_costs[(evaluation_cache.max_x, target_y)]
        for target_y in profile.target_ys
        if target_y != profile.center_target
    ]
    center_gap = sum(side_actions) / len(side_actions) - center_action

    arrival_shifts = [
        profile.distorted_arrivals[(evaluation_cache.max_x, y)] - free_arrivals[(evaluation_cache.max_x, y)]
        for y in evaluation_cache.right_boundary_ys
        if (evaluation_cache.max_x, y) in free_arrivals
        and (evaluation_cache.max_x, y) in profile.distorted_arrivals
    ]
    arrival_span = max(arrival_shifts) - min(arrival_shifts)
    _survived, status = classify_robustness(center_gap, arrival_span)

    path_distances: list[tuple[int, float]] = []
    for target_y in profile.target_ys:
        path = reconstruct_path(
            (evaluation_cache.min_x, profile.source_y),
            (evaluation_cache.max_x, target_y),
            distorted_previous,
        )
        path_distances.append(
            (
                target_y,
                sum(abs(y - profile.centroid_y) for _x, y in path) / len(path),
            )
        )

    center_distance = next(
        distance
        for target_y, distance in path_distances
        if target_y == profile.center_target
    )
    side_average = (
        sum(distance for target_y, distance in path_distances if target_y != profile.center_target)
        / len(side_actions)
    )
    geometric_focus_gap = side_average - center_distance

    margins: list[float] = []
    for target_y in all_off_center_targets(list(evaluation_cache.right_boundary_ys), profile.source_y):
        free_path = reconstruct_path(
            (evaluation_cache.min_x, profile.source_y),
            (evaluation_cache.max_x, target_y),
            free_previous,
        )
        distorted_path = reconstruct_path(
            (evaluation_cache.min_x, profile.source_y),
            (evaluation_cache.max_x, target_y),
            distorted_previous,
        )
        free_delay = path_delay_total(
            free_path,
            free_rule,
            evaluation_cache.free_field,
        )
        distorted_delay = path_delay_total(
            distorted_path,
            distorted_rule,
            profile.field,
        )
        retained_total = path_retained_total(
            distorted_path,
            distorted_rule,
            profile.field,
        )
        margins.append(
            postulates.action_retained_weight * retained_total
            - 2.0 * (distorted_delay - free_delay)
        )
    min_margin = min(margins)
    stiffness = center_gap / geometric_focus_gap if geometric_focus_gap != 0.0 else math.inf
    snapshot = FrontierMetricSnapshot(
        centroid_y=profile.centroid_y,
        center_gap=center_gap,
        arrival_span=arrival_span,
        status=status,
        status_rank=robustness_rank(status),
        min_margin=min_margin,
        min_wrapped_margin=min_margin,
        geometric_focus_gap=geometric_focus_gap,
        stiffness=stiffness,
    )
    evaluation_cache.metric_snapshots[cache_key] = snapshot
    return snapshot


def build_frontier_postulates(retained_weight: float) -> RulePostulates:
    return RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
        action_mode="retained_mix",
        field_mode="relaxed",
        action_retained_weight=retained_weight,
    )


def evaluate_frontier_candidate(
    candidate: RuleCandidate,
    rule_family: str,
    pack_name: str,
    scenario_name: str,
    retained_weight: float,
    search_sources: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    postulates: RulePostulates,
    current_selected: bool,
    evaluation_cache: FrontierEvaluationCache | None = None,
) -> EvaluatedCandidate:
    if evaluation_cache is None:
        center_gap, arrival_span, centroid_y, _survived, status = evaluate_rule_candidate(
            nodes,
            wrap_y,
            candidate,
            postulates,
        )
        min_margin, min_wrapped_margin = minimum_proper_time_margin(
            nodes,
            wrap_y,
            candidate,
            postulates,
        )
        _source_y, _center_distance, _side_average, geometric_focus_gap, _path_shapes = geometric_focus_summary(
            nodes,
            wrap_y,
            candidate,
            postulates,
        )
        stiffness = center_gap / geometric_focus_gap if geometric_focus_gap != 0.0 else math.inf
        status_rank = robustness_rank(status)
    else:
        snapshot = frontier_metric_snapshot(
            candidate,
            nodes,
            wrap_y,
            postulates,
            evaluation_cache,
        )
        center_gap = snapshot.center_gap
        arrival_span = snapshot.arrival_span
        centroid_y = snapshot.centroid_y
        status = snapshot.status
        status_rank = snapshot.status_rank
        min_margin = snapshot.min_margin
        min_wrapped_margin = snapshot.min_wrapped_margin
        geometric_focus_gap = snapshot.geometric_focus_gap
        stiffness = snapshot.stiffness
    focus_score = focus_observable_score(center_gap, arrival_span, "box-min")
    return EvaluatedCandidate(
        rule_family=rule_family,
        pack_name=pack_name,
        scenario_name=scenario_name,
        retained_weight=retained_weight,
        candidate_identity=candidate_identity_key(candidate),
        search_sources=search_sources,
        seed_node=candidate.seed_node,
        survive_counts=candidate.survive_counts,
        birth_counts=candidate.birth_counts,
        rule_signature=format_rule_signature(
            candidate.survive_counts,
            candidate.birth_counts,
        ),
        persistent_nodes=len(candidate.persistent_nodes),
        occupancy_mean=candidate.occupancy_mean,
        density=candidate.density,
        center_gap=center_gap,
        arrival_span=arrival_span,
        centroid_y=centroid_y,
        status=status,
        status_rank=status_rank,
        min_margin=min_margin,
        min_wrapped_margin=min_wrapped_margin,
        geometric_focus_gap=geometric_focus_gap,
        stiffness=stiffness,
        focus_score=focus_score,
        current_selected=current_selected,
    )


def frontier_axes(
    ranking_mode: str = "bucketed",
) -> dict[str, tuple[str, ...]]:
    primary_axis = "status_rank" if ranking_mode == "bucketed" else "focus_score"
    return {
        "robustness": (primary_axis, "center_gap", "arrival_span"),
        "proper_time": (primary_axis, "min_margin", "min_wrapped_margin"),
        "geometry": (primary_axis, "geometric_focus_gap"),
        "mixed": (primary_axis, "arrival_span", "stiffness", "min_wrapped_margin"),
    }


def dominates_candidate(
    left: EvaluatedCandidate,
    right: EvaluatedCandidate,
    axes: tuple[str, ...],
) -> bool:
    left_values = [getattr(left, axis) for axis in axes]
    right_values = [getattr(right, axis) for axis in axes]
    return all(left_value >= right_value for left_value, right_value in zip(left_values, right_values)) and any(
        left_value > right_value for left_value, right_value in zip(left_values, right_values)
    )


def pareto_frontier_identities(
    candidates: list[EvaluatedCandidate],
    axes: tuple[str, ...],
) -> set[
    tuple[
        frozenset[int],
        frozenset[int],
        frozenset[tuple[int, int]],
    ]
]:
    frontier: set[
        tuple[
            frozenset[int],
            frozenset[int],
            frozenset[tuple[int, int]],
        ]
    ] = set()
    for candidate in candidates:
        if any(
            dominates_candidate(other_candidate, candidate, axes)
            for other_candidate in candidates
            if other_candidate.candidate_identity != candidate.candidate_identity
        ):
            continue
        frontier.add(candidate.candidate_identity)
    return frontier


def format_frontier_rule_signatures(
    candidates: list[EvaluatedCandidate],
) -> str:
    signatures = sorted({candidate.rule_signature for candidate in candidates})
    return ", ".join(signatures) if signatures else "-"


def collect_raw_frontier_pool(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
) -> RawFrontierPool:
    xs = [x for x, _y in nodes]
    ys = [y for _x, y in nodes]
    graph_center = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    pooled_candidates: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        RuleCandidate,
    ] = {}
    candidate_sources: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        str,
    ] = {}

    search_specs = (
        (
            "primary",
            dict(
                evolution_steps=8,
                sample_window=3,
                occupancy_threshold=2 / 3,
                min_component_fraction=0.9,
                preferred_rule_pairs=WINNER_RULE_PAIRS,
                preferred_bonus=0.05,
                seed_builders=(point_seed_builder,),
            ),
        ),
        (
            "fallback",
            dict(
                evolution_steps=10,
                sample_window=4,
                occupancy_threshold=0.6,
                min_component_fraction=0.7,
                preferred_rule_pairs=WINNER_RULE_PAIRS,
                preferred_bonus=0.08,
                seed_builders=(point_seed_builder, cluster_seed_builder),
            ),
        ),
    )

    primary_best_identity = None
    fallback_best_identity = None
    rescue_identity_list: list[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]]
    ] = []
    winner_signatures = {
        format_rule_signature(survive_counts, birth_counts)
        for survive_counts, birth_counts in WINNER_RULE_PAIRS
        if survive_counts in count_options and birth_counts in count_options
    }

    for source_label, search_kwargs in search_specs:
        collected_candidates, _diagnostics = collect_self_maintenance_candidates(
            nodes,
            count_options=count_options,
            wrap_y=wrap_y,
            **search_kwargs,
        )
        if collected_candidates:
            best_identity = candidate_identity_key(collected_candidates[0])
            if source_label == "primary":
                primary_best_identity = best_identity
            else:
                fallback_best_identity = best_identity
        for candidate in collected_candidates:
            identity = candidate_identity_key(candidate)
            if identity not in pooled_candidates:
                pooled_candidates[identity] = candidate
                candidate_sources[identity] = source_label
            else:
                candidate_sources[identity] = merge_candidate_sources(
                    candidate_sources[identity],
                    source_label,
                )

    present_rule_signatures = {
        format_rule_signature(candidate.survive_counts, candidate.birth_counts)
        for candidate in pooled_candidates.values()
    }
    for survive_counts, birth_counts in WINNER_RULE_PAIRS:
        if survive_counts not in count_options or birth_counts not in count_options:
            continue
        winner_signature = format_rule_signature(survive_counts, birth_counts)
        if winner_signature in present_rule_signatures:
            continue
        exact_candidates, _diagnostics = collect_self_maintenance_candidates(
            nodes,
            count_options=count_options,
            wrap_y=wrap_y,
            evolution_steps=10,
            sample_window=4,
            occupancy_threshold=0.6,
            min_component_fraction=0.7,
            exact_rule_pairs=((survive_counts, birth_counts),),
            preferred_rule_pairs=WINNER_RULE_PAIRS,
            preferred_bonus=0.2,
            seed_builders=(point_seed_builder, cluster_seed_builder),
        )
        for candidate in exact_candidates:
            identity = candidate_identity_key(candidate)
            rescue_identity_list.append(identity)
            if identity not in pooled_candidates:
                pooled_candidates[identity] = candidate
                candidate_sources[identity] = "rescue"
                present_rule_signatures.add(winner_signature)
            else:
                candidate_sources[identity] = merge_candidate_sources(
                    candidate_sources[identity],
                    "rescue",
                )
                present_rule_signatures.add(winner_signature)

    primary_selector_identity = primary_best_identity
    fallback_selector_identity = fallback_best_identity
    rescue_selector_identities = tuple(
        dict.fromkeys(
            identity
            for identity, candidate in pooled_candidates.items()
            if format_rule_signature(
                candidate.survive_counts,
                candidate.birth_counts,
            ) in winner_signatures
        )
    )

    best_identity_by_signature: dict[str, tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]]] = {}
    best_signature_key: dict[str, tuple[float, ...]] = {}
    merged_signature_sources: dict[str, str] = {}
    for identity, candidate in pooled_candidates.items():
        rule_signature = format_rule_signature(
            candidate.survive_counts,
            candidate.birth_counts,
        )
        merged_signature_sources[rule_signature] = merge_candidate_sources(
            merged_signature_sources.get(rule_signature, ""),
            candidate_sources[identity],
        )
        search_key = candidate_search_key(
            candidate,
            graph_center=graph_center,
            preferred_set=set(),
            preferred_bonus=0.0,
        )
        if rule_signature not in best_signature_key or search_key > best_signature_key[rule_signature]:
            best_signature_key[rule_signature] = search_key
            best_identity_by_signature[rule_signature] = identity

    signature_pooled_candidates = {
        identity: pooled_candidates[identity]
        for identity in best_identity_by_signature.values()
    }
    signature_candidate_sources = {
        identity: merged_signature_sources[
            format_rule_signature(
                signature_pooled_candidates[identity].survive_counts,
                signature_pooled_candidates[identity].birth_counts,
            )
        ]
        for identity in signature_pooled_candidates
    }

    if primary_best_identity is not None:
        primary_signature = format_rule_signature(
            pooled_candidates[primary_best_identity].survive_counts,
            pooled_candidates[primary_best_identity].birth_counts,
        )
        primary_best_identity = best_identity_by_signature[primary_signature]
    if fallback_best_identity is not None:
        fallback_signature = format_rule_signature(
            pooled_candidates[fallback_best_identity].survive_counts,
            pooled_candidates[fallback_best_identity].birth_counts,
        )
        fallback_best_identity = best_identity_by_signature[fallback_signature]
    rescue_identity_list = list(
        dict.fromkeys(
            best_identity_by_signature[
                format_rule_signature(
                    pooled_candidates[identity].survive_counts,
                    pooled_candidates[identity].birth_counts,
                )
            ]
            for identity in rescue_identity_list
        )
    )

    return RawFrontierPool(
        selector_candidates=dict(pooled_candidates),
        primary_selector_identity=primary_selector_identity,
        fallback_selector_identity=fallback_selector_identity,
        rescue_selector_identities=rescue_selector_identities,
        pooled_candidates=signature_pooled_candidates,
        candidate_sources=signature_candidate_sources,
        primary_best_identity=primary_best_identity,
        fallback_best_identity=fallback_best_identity,
        rescue_identities=tuple(dict.fromkeys(rescue_identity_list)),
    )


def collect_restricted_frontier_pool(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    allowed_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...],
) -> RawFrontierPool:
    if not allowed_rule_pairs:
        return collect_raw_frontier_pool(nodes, wrap_y, count_options)

    xs = [x for x, _y in nodes]
    ys = [y for _x, y in nodes]
    graph_center = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    pooled_candidates: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        RuleCandidate,
    ] = {}
    candidate_sources: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        str,
    ] = {}

    search_specs = (
        (
            "primary",
            dict(
                evolution_steps=8,
                sample_window=3,
                occupancy_threshold=2 / 3,
                min_component_fraction=0.9,
                preferred_rule_pairs=allowed_rule_pairs,
                exact_rule_pairs=allowed_rule_pairs,
                preferred_bonus=0.05,
                seed_builders=(point_seed_builder,),
            ),
        ),
        (
            "fallback",
            dict(
                evolution_steps=10,
                sample_window=4,
                occupancy_threshold=0.6,
                min_component_fraction=0.7,
                preferred_rule_pairs=allowed_rule_pairs,
                exact_rule_pairs=allowed_rule_pairs,
                preferred_bonus=0.08,
                seed_builders=(point_seed_builder, cluster_seed_builder),
            ),
        ),
    )

    primary_best_identity = None
    fallback_best_identity = None
    for source_label, search_kwargs in search_specs:
        collected_candidates, _diagnostics = collect_self_maintenance_candidates(
            nodes,
            count_options=count_options,
            wrap_y=wrap_y,
            **search_kwargs,
        )
        if collected_candidates:
            best_identity = candidate_identity_key(collected_candidates[0])
            if source_label == "primary":
                primary_best_identity = best_identity
            else:
                fallback_best_identity = best_identity
        for candidate in collected_candidates:
            identity = candidate_identity_key(candidate)
            if identity not in pooled_candidates:
                pooled_candidates[identity] = candidate
                candidate_sources[identity] = source_label
            else:
                candidate_sources[identity] = merge_candidate_sources(
                    candidate_sources[identity],
                    source_label,
                )

    best_identity_by_signature: dict[
        str,
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
    ] = {}
    best_signature_key: dict[str, tuple[float, ...]] = {}
    merged_signature_sources: dict[str, str] = {}
    for identity, candidate in pooled_candidates.items():
        rule_signature = format_rule_signature(
            candidate.survive_counts,
            candidate.birth_counts,
        )
        merged_signature_sources[rule_signature] = merge_candidate_sources(
            merged_signature_sources.get(rule_signature, ""),
            candidate_sources[identity],
        )
        search_key = candidate_search_key(
            candidate,
            graph_center=graph_center,
            preferred_set=set(allowed_rule_pairs),
            preferred_bonus=0.0,
        )
        if rule_signature not in best_signature_key or search_key > best_signature_key[rule_signature]:
            best_signature_key[rule_signature] = search_key
            best_identity_by_signature[rule_signature] = identity

    signature_pooled_candidates = {
        identity: pooled_candidates[identity]
        for identity in best_identity_by_signature.values()
    }
    signature_candidate_sources = {
        identity: merged_signature_sources[
            format_rule_signature(
                signature_pooled_candidates[identity].survive_counts,
                signature_pooled_candidates[identity].birth_counts,
            )
        ]
        for identity in signature_pooled_candidates
    }

    if primary_best_identity is not None:
        primary_signature = format_rule_signature(
            pooled_candidates[primary_best_identity].survive_counts,
            pooled_candidates[primary_best_identity].birth_counts,
        )
        primary_best_identity = best_identity_by_signature[primary_signature]
    if fallback_best_identity is not None:
        fallback_signature = format_rule_signature(
            pooled_candidates[fallback_best_identity].survive_counts,
            pooled_candidates[fallback_best_identity].birth_counts,
        )
        fallback_best_identity = best_identity_by_signature[fallback_signature]

    all_signature_identities = tuple(dict.fromkeys(signature_pooled_candidates.keys()))
    return RawFrontierPool(
        selector_candidates=dict(signature_pooled_candidates),
        primary_selector_identity=primary_best_identity,
        fallback_selector_identity=fallback_best_identity,
        rescue_selector_identities=all_signature_identities,
        pooled_candidates=signature_pooled_candidates,
        candidate_sources=signature_candidate_sources,
        primary_best_identity=primary_best_identity,
        fallback_best_identity=fallback_best_identity,
        rescue_identities=all_signature_identities,
    )


def collect_limited_rediscovery_frontier_pool(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    allowed_rule_pairs: tuple[tuple[frozenset[int], frozenset[int]], ...],
    rediscovery_limit: int = 2,
) -> RawFrontierPool:
    tracked_pool = collect_restricted_frontier_pool(
        nodes,
        wrap_y,
        count_options,
        allowed_rule_pairs,
    )
    open_pool = collect_raw_frontier_pool(nodes, wrap_y, count_options)
    return merge_limited_rediscovery_frontier_pool(
        nodes,
        tracked_pool,
        open_pool,
        rediscovery_limit=rediscovery_limit,
    )


def merge_limited_rediscovery_frontier_pool(
    nodes: set[tuple[int, int]],
    tracked_pool: RawFrontierPool,
    open_pool: RawFrontierPool,
    rediscovery_limit: int = 2,
) -> RawFrontierPool:
    if rediscovery_limit <= 0:
        return tracked_pool

    tracked_signatures = {
        format_rule_signature(candidate.survive_counts, candidate.birth_counts)
        for candidate in tracked_pool.pooled_candidates.values()
    }
    graph_center = perturbation_graph_center(nodes)
    rediscovery_identities = sorted(
        (
            identity
            for identity, candidate in open_pool.pooled_candidates.items()
            if format_rule_signature(candidate.survive_counts, candidate.birth_counts)
            not in tracked_signatures
        ),
        key=lambda identity: candidate_search_key(
            open_pool.pooled_candidates[identity],
            graph_center=graph_center,
            preferred_set=set(),
            preferred_bonus=0.0,
        ),
        reverse=True,
    )[:rediscovery_limit]
    if not rediscovery_identities:
        return tracked_pool

    selector_candidates = dict(tracked_pool.selector_candidates)
    pooled_candidates = dict(tracked_pool.pooled_candidates)
    candidate_sources = dict(tracked_pool.candidate_sources)
    rescue_selector_identities = list(tracked_pool.rescue_selector_identities)
    rescue_identities = list(tracked_pool.rescue_identities)

    for identity in rediscovery_identities:
        candidate = open_pool.pooled_candidates[identity]
        selector_candidates[identity] = candidate
        pooled_candidates[identity] = candidate
        candidate_sources[identity] = merge_candidate_sources(
            candidate_sources.get(identity, ""),
            merge_candidate_sources(
                open_pool.candidate_sources.get(identity, ""),
                "rediscovery",
            ),
        )
        rescue_selector_identities.append(identity)
        rescue_identities.append(identity)

    return RawFrontierPool(
        selector_candidates=selector_candidates,
        primary_selector_identity=tracked_pool.primary_selector_identity,
        fallback_selector_identity=tracked_pool.fallback_selector_identity,
        rescue_selector_identities=tuple(dict.fromkeys(rescue_selector_identities)),
        pooled_candidates=pooled_candidates,
        candidate_sources=candidate_sources,
        primary_best_identity=tracked_pool.primary_best_identity,
        fallback_best_identity=tracked_pool.fallback_best_identity,
        rescue_identities=tuple(dict.fromkeys(rescue_identities)),
    )


def choose_current_selected_signature(
    raw_pool: RawFrontierPool,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    postulates: RulePostulates,
    evaluation_cache: FrontierEvaluationCache | None = None,
    selector_mode: str = "always_compare",
) -> str | None:
    selector_metric_cache: dict[
        tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
        tuple[tuple[float, ...], str, str],
    ] = {}

    def selector_metrics(
        identity: tuple[frozenset[int], frozenset[int], frozenset[tuple[int, int]]],
    ) -> tuple[tuple[float, ...], str, str]:
        if identity not in selector_metric_cache:
            candidate = raw_pool.selector_candidates[identity]
            if evaluation_cache is None:
                center_gap, arrival_span, centroid_y, _survived, status = evaluate_rule_candidate(
                    nodes,
                    wrap_y,
                    candidate,
                    postulates,
                )
            else:
                snapshot = frontier_metric_snapshot(
                    candidate,
                    nodes,
                    wrap_y,
                    postulates,
                    evaluation_cache,
                )
                center_gap = snapshot.center_gap
                arrival_span = snapshot.arrival_span
                centroid_y = snapshot.centroid_y
                status = snapshot.status
            selector_metric_cache[identity] = (
                candidate_quality_key(
                    candidate,
                    (
                        center_gap,
                        arrival_span,
                        centroid_y,
                        status == "survives",
                        status,
                    ),
                ),
                status,
                format_rule_signature(
                    candidate.survive_counts,
                    candidate.birth_counts,
                ),
            )
        return selector_metric_cache[identity]

    selected_identity = raw_pool.primary_selector_identity or raw_pool.fallback_selector_identity
    selected_status = "no pattern"
    selected_key = None
    if selected_identity is not None:
        selected_key, selected_status, _selected_signature = selector_metrics(selected_identity)
    should_consult_rescue = (
        selector_mode == "always_compare"
        or selected_identity is None
        or selected_status != "survives"
    )
    if should_consult_rescue:
        rescue_identities = [
            identity
            for identity in raw_pool.rescue_selector_identities
            if identity in raw_pool.selector_candidates
        ]
        if rescue_identities:
            best_rescue_identity = max(
                rescue_identities,
                key=lambda identity: selector_metrics(identity)[0],
            )
            rescue_key, _rescue_status, _rescue_signature = selector_metrics(best_rescue_identity)
            if selected_key is None or rescue_key > selected_key:
                selected_identity = best_rescue_identity
                selected_key = rescue_key

    if selected_identity is None:
        return None
    return selector_metrics(selected_identity)[2]


def collect_candidate_pool(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    rule_family: str,
    count_options: tuple[frozenset[int], ...],
    retained_weight: float,
    raw_pool: RawFrontierPool | None = None,
    evaluation_cache: FrontierEvaluationCache | None = None,
) -> list[EvaluatedCandidate]:
    postulates = build_frontier_postulates(retained_weight)
    current_raw_pool = raw_pool or collect_raw_frontier_pool(
        nodes,
        wrap_y,
        count_options,
    )
    current_evaluation_cache = evaluation_cache or build_frontier_evaluation_cache(nodes, wrap_y)

    evaluated_candidates = [
        evaluate_frontier_candidate(
            candidate=candidate,
            rule_family=rule_family,
            pack_name=pack_name,
            scenario_name=scenario_name,
            retained_weight=retained_weight,
            search_sources=current_raw_pool.candidate_sources[identity],
            nodes=nodes,
            wrap_y=wrap_y,
            postulates=postulates,
            current_selected=False,
            evaluation_cache=current_evaluation_cache,
        )
        for identity, candidate in current_raw_pool.pooled_candidates.items()
    ]
    selected_signature = choose_current_selected_signature(
        current_raw_pool,
        nodes,
        wrap_y,
        postulates,
        current_evaluation_cache,
        selector_mode="always_compare",
    )
    for candidate in evaluated_candidates:
        candidate.current_selected = candidate.rule_signature == selected_signature
    evaluated_candidates.sort(
        key=lambda candidate: (
            candidate.current_selected,
            candidate.status_rank,
            candidate.center_gap + candidate.arrival_span,
            candidate.arrival_span,
            candidate.center_gap,
            candidate.rule_signature,
            candidate.seed_node,
        ),
        reverse=True,
    )

    frontier_sets = {
        view_name: pareto_frontier_identities(evaluated_candidates, axes)
        for view_name, axes in frontier_axes().items()
    }
    for candidate in evaluated_candidates:
        candidate.on_robustness = candidate.candidate_identity in frontier_sets["robustness"]
        candidate.on_proper_time = candidate.candidate_identity in frontier_sets["proper_time"]
        candidate.on_geometry = candidate.candidate_identity in frontier_sets["geometry"]
        candidate.on_mixed = candidate.candidate_identity in frontier_sets["mixed"]

    return evaluated_candidates


def frontier_case_analysis(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    rule_family: str,
    count_options: tuple[frozenset[int], ...],
    retained_weight: float,
    raw_pool: RawFrontierPool | None = None,
    evaluation_cache: FrontierEvaluationCache | None = None,
) -> tuple[FrontierScenarioRow, list[EvaluatedCandidate]]:
    candidates = collect_candidate_pool(
        pack_name=pack_name,
        scenario_name=scenario_name,
        nodes=nodes,
        wrap_y=wrap_y,
        rule_family=rule_family,
        count_options=count_options,
        retained_weight=retained_weight,
        raw_pool=raw_pool,
        evaluation_cache=evaluation_cache,
    )
    selected_candidates = [candidate for candidate in candidates if candidate.current_selected]
    selected_candidate = selected_candidates[0] if selected_candidates else None
    robustness_candidates = [candidate for candidate in candidates if candidate.on_robustness]
    proper_time_candidates = [candidate for candidate in candidates if candidate.on_proper_time]
    geometry_candidates = [candidate for candidate in candidates if candidate.on_geometry]
    mixed_candidates = [candidate for candidate in candidates if candidate.on_mixed]
    row = FrontierScenarioRow(
        pack_name=pack_name,
        scenario_name=scenario_name,
        rule_family=rule_family,
        retained_weight=retained_weight,
        pool_size=len(candidates),
        selected_rule=(selected_candidate.rule_signature if selected_candidate is not None else "none"),
        selected_on_robustness=(selected_candidate.on_robustness if selected_candidate is not None else False),
        selected_on_proper_time=(selected_candidate.on_proper_time if selected_candidate is not None else False),
        selected_on_geometry=(selected_candidate.on_geometry if selected_candidate is not None else False),
        selected_on_mixed=(selected_candidate.on_mixed if selected_candidate is not None else False),
        robustness_count=len(robustness_candidates),
        proper_time_count=len(proper_time_candidates),
        geometry_count=len(geometry_candidates),
        mixed_count=len(mixed_candidates),
        robustness_rules=format_frontier_rule_signatures(robustness_candidates),
        proper_time_rules=format_frontier_rule_signatures(proper_time_candidates),
        geometry_rules=format_frontier_rule_signatures(geometry_candidates),
        mixed_rules=format_frontier_rule_signatures(mixed_candidates),
    )
    return row, candidates


def frontier_sweep_results(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> tuple[list[FrontierScenarioRow], list[EvaluatedCandidate]]:
    scenario_rows: list[FrontierScenarioRow] = []
    candidates: list[EvaluatedCandidate] = []
    evaluation_caches: dict[tuple[str, str], FrontierEvaluationCache] = {}
    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                scenario_key = (pack_name, scenario_name)
                current_evaluation_cache = evaluation_caches.get(scenario_key)
                if current_evaluation_cache is None:
                    current_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
                    evaluation_caches[scenario_key] = current_evaluation_cache
                raw_pool = collect_raw_frontier_pool(
                    nodes,
                    wrap_y,
                    count_options,
                )
                for retained_weight in retained_weights:
                    scenario_row, case_candidates = frontier_case_analysis(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        nodes=nodes,
                        wrap_y=wrap_y,
                        rule_family=rule_family,
                        count_options=count_options,
                        retained_weight=retained_weight,
                        raw_pool=raw_pool,
                        evaluation_cache=current_evaluation_cache,
                    )
                    scenario_rows.append(scenario_row)
                    candidates.extend(case_candidates)
    return scenario_rows, candidates


def summarize_frontier_aggregates(
    candidates: list[EvaluatedCandidate],
) -> list[FrontierAggregateRow]:
    case_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    selected_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    robustness_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    proper_time_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    geometry_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    mixed_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)

    for candidate in candidates:
        family_rule = (candidate.rule_family, candidate.rule_signature)
        case_key = (candidate.pack_name, candidate.scenario_name, candidate.retained_weight)
        case_sets[family_rule].add(case_key)
        if candidate.current_selected:
            selected_sets[family_rule].add(case_key)
        if candidate.on_robustness:
            robustness_sets[family_rule].add(case_key)
        if candidate.on_proper_time:
            proper_time_sets[family_rule].add(case_key)
        if candidate.on_geometry:
            geometry_sets[family_rule].add(case_key)
        if candidate.on_mixed:
            mixed_sets[family_rule].add(case_key)

    rows = [
        FrontierAggregateRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            case_hits=len(case_sets[(rule_family, rule_signature)]),
            selected_hits=len(selected_sets[(rule_family, rule_signature)]),
            robustness_hits=len(robustness_sets[(rule_family, rule_signature)]),
            proper_time_hits=len(proper_time_sets[(rule_family, rule_signature)]),
            geometry_hits=len(geometry_sets[(rule_family, rule_signature)]),
            mixed_hits=len(mixed_sets[(rule_family, rule_signature)]),
        )
        for rule_family, rule_signature in case_sets
    ]
    return sorted(
        rows,
        key=lambda row: (
            row.rule_family,
            -row.mixed_hits,
            -row.robustness_hits,
            -row.proper_time_hits,
            -row.geometry_hits,
            -row.selected_hits,
            row.rule_signature,
        ),
    )


def frontier_signature_sets(
    candidates: list[EvaluatedCandidate],
) -> dict[str, set[str]]:
    return {
        "robustness": {candidate.rule_signature for candidate in candidates if candidate.on_robustness},
        "proper_time": {candidate.rule_signature for candidate in candidates if candidate.on_proper_time},
        "geometry": {candidate.rule_signature for candidate in candidates if candidate.on_geometry},
        "mixed": {candidate.rule_signature for candidate in candidates if candidate.on_mixed},
    }


def base_palette_rule_pairs(
    candidates: list[EvaluatedCandidate],
) -> tuple[tuple[frozenset[int], frozenset[int]], ...]:
    return tuple(
        dict.fromkeys(
            (
                candidate.survive_counts,
                candidate.birth_counts,
            )
            for candidate in candidates
            if candidate.current_selected
            or candidate.on_robustness
            or candidate.on_proper_time
            or candidate.on_geometry
            or candidate.on_mixed
        )
    )


def perturbation_case_needs_drift_report(row: PerturbationCaseRow) -> bool:
    return (
        not row.selected_matches_base
        or not row.base_selected_alive
        or not row.robustness_overlap
        or not row.mixed_overlap
    )


def perturbation_case_sort_key(row: PerturbationCaseRow) -> tuple[object, ...]:
    return (
        row.selected_matches_base,
        row.base_selected_alive,
        row.mixed_overlap,
        row.robustness_overlap,
        row.rule_family,
        row.pack_name,
        row.scenario_name,
        row.variant_name,
    )


def bounded_insert_sorted(
    rows: list[object],
    row: object,
    limit: int,
    key_fn: Callable[[object], tuple[object, ...]],
) -> None:
    rows.append(row)
    rows.sort(key=key_fn)
    if len(rows) > limit:
        del rows[limit:]


def build_perturbation_aggregate_rows(
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationCaseRow]],
) -> list[PerturbationAggregateRow]:
    aggregate_rows = [
        PerturbationAggregateRow(
            rule_family=rule_family,
            variant_name=variant_name,
            cases=len(rows),
            survives=sum(row.perturbed_status == "survives" for row in rows),
            selected_retained=sum(row.selected_matches_base for row in rows),
            base_selected_alive=sum(row.base_selected_alive for row in rows),
            robustness_overlap=sum(row.robustness_overlap for row in rows),
            proper_time_overlap=sum(row.proper_time_overlap for row in rows),
            geometry_overlap=sum(row.geometry_overlap for row in rows),
            mixed_overlap=sum(row.mixed_overlap for row in rows),
        )
        for (rule_family, variant_name), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.variant_name != "all",
            row.variant_name,
        )
    )
    return aggregate_rows


def perturbation_frontier_results_for_factory(
    perturbation_factory: Callable[
        [str, str, set[tuple[int, int]], bool],
        tuple[tuple[str, set[tuple[int, int]], int], ...],
    ],
    retained_weight: float = 1.0,
) -> tuple[list[PerturbationCaseRow], list[PerturbationAggregateRow]]:
    case_rows: list[PerturbationCaseRow] = []
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationCaseRow]] = defaultdict(list)

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                base_raw_pool = collect_raw_frontier_pool(
                    nodes,
                    wrap_y,
                    count_options,
                )
                base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
                base_row, base_candidates = frontier_case_analysis(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weight=retained_weight,
                    raw_pool=base_raw_pool,
                    evaluation_cache=base_evaluation_cache,
                )
                base_signature_sets = frontier_signature_sets(base_candidates)
                base_selected_rule = base_row.selected_rule
                allowed_rule_pairs = base_palette_rule_pairs(base_candidates)

                for variant_name, perturbed_nodes, node_delta in perturbation_factory(
                    pack_name,
                    scenario_name,
                    nodes,
                    wrap_y,
                ):
                    perturbed_raw_pool = collect_restricted_frontier_pool(
                        perturbed_nodes,
                        wrap_y,
                        count_options,
                        allowed_rule_pairs,
                    )
                    perturbed_evaluation_cache = build_frontier_evaluation_cache(
                        perturbed_nodes,
                        wrap_y,
                    )
                    perturbed_row, perturbed_candidates = frontier_case_analysis(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        nodes=perturbed_nodes,
                        wrap_y=wrap_y,
                        rule_family=rule_family,
                        count_options=count_options,
                        retained_weight=retained_weight,
                        raw_pool=perturbed_raw_pool,
                        evaluation_cache=perturbed_evaluation_cache,
                    )
                    perturbed_signature_sets = frontier_signature_sets(perturbed_candidates)
                    perturbed_frontier_union = set().union(*perturbed_signature_sets.values())
                    selected_candidate = next(
                        (
                            candidate
                            for candidate in perturbed_candidates
                            if candidate.current_selected
                        ),
                        None,
                    )
                    case_row = PerturbationCaseRow(
                        rule_family=rule_family,
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        variant_name=variant_name,
                        node_delta=node_delta,
                        base_selected_rule=base_selected_rule,
                        perturbed_selected_rule=perturbed_row.selected_rule,
                        perturbed_status=(
                            selected_candidate.status if selected_candidate is not None else "no pattern"
                        ),
                        selected_matches_base=(perturbed_row.selected_rule == base_selected_rule),
                        base_selected_alive=(base_selected_rule in perturbed_frontier_union),
                        robustness_overlap=bool(
                            base_signature_sets["robustness"]
                            & perturbed_signature_sets["robustness"]
                        ),
                        proper_time_overlap=bool(
                            base_signature_sets["proper_time"]
                            & perturbed_signature_sets["proper_time"]
                        ),
                        geometry_overlap=bool(
                            base_signature_sets["geometry"]
                            & perturbed_signature_sets["geometry"]
                        ),
                        mixed_overlap=bool(
                            base_signature_sets["mixed"] & perturbed_signature_sets["mixed"]
                        ),
                    )
                    case_rows.append(case_row)
                    grouped_rows[(rule_family, variant_name)].append(case_row)
                    grouped_rows[(rule_family, "all")].append(case_row)

    aggregate_rows = [
        PerturbationAggregateRow(
            rule_family=rule_family,
            variant_name=variant_name,
            cases=len(rows),
            survives=sum(row.perturbed_status == "survives" for row in rows),
            selected_retained=sum(row.selected_matches_base for row in rows),
            base_selected_alive=sum(row.base_selected_alive for row in rows),
            robustness_overlap=sum(row.robustness_overlap for row in rows),
            proper_time_overlap=sum(row.proper_time_overlap for row in rows),
            geometry_overlap=sum(row.geometry_overlap for row in rows),
            mixed_overlap=sum(row.mixed_overlap for row in rows),
        )
        for (rule_family, variant_name), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.variant_name != "all",
            row.variant_name,
        )
    )
    return case_rows, aggregate_rows


def perturbation_frontier_summary_for_factory(
    perturbation_factory: Callable[
        [str, str, set[tuple[int, int]], bool],
        tuple[tuple[str, set[tuple[int, int]], int], ...],
    ],
    retained_weight: float = 1.0,
    drift_limit: int = 16,
    perturbed_pool_builder: Callable[
        [set[tuple[int, int]], bool, tuple[frozenset[int], ...], tuple[tuple[frozenset[int], frozenset[int]], ...]],
        RawFrontierPool,
    ] | None = None,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationCaseRow]] = defaultdict(list)
    drift_rows: list[PerturbationCaseRow] = []
    current_pool_builder = perturbed_pool_builder or collect_restricted_frontier_pool

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                base_raw_pool = collect_raw_frontier_pool(
                    nodes,
                    wrap_y,
                    count_options,
                )
                base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
                base_row, base_candidates = frontier_case_analysis(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weight=retained_weight,
                    raw_pool=base_raw_pool,
                    evaluation_cache=base_evaluation_cache,
                )
                base_signature_sets = frontier_signature_sets(base_candidates)
                base_selected_rule = base_row.selected_rule
                allowed_rule_pairs = base_palette_rule_pairs(base_candidates)

                for variant_name, perturbed_nodes, node_delta in perturbation_factory(
                    pack_name,
                    scenario_name,
                    nodes,
                    wrap_y,
                ):
                    perturbed_raw_pool = current_pool_builder(
                        perturbed_nodes,
                        wrap_y,
                        count_options,
                        allowed_rule_pairs,
                    )
                    perturbed_evaluation_cache = build_frontier_evaluation_cache(
                        perturbed_nodes,
                        wrap_y,
                    )
                    perturbed_row, perturbed_candidates = frontier_case_analysis(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        nodes=perturbed_nodes,
                        wrap_y=wrap_y,
                        rule_family=rule_family,
                        count_options=count_options,
                        retained_weight=retained_weight,
                        raw_pool=perturbed_raw_pool,
                        evaluation_cache=perturbed_evaluation_cache,
                    )
                    perturbed_signature_sets = frontier_signature_sets(perturbed_candidates)
                    perturbed_frontier_union = set().union(*perturbed_signature_sets.values())
                    selected_candidate = next(
                        (
                            candidate
                            for candidate in perturbed_candidates
                            if candidate.current_selected
                        ),
                        None,
                    )
                    case_row = PerturbationCaseRow(
                        rule_family=rule_family,
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        variant_name=variant_name,
                        node_delta=node_delta,
                        base_selected_rule=base_selected_rule,
                        perturbed_selected_rule=perturbed_row.selected_rule,
                        perturbed_status=(
                            selected_candidate.status if selected_candidate is not None else "no pattern"
                        ),
                        selected_matches_base=(perturbed_row.selected_rule == base_selected_rule),
                        base_selected_alive=(base_selected_rule in perturbed_frontier_union),
                        robustness_overlap=bool(
                            base_signature_sets["robustness"]
                            & perturbed_signature_sets["robustness"]
                        ),
                        proper_time_overlap=bool(
                            base_signature_sets["proper_time"]
                            & perturbed_signature_sets["proper_time"]
                        ),
                        geometry_overlap=bool(
                            base_signature_sets["geometry"]
                            & perturbed_signature_sets["geometry"]
                        ),
                        mixed_overlap=bool(
                            base_signature_sets["mixed"] & perturbed_signature_sets["mixed"]
                        ),
                    )
                    grouped_rows[(rule_family, variant_name)].append(case_row)
                    grouped_rows[(rule_family, "all")].append(case_row)
                    if perturbation_case_needs_drift_report(case_row):
                        bounded_insert_sorted(
                            drift_rows,
                            case_row,
                            drift_limit,
                            perturbation_case_sort_key,
                        )

    return build_perturbation_aggregate_rows(grouped_rows), drift_rows


def perturbation_frontier_results(
    retained_weight: float = 1.0,
) -> tuple[list[PerturbationCaseRow], list[PerturbationAggregateRow]]:
    return perturbation_frontier_results_for_factory(
        lambda _pack_name, _scenario_name, nodes, wrap_y: deterministic_topology_perturbations(
            nodes,
            wrap_y,
        ),
        retained_weight=retained_weight,
    )


def perturbation_frontier_summary(
    retained_weight: float = 1.0,
    drift_limit: int = 16,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    return perturbation_frontier_summary_for_factory(
        lambda _pack_name, _scenario_name, nodes, wrap_y: deterministic_topology_perturbations(
            nodes,
            wrap_y,
        ),
        retained_weight=retained_weight,
        drift_limit=drift_limit,
    )


def random_perturbation_frontier_results(
    retained_weight: float = 1.0,
    variant_limit: int = 2,
) -> tuple[list[PerturbationCaseRow], list[PerturbationAggregateRow]]:
    return perturbation_frontier_results_for_factory(
        lambda pack_name, scenario_name, nodes, wrap_y: random_topology_perturbations(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=variant_limit,
        ),
        retained_weight=retained_weight,
    )


def random_perturbation_frontier_summary(
    retained_weight: float = 1.0,
    drift_limit: int = 16,
    variant_limit: int = 2,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    return perturbation_frontier_summary_for_factory(
        lambda pack_name, scenario_name, nodes, wrap_y: random_topology_perturbations(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=variant_limit,
        ),
        retained_weight=retained_weight,
        drift_limit=drift_limit,
    )


def random_rediscovery_perturbation_frontier_summary(
    retained_weight: float = 1.0,
    drift_limit: int = 16,
    variant_limit: int = 3,
    rediscovery_limit: int = 2,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    return perturbation_frontier_summary_for_factory(
        lambda pack_name, scenario_name, nodes, wrap_y: random_topology_perturbations(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=variant_limit,
        ),
        retained_weight=retained_weight,
        drift_limit=drift_limit,
        perturbed_pool_builder=lambda nodes, wrap_y, count_options, allowed_rule_pairs: (
            collect_limited_rediscovery_frontier_pool(
                nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
                rediscovery_limit=rediscovery_limit,
            )
        ),
    )


def geometry_randomization_frontier_summary(
    retained_weight: float = 1.0,
    drift_limit: int = 16,
    variant_limit: int = 2,
    rediscovery_limit: int = 1,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    return perturbation_frontier_summary_for_factory(
        lambda pack_name, scenario_name, nodes, wrap_y: randomized_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=variant_limit,
        ),
        retained_weight=retained_weight,
        drift_limit=drift_limit,
        perturbed_pool_builder=lambda nodes, wrap_y, count_options, allowed_rule_pairs: (
            collect_limited_rediscovery_frontier_pool(
                nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
                rediscovery_limit=rediscovery_limit,
            )
        ),
    )


def procedural_geometry_frontier_summary(
    retained_weight: float = 1.0,
    drift_limit: int = 16,
    variant_limit: int = 2,
    rediscovery_limit: int = 1,
) -> tuple[list[PerturbationAggregateRow], list[PerturbationCaseRow]]:
    return perturbation_frontier_summary_for_factory(
        lambda pack_name, scenario_name, nodes, wrap_y: procedural_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=variant_limit,
        ),
        retained_weight=retained_weight,
        drift_limit=drift_limit,
        perturbed_pool_builder=lambda nodes, wrap_y, count_options, allowed_rule_pairs: (
            collect_limited_rediscovery_frontier_pool(
                nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
                rediscovery_limit=rediscovery_limit,
            )
        ),
    )


def procedural_compact_failure_diagnostics(
    retained_weight: float = 1.0,
    variant_limit: int = 2,
    rediscovery_limit: int = 1,
) -> list[ProceduralFailureDiagnosticRow]:
    compact_count_options = dict(family_count_options())["compact"]
    rows: list[ProceduralFailureDiagnosticRow] = []

    for pack_name, scenarios in benchmark_packs():
        for scenario_name, nodes, wrap_y in scenarios:
            base_raw_pool = collect_raw_frontier_pool(
                nodes,
                wrap_y,
                compact_count_options,
            )
            base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
            _base_row, base_candidates = frontier_case_analysis(
                pack_name=pack_name,
                scenario_name=scenario_name,
                nodes=nodes,
                wrap_y=wrap_y,
                rule_family="compact",
                count_options=compact_count_options,
                retained_weight=retained_weight,
                raw_pool=base_raw_pool,
                evaluation_cache=base_evaluation_cache,
            )
            base_mixed_rules = {
                candidate.rule_signature
                for candidate in base_candidates
                if candidate.on_mixed
            }
            allowed_rule_pairs = base_palette_rule_pairs(base_candidates)
            scenario_variant_rows: list[ProceduralFailureDiagnosticRow] = []

            for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
                pack_name,
                scenario_name,
                nodes,
                wrap_y,
                variant_limit=variant_limit,
            ):
                perturbed_pool = collect_limited_rediscovery_frontier_pool(
                    perturbed_nodes,
                    wrap_y,
                    compact_count_options,
                    allowed_rule_pairs,
                    rediscovery_limit=rediscovery_limit,
                )
                perturbed_evaluation_cache = build_frontier_evaluation_cache(
                    perturbed_nodes,
                    wrap_y,
                )
                _perturbed_row, perturbed_candidates = frontier_case_analysis(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=perturbed_nodes,
                    wrap_y=wrap_y,
                    rule_family="compact",
                    count_options=compact_count_options,
                    retained_weight=retained_weight,
                    raw_pool=perturbed_pool,
                    evaluation_cache=perturbed_evaluation_cache,
                )
                selected_candidate = next(
                    candidate for candidate in perturbed_candidates if candidate.current_selected
                )
                perturbed_mixed_rules = {
                    candidate.rule_signature
                    for candidate in perturbed_candidates
                    if candidate.on_mixed
                }
                (
                    mean_center,
                    center_range,
                    center_total_variation,
                    crosses_midline,
                    span_range,
                ) = column_profile_geometry_metrics(perturbed_nodes)
                scenario_variant_rows.append(
                    ProceduralFailureDiagnosticRow(
                        scenario_name=f"{pack_name}:{scenario_name}",
                        variant_name=variant_name,
                        selected_rule=selected_candidate.rule_signature,
                        status=selected_candidate.status,
                        mixed_overlap=bool(base_mixed_rules & perturbed_mixed_rules),
                        center_gap=selected_candidate.center_gap,
                        arrival_span=selected_candidate.arrival_span,
                        mean_center=mean_center,
                        center_range=center_range,
                        center_total_variation=center_total_variation,
                        crosses_midline=crosses_midline,
                        span_range=span_range,
                    )
                )

            if any(row.status != "survives" for row in scenario_variant_rows):
                rows.extend(scenario_variant_rows)

    rows.sort(key=lambda row: (row.scenario_name, row.variant_name))
    return rows


def contour_sensitivity_sweep(
    retained_weight: float = 1.0,
    rediscovery_limit: int = 1,
    alphas: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> list[ContourSensitivityRow]:
    compact_count_options = dict(family_count_options())["compact"]
    pack_name = "base"
    scenario_name = "taper-hard"
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)

    base_raw_pool = collect_raw_frontier_pool(
        nodes,
        wrap_y,
        compact_count_options,
    )
    base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
    _base_row, base_candidates = frontier_case_analysis(
        pack_name=pack_name,
        scenario_name=scenario_name,
        nodes=nodes,
        wrap_y=wrap_y,
        rule_family="compact",
        count_options=compact_count_options,
        retained_weight=retained_weight,
        raw_pool=base_raw_pool,
        evaluation_cache=base_evaluation_cache,
    )
    base_mixed_rules = {
        candidate.rule_signature
        for candidate in base_candidates
        if candidate.on_mixed
    }
    allowed_rule_pairs = base_palette_rule_pairs(base_candidates)

    procedural_variants = {
        variant_name: perturbed_nodes
        for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=2,
        )
    }
    survivor_nodes = procedural_variants["procedural-a"]
    miss_nodes = procedural_variants["procedural-b"]
    xs, survivor_centers, _survivor_spans = ordered_profile_centers_and_spans(survivor_nodes)
    miss_xs, miss_centers, miss_spans = ordered_profile_centers_and_spans(miss_nodes)
    if xs != miss_xs:
        raise RuntimeError("Contour sensitivity sweep requires aligned x columns.")

    rows: list[ContourSensitivityRow] = []
    for alpha in alphas:
        centers = tuple(
            survivor_center + alpha * (miss_center - survivor_center)
            for survivor_center, miss_center in zip(survivor_centers, miss_centers)
        )
        profile = build_profile_from_centers_and_spans(xs, centers, miss_spans)
        sweep_nodes = build_nodes_from_interval_profile(profile)
        sweep_pool = collect_limited_rediscovery_frontier_pool(
            sweep_nodes,
            wrap_y,
            compact_count_options,
            allowed_rule_pairs,
            rediscovery_limit=rediscovery_limit,
        )
        sweep_evaluation_cache = build_frontier_evaluation_cache(sweep_nodes, wrap_y)
        _sweep_row, sweep_candidates = frontier_case_analysis(
            pack_name=pack_name,
            scenario_name=scenario_name,
            nodes=sweep_nodes,
            wrap_y=wrap_y,
            rule_family="compact",
            count_options=compact_count_options,
            retained_weight=retained_weight,
            raw_pool=sweep_pool,
            evaluation_cache=sweep_evaluation_cache,
        )
        selected_candidate = next(
            candidate for candidate in sweep_candidates if candidate.current_selected
        )
        sweep_mixed_rules = {
            candidate.rule_signature
            for candidate in sweep_candidates
            if candidate.on_mixed
        }
        (
            mean_center,
            center_range,
            center_total_variation,
            crosses_midline,
            _span_range,
        ) = column_profile_geometry_metrics(sweep_nodes)
        rows.append(
            ContourSensitivityRow(
                alpha=alpha,
                selected_rule=selected_candidate.rule_signature,
                status=selected_candidate.status,
                mixed_overlap=bool(base_mixed_rules & sweep_mixed_rules),
                center_gap=selected_candidate.center_gap,
                arrival_span=selected_candidate.arrival_span,
                mean_center=mean_center,
                center_range=center_range,
                center_total_variation=center_total_variation,
                crosses_midline=crosses_midline,
            )
        )

    return rows


def selected_metric_rows_for_factory(
    dataset: str,
    perturbation_factory: Callable[
        [str, str, set[tuple[int, int]], bool],
        tuple[tuple[str, set[tuple[int, int]], int], ...],
    ],
    retained_weight: float = 1.0,
    perturbed_pool_builder: Callable[
        [set[tuple[int, int]], bool, tuple[frozenset[int], ...], tuple[tuple[frozenset[int], frozenset[int]], ...]],
        RawFrontierPool,
    ] | None = None,
) -> list[SelectedMetricCaseRow]:
    current_pool_builder = perturbed_pool_builder or collect_restricted_frontier_pool
    rows: list[SelectedMetricCaseRow] = []

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                base_raw_pool = collect_raw_frontier_pool(
                    nodes,
                    wrap_y,
                    count_options,
                )
                base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
                _base_row, base_candidates = frontier_case_analysis(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weight=retained_weight,
                    raw_pool=base_raw_pool,
                    evaluation_cache=base_evaluation_cache,
                )
                allowed_rule_pairs = base_palette_rule_pairs(base_candidates)

                for variant_name, perturbed_nodes, _node_delta in perturbation_factory(
                    pack_name,
                    scenario_name,
                    nodes,
                    wrap_y,
                ):
                    perturbed_raw_pool = current_pool_builder(
                        perturbed_nodes,
                        wrap_y,
                        count_options,
                        allowed_rule_pairs,
                    )
                    perturbed_evaluation_cache = build_frontier_evaluation_cache(
                        perturbed_nodes,
                        wrap_y,
                    )
                    perturbed_row, perturbed_candidates = frontier_case_analysis(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        nodes=perturbed_nodes,
                        wrap_y=wrap_y,
                        rule_family=rule_family,
                        count_options=count_options,
                        retained_weight=retained_weight,
                        raw_pool=perturbed_raw_pool,
                        evaluation_cache=perturbed_evaluation_cache,
                    )
                    selected_candidate = next(
                        candidate for candidate in perturbed_candidates if candidate.current_selected
                    )
                    rows.append(
                        SelectedMetricCaseRow(
                            dataset=dataset,
                            rule_family=rule_family,
                            pack_name=pack_name,
                            scenario_name=scenario_name,
                            variant_name=variant_name,
                            selected_rule=perturbed_row.selected_rule,
                            status=selected_candidate.status,
                            center_gap=selected_candidate.center_gap,
                            arrival_span=selected_candidate.arrival_span,
                        )
                    )

    return rows


def focus_observable_benchmark(
    retained_weight: float = 1.0,
    geometry_variant_limit: int = 2,
    geometry_rediscovery_limit: int = 1,
    procedural_variant_limit: int = 2,
    procedural_rediscovery_limit: int = 1,
) -> list[FocusObservableBenchmarkRow]:
    postulates = build_frontier_postulates(retained_weight)
    core_rows = run_robustness_sweep(postulates)
    geometry_rows = selected_metric_rows_for_factory(
        dataset="geometry",
        perturbation_factory=lambda pack_name, scenario_name, nodes, wrap_y: randomized_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=geometry_variant_limit,
        ),
        retained_weight=retained_weight,
        perturbed_pool_builder=lambda nodes, wrap_y, count_options, allowed_rule_pairs: (
            collect_limited_rediscovery_frontier_pool(
                nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
                rediscovery_limit=geometry_rediscovery_limit,
            )
        ),
    )
    procedural_rows = selected_metric_rows_for_factory(
        dataset="procedural",
        perturbation_factory=lambda pack_name, scenario_name, nodes, wrap_y: procedural_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=procedural_variant_limit,
        ),
        retained_weight=retained_weight,
        perturbed_pool_builder=lambda nodes, wrap_y, count_options, allowed_rule_pairs: (
            collect_limited_rediscovery_frontier_pool(
                nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
                rediscovery_limit=procedural_rediscovery_limit,
            )
        ),
    )
    contour_rows = contour_sensitivity_sweep(rediscovery_limit=procedural_rediscovery_limit)
    observables = ("box-min", "harmonic", "geometric", "arithmetic")
    benchmark_rows: list[FocusObservableBenchmarkRow] = []

    for observable in observables:
        core_preserved = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in core_rows
            if row.status == "survives"
        )
        geometry_survive_cases = sum(row.status == "survives" for row in geometry_rows)
        geometry_non_survive_cases = sum(row.status != "survives" for row in geometry_rows)
        geometry_preserved = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in geometry_rows
            if row.status == "survives"
        )
        geometry_promoted = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in geometry_rows
            if row.status != "survives"
        )
        procedural_survive_cases = sum(row.status == "survives" for row in procedural_rows)
        procedural_non_survive_cases = sum(row.status != "survives" for row in procedural_rows)
        procedural_preserved = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in procedural_rows
            if row.status == "survives"
        )
        procedural_promoted = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in procedural_rows
            if row.status != "survives"
        )
        contour_survive_cases = sum(row.status == "survives" for row in contour_rows)
        contour_survive_preserved = sum(
            classify_focus_observable(row.center_gap, row.arrival_span, observable)[1] == "survives"
            for row in contour_rows
            if row.status == "survives"
        )
        contour_miss = next(row for row in contour_rows if row.alpha == 1.0)
        contour_miss_score, contour_miss_status = classify_focus_observable(
            contour_miss.center_gap,
            contour_miss.arrival_span,
            observable,
        )
        benchmark_rows.append(
            FocusObservableBenchmarkRow(
                observable=observable,
                core_preserved=core_preserved,
                core_cases=sum(row.status == "survives" for row in core_rows),
                geometry_preserved=geometry_preserved,
                geometry_survive_cases=geometry_survive_cases,
                geometry_promoted=geometry_promoted,
                geometry_non_survive_cases=geometry_non_survive_cases,
                procedural_preserved=procedural_preserved,
                procedural_survive_cases=procedural_survive_cases,
                procedural_promoted=procedural_promoted,
                procedural_non_survive_cases=procedural_non_survive_cases,
                contour_survive_preserved=contour_survive_preserved,
                contour_survive_cases=contour_survive_cases,
                contour_miss_status=contour_miss_status,
                contour_miss_score=contour_miss_score,
            )
        )

    benchmark_rows.sort(
        key=lambda row: (
            -row.core_preserved,
            -row.geometry_preserved,
            -row.procedural_preserved,
            -row.contour_survive_preserved,
            -row.geometry_promoted,
            -row.procedural_promoted,
            row.observable,
        )
    )
    return benchmark_rows


def frontier_candidate_case_key(
    candidate: EvaluatedCandidate,
) -> tuple[str, str, str, float]:
    return (
        candidate.rule_family,
        candidate.pack_name,
        candidate.scenario_name,
        candidate.retained_weight,
    )


def frontier_scenario_case_key(
    row: FrontierScenarioRow,
) -> tuple[str, str, str, float]:
    return (
        row.rule_family,
        row.pack_name,
        row.scenario_name,
        row.retained_weight,
    )


def evaluated_candidate_quality_key(
    candidate: EvaluatedCandidate,
) -> tuple[float, ...]:
    return (
        candidate.status_rank,
        candidate.center_gap + candidate.arrival_span,
        candidate.arrival_span,
        candidate.center_gap,
        candidate.occupancy_mean,
        candidate.density,
    )


def relabel_frontier_candidate_status(
    candidate: EvaluatedCandidate,
    observable: str,
) -> EvaluatedCandidate:
    score, status = classify_focus_observable(
        candidate.center_gap,
        candidate.arrival_span,
        observable,
    )
    return replace(
        candidate,
        status=status,
        status_rank=robustness_rank(status),
        focus_score=score,
        current_selected=False,
        on_robustness=False,
        on_proper_time=False,
        on_geometry=False,
        on_mixed=False,
    )


def frontier_primary_metric(
    candidate: EvaluatedCandidate,
    ranking_mode: str,
) -> float:
    if ranking_mode == "bucketed":
        return float(candidate.status_rank)
    if ranking_mode == "continuous":
        return candidate.focus_score
    raise ValueError(f"Unknown frontier ranking mode: {ranking_mode}")


def rerank_frontier_case_candidates(
    candidates: list[EvaluatedCandidate],
    observable: str,
    ranking_mode: str = "bucketed",
) -> tuple[FrontierScenarioRow, list[EvaluatedCandidate]]:
    relabeled_candidates = [
        relabel_frontier_candidate_status(candidate, observable)
        for candidate in candidates
    ]
    if not relabeled_candidates:
        raise ValueError("Cannot rerank an empty frontier case")

    selected_identity = max(
        relabeled_candidates,
        key=lambda candidate: (
            (
                frontier_primary_metric(candidate, ranking_mode),
                candidate.center_gap + candidate.arrival_span,
                candidate.arrival_span,
                candidate.center_gap,
                candidate.occupancy_mean,
                candidate.density,
            ),
            candidate.rule_signature,
            candidate.seed_node,
        ),
    ).candidate_identity

    frontier_sets = {
        view_name: pareto_frontier_identities(relabeled_candidates, axes)
        for view_name, axes in frontier_axes(ranking_mode).items()
    }
    relabeled_candidates = [
        replace(
            candidate,
            current_selected=candidate.candidate_identity == selected_identity,
            on_robustness=candidate.candidate_identity in frontier_sets["robustness"],
            on_proper_time=candidate.candidate_identity in frontier_sets["proper_time"],
            on_geometry=candidate.candidate_identity in frontier_sets["geometry"],
            on_mixed=candidate.candidate_identity in frontier_sets["mixed"],
        )
        for candidate in relabeled_candidates
    ]
    relabeled_candidates.sort(
        key=lambda candidate: (
            candidate.current_selected,
            frontier_primary_metric(candidate, ranking_mode),
            candidate.center_gap + candidate.arrival_span,
            candidate.arrival_span,
            candidate.center_gap,
            candidate.rule_signature,
            candidate.seed_node,
        ),
        reverse=True,
    )

    selected_candidates = [candidate for candidate in relabeled_candidates if candidate.current_selected]
    selected_candidate = selected_candidates[0] if selected_candidates else None
    robustness_candidates = [candidate for candidate in relabeled_candidates if candidate.on_robustness]
    proper_time_candidates = [candidate for candidate in relabeled_candidates if candidate.on_proper_time]
    geometry_candidates = [candidate for candidate in relabeled_candidates if candidate.on_geometry]
    mixed_candidates = [candidate for candidate in relabeled_candidates if candidate.on_mixed]
    first_candidate = relabeled_candidates[0]
    row = FrontierScenarioRow(
        pack_name=first_candidate.pack_name,
        scenario_name=first_candidate.scenario_name,
        rule_family=first_candidate.rule_family,
        retained_weight=first_candidate.retained_weight,
        pool_size=len(relabeled_candidates),
        selected_rule=selected_candidate.rule_signature if selected_candidate is not None else "-",
        selected_on_robustness=selected_candidate.on_robustness if selected_candidate is not None else False,
        selected_on_proper_time=selected_candidate.on_proper_time if selected_candidate is not None else False,
        selected_on_geometry=selected_candidate.on_geometry if selected_candidate is not None else False,
        selected_on_mixed=selected_candidate.on_mixed if selected_candidate is not None else False,
        robustness_count=len(robustness_candidates),
        proper_time_count=len(proper_time_candidates),
        geometry_count=len(geometry_candidates),
        mixed_count=len(mixed_candidates),
        robustness_rules=format_frontier_rule_signatures(robustness_candidates),
        proper_time_rules=format_frontier_rule_signatures(proper_time_candidates),
        geometry_rules=format_frontier_rule_signatures(geometry_candidates),
        mixed_rules=format_frontier_rule_signatures(mixed_candidates),
    )
    return row, relabeled_candidates


def frontier_observable_ablation(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    observable: str = "harmonic",
    ranking_mode: str = "bucketed",
) -> tuple[
    list[FrontierObservableAblationRow],
    list[FrontierObservableChangeRow],
    list[FrontierScenarioRow],
    list[EvaluatedCandidate],
]:
    baseline_rows_by_case = {
        frontier_scenario_case_key(row): row
        for row in baseline_rows
    }
    grouped_candidates: DefaultDict[
        tuple[str, str, str, float],
        list[EvaluatedCandidate],
    ] = defaultdict(list)
    for candidate in baseline_candidates:
        grouped_candidates[frontier_candidate_case_key(candidate)].append(candidate)

    ablated_rows: list[FrontierScenarioRow] = []
    ablated_candidates: list[EvaluatedCandidate] = []
    change_rows: list[FrontierObservableChangeRow] = []
    aggregate_counts: DefaultDict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for case_key in sorted(grouped_candidates):
        case_candidates = grouped_candidates[case_key]
        baseline_row = baseline_rows_by_case[case_key]
        baseline_candidates_by_rule = {
            candidate.rule_signature: candidate
            for candidate in case_candidates
        }
        ablated_row, ablated_case_candidates = rerank_frontier_case_candidates(
            case_candidates,
            observable,
            ranking_mode=ranking_mode,
        )
        ablated_candidates_by_rule = {
            candidate.rule_signature: candidate
            for candidate in ablated_case_candidates
        }
        ablated_rows.append(ablated_row)
        ablated_candidates.extend(ablated_case_candidates)

        selected_candidate = next(
            candidate for candidate in ablated_case_candidates if candidate.current_selected
        )
        baseline_selected_candidate = ablated_candidates_by_rule.get(
            baseline_row.selected_rule
        )
        family_counts = aggregate_counts[ablated_row.rule_family]
        family_counts["cases"] += 1
        family_counts["selected_changes"] += (
            ablated_row.selected_rule != baseline_row.selected_rule
        )
        family_counts["selected_survives"] += selected_candidate.status == "survives"
        family_counts["selected_on_robustness"] += ablated_row.selected_on_robustness
        family_counts["selected_on_proper_time"] += ablated_row.selected_on_proper_time
        family_counts["selected_on_geometry"] += ablated_row.selected_on_geometry
        family_counts["selected_on_mixed"] += ablated_row.selected_on_mixed
        if baseline_selected_candidate is not None:
            family_counts["baseline_selected_survives"] += (
                baseline_selected_candidate.status == "survives"
            )
            family_counts["baseline_on_robustness"] += baseline_selected_candidate.on_robustness
            family_counts["baseline_on_proper_time"] += baseline_selected_candidate.on_proper_time
            family_counts["baseline_on_geometry"] += baseline_selected_candidate.on_geometry
            family_counts["baseline_on_mixed"] += baseline_selected_candidate.on_mixed

        baseline_selected_baseline = baseline_candidates_by_rule[baseline_row.selected_rule]
        if (
            ablated_row.selected_rule != baseline_row.selected_rule
            or baseline_selected_candidate is None
            or baseline_selected_candidate.status != baseline_selected_baseline.status
            or baseline_selected_candidate.on_robustness != baseline_row.selected_on_robustness
            or baseline_selected_candidate.on_proper_time != baseline_row.selected_on_proper_time
            or baseline_selected_candidate.on_geometry != baseline_row.selected_on_geometry
            or baseline_selected_candidate.on_mixed != baseline_row.selected_on_mixed
        ):
            change_rows.append(
                FrontierObservableChangeRow(
                    pack_name=ablated_row.pack_name,
                    scenario_name=ablated_row.scenario_name,
                    rule_family=ablated_row.rule_family,
                    retained_weight=ablated_row.retained_weight,
                    baseline_selected_rule=baseline_row.selected_rule,
                    observable_selected_rule=ablated_row.selected_rule,
                    baseline_selected_status=(
                        baseline_selected_candidate.status
                        if baseline_selected_candidate is not None
                        else "missing"
                    ),
                    observable_selected_status=selected_candidate.status,
                    baseline_on_robustness=(
                        baseline_selected_candidate.on_robustness
                        if baseline_selected_candidate is not None
                        else False
                    ),
                    baseline_on_proper_time=(
                        baseline_selected_candidate.on_proper_time
                        if baseline_selected_candidate is not None
                        else False
                    ),
                    baseline_on_geometry=(
                        baseline_selected_candidate.on_geometry
                        if baseline_selected_candidate is not None
                        else False
                    ),
                    baseline_on_mixed=(
                        baseline_selected_candidate.on_mixed
                        if baseline_selected_candidate is not None
                        else False
                    ),
                    observable_on_robustness=ablated_row.selected_on_robustness,
                    observable_on_proper_time=ablated_row.selected_on_proper_time,
                    observable_on_geometry=ablated_row.selected_on_geometry,
                    observable_on_mixed=ablated_row.selected_on_mixed,
                )
            )

    aggregate_rows = [
        FrontierObservableAblationRow(
            observable=f"{observable}-{ranking_mode}",
            rule_family=rule_family,
            cases=counts["cases"],
            selected_changes=counts["selected_changes"],
            selected_survives=counts["selected_survives"],
            baseline_selected_survives=counts["baseline_selected_survives"],
            selected_on_robustness=counts["selected_on_robustness"],
            selected_on_proper_time=counts["selected_on_proper_time"],
            selected_on_geometry=counts["selected_on_geometry"],
            selected_on_mixed=counts["selected_on_mixed"],
            baseline_on_robustness=counts["baseline_on_robustness"],
            baseline_on_proper_time=counts["baseline_on_proper_time"],
            baseline_on_geometry=counts["baseline_on_geometry"],
            baseline_on_mixed=counts["baseline_on_mixed"],
        )
        for rule_family, counts in aggregate_counts.items()
    ]
    aggregate_rows.sort(key=lambda row: row.rule_family)
    change_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.pack_name,
            row.scenario_name,
            row.retained_weight,
        )
    )
    return aggregate_rows, change_rows, ablated_rows, ablated_candidates


DERIVED_AXIS_METRIC_FIELDS = (
    "center_gap",
    "arrival_span",
    "min_margin",
    "geometric_focus_gap",
    "focus_score",
)


DERIVED_AXIS_BASIS_FIELDS = (
    ("full5", DERIVED_AXIS_METRIC_FIELDS),
    ("no_focus", ("center_gap", "arrival_span", "min_margin", "geometric_focus_gap")),
    ("focus3", ("center_gap", "arrival_span", "focus_score")),
    ("no_margin", ("center_gap", "arrival_span", "geometric_focus_gap", "focus_score")),
    ("action3", ("arrival_span", "min_margin", "focus_score")),
)


DERIVED_BOOTSTRAP_RANDOM_COUNT = 12
DERIVED_BOOTSTRAP_RANDOM_SEED = 17
DERIVED_BOOTSTRAP_TRANSFORM_MODES = (
    "signed_sqrt",
    "signed_log1p",
    "softsign",
)
DERIVED_TRANSFORM_STRENGTHS = (0.0, 0.25, 0.5, 0.75, 1.0)
DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_COUNT = 2
DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_SEED = 71
DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_COUNT = 8
DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED = 211
DERIVED_PROJECTION_GENERATOR_TYPES = ("raw", "row_norm", "orthonormal")
DERIVED_PROJECTION_GENERATOR_COUNT = 4
DERIVED_PROJECTION_DIMENSIONS = (2, 3, 4, 5)


def derived_metric_vector(candidate: EvaluatedCandidate) -> tuple[float, ...]:
    return tuple(float(getattr(candidate, field_name)) for field_name in DERIVED_AXIS_METRIC_FIELDS)


def derived_metric_vector_for_fields(
    candidate: EvaluatedCandidate,
    metric_fields: tuple[str, ...],
) -> tuple[float, ...]:
    return tuple(float(getattr(candidate, field_name)) for field_name in metric_fields)


def dot_product(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))


def matrix_vector_product(
    matrix: tuple[tuple[float, ...], ...],
    vector: tuple[float, ...],
) -> tuple[float, ...]:
    return tuple(
        sum(row_value * vector_value for row_value, vector_value in zip(row, vector))
        for row in matrix
    )


def normalize_vector(vector: tuple[float, ...]) -> tuple[float, ...]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm <= 0.0:
        return tuple(0.0 for _value in vector)
    return tuple(value / norm for value in vector)


def principal_component(
    covariance: tuple[tuple[float, ...], ...],
    seed: tuple[float, ...],
    iterations: int = 32,
) -> tuple[float, tuple[float, ...]]:
    vector = normalize_vector(seed)
    if all(value == 0.0 for value in vector):
        vector = tuple(1.0 if index == 0 else 0.0 for index in range(len(seed)))
    for _step in range(iterations):
        projected = matrix_vector_product(covariance, vector)
        if math.sqrt(sum(value * value for value in projected)) <= 1e-12:
            break
        vector = normalize_vector(projected)
    eigenvalue = dot_product(vector, matrix_vector_product(covariance, vector))
    return eigenvalue, vector


def deflate_covariance(
    covariance: tuple[tuple[float, ...], ...],
    eigenvalue: float,
    eigenvector: tuple[float, ...],
) -> tuple[tuple[float, ...], ...]:
    return tuple(
        tuple(
            covariance[row_index][column_index]
            - eigenvalue * eigenvector[row_index] * eigenvector[column_index]
            for column_index in range(len(covariance[row_index]))
        )
        for row_index in range(len(covariance))
    )


def derived_axis_seed_vectors(
    dimension: int,
) -> tuple[tuple[float, ...], ...]:
    all_positive = tuple(1.0 for _index in range(dimension))
    alternating = tuple(1.0 if index % 2 == 0 else -1.0 for index in range(dimension))
    staggered = tuple(
        (1.0 if index % 3 == 0 else (-1.0 if index % 3 == 1 else 0.5))
        for index in range(dimension)
    )
    return (all_positive, alternating, staggered)


def standardized_metric_rows(
    metric_rows: list[tuple[float, ...]],
) -> list[tuple[float, ...]]:
    if not metric_rows:
        return []
    dimension = len(metric_rows[0])
    means = [
        sum(row[index] for row in metric_rows) / len(metric_rows)
        for index in range(dimension)
    ]
    variances = [
        sum((row[index] - means[index]) ** 2 for row in metric_rows) / max(1, len(metric_rows) - 1)
        for index in range(dimension)
    ]
    scales = [math.sqrt(variance) if variance > 1e-12 else 1.0 for variance in variances]
    return [
        tuple((row[index] - means[index]) / scales[index] for index in range(dimension))
        for row in metric_rows
    ]


def covariance_from_standardized_rows(
    standardized_rows: list[tuple[float, ...]],
) -> tuple[tuple[float, ...], ...]:
    if not standardized_rows:
        return tuple()
    dimension = len(standardized_rows[0])
    return tuple(
        tuple(
            sum(row[left_index] * row[right_index] for row in standardized_rows) / max(1, len(standardized_rows) - 1)
            for right_index in range(dimension)
        )
        for left_index in range(dimension)
    )


def annotate_candidates_with_component_scores(
    candidates: list[EvaluatedCandidate],
    standardized_rows: list[tuple[float, ...]],
    components: list[tuple[float, tuple[float, ...]]],
) -> list[EvaluatedCandidate]:
    annotated_candidates = [
        replace(
            candidate,
            pc1_score=0.0,
            pc2_score=0.0,
            pc3_score=0.0,
        )
        for candidate in candidates
    ]
    for component_index, (_eigenvalue, eigenvector) in enumerate(components[:3]):
        annotated_candidates = [
            replace(
                candidate,
                **{
                    f"pc{component_index + 1}_score": dot_product(
                        standardized_row,
                        eigenvector,
                    )
                },
            )
            for candidate, standardized_row in zip(annotated_candidates, standardized_rows)
        ]
    return annotated_candidates


def derived_axis_components_from_metric_rows(
    candidates: list[EvaluatedCandidate],
    metric_rows: list[tuple[float, ...]],
    anchor: tuple[float, ...],
    component_count: int = 3,
) -> tuple[list[tuple[float, tuple[float, ...]]], list[EvaluatedCandidate]]:
    if not candidates or not metric_rows:
        return [], []

    dimension = len(metric_rows[0])
    standardized_rows = standardized_metric_rows(metric_rows)
    covariance = covariance_from_standardized_rows(standardized_rows)
    if all(value == 0.0 for value in anchor):
        anchor = tuple(1.0 for _field in range(dimension))
    seed_vectors = derived_axis_seed_vectors(dimension)
    working_covariance = covariance
    components: list[tuple[float, tuple[float, ...]]] = []
    for component_index in range(min(component_count, dimension)):
        default_seed = tuple(
            1.0 if metric_index == component_index else 0.0
            for metric_index in range(dimension)
        )
        eigenvalue, eigenvector = principal_component(
            working_covariance,
            seed_vectors[component_index] if component_index < len(seed_vectors) else default_seed,
        )
        if eigenvalue <= 1e-10 or all(abs(value) <= 1e-10 for value in eigenvector):
            break
        if dot_product(eigenvector, anchor) < 0.0:
            eigenvector = tuple(-value for value in eigenvector)
        components.append((eigenvalue, eigenvector))
        working_covariance = deflate_covariance(
            working_covariance,
            eigenvalue,
            eigenvector,
        )
    return components, annotate_candidates_with_component_scores(
        candidates,
        standardized_rows,
        components,
    )


def derived_axis_components(
    candidates: list[EvaluatedCandidate],
    metric_fields: tuple[str, ...],
    component_count: int = 3,
) -> tuple[list[tuple[float, tuple[float, ...]]], list[EvaluatedCandidate]]:
    if not candidates:
        return [], []

    metric_rows = [
        derived_metric_vector_for_fields(candidate, metric_fields)
        for candidate in candidates
    ]
    anchor = tuple(
        1.0 if field_name in {"center_gap", "arrival_span", "focus_score"} else 0.0
        for field_name in metric_fields
    )
    return derived_axis_components_from_metric_rows(
        candidates,
        metric_rows,
        anchor,
        component_count=component_count,
    )


def derived_axis_loadings(
    candidates: list[EvaluatedCandidate],
    component_count: int = 3,
) -> tuple[list[DerivedAxisLoadingRow], list[EvaluatedCandidate]]:
    components, annotated_candidates = derived_axis_components(
        candidates,
        DERIVED_AXIS_METRIC_FIELDS,
        component_count=component_count,
    )
    loading_rows: list[DerivedAxisLoadingRow] = []
    for component_index, (eigenvalue, eigenvector) in enumerate(components):
        loading_rows.append(
            DerivedAxisLoadingRow(
                component=f"pc{component_index + 1}",
                eigenvalue=eigenvalue,
                center_gap=eigenvector[0],
                arrival_span=eigenvector[1],
                min_margin=eigenvector[2],
                geometric_focus_gap=eigenvector[3],
                focus_score=eigenvector[4],
            )
        )
    return loading_rows, annotated_candidates


def derived_axis_frontier_views() -> dict[str, tuple[str, ...]]:
    return {
        "pc1": ("pc1_score",),
        "pc12": ("pc1_score", "pc2_score"),
        "pc123": ("pc1_score", "pc2_score", "pc3_score"),
    }


def derived_axis_signature_sets(
    candidates: list[EvaluatedCandidate],
    views: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, set[str]]:
    active_views = views or derived_axis_frontier_views()
    sets: dict[str, set[str]] = {}
    for view_name, axes in active_views.items():
        identities = pareto_frontier_identities(candidates, axes)
        sets[view_name] = {
            candidate.rule_signature
            for candidate in candidates
            if candidate.candidate_identity in identities
        }
    return sets


def derived_axis_frontier_analysis(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
) -> tuple[
    list[DerivedAxisLoadingRow],
    list[DerivedAxisScenarioRow],
    list[DerivedAxisAggregateRow],
]:
    loading_rows, annotated_candidates = derived_axis_loadings(baseline_candidates)
    scenario_rows, aggregate_rows, _pc123_signatures_by_case = evaluate_derived_axis_candidates(
        baseline_rows,
        annotated_candidates,
    )
    return loading_rows, scenario_rows, aggregate_rows


def evaluate_derived_axis_candidates(
    baseline_rows: list[FrontierScenarioRow],
    annotated_candidates: list[EvaluatedCandidate],
) -> tuple[
    list[DerivedAxisScenarioRow],
    list[DerivedAxisAggregateRow],
    dict[tuple[str, str, str, float], set[str]],
]:
    grouped_candidates: DefaultDict[
        tuple[str, str, str, float],
        list[EvaluatedCandidate],
    ] = defaultdict(list)
    for candidate in annotated_candidates:
        grouped_candidates[frontier_candidate_case_key(candidate)].append(candidate)
    baseline_rows_by_case = {
        frontier_scenario_case_key(row): row
        for row in baseline_rows
    }
    derived_views = derived_axis_frontier_views()
    scenario_rows: list[DerivedAxisScenarioRow] = []
    case_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    selected_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    pc1_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    pc12_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    pc123_sets: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    pc123_signatures_by_case: dict[tuple[str, str, str, float], set[str]] = {}

    for case_key in sorted(grouped_candidates):
        case_candidates = grouped_candidates[case_key]
        baseline_row = baseline_rows_by_case[case_key]
        frontier_identities = {
            view_name: pareto_frontier_identities(case_candidates, axes)
            for view_name, axes in derived_views.items()
        }
        selected_candidate = next(
            candidate
            for candidate in case_candidates
            if candidate.rule_signature == baseline_row.selected_rule and candidate.current_selected
        )
        pc1_candidates = [
            candidate for candidate in case_candidates if candidate.candidate_identity in frontier_identities["pc1"]
        ]
        pc12_candidates = [
            candidate for candidate in case_candidates if candidate.candidate_identity in frontier_identities["pc12"]
        ]
        pc123_candidates = [
            candidate for candidate in case_candidates if candidate.candidate_identity in frontier_identities["pc123"]
        ]
        pc123_signatures_by_case[case_key] = {
            candidate.rule_signature
            for candidate in pc123_candidates
        }
        scenario_rows.append(
            DerivedAxisScenarioRow(
                pack_name=baseline_row.pack_name,
                scenario_name=baseline_row.scenario_name,
                rule_family=baseline_row.rule_family,
                retained_weight=baseline_row.retained_weight,
                selected_rule=baseline_row.selected_rule,
                selected_on_pc1=selected_candidate.candidate_identity in frontier_identities["pc1"],
                selected_on_pc12=selected_candidate.candidate_identity in frontier_identities["pc12"],
                selected_on_pc123=selected_candidate.candidate_identity in frontier_identities["pc123"],
                pc1_count=len(pc1_candidates),
                pc12_count=len(pc12_candidates),
                pc123_count=len(pc123_candidates),
                pc1_rules=format_frontier_rule_signatures(pc1_candidates),
                pc12_rules=format_frontier_rule_signatures(pc12_candidates),
                pc123_rules=format_frontier_rule_signatures(pc123_candidates),
            )
        )
        case_triplet = (baseline_row.pack_name, baseline_row.scenario_name, baseline_row.retained_weight)
        for candidate in case_candidates:
            family_rule = (candidate.rule_family, candidate.rule_signature)
            case_sets[family_rule].add(case_triplet)
            if candidate.current_selected:
                selected_sets[family_rule].add(case_triplet)
            if candidate.candidate_identity in frontier_identities["pc1"]:
                pc1_sets[family_rule].add(case_triplet)
            if candidate.candidate_identity in frontier_identities["pc12"]:
                pc12_sets[family_rule].add(case_triplet)
            if candidate.candidate_identity in frontier_identities["pc123"]:
                pc123_sets[family_rule].add(case_triplet)

    aggregate_rows = [
        DerivedAxisAggregateRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            case_hits=len(case_sets[(rule_family, rule_signature)]),
            selected_hits=len(selected_sets[(rule_family, rule_signature)]),
            pc1_hits=len(pc1_sets[(rule_family, rule_signature)]),
            pc12_hits=len(pc12_sets[(rule_family, rule_signature)]),
            pc123_hits=len(pc123_sets[(rule_family, rule_signature)]),
        )
        for rule_family, rule_signature in case_sets
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.pc123_hits,
            -row.pc12_hits,
            -row.pc1_hits,
            -row.selected_hits,
            row.rule_signature,
            )
        )
    return scenario_rows, aggregate_rows, pc123_signatures_by_case


def derived_basis_ablation(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    basis_fields: tuple[tuple[str, tuple[str, ...]], ...] = DERIVED_AXIS_BASIS_FIELDS,
) -> list[DerivedBasisAblationRow]:
    basis_case_pc123_signatures: dict[str, dict[tuple[str, str, str, float], set[str]]] = {}
    basis_aggregate_rows: dict[str, list[DerivedAxisAggregateRow]] = {}
    basis_selected_counts: dict[str, tuple[int, int, int]] = {}

    for basis_name, metric_fields in basis_fields:
        _components, annotated_candidates = derived_axis_components(
            baseline_candidates,
            metric_fields,
        )
        scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
            baseline_rows,
            annotated_candidates,
        )
        basis_case_pc123_signatures[basis_name] = pc123_signatures_by_case
        basis_selected_counts[basis_name] = tuple(
            sum(
                getattr(row, attribute)
                for row in scenario_rows
            )
            for attribute in ("selected_on_pc1", "selected_on_pc12", "selected_on_pc123")
        )
        basis_aggregate_rows[basis_name] = aggregate_rows

    full_case_signatures = basis_case_pc123_signatures["full5"]
    ablation_rows: list[DerivedBasisAblationRow] = []
    total_cases = len(baseline_rows)
    for basis_name, metric_fields in basis_fields:
        selected_on_pc1, selected_on_pc12, selected_on_pc123 = basis_selected_counts[basis_name]
        pc123_overlap_with_full = sum(
            bool(
                basis_case_pc123_signatures[basis_name][case_key]
                & full_case_signatures[case_key]
            )
            for case_key in full_case_signatures
        )
        aggregate_rows = basis_aggregate_rows[basis_name]
        compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
        extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
        ablation_rows.append(
            DerivedBasisAblationRow(
                basis_name=basis_name,
                metrics=", ".join(metric_fields),
                dimension=len(metric_fields),
                cases=total_cases,
                selected_on_pc1=selected_on_pc1,
                selected_on_pc12=selected_on_pc12,
                selected_on_pc123=selected_on_pc123,
                pc123_overlap_with_full=pc123_overlap_with_full,
                compact_top_rule=compact_top.rule_signature if compact_top is not None else "-",
                compact_top_pc123=compact_top.pc123_hits if compact_top is not None else 0,
                extended_top_rule=extended_top.rule_signature if extended_top is not None else "-",
                extended_top_pc123=extended_top.pc123_hits if extended_top is not None else 0,
            )
        )
    return ablation_rows


def bootstrap_subset_basis_fields() -> tuple[tuple[str, tuple[str, ...]], ...]:
    rows: list[tuple[str, tuple[str, ...]]] = [("full5", DERIVED_AXIS_METRIC_FIELDS)]
    for subset_size in (3, 4):
        for subset_fields in itertools.combinations(DERIVED_AXIS_METRIC_FIELDS, subset_size):
            basis_name = f"sub{subset_size}:{'+'.join(field.replace('_', '') for field in subset_fields)}"
            rows.append((basis_name, subset_fields))
    return tuple(rows)


def random_projection_basis_specs(
    count: int = DERIVED_BOOTSTRAP_RANDOM_COUNT,
    seed: int = DERIVED_BOOTSTRAP_RANDOM_SEED,
    projection_dimension: int = 3,
) -> tuple[tuple[str, tuple[tuple[float, ...], ...]], ...]:
    rng = random.Random(seed)
    base_dimension = len(DERIVED_AXIS_METRIC_FIELDS)
    specs: list[tuple[str, tuple[tuple[float, ...], ...]]] = []
    for basis_index in range(count):
        matrix = []
        for _projection_index in range(projection_dimension):
            row = [rng.uniform(-1.0, 1.0) for _metric_index in range(base_dimension)]
            if math.sqrt(sum(value * value for value in row)) <= 1e-6:
                row[0] = 1.0
            matrix.append(tuple(row))
        specs.append((f"rand{basis_index + 1:02d}", tuple(matrix)))
    return tuple(specs)


def normalize_projection_row(row: tuple[float, ...]) -> tuple[float, ...]:
    norm = math.sqrt(sum(value * value for value in row))
    if norm <= 1e-9:
        normalized = [0.0] * len(row)
        normalized[0] = 1.0
        return tuple(normalized)
    return tuple(value / norm for value in row)


def orthonormalize_projection_matrix(
    projection_matrix: tuple[tuple[float, ...], ...],
) -> tuple[tuple[float, ...], ...]:
    vectors: list[list[float]] = []
    base_dimension = len(projection_matrix[0]) if projection_matrix else 0
    for row in projection_matrix:
        vector = [float(value) for value in row]
        for prior in vectors:
            dot = sum(value * prior_value for value, prior_value in zip(vector, prior))
            for index, prior_value in enumerate(prior):
                vector[index] -= dot * prior_value
        norm = math.sqrt(sum(value * value for value in vector))
        if norm <= 1e-9:
            fallback_axis = None
            best_remaining = -1.0
            for axis_index in range(base_dimension):
                basis = [0.0] * base_dimension
                basis[axis_index] = 1.0
                for prior in vectors:
                    dot = sum(value * prior_value for value, prior_value in zip(basis, prior))
                    for index, prior_value in enumerate(prior):
                        basis[index] -= dot * prior_value
                basis_norm = math.sqrt(sum(value * value for value in basis))
                if basis_norm > best_remaining:
                    best_remaining = basis_norm
                    fallback_axis = [value / basis_norm for value in basis] if basis_norm > 1e-9 else None
            if fallback_axis is None:
                fallback_axis = [0.0] * base_dimension
                if base_dimension:
                    fallback_axis[0] = 1.0
            vectors.append(fallback_axis)
            continue
        vectors.append([value / norm for value in vector])
    return tuple(tuple(vector) for vector in vectors)


def projection_matrix_variant(
    projection_matrix: tuple[tuple[float, ...], ...],
    generator: str,
) -> tuple[tuple[float, ...], ...]:
    if generator == "raw":
        return projection_matrix
    if generator == "row_norm":
        return tuple(normalize_projection_row(row) for row in projection_matrix)
    if generator == "orthonormal":
        return orthonormalize_projection_matrix(projection_matrix)
    raise ValueError(f"Unknown projection generator: {generator}")


def projected_metric_rows(
    candidates: list[EvaluatedCandidate],
    projection_matrix: tuple[tuple[float, ...], ...],
) -> tuple[list[tuple[float, ...]], tuple[float, ...]]:
    base_rows = [derived_metric_vector(candidate) for candidate in candidates]
    projected_rows = [
        tuple(
            sum(weight * value for weight, value in zip(projection_row, base_row))
            for projection_row in projection_matrix
        )
        for base_row in base_rows
    ]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    projected_anchor = tuple(
        sum(weight * value for weight, value in zip(projection_row, base_anchor))
        for projection_row in projection_matrix
    )
    return projected_rows, projected_anchor


def transform_metric_value(value: float, mode: str, strength: float = 1.0) -> float:
    if mode == "identity" or strength <= 0.0:
        return value
    full_value: float
    if mode == "signed_sqrt":
        full_value = math.copysign(math.sqrt(abs(value)), value) if value != 0.0 else 0.0
    elif mode == "signed_log1p":
        full_value = math.copysign(math.log1p(abs(value)), value) if value != 0.0 else 0.0
    elif mode == "softsign":
        full_value = value / (1.0 + abs(value)) if value != 0.0 else 0.0
    else:
        raise ValueError(f"Unknown metric transform mode: {mode}")
    if strength >= 1.0:
        return full_value
    return (1.0 - strength) * value + strength * full_value


def transform_metric_rows(
    metric_rows: list[tuple[float, ...]],
    mode: str,
    strength: float = 1.0,
) -> list[tuple[float, ...]]:
    return [
        tuple(transform_metric_value(value, mode, strength) for value in row)
        for row in metric_rows
    ]


def transform_anchor(
    anchor: tuple[float, ...],
    mode: str,
    strength: float = 1.0,
) -> tuple[float, ...]:
    return tuple(transform_metric_value(value, mode, strength) for value in anchor)


def project_metric_rows_and_anchor(
    metric_rows: list[tuple[float, ...]],
    anchor: tuple[float, ...],
    projection_matrix: tuple[tuple[float, ...], ...],
) -> tuple[list[tuple[float, ...]], tuple[float, ...]]:
    projected_rows = [
        tuple(
            sum(weight * value for weight, value in zip(projection_row, row))
            for projection_row in projection_matrix
        )
        for row in metric_rows
    ]
    projected_anchor = tuple(
        sum(weight * value for weight, value in zip(projection_row, anchor))
        for projection_row in projection_matrix
    )
    return projected_rows, projected_anchor


def derived_bootstrap_ensemble(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    random_basis_count: int = DERIVED_BOOTSTRAP_RANDOM_COUNT,
) -> tuple[list[DerivedBootstrapBasisRow], list[DerivedBootstrapStabilityRow]]:
    subset_specs = bootstrap_subset_basis_fields()
    random_specs = random_projection_basis_specs(count=random_basis_count)
    basis_case_pc123_signatures: dict[str, dict[tuple[str, str, str, float], set[str]]] = {}
    basis_rows: list[DerivedBootstrapBasisRow] = []
    family_rule_case_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)
    family_rule_basis_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_subset_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_linear_random_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_nonlinear_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_top_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)

    def record_basis(
        basis_name: str,
        basis_type: str,
        basis_dimension: int,
        annotated_candidates: list[EvaluatedCandidate],
    ) -> None:
        scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
            baseline_rows,
            annotated_candidates,
        )
        basis_case_pc123_signatures[basis_name] = pc123_signatures_by_case
        selected_on_pc123 = sum(row.selected_on_pc123 for row in scenario_rows)
        compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
        extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
        if compact_top is not None:
            family_rule_top_hits[(compact_top.rule_family, compact_top.rule_signature)] += 1
        if extended_top is not None:
            family_rule_top_hits[(extended_top.rule_family, extended_top.rule_signature)] += 1
        for aggregate_row in aggregate_rows:
            family_rule = (aggregate_row.rule_family, aggregate_row.rule_signature)
            if aggregate_row.pc123_hits > 0:
                family_rule_basis_hits[family_rule].add(basis_name)
                if basis_type == "subset":
                    family_rule_subset_hits[family_rule].add(basis_name)
                elif basis_type == "linear-random":
                    family_rule_linear_random_hits[family_rule].add(basis_name)
                else:
                    family_rule_nonlinear_hits[family_rule].add(basis_name)
                family_rule_case_hits[family_rule] += aggregate_row.pc123_hits
        basis_rows.append(
            DerivedBootstrapBasisRow(
                basis_name=basis_name,
                basis_type=basis_type,
                dimension=basis_dimension,
                cases=len(baseline_rows),
                selected_on_pc123=selected_on_pc123,
                pc123_overlap_with_full=0,
                compact_top_rule=compact_top.rule_signature if compact_top is not None else "-",
                compact_top_pc123=compact_top.pc123_hits if compact_top is not None else 0,
                extended_top_rule=extended_top.rule_signature if extended_top is not None else "-",
                extended_top_pc123=extended_top.pc123_hits if extended_top is not None else 0,
            )
        )

    for basis_name, metric_fields in subset_specs:
        _components, annotated_candidates = derived_axis_components(
            baseline_candidates,
            metric_fields,
        )
        record_basis(basis_name, "subset", len(metric_fields), annotated_candidates)

    for basis_name, projection_matrix in random_specs:
        metric_rows, anchor = project_metric_rows_and_anchor(
            base_metric_rows,
            base_anchor,
            projection_matrix,
        )
        _components, annotated_candidates = derived_axis_components_from_metric_rows(
            baseline_candidates,
            metric_rows,
            anchor,
        )
        record_basis(basis_name, "linear-random", len(projection_matrix), annotated_candidates)

    for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
        transformed_rows = transform_metric_rows(base_metric_rows, transform_mode)
        transformed_anchor = transform_anchor(base_anchor, transform_mode)
        _components, annotated_candidates = derived_axis_components_from_metric_rows(
            baseline_candidates,
            transformed_rows,
            transformed_anchor,
        )
        record_basis(f"xform:{transform_mode}", "nonlinear", len(DERIVED_AXIS_METRIC_FIELDS), annotated_candidates)

        transform_random_specs = random_projection_basis_specs(
            count=DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_COUNT,
            seed=DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_SEED + transform_index,
        )
        for random_name, projection_matrix in transform_random_specs:
            projected_rows, projected_anchor = project_metric_rows_and_anchor(
                transformed_rows,
                transformed_anchor,
                projection_matrix,
            )
            _components, annotated_candidates = derived_axis_components_from_metric_rows(
                baseline_candidates,
                projected_rows,
                projected_anchor,
            )
            record_basis(
                f"{transform_mode}:{random_name}",
                "nonlinear",
                len(projection_matrix),
                annotated_candidates,
            )

    full_signatures = basis_case_pc123_signatures["full5"]
    for row in basis_rows:
        row.pc123_overlap_with_full = sum(
            bool(
                basis_case_pc123_signatures[row.basis_name][case_key]
                & full_signatures[case_key]
            )
            for case_key in full_signatures
        )

    stability_rows = [
        DerivedBootstrapStabilityRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            basis_hits=len(family_rule_basis_hits[(rule_family, rule_signature)]),
            subset_basis_hits=len(family_rule_subset_hits[(rule_family, rule_signature)]),
            linear_random_hits=len(family_rule_linear_random_hits[(rule_family, rule_signature)]),
            nonlinear_basis_hits=len(family_rule_nonlinear_hits[(rule_family, rule_signature)]),
            case_basis_hits=family_rule_case_hits[(rule_family, rule_signature)],
            top_basis_hits=family_rule_top_hits[(rule_family, rule_signature)],
        )
        for rule_family, rule_signature in family_rule_basis_hits
    ]
    basis_rows.sort(
        key=lambda row: (
            row.basis_type != "subset",
            row.basis_name,
        )
    )
    stability_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.basis_hits,
            -row.case_basis_hits,
            -row.top_basis_hits,
            row.rule_signature,
        )
    )
    return basis_rows, stability_rows


def derived_transform_strength_sweep(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    random_projection_count: int = DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_COUNT,
) -> tuple[
    list[DerivedTransformBreakRow],
    list[DerivedTransformStrengthRow],
    list[DerivedTransformStabilityRow],
]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    full_components, full_candidates = derived_axis_components(
        baseline_candidates,
        DERIVED_AXIS_METRIC_FIELDS,
    )
    _full_scenario_rows, _full_aggregate_rows, full_pc123_signatures = evaluate_derived_axis_candidates(
        baseline_rows,
        full_candidates,
    )
    del full_components

    strength_rows: list[DerivedTransformStrengthRow] = []
    family_rule_basis_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_direct_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_projected_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_top_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)

    def evaluate_strength_basis(
        basis_name: str,
        mode: str,
        strength: float,
        variant_name: str,
        metric_rows: list[tuple[float, ...]],
        anchor: tuple[float, ...],
    ) -> None:
        _components, annotated_candidates = derived_axis_components_from_metric_rows(
            baseline_candidates,
            metric_rows,
            anchor,
        )
        scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
            baseline_rows,
            annotated_candidates,
        )
        compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
        extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
        if compact_top is not None:
            family_rule_top_hits[(compact_top.rule_family, compact_top.rule_signature)] += 1
        if extended_top is not None:
            family_rule_top_hits[(extended_top.rule_family, extended_top.rule_signature)] += 1
        selected_on_pc123 = sum(row.selected_on_pc123 for row in scenario_rows)
        pc123_overlap_with_full = sum(
            bool(pc123_signatures_by_case[case_key] & full_pc123_signatures[case_key])
            for case_key in full_pc123_signatures
        )
        strength_rows.append(
            DerivedTransformStrengthRow(
                basis_name=basis_name,
                mode=mode,
                strength=strength,
                variant_name=variant_name,
                selected_on_pc123=selected_on_pc123,
                pc123_overlap_with_full=pc123_overlap_with_full,
                compact_top_rule=compact_top.rule_signature if compact_top is not None else "-",
                compact_top_pc123=compact_top.pc123_hits if compact_top is not None else 0,
                extended_top_rule=extended_top.rule_signature if extended_top is not None else "-",
                extended_top_pc123=extended_top.pc123_hits if extended_top is not None else 0,
            )
        )
        is_direct = variant_name == "direct"
        for aggregate_row in aggregate_rows:
            if aggregate_row.pc123_hits <= 0:
                continue
            family_rule = (aggregate_row.rule_family, aggregate_row.rule_signature)
            family_rule_basis_hits[family_rule].add(basis_name)
            if is_direct:
                family_rule_direct_hits[family_rule].add(basis_name)
            else:
                family_rule_projected_hits[family_rule].add(basis_name)

    for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
        transform_random_specs = random_projection_basis_specs(
            count=random_projection_count,
            seed=DERIVED_BOOTSTRAP_TRANSFORM_RANDOM_SEED + transform_index,
        )
        for strength in strengths:
            transformed_rows = transform_metric_rows(
                base_metric_rows,
                transform_mode,
                strength=strength,
            )
            transformed_anchor = transform_anchor(
                base_anchor,
                transform_mode,
                strength=strength,
            )
            evaluate_strength_basis(
                basis_name=f"{transform_mode}:s{strength:.2f}:direct",
                mode=transform_mode,
                strength=strength,
                variant_name="direct",
                metric_rows=transformed_rows,
                anchor=transformed_anchor,
            )
            for random_name, projection_matrix in transform_random_specs:
                projected_rows, projected_anchor = project_metric_rows_and_anchor(
                    transformed_rows,
                    transformed_anchor,
                    projection_matrix,
                )
                evaluate_strength_basis(
                    basis_name=f"{transform_mode}:s{strength:.2f}:{random_name}",
                    mode=transform_mode,
                    strength=strength,
                    variant_name=random_name,
                    metric_rows=projected_rows,
                    anchor=projected_anchor,
                )

    break_rows: list[DerivedTransformBreakRow] = []
    total_cases = len(baseline_rows)
    for mode in DERIVED_BOOTSTRAP_TRANSFORM_MODES:
        mode_rows = [row for row in strength_rows if row.mode == mode]
        direct_rows = sorted(
            (row for row in mode_rows if row.variant_name == "direct"),
            key=lambda row: row.strength,
        )
        projected_rows = sorted(
            (row for row in mode_rows if row.variant_name != "direct"),
            key=lambda row: (row.strength, row.variant_name),
        )
        direct_baseline = direct_rows[0] if direct_rows else None
        direct_break_strength = next(
            (
                row.strength
                for row in direct_rows
                if direct_baseline is not None
                and row.strength > direct_baseline.strength
                and (
                    row.pc123_overlap_with_full < direct_baseline.pc123_overlap_with_full
                    or row.selected_on_pc123 < direct_baseline.selected_on_pc123
                )
            ),
            None,
        )
        projected_baselines = {
            row.variant_name: row
            for row in projected_rows
            if row.strength == min(strengths)
        }
        projected_break_strength = next(
            (
                row.strength
                for row in projected_rows
                if row.variant_name in projected_baselines
                and row.strength > projected_baselines[row.variant_name].strength
                and (
                    row.pc123_overlap_with_full < projected_baselines[row.variant_name].pc123_overlap_with_full
                    or row.selected_on_pc123 < projected_baselines[row.variant_name].selected_on_pc123
                )
            ),
            None,
        )
        weakest_row = min(
            mode_rows,
            key=lambda row: (
                row.pc123_overlap_with_full,
                row.selected_on_pc123,
                row.variant_name,
                row.strength,
            ),
        )
        break_rows.append(
            DerivedTransformBreakRow(
                mode=mode,
                direct_transform_break_strength=direct_break_strength,
                projected_transform_break_strength=projected_break_strength,
                weakest_basis_name=weakest_row.basis_name,
                weakest_overlap=weakest_row.pc123_overlap_with_full,
                weakest_selected_on_pc123=weakest_row.selected_on_pc123,
            )
        )

    stability_rows = [
        DerivedTransformStabilityRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            basis_hits=len(family_rule_basis_hits[(rule_family, rule_signature)]),
            direct_hits=len(family_rule_direct_hits[(rule_family, rule_signature)]),
            projected_hits=len(family_rule_projected_hits[(rule_family, rule_signature)]),
            top_hits=family_rule_top_hits[(rule_family, rule_signature)],
        )
        for rule_family, rule_signature in family_rule_basis_hits
    ]
    strength_rows.sort(
        key=lambda row: (
            row.mode,
            row.strength,
            row.variant_name != "direct",
            row.variant_name,
        )
    )
    break_rows.sort(key=lambda row: row.mode)
    stability_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.basis_hits,
            -row.top_hits,
            row.rule_signature,
        )
    )
    return break_rows, strength_rows, stability_rows


def derived_transform_projection_bootstrap(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    projection_count: int = DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_COUNT,
) -> tuple[list[DerivedProjectionBootstrapRow], list[DerivedProjectionStabilityRow]]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    _full_components, full_candidates = derived_axis_components(
        baseline_candidates,
        DERIVED_AXIS_METRIC_FIELDS,
    )
    _full_scenario_rows, _full_aggregate_rows, full_pc123_signatures = evaluate_derived_axis_candidates(
        baseline_rows,
        full_candidates,
    )

    basis_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    top_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)
    bootstrap_rows: list[DerivedProjectionBootstrapRow] = []

    for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
        for strength in strengths:
            transformed_rows = transform_metric_rows(
                base_metric_rows,
                transform_mode,
                strength=strength,
            )
            transformed_anchor = transform_anchor(
                base_anchor,
                transform_mode,
                strength=strength,
            )
            random_specs = random_projection_basis_specs(
                count=projection_count,
                seed=(
                    DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED
                    + 100 * transform_index
                    + int(round(strength * 100))
                ),
            )

            projection_overlaps: list[int] = []
            projection_selected: list[int] = []
            compact_basis_counts: Counter[str] = Counter()
            compact_top_counts: Counter[str] = Counter()
            extended_basis_counts: Counter[str] = Counter()
            extended_top_counts: Counter[str] = Counter()

            for random_name, projection_matrix in random_specs:
                projected_rows, projected_anchor = project_metric_rows_and_anchor(
                    transformed_rows,
                    transformed_anchor,
                    projection_matrix,
                )
                _components, annotated_candidates = derived_axis_components_from_metric_rows(
                    baseline_candidates,
                    projected_rows,
                    projected_anchor,
                )
                scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
                    baseline_rows,
                    annotated_candidates,
                )
                basis_name = f"{transform_mode}:s{strength:.2f}:{random_name}"
                overlap = sum(
                    bool(pc123_signatures_by_case[case_key] & full_pc123_signatures[case_key])
                    for case_key in full_pc123_signatures
                )
                projection_overlaps.append(overlap)
                projection_selected.append(sum(row.selected_on_pc123 for row in scenario_rows))

                compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
                extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
                if compact_top is not None:
                    compact_top_counts[compact_top.rule_signature] += 1
                    top_hits[(compact_top.rule_family, compact_top.rule_signature)] += 1
                if extended_top is not None:
                    extended_top_counts[extended_top.rule_signature] += 1
                    top_hits[(extended_top.rule_family, extended_top.rule_signature)] += 1

                for aggregate_row in aggregate_rows:
                    if aggregate_row.pc123_hits <= 0:
                        continue
                    family_rule = (aggregate_row.rule_family, aggregate_row.rule_signature)
                    basis_hits[family_rule].add(basis_name)
                    if aggregate_row.rule_family == "compact":
                        compact_basis_counts[aggregate_row.rule_signature] += 1
                    else:
                        extended_basis_counts[aggregate_row.rule_signature] += 1

            compact_dominant_rule = max(
                compact_basis_counts,
                key=lambda signature: (
                    compact_basis_counts[signature],
                    compact_top_counts[signature],
                    signature,
                ),
            )
            extended_dominant_rule = max(
                extended_basis_counts,
                key=lambda signature: (
                    extended_basis_counts[signature],
                    extended_top_counts[signature],
                    signature,
                ),
            )
            bootstrap_rows.append(
                DerivedProjectionBootstrapRow(
                    mode=transform_mode,
                    strength=strength,
                    projections=len(random_specs),
                    overlap_min=min(projection_overlaps),
                    overlap_avg=sum(projection_overlaps) / len(projection_overlaps),
                    selected_min=min(projection_selected),
                    selected_avg=sum(projection_selected) / len(projection_selected),
                    compact_dominant_rule=compact_dominant_rule,
                    compact_dominant_basis_hits=compact_basis_counts[compact_dominant_rule],
                    compact_dominant_top_hits=compact_top_counts[compact_dominant_rule],
                    extended_dominant_rule=extended_dominant_rule,
                    extended_dominant_basis_hits=extended_basis_counts[extended_dominant_rule],
                    extended_dominant_top_hits=extended_top_counts[extended_dominant_rule],
                )
            )

    stability_rows = [
        DerivedProjectionStabilityRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            basis_hits=len(basis_hits[(rule_family, rule_signature)]),
            top_hits=top_hits[(rule_family, rule_signature)],
        )
        for rule_family, rule_signature in basis_hits
    ]
    bootstrap_rows.sort(key=lambda row: (row.mode, row.strength))
    stability_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.basis_hits,
            -row.top_hits,
            row.rule_signature,
        )
    )
    return bootstrap_rows, stability_rows


def derived_projection_generator_ablation(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    generator_types: tuple[str, ...] = DERIVED_PROJECTION_GENERATOR_TYPES,
    projection_count: int = DERIVED_PROJECTION_GENERATOR_COUNT,
) -> list[ProjectionGeneratorAblationRow]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    _full_components, full_candidates = derived_axis_components(
        baseline_candidates,
        DERIVED_AXIS_METRIC_FIELDS,
    )
    _full_scenario_rows, _full_aggregate_rows, full_pc123_signatures = evaluate_derived_axis_candidates(
        baseline_rows,
        full_candidates,
    )

    rows: list[ProjectionGeneratorAblationRow] = []
    for generator in generator_types:
        overlaps: list[int] = []
        selecteds: list[int] = []
        weakest_basis_name = "-"
        weakest_pair: tuple[int, int] | None = None
        compact_basis_counts: Counter[str] = Counter()
        compact_top_counts: Counter[str] = Counter()
        extended_basis_counts: Counter[str] = Counter()
        extended_top_counts: Counter[str] = Counter()

        for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
            for strength in strengths:
                transformed_rows = transform_metric_rows(
                    base_metric_rows,
                    transform_mode,
                    strength=strength,
                )
                transformed_anchor = transform_anchor(
                    base_anchor,
                    transform_mode,
                    strength=strength,
                )
                random_specs = random_projection_basis_specs(
                    count=projection_count,
                    seed=(
                        DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED
                        + 100 * transform_index
                        + int(round(strength * 100))
                    ),
                )
                for random_name, projection_matrix in random_specs:
                    basis_name = f"{generator}:{transform_mode}:s{strength:.2f}:{random_name}"
                    adjusted_projection = projection_matrix_variant(
                        projection_matrix,
                        generator,
                    )
                    projected_rows, projected_anchor = project_metric_rows_and_anchor(
                        transformed_rows,
                        transformed_anchor,
                        adjusted_projection,
                    )
                    _components, annotated_candidates = derived_axis_components_from_metric_rows(
                        baseline_candidates,
                        projected_rows,
                        projected_anchor,
                    )
                    scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
                        baseline_rows,
                        annotated_candidates,
                    )
                    overlap = sum(
                        bool(pc123_signatures_by_case[case_key] & full_pc123_signatures[case_key])
                        for case_key in full_pc123_signatures
                    )
                    selected_on_pc123 = sum(row.selected_on_pc123 for row in scenario_rows)
                    overlaps.append(overlap)
                    selecteds.append(selected_on_pc123)
                    pair = (overlap, selected_on_pc123)
                    if weakest_pair is None or pair < weakest_pair:
                        weakest_pair = pair
                        weakest_basis_name = basis_name

                    compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
                    extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
                    if compact_top is not None:
                        compact_top_counts[compact_top.rule_signature] += 1
                    if extended_top is not None:
                        extended_top_counts[extended_top.rule_signature] += 1
                    for aggregate_row in aggregate_rows:
                        if aggregate_row.pc123_hits <= 0:
                            continue
                        if aggregate_row.rule_family == "compact":
                            compact_basis_counts[aggregate_row.rule_signature] += 1
                        else:
                            extended_basis_counts[aggregate_row.rule_signature] += 1

        compact_dominant_rule = max(
            compact_basis_counts,
            key=lambda signature: (
                compact_basis_counts[signature],
                compact_top_counts[signature],
                signature,
            ),
        )
        extended_dominant_rule = max(
            extended_basis_counts,
            key=lambda signature: (
                extended_basis_counts[signature],
                extended_top_counts[signature],
                signature,
            ),
        )
        rows.append(
            ProjectionGeneratorAblationRow(
                generator=generator,
                bases=len(overlaps),
                weakest_basis_name=weakest_basis_name,
                overlap_min=min(overlaps),
                overlap_avg=sum(overlaps) / len(overlaps),
                selected_min=min(selecteds),
                selected_avg=sum(selecteds) / len(selecteds),
                compact_dominant_rule=compact_dominant_rule,
                compact_dominant_basis_hits=compact_basis_counts[compact_dominant_rule],
                compact_dominant_top_hits=compact_top_counts[compact_dominant_rule],
                extended_dominant_rule=extended_dominant_rule,
                extended_dominant_basis_hits=extended_basis_counts[extended_dominant_rule],
                extended_dominant_top_hits=extended_top_counts[extended_dominant_rule],
            )
        )

    rows.sort(key=lambda row: row.generator)
    return rows


def derived_projection_dimension_ablation(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    projection_dimensions: tuple[int, ...] = DERIVED_PROJECTION_DIMENSIONS,
    projection_count: int = DERIVED_PROJECTION_GENERATOR_COUNT,
    generator: str = "orthonormal",
) -> list[ProjectionDimensionAblationRow]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    _full_components, full_candidates = derived_axis_components(
        baseline_candidates,
        DERIVED_AXIS_METRIC_FIELDS,
    )
    _full_scenario_rows, _full_aggregate_rows, full_pc123_signatures = evaluate_derived_axis_candidates(
        baseline_rows,
        full_candidates,
    )

    rows: list[ProjectionDimensionAblationRow] = []
    for projection_dimension in projection_dimensions:
        overlaps: list[int] = []
        selecteds: list[int] = []
        weakest_basis_name = "-"
        weakest_pair: tuple[int, int] | None = None
        compact_basis_counts: Counter[str] = Counter()
        compact_top_counts: Counter[str] = Counter()
        extended_basis_counts: Counter[str] = Counter()
        extended_top_counts: Counter[str] = Counter()

        for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
            for strength in strengths:
                transformed_rows = transform_metric_rows(
                    base_metric_rows,
                    transform_mode,
                    strength=strength,
                )
                transformed_anchor = transform_anchor(
                    base_anchor,
                    transform_mode,
                    strength=strength,
                )
                random_specs = random_projection_basis_specs(
                    count=projection_count,
                    seed=(
                        DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED
                        + 100 * transform_index
                        + int(round(strength * 100))
                    ),
                    projection_dimension=projection_dimension,
                )
                for random_name, projection_matrix in random_specs:
                    basis_name = f"d{projection_dimension}:{transform_mode}:s{strength:.2f}:{random_name}"
                    adjusted_projection = projection_matrix_variant(
                        projection_matrix,
                        generator,
                    )
                    projected_rows, projected_anchor = project_metric_rows_and_anchor(
                        transformed_rows,
                        transformed_anchor,
                        adjusted_projection,
                    )
                    _components, annotated_candidates = derived_axis_components_from_metric_rows(
                        baseline_candidates,
                        projected_rows,
                        projected_anchor,
                    )
                    scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
                        baseline_rows,
                        annotated_candidates,
                    )
                    overlap = sum(
                        bool(pc123_signatures_by_case[case_key] & full_pc123_signatures[case_key])
                        for case_key in full_pc123_signatures
                    )
                    selected_on_pc123 = sum(row.selected_on_pc123 for row in scenario_rows)
                    overlaps.append(overlap)
                    selecteds.append(selected_on_pc123)
                    pair = (overlap, selected_on_pc123)
                    if weakest_pair is None or pair < weakest_pair:
                        weakest_pair = pair
                        weakest_basis_name = basis_name

                    compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
                    extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
                    if compact_top is not None:
                        compact_top_counts[compact_top.rule_signature] += 1
                    if extended_top is not None:
                        extended_top_counts[extended_top.rule_signature] += 1
                    for aggregate_row in aggregate_rows:
                        if aggregate_row.pc123_hits <= 0:
                            continue
                        if aggregate_row.rule_family == "compact":
                            compact_basis_counts[aggregate_row.rule_signature] += 1
                        else:
                            extended_basis_counts[aggregate_row.rule_signature] += 1

        compact_dominant_rule = max(
            compact_basis_counts,
            key=lambda signature: (
                compact_basis_counts[signature],
                compact_top_counts[signature],
                signature,
            ),
        )
        extended_dominant_rule = max(
            extended_basis_counts,
            key=lambda signature: (
                extended_basis_counts[signature],
                extended_top_counts[signature],
                signature,
            ),
        )
        rows.append(
            ProjectionDimensionAblationRow(
                dimension=projection_dimension,
                bases=len(overlaps),
                weakest_basis_name=weakest_basis_name,
                overlap_min=min(overlaps),
                overlap_avg=sum(overlaps) / len(overlaps),
                selected_min=min(selecteds),
                selected_avg=sum(selecteds) / len(selecteds),
                compact_dominant_rule=compact_dominant_rule,
                compact_dominant_basis_hits=compact_basis_counts[compact_dominant_rule],
                compact_dominant_top_hits=compact_top_counts[compact_dominant_rule],
                extended_dominant_rule=extended_dominant_rule,
                extended_dominant_basis_hits=extended_basis_counts[extended_dominant_rule],
                extended_dominant_top_hits=extended_top_counts[extended_dominant_rule],
            )
        )

    rows.sort(key=lambda row: row.dimension)
    return rows


def derived_projection_family_stability_map(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    projection_dimension: int = 4,
    generator: str = "orthonormal",
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    projection_count: int = DERIVED_PROJECTION_GENERATOR_COUNT,
) -> tuple[list[ProjectionFamilyBasisRow], list[ProjectionFamilyStabilityRow]]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    _full_components, full_candidates = derived_axis_components(
        baseline_candidates,
        DERIVED_AXIS_METRIC_FIELDS,
    )
    _full_scenario_rows, _full_aggregate_rows, full_pc123_signatures = evaluate_derived_axis_candidates(
        baseline_rows,
        full_candidates,
    )

    basis_rows: list[ProjectionFamilyBasisRow] = []
    family_rule_basis_hits: DefaultDict[tuple[str, str], set[str]] = defaultdict(set)
    family_rule_case_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)
    family_rule_top_hits: DefaultDict[tuple[str, str], int] = defaultdict(int)

    for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
        for strength in strengths:
            transformed_rows = transform_metric_rows(
                base_metric_rows,
                transform_mode,
                strength=strength,
            )
            transformed_anchor = transform_anchor(
                base_anchor,
                transform_mode,
                strength=strength,
            )
            random_specs = random_projection_basis_specs(
                count=projection_count,
                seed=(
                    DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED
                    + 100 * transform_index
                    + int(round(strength * 100))
                ),
                projection_dimension=projection_dimension,
            )
            for random_name, projection_matrix in random_specs:
                basis_name = f"{generator}:d{projection_dimension}:{transform_mode}:s{strength:.2f}:{random_name}"
                adjusted_projection = projection_matrix_variant(
                    projection_matrix,
                    generator,
                )
                projected_rows, projected_anchor = project_metric_rows_and_anchor(
                    transformed_rows,
                    transformed_anchor,
                    adjusted_projection,
                )
                _components, annotated_candidates = derived_axis_components_from_metric_rows(
                    baseline_candidates,
                    projected_rows,
                    projected_anchor,
                )
                scenario_rows, aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
                    baseline_rows,
                    annotated_candidates,
                )
                selected_on_pc123 = sum(row.selected_on_pc123 for row in scenario_rows)
                overlap = sum(
                    bool(pc123_signatures_by_case[case_key] & full_pc123_signatures[case_key])
                    for case_key in full_pc123_signatures
                )
                compact_top = next((row for row in aggregate_rows if row.rule_family == "compact"), None)
                extended_top = next((row for row in aggregate_rows if row.rule_family == "extended"), None)
                if compact_top is not None:
                    family_rule_top_hits[(compact_top.rule_family, compact_top.rule_signature)] += 1
                if extended_top is not None:
                    family_rule_top_hits[(extended_top.rule_family, extended_top.rule_signature)] += 1
                for aggregate_row in aggregate_rows:
                    if aggregate_row.pc123_hits <= 0:
                        continue
                    family_rule = (aggregate_row.rule_family, aggregate_row.rule_signature)
                    family_rule_basis_hits[family_rule].add(basis_name)
                    family_rule_case_hits[family_rule] += aggregate_row.pc123_hits

                basis_rows.append(
                    ProjectionFamilyBasisRow(
                        basis_name=basis_name,
                        mode=transform_mode,
                        strength=strength,
                        selected_on_pc123=selected_on_pc123,
                        pc123_overlap_with_full=overlap,
                        compact_top_rule=compact_top.rule_signature if compact_top is not None else "-",
                        compact_top_pc123=compact_top.pc123_hits if compact_top is not None else 0,
                        extended_top_rule=extended_top.rule_signature if extended_top is not None else "-",
                        extended_top_pc123=extended_top.pc123_hits if extended_top is not None else 0,
                    )
                )

    stability_rows = [
        ProjectionFamilyStabilityRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            basis_hits=len(family_rule_basis_hits[(rule_family, rule_signature)]),
            case_hits=family_rule_case_hits[(rule_family, rule_signature)],
            top_hits=family_rule_top_hits[(rule_family, rule_signature)],
        )
        for rule_family, rule_signature in family_rule_basis_hits
    ]
    basis_rows.sort(
        key=lambda row: (
            row.mode,
            row.strength,
            row.basis_name,
        )
    )
    stability_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.basis_hits,
            -row.case_hits,
            -row.top_hits,
            row.rule_signature,
        )
    )
    return basis_rows, stability_rows


def derived_projection_family_case_core_analysis(
    baseline_rows: list[FrontierScenarioRow],
    baseline_candidates: list[EvaluatedCandidate],
    projection_dimension: int = 4,
    generator: str = "orthonormal",
    strengths: tuple[float, ...] = DERIVED_TRANSFORM_STRENGTHS,
    projection_count: int = DERIVED_PROJECTION_GENERATOR_COUNT,
) -> tuple[list[ProjectionFamilyCaseCoreRow], list[ProjectionFamilyCoreAggregateRow]]:
    base_metric_rows = [derived_metric_vector(candidate) for candidate in baseline_candidates]
    base_anchor = (1.0, 1.0, 0.0, 0.0, 1.0)
    baseline_rows_by_case = {
        frontier_scenario_case_key(row): row
        for row in baseline_rows
    }
    case_signature_sets: DefaultDict[
        tuple[str, str, str, float],
        list[set[str]],
    ] = defaultdict(list)

    for transform_index, transform_mode in enumerate(DERIVED_BOOTSTRAP_TRANSFORM_MODES):
        for strength in strengths:
            transformed_rows = transform_metric_rows(
                base_metric_rows,
                transform_mode,
                strength=strength,
            )
            transformed_anchor = transform_anchor(
                base_anchor,
                transform_mode,
                strength=strength,
            )
            random_specs = random_projection_basis_specs(
                count=projection_count,
                seed=(
                    DERIVED_TRANSFORM_PROJECTION_BOOTSTRAP_SEED
                    + 100 * transform_index
                    + int(round(strength * 100))
                ),
                projection_dimension=projection_dimension,
            )
            for _random_name, projection_matrix in random_specs:
                adjusted_projection = projection_matrix_variant(
                    projection_matrix,
                    generator,
                )
                projected_rows, projected_anchor = project_metric_rows_and_anchor(
                    transformed_rows,
                    transformed_anchor,
                    adjusted_projection,
                )
                _components, annotated_candidates = derived_axis_components_from_metric_rows(
                    baseline_candidates,
                    projected_rows,
                    projected_anchor,
                )
                _scenario_rows, _aggregate_rows, pc123_signatures_by_case = evaluate_derived_axis_candidates(
                    baseline_rows,
                    annotated_candidates,
                )
                for case_key, signatures in pc123_signatures_by_case.items():
                    case_signature_sets[case_key].append(signatures)

    case_rows: list[ProjectionFamilyCaseCoreRow] = []
    core_hits: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    union_hits: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)
    selected_core_hits: DefaultDict[tuple[str, str], set[tuple[str, str, float]]] = defaultdict(set)

    for case_key in sorted(case_signature_sets):
        signature_sets = case_signature_sets[case_key]
        baseline_row = baseline_rows_by_case[case_key]
        selected_rule = baseline_row.selected_rule
        if signature_sets:
            core_rules_set = set.intersection(*(set(signatures) for signatures in signature_sets))
            union_rules_set = set.union(*(set(signatures) for signatures in signature_sets))
        else:
            core_rules_set = set()
            union_rules_set = set()
        case_triplet = (
            baseline_row.pack_name,
            baseline_row.scenario_name,
            baseline_row.retained_weight,
        )
        for rule_signature in core_rules_set:
            family_rule = (baseline_row.rule_family, rule_signature)
            core_hits[family_rule].add(case_triplet)
            if rule_signature == selected_rule:
                selected_core_hits[family_rule].add(case_triplet)
        for rule_signature in union_rules_set:
            family_rule = (baseline_row.rule_family, rule_signature)
            union_hits[family_rule].add(case_triplet)

        case_rows.append(
            ProjectionFamilyCaseCoreRow(
                pack_name=baseline_row.pack_name,
                scenario_name=baseline_row.scenario_name,
                rule_family=baseline_row.rule_family,
                retained_weight=baseline_row.retained_weight,
                selected_rule=selected_rule,
                selected_in_core=selected_rule in core_rules_set,
                core_count=len(core_rules_set),
                union_count=len(union_rules_set),
                core_rules=", ".join(sorted(core_rules_set)) if core_rules_set else "-",
                union_rules=", ".join(sorted(union_rules_set)) if union_rules_set else "-",
            )
        )

    aggregate_rows = [
        ProjectionFamilyCoreAggregateRow(
            rule_family=rule_family,
            rule_signature=rule_signature,
            core_hits=len(core_hits[(rule_family, rule_signature)]),
            union_hits=len(union_hits[(rule_family, rule_signature)]),
            selected_core_hits=len(selected_core_hits[(rule_family, rule_signature)]),
        )
        for rule_family, rule_signature in union_hits
    ]
    case_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.pack_name,
            row.scenario_name,
            row.retained_weight,
        )
    )
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.core_hits,
            -row.union_hits,
            -row.selected_core_hits,
            row.rule_signature,
        )
    )
    return case_rows, aggregate_rows


def projection_core_regime(row: ProjectionFamilyCaseCoreRow) -> str:
    if row.core_count <= 0:
        return "empty"
    if row.core_count == 1:
        return "single-selected" if row.selected_in_core else "single-other"
    return "multi-selected" if row.selected_in_core else "multi-other"


def scenario_shape_name(scenario_name: str) -> str:
    return scenario_name.split("-")[0]


def projection_core_mechanism_map(
    case_rows: list[ProjectionFamilyCaseCoreRow],
) -> tuple[list[ProjectionCoreMechanismRow], list[ProjectionCoreMechanismCaseRow]]:
    grouped_rows: DefaultDict[str, list[ProjectionCoreMechanismCaseRow]] = defaultdict(list)
    case_feature_rows: list[ProjectionCoreMechanismCaseRow] = []
    scenario_feature_cache: dict[tuple[str, str], tuple[bool, int, float, float, float, bool]] = {}

    for row in case_rows:
        cache_key = (row.pack_name, row.scenario_name)
        if cache_key not in scenario_feature_cache:
            nodes, wrap_y = scenario_by_name(row.pack_name, row.scenario_name)
            (
                _mean_center,
                center_range,
                center_total_variation,
                crosses_midline,
                span_range,
            ) = column_profile_geometry_metrics(nodes)
            scenario_feature_cache[cache_key] = (
                wrap_y,
                len(nodes),
                center_range,
                center_total_variation,
                span_range,
                crosses_midline,
            )
        wrap_y, node_count, center_range, center_total_variation, span_range, crosses_midline = scenario_feature_cache[cache_key]
        mechanism_row = ProjectionCoreMechanismCaseRow(
            pack_name=row.pack_name,
            scenario_name=row.scenario_name,
            rule_family=row.rule_family,
            retained_weight=row.retained_weight,
            regime=projection_core_regime(row),
            selected_rule=row.selected_rule,
            selected_in_core=row.selected_in_core,
            core_count=row.core_count,
            union_count=row.union_count,
            wrap_y=wrap_y,
            crosses_midline=crosses_midline,
            nodes=node_count,
            center_range=center_range,
            center_variation=center_total_variation,
            span_range=span_range,
        )
        case_feature_rows.append(mechanism_row)
        grouped_rows[mechanism_row.regime].append(mechanism_row)

    regime_rows: list[ProjectionCoreMechanismRow] = []
    regime_order = ("empty", "single-selected", "single-other", "multi-selected", "multi-other")
    for regime in regime_order:
        rows = grouped_rows.get(regime, [])
        if not rows:
            continue
        regime_rows.append(
            ProjectionCoreMechanismRow(
                regime=regime,
                cases=len(rows),
                selected_in_core_cases=sum(row.selected_in_core for row in rows),
                wrap_cases=sum(row.wrap_y for row in rows),
                rect_cases=sum(scenario_shape_name(row.scenario_name) == "rect" for row in rows),
                taper_cases=sum(scenario_shape_name(row.scenario_name) == "taper" for row in rows),
                skew_cases=sum(scenario_shape_name(row.scenario_name) == "skew" for row in rows),
                crossing_cases=sum(row.crosses_midline for row in rows),
                avg_nodes=sum(row.nodes for row in rows) / len(rows),
                avg_center_range=sum(row.center_range for row in rows) / len(rows),
                avg_center_variation=sum(row.center_variation for row in rows) / len(rows),
                avg_span_range=sum(row.span_range for row in rows) / len(rows),
            )
        )

    case_feature_rows.sort(
        key=lambda row: (
            {"empty": 0, "single-other": 1, "single-selected": 2, "multi-other": 3, "multi-selected": 4}[row.regime],
            -row.center_variation,
            -row.center_range,
            row.rule_family,
            row.pack_name,
            row.scenario_name,
            row.retained_weight,
        )
    )
    return regime_rows, case_feature_rows


def harmonic_continuous_case_analysis(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    rule_family: str,
    count_options: tuple[frozenset[int], ...],
    retained_weight: float,
) -> tuple[FrontierScenarioRow, list[EvaluatedCandidate]]:
    scenario_row, candidates = frontier_case_analysis(
        pack_name=pack_name,
        scenario_name=scenario_name,
        nodes=nodes,
        wrap_y=wrap_y,
        rule_family=rule_family,
        count_options=count_options,
        retained_weight=retained_weight,
    )
    _harmonic_agg, _harmonic_changes, harmonic_rows, harmonic_candidates = frontier_observable_ablation(
        [scenario_row],
        candidates,
        observable="harmonic",
        ranking_mode="bucketed",
    )
    _harmonic_cont_agg, _harmonic_cont_changes, harmonic_cont_rows, harmonic_cont_candidates = frontier_observable_ablation(
        harmonic_rows,
        harmonic_candidates,
        observable="harmonic",
        ranking_mode="continuous",
    )
    return harmonic_cont_rows[0], harmonic_cont_candidates


def roughness_core_sweep(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
    alphas: tuple[float, ...] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
) -> tuple[list[RoughnessCoreSweepRow], list[RoughnessCoreAggregateRow]]:
    pack_name = "base"
    scenario_name = "taper-hard"
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    procedural_variants = {
        variant_name: perturbed_nodes
        for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
            pack_name,
            scenario_name,
            nodes,
            wrap_y,
            variant_limit=2,
        )
    }
    survivor_nodes = procedural_variants["procedural-a"]
    miss_nodes = procedural_variants["procedural-b"]
    xs, survivor_centers, _survivor_spans = ordered_profile_centers_and_spans(survivor_nodes)
    miss_xs, miss_centers, miss_spans = ordered_profile_centers_and_spans(miss_nodes)
    if xs != miss_xs:
        raise RuntimeError("Roughness core sweep requires aligned x columns.")

    rows: list[RoughnessCoreSweepRow] = []
    for alpha in alphas:
        centers = tuple(
            survivor_center + alpha * (miss_center - survivor_center)
            for survivor_center, miss_center in zip(survivor_centers, miss_centers)
        )
        profile = build_profile_from_centers_and_spans(xs, centers, miss_spans)
        sweep_nodes = build_nodes_from_interval_profile(profile)
        (
            _mean_center,
            center_range,
            center_variation,
            crosses_midline,
            span_range,
        ) = column_profile_geometry_metrics(sweep_nodes)
        for rule_family, count_options in family_count_options():
            for retained_weight in retained_weights:
                harmonic_cont_row, harmonic_cont_candidates = harmonic_continuous_case_analysis(
                    pack_name=pack_name,
                    scenario_name=f"{scenario_name}:roughness-{alpha:.2f}",
                    nodes=sweep_nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weight=retained_weight,
                )
                case_core_rows, _aggregate_rows = derived_projection_family_case_core_analysis(
                    [harmonic_cont_row],
                    harmonic_cont_candidates,
                    projection_dimension=4,
                    generator="orthonormal",
                )
                case_core_row = case_core_rows[0]
                rows.append(
                    RoughnessCoreSweepRow(
                        alpha=alpha,
                        rule_family=rule_family,
                        retained_weight=retained_weight,
                        regime=projection_core_regime(case_core_row),
                        selected_rule=case_core_row.selected_rule,
                        selected_in_core=case_core_row.selected_in_core,
                        core_count=case_core_row.core_count,
                        union_count=case_core_row.union_count,
                        center_range=center_range,
                        center_variation=center_variation,
                        span_range=span_range,
                        crosses_midline=crosses_midline,
                    )
                )

    aggregate_rows: list[RoughnessCoreAggregateRow] = []
    for alpha in alphas:
        for rule_family in ("compact", "extended"):
            family_rows = [
                row
                for row in rows
                if row.alpha == alpha and row.rule_family == rule_family
            ]
            aggregate_rows.append(
                RoughnessCoreAggregateRow(
                    alpha=alpha,
                    rule_family=rule_family,
                    cases=len(family_rows),
                    selected_in_core_cases=sum(row.selected_in_core for row in family_rows),
                    empty_cases=sum(row.regime == "empty" for row in family_rows),
                    single_selected_cases=sum(row.regime == "single-selected" for row in family_rows),
                    single_other_cases=sum(row.regime == "single-other" for row in family_rows),
                    multi_selected_cases=sum(row.regime == "multi-selected" for row in family_rows),
                    multi_other_cases=sum(row.regime == "multi-other" for row in family_rows),
                    avg_core_count=sum(row.core_count for row in family_rows) / len(family_rows),
                    center_range=family_rows[0].center_range,
                    center_variation=family_rows[0].center_variation,
                    span_range=family_rows[0].span_range,
                    crosses_midline=family_rows[0].crosses_midline,
                )
            )

    rows.sort(key=lambda row: (row.rule_family, row.retained_weight, row.alpha))
    aggregate_rows.sort(key=lambda row: (row.rule_family, row.alpha))
    return rows, aggregate_rows


def normalize_mode_vector(values: tuple[float, ...]) -> tuple[float, ...]:
    mean_value = sum(values) / len(values)
    centered = tuple(value - mean_value for value in values)
    max_abs = max(abs(value) for value in centered)
    if max_abs <= 1e-9:
        return tuple(0.0 for _value in centered)
    return tuple(value / max_abs for value in centered)


def centerline_mode_basis(xs: tuple[int, ...]) -> dict[str, tuple[float, ...]]:
    length = len(xs)
    if length <= 1:
        return {"flat": tuple(0.0 for _x in xs)}
    normalized_xs = tuple(
        -1.0 + 2.0 * index / (length - 1)
        for index in range(length)
    )
    return {
        "tilt": normalize_mode_vector(normalized_xs),
        "bowl": normalize_mode_vector(tuple(2.0 * x * x - 1.0 for x in normalized_xs)),
        "step": normalize_mode_vector(
            tuple(-1.0 if index < length / 2 else 1.0 for index in range(length))
        ),
        "zigzag": normalize_mode_vector(
            tuple(1.0 if index % 2 == 0 else -1.0 for index in range(length))
        ),
    }


def centerline_mode_invariants(
    centers: tuple[float, ...],
) -> tuple[str, int, float]:
    diffs = [
        centers[index + 1] - centers[index]
        for index in range(len(centers) - 1)
    ]
    nonzero_diffs = [diff for diff in diffs if abs(diff) > 1e-9]
    total_variation = sum(abs(diff) for diff in nonzero_diffs)
    turning_points = 0
    if len(nonzero_diffs) >= 2:
        signs = [1 if diff > 0.0 else -1 for diff in nonzero_diffs]
        turning_points = sum(
            signs[index + 1] != signs[index]
            for index in range(len(signs) - 1)
        )
    max_step_fraction = (
        max(abs(diff) for diff in nonzero_diffs) / total_variation
        if total_variation > 1e-9
        else 0.0
    )
    if total_variation <= 1e-9:
        signature = "flat"
    elif turning_points >= 2:
        signature = "oscillatory"
    elif turning_points == 1:
        signature = "curved"
    elif max_step_fraction >= 0.6:
        signature = "step-like"
    else:
        signature = "smooth-monotone"
    return signature, turning_points, max_step_fraction


def centerline_mode_core_sweep(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
    amplitudes: tuple[float, ...] = (0.0, 0.5, 1.0, 1.5, 2.0),
) -> tuple[list[CenterlineModeSweepRow], list[CenterlineModeAggregateRow]]:
    pack_name = "base"
    scenario_name = "taper-hard"
    nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    xs, base_centers, base_spans = ordered_profile_centers_and_spans(nodes)
    mode_basis = centerline_mode_basis(xs)

    rows: list[CenterlineModeSweepRow] = []
    for mode_name, mode_vector in mode_basis.items():
        for amplitude in amplitudes:
            centers = tuple(
                center + amplitude * mode_component
                for center, mode_component in zip(base_centers, mode_vector)
            )
            signature, turning_points, max_step_fraction = centerline_mode_invariants(
                centers,
            )
            profile = build_profile_from_centers_and_spans(xs, centers, base_spans)
            sweep_nodes = build_nodes_from_interval_profile(profile)
            (
                _mean_center,
                center_range,
                center_variation,
                crosses_midline,
                span_range,
            ) = column_profile_geometry_metrics(sweep_nodes)
            for rule_family, count_options in family_count_options():
                for retained_weight in retained_weights:
                    harmonic_cont_row, harmonic_cont_candidates = harmonic_continuous_case_analysis(
                        pack_name=pack_name,
                        scenario_name=f"{scenario_name}:{mode_name}:{amplitude:.2f}",
                        nodes=sweep_nodes,
                        wrap_y=wrap_y,
                        rule_family=rule_family,
                        count_options=count_options,
                        retained_weight=retained_weight,
                    )
                    case_core_rows, _aggregate_rows = derived_projection_family_case_core_analysis(
                        [harmonic_cont_row],
                        harmonic_cont_candidates,
                        projection_dimension=4,
                        generator="orthonormal",
                    )
                    case_core_row = case_core_rows[0]
                    rows.append(
                        CenterlineModeSweepRow(
                            mode=mode_name,
                            amplitude=amplitude,
                            rule_family=rule_family,
                            retained_weight=retained_weight,
                            signature=signature,
                            turning_points=turning_points,
                            max_step_fraction=max_step_fraction,
                            regime=projection_core_regime(case_core_row),
                            selected_rule=case_core_row.selected_rule,
                            selected_in_core=case_core_row.selected_in_core,
                            core_count=case_core_row.core_count,
                            union_count=case_core_row.union_count,
                            center_range=center_range,
                            center_variation=center_variation,
                            span_range=span_range,
                            crosses_midline=crosses_midline,
                        )
                    )

    aggregate_rows: list[CenterlineModeAggregateRow] = []
    for mode_name in sorted(mode_basis):
        for amplitude in amplitudes:
            for rule_family in ("compact", "extended"):
                family_rows = [
                    row
                    for row in rows
                    if row.mode == mode_name
                    and row.amplitude == amplitude
                    and row.rule_family == rule_family
                ]
                aggregate_rows.append(
                    CenterlineModeAggregateRow(
                        mode=mode_name,
                        amplitude=amplitude,
                        rule_family=rule_family,
                        signature=family_rows[0].signature,
                        cases=len(family_rows),
                        selected_in_core_cases=sum(row.selected_in_core for row in family_rows),
                        empty_cases=sum(row.regime == "empty" for row in family_rows),
                        single_selected_cases=sum(row.regime == "single-selected" for row in family_rows),
                        single_other_cases=sum(row.regime == "single-other" for row in family_rows),
                        multi_selected_cases=sum(row.regime == "multi-selected" for row in family_rows),
                        multi_other_cases=sum(row.regime == "multi-other" for row in family_rows),
                        avg_core_count=sum(row.core_count for row in family_rows) / len(family_rows),
                        center_range=family_rows[0].center_range,
                        center_variation=family_rows[0].center_variation,
                        span_range=family_rows[0].span_range,
                        crosses_midline=family_rows[0].crosses_midline,
                    )
                )

    rows.sort(key=lambda row: (row.rule_family, row.mode, row.amplitude, row.retained_weight))
    aggregate_rows.sort(key=lambda row: (row.rule_family, row.mode, row.amplitude))
    return rows, aggregate_rows


def centerline_invariant_analysis(
    mode_rows: list[CenterlineModeSweepRow],
) -> tuple[list[CenterlineInvariantAggregateRow], list[CenterlineInvariantComparisonRow]]:
    grouped_aggregate: DefaultDict[tuple[str, str, bool], list[CenterlineModeSweepRow]] = defaultdict(list)
    grouped_comparison: DefaultDict[tuple[str, float, str, bool], list[CenterlineModeSweepRow]] = defaultdict(list)

    for row in mode_rows:
        grouped_aggregate[(row.rule_family, row.signature, row.crosses_midline)].append(row)
        grouped_comparison[(row.rule_family, row.center_variation, row.signature, row.crosses_midline)].append(row)

    aggregate_rows: list[CenterlineInvariantAggregateRow] = []
    for (rule_family, signature, crosses_midline), rows in grouped_aggregate.items():
        aggregate_rows.append(
            CenterlineInvariantAggregateRow(
                rule_family=rule_family,
                signature=signature,
                crosses_midline=crosses_midline,
                cases=len(rows),
                selected_in_core_cases=sum(row.selected_in_core for row in rows),
                empty_cases=sum(row.regime == "empty" for row in rows),
                avg_core_count=sum(row.core_count for row in rows) / len(rows),
                avg_center_variation=sum(row.center_variation for row in rows) / len(rows),
            )
        )

    comparison_rows: list[CenterlineInvariantComparisonRow] = []
    for (rule_family, center_variation, signature, crosses_midline), rows in grouped_comparison.items():
        comparison_rows.append(
            CenterlineInvariantComparisonRow(
                rule_family=rule_family,
                center_variation=center_variation,
                signature=signature,
                crosses_midline=crosses_midline,
                cases=len(rows),
                selected_in_core_cases=sum(row.selected_in_core for row in rows),
                empty_cases=sum(row.regime == "empty" for row in rows),
                avg_core_count=sum(row.core_count for row in rows) / len(rows),
            )
        )

    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            -row.selected_in_core_cases,
            row.empty_cases,
            row.signature,
            row.crosses_midline,
        )
    )
    comparison_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.center_variation,
            row.signature,
            row.crosses_midline,
        )
    )
    return aggregate_rows, comparison_rows


def random_rediscovery_limit_sweep_summary(
    retained_weight: float = 1.0,
    variant_limit: int = 3,
    rediscovery_limits: tuple[int, ...] = (0, 1, 2, 3),
) -> list[RediscoveryLimitAggregateRow]:
    sorted_limits = tuple(sorted(dict.fromkeys(rediscovery_limits)))
    grouped_rows: DefaultDict[tuple[int, str], list[PerturbationCaseRow]] = defaultdict(list)

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                base_raw_pool = collect_raw_frontier_pool(
                    nodes,
                    wrap_y,
                    count_options,
                )
                base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
                base_row, base_candidates = frontier_case_analysis(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weight=retained_weight,
                    raw_pool=base_raw_pool,
                    evaluation_cache=base_evaluation_cache,
                )
                base_signature_sets = frontier_signature_sets(base_candidates)
                base_selected_rule = base_row.selected_rule
                allowed_rule_pairs = base_palette_rule_pairs(base_candidates)

                for variant_name, perturbed_nodes, node_delta in random_topology_perturbations(
                    pack_name,
                    scenario_name,
                    nodes,
                    wrap_y,
                    variant_limit=variant_limit,
                ):
                    perturbed_evaluation_cache = build_frontier_evaluation_cache(
                        perturbed_nodes,
                        wrap_y,
                    )
                    tracked_pool = collect_restricted_frontier_pool(
                        perturbed_nodes,
                        wrap_y,
                        count_options,
                        allowed_rule_pairs,
                    )
                    open_pool = collect_raw_frontier_pool(
                        perturbed_nodes,
                        wrap_y,
                        count_options,
                    )

                    for rediscovery_limit in sorted_limits:
                        perturbed_raw_pool = merge_limited_rediscovery_frontier_pool(
                            perturbed_nodes,
                            tracked_pool,
                            open_pool,
                            rediscovery_limit=rediscovery_limit,
                        )
                        perturbed_row, perturbed_candidates = frontier_case_analysis(
                            pack_name=pack_name,
                            scenario_name=scenario_name,
                            nodes=perturbed_nodes,
                            wrap_y=wrap_y,
                            rule_family=rule_family,
                            count_options=count_options,
                            retained_weight=retained_weight,
                            raw_pool=perturbed_raw_pool,
                            evaluation_cache=perturbed_evaluation_cache,
                        )
                        perturbed_signature_sets = frontier_signature_sets(perturbed_candidates)
                        perturbed_frontier_union = set().union(*perturbed_signature_sets.values())
                        selected_candidate = next(
                            (
                                candidate
                                for candidate in perturbed_candidates
                                if candidate.current_selected
                            ),
                            None,
                        )
                        case_row = PerturbationCaseRow(
                            rule_family=rule_family,
                            pack_name=pack_name,
                            scenario_name=scenario_name,
                            variant_name=variant_name,
                            node_delta=node_delta,
                            base_selected_rule=base_selected_rule,
                            perturbed_selected_rule=perturbed_row.selected_rule,
                            perturbed_status=(
                                selected_candidate.status if selected_candidate is not None else "no pattern"
                            ),
                            selected_matches_base=(perturbed_row.selected_rule == base_selected_rule),
                            base_selected_alive=(base_selected_rule in perturbed_frontier_union),
                            robustness_overlap=bool(
                                base_signature_sets["robustness"]
                                & perturbed_signature_sets["robustness"]
                            ),
                            proper_time_overlap=bool(
                                base_signature_sets["proper_time"]
                                & perturbed_signature_sets["proper_time"]
                            ),
                            geometry_overlap=bool(
                                base_signature_sets["geometry"]
                                & perturbed_signature_sets["geometry"]
                            ),
                            mixed_overlap=bool(
                                base_signature_sets["mixed"] & perturbed_signature_sets["mixed"]
                            ),
                        )
                        grouped_rows[(rediscovery_limit, rule_family)].append(case_row)

    aggregate_rows = [
        RediscoveryLimitAggregateRow(
            rediscovery_limit=rediscovery_limit,
            rule_family=rule_family,
            cases=len(rows),
            survives=sum(row.perturbed_status == "survives" for row in rows),
            selected_retained=sum(row.selected_matches_base for row in rows),
            base_selected_alive=sum(row.base_selected_alive for row in rows),
            robustness_overlap=sum(row.robustness_overlap for row in rows),
            proper_time_overlap=sum(row.proper_time_overlap for row in rows),
            geometry_overlap=sum(row.geometry_overlap for row in rows),
            mixed_overlap=sum(row.mixed_overlap for row in rows),
        )
        for (rediscovery_limit, rule_family), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (row.rediscovery_limit, row.rule_family)
    )
    return aggregate_rows


def perturbation_weight_stability_results(
    retained_weights: tuple[float, float] = (0.95, 1.0),
) -> tuple[list[PerturbationWeightCaseRow], list[PerturbationWeightAggregateRow]]:
    low_weight, high_weight = retained_weights
    low_case_rows, _low_aggregate_rows = perturbation_frontier_results(retained_weight=low_weight)
    high_case_rows, _high_aggregate_rows = perturbation_frontier_results(retained_weight=high_weight)

    low_by_key = {
        (
            row.rule_family,
            row.pack_name,
            row.scenario_name,
            row.variant_name,
        ): row
        for row in low_case_rows
    }
    high_by_key = {
        (
            row.rule_family,
            row.pack_name,
            row.scenario_name,
            row.variant_name,
        ): row
        for row in high_case_rows
    }

    case_rows: list[PerturbationWeightCaseRow] = []
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationWeightCaseRow]] = defaultdict(list)
    for case_key in sorted(set(low_by_key) & set(high_by_key)):
        low_row = low_by_key[case_key]
        high_row = high_by_key[case_key]
        case_row = PerturbationWeightCaseRow(
            rule_family=low_row.rule_family,
            pack_name=low_row.pack_name,
            scenario_name=low_row.scenario_name,
            variant_name=low_row.variant_name,
            low_weight=low_weight,
            high_weight=high_weight,
            low_selected_rule=low_row.perturbed_selected_rule,
            high_selected_rule=high_row.perturbed_selected_rule,
            low_status=low_row.perturbed_status,
            high_status=high_row.perturbed_status,
            same_selected=(low_row.perturbed_selected_rule == high_row.perturbed_selected_rule),
            survives_both=(low_row.perturbed_status == "survives" and high_row.perturbed_status == "survives"),
            base_alive_both=(low_row.base_selected_alive and high_row.base_selected_alive),
            robustness_both=(low_row.robustness_overlap and high_row.robustness_overlap),
            proper_time_both=(low_row.proper_time_overlap and high_row.proper_time_overlap),
            geometry_both=(low_row.geometry_overlap and high_row.geometry_overlap),
            mixed_both=(low_row.mixed_overlap and high_row.mixed_overlap),
        )
        case_rows.append(case_row)
        grouped_rows[(case_row.rule_family, case_row.variant_name)].append(case_row)
        grouped_rows[(case_row.rule_family, "all")].append(case_row)

    aggregate_rows = [
        PerturbationWeightAggregateRow(
            rule_family=rule_family,
            variant_name=variant_name,
            cases=len(rows),
            survives_both=sum(row.survives_both for row in rows),
            same_selected=sum(row.same_selected for row in rows),
            base_alive_both=sum(row.base_alive_both for row in rows),
            robustness_both=sum(row.robustness_both for row in rows),
            proper_time_both=sum(row.proper_time_both for row in rows),
            geometry_both=sum(row.geometry_both for row in rows),
            mixed_both=sum(row.mixed_both for row in rows),
        )
        for (rule_family, variant_name), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.variant_name != "all",
            row.variant_name,
        )
    )
    return case_rows, aggregate_rows


def perturbation_weight_case_needs_drift_report(row: PerturbationWeightCaseRow) -> bool:
    return (
        not row.same_selected
        or not row.base_alive_both
        or not row.robustness_both
        or not row.mixed_both
    )


def perturbation_weight_case_sort_key(
    row: PerturbationWeightCaseRow,
) -> tuple[object, ...]:
    return (
        row.same_selected,
        row.base_alive_both,
        row.mixed_both,
        row.robustness_both,
        row.rule_family,
        row.pack_name,
        row.scenario_name,
        row.variant_name,
    )


def perturbation_weight_ladder_case_needs_drift_report(
    row: PerturbationWeightLadderCaseRow,
) -> bool:
    return (
        not row.same_selected_all
        or not row.base_alive_all
        or not row.robustness_all
        or not row.mixed_all
    )


def perturbation_weight_ladder_case_sort_key(
    row: PerturbationWeightLadderCaseRow,
) -> tuple[object, ...]:
    return (
        row.same_selected_all,
        row.base_alive_all,
        row.mixed_all,
        row.robustness_all,
        row.rule_family,
        row.pack_name,
        row.scenario_name,
        row.variant_name,
    )


def scenario_perturbation_rows_by_weight(
    pack_name: str,
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    rule_family: str,
    count_options: tuple[frozenset[int], ...],
    retained_weights: tuple[float, ...],
) -> dict[float, dict[str, PerturbationCaseRow]]:
    base_raw_pool = collect_raw_frontier_pool(
        nodes,
        wrap_y,
        count_options,
    )
    base_evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
    perturbation_variants = deterministic_topology_perturbations(
        nodes,
        wrap_y,
    )
    variant_inputs = {
        variant_name: (
            node_delta,
            perturbed_nodes,
            build_frontier_evaluation_cache(
                perturbed_nodes,
                wrap_y,
            ),
        )
        for variant_name, perturbed_nodes, node_delta in perturbation_variants
    }

    scenario_rows_by_weight: dict[float, dict[str, PerturbationCaseRow]] = {}
    for retained_weight in retained_weights:
        base_row, base_candidates = frontier_case_analysis(
            pack_name=pack_name,
            scenario_name=scenario_name,
            nodes=nodes,
            wrap_y=wrap_y,
            rule_family=rule_family,
            count_options=count_options,
            retained_weight=retained_weight,
            raw_pool=base_raw_pool,
            evaluation_cache=base_evaluation_cache,
        )
        base_signature_sets = frontier_signature_sets(base_candidates)
        base_selected_rule = base_row.selected_rule
        allowed_rule_pairs = base_palette_rule_pairs(base_candidates)
        rows_by_variant: dict[str, PerturbationCaseRow] = {}

        for variant_name in sorted(variant_inputs):
            node_delta, perturbed_nodes, perturbed_evaluation_cache = variant_inputs[
                variant_name
            ]
            perturbed_raw_pool = collect_restricted_frontier_pool(
                perturbed_nodes,
                wrap_y,
                count_options,
                allowed_rule_pairs,
            )
            perturbed_row, perturbed_candidates = frontier_case_analysis(
                pack_name=pack_name,
                scenario_name=scenario_name,
                nodes=perturbed_nodes,
                wrap_y=wrap_y,
                rule_family=rule_family,
                count_options=count_options,
                retained_weight=retained_weight,
                raw_pool=perturbed_raw_pool,
                evaluation_cache=perturbed_evaluation_cache,
            )
            perturbed_signature_sets = frontier_signature_sets(perturbed_candidates)
            perturbed_frontier_union = set().union(*perturbed_signature_sets.values())
            selected_candidate = next(
                (
                    candidate
                    for candidate in perturbed_candidates
                    if candidate.current_selected
                ),
                None,
            )
            rows_by_variant[variant_name] = PerturbationCaseRow(
                rule_family=rule_family,
                pack_name=pack_name,
                scenario_name=scenario_name,
                variant_name=variant_name,
                node_delta=node_delta,
                base_selected_rule=base_selected_rule,
                perturbed_selected_rule=perturbed_row.selected_rule,
                perturbed_status=(
                    selected_candidate.status if selected_candidate is not None else "no pattern"
                ),
                selected_matches_base=(perturbed_row.selected_rule == base_selected_rule),
                base_selected_alive=(base_selected_rule in perturbed_frontier_union),
                robustness_overlap=bool(
                    base_signature_sets["robustness"]
                    & perturbed_signature_sets["robustness"]
                ),
                proper_time_overlap=bool(
                    base_signature_sets["proper_time"]
                    & perturbed_signature_sets["proper_time"]
                ),
                geometry_overlap=bool(
                    base_signature_sets["geometry"]
                    & perturbed_signature_sets["geometry"]
                ),
                mixed_overlap=bool(
                    base_signature_sets["mixed"] & perturbed_signature_sets["mixed"]
                ),
            )

        scenario_rows_by_weight[retained_weight] = rows_by_variant

    return scenario_rows_by_weight


def build_perturbation_weight_aggregate_rows(
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationWeightCaseRow]],
) -> list[PerturbationWeightAggregateRow]:
    aggregate_rows = [
        PerturbationWeightAggregateRow(
            rule_family=rule_family,
            variant_name=variant_name,
            cases=len(rows),
            survives_both=sum(row.survives_both for row in rows),
            same_selected=sum(row.same_selected for row in rows),
            base_alive_both=sum(row.base_alive_both for row in rows),
            robustness_both=sum(row.robustness_both for row in rows),
            proper_time_both=sum(row.proper_time_both for row in rows),
            geometry_both=sum(row.geometry_both for row in rows),
            mixed_both=sum(row.mixed_both for row in rows),
        )
        for (rule_family, variant_name), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.variant_name != "all",
            row.variant_name,
        )
    )
    return aggregate_rows


def build_perturbation_weight_ladder_aggregate_rows(
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationWeightLadderCaseRow]],
) -> list[PerturbationWeightLadderAggregateRow]:
    aggregate_rows = [
        PerturbationWeightLadderAggregateRow(
            rule_family=rule_family,
            variant_name=variant_name,
            cases=len(rows),
            survives_all=sum(row.survives_all for row in rows),
            same_selected_all=sum(row.same_selected_all for row in rows),
            base_alive_all=sum(row.base_alive_all for row in rows),
            robustness_all=sum(row.robustness_all for row in rows),
            proper_time_all=sum(row.proper_time_all for row in rows),
            geometry_all=sum(row.geometry_all for row in rows),
            mixed_all=sum(row.mixed_all for row in rows),
        )
        for (rule_family, variant_name), rows in grouped_rows.items()
    ]
    aggregate_rows.sort(
        key=lambda row: (
            row.rule_family,
            row.variant_name != "all",
            row.variant_name,
        )
    )
    return aggregate_rows


def perturbation_weight_stability_summary(
    retained_weights: tuple[float, float] = (0.95, 1.0),
    drift_limit: int = 16,
) -> tuple[list[PerturbationWeightAggregateRow], list[PerturbationWeightCaseRow]]:
    low_weight, high_weight = retained_weights
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationWeightCaseRow]] = defaultdict(list)
    drift_rows: list[PerturbationWeightCaseRow] = []

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                scenario_rows_by_weight = scenario_perturbation_rows_by_weight(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weights=(low_weight, high_weight),
                )

                for variant_name in sorted(
                    set(scenario_rows_by_weight[low_weight]) & set(scenario_rows_by_weight[high_weight])
                ):
                    low_row = scenario_rows_by_weight[low_weight][variant_name]
                    high_row = scenario_rows_by_weight[high_weight][variant_name]
                    case_row = PerturbationWeightCaseRow(
                        rule_family=low_row.rule_family,
                        pack_name=low_row.pack_name,
                        scenario_name=low_row.scenario_name,
                        variant_name=low_row.variant_name,
                        low_weight=low_weight,
                        high_weight=high_weight,
                        low_selected_rule=low_row.perturbed_selected_rule,
                        high_selected_rule=high_row.perturbed_selected_rule,
                        low_status=low_row.perturbed_status,
                        high_status=high_row.perturbed_status,
                        same_selected=(low_row.perturbed_selected_rule == high_row.perturbed_selected_rule),
                        survives_both=(low_row.perturbed_status == "survives" and high_row.perturbed_status == "survives"),
                        base_alive_both=(low_row.base_selected_alive and high_row.base_selected_alive),
                        robustness_both=(low_row.robustness_overlap and high_row.robustness_overlap),
                        proper_time_both=(low_row.proper_time_overlap and high_row.proper_time_overlap),
                        geometry_both=(low_row.geometry_overlap and high_row.geometry_overlap),
                        mixed_both=(low_row.mixed_overlap and high_row.mixed_overlap),
                    )
                    grouped_rows[(case_row.rule_family, case_row.variant_name)].append(case_row)
                    grouped_rows[(case_row.rule_family, "all")].append(case_row)
                    if perturbation_weight_case_needs_drift_report(case_row):
                        bounded_insert_sorted(
                            drift_rows,
                            case_row,
                            drift_limit,
                            perturbation_weight_case_sort_key,
                        )

    return build_perturbation_weight_aggregate_rows(grouped_rows), drift_rows


def perturbation_weight_ladder_summary(
    retained_weights: tuple[float, ...] = (0.9, 0.95, 1.0),
    drift_limit: int = 16,
) -> tuple[list[PerturbationWeightLadderAggregateRow], list[PerturbationWeightLadderCaseRow]]:
    grouped_rows: DefaultDict[tuple[str, str], list[PerturbationWeightLadderCaseRow]] = defaultdict(list)
    drift_rows: list[PerturbationWeightLadderCaseRow] = []
    sorted_weights = tuple(sorted(dict.fromkeys(retained_weights)))

    for rule_family, count_options in family_count_options():
        for pack_name, scenarios in benchmark_packs():
            for scenario_name, nodes, wrap_y in scenarios:
                scenario_rows_by_weight = scenario_perturbation_rows_by_weight(
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    nodes=nodes,
                    wrap_y=wrap_y,
                    rule_family=rule_family,
                    count_options=count_options,
                    retained_weights=sorted_weights,
                )
                variant_names = set.intersection(
                    *(set(rows_by_variant) for rows_by_variant in scenario_rows_by_weight.values())
                )

                for variant_name in sorted(variant_names):
                    rows = [scenario_rows_by_weight[weight][variant_name] for weight in sorted_weights]
                    selected_rules = tuple(row.perturbed_selected_rule for row in rows)
                    statuses = tuple(row.perturbed_status for row in rows)
                    case_row = PerturbationWeightLadderCaseRow(
                        rule_family=rows[0].rule_family,
                        pack_name=rows[0].pack_name,
                        scenario_name=rows[0].scenario_name,
                        variant_name=rows[0].variant_name,
                        weights=sorted_weights,
                        selected_rules=selected_rules,
                        statuses=statuses,
                        same_selected_all=(len(set(selected_rules)) == 1),
                        survives_all=all(status == "survives" for status in statuses),
                        base_alive_all=all(row.base_selected_alive for row in rows),
                        robustness_all=all(row.robustness_overlap for row in rows),
                        proper_time_all=all(row.proper_time_overlap for row in rows),
                        geometry_all=all(row.geometry_overlap for row in rows),
                        mixed_all=all(row.mixed_overlap for row in rows),
                    )
                    grouped_rows[(case_row.rule_family, case_row.variant_name)].append(case_row)
                    grouped_rows[(case_row.rule_family, "all")].append(case_row)
                    if perturbation_weight_ladder_case_needs_drift_report(case_row):
                        bounded_insert_sorted(
                            drift_rows,
                            case_row,
                            drift_limit,
                            perturbation_weight_ladder_case_sort_key,
                        )

    return build_perturbation_weight_ladder_aggregate_rows(grouped_rows), drift_rows


def frontier_hard_case_trace(
    retained_weights: tuple[float, ...] = (0.75, 0.8, 0.85, 0.9, 0.95, 1.0),
) -> tuple[str, str, list[FrontierTraceRow]]:
    hardest_rows = critical_weight_cases()
    hardest_pack = hardest_rows[0].pack_name if hardest_rows else "mirror"
    hardest_scenario = hardest_rows[0].scenario_name if hardest_rows else "rect-hard-large"
    nodes, wrap_y = scenario_by_name(hardest_pack, hardest_scenario)
    fallback_candidate, _fallback_diag = scan_self_maintaining_rules_fallback_only(
        nodes,
        wrap_y,
        RulePostulates(phase_per_action=4.0),
    )
    rescue_candidate, _rescue_diag, _rescue_metrics = quality_rescue_rule(
        nodes,
        wrap_y,
        SWEEP_COMPACT_COUNT_OPTIONS,
        build_frontier_postulates(1.0),
    )
    raw_pool = collect_raw_frontier_pool(
        nodes,
        wrap_y,
        SWEEP_COMPACT_COUNT_OPTIONS,
    )
    evaluation_cache = build_frontier_evaluation_cache(nodes, wrap_y)
    traced_signatures = [
        format_rule_signature(
            fallback_candidate.survive_counts,
            fallback_candidate.birth_counts,
        )
        if fallback_candidate is not None
        else "none",
        format_rule_signature(
            rescue_candidate.survive_counts,
            rescue_candidate.birth_counts,
        )
        if rescue_candidate is not None
        else "none",
    ]

    rows: list[FrontierTraceRow] = []
    for retained_weight in retained_weights:
        _scenario_row, case_candidates = frontier_case_analysis(
            pack_name=hardest_pack,
            scenario_name=hardest_scenario,
            nodes=nodes,
            wrap_y=wrap_y,
            rule_family="compact",
            count_options=SWEEP_COMPACT_COUNT_OPTIONS,
            retained_weight=retained_weight,
            raw_pool=raw_pool,
            evaluation_cache=evaluation_cache,
        )
        candidates_by_signature: dict[str, EvaluatedCandidate] = {}
        for candidate in case_candidates:
            existing_candidate = candidates_by_signature.get(candidate.rule_signature)
            candidate_key = (
                candidate.current_selected,
                candidate.on_robustness or candidate.on_proper_time or candidate.on_geometry or candidate.on_mixed,
                candidate.on_robustness,
                candidate.on_mixed,
                candidate.on_proper_time,
                candidate.on_geometry,
                candidate.status_rank,
                candidate.center_gap + candidate.arrival_span,
                candidate.min_margin,
                candidate.seed_node,
            )
            if existing_candidate is None:
                candidates_by_signature[candidate.rule_signature] = candidate
                continue
            existing_key = (
                existing_candidate.current_selected,
                existing_candidate.on_robustness or existing_candidate.on_proper_time or existing_candidate.on_geometry or existing_candidate.on_mixed,
                existing_candidate.on_robustness,
                existing_candidate.on_mixed,
                existing_candidate.on_proper_time,
                existing_candidate.on_geometry,
                existing_candidate.status_rank,
                existing_candidate.center_gap + existing_candidate.arrival_span,
                existing_candidate.min_margin,
                existing_candidate.seed_node,
            )
            if candidate_key > existing_key:
                candidates_by_signature[candidate.rule_signature] = candidate
        for traced_signature in traced_signatures:
            candidate = candidates_by_signature.get(traced_signature)
            if candidate is None:
                rows.append(
                    FrontierTraceRow(
                        retained_weight=retained_weight,
                        rule_signature=traced_signature,
                        search_sources="-",
                        current_selected=False,
                        on_robustness=False,
                        on_proper_time=False,
                        on_geometry=False,
                        on_mixed=False,
                        status="not in pool",
                        center_gap=float("nan"),
                        arrival_span=float("nan"),
                        min_margin=float("nan"),
                        min_wrapped_margin=float("nan"),
                    )
                )
                continue
            rows.append(
                FrontierTraceRow(
                    retained_weight=retained_weight,
                    rule_signature=traced_signature,
                    search_sources=candidate.search_sources,
                    current_selected=candidate.current_selected,
                    on_robustness=candidate.on_robustness,
                    on_proper_time=candidate.on_proper_time,
                    on_geometry=candidate.on_geometry,
                    on_mixed=candidate.on_mixed,
                    status=candidate.status,
                    center_gap=candidate.center_gap,
                    arrival_span=candidate.arrival_span,
                    min_margin=candidate.min_margin,
                    min_wrapped_margin=candidate.min_wrapped_margin,
                )
            )
    return hardest_pack, hardest_scenario, rows


def sample_boundary_arrivals(
    width: int,
    sample_ys: list[int],
    free_arrivals: dict[tuple[int, int], float],
    distorted_arrivals: dict[tuple[int, int], float],
) -> list[BoundaryArrival]:
    return [
        BoundaryArrival(
            y=y,
            free_arrival=free_arrivals[(width, y)],
            distorted_arrival=distorted_arrivals[(width, y)],
        )
        for y in sample_ys
    ]


def two_slit_distribution(
    screen_positions: list[int],
    record_created: bool,
    positive_only: bool = False,
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Asynchronous path sum on a causally oriented slit graph."""

    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
        ),
    )
    width = 16
    height = 10
    barrier_x = 8
    slit_ys = {-4, 4}
    source = (1, 0)
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y)
        for y in range(-height, height + 1)
        if y not in slit_ys
    )
    nodes = build_rectangular_nodes(
        width=width,
        height=height,
        blocked_nodes=blocked_nodes,
    )
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j
    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    for node in order:
        matching_states = [
            (state, amplitude)
            for state, amplitude in list(states.items())
            if state[0] == node
        ]
        if not matching_states:
            continue

        if node[0] == detector_x:
            for state, amplitude in matching_states:
                _current_node, _heading, sector = state
                boundary_distribution[node[1]][sector] += amplitude
                del states[state]
            continue

        for (current_node, heading, sector), amplitude in matching_states:
            del states[(current_node, heading, sector)]
            for neighbor in dag.get(node, []):
                dx = neighbor[0] - node[0]
                dy = neighbor[1] - node[1]
                next_heading = (dx, dy)
                _delay, _action_increment, link_amplitude = local_edge_properties(
                    node,
                    neighbor,
                    rule,
                    node_field,
                )
                if positive_only:
                    link_amplitude = complex(abs(link_amplitude), 0.0)

                next_sector = sector
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    if record_created:
                        next_sector = "upper" if neighbor[1] > 0 else "lower"
                    if neighbor[1] > 0:
                        link_amplitude *= cmath.exp(1j * phase_shift_upper)

                states[(neighbor, next_heading, next_sector)] += amplitude * link_amplitude

    distribution: dict[int, float] = {}
    for y in screen_positions:
        sector_amplitudes = boundary_distribution.get(y, {})
        if record_created:
            probability = sum(abs(amplitude) ** 2 for amplitude in sector_amplitudes.values())
        else:
            probability = abs(sum(sector_amplitudes.values())) ** 2
        distribution[y] = probability

    if not normalize:
        return distribution

    normalizer = sum(distribution.values())
    return {y: probability / normalizer for y, probability in distribution.items()}


def center_detector_phase_scan(phases: list[float]) -> list[tuple[float, float]]:
    """Compare how smoothly the center detector responds to a phase shifter."""

    raw_result: list[tuple[float, float]] = []
    for phase in phases:
        probability = two_slit_distribution(
            screen_positions=[0],
            record_created=False,
            phase_shift_upper=phase,
            normalize=False,
        )[0]
        raw_result.append((phase, probability))

    normalizer = max(probability for _phase, probability in raw_result)
    return [(phase, probability / normalizer) for phase, probability in raw_result]


def apply_hadamard(state: tuple[complex, complex]) -> tuple[complex, complex]:
    factor = 1 / math.sqrt(2)
    a, b = state
    return factor * (a + b), factor * (a - b)


def p_total(state: tuple[complex, complex], p: int) -> float:
    return sum(abs(amplitude) ** p for amplitude in state)


def born_rule_pressure_test() -> dict[int, list[tuple[float, float]]]:
    """Check which p-norm is preserved by reversible linear mixing."""

    samples = [
        (1.0 + 0.0j, 0.0 + 0.0j),
        (1 / math.sqrt(2), 1j / math.sqrt(2)),
        (2.0 - 1.0j, -0.5 + 1.5j),
    ]

    result: dict[int, list[tuple[float, float]]] = {}
    for p in (1, 2, 4):
        comparisons: list[tuple[float, float]] = []
        for state in samples:
            before = p_total(state, p)
            after = p_total(apply_hadamard(state), p)
            comparisons.append((before, after))
        result[p] = comparisons
    return result


def render_arrival_table(rows: list[BoundaryArrival]) -> str:
    lines = [
        "y  | free arrival | distorted arrival",
        "---+--------------+------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.y:>2} | "
            f"{row.free_arrival:>12.3f} | "
            f"{row.distorted_arrival:>16.3f}"
        )
    return "\n".join(lines)


def render_geodesic_table(rows: list[GeodesicComparison]) -> str:
    lines = [
        "target y | free action | distorted action | free path y-seq | distorted path y-seq",
        "---------+-------------+------------------+-----------------+----------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.target_y:>8} | "
            f"{row.free_action:>11.3f} | "
            f"{row.distorted_action:>16.3f} | "
            f"{row.free_path_y:>15} | "
            f"{row.distorted_path_y:>20}"
        )
    return "\n".join(lines)


def render_symmetry_table(rows: list[SymmetryCandidate]) -> str:
    lines = [
        "candidate local scalar                  | max boost drift",
        "----------------------------------------+----------------",
    ]
    for row in rows:
        lines.append(f"{row.name:<40} | {row.max_boost_drift:>14.6f}")
    return "\n".join(lines)


def render_field_samples(rows: list[PatternSample]) -> str:
    lines = [
        "node      | occup. | support | derived field",
        "----------+--------+---------+--------------",
    ]
    for row in rows:
        lines.append(
            f"{str(row.node):<10} | "
            f"{row.occupancy:>6.3f} | "
            f"{row.persistence_support:>7.3f} | "
            f"{row.field_strength:>12.6f}"
        )
    return "\n".join(lines)


def render_distribution(name: str, distribution: dict[int, float]) -> str:
    lines = [name, "y  | probability", "---+------------"]
    for y in sorted(distribution):
        lines.append(f"{y:>2} | {distribution[y]:>10.4f}")
    return "\n".join(lines)


def render_phase_scan(scan: list[tuple[float, float]]) -> str:
    lines = ["phase(rad) | center probability", "-----------+-------------------"]
    for phase, probability in scan:
        lines.append(f"{phase:>9.3f} | {probability:>17.4f}")
    return "\n".join(lines)


def render_born_test(result: dict[int, list[tuple[float, float]]]) -> str:
    lines = ["p-rule | before -> after under Hadamard mixing", "------+--------------------------------------"]
    for p in sorted(result):
        for index, (before, after) in enumerate(result[p], start=1):
            label = f"{p}" if index == 1 else ""
            lines.append(f"{label:>6} | sample {index}: {before:>8.4f} -> {after:>8.4f}")
    return "\n".join(lines)


def classify_robustness(center_gap: float, arrival_span: float) -> tuple[bool, str]:
    if center_gap > 0.1 and arrival_span > 0.5:
        return True, "survives"
    if center_gap > 0.05 and arrival_span > 0.25:
        return False, "mixed"
    return False, "fragile"


def focus_observable_score(
    center_gap: float,
    arrival_span: float,
    observable: str,
) -> float:
    normalized_gap = max(0.0, center_gap / 0.1)
    normalized_span = max(0.0, arrival_span / 0.5)
    if observable == "box-min":
        return min(normalized_gap, normalized_span)
    if observable == "harmonic":
        denominator = normalized_gap + normalized_span
        return (
            0.0
            if denominator <= 0.0
            else (2.0 * normalized_gap * normalized_span) / denominator
        )
    if observable == "geometric":
        return math.sqrt(normalized_gap * normalized_span)
    if observable == "arithmetic":
        return 0.5 * (normalized_gap + normalized_span)
    raise ValueError(f"Unknown focus observable: {observable}")


def classify_focus_observable(
    center_gap: float,
    arrival_span: float,
    observable: str,
) -> tuple[float, str]:
    score = focus_observable_score(center_gap, arrival_span, observable)
    if score > 1.0:
        return score, "survives"
    if score > 0.5:
        return score, "mixed"
    return score, "fragile"


def summarize_robustness(rows: list[RobustnessResult]) -> list[FamilyDiagnostic]:
    summaries: list[FamilyDiagnostic] = []
    for family in sorted({row.rule_family for row in rows}):
        family_rows = [row for row in rows if row.rule_family == family]
        active_rows = [row for row in family_rows if row.status != "no pattern"]
        rule_counts = Counter(
            row.rule_signature
            for row in active_rows
            if row.rule_signature != "-"
        )
        dominant_rule = rule_counts.most_common(1)[0][0] if rule_counts else "-"

        if active_rows:
            avg_rule_breadth = sum(row.rule_breadth for row in active_rows) / len(active_rows)
            avg_nodes = sum(row.persistent_nodes for row in active_rows) / len(active_rows)
            avg_center_gap = sum(row.center_gap for row in active_rows) / len(active_rows)
            avg_arrival_span = sum(row.arrival_span for row in active_rows) / len(active_rows)
        else:
            avg_rule_breadth = float("nan")
            avg_nodes = float("nan")
            avg_center_gap = float("nan")
            avg_arrival_span = float("nan")

        summaries.append(
            FamilyDiagnostic(
                rule_family=family,
                survives=sum(row.status == "survives" for row in family_rows),
                mixed=sum(row.status == "mixed" for row in family_rows),
                fragile=sum(row.status == "fragile" for row in family_rows),
                no_pattern=sum(row.status == "no pattern" for row in family_rows),
                avg_rule_breadth=avg_rule_breadth,
                avg_nodes=avg_nodes,
                avg_center_gap=avg_center_gap,
                avg_arrival_span=avg_arrival_span,
                dominant_rule=dominant_rule,
            )
        )
    return summaries


def render_robustness_table(rows: list[RobustnessResult]) -> str:
    lines = [
        "scenario    | family   | search   | rule              | nodes | center gap | arrival span | status",
        "------------+----------+----------+-------------------+-------+------------+--------------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.scenario_name:<11} | "
            f"{row.rule_family:<8} | "
            f"{('fallback' if row.fallback_used else 'primary'):<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.persistent_nodes:>5} | "
            f"{row.center_gap:>10.3f} | "
            f"{row.arrival_span:>12.3f} | "
            f"{row.status}"
        )
    return "\n".join(lines)


def render_family_diagnostics_table(rows: list[FamilyDiagnostic]) -> str:
    lines = [
        "family   | survives | mixed | fragile | no pattern | avg breadth | avg nodes | avg gap | avg span | dominant rule",
        "---------+----------+-------+---------+------------+-------------+-----------+---------+----------+-------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.survives:>8} | "
            f"{row.mixed:>5} | "
            f"{row.fragile:>7} | "
            f"{row.no_pattern:>10} | "
            f"{row.avg_rule_breadth:>11.2f} | "
            f"{row.avg_nodes:>9.2f} | "
            f"{row.avg_center_gap:>7.3f} | "
            f"{row.avg_arrival_span:>8.3f} | "
            f"{row.dominant_rule}"
        )
    return "\n".join(lines)


def render_failure_diagnostics_table(rows: list[RobustnessResult]) -> str:
    filtered_rows = [row for row in rows if row.status != "survives"]
    if not filtered_rows:
        return "no non-surviving scenarios under current sweep"

    lines = [
        "scenario    | family   | status     | accepted/trials | empty | split | size | boundary | dominant",
        "------------+----------+------------+-----------------+-------+-------+------+----------+----------",
    ]
    for row in filtered_rows:
        lines.append(
            f"{row.scenario_name:<11} | "
            f"{row.rule_family:<8} | "
            f"{row.status:<10} | "
            f"{row.accepted_candidates:>8}/{row.total_trials:<6} | "
            f"{row.empty_patterns:>5} | "
            f"{row.disconnected_rejections:>5} | "
            f"{row.size_rejections:>4} | "
            f"{row.boundary_rejections:>8} | "
            f"{row.dominant_rejection}"
        )
    return "\n".join(lines)


def render_focused_comparison_table(rows: list[FocusedComparison]) -> str:
    lines = [
        "setup              | rule              | center gap | arrival span | status",
        "-------------------+-------------------+------------+--------------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.label:<17} | "
            f"{row.rule_signature:<17} | "
            f"{row.center_gap:>10.3f} | "
            f"{row.arrival_span:>12.3f} | "
            f"{row.status}"
        )
    return "\n".join(lines)


def render_ablation_table(rows: list[AblationResult]) -> str:
    lines = [
        "remove option | survives | mixed | fragile | no pattern | failed scenarios",
        "--------------+----------+-------+---------+------------+------------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.removed_option:<13} | "
            f"{row.survives:>8} | "
            f"{row.mixed:>5} | "
            f"{row.fragile:>7} | "
            f"{row.no_pattern:>10} | "
            f"{row.failed_scenarios}"
        )
    return "\n".join(lines)


def render_mechanism_ablation_table(rows: list[MechanismAblationResult]) -> str:
    lines = [
        "mechanism               | survives | mixed | fragile | no pattern | avg gap | avg span | failed scenarios",
        "------------------------+----------+-------+---------+------------+---------+----------+------------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.label:<24} | "
            f"{row.survives:>8} | "
            f"{row.mixed:>5} | "
            f"{row.fragile:>7} | "
            f"{row.no_pattern:>10} | "
            f"{row.avg_center_gap:>7.3f} | "
            f"{row.avg_arrival_span:>8.3f} | "
            f"{row.failed_scenarios}"
        )
    return "\n".join(lines)


def render_action_discriminator_table(rows: list[ActionDiscriminatorResult]) -> str:
    lines = [
        "mechanism               | survives | min response | min wrapped | failed scenarios",
        "------------------------+----------+--------------+-------------+------------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.label:<24} | "
            f"{row.survives:>8} | "
            f"{row.min_response:>12.3f} | "
            f"{row.min_wrapped_response:>11.3f} | "
            f"{row.failed_scenarios}"
        )
    return "\n".join(lines)


def render_action_family_table(rows: list[ActionFamilyResult]) -> str:
    lines = [
        "retained w | survives | mixed | fragile | avg gap | avg span | min response | min wrapped",
        "-----------+----------+-------+---------+---------+----------+--------------+------------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>10.2f} | "
            f"{row.survives:>8} | "
            f"{row.mixed:>5} | "
            f"{row.fragile:>7} | "
            f"{row.avg_center_gap:>7.3f} | "
            f"{row.avg_arrival_span:>8.3f} | "
            f"{row.min_response:>12.3f} | "
            f"{row.min_wrapped_response:>10.3f}"
        )
    return "\n".join(lines)


def render_action_pack_table(rows: list[ActionPackResult]) -> str:
    lines = [
        "pack   | retained w | survives | mixed | fragile | min response | min wrapped | pass",
        "-------+------------+----------+-------+---------+--------------+-------------+-----",
    ]
    for row in rows:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.retained_weight:>10.2f} | "
            f"{row.survives:>8} | "
            f"{row.mixed:>5} | "
            f"{row.fragile:>7} | "
            f"{row.min_response:>12.3f} | "
            f"{row.min_wrapped_response:>11.3f} | "
            f"{'yes' if row.pack_pass else 'no'}"
        )
    return "\n".join(lines)


def render_proper_time_consistency_table(
    rows: list[ProperTimeConsistencyResult],
) -> str:
    lines = [
        "retained w | survives | min margin | min wrapped | pass | worst case",
        "-----------+----------+------------+-------------+------+------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>10.2f} | "
            f"{row.survives:>8} | "
            f"{row.min_margin:>10.3f} | "
            f"{row.min_wrapped_margin:>11.3f} | "
            f"{'yes' if row.pass_all else 'no':>4} | "
            f"{row.worst_case}"
        )
    return "\n".join(lines)


def render_critical_weight_table(
    rows: list[CriticalWeightCase],
    limit: int = 6,
) -> str:
    lines = [
        "pack   | scenario         | target y | critical w* | margin@1 | delay penalty | retained",
        "-------+------------------+----------+-------------+----------+---------------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.target_y:>8} | "
            f"{row.critical_weight:>11.3f} | "
            f"{row.margin_at_one:>8.3f} | "
            f"{row.delay_penalty:>13.3f} | "
            f"{row.retained_total:>7.3f}"
        )
    return "\n".join(lines)


def render_weight_branch_scan_table(
    rows: list[WeightBranchScanRow],
) -> str:
    lines = [
        "weight | rule              | source y | worst target | min margin | active w*",
        "-------+-------------------+----------+--------------+------------+----------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>6.2f} | "
            f"{row.rule_signature:<17} | "
            f"{row.source_y:>8} | "
            f"{row.worst_target_y:>12} | "
            f"{row.min_margin:>10.3f} | "
            f"{row.critical_weight:>8.3f}"
        )
    return "\n".join(lines)


def render_rule_selection_diagnostic_table(
    rows: list[RuleSelectionDiagnosticRow],
) -> str:
    lines = [
        "weight | fallback rule     | gap/span   | status   | rescue rule       | gap/span   | status   | final rule         | switched",
        "-------+-------------------+------------+----------+-------------------+------------+----------+--------------------+---------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>6.2f} | "
            f"{row.fallback_rule:<17} | "
            f"{row.fallback_center_gap:>5.3f}/{row.fallback_arrival_span:>5.3f} | "
            f"{row.fallback_status:<8} | "
            f"{row.rescue_rule:<17} | "
            f"{row.rescue_center_gap:>5.3f}/{row.rescue_arrival_span:>5.3f} | "
            f"{row.rescue_status:<8} | "
            f"{row.final_rule:<18} | "
            f"{'yes' if row.switched else 'no'}"
        )
    return "\n".join(lines)


def render_fixed_branch_competition_table(
    rows: list[FixedBranchCompetitionRow],
) -> str:
    lines = [
        "weight | branch         | rule              | center gap | arrival span | status   | min margin",
        "-------+----------------+-------------------+------------+--------------+----------+-----------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>6.2f} | "
            f"{row.branch_label:<14} | "
            f"{row.rule_signature:<17} | "
            f"{row.center_gap:>10.3f} | "
            f"{row.arrival_span:>12.3f} | "
            f"{row.status:<8} | "
            f"{row.min_margin:>9.3f}"
        )
    return "\n".join(lines)


def render_center_gap_geometry_table(
    rows: list[CenterGapGeometryRow],
) -> str:
    lines = [
        "branch         | rule              | source y start->end | stable paths | center action | side avg     | gap",
        "---------------+-------------------+---------------------+--------------+---------------+--------------+-----------",
    ]
    for row in rows:
        lines.append(
            f"{row.branch_label:<14} | "
            f"{row.rule_signature:<17} | "
            f"{row.source_y_start:>3}->{row.source_y_end:<3}            | "
            f"{'yes' if row.stable_paths else 'no':<12} | "
            f"{row.center_action_start:>5.3f}->{row.center_action_end:<5.3f} | "
            f"{row.side_avg_start:>5.3f}->{row.side_avg_end:<6.3f} | "
            f"{row.gap_start:>5.3f}->{row.gap_end:<5.3f}"
        )
    return "\n".join(lines)


def render_focus_metric_comparison_table(
    rows: list[FocusMetricComparisonRow],
) -> str:
    lines = [
        "weight | action gap f/r | geom gap f/r | stiffness f/r | action winner | geom winner | stiffness winner",
        "-------+----------------+--------------+---------------+---------------+-------------+-----------------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>6.2f} | "
            f"{row.fallback_action_gap:>5.3f}/{row.rescue_action_gap:<5.3f} | "
            f"{row.fallback_geometric_gap:>5.3f}/{row.rescue_geometric_gap:<5.3f} | "
            f"{row.fallback_stiffness:>5.3f}/{row.rescue_stiffness:<5.3f} | "
            f"{row.action_winner:<13} | "
            f"{row.geometric_winner:<11} | "
            f"{row.stiffness_winner}"
        )
    return "\n".join(lines)


def render_selector_policy_table(
    rows: list[SelectorPolicyRow],
) -> str:
    lines = [
        "weight | fallback status/quality | rescue status/quality | legacy gated       | current compare    | differs",
        "-------+-------------------------+-----------------------+--------------------+--------------------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>6.2f} | "
            f"{row.fallback_status:<8}/{row.fallback_quality:>5.3f}   | "
            f"{row.rescue_status:<8}/{row.rescue_quality:>5.3f} | "
            f"{row.gated_final_rule:<18} | "
            f"{row.ungated_final_rule:<18} | "
            f"{'yes' if row.differs else 'no'}"
        )
    return "\n".join(lines)


def render_selector_sweep_table(
    rows: list[SelectorSweepCase],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | weight | legacy rule/status   | current rule/status  | differs",
        "-------+------------------+--------+----------------------+----------------------+--------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.retained_weight:>6.2f} | "
            f"{row.gated_rule:<18}/{row.gated_status:<8} | "
            f"{row.ungated_rule:<18}/{row.ungated_status:<8} | "
            f"{'yes' if row.differs else 'no'}"
        )
    return "\n".join(lines)


def format_metric(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return f"{value:.3f}"


def render_frontier_scenario_table(
    rows: list[FrontierScenarioRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | w    | pool | selected           | sel R/P/G/M | R/P/G/M counts | robustness rules     | proper-time rules   | geometry rules      | mixed rules",
        "-------+------------------+----------+------+-----+--------------------+-------------+----------------+----------------------+---------------------+---------------------+---------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.pool_size:>3} | "
            f"{row.selected_rule:<18} | "
            f"{('Y' if row.selected_on_robustness else 'n')}/{('Y' if row.selected_on_proper_time else 'n')}/{('Y' if row.selected_on_geometry else 'n')}/{('Y' if row.selected_on_mixed else 'n'):<7} | "
            f"{row.robustness_count:>1}/{row.proper_time_count:>1}/{row.geometry_count:>1}/{row.mixed_count:>1}          | "
            f"{row.robustness_rules:<20} | "
            f"{row.proper_time_rules:<19} | "
            f"{row.geometry_rules:<19} | "
            f"{row.mixed_rules}"
        )
    return "\n".join(lines)


def render_frontier_aggregate_table(
    rows: list[FrontierAggregateRow],
) -> str:
    lines = [
        "family   | rule              | cases | selected | robustness | proper-time | geometry | mixed",
        "---------+-------------------+-------+----------+------------+-------------+----------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.case_hits:>5} | "
            f"{row.selected_hits:>8} | "
            f"{row.robustness_hits:>10} | "
            f"{row.proper_time_hits:>11} | "
            f"{row.geometry_hits:>8} | "
            f"{row.mixed_hits:>4}"
        )
    return "\n".join(lines)


def render_derived_axis_loading_table(
    rows: list[DerivedAxisLoadingRow],
) -> str:
    lines = [
        "component | eigen | center | arrival | margin | geometry | focus",
        "----------+-------+--------+---------+--------+----------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.component:<8} | "
            f"{row.eigenvalue:>5.2f} | "
            f"{row.center_gap:>6.3f} | "
            f"{row.arrival_span:>7.3f} | "
            f"{row.min_margin:>6.3f} | "
            f"{row.geometric_focus_gap:>8.3f} | "
            f"{row.focus_score:>5.3f}"
        )
    return "\n".join(lines)


def render_derived_axis_scenario_table(
    rows: list[DerivedAxisScenarioRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | w    | selected           | sel pc1/12/123 | counts  | pc1 rules           | pc12 rules          | pc123 rules",
        "-------+------------------+----------+------+--------------------+----------------+---------+---------------------+---------------------+---------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.selected_rule:<18} | "
            f"{('Y' if row.selected_on_pc1 else 'n')}/{('Y' if row.selected_on_pc12 else 'n')}/{('Y' if row.selected_on_pc123 else 'n'):<10} | "
            f"{row.pc1_count:>1}/{row.pc12_count:>2}/{row.pc123_count:>3} | "
            f"{row.pc1_rules:<19} | "
            f"{row.pc12_rules:<19} | "
            f"{row.pc123_rules}"
        )
    return "\n".join(lines)


def render_derived_axis_aggregate_table(
    rows: list[DerivedAxisAggregateRow],
) -> str:
    lines = [
        "family   | rule              | cases | selected | pc1 | pc12 | pc123",
        "---------+-------------------+-------+----------+-----+------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.case_hits:>5} | "
            f"{row.selected_hits:>8} | "
            f"{row.pc1_hits:>3} | "
            f"{row.pc12_hits:>4} | "
            f"{row.pc123_hits:>4}"
        )
    return "\n".join(lines)


def render_derived_basis_ablation_table(
    rows: list[DerivedBasisAblationRow],
) -> str:
    lines = [
        "basis      | dim | sel pc1/12/123 | pc123 ovlp | compact top        | ext top            | metrics",
        "-----------+-----+----------------+------------+--------------------+--------------------+------------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.basis_name:<9} | "
            f"{row.dimension:>3} | "
            f"{row.selected_on_pc1:>3}/{row.selected_on_pc12:<3}/{row.selected_on_pc123:<3} | "
            f"{row.pc123_overlap_with_full:>10} | "
            f"{row.compact_top_rule:<18} {row.compact_top_pc123:>2} | "
            f"{row.extended_top_rule:<18} {row.extended_top_pc123:>2} | "
            f"{row.metrics}"
        )
    return "\n".join(lines)


def render_derived_bootstrap_basis_table(
    rows: list[DerivedBootstrapBasisRow],
    limit: int = 16,
) -> str:
    lines = [
        "basis      | type   | dim | sel pc123 | ovlp full | compact top        | ext top",
        "-----------+--------+-----+-----------+-----------+--------------------+--------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.basis_name:<9} | "
            f"{row.basis_type:<6} | "
            f"{row.dimension:>3} | "
            f"{row.selected_on_pc123:>9} | "
            f"{row.pc123_overlap_with_full:>9} | "
            f"{row.compact_top_rule:<18} {row.compact_top_pc123:>2} | "
            f"{row.extended_top_rule:<18} {row.extended_top_pc123:>2}"
        )
    return "\n".join(lines)


def render_derived_bootstrap_stability_table(
    rows: list[DerivedBootstrapStabilityRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | rule              | basis hits | subset | lin-rnd | nonlin | case hits | top hits",
        "---------+-------------------+------------+--------+---------+--------+-----------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.basis_hits:>10} | "
            f"{row.subset_basis_hits:>6} | "
            f"{row.linear_random_hits:>7} | "
            f"{row.nonlinear_basis_hits:>6} | "
            f"{row.case_basis_hits:>9} | "
            f"{row.top_basis_hits:>7}"
        )
    return "\n".join(lines)


def render_derived_transform_break_table(
    rows: list[DerivedTransformBreakRow],
) -> str:
    lines = [
        "mode         | direct xfrm | proj xfrm  | weakest basis               | overlap | sel pc123",
        "-------------+-------------+------------+----------------------------+---------+----------",
    ]
    for row in rows:
        direct_label = "-" if row.direct_transform_break_strength is None else f"{row.direct_transform_break_strength:.2f}"
        projected_label = "-" if row.projected_transform_break_strength is None else f"{row.projected_transform_break_strength:.2f}"
        lines.append(
            f"{row.mode:<11} | "
            f"{direct_label:>11} | "
            f"{projected_label:>10} | "
            f"{row.weakest_basis_name:<26} | "
            f"{row.weakest_overlap:>7} | "
            f"{row.weakest_selected_on_pc123:>8}"
        )
    return "\n".join(lines)


def render_derived_transform_strength_table(
    rows: list[DerivedTransformStrengthRow],
    limit: int = 15,
) -> str:
    lines = [
        "mode         | s    | variant | sel pc123 | ovlp full | compact top        | ext top",
        "-------------+------+---------+-----------+-----------+--------------------+--------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.mode:<11} | "
            f"{row.strength:>4.2f} | "
            f"{row.variant_name:<7} | "
            f"{row.selected_on_pc123:>9} | "
            f"{row.pc123_overlap_with_full:>9} | "
            f"{row.compact_top_rule:<18} {row.compact_top_pc123:>2} | "
            f"{row.extended_top_rule:<18} {row.extended_top_pc123:>2}"
        )
    return "\n".join(lines)


def render_derived_transform_stability_table(
    rows: list[DerivedTransformStabilityRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | rule              | basis hits | direct | projected | top hits",
        "---------+-------------------+------------+--------+-----------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.basis_hits:>10} | "
            f"{row.direct_hits:>6} | "
            f"{row.projected_hits:>9} | "
            f"{row.top_hits:>7}"
        )
    return "\n".join(lines)


def render_derived_projection_bootstrap_table(
    rows: list[DerivedProjectionBootstrapRow],
    limit: int = 15,
) -> str:
    lines = [
        "mode         | s    | proj | ovlp min/avg | sel min/avg | compact dom       | ext dom",
        "-------------+------+------|--------------+-------------+-------------------+-------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.mode:<11} | "
            f"{row.strength:>4.2f} | "
            f"{row.projections:>4} | "
            f"{row.overlap_min:>3}/{row.overlap_avg:>7.2f} | "
            f"{row.selected_min:>3}/{row.selected_avg:>7.2f} | "
            f"{row.compact_dominant_rule:<17} {row.compact_dominant_basis_hits:>1}/{row.projections:<1} | "
            f"{row.extended_dominant_rule:<17} {row.extended_dominant_basis_hits:>1}/{row.projections:<1}"
        )
    return "\n".join(lines)


def render_derived_projection_stability_table(
    rows: list[DerivedProjectionStabilityRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | rule              | basis hits | top hits",
        "---------+-------------------+------------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.basis_hits:>10} | "
            f"{row.top_hits:>7}"
        )
    return "\n".join(lines)


def render_projection_generator_ablation_table(
    rows: list[ProjectionGeneratorAblationRow],
) -> str:
    lines = [
        "generator    | bases | ovlp min/avg | sel min/avg | weakest basis                       | compact dom       | ext dom",
        "-------------+-------+--------------+-------------+------------------------------------+-------------------+-------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.generator:<12} | "
            f"{row.bases:>5} | "
            f"{row.overlap_min:>3}/{row.overlap_avg:>7.2f} | "
            f"{row.selected_min:>3}/{row.selected_avg:>7.2f} | "
            f"{row.weakest_basis_name:<34} | "
            f"{row.compact_dominant_rule:<17} {row.compact_dominant_basis_hits:>2}/{row.bases:<2} | "
            f"{row.extended_dominant_rule:<17} {row.extended_dominant_basis_hits:>2}/{row.bases:<2}"
        )
    return "\n".join(lines)


def render_projection_dimension_ablation_table(
    rows: list[ProjectionDimensionAblationRow],
) -> str:
    lines = [
        "dim | bases | ovlp min/avg | sel min/avg | weakest basis                    | compact dom       | ext dom",
        "----+-------+--------------+-------------+---------------------------------+-------------------+-------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.dimension:>3} | "
            f"{row.bases:>5} | "
            f"{row.overlap_min:>3}/{row.overlap_avg:>7.2f} | "
            f"{row.selected_min:>3}/{row.selected_avg:>7.2f} | "
            f"{row.weakest_basis_name:<31} | "
            f"{row.compact_dominant_rule:<17} {row.compact_dominant_basis_hits:>2}/{row.bases:<2} | "
            f"{row.extended_dominant_rule:<17} {row.extended_dominant_basis_hits:>2}/{row.bases:<2}"
        )
    return "\n".join(lines)


def render_projection_family_basis_table(
    rows: list[ProjectionFamilyBasisRow],
    limit: int = 15,
) -> str:
    lines = [
        "mode         | s    | sel pc123 | ovlp full | compact top        | ext top",
        "-------------+------+-----------+-----------+--------------------+--------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.mode:<11} | "
            f"{row.strength:>4.2f} | "
            f"{row.selected_on_pc123:>9} | "
            f"{row.pc123_overlap_with_full:>9} | "
            f"{row.compact_top_rule:<18} {row.compact_top_pc123:>2} | "
            f"{row.extended_top_rule:<18} {row.extended_top_pc123:>2}"
        )
    return "\n".join(lines)


def render_projection_family_stability_table(
    rows: list[ProjectionFamilyStabilityRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | rule              | basis hits | case hits | top hits",
        "---------+-------------------+------------+-----------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.basis_hits:>10} | "
            f"{row.case_hits:>9} | "
            f"{row.top_hits:>7}"
        )
    return "\n".join(lines)


def render_projection_family_case_core_table(
    rows: list[ProjectionFamilyCaseCoreRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | w    | selected           | sel core | core/union | core rules",
        "-------+------------------+----------+------+--------------------+----------+------------+------------------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.selected_rule:<18} | "
            f"{('Y' if row.selected_in_core else 'n'):<8} | "
            f"{row.core_count:>3}/{row.union_count:<6} | "
            f"{row.core_rules}"
        )
    return "\n".join(lines)


def render_projection_family_core_aggregate_table(
    rows: list[ProjectionFamilyCoreAggregateRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | rule              | core hits | union hits | sel-core hits",
        "---------+-------------------+-----------+------------+--------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.rule_signature:<17} | "
            f"{row.core_hits:>9} | "
            f"{row.union_hits:>10} | "
            f"{row.selected_core_hits:>12}"
        )
    return "\n".join(lines)


def render_projection_core_mechanism_table(
    rows: list[ProjectionCoreMechanismRow],
) -> str:
    lines = [
        "regime          | cases | wrap | rect/taper/skew | cross | avg nodes | avg crng | avg cvar | avg srng",
        "----------------+-------+------+-----------------+-------+-----------+----------+----------+---------",
    ]
    for row in rows:
        lines.append(
            f"{row.regime:<15} | "
            f"{row.cases:>5} | "
            f"{row.wrap_cases:>4} | "
            f"{row.rect_cases:>4}/{row.taper_cases:<5}/{row.skew_cases:<4} | "
            f"{row.crossing_cases:>5} | "
            f"{row.avg_nodes:>9.2f} | "
            f"{row.avg_center_range:>8.2f} | "
            f"{row.avg_center_variation:>8.2f} | "
            f"{row.avg_span_range:>7.2f}"
        )
    return "\n".join(lines)


def render_projection_core_mechanism_case_table(
    rows: list[ProjectionCoreMechanismCaseRow],
    limit: int = 12,
) -> str:
    lines = [
        "regime          | pack   | scenario         | family   | w    | sel core | core/u | wrap | cross | crng | cvar | srng",
        "----------------+--------+------------------+----------+------+----------+--------+------+-------+------+-------+-----",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.regime:<15} | "
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{('Y' if row.selected_in_core else 'n'):<8} | "
            f"{row.core_count:>2}/{row.union_count:<5} | "
            f"{('Y' if row.wrap_y else 'n'):<4} | "
            f"{('Y' if row.crosses_midline else 'n'):<5} | "
            f"{row.center_range:>4.1f} | "
            f"{row.center_variation:>5.1f} | "
            f"{row.span_range:>3.1f}"
        )
    return "\n".join(lines)


def render_roughness_core_aggregate_table(
    rows: list[RoughnessCoreAggregateRow],
) -> str:
    lines = [
        "family   | alpha | sel core | empty | single sel/other | multi sel/other | avg core | crng | cvar | srng | cross",
        "---------+-------+----------+-------+------------------+-----------------+----------+------+------+------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.alpha:>5.2f} | "
            f"{row.selected_in_core_cases:>8} | "
            f"{row.empty_cases:>5} | "
            f"{row.single_selected_cases:>6}/{row.single_other_cases:<5} | "
            f"{row.multi_selected_cases:>5}/{row.multi_other_cases:<5} | "
            f"{row.avg_core_count:>8.2f} | "
            f"{row.center_range:>4.1f} | "
            f"{row.center_variation:>4.1f} | "
            f"{row.span_range:>4.1f} | "
            f"{('Y' if row.crosses_midline else 'n'):<4}"
        )
    return "\n".join(lines)


def render_roughness_core_case_table(
    rows: list[RoughnessCoreSweepRow],
    limit: int = 18,
) -> str:
    lines = [
        "family   | w    | alpha | regime          | sel core | core/u | rule",
        "---------+------+-------+-----------------+----------+--------+-------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.alpha:>5.2f} | "
            f"{row.regime:<15} | "
            f"{('Y' if row.selected_in_core else 'n'):<8} | "
            f"{row.core_count:>2}/{row.union_count:<5} | "
            f"{row.selected_rule}"
        )
    return "\n".join(lines)


def render_centerline_mode_aggregate_table(
    rows: list[CenterlineModeAggregateRow],
) -> str:
    lines = [
        "family   | mode   | amp  | sel core | empty | single sel/other | multi sel/other | avg core | cvar | cross",
        "---------+--------+------+----------+-------+------------------+-----------------+----------+------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.mode:<6} | "
            f"{row.amplitude:>4.1f} | "
            f"{row.selected_in_core_cases:>8} | "
            f"{row.empty_cases:>5} | "
            f"{row.single_selected_cases:>6}/{row.single_other_cases:<5} | "
            f"{row.multi_selected_cases:>5}/{row.multi_other_cases:<5} | "
            f"{row.avg_core_count:>8.2f} | "
            f"{row.center_variation:>4.1f} | "
            f"{('Y' if row.crosses_midline else 'n'):<4}"
        )
    return "\n".join(lines)


def render_centerline_mode_case_table(
    rows: list[CenterlineModeSweepRow],
    limit: int = 20,
) -> str:
    lines = [
        "family   | mode   | amp  | w    | regime          | sel core | core/u | rule",
        "---------+--------+------+-------+-----------------+----------+--------+-------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.mode:<6} | "
            f"{row.amplitude:>4.1f} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.regime:<15} | "
            f"{('Y' if row.selected_in_core else 'n'):<8} | "
            f"{row.core_count:>2}/{row.union_count:<5} | "
            f"{row.selected_rule}"
        )
    return "\n".join(lines)


def render_centerline_invariant_aggregate_table(
    rows: list[CenterlineInvariantAggregateRow],
    limit: int = 12,
) -> str:
    lines = [
        "family   | signature       | cross | cases | sel core | empty | avg core | avg cvar",
        "---------+-----------------+-------+-------+----------+-------+----------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.signature:<15} | "
            f"{('Y' if row.crosses_midline else 'n'):<5} | "
            f"{row.cases:>5} | "
            f"{row.selected_in_core_cases:>8} | "
            f"{row.empty_cases:>5} | "
            f"{row.avg_core_count:>8.2f} | "
            f"{row.avg_center_variation:>7.2f}"
        )
    return "\n".join(lines)


def render_centerline_invariant_comparison_table(
    rows: list[CenterlineInvariantComparisonRow],
    limit: int = 16,
) -> str:
    lines = [
        "family   | cvar | signature       | cross | cases | sel core | empty | avg core",
        "---------+------+-----------------+-------+-------+----------+-------+---------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.center_variation:>4.1f} | "
            f"{row.signature:<15} | "
            f"{('Y' if row.crosses_midline else 'n'):<5} | "
            f"{row.cases:>5} | "
            f"{row.selected_in_core_cases:>8} | "
            f"{row.empty_cases:>5} | "
            f"{row.avg_core_count:>7.2f}"
        )
    return "\n".join(lines)


def render_frontier_trace_table(
    rows: list[FrontierTraceRow],
) -> str:
    lines = [
        "w    | rule              | sources      | current | R/P/G/M | status      | gap/span       | margin/wrapped",
        "-----+-------------------+--------------+---------+---------+-------------+----------------+---------------",
    ]
    for row in rows:
        lines.append(
            f"{row.retained_weight:>4.2f} | "
            f"{row.rule_signature:<17} | "
            f"{row.search_sources:<12} | "
            f"{'yes' if row.current_selected else 'no':<7} | "
            f"{('Y' if row.on_robustness else 'n')}/{('Y' if row.on_proper_time else 'n')}/{('Y' if row.on_geometry else 'n')}/{('Y' if row.on_mixed else 'n'):<5} | "
            f"{row.status:<11} | "
            f"{format_metric(row.center_gap):>6}/{format_metric(row.arrival_span):<7} | "
            f"{format_metric(row.min_margin):>6}/{format_metric(row.min_wrapped_margin)}"
        )
    return "\n".join(lines)


def render_perturbation_aggregate_table(
    rows: list[PerturbationAggregateRow],
) -> str:
    lines = [
        "family   | variant      | cases | survives | same sel | base alive | R ovlp | P ovlp | G ovlp | M ovlp",
        "---------+--------------+-------+----------+----------+------------+--------+--------+--------+-------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{row.cases:>5} | "
            f"{row.survives:>8} | "
            f"{row.selected_retained:>8} | "
            f"{row.base_selected_alive:>10} | "
            f"{row.robustness_overlap:>6} | "
            f"{row.proper_time_overlap:>6} | "
            f"{row.geometry_overlap:>6} | "
            f"{row.mixed_overlap:>5}"
        )
    return "\n".join(lines)


def render_perturbation_case_table(
    rows: list[PerturbationCaseRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | variant      | dN | base -> perturbed   | status    | same | alive | R/P/G/M",
        "-------+------------------+----------+--------------+----+---------------------+-----------+------+-------+--------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{row.node_delta:>2} | "
            f"{row.base_selected_rule:<9}->{row.perturbed_selected_rule:<9} | "
            f"{row.perturbed_status:<9} | "
            f"{'yes' if row.selected_matches_base else 'no ':<4} | "
            f"{'yes' if row.base_selected_alive else 'no ':<5} | "
            f"{('Y' if row.robustness_overlap else 'n')}/{('Y' if row.proper_time_overlap else 'n')}/{('Y' if row.geometry_overlap else 'n')}/{('Y' if row.mixed_overlap else 'n')}"
        )
    return "\n".join(lines)


def render_perturbation_weight_aggregate_table(
    rows: list[PerturbationWeightAggregateRow],
) -> str:
    lines = [
        "family   | variant      | cases | survive both | same sel | base alive both | R both | P both | G both | M both",
        "---------+--------------+-------+--------------+----------+-----------------+--------+--------+--------+-------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{row.cases:>5} | "
            f"{row.survives_both:>12} | "
            f"{row.same_selected:>8} | "
            f"{row.base_alive_both:>15} | "
            f"{row.robustness_both:>6} | "
            f"{row.proper_time_both:>6} | "
            f"{row.geometry_both:>6} | "
            f"{row.mixed_both:>5}"
        )
    return "\n".join(lines)


def render_perturbation_weight_case_table(
    rows: list[PerturbationWeightCaseRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | variant      | sel@low -> sel@high   | stat low/high | same | alive | R/P/G/M both",
        "-------+------------------+----------+--------------+-----------------------+---------------+------+-------+---------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{row.low_selected_rule:<9}->{row.high_selected_rule:<9} | "
            f"{row.low_status:<6}/{row.high_status:<6} | "
            f"{'yes' if row.same_selected else 'no ':<4} | "
            f"{'yes' if row.base_alive_both else 'no ':<5} | "
            f"{('Y' if row.robustness_both else 'n')}/{('Y' if row.proper_time_both else 'n')}/{('Y' if row.geometry_both else 'n')}/{('Y' if row.mixed_both else 'n')}"
        )
    return "\n".join(lines)


def render_perturbation_weight_ladder_aggregate_table(
    rows: list[PerturbationWeightLadderAggregateRow],
) -> str:
    lines = [
        "family   | variant      | cases | survive all | same sel all | base alive all | R all | P all | G all | M all",
        "---------+--------------+-------+-------------+--------------+----------------+-------+-------+-------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{row.cases:>5} | "
            f"{row.survives_all:>11} | "
            f"{row.same_selected_all:>12} | "
            f"{row.base_alive_all:>14} | "
            f"{row.robustness_all:>5} | "
            f"{row.proper_time_all:>5} | "
            f"{row.geometry_all:>5} | "
            f"{row.mixed_all:>4}"
        )
    return "\n".join(lines)


def render_perturbation_weight_ladder_case_table(
    rows: list[PerturbationWeightLadderCaseRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | variant      | status path         | same | alive | R/P/G/M all",
        "-------+------------------+----------+--------------+---------------------+------+-------+-------------",
    ]
    for row in rows[:limit]:
        status_path = "/".join(row.statuses)
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.variant_name:<12} | "
            f"{status_path:<19} | "
            f"{'yes' if row.same_selected_all else 'no ':<4} | "
            f"{'yes' if row.base_alive_all else 'no ':<5} | "
            f"{('Y' if row.robustness_all else 'n')}/{('Y' if row.proper_time_all else 'n')}/{('Y' if row.geometry_all else 'n')}/{('Y' if row.mixed_all else 'n')}"
        )
    return "\n".join(lines)


def render_rediscovery_limit_aggregate_table(
    rows: list[RediscoveryLimitAggregateRow],
) -> str:
    lines = [
        "limit | family   | cases | survives | sel kept | base alive | R ovlp | P ovlp | G ovlp | M ovlp",
        "------+----------+-------+----------+----------+------------+--------+--------+--------+-------",
    ]
    for row in rows:
        lines.append(
            f"{row.rediscovery_limit:>5} | "
            f"{row.rule_family:<8} | "
            f"{row.cases:>5} | "
            f"{row.survives:>8} | "
            f"{row.selected_retained:>8} | "
            f"{row.base_selected_alive:>10} | "
            f"{row.robustness_overlap:>6} | "
            f"{row.proper_time_overlap:>6} | "
            f"{row.geometry_overlap:>6} | "
            f"{row.mixed_overlap:>5}"
        )
    return "\n".join(lines)


def render_procedural_failure_diagnostic_table(
    rows: list[ProceduralFailureDiagnosticRow],
) -> str:
    lines = [
        "scenario         | variant      | selected rule        | status    | mixed | gap/span      | mean c | c-range | c-var | cross | s-range",
        "-----------------+--------------+----------------------+-----------+-------+---------------+--------+---------+-------+-------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.scenario_name:<15} | "
            f"{row.variant_name:<12} | "
            f"{row.selected_rule:<20} | "
            f"{row.status:<9} | "
            f"{'yes' if row.mixed_overlap else 'no ':<5} | "
            f"{row.center_gap:>5.3f}/{row.arrival_span:<5.3f} | "
            f"{row.mean_center:>6.2f} | "
            f"{row.center_range:>7.2f} | "
            f"{row.center_total_variation:>5.2f} | "
            f"{'yes' if row.crosses_midline else 'no ':<5} | "
            f"{row.span_range:>6}"
        )
    return "\n".join(lines)


def render_contour_sensitivity_table(
    rows: list[ContourSensitivityRow],
) -> str:
    lines = [
        "alpha | selected rule        | status    | mixed | gap/span      | mean c | c-range | c-var | cross",
        "------+----------------------+-----------+-------+---------------+--------+---------+-------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.alpha:>5.2f} | "
            f"{row.selected_rule:<20} | "
            f"{row.status:<9} | "
            f"{'yes' if row.mixed_overlap else 'no ':<5} | "
            f"{row.center_gap:>5.3f}/{row.arrival_span:<5.3f} | "
            f"{row.mean_center:>6.2f} | "
            f"{row.center_range:>7.2f} | "
            f"{row.center_total_variation:>5.2f} | "
            f"{'yes' if row.crosses_midline else 'no ':<4}"
        )
    return "\n".join(lines)


def render_focus_observable_benchmark_table(
    rows: list[FocusObservableBenchmarkRow],
) -> str:
    lines = [
        "observable  | core ok | geom ok/prom | proc ok/prom | contour ok | contour miss",
        "------------+---------+--------------+--------------+------------+--------------",
    ]
    for row in rows:
        lines.append(
            f"{row.observable:<10} | "
            f"{row.core_preserved:>2}/{row.core_cases:<2} | "
            f"{row.geometry_preserved:>2}/{row.geometry_survive_cases:<2} +{row.geometry_promoted:>1}/{row.geometry_non_survive_cases:<1} | "
            f"{row.procedural_preserved:>2}/{row.procedural_survive_cases:<2} +{row.procedural_promoted:>1}/{row.procedural_non_survive_cases:<1} | "
            f"{row.contour_survive_preserved:>2}/{row.contour_survive_cases:<2} | "
            f"{row.contour_miss_status:<8} {row.contour_miss_score:>5.2f}"
        )
    return "\n".join(lines)


def render_frontier_observable_ablation_table(
    rows: list[FrontierObservableAblationRow],
) -> str:
    lines = [
        "observable  | family   | cases | sel chg | sel surv | base surv | sel R/P/G/M | base R/P/G/M",
        "------------+----------+-------+---------+----------+-----------+-------------+--------------",
    ]
    for row in rows:
        lines.append(
            f"{row.observable:<10} | "
            f"{row.rule_family:<8} | "
            f"{row.cases:>5} | "
            f"{row.selected_changes:>7} | "
            f"{row.selected_survives:>8} | "
            f"{row.baseline_selected_survives:>9} | "
            f"{row.selected_on_robustness:>3}/{row.selected_on_proper_time:<1}/{row.selected_on_geometry:<1}/{row.selected_on_mixed:<1}       | "
            f"{row.baseline_on_robustness:>4}/{row.baseline_on_proper_time:<1}/{row.baseline_on_geometry:<1}/{row.baseline_on_mixed:<1}"
        )
    return "\n".join(lines)


def render_frontier_observable_change_table(
    rows: list[FrontierObservableChangeRow],
    limit: int = 12,
) -> str:
    lines = [
        "pack   | scenario         | family   | w    | baseline -> observable | base@obs  | sel@obs  | base R/P/G/M | obs R/P/G/M",
        "-------+------------------+----------+------+------------------------+-----------+----------+--------------+-------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.pack_name:<6} | "
            f"{row.scenario_name:<16} | "
            f"{row.rule_family:<8} | "
            f"{row.retained_weight:>4.2f} | "
            f"{row.baseline_selected_rule:<9}->{row.observable_selected_rule:<9} | "
            f"{row.baseline_selected_status:<9} | "
            f"{row.observable_selected_status:<8} | "
            f"{('Y' if row.baseline_on_robustness else 'n')}/{('Y' if row.baseline_on_proper_time else 'n')}/{('Y' if row.baseline_on_geometry else 'n')}/{('Y' if row.baseline_on_mixed else 'n'):<4} | "
            f"{('Y' if row.observable_on_robustness else 'n')}/{('Y' if row.observable_on_proper_time else 'n')}/{('Y' if row.observable_on_geometry else 'n')}/{('Y' if row.observable_on_mixed else 'n')}"
        )
    return "\n".join(lines)


def main() -> None:
    print("DISCRETE EVENT-NETWORK TOY MODEL")
    print()
    derived_nodes = build_rectangular_nodes(width=12, height=8)
    flat_postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
    )
    distorted_postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
    )
    free_rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=flat_postulates,
    )
    chosen_rule = select_self_maintenance_rule(
        derived_nodes,
        preferred_rule_pairs=WINNER_RULE_PAIRS,
        preferred_bonus=0.05,
    )
    pattern_seed = point_seed(center=chosen_rule.seed_node)
    persistent_nodes = chosen_rule.persistent_nodes
    occupancy = chosen_rule.occupancy
    orbit_sizes = chosen_rule.orbit_sizes
    distorted_rule = derive_local_rule(
        persistent_nodes=persistent_nodes,
        postulates=distorted_postulates,
    )
    derived_support = derive_persistence_support(derived_nodes, persistent_nodes)
    derived_field = derive_node_field(derived_nodes, distorted_rule)
    centroid_x, centroid_y = field_centroid(derived_field)
    source_y = max(-8, min(8, round(centroid_y)))
    arrival_source_y = max(-6, min(6, source_y))
    geodesic_target_ys = clamped_offsets(source_y, offsets=[-4, 0, 4], height=8)
    arrival_sample_ys = clamped_offsets(arrival_source_y, offsets=[-6, -3, 0, 3, 6], height=6)
    sorted_persistent_nodes = sorted(persistent_nodes)
    centroid_node = min(
        sorted_persistent_nodes,
        key=lambda node: ((node[0] - centroid_x) ** 2 + (node[1] - centroid_y) ** 2, node),
    )

    print("1) Stationary-action geodesics from the shared local rule")
    geodesic_rows = compare_geodesics(
        width=12,
        height=8,
        source=(0, source_y),
        target_ys=geodesic_target_ys,
        free_rule=free_rule,
        distorted_rule=distorted_rule,
    )
    print(render_geodesic_table(geodesic_rows))
    print()
    print("Interpretation:")
    print("- These paths minimize local action increments while causal order still comes from the same local-delay rule that defines the async DAG.")
    print(f"- The source row is recentered to the emergent field centroid at y ~= {centroid_y:.3f}, so we are testing bending toward the mass-like pattern rather than toward a fixed global down direction.")
    print("- The action now comes from a proper-time-style deficit computed from the same local delay field, so there is no separate attraction knob.")
    print("- In the distorted region that deficit is smaller, so off-center paths stay close to the centroid longer before peeling away.")
    print("- That is closer to an attractive gravity-like limit, though the specific extremal principle is still assumed rather than derived.")
    print()

    print("2) Emergent persistent pattern and derived field")
    print(
        "seed size = "
        f"{len(pattern_seed)}; selected seed = {chosen_rule.seed_node}; "
        f"selected rule = S{sorted(chosen_rule.survive_counts)}/B{sorted(chosen_rule.birth_counts)}; "
        f"late-orbit sizes = {orbit_sizes}; persistent nodes = {len(persistent_nodes)}; "
        f"occupancy mean = {chosen_rule.occupancy_mean:.3f}; support sum = {chosen_rule.support_sum:.3f}; "
        f"density = {chosen_rule.density:.3f}; area = {chosen_rule.area}"
    )
    field_rows = sample_pattern(
        occupancy,
        derived_support,
        derived_field,
        sample_nodes=[
            sorted_persistent_nodes[0],
            centroid_node,
            sorted_persistent_nodes[-1],
            (round(centroid_x), source_y),
            (0, source_y),
        ],
    )
    print(render_field_samples(field_rows))
    print(f"effective field centroid ~= ({centroid_x:.3f}, {centroid_y:.3f})")
    print()
    print("Interpretation:")
    print("- A minimal one-node disturbance and its local self-maintenance rule are now selected together by searching all interior one-node seeds against a compact rule family.")
    print("- The persistent pattern is defined by late-time occupancy of the selected rule's repeating orbit rather than a hand-picked snapshot.")
    print("- The chosen pattern is the most localized stable non-boundary component under transparent criteria: high occupancy, high density, strong internal support, and small area.")
    print("- The slowing field is then the equilibrium of that persistent pattern under local neighbor averaging, so mass-like sourcing comes from the pattern's own self-maintained structure.")
    print("- The effective field centroid can drift away from the pattern's geometric center, which is a nice sign that boundaries and environment matter to what counts as mass-like load.")
    print()

    print("3) Emergent causal order from positive local delays")
    free_arrivals = infer_causal_arrival_times(
        width=12,
        height=6,
        source=(0, arrival_source_y),
        rule=free_rule,
    )
    distorted_arrivals = infer_causal_arrival_times(
        width=12,
        height=6,
        source=(0, arrival_source_y),
        rule=distorted_rule,
    )
    boundary_rows = sample_boundary_arrivals(
        width=12,
        sample_ys=arrival_sample_ys,
        free_arrivals=free_arrivals,
        distorted_arrivals=distorted_arrivals,
    )
    print(render_arrival_table(boundary_rows))
    print()
    print("Interpretation:")
    print("- No global step counter is used here; causal order is inferred from positive local delays.")
    print("- The emergent mass-like pattern reshapes causal order asymmetrically across the boundary detectors.")
    print()

    print("4) Two-slit event network with and without durable path records")
    screen_positions = list(range(-10, 11))
    coherent = two_slit_distribution(screen_positions, record_created=False)
    recorded = two_slit_distribution(screen_positions, record_created=True)
    positive_only = two_slit_distribution(
        screen_positions,
        record_created=False,
        positive_only=True,
    )
    print(render_distribution("coherent histories", coherent))
    print()
    print(render_distribution("durable path record created", recorded))
    print()
    print(render_distribution("positive weights only (no phase cancellation)", positive_only))
    print()
    print("Interpretation:")
    print("- Interference appears only when alternative histories combine before scoring.")
    print("- Durable records remove cross-branch interference even with no conscious observer.")
    print("- The remaining structure in each record sector is single-slit diffraction from local paths.")
    print("- Positive-only weights cannot reproduce destructive interference dips.")
    print()

    print("5) Continuous phase shift pressure test")
    phase_scan = center_detector_phase_scan(
        [index * math.pi / 4 for index in range(9)]
    )
    print(render_phase_scan(phase_scan))
    print()
    print("Interpretation:")
    print("- Complex phases let a local phase shifter smoothly tune detection rates.")
    print("- This is one reason positive real weights are too weak for quantum behavior.")
    print()

    print("6) Born-rule pressure test")
    born_test = born_rule_pressure_test()
    print(render_born_test(born_test))
    print()
    print("Interpretation:")
    print("- If amplitudes evolve by reversible linear mixing, the 2-norm is singled out.")
    print("- That does not derive the square rule from nothing, but it constrains the cheat.")
    print()

    print("7) Local symmetry pressure test")
    symmetry_rows = retained_update_symmetry_test()
    print(render_symmetry_table(symmetry_rows))
    print()
    print("Interpretation:")
    print("- If local neighborhoods admit a universal signal speed and boost-like frame mixing, the retained update sqrt(dt^2 - dx^2) is the stable scalar.")
    print("- The action we use is then interpreted as spent delay: coordinate delay minus retained update.")
    print("- That does not fully derive the rule, but it narrows the remaining assumption to the accounting step rather than the invariant itself.")
    print()

    print("8) Robustness sweep across shapes, boundaries, and rule families")
    robustness_rows = run_robustness_sweep(distorted_postulates)
    family_diagnostics = summarize_robustness(robustness_rows)
    print(render_robustness_table(robustness_rows))
    print()
    print(render_family_diagnostics_table(family_diagnostics))
    print()
    print(render_failure_diagnostics_table(robustness_rows))
    print()
    survived_count = sum(row.survived for row in robustness_rows)
    mixed_count = sum(row.status == "mixed" for row in robustness_rows)
    no_pattern_count = sum(row.status == "no pattern" for row in robustness_rows)
    family_by_name = {row.rule_family: row for row in family_diagnostics}
    failure_rows = [row for row in robustness_rows if row.status != "survives"]
    dominant_failures = Counter(row.dominant_rejection for row in failure_rows)
    dominant_failure_label = dominant_failures.most_common(1)[0][0] if dominant_failures else "none"
    no_pattern_rows = [row for row in robustness_rows if row.status == "no pattern"]
    no_pattern_failures = Counter(row.dominant_rejection for row in no_pattern_rows)
    no_pattern_label = no_pattern_failures.most_common(1)[0][0] if no_pattern_failures else "none"
    skew_rows = [row for row in robustness_rows if row.scenario_name.startswith("skew")]
    fallback_rescues = sum(row.fallback_used and row.status != "no pattern" for row in robustness_rows)
    print("Interpretation:")
    print("- Each scenario varies graph shape, vertical boundary treatment, or the searched local rule family while keeping the same ontology.")
    print("- `center gap` measures whether the action-favored path stays focused near the emergent field centroid instead of peeling away immediately.")
    print("- `arrival span` measures how non-uniform the induced boundary delay shifts are across the far edge.")
    print(f"- In this run, {survived_count} scenarios were `survives`, {mixed_count} were `mixed`, and {no_pattern_count} produced no compact persistent pattern under the sweep budget.")
    print(f"- The staged search rescued {fallback_rescues} scenarios that the primary point-seed search did not solve on its own.")
    print("- The family table adds an explanatory layer: average selected-rule breadth, average persistent-node count, and the dominant winning rule signature.")
    compact_family = family_by_name.get("compact")
    extended_family = family_by_name.get("extended")
    if compact_family and extended_family:
        if compact_family.survives == 6 and extended_family.survives == 6:
            print(f"- With the minimal compact subset, both families now survive all six scenarios; `extended` still produces the larger average boundary-delay span ({extended_family.avg_arrival_span:.3f} vs {compact_family.avg_arrival_span:.3f}), while `compact` keeps the slightly larger average center gap ({compact_family.avg_center_gap:.3f} vs {extended_family.avg_center_gap:.3f}).")
        elif compact_family.no_pattern == 0 and extended_family.no_pattern == 0:
            print(f"- Under the staged search, both families now find compact patterns in all sweep scenarios; `extended` produces the larger average boundary-delay span ({extended_family.avg_arrival_span:.3f} vs {compact_family.avg_arrival_span:.3f}), while `compact` now has the slightly larger average center gap ({compact_family.avg_center_gap:.3f} vs {extended_family.avg_center_gap:.3f}).")
        else:
            print(f"- Here the `extended` family looks healthier because it found compact patterns in {6 - extended_family.no_pattern}/6 cases versus {6 - compact_family.no_pattern}/6 for `compact`, and its active cases produced a larger average boundary-delay span ({extended_family.avg_arrival_span:.3f} vs {compact_family.avg_arrival_span:.3f}).")
    if failure_rows:
        print(f"- Across the non-surviving cases, the most common rejection mode was `{dominant_failure_label}`.")
        if no_pattern_count:
            print(f"- Among the strict `no pattern` cases, the dominant blocker was `{no_pattern_label}`, which helps tell us whether the issue is topology-driven or just selector strictness.")
        else:
            print("- There are no remaining strict `no pattern` cases in this sweep, so the current bottleneck has shifted from pattern existence to pattern quality.")
        if skew_rows:
            print(f"- In the skewed geometries specifically, the search failed mostly by producing empty or fragmented candidates ({sum(row.empty_patterns for row in skew_rows)} empty, {sum(row.disconnected_rejections for row in skew_rows)} split, {sum(row.boundary_rejections for row in skew_rows)} boundary), so the current weakness looks more like pattern-formation difficulty than boundary filtering.")
    else:
        print("- There are no non-surviving cases in this sweep, so within the current budget the remaining question is no longer `does the compact family fail?` but `how small can the compact family stay while preserving the hard-topology winners?`.")
    print("- This does not prove universality, but it starts separating structural behavior from single-geometry artifacts.")
    print()

    print("9) Minimal compact subset that preserves the hard-topology winners")
    focused_rows = focused_skew_wrap_diagnosis(distorted_postulates)
    repaired_subset, hard_rows = derive_motif_preserving_compact_subset(distorted_postulates)
    minimal_subset, minimal_rows = derive_smallest_surviving_subset(
        repaired_subset,
        distorted_postulates,
    )
    print(render_focused_comparison_table(focused_rows))
    print()
    print("Interpretation:")
    print("- The legacy reduced family is shown only as a diagnosis baseline; the current compact sweep uses the minimal surviving subset.")
    focused_by_label = {row.label: row for row in focused_rows}
    legacy_reduced = focused_by_label.get("legacy reduced")
    repaired_reduced = focused_by_label.get("four-option repair")
    minimal_reduced = focused_by_label.get("minimal three")
    compact_full = focused_by_label.get("compact full")
    if legacy_reduced and repaired_reduced:
        print(f"- In `skew-wrap`, the legacy reduced family picked {legacy_reduced.rule_signature} and stayed `{legacy_reduced.status}`, while the repaired four-option family upgrades to {repaired_reduced.rule_signature} and lands `{repaired_reduced.status}`.")
    if minimal_reduced and compact_full and minimal_reduced.rule_signature == compact_full.rule_signature:
        print(f"- The minimal three-option family and the full compact family converge on the same hard-case winner, {minimal_reduced.rule_signature}, so we do not need the full compact palette to keep that behavior.")
    hard_rule_signatures = ", ".join(
        f"{row.scenario_name} -> {row.rule_signature}"
        for row in hard_rows
    )
    print(f"- Under the full compact family, the hard-topology winners are {hard_rule_signatures}.")
    print(f"- Preserving those hard-topology winners first repairs the compact family to {format_count_options(repaired_subset)}.")
    print(f"- Exhaustive minimization inside that repaired family then shrinks it further to {format_count_options(minimal_subset)} while still surviving all six sweep scenarios.")
    if minimal_subset == SWEEP_COMPACT_COUNT_OPTIONS and all(row.status == 'survives' for row in minimal_rows):
        print("- That is the current compact sweep family, so we can proceed with a genuinely minimal reduced subset instead of treating motif omission as a blocker.")
    print()

    print("10) One-by-one ablation of the minimal compact subset")
    ablation_rows = ablate_compact_subset(SWEEP_COMPACT_COUNT_OPTIONS, distorted_postulates)
    print(render_ablation_table(ablation_rows))
    print()
    print("Interpretation:")
    print("- This asks the sharper question: once the compact family is minimal, which surviving-count options are actually indispensable?")
    option_labels = {row.removed_option: row for row in ablation_rows}
    remove_13 = option_labels.get("[1, 3]")
    remove_23 = option_labels.get("[2, 3]")
    remove_34 = option_labels.get("[3, 4]")
    if remove_13:
        print(f"- Removing `[1, 3]` breaks `skew-wrap` first ({remove_13.failed_scenarios}), so that motif is carrying the hardest wrapped skew case.")
    if remove_23:
        print(f"- Removing `[2, 3]` breaks `taper-wrap` first ({remove_23.failed_scenarios}), so that motif is doing important work for the wrapped tapered geometry.")
    if remove_34:
        print(f"- Removing `[3, 4]` is the most damaging ablation ({remove_34.failed_scenarios}), which makes it look like the strongest structural motif in the current compact family.")
    print("- In other words, the current compact family is no longer just small; within the current sweep it is irreducible.")
    print()

    print("11) Mechanism ablation of the load-bearing assumptions")
    mechanism_rows = mechanism_ablation_results()
    print(render_mechanism_ablation_table(mechanism_rows))
    print()
    print("Interpretation:")
    print("- This tests the deeper question behind the toy theory: which assumptions in the dynamics are actually carrying the gravity-like behavior, and which are still underconstrained?")
    mechanism_by_label = {row.label: row for row in mechanism_rows}
    baseline_mechanism = mechanism_by_label.get("baseline")
    coordinate_action = mechanism_by_label.get("coordinate-delay action")
    link_length_action = mechanism_by_label.get("link-length action")
    support_only_field = mechanism_by_label.get("support-only field")
    no_field_mechanism = mechanism_by_label.get("no field")
    if baseline_mechanism:
        print(f"- The baseline survives all six compact-family scenarios with average gap {baseline_mechanism.avg_center_gap:.3f} and average span {baseline_mechanism.avg_arrival_span:.3f}.")
    if coordinate_action:
        print(f"- Replacing spent-delay action with plain coordinate delay weakens the model enough to break {coordinate_action.failed_scenarios}, so the action accounting is doing some real work.")
    if support_only_field:
        print(f"- Replacing relaxed field propagation with raw local support weakens the hardest wrapped skew case ({support_only_field.failed_scenarios}), which is strong evidence that field relaxation is load-bearing.")
    if no_field_mechanism:
        print(f"- Removing the field entirely collapses the whole effect ({no_field_mechanism.failed_scenarios}), so the delay field is definitely not decorative.")
    if link_length_action:
        print(f"- The uncomfortable result is that bare link-length action still survives the current sweep, which means the present robustness metric does not yet uniquely single out the proper-time-style action.")
    print("- That last point is probably the clearest sign of where we still need to go before calling this a genuinely strong toy-theory result: we need a sharper discriminator that rewards the intended action rule and rejects cruder substitutes.")
    print()

    print("12) Action-response discriminator for the chosen geodesics")
    action_rows = action_discriminator_results()
    print(render_action_discriminator_table(action_rows))
    print()
    print("Interpretation:")
    print("- This adds the missing check: if the field really matters to the action rule, the distorted geodesic should move relative to the free geodesic instead of merely inheriting good center-gap scores from geometry alone.")
    action_by_label = {row.label: row for row in action_rows}
    baseline_action = action_by_label.get("baseline")
    coordinate_action = action_by_label.get("coordinate-delay action")
    link_length_action = action_by_label.get("link-length action")
    support_only_action = action_by_label.get("support-only field")
    if baseline_action:
        print(f"- The baseline is the only tested mechanism that both survives all six scenarios and keeps a strictly positive minimum wrapped-case response ({baseline_action.min_wrapped_response:.3f}).")
    if coordinate_action:
        print(f"- Coordinate-delay action fails this discriminator because it breaks {coordinate_action.failed_scenarios} and also drops to zero wrapped-case response in at least one scenario.")
    if link_length_action:
        print(f"- Bare link-length action also fails: it survives the old sweep, but its minimum response is {link_length_action.min_response:.3f}, which means the chosen paths are not reacting to the field at all.")
    if support_only_action:
        print(f"- Support-only field propagation still bends paths, but it does not survive the hard wrapped skew case ({support_only_action.failed_scenarios}), so field relaxation remains part of the load-bearing structure.")
    print("- That is a meaningful upgrade in where we stand: among the named alternatives we tested here, the intended spent-delay action with relaxed field propagation is the only one that survives both robustness and field-response.")
    print()

    print("13) Parameterized retained-weight action family sweep")
    action_family_rows = action_family_results()
    print(render_action_family_table(action_family_rows))
    print()
    print("Interpretation:")
    print("- This widens the action search from a few named formulas to a one-parameter family: action = delay - w * retained_update, with field relaxation held fixed.")
    positive_response_rows = [
        row for row in action_family_rows
        if row.survives == len(robustness_scenarios()) and row.min_wrapped_response > 0.0
    ]
    if positive_response_rows:
        surviving_weights = ", ".join(f"{row.retained_weight:.2f}" for row in positive_response_rows)
        strongest_row = max(positive_response_rows, key=lambda row: row.min_wrapped_response)
        print(f"- Under the combined robustness-plus-response benchmark, the surviving retained-weight window narrows to the high end of the tested family: w = {surviving_weights}.")
        print(f"- Within that window, the strongest wrapped-case path response occurs at w = {strongest_row.retained_weight:.2f} with minimum wrapped response {strongest_row.min_wrapped_response:.3f}.")
    print("- So the broader family sweep does not yet prove that the exact spent-delay coefficient must be 1.0, but it does push us away from the low-weight half of the family and toward the proper-time-style end.")
    print()

    print("14) Cross-pack benchmark for the retained-weight family")
    pack_rows = action_family_pack_results()
    print(render_action_pack_table(pack_rows))
    print()
    print("Interpretation:")
    print("- This broadens the benchmark beyond the original six-scenario sweep by checking the same retained-weight family on larger and mirrored packs as well.")
    all_pack_names = {pack_name for pack_name, _scenarios in benchmark_packs()}
    pack_winners = sorted(
        {
            row.retained_weight
            for row in pack_rows
            if row.pack_pass
        }
    )
    passing_all_packs = [
        weight
        for weight in sorted({row.retained_weight for row in pack_rows})
        if {
            row.pack_name
            for row in pack_rows
            if row.retained_weight == weight and row.pack_pass
        } == all_pack_names
    ]
    if passing_all_packs:
        print(
            "- Across the tested packs, the retained weights that pass every pack-level benchmark are "
            + ", ".join(f"w = {weight:.2f}" for weight in passing_all_packs)
            + "."
        )
    if pack_winners:
        strongest_pack_row = max(
            (row for row in pack_rows if row.pack_pass),
            key=lambda row: (row.min_wrapped_response, row.min_response, row.retained_weight),
        )
        print(
            f"- The strongest pack-level response in the current grid occurs for pack `{strongest_pack_row.pack_name}` at w = {strongest_pack_row.retained_weight:.2f}, with minimum wrapped response {strongest_pack_row.min_wrapped_response:.3f}."
        )
    print("- This is encouraging but still not a full derivation: the benchmark keeps narrowing us toward the high-retained-update end, but it has not yet collapsed the family to a single exact coefficient.")
    print()

    print("15) High-end proper-time consistency benchmark")
    proper_time_rows = proper_time_consistency_results()
    print(render_proper_time_consistency_table(proper_time_rows))
    print()
    print("Interpretation:")
    print("- This is a sharper high-end zoom: for every pack and every off-center boundary target, it asks whether the distorted geodesic saves more action than the extra coordinate delay it willingly spends in the field.")
    print("- A positive margin here means the path choice is being driven by full retained-update leverage rather than by a weaker partial weighting that still bends the path but never quite dominates the extra delay.")
    proper_time_winners = [row for row in proper_time_rows if row.pass_all]
    if proper_time_winners:
        print(
            "- In the tested high-end grid, the retained weights that keep that margin positive across every surviving pack and wrapped case are "
            + ", ".join(f"w = {row.retained_weight:.2f}" for row in proper_time_winners)
            + "."
        )
    strongest_proper_time = max(
        proper_time_rows,
        key=lambda row: (row.min_margin, row.min_wrapped_margin, row.retained_weight),
    )
    print(
        f"- The strongest minimum margin in this grid occurs at w = {strongest_proper_time.retained_weight:.2f}, with worst case `{strongest_proper_time.worst_case}` and minimum margin {strongest_proper_time.min_margin:.3f}."
    )
    print("- This still is not a first-principles derivation, but it is the first benchmark in this toy model that singles out the exact spent-delay point within a tested retained-weight family.")
    print()

    print("16) Critical-weight decomposition of the w = 1 crossing")
    critical_rows = critical_weight_cases()
    print(render_critical_weight_table(critical_rows))
    print()
    print("Interpretation:")
    print("- For a fixed distorted path, the proper-time consistency margin is linear in the retained weight: margin(w) = w * retained_total - 2 * delay_penalty.")
    print("- That means each off-center target carries a calculable critical weight w* = 2 * delay_penalty / retained_total, above which that path finally pays for the extra coordinate delay it spends in the field.")
    if critical_rows:
        worst_row = critical_rows[0]
        print(
            f"- In the current run the largest observed threshold is w* = {worst_row.critical_weight:.3f} at `{worst_row.pack_name}:{worst_row.scenario_name}` targeting y = {worst_row.target_y}, with margin@1 = {worst_row.margin_at_one:.3f}."
        )
    print("- That does not derive the spent-delay rule from deeper symmetry yet, but it does explain the empirical crossing: the hardest cases need a coefficient just under 1, which is why 0.95 still fails while 1.00 passes.")
    print("- So the model is now doing something stronger than brute-force search: it is exposing a specific accounting identity that controls where the retained-weight family changes sign.")
    print()

    print("17) Active-branch scan of the hardest crossing case")
    hardest_pack = critical_rows[0].pack_name if critical_rows else "large"
    hardest_scenario = critical_rows[0].scenario_name if critical_rows else "skew-wrap-large"
    branch_rows = weight_branch_scan(hardest_pack, hardest_scenario)
    print(render_weight_branch_scan_table(branch_rows))
    print()
    print("Interpretation:")
    print("- The global benchmark is not one fixed line in w; it is the lower envelope of the active rule-and-path branches selected by the search.")
    if branch_rows:
        start_rule = branch_rows[0].rule_signature
        end_rule = branch_rows[-1].rule_signature
        if start_rule != end_rule:
            print(
                f"- In the hardest case, the active branch switches from `{start_rule}` at low high-end weights to `{end_rule}` near the crossing, so the final sign change is a branch-switch plus a linear margin crossing, not just one branch sliding upward."
            )
        else:
            print(
                f"- In the hardest case, the same branch `{start_rule}` remains active across the scanned weights, so the sign change is a single linear crossing."
            )
        final_row = branch_rows[-1]
        print(
            f"- At the top end of the scan, the active branch carries critical weight w* = {final_row.critical_weight:.3f}; that is why the margin is still negative at 0.95 but positive at 1.00."
        )
    print("- This is the more rigorous picture: the toy model’s retained-weight benchmark is piecewise linear in w because the optimizer can switch motifs, sources, and paths as w changes.")
    print()

    print("18) Why the current selector prefers the rescue motif")
    selection_rows = rule_selection_diagnostics(hardest_pack, hardest_scenario)
    print(render_rule_selection_diagnostic_table(selection_rows))
    print()
    print("Interpretation:")
    print("- This separates the search stages. The fallback scan keeps proposing one compact motif, while the rescue stage evaluates a small winner-rule palette by the same quality key the current always-compare selector uses.")
    if selection_rows:
        low_row = selection_rows[0]
        high_row = selection_rows[-1]
        low_fallback_quality = low_row.fallback_center_gap + low_row.fallback_arrival_span
        low_rescue_quality = low_row.rescue_center_gap + low_row.rescue_arrival_span
        high_fallback_quality = high_row.fallback_center_gap + high_row.fallback_arrival_span
        high_rescue_quality = high_row.rescue_center_gap + high_row.rescue_arrival_span
        if all(row.switched for row in selection_rows):
            print(
                f"- On the current hardest case, the rescue motif `{low_row.rescue_rule}` wins the quality comparison at every scanned weight, even though the fallback motif `{low_row.fallback_rule}` also stays `{low_row.fallback_status}` throughout."
            )
            print(
                f"- At w = {low_row.retained_weight:.2f}, the fallback branch has the slightly larger center gap ({low_row.fallback_center_gap:.3f} vs {low_row.rescue_center_gap:.3f}), but the rescue branch carries much larger arrival span ({low_row.rescue_arrival_span:.3f} vs {low_row.fallback_arrival_span:.3f}), so the total quality key already favors rescue ({low_rescue_quality:.3f} vs {low_fallback_quality:.3f})."
            )
            print(
                f"- By w = {high_row.retained_weight:.2f}, the rescue branch also edges ahead in center gap ({high_row.rescue_center_gap:.3f} vs {high_row.fallback_center_gap:.3f}) while keeping the same span advantage, so the preference is even cleaner ({high_rescue_quality:.3f} vs {high_fallback_quality:.3f})."
            )
        else:
            print(
                f"- At low scanned weights, the fallback motif `{low_row.fallback_rule}` remains the final choice."
            )
            print(
                f"- Later in the scan, the rescue motif `{high_row.rescue_rule}` overtakes it because the quality comparison changes, not because the search discovers a completely new type of structure."
            )
    print("- So the selector is not maximizing proper-time consistency by itself. It is maximizing a hand-chosen robustness quality, and on the current hardest case that quality prefers the rescue motif from the start.")
    print()

    print("19) Frozen-branch competition on the hardest case")
    frozen_rows = fixed_branch_competition(hardest_pack, hardest_scenario)
    print(render_fixed_branch_competition_table(frozen_rows))
    print()
    print("Interpretation:")
    print("- This removes one more layer of heuristic freedom: the two competing persistent patterns are frozen, and only the action weight w is varied.")
    print("- That means any crossover we still see is coming from the dynamics and robustness metrics, not from the search rediscovering different patterns at each weight.")
    fallback_rows = [row for row in frozen_rows if row.branch_label == 'fallback-fixed']
    rescue_rows = [row for row in frozen_rows if row.branch_label == 'rescue-fixed']
    if fallback_rows and rescue_rows:
        fallback_positive = next((row.retained_weight for row in fallback_rows if row.min_margin > 0.0), None)
        rescue_positive = next((row.retained_weight for row in rescue_rows if row.min_margin > 0.0), None)
        print(
            f"- The frozen fallback branch `{fallback_rows[0].rule_signature}` becomes proper-time-consistent earlier, with minimum margin rising from {fallback_rows[0].min_margin:.3f} to {fallback_rows[-1].min_margin:.3f}{'' if fallback_positive is None else f' and turning positive by w = {fallback_positive:.2f}' }."
        )
        print(
            f"- The frozen rescue branch `{rescue_rows[0].rule_signature}` keeps the much larger arrival span ({rescue_rows[0].arrival_span:.3f} vs {fallback_rows[0].arrival_span:.3f}) and only becomes proper-time-consistent near the top end{'' if rescue_positive is None else f', at w = {rescue_positive:.2f}' }."
        )
        print(
            f"- Both frozen branches remain `{fallback_rows[0].status}`/`{rescue_rows[0].status}` under the present sweep criteria, so the current selector is not choosing between 'working' and 'failing' physics here. It is choosing between an earlier proper-time win and a stronger delay-distortion signature."
        )
    print("- So the hardest current case exposes a sharper tension than before: the selected branch is not the earliest proper-time winner, but the branch that looks strongest under the present robustness quality key.")
    print()

    print("20) Geometric meaning of center-gap collapse")
    geometry_rows = center_gap_geometry_diagnostics(hardest_pack, hardest_scenario)
    print(render_center_gap_geometry_table(geometry_rows))
    print()
    print("Interpretation:")
    print("- This asks the geometric question directly: does center-gap collapse come from path shapes changing, from the source row shifting, or from the action contrast between fixed center and side routes collapsing?")
    if geometry_rows:
        fallback_geometry = next(
            (row for row in geometry_rows if row.branch_label == "fallback-fixed"),
            None,
        )
        rescue_geometry = next(
            (row for row in geometry_rows if row.branch_label == "rescue-fixed"),
            None,
        )
        if fallback_geometry is not None:
            print(
                f"- On the old branch, the source row stays at y = {fallback_geometry.source_y_start} and the comparison paths remain {'the same' if fallback_geometry.stable_paths else 'different'} from w = 0.75 to w = 1.00."
            )
            print(
                f"- Its center action falls from {fallback_geometry.center_action_start:.3f} to {fallback_geometry.center_action_end:.3f}, while the side average falls from {fallback_geometry.side_avg_start:.3f} to {fallback_geometry.side_avg_end:.3f}. That changes the gap from {fallback_geometry.gap_start:.3f} to {fallback_geometry.gap_end:.3f}."
            )
        if rescue_geometry is not None:
            print(
                f"- The rescue branch keeps the same source row at y = {rescue_geometry.source_y_start}, changes path shape as w rises, and ends with gap {rescue_geometry.gap_end:.3f}."
            )
            if fallback_geometry is not None:
                print(
                    f"- So the current selector is not responding to a source-row jump. It is comparing two fixed-source branches whose final action contrast and delay-distortion trade off differently ({fallback_geometry.gap_end:.3f} vs {rescue_geometry.gap_end:.3f} in final gap)."
                )
    print("- The geometry diagnostic now points to the same issue as the frozen-branch comparison: the selector is sensitive to how much path contrast survives together with the broader boundary-delay signal, not just to proper-time margin.")
    print()

    print("21) Alternative focus metrics on the frozen hard-case branches")
    focus_rows = focus_metric_comparison(hardest_pack, hardest_scenario)
    print(render_focus_metric_comparison_table(focus_rows))
    print()
    print("Interpretation:")
    print("- This asks whether the hard-case ranking is specific to the current action-gap focus metric or whether it survives under more geometric observables.")
    if focus_rows:
        first_focus = focus_rows[0]
        last_focus = focus_rows[-1]
        if first_focus.action_winner == last_focus.action_winner:
            print(
                f"- Under raw action-gap, the {first_focus.action_winner} branch wins throughout the scan ({first_focus.fallback_action_gap:.3f}/{first_focus.rescue_action_gap:.3f} at w = {focus_rows[0].retained_weight:.2f}, {last_focus.fallback_action_gap:.3f}/{last_focus.rescue_action_gap:.3f} at w = {focus_rows[-1].retained_weight:.2f})."
            )
        else:
            print(
                f"- Under raw action-gap, the ranking flips across the scan: `{first_focus.action_winner}` wins at w = {focus_rows[0].retained_weight:.2f} ({first_focus.fallback_action_gap:.3f}/{first_focus.rescue_action_gap:.3f}), but `{last_focus.action_winner}` wins by w = {focus_rows[-1].retained_weight:.2f} ({last_focus.fallback_action_gap:.3f}/{last_focus.rescue_action_gap:.3f})."
            )
        print(
            f"- Under pure geometric focus gap, the {first_focus.geometric_winner} branch wins throughout ({first_focus.fallback_geometric_gap:.3f}/{first_focus.rescue_geometric_gap:.3f} at the start, unchanged in winner at the end)."
        )
        print(
            f"- The stiffness ratio, which measures action-gap per unit geometric separation, favors the {first_focus.stiffness_winner} branch throughout and captures the fact that no single focus observable is emerging as uniquely canonical here."
        )
    print("- So `center gap` is not a neutral physical truth of the toy model. It is one particular focusing observable, and metric choice materially changes which branch looks best.")
    print()

    print("22) Legacy gated selector versus current always-compare selection")
    selector_rows = selector_policy_diagnostics(hardest_pack, hardest_scenario)
    print(render_selector_policy_table(selector_rows))
    print()
    selector_sweep_rows = selector_policy_sweep_cases()
    differing_sweep_rows = [row for row in selector_sweep_rows if row.differs]
    print(render_selector_sweep_table(differing_sweep_rows, limit=len(differing_sweep_rows)))
    print()
    print("Interpretation:")
    print("- The current resolver always compares fallback and rescue candidates by the same quality key. This section compares that baseline against the older gated policy, which only consulted rescue after the fallback branch dropped below `survives`.")
    if selector_rows:
        differing_rows = [row for row in selector_rows if row.differs]
        if differing_rows:
            print(
                f"- On the current hardest case, the legacy gated selector keeps `{differing_rows[0].gated_final_rule}` while the current selector prefers `{differing_rows[0].ungated_final_rule}` over the full differing window w = {differing_rows[0].retained_weight:.2f}..{differing_rows[-1].retained_weight:.2f}."
            )
    if differing_sweep_rows:
        changed_scenarios = ", ".join(
            sorted({f"{row.pack_name}:{row.scenario_name}" for row in differing_sweep_rows})
        )
        print(
            f"- Across the compact benchmark packs, changing only the selector policy alters {len(differing_sweep_rows)}/{len(selector_sweep_rows)} pack-weight cases, concentrated in {changed_scenarios}."
        )
        if all(row.gated_status == row.ungated_status == "survives" for row in differing_sweep_rows):
            print("- Every changed case still `survives` under both selectors, so selector policy is steering branch choice more than pass/fail status.")
    print("- This is the cleanest current conclusion: both the focusing metric and the selector policy are load-bearing choices in the present toy model.")
    print()

    print("23) Selector-free frontier overview")
    frontier_scenario_rows, frontier_candidates = frontier_sweep_results()
    interesting_frontier_rows = [
        row
        for row in frontier_scenario_rows
        if len({row.robustness_rules, row.proper_time_rules, row.geometry_rules, row.mixed_rules}) > 1
        or not (
            row.selected_on_robustness
            and row.selected_on_proper_time
            and row.selected_on_geometry
            and row.selected_on_mixed
        )
    ]
    print(
        render_frontier_scenario_table(
            interesting_frontier_rows,
            limit=min(12, len(interesting_frontier_rows)),
        )
    )
    print()
    print("Interpretation:")
    total_frontier_cases = len(frontier_scenario_rows)
    print("- This keeps all viable motifs in play instead of collapsing immediately to one winner.")
    print(
        f"- Across {total_frontier_cases} family-pack-weight cases, {len(interesting_frontier_rows)} show either frontier disagreement between views or a current selector that is not on every frontier."
    )
    print(
        f"- The current selector lies on the robustness/proper-time/geometry/mixed frontiers in "
        f"{sum(row.selected_on_robustness for row in frontier_scenario_rows)}/{total_frontier_cases}, "
        f"{sum(row.selected_on_proper_time for row in frontier_scenario_rows)}/{total_frontier_cases}, "
        f"{sum(row.selected_on_geometry for row in frontier_scenario_rows)}/{total_frontier_cases}, and "
        f"{sum(row.selected_on_mixed for row in frontier_scenario_rows)}/{total_frontier_cases} cases."
    )
    print("- So the frontier view is already doing something the scalar selector cannot: it separates 'still viable under some physical reading' from 'currently chosen by one quality key'.")
    print()

    print("24) Frontier motif frequency across both families")
    frontier_aggregate_rows = summarize_frontier_aggregates(frontier_candidates)
    print(render_frontier_aggregate_table(frontier_aggregate_rows[:12]))
    print()
    print("Interpretation:")
    compact_frontier_rows = [row for row in frontier_aggregate_rows if row.rule_family == "compact"]
    extended_frontier_rows = [row for row in frontier_aggregate_rows if row.rule_family == "extended"]
    if compact_frontier_rows:
        print(
            f"- In `compact`, the most persistent frontier motif in this run is `{compact_frontier_rows[0].rule_signature}`, appearing on the mixed frontier in {compact_frontier_rows[0].mixed_hits} cases and being currently selected in {compact_frontier_rows[0].selected_hits}."
        )
    if extended_frontier_rows:
        print(
            f"- In `extended`, the most persistent frontier motif in this run is `{extended_frontier_rows[0].rule_signature}`, appearing on the mixed frontier in {extended_frontier_rows[0].mixed_hits} cases and being currently selected in {extended_frontier_rows[0].selected_hits}."
        )
    print("- This is the selector-invariant layer we wanted: it tells us which motifs keep reappearing as nondominated, even when the current baseline picks only one of them.")
    print()

    print("25) Hard-case frontier trace for the fallback and rescue motifs")
    trace_pack, trace_scenario, frontier_trace_rows = frontier_hard_case_trace()
    print(render_frontier_trace_table(frontier_trace_rows))
    print()
    print("Interpretation:")
    print(f"- This focuses on the current hardest compact case, `{trace_pack}:{trace_scenario}`, and tracks the fallback/rescue motifs across the retained-weight scan.")
    trace_by_signature: DefaultDict[str, list[FrontierTraceRow]] = defaultdict(list)
    for row in frontier_trace_rows:
        trace_by_signature[row.rule_signature].append(row)
    for rule_signature, rows in trace_by_signature.items():
        if rule_signature == "none":
            continue
        print(
            f"- `{rule_signature}` lands on robustness/proper-time/geometry/mixed in "
            f"{sum(row.on_robustness for row in rows)}/{len(rows)}, "
            f"{sum(row.on_proper_time for row in rows)}/{len(rows)}, "
            f"{sum(row.on_geometry for row in rows)}/{len(rows)}, and "
            f"{sum(row.on_mixed for row in rows)}/{len(rows)} weights."
        )
    print("- That is the cleanest selector-free version of the current result: different metric views keep different motifs alive, which is why a single scalar selector still carries real interpretive weight.")
    print()

    print("26) Deterministic topology perturbation ensemble")
    perturbation_aggregate_rows, drift_rows = perturbation_frontier_summary()
    print(render_perturbation_aggregate_table(perturbation_aggregate_rows))
    print()
    print("Interpretation:")
    print("- This is the first perturbation ensemble around the benchmark graphs themselves: instead of asking only which motifs survive the hand-authored topologies, it asks which conclusions survive small deterministic node removals and shifts at the strongest retained-weight point w = 1.0.")
    perturbation_all_rows = [row for row in perturbation_aggregate_rows if row.variant_name == "all"]
    for row in perturbation_all_rows:
        print(
            f"- In `{row.rule_family}`, the perturbed selected rule still `survives` in {row.survives}/{row.cases} cases, matches the unperturbed selected rule in {row.selected_retained}/{row.cases}, and keeps the baseline selected motif alive on some perturbed frontier in {row.base_selected_alive}/{row.cases}."
        )
        print(
            f"- The baseline frontier overlaps persist in robustness/proper-time/geometry/mixed for {row.robustness_overlap}/{row.cases}, {row.proper_time_overlap}/{row.cases}, {row.geometry_overlap}/{row.cases}, and {row.mixed_overlap}/{row.cases} perturbed cases."
        )
    print("- So this section starts turning the frontier layer into a universality test: not 'which motif wins one graph,' but 'which motif and frontier claims survive when the graph itself is nudged.'")
    print()

    print("27) Perturbation drift cases")
    print(render_perturbation_case_table(drift_rows, limit=min(16, len(drift_rows))))
    print()
    print("Interpretation:")
    if drift_rows:
        selected_drift = [row for row in drift_rows if not row.selected_matches_base]
        fragile_drift = [row for row in drift_rows if not row.base_selected_alive]
        print(
            f"- There are {len(drift_rows)} perturbed cases where either the selected motif changes or one of the baseline frontier-overlap claims drops out."
        )
        if selected_drift:
            print(
                f"- In {len(selected_drift)} of them, the selected motif itself changes under perturbation, which is the cleanest sign that some current conclusions are still topology-sensitive."
            )
        if fragile_drift:
            print(
                f"- In {len(fragile_drift)} cases, the unperturbed selected motif is not even frontier-alive after perturbation, which is a stronger failure than a simple selector switch."
            )
    print("- This is exactly the kind of pressure test we wanted: it tells us which current stories are genuinely topology-robust and which ones are still partly artifacts of the specific benchmark graphs.")
    print()

    print("28) Cross-weight stability of the perturbation ensemble")
    perturbation_weight_aggregate_rows, weight_drift_rows = perturbation_weight_stability_summary()
    print(render_perturbation_weight_aggregate_table(perturbation_weight_aggregate_rows))
    print()
    print("Interpretation:")
    print("- This asks a stricter question than the single-weight perturbation pass: not just whether a selector-free motif survives topology nudges at w = 1.0, but whether that topology-robust story also survives when the retained weight is moved down to w = 0.95.")
    weight_all_rows = [row for row in perturbation_weight_aggregate_rows if row.variant_name == "all"]
    for row in weight_all_rows:
        print(
            f"- In `{row.rule_family}`, the same perturbed selected rule survives at both weights in {row.survives_both}/{row.cases} cases, the selected motif itself stays the same in {row.same_selected}/{row.cases}, and the mixed-frontier overlap survives at both weights in {row.mixed_both}/{row.cases}."
        )
        print(
            f"- The tighter selector-free overlaps persist at both weights in robustness/proper-time/geometry for {row.robustness_both}/{row.cases}, {row.proper_time_both}/{row.cases}, and {row.geometry_both}/{row.cases} cases."
        )
    print("- So this section distinguishes two different notions of stability: frontier families that survive both topology and weight nudges, and exact selected winners that are still comparatively fragile.")
    print()

    print("29) Cross-weight perturbation drift cases")
    print(render_perturbation_weight_case_table(weight_drift_rows, limit=min(16, len(weight_drift_rows))))
    print()
    print("Interpretation:")
    if weight_drift_rows:
        selector_weight_drift = [row for row in weight_drift_rows if not row.same_selected]
        overlap_weight_drift = [row for row in weight_drift_rows if not row.robustness_both or not row.base_alive_both]
        print(
            f"- There are {len(weight_drift_rows)} perturbed cases where the story changes across w = {weight_drift_rows[0].low_weight:.2f} -> {weight_drift_rows[0].high_weight:.2f}."
        )
        if selector_weight_drift:
            print(
                f"- In {len(selector_weight_drift)} of them, the selected perturbed motif changes across the two retained weights, which is the cleanest sign that the winner remains more weight-sensitive than the frontier family."
            )
        if overlap_weight_drift:
            print(
                f"- In {len(overlap_weight_drift)} cases, even a stronger selector-free overlap claim drops out across the two weights, so those are the places where the current model still looks weight-fragile rather than merely selector-fragile."
            )
    print("- This is the current frontier of rigor in the toy model: the mixed-frontier family looks substantially more stable than the exact winner, but the winner is still the piece most easily knocked around by both topology and retained-weight changes.")
    print()

    print("30) High-end weight ladder stability of the perturbation ensemble")
    ladder_weights = (0.9, 0.95, 1.0)
    perturbation_weight_ladder_rows, ladder_drift_rows = perturbation_weight_ladder_summary(
        retained_weights=ladder_weights
    )
    print(render_perturbation_weight_ladder_aggregate_table(perturbation_weight_ladder_rows))
    print()
    print("Interpretation:")
    print(
        f"- This pushes the weight-side test one notch farther without opening the whole retained-weight family: it asks which perturbation stories survive across the full high-end ladder w = {ladder_weights[0]:.2f}, {ladder_weights[1]:.2f}, and {ladder_weights[2]:.2f}."
    )
    ladder_all_rows = [row for row in perturbation_weight_ladder_rows if row.variant_name == "all"]
    for row in ladder_all_rows:
        print(
            f"- In `{row.rule_family}`, the perturbed selected rule survives at all three weights in {row.survives_all}/{row.cases} cases, stays exactly the same in {row.same_selected_all}/{row.cases}, and keeps mixed-frontier overlap across the whole ladder in {row.mixed_all}/{row.cases}."
        )
        print(
            f"- The tighter selector-free overlaps persist across all three weights in robustness/proper-time/geometry for {row.robustness_all}/{row.cases}, {row.proper_time_all}/{row.cases}, and {row.geometry_all}/{row.cases} cases."
        )
    print("- This is the stronger local weight-robustness question: not just whether the model survives one nearby shift, but whether the same selector-free story holds across a small high-end band around the spent-delay point.")
    print()

    print("31) High-end weight ladder drift cases")
    print(
        render_perturbation_weight_ladder_case_table(
            ladder_drift_rows,
            limit=min(16, len(ladder_drift_rows)),
        )
    )
    print()
    print("Interpretation:")
    if ladder_drift_rows:
        ladder_selector_drift = [row for row in ladder_drift_rows if not row.same_selected_all]
        ladder_overlap_drift = [
            row
            for row in ladder_drift_rows
            if not row.robustness_all or not row.base_alive_all
        ]
        print(
            f"- There are {len(ladder_drift_rows)} perturbed cases where the story fails to stay intact across the full three-weight ladder."
        )
        if ladder_selector_drift:
            print(
                f"- In {len(ladder_selector_drift)} of them, the selected perturbed motif changes somewhere along the ladder, which is the clearest sign that exact winners are still more weight-sensitive than the frontier family."
            )
        if ladder_overlap_drift:
            print(
                f"- In {len(ladder_overlap_drift)} cases, even a stronger overlap claim drops out at some point on the ladder, so those are the places where the selector-free story is still locally weight-fragile."
            )
    print("- This gives us a better discriminator than the old pairwise check: if the mixed-frontier story remains strong here too, it is much harder to dismiss as a two-point artifact.")
    print()

    print("32) Slightly wider random perturbation ensemble")
    random_variant_limit = 3
    random_aggregate_rows, random_drift_rows = random_perturbation_frontier_summary(
        variant_limit=random_variant_limit
    )
    print(render_perturbation_aggregate_table(random_aggregate_rows))
    print()
    print("Interpretation:")
    print(
        f"- This widens the perturbation test in the other direction: instead of only using hand-picked center and upper nudges, it samples {random_variant_limit} deterministic-random perturbation variants per scenario from the same removable/addable node sets for each benchmark graph."
    )
    random_all_rows = [row for row in random_aggregate_rows if row.variant_name == "all"]
    for row in random_all_rows:
        print(
            f"- In `{row.rule_family}`, the random perturbations still `survive` in {row.survives}/{row.cases} cases, keep the unperturbed selected motif frontier-alive in {row.base_selected_alive}/{row.cases}, and preserve mixed-frontier overlap in {row.mixed_overlap}/{row.cases}."
        )
        print(
            f"- The exact selected winner is retained in {row.selected_retained}/{row.cases} random perturbation cases, while robustness overlap survives in {row.robustness_overlap}/{row.cases}."
        )
    print("- So this is the direct check we wanted: if the same mixed-frontier robust, exact-winner fragile split survives random nudges as well, it is much less likely to be an artifact of the hand-picked perturbation shapes.")
    print()

    print("33) Random perturbation drift cases")
    print(render_perturbation_case_table(random_drift_rows, limit=min(16, len(random_drift_rows))))
    print()
    print("Interpretation:")
    if random_drift_rows:
        random_selected_drift = [row for row in random_drift_rows if not row.selected_matches_base]
        random_overlap_drift = [row for row in random_drift_rows if not row.robustness_overlap or not row.base_selected_alive]
        print(
            f"- There are {len(random_drift_rows)} random perturbation cases where either the selected motif changes or a stronger baseline-overlap claim drops out."
        )
        if random_selected_drift:
            print(
                f"- In {len(random_selected_drift)} of them, the exact winner changes under random nudges, which is the cleanest continuation of the earlier selector-fragility story."
            )
        if random_overlap_drift:
            print(
                f"- In {len(random_overlap_drift)} random cases, a stronger overlap claim also breaks, which marks the places where even the selector-free story is not yet fully perturbation-robust."
            )
    print("- This is now a stronger statement than before: we are no longer only showing that the split survives curated perturbations; we are checking that it still appears under seeded random graph nudges.")
    print()

    print("34) Random perturbation ensemble with limited motif rediscovery")
    rediscovery_limit = 2
    rediscovery_aggregate_rows, rediscovery_drift_rows = (
        random_rediscovery_perturbation_frontier_summary(
            variant_limit=random_variant_limit,
            rediscovery_limit=rediscovery_limit,
        )
    )
    print(render_perturbation_aggregate_table(rediscovery_aggregate_rows))
    print()
    print("Interpretation:")
    print(
        f"- This removes one more cheat from the random ensemble: instead of forcing every perturbed graph to stay inside the unperturbed frontier palette, it lets up to {rediscovery_limit} extra locally rediscovered motifs back into the candidate pool."
    )
    rediscovery_all_rows = [
        row for row in rediscovery_aggregate_rows if row.variant_name == "all"
    ]
    for tracked_row in random_all_rows:
        rediscovery_row = next(
            row
            for row in rediscovery_all_rows
            if row.rule_family == tracked_row.rule_family
        )
        print(
            f"- In `{tracked_row.rule_family}`, mixed-frontier overlap moves from {tracked_row.mixed_overlap}/{tracked_row.cases} under tracked palette to {rediscovery_row.mixed_overlap}/{rediscovery_row.cases} under limited rediscovery, while selected-rule retention moves from {tracked_row.selected_retained}/{tracked_row.cases} to {rediscovery_row.selected_retained}/{rediscovery_row.cases}."
        )
        print(
            f"- Robustness overlap moves from {tracked_row.robustness_overlap}/{tracked_row.cases} to {rediscovery_row.robustness_overlap}/{rediscovery_row.cases}, and baseline selected-motif frontier survival moves from {tracked_row.base_selected_alive}/{tracked_row.cases} to {rediscovery_row.base_selected_alive}/{rediscovery_row.cases}."
        )
    print("- This is the cleaner robustness question: which selector-free conclusions survive once perturbed graphs are allowed a little local novelty instead of being forced to reuse the base palette.")
    print()

    print("35) Limited-rediscovery random drift cases")
    print(
        render_perturbation_case_table(
            rediscovery_drift_rows,
            limit=min(16, len(rediscovery_drift_rows)),
        )
    )
    print()
    print("Interpretation:")
    if rediscovery_drift_rows:
        rediscovery_selected_drift = [
            row for row in rediscovery_drift_rows if not row.selected_matches_base
        ]
        rediscovery_overlap_drift = [
            row
            for row in rediscovery_drift_rows
            if not row.robustness_overlap or not row.base_selected_alive
        ]
        print(
            f"- There are {len(rediscovery_drift_rows)} limited-rediscovery random cases where either the selected motif changes or a stronger baseline-overlap claim drops out."
        )
        if rediscovery_selected_drift:
            print(
                f"- In {len(rediscovery_selected_drift)} of them, the exact winner changes even after allowing local rediscovery, so selector fragility clearly survives that relaxation."
            )
        if rediscovery_overlap_drift:
            print(
                f"- In {len(rediscovery_overlap_drift)} cases, stronger overlap claims still break, which tells us the remaining fragility is not only a palette-inheritance artifact."
            )
    print("- If the mixed-frontier story stays strong here, that is much better evidence that it reflects something structural in the toy model rather than just inherited motif bookkeeping.")
    print()

    print("36) Rediscovery-limit sweep on the random perturbation ensemble")
    rediscovery_limit_rows = random_rediscovery_limit_sweep_summary(
        variant_limit=random_variant_limit,
        rediscovery_limits=(0, 1, 2, 3),
    )
    print(render_rediscovery_limit_aggregate_table(rediscovery_limit_rows))
    print()
    print("Interpretation:")
    for rule_family in ("compact", "extended"):
        family_rows = [
            row for row in rediscovery_limit_rows if row.rule_family == rule_family
        ]
        family_rows.sort(key=lambda row: row.rediscovery_limit)
        if not family_rows:
            continue
        first_row = family_rows[0]
        last_row = family_rows[-1]
        print(
            f"- In `{rule_family}`, moving from rediscovery limit {first_row.rediscovery_limit} to {last_row.rediscovery_limit} changes survives from {first_row.survives}/{first_row.cases} to {last_row.survives}/{last_row.cases}, mixed-overlap from {first_row.mixed_overlap}/{first_row.cases} to {last_row.mixed_overlap}/{last_row.cases}, and robustness-overlap from {first_row.robustness_overlap}/{first_row.cases} to {last_row.robustness_overlap}/{last_row.cases}."
        )
    print("- This is the cleanest cheat-removal readout on the random side so far: if the mixed frontier saturates while the stronger overlap claims erode, that means the selector-free family is more structural than the exact inherited frontier identity, but not completely independent of palette restrictions.")
    print()

    print("37) Geometry-randomized benchmark ensemble")
    geometry_variant_limit = 2
    geometry_rediscovery_limit = 1
    geometry_aggregate_rows, geometry_drift_rows = geometry_randomization_frontier_summary(
        variant_limit=geometry_variant_limit,
        rediscovery_limit=geometry_rediscovery_limit,
    )
    print(render_perturbation_aggregate_table(geometry_aggregate_rows))
    print()
    print("Interpretation:")
    print(
        f"- This attacks the hand-authored graph-family cheat more directly: instead of only punching or shifting nodes inside the benchmark packs, it jitters the whole column profile of each graph into {geometry_variant_limit} deterministic whole-shape variants and then allows the minimal rediscovery limit {geometry_rediscovery_limit} that already repaired random fragility."
    )
    geometry_all_rows = [
        row for row in geometry_aggregate_rows if row.variant_name == "all"
    ]
    for row in geometry_all_rows:
        print(
            f"- In `{row.rule_family}`, the geometry-randomized cases still `survive` in {row.survives}/{row.cases}, keep mixed-frontier overlap in {row.mixed_overlap}/{row.cases}, and keep robustness overlap in {row.robustness_overlap}/{row.cases}."
        )
        print(
            f"- The unperturbed selected motif stays frontier-alive in {row.base_selected_alive}/{row.cases}, while the exact selected winner is retained in only {row.selected_retained}/{row.cases} cases."
        )
    print("- If this section holds up, it is stronger than the earlier node-perturbation story: it says the mixed-frontier result is surviving not just local edits to fixed graphs, but small coherent deformations of the graph family itself.")
    print()

    print("38) Geometry-randomized drift cases")
    print(
        render_perturbation_case_table(
            geometry_drift_rows,
            limit=min(16, len(geometry_drift_rows)),
        )
    )
    print()
    print("Interpretation:")
    if geometry_drift_rows:
        geometry_selected_drift = [
            row for row in geometry_drift_rows if not row.selected_matches_base
        ]
        geometry_overlap_drift = [
            row
            for row in geometry_drift_rows
            if not row.robustness_overlap or not row.base_selected_alive
        ]
        print(
            f"- There are {len(geometry_drift_rows)} geometry-randomized cases where either the selected motif changes or a stronger overlap claim drops out."
        )
        if geometry_selected_drift:
            print(
                f"- In {len(geometry_selected_drift)} of them, the exact winner changes under whole-shape jitter, which keeps reinforcing that exact-winner identity is much more fragile than the selector-free mixed frontier."
            )
        if geometry_overlap_drift:
            print(
                f"- In {len(geometry_overlap_drift)} of them, stronger overlap claims also break, which tells us whole-family geometry is still a real source of fragility even after minimal rediscovery."
            )
    print("- This is the new pressure point on the graph-family cheat: if the mixed frontier stays strong here too, then a lot of the current result is surviving beyond the specific hand-authored pack shapes.")
    print()

    print("39) Procedural graph-generator ensemble")
    procedural_variant_limit = 2
    procedural_rediscovery_limit = 1
    procedural_aggregate_rows, procedural_drift_rows = procedural_geometry_frontier_summary(
        variant_limit=procedural_variant_limit,
        rediscovery_limit=procedural_rediscovery_limit,
    )
    print(render_perturbation_aggregate_table(procedural_aggregate_rows))
    print()
    print("Interpretation:")
    print(
        f"- This goes one step farther than whole-shape jitter: instead of deforming the existing contour, it regenerates the graph column profile from scratch inside the same bounding box using a seeded smooth contour rule, again with the minimal rediscovery limit {procedural_rediscovery_limit}."
    )
    procedural_all_rows = [
        row for row in procedural_aggregate_rows if row.variant_name == "all"
    ]
    for row in procedural_all_rows:
        print(
            f"- In `{row.rule_family}`, the procedural cases still `survive` in {row.survives}/{row.cases}, keep mixed-frontier overlap in {row.mixed_overlap}/{row.cases}, and keep robustness overlap in {row.robustness_overlap}/{row.cases}."
        )
        print(
            f"- The unperturbed selected motif stays frontier-alive in {row.base_selected_alive}/{row.cases}, while the exact selected winner is retained in only {row.selected_retained}/{row.cases} cases."
        )
    print("- This is the cleanest attack yet on the hand-authored graph-family cheat: if the mixed frontier still stays strong here, it is surviving not just perturbations of the benchmark family, but a small independent graph generator living in the same bounding boxes.")
    print()

    print("40) Procedural graph-generator drift cases")
    print(
        render_perturbation_case_table(
            procedural_drift_rows,
            limit=min(16, len(procedural_drift_rows)),
        )
    )
    print()
    print("Interpretation:")
    if procedural_drift_rows:
        procedural_selected_drift = [
            row for row in procedural_drift_rows if not row.selected_matches_base
        ]
        procedural_overlap_drift = [
            row
            for row in procedural_drift_rows
            if not row.robustness_overlap or not row.base_selected_alive
        ]
        print(
            f"- There are {len(procedural_drift_rows)} procedural cases where either the selected motif changes or a stronger overlap claim drops out."
        )
        if procedural_selected_drift:
            print(
                f"- In {len(procedural_selected_drift)} of them, the exact winner changes under independently generated geometry, which is another reminder that selected-winner identity is the most fragile layer of the current story."
            )
        if procedural_overlap_drift:
            print(
                f"- In {len(procedural_overlap_drift)} of them, stronger overlap claims also break, which is where the graph-family cheat is still showing through most clearly."
            )
    print("- If the mixed frontier survives this too, then we are getting close to the limit of what the current benchmark machinery can tell us without moving to a broader graph-generator study.")
    print()

    print("41) Focused diagnostic on the compact procedural miss")
    procedural_failure_rows = procedural_compact_failure_diagnostics(
        variant_limit=procedural_variant_limit,
        rediscovery_limit=procedural_rediscovery_limit,
    )
    print(render_procedural_failure_diagnostic_table(procedural_failure_rows))
    print()
    print("Interpretation:")
    if procedural_failure_rows:
        failed_rows = [
            row for row in procedural_failure_rows if row.status != "survives"
        ]
        if failed_rows:
            failed_row = failed_rows[0]
            comparison_row = next(
                (
                    row
                    for row in procedural_failure_rows
                    if row.scenario_name == failed_row.scenario_name
                    and row.status == "survives"
                ),
                None,
            )
            print(
                f"- The lone compact procedural survive miss is `{failed_row.scenario_name}:{failed_row.variant_name}`. It still keeps mixed-frontier overlap, but it drops from `survives` to `{failed_row.status}` because its arrival span falls to {failed_row.arrival_span:.3f} even though its center gap stays high at {failed_row.center_gap:.3f}."
            )
            if comparison_row is not None:
                print(
                    f"- Compared with the nearby surviving sibling `{comparison_row.variant_name}`, the miss has much larger centerline swing ({failed_row.center_range:.2f} vs {comparison_row.center_range:.2f}) and total centerline variation ({failed_row.center_total_variation:.2f} vs {comparison_row.center_total_variation:.2f})."
                )
            if failed_row.crosses_midline:
                print(
                    "- So the current evidence points to one specific sensitivity: a cross-midline, high-variation centerline can preserve local focusing while flattening far-boundary delay distortion enough to miss the current `survives` threshold."
                )
    print("- That is a useful narrowing of the remaining cheat: the model does not look generically fragile here; it looks specifically sensitive to shapes that keep local geodesic focusing but stop imprinting a strong boundary-delay signature.")
    print()

    print("42) Contour-sensitivity sweep for the compact taper-hard miss")
    contour_rows = contour_sensitivity_sweep(
        rediscovery_limit=procedural_rediscovery_limit,
    )
    print(render_contour_sensitivity_table(contour_rows))
    print()
    print("Interpretation:")
    survive_rows = [row for row in contour_rows if row.status == "survives"]
    mixed_rows = [row for row in contour_rows if row.status == "mixed"]
    if survive_rows and mixed_rows:
        last_survive = survive_rows[-1]
        first_mixed = mixed_rows[0]
        print(
            f"- Holding the span profile fixed and increasing only the centerline deformation keeps mixed-frontier overlap intact throughout the sweep, but the `survives -> mixed` transition happens once arrival span falls below the current `0.5` cutoff: {last_survive.arrival_span:.3f} at alpha={last_survive.alpha:.2f} versus {first_mixed.arrival_span:.3f} at alpha={first_mixed.alpha:.2f}."
        )
        print(
            f"- Over the same transition, center gap does not collapse ({last_survive.center_gap:.3f} -> {first_mixed.center_gap:.3f}); what grows sharply is centerline swing ({last_survive.center_total_variation:.2f} -> {first_mixed.center_total_variation:.2f})."
        )
        if first_mixed.crosses_midline:
            print(
                "- That directly supports the current hypothesis: stronger cross-midline centerline variation can preserve local focusing while washing out the far-boundary delay signature that the present robustness threshold still needs."
            )
    print("- This is the strongest mechanism test we have on that miss so far because it varies one geometric ingredient while holding the span profile nearly fixed.")
    print()

    print("43) Benchmark of alternative focusing observables")
    focus_benchmark_rows = focus_observable_benchmark(
        geometry_variant_limit=geometry_variant_limit,
        geometry_rediscovery_limit=geometry_rediscovery_limit,
        procedural_variant_limit=procedural_variant_limit,
        procedural_rediscovery_limit=procedural_rediscovery_limit,
    )
    print(render_focus_observable_benchmark_table(focus_benchmark_rows))
    print()
    print("Interpretation:")
    best_observable = focus_benchmark_rows[0]
    print(
        f"- This compares the current axis-aligned threshold (`box-min`) against smooth combined observables on the core robustness sweep, the geometry-randomized ensemble, the procedural generator, and the contour miss."
    )
    print(
        f"- In this run, `{best_observable.observable}` is the strongest tested smoother by the current benchmark ordering: it preserves {best_observable.core_preserved}/{best_observable.core_cases} core survives, {best_observable.geometry_preserved}/{best_observable.geometry_survive_cases} geometry-randomized survives, and {best_observable.procedural_preserved}/{best_observable.procedural_survive_cases} procedural survives while classifying the contour miss as `{best_observable.contour_miss_status}`."
    )
    box_row = next(row for row in focus_benchmark_rows if row.observable == "box-min")
    harmonic_row = next(row for row in focus_benchmark_rows if row.observable == "harmonic")
    print(
        f"- The key question is whether a smoother observable can rescue the contour miss without promoting obviously weak cases too aggressively. `box-min` leaves the contour miss at `{box_row.contour_miss_status}`, while `harmonic` changes it to `{harmonic_row.contour_miss_status}` with score {harmonic_row.contour_miss_score:.2f}."
    )
    print("- That gives us a direct threshold-cheat diagnostic: we can now argue from measured tradeoffs rather than from one hand-picked miss.")
    print()

    print("44) Harmonic-status ablation through the frontier machinery")
    harmonic_ablation_rows, harmonic_change_rows, harmonic_frontier_rows, harmonic_frontier_candidates = frontier_observable_ablation(
        frontier_scenario_rows,
        frontier_candidates,
        observable="harmonic",
    )
    print(render_frontier_observable_ablation_table(harmonic_ablation_rows))
    print()
    interesting_harmonic_changes = [
        row
        for row in harmonic_change_rows
        if row.baseline_selected_rule != row.observable_selected_rule
        or row.baseline_selected_status != row.observable_selected_status
        or row.baseline_on_mixed != row.observable_on_mixed
        or row.baseline_on_robustness != row.observable_on_robustness
    ]
    print(
        render_frontier_observable_change_table(
            interesting_harmonic_changes,
            limit=min(12, len(interesting_harmonic_changes)),
        )
    )
    print()
    print("Interpretation:")
    total_harmonic_cases = len(harmonic_frontier_rows)
    total_harmonic_candidates = len(harmonic_frontier_candidates)
    harmonic_selected_changes = sum(row.selected_changes for row in harmonic_ablation_rows)
    harmonic_selected_survives = sum(row.selected_survives for row in harmonic_ablation_rows)
    harmonic_base_survives = sum(row.baseline_selected_survives for row in harmonic_ablation_rows)
    print(
        f"- This is a diagnostic-only pass: it keeps the same evaluated frontier candidates ({total_harmonic_candidates} across {total_harmonic_cases} benchmark cases) and only relabels their `status/status_rank` under the `harmonic` focusing observable before rerunning selection and Pareto membership."
    )
    print(
        f"- Under that relabeling, the selected rule changes in {harmonic_selected_changes}/{total_harmonic_cases} cases. The harmonic-selected rule `survives` in {harmonic_selected_survives}/{total_harmonic_cases} cases, while the baseline-selected rule still `survives` under harmonic in {harmonic_base_survives}/{total_harmonic_cases}."
    )
    compact_harmonic = next(
        (row for row in harmonic_ablation_rows if row.rule_family == "compact"),
        None,
    )
    extended_harmonic = next(
        (row for row in harmonic_ablation_rows if row.rule_family == "extended"),
        None,
    )
    if compact_harmonic is not None and extended_harmonic is not None:
        print(
            f"- In `compact`, the harmonic-selected rule lies on the mixed frontier in {compact_harmonic.selected_on_mixed}/{compact_harmonic.cases} cases and keeps the baseline-selected motif on that same frontier in {compact_harmonic.baseline_on_mixed}/{compact_harmonic.cases}. In `extended`, those counts are {extended_harmonic.selected_on_mixed}/{extended_harmonic.cases} and {extended_harmonic.baseline_on_mixed}/{extended_harmonic.cases}."
        )
    if interesting_harmonic_changes:
        first_change = interesting_harmonic_changes[0]
        print(
            f"- The first changed case here is `{first_change.pack_name}:{first_change.scenario_name}` at w = {first_change.retained_weight:.2f}, where the baseline-selected `{first_change.baseline_selected_rule}` is reinterpreted under harmonic as `{first_change.baseline_selected_status}` and the harmonic rerank picks `{first_change.observable_selected_rule}`."
        )
    print(
        "- So this does not replace the baseline selector yet. It tells us how much of the current frontier story depends on the sharp box-min status rule, and how much survives once the threshold is smoothed while the rest of the machinery is held fixed."
    )
    print()

    print("45) Continuous-score ablation inside the harmonic frontier pass")
    harmonic_continuous_rows, harmonic_continuous_changes, harmonic_continuous_frontier_rows, harmonic_continuous_frontier_candidates = frontier_observable_ablation(
        harmonic_frontier_rows,
        harmonic_frontier_candidates,
        observable="harmonic",
        ranking_mode="continuous",
    )
    print(render_frontier_observable_ablation_table(harmonic_continuous_rows))
    print()
    interesting_continuous_changes = [
        row
        for row in harmonic_continuous_changes
        if row.baseline_selected_rule != row.observable_selected_rule
        or row.baseline_on_robustness != row.observable_on_robustness
        or row.baseline_on_proper_time != row.observable_on_proper_time
        or row.baseline_on_geometry != row.observable_on_geometry
        or row.baseline_on_mixed != row.observable_on_mixed
    ]
    print(
        render_frontier_observable_change_table(
            interesting_continuous_changes,
            limit=min(12, len(interesting_continuous_changes)),
        )
    )
    print()
    print("Interpretation:")
    total_continuous_cases = len(harmonic_continuous_frontier_rows)
    total_continuous_candidates = len(harmonic_continuous_frontier_candidates)
    continuous_selected_changes = sum(row.selected_changes for row in harmonic_continuous_rows)
    continuous_selected_survives = sum(row.selected_survives for row in harmonic_continuous_rows)
    continuous_bucketed_survives = sum(row.baseline_selected_survives for row in harmonic_continuous_rows)
    print(
        f"- This is the bucketization test proper: it keeps the same harmonic-relabeled candidate pool ({total_continuous_candidates} candidates across {total_continuous_cases} cases) and replaces the discrete `status_rank` gate with the continuous harmonic focus score as the leading selector/frontier axis."
    )
    print(
        f"- Relative to the bucketed harmonic pass, the selected rule changes in {continuous_selected_changes}/{total_continuous_cases} cases. The continuously ranked harmonic-selected rule still `survives` in {continuous_selected_survives}/{total_continuous_cases} cases, while the bucketed harmonic-selected rule still `survives` in {continuous_bucketed_survives}/{total_continuous_cases}."
    )
    compact_continuous = next(
        (row for row in harmonic_continuous_rows if row.rule_family == "compact"),
        None,
    )
    extended_continuous = next(
        (row for row in harmonic_continuous_rows if row.rule_family == "extended"),
        None,
    )
    if compact_continuous is not None and extended_continuous is not None:
        print(
            f"- In both families, the continuously ranked harmonic selector now lies on all four frontier views in every scanned case: `compact` {compact_continuous.selected_on_robustness}/{compact_continuous.cases}, {compact_continuous.selected_on_proper_time}/{compact_continuous.cases}, {compact_continuous.selected_on_geometry}/{compact_continuous.cases}, {compact_continuous.selected_on_mixed}/{compact_continuous.cases}; `extended` {extended_continuous.selected_on_robustness}/{extended_continuous.cases}, {extended_continuous.selected_on_proper_time}/{extended_continuous.cases}, {extended_continuous.selected_on_geometry}/{extended_continuous.cases}, {extended_continuous.selected_on_mixed}/{extended_continuous.cases}."
        )
        print(
            f"- By contrast, the bucketed harmonic winner remains on the continuous proper-time/geometry frontiers in only {compact_continuous.baseline_on_proper_time}/{compact_continuous.cases} and {compact_continuous.baseline_on_geometry}/{compact_continuous.cases} compact cases, and {extended_continuous.baseline_on_proper_time}/{extended_continuous.cases} and {extended_continuous.baseline_on_geometry}/{extended_continuous.cases} extended cases."
        )
    if interesting_continuous_changes:
        first_change = interesting_continuous_changes[0]
        print(
            f"- The first changed case here is `{first_change.pack_name}:{first_change.scenario_name}` at w = {first_change.retained_weight:.2f}, where the bucketed harmonic winner `{first_change.baseline_selected_rule}` gives way to `{first_change.observable_selected_rule}` once the harmonic score is treated continuously instead of in `survives/mixed/fragile` buckets."
        )
    print(
        "- So the bucketization is not just cosmetic. It is carrying most of the frontier disagreement: once the harmonic score is used continuously, the winner changes only moderately, but the selected motif becomes nondominated on every frontier in every scanned case."
    )
    print()

    print("46) Derived-axis frontier analysis on the harmonic-continuous candidate pool")
    derived_loading_rows, derived_scenario_rows, derived_aggregate_rows = derived_axis_frontier_analysis(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(render_derived_axis_loading_table(derived_loading_rows))
    print()
    interesting_derived_rows = [
        row
        for row in derived_scenario_rows
        if len({row.pc1_rules, row.pc12_rules, row.pc123_rules}) > 1
        or not (row.selected_on_pc1 and row.selected_on_pc12 and row.selected_on_pc123)
    ]
    print(
        render_derived_axis_scenario_table(
            interesting_derived_rows,
            limit=min(12, len(interesting_derived_rows)),
        )
    )
    print()
    print(render_derived_axis_aggregate_table(derived_aggregate_rows[:12]))
    print()
    print("Interpretation:")
    total_derived_cases = len(derived_scenario_rows)
    print(
        f"- This pass removes the hand-named frontier vocabulary itself. It derives a compact basis from covariance across `center_gap`, `arrival_span`, `min_margin`, `geometric_focus_gap`, and the harmonic focus score on the harmonic-continuous candidate pool."
    )
    print(
        f"- Across {total_derived_cases} harmonic-continuous cases, the selected rule lies on the derived pc1 / pc12 / pc123 frontiers in "
        f"{sum(row.selected_on_pc1 for row in derived_scenario_rows)}/{total_derived_cases}, "
        f"{sum(row.selected_on_pc12 for row in derived_scenario_rows)}/{total_derived_cases}, and "
        f"{sum(row.selected_on_pc123 for row in derived_scenario_rows)}/{total_derived_cases} cases."
    )
    if derived_loading_rows:
        first_loading = derived_loading_rows[0]
        print(
            f"- The leading derived axis `{first_loading.component}` loads most strongly on arrival/focus-style structure ({first_loading.arrival_span:.3f}, {first_loading.focus_score:.3f}) with center-gap contribution {first_loading.center_gap:.3f}."
        )
    compact_derived = next(
        (row for row in derived_aggregate_rows if row.rule_family == "compact"),
        None,
    )
    extended_derived = next(
        (row for row in derived_aggregate_rows if row.rule_family == "extended"),
        None,
    )
    if compact_derived is not None:
        print(
            f"- In `compact`, the most persistent derived-axis motif in this run is `{compact_derived.rule_signature}`, appearing on the pc123 frontier in {compact_derived.pc123_hits} cases while being selected in {compact_derived.selected_hits}."
        )
    if extended_derived is not None:
        print(
            f"- In `extended`, the most persistent derived-axis motif in this run is `{extended_derived.rule_signature}`, appearing on the pc123 frontier in {extended_derived.pc123_hits} cases while being selected in {extended_derived.selected_hits}."
        )
    print(
        f"- The full derived frontier is much more faithful than the lower-dimensional projections: the selected rule stays on pc123 in {sum(row.selected_on_pc123 for row in derived_scenario_rows)}/{total_derived_cases} cases, but only on pc1 in {sum(row.selected_on_pc1 for row in derived_scenario_rows)}/{total_derived_cases} and on pc12 in {sum(row.selected_on_pc12 for row in derived_scenario_rows)}/{total_derived_cases}."
    )
    if interesting_derived_rows:
        print(
            f"- {len(interesting_derived_rows)}/{total_derived_cases} cases still show disagreement between pc1 / pc12 / pc123 or lose the selected rule from one of those projections, so the covariance-derived basis does not simply collapse the story to one low-dimensional frontier."
        )
    print(
        "- So this is the cleanest current test of selector-invariant structure without our hand-picked view vocabulary. The result is mixed but informative: the same core motif family still dominates the full derived frontier, but much of the apparent low-dimensional agreement disappears once we stop naming the views ourselves."
    )
    print()

    print("47) Metric-basis ablation of the derived frontier")
    derived_basis_rows = derived_basis_ablation(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(render_derived_basis_ablation_table(derived_basis_rows))
    print()
    print("Interpretation:")
    full_basis_row = next(row for row in derived_basis_rows if row.basis_name == "full5")
    print(
        f"- This asks whether the derived-axis result is specific to our current five-metric basis or whether it survives smaller alternative bases. The full basis keeps the selected rule on pc123 in {full_basis_row.selected_on_pc123}/{full_basis_row.cases} cases."
    )
    smaller_bases = [row for row in derived_basis_rows if row.basis_name != "full5"]
    strongest_alternative = sorted(
        smaller_bases,
        key=lambda row: (-row.selected_on_pc123, -row.pc123_overlap_with_full, row.dimension, row.basis_name),
    )[0]
    weakest_alternative = sorted(
        smaller_bases,
        key=lambda row: (row.selected_on_pc123, row.pc123_overlap_with_full, row.dimension, row.basis_name),
    )[0]
    print(
        f"- The strongest smaller basis in this run is `{strongest_alternative.basis_name}`, which keeps the selected rule on pc123 in {strongest_alternative.selected_on_pc123}/{strongest_alternative.cases} cases and overlaps the full-basis pc123 frontier in {strongest_alternative.pc123_overlap_with_full}/{strongest_alternative.cases}."
    )
    print(
        f"- The weakest is `{weakest_alternative.basis_name}`, at {weakest_alternative.selected_on_pc123}/{weakest_alternative.cases} selected-on-pc123 and {weakest_alternative.pc123_overlap_with_full}/{weakest_alternative.cases} full-basis overlap."
    )
    if all(row.pc123_overlap_with_full == full_basis_row.cases for row in derived_basis_rows):
        print(
            f"- Every tested basis still shares at least one pc123 motif with the full-basis frontier in all {full_basis_row.cases} cases, so the full derived frontier is not isolated to one metric bundle."
        )
    compact_top_matches = sum(
        row.compact_top_rule == full_basis_row.compact_top_rule
        for row in derived_basis_rows
    )
    extended_top_matches = sum(
        row.extended_top_rule == full_basis_row.extended_top_rule
        for row in derived_basis_rows
    )
    print(
        f"- The top pc123 motif is basis-stable in `compact` for {compact_top_matches}/{len(derived_basis_rows)} tested bases and in `extended` for {extended_top_matches}/{len(derived_basis_rows)}."
    )
    print(
        "- So this is the next cheat-removal result: the full covariance-derived frontier is not uniquely tied to one hand-picked metric bundle, but the detailed motif ranking is still basis-dependent. Some reduced bases preserve the pc123 story completely, while others flip the leading motif family."
    )
    print()

    print("48) Bootstrap stability map over basis ensembles")
    bootstrap_basis_rows, bootstrap_stability_rows = derived_bootstrap_ensemble(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(
        render_derived_bootstrap_basis_table(
            bootstrap_basis_rows,
            limit=min(16, len(bootstrap_basis_rows)),
        )
    )
    print()
    print(render_derived_bootstrap_stability_table(bootstrap_stability_rows[:12]))
    print()
    print("Interpretation:")
    subset_basis_count = sum(row.basis_type == "subset" for row in bootstrap_basis_rows)
    linear_random_basis_count = sum(row.basis_type == "linear-random" for row in bootstrap_basis_rows)
    nonlinear_basis_count = sum(row.basis_type == "nonlinear" for row in bootstrap_basis_rows)
    total_basis_count = len(bootstrap_basis_rows)
    print(
        f"- This is the stability-map version of the basis test: instead of checking a few named bases, it bootstraps {subset_basis_count} subset bases, {linear_random_basis_count} seeded linear-random projection bases, and {nonlinear_basis_count} mild nonlinear bases, for {total_basis_count} total basis views on the same harmonic-continuous candidate pool."
    )
    if bootstrap_basis_rows:
        full_basis_bootstrap = next(row for row in bootstrap_basis_rows if row.basis_name == "full5")
        print(
            f"- The reference full basis keeps the selected rule on pc123 in {full_basis_bootstrap.selected_on_pc123}/{full_basis_bootstrap.cases} cases. We can now compare every other basis against that at scale."
        )
    compact_bootstrap = next((row for row in bootstrap_stability_rows if row.rule_family == "compact"), None)
    extended_bootstrap = next((row for row in bootstrap_stability_rows if row.rule_family == "extended"), None)
    if compact_bootstrap is not None:
        print(
            f"- In `compact`, the most ensemble-stable pc123 motif is `{compact_bootstrap.rule_signature}`, appearing in {compact_bootstrap.basis_hits}/{total_basis_count} bases and {compact_bootstrap.case_basis_hits} basis-case frontiers, with {compact_bootstrap.top_basis_hits} top-basis wins."
        )
    if extended_bootstrap is not None:
        print(
            f"- In `extended`, the most ensemble-stable pc123 motif is `{extended_bootstrap.rule_signature}`, appearing in {extended_bootstrap.basis_hits}/{total_basis_count} bases and {extended_bootstrap.case_basis_hits} basis-case frontiers, with {extended_bootstrap.top_basis_hits} top-basis wins."
        )
    if compact_bootstrap is not None and extended_bootstrap is not None:
        print(
            f"- The same motif family wins both stability maps in this run: `{compact_bootstrap.rule_signature}` / `{extended_bootstrap.rule_signature}`."
        )
    ubiquitous_rules = [
        row
        for row in bootstrap_stability_rows
        if row.basis_hits == total_basis_count
    ]
    if ubiquitous_rules:
        print(
            f"- Basis ubiquity is broader than top-rank dominance here: {len(ubiquitous_rules)} motif-family pairs appear on pc123 in every sampled basis, but `{compact_bootstrap.rule_signature}` still leads because it wins more basis-case frontiers and more top-basis slots."
        )
    if compact_bootstrap is not None and extended_bootstrap is not None:
        print(
            f"- The dominant motif also survives the broadened generator itself: in `compact` it appears in {compact_bootstrap.subset_basis_hits}/{subset_basis_count} subset bases, {compact_bootstrap.linear_random_hits}/{linear_random_basis_count} linear-random bases, and {compact_bootstrap.nonlinear_basis_hits}/{nonlinear_basis_count} nonlinear bases; in `extended`, those counts are {extended_bootstrap.subset_basis_hits}/{subset_basis_count}, {extended_bootstrap.linear_random_hits}/{linear_random_basis_count}, and {extended_bootstrap.nonlinear_basis_hits}/{nonlinear_basis_count}."
        )
    full_overlap_basis_count = sum(
        row.pc123_overlap_with_full == row.cases
        for row in bootstrap_basis_rows
    )
    weakest_bootstrap_basis = min(
        bootstrap_basis_rows,
        key=lambda row: (row.pc123_overlap_with_full, row.selected_on_pc123, row.basis_name),
    )
    print(
        f"- The broadened generator is not perfectly faithful anymore: {full_overlap_basis_count}/{total_basis_count} sampled bases keep full case-by-case pc123 overlap with the full reference, and the weakest current basis is `{weakest_bootstrap_basis.basis_name}` at {weakest_bootstrap_basis.pc123_overlap_with_full}/{weakest_bootstrap_basis.cases} overlap and {weakest_bootstrap_basis.selected_on_pc123}/{weakest_bootstrap_basis.cases} selected-on-pc123."
    )
    print(
        "- This is the strongest current answer to the basis-dependence question: not which motif wins for one chosen basis, or even one basis family, but which motifs keep reappearing on the full derived frontier across subset, linear-random, and nonlinear basis ensembles."
    )
    print()

    print("49) Transform-strength sweep inside the nonlinear basis family")
    transform_break_rows, transform_strength_rows, transform_stability_rows = derived_transform_strength_sweep(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(render_derived_transform_break_table(transform_break_rows))
    print()
    print(
        render_derived_transform_strength_table(
            transform_strength_rows,
            limit=min(15, len(transform_strength_rows)),
        )
    )
    print()
    print(render_derived_transform_stability_table(transform_stability_rows[:12]))
    print()
    print("Interpretation:")
    total_transform_bases = len(transform_strength_rows)
    print(
        f"- This pushes on the last hand-set part of the nonlinear family: not just which transform class is used, but how hard it is applied. The current sweep covers {total_transform_bases} transform views across direct and projected variants."
    )
    earliest_projected_break = min(
        (
            row.projected_transform_break_strength
            for row in transform_break_rows
            if row.projected_transform_break_strength is not None
        ),
        default=None,
    )
    earliest_direct_break = min(
        (
            row.direct_transform_break_strength
            for row in transform_break_rows
            if row.direct_transform_break_strength is not None
        ),
        default=None,
    )
    if earliest_direct_break is None:
        print("- None of the direct transformed bases break their identity-strength baseline anywhere on the current strength grid.")
    else:
        print(
            f"- The earliest direct transform-induced break on the current grid occurs at strength {earliest_direct_break:.2f}."
        )
    if earliest_projected_break is None:
        print("- None of the projected transformed bases degrade beyond their strength-zero projection baselines on the current grid either.")
    else:
        print(
            f"- The earliest projected transform-induced break occurs at strength {earliest_projected_break:.2f}, which tells us the transform/projection combination is what starts to destabilize overlap first once projection alone is factored out."
        )
    weakest_transform_row = min(
        transform_strength_rows,
        key=lambda row: (
            row.pc123_overlap_with_full,
            row.selected_on_pc123,
            row.mode,
            row.strength,
            row.variant_name,
        ),
    )
    print(
        f"- The weakest current transform view is `{weakest_transform_row.basis_name}`, with overlap {weakest_transform_row.pc123_overlap_with_full}/{len(harmonic_continuous_frontier_rows)} and selected-on-pc123 {weakest_transform_row.selected_on_pc123}/{len(harmonic_continuous_frontier_rows)}."
    )
    compact_transform = next((row for row in transform_stability_rows if row.rule_family == "compact"), None)
    extended_transform = next((row for row in transform_stability_rows if row.rule_family == "extended"), None)
    if compact_transform is not None:
        print(
            f"- In `compact`, the most transform-stable motif is `{compact_transform.rule_signature}`, appearing in {compact_transform.basis_hits}/{total_transform_bases} transform views with {compact_transform.top_hits} top-view wins."
        )
    if extended_transform is not None:
        print(
            f"- In `extended`, the most transform-stable motif is `{extended_transform.rule_signature}`, appearing in {extended_transform.basis_hits}/{total_transform_bases} transform views with {extended_transform.top_hits} top-view wins."
        )
    print(
        "- So this turns the nonlinear family into a proper stress test: we can now say not just that some mild transforms work, but where overlap first starts to break and which motifs remain stable across the whole transform-strength sweep."
    )
    print()

    print("50) Projection-bootstrap sweep inside the transformed basis family")
    projection_bootstrap_rows, projection_stability_rows = derived_transform_projection_bootstrap(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(
        render_derived_projection_bootstrap_table(
            projection_bootstrap_rows,
            limit=min(15, len(projection_bootstrap_rows)),
        )
    )
    print()
    print(render_derived_projection_stability_table(projection_stability_rows[:12]))
    print()
    print("Interpretation:")
    total_projection_bases = len(projection_bootstrap_rows) * (
        projection_bootstrap_rows[0].projections if projection_bootstrap_rows else 0
    )
    print(
        f"- This removes the next hand-choice after the transform-strength sweep: instead of only two seeded projected variants per transform, it samples {total_projection_bases} projected bases across mode/strength combinations."
    )
    weakest_projection_row = min(
        projection_bootstrap_rows,
        key=lambda row: (
            row.overlap_min,
            row.selected_min,
            row.mode,
            row.strength,
        ),
    )
    print(
        f"- The weakest projection family on the current grid is `{weakest_projection_row.mode}` at strength {weakest_projection_row.strength:.2f}, with minimum overlap {weakest_projection_row.overlap_min}/{len(harmonic_continuous_frontier_rows)} and minimum selected-on-pc123 {weakest_projection_row.selected_min}/{len(harmonic_continuous_frontier_rows)} across its {weakest_projection_row.projections} projected bases."
    )
    compact_projection = next((row for row in projection_stability_rows if row.rule_family == "compact"), None)
    extended_projection = next((row for row in projection_stability_rows if row.rule_family == "extended"), None)
    if compact_projection is not None:
        print(
            f"- In `compact`, the most projection-stable motif is `{compact_projection.rule_signature}`, appearing in {compact_projection.basis_hits}/{total_projection_bases} projected bases with {compact_projection.top_hits} top-basis wins."
        )
    if extended_projection is not None:
        print(
            f"- In `extended`, the most projection-stable motif is `{extended_projection.rule_signature}`, appearing in {extended_projection.basis_hits}/{total_projection_bases} projected bases with {extended_projection.top_hits} top-basis wins."
        )
    print(
        "- The important twist is that the first strong variation now comes from projection choice itself, not from transform intensity alone. Even so, the same dominant motif still resurfaces across the full broadened projection family."
    )
    print()

    print("51) Projection-generator ablation")
    projection_generator_rows = derived_projection_generator_ablation(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(render_projection_generator_ablation_table(projection_generator_rows))
    print()
    print("Interpretation:")
    best_projection_generator = max(
        projection_generator_rows,
        key=lambda row: (
            row.overlap_min,
            row.selected_min,
            row.overlap_avg,
            row.selected_avg,
            row.generator,
        ),
    )
    weakest_projection_generator = min(
        projection_generator_rows,
        key=lambda row: (
            row.overlap_min,
            row.selected_min,
            row.overlap_avg,
            row.selected_avg,
            row.generator,
        ),
    )
    print(
        f"- This asks whether the new projection sensitivity is structural or mostly an artifact of the current random-projection generator. The strongest generator in the current run is `{best_projection_generator.generator}`, while the weakest is `{weakest_projection_generator.generator}`."
    )
    print(
        f"- `{best_projection_generator.generator}` reaches minimum overlap {best_projection_generator.overlap_min}/{len(harmonic_continuous_frontier_rows)} and minimum selected-on-pc123 {best_projection_generator.selected_min}/{len(harmonic_continuous_frontier_rows)}. `{weakest_projection_generator.generator}` drops to {weakest_projection_generator.overlap_min}/{len(harmonic_continuous_frontier_rows)} and {weakest_projection_generator.selected_min}/{len(harmonic_continuous_frontier_rows)}."
    )
    print(
        f"- The compact dominant motif under the best generator is `{best_projection_generator.compact_dominant_rule}` with {best_projection_generator.compact_dominant_basis_hits}/{best_projection_generator.bases} basis hits; in extended it is `{best_projection_generator.extended_dominant_rule}` with {best_projection_generator.extended_dominant_basis_hits}/{best_projection_generator.bases}."
    )
    print(
        "- If normalization or orthonormalization materially improves the weak cells, then part of the earlier instability was coming from projection scaling rather than from the toy model’s motif structure itself."
    )
    print()

    print("52) Projection-dimension ablation")
    projection_dimension_rows = derived_projection_dimension_ablation(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
    )
    print(render_projection_dimension_ablation_table(projection_dimension_rows))
    print()
    print("Interpretation:")
    best_dimension = max(
        projection_dimension_rows,
        key=lambda row: (
            row.overlap_min,
            row.selected_min,
            row.overlap_avg,
            row.selected_avg,
            row.dimension,
        ),
    )
    weakest_dimension = min(
        projection_dimension_rows,
        key=lambda row: (
            row.overlap_min,
            row.selected_min,
            row.overlap_avg,
            row.selected_avg,
            row.dimension,
        ),
    )
    print(
        f"- This asks whether the current projection instability is mostly about the random generator or about compressing the metric space too aggressively. On the current sweep, the strongest dimension is `{best_dimension.dimension}` and the weakest is `{weakest_dimension.dimension}`."
    )
    print(
        f"- Dimension {best_dimension.dimension} reaches minimum overlap {best_dimension.overlap_min}/{len(harmonic_continuous_frontier_rows)} and minimum selected-on-pc123 {best_dimension.selected_min}/{len(harmonic_continuous_frontier_rows)}. Dimension {weakest_dimension.dimension} falls to {weakest_dimension.overlap_min}/{len(harmonic_continuous_frontier_rows)} and {weakest_dimension.selected_min}/{len(harmonic_continuous_frontier_rows)}."
    )
    print(
        f"- The compact dominant motif at the strongest dimension is `{best_dimension.compact_dominant_rule}` with {best_dimension.compact_dominant_basis_hits}/{best_dimension.bases} basis hits; in extended it is `{best_dimension.extended_dominant_rule}` with {best_dimension.extended_dominant_basis_hits}/{best_dimension.bases}."
    )
    print(
        "- If higher dimensions materially restore overlap, then some of the remaining instability is compression-driven rather than a failure of the underlying motif family."
    )
    print()

    print("53) Selector-free stability map on the 4D orthonormal projection family")
    projection_family_basis_rows, projection_family_stability_rows = derived_projection_family_stability_map(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
        projection_dimension=4,
        generator="orthonormal",
    )
    print(
        render_projection_family_basis_table(
            projection_family_basis_rows,
            limit=min(15, len(projection_family_basis_rows)),
        )
    )
    print()
    print(render_projection_family_stability_table(projection_family_stability_rows[:12]))
    print()
    print("Interpretation:")
    total_projection_family_bases = len(projection_family_basis_rows)
    full_overlap_projection_family = sum(
        row.pc123_overlap_with_full == len(harmonic_continuous_frontier_rows)
        for row in projection_family_basis_rows
    )
    min_selected_projection_family = min(
        row.selected_on_pc123
        for row in projection_family_basis_rows
    )
    max_selected_projection_family = max(
        row.selected_on_pc123
        for row in projection_family_basis_rows
    )
    compact_projection_family = next(
        (row for row in projection_family_stability_rows if row.rule_family == "compact"),
        None,
    )
    extended_projection_family = next(
        (row for row in projection_family_stability_rows if row.rule_family == "extended"),
        None,
    )
    ubiquitous_projection_family = [
        row
        for row in projection_family_stability_rows
        if row.basis_hits == total_projection_family_bases
    ]
    print(
        f"- This reruns the selector-free stability story on the stronger `4D orthonormal` projection family instead of treating `3D` as the default bottleneck. The family contains {total_projection_family_bases} projected bases across mode, strength, and projection variants."
    )
    print(
        f"- The overlap story is now much cleaner: {full_overlap_projection_family}/{total_projection_family_bases} bases keep nonempty `pc123` overlap with the full reference in all {len(harmonic_continuous_frontier_rows)} cases."
    )
    print(
        f"- Selected-rule retention is still not perfectly invariant, but it is much stronger than in the tighter projected families: selected-on-`pc123` ranges from {min_selected_projection_family}/{len(harmonic_continuous_frontier_rows)} to {max_selected_projection_family}/{len(harmonic_continuous_frontier_rows)} across the family."
    )
    if compact_projection_family is not None:
        print(
            f"- In `compact`, the dominant selector-free motif is `{compact_projection_family.rule_signature}`, appearing in {compact_projection_family.basis_hits}/{total_projection_family_bases} bases, {compact_projection_family.case_hits} basis-case frontiers, and {compact_projection_family.top_hits} top-basis wins."
        )
    if extended_projection_family is not None:
        print(
            f"- In `extended`, the dominant selector-free motif is `{extended_projection_family.rule_signature}`, appearing in {extended_projection_family.basis_hits}/{total_projection_family_bases} bases, {extended_projection_family.case_hits} basis-case frontiers, and {extended_projection_family.top_hits} top-basis wins."
        )
    print(
        f"- Ubiquity is broader than a single winner here too: {len(ubiquitous_projection_family)} motif-family pairs appear on `pc123` in all {total_projection_family_bases} bases of the 4D orthonormal family."
    )
    print(
        "- So once the projection bottleneck is relaxed, much more of the selector-free structure survives intact. The remaining disagreement now looks more like motif ranking inside a robust family than like wholesale loss of overlap."
    )
    print()

    print("54) Case-core analysis on the 4D orthonormal family")
    projection_case_core_rows, projection_core_aggregate_rows = derived_projection_family_case_core_analysis(
        harmonic_continuous_frontier_rows,
        harmonic_continuous_frontier_candidates,
        projection_dimension=4,
        generator="orthonormal",
    )
    interesting_projection_core_rows = [
        row
        for row in projection_case_core_rows
        if row.core_count > 1 or not row.selected_in_core or row.core_count != row.union_count
    ]
    print(
        render_projection_family_case_core_table(
            interesting_projection_core_rows,
            limit=min(12, len(interesting_projection_core_rows)),
        )
    )
    print()
    print(render_projection_family_core_aggregate_table(projection_core_aggregate_rows[:12]))
    print()
    print("Interpretation:")
    total_projection_cases = len(projection_case_core_rows)
    nonempty_core_cases = sum(row.core_count > 0 for row in projection_case_core_rows)
    selected_in_core_cases = sum(row.selected_in_core for row in projection_case_core_rows)
    exact_core_cases = sum(row.core_count == row.union_count for row in projection_case_core_rows)
    max_core_size = max((row.core_count for row in projection_case_core_rows), default=0)
    compact_core = next(
        (row for row in projection_core_aggregate_rows if row.rule_family == "compact"),
        None,
    )
    extended_core = next(
        (row for row in projection_core_aggregate_rows if row.rule_family == "extended"),
        None,
    )
    print(
        f"- This is the stricter selector-free question: not which motifs appear in many `4D orthonormal` bases, but which ones survive the intersection across all 60 bases for each case."
    )
    print(
        f"- The case core is nonempty in {nonempty_core_cases}/{total_projection_cases} cases, and the currently selected rule is itself in the case core in {selected_in_core_cases}/{total_projection_cases}."
    )
    print(
        f"- Exact basis-indifference is still rare: only {exact_core_cases}/{total_projection_cases} cases have `core == union`, and the largest current core size is {max_core_size}."
    )
    if compact_core is not None:
        print(
            f"- In `compact`, the strongest unavoidable motif is `{compact_core.rule_signature}`, with {compact_core.core_hits} core hits out of {compact_core.union_hits} union hits and {compact_core.selected_core_hits} cases where it is both selected and unavoidable."
        )
    if extended_core is not None:
        print(
            f"- In `extended`, the strongest unavoidable motif is `{extended_core.rule_signature}`, with {extended_core.core_hits} core hits out of {extended_core.union_hits} union hits and {extended_core.selected_core_hits} cases where it is both selected and unavoidable."
        )
    print(
        "- That tells us the remaining disagreement is not just about whether motifs appear somewhere on the frontier. We can now separate broad family ubiquity from true case-by-case inevitability inside the stronger 4D projection family."
    )
    print()

    print("55) Mechanism map for 4D case-core regimes")
    projection_core_mechanism_rows, projection_core_case_rows = projection_core_mechanism_map(
        projection_case_core_rows,
    )
    interesting_projection_mechanism_rows = [
        row
        for row in projection_core_case_rows
        if row.regime in {"empty", "single-other", "multi-other"}
        or row.center_variation >= 6.0
    ]
    print(render_projection_core_mechanism_table(projection_core_mechanism_rows))
    print()
    print(
        render_projection_core_mechanism_case_table(
            interesting_projection_mechanism_rows,
            limit=min(12, len(interesting_projection_mechanism_rows)),
        )
    )
    print()
    print("Interpretation:")
    empty_regime = next((row for row in projection_core_mechanism_rows if row.regime == "empty"), None)
    single_selected_regime = next((row for row in projection_core_mechanism_rows if row.regime == "single-selected"), None)
    multi_selected_regime = next((row for row in projection_core_mechanism_rows if row.regime == "multi-selected"), None)
    if empty_regime is not None:
        print(
            f"- Empty-core cases cluster in a distinctive part of the current graph family: {empty_regime.cases} cases, including {empty_regime.skew_cases} skew shapes and {empty_regime.crossing_cases} midline-crossing profiles, with average center-variation {empty_regime.avg_center_variation:.2f} and span-range {empty_regime.avg_span_range:.2f}."
        )
    if single_selected_regime is not None:
        print(
            f"- Single-motif cores are the cleanest regime. In the current run there are {single_selected_regime.cases} such cases, dominated by rect+taper shapes ({single_selected_regime.rect_cases + single_selected_regime.taper_cases}/{single_selected_regime.cases}) with lower average center-variation {single_selected_regime.avg_center_variation:.2f}."
        )
    if multi_selected_regime is not None:
        print(
            f"- Multi-motif cores are rare and mostly taper-shaped: {multi_selected_regime.cases} cases, {multi_selected_regime.taper_cases} of them taper, with average center-variation {multi_selected_regime.avg_center_variation:.2f} and crossing count {multi_selected_regime.crossing_cases}/{multi_selected_regime.cases}."
        )
    print(
        "- This turns the case-core result into a real mechanism map: empty cores, single-motif cores, and multi-motif cores now line up with different contour-roughness and topology signatures instead of only looking like abstract counts."
    )
    print()

    print("56) Controlled roughness sweep at fixed span profile")
    roughness_core_rows, roughness_core_aggregate_rows = roughness_core_sweep()
    roughness_transition_rows = [
        row
        for row in roughness_core_rows
        if row.alpha in {0.0, 0.2, 0.6, 1.0}
        and row.retained_weight in {0.75, 1.0}
    ]
    print(render_roughness_core_aggregate_table(roughness_core_aggregate_rows))
    print()
    print(
        render_roughness_core_case_table(
            roughness_transition_rows,
            limit=min(18, len(roughness_transition_rows)),
        )
    )
    print()
    print("Interpretation:")
    compact_alpha0 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "compact" and row.alpha == 0.0)
    compact_alpha02 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "compact" and row.alpha == 0.2)
    compact_alpha06 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "compact" and row.alpha == 0.6)
    compact_alpha1 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "compact" and row.alpha == 1.0)
    extended_alpha0 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "extended" and row.alpha == 0.0)
    extended_alpha02 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "extended" and row.alpha == 0.2)
    extended_alpha06 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "extended" and row.alpha == 0.6)
    extended_alpha1 = next(row for row in roughness_core_aggregate_rows if row.rule_family == "extended" and row.alpha == 1.0)
    print(
        f"- This is the controlled version of the mechanism question: the span profile is held fixed while only the centerline path changes. The key variable is the realized roughness, not alpha by itself."
    )
    print(
        f"- In `compact`, the low-roughness mid-sweep states are the clean ones: alpha {compact_alpha02.alpha:.2f} has center-variation {compact_alpha02.center_variation:.1f}, selected-in-core {compact_alpha02.selected_in_core_cases}/{compact_alpha02.cases}, and zero empty cases, while the rougher states at alpha {compact_alpha0.alpha:.2f}, {compact_alpha06.alpha:.2f}, and {compact_alpha1.alpha:.2f} all return to all-empty cores."
    )
    print(
        f"- In `extended`, the same geometry family shows a richer version of that pattern: alpha {extended_alpha02.alpha:.2f} at center-variation {extended_alpha02.center_variation:.1f} gives {extended_alpha02.multi_selected_cases}/{extended_alpha02.cases} multi-selected cores, alpha {extended_alpha06.alpha:.2f} at variation {extended_alpha06.center_variation:.1f} collapses to {extended_alpha06.empty_cases}/{extended_alpha06.cases} empty cores, and the roughest endpoint alpha {extended_alpha1.alpha:.2f} partially re-enters the single-selected regime ({extended_alpha1.single_selected_cases}/{extended_alpha1.cases})."
    )
    print(
        "- So the transition is continuous in the geometry metrics but not monotone in alpha. What survives the control test is the stronger claim: the case-core regime clearly tracks realized centerline roughness at fixed span profile, even though the response can be family-dependent and re-entrant."
    )
    print()

    print("57) Centerline-mode basis sweep at fixed span profile")
    mode_core_rows, mode_core_aggregate_rows = centerline_mode_core_sweep()
    interesting_mode_rows = [
        row
        for row in mode_core_rows
        if row.amplitude in {0.0, 1.0, 2.0}
        and row.retained_weight in {0.75, 1.0}
        and row.regime != "single-selected"
    ]
    print(render_centerline_mode_aggregate_table(mode_core_aggregate_rows))
    print()
    print(
        render_centerline_mode_case_table(
            interesting_mode_rows,
            limit=min(20, len(interesting_mode_rows)),
        )
    )
    print()
    print("Interpretation:")
    compact_tilt_10 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "compact" and row.mode == "tilt" and row.amplitude == 1.0
    )
    compact_step_15 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "compact" and row.mode == "step" and row.amplitude == 1.5
    )
    compact_zigzag_05 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "compact" and row.mode == "zigzag" and row.amplitude == 0.5
    )
    extended_bowl_15 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "extended" and row.mode == "bowl" and row.amplitude == 1.5
    )
    extended_zigzag_05 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "extended" and row.mode == "zigzag" and row.amplitude == 0.5
    )
    extended_zigzag_15 = next(
        row
        for row in mode_core_aggregate_rows
        if row.rule_family == "extended" and row.mode == "zigzag" and row.amplitude == 1.5
    )
    print(
        "- This removes the last big path-choice cheat in the roughness story. Instead of one interpolation path, the same fixed-span test now probes four independent centerline modes."
    )
    print(
        f"- The broad roughness link survives, but not as a one-number rule. In `compact`, the smoother `tilt` mode stays mostly single-selected through amplitude {compact_tilt_10.amplitude:.1f} ({compact_tilt_10.selected_in_core_cases}/{compact_tilt_10.cases} selected-in-core at center-variation {compact_tilt_10.center_variation:.1f}), and `step` even recovers to {compact_step_15.selected_in_core_cases}/{compact_step_15.cases} selected-in-core at amplitude {compact_step_15.amplitude:.1f}. By contrast, `zigzag` is already fully destructive at amplitude {compact_zigzag_05.amplitude:.1f}, with {compact_zigzag_05.empty_cases}/{compact_zigzag_05.cases} empty cores and center-variation {compact_zigzag_05.center_variation:.1f}."
    )
    print(
        f"- `Extended` shows the same dependence on mode symmetry even more strongly. `Bowl` at amplitude {extended_bowl_15.amplitude:.1f} gives {extended_bowl_15.multi_selected_cases}/{extended_bowl_15.cases} multi-selected cores, while `zigzag` collapses to {extended_zigzag_05.empty_cases}/{extended_zigzag_05.cases} empty cores already at amplitude {extended_zigzag_05.amplitude:.1f}, then re-enters as {extended_zigzag_15.selected_in_core_cases}/{extended_zigzag_15.cases} selected-in-core at amplitude {extended_zigzag_15.amplitude:.1f}."
    )
    print(
        "- So the stronger statement is now: case-core structure depends on realized roughness, but also on the symmetry class of the deformation. The roughness-core link is broader than one interpolation path, yet not reducible to roughness magnitude alone."
    )
    print()

    print("58) Centerline-invariant mechanism test")
    invariant_aggregate_rows, invariant_comparison_rows = centerline_invariant_analysis(
        mode_core_rows,
    )
    informative_comparison_rows = [
        row
        for row in invariant_comparison_rows
        if sum(
            candidate.rule_family == row.rule_family
            and candidate.center_variation == row.center_variation
            for candidate in invariant_comparison_rows
        ) > 1
    ]
    print(
        render_centerline_invariant_aggregate_table(
            invariant_aggregate_rows,
            limit=min(12, len(invariant_aggregate_rows)),
        )
    )
    print()
    print(
        render_centerline_invariant_comparison_table(
            informative_comparison_rows,
            limit=min(16, len(informative_comparison_rows)),
        )
    )
    print()
    print("Interpretation:")
    compact_cvar2 = [
        row
        for row in invariant_comparison_rows
        if row.rule_family == "compact" and row.center_variation == 2.0
    ]
    extended_cvar6 = [
        row
        for row in invariant_comparison_rows
        if row.rule_family == "extended" and row.center_variation == 6.0
    ]
    divergence_groups = 0
    for rule_family in ("compact", "extended"):
        roughness_values = sorted({row.center_variation for row in invariant_comparison_rows if row.rule_family == rule_family})
        for roughness_value in roughness_values:
            rows = [
                row
                for row in invariant_comparison_rows
                if row.rule_family == rule_family and row.center_variation == roughness_value
            ]
            if len(rows) >= 2 and len({row.selected_in_core_cases for row in rows}) >= 2:
                divergence_groups += 1
    print(
        "- This compares a small invariant set against raw roughness directly. The key question is whether similar roughness values still split by invariant class."
    )
    if compact_cvar2:
        print(
            f"- In `compact` at center-variation 2.0, the invariant split is already strong: "
            + "; ".join(
                f"{row.signature}/{('cross' if row.crosses_midline else 'no-cross')} -> {row.selected_in_core_cases}/{row.cases} sel-core"
                for row in compact_cvar2
            )
            + "."
        )
    if extended_cvar6:
        print(
            f"- In `extended` at center-variation 6.0, the same thing happens: "
            + "; ".join(
                f"{row.signature}/{('cross' if row.crosses_midline else 'no-cross')} -> {row.selected_in_core_cases}/{row.cases} sel-core"
                for row in extended_cvar6
            )
            + "."
        )
    print(
        f"- Across the current mode sweep, there are {divergence_groups} roughness groups where identical center-variation still splits into different case-core outcomes by invariant class."
    )
    print(
        "- So the answer is now clearer: monotone vs oscillatory and crossing vs non-crossing do explain the behavior better than roughness magnitude alone, although they still do not collapse everything to a single invariant rule."
    )
    print()

    print("REMAINING CHEATS")
    print("- The spatial graph itself is still hand-authored rather than derived from deeper constraints.")
    print("- The gravity-like classical limit still assumes that histories extremize spent delay dt - sqrt(dt^2 - ds^2) rather than deriving that accounting rule from deeper dynamics.")
    print("- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.")
    print("- The current robustness quality is still hand-chosen too: center gap, arrival span, and selector policy materially affect which surviving branch the model prefers on hard cases.")
    print("- Complex amplitudes are assumed because they match the interference requirement.")
    print("- Consciousness is not modeled here; only durable records and self-insensitive measurement.")


if __name__ == "__main__":
    main()
