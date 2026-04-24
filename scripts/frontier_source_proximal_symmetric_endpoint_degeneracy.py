#!/usr/bin/env python3
"""
Symmetric-endpoint degeneracy of the source-proximal non-bridge edge rule.

Context.
  On a cycle-bearing graph with a source vertex s and an isotropic kernel
  K: N -> R depending only on graph distance, the source-proximal non-
  bridge edge rule picks, within a given cycle, the non-bridge edge whose
  midpoint distance (d(s,u) + d(s,v))/2 is smallest. This rule has been
  proposed as an optimal-sensitivity detector for a time-varying source
  amplitude driving phi(v, t) = S(t) * K(d(s, v)).

Finding.
  The rule has a characterized degeneracy. When the selected edge e=(u,v)
  has equidistant endpoints d(s,u) = d(s,v), the detector returns
  span_e(t) = 0 identically, for any time-dependent source amplitude S(t)
  and any isotropic kernel K.

Proof (S.1, symbolic).
    phi(u, t) = S(t) * K(d(s, u))
    phi(v, t) = S(t) * K(d(s, v))
    d(s,u) = d(s,v)  ==>  K(d(s,u)) = K(d(s,v))
                       ==>  phi(u, t) = phi(v, t) for all t
                       ==>  j_e(t) := phi(v, t) - phi(u, t) = 0 identically.

Concrete counter-example.
  Triangular prism: bottom triangle 0-1-2, top triangle 3-4-5, verticals
  0-3, 1-4, 2-5. Source s=5, BFS root 0.
    BFS tree edges: {(0,1), (0,2), (0,3), (3,4), (3,5)}.
    Back edges:     {(1,2), (1,4), (2,5), (4,5)}.
  Fundamental cycle from back-edge (1,4): 1 -> 0 -> 3 -> 4 -> 1, with
  edges (1,0), (0,3), (3,4), (4,1). Midpoint distances to source 5:
    (0,1): (2+2)/2 = 2.0
    (0,3): (2+1)/2 = 1.5
    (3,4): (1+1)/2 = 1.0   <-- minimum, symmetric endpoints
    (1,4): (2+1)/2 = 1.5
  The rule selects (3,4), whose endpoints 3 and 4 are both distance 1
  from source 5. Under any isotropic kernel K, phi(3, t) = phi(4, t) and
  the detector span is zero.

Positive control.
  A different basis cycle of the same prism uses edge (2,5), endpoints at
  distances 1 and 0 from source 5. Span > 0 under the same kernel.
  The degeneracy is specific to edges with endpoint symmetry, not a
  graph-wide failure.

Remediation.
  Among candidate non-bridge edges in a cycle, restrict to edges with
  non-equidistant endpoints before minimizing midpoint distance. If no
  such edge exists, declare the cycle's detector N/A (the graph-geometric
  symmetry forces a degenerate readout for every non-bridge edge under
  any isotropic kernel).

Scope.
  The derivation uses only that K depends on d(s, v) alone. For
  anisotropic kernels (e.g., direction-biased or path-sensitive), the
  failure mode does not necessarily apply.

Falsifier.
  - A graph with an isotropic kernel where equidistant endpoints of a
    non-bridge edge produce nonzero span (would contradict S.1).
  - A source-proximal-rule selection that gives zero span without
    equidistant endpoints (would contradict the characterization).
"""

from __future__ import annotations

import math
import sys
import time
from collections import deque
from typing import Dict, List, Set, Tuple

import numpy as np
import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# -------- Graph helpers --------

Edge = Tuple[int, int]
Adj = Dict[int, List[int]]


def edges_of(adj: Adj) -> Set[Edge]:
    out: Set[Edge] = set()
    for u, nbs in adj.items():
        for v in nbs:
            out.add((min(u, v), max(u, v)))
    return out


def num_components(adj: Adj) -> int:
    verts = set(adj.keys())
    for nbs in adj.values():
        verts.update(nbs)
    seen: Set[int] = set()
    count = 0
    for v in verts:
        if v in seen:
            continue
        count += 1
        q = deque([v])
        while q:
            x = q.popleft()
            if x in seen:
                continue
            seen.add(x)
            for n in adj.get(x, ()):
                if n not in seen:
                    q.append(n)
    return count


def bfs_distance(adj: Adj, source: int, target: int) -> int:
    if source == target:
        return 0
    seen = {source}
    q = deque([(source, 0)])
    while q:
        v, d = q.popleft()
        for u in adj.get(v, ()):
            if u in seen:
                continue
            if u == target:
                return d + 1
            seen.add(u)
            q.append((u, d + 1))
    return math.inf


def bfs_spanning_tree(adj: Adj, root: int) -> Tuple[Dict[int, int], Set[Edge]]:
    parent: Dict[int, int] = {root: -1}
    tree_edges: Set[Edge] = set()
    q = deque([root])
    while q:
        v = q.popleft()
        for u in adj.get(v, ()):
            if u not in parent:
                parent[u] = v
                tree_edges.add((min(u, v), max(u, v)))
                q.append(u)
    return parent, tree_edges


def tree_path(parent: Dict[int, int], src: int, dst: int) -> List[int]:
    anc_src = []
    x = src
    while x != -1:
        anc_src.append(x)
        x = parent[x]
    anc_set = set(anc_src)
    from_dst = []
    x = dst
    while x not in anc_set and x != -1:
        from_dst.append(x)
        x = parent[x]
    lca = x
    up = []
    y = src
    while y != lca:
        up.append(y)
        y = parent[y]
    up.append(lca)
    return up + list(reversed(from_dst))


def fundamental_cycles(adj: Adj, root: int) -> List[List[int]]:
    parent, tree_edges = bfs_spanning_tree(adj, root)
    back_edges = sorted(edges_of(adj) - tree_edges)
    return [tree_path(parent, u, v) + [u] for (u, v) in back_edges]


def is_bridge(adj: Adj, edge: Edge) -> bool:
    a, b = edge
    cut = {v: [x for x in nbs if not ((v == a and x == b) or (v == b and x == a))]
           for v, nbs in adj.items()}
    return num_components(cut) > num_components(adj)


def cycle_edge_sequence(cycle: List[int]) -> List[Edge]:
    return [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]


def source_proximal_non_bridge(adj: Adj, cycle: List[int], source: int) -> Edge | None:
    candidates: List[Edge] = []
    for a, b in cycle_edge_sequence(cycle):
        e = (min(a, b), max(a, b))
        if not is_bridge(adj, e):
            candidates.append(e)
    if not candidates:
        return None
    return min(candidates,
               key=lambda e: (bfs_distance(adj, source, e[0])
                              + bfs_distance(adj, source, e[1])) / 2.0)


def triangular_prism_adj() -> Adj:
    return {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 5],
        3: [0, 4, 5],
        4: [1, 3, 5],
        5: [2, 3, 4],
    }


# -------- S.1 Symbolic proof --------

def s1_symbolic_proof() -> None:
    """For any symbolic isotropic kernel K(d), equidistant endpoints
    give j = phi_v - phi_u = 0 identically. This is the general statement
    the failure mode rests on."""
    section("S.1 Symbolic proof: isotropic kernel + equidistant endpoints -> j = 0")

    S = sp.Function("S")
    K = sp.Function("K")
    t, d_equal = sp.symbols("t d_equal", real=True)

    # Two vertices at the same graph distance d_equal from the source.
    phi_u = S(t) * K(d_equal)
    phi_v = S(t) * K(d_equal)
    j_symbolic = sp.simplify(phi_v - phi_u)

    record(
        "S.1 symbolic j(t) = phi_v(t) - phi_u(t) simplifies to 0 for equidistant endpoints",
        j_symbolic == 0,
        f"phi_u = S(t) * K(d_equal),  phi_v = S(t) * K(d_equal)\n"
        f"j_symbolic = simplify(phi_v - phi_u) = {j_symbolic}",
    )

    # Sanity: with distinct distances d_u != d_v, j need not be zero.
    d_u, d_v = sp.symbols("d_u d_v", real=True)
    j_asym = sp.simplify(S(t) * K(d_v) - S(t) * K(d_u))
    record(
        "S.1b non-equidistant case: j_symbolic is NOT identically zero",
        j_asym != 0,
        f"j_asym = S(t) * (K(d_v) - K(d_u)) = {j_asym}",
    )


# -------- S.2 Concrete counter-example on the triangular prism --------

def s2_prism_counter_example() -> None:
    section("S.2 Concrete counter-example: triangular prism, source=5, BFS root=0")

    adj = triangular_prism_adj()
    source = 5
    root = 0

    cycles = fundamental_cycles(adj, root=root)

    # The back-edge (1,4) generates the cycle containing edge (3,4).
    # Find it explicitly.
    target_cycle = None
    for c in cycles:
        if (3, 4) in {(min(a, b), max(a, b)) for a, b in cycle_edge_sequence(c)}:
            target_cycle = c
            break

    record(
        "S.2 prism has a fundamental cycle containing the symmetric edge (3,4)",
        target_cycle is not None,
        f"fundamental cycles from root 0: {cycles}\n"
        f"target cycle (contains edge (3,4)): {target_cycle}",
    )

    sp_edge = source_proximal_non_bridge(adj, target_cycle, source)
    d_a = bfs_distance(adj, source, sp_edge[0])
    d_b = bfs_distance(adj, source, sp_edge[1])

    record(
        "S.2 source-proximal rule selects edge (3,4) with equidistant endpoints d=1",
        sp_edge == (3, 4) and d_a == 1 and d_b == 1,
        f"selected edge = {sp_edge},  d(5, {sp_edge[0]}) = {d_a},  d(5, {sp_edge[1]}) = {d_b}",
    )


# -------- S.3 Kernel-independence: three different isotropic kernels --------

def _span_on_prism_edge(kernel_fn, source: int = 5) -> Dict[Edge, float]:
    """Compute numeric span over one period of S(t) = sin(t) for each edge
    of the target cycle under a given isotropic kernel."""
    adj = triangular_prism_adj()
    verts = sorted(adj.keys())
    times = np.linspace(0, 2 * np.pi, 40)
    S_t = np.sin(times)
    phi = {v: S_t * kernel_fn(bfs_distance(adj, source, v)) for v in verts}

    cycles = fundamental_cycles(adj, root=0)
    target_cycle = next(c for c in cycles
                        if (3, 4) in {(min(a, b), max(a, b)) for a, b in cycle_edge_sequence(c)})
    spans: Dict[Edge, float] = {}
    for a, b in cycle_edge_sequence(target_cycle):
        e = (min(a, b), max(a, b))
        j_t = phi[e[1]] - phi[e[0]]
        spans[e] = float(j_t.max() - j_t.min())
    return spans


def s3_kernel_independence() -> None:
    section("S.3 Kernel-independence: span_{(3,4)} = 0 for Yukawa, Coulomb, and log kernels")

    kernels = {
        "Yukawa mu=1.0":     lambda d: math.exp(-1.0 * d),
        "Yukawa mu=0.3":     lambda d: math.exp(-0.3 * d),
        "Coulomb-like":      lambda d: 1.0 / (1.0 + d),
        "Log kernel":        lambda d: -math.log(1.0 + d),
    }

    for name, kfn in kernels.items():
        spans = _span_on_prism_edge(kfn)
        span_34 = spans[(3, 4)]
        record(
            f"S.3 {name}: span on equidistant edge (3,4) is zero",
            span_34 < 1e-12,
            f"span_{{(3,4)}} = {span_34:.3e}  (all spans on target cycle: "
            + ", ".join(f"{e}:{s:.4f}" for e, s in sorted(spans.items())) + ")",
        )


# -------- S.4 Positive control: cycle through edge (2,5) gives nonzero span --------

def s4_positive_control() -> None:
    section("S.4 Positive control: a basis cycle through asymmetric edge (2,5) gives span > 0")

    adj = triangular_prism_adj()
    source = 5
    cycles = fundamental_cycles(adj, root=0)

    # Identify the basis cycle containing edge (2,5).
    target_cycle = next(c for c in cycles
                        if (2, 5) in {(min(a, b), max(a, b)) for a, b in cycle_edge_sequence(c)})
    sp_edge = source_proximal_non_bridge(adj, target_cycle, source)
    d_a = bfs_distance(adj, source, sp_edge[0])
    d_b = bfs_distance(adj, source, sp_edge[1])

    kfn = lambda d: math.exp(-1.0 * d)  # Yukawa mu=1.0
    spans = {}
    times = np.linspace(0, 2 * np.pi, 40)
    S_t = np.sin(times)
    phi = {v: S_t * kfn(bfs_distance(adj, source, v)) for v in sorted(adj.keys())}
    for a, b in cycle_edge_sequence(target_cycle):
        e = (min(a, b), max(a, b))
        j_t = phi[e[1]] - phi[e[0]]
        spans[e] = float(j_t.max() - j_t.min())

    record(
        "S.4 cycle through (2,5) picks an asymmetric edge with nonzero span",
        d_a != d_b and spans[sp_edge] > 1e-6,
        f"cycle = {target_cycle}\n"
        f"selected edge = {sp_edge},  d(5,{sp_edge[0]}) = {d_a},  d(5,{sp_edge[1]}) = {d_b}\n"
        f"span = {spans[sp_edge]:.4f}  (vs zero on the symmetric cycle)",
    )


# -------- S.5 Remediation: pre-filter asymmetric-endpoint edges --------

def source_proximal_asymmetric_only(adj: Adj, cycle: List[int], source: int) -> Edge | None:
    """Remediation: among non-bridge cycle edges, restrict to those with
    d(s, u) != d(s, v), then pick the minimum-midpoint-distance edge.
    Return None if every non-bridge edge is symmetric (detector N/A)."""
    candidates: List[Edge] = []
    for a, b in cycle_edge_sequence(cycle):
        e = (min(a, b), max(a, b))
        if is_bridge(adj, e):
            continue
        d_a = bfs_distance(adj, source, e[0])
        d_b = bfs_distance(adj, source, e[1])
        if d_a != d_b:
            candidates.append(e)
    if not candidates:
        return None
    return min(candidates,
               key=lambda e: (bfs_distance(adj, source, e[0])
                              + bfs_distance(adj, source, e[1])) / 2.0)


def s5_remediation() -> None:
    section("S.5 Remediation: pre-filter asymmetric-endpoint edges restores nonzero span")

    adj = triangular_prism_adj()
    source = 5
    cycles = fundamental_cycles(adj, root=0)
    target_cycle = next(c for c in cycles
                        if (3, 4) in {(min(a, b), max(a, b)) for a, b in cycle_edge_sequence(c)})

    kfn = lambda d: math.exp(-1.0 * d)
    times = np.linspace(0, 2 * np.pi, 40)
    S_t = np.sin(times)
    phi = {v: S_t * kfn(bfs_distance(adj, source, v)) for v in sorted(adj.keys())}

    sp_edge = source_proximal_asymmetric_only(adj, target_cycle, source)
    j_t = phi[sp_edge[1]] - phi[sp_edge[0]]
    span = float(j_t.max() - j_t.min())
    d_a = bfs_distance(adj, source, sp_edge[0])
    d_b = bfs_distance(adj, source, sp_edge[1])

    record(
        "S.5 asymmetric-only rule on the same cycle selects an edge with nonzero span",
        d_a != d_b and span > 1e-6,
        f"asymmetric-only edge on target cycle = {sp_edge}, "
        f"d(5,{sp_edge[0]})={d_a}, d(5,{sp_edge[1]})={d_b}, span = {span:.4f}\n"
        f"(vs span = 0 from the original rule, which picked symmetric edge (3,4))",
    )


def main() -> int:
    t0 = time.time()
    s1_symbolic_proof()
    s2_prism_counter_example()
    s3_kernel_independence()
    s4_positive_control()
    s5_remediation()

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    elapsed = time.time() - t0
    print(f"PASSED: {n_pass}/{n_total}   wallclock: {elapsed:.2f}s")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("FINDING.")
        print(" The source-proximal non-bridge edge rule has a characterized")
        print(" degeneracy: under any isotropic kernel K(d(s, v)), a selected")
        print(" edge with equidistant endpoints gives span = 0 identically.")
        print(" On the triangular prism with source at vertex 5, the rule's")
        print(" current formulation picks the symmetric edge (3, 4), producing")
        print(" a zero-span detector. Pre-filtering asymmetric-endpoint edges")
        print(" restores a nonzero span on the same cycle.")
        print()
        print(" This is a graph-geometric observation about the heuristic,")
        print(" not a statement about the underlying physics. The detector")
        print(" miss is deterministic and kernel-independent; it should be")
        print(" flagged before the rule is applied downstream.")
        return 0

    print("FAILs detected.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
