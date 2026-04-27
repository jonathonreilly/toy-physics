#!/usr/bin/env python3
r"""
Cl(3) Yukawa Casimir-Difference Bridge — Candidate Lemma runner.

Verifies the support-grade content of
docs/CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md.

What this runner verifies:
  - Retained gauge inputs T = 1/2, Y = -1/2 for lepton L doublet
  - RHS = T(T+1) - Y² = 1/2 (exact Fraction)
  - Three Q-bridge support faces all give 1/2 (exact Fraction)
  - Compositional collapse: all three reduce to (dim(SU(2)_L)-1)/dim(Cl⁺(3))
  - Brannen relation: |b|²/a² = 1/2 ⇔ c = √2 ⇔ Q = 2/3

What this runner does NOT verify (because it is not yet derived):
  - The Yukawa Casimir-difference candidate lemma |b|²/a² = T(T+1)-Y²
    as a structural identification on the physical lepton Yukawa amplitude.

The candidate lemma's RHS is retained algebra; the LHS is the Q-bridge
primitive; the bridge between them is the open Q-side closure step.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import Tuple


PASSES: list[Tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    # ------------------------------------------------------------------------
    # Section 1: Retained gauge inputs for lepton L doublet
    # ------------------------------------------------------------------------
    section("§1. Retained gauge inputs for lepton L doublet (CL3_SM_EMBEDDING_THEOREM)")

    T = Fraction(1, 2)  # SU(2)_L weak isospin for doublet
    Y = Fraction(-1, 2)  # SM hypercharge of left-handed lepton doublet

    check(
        "1.1 T = 1/2 (lepton L doublet, SU(2)_L doublet from Cl⁺(3) ≅ ℍ)",
        T == Fraction(1, 2),
        f"T = {T} (CL3_SM_EMBEDDING §A: SU(2)_L generators J_k, Casimir = 3/4)",
    )

    check(
        "1.2 Y = -1/2 (left-handed lepton doublet hypercharge, SM)",
        Y == Fraction(-1, 2),
        f"Y = {Y} (CL3_SM_EMBEDDING §E: P_antisymm ⊗ fiber, lepton L block)",
    )

    # ------------------------------------------------------------------------
    # Section 2: RHS computation: T(T+1) - Y² = 1/2
    # ------------------------------------------------------------------------
    section("§2. RHS algebraic identity: T(T+1) - Y² = 1/2 for lepton L doublet")

    T_T_plus_1 = T * (T + 1)
    Y_squared = Y * Y
    RHS = T_T_plus_1 - Y_squared

    check(
        "2.1 T(T+1) = 1/2 · 3/2 = 3/4 (Casimir of spin-1/2 doublet)",
        T_T_plus_1 == Fraction(3, 4),
        f"T(T+1) = {T_T_plus_1}",
    )

    check(
        "2.2 Y² = (-1/2)² = 1/4",
        Y_squared == Fraction(1, 4),
        f"Y² = {Y_squared}",
    )

    check(
        "2.3 T(T+1) - Y² = 3/4 - 1/4 = 1/2 (retained algebraic identity)",
        RHS == Fraction(1, 2),
        f"T(T+1) - Y² = {RHS}",
    )

    # ------------------------------------------------------------------------
    # Section 3: Three Q-bridge support faces all give 1/2
    # ------------------------------------------------------------------------
    section("§3. Three Q-bridge support faces all give 1/2 (KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE)")

    # F_dim: dim(spinor of Cl⁺(3)) / dim(Cl⁺(3))
    dim_spinor_Cl_plus_3 = 2  # complex spinor of ℍ ≅ Cl⁺(3) is 2-dim
    dim_Cl_plus_3 = 4  # {I, e_12, e_13, e_23}
    F_dim = Fraction(dim_spinor_Cl_plus_3, dim_Cl_plus_3)
    check(
        "3.1 F_dim: dim(spinor) / dim(Cl⁺(3)) = 2/4 = 1/2",
        F_dim == Fraction(1, 2),
        f"dim(spinor) = {dim_spinor_Cl_plus_3}, dim(Cl⁺(3)) = {dim_Cl_plus_3}, F_dim = {F_dim}",
    )

    # F_T: T(T+1) - Y²
    F_T = RHS
    check(
        "3.2 F_T: T(T+1) - Y² = 1/2",
        F_T == Fraction(1, 2),
        f"F_T = {F_T}",
    )

    # F_TY: (T(T+1) - Y²) / (T(T+1) + Y²)
    F_TY = (T_T_plus_1 - Y_squared) / (T_T_plus_1 + Y_squared)
    check(
        "3.3 F_TY: (T(T+1)-Y²) / (T(T+1)+Y²) = (1/2)/(1) = 1/2",
        F_TY == Fraction(1, 2),
        f"F_TY = {F_TY}",
    )

    check(
        "3.4 All three faces give the same value 1/2 (collapse to single primitive)",
        F_dim == F_T == F_TY == Fraction(1, 2),
        f"F_dim = F_T = F_TY = {F_dim}",
    )

    # ------------------------------------------------------------------------
    # Section 4: Compositional collapse to single Cl(3) sub-algebra dimension count
    # ------------------------------------------------------------------------
    section("§4. Compositional identity: all three faces ↔ Cl(3) sub-algebra count")

    dim_SU2_L = 3  # three bivector generators of Cl⁺(3): {e_12, e_13, e_23}
    dim_U1_Y_central = 1  # the pseudoscalar ω
    composite = Fraction(dim_SU2_L - dim_U1_Y_central, dim_Cl_plus_3)
    check(
        "4.1 Composite: (dim(SU(2)_L) - dim(U(1)_Y central)) / dim(Cl⁺(3)) = (3-1)/4 = 1/2",
        composite == Fraction(1, 2),
        f"(dim(SU(2)_L) - dim(U(1)_Y central)) / dim(Cl⁺(3)) = ({dim_SU2_L} - {dim_U1_Y_central})/{dim_Cl_plus_3} = {composite}",
    )

    check(
        "4.2 All three Q-bridge faces collapse to this Cl(3) sub-algebra count",
        F_dim == F_T == F_TY == composite == Fraction(1, 2),
        f"F_dim = {F_dim}, F_T = {F_T}, F_TY = {F_TY}, composite = {composite}",
    )

    # ------------------------------------------------------------------------
    # Section 5: Brannen relation between P_Q and Q
    # ------------------------------------------------------------------------
    section("§5. Brannen relation: |b|²/a² = 1/2 ⇔ c = √2 ⇔ Q = 2/3")

    P_Q = Fraction(1, 2)
    # c² = 4 |b|²/a² = 4 · P_Q = 2 ⇒ c = √2
    c_squared = 4 * P_Q
    check(
        "5.1 P_Q = 1/2 forces c² = 4·P_Q = 2 (Brannen carrier condition)",
        c_squared == 2,
        f"c² = 4 · P_Q = {c_squared}",
    )

    # Q = (2 + c²) / 6 (Brannen formula → Koide ratio derivation)
    Q = (2 + c_squared) / 6
    check(
        "5.2 Q = (2 + c²) / 6 = 4/6 = 2/3 (Koide for charged leptons)",
        Q == Fraction(2, 3),
        f"Q = (2 + {c_squared}) / 6 = {Q}",
    )

    # ------------------------------------------------------------------------
    # Section 6: scope statement — what this runner does NOT verify
    # ------------------------------------------------------------------------
    section("§6. Scope statement: candidate lemma articulated, NOT derived")

    print("This runner verifies:")
    print("  - Retained gauge inputs T = 1/2, Y = -1/2 for lepton L doublet")
    print("  - RHS = T(T+1) - Y² = 1/2 (exact Fraction)")
    print("  - Three Q-bridge support faces all give 1/2 (exact Fraction)")
    print("  - Compositional collapse to (dim(SU(2)_L)-1)/dim(Cl⁺(3)) = 1/2")
    print("  - Brannen relation: P_Q = 1/2 → c = √2 → Q = 2/3")
    print()
    print("This runner does NOT verify:")
    print()
    print("  The Yukawa Casimir-difference candidate lemma")
    print()
    print("    |b|² / a² = T(T+1) - Y² on the physical lepton Yukawa amplitude")
    print()
    print("  as a structural identification. Both sides equal 1/2 numerically on")
    print("  retained data, but the structural derivation chain that takes")
    print("  T(T+1) - Y² (gauge-Casimir-space) into the lepton-flavor amplitude")
    print("  moduli (a, |b|) is the open Q-side closure step.")
    print()
    print("  See docs/CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_CANDIDATE_NOTE_2026-04-25.md §3")
    print("  for the specific structural derivation gap that remains open.")

    # ------------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------------
    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    n_fail = n_total - n_pass
    print(f"PASSED: {n_pass}/{n_total}")
    for label, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print()
    print("Closeout flags:")
    print("  Q_BRIDGE_SUPPORT_FACES_ALGEBRAIC_VALUES_RETAINED=TRUE")
    print("  RHS_T_T_PLUS_1_MINUS_Y_SQ_EQ_HALF_FOR_LEPTON_L_DOUBLET=RETAINED")
    print("  ALGEBRAIC_FACES_COMPOSITIONAL_COLLAPSE_TO_CL3_DIMENSION_COUNT=TRUE")
    print("  YUKAWA_CASIMIR_DIFFERENCE_LEMMA=ARTICULATED_AS_CANDIDATE_NOT_DERIVED")
    print("  P_Q_BRIDGE_PHYSICAL_DERIVATION_ON_FLAVOR_AMPLITUDE=STILL_OPEN")
    print("  Q_L_EQ_2_OVER_3_RETAINED_CLOSURE=FALSE")

    if n_fail == 0:
        print()
        print("VERDICT: candidate lemma articulated and retained algebraic")
        print("  pieces verified. RHS = 1/2 from gauge structure; LHS = P_Q is")
        print("  the open Q-bridge primitive. Closure of the candidate lemma")
        print("  requires a structural derivation chain (see note §3) not")
        print("  supplied in this runner.")
        return 0
    else:
        print()
        print(f"VERDICT: support not all verified — {n_fail} FAIL.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
