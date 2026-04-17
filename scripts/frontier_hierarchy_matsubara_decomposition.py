#!/usr/bin/env python3
"""
Hierarchy Matsubara decomposition on the minimal APBC hypercube.

This script derives and verifies an exact closed-form temporal-mode
decomposition for the hierarchy determinant on the L_s = 2 APBC hypercube.

Key result:
  On the minimal spatial APBC block, all spatial momenta sit at the BZ
  corners, so sin^2(k_i) = 1 for i = 1,2,3. Therefore the full Lt-dependent
  determinant reduces exactly to a temporal Matsubara average:

    |det(D + m)| = prod_omega [m^2 + u0^2 (3 + sin^2 omega)]^4

  where omega = (2n+1) pi / Lt are the APBC temporal momenta.

This gives exact formulas for:
  - determinant magnitude
  - free-energy density difference
  - condensate density

The remaining theorem is then no longer "what is the determinant?" but
"which temporal averaging of this exact formula is the physical EWSB order
parameter?"
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


def temporal_modes(Lt: int):
    return np.array([(2 * n + 1) * math.pi / Lt for n in range(Lt)], dtype=float)


def exact_det_formula(Lt: int, u0: float, mass: float) -> float:
    omegas = temporal_modes(Lt)
    vals = [mass**2 + u0**2 * (3.0 + math.sin(w) ** 2) for w in omegas]
    prod = 1.0
    for v in vals:
        prod *= v**4
    return prod


def exact_free_energy_density(Lt: int, u0: float, mass: float) -> float:
    omegas = temporal_modes(Lt)
    return (1.0 / (2.0 * Lt)) * sum(
        math.log1p(mass**2 / (u0**2 * (3.0 + math.sin(w) ** 2))) for w in omegas
    )


def exact_condensate_density(Lt: int, u0: float, mass: float) -> float:
    omegas = temporal_modes(Lt)
    return (mass / Lt) * sum(
        1.0 / (mass**2 + u0**2 * (3.0 + math.sin(w) ** 2)) for w in omegas
    )


def test_closed_form_determinant():
    print("\n" + "=" * 78)
    print("PART 1: CLOSED-FORM DETERMINANT")
    print("=" * 78)

    Ls = 2
    max_rel = 0.0
    for Lt in [2, 4, 6, 8]:
        for u0 in [0.6, 0.9, 1.2]:
            for m in [0.0, 0.1, 0.5]:
                D = build_dirac_4d_apbc(Ls, Lt, u0, m)
                direct = abs(np.linalg.det(D))
                exact = exact_det_formula(Lt, u0, m)
                rel = abs(direct - exact) / exact
                max_rel = max(max_rel, rel)
                print(f"  Lt={Lt}, u0={u0:.1f}, m={m:.1f}: direct={direct:.8e}, exact={exact:.8e}, rel={rel:.2e}")
    check("exact Matsubara determinant formula matches direct determinant",
          max_rel < 1e-10,
          f"max relative error = {max_rel:.2e}")


def test_closed_form_intensive_observables():
    print("\n" + "=" * 78)
    print("PART 2: CLOSED-FORM FREE-ENERGY AND CONDENSATE DENSITIES")
    print("=" * 78)

    Ls = 2
    u0 = 0.9
    max_f = 0.0
    max_c = 0.0
    for Lt in [2, 4, 6, 8, 10]:
        D0 = build_dirac_4d_apbc(Ls, Lt, u0, 0.0)
        ld0 = np.linalg.slogdet(D0)[1]
        n = Ls**3 * Lt
        for m in [1e-3, 1e-2, 0.1]:
            Dm = build_dirac_4d_apbc(Ls, Lt, u0, m)
            ldm = np.linalg.slogdet(Dm)[1]
            direct_f = (ldm - ld0) / n
            exact_f = exact_free_energy_density(Lt, u0, m)
            direct_c = float(np.trace(np.linalg.inv(Dm)).real / n)
            exact_c = exact_condensate_density(Lt, u0, m)
            err_f = abs(direct_f - exact_f)
            err_c = abs(direct_c - exact_c)
            max_f = max(max_f, err_f)
            max_c = max(max_c, err_c)
            print(f"  Lt={Lt}, m={m:g}: f_direct={direct_f:.10e}, f_exact={exact_f:.10e}, c_direct={direct_c:.10e}, c_exact={exact_c:.10e}")
    check("exact free-energy density formula matches direct computation",
          max_f < 1e-12,
          f"max absolute error = {max_f:.2e}")
    check("exact condensate density formula matches direct computation",
          max_c < 1e-12,
          f"max absolute error = {max_c:.2e}")


def test_uv_endpoint_interpretation():
    print("\n" + "=" * 78)
    print("PART 3: UV ENDPOINT INTERPRETATION")
    print("=" * 78)

    u0 = 0.9
    mass = 1e-2

    cond2 = exact_condensate_density(2, u0, mass)
    cond10 = exact_condensate_density(10, u0, mass)
    ratio = cond10 / cond2
    root4 = ratio ** (-1 / 4)
    root16 = ratio ** (-1 / 16)
    alpha_bare = 1.0 / (4.0 * math.pi)
    m_planck = 1.2209e19
    hierarchy_u0 = 0.5934 ** 0.25
    alpha_lm = alpha_bare / hierarchy_u0
    c_obs = 246.22 / (m_planck * alpha_lm**16)

    print(f"  cond(Lt=2)  = {cond2:.10f}")
    print(f"  cond(Lt=10) = {cond10:.10f}")
    print(f"  ratio       = {ratio:.10f}")
    print(f"  C_obs       = {c_obs:.10f}")
    print(f"  ratio^(-1/4)  = {root4:.10f}")
    print(f"  ratio^(-1/16) = {root16:.10f}")

    check("dimension-4 compression is closer to the observed hierarchy prefactor than 16th-root compression",
          abs(root4 - c_obs) < abs(root16 - c_obs),
          f"|root4-C_obs|={abs(root4-c_obs):.6f}, |root16-C_obs|={abs(root16-c_obs):.6f}")


def main():
    print("Hierarchy Matsubara decomposition")
    print("=" * 78)
    test_closed_form_determinant()
    test_closed_form_intensive_observables()
    test_uv_endpoint_interpretation()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
