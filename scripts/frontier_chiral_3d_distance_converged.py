#!/usr/bin/env python3
"""Distance law in the converged 3D chiral walk regime (n=21, N=16).

Measure how the gravitational centroid shift scales with distance between
source and mass, and verify F proportional to M at each distance.

SETUP:
  - 21x21 transverse grid, 16 propagation layers
  - Periodic BC, symmetric Lorentzian coin (theta coupling)
  - Source at center (10, 10), mass at z offsets {2..8}
  - Balanced source: equal +y and +z chiralities

DISTANCE SCAN:
  For mass_offset in {2, 3, 4, 5, 6, 7, 8}:
    Run 3D chiral walk, measure gravity delta (toward metric).

  Fit TOWARD points to power law: delta = A / offset^alpha.

F-PROP-M AT EACH DISTANCE:
  For each offset, sweep strength {1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4}:
    Measure delta, fit alpha.

HYPOTHESIS: "Distance law has a well-defined exponent in the converged regime."
FALSIFICATION: "If half the offsets are AWAY even in the converged regime."
"""

from __future__ import annotations

import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


# ── Parameters ────────────────────────────────────────────────────────
N_YZ = 21
N_LAYERS = 16
THETA0 = 0.30
THETA_GAIN = -1.0  # theta = theta0*(1 + (-1)*f) = theta0*(1-f), matching convergence test
SOFTENING = 0.25
SOURCE_Y = 10
SOURCE_Z = 10
MASS_OFFSETS = [2, 3, 4, 5, 6, 7, 8]
STRENGTH_DEFAULT = 5e-4
FM_STRENGTHS = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4]
MASS_X = N_LAYERS // 2  # mass at layer center


def site_base(n_yz: int, y: int, z: int) -> int:
    return 4 * (y * n_yz + z)


def make_localized_field_3d(
    n_layers: int,
    n_yz: int,
    strength: float,
    x_mass: int,
    y_mass: int,
    z_mass: int,
) -> np.ndarray:
    """Localized 1/r field from a point mass at (x_mass, y_mass, z_mass)."""
    field = np.zeros((n_layers, n_yz, n_yz), dtype=float)
    for x in range(n_layers):
        for y in range(n_yz):
            for z in range(n_yz):
                r2 = ((x - x_mass) ** 2
                      + (y - y_mass) ** 2
                      + (z - z_mass) ** 2)
                field[x, y, z] = strength / math.sqrt(r2 + SOFTENING)
    return field


def propagate_3d(field: np.ndarray) -> tuple[np.ndarray, list[float]]:
    """3D chiral walk with periodic BC and symmetric Lorentzian coin.

    State: 4 components per site (+y, -y, +z, -z).
    Coin: symmetric 2x2 rotation with theta = theta0*(1 + gain*f).
    Shift: periodic wrap in both y and z.
    """
    dim = 4 * N_YZ * N_YZ
    psi = np.zeros(dim, dtype=complex)
    base = site_base(N_YZ, SOURCE_Y, SOURCE_Z)
    # Balanced source: equal +y and +z
    psi[base + 0] = 1.0 / math.sqrt(2.0)
    psi[base + 2] = 1.0 / math.sqrt(2.0)
    norms = [float(np.sum(np.abs(psi) ** 2))]

    for x in range(N_LAYERS):
        # Coin step
        for y in range(N_YZ):
            for z in range(N_YZ):
                base = site_base(N_YZ, y, z)
                f = field[x, y, z]
                theta = THETA0 * (1.0 + THETA_GAIN * f)
                c = math.cos(theta)
                s = math.sin(theta)

                p_py, p_my = psi[base + 0], psi[base + 1]
                p_pz, p_mz = psi[base + 2], psi[base + 3]
                psi[base + 0] = c * p_py - s * p_my
                psi[base + 1] = s * p_py + c * p_my
                psi[base + 2] = c * p_pz - s * p_mz
                psi[base + 3] = s * p_pz + c * p_mz

        # Shift step with periodic wrap
        new_psi = np.zeros_like(psi)
        for y in range(N_YZ):
            yp = (y + 1) % N_YZ
            ym = (y - 1) % N_YZ
            for z in range(N_YZ):
                zp = (z + 1) % N_YZ
                zm = (z - 1) % N_YZ
                base = site_base(N_YZ, y, z)

                dst = site_base(N_YZ, yp, z)
                new_psi[dst + 0] += psi[base + 0]

                dst = site_base(N_YZ, ym, z)
                new_psi[dst + 1] += psi[base + 1]

                dst = site_base(N_YZ, y, zp)
                new_psi[dst + 2] += psi[base + 2]

                dst = site_base(N_YZ, y, zm)
                new_psi[dst + 3] += psi[base + 3]

        psi = new_psi
        norms.append(float(np.sum(np.abs(psi) ** 2)))

    return psi, norms


def detector_probs_3d(psi: np.ndarray) -> np.ndarray:
    probs = np.zeros((N_YZ, N_YZ), dtype=float)
    for y in range(N_YZ):
        for z in range(N_YZ):
            base = site_base(N_YZ, y, z)
            probs[y, z] = float(np.sum(np.abs(psi[base:base + 4]) ** 2))
    return probs


def centroid_z(probs: np.ndarray) -> float:
    z_marginal = probs.sum(axis=0)
    total = float(z_marginal.sum())
    zs = np.arange(len(z_marginal), dtype=float)
    return float(np.dot(zs, z_marginal) / total) if total > 1e-30 else len(z_marginal) / 2.0


def toward_delta(c_flat: float, c_field: float, mass_z: int) -> float:
    """Positive = centroid moved TOWARD mass, negative = AWAY."""
    return abs(c_flat - mass_z) - abs(c_field - mass_z)


def fit_power_law(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Fit |y| = A * x^alpha in log-log space. Returns (alpha, R^2)."""
    arr = np.array(ys, dtype=float)
    signs = np.sign(arr)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        return float("nan"), 0.0
    log_x = np.log10(np.array(xs, dtype=float))
    log_y = np.log10(np.abs(arr))
    coeffs = np.polyfit(log_x, log_y, 1)
    alpha = float(coeffs[0])
    pred = np.polyval(coeffs, log_x)
    ss_res = float(np.sum((log_y - pred) ** 2))
    ss_tot = float(np.sum((log_y - np.mean(log_y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return alpha, r2


def run_single(strength: float, mass_z: int) -> tuple[float, float, float, float]:
    """Run one (flat, field) pair. Returns (c_flat, c_field, delta_toward, max_norm_dev)."""
    field = make_localized_field_3d(N_LAYERS, N_YZ, strength, MASS_X, SOURCE_Y, mass_z)
    field0 = np.zeros_like(field)
    psi_0, norms0 = propagate_3d(field0)
    psi_f, normsf = propagate_3d(field)
    probs_0 = detector_probs_3d(psi_0)
    probs_f = detector_probs_3d(psi_f)
    c0 = centroid_z(probs_0)
    cf = centroid_z(probs_f)
    delta = toward_delta(c0, cf, mass_z)
    max_dev = max(
        max(abs(v - 1.0) for v in norms0),
        max(abs(v - 1.0) for v in normsf),
    )
    return c0, cf, delta, max_dev


def main() -> None:
    t0 = time.time()
    print("=" * 78)
    print("FRONTIER: 3D CHIRAL DISTANCE LAW (CONVERGED REGIME)")
    print("=" * 78)
    print(f"Grid: {N_YZ}x{N_YZ}, layers={N_LAYERS}")
    print(f"Source: (y={SOURCE_Y}, z={SOURCE_Z})")
    print(f"theta0={THETA0}, theta_gain={THETA_GAIN}, softening={SOFTENING}")
    print(f"Mass x={MASS_X}, y={SOURCE_Y} (same as source y)")
    print(f"Mass z offsets: {MASS_OFFSETS}")
    print(f"Default strength: {STRENGTH_DEFAULT}")
    print(f"F-prop-M strengths: {FM_STRENGTHS}")
    print("Periodic BC, symmetric Lorentzian coin, balanced source.")
    print()

    # ── Part 1: Distance profile at default strength ──────────────
    print("=" * 78)
    print("PART 1: DISTANCE PROFILE (strength = {:.1e})".format(STRENGTH_DEFAULT))
    print("=" * 78)
    print(f"{'offset':>7} {'mass_z':>7} {'c_flat':>10} {'c_field':>10} "
          f"{'delta':>12} {'dir':>7} {'norm_dev':>10}")
    print("-" * 78)

    offsets_toward = []
    deltas_toward = []
    all_results = {}

    for offset in MASS_OFFSETS:
        mass_z = SOURCE_Z - offset  # mass below source
        c0, cf, delta, dev = run_single(STRENGTH_DEFAULT, mass_z)
        direction = "TOWARD" if delta > 0 else ("AWAY" if delta < 0 else "NONE")
        all_results[offset] = (mass_z, c0, cf, delta, direction, dev)

        if delta > 0:
            offsets_toward.append(offset)
            deltas_toward.append(delta)

        print(f"{offset:>7d} {mass_z:>7d} {c0:>10.6f} {cf:>10.6f} "
              f"{delta:>+12.6e} {direction:>7} {dev:>10.2e}")

    toward_count = sum(1 for r in all_results.values() if r[4] == "TOWARD")
    away_count = sum(1 for r in all_results.values() if r[4] == "AWAY")
    print(f"\nTOWARD: {toward_count}/{len(MASS_OFFSETS)}, "
          f"AWAY: {away_count}/{len(MASS_OFFSETS)}")

    # ── Distance law fit ──────────────────────────────────────────
    print("\n" + "=" * 78)
    print("PART 2: DISTANCE LAW FIT (TOWARD points only)")
    print("=" * 78)

    if len(offsets_toward) >= 3:
        alpha_dist, r2_dist = fit_power_law(
            [float(o) for o in offsets_toward], deltas_toward
        )
        print(f"Fit: delta ~ offset^alpha")
        print(f"  alpha = {alpha_dist:.4f}")
        print(f"  R^2   = {r2_dist:.6f}")
        print(f"  N_pts = {len(offsets_toward)}")

        # Print individual fit residuals
        if not math.isnan(alpha_dist):
            log_o = np.log10(np.array(offsets_toward, dtype=float))
            log_d = np.log10(np.abs(np.array(deltas_toward)))
            coeffs = np.polyfit(log_o, log_d, 1)
            pred = np.polyval(coeffs, log_o)
            print(f"\n{'offset':>7} {'log(delta)':>12} {'predicted':>12} {'residual':>12}")
            for i, o in enumerate(offsets_toward):
                print(f"{o:>7d} {log_d[i]:>12.6f} {pred[i]:>12.6f} "
                      f"{log_d[i] - pred[i]:>+12.6f}")
    else:
        alpha_dist = float("nan")
        r2_dist = 0.0
        print(f"Insufficient TOWARD points for fit ({len(offsets_toward)} < 3)")

    # Also fit ALL points (using abs delta)
    all_offsets = list(all_results.keys())
    all_deltas = [all_results[o][3] for o in all_offsets]
    all_abs = [abs(d) for d in all_deltas]
    if all(d > 0 for d in all_abs):
        alpha_all, r2_all = fit_power_law(
            [float(o) for o in all_offsets], all_abs
        )
        print(f"\nFit over ALL points (abs delta):")
        print(f"  alpha = {alpha_all:.4f}, R^2 = {r2_all:.6f}")

    # ── Part 3: F-prop-M at each distance ─────────────────────────
    print("\n" + "=" * 78)
    print("PART 3: F-PROP-M AT EACH DISTANCE")
    print("=" * 78)
    print("For each offset, sweep strength and fit delta vs strength.")
    print()

    fm_results = {}

    for offset in MASS_OFFSETS:
        mass_z = SOURCE_Z - offset
        print(f"  offset={offset}, mass_z={mass_z}:")

        str_deltas = []
        str_dirs = []
        for s in FM_STRENGTHS:
            _, _, delta, _ = run_single(s, mass_z)
            direction = "TOWARD" if delta > 0 else ("AWAY" if delta < 0 else "NONE")
            str_deltas.append(delta)
            str_dirs.append(direction)
            print(f"    s={s:.1e}: delta={delta:+.6e}  {direction}")

        # Fit alpha for this offset
        alpha_fm, r2_fm = fit_power_law(FM_STRENGTHS, str_deltas)
        toward_ct = sum(1 for d in str_dirs if d == "TOWARD")
        fm_results[offset] = (alpha_fm, r2_fm, toward_ct, len(FM_STRENGTHS))

        print(f"    => alpha={alpha_fm:.4f}, R^2={r2_fm:.6f}, "
              f"TOWARD {toward_ct}/{len(FM_STRENGTHS)}")
        print()

    # ── F-prop-M summary ──────────────────────────────────────────
    print("=" * 78)
    print("F-PROP-M SUMMARY (want alpha ~ 1.0 for linearity)")
    print("=" * 78)
    print(f"{'offset':>7} {'alpha':>8} {'R^2':>8} {'toward':>10} {'verdict':>10}")
    print("-" * 50)

    fm_pass_count = 0
    for offset in MASS_OFFSETS:
        alpha_fm, r2_fm, tw, tot = fm_results[offset]
        linear = abs(alpha_fm - 1.0) < 0.25 and r2_fm > 0.95
        if linear:
            fm_pass_count += 1
        verdict = "LINEAR" if linear else "NONLIN"
        if math.isnan(alpha_fm):
            verdict = "NO_FIT"
        print(f"{offset:>7d} {alpha_fm:>8.4f} {r2_fm:>8.4f} "
              f"{tw}/{tot:>7} {verdict:>10}")

    # ── Final summary ─────────────────────────────────────────────
    elapsed = time.time() - t0
    print("\n" + "=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78)

    print(f"\n  Distance profile:")
    print(f"    TOWARD: {toward_count}/{len(MASS_OFFSETS)} offsets")
    if not math.isnan(alpha_dist):
        print(f"    Distance exponent: alpha = {alpha_dist:.4f} (R^2 = {r2_dist:.6f})")
    else:
        print(f"    Distance exponent: could not fit")

    print(f"\n  F-prop-M linearity:")
    print(f"    Linear (alpha~1) at {fm_pass_count}/{len(MASS_OFFSETS)} offsets")

    # Hypothesis testing
    half = len(MASS_OFFSETS) // 2
    hyp_dist = toward_count > half
    hyp_fm = fm_pass_count > half

    print(f"\n  HYPOTHESIS (well-defined distance exponent):")
    if hyp_dist and not math.isnan(alpha_dist):
        print(f"    SUPPORTED: {toward_count}/{len(MASS_OFFSETS)} TOWARD, "
              f"alpha={alpha_dist:.3f}")
    else:
        print(f"    FALSIFIED: only {toward_count}/{len(MASS_OFFSETS)} TOWARD")

    print(f"\n  FALSIFICATION criterion (>= half AWAY):")
    if away_count >= half:
        print(f"    TRIGGERED: {away_count}/{len(MASS_OFFSETS)} AWAY")
    else:
        print(f"    NOT triggered: only {away_count}/{len(MASS_OFFSETS)} AWAY")

    print(f"\n  F-prop-M holds everywhere?")
    if hyp_fm:
        print(f"    YES: linear at {fm_pass_count}/{len(MASS_OFFSETS)} distances")
    else:
        print(f"    NO: linear at only {fm_pass_count}/{len(MASS_OFFSETS)} distances")

    print(f"\n  Runtime: {elapsed:.1f}s")
    print("=" * 78)


if __name__ == "__main__":
    main()
