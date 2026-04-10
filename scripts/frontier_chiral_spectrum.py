#!/usr/bin/env python3
"""Chiral standing-wave spectrum in a box.

This script tests the exact lattice standing-wave spectrum of the chiral
walk with reflecting boundaries and distinguishes it from the low-energy
n^2 approximation.

Exact lattice spectrum:
    E_n = arccos(cos(theta) * cos(k_n))
    k_n = n * pi / W

Low-energy expansion:
    E_n = theta + k_n^2 / (2 sin(theta)) + O(k_n^4)

So the total energy is not n^2; only the low-energy kinetic shift is.
Dependencies: numpy only.
"""

from __future__ import annotations

import math

import numpy as np


THETA = 0.3
WIDTHS = (21, 31, 41, 61, 81)
MAX_LEVELS = 8


def build_chiral_unitary(n_sites: int, theta: float) -> np.ndarray:
    """Build the reflecting-boundary 2n x 2n chiral walk unitary."""
    dim = 2 * n_sites
    coin = np.zeros((dim, dim), dtype=np.complex128)
    shift = np.zeros((dim, dim), dtype=np.complex128)

    c = math.cos(theta)
    s = math.sin(theta)
    for y in range(n_sites):
        ip = 2 * y
        im = ip + 1
        coin[ip, ip] = c
        coin[ip, im] = -s
        coin[im, ip] = s
        coin[im, im] = c

        if y + 1 < n_sites:
            shift[2 * (y + 1), ip] = 1.0
        else:
            shift[2 * y + 1, ip] = 1.0

        if y - 1 >= 0:
            shift[2 * (y - 1) + 1, im] = 1.0
        else:
            shift[2 * y, im] = 1.0

    return shift @ coin


def extract_spectrum(U: np.ndarray) -> tuple[np.ndarray, float]:
    phases = np.angle(np.linalg.eigvals(U))
    phases = np.sort(phases)
    radius_err = float(np.max(np.abs(np.abs(np.linalg.eigvals(U)) - 1.0)))
    return phases, radius_err


def standing_wave_energies(theta: float, width: int, n_levels: int) -> np.ndarray:
    levels = []
    for n in range(1, n_levels + 1):
        k_n = n * np.pi / width
        arg = np.cos(theta) * np.cos(k_n)
        arg = np.clip(arg, -1.0, 1.0)
        levels.append(np.arccos(arg))
    return np.asarray(levels, dtype=float)


def low_energy_approx(theta: float, width: int, n_levels: int) -> np.ndarray:
    pref = 1.0 / (2.0 * np.sin(theta))
    levels = []
    for n in range(1, n_levels + 1):
        k_n = n * np.pi / width
        levels.append(theta + pref * k_n**2)
    return np.asarray(levels, dtype=float)


def summarize_width(width: int, theta: float) -> dict[str, float]:
    U = build_chiral_unitary(width, theta)
    phases, radius_err = extract_spectrum(U)
    pos = np.sort(phases[phases > 1e-10])
    exact = standing_wave_energies(theta, width, min(MAX_LEVELS, len(pos)))
    approx = low_energy_approx(theta, width, min(MAX_LEVELS, len(pos)))

    print("\n" + "=" * 72)
    print(f"width = {width}, theta = {theta:.3f}")
    print("=" * 72)
    print(f"unitarity max|U^†U - I| = {radius_err:.3e}")
    print(f"positive phases extracted = {len(pos)}")
    print("\nfirst standing-wave levels")
    print(f"{'n':>4s}  {'E_num':>12s}  {'E_exact':>12s}  {'|Δ_exact|':>12s}  {'E-theta':>12s}  {'n^2 approx':>12s}")
    print(f"{'---':>4s}  {'---':>12s}  {'---':>12s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")

    for i in range(min(MAX_LEVELS, len(pos), len(exact))):
        n = i + 1
        e_num = pos[i]
        e_exact = exact[i]
        delta = abs(e_num - e_exact)
        kinetic = e_num - theta
        low = approx[i] - theta
        print(f"{n:4d}  {e_num:12.6f}  {e_exact:12.6f}  {delta:12.2e}  {kinetic:12.6f}  {low:12.6f}")

    delta_exact = exact - theta
    if len(delta_exact) >= 2:
        n_vals = np.arange(1, len(delta_exact) + 1, dtype=float)
        x = n_vals**2
        y = delta_exact
        a, b = np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)[0]
        pred = a + b * x
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        ss_res = float(np.sum((y - pred) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    else:
        b = float("nan")
        r2 = 0.0

    # Ground-state kinetic scaling for this width.
    delta1 = float(pos[0] - theta) if len(pos) > 0 else float("nan")
    print("\nlow-energy diagnostic")
    print(f"ground kinetic shift E_1-theta = {delta1:.6e}")
    print(f"fit of exact kinetic shift to n^2 over first {len(delta_exact)} levels: slope={b:.6e}, R^2={r2:.8f}")
    print("interpretation: total spectrum is exact lattice KG; n^2 only appears in the low-energy kinetic shift.")

    return {
        "width": float(width),
        "delta1": delta1,
        "radius_err": radius_err,
        "fit_r2": r2,
    }


def main() -> None:
    print("=" * 72)
    print("FRONTIER: CHIRAL WALK STANDING-WAVE SPECTRUM")
    print("=" * 72)
    print(f"theta = {THETA:.3f}")
    print("exact standing-wave spectrum: E_n = arccos(cos(theta) * cos(n*pi/W))")
    print("low-energy limit: E_n - theta ≈ n^2 * pi^2 / (2 sin(theta) W^2)")

    width_results = [summarize_width(width, THETA) for width in WIDTHS]

    widths = np.asarray([r["width"] for r in width_results], dtype=float)
    delta1 = np.asarray([r["delta1"] for r in width_results], dtype=float)
    mask = delta1 > 1e-30
    coeffs = np.polyfit(np.log(widths[mask]), np.log(delta1[mask]), 1)
    print("\n" + "=" * 72)
    print("WIDTH SCALING")
    print("=" * 72)
    print(f"ground-state kinetic shift scaling: E_1 - theta ~ W^{coeffs[0]:.3f}")
    print("particle-in-a-box low-energy prediction: exponent = -2.0")

    print("\nSUMMARY")
    print("Exact lattice spectrum is not n^2 for total energies.")
    print("The n^2 law is only the low-energy expansion of the kinetic shift E_n - theta.")
    for r in width_results:
        print(
            f"width={int(r['width'])}: radius_err={r['radius_err']:.3e}, "
            f"fit_R2={r['fit_r2']:.8f}"
        )


if __name__ == "__main__":
    main()
