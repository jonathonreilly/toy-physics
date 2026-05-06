#!/usr/bin/env python3
"""Executable certificate for the NN topological causal-bound note.

This runner checks the finite graph dependency-support recurrence used in
docs/LATTICE_NN_LIGHT_CONE_NOTE.md. It intentionally checks only graph
reachability, not a physical spacetime light cone or distance law.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable


Vertex = int
Edge = tuple[Vertex, Vertex]


@dataclass(frozen=True)
class GraphCase:
    name: str
    vertex_count: int
    edges: tuple[Edge, ...]
    horizon: int
    include_self_edges: bool


def dependency_edges(case: GraphCase) -> tuple[Edge, ...]:
    edges = set(case.edges)
    if case.include_self_edges:
        edges.update((v, v) for v in range(case.vertex_count))
    return tuple(sorted(edges))


def predecessors(vertex_count: int, edges: Iterable[Edge]) -> list[set[Vertex]]:
    pred = [set() for _ in range(vertex_count)]
    for u, v in edges:
        pred[v].add(u)
    return pred


def successors(vertex_count: int, edges: Iterable[Edge]) -> list[set[Vertex]]:
    succ = [set() for _ in range(vertex_count)]
    for u, v in edges:
        succ[u].add(v)
    return succ


def dependency_supports(
    vertex_count: int, pred: list[set[Vertex]], horizon: int
) -> list[list[set[Vertex]]]:
    """deps[t][v] is the set of initial vertices that can affect v at tick t."""
    deps = [[{v} for v in range(vertex_count)]]
    for _ in range(horizon):
        previous = deps[-1]
        current = []
        for v in range(vertex_count):
            support = set()
            for u in pred[v]:
                support.update(previous[u])
            current.append(support)
        deps.append(current)
    return deps


def forward_reachability(
    vertex_count: int, succ: list[set[Vertex]], source: Vertex, horizon: int
) -> list[set[Vertex]]:
    reached_by_tick = [{source}]
    frontier = {source}
    reached = {source}
    for _ in range(horizon):
        next_frontier = set()
        for u in frontier:
            next_frontier.update(succ[u])
        reached.update(next_frontier)
        reached_by_tick.append(set(reached))
        frontier = next_frontier
    return reached_by_tick


def check_case(case: GraphCase) -> tuple[int, int]:
    edges = dependency_edges(case)
    pred = predecessors(case.vertex_count, edges)
    succ = successors(case.vertex_count, edges)
    deps = dependency_supports(case.vertex_count, pred, case.horizon)

    checks = 0
    for source in range(case.vertex_count):
        reachable = forward_reachability(
            case.vertex_count, succ, source, case.horizon
        )
        for tick in range(case.horizon + 1):
            affected = {
                vertex
                for vertex in range(case.vertex_count)
                if source in deps[tick][vertex]
            }
            assert affected <= reachable[tick], (
                case.name,
                source,
                tick,
                sorted(affected),
                sorted(reachable[tick]),
            )
            outside = set(range(case.vertex_count)) - reachable[tick]
            assert all(source not in deps[tick][v] for v in outside)
            checks += 2
            if case.include_self_edges:
                assert affected == reachable[tick], (
                    case.name,
                    source,
                    tick,
                    sorted(affected),
                    sorted(reachable[tick]),
                )
                checks += 1
    return len(edges), checks


def line_case(length: int, horizon: int) -> GraphCase:
    edges = []
    for i in range(length - 1):
        edges.append((i, i + 1))
        edges.append((i + 1, i))
    return GraphCase("undirected_nn_line", length, tuple(edges), horizon, True)


def grid_case(width: int, height: int, horizon: int) -> GraphCase:
    def idx(x: int, y: int) -> int:
        return y * width + x

    edges = []
    for y in range(height):
        for x in range(width):
            if x + 1 < width:
                edges.append((idx(x, y), idx(x + 1, y)))
                edges.append((idx(x + 1, y), idx(x, y)))
            if y + 1 < height:
                edges.append((idx(x, y), idx(x, y + 1)))
                edges.append((idx(x, y + 1), idx(x, y)))
    return GraphCase(
        "undirected_nn_grid", width * height, tuple(edges), horizon, True
    )


def branching_dag_case() -> GraphCase:
    edges = (
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 5),
        (4, 5),
        (5, 6),
        (3, 7),
    )
    return GraphCase("branching_dag", 8, edges, 5, False)


def layered_dag_case() -> GraphCase:
    layers = [range(0, 2), range(2, 5), range(5, 9), range(9, 12)]
    edges = []
    for left_layer, right_layer in zip(layers, layers[1:]):
        for u in left_layer:
            for v in right_layer:
                if (u + 2 * v) % 3 != 1:
                    edges.append((u, v))
    return GraphCase("layered_dag", 12, tuple(edges), 4, False)


def main() -> None:
    cases = (
        line_case(length=9, horizon=5),
        grid_case(width=5, height=4, horizon=4),
        branching_dag_case(),
        layered_dag_case(),
    )

    total_checks = 0
    print("NN topological causal-bound certificate")
    print("claim: finite graph/DAG forward reachability only")
    print()

    for case in cases:
        edge_count, checks = check_case(case)
        total_checks += checks
        print(
            f"PASS {case.name}: vertices={case.vertex_count} "
            f"dependency_edges={edge_count} horizon={case.horizon} "
            f"mode={'exact' if case.include_self_edges else 'bound'} "
            f"assertions={checks}"
        )

    print()
    print(f"TOTAL PASS: {len(cases)} graph families, {total_checks} assertions")
    print("NON-CLAIMS:")
    print("  - no emergent relativity check")
    print("  - no Lorentz-invariance check")
    print("  - no physical-spacetime light-cone check")
    print("  - no universal-speed-law check")
    print("  - no causal-field distance-law check")
    print("  - no mass-response or Newtonian falloff check")


if __name__ == "__main__":
    main()
