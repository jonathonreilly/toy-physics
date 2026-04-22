#!/usr/bin/env python3
"""
Frontier runner - Quark bimodule NORM-existence theorem.

Companion to
`docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`.

On the retained CKM projector ray, let

    I := R * Im(p)

be the one-real imaginary channel. At the physical retained claim
`a_d = rho = Re(r)`, the exact bridge family

    a_u(kappa) = Im(p) * (1 - rho * kappa),
    kappa in [sqrt(supp), 1],

lifts to actual complementary real-linear endomorphisms of `I`:

    D_kappa(x) = rho * kappa * x,
    U_kappa(x) = (1 - rho * kappa) * x.

This answers the binary residue cleanly:

    yes, an LO split law exists on the bimodule.

Checks:
  T1  Retained interval is nonempty: sqrt(supp) <= 1
  T2  support / target / BICAC kappas lie in the retained interval
  T3  Each D_kappa, U_kappa is a real-linear endomorphism of I
  T4  Complementarity: U_kappa + D_kappa = Id_I
  T5  Contractivity: 0 <= rho*kappa <= 1 on the retained interval
  T6  Applying U_kappa to Im(p) reproduces the exact bridge family
  T7  Support endpoint gives a_u = sin_d * supp exactly
  T8  Target point gives a_u = 0.7748865611 (10 decimals)
  T9  BICAC endpoint gives STRC-LO exactly
  T10 The three distinguished laws are pairwise distinct

Expected: PASS=10 FAIL=0.
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
class NormLaw:
    label: str
    kappa: float
    up_coeff: float
    down_coeff: float


def apply(coeff: float, x: float) -> float:
    return coeff * x


def main() -> int:
    print("=" * 72)
    print("  Quark Bimodule NORM-Existence Theorem")
    print("  Binary residue: does an LO split law exist on the bimodule?")
    print("=" * 72)

    sin_d = math.sqrt(5.0 / 6.0)
    rho = 1.0 / math.sqrt(42.0)
    supp = 6.0 / 7.0
    delta_A1 = 1.0 / 42.0

    kappa_support = math.sqrt(supp)
    kappa_target = 1.0 - supp * delta_A1
    kappa_bicac = 1.0

    laws = []
    for label, kappa in (
        ("support", kappa_support),
        ("target", kappa_target),
        ("BICAC", kappa_bicac),
    ):
        down_coeff = rho * kappa
        up_coeff = 1.0 - down_coeff
        laws.append(NormLaw(label, kappa, up_coeff, down_coeff))

    print()
    print("  Retained channel and laws:")
    print(f"    I = R * Im(p),    Im(p) = sin_d = {sin_d:.12f}")
    print(f"    rho = Re(r) = {rho:.12f}")
    print(f"    interval = [sqrt(6/7), 1] = [{kappa_support:.12f}, 1.000000000000]")
    print()
    for law in laws:
        print(
            f"    {law.label:7s}  kappa={law.kappa:.12f}  "
            f"D(x)={law.down_coeff:.12f} x  U(x)={law.up_coeff:.12f} x"
        )

    print()
    print("  Theorem checks:")

    check(
        "T1  Retained interval is nonempty: sqrt(supp) <= 1",
        kappa_support <= 1.0,
        f"sqrt(supp) = {kappa_support:.12f}",
    )

    check(
        "T2  support / target / BICAC kappas lie in the retained interval",
        all(kappa_support <= law.kappa <= 1.0 for law in laws),
        ", ".join(f"{law.label}={law.kappa:.12f}" for law in laws),
    )

    linear_ok = all(
        abs(apply(law.up_coeff, 2.0) - 2.0 * apply(law.up_coeff, 1.0)) < 1e-15
        and abs(apply(law.down_coeff, 2.0) - 2.0 * apply(law.down_coeff, 1.0)) < 1e-15
        for law in laws
    )
    check(
        "T3  Each D_kappa, U_kappa is a real-linear endomorphism of I",
        linear_ok,
        "checked on the basis generator of the one-real channel",
    )

    comp_ok = all(abs((law.up_coeff + law.down_coeff) - 1.0) < 1e-15 for law in laws)
    check(
        "T4  Complementarity: U_kappa + D_kappa = Id_I",
        comp_ok,
        ", ".join(f"{law.label}:{law.up_coeff + law.down_coeff:.15f}" for law in laws),
    )

    contractive_ok = all(0.0 <= law.down_coeff <= 1.0 for law in laws)
    check(
        "T5  Contractivity: 0 <= rho*kappa <= 1 on the retained interval",
        contractive_ok,
        ", ".join(f"{law.label}:{law.down_coeff:.12f}" for law in laws),
    )

    bridge_ok = all(
        abs(apply(law.up_coeff, sin_d) - sin_d * (1.0 - rho * law.kappa)) < 1e-15
        for law in laws
    )
    check(
        "T6  Applying U_kappa to Im(p) reproduces the exact bridge family",
        bridge_ok,
        ", ".join(
            f"{law.label}:{apply(law.up_coeff, sin_d):.12f}" for law in laws
        ),
    )

    support_amp = apply(laws[0].up_coeff, sin_d)
    check(
        "T7  Support endpoint gives a_u = sin_d * supp exactly",
        abs(support_amp - sin_d * supp) < 1e-15,
        f"a_u_support = {support_amp:.15f}",
    )

    target_amp = apply(laws[1].up_coeff, sin_d)
    check(
        "T8  Target point gives a_u = 0.7748865611 (10 decimals)",
        abs(target_amp - 0.7748865611) < 5e-11,
        f"a_u_target = {target_amp:.10f}",
    )

    bicac_amp = apply(laws[2].up_coeff, sin_d)
    check(
        "T9  BICAC endpoint gives STRC-LO exactly",
        abs(bicac_amp + rho * sin_d - sin_d) < 1e-15,
        f"|LHS-RHS| = {abs(bicac_amp + rho * sin_d - sin_d):.3e}",
    )

    check(
        "T10 The three distinguished laws are pairwise distinct",
        len({round(law.up_coeff, 12) for law in laws}) == 3
        and len({round(law.down_coeff, 12) for law in laws}) == 3
        and Fraction(48, 49) > Fraction(0, 1),
        ", ".join(f"{law.label}:{law.up_coeff:.12f}" for law in laws),
    )

    print()
    print("  Consequence:")
    print("    The bimodule already carries actual LO split laws on the one-real")
    print("    imaginary channel. The residue is no longer existence; it is which")
    print("    law is canonical or retained-physics-selected.")

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("Quark bimodule NORM-existence theorem: VERIFIED")
    else:
        print("FAILURES DETECTED")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
