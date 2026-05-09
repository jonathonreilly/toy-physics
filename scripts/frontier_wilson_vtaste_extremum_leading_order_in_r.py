#!/usr/bin/env python3
"""Wilson-shifted V_taste extremum at leading order in r — bounded source-note runner.

Verifies docs/WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md:

  m^*       =  -4 r    +  O(r^3),                                              (2)

  d^2 V^W / dm^2 |_{m = m^*}
            =  -4 / u_0^2  +  12 r^2 / u_0^4  +  O(r^4).                       (3)

Inputs (canonical bounded surface; no Monte Carlo, no PDG):
- staircase multiplicities binomial(4, k) for k in {0, 1, 2, 3, 4}
- V_taste^W formula (1) and its first two derivatives, from the same-batch note
  docs/WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md
  (runner handles graceful pre-merge absence)

stdlib only; exact `Fraction` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md"

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


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    num = 1
    for i in range(k):
        num *= (n - i)
        num //= (i + 1)
    return num


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: Wilson-Shifted V_taste Extremum",
         "Wilson-Shifted V_taste Extremum at Leading Order in r"),
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
        ("exact-shift formula present (m^* = -4r exact, all orders)",
         "m^*       =  - 4 r       (exact, all orders in r)"),
        ("leading-curvature formula present",
         "12 r^2 ) / u_0^4"),
        ("centered-binomial-moment identity (4) stated", "= 16"),
        ("variance-ratio explanation",
         "80 - 32^2 / 16 = 80 - 64 = 16"),
        ("ratio 5x reduction noted", "5×"),
        ("V_taste^W upstream cited (sister)",
         "WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08"),
        ("Wilson staircase upstream cited",
         "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08"),
        ("Higgs note upstream cited",
         "HIGGS_MASS_FROM_AXIOM_NOTE.md"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
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
# Part 3: Cited upstream files exist (with graceful same-batch handling)
# ---------------------------------------------------------------------------
def part3_premise_class_consistency():
    section("Part 3: cited upstream files (with graceful same-batch handling)")
    must_exist = [
        "docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md",
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(
            f"upstream exists: {rel}",
            (ROOT / rel).exists(),
        )

    # Same-batch reference: V_taste^W note may be absent during pre-merge validation.
    forward_refs = [
        "docs/WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md",
    ]
    for rel in forward_refs:
        path = ROOT / rel
        if path.exists():
            check(f"same-batch reference present: {rel}", True)
        else:
            print(f"  [INFO] same-batch reference not yet on this branch: {rel}")
            print(f"         (intentional; audit lane resolves order)")


# ---------------------------------------------------------------------------
# Part 4: Binomial moments — including the centered moment that drives (3)
# ---------------------------------------------------------------------------
def part4_binomial_moments():
    section("Part 4: binomial moments on Σ_k binomial(4, k) f(k)")
    moment_0 = sum(binomial(4, k) for k in range(5))
    moment_1 = sum(binomial(4, k) * k for k in range(5))
    moment_2 = sum(binomial(4, k) * k * k for k in range(5))
    moment_centered_2 = sum(binomial(4, k) * (k - 2) ** 2 for k in range(5))

    check("Σ binomial(4, k) = 16 (state count)", moment_0 == 16,
          f"got {moment_0}")
    check("Σ binomial(4, k) · k = 32", moment_1 == 32,
          f"got {moment_1}")
    check("Σ binomial(4, k) · k^2 = 80", moment_2 == 80,
          f"got {moment_2}")
    check("Σ binomial(4, k) · (k-2)^2 = 16 (centered second moment, drives +12 coefficient)",
          moment_centered_2 == 16,
          f"got {moment_centered_2}")

    # Variance-identity sanity check (use Fraction division to avoid latent
    # fragility under refactor: integer // would silently round if the
    # numerator weren't exactly divisible).
    variance_check_frac = Fraction(moment_2) - Fraction(moment_1) ** 2 / Fraction(moment_0)
    check(
        "variance identity: Σ k^2 · binom - (Σ k · binom)^2 / Σ binom = 80 - 64 = 16 = Σ (k-2)^2 · binom",
        variance_check_frac == Fraction(16) == Fraction(moment_centered_2),
        f"variance_check = {variance_check_frac}, moment_centered_2 = {moment_centered_2}",
    )

    # Ratio: 80 / 16 = 5 (drives the 60/12 = 5 ratio)
    check(
        "moment ratio Σ k^2 · binom / Σ (k-2)^2 · binom = 80 / 16 = 5",
        moment_2 == 5 * moment_centered_2,
        f"80 / 16 = {Fraction(80, 16)}",
    )


# ---------------------------------------------------------------------------
# Part 5: Extremum shift m^* = -4r EXACTLY (all orders in r)
# ---------------------------------------------------------------------------
def part5_extremum_shift_is_exact():
    section("Part 5: m^* = -4r is EXACT (not just leading-order)")
    # Reduced equation at leading order (denominators -> 4 u_0^2):
    #   Σ_k binomial(4, k) · (2rk + δm) = 0
    #   2r · Σ_k binomial(4, k) · k  +  δm · Σ_k binomial(4, k)  =  0
    #   2r · 32  +  δm · 16  =  0
    #   δm = -4r
    # The full claim is stronger: by k → 4-k reflection symmetry on
    # binomial(4, k) and the antisymmetric pair shifts (2r(k-2) and
    # 2r(2-k)), every pair contribution to dV^W/dm at m=-4r cancels
    # term-by-term, so dV^W/dm |_{m=-4r} = 0 identically (all orders).
    moment_1 = Fraction(32)
    moment_0 = Fraction(16)
    delta_m_per_r = -Fraction(2) * moment_1 / moment_0
    check(
        "leading-order shift coefficient: δm / r = -2 · Σ k · binom / Σ binom = -2 · 32 / 16 = -4",
        delta_m_per_r == Fraction(-4),
        f"got {delta_m_per_r}",
    )

    # EXACT identity check: dV^W/dm at m=-4r should be identically zero
    # for every (rational) r and every (rational) u_0, not just at small r.
    u_0 = Fraction(8776, 10000)
    u_0_sq = u_0 * u_0
    for r_test in [
        Fraction(1, 100),
        Fraction(1, 10),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
        Fraction(10),
    ]:
        m_star = Fraction(-4) * r_test
        derivative = Fraction(0)
        for k in range(5):
            mult = Fraction(binomial(4, k))
            u_k = 2 * r_test * k + m_star  # = 2r(k-2)
            denom = u_k * u_k + 4 * u_0_sq
            derivative -= mult * u_k / denom

        check(
            f"dV^W/dm at m=-4r is EXACTLY 0 at r={r_test} (k → 4-k reflection symmetry)",
            derivative == Fraction(0),
            f"derivative = {derivative} (must be exactly 0)",
        )

    # Sanity: print the symmetry argument
    print()
    print("  Symmetry argument: at m = -4r, u_k = 2r(k-2). Pair (k, 4-k):")
    print("    binom(4, k) = binom(4, 4-k), and u_{4-k} = 2r((4-k)-2) = -2r(k-2) = -u_k.")
    print("    Each pair (k, 4-k): mult · u_k / (u_k^2 + 4u_0^2) + mult · u_{4-k} / (u_{4-k}^2 + 4u_0^2)")
    print("                       = mult · u_k / (u_k^2 + 4u_0^2) + mult · (-u_k) / (u_k^2 + 4u_0^2)")
    print("                       = 0.")
    print("    The k=2 self-paired term has u_2 = 0 directly. So all pair sums and the singleton")
    print("    contribute zero, giving dV^W/dm |_{m=-4r} = 0 identically.")


# ---------------------------------------------------------------------------
# Part 6: Curvature at m^* = -4r leading-order = -4/u_0^2 + 12 r^2 / u_0^4
# ---------------------------------------------------------------------------
def part6_curvature_at_extremum():
    section("Part 6: d^2 V^W / dm^2 |_{m=-4r} = -4/u_0^2 + 12 r^2 / u_0^4 + O(r^4)")
    # d^2 V^W / dm^2 = Σ_k binomial(4, k) · ((2rk + m)^2 - 4 u_0^2) /
    #                                       ((2rk + m)^2 + 4 u_0^2)^2
    # At m = -4r: (2rk + m) = 2r(k - 2)
    # So:
    #   d^2 V^W / dm^2 |_{m=-4r}
    #     = Σ_k binomial(4, k) · (4 r^2 (k-2)^2 - 4 u_0^2) / (4 r^2 (k-2)^2 + 4 u_0^2)^2
    #     = (1/4) · Σ_k binomial(4, k) · ((k-2)^2 r^2 - u_0^2) / ((k-2)^2 r^2 + u_0^2)^2

    u_0 = Fraction(8776, 10000)
    u_0_sq = u_0 * u_0

    for r_test in [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 2), Fraction(1)]:
        r_sq = r_test * r_test
        curvature = Fraction(0)
        for k in range(5):
            mult = Fraction(binomial(4, k))
            shift_sq = (k - 2) ** 2 * r_sq
            numer = shift_sq - u_0_sq
            denom = (shift_sq + u_0_sq) ** 2
            curvature += mult * numer / denom
        curvature /= 4

        if r_test == 0:
            expected = -Fraction(4) / u_0_sq
            check(
                "r=0: curvature at m^*=0 = -4/u_0^2 (matches parent eq. [3])",
                curvature == expected,
                f"got {curvature}, expected {expected}",
            )
        else:
            # Compare to leading-order Taylor approximation -4/u_0^2 + 12 r^2 / u_0^4:
            taylor_12 = -Fraction(4) / u_0_sq + Fraction(12) * r_sq / (u_0_sq * u_0_sq)
            taylor_60 = -Fraction(4) / u_0_sq + Fraction(60) * r_sq / (u_0_sq * u_0_sq)
            diff_12 = abs(curvature - taylor_12)
            diff_60 = abs(curvature - taylor_60)
            print(f"  r = {r_test} = {float(r_test):.6f}")
            print(f"    curvature exact  = {float(curvature):.10f}")
            print(f"    Taylor with 12   = {float(taylor_12):.10f}, diff = {float(diff_12):.3e}")
            print(f"    Taylor with 60   = {float(taylor_60):.10f}, diff = {float(diff_60):.3e}")
            check(
                f"r = {r_test}: leading-order Taylor with coefficient 12 closer than coefficient 60",
                diff_12 < diff_60,
                f"diff_12 = {float(diff_12):.3e}, diff_60 = {float(diff_60):.3e}",
            )


# ---------------------------------------------------------------------------
# Part 6b: Direct extraction of the leading-r^2 coefficient — pin to 12 cleanly
# ---------------------------------------------------------------------------
def part6b_direct_nlo_coefficient_extraction():
    section("Part 6b: direct extraction of the +12 r^2/u_0^4 coefficient at small r")
    # At small r, define c(r) := (curvature - (-4/u_0^2)) · u_0^4 / r^2.
    # The leading-order claim is c(r) → 12 as r → 0.
    # We extract c(r) at successively smaller r and verify convergence to 12.
    u_0 = Fraction(8776, 10000)
    u_0_sq = u_0 * u_0
    u_0_pow4 = u_0_sq * u_0_sq

    leading_zero = -Fraction(4) / u_0_sq

    extracted_values = []
    for r_test in [Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10_000), Fraction(1, 100_000)]:
        rsq = r_test * r_test
        curvature = Fraction(0)
        for k in range(5):
            mult = Fraction(binomial(4, k))
            shift_sq = (k - 2) ** 2 * rsq
            numer = shift_sq - u_0_sq
            denom = (shift_sq + u_0_sq) ** 2
            curvature += mult * numer / denom
        curvature /= 4
        # Extract leading r^2 coefficient
        c = (curvature - leading_zero) * u_0_pow4 / rsq
        extracted_values.append((r_test, c))
        print(f"  r = {r_test} ({float(r_test):.0e}):  c(r) = {float(c):.10f}")

    # As r → 0, c(r) should → 12 cleanly. At r = 1/100_000, the extracted
    # value should agree with 12 to many decimal places (the residual is
    # O(r^2 / u_0^2) suppressed).
    smallest_r, smallest_c = extracted_values[-1]
    diff_from_12 = abs(smallest_c - Fraction(12))
    threshold = Fraction(1, 1_000_000)  # less than 1e-6
    check(
        f"at r = 1/100_000, c(r) → 12 cleanly (diff < 1e-6)",
        diff_from_12 < threshold,
        f"c({smallest_r}) = {float(smallest_c):.10f}, |c - 12| = {float(diff_from_12):.3e}",
    )

    # Also verify c(r) is MONOTONICALLY APPROACHING 12 (not just close at one r).
    # The residual goes as r^2, so |c(r) - 12| should decrease as r decreases.
    diffs = [abs(c - Fraction(12)) for r, c in extracted_values]
    monotone = all(diffs[i + 1] <= diffs[i] for i in range(len(diffs) - 1))
    check(
        "c(r) approaches 12 monotonically as r → 0 (consistent with O(r^2) residual)",
        monotone,
        f"diffs from 12 at r ∈ {{1/100, 1/1000, 1/10K, 1/100K}}: {[float(d) for d in diffs]}",
    )

    # Cross-check: the derived structural value is 3 · 16 / 4 = 12.
    derived_coeff = Fraction(3) * Fraction(16) / Fraction(4)
    check(
        "structural derivation: 3 · Σ binom·(k-2)^2 / 4 = 3 · 16 / 4 = 12",
        derived_coeff == Fraction(12),
        f"got {derived_coeff}",
    )


# ---------------------------------------------------------------------------
# Part 7: Reduction at r = 0 (extremum at m^* = 0, curvature = -4/u_0^2)
# ---------------------------------------------------------------------------
def part7_r_zero_reduction():
    section("Part 7: r → 0 reduction (m^* = 0; curvature = -4/u_0^2)")
    # At r = 0, the leading-order shift m^* = -4r = 0.
    # Curvature there: (1/4) · Σ binomial(4, k) · (-u_0^2) / u_0^4
    #                = (1/4) · 16 · (-1/u_0^2)
    #                = -4 / u_0^2
    u_0 = Fraction(8776, 10000)
    u_0_sq = u_0 * u_0

    m_star_at_r0 = Fraction(0)
    check(
        "r=0: m^* = -4 · 0 = 0 (extremum at the symmetric point)",
        m_star_at_r0 == 0,
    )

    curvature_at_r0 = Fraction(0)
    for k in range(5):
        mult = Fraction(binomial(4, k))
        # at r=0: (k-2)^2 r^2 = 0, so each term = (0 - u_0^2)/u_0^4 = -1/u_0^2
        curvature_at_r0 += mult * (-Fraction(1)) / u_0_sq
    curvature_at_r0 /= 4

    expected = -Fraction(4) / u_0_sq
    check(
        "r=0: d^2V^W/dm^2 |_{m^*=0} = -4/u_0^2 (matches parent eq. [3])",
        curvature_at_r0 == expected,
        f"got {curvature_at_r0}, expected {expected}",
    )


# ---------------------------------------------------------------------------
# Part 8: Forbidden-import audit
# ---------------------------------------------------------------------------
def part8_forbidden_imports():
    section("Part 8: stdlib-only / no PDG pins")
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

    suspicious = re.findall(
        r"\b(?:m_[a-z]+|alpha_[a-z]+|g_[a-z]+_obs)\s*=\s*\d+\.\d+\b",
        runner_text,
    )
    check(
        "no PDG-value pin pattern",
        not suspicious,
        f"matches: {suspicious}" if suspicious else "none",
    )


# ---------------------------------------------------------------------------
# Part 9: Boundary check — what this note explicitly does NOT close
# ---------------------------------------------------------------------------
def part9_boundary_check():
    section("Part 9: boundary check (what is NOT closed)")
    not_claimed = [
        "the physical Higgs mass `m_H` numerical value",
        "the `V_taste^W` extremum `m^*` to all orders in `r`",
        "the curvature at `m^*` to all orders in `r`",
        "the +12% Higgs gap chain",
        "the Wilson coefficient `r`",
        "the plaquette mean-field link `u_0`",
        "the staggered-Dirac realization gate",
        "the `g_bare = 1` derivation",
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


def main() -> int:
    banner("frontier_wilson_vtaste_extremum_leading_order_in_r.py")
    print(" Bounded source note: m^* = -4r + O(r^3); curvature there =")
    print("   -4/u_0^2 + 12 r^2 / u_0^4 + O(r^4). 5x smaller correction than")
    print("   at m=0, from variance identity Σ binom·(k-2)^2 = 16 vs Σ binom·k^2 = 80.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_premise_class_consistency()
    part4_binomial_moments()
    part5_extremum_shift_is_exact()
    part6_curvature_at_extremum()
    part6b_direct_nlo_coefficient_extraction()
    part7_r_zero_reduction()
    part8_forbidden_imports()
    part9_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: m^* = -4r EXACTLY (k → 4-k reflection symmetry on")
        print(" binomial(4,k) makes dV^W/dm |_{m=-4r} identically zero, all orders).")
        print(" d^2V^W/dm^2 |_{m=-4r} = -4/u_0^2 + 12 r^2/u_0^4 + O(r^4).")
        print(" Leading-r^2 coefficient pinned to 12 by direct extraction at r → 0.")
        print(" 5x smaller than at m=0 (variance vs raw second moment: 16 vs 80).")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
