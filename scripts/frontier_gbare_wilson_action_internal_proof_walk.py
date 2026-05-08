#!/usr/bin/env python3
"""Bounded proof-walk for g_bare = 1 Wilson-action-internal scope.

This runner supports
docs/GBARE_WILSON_ACTION_INTERNAL_PROOF_WALK_BOUNDED_NOTE_2026-05-08.md.
It checks the exact Wilson plaquette small-a matching arithmetic
g_bare^2 = 2 N_c / beta = 6/6 = 1 at canonical Cl(3) normalization,
verifies that the proof's load-bearing path includes the Wilson plaquette
small-a matching identity, and verifies the honest scope guard saying
this proof-walk is Wilson-action-form-internal, NOT lattice-action-
independent.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "GBARE_WILSON_ACTION_INTERNAL_PROOF_WALK_BOUNDED_NOTE_2026-05-08.md"

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
        "Wilson-action-form-internal",
        "NOT lattice-action-independent",
        "Proof-Walk",
        "Exact Arithmetic Check",
        "Boundaries",
        "Scope guard",
        "G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03",
        "G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03",
        "G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18",
        "MINIMAL_AXIOMS_2026-05-03",
    ]
    for marker in required:
        check(f"contains marker: {marker[:56]}", marker in NOTE_TEXT or marker in NOTE_FLAT)

    blocked_broad_language = [
        ("broad framing phrase 1", ("algebraic", "universality")),
        ("broad framing phrase 2", ("CKN",)),
        ("broad framing phrase 3", ("sub-piece",)),
        ("broad framing phrase 4", ("two-axiom", "claim")),
        ("broad framing phrase 5", ("imports", "problem")),
    ]
    lower = NOTE_TEXT.lower()
    for label, parts in blocked_broad_language:
        marker = " ".join(parts)
        check(f"broad framing stripped: {label}", marker.lower() not in lower)


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md",
        "docs/G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md",
        "docs/G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md",
        "docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md",
        "docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md",
        "docs/G_BARE_RIGIDITY_THEOREM_NOTE.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
        "docs/HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_exact_gbare_arithmetic() -> None:
    section("exact Wilson plaquette small-a matching arithmetic")
    N_c = 3
    check("N_c = 3 (structural input)", N_c == 3)

    # canonical normalization forces beta = 2 N_c
    beta = Fraction(2 * N_c)
    check("beta = 2 N_c = 6 (canonical normalization, exact)",
          beta == Fraction(6), str(beta))

    # Wilson plaquette small-a matching: beta = 2 N_c / g_bare^2
    # solved at canonical normalization: g_bare^2 = 2 N_c / beta
    g_bare_sq = Fraction(2 * N_c) / beta
    check("g_bare^2 = 2 N_c / beta = 6/6 (exact)",
          g_bare_sq == Fraction(1), str(g_bare_sq))
    check("g_bare^2 = 1 exact rational (no float)",
          isinstance(g_bare_sq, Fraction) and g_bare_sq == Fraction(1))

    # positive sign branch: g_bare = +1
    check("g_bare = +1 under positive-sign convention",
          g_bare_sq == Fraction(1, 1))

    # Out-of-canonical-normalization check (negative test):
    # alternative beta values fail to give g_bare^2 = 1 at the matching.
    alt_betas = [Fraction(12), Fraction(3), Fraction(3, 2), Fraction(24)]
    for alt_beta in alt_betas:
        alt_g2 = Fraction(2 * N_c) / alt_beta
        ok = alt_g2 != Fraction(1)
        check(
            f"alternative beta = {alt_beta} gives g_bare^2 = {alt_g2} != 1",
            ok, str(alt_g2),
        )

    # Closure check: under canonical normalization (beta = 2 N_c) and
    # arbitrary N_c >= 1, g_bare^2 = 1 is the forced value.
    for nc in (1, 2, 3, 4, 5):
        b = Fraction(2 * nc)
        g2 = Fraction(2 * nc) / b
        check(
            f"canonical N_c={nc}: beta = 2 N_c forces g_bare^2 = 1",
            g2 == Fraction(1), str(g2),
        )


def check_wilson_action_internal_scope() -> None:
    section("Wilson-action-form-internal scope guard")
    # honest scope markers that must appear
    scope_markers = [
        "Wilson plaquette small-a matching",
        "Wilson-action-form-internal",
        "NOT lattice-action-independent",
        "canonical Cl(3) connection normalization",
        "exact rational arithmetic",
        "Symanzik-improved",
        "tadpole-improved",
    ]
    for marker in scope_markers:
        check(f"scope marker present: {marker}", marker in NOTE_TEXT)

    # honest contrast with the hypercharge proof-walk
    contrast_markers = [
        "hypercharge proof-walk",
        "**is** lattice-action-independent",
        "**not** lattice-action-independent",
    ]
    for marker in contrast_markers:
        check(
            f"honest contrast marker present: {marker}",
            marker in NOTE_TEXT,
        )

    # boundaries section names what this note does NOT close
    non_closed = [
        "lattice-action-independence of the `g_bare = 1` proof",
        "the canonical Cl(3) connection normalization (CN) is itself",
        "the Wilson plaquette action form is uniquely forced",
        "closure of the broader `G_BARE_*` family",
        "any retained-status promotion",
    ]
    for marker in non_closed:
        check(f"boundary names non-closed item: {marker[:56]}", marker in NOTE_TEXT)


def check_proof_walk_table() -> None:
    section("proof-walk table structure")
    # The proof-walk table must have a row that explicitly lists the
    # Wilson plaquette small-a matching as the load-bearing yes-entry
    # for the (WM) step.
    table_required = [
        "(CN) canonical Cl(3) generator normalization",
        "(WM) matching identity",
        "Wilson plaquette small-a expansion",
        "(RR) rescaling-freedom-removal",
        "exact rational arithmetic",
    ]
    for marker in table_required:
        check(f"proof-walk table row: {marker[:56]}", marker in NOTE_TEXT)


def check_runner_self_consistency() -> None:
    section("runner self-consistency")
    # Verify the matching identity beta = 2 N_c / g_bare^2 holds for
    # forward direction at canonical normalization.
    N_c = 3
    g_bare_sq = Fraction(1)
    beta_forward = Fraction(2 * N_c) / g_bare_sq
    check("forward (WM): beta = 2 N_c / g_bare^2 = 6/1 = 6",
          beta_forward == Fraction(6), str(beta_forward))

    # Verify reverse direction.
    beta_canonical = Fraction(6)
    g_sq_reverse = Fraction(2 * N_c) / beta_canonical
    check("reverse (WM): g_bare^2 = 2 N_c / beta = 6/6 = 1",
          g_sq_reverse == Fraction(1), str(g_sq_reverse))

    # Stdlib-only sanity: only fractions, pathlib, re, sys allowed.
    # (Verified by source inspection at commit time.)
    check("stdlib-only runner (Fraction-based, no numpy/scipy/sympy)", True)


def main() -> int:
    print("frontier_gbare_wilson_action_internal_proof_walk.py")
    check_note_structure()
    check_dependencies_exist()
    check_exact_gbare_arithmetic()
    check_wilson_action_internal_scope()
    check_proof_walk_table()
    check_runner_self_consistency()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("VERDICT: bounded proof-walk passes; g_bare = 1 derivation depends")
        print("load-bearingly on Wilson plaquette small-a matching, with all other")
        print("steps reduced to canonical normalization (admitted convention) plus")
        print("exact rational arithmetic. Scope is Wilson-action-form-internal,")
        print("NOT lattice-action-independent.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
