#!/usr/bin/env python3
"""
Frontier: Three Remaining Gaps in One Script
=============================================================

Gap 1 -- Why is the distance exponent -0.6 instead of -1.0?
  Hypothesis: beam probability at distance d grows as ~d^beta,
  so effective coupling = field(d) * beam_prob(d) ~ d^(alpha_field + beta).
  Measure beam_prob profile, compare delta(d) vs effective_coupling(d).

Gap 2 -- 3D chiral superposition (never tested)
  Two masses at z=center+3 and z=center+5. Additive fields.
  Compute superposition error.

Gap 3 -- Decoherence scaling on chiral
  Does the chiral walk have a CLT ceiling?
  Run at N=10,15,20,25,30, measure bath purity from two-path overlap.

HYPOTHESIS: "Distance exponent comes from beam spreading.
             3D superposition < 5%. Decoherence persists at all N."
"""

from __future__ import annotations
import math
import time

import numpy as np


# ======================================================================
# SHARED UTILITIES
# ======================================================================

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
# 1D CHIRAL WALK
# ======================================================================

def make_field_1d(n_layers, n_y, strength, mass_y):
    """1/r field from mass at mass_y."""
    field = np.zeros((n_layers, n_y))
    ys = np.arange(n_y, dtype=float)
    for x in range(n_layers):
        field[x, :] = strength / (np.abs(ys - mass_y) + 0.1)
    return field


def propagate_chiral_1d(n_y, n_layers, theta_0, field, source_y):
    """1D chiral walk with Lorentzian coupling."""
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0  # right-mover at source

    for x in range(n_layers):
        # Coin
        for y in range(n_y):
            f = field[x, y] if field is not None else 0.0
            th = theta_0 * (1.0 - f)
            i_p = 2 * y
            i_m = 2 * y + 1
            pp, pm = psi[i_p], psi[i_m]
            psi[i_p] = np.cos(th) * pp - np.sin(th) * pm
            psi[i_m] = np.sin(th) * pp + np.cos(th) * pm

        # Shift with reflecting boundaries
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
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid_1d(probs):
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.sum(ys * probs) / total)


# ======================================================================
# 3D CHIRAL WALK
# ======================================================================

def make_field_3d(n_layers, n_yz, strength, mass_z):
    """1/r field from a mass at z=mass_z (z-dependence only)."""
    field = np.zeros((n_layers, n_yz, n_yz))
    zs = np.arange(n_yz, dtype=float)
    for x in range(n_layers):
        for y in range(n_yz):
            field[x, y, :] = strength / (np.abs(zs - mass_z) + 0.1)
    return field


def propagate_chiral_3d(n_yz, n_layers, theta_0, field, source_y, source_z):
    """3D chiral walk: 4 components per (y,z) site."""
    dim = 4 * n_yz * n_yz
    psi = np.zeros(dim, dtype=complex)
    src = 4 * (source_y * n_yz + source_z)
    psi[src + 0] = 1.0 / np.sqrt(2)
    psi[src + 2] = 1.0 / np.sqrt(2)

    for x in range(n_layers):
        for y in range(n_yz):
            for z in range(n_yz):
                f = field[x, y, z]
                base = 4 * (y * n_yz + z)
                th = theta_0 * (1.0 - f)
                # Mix (+y, -y)
                p_py, p_my = psi[base], psi[base + 1]
                psi[base] = np.cos(th) * p_py - np.sin(th) * p_my
                psi[base + 1] = np.sin(th) * p_py + np.cos(th) * p_my
                # Mix (+z, -z)
                p_pz, p_mz = psi[base + 2], psi[base + 3]
                psi[base + 2] = np.cos(th) * p_pz - np.sin(th) * p_mz
                psi[base + 3] = np.sin(th) * p_pz + np.cos(th) * p_mz

        # Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_yz):
            for z in range(n_yz):
                base = 4 * (y * n_yz + z)
                # +y -> (y+1, z)
                if y + 1 < n_yz:
                    dst = 4 * ((y + 1) * n_yz + z)
                    new_psi[dst] += psi[base]
                else:
                    new_psi[base + 1] += psi[base]
                # -y -> (y-1, z)
                if y - 1 >= 0:
                    dst = 4 * ((y - 1) * n_yz + z)
                    new_psi[dst + 1] += psi[base + 1]
                else:
                    new_psi[base] += psi[base + 1]
                # +z -> (y, z+1)
                if z + 1 < n_yz:
                    dst = 4 * (y * n_yz + (z + 1))
                    new_psi[dst + 2] += psi[base + 2]
                else:
                    new_psi[base + 3] += psi[base + 2]
                # -z -> (y, z-1)
                if z - 1 >= 0:
                    dst = 4 * (y * n_yz + (z - 1))
                    new_psi[dst + 3] += psi[base + 3]
                else:
                    new_psi[base + 2] += psi[base + 3]
        psi = new_psi

    return psi


def detector_probs_3d(psi, n_yz):
    probs = np.zeros((n_yz, n_yz))
    for y in range(n_yz):
        for z in range(n_yz):
            base = 4 * (y * n_yz + z)
            probs[y, z] = sum(abs(psi[base + c]) ** 2 for c in range(4))
    return probs


def centroid_z_3d(probs_2d):
    total = probs_2d.sum()
    if total < 1e-30:
        return probs_2d.shape[1] / 2.0
    z_marginal = probs_2d.sum(axis=0)
    zs = np.arange(probs_2d.shape[1])
    return float(np.sum(zs * z_marginal) / total)


# ======================================================================
# DECOHERENCE PURITY (two-path Gram matrix)
# ======================================================================

def bath_purity_1d(psi_a, psi_b, n_y, dcl=0.5):
    """Purity of bath (detector) from two-path overlap.

    Gram matrix G_ij = <psi_i | psi_j>.
    Mix matrix M = [[1, dcl], [dcl, 1]] (classical limit parameter).
    rho = M . G  (unnormalized).
    Purity = Tr(rho^2) / Tr(rho)^2.
    """
    a_amp = np.concatenate([psi_a[2*y:2*y+2] for y in range(n_y)])
    b_amp = np.concatenate([psi_b[2*y:2*y+2] for y in range(n_y)])
    gram = np.array([
        [np.vdot(a_amp, a_amp), np.vdot(a_amp, b_amp)],
        [np.vdot(b_amp, a_amp), np.vdot(b_amp, b_amp)],
    ], dtype=np.complex128)
    mix = np.array([[1.0, dcl], [dcl, 1.0]], dtype=np.complex128)
    mg = mix @ gram
    tr = np.trace(mg).real
    if tr <= 1e-30:
        return 1.0
    return float((np.trace(mg @ mg) / (tr * tr)).real)


# ======================================================================
# MAIN
# ======================================================================

def main():
    t_total = time.time()
    print("=" * 72)
    print("THREE REMAINING GAPS")
    print("=" * 72)
    print()

    # ------------------------------------------------------------------
    # GAP 1: WHY IS THE DISTANCE EXPONENT -0.6?
    # ------------------------------------------------------------------
    print("=" * 72)
    print("GAP 1: DISTANCE EXPONENT DECOMPOSITION")
    print("  Hypothesis: delta(d) ~ field(d) * beam_prob(d)")
    print("  field(d) ~ 1/d, beam_prob(d) ~ d^beta => delta ~ d^(-1 + beta)")
    print("=" * 72)
    print()

    N_Y = 61
    N_LAYERS = 30
    THETA_0 = 0.3
    STRENGTH = 5e-4
    SOURCE = N_Y // 2

    # Free propagation (flat space)
    field_flat = np.zeros((N_LAYERS, N_Y))
    psi_free = propagate_chiral_1d(N_Y, N_LAYERS, THETA_0, field_flat, SOURCE)
    probs_free = detector_probs_1d(psi_free, N_Y)
    c_free = centroid_1d(probs_free)
    print(f"  Free centroid: {c_free:.6f} (source={SOURCE})")
    print()

    # Use even distances only -- chiral walk has parity: odd-distance sites
    # have zero probability after even number of steps.
    # Also measure cumulative beam probability in a window around each d.
    distances = list(range(2, 16))
    deltas = []
    beam_probs = []
    fields_at_d = []
    eff_couplings = []
    used_ds = []

    print(f"  {'d':>3}  {'delta':>14}  {'beam_P(d)':>12}  {'beam_cum':>12}  "
          f"{'field(d)':>12}  {'eff_coup':>12}  {'dir':>6}")
    print(f"  {'---':>3}  {'-----':>14}  {'---------':>12}  {'--------':>12}  "
          f"{'--------':>12}  {'--------':>12}  {'---':>6}")

    for d in distances:
        y_mass = SOURCE + d
        if y_mass >= N_Y:
            break

        # Deflection with mass at y_mass
        field_m = make_field_1d(N_LAYERS, N_Y, STRENGTH, y_mass)
        psi_m = propagate_chiral_1d(N_Y, N_LAYERS, THETA_0, field_m, SOURCE)
        probs_m = detector_probs_1d(psi_m, N_Y)
        c_m = centroid_1d(probs_m)
        delta = c_m - c_free

        # Beam probability: cumulative in window [y_mass-1, y_mass+1]
        # This avoids the parity zero problem
        lo = max(0, y_mass - 1)
        hi = min(N_Y, y_mass + 2)
        bp_cum = probs_free[lo:hi].sum()

        bp_point = probs_free[y_mass]

        # Field strength at mass location
        f_d = STRENGTH / (d + 0.1)

        # Effective coupling = field * cumulative beam prob
        ec = f_d * bp_cum

        direction = "TOWARD" if delta > 0 else "AWAY"

        deltas.append(abs(delta))
        beam_probs.append(bp_cum)
        fields_at_d.append(f_d)
        eff_couplings.append(ec)
        used_ds.append(d)

        print(f"  {d:3d}  {delta:14.10f}  {bp_point:12.6e}  {bp_cum:12.6e}  "
              f"{f_d:12.6e}  {ec:12.6e}  {direction:>6}")

    print()

    # Power law fits (filter to nonzero values)
    valid_idx = [i for i in range(len(used_ds))
                 if deltas[i] > 1e-30 and beam_probs[i] > 1e-30]
    valid_ds = [used_ds[i] for i in valid_idx]
    valid_deltas = [deltas[i] for i in valid_idx]
    valid_bp = [beam_probs[i] for i in valid_idx]
    valid_ec = [eff_couplings[i] for i in valid_idx]

    if len(valid_ds) >= 3:
        alpha_delta, r2_delta = fit_power(valid_ds, valid_deltas)
        alpha_beam, r2_beam = fit_power(valid_ds, valid_bp)
        alpha_eff, r2_eff = fit_power(valid_ds, valid_ec)

        print(f"  |delta(d)| exponent:      alpha = {alpha_delta:.3f}  (R2={r2_delta:.3f})")
        print(f"  beam_prob_cum(d) exponent: beta  = {alpha_beam:.3f}  (R2={r2_beam:.3f})")
        print(f"  eff_coupling(d) exponent:  gamma = {alpha_eff:.3f}  (R2={r2_eff:.3f})")
        print()
        print(f"  Prediction: alpha ~ -1 + beta = {-1 + alpha_beam:.3f}")
        print(f"  Actual alpha:                  = {alpha_delta:.3f}")
        residual = abs(alpha_delta - (-1 + alpha_beam))
        print(f"  Residual |alpha - (-1+beta)|:  = {residual:.3f}")
        print(f"  MATCH (within 0.3): {residual < 0.3}")
        print()

        # Correlation: does delta track eff_coupling?
        log_delta = np.log(np.array(valid_deltas))
        log_ec = np.log(np.array(valid_ec))
        corr = np.corrcoef(log_delta, log_ec)[0, 1]
        print(f"  Correlation(log|delta|, log(eff_coupling)): {corr:.4f}")

    print()

    # ------------------------------------------------------------------
    # GAP 2: 3D CHIRAL SUPERPOSITION
    # ------------------------------------------------------------------
    print("=" * 72)
    print("GAP 2: 3D CHIRAL SUPERPOSITION")
    print("=" * 72)
    print()

    N_YZ = 21
    N_LAYERS_3D = 16
    THETA_3D = 0.3
    STR_3D = 5e-4
    SRC_Y = N_YZ // 2
    SRC_Z = N_YZ // 2
    MASS_Z_A = SRC_Z + 3
    MASS_Z_B = SRC_Z + 5

    print(f"  n_yz={N_YZ}, N={N_LAYERS_3D}, source=({SRC_Y},{SRC_Z})")
    print(f"  Mass A at z={MASS_Z_A}, Mass B at z={MASS_Z_B}")
    print()

    # Build fields
    field_none = np.zeros((N_LAYERS_3D, N_YZ, N_YZ))
    field_A = make_field_3d(N_LAYERS_3D, N_YZ, STR_3D, MASS_Z_A)
    field_B = make_field_3d(N_LAYERS_3D, N_YZ, STR_3D, MASS_Z_B)
    field_AB = field_A + field_B

    configs = {
        "no mass": field_none,
        "mass A": field_A,
        "mass B": field_B,
        "mass A+B": field_AB,
    }

    centroids_3d = {}
    for name, field in configs.items():
        t0 = time.time()
        psi = propagate_chiral_3d(N_YZ, N_LAYERS_3D, THETA_3D, field, SRC_Y, SRC_Z)
        probs = detector_probs_3d(psi, N_YZ)
        cz = centroid_z_3d(probs)
        norm = probs.sum()
        elapsed = time.time() - t0
        centroids_3d[name] = cz
        print(f"  {name:>10s}: centroid_z={cz:.8f}, norm={norm:.6e} ({elapsed:.1f}s)")

    print()

    c0 = centroids_3d["no mass"]
    dA = centroids_3d["mass A"] - c0
    dB = centroids_3d["mass B"] - c0
    dAB = centroids_3d["mass A+B"] - c0
    dsum = dA + dB

    print(f"  delta_A  = {dA:+.8e}")
    print(f"  delta_B  = {dB:+.8e}")
    print(f"  delta_AB = {dAB:+.8e}")
    print(f"  delta_A + delta_B = {dsum:+.8e}")
    print()

    # Directions (both masses at z > source, so TOWARD means delta > 0)
    dir_A = "TOWARD" if dA > 0 else "AWAY"
    dir_B = "TOWARD" if dB > 0 else "AWAY"
    print(f"  Mass A (z={MASS_Z_A}): {dir_A}")
    print(f"  Mass B (z={MASS_Z_B}): {dir_B}")

    if abs(dsum) > 1e-30:
        sup_err = abs(dAB - dsum) / abs(dsum)
        print(f"  Superposition error: {sup_err*100:.4f}%")
    else:
        max_single = max(abs(dA), abs(dB))
        if max_single > 1e-30:
            sup_err = abs(dAB - dsum) / max_single
            print(f"  Superposition error (rel to max): {sup_err*100:.4f}%")
        else:
            sup_err = 0.0
            print("  Both shifts are zero -- cannot compute error")

    print()

    # ------------------------------------------------------------------
    # GAP 3: DECOHERENCE SCALING ON CHIRAL
    # ------------------------------------------------------------------
    print("=" * 72)
    print("GAP 3: DECOHERENCE (PURITY) SCALING")
    print("  Two-path purity vs N.  CLT ceiling => purity -> 1 as N -> inf")
    print("=" * 72)
    print()

    N_Y_DEC = 61
    THETA_DEC = 0.3
    # Use stronger field to see decoherence more clearly
    STR_DEC = 5e-2
    SOURCE_DEC = N_Y_DEC // 2
    MASS_OFFSET_A = 3
    MASS_OFFSET_B = 5
    DCL = 0.5  # classical mixing parameter

    N_values = [10, 15, 20, 25, 30, 40, 50]

    print(f"  n_y={N_Y_DEC}, theta={THETA_DEC}, strength={STR_DEC}")
    print(f"  Path A: mass at source+{MASS_OFFSET_A}")
    print(f"  Path B: mass at source+{MASS_OFFSET_B}")
    print(f"  dcl={DCL}")
    print()
    print(f"  {'N':>4}  {'purity':>14}  {'1-purity':>14}  {'delta_centroid':>14}  {'time':>6}")
    print(f"  {'----':>4}  {'------':>14}  {'--------':>14}  {'--------------':>14}  {'----':>6}")

    purities = []
    for N in N_values:
        t0 = time.time()
        y_mass_a = SOURCE_DEC + MASS_OFFSET_A
        y_mass_b = SOURCE_DEC + MASS_OFFSET_B

        field_a = make_field_1d(N, N_Y_DEC, STR_DEC, y_mass_a)
        field_b = make_field_1d(N, N_Y_DEC, STR_DEC, y_mass_b)

        psi_a = propagate_chiral_1d(N_Y_DEC, N, THETA_DEC, field_a, SOURCE_DEC)
        psi_b = propagate_chiral_1d(N_Y_DEC, N, THETA_DEC, field_b, SOURCE_DEC)

        pur = bath_purity_1d(psi_a, psi_b, N_Y_DEC, DCL)

        # Also compute centroid difference as a sanity check
        probs_a = detector_probs_1d(psi_a, N_Y_DEC)
        probs_b = detector_probs_1d(psi_b, N_Y_DEC)
        dc = abs(centroid_1d(probs_a) - centroid_1d(probs_b))

        elapsed = time.time() - t0
        purities.append(pur)
        print(f"  {N:4d}  {pur:14.10f}  {1-pur:14.6e}  {dc:14.10f}  {elapsed:5.1f}s")

    print()

    # Check trend
    if purities[-1] > purities[0]:
        trend = "INCREASING (approaching CLT ceiling)"
    elif purities[-1] < purities[0]:
        trend = "DECREASING (decoherence grows with N)"
    else:
        trend = "FLAT"

    print(f"  Purity trend: {trend}")
    print(f"  Purity at N={N_values[0]}: {purities[0]:.6f}")
    print(f"  Purity at N={N_values[-1]}: {purities[-1]:.6f}")
    print(f"  Change: {purities[-1] - purities[0]:+.6f}")
    print()

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()

    print("Gap 1 -- Distance exponent decomposition:")
    if len(valid_ds) >= 3:
        print(f"  |delta(d)| ~ d^{alpha_delta:.2f}")
        print(f"  beam_prob_cum(d) ~ d^{alpha_beam:.2f}")
        print(f"  Predicted: alpha = -1 + beta = {-1 + alpha_beam:.2f}")
        print(f"  Actual:    alpha = {alpha_delta:.2f}")
        residual_sum = abs(alpha_delta - (-1 + alpha_beam))
        print(f"  MATCH (within 0.3): {residual_sum < 0.3}")
    print()

    print("Gap 2 -- 3D chiral superposition:")
    print(f"  Mass A: {dir_A}, Mass B: {dir_B}")
    print(f"  Superposition error: {sup_err*100:.4f}%")
    print(f"  PASS (<5%): {sup_err < 0.05}")
    print()

    print("Gap 3 -- Decoherence scaling:")
    print(f"  Purity trend: {trend}")
    print(f"  Purity range: [{min(purities):.4f}, {max(purities):.4f}]")
    ceiling = all(p > 0.99 for p in purities)
    decoherence_grows = purities[-1] < purities[0] - 0.001
    print(f"  CLT ceiling (all purity > 0.99): {ceiling}")
    print(f"  Decoherence grows with N: {decoherence_grows}")
    print()

    elapsed_total = time.time() - t_total
    print(f"Total time: {elapsed_total:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
