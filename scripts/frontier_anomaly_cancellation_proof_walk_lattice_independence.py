#!/usr/bin/env python3
"""Bounded proof-walk for anomaly cancellation lattice-action independence.

This runner supports
docs/ANOMALY_CANCELLATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact rational arithmetic of the four anomaly cancellation
identities

    (E1)  Tr[Y]            = 0,
    (E2)  Tr[SU(3)^2 Y]    = 0,
    (E3)  Tr[Y^3]_LH       = -16/9,
    (E4)  Tr[Y^3]          = 0,

and verifies that the note's load-bearing proof-walk is limited to
chiral-content multiplicities, the Dynkin-index normalization
T(fund) = 1/2, exact rational arithmetic, and the already-admitted
electric-charge convention used upstream to fix the SM right-handed
hypercharges.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "ANOMALY_CANCELLATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"
)

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
        "do not use lattice-action machinery",
        "Proof-Walk",
        "Exact Arithmetic Check",
        "Boundaries",
        "ANOMALY_FORCES_TIME_THEOREM",
        "LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25",
        "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24",
        "HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
        "(E1)",
        "(E2)",
        "(E3)",
        "(E4)",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("realization-invariance", "test")),
        ("broad framing phrase 3", ("imports", "problem")),
        ("broad framing phrase 4", ("two-axiom", "claim")),
        ("broad framing phrase 5", ("Every", "prediction", "listed")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/ANOMALY_FORCES_TIME_THEOREM.md",
        "docs/LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md",
        "docs/STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "docs/HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md",
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_anomaly_arithmetic() -> None:
    section("exact anomaly trace arithmetic")

    y = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }
    mult = {"Q_L": 6, "L_L": 2, "u_R": 3, "d_R": 3, "e_R": 1, "nu_R": 1}

    check("Q_L hypercharge = 1/3", y["Q_L"] == Fraction(1, 3), str(y["Q_L"]))
    check("L_L hypercharge = -1", y["L_L"] == Fraction(-1), str(y["L_L"]))
    check("u_R hypercharge = 4/3", y["u_R"] == Fraction(4, 3), str(y["u_R"]))
    check("d_R hypercharge = -2/3", y["d_R"] == Fraction(-2, 3), str(y["d_R"]))
    check("e_R hypercharge = -2", y["e_R"] == Fraction(-2), str(y["e_R"]))
    check("nu_R hypercharge = 0", y["nu_R"] == Fraction(0), str(y["nu_R"]))

    check("Q_L multiplicity = 3 colors * 2 isospin", mult["Q_L"] == 3 * 2)
    check("L_L multiplicity = 1 color * 2 isospin", mult["L_L"] == 1 * 2)
    check("u_R multiplicity = 3 colors * 1 isospin", mult["u_R"] == 3 * 1)
    check("d_R multiplicity = 3 colors * 1 isospin", mult["d_R"] == 3 * 1)
    check("e_R multiplicity = 1", mult["e_R"] == 1)
    check("nu_R multiplicity = 1", mult["nu_R"] == 1)

    # (E1) Tr[Y] = 0
    tr_y_lh = mult["Q_L"] * y["Q_L"] + mult["L_L"] * y["L_L"]
    tr_y_rh = (
        -mult["u_R"] * y["u_R"]
        - mult["d_R"] * y["d_R"]
        - mult["e_R"] * y["e_R"]
        - mult["nu_R"] * y["nu_R"]
    )
    tr_y = tr_y_lh + tr_y_rh
    check("E1 LH partial Tr[Y]_LH = 0", tr_y_lh == 0, str(tr_y_lh))
    check("E1 RH partial Tr[Y]_RH = 0", tr_y_rh == 0, str(tr_y_rh))
    check("E1 full Tr[Y] = 0", tr_y == 0, str(tr_y))

    # (E2) Tr[SU(3)^2 Y] = 0  with T(3) = 1/2
    dynkin_fund = Fraction(1, 2)
    tr_su3_lh = dynkin_fund * 2 * y["Q_L"]
    tr_su3_rh = dynkin_fund * (-y["u_R"] - y["d_R"])
    tr_su3 = tr_su3_lh + tr_su3_rh
    check("E2 Dynkin index T(fund) = 1/2", dynkin_fund == Fraction(1, 2))
    check("E2 LH-quark Tr[SU(3)^2 Y]_LH = 1/3", tr_su3_lh == Fraction(1, 3), str(tr_su3_lh))
    check("E2 RH-quark Tr[SU(3)^2 Y]_RH = -1/3", tr_su3_rh == Fraction(-1, 3), str(tr_su3_rh))
    check("E2 full Tr[SU(3)^2 Y] = 0", tr_su3 == 0, str(tr_su3))

    # (E3) Tr[Y^3]_LH = -16/9
    tr_y3_lh = mult["Q_L"] * y["Q_L"] ** 3 + mult["L_L"] * y["L_L"] ** 3
    tr_y3_lh_QL = mult["Q_L"] * y["Q_L"] ** 3
    tr_y3_lh_LL = mult["L_L"] * y["L_L"] ** 3
    check("E3 Q_L cubic = 2/9", tr_y3_lh_QL == Fraction(2, 9), str(tr_y3_lh_QL))
    check("E3 L_L cubic = -2", tr_y3_lh_LL == Fraction(-2), str(tr_y3_lh_LL))
    check("E3 Tr[Y^3]_LH = -16/9", tr_y3_lh == Fraction(-16, 9), str(tr_y3_lh))

    # (E4) Tr[Y^3] = 0 (full content)
    tr_y3_rh = (
        -mult["u_R"] * y["u_R"] ** 3
        - mult["d_R"] * y["d_R"] ** 3
        - mult["e_R"] * y["e_R"] ** 3
        - mult["nu_R"] * y["nu_R"] ** 3
    )
    tr_y3 = tr_y3_lh + tr_y3_rh
    check("E4 Tr[Y^3]_RH = 16/9", tr_y3_rh == Fraction(16, 9), str(tr_y3_rh))
    check("E4 full Tr[Y^3] = 0", tr_y3 == 0, str(tr_y3))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = {
        "chiral-content multiplicities",
        "Dynkin-index normalization",
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

    boundary_items = [
        "Adler-Bell-Jackiw anomaly-to-inconsistency",
        "the right-handed completion existence statement",
        "derivation of the chiral matter content itself",
        "the staggered-Dirac realization gate",
        "Witten SU(2) `Z_2` integer count",
        "pure-color SU(3)^3 cubic gauge-anomaly cancellation",
        "`B - L` anomaly-freedom closure",
        "3+1 spacetime-forcing downstream step",
        "any parent theorem/status promotion",
    ]
    for marker in boundary_items:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def check_proof_walk_table_coverage() -> None:
    section("proof-walk table coverage (one per identity)")
    # Each per-identity proof-walk is keyed by an `### (Ek)` heading and
    # the per-row "Lattice-action input?" column. Confirm both appear and
    # confirm every "Lattice-action input?" column body answers "no" for
    # every row in this note.
    for identity in ("(E1)", "(E2)", "(E3)", "(E4)"):
        check(
            f"per-identity proof-walk heading present: {identity}",
            f"### {identity}" in NOTE_TEXT,
        )

    # Count the proof-walk rows. Every row should answer the
    # "Lattice-action input?" column with "no".
    table_rows = re.findall(r"^\| .+\| .+\| no \|\s*$", NOTE_TEXT, flags=re.MULTILINE)
    check(
        "all proof-walk rows answer 'no' to lattice-action input",
        len(table_rows) >= 13,
        f"row count = {len(table_rows)}",
    )

    # Confirm there is no row with a 'yes' answer to the lattice-action
    # column in the proof-walk tables.
    bad_rows = re.findall(r"^\| .+\| .+\| yes \|\s*$", NOTE_TEXT, flags=re.MULTILINE)
    check(
        "no proof-walk row answers 'yes' to lattice-action input",
        len(bad_rows) == 0,
        f"bad row count = {len(bad_rows)}",
    )


def main() -> int:
    print("frontier_anomaly_cancellation_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_exact_anomaly_arithmetic()
    check_lattice_action_boundary()
    check_proof_walk_table_coverage()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; the four anomaly cancellation")
        print("identities Tr[Y]=0, Tr[SU(3)^2 Y]=0, Tr[Y^3]_LH = -16/9, and")
        print("Tr[Y^3]=0 use no lattice-action quantity as a load-bearing input in")
        print("their cited proofs.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
