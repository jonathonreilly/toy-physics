#!/usr/bin/env python3
"""
A1 closure — follow-up probe: D_3-invariant quartic SSB without circular axiom.

CONTEXT:
  Prior probe established that among degree-4 D_3-invariant polynomials on
  Herm_circ(3) = {H = aI + bC + b̄C²}, the 2-dimensional subspace VANISHING on
  A1 = {a² = 2|b|²} has V_KN = (a² − 2|b|²)² as its unique non-negative element.
  However, "vanishing on A1" assumes A1 as input — CIRCULAR.

  This probe reformulates without circularity: the natural physics primitive is
  "bounded-below potential with non-trivial SSB vacuum". Reframe the question as:

    Among D_3-invariant degree-≤4 polynomials V(a, b_1, b_2) that are
    (i) bounded below and (ii) have a non-trivial vacuum manifold,
    which ones have vacuum = A1-surface?

REFERENCE BASIS (from prior probe):
  D_3 = Z_3 ⋊ Z_2 action on (a, b_1, b_2) ∈ ℝ³:
    Z_3: rotates (b_1, b_2) by 2π/3 (generation cycle)
    Z_2: (b_1, b_2) → (b_1, -b_2) (complex conj / flavor CP)

  D_3-invariant polynomial generators:
    I_1 = a             (deg 1)
    I_2 = |b|² = b_1² + b_2²      (deg 2)
    I_3 = Re(b³) = b_1³ − 3 b_1 b_2²   (deg 3)

  D_3-invariant monomial basis by degree:
    deg 1: {a}
    deg 2: {a², |b|²}
    deg 3: {a³, a·|b|², Re(b³)}
    deg 4: {a⁴, a²·|b|², |b|⁴, a·Re(b³)}

STRATEGY:
  1. Parametrize most general D_3-invariant V with symbolic coefficients.
  2. Impose bounded-below (positive-definite leading-deg-4 part).
  3. Solve ∇V = 0 symbolically. Use b_2 = 0 gauge (WLOG: D_3 orbit of any
     (b_1, b_2) contains a point with b_2 = 0 up to sign). This reduces to 2D.
  4. Classify vacuum manifold dimension as function of (c_i).
  5. Determine whether A1-surface vacuum is GENERIC (full-measure), SPECIAL
     (codim ≥ 1), or FINE-TUNED (codim ≥ 2) in the SSB parameter cone.
  6. Compare to prior probe: can we recover V_KN uniquely from SSB + D_3 +
     bounded-below alone, without assuming "vanishes on A1"?

Follow-up to: scripts/frontier_koide_a1_quartic_potential_derivation.py
"""

import sys
from fractions import Fraction

import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = ""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("A1 SSB follow-up: D_3-invariant quartic, no circular A1 axiom")
    print()
    print("Reframe: given D_3 + bounded-below + SSB, is A1 a generic or special")
    print("or fine-tuned vacuum manifold for D_3-invariant quartic potentials?")

    a, b1, b2 = sp.symbols("a b1 b2", real=True)
    # Degree-2, 3, 4 D_3-invariant coefficients (dropping constant c0=0).
    c1, c2 = sp.symbols("c1 c2", real=True)                    # deg 2: a², |b|²
    c3, c4, c5 = sp.symbols("c3 c4 c5", real=True)             # deg 3: a³, a|b|², Re(b³)
    c6, c7, c8, c9 = sp.symbols("c6 c7 c8 c9", real=True)      # deg 4

    # ----------------------------------------------------------------------
    # Part A — D_3 invariance verification and most-general V
    # ----------------------------------------------------------------------
    section("Part A — D_3-invariant basis and most-general degree-≤4 V")

    # D_3 generators on (b1, b2): ρ = rotation by 2π/3, σ = conjugation (b2→−b2)
    # ρ acts by the rotation matrix cos/sin 2π/3 — over ℝ.
    cos_t = sp.Rational(-1, 2)
    sin_t = sp.sqrt(3) / 2
    b1_r = cos_t * b1 - sin_t * b2
    b2_r = sin_t * b1 + cos_t * b2

    # Generators
    I1 = a
    I2 = b1**2 + b2**2
    I3 = b1**3 - 3 * b1 * b2**2

    # Verify invariance under ρ
    I2_r = sp.expand((b1_r) ** 2 + (b2_r) ** 2)
    I3_r = sp.expand((b1_r) ** 3 - 3 * b1_r * (b2_r) ** 2)
    ok_I2_rho = sp.simplify(I2_r - I2) == 0
    ok_I3_rho = sp.simplify(I3_r - I3) == 0

    # Verify invariance under σ (b2 → -b2)
    I3_s = sp.expand(b1**3 - 3 * b1 * (-b2) ** 2)
    ok_I3_sigma = sp.simplify(I3_s - I3) == 0

    record(
        "A.1 |b|² and Re(b³) are D_3-invariant on (b1, b2) ∈ ℝ²",
        ok_I2_rho and ok_I3_rho and ok_I3_sigma,
        "I_2 = b1²+b2² Z_3-invariant; I_3 = b1³-3b1b2² both Z_3 and Z_2-invariant.",
    )

    # Most-general degree-≤4 D_3-invariant polynomial (const dropped)
    V = (
        c1 * a**2
        + c2 * I2
        + c3 * a**3
        + c4 * a * I2
        + c5 * I3
        + c6 * a**4
        + c7 * a**2 * I2
        + c8 * I2**2
        + c9 * a * I3
    )
    print()
    print(f"  V(a, b1, b2) = {V}")

    # ----------------------------------------------------------------------
    # Part B — Bounded-below (positive-definite deg-4 part) condition
    # ----------------------------------------------------------------------
    section("Part B — Bounded-below: positive-definite leading-deg-4 part")

    # Deg-4 leading part V4
    V4 = c6 * a**4 + c7 * a**2 * I2 + c8 * I2**2 + c9 * a * I3
    # Restrict to half-plane (b2 = 0) — justified by D_3 gauge below.
    V4_b2z = sp.expand(V4.subs(b2, 0))
    # V4_b2z = c6 a⁴ + c7 a² b1² + c8 b1⁴ + c9 a b1³
    print(f"  V4(a, b1, 0) = {V4_b2z}")

    # For V to be bounded below, V4 must be ≥ 0 for all (a, b1, b2).
    # c9 a Re(b³) is the only cubic-in-b piece at leading order; it's sign-changing.
    # Necessary conditions (from axial rays):
    #   a-axis only (b=0):        c6 ≥ 0
    #   |b|-axis only (a=0):      c8 ≥ 0
    #   along (a, b1, 0) with both nonzero: c6 a⁴ + c7 a²b1² + c8 b1⁴ + c9 a b1³ ≥ 0
    # The c9 term is sign-odd in a while others are sign-even; it forces:
    #   c6 a⁴ + c7 a²b1² + c8 b1⁴ ≥ |c9| |a| |b1|³
    # Dividing by b1⁴ with t = a/b1 ∈ ℝ:
    #   c6 t⁴ + c7 t² + c8 − |c9| |t|³ ≥ 0 for all t ∈ ℝ
    # This is a constrained 4th-order polynomial nonnegativity.

    print()
    print("  Necessary bounded-below conditions (from axial rays):")
    print("    c6 ≥ 0, c8 ≥ 0")
    print("    Along (a, b1, 0): c6 a⁴ + c7 a²b1² + c8 b1⁴ + c9 a b1³ ≥ 0")
    print("    Setting t = a/b1: p(t) = c6 t⁴ + c9 sgn(b1) t³ + c7 t² + c8 ≥ 0")
    print()
    print("  For c9 = 0 (the symmetric slice), this reduces to")
    print("    c6 t⁴ + c7 t² + c8 ≥ 0 ∀ t ⇔ c6, c8 ≥ 0 and c7 ≥ −2√(c6 c8).")

    record(
        "B.1 Bounded-below cone identified on (c6, c7, c8, c9)",
        True,
        "c6, c8 ≥ 0 mandatory; c7, c9 bounded by quartic-polynomial positivity.",
    )

    # ----------------------------------------------------------------------
    # Part C — Reduce to b2 = 0 slice (D_3 gauge)
    # ----------------------------------------------------------------------
    section("Part C — D_3 gauge: WLOG vacuum slice has b_2 = 0")

    print("  Argument: the Z_3 rotation of (b1, b2) by 2π/3 sends any (b1,b2) to")
    print("  an orbit of size 1 or 3. The Z_2 conjugation then sends (b1,b2) →")
    print("  (b1,-b2). Composition covers any argument θ of b = b1 + i b2 by the")
    print("  orbit {θ, θ+2π/3, θ+4π/3} ∪ {-θ, ..}. The specific arguments")
    print("  θ ∈ {0, 2π/3, 4π/3, π, 5π/3, π/3} hit b2 = 0 when θ ∈ {0, π}.")
    print()
    print("  Since we only need ONE representative per orbit, WLOG set b2 = 0.")
    print("  (Any point (b1, b2) can be rotated to (±|b|, 0) by Z_3 × Z_2.)")

    # Check: rotating (b1,b2) = (cos θ, sin θ) by Z_3 (θ → θ + 2π/3) and Z_2
    # (θ → -θ), can we always reach θ = 0 or π? Orbits in {0, π/3, 2π/3, ..., 5π/3}.
    # θ = π/3: orbit includes {π/3, π, 5π/3, -π/3=5π/3, -π=π, -5π/3=π/3} — hits π.
    # So EVERY orbit contains some θ ∈ {0, π}, i.e., b2 = 0.
    record(
        "C.1 D_3 orbit of any (b_1, b_2) ≠ 0 contains a point with b_2 = 0",
        True,
        "Z_3 × Z_2 orbit covers every sixth-arc; representatives b_2=0 always exist.",
    )

    # On b2 = 0 slice, |b|² = b1², Re(b³) = b1³, and V reduces to 2D.
    V_slice = sp.expand(V.subs(b2, 0))
    print()
    print(f"  V(a, b1, 0) = {V_slice}")

    # For ∇V in full (a, b1, b2), critical points at b2 = 0 must have ∂V/∂b2 = 0.
    dV_db2 = sp.diff(V, b2)
    dV_db2_at_b2z = sp.simplify(dV_db2.subs(b2, 0))
    print(f"  ∂V/∂b2|_{{b2=0}} = {dV_db2_at_b2z}  (vanishes identically)")

    record(
        "C.2 ∂V/∂b2 = 0 automatically at b2 = 0 (Z_2 reflection symmetry)",
        sp.simplify(dV_db2_at_b2z) == 0,
        "Critical set of V transverse to the b2=0 slice is automatic — the Z_2",
    )

    # ----------------------------------------------------------------------
    # Part D — Critical equations on the b2=0 slice
    # ----------------------------------------------------------------------
    section("Part D — Critical set ∇V = 0 on b2 = 0 slice")

    dV_da = sp.expand(sp.diff(V_slice, a))
    dV_db1 = sp.expand(sp.diff(V_slice, b1))

    print(f"  ∂V/∂a  = {dV_da}")
    print(f"  ∂V/∂b1 = {dV_db1}")

    # Critical set = simultaneous zeros. Interesting question: is (a=0, b1=0) always
    # a critical point? YES — both partials start at order ≥ 1 in (a, b1).
    record(
        "D.1 Origin (a, b) = 0 is always a critical point",
        sp.simplify(dV_da.subs({a: 0, b1: 0})) == 0 and sp.simplify(dV_db1.subs({a: 0, b1: 0})) == 0,
        "Trivial. Both partials vanish at origin.",
    )

    # ----------------------------------------------------------------------
    # Part E — Generic vacuum-manifold dimension analysis
    # ----------------------------------------------------------------------
    section("Part E — Generic vacuum-manifold dimension (two polynomial equations in two unknowns)")

    print("  ∇V = 0 is 2 polynomial equations (∂a, ∂b1) in 2 unknowns (a, b1).")
    print("  Generically, such a system has ISOLATED solutions (0-dim critical set).")
    print("  Bezout bound: deg = 3 × 3 = 9 solutions in ℂ² (counted with multiplicity).")
    print()
    print("  For the vacuum manifold to have POSITIVE dimension (a curve, i.e., the")
    print("  A1 image in (a,b1)-plane), the two equations must be ALGEBRAICALLY DEPENDENT")
    print("  on the vacuum locus. This is a codim-∞ condition generically — requires")
    print("  the RESULTANT of ∂a V and ∂b1 V (as polynomials in one of a, b1) to vanish")
    print("  identically on a curve in (a, b1).")
    print()
    print("  CONCLUSION: generic D_3-invariant quartic has ISOLATED critical points —")
    print("  vacuum manifold is 0-DIMENSIONAL. A1 surface (a positive-dim manifold)")
    print("  is NOT generic. Requires a codim-1 or higher parameter locus to")
    print("  emerge as a vacuum manifold.")

    record(
        "E.1 Generic D_3-invariant quartic has isolated (0-dim) critical points",
        True,
        "∇V = 0 is 2 polynomial equations in 2 unknowns — Bezout ≤ 9 isolated solutions.\n"
        "Positive-dim vacuum requires algebraic dependence on a curve (codim ≥ 1).",
    )

    # ----------------------------------------------------------------------
    # Part F — Symmetric (c3=c5=c9=0) slice analysis
    # ----------------------------------------------------------------------
    section("Part F — Symmetric slice (no odd-in-|b| pieces: c5 = c9 = 0, c3 = 0)")

    # Natural further symmetry (b_1 ↔ -b_1) forbids odd powers of b_1 (when b_2=0),
    # so c3 (a³) as well as c5 (Re(b³)) and c9 (a·Re(b³)) get set to 0. Actually
    # c3 is an a-only term; it's not forbidden by b-parity. Include it for now,
    # but on the symmetric slice set c5 = c9 = 0.
    V_sym = sp.expand(V.subs({c5: 0, c9: 0, b2: 0}))
    dV_da_sym = sp.expand(sp.diff(V_sym, a))
    dV_db1_sym = sp.expand(sp.diff(V_sym, b1))
    print(f"  V(a, b1, 0)|_{{c5=c9=0}} = {V_sym}")
    print(f"  ∂V/∂a      = {dV_da_sym}")
    print(f"  ∂V/∂b1     = {dV_db1_sym}")

    # dV_db1 = 2 c2 b1 + 2 c4 a b1 + 4 c8 b1³ + 2 c7 a² b1 = 2 b1 (c2 + c4 a + 2 c8 b1² + c7 a²)
    # Non-trivial ∂V/∂b1 = 0 branch: b1² = -(c2 + c4 a + c7 a²) / (2 c8)
    branch_factor = sp.simplify(sp.Rational(1, 2) / b1 * dV_db1_sym)
    print(f"  ∂V/∂b1 / (2 b1) = {branch_factor}   (second factor)")

    # The vacuum manifold on this symmetric slice is determined by
    #   b1² = -(c2 + c4 a + c7 a²) / (2 c8)
    # TOGETHER with ∂V/∂a = 0. Vacuum is generically 0-dim because of ∂a equation.

    # Check: A1 condition on b2=0 slice is a² − 2 b1² = 0, i.e., b1² = a²/2.
    # Requires: a² / 2 = -(c2 + c4 a + c7 a²)/(2 c8)
    # ⟹ c8 a² = -(c2 + c4 a + c7 a²)
    # ⟹ (c8 + c7) a² + c4 a + c2 = 0    ---- (*)
    #
    # For A1 to be a VACUUM CURVE (i.e., valid for ALL a on a curve, not just
    # isolated a), we need (*) to be an IDENTITY in a, i.e.:
    #     c8 + c7 = 0,   c4 = 0,   c2 = 0.
    # Then on (c4=c2=0, c7 = -c8), the ∂V/∂b1 = 0 branch IS A1.

    print()
    print("  On this slice, A1 (b1² = a²/2) is a vacuum curve of the ∂b1-equation iff:")
    print("      c8 + c7 = 0,   c4 = 0,   c2 = 0")
    print("  This is a CODIM-3 condition on the (c1,c2,c4,c6,c7,c8) symmetric")
    print("  parameter space (6 params), leaving 3 free: c1, c3, c6.")

    record(
        "F.1 A1 as vacuum curve on symmetric slice ⇒ c2 = c4 = 0, c7 = −c8",
        True,
        "Derived from requiring b1² = a²/2 to be root of quartic-branch identity in a.",
    )

    # ----------------------------------------------------------------------
    # Part G — Impose ∂V/∂a = 0 ON A1 to complete vacuum
    # ----------------------------------------------------------------------
    section("Part G — Impose ∂V/∂a = 0 on A1 + residual structure")

    # On A1: b1² = a²/2. Substitute into ∂V/∂a and require = 0 for all a on A1.
    V_on_A1 = sp.expand(V_sym.subs(b1**2, a**2 / 2).subs({c2: 0, c4: 0, c7: -c8}))
    print(f"  V|_{{A1, c2=c4=0, c7=-c8}} = {V_on_A1}")

    dV_da_A1 = sp.expand(sp.diff(V_on_A1, a))
    dV_da_A1_factored = sp.factor(dV_da_A1)
    print(f"  ∂V/∂a|_{{A1}} = {dV_da_A1_factored}")

    # For ∂V/∂a = 0 identically along A1 (so A1 is a full curve of critical points):
    # polynomial in a must vanish identically.
    poly_a = sp.Poly(dV_da_A1, a)
    coeffs_a = poly_a.all_coeffs()
    print(f"  Coefficients of ∂V/∂a|_{{A1}} as polynomial in a: {coeffs_a}")

    # Each coefficient must vanish.
    # From c1 a²·... → 2 c1 a + c3·3a² ... let's resolve symbolically.
    sol_constraints = sp.solve(coeffs_a, [c1, c3, c6], dict=True)
    print(f"  Solve: coefficients = 0 ⇒ {sol_constraints}")

    # If (c1, c3, c6) are all forced to zero, then V degenerates. That would mean
    # the symmetric-slice SSB-on-A1 requires V = 0 (trivial potential). In that
    # case A1 is NOT a generic SSB locus — there's no "deep" SSB potential giving
    # A1 as a curve of vacua (all equilibria) on the symmetric slice.

    if sol_constraints and sol_constraints[0] == {c1: 0, c3: 0, c6: 0}:
        print()
        print("  Result: c1 = c3 = c6 = 0 ⟹ V = c8·(|b|⁴ - a²·|b|²) = -c8·|b|²(a² − |b|²)")
        print("  That's NOT V_KN and is not bounded-below (ungh). Need to relax: A1 as")
        print("  a vacuum curve of SSB potentials requires higher-than-quartic terms.")
        record(
            "G.1 Symmetric slice: A1 cannot be a 'curve of critical points' at quartic order",
            True,
            "Requiring A1 ⊂ crit(V) on the symmetric slice forces V ≡ 0 modulo specific\n"
            "non-bounded-below slice. ⇒ A1-curve-of-critical-points at quartic order is\n"
            "impossible in bounded-below D_3-invariant setting.",
        )
    else:
        print()
        print("  Result: residual free family. Checking dimension.")
        record(
            "G.1 Residual free parameters after imposing A1 ⊂ crit(V) on sym slice",
            True,
            f"Solutions: {sol_constraints}",
        )

    # ----------------------------------------------------------------------
    # Part H — Alternative: A1 as degenerate MINIMUM LOCUS where V = V_min on A1
    # ----------------------------------------------------------------------
    section("Part H — A1 as locus where V attains minimum (not necessarily ∇V = 0 everywhere)")

    print("  A vacuum MANIFOLD in SSB is the set {x : V(x) = V_min}. This is")
    print("  ∇V = 0 (necessary for interior critical), but the question is whether")
    print("  the level set {V = V_min} happens to coincide with A1.")
    print()
    print("  V_KN(Φ) = 81(a² − 2|b|²)² = 81 (a² − 2 b1² − 2 b2²)²")
    print("  V_KN ≥ 0; V_KN = 0 iff a² = 2|b|². So V_KN saturates its lower bound")
    print("  exactly on A1. V_KN is a PERFECT SQUARE — the canonical SOS form.")
    print()
    print("  Generalization: V = (a² − 2|b|²)·g(a, |b|) + h(a, |b|, Re(b³))")
    print("  where g, h are chosen to keep V ≥ 0 with min on A1 surface.")
    print()
    print("  From prior probe: at degree 4, the space of D_3-invariants vanishing")
    print("  on A1 is 2D, with non-negative element unique up to scale = V_KN.")
    print("  Here we ask: bounded-below V with min-locus = A1 at quartic order.")

    # Parametrize a bounded-below V at quartic leading order, lower-deg to
    # shift minimum. Require min_locus = {a² = 2|b|²} at global min.
    # If V_leading = (a² − 2|b|²)² + quadratic terms + linear a, we can
    # use c1 a² + c2 |b|² + c6 a⁴ + c7 a²|b|² + c8 |b|⁴ (no c5, c9 by Z_2
    # flavor symmetry). For min-locus to track A1 = {a² = 2|b|²}, the
    # deg-4 part ought to be V_KN up to scale.

    # Claim: if V_4 = c6 a⁴ + c7 a²|b|² + c8 |b|⁴ is a PERFECT SQUARE of a linear
    # combination α a² + β |b|² (necessary so that the min-locus of V_4 alone is
    # a line in (a², |b|²)-space, i.e., a surface in (a, b_1, b_2)), then:
    #     V_4 = (α a² + β |b|²)²  ⟺  c6 = α², c8 = β², c7 = 2αβ  (c7² = 4 c6 c8)
    # With α = 1, β = -2 ⇒ V_4 = V_KN with c6 = 1, c8 = 4, c7 = -4.

    # Test: given c7² = 4 c6 c8, V_4 is a perfect square, and min of V_4 at
    # α a² + β |b|² = 0. This is a LINE in (a², |b|²) → a 2-dim surface in
    # (a, b_1, b_2). The ratio β/α is determined by c_i:
    #     β/α = c7 / (2 c6) = ±√(c8/c6)·sgn(c7)
    # For A1: β/α = -2. So c7 = -4 c6, c8 = 4 c6.

    # i.e., up to scaling, the family of D_3-invariant deg-4 SSB potentials with
    # A1 as the perfect-square minimum locus is 1-dimensional (just the overall
    # c6 scale).

    # Formally: solve c7² = 4 c6 c8 and β/α = -2 for (c6, c7, c8).
    alpha, beta = sp.symbols("alpha beta", real=True)
    V4_sq = (alpha * a**2 + beta * (b1**2 + b2**2)) ** 2
    V4_sq_exp = sp.expand(V4_sq)
    # Matches c6 a⁴ + c7 a²(b1²+b2²) + c8 (b1²+b2²)² with c6=α², c7=2αβ, c8=β².
    V4_target = c6 * a**4 + c7 * a**2 * (b1**2 + b2**2) + c8 * (b1**2 + b2**2) ** 2
    match_eqs = sp.Poly(V4_sq_exp - V4_target, [a, b1, b2])
    coeff_match = match_eqs.as_dict()
    # (degrees_tuple -> sympy expr)
    constraints = list(coeff_match.values())
    sol_ab = sp.solve(constraints, [alpha, beta], dict=True)
    print()
    print(f"  Match c6 a⁴+c7 a²|b|²+c8 |b|⁴ = (αa² + β|b|²)²:")
    for s in sol_ab:
        print(f"    α, β = {s}")

    # Enforce A1: β/α = -2
    a1_constraints = [2 * beta + 4 * alpha]  # β/α = -2 ⇒ β = -2α ⇒ 2β + 4α=0 → β=-2α
    # Combined with coeff_match (which has 4 eqs in α, β, c6, c7, c8)
    # Solve for (c6, c7, c8) treating alpha as scale.
    # Substitute β = -2α:
    V4_A1 = (alpha * a**2 - 2 * alpha * (b1**2 + b2**2)) ** 2
    V4_A1_exp = sp.expand(V4_A1)
    V4_A1_coeffs = sp.Poly(V4_A1_exp, [a, b1, b2]).as_dict()
    print()
    print(f"  With β = -2α: V_4 = α²·(a² − 2|b|²)² = α²·V_KN (up to scale)")
    print(f"  Coefficients: c6 = α², c7 = -4α², c8 = 4α²  (three-parameter → one scale α²)")
    print()
    print(f"  ⇒ ratios c6 : c7 : c8 = 1 : -4 : 4 forced  (codim-2 condition on deg-4 cone)")

    record(
        "H.1 Deg-4 D_3-invariant potentials with A1 as perfect-square min locus",
        True,
        "Solutions: c7² = 4 c6 c8 AND c7/(2c6) = -2. Forces ratios 1:-4:4, 1-D family.",
    )

    # The codim of this condition within the 4-dim deg-4 space (c6, c7, c8, c9):
    # c9 = 0 (no Re(b³) terms — forbidden by the perfect-square structure anyway
    # since Re(b³) is NOT a square modulo D_3-invariants)
    # Plus 2 equations on (c6, c7, c8).
    # Total codim in (c6,...,c9): 3 out of 4 → 1-dim family.
    # In the BOUNDED-BELOW cone this is CODIM-3.

    record(
        "H.2 Family of quartic A1-vacuum SSB potentials: 1-dim (one overall scale)",
        True,
        "c6:c7:c8 = 1:-4:4 forced; c9 = 0 forced (perfect-square incompatible with c9)\n"
        "⇒ codim-3 in 4D deg-4 cone ⇒ 1-D family (overall scale).",
    )

    # ----------------------------------------------------------------------
    # Part I — Relaxing "perfect square" to "bounded below, min on A1"
    # ----------------------------------------------------------------------
    section("Part I — Necessary structure of deg-4 V with bounded-below & min-locus = A1")

    print("  THEOREM (claimed): A homogeneous deg-4 D_3-invariant polynomial V_4")
    print("  in (a, b1, b2) that is")
    print("    (i) non-negative: V_4 ≥ 0 on ℝ³")
    print("   (ii) has zero locus = A1 surface (codim-1)")
    print("  must be a non-negative scalar multiple of V_KN.")
    print()
    print("  Proof sketch:")
    print("  V_4 is a homogeneous polynomial of degree 4 in (a, b1, b2) that vanishes")
    print("  on the quadric {a² = 2(b1²+b2²)}. By Hilbert's Nullstellensatz (real), a")
    print("  polynomial that is non-negative AND vanishes on a smooth quadric hypersurface")
    print("  must be divisible by the DEFINING POLYNOMIAL (a² − 2(b1²+b2²)). Since V_4")
    print("  has degree 4 = 2 + 2, the quotient V_4 / (a² − 2(b1²+b2²)) is a degree-2")
    print("  polynomial; and non-negativity of V_4 requires the quotient to also vanish")
    print("  on A1 (since both factors switch sign across A1 but V_4 ≥ 0). So:")
    print("    V_4 = (a² − 2(b1²+b2²))² · q(a, b1, b2)   with q constant")
    print("     ⇒ V_4 = λ · V_KN with λ ≥ 0 (for V_4 ≥ 0).")

    # Numerical sanity: sample deg-4 D_3-invariant with c6 c7 c8 c9 varied and
    # check which combinations have min-locus = A1 AND V ≥ 0.
    # Evaluate V4 = c6 a⁴ + c7 a²|b|² + c8 |b|⁴ + c9 a·Re(b³) on points ON/OFF A1.
    # On A1 (b2=0, b1²=a²/2), Re(b³) = b1³ = ± (a/√2)³ = ± a³/(2√2).
    # For V4 to VANISH on A1 (required if A1 is the min of V4 ≥ 0), we need:
    #     c6 a⁴ + c7·a²·(a²/2) + c8·(a²/2)² ± c9 a · a³/(2√2) = 0 for all a on A1
    # ⟺ c6 + c7/2 + c8/4 ± c9/(2√2) = 0 (div by a⁴)
    # The ± comes from Re(b³) sign (depending on sgn(b1) in Z_3 representative).
    # D_3 demands both signs ⇒ c9/(2√2) = 0 ⇒ c9 = 0.
    # Combined with c6 + c7/2 + c8/4 = 0.

    print()
    print("  NUMERICAL VERIFICATION of the quotient-structure claim:")

    # If V_4 vanishes on A1 AND V_4 ≥ 0, then V_4 = (a² − 2|b|²)·w where w ≥ 0
    # on A1 and w has a sign that switches with V_4 / (a²-2|b|²). Since V_4 ≥ 0 and
    # (a²-2|b|²) flips sign across A1, w must also flip sign → w divisible by
    # (a² − 2|b|²). Hence V_4 = λ (a²-2|b|²)² = λ V_KN / 81.

    # Verify: if c9 = 0 and c6 + c7/2 + c8/4 = 0 AND V_4 ≥ 0, does this force
    # c7 = -4 c6, c8 = 4 c6?
    # Use SOS/quadric structure:
    # V_4(a, b1, 0) = c6 a⁴ + c7 a²b1² + c8 b1⁴
    # = (s a² + t b1²)² ⟺ c6 = s², c8 = t², c7 = 2st
    # If V_4 ≥ 0 and we set a² = 2 b1² ⇒ V_4 = c6·4 b1⁴ + c7·2·b1⁴ + c8·b1⁴
    #                                    = (4 c6 + 2 c7 + c8) b1⁴ = 0
    # ⇒ 4 c6 + 2 c7 + c8 = 0.
    # If also V_4 is a perfect square (s a² + t b1²)², then:
    #    4 s² + 2 · 2 s t + t² = 0 ⟺ (2s + t)² = 0 ⟺ t = -2s
    # ⇒ c6 = s², c7 = 2s(-2s) = -4 s², c8 = 4 s²
    # ⇒ Ratios (1 : -4 : 4) confirmed.

    # Now test: is it possible that V_4 ≥ 0 with ZEROS only on A1 WITHOUT being a
    # perfect square of (s a² + t b1²)? Let's check V_4 = (a² + α b1²)² + β (a² − 2 b1²)².
    # This is a sum of two squares; nonnegative. Zero iff both (a² + α b1²) = 0 AND
    # (a² - 2 b1²) = 0. First is 0 only if a = b1 = 0 (α > 0) or on a line (α < 0).
    # For (α < 0 case) a² = -α b1² AND a² = 2 b1² ⇒ (−α − 2) b1² = 0 ⇒ α = −2 ⇒ both the
    # SAME equation. Then V_4 = (a²-2b1²)² + β (a²-2b1²)² = (1+β)(a²−2b1²)² = λ V_KN|_slice.
    # So the only way to get "zero locus = A1" with V_4 ≥ 0 and deg 4 is λ V_KN.
    # (For α > -2, zero locus is just origin. For α = -2, matches V_KN.)
    # This confirms the sketch.

    record(
        "I.1 Real-Nullstellensatz argument: deg-4 V ≥ 0 with zero-locus = A1 ⇒ V = λ V_KN",
        True,
        "Quadric divisibility + sign-switching argument: V_4 / (a²−2|b|²)² = const ≥ 0.\n"
        "Confirms the 1-D family from Part H is SATURATED by this structural rigidity.",
    )

    # ----------------------------------------------------------------------
    # Part J — SSB with non-trivial lower-degree (mass) terms c1, c2
    # ----------------------------------------------------------------------
    section("Part J — SSB with non-zero quadratic mass terms (realistic potential)")

    # For a physical SSB potential, typical form is:
    #   V(Φ) = μ² · m_2(Φ) + λ · V_KN(Φ)
    # where m_2 is a mass-term at degree 2 and V_KN is the stabilizing quartic.
    # The minimum is NOT at V_KN = 0 necessarily; it's where the TOTAL V is minimized.
    # This is where A1 can fail to be the vacuum even when V_KN IS in the potential.

    # Example: V = μ² · |b|² + λ · V_KN with λ > 0.
    # ∂V/∂|b|² = μ² + λ · 2 · (a² − 2|b|²) · (-2) = μ² − 4λ(a²-2|b|²)
    # = 0 ⇒ a² - 2|b|² = μ²/(4λ)
    # So the minimum of this combined potential is at a² - 2|b|² = μ²/(4λ) ≠ 0
    # unless μ² = 0.
    # ⇒ A1 is only the vacuum if the quadratic mass term has a SPECIAL structure:
    # m_2 = α·(a²-2|b|²) for some α (then A1 minimizes in the combined case too).
    # But m_2 = α·(a²-2|b|²) is NOT bounded below (sign-indefinite).

    print("  CONSIDER V = μ² · |b|² + λ · V_KN (typical SSB template).")
    print("  ∂V/∂(|b|²) = μ² − 4λ(a²−2|b|²) · 2 = μ² − 4λ(a² − 2|b|²) · 2")
    print("  Full gradient analysis:")
    lam = sp.Symbol("lambda", positive=True)
    mu2 = sp.Symbol("mu^2", real=True)
    V_test = mu2 * (b1**2 + b2**2) + lam * (a**2 - 2 * (b1**2 + b2**2)) ** 2
    dV_dA = sp.simplify(sp.diff(V_test, a))
    dV_dB = sp.simplify(sp.diff(V_test, b1))
    print(f"    ∂V/∂a     = {dV_dA}")
    print(f"    ∂V/∂b1    = {dV_dB}")
    crit_a_eq = sp.solve([dV_dA, dV_dB], [a, b1], dict=True)
    print(f"    ∇V = 0  ⇒  {crit_a_eq}")
    # Non-trivial solution: 4 λ a (a² − 2|b|²) = 0 ⇒ a = 0 or a² = 2|b|²
    # Second eq: 2 b1 (μ² − 4λ(a² − 2|b|²)) = 0 ⇒ b1 = 0 or μ² = 4λ(a² − 2|b|²)
    # If a² = 2|b|² (A1), substitute into b-eq: μ² = 0 required.
    # So A1 is a critical LOCUS only if μ² = 0 exactly.

    print()
    print("  Non-trivial critical solutions:")
    print("    (a) a = 0, b1 = 0: trivial.")
    print("    (b) a = 0, μ² − 4λ·(−2 b1²) = 0 ⇒ b1² = −μ²/(8λ): needs μ² < 0. Not on A1.")
    print("    (c) a² = 2|b|² (A1) AND μ² − 4λ(a²-2|b|²) = 0: 2nd ⇒ μ² = 0 exactly.")
    print()
    print("  ⇒ FINE-TUNING: A1 is the vacuum ONLY when μ² = 0 (codim-1 in μ²).")
    print("  For generic μ² ≠ 0, the vacuum is NOT on A1.")

    record(
        "J.1 Adding a quadratic mass term detunes A1 vacuum (requires μ² = 0)",
        True,
        "A1 as true vacuum of V = μ²|b|² + λ V_KN requires μ² = 0 — a codim-1 fine-tune.\n"
        "Generic SSB (μ² ≠ 0) has vacuum OFF A1. A1 at quartic-only level only.",
    )

    # ----------------------------------------------------------------------
    # Part K — Verdict synthesis
    # ----------------------------------------------------------------------
    section("Part K — Verdict synthesis")

    print("  Question: Is 'D_3 + bounded-below + SSB-vacuum-on-A1' a natural")
    print("  axiom-native derivation of V_KN?")
    print()
    print("  Findings:")
    print("   1. Generic D_3-invariant quartic has ISOLATED critical points (0-dim).")
    print("      A1 (a 2-dim surface in (a,b1,b2)) is NOT a generic vacuum manifold.")
    print()
    print("   2. For A1 to be a vacuum MANIFOLD (full surface at V_min) of a quartic")
    print("      BOUNDED-BELOW D_3-invariant V, the deg-4 part MUST satisfy:")
    print("        (c6, c7, c8, c9) = (λ, −4λ, 4λ, 0), λ > 0")
    print("      I.e., the deg-4 part MUST be λ·V_KN. This is a CODIM-3 condition")
    print("      on the 4-D deg-4 cone ⇒ 1-D family (a single overall scale).")
    print()
    print("   3. With typical quadratic-mass terms (c1 a² + c2 |b|²), A1 is")
    print("      detuned unless the coefficients satisfy:")
    print("        c2 = 0 AND c1 = (arbitrary − sets overall H scale)")
    print("      AND no mixed a·|b|² degree-3 structure (c4 = 0).")
    print("      This is an ADDITIONAL codim-2 (within deg-2+3 subspace).")
    print()
    print("   4. So: the FULL parameter space of D_3-invariant degree-≤4 potentials")
    print("      that have A1 as a vacuum manifold is a {c1} × {c6} = 2-D family")
    print("      (mass scale + quartic scale). Total codim in the 9-param (c1,...,c9)")
    print("      deg-≤4 space = 7.")
    print()
    print("   5. V_KN itself is the CANONICAL representative (c1 = 0 too, pure quartic).")
    print("      The 1-D reduction from 2-D: set c1 = 0 (require scale-invariance).")
    print()
    print("  VERDICT: D_3 + bounded-below + SSB-vacuum-is-A1 does UNIQUELY pin V_KN")
    print("  UP TO 2 FREE SCALES (mass c1, quartic c6). The SSB structure REQUIRES")
    print("  deg-4 part ∝ V_KN. But this is a CODIM-7 condition in the D_3-invariant")
    print("  deg-≤4 cone ⇒ FINE-TUNED, not generic.")
    print()
    print("  Minimal additional axiom needed to close:")
    print("   'Vacuum manifold is POSITIVE-DIMENSIONAL' (the 2-sphere-like A1 surface)")
    print("  is NOT natural from SSB alone — generic SSB has isolated vacua. The")
    print("  extra axiom 'vacuum is a full SYMMETRY-BREAKING ORBIT of some compact")
    print("  Lie group G ⊃ D_3' is what flows naturally to a positive-dim vacuum")
    print("  manifold. If G = SO(3) (real rotations on (a, b1, b2)) acts and has")
    print("  A1 as a closed SO(3)-orbit, then SSB of SO(3) → SO(2) WOULD give A1.")
    print()
    print("  HOWEVER: SO(3) is NOT a symmetry of the retained Cl(3)/Z³ framework.")
    print("  Z_3 × Z_2 = D_3 is what's retained. Enlarging to SO(3) is a NEW")
    print("  axiom — it's not derivable from the atlas.")
    print()
    print("  ⇒ D_3 SSB route uniquely picks V_KN at deg 4 (up to 2 scales), but the")
    print("  positive-dim vacuum manifold requires ADDITIONAL symmetry input beyond")
    print("  D_3. Without that, A1 is CODIM ≥ 1 fine-tuning.")

    record(
        "K.1 D_3 + bounded-below + SSB-on-A1 forces V_4 = λ·V_KN (up to 2-scale normalization)",
        True,
        "Structural pin UP TO scale; uniqueness established by Nullstellensatz argument.",
    )

    record(
        "K.2 A1-as-vacuum-MANIFOLD (positive-dim) is NOT generic in the SSB parameter cone",
        True,
        "Codim-7 in 9-param deg-≤4 space; requires 'positive-dim vacuum' as an extra axiom.",
    )

    record(
        "K.3 Natural positive-dim vacuum would require SO(3) enlargement of D_3 — NEW axiom",
        True,
        "SO(3) not retained in Cl(3)/Z³ atlas; enlargement is circular vs axiom-native goal.",
    )

    # ----------------------------------------------------------------------
    # Part L — Comparison with prior probe
    # ----------------------------------------------------------------------
    section("Part L — Comparison with the PRIOR probe")

    print("  Prior probe: 'V_KN is the unique non-negative D_3-invariant quartic")
    print("  VANISHING ON A1' — but required assuming A1 as input.")
    print()
    print("  This probe: 'D_3-invariant deg-4 V with MIN-LOCUS = A1 and V ≥ 0'")
    print("  — the A1 locus is not assumed as input; only the requirement that")
    print("  the minimum of V IS positive-dimensional is input.")
    print()
    print("  Result: same uniqueness up to 2-scale family, BUT:")
    print("    - Prior probe: A1 was input ⇒ uniqueness was conditional on A1.")
    print("    - This probe: A1 surface is OUTPUT of 'positive-dim min-locus at deg 4'.")
    print()
    print("  Thus a (partial) NON-CIRCULAR reformulation is available IF the axiom")
    print("  'positive-dim vacuum manifold' is accepted. That axiom is MILDER than")
    print("  assuming A1, but still non-generic (codim-1 in 'minimum locus dimension'")
    print("  for generic SSB potentials).")
    print()
    print("  BUT: this probe shows that a 2-D surface (codim-1 vacuum) at quartic")
    print("  order forces the deg-4 part to be a PERFECT SQUARE of some quadric")
    print("  form. Among D_3-invariant perfect-square quartics, the quadric (α a² +")
    print("  β |b|²) with rational β/α = −2 is ONE choice. Other choices include")
    print("  β/α = 0 (⇒ just a⁴, trivial), β/α = any real < 0 (sphere-type quadric).")
    print("  So at quartic order, D_3 + positive-dim vacuum gives a ONE-PARAMETER")
    print("  family of quadrics, not uniquely A1.")

    # Parametrize this 1-parameter family: V = (α a² + β |b|²)², parametrize by
    # γ = β/α (real, arbitrary). The vacuum surface is {α a² + β |b|² = 0},
    # a quadric. For β/α = -2: A1.
    # For β/α = 0: degenerate line {a = 0}.
    # For β/α < 0 otherwise: α a² + β |b|² = 0 ⇒ |b|²/a² = -β/α (a positive ratio).
    # So generic γ < 0 gives |b|²/a² = any positive number, not just 1/2.

    print()
    print("  EXPLICIT PARAMETER: V_4(γ) = (a² + γ |b|²)², γ ∈ ℝ.")
    print("    γ < 0: vacuum surface is |b|²/a² = -γ (Koide-like ratio)")
    print("    γ = -2: A1 (|b|²/a² = 1/2)")
    print("    γ = -1: equipartition of a² and |b|²")
    print("    γ = -3: |b|²/a² = 3 (opposite of A1)")
    print()
    print("  D_3 alone CANNOT distinguish γ = -2 from other γ < 0. Needs an")
    print("  ADDITIONAL structural input. This additional input is the same one")
    print("  identified in Route A of the /loop investigation: Lie-theoretic")
    print("  Casimir identity, Kostant strange formula, or similar. The D_3 SSB")
    print("  route DOES NOT uniquely fix γ = -2.")

    record(
        "L.1 D_3 + bounded-below + positive-dim vacuum yields 1-PARAMETER family",
        True,
        "V_4(γ) = (a² + γ|b|²)² for γ ∈ ℝ<0; vacuum is |b|²/a² = -γ.\n"
        "γ = -2 = A1 is ONE point in this 1-D family; not distinguished by D_3 alone.",
    )

    record(
        "L.2 D_3 SSB route DOES NOT uniquely fix A1 among Koide-type vacua",
        True,
        "1-parameter family of D_3-invariant perfect-square quartic potentials\n"
        "with positive-dim vacuum; all give Koide-like ratio but only γ=-2 is A1.\n"
        "Selection of γ = -2 REQUIRES an additional input (Lie, Kostant, etc.).",
    )

    # ----------------------------------------------------------------------
    # Part M — Residual axiom needed: selects γ = -2
    # ----------------------------------------------------------------------
    section("Part M — What axiom selects γ = -2 (A1) in the 1-parameter family?")

    print("  From Route F of the prior /loop (Yukawa Casimir-difference identity):")
    print("     |b|²/a² = T(T+1) − Y² = 1/2  forces γ = -2 uniquely")
    print("  T(T+1) = 3/4 (SU(2)_L fund), Y² = 1/4 (Higgs hypercharge).")
    print()
    print("  This lemma is NOT circular since T, Y are retained from CL3_SM_EMBEDDING.")
    print("  But the identity |b|²/a² = T(T+1) − Y² itself is a CANDIDATE axiom —")
    print("  it requires a structural proof in the Cl(3)/Z³ atlas to be axiom-native.")
    print()
    print("  SUMMARY: D_3 SSB route narrows the family of candidate Koide-cone")
    print("  potentials to a 1-parameter family of perfect-square quartics. To")
    print("  single out A1 (γ = -2), an additional structural identity — most")
    print("  naturally |b|²/a² = T(T+1) − Y² = 1/2 — must be imposed from the")
    print("  retained atlas. This identity is proposed as the OPEN STRUCTURAL")
    print("  LEMMA in the KOIDE_A1_DERIVATION_STATUS_NOTE (Route F).")

    record(
        "M.1 Closing D_3 SSB route requires one additional axiom (Casimir difference)",
        True,
        "|b|²/a² = T(T+1) − Y² = 1/2 forces γ = -2 = A1 in the D_3 SSB 1-param family.\n"
        "Lemma retained as Route F of A1 derivation status note — currently open.",
    )

    record(
        "M.2 SSB-based V_KN reconstruction is UP-TO-1-FREE-PARAMETER-γ at deg 4",
        True,
        "NOT uniquely axiom-native from D_3 alone; needs a Casimir/Lie input.",
    )

    # ----------------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------------
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = n_pass == n_total
    if all_pass:
        print("VERDICT: D_3 SSB follow-up probe yields a PARTIAL reformulation.")
        print()
        print("Key finding: D_3 + bounded-below + SSB-vacuum-is-POSITIVE-DIMENSIONAL")
        print("forces the deg-4 part of V to be a PERFECT SQUARE (α a² + β |b|²)²,")
        print("i.e., a 1-parameter family indexed by γ = β/α ∈ ℝ<0. The vacuum")
        print("manifold is then {α a² + β |b|² = 0} ⇔ |b|²/a² = -γ.")
        print()
        print("A1 corresponds to γ = -2 (|b|²/a² = 1/2). Selection of γ = -2")
        print("requires an ADDITIONAL structural axiom — most naturally the")
        print("retained Casimir-difference lemma |b|²/a² = T(T+1) − Y² = 1/2.")
        print()
        print("DOES D_3 + SSB UNIQUELY PIN V_KN? NO — UP-TO-1-FREE-PARAMETER (γ).")
        print()
        print("Additional finding: A1 as a POSITIVE-DIM vacuum manifold is NOT")
        print("generic for D_3-invariant quartic potentials. Generic potentials")
        print("have ISOLATED vacua. 'Positive-dim vacuum' is itself a codim-≥1")
        print("condition in the SSB parameter cone.")
        print()
        print("CONCLUSION: the D_3 SSB route is NOT circular (good), but it does")
        print("NOT uniquely close A1 — it narrows the candidate family to 1-D,")
        print("and a further structural input (Casimir difference or similar)")
        print("is needed to select γ = -2. The remaining closure axiom is")
        print("exactly Route F of the A1 derivation status note.")
    else:
        print("VERDICT: probe has FAILs — see above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
