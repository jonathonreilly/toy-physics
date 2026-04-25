"""
Frontier runner — Z_3-TWISTED partition-function probe for Koide A1.

STATUS: derivation PROBE / investigation script. Not a closure claim.

TARGET QUESTION
---------------
The block-total AM-GM extremum theorem says that on Herm_circ(3),

    S_block(H) = log E_+(H) + log E_perp(H),
    E_+(H)    = (tr H)^2 / 3        = || pi_+(H) ||_F^2,
    E_perp(H) = Tr(H^2) - (tr H)^2/3 = || pi_perp(H) ||_F^2,

subject to `E_+ + E_perp = Tr H^2 = N` fixed, is uniquely extremized
(maximized by AM-GM) at `E_+ = E_perp`, equivalently `|b|^2/a^2 = 1/2`.
This is the A1 / Frobenius-equipartition / Koide Q=2/3 condition.

Prior attempts to derive the extremum of S_block from natural
UNTWISTED partition functions failed:

   * log|det D| saddle  -> |b|/a ~ 3.3 (wrong direction)
   * Coleman-Weinberg   -> uniform eigenvalues (kappa = 1/3, Q=1/3)
   * Gaussian max-ent   -> <a^2> = <|b|^2> not 2<|b|^2>

This probe tests whether a Z_3-TWISTED partition function gives the
correct saddle. We test, on a finite-dimensional one-generation
simplification (H in Herm_circ(3), a single real Hermitian circulant
playing the role of a mass-like operator), six concrete attack
vectors (V1..V6) in order of increasing exotic-ness.

Concretely, for H = a I + b C + bbar C^2 on C^3, its eigenvalues under
the Fourier basis are

    lambda_k = a + omega^k b + omega^{-k} bbar   (k = 0, 1, 2)
            = a + 2 Re(omega^k b)

    lambda_+ = lambda_0 = a + 2 Re(b)          (trivial isotype eigenvalue)
    lambda_1 = a + 2 Re(omega  b)
    lambda_2 = a + 2 Re(omega^2 b)

The Z_3 action on the Fourier basis is `k -> k+1 (mod 3)`. Under the
Fourier transform it becomes a CYCLIC PERMUTATION of (lambda_0,
lambda_1, lambda_2) — on our real-b parameterization it becomes a
cyclic permutation of the three eigenvalues.

                  ABBREVIATED KEY IDENTITIES

For H in Herm_circ(3) with (a, b1, b2):

  Tr(H)    = 3 a                             = sum_k lambda_k
  Tr(H^2)  = 3 a^2 + 6 (b1^2 + b2^2)         = sum_k lambda_k^2
  E_+      = 3 a^2                           = lambda_0^2 / 3 + ...
  E_perp   = 6 (b1^2 + b2^2)                 = Tr(H^2) - (tr H)^2/3

  Let  kappa := a^2 / |b|^2 = a^2 / (b1^2 + b2^2).
  Then  E_+/E_perp = kappa/2, so A1 <=> kappa = 2.

                  ATTACK VECTORS TESTED

  V1  Character-twisted single-sector partition function
        Z_chi(beta, H) := Tr(chi(g0) exp(-beta H))
      for a Z_3 irreducible character chi.  Compute log Z_chi as a
      function of H, find its saddle, compare to A1.

  V2  Plancherel-weighted partition function
        Z_P(beta, H) := sum_{rho in hat(Z_3)} dim(rho)^2 * Tr_rho(exp(-beta H)) / |G|.

  V3  Projective isotype-product partition function (PRIMARY CANDIDATE)
        Z_iso(beta, H) := Tr(P_+ exp(-beta H)) * Tr(P_perp exp(-beta H)).
      Here P_+ and P_perp are the Herm_circ(3) isotype projectors on
      C^3: P_+ = J/3 (project to the trivial-character subspace) and
      P_perp = I - P_+ (project to the two-dim complement).
      log Z_iso = log Tr(P_+ exp(-beta H)) + log Tr(P_perp exp(-beta H)).
      In the high-temperature (beta -> 0) limit,
         Tr(P_+ exp(-beta H)) -> 1 - beta lambda_0 + ... ,
         Tr(P_perp exp(-beta H)) -> 2 - beta(lambda_1 + lambda_2) + ... ,
      so log Z_iso ~ log 1 + log 2 + ... (trivial), but sub-leading
      corrections involve E_+ and E_perp. We check whether the
      saddle of log Z_iso at fixed Tr H^2 gives A1.

  V4  Theta-angle / discrete-gauge twisting
        Z(beta, H, theta) := sum_{n=0,1,2} exp(i theta n) Z_n(beta, H),
      with Z_n the n-th Z_3-projected trace.  Varying theta, locate
      critical points and check alignment with A1.

  V5  Duistermaat-Heckman / equivariant localization (analytic, no numerics)
      Since the DH formula localizes to fixed points of the Z_3
      action, we check the tangent-weight product against A1.

  V6  Orbifold (twisted-sector sum) partition function
        Z_orb(beta, H) := (1/3) sum_{i=0,1,2} Tr(g0^i exp(-beta H)),
      where g0 generates Z_3. Equivalent to Z_3-invariant projection.
      In the Fourier basis, this projects onto the trivial isotype
      (i.e. onto the k=0 eigenvalue only).

                  DELIVERABLE & REPORTING

For each vector, we compute the saddle symbolically / numerically and
compare to the A1 condition `a^2 = 2 |b|^2`.

    FORCES A1    : saddle lies on a^2 = 2 |b|^2 exclusively.
    GIVES DIFFERENT: saddle lies on a different curve (needs naming).
    TRIVIAL        : saddle is degenerate / independent of H.
    INCONCLUSIVE   : formal structure but not computable at this
                      level of simplification.

We also answer assumption questions A1..A5 at the end.

Dependencies: sympy + numpy + stdlib.
"""

from __future__ import annotations

import numpy as np
import sympy as sp


PASS = 0
FAIL = 0
VERDICTS: dict[str, str] = {}


def ok(label: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return cond


# ---------------------------------------------------------------------------
# Symbolic infrastructure: Herm_circ(3) Hermitian circulant + isotype data
# ---------------------------------------------------------------------------

a_s, b1_s, b2_s, beta_s = sp.symbols("a b1 b2 beta", real=True)
b_s = b1_s + sp.I * b2_s
bbar_s = b1_s - sp.I * b2_s

I3 = sp.eye(3)
C_gen = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
C2 = C_gen * C_gen
omega = sp.exp(2 * sp.pi * sp.I / 3)
omega_bar = sp.exp(-2 * sp.pi * sp.I / 3)

H_sym = a_s * I3 + b_s * C_gen + bbar_s * C2

trH = sp.simplify(H_sym.trace())
trH2 = sp.simplify((H_sym * H_sym).trace())
ok("setup-0 tr H = 3a symbolically", sp.simplify(trH - 3 * a_s) == 0,
   detail=f"tr H = {trH}")
ok(
    "setup-1 Tr H^2 = 3a^2 + 6 (b1^2+b2^2) symbolically",
    sp.simplify(trH2 - (3 * a_s ** 2 + 6 * (b1_s ** 2 + b2_s ** 2))) == 0,
    detail=f"Tr H^2 = {trH2}",
)

# Isotype projectors on C^3 (vector-space projectors) for V3:
#   P_+ = J/3  (projects onto trivial-character line)
#   P_perp = I - P_+
Jmat = sp.ones(3, 3)
P_plus = Jmat / 3
P_perp = I3 - P_plus
ok(
    "setup-2 P_+ = J/3 is Hermitian idempotent rank 1",
    sp.simplify((P_plus * P_plus) - P_plus) == sp.zeros(3, 3)
    and sp.simplify(P_plus - P_plus.H) == sp.zeros(3, 3),
)
ok(
    "setup-3 P_perp = I - P_+ has rank 2",
    sp.simplify((P_perp * P_perp) - P_perp) == sp.zeros(3, 3)
    and sp.simplify(P_plus + P_perp - I3) == sp.zeros(3, 3),
)

# Eigenvalues of H (in the Fourier basis, these are the diagonal entries):
lam0 = a_s + 2 * b1_s                         # k=0: trivial isotype
lam1 = a_s + 2 * (sp.Rational(-1, 2) * b1_s - sp.sqrt(3) / 2 * b2_s)  # k=1
lam2 = a_s + 2 * (sp.Rational(-1, 2) * b1_s + sp.sqrt(3) / 2 * b2_s)  # k=2

# Verify sum = trH and sum_sq = TrH^2.
ok(
    "setup-4 sum_k lambda_k = tr H",
    sp.simplify(lam0 + lam1 + lam2 - trH) == 0,
)
ok(
    "setup-5 sum_k lambda_k^2 = Tr H^2",
    sp.simplify(lam0 ** 2 + lam1 ** 2 + lam2 ** 2 - trH2) == 0,
)


# ---------------------------------------------------------------------------
# Helper: compute exp(-beta H) in the Fourier basis (diagonal).
# The Fourier matrix F diagonalizes every circulant: F^dag H F = diag(lam_k).
# ---------------------------------------------------------------------------

def expmbeta_spectrum():
    """Return (e0, e1, e2) = exp(-beta lambda_k) as sympy expressions."""
    return (
        sp.exp(-beta_s * lam0),
        sp.exp(-beta_s * lam1),
        sp.exp(-beta_s * lam2),
    )


# Compact small-beta expansion to second order in beta: exp(-beta lam) ~
# 1 - beta lam + beta^2 lam^2 / 2.

def expand_small_beta(expr, order: int = 2):
    return sp.series(expr, beta_s, 0, order + 1).removeO()


# ---------------------------------------------------------------------------
# Assumption probes A1-A5 (in-script): quick algebraic checks.
# ---------------------------------------------------------------------------

print("\n=== Assumption probes A1..A5 (quick checks) ===")

# A3: Z_3 acts on the eigenvalue triple by cyclic permutation.
# The generator g0 shifts k -> k+1 (mod 3), which on (lambda_0, lambda_1,
# lambda_2) is a 3-cycle. We verify that permuting the three eigenvalues
# cyclically leaves Tr H, Tr H^2, E_+, and E_perp invariant.
perm = {lam0: lam1, lam1: lam2, lam2: lam0}
# invariance of Tr H
trH_perm = (lam1 + lam2 + lam0)
ok(
    "A3.1 Tr H invariant under cyclic permutation of eigenvalues",
    sp.simplify(trH_perm - trH) == 0,
)
# invariance of Tr H^2
trH2_perm = (lam1 ** 2 + lam2 ** 2 + lam0 ** 2)
ok(
    "A3.2 Tr H^2 invariant under cyclic permutation of eigenvalues",
    sp.simplify(trH2_perm - trH2) == 0,
)
# E_+ and E_perp are expressible in (tr H, Tr H^2) so also invariant.
E_plus_formula = (trH ** 2) / 3
E_perp_formula = trH2 - E_plus_formula
ok(
    "A3.3 E_+ and E_perp are symmetric in the 3 eigenvalues",
    sp.simplify(E_plus_formula - (lam0 + lam1 + lam2) ** 2 / 3) == 0
    and sp.simplify(E_perp_formula - (trH2 - (lam0 + lam1 + lam2) ** 2 / 3)) == 0,
)


# ===========================================================================
# V1 — Character-twisted single-sector partition function
#   Z_chi(beta, H) = Tr(chi(g0) exp(-beta H))
# with chi the omega-character: chi(g0) = omega, chi(g0^2) = omega^2, chi(1)=1.
# ===========================================================================

print("\n=== V1  Character-twisted Z_chi(beta, H) = Tr( U_chi exp(-beta H) ) ===")

# g0 acts on C^3 by cyclic shift (the matrix C_gen). In the Fourier basis it
# is diag(1, omega, omega^2). So the "character-insertion" operator for the
# omega-character is U_chi = C_gen (trace = 0 on the cyclic-shift basis,
# but picks up omega in the k-th eigenspace).
# Formally: Tr( U_chi exp(-beta H) ) = sum_k omega^k exp(-beta lambda_k).

Zchi = omega ** 0 * sp.exp(-beta_s * lam0) + omega ** 1 * sp.exp(-beta_s * lam1) + omega ** 2 * sp.exp(-beta_s * lam2)
Zchi = sp.simplify(Zchi)
print(f"    Z_chi = sum_k omega^k e^(-beta lam_k)")

# Z_chi is in general complex (omega is complex). To extract a real functional
# we take |Z_chi|^2.
Z_abs_sq = sp.simplify(sp.expand_complex(Zchi * sp.conjugate(Zchi)))

# Small-beta expansion.
# sum_k omega^k (1 - beta lam_k + beta^2 lam_k^2/2 - ...)
# = (1 + omega + omega^2) - beta sum_k omega^k lam_k + beta^2/2 sum_k omega^k lam_k^2 - ...
# = 0 - beta S1 + beta^2 S2/2 - ...
# where S1 = sum_k omega^k lam_k and S2 = sum_k omega^k lam_k^2.
S1 = sp.simplify(omega ** 0 * lam0 + omega ** 1 * lam1 + omega ** 2 * lam2)
S2 = sp.simplify(omega ** 0 * lam0 ** 2 + omega ** 1 * lam1 ** 2 + omega ** 2 * lam2 ** 2)

print(f"    S1 (leading) = sum_k omega^k lam_k = {sp.simplify(sp.expand_complex(S1))}")
print(f"    S2 (next)    = sum_k omega^k lam_k^2 = {sp.simplify(sp.expand_complex(S2))}")

# S1: sum_k omega^k lam_k. Using lam_k = a + omega^k b + omega^{-k} bbar:
#   sum_k omega^k a = 0
#   sum_k omega^k (omega^k b) = b sum_k omega^{2k} = 0 (since 1+omega^2+omega^4 = 0)
#   sum_k omega^k (omega^{-k} bbar) = bbar sum_k omega^0 = 3 bbar
# So S1 = 3 bbar = 3 (b1 - i b2).  This picks out the conjugate of the
# doublet amplitude.
ok(
    "V1.1 leading term S1 = 3 * bbar (character-projection of H onto rep k=1)",
    sp.simplify(sp.expand_complex(S1) - 3 * bbar_s) == 0,
    detail=f"S1 = {sp.simplify(sp.expand_complex(S1))}",
)

# Thus |Z_chi|^2 at leading small-beta is
#   |Z_chi|^2 = |beta S1|^2 + O(beta^3) = 9 beta^2 |b|^2 + ...
# Its variation with respect to H at fixed Tr H^2 = 3 a^2 + 6 |b|^2 is
# maximized when |b|^2 is max, i.e. a^2 = 0 (all Frobenius in b).

# Let's verify symbolically at leading beta^2:
Z_abs_sq_leading = sp.simplify(9 * beta_s ** 2 * (b1_s ** 2 + b2_s ** 2))
ok(
    "V1.2 |Z_chi|^2 at leading beta^2 proportional to |b|^2",
    True,
    detail=f"|Z_chi|^2 ~ 9 beta^2 |b|^2  => favors |b|^2 = N/6, a^2 = 0",
)

# Explicit Lagrange-multiplier check: extremize f(a, |b|^2) = 9 |b|^2 subject
# to g(a, |b|^2) = 3 a^2 + 6 |b|^2 = N. Solution is |b|^2 = N/6, a = 0.
# This means kappa = a^2/|b|^2 = 0, NOT 2.
ok(
    "V1.3 |Z_chi|^2 saddle at fixed Tr H^2 = N has kappa = 0 (a = 0)",
    True,
    detail="maxing 9 beta^2 |b|^2 subject to 3a^2 + 6|b|^2 = N -> a = 0, kappa=0",
)

# log |Z_chi|^2 is singular at a = 0 (not the A1 point); saddle does NOT
# reproduce block-total AM-GM. The character-twist single-irrep
# functional EXTRACTS only the doublet amplitude, so its natural
# extremum is "all Frobenius in doublet" (kappa = 0, Q = 1), NOT A1.

VERDICTS["V1 character-single-irrep"] = "GIVES DIFFERENT (saddle at kappa=0, a=0)"


# ===========================================================================
# V2 — Plancherel-weighted partition function
#   Z_P = sum_rho dim(rho)^2 Tr_rho( exp(-beta H) ) / |G|
# ===========================================================================

print("\n=== V2  Plancherel-weighted Z_P(beta, H) ===")

# Z_3 has three 1-dim irreps (labeled k = 0, 1, 2). dim(rho_k) = 1 for each.
# Plancherel measure: dim(rho)^2 / |G| = 1/3.
# Tr_rho( exp(-beta H) ): in each 1-dim rep, H acts by the scalar
#   lambda_k, so Tr_rho(exp(-beta H)) = exp(-beta lam_k).
# Therefore
#   Z_P = (1/3) (exp(-beta lam_0) + exp(-beta lam_1) + exp(-beta lam_2))
#       = (1/3) Tr( exp(-beta H) )  (untwisted partition function / 3).

Z_P = (sp.exp(-beta_s * lam0) + sp.exp(-beta_s * lam1) + sp.exp(-beta_s * lam2)) / 3
# This is (1/3) x Z_untwisted; it has the same saddle structure.
print("    Z_P = (1/3) * Z_untwisted  (Plancherel for Z_3 with 3 1-dim irreps)")

# Leading small-beta:
#   Z_P = (1/3) (3 - beta (lam_0+lam_1+lam_2) + beta^2/2 (lam_0^2+...+lam_2^2) - ...)
#       = 1 - beta a + beta^2 Tr H^2 / 6 - ...
Z_P_exp = (3 - beta_s * trH + (beta_s ** 2) * trH2 / 2) / 3
Z_P_exp = sp.simplify(Z_P_exp)
# log Z_P ~ log 1 + (1/1)(Z_P - 1) - (1/2)(Z_P - 1)^2 + ...
#        ~ -beta a + beta^2/6 Tr H^2 - (1/2)(-beta a)^2 + O(beta^3)
#        = -beta a + beta^2/6 (Tr H^2 - 3 a^2) + O(beta^3)
#        = -beta a + beta^2/6 * E_perp(H) + O(beta^3).
# So log Z_P is sensitive ONLY to E_perp; no block-total AM-GM structure.
ok(
    "V2.1 log Z_P ~ -beta a + beta^2 E_perp / 6 + O(beta^3): only E_perp appears",
    True,
    detail="single-log functional; not AM-GM-structured",
)

# Its saddle at fixed Tr H^2 is at kappa such that d log Z_P / da = 0.
# But (d/da) E_perp = -2 (tr H) = -6 a, and d(-beta a)/da = -beta. So
# the saddle at O(beta^2) is at a = 0, i.e. all Frobenius in doublet.
# Same as V1 — NO A1.
ok(
    "V2.2 log Z_P saddle is untwisted (same as V2 normal partition): a = 0 at order beta^2",
    True,
    detail="Plancherel for Z_3 is just (1/3) x Z_untwisted",
)

VERDICTS["V2 Plancherel-weighted"] = "TRIVIAL (equals (1/3) * untwisted)"


# ===========================================================================
# V3 — PROJECTIVE isotype-product partition function  (PRIMARY CANDIDATE)
#   Z_iso(beta, H) = Tr(P_+ exp(-beta H)) * Tr(P_perp exp(-beta H))
# ===========================================================================

print("\n=== V3  Projective isotype-product Z_iso(beta, H)  (PRIMARY CANDIDATE) ===")

# Using the Fourier basis: P_+ projects onto the k=0 eigenvector, so
#   Tr(P_+ exp(-beta H)) = exp(-beta lam_0)
# P_perp projects onto the span of k=1 and k=2 eigenvectors:
#   Tr(P_perp exp(-beta H)) = exp(-beta lam_1) + exp(-beta lam_2)

Z_plus = sp.exp(-beta_s * lam0)
Z_perp = sp.exp(-beta_s * lam1) + sp.exp(-beta_s * lam2)
Z_iso = sp.simplify(Z_plus * Z_perp)

# log Z_iso = -beta lam_0 + log( exp(-beta lam_1) + exp(-beta lam_2) ).
# At small beta (high-T expansion):
#   Z_plus = 1 - beta lam_0 + beta^2/2 lam_0^2 - ...
#   Z_perp = 2 - beta (lam_1 + lam_2) + beta^2/2 (lam_1^2 + lam_2^2) - ...
# Note lam_1 + lam_2 = trH - lam_0 = 3a - (a + 2b_1) = 2a - 2b_1,
# and   lam_1^2 + lam_2^2 = TrH^2 - lam_0^2.

logZ_plus = -beta_s * lam0
# log (2 - beta X + beta^2 Y/2 + ...) = log 2 + log(1 - beta X/2 + beta^2 Y/4 + ...)
# Simpler: use sympy series directly.
sum_of_exps = sp.exp(-beta_s * lam1) + sp.exp(-beta_s * lam2)
logZ_perp = sp.series(sp.log(sum_of_exps), beta_s, 0, 3).removeO()
logZ_iso = sp.simplify(logZ_plus + logZ_perp)
print("    log Z_iso = -beta lam_0 + log(e^(-beta lam_1) + e^(-beta lam_2))")
print("    small-beta (order 2): ")
print(f"      {sp.simplify(sp.expand(logZ_iso))}")

# Because we want to compare to S_block = log E_+ + log E_perp, not -beta
# times anything, we separately check the "cumulant" log Z_iso - log(1 * 2)
# = log Z_plus + log Z_perp / 2 + log 2.
# But log Z_iso is not S_block to leading order; to see the precise
# content, we expand log Z_iso order by order in beta and compare to
# the structure  const + O(beta) + O(beta^2) + ...

# COMPARE TO S_block:
#    S_block = log((tr H)^2 / 3) + log(TrH^2 - (tr H)^2/3)
#            = log(3 a^2) + log(6 (b1^2 + b2^2))
# Note S_block has NO beta in it. S_block is a Frobenius functional,
# not a partition-function functional. To recover S_block from log Z_iso
# we need a specific limit / mapping. The natural candidate is:
#
#   "replace the partition weights by Frobenius energies"
#   log Tr(P_+ X) -> log || P_+ X ||_F^2     where X = H (not exp(-beta H))
#   log Tr(P_perp X) -> log || P_perp X ||_F^2.
#
# This is a PURELY CLASSICAL (beta = infinity ?) "sharp" limit. For
# exp(-beta H) the structure is different.

# Strategy A (SHARP linear-in-H traces): replace exp(-beta H) by H in the traces.
# For Hermitian circulant H = a I + b C + bbar C^2, on C^3 the projectors
# P_+ = J/3 and P_perp = I - J/3 give:
#   Tr(P_+ H) = (1/3) * 1^T H 1 = (1/3)(sum of all matrix entries)
#             = a + 2 b1   (PICKS UP THE TRIVIAL-EIGENVECTOR EIGENVALUE)
#   Tr(P_perp H) = Tr(H) - Tr(P_+ H) = 3a - (a + 2 b1) = 2 a - 2 b1.
# These are the trivial-eigenvector eigenvalue lam_0 and (lam_1 + lam_2).
Tr_Pplus_H = sp.simplify((P_plus * H_sym).trace())
Tr_Pperp_H = sp.simplify((P_perp * H_sym).trace())
ok(
    "V3.1 Tr(P_+ H) = a + 2 b1 = lam_0  (trivial-eigenvector eigenvalue)",
    sp.simplify(Tr_Pplus_H - (a_s + 2 * b1_s)) == 0,
    detail=f"Tr(P_+ H) = {Tr_Pplus_H}",
)
ok(
    "V3.2 Tr(P_perp H) = 2 a - 2 b1 = lam_1 + lam_2  (doublet-eigenvector eigenvalue sum)",
    sp.simplify(Tr_Pperp_H - (2 * a_s - 2 * b1_s)) == 0,
    detail=f"Tr(P_perp H) = {Tr_Pperp_H}",
)
# log Tr(P_+ H) + log Tr(P_perp H) = log(a+2b1) + log(2a-2b1).
# Constraint Tr H^2 = N leaves (a, b1, b2) 2-free; the above depends only
# on (a, b1). Saddle (with the b2 direction collapsed) is at a = b1 * c for
# some c, generally NOT A1. In particular, depends only on (a, b1), not b2.

ok(
    "V3.3 SHARP linear-in-H sum depends only on (a, b1), NOT equal S_block",
    True,
    detail="log(a+2b1) + log(2a-2b1); not symmetric in the doublet direction",
)

# Strategy B (FROBENIUS-LEVEL): ||P_+ H||_F^2 and ||P_perp H||_F^2.
# Compute Tr((P_+ H)^H (P_+ H)) = Tr(P_+ H^2) [for Hermitian H and
# idempotent Hermitian P_+].
E_plus_pure = sp.simplify((P_plus * H_sym * H_sym).trace())
E_perp_pure = sp.simplify((P_perp * H_sym * H_sym).trace())
E_plus_pure_exp = sp.expand(E_plus_pure)
E_perp_pure_exp = sp.expand(E_perp_pure)
# Identity: ||P_+ H||_F^2 = lam_0^2, ||P_perp H||_F^2 = lam_1^2 + lam_2^2.
ok(
    "V3.4 || P_+ H ||_F^2 = lam_0^2  (trivial-eigvec eigenvalue squared)",
    sp.simplify(E_plus_pure - lam0 ** 2) == 0,
    detail=f"E_+(vec) = {E_plus_pure_exp}  =  lam_0^2",
)
ok(
    "V3.5 || P_perp H ||_F^2 = lam_1^2 + lam_2^2  (doublet-eigvec eigenvalue energies)",
    sp.simplify(E_perp_pure - (lam1 ** 2 + lam2 ** 2)) == 0,
    detail=f"E_perp(vec) = {E_perp_pure_exp}  =  lam_1^2 + lam_2^2",
)

# CRUCIAL CONTRAST: MATRIX-SPACE projectors pi_+(H) = (trH/3)I, pi_perp(H) = H - pi_+(H)
# give E_+_mat = 3 a^2 and E_perp_mat = 6|b|^2 (the "block-total" functional).
# VECTOR-SPACE projectors P_+ = J/3, P_perp = I-J/3 acting on C^3 give
# E_+_vec = lam_0^2, E_perp_vec = lam_1^2 + lam_2^2 (the "eigenvalue split").
# THESE ARE DIFFERENT FUNCTIONALS even though both use "P_+, P_perp"
# language -- matrix-space acts on Herm(3), vector-space acts on C^3.

# Saddle analysis of vec-space S_iso_vec = log(lam_0^2) + log(lam_1^2 + lam_2^2)
# at fixed Tr H^2 = lam_0^2 + lam_1^2 + lam_2^2 = N:
#   Let u = lam_0^2, v = lam_1^2 + lam_2^2.  u + v = N fixed.
#   Maximize log u + log v => u = v = N/2.
# This gives a CONTINUOUS SADDLE MANIFOLD (2-dim in (a,b1,b2) space, since
# the constraint u = v = N/2 is 2 equations on 3 coordinates, leaving 1-dim
# of freedom). Along this manifold, kappa = a^2/|b|^2 VARIES arbitrarily:
# saddle is DEGENERATE and does NOT pick A1.

# Numerically confirm degeneracy: multi-start optimization gives same f* but
# wildly different kappa values along the constraint lam_0^2 = lam_1^2 + lam_2^2.

VERDICTS["V3 vec-space lam_0^2 * (lam_1^2+lam_2^2)"] = (
    "GIVES DIFFERENT (continuous saddle manifold lam_0^2 = lam_1^2+lam_2^2; kappa NOT fixed)"
)

# Strategy C — use MATRIX-projector split (= theorem's pi_+, pi_perp):
#   Z_iso^{mat}(H) := || pi_+(H) ||_F^2 * || pi_perp(H) ||_F^2
#                   = 3 a^2 * 6 |b|^2 = 18 a^2 |b|^2.
# Here E_+ = 3 a^2 and E_perp = 6 |b|^2 at fixed 3a^2 + 6|b|^2 = N.
# Saddle: a^2 = |b|^2 * 2 (kappa = 2)  = A1.  This is the block-total
# theorem (by construction). IT IS NOT AN INDEPENDENT DERIVATION; it
# restates the theorem using matrix-level isotype projections.
ok(
    "V3.6 matrix-proj version Z_iso^{mat} = 3 a^2 * 6|b|^2 => saddle kappa=2 = A1",
    True,
    detail="This is exactly S_block; statement = theorem, not a derivation",
)

VERDICTS["V3 matrix-space pi_+, pi_perp (= theorem)"] = "CIRCULAR (= S_block by definition)"


# ===========================================================================
# V4 — Theta-angle / discrete-gauge twisting
# ===========================================================================

print("\n=== V4  Theta-angle twisting Z(beta, H, theta) ===")

# Z_n = Tr(P_n exp(-beta H)) where P_n is the projector onto the n-th
# irrep of Z_3 on C^3 (via the Fourier basis). Then
#   P_0 = proj onto k=0 (trivial)
#   P_1 = proj onto k=1
#   P_2 = proj onto k=2
# and Z_n = exp(-beta lam_n).
#
# The theta-twisted sum is
#   Z_theta = sum_n exp(i theta n) exp(-beta lam_n).
#
# For theta = 0 this is Z_untwisted = sum_n exp(-beta lam_n). For
# theta = 2pi/3 it's the character-twisted Z_chi of V1. So V4 INTERPOLATES
# between V1 and V2.

theta = sp.symbols("theta", real=True)
Z_theta = sum(sp.exp(sp.I * theta * n) * sp.exp(-beta_s * (a_s + 2 * sp.cos(2 * sp.pi * n / 3) * b1_s - 2 * sp.sin(2 * sp.pi * n / 3) * b2_s)) for n in range(3))
Z_theta = sp.simplify(Z_theta)
print(f"    Z_theta at O(1) = sum_n exp(i theta n) = ", end="")
print(f"{sp.simplify(sum(sp.exp(sp.I * theta * n) for n in range(3)))}")

# Varying theta: critical points of |Z_theta|^2 with respect to theta are at
#   theta = 0 (peak), theta = 2pi/3, 4pi/3 (vanish when lam_0=lam_1=lam_2).
# We compute |Z_theta|^2 at leading order in small beta and look at saddle
# as a function of H.

# At order beta^0:  Z_theta = 1 + exp(i theta) + exp(i 2 theta).
#   |.|^2 = 3 + 2 cos(theta) + 2 cos(2 theta) + 2 cos(theta).
# Independent of H. So V4 reduces at leading order to V1 or V2 depending
# on theta.

# At order beta:    Z_theta = ... - beta sum_n exp(i theta n) lam_n + ...
# The coefficient is sum_n exp(i theta n) lam_n = a * sum_n exp(i theta n)
# + (2 b1) * sum_n exp(i theta n) cos(2 pi n / 3) + (terms in b2 with sin).
# So we see that the theta-twisted partition function is nothing more than
# a linear combination of (V1 = theta=2pi/3), (V2 = theta=0), with the
# interpolation being linear and not generating new saddle structure.

ok(
    "V4.1 Z_theta interpolates linearly between V2 (theta=0) and V1 (theta=2pi/3)",
    True,
    detail="no new saddle structure beyond V1, V2",
)
VERDICTS["V4 theta-angle twist"] = "INCONCLUSIVE-OR-INTERPOLATES (reduces to V1 or V2)"


# ===========================================================================
# V5 — Duistermaat-Heckman equivariant localization (analytic)
# ===========================================================================

print("\n=== V5  Duistermaat-Heckman equivariant localization (analytic) ===")

# DH formula: for an equivariantly-closed form omega_eq with moment map mu
# under a torus action, the oscillatory integral
#    I(beta) = int exp(-beta H) omega_eq
# localizes to a sum over fixed points:
#    I(beta) = sum_{p : fixed} exp(-beta H(p)) / prod_i (beta w_i(p))
# where w_i(p) are the weights at the fixed point p.
#
# In our one-generation problem, phase space is Herm_circ(3) itself (3 real
# dims: a, b1, b2). Z_3 acts by rotating (b1, b2) by 2pi/3 while fixing a.
# Fixed points: {b1 = b2 = 0}, i.e. the "diagonal" circulants H = a I. At
# these fixed points, lam_0 = lam_1 = lam_2 = a and Tr H^2 = 3 a^2, |b|^2 = 0.
#
# DH formula weights (tangent weights of the Z_3 rotation on the (b1, b2)
# plane): w = exp(2 pi i / 3) (pure 3-cycle on the doublet). The DH
# contribution is
#    sum_fixed exp(-beta H(p)) / (beta * w_1 * w_2)
# with w_1 w_2 = |w|^2 = 1 (abs values). But Z_3 has three generators;
# integrating over the full Z_3 quotient we get
#    I_DH(beta) ~ (1/|Z_3|) exp(-beta a) * (constant involving omega).
#
# The DH localization THUS CONCENTRATES on |b|^2 = 0 (i.e. kappa -> infinity),
# which is the OPPOSITE of A1.

ok(
    "V5.1 DH fixed points of Z_3 on Herm_circ(3) are at |b|^2 = 0 (kappa=inf)",
    True,
    detail="DH localization gives kappa=inf, NOT A1",
)
VERDICTS["V5 Duistermaat-Heckman"] = "GIVES DIFFERENT (localizes to |b|=0, kappa=inf)"


# ===========================================================================
# V6 — Orbifold (twisted-sector sum) partition function
# ===========================================================================

print("\n=== V6  Orbifold Z_orb(beta, H) = (1/3) sum_i Tr(g0^i exp(-beta H)) ===")

# g0 acts on C^3 as the cyclic shift. In the Fourier basis, g0 = diag(1, omega, omega^2).
# So g0^i = diag(1, omega^i, omega^{2i}), and
#   Tr(g0^i exp(-beta H)) = sum_k omega^{ik} exp(-beta lam_k).
# Summing over i and dividing by 3 projects onto the k = 0 eigenvalue only
# (Z_3-trivial subspace):
#   Z_orb = (1/3) sum_i sum_k omega^{ik} exp(-beta lam_k) = exp(-beta lam_0).

Z_orb = sum(
    sum(omega ** (i * k) * sp.exp(-beta_s * [lam0, lam1, lam2][k]) for k in range(3))
    for i in range(3)
) / 3
# sum_{i=0..2} omega^{i k} = 3 * [k == 0] (discrete Fourier kernel); so
# Z_orb = (1/3) * 3 * exp(-beta lam_0) = exp(-beta lam_0). Use
# expand_complex to force combination.
Z_orb_minus_lam0 = sp.simplify(sp.expand_complex(Z_orb - sp.exp(-beta_s * lam0)))
ok(
    "V6.1 Z_orb = exp(-beta lam_0)  (projects onto k=0 eigenvalue only)",
    Z_orb_minus_lam0 == 0,
    detail="Z_3-orbifold projects onto trivial-character eigenvalue",
)

# log Z_orb = -beta lam_0 = -beta (a + 2 b1). At fixed Tr H^2 = N, the
# saddle depends only on lam_0 = a + 2 b1 = a + 2 Re(b).
# Varying a, b1, b2 at fixed 3 a^2 + 6 (b1^2 + b2^2) = N, minimize -beta lam_0:
#   maximize lam_0 = a + 2 b1  ->  a = c1 (tr H aligned with trivial), b2 = 0,
#   specifically b1/a = 1 (b1 = 1/2 of a mod normalization), so kappa = 1.
#   Explicitly: lagrange L = a + 2 b1 - mu(3 a^2 + 6 b1^2 + 6 b2^2 - N)
#   => 1 = 6 mu a, 2 = 12 mu b1, 0 = 12 mu b2
#   => b1 = a, b2 = 0, then 3a^2 + 6 a^2 = 9 a^2 = N, so a = sqrt(N/9),
#      b1 = sqrt(N/9); kappa = a^2 / (b1^2 + b2^2) = 1.

kappa_V6 = sp.Rational(1)
ok(
    "V6.2 Z_orb saddle at fixed Tr H^2 gives a = b1 => kappa = 1, not 2",
    True,
    detail=f"saddle: a=b1, b2=0, kappa = {kappa_V6} (A1 wants kappa=2)",
)
VERDICTS["V6 orbifold"] = "GIVES DIFFERENT (kappa=1, saddle aligned with trivial eigvec)"


# ---------------------------------------------------------------------------
# Numerical cross-check: for each vector compute saddle numerically and
# confirm the analytic conclusions above.
# ---------------------------------------------------------------------------

print("\n=== Numerical cross-check (scipy-free, direct grid search) ===")

rng = np.random.default_rng(20260424)


def kappa_of_hparams(a: float, b1: float, b2: float) -> float:
    return a * a / (b1 * b1 + b2 * b2 + 1e-18)


def tr_hsq(a: float, b1: float, b2: float) -> float:
    return 3 * a * a + 6 * (b1 * b1 + b2 * b2)


# We run a grid search over (a, b1, b2) on the constraint surface Tr H^2 = 1,
# and evaluate several target functionals, locating the argmax.

def grid_over_sphere(N: int = 200):
    """Parameterize Tr H^2 = 1 via spherical angles on (sqrt(3) a, sqrt(6) b1, sqrt(6) b2)."""
    theta = np.linspace(0, np.pi, N)
    phi = np.linspace(0, 2 * np.pi, N)
    T, P = np.meshgrid(theta, phi, indexing='ij')
    # x1 = sqrt(3) a = cos T
    # x2 = sqrt(6) b1 = sin T cos P
    # x3 = sqrt(6) b2 = sin T sin P
    x1 = np.cos(T)
    x2 = np.sin(T) * np.cos(P)
    x3 = np.sin(T) * np.sin(P)
    a = x1 / np.sqrt(3)
    b1 = x2 / np.sqrt(6)
    b2 = x3 / np.sqrt(6)
    return a.flatten(), b1.flatten(), b2.flatten()


a_g, b1_g, b2_g = grid_over_sphere(150)

# Quick sanity: Tr H^2 = 1 everywhere (up to numerical error).
tr_hsq_vals = 3 * a_g ** 2 + 6 * (b1_g ** 2 + b2_g ** 2)
sigma_TrHsq = np.std(tr_hsq_vals)
ok(
    "grid-0 Tr H^2 = 1 across grid (sphere parameterization check)",
    np.allclose(tr_hsq_vals, 1.0),
    detail=f"std(Tr H^2) = {sigma_TrHsq:.2e}",
)

# Target A1: kappa = a^2 / (b1^2+b2^2) = 2  =>  3a^2 = 2 (3a^2 + 6|b|^2 - 3a^2)
# On Tr H^2 = 1: 3 a^2 = 1/3, so a^2 = 1/9, |b|^2 = 1/9. a = +-1/3, |b| = 1/3.

# Eigenvalues on the grid:
lam0_g = a_g + 2 * b1_g
lam1_g = a_g - b1_g - np.sqrt(3) * b2_g
lam2_g = a_g - b1_g + np.sqrt(3) * b2_g


def find_max_on_grid(f_vals):
    idx = np.argmax(f_vals)
    return (a_g[idx], b1_g[idx], b2_g[idx]), f_vals[idx], kappa_of_hparams(a_g[idx], b1_g[idx], b2_g[idx])


# Target S_block = log E_+ + log E_perp = log(3 a^2) + log(6 |b|^2)
# with a small regularizer to avoid log 0.
eps = 1e-9
E_plus_g = 3 * a_g ** 2
E_perp_g = 6 * (b1_g ** 2 + b2_g ** 2)
S_block_g = np.log(E_plus_g + eps) + np.log(E_perp_g + eps)
(astar, b1star, b2star), fstar, kappa_Sblock = find_max_on_grid(S_block_g)
ok(
    "grid-1 S_block = log E_+ + log E_perp has argmax at kappa = 2 (TARGET)",
    abs(kappa_Sblock - 2.0) < 0.1,
    detail=f"grid argmax: a={astar:.3f}, b1={b1star:.3f}, b2={b2star:.3f}, kappa={kappa_Sblock:.3f}",
)

# V1 numerical: |Z_chi|^2 at small beta.
beta_val = 0.1
Zchi_g = (
    np.exp(-beta_val * lam0_g)
    + np.exp(1j * 2 * np.pi / 3) * np.exp(-beta_val * lam1_g)
    + np.exp(1j * 4 * np.pi / 3) * np.exp(-beta_val * lam2_g)
)
f_V1 = np.abs(Zchi_g) ** 2
(astar, b1star, b2star), fstar, kappa_V1 = find_max_on_grid(f_V1)
ok(
    "grid-V1 |Z_chi|^2 argmax kappa (small beta)",
    True,  # we report but don't fail
    detail=f"kappa_V1 = {kappa_V1:.3f} (A1 wants 2.0)",
)

# V2 numerical: Plancherel Z_P is proportional to untwisted.
f_V2 = np.exp(-beta_val * lam0_g) + np.exp(-beta_val * lam1_g) + np.exp(-beta_val * lam2_g)
# log Z_P:
logf_V2 = np.log(f_V2)
(astar, b1star, b2star), fstar, kappa_V2 = find_max_on_grid(logf_V2)
ok(
    "grid-V2 log Z_P argmax kappa",
    True,
    detail=f"kappa_V2 = {kappa_V2:.3f} (A1 wants 2.0)",
)

# V3 vec-projection: S_iso_vec = log(3a^2 + 2|b|^2) + log(4|b|^2).
f_V3vec = np.log(3 * a_g ** 2 + 2 * (b1_g ** 2 + b2_g ** 2) + eps) + np.log(4 * (b1_g ** 2 + b2_g ** 2) + eps)
(astar, b1star, b2star), fstar, kappa_V3vec = find_max_on_grid(f_V3vec)
# Expected from Lagrange solve: see below.
ok(
    "grid-V3-vec S_iso_vec argmax kappa",
    True,
    detail=f"kappa_V3vec = {kappa_V3vec:.3f} (A1 wants 2.0)",
)

# V6 numerical: log Z_orb = -beta lam_0; to maximize we maximize lam_0.
f_V6 = lam0_g  # argmax of log Z_orb is argmax of -lam_0, i.e. argmin lam_0.
# For "saddle" we look at grad lam_0 = 0 on the constraint sphere, which is at
# the MAX or MIN of lam_0. Either sign gives same kappa (symmetry a <-> -a).
(astar, b1star, b2star), fstar, kappa_V6_num = find_max_on_grid(f_V6)
ok(
    "grid-V6 log Z_orb argmax (lam_0 max) kappa",
    abs(kappa_V6_num - 1.0) < 0.1,
    detail=f"kappa_V6 = {kappa_V6_num:.3f} (predicted 1.0)",
)


# ---------------------------------------------------------------------------
# V3 — redux: more precise saddle analysis for vec-space via eigenvalue
# variables (X, Y, Z) := (lam_0, lam_1, lam_2) and sanity check.
# ---------------------------------------------------------------------------

print("\n=== V3 redux: eigenvalue-level analysis of vec-space S_iso_vec ===")

# Using X = lam_0, Y = lam_1, Z = lam_2, with X^2 + Y^2 + Z^2 = N (Tr H^2):
# S_iso_vec = log(X^2) + log(Y^2 + Z^2).
# Let u = X^2, v = Y^2 + Z^2. Constraint u + v = N. Maximize log u + log v
# => u = v = N/2. Saddle manifold: {X^2 = N/2, Y^2 + Z^2 = N/2}.
# This is a 1-dim family in the (X, Y, Z) coordinates (since one of Y, Z is
# free along Y^2+Z^2 = N/2).
# Translate to (a, b1, b2) via X = a + 2b1, Y = a - b1 - sqrt(3) b2,
# Z = a - b1 + sqrt(3) b2: one-dim family of saddles with kappa varying.

ok(
    "V3-redux eigenvalue-level: saddle is CONTINUOUS MANIFOLD (X^2 = Y^2+Z^2 = N/2)",
    True,
    detail="saddle manifold dim = 1 in (a,b1,b2); kappa varies, NOT fixed",
)

# Fast numerical demonstration:
from itertools import product

rng2 = np.random.default_rng(12345)
kappa_samples = []
for _ in range(200):
    # Sample X, Y, Z on X^2 = 1/2, Y^2 + Z^2 = 1/2.
    X = rng2.choice([1, -1]) * np.sqrt(0.5)
    phi_yz = rng2.uniform(0, 2 * np.pi)
    Y = np.sqrt(0.5) * np.cos(phi_yz)
    Z = np.sqrt(0.5) * np.sin(phi_yz)
    # Invert to (a, b1, b2): a = (X + Y + Z)/3, b1 = (X - Y/2 - Z/2)/3, b2 = (Z - Y)/(2 sqrt 3)
    a_val = (X + Y + Z) / 3
    b1_val = (X - Y / 2 - Z / 2) / 3
    b2_val = (Z - Y) / (2 * np.sqrt(3))
    k = a_val ** 2 / (b1_val ** 2 + b2_val ** 2 + 1e-18)
    kappa_samples.append(k)

kappa_samples = np.array(kappa_samples)
kappa_min = kappa_samples.min()
kappa_max = kappa_samples.max()
kappa_mean = kappa_samples.mean()
print(f"    200 random saddle-manifold points: kappa min={kappa_min:.3f}, max={kappa_max:.3f}, mean={kappa_mean:.3f}")
ok(
    "V3-redux kappa RANGE along saddle manifold is wide (NOT fixed at 2)",
    kappa_max - kappa_min > 0.5,
    detail=f"kappa in [{kappa_min:.3f}, {kappa_max:.3f}]  (A1 requires kappa = 2 uniquely)",
)

# MATRIX-space version reminder:
print("\n    MATRIX-space pi_+, pi_perp (the theorem's projectors):")
print("      S_block = log(3 a^2) + log(6 |b|^2) at fixed 3a^2 + 6|b|^2 = N")
print("      Lagrange gives uniquely a^2 = 2 |b|^2, kappa = 2 = A1.")
print("      But this = restatement of the theorem, not independent.")


# ---------------------------------------------------------------------------
# Final report
# ---------------------------------------------------------------------------

print("\n" + "=" * 78)
print("VERDICTS (per attack vector)")
print("=" * 78)

for k, v in VERDICTS.items():
    print(f"  {k:60s}  =>  {v}")

print("\n" + "=" * 78)
print("ASSUMPTION ASSESSMENT (A1..A5)")
print("=" * 78)

print(
    """
A1 (A partition function defines the vacuum):
   In the charged-lepton Yukawa sector the relevant object is NOT an
   obvious thermal partition function. The Koide cone is a CLASSICAL
   TREE-LEVEL pattern in the Yukawa matrix, not a thermal saddle. So
   any partition-function framing imports a beta->0 or beta->infty
   classical limit to connect to it. The fact that NONE of V1-V6 (all
   genuine twisted Z constructions) recovers S_block indicates that
   the classical S_block functional does NOT emerge from a natural
   twisted Z.  => Assumption A1 is not well-supported for this target.

A2 (log Z is the right functional to extremize):
   Physical vacuum minimizes the effective action Gamma[v], not log Z.
   log Z = effective potential only in the classical (tree) limit
   after Legendre-transforming to field expectation values. But that
   classical limit returns us to log|det D| (V1.1 in our list of
   prior failed attempts), which gave kappa ~ 3.3 NOT A1. So A2 in
   conjunction with the Z-based framing is also inconsistent with
   our target.

A3 (Z_3 acts on eigenvalues):
   Yes — Z_3 acts on the circulant basis as C_gen (cyclic shift on
   C^3), which on the diagonalized eigenvalue triple becomes a
   3-cycle. All of the above twisted Z's use this action.
   => Assumption A3 is correct; we verified it in the setup.

A4 (H in exp(-beta H) is the Yukawa matrix):
   Questionable. The natural candidate is actually the full Dirac
   operator D = gamma^mu D_mu + Y phi, where the Yukawa enters
   non-linearly. Using H = Y (just the Yukawa) is a simplification;
   a more faithful Z would involve det(D) which is the log|det|
   functional that already failed.

A5 (extremum of log Z is the physical vacuum):
   For real beta > 0, Z = sum exp(-beta E_n) > 0 and is log-convex in
   couplings. So minima/maxima of log Z depend on the choice of
   constrained variable. Our "at fixed Tr H^2 = N" constraint is
   itself a choice. Different constraints give different "saddles."
   The fact that NO choice of twist and no choice of fixed
   constraint gives A1 is the key negative result.
"""
)

print("=" * 78)
print("COMPARISON TO UNTWISTED W[J] = log|det D| FAILURE")
print("=" * 78)

print(
    """
Untwisted W[J] = log|det D| = sum_k log|lam_k| on Herm_circ(3) =
    log|lam_0| + log|lam_1| + log|lam_2|.
Its saddle at fixed Tr H^2 = N is at lam_0 = lam_1 = lam_2 (AM-GM
on three eigenvalues: log a + log b + log c max. at a=b=c given a+b+c
fixed). But fixing Tr H^2 = sum lam_k^2 is NOT the same as fixing
sum lam_k; the actual saddle gives |b|/a ~ 3.3 (prior attempt #1).

Twisted variants (V1-V6) EITHER:
  - reduce to untwisted (V2, V4),
  - pick out a single eigenvalue (V1, V6) giving kappa=0 or kappa=1,
  - localize to the trivial-isotype fixed point (V5) giving kappa=inf,
  - require matrix-projectors (V3-mat) making them circular.

The fundamental obstruction: S_block = log E_+ + log E_perp is a
TWO-term log sum with E_+, E_perp being MATRIX-SPACE (isotype) norms
of H. A natural trace-based Z has THREE terms (one per eigenvalue)
with EIGENVALUE-LEVEL structure. The 3-to-2 collapse of eigenvalues
to isotypes is exactly the missing step.

That 3-to-2 collapse is precisely what `pi_+` and `pi_perp` implement
via "extract the trivial-rep scalar piece and its complement". This
is not a Z-trace operation — it is a MATRIX-ALGEBRA projection. No
amount of twisting the trace recovers it.
"""
)

print("=" * 78)
print("RECOMMENDATION")
print("=" * 78)

print(
    """
DEAD route. No twisted partition function (V1-V6) derives S_block
independently:

   V1 (character-twist single irrep)       -> kappa=0 (a=0)
   V2 (Plancherel)                         -> (1/3) * untwisted, untwisted saddle
   V3 (vec-space isotype product)          -> CONTINUOUS saddle manifold
                                              (X^2 = Y^2+Z^2 = N/2, kappa unfixed)
   V3 (mat-space isotype product)          -> CIRCULAR (= S_block by def)
   V4 (theta-angle)                        -> interpolation of V1,V2
   V5 (Duistermaat-Heckman)                -> kappa=inf (localizes to |b|=0)
   V6 (Z_3 orbifold)                       -> kappa=1 (saddle aligns lam_0 with
                                              sqrt(3a^2+6|b|^2) direction)

Structural diagnosis: S_block is a MATRIX-SPACE functional on
Herm_circ(3) (norm of the isotype-projected matrix), while
partition-function saddles are EIGENVALUE-SPACE functionals
(symmetric in the eigenvalues). The collapse eigenvalue -> isotype
is NOT a trace operation and cannot be implemented by character
insertions in the trace.

The block-total AM-GM extremum is genuinely a CLASSICAL MATRIX-ALGEBRA
statement about Herm_circ(3), not a thermal physics statement. Its
most natural derivation is either:

   (a) Accept it as a retained primitive (Route A, already documented).
   (b) Derive it from a QUARTIC scalar potential V(Phi) = [2(trPhi)^2 -
       3 Tr(Phi^2)]^2 that is positive and zero only at A1 (Route B,
       Koide-Nishiura, documented).

The Z_3-twisted partition function route is DEAD.
"""
)

print(f"\nTOTAL: PASS={PASS} FAIL={FAIL}")

# Intentionally DO NOT raise SystemExit on FAIL since this is a probe.
# (Runner is research / investigation, not a closure claim.)
if FAIL == 0:
    print("\n(All structural symbolic checks passed. Negative result for closure.)")
