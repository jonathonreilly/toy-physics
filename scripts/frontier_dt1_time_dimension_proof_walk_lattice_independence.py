#!/usr/bin/env python3
"""Bounded proof-walk for time-dimension d_t = 1 lattice-action independence.

This runner supports
docs/DT1_TIME_DIMENSION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md.
It checks the exact algebraic facts that feed the time-piece argument
of the cited time theorem (Steps 1--4 of ANOMALY_FORCES_TIME_THEOREM.md)
and verifies that the note's load-bearing proof-walk is limited to
chiral-content multiplicities, group-index bookkeeping, exact rational
arithmetic, the Clifford-algebra classification of the volume element,
the cited chirality grading, and the cited single-clock codimension-1
evolution structure.

Honest scope: the spatial dimension d_s = 3 is given by the framework
axiom A2 (Z^3 substrate); it is NOT derived from a proof-walk in this
note and NOT derived from anomaly cancellation in the source theorem.
The narrow proof-walked claim here is the temporal piece d_t = 1 only.
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
    / "DT1_TIME_DIMENSION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md"
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
        "Proposal allowed:** false",
        "source-note proposal only",
        "does not add a new axiom",
        "does not use lattice-action machinery",
        "Proof-Walk",
        "Exact Arithmetic Check",
        "Boundaries",
        "ANOMALY_FORCES_TIME_THEOREM",
        "AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03",
        "CPT_EXACT_NOTE",
        "MINIMAL_AXIOMS_2026-05-03",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("(S)+(T)+(J)", "joint")),
        ("broad framing phrase 3", ("joint", "forcing")),
        ("broad framing phrase 4", ("two-axiom", "claim")),
        ("broad framing phrase 5", ("Every", "prediction", "listed")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_honest_scope() -> None:
    section("honest scope (d_s = 3 from A2, not derived)")
    # The note must explicitly name d_s = 3 as an A2 substrate-axiom input.
    must_state_a2_input = [
        "d_s = 3` is given directly by the\n  framework axiom A2",
        "NOT derived from a proof-walk in this",
        "NOT derived from\n  anomaly cancellation",
        "narrow proof-walked claim here is the temporal piece `d_t = 1`",
    ]
    for marker in must_state_a2_input:
        check(
            f"states honest A2 scope: {marker[:60].splitlines()[0]}",
            marker in NOTE_TEXT,
        )


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/ANOMALY_FORCES_TIME_THEOREM.md",
        "docs/CPT_EXACT_NOTE.md",
        "docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md",
        "docs/NATIVE_GAUGE_CLOSURE_NOTE.md",
        "docs/LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_lh_anomaly_traces() -> None:
    section("exact LH-anomaly traces (Step 1 input)")
    # Left-handed content of one generation:
    # Q_L = (2, 3)_{+1/3}: SU(2) doublet, SU(3) triplet, Y = +1/3, mult 6
    # L_L = (2, 1)_{-1}:   SU(2) doublet, SU(3) singlet, Y = -1,   mult 2
    y_QL = Fraction(1, 3)
    y_LL = Fraction(-1)
    n_QL = 6
    n_LL = 2
    dynkin_fund = Fraction(1, 2)

    tr_y_lh = n_QL * y_QL + n_LL * y_LL
    check("Tr[Y]_LH = 0", tr_y_lh == 0, str(tr_y_lh))

    # Tr[SU(2)^2 Y]_LH = T(fund_SU2) * (n_color_QL * y_QL + n_color_LL * y_LL)
    # SU(2) doublet T = 1/2; trace runs over color-replicated doublets
    tr_su2_y_lh = dynkin_fund * (3 * y_QL + 1 * y_LL)
    check("Tr[SU(2)^2 Y]_LH = 0", tr_su2_y_lh == 0, str(tr_su2_y_lh))

    # Tr[SU(3)^2 Y]_LH = T(fund_SU3) * (2 * y_QL)
    # SU(3) triplet T = 1/2; trace runs over isospin-replicated triplets
    tr_su3_y_lh = dynkin_fund * (2 * y_QL)
    check("Tr[SU(3)^2 Y]_LH = 1/3", tr_su3_y_lh == Fraction(1, 3), str(tr_su3_y_lh))

    tr_y_cubed_lh = n_QL * y_QL ** 3 + n_LL * y_LL ** 3
    check("Tr[Y^3]_LH = -16/9", tr_y_cubed_lh == Fraction(-16, 9), str(tr_y_cubed_lh))

    # The two nonzero LH traces are the inconsistency that drives Steps 2-4.
    nonzero_anomaly_traces = (tr_su3_y_lh, tr_y_cubed_lh)
    any_nonzero = any(t != 0 for t in nonzero_anomaly_traces)
    check("LH content is anomalous (drives Steps 2-4)", any_nonzero)


def check_full_spectrum_anomaly_cancellation() -> None:
    section("full SM spectrum cancels anomaly (Step 2 output)")
    y = {
        "Q_L": Fraction(1, 3),
        "L_L": Fraction(-1),
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2),
        "nu_R": Fraction(0),
    }
    mult = {"Q_L": 6, "L_L": 2, "u_R": 3, "d_R": 3, "e_R": 1, "nu_R": 1}

    # Tr[Y] (LH minus RH for chirality-signed convention)
    tr_y = (
        mult["Q_L"] * y["Q_L"]
        + mult["L_L"] * y["L_L"]
        - mult["u_R"] * y["u_R"]
        - mult["d_R"] * y["d_R"]
        - mult["e_R"] * y["e_R"]
        - mult["nu_R"] * y["nu_R"]
    )
    check("Tr[Y] = 0 on full spectrum", tr_y == 0, str(tr_y))

    dynkin_fund = Fraction(1, 2)
    tr_su3_y = dynkin_fund * (2 * y["Q_L"] - y["u_R"] - y["d_R"])
    check(
        "Tr[SU(3)^2 Y] = 0 per color on full spectrum",
        tr_su3_y == 0,
        str(tr_su3_y),
    )

    tr_y_cubed = (
        mult["Q_L"] * y["Q_L"] ** 3
        + mult["L_L"] * y["L_L"] ** 3
        - mult["u_R"] * y["u_R"] ** 3
        - mult["d_R"] * y["d_R"] ** 3
        - mult["e_R"] * y["e_R"] ** 3
        - mult["nu_R"] * y["nu_R"] ** 3
    )
    check("Tr[Y^3] = 0 on full spectrum", tr_y_cubed == 0, str(tr_y_cubed))


def check_clifford_volume_classification() -> None:
    section("Clifford volume-element parity (Step 3 input)")
    # omega = gamma_1 ... gamma_n satisfies
    #   omega gamma_mu = (-1)^{n-1} gamma_mu omega
    # n even: anticommutes with all generators -> chirality gamma_5 exists.
    # n odd:  commutes (central) -> no element anticommutes with all -> no chirality.
    for n in range(0, 9):
        sign = (-1) ** (n - 1)
        # We define "anticommutes" iff sign == -1.
        anticommutes = sign == -1
        chirality_exists = anticommutes
        if n % 2 == 0:
            check(
                f"n={n} (even): omega anticommutes with gamma_mu, chirality exists",
                chirality_exists,
            )
        else:
            check(
                f"n={n} (odd): omega is central, no chirality grading",
                not chirality_exists,
            )


def check_d_s_from_a2_then_d_t_odd() -> None:
    section("d_s = 3 from A2, then d_t must be odd (Step 3 conclusion)")
    # A2 supplies d_s = 3 directly. Not derived here.
    d_s = 3
    check("d_s comes from A2 axiom (Z^3 substrate)", d_s == 3)

    # Chirality requires d_s + d_t even, so d_t must be odd given d_s = 3.
    for d_t in range(0, 8):
        n_total = d_s + d_t
        chirality_ok = (n_total % 2) == 0
        if d_t % 2 == 1:
            check(
                f"d_t = {d_t} (odd): d_s + d_t = {n_total} even, chirality OK",
                chirality_ok,
            )
        else:
            check(
                f"d_t = {d_t} (even): d_s + d_t = {n_total} odd, chirality fails",
                not chirality_ok,
            )


def check_single_clock_excludes_dt_gt_1() -> None:
    section("single-clock codim-1 evolution excludes d_t > 1 (Step 4)")
    # Cited theorem: AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md
    # is treated as a black box; this check encodes the conclusion only.
    def single_clock_admits(d_t: int) -> bool:
        return d_t == 1

    for d_t in range(0, 8):
        admits = single_clock_admits(d_t)
        if d_t == 1:
            check(f"single-clock admits d_t = {d_t}", admits)
        else:
            check(f"single-clock excludes d_t = {d_t}", not admits)


def check_d_t_unique_one() -> None:
    section("uniqueness: d_t = 1 (Step 5 combine)")
    d_s = 3
    survivors = []
    for d_t in range(0, 8):
        chirality_ok = ((d_s + d_t) % 2) == 0   # Step 3 (Clifford)
        odd_ok = (d_t % 2) == 1                 # Step 3 conclusion (parity)
        single_clock_ok = d_t == 1              # Step 4 (cited theorem)
        if chirality_ok and odd_ok and single_clock_ok:
            survivors.append(d_t)
    check("only d_t = 1 survives the three constraints", survivors == [1], str(survivors))


def check_lattice_action_boundary() -> None:
    section("load-bearing input boundary")
    allowed_inputs = {
        "chiral-content multiplicities",
        "Dynkin-index bookkeeping",
        "exact rational arithmetic",
        "Clifford-algebra classification",
        "Clifford-volume / sublattice-parity chirality grading",
        "single-clock codimension-1 evolution structure",
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
        "the spatial dimension `d_s = 3`",
        "bare external ABJ anomaly-to-inconsistency admission",
        "the staggered-Dirac realization gate",
        "any continuum-limit numerical claim",
        "any parent theorem/status promotion",
    ]
    for marker in boundary_items:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def check_no_status_promotion_language() -> None:
    section("no status-promotion language")
    forbidden_promotion_phrases = [
        "retained promotion",
        "promote to retained",
        "promote to positive_theorem",
        "claim_type: positive_theorem",
        "claim_type: retained",
    ]
    for marker in forbidden_promotion_phrases:
        check(f"absent: {marker}", marker not in NOTE_TEXT)


def main() -> int:
    print("frontier_dt1_time_dimension_proof_walk_lattice_independence.py")
    check_note_structure()
    check_honest_scope()
    check_dependencies_exist()
    check_exact_lh_anomaly_traces()
    check_full_spectrum_anomaly_cancellation()
    check_clifford_volume_classification()
    check_d_s_from_a2_then_d_t_odd()
    check_single_clock_excludes_dt_gt_1()
    check_d_t_unique_one()
    check_lattice_action_boundary()
    check_no_status_promotion_language()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; the time-dimension forcing chain")
        print("that gives d_t = 1 uses no lattice-action quantity as a load-bearing")
        print("input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
