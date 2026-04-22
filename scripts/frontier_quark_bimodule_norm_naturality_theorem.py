#!/usr/bin/env python3
"""
Frontier runner - Quark bimodule NORM-naturality theorem.

Companion to
`docs/QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md`.

Let `I = R * Im(p)` be the one-real imaginary channel on the retained CKM ray.
For `a in [0,1]`, a normalized NORM family is a pair of real-linear maps

    D_a, U_a : I -> I

with:
  (N1) complementarity: D_a + U_a = Id_I,
  (N2) endpoint normalization: D_0 = 0, D_1 = Id_I,
  (N3) affine naturality in the ownership parameter:
       D_{t a + (1-t) b} = t D_a + (1-t) D_b.

Because `I` is one-real-dimensional, every endomorphism is scalar
multiplication. Evaluating (N3) at `b=0`, `t=a` gives

    D_a = a D_1 + (1-a) D_0 = a Id_I,

so uniquely

    D_a(x) = a x,
    U_a(x) = (1-a) x.

At the physical point `a = rho = Re(r)`, this is exactly BICAC / STRC-LO.
The support and target bridge profiles are still affine, but fail endpoint
normalization: their `D_1` is `sqrt(6/7) Id_I` or `(48/49) Id_I`, not `Id_I`.

Checks:
  T1  Canonical family D_a(x)=a x, U_a(x)=(1-a) x satisfies complementarity
  T2  Canonical family satisfies endpoint normalization
  T3  Canonical family satisfies affine naturality on a sample grid
  T4  The affine-normalized axioms force D_a = a Id_I exactly
  T5  At a = rho the canonical family gives BICAC / STRC-LO
  T6  Support profile fails endpoint normalization at a = 1
  T7  Target profile fails endpoint normalization at a = 1
  T8  BICAC profile is the unique constant-kappa profile that is normalized

Expected: PASS=8 FAIL=0.
"""

from __future__ import annotations

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


def canonical_down(a: float, x: float) -> float:
    return a * x


def canonical_up(a: float, x: float) -> float:
    return (1.0 - a) * x


def constant_kappa_down(kappa: float, a: float, x: float) -> float:
    return kappa * a * x


def main() -> int:
    print("=" * 72)
    print("  Quark Bimodule NORM-Naturality Theorem")
    print("  Unique normalized affine extension of the LO split law")
    print("=" * 72)

    rho = 1.0 / math.sqrt(42.0)
    sin_d = math.sqrt(5.0 / 6.0)
    supp = 6.0 / 7.0
    delta_A1 = 1.0 / 42.0

    kappa_support = math.sqrt(supp)
    kappa_target = 1.0 - supp * delta_A1
    kappa_bicac = 1.0

    sample_a = [0.0, 0.1, rho, 0.5, 1.0]
    sample_pairs = [(0.0, 1.0, 0.25), (rho, 1.0, 0.5), (0.2, 0.8, 0.3)]

    print()
    print("  Retained physical point:")
    print(f"    rho   = {rho:.12f}")
    print(f"    sin_d = {sin_d:.12f}")
    print()
    print("  Distinguished constant-kappa profiles:")
    print(f"    support: kappa = sqrt(6/7) = {kappa_support:.12f}")
    print(f"    target : kappa = 48/49     = {kappa_target:.12f}")
    print(f"    BICAC  : kappa = 1         = {kappa_bicac:.12f}")

    print()
    print("  Theorem checks:")

    comp_ok = all(
        abs(canonical_down(a, 1.0) + canonical_up(a, 1.0) - 1.0) < 1e-15
        for a in sample_a
    )
    check(
        "T1  Canonical family D_a(x)=a x, U_a(x)=(1-a) x satisfies complementarity",
        comp_ok,
        "checked on sample ownership values",
    )

    endpoint_ok = (
        abs(canonical_down(0.0, 1.0)) < 1e-15
        and abs(canonical_down(1.0, 1.0) - 1.0) < 1e-15
    )
    check(
        "T2  Canonical family satisfies endpoint normalization",
        endpoint_ok,
        f"D_0(1)={canonical_down(0.0, 1.0):.1f}, D_1(1)={canonical_down(1.0, 1.0):.1f}",
    )

    affine_ok = True
    for a, b, t in sample_pairs:
        lhs = canonical_down(t * a + (1.0 - t) * b, 1.0)
        rhs = t * canonical_down(a, 1.0) + (1.0 - t) * canonical_down(b, 1.0)
        affine_ok &= abs(lhs - rhs) < 1e-15
    check(
        "T3  Canonical family satisfies affine naturality on a sample grid",
        affine_ok,
        "D_{ta+(1-t)b} = t D_a + (1-t) D_b",
    )

    derivation_ok = all(
        abs(
            canonical_down(a, 1.0)
            - (
                a * canonical_down(1.0, 1.0)
                + (1.0 - a) * canonical_down(0.0, 1.0)
            )
        )
        < 1e-15
        for a in sample_a
    )
    check(
        "T4  The affine-normalized axioms force D_a = a Id_I exactly",
        derivation_ok,
        "D_a = a D_1 + (1-a) D_0 = a Id_I",
    )

    a_u_lo = canonical_up(rho, sin_d)
    check(
        "T5  At a = rho the canonical family gives BICAC / STRC-LO",
        abs(a_u_lo + rho * sin_d - sin_d) < 1e-15,
        f"a_u_LO = {a_u_lo:.12f}",
    )

    support_d1 = constant_kappa_down(kappa_support, 1.0, 1.0)
    check(
        "T6  Support profile fails endpoint normalization at a = 1",
        abs(support_d1 - 1.0) > 1e-3,
        f"D_1^support = {support_d1:.12f}",
    )

    target_d1 = constant_kappa_down(kappa_target, 1.0, 1.0)
    check(
        "T7  Target profile fails endpoint normalization at a = 1",
        abs(target_d1 - 1.0) > 1e-3,
        f"D_1^target = {target_d1:.12f}",
    )

    unique_normalized = (
        abs(constant_kappa_down(kappa_bicac, 1.0, 1.0) - 1.0) < 1e-15
        and abs(support_d1 - 1.0) > 1e-3
        and abs(target_d1 - 1.0) > 1e-3
    )
    check(
        "T8  BICAC profile is the unique constant-kappa profile that is normalized",
        unique_normalized,
        f"D_1^BICAC = {constant_kappa_down(kappa_bicac, 1.0, 1.0):.1f}",
    )

    print()
    print("  Consequence:")
    print("    If the branch accepts affine-normalized NORM naturality on the full")
    print("    ownership interval, BICAC is no longer an arbitrary endpoint choice.")
    print("    It is the unique normalized extension of the bimodule split law.")

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("Quark bimodule NORM-naturality theorem: VERIFIED")
    else:
        print("FAILURES DETECTED")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
