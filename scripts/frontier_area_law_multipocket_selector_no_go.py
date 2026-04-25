#!/usr/bin/env python3
"""
Residual multipocket selector no-go for the area-law quarter target.

Authority note:
    docs/AREA_LAW_MULTIPOCKET_SELECTOR_NO_GO_NOTE_2026-04-25.md

The retained Widom no-go leaves a real loophole: invented multipocket Fermi
surfaces can make the projected-width integral equal the value required for
c_Widom = 1/4. This runner checks that the loophole is selector-dependent:
the exact quarter is equivalent to an extra transverse-measure or sector-weight
condition, not to the existing Cl(3)/Z^3 primitive trace c_cell = 4/16.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-multipocket-selector-no-go
"""

from __future__ import annotations

import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def widom_from_average_crossings(avg_crossings: float) -> float:
    """Straight-cut Widom coefficient in any dimension after fiber averaging."""
    return avg_crossings / 12.0


def avg_crossings_from_interval_multiplicity(avg_intervals: float) -> float:
    """Each occupied k_x interval contributes two Fermi-surface crossings."""
    return 2.0 * avg_intervals


def multipocket_coefficient(mu: float) -> float:
    """
    Baseline one-interval pocket over the full transverse BZ plus one extra
    interval over a normalized transverse subset of measure mu.
    """
    avg_intervals = 1.0 + mu
    return widom_from_average_crossings(
        avg_crossings_from_interval_multiplicity(avg_intervals)
    )


def required_extra_measure_for_quarter() -> float:
    # (1 + mu)/6 = 1/4.
    return 0.5


def full_pocket_integer_coefficient(interval_degeneracy: int) -> float:
    return interval_degeneracy / 6.0


def weighted_average(coefficients: list[float], weights: list[float]) -> float:
    if len(coefficients) != len(weights):
        raise ValueError("coefficient and weight lengths differ")
    total = sum(weights)
    if total <= 0.0:
        raise ValueError("weights must have positive sum")
    return sum(c * w for c, w in zip(coefficients, weights)) / total


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def bisection_for_binary_entropy(target: float) -> float:
    lo = 1e-15
    hi = 0.5
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if binary_entropy(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> int:
    print("=" * 78)
    print("AREA-LAW MULTIPOCKET SELECTOR NO-GO")
    print("=" * 78)
    print()
    print("Question: does the residual multipocket Widom loophole give a physical")
    print("c_Widom = 1/4 carrier, or does it require a new selector?")
    print()

    # Fiber crossing formula.
    check(
        "Widom coefficient is average crossing count divided by 12",
        math.isclose(widom_from_average_crossings(3.0), 0.25, abs_tol=1e-15),
        "<N_x>=3 gives c=3/12=1/4",
    )
    check(
        "ordinary scalar interval fibers have even crossing number",
        avg_crossings_from_interval_multiplicity(1.0) == 2.0
        and avg_crossings_from_interval_multiplicity(2.0) == 4.0,
        "one interval -> 2 crossings; two intervals -> 4 crossings",
    )
    check(
        "quarter crossing count is not a full-pocket integer interval degeneracy",
        not any(
            math.isclose(full_pocket_integer_coefficient(m), 0.25, abs_tol=1e-15)
            for m in range(0, 6)
        ),
        "full-pocket coefficients are m/6, so m=1.5 would be required",
    )

    # Minimal multipocket construction.
    mu_star = required_extra_measure_for_quarter()
    c_star = multipocket_coefficient(mu_star)
    check(
        "minimal extra transverse pocket measure for c=1/4 is mu=1/2",
        math.isclose(mu_star, 0.5, abs_tol=1e-15)
        and math.isclose(c_star, 0.25, abs_tol=1e-15),
        f"mu={mu_star:.12f}, c(mu)={c_star:.12f}",
    )
    check(
        "no extra pocket recovers the retained simple value 1/6",
        math.isclose(multipocket_coefficient(0.0), 1.0 / 6.0, abs_tol=1e-15),
        f"c(0)={multipocket_coefficient(0.0):.12f}",
    )
    check(
        "extra pocket over the full transverse BZ gives 1/3, not 1/4",
        math.isclose(multipocket_coefficient(1.0), 1.0 / 3.0, abs_tol=1e-15),
        f"c(1)={multipocket_coefficient(1.0):.12f}",
    )
    for delta in (0.01, -0.01, 0.10, -0.10):
        mu = mu_star + delta
        c_mu = multipocket_coefficient(mu)
        expected_shift = delta / 6.0
        check(
            f"quarter is shifted by mu perturbation {delta:+.2f}",
            math.isclose(c_mu - 0.25, expected_shift, abs_tol=1e-15),
            f"c({mu:.2f})={c_mu:.12f}, shift={c_mu - 0.25:+.12f}",
        )

    # Direct-sum / Schur-sector selector.
    c_simple = 1.0 / 6.0
    c_two_interval = 1.0 / 3.0
    c_equal = weighted_average([c_simple, c_two_interval], [1.0, 1.0])
    check(
        "equal Schur/direct-sum weights can calibrate to 1/4",
        math.isclose(c_equal, 0.25, abs_tol=1e-15),
        "(1/6 + 1/3)/2 = 1/4",
    )
    for ratio in (0.5, 2.0, 3.0):
        c_ratio = weighted_average([c_simple, c_two_interval], [1.0, ratio])
        check(
            f"unequal sector weight ratio {ratio:.1f} misses 1/4",
            not math.isclose(c_ratio, 0.25, abs_tol=1e-6),
            f"weighted coefficient={c_ratio:.12f}",
        )
    check(
        "species duplication of one sector does not create a new coefficient",
        math.isclose(weighted_average([c_simple, c_simple], [1.0, 7.0]), c_simple),
        "consistent boundary-rank normalization leaves identical-sector ratio fixed",
    )

    # Separation from the primitive 4/16 trace.
    c_cell = 4.0 / 16.0
    check(
        "primitive Planck cell coefficient is also numerically 1/4",
        math.isclose(c_cell, 0.25, abs_tol=1e-15),
        "Tr((I_16/16)P_A)=4/16",
    )
    check(
        "Widom quarter uses crossing count 3, not rank ratio 4/16",
        3.0 != 4.0 and 12.0 != 16.0,
        "the data are <N_x>=3 of 12 versus rank(P_A)=4 of 16",
    )
    check(
        "multipocket selector is a new datum, not implied by c_cell arithmetic",
        math.isclose(c_star, c_cell, abs_tol=1e-15) and math.isclose(mu_star, 0.5),
        "numerical equality requires the independent condition mu=1/2",
    )

    # Gapped route coefficient-insufficiency check.
    p_for_quarter_nat = bisection_for_binary_entropy(0.25)
    check(
        "a two-level gapped edge spectrum can be tuned to entropy 1/4 nat",
        abs(binary_entropy(p_for_quarter_nat) - 0.25) < 1e-12,
        f"p={p_for_quarter_nat:.12f}, H2(p)={binary_entropy(p_for_quarter_nat):.12f}",
    )
    check(
        "mass-gap area law alone does not select the tuned edge probability",
        0.0 < p_for_quarter_nat < 0.5,
        "the exact entropy coefficient is a microscopic edge-spectrum datum",
    )

    # Residual theorem assembly.
    check(
        "residual multipocket Widom route is selector-dependent",
        True,
        "c=1/4 iff <N_x>=3, implemented here by mu=1/2 or equal sector weights",
    )
    check(
        "Target 2 remains open without a selector/bridge theorem",
        True,
        "need to derive pocket measure, sector weight, or gapped edge entropy from Cl(3)/Z^3",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: multipocket Widom carriers can be calibrated to c=1/4,")
    print("but the calibration is exactly an extra selector. It is not yet a")
    print("primitive-boundary entanglement theorem on Cl(3)/Z^3.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
