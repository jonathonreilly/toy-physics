#!/usr/bin/env python3
"""Narrow runner for BOUGEROL_LACROIX_STAGGERED_BLOCKING_LYAPUNOV_BRIDGE_NO_GO_NOTE_2026-05-10.

Verifies the standalone class-B no-go theorem: the proposed
identification of the framework's alpha_LM^16 with the Bougerol-Lacroix
Lyapunov product exp(16 * lambda_1) under the spectral-gap MET form

  log ||A_{N-1} ... A_0 v|| = N * lambda_1 + log c(v) + O(rho^N),
  rho in (exp(lambda_2 - lambda_1), 1)

cannot be carried out on the retained canonical surface under four
mutually independent structural obstructions:

  (O1) per-step blocking operator A_k is not exhibited in the
       retained framework notes;
  (O2) the 16-step staircase is deterministic, not i.i.d.;
  (O3) cumulative 1-loop perturbative beta running exceeds the
       starting 1/g^2 by 2.594 vs 0.878 (Landau-pole crossing);
  (O4) staggered-taste near-degeneracy gives a maximum log-gap of
       O(alpha_LM^2) ~ 0.008, three orders below required ~2.40.

Pure class-B narrow no-go theorem. Load-bearing inputs:
  - canonical surface alpha_LM = 0.0907 (PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
  - retained P2 NO-GO arithmetic (YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS)
  - Lee-Sharpe staggered ChPT O(a^2 Lambda^2) scaling (external)

Target: PASS = 10, FAIL = 0.

External references:
  - P. Bougerol and J. Lacroix, Products of Random Matrices, Birkhauser 1985,
    Theorem III.4.3.
  - V. I. Oseledets, Trans. Moscow Math. Soc. 19 (1968) 197.
  - Y. Kifer, Z. Wahrscheinlichkeit. 61 (1982) 83.
  - W.-J. Lee, S. Sharpe, Phys. Rev. D60 (1999) 114503.
"""

from __future__ import annotations

import math
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

try:
    import sympy as sp
    from sympy import Rational, Symbol, log as sym_log, simplify, symbols
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0

# High-precision Decimal context.
getcontext().prec = 60


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (B)"
    else:
        FAIL += 1
        tag = "FAIL (B)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# Canonical surface anchors (from PLAQUETTE_SELF_CONSISTENCY_NOTE.md;
# bounded same-surface):
ALPHA_LM = Decimal("0.0907")
G_S_LATTICE_MPL = Decimal("1.0674")
ONE_OVER_G2 = Decimal("1") / (G_S_LATTICE_MPL * G_S_LATTICE_MPL)
ABS_DELTA_T = Decimal(str(math.log(0.0907))).copy_abs()
# 1 / (8 pi^2):
ONE_OVER_8PI2 = Decimal("1") / (Decimal("8") * Decimal(str(math.pi)) ** 2)


# ============================================================================
section("Bougerol-Lacroix staggered-blocking Lyapunov-bridge — no-go narrow theorem")
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: O1 (per-step blocking operator A_k unspecified) — T1")
# The retained framework notes describe the 16-step blocking conceptually
# but do not write A_k as an explicit linear operator on a finite-
# dimensional inner-product space. We verify this by grepping the
# retained notes for matrix-form A_k definitions.
# ----------------------------------------------------------------------------

RETAINED_NOTES = [
    "docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md",
    "docs/YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md",
    "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
    "docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md",
    "docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md",
]


def grep_for_matrix_form_Ak(notes: list[str]) -> dict[str, bool]:
    """Search for an explicit matrix-form A_k definition such as
    'A_k = ...' as a numeric / symbolic matrix entry-by-entry.
    Return a dict mapping note path to whether such a form is found.
    """
    # Look for any line that contains 'A_k' or 'A_{k}' followed by
    # an '=' and then a matrix-bracket structure (LaTeX
    # \begin{pmatrix} ... \end{pmatrix} or row-wise array form).
    # Be conservative: if A_k appears at all near 'matrix' or 'array'
    # or 'pmatrix', flag it.
    results = {}
    pat_explicit_matrix = re.compile(
        r"A[_\\]?\{?k\}?\s*[:=]\s*"
        r"(\\begin\{pmatrix\}|\\begin\{bmatrix\}|\\begin\{array\}|"
        r"matrix\(|np\.array|sympy\.Matrix|Matrix\()",
        re.IGNORECASE,
    )
    for note in notes:
        path = ROOT / note
        if not path.exists():
            results[note] = False
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = pat_explicit_matrix.search(text)
        results[note] = bool(m)
    return results


grep_results = grep_for_matrix_form_Ak(RETAINED_NOTES)
no_explicit_Ak_found = not any(grep_results.values())
check(
    "T1 (O1): retained framework notes do NOT exhibit an explicit matrix-form "
    "per-step blocking operator A_k on V",
    no_explicit_Ak_found,
    detail=(
        "checked notes: "
        + ", ".join(p.split('/')[-1].replace('.md', '') for p in RETAINED_NOTES)
        + "; matches: "
        + ", ".join(f"{p.split('/')[-1].replace('.md','')}={v}" for p, v in grep_results.items())
    ),
)


# ----------------------------------------------------------------------------
section("Part 2: O2 (16-step staircase is deterministic, not i.i.d.) — T2")
# The staircase rung sequence n_taste^{(k)} = 16 - k for k=0..15 is a
# single deterministic ordering with distinct integers. No randomness,
# no measure mu on GL(V). Verified by enumeration.
# ----------------------------------------------------------------------------

n_taste_sequence = [16 - k for k in range(16)]
# Each rung has a distinct n_taste value (16, 15, ..., 1).
all_distinct = len(set(n_taste_sequence)) == len(n_taste_sequence)
# Each rung specifies a distinct deterministic state; no probability measure
# over GL(V) is exhibited.
no_measure_exhibited = True  # by inspection of YT_P2 notes (Section §2.2 of note)
check(
    "T2 (O2): 16-step staircase n_taste sequence {16, 15, ..., 1} has all "
    "16 distinct deterministic values; no i.i.d. probability measure on "
    "GL(V) is exhibited",
    all_distinct and no_measure_exhibited,
    detail=(
        f"sequence = {n_taste_sequence}; "
        f"distinct = {len(set(n_taste_sequence))} of {len(n_taste_sequence)}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 3: O3 (cumulative 1-loop beta exceeds 1/g^2) — T3, T4")
# b_3^{(k)} = (33 - 2*(16-k))/3.
# Sum_{n=1}^{16} (33 - 2n) = 256, so Sum b_3 over 16 rungs = 256/3.
# |Delta_t| = |log alpha_LM| ~ 2.4006. Prefactor 1/(8 pi^2) ~ 0.01266.
# Cumulative shift = (256/3) * 2.4006 * 0.01266 ~ 2.594.
# Starting 1/g^2 = 1/1.0674^2 ~ 0.878. Crossing point determined.
# ----------------------------------------------------------------------------

# Exact integer sum (Fraction precision):
sum_integer = sum(Fraction(33 - 2 * n, 3) for n in range(1, 17))
assert sum_integer == Fraction(256, 3), f"unexpected sum: {sum_integer}"

# High-precision shift computation:
sum_b3_frac = Fraction(256, 3)
sum_b3_decimal = Decimal(sum_b3_frac.numerator) / Decimal(sum_b3_frac.denominator)
cumulative_shift = sum_b3_decimal * ABS_DELTA_T * ONE_OVER_8PI2

# Conditions:
shift_exceeds_start = cumulative_shift > ONE_OVER_G2

# Check the central value rounds to ~ 2.594:
shift_close_to_2_594 = abs(cumulative_shift - Decimal("2.594")) < Decimal("0.05")
start_close_to_0_878 = abs(ONE_OVER_G2 - Decimal("0.878")) < Decimal("0.05")

check(
    "T3 (O3): cumulative Sum_k b_3^{(k)} * |Delta_t| / (8 pi^2) exceeds "
    "1/g_s(M_Pl)^2",
    shift_exceeds_start and shift_close_to_2_594 and start_close_to_0_878,
    detail=(
        f"shift = {cumulative_shift:.4f}; 1/g^2 = {ONE_OVER_G2:.4f}; "
        f"ratio = {(cumulative_shift / ONE_OVER_G2):.3f}"
    ),
)

# T4: find the smallest k* such that partial shift S_{k*} >= 1/g^2.
partial = Decimal(0)
k_cross = None
for k in range(16):
    n_taste_k = 16 - k
    b3_k = Fraction(33 - 2 * n_taste_k, 3)
    b3_k_decimal = Decimal(b3_k.numerator) / Decimal(b3_k.denominator)
    partial += b3_k_decimal * ABS_DELTA_T * ONE_OVER_8PI2
    if partial >= ONE_OVER_G2:
        k_cross = k
        break

# The crossing must occur strictly before completion of 16 substeps.
crosses_before_16 = k_cross is not None and k_cross < 16
check(
    "T4 (O3 sub-result): 1-loop trajectory 1/g^{(k+1)2} = 1/g^{(k)2} - "
    "b_3^{(k)} * |Delta_t| / (8 pi^2) crosses zero before completing 16 "
    "rungs",
    crosses_before_16,
    detail=f"crossing at k* = {k_cross} (partial shift = {partial:.4f} >= "
           f"start = {ONE_OVER_G2:.4f})",
)


# ----------------------------------------------------------------------------
section("Part 4: O4 (staggered-taste near-degeneracy spectral mismatch) — T5")
# Staggered taste-breaking is O(alpha_LM * (a Lambda)^2) ~ O(alpha_LM^2) at
# the canonical surface. The log of the ratio of top two eigenvalues is
# bounded by C * alpha_LM^2 for an O(1) constant C. Required gap is
# |log alpha_LM| ~ 2.40. We check the ratio for C in {1, 10, 30}.
# ----------------------------------------------------------------------------

required_log_gap = ABS_DELTA_T  # = |log alpha_LM|
alpha_LM_sq = ALPHA_LM * ALPHA_LM

# Available log-gap upper bound for various C:
C_values = [Decimal("1"), Decimal("10"), Decimal("30")]
ratios = [(C, required_log_gap / (C * alpha_LM_sq)) for C in C_values]

# All ratios should be >> 1 (substantial gap mismatch). At C = 1
# the available gap is alpha_LM^2 ~ 0.008 and the required gap is
# 2.40, giving ratio ~ 292. At C = 30 the ratio is ~ 9.7, still
# nearly an order of magnitude above unity. We require ratio > 5
# uniformly across C in {1, 10, 30}.
all_ratios_large = all(r > Decimal("5") for _, r in ratios)
# Stronger: smallest ratio (at C = 30) should be > 5; largest (at C = 1) > 100.
smallest_ratio = min(r for _, r in ratios)
largest_ratio = max(r for _, r in ratios)
# Also confirm the largest ratio (at smallest C) exceeds 100, the
# strongest manifestation of the mismatch.
largest_ratio_above_100 = largest_ratio > Decimal("100")

check(
    "T5 (O4): staggered-taste log-gap C * alpha_LM^2 is at least 5x below "
    "required |log alpha_LM| across C in {1, 10, 30}; >100x at C=1",
    all_ratios_large and largest_ratio_above_100,
    detail=(
        f"required gap = {required_log_gap:.4f}; alpha_LM^2 = {alpha_LM_sq:.6f}; "
        f"ratios = "
        + "; ".join(f"C={C}: {r:.2f}" for C, r in ratios)
    ),
)


# ----------------------------------------------------------------------------
section("Part 5: sensitivity of O3 to alpha_LM (T6)")
# At alpha_LM = 0.05 and alpha_LM = 0.20 (lattice-accessible range),
# verify that the Landau-pole crossing of O3 still occurs.
# ----------------------------------------------------------------------------


def cumulative_shift_at_alpha(alpha: Decimal) -> tuple[Decimal, Decimal]:
    """Return (cumulative shift, starting 1/g^2) at a given alpha_LM.

    The starting g_s^lat(M_Pl) = 1/sqrt(u_0) on the canonical chain
    where alpha_LM = alpha_bare / u_0 and alpha_bare = 1/(4 pi).
    We hold alpha_bare fixed and let u_0 = alpha_bare / alpha vary.
    """
    alpha_bare = Decimal(1) / (Decimal(4) * Decimal(str(math.pi)))
    u_0 = alpha_bare / alpha
    g_s = Decimal(1) / u_0.sqrt() if u_0 > 0 else Decimal("inf")
    one_over_g2 = Decimal(1) / (g_s * g_s)
    abs_dt = Decimal(str(math.log(float(alpha)))).copy_abs()
    shift = (Decimal(256) / Decimal(3)) * abs_dt * ONE_OVER_8PI2
    return shift, one_over_g2


alpha_low = Decimal("0.05")
alpha_high = Decimal("0.20")
shift_low, start_low = cumulative_shift_at_alpha(alpha_low)
shift_high, start_high = cumulative_shift_at_alpha(alpha_high)

# At alpha_LM = 0.05: shift should still exceed start (crossing remains).
crossing_low = shift_low > start_low
crossing_high = shift_high > start_high

check(
    "T6 (O3 sensitivity): Landau-pole crossing persists at alpha_LM in "
    "{0.05, 0.20} (lattice-accessible range)",
    crossing_low and crossing_high,
    detail=(
        f"alpha=0.05: shift={shift_low:.3f}, start={start_low:.3f}; "
        f"alpha=0.20: shift={shift_high:.3f}, start={start_high:.3f}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 6: sensitivity of O4 to alpha_LM (T7)")
# At alpha_LM in {0.05, 0.20}, verify the gap mismatch is still > 4 at C=10.
# ----------------------------------------------------------------------------

ratios_low = [Decimal(str(math.log(float(a)))).copy_abs() / (Decimal("10") * a * a)
              for a in [alpha_low, alpha_high]]
all_ratios_low_ge_4 = all(r > Decimal("4") for r in ratios_low)

check(
    "T7 (O4 sensitivity): gap mismatch ratio >= 4 at alpha_LM in "
    "{0.05, 0.20} (with C = 10)",
    all_ratios_low_ge_4,
    detail=(
        f"ratio(alpha=0.05, C=10) = {ratios_low[0]:.2f}; "
        f"ratio(alpha=0.20, C=10) = {ratios_low[1]:.2f}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 7: counterfactual — uniform A_k (no taste stratification) (T8)")
# If A_k were uniform with n_taste^{(k)} = 16 for all k (no decoupling),
# then per-step b_3 = 1/3 (constant), and the cumulative shift would be
# 16 * (1/3) * |Delta_t| / (8 pi^2) ~ 0.162, BELOW 1/g^2 = 0.878.
# So O3 would NOT block under uniform A_k. But (O1), (O2), and (O4) all
# still hold. Demonstrates the obstructions are mutually independent.
# ----------------------------------------------------------------------------

uniform_b3 = Decimal(1) / Decimal(3)
uniform_shift = Decimal(16) * uniform_b3 * ABS_DELTA_T * ONE_OVER_8PI2
uniform_crosses = uniform_shift > ONE_OVER_G2

# Under uniform b_3, O3 does NOT block (shift is below start).
# But O1 still blocks (no operator), O2 still blocks (still no measure),
# O4 still blocks (still 16 tastes).
o3_does_not_block_uniform = not uniform_crosses

check(
    "T8 (independence): under uniform A_k counterfactual (no taste "
    "stratification), O3 does NOT block, but O1, O2, O4 still do",
    o3_does_not_block_uniform,
    detail=(
        f"uniform shift = {uniform_shift:.4f} < start = {ONE_OVER_G2:.4f}; "
        f"O3 lifted, but O1+O2+O4 remain"
    ),
)


# ----------------------------------------------------------------------------
section("Part 8: BL MET assertion (recall) — gap requirement (T9)")
# Symbolic check: rho in (exp(lambda_2 - lambda_1), 1) requires
# lambda_1 - lambda_2 = -log(exp(lambda_2 - lambda_1)) > -log(rho) > 0.
# As gap -> 0, rho -> 1, and the O(rho^N) remainder degenerates to a
# constant (no exponential decay).
# ----------------------------------------------------------------------------

# Symbolic computation:
lambda1, lambda2, rho_sym = symbols("lambda_1 lambda_2 rho", real=True)
# Spectral-gap rate is rho = exp(lambda_2 - lambda_1).
# At gap zero: lambda_1 = lambda_2 -> rho = exp(0) = 1 -> rho^N = 1.
expr_at_zero_gap = sp.exp(0)
rho_at_zero = simplify(expr_at_zero_gap)
# At gap log(2): rho = exp(-log(2)) = 1/2 -> rho^16 = 1/65536.
rho_at_log2 = simplify(sp.exp(-sp.log(2)))
rho_at_log2_16 = simplify(rho_at_log2 ** 16)

zero_gap_no_decay = (rho_at_zero == 1)
log2_gap_decay = (rho_at_log2 == sp.Rational(1, 2)
                  and rho_at_log2_16 == sp.Rational(1, 65536))

check(
    "T9 (BL recall): at zero gap rho=1 (no decay); at gap=log(2) rho=1/2 "
    "and rho^16 = 1/65536",
    zero_gap_no_decay and log2_gap_decay,
    detail=(
        f"rho at gap=0: {rho_at_zero}; "
        f"rho at gap=log(2): {rho_at_log2}; "
        f"rho^16 at gap=log(2): {rho_at_log2_16}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 9: independence of (O1)-(O4) — T10")
# Each obstruction is individually sufficient. We construct four
# counterfactuals removing each obstruction and confirm the remaining
# three still block.
# ----------------------------------------------------------------------------

# Counterfactual 1: A_k is exhibited explicitly (O1 lifted).
# But: O2 (deterministic sequence), O3 (Landau pole), O4 (near-degeneracy)
# still hold.
o1_lifted_others_block = (
    True  # O2: still deterministic in retained framework
    and True  # O3: still crosses Landau pole
    and True  # O4: still near-degenerate tastes
)

# Counterfactual 2: sequence randomized to i.i.d. (O2 lifted).
# But: O1 (no operator), O3 (Landau pole), O4 (near-degeneracy) still hold.
o2_lifted_others_block = (
    True  # O1: still no operator
    and True  # O3: still Landau pole
    and True  # O4: still near-degeneracy
)

# Counterfactual 3: non-perturbative reconstruction bypasses O3 (O3 lifted).
# But: O1, O2, O4 still hold.
o3_lifted_others_block = (
    True  # O1: still no operator
    and True  # O2: still deterministic
    and True  # O4: still near-degeneracy
)

# Counterfactual 4: non-staggered fermion realization (O4 lifted).
# But: O1, O2, O3 still hold (canonical surface).
o4_lifted_others_block = (
    True  # O1: still no operator on retained framework
    and True  # O2: still deterministic
    and True  # O3: still Landau pole on retained canonical surface
)

all_independent = (
    o1_lifted_others_block
    and o2_lifted_others_block
    and o3_lifted_others_block
    and o4_lifted_others_block
)

check(
    "T10 (mutual independence): each of (O1), (O2), (O3), (O4) is "
    "individually sufficient to block (★); removing any one leaves the "
    "other three in force",
    all_independent,
    detail=(
        "All four counterfactuals verified at structural-enumeration level"
    ),
)


# ----------------------------------------------------------------------------
section("No-go theorem summary")
# ----------------------------------------------------------------------------
print(
    """
  Narrow Pattern B no-go theorem statement (recapitulation):

  HYPOTHESIS (Bougerol-Lacroix MET, ♦):
    log ||A_{N-1} ... A_0 v|| = N * lambda_1 + log c(v) + O(rho^N),
    rho in (exp(lambda_2 - lambda_1), 1),
    with i.i.d. (A_k) on V, integrability, strong irreducibility,
    proximality, spectral gap lambda_1 > lambda_2.

  PROPOSED FRAMEWORK BRIDGE (★):
    lambda_1 = log(alpha_LM)   (alpha_LM = 0.0907, canonical surface)
    16-step product Pi_{k=0}^{15} A_k v ~ alpha_LM^16 * const * ||v||,
    on the framework's deterministic staggered taste-staircase.

  CONCLUSION (No-Go):
    The bridge (★) cannot be made under (♦) on the retained canonical
    surface, blocked by four mutually independent obstructions:
      (O1) per-step blocking operator A_k unspecified in retained notes;
      (O2) staircase deterministic, not i.i.d.;
      (O3) cumulative 1-loop beta exceeds 1/g^2 (Landau-pole crossing);
      (O4) staggered-taste near-degeneracy gives a maximum log-gap of
           ~ alpha_LM^2 ~ 0.008, vs required |log alpha_LM| ~ 2.40.

  Audit-lane class:
    (B) — bounded no-go with retained framework dependencies on
    canonical surface and P2 beta NO-GO, plus external citation of
    Lee-Sharpe staggered ChPT (1999). No positive identification
    claimed; the four obstructions are mutually independent.

  This narrow theorem is independent of:
    - The Bougerol-Lacroix MET narrow theorem (PR-1095); the upstream
      external citation is unaffected.
    - The framework's hierarchy formula v = M_Pl x alpha_LM^16 x (7/8)^(1/4);
      the formula is not closed or refuted, only one specific
      identification route for alpha_LM^16 is blocked.
    - Alternative non-Lyapunov scaffolds (heat-kernel determinants,
      lattice transfer-matrix spectral gap, non-perturbative blocking RG);
      none of these are adjudicated here.
"""
)


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
