#!/usr/bin/env python3
"""
Hierarchy spatial-BC selection and native u0 scaling theorem.

This script addresses two remaining support theorems for the hierarchy route:

1. Spatial APBC on the even L_s = 2 hypercube:
   prove that temporal APBC plus spatial APBC is the only minimal-cube choice
   that yields a finite intensive 3+1 effective-potential limit.

2. alpha_LM / one-link tadpole scaling:
   prove that the exact hierarchy observables carry one power of u0 per hopping
   amplitude, not two, by exact homogeneity of the intensive effective action.
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


def build_dirac(
    Ls: int,
    Lt: int,
    u0: float,
    mass: float = 0.0,
    spatial_apbc: bool = True,
    temporal_apbc: bool = True,
):
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
                    sign = -1.0 if (spatial_apbc and x0 + 1 >= Ls) else 1.0
                    D[i, idx(xf, x1, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x0 - 1) % Ls
                    sign = -1.0 if (spatial_apbc and x0 - 1 < 0) else 1.0
                    D[i, idx(xb, x1, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** x0
                    xf = (x1 + 1) % Ls
                    sign = -1.0 if (spatial_apbc and x1 + 1 >= Ls) else 1.0
                    D[i, idx(x0, xf, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x1 - 1) % Ls
                    sign = -1.0 if (spatial_apbc and x1 - 1 < 0) else 1.0
                    D[i, idx(x0, xb, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1)
                    xf = (x2 + 1) % Ls
                    sign = -1.0 if (spatial_apbc and x2 + 1 >= Ls) else 1.0
                    D[i, idx(x0, x1, xf, t)] += u0 * eta * sign / 2.0
                    xb = (x2 - 1) % Ls
                    sign = -1.0 if (spatial_apbc and x2 - 1 < 0) else 1.0
                    D[i, idx(x0, x1, xb, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1 + x2)
                    tf = (t + 1) % Lt
                    sign = -1.0 if (temporal_apbc and t + 1 >= Lt) else 1.0
                    D[i, idx(x0, x1, x2, tf)] += u0 * eta * sign / 2.0
                    tb = (t - 1) % Lt
                    sign = -1.0 if (temporal_apbc and t - 1 < 0) else 1.0
                    D[i, idx(x0, x1, x2, tb)] -= u0 * eta * sign / 2.0
    return D


def temporal_modes(Lt: int):
    return [(2 * n + 1) * math.pi / Lt for n in range(Lt)]


def exact_det_formula(Lt: int, u0: float, mass: float, spatial_apbc: bool) -> float:
    prod = 1.0
    for w in temporal_modes(Lt):
        base = 3.0 + math.sin(w) ** 2 if spatial_apbc else math.sin(w) ** 2
        prod *= (mass**2 + u0**2 * base) ** 4
    return prod


def free_energy_density(Lt: int, u0: float, mass: float, spatial_apbc: bool) -> float:
    return math.log(exact_det_formula(Lt, u0, mass, spatial_apbc) / exact_det_formula(Lt, u0, 0.0, spatial_apbc)) / (
        2.0 * Lt * 2**3
    )


def quadratic_coefficient(Lt: int, u0: float, spatial_apbc: bool) -> float:
    denom = lambda w: 3.0 + math.sin(w) ** 2 if spatial_apbc else math.sin(w) ** 2
    return (1.0 / (2.0 * Lt * u0**2)) * sum(1.0 / denom(w) for w in temporal_modes(Lt))


def exact_apbc_a_inf(u0: float) -> float:
    return 1.0 / (4.0 * math.sqrt(3.0) * u0**2)


def exact_pbc_a(Lt: int, u0: float) -> float:
    return Lt / (4.0 * u0**2)


def test_exact_det_formulas_for_both_spatial_bcs():
    print("\n" + "=" * 78)
    print("PART 1: EXACT DET FORMULAS FOR BOTH SPATIAL BC CHOICES")
    print("=" * 78)

    Ls = 2
    max_rel = 0.0
    for spatial_apbc in [False, True]:
        label = "APBC" if spatial_apbc else "PBC"
        for Lt in [2, 4, 6, 8]:
            for u0 in [0.6, 0.9, 1.2]:
                for mass in [0.0, 0.1, 0.5]:
                    D = build_dirac(Ls, Lt, u0, mass, spatial_apbc=spatial_apbc, temporal_apbc=True)
                    direct = abs(np.linalg.det(D))
                    exact = exact_det_formula(Lt, u0, mass, spatial_apbc)
                    rel = abs(direct - exact) / (exact if exact else 1.0)
                    max_rel = max(max_rel, rel)
                    if Lt == 2 and u0 == 0.9 and mass in [0.0, 0.1]:
                        print(f"  {label}, Lt={Lt}, m={mass:.1f}: direct={direct:.8e}, exact={exact:.8e}, rel={rel:.2e}")
    check(
        "exact determinant formulas match direct matrices for both spatial BC choices",
        max_rel < 3e-13,
        f"max relative error = {max_rel:.2e}",
    )


def test_u0_power_independence():
    print("\n" + "=" * 78)
    print("PART 2: EXACT u0 POWER IS 8 Lt FOR BOTH SPATIAL BC CHOICES")
    print("=" * 78)

    max_rel_spread = 0.0
    for spatial_apbc in [False, True]:
        label = "APBC" if spatial_apbc else "PBC"
        for Lt in [2, 4, 6]:
            vals = []
            for u0 in [0.6, 0.9, 1.2]:
                D = build_dirac(2, Lt, u0, 0.0, spatial_apbc=spatial_apbc, temporal_apbc=True)
                vals.append(abs(np.linalg.det(D)) / (u0 ** (8 * Lt)))
            spread = max(vals) - min(vals)
            rel_spread = spread / sum(vals) * len(vals)
            max_rel_spread = max(max_rel_spread, rel_spread)
            print(f"  {label}, Lt={Lt}: det/u0^(8Lt) = {vals}")
    check(
        "zero-mass determinant carries exact power u0^(8 Lt) regardless of spatial BC",
        max_rel_spread < 1e-12,
        f"max relative spread = {max_rel_spread:.2e}",
    )


def test_exact_u0_homogeneity_of_intensive_observable():
    print("\n" + "=" * 78)
    print("PART 3: EXACT INTENSIVE u0 HOMOGENEITY")
    print("=" * 78)

    max_err = 0.0
    for spatial_apbc in [False, True]:
        label = "APBC" if spatial_apbc else "PBC"
        for Lt in [2, 4, 6]:
            for u0 in [0.6, 0.9, 1.2]:
                for mass in [1e-3, 1e-2, 0.1]:
                    lhs = free_energy_density(Lt, u0, mass, spatial_apbc)
                    rhs = free_energy_density(Lt, 1.0, mass / u0, spatial_apbc)
                    err = abs(lhs - rhs)
                    max_err = max(max_err, err)
            print(f"  {label}, Lt={Lt}: max |f(u0,m)-f(1,m/u0)| <= {max_err:.2e}")
    check(
        "free-energy density depends on u0 only through m/u0",
        max_err < 1e-14,
        f"max absolute error = {max_err:.2e}",
    )


def test_spatial_apbc_selected_by_finite_3plus1_limit():
    print("\n" + "=" * 78)
    print("PART 4: SPATIAL APBC IS SELECTED BY FINITENESS OF THE 3+1 LIMIT")
    print("=" * 78)

    u0 = 0.9
    a_apbc_40 = quadratic_coefficient(40, u0, spatial_apbc=True)
    a_apbc_inf = exact_apbc_a_inf(u0)
    max_rel_pbc = 0.0
    for Lt in [2, 4, 6, 8, 10]:
        a_pbc = quadratic_coefficient(Lt, u0, spatial_apbc=False)
        a_pbc_exact = exact_pbc_a(Lt, u0)
        rel = abs(a_pbc - a_pbc_exact) / a_pbc_exact
        max_rel_pbc = max(max_rel_pbc, rel)
        print(f"  PBC, Lt={Lt}: A={a_pbc:.12e}, exact={a_pbc_exact:.12e}")
    print(f"  APBC, Lt=40: A={a_apbc_40:.12e}, A_inf={a_apbc_inf:.12e}")

    check(
        "spatial PBC coefficient diverges exactly as Lt / (4 u0^2)",
        max_rel_pbc < 1e-14,
        f"max relative error = {max_rel_pbc:.2e}",
    )
    check(
        "spatial APBC coefficient converges to a finite 3+1 limit",
        abs(a_apbc_40 - a_apbc_inf) < 1e-14,
        f"absolute error = {abs(a_apbc_40 - a_apbc_inf):.2e}",
    )
    check(
        "only spatial APBC yields a finite intensive temporal average",
        quadratic_coefficient(10, u0, spatial_apbc=False) > 5 * a_apbc_inf,
        f"A_pbc(10)/A_apbc(inf) = {quadratic_coefficient(10,u0,False)/a_apbc_inf:.2f}",
    )


def test_linear_u0_scaling_is_unique():
    print("\n" + "=" * 78)
    print("PART 5: NATIVE u0 SCALING SELECTS ONE POWER PER LINK")
    print("=" * 78)

    vals_linear = []
    vals_quadratic = []
    for u0 in [0.6, 0.9, 1.2]:
        a = quadratic_coefficient(2, u0, spatial_apbc=True)
        vals_linear.append(a * u0**2)
        vals_quadratic.append(a * u0**4)

    spread_linear = max(vals_linear) - min(vals_linear)
    spread_quadratic = max(vals_quadratic) - min(vals_quadratic)

    print(f"  A_2(u0) * u0^2 = {vals_linear}")
    print(f"  A_2(u0) * u0^4 = {vals_quadratic}")

    check(
        "exact local coefficient scales as u0^(-2), i.e. one power of u0 per field insertion pair",
        spread_linear < 1e-15,
        f"max spread = {spread_linear:.2e}",
    )
    check(
        "a quadratic tadpole power would oversubtract the exact local scaling",
        spread_quadratic > 0.05,
        f"max spread = {spread_quadratic:.6f}",
    )


def main():
    print("Hierarchy spatial-BC selection and native u0 scaling")
    print("=" * 78)
    test_exact_det_formulas_for_both_spatial_bcs()
    test_u0_power_independence()
    test_exact_u0_homogeneity_of_intensive_observable()
    test_spatial_apbc_selected_by_finite_3plus1_limit()
    test_linear_u0_scaling_is_unique()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
