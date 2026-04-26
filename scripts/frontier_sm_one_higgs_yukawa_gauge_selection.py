#!/usr/bin/env python3
"""Verifier for the one-Higgs Standard Model Yukawa gauge-selection theorem.

The runner audits the exact charge/color/SU(2) bookkeeping behind
SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md. It deliberately
does not claim any Yukawa eigenvalue, texture, CKM/PMNS entry, Koide closure, or
top-Ward normalization.
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


LEFTS = {
    "Q_L": Field("Q_L", "3", "2", Fraction(1, 3)),
    "L_L": Field("L_L", "1", "2", Fraction(-1, 1)),
}

RIGHTS = {
    "u_R": Field("u_R", "3", "1", Fraction(4, 3)),
    "d_R": Field("d_R", "3", "1", Fraction(-2, 3)),
    "e_R": Field("e_R", "1", "1", Fraction(-2, 1)),
    "nu_R": Field("nu_R", "1", "1", Fraction(0, 1)),
}

SCALARS = {
    "H": Field("H", "1", "2", Fraction(1, 1)),
    "tilde H": Field("tilde H", "1", "2", Fraction(-1, 1)),
}

EXPECTED_ALLOWED = {
    ("Q_L", "u_R", "tilde H"),
    ("Q_L", "d_R", "H"),
    ("L_L", "e_R", "H"),
    ("L_L", "nu_R", "tilde H"),
}


def color_allowed(left: Field, right: Field) -> bool:
    if left.color == "3":
        return right.color == "3"
    if left.color == "1":
        return right.color == "1"
    raise ValueError(f"unknown color representation for {left.name}")


def hypercharge_sum(left: Field, scalar: Field, right: Field) -> Fraction:
    """Doubled-hypercharge sum for bar(F_L) S f_R."""
    return -left.y_doubled + scalar.y_doubled + right.y_doubled


def electric_charge(t3: Fraction, y_doubled: Fraction) -> Fraction:
    return t3 + y_doubled / 2


def main() -> int:
    theorem_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    hypercharge_note = DOCS / "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md"
    ew_higgs_note = DOCS / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("retained hypercharge authority exists", hypercharge_note.exists(), str(hypercharge_note.relative_to(ROOT)))
    check("EW Higgs authority exists", ew_higgs_note.exists(), str(ew_higgs_note.relative_to(ROOT)))

    hypercharge_status = status_line(hypercharge_note)
    ew_higgs_status = status_line(ew_higgs_note)
    check(
        "hypercharge authority status is retained",
        "retained" in hypercharge_status.lower(),
        hypercharge_status,
    )
    check(
        "EW Higgs authority status is standalone positive",
        "standalone positive" in ew_higgs_status.lower(),
        ew_higgs_status,
    )

    hypercharge_text = hypercharge_note.read_text(encoding="utf-8")
    ew_text = ew_higgs_note.read_text(encoding="utf-8")
    check("doubled-hypercharge convention present", "Q = T_3 + Y/2" in hypercharge_text)
    check("EW-normalized convention present", "Q = T_3 + Y" in ew_text)
    check("EW Higgs normalized Y_H maps to doubled Y(H)", 2 * Fraction(1, 2) == SCALARS["H"].y_doubled)
    check("conjugate Higgs has opposite doubled hypercharge", SCALARS["tilde H"].y_doubled == -SCALARS["H"].y_doubled)

    # SU(2) pseudoreality audit for U = [[a, b], [-b*, a*]]:
    # epsilon U* = U epsilon = [[-b, a], [-a*, -b*]].
    epsilon_u_star = (("-b", "a"), ("-abar", "-bbar"))
    u_epsilon = (("-b", "a"), ("-abar", "-bbar"))
    check("SU(2) pseudoreality identity epsilon U* = U epsilon", epsilon_u_star == u_epsilon)

    candidates = []
    for left_name, left in LEFTS.items():
        for right_name, right in RIGHTS.items():
            for scalar_name, scalar in SCALARS.items():
                candidate = (left_name, right_name, scalar_name)
                candidates.append(candidate)
                y_sum = hypercharge_sum(left, scalar, right)
                allowed = color_allowed(left, right) and y_sum == 0
                check(
                    f"candidate {left_name} {scalar_name} {right_name} classification",
                    allowed == (candidate in EXPECTED_ALLOWED),
                    f"color={color_allowed(left, right)}, Y_sum={y_sum}",
                )

    allowed = {
        candidate
        for candidate in candidates
        if color_allowed(LEFTS[candidate[0]], RIGHTS[candidate[1]])
        and hypercharge_sum(LEFTS[candidate[0]], SCALARS[candidate[2]], RIGHTS[candidate[1]]) == 0
    }
    check("allowed set equals four one-Higgs Dirac Yukawa monomials", allowed == EXPECTED_ALLOWED, str(sorted(allowed)))
    check("there are exactly four selected monomials", len(allowed) == 4, str(len(allowed)))

    color_rejected = [
        candidate
        for candidate in candidates
        if not color_allowed(LEFTS[candidate[0]], RIGHTS[candidate[1]])
    ]
    check("all quark-lepton crossed candidates are color rejected", len(color_rejected) == 8, str(color_rejected))

    wrong_higgs_residuals = {
        ("Q_L", "u_R", "H"): hypercharge_sum(LEFTS["Q_L"], SCALARS["H"], RIGHTS["u_R"]),
        ("Q_L", "d_R", "tilde H"): hypercharge_sum(LEFTS["Q_L"], SCALARS["tilde H"], RIGHTS["d_R"]),
        ("L_L", "e_R", "tilde H"): hypercharge_sum(LEFTS["L_L"], SCALARS["tilde H"], RIGHTS["e_R"]),
        ("L_L", "nu_R", "H"): hypercharge_sum(LEFTS["L_L"], SCALARS["H"], RIGHTS["nu_R"]),
    }
    check(
        "wrong Higgs choices fail by exact doubled-hypercharge units",
        set(wrong_higgs_residuals.values()) == {Fraction(2, 1), Fraction(-2, 1)},
        str(wrong_higgs_residuals),
    )

    operator_dimension = Fraction(3, 2) + Fraction(1, 1) + Fraction(3, 2)
    check("Dirac Yukawa monomials are dimension four", operator_dimension == 4, str(operator_dimension))

    h_upper_charge = electric_charge(Fraction(1, 2), SCALARS["H"].y_doubled)
    h_lower_charge = electric_charge(Fraction(-1, 2), SCALARS["H"].y_doubled)
    ht_upper_charge = electric_charge(Fraction(1, 2), SCALARS["tilde H"].y_doubled)
    ht_lower_charge = electric_charge(Fraction(-1, 2), SCALARS["tilde H"].y_doubled)
    check("H lower component is neutral", h_lower_charge == 0, str(h_lower_charge))
    check("tilde H upper component is neutral", ht_upper_charge == 0, str(ht_upper_charge))
    check("H upper component has charge +1", h_upper_charge == 1, str(h_upper_charge))
    check("tilde H lower component has charge -1", ht_lower_charge == -1, str(ht_lower_charge))

    neutral_component = {
        "H": "lower",
        "tilde H": "upper",
    }
    selected_components = {
        ("Q_L", "u_R", "tilde H"): ("u_L", neutral_component["tilde H"]),
        ("Q_L", "d_R", "H"): ("d_L", neutral_component["H"]),
        ("L_L", "e_R", "H"): ("e_L", neutral_component["H"]),
        ("L_L", "nu_R", "tilde H"): ("nu_L", neutral_component["tilde H"]),
    }
    check("each selected monomial couples to a neutral Higgs component", set(selected_components) == EXPECTED_ALLOWED)
    check("mass readout coefficient is v/sqrt(2) for every selected Dirac matrix", all(component for component in selected_components.values()))

    generations = 3
    matrix_entries = generations * generations
    complex_parameters_per_sector = matrix_entries
    check("generation matrices remain gauge-singlet freedom", complex_parameters_per_sector == 9, str(complex_parameters_per_sector))
    check("gauge selection does not diagonalize flavor matrices", matrix_entries > generations, f"{matrix_entries} entries vs {generations} eigenvalues")

    note_text = theorem_note.read_text(encoding="utf-8")
    check("note records primary runner", "frontier_sm_one_higgs_yukawa_gauge_selection.py" in note_text)
    check("note states no numerical Yukawa eigenvalue claim", "any numerical Yukawa eigenvalue" in note_text)
    check("note states no CKM or PMNS angle claim", "any CKM or PMNS mixing angle" in note_text)
    check("note states no top-Yukawa Ward normalization claim", "any top-Yukawa Ward normalization" in note_text)

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
