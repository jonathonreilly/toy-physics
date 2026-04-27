#!/usr/bin/env python3
"""Chronology lane probe: late-to-early channel versus retarded DAG semantics.

The retained chronology surface uses one clock and a directed/retarded causal
order. This probe starts with a small acyclic causal graph, then inserts a
late-to-early edge. The insertion has two possible readings:

1. as a local retarded channel, it fails because it violates time orientation
   and destroys topological order;
2. as a solvable equation system, it becomes a global fixed-point problem whose
   earlier values can depend on future source data.

The second reading is outside the retained local Cauchy-data framework.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction


PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def topo_order(nodes: list[str], edges: list[tuple[str, str]]) -> list[str] | None:
    children = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for src, dst in edges:
        children[src].append(dst)
        indegree[dst] += 1

    q = deque(node for node in nodes if indegree[node] == 0)
    order: list[str] = []
    while q:
        node = q.popleft()
        order.append(node)
        for dst in children[node]:
            indegree[dst] -= 1
            if indegree[dst] == 0:
                q.append(dst)
    return order if len(order) == len(nodes) else None


def time_orientation_violations(
    times: dict[str, int], edges: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    return [(src, dst) for src, dst in edges if times[dst] <= times[src]]


def retarded_evaluate(
    order: list[str],
    edges: list[tuple[str, str]],
    source: dict[str, Fraction],
    alpha: Fraction,
) -> dict[str, Fraction]:
    parents = {node: [] for node in order}
    for src, dst in edges:
        parents[dst].append(src)

    values: dict[str, Fraction] = {}
    for node in order:
        values[node] = source.get(node, Fraction(0)) + alpha * sum(
            values[parent] for parent in parents[node]
        )
    return values


def solve_linear_system(
    nodes: list[str],
    edges: list[tuple[str, str]],
    source: dict[str, Fraction],
    alpha: Fraction,
) -> dict[str, Fraction]:
    """Solve x_dst - alpha * sum_parent x_parent = source_dst exactly."""

    index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    rhs = [source.get(node, Fraction(0)) for node in nodes]

    for node in nodes:
        row = index[node]
        matrix[row][row] = Fraction(1)
    for src, dst in edges:
        matrix[index[dst]][index[src]] -= alpha

    # Gauss-Jordan elimination over Fractions.
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if matrix[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular fixed-point system")
        if pivot != col:
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            rhs[col], rhs[pivot] = rhs[pivot], rhs[col]

        scale = matrix[col][col]
        matrix[col] = [value / scale for value in matrix[col]]
        rhs[col] /= scale

        for row in range(n):
            if row == col:
                continue
            factor = matrix[row][col]
            if factor == 0:
                continue
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[col])
            ]
            rhs[row] -= factor * rhs[col]

    return {node: rhs[index[node]] for node in nodes}


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> int:
    print("=" * 88)
    print("CHRONOLOGY CYCLE INSERTION PROBE")
    print("  Test: a late-to-early edge is not a retained retarded channel.")
    print("=" * 88)
    print()

    nodes = ["R0", "A1", "B1", "C2"]
    times = {"R0": 0, "A1": 1, "B1": 1, "C2": 2}
    retarded_edges = [("R0", "A1"), ("A1", "C2"), ("R0", "B1"), ("B1", "C2")]
    cycle_edge = ("C2", "R0")
    cyclic_edges = retarded_edges + [cycle_edge]
    source = {
        "R0": Fraction(1),
        "A1": Fraction(0),
        "B1": Fraction(0),
        "C2": Fraction(2),
    }
    alpha = Fraction(1, 2)

    order = topo_order(nodes, retarded_edges)
    check("retarded graph has a topological order", order is not None, f"order={order}")
    check(
        "retarded graph has no time-orientation violation",
        time_orientation_violations(times, retarded_edges) == [],
    )

    if order is None:
        raise SystemExit(1)
    retarded_values = retarded_evaluate(order, retarded_edges, source, alpha)
    check(
        "earlier record value is source-local in the retarded graph",
        retarded_values["R0"] == source["R0"],
        f"R0={fmt_fraction(retarded_values['R0'])}",
    )

    cyclic_order = topo_order(nodes, cyclic_edges)
    violations = time_orientation_violations(times, cyclic_edges)
    check("late-to-early insertion destroys topological order", cyclic_order is None)
    check(
        "late-to-early insertion violates clock orientation",
        violations == [cycle_edge],
        f"violations={violations}",
    )

    fixed_a = solve_linear_system(nodes, cyclic_edges, source, alpha)
    source_b = dict(source)
    source_b["C2"] += Fraction(1)
    fixed_b = solve_linear_system(nodes, cyclic_edges, source_b, alpha)
    delta_r0 = fixed_b["R0"] - fixed_a["R0"]

    check(
        "fixed-point reading makes earlier value depend on future source",
        delta_r0 != 0,
        f"Delta R0 from changing C2 source = {fmt_fraction(delta_r0)}",
    )
    check(
        "future dependence appears only after leaving DAG semantics",
        cyclic_order is None and delta_r0 != 0,
        "classification=nonlocal fixed-point/final-boundary import",
    )

    print()
    print("SAFE READ")
    print("  - The retained retarded graph has a partial order and evaluates forward.")
    print("  - The late-to-early channel is not a local retarded operation.")
    print(
        "  - If forced into equations anyway, it is a global fixed-point problem,"
        " not operational past signaling inside the retained framework."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
