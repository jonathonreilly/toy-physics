#!/usr/bin/env python3
"""Chiral two-body superposition diagnostic on the 1D localized theta harness.

This is intentionally narrow:
  - 1D transverse chiral walk
  - theta-coupled localized fields
  - compare the centroid shift from a combined two-mass field against the
    sum of the individual centroid shifts

Because theta_eff = theta0 * (1 + f_total) is nonlinear inside the local
coin, exact field superposition is not guaranteed. This script measures how
large that nonlinearity is on the current 1D chiral lane.
"""

from __future__ import annotations

import math

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


N_Y = 25
N_LAYERS = 20
THETA0 = 0.30
SOURCE_Y = 10
MASS_X = 10
MASS_A_Y = 18
MASS_B_Y = 22
SOFTENING = 0.1
STRENGTHS = [1e-6, 1e-5, 1e-4, 1e-3]


def make_field(n_layers: int, n_y: int, strength: float, mass_x: int, mass_y: int) -> np.ndarray:
    field = np.zeros((n_layers, n_y), dtype=float)
    for x in range(n_layers):
        for y in range(n_y):
            r2 = (x - mass_x) ** 2 + (y - mass_y) ** 2
            field[x, y] = strength / math.sqrt(r2 + SOFTENING)
    return field


def propagate(field: np.ndarray) -> np.ndarray:
    psi = np.zeros(2 * N_Y, dtype=complex)
    psi[2 * SOURCE_Y] = 1.0

    for x in range(N_LAYERS):
        for y in range(N_Y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            theta = THETA0 * (1.0 + field[x, y])
            c = math.cos(theta)
            s = math.sin(theta)
            psi[idx_p] = c * pp - s * pm
            psi[idx_m] = s * pp + c * pm

        new_psi = np.zeros_like(psi)
        for y in range(N_Y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            if y + 1 < N_Y:
                new_psi[2 * (y + 1)] += psi[idx_p]
            else:
                new_psi[idx_m] += psi[idx_p]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[idx_m]
            else:
                new_psi[idx_p] += psi[idx_m]
        psi = new_psi

    return psi


def centroid(psi: np.ndarray) -> float:
    probs = np.zeros(N_Y, dtype=float)
    for y in range(N_Y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    ys = np.arange(N_Y, dtype=float)
    return float(np.dot(ys, probs) / probs.sum())


def main() -> None:
    print("FRONTIER: CHIRAL TWO-BODY SUPERPOSITION")
    print("Lane: 1D transverse local theta-coupled chiral walk")
    print(f"Source y={SOURCE_Y}, masses at y={MASS_A_Y} and y={MASS_B_Y}, x={MASS_X}")
    print()

    c0 = centroid(propagate(np.zeros((N_LAYERS, N_Y), dtype=float)))
    rel_errors = []
    for strength in STRENGTHS:
        f_a = make_field(N_LAYERS, N_Y, strength, MASS_X, MASS_A_Y)
        f_b = make_field(N_LAYERS, N_Y, strength, MASS_X, MASS_B_Y)
        f_ab = f_a + f_b

        da = centroid(propagate(f_a)) - c0
        db = centroid(propagate(f_b)) - c0
        dab = centroid(propagate(f_ab)) - c0
        expected = da + db

        denom = max(abs(expected), 1e-30)
        rel_err = abs(dab - expected) / denom
        rel_errors.append(rel_err)
        print(
            f"  strength={strength:.1e}: delta_a={da:+.6e}, delta_b={db:+.6e}, "
            f"delta_ab={dab:+.6e}, expected={expected:+.6e}, rel_err={100*rel_err:.2f}%"
        )

    print()
    print(f"Mean relative superposition error: {100*np.mean(rel_errors):.2f}%")
    print(f"Spread across strengths: {100*np.std(rel_errors):.2f}%")
    print("Interpretation:")
    print("  - this is a 1D chiral/theta lane test only")
    print("  - exact superposition is not expected because the local coin angle depends nonlinearly on the summed field")


if __name__ == "__main__":
    main()
