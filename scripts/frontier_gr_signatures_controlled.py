#!/usr/bin/env python3
"""Controlled GR-signature tests: frozen-source vs Poisson-solved fields.

Review-flagged issues addressed:
  1. Tests 1-2 (time dilation, WEP) are "exact by construction" for ANY 1/r
     field in S = L(1-f). They test the action's structure, not self-consistency.
     This script labels them explicitly and runs a FROZEN-SOURCE CONTROL.
  2. The factor-of-2 light bending requires an extra spatial metric factor
     (1-f) on path length that is NOT independently derived from the axioms.
  3. A frozen (hand-crafted) 1/r field is tested alongside the Poisson-solved
     field. If results match, the signatures are GEOMETRIC (from the action
     form) not from dynamic self-consistency.

The control: hand-craft f(r) = A/r (analytic 1/r, no Poisson solve) and run
the same GR tests. Compare results to the Poisson-solved field.

PStack experiment: emergent-gr-signatures-controlled
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ===========================================================================
# Field generators
# ===========================================================================

def solve_poisson_sparse(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0) -> np.ndarray:
    """Solve 3D Poisson equation with Dirichlet BC using sparse solver."""
    M = N - 2
    n_interior = M * M * M

    def idx(i, j, k):
        return i * M * M + j * M + k

    rows, cols, vals = [], [], []
    rhs = np.zeros(n_interior)
    mx, my, mz = mass_pos
    mi, mj, mk = mx - 1, my - 1, mz - 1

    for i in range(M):
        for j in range(M):
            for k in range(M):
                c = idx(i, j, k)
                rows.append(c); cols.append(c); vals.append(-6.0)
                if i > 0:
                    rows.append(c); cols.append(idx(i-1, j, k)); vals.append(1.0)
                if i < M - 1:
                    rows.append(c); cols.append(idx(i+1, j, k)); vals.append(1.0)
                if j > 0:
                    rows.append(c); cols.append(idx(i, j-1, k)); vals.append(1.0)
                if j < M - 1:
                    rows.append(c); cols.append(idx(i, j+1, k)); vals.append(1.0)
                if k > 0:
                    rows.append(c); cols.append(idx(i, j, k-1)); vals.append(1.0)
                if k < M - 1:
                    rows.append(c); cols.append(idx(i, j, k+1)); vals.append(1.0)
                if i == mi and j == mj and k == mk:
                    rhs[c] = -mass_strength

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))
    phi_interior = spsolve(A, rhs)

    field = np.zeros((N, N, N))
    for i in range(M):
        for j in range(M):
            for k in range(M):
                field[i+1, j+1, k+1] = phi_interior[idx(i, j, k)]
    return field


def solve_poisson_jacobi(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0,
                         max_iter: int = 8000, tol: float = 1e-7) -> np.ndarray:
    """Fallback Jacobi solver."""
    field = np.zeros((N, N, N))
    source = np.zeros((N, N, N))
    mx, my, mz = mass_pos
    source[mx, my, mz] = mass_strength
    for _ in range(max_iter):
        new = np.zeros_like(field)
        new[1:-1, 1:-1, 1:-1] = (
            field[2:, 1:-1, 1:-1] + field[:-2, 1:-1, 1:-1] +
            field[1:-1, 2:, 1:-1] + field[1:-1, :-2, 1:-1] +
            field[1:-1, 1:-1, 2:] + field[1:-1, 1:-1, :-2] +
            source[1:-1, 1:-1, 1:-1]
        ) / 6.0
        if np.max(np.abs(new - field)) < tol:
            field = new
            break
        field = new
    return field


def solve_poisson(N: int, mass_pos: tuple[int, int, int],
                  mass_strength: float = 1.0) -> np.ndarray:
    if HAS_SCIPY and N <= 50:
        return solve_poisson_sparse(N, mass_pos, mass_strength)
    return solve_poisson_jacobi(N, mass_pos, mass_strength)


def make_frozen_1_over_r(N: int, mass_pos: tuple[int, int, int],
                         amplitude: float) -> np.ndarray:
    """Hand-craft a 1/r field centered at mass_pos. No Poisson solve.

    f(x) = amplitude / max(|x - mass_pos|, 1)

    This is NOT a solution of any PDE on the lattice -- it is a static,
    externally imposed field. If the GR signature tests give the same
    results for this frozen field as for the Poisson-solved field, then
    the signatures come from the ACTION STRUCTURE, not from self-consistency.
    """
    mx, my, mz = mass_pos
    field = np.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                r = math.sqrt((i - mx)**2 + (j - my)**2 + (k - mz)**2)
                r = max(r, 1.0)
                field[i, j, k] = amplitude / r
    return field


def make_frozen_1_over_r2(N: int, mass_pos: tuple[int, int, int],
                          amplitude: float) -> np.ndarray:
    """Hand-craft a 1/r^2 field (WRONG radial dependence for gravity).

    This tests whether the GR signatures depend on the field being 1/r
    specifically, or work for any radially decaying field.
    """
    mx, my, mz = mass_pos
    field = np.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                r = math.sqrt((i - mx)**2 + (j - my)**2 + (k - mz)**2)
                r = max(r, 1.0)
                field[i, j, k] = amplitude / (r * r)
    return field


# ===========================================================================
# Phase accumulation along rays
# ===========================================================================

def accumulate_phase_along_ray(field: np.ndarray, k: float,
                               mid: int, y: int, z: int) -> float:
    """Phase = k * sum_x [1 - f(x, y, z)] (valley-linear action)."""
    N = field.shape[0]
    phase = 0.0
    for x in range(1, N - 1):
        phase += k * (1.0 - field[x, y, z])
    return phase


def accumulate_phase_metric_corrected(field: np.ndarray, k: float,
                                      mid: int, y: int, z: int) -> float:
    """Phase with spatial metric correction: k * sum [(1-f)^2]."""
    N = field.shape[0]
    phase = 0.0
    for x in range(1, N - 1):
        f = field[x, y, z]
        phase += k * (1.0 - f) ** 2
    return phase


# ===========================================================================
# Test 1: Gravitational time dilation (with control)
# ===========================================================================

def test_time_dilation(N: int, field: np.ndarray, field_label: str,
                       k: float) -> dict:
    """Test time dilation: phase accumulation rate = k*(1-f).

    EXACT BY CONSTRUCTION: For ANY field f in S = L(1-f), phase deficit
    equals k * sum(f). This is an identity of the action, not a prediction.

    The non-trivial content is that (1-f) matches GR's g_00^{1/2} when
    f = 2GM/rc^2, but that matching is an INTERPRETATION, not a test.
    """
    mid = N // 2
    b_values = list(range(2, min(mid - 2, 13)))
    z = mid

    b_ref = b_values[-1]
    phase_ref = accumulate_phase_along_ray(field, k, mid, mid + b_ref, z)

    ratios = []
    for b in b_values:
        y = mid + b
        phase_b = accumulate_phase_along_ray(field, k, mid, y, z)
        delta_phase = phase_b - phase_ref

        pred_delta = 0.0
        for x in range(1, N - 1):
            pred_delta += k * (field[x, mid + b_ref, z] - field[x, y, z])

        ratio = delta_phase / pred_delta if abs(pred_delta) > 1e-15 else float('nan')
        if not math.isnan(ratio):
            ratios.append(ratio)

    mean_ratio = np.mean(ratios) if ratios else float('nan')
    std_ratio = np.std(ratios) if ratios else float('nan')

    return {
        'label': field_label,
        'mean_ratio': mean_ratio,
        'std_ratio': std_ratio,
        'n_points': len(ratios),
        'exact_by_construction': True,
    }


# ===========================================================================
# Test 2: Weak equivalence principle (with control)
# ===========================================================================

def test_wep(N: int, field: np.ndarray, field_label: str) -> dict:
    """Test WEP: deflection independent of k.

    EXACT BY CONSTRUCTION: deflection = dS/db = d/db sum(1-f), which is
    k-independent for ANY field f. This is an identity of S = L(1-f).
    """
    mid = N // 2
    k_values = [2.0, 4.0, 6.0, 8.0, 12.0, 16.0]
    z = mid
    b_test = 4
    y_b = mid + b_test
    y_b1 = mid + b_test + 1

    deflections = []
    for k in k_values:
        phase_b = accumulate_phase_along_ray(field, k, mid, y_b, z)
        phase_b1 = accumulate_phase_along_ray(field, k, mid, y_b1, z)
        d_phase = phase_b1 - phase_b
        deflection = d_phase / k
        deflections.append(deflection)

    mean_defl = np.mean(deflections)
    std_defl = np.std(deflections)
    spread = std_defl / abs(mean_defl) * 100 if abs(mean_defl) > 1e-15 else float('inf')

    return {
        'label': field_label,
        'mean_deflection': mean_defl,
        'spread_pct': spread,
        'n_k_values': len(k_values),
        'exact_by_construction': True,
    }


# ===========================================================================
# Test 3: Light deflection factor of 2 (with control + caveats)
# ===========================================================================

def test_light_deflection(N: int, field: np.ndarray, field_label: str,
                          k: float) -> dict:
    """Test factor-of-2 in light bending.

    This test compares two ACTION CHOICES:
      - Time-dilation only: S = L*(1-f)        => deflection ~ d/db sum(f)
      - Full metric:        S_eff = L*(1-f)^2  => deflection ~ d/db sum(2f)

    The factor-of-2 is a CONSEQUENCE of choosing S_eff = L*(1-f)^2.
    It is NOT derived from the axioms, which give S = L*(1-f).
    The spatial metric factor requires independent justification.
    """
    mid = N // 2
    b_values = list(range(2, min(mid - 3, 12)))
    z = mid

    ratios = []
    for b in b_values:
        y_b = mid + b
        y_b1 = mid + b + 1
        if y_b1 >= N - 1:
            continue

        phase_td_b = accumulate_phase_along_ray(field, k, mid, y_b, z)
        phase_td_b1 = accumulate_phase_along_ray(field, k, mid, y_b1, z)
        defl_td = phase_td_b1 - phase_td_b

        phase_fm_b = accumulate_phase_metric_corrected(field, k, mid, y_b, z)
        phase_fm_b1 = accumulate_phase_metric_corrected(field, k, mid, y_b1, z)
        defl_fm = phase_fm_b1 - phase_fm_b

        ratio = defl_fm / defl_td if abs(defl_td) > 1e-15 else float('nan')
        if not math.isnan(ratio):
            ratios.append(ratio)

    mean_ratio = np.mean(ratios) if ratios else float('nan')
    std_ratio = np.std(ratios) if ratios else float('nan')

    return {
        'label': field_label,
        'mean_ratio': mean_ratio,
        'std_ratio': std_ratio,
        'n_points': len(ratios),
        'conditional': True,
        'condition': 'Requires spatial metric factor (1-f) on path length, not derived from axioms',
    }


# ===========================================================================
# Test 4: Static vs dynamic comparison
# ===========================================================================

def compare_fields(N: int, field_poisson: np.ndarray,
                   field_frozen: np.ndarray) -> dict:
    """Compare Poisson-solved field to frozen 1/r field.

    If GR signatures match for both, the signatures are GEOMETRIC
    (from the action structure) not from dynamic self-consistency.

    What WOULD distinguish them: self-consistent iteration. A frozen
    field does not respond to the propagator's density distribution.
    """
    mid = N // 2

    # Radial profile comparison
    r_vals = []
    poisson_vals = []
    frozen_vals = []
    for dr in range(2, min(mid - 2, 13)):
        y = mid + dr
        if y >= N - 1:
            break
        r_vals.append(dr)
        poisson_vals.append(field_poisson[mid, y, mid])
        frozen_vals.append(field_frozen[mid, y, mid])

    r_arr = np.array(r_vals, dtype=float)
    p_arr = np.array(poisson_vals)
    f_arr = np.array(frozen_vals)

    # Fit power law exponents
    results = {}
    for label, arr in [('poisson', p_arr), ('frozen', f_arr)]:
        mask = (np.abs(arr) > 1e-30) & (r_arr > 1)
        if mask.sum() >= 3:
            lnr = np.log(r_arr[mask])
            lnphi = np.log(np.abs(arr[mask]))
            coeffs = np.polyfit(lnr, lnphi, 1)
            beta = -coeffs[0]
            fit = coeffs[0] * lnr + coeffs[1]
            ss_res = np.sum((lnphi - fit)**2)
            ss_tot = np.sum((lnphi - np.mean(lnphi))**2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        else:
            beta = float('nan')
            r2 = float('nan')
        results[label] = {'beta': beta, 'r2': r2}

    # Laplacian check: does the frozen field satisfy Poisson?
    lap_vals = []
    for dr in [3, 5, 7]:
        if mid + dr + 1 >= N - 1:
            continue
        x0, y0, z0 = mid, mid + dr, mid
        lap = (field_frozen[x0+1,y0,z0] + field_frozen[x0-1,y0,z0]
               + field_frozen[x0,y0+1,z0] + field_frozen[x0,y0-1,z0]
               + field_frozen[x0,y0,z0+1] + field_frozen[x0,y0,z0-1]
               - 6*field_frozen[x0,y0,z0])
        lap_vals.append((dr, lap))

    results['laplacian_residuals'] = lap_vals
    return results


# ===========================================================================
# Main
# ===========================================================================

def main():
    t_total = time.time()

    print("=" * 80)
    print("CONTROLLED GR-SIGNATURE TESTS")
    print("Frozen-source control to separate geometry from self-consistency")
    print("=" * 80)
    print()
    print("MOTIVATION: The review flagged that tests 1-2 are 'exact by")
    print("construction' -- they test identities of S = L(1-f), not")
    print("independent predictions from self-consistency. This script adds")
    print("a FROZEN-SOURCE CONTROL: a hand-crafted 1/r field (not Poisson-")
    print("solved) to prove the signatures are geometric, not dynamic.")
    print()

    N = 31
    k = 4.0
    mid = N // 2
    mass_pos = (mid, mid, mid)

    # -------------------------------------------------------------------
    # Generate fields
    # -------------------------------------------------------------------
    print("=" * 80)
    print("FIELD GENERATION")
    print("=" * 80)
    print()

    # 1. Poisson-solved field
    mass_strength = 1.0
    field_poisson = solve_poisson(N, mass_pos, mass_strength)
    f_poisson_at_r5 = field_poisson[mid, mid + 5, mid]

    # 2. Frozen 1/r field, matched in amplitude to Poisson at r=5
    frozen_amplitude = f_poisson_at_r5 * 5.0
    field_frozen = make_frozen_1_over_r(N, mass_pos, frozen_amplitude)

    # 3. Frozen 1/r^2 field (wrong radial dependence)
    frozen_amp_r2 = f_poisson_at_r5 * 25.0
    field_wrong = make_frozen_1_over_r2(N, mass_pos, frozen_amp_r2)

    print(f"Lattice: N={N}, mass at ({mid},{mid},{mid})")
    print(f"Poisson field at r=5: {f_poisson_at_r5:.8f}")
    print(f"Frozen 1/r amplitude: {frozen_amplitude:.8f}")
    print(f"Frozen 1/r^2 amplitude: {frozen_amp_r2:.8f}")
    print()

    # Radial profiles
    print("Radial profiles:")
    print(f"{'r':>4s} {'Poisson':>12s} {'Frozen 1/r':>12s} {'Frozen 1/r2':>12s}")
    print("-" * 45)
    for r in [2, 3, 4, 5, 7, 10]:
        if mid + r >= N - 1:
            continue
        fp = field_poisson[mid, mid + r, mid]
        ff = field_frozen[mid, mid + r, mid]
        fw = field_wrong[mid, mid + r, mid]
        print(f"{r:>4d} {fp:>12.8f} {ff:>12.8f} {fw:>12.8f}")
    print()

    # -------------------------------------------------------------------
    # TEST 1: Time dilation -- EXACT BY CONSTRUCTION
    # -------------------------------------------------------------------
    print("=" * 80)
    print("TEST 1: GRAVITATIONAL TIME DILATION")
    print("  STATUS: EXACT BY CONSTRUCTION")
    print("  For ANY field f, phase deficit = k * sum(f). This is an")
    print("  identity of S = L(1-f), not a test of self-consistency.")
    print("=" * 80)
    print()

    fields = [
        (field_poisson, "Poisson-solved"),
        (field_frozen, "Frozen 1/r"),
        (field_wrong, "Frozen 1/r^2"),
    ]

    td_results = []
    for field, label in fields:
        result = test_time_dilation(N, field, label, k)
        td_results.append(result)

    print(f"{'Field':>18s} {'ratio':>10s} {'std':>10s} {'status':>20s}")
    print("-" * 62)
    for r in td_results:
        status = "EXACT (by construction)" if abs(r['mean_ratio'] - 1.0) < 0.001 else "DEVIATION"
        print(f"{r['label']:>18s} {r['mean_ratio']:>10.6f} {r['std_ratio']:>10.2e} {status:>20s}")

    print()
    print("INTERPRETATION: ALL fields give ratio = 1.000 because this is an")
    print("identity of the action S = L(1-f). The frozen field gives the SAME")
    print("result as Poisson-solved. This confirms the signature is GEOMETRIC,")
    print("not from self-consistency.")
    print()

    # -------------------------------------------------------------------
    # TEST 2: WEP -- EXACT BY CONSTRUCTION
    # -------------------------------------------------------------------
    print("=" * 80)
    print("TEST 2: WEAK EQUIVALENCE PRINCIPLE")
    print("  STATUS: EXACT BY CONSTRUCTION")
    print("  Deflection = dS/db = d/db sum(1-f) is k-independent for ANY f.")
    print("  This is an identity of S = L(1-f), not a test of dynamics.")
    print("=" * 80)
    print()

    wep_results = []
    for field, label in fields:
        result = test_wep(N, field, label)
        wep_results.append(result)

    print(f"{'Field':>18s} {'deflection':>14s} {'spread%':>10s} {'status':>20s}")
    print("-" * 66)
    for r in wep_results:
        status = "EXACT (by construction)" if r['spread_pct'] < 0.01 else f"spread={r['spread_pct']:.4f}%"
        print(f"{r['label']:>18s} {r['mean_deflection']:>+14.8f} {r['spread_pct']:>10.4f} {status:>20s}")

    print()
    print("INTERPRETATION: ALL fields give zero spread because deflection = dS/db")
    print("and S = sum(1-f) is k-independent by construction. The frozen field")
    print("confirms this is geometric, not dynamic.")
    print()

    # -------------------------------------------------------------------
    # TEST 3: Light deflection factor of 2 -- CONDITIONAL
    # -------------------------------------------------------------------
    print("=" * 80)
    print("TEST 3: LIGHT DEFLECTION FACTOR OF 2")
    print("  STATUS: CONDITIONAL")
    print("  This tests: IF S_eff = L*(1-f)^2 (spatial metric included),")
    print("  THEN deflection doubles. The spatial metric factor is NOT")
    print("  derived from the axioms.")
    print("=" * 80)
    print()
    print("What IS derived:  S = L*(1-f)  [valley-linear action from axioms]")
    print("What is ASSUMED:  S_eff = L*(1-f)^2  [spatial metric adds another (1-f)]")
    print("What is TESTED:   Does (1-f)^2 give 2x deflection? (Yes, by algebra.)")
    print()

    ld_results = []
    for field, label in fields:
        result = test_light_deflection(N, field, label, k)
        ld_results.append(result)

    print(f"{'Field':>18s} {'FM/TD ratio':>12s} {'std':>10s} {'near 2.0?':>12s}")
    print("-" * 56)
    for r in ld_results:
        near2 = "YES" if abs(r['mean_ratio'] - 2.0) < 0.05 else f"dev={abs(r['mean_ratio']-2.0):.4f}"
        print(f"{r['label']:>18s} {r['mean_ratio']:>12.6f} {r['std_ratio']:>10.4f} {near2:>12s}")

    print()
    print("INTERPRETATION: ALL fields give ratio ~ 2.0 because:")
    print("  (1-f)^2 ~ 1 - 2f + f^2, so the phase deficit doubles (to leading")
    print("  order in f). This is ALGEBRA, not physics. The factor-of-2 is")
    print("  guaranteed for ANY field once you choose S_eff = L*(1-f)^2.")
    print()
    print("What WOULD make this non-trivial: an independent derivation showing")
    print("that the path-sum propagator naturally produces (1-f)^2 as the")
    print("effective action, rather than (1-f). This is NOT YET DONE.")
    print()

    # -------------------------------------------------------------------
    # TEST 4: Static vs dynamic field comparison
    # -------------------------------------------------------------------
    print("=" * 80)
    print("TEST 4: STATIC vs DYNAMIC FIELD COMPARISON")
    print("  What distinguishes Poisson-solved from frozen 1/r?")
    print("=" * 80)
    print()

    comp = compare_fields(N, field_poisson, field_frozen)

    print("Radial decay exponents:")
    print(f"  Poisson-solved: beta = {comp['poisson']['beta']:.4f} (R^2 = {comp['poisson']['r2']:.4f})")
    print(f"  Frozen 1/r:     beta = {comp['frozen']['beta']:.4f} (R^2 = {comp['frozen']['r2']:.4f})")
    print()

    print("Laplacian of frozen field (should be nonzero if NOT a Poisson solution):")
    for dr, lap in comp['laplacian_residuals']:
        print(f"  r={dr}: nabla^2 f_frozen = {lap:.6e}")

    print()
    print("KEY DIFFERENCE: The Poisson-solved field satisfies nabla^2 f = -delta")
    print("(Laplacian vanishes away from source). The frozen 1/r field does NOT")
    print("satisfy Poisson on the lattice (nonzero Laplacian residual).")
    print()
    print("For the GR signature tests (1-3), this difference is IRRELEVANT:")
    print("the signatures depend only on f appearing in S = L(1-f), not on")
    print("what equation f satisfies.")
    print()
    print("What DOES require Poisson: self-consistent iteration, where the field")
    print("is sourced by the propagator's own density rho = |psi|^2. Only the")
    print("Poisson field achieves this loop closure (tested in the separate")
    print("self-consistency script).")
    print()

    # -------------------------------------------------------------------
    # TEST 5: Wrong radial dependence -- what changes
    # -------------------------------------------------------------------
    print("=" * 80)
    print("TEST 5: WRONG RADIAL DEPENDENCE (1/r^2 FIELD)")
    print("  Tests whether GR signatures depend on the 1/r profile")
    print("=" * 80)
    print()

    # For 1/r^2 field, the GR tests still give the same structural results
    # (ratio=1 for time dilation, zero spread for WEP, ratio=2 for factor-of-2)
    # because these are properties of the ACTION, not the field shape.

    print("Time dilation for 1/r^2 field:")
    td_wrong = test_time_dilation(N, field_wrong, "Frozen 1/r^2", k)
    print(f"  Ratio: {td_wrong['mean_ratio']:.6f} (1.0 = exact by construction)")

    print()
    print("WEP for 1/r^2 field:")
    wep_wrong = test_wep(N, field_wrong, "Frozen 1/r^2")
    print(f"  Spread: {wep_wrong['spread_pct']:.6f}% (0.0 = exact by construction)")

    print()
    print("Factor-of-2 for 1/r^2 field:")
    ld_wrong = test_light_deflection(N, field_wrong, "Frozen 1/r^2", k)
    print(f"  FM/TD ratio: {ld_wrong['mean_ratio']:.6f} (2.0 = algebraic identity)")

    print()
    print("CONCLUSION: Even with a 1/r^2 field (wrong for gravity), ALL three")
    print("GR signatures hold identically. This PROVES these signatures test")
    print("the action structure S = L(1-f), not the field's radial profile.")
    print()
    print("What DOES depend on 1/r: the FORCE LAW. A 1/r potential gives 1/r^2")
    print("force (Newtonian gravity). A 1/r^2 potential gives 1/r^3 force")
    print("(non-physical). The force law is tested by self-consistency and")
    print("orbital dynamics, NOT by the GR-signature tests.")
    print()

    # ===================================================================
    # FINAL SUMMARY TABLE
    # ===================================================================
    elapsed = time.time() - t_total

    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print()
    print(f"{'Test':>30s} | {'Status':>25s} | {'What it tests':>35s}")
    print("-" * 96)
    print(f"{'Time dilation':>30s} | {'EXACT BY CONSTRUCTION':>25s} | {'Action structure S=L(1-f)':>35s}")
    print(f"{'WEP (k-independence)':>30s} | {'EXACT BY CONSTRUCTION':>25s} | {'Action structure S=L(1-f)':>35s}")
    print(f"{'Factor-of-2 deflection':>30s} | {'CONDITIONAL':>25s} | {'Algebra of (1-f)^2, IF assumed':>35s}")
    print(f"{'Conformal metric':>30s} | {'STRUCTURAL':>25s} | {'Action implies g_ij = (1-f) d_ij':>35s}")
    print()

    print("=" * 80)
    print("BOUNDED CLAIMS")
    print("=" * 80)
    print()
    print("WHAT IS TRUE:")
    print("  1. The action S = L(1-f) produces time dilation and WEP as")
    print("     IDENTITIES. Any field f in this action gives these results.")
    print("     The non-trivial content is that f = s/r (from Poisson)")
    print("     makes (1-f) match the Schwarzschild time-time component.")
    print()
    print("  2. IF the spatial metric factor is included (S_eff = L*(1-f)^2),")
    print("     THEN light deflection doubles. This is algebra, not a prediction.")
    print()
    print("  3. The frozen-source control confirms these are GEOMETRIC signatures")
    print("     of the action form, not consequences of self-consistent dynamics.")
    print()
    print("WHAT IS NOT YET SHOWN:")
    print("  1. Why the spatial metric should contribute an additional (1-f)")
    print("     factor. This requires deriving the effective action from the")
    print("     full path-sum propagator structure, which is not done.")
    print()
    print("  2. That self-consistency adds any GR content beyond what the")
    print("     action structure already gives. The frozen field gives all")
    print("     the same signatures without self-consistency.")
    print()
    print("  3. Any connection to the FULL GR (nonlinear regime, frame")
    print("     dragging, gravitational waves). Only weak-field, static,")
    print("     spherically symmetric case is addressed.")
    print()
    print("WHAT WOULD CONSTITUTE A GENUINE PREDICTION:")
    print("  - Deriving the spatial metric factor from the propagator")
    print("  - Showing self-consistent dynamics produces effects BEYOND")
    print("    what a frozen field gives (e.g., back-reaction)")
    print("  - Reproducing a GR effect that is NOT an identity of S = L(1-f)")
    print("    or S = L(1-f)^2 (e.g., precession, gravitational redshift")
    print("    of spectral lines from the propagator)")
    print()
    print(f"Total runtime: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
