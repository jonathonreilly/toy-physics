#!/usr/bin/env python3
"""Pattern A narrow runner for `BETA_GBARE_RESCALING_ABSTRACT_IDENTITY_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone polynomial-algebra identity:

  Let (g, c, N) be abstract symbolic variables with g > 0, c > 0, and
  N arbitrary in any field of characteristic zero. Define

      beta(g, N)  :=  2 N / g^2.                                   (1)

  Then under the multiplicative rescaling g -> g / c,

      beta(g/c, N)  =  c^2 * beta(g, N).                           (3)

  Equivalently, the product beta(g, N) * g^2 = 2 N is invariant under
  the joint rescaling (g, beta) -> (g/c, c^2 * beta).

This is pure polynomial algebra over the rationals. No lattice gauge
theory, no Wilson plaquette action, no Cl(3) framework input, no SU(N_c)
gauge group, no physical bare-coupling identification, and no external
numerical or unit-convention import.

The narrow theorem applies in particular to the special instance
(g, N, c) = (1, 3, 2) (which yields beta(1, 3) = 6 and beta(1/2, 3) = 24,
giving 24 = 4 * 6 = c^2 * beta as required), but does not claim those
values; the abstract identity is the only premise.

Companion role: not a new audit-companion; this is a Pattern A new
narrow claim row carving out the pure-algebra core of the symbolic
rescaling content underlying the existing
`g_bare_canonical_convention_narrow_theorem_note_2026-05-02`. The narrow
theorem here drops the upstream graph-first SU(N_c) and Wilson-action
dependencies entirely by stating only the abstract algebraic identity.
"""

from fractions import Fraction
from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, simplify, symbols, expand, together
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "BETA_GBARE_RESCALING_ABSTRACT_IDENTITY_NARROW_THEOREM_NOTE_2026-05-10.md"

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
section("Pattern A narrow theorem: beta(g/c, N) = c^2 * beta(g, N) (abstract)")
# Pure polynomial algebra over Q. No lattice gauge theory input.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: symbolic algebraic identity (T1) via sympy")
# ----------------------------------------------------------------------------
g, c, N = symbols('g c N', positive=True, real=True)

beta = 2 * N / g**2
beta_rescaled = beta.subs(g, g / c)

print(f"\n  beta(g, N) = {beta}")
print(f"  beta(g/c, N) = {simplify(beta_rescaled)}")

residual_T1 = simplify(beta_rescaled - c**2 * beta)
print(f"  residual T1 (beta(g/c, N) - c^2 * beta(g, N)) = {residual_T1}")
check("T1 symbolic: beta(g/c, N) - c^2 * beta(g, N) is identically zero",
      residual_T1 == 0,
      detail=f"sympy.simplify gives {residual_T1}")

# Cross-confirm via expand on a common denominator.
residual_T1_expanded = expand(together(beta_rescaled - c**2 * beta))
check("T1 via expand+together: residual is 0 as polynomial fraction",
      residual_T1_expanded == 0,
      detail=f"expand(together(...)) = {residual_T1_expanded}")


# ----------------------------------------------------------------------------
section("Part 2: joint-rescaling invariance (T2) via sympy")
# ----------------------------------------------------------------------------
# Joint rescaling: g -> g/c, beta -> c^2 * beta.
# Invariance: (c^2 * beta) * (g/c)^2 = beta * g^2 = 2 N.
beta_new = c**2 * beta
g_new = g / c
product_original = beta * g**2
product_rescaled = beta_new * g_new**2

print(f"\n  beta * g^2 = {simplify(product_original)}")
print(f"  (c^2 * beta) * (g/c)^2 = {simplify(product_rescaled)}")

residual_T2 = simplify(product_rescaled - product_original)
check("T2 symbolic: (c^2 * beta) * (g/c)^2 - beta * g^2 is identically zero",
      residual_T2 == 0,
      detail=f"simplify gives {residual_T2}")

residual_T2_to_2N = simplify(product_rescaled - 2 * N)
check("T2 symbolic: rescaled product equals 2 N",
      residual_T2_to_2N == 0,
      detail=f"residual to 2 N = {residual_T2_to_2N}")


# ----------------------------------------------------------------------------
section("Part 3: concrete rational instances of (T1) at exact precision")
# ----------------------------------------------------------------------------
# beta_rat(g, N) := 2 N / g^2 over Fraction.
def beta_rat(g_val, N_val):
    return Fraction(2) * Fraction(N_val) / Fraction(g_val)**2


cases = [
    (Fraction(1), Fraction(3), Fraction(2), "g=1, N=3, c=2"),
    (Fraction(2), Fraction(3), Fraction(3), "g=2, N=3, c=3"),
    (Fraction(1), Fraction(5), Fraction(1, 2), "g=1, N=5, c=1/2"),
    (Fraction(3), Fraction(7), Fraction(7, 11), "g=3, N=7, c=7/11"),
    (Fraction(1), Fraction(1), Fraction(1), "g=1, N=1, c=1 (trivial rescaling)"),
    (Fraction(5, 7), Fraction(11, 13), Fraction(2, 9), "g=5/7, N=11/13, c=2/9"),
]

for g_val, N_val, c_val, label in cases:
    lhs = beta_rat(g_val / c_val, N_val)
    rhs = c_val**2 * beta_rat(g_val, N_val)
    check(f"T1 concrete ({label}): beta(g/c, N) = c^2 * beta(g, N)",
          lhs == rhs,
          detail=f"lhs={lhs}, rhs={rhs}")


# ----------------------------------------------------------------------------
section("Part 4: non-trivial rescaling strictly changes beta when N != 0 (T3)")
# ----------------------------------------------------------------------------
# For c != 1 and N != 0, beta(g/c, N) != beta(g, N).
nontrivial_cases = [
    (Fraction(1), Fraction(3), Fraction(2)),
    (Fraction(2), Fraction(3), Fraction(3)),
    (Fraction(1), Fraction(5), Fraction(1, 2)),
    (Fraction(3), Fraction(7), Fraction(7, 11)),
    (Fraction(5, 7), Fraction(11, 13), Fraction(2, 9)),
]

for g_val, N_val, c_val in nontrivial_cases:
    if c_val == Fraction(1) or N_val == Fraction(0):
        continue
    beta_orig = beta_rat(g_val, N_val)
    beta_resc = beta_rat(g_val / c_val, N_val)
    check(f"T3 non-trivial (g={g_val}, N={N_val}, c={c_val}): beta strictly changes",
          beta_orig != beta_resc,
          detail=f"beta_orig={beta_orig}, beta_rescaled={beta_resc}")


# ----------------------------------------------------------------------------
section("Part 5: orbit exhaustion of g under sigma_c (T3 surjectivity)")
# ----------------------------------------------------------------------------
# For (g0, N0) = (1, 3) and any positive rational g', selecting c = g0 / g'
# sends g0 -> g'. Cover a representative grid.
g0 = Fraction(1)
N0 = Fraction(3)
target_grid = [Fraction(1, 7), Fraction(2, 5), Fraction(3, 4), Fraction(1),
               Fraction(7, 4), Fraction(13, 11), Fraction(99, 100)]
for g_target in target_grid:
    c_choice = g0 / g_target  # positive rational
    g_image = g0 / c_choice
    check(f"T3 orbit-exhaustion: c = g0/g' = {c_choice} sends g0=1 -> g'={g_target}",
          g_image == g_target,
          detail=f"g0/c = {g_image}")


# ----------------------------------------------------------------------------
section("Part 6: invariance of the product beta * g^2 at exact rational")
# ----------------------------------------------------------------------------
for g_val, N_val, c_val, label in cases:
    beta_orig = beta_rat(g_val, N_val)
    prod_orig = beta_orig * g_val**2
    g_new = g_val / c_val
    beta_new = c_val**2 * beta_orig
    prod_new = beta_new * g_new**2
    expected = Fraction(2) * N_val
    check(f"T2 concrete ({label}): rescaled product equals 2 N = {expected}",
          prod_new == expected and prod_orig == expected,
          detail=f"prod_orig={prod_orig}, prod_new={prod_new}, 2N={expected}")


# ----------------------------------------------------------------------------
section("Part 7: independence from any lattice / Cl(3) / SU(N_c) input")
# ----------------------------------------------------------------------------
# The narrow theorem holds for any abstract (g, c, N). The "Wilson lattice
# instance" (g, N, c) = (g_bare, N_c, ...) is a SPECIAL CASE; the theorem
# does not depend on, derive, or claim those identifications.
#
# Demonstrate the identity at a non-physical instance with N=0:
g_irr = Fraction(7, 13)
N_zero = Fraction(0)
c_any = Fraction(5, 3)
# When N=0, beta(g, 0) = 0 for all g, so c^2 * 0 = 0 trivially.
beta_zero_lhs = Fraction(2) * N_zero / (g_irr / c_any)**2
beta_zero_rhs = c_any**2 * (Fraction(2) * N_zero / g_irr**2)
check("non-physical instance N=0 still satisfies identity (trivially)",
      beta_zero_lhs == beta_zero_rhs == Fraction(0),
      detail=f"both sides = 0 when N=0")

# Demonstrate at irrational symbolic instance via sympy (no lattice content):
# (g, N, c) all symbolic, no specific value assigned.
symbolic_residual = simplify((Fraction(2) * N / (g / c)**2) - c**2 * (Fraction(2) * N / g**2))
check("identity holds at fully symbolic (g, N, c) with no numerical values",
      symbolic_residual == 0,
      detail=f"residual at fully symbolic = {symbolic_residual}")


# ----------------------------------------------------------------------------
section("Part 8: note structure and narrow-scope discipline")
# ----------------------------------------------------------------------------
note_text = NOTE_PATH.read_text()
required = [
    "β–g_bare Rescaling Abstract Identity Narrow Theorem",
    "Claim type:** positive_theorem",
    "polynomial-algebra identity",
    "no lattice gauge theory",
    "no Wilson plaquette action",
    "Cl(3) framework input",
    "Cited dependencies\n\nNone",
    "Forbidden imports check",
    "β(g, N)  :=  2 N / g²",
    "β(g / c, N)  =  c² · β(g, N)",
]
for s in required:
    check(f"note contains: {s!r}", s in note_text)

# Critical: the narrow note must NOT claim physical-convention identifications.
forbidden = [
    "g_bare = 1 is uniquely forced",
    "Wilson plaquette action is uniquely forced",
    "g_bare = 1 follows from Cl(3)",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden physical claim: {f!r}",
          f not in note_text)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (g, c, N) be abstract symbolic variables with g > 0, c > 0, and
    N arbitrary in any field of characteristic zero. Define

        beta(g, N)  :=  2 N / g^2.

  CONCLUSION:
    Under the multiplicative rescaling g -> g / c,

        beta(g/c, N)  =  c^2 * beta(g, N).                          (T1)

    Equivalently, the product beta(g, N) * g^2 = 2 N is invariant under
    the joint rescaling (g, beta) -> (g/c, c^2 * beta).              (T2)

    The orbit of any positive g under sigma_c is the entire positive
    ray, and the beta-fiber over each value is a single point in g.   (T3)

  Audit-lane class:
    (A) -- pure polynomial algebra over Q. No external numerical,
    lattice, Cl(3), or SU(N_c) input. Proof is one-line direct
    substitution.

  This narrow theorem is independent of the sibling g_bare canonical-
  convention narrow theorem's physical Wilson-action / SU(N_c=3)
  framing. The Wilson lattice instance (g, N, c) = (g_bare, N_c, ...) is
  just one application; the rescaling identity holds for any abstract
  (g, c, N) by the same algebraic substitution.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
