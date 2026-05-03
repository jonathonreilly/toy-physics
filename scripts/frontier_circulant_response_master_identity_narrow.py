#!/usr/bin/env python3
"""Pattern A narrow runner for `CIRCULANT_RESPONSE_MASTER_IDENTITY_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone Hermitian-circulant response identity:

  Let C be the 3x3 cyclic permutation matrix on C^3 (C^3 = I), and define
  the circulant Hermitian family

      G(g_0, g_1)  =  g_0 * I  +  g_1 * C  +  conjugate(g_1) * C^2,
                       g_0 ∈ R, g_1 ∈ C.

  With cyclic basis B_0 = I, B_1 = C + C^2, B_2 = i (C - C^2), define
  the Frobenius-pairing responses

      r_0  =  Re Tr(G B_0),
      r_1  =  Re Tr(G B_1),
      r_2  =  Re Tr(G B_2).

  THEN:
    (i)   r_0 = 3 g_0,
          r_1 = 6 Re(g_1),
          r_2 = 6 Im(g_1).
    (ii)  Master identity:
              2 r_0^2  -  (r_1^2 + r_2^2)  =  18 (g_0^2 - 2 |g_1|^2).
    (iii) The Koide cone condition `2 r_0^2 = r_1^2 + r_2^2` is exactly
          equivalent to the global one-scalar equation
          `g_0^2 = 2 |g_1|^2`. On the open subdomain `g_1 != 0`,
          this can be written as kappa := g_0^2 / |g_1|^2 = 2.

This is class-A pure linear algebra on Hermitian circulant 3x3 matrices.
No Koide / charged-lepton / observable-principle / second-order-return
framework input is consumed.

"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros, I as sym_I, im, re, conjugate, expand
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: Hermitian-circulant response master identity")
# ============================================================================

# 3x3 cyclic permutation matrix
C = Matrix([[0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]])
C2 = C * C
C3 = C * C * C
I3 = eye(3)

# Sanity: C^3 = I, Tr(C) = Tr(C^2) = 0.
check("C^3 = I exact",
      C3 == I3)
check("Tr(C) = 0 exact",
      C.trace() == 0)
check("Tr(C^2) = 0 exact",
      C2.trace() == 0)


# ----------------------------------------------------------------------------
section("Part 1: Hermitian circulant family G(g_0, g_1)")
# ----------------------------------------------------------------------------
g_0 = symbols('g_0', real=True)
g_1_re, g_1_im = symbols('g_1_re g_1_im', real=True)
g_1 = g_1_re + sym_I * g_1_im
g_1_conj = g_1_re - sym_I * g_1_im

G = g_0 * I3 + g_1 * C + g_1_conj * C2

# G is Hermitian
G_dagger = G.H
check("G(g_0, g_1) is Hermitian (G = G^dagger)",
      simplify(G - G_dagger) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 2: cyclic basis B_0 = I, B_1 = C + C^2, B_2 = i (C - C^2) Hermitian")
# ----------------------------------------------------------------------------
B_0 = I3
B_1 = C + C2
B_2 = sym_I * (C - C2)

check("B_0 Hermitian",
      B_0 == B_0.H)
check("B_1 Hermitian",
      simplify(B_1 - B_1.H) == zeros(3, 3))
check("B_2 Hermitian",
      simplify(B_2 - B_2.H) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 3: response formulas r_0 = 3 g_0, r_1 = 6 Re(g_1), r_2 = 6 Im(g_1)")
# ----------------------------------------------------------------------------
def Re_Tr(M):
    return simplify(re(M.trace()))


r_0 = Re_Tr(G * B_0)
r_1 = Re_Tr(G * B_1)
r_2 = Re_Tr(G * B_2)

print(f"\n  r_0 = {r_0}")
print(f"  r_1 = {r_1}")
print(f"  r_2 = {r_2}")

check("r_0 = 3 g_0 exact",
      simplify(r_0 - 3 * g_0) == 0,
      detail=f"r_0 = {r_0}")
check("r_1 = 6 Re(g_1) = 6 g_1_re exact",
      simplify(r_1 - 6 * g_1_re) == 0,
      detail=f"r_1 = {r_1}")
check("r_2 = 6 Im(g_1) = 6 g_1_im exact",
      simplify(r_2 - 6 * g_1_im) == 0,
      detail=f"r_2 = {r_2}")


# ----------------------------------------------------------------------------
section("Part 4: Master identity 2 r_0^2 - (r_1^2 + r_2^2) = 18 (g_0^2 - 2 |g_1|^2)")
# ----------------------------------------------------------------------------
LHS = simplify(2 * r_0**2 - (r_1**2 + r_2**2))
g_1_sq = g_1_re**2 + g_1_im**2  # |g_1|^2
RHS = simplify(18 * (g_0**2 - 2 * g_1_sq))
check("Master identity 2 r_0^2 - (r_1^2 + r_2^2) = 18 (g_0^2 - 2 |g_1|^2) symbolic",
      simplify(LHS - RHS) == 0,
      detail=f"LHS - RHS = {simplify(LHS - RHS)}")


# ----------------------------------------------------------------------------
section("Part 5: Koide cone reduces to one-scalar equation g_0^2 = 2 |g_1|^2")
# ----------------------------------------------------------------------------
# 2 r_0^2 = r_1^2 + r_2^2  iff  g_0^2 = 2 |g_1|^2.
# At g_0^2 = 2 |g_1|^2: 18(g_0^2 - 2 |g_1|^2) = 0, hence LHS = 0.
sub_on_cone = {g_0: sympy.sqrt(2) * sympy.sqrt(g_1_sq)}
LHS_on_cone = simplify(LHS.subs(sub_on_cone))
check("On cone g_0 = sqrt(2) |g_1|: 2 r_0^2 - (r_1^2 + r_2^2) = 0 exact",
      LHS_on_cone == 0,
      detail=f"LHS at cone = {LHS_on_cone}")


# ----------------------------------------------------------------------------
section("Part 6: kappa = g_0^2 / |g_1|^2 = 2 on the nonzero cone")
# ----------------------------------------------------------------------------
# kappa is well-defined when g_1 != 0; on cone, kappa = 2.
g_1_re_concrete, g_1_im_concrete = Rational(1, 3), Rational(1, 5)
g_1_sq_concrete = g_1_re_concrete**2 + g_1_im_concrete**2
g_0_concrete_on_cone = sympy.sqrt(2 * g_1_sq_concrete)
kappa_on_cone = simplify(g_0_concrete_on_cone**2 / g_1_sq_concrete)
check("at concrete nonzero (g_1_re, g_1_im) = (1/3, 1/5) on cone: kappa = 2",
      simplify(kappa_on_cone - Rational(2)) == 0,
      detail=f"kappa = {kappa_on_cone}")


# ----------------------------------------------------------------------------
section("Part 7: trace identities used in the response derivation")
# ----------------------------------------------------------------------------
# Tr(C) = Tr(C^2) = 0, Tr(C^3) = 3.
# Tr(I . I) = 3, Tr(I . C) = Tr(C) = 0, Tr(I . C^2) = 0.
# Tr(C . I) = 0, Tr(C . C) = Tr(C^2) = 0, Tr(C . C^2) = Tr(C^3) = 3.
# Etc.
check("Tr(C^3) = 3 exact",
      C3.trace() == 3)
check("Tr(C * C^2) = Tr(C^3) = 3 exact",
      (C * C2).trace() == 3)
check("Tr(C^2 * C) = Tr(C^3) = 3 exact",
      (C2 * C).trace() == 3)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let C be the 3x3 cyclic permutation matrix and define
        G(g_0, g_1) = g_0 I + g_1 C + conjugate(g_1) C^2,
            g_0 ∈ R, g_1 ∈ C,
    with cyclic basis B_0 = I, B_1 = C + C^2, B_2 = i (C - C^2).
    Define responses
        r_i = Re Tr(G B_i)  for i = 0, 1, 2.

  CONCLUSION:
    (T1) r_0 = 3 g_0, r_1 = 6 Re(g_1), r_2 = 6 Im(g_1).
    (T2) Master identity:
            2 r_0^2 - (r_1^2 + r_2^2)  =  18 (g_0^2 - 2 |g_1|^2).
    (T3) Koide cone condition 2 r_0^2 = r_1^2 + r_2^2 is exactly
         equivalent to the global equation g_0^2 = 2 |g_1|^2.
         On the open subdomain g_1 != 0 this can also be written as
         kappa := g_0^2 / |g_1|^2 = 2. At g_1 = 0 the cone forces
         g_0 = 0 and the kappa quotient is undefined.

  Audit-lane class:
    (A) — pure linear algebra on Hermitian-circulant 3x3 matrices and
    cyclic basis. No Koide / charged-lepton / observable-principle
    framework input.

  This narrow theorem isolates the response-master identity from the
  parent's bundled framework. The parent's bounded one-scalar
  obstruction conclusion still requires the upstream A1 cited
  hw=1 triplet, A2 observable principle, A3 second-order return,
  but the underlying linear-algebra response computation becomes
  audit-able as a standalone primitive.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
