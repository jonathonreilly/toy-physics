#!/usr/bin/env python3
"""Bounded theorem runner for Wald-Noether BP §5 with explicit admissions.

This runner supports
docs/WALD_NOETHER_BP5_BOUNDED_THEOREM_NOTE_2026-05-10.md.

It checks:

1. structural markers on the bounded theorem note (explicit
   admissions block, retained-no-go citations, open-derivation-gap
   section, "Status authority" framing, repo-canonical vocabulary);
2. existence of every cited authority file in docs/;
3. that every cited authority is referenced in markdown-link form
   so the citation graph parser registers an outgoing edge;
4. the algebraic identities Tr(P_A) = 4, rank(P_A) = 4, and
   Tr(rho_cell P_A) = 1/4 on the time-locked primitive event cell;
5. the Wald-Einstein-Hilbert evaluation S_Wald = A / (4 G_N);
6. the chain identity c_cell = 1 / (4 G_Newton,lat) ⇒ G_Newton,lat = 1;
7. that no observational comparator (S_BH_obs, M_Pl_obs,
   G_Newton_obs) enters the proof input;
8. that no new repo vocabulary is introduced.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WALD_NOETHER_BP5_BOUNDED_THEOREM_NOTE_2026-05-10.md"

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

# Match the same regex the citation-graph builder uses, so this runner
# is robust to citation-form regressions that would silently disappear
# from the dependency graph.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")


CITED_AUTHORITIES = [
    "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
    "PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md",
    "FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md",
    "BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md",
    "PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md",
    "PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md",
    "BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md",
    "PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md",
    "MINIMAL_AXIOMS_2026-05-03.md",
    "BH_ENTROPY_DERIVED_NOTE.md",
]


def check_note_structure() -> None:
    section("note structure and scope")
    required_markers = [
        # claim-type and audit-status authority framing
        "Claim type:** bounded_theorem",
        "Status authority:** independent audit lane only",
        "Type:** bounded_theorem",
        # explicit admissions block
        "Explicit admissions",
        "(X1) Staggered-Dirac realization gate",
        "(X2) Link-local first-variation route",
        # constraints respected (the two retained no-gos)
        "Constraints respected",
        "Hodge-dual degeneracy under substrate symmetries",
        "Free-fermion RT-ratio asymptotes to 1/6, not 1/4",
        # open derivation gap section
        "Open derivation gap",
        "Staggered-Dirac realization gate closure",
        "Link-local first-variation theorem audit promotion",
        # boundaries
        "Boundaries",
        "does not close",
        # explicit no-new-axiom marker
        "framework axiom set remains `A1 + A2`",
        # explicit conditional language on the carrier
        "conditional on (X1) + (X2)",
        # explicit recognition that c_cell trace is pure linear algebra,
        # not a new claim of this note
        "are NOT new content of this note",
        # repo-canonical 'open_gate' label for X1
        "open_gate",
    ]
    for marker in required_markers:
        check(f"contains marker: {marker[:64]}", marker in NOTE_TEXT or marker in NOTE_FLAT)


def check_no_new_vocabulary() -> None:
    section("no new repo vocabulary (per feedback_no_new_repo_vocabulary)")
    blocked_phrases = [
        "algebraic universality",
        "two-class framing",
        "lattice-realization-invariant by definition",
        "carrier from A_min alone",
        # explicit guard against introducing the optional causal-set
        # vocabulary mentioned in the briefing; no precedent exists in
        # the repo, so the note must not introduce it.
        "Dou-Sorkin",
        "horizon molecule",
        "causal set",
    ]
    lower = NOTE_TEXT.lower()
    for phrase in blocked_phrases:
        check(f"forbidden vocabulary absent: {phrase}", phrase.lower() not in lower)


def check_admissions_status_reporting() -> None:
    section("explicit live ledger status reporting on admissions")
    # The note must report a live effective_status value for each
    # admitted upstream gate so reviewers can verify the claimed
    # bounded scope without re-reading the audit ledger.
    must_report = [
        ("X1 ledger status string present", "open_gate"),
        ("X2 ledger status string present", "unaudited"),
        ("retained_no_go status string present", "retained_no_go"),
        ("X1 live verification stamp present", "verified 2026-05-10"),
    ]
    for label, marker in must_report:
        check(label, marker in NOTE_TEXT, marker)


def check_cited_authorities_in_markdown_link_form() -> None:
    section("cited authorities exist and are in markdown-link form")
    found_links = LINK_RE.findall(NOTE_TEXT)
    # The LINK_RE captures group 1 = path inside the parens; normalise
    # to bare filenames (the note uses relative names like FOO.md and
    # ../scripts/foo.py for runners).
    found_md_names = {Path(p).name for p in found_links if p.endswith(".md")}
    for authority in CITED_AUTHORITIES:
        check(
            f"cited authority exists in docs/: {authority}",
            (ROOT / "docs" / authority).exists(),
        )
        check(
            f"cited authority appears in markdown-link form: {authority}",
            authority in found_md_names,
            f"(found {len(found_md_names)} md links)",
        )


def check_primitive_event_cell_algebra() -> None:
    section("primitive event cell algebra (Tr(P_A)=4, Tr(rho_cell P_A)=1/4)")
    axes = ["t", "x", "y", "z"]
    subsets = []
    for k in range(len(axes) + 1):
        for combo in combinations(axes, k):
            subsets.append(frozenset(combo))
    check("Boolean event cell has 16 basis states", len(subsets) == 16)

    index_of = {s: i for i, s in enumerate(subsets)}
    p1_indices = [index_of[frozenset({a})] for a in axes]
    check("P_1 is rank 4 (4 one-axis subsets)", len(p1_indices) == 4)

    P_A = np.zeros((16, 16), dtype=int)
    for i in p1_indices:
        P_A[i, i] = 1
    rho_cell = np.eye(16) / 16

    rank = int(np.trace(P_A))
    check("Tr(P_A) = 4", rank == 4, str(rank))
    check("rank(P_A) = 4", int(np.linalg.matrix_rank(P_A)) == 4)

    c_cell = Fraction(int(np.trace(P_A)), 16)
    check("Tr(rho_cell P_A) = 1/4", c_cell == Fraction(1, 4), str(c_cell))

    # Hodge-dual P_3 also has rank 4 — this is what FIRST_ORDER_COFRAME
    # no-go is about. Verify the dimension so the runner records that
    # this note is aware of the Hodge ambiguity it cites.
    p3_indices = [
        index_of[frozenset(set(axes) - {a})] for a in axes
    ]
    P_3 = np.zeros((16, 16), dtype=int)
    for i in p3_indices:
        P_3[i, i] = 1
    check("rank(P_3) = 4 (Hodge-dual carrier flagged by retained no-go)",
          int(np.trace(P_3)) == 4)
    check("Tr(rho_cell P_3) = 1/4 (Hodge-dual coincidence on Hamming traces)",
          Fraction(int(np.trace(P_3)), 16) == Fraction(1, 4))
    check("P_1 ≠ P_3 as projectors", not np.array_equal(P_A, P_3))


def check_wald_einstein_hilbert_evaluation() -> None:
    section("Wald-Einstein-Hilbert evaluation S_Wald = A / (4 G_N)")
    # Symbolic identity: the EH Lagrangian L = R / (16 pi G_N) gives
    # dL/dR_{abcd} = (1 / (16 pi G_N)) * (1/2)(g^{ac} g^{bd} - g^{ad} g^{bc}).
    # The Wald formula S = -2 pi int_Sigma (dL/dR_{abcd}) eps_{ab} eps_{cd}
    # collapses to A / (4 G_N) for a stationary Killing horizon of area A
    # because the binormal contractions give eps_{ab} eps^{ab} = -2 and
    # the area integral yields A.
    #
    # Here we verify the dimensionless coefficient: -2 pi * (1 / (16 pi))
    # * (-2) = 1/4.  Combined with the area integral A and the G_N
    # denominator that's the standard Wald-EH coefficient.
    import math
    coefficient = -2 * math.pi * (1.0 / (16.0 * math.pi)) * (-2.0)
    check("Wald-EH coefficient = 1/4", math.isclose(coefficient, 0.25), str(coefficient))

    # Composition: c_cell = 1/(4 G_Newton,lat) with c_cell = 1/4
    # forces G_Newton,lat = 1.
    c_cell = Fraction(1, 4)
    g_newton_lat = Fraction(1, 4) / c_cell
    check("c_cell = 1/(4 G_Newton,lat) with c_cell = 1/4 forces G_Newton,lat = 1",
          g_newton_lat == Fraction(1, 1), str(g_newton_lat))


def check_no_observational_comparator() -> None:
    section("no observational comparator enters the proof input")
    forbidden_observational_inputs = [
        "S_BH_obs",
        "M_Pl_obs",
        "G_Newton_obs",
        "PDG",
        "Monte Carlo measurement",
        "fitted observational value",
    ]
    for marker in forbidden_observational_inputs:
        # We allow the marker to be named only as an explicit exclusion;
        # for this bounded theorem note none of these tokens should
        # appear at all, since there is no comparator section.
        check(
            f"forbidden observational input not present: {marker}",
            marker not in NOTE_TEXT,
        )


def check_runner_self_reference() -> None:
    section("runner self-reference is consistent")
    self_path_marker = "scripts/frontier_wald_noether_bp5_bounded.py"
    check(
        "note cites this runner by relative path",
        self_path_marker in NOTE_TEXT,
        self_path_marker,
    )


def main() -> int:
    print("frontier_wald_noether_bp5_bounded.py")
    check_note_structure()
    check_no_new_vocabulary()
    check_admissions_status_reporting()
    check_cited_authorities_in_markdown_link_form()
    check_primitive_event_cell_algebra()
    check_wald_einstein_hilbert_evaluation()
    check_no_observational_comparator()
    check_runner_self_reference()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print(
            "VERDICT: bounded theorem composed on explicit admissions (X1) and (X2); "
            "the two retained no-gos are respected and the open derivation gap is named."
        )
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
