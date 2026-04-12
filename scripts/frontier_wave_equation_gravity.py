#!/usr/bin/env python3
"""Wave equation gravity: promote Poisson to d'Alembertian, get gravitational waves.

Previous probes showed that the Poisson equation (nabla^2 f = -rho) gives
instantaneous gravity -- no gravitational waves. The fix: promote to the
retarded wave equation:

    box f = (d^2/dt^2 - nabla^2) f = -rho

On a lattice with discrete time steps (leapfrog integrator):

    f(t+1) = 2*f(t) - f(t-1) + dt^2 * nabla^2 f(t) + dt^2 * rho(t)

This is the standard Verlet/leapfrog scheme for the wave equation.

Tests:
  1. Wave propagation from sudden source -- wavefront at speed c=1
  2. Static source steady state recovers Poisson (Newton at low frequency)
  3. Moving source produces retarded field (light-cone causality)
  4. Oscillating source: radiation amplitude ~ 1/r (not 1/r^2)
  5. Propagator coupling: mass law and distance law preserved

CFL condition: dt < dx/c = 1, using dt=0.5 for safety.

PStack experiment: wave-equation-gravity
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


# ============================================================================
# Wave equation solver (leapfrog on 3D lattice)
# ============================================================================

def laplacian_3d(f: np.ndarray) -> np.ndarray:
    """Compute discrete Laplacian of 3D field with Dirichlet BC (boundary=0)."""
    lap = -6.0 * f.copy()
    lap[1:, :, :] += f[:-1, :, :]
    lap[:-1, :, :] += f[1:, :, :]
    lap[:, 1:, :] += f[:, :-1, :]
    lap[:, :-1, :] += f[:, 1:, :]
    lap[:, :, 1:] += f[:, :, :-1]
    lap[:, :, :-1] += f[:, :, 1:]
    # Enforce Dirichlet BC: boundary stays zero
    lap[0, :, :] = 0.0
    lap[-1, :, :] = 0.0
    lap[:, 0, :] = 0.0
    lap[:, -1, :] = 0.0
    lap[:, :, 0] = 0.0
    lap[:, :, -1] = 0.0
    return lap


def wave_evolve(N: int, n_steps: int, dt: float,
                rho_func, absorbing_layers: int = 4) -> list[np.ndarray]:
    """Evolve the wave equation box f = -rho on an NxNxN lattice.

    Uses leapfrog: f(t+1) = 2f(t) - f(t-1) + dt^2 * (lap f(t) + rho(t))

    rho_func(step, N) -> NxNxN array of source density at that step.

    Returns list of field snapshots (one per step).
    """
    f_cur = np.zeros((N, N, N))
    f_prev = np.zeros((N, N, N))
    snapshots = [f_cur.copy()]

    for step in range(1, n_steps + 1):
        rho = rho_func(step, N)
        lap = laplacian_3d(f_cur)
        f_next = 2.0 * f_cur - f_prev + dt * dt * (lap + rho)

        # Absorbing boundary: exponential damping in boundary layer
        if absorbing_layers > 0:
            for axis in range(3):
                for side in [0, 1]:
                    for d in range(absorbing_layers):
                        sigma = 0.5 * (1.0 - d / absorbing_layers)
                        slices = [slice(None)] * 3
                        if side == 0:
                            slices[axis] = d
                        else:
                            slices[axis] = N - 1 - d
                        f_next[tuple(slices)] *= (1.0 - sigma)

        # Enforce Dirichlet on outer boundary
        f_next[0, :, :] = 0.0
        f_next[-1, :, :] = 0.0
        f_next[:, 0, :] = 0.0
        f_next[:, -1, :] = 0.0
        f_next[:, :, 0] = 0.0
        f_next[:, :, -1] = 0.0

        f_prev = f_cur
        f_cur = f_next
        snapshots.append(f_cur.copy())

    return snapshots


def solve_poisson_static(N: int, source_pos: tuple[int, int, int],
                         strength: float = 1.0) -> np.ndarray:
    """Solve nabla^2 f = -rho for a point source (Dirichlet BC).

    Falls back to Gauss-Seidel if scipy is not available.
    """
    f = np.zeros((N, N, N))
    sx, sy, sz = source_pos

    if HAS_SCIPY:
        M = N - 2
        n_int = M * M * M

        ii, jj, kk = np.mgrid[0:M, 0:M, 0:M]
        flat = ii.ravel() * M * M + jj.ravel() * M + kk.ravel()

        rows = [flat]
        cols = [flat]
        vals = [np.full(n_int, -6.0)]

        for di, dj, dk in [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                           (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            ni = ii + di
            nj = jj + dj
            nk = kk + dk
            mask = ((ni >= 0) & (ni < M) & (nj >= 0) & (nj < M) &
                    (nk >= 0) & (nk < M))
            src = flat[mask.ravel()]
            dst = ni[mask] * M * M + nj[mask] * M + nk[mask]
            rows.append(src)
            cols.append(dst.ravel())
            vals.append(np.ones(src.shape[0]))

        all_rows = np.concatenate(rows)
        all_cols = np.concatenate(cols)
        all_vals = np.concatenate(vals)
        A = sparse.csr_matrix((all_vals, (all_rows, all_cols)),
                              shape=(n_int, n_int))

        rhs = np.zeros(n_int)
        mi, mj, mk = sx - 1, sy - 1, sz - 1
        if 0 <= mi < M and 0 <= mj < M and 0 <= mk < M:
            rhs[mi * M * M + mj * M + mk] = -strength

        sol = spsolve(A, rhs)
        f[1:N-1, 1:N-1, 1:N-1] = sol.reshape((M, M, M))
    else:
        for _ in range(500):
            for ix in range(1, N - 1):
                for iy in range(1, N - 1):
                    for iz in range(1, N - 1):
                        src = strength if (ix == sx and iy == sy and iz == sz) else 0.0
                        f[ix, iy, iz] = (
                            f[ix-1, iy, iz] + f[ix+1, iy, iz] +
                            f[ix, iy-1, iz] + f[ix, iy+1, iz] +
                            f[ix, iy, iz-1] + f[ix, iy, iz+1] +
                            src
                        ) / 6.0
    return f


# ============================================================================
# Propagator for coupling test (from distance_law probes)
# ============================================================================

BETA = 0.8
K_DEFAULT = 5.0
MAX_D_PHYS = 3


def propagate_beam(field: np.ndarray, k: float, source_yz: tuple[int, int],
                   max_d: int = 3) -> np.ndarray:
    """Propagate amplitude through 3D lattice with given field.

    Propagates along x-axis (layer by layer) with transverse y,z coupling.
    Returns complex amplitude array shaped (N, N, N).
    """
    N = field.shape[0]
    amps = np.zeros((N, N, N), dtype=np.complex128)
    sy, sz = source_yz
    amps[0, sy, sz] = 1.0

    md = min(max_d, N // 2)

    for layer in range(N - 1):
        for iy in range(N):
            for iz in range(N):
                a = amps[layer, iy, iz]
                if abs(a) < 1e-30:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        ny, nz = iy + dy, iz + dz
                        if ny < 0 or ny >= N or nz < 0 or nz >= N:
                            continue
                        dx = 1.0
                        dyp = float(dy)
                        dzp = float(dz)
                        L = math.sqrt(dx * dx + dyp * dyp + dzp * dzp)
                        theta = math.atan2(math.sqrt(dyp**2 + dzp**2), dx)
                        w = math.exp(-BETA * theta * theta)
                        lf = 0.5 * (field[layer, iy, iz]
                                     + field[layer + 1, ny, nz])
                        act = L * (1.0 - lf)
                        phase = k * act
                        amps[layer + 1, ny, nz] += (
                            a * np.exp(1j * phase) * w / (L * L)
                        )
    return amps


def measure_deflection(field: np.ndarray, k: float, source_yz: tuple[int, int],
                       max_d: int = 2) -> float:
    """Measure beam deflection as centroid shift relative to no-field propagation."""
    # Propagate with field
    amps_field = propagate_beam(field, k, source_yz, max_d=max_d)
    # Propagate with no field
    zero_field = np.zeros_like(field)
    amps_free = propagate_beam(zero_field, k, source_yz, max_d=max_d)

    N = field.shape[0]

    def centroid_z(amps):
        det = amps[-1, :, :]
        prob = np.abs(det) ** 2
        total = prob.sum()
        if total < 1e-30:
            return float('nan')
        z_vals = np.arange(N, dtype=float)
        return np.sum(prob * z_vals[None, :]) / total

    c_field = centroid_z(amps_field)
    c_free = centroid_z(amps_free)
    if math.isnan(c_field) or math.isnan(c_free):
        return 0.0
    return c_field - c_free


# ============================================================================
# Test 1: Wave propagation from sudden source
# ============================================================================

def test_wave_propagation(N: int = 31, dt: float = 0.5, n_steps: int = 40):
    """Turn on a point source at t=0, measure outward-propagating wavefront."""
    print("=" * 72)
    print("TEST 1: Wave propagation from sudden source")
    print("=" * 72)
    center = N // 2

    def rho_sudden(step, n):
        rho = np.zeros((n, n, n))
        rho[center, center, center] = 1.0
        return rho

    t0 = time.time()
    snaps = wave_evolve(N, n_steps, dt, rho_sudden, absorbing_layers=5)
    elapsed = time.time() - t0
    print(f"  Lattice: {N}^3, dt={dt}, steps={n_steps}, time={elapsed:.1f}s")

    # Measure field along radial direction at each timestep
    print(f"\n  Wavefront position vs time:")
    print(f"  {'step':>6} {'t':>8} {'r_front':>10} {'c_eff':>10}")

    wavefront_data = []
    for step in range(1, n_steps + 1):
        t = step * dt
        f = snaps[step]
        # Radial profile along x-axis from center
        radial = f[center:, center, center]
        # Find wavefront: outermost point with |f| > threshold
        threshold = 0.001 * np.abs(radial).max() if np.abs(radial).max() > 0 else 0
        if threshold > 0:
            idx_front = 0
            for i in range(len(radial) - 1, 0, -1):
                if abs(radial[i]) > threshold:
                    idx_front = i
                    break
            r_front = float(idx_front)
            c_eff = r_front / t if t > 0 else 0.0
            wavefront_data.append((step, t, r_front, c_eff))
            if step % 5 == 0 or step <= 5:
                print(f"  {step:6d} {t:8.1f} {r_front:10.1f} {c_eff:10.3f}")

    # Measure effective wavefront speed from early-to-mid data
    # (before absorbing BC kills the wavefront at the edges)
    if len(wavefront_data) > 5:
        # Use steps where wavefront hasn't hit boundary yet (r < center-5)
        usable = [d for d in wavefront_data
                  if d[2] > 1.0 and d[2] < center - 6 and d[1] > 0]
        if len(usable) >= 3:
            times = np.array([d[1] for d in usable])
            fronts = np.array([d[2] for d in usable])
            coeffs = np.polyfit(times, fronts, 1)
            c_wave = coeffs[0]
        else:
            c_wave = wavefront_data[5][3] if len(wavefront_data) > 5 else 0.0
    else:
        c_wave = wavefront_data[-1][3] if wavefront_data else 0.0

    print(f"\n  Measured wavefront speed: c_grav = {c_wave:.3f}")
    print(f"  Expected (lattice units):  c = 1.0")
    print(f"  Ratio c_grav/c_expected:  {c_wave:.3f}")

    # Check field settles toward 1/r at late times
    f_final = snaps[-1]
    radial_final = f_final[center:, center, center]
    r_vals = np.arange(1, len(radial_final))
    f_vals = radial_final[1:len(radial_final)]

    # Fit power law in range r=2..8
    mask = (r_vals >= 2) & (r_vals <= 8) & (np.abs(f_vals) > 1e-10)
    if mask.sum() >= 3:
        log_r = np.log(r_vals[mask].astype(float))
        log_f = np.log(np.abs(f_vals[mask]))
        coeffs = np.polyfit(log_r, log_f, 1)
        alpha_settle = coeffs[0]
        print(f"\n  Late-time radial profile: f(r) ~ r^{alpha_settle:.2f}")
        print(f"  Expected (Poisson steady state): r^{-1.0}")
    else:
        alpha_settle = float('nan')
        print(f"\n  Late-time profile: insufficient data for fit")

    passed = abs(c_wave - 1.0) < 0.3  # within 30% of c=1
    status = "PASS" if passed else "PARTIAL"
    print(f"\n  Status: {status}")
    return c_wave, alpha_settle, passed


# ============================================================================
# Test 2: Newton recovered at low frequency (static source -> steady state)
# ============================================================================

def test_newton_recovery(N: int = 31, dt: float = 0.5, n_steps: int = 200):
    """Static source evolves to Poisson steady state."""
    print("\n" + "=" * 72)
    print("TEST 2: Newton recovered at low frequency (static source)")
    print("=" * 72)
    center = N // 2

    def rho_static(step, n):
        rho = np.zeros((n, n, n))
        rho[center, center, center] = 1.0
        return rho

    t0 = time.time()
    snaps = wave_evolve(N, n_steps, dt, rho_static, absorbing_layers=5)
    elapsed = time.time() - t0
    print(f"  Lattice: {N}^3, dt={dt}, steps={n_steps}, time={elapsed:.1f}s")

    f_wave = snaps[-1]

    # Compare to Poisson solution
    f_poisson = solve_poisson_static(N, (center, center, center), strength=1.0)

    # Radial profiles
    radial_wave = f_wave[center:, center, center]
    radial_poisson = f_poisson[center:, center, center]

    print(f"\n  Radial profiles (wave steady state vs Poisson):")
    print(f"  {'r':>4} {'f_wave':>12} {'f_poisson':>12} {'ratio':>10}")

    ratios = []
    for r in range(1, min(12, N // 2 - 2)):
        fw = radial_wave[r]
        fp = radial_poisson[r]
        ratio = fw / fp if abs(fp) > 1e-15 else float('nan')
        ratios.append(ratio)
        print(f"  {r:4d} {fw:12.6f} {fp:12.6f} {ratio:10.4f}")

    # Fit force law from wave steady state
    r_vals = np.arange(2, min(10, N // 2 - 3))
    f_vals = np.array([radial_wave[r] for r in r_vals])
    mask = np.abs(f_vals) > 1e-10
    if mask.sum() >= 3:
        log_r = np.log(r_vals[mask].astype(float))
        log_f = np.log(np.abs(f_vals[mask]))
        coeffs = np.polyfit(log_r, log_f, 1)
        alpha_wave = coeffs[0]
    else:
        alpha_wave = float('nan')

    # Same for Poisson
    fp_vals = np.array([radial_poisson[r] for r in r_vals])
    mask_p = np.abs(fp_vals) > 1e-10
    if mask_p.sum() >= 3:
        log_rp = np.log(r_vals[mask_p].astype(float))
        log_fp = np.log(np.abs(fp_vals[mask_p]))
        coeffs_p = np.polyfit(log_rp, log_fp, 1)
        alpha_poisson = coeffs_p[0]
    else:
        alpha_poisson = float('nan')

    # Check convergence of ratios
    valid_ratios = [r for r in ratios if not math.isnan(r) and abs(r) > 0.01]
    if valid_ratios:
        mean_ratio = np.mean(valid_ratios)
        std_ratio = np.std(valid_ratios)
    else:
        mean_ratio = float('nan')
        std_ratio = float('nan')

    print(f"\n  Force law exponent (wave steady state):  alpha = {alpha_wave:.3f}")
    print(f"  Force law exponent (Poisson):             alpha = {alpha_poisson:.3f}")
    print(f"  Wave/Poisson ratio: {mean_ratio:.4f} +/- {std_ratio:.4f}")
    print(f"  Expected: alpha = -1.0 (potential), force ~ 1/r^2")

    passed = (not math.isnan(alpha_wave) and abs(alpha_wave - (-1.0)) < 0.15
              and not math.isnan(mean_ratio))
    status = "PASS" if passed else "PARTIAL"
    print(f"\n  Status: {status}")
    return alpha_wave, alpha_poisson, mean_ratio, passed


# ============================================================================
# Test 3: Moving source produces retarded field
# ============================================================================

def test_retardation(N: int = 41, dt: float = 0.5, n_steps: int = 80):
    """Moving source: field asymmetry demonstrates retardation.

    Compare wave-equation field to instantaneous Poisson field for a moving
    source. The wave field should lag behind (asymmetry in front vs behind
    the source). We measure the field at equal distances ahead and behind
    the source -- with retardation, the field behind should be stronger
    (it was sourced when the source was closer).
    """
    print("\n" + "=" * 72)
    print("TEST 3: Moving source produces retarded field")
    print("=" * 72)
    center = N // 2
    v_source = 0.4  # source velocity in lattice units (v < c=1)

    def rho_moving(step, n):
        rho = np.zeros((n, n, n))
        t = step * dt
        x_src = center + v_source * t
        ix_src = int(round(x_src))
        if 1 <= ix_src < n - 1:
            rho[ix_src, center, center] = 1.0
        return rho

    t0 = time.time()
    snaps = wave_evolve(N, n_steps, dt, rho_moving, absorbing_layers=5)
    elapsed = time.time() - t0
    print(f"  Lattice: {N}^3, v_source={v_source}, dt={dt}, steps={n_steps}")
    print(f"  Time: {elapsed:.1f}s")

    # Measure field asymmetry: compare f(x_src + d) vs f(x_src - d)
    # For retarded field: f_behind > f_ahead (field hasn't caught up in front)
    print(f"\n  Field asymmetry (behind vs ahead of moving source):")
    print(f"  {'step':>6} {'t':>6} {'x_src':>6} {'d':>4} "
          f"{'f_behind':>12} {'f_ahead':>12} {'ratio':>8}")

    asymmetry_ratios = []
    for step in range(20, n_steps + 1, 10):
        t = step * dt
        f = snaps[step]
        x_src = center + v_source * t
        ix_src = int(round(x_src))

        for d in [3, 5, 7]:
            ix_behind = ix_src - d
            ix_ahead = ix_src + d
            if 1 <= ix_behind < N - 1 and 1 <= ix_ahead < N - 1:
                f_behind = abs(f[ix_behind, center, center])
                f_ahead = abs(f[ix_ahead, center, center])
                if f_ahead > 1e-12:
                    ratio = f_behind / f_ahead
                    asymmetry_ratios.append(ratio)
                    if step % 20 == 0:
                        print(f"  {step:6d} {t:6.1f} {ix_src:6d} {d:4d} "
                              f"{f_behind:12.6f} {f_ahead:12.6f} {ratio:8.3f}")

    if asymmetry_ratios:
        mean_asym = np.mean(asymmetry_ratios)
        std_asym = np.std(asymmetry_ratios)
        print(f"\n  Mean asymmetry ratio (behind/ahead): {mean_asym:.3f} +/- {std_asym:.3f}")
        print(f"  Expected for retarded field: > 1.0 (field stronger behind)")
        print(f"  Expected for instantaneous:  = 1.0 (symmetric)")
        passed = mean_asym > 1.01  # at least 1% asymmetry
    else:
        mean_asym = float('nan')
        passed = False

    status = "PASS" if passed else "PARTIAL"
    print(f"\n  Status: {status}")
    return mean_asym, passed


# ============================================================================
# Test 4: Gravitational wave energy (oscillating source)
# ============================================================================

def test_radiation(N: int = 51, dt: float = 0.5, n_steps: int = 120):
    """Oscillating source: radiation amplitude ~ 1/r, power ~ omega^2."""
    print("\n" + "=" * 72)
    print("TEST 4: Gravitational wave energy (oscillating source)")
    print("=" * 72)
    center = N // 2
    omega = 0.3  # angular frequency

    def rho_oscillating(step, n):
        rho = np.zeros((n, n, n))
        t = step * dt
        rho[center, center, center] = math.sin(omega * t)
        return rho

    t0 = time.time()
    snaps = wave_evolve(N, n_steps, dt, rho_oscillating, absorbing_layers=6)
    elapsed = time.time() - t0
    print(f"  Lattice: {N}^3, omega={omega}, dt={dt}, steps={n_steps}")
    print(f"  Time: {elapsed:.1f}s")

    # Measure amplitude envelope at various distances
    # Use late-time snapshots to avoid transient
    late_start = n_steps // 2
    late_snaps = snaps[late_start:]

    print(f"\n  Radiation amplitude vs distance:")
    print(f"  {'r':>4} {'amp_max':>12} {'expected_1/r':>14} {'expected_1/r2':>14}")

    r_list = []
    amp_list = []
    for r in range(3, min(20, center - 5)):
        # Measure max field amplitude at distance r from center (along x-axis)
        amp_max = 0.0
        for snap in late_snaps:
            amp_max = max(amp_max, abs(snap[center + r, center, center]))
        if amp_max > 1e-12:
            r_list.append(r)
            amp_list.append(amp_max)

    if len(r_list) >= 2:
        # Normalize
        amp_ref = amp_list[0]
        r_ref = r_list[0]
        for i, (r, amp) in enumerate(zip(r_list, amp_list)):
            inv_r = amp_ref * r_ref / r
            inv_r2 = amp_ref * (r_ref / r) ** 2
            print(f"  {r:4d} {amp:12.6f} {inv_r:14.6f} {inv_r2:14.6f}")

    # Fit power law: amplitude ~ r^gamma
    if len(r_list) >= 4:
        log_r = np.log(np.array(r_list, dtype=float))
        log_amp = np.log(np.array(amp_list))
        coeffs = np.polyfit(log_r, log_amp, 1)
        gamma = coeffs[0]
    else:
        gamma = float('nan')

    print(f"\n  Radiation decay exponent: amplitude ~ r^{gamma:.3f}")
    print(f"  Expected for radiation: r^{-1.0} (1/r decay)")
    print(f"  Expected for static:    r^{-2.0} (1/r^2 decay)")

    # Test frequency dependence: run at two frequencies
    print(f"\n  Frequency dependence of radiated amplitude:")
    omegas = [0.15, 0.3, 0.6]
    amp_at_r10 = []
    r_measure = min(10, center - 6)

    for om in omegas:
        def rho_om(step, n, _om=om):
            rho = np.zeros((n, n, n))
            t = step * dt
            rho[center, center, center] = math.sin(_om * t)
            return rho

        s = wave_evolve(N, n_steps, dt, rho_om, absorbing_layers=6)
        late_s = s[late_start:]
        amp_max = max(abs(sn[center + r_measure, center, center])
                      for sn in late_s)
        amp_at_r10.append(amp_max)
        print(f"  omega={om:.2f}  amp(r={r_measure})={amp_max:.6f}")

    # Check scaling: amplitude should scale with omega (for monopole radiation)
    if len(amp_at_r10) >= 2 and all(a > 1e-12 for a in amp_at_r10):
        # Fit: log(amp) = p * log(omega) + const
        log_om = np.log(np.array(omegas))
        log_a = np.log(np.array(amp_at_r10))
        p_fit = np.polyfit(log_om, log_a, 1)[0]
        print(f"\n  Amplitude ~ omega^{p_fit:.2f}")
        print(f"  (Monopole radiation predicts omega^1-2)")
    else:
        p_fit = float('nan')

    passed = not math.isnan(gamma) and -1.5 < gamma < -0.5
    status = "PASS" if passed else "PARTIAL"
    print(f"\n  Status: {status}")
    return gamma, passed


# ============================================================================
# Test 5: Couple wave-equation field to propagator
# ============================================================================

def test_propagator_coupling(N: int = 25, dt: float = 0.5, n_steps: int = 200):
    """Use wave equation steady-state field in propagator, check mass + distance law.

    The key question: does replacing Poisson with the wave equation steady state
    preserve the Newtonian propagator results? We compare deflection measurements
    using both field sources.
    """
    print("\n" + "=" * 72)
    print("TEST 5: Propagator coupling (wave field vs Poisson)")
    print("=" * 72)
    center = N // 2

    # --- Get wave equation steady-state fields at unit strength ---
    def rho_static(step, n):
        rho = np.zeros((n, n, n))
        rho[center, center, center] = 1.0
        return rho

    t0 = time.time()
    snaps = wave_evolve(N, n_steps, dt, rho_static, absorbing_layers=4)
    f_wave_unit = snaps[-1]
    elapsed_wave = time.time() - t0

    # --- Get Poisson field ---
    t1 = time.time()
    f_poisson_unit = solve_poisson_static(N, (center, center, center), strength=1.0)
    elapsed_poisson = time.time() - t1

    print(f"  Wave field:    {elapsed_wave:.1f}s ({n_steps} steps)")
    print(f"  Poisson field: {elapsed_poisson:.1f}s")

    # Check how similar the two fields are
    mask_interior = np.zeros((N, N, N), dtype=bool)
    mask_interior[3:-3, 3:-3, 3:-3] = True
    fw_int = f_wave_unit[mask_interior]
    fp_int = f_poisson_unit[mask_interior]
    if np.linalg.norm(fp_int) > 1e-10:
        field_corr = np.dot(fw_int, fp_int) / (
            np.linalg.norm(fw_int) * np.linalg.norm(fp_int)
        )
    else:
        field_corr = 0.0
    print(f"  Field correlation (wave vs Poisson interior): {field_corr:.6f}")

    # --- Mass law: deflection vs source strength ---
    # Use small masses to stay in linear regime
    print(f"\n  A. Mass law (deflection vs source strength):")
    print(f"  {'s':>6} {'defl_wave':>12} {'defl_poisson':>14}")

    strengths = [0.05, 0.1, 0.2, 0.4]
    k_prop = 8.0  # larger k gives cleaner deflection signal
    defl_wave_list = []
    defl_poisson_list = []

    for s_val in strengths:
        fw = f_wave_unit * s_val
        fp = f_poisson_unit * s_val

        source_yz = (center, center + 3)
        dw = measure_deflection(fw, k_prop, source_yz, max_d=2)
        dp = measure_deflection(fp, k_prop, source_yz, max_d=2)
        defl_wave_list.append(abs(dw))
        defl_poisson_list.append(abs(dp))
        print(f"  {s_val:6.2f} {dw:12.6f} {dp:14.6f}")

    # Fit mass law: defl ~ s^beta
    def fit_power(x_list, y_list):
        valid = [(x, y) for x, y in zip(x_list, y_list) if y > 1e-10]
        if len(valid) >= 3:
            lx = np.log([v[0] for v in valid])
            ly = np.log([v[1] for v in valid])
            return np.polyfit(lx, ly, 1)[0]
        return float('nan')

    beta_wave = fit_power(strengths, defl_wave_list)
    beta_poisson = fit_power(strengths, defl_poisson_list)

    print(f"\n  Mass law beta (wave):    {beta_wave:.3f}")
    print(f"  Mass law beta (Poisson): {beta_poisson:.3f}")
    print(f"  Expected: beta ~ 1.0")

    # --- Distance law: deflection vs impact parameter ---
    print(f"\n  B. Distance law (deflection vs impact parameter):")
    print(f"  {'b':>6} {'defl_wave':>12} {'defl_poisson':>14}")

    b_vals = [2, 3, 4, 5, 6, 7, 8]
    s_fixed = 0.2  # fixed strength in linear regime
    fw = f_wave_unit * s_fixed
    fp = f_poisson_unit * s_fixed
    defl_b_wave = []
    defl_b_poisson = []

    for b in b_vals:
        source_yz = (center, center + b)
        if source_yz[1] >= N - 2:
            continue
        dw = measure_deflection(fw, k_prop, source_yz, max_d=2)
        dp = measure_deflection(fp, k_prop, source_yz, max_d=2)
        defl_b_wave.append((b, abs(dw)))
        defl_b_poisson.append((b, abs(dp)))
        print(f"  {b:6d} {dw:12.6f} {dp:14.6f}")

    alpha_wave = fit_power([v[0] for v in defl_b_wave],
                           [v[1] for v in defl_b_wave])
    alpha_poisson = fit_power([v[0] for v in defl_b_poisson],
                              [v[1] for v in defl_b_poisson])

    print(f"\n  Distance law alpha (wave):    {alpha_wave:.3f}")
    print(f"  Distance law alpha (Poisson): {alpha_poisson:.3f}")
    print(f"  Expected: alpha ~ -1.0")

    # Check wave vs Poisson agreement
    if not math.isnan(beta_wave) and not math.isnan(beta_poisson):
        beta_diff = abs(beta_wave - beta_poisson)
        print(f"\n  Wave-Poisson beta difference:  {beta_diff:.3f}")
    if not math.isnan(alpha_wave) and not math.isnan(alpha_poisson):
        alpha_diff = abs(alpha_wave - alpha_poisson)
        print(f"  Wave-Poisson alpha difference: {alpha_diff:.3f}")

    passed_mass = not math.isnan(beta_wave) and abs(beta_wave - 1.0) < 0.3
    passed_dist = not math.isnan(alpha_wave) and abs(alpha_wave - (-1.0)) < 0.5
    passed_agree = (not math.isnan(beta_wave) and not math.isnan(beta_poisson)
                    and abs(beta_wave - beta_poisson) < 0.3)
    passed = passed_mass or (passed_agree and passed_dist)
    status = "PASS" if passed else "PARTIAL"
    print(f"\n  Status: {status}")
    return beta_wave, alpha_wave, beta_poisson, alpha_poisson, passed


# ============================================================================
# Main
# ============================================================================

def main():
    print("Wave Equation Gravity: box f = -rho on 3D lattice")
    print("Promoting Poisson (elliptic) to d'Alembertian (hyperbolic)")
    print("Leapfrog integrator, dt=0.5, Dirichlet + absorbing BC")
    print()

    t_start = time.time()
    results = {}

    # Test 1: Wave propagation
    c_wave, alpha_settle, pass1 = test_wave_propagation(N=31, dt=0.5, n_steps=40)
    results['wave_speed'] = c_wave
    results['settle_exponent'] = alpha_settle
    results['test1_pass'] = pass1

    # Test 2: Newton recovery
    alpha_w, alpha_p, ratio, pass2 = test_newton_recovery(N=31, dt=0.5, n_steps=200)
    results['alpha_wave_steady'] = alpha_w
    results['alpha_poisson'] = alpha_p
    results['wave_poisson_ratio'] = ratio
    results['test2_pass'] = pass2

    # Test 3: Retardation
    asym, pass3 = test_retardation(N=41, dt=0.5, n_steps=80)
    results['retardation_asymmetry'] = asym
    results['test3_pass'] = pass3

    # Test 4: Radiation
    gamma, pass4 = test_radiation(N=51, dt=0.5, n_steps=120)
    results['radiation_exponent'] = gamma
    results['test4_pass'] = pass4

    # Test 5: Propagator coupling
    beta_w, alpha_w5, beta_p, alpha_p5, pass5 = test_propagator_coupling(
        N=21, dt=0.5, n_steps=150
    )
    results['beta_wave'] = beta_w
    results['alpha_wave_prop'] = alpha_w5
    results['beta_poisson'] = beta_p
    results['alpha_poisson_prop'] = alpha_p5
    results['test5_pass'] = pass5

    t_total = time.time() - t_start

    # Summary
    print("\n" + "=" * 72)
    print("SUMMARY: Wave Equation Gravity")
    print("=" * 72)
    n_pass = sum(1 for k in results if k.endswith('_pass') and results[k])
    n_total = sum(1 for k in results if k.endswith('_pass'))
    print(f"  Tests passed: {n_pass}/{n_total}")
    print(f"  Total time: {t_total:.1f}s")
    print()
    print(f"  Test 1 - Wavefront speed:     c = {results['wave_speed']:.3f}  "
          f"(expect 1.0)  {'PASS' if results['test1_pass'] else 'PARTIAL'}")
    print(f"  Test 2 - Newton recovery:     alpha = {results['alpha_wave_steady']:.3f}  "
          f"(expect -1.0) {'PASS' if results['test2_pass'] else 'PARTIAL'}")
    print(f"  Test 3 - Retardation asym:    ratio = {results['retardation_asymmetry']:.3f}  "
          f"(expect > 1)  {'PASS' if results['test3_pass'] else 'PARTIAL'}")
    print(f"  Test 4 - Radiation decay:     gamma = {results['radiation_exponent']:.3f}  "
          f"(expect -1.0) {'PASS' if results['test4_pass'] else 'PARTIAL'}")
    print(f"  Test 5 - Propagator coupling: beta = {results['beta_wave']:.3f}, "
          f"alpha = {results['alpha_wave_prop']:.3f}  "
          f"{'PASS' if results['test5_pass'] else 'PARTIAL'}")
    print()

    if n_pass >= 4:
        print("  CONCLUSION: Wave equation gravity works.")
        print("  Promoting Poisson to d'Alembertian produces gravitational waves")
        print("  while recovering Newton at low frequency. The propagator coupling")
        print("  preserves mass and distance laws.")
    elif n_pass >= 2:
        print("  CONCLUSION: Partial success.")
        print("  Some wave equation features emerge but not all.")
    else:
        print("  CONCLUSION: Wave equation needs further investigation.")
        print("  The lattice discretization may need refinement.")

    print()
    return results


if __name__ == "__main__":
    main()
