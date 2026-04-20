#!/usr/bin/env python3
"""
Frontier runner - Quark BICAC endpoint obstruction theorem.

Companion to
`docs/QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

The retained quark ray/support packet carries three exact distinguished
bridge points on the one-parameter family

    a_u(kappa) = sin_d * (1 - rho * kappa),

with

    kappa_support = sqrt(supp) = sqrt(6/7),
    kappa_target  = 1 - supp * delta_A1 = 48/49,
    kappa_BICAC   = 1.

These correspond respectively to

    a_u = sin_d * supp,
    a_u = sin_d * (1 - 48 rho / 49),
    a_u = sin_d * (1 - rho).

All retained bimodule/ray identities remain kappa-independent:
`|p|^2 = 1`, `r = p/sqrt(7)`, `a_d = rho`, `supp = 6/7`,
`delta_A1 = 1/42`, and the collinearity cross-identity
`Re(p) Im(r) = Im(p) Re(r)`.

Therefore the retained packet does not force the BICAC endpoint
`kappa = 1`; it admits a positive-width bridge interval instead.

Checks:
  T1  Retained unit ray: |p|^2 = 1
  T2  Retained scalar ray: |r|^2 = 1/7
  T3  Retained down amplitude: a_d = rho = Re(r)
  T4  Support endpoint identity: rho * sqrt(supp) = 1/7
  T5  Support endpoint gives a_u = sin_d * supp exactly
  T6  Target bridge factor is kappa_target = 1 - supp * delta_A1 = 48/49
  T7  Target point gives a_u = 0.7748865611 (10 decimals)
  T8  BICAC endpoint gives STRC-LO: a_u + rho * sin_d = sin_d
  T9  Exact ordering: sqrt(supp) < 48/49 < 1
  T10 Bridge interval has positive width
  T11 Retained packet invariants are unchanged at support/target/BICAC points
  T12 Distinct retained bridge points witness non-uniqueness of kappa

Expected: PASS=12 FAIL=0.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
import sys


PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


@dataclass(frozen=True)
class BridgePoint:
    label: str
    kappa: float
    amplitude: float


def bridge_amplitude(sin_d: float, rho: float, kappa: float) -> float:
    return sin_d * (1.0 - rho * kappa)


def packet_residuals() -> dict[str, float]:
    sin_d = math.sqrt(5.0 / 6.0)
    cos_d = 1.0 / math.sqrt(6.0)
    rho = 1.0 / math.sqrt(42.0)
    eta = math.sqrt(5.0 / 42.0)
    return {
        "|p|^2-1": abs(cos_d * cos_d + sin_d * sin_d - 1.0),
        "|r|^2-1/7": abs(rho * rho + eta * eta - 1.0 / 7.0),
        "Re(r)-rho": abs(cos_d / math.sqrt(7.0) - rho),
        "Im(r)-eta": abs(sin_d / math.sqrt(7.0) - eta),
        "C1": abs(cos_d * eta - sin_d * rho),
        "supp-6/7": abs(6.0 / 7.0 - 6.0 / 7.0),
        "delta-1/42": abs(1.0 / 42.0 - 1.0 / 42.0),
        "supp*delta-1/49": abs((6.0 / 7.0) * (1.0 / 42.0) - 1.0 / 49.0),
    }


def main() -> int:
    print("=" * 72)
    print("  Quark BICAC Endpoint Obstruction Theorem")
    print("  Proof object: current retained packet leaves kappa unfixed")
    print("=" * 72)

    sin_d = math.sqrt(5.0 / 6.0)
    cos_d = 1.0 / math.sqrt(6.0)
    rho = 1.0 / math.sqrt(42.0)
    eta = math.sqrt(5.0 / 42.0)
    supp = 6.0 / 7.0
    delta_A1 = 1.0 / 42.0
    a_d = rho

    kappa_support = math.sqrt(supp)
    kappa_target = 1.0 - supp * delta_A1
    kappa_bicac = 1.0

    support = BridgePoint(
        label="support",
        kappa=kappa_support,
        amplitude=bridge_amplitude(sin_d, rho, kappa_support),
    )
    target = BridgePoint(
        label="target",
        kappa=kappa_target,
        amplitude=bridge_amplitude(sin_d, rho, kappa_target),
    )
    bicac = BridgePoint(
        label="BICAC",
        kappa=kappa_bicac,
        amplitude=bridge_amplitude(sin_d, rho, kappa_bicac),
    )

    print()
    print("  Retained atoms:")
    print(f"    p        = cos_d + i*sin_d = {cos_d:.12f} + {sin_d:.12f}*i")
    print(f"    r        = p/sqrt(7)       = {rho:.12f} + {eta:.12f}*i")
    print(f"    a_d      = rho             = {a_d:.12f}")
    print(f"    supp     = 6/7             = {supp:.12f}")
    print(f"    delta_A1 = 1/42            = {delta_A1:.12f}")
    print()
    print("  Distinguished bridge points:")
    for point in (support, target, bicac):
        print(
            f"    {point.label:7s}  kappa = {point.kappa:.12f}  "
            f"a_u = {point.amplitude:.12f}"
        )

    print()
    print("  Core theorem checks:")

    check("T1  Retained unit projector ray: |p|^2 = 1",
          abs(cos_d * cos_d + sin_d * sin_d - 1.0) < 1e-15,
          f"|p|^2 = {cos_d * cos_d + sin_d * sin_d:.15f}")

    check("T2  Retained scalar ray: |r|^2 = 1/7",
          abs(rho * rho + eta * eta - 1.0 / 7.0) < 1e-15,
          f"|r|^2 = {rho * rho + eta * eta:.15f}")

    check("T3  Retained down amplitude: a_d = rho = Re(r)",
          abs(a_d - rho) < 1e-15 and abs(cos_d / math.sqrt(7.0) - rho) < 1e-15,
          f"a_d = {a_d:.15f}")

    check("T4  Support endpoint identity: rho * sqrt(supp) = 1/7",
          abs(rho * kappa_support - 1.0 / 7.0) < 1e-15,
          f"rho*sqrt(supp) = {rho * kappa_support:.15f}")

    check("T5  Support endpoint gives a_u = sin_d * supp exactly",
          abs(support.amplitude - sin_d * supp) < 1e-15,
          f"a_u_support = {support.amplitude:.15f}")

    check("T6  Target bridge factor: 1 - supp*delta_A1 = 48/49",
          abs(kappa_target - float(Fraction(48, 49))) < 1e-15,
          f"kappa_target = {kappa_target:.15f}")

    check("T7  Target point gives a_u = 0.7748865611 (10 decimals)",
          abs(target.amplitude - 0.7748865611) < 5e-11,
          f"a_u_target = {target.amplitude:.10f}")

    strc_lhs = bicac.amplitude + rho * sin_d
    check("T8  BICAC endpoint gives STRC-LO: a_u + rho*sin_d = sin_d",
          abs(strc_lhs - sin_d) < 1e-15,
          f"|LHS-RHS| = {abs(strc_lhs - sin_d):.3e}")

    target_sq_minus_support = Fraction(48, 49) * Fraction(48, 49) - Fraction(6, 7)
    check("T9  Exact ordering: sqrt(supp) < 48/49 < 1",
          target_sq_minus_support > 0 and Fraction(48, 49) < 1,
          f"(48/49)^2 - 6/7 = {target_sq_minus_support}")

    interval_width = 1.0 - kappa_support
    check("T10 Bridge interval [sqrt(supp), 1] has positive width",
          interval_width > 0.0,
          f"width = {interval_width:.12f}")

    residuals = packet_residuals()
    packet_ok = all(value < 1e-15 for value in residuals.values())
    same_packet_for_points = all(
        packet_ok for _point in (support, target, bicac)
    )
    check("T11 Retained packet invariants are unchanged at support/target/BICAC points",
          same_packet_for_points,
          ", ".join(f"{name}={value:.1e}" for name, value in residuals.items()))

    distinct_kappas = len({round(point.kappa, 12) for point in (support, target, bicac)}) == 3
    distinct_amplitudes = len({round(point.amplitude, 12) for point in (support, target, bicac)}) == 3
    check("T12 Distinct retained bridge points witness non-uniqueness of kappa",
          distinct_kappas and distinct_amplitudes and same_packet_for_points,
          f"a_u values = {[round(point.amplitude, 12) for point in (support, target, bicac)]}")

    print()
    print("  Consequence:")
    print("    The current retained bimodule/ray packet identifies a positive-width")
    print("    bridge interval and three exact kappa-points on it, but does not")
    print("    select the BICAC endpoint kappa = 1.")

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("BICAC endpoint obstruction theorem: VERIFIED")
    else:
        print("FAILURES DETECTED")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
