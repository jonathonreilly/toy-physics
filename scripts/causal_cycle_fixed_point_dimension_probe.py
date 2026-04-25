#!/usr/bin/env python3
"""Chronology lane probe: causal cycles trade Cauchy freedom for constraints.

The retained local-data surface evaluates retarded directed acyclic graphs by
choosing source data freely and solving forward in a topological order. If a
directed causal cycle is inserted, the same node equations

    x_dst = source_dst + alpha * sum_parent x_parent

are no longer a forward Cauchy problem. They become a global fixed-point system

    (I - alpha A) x = source.

For nonsingular cycles this is still uniquely solvable for every source vector,
but only as a global fixed-point solve. In singular identity-cycle limits, not
every source vector is consistent, and admissible source dimension is reduced.
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


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fmt_vector(nodes: list[str], values: dict[str, Fraction]) -> str:
    return "(" + ", ".join(f"{node}={fmt_fraction(values[node])}" for node in nodes) + ")"


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


def coefficient_matrix(
    nodes: list[str], edges: list[tuple[str, str]], alpha: Fraction
) -> list[list[Fraction]]:
    """Return M for M x = source, with M = I - alpha A."""

    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[Fraction(0) for _ in nodes] for _ in nodes]
    for node in nodes:
        matrix[index[node]][index[node]] = Fraction(1)
    for src, dst in edges:
        matrix[index[dst]][index[src]] -= alpha
    return matrix


def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []

    row_count = len(rows)
    col_count = len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0

    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]

        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = rows[row][col]
            if factor == 0:
                continue
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break

    return rows, pivot_cols


def rank(matrix: list[list[Fraction]]) -> int:
    return len(rref(matrix)[1])


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(col) for col in zip(*matrix)]


def nullspace_basis(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    reduced, pivot_cols = rref(matrix)
    if not reduced:
        return []

    col_count = len(reduced[0])
    pivot_set = set(pivot_cols)
    pivot_row_for_col = {col: row for row, col in enumerate(pivot_cols)}
    free_cols = [col for col in range(col_count) if col not in pivot_set]
    basis: list[list[Fraction]] = []

    for free_col in free_cols:
        vector = [Fraction(0) for _ in range(col_count)]
        vector[free_col] = Fraction(1)
        for pivot_col in pivot_cols:
            row = pivot_row_for_col[pivot_col]
            vector[pivot_col] = -reduced[row][free_col]
        basis.append(vector)
    return basis


def source_vector(nodes: list[str], source: dict[str, Fraction]) -> list[Fraction]:
    return [source.get(node, Fraction(0)) for node in nodes]


def augmented(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[list[Fraction]]:
    return [row[:] + [rhs_value] for row, rhs_value in zip(matrix, rhs)]


def is_consistent(matrix: list[list[Fraction]], rhs: list[Fraction]) -> bool:
    return rank(matrix) == rank(augmented(matrix, rhs))


def solve_unique(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    if rank(matrix) != len(matrix[0]):
        raise ValueError("system is not uniquely solvable")
    reduced, pivot_cols = rref(augmented(matrix, rhs))
    solution = [Fraction(0) for _ in range(len(matrix[0]))]
    for row, col in enumerate(pivot_cols):
        if col < len(solution):
            solution[col] = reduced[row][-1]
    return solution


def particular_solution(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    if not is_consistent(matrix, rhs):
        raise ValueError("system is inconsistent")
    reduced, pivot_cols = rref(augmented(matrix, rhs))
    solution = [Fraction(0) for _ in range(len(matrix[0]))]
    for row, col in enumerate(pivot_cols):
        if col < len(solution):
            solution[col] = reduced[row][-1]
    return solution


def vector_to_dict(nodes: list[str], vector: list[Fraction]) -> dict[str, Fraction]:
    return {node: vector[i] for i, node in enumerate(nodes)}


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


def dimension_report(matrix: list[list[Fraction]]) -> dict[str, int]:
    node_dim = len(matrix)
    matrix_rank = rank(matrix)
    return {
        "nodes": node_dim,
        "rank": matrix_rank,
        "admissible_source_dimension": matrix_rank,
        "source_constraints": node_dim - matrix_rank,
        "solution_freedom_dimension": len(matrix[0]) - matrix_rank,
    }


def print_report(label: str, report: dict[str, int]) -> None:
    print(f"{label}:")
    print(f"  nodes = {report['nodes']}")
    print(f"  rank(M) = {report['rank']}")
    print(f"  admissible source dimension = {report['admissible_source_dimension']}")
    print(f"  source constraints = {report['source_constraints']}")
    print(f"  solution freedom dimension = {report['solution_freedom_dimension']}")


def dot(lhs: list[Fraction], rhs: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(lhs, rhs))


def constraint_text(nodes: list[str], constraint: list[Fraction]) -> str:
    terms = []
    for node, coeff in zip(nodes, constraint):
        if coeff == 0:
            continue
        terms.append(f"{fmt_fraction(coeff)}*s_{node}")
    return " + ".join(terms) + " = 0"


def main() -> int:
    print("=" * 88)
    print("CAUSAL CYCLE FIXED-POINT DIMENSION PROBE")
    print("  Test: directed cycles replace local Cauchy freedom with fixed-point algebra.")
    print("=" * 88)
    print()

    nodes = ["R0", "M1", "L2"]
    chain_edges = [("R0", "M1"), ("M1", "L2")]
    cycle_edges = chain_edges + [("L2", "R0")]
    source = {"R0": Fraction(1), "M1": Fraction(0), "L2": Fraction(0)}
    alpha = Fraction(1, 2)

    print("CASE 1: acyclic chain / retained retarded Cauchy solve")
    order = topo_order(nodes, chain_edges)
    chain_matrix = coefficient_matrix(nodes, chain_edges, alpha)
    chain_report = dimension_report(chain_matrix)
    print_report("  Dimension count", chain_report)
    check("acyclic chain has a topological order", order == nodes, f"order={order}")
    check("acyclic chain admits all local source data", chain_report["admissible_source_dimension"] == 3)
    check("acyclic chain imposes no source constraints", chain_report["source_constraints"] == 0)
    check("acyclic chain has unique forward solution", chain_report["solution_freedom_dimension"] == 0)
    if order is None:
        raise SystemExit(1)
    forward = retarded_evaluate(order, chain_edges, source, alpha)
    linear = vector_to_dict(nodes, solve_unique(chain_matrix, source_vector(nodes, source)))
    print(f"  forward solution = {fmt_vector(nodes, forward)}")
    check("topological solve matches linear solve", forward == linear)
    print()

    print("CASE 2: nonsingular directed cycle / global fixed-point solve")
    cycle_order = topo_order(nodes, cycle_edges)
    cycle_matrix = coefficient_matrix(nodes, cycle_edges, alpha)
    cycle_report = dimension_report(cycle_matrix)
    print_report("  Dimension count", cycle_report)
    fixed_a = vector_to_dict(nodes, solve_unique(cycle_matrix, source_vector(nodes, source)))
    perturbed_source = dict(source)
    perturbed_source["L2"] += Fraction(1)
    fixed_b = vector_to_dict(
        nodes, solve_unique(cycle_matrix, source_vector(nodes, perturbed_source))
    )
    delta_r0 = fixed_b["R0"] - fixed_a["R0"]
    print(f"  fixed-point solution = {fmt_vector(nodes, fixed_a)}")
    print(f"  Delta R0 when L2 source is raised by 1 = {fmt_fraction(delta_r0)}")
    check("cycle has no topological order", cycle_order is None)
    check("nonsingular cycle still admits every source vector", cycle_report["admissible_source_dimension"] == 3)
    check("nonsingular cycle has unique global fixed point", cycle_report["solution_freedom_dimension"] == 0)
    check("late source affects earlier node only in fixed-point reading", delta_r0 == Fraction(4, 7))
    print("  classification = global fixed-point solve, not retained forward Cauchy evolution")
    print()

    print("CASE 3: singular identity cycle / self-consistency constraint")
    identity_alpha = Fraction(1)
    singular_matrix = coefficient_matrix(nodes, cycle_edges, identity_alpha)
    singular_report = dimension_report(singular_matrix)
    left_constraints = nullspace_basis(transpose(singular_matrix))
    admissible_source = {"R0": Fraction(1), "M1": Fraction(-1), "L2": Fraction(0)}
    inconsistent_source = {"R0": Fraction(1), "M1": Fraction(0), "L2": Fraction(0)}
    admissible_rhs = source_vector(nodes, admissible_source)
    inconsistent_rhs = source_vector(nodes, inconsistent_source)
    singular_particular = vector_to_dict(
        nodes, particular_solution(singular_matrix, admissible_rhs)
    )
    print_report("  Dimension count", singular_report)
    for constraint in left_constraints:
        print(f"  consistency constraint: {constraint_text(nodes, constraint)}")
    print(f"  one admissible solution with free parameter set to 0 = {fmt_vector(nodes, singular_particular)}")
    check("identity cycle is singular", singular_report["rank"] == 2)
    check("identity cycle reduces admissible source dimension", singular_report["admissible_source_dimension"] == 2)
    check("identity cycle imposes one source constraint", singular_report["source_constraints"] == 1)
    check("identity cycle leaves one fixed-point free variable", singular_report["solution_freedom_dimension"] == 1)
    check("sum-zero source is consistent", is_consistent(singular_matrix, admissible_rhs))
    check("non-sum-zero source is rejected", not is_consistent(singular_matrix, inconsistent_rhs))
    if left_constraints:
        check(
            "reported constraint accepts admissible source",
            dot(left_constraints[0], admissible_rhs) == 0,
        )
        check(
            "reported constraint rejects inconsistent source",
            dot(left_constraints[0], inconsistent_rhs) != 0,
        )
    print()

    print("SAFE READ")
    print("  - A DAG keeps source/local Cauchy data freely specifiable and solves forward.")
    print("  - A nonsingular cycle can be solved only as a global fixed-point problem.")
    print("  - A singular identity cycle cuts admissible source dimension and adds a")
    print("    self-consistency constraint, so local data are no longer freely chosen.")
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
