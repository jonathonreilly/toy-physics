#!/usr/bin/env python3
"""Pattern A narrow runner for
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies, on abstract symbols (a in R, b in C), the standalone Hermitian-matrix
algebraic identities on Herm_circ(3) underlying the parent
`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19` row:

  (T1) the canonical real-isotype projectors pi_+, pi_perp on
       H = a I + b C + bbar C^2 decompose H orthogonally with real-image
       dimensions (1, 2);
  (T2) E_+(H) := || pi_+(H) ||_F^2 = 3 a^2;
       E_perp(H) := || pi_perp(H) ||_F^2 = 6 |b|^2;
  (T3) the equal-weight log-functional S = log E_+ + log E_perp, under the
       constraint E_+ + E_perp = E_tot > 0, has unique interior critical
       point E_+ = E_perp = E_tot / 2, equivalently a^2 = 2 |b|^2,
       i.e. kappa = 2; Hessian is strictly negative-definite there;
  (T4) the real-irrep multiplicity pattern (trivial, doublets, sign) = (1, (1,), 0)
       on Herm_circ(d) is uniquely realized at d = 3 among d in {2, 3, 4, 5, 6}.

This narrow theorem treats (a, b) as ABSTRACT SYMBOLS. It does not select
between weight choices (e.g. multiplicity (1, 1) vs real-dim (1, 2)),
does not consume any selection-principle authority for the canonical
log-functional, and does not consume any PDG / literature / Wilson /
spectrum-side Koide / Berry / Brannen authority.

The narrow theorem can be applied to ANY Hermitian circulant
parametrized by (a, b); the framework-specific charged-lepton
identification with PDG masses is NOT load-bearing here.

Companion role: not a new audit-companion; this is a Pattern A new
narrow claim row carving out the algebraic core of the existing
`koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19`
(claim_type=positive_theorem, load_bearing_step_class=A).
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import (
        Rational, sqrt, simplify, symbols, expand,
        I, conjugate, Matrix, eye, zeros, trace, log, diff,
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
section("Pattern A narrow theorem: block-total Frobenius algebraic identities on Herm_circ(3)")
# ============================================================================

# Symbolic ingredients: a in R, b = x + i y in C with real x, y.
a, x, y = symbols("a x y", real=True)
b = x + I * y
bbar = conjugate(b)

# 3x3 cyclic permutation C with C[i, (i+1) mod 3] = 1.
C = Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
I3 = eye(3)
C2 = simplify(C * C)
C3 = simplify(C * C * C)

# Sanity: C^3 = I and trace(C) = trace(C^2) = 0.
check("C^3 = I (cyclic permutation cubes to identity)",
      C3 == I3, detail="explicit matrix product")
check("tr(C) = 0", trace(C) == 0, detail=f"tr(C) = {trace(C)}")
check("tr(C^2) = 0", trace(C2) == 0, detail=f"tr(C^2) = {trace(C2)}")

# Hermitian circulant H = a I + b C + bbar C^2.
H = a * I3 + b * C + bbar * C2


# ----------------------------------------------------------------------------
section("Part 1 (T1): orthogonal-projector decomposition and image dimensions")
# ----------------------------------------------------------------------------

# Define pi_+ and pi_perp on the H above.
tr_H = simplify(trace(H))
check("tr(H) = 3 a on Herm_circ(3)",
      simplify(tr_H - 3 * a) == 0, detail=f"tr(H) = {tr_H}")

pi_plus_H = (tr_H / 3) * I3  # = a I
pi_perp_H = simplify(H - pi_plus_H)
check("pi_+(H) = a I on Herm_circ(3) instance",
      simplify(pi_plus_H - a * I3) == zeros(3, 3),
      detail=f"pi_+(H) - a I = {simplify(pi_plus_H - a * I3)}")
check("pi_perp(H) = b C + bbar C^2 on Herm_circ(3) instance",
      simplify(pi_perp_H - (b * C + bbar * C2)) == zeros(3, 3),
      detail=f"pi_perp(H) - (b C + bbar C^2) = {simplify(pi_perp_H - (b * C + bbar * C2))}")

# Idempotency: pi_+ applied twice to H equals pi_+(H).
# Treat pi_+ as the operator X -> (tr(X)/3) I.
def pi_plus(X):
    return (trace(X) / 3) * I3

def pi_perp_op(X):
    return X - pi_plus(X)

pi_plus_pi_plus_H = simplify(pi_plus(pi_plus_H))
check("pi_+(pi_+(H)) = pi_+(H) (idempotent)",
      simplify(pi_plus_pi_plus_H - pi_plus_H) == zeros(3, 3),
      detail="idempotency")

pi_plus_pi_perp_H = simplify(pi_plus(pi_perp_H))
check("pi_+(pi_perp(H)) = 0 (orthogonal projectors)",
      pi_plus_pi_perp_H == zeros(3, 3),
      detail=f"pi_+(pi_perp(H)) = {pi_plus_pi_perp_H}")

# Hermiticity: pi_+(H) is its own conjugate-transpose; same for pi_perp(H).
pi_plus_H_H = pi_plus_H.H  # conjugate transpose
check("pi_+(H) is Hermitian",
      simplify(pi_plus_H_H - pi_plus_H) == zeros(3, 3),
      detail="(a I)^H = a I since a is real")

pi_perp_H_H = simplify(pi_perp_H.H)
check("pi_perp(H) is Hermitian",
      simplify(pi_perp_H_H - pi_perp_H) == zeros(3, 3),
      detail="(b C + bbar C^2)^H = b C + bbar C^2 since C^H = C^2")

# Frobenius orthogonality: <pi_+(H), pi_perp(H)>_F = tr(pi_+(H)^H pi_perp(H)) = 0.
inner_pp = simplify(trace(pi_plus_H.H * pi_perp_H))
check("Frobenius orthogonality: <pi_+(H), pi_perp(H)>_F = 0",
      simplify(inner_pp) == 0,
      detail=f"<pi_+(H), pi_perp(H)>_F = {inner_pp}")

# Sum: pi_+ + pi_perp = identity (on H).
sum_proj_H = simplify(pi_plus_H + pi_perp_H)
check("pi_+(H) + pi_perp(H) = H (decomposition completeness)",
      simplify(sum_proj_H - H) == zeros(3, 3),
      detail="completeness on the 3-parameter (a, b) family")

# Real image dimensions: image(pi_+) is the real-1-dim span of I; image(pi_perp)
# is the real-2-dim span of {C + C^2, i(C - C^2)} -- equivalently, of the
# real and imaginary parts of b in the parametrization H = a I + b C + bbar C^2.
# Doublet-isotype Hermitian basis on Herm_circ(3): {B_1, B_2} with
#   B_1 := C + C^2  (real symmetric, all-real entries),
#   B_2 := i (C - C^2) (Hermitian with pure-imaginary off-diagonals; Hermitian
#                       since (i (C - C^2))^H = -i (C^H - (C^2)^H)
#                                              = -i (C^2 - C) = i (C - C^2)).
# Both lie in Herm_circ(3); pi_perp(H) = (Re b) B_1 + (Im b) B_2 for H = aI + bC + bbar C^2.
B1 = simplify(C + C2)
B2 = simplify(I * (C - C2))
# Sanity: B_1 is Hermitian, B_2 is Hermitian.
check("B_1 := C + C^2 is Hermitian (real symmetric)",
      simplify(B1.H - B1) == zeros(3, 3),
      detail="all-real-entry symmetric matrix")
check("B_2 := i(C - C^2) is Hermitian (pure-imaginary off-diagonals)",
      simplify(B2.H - B2) == zeros(3, 3),
      detail="B_2^H = -i (C^2 - C) = i (C - C^2) = B_2")

# Decomposition: pi_perp(H) = (Re b) B_1 + (Im b) B_2.
re_b, im_b = symbols("re_b im_b", real=True)
b_real_param = re_b + I * im_b
pi_perp_in_B = simplify(re_b * B1 + im_b * B2)
H_with_param = a * I3 + b_real_param * C + conjugate(b_real_param) * C2
pi_perp_via_param = simplify(H_with_param - (trace(H_with_param) / 3) * I3)
check("pi_perp(H) = (Re b) B_1 + (Im b) B_2 (Hermitian-basis expansion)",
      simplify(pi_perp_via_param - pi_perp_in_B) == zeros(3, 3),
      detail="Hermitian-basis expansion with (Re b, Im b) real coordinates")

# Image dimensions: rank of the real 3 x 9 matrix [vec(I) ; vec(B_1) ; vec(B_2)].
# In the algebraic narrow runner we verify (i) image(pi_+) has real dim 1
# because pi_+(H) ranges over R*I as a varies, and (ii) image(pi_perp) has real
# dim 2 because pi_perp(H) ranges over R*B_1 + R*B_2 as (Re b, Im b) vary.
# Sympy linear independence over R:
flat_I = Matrix([I3.row(0).tolist()[0] + I3.row(1).tolist()[0] + I3.row(2).tolist()[0]])
flat_B1 = Matrix([B1.row(0).tolist()[0] + B1.row(1).tolist()[0] + B1.row(2).tolist()[0]])
# Pull i out of B_2 to give a flat real basis vector: B_2 = i * (C^2 - C),
# so the real coordinate is (Im b) and the basis vector is i * flat(C^2 - C).
# For rank-over-R purposes we record the basis-element flat(C^2 - C) times i,
# but linear independence of {I, B_1, B_2} over R only requires that no real
# linear combination of the three vanishes -- equivalent to linear independence
# of the real-coordinate parametrization (a, Re b, Im b), which is automatic
# since they are independent symbols in the H = a I + b C + bbar C^2 expansion.
flat_B2 = Matrix([B2.row(0).tolist()[0] + B2.row(1).tolist()[0] + B2.row(2).tolist()[0]])

# Sanity for image(pi_+): rank of {I} = 1.
M_plus = Matrix.vstack(flat_I)
check("rank of image(pi_+) generators = 1 (single trivial-isotype slot, real dim 1)",
      M_plus.rank() == 1, detail="image(pi_+) = R * I")

# Sanity for image(pi_perp): rank of {B_1, B_2} = 2.
M_perp = Matrix.vstack(flat_B1, flat_B2)
check("rank of image(pi_perp) generators = 2 (doublet isotype, real dim 2)",
      M_perp.rank() == 2, detail="image(pi_perp) = R B_1 + R B_2")

# Joint sanity: {I, B_1, B_2} linearly independent (image(pi_+) + image(pi_perp) is 3-dim real).
M_full = Matrix.vstack(flat_I, flat_B1, flat_B2)
check("{I, B_1, B_2} linearly independent over R (image(pi_+) + image(pi_perp) = real dim 3)",
      M_full.rank() == 3, detail="orthogonal direct sum is real dim 1 + 2 = 3")


# ----------------------------------------------------------------------------
section("Part 2 (T2): block-total Frobenius identities E_+ = 3 a^2, E_perp = 6 |b|^2")
# ----------------------------------------------------------------------------

# E_+(H) = || pi_+(H) ||_F^2 = tr((a I)^H (a I)) = a^2 tr(I) = 3 a^2.
E_plus_def = simplify(trace(pi_plus_H.H * pi_plus_H))
E_plus_expected = 3 * a**2
check("E_+(H) = tr((a I)^H (a I)) = 3 a^2 (exact symbolic)",
      simplify(E_plus_def - E_plus_expected) == 0,
      detail=f"E_+(H) = {E_plus_def}")

# E_perp(H) = || pi_perp(H) ||_F^2 = tr((b C + bbar C^2)^H (b C + bbar C^2)) = 6 |b|^2.
E_perp_def = simplify(trace(pi_perp_H.H * pi_perp_H))
# Expected in (x, y) coords: 6 (x^2 + y^2).
E_perp_expected = 6 * (x**2 + y**2)
check("E_perp(H) = 6 |b|^2 (exact symbolic, in (x, y) coords)",
      simplify(E_perp_def - E_perp_expected) == 0,
      detail=f"E_perp(H) = {E_perp_def}")

# Same statement in (b, bbar) coords.
abs_b_sq = simplify(b * bbar)
check("|b|^2 = x^2 + y^2 (real / imag decomposition consistency)",
      simplify(abs_b_sq - (x**2 + y**2)) == 0, detail=f"|b|^2 = {abs_b_sq}")


# ----------------------------------------------------------------------------
section("Part 3 (T3): equal-weight Lagrange extremum -> kappa = 2")
# ----------------------------------------------------------------------------

# Treat E_+, E_perp as positive reals; constraint E_+ + E_perp = E_tot.
Ep, Epp, mu, E_tot = symbols("Ep Epp mu E_tot", positive=True, real=True)
S = log(Ep) + log(Epp)
L = S - mu * (Ep + Epp - E_tot)

# Stationary equations: dL/dEp = 0 and dL/dEpp = 0.
dL_dEp = simplify(diff(L, Ep))
dL_dEpp = simplify(diff(L, Epp))
# Solve 1/Ep = mu and 1/Epp = mu, with Ep + Epp = E_tot.
sol = sympy.solve([dL_dEp, dL_dEpp, Ep + Epp - E_tot], [Ep, Epp, mu], dict=True)

# We expect a unique positive solution with Ep = Epp = E_tot / 2 and mu = 2 / E_tot.
expected = {Ep: E_tot / 2, Epp: E_tot / 2, mu: 2 / E_tot}
match = any(all(simplify(s.get(k) - v) == 0 for k, v in expected.items()) for s in sol)
check("Lagrange critical point: E_+ = E_perp = E_tot / 2 (unique on positive orthant)",
      match, detail=f"sol = {sol}")

# Substituting into (T2): 3 a^2 = 6 |b|^2 ==> a^2 = 2 |b|^2 ==> kappa = 2.
# Set E_+ = 3 a^2 and E_perp = 6 |b|^2; demand them equal.
kappa_extremum_eq = simplify(3 * a**2 - 6 * (x**2 + y**2))  # = 0 at extremum
# This is equivalent to a^2 = 2 (x^2 + y^2). With kappa = a^2 / |b|^2:
# At the extremum, kappa = a^2 / (x^2 + y^2) = 2.
# Symbolic identity: solve a^2 - 2 (x^2 + y^2) = 0 for kappa.
# We verify the identity "E_+ = E_perp <=> a^2 = 2 |b|^2" directly.
lhs_iff = simplify(E_plus_def - E_perp_def)  # = 3 a^2 - 6 (x^2 + y^2)
rhs_iff = 3 * (a**2 - 2 * (x**2 + y**2))
check("E_+ = E_perp  <=>  a^2 = 2 |b|^2  (algebraic equivalence)",
      simplify(lhs_iff - rhs_iff) == 0,
      detail=f"E_+ - E_perp = 3 (a^2 - 2 |b|^2) = {simplify(lhs_iff)}")

# Hessian: d^2 S / dEp^2 = -1/Ep^2, d^2 S / dEpp^2 = -1/Epp^2.
# At Ep = Epp = E_tot/2, both equal -4/E_tot^2 < 0.
H_pp = simplify(diff(S, Ep, 2))
H_qq = simplify(diff(S, Epp, 2))
H_pq = simplify(diff(diff(S, Ep), Epp))
H_pp_at = simplify(H_pp.subs(Ep, E_tot / 2))
H_qq_at = simplify(H_qq.subs(Epp, E_tot / 2))
check("d^2 S / dE_+^2 at critical point = -4 / E_tot^2 < 0",
      simplify(H_pp_at - (-4 / E_tot**2)) == 0,
      detail=f"d^2 S / dE_+^2 = {H_pp_at}")
check("d^2 S / dE_perp^2 at critical point = -4 / E_tot^2 < 0",
      simplify(H_qq_at - (-4 / E_tot**2)) == 0,
      detail=f"d^2 S / dE_perp^2 = {H_qq_at}")
check("cross-partial d^2 S / dE_+ dE_perp = 0",
      simplify(H_pq) == 0, detail=f"cross-partial = {H_pq}")


# ----------------------------------------------------------------------------
section("Part 4 (T4): d = 3 uniqueness of the (1, (1,), 0) multiplicity pattern")
# ----------------------------------------------------------------------------

# For each d in {2, 3, 4, 5, 6}, count:
#   trivial (k = 0): always 1.
#   doublets (conjugate pair {k, d - k} with k != d - k mod d): floor((d - 1) / 2).
#   sign (k = d/2 when d even): 1 if d even else 0.
def multiplicity_pattern(d):
    trivial = 1
    n_doublets = (d - 1) // 2
    sign = 1 if d % 2 == 0 else 0
    return (trivial, tuple([1] * n_doublets), sign)

expected_patterns = {
    2: (1, (), 1),
    3: (1, (1,), 0),
    4: (1, (1,), 1),
    5: (1, (1, 1), 0),
    6: (1, (1, 1), 1),
}

for d in (2, 3, 4, 5, 6):
    got = multiplicity_pattern(d)
    exp = expected_patterns[d]
    check(f"Herm_circ(d={d}) multiplicity pattern = {exp}",
          got == exp, detail=f"got {got}")

# d = 3 uniqueness: which d in {2, ..., 6} have pattern (1, (1,), 0)?
unique_d = [d for d in (2, 3, 4, 5, 6) if multiplicity_pattern(d) == (1, (1,), 0)]
check("d = 3 is the unique d in {2, 3, 4, 5, 6} with pattern (1, (1,), 0)",
      unique_d == [3], detail=f"d's with pattern (1, (1,), 0): {unique_d}")


# ----------------------------------------------------------------------------
section("Part 5: parent / sibling row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
try:
    ledger = json.loads(LEDGER.read_text())
    parent = ledger['rows'].get(
        'koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19', {})
    sibling = ledger['rows'].get(
        'koide_circulant_character_bridge_narrow_theorem_note_2026-05-09', {})
    print(f"\n  Parent row state on origin/main:")
    print(f"    effective_status: {parent.get('effective_status')}")
    print(f"    claim_type:       {parent.get('claim_type')}")
    print(f"  Sister narrow row state on origin/main:")
    print(f"    effective_status: {sibling.get('effective_status')}")
    print(f"    claim_type:       {sibling.get('claim_type')}")

    check("parent row is unaudited (this narrow theorem is a rescope, not a promotion)",
          parent.get('effective_status') == 'unaudited',
          detail=f"effective_status = {parent.get('effective_status')}")
except Exception as e:
    check(f"parent-row ledger read (defensive)", False, detail=str(e))


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESES:
    Let (a, b) in R x C be abstract symbols. Let C be the 3 x 3 cyclic
    permutation matrix. Define H = a I + b C + bbar C^2, and the canonical
    real-isotype projectors
        pi_+(H)    = (tr H / 3) I,
        pi_perp(H) = H - pi_+(H).
    Define block totals E_+(H) := || pi_+(H) ||_F^2 and
    E_perp(H) := || pi_perp(H) ||_F^2.

  CONCLUSIONS:
    (T1)  pi_+, pi_perp are orthogonal Hermitian projectors; image(pi_+)
          and image(pi_perp) have real dimensions 1 and 2 respectively.
    (T2)  E_+(H) = 3 a^2; E_perp(H) = 6 |b|^2.
    (T3)  S = log E_+ + log E_perp at fixed E_+ + E_perp = E_tot is
          extremized uniquely at E_+ = E_perp = E_tot / 2, i.e. a^2 = 2 |b|^2
          (kappa = 2); Hessian is strictly negative-definite there.
    (T4)  The real-irrep multiplicity pattern (trivial, doublets, sign)
          = (1, (1,), 0) on Herm_circ(d) is uniquely realized at d = 3
          among d in {2, 3, 4, 5, 6}.

  Audit-lane class:
    (A) - pure linear algebra and elementary cyclic-group representation
    theory. No PDG observed values, no literature numerical comparator,
    no fitted selectors, no admitted unit conventions, no F1-vs-F3
    selection-principle authority.

  This narrow theorem isolates the algebraic identities of the parent
  KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19 from
  its companion (i) selection claim that the multiplicity weighting
  (1, 1) is the canonical extremal principle, and (ii) two-route closure
  positioning. The F1-vs-F3 weighting question is recorded as an Open
  derivation gap, with the 30-probe BAE campaign as the live
  characterization.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
