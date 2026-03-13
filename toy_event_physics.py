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
import math
from typing import DefaultDict


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
    persistent_nodes: int
    center_gap: float
    arrival_span: float
    centroid_y: float
    survived: bool
    status: str


@dataclass(frozen=True)
class LocalRule:
    persistent_nodes: frozenset[tuple[int, int]]
    phase_wavenumber: float
    attenuation_power: float = 1.0


@dataclass(frozen=True)
class RulePostulates:
    phase_per_action: float
    attenuation_power: float = 1.0


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

SWEEP_COMPACT_COUNT_OPTIONS = (
    frozenset({1}),
    frozenset({2}),
    frozenset({3}),
    frozenset({1, 2}),
    frozenset({2, 3}),
    frozenset({3, 4}),
)

SWEEP_EXTENDED_COUNT_OPTIONS = SWEEP_COMPACT_COUNT_OPTIONS + (
    frozenset({1, 3}),
    frozenset({1, 2, 3}),
    frozenset({2, 3, 4}),
    frozenset({1, 2, 3, 4}),
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
    )


def proper_time_deficit(delay: float, link_length: float) -> float:
    """Positive action-like cost from local delay and retained proper update."""

    retained_update = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    return delay - retained_update


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


def select_self_maintenance_rule(
    nodes: set[tuple[int, int]],
    count_options: tuple[frozenset[int], ...] = COMPACT_COUNT_OPTIONS,
    wrap_y: bool = False,
    evolution_steps: int = 10,
    sample_window: int = 4,
    occupancy_threshold: float = 0.75,
) -> RuleCandidate:
    """Search over seeds and local rules for a compact localized persistent pattern."""
    best_candidate: RuleCandidate | None = None
    best_key: tuple[float, ...] | None = None
    graph_boundaries = boundary_nodes(nodes, wrap_y=wrap_y)
    interior_nodes = sorted(node for node in nodes if node not in graph_boundaries)
    xs = [x for x, _y in nodes]
    ys = [y for _x, y in nodes]
    graph_center = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)

    for seed_node in interior_nodes:
        seed_nodes = point_seed(seed_node)
        for survive_counts in count_options:
            for birth_counts in count_options:
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
                    continue

                largest_component = max(
                    connected_components(persistent_nodes, nodes, wrap_y=wrap_y),
                    key=len,
                )
                if len(largest_component) != len(persistent_nodes):
                    continue
                if not 4 <= len(largest_component) <= 16:
                    continue

                density = component_density(largest_component)
                boundary_count = boundary_touch_count(largest_component, nodes, wrap_y=wrap_y)
                if boundary_count:
                    continue

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
                    -float(candidate.area),
                    -float(orbit_variation),
                    -float(seed_distance_sq),
                    -float(candidate.seed_node[0]),
                    -float(candidate.seed_node[1]),
                )
                if best_key is None or candidate_key > best_key:
                    best_key = candidate_key
                    best_candidate = candidate

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
    if not any(support.values()):
        return support

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
    action_increment = proper_time_deficit(delay, link_length)

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
    action_cost: dict[tuple[int, int], float] = {source: 0.0}
    previous: dict[tuple[int, int], tuple[int, int]] = {}
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, source)]

    while frontier:
        current_action, node = heapq.heappop(frontier)
        if current_action != action_cost[node]:
            continue
        if node == target:
            break

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

    path = [target]
    current = target
    while current != source:
        current = previous[current]
        path.append(current)
    path.reverse()
    return action_cost[target], path


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


def evaluate_robustness_scenario(
    scenario_name: str,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    count_options: tuple[frozenset[int], ...],
    rule_family: str,
    postulates: RulePostulates,
) -> RobustnessResult:
    min_x = min(x for x, _y in nodes)
    max_x = max(x for x, _y in nodes)
    left_boundary_ys = sorted(y for x, y in nodes if x == min_x)
    right_boundary_ys = sorted(y for x, y in nodes if x == max_x)

    chosen_rule = select_self_maintenance_rule(
        nodes,
        count_options=count_options,
        wrap_y=wrap_y,
        evolution_steps=8,
        sample_window=3,
        occupancy_threshold=2 / 3,
    )
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

    return RobustnessResult(
        scenario_name=scenario_name,
        rule_family=rule_family,
        seed_node=chosen_rule.seed_node,
        persistent_nodes=len(chosen_rule.persistent_nodes),
        center_gap=center_gap,
        arrival_span=arrival_span,
        centroid_y=centroid_y,
        survived=survived,
        status=status,
    )


def run_robustness_sweep(postulates: RulePostulates) -> list[RobustnessResult]:
    scenarios = (
        ("rect-hard", build_rectangular_nodes(6, 4), False),
        ("rect-wrap", build_rectangular_nodes(6, 4), True),
        ("taper-hard", build_tapered_nodes(6, 4), False),
        ("taper-wrap", build_tapered_nodes(6, 4), True),
        ("skew-hard", build_skewed_nodes(6, 4), False),
        ("skew-wrap", build_skewed_nodes(6, 4), True),
    )
    rule_families = (
        ("compact", SWEEP_COMPACT_COUNT_OPTIONS),
        ("extended", SWEEP_EXTENDED_COUNT_OPTIONS),
    )

    results: list[RobustnessResult] = []
    for scenario_name, nodes, wrap_y in scenarios:
        for rule_family, count_options in rule_families:
            try:
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
            except RuntimeError:
                results.append(
                    RobustnessResult(
                        scenario_name=scenario_name,
                        rule_family=rule_family,
                        seed_node=(-1, -1),
                        persistent_nodes=0,
                        center_gap=float("nan"),
                        arrival_span=float("nan"),
                        centroid_y=float("nan"),
                        survived=False,
                        status="no pattern",
                    )
                )
    return results


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


def render_robustness_table(rows: list[RobustnessResult]) -> str:
    lines = [
        "scenario    | family   | seed     | nodes | center gap | arrival span | centroid y | status",
        "------------+----------+----------+-------+------------+--------------+------------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.scenario_name:<11} | "
            f"{row.rule_family:<8} | "
            f"{str(row.seed_node):<8} | "
            f"{row.persistent_nodes:>5} | "
            f"{row.center_gap:>10.3f} | "
            f"{row.arrival_span:>12.3f} | "
            f"{row.centroid_y:>10.3f} | "
            f"{row.status}"
        )
    return "\n".join(lines)


def main() -> None:
    print("ALIEN-EVENT TOY MODEL")
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
    chosen_rule = select_self_maintenance_rule(derived_nodes)
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
    print(render_robustness_table(robustness_rows))
    print()
    survived_count = sum(row.survived for row in robustness_rows)
    mixed_count = sum(row.status == "mixed" for row in robustness_rows)
    no_pattern_count = sum(row.status == "no pattern" for row in robustness_rows)
    family_summaries = []
    for family in sorted({row.rule_family for row in robustness_rows}):
        family_rows = [row for row in robustness_rows if row.rule_family == family]
        family_summaries.append(
            (
                family,
                sum(row.survived for row in family_rows),
                sum(row.status == "mixed" for row in family_rows),
                sum(row.status == "no pattern" for row in family_rows),
            )
        )
    print("Interpretation:")
    print("- Each scenario varies graph shape, vertical boundary treatment, or the searched local rule family while keeping the same ontology.")
    print("- `center gap` measures whether the action-favored path stays focused near the emergent field centroid instead of peeling away immediately.")
    print("- `arrival span` measures how non-uniform the induced boundary delay shifts are across the far edge.")
    print(f"- In this run, {survived_count} scenarios were `survives`, {mixed_count} were `mixed`, and {no_pattern_count} produced no compact persistent pattern under the sweep budget.")
    for family, family_survives, family_mixed, family_no_pattern in family_summaries:
        print(f"- `{family}` family: {family_survives} survives, {family_mixed} mixed, {family_no_pattern} no pattern.")
    print("- This does not prove universality, but it starts separating structural behavior from single-geometry artifacts.")
    print()

    print("REMAINING CHEATS")
    print("- The spatial graph itself is still hand-authored rather than derived from deeper constraints.")
    print("- The gravity-like classical limit still assumes that histories extremize spent delay dt - sqrt(dt^2 - ds^2) rather than deriving that accounting rule from deeper dynamics.")
    print("- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.")
    print("- Complex amplitudes are assumed because they match the interference requirement.")
    print("- Consciousness is not modeled here; only durable records and self-insensitive measurement.")


if __name__ == "__main__":
    main()
