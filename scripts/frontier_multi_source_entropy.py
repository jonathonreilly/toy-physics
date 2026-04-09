"""Multi-source entanglement entropy: breaking the ln(2) saturation.

Hypothesis: The S_vN = ln(2) saturation observed in the area-law script
is an artifact of the single-source initial condition creating a rank-2
effective state. Using multiple source positions should produce a
higher-rank density matrix and break the ln(2) ceiling.

Method:
  - For N_s source positions on x=0, propagate each independently.
  - At x=cut_x, collect amplitudes M[y_cut, source_idx].
  - rho_B = M @ M^H, normalize, compute S_vN.
  - Compare S_vN across N_s = 1, 2, 3, 5, 9, 13, 17.

Falsification: If S stays at ln(2) for all N_s, the slit geometry
constrains entanglement regardless of source count.

Overclaiming guard: Even if S grows with N_s, do NOT claim area law.

Pure Python -- no numpy dependency.
"""

from __future__ import annotations

import cmath
import math
import sys
import os
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_with_field,
    build_causal_dag,
    local_edge_properties,
)

# ---------------------------------------------------------------------------
# Pure-Python complex Hermitian eigenvalue solver (Jacobi)
# Copied from frontier_entanglement_area_law.py
# ---------------------------------------------------------------------------

Matrix = list[list[complex]]


def mat_zeros(n: int) -> Matrix:
    return [[0.0 + 0j for _ in range(n)] for _ in range(n)]


def hermitian_eigenvalues(h: Matrix, max_iter: int = 500) -> list[float]:
    """Eigenvalues of a complex Hermitian matrix via Jacobi rotations."""
    n = len(h)
    if n == 0:
        return []
    if n == 1:
        return [h[0][0].real]

    a: Matrix = [[h[i][j] for j in range(n)] for i in range(n)]

    for i in range(n):
        a[i][i] = complex(a[i][i].real, 0.0)
        for j in range(i + 1, n):
            avg = 0.5 * (a[i][j] + a[j][i].conjugate())
            a[i][j] = avg
            a[j][i] = avg.conjugate()

    for _sweep in range(max_iter):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                mag = abs(a[i][j])
                if mag > max_val:
                    max_val = mag
                    p, q = i, j
        if max_val < 1e-14:
            break

        z = a[p][q]
        mag_z = abs(z)
        if mag_z < 1e-30:
            continue

        phase = z / mag_z
        phase_conj = phase.conjugate()

        app = a[p][p].real
        aqq = a[q][q].real
        diff = app - aqq

        if abs(diff) < 1e-30:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2.0 * mag_z, diff)

        c = math.cos(theta)
        s = math.sin(theta)

        for i in range(n):
            if i == p or i == q:
                continue
            aip = a[i][p]
            aiq = a[i][q]
            a[i][p] = c * aip + s * phase_conj * aiq
            a[p][i] = a[i][p].conjugate()
            a[i][q] = -s * phase * aip + c * aiq
            a[q][i] = a[i][q].conjugate()

        new_pp = c * c * app + 2 * c * s * mag_z + s * s * aqq
        new_qq = s * s * app - 2 * c * s * mag_z + c * c * aqq
        a[p][p] = complex(new_pp, 0.0)
        a[q][q] = complex(new_qq, 0.0)
        a[p][q] = 0.0 + 0j
        a[q][p] = 0.0 + 0j

    return sorted(a[i][i].real for i in range(n))


def von_neumann_entropy(eigenvalues: list[float]) -> float:
    entropy = 0.0
    for lam in eigenvalues:
        if lam > 1e-15:
            entropy -= lam * math.log(lam)
    return entropy


# ---------------------------------------------------------------------------
# Propagation
# ---------------------------------------------------------------------------


def propagate_single_source(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule: Any,
    node_field: dict[tuple[int, int], float],
    cut_x: int,
) -> dict[int, complex]:
    """Propagate unit amplitude from a single source, return {y_cut: amplitude}."""
    arrival_times = infer_arrival_times_with_field(nodes, source, rule, node_field)
    dag = build_causal_dag(nodes, arrival_times)

    state: dict[tuple[int, int], complex] = {source: 1.0 + 0j}

    order = sorted(
        (n for n in arrival_times if n in dag or n == source),
        key=lambda n: arrival_times[n],
    )

    result: dict[int, complex] = {}

    for node in order:
        amp = state.get(node)
        if amp is None or abs(amp) < 1e-30:
            continue

        if node[0] == cut_x:
            result[node[1]] = result.get(node[1], 0j) + amp
            continue

        if node[0] > cut_x:
            continue

        for neighbor in dag.get(node, []):
            _, _, link_amp = local_edge_properties(
                node, neighbor, rule, node_field,
            )
            if neighbor not in state:
                state[neighbor] = 0j
            state[neighbor] += amp * link_amp

    return result


def build_propagator_matrix(
    nodes: set[tuple[int, int]],
    sources: list[tuple[int, int]],
    rule: Any,
    node_field: dict[tuple[int, int], float],
    cut_x: int,
    y_cut_positions: list[int],
) -> Matrix:
    """Build M[y_cut_idx, source_idx] by propagating from each source."""
    n_cut = len(y_cut_positions)
    n_src = len(sources)
    y_to_idx = {y: i for i, y in enumerate(y_cut_positions)}

    M = [[0.0 + 0j for _ in range(n_src)] for _ in range(n_cut)]

    for j, src in enumerate(sources):
        amplitudes = propagate_single_source(nodes, src, rule, node_field, cut_x)
        for y, amp in amplitudes.items():
            if y in y_to_idx:
                M[y_to_idx[y]][j] += amp

    return M


def build_rho_B(M: Matrix) -> Matrix:
    """rho_B(y, y') = sum_j M(y, j) * conj(M(y', j)) = M @ M^dagger."""
    n_cut = len(M)
    if n_cut == 0:
        return []
    n_src = len(M[0])

    rho = mat_zeros(n_cut)
    for i in range(n_cut):
        for j in range(n_cut):
            s = 0.0 + 0j
            for k in range(n_src):
                s += M[i][k] * M[j][k].conjugate()
            rho[i][j] = s
    return rho


# ---------------------------------------------------------------------------
# Source selection
# ---------------------------------------------------------------------------


def select_sources(height: int, n_sources: int) -> list[tuple[int, int]]:
    """Select n_sources evenly spaced y-positions from [-height, height] at x=0."""
    y_min = -height
    y_max = height
    full_range = list(range(y_min, y_max + 1))

    if n_sources >= len(full_range):
        return [(0, y) for y in full_range]

    if n_sources == 1:
        return [(0, 0)]

    if n_sources == 2:
        step = height
        return [(0, -step), (0, step)]

    # Evenly spaced including endpoints
    indices = [round(i * (len(full_range) - 1) / (n_sources - 1)) for i in range(n_sources)]
    return [(0, full_range[idx]) for idx in indices]


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_multi_source(
    height: int,
    width: int,
    cut_x: int,
    postulates: RulePostulates,
    n_sources: int,
    persistent_nodes: frozenset[tuple[int, int]] = frozenset(),
) -> dict[str, Any]:
    """Run experiment with n_sources source positions."""
    nodes = build_rectangular_nodes(width=width, height=height)
    rule = derive_local_rule(persistent_nodes=persistent_nodes, postulates=postulates)
    node_field = derive_node_field(nodes, rule)

    sources = select_sources(height, n_sources)
    # Filter to sources that actually exist in nodes
    sources = [s for s in sources if s in nodes]

    y_cut_positions = sorted(y for (x, y) in nodes if x == cut_x)

    M = build_propagator_matrix(nodes, sources, rule, node_field, cut_x, y_cut_positions)
    rho = build_rho_B(M)

    # Normalize
    n = len(rho)
    tr = sum(rho[i][i].real for i in range(n))
    if tr > 1e-30:
        for i in range(n):
            for j in range(n):
                rho[i][j] /= tr

    eigenvalues = hermitian_eigenvalues(rho)
    s_vn = von_neumann_entropy(eigenvalues)
    rank = sum(1 for e in eigenvalues if e > 1e-10)

    return {
        "n_sources_requested": n_sources,
        "n_sources_actual": len(sources),
        "source_ys": [s[1] for s in sources],
        "n_cut": len(y_cut_positions),
        "S_vN": s_vn,
        "rank": rank,
        "trace_before_norm": tr,
        "eigenvalues": eigenvalues,
    }


def main() -> None:
    LN2 = math.log(2)

    print("=" * 80)
    print("MULTI-SOURCE ENTANGLEMENT ENTROPY: BREAKING ln(2) SATURATION?")
    print("=" * 80)
    print()
    print("Hypothesis: S_vN = ln(2) saturation is an artifact of single-source")
    print("  initial condition creating rank-2 effective state. Multiple sources")
    print("  should increase the rank and break the ceiling.")
    print()
    print("Falsification: If S stays at ln(2) for all N_s, geometry constrains it.")
    print("Overclaiming guard: Even if S grows, do NOT claim area law.")
    print()

    width = 20
    height = 8
    cut_x = 10
    boundary = 2 * height + 1  # = 17

    postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
    )

    mass_nodes = frozenset(
        (x, y)
        for x in range(width // 2 - 1, width // 2 + 2)
        for y in range(-1, 2)
        if abs(x - width // 2) + abs(y) <= 2
    )

    ns_values = [1, 2, 3, 5, 9, 13, 17]

    # ===================================================================
    # Experiment A: Free space, vary N_s
    # ===================================================================
    print(f"Parameters: width={width}, height={height}, cut_x={cut_x}, "
          f"k={postulates.phase_per_action}, p={postulates.attenuation_power}")
    print(f"Boundary (n_cut) = {boundary}")
    print(f"ln(2) = {LN2:.6f}")
    print()

    print("EXPERIMENT A: Free space -- vary number of sources")
    print("-" * 72)
    header = f"{'N_s':>4} {'actual':>6} {'S_vN':>10} {'rank':>5} {'S/ln(2)':>8} {'S/ln(N_s)':>10} {'S/ln(bnd)':>10}"
    print(header)
    print("-" * len(header))

    results_free: list[dict] = []
    for ns in ns_values:
        r = run_multi_source(height, width, cut_x, postulates, ns)
        results_free.append(r)

        s = r["S_vN"]
        ln_ns = math.log(max(r["n_sources_actual"], 1))
        ln_bnd = math.log(boundary)
        ratio_ln2 = s / LN2 if LN2 > 0 else 0
        ratio_ns = s / ln_ns if ln_ns > 0 else float("inf")
        ratio_bnd = s / ln_bnd if ln_bnd > 0 else 0

        print(f"{ns:>4} {r['n_sources_actual']:>6} {s:>10.6f} {r['rank']:>5} "
              f"{ratio_ln2:>8.4f} {ratio_ns:>10.4f} {ratio_bnd:>10.4f}")

    # ===================================================================
    # Experiment B: With mass cluster, vary N_s
    # ===================================================================
    print()
    print("EXPERIMENT B: With mass cluster -- vary number of sources")
    print("-" * 72)
    print(header)
    print("-" * len(header))

    results_mass: list[dict] = []
    for ns in ns_values:
        r = run_multi_source(height, width, cut_x, postulates, ns, mass_nodes)
        results_mass.append(r)

        s = r["S_vN"]
        ln_ns = math.log(max(r["n_sources_actual"], 1))
        ln_bnd = math.log(boundary)
        ratio_ln2 = s / LN2 if LN2 > 0 else 0
        ratio_ns = s / ln_ns if ln_ns > 0 else float("inf")
        ratio_bnd = s / ln_bnd if ln_bnd > 0 else 0

        print(f"{ns:>4} {r['n_sources_actual']:>6} {s:>10.6f} {r['rank']:>5} "
              f"{ratio_ln2:>8.4f} {ratio_ns:>10.4f} {ratio_bnd:>10.4f}")

    # ===================================================================
    # Comparison table
    # ===================================================================
    print()
    print("=" * 72)
    print("COMPARISON: Free vs Mass")
    print("-" * 72)
    print(f"{'N_s':>4} {'S_free':>10} {'S_mass':>10} {'dS':>10} {'rk_f':>5} {'rk_m':>5}")
    print("-" * 50)
    for rf, rm in zip(results_free, results_mass):
        ns = rf["n_sources_actual"]
        ds = rm["S_vN"] - rf["S_vN"]
        print(f"{ns:>4} {rf['S_vN']:>10.6f} {rm['S_vN']:>10.6f} {ds:>10.6f} "
              f"{rf['rank']:>5} {rm['rank']:>5}")

    # ===================================================================
    # Eigenvalue spectrum for key cases
    # ===================================================================
    print()
    print("=" * 72)
    print("EIGENVALUE SPECTRUM (top 5 eigenvalues)")
    print("-" * 72)
    for r in results_free:
        ns = r["n_sources_actual"]
        top5 = r["eigenvalues"][-5:]
        top5_str = ", ".join(f"{e:.6f}" for e in reversed(top5))
        print(f"  N_s={ns:>2}: [{top5_str}]")

    # ===================================================================
    # Analysis
    # ===================================================================
    print()
    print("=" * 72)
    print("ANALYSIS")
    print("=" * 72)

    s_values = [r["S_vN"] for r in results_free]
    ns_actual = [r["n_sources_actual"] for r in results_free]
    ranks = [r["rank"] for r in results_free]

    s_single = s_values[0]
    s_max = max(s_values)
    ns_at_max = ns_actual[s_values.index(s_max)]

    print(f"\n  Single source (N_s=1):  S = {s_single:.6f}  (= {s_single/LN2:.3f} * ln(2))")
    print(f"  Maximum entropy:        S = {s_max:.6f}  at N_s={ns_at_max}")
    print(f"  Maximum rank:           {max(ranks)} at N_s={ns_actual[ranks.index(max(ranks))]}")
    print(f"  ln(2) = {LN2:.6f},  ln(boundary={boundary}) = {math.log(boundary):.6f}")

    # Check monotonicity
    monotone = all(s_values[i] <= s_values[i + 1] + 1e-10 for i in range(len(s_values) - 1))
    print(f"\n  S monotonically increasing with N_s: {monotone}")

    # Check if ln(2) barrier is broken
    ln2_broken = s_max > LN2 + 0.01
    print(f"  ln(2) barrier broken: {ln2_broken}")
    if ln2_broken:
        by_how_much = s_max - LN2
        print(f"    Exceeded by {by_how_much:.6f} (= {by_how_much/LN2*100:.1f}% of ln(2))")
        print(f"    ==> POSITIVE: Multi-source DOES break ln(2) saturation")
    else:
        print(f"    S_max = {s_max:.6f} vs ln(2) = {LN2:.6f}")
        print(f"    ==> NEGATIVE: ln(2) ceiling persists regardless of source count")

    # Rank analysis
    print(f"\n  Rank progression: {list(zip(ns_actual, ranks))}")
    rank_grows = ranks[-1] > ranks[0]
    print(f"  Rank grows with N_s: {rank_grows}")
    if rank_grows:
        print(f"    ==> State space effectively enlarges with more sources")
    else:
        print(f"    ==> Rank stuck at {ranks[0]} -- geometry limits effective dimension")

    # Scaling check: does S ~ ln(N_s)?
    log_ns = [math.log(n) for n in ns_actual if n > 1]
    s_multi = [s for s, n in zip(s_values, ns_actual) if n > 1]
    if len(log_ns) >= 3:
        n_fit = len(log_ns)
        x_mean = sum(log_ns) / n_fit
        y_mean = sum(s_multi) / n_fit
        ss_xx = sum((x - x_mean) ** 2 for x in log_ns)
        ss_yy = sum((y - y_mean) ** 2 for y in s_multi)
        ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(log_ns, s_multi))
        if ss_xx > 1e-30:
            slope = ss_xy / ss_xx
            r2 = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 1e-30 else 0
            print(f"\n  Scaling fit S vs ln(N_s): slope={slope:.4f}, R^2={r2:.4f}")
            if r2 > 0.9 and abs(slope - 1.0) < 0.3:
                print(f"    ==> S ~ ln(N_s) scaling (near slope=1)")
            elif r2 > 0.7:
                print(f"    ==> Some logarithmic scaling (slope={slope:.2f})")
            else:
                print(f"    ==> Poor fit to ln(N_s)")

    # Mass effect
    ds_mass = [rm["S_vN"] - rf["S_vN"] for rf, rm in zip(results_free, results_mass)]
    ds_mean = sum(ds_mass) / len(ds_mass)
    print(f"\n  Mass effect: mean dS = {ds_mean:.6f}")
    if abs(ds_mean) > 0.01:
        direction = "increases" if ds_mean > 0 else "decreases"
        print(f"    ==> Mass cluster {direction} entropy by {abs(ds_mean):.4f}")
    else:
        print(f"    ==> Negligible mass effect")

    print()


if __name__ == "__main__":
    main()
