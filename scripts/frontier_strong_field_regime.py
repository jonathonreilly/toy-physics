#!/usr/bin/env python3
"""Strong-field regime characterization: horizon structure and breakdown.

Physics
-------
The path-sum propagator uses action S = L(1 - f).  In the weak-field regime
f << 1, this reproduces Newtonian gravity (deflection, time dilation, etc.).
As f approaches 1, the action S -> 0 and phase accumulation freezes.
When f > 1, the action becomes negative, inverting the phase gradient.

This script characterizes the four regimes:
  f << 1 : weak-field, Newtonian
  f ~ 0.5 : intermediate, deviations from GR linearization
  f -> 1  : horizon-like, phase freezing
  f > 1   : super-horizon, amplitude amplification / breakdown

Tests
-----
1. Propagator amplitude vs uniform field strength (f = 0.1 to 0.99)
2. Effective horizon radius and wavepacket shadow mapping
3. Deflection angle deviation from weak-field GR prediction
4. Super-horizon (f > 1) behavior and natural breakdown scale

Uses 3D lattice with Poisson-sourced field and 1D transfer-matrix propagation.

PStack experiment: strong-field-regime
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
# Poisson solver (shared infrastructure)
# ===========================================================================

def solve_poisson_sparse(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0) -> np.ndarray:
    """Solve 3D Poisson equation with Dirichlet BC using sparse solver."""
    M_int = N - 2
    n_interior = M_int * M_int * M_int

    def idx(i, j, k):
        return i * M_int * M_int + j * M_int + k

    rows, cols, vals = [], [], []
    rhs = np.zeros(n_interior)
    mx, my, mz = mass_pos
    mi, mj, mk = mx - 1, my - 1, mz - 1

    for i in range(M_int):
        for j in range(M_int):
            for k in range(M_int):
                c = idx(i, j, k)
                rows.append(c); cols.append(c); vals.append(-6.0)
                if i > 0:
                    rows.append(c); cols.append(idx(i-1, j, k)); vals.append(1.0)
                if i < M_int - 1:
                    rows.append(c); cols.append(idx(i+1, j, k)); vals.append(1.0)
                if j > 0:
                    rows.append(c); cols.append(idx(i, j-1, k)); vals.append(1.0)
                if j < M_int - 1:
                    rows.append(c); cols.append(idx(i, j+1, k)); vals.append(1.0)
                if k > 0:
                    rows.append(c); cols.append(idx(i, j, k-1)); vals.append(1.0)
                if k < M_int - 1:
                    rows.append(c); cols.append(idx(i, j, k+1)); vals.append(1.0)
                if i == mi and j == mj and k == mk:
                    rhs[c] = -mass_strength

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))
    phi_interior = spsolve(A, rhs)

    field = np.zeros((N, N, N))
    for i in range(M_int):
        for j in range(M_int):
            for k in range(M_int):
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


# ===========================================================================
# 1D transfer matrix propagator
# ===========================================================================

def cos2_kernel(theta: float) -> float:
    """cos^2 angular kernel."""
    return math.cos(theta) ** 2


def build_1d_transfer_matrix(
    field_1d: np.ndarray,
    k_phase: float,
    atten_power: float,
    max_dy: int | None = None,
) -> np.ndarray:
    """Transfer matrix for one x-step on a 1D transverse line.

    M[y_out, y_in] = exp(i * k * L * (1 - f_avg)) * w(theta) / L^p
    """
    ny = len(field_1d)
    M = np.zeros((ny, ny), dtype=complex)

    for y_out in range(ny):
        f_out = field_1d[y_out]
        for y_in in range(ny):
            dy = y_out - y_in
            if max_dy is not None and abs(dy) > max_dy:
                continue

            f_in = field_1d[y_in]
            L = math.sqrt(1.0 + dy * dy)
            f_avg = 0.5 * (f_in + f_out)
            S = L * (1.0 - f_avg)
            theta = math.atan2(abs(dy), 1.0)
            w = cos2_kernel(theta)
            M[y_out, y_in] = np.exp(1j * k_phase * S) * w / (L ** atten_power)

    return M


def gaussian_wavepacket(ny: int, center: float, sigma: float,
                        k0: float = 0.0) -> np.ndarray:
    """Normalized Gaussian wavepacket in 1D transverse space."""
    y = np.arange(ny, dtype=float)
    psi = np.exp(-0.5 * ((y - center) / sigma) ** 2) * np.exp(1j * k0 * y)
    norm = np.sqrt(np.sum(np.abs(psi) ** 2))
    if norm > 0:
        psi /= norm
    return psi


# ===========================================================================
# Test 1: Propagator amplitude vs uniform field strength
# ===========================================================================

def test1_amplitude_vs_field_strength():
    """Propagate wavepacket through uniform-field region, measure transmission."""
    print("=" * 70)
    print("TEST 1: Propagator amplitude vs uniform field strength")
    print("=" * 70)

    N_trans = 31          # transverse lattice size
    N_prop = 20           # propagation layers
    k_phase = 6.0
    atten_power = 1.0
    max_dy = 5
    sigma = 3.0
    center = N_trans // 2

    f_values = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0, 1.05, 1.1]

    print(f"\nLattice: {N_trans} transverse x {N_prop} propagation layers")
    print(f"k = {k_phase}, p = {atten_power}, max_dy = {max_dy}")
    print(f"Gaussian sigma = {sigma}, center = {center}")
    print()
    print(f"{'f':>6s}  {'|psi_out|':>10s}  {'|psi_in|':>10s}  "
          f"{'ratio':>10s}  {'norm_out':>10s}  {'phase_per_step':>14s}")
    print("-" * 70)

    results = []

    for f_val in f_values:
        # Uniform field: f_1d = f_val everywhere
        field_1d = np.full(N_trans, f_val)

        # Build transfer matrix for this uniform field
        M = build_1d_transfer_matrix(field_1d, k_phase, atten_power, max_dy)

        # Initial wavepacket
        psi = gaussian_wavepacket(N_trans, center, sigma)
        norm_in = np.sqrt(np.sum(np.abs(psi) ** 2))
        amp_in = np.max(np.abs(psi))

        # Propagate through N_prop layers
        for _ in range(N_prop):
            psi = M @ psi

        norm_out = np.sqrt(np.sum(np.abs(psi) ** 2))
        amp_out = np.max(np.abs(psi))
        ratio = norm_out / norm_in if norm_in > 0 else 0.0

        # Expected phase per step: k * (1 - f)
        phase_step = k_phase * (1.0 - f_val)

        print(f"{f_val:6.2f}  {amp_out:10.4e}  {amp_in:10.4e}  "
              f"{ratio:10.4e}  {norm_out:10.4e}  {phase_step:14.4f}")

        results.append({
            'f': f_val,
            'amp_in': amp_in,
            'amp_out': amp_out,
            'norm_in': norm_in,
            'norm_out': norm_out,
            'ratio': ratio,
            'phase_per_step': phase_step,
        })

    # Analysis
    print()
    print("--- Analysis ---")
    # Find where ratio transitions
    ratios = [r['ratio'] for r in results]
    f_vals = [r['f'] for r in results]

    # At f=0, ratio should be some baseline
    baseline = ratios[0] if ratios[0] > 0 else 1.0
    print(f"Baseline ratio (f=0): {baseline:.4e}")

    # Check f=1 behavior
    idx_f1 = None
    for i, fv in enumerate(f_vals):
        if abs(fv - 1.0) < 0.01:
            idx_f1 = i
            break
    if idx_f1 is not None:
        print(f"Ratio at f=1.0: {ratios[idx_f1]:.4e}")
        if ratios[idx_f1] > baseline:
            print("  -> f=1 AMPLIFIES (phase frozen, no destructive interference)")
        elif ratios[idx_f1] < baseline * 0.1:
            print("  -> f=1 ABSORBS (amplitude suppressed)")
        else:
            print("  -> f=1 NEUTRAL (similar to free propagation)")

    # Check f>1 behavior
    for i, fv in enumerate(f_vals):
        if fv > 1.0:
            print(f"Ratio at f={fv:.2f}: {ratios[i]:.4e}"
                  f"  (amplification factor vs baseline: {ratios[i]/baseline:.2f}x)")

    return results


# ===========================================================================
# Test 2: Effective horizon radius and shadow mapping
# ===========================================================================

def test2_horizon_shadow():
    """Map the effective horizon radius and wavepacket shadow."""
    print("\n" + "=" * 70)
    print("TEST 2: Effective horizon radius and shadow mapping")
    print("=" * 70)

    N = 31
    mid = N // 2
    k_phase = 6.0
    atten_power = 1.0
    max_dy = 5
    sigma = 2.0

    # Mass strengths chosen so horizon forms at varying radii
    mass_strengths = [20, 40, 60, 80, 120]

    print(f"\nLattice: {N}^3, mass at center ({mid},{mid},{mid})")
    print(f"k = {k_phase}, p = {atten_power}")
    print()

    results = []

    for ms in mass_strengths:
        t0 = time.time()
        field = solve_poisson(N, (mid, mid, mid), ms)
        t_solve = time.time() - t0

        # Find horizon radius: where f = 1 along radial direction
        f_radial = field[mid, mid, mid:]
        r_horizon = None
        for r in range(1, len(f_radial)):
            if f_radial[r] < 1.0 and (r == 0 or f_radial[r-1] >= 1.0):
                # Interpolate
                if r > 0 and f_radial[r-1] > 1.0:
                    r_horizon = r - 1 + (f_radial[r-1] - 1.0) / (f_radial[r-1] - f_radial[r])
                break
            elif f_radial[r] >= 1.0:
                continue

        # If no crossing found, check if all interior is above 1
        if r_horizon is None:
            for r in range(len(f_radial) - 1, 0, -1):
                if f_radial[r] >= 1.0:
                    r_horizon = r
                    break

        f_max = field[mid, mid, mid]
        f_at_r5 = field[mid, mid, mid + 5] if mid + 5 < N else 0

        # Surface gravity at horizon
        kappa = None
        if r_horizon is not None and r_horizon > 0:
            r_h_int = int(round(r_horizon))
            if r_h_int > 0 and mid + r_h_int + 1 < N and mid + r_h_int - 1 >= 0:
                kappa = abs(field[mid, mid, mid + r_h_int + 1]
                           - field[mid, mid, mid + r_h_int - 1]) / 2.0

        print(f"\n  Mass strength = {ms}")
        print(f"  f_max (center) = {f_max:.4f}")
        print(f"  f(r=5) = {f_at_r5:.4f}")
        print(f"  Horizon radius r_h = {r_horizon}")
        if kappa is not None:
            print(f"  Surface gravity kappa = {kappa:.4f}")
        print(f"  Poisson solve: {t_solve:.2f}s")

        # Propagate wavepackets at different impact parameters
        # Use the midplane z=mid, propagate along x, transverse in y
        field_midz = field[:, :, mid]  # 2D slice at z=mid

        impact_params = list(range(0, mid, 2))  # b = 0, 2, 4, ...
        shadow_data = []

        for b in impact_params:
            y_init = mid + b
            if y_init >= N - 2:
                break

            # 1D propagation along x with transverse field at z=mid
            psi = gaussian_wavepacket(N, y_init, sigma)
            norm_in = np.sqrt(np.sum(np.abs(psi) ** 2))

            for x in range(1, N - 1):
                field_1d = field_midz[x, :]
                M = build_1d_transfer_matrix(field_1d, k_phase, atten_power, max_dy)
                psi = M @ psi

            norm_out = np.sqrt(np.sum(np.abs(psi) ** 2))
            ratio = norm_out / norm_in if norm_in > 0 else 0.0

            # Centroid shift (deflection)
            y_coords = np.arange(N, dtype=float)
            prob = np.abs(psi) ** 2
            total_prob = np.sum(prob)
            if total_prob > 1e-30:
                centroid = np.sum(y_coords * prob) / total_prob
                deflection = centroid - y_init
            else:
                centroid = y_init
                deflection = 0.0

            shadow_data.append({
                'b': b,
                'ratio': ratio,
                'deflection': deflection,
                'norm_out': norm_out,
            })

        print(f"\n  Shadow map (impact parameter b, transmission ratio, deflection):")
        print(f"  {'b':>4s}  {'ratio':>10s}  {'deflection':>10s}  {'status':>12s}")
        print(f"  " + "-" * 44)

        for sd in shadow_data:
            b = sd['b']
            in_horizon = "INSIDE r_h" if (r_horizon and b < r_horizon) else ""
            print(f"  {b:4d}  {sd['ratio']:10.4e}  {sd['deflection']:10.4f}  {in_horizon:>12s}")

        results.append({
            'ms': ms,
            'f_max': f_max,
            'r_horizon': r_horizon,
            'kappa': kappa,
            'shadow': shadow_data,
        })

    return results


# ===========================================================================
# Test 3: Deviation from weak-field GR
# ===========================================================================

def test3_gr_deviation():
    """Compare propagator deflection to weak-field GR prediction."""
    print("\n" + "=" * 70)
    print("TEST 3: Deviation from weak-field GR prediction")
    print("=" * 70)

    N = 31
    mid = N // 2
    k_phase = 6.0
    atten_power = 1.0
    max_dy = 5
    sigma = 2.0
    b_test = 8  # impact parameter for deflection measurement

    # Use varying mass strengths to create different peak f values
    # We want the peak f at r=b_test to vary from 0.1 to 0.9
    # f ~ ms / (4 * pi * r) from Poisson, so ms ~ f_target * 4 * pi * r
    target_f_at_b = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    # Rough calibration: need to solve and measure
    # Start with a range of mass strengths and measure actual f at b
    ms_range = [2, 5, 10, 15, 25, 40, 60]

    print(f"\nLattice: {N}^3, mass at center, impact parameter b = {b_test}")
    print(f"k = {k_phase}, p = {atten_power}")
    print()

    print(f"{'ms':>6s}  {'f_peak':>8s}  {'f_at_b':>8s}  {'defl_prop':>10s}  "
          f"{'defl_GR':>10s}  {'deviation%':>10s}")
    print("-" * 62)

    results = []

    for ms in ms_range:
        field = solve_poisson(N, (mid, mid, mid), ms)

        f_peak = field[mid, mid, mid]
        f_at_b = field[mid, mid + b_test, mid] if mid + b_test < N else 0
        f_at_b_x = field[mid, mid, mid]  # peak along propagation path

        # Propagator deflection: propagate at impact parameter b
        field_midz = field[:, :, mid]
        y_init = mid + b_test
        if y_init >= N - 1:
            continue

        psi = gaussian_wavepacket(N, y_init, sigma)

        for x in range(1, N - 1):
            field_1d = field_midz[x, :]
            M = build_1d_transfer_matrix(field_1d, k_phase, atten_power, max_dy)
            psi = M @ psi

        # Measure deflection
        y_coords = np.arange(N, dtype=float)
        prob = np.abs(psi) ** 2
        total_prob = np.sum(prob)
        if total_prob > 1e-30:
            centroid = np.sum(y_coords * prob) / total_prob
            defl_prop = centroid - y_init
        else:
            defl_prop = 0.0

        # Weak-field GR prediction: deflection ~ integral of df/dy along path
        # In weak field, phase shift = k * integral of f(x,y) dx
        # Deflection angle ~ d(phase)/dy / k
        # For point source, analytic: delta_y ~ ms / (4*pi*b) * N_eff / k_eff
        # But let us compute numerically in the weak-field limit:
        # Sum f along the path at b and at b+1, take the gradient
        phase_at_b = 0.0
        phase_at_b1 = 0.0
        for x in range(1, N - 1):
            if mid + b_test < N:
                phase_at_b += field[x, mid + b_test, mid]
            if mid + b_test + 1 < N:
                phase_at_b1 += field[x, mid + b_test + 1, mid]

        # Weak-field deflection: gradient of integrated phase
        defl_gr = k_phase * (phase_at_b - phase_at_b1)
        # This is the transverse momentum kick; convert to displacement
        # over the propagation length
        # Actually, for the discrete lattice, the weak-field prediction is:
        # The transverse phase gradient creates a momentum kick
        # delta_k_y = k * sum_x (f(x,b) - f(x,b+1))
        # displacement = delta_k_y * N_prop / k (in lattice units, roughly)
        n_prop = N - 2
        defl_gr_displacement = defl_gr * n_prop / (k_phase * k_phase) if k_phase > 0 else 0

        # Simple deviation
        if abs(defl_gr_displacement) > 1e-10:
            deviation_pct = abs(defl_prop - defl_gr_displacement) / abs(defl_gr_displacement) * 100
        else:
            deviation_pct = float('inf') if abs(defl_prop) > 1e-10 else 0.0

        print(f"{ms:6.1f}  {f_peak:8.4f}  {f_at_b:8.4f}  {defl_prop:10.4f}  "
              f"{defl_gr_displacement:10.4f}  {deviation_pct:10.1f}")

        results.append({
            'ms': ms,
            'f_peak': f_peak,
            'f_at_b': f_at_b,
            'defl_prop': defl_prop,
            'defl_gr_weak': defl_gr_displacement,
            'deviation_pct': deviation_pct,
        })

    # Find threshold where deviation > 10% and > 50%
    print()
    print("--- Weak-field validity thresholds ---")
    thresh_10 = None
    thresh_50 = None
    for r in results:
        if r['deviation_pct'] > 10 and thresh_10 is None:
            thresh_10 = r
        if r['deviation_pct'] > 50 and thresh_50 is None:
            thresh_50 = r

    if thresh_10:
        print(f"10% deviation at f_peak ~ {thresh_10['f_peak']:.3f} "
              f"(f_at_b ~ {thresh_10['f_at_b']:.3f}, ms = {thresh_10['ms']})")
    else:
        print("10% deviation: NOT REACHED in tested range")

    if thresh_50:
        print(f"50% deviation at f_peak ~ {thresh_50['f_peak']:.3f} "
              f"(f_at_b ~ {thresh_50['f_at_b']:.3f}, ms = {thresh_50['ms']})")
    else:
        print("50% deviation: NOT REACHED in tested range")

    return results


# ===========================================================================
# Test 4: Super-horizon (f > 1) behavior
# ===========================================================================

def test4_super_horizon():
    """Characterize propagator behavior when f exceeds 1."""
    print("\n" + "=" * 70)
    print("TEST 4: Super-horizon (f > 1) behavior")
    print("=" * 70)

    N_trans = 31
    N_prop = 20
    k_phase = 6.0
    atten_power = 1.0
    max_dy = 5
    sigma = 3.0
    center = N_trans // 2

    f_values = [0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0]

    print(f"\nUniform field propagation: {N_trans} transverse x {N_prop} layers")
    print(f"k = {k_phase}, p = {atten_power}")
    print()
    print(f"{'f':>6s}  {'S=L(1-f)':>10s}  {'norm_out':>10s}  {'growth_rate':>12s}  "
          f"{'phase_sign':>10s}  {'behavior':>20s}")
    print("-" * 78)

    results = []

    for f_val in f_values:
        field_1d = np.full(N_trans, f_val)
        M = build_1d_transfer_matrix(field_1d, k_phase, atten_power, max_dy)

        psi = gaussian_wavepacket(N_trans, center, sigma)
        norm_in = np.sqrt(np.sum(np.abs(psi) ** 2))

        # Track norm at each step
        norms = [norm_in]
        for step in range(N_prop):
            psi = M @ psi
            norms.append(np.sqrt(np.sum(np.abs(psi) ** 2)))

        norm_out = norms[-1]
        ratio = norm_out / norm_in if norm_in > 0 else 0.0

        # Growth rate per step (geometric mean)
        if norm_in > 0 and norm_out > 0:
            growth_rate = (norm_out / norm_in) ** (1.0 / N_prop)
        else:
            growth_rate = 0.0

        S_action = 1.0 - f_val  # action per unit length
        phase_sign = "positive" if S_action > 0 else ("zero" if S_action == 0 else "negative")

        # Classify behavior
        if ratio < 0.1:
            behavior = "ABSORBED"
        elif ratio < 0.5:
            behavior = "ATTENUATED"
        elif ratio < 2.0:
            behavior = "TRANSMITTED"
        elif ratio < 10.0:
            behavior = "AMPLIFIED"
        else:
            behavior = "DIVERGENT"

        print(f"{f_val:6.2f}  {S_action:10.4f}  {norm_out:10.4e}  "
              f"{growth_rate:12.6f}  {phase_sign:>10s}  {behavior:>20s}")

        results.append({
            'f': f_val,
            'S_action': S_action,
            'norm_in': norm_in,
            'norm_out': norm_out,
            'ratio': ratio,
            'growth_rate': growth_rate,
            'norms': norms,
            'behavior': behavior,
        })

    # Analysis: find the maximum stable f
    print()
    print("--- Super-horizon analysis ---")

    # Check if there is a natural maximum f
    for r in results:
        if r['f'] >= 1.0:
            print(f"  f = {r['f']:.2f}: action S = {r['S_action']:.3f}, "
                  f"norm grows by {r['ratio']:.2e}x over {N_prop} steps "
                  f"({r['behavior']})")

    # Spectral radius of transfer matrix at each f
    print()
    print("  Transfer matrix spectral radius (largest eigenvalue magnitude):")
    print(f"  {'f':>6s}  {'spectral_r':>12s}  {'implies':>20s}")
    print(f"  " + "-" * 44)

    for f_val in [0.5, 0.9, 1.0, 1.1, 1.5, 2.0]:
        field_1d = np.full(N_trans, f_val)
        M = build_1d_transfer_matrix(field_1d, k_phase, atten_power, max_dy)
        eigenvalues = np.linalg.eigvals(M)
        spec_r = np.max(np.abs(eigenvalues))
        stability = "stable" if spec_r <= 1.0 else f"unstable ({spec_r:.3f}x/step)"
        print(f"  {f_val:6.2f}  {spec_r:12.6f}  {stability:>20s}")

    return results


# ===========================================================================
# Test 5: Schwarzschild radius analog
# ===========================================================================

def test5_schwarzschild_analog():
    """Define and characterize the analog of the Schwarzschild radius."""
    print("\n" + "=" * 70)
    print("TEST 5: Schwarzschild radius analog")
    print("=" * 70)

    N = 31
    mid = N // 2
    mass_strengths = [10, 20, 40, 60, 80, 100, 120]

    print(f"\nLattice: {N}^3, mass at center")
    print("Finding r_h where f(r_h) = 1 for each mass strength")
    print()
    print(f"{'ms':>6s}  {'f_max':>8s}  {'r_h':>6s}  {'kappa':>8s}  "
          f"{'r_h/ms':>8s}  {'has_horizon':>12s}")
    print("-" * 58)

    results = []

    for ms in mass_strengths:
        field = solve_poisson(N, (mid, mid, mid), ms)
        f_max = field[mid, mid, mid]

        # Find r_h along z-axis from center
        f_radial = []
        for r in range(mid + 1):
            if mid + r < N:
                f_radial.append(field[mid, mid, mid + r])
            else:
                f_radial.append(0.0)

        r_horizon = None
        for r in range(1, len(f_radial)):
            if f_radial[r] < 1.0 <= f_radial[r - 1]:
                # Linear interpolation
                r_horizon = (r - 1) + (f_radial[r - 1] - 1.0) / (f_radial[r - 1] - f_radial[r])
                break

        has_horizon = r_horizon is not None

        # Surface gravity
        kappa = None
        if has_horizon and r_horizon > 0:
            r_lo = int(math.floor(r_horizon))
            r_hi = min(r_lo + 2, len(f_radial) - 1)
            r_lo_safe = max(r_lo - 1, 0)
            if r_hi > r_lo_safe:
                kappa = abs(f_radial[r_hi] - f_radial[r_lo_safe]) / (r_hi - r_lo_safe)

        r_h_over_ms = r_horizon / ms if r_horizon and ms > 0 else None

        print(f"{ms:6.1f}  {f_max:8.4f}  "
              f"{r_horizon if r_horizon else 'none':>6s}  " if not r_horizon else
              f"{ms:6.1f}  {f_max:8.4f}  {r_horizon:6.2f}  "
              f"{kappa if kappa else 0:8.4f}  "
              f"{r_h_over_ms if r_h_over_ms else 0:8.5f}  "
              f"{'YES' if has_horizon else 'no':>12s}")

        results.append({
            'ms': ms,
            'f_max': f_max,
            'r_horizon': r_horizon,
            'kappa': kappa,
            'has_horizon': has_horizon,
            'r_h_over_ms': r_h_over_ms,
        })

    # Check if r_h is proportional to ms (like Schwarzschild r_s = 2GM/c^2)
    print()
    print("--- Schwarzschild scaling check ---")
    has_h = [(r['ms'], r['r_horizon']) for r in results if r['has_horizon']]
    if len(has_h) >= 2:
        ms_arr = np.array([h[0] for h in has_h])
        rh_arr = np.array([h[1] for h in has_h])

        # Linear fit r_h = a * ms + b
        if len(ms_arr) >= 2:
            coeffs = np.polyfit(ms_arr, rh_arr, 1)
            r_pred = np.polyval(coeffs, ms_arr)
            ss_res = np.sum((rh_arr - r_pred) ** 2)
            ss_tot = np.sum((rh_arr - np.mean(rh_arr)) ** 2)
            r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

            print(f"  Linear fit: r_h = {coeffs[0]:.4f} * ms + {coeffs[1]:.4f}")
            print(f"  R^2 = {r_squared:.4f}")
            if r_squared > 0.95:
                print(f"  -> r_h IS proportional to ms (Schwarzschild-like scaling)")
                print(f"  -> Proportionality constant: r_h / ms ~ {coeffs[0]:.4f}")
            else:
                print(f"  -> r_h is NOT simply proportional to ms")

        # Compare to 3D Poisson: phi ~ ms / (4*pi*r), so f=1 at r = ms/(4*pi)
        # Expected: r_h ~ ms / (4*pi) ~ 0.0796 * ms
        expected_coeff = 1.0 / (4.0 * math.pi)
        print(f"\n  Expected from 3D Poisson (f = ms/(4*pi*r)): r_h = {expected_coeff:.4f} * ms")
        if len(has_h) > 0:
            actual_coeff = np.mean(rh_arr / ms_arr)
            print(f"  Measured mean r_h/ms = {actual_coeff:.4f}")
            print(f"  Ratio (measured/expected) = {actual_coeff/expected_coeff:.4f}")
    else:
        print("  Insufficient data points with horizons for scaling analysis")

    return results


# ===========================================================================
# Main
# ===========================================================================

def main():
    t_start = time.time()

    print("Strong-Field Regime Characterization")
    print("=" * 70)
    print("Framework: S = L(1-f), path-sum propagator on 3D lattice")
    print("Exploring: f -> 1 (horizon), f > 1 (breakdown)")
    print()

    results1 = test1_amplitude_vs_field_strength()
    results2 = test2_horizon_shadow()
    results3 = test3_gr_deviation()
    results4 = test4_super_horizon()
    results5 = test5_schwarzschild_analog()

    # ===========================================================================
    # Summary
    # ===========================================================================
    print("\n" + "=" * 70)
    print("SUMMARY: Strong-Field Regime")
    print("=" * 70)

    # Test 1 summary
    print("\n1. AMPLITUDE VS FIELD STRENGTH:")
    for r in results1:
        if r['f'] in [0.0, 0.5, 0.9, 1.0, 1.1]:
            print(f"   f = {r['f']:.2f}: transmission ratio = {r['ratio']:.4e} "
                  f"(phase/step = {r['phase_per_step']:.2f})")

    # Test 2 summary
    print("\n2. HORIZON STRUCTURE:")
    for r in results2:
        rh = r['r_horizon']
        rh_str = f"{rh:.2f}" if rh else "none"
        # Count shadow entries below / above horizon
        trapped = 0
        passed = 0
        if r['shadow']:
            for sd in r['shadow']:
                if rh and sd['b'] < rh and sd['ratio'] > 2.0:
                    trapped += 1
                elif sd['ratio'] < 2.0:
                    passed += 1
        print(f"   ms = {r['ms']}: r_h = {rh_str}, f_max = {r['f_max']:.2f}")

    # Test 3 summary
    print("\n3. WEAK-FIELD VALIDITY:")
    for r in results3:
        dev = r['deviation_pct']
        dev_str = f"{dev:.1f}%" if dev < 1e6 else "inf"
        print(f"   ms = {r['ms']}: f_peak = {r['f_peak']:.3f}, "
              f"deviation from weak-field = {dev_str}")

    # Test 4 summary
    print("\n4. SUPER-HORIZON BEHAVIOR:")
    for r in results4:
        if r['f'] >= 0.95:
            print(f"   f = {r['f']:.2f}: {r['behavior']} "
                  f"(growth rate = {r['growth_rate']:.4f}/step)")

    # Test 5 summary
    print("\n5. SCHWARZSCHILD ANALOG:")
    for r in results5:
        if r['has_horizon']:
            print(f"   ms = {r['ms']}: r_h = {r['r_horizon']:.2f}")

    # Overall assessment
    print("\n" + "-" * 70)
    print("OVERALL ASSESSMENT:")
    print("-" * 70)

    # Check if f=1 is absorbing, transmitting, or amplifying
    f1_result = None
    for r in results1:
        if abs(r['f'] - 1.0) < 0.01:
            f1_result = r

    if f1_result:
        ratio = f1_result['ratio']
        baseline = results1[0]['ratio'] if results1[0]['ratio'] > 0 else 1.0
        if ratio > baseline * 2:
            print("- The f=1 surface AMPLIFIES rather than absorbs: NOT a true horizon")
            print("  This is because S=0 removes phase variation, eliminating")
            print("  destructive interference that normally limits amplitude.")
        elif ratio < baseline * 0.5:
            print("- The f=1 surface ABSORBS: acts as a partial horizon")
        else:
            print("- The f=1 surface is NEUTRAL: amplitude passes through")
            print("  Phase freezing at S=0 does not create an absorbing boundary.")

    # Check super-horizon stability
    f_gt1 = [r for r in results4 if r['f'] > 1.0]
    if f_gt1:
        all_unstable = all(r['growth_rate'] > 1.0 for r in f_gt1)
        if all_unstable:
            print("- ALL f > 1 regions are UNSTABLE (amplitude grows exponentially)")
            print("  The framework has a natural breakdown at f = 1.")
            print("  This is analogous to the Schwarzschild singularity: the")
            print("  propagator ceases to be physically meaningful beyond f = 1.")
        else:
            stable_f = [r['f'] for r in f_gt1 if r['growth_rate'] <= 1.0]
            print(f"- Some f > 1 regions are stable: f = {stable_f}")

    # Timing
    t_total = time.time() - t_start
    print(f"\nTotal runtime: {t_total:.1f}s")


if __name__ == "__main__":
    main()
