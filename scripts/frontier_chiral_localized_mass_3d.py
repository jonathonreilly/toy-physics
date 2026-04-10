#!/usr/bin/env python3
"""Localized 3D chiral mass harness on a periodic unitary walk.

This is a 2+1D spacetime chiral walk:
  - propagation direction x (layer index)
  - two transverse directions y, z
  - four local chiral components (+y, -y, +z, -z)

The field is localized at a point (x_mass, y_mass, z_mass), and enters
through the local mixing angle:

  theta_eff(x, y, z) = theta0 * (1 + theta_gain * field(x, y, z))

with periodic wrap in y and z so the local coin+shift update remains exactly
unitary and boundary reflections do not contaminate the baseline.
"""

from __future__ import annotations

import math

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


N_YZ = 15
N_LAYERS = 18
THETA0 = 0.30
THETA_GAIN = 0.80
STRENGTH = 5e-3
SOFTENING = 0.25
SOURCE_Y = 7
SOURCE_Z = 10
MASS_X = 10
MASS_Y = 7
MASS_Z = 5
K_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]


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
    field = np.zeros((n_layers, n_yz, n_yz), dtype=float)
    for x in range(n_layers):
        for y in range(n_yz):
            for z in range(n_yz):
                r2 = ((x - x_mass) ** 2 +
                      (y - y_mass) ** 2 +
                      (z - z_mass) ** 2)
                field[x, y, z] = strength / math.sqrt(r2 + SOFTENING)
    return field


def propagate_3d_theta(field: np.ndarray) -> tuple[np.ndarray, list[float]]:
    dim = 4 * N_YZ * N_YZ
    psi = np.zeros(dim, dtype=complex)
    base = site_base(N_YZ, SOURCE_Y, SOURCE_Z)
    psi[base + 0] = 1.0 / math.sqrt(2.0)
    psi[base + 2] = 1.0 / math.sqrt(2.0)
    norms = [float(np.sum(np.abs(psi) ** 2))]

    for x in range(N_LAYERS):
        # Coin
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

        # Shift with periodic wrap
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
    return abs(c_flat - mass_z) - abs(c_field - mass_z)


def fit_power_law(strengths: list[float], deltas: list[float]) -> tuple[float, float]:
    arr = np.array(deltas, dtype=float)
    signs = np.sign(arr)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        return float("nan"), 0.0
    log_s = np.log10(np.array(strengths, dtype=float))
    log_d = np.log10(np.abs(arr))
    coeffs = np.polyfit(log_s, log_d, 1)
    alpha = float(coeffs[0])
    pred = np.polyval(coeffs, log_s)
    ss_res = float(np.sum((log_d - pred) ** 2))
    ss_tot = float(np.sum((log_d - np.mean(log_d)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return alpha, r2


def run_once(strength: float) -> tuple[float, float, float, float]:
    field = make_localized_field_3d(N_LAYERS, N_YZ, strength, MASS_X, MASS_Y, MASS_Z)
    field0 = np.zeros_like(field)
    psi_0, norms0 = propagate_3d_theta(field0)
    psi_f, normsf = propagate_3d_theta(field)
    probs_0 = detector_probs_3d(psi_0)
    probs_f = detector_probs_3d(psi_f)
    c0 = centroid_z(probs_0)
    cf = centroid_z(probs_f)
    delta = toward_delta(c0, cf, MASS_Z)
    max_dev = max(
        max(abs(v - 1.0) for v in norms0),
        max(abs(v - 1.0) for v in normsf),
    )
    return c0, cf, delta, max_dev


def main() -> None:
    print("FRONTIER: CHIRAL LOCALIZED MASS 3D")
    print(f"Grid: {N_YZ} x {N_YZ}, layers={N_LAYERS}")
    print(f"Source: ({SOURCE_Y}, {SOURCE_Z})")
    print(f"Mass: ({MASS_X}, {MASS_Y}, {MASS_Z})")
    print(f"theta0={THETA0}, theta_gain={THETA_GAIN}, strength={STRENGTH}")
    print("Periodic wrap in y,z to preserve exact local unitarity.")
    print()

    print("Norm + gravity scan across reference k labels")
    deltas = []
    max_norm_dev = 0.0
    for k in K_VALUES:
        c0, cf, delta, dev = run_once(STRENGTH)
        max_norm_dev = max(max_norm_dev, dev)
        deltas.append(delta)
        direction = "TOWARD" if delta > 0 else ("AWAY" if delta < 0 else "NONE")
        print(
            f"  k={k:3.1f}: cz_flat={c0:.6f}, cz_field={cf:.6f}, "
            f"delta_toward={delta:+.6e}, {direction}"
        )

    print(f"\nMax norm deviation across scans: {max_norm_dev:.3e}")
    mean_delta = float(np.mean(deltas))
    std_delta = float(np.std(deltas))
    toward_count = sum(1 for d in deltas if d > 0)
    print(
        f"Spectral aggregate (equal-weight mean): {mean_delta:+.6e} ± {std_delta:.2e} "
        f"({toward_count}/{len(deltas)} TOWARD)"
    )

    print("\nF∝M scan at reference k=2.5 label")
    strengths = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4]
    fm_deltas = []
    for s in strengths:
        _, _, delta, _ = run_once(s)
        fm_deltas.append(delta)
        direction = "TOWARD" if delta > 0 else ("AWAY" if delta < 0 else "NONE")
        print(f"  strength={s:.1e}: delta_toward={delta:+.6e}, {direction}")

    alpha, r2 = fit_power_law(strengths, fm_deltas)
    print(f"\nF∝M fit: alpha={alpha:.3f}, R^2={r2:.4f}")
    print("\nCaveats:")
    print("  - Gravity observable is detector-plane centroid shift toward the mass in z.")
    print("  - k is a reference label only here; theta-coupled gravity is achromatic.")
    print("  - Sign depends on the chosen theta_gain convention and source/mass geometry.")


if __name__ == "__main__":
    main()
