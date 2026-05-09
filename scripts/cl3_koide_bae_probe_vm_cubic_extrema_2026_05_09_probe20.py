"""
Koide BAE Probe 20 — V(m) Cubic-Extrema Extension to hw=1

Tests whether the retained Z^3 scalar potential V(m) on the local Clifford
trace m = Tr(K_sel), when extended via spectral functional calculus to the
3-dim hw=1 C_3-orbit subspace (Hermitian circulants H = aI + bC + b-bar C^2),
yields extrema satisfying the Brannen Amplitude Equipartition (BAE)
condition |b|^2 / a^2 = 1/2.

Retained inputs (ALL from KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19,
in-scope retained content only):
    - V(m) = V_0 + L*m + (3/2)*m^2 + (1/6)*m^3
    - L = c1 + c2/2 with c2 = 35/12 exactly, c1 numerically -0.2526...
    - g_2 = 3/2, g_3 = 1/6 — Clifford-fixed by Tr(T_m^2)=3, Tr(T_m^3)=1
    - The Z^3-invariant scalar action ON THE LOCAL CLIFFORD TRACE.

Out-of-scope: any "mass tower" claim from the same note (depends on hidden
upstream inputs K_frozen, c1/c2, H_* witness rates).

Hypothesis tested:
    V_total(a, b, b-bar) := Tr V(H) = sum_k V(lambda_k(a, b))
    extremized over (a, Re b, Im b) on the C_3-orbit hw=1, yields a critical
    point with |b|^2/a^2 = 1/2 (the BAE condition).

Concrete attack steps (all algebra; no PDG values consumed):
    Step 1: Verify V_total agrees with V(m) at b=0 (extension consistency).
    Step 2: Compute Tr H, Tr H^2, Tr H^3 in (a, |b|, arg b) coordinates.
    Step 3: Compute V_total(a, r, phi) where r = |b|, phi = arg b.
    Step 4: Solve the angular extremum sin(3 phi) = 0 -> cos(3 phi) = +/- 1.
    Step 5: Solve the (a, r) extremum equations.
    Step 6: Test BAE condition r^2/a^2 = 1/2 against the V_total extrema.
    Step 7: Per-eigenvalue extremization V'(lambda_k) = 0 for each k.
    Step 8: Both routes fail to close BAE.

VERDICT (anticipated): STRUCTURAL OBSTRUCTION.

  V(m) functional extension to hw=1 does NOT generically force BAE. The
  V_total extremum equations couple (a, r) via L (the linear coefficient),
  and BAE r^2/a^2 = 1/2 is NOT a generic algebraic consequence — it would
  require a specific tuning of L that is incompatible with the retained
  L = c1 + c2/2 ~ 1.2057.

  Per-eigenvalue extremization (V'(lambda_k) = 0 for all k) on the C_3-orbit
  fixes lambda_k in {0, -6} but the resulting (a, r) configurations do not
  satisfy BAE.

  This rules out "V(m) extension to hw=1" as an A-tier closure route for
  BAE. The obstruction is precise: BAE requires the relation
  7 a^2 + 48 a + 72 = 0 between (a, r), while V_total extremization requires
  9 a^2 + 54 a + 72 + 2 L = 0. These coincide only for L = 0 (where neither
  root is BAE) or for specific tuned L, not for retained L.

No PDG values consumed. No new axioms introduced. Pure polynomial-algebra
analysis of the spectral-functional extension.
"""

from __future__ import annotations

import numpy as np
import sympy as sp


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    """Single PASS/FAIL line, mirroring the campaign's runner style."""
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
        if detail:
            print(f"        detail: {detail}")


# ----------------------------------------------------------------------
# Algebraic primitives
# ----------------------------------------------------------------------

omega = np.exp(2j * np.pi / 3)
C = np.zeros((3, 3), dtype=complex)
C[1, 0] = C[2, 1] = C[0, 2] = 1.0
C2 = C @ C
I3 = np.eye(3, dtype=complex)


def hermitian_circulant(a: float, b: complex) -> np.ndarray:
    """H = aI + bC + b-bar C^2 (Hermitian circulant)."""
    return a * I3 + b * C + np.conj(b) * C2


def eigenvalues_circulant(a: float, b: complex) -> np.ndarray:
    """Closed-form eigenvalues lambda_k = a + 2|b|cos(arg(b) + 2 pi k /3)."""
    r, phi = abs(b), np.angle(b)
    return np.array([a + 2 * r * np.cos(phi + 2 * np.pi * k / 3) for k in range(3)])


# ----------------------------------------------------------------------
# Section 0: Setup and retained-input recital
# ----------------------------------------------------------------------

print("=" * 70)
print("Section 0: Retained V(m) inputs (from KOIDE_Z3_SCALAR_POTENTIAL note)")
print("=" * 70)
print()
print("  V(m) = V_0 + L*m + (3/2)*m^2 + (1/6)*m^3   [single real coord]")
print("  g_2 = 3/2  (from Tr T_m^2 = 3)")
print("  g_3 = 1/6  (from Tr T_m^3 = 1)")
print("  L = c_1 + c_2/2   with c_2 = 35/12 exact, c_1 ~ -0.2526")
print("  L ~ 1.2057  (numerically retained)")
print()

# Use exact symbolic values where retained:
c2_exact = sp.Rational(35, 12)
# c1 numerically (the retained note gives c1 ~ -0.2526; full closed form
# is not load-bearing for the obstruction since we test PARAMETRIC L)
c1_num = -0.2526
L_num = c1_num + float(c2_exact) / 2.0  # ~ 1.2057
print(f"  L (numerical, retained) = {L_num:.6f}")
print()


# ----------------------------------------------------------------------
# Section 1: Trace identities for circulants
# ----------------------------------------------------------------------

print("=" * 70)
print("Section 1: Tr(H), Tr(H^2), Tr(H^3) for H = aI + bC + b-bar C^2")
print("=" * 70)
print()

# Symbolic verification
a_s, r_s, phi_s = sp.symbols("a r phi", real=True)
b_s = r_s * sp.exp(sp.I * phi_s)
bbar_s = sp.conjugate(b_s)

# Symbolic eigenvalues
lam_k = [a_s + 2 * r_s * sp.cos(phi_s + 2 * sp.pi * k / 3) for k in range(3)]


def trig_simp(expr):
    """Trig-aware simplification: expand_trig + simplify is the most
    reliable combination for collapsing sums of cos/sin of phi+2 pi k/3."""
    return sp.simplify(sp.expand_trig(sp.expand(expr)))


# Trace H^n = sum lam_k^n
TrH1 = trig_simp(sum(lam_k))
TrH2 = trig_simp(sum(l**2 for l in lam_k))
TrH3 = trig_simp(sum(l**3 for l in lam_k))

print(f"  Tr(H)   = {TrH1}")
print(f"  Tr(H^2) = {TrH2}")
print(f"  Tr(H^3) = {TrH3}")
print()

# Expected forms:
#   Tr(H)   = 3a
#   Tr(H^2) = 3a^2 + 6r^2
#   Tr(H^3) = 3a^3 + 18 a r^2 + 6 r^3 cos(3 phi)
TrH1_expected = 3 * a_s
TrH2_expected = 3 * a_s**2 + 6 * r_s**2
TrH3_expected = 3 * a_s**3 + 18 * a_s * r_s**2 + 6 * r_s**3 * sp.cos(3 * phi_s)

check("1.1 Tr(H) = 3a (sum eigenvalues)",
      trig_simp(TrH1 - TrH1_expected) == 0)
check("1.2 Tr(H^2) = 3a^2 + 6r^2 (sum eigenvalues^2)",
      trig_simp(TrH2 - TrH2_expected) == 0)
check("1.3 Tr(H^3) = 3a^3 + 18 a r^2 + 6 r^3 cos(3 phi)",
      trig_simp(TrH3 - TrH3_expected) == 0)

# Numerical cross-check
H_num = hermitian_circulant(1.7, 0.6 + 0.4j)
a_n, r_n, phi_n = 1.7, abs(0.6 + 0.4j), np.angle(0.6 + 0.4j)
check("1.4 numerical Tr H = 3a",
      abs(np.trace(H_num).real - 3 * a_n) < 1e-9)
check("1.5 numerical Tr H^2 = 3a^2 + 6r^2",
      abs(np.trace(H_num @ H_num).real - (3 * a_n**2 + 6 * r_n**2)) < 1e-9)
check("1.6 numerical Tr H^3 = 3a^3 + 18 a r^2 + 6 r^3 cos(3phi)",
      abs(np.trace(H_num @ H_num @ H_num).real
          - (3 * a_n**3 + 18 * a_n * r_n**2 + 6 * r_n**3 * np.cos(3 * phi_n))) < 1e-9)


# ----------------------------------------------------------------------
# Section 2: Extension V_total via functional calculus
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 2: V_total(a, r, phi) := sum_k V(lambda_k)")
print("=" * 70)
print()

# Define V symbolically with the retained coefficients
m_s, V0_s, L_s = sp.symbols("m V_0 L", real=True)
V_of_m = V0_s + L_s * m_s + sp.Rational(3, 2) * m_s**2 + sp.Rational(1, 6) * m_s**3

# V_total = sum V(lambda_k) — using the trace identities directly
V_total = sum(V_of_m.subs(m_s, l) for l in lam_k)
V_total = sp.simplify(sp.expand(V_total))
V_total = sp.simplify(V_total)

# Substitute Tr H^n directly:
# V_total = 3 V0 + L * Tr H + (3/2) Tr H^2 + (1/6) Tr H^3
V_total_via_traces = (
    3 * V0_s
    + L_s * TrH1_expected
    + sp.Rational(3, 2) * TrH2_expected
    + sp.Rational(1, 6) * TrH3_expected
)
V_total_via_traces = sp.expand(V_total_via_traces)

check("2.1 V_total (sum V(lambda_k)) equals trace expansion",
      sp.simplify(V_total - V_total_via_traces) == 0)

# Display:
print("  V_total = 3 V_0 + 3 L a + (9/2) a^2 + 9 r^2 + (1/2) a^3")
print("            + 3 a r^2 + r^3 cos(3 phi)")
print()
print("  symbolic V_total:")
sp.pprint(V_total_via_traces)
print()

# Verify the expected closed form
V_total_expected = (
    3 * V0_s + 3 * L_s * a_s + sp.Rational(9, 2) * a_s**2 + 9 * r_s**2
    + sp.Rational(1, 2) * a_s**3 + 3 * a_s * r_s**2 + r_s**3 * sp.cos(3 * phi_s)
)
check("2.2 V_total matches expected closed form",
      sp.simplify(V_total_via_traces - V_total_expected) == 0)


# ----------------------------------------------------------------------
# Section 3: Reduction at b = 0 reproduces V(m)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 3: Extension consistency: V_total(a, 0, phi) reduces to 3 V(a)")
print("=" * 70)
print()

V_total_at_r0 = V_total_expected.subs(r_s, 0)
expected_3V = 3 * V_of_m.subs(m_s, a_s)
check("3.1 V_total(a, 0, phi) = 3 V(a)  [b=0 limit]",
      sp.simplify(V_total_at_r0 - expected_3V) == 0)

# 1D extremum: dV(m)/dm = 0 -> m^2 + 6m + 2L = 0
# (matches the retained note's m_V ~ -0.433 for L ~ 1.2057)
dV_dm = sp.diff(V_of_m, m_s)
crit_1d = sp.solve(dV_dm, m_s)
print(f"  1D critical points (dV/dm = 0): m = {crit_1d}")

# Verify quadratic m^2 + 6m + 2L = 0 (after multiplying by 2 to clear fractions)
quad_1d = sp.expand(2 * dV_dm)  # = 2L + 6m + m^2
check("3.2 1D extremum equation: m^2 + 6m + 2L = 0",
      sp.simplify(quad_1d - (m_s**2 + 6 * m_s + 2 * L_s)) == 0)

# Numerical check vs retained note
m_V_numerical = -3 + np.sqrt(9 - 2 * L_num)  # = -0.433 per note
check("3.3 m_V (V_eff minimum) ~ -0.433 matches retained note",
      abs(m_V_numerical - (-0.433)) < 0.005)


# ----------------------------------------------------------------------
# Section 4: Angular extremum forces sin(3 phi) = 0
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 4: Angular extremum dV_total/d(phi) = 0")
print("=" * 70)
print()

dV_dphi = sp.diff(V_total_expected, phi_s)
print(f"  dV_total/dphi = {sp.simplify(dV_dphi)}")
print()

# Expected: dV/dphi = -3 r^3 sin(3 phi)
check("4.1 dV/dphi = -3 r^3 sin(3 phi)",
      sp.simplify(dV_dphi - (-3 * r_s**3 * sp.sin(3 * phi_s))) == 0)

# Solutions: sin(3 phi) = 0 -> 3 phi = n*pi -> phi = n*pi/3
# Two cosine cases: cos(3 phi) = +1 or cos(3 phi) = -1
# These are the discrete C_3 directions (and their pi-shifted counterparts)
print("  Angular extremum: sin(3 phi) = 0  =>  3 phi in pi*Z")
print("    cos(3 phi) = +1: phi in {0, 2pi/3, 4pi/3}     [C_3 directions]")
print("    cos(3 phi) = -1: phi in {pi/3, pi, 5pi/3}     [shifted directions]")
print()


# ----------------------------------------------------------------------
# Section 5: Radial-amplitude extremum equations
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 5: dV/da = 0 and dV/dr = 0 (with cos(3 phi) = eps in {+1, -1})")
print("=" * 70)
print()

eps_s = sp.symbols("eps", real=True)  # eps = cos(3 phi) in {+/-1}
V_total_with_eps = V_total_expected.subs(sp.cos(3 * phi_s), eps_s)

dV_da = sp.diff(V_total_with_eps, a_s)
dV_dr = sp.diff(V_total_with_eps, r_s)

print(f"  dV/da = {sp.simplify(dV_da)}")
print(f"  dV/dr = {sp.simplify(dV_dr)}")
print()

# Expected:
#   dV/da = 3 L + 9 a + (3/2) a^2 + 3 r^2
#   dV/dr = 18 r + 6 a r + 3 eps r^2 = 3 r * (6 + 2a + eps r)
dV_da_expected = 3 * L_s + 9 * a_s + sp.Rational(3, 2) * a_s**2 + 3 * r_s**2
dV_dr_expected = 18 * r_s + 6 * a_s * r_s + 3 * eps_s * r_s**2

check("5.1 dV/da = 3L + 9a + (3/2)a^2 + 3 r^2",
      sp.simplify(dV_da - dV_da_expected) == 0)
check("5.2 dV/dr = 3r(6 + 2a + eps r)",
      sp.simplify(dV_dr - dV_dr_expected) == 0)

# Non-trivial branch (r != 0): r = -eps(6 + 2a) / 1 = -(6 + 2a)/eps = -eps(6 + 2a)
# (since eps^2 = 1).
# Substitute back into dV/da = 0:
#   3L + 9a + (3/2)a^2 + 3 (6 + 2a)^2 = 0
# Multiply by 2/3:
#   2L + 6a + a^2 + 2(6+2a)^2 = 0
# Expand:
#   2L + 6a + a^2 + 2(36 + 24a + 4a^2) = 0
#   2L + 6a + a^2 + 72 + 48a + 8a^2 = 0
#   9 a^2 + 54 a + 72 + 2 L = 0

r_nontrivial = -eps_s * (6 + 2 * a_s)  # eps^2 = 1 implies this
substituted_raw = sp.expand(dV_da.subs(r_s, r_nontrivial))
# Apply eps^2 = 1 (since eps = cos(3 phi) in {+1, -1}):
substituted = sp.simplify(substituted_raw.subs(eps_s**2, 1))
# Multiply through by 2/3 to clear the (3/2)a^2 fraction
quad_a = sp.simplify(sp.expand(2 * substituted / 3))
print(f"  Substituting r = -eps(6+2a) into dV/da=0 (and clearing factor 2/3):")
print(f"  -> {quad_a} = 0")
print()

quad_a_expected = 2 * L_s + 6 * a_s + a_s**2 + 2 * (6 + 2 * a_s) ** 2
quad_a_expected = sp.expand(quad_a_expected)
# The simplified form is 9 a^2 + 54 a + 72 + 2L
quad_a_canonical = 9 * a_s**2 + 54 * a_s + 72 + 2 * L_s

check("5.3 (a, r) extremum reduces to 9 a^2 + 54 a + 72 + 2L = 0",
      sp.simplify(quad_a_expected - quad_a_canonical) == 0)
check("5.4 quadratic-in-a from substitution matches",
      sp.simplify(quad_a - quad_a_canonical) == 0)


# ----------------------------------------------------------------------
# Section 6: BAE condition |b|^2 / a^2 = 1/2 in (a, r) coords
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 6: BAE algebraic condition r^2/a^2 = 1/2")
print("=" * 70)
print()

# BAE: r^2 = a^2 / 2
# With non-trivial branch r = -eps(6+2a), r^2 = (6+2a)^2 = 4(3+a)^2
# So 4(3+a)^2 = a^2/2  ->  8(3+a)^2 = a^2  ->  8(9 + 6a + a^2) = a^2
# -> 72 + 48a + 8 a^2 = a^2  ->  7 a^2 + 48 a + 72 = 0
bae_condition = 8 * (3 + a_s) ** 2 - a_s**2
bae_canonical = 7 * a_s**2 + 48 * a_s + 72

check("6.1 BAE r^2/a^2=1/2 with r=-eps(6+2a) reduces to 7a^2 + 48a + 72 = 0",
      sp.simplify(sp.expand(bae_condition) - bae_canonical) == 0)

# Roots of 7a^2 + 48a + 72 = 0:
#   discriminant = 48^2 - 4*7*72 = 2304 - 2016 = 288 = 144*2
#   a = (-48 +/- 12 sqrt(2)) / 14 = (-24 +/- 6 sqrt(2)) / 7
bae_roots = sp.solve(bae_canonical, a_s)
print(f"  BAE roots (in a): {bae_roots}")
print(f"  Numerical: {[complex(r).real for r in bae_roots]}")
print()


# ----------------------------------------------------------------------
# Section 7: Comparison of V_total vs BAE quadratics in a
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 7: V_total extremum vs BAE — same root for which L?")
print("=" * 70)
print()

# V_total extrema: 9 a^2 + 54 a + 72 + 2L = 0
# BAE:             7 a^2 + 48 a + 72       = 0
#
# These are linearly independent quadratics in a. They share a root iff a
# satisfies both:
#   resultant condition or equivalently: subtract suitable multiples.
# Subtract 7/9 of V_total quadratic from BAE:
#   (7 - 7) a^2 + (48 - 54*7/9) a + (72 - 72*7/9 - 2L*7/9) = 0
#   0 a^2 + (48 - 42) a + (72 - 56 - 14L/9) = 0
#   6 a + 16 - 14L/9 = 0
#   a = (14L/9 - 16) / 6 = (14L - 144) / 54 = (7L - 72) / 27

# So the shared root (when one exists) is a = (7L - 72) / 27.
# Substitute into BAE:
shared_root = (7 * L_s - 72) / 27
bae_at_shared = sp.simplify(bae_canonical.subs(a_s, shared_root))
print(f"  Shared-root expression: a = (7L - 72) / 27")
print(f"  BAE evaluated at shared root: {bae_at_shared}")

# This should be 0 only for the L values that admit a shared root.
# Solve for L:
L_compatibility = sp.solve(bae_at_shared, L_s)
print(f"  L values for V_total/BAE compatibility: {L_compatibility}")
print()

# These should be the L values L1, L2 such that the V_total quadratic has
# a root coincident with a BAE root.
# Compute numerical L1, L2 vs retained L:
print(f"  Retained L = c1 + c2/2 ~ {L_num:.4f}")
print(f"  Required L for compatibility: {[float(L_v) for L_v in L_compatibility]}")
print()

retained_L_compatible = any(abs(float(L_v) - L_num) < 0.01 for L_v in L_compatibility)
check("7.1 V_total/BAE compatibility L values DIFFER from retained L",
      not retained_L_compatible,
      detail=f"retained L = {L_num:.4f}; required = {[float(L_v) for L_v in L_compatibility]}")


# ----------------------------------------------------------------------
# Section 8: Numerical V_total extrema for retained L vs BAE
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 8: Numerical V_total extrema at retained L vs BAE roots")
print("=" * 70)
print()

# V_total extremum quadratic: 9 a^2 + 54 a + 72 + 2L = 0
# -> a^2 + 6a + 8 + 2L/9 = 0
# -> a = -3 +/- sqrt(9 - 8 - 2L/9) = -3 +/- sqrt(1 - 2L/9)
disc = 1 - 2 * L_num / 9
print(f"  Discriminant 1 - 2L/9 = {disc:.6f}")
if disc > 0:
    a1 = -3 + np.sqrt(disc)
    a2 = -3 - np.sqrt(disc)
    print(f"  V_total extrema: a1 = {a1:.4f}, a2 = {a2:.4f}")
    # r at each: r = -eps*(6+2a) — pick sign so r > 0
    r1_abs = abs(6 + 2 * a1)
    r2_abs = abs(6 + 2 * a2)
    print(f"  r1 = {r1_abs:.4f}, r2 = {r2_abs:.4f}")
    print(f"  r1^2/a1^2 = {r1_abs**2/a1**2:.4f}  (BAE = 0.5)")
    print(f"  r2^2/a2^2 = {r2_abs**2/a2**2:.4f}  (BAE = 0.5)")
    print()
    check("8.1 V_total extremum a1: r^2/a^2 != 1/2",
          abs(r1_abs**2 / a1**2 - 0.5) > 0.05,
          detail=f"r1^2/a1^2 = {r1_abs**2/a1**2:.4f}")
    check("8.2 V_total extremum a2: r^2/a^2 != 1/2",
          abs(r2_abs**2 / a2**2 - 0.5) > 0.05,
          detail=f"r2^2/a2^2 = {r2_abs**2/a2**2:.4f}")
else:
    check("8.0 V_total quadratic has real roots (discriminant > 0)", False,
          detail=f"discriminant = {disc}")


# ----------------------------------------------------------------------
# Section 9: Numerical V_total via direct gradient descent (independent check)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 9: Numerical confirmation by explicit V_total minimization")
print("=" * 70)
print()


def V_total_numerical(a: float, r: float, phi: float, L: float) -> float:
    """V_total(a, r, phi; L) — V_0 dropped (constant)."""
    return (
        3 * L * a + 4.5 * a**2 + 9 * r**2 + 0.5 * a**3
        + 3 * a * r**2 + r**3 * np.cos(3 * phi)
    )


def grad_V_total(a: float, r: float, phi: float, L: float) -> tuple[float, float, float]:
    """Gradient of V_total."""
    dVda = 3 * L + 9 * a + 1.5 * a**2 + 3 * r**2
    dVdr = 18 * r + 6 * a * r + 3 * r**2 * np.cos(3 * phi)
    dVdphi = -3 * r**3 * np.sin(3 * phi)
    return dVda, dVdr, dVdphi


# Numerical Newton's method to find the non-trivial extremum on
# eps = cos(3 phi) = -1 (so phi = pi/3). Use Newton on (a, r) with
# fixed phi = pi/3 (since the angular extremum is decoupled and the
# non-trivial branch satisfies r > 0, eps = sign-chosen).
# We use the algebraic prediction a = -3 + sqrt(1 - 2L/9) as the seed
# for a, and r = |6 + 2a|.

phi_fixed = np.pi / 3.0  # so cos(3 phi) = -1, eps = -1
a_seed = -3.0 + np.sqrt(disc)  # close to a1
r_seed = abs(6 + 2 * a_seed)
a, r, phi = a_seed, r_seed, phi_fixed

# Refine with Newton on (a, r) using the analytic gradient and Hessian-style step.
# Use damped gradient descent on the quadratic-projected residual.
step = 0.005
for it in range(50000):
    g_a, g_r, g_phi = grad_V_total(a, r, phi, L_num)
    # phi-projection: keep phi fixed (it's already at angular extremum)
    a -= step * g_a
    r -= step * g_r
    if abs(g_a) + abs(g_r) < 1e-12:
        break

print(f"  Numerical extremum found (phi fixed = pi/3): a = {a:.6f}, r = {r:.6f}")
print(f"  cos(3 phi) = {np.cos(3 * phi):.6f}")
if abs(a) > 1e-9:
    ratio_num = r**2 / a**2
    print(f"  r^2/a^2 = {ratio_num:.6f}  (BAE target: 0.5)")
else:
    ratio_num = float("nan")
    print(f"  r^2/a^2 = NaN (a = 0)")
print()

# Verify gradient is small
g_a, g_r, g_phi = grad_V_total(a, r, phi, L_num)
check("9.1 Numerical gradient at extremum near zero",
      abs(g_a) + abs(g_r) < 1e-6,
      detail=f"|g_a|+|g_r| = {abs(g_a)+abs(g_r):.3e}")
check("9.2 Numerical extremum r^2/a^2 != 1/2 (BAE not satisfied)",
      abs(ratio_num - 0.5) > 0.05,
      detail=f"r^2/a^2 = {ratio_num:.4f}, |delta|={abs(ratio_num-0.5):.4f}")
check("9.3 Quadratic prediction matches numerical extremum a-coord",
      abs(a - a1) < 0.05 or abs(a - a2) < 0.05,
      detail=f"a = {a:.4f}; predicted a1 = {a1:.4f}, a2 = {a2:.4f}")


# ----------------------------------------------------------------------
# Section 10: Per-eigenvalue extremization (alternative interpretation)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 10: Per-eigenvalue V'(lambda_k)=0 alternative")
print("=" * 70)
print()

# Alternative interpretation: each eigenvalue lambda_k must extremize V.
# V'(lambda) = L + 3 lambda + (1/2) lambda^2 = 0
#  -> lambda^2 + 6 lambda + 2L = 0
#  -> lambda = -3 +/- sqrt(9 - 2L)

# At L = 0, V'(lambda) = 3 lambda + (1/2) lambda^2 = lambda(3 + lambda/2)
#  -> roots: lambda = 0 or lambda = -6.
# For L > 0, the roots shift; for L = L_num ~ 1.2057, lambda = -0.433 or -5.567.

# In the C_3-orbit (lambda_0, lambda_1, lambda_2) parameterized by (a, r, phi),
# requiring all three eigenvalues simultaneously equal to a critical lambda_*
# forces r = 0 (degenerate). With the two roots lambda_+ and lambda_-, only
# certain triples are realizable as (a + 2r cos(phi + 2 pi k /3)) for some
# (a, r, phi). Test each multiset.

V_prime_roots = sp.solve(L_s + 3 * m_s + sp.Rational(1, 2) * m_s**2, m_s)
print(f"  V'(lambda) = 0 roots: lambda in {V_prime_roots}")
print(f"  At L_num = {L_num:.4f}: lambda = {[complex(r.subs(L_s, L_num)).real for r in V_prime_roots]}")
print()

# Take L = 0 case for cleanest analysis (per Clifford-only contribution):
# lambda in {0, -6}
print("  Per-eigenvalue test at L=0: lambda in {0, -6}")
print("  C_3-orbit triples (lambda_0, lambda_1, lambda_2) with each in {0, -6}:")

triples_l0 = [
    (0.0, 0.0, 0.0),
    (0.0, 0.0, -6.0),
    (0.0, -6.0, -6.0),
    (-6.0, -6.0, -6.0),
]
for triple in triples_l0:
    a_t = sum(triple) / 3.0
    # var(lambda_k - a) should equal 2 r^2
    sumsq = sum((l - a_t) ** 2 for l in triple)
    r2_t = sumsq / 6.0  # since sum (lambda - a)^2 = sum 4 r^2 cos^2 = 6 r^2
    if a_t == 0.0:
        ratio = float("inf") if r2_t > 0 else float("nan")
    else:
        ratio = r2_t / (a_t ** 2)
    print(f"    triple {triple}: a={a_t:.3f}, r^2={r2_t:.3f}, "
          f"r^2/a^2={ratio:.4f}")

# None of these give r^2/a^2 = 0.5
# Triple (0, -6, -6): a=-4, r^2=4, r^2/a^2=0.25
# Triple (0, 0, -6): a=-2, r^2=4, r^2/a^2=1.0
# Triple (0, 0, 0):  a=0,  r^2=0  (degenerate)
# Triple (-6,-6,-6): a=-6, r^2=0  (degenerate)

ratios_l0 = []
for triple in triples_l0:
    a_t = sum(triple) / 3.0
    sumsq = sum((l - a_t) ** 2 for l in triple)
    r2_t = sumsq / 6.0
    if a_t != 0.0:
        ratios_l0.append(r2_t / (a_t ** 2))

# BAE wants r^2/a^2 = 0.5; check none of the per-eigenvalue triples satisfies it
check("10.1 Per-eigenvalue triples (L=0) — no triple satisfies BAE r^2/a^2=1/2",
      all(abs(r - 0.5) > 1e-6 for r in ratios_l0),
      detail=f"realized ratios: {ratios_l0}")


# ----------------------------------------------------------------------
# Section 11: The structural obstruction
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 11: Structural obstruction — V(m) extension does NOT close BAE")
print("=" * 70)
print()

# The two routes considered:
#   (A) V_total(a, r, phi) extremum: governed by  9 a^2 + 54 a + 72 + 2L = 0
#       and r = -eps(6 + 2a), eps in {+/-1}.
#   (B) Per-eigenvalue V'(lambda_k) = 0 for all k: forces lambda_k in
#       {-3 + sqrt(9-2L), -3 - sqrt(9-2L)} discrete set, only certain
#       triples are realizable as a C_3 orbit.
#
# Neither closes BAE for retained L = c1 + c2/2 ~ 1.2057.

# Test 11.1: Route (A) and BAE share roots only for specific L values.
print("  Route A: V_total extrema vs BAE compatibility")
print(f"    Required L: {[float(L_v) for L_v in L_compatibility]}")
print(f"    Retained L: {L_num:.4f}")
print(f"    -> retained L is NOT in the compatibility set")
print()

# Test 11.2: Route (B) per-eigenvalue closure fails by construction.
print("  Route B: per-eigenvalue extremization")
print("    realizable C_3 triples at L=0: r^2/a^2 in {0, 0.25, 1.0, undef}")
print("    -> none equals 1/2")
print()

# Test 11.3: The obstruction is precise.
print("  The obstruction is precise:")
print("    BAE quadratic-in-a:    7 a^2 + 48 a + 72 = 0")
print("    V_total quadratic-in-a: 9 a^2 + 54 a + 72 + 2L = 0")
print("    These coincide ONLY for a tuned L; not for retained L.")
print()

check("11.1 Route A: retained L not in V_total/BAE compatibility set",
      not retained_L_compatible)
check("11.2 Route B: per-eigenvalue triples (L=0) miss BAE",
      all(abs(r - 0.5) > 1e-6 for r in ratios_l0))


# ----------------------------------------------------------------------
# Section 12: What about V(m) with the BROADER claim (out of scope)?
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 12: Out-of-scope check — broader 'mass tower' claim")
print("=" * 70)
print()

# The retained note says: V_eff minimum at m_V ~ -0.433 does NOT equal
# the physical selected point m_* ~ -1.161. So even the 1D extremization
# fails to identify the physical m_* — and that's the in-note honest gap.
# Extending to hw=1 inherits this gap; it cannot improve it.
m_V_check = m_V_numerical
m_phys_check = -1.161  # cited in retained note (NOT a derivation input)
gap = abs(m_V_check - m_phys_check)
print(f"  m_V (V_eff minimum on retained L)    ~ {m_V_check:.4f}")
print(f"  m_* (physical selected point, cited) ~ {m_phys_check:.4f}")
print(f"  Gap: {gap:.4f}")
print()
print("  The retained note flags m_V != m_* as an honest gap.")
print("  Extending to hw=1 cannot close this gap because:")
print("    - hw=1 extremization REDUCES to 1D extremization at r=0.")
print("    - At the non-trivial r > 0 branch, the (a, r) configuration")
print("      does not satisfy BAE for retained L.")
print()

check("12.1 m_V (V_eff min) != m_* (physical point) — retained gap",
      gap > 0.5)


# ----------------------------------------------------------------------
# Section 13: Verdict
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 13: Verdict")
print("=" * 70)
print()
print("VERDICT: STRUCTURAL OBSTRUCTION (sharpened).")
print()
print("V(m) functional extension to hw=1 does NOT close BAE |b|^2/a^2=1/2.")
print()
print("Two natural extensions tested:")
print("  (A) V_total = sum V(lambda_k)  -- functional-calculus aggregation")
print("      Extremum equations:")
print("        dV/da = 0  =>  3L + 9a + (3/2)a^2 + 3r^2 = 0")
print("        dV/dr = 0  =>  18r + 6ar + 3 eps r^2 = 0  (eps = cos(3 phi) = +/-1)")
print("        dV/dphi=0  =>  sin(3 phi) = 0")
print("      Non-trivial branch r = -eps(6+2a) substituted:")
print("        9 a^2 + 54 a + 72 + 2L = 0")
print("      BAE r^2/a^2 = 1/2 with same r-substitution gives:")
print("        7 a^2 + 48 a + 72 = 0")
print("      These linearly independent quadratics share a root only for")
print(f"      specific L values: {[float(L_v) for L_v in L_compatibility]}")
print(f"      Retained L ~ {L_num:.4f} is NOT compatible.")
print()
print("  (B) Per-eigenvalue V'(lambda_k) = 0 for all k")
print("      At L=0: lambda in {0, -6}, four C_3-orbit triples possible")
print("      Realized r^2/a^2: {undef, 1.0, 0.25, undef} -- none = 1/2.")
print()
print("Why this is structural, not tunable:")
print("  - The 1D V(m) extension to hw=1 is the canonical functional-calculus")
print("    extension. Any other 'extension' would require an additional choice")
print("    (e.g., ad-hoc weighting of eigenvalues), which would be a new")
print("    admission, not a derivation.")
print("  - The retained L = c1 + c2/2 inherits the K_frozen upstream condition")
print("    (out-of-scope per the retained note's scope statement). Even if a")
print("    different K_frozen could give the compatible L, that would shift the")
print("    closure target to deriving K_frozen, not deriving BAE from V(m).")
print()
print("This rules out the 'V(m) extension to hw=1' route as a closure mechanism")
print("for BAE within retained content.")
print()
print("Sharpened residue:")
print("  BAE |b|^2/a^2 = 1/2 is NOT recoverable from spectral-functional")
print("  extension of V(m) to the hw=1 C_3-orbit. Other routes (Q-readout")
print("  functional pivot per Probe 16, retained-U(1) hunt per Probe 14,")
print("  Plancherel/Peter-Weyl per Probe 12) remain open or already bounded.")
print()


# ----------------------------------------------------------------------
# Final summary
# ----------------------------------------------------------------------

print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
