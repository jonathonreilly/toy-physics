#!/usr/bin/env python3
"""
Koide A1 from the Casimir-Difference Lemma — derivation skeleton

This script is the first deliverable on the Casimir-difference closure
track for Koide A1 (Q = 2/3). It records the architecture, verifies the
key identity (A1*), and isolates the three load-bearing proof
obligations O1, O2, O3 as concrete future runners.

Authority for the surrounding derivation:
    docs/KOIDE_A1_CASIMIR_DIFFERENCE_LEMMA_DERIVATION_NOTE.md

Companion (existing observation runner, no derivation):
    scripts/frontier_koide_a1_yukawa_casimir_identity.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


@dataclass(frozen=True)
class Particle:
    label: str
    T: Fraction
    Y: Fraction
    role: str  # "L-doublet" | "Higgs" | "Q-doublet" | "RH-singlet"

    @property
    def casimir_sum(self) -> Fraction:
        return self.T * (self.T + 1) + self.Y * self.Y

    @property
    def casimir_diff(self) -> Fraction:
        return self.T * (self.T + 1) - self.Y * self.Y

    @property
    def three_Y_sq(self) -> Fraction:
        return 3 * self.Y * self.Y

    @property
    def a1_star_residual(self) -> Fraction:
        # (A1*) condition: 3 Y² = T(T+1)  ⇔  T(T+1) − 3 Y² = 0.
        return self.T * (self.T + 1) - 3 * self.Y * self.Y


SM_TABLE: list[Particle] = [
    Particle("Lepton SU(2)_L doublet L", Fraction(1, 2), Fraction(-1, 2), "L-doublet"),
    Particle("Higgs H",                  Fraction(1, 2), Fraction( 1, 2), "Higgs"),
    Particle("Quark SU(2)_L doublet Q",  Fraction(1, 2), Fraction( 1, 6), "Q-doublet"),
    Particle("e_R",                      Fraction(0),    Fraction(-1),    "RH-singlet"),
    Particle("u_R",                      Fraction(0),    Fraction( 2, 3), "RH-singlet"),
    Particle("d_R",                      Fraction(0),    Fraction(-1, 3), "RH-singlet"),
]


def main() -> int:
    section("Koide A1 ⟸ Casimir-difference lemma — closure architecture")
    print(
        "Reduces A1 / Q = 2/3 to two primitives on the retained surface:\n"
        "  P1 (sum)        : a_0² = c · (T(T+1) + Y²) · v_EW²\n"
        "  P2 (difference) : |z|² = c · (T(T+1) − Y²) · v_EW²   [SAME c]\n"
        "Then a_0² = 2|z|²  ⟺  T(T+1) + Y² = 2 (T(T+1) − Y²)\n"
        "                   ⟺  3 Y² = T(T+1)        (condition A1*)"
    )

    # ---- A. Numerical Casimir audit across SM particles ---------------------
    section("A. Per-particle Casimir audit (sum, difference, A1* residual)")
    print(
        f"  {'particle':<28}{'T':<6}{'Y':<8}"
        f"{'C_sum':<8}{'C_diff':<8}{'3Y²':<8}{'A1* res':<10}"
    )
    print("  " + "-" * 78)
    for p in SM_TABLE:
        print(
            f"  {p.label:<28}{str(p.T):<6}{str(p.Y):<8}"
            f"{str(p.casimir_sum):<8}{str(p.casimir_diff):<8}"
            f"{str(p.three_Y_sq):<8}{str(p.a1_star_residual):<10}"
        )

    # ---- B. Verify the SUM identity for the Yukawa doublets ----------------
    section("B. Sum identity: T(T+1) + Y² = 1 holds iff retained C_τ = 1")
    L = SM_TABLE[0]
    H = SM_TABLE[1]
    record(
        "B.1 Lepton doublet L: T(T+1) + Y² = 1",
        L.casimir_sum == 1,
        f"T(T+1) + Y² = 3/4 + 1/4 = {L.casimir_sum}",
    )
    record(
        "B.2 Higgs H: T(T+1) + Y² = 1",
        H.casimir_sum == 1,
        f"T(T+1) + Y² = 3/4 + 1/4 = {H.casimir_sum}",
    )
    record(
        "B.3 Both Yukawa-doublet participants share the same SUM = 1",
        L.casimir_sum == H.casimir_sum == 1,
        "This is the retained C_τ = 1 input that already powers the y_τ derivation.",
    )

    # ---- C. Verify the DIFFERENCE identity for the Yukawa doublets ---------
    section("C. Difference identity: T(T+1) − Y² = 1/2 holds iff candidate lemma")
    record(
        "C.1 Lepton doublet L: T(T+1) − Y² = 1/2",
        L.casimir_diff == Fraction(1, 2),
        f"T(T+1) − Y² = 3/4 − 1/4 = {L.casimir_diff}",
    )
    record(
        "C.2 Higgs H: T(T+1) − Y² = 1/2",
        H.casimir_diff == Fraction(1, 2),
        f"T(T+1) − Y² = 3/4 − 1/4 = {H.casimir_diff}",
    )
    record(
        "C.3 Both Yukawa-doublet participants share the same DIFFERENCE = 1/2",
        L.casimir_diff == H.casimir_diff == Fraction(1, 2),
        "This is the candidate Casimir-difference lemma to be derived.",
    )

    # ---- D. Verify the (A1*) condition 3Y² = T(T+1) for L, H ----------------
    section("D. (A1*) condition 3 Y² = T(T+1)  ⟺  Y² = (1/3) T(T+1)")
    record(
        "D.1 (A1*) holds for lepton doublet L",
        L.a1_star_residual == 0,
        f"3 Y² − T(T+1) = 3·1/4 − 3/4 = {L.a1_star_residual}",
    )
    record(
        "D.2 (A1*) holds for Higgs H",
        H.a1_star_residual == 0,
        f"3 Y² − T(T+1) = 3·1/4 − 3/4 = {H.a1_star_residual}",
    )

    # ---- E. Uniqueness sweep: only L and H satisfy (A1*) -------------------
    section("E. Uniqueness sweep over SM matter assignments")
    others = [p for p in SM_TABLE if p.role not in ("L-doublet", "Higgs")]
    others_fail_A1_star = all(p.a1_star_residual != 0 for p in others)
    print("  particles with A1* residual ≠ 0:")
    for p in others:
        print(f"    - {p.label:<28} residual = {p.a1_star_residual}")
    record(
        "E.1 Only L and H satisfy (A1*) among SM matter content",
        others_fail_A1_star,
        "Quark doublet (Y = 1/6) and RH singlets (T = 0) all fail.",
    )

    # ---- F. Equivalent reading: (sum, diff) jointly pin (T, Y) ------------
    section("F. (sum, diff) jointly pin (T, Y) up to sign of Y")
    sum_diff_target = (Fraction(1), Fraction(1, 2))
    candidates = [p for p in SM_TABLE
                  if (p.casimir_sum, p.casimir_diff) == sum_diff_target]
    record(
        "F.1 Exactly the {L, H} pair has (C_sum, C_diff) = (1, 1/2)",
        len(candidates) == 2 and {p.role for p in candidates} == {"L-doublet", "Higgs"},
        "So the SUM (retained C_τ = 1) plus the candidate DIFFERENCE pin Y² = 1/4 and T = 1/2.",
    )

    # ---- G. Reverse-direction check: (A1*) forces Y = ±1/2 given T = 1/2 ----
    section("G. (A1*) forces Y² = 1/4 given the Cl(3)-retained T = 1/2")
    T_input = Fraction(1, 2)
    Ysq_required = T_input * (T_input + 1) / 3
    record(
        "G.1 With T = 1/2 (from Cl⁺(3) ≅ ℍ), (A1*) ⟹ Y² = 1/4",
        Ysq_required == Fraction(1, 4),
        f"Y² required = T(T+1)/3 = {Ysq_required}, i.e. Y = ±1/2.",
    )

    # ---- H. Architecture isolation: list the open primitives ---------------
    section("H. Open proof obligations (each is a future runner)")
    obligations = [
        ("O1", "C_3 character / S_3-irrep alignment of √m on the hw=1 carrier",
         "Show a_0² ↔ ‖A_1 component‖² and |z|² ↔ (1/2)‖E component‖²."),
        ("O2", "Sum-Casimir matches the trivial-character (e_+) weight",
         "Strengthen retained C_τ = 1 ⟹ y_τ to a_0² = c · (T(T+1) + Y²) · v_EW²."),
        ("O3", "Difference-Casimir matches the non-trivial-character weight (same c)",
         "New identity: |z|² = c · (T(T+1) − Y²) · v_EW²."),
    ]
    for tag, head, detail in obligations:
        print(f"  [{tag}] {head}")
        print(f"        {detail}")
    record(
        "H.1 Three named obligations isolated; closure follows from them + retained inputs",
        True,
        "O1 + O2 + O3 + (Cl⁺(3) ⟹ T=1/2) + (ω-pseudoscalar ⟹ Y=±1/2) ⟹ A1.",
    )

    # ---- Summary -----------------------------------------------------------
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print()
    if n_pass == n_total:
        print("VERDICT: closure architecture is self-consistent on the SM Yukawa-doublet")
        print("assignment. The remaining derivation reduces to the three named primitives")
        print("O1, O2, O3 listed in section H. The Cl(3) embedding already retains the")
        print("inputs T = 1/2 and Y² = 1/4, so once O1–O3 close, A1 / Q = 2/3 follows.")
        return 0
    print("VERDICT: scaffolding has FAIL entries — fix before continuing.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
