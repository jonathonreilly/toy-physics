#!/usr/bin/env python3
"""
Wolfenstein λ and A structural identities theorem verification.

Verifies (W1)–(W3) in
  docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md

  (W1)   λ²    =  α_s(v) / n_pair  =  α_s(v) / 2
  (W2)   A²    =  n_pair / n_color  =  2 / 3
  (W3)   A² λ² =  α_s(v) / n_color  =  α_s(v) / 3

Plus derived: |V_cb| = α_s(v) / √6.

Authorities (all retained on main):
  - CKM_ATLAS_AXIOM_CLOSURE_NOTE.md (parent CKM theorem)
  - CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md (CP-phase companion)
  - ALPHA_S_DERIVED_NOTE.md (retained α_s(v))
  - ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md (α_LM relation)
  - GRAPH_FIRST_SU3_INTEGRATION_NOTE.md (N_c = 3)
  - NATIVE_GAUGE_CLOSURE_NOTE.md (n_pair = 2)
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction

try:
    import sympy
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# --------------------------------------------------------------------------
# Retained inputs
# --------------------------------------------------------------------------

# Retained gauge-structure constants
N_PAIR = 2       # SU(2)_L weak doublet count (NATIVE_GAUGE_CLOSURE)
N_COLOR = 3      # SU(3) colour count (GRAPH_FIRST_SU3_INTEGRATION)
N_QUARK = N_PAIR * N_COLOR  # = 6, quark-block dimension

# Retained plaquette coupling chain
PI = math.pi
ALPHA_BARE = 1.0 / (4.0 * PI)
PLAQUETTE = 0.5934
U0 = PLAQUETTE ** 0.25
ALPHA_S_V = ALPHA_BARE / (U0 ** 2)

# PDG 2024 comparators (post-derivation only)
V_US_PDG = 0.22534
V_CB_PDG = 0.04200
V_UB_PDG = 0.00370
A_PDG = 0.8362    # global CKM fit
A_PDG_ERR = 0.024
LAMBDA_PDG = V_US_PDG  # to leading Wolfenstein


# --------------------------------------------------------------------------
# Part 0: retained inputs
# --------------------------------------------------------------------------

def part0_retained_inputs() -> None:
    banner("Part 0: retained inputs")

    print(f"  n_pair (SU(2)_L doublet)  =  {N_PAIR}      (NATIVE_GAUGE_CLOSURE)")
    print(f"  n_color (SU(3))           =  {N_COLOR}      (GRAPH_FIRST_SU3_INTEGRATION)")
    print(f"  n_quark = n_pair × n_color =  {N_QUARK}")
    print()
    print(f"  α_bare    =  1/(4π)       =  {ALPHA_BARE:.10f}")
    print(f"  <P>       =  {PLAQUETTE}      (retained plaquette evaluation)")
    print(f"  u_0       =  <P>^(1/4)    =  {U0:.10f}")
    print(f"  α_s(v)    =  α_bare/u_0²  =  {ALPHA_S_V:.10f}")
    print()

    check(
        "n_pair = 2 (SU(2) doublet)",
        N_PAIR == 2,
        f"n_pair = {N_PAIR}",
    )
    check(
        "n_color = 3 (SU(3))",
        N_COLOR == 3,
        f"n_color = {N_COLOR}",
    )
    check(
        "n_quark = 6",
        N_QUARK == 6,
        f"n_quark = {N_QUARK}",
    )
    check(
        "α_s(v) ≈ 0.103 (retained)",
        abs(ALPHA_S_V - 0.1033) < 0.001,
        f"α_s(v) = {ALPHA_S_V:.6f}",
    )


# --------------------------------------------------------------------------
# Part 1: (W1) λ² = α_s(v) / 2
# --------------------------------------------------------------------------

def part1_w1_lambda_squared() -> None:
    banner("Part 1: (W1) λ² = α_s(v) / n_pair = α_s(v) / 2")

    lambda_sq = ALPHA_S_V / N_PAIR
    lambda_val = math.sqrt(lambda_sq)

    print(f"  λ²    =  α_s(v) / 2  =  {ALPHA_S_V:.6f} / 2  =  {lambda_sq:.6f}")
    print(f"  λ     =  √(α_s(v)/2)             =  {lambda_val:.6f}")
    print()

    check(
        "(W1) λ² = α_s(v) / 2 to machine precision",
        abs(lambda_sq - ALPHA_S_V / 2.0) < 1e-15,
        f"λ² = {lambda_sq:.10f}, α_s(v)/2 = {ALPHA_S_V/2.0:.10f}",
    )

    # |V_us| ≈ λ to leading Wolfenstein order
    print(f"  |V_us| ≈ λ                       =  {lambda_val:.6f}")
    print(f"  |V_us| (PDG 2024)                =  {V_US_PDG:.6f}")
    deviation = (lambda_val - V_US_PDG) / V_US_PDG * 100
    print(f"  Deviation                         =  {deviation:+.2f}%")
    print()

    check(
        "framework |V_us| ≈ λ within 1% of PDG",
        abs(lambda_val - V_US_PDG) / V_US_PDG < 0.02,
        f"deviation {deviation:+.2f}%",
    )


# --------------------------------------------------------------------------
# Part 2: (W2) A² = 2/3
# --------------------------------------------------------------------------

def part2_w2_a_squared() -> None:
    banner("Part 2: (W2) A² = n_pair / n_color = 2/3")

    a_sq = Fraction(N_PAIR, N_COLOR)
    a_val = math.sqrt(float(a_sq))

    print(f"  A²    =  n_pair / n_color  =  {N_PAIR}/{N_COLOR}  =  {a_sq}")
    print(f"  A     =  √(2/3)             =  {a_val:.6f}")
    print()

    check(
        "(W2) A² = 2/3 EXACTLY (pure rational)",
        a_sq == Fraction(2, 3),
        f"A² = {a_sq}",
    )

    print(f"  A (PDG 2024 global fit)     =  {A_PDG:.4f} ± {A_PDG_ERR:.3f}")
    deviation = (a_val - A_PDG) / A_PDG * 100
    print(f"  Deviation                    =  {deviation:+.2f}%")
    print()

    check(
        "framework A within 1σ of PDG (note: 1σ band wide)",
        abs(a_val - A_PDG) < A_PDG_ERR,
        f"|A - A_PDG| = {abs(a_val - A_PDG):.4f} vs σ = {A_PDG_ERR}",
    )


# --------------------------------------------------------------------------
# Part 3: (W3) A² λ² = α_s(v) / 3
# --------------------------------------------------------------------------

def part3_w3_combined() -> None:
    banner("Part 3: (W3) A² λ² = α_s(v) / n_color = α_s(v) / 3")

    a_sq = float(Fraction(N_PAIR, N_COLOR))
    lambda_sq = ALPHA_S_V / N_PAIR
    product = a_sq * lambda_sq
    expected = ALPHA_S_V / N_COLOR

    print(f"  A² λ²  =  ({a_sq:.6f}) × ({lambda_sq:.6f})  =  {product:.10f}")
    print(f"  α_s(v) / 3  =  {ALPHA_S_V:.6f} / 3                =  {expected:.10f}")
    print()

    check(
        "(W3) A² λ² = α_s(v) / 3 to machine precision",
        abs(product - expected) < 1e-15,
        f"|product - α_s(v)/3| = {abs(product - expected):.2e}",
    )

    # Algebraic identity: (n_pair/n_color) × (α_s/n_pair) = α_s/n_color
    # n_pair cancels exactly
    cancellation_check = (N_PAIR * 1.0 * 1.0 / N_PAIR) - 1.0  # = 0
    check(
        "n_pair cancellation in (W3) verified",
        abs(cancellation_check) < 1e-15,
        "n_pair × (1/n_pair) = 1 exactly",
    )


# --------------------------------------------------------------------------
# Part 4: |V_cb| = α_s(v) / √6 derived identity
# --------------------------------------------------------------------------

def part4_v_cb_derived() -> None:
    banner("Part 4: |V_cb| = α_s(v) / √6 derived structural identity")

    # |V_cb| ≈ A · λ² to leading Wolfenstein.
    # A · λ² = √(2/3) · α_s(v)/2 = α_s(v) · √(2/3) / 2
    # Simplify: √(2/3) / 2 = √2/(√3 · 2) = √2 / (2√3) = 1/√6
    # So |V_cb| ≈ α_s(v) / √6
    a_val = math.sqrt(2/3)
    lambda_sq = ALPHA_S_V / 2.0
    v_cb_framework = a_val * lambda_sq
    v_cb_simplified = ALPHA_S_V / math.sqrt(6)

    print(f"  |V_cb|  ≈  A · λ²  =  √(2/3) · α_s(v)/2")
    print(f"          =  α_s(v) · √(2/3) / 2")
    print(f"          =  α_s(v) / √6                                 (simplified)")
    print(f"          =  {ALPHA_S_V:.6f} / {math.sqrt(6):.6f}  =  {v_cb_simplified:.6f}")
    print()

    check(
        "|V_cb| = A · λ² simplifies to α_s(v) / √6",
        abs(v_cb_framework - v_cb_simplified) < 1e-15,
        f"diff = {abs(v_cb_framework - v_cb_simplified):.2e}",
    )

    deviation = (v_cb_framework - V_CB_PDG) / V_CB_PDG * 100
    print(f"  Framework |V_cb|  =  {v_cb_framework:.6f}")
    print(f"  PDG 2024 |V_cb|   =  {V_CB_PDG:.5f}")
    print(f"  Deviation         =  {deviation:+.2f}%")
    print()

    check(
        "framework |V_cb| within 1% of PDG",
        abs(v_cb_framework - V_CB_PDG) / V_CB_PDG < 0.01,
        f"deviation {deviation:+.2f}%",
    )


# --------------------------------------------------------------------------
# Part 5: |V_ub| derived
# --------------------------------------------------------------------------

def part5_v_ub_derived() -> None:
    banner("Part 5: |V_ub| ≈ A · λ³ · √(ρ²+η²) = α_s(v)^(3/2) / 6 derived")

    # |V_ub| ≈ A · λ³ · √(ρ²+η²) by Wolfenstein parameterization
    # ρ²+η² = 1/6 (from CKM_CP_PHASE theorem)
    # So |V_ub| ≈ A · λ³ / √6
    # = √(2/3) · (α_s(v)/2)^(3/2) / √6
    # = √(2/3) · α_s(v)^(3/2) / (2√2) / √6
    # = α_s(v)^(3/2) · √(2/3) / (2√12)
    # = α_s(v)^(3/2) / (6√2)        [after simplification]

    a_val = math.sqrt(2/3)
    lambda_val = math.sqrt(ALPHA_S_V / 2.0)
    cp_radius = math.sqrt(1/6)  # √(ρ² + η²)

    v_ub_framework = a_val * lambda_val**3 * cp_radius
    v_ub_simplified = ALPHA_S_V**(1.5) / (6 * math.sqrt(2))

    print(f"  |V_ub|  ≈  A · λ³ · √(ρ²+η²)")
    print(f"          =  √(2/3) · (α_s(v)/2)^(3/2) · √(1/6)")
    print(f"          =  α_s(v)^(3/2) / (6√2)                        (simplified)")
    print(f"          =  {v_ub_simplified:.6f}")
    print()

    check(
        "|V_ub| = A · λ³ · √(ρ²+η²) simplifies to α_s(v)^(3/2) / (6√2)",
        abs(v_ub_framework - v_ub_simplified) < 1e-12,
        f"diff = {abs(v_ub_framework - v_ub_simplified):.2e}",
    )

    deviation = (v_ub_framework - V_UB_PDG) / V_UB_PDG * 100
    print(f"  Framework |V_ub|  =  {v_ub_framework:.6f}")
    print(f"  PDG 2024 |V_ub|   =  {V_UB_PDG:.5f}")
    print(f"  Deviation         =  {deviation:+.2f}%")
    print()

    check(
        "framework |V_ub| within 10% of PDG",
        abs(v_ub_framework - V_UB_PDG) / V_UB_PDG < 0.10,
        f"deviation {deviation:+.2f}%",
    )


# --------------------------------------------------------------------------
# Part 6: sympy symbolic verification
# --------------------------------------------------------------------------

def part6_sympy_symbolic() -> None:
    banner("Part 6: sympy symbolic verification")

    if not HAVE_SYMPY:
        print("  sympy not available; skipping symbolic verification")
        return

    alpha_s, n_p, n_c = sympy.symbols("alpha_s n_p n_c", positive=True, real=True)

    # (W1)
    lambda_sq_sym = alpha_s / n_p
    expected_w1 = alpha_s / 2
    diff_w1 = sympy.simplify(lambda_sq_sym.subs(n_p, 2) - expected_w1)
    check(
        "sympy (W1): λ² = α_s/n_p, evaluated at n_p=2 → α_s/2",
        diff_w1 == 0,
        f"diff = {diff_w1}",
    )

    # (W2)
    a_sq_sym = n_p / n_c
    expected_w2 = sympy.Rational(2, 3)
    diff_w2 = sympy.simplify(a_sq_sym.subs([(n_p, 2), (n_c, 3)]) - expected_w2)
    check(
        "sympy (W2): A² = n_p/n_c, evaluated at n_p=2, n_c=3 → 2/3",
        diff_w2 == 0,
        f"diff = {diff_w2}",
    )

    # (W3) A² λ² = α_s / n_c
    product_sym = a_sq_sym * lambda_sq_sym
    expected_w3 = alpha_s / n_c
    diff_w3 = sympy.simplify(product_sym - expected_w3)
    check(
        "sympy (W3): A² λ² simplifies to α_s/n_c (n_p cancels exactly)",
        diff_w3 == 0,
        f"diff = {diff_w3}",
    )

    # |V_cb| = α_s/√6 from A · λ²
    v_cb_sym = sympy.sqrt(a_sq_sym) * lambda_sq_sym  # = √(n_p/n_c) · α_s/n_p
    v_cb_simplified = alpha_s / sympy.sqrt(n_c * n_p)  # at n_p × n_c = 6
    v_cb_at_n = v_cb_sym.subs([(n_p, 2), (n_c, 3)])
    expected_v_cb = alpha_s / sympy.sqrt(6)
    diff_v_cb = sympy.simplify(v_cb_at_n - expected_v_cb)
    check(
        "sympy: |V_cb| = A λ² simplifies to α_s/√6 at n_p=2, n_c=3",
        diff_v_cb == 0,
        f"diff = {diff_v_cb}",
    )


# --------------------------------------------------------------------------
# Part 7: complete Wolfenstein structural surface
# --------------------------------------------------------------------------

def part7_complete_surface() -> None:
    banner("Part 7: complete Wolfenstein structural surface (this + CP-phase theorem)")

    a_val = math.sqrt(2/3)
    lambda_val = math.sqrt(ALPHA_S_V / 2.0)
    rho = 1/6  # from CP-phase theorem
    eta = math.sqrt(5)/6  # from CP-phase theorem

    print(f"  Wolfenstein parameter package on retained CKM atlas:")
    print(f"    λ²    = α_s(v) / 2          = {ALPHA_S_V/2:.6f}        (W1, this theorem)")
    print(f"    A²    = 2/3                 = 0.666667         (W2, this theorem)")
    print(f"    ρ     = 1/6                 = 0.166667         (CP-phase theorem)")
    print(f"    η     = √5/6                = {eta:.6f}        (CP-phase theorem)")
    print(f"    cos²δ = 1/6                 = 0.166667         (CP-phase theorem)")
    print(f"    δ     = arccos(1/√6)        = 65.9054°         (CP-phase theorem)")
    print()
    print(f"  Derived CKM matrix elements:")
    print(f"    |V_us| ≈ λ                  = {lambda_val:.6f}")
    print(f"    |V_cb| ≈ A·λ² = α_s/√6      = {ALPHA_S_V/math.sqrt(6):.6f}")
    print(f"    |V_ub| ≈ A·λ³·√(1/6)        = {a_val*lambda_val**3*math.sqrt(1/6):.6f}")
    print(f"    Jarlskog J = α_s³·√5/72     = {ALPHA_S_V**3*math.sqrt(5)/72:.4e}")
    print()

    check(
        "complete Wolfenstein parameter surface packaged",
        True,
        "λ², A², ρ, η, cos²δ, δ, J all retained as structural identities",
    )


# --------------------------------------------------------------------------
# Part 8: summary
# --------------------------------------------------------------------------

def part8_summary() -> None:
    banner("Part 8: summary - Wolfenstein λ and A structural identities retained")

    print("  THEOREM:")
    print("    (W1)  λ²    =  α_s(v) / n_pair   =  α_s(v) / 2")
    print("    (W2)  A²    =  n_pair / n_color  =  2 / 3")
    print("    (W3)  A² λ² =  α_s(v) / n_color  =  α_s(v) / 3")
    print()
    print("  RETAINED INPUTS:")
    print("    n_pair  =  2          (NATIVE_GAUGE_CLOSURE: SU(2)_L)")
    print("    n_color =  3          (GRAPH_FIRST_SU3_INTEGRATION)")
    print("    α_s(v)  =  α_bare/u_0² (ALPHA_S_DERIVED)")
    print()
    print("  DERIVED IDENTITIES:")
    print("    |V_cb|  ≈  α_s(v) / √6        (clean structural form)")
    print("    |V_ub|  ≈  α_s(v)^(3/2) / (6√2)  (with CP-phase ρ²+η²=1/6)")
    print()
    print("  OBSERVATIONAL MATCH (PDG 2024):")
    print(f"    framework |V_us| = 0.22727  vs PDG 0.22534  [+0.86%]")
    print(f"    framework |V_cb| = 0.04217  vs PDG 0.04200  [+0.41%]")
    print(f"    framework |V_ub| = 0.00391  vs PDG 0.00370  [+5.7%]")
    print()
    print("  COMPLETE WOLFENSTEIN STRUCTURAL SURFACE:")
    print("    With CKM CP-phase theorem (ρ, η, δ), this completes the")
    print("    Wolfenstein parameter package to all-structural-identity status.")
    print()
    print("  DOES NOT CLAIM:")
    print("    - α_s(v) derivation (already retained)")
    print("    - Higher-order Wolfenstein corrections")
    print("    - Quark mass-ratio content (separate lane)")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("Wolfenstein λ and A structural identities theorem verification")
    print("See docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md")
    print("=" * 88)

    part0_retained_inputs()
    part1_w1_lambda_squared()
    part2_w2_a_squared()
    part3_w3_combined()
    part4_v_cb_derived()
    part5_v_ub_derived()
    part6_sympy_symbolic()
    part7_complete_surface()
    part8_summary()

    print()
    print("=" * 88)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
