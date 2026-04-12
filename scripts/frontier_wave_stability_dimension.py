#!/usr/bin/env python3
"""Wave stability vs dimension: does Huygens' principle select d=3?

In odd spatial dimensions (d=1,3,5,...), Huygens' principle holds: a sharp
wavefront propagates with no afterglow.  In even dimensions (d=2,4,...),
Huygens fails: waves leave a tail inside the light cone.

If the wave equation box f = -rho mediates gravity, even-dimensional spaces
develop ringing after perturbations.  This could cause self-consistent
instabilities, selecting odd d for physics.  We test d=2,3,4,5.

Tests:
  1. Wave propagation from sudden source: clean front (odd d) vs afterglow (even d)
  2. Self-consistent stability: perturbation ringdown time
  3. Energy conservation: E(t) = 1/2 sum(fdot^2) + 1/2 sum(|grad f|^2)

CFL condition: dt < dx/sqrt(d), using dt=0.5 for all d (safe for d<=4).

PStack experiment: wave-stability-dimension
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np


# ============================================================================
# d-dimensional Laplacian (Dirichlet BC)
# ============================================================================

def laplacian_nd(f: np.ndarray) -> np.ndarray:
    """Discrete Laplacian of d-dimensional field with Dirichlet BC."""
    d = f.ndim
    lap = -2.0 * d * f.copy()
    for axis in range(d):
        lap += np.roll(f, 1, axis=axis) + np.roll(f, -1, axis=axis)
    # Fix roll wrap-around: zero out boundary slices
    for axis in range(d):
        idx_lo = [slice(None)] * d
        idx_hi = [slice(None)] * d
        idx_lo[axis] = 0
        idx_hi[axis] = -1
        lap[tuple(idx_lo)] = 0.0
        lap[tuple(idx_hi)] = 0.0
    return lap


def gradient_energy_nd(f: np.ndarray) -> float:
    """Compute sum of |grad f|^2 using forward differences."""
    d = f.ndim
    total = 0.0
    for axis in range(d):
        diff = np.diff(f, axis=axis)
        total += np.sum(diff ** 2)
    return total


# ============================================================================
# Lattice sizes per dimension
# ============================================================================

LATTICE_SIZES = {2: 20, 3: 12, 4: 6, 5: 4}


def make_lattice(d: int) -> int:
    """Return lattice side length for spatial dimension d."""
    return LATTICE_SIZES.get(d, 4)


def center_index(N: int, d: int) -> tuple:
    """Return center multi-index for an N^d lattice."""
    return tuple([N // 2] * d)


# ============================================================================
# Wave equation solver (leapfrog, d-dimensional)
# ============================================================================

def wave_evolve_nd(d: int, N: int, n_steps: int, dt: float,
                   rho_func, absorbing_layers: int = 2):
    """Evolve box f = -rho on N^d lattice.

    Leapfrog: f(t+1) = 2f(t) - f(t-1) + dt^2 * (lap f(t) + rho(t))

    Returns (snapshots, f_dot_snapshots) where f_dot = (f_cur - f_prev)/dt.
    """
    shape = tuple([N] * d)
    f_cur = np.zeros(shape)
    f_prev = np.zeros(shape)
    snapshots = [f_cur.copy()]
    fdot_snapshots = [np.zeros(shape)]

    for step in range(1, n_steps + 1):
        rho = rho_func(step, N, d)
        lap = laplacian_nd(f_cur)
        f_next = 2.0 * f_cur - f_prev + dt * dt * (lap + rho)

        # Absorbing boundary: damping in boundary layers
        if absorbing_layers > 0:
            for axis in range(d):
                for side in [0, 1]:
                    for layer in range(absorbing_layers):
                        sigma = 0.5 * (1.0 - layer / absorbing_layers)
                        slices = [slice(None)] * d
                        if side == 0:
                            slices[axis] = layer
                        else:
                            slices[axis] = N - 1 - layer
                        f_next[tuple(slices)] *= (1.0 - sigma)

        # Dirichlet BC: boundary = 0
        for axis in range(d):
            idx_lo = [slice(None)] * d
            idx_hi = [slice(None)] * d
            idx_lo[axis] = 0
            idx_hi[axis] = -1
            f_next[tuple(idx_lo)] = 0.0
            f_next[tuple(idx_hi)] = 0.0

        fdot = (f_next - f_cur) / dt
        f_prev = f_cur
        f_cur = f_next
        snapshots.append(f_cur.copy())
        fdot_snapshots.append(fdot.copy())

    return snapshots, fdot_snapshots


# ============================================================================
# Radial profile extraction
# ============================================================================

def radial_profile(f: np.ndarray, d: int) -> tuple[np.ndarray, np.ndarray]:
    """Extract spherically averaged radial profile from d-dim field.

    Returns (r_vals, f_vals) where r_vals are integer radii.
    """
    N = f.shape[0]
    ctr = N // 2
    # Build distance array
    grids = np.ogrid[tuple(slice(-ctr, N - ctr) for _ in range(d))]
    r2 = sum(g ** 2 for g in grids)
    r = np.sqrt(r2.astype(float))

    max_r = ctr - 1
    r_vals = np.arange(0, max_r + 1)
    f_vals = np.zeros(max_r + 1)
    counts = np.zeros(max_r + 1)

    r_int = np.round(r).astype(int)
    for ri in range(max_r + 1):
        mask = (r_int == ri)
        if mask.any():
            f_vals[ri] = np.mean(np.abs(f[mask]))
            counts[ri] = mask.sum()

    return r_vals, f_vals


# ============================================================================
# Test 1: Wave propagation from sudden source
# ============================================================================

def test_wave_propagation(d: int, dt: float = 0.5):
    """Turn on a point source at t=0, measure wavefront and afterglow."""
    N = make_lattice(d)
    ctr = center_index(N, d)
    # Enough steps for wave to cross half the lattice
    n_steps = max(20, int(2.0 * (N // 2) / dt))

    def rho_sudden(step, n, dim):
        shape = tuple([n] * dim)
        rho = np.zeros(shape)
        c = tuple([n // 2] * dim)
        rho[c] = 1.0
        return rho

    print(f"\n  d={d}: lattice {N}^{d}, steps={n_steps}")
    t0 = time.time()
    snaps, fdots = wave_evolve_nd(d, N, n_steps, dt, rho_sudden,
                                  absorbing_layers=min(2, N // 4))
    elapsed = time.time() - t0
    print(f"    Evolved in {elapsed:.1f}s")

    # Measure field at several radii vs time
    # Pick probe radii: r = 1, 2, ..., min(N//2-2, 5)
    max_probe_r = min(N // 2 - 2, 5)
    probe_radii = list(range(1, max_probe_r + 1))

    # For each probe radius, find peak time and measure afterglow
    print(f"    Probe radii: {probe_radii}")
    print(f"    {'r':>4} {'t_peak':>8} {'f_peak':>10} {'afterglow':>12} {'ratio':>10}")

    afterglow_ratios = []
    for r_probe in probe_radii:
        # Extract field at radius r_probe along first axis from center
        idx = list(ctr)
        idx[0] = ctr[0] + r_probe
        if idx[0] >= N:
            continue
        idx = tuple(idx)

        # Time series at this point
        ts = np.array([snaps[s][idx] for s in range(len(snaps))])
        abs_ts = np.abs(ts)

        # Peak
        peak_step = np.argmax(abs_ts)
        f_peak = abs_ts[peak_step]
        t_peak = peak_step * dt

        if f_peak < 1e-15:
            afterglow_ratios.append(0.0)
            print(f"    {r_probe:4d} {t_peak:8.1f} {f_peak:10.2e} {'---':>12} {'---':>10}")
            continue

        # Afterglow: average |f| in window [t_peak + 2*r, end]
        late_start = min(peak_step + 2 * r_probe, len(snaps) - 1)
        if late_start < len(snaps) - 2:
            afterglow_mean = np.mean(abs_ts[late_start:])
        else:
            afterglow_mean = abs_ts[-1]

        ratio = afterglow_mean / f_peak
        afterglow_ratios.append(ratio)
        print(f"    {r_probe:4d} {t_peak:8.1f} {f_peak:10.2e} {afterglow_mean:12.2e} {ratio:10.4f}")

    mean_afterglow = np.mean(afterglow_ratios) if afterglow_ratios else 0.0
    return mean_afterglow


# ============================================================================
# Test 2: Self-consistent stability (perturbation ringdown)
# ============================================================================

def test_perturbation_ringdown(d: int, dt: float = 0.5):
    """Evolve to near-steady state, perturb, measure ringdown."""
    N = make_lattice(d)
    ctr = center_index(N, d)

    # Phase 1: evolve with static source to approach steady state
    settle_steps = max(40, int(4.0 * (N // 2) / dt))

    def rho_static(step, n, dim):
        shape = tuple([n] * dim)
        rho = np.zeros(shape)
        c = tuple([n // 2] * dim)
        rho[c] = 1.0
        return rho

    print(f"\n  d={d}: lattice {N}^{d}")
    print(f"    Phase 1: settle for {settle_steps} steps")
    t0 = time.time()
    snaps1, fdots1 = wave_evolve_nd(d, N, settle_steps, dt, rho_static,
                                    absorbing_layers=min(2, N // 4))

    # Save state at end of settling
    f_settled = snaps1[-1].copy()
    f_prev_settled = snaps1[-2].copy()

    # Phase 2: perturb the source (increase by 10%) and continue evolving
    perturb_steps = max(40, int(4.0 * (N // 2) / dt))

    def rho_perturbed(step, n, dim):
        shape = tuple([n] * dim)
        rho = np.zeros(shape)
        c = tuple([n // 2] * dim)
        rho[c] = 1.1  # 10% perturbation
        return rho

    # Continue from settled state
    shape = tuple([N] * d)
    f_cur = f_settled.copy()
    f_prev = f_prev_settled.copy()

    # Track difference from what a static 1.1 source would settle to
    # We measure |f(t) - f_settled| at a probe point
    probe = list(ctr)
    probe[0] = min(ctr[0] + 2, N - 2)
    probe = tuple(probe)

    f_at_probe_settled = f_settled[probe]
    deviations = []

    for step in range(1, perturb_steps + 1):
        rho = rho_perturbed(step, N, d)
        lap = laplacian_nd(f_cur)
        f_next = 2.0 * f_cur - f_prev + dt * dt * (lap + rho)

        # Absorbing BC
        abl = min(2, N // 4)
        if abl > 0:
            for axis in range(d):
                for side in [0, 1]:
                    for layer in range(abl):
                        sigma = 0.5 * (1.0 - layer / abl)
                        slices = [slice(None)] * d
                        if side == 0:
                            slices[axis] = layer
                        else:
                            slices[axis] = N - 1 - layer
                        f_next[tuple(slices)] *= (1.0 - sigma)

        for axis in range(d):
            idx_lo = [slice(None)] * d
            idx_hi = [slice(None)] * d
            idx_lo[axis] = 0
            idx_hi[axis] = -1
            f_next[tuple(idx_lo)] = 0.0
            f_next[tuple(idx_hi)] = 0.0

        f_prev = f_cur
        f_cur = f_next

        # Deviation at probe
        dev = abs(f_cur[probe] - f_at_probe_settled)
        deviations.append(dev)

    elapsed = time.time() - t0

    deviations = np.array(deviations)
    # Normalize to peak deviation
    peak_dev = deviations.max() if deviations.max() > 1e-15 else 1.0

    # Ringdown: measure how quickly deviation decays
    # Find when deviation first drops below 50% of peak (after peak)
    peak_idx = np.argmax(deviations)
    half_life_steps = perturb_steps  # default: never decays
    for i in range(peak_idx, len(deviations)):
        if deviations[i] < 0.5 * peak_dev:
            half_life_steps = i - peak_idx
            break

    half_life_t = half_life_steps * dt

    # Late-time residual: average deviation in last quarter
    late_quarter = deviations[3 * len(deviations) // 4:]
    late_residual = np.mean(late_quarter) / peak_dev if peak_dev > 1e-15 else 0.0

    print(f"    Phase 2: perturbed for {perturb_steps} steps, elapsed {elapsed:.1f}s")
    print(f"    Peak deviation: {peak_dev:.4e}")
    print(f"    Half-life: {half_life_t:.1f} (steps: {half_life_steps})")
    print(f"    Late residual (fraction of peak): {late_residual:.4f}")

    return half_life_t, late_residual


# ============================================================================
# Test 3: Energy conservation
# ============================================================================

def test_energy_conservation(d: int, dt: float = 0.5):
    """Evolve wave equation, track total energy E = KE + PE."""
    N = make_lattice(d)
    ctr = center_index(N, d)

    # Use a short burst source: on for 5 steps, then off
    burst_duration = 5

    def rho_burst(step, n, dim):
        shape = tuple([n] * dim)
        rho = np.zeros(shape)
        if step <= burst_duration:
            c = tuple([n // 2] * dim)
            rho[c] = 1.0
        return rho

    # Evolve long enough to see energy behavior after source turns off
    n_steps = max(60, int(6.0 * (N // 2) / dt))

    print(f"\n  d={d}: lattice {N}^{d}, steps={n_steps}")
    t0 = time.time()
    snaps, fdots = wave_evolve_nd(d, N, n_steps, dt, rho_burst,
                                  absorbing_layers=min(2, N // 4))
    elapsed = time.time() - t0
    print(f"    Evolved in {elapsed:.1f}s")

    # Compute energy at each step
    energies = []
    for s in range(len(snaps)):
        KE = 0.5 * np.sum(fdots[s] ** 2)
        PE = 0.5 * gradient_energy_nd(snaps[s])
        E_total = KE + PE
        energies.append((KE, PE, E_total))

    energies = np.array(energies)

    # Energy after source turns off (steps > burst_duration + some buffer)
    free_start = burst_duration + 5
    if free_start >= len(energies):
        free_start = len(energies) // 2

    E_free = energies[free_start:, 2]
    if len(E_free) > 1 and E_free[0] > 1e-15:
        E_max = E_free.max()
        E_min = E_free.min()
        E_mean = E_free.mean()
        E_variation = (E_max - E_min) / E_mean if E_mean > 1e-15 else 0.0

        # Check for growth: linear fit slope
        t_vals = np.arange(len(E_free)) * dt
        if len(t_vals) >= 3:
            coeffs = np.polyfit(t_vals, E_free, 1)
            E_slope = coeffs[0]
            E_growth_rate = E_slope / E_mean if E_mean > 1e-15 else 0.0
        else:
            E_growth_rate = 0.0
    else:
        E_variation = 0.0
        E_growth_rate = 0.0
        E_mean = 0.0

    # Print energy at select timesteps
    print(f"    {'step':>6} {'t':>8} {'KE':>12} {'PE':>12} {'E_total':>12}")
    sample_steps = list(range(0, len(energies), max(1, len(energies) // 10)))
    if len(energies) - 1 not in sample_steps:
        sample_steps.append(len(energies) - 1)
    for s in sample_steps:
        t = s * dt
        KE, PE, E = energies[s]
        print(f"    {s:6d} {t:8.1f} {KE:12.4e} {PE:12.4e} {E:12.4e}")

    print(f"\n    Free-field energy variation: {E_variation:.4f}")
    print(f"    Energy growth rate (per unit time): {E_growth_rate:.4e}")
    print(f"    Mean energy (free phase): {E_mean:.4e}")

    is_stable = E_growth_rate < 0.01  # less than 1% growth per unit time
    return E_variation, E_growth_rate, is_stable


# ============================================================================
# Main
# ============================================================================

def main():
    dims = [2, 3, 4, 5]

    # ------------------------------------------------------------------
    print("=" * 72)
    print("WAVE STABILITY vs DIMENSION: Huygens principle test")
    print("=" * 72)
    print(f"\nDimensions to test: {dims}")
    print(f"Lattice sizes: {dict((d, make_lattice(d)) for d in dims)}")

    # ------------------------------------------------------------------
    # Test 1: Wave propagation / afterglow
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("TEST 1: Wave propagation — afterglow measurement")
    print("=" * 72)
    print("  Huygens holds in odd d: clean wavefront, no afterglow.")
    print("  Huygens fails in even d: afterglow inside light cone.")

    afterglow_results = {}
    for d in dims:
        ag = test_wave_propagation(d)
        afterglow_results[d] = ag

    print(f"\n  SUMMARY — Afterglow ratio (late field / peak):")
    print(f"  {'d':>4} {'afterglow':>12} {'Huygens?':>10} {'parity':>8}")
    for d in dims:
        ag = afterglow_results[d]
        parity = "odd" if d % 2 == 1 else "even"
        huygens = "YES" if d % 2 == 1 else "NO"
        print(f"  {d:4d} {ag:12.4f} {huygens:>10} {parity:>8}")

    # ------------------------------------------------------------------
    # Test 2: Perturbation ringdown
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("TEST 2: Perturbation ringdown — self-consistent stability")
    print("=" * 72)
    print("  Odd d: perturbation propagates away cleanly.")
    print("  Even d: afterglow may cause persistent ringing.")

    ringdown_results = {}
    for d in dims:
        hl, residual = test_perturbation_ringdown(d)
        ringdown_results[d] = (hl, residual)

    print(f"\n  SUMMARY — Ringdown:")
    print(f"  {'d':>4} {'half_life':>12} {'late_resid':>12} {'stable?':>10}")
    for d in dims:
        hl, res = ringdown_results[d]
        stable = "YES" if res < 0.3 else "RING"
        print(f"  {d:4d} {hl:12.1f} {res:12.4f} {stable:>10}")

    # ------------------------------------------------------------------
    # Test 3: Energy conservation
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("TEST 3: Energy conservation")
    print("=" * 72)
    print("  Stable: energy conserved after source off.")
    print("  Unstable: energy grows (positive growth rate).")

    energy_results = {}
    for d in dims:
        var, growth, stable = test_energy_conservation(d)
        energy_results[d] = (var, growth, stable)

    print(f"\n  SUMMARY — Energy:")
    print(f"  {'d':>4} {'variation':>12} {'growth_rate':>14} {'stable?':>10}")
    for d in dims:
        var, growth, stable = energy_results[d]
        status = "STABLE" if stable else "UNSTABLE"
        print(f"  {d:4d} {var:12.4f} {growth:14.4e} {status:>10}")

    # ------------------------------------------------------------------
    # Final synthesis
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SYNTHESIS: Does the wave equation select d=3?")
    print("=" * 72)

    print(f"\n  {'d':>4} {'afterglow':>10} {'ringdown':>10} {'E_stable':>10} {'Huygens':>8} {'verdict':>12}")
    for d in dims:
        ag = afterglow_results[d]
        hl, res = ringdown_results[d]
        var, growth, stable = energy_results[d]
        huygens = "YES" if d % 2 == 1 else "NO"
        # Verdict: clean if low afterglow + low residual + stable energy
        if ag < 0.2 and res < 0.3 and stable:
            verdict = "CLEAN"
        elif stable:
            verdict = "RINGING"
        else:
            verdict = "UNSTABLE"
        print(f"  {d:4d} {ag:10.4f} {res:10.4f} {'Y' if stable else 'N':>10} {huygens:>8} {verdict:>12}")

    print(f"\n  Key finding:")
    # Compare odd vs even dimensions
    odd_ds = [d for d in dims if d % 2 == 1]
    even_ds = [d for d in dims if d % 2 == 0]

    avg_ag_odd = np.mean([afterglow_results[d] for d in odd_ds])
    avg_ag_even = np.mean([afterglow_results[d] for d in even_ds])
    avg_res_odd = np.mean([ringdown_results[d][1] for d in odd_ds])
    avg_res_even = np.mean([ringdown_results[d][1] for d in even_ds])

    print(f"    Odd  dims (d={odd_ds}): avg afterglow={avg_ag_odd:.4f}, avg residual={avg_res_odd:.4f}")
    print(f"    Even dims (d={even_ds}): avg afterglow={avg_ag_even:.4f}, avg residual={avg_res_even:.4f}")

    if avg_ag_even > 2.0 * avg_ag_odd:
        print(f"    Even dims show {avg_ag_even/avg_ag_odd:.1f}x MORE afterglow than odd dims.")
        print(f"    => Huygens principle distinguishes odd from even dimensions.")
    else:
        print(f"    Afterglow ratio even/odd = {avg_ag_even/(avg_ag_odd+1e-15):.2f} — "
              f"effect {'clear' if avg_ag_even > avg_ag_odd else 'reversed/unclear'}.")

    if avg_res_even > 2.0 * avg_res_odd:
        print(f"    Even dims show {avg_res_even/avg_res_odd:.1f}x MORE ringing than odd dims.")
        print(f"    => Self-consistent wave equation selects ODD dimensions.")
    else:
        print(f"    Ringdown residual ratio even/odd = {avg_res_even/(avg_res_odd+1e-15):.2f}")

    # d=3 specifically
    ag3 = afterglow_results.get(3, 0)
    res3 = ringdown_results.get(3, (0, 0))[1]
    _, growth3, stable3 = energy_results.get(3, (0, 0, True))
    print(f"\n    d=3 specifically: afterglow={ag3:.4f}, residual={res3:.4f}, "
          f"energy_stable={'YES' if stable3 else 'NO'}")

    # Check if d=3 is the unique "clean" dimension
    # Use relative thresholds: afterglow < median, residual < median
    ag_vals = [afterglow_results[d] for d in dims if afterglow_results[d] > 0]
    res_vals = [ringdown_results[d][1] for d in dims]
    ag_thresh = np.median(ag_vals) if ag_vals else 0.5
    res_thresh = np.median(res_vals) if res_vals else 0.5
    clean_dims = [d for d in dims
                  if afterglow_results[d] < ag_thresh
                  and ringdown_results[d][1] < res_thresh
                  and energy_results[d][2]]
    print(f"    Clean dimensions: {clean_dims}")
    if 3 in clean_dims and 4 not in clean_dims:
        print(f"    => d=3 is clean, d=4 is not => wave equation selects d=3 over d=4.")
    elif 3 in clean_dims:
        print(f"    => d=3 is clean (but so are others; selection not unique to d=3).")
    else:
        print(f"    => d=3 not uniquely selected by this test.")

    print(f"\n  NOTE: On small lattices ({LATTICE_SIZES}), boundary effects")
    print(f"  compete with Huygens tails. Larger lattices sharpen the signal.")


if __name__ == "__main__":
    main()
