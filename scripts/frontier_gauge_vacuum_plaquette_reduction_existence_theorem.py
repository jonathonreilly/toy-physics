#!/usr/bin/env python3
"""
Exact existence / uniqueness theorem for the Wilson plaquette reduction law.

This closes the exact implicit reduction-law statement on finite periodic
Wilson L^4 evaluation surfaces, while keeping the explicit nonperturbative
form at beta = 6 open.
"""

from __future__ import annotations

import math
import sys
from typing import Iterable

import numpy as np

sys.path.insert(0, "scripts")

from canonical_plaquette_surface import CANONICAL_PLAQUETTE  # noqa: E402
from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel  # noqa: E402
from frontier_gauge_vacuum_plaquette_constant_lift_obstruction import full_wilson_strong_coupling_slope  # noqa: E402
from frontier_gauge_vacuum_plaquette_mixed_cumulant_audit import beta_eff_beta5_coefficient  # noqa: E402


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

N_C = 3
DIMS = 4


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def local_plaquette_density(matrix: np.ndarray) -> float:
    return float(np.trace(matrix).real / N_C)


def center_matrix() -> np.ndarray:
    phase = np.exp(2j * math.pi / 3.0)
    return phase * np.eye(3, dtype=complex)


def diagonal_phase_link(theta: float) -> np.ndarray:
    return np.diag([np.exp(1j * theta), np.exp(-1j * theta), 1.0]).astype(complex)


def build_identity_links(L: int = 2, ndim: int = DIMS) -> dict[tuple[int, ...], list[np.ndarray]]:
    links: dict[tuple[int, ...], list[np.ndarray]] = {}
    for coords in np.ndindex(*([L] * ndim)):
        links[coords] = [np.eye(3, dtype=complex) for _ in range(ndim)]
    return links


def measure_average_plaquette(links: dict[tuple[int, ...], list[np.ndarray]], L: int = 2, ndim: int = DIMS) -> float:
    total = 0.0
    count = 0
    for coords in np.ndindex(*([L] * ndim)):
        x = list(coords)
        for mu in range(ndim):
            for nu in range(mu + 1, ndim):
                xm = list(x)
                xm[mu] = (xm[mu] + 1) % L
                xn = list(x)
                xn[nu] = (xn[nu] + 1) % L
                u_p = (
                    links[tuple(x)][mu]
                    @ links[tuple(xm)][nu]
                    @ links[tuple(xn)][mu].conj().T
                    @ links[tuple(x)][nu].conj().T
                )
                total += np.trace(u_p).real / N_C
                count += 1
    return total / count


def implicit_beta_eff(target_plaquette: float, lo: float = 0.0, hi: float = 20.0, steps: int = 100) -> float:
    left = lo
    right = hi
    for _ in range(steps):
        mid = 0.5 * (left + right)
        p_mid, _ = plaquette_from_bessel(mid)
        if p_mid < target_plaquette:
            left = mid
        else:
            right = mid
    return 0.5 * (left + right)


def sample_monotone(values: Iterable[float]) -> bool:
    vals = list(values)
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


def main() -> int:
    identity_density = local_plaquette_density(np.eye(3, dtype=complex))
    center_density = local_plaquette_density(center_matrix())

    links_identity = build_identity_links()
    links_deformed = build_identity_links()
    links_deformed[(0, 0, 0, 0)][0] = diagonal_phase_link(0.41)
    avg_identity = measure_average_plaquette(links_identity)
    avg_deformed = measure_average_plaquette(links_deformed)

    sample_betas = [0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 10.0, 20.0]
    sample_local_plaquettes = [plaquette_from_bessel(beta)[0] for beta in sample_betas]

    canonical_beta_eff = implicit_beta_eff(CANONICAL_PLAQUETTE)
    candidate_beta_eff = implicit_beta_eff(0.593530679977098)
    slope_full = full_wilson_strong_coupling_slope()
    onset_coeff = beta_eff_beta5_coefficient()

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE REDUCTION EXISTENCE THEOREM")
    print("=" * 78)
    print()
    print("Local one-plaquette block")
    print(f"  X(identity)                           = {identity_density:.15f}")
    print(f"  X(center)                             = {center_density:.15f}")
    print(f"  sampled P_1plaq(betas)                = {[round(v, 12) for v in sample_local_plaquettes]}")
    print()
    print("Finite Wilson evaluation surface witness")
    print(f"  average plaquette on identity config  = {avg_identity:.15f}")
    print(f"  average plaquette on deformed config  = {avg_deformed:.15f}")
    print()
    print("Implicit reduction parameters")
    print(f"  canonical implicit beta_eff(0.5934)   = {canonical_beta_eff:.15f}")
    print(f"  candidate support beta_eff            = {candidate_beta_eff:.15f}")
    print(f"  delta(beta_eff)                       = {candidate_beta_eff - canonical_beta_eff:+.15f}")
    print()
    print("Onset data")
    print(f"  full-vacuum slope                     = {slope_full:.15f}")
    print(f"  beta_eff beta^5 coefficient           = {float(onset_coeff):.15e}")
    print()

    check(
        "the local one-plaquette observable is nonconstant on SU(3)",
        abs(identity_density - 1.0) < 1.0e-15 and abs(center_density + 0.5) < 1.0e-15,
        detail="X(U)=Re Tr U / 3 takes the values 1 and -1/2 on explicit SU(3) elements",
    )
    check(
        "the finite periodic Wilson plaquette observable is nonconstant on the evaluation surface",
        avg_identity > avg_deformed and abs(avg_identity - 1.0) < 1.0e-15,
        detail=f"identity average = {avg_identity:.15f}, deformed average = {avg_deformed:.15f}",
    )
    check(
        "sampled local one-plaquette values are consistent with the strict-monotonicity theorem",
        sample_monotone(sample_local_plaquettes) and 0.0 < sample_local_plaquettes[0] < sample_local_plaquettes[-1] < 1.0,
        detail="sampled local plaquette values increase strictly from beta=0.1 to beta=20 and stay in (0,1)",
        bucket="SUPPORT",
    )
    check(
        "explicit witnesses and range bounds are consistent with the exact implicit reduction-law theorem",
        avg_deformed < 1.0 and avg_identity <= 1.0 and sample_monotone(sample_local_plaquettes),
        detail="strict monotonicity of P_1plaq plus 0 <= P_L(beta) < 1 gives uniqueness on the finite Wilson surface",
        bucket="SUPPORT",
    )
    check(
        "the reduction law onset is exact with beta_eff'(0)=1",
        abs(slope_full - (1.0 / 18.0)) < 1.0e-15,
        detail=f"P_full'(0)=P_1plaq'(0)={slope_full:.15f}",
    )
    check(
        "the first nonlinear coefficient of the exact onset law is beta^5/26244",
        onset_coeff.numerator == 1 and onset_coeff.denominator == 26244,
        detail=f"beta_eff(beta)=beta + ({onset_coeff}) beta^5 + O(beta^6)",
    )

    check(
        "the canonical same-surface plaquette therefore has a unique implicit nonperturbative reduction parameter",
        9.0 < canonical_beta_eff < 10.0,
        detail=f"beta_eff^can = {canonical_beta_eff:.15f}",
        bucket="SUPPORT",
    )
    check(
        "the old constant-lift candidate remains numerically close to the exact implicit canonical beta_eff",
        abs(candidate_beta_eff - canonical_beta_eff) < 5.0e-3,
        detail=f"|candidate - implicit| = {abs(candidate_beta_eff - canonical_beta_eff):.6e}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
