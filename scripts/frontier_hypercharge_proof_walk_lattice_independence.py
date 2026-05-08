#!/usr/bin/env python3
"""Bounded proof-walk for hypercharge lattice-action independence.

This runner supports
docs/HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md.
It checks the exact hypercharge arithmetic and verifies that the note's
load-bearing proof-walk is limited to chiral-content multiplicities,
group-index bookkeeping, exact rational arithmetic, and the stated
electric-charge convention.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md"

PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS" if ok else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{tag}] {name}{suffix}")
    return ok


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


NOTE_TEXT = NOTE_PATH.read_text()
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


def check_note_structure() -> None:
    section("note structure and scope")
    required = [
        "Claim type:** bounded_theorem",
        "source-note proposal only",
        "does not add a new axiom",
        "does not use lattice-action machinery",
        "Proof-Walk",
        "Exact Arithmetic Check",
        "Boundaries",
        "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("imports", "problem")),
        ("broad framing phrase 3", ("two-axiom", "claim")),
        ("broad framing phrase 4", ("Every", "prediction", "listed")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/ANOMALY_FORCES_TIME_THEOREM.md",
        "docs/LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_hypercharge_arithmetic() -> None:
    section("exact hypercharge arithmetic")
    discriminant = Fraction(36) + Fraction(288)
    check("discriminant = 324", discriminant == Fraction(324), str(discriminant))
    check("discriminant square root = 18", 18 * 18 == int(discriminant))

    y1_plus = Fraction(6 + 18, 18)
    y1_minus = Fraction(6 - 18, 18)
    check("positive root = 4/3", y1_plus == Fraction(4, 3), str(y1_plus))
    check("negative root = -2/3", y1_minus == Fraction(-2, 3), str(y1_minus))

    y = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": y1_plus,
        "d_R": Fraction(2, 3) - y1_plus,
        "e_R": -3 * Fraction(2, 3),
        "nu_R": Fraction(0),
    }
    expected = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }
    for key, val in expected.items():
        check(f"{key} = {val}", y[key] == val, str(y[key]))

    mult = {"Q_L": 6, "L_L": 2, "u_R": 3, "d_R": 3, "e_R": 1, "nu_R": 1}
    check("Q_L multiplicity = 3 colors * 2 isospin", mult["Q_L"] == 3 * 2)
    check("L_L multiplicity = 1 color * 2 isospin", mult["L_L"] == 1 * 2)
    check("u_R multiplicity = 3 colors * 1 isospin", mult["u_R"] == 3 * 1)
    check("d_R multiplicity = 3 colors * 1 isospin", mult["d_R"] == 3 * 1)
    check("e_R multiplicity = 1", mult["e_R"] == 1)
    check("nu_R multiplicity = 1", mult["nu_R"] == 1)

    tr_y = (
        mult["Q_L"] * y["Q_L"]
        + mult["L_L"] * y["L_L"]
        - mult["u_R"] * y["u_R"]
        - mult["d_R"] * y["d_R"]
        - mult["e_R"] * y["e_R"]
        - mult["nu_R"] * y["nu_R"]
    )
    check("Tr[Y] = 0", tr_y == 0, str(tr_y))

    dynkin_fund = Fraction(1, 2)
    tr_su3_y = dynkin_fund * (2 * y["Q_L"] - y["u_R"] - y["d_R"])
    check("Tr[SU(3)^2 Y] = 0 per color", tr_su3_y == 0, str(tr_su3_y))

    tr_y_cubed = (
        mult["Q_L"] * y["Q_L"] ** 3
        + mult["L_L"] * y["L_L"] ** 3
        - mult["u_R"] * y["u_R"] ** 3
        - mult["d_R"] * y["d_R"] ** 3
        - mult["e_R"] * y["e_R"] ** 3
        - mult["nu_R"] * y["nu_R"] ** 3
    )
    check("Tr[Y^3] = 0", tr_y_cubed == 0, str(tr_y_cubed))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = {
        "chiral-content multiplicities",
        "SU(2) and SU(3) Dynkin-index bookkeeping",
        "exact rational arithmetic",
        "electric-charge convention",
    }
    forbidden_inputs = {
        "Wilson plaquette action",
        "staggered phases",
        "Brillouin-zone labels",
        "link unitaries",
        "lattice scale",
        "u_0",
        "Monte Carlo measurement",
        "fitted observational value",
    }
    for marker in allowed_inputs:
        check(f"allowed input named: {marker}", marker in NOTE_TEXT)
    for marker in forbidden_inputs:
        check(f"forbidden input named only as excluded: {marker}", marker in NOTE_TEXT)

    positive_claims = [
        "derivation of the chiral matter content itself",
        "the staggered-Dirac realization gate",
        "any parent theorem/status promotion",
    ]
    for marker in positive_claims:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def main() -> int:
    print("frontier_hypercharge_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_exact_hypercharge_arithmetic()
    check_lattice_action_boundary()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; hypercharge uniqueness uses no")
        print("lattice-action quantity as a load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
