#!/usr/bin/env python3
"""
Frontier: Chiral Distance Law Diagnosis + 3D Superposition Test
================================================================

TWO TESTS IN ONE SCRIPT:

Part 1: Distance law diagnosis on WIDE lattice
  The 1D chiral walk gives b^(-2.41) distance falloff. Why so steep?
  Measure delta(d) at d=1..15 on n_y=61, plus beam width at mass location.
  This maps the full distance curve and diagnoses the geometry factor.

Part 2: 3D chiral superposition
  The 1D chiral walk has 26% superposition error. The transfer matrix had 0.01%.
  Does the 2+1D chiral walk also have better superposition?
  Mass A at z=3, Mass B at z=7. Four configs: none, A, B, A+B.
  Measure centroid shift, compute superposition error.

HYPOTHESIS: "Distance exponent is geometry-dependent. 3D superposition error < 10%."
FALSIFICATION: "If 3D superposition error > 20%."
"""

from __future__ import annotations
import math
import time

import numpy as np


# ======================================================================
# PART 1: 1D CHIRAL WALK -- DISTANCE LAW DIAGNOSIS
# ======================================================================

N_Y_1D = 61
N_LAYERS_1D = 30
THETA_0_1D = 0.3
STRENGTH_1D = 5e-4
SOURCE_Y_1D = N_Y_1D // 2  # = 30


def make_field_1d(n_layers, n_y, strength, mass_y):
    """1/r field from mass at mass_y."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            field[x, y] = strength / (abs(y - mass_y) + 0.1)
    return field


def propagate_chiral_1d(n_y, n_layers, theta_0, field, source_y):
    """1D Lorentzian chiral walk. theta(y) = theta_0 * (1 - f(x,y))."""
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0  # right-mover at source

    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_y):
            f = field[x, y] if field is not None else 0.0
            th = theta_0 * (1.0 - f)
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(th) * pp - np.sin(th) * pm
            psi[idx_m] = np.sin(th) * pp + np.cos(th) * pm

        # Step 2: Shift with reflecting boundaries
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]
        psi = new_psi

    return psi


def detector_probs_1d(psi, n_y):
    """Total probability at each y site."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid_1d(probs):
    """Probability-weighted centroid."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.sum(ys * probs) / total)


def beam_width(probs, center):
    """RMS beam width around center."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    mean_sq = float(np.sum((ys - center) ** 2 * probs) / total)
    return math.sqrt(mean_sq)


def fit_power(x_data, y_data):
    """Fit log-log power law. Returns (slope, R^2)."""
    if len(x_data) < 3:
        return float('nan'), 0.0
    lx = np.log(np.array(x_data, dtype=float))
    ly = np.log(np.array(y_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx) ** 2)
    sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return float('nan'), 0.0
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx))) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(slope), float(r2)


# ======================================================================
# PART 2: 3D CHIRAL WALK -- SUPERPOSITION TEST
# ======================================================================

N_YZ = 13
N_LAYERS_3D = 15
THETA_0_3D = 0.3
STRENGTH_3D = 5e-4
SOURCE_Y_3D = 6
SOURCE_Z_3D = 6
MASS_Z_A = 3   # Mass A at z=3
MASS_Z_B = 7   # Mass B at z=7 (asymmetric, both on different sides)


def make_field_3d(n_layers, n_yz, strength, mass_z):
    """1/r field from a mass at z=mass_z (only z-dependence)."""
    field = np.zeros((n_layers, n_yz, n_yz))
    for x in range(n_layers):
        for y in range(n_yz):
            for z in range(n_yz):
                field[x, y, z] = strength / (abs(z - mass_z) + 0.1)
    return field


def chiral_propagate_3d(n_yz, n_layers, field_3d, theta_0, source_y, source_z):
    """
    3D chiral walk: 4 components per site (psi_+y, psi_-y, psi_+z, psi_-z).
    Lorentzian theta coupling: theta(y,z) = theta_0 * (1 - f(x,y,z)).
    """
    dim = 4 * n_yz * n_yz
    psi = np.zeros(dim, dtype=complex)
    src_idx = 4 * (source_y * n_yz + source_z)
    psi[src_idx + 0] = 1.0 / np.sqrt(2)  # +y
    psi[src_idx + 2] = 1.0 / np.sqrt(2)  # +z

    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_yz):
            for z in range(n_yz):
                f = field_3d[x, y, z]
                base = 4 * (y * n_yz + z)
                th = theta_0 * (1.0 - f)

                # Mix (psi_+y, psi_-y)
                p_py = psi[base + 0]
                p_my = psi[base + 1]
                psi[base + 0] = np.cos(th) * p_py - np.sin(th) * p_my
                psi[base + 1] = np.sin(th) * p_py + np.cos(th) * p_my

                # Mix (psi_+z, psi_-z)
                p_pz = psi[base + 2]
                p_mz = psi[base + 3]
                psi[base + 2] = np.cos(th) * p_pz - np.sin(th) * p_mz
                psi[base + 3] = np.sin(th) * p_pz + np.cos(th) * p_mz

        # Step 2: Shift with reflecting boundaries
        new_psi = np.zeros_like(psi)
        for y in range(n_yz):
            for z in range(n_yz):
                base = 4 * (y * n_yz + z)

                # psi_+y -> (y+1, z)
                if y + 1 < n_yz:
                    dst = 4 * ((y + 1) * n_yz + z)
                    new_psi[dst + 0] += psi[base + 0]
                else:
                    new_psi[base + 1] += psi[base + 0]

                # psi_-y -> (y-1, z)
                if y - 1 >= 0:
                    dst = 4 * ((y - 1) * n_yz + z)
                    new_psi[dst + 1] += psi[base + 1]
                else:
                    new_psi[base + 0] += psi[base + 1]

                # psi_+z -> (y, z+1)
                if z + 1 < n_yz:
                    dst = 4 * (y * n_yz + (z + 1))
                    new_psi[dst + 2] += psi[base + 2]
                else:
                    new_psi[base + 3] += psi[base + 2]

                # psi_-z -> (y, z-1)
                if z - 1 >= 0:
                    dst = 4 * (y * n_yz + (z - 1))
                    new_psi[dst + 3] += psi[base + 3]
                else:
                    new_psi[base + 2] += psi[base + 3]

        psi = new_psi

    return psi


def detector_probs_3d(psi, n_yz):
    """Probability at each (y, z): sum over all 4 chiralities."""
    probs = np.zeros((n_yz, n_yz))
    for y in range(n_yz):
        for z in range(n_yz):
            base = 4 * (y * n_yz + z)
            probs[y, z] = sum(abs(psi[base + c]) ** 2 for c in range(4))
    return probs


def centroid_z_3d(probs_2d):
    """Probability-weighted centroid in z direction."""
    n_y, n_z = probs_2d.shape
    total = probs_2d.sum()
    if total < 1e-30:
        return n_z / 2.0
    z_marginal = probs_2d.sum(axis=0)
    zs = np.arange(n_z)
    return float(np.sum(zs * z_marginal) / total)


# ======================================================================
# MAIN
# ======================================================================

def main():
    t_total = time.time()
    print("=" * 72)
    print("CHIRAL DISTANCE LAW DIAGNOSIS + 3D SUPERPOSITION TEST")
    print("=" * 72)
    print()

    # ==================================================================
    # PART 1: DISTANCE LAW DIAGNOSIS (1D, wide lattice)
    # ==================================================================
    print("=" * 72)
    print("PART 1: DISTANCE LAW DIAGNOSIS")
    print(f"  n_y={N_Y_1D}, n_layers={N_LAYERS_1D}, theta_0={THETA_0_1D}")
    print(f"  strength={STRENGTH_1D}, source_y={SOURCE_Y_1D}")
    print("=" * 72)
    print()

    offsets = list(range(1, 16))  # d=1 through d=15
    field_0 = np.zeros((N_LAYERS_1D, N_Y_1D))

    # Free propagation
    psi_free = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                    field_0, SOURCE_Y_1D)
    probs_free = detector_probs_1d(psi_free, N_Y_1D)
    c_free = centroid_1d(probs_free)
    w_free = beam_width(probs_free, c_free)
    print(f"  Free centroid: {c_free:.6f} (center={SOURCE_Y_1D})")
    print(f"  Free beam width (RMS): {w_free:.4f}")
    print()

    toward_count = 0
    toward_ds = []
    toward_deltas = []
    all_ds = []
    all_deltas = []
    all_widths = []

    print(f"  {'d':>3s}  {'y_mass':>6s}  {'centroid':>10s}  {'delta':>14s}  "
          f"{'|delta|':>12s}  {'beam_W':>8s}  {'dir':>6s}")
    print(f"  {'---':>3s}  {'------':>6s}  {'--------':>10s}  {'--------':>14s}  "
          f"{'--------':>12s}  {'------':>8s}  {'---':>6s}")

    for d in offsets:
        y_mass = SOURCE_Y_1D + d
        if y_mass >= N_Y_1D:
            print(f"  {d:3d}  SKIP (y_mass={y_mass} >= {N_Y_1D})")
            continue
        field_m = make_field_1d(N_LAYERS_1D, N_Y_1D, STRENGTH_1D, y_mass)
        psi_m = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                     field_m, SOURCE_Y_1D)
        probs_m = detector_probs_1d(psi_m, N_Y_1D)
        c_m = centroid_1d(probs_m)
        delta = c_m - c_free

        # Beam width at the mass location from the FREE walk
        # This tells us how much probability is near the mass
        w_at_mass = beam_width(probs_free, float(y_mass))

        direction = "TOWARD" if delta > 0 else "AWAY"
        if delta > 0:
            toward_count += 1
            toward_ds.append(d)
            toward_deltas.append(abs(delta))

        all_ds.append(d)
        all_deltas.append(delta)
        all_widths.append(w_at_mass)

        print(f"  {d:3d}  {y_mass:6d}  {c_m:10.6f}  {delta:14.10f}  "
              f"{abs(delta):12.2e}  {w_at_mass:8.4f}  {direction:>6s}")

    print()
    total_pts = len(all_ds)
    print(f"  TOWARD: {toward_count}/{total_pts}, "
          f"AWAY: {total_pts - toward_count}/{total_pts}")

    # Power law fit on TOWARD points
    if len(toward_ds) >= 3:
        slope_t, r2_t = fit_power(toward_ds, toward_deltas)
        print(f"  Power-law fit (TOWARD): slope={slope_t:.3f}, R^2={r2_t:.4f}")

    # Power law fit on ALL |delta| (regardless of sign)
    abs_all = [abs(d) for d in all_deltas]
    if len(all_ds) >= 3:
        slope_all, r2_all = fit_power(all_ds, abs_all)
        print(f"  Power-law fit (ALL |delta|): slope={slope_all:.3f}, R^2={r2_all:.4f}")

    # Measure free beam probability profile at different distances from source
    print()
    print("  --- Free beam probability at mass locations ---")
    print(f"  {'d':>3s}  {'P(y_mass)':>12s}  {'P(d)/P(1)':>12s}")
    print(f"  {'---':>3s}  {'--------':>12s}  {'--------':>12s}")
    p_at_1 = probs_free[SOURCE_Y_1D + 1] if SOURCE_Y_1D + 1 < N_Y_1D else 0
    for d in offsets:
        y_mass = SOURCE_Y_1D + d
        if y_mass >= N_Y_1D:
            break
        p_at_d = probs_free[y_mass]
        ratio = p_at_d / p_at_1 if p_at_1 > 1e-30 else 0
        print(f"  {d:3d}  {p_at_d:12.6e}  {ratio:12.6f}")

    # Fit beam falloff
    beam_ds = []
    beam_ps = []
    for d in offsets:
        y_mass = SOURCE_Y_1D + d
        if y_mass >= N_Y_1D:
            break
        p = probs_free[y_mass]
        if p > 1e-30:
            beam_ds.append(d)
            beam_ps.append(p)
    if len(beam_ds) >= 3:
        slope_beam, r2_beam = fit_power(beam_ds, beam_ps)
        print(f"  Beam probability falloff: slope={slope_beam:.3f}, R^2={r2_beam:.4f}")
        print(f"  => Beam P(d) ~ d^{slope_beam:.2f}")

    print()

    # ==================================================================
    # PART 2: 3D CHIRAL SUPERPOSITION TEST
    # ==================================================================
    print("=" * 72)
    print("PART 2: 3D CHIRAL SUPERPOSITION TEST")
    print(f"  n_yz={N_YZ}, n_layers={N_LAYERS_3D}, theta_0={THETA_0_3D}")
    print(f"  strength={STRENGTH_3D}")
    print(f"  source=(y={SOURCE_Y_3D}, z={SOURCE_Z_3D})")
    print(f"  Mass A at z={MASS_Z_A}, Mass B at z={MASS_Z_B}")
    print("=" * 72)
    print()

    # Build fields
    field_none = np.zeros((N_LAYERS_3D, N_YZ, N_YZ))
    field_A = make_field_3d(N_LAYERS_3D, N_YZ, STRENGTH_3D, MASS_Z_A)
    field_B = make_field_3d(N_LAYERS_3D, N_YZ, STRENGTH_3D, MASS_Z_B)
    field_AB = field_A + field_B  # additive superposition

    # Run 4 configs
    configs = {
        "no mass": field_none,
        "mass A (z=3)": field_A,
        "mass B (z=7)": field_B,
        "mass A+B": field_AB,
    }

    centroids = {}
    norms = {}
    for name, field in configs.items():
        t0 = time.time()
        psi = chiral_propagate_3d(N_YZ, N_LAYERS_3D, field, THETA_0_3D,
                                   SOURCE_Y_3D, SOURCE_Z_3D)
        probs = detector_probs_3d(psi, N_YZ)
        cz = centroid_z_3d(probs)
        norm = probs.sum()
        elapsed = time.time() - t0
        centroids[name] = cz
        norms[name] = norm
        print(f"  {name:>15s}: centroid_z = {cz:.8f}, norm = {norm:.8e}  "
              f"({elapsed:.1f}s)")

    print()

    # Compute shifts
    c0 = centroids["no mass"]
    delta_A = centroids["mass A (z=3)"] - c0
    delta_B = centroids["mass B (z=7)"] - c0
    delta_AB = centroids["mass A+B"] - c0
    delta_sum = delta_A + delta_B

    print(f"  delta_A  = {delta_A:+.8e}")
    print(f"  delta_B  = {delta_B:+.8e}")
    print(f"  delta_AB = {delta_AB:+.8e}")
    print(f"  delta_A + delta_B = {delta_sum:+.8e}")
    print()

    # Directions
    # Mass A at z=3, source at z=6: TOWARD means delta_z < 0
    dir_A = "TOWARD" if delta_A < 0 else "AWAY"
    # Mass B at z=7, source at z=6: TOWARD means delta_z > 0
    dir_B = "TOWARD" if delta_B > 0 else "AWAY"
    print(f"  Mass A direction: {dir_A} (mass at z={MASS_Z_A}, source z={SOURCE_Z_3D})")
    print(f"  Mass B direction: {dir_B} (mass at z={MASS_Z_B}, source z={SOURCE_Z_3D})")
    print()

    # Superposition error
    if abs(delta_sum) > 1e-30:
        sup_error = abs(delta_AB - delta_sum) / abs(delta_sum)
        print(f"  Superposition error = |delta_AB - (delta_A + delta_B)| / |delta_A + delta_B|")
        print(f"                      = {abs(delta_AB - delta_sum):.6e} / {abs(delta_sum):.6e}")
        print(f"                      = {sup_error:.4f} ({sup_error*100:.2f}%)")
    else:
        # If delta_sum ~ 0, use absolute comparison
        sup_error_abs = abs(delta_AB - delta_sum)
        print(f"  delta_A + delta_B ~ 0, using absolute error")
        print(f"  |delta_AB - delta_sum| = {sup_error_abs:.6e}")
        # Relative to max single shift
        max_single = max(abs(delta_A), abs(delta_B))
        if max_single > 1e-30:
            sup_error = sup_error_abs / max_single
            print(f"  Relative to max single shift: {sup_error:.4f} ({sup_error*100:.2f}%)")
        else:
            sup_error = 0.0

    print()

    # Also compute 1D superposition for comparison
    print("  --- 1D superposition comparison ---")
    # Use d=4 and d=8 to avoid symmetry
    field_1d_0 = np.zeros((N_LAYERS_1D, N_Y_1D))
    y_mass_1d_A = SOURCE_Y_1D + 4
    y_mass_1d_B = SOURCE_Y_1D + 8

    field_1d_A = make_field_1d(N_LAYERS_1D, N_Y_1D, STRENGTH_1D, y_mass_1d_A)
    field_1d_B = make_field_1d(N_LAYERS_1D, N_Y_1D, STRENGTH_1D, y_mass_1d_B)
    field_1d_AB = field_1d_A + field_1d_B

    psi_1d_0 = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                    field_1d_0, SOURCE_Y_1D)
    c_1d_0 = centroid_1d(detector_probs_1d(psi_1d_0, N_Y_1D))

    psi_1d_A = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                    field_1d_A, SOURCE_Y_1D)
    c_1d_A = centroid_1d(detector_probs_1d(psi_1d_A, N_Y_1D))

    psi_1d_B = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                    field_1d_B, SOURCE_Y_1D)
    c_1d_B = centroid_1d(detector_probs_1d(psi_1d_B, N_Y_1D))

    psi_1d_AB = propagate_chiral_1d(N_Y_1D, N_LAYERS_1D, THETA_0_1D,
                                     field_1d_AB, SOURCE_Y_1D)
    c_1d_AB = centroid_1d(detector_probs_1d(psi_1d_AB, N_Y_1D))

    d1_A = c_1d_A - c_1d_0
    d1_B = c_1d_B - c_1d_0
    d1_AB = c_1d_AB - c_1d_0
    d1_sum = d1_A + d1_B

    print(f"  1D: delta_A={d1_A:+.8e}, delta_B={d1_B:+.8e}")
    print(f"  1D: delta_AB={d1_AB:+.8e}, delta_A+B={d1_sum:+.8e}")
    if abs(d1_sum) > 1e-30:
        sup_1d = abs(d1_AB - d1_sum) / abs(d1_sum)
        print(f"  1D superposition error: {sup_1d:.4f} ({sup_1d*100:.2f}%)")
    else:
        sup_1d_abs = abs(d1_AB - d1_sum)
        max_1d = max(abs(d1_A), abs(d1_B))
        if max_1d > 1e-30:
            sup_1d = sup_1d_abs / max_1d
            print(f"  1D superposition error (rel to max): {sup_1d:.4f} ({sup_1d*100:.2f}%)")

    print()

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)

    print()
    print("Part 1 -- Distance law diagnosis:")
    print(f"  Lattice: n_y={N_Y_1D}, L={N_LAYERS_1D}")
    print(f"  Free beam width: {w_free:.4f}")
    print(f"  TOWARD: {toward_count}/{total_pts}")
    if len(toward_ds) >= 3:
        print(f"  TOWARD power law: slope={slope_t:.3f}, R^2={r2_t:.4f}")
    if len(all_ds) >= 3:
        print(f"  ALL |delta| power law: slope={slope_all:.3f}, R^2={r2_all:.4f}")
    if len(beam_ds) >= 3:
        print(f"  Free beam P(d): slope={slope_beam:.3f}")
        print(f"  => If delta ~ P(d) * (1/d), expect slope ~ {slope_beam - 1:.1f}")

    print()
    print("Part 2 -- 3D superposition:")
    print(f"  Mass A direction: {dir_A}")
    print(f"  Mass B direction: {dir_B}")
    print(f"  3D superposition error: {sup_error*100:.2f}%")
    sup_pass = sup_error < 0.10
    sup_falsified = sup_error > 0.20
    print(f"  PASS (<10%): {sup_pass}")
    print(f"  FALSIFIED (>20%): {sup_falsified}")

    print()
    elapsed_total = time.time() - t_total
    print(f"  Total time: {elapsed_total:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
