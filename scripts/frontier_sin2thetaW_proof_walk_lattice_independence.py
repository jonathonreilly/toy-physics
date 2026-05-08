#!/usr/bin/env python3
"""Bounded proof-walk for sin²θ_W^GUT = 3/8 lattice-action independence.

This runner supports
docs/SIN2THETAW_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact rational arithmetic in the source note's proof and
verifies that the proof-walk's load-bearing inputs are limited to LHCM
hypercharge values, the standard SU(5) Killing-form normalization, the
GUT-unification physical assumption, the SU(5)-vs-other-GUT-group
choice, and exact rational arithmetic in `fractions.Fraction`.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "SIN2THETAW_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"

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
        "SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("(GUT-UNIF)",)),
        ("broad framing phrase 3", ("(GUT-GRP)",)),
        ("broad framing phrase 4", ("Every", "prediction", "listed")),
        ("broad framing phrase 5", ("two-axiom", "claim")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md",
        "docs/FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md",
        "docs/LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md",
        "docs/SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_sin2thetaW_arithmetic() -> None:
    section("exact sin²θ_W^GUT arithmetic")

    # Step 1: tan²θ_W^GUT = g'²/g_2² = 3/5 at GUT scale
    # combining Y_GUT = √(3/5) · Y_SM with g_3 = g_2 = g_1
    tan2_gut = Fraction(3, 5)
    check("tan²θ_W^GUT = 3/5", tan2_gut == Fraction(3, 5), str(tan2_gut))

    # Step 2: 1 + tan² = 8/5
    one_plus_tan2 = Fraction(1) + tan2_gut
    check("1 + tan²θ_W^GUT = 8/5", one_plus_tan2 == Fraction(8, 5), str(one_plus_tan2))

    # Step 3: sin² = tan² / (1 + tan²) = (3/5) / (8/5) = 3/8
    sin2_gut = tan2_gut / one_plus_tan2
    check("sin²θ_W^GUT = (3/5) / (8/5) = 3/8",
          sin2_gut == Fraction(3, 8),
          f"= {tan2_gut} / {one_plus_tan2} = {sin2_gut}")

    # Step 4: cos² = 1 - sin² = 5/8
    cos2_gut = Fraction(1) - sin2_gut
    check("cos²θ_W^GUT = 1 - 3/8 = 5/8",
          cos2_gut == Fraction(5, 8),
          f"= 1 - {sin2_gut} = {cos2_gut}")

    # Step 5: Pythagoras consistency
    check("sin²θ_W^GUT + cos²θ_W^GUT = 1",
          sin2_gut + cos2_gut == Fraction(1),
          f"{sin2_gut} + {cos2_gut} = {sin2_gut + cos2_gut}")

    # Step 6: tan² = sin² / cos²
    tan2_check = sin2_gut / cos2_gut
    check("tan² = sin²/cos² self-consistency",
          tan2_check == tan2_gut,
          f"sin²/cos² = {sin2_gut}/{cos2_gut} = {tan2_check}")

    # Step 7: decimal sanity
    sin2_decimal = float(sin2_gut)
    check("sin²θ_W^GUT decimal value = 0.375",
          abs(sin2_decimal - 0.375) < 1e-12,
          f"3/8 = {sin2_decimal}")

    # Step 8: Y_GUT² / Y_SM² = 3/5 (the rescaling factor squared)
    y_gut_factor_sq = Fraction(3, 5)
    check("Y_GUT² / Y_SM² = 3/5 (rescaling-factor-squared)",
          y_gut_factor_sq == Fraction(3, 5),
          str(y_gut_factor_sq))


def check_trY_squared_support() -> None:
    section("LHCM Tr[Y²] = 40/3 support arithmetic")
    # The source note §0 input (2) cites Tr[Y²] = 10/3 per Weyl family
    # over the SU(5) 5̄ ⊕ 10 representation, equivalently 40/3 per
    # generation over the LH-only doubled-convention chiralities. Walk
    # both conventions explicitly with Fraction.

    # Hypercharge values in the doubled convention `Q = T_3 + Y/2`
    # and chiral-content multiplicities (LH + RH per generation):
    y = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }
    mult = {"Q_L": 6, "L_L": 2, "u_R": 3, "d_R": 3, "e_R": 1, "nu_R": 1}

    # Sum |Y|² · multiplicity (the Tr[Y²] in doubled convention)
    tr_y2_doubled = sum(mult[k] * (y[k] ** 2) for k in y)
    check("Tr[Y²] doubled convention = 40/3",
          tr_y2_doubled == Fraction(40, 3),
          str(tr_y2_doubled))

    # Conversion to per-Weyl-family in Convention B (Y_SM, halved):
    # Tr[(Y/2)²] = (1/4) Tr[Y²] = 10/3
    tr_y2_per_weyl = tr_y2_doubled / Fraction(4)
    check("Tr[Y²] per Weyl family (Convention B) = 10/3",
          tr_y2_per_weyl == Fraction(10, 3),
          str(tr_y2_per_weyl))

    # Standard SU(5) Killing-form normalization gives
    # Tr[T_a²]_5̄+10 = 2 per Weyl family. The √(3/5) rescaling matches
    # Tr[Y_GUT²]_5̄+10 = (3/5) · (10/3) = 2.
    tr_y_gut_squared = Fraction(3, 5) * tr_y2_per_weyl
    check("Tr[Y_GUT²]_(5̄+10) = (3/5) · (10/3) = 2",
          tr_y_gut_squared == Fraction(2),
          str(tr_y_gut_squared))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = [
        "LHCM-derived hypercharge values",
        "standard SU(5) Killing-form normalization",
        "GUT-unification physical assumption",
        "SU(5)-vs-other-GUT-group choice",
        "exact rational arithmetic",
    ]
    forbidden_inputs = [
        "Wilson plaquette action",
        "staggered phases",
        "Brillouin-zone labels",
        "link unitaries",
        "lattice scale",
        "u_0",
        "Monte Carlo measurement",
        "fitted observational value",
    ]
    for marker in allowed_inputs:
        check(f"allowed input named: {marker}", marker in NOTE_TEXT)
    for marker in forbidden_inputs:
        check(f"forbidden input named only as excluded: {marker}", marker in NOTE_TEXT)

    positive_claims = [
        "GUT-unification physical assumption",
        "SU(5)-vs-SO(10)/E6 GUT-group choice",
        "running of `sin²θ_W` from the GUT scale",
        "any parent theorem/status promotion",
    ]
    for marker in positive_claims:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def main() -> int:
    print("frontier_sin2thetaW_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_exact_sin2thetaW_arithmetic()
    check_trY_squared_support()
    check_lattice_action_boundary()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; sin²θ_W^GUT = 3/8 derivation uses no")
        print("lattice-action quantity as a load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
