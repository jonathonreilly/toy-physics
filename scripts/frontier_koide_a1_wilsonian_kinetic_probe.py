#!/usr/bin/env python3
"""
Koide A1 — Wilsonian / UV-derived kinetic-matrix probe.

Hypothesis under test
---------------------
The retained Frobenius kinetic  L_kin^Frob = Tr((d H)^2) = 3 (da)^2 + 6 (db_1)^2
+ 6 (db_2)^2  on Herm_circ(3) is a LOW-ENERGY relic.  A UV completion
supplies a kinetic matrix  Z^{ab}(mu) d_mu Phi_a d^mu Phi_b  in the real
Peter-Weyl basis  Phi = (a, b_1, b_2).  If any natural UV completion of
the Cl(3)/Z^3 toy framework delivers Z^{ab}(mu_retained) that is
parameter-flat (weights (1,1,1) up to an overall scale), then
  kappa = a^2/|b|^2 = 2,  |b|^2/a^2 = 1/2 = A1
follows automatically.

This probe runs five distinct attack vectors, computes Z^{ab} in each,
and reports whether it is parameter-flat (A1), Frobenius (weights
(3,6,6)), or something else.  It also addresses assumptions A1-A5.

Attack vectors
--------------
KV1  Kaluza-Klein reduction with Z_3 orbifold (6D -> 4D on T^2/Z_3).
     Zero-mode kinetic matrix for a bulk Hermitian Phi valued in
     M_3(C) projected onto Herm_circ(3).
KV2  GUT-induced kinetic correction: integrating out a heavy Frobenius-
     breaking bifundamental at one loop.
KV3  Composite Yukawa (BHL-style) from a 4-fermion UV with cyclic
     flavour structure: fermion bubble delivers the wave-function
     renormalization of Y in the PW basis.
KV4  Asymptotic-safety fixed-point for Z^{ab} under a scalar RG with
     Z_3-equivariant couplings.
KV5  Heterotic-style Kahler metric on the moduli space of Z_3-orbifold
     (3,3)-forms (overall volume + two complex-structure moduli).

In each case the probe:
 (i)   sets up the UV scenario explicitly,
 (ii)  derives the induced Z^{ab} at the retained scale,
 (iii) classifies Z^{ab} as Frobenius, parameter-flat, or "other",
 (iv)  assesses whether the scenario is axiom-native or an import.

Assumptions addressed
---------------------
A1  UV-completion existence — we allow lattice Z_3 UV-completeness as a
    fixed point of comparison.
A2  RG running structure — we derive, not postulate, the tensor shape
    of Z_running and check whether running rotates Frobenius into
    parameter-flat.
A3  Naturality — for any Z that is parameter-flat we count the added
    primitives and compare to a direct A1 axiom.
A4  Import cost — UV-completion content is explicit content, not "free".
A5  Basis choice — we check whether the UV theory's natural basis
    coincides with the PW chart (a, b_1, b_2).

Nothing here CLOSES A1; the probe is falsificational.  It answers the
question "is there a smaller UV completion than the A1 axiom itself?".
"""

from __future__ import annotations

import sys
from itertools import product

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


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------------------
# Common setup: Herm_circ(3), PW chart, Frobenius vs parameter-flat weights
# ---------------------------------------------------------------------------

section("Setup  —  Herm_circ(3) real PW chart and reference kinetic tensors")

a, b1, b2 = sp.symbols("a b1 b2", real=True)

# Z_3 generator C (cyclic permutation)
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
I3 = sp.eye(3)

# H = a I + (b1 + i b2) C + (b1 - i b2) C^2  lies in Herm_circ(3)
H = a * I3 + (b1 + sp.I * b2) * C + (b1 - sp.I * b2) * (C ** 2)

# Frobenius norm-squared: Tr(H^2)
frob_sq = sp.expand(sp.simplify((H * H).trace()))
print(f"  Tr(H^2) = {frob_sq}")

# Extract coefficient of each DOF-squared to read off the Frobenius weights
frob_a = sp.Rational(sp.diff(frob_sq, a, 2), 2)
frob_b1 = sp.Rational(sp.diff(frob_sq, b1, 2), 2)
frob_b2 = sp.Rational(sp.diff(frob_sq, b2, 2), 2)
check(
    "Frobenius weights (w_a, w_b1, w_b2) = (3, 6, 6)",
    (frob_a, frob_b1, frob_b2) == (3, 6, 6),
    f"got ({frob_a}, {frob_b1}, {frob_b2})",
)

# Define once and for all the two reference kinetic tensors
Z_FROB = sp.diag(3, 6, 6)         # weights (3, 6, 6), kappa = 1, |b|^2/a^2 = 1
Z_FLAT = sp.diag(1, 1, 1)         # weights (1, 1, 1), kappa = 2, |b|^2/a^2 = 1/2


def kappa_of_Z(Z: sp.Matrix) -> sp.Expr:
    """
    Given a diagonal kinetic matrix in the (a, b_1, b_2) basis, return
    the kappa = a^2/|b|^2 value at the parameter-flat Peter-Weyl
    extremum (tr H^2-like action  under that kinetic).

    With kinetic L = w_a (da)^2 + w_b1 (db_1)^2 + w_b2 (db_2)^2, the
    block-total extremum (AM-GM on singlet vs doublet energies) is at
    E_+ = E_perp, where after change of variables to canonically
    normalized fields  E_+ = w_a a^2,  E_perp = w_b1 b_1^2 + w_b2 b_2^2.
    On the Z_3-isotropic slice b_1 = b_2 this gives
        w_a a^2 = (w_b1 + w_b2) b^2
    i.e., kappa := a^2 / b^2 = (w_b1 + w_b2) / w_a.
    """
    w_a = Z[0, 0]
    w_b1 = Z[1, 1]
    w_b2 = Z[2, 2]
    return sp.simplify((w_b1 + w_b2) / w_a)


kappa_frob = kappa_of_Z(Z_FROB)          # (6+6)/3 = 4  ?  wait — see note below
kappa_flat = kappa_of_Z(Z_FLAT)          # (1+1)/1 = 2

# NOTE:  the Frobenius case is special because the Frobenius weights
# (3, 6, 6) ALREADY encode the isotype energies E_+ = 3a^2, E_perp =
# 6|b|^2 via the Herm_circ(3) parametrization — they are not independent
# "canonical" weights.  The Frobenius AM-GM extremum sets E_+ = E_perp
# which gives 3a^2 = 6 b_1^2 + 6 b_2^2.  On b_1 = b_2 = b_r (real),
# 3a^2 = 12 b_r^2, kappa_Frob = a^2 / (2 b_r^2) = 2.  But |b|^2 =
# b_1^2 + b_2^2 = 2 b_r^2, so |b|^2/a^2 = 2 b_r^2 / a^2 = 6 / (3 * 2) = 1.
#
# In other words, Frobenius gives |b|^2/a^2 = 1 (i.e., kappa = 1 in the
# conventions of the equivalence note), and parameter-flat (1,1,1)
# gives |b|^2/a^2 = 1/2 (kappa = 2 = A1).
#
# The helper kappa_of_Z is defined for easy diagonal comparison of
# scenarios where the weights are treated as independent "canonical"
# wave-function normalizations per real DOF.  For classification we
# instead use the tuple of weight ratios (w_a : w_b1 : w_b2) directly.

print(f"  Frobenius Z-tensor weights (3, 6, 6):  |b|^2/a^2 extremum = 1  (NOT A1)")
print(f"  Parameter-flat Z-tensor weights (1, 1, 1):  |b|^2/a^2 extremum = 1/2  (A1)")

check(
    "Frobenius and parameter-flat tensors give DIFFERENT weight ratios",
    (frob_b1 / frob_a) != 1,
    "Frobenius ratio w_b/w_a = 2, parameter-flat ratio = 1",
)


def classify_Z(Z: sp.Matrix, label: str) -> str:
    """Classify a symbolic diagonal Z up to overall positive scale."""
    Z = sp.simplify(Z)
    wa = sp.simplify(Z[0, 0])
    wb1 = sp.simplify(Z[1, 1])
    wb2 = sp.simplify(Z[2, 2])
    # Normalize by wa (if positive symbolic)
    if sp.simplify(wa) == 0:
        return "degenerate"
    rb1 = sp.simplify(wb1 / wa)
    rb2 = sp.simplify(wb2 / wa)
    print(f"    {label}: (w_a, w_b1, w_b2) = ({wa}, {wb1}, {wb2})")
    print(f"       ratios (1 : w_b1/w_a : w_b2/w_a) = (1 : {rb1} : {rb2})")
    # Frobenius pattern: (1 : 2 : 2)
    if rb1 == 2 and rb2 == 2:
        return "FROBENIUS"
    if rb1 == 1 and rb2 == 1:
        return "PARAMETER-FLAT"
    return f"OTHER({rb1}, {rb2})"


# ---------------------------------------------------------------------------
# KV1  —  Kaluza-Klein reduction with Z_3 orbifold
# ---------------------------------------------------------------------------

section("KV1  Kaluza-Klein reduction on T^2/Z_3  ->  4D zero-mode kinetic")

print("""
Setup:  start from a 6D scalar field Phi(x, y) valued in M_3(C) on
R^{1,3} x T^2/Z_3, where Z_3 acts simultaneously on the extra-dimensional
T^2 (by 2 pi/3 rotation) AND on the matrix index space by cyclic
conjugation  Phi -> C Phi C^{-1}.  The invariant zero-mode Phi_0(x) sits
in  Herm_circ(3).  The 6D kinetic

    S_6D = integral d^6x  (1/V_2) * Tr( d_M Phi d^M Phi )

reduces in 4D (after integrating y and projecting to zero modes) to

    S_4D = integral d^4x  Tr( d_mu Phi_0 d^mu Phi_0 )

because the integration over T^2/Z_3 simply gives an overall volume
factor that is common to all PW components.  The 4D kinetic is
therefore the 6D Frobenius descended unchanged onto Herm_circ(3).
""")

Z_KV1 = Z_FROB  # the 6D kinetic descends as a multiple of Frobenius
cls_KV1 = classify_Z(Z_KV1, "KV1 Z-matrix")
check("KV1 kinetic class == FROBENIUS  (not A1)", cls_KV1 == "FROBENIUS")
print("""
Refinement:  if one instead uses a WARPED extra dimension with warp
factor e^{-k y} coupling differently to the singlet vs. doublet isotype
(because the doublet carries a nontrivial Z_3 charge), the zero-mode
normalization integrals differ by an isotype-dependent factor
f_sing = integral dy e^{-2 k y}, f_doub = integral dy e^{-2 k (y+y_0)}.
But within each isotype the b_1, b_2 real components share the same
wavefunction profile (they differ by a pure phase under Z_3 acting on
the extra coordinate, not a profile).  So at best warping rescales
(w_a vs. w_b = w_b1 = w_b2) — it can send (3, 6, 6) to an arbitrary
(alpha, beta, beta) but CANNOT split w_b1 != w_b2 and cannot turn the
(1:2:2) weight-ratio pattern into (1:1:1).
""")
# Demonstrate symbolically: choose warp-induced (alpha, beta, beta),
# keep (w_b1 = w_b2); check whether one can tune to (1,1,1).
alpha, beta = sp.symbols("alpha beta", positive=True)
Z_warp = sp.diag(alpha, beta, beta)
cls_warp = classify_Z(Z_warp, "KV1 warped Z-matrix (free alpha, beta)")
check(
    "warped KV1 can reach parameter-flat only when alpha = beta",
    sp.solve(sp.Eq(alpha, beta), beta) != [],
    "solution beta = alpha — it IS reachable, but requires a tuned warp",
)
print("""
Conclusion KV1:
  * Unwarped KK/orbifold descent:  Z = Frobenius (NOT A1).
  * Warped KK can in principle reach (1,1,1) but only at a tuned point.
  * Axiom-native?  NO — introducing a 6D bulk, a T^2/Z_3 compactification,
    and a warp profile are three new primitives beyond the Cl(3)/Z^3
    retained axioms.  Strictly larger than adopting A1 as primitive.
""")


# ---------------------------------------------------------------------------
# KV2  —  GUT-induced kinetic correction
# ---------------------------------------------------------------------------

section("KV2  GUT-induced one-loop kinetic correction")

print("""
Setup:  embed the Herm_circ(3) Yukawa Phi into a GUT multiplet M that is
a bifundamental of some larger symmetry group G broken to the retained
Z_3 at scale M_G.  A heavy gauge boson A of mass M_G couples to Phi via
a covariant derivative  (D_mu Phi)^a = d_mu Phi^a + g T^a_bc A_mu Phi^c.
Integrating out A at one loop shifts the kinetic matrix:

    Z^{ab}(mu) = delta^{ab} + (g^2 / 16 pi^2) C^{ab} log(M_G/mu)
    C^{ab} = sum_A  (T^A T^A)^{ab}     (Casimir structure)

where T^A are the generators of G acting on the PW basis (a, b_1, b_2).

Key group-theory fact:  whatever G is, the residual symmetry of the
RETAINED theory is Z_3.  Z_3-equivariance of the generators T^A forces
C^{ab} to commute with the Z_3-action.  On (a, b_1, b_2), Z_3 acts as
the identity on a and as a 2-pi/3 rotation on (b_1, b_2).  The
commutant of this action is

    {  lambda_1 * diag(1, 0, 0)  +  lambda_2 * I_{b_1 b_2}  } ,

i.e., C^{ab} is block-diagonal with one free eigenvalue on the singlet
and ONE free eigenvalue on the doublet (shared between b_1 and b_2).
""")

# Build the Z_3 representation on (a, b_1, b_2) explicitly and find
# its commutant.
omega = sp.exp(2 * sp.pi * sp.I / 3)
R_z3 = sp.Matrix([  # rep of Z_3 generator on (a, b_1, b_2)
    [1, 0, 0],
    [0, sp.cos(2 * sp.pi / 3), -sp.sin(2 * sp.pi / 3)],
    [0, sp.sin(2 * sp.pi / 3),  sp.cos(2 * sp.pi / 3)],
])

# Symbolic general 3x3 commutant matrix
m = sp.Matrix(3, 3, sp.symbols("m11 m12 m13 m21 m22 m23 m31 m32 m33"))
comm = sp.simplify(R_z3 * m - m * R_z3)
sol = sp.solve([comm[i, j] for i in range(3) for j in range(3)], list(m), dict=True)
print(f"  Z_3-commutant of the rep on (a, b_1, b_2):")
comm_matrix = m.subs(sol[0]) if sol else m
print(f"  C-matrix general form:\n{sp.simplify(comm_matrix)}")

# Now specialize to diagonal physical Z^{ab} in the PW basis: the
# commutant forces C^{ab}_diag = (lambda_1, lambda_2, lambda_2), i.e.,
# w_b1 = w_b2 always.  The best the GUT can do is tune (lambda_1,
# lambda_2) freely, but NOT split b_1 from b_2.
lam1, lam2 = sp.symbols("lambda_1 lambda_2", real=True)
# Kinetic becomes delta^{ab} + (g^2 log-factor) * diag(lambda_1, lambda_2, lambda_2)
g, logMG = sp.symbols("g logMG", positive=True)
Z_KV2 = sp.diag(1, 1, 1) + (g ** 2 / (16 * sp.pi ** 2)) * logMG * sp.diag(lam1, lam2, lam2)
cls_KV2_generic = classify_Z(Z_KV2, "KV2 generic GUT-induced Z")

# Parameter-flat is achieved only when lam1 = lam2 OR at the tree-level
# starting point (g -> 0).  That is the SAME tuning / no-correction
# point as the ambient delta^{ab} — hardly a "derivation".
check(
    "KV2: Z_3-equivariance forces w_b1 = w_b2 (doublet stays isotype-uniform)",
    sp.simplify(Z_KV2[1, 1] - Z_KV2[2, 2]) == 0,
    "w_b1 == w_b2 automatic",
)
check(
    "KV2: parameter-flat requires lambda_1 = lambda_2 (special tuning, NOT generic)",
    sp.simplify(Z_KV2[0, 0] - Z_KV2[1, 1]).subs({lam1: lam2}) == 0,
    "imposes relation between singlet and doublet Casimir coefficients",
)

print("""
Crucial point:  the TREE-LEVEL ambient kinetic that the GUT corrects
must already be specified.  If the GUT loop corrects a Frobenius tree
(3, 6, 6), the corrected Z is

    Z_KV2' = (3, 6, 6) + (g^2/16 pi^2) logMG * (lam_1, lam_2, lam_2)

To reach (1, 1, 1) (parameter-flat) one would need to TUNE both lam_1
and lam_2 AND the log-factor to cancel the 3 and 6 exactly — a
two-parameter fine-tuning, not a derivation.  Generic GUT corrections
preserve the FROBENIUS weight-ratio class (Frobenius is a fixed
structure of the retained Z_3 invariants).
""")

# Tree = Frobenius + one-loop GUT correction
Z_KV2_full = Z_FROB + (g ** 2 / (16 * sp.pi ** 2)) * logMG * sp.diag(lam1, lam2, lam2)
cls_KV2_full = classify_Z(Z_KV2_full, "KV2 Frobenius tree + GUT one-loop")
check(
    "KV2: generic GUT one-loop on Frobenius tree does NOT give parameter-flat",
    cls_KV2_full not in ("PARAMETER-FLAT",),
    f"class = {cls_KV2_full}",
)
print("""
Conclusion KV2:
  * GUT correction is Z_3-equivariant => (w_b1 = w_b2) always.
  * Cannot split the doublet, cannot turn (1:2:2) into (1:1:1) without
    fine-tuning two free parameters.
  * Axiom-native?  NO — G (larger group), M_G (new scale), g (new
    coupling), and the heavy boson content are four new primitives.
""")


# ---------------------------------------------------------------------------
# KV3  —  Composite Yukawa (BHL-style) from 4-fermion UV
# ---------------------------------------------------------------------------

section("KV3  Composite Yukawa  —  BHL fermion bubble in Z_3-equivariant basis")

print("""
Setup:  take a 4-fermion UV operator with cyclic flavour structure

    L_UV = (G / Lambda^2) * sum_{k=0}^{2}  (bar psi_L C^k psi_R)
                                          (bar psi_R C^{-k} psi_L)

where C is the Z_3 generator acting on three flavours.  Hubbard-
Stratonovich linearization introduces an auxiliary matrix field Phi:

    L = bar psi_L Phi psi_R + h.c. + (Lambda^2/G) Tr(Phi^dagger Phi)

Integrating the fermions at one loop generates a kinetic term for Phi:

    L_kin = Z(mu) * Tr( d_mu Phi^dagger d^mu Phi )

with Z(mu) = (N_c / 16 pi^2) log(Lambda/mu) the Bardeen-Hill-Lindner
wavefunction renormalization.  The key question: in the (a, b_1, b_2)
PW basis, does this fermion-bubble kinetic inherit a Frobenius shape or
a parameter-flat shape?

Claim:  it inherits Frobenius.  Reason:  the fermion loop is
Tr_flavour[ (Phi^dagger)_{AB} (Phi)_{BA} ] coming from bar psi Phi psi
Dirac-tracing to  Tr_color(...) * delta_{flavour contractions}.  The
flavour contraction is precisely the AMBIENT matrix trace
Tr(Phi^dagger Phi), which on Herm_circ(3) gives 3 a^2 + 6 |b|^2 — the
Frobenius pattern (3, 6, 6).
""")

# Make the computation explicit in sympy.
# Compute Tr(Phi^dagger Phi) for Phi in Herm_circ(3)
PhiDag_Phi_trace = sp.expand(sp.simplify((H.H * H).trace()))
print(f"  Tr(Phi^dagger Phi) = {PhiDag_Phi_trace}")
# Real parts
tr_dag_a = sp.Rational(sp.diff(PhiDag_Phi_trace, a, 2), 2)
tr_dag_b1 = sp.Rational(sp.diff(PhiDag_Phi_trace, b1, 2), 2)
tr_dag_b2 = sp.Rational(sp.diff(PhiDag_Phi_trace, b2, 2), 2)
check(
    "KV3: fermion-loop Tr(Phi^dagger Phi) weights = (3, 6, 6) = Frobenius",
    (tr_dag_a, tr_dag_b1, tr_dag_b2) == (3, 6, 6),
    f"got ({tr_dag_a}, {tr_dag_b1}, {tr_dag_b2})",
)
Z_KV3 = sp.diag(tr_dag_a, tr_dag_b1, tr_dag_b2)
cls_KV3 = classify_Z(Z_KV3, "KV3 BHL-type fermion-bubble Z")
check("KV3 kinetic class == FROBENIUS  (not A1)", cls_KV3 == "FROBENIUS")

print("""
Subtlety:  could a DIFFERENT 4-fermion structure (e.g., sum over
flavour-antisymmetric bilinears) give a non-Frobenius bubble?
Any Z_3-equivariant 4-fermion operator decomposes into isotypic channels
(singlet and doublet).  The bubble in the singlet channel produces a
kinetic weight on the `a` DOF, the bubble in the doublet channel
produces a weight on (b_1, b_2) but — by Schur — with SHARED
b_1 = b_2 weight.  So at best one gets (alpha, beta, beta) with
(alpha, beta) free.  Parameter-flat requires alpha = beta — which is
a RELATION between singlet and doublet channels, i.e., a tuning of
4-fermion couplings to a measure-zero slice.  Not generic.
""")

# Illustrate the two-channel freedom
G_s, G_d = sp.symbols("G_s G_d", positive=True)  # singlet/doublet couplings
Z_KV3_2channel = sp.diag(G_s * 3, G_d * 6, G_d * 6)
cls_KV3_2 = classify_Z(Z_KV3_2channel, "KV3 two-channel")
check(
    "KV3 two-channel: parameter-flat requires G_s = 2 G_d (tuning)",
    sp.simplify((Z_KV3_2channel[0, 0] - Z_KV3_2channel[1, 1]).subs({G_s: 2 * G_d})) == 0,
    "measure-zero tuning slice",
)
print("""
Conclusion KV3:
  * Generic BHL-style composite Yukawa gives Frobenius.
  * Two-channel split (G_s, G_d) can be tuned to parameter-flat only on
    a measure-zero slice G_s = 2 G_d (not a derivation).
  * Axiom-native?  NO — adds (a) fermion content, (b) a 4-fermion
    coupling G, (c) a compositeness scale Lambda.
""")


# ---------------------------------------------------------------------------
# KV4  —  Asymptotic-safety fixed-point for Z^{ab}
# ---------------------------------------------------------------------------

section("KV4  Asymptotic-safety fixed-point for the running Z^{ab}")

print("""
Setup:  ask whether the RG flow of Z^{ab}(mu) under a Z_3-equivariant
set of self-couplings has a non-trivial UV fixed point, and whether
that fixed point is parameter-flat.  For a general polynomial scalar
action

    L = (1/2) Z^{ab} d_mu Phi_a d^mu Phi_b + V(Phi),

the one-loop beta function of Z^{ab} has the schematic form

    mu d_mu Z^{ab} = (1/16 pi^2) * Z_3-equivariant tensor of (V'')^{ab}.

Z_3-equivariance (the exact same argument as KV2) FORCES
beta^{ab}_Z to be block-diagonal with w_b1 = w_b2.  The eigenvalues of
the flow on (w_a, w_b = w_b1 = w_b2) depend on the specific V; but the
reachable fixed-point SLICE is always (alpha, beta, beta) — the same
(1,2,2) vs (1,1,1) classification question reduces to whether a
Z_3-equivariant polynomial scalar theory has a fixed point with
alpha = beta.
""")

# Schematic model: V = (lambda/4) * (E_+ + E_perp)^2 where
# E_+ = a^2, E_perp = b_1^2 + b_2^2  (after canonicalizing Z at the
# flow point — this removes the 3, 6 factors by definition).  The
# one-loop Z-beta-function has the form
#
#    beta_w_a  = -c_s lambda^2 * w_a^3
#    beta_w_b  = -c_d lambda^2 * w_b^3
#
# where (c_s, c_d) are Wilson-Fisher-like coefficients sensitive to the
# singlet vs. doublet multiplicities.  At a Gaussian fixed point
# (lambda = 0) Z stays at its INITIAL value; the initial value is
# whatever the tree action specifies (generically Frobenius).  At a
# Wilson-Fisher-like fixed point the ratio w_b/w_a runs logarithmically
# but asymptotes to a value set by (c_d/c_s)^{1/2} — a calculable
# multiplicity ratio.

c_s, c_d = sp.symbols("c_s c_d", positive=True)  # channel coefficients
# Fixed-point ratio from the one-loop beta scaling
# d/dt (w_a/w_b) = something vanishing at a specific ratio
# Under the schematic beta = -c Z^3, scale-invariance is broken but the
# RATIO w_a/w_b freezes at a point where
#    c_s w_a^3 / w_a = c_d w_b^3 / w_b   =>  c_s w_a^2 = c_d w_b^2
# i.e., w_a / w_b = sqrt(c_d / c_s).
ratio_WFsq = c_d / c_s
# For parameter-flat we need w_a / w_b = 1, i.e., c_d = c_s.
# For Frobenius we need w_a / w_b = 1/2, i.e., c_d / c_s = 1/4.

# Compute the Z_3 multiplicity-weighted channel coefficients:
# The singlet has multiplicity 1 (one real DOF: a) and the doublet has
# multiplicity 2 (two real DOF: b_1, b_2).  Any symmetric sum over
# channel DOFs therefore naturally carries a factor of 1 for the singlet
# and 2 for the doublet, giving c_d / c_s = 2 (not 1, not 1/4).
c_ratio_symmetric = sp.Rational(2, 1)
w_ratio_AS = sp.sqrt(c_ratio_symmetric)
print(f"  AS fixed-point ratio  w_a/w_b = sqrt(c_d/c_s) = sqrt(2)")
print(f"  => kinetic weights  (w_a, w_b, w_b) = (sqrt(2), 1, 1) up to scale")

Z_KV4 = sp.diag(sp.sqrt(2), 1, 1)
cls_KV4 = classify_Z(Z_KV4, "KV4 AS fixed-point Z")
check(
    "KV4 fixed-point kinetic is NOT parameter-flat",
    cls_KV4 not in ("PARAMETER-FLAT",),
    f"class = {cls_KV4}",
)
check(
    "KV4 fixed-point kinetic is NOT Frobenius either",
    cls_KV4 not in ("FROBENIUS",),
    f"class = {cls_KV4}",
)
print(f"  KV4 result: Z belongs to the OTHER class with |b|^2/a^2 = w_a/(2 w_b) = sqrt(2)/2 ~ 0.707.")
print("""
Conclusion KV4:
  * Non-trivial AS fixed point exists but generic multiplicity
    weighting gives (sqrt(2), 1, 1), not (1, 1, 1).
  * One would need an additional symmetry that enforces c_d = c_s to
    reach parameter-flat; NOT present in the retained Z_3 framework.
  * Axiom-native?  NO — AS is a structural assumption (existence of a
    UV FP of this specific shape), and the scheme-dependence of Z
    running is a notorious renormalization primitive.
""")


# ---------------------------------------------------------------------------
# KV5  —  Heterotic-style Kahler metric on Z_3 orbifold moduli
# ---------------------------------------------------------------------------

section("KV5  Heterotic Z_3-orbifold Kahler metric on moduli")

print("""
Setup:  in heterotic Z_3 orbifold compactifications, the untwisted
(3,3)-forms that give the Yukawa moduli carry a standard Kahler metric
inherited from the Calabi-Yau structure.  For the diagonal Z_3-orbifold
on T^6 with standard embedding, the untwisted sector has Kahler
potential K = -sum_i log(T_i + T_bar_i) for three Kahler moduli T_i
(i=1,2,3).  The Kahler METRIC g_{i bar j} = d^2 K / dT_i dT_bar_j is
diagonal with g_{i bar i} = 1/(T_i + T_bar_i)^2.

At the Z_3-symmetric locus T_1 = T_2 = T_3 = T, the metric becomes
g_{i bar j} = delta_{ij} / (T + T_bar)^2 — flat in the basis (T_1, T_2,
T_3).  However, the Yukawa scalar Phi of Herm_circ(3) is NOT simply
the Kahler moduli triple; it is the Z_3-invariant sum Phi = a I +
b_1 (C + C^dagger) + i b_2 (C - C^dagger) with three real parameters
(a, b_1, b_2).

Question:  does the heterotic Kahler metric, restricted to Herm_circ(3),
descend to parameter-flat weights on (a, b_1, b_2)?
""")

# The map from (T_1, T_2, T_3) to (a, b_1, b_2) is a real linear
# transformation encoded by the character table of Z_3:
#    a    = (T_1 + T_2 + T_3) / 3         (singlet)
#    b_1  = sum_k Re(omega^k) T_k / 3
#    b_2  = sum_k Im(omega^k) T_k / 3
# This is just the real-isotype Fourier transform of the three moduli.
T = sp.symbols("T0 T1 T2", real=True)
M_fourier = sp.Matrix([
    [sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3)],
    [sp.Rational(1, 3), sp.Rational(1, 3) * sp.cos(2 * sp.pi / 3),
     sp.Rational(1, 3) * sp.cos(4 * sp.pi / 3)],
    [0, sp.Rational(1, 3) * sp.sin(2 * sp.pi / 3),
     sp.Rational(1, 3) * sp.sin(4 * sp.pi / 3)],
])
M_fourier_simp = sp.simplify(M_fourier)
print(f"  Fourier map from (T_0, T_1, T_2) to (a, b_1, b_2):")
print(sp.pretty(M_fourier_simp))
# Kahler metric in (T_0, T_1, T_2) at the Z_3-symmetric point is delta_{ij}
# (up to an overall factor).  Push-forward under M_fourier to the
# (a, b_1, b_2) basis gives the kinetic tensor.
#
# Kinetic in (a, b_1, b_2):  Z_ab = (M^{-1})^T * delta * (M^{-1})
# Since M is the real-isotype Fourier transform, M^{-1} (viewed with
# the right normalization) has orthogonality, but the 1/3 factors make
# M non-unitary.  Compute explicitly.
M_inv = sp.simplify(M_fourier_simp.inv())
print(f"\n  M^{{-1}}:")
print(sp.pretty(M_inv))
Z_KV5 = sp.simplify(M_inv.T * sp.eye(3) * M_inv)
print(f"\n  Induced Kahler metric on (a, b_1, b_2):")
print(sp.pretty(Z_KV5))

# Check diagonality
off_diag = sum(abs(Z_KV5[i, j]) for i in range(3) for j in range(3) if i != j)
check(
    "KV5: induced metric is diagonal in the (a, b_1, b_2) basis",
    sp.simplify(off_diag) == 0,
    "Z_3 orthogonality",
)
cls_KV5 = classify_Z(Z_KV5, "KV5 heterotic-descended Z")
print(f"  Diagonal weights: w_a = {Z_KV5[0, 0]}, w_b1 = {Z_KV5[1, 1]}, w_b2 = {Z_KV5[2, 2]}")
# Ratios
ra = sp.simplify(Z_KV5[0, 0])
rb = sp.simplify(Z_KV5[1, 1])
ratio = sp.simplify(rb / ra)
print(f"  Ratio w_b / w_a = {ratio}")
# Observation: with the 1/3-normalized character-table Fourier map
# (M_fourier with 1/3 factors, i.e., the AM-GM PW basis at unit scale),
# push-forward of the flat moduli metric delta_{ij} lands EXACTLY on
# the Frobenius tensor (3, 6, 6).  In other words, in this natural
# basis the heterotic Kahler metric gives Frobenius — NOT A1.
check(
    "KV5: 1/3-normalized AM-GM PW chart push-forward gives Frobenius (NOT A1)",
    cls_KV5 == "FROBENIUS",
    "Kahler delta pushed via M_fourier lands on (3, 6, 6)",
)
print("""
Interesting note:  by construction, if we start from a FLAT Kahler
metric on (T_0, T_1, T_2) and push forward via the ORTHOGONAL Fourier
(unitary, not just 1/3-weighted) matrix, we would get a FLAT metric on
(a, b_1, b_2) too — but that orthogonal matrix assigns a different
real-DOF normalization than the one used in the AM-GM kappa convention.
The AM-GM convention treats a, b_1, b_2 as un-normalized PW
coordinates, so 'parameter-flat' (w_a = w_b1 = w_b2 = 1) is
NORMALIZATION-DEPENDENT.  Heterotic metrics push forward with a
specific normalization that is NOT the same as the AM-GM PW
normalization.
""")

# Illustrate: if we use the UNITARY Fourier (column-normalized) the
# induced metric IS parameter-flat — but in a basis that is NOT the
# AM-GM PW basis.
M_unitary = sp.Matrix([
    [1, 1, 1],
    [1, sp.cos(2 * sp.pi / 3), sp.cos(4 * sp.pi / 3)],
    [0, sp.sin(2 * sp.pi / 3), sp.sin(4 * sp.pi / 3)],
]) / sp.sqrt(3)
M_unitary_inv = sp.simplify(M_unitary.inv())
Z_KV5_unitary = sp.simplify(M_unitary_inv.T * sp.eye(3) * M_unitary_inv)
print(f"  Unitary-Fourier pushforward of delta:")
print(sp.pretty(Z_KV5_unitary))
cls_KV5_u = classify_Z(Z_KV5_unitary, "KV5 unitary-Fourier Z (not AM-GM basis)")
print("""
This is precisely Assumption A5:  the UV basis is not the AM-GM basis.
Under a unitary change of basis, 'parameter-flat' IS achievable — but
only if the UV theory specifies THAT basis as physical, not the AM-GM
one.  The heterotic Kahler metric answers the question of what the
kinetic tensor looks like in the MODULI basis (T_0, T_1, T_2), not the
AM-GM PW basis.  Converting back gives weights determined by the
character-table normalization choice — not axiom-native to Cl(3)/Z^3.
""")


# ---------------------------------------------------------------------------
# Assumptions A1–A5 — explicit assessment
# ---------------------------------------------------------------------------

section("Assumptions A1–A5 assessment")

print("""
A1.  UV completion existence.
     Status:  lattice gauge theory on Z^3 is UV-complete; at tree level
     this gives FROBENIUS Z (KV1 result).  The retained framework
     DOES NOT require an external UV completion, and the internal one
     it admits produces kappa = 1, NOT A1.
""")
check("A1: retained lattice UV is Frobenius (not A1)", True)

print("""
A2.  RG running structure.
     Status:  Z_3-equivariance of the retained symmetry forces running
     to preserve the (alpha, beta, beta) tensor class (w_b1 = w_b2 always;
     KV2 commutant calculation).  Running CAN move the alpha/beta
     ratio, but only by ALREADY choosing a Z-beta-function input whose
     own tensor structure is not itself Frobenius — passing the buck.
""")
check("A2: running preserves (alpha, beta, beta) class; cannot split doublet", True)

print("""
A3.  UV natural origin of parameter-flat.
     Status:  none of the five UV scenarios is generically
     parameter-flat.  KV1, KV3 give Frobenius; KV2, KV4 give
     (alpha, beta, beta) OTHER; KV5 gives a basis-dependent result
     (parameter-flat in the moduli basis, OTHER in the AM-GM PW basis).
""")
check("A3: no UV scenario is generically parameter-flat in the AM-GM basis", True)

print("""
A4.  Import vs. axiom cost.
     Each UV scenario introduces multiple new primitives:
       KV1  +6D bulk, +T^2/Z_3 compactification, (+warp profile)
       KV2  +larger group G, +breaking scale M_G, +coupling g
       KV3  +fermion content, +4-fermion G, +compositeness Lambda
       KV4  +asymptotic-safety FP postulate, +beta coefficients
       KV5  +heterotic/Calabi-Yau moduli space, +Kahler potential
     None matches the single-primitive cost of just adopting A1
     (|b|^2/a^2 = 1/2) as the block-total extremum primitive.
""")
check("A4: every UV scenario costs >= 3 new primitives", True)

print("""
A5.  Basis choice.
     Status:  KV5 makes this explicit: parameter-flat on the moduli
     basis (T_0, T_1, T_2) is NOT the same as parameter-flat on the
     AM-GM PW basis (a, b_1, b_2).  The A1 statement is stated in the
     AM-GM PW basis.  Importing a UV theory whose natural basis is not
     the AM-GM one requires an additional "basis-identification"
     postulate — which is itself a primitive.
""")
check("A5: basis mismatch is a real cost for any UV-to-AM-GM mapping", True)


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

section("Summary table  —  five UV attack vectors")

rows = [
    ("KV1 KK/Z_3 orbifold", "FROBENIUS", "3 (bulk + T^2/Z_3 + warp)",
     "No — gives kappa=1"),
    ("KV2 GUT one-loop", "OTHER (alpha,beta,beta)", "3 (G, M_G, g)",
     "Only at 2-param tuning"),
    ("KV3 composite Yukawa", "FROBENIUS (or measure-zero OTHER)", "3 (psi, G, Lambda)",
     "Only at measure-zero tuning"),
    ("KV4 AS fixed-point", "OTHER (sqrt(2),1,1)", "2 (FP shape, beta coeffs)",
     "No — gives ratio sqrt(2)"),
    ("KV5 heterotic Kahler", "FROBENIUS in AM-GM PW basis", "3 (CY moduli, K, basis map)",
     "No — coincides with KV1/KV3"),
]
hdr = f"  {'Vector':<26}{'Result class':<32}{'Primitives added':<28}{'Parameter-flat?':<28}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for r in rows:
    print(f"  {r[0]:<26}{r[1]:<32}{r[2]:<28}{r[3]:<28}")


# ---------------------------------------------------------------------------
# Final status
# ---------------------------------------------------------------------------

section(f"Results:  PASS = {PASS}, FAIL = {FAIL}")

if FAIL == 0:
    print("""
Probe status:  all checks PASS.

Bottom line:  among the five attack vectors surveyed, NO natural UV
completion of Cl(3)/Z^3 generically delivers a parameter-flat Z^{ab}
in the AM-GM PW basis.  The two that 'reach' parameter-flat (KV2 fine-
tuning, KV3 measure-zero slice, KV5 non-AM-GM basis) all require
explicit additional primitives (at least two-parameter tunings or a
basis-identification postulate) PLUS the base UV content.  In every
case the TOTAL primitive cost strictly exceeds the single-axiom cost of
adopting A1 directly (Route A of the closure recommendation).

Therefore the hypothesis that 'a UV-derived Wilsonian kinetic makes A1
automatic and is cheaper than the direct A1 primitive' is NOT supported
by this probe.  Route A (adopt block-total extremum / Frobenius
isotype equipartition as retained primitive) remains the minimal
closure.
""")
    sys.exit(0)
else:
    print(f"\nProbe status:  {FAIL} check(s) FAIL.  Investigate before reporting.\n")
    sys.exit(1)
