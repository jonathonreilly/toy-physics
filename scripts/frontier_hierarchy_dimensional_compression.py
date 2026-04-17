#!/usr/bin/env python3
"""
Hierarchy dimensional-compression diagnostic.

Purpose:
  Quantify how an intensive L_t residual maps into a correction on the
  electroweak scale depending on the DIMENSION of the physical observable.

This does not prove the determinant-to-VEV theorem. It does sharpen the
remaining target:
  - if the physical map is directly scale-like, the correction is closer to a
    16th root and is too small
  - if the physical map comes from a dimension-4 effective potential density,
    the correction is naturally a fourth root and is the right order of
    magnitude for the observed 253 -> 246 GeV gap
"""

from __future__ import annotations

import math
import sys

import numpy as np

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

                    eta = 1.0
                    xf = (x0 + 1) % Ls
                    sign = -1.0 if x0 + 1 >= Ls else 1.0
                    D[i, idx(xf, x1, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x0 - 1) % Ls
                    sign = -1.0 if x0 - 1 < 0 else 1.0
                    D[i, idx(xb, x1, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** x0
                    xf = (x1 + 1) % Ls
                    sign = -1.0 if x1 + 1 >= Ls else 1.0
                    D[i, idx(x0, xf, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x1 - 1) % Ls
                    sign = -1.0 if x1 - 1 < 0 else 1.0
                    D[i, idx(x0, xb, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1)
                    xf = (x2 + 1) % Ls
                    sign = -1.0 if x2 + 1 >= Ls else 1.0
                    D[i, idx(x0, x1, xf, t)] += u0 * eta * sign / 2.0
                    xb = (x2 - 1) % Ls
                    sign = -1.0 if x2 - 1 < 0 else 1.0
                    D[i, idx(x0, x1, xb, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1 + x2)
                    tf = (t + 1) % Lt
                    sign = -1.0 if t + 1 >= Lt else 1.0
                    D[i, idx(x0, x1, x2, tf)] += u0 * eta * sign / 2.0
                    tb = (t - 1) % Lt
                    sign = -1.0 if t - 1 < 0 else 1.0
                    D[i, idx(x0, x1, x2, tb)] -= u0 * eta * sign / 2.0
    return D


def condensate_density(Ls: int, Lt: int, u0: float, mass: float) -> float:
    D = build_dirac_4d_apbc(Ls, Lt, u0, mass)
    return float(np.trace(np.linalg.inv(D)).real / (Ls**3 * Lt))


def main():
    print("Hierarchy dimensional-compression diagnostic")
    print("=" * 78)

    Ls = 2
    u0 = 0.9
    mass = 1e-2
    alpha_bare = 1.0 / (4.0 * np.pi)
    m_planck = 1.2209e19
    hierarchy_u0 = 0.5934 ** 0.25
    alpha_lm = alpha_bare / hierarchy_u0
    v_pred = m_planck * alpha_lm**16
    v_obs = 246.22
    c_obs = v_obs / v_pred

    cond_2 = condensate_density(Ls, 2, u0, mass)
    cond_10 = condensate_density(Ls, 10, u0, mass)
    ratio = cond_10 / cond_2

    print(f"\n  Using condensate density ratio at u0 = {u0}, m = {mass}")
    print(f"  cond(Lt=2)  = {cond_2:.10f}")
    print(f"  cond(Lt=10) = {cond_10:.10f}")
    print(f"  ratio       = {ratio:.10f}")
    print(f"  observed prefactor needed: C_obs = v_obs / v_pred = {c_obs:.10f}")

    candidates = {}
    for dim in [3, 4, 8, 16]:
        root = ratio ** (1 / dim)
        inv_root = 1 / root
        candidates[dim] = (root, inv_root)
        print(f"\n  Dimension-{dim} compression:")
        print(f"    ratio^(1/{dim})     = {root:.10f}")
        print(f"    ratio^(-1/{dim})    = {inv_root:.10f}")
        print(f"    direct shift        = {(root - 1) * 100:+.3f}%")
        print(f"    inverse shift       = {(inv_root - 1) * 100:+.3f}%")
        print(f"    distance to C_obs   = {abs(inv_root - c_obs):.6f}")

    check("16th-root compression is too small to explain the full pre-selector hierarchy shift",
          abs(candidates[16][1] - c_obs) > 0.01,
          f"ratio^(-1/16) = {candidates[16][1]:.6f}, C_obs = {c_obs:.6f}")

    check("4th-root inverse compression is in the right magnitude range for the observed gap",
          abs(candidates[4][1] - c_obs) < 0.01,
          f"ratio^(-1/4) = {candidates[4][1]:.6f}, C_obs = {c_obs:.6f}")

    print("\nConclusion:")
    print("  If the physical order parameter is dimension-4 (effective potential")
    print("  density), the residual block normalization naturally compresses to")
    print("  the few-percent level. If it is interpreted as a direct scale")
    print("  correction, the 16th-root effect is too small.")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
