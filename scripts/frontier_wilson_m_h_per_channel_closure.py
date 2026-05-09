#!/usr/bin/env python3
"""Wilson m_H per-channel closure values — bounded source-note runner.

Verifies docs/WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md:

For each subset S of the Hamming-weight classes {0, 1, 2, 3, 4} on the 16
BZ corners of Z^3 + t (APBC, L = 2), with multiplicities binomial(4, k) =
(1, 4, 6, 4, 1), the per-channel readout under the all-orders Wilson
curvature at m^* = -4r is

  ( m_H_W / v )^2_(S)
     = ( 1 / ( 4 · N_taste^(eff)(S) ) ) · Σ_{k ∈ S} binomial(4, k) ·
         ( u_0^2 - (k - 2)^2 r^2 ) / ( (k - 2)^2 r^2 + u_0^2 )^2          (S)

with N_taste^(eff)(S) = Σ_{k ∈ S} binomial(4, k). The choice of S is the
"channel identification". This runner verifies four cases:

  S = {2}      (k=2-only):       r-independent; no closure
  S = {0, 4}   (k=0,4 paired):    closure r_{0,4} ≈ 0.12192
  S = {1, 3}   (k=1,3 paired):    closure r_{1,3} ≈ 0.24383
  S = {0..4}   (uniform-16):      closure r_{16}  ≈ 0.26855  (sister-note ref)

The runner verifies, at exact rational precision via fractions.Fraction:
  (Part 1) note structure;
  (Part 2) forbidden-vocabulary absence;
  (Part 3) cited upstreams (with graceful forward-references);
  (Part 4) per-channel formulas at r = 0 reduce to parent eq. [5] = 1/(4 u_0^2);
  (Part 5) S = {2} is r-independent; no closure to the comparison target;
  (Part 6) S = {0, 4} bisection on bracket [0.12, 0.14] in Fraction
           arithmetic; converges to r_{0,4} ≈ 0.12192 ± 10^{-5};
  (Part 7) S = {1, 3} bisection on bracket [0.22, 0.25]; converges to
           r_{1,3} ≈ 0.24383 ± 10^{-5};
  (Part 8) rescaling identity r_{1,3} = 2 · r_{0,4} verified at bisection
           precision;
  (Part 9) S = {0..4} uniform-16 cross-check on bracket [0.26, 0.28];
           reproduces r_{16} ≈ 0.26855 of the sister all-orders note;
  (Part 10) per-channel ordering r_{0,4} < r_{1,3} < r_{16};
  (Part 11) validity-boundary check (each closure value < its perturbative
            radius);
  (Part 12) forbidden-import audit (stdlib only, no PDG pins beyond declared
            comparison);
  (Part 13) boundary check (what is NOT closed).

m_H_PDG = 125.10 GeV is used ONLY as a comparison input for the closure-
value computation; it is NOT load-bearing for the derivation of the
per-channel formulas.

stdlib only; exact `Fraction` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md"

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

# m_H_PDG used ONLY as comparison input for the closure-value computation.
# This is NOT a load-bearing input for the derivation of the per-channel
# formulas.
M_H_PDG_COMPARISON = Fraction(12510, 100)  # 125.10 GeV (PDG comparison only)
TARGET_SQ = (M_H_PDG_COMPARISON / V_GEV) ** 2

BINOM_4 = [1, 4, 6, 4, 1]   # binomial(4, 0..4) — staircase multiplicities


# ---------------------------------------------------------------------------
# Per-channel readout (m_H_W / v)^2_(S) for an arbitrary subset S of {0..4}
# ---------------------------------------------------------------------------
def per_channel_readout(r: Fraction, S: list[int],
                        u_0: Fraction = U_0) -> Fraction:
    """(m_H_W / v)^2_(S) = (1/(4 N_eff)) · Σ_{k in S} binom(4,k) ·
       (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2."""
    u0sq = u_0 * u_0
    rsq = r * r
    N_eff = sum(BINOM_4[k] for k in S)
    if N_eff == 0:
        raise ValueError("S must be non-empty")
    total = Fraction(0)
    for k in S:
        kk_sq = (k - 2) ** 2
        x = kk_sq * rsq
        numer = u0sq - x
        denom = (x + u0sq) ** 2
        total += BINOM_4[k] * numer / denom
    return total / (4 * N_eff)


def bisect_for_closure(S: list[int], lo: Fraction, hi: Fraction,
                       tol: Fraction = Fraction(1, 10**8),
                       max_iter: int = 200) -> tuple[Fraction, int, Fraction]:
    """Bisect (m_H_W/v)^2_(S) - TARGET = 0 on [lo, hi]. Returns (r_mid, iters,
    final width)."""
    f_lo = per_channel_readout(lo, S) - TARGET_SQ
    f_hi = per_channel_readout(hi, S) - TARGET_SQ
    if f_lo * f_hi >= 0:
        raise ValueError(
            f"Bracket [{float(lo):.4f}, {float(hi):.4f}] does not have "
            f"opposite-sign endpoints for S={S}: "
            f"f(lo)={float(f_lo):+.6f}, f(hi)={float(f_hi):+.6f}"
        )
    iters = 0
    while hi - lo > tol and iters < max_iter:
        mid = (lo + hi) / 2
        f_mid = per_channel_readout(mid, S) - TARGET_SQ
        if f_mid * f_lo > 0:
            lo = mid
            f_lo = f_mid
        else:
            hi = mid
            f_hi = f_mid
        iters += 1
    return (lo + hi) / 2, iters, hi - lo


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: Per-Channel Closure",
         "Per-Channel Closure"),
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
        ("formula (S) per-channel readout",
         "( 1 / ( 4 · N_taste^(eff)(S) ) ) · Σ_{k ∈ S}"),
        ("S = {2} k=2-only stated r-independent",
         "CONSTANT in r"),
        ("S = {0, 4} formula stated",
         "( u_0^2 - 4 r^2 )"),
        ("S = {1, 3} formula stated",
         "( u_0^2 - r^2 )"),
        ("k=2-only no closure stated",
         "no closure to TARGET"),
        ("k04 closure value 0.12192 stated",
         "0.12192"),
        ("k13 closure value 0.24383 stated",
         "0.24383"),
        ("uniform-16 closure value 0.26855 stated (sister ref)",
         "0.26855"),
        ("rescaling identity r_{1,3} = 2 r_{0,4} stated",
         "r_{1,3} ≈ 2 · r_{0,4}"),
        ("rescaling derivation: (k-2)^2 = 4 vs 1 stated",
         "(where `(k - 2)^2 = 4`)"),
        ("uniform-N_taste=16 admission cited as one identification",
         "uniform-`N_taste = 16`"),
        ("non-derived flag on identification",
         "non-derived"),
        ("validity boundary u_0 / 2 for k=0,4 stated",
         "r < u_0 / 2"),
        ("validity boundary u_0 for k=1,3 stated",
         "r < u_0`"),
        ("ratio 0.278 to boundary stated",
         "≈ 0.278"),
        ("all-orders sister upstream cited",
         "WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08"),
        ("V_taste^W extremum upstream cited (sister)",
         "WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08"),
        ("V_taste^W formula upstream cited (sister)",
         "WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08"),
        ("Wilson staircase upstream cited",
         "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08"),
        ("Higgs note upstream cited",
         "HIGGS_MASS_FROM_AXIOM_NOTE.md"),
        ("Higgs-channel boundary upstream cited (sister)",
         "HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("PDG comparison input flagged not-load-bearing",
         "comparison input only"),
        ("not-load-bearing label explicit",
         "**not load-\nbearing**"),
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
    # Extract the runner's module docstring (the prose at the top) — this
    # is where stray meta-framing language would actually appear, NOT in
    # the `forbidden = [...]` list literal below.
    runner_text = Path(__file__).read_text()
    docstring_match = re.match(r'^(?:#![^\n]*\n)?[^"]*"""(.*?)"""',
                               runner_text, re.DOTALL)
    runner_docstring = docstring_match.group(1) if docstring_match else ""

    for token in forbidden:
        in_note = token in NOTE_TEXT
        in_runner_docstring = token in runner_docstring
        check(
            f"absent in note (rejected vocabulary): {token!r}",
            not in_note,
        )
        check(
            f"absent in runner docstring (rejected vocabulary): {token!r}",
            not in_runner_docstring,
        )


# ---------------------------------------------------------------------------
# Part 3: Cited upstream files (with graceful forward-references)
# ---------------------------------------------------------------------------
def part3_cited_upstreams():
    section("Part 3: cited upstreams (with graceful forward-references)")
    must_exist = [
        "docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md",
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())

    forward_refs = [
        "docs/WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md",
    ]
    for rel in forward_refs:
        path = ROOT / rel
        if path.exists():
            check(f"sister forward-reference present: {rel}", True)
        else:
            print(f"  [INFO] sister forward-reference not yet on this branch: {rel}")
            print(f"         (intentional; audit lane resolves order)")


# ---------------------------------------------------------------------------
# Part 4: Per-channel formulas at r = 0 reduce to parent eq. [5]
# ---------------------------------------------------------------------------
def part4_reduction_at_r_zero():
    section("Part 4: per-channel formulas at r = 0 reduce to parent eq. [5]")
    expected = Fraction(1) / (4 * U_0_SQ)
    print(f"  parent eq. [5]: 1/(4 u_0^2) = {float(expected):.10f}")
    print(f"  ((m_H_zero/v)^2 = (1/(2 u_0))^2 = {float(expected):.10f})")
    print()

    cases = [
        ("S = {2} (k=2-only)", [2]),
        ("S = {0, 4}", [0, 4]),
        ("S = {1, 3}", [1, 3]),
        ("S = {0..4} (uniform-16)", [0, 1, 2, 3, 4]),
        ("S = {0}", [0]),
        ("S = {1}", [1]),
        ("S = {3}", [3]),
        ("S = {4}", [4]),
        ("S = {0, 1, 4}", [0, 1, 4]),
    ]
    for label, S in cases:
        val = per_channel_readout(Fraction(0), S)
        N_eff = sum(BINOM_4[k] for k in S)
        check(
            f"{label} at r=0 equals 1/(4 u_0^2) EXACTLY (N_eff={N_eff})",
            val == expected,
            f"diff = {val - expected}",
        )


# ---------------------------------------------------------------------------
# Part 5: S = {2} is r-independent; no closure
# ---------------------------------------------------------------------------
def part5_k2_only_r_independent():
    section("Part 5: S = {2} (k=2-only) is r-independent; no closure")
    expected = Fraction(1) / (4 * U_0_SQ)
    print(f"  Constant value 1/(4 u_0^2) = {float(expected):.10f}")
    print(f"  Target (m_H_PDG/v)^2       = {float(TARGET_SQ):.10f}")
    print(f"  Gap (constant - target)    = {float(expected - TARGET_SQ):+.10f}")
    print()

    test_rs = [
        Fraction(0),
        Fraction(1, 100),
        Fraction(1, 10),
        Fraction(2, 10),
        Fraction(3, 10),
        Fraction(4, 10),
        Fraction(5, 10),
        Fraction(8776, 10000),  # u_0
        Fraction(1),
    ]
    for r in test_rs:
        val = per_channel_readout(r, [2])
        check(
            f"  S={{2}} at r={float(r):.4f} equals 1/(4 u_0^2) EXACTLY (r-independent)",
            val == expected,
        )

    # r-independent at the algebraic level: at k=2, (k-2)^2 = 0, so the
    # summand is binom(4,2) · u_0^2 / u_0^4 = 6/u_0^2; divide by 4·6 = 24
    # gives 1/(4 u_0^2).
    summand_at_k2 = BINOM_4[2] * U_0_SQ / (U_0_SQ ** 2)
    expected_summand = Fraction(6) / U_0_SQ
    check(
        "S={2} algebraic verification: summand = 6/u_0^2",
        summand_at_k2 == expected_summand,
    )
    check(
        "S={2} algebraic verification: 6/u_0^2 / (4 · 6) = 1/(4 u_0^2)",
        summand_at_k2 / (4 * BINOM_4[2]) == expected,
    )

    # No closure: |constant - target| stays positive forever
    gap = expected - TARGET_SQ
    check(
        "S={2} does not close to target: 1/(4 u_0^2) > (m_H_PDG/v)^2 (the +12% gap)",
        gap > 0,
        f"gap = {float(gap):+.6f}",
    )

    # The +12% gap interpretation: m_H_zero / m_H_PDG ≈ 1.12
    m_H_zero = V_GEV / (2 * U_0)
    ratio = m_H_zero / M_H_PDG_COMPARISON
    print(f"  m_H_zero / m_H_PDG = {float(ratio):.4f} (the canonical +12% gap)")
    check(
        "+12% gap canonically present: m_H_zero / m_H_PDG > 1.12",
        ratio > Fraction(112, 100),
        f"ratio = {float(ratio):.4f}",
    )


# ---------------------------------------------------------------------------
# Part 6: S = {0, 4} bisection on bracket [0.12, 0.14]
# ---------------------------------------------------------------------------
def part6_k04_bisection() -> Fraction:
    section("Part 6: S = {0, 4} bisection on bracket [0.12, 0.14]")
    S = [0, 4]
    lo = Fraction(12, 100)   # 0.12
    hi = Fraction(14, 100)   # 0.14

    f_lo = per_channel_readout(lo, S) - TARGET_SQ
    f_hi = per_channel_readout(hi, S) - TARGET_SQ
    print(f"  f(lo = {float(lo):.4f}) = {float(f_lo):+.6f}")
    print(f"  f(hi = {float(hi):.4f}) = {float(f_hi):+.6f}")
    check(
        "bracket endpoint sign change: f(0.12) > 0 and f(0.14) < 0",
        f_lo > 0 and f_hi < 0,
        f"f(0.12) = {float(f_lo):+.6f}, f(0.14) = {float(f_hi):+.6f}",
    )

    r_k04, iters, width = bisect_for_closure(S, lo, hi)
    print()
    print(f"  After {iters} bisection iterations:")
    print(f"    bracket width = {float(width):.2e}")
    print(f"    midpoint r_{{0,4}} = {float(r_k04):.10f}")
    print(f"    (m_H_W/v)^2_({{0,4}}) at result = "
          f"{float(per_channel_readout(r_k04, S)):.10f}")
    print(f"    target                    = {float(TARGET_SQ):.10f}")

    check(
        "bisection converges (bracket width ≤ 10^{-5})",
        width <= Fraction(1, 10**5),
        f"width = {float(width):.2e}",
    )

    note_claimed = Fraction(12192, 100000)
    diff_claim = abs(r_k04 - note_claimed)
    check(
        "bisection result within 10^{-4} of note's claimed 0.12192",
        diff_claim < Fraction(1, 10**4),
        f"|result - 0.12192| = {float(diff_claim):.2e}",
    )

    val_at_result = per_channel_readout(r_k04, S)
    diff_target = abs(val_at_result - TARGET_SQ)
    check(
        "(m_H_W/v)^2_({0,4}) at result matches target to < 10^{-7}",
        diff_target < Fraction(1, 10**7),
        f"|(m_H_W/v)^2(result) - target| = {float(diff_target):.2e}",
    )

    # Cross-check: explicit closed-form formula for S = {0, 4}:
    #   (m_H_W/v)^2_({0,4}) = (u_0^2 - 4 r^2) / (4 · (4 r^2 + u_0^2)^2)
    rsq = r_k04 * r_k04
    explicit = (U_0_SQ - 4 * rsq) / (4 * (4 * rsq + U_0_SQ) ** 2)
    check(
        "explicit closed form for S={0,4} matches general per-channel readout",
        per_channel_readout(r_k04, S) == explicit,
    )

    return r_k04


# ---------------------------------------------------------------------------
# Part 7: S = {1, 3} bisection on bracket [0.22, 0.25]
# ---------------------------------------------------------------------------
def part7_k13_bisection() -> Fraction:
    section("Part 7: S = {1, 3} bisection on bracket [0.22, 0.25]")
    S = [1, 3]
    lo = Fraction(22, 100)   # 0.22
    hi = Fraction(25, 100)   # 0.25

    f_lo = per_channel_readout(lo, S) - TARGET_SQ
    f_hi = per_channel_readout(hi, S) - TARGET_SQ
    print(f"  f(lo = {float(lo):.4f}) = {float(f_lo):+.6f}")
    print(f"  f(hi = {float(hi):.4f}) = {float(f_hi):+.6f}")
    check(
        "bracket endpoint sign change: f(0.22) > 0 and f(0.25) < 0",
        f_lo > 0 and f_hi < 0,
        f"f(0.22) = {float(f_lo):+.6f}, f(0.25) = {float(f_hi):+.6f}",
    )

    r_k13, iters, width = bisect_for_closure(S, lo, hi)
    print()
    print(f"  After {iters} bisection iterations:")
    print(f"    bracket width = {float(width):.2e}")
    print(f"    midpoint r_{{1,3}} = {float(r_k13):.10f}")
    print(f"    (m_H_W/v)^2_({{1,3}}) at result = "
          f"{float(per_channel_readout(r_k13, S)):.10f}")
    print(f"    target                    = {float(TARGET_SQ):.10f}")

    check(
        "bisection converges (bracket width ≤ 10^{-5})",
        width <= Fraction(1, 10**5),
        f"width = {float(width):.2e}",
    )

    note_claimed = Fraction(24383, 100000)
    diff_claim = abs(r_k13 - note_claimed)
    check(
        "bisection result within 10^{-4} of note's claimed 0.24383",
        diff_claim < Fraction(1, 10**4),
        f"|result - 0.24383| = {float(diff_claim):.2e}",
    )

    val_at_result = per_channel_readout(r_k13, S)
    diff_target = abs(val_at_result - TARGET_SQ)
    check(
        "(m_H_W/v)^2_({1,3}) at result matches target to < 10^{-7}",
        diff_target < Fraction(1, 10**7),
        f"|(m_H_W/v)^2(result) - target| = {float(diff_target):.2e}",
    )

    # Explicit closed-form for S = {1, 3}:
    #   (m_H_W/v)^2_({1,3}) = (u_0^2 - r^2) / (4 · (r^2 + u_0^2)^2)
    rsq = r_k13 * r_k13
    explicit = (U_0_SQ - rsq) / (4 * (rsq + U_0_SQ) ** 2)
    check(
        "explicit closed form for S={1,3} matches general per-channel readout",
        per_channel_readout(r_k13, S) == explicit,
    )

    return r_k13


# ---------------------------------------------------------------------------
# Part 8: rescaling identity r_{1,3} = 2 · r_{0,4}
# ---------------------------------------------------------------------------
def part8_rescaling_identity(r_k04: Fraction, r_k13: Fraction):
    section("Part 8: rescaling identity r_{1,3} = 2 · r_{0,4}")
    # The (k-2)^2 r^2 terms are 4 r^2 for {0, 4} and 1 r^2 for {1, 3}.
    # Substituting r → 2 r in the {1, 3} formula gives the {0, 4} formula
    # exactly (modulo the binomial multiplicities, but the binomial cancels
    # against N_eff in the per-channel readout: binom(4, 0)/2 = 1/2 and
    # binom(4, 1)/8 = 1/2; identical). So r_{1,3} = 2 · r_{0,4}.
    print(f"  r_{{0,4}} = {float(r_k04):.10f}")
    print(f"  r_{{1,3}} = {float(r_k13):.10f}")
    print(f"  2 · r_{{0,4}} = {float(2 * r_k04):.10f}")
    print(f"  ratio r_{{1,3}} / r_{{0,4}} = {float(r_k13 / r_k04):.10f}")

    diff = abs(r_k13 - 2 * r_k04)
    check(
        "rescaling identity: |r_{1,3} - 2 · r_{0,4}| < 10^{-5}",
        diff < Fraction(1, 10**5),
        f"diff = {float(diff):.2e}",
    )
    check(
        "ratio r_{1,3} / r_{0,4} ≈ 2 within 10^{-4}",
        abs(r_k13 / r_k04 - 2) < Fraction(1, 10**4),
        f"ratio = {float(r_k13 / r_k04):.6f}",
    )

    # Algebraic substitution check: per-channel readout for {1, 3} at r
    # equals per-channel readout for {0, 4} at r/2 — verify directly.
    # Pick a few r values:
    for r_test in [Fraction(1, 10), Fraction(2, 10), Fraction(3, 10),
                   r_k13]:
        val_13 = per_channel_readout(r_test, [1, 3])
        val_04 = per_channel_readout(r_test / 2, [0, 4])
        check(
            f"  algebraic identity at r={float(r_test):.4f}: "
            f"(m_H/v)^2_{{1,3}}(r) == (m_H/v)^2_{{0,4}}(r/2)",
            val_13 == val_04,
            f"diff = {val_13 - val_04}",
        )


# ---------------------------------------------------------------------------
# Part 9: S = {0..4} uniform-16 cross-check (sister-note value 0.26855)
# ---------------------------------------------------------------------------
def part9_uniform16_cross_check() -> Fraction:
    section("Part 9: S = {0..4} uniform-16 cross-check (sister r_{16} ≈ 0.26855)")
    S = [0, 1, 2, 3, 4]
    lo = Fraction(26, 100)   # 0.26
    hi = Fraction(28, 100)   # 0.28

    f_lo = per_channel_readout(lo, S) - TARGET_SQ
    f_hi = per_channel_readout(hi, S) - TARGET_SQ
    print(f"  f(lo = {float(lo):.4f}) = {float(f_lo):+.6f}")
    print(f"  f(hi = {float(hi):.4f}) = {float(f_hi):+.6f}")
    check(
        "bracket endpoint sign change: f(0.26) > 0 and f(0.28) < 0",
        f_lo > 0 and f_hi < 0,
    )

    r_16, iters, width = bisect_for_closure(S, lo, hi)
    print()
    print(f"  After {iters} bisection iterations:")
    print(f"    midpoint r_{{16}} = {float(r_16):.10f}")
    print(f"    sister-note value: 0.26855")

    check(
        "bisection converges (bracket width ≤ 10^{-5})",
        width <= Fraction(1, 10**5),
    )

    sister_value = Fraction(26855, 100000)
    diff = abs(r_16 - sister_value)
    check(
        "uniform-16 closure matches sister all-orders note value 0.26855",
        diff < Fraction(1, 10**4),
        f"|r_{{16}} - 0.26855| = {float(diff):.2e}",
    )

    # Sanity: the uniform-16 form is also the (1/64) Σ form from the sister:
    sister_form_at_r16 = Fraction(0)
    rsq = r_16 * r_16
    for k in range(5):
        kk_sq = (k - 2) ** 2
        x = kk_sq * rsq
        sister_form_at_r16 += BINOM_4[k] * (U_0_SQ - x) / (x + U_0_SQ) ** 2
    sister_form_at_r16 /= 64
    general_form = per_channel_readout(r_16, S)
    check(
        "general per-channel readout at S=full equals sister (1/64) Σ form",
        general_form == sister_form_at_r16,
    )

    return r_16


# ---------------------------------------------------------------------------
# Part 10: per-channel ordering r_{0,4} < r_{1,3} < r_{16}
# ---------------------------------------------------------------------------
def part10_per_channel_ordering(r_k04: Fraction, r_k13: Fraction,
                                r_16: Fraction):
    section("Part 10: per-channel ordering r_{0,4} < r_{1,3} < r_{16}")
    print(f"  r_{{0,4}} = {float(r_k04):.10f}")
    print(f"  r_{{1,3}} = {float(r_k13):.10f}")
    print(f"  r_{{16}}  = {float(r_16):.10f}")
    check(
        "ordering: r_{0,4} < r_{1,3}",
        r_k04 < r_k13,
        f"r_{{0,4}} = {float(r_k04):.5f}, r_{{1,3}} = {float(r_k13):.5f}",
    )
    check(
        "ordering: r_{1,3} < r_{16}",
        r_k13 < r_16,
        f"r_{{1,3}} = {float(r_k13):.5f}, r_{{16}} = {float(r_16):.5f}",
    )
    check(
        "no closure for S = {2} (r-independent constant readout)",
        per_channel_readout(Fraction(0), [2])
        == per_channel_readout(Fraction(1, 2), [2]),
    )


# ---------------------------------------------------------------------------
# Part 11: validity-boundary check (each closure < perturbative radius)
# ---------------------------------------------------------------------------
def part11_validity_boundaries(r_k04: Fraction, r_k13: Fraction,
                               r_16: Fraction):
    section("Part 11: validity-boundary check")
    # For S = {0, 4}, the dominant Taylor parameter is x = 4 r^2; convergence
    # requires 4 r^2 < u_0^2, i.e., r < u_0/2.
    boundary_04 = U_0 / 2
    # For S = {1, 3}, the dominant Taylor parameter is x = r^2; convergence
    # requires r^2 < u_0^2, i.e., r < u_0.
    boundary_13 = U_0
    # For S = {0..4}, the dominant Taylor parameter is set by the k=0,4
    # summands (largest (k-2)^2 = 4); same as S = {0, 4}: r < u_0 / 2.
    boundary_16 = U_0 / 2

    print(f"  S={{0,4}} boundary: u_0/2 = {float(boundary_04):.6f}")
    print(f"     r_{{0,4}} = {float(r_k04):.6f}; ratio = {float(r_k04/boundary_04):.4f}")
    print(f"  S={{1,3}} boundary: u_0   = {float(boundary_13):.6f}")
    print(f"     r_{{1,3}} = {float(r_k13):.6f}; ratio = {float(r_k13/boundary_13):.4f}")
    print(f"  S={{16}}  boundary: u_0/2 = {float(boundary_16):.6f}")
    print(f"     r_{{16}}  = {float(r_16):.6f}; ratio = {float(r_16/boundary_16):.4f}")

    check(
        "S={0,4}: r_{0,4} < u_0/2 (within perturbative-Taylor radius)",
        r_k04 < boundary_04,
    )
    check(
        "S={1,3}: r_{1,3} < u_0 (within perturbative-Taylor radius)",
        r_k13 < boundary_13,
    )
    check(
        "S={16}: r_{16} < u_0/2 (within perturbative-Taylor radius)",
        r_16 < boundary_16,
    )

    # The ratio r/boundary should be the SAME for {0,4} and {1,3} as a
    # consequence of the rescaling identity r_{1,3} = 2 r_{0,4} and
    # boundary_13 = 2 boundary_04:
    ratio_04 = r_k04 / boundary_04
    ratio_13 = r_k13 / boundary_13
    diff = abs(ratio_04 - ratio_13)
    check(
        "dimensionless ratio r/boundary equal for {0,4} and {1,3} "
        "(rescaling identity)",
        diff < Fraction(1, 10**5),
        f"ratio_{{0,4}} = {float(ratio_04):.5f}, "
        f"ratio_{{1,3}} = {float(ratio_13):.5f}",
    )
    check(
        "dimensionless ratio ≈ 0.278 for {0,4} and {1,3}",
        abs(ratio_04 - Fraction(278, 1000)) < Fraction(1, 100),
        f"computed ratio = {float(ratio_04):.4f}",
    )


# ---------------------------------------------------------------------------
# Part 12: forbidden-import audit
# ---------------------------------------------------------------------------
def part12_forbidden_imports():
    section("Part 12: stdlib-only / no PDG pins (other than declared comparison)")
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

    # The runner declares m_H_PDG = 125.10 as an EXPLICIT comparison input.
    declared_comparison = (
        "M_H_PDG_COMPARISON" in runner_text
        and "comparison input" in runner_text
        and "NOT load-bearing" in runner_text
    )
    check(
        "PDG comparison declared with explicit not-load-bearing label",
        declared_comparison,
    )

    # Check no OTHER PDG-style pins appear (m_e, m_mu, alpha, etc.)
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
# Part 13: boundary check — what is NOT closed
# ---------------------------------------------------------------------------
def part13_boundary_check():
    section("Part 13: boundary check (what is NOT closed)")
    not_claimed = [
        "the +12 % Higgs gap chain",
        "the Higgs-channel assignment itself",
        "the physical Higgs mass `m_H` numerical value",
        "the value of the Wilson coefficient `r` itself",
        "the plaquette mean-field link `u_0` numerical value",
        "the staggered-Dirac realization gate",
        "the `g_bare = 1` derivation",
        "any parent theorem/status promotion",
        "any claim that `S = {2}` (the central single-class Higgs",
        "the exact algebraic matching roots for `r`",
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

    # Conditional admissions:
    check(
        "matching values flagged as conditional on channel identification",
        "the chosen channel identification" in NOTE_TEXT,
    )
    check(
        "matching values flagged as conditional on tree-level mean-field",
        "tree-level mean-field formalism" in NOTE_TEXT,
    )
    check(
        "matching values flagged as conditional on non-zero r (not canonical KS)",
        "pure-Kogut-Susskind staggered setup" in NOTE_TEXT,
    )


def main() -> int:
    banner("frontier_wilson_m_h_per_channel_closure.py")
    print(" Bounded source note: per-channel closure values for the +12% Higgs gap")
    print("   under different channel identifications S of the Hamming-weight classes.")
    print("   S = {2}-only is r-independent (no closure).")
    print("   S = {0, 4} closes at r ≈ 0.12192.")
    print("   S = {1, 3} closes at r ≈ 0.24383 = 2 · r_{0,4} (rescaling identity).")
    print("   S = {0..4} uniform-16 closes at r ≈ 0.26855 (sister-note ref).")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()
    part4_reduction_at_r_zero()
    part5_k2_only_r_independent()
    r_k04 = part6_k04_bisection()
    r_k13 = part7_k13_bisection()
    part8_rescaling_identity(r_k04, r_k13)
    r_16 = part9_uniform16_cross_check()
    part10_per_channel_ordering(r_k04, r_k13, r_16)
    part11_validity_boundaries(r_k04, r_k13, r_16)
    part12_forbidden_imports()
    part13_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: per-channel closure values verified at exact rational")
        print(" precision. The k=2-only identification is r-independent (the closure")
        print(" mechanism breaks because the Wilson factor (k-2)^2 vanishes at k=2);")
        print(" no value of r closes the +12% gap in this channel. The k={0,4} and")
        print(" k={1,3} paired-class identifications close at r_{0,4} ≈ 0.12192 and")
        print(" r_{1,3} ≈ 0.24383 respectively (bisection precision ± 10^{-5}); the")
        print(" two are related by the algebraic-substitution identity r_{1,3} = 2 ·")
        print(" r_{0,4} at the matching-equation level. The uniform-16 identification")
        print(" reproduces the all-orders sister-note value r_{16} ≈ 0.26855. All")
        print(" matching readouts are conditional on (i) channel identification, (ii)")
        print(" tree-level mean-field, (iii) non-zero r — none of which is a derived")
        print(" value of the Wilson coefficient.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
