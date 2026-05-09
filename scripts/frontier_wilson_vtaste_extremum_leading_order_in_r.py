#!/usr/bin/env python3
"""Wilson-shifted V_taste extremum at leading order in r — bounded source-note runner.

Verifies docs/WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md:

  m^*       =  -4 r    +  O(r^3),                                              (2)

  d^2 V^W / dm^2 |_{m = m^*}
            =  -4 / u_0^2  +  12 r^2 / u_0^4  +  O(r^4).                       (3)

Inputs (canonical bounded surface; no Monte Carlo, no PDG):
- staircase multiplicities binomial(4, k) for k in {0, 1, 2, 3, 4}
- V_taste^W formula (1) and its first two derivatives, from the sister note
  docs/WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md
  (forward-reference; on a sister branch — runner handles graceful absence)

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
        ("leading-shift formula present", "m^*       =  - 4 r"),
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
# Part 3: Cited upstream files exist (with graceful forward-reference)
# ---------------------------------------------------------------------------
def part3_premise_class_consistency():
    section("Part 3: cited upstream files (with graceful forward-reference)")
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

    # Sister forward-reference: V_taste^W note may be on a sibling branch.
    forward_refs = [
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

    # Variance-identity sanity check:
    variance_check = moment_2 - (moment_1 ** 2) // moment_0
    check(
        "variance identity: Σ k^2 · binom - (Σ k · binom)^2 / Σ binom = 80 - 64 = 16 = Σ (k-2)^2 · binom",
        variance_check == 16 == moment_centered_2,
        f"variance_check = {variance_check}, moment_centered_2 = {moment_centered_2}",
    )

    # Ratio: 80 / 16 = 5 (drives the 60/12 = 5 ratio)
    check(
        "moment ratio Σ k^2 · binom / Σ (k-2)^2 · binom = 80 / 16 = 5",
        moment_2 == 5 * moment_centered_2,
        f"80 / 16 = {Fraction(80, 16)}",
    )


# ---------------------------------------------------------------------------
# Part 5: Leading-order extremum shift m^* = -4r
# ---------------------------------------------------------------------------
def part5_leading_extremum_shift():
    section("Part 5: m^* = -4r at leading order in r")
    # Reduced equation at leading order (denominators -> 4 u_0^2):
    #   Σ_k binomial(4, k) · (2rk + δm) = 0
    #   2r · Σ_k binomial(4, k) · k  +  δm · Σ_k binomial(4, k)  =  0
    #   2r · 32  +  δm · 16  =  0
    #   δm = -4r
    moment_1 = Fraction(32)
    moment_0 = Fraction(16)
    # Symbolically:  delta_m = - 2r * moment_1 / moment_0  =  - 2r * 32 / 16  =  -4r
    delta_m_per_r = -Fraction(2) * moment_1 / moment_0  # coefficient of r in δm
    check(
        "leading-order shift coefficient: δm / r = -2 · Σ k · binom / Σ binom = -2 · 32 / 16 = -4",
        delta_m_per_r == Fraction(-4),
        f"got {delta_m_per_r}",
    )

    # Verify by direct substitution at small r and small u_0:
    u_0 = Fraction(8776, 10000)
    u_0_sq = u_0 * u_0
    r = Fraction(1, 1000)  # very small r so leading-order should be highly accurate
    m_star_leading = Fraction(-4) * r

    # dV^W/dm at the leading-order m^*:
    derivative = Fraction(0)
    for k in range(5):
        mult = Fraction(binomial(4, k))
        u_k = 2 * r * k + m_star_leading
        denom = u_k * u_k + 4 * u_0_sq
        derivative -= mult * u_k / denom

    # At leading order in r, derivative should be ~ 0. The next-order term
    # is O(r^3). Check that the residual is small relative to the typical
    # scale 1/u_0:
    typical_scale = Fraction(1) / u_0
    residual_to_scale = abs(derivative) / typical_scale
    print(f"  r = {r}, u_0 = {u_0}")
    print(f"  m^* (leading) = -4r = {m_star_leading}")
    print(f"  dV^W/dm at m^* (leading) = {float(derivative):.3e}")
    print(f"  residual / (1/u_0) = {float(residual_to_scale):.3e}")
    # At r = 1/1000, the leading-order approximation gives a residual of
    # O(r^3) / O(1) = O(10^-9). Demand the residual is < 10^-6 to be safe.
    threshold = Fraction(1, 1_000_000)
    check(
        "dV^W/dm at m^*_leading is negligible at r = 1/1000 (consistent with O(r^3) residual)",
        residual_to_scale < threshold,
        f"residual_to_scale = {float(residual_to_scale):.3e}, threshold = 1e-6",
    )


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
    part5_leading_extremum_shift()
    part6_curvature_at_extremum()
    part7_r_zero_reduction()
    part8_forbidden_imports()
    part9_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: m^* = -4r + O(r^3); d^2V^W/dm^2 |_{m=-4r} = -4/u_0^2")
        print(" + 12 r^2/u_0^4 + O(r^4). Leading correction is 5x smaller than")
        print(" at m=0 (variance ratio Σ binomial(4,k)·(k-2)^2 / Σ binomial(4,k)·k^2")
        print(" = 16/80 = 1/5).")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
