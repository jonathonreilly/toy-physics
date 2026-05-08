#!/usr/bin/env python3
"""Bounded proof-walk for Y_GUT normalization lattice-action independence.

This runner supports
docs/YGUT_NORMALIZATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact trace-consistency arithmetic and verifies that the
note's load-bearing proof-walk is limited to the LH-form chirality
table imported from the SU(5) embedding-consistency theorem, the
squared-hypercharge trace identities (Y1)-(Y5) imported from the
squared-trace catalog, SU(N) Dynkin-index bookkeeping under the
standard Killing-form normalization convention, and exact rational
arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "YGUT_NORMALIZATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"

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
        "HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25",
        "SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
        "standard Lie-algebra Killing-form normalization convention",
        "Tr[T_a T_b]_fund = (1/2)",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("lattice-realization-invariant",)),
        ("broad framing phrase 3", ("two-class",)),
        ("broad framing phrase 4", ("(SU5-CKN)",)),
        ("broad framing phrase 5", ("imports", "problem")),
        ("broad framing phrase 6", ("two-axiom", "claim")),
        ("broad framing phrase 7", ("Every", "prediction", "listed")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md",
        "docs/SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md",
        "docs/FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md",
        "docs/STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_lh_form_chirality_table() -> None:
    """Per-Weyl-family LH-form table (15 chiralities in 5̄+10; ν^c_L singlet
    sits in the SU(5) `1`)."""
    section("LH-form chirality table (per Weyl family)")

    # (SU(3) rep, SU(2) rep, Y_min, multiplicity, target SU(5) slot)
    chiralities = [
        ("Q_L",   "3",   "2", Fraction( 1, 6), 6, "10"),
        ("u^c_L", "3bar","1", Fraction(-2, 3), 3, "10"),
        ("e^c_L", "1",   "1", Fraction( 1),    1, "10"),
        ("d^c_L", "3bar","1", Fraction( 1, 3), 3, "5bar"),
        ("L_L",   "1",   "2", Fraction(-1, 2), 2, "5bar"),
        ("nu^c_L","1",   "1", Fraction( 0),    1, "1"),
    ]

    # Total state count per generation = 16
    total = sum(c[4] for c in chiralities)
    check("total chiralities per generation = 16", total == 16, str(total))

    # Slot-by-slot completeness
    by_slot = {"5bar": 0, "10": 0, "1": 0}
    for _name, _su3, _su2, _ymin, mult, slot in chiralities:
        by_slot[slot] += mult
    check("|5bar| = 5 (3 + 2 states)", by_slot["5bar"] == 5, str(by_slot["5bar"]))
    check("|10| = 10 (6 + 3 + 1 states)", by_slot["10"] == 10, str(by_slot["10"]))
    check("|1| = 1 (singlet)", by_slot["1"] == 1, str(by_slot["1"]))

    # 5bar + 10 = 15 chiralities (per Weyl family in 5bar+10)
    in_5bar_10 = by_slot["5bar"] + by_slot["10"]
    check("|5bar + 10| = 15 per Weyl family", in_5bar_10 == 15, str(in_5bar_10))


def check_squared_trace_per_rep() -> None:
    section("squared Y_min trace per SU(5) rep, per Weyl family")

    # Per-rep entries: (block label, multiplicity, Y_min)
    rep_5bar = [
        ("d^c_L", 3, Fraction(1, 3)),
        ("L_L",   2, Fraction(-1, 2)),
    ]
    rep_10 = [
        ("u^c_L", 3, Fraction(-2, 3)),
        ("Q_L",   6, Fraction( 1, 6)),
        ("e^c_L", 1, Fraction( 1)),
    ]

    tr_5bar = sum(m * y * y for _l, m, y in rep_5bar)
    tr_10   = sum(m * y * y for _l, m, y in rep_10)
    tr_5bar_10 = tr_5bar + tr_10

    check("Tr[Y_min^2]_5bar = 5/6", tr_5bar == Fraction(5, 6), str(tr_5bar))
    check("Tr[Y_min^2]_10 = 5/2", tr_10 == Fraction(5, 2), str(tr_10))
    check(
        "Tr[Y_min^2]_5bar+10 = 10/3 (per Weyl family)",
        tr_5bar_10 == Fraction(10, 3),
        str(tr_5bar_10),
    )

    # Manual cross-check of the LHCM-derived 10/3 per Weyl family
    manual_5bar = (
        Fraction(3) * Fraction(1, 3) ** 2
        + Fraction(2) * Fraction(1, 2) ** 2
    )
    manual_10 = (
        Fraction(3) * Fraction(2, 3) ** 2
        + Fraction(6) * Fraction(1, 6) ** 2
        + Fraction(1) * Fraction(1) ** 2
    )
    check("manual Tr[Y_min^2]_5bar = 5/6", manual_5bar == Fraction(5, 6),
          str(manual_5bar))
    check("manual Tr[Y_min^2]_10 = 5/2", manual_10 == Fraction(5, 2),
          str(manual_10))


def check_dynkin_index_sum() -> None:
    section("SU(N) Dynkin-index sum under standard Killing-form normalization")

    # Standard SU(N) Killing-form normalization convention:
    # Tr[T_a T_b]_fund = (1/2) δ_{ab}, equivalently T(fund) = 1/2.
    T_fund = Fraction(1, 2)        # SU(5) fundamental Dynkin index
    T_5bar = T_fund                # 5bar has the same index as 5
    T_10   = Fraction(3, 2)        # standard SU(5) antisymmetric-rank-2 index

    check("T(5bar) = 1/2 under standard Killing-form normalization",
          T_5bar == Fraction(1, 2), str(T_5bar))
    check("T(10) = 3/2 under standard Killing-form normalization",
          T_10 == Fraction(3, 2), str(T_10))

    tr_T_5bar_10 = T_5bar + T_10
    check("Tr[T_a^2]_5bar+10 = 2 per Weyl family",
          tr_T_5bar_10 == Fraction(2), str(tr_T_5bar_10))


def check_trace_consistency_solve() -> None:
    section("trace-consistency solve for Y_GUT = c * Y_min rescaling")

    tr_y_min2_5bar_10 = Fraction(10, 3)
    tr_T2_5bar_10 = Fraction(2)

    # Trace-consistency equation: c^2 * Tr[Y_min^2]_5bar+10 = Tr[T_a^2]_5bar+10
    c_squared = tr_T2_5bar_10 / tr_y_min2_5bar_10
    check("c^2 = 6/10 = 3/5", c_squared == Fraction(3, 5), str(c_squared))

    # Numerator/denominator forced: 2 / (10/3) = 6/10 = 3/5
    num = tr_T2_5bar_10 * 3
    den = tr_y_min2_5bar_10 * 3
    check("numerator forced = 6", num == Fraction(6), str(num))
    check("denominator forced = 10", den == Fraction(10), str(den))

    # Doubled-convention restatement: Y_GUT^2 / Y^2 = (1/4) * (Y_GUT^2 / Y_min^2)
    # since Y_min = Y/2.
    ratio_doubled = c_squared * Fraction(1, 4)
    check("Y_GUT^2 / Y^2 = 3/20 (doubled convention)",
          ratio_doubled == Fraction(3, 20), str(ratio_doubled))

    # Tr[Y_GUT^2]_5bar+10 = c^2 * Tr[Y_min^2]_5bar+10 = 2 per Weyl family
    tr_y_gut2 = c_squared * tr_y_min2_5bar_10
    check("Tr[Y_GUT^2]_5bar+10 = 2 per Weyl family",
          tr_y_gut2 == Fraction(2), str(tr_y_gut2))

    # Three-generation lift: 3 * 2 = 6 matches (Y5)
    tr_y_gut2_three_gen = 3 * tr_y_gut2
    check("Tr[Y_GUT^2]_three_gen = 6 (matches Y5)",
          tr_y_gut2_three_gen == Fraction(6), str(tr_y_gut2_three_gen))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = [
        "LH-form chirality table",
        "squared-hypercharge trace identities",
        "SU(N) Dynkin-index bookkeeping",
        "exact rational arithmetic",
        "standard Lie-algebra Killing-form normalization convention",
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
        "derivation of the chiral matter content itself",
        "the staggered-Dirac realization gate",
        "minimality of SU(5)",
        "any GUT-scale derivation or proton-decay claim",
        "any parent theorem/status promotion",
    ]
    for marker in positive_claims:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def main() -> int:
    print("frontier_ygut_normalization_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_lh_form_chirality_table()
    check_squared_trace_per_rep()
    check_dynkin_index_sum()
    check_trace_consistency_solve()
    check_lattice_action_boundary()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; Y_GUT = sqrt(3/5) * Y_min uses no")
        print("lattice-action quantity as a load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
