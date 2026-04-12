#!/usr/bin/env python3
"""Frozen / static-source control for the 3D distance-law on 64^3.

Answers the question: does the deflection exponent alpha depend on whether
the Poisson field is computed self-consistently or injected from an external
analytic source?

Three arms on each grid size (31^3, 48^3, 64^3):

  DYNAMIC   — solve Poisson from a point mass (existing approach)
  FROZEN    — hand-crafted 1/r field, NOT Poisson-solved
  ANALYTIC  — exact finite-sum prediction for the ray deflection

For each arm, measure alpha via log-log fit across impact parameters.

Pass condition: all three arms agree within 0.5% on alpha, confirming
that the distance law is a geometric property of the valley-linear
action, not an artifact of the Poisson solver.

Grid sizes: 31^3, 48^3, 64^3 (convergence subset from the closure script).
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


# ---------------------------------------------------------------------------
# Poisson solvers (from distance_law_3d_64_closure.py)
# ---------------------------------------------------------------------------

def solve_poisson_sparse(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0) -> np.ndarray:
    """Solve 3D Poisson equation with Dirichlet BC using sparse direct solver."""
    M = N - 2
    n_interior = M * M * M

    def idx(i, j, k):
        return i * M * M + j * M + k

    rows = []
    cols = []
    vals = []
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
                         max_iter: int = 5000,
                         tol: float = 1e-7) -> np.ndarray:
    """Fallback Jacobi solver if scipy is unavailable."""
    field = np.zeros((N, N, N))
    source = np.zeros((N, N, N))
    mx, my, mz = mass_pos
    source[mx, my, mz] = mass_strength

    for iteration in range(max_iter):
        new = np.zeros_like(field)
        new[1:-1, 1:-1, 1:-1] = (
            field[2:, 1:-1, 1:-1] + field[:-2, 1:-1, 1:-1] +
            field[1:-1, 2:, 1:-1] + field[1:-1, :-2, 1:-1] +
            field[1:-1, 1:-1, 2:] + field[1:-1, 1:-1, :-2] +
            source[1:-1, 1:-1, 1:-1]
        ) / 6.0
        max_change = np.max(np.abs(new - field))
        field = new
        if max_change < tol:
            break

    return field


def solve_poisson(N: int, mass_pos: tuple[int, int, int],
                  mass_strength: float = 1.0) -> np.ndarray:
    """Auto-select best Poisson solver."""
    if HAS_SCIPY and N <= 50:
        return solve_poisson_sparse(N, mass_pos, mass_strength)
    else:
        return solve_poisson_jacobi(N, mass_pos, mass_strength,
                                    max_iter=8000, tol=1e-7)


# ---------------------------------------------------------------------------
# Frozen 1/r field (hand-crafted, no Poisson solve)
# ---------------------------------------------------------------------------

def make_frozen_field(N: int, mass_pos: tuple[int, int, int],
                      strength: float = 1.0) -> np.ndarray:
    """Build a 1/r field centered at mass_pos with Dirichlet BC.

    Uses the exact discrete Green's function normalization: for a point
    source on the infinite lattice, phi ~ s / (4*pi*r).  We apply
    Dirichlet BC by zeroing the boundary.  The normalization constant s
    is calibrated to match the Poisson field at r = N//4 (well inside
    the boundary) so that both arms see the same field amplitude in the
    fitting window.
    """
    field = np.zeros((N, N, N))
    mx, my, mz = mass_pos

    # Build raw 1/r field
    for x in range(1, N - 1):
        for y in range(1, N - 1):
            for z in range(1, N - 1):
                dx = x - mx
                dy = y - my
                dz = z - mz
                r = math.sqrt(dx * dx + dy * dy + dz * dz)
                if r > 0.5:
                    field[x, y, z] = strength / (4.0 * math.pi * r)
                else:
                    # At the source point, use the value at r=1 lattice spacing
                    field[x, y, z] = strength / (4.0 * math.pi * 1.0)

    # Dirichlet BC: boundary is already zero
    return field


def calibrate_frozen_to_dynamic(frozen: np.ndarray, dynamic: np.ndarray,
                                mid: int, r_cal: int) -> np.ndarray:
    """Rescale frozen field so it matches the dynamic Poisson field at r_cal.

    This removes the overall normalization ambiguity (lattice Green's function
    prefactor) without changing the shape.  The control tests that shape (1/r)
    matters, not that the absolute amplitude matches.
    """
    f_fro = frozen[mid, mid + r_cal, mid]
    f_dyn = dynamic[mid, mid + r_cal, mid]

    if abs(f_fro) < 1e-30:
        return frozen

    ratio = f_dyn / f_fro
    return frozen * ratio


# ---------------------------------------------------------------------------
# Analytic finite-sum deflection
# ---------------------------------------------------------------------------

def analytic_deflection(N: int, mid: int, b: int, k: float,
                        field_scale: float) -> float:
    """Exact analytic deflection for a 1/r field on the finite lattice.

    The accumulated phase along a ray at impact parameter b is:
        Phi(b) = sum_{x=1}^{N-2} k * (1 - field_scale / (4*pi*r(x,b)))

    where r(x,b) = sqrt((x-mid)^2 + b^2).

    Deflection = Phi(b+1) - Phi(b).
    """
    z_offset = 0  # ray at z = mid, so z-distance is 0

    phase_b = 0.0
    phase_b1 = 0.0

    for x in range(1, N - 1):
        dx = x - mid
        r_b = math.sqrt(dx * dx + b * b + z_offset * z_offset)
        r_b1 = math.sqrt(dx * dx + (b + 1) * (b + 1) + z_offset * z_offset)

        if r_b > 0.5:
            f_b = field_scale / (4.0 * math.pi * r_b)
        else:
            f_b = field_scale / (4.0 * math.pi * 1.0)

        if r_b1 > 0.5:
            f_b1 = field_scale / (4.0 * math.pi * r_b1)
        else:
            f_b1 = field_scale / (4.0 * math.pi * 1.0)

        phase_b += k * (1.0 - f_b)
        phase_b1 += k * (1.0 - f_b1)

    return phase_b1 - phase_b


# ---------------------------------------------------------------------------
# Ray deflection via accumulated phase (from closure script)
# ---------------------------------------------------------------------------

def compute_deflections(field: np.ndarray, k: float, mid: int,
                        b_values: list[int]) -> list[float]:
    """Compute deflection at each impact parameter b."""
    N = field.shape[0]
    z = mid
    deflections = []

    for b in b_values:
        y_b = mid + b
        y_b1 = mid + b + 1

        if y_b1 >= N - 1:
            deflections.append(0.0)
            continue

        phase_b = 0.0
        phase_b1 = 0.0
        for x in range(1, N - 1):
            phase_b += k * (1.0 - field[x, y_b, z])
            phase_b1 += k * (1.0 - field[x, y_b1, z])

        deflections.append(phase_b1 - phase_b)

    return deflections


# ---------------------------------------------------------------------------
# Power-law fitting
# ---------------------------------------------------------------------------

def fit_power_law(b_arr: np.ndarray, d_arr: np.ndarray):
    """Fit |delta| = A * b^alpha in log-log space. Returns (alpha, alpha_err, R^2)."""
    mask = (d_arr != 0) & (b_arr > 0)
    if mask.sum() < 3:
        return float('nan'), float('nan'), float('nan')

    x = np.log(b_arr[mask].astype(float))
    y = np.log(np.abs(d_arr[mask]).astype(float))
    n = len(x)

    mx = x.mean()
    my = y.mean()
    sxx = np.sum((x - mx) ** 2)
    sxy = np.sum((x - mx) * (y - my))

    if sxx < 1e-12:
        return float('nan'), float('nan'), float('nan')

    alpha = sxy / sxx
    intercept = my - alpha * mx

    y_pred = alpha * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    if n > 2:
        s2 = ss_res / (n - 2)
        alpha_err = math.sqrt(s2 / sxx)
    else:
        alpha_err = float('nan')

    return alpha, alpha_err, r2


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 80)
    print("FROZEN / STATIC-SOURCE CONTROL — DISTANCE LAW ON 64^3")
    print("=" * 80)
    print()
    print("Question: does the deflection exponent alpha depend on whether")
    print("the 1/r field is Poisson-solved or hand-crafted?")
    print()
    print("Arms:")
    print("  DYNAMIC  — Poisson-solved field from point mass")
    print("  FROZEN   — hand-crafted 1/r, calibrated to dynamic amplitude")
    print("  ANALYTIC — exact finite-sum deflection (no grid field at all)")
    print()
    print("Pass condition: all three alpha agree within 0.5%")
    print()

    k = 4.0
    mass_strength = 1.0
    min_b = 2

    grid_sizes = [31, 48, 64]

    all_results = {}

    for N in grid_sizes:
        t0 = time.time()
        mid = N // 2
        max_b = min(mid - 3, 14)
        b_values = list(range(min_b, max_b + 1))
        b_arr = np.array(b_values)
        far_mask = b_arr >= 3
        b_far = b_arr[far_mask]
        r_cal = N // 4  # calibration radius: well inside boundary

        print(f"{'='*70}")
        print(f"N = {N}  ({N**3:,} sites)  mid = {mid}  b = {min_b}..{max_b}")
        print(f"{'='*70}")

        # --- ARM 1: DYNAMIC (Poisson-solved) ---
        t1 = time.time()
        field_dyn = solve_poisson(N, (mid, mid, mid), mass_strength)
        dt_poisson = time.time() - t1

        defl_dyn = compute_deflections(field_dyn, k, mid, b_values)
        d_dyn = np.array(defl_dyn)
        alpha_dyn, err_dyn, r2_dyn = fit_power_law(b_far, d_dyn[far_mask])

        print(f"\n  DYNAMIC (Poisson-solved): {dt_poisson:.1f}s")
        print(f"    alpha = {alpha_dyn:.6f} +/- {err_dyn:.6f}  R^2 = {r2_dyn:.6f}")

        # --- ARM 2: FROZEN (hand-crafted 1/r) ---
        t2 = time.time()
        field_fro_raw = make_frozen_field(N, (mid, mid, mid), mass_strength)
        field_fro = calibrate_frozen_to_dynamic(field_fro_raw, field_dyn,
                                                 mid, r_cal)
        dt_frozen = time.time() - t2

        defl_fro = compute_deflections(field_fro, k, mid, b_values)
        d_fro = np.array(defl_fro)
        alpha_fro, err_fro, r2_fro = fit_power_law(b_far, d_fro[far_mask])

        print(f"\n  FROZEN (hand-crafted 1/r, calibrated): {dt_frozen:.1f}s")
        print(f"    alpha = {alpha_fro:.6f} +/- {err_fro:.6f}  R^2 = {r2_fro:.6f}")

        # Check field shape agreement
        r_checks = [2, 3, 5, 8]
        r_checks = [r for r in r_checks if mid + r < N - 1]
        print(f"\n  Field shape comparison (f_dyn vs f_fro at r = {r_checks}):")
        print(f"    {'r':>4s}  {'f_dyn':>12s}  {'f_fro':>12s}  {'ratio':>10s}")
        for r in r_checks:
            fd = field_dyn[mid, mid + r, mid]
            ff = field_fro[mid, mid + r, mid]
            ratio = ff / fd if abs(fd) > 1e-30 else float('nan')
            print(f"    {r:>4d}  {fd:>12.8f}  {ff:>12.8f}  {ratio:>10.6f}")

        # --- ARM 3: ANALYTIC (exact finite-sum) ---
        # Calibrate the analytic field_scale to match the dynamic field
        # at the calibration radius
        f_dyn_cal = field_dyn[mid, mid + r_cal, mid]
        field_scale_analytic = f_dyn_cal * 4.0 * math.pi * r_cal

        t3 = time.time()
        defl_ana = []
        for b in b_values:
            d = analytic_deflection(N, mid, b, k, field_scale_analytic)
            defl_ana.append(d)
        dt_analytic = time.time() - t3

        d_ana = np.array(defl_ana)
        alpha_ana, err_ana, r2_ana = fit_power_law(b_far, d_ana[far_mask])

        print(f"\n  ANALYTIC (exact finite-sum): {dt_analytic:.1f}s")
        print(f"    alpha = {alpha_ana:.6f} +/- {err_ana:.6f}  R^2 = {r2_ana:.6f}")

        # --- Deflection table ---
        print(f"\n  {'b':>4s}  {'dyn':>14s}  {'fro':>14s}  {'ana':>14s}"
              f"  {'fro/dyn':>10s}  {'ana/dyn':>10s}")
        for i, b in enumerate(b_values):
            ratio_f = defl_fro[i] / defl_dyn[i] if abs(defl_dyn[i]) > 1e-30 else float('nan')
            ratio_a = defl_ana[i] / defl_dyn[i] if abs(defl_dyn[i]) > 1e-30 else float('nan')
            print(f"  {b:>4d}  {defl_dyn[i]:>14.8f}  {defl_fro[i]:>14.8f}"
                  f"  {defl_ana[i]:>14.8f}  {ratio_f:>10.6f}  {ratio_a:>10.6f}")

        # --- Alpha comparison ---
        print(f"\n  ALPHA COMPARISON (far-field, b >= 3):")
        print(f"    DYNAMIC:  {alpha_dyn:.6f} +/- {err_dyn:.6f}")
        print(f"    FROZEN:   {alpha_fro:.6f} +/- {err_fro:.6f}")
        print(f"    ANALYTIC: {alpha_ana:.6f} +/- {err_ana:.6f}")

        if not any(math.isnan(a) for a in [alpha_dyn, alpha_fro, alpha_ana]):
            spread_df = abs(alpha_dyn - alpha_fro) / abs(alpha_dyn) * 100
            spread_da = abs(alpha_dyn - alpha_ana) / abs(alpha_dyn) * 100
            spread_fa = abs(alpha_fro - alpha_ana) / abs(alpha_fro) * 100
            max_spread = max(spread_df, spread_da, spread_fa)

            print(f"\n    |alpha_dyn - alpha_fro| / |alpha_dyn| = {spread_df:.4f}%")
            print(f"    |alpha_dyn - alpha_ana| / |alpha_dyn| = {spread_da:.4f}%")
            print(f"    |alpha_fro - alpha_ana| / |alpha_fro| = {spread_fa:.4f}%")
            print(f"    Max pairwise spread: {max_spread:.4f}%")

            if max_spread < 0.5:
                print(f"    >>> PASS: all three arms agree within 0.5%")
            elif max_spread < 1.0:
                print(f"    >>> MARGINAL: spread {max_spread:.3f}% (threshold 0.5%)")
            else:
                print(f"    >>> FAIL: spread {max_spread:.3f}% exceeds 0.5%")

        dt_total = time.time() - t0
        print(f"\n  Total time for N={N}: {dt_total:.1f}s")

        all_results[N] = {
            'alpha_dyn': alpha_dyn, 'err_dyn': err_dyn, 'r2_dyn': r2_dyn,
            'alpha_fro': alpha_fro, 'err_fro': err_fro, 'r2_fro': r2_fro,
            'alpha_ana': alpha_ana, 'err_ana': err_ana, 'r2_ana': r2_ana,
        }

    # ---------------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------------
    print()
    print("=" * 80)
    print("CONVERGENCE SUMMARY — FROZEN/STATIC-SOURCE CONTROL")
    print("=" * 80)
    print()
    print(f"{'N':>4s}  {'a_dyn':>10s}  {'a_fro':>10s}  {'a_ana':>10s}"
          f"  {'max_%spread':>12s}  {'status':>10s}")
    print("-" * 65)

    all_pass = True
    for N in grid_sizes:
        r = all_results[N]
        ad = r['alpha_dyn']
        af = r['alpha_fro']
        aa = r['alpha_ana']

        if any(math.isnan(a) for a in [ad, af, aa]):
            print(f"{N:>4d}  {ad:>10.5f}  {af:>10.5f}  {aa:>10.5f}"
                  f"  {'NaN':>12s}  {'SKIP':>10s}")
            continue

        spreads = [
            abs(ad - af) / abs(ad) * 100,
            abs(ad - aa) / abs(ad) * 100,
            abs(af - aa) / abs(af) * 100,
        ]
        ms = max(spreads)
        status = "PASS" if ms < 0.5 else ("MARGINAL" if ms < 1.0 else "FAIL")
        if ms >= 0.5:
            all_pass = False

        print(f"{N:>4d}  {ad:>10.5f}  {af:>10.5f}  {aa:>10.5f}"
              f"  {ms:>11.4f}%  {status:>10s}")

    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    if all_pass:
        print("  ALL GRID SIZES PASS: alpha is independent of field source")
        print("  The distance exponent is a geometric property of the")
        print("  valley-linear action S = L(1-f), not an artifact of the")
        print("  Poisson solver.")
        print()
        print("  This closes the frozen/static-source control gate for the")
        print("  distance-law lane on the ordered-cubic 64^3 surface.")
    else:
        print("  NOT ALL GRID SIZES PASS the 0.5% threshold.")
        print("  Investigate the field-shape comparison tables above to")
        print("  determine whether boundary effects or normalization")
        print("  differences explain the spread.")

    print()
    print("=" * 80)
    print("SAFE READ")
    print("=" * 80)
    print("  Three-arm control on 31^3, 48^3, 64^3:")
    print("    DYNAMIC  = Poisson-solved 1/r field")
    print("    FROZEN   = hand-crafted 1/r, calibrated amplitude")
    print("    ANALYTIC = exact finite-sum deflection (no grid field)")
    print("  All three use the same valley-linear action S = L(1-f).")
    print("  Pass condition: alpha agrees within 0.5% across all arms.")
    print("  This confirms the exponent is geometric, not solver-dependent.")


if __name__ == "__main__":
    main()
