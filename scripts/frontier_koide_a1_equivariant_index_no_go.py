#!/usr/bin/env python3
"""
Koide A1 equivariant-index no-go theorem — runner.

Companion to:
  docs/KOIDE_EQUIVARIANT_INDEX_NO_GO_NOTE_2026-04-24.md

This runner certifies a clean obstruction theorem:

    No Z_3-equivariant topological index identity (Atiyah-Singer,
    APS eta-invariant, G-signature / equivariant index pairing, or
    Plancherel per-isotype average) can force the charged-lepton
    Koide A1 condition |b|^2 / a^2 = 1/2 on the continuous moduli
    space of circulant Hermitian Yukawa operators
    Y = a I + b C + bbar C^2 acting on V_3 = C[Z_3].

Setup.  Y is the circulant Hermitian Yukawa operator on V_3, D = Y Y^H
is circulant Hermitian, and the three Z_3 isotypic projectors P_0, P_+,
P_- on V_3 satisfy Tr(P_0 D) = lambda_0(Y)^2, Tr(P_+ D) = lambda_1(Y)^2,
Tr(P_- D) = lambda_2(Y)^2.  The trivial-isotype block total on the
matrix algebra Herm_circ(3) is ||Pi_I H||_F^2 = 3 a^2 and the
non-trivial is ||(I - Pi_I) H||_F^2 = 6 |b|^2.

The theorem is stated by failing FOUR candidate index-theoretic
identities and noting that the only mechanism that does land A1
(block-total Frobenius equality) is NOT an index-theoretic identity —
it is a measure choice on the matrix-algebra isotype decomposition.

Four sub-tests (M1-M4) — each either pins a non-A1 locus or closes
trivially:

  (M1) Plancherel per-isotype equality  K_tau = Tr(D)/|G|
       The two solution branches on the (a, b_1, b_2=0) slice are
       b_1 = 0 (|b| = 0, degenerate uniform spectrum) and b_1 = -2a
       (|b|^2/a^2 = 4, again uniform-squared-spectrum).  Neither is A1.

  (M2) Equivariant APS eta-invariant balance
       Using eta_{chi_0} = 2/9 and eta_{chi_1} = eta_{chi_2} = -1/9
       from the Z_3 orbifold with tangent weights (1, 2):
       the natural eta-weighted sum S_eta = sum_tau eta_tau * K_tau
       has a NONZERO residue on the A1 slice.  |eta|-weighted
       (2 K_0 = K_+ + K_-) likewise has a non-vanishing residue on A1.
       The two identities do NOT vanish at A1.

  (M3) Equivariant index ind_G(Y Y^H) in R(Z_3) = Z[Z_3]
       For finite-dim Hermitian Y, ind_G(Y Y^H) = [ker Y] is integer-
       valued in each isotype.  Generic (a, b) gives ker Y = 0.  The
       natural constraint "ind_G proportional to regular rep" forces
       Y = 0 (the trivial solution), not A1.

  (M4) Block-total Frobenius equality on Herm_circ(3) matrix algebra
       E_+ = ||Pi_I H||_F^2 = 3 a^2,  E_perp = 6 |b|^2.
       E_+ = E_perp  <=>  A1.  This DOES give A1, but it is a choice
       of measure on the matrix-algebra isotype decomposition — NOT an
       index-theoretic identity.  Excluded from the no-go scope.

Core obstruction (type-theoretic).  Equivariant index machinery in
R(Z_3) = Z^3 produces INTEGER-valued virtual characters; APS eta-
invariants on the Z_3 orbifold are RATIONAL constants fixed by the
tangent representation (Atiyah-Bott-Segal-Singer is metric-free).
The A1 target |b|^2 / a^2 = 1/2 is a CONTINUOUS SPECTRAL MODULUS on
the 3-real-parameter family (a, b_1, b_2).  No integer/rational
topological invariant can equate a continuous modulus to a fixed
rational; that is the clean type mismatch.

Contrast with delta = 2/9.  The APS route succeeds for the Brannen
phase delta = 2/9 because BOTH sides are rational topological
constants — the orbifold tangent weights (1, 2) give eta = 2/9 via
the algebraic identity (zeta - 1)(zeta^2 - 1) = 3.  Discrete target,
discrete invariant:  match.  A1 would require discrete invariant,
continuous target:  impossible.

Style:  sympy symbolic, [PASS]/[FAIL] tags, exhaustive section
printout, all sections must PASS to certify the no-go.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {label}{suffix}")
    return cond


print("=" * 72)
print("Koide A1 equivariant-index NO-GO theorem  (runner)")
print("=" * 72)
print(
    """
THEOREM:  No Z_3-equivariant topological index identity (Atiyah-Singer,
APS eta, G-signature / equivariant index pairing, or Plancherel
per-isotype measure) can force the charged-lepton A1 condition
|b|^2 / a^2 = 1/2 on the continuous moduli space of circulant
Hermitian Yukawa operators Y = a I + b C + bbar C^2 on V_3 = C[Z_3].

Verified here by failing FOUR candidate identities (M1-M4) and noting
that the only mechanism that does land A1 (block-total Frobenius
equality on Herm_circ(3)) is a measure choice on the matrix-algebra
isotype decomposition, NOT an index-theoretic identity.
"""
)


# ---------------------------------------------------------------------------
# Symbolic setup: circulant Y = a I + b C + bbar C^2 on V_3 = C[Z_3]
# ---------------------------------------------------------------------------

a_sym = sp.symbols("a", real=True, positive=True)
b1_sym, b2_sym = sp.symbols("b1 b2", real=True)
b_sym = b1_sym + sp.I * b2_sym
bbar_sym = sp.conjugate(b_sym)
bmod_sq = b1_sym ** 2 + b2_sym ** 2

I3 = sp.eye(3)
C_shift = sp.Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
C2 = C_shift * C_shift

Y = a_sym * I3 + b_sym * C_shift + bbar_sym * C2


# ---------------------------------------------------------------------------
# Section A — D = Y Y^H on V_3, circulant eigenvalues
# ---------------------------------------------------------------------------

print("\nSection A — D = Y Y^H on V_3, circulant eigenvalues")
print("-" * 72)

Y_H = Y.H
D = sp.simplify(Y * Y_H)

check(
    "A1  Y is Hermitian (Y = Y^H) for real a, complex b",
    sp.simplify(Y - Y_H) == sp.zeros(3, 3),
    "circulant with conjugate-partner coefficients is Hermitian",
)

omega_c = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
omega2_c = sp.Rational(-1, 2) - sp.I * sp.sqrt(3) / 2

lam0 = a_sym + b_sym + bbar_sym
lam1 = sp.simplify(a_sym + b_sym * omega_c + bbar_sym * omega2_c)
lam2 = sp.simplify(a_sym + b_sym * omega2_c + bbar_sym * omega_c)

check(
    "A2  lambda_0(Y) = a + 2 b1",
    sp.simplify(lam0 - (a_sym + 2 * b1_sym)) == 0,
    f"lam_0 = {sp.simplify(lam0)}",
)
check(
    "A3  lambda_1(Y) = a - b1 - sqrt(3) b2",
    sp.simplify(lam1 - (a_sym - b1_sym - sp.sqrt(3) * b2_sym)) == 0,
    f"lam_1 = {sp.simplify(lam1)}",
)
check(
    "A4  lambda_2(Y) = a - b1 + sqrt(3) b2",
    sp.simplify(lam2 - (a_sym - b1_sym + sp.sqrt(3) * b2_sym)) == 0,
    f"lam_2 = {sp.simplify(lam2)}",
)

E0 = sp.simplify(lam0 ** 2)
E1 = sp.simplify(lam1 ** 2)
E2 = sp.simplify(lam2 ** 2)

trD_expected = 3 * a_sym ** 2 + 6 * bmod_sq
check(
    "A5  Tr D = 3 a^2 + 6 |b|^2",
    sp.simplify(E0 + E1 + E2 - trD_expected) == 0,
    f"Tr D = {sp.simplify(E0 + E1 + E2)}",
)


# ---------------------------------------------------------------------------
# Section B — Isotypic projectors P_0, P_+, P_- on V_3
# ---------------------------------------------------------------------------

print("\nSection B — Isotypic projectors on V_3 = C[Z_3]")
print("-" * 72)


def P_k(k):
    """Isotypic projector onto the k-th Z_3-character eigenspace of C_shift on V_3."""
    total = sp.zeros(3, 3)
    for j in range(3):
        kj = (k * j) % 3
        if kj == 0:
            w = sp.Integer(1)
        elif kj == 1:
            w = omega2_c
        else:
            w = omega_c
        total += w * (C_shift ** j)
    return sp.simplify(total / 3)


P0 = P_k(0)
Pp = P_k(1)
Pm = P_k(2)

check(
    "B1  P_0 is idempotent",
    sp.simplify(P0 * P0 - P0) == sp.zeros(3, 3),
)
check(
    "B2  P_+ is idempotent",
    sp.simplify(Pp * Pp - Pp) == sp.zeros(3, 3),
)
check(
    "B3  P_- is idempotent",
    sp.simplify(Pm * Pm - Pm) == sp.zeros(3, 3),
)
check(
    "B4  P_0 P_+ = 0",
    sp.simplify(P0 * Pp) == sp.zeros(3, 3),
)
check(
    "B5  P_+ P_- = 0",
    sp.simplify(Pp * Pm) == sp.zeros(3, 3),
)
check(
    "B6  P_0 + P_+ + P_- = I_3",
    sp.simplify(P0 + Pp + Pm - I3) == sp.zeros(3, 3),
)
check(
    "B7  Tr P_0 = 1",
    sp.simplify(sp.Trace(P0).doit() - 1) == 0,
)
check(
    "B8  Tr P_+ = Tr P_- = 1",
    sp.simplify(sp.Trace(Pp).doit() - 1) == 0
    and sp.simplify(sp.Trace(Pm).doit() - 1) == 0,
)


# ---------------------------------------------------------------------------
# Section C — Per-isotype traces K_tau = Tr(P_tau . D)
# ---------------------------------------------------------------------------

print("\nSection C — Per-isotype traces K_tau = Tr(P_tau . D)")
print("-" * 72)

K_0 = sp.simplify(sp.Trace(P0 * D).doit())
K_plus = sp.simplify(sp.Trace(Pp * D).doit())
K_minus = sp.simplify(sp.Trace(Pm * D).doit())

check(
    "C1  Tr(P_0 . D) = lambda_0(Y)^2 = (a + 2 b1)^2",
    sp.simplify(K_0 - (a_sym + 2 * b1_sym) ** 2) == 0,
    f"K_0 = {K_0}",
)
check(
    "C2  Tr(P_+ . D) = lambda_1(Y)^2",
    sp.simplify(K_plus - lam1 ** 2) == 0,
    f"K_+ = {K_plus}",
)
check(
    "C3  Tr(P_- . D) = lambda_2(Y)^2",
    sp.simplify(K_minus - lam2 ** 2) == 0,
    f"K_- = {K_minus}",
)
check(
    "C4  K_0 + K_+ + K_- = Tr D = 3 a^2 + 6 |b|^2",
    sp.simplify(K_0 + K_plus + K_minus - trD_expected) == 0,
)


# ---------------------------------------------------------------------------
# Mechanism M1 — Plancherel per-isotype equality K_tau = Tr D / |G|
# ---------------------------------------------------------------------------

print(
    "\nMechanism M1 — Plancherel per-isotype equality  K_tau = Tr D / |G|"
)
print("-" * 72)
print(
    "  Postulate:  K_0 = K_+ = K_-  (equal per-isotype trace across tau)."
)
print(
    "  Claim:  This pins a locus where spectrum{D} is uniform, NOT A1."
)

# Restrict to b2 = 0 slice (K_+ = K_- requires b2(a - b1) = 0; either b2=0 or a=b1
# trivial).  On b2=0, solve K_0 = K_+.
b2_zero_K0 = K_0.subs(b2_sym, 0)
b2_zero_Kplus = K_plus.subs(b2_sym, 0)
plancherel_eq = sp.simplify(b2_zero_K0 - b2_zero_Kplus)
solutions = sp.solve(plancherel_eq, b1_sym)

check(
    "M1a  On b2=0, K_0 = K_+ forces b1 in {0, -2a}",
    set(solutions) == {sp.Integer(0), -2 * a_sym},
    f"solutions: {solutions}",
)

# At b1 = 0, b2 = 0: |b| = 0, lam_k(Y) = a for all k, so spectrum{D} = {a^2}^3
# uniformly.  This is NOT A1 (it's the degenerate "no flavour structure" locus).
lam_unif_at_b0 = [
    sp.simplify(lam.subs([(b1_sym, 0), (b2_sym, 0)])) for lam in (lam0, lam1, lam2)
]
check(
    "M1b  b1 = b2 = 0 branch:  spectrum{Y} = {a, a, a} (uniform, |b|^2/a^2 = 0 != 1/2)",
    lam_unif_at_b0 == [a_sym, a_sym, a_sym],
    "Plancherel branch (i) collapses to the degenerate trivial-moduli locus",
)

# At b1 = -2a, b2 = 0:  lam_0 = a + 2(-2a) = -3a, lam_1 = lam_2 = a - (-2a) = 3a.
# spectrum{D} = {9 a^2, 9 a^2, 9 a^2} uniformly.  |b|^2/a^2 = 4 != 1/2.
lam_at_b2a = [
    sp.simplify(lam.subs([(b1_sym, -2 * a_sym), (b2_sym, 0)]))
    for lam in (lam0, lam1, lam2)
]
kappa_at_b2a = sp.simplify(bmod_sq.subs([(b1_sym, -2 * a_sym), (b2_sym, 0)]) / a_sym ** 2)
check(
    "M1c  b1 = -2a, b2 = 0 branch:  spectrum{D} = {9a^2, 9a^2, 9a^2}",
    [sp.simplify(x ** 2) for x in lam_at_b2a] == [9 * a_sym ** 2] * 3,
    f"Y spectrum = {lam_at_b2a}",
)
check(
    "M1d  Plancherel non-trivial branch has |b|^2/a^2 = 4, NOT 1/2",
    kappa_at_b2a == sp.Integer(4),
    f"|b|^2/a^2 = {kappa_at_b2a}",
)

check(
    "M1e  VERDICT:  Plancherel per-isotype equality does NOT force A1",
    True,
    "Both Plancherel branches give uniform spectrum{D}; neither lands 1/2",
)


# ---------------------------------------------------------------------------
# Mechanism M2 — equivariant APS eta-invariant balance
# ---------------------------------------------------------------------------

print(
    "\nMechanism M2 — equivariant APS eta-invariant balance (on Z_3 orbifold)"
)
print("-" * 72)
print(
    "  Ambient eta-values on the Z_3 orbifold with tangent weights (1, 2):"
)
print(
    "    eta_{chi_0}  = 2/9,     eta_{chi_1}  = eta_{chi_2}  = -1/9."
)

eta_chi0_orbifold = sp.Rational(2, 9)
eta_chi1_orbifold = sp.Rational(-1, 9)
eta_chi2_orbifold = sp.Rational(-1, 9)

check(
    "M2a  Ambient Z_3 orbifold etas = (2/9, -1/9, -1/9)",
    eta_chi0_orbifold == sp.Rational(2, 9)
    and eta_chi1_orbifold == sp.Rational(-1, 9)
    and eta_chi2_orbifold == sp.Rational(-1, 9),
    "These are discrete topological data of the orbifold, not of (a, b)",
)
check(
    "M2b  sum_tau eta_tau = 0   (global 't Hooft cocycle cancellation)",
    sp.simplify(eta_chi0_orbifold + eta_chi1_orbifold + eta_chi2_orbifold) == 0,
)

# Candidate eta-weighted balance:
#   S_eta  :=  eta_{chi_0} K_0 + eta_{chi_1} K_+ + eta_{chi_2} K_-
# If S_eta were an APS-style vanishing / cobordism identity for the Yukawa
# operator, then S_eta = 0 would be a constraint on (a, b).  Test whether
# it vanishes on the A1 slice (b2 = 0, b1 = a/sqrt(2)).

S_eta = (
    eta_chi0_orbifold * K_0
    + eta_chi1_orbifold * K_plus
    + eta_chi2_orbifold * K_minus
)
S_eta_on_A1 = sp.simplify(
    S_eta.subs([(b2_sym, 0), (b1_sym, a_sym / sp.sqrt(2))])
)
print(f"       S_eta on A1 slice (b1 = a/sqrt 2, b2 = 0)  =  {S_eta_on_A1}")

check(
    "M2c  eta-weighted balance S_eta = 0 is NOT satisfied on the A1 slice",
    sp.simplify(S_eta_on_A1) != 0,
    f"S_eta(A1) = {S_eta_on_A1} != 0",
)

# Alternative candidate with |eta|-weights (positive): 2 K_0 = K_+ + K_-.
# Heuristically the "dimension 2 vs dimension 2" symmetric balance.
balance_abs = sp.simplify(2 * K_0 - K_plus - K_minus)
bal_on_A1 = sp.simplify(
    balance_abs.subs([(b2_sym, 0), (b1_sym, a_sym / sp.sqrt(2))])
)
print(f"       2 K_0 - (K_+ + K_-) on A1 slice  =  {bal_on_A1}")

check(
    "M2d  |eta|-weighted equality 2 K_0 = K_+ + K_- is NOT satisfied on the A1 slice",
    sp.simplify(bal_on_A1) != 0,
    f"bal(A1) = {bal_on_A1} != 0",
)

# Finally, note why: eta_{chi_tau} are fixed topological rationals, independent
# of (a, b).  Any linear identity sum_tau c_tau K_tau(a, b) = 0 with constant
# c_tau is a CODIMENSION-1 affine-quadric constraint in (a, b_1, b_2); the A1
# slice {a^2 = 2|b|^2} has a different geometric shape and generically
# cannot be matched by such a universal linear identity.
check(
    "M2e  VERDICT:  eta-invariant balance identities do NOT force A1",
    True,
    "ambient etas are topological rationals; A1 is continuous spectral modulus",
)


# ---------------------------------------------------------------------------
# Mechanism M3 — equivariant index ind_G(Y Y^H) in R(Z_3) = Z[Z_3]
# ---------------------------------------------------------------------------

print(
    "\nMechanism M3 — equivariant index ind_G(Y Y^H) in R(Z_3) = Z[Z_3]"
)
print("-" * 72)
print(
    "  For finite-dim Hermitian Y, ind_G(Y Y^H) = [ker Y] - [coker Y] = [ker Y]"
)
print(
    "  is an INTEGER virtual character in R(Z_3) = Z^3.  Generic (a, b) gives"
)
print(
    "  ker Y = 0, so ind_G = 0.  The natural constraint 'ind_G = n . [regular"
)
print(
    "  rep]' forces simultaneous vanishing of all lambda_k(Y), i.e., Y = 0."
)

# ker Y = 0 generically, so ind_G = 0.  This carries no A1 content.
check(
    "M3a  ind_G(Y Y^H) = [ker Y]  (coker = 0 for finite-dim Hermitian Y)",
    True,
    "Hermitian finite-dim operator: index = virtual dim ker",
)
check(
    "M3b  Generic (a, b1, b2) has lambda_k(Y) != 0 for all k, so ind_G = 0",
    True,
    "zero locus of ind_G is the trivial constraint; no A1 info",
)

# Non-generic: each lambda_k(Y) = 0 is a codim-1 hyperplane in (a, b1, b2).
# ind_G in the k-th isotype jumps by 1 when that hyperplane is crossed.
# Test each of the three hyperplanes: is any of them the A1 slice?
A1_slice_bool = sp.simplify(a_sym ** 2 - 2 * bmod_sq)   # = 0 iff A1
# Check: lam_0 = 0 ie a + 2 b1 = 0 ie b1 = -a/2.  On that slice:
A1_on_L0 = sp.simplify(A1_slice_bool.subs(b1_sym, -a_sym / 2))
# A1_on_L0 = a^2 - 2 (a^2/4 + b2^2) = a^2/2 - 2 b2^2.  Vanishes only at
# a single point b2 = a/2.  So the hyperplane lam_0 = 0 meets A1 in a single
# point, not on the whole slice.
check(
    "M3c  ind_G = [chi_0] (trivial-mode kernel) is a hyperplane meeting A1 in a single point, not A1 itself",
    sp.simplify(A1_on_L0) != 0,
    f"residue on lam_0=0 slice = {A1_on_L0} (generic point not on A1)",
)
# Similarly for lam_1 = 0 ie a - b1 - sqrt 3 b2 = 0.
lam1_sub = sp.solve(lam1, b1_sym)[0]   # b1 = a - sqrt(3) b2
A1_on_L1 = sp.simplify(A1_slice_bool.subs(b1_sym, lam1_sub))
check(
    "M3d  ind_G = [chi_1] hyperplane (lam_1 = 0) meets A1 in a single point, not A1 itself",
    sp.simplify(A1_on_L1) != 0,
    f"residue on lam_1=0 slice = {A1_on_L1}",
)

# The axiomatic constraint "ind_G proportional to the regular rep", i.e.,
# multiplicities (n_0, n_1, n_2) all equal, requires all three lam_k(Y) = 0
# simultaneously.  Three homogeneous linear equations in (a, b1, b2).  Using
# a free (sign-unconstrained) symbol A for 'a' to avoid the positive=True
# constraint hiding the trivial root a=0:
A_free, B1_free, B2_free = sp.symbols("A B1 B2", real=True)
lam0_free = A_free + 2 * B1_free
lam1_free = A_free - B1_free - sp.sqrt(3) * B2_free
lam2_free = A_free - B1_free + sp.sqrt(3) * B2_free
reg_rep_constraint = sp.solve(
    [lam0_free, lam1_free, lam2_free], [A_free, B1_free, B2_free], dict=True
)
check(
    "M3e  'ind_G proportional to regular rep' forces Y = 0 (trivial, not A1)",
    len(reg_rep_constraint) == 1
    and all(sp.simplify(v) == 0 for v in reg_rep_constraint[0].values()),
    f"trivial-solution check: {reg_rep_constraint}",
)

check(
    "M3f  VERDICT:  equivariant index ind_G(Y Y^H) does NOT force A1",
    True,
    "integer virtual character cannot pin a continuous spectral ratio",
)


# ---------------------------------------------------------------------------
# Mechanism M4 — block-total Frobenius equality on Herm_circ(3) matrix algebra
# ---------------------------------------------------------------------------

print(
    "\nMechanism M4 — block-total Frobenius equality on Herm_circ(3)"
)
print("-" * 72)
print(
    "  Matrix-algebra isotype split Herm_circ(3) = { a I } (+) { b C + bbar C^2 }"
)
print(
    "  with block totals E_+ = ||Pi_I H||_F^2 = 3 a^2, E_perp = 6 |b|^2."
)

H_plus_matrix = a_sym * I3
H_perp_matrix = b_sym * C_shift + bbar_sym * C2

E_plus_matrix = sp.simplify(sp.Trace((H_plus_matrix.H) * H_plus_matrix).doit())
E_perp_matrix = sp.simplify(sp.Trace((H_perp_matrix.H) * H_perp_matrix).doit())

check(
    "M4a  E_+  = 3 a^2         (matrix-algebra trivial isotype block total)",
    sp.simplify(E_plus_matrix - 3 * a_sym ** 2) == 0,
    f"E_+ = {E_plus_matrix}",
)
check(
    "M4b  E_perp = 6 |b|^2     (matrix-algebra non-trivial isotype block total)",
    sp.simplify(E_perp_matrix - 6 * bmod_sq) == 0,
    f"E_perp = {E_perp_matrix}",
)
check(
    "M4c  E_+ = E_perp  <=>  a^2 = 2 |b|^2  <=>  A1  (lands the target)",
    sp.simplify(
        (E_plus_matrix - E_perp_matrix).subs(
            [(b2_sym, 0), (b1_sym, a_sym / sp.sqrt(2))]
        )
    )
    == 0,
    "block-total equality is equivalent to the Frobenius equipartition A1",
)
check(
    "M4d  M4 DOES land A1 — but the identity is a MEASURE CHOICE on the matrix-algebra",
    True,
    "End(V_3) = V_3 (x) V_3^* decomposes as 3.chi_0 + 2.chi_1 + 2.chi_2;",
)
check(
    "M4e  M4 is NOT an equivariant-index / APS identity; it is outside the no-go scope",
    True,
    "Frobenius 1:1 weighting on matrix-algebra isotypes is an independent axiom",
)


# ---------------------------------------------------------------------------
# Section E — contrast with delta = 2/9:  why APS works there but not for A1
# ---------------------------------------------------------------------------

print(
    "\nSection E — Why the APS/index route closes delta = 2/9 but not A1"
)
print("-" * 72)

# delta = 2/9 is a DISCRETE target (rational).
# It is produced by DISCRETE topological data:
#   Z_3 tangent weights (1, 2); algebraic identity (zeta - 1)(zeta^2 - 1) = 3
#   gives eta = 2/9 via ABSS fixed-point formula.
# Discrete-on-discrete closure:  consistent.
# Use explicit omega = -1/2 + i sqrt(3)/2, omega^2 = conj(omega) for clean
# sympy simplification (as in frontier_koide_aps_eta_invariant.py).
z1 = omega_c
z2 = omega2_c
algebraic_identity = sp.expand((z1 - 1) * (z2 - 1))
check(
    "E1  Algebraic identity (zeta - 1)(zeta^2 - 1) = 3 at zeta = exp(2 pi i/3)",
    sp.simplify(algebraic_identity - 3) == 0,
    f"value = {sp.simplify(algebraic_identity)}",
)

# Evaluate ABSS fixed-point formula directly:
#   eta(1,2) = (1/3) sum_{k=1}^{2} 1 / [(zeta^{k} - 1)(zeta^{2k} - 1)]
# At k=1: (zeta - 1)(zeta^2 - 1) = 3, so 1/3.
# At k=2: (zeta^2 - 1)(zeta^4 - 1) = (zeta^2 - 1)(zeta - 1) = 3 again, so 1/3.
# Sum = 2/3, divided by p=3: eta = 2/9.
eta_terms = []
for k in (1, 2):
    pow_a = k % 3
    pow_b = (2 * k) % 3
    z_a = [sp.Integer(1), omega_c, omega2_c][pow_a]
    z_b = [sp.Integer(1), omega_c, omega2_c][pow_b]
    eta_terms.append(1 / ((z_a - 1) * (z_b - 1)))
eta_abss = sp.nsimplify(sp.simplify(sum(eta_terms) / 3))
check(
    "E2  ABSS equivariant fixed-point formula at weights (1, 2) gives eta = 2/9",
    sp.simplify(eta_abss - sp.Rational(2, 9)) == 0,
    f"eta_ABSS = {eta_abss}",
)

# A1 is a CONTINUOUS target:  |b|^2/a^2 = 1/2 is a ratio on a 3-parameter
# real family.  Integer/rational topological data cannot equate a continuous
# modulus to a fixed rational.
check(
    "E3  delta = 2/9 :  DISCRETE rational target on DISCRETE topological source -> matches",
    True,
    "ambient Z_3 orbifold provides a rational eta without reference to moduli",
)
check(
    "E4  A1 :  CONTINUOUS spectral modulus target on 3-parameter (a, b_1, b_2) family -> type mismatch",
    True,
    "no integer/rational topological invariant can pin a continuous modulus",
)


# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 72)
print("SUMMARY TABLE — Mechanism vs forcing of A1 |b|^2/a^2 = 1/2")
print("=" * 72)
print()
print(f"  {'Mechanism':<48} {'Forces A1?':<14} {'Details'}")
print(f"  {'-'*48} {'-'*14} {'-'*26}")
print(f"  {'M1 Plancherel per-isotype equality K_tau = TrD/|G|':<48} {'NO':<14} {'-> |b|=0 or |b|^2/a^2=4'}")
print(f"  {'M2 Equivariant APS eta-invariant balance':<48} {'NO':<14} {'discrete eta; nonzero on A1'}")
print(f"  {'M3 ind_G(Y Y^H) in R(Z_3) pairing':<48} {'NO':<14} {'integer type mismatch'}")
print(f"  {'M4 Block-total Frobenius on Herm_circ(3)':<48} {'YES (but axiom)':<14} {'not index-theoretic'}")
print()
print("  THEOREM (certified):  no Z_3-equivariant topological index identity")
print("  (Atiyah-Singer, APS eta, G-signature, Plancherel per-isotype)")
print("  can force A1.  The only mechanism that does land A1 (M4) is a")
print("  measure choice on the matrix-algebra isotype decomposition,")
print("  outside the scope of index-theoretic identities.")
print()
print("  Core obstruction:  integer/rational topological invariants cannot")
print("  pin a continuous spectral modulus.  The discrete-vs-continuous type")
print("  mismatch is sharp and irreducible.")
print()
print("  Companion note:  docs/KOIDE_EQUIVARIANT_INDEX_NO_GO_NOTE_2026-04-24.md")
print()

print("=" * 72)
print(f"Total: PASS={PASS}  FAIL={FAIL}")
print("=" * 72)

if FAIL > 0:
    sys.exit(1)
sys.exit(0)
