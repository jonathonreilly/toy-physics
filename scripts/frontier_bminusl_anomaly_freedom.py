#!/usr/bin/env python3
"""
B-L anomaly-freedom theorem verification.

All fields are written as left-handed Weyl fermions. Right-handed species are
therefore represented by their charge-conjugate left-handed fields, so their
U(1) charges are sign-flipped.

The retained one-generation content including nu_R cancels the full anomaly
set needed to gauge U(1)_{B-L} alongside the retained SM gauge group:

  G1  grav^2 U(1)_{B-L}
  G2  U(1)_{B-L}^3
  G3  SU(3)^2 U(1)_{B-L}
  G4  SU(2)^2 U(1)_{B-L}
  G5  U(1)_Y^2 U(1)_{B-L}
  G6  U(1)_Y U(1)_{B-L}^2

The nu_R^c field is load-bearing for G1 and G2, and inert for G3-G6.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


@dataclass(frozen=True)
class Fermion:
    name: str
    su3_dim: int
    su2_dim: int
    colour_mult: int
    weak_mult: int
    hypercharge: Fraction
    b_minus_l: Fraction

    @property
    def multiplicity(self) -> int:
        return self.colour_mult * self.weak_mult

    @property
    def su3_charged(self) -> bool:
        return self.su3_dim == 3

    @property
    def su2_doublet(self) -> bool:
        return self.su2_dim == 2


# Doubled-hypercharge convention: Q = T3 + Y/2.
FERMIONS = [
    Fermion("Q_L", 3, 2, 3, 2, Fraction(1, 3), Fraction(1, 3)),
    Fermion("L_L", 1, 2, 1, 2, Fraction(-1, 1), Fraction(-1, 1)),
    Fermion("u_R^c", 3, 1, 3, 1, Fraction(-4, 3), Fraction(-1, 3)),
    Fermion("d_R^c", 3, 1, 3, 1, Fraction(2, 3), Fraction(-1, 3)),
    Fermion("e_R^c", 1, 1, 1, 1, Fraction(2, 1), Fraction(1, 1)),
    Fermion("nu_R^c", 1, 1, 1, 1, Fraction(0, 1), Fraction(1, 1)),
]


def trace_linear(fields: list[Fermion], charge: str) -> Fraction:
    return sum(f.multiplicity * getattr(f, charge) for f in fields)


def trace_cubic(fields: list[Fermion], charge: str) -> Fraction:
    return sum(f.multiplicity * getattr(f, charge) ** 3 for f in fields)


def mixed_su3_u1(fields: list[Fermion], charge: str) -> Fraction:
    # Common Dynkin factor T(3)=T(3bar)=1/2 is omitted; only cancellation matters.
    return sum(f.weak_mult * getattr(f, charge) for f in fields if f.su3_charged)


def mixed_su2_u1(fields: list[Fermion], charge: str) -> Fraction:
    # Common Dynkin factor T(2)=1/2 is omitted; only cancellation matters.
    return sum(f.colour_mult * getattr(f, charge) for f in fields if f.su2_doublet)


def mixed_y2_bl(fields: list[Fermion]) -> Fraction:
    return sum(f.multiplicity * f.hypercharge**2 * f.b_minus_l for f in fields)


def mixed_y_bl2(fields: list[Fermion]) -> Fraction:
    return sum(f.multiplicity * f.hypercharge * f.b_minus_l**2 for f in fields)


def anomaly_packet(fields: list[Fermion]) -> dict[str, Fraction]:
    return {
        "G1_grav_BL": trace_linear(fields, "b_minus_l"),
        "G2_BL_cubic": trace_cubic(fields, "b_minus_l"),
        "G3_SU3_SU3_BL": mixed_su3_u1(fields, "b_minus_l"),
        "G4_SU2_SU2_BL": mixed_su2_u1(fields, "b_minus_l"),
        "G5_Y_Y_BL": mixed_y2_bl(fields),
        "G6_Y_BL_BL": mixed_y_bl2(fields),
    }


def part0_content_audit() -> None:
    banner("Part 0: retained one-generation content in LH-conjugate frame")

    print(
        f"  {'field':>8s}  {'SU3':>3s}  {'SU2':>3s}  "
        f"{'mult':>4s}  {'Y':>6s}  {'B-L':>6s}"
    )
    for f in FERMIONS:
        print(
            f"  {f.name:>8s}  {f.su3_dim:>3d}  {f.su2_dim:>3d}  "
            f"{f.multiplicity:>4d}  {str(f.hypercharge):>6s}  {str(f.b_minus_l):>6s}"
        )

    total = sum(f.multiplicity for f in FERMIONS)
    check("one generation contains 16 LH-frame Weyl states including nu_R", total == 16, f"count={total}")

    expected = {
        "Q_L": (Fraction(1, 3), Fraction(1, 3)),
        "L_L": (Fraction(-1, 1), Fraction(-1, 1)),
        "u_R^c": (Fraction(-4, 3), Fraction(-1, 3)),
        "d_R^c": (Fraction(2, 3), Fraction(-1, 3)),
        "e_R^c": (Fraction(2, 1), Fraction(1, 1)),
        "nu_R^c": (Fraction(0, 1), Fraction(1, 1)),
    }
    for f in FERMIONS:
        y_expected, bl_expected = expected[f.name]
        check(f"Y({f.name}) = {y_expected}", f.hypercharge == y_expected)
        check(f"B-L({f.name}) = {bl_expected}", f.b_minus_l == bl_expected)


def part1_full_anomaly_closure() -> None:
    banner("Part 1: full B-L anomaly packet")

    values = anomaly_packet(FERMIONS)
    labels = {
        "G1_grav_BL": "G1 grav^2 U(1)_{B-L}",
        "G2_BL_cubic": "G2 U(1)_{B-L}^3",
        "G3_SU3_SU3_BL": "G3 SU(3)^2 U(1)_{B-L}",
        "G4_SU2_SU2_BL": "G4 SU(2)^2 U(1)_{B-L}",
        "G5_Y_Y_BL": "G5 U(1)_Y^2 U(1)_{B-L}",
        "G6_Y_BL_BL": "G6 U(1)_Y U(1)_{B-L}^2",
    }
    for key, label in labels.items():
        print(f"  {label:<34s} = {values[key]}")
        check(f"{label} cancels exactly", values[key] == 0, f"value={values[key]}")


def part2_component_contributions() -> None:
    banner("Part 2: exact rational contribution checks")

    contributions = {
        "G1": [(f.name, f.multiplicity * f.b_minus_l) for f in FERMIONS],
        "G2": [(f.name, f.multiplicity * f.b_minus_l**3) for f in FERMIONS],
        "G3": [(f.name, f.weak_mult * f.b_minus_l) for f in FERMIONS if f.su3_charged],
        "G4": [(f.name, f.colour_mult * f.b_minus_l) for f in FERMIONS if f.su2_doublet],
        "G5": [(f.name, f.multiplicity * f.hypercharge**2 * f.b_minus_l) for f in FERMIONS],
        "G6": [(f.name, f.multiplicity * f.hypercharge * f.b_minus_l**2) for f in FERMIONS],
    }

    expected_totals = {name: Fraction(0, 1) for name in contributions}
    for name, rows in contributions.items():
        total = sum(value for _, value in rows)
        rendered = " + ".join(f"{field}:{value}" for field, value in rows)
        print(f"  {name}: {rendered} = {total}")
        check(f"{name} contribution sum is exactly zero", total == expected_totals[name])


def part3_nu_r_ablation() -> None:
    banner("Part 3: nu_R ablation")

    without_nu_r = [f for f in FERMIONS if f.name != "nu_R^c"]
    values = anomaly_packet(without_nu_r)

    print("  Without nu_R^c:")
    for key, value in values.items():
        print(f"    {key:<18s} = {value}")

    check("without nu_R, G1 linear B-L anomaly is -1", values["G1_grav_BL"] == -1)
    check("without nu_R, G2 cubic B-L anomaly is -1", values["G2_BL_cubic"] == -1)
    check("without nu_R, G3 remains zero because nu_R is colour-singlet", values["G3_SU3_SU3_BL"] == 0)
    check("without nu_R, G4 remains zero because nu_R is weak-singlet", values["G4_SU2_SU2_BL"] == 0)
    check("without nu_R, G5 remains zero because Y(nu_R)=0", values["G5_Y_Y_BL"] == 0)
    check("without nu_R, G6 remains zero because Y(nu_R)=0", values["G6_Y_BL_BL"] == 0)

    nu = next(f for f in FERMIONS if f.name == "nu_R^c")
    check("nu_R^c carries B-L = +1", nu.b_minus_l == 1)
    check("nu_R^c carries Y = 0", nu.hypercharge == 0)
    check("nu_R^c is SU(3) x SU(2) singlet", nu.su3_dim == 1 and nu.su2_dim == 1)


def part4_proton_decay_bookkeeping() -> None:
    banner("Part 4: B-L preserving proton-decay bookkeeping")

    # Particle-frame bookkeeping for common proton-decay channels.
    proton_bl = Fraction(1, 1)
    positron_pion_bl = Fraction(1, 1)  # e+ has L=-1, pi0 has B=L=0.
    electron_pion_bl = Fraction(-1, 1)  # e- has L=+1, pi+ has B=L=0.

    check("p -> e+ pi0 preserves B-L", positron_pion_bl - proton_bl == 0)
    check("p -> e- pi+ would violate B-L by -2", electron_pion_bl - proton_bl == -2)


def part5_scope_summary() -> None:
    banner("Part 5: summary")

    print("  LANDED STRUCTURAL CONTENT:")
    print("    G1  grav^2 U(1)_{B-L}              = 0")
    print("    G2  U(1)_{B-L}^3                   = 0")
    print("    G3  SU(3)^2 U(1)_{B-L}             = 0")
    print("    G4  SU(2)^2 U(1)_{B-L}             = 0")
    print("    G5  U(1)_Y^2 U(1)_{B-L}            = 0")
    print("    G6  U(1)_Y U(1)_{B-L}^2            = 0")
    print()
    print("  BOUNDARY:")
    print("    This proves B-L is gaugeable on the retained content.")
    print("    It does not assert that B-L is gauged in the retained framework.")
    print("    It does not predict a Z' mass/coupling or a Majorana mass structure.")


def main() -> int:
    print("=" * 88)
    print("B-L anomaly-freedom theorem verification")
    print("See docs/BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md")
    print("=" * 88)

    part0_content_audit()
    part1_full_anomaly_closure()
    part2_component_contributions()
    part3_nu_r_ablation()
    part4_proton_decay_bookkeeping()
    part5_scope_summary()

    print()
    print("=" * 88)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
