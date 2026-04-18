"""Historical boundary-transfer entropy diagnostic on the event-network DAG.

This script is preserved as a diagnostic/historical probe only.

It does NOT construct a canonical subsystem reduced density matrix on a single
many-body state. Instead it builds a source-to-cut transfer matrix:
- Region A = source boundary (x=0), region B = cut boundary (x=cut_x).
- Propagate from EACH source y_in on x=0 independently through the DAG.
- Collect amplitudes M[y_cut, y_in] at the cut boundary.
- Form
      rho_B(y, y') = sum_{y_in} M(y, y_in) * conj(M(y', y_in))
  which traces over source labels in this transfer construction.
- S_vN = -Tr(rho_B ln rho_B)

Diagnostic question: does this transfer entropy track boundary size more
closely than region volume on the audited surface?

Eigensolver: proper complex Hermitian Jacobi diagonalization using
complex Givens rotations (phase-factored 2x2 subproblem).

Pure-Python implementation (no numpy dependency).
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
# ---------------------------------------------------------------------------

Matrix = list[list[complex]]


def mat_zeros(n: int) -> Matrix:
    return [[0.0 + 0j for _ in range(n)] for _ in range(n)]


def hermitian_eigenvalues(h: Matrix, max_iter: int = 500) -> list[float]:
    """Eigenvalues of a complex Hermitian matrix via Jacobi rotations.

    Uses complex Givens rotations: for off-diagonal h[p][q] = |z|*exp(i*phi),
    factor out the phase, solve the real 2x2 problem, then apply the
    unitary rotation U that zeroes h[p][q] and h[q][p].
    """
    n = len(h)
    if n == 0:
        return []
    if n == 1:
        return [h[0][0].real]

    # Work on a copy
    a: Matrix = [[h[i][j] for j in range(n)] for i in range(n)]

    # Force exact Hermitian symmetry
    for i in range(n):
        a[i][i] = complex(a[i][i].real, 0.0)
        for j in range(i + 1, n):
            avg = 0.5 * (a[i][j] + a[j][i].conjugate())
            a[i][j] = avg
            a[j][i] = avg.conjugate()

    for _sweep in range(max_iter):
        # Find largest off-diagonal magnitude
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

        # Complex Givens rotation for Hermitian 2x2 subproblem
        # a[p][q] = z = |z| * exp(i*phi)
        z = a[p][q]
        mag_z = abs(z)
        if mag_z < 1e-30:
            continue

        # Phase factor: e^{-i*phi} rotates z to real
        phase = z / mag_z  # exp(i*phi)
        phase_conj = phase.conjugate()  # exp(-i*phi)

        # Real 2x2 problem: [[app, |z|], [|z|, aqq]]
        app = a[p][p].real
        aqq = a[q][q].real
        diff = app - aqq

        if abs(diff) < 1e-30:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2.0 * mag_z, diff)

        c = math.cos(theta)
        s = math.sin(theta)

        # The unitary rotation matrix U acts as:
        #   row p: c * row_p + s * phase_conj * row_q
        #   row q: -s * phase * row_p + c * row_q
        # And similarly for columns.

        # Update rows/columns for all i != p, q
        for i in range(n):
            if i == p or i == q:
                continue
            aip = a[i][p]
            aiq = a[i][q]
            a[i][p] = c * aip + s * phase_conj * aiq
            a[p][i] = a[i][p].conjugate()
            a[i][q] = -s * phase * aip + c * aiq
            a[q][i] = a[i][q].conjugate()

        # Update diagonal elements
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
# Core: build propagator matrix M[y_cut, y_source]
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
# Diagnostics
# ---------------------------------------------------------------------------


def rho_diagnostics(rho: Matrix) -> dict[str, float]:
    """Compute diagnostic quantities for the density matrix."""
    n = len(rho)
    if n == 0:
        return {"trace": 0.0, "max_abs": 0.0, "max_imag_ratio": 0.0}

    tr = sum(rho[i][i].real for i in range(n))
    max_abs = 0.0
    max_imag = 0.0
    for i in range(n):
        for j in range(n):
            a = abs(rho[i][j])
            if a > max_abs:
                max_abs = a
            im = abs(rho[i][j].imag)
            if im > max_imag:
                max_imag = im

    # Check Hermiticity: max |rho[i][j] - conj(rho[j][i])|
    max_herm_err = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            err = abs(rho[i][j] - rho[j][i].conjugate())
            if err > max_herm_err:
                max_herm_err = err

    ratio = max_imag / max_abs if max_abs > 1e-30 else 0.0
    return {
        "trace": tr,
        "max_abs": max_abs,
        "max_imag": max_imag,
        "max_imag_ratio": ratio,
        "hermiticity_error": max_herm_err,
    }


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_experiment(
    height: int,
    width: int,
    cut_x: int,
    postulates: RulePostulates,
    persistent_nodes: frozenset[tuple[int, int]] = frozenset(),
) -> dict[str, Any]:
    """Run a single bipartition experiment.

    Returns dict with: boundary_size, volume_A, S_vN, rank, n_sources,
    max_imag_ratio, trace.
    """
    nodes = build_rectangular_nodes(width=width, height=height)
    rule = derive_local_rule(persistent_nodes=persistent_nodes, postulates=postulates)
    node_field = derive_node_field(nodes, rule)

    # Sources: all y-positions at x=0
    sources = sorted([(0, y) for (x, y) in nodes if x == 0], key=lambda n: n[1])
    # Cut boundary: all y-positions at x=cut_x
    y_cut_positions = sorted(y for (x, y) in nodes if x == cut_x)

    M = build_propagator_matrix(nodes, sources, rule, node_field, cut_x, y_cut_positions)
    rho = build_rho_B(M)

    diag = rho_diagnostics(rho)

    # Normalize rho
    tr = diag["trace"]
    n = len(rho)
    if tr > 1e-30:
        for i in range(n):
            for j in range(n):
                rho[i][j] /= tr

    eigenvalues = hermitian_eigenvalues(rho)
    s_vn = von_neumann_entropy(eigenvalues)
    rank = sum(1 for e in eigenvalues if e > 1e-10)

    boundary_size = len(y_cut_positions)
    volume_a = sum(1 for (x, _) in nodes if x < cut_x)

    return {
        "boundary_size": boundary_size,
        "volume_A": volume_a,
        "S_vN": s_vn,
        "rank": rank,
        "n_sources": len(sources),
        "n_cut": len(y_cut_positions),
        "max_imag_ratio": diag["max_imag_ratio"],
        "hermiticity_error": diag["hermiticity_error"],
        "trace_before_norm": diag["trace"],
    }


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
    print("BOUNDARY-TRANSFER ENTROPY DIAGNOSTIC ON EVENT-NETWORK DAG")
    print("=" * 80)
    print()
    print("Method: source-to-cut transfer construction")
    print("  Region A = source boundary (x=0), region B = cut boundary (x=cut_x)")
    print("  Propagate from EACH source y_in independently to build M[y_cut, y_in]")
    print("  rho_B = M @ M^dagger  (traces over source labels in this construction)")
    print("  S_vN = -Tr(rho_B ln rho_B)")
    print("  Historical note: this is not the live Dirac-sea boundary-law package.")
    print()
    print("Eigensolver: complex Hermitian Jacobi with proper Givens rotations")
    print()

    width = 20
    cut_x = 10

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
    # ===================================================================
    heights = [3, 4, 5, 6, 7, 8, 9, 10, 12, 14]

    print(f"EXPERIMENT A: Vary boundary size")
    print(f"  width={width}, cut_x={cut_x}")
    print()

    header = (f"{'h':>3} {'bnd':>4} {'vol':>5} {'nsrc':>5} "
              f"{'S_free':>10} {'rk_f':>4} {'S_mass':>10} {'rk_m':>4} "
              f"{'dS':>8} {'Im/|rho|':>8}")
    print(header)
    print("-" * len(header))

    data_free: list[dict] = []
    data_mass: list[dict] = []

    for h in heights:
        rf = run_experiment(h, width, cut_x, postulates)
        data_free.append(rf)

        rm = run_experiment(h, width, cut_x, postulates, mass_nodes)
        data_mass.append(rm)

        print(f"{h:>3} {rf['boundary_size']:>4} {rf['volume_A']:>5} {rf['n_sources']:>5} "
              f"{rf['S_vN']:>10.6f} {rf['rank']:>4} {rm['S_vN']:>10.6f} {rm['rank']:>4} "
              f"{rm['S_vN'] - rf['S_vN']:>8.4f} {rf['max_imag_ratio']:>8.4f}")

    # Fits for free space
    bnds = [float(d["boundary_size"]) for d in data_free]
    s_f = [d["S_vN"] for d in data_free]
    vols = [float(d["volume_A"]) for d in data_free]
    s_m = [d["S_vN"] for d in data_mass]

    print("\n--- Free space fits ---")
    a_b, b_b, r2_b = linear_fit(bnds, s_f)
    print(f"  S vs boundary: slope={a_b:.5f}  R^2={r2_b:.4f}")
    a_v, b_v, r2_v = linear_fit(vols, s_f)
    print(f"  S vs volume:   slope={a_v:.6f}  R^2={r2_v:.4f}")

    log_b = [math.log(b) for b in bnds if b > 0]
    log_sf = [math.log(max(s, 1e-15)) for s, b in zip(s_f, bnds) if b > 0]
    alpha, _, r2_pl = linear_fit(log_b, log_sf)
    print(f"  Power law: S ~ bnd^{alpha:.3f}  R^2={r2_pl:.4f}")

    print("\n--- With mass fits ---")
    a_bm, _, r2_bm = linear_fit(bnds, s_m)
    print(f"  S vs boundary: slope={a_bm:.5f}  R^2={r2_bm:.4f}")
    log_sm = [math.log(max(s, 1e-15)) for s, b in zip(s_m, bnds) if b > 0]
    alpha_m, _, r2_plm = linear_fit(log_b, log_sm)
    print(f"  Power law: S ~ bnd^{alpha_m:.3f}  R^2={r2_plm:.4f}")

    # ===================================================================
    # Experiment B: Robustness -- vary cut_x at fixed height
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("EXPERIMENT B: Vary cut_x (robustness check)")
    print("=" * 80)

    fixed_h = 8
    cut_positions_b = [4, 6, 8, 10, 12, 14, 16]

    print(f"  height={fixed_h}, boundary = {2 * fixed_h + 1}\n")
    print(f"{'cut_x':>5} {'nsrc':>5} {'ncut':>5} {'S_free':>10} {'rank':>5} {'Im/|rho|':>8}")
    print("-" * 48)

    for cx in cut_positions_b:
        r = run_experiment(fixed_h, width, cx, postulates)
        print(f"{cx:>5} {r['n_sources']:>5} {r['n_cut']:>5} "
              f"{r['S_vN']:>10.6f} {r['rank']:>5} {r['max_imag_ratio']:>8.4f}")

    # ===================================================================
    # Experiment C: Fixed height, vary cut_x (volume test)
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("EXPERIMENT C: Fixed height=8, vary cut_x (constant boundary test)")
    print("=" * 80)

    fixed_h_c = 8
    cut_positions = [4, 6, 8, 10, 12, 14, 16, 18]

    print(f"  height={fixed_h_c}, boundary = {2 * fixed_h_c + 1}\n")
    print(f"{'cut_x':>5} {'vol_A':>6} {'S_free':>10} {'S_mass':>10}")
    print("-" * 40)

    s_free_c: list[float] = []
    s_mass_c: list[float] = []
    vols_c: list[float] = []

    for cx in cut_positions:
        rf = run_experiment(fixed_h_c, width, cx, postulates)
        rm = run_experiment(fixed_h_c, width, cx, postulates, mass_nodes)
        print(f"{cx:>5} {rf['volume_A']:>6} {rf['S_vN']:>10.6f} {rm['S_vN']:>10.6f}")
        s_free_c.append(rf["S_vN"])
        s_mass_c.append(rm["S_vN"])
        vols_c.append(float(rf["volume_A"]))

    bnd_const = 2 * fixed_h_c + 1
    s_mean = sum(s_free_c) / len(s_free_c)
    s_std = math.sqrt(sum((s - s_mean) ** 2 for s in s_free_c) / len(s_free_c))
    cv = s_std / s_mean if s_mean > 0 else float("inf")
    _, _, r2_vc = linear_fit(vols_c, s_free_c)

    print(f"\n  Boundary = {bnd_const} (constant)")
    print(f"  S_free: mean={s_mean:.4f}, std={s_std:.4f}, CV={cv:.3f}")
    print(f"  S_free vs volume_A: R^2={r2_vc:.4f}")

    # ===================================================================
    # Diagnostic: show rho structure for one case
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("DIAGNOSTIC: rho_B structure for height=6, cut_x=10")
    print("=" * 80)

    diag_h = 6
    nodes = build_rectangular_nodes(width=width, height=diag_h)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    nf = derive_node_field(nodes, rule)
    sources = sorted([(0, y) for (x, y) in nodes if x == 0], key=lambda n: n[1])
    y_cut = sorted(y for (x, y) in nodes if x == cut_x)

    M = build_propagator_matrix(nodes, sources, rule, nf, cut_x, y_cut)
    rho = build_rho_B(M)
    diag_info = rho_diagnostics(rho)

    print(f"  M shape: {len(M)} x {len(M[0]) if M else 0}")
    print(f"  rho_B shape: {len(rho)} x {len(rho)}")
    print(f"  Tr(rho_B) = {diag_info['trace']:.6f}")
    print(f"  max |rho[i][j]| = {diag_info['max_abs']:.6f}")
    print(f"  max |Im(rho[i][j])| = {diag_info['max_imag']:.6f}")
    print(f"  max |Im| / max |rho| = {diag_info['max_imag_ratio']:.4f}")
    print(f"  Hermiticity error = {diag_info['hermiticity_error']:.2e}")

    # Show a few rho entries
    n = len(rho)
    tr = diag_info["trace"]
    if tr > 1e-30:
        for i in range(n):
            for j in range(n):
                rho[i][j] /= tr

    print(f"\n  Sample rho_B entries (after normalization, Tr=1):")
    show_n = min(5, n)
    for i in range(show_n):
        for j in range(show_n):
            r, im = rho[i][j].real, rho[i][j].imag
            print(f"    rho[{i},{j}] = {r:+.6f} {im:+.6f}i", end="")
            if j < show_n - 1:
                print("  |", end="")
        print()

    eigs = hermitian_eigenvalues(rho)
    print(f"\n  Eigenvalues (top 10): {[f'{e:.6f}' for e in eigs[-10:]]}")
    print(f"  Sum of eigenvalues: {sum(eigs):.6f}")

    # ===================================================================
    # Summary
    # ===================================================================
    print(f"\n\n{'=' * 80}")
    print("SUMMARY AND INTERPRETATION")
    print("=" * 80)

    print(f"\n1. BOUNDARY SCALING IN THIS TRANSFER CONSTRUCTION (Experiment A):")
    print(f"   Free:  S ~ boundary^{alpha:.2f}  (R^2={r2_pl:.3f})")
    print(f"   Mass:  S ~ boundary^{alpha_m:.2f}  (R^2={r2_plm:.3f})")
    if alpha > 0.5 and r2_pl > 0.7:
        print(f"   ==> POSITIVE BOUNDARY-SCALING SIGNAL in free space")
    elif alpha > 0 and r2_pl > 0.5:
        print(f"   ==> WEAK POSITIVE BOUNDARY SCALING (sub-linear growth)")
    elif alpha < 0:
        print(f"   ==> ENTROPY SATURATES (sublinear boundary scaling)")
    else:
        print(f"   ==> INCONCLUSIVE (alpha={alpha:.2f}, R^2={r2_pl:.3f})")

    print(f"\n2. VOLUME INDEPENDENCE TEST (Experiment C, fixed boundary={bnd_const}):")
    if cv < 0.25 and r2_vc < 0.5:
        print(f"   S roughly constant (CV={cv:.3f}) despite volume changes")
        print(f"   ==> BOUNDARY-CONTROLLED: entropy does not track volume")
        if alpha < 0.1:
            print(f"   BUT: boundary scaling is flat/negative (alpha={alpha:.2f}),")
            print(f"   so this is SATURATING / SUBLINEAR, not a clean boundary-growth signal")
        else:
            print(f"   ==> Consistent with positive boundary-controlled scaling here")
    elif r2_vc > 0.7:
        print(f"   S grows with volume (R^2={r2_vc:.3f})")
        print(f"   ==> VOLUME LAW component present")
    else:
        print(f"   Intermediate: CV={cv:.3f}, R^2_vol={r2_vc:.3f}")
        print(f"   ==> MIXED SCALING regime")

    deltas = [data_mass[i]["S_vN"] - data_free[i]["S_vN"] for i in range(len(heights))]
    delta_mean = sum(deltas) / len(deltas)
    print(f"\n3. GRAVITATIONAL EFFECT:")
    print(f"   Mean delta_S (mass - free) = {delta_mean:.4f}")
    if delta_mean > 0.1:
        print(f"   Mass INCREASES entanglement entropy")
        print(f"   ==> Gravitational field enhances boundary correlations")
    elif delta_mean < -0.1:
        print(f"   Mass DECREASES entanglement entropy (gravitational focusing)")
    else:
        print(f"   Negligible mass effect (|dS| < 0.1)")

    # Imaginary part diagnostic
    mean_imag_ratio = sum(d["max_imag_ratio"] for d in data_free) / len(data_free)
    print(f"\n4. IMAGINARY PART DIAGNOSTIC:")
    print(f"   Mean max|Im(rho)|/max|rho| across Exp A = {mean_imag_ratio:.4f}")
    if mean_imag_ratio > 0.01:
        print(f"   ==> Imaginary parts are SIGNIFICANT -- complex Hermitian solver required")
    else:
        print(f"   ==> Imaginary parts negligible -- real-symmetric would suffice")

    print()


if __name__ == "__main__":
    main()
