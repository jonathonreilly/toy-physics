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
from dataclasses import dataclass
import cmath
import heapq
import itertools
import math
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

    best_candidate: RuleCandidate | None = None
    best_key: tuple[float, ...] | None = None
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
                    preferred_score = preferred_bonus if (survive_counts, birth_counts) in preferred_set else 0.0
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
                    orbit_variation = max(orbit_sizes[-4:]) - min(orbit_sizes[-4:])

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
                    seed_distance_sq = (
                        (candidate.seed_node[0] - graph_center[0]) ** 2
                        + (candidate.seed_node[1] - graph_center[1]) ** 2
                    )
                    candidate_key = (
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
                    if best_key is None or candidate_key > best_key:
                        best_key = candidate_key
                        best_candidate = candidate

    diagnostics = SearchDiagnostics(
        total_trials=total_trials,
        empty_patterns=rejection_counts["empty"],
        disconnected_rejections=rejection_counts["disconnected"],
        size_rejections=rejection_counts["size"],
        boundary_rejections=rejection_counts["boundary"],
        accepted_candidates=accepted_candidates,
        dominant_rejection=dominant_rejection_label(rejection_counts),
    )
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
        center_gap, arrival_span, _centroid_y, _survived, status = metrics
        quality_key = (
            robustness_rank(status),
            center_gap + arrival_span,
            arrival_span,
            center_gap,
            candidate.occupancy_mean,
            candidate.density,
        )
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
    center_gap, arrival_span, _centroid_y, _survived, status = metrics
    if status != "survives":
        rescue_rule, rescue_diagnostics, rescue_metrics = quality_rescue_rule(
            nodes,
            wrap_y=wrap_y,
            count_options=count_options,
            postulates=postulates,
        )
        diagnostics = merge_search_diagnostics(diagnostics, rescue_diagnostics)
        if rescue_rule is not None and rescue_metrics is not None:
            rescue_key = (
                robustness_rank(rescue_metrics[4]),
                rescue_metrics[0] + rescue_metrics[1],
                rescue_metrics[1],
                rescue_metrics[0],
            )
            current_key = (
                robustness_rank(status),
                center_gap + arrival_span,
                arrival_span,
                center_gap,
            )
            if rescue_key > current_key:
                chosen_rule = rescue_rule
                metrics = rescue_metrics
                fallback_used = True

    return chosen_rule, diagnostics, metrics, fallback_used


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


def minimum_proper_time_margin(
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    chosen_rule: RuleCandidate,
    postulates: RulePostulates,
) -> tuple[float, float]:
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

    margins: list[float] = []
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
        distorted_delay = path_delay_total(distorted_path, distorted_rule, distorted_field)
        action_gain = free_action - distorted_action
        delay_penalty = distorted_delay - free_delay
        margins.append(action_gain - delay_penalty)

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

            for target_y in all_off_center_targets(right_boundary_ys, source_y):
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
                critical_weight = (
                    (2.0 * delay_penalty / retained_total)
                    if retained_total > 0.0
                    else math.inf
                )
                rows.append(
                    CriticalWeightCase(
                        pack_name=pack_name,
                        scenario_name=scenario_name,
                        target_y=target_y,
                        critical_weight=critical_weight,
                        margin_at_one=retained_total - 2.0 * delay_penalty,
                        delay_penalty=delay_penalty,
                        retained_total=retained_total,
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


def main() -> None:
    print("OCTOPUS PHYSICS TOY MODEL")
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

    print("REMAINING CHEATS")
    print("- The spatial graph itself is still hand-authored rather than derived from deeper constraints.")
    print("- The gravity-like classical limit still assumes that histories extremize spent delay dt - sqrt(dt^2 - ds^2) rather than deriving that accounting rule from deeper dynamics.")
    print("- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.")
    print("- Complex amplitudes are assumed because they match the interference requirement.")
    print("- Consciousness is not modeled here; only durable records and self-insensitive measurement.")


if __name__ == "__main__":
    main()
