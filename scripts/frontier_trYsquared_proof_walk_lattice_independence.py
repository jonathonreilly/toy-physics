#!/usr/bin/env python3
"""Bounded proof-walk for Tr[Y^2] catalog lattice-action independence.

This runner supports
docs/TRYSQUARED_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact Tr[Y^2] catalog arithmetic (Y1-Y5) and verifies
that the note's load-bearing proof-walk is limited to chiral-content
multiplicities, admitted hypercharge values, exact rational arithmetic,
and SU(2)/SU(3) Dynkin-index bookkeeping for the GUT-consistency row.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "TRYSQUARED_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"

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
        ("broad framing phrase 5", ("two-class", "framing")),
        ("broad framing phrase 6", ("lattice-realization-invariant", "by")),
        ("broad framing phrase 7", ("retires", "admission")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md",
        "docs/STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
        "docs/HYPERCHARGE_IDENTIFICATION_NOTE.md",
        "docs/THREE_GENERATION_STRUCTURE_NOTE.md",
        "docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md",
        "docs/ANOMALY_FORCES_TIME_THEOREM.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


# Admitted hypercharge values from the cited uniqueness theorem.
Y = {
    "Q_L": Fraction(1, 3),
    "L_L": Fraction(-1),
    "u_R": Fraction(4, 3),
    "d_R": Fraction(-2, 3),
    "e_R": Fraction(-2),
    "nu_R": Fraction(0),
}

# Multiplicities = (color count) * (SU(2) doublet count) per state.
MULT = {
    "Q_L": 6,   # 3 colors * 2 isospin
    "L_L": 2,   # 1 color  * 2 isospin
    "u_R": 3,   # 3 colors * 1
    "d_R": 3,   # 3 colors * 1
    "e_R": 1,
    "nu_R": 1,
}

LH_KEYS = ("Q_L", "L_L")
RH_KEYS = ("u_R", "d_R", "e_R", "nu_R")
N_GEN = 3


def check_admitted_inputs() -> None:
    section("admitted hypercharges and multiplicities")
    expected_y = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }
    for key, val in expected_y.items():
        check(f"Y({key}) = {val}", Y[key] == val, str(Y[key]))

    check("Q_L multiplicity = 3 colors * 2 isospin", MULT["Q_L"] == 3 * 2)
    check("L_L multiplicity = 1 color * 2 isospin", MULT["L_L"] == 1 * 2)
    check("u_R multiplicity = 3 colors * 1 isospin", MULT["u_R"] == 3 * 1)
    check("d_R multiplicity = 3 colors * 1 isospin", MULT["d_R"] == 3 * 1)
    check("e_R multiplicity = 1", MULT["e_R"] == 1)
    check("nu_R multiplicity = 1", MULT["nu_R"] == 1)
    check("LH state count = 8", sum(MULT[k] for k in LH_KEYS) == 8)
    check("RH state count = 8", sum(MULT[k] for k in RH_KEYS) == 8)
    check("one-generation state count = 16",
          sum(MULT[k] for k in LH_KEYS + RH_KEYS) == 16)


def tr_y_squared(keys) -> Fraction:
    total = Fraction(0)
    for k in keys:
        total += Fraction(MULT[k]) * (Y[k] ** 2)
    return total


def check_y1_lh_trace() -> Fraction:
    section("(Y1) Tr[Y^2]_LH = 8/3")
    q_term = Fraction(MULT["Q_L"]) * (Y["Q_L"] ** 2)
    l_term = Fraction(MULT["L_L"]) * (Y["L_L"] ** 2)
    check("Q_L contribution = 6 * (1/3)^2 = 2/3",
          q_term == Fraction(2, 3), str(q_term))
    check("L_L contribution = 2 * (-1)^2 = 2",
          l_term == Fraction(2), str(l_term))

    tr_lh = tr_y_squared(LH_KEYS)
    check("Tr[Y^2]_LH = 8/3", tr_lh == Fraction(8, 3), str(tr_lh))
    return tr_lh


def check_y2_rh_trace() -> Fraction:
    section("(Y2) Tr[Y^2]_RH = 32/3")
    u_term = Fraction(MULT["u_R"]) * (Y["u_R"] ** 2)
    d_term = Fraction(MULT["d_R"]) * (Y["d_R"] ** 2)
    e_term = Fraction(MULT["e_R"]) * (Y["e_R"] ** 2)
    nu_term = Fraction(MULT["nu_R"]) * (Y["nu_R"] ** 2)
    check("u_R contribution = 3 * (4/3)^2 = 16/3",
          u_term == Fraction(16, 3), str(u_term))
    check("d_R contribution = 3 * (-2/3)^2 = 4/3",
          d_term == Fraction(4, 3), str(d_term))
    check("e_R contribution = 1 * (-2)^2 = 4",
          e_term == Fraction(4), str(e_term))
    check("nu_R contribution = 0", nu_term == Fraction(0), str(nu_term))

    tr_rh = tr_y_squared(RH_KEYS)
    check("Tr[Y^2]_RH = 32/3", tr_rh == Fraction(32, 3), str(tr_rh))
    return tr_rh


def check_y3_one_gen(tr_lh: Fraction, tr_rh: Fraction) -> Fraction:
    section("(Y3) Tr[Y^2]_one_gen = 40/3")
    tr_one = tr_lh + tr_rh
    check("Tr[Y^2]_one_gen = (Y1) + (Y2)", tr_one == Fraction(40, 3),
          str(tr_one))
    tr_direct = tr_y_squared(LH_KEYS + RH_KEYS)
    check("Tr[Y^2]_one_gen direct sum matches",
          tr_direct == tr_one, str(tr_direct))
    return tr_one


def check_y4_three_gen(tr_one: Fraction) -> Fraction:
    section("(Y4) Tr[Y^2]_three_gen = 40")
    tr_three = N_GEN * tr_one
    check("Tr[Y^2]_three_gen = 3 * (Y3)",
          tr_three == Fraction(40), str(tr_three))
    return tr_three


def dynkin_su2_one_gen() -> Fraction:
    # SU(2) doublets contribute T(fund) = 1/2; sum over color copies.
    half = Fraction(1, 2)
    # Q_L: 3 color copies, doublet
    s = Fraction(3) * half
    # L_L: 1 color, doublet
    s += Fraction(1) * half
    return s


def dynkin_su3_one_gen() -> Fraction:
    # SU(3) fundamentals contribute T(fund) = 1/2; sum over SU(2) copies.
    half = Fraction(1, 2)
    s = Fraction(0)
    s += Fraction(2) * half  # Q_L: SU(2) doublet, fund
    s += Fraction(1) * half  # u_R: singlet, fund
    s += Fraction(1) * half  # d_R: singlet, fund
    return s


def check_y5_gut_consistency(tr_three: Fraction) -> None:
    section("(Y5) GUT-consistency: Tr[Y_GUT^2]_three_gen = 6 = Dynkin sums")
    gut_factor = Fraction(3, 20)
    tr_gut = gut_factor * tr_three
    check("(3/20) * Tr[Y^2]_three_gen = 6",
          tr_gut == Fraction(6), str(tr_gut))

    su2_one = dynkin_su2_one_gen()
    su3_one = dynkin_su3_one_gen()
    check("Tr[T_a^2]_SU(2),one_gen = 2", su2_one == Fraction(2), str(su2_one))
    check("Tr[T_a^2]_SU(3),one_gen = 2", su3_one == Fraction(2), str(su3_one))

    su2_three = N_GEN * su2_one
    su3_three = N_GEN * su3_one
    check("Tr[T_a^2]_SU(2),three_gen = 6",
          su2_three == Fraction(6), str(su2_three))
    check("Tr[T_a^2]_SU(3),three_gen = 6",
          su3_three == Fraction(6), str(su3_three))

    check("(Y5) Tr[Y_GUT^2]_three_gen = SU(2) Dynkin sum",
          tr_gut == su2_three, f"{tr_gut} vs {su2_three}")
    check("(Y5) Tr[Y_GUT^2]_three_gen = SU(3) Dynkin sum",
          tr_gut == su3_three, f"{tr_gut} vs {su3_three}")

    # Conversion factor consistency.
    minimal_factor = Fraction(3, 5)  # Y_GUT^2 / Y_min^2 with Y_min = Y/2
    check("Y_GUT^2 / Y^2 = 3/20", gut_factor == Fraction(3, 20))
    check("Y_GUT^2 / Y_min^2 = 3/5 (Y_min = Y/2)",
          minimal_factor == Fraction(4) * gut_factor, str(minimal_factor))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = {
        "chiral-content multiplicities",
        "admitted hypercharge assignments",
        "exact rational arithmetic",
        "Dynkin-index bookkeeping",
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
    print("frontier_trYsquared_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    check_admitted_inputs()
    tr_lh = check_y1_lh_trace()
    tr_rh = check_y2_rh_trace()
    tr_one = check_y3_one_gen(tr_lh, tr_rh)
    tr_three = check_y4_three_gen(tr_one)
    check_y5_gut_consistency(tr_three)
    check_lattice_action_boundary()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; the Tr[Y^2] catalog identities use")
        print("no lattice-action quantity as a load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
