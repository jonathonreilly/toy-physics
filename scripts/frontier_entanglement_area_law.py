"""Entanglement area law on the discrete event-network DAG.

Propagate a wave packet through a rectangular DAG, partition at a vertical
cut, trace out region B to obtain the reduced density matrix of region A,
and compute von Neumann entropy.  Vary the boundary size (DAG height) to
test whether S ~ boundary (area law) or S ~ volume.

Key physical setup:
- A single source at (0, 0) propagates through a DAG of width W, height H.
- At the cut boundary x=cut_x, we have 2H+1 spatial sites.
- We track which y-band each path traverses at an intermediate point,
  creating "which-path" sectors. If a path went through y-band k at
  the midpoint, that's sector k.  Different sectors are orthogonal
  (they carry distinguishing environmental information in the full
  theory).
- The reduced density matrix after tracing over sectors:
      rho(y,y') = sum_k  psi_k(y) psi_k(y')*
- Von Neumann entropy S = -Tr(rho ln rho)

For area law: S should scale with boundary size (2H+1), not volume (H*cut_x).

Pure-Python implementation (no numpy dependency).
"""

from __future__ import annotations

import cmath
import math
import sys
import os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
    local_edge_properties,
)

# ---------------------------------------------------------------------------
# Pure-Python Hermitian eigenvalue solver (Jacobi)
# ---------------------------------------------------------------------------

Matrix = list[list[complex]]


def mat_zeros(n: int) -> Matrix:
    return [[0.0 + 0j for _ in range(n)] for _ in range(n)]


def hermitian_eigenvalues(h: Matrix, max_iter: int = 300) -> list[float]:
    n = len(h)
    if n == 0:
        return []
    if n == 1:
        return [h[0][0].real]

    a = [[h[i][j].real for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            avg = 0.5 * (a[i][j] + a[j][i])
            a[i][j] = avg
            a[j][i] = avg

    for _ in range(max_iter * n):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > max_val:
                    max_val = abs(a[i][j])
                    p, q = i, j
        if max_val < 1e-14:
            break

        if abs(a[p][p] - a[q][q]) < 1e-30:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2 * a[p][q], a[p][p] - a[q][q])

        c = math.cos(theta)
        s = math.sin(theta)

        new_a = [row[:] for row in a]
        for i in range(n):
            if i != p and i != q:
                new_a[i][p] = c * a[i][p] + s * a[i][q]
                new_a[p][i] = new_a[i][p]
                new_a[i][q] = -s * a[i][p] + c * a[i][q]
                new_a[q][i] = new_a[i][q]

        new_a[p][p] = c * c * a[p][p] + 2 * s * c * a[p][q] + s * s * a[q][q]
        new_a[q][q] = s * s * a[p][p] - 2 * s * c * a[p][q] + c * c * a[q][q]
        new_a[p][q] = 0.0
        new_a[q][p] = 0.0
        a = new_a

    return sorted(a[i][i] for i in range(n))


def von_neumann_entropy_from_eigenvalues(eigenvalues: list[float]) -> float:
    entropy = 0.0
    for lam in eigenvalues:
        if lam > 1e-15:
            entropy -= lam * math.log(lam)
    return entropy


# ---------------------------------------------------------------------------
# Core propagation with sector tracking
# ---------------------------------------------------------------------------


def propagate_with_node_sectors(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule,
    node_field: dict[tuple[int, int], float],
    cut_x: int,
    sector_x: int,
) -> tuple[dict[int, dict[int, complex]], list[int]]:
    """Propagate from source, labeling paths by which node they pass through
    at x=sector_x.

    The sector label is the y-coordinate at x=sector_x.  This gives
    the maximum possible number of orthogonal sectors (one per node at
    the sector column), creating rich entanglement structure.

    Returns:
        sectors: {sector_y: {cut_y: amplitude}}
        y_positions: sorted list of y at cut_x
    """
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)

    # State: (node, sector_label) -> amplitude
    # sector_label starts as None (before sector_x), becomes y at sector_x
    state: DefaultDict[tuple[tuple[int, int], int | None], complex] = defaultdict(complex)
    state[(source, None)] = 1.0 + 0.0j

    order = sorted(
        (n for n in arrival_times if n in dag or n == source),
        key=lambda n: arrival_times[n],
    )

    # sector_y -> {y_at_cut: amplitude}
    boundary: DefaultDict[int, DefaultDict[int, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    for node in order:
        matching = [
            (sec, amp)
            for (n, sec), amp in list(state.items())
            if n == node and abs(amp) > 1e-30
        ]
        if not matching:
            continue

        if node[0] == cut_x:
            for sec, amp in matching:
                if sec is not None:
                    boundary[sec][node[1]] += amp
                del state[(node, sec)]
            continue

        if node[0] > cut_x:
            for sec, amp in matching:
                del state[(node, sec)]
            continue

        for sec, amp in matching:
            del state[(node, sec)]
            for neighbor in dag.get(node, []):
                _, _, link_amp = local_edge_properties(
                    node, neighbor, rule, node_field,
                )
                next_sec = sec
                # Assign sector when crossing sector_x
                if node[0] < sector_x <= neighbor[0]:
                    next_sec = neighbor[1]
                elif node[0] == sector_x and sec is None:
                    next_sec = node[1]

                state[(neighbor, next_sec)] += amp * link_amp

    y_positions = sorted(y for (x, y) in nodes if x == cut_x)
    return dict(boundary), y_positions


def build_rho_and_entropy(
    sectors: dict[int, dict[int, complex]],
    y_positions: list[int],
) -> tuple[float, int, list[float]]:
    """Build density matrix from sector amplitudes, return (S_vN, rank, eigenvalues)."""
    n = len(y_positions)
    y_to_idx = {y: i for i, y in enumerate(y_positions)}
    rho = mat_zeros(n)

    for sec_y, amp_dict in sectors.items():
        psi = [0.0 + 0j] * n
        for y, amp in amp_dict.items():
            if y in y_to_idx:
                psi[y_to_idx[y]] = amp
        for i in range(n):
            for j in range(n):
                rho[i][j] += psi[i] * psi[j].conjugate()

    tr = sum(rho[i][i].real for i in range(n))
    if tr > 1e-30:
        for i in range(n):
            for j in range(n):
                rho[i][j] /= tr

    eigenvalues = hermitian_eigenvalues(rho)
    s_vn = von_neumann_entropy_from_eigenvalues(eigenvalues)
    rank = sum(1 for e in eigenvalues if e > 1e-10)

    return s_vn, rank, eigenvalues


def run_experiment(
    height: int,
    width: int,
    cut_x: int,
    sector_x: int,
    source: tuple[int, int],
    persistent_nodes: frozenset[tuple[int, int]],
    postulates: RulePostulates,
) -> tuple[int, int, float, int, int]:
    """Returns (boundary_size, volume_A, S_vN, rank, n_sectors)."""
    nodes = build_rectangular_nodes(width=width, height=height)
    rule = derive_local_rule(persistent_nodes=persistent_nodes, postulates=postulates)
    node_field = derive_node_field(nodes, rule)

    sectors, y_positions = propagate_with_node_sectors(
        nodes, source, rule, node_field, cut_x, sector_x,
    )

    s_vn, rank, _ = build_rho_and_entropy(sectors, y_positions)

    boundary_size = len(y_positions)
    volume_a = sum(1 for (x, _) in nodes if x < cut_x)
    n_sectors = len(sectors)

    return boundary_size, volume_a, s_vn, rank, n_sectors


def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    ss_yy = sum((y - y_mean) ** 2 for y in ys)
    ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    if ss_xx < 1e-30:
        return 0.0, y_mean, 0.0
    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 1e-30 else 0.0
    return slope, intercept, r_squared


def main() -> None:
    print("=" * 80)
    print("ENTANGLEMENT AREA LAW ON DISCRETE EVENT-NETWORK DAG")
    print("=" * 80)
    print()
    print("Method: single source at (0,0), sector label = y-coordinate at")
    print("intermediate column.  Each node at the sector column defines an")
    print("orthogonal 'which-path' sector.  The number of sectors grows with")
    print("height (= boundary size), providing a natural area-law test.")
    print()

    width = 20
    cut_x = 10
    source = (0, 0)

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

    # ===================================================================
    # Experiment A: Vary height => vary boundary size
    #   sector_x = cut_x // 2 = 5
    # ===================================================================
    sector_x = cut_x // 2
    heights = [3, 4, 5, 6, 7, 8, 9, 10, 12, 14]

    print(f"EXPERIMENT A: Vary boundary size  (sector_x={sector_x})")
    print(f"  width={width}, cut_x={cut_x}, source={source}")
    print()

    header = (f"{'h':>3} {'bnd':>4} {'vol':>5} {'nsec':>5} "
              f"{'S_free':>10} {'rk_f':>4} {'S_mass':>10} {'rk_m':>4} {'dS':>8}")
    print(header)
    print("-" * len(header))

    data_free: list[tuple[int, int, float, int]] = []
    data_mass: list[tuple[int, int, float, int]] = []

    for h in heights:
        bnd, vol, sf, rkf, nsec = run_experiment(
            h, width, cut_x, sector_x, source, frozenset(), postulates,
        )
        data_free.append((bnd, vol, sf, rkf))

        _, _, sm, rkm, _ = run_experiment(
            h, width, cut_x, sector_x, source, mass_nodes, postulates,
        )
        data_mass.append((bnd, vol, sm, rkm))

        print(f"{h:>3} {bnd:>4} {vol:>5} {nsec:>5} "
              f"{sf:>10.6f} {rkf:>4} {sm:>10.6f} {rkm:>4} {sm - sf:>8.4f}")

    # Fits for free space
    bnds = [float(d[0]) for d in data_free]
    s_f = [d[2] for d in data_free]
    vols = [float(d[1]) for d in data_free]
    s_m = [d[2] for d in data_mass]

    print("\n--- Free space fits ---")
    a_b, b_b, r2_b = linear_fit(bnds, s_f)
    print(f"  S vs boundary: slope={a_b:.5f}  R^2={r2_b:.4f}")
    a_v, b_v, r2_v = linear_fit(vols, s_f)
    print(f"  S vs volume:   slope={a_v:.6f}  R^2={r2_v:.4f}")

    log_b = [math.log(b) for b in bnds]
    log_sf = [math.log(max(s, 1e-15)) for s in s_f]
    alpha, _, r2_pl = linear_fit(log_b, log_sf)
    print(f"  Power law: S ~ bnd^{alpha:.3f}  R^2={r2_pl:.4f}")

    print("\n--- With mass fits ---")
    a_bm, _, r2_bm = linear_fit(bnds, s_m)
    print(f"  S vs boundary: slope={a_bm:.5f}  R^2={r2_bm:.4f}")
    log_sm = [math.log(max(s, 1e-15)) for s in s_m]
    alpha_m, _, r2_plm = linear_fit(log_b, log_sm)
    print(f"  Power law: S ~ bnd^{alpha_m:.3f}  R^2={r2_plm:.4f}")

    # ===================================================================
    # Experiment B: Vary sector_x position to test robustness
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("EXPERIMENT B: Vary sector_x (robustness check)")
    print("=" * 80)

    fixed_h = 8
    sector_positions = [2, 3, 4, 5, 6, 7, 8]

    print(f"  height={fixed_h}, cut_x={cut_x}\n")
    print(f"{'sec_x':>5} {'nsec':>5} {'S_free':>10} {'rank':>5}")
    print("-" * 30)

    for sx in sector_positions:
        _, _, sf, rk, nsec = run_experiment(
            fixed_h, width, cut_x, sx, source, frozenset(), postulates,
        )
        print(f"{sx:>5} {nsec:>5} {sf:>10.6f} {rk:>5}")

    # ===================================================================
    # Experiment C: Fixed height, vary cut_x (volume test)
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("EXPERIMENT C: Fixed height=8, vary cut_x (constant boundary test)")
    print("=" * 80)

    fixed_h_c = 8
    cut_positions = [4, 6, 8, 10, 12, 14, 16, 18]

    print(f"  height={fixed_h_c}, boundary = {2 * fixed_h_c + 1}\n")
    print(f"{'cut_x':>5} {'sec_x':>5} {'vol_A':>6} {'S_free':>10} {'S_mass':>10}")
    print("-" * 46)

    s_free_c: list[float] = []
    s_mass_c: list[float] = []
    vols_c: list[float] = []

    for cx in cut_positions:
        sx = max(1, cx // 2)
        bnd, vol, sf, _, _ = run_experiment(
            fixed_h_c, width, cx, sx, source, frozenset(), postulates,
        )
        _, _, sm, _, _ = run_experiment(
            fixed_h_c, width, cx, sx, source, mass_nodes, postulates,
        )
        print(f"{cx:>5} {sx:>5} {vol:>6} {sf:>10.6f} {sm:>10.6f}")
        s_free_c.append(sf)
        s_mass_c.append(sm)
        vols_c.append(float(vol))

    bnd_const = 2 * fixed_h_c + 1
    s_mean = sum(s_free_c) / len(s_free_c)
    s_std = math.sqrt(sum((s - s_mean) ** 2 for s in s_free_c) / len(s_free_c))
    cv = s_std / s_mean if s_mean > 0 else float("inf")
    _, _, r2_vc = linear_fit(vols_c, s_free_c)

    print(f"\n  Boundary = {bnd_const} (constant)")
    print(f"  S_free: mean={s_mean:.4f}, std={s_std:.4f}, CV={cv:.3f}")
    print(f"  S_free vs volume_A: R^2={r2_vc:.4f}")

    # ===================================================================
    # Experiment D: Diagonal cut test -- at fixed width, if we change
    #   height we change both boundary AND volume together.  The
    #   discriminator is Experiment C where boundary is fixed.
    # ===================================================================

    # ===================================================================
    # Summary
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("SUMMARY AND INTERPRETATION")
    print("=" * 80)

    print(f"\n1. BOUNDARY SCALING (Experiment A):")
    print(f"   Free:  S ~ boundary^{alpha:.2f}  (R^2={r2_pl:.3f})")
    print(f"   Mass:  S ~ boundary^{alpha_m:.2f}  (R^2={r2_plm:.3f})")
    if alpha > 0.5 and r2_pl > 0.7:
        print(f"   ==> AREA LAW SUPPORTED in free space")
    elif alpha > 0 and r2_pl > 0.5:
        print(f"   ==> WEAK AREA LAW (sub-linear growth)")
    elif alpha < 0:
        print(f"   ==> ENTROPY SATURATES (sub-area-law)")

    print(f"\n2. VOLUME INDEPENDENCE TEST (Experiment C, fixed boundary={bnd_const}):")
    if cv < 0.25 and r2_vc < 0.5:
        print(f"   S roughly constant (CV={cv:.3f}) despite volume changes")
        print(f"   ==> AREA LAW CONFIRMED: entropy depends on boundary, not volume")
    elif r2_vc > 0.7:
        print(f"   S grows with volume (R^2={r2_vc:.3f})")
        print(f"   ==> VOLUME LAW component present")
    else:
        print(f"   Intermediate: CV={cv:.3f}, R^2_vol={r2_vc:.3f}")
        if cv < 0.4:
            print(f"   ==> PREDOMINANTLY AREA LAW with some volume dependence")
        else:
            print(f"   ==> MIXED SCALING regime")

    deltas = [data_mass[i][2] - data_free[i][2] for i in range(len(heights))]
    delta_mean = sum(deltas) / len(deltas)
    print(f"\n3. GRAVITATIONAL EFFECT:")
    print(f"   Mean delta_S (mass - free) = {delta_mean:.4f}")
    if delta_mean > 0.1:
        print(f"   Mass INCREASES entanglement entropy")
        print(f"   ==> Gravitational field enhances boundary correlations")
        print(f"   ==> Consistent with Bekenstein-Hawking: more mass -> more entropy")
    elif delta_mean < -0.1:
        print(f"   Mass DECREASES entanglement entropy (gravitational focusing)")
    else:
        print(f"   Negligible mass effect")

    print()


if __name__ == "__main__":
    main()
