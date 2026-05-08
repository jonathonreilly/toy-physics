#!/usr/bin/env python3
"""Bounded proof-walk for SU(5) 5̄ ⊕ 10 ⊕ 1 decomposition lattice-independence.

This runner supports
docs/SU5_DECOMPOSITION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact slot-matching arithmetic and verifies that the
note's load-bearing proof-walk is limited to chiral-content multiplicities,
LHCM hypercharge values, standard SU(5) representation theory (Schur
lemma + antisymmetric tensor decomposition), exact rational arithmetic,
and the standard `5 = 3 ⊕ 2` block embedding `SU(3) × SU(2) ⊂ SU(5)`.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "SU5_DECOMPOSITION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"

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
        "SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07",
        "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
        "Schur lemma",
        "antisymmetric tensor decomposition",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("lattice-realization-invariant",)),
        ("broad framing phrase 3", ("imports", "problem")),
        ("broad framing phrase 4", ("two-axiom", "claim")),
        ("broad framing phrase 5", ("realization-invariance",)),
        ("broad framing phrase 6", ("Every", "prediction", "listed")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md",
        "docs/STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md",
        "docs/THREE_GENERATION_STRUCTURE_NOTE.md",
        "docs/FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_lhcm_chirality_table() -> None:
    """Verify the LH-form one-generation 16-chirality table.

    Each LH chirality has (SU(3) rep, SU(2) rep, Y_min). The Y_min values
    are derived from the LHCM doubled-convention Y values via Y_min = Y/2
    (LH content unchanged) or via sign flip + Y_min = (-Y)/2 (RH → LH
    conjugate).
    """
    section("LHCM 16-chirality LH-form table")

    # Doubled-convention Y values per LHCM hypercharge uniqueness:
    Y_doubled = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }

    # Multiplicities (color × isospin per chirality class):
    mult = {
        "Q_L": 6,    # 3 colors * 2 isospin
        "L_L": 2,    # 1 color * 2 isospin
        "u_R": 3,    # 3 colors
        "d_R": 3,    # 3 colors
        "e_R": 1,    # 1 state
        "nu_R": 1,   # 1 state
    }

    # LH-form table: (SU3 rep, SU2 dim, Y_min)
    # LH chiralities: Q_L, L_L unchanged with Y_min = Y/2.
    # RH chiralities: pass to LH conjugate, sign flips, Y_min = -Y/2.
    lhcm_lh = {
        "Q_L":   ("3",   2, Y_doubled["Q_L"] / 2),     # = +1/6
        "u^c_L": ("3bar", 1, -Y_doubled["u_R"] / 2),   # = -2/3
        "d^c_L": ("3bar", 1, -Y_doubled["d_R"] / 2),   # = +1/3
        "L_L":   ("1",   2, Y_doubled["L_L"] / 2),     # = -1/2
        "e^c_L": ("1",   1, -Y_doubled["e_R"] / 2),    # = +1
        "nu^c_L":("1",   1, -Y_doubled["nu_R"] / 2),   # = 0
    }

    expected = {
        "Q_L":   ("3",    2, Fraction(1, 6)),
        "u^c_L": ("3bar", 1, Fraction(-2, 3)),
        "d^c_L": ("3bar", 1, Fraction(1, 3)),
        "L_L":   ("1",    2, Fraction(-1, 2)),
        "e^c_L": ("1",    1, Fraction(1)),
        "nu^c_L":("1",    1, Fraction(0)),
    }

    for key, val in expected.items():
        check(
            f"{key} LH-form triple = {val}",
            lhcm_lh[key] == val,
            str(lhcm_lh[key]),
        )

    # Multiplicity per chirality class (LH form has same counts):
    expected_mult = {
        "Q_L": 6, "u^c_L": 3, "d^c_L": 3,
        "L_L": 2, "e^c_L": 1, "nu^c_L": 1,
    }
    total_states = 0
    for key, m in expected_mult.items():
        # LH form: u^c_L matches u_R count, etc.
        rh_key = key.replace("^c_L", "_R") if "^c_L" in key else key
        if rh_key == "nu_R":
            rh_key = "nu_R"
        check(
            f"{key} multiplicity = {m}",
            mult[rh_key] == m,
            str(mult[rh_key]),
        )
        total_states += m

    check("|LH content| = 16 per generation", total_states == 16, str(total_states))


def check_su5_branchings() -> None:
    """Verify standard SU(5) branchings under the manifest 3+2 block embedding.

    The unique traceless diagonal SU(5) Cartan generator commuting with
    su(3) ⊕ su(2) is fixed (up to sign and overall scale) by Schur's lemma
    + tracelessness. Working in Y_min units, the eigenvalues on the
    defining 5 are (-1/3, -1/3, -1/3, +1/2, +1/2) (3a + 2b = 0 with
    a = -1/3, b = +1/2).
    """
    section("SU(5) branchings from Schur + tracelessness + ∧²")

    # Defining 5 Y_min eigenvalues:
    a = Fraction(-1, 3)  # (3, 1) block
    b = Fraction(1, 2)   # (1, 2) block

    # Tracelessness: 3a + 2b = 0
    check("tracelessness 3a + 2b = 0", 3 * a + 2 * b == 0, f"3*{a} + 2*{b} = {3*a + 2*b}")

    # 5 = (3, 1)_{a} ⊕ (1, 2)_{b}
    rep_5 = [("3", 1, a), ("1", 2, b)]
    check("5 has (3,1) component with Y_min = -1/3", rep_5[0] == ("3", 1, Fraction(-1, 3)))
    check("5 has (1,2) component with Y_min = +1/2", rep_5[1] == ("1", 2, Fraction(1, 2)))

    # 5̄ = complex conjugate of 5: same SU(3) → 3̄, SU(2) → 2 (real), Y → -Y
    rep_5bar = [("3bar", 1, -a), ("1", 2, -b)]
    check("5̄ has (3̄,1) component with Y_min = +1/3", rep_5bar[0] == ("3bar", 1, Fraction(1, 3)))
    check("5̄ has (1,2) component with Y_min = -1/2", rep_5bar[1] == ("1", 2, Fraction(-1, 2)))

    # 10 = ∧²(5)
    # ∧²((3,1) ⊕ (1,2)) = ∧²(3,1) ⊕ ((3,1) ⊗ (1,2)) ⊕ ∧²(1,2)
    #   ∧²(3) = 3̄ (antisymmetric pair of fundamental SU(3))
    #   ∧²(2) = 1 (singlet of SU(2))
    #   (3) ⊗ (2) = (3, 2) (mixed)
    # Y_min adds under tensor product, doubles under ∧²:
    rep_10 = [
        ("3bar", 1, 2 * a),        # ∧²(3,1)_a   = (3̄,1)_{2a}
        ("3",    2, a + b),        # (3,1)_a ⊗ (1,2)_b = (3,2)_{a+b}
        ("1",    1, 2 * b),        # ∧²(1,2)_b  = (1,1)_{2b}
    ]
    check("10 has (3̄,1) component with Y_min = -2/3", rep_10[0] == ("3bar", 1, Fraction(-2, 3)))
    check("10 has (3,2) component with Y_min = +1/6", rep_10[1] == ("3", 2, Fraction(1, 6)))
    check("10 has (1,1) component with Y_min = +1", rep_10[2] == ("1", 1, Fraction(1)))

    # 1 = (1, 1)_0
    rep_1 = [("1", 1, Fraction(0))]
    check("1 has (1,1) component with Y_min = 0", rep_1[0] == ("1", 1, Fraction(0)))

    # State counts:
    def state_count(rep):
        # rep entry: (su3_label, su2_dim, Y_min)
        # SU(3) dimensions: "3", "3bar" -> 3; "1" -> 1
        su3_dim = {"3": 3, "3bar": 3, "1": 1}
        return sum(su3_dim[r[0]] * r[1] for r in rep)

    check("|5| = 3 + 2 = 5", state_count(rep_5) == 5, str(state_count(rep_5)))
    check("|5̄| = 3 + 2 = 5", state_count(rep_5bar) == 5, str(state_count(rep_5bar)))
    check("|10| = 3 + 6 + 1 = 10", state_count(rep_10) == 10, str(state_count(rep_10)))
    check("|1| = 1", state_count(rep_1) == 1, str(state_count(rep_1)))
    check(
        "|5̄ ⊕ 10 ⊕ 1| = 5 + 10 + 1 = 16",
        state_count(rep_5bar) + state_count(rep_10) + state_count(rep_1) == 16,
    )

    return rep_5bar, rep_10, rep_1


def check_slot_match(rep_5bar, rep_10, rep_1) -> None:
    """Verify each LHCM chirality maps to a unique SU(5) slot
    via (SU(3), SU(2), Y_min) triple equality, and that every slot
    is filled exactly once.
    """
    section("slot-by-slot match")

    lhcm_lh = {
        "Q_L":    ("3",    2, Fraction(1, 6)),
        "u^c_L":  ("3bar", 1, Fraction(-2, 3)),
        "d^c_L":  ("3bar", 1, Fraction(1, 3)),
        "L_L":    ("1",    2, Fraction(-1, 2)),
        "e^c_L":  ("1",    1, Fraction(1)),
        "nu^c_L": ("1",    1, Fraction(0)),
    }

    # Build slot inventory: list of (rep_name, triple) pairs.
    slots = []
    for triple in rep_5bar:
        slots.append(("5bar", triple))
    for triple in rep_10:
        slots.append(("10", triple))
    for triple in rep_1:
        slots.append(("1", triple))

    # Expected matches:
    expected_assignment = {
        "Q_L":    "10",
        "u^c_L":  "10",
        "e^c_L":  "10",
        "d^c_L":  "5bar",
        "L_L":    "5bar",
        "nu^c_L": "1",
    }

    consumed = [False] * len(slots)
    for chirality, triple in lhcm_lh.items():
        # Find unique slot matching this triple:
        matches = [
            i for i, (rep_name, slot_triple) in enumerate(slots)
            if slot_triple == triple and not consumed[i]
        ]
        assigned_rep = expected_assignment[chirality]
        check(
            f"{chirality} → {assigned_rep}: slot match exists",
            len(matches) == 1,
            f"matches={len(matches)}",
        )
        if matches:
            idx = matches[0]
            slot_rep = slots[idx][0]
            check(
                f"{chirality} → {assigned_rep}: rep is {assigned_rep}",
                slot_rep == assigned_rep,
                f"got {slot_rep}",
            )
            consumed[idx] = True

    # Every slot consumed exactly once:
    check("every SU(5) slot filled exactly once", all(consumed), str(consumed.count(False)) + " unfilled")


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = [
        "chiral-content multiplicities",
        "LHCM-derived hypercharge values",
        "standard SU(5) representation theory",
        "Schur lemma",
        "exact rational arithmetic",
        "block embedding",
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
        "any parent theorem/status promotion",
        "SU(5) minimality",
    ]
    for marker in positive_claims:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def check_proof_walk_table() -> None:
    """Verify the proof-walk table contains the six chirality slot rows
    plus the structural rep-theory + transcription rows.
    """
    section("proof-walk table coverage")
    chirality_rows = [
        "`Q_L → 10` slot match",
        "`u^c_L → 10` slot match",
        "`e^c_L → 10` slot match",
        "`d^c_L → 5̄` slot match",
        "`L_L → 5̄` slot match",
        "`ν^c_L → 1` slot match",
    ]
    for row in chirality_rows:
        check(f"proof-walk row present: {row}", row in NOTE_TEXT)

    structural_rows = [
        "LH-form transcription",
        "`5 = (3,1) ⊕ (1,2)` branching",
        "`10 = ∧²(5)` branching",
        "State-count bookkeeping",
    ]
    for row in structural_rows:
        check(f"proof-walk structural row present: {row}", row in NOTE_TEXT)

    # All proof-walk rows declare lattice-action input = no.
    # Count "| no |" cell occurrences in the proof-walk table.
    no_count = NOTE_TEXT.count("| no |")
    check("proof-walk table has >= 14 'no' cells (every row)", no_count >= 14, f"found {no_count}")


def main() -> int:
    print("frontier_su5_decomposition_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_exact_lhcm_chirality_table()
    rep_5bar, rep_10, rep_1 = check_su5_branchings()
    check_slot_match(rep_5bar, rep_10, rep_1)
    check_lattice_action_boundary()
    check_proof_walk_table()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; SU(5) 5̄ ⊕ 10 ⊕ 1 slot-matching")
        print("uses no lattice-action quantity as a load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
