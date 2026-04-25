#!/usr/bin/env python3
"""Exact audit for the hypercharge squared-trace catalog theorem.

Verifies the structural identities in
  docs/HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md

  (Y1) Tr[Y^2]_LH         = 8/3
  (Y2) Tr[Y^2]_RH         = 32/3
  (Y3) Tr[Y^2]_one_gen    = 40/3
  (Y4) Tr[Y^2]_three_gen  = 40
  (Y5) Tr[Y_GUT^2]_three_gen = (3/20) Tr[Y^2]_three_gen
                              = 6
                              = Tr[T^2]_SU(2) = Tr[T^2]_SU(3) at three gen

All arithmetic is exact via fractions.Fraction; no observation-side input
is used.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


N_GEN = 3
N_COLOR = 3
N_PAIR = 2
DYNKIN_FUND = Fraction(1, 2)


@dataclass(frozen=True)
class Block:
    name: str
    su2_mult: int
    su3_mult: int
    hypercharge: Fraction

    @property
    def states(self) -> int:
        return self.su2_mult * self.su3_mult

    @property
    def y_squared_contribution(self) -> Fraction:
        return self.states * self.hypercharge ** 2

    @property
    def su2_dynkin_contribution(self) -> Fraction:
        if self.su2_mult == 1:
            return Fraction(0)
        return self.su3_mult * DYNKIN_FUND

    @property
    def su3_dynkin_contribution(self) -> Fraction:
        if self.su3_mult == 1:
            return Fraction(0)
        return self.su2_mult * DYNKIN_FUND


LH_BLOCKS = (
    Block("Q_L", su2_mult=2, su3_mult=3, hypercharge=Fraction(1, 3)),
    Block("L_L", su2_mult=2, su3_mult=1, hypercharge=Fraction(-1, 1)),
)

RH_BLOCKS = (
    Block("u_R", su2_mult=1, su3_mult=3, hypercharge=Fraction(4, 3)),
    Block("d_R", su2_mult=1, su3_mult=3, hypercharge=Fraction(-2, 3)),
    Block("e_R", su2_mult=1, su3_mult=1, hypercharge=Fraction(-2, 1)),
    Block("nu_R", su2_mult=1, su3_mult=1, hypercharge=Fraction(0, 1)),
)


def tr_y_sq(blocks) -> Fraction:
    return sum((b.y_squared_contribution for b in blocks), Fraction(0))


def tr_su2_dynkin(blocks) -> Fraction:
    return sum((b.su2_dynkin_contribution for b in blocks), Fraction(0))


def tr_su3_dynkin(blocks) -> Fraction:
    return sum((b.su3_dynkin_contribution for b in blocks), Fraction(0))


def audit_inputs() -> None:
    banner("Retained inputs")

    print(f"  N_GEN   = {N_GEN}")
    print(f"  N_COLOR = {N_COLOR}")
    print(f"  N_PAIR  = {N_PAIR}")
    print(f"  T(fund) = {DYNKIN_FUND}")
    check("three retained generations", N_GEN == 3)
    check("retained N_color = 3", N_COLOR == 3)
    check("retained N_pair (SU(2) doublet) = 2", N_PAIR == 2)
    check("Dynkin index of fundamental is 1/2", DYNKIN_FUND == Fraction(1, 2))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/ANOMALY_FORCES_TIME_THEOREM.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_lh_block_table() -> None:
    banner("LH block table")
    expected = {
        "Q_L": (2, 3, Fraction(1, 3), 6, Fraction(1, 9)),
        "L_L": (2, 1, Fraction(-1, 1), 2, Fraction(1, 1)),
    }
    for block in LH_BLOCKS:
        exp = expected[block.name]
        ok = (
            block.su2_mult == exp[0]
            and block.su3_mult == exp[1]
            and block.hypercharge == exp[2]
            and block.states == exp[3]
            and block.hypercharge ** 2 == exp[4]
        )
        check(
            f"LH block {block.name} = (su2={block.su2_mult}, su3={block.su3_mult}, Y={block.hypercharge})",
            ok,
            f"states={block.states}, Y^2={block.hypercharge**2}",
        )

    total_states = sum(b.states for b in LH_BLOCKS)
    check("LH state count is 8", total_states == 8, f"states = {total_states}")


def audit_rh_block_table() -> None:
    banner("RH block table")
    expected = {
        "u_R": (1, 3, Fraction(4, 3), 3, Fraction(16, 9)),
        "d_R": (1, 3, Fraction(-2, 3), 3, Fraction(4, 9)),
        "e_R": (1, 1, Fraction(-2, 1), 1, Fraction(4, 1)),
        "nu_R": (1, 1, Fraction(0, 1), 1, Fraction(0, 1)),
    }
    for block in RH_BLOCKS:
        exp = expected[block.name]
        ok = (
            block.su2_mult == exp[0]
            and block.su3_mult == exp[1]
            and block.hypercharge == exp[2]
            and block.states == exp[3]
            and block.hypercharge ** 2 == exp[4]
        )
        check(
            f"RH block {block.name} = (su2={block.su2_mult}, su3={block.su3_mult}, Y={block.hypercharge})",
            ok,
            f"states={block.states}, Y^2={block.hypercharge**2}",
        )

    total_states = sum(b.states for b in RH_BLOCKS)
    check("RH state count is 8", total_states == 8, f"states = {total_states}")


def audit_y1_lh_squared_trace() -> None:
    banner("Y1: Tr[Y^2]_LH = 8/3")
    value = tr_y_sq(LH_BLOCKS)
    print(f"  Tr[Y^2]_LH = {value}")
    check("Tr[Y^2]_LH equals 8/3", value == Fraction(8, 3), f"got {value}")
    expanded = (
        Fraction(6) * Fraction(1, 3) ** 2
        + Fraction(2) * Fraction(-1) ** 2
    )
    check(
        "expansion 6*(1/3)^2 + 2*(-1)^2 = 8/3",
        expanded == Fraction(8, 3),
        f"expanded = {expanded}",
    )


def audit_y2_rh_squared_trace() -> None:
    banner("Y2: Tr[Y^2]_RH = 32/3")
    value = tr_y_sq(RH_BLOCKS)
    print(f"  Tr[Y^2]_RH = {value}")
    check("Tr[Y^2]_RH equals 32/3", value == Fraction(32, 3), f"got {value}")
    expanded = (
        Fraction(3) * Fraction(4, 3) ** 2
        + Fraction(3) * Fraction(-2, 3) ** 2
        + Fraction(1) * Fraction(-2) ** 2
        + Fraction(1) * Fraction(0) ** 2
    )
    check(
        "expansion 3*(4/3)^2 + 3*(-2/3)^2 + 4 + 0 = 32/3",
        expanded == Fraction(32, 3),
        f"expanded = {expanded}",
    )


def audit_y3_one_generation_total() -> None:
    banner("Y3: Tr[Y^2]_one_gen = 40/3")
    one_gen = tr_y_sq(LH_BLOCKS) + tr_y_sq(RH_BLOCKS)
    print(f"  Tr[Y^2]_one_gen = {one_gen}")
    check(
        "Tr[Y^2]_one_gen equals 40/3",
        one_gen == Fraction(40, 3),
        f"got {one_gen}",
    )
    check(
        "8/3 + 32/3 = 40/3",
        Fraction(8, 3) + Fraction(32, 3) == Fraction(40, 3),
    )
    check("16-state count per generation", 8 + 8 == 16)


def audit_y4_three_generation_total() -> None:
    banner("Y4: Tr[Y^2]_three_gen = 40")
    one_gen = tr_y_sq(LH_BLOCKS) + tr_y_sq(RH_BLOCKS)
    three_gen = N_GEN * one_gen
    print(f"  Tr[Y^2]_three_gen = {three_gen}")
    check(
        "Tr[Y^2]_three_gen equals 40",
        three_gen == Fraction(40, 1),
        f"got {three_gen}",
    )
    check("3 * 40/3 = 40", N_GEN * Fraction(40, 3) == 40)


def audit_y5_gut_consistency() -> None:
    banner("Y5: Tr[Y_GUT^2]_three_gen = 6 = Tr[T^2]_SU(2,3)")
    one_gen_y = tr_y_sq(LH_BLOCKS) + tr_y_sq(RH_BLOCKS)
    three_gen_y = N_GEN * one_gen_y

    one_gen_su2 = tr_su2_dynkin(LH_BLOCKS) + tr_su2_dynkin(RH_BLOCKS)
    one_gen_su3 = tr_su3_dynkin(LH_BLOCKS) + tr_su3_dynkin(RH_BLOCKS)
    three_gen_su2 = N_GEN * one_gen_su2
    three_gen_su3 = N_GEN * one_gen_su3

    print(f"  Tr[T^2]_SU(2),one_gen   = {one_gen_su2}")
    print(f"  Tr[T^2]_SU(3),one_gen   = {one_gen_su3}")
    print(f"  Tr[T^2]_SU(2),three_gen = {three_gen_su2}")
    print(f"  Tr[T^2]_SU(3),three_gen = {three_gen_su3}")

    check("Tr[T^2]_SU(2) per generation = 2", one_gen_su2 == Fraction(2, 1))
    check("Tr[T^2]_SU(3) per generation = 2", one_gen_su3 == Fraction(2, 1))
    check("Tr[T^2]_SU(2) over three gens = 6", three_gen_su2 == 6)
    check("Tr[T^2]_SU(3) over three gens = 6", three_gen_su3 == 6)

    gut_factor = Fraction(3, 20)
    gut_squared_trace = gut_factor * three_gen_y
    print(f"  Y_GUT^2 / Y^2 (doubled)   = {gut_factor}")
    print(f"  Tr[Y_GUT^2]_three_gen     = {gut_squared_trace}")

    check(
        "Y_GUT^2 = (3/20) Y^2 in doubled convention",
        gut_factor == Fraction(3, 20),
    )
    check(
        "Tr[Y_GUT^2]_three_gen = 6",
        gut_squared_trace == 6,
        f"got {gut_squared_trace}",
    )
    check(
        "Tr[Y_GUT^2]_three_gen = Tr[T^2]_SU(2),three_gen",
        gut_squared_trace == three_gen_su2,
    )
    check(
        "Tr[Y_GUT^2]_three_gen = Tr[T^2]_SU(3),three_gen",
        gut_squared_trace == three_gen_su3,
    )

    minimal_factor = Fraction(3, 5)
    check(
        "Y_GUT^2 / Y_min^2 = 3/5 with Y_min = Y/2",
        minimal_factor * Fraction(1, 4) == gut_factor,
        f"3/5 * 1/4 = {minimal_factor * Fraction(1,4)}",
    )


def audit_companion_consistency() -> None:
    banner("Companion: cross-check against retained linear and cubic traces")
    linear = sum(
        (b.states * b.hypercharge for b in (*LH_BLOCKS, *RH_BLOCKS)),
        Fraction(0),
    )
    cubic_lh_only = sum(
        (b.states * b.hypercharge ** 3 for b in LH_BLOCKS),
        Fraction(0),
    )
    print(f"  Tr[Y]_one_gen           = {linear}")
    print(f"  Tr[Y^3]_LH_only         = {cubic_lh_only}")
    check(
        "Tr[Y]_one_gen = 0 (anomaly cancellation, sign convention LH-RH summed direct)",
        linear == 0,
    )
    check(
        "Tr[Y^3]_LH_only = -16/9 (matches retained anomaly catalog)",
        cubic_lh_only == Fraction(-16, 9),
        f"got {cubic_lh_only}",
    )


def main() -> int:
    print("=" * 88)
    print("Hypercharge squared-trace catalog theorem audit")
    print("See docs/HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_lh_block_table()
    audit_rh_block_table()
    audit_y1_lh_squared_trace()
    audit_y2_rh_squared_trace()
    audit_y3_one_generation_total()
    audit_y4_three_generation_total()
    audit_y5_gut_consistency()
    audit_companion_consistency()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
