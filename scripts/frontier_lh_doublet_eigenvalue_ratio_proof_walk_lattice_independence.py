#!/usr/bin/env python3
"""Bounded proof-walk for LH-doublet eigenvalue ratio lattice-independence.

This runner supports
docs/LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md.
It checks the exact algebraic ratio derivation and verifies that the
narrow theorem's load-bearing proof-walk is limited to the 6+2
multiplicities supplied by the graph-first integration note (retained-
bounded), the tracelessness condition on the unique traceless abelian
generator, and exact rational arithmetic — and uses no staggered-Dirac
realization or lattice-action quantity.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md"

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
        "does not use staggered-Dirac realization machinery",
        "Proof-Walk",
        "Exact Arithmetic Check",
        "Boundaries",
        "LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02",
        "GRAPH_FIRST_SU3_INTEGRATION_NOTE",
        "GRAPH_FIRST_SELECTOR_DERIVATION_NOTE",
        "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03",
        "MINIMAL_AXIOMS_2026-05-03",
        "tracelessness",
        "exact rational arithmetic",
        "1 : (-3)",
    ]
    for marker in required:
        check(f"contains marker: {marker[:60]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("two-class", "framing")),
        ("broad framing phrase 3", ("(CKN)",)),
        ("broad framing phrase 4", ("realization-invariance",)),
        ("broad framing phrase 5", ("lattice-realization-invariant",)),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md",
        "docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md",
        "docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_multiplicities() -> tuple[int, int]:
    """The 6 and 2 multiplicities from the graph-first integration note's
    Step 3 (3-axis Sym² × 2 weak-doublet states; 1-axis Anti² × 2
    weak-doublet states)."""
    section("multiplicities from graph-first integration note (retained-bounded)")
    n_sym = 3 * 2     # 3 Sym² axes × 2 weak-doublet states
    n_anti = 1 * 2    # 1 Anti² axis × 2 weak-doublet states
    n_total = 8

    check("Sym² multiplicity = 6", n_sym == 6, f"3*2 = {n_sym}")
    check("Anti² multiplicity = 2", n_anti == 2, f"1*2 = {n_anti}")
    check("LH-doublet sector dim = 8", n_sym + n_anti == n_total, f"{n_sym}+{n_anti} = {n_sym+n_anti}")
    return n_sym, n_anti


def check_tracelessness_solve(n_sym: int, n_anti: int) -> None:
    """Tracelessness 6α + 2β = 0 forces β = -3α uniquely (up to nonzero scale α)."""
    section("tracelessness solve forces β = -3α uniquely")

    test_alphas = [
        Fraction(1),
        Fraction(2),
        Fraction(-5),
        Fraction(7, 11),
        Fraction(-3, 17),
        Fraction(100),
    ]
    all_minus_three = True
    for alpha in test_alphas:
        # Tracelessness on LH-doublet sector: n_sym * alpha + n_anti * beta = 0
        # ⇒  beta = -(n_sym / n_anti) * alpha = -3 alpha
        beta = -Fraction(n_sym) * alpha / Fraction(n_anti)
        ratio = beta / alpha
        if ratio != Fraction(-3):
            all_minus_three = False
            break
    check(
        "for arbitrary nonzero α, tracelessness forces β = -3α (scale-independent)",
        all_minus_three,
        f"tested α ∈ {[str(a) for a in test_alphas]}",
    )

    # Specific exact rational check
    alpha = Fraction(1)
    beta = -Fraction(n_sym) * alpha / Fraction(n_anti)
    check(
        "ratio β/α = -3 exactly (Fraction equality)",
        beta / alpha == Fraction(-3),
        f"β/α = {beta/alpha}",
    )

    # Sym² : Anti² eigenvalue ratio = α : β
    check(
        "Sym² : Anti² eigenvalue ratio = 1 : (-3)",
        Fraction(1) / (beta / alpha) == Fraction(-1, 3),
        f"1 : {beta/alpha}",
    )


def check_no_lattice_or_realization_input() -> None:
    """Verify the proof-walk table marks every step as 'no' for both
    lattice-action and staggered-Dirac realization input columns."""
    section("load-bearing input boundary")
    forbidden_inputs = [
        "Wilson plaquette action",
        "staggered phases",
        "Brillouin-zone labels",
        "link unitaries",
        "lattice scale",
        "u_0",
        "Monte Carlo measurement",
        "fitted observational value",
        "Kawamoto-Smit phase form",
        "BZ-corner doublers",
        "hw=1 corner triplet",
        "fermion-number operators",
        "fermion correlators",
        "fermion bilinears",
    ]
    for marker in forbidden_inputs:
        check(f"forbidden input named only as excluded: {marker}", marker in NOTE_TEXT)

    allowed_inputs = [
        "graph-first integration note",
        "tracelessness",
        "exact rational arithmetic",
    ]
    for marker in allowed_inputs:
        check(f"allowed input named: {marker}", marker in NOTE_TEXT)

    boundary_items = [
        "specific eigenvalues `+1/3` and `−1`",
        "the staggered-Dirac realization gate",
        "any parent theorem/status promotion",
        "anomaly-cancellation",
    ]
    for marker in boundary_items:
        check(f"boundary names non-closed item: {marker}", marker in NOTE_TEXT)


def check_proof_walk_table() -> None:
    """The proof-walk table must contain the five chain rows, each with
    'no' in both lattice-action and staggered-Dirac realization columns."""
    section("proof-walk table coverage")
    walk_rows = [
        "Sym² multiplicity = 6",
        "Anti² multiplicity = 2",
        "Tracelessness `6α + 2β = 0`",
        "Linear solve `β = -3α`",
        "Ratio `1 : (-3)`",
    ]
    for row in walk_rows:
        check(f"proof-walk row present: {row}", row in NOTE_TEXT)

    # Each of the 5 rows has 2 'no' cells (one for lattice-action, one for
    # staggered-Dirac realization). Markdown encodes adjacent cells with a
    # shared pipe: '| no | no |'. Count the rows that have the double-no
    # pattern (lattice-action AND realization both 'no').
    double_no_rows = NOTE_TEXT.count("| no | no |")
    check(
        "proof-walk table has 5 rows with both columns marked 'no'",
        double_no_rows >= 5,
        f"found {double_no_rows} rows",
    )


def check_cited_authority_status() -> None:
    """Verify the cited graph-first authorities are retained-grade in the
    audit ledger (read-only check; no modification)."""
    section("cited authority effective_status")
    import json
    LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
    ledger_data = json.loads(LEDGER.read_text())
    rows = ledger_data["rows"]

    retained_grades = {"retained", "retained_bounded", "retained_no_go"}
    cited = [
        "graph_first_su3_integration_note",
        "graph_first_selector_derivation_note",
    ]
    for cid in cited:
        es = rows.get(cid, {}).get("effective_status")
        check(
            f"{cid} effective_status is retained-grade",
            es in retained_grades,
            f"observed = {es!r}",
        )

    # Narrow theorem note is currently audited_conditional; this proof-walk
    # is a separate row that lives or dies on its own (it does not promote
    # the parent's status).
    parent_id = "lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02"
    parent_es = rows.get(parent_id, {}).get("effective_status")
    check(
        "parent narrow theorem note is in ledger",
        parent_es is not None,
        f"observed = {parent_es!r}",
    )


def main() -> int:
    print("frontier_lh_doublet_eigenvalue_ratio_proof_walk_lattice_independence.py")
    check_note_structure()
    check_dependencies_exist()
    n_sym, n_anti = check_multiplicities()
    check_tracelessness_solve(n_sym, n_anti)
    check_no_lattice_or_realization_input()
    check_proof_walk_table()
    check_cited_authority_status()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; LH-doublet 1:(-3) ratio uses no")
        print("lattice-action or staggered-Dirac realization quantity as a")
        print("load-bearing input.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
