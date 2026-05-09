#!/usr/bin/env python3
"""Wilson-corrected m_H_tree at extremum, all orders in r — bounded source-note runner.

Verifies docs/WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md:

  ( m_H_tree^W / v )^2
     = (1 / 64) · Σ_{k=0}^{4} binomial(4, k) ·
         ( u_0^2 - (k - 2)^2 r^2 ) / ( (k - 2)^2 r^2 + u_0^2 )^2          (eq. (2))

This is the EXACT (all orders in r) closed form, derived from the curvature
at the Wilson-shifted extremum m^* = -4r (sister forward-reference) under
the parent's uniform-N_taste = 16 channel admission.

The runner verifies, at exact rational precision via fractions.Fraction:
  (Part 1) note structure;
  (Part 2) forbidden-vocabulary absence;
  (Part 3) cited upstreams (with graceful forward-references);
  (Part 4) reduction at r = 0: each summand → 1/u_0^2; sum → 16/u_0^2; /64 →
           1/(4 u_0^2); matches parent eq. [5];
  (Part 5) reduction to PR-#761's leading order at small r: extracts the
           coefficient -3/4 of r^2/u_0^4 in the Taylor expansion at small r,
           verifying the all-orders form contains PR-#761 as its leading
           contribution;
  (Part 6) bisection on bracket [0.26, 0.28] in Fraction arithmetic; verifies
           bracket-endpoint sign change and converges to r_all_orders ≈
           0.26855 ± 10^{-5};
  (Part 7) comparison to leading-order linear-form value r_leading ≈ 0.23572:
           shift +13.9 %;
  (Part 8) perturbative-validity confirmation: r_all_orders < u_0 / 2 ≈ 0.439
           (radius of convergence boundary set by k = 0, 4 summands);
  (Part 9) forbidden-import audit (stdlib only, no PDG pins beyond declared
           comparison);
  (Part 10) boundary check (what is NOT closed).

m_H_PDG = 125.10 GeV is used ONLY as a comparison input for the closure-
value computation; it is NOT load-bearing for the derivation of (2).

stdlib only; exact `Fraction` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md"

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

# m_H_PDG used ONLY as comparison input for the closure-value computation.
# This is NOT a load-bearing input for the derivation of (2).
M_H_PDG_COMPARISON = Fraction(12510, 100)  # 125.10 GeV (PDG comparison only)
TARGET_SQ = (M_H_PDG_COMPARISON / V_GEV) ** 2

BINOM_4 = [1, 4, 6, 4, 1]   # binomial(4, 0..4) — staircase multiplicities


# ---------------------------------------------------------------------------
# Closed-form (m_H_W / v)^2 (eq. (2))
# ---------------------------------------------------------------------------
def m_H_W_squared_over_v_squared(r: Fraction, u_0: Fraction = U_0) -> Fraction:
    """Exact (m_H_tree^W / v)^2 from the all-orders closed form (eq. (2))."""
    u0sq = u_0 * u_0
    rsq = r * r
    total = Fraction(0)
    for k in range(5):
        kk_sq = (k - 2) ** 2
        x = kk_sq * rsq
        numer = u0sq - x
        denom = (x + u0sq) ** 2
        total += BINOM_4[k] * numer / denom
    return total / 64


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: All Orders in r",
         "All Orders in r"),
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
        ("formula (2) all-orders closed form",
         "( 1 / 64 ) · Σ_{k=0}^{4}  binomial(4, k)"),
        ("formula (3) sqrt form",
         "( v / 8 ) · sqrt"),
        ("reduction to 1/(4 u_0^2) at r=0 stated",
         "1 / (4 u_0^2)"),
        ("reduction to PR-#761 leading order at small r stated",
         "(1/(4u_0^2)) · (1 - 3 r^2 / u_0^2) + O(r^4)"),
        ("bisection bracket [0.26, 0.28] stated",
         "bracket `[0.26, 0.28]`"),
        ("all-orders closure value 0.26855 stated",
         "0.26855"),
        ("leading-order closure value 0.23572 cited",
         "0.23572"),
        ("relative shift 13.9% stated",
         "13.9 %"),
        ("validity boundary u_0 / 2 stated",
         "u_0 / 2 ≈ 0.439"),
        ("uniform-N_taste=16 admission cited",
         "uniform-`N_taste = 16`"),
        ("non-derived admission flagged",
         "non-derived"),
        ("V_taste^W extremum upstream cited (sister)",
         "WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08"),
        ("m_H_tree leading-order upstream cited (sister)",
         "WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08"),
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
         "comparison input only, not load-bearing"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden vocabulary
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary():
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
        "Wilson asymptotic universality",
    ]
    for token in forbidden:
        check(
            f"absent (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )


# ---------------------------------------------------------------------------
# Part 3: Cited upstream files (with graceful forward-references)
# ---------------------------------------------------------------------------
def part3_cited_upstreams():
    section("Part 3: cited upstreams (with graceful forward-references)")
    must_exist = [
        "docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md",
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())

    forward_refs = [
        "docs/WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md",
        "docs/WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md",
        "docs/HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md",
    ]
    for rel in forward_refs:
        path = ROOT / rel
        if path.exists():
            check(f"sister forward-reference present: {rel}", True)
        else:
            print(f"  [INFO] sister forward-reference not yet on this branch: {rel}")
            print(f"         (intentional; audit lane resolves order)")


# ---------------------------------------------------------------------------
# Part 4: Reduction at r = 0 to parent eq. [5] (1 / (4 u_0^2))
# ---------------------------------------------------------------------------
def part4_reduction_at_r_zero():
    section("Part 4: reduction at r = 0 to parent eq. [5] = 1/(4 u_0^2)")
    val_at_zero = m_H_W_squared_over_v_squared(Fraction(0))
    expected = Fraction(1) / (4 * U_0_SQ)
    print(f"  u_0 = {float(U_0)}, u_0^2 = {float(U_0_SQ):.6f}")
    print(f"  (m_H_W/v)^2 at r=0 (formula): {float(val_at_zero):.10f}")
    print(f"  parent eq. [5]:               1/(4 u_0^2) = {float(expected):.10f}")
    check(
        "(m_H_W/v)^2 at r=0 equals 1/(4 u_0^2) EXACTLY in Fraction arithmetic",
        val_at_zero == expected,
        f"diff = {val_at_zero - expected}",
    )

    # Inspect each summand at r=0:
    print("  Per-summand at r=0:")
    total_summands = Fraction(0)
    for k in range(5):
        kk_sq = (k - 2) ** 2
        x = kk_sq * 0
        numer = U_0_SQ - x
        denom = (x + U_0_SQ) ** 2
        summand = BINOM_4[k] * numer / denom
        total_summands += summand
        print(f"    k={k}: binom={BINOM_4[k]}, (k-2)^2={kk_sq}, "
              f"summand value = {float(summand):.6f}, "
              f"= binom*1/u_0^2 = {float(BINOM_4[k] * Fraction(1) / U_0_SQ):.6f}")
        check(
            f"  summand at r=0 for k={k} equals binom·1/u_0^2 EXACTLY",
            summand == BINOM_4[k] * Fraction(1) / U_0_SQ,
        )

    # Σ binom(4,k) = 16 (Hamming-staircase total state count):
    check(
        "Σ_k binomial(4, k) = 16 (staircase total state count)",
        sum(BINOM_4) == 16,
    )
    check(
        "Σ summands at r=0 = 16/u_0^2 EXACTLY",
        total_summands == Fraction(16) / U_0_SQ,
    )


# ---------------------------------------------------------------------------
# Part 5: Reduction to PR-#761's leading order at small r
# ---------------------------------------------------------------------------
def part5_reduction_to_leading_order():
    section("Part 5: reduction to PR-#761 leading-order form at small r")
    # PR #761's leading-order squared form:
    #   (m_H_W / v)^2_LO = (1 / (4 u_0^2)) · (1 - 3 r^2 / u_0^2)
    # We extract the coefficient of r^2 in the expansion of (m_H_W/v)^2 by
    # computing
    #   c(r) := ((m_H_W/v)^2(r) - (m_H_W/v)^2(0)) / r^2
    # at successively smaller r and verifying convergence to -3/(4 u_0^4).
    def lo_coeff_extract(r: Fraction) -> Fraction:
        val = m_H_W_squared_over_v_squared(r)
        val0 = Fraction(1) / (4 * U_0_SQ)  # value at r=0
        return (val - val0) / (r * r)

    expected_leading_coeff = -Fraction(3) / (4 * U_0_SQ * U_0_SQ)
    print(f"  Expected leading coefficient of r^2 (i.e., -3/(4 u_0^4)):"
          f" {float(expected_leading_coeff):.6f}")

    # As r → 0, the extracted coefficient → -3/(4 u_0^4):
    test_rs = [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000),
               Fraction(1, 10000)]
    extracted_history = []
    for r in test_rs:
        c = lo_coeff_extract(r)
        extracted_history.append((r, c))
        diff = c - expected_leading_coeff
        print(f"    r = {float(r):.0e}: c(r) = {float(c):.6f}, "
              f"diff from -3/(4u_0^4) = {float(diff):.6e}")

    # The smallest-r extracted coefficient should be very close:
    smallest_r, smallest_c = extracted_history[-1]
    diff_at_smallest = smallest_c - expected_leading_coeff
    check(
        "lim_{r→0} (m_H_W/v)^2 coefficient of r^2 equals -3/(4 u_0^4) [PR-#761]",
        abs(diff_at_smallest) < Fraction(1, 100) * abs(expected_leading_coeff),
        f"at r=10^-4: c = {float(smallest_c):.6f}, expected ≈ {float(expected_leading_coeff):.6f}, "
        f"diff = {float(diff_at_smallest):.4e}",
    )

    # As r → 0 the magnitude of the difference should DECREASE quadratically
    # (next-order coefficient is +5·40/u_0^6 / 64 = +25/(8 u_0^6) at r^4, so
    # c(r) ≈ -3/(4u_0^4) + (25/(8u_0^6)) r^2 + ...).
    diffs = [lo_coeff_extract(r) - expected_leading_coeff for r in test_rs]
    abs_diffs = [abs(float(d)) for d in diffs]
    print(f"  |c(r) - (-3/(4u_0^4))| as r decreases: "
          f"{[f'{d:.4e}' for d in abs_diffs]}")
    check(
        "|c(r) - leading| decreases monotonically as r → 0 (quadratic convergence)",
        all(abs_diffs[i] >= abs_diffs[i + 1] for i in range(len(abs_diffs) - 1)),
        f"abs_diffs = {abs_diffs}",
    )

    # Direct verification of next-order coefficient: coefficient of r^4 in
    # the Taylor expansion of (m_H_W/v)^2 should be +25/(8 u_0^6).
    # Check: (c(r) - leading) / r^2 → +25/(8 u_0^6).
    expected_r4_coeff = Fraction(25) / (8 * U_0_SQ ** 3)
    print(f"  Expected r^4 coefficient (+25/(8 u_0^6)): "
          f"{float(expected_r4_coeff):.6f}")
    r4_extracted = []
    for r in test_rs[:-1]:  # not 1e-4, where rounding hurts the extraction
        c = lo_coeff_extract(r)
        r4 = (c - expected_leading_coeff) / (r * r)
        r4_extracted.append((r, r4))
        print(f"    r = {float(r):.0e}: c_r4(r) = {float(r4):.6f}, "
              f"diff from +25/(8u_0^6) = {float(r4 - expected_r4_coeff):.4e}")
    smallest_r4_r, smallest_r4_c = r4_extracted[-1]
    check(
        "next-order coefficient of r^4 in (m_H_W/v)^2 equals +25/(8 u_0^6)",
        abs(smallest_r4_c - expected_r4_coeff) <
        Fraction(1, 100) * abs(expected_r4_coeff),
        f"at r=10^-3: c_r4 = {float(smallest_r4_c):.6f}, "
        f"expected ≈ {float(expected_r4_coeff):.6f}",
    )


# ---------------------------------------------------------------------------
# Part 6: Bisection for r_all_orders on [0.26, 0.28] in Fraction arithmetic
# ---------------------------------------------------------------------------
def part6_bisection_for_r_all_orders():
    section("Part 6: bisection for r_all_orders on [0.26, 0.28] (Fraction)")
    print(f"  Target: (m_H_PDG / v)^2 = ({float(M_H_PDG_COMPARISON)}/{float(V_GEV)})^2")
    print(f"           = {float(TARGET_SQ):.10f}  (PDG comparison input ONLY)")
    print()

    lo = Fraction(26, 100)   # 0.26
    hi = Fraction(28, 100)   # 0.28

    f_lo = m_H_W_squared_over_v_squared(lo) - TARGET_SQ
    f_hi = m_H_W_squared_over_v_squared(hi) - TARGET_SQ
    print(f"  f(lo = {float(lo):.4f}) = {float(f_lo):+.6f}")
    print(f"  f(hi = {float(hi):.4f}) = {float(f_hi):+.6f}")

    check(
        "bracket endpoint sign change: f(0.26) > 0 and f(0.28) < 0",
        f_lo > 0 and f_hi < 0,
        f"f(0.26) = {float(f_lo):+.6f}, f(0.28) = {float(f_hi):+.6f}",
    )

    # Bisect until bracket width <= 1e-8 (well below the claimed 10^{-5}):
    target_tol = Fraction(1, 10**8)
    iters = 0
    while hi - lo > target_tol and iters < 200:
        mid = (lo + hi) / 2
        f_mid = m_H_W_squared_over_v_squared(mid) - TARGET_SQ
        if f_mid > 0:
            lo = mid
        else:
            hi = mid
        iters += 1

    result = (lo + hi) / 2
    bracket_width = hi - lo

    print()
    print(f"  After {iters} bisection iterations:")
    print(f"    bracket = [{float(lo):.10f}, {float(hi):.10f}], "
          f"width = {float(bracket_width):.2e}")
    print(f"    midpoint r_all_orders = {float(result):.10f}")
    print(f"    (m_H_W/v)^2 at result = "
          f"{float(m_H_W_squared_over_v_squared(result)):.10f}")
    print(f"    target                = {float(TARGET_SQ):.10f}")

    check(
        "bisection converges (bracket width ≤ 10^{-5})",
        bracket_width <= Fraction(1, 10**5),
        f"width = {float(bracket_width):.2e}",
    )

    # Note's claimed value: r_all_orders ≈ 0.26855 ± 10^{-5}
    note_claimed = Fraction(26855, 100000)
    diff_claim = abs(result - note_claimed)
    check(
        "bisection result within 10^{-4} of note's claimed 0.26855",
        diff_claim < Fraction(1, 10**4),
        f"|result - 0.26855| = {float(diff_claim):.2e}",
    )

    # And the result, evaluated in the all-orders formula, should reproduce
    # the target to high precision (within floating-point):
    val_at_result = m_H_W_squared_over_v_squared(result)
    diff_target = abs(val_at_result - TARGET_SQ)
    check(
        "(m_H_W/v)^2 at result matches target to < 10^{-7}",
        diff_target < Fraction(1, 10**7),
        f"|(m_H_W/v)^2(result) - target| = {float(diff_target):.2e}",
    )

    return result


# ---------------------------------------------------------------------------
# Part 7: Comparison to leading-order linear-form (PR #761) value 0.23572
# ---------------------------------------------------------------------------
def part7_comparison_to_leading_order(r_all_orders: Fraction):
    section("Part 7: comparison to leading-order linear-form (PR #761)")
    # PR #761's leading-order linear-Taylor closure equation:
    #   m_H_W ≈ m_H_zero · (1 - (3/2) r^2 / u_0^2) = m_H_PDG
    # ⇒  (r/u_0)^2 = (2/3) · (1 - m_H_PDG/m_H_zero)
    m_H_zero = V_GEV / (2 * U_0)  # = v / (2 u_0)
    ratio = M_H_PDG_COMPARISON / m_H_zero
    rsq_over_u0sq_LO = (Fraction(2) / Fraction(3)) * (Fraction(1) - ratio)
    rsq_LO = rsq_over_u0sq_LO * U_0_SQ
    # Compute r_LO via Fraction sqrt approximation:
    # We know rsq_LO exactly. We just want r_LO_approx ≈ sqrt(rsq_LO).
    # Use a few Newton iterations:
    r_LO = Fraction(rsq_LO.numerator) / Fraction(rsq_LO.denominator)  # placeholder
    # Initial guess from float sqrt:
    r_LO = Fraction(int(round(float(rsq_LO) ** 0.5 * 10**10)), 10**10)
    # Newton iterations (returns rational approximation):
    for _ in range(10):
        if r_LO == 0:
            break
        r_LO = (r_LO + rsq_LO / r_LO) / 2

    print(f"  m_H_zero = v / (2 u_0) = {float(m_H_zero):.6f} GeV")
    print(f"  (r_LO / u_0)^2 = (2/3)·(1 - m_H_PDG/m_H_zero) = "
          f"{float(rsq_over_u0sq_LO):.6f}")
    print(f"  r_LO = {float(r_LO):.5f}")
    print(f"  PR-#761 stated value: 0.23572")

    # Verify r_LO ≈ 0.23572:
    expected_r_LO = Fraction(23572, 100000)
    diff_LO = abs(r_LO - expected_r_LO)
    check(
        "linear-form leading-order r_leading ≈ 0.23572 (PR #761)",
        diff_LO < Fraction(1, 10**4),
        f"r_LO_recomputed = {float(r_LO):.6f}, "
        f"PR-#761 = 0.23572, diff = {float(diff_LO):.2e}",
    )

    # Relative shift:
    rel_shift = (r_all_orders - r_LO) / r_LO
    print(f"  r_all_orders = {float(r_all_orders):.6f}")
    print(f"  Relative shift (r_all_orders - r_LO)/r_LO = "
          f"{float(rel_shift) * 100:.2f} %")

    # Note claims ~13.9 %:
    expected_shift_pct = Fraction(139, 1000)  # 0.139
    diff_shift = abs(rel_shift - expected_shift_pct)
    check(
        "relative shift (r_all_orders - r_leading)/r_leading ≈ 13.9%",
        diff_shift < Fraction(5, 1000),  # within 0.5 percentage points
        f"shift = {float(rel_shift) * 100:.2f} %, expected ≈ 13.9 %, "
        f"diff = {float(diff_shift) * 100:.2f} %-pts",
    )

    # The all-orders shift is POSITIVE — leading-order under-estimates r:
    check(
        "all-orders r is LARGER than linear-form leading-order r "
        "(leading-order under-estimates)",
        r_all_orders > r_LO,
        f"r_all = {float(r_all_orders):.5f} vs r_LO = {float(r_LO):.5f}",
    )


# ---------------------------------------------------------------------------
# Part 8: Perturbative validity (radius of convergence boundary)
# ---------------------------------------------------------------------------
def part8_perturbative_validity(r_all_orders: Fraction):
    section("Part 8: perturbative validity (r < u_0 / 2 ≈ 0.439)")
    # The Taylor expansion of f(x) = (u_0^2 - x)/(u_0^2 + x)^2 has radius of
    # convergence x = u_0^2 (the singularity at x = -u_0^2 is at distance
    # u_0^2 from the origin). For the dominant k = 0, 4 summands, x = 4 r^2,
    # so the radius gives 4 r^2 < u_0^2, i.e., r < u_0 / 2.
    boundary = U_0 / 2
    print(f"  Validity boundary: u_0 / 2 = {float(boundary):.6f}")
    print(f"  r_all_orders     = {float(r_all_orders):.6f}")
    ratio = r_all_orders / boundary
    print(f"  r_all_orders / (u_0/2) = {float(ratio):.4f} "
          f"(should be < 1 for convergent Taylor)")

    check(
        "r_all_orders < u_0/2 (within perturbative-Taylor radius of convergence)",
        r_all_orders < boundary,
        f"r_all = {float(r_all_orders):.5f}, u_0/2 = {float(boundary):.5f}",
    )

    # Expansion parameter (2r/u_0)^2 should be < 1 for Taylor convergence:
    exp_param = (2 * r_all_orders / U_0) ** 2
    print(f"  (2 r / u_0)^2 at r_all_orders = {float(exp_param):.4f} (must be < 1)")
    check(
        "(2 r / u_0)^2 < 1 at r_all_orders (dominant-summand Taylor parameter)",
        exp_param < 1,
        f"(2r/u_0)^2 = {float(exp_param):.4f}",
    )

    # And the expansion parameter should be ≈ 0.37 (per note):
    diff_param = abs(exp_param - Fraction(37, 100))
    check(
        "(2 r / u_0)^2 ≈ 0.37 at r_all_orders (per note)",
        diff_param < Fraction(2, 100),
        f"computed = {float(exp_param):.4f}, expected ≈ 0.37",
    )


# ---------------------------------------------------------------------------
# Part 9: Forbidden-import audit
# ---------------------------------------------------------------------------
def part9_forbidden_imports():
    section("Part 9: stdlib-only / no PDG pins (other than declared comparison)")
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
# Part 10: Boundary check — what is NOT closed
# ---------------------------------------------------------------------------
def part10_boundary_check():
    section("Part 10: boundary check (what is NOT closed)")
    not_claimed = [
        "the +12% Higgs gap chain",
        "the physical Higgs mass `m_H` numerical value",
        "the value of the Wilson coefficient `r` itself",
        "the plaquette mean-field link `u_0` numerical value",
        "the staggered-Dirac realization gate",
        "the `g_bare = 1` derivation",
        "any parent theorem/status promotion",
        "the *exact* (irrational) closure value of `r`",
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

    # The closure value is FLAGGED as conditional on three admissions:
    check(
        "closure value flagged as conditional on uniform-N_taste=16 admission",
        "uniform-`N_taste = 16` channel admission (non-derived)" in NOTE_TEXT,
    )
    check(
        "closure value flagged as conditional on tree-level mean-field",
        "tree-level mean-field formalism" in NOTE_TEXT,
    )
    check(
        "closure value flagged as conditional on non-zero r (not canonical KS)",
        "not part of the canonical pure-" in NOTE_TEXT,
    )


def main() -> int:
    banner("frontier_wilson_m_h_tree_at_extremum_all_orders.py")
    print(" Bounded source note: (m_H_W/v)^2 = (1/64) Σ_k binomial(4,k) ·")
    print("   (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2  (eq. (2), exact in r)")
    print("   Reduces to 1/(4u_0^2) at r=0 (parent eq. [5]) and to PR-#761's")
    print("   leading-order form at small r. All-orders bisection gives")
    print("   r_all_orders ≈ 0.26855 ± 10^{-5}, a +13.9% shift from")
    print("   the linear-form leading-order value 0.23572.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()
    part4_reduction_at_r_zero()
    part5_reduction_to_leading_order()
    r_all_orders = part6_bisection_for_r_all_orders()
    part7_comparison_to_leading_order(r_all_orders)
    part8_perturbative_validity(r_all_orders)
    part9_forbidden_imports()
    part10_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: all-orders closed form (m_H_W/v)^2 = (1/64) Σ_k binomial(4,k) ·")
        print(" (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2 verified at exact")
        print(" rational precision. Reduces to 1/(4u_0^2) at r=0 (matches parent eq.")
        print(" [5]) and to PR-#761's leading order at small r. Bisection gives")
        print(" r_all_orders ≈ 0.26855 ± 10^{-5}, a ~14% shift from the leading-order")
        print(" closure value 0.23572. The all-orders shift is non-trivial: leading-")
        print(" order linear-Taylor under-estimates r by ~14% under the canonical")
        print(" admissions. Closure is conditional on uniform-N_taste=16 + tree-level")
        print(" + non-zero r.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
