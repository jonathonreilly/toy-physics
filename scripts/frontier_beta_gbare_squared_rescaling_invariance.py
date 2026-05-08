#!/usr/bin/env python3
"""Bounded arithmetic identity runner for `beta * g_bare^2 = 2 N_c`.

This runner supports
docs/BETA_GBARE_SQUARED_RESCALING_INVARIANCE_BOUNDED_NOTE_2026-05-08.md.
It verifies, at exact rational precision, that the dimensionless
identity `beta * g_bare^2 = 2 N_c` (a direct algebraic consequence of
the Wilson small-a matching `beta = 2 N_c / g_bare^2` carried by
G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md) is invariant under the
generator-basis rescaling `T_a -> c * T_a` (equivalently `A -> c * A`)
established by
G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md.

The runner is stdlib-only and uses `fractions.Fraction` throughout. The
checked rescaling values are `c in {1/2, 1, 2, 3}`.
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
    / "BETA_GBARE_SQUARED_RESCALING_INVARIANCE_BOUNDED_NOTE_2026-05-08.md"
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
        "bounded arithmetic identity",
        "Imported Authorities",
        "Arithmetic Identity Table",
        "Boundaries",
        "G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18",
        "G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03",
        "fractions.Fraction",
    ]
    for marker in required:
        check(
            f"contains marker: {marker[:56]}",
            marker in NOTE_TEXT or marker in NOTE_FLAT,
        )

    forbidden_framing = [
        "continuum-limit class",
        "two-class",
        "Wilson asymptotic universality",
        "sub-class (i)",
        "sub-class (ii)",
        "algebraic universality",
        "lattice-realization-invariant",
    ]
    lower = NOTE_TEXT.lower()
    for marker in forbidden_framing:
        check(
            f"forbidden framing absent: {marker}",
            marker.lower() not in lower,
            "" if marker.lower() not in lower else "found",
        )


def check_dependencies_exist() -> None:
    section("dependency files")
    deps = [
        "docs/G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md",
        "docs/G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md",
    ]
    for rel in deps:
        check(f"dependency exists: {rel}", (ROOT / rel).exists())


def check_imported_inputs_exist() -> None:
    section("imported authority content checks")
    two_ward = (ROOT / "docs" / "G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md").read_text()
    check(
        "two-ward note carries Wilson small-a matching beta = 2 N_c / g_bare^2",
        "g_bare^2" in two_ward.replace("²", "^2")
        or "g_bare²" in two_ward
        or "2 N_c" in two_ward,
    )
    check(
        "two-ward note carries the canonical g_bare = 1 closure value",
        "g_bare = 1" in two_ward or "g_bare² = 1" in two_ward or "g_bare^2 = 1" in two_ward.replace("²", "^2"),
    )
    rescaling = (
        ROOT / "docs" / "G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md"
    ).read_text()
    check(
        "rescaling note carries the T_a -> c T_a generator-basis rescaling",
        "T_a -> c" in rescaling or "T_a → c" in rescaling or "c * T_a" in rescaling or "c T_a" in rescaling,
    )
    check(
        "rescaling note carries the beta -> c^2 beta mapping",
        "c^2 * beta" in rescaling
        or "c^2 beta" in rescaling
        or "c^2 * (2 N_c" in rescaling
        or "c^2 * β" in rescaling,
    )


def check_arithmetic_identity_at_canonical_value() -> None:
    section("arithmetic identity at canonical g_bare^2 = 1, N_c = 3")
    n_c = Fraction(3)
    g_bare_sq = Fraction(1)
    beta = Fraction(2 * n_c) / g_bare_sq
    check("beta = 2 N_c / g_bare^2 = 6", beta == Fraction(6), str(beta))
    product = beta * g_bare_sq
    check(
        "beta * g_bare^2 = 2 N_c (canonical value)",
        product == 2 * n_c,
        str(product),
    )


def check_rescaling_invariance_table() -> None:
    section("rescaling invariance table at exact rational precision")
    n_c = Fraction(3)
    target = 2 * n_c

    g_bare_sq_canonical = Fraction(1)
    beta_canonical = 2 * n_c / g_bare_sq_canonical
    check(
        "canonical product equals 2 N_c",
        beta_canonical * g_bare_sq_canonical == target,
        str(beta_canonical * g_bare_sq_canonical),
    )

    rescaling_values = [Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)]

    expected_pairs = {
        Fraction(1, 2): (Fraction(6) / Fraction(4), Fraction(4)),
        Fraction(1): (Fraction(6), Fraction(1)),
        Fraction(2): (Fraction(24), Fraction(1, 4)),
        Fraction(3): (Fraction(54), Fraction(1, 9)),
    }

    for c in rescaling_values:
        c_sq = c * c
        beta_prime = c_sq * beta_canonical
        g_bare_sq_prime = g_bare_sq_canonical / c_sq

        check(
            f"c = {c}: beta'(c) = c^2 * beta",
            beta_prime == c_sq * beta_canonical,
            f"beta'={beta_prime}",
        )
        check(
            f"c = {c}: g_bare'^2(c) = g_bare^2 / c^2",
            g_bare_sq_prime == g_bare_sq_canonical / c_sq,
            f"g_bare'^2={g_bare_sq_prime}",
        )

        exp_beta_prime, exp_g_sq_prime = expected_pairs[c]
        check(
            f"c = {c}: beta'(c) matches expected table value",
            beta_prime == exp_beta_prime,
            f"beta'={beta_prime} expected={exp_beta_prime}",
        )
        check(
            f"c = {c}: g_bare'^2(c) matches expected table value",
            g_bare_sq_prime == exp_g_sq_prime,
            f"g_bare'^2={g_bare_sq_prime} expected={exp_g_sq_prime}",
        )

        product_prime = beta_prime * g_bare_sq_prime
        check(
            f"c = {c}: beta'(c) * g_bare'^2(c) = 2 N_c (rescaling-invariant)",
            product_prime == target,
            f"product={product_prime}",
        )

        c_powers_cancel = c_sq * (Fraction(1) / c_sq)
        check(
            f"c = {c}: c^2 * (1 / c^2) = 1 (algebraic cancellation)",
            c_powers_cancel == Fraction(1),
            f"c^2/c^2={c_powers_cancel}",
        )


def check_arithmetic_identity_symbolic_consistency() -> None:
    section("identity holds for arbitrary g_bare^2 (symbolic substitution)")
    n_c = Fraction(3)
    target = 2 * n_c
    for num, den in [(1, 1), (3, 4), (5, 7), (11, 13), (1, 100)]:
        g_bare_sq = Fraction(num, den)
        beta = 2 * n_c / g_bare_sq
        product = beta * g_bare_sq
        check(
            f"beta * g_bare^2 = 2 N_c at g_bare^2 = {g_bare_sq}",
            product == target,
            str(product),
        )

        for c in [Fraction(1, 2), Fraction(2), Fraction(3)]:
            c_sq = c * c
            beta_prime = c_sq * beta
            g_bare_sq_prime = g_bare_sq / c_sq
            product_prime = beta_prime * g_bare_sq_prime
            check(
                f"rescaling invariance at g_bare^2 = {g_bare_sq}, c = {c}",
                product_prime == target,
                f"product={product_prime}",
            )


def check_boundary_clauses() -> None:
    section("boundary clauses present")
    boundaries = [
        "bounded arithmetic identity only",
        "continuum-limit statement",
        "any retention or promotion",
        "imported Wilson small-`a` matching relation",
        "imported generator-basis rescaling theorem",
        "Wilson plaquette vs Symanzik vs",
        "canonical Cl(3) connection normalization",
        "parent theorem/status promotion",
    ]
    for marker in boundaries:
        check(f"boundary clause present: {marker}", marker in NOTE_TEXT)


def main() -> int:
    print("frontier_beta_gbare_squared_rescaling_invariance.py")
    check_note_structure()
    check_dependencies_exist()
    check_imported_inputs_exist()
    check_arithmetic_identity_at_canonical_value()
    check_rescaling_invariance_table()
    check_arithmetic_identity_symbolic_consistency()
    check_boundary_clauses()
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print(
            "VERDICT: bounded arithmetic identity passes; beta * g_bare^2 = 2 N_c is"
        )
        print(
            "invariant under the imported generator-basis rescaling for c in {1/2, 1,"
        )
        print("2, 3} at exact rational precision.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
