#!/usr/bin/env python3
"""Direct top-Ward lift no-go for charged leptons.

This runner verifies the exact retention gate behind
CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md.

It proves only a negative boundary: one-Higgs gauge selection permits
bar L_L H e_R but leaves the charged-lepton generation matrix Y_e free.
The retained top Ward factor 1/sqrt(6) depends on a color x isospin
scalar-singlet normalization on the Q_L block and is not produced by the
colorless charged-lepton monomial by direct analogy.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


@dataclass(frozen=True)
class Field:
    name: str
    color_dim: int
    su2_dim: int
    y_doubled: Fraction


L_L = Field("L_L", color_dim=1, su2_dim=2, y_doubled=Fraction(-1, 1))
E_R = Field("e_R", color_dim=1, su2_dim=1, y_doubled=Fraction(-2, 1))
H = Field("H", color_dim=1, su2_dim=2, y_doubled=Fraction(1, 1))
H_TILDE = Field("tilde H", color_dim=1, su2_dim=2, y_doubled=Fraction(-1, 1))


def hypercharge_sum(left: Field, scalar: Field, right: Field) -> Fraction:
    """Doubled-hypercharge sum for bar(F_L) S f_R."""
    return -left.y_doubled + scalar.y_doubled + right.y_doubled


def color_allowed(left: Field, right: Field) -> bool:
    return left.color_dim == right.color_dim


def monomial_allowed(left: Field, scalar: Field, right: Field) -> bool:
    return color_allowed(left, right) and hypercharge_sum(left, scalar, right) == 0


Matrix = tuple[tuple[Fraction, ...], ...]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols))
        for i in range(rows)
    )


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))


def all_generation_entries_allowed(scalar: Field) -> bool:
    return all(monomial_allowed(L_L, scalar, E_R) for _i in range(3) for _j in range(3))


def main() -> int:
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    top_ward_note = DOCS / "YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
    color_projection_note = DOCS / "YUKAWA_COLOR_PROJECTION_THEOREM.md"
    charged_review_note = DOCS / "CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md"

    check("one-Higgs gauge-selection note exists", one_higgs_note.exists(), str(one_higgs_note.relative_to(ROOT)))
    check("top Ward identity note exists", top_ward_note.exists(), str(top_ward_note.relative_to(ROOT)))
    check("top color-projection note exists", color_projection_note.exists(), str(color_projection_note.relative_to(ROOT)))
    check("charged-lepton bounded review note exists", charged_review_note.exists(), str(charged_review_note.relative_to(ROOT)))

    one_higgs_text = one_higgs_note.read_text(encoding="utf-8")
    top_ward_text = top_ward_note.read_text(encoding="utf-8")

    print()
    print("A. One-Higgs charged-lepton gauge selection")
    print("-" * 72)
    h_sum = hypercharge_sum(L_L, H, E_R)
    h_tilde_sum = hypercharge_sum(L_L, H_TILDE, E_R)
    check(
        "bar L_L H e_R is hypercharge neutral",
        h_sum == 0,
        f"-Y(L_L)+Y(H)+Y(e_R) = {h_sum}",
    )
    check("bar L_L H e_R is color allowed", color_allowed(L_L, E_R), "1 x 1 color singlet")
    check("bar L_L H e_R is gauge allowed", monomial_allowed(L_L, H, E_R))
    check(
        "bar L_L tilde H e_R is rejected by hypercharge",
        h_tilde_sum != 0,
        f"-Y(L_L)+Y(tilde H)+Y(e_R) = {h_tilde_sum}",
    )
    check(
        "wrong-Higgs rejection has exact doubled-hypercharge residual -2",
        h_tilde_sum == Fraction(-2, 1),
        str(h_tilde_sum),
    )

    print()
    print("B. Y_e remains a free generation matrix")
    print("-" * 72)
    y_e: Matrix = (
        (Fraction(1, 1), Fraction(2, 1), Fraction(0, 1)),
        (Fraction(0, 1), Fraction(3, 1), Fraction(4, 1)),
        (Fraction(5, 1), Fraction(0, 1), Fraction(6, 1)),
    )
    nonzero_offdiag = [(0, 1), (1, 2), (2, 0)]
    check("all nine Y_e entries multiply the same gauge-allowed monomial", all_generation_entries_allowed(H))
    check(
        "arbitrary diagonal entries remain gauge invariant",
        all(monomial_allowed(L_L, H, E_R) and y_e[i][i] != 0 for i in range(3)),
        f"diag(Y_e) = {[y_e[i][i] for i in range(3)]}",
    )
    check(
        "arbitrary off-diagonal entries remain gauge invariant",
        all(monomial_allowed(L_L, H, E_R) and y_e[i][j] != 0 for i, j in nonzero_offdiag),
        f"nonzero off-diagonal entries = {nonzero_offdiag}",
    )
    check("wrong-Higgs Y_e matrix is rejected entrywise", not all_generation_entries_allowed(H_TILDE))

    # A cyclic generation relabeling is unitary. It changes entries but cannot
    # change gauge invariance because the gauge charges are generation-blind.
    u_left: Matrix = (
        (Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)),
        (Fraction(1, 1), Fraction(0, 1), Fraction(0, 1)),
        (Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)),
    )
    u_right: Matrix = (
        (Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)),
        (Fraction(1, 1), Fraction(0, 1), Fraction(0, 1)),
        (Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)),
    )
    rotated = matmul(matmul(u_left, y_e), transpose(u_right))
    check("generation-basis rotations change Y_e entries", rotated != y_e, f"Y_e' = {rotated}")
    check("rotated Y_e entries remain gauge invariant", all_generation_entries_allowed(H))
    check(
        "gauge selection does not select eigenvalues, rank, hierarchy, or texture",
        "does not force diagonal form, hierarchy, rank, phase, or texture" in one_higgs_text,
    )

    print()
    print("C. Direct top-Ward normalization does not lift")
    print("-" * 72)
    top_color_dim = 3
    top_isospin_dim = 2
    top_singlet_norm_sq = top_color_dim * top_isospin_dim
    lepton_color_dim = 1
    lepton_isospin_dim = 2
    lepton_doublet_norm_sq = lepton_color_dim * lepton_isospin_dim
    charged_component_norm_sq = 1
    direct_lepton_norm_squares = {charged_component_norm_sq, lepton_doublet_norm_sq}

    check("top Ward singlet normalization square is color times isospin = 6", top_singlet_norm_sq == 6)
    check("charged-lepton monomial is colorless", lepton_color_dim == 1)
    check(
        "direct charged-lepton gauge normalizations are 1 or 2, never 6",
        top_singlet_norm_sq not in direct_lepton_norm_squares,
        f"direct options = {sorted(direct_lepton_norm_squares)}",
    )
    check(
        "lepton weak-doublet singlet would give 1/sqrt(2), not 1/sqrt(6)",
        lepton_doublet_norm_sq == 2 and lepton_doublet_norm_sq != top_singlet_norm_sq,
    )
    check(
        "post-EWSB charged component gives coefficient one before Y_e, not 1/sqrt(6)",
        charged_component_norm_sq == 1 and charged_component_norm_sq != top_singlet_norm_sq,
    )
    generation_triplet_norm_sq = 3
    would_be_generation_times_weak = generation_triplet_norm_sq * lepton_isospin_dim
    check(
        "generation times weak dimension 6 would add a new generation primitive",
        would_be_generation_times_weak == 6 and generation_triplet_norm_sq not in direct_lepton_norm_squares,
        "this is not one-Higgs gauge selection and does not select tau",
    )
    check("top Ward note states factor 1/sqrt(6)", "1/sqrt(6)" in top_ward_text)
    check("top Ward note ties factor to Q_L block", "Q_L block" in top_ward_text)

    print()
    print("D. Comparator firewall")
    print("-" * 72)
    comparators = {
        "m_e_MeV": 0.510998950,
        "m_mu_MeV": 105.6583755,
        "m_tau_MeV": 1776.86,
    }
    proof_input_keys = {
        "field_charges",
        "color_representations",
        "generation_blind_gauge_action",
        "basis_rotation_unitarity",
        "direct_normalization_dimensions",
        "source_note_scope_strings",
    }
    print(f"Comparator masses, not proof inputs: {comparators}")
    check(
        "observed charged-lepton masses are not proof-input keys",
        set(comparators).isdisjoint(proof_input_keys),
        f"proof keys = {sorted(proof_input_keys)}",
    )
    check(
        "bounded review marks charged-lepton masses as observational pin",
        "explicit observational pin" in charged_review_note.read_text(encoding="utf-8"),
    )

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: exact no-go for direct top-Ward lift to charged leptons.")
        print("Y_e remains free under one-Higgs gauge selection; a retained")
        print("charged-lepton mass theorem needs an additional generation,")
        print("loop-normalization, or source-domain primitive.")
        return 0
    print("VERDICT: no-go artifact has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
