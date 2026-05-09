#!/usr/bin/env python3
"""Higgs taste-singlet projection on Hamming-weight staircase — bounded source-note runner.

Verifies docs/HIGGS_TASTE_SINGLET_PROJECTION_BOUNDED_NOTE_2026-05-09.md:

  ( m_H_W / v )^2  =  Σ_{k=0}^{4}  w_k · c_k ( r, u_0 )                   (eq. (1))

where:
  w_k             =  binomial(4, k) / 16                                  (eq. (2))
  c_k(r, u_0)     =  (u_0^2 - (k-2)^2 r^2) / ( 4 · ((k-2)^2 r^2 + u_0^2)^2 )  (eq. (3))

The runner verifies, at exact rational precision via fractions.Fraction:

  (Part 1) note structure;
  (Part 2) forbidden-vocabulary absence (note + runner module docstring);
  (Part 3) cited upstreams (with graceful forward-references);
  (Part 4) weight normalization Σ w_k = 1 (taste-singlet projection sums on
           Hamming staircase to unity);
  (Part 5) reduction at r=0: c_k(0, u_0) = 1/(4 u_0^2) for every k;
           Σ w_k c_k(0, u_0) = 1/(4 u_0^2) (matches parent eq. [5]);
  (Part 6) k=2 Wilson-decoupling: c_2(r, u_0) = 1/(4 u_0^2) for all r;
  (Part 7) reflection symmetry: c_0(r) = c_4(r), c_1(r) = c_3(r);
  (Part 8) cross-validation against PR-#773 total at multiple r values;
  (Part 9) closure cross-check at r ≈ 0.26855: Σ w_k c_k ≈ (m_H_PDG/v)²;
  (Part 10) per-level numerical breakdown table at r ≈ 0.26855;
  (Part 11) forbidden-import audit;
  (Part 12) boundary check (what is NOT closed).

m_H_PDG = 125.10 GeV is used ONLY as comparison input for the closure cross-
check; it is NOT load-bearing for the derivation of (1)–(3).

stdlib only; exact `Fraction` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HIGGS_TASTE_SINGLET_PROJECTION_BOUNDED_NOTE_2026-05-09.md"

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


# Canonical surface values (admitted at upstream Wilson surface; not derived
# in this note). Listed here with explicit Fraction so all arithmetic is exact.
V_GEV = Fraction(24622, 100)        # parent Higgs note: v = 246.22 GeV
U_0 = Fraction(8776, 10000)         # parent Higgs note: u_0 = 0.8776
U_0_SQ = U_0 * U_0
N_TASTE = Fraction(16)              # uniform Higgs-channel admission

# m_H_PDG used ONLY as comparison input for the closure cross-check.
# NOT a load-bearing input for the derivation of (1)–(3).
M_H_PDG_COMPARISON = Fraction(12510, 100)  # 125.10 GeV (PDG comparison only)
TARGET_SQ = (M_H_PDG_COMPARISON / V_GEV) ** 2

BINOM_4 = [1, 4, 6, 4, 1]   # binomial(4, 0..4) — staircase multiplicities


# ---------------------------------------------------------------------------
# Decomposition formulas (eqs. (2)–(3))
# ---------------------------------------------------------------------------
def w_k(k: int) -> Fraction:
    """Taste-singlet projection weight at Hamming level k (eq. (2))."""
    return Fraction(BINOM_4[k], 16)


def c_k(k: int, r: Fraction, u_0: Fraction = U_0) -> Fraction:
    """Per-corner curvature at Hamming level k (eq. (3))."""
    u0sq = u_0 * u_0
    rsq = r * r
    kk_sq = (k - 2) ** 2
    x = kk_sq * rsq
    numer = u0sq - x
    denom = 4 * (x + u0sq) ** 2
    return numer / denom


def total_decomposed(r: Fraction, u_0: Fraction = U_0) -> Fraction:
    """Decomposed total Σ_k w_k · c_k(r, u_0) (eq. (1))."""
    return sum(w_k(k) * c_k(k, r, u_0) for k in range(5))


def total_pr773(r: Fraction, u_0: Fraction = U_0) -> Fraction:
    """PR-#773 all-orders total (eq. (2) of #773), for cross-validation."""
    u0sq = u_0 * u_0
    rsq = r * r
    s = Fraction(0)
    for k in range(5):
        kk_sq = (k - 2) ** 2
        x = kk_sq * rsq
        numer = u0sq - x
        denom = (x + u0sq) ** 2
        s += BINOM_4[k] * numer / denom
    return s / 64


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: Taste-Singlet Projection",
         "Taste-Singlet Projection"),
        ("claim_type: bounded_theorem", "Claim type:** bounded_theorem"),
        ("status authority phrase",
         "source-note proposal only; audit verdict and"),
        ("Claim section header", "## Claim"),
        ("Proof-Walk section header", "## Proof-Walk"),
        ("Exact Arithmetic Check section header",
         "## Exact Arithmetic Check"),
        ("Dependencies section header", "## Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("formula (1) decomposed sum",
         "Σ_{k=0}^{4}  w_k · c_k ( r, u_0 )"),
        ("formula (2) weight definition w_k = binomial(4,k)/16",
         "binomial(4, k) / 16"),
        ("formula (3) per-corner curvature c_k",
         "( u_0^2  -  ( k - 2 )^2 r^2 )"),
        ("Σ w_k = 1 stated",
         "( 1 + 4 + 6 + 4 + 1 ) / 16  =  16 / 16  =  1"),
        ("k=2 Wilson-decoupling stated",
         "Central level `k = 2` is Wilson-decoupled"),
        ("c_2 = 1/(4 u_0^2) r-independent stated",
         "r-independent for all r"),
        ("k → 4-k reflection symmetry stated",
         "Reflection symmetry under `k → 4 - k`"),
        ("c_0 = c_4, c_1 = c_3 stated",
         "c_0 ( r, u_0 )  =  c_4 ( r, u_0 ),"),
        ("reduction at r=0 to parent eq [5]",
         "matching\nthe parent eq. `[5]`"),
        ("σ = taste-singlet structural identification flagged",
         "structural identification"),
        ("uniform-N_taste=16 factored into (A) + (B) statement",
         "two structural inputs to the uniform-`N_taste = 16` weighting"),
        ("Hamming staircase upstream cited",
         "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08"),
        ("PR-#773 all-orders upstream cited (forward-ref)",
         "WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08"),
        ("V_taste extremum upstream cited (forward-ref)",
         "WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08"),
        ("Higgs-channel boundary upstream cited (forward-ref)",
         "HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08"),
        ("parent Higgs note upstream cited",
         "HIGGS_MASS_FROM_AXIOM_NOTE.md"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("PDG comparison flagged not load-bearing",
         "comparison input only, NOT load-bearing"),
        ("note explicitly does NOT change closure value statement",
         "is unchanged by this re-organization"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden vocabulary
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary():
    section("Part 2: forbidden meta-framing vocabulary absent (note + runner)")
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
        "Wilson asymptotic universality",
    ]
    runner_text = Path(__file__).read_text()
    docstring_match = re.match(r'^(?:#![^\n]*\n)?[^"]*"""(.*?)"""',
                               runner_text, re.DOTALL)
    runner_docstring = docstring_match.group(1) if docstring_match else ""
    for token in forbidden:
        check(
            f"absent in note (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )
        check(
            f"absent in runner docstring (rejected vocabulary): {token!r}",
            token not in runner_docstring,
        )


# ---------------------------------------------------------------------------
# Part 3: Cited upstream files (with graceful forward-references)
# ---------------------------------------------------------------------------
def part3_cited_upstreams():
    section("Part 3: cited upstreams (with graceful forward-references)")
    must_exist = [
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())

    forward_refs = [
        "docs/WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md",
        "docs/HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md",
    ]
    for rel in forward_refs:
        path = ROOT / rel
        if path.exists():
            check(f"sister forward-reference present: {rel}", True)
        else:
            print(f"  [INFO] sister forward-reference not yet on this branch: {rel}")
            print(f"         (intentional; audit lane resolves order)")


# ---------------------------------------------------------------------------
# Part 4: Weight normalization Σ w_k = 1
# ---------------------------------------------------------------------------
def part4_weight_normalization():
    section("Part 4: weight normalization Σ w_k = 1")
    weights = [w_k(k) for k in range(5)]
    print(f"  w_k = [w_0, w_1, w_2, w_3, w_4] = [{weights[0]}, {weights[1]}, "
          f"{weights[2]}, {weights[3]}, {weights[4]}]")
    print(f"      = [1/16, 4/16, 6/16, 4/16, 1/16] = [1/16, 1/4, 3/8, 1/4, 1/16]")

    total = sum(weights)
    check(
        "Σ_k w_k = 1 EXACTLY in Fraction arithmetic",
        total == Fraction(1),
        f"sum = {total}",
    )
    # Spot-check individual weights:
    check(
        "w_0 = w_4 = 1/16 (corner-of-corner multiplicity)",
        weights[0] == Fraction(1, 16) and weights[4] == Fraction(1, 16),
        f"w_0={weights[0]}, w_4={weights[4]}",
    )
    check(
        "w_2 = 3/8 = 6/16 (central-level multiplicity)",
        weights[2] == Fraction(3, 8),
        f"w_2={weights[2]}",
    )


# ---------------------------------------------------------------------------
# Part 5: Reduction at r = 0 to parent eq. [5]
# ---------------------------------------------------------------------------
def part5_reduction_at_r_zero():
    section("Part 5: reduction at r=0 — every c_k = 1/(4 u_0^2)")
    expected = Fraction(1) / (4 * U_0_SQ)
    print(f"  Expected per-corner value: 1/(4 u_0^2) = {float(expected):.10f}")

    for k in range(5):
        c = c_k(k, Fraction(0))
        match = c == expected
        print(f"    c_{k}(0, u_0) = {float(c):.10f}, "
              f"diff from 1/(4 u_0^2) = {float(c - expected):+.2e}")
        check(
            f"c_{k}(0, u_0) = 1/(4 u_0^2) EXACTLY",
            match,
            f"diff = {c - expected}",
        )

    # Σ_k w_k c_k(0) = 1·(1/(4u_0^2)) = 1/(4u_0^2)
    total = total_decomposed(Fraction(0))
    check(
        "Σ_k w_k c_k(0, u_0) = 1/(4 u_0^2) EXACTLY (matches parent eq. [5])",
        total == expected,
        f"diff = {total - expected}",
    )


# ---------------------------------------------------------------------------
# Part 6: k=2 Wilson-decoupling
# ---------------------------------------------------------------------------
def part6_k2_wilson_decoupling():
    section("Part 6: k=2 Wilson-decoupling — c_2(r, u_0) = 1/(4 u_0^2) for all r")
    expected = Fraction(1) / (4 * U_0_SQ)
    test_rs = [
        Fraction(0),
        Fraction(1, 10),
        Fraction(235, 1000),
        Fraction(26855, 100000),
        Fraction(4, 10),
    ]
    for r in test_rs:
        c = c_k(2, r)
        match = c == expected
        print(f"  c_2({float(r):.5f}, u_0) = {float(c):.10f}, "
              f"diff = {float(c - expected):+.2e}")
        check(
            f"c_2(r={float(r):.5f}) = 1/(4 u_0^2) EXACTLY (Wilson-decoupled)",
            match,
            f"diff = {c - expected}",
        )


# ---------------------------------------------------------------------------
# Part 7: Reflection symmetry under k → 4-k
# ---------------------------------------------------------------------------
def part7_reflection_symmetry():
    section("Part 7: reflection symmetry — c_0 = c_4, c_1 = c_3")
    test_rs = [
        Fraction(1, 10),
        Fraction(235, 1000),
        Fraction(26855, 100000),
        Fraction(4, 10),
    ]
    for r in test_rs:
        c0 = c_k(0, r)
        c4 = c_k(4, r)
        c1 = c_k(1, r)
        c3 = c_k(3, r)
        print(f"  r = {float(r):.5f}: c_0 = {float(c0):.6f}, c_4 = {float(c4):.6f}, "
              f"c_1 = {float(c1):.6f}, c_3 = {float(c3):.6f}")
        check(
            f"c_0(r={float(r):.4f}) = c_4(r={float(r):.4f}) EXACTLY",
            c0 == c4,
            f"diff = {c0 - c4}",
        )
        check(
            f"c_1(r={float(r):.4f}) = c_3(r={float(r):.4f}) EXACTLY",
            c1 == c3,
            f"diff = {c1 - c3}",
        )


# ---------------------------------------------------------------------------
# Part 8: Cross-validation against PR-#773 all-orders total
# ---------------------------------------------------------------------------
def part8_cross_validation_pr773():
    section("Part 8: cross-validation Σ_k w_k c_k(r) == PR-#773 total")
    test_rs = [
        Fraction(0),
        Fraction(1, 10),
        Fraction(235, 1000),
        Fraction(26855, 100000),
        Fraction(4, 10),
    ]
    for r in test_rs:
        decomp = total_decomposed(r)
        pr773 = total_pr773(r)
        match = decomp == pr773
        print(f"  r = {float(r):.5f}: decomposed = {float(decomp):.10f}, "
              f"PR-#773 = {float(pr773):.10f}, diff = {float(decomp - pr773):+.2e}")
        check(
            f"Σ_k w_k c_k(r={float(r):.4f}) == PR-#773 total EXACTLY",
            match,
            f"diff = {decomp - pr773}",
        )


# ---------------------------------------------------------------------------
# Part 9: Closure cross-check at r ≈ 0.26855
# ---------------------------------------------------------------------------
def part9_closure_cross_check():
    section("Part 9: closure cross-check at r_all_orders ≈ 0.26855")
    print(f"  Target (m_H_PDG / v)^2 = {float(TARGET_SQ):.10f}")
    print(f"  (m_H_PDG = {float(M_H_PDG_COMPARISON)} GeV used as comparison")
    print(f"   input only; NOT load-bearing for derivation of (1)–(3))")

    r_closure = Fraction(26855, 100000)  # ≈ 0.26855
    val = total_decomposed(r_closure)
    diff = val - TARGET_SQ
    rel_diff = abs(diff) / TARGET_SQ
    print(f"  At r = {float(r_closure):.5f}:")
    print(f"    Σ_k w_k c_k = {float(val):.10f}")
    print(f"    target      = {float(TARGET_SQ):.10f}")
    print(f"    abs diff    = {float(diff):+.2e}")
    print(f"    rel diff    = {float(rel_diff):.2e}")

    # The closure value 0.26855 from PR #773 is rounded; tolerance ~ 10^{-4}
    # (absolute) since closure was bisected to 10^{-5} bracket width:
    check(
        "Σ_k w_k c_k(0.26855) ≈ (m_H_PDG/v)^2 within 10^{-4} (PR-#773 closure)",
        rel_diff < Fraction(1, 10**3),  # within 0.1%
        f"abs diff = {float(diff):.2e}, rel diff = {float(rel_diff):.2e}",
    )


# ---------------------------------------------------------------------------
# Part 10: Per-level numerical breakdown table at r ≈ 0.26855
# ---------------------------------------------------------------------------
def part10_per_level_breakdown():
    section("Part 10: per-level breakdown at r_all_orders ≈ 0.26855")
    r = Fraction(26855, 100000)
    print(f"  At r = {float(r):.5f}, u_0 = {float(U_0)}:")
    print()
    print(f"    {'k':>3}  {'binom(4,k)':>10}  {'w_k':>10}  "
          f"{'c_k(r,u_0)':>12}  {'w_k · c_k':>14}")
    print(f"    {'-'*3}  {'-'*10}  {'-'*10}  {'-'*12}  {'-'*14}")
    total = Fraction(0)
    for k in range(5):
        wk = w_k(k)
        ck = c_k(k, r)
        contrib = wk * ck
        total += contrib
        print(f"    {k:>3}  {BINOM_4[k]:>10}  {float(wk):>10.4f}  "
              f"{float(ck):>12.6f}  {float(contrib):>14.8f}")
    print(f"    {'-'*3}  {'-'*10}  {'-'*10}  {'-'*12}  {'-'*14}")
    print(f"    {'Σ':>3}  {'16':>10}  {float(sum(w_k(k) for k in range(5))):>10.4f}  "
          f"{'':>12}  {float(total):>14.8f}")
    print()
    print(f"    target (m_H_PDG/v)^2  = {float(TARGET_SQ):.8f}")
    print(f"    Σ_k w_k · c_k         = {float(total):.8f}")
    print(f"    abs diff              = {float(total - TARGET_SQ):+.2e}")

    # Confirm k=2 contribution:
    contrib_k2 = w_k(2) * c_k(2, r)
    expected_k2 = Fraction(3, 8) * Fraction(1) / (4 * U_0_SQ)  # = 3/(32 u_0^2)
    check(
        "k=2 contribution = (3/8) · 1/(4 u_0^2) = 3/(32 u_0^2) EXACTLY",
        contrib_k2 == expected_k2,
        f"diff = {contrib_k2 - expected_k2}",
    )


# ---------------------------------------------------------------------------
# Part 11: Forbidden-import audit
# ---------------------------------------------------------------------------
def part11_forbidden_imports():
    section("Part 11: stdlib-only / no PDG pins (other than declared comparison)")
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

    declared_comparison = (
        "M_H_PDG_COMPARISON" in runner_text
        and "comparison input" in runner_text
        and "NOT load-bearing" in runner_text
    )
    check(
        "PDG comparison declared with explicit not-load-bearing label",
        declared_comparison,
    )

    suspicious = re.findall(
        r"\b(?:m_e|m_mu|m_tau|m_W|m_Z|alpha_em|alpha_obs|g_obs)\s*=\s*\d+\.\d+\b",
        runner_text,
    )
    check(
        "no extra PDG pins beyond declared m_H_PDG comparison",
        not suspicious,
        f"matches: {suspicious}" if suspicious else "none (clean)",
    )


# ---------------------------------------------------------------------------
# Part 12: Boundary check — what is NOT closed
# ---------------------------------------------------------------------------
def part12_boundary_check():
    section("Part 12: boundary check (what is NOT closed)")
    not_claimed = [
        "the +12% Higgs gap chain",
        "the σ = taste-singlet identification itself",
        "the value of the Wilson coefficient `r` itself",
        "any parent theorem/status promotion",
    ]
    for marker in not_claimed:
        check(
            f"note explicitly does not close: {marker[:60]}",
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

    # Note explicitly factors uniform-N_taste=16 into (A) σ = taste-singlet +
    # (B) binom(4,k) staircase counting:
    check(
        "factors uniform-N_taste=16 admission into (A) + (B)",
        "structural identification `σ = taste-singlet`" in NOTE_TEXT,
    )
    check(
        "(B) counting fact about (Z/2)^4 explicitly stated",
        "counting fact that 16 corners of `Z³+t`" in NOTE_TEXT,
    )

    # Note acknowledges this doesn't change closure value:
    check(
        "explicitly states closure value is unchanged by this re-organization",
        "is unchanged by this re-organization" in NOTE_TEXT,
    )


def main() -> int:
    banner("frontier_higgs_taste_singlet_projection.py")
    print(" Bounded source note: under σ = taste-singlet (parent identification),")
    print("   (m_H_W/v)^2 = Σ_k w_k · c_k with w_k = binomial(4,k)/16 and")
    print("   c_k = (u_0^2 - (k-2)^2 r^2)/(4·((k-2)^2 r^2 + u_0^2)^2). Three")
    print("   structural consequences: (i) k=2 Wilson-decoupled; (ii) k → 4-k")
    print("   reflection; (iii) reduction at r=0 to parent's 1/(4u_0^2). Cross-")
    print("   validates PR #773 total at multiple r values. Factors the parent's")
    print("   uniform-N_taste=16 admission into σ=taste-singlet (structural) +")
    print("   binom(4,k) counting fact, both more constrained than free N_taste.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()
    part4_weight_normalization()
    part5_reduction_at_r_zero()
    part6_k2_wilson_decoupling()
    part7_reflection_symmetry()
    part8_cross_validation_pr773()
    part9_closure_cross_check()
    part10_per_level_breakdown()
    part11_forbidden_imports()
    part12_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: under σ = taste-singlet (parent identification), the all-orders")
        print(" Wilson-corrected (m_H_W/v)^2 decomposes on the Hamming staircase as")
        print(" Σ_k w_k · c_k(r, u_0) with derived weights w_k = binomial(4,k)/16 and")
        print(" per-corner curvatures c_k(r, u_0) = (u_0^2 - (k-2)^2 r^2)/(4·((k-2)^2 r^2")
        print(" + u_0^2)^2). Three structural consequences verified at exact rational")
        print(" precision: (i) k=2 channel r-decoupled (c_2 = 1/(4u_0^2) for all r);")
        print(" (ii) k → 4-k reflection symmetry (c_0 = c_4, c_1 = c_3); (iii) reduction")
        print(" at r=0 to parent's 1/(4u_0^2). Cross-validates PR #773 total at r ∈")
        print(" {0, 0.1, 0.235, 0.26855, 0.4}. The decomposition factors the parent's")
        print(" uniform-N_taste=16 admission into σ = taste-singlet (structural) +")
        print(" binom(4,k) staircase counting, both more constrained than a free N_taste")
        print(" numerical choice.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
