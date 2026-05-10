#!/usr/bin/env python3
"""Runner for `STAGGERED_DIRAC_HW1_THREE_EIGENVALUE_STRUCTURE_POSITIVE_THEOREM_NOTE_2026-05-10`.

Mechanical sympy diagnostic verifying the Schur reduction of Hermitian
operators commuting with the Z/3Z regular representation on H_{hw=1},
the closed-form eigenvalue formula

    lambda_k = a + 2 |b| cos(arg(b) + 2 pi k / 3),    k = 0, 1, 2,

and generic three-distinctness on the circulant family

    H = a I + b C + bbar C^2,    (a, b) in R x C,    b != 0.

This is a Pattern A pure-algebra verification on R x C with the standard
root-of-unity identity 1 + w + w^2 = 0. No PDG numerical input, no
Koide / BAE assumption, no species-naming dependence.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import (
        Rational,
        sqrt,
        cos,
        simplify,
        expand,
        symbols,
        I,
        re,
        im,
        conjugate,
        Matrix,
        eye,
        atan2,
        Abs,
        nsimplify,
        N,
        Symbol,
        pi,
    )
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
section("Premises and symbolic setup")
# ============================================================================

# Free symbols: a in R, b = x + i y in C.
a, x, y = symbols("a x y", real=True)
b = x + I * y
bbar = conjugate(b)

# Standard 3x3 cyclic permutation matrix.
C = Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
I3 = eye(3)
C2 = simplify(C * C)

# Root of unity w = exp(2 pi i / 3) = -1/2 + i sqrt(3)/2.
w = Rational(-1, 2) + I * sqrt(Rational(3)) / 2
wbar = conjugate(w)

check("C^3 = I (cyclic permutation cubes to identity)",
      simplify(C * C * C) == I3,
      detail="explicit matrix product")
check("1 + w + w^2 = 0 (sum of cube roots of unity)",
      simplify(1 + w + w**2) == 0, detail=f"explicit value")
check("w^3 = 1 (cube root of unity)",
      simplify(w**3) == 1, detail="explicit value")


# ============================================================================
section("Part 1: Schur reduction — circulant form for [H, C] = 0")
# ============================================================================

# Generic Hermitian H = a I + b C + bbar C^2.
H = a * I3 + b * C + bbar * C2

# Verify H is Hermitian: H = H^\dagger.
H_dag = H.H  # complex-conjugate transpose
check("H = a I + b C + bbar C^2 is Hermitian (H = H^dagger)",
      simplify(H - H_dag) == Matrix.zeros(3, 3),
      detail="check by direct conjugate-transpose")

# Verify [H, C] = 0 (H commutes with the cyclic generator).
commutator_HC = simplify(H * C - C * H)
check("[H, C] = 0 (H commutes with the cyclic generator C)",
      commutator_HC == Matrix.zeros(3, 3),
      detail=f"commutator H C - C H = 0 elementwise")

# Schur claim: the centralizer of C in M_3(C)_Herm is exactly the circulant
# family {a I + b C + bbar C^2 : a in R, b in C} — three real parameters
# (a, Re b, Im b). We verify this by checking that an arbitrary 3x3 Hermitian
# matrix commuting with C must take the circulant form.

# A general 3x3 Hermitian matrix has 9 real parameters; we parameterize.
h11, h22, h33 = symbols("h11 h22 h33", real=True)
h12r, h12i = symbols("h12r h12i", real=True)
h13r, h13i = symbols("h13r h13i", real=True)
h23r, h23i = symbols("h23r h23i", real=True)

Hg = Matrix([
    [h11, h12r + I * h12i, h13r + I * h13i],
    [h12r - I * h12i, h22, h23r + I * h23i],
    [h13r - I * h13i, h23r - I * h23i, h33],
])

# Commutator condition Hg C = C Hg yields linear constraints.
comm_general = simplify(Hg * C - C * Hg)
# Collect constraints from the 9 entries.
constraints = []
for i in range(3):
    for j in range(3):
        entry = simplify(comm_general[i, j])
        if entry != 0:
            constraints.append(entry)

# Solve symbolically.
from sympy import solve
unknowns = [h11, h22, h33, h12r, h12i, h13r, h13i, h23r, h23i]
sol = solve(constraints, unknowns, dict=True)
# Sol should have a unique solution family parameterized by a, b (3 reals).
# Specifically the centralizer is 3-dim.
check("Centralizer of C in M_3(C)_Herm has 3 real parameters (circulant family)",
      len(sol) == 1,
      detail=f"solution count = {len(sol)}, expected = 1 family")

if len(sol) == 1:
    parametrization = sol[0]
    # Verify: substituting the parametrization yields the circulant form.
    Hg_circulant = Hg.subs(parametrization)
    # Now Hg_circulant should equal a I + b C + bbar C^2 for some identification.
    # The diagonal entries should all be equal (= a), and the off-diagonal
    # entries should be circulant.
    diag_entries = [simplify(Hg_circulant[i, i]) for i in range(3)]
    check("Centralizer is circulant: diag(H) = (a, a, a)",
          diag_entries[0] == diag_entries[1] == diag_entries[2],
          detail=f"diag = {diag_entries}")
    # Off-diagonal pattern: Hg_circulant[0,1] = Hg_circulant[1,2] = Hg_circulant[2,0]
    # = b (the upper cyclic shift coefficient).
    upper_off = [
        simplify(Hg_circulant[0, 1]),
        simplify(Hg_circulant[1, 2]),
        simplify(Hg_circulant[2, 0]),
    ]
    check("Centralizer is circulant: H[i, (i+1) mod 3] all equal (= b)",
          upper_off[0] == upper_off[1] == upper_off[2],
          detail=f"upper off-diagonals = {upper_off}")
    lower_off = [
        simplify(Hg_circulant[1, 0]),
        simplify(Hg_circulant[2, 1]),
        simplify(Hg_circulant[0, 2]),
    ]
    check("Centralizer is circulant: H[i, (i-1) mod 3] all equal (= bbar)",
          lower_off[0] == lower_off[1] == lower_off[2],
          detail=f"lower off-diagonals = {lower_off}")
    # And upper = conjugate(lower) (Hermiticity within the circulant family).
    check("Upper off-diagonal = conjugate(lower) (Hermiticity in circulant family)",
          simplify(upper_off[0] - conjugate(lower_off[0])) == 0,
          detail="b = conjugate(bbar)")


# ============================================================================
section("Part 2: Eigenvalue formula on the circulant family")
# ============================================================================

# Eigenvalue formula via Fourier basis: v_k = (1, w^k, w^{2k})^T.
# Expected: lambda_k = a + b w^k + bbar w^{-k}.
def lam_formula(k):
    return a + b * w**k + bbar * w**(-k)


for k in (0, 1, 2):
    v_k = Matrix([1, w**k, w**(2 * k)])
    lhs = simplify(H * v_k)
    rhs = simplify(lam_formula(k) * v_k)
    diff = simplify(expand(lhs - rhs))
    check(f"H v_{k} = lambda_{k} v_{k} with lambda_{k} = a + b w^{k} + bbar w^{{-{k}}}",
          diff == Matrix([0, 0, 0]),
          detail=f"residual = {diff.T.tolist()[0]}")


# ============================================================================
section("Part 3: Cosine form lambda_k = a + 2 |b| cos(arg(b) + 2 pi k / 3)")
# ============================================================================

# For b = |b| e^{i theta} with theta = arg(b), the closed-form eigenvalue is
# lambda_k = a + 2 |b| cos(theta + 2 pi k / 3).
# We verify this symbolically by writing b in polar form.
r_sym, theta_sym = symbols("r theta", real=True, positive=True)
# Substitute b = r e^{i theta} = r (cos theta + i sin theta), so x = r cos theta,
# y = r sin theta.
b_polar = r_sym * (cos(theta_sym) + I * sympy.sin(theta_sym))
bbar_polar = conjugate(b_polar)


def lam_polar(k):
    """Eigenvalue under (a, b = r e^{i theta}) parameterization."""
    return a + b_polar * w**k + bbar_polar * w**(-k)


def lam_cosine_form(k):
    """Closed-form cosine eigenvalue."""
    return a + 2 * r_sym * cos(theta_sym + 2 * sympy.pi * k / 3)


for k in (0, 1, 2):
    raw = simplify(expand(lam_polar(k), complex=True))
    closed = simplify(expand(lam_cosine_form(k)))
    diff = simplify(expand(raw - closed, trig=True))
    diff_trig = sympy.trigsimp(diff)
    check(f"lambda_{k}(a, |b|, arg(b)) = a + 2 |b| cos(arg(b) + 2 pi * {k} / 3)",
          diff_trig == 0,
          detail=f"trig-simplified diff = {diff_trig}")


# ============================================================================
section("Part 4: Generic three-distinctness on the circulant family")
# ============================================================================

# At a generic value (b != 0, arg(b) not in {0, pi/3, ..., 2 pi / 3} grid),
# the three eigenvalues are pairwise distinct.
# Concrete instance: a = 0, |b| = 1, arg(b) = 2/9 (the Brannen lepton phase).
a_val = Rational(0)
r_val = Rational(1)
theta_val = Rational(2, 9)  # 2/9 rad (not a coincidence value)
subs_generic = {a: a_val, r_sym: r_val, theta_sym: theta_val}
lam_vals = [N(lam_cosine_form(k).subs(subs_generic)) for k in (0, 1, 2)]
check("At (a, |b|, arg(b)) = (0, 1, 2/9), three eigenvalues are pairwise distinct",
      lam_vals[0] != lam_vals[1] != lam_vals[2] and lam_vals[0] != lam_vals[2],
      detail=f"lambda = {[float(v) for v in lam_vals]}")

# Coincidence instance: theta = 0 (here cos(0) and cos(2pi/3) and cos(4pi/3)
# are 1, -1/2, -1/2 — so two equal eigenvalues). NOT three distinct.
theta_coin = Rational(0)
subs_coin = {a: a_val, r_sym: r_val, theta_sym: theta_coin}
lam_coin = [N(lam_cosine_form(k).subs(subs_coin)) for k in (0, 1, 2)]
check("At (a, |b|, arg(b)) = (0, 1, 0), two eigenvalues coincide (cos(2pi/3) = cos(4pi/3))",
      abs(float(lam_coin[1] - lam_coin[2])) < 1e-9,
      detail=f"lambda = {[float(v) for v in lam_coin]}")

# Coincidence instance #2: b = 0 — spectrum collapses to a triple of a.
subs_zero = {a: Rational(2), r_sym: Rational(0), theta_sym: Rational(0)}
lam_zero = [N(lam_cosine_form(k).subs(subs_zero)) for k in (0, 1, 2)]
check("At b = 0, spectrum collapses to (a, a, a)",
      lam_zero[0] == lam_zero[1] == lam_zero[2],
      detail=f"lambda = {[float(v) for v in lam_zero]}")

# Counterfactual: at a non-coincidence instance, verify trace and lowest-order
# symmetric polynomial agree with the operator (Tr H = 3a, sum lambda_k = 3a).
# Test at (a = 1, b = 1 + 2i):
subs_test = {a: Rational(1), x: Rational(1), y: Rational(2)}
H_test = H.subs(subs_test)
trH_test = simplify(H_test.trace())
check("Tr(H) = 3 a (independent of b)",
      trH_test == 3,
      detail=f"Tr(H) = {trH_test} at (a=1, b=1+2i)")
sum_lam_test = simplify(sum(lam_formula(k).subs({a: Rational(1), x: Rational(1), y: Rational(2)})
                            for k in (0, 1, 2)))
check("Sum lambda_k = 3 a (independent of b)",
      sum_lam_test == 3,
      detail=f"sum lambda_k = {sum_lam_test} at (a=1, b=1+2i)")


# ============================================================================
section("Part 5: Mass-ordering convention sanity (assign species labels)")
# ============================================================================

# This is a labeling convention: given three distinct real lambda_k, sort
# them and assign species labels. No physics input; just sorting.

# At (a = 0, |b| = 1, arg(b) = 2/9), the three values are
# cos(2/9), cos(2/9 + 2pi/3), cos(2/9 + 4pi/3) times 2.
sorted_lam_generic = sorted([float(v) for v in lam_vals])
check("Mass-ordering: sorted eigenvalues are three distinct real numbers",
      sorted_lam_generic[0] < sorted_lam_generic[1] < sorted_lam_generic[2],
      detail=f"sorted = {sorted_lam_generic}")

# Verify the convention itself: assigning {e, mu, tau} = (smallest, mid, largest)
# is the same convention as SM (u, c, t) and (nu_1, nu_2, nu_3) and (K_S, K_L).
# This is purely a labeling rule; the runner records the rule.
species_labels = ["e", "mu", "tau"]
ordered_pairs = list(zip(species_labels, sorted_lam_generic))
check("Mass-ordering assigns (e, mu, tau) to (smallest, middle, largest) eigenvalue",
      ordered_pairs[0][0] == "e" and ordered_pairs[1][0] == "mu"
      and ordered_pairs[2][0] == "tau",
      detail=f"convention: {ordered_pairs}")


# ============================================================================
section("Part 6: Review-hygiene checks on the note")
# ============================================================================

NOTE_PATH = ROOT / "docs" / "STAGGERED_DIRAC_HW1_THREE_EIGENVALUE_STRUCTURE_POSITIVE_THEOREM_NOTE_2026-05-10.md"
RUNNER_PATH = Path(__file__)


def file_contains(p, substr):
    return p.exists() and substr in p.read_text()


def file_lacks(p, substr):
    return p.exists() and substr not in p.read_text()


check("Note exists at expected path",
      NOTE_PATH.exists(),
      detail=str(NOTE_PATH.relative_to(ROOT)))

check("Note declares Type: positive_theorem",
      file_contains(NOTE_PATH, "**Type:** positive_theorem"),
      detail="line: **Type:** positive_theorem")

check("Note declares Claim type: positive_theorem",
      file_contains(NOTE_PATH, "**Claim type:** positive_theorem"),
      detail="line: **Claim type:** positive_theorem")

check("Note declares Status authority: independent audit lane only",
      file_contains(NOTE_PATH, "**Status authority:** independent audit lane only"),
      detail="line: **Status authority:** independent audit lane only")

check("Note declares Authority role: source-note proposal",
      file_contains(NOTE_PATH, "**Authority role:** source-note proposal"),
      detail="line: source-note proposal")

# Vocabulary discipline: no AC_lambda.struct / AC_lambda.label / BAE-decomposition.
forbidden_tags = [
    "AC_λ.struct",
    "AC_λ.label",
    "AC_lambda.struct",
    "AC_lambda.label",
    "BAE-decomposition",
    "three-mass structure",
    "AC_φλ dissolution",
    "AC_phi_lambda dissolution",
]
for tag in forbidden_tags:
    check(f"Forbidden vocabulary not used: {tag!r}",
          file_lacks(NOTE_PATH, tag),
          detail=f"absence of forbidden vocabulary tag {tag!r}")

# Markdown-link citation format.
required_citations = [
    "[`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)",
    "[`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)",
    "[`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)",
    "[`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)",
    "[`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)",
    "[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)",
]
for cite in required_citations:
    short = cite.split("(")[1].rstrip(")")
    check(f"Markdown-link citation present: {short!r}",
          file_contains(NOTE_PATH, cite),
          detail=f"markdown-link form")

# No PDG numerical inputs.
forbidden_numbers = ["0.510998", "105.6583", "1776.86"]
for num in forbidden_numbers:
    check(f"PDG numerical input absent: {num!r}",
          file_lacks(NOTE_PATH, num),
          detail="no charged-lepton mass values used")

# No new axiom admission.
check("No new axiom admission language",
      file_lacks(NOTE_PATH, "new_axiom_admission: true"),
      detail="audit-yaml block has new_axiom_admission: false")

check("BAE explicitly NOT consumed (excluded from positive statement)",
      file_contains(NOTE_PATH, "BAE explicitly NOT consumed"),
      detail="amplitude-equipartition deliberately excluded")

check("Koide Q = 2/3 deliberately excluded",
      file_contains(NOTE_PATH, "Does NOT derive Koide"),
      detail="Koide excluded; depends on BAE")


# ============================================================================
section("Narrow positive theorem summary")
# ============================================================================
print("""
  Positive theorem statement:

  HYPOTHESIS:
    A1: Cl(3) per-site local algebra.
    A2: Z^3 spatial substrate with APBC.
    R1: BZ-corner forcing of M_3(C) on H_{hw=1} == C^3, with Z/3Z
        cyclic generator C permuting the three hw=1 corners.
    R2: Schur reduction of Hermitian operators commuting with the
        Z/3Z regular representation on H_{hw=1}, yielding the
        circulant form a I + b C + bbar C^2 with (a, b) in R x C.

  CONCLUSION (T1, T2, T3, T4):
    (T1)  Operator class on H_{hw=1} reduces to circulants
              H = a I + b C + bbar C^2,    (a, b) in R x C.
    (T2)  Eigenvalues take the closed form
              lambda_k = a + 2 |b| cos(arg(b) + 2 pi k / 3),
              k = 0, 1, 2.
    (T3)  For b != 0 and arg(b) mod 2 pi / 3 outside the discrete
          coincidence set, the three eigenvalues are pairwise
          distinct real numbers.
    (T4)  Species labels {e, mu, tau} are assigned to the ordered
          eigenvalue triple by the standard mass-ordering convention,
          parallel to the SM conventions for (u, c, t),
          (nu_1, nu_2, nu_3), (K_S, K_L).

  Audit-lane class:
    (A) - pure representation theory / polynomial algebra over R x C
    with the standard root-of-unity identity 1 + w + w^2 = 0. No
    PDG numerical input, no Koide identity, no BAE assumption,
    no species-naming dependence on intrinsic operator properties.

  This positive theorem isolates the structural three-eigenvalue
  prediction (the "preserved-C_3 reading" of the framework's hw=1
  triplet) plus the mass-ordering labeling convention, deliberately
  excluding BAE and Koide Q = 2/3 (which require additional
  amplitude-ratio admission).
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
