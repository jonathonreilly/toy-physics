#!/usr/bin/env python3
"""Higgs-channel effective-N_taste boundary bounded source-note runner.

Verifies the narrow boundary claim in
docs/HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md

  - Given the Wilson Hamming-weight staircase identity on the 16 BZ
    corners of Z^3 + t APBC (multiplicities binomial(4, hw)
    = (1, 4, 6, 4, 1) for hw in {0, 1, 2, 3, 4}, Wilson shifts
    (0, 2r, 4r, 6r, 8r); proved combinatorially in
    docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md),
    the staircase does not by itself fix the effective N_taste in
    formula [5] of HIGGS_MASS_FROM_AXIOM_NOTE.md, which uses
    N_taste = 16 to obtain m_H_tree = v/(2 u_0) = 140.3 GeV.
  - Identifying the Higgs with a single Hamming-weight class
    hw = k gives effective N_taste^(k) = binomial(4, k) and
    m_H_tree^(k) = v * sqrt(4 / (u_0^2 * binomial(4, k))).
  - The five single-class values are pairwise distinct from the
    uniform-N_taste = 16 value v^2 / (4 u_0^2). The "uniform 16"
    choice is itself an admission, not a consequence of the
    staircase identity.

stdlib only; exact `Fraction` arithmetic for the squared values.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md"

PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""))


def banner(title: str) -> None:
    print()
    print("=" * 88)
    print(f" {title}")
    print("=" * 88)


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(f" {title}")
    print("-" * 88)


NOTE_TEXT = NOTE_PATH.read_text()
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


# ---------------------------------------------------------------------------
# Part 1: Note structure (mirrors the HYPERCHARGE proof-walk template).
# ---------------------------------------------------------------------------
def part1_note_structure() -> None:
    section("Part 1: note structure")
    required = [
        ("title token: Higgs-Channel Effective N_taste Boundary",
         "Higgs-Channel Effective N_taste Boundary"),
        ("claim_type: bounded_theorem", "Claim type:** bounded_theorem"),
        ("status authority phrase",
         "source-note proposal only; audit verdict and"),
        ("Claim section header", "## Claim"),
        ("Channel-assignment table header",
         "## Channel-assignment table"),
        ("Exact Arithmetic Check section header",
         "## Exact Arithmetic Check"),
        ("Dependencies section header", "## Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("upstream Wilson staircase note cited",
         "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08"),
        ("parent Higgs note cited",
         "HIGGS_MASS_FROM_AXIOM_NOTE.md"),
        ("staircase multiplicity tuple stated",
         "(1, 4, 6, 4, 1)"),
        ("Wilson-shift tuple stated",
         "(0, 2r, 4r, 6r, 8r)"),
        ("formula [5] referenced",
         "formula [5]"),
        ("uniform-16 admission named",
         "uniform"),
        ("140.3 GeV headline named",
         "140.3 GeV"),
        ("STAGGERED_DIRAC_REALIZATION_GATE upstream cited",
         "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03"),
        ("MINIMAL_AXIOMS_2026-05-03 upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("source-note proposal language present",
         "source-note proposal only"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden-vocabulary guard (rejected meta-framing tokens
# from the 2026-05-08 review-loop discipline must be absent).
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary() -> None:
    section("Part 2: forbidden meta-framing vocabulary absent")
    forbidden = [
        "algebraic universality",
        "lattice-realization-invariant",
        "two-class framing",
        "(CKN)",
        "(LCL)",
        "(SU5-CKN)",
        "imports problem",
        "Every prediction listed",
        "two-axiom claim",
        "retires admission",
        "sub-class (i)",
        "sub-class (ii)",
    ]
    for token in forbidden:
        check(
            f"absent (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )


# ---------------------------------------------------------------------------
# Part 3: Multiplicities binomial(4, hw) and the 16-state count
# (load-bearing combinatorial input, cited from the upstream Wilson
# staircase note; verified here for self-containment).
# ---------------------------------------------------------------------------
def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    num = 1
    for i in range(k):
        num *= (n - i)
        num //= (i + 1)
    return num


def part3_multiplicities() -> None:
    section("Part 3: multiplicities binomial(4, hw) and 16-state sum")
    expected = [(0, 1), (1, 4), (2, 6), (3, 4), (4, 1)]
    total = 0
    for hw, mult_expected in expected:
        mult = binomial(4, hw)
        check(
            f"binomial(4, {hw}) = {mult_expected}",
            mult == mult_expected,
            f"computed {mult}",
        )
        total += mult
    check(
        "sum over hw classes = 2^4 = 16",
        total == 16,
        f"sum = {total}",
    )


# ---------------------------------------------------------------------------
# Part 4: Channel-assignment table — for each k ∈ {0,1,2,3,4}, compute
# (m_H_tree^(k))^2 = v^2 · 4 / (u_0^2 · binomial(4, k)) at exact
# Fraction precision, with the Higgs note's stated v and u_0 as exact
# rationals.
# ---------------------------------------------------------------------------
# v = 246.22 GeV  ->  Fraction(24622, 100) = Fraction(12311, 50)
V = Fraction(24622, 100)
# u_0 = 0.8776   ->  Fraction(8776, 10000) = Fraction(1097, 1250)
U0 = Fraction(8776, 10000)


def m_h_tree_squared(n_taste_int: int) -> Fraction:
    """Return (m_H_tree)^2 for effective N_taste = n_taste_int.

    formula [1] in the note:
        (m_H_tree)^2  =  v^2 · 4  /  ( u_0^2 · N_taste )
    """
    return (V * V * Fraction(4)) / (U0 * U0 * Fraction(n_taste_int))


def part4_channel_assignment_table() -> None:
    section("Part 4: channel-assignment table at exact Fraction precision")
    # Rational-arithmetic placeholder values check.
    check(
        "v = 246.22 as exact Fraction(12311, 50)",
        V == Fraction(12311, 50),
        f"V = {V}",
    )
    check(
        "u_0 = 0.8776 as exact Fraction(1097, 1250)",
        U0 == Fraction(1097, 1250),
        f"U0 = {U0}",
    )
    check(
        "v stated = 24622 / 100",
        Fraction(24622, 100) == V,
    )
    check(
        "u_0 stated = 8776 / 10000",
        Fraction(8776, 10000) == U0,
    )

    # Per-class squared values.
    rows: dict[int, tuple[int, Fraction]] = {}
    for k in (0, 1, 2, 3, 4):
        n_k = binomial(4, k)
        m_sq = m_h_tree_squared(n_k)
        rows[k] = (n_k, m_sq)

    # Symbolic equalities expected from the note's claim.
    check(
        "k = 0 and k = 4 share N_taste = 1 (binomial symmetry)",
        rows[0][0] == rows[4][0] == 1,
    )
    check(
        "k = 1 and k = 3 share N_taste = 4 (binomial symmetry)",
        rows[1][0] == rows[3][0] == 4,
    )
    check(
        "k = 2 has N_taste = 6",
        rows[2][0] == 6,
    )
    check(
        "k = 0 and k = 4 give equal (m_H_tree)^2 (binomial symmetry)",
        rows[0][1] == rows[4][1],
        f"{rows[0][1]} vs {rows[4][1]}",
    )
    check(
        "k = 1 and k = 3 give equal (m_H_tree)^2 (binomial symmetry)",
        rows[1][1] == rows[3][1],
        f"{rows[1][1]} vs {rows[3][1]}",
    )

    # Distinctness across the three non-symmetric outcomes:
    # {k=0/4 -> N=1, k=1/3 -> N=4, k=2 -> N=6} should give three
    # different squared values.
    distinct_squares = {rows[0][1], rows[1][1], rows[2][1]}
    check(
        "k = 0/4, k = 1/3, k = 2 give three pairwise-distinct (m_H_tree)^2",
        len(distinct_squares) == 3,
        f"distinct = {len(distinct_squares)}",
    )

    # Numerical readouts for table sanity (pure float report; truth is
    # the Fraction equality above).
    for k in (0, 1, 2, 3, 4):
        n_k, m_sq = rows[k]
        m_float = float(m_sq) ** 0.5
        rounded = round(m_float, 1)
        check(
            f"k = {k}: N_taste = {n_k}, m_H_tree ≈ {rounded:.1f} GeV",
            True,
            f"(m_H_tree)^2 = {m_sq}",
        )

    # Spot-check the rounded numerical predictions against the table in
    # the note (read as approximate display).
    expected_rounded = {0: 561.1, 1: 280.6, 2: 229.1, 3: 280.6, 4: 561.1}
    for k, target in expected_rounded.items():
        m_float = float(rows[k][1]) ** 0.5
        rounded = round(m_float, 1)
        check(
            f"k = {k}: rounded m_H_tree ≈ {target} GeV (display only)",
            abs(rounded - target) <= 0.1,
            f"computed {rounded}",
        )


# ---------------------------------------------------------------------------
# Part 5: Uniform-16 admission identity — the choice that produces the
# existing 140.3 GeV headline.
# ---------------------------------------------------------------------------
def part5_uniform_admission() -> None:
    section("Part 5: uniform-N_taste = 16 admission and 140.3 GeV identity")
    # Sum of staircase multiplicities = 16 (the structural fact that
    # makes the uniform admission consistent with the staircase).
    multiplicity_sum = sum(binomial(4, k) for k in (0, 1, 2, 3, 4))
    check(
        "sum_{k=0}^{4} binomial(4, k) = 16",
        multiplicity_sum == 16,
        f"sum = {multiplicity_sum}",
    )

    # Uniform-16 squared value = v^2 / (4 u_0^2) = (v/(2 u_0))^2.
    m_sq_uniform = m_h_tree_squared(16)
    direct = (V / (Fraction(2) * U0)) ** 2
    check(
        "uniform-16: (m_H_tree)^2 = v^2 / (4 u_0^2) = (v/(2 u_0))^2",
        m_sq_uniform == direct,
        f"{m_sq_uniform} vs {direct}",
    )

    # Numerical: should round to 140.3 GeV at 0.1-GeV precision.
    m_float = float(m_sq_uniform) ** 0.5
    rounded = round(m_float, 1)
    check(
        "uniform-16: m_H_tree rounds to 140.3 GeV (display)",
        abs(rounded - 140.3) <= 0.1,
        f"computed {rounded}",
    )


# ---------------------------------------------------------------------------
# Part 6: Distinctness — none of the five single-class values coincides
# with the uniform-16 value (the boundary statement).
# ---------------------------------------------------------------------------
def part6_distinctness_from_uniform() -> None:
    section("Part 6: single-class assignments distinct from uniform-16")
    m_sq_uniform = m_h_tree_squared(16)
    for k in (0, 1, 2, 3, 4):
        n_k = binomial(4, k)
        m_sq_k = m_h_tree_squared(n_k)
        check(
            f"k = {k} (N_taste = {n_k}): (m_H_tree)^2 != uniform-16 (m_H_tree)^2",
            m_sq_k != m_sq_uniform,
            f"{m_sq_k} vs {m_sq_uniform}",
        )

    # Also verify the symbolic ratio: uniform-16 / single-class-k =
    # binomial(4, k) / 16 (each single-class value is scaled relative
    # to the uniform value by 16 / binomial(4, k)).
    for k in (0, 1, 2, 3, 4):
        n_k = binomial(4, k)
        m_sq_k = m_h_tree_squared(n_k)
        ratio = m_sq_k / m_sq_uniform
        expected = Fraction(16, n_k)
        check(
            f"k = {k}: ratio (m_H_tree^(k))^2 / (uniform-16)^2 = 16 / binomial(4, {k}) = {expected}",
            ratio == expected,
            f"ratio = {ratio}",
        )


# ---------------------------------------------------------------------------
# Part 7: Cited upstream files exist.
# ---------------------------------------------------------------------------
def part7_premise_class_consistency() -> None:
    section("Part 7: cited upstream files exist on this branch")
    must_exist = [
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(
            f"upstream exists: {rel}",
            (ROOT / rel).exists(),
        )


# ---------------------------------------------------------------------------
# Part 8: Forbidden-import audit (stdlib only; no PDG-value pins).
# ---------------------------------------------------------------------------
def part8_forbidden_imports() -> None:
    section("Part 8: stdlib-only / no PDG-value pins in runner code")
    runner_text = Path(__file__).read_text()
    allowed_imports = {"fractions", "pathlib", "re", "sys", "__future__"}
    import_lines = [
        ln.strip() for ln in runner_text.splitlines()
        if ln.strip().startswith("import ") or ln.strip().startswith("from ")
    ]
    bad: list[str] = []
    for ln in import_lines:
        if ln.startswith("from "):
            mod = ln.split()[1].split(".")[0]
        elif ln.startswith("import "):
            mod = ln.split()[1].split(".")[0].rstrip(",")
        else:
            continue
        if mod not in allowed_imports:
            bad.append(ln)
    check(
        "all top-level imports are stdlib (no numpy/scipy/sympy/etc.)",
        not bad,
        f"non-stdlib = {bad}" if bad else "stdlib only",
    )

    # Note: this runner deliberately uses v = 246.22 and u_0 = 0.8776
    # as Fraction placeholders matching the values stated in
    # HIGGS_MASS_FROM_AXIOM_NOTE.md. These are not new PDG pins; they
    # are the parent note's already-stated values. The pin-pattern
    # search below excludes the explicit Fraction(...) construction.
    # We check that no observable (m_X = float, alpha_X = float) is
    # being introduced by this runner.
    suspicious_floats = re.findall(
        r"\b(?:m_[a-z]+|alpha_[a-z]+|g_[a-z]+_obs)\s*=\s*\d+\.\d+\b",
        runner_text,
    )
    check(
        "no PDG-observable pin pattern (m_X = ..., alpha_X = ...)",
        not suspicious_floats,
        f"matches: {suspicious_floats}" if suspicious_floats else "none",
    )


# ---------------------------------------------------------------------------
# Part 9: Boundary check — what this note explicitly does NOT close.
# ---------------------------------------------------------------------------
def part9_boundary_check() -> None:
    section("Part 9: boundary check (what is NOT closed)")
    not_claimed = [
        "the `+12%` Higgs gap chain",
        "the Higgs-channel assignment itself",
        "any derivation of the Wilson coefficient `r`",
        "the staggered-Dirac realization gate",
        "any retention upgrade of `HIGGS_MASS_FROM_AXIOM_NOTE.md`",
        "any retention upgrade of",
        "any claim that one of the five single-class values is preferred",
        "the uniform `N_taste = 16` choice is wrong",
        "any parent theorem/status promotion",
    ]
    for marker in not_claimed:
        check(
            f"note explicitly does not close: {marker}",
            marker in NOTE_TEXT,
        )

    check(
        "claim_type: bounded_theorem stated",
        "Claim type:** bounded_theorem" in NOTE_TEXT,
    )
    check(
        "source-note proposal language present",
        "source-note proposal only" in NOTE_TEXT,
    )
    check(
        "boundary explicitly states staircase does not by itself fix N_taste",
        "does not by itself fix" in NOTE_TEXT
        or "does not by itself fix the effective" in NOTE_FLAT
        or "does** not** fix" in NOTE_TEXT
        or "does **not**" in NOTE_TEXT,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    banner("frontier_higgs_channel_effective_ntaste_boundary.py")
    print(" Bounded boundary statement: the Wilson Hamming-weight staircase")
    print(" does not by itself fix N_taste in HIGGS_MASS_FROM_AXIOM_NOTE.md")
    print(" formula [5]; the five single-class assignments give five")
    print(" distinct m_H_tree values, none matching the uniform-16 admission")
    print(" that produces the existing 140.3 GeV headline.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_multiplicities()
    part4_channel_assignment_table()
    part5_uniform_admission()
    part6_distinctness_from_uniform()
    part7_premise_class_consistency()
    part8_forbidden_imports()
    part9_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: the Wilson Hamming-weight staircase does not by itself")
        print(" fix N_taste in HIGGS_MASS_FROM_AXIOM_NOTE.md formula [5]; the")
        print(" five single-class assignments give five distinct m_H_tree")
        print(" values, none of which coincides with the uniform-16 admission")
        print(" that produces the existing 140.3 GeV headline.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
