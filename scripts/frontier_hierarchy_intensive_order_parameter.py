#!/usr/bin/env python3
"""
Hierarchy intensive-order-parameter diagnostics.

Goal:
  Test the only viable route to the determinant-to-VEV theorem:
  move from extensive determinants to intensive free-energy / condensate
  observables and quantify how much of the L_t = 2 mismatch survives.

This script establishes three facts:
  1. raw zero-mass determinant factorization at L_t = 2n is exact in u0
  2. mass-deformed determinant ratios do NOT factorize exactly through L_t = 2
  3. intensive observables (free-energy density and condensate density)
     stabilize rapidly with L_t, so the residual compresses strongly once it
     is mapped through a low root

The last point does not close the hierarchy theorem, but it tells us the
right mathematical target: an intensive local order parameter, not the
extensive determinant itself.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def build_dirac_4d_apbc(Ls: int, Lt: int, u0: float, mass: float = 0.0):
    """Build staggered Dirac on Ls^3 x Lt with APBC in all directions."""
    n = Ls**3 * Lt
    D = np.zeros((n, n), dtype=complex)

    def idx(x0: int, x1: int, x2: int, t: int) -> int:
        return (((x0 % Ls) * Ls + (x1 % Ls)) * Ls + (x2 % Ls)) * Lt + (t % Lt)

    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for t in range(Lt):
                    i = idx(x0, x1, x2, t)
                    D[i, i] += mass

                    # mu = 0
                    eta = 1.0
                    xf = (x0 + 1) % Ls
                    sign = -1.0 if x0 + 1 >= Ls else 1.0
                    D[i, idx(xf, x1, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x0 - 1) % Ls
                    sign = -1.0 if x0 - 1 < 0 else 1.0
                    D[i, idx(xb, x1, x2, t)] -= u0 * eta * sign / 2.0

                    # mu = 1
                    eta = (-1.0) ** x0
                    xf = (x1 + 1) % Ls
                    sign = -1.0 if x1 + 1 >= Ls else 1.0
                    D[i, idx(x0, xf, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x1 - 1) % Ls
                    sign = -1.0 if x1 - 1 < 0 else 1.0
                    D[i, idx(x0, xb, x2, t)] -= u0 * eta * sign / 2.0

                    # mu = 2
                    eta = (-1.0) ** (x0 + x1)
                    xf = (x2 + 1) % Ls
                    sign = -1.0 if x2 + 1 >= Ls else 1.0
                    D[i, idx(x0, x1, xf, t)] += u0 * eta * sign / 2.0
                    xb = (x2 - 1) % Ls
                    sign = -1.0 if x2 - 1 < 0 else 1.0
                    D[i, idx(x0, x1, xb, t)] -= u0 * eta * sign / 2.0

                    # mu = 3
                    eta = (-1.0) ** (x0 + x1 + x2)
                    tf = (t + 1) % Lt
                    sign = -1.0 if t + 1 >= Lt else 1.0
                    D[i, idx(x0, x1, x2, tf)] += u0 * eta * sign / 2.0
                    tb = (t - 1) % Lt
                    sign = -1.0 if t - 1 < 0 else 1.0
                    D[i, idx(x0, x1, x2, tb)] -= u0 * eta * sign / 2.0

    return D


def logabsdet(M: np.ndarray) -> float:
    sign, value = np.linalg.slogdet(M)
    if abs(sign) == 0:
        return -np.inf
    return float(value)


def test_raw_factorization():
    print("\n" + "=" * 78)
    print("PART 1: RAW ZERO-MASS FACTORIZATION")
    print("=" * 78)

    Ls = 2
    u0_values = [0.5, 0.7, 0.9, 1.2]
    ratios_4 = []
    ratios_6 = []
    for u0 in u0_values:
        D2 = build_dirac_4d_apbc(Ls, 2, u0, 0.0)
        D4 = build_dirac_4d_apbc(Ls, 4, u0, 0.0)
        D6 = build_dirac_4d_apbc(Ls, 6, u0, 0.0)
        ratios_4.append(abs(np.linalg.det(D4)) / abs(np.linalg.det(D2)) ** 2)
        ratios_6.append(abs(np.linalg.det(D6)) / abs(np.linalg.det(D2)) ** 3)

    spread_4 = max(ratios_4) / min(ratios_4) - 1.0
    spread_6 = max(ratios_6) / min(ratios_6) - 1.0
    check("det(L_t=4) / det(L_t=2)^2 is u0-independent",
          spread_4 < 1e-10,
          f"spread = {spread_4:.2e}, C_2 = {ratios_4[0]:.8f}")
    check("det(L_t=6) / det(L_t=2)^3 is u0-independent",
          spread_6 < 1e-10,
          f"spread = {spread_6:.2e}, C_3 = {ratios_6[0]:.8f}")


def test_mass_ratio_failure():
    print("\n" + "=" * 78)
    print("PART 2: MASS-DEFORMED DETERMINANT RATIOS DO NOT FACTORIZE")
    print("=" * 78)

    Ls = 2
    u0 = 0.9
    masses = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

    D20 = build_dirac_4d_apbc(Ls, 2, u0, 0.0)
    D40 = build_dirac_4d_apbc(Ls, 4, u0, 0.0)
    D60 = build_dirac_4d_apbc(Ls, 6, u0, 0.0)
    det20 = abs(np.linalg.det(D20))
    det40 = abs(np.linalg.det(D40))
    det60 = abs(np.linalg.det(D60))

    worst_4 = 0.0
    worst_6 = 0.0
    for m in masses:
        D2 = build_dirac_4d_apbc(Ls, 2, u0, m)
        D4 = build_dirac_4d_apbc(Ls, 4, u0, m)
        D6 = build_dirac_4d_apbc(Ls, 6, u0, m)
        q2 = abs(np.linalg.det(D2)) / det20
        q4 = abs(np.linalg.det(D4)) / det40
        q6 = abs(np.linalg.det(D6)) / det60
        r4 = q4 / (q2 ** 2)
        r6 = q6 / (q2 ** 3)
        worst_4 = max(worst_4, abs(r4 - 1.0))
        worst_6 = max(worst_6, abs(r6 - 1.0))
        print(f"  m = {m:>4.2f}:  q4/q2^2 = {r4:.6f},  q6/q2^3 = {r6:.6f}")

    check("mass-deformed ratio is not exactly one-block factorized at L_t=4",
          worst_4 > 0.10,
          f"max |q4/q2^2 - 1| = {worst_4:.4f}")
    check("mass-deformed ratio is not exactly one-block factorized at L_t=6",
          worst_6 > 0.10,
          f"max |q6/q2^3 - 1| = {worst_6:.4f}")


def test_intensive_observables():
    print("\n" + "=" * 78)
    print("PART 3: INTENSIVE OBSERVABLES")
    print("=" * 78)

    Ls = 2
    u0 = 0.9
    masses = [1e-3, 1e-2]
    lt_values = [2, 4, 6, 8, 10]

    condensates = {m: {} for m in masses}
    free_energy_density = {m: {} for m in masses}

    for Lt in lt_values:
        D0 = build_dirac_4d_apbc(Ls, Lt, u0, 0.0)
        ld0 = logabsdet(D0)
        n_sites = Ls**3 * Lt
        for m in masses:
            Dm = build_dirac_4d_apbc(Ls, Lt, u0, m)
            ld = logabsdet(Dm)
            cond = float(np.trace(np.linalg.inv(Dm)).real / n_sites)
            df = (ld - ld0) / n_sites
            condensates[m][Lt] = cond
            free_energy_density[m][Lt] = df
            print(f"  L_t = {Lt:2d}, m = {m:>6.3g}:  cond/site = {cond:.10f},  delta_f/site = {df:.10f}")

    # Use Lt=10 as finite-volume stand-in for the long-circle limit.
    for m in masses:
        ratio_cond = condensates[m][10] / condensates[m][2]
        ratio_f = free_energy_density[m][10] / free_energy_density[m][2]
        print(f"\n  m = {m:>6.3g}:")
        print(f"    condensate ratio (Lt=10 / Lt=2) = {ratio_cond:.6f}")
        print(f"    free-energy density ratio       = {ratio_f:.6f}")
        print(f"    fourth-root compression         = {ratio_cond**0.25:.6f}")
        print(f"    sixteenth-root compression      = {ratio_cond**(1/16):.6f}")

        check(f"condensate density stabilizes rapidly for m = {m:g}",
              abs(condensates[m][10] / condensates[m][8] - 1.0) < 1e-3,
              f"Lt=8 -> 10 drift = {(condensates[m][10] / condensates[m][8] - 1.0):.2e}")
        check(f"intensive Lt=2 mismatch is only few-percent after fourth-root compression for m = {m:g}",
              ratio_cond**0.25 < 1.05,
              f"(Lt=10/Lt=2)^(1/4) = {ratio_cond**0.25:.6f}")


def main():
    print("Hierarchy intensive-order-parameter diagnostics")
    print("=" * 78)
    test_raw_factorization()
    test_mass_ratio_failure()
    test_intensive_observables()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
