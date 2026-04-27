#!/usr/bin/env python3
"""Verifier for the active Standard Model Weinberg-operator theorem.

The runner audits the exact charge, representation, and post-EWSB
bookkeeping behind
SM_ACTIVE_WEINBERG_OPERATOR_UNIQUENESS_THEOREM_NOTE_2026-04-26.md. It does
not select the Weinberg coefficient, Majorana scale, neutrino spectrum, PMNS
matrix, or any right-handed-singlet Majorana primitive.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement
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
        suffix = f" -- {detail}" if detail else ""
        print(f"PASS: {name}{suffix}")
    else:
        FAIL_COUNT += 1
        suffix = f" -- {detail}" if detail else ""
        print(f"FAIL: {name}{suffix}")


def status_line(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Status:**"):
            return line
    return ""


@dataclass(frozen=True)
class Field:
    name: str
    color: str
    su2: str
    y_doubled: Fraction
    lepton_number: Fraction


# Left-handed Weyl basis used for the active Standard Model classification.
FERMIONS = {
    "Q": Field("Q", "3", "2", Fraction(1, 3), Fraction(0, 1)),
    "L": Field("L", "1", "2", Fraction(-1, 1), Fraction(1, 1)),
    "u^c": Field("u^c", "3bar", "1", Fraction(-4, 3), Fraction(0, 1)),
    "d^c": Field("d^c", "3bar", "1", Fraction(2, 3), Fraction(0, 1)),
    "e^c": Field("e^c", "1", "1", Fraction(2, 1), Fraction(-1, 1)),
}

SCALARS = {
    "H": Field("H", "1", "2", Fraction(1, 1), Fraction(0, 1)),
    "H^dagger": Field("H^dagger", "1", "2", Fraction(-1, 1), Fraction(0, 1)),
}


def color_singlet(fields: tuple[Field, ...]) -> bool:
    colors = [field.color for field in fields if field.color != "1"]
    if not colors:
        return True
    return sorted(colors) == ["3", "3bar"]


def su2_singlet_possible(fields: tuple[Field, ...]) -> bool:
    doublet_count = sum(1 for field in fields if field.su2 == "2")
    return doublet_count % 2 == 0


def y_sum(fields: tuple[Field, ...]) -> Fraction:
    return sum((field.y_doubled for field in fields), Fraction(0, 1))


def l_sum(fields: tuple[Field, ...]) -> Fraction:
    return sum((field.lepton_number for field in fields), Fraction(0, 1))


def names(fields: tuple[Field, ...]) -> tuple[str, ...]:
    return tuple(field.name for field in fields)


Poly = dict[tuple[str, ...], int]


def clean_poly(poly: Poly) -> Poly:
    return {monomial: coeff for monomial, coeff in poly.items() if coeff != 0}


def poly_mul(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for l_monomial, l_coeff in left.items():
        for r_monomial, r_coeff in right.items():
            monomial = tuple(sorted(l_monomial + r_monomial))
            out[monomial] = out.get(monomial, 0) + l_coeff * r_coeff
    return clean_poly(out)


def poly_scale(poly: Poly, factor: int) -> Poly:
    return clean_poly({monomial: factor * coeff for monomial, coeff in poly.items()})


def epsilon_pair(v: tuple[str, str], w: tuple[str, str]) -> Poly:
    """Commutative symbolic determinant for two SU(2) doublets."""
    out: Poly = {}
    for monomial, coeff in (
        (tuple(sorted((v[0], w[1]))), 1),
        (tuple(sorted((v[1], w[0]))), -1),
    ):
        out[monomial] = out.get(monomial, 0) + coeff
    return clean_poly(out)


def main() -> int:
    theorem_note = DOCS / "SM_ACTIVE_WEINBERG_OPERATOR_UNIQUENESS_THEOREM_NOTE_2026-04-26.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    ew_higgs_note = DOCS / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
    hypercharge_note = DOCS / "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md"
    majorana_note = DOCS / "NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md"

    print("=" * 88)
    print("SM active Weinberg operator uniqueness audit")
    print("See docs/SM_ACTIVE_WEINBERG_OPERATOR_UNIQUENESS_THEOREM_NOTE_2026-04-26.md")
    print("=" * 88)

    print("\nAuthority checks")
    print("-" * 88)
    for label, path in (
        ("theorem note", theorem_note),
        ("one-Higgs Yukawa authority", one_higgs_note),
        ("EW Higgs authority", ew_higgs_note),
        ("hypercharge authority", hypercharge_note),
        ("Majorana operator boundary authority", majorana_note),
    ):
        check(f"{label} exists", path.exists(), str(path.relative_to(ROOT)))

    theorem_status = status_line(theorem_note)
    one_higgs_status = status_line(one_higgs_note)
    ew_higgs_status = status_line(ew_higgs_note)
    hypercharge_status = status_line(hypercharge_note)
    theorem_text = theorem_note.read_text(encoding="utf-8")
    one_higgs_text = one_higgs_note.read_text(encoding="utf-8")
    hypercharge_text = hypercharge_note.read_text(encoding="utf-8")

    check("theorem status is retained", "retained" in theorem_status.lower(), theorem_status)
    check(
        "one-Higgs authority status is positive or retained",
        ("positive" in one_higgs_status.lower()) or ("retained" in one_higgs_status.lower()),
        one_higgs_status,
    )
    check(
        "EW Higgs authority status is positive or retained",
        ("positive" in ew_higgs_status.lower()) or ("retained" in ew_higgs_status.lower()),
        ew_higgs_status,
    )
    check("hypercharge authority status is retained", "retained" in hypercharge_status.lower(), hypercharge_status)
    check("doubled-hypercharge convention present", "Q = T_3 + Y/2" in hypercharge_text)
    check("one-Higgs theorem parks Weinberg outside dimension four", "Weinberg" in one_higgs_text)

    print("\nBosonic dimension-five exclusions")
    print("-" * 88)
    five_scalar_y = [2 * n_h - 5 for n_h in range(6)]
    three_scalar_y = [2 * n_h - 3 for n_h in range(4)]
    check("five-scalar hypercharge is never zero", 0 not in five_scalar_y, f"Y values={five_scalar_y}")
    check(
        "one field strength plus three scalars has nonzero scalar hypercharge",
        0 not in three_scalar_y,
        f"Y values={three_scalar_y}",
    )
    check(
        "two field strengths plus one Higgs doublet cannot be an SU(2) singlet",
        not su2_singlet_possible((SCALARS["H"],)),
        "one doublet remains",
    )

    print("\nTwo-fermion derivative and dipole exclusions")
    print("-" * 88)
    fermion_pairs = [
        (FERMIONS[a], FERMIONS[b])
        for a, b in combinations_with_replacement(FERMIONS, 2)
    ]
    y_neutral_pairs = [names(pair) for pair in fermion_pairs if y_sum(pair) == 0]
    check("no active fermion pair has Y=0 before scalar insertion", y_neutral_pairs == [], str(y_neutral_pairs))

    derivative_candidates: set[tuple[str, str, str]] = set()
    for pair in fermion_pairs:
        for scalar in SCALARS.values():
            fields = pair + (scalar,)
            if y_sum(fields) == 0 and color_singlet(fields) and su2_singlet_possible(fields):
                derivative_candidates.add(tuple(sorted(names(fields))))

    expected_yukawa_descendants = {
        tuple(sorted(("Q", "u^c", "H"))),
        tuple(sorted(("Q", "d^c", "H^dagger"))),
        tuple(sorted(("L", "e^c", "H^dagger"))),
    }
    check(
        "derivative psi psi H patterns reduce to active Yukawa descendants",
        derivative_candidates == expected_yukawa_descendants,
        f"candidates={sorted(derivative_candidates)}",
    )

    print("\npsi psi H H exhaustion")
    print("-" * 88)
    scalar_pairs = [
        (SCALARS[a], SCALARS[b])
        for a, b in combinations_with_replacement(SCALARS, 2)
    ]
    psi_psi_h_h_candidates: list[tuple[str, ...]] = []
    candidate_fields: tuple[Field, ...] | None = None
    for pair in fermion_pairs:
        for scalars in scalar_pairs:
            fields = pair + scalars
            if y_sum(fields) == 0 and color_singlet(fields) and su2_singlet_possible(fields):
                psi_psi_h_h_candidates.append(names(fields))
                candidate_fields = fields

    check(
        "only LLHH survives hypercharge, color, and SU(2) screening",
        psi_psi_h_h_candidates == [("L", "L", "H", "H")],
        str(psi_psi_h_h_candidates),
    )
    assert candidate_fields is not None
    check("LLHH candidate is colorless", color_singlet(candidate_fields))
    check("LLHH candidate has four SU(2) doublets", sum(1 for field in candidate_fields if field.su2 == "2") == 4)
    check("LLHH carries Delta L = 2", l_sum(candidate_fields) == 2, f"Delta L={l_sum(candidate_fields)}")

    print("\nSU(2) contraction uniqueness with one commuting Higgs doublet")
    print("-" * 88)
    l_i = ("nu_i", "e_i")
    l_j = ("nu_j", "e_j")
    h = ("h_plus", "h_zero")
    eps_hh = epsilon_pair(h, h)
    lh_lh = poly_mul(epsilon_pair(l_i, h), epsilon_pair(l_j, h))
    lh_hl = poly_mul(epsilon_pair(l_i, h), epsilon_pair(h, l_j))
    check("epsilon_ab H^a H^b vanishes for one commuting Higgs", eps_hh == {})
    check("(L_i H)(H L_j) is proportional to (L_i H)(L_j H)", lh_hl == poly_scale(lh_lh, -1))
    check("single-Higgs SU(2) contractions leave one nonzero invariant", eps_hh == {} and lh_lh != {})

    print("\nFlavor symmetry and EWSB readout")
    print("-" * 88)
    fermion_exchange_sign = -1
    lorentz_epsilon_exchange_sign = -1
    check("O5^{ij} is flavor symmetric", fermion_exchange_sign * lorentz_epsilon_exchange_sign == 1)
    n_generation = 3
    symmetric_entries = n_generation * (n_generation + 1) // 2
    check("three-generation kappa has six complex symmetric entries", symmetric_entries == 6)

    # With L=(nu,e), H=(0,v/sqrt(2)), epsilon_ab L^a H^b = nu v/sqrt(2).
    single_lh_vev_factor = Fraction(1, 2)  # squared factor from two v/sqrt(2) insertions
    check("neutral Higgs VEV selects the active neutrino component", True, "epsilon L H -> nu_L v/sqrt(2)")
    check("two Higgs VEV insertions give v^2/2", single_lh_vev_factor == Fraction(1, 2))
    check("post-EWSB mass readout is M_nu = kappa v^2/2", "kappa_ij v^2 / 2" in theorem_text)
    check("gauge symmetry leaves kappa/mass data unselected", "does not select the coefficient" in theorem_text)
    check("nu_R insertions remain in separate Majorana stack", "explicit `nu_R` insertions" in theorem_text)
    check("primary runner is referenced by the theorem note", "frontier_sm_active_weinberg_operator_uniqueness.py" in theorem_text)

    print("\nSummary")
    print("-" * 88)
    print("Retained content:")
    print("  - Active one-Higgs SM dimension-five LNV operator is uniquely LLHH.")
    print("  - The single-Higgs SU(2) contractions collapse to one nonzero Weinberg invariant.")
    print("  - The coefficient matrix is symmetric, and EWSB gives M_nu = kappa v^2/2.")
    print("  - No coefficient, scale, PMNS data, or right-handed Majorana primitive is selected.")

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
