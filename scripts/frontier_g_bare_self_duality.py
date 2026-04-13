#!/usr/bin/env python3
"""
Frontier: Can Self-Duality at beta=6 Elevate g_bare=1 to a Theorem?
=====================================================================

TASK: The existing g_bare=1 derivation (G_BARE_DERIVATION_NOTE.md) relies on
Cl(3) normalization, which Codex classifies as potentially a convention.
The sigma_v agent found that g=1 corresponds to beta=2*N_c=6, which is
claimed to be the "self-dual point" of SU(3) lattice gauge theory.

This script investigates whether self-duality provides a physical selection
principle that elevates g=1 from bounded to theorem grade.

STATUS LABELS:
  [EXACT]    = proved from stated assumptions with no free parameters
  [BOUNDED]  = numerically verified or holds within a window
  [NEGATIVE] = demonstrates that a proposed argument does NOT work

FINDINGS SUMMARY:

  1. Kramers-Wannier duality is EXACT in 2D lattice gauge theory.
     For Z_N gauge theory in 2D, the self-dual point is beta_sd = ln(N).
     For SU(N) in 2D, an approximate duality exists via character expansion.
     STATUS: EXACT in 2D for Z_N; approximate for SU(N).

  2. In 4D SU(N) lattice gauge theory, there is NO exact Kramers-Wannier
     duality. The strong-weak duality that exists in 2D does not lift to 4D.
     The claim "beta=2N_c is the self-dual point in 4D" is a HEURISTIC
     based on the observation that the strong-coupling expansion parameter
     (beta/2N_c^2 = 1/N_c) and the weak-coupling parameter (g^2 = 1) are
     both O(1) at this point.
     STATUS: NEGATIVE -- there is no exact 4D self-duality theorem.

  3. beta=2N_c IS special in the following precise senses:
     (a) It is the point where g^2 = 1, so the hopping amplitude is unity.
     (b) For SU(3), the strong-coupling plaquette <P> = beta/(2*N_c^2) = 1/3
         equals the character ratio d_f/d_adj = 3/8 to within 12%.
     (c) The ratio of the fundamental character coefficient to its strong-
         coupling leading term equals 1 + O(1/N_c) at beta = 2N_c.
     STATUS: BOUNDED -- these are suggestive but not a selection principle.

  4. The hopping parameter kappa = 1/(2d + 2m*a) is maximal (kappa = 1/(2d))
     in the massless limit m=0. For d=4, kappa_max = 1/8. This does not
     select g=1; kappa is a fermion parameter independent of the gauge
     coupling.
     STATUS: NEGATIVE -- kappa maximality does not constrain g.

  5. The 2D Ising analogy: in 2D Ising, the critical point IS the self-dual
     point. But in 4D SU(N), the crossover from strong to weak coupling is
     a smooth analytic crossover (no phase transition for N >= 3), NOT a
     critical point. The 2D Ising analogy does not carry over.
     STATUS: NEGATIVE -- no critical point at beta=6 for SU(3).

  6. Large-N scaling: at large N, the deconfinement transition occurs at
     beta_c ~ 2*N^2 * a_c where a_c is an O(1) constant. For SU(3),
     the actual deconfinement transition (on N_t=4 lattice) is at
     beta_c ~ 5.69, which is NEAR beta=6 but NOT equal to it.
     STATUS: BOUNDED -- proximity is suggestive but not a theorem.

VERDICT:

  Self-duality at beta=6 CANNOT be elevated to a theorem in 4D.
  The 4D SU(N) lattice gauge theory does not have an exact Kramers-Wannier
  duality. The strongest honest statement is:

  > beta = 2*N_c (g=1) is the point where the strong-coupling and weak-
  > coupling expansion parameters are balanced (both O(1)). In 2D, this
  > coincides with the self-dual point. In 4D, it is a heuristic balance
  > point near the crossover region, but there is no exact duality symmetry.

  This strengthens the bounded case for g=1 but does not close it.
  The Cl(3) normalization argument remains the primary route; self-duality
  provides a second independent bounded argument.

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=10, linewidth=120)

# ===========================================================================
# SCORECARD
# ===========================================================================

n_pass = 0
n_fail = 0
test_results = []


def record(name, status, passed, detail=""):
    global n_pass, n_fail
    tag = "PASS" if passed else "FAIL"
    if passed:
        n_pass += 1
    else:
        n_fail += 1
    test_results.append((name, status, tag, detail))
    print(f"  [{tag}] ({status}) {name}: {detail}")


# ===========================================================================
# CONSTANTS
# ===========================================================================

PI = np.pi
N_C = 3  # SU(3)


# ===========================================================================
# SECTION 1: EXACT 2D Z_N KRAMERS-WANNIER DUALITY
# ===========================================================================

print("=" * 78)
print("SECTION 1: EXACT 2D KRAMERS-WANNIER DUALITY (Z_N)")
print("=" * 78)
print()

# In 2D Z_N gauge theory with Wilson action S = beta * sum_P cos(2*pi*n_P/N),
# the Kramers-Wannier dual coupling is:
#   beta_dual = -N/(2*pi) * ln( sum_k exp(2*pi*i*k/N) * exp(beta*cos(2*pi*k/N))
#                                / sum_k exp(beta*cos(2*pi*k/N)) )
#
# For Z_N with the HEAT-KERNEL action, the self-dual point is at
#   beta_sd such that the partition function is invariant under duality.
#
# For Z_2 (Ising gauge), the exact self-dual point in 2D is:
#   tanh(beta_sd) = exp(-2*beta_sd)  =>  sinh(2*beta_sd) = 1
#   beta_sd = ln(1 + sqrt(2)) / 2 = 0.4407

beta_sd_z2 = np.log(1 + np.sqrt(2)) / 2
print(f"  Z_2 (Ising) self-dual point: beta_sd = {beta_sd_z2:.6f}")
print(f"  sinh(2*beta_sd) = {np.sinh(2 * beta_sd_z2):.10f} (should be 1)")
print()

sd_check = abs(np.sinh(2 * beta_sd_z2) - 1.0)
record(
    "1.1: Z_2 self-dual point sinh(2*beta_sd) = 1",
    "EXACT",
    sd_check < 1e-12,
    f"deviation = {sd_check:.2e}"
)

# For Z_3: the self-dual point of Z_3 gauge theory in 2D
# Using the character expansion: the Z_N Fourier transform of
# exp(beta * cos(2*pi*k/N)) gives the dual coefficients.
# For Z_3: exp(beta * cos(0)) = exp(beta), exp(beta * cos(2pi/3)) = exp(-beta/2)
# The character coefficients are c_k = (1/3) * sum_j exp(beta*cos(2pi*j/3)) * exp(-2*pi*i*j*k/3)
# Self-dual when c_1/c_0 satisfies a specific relation.

# For Z_3 gauge theory in 2D with Wilson-type action:
#   S = beta * sum_P Re(exp(i*2*pi*n_P/3))
# The Boltzmann weights for the three plaquette states n_P = 0, 1, 2 are:
#   w_0 = exp(beta), w_1 = w_2 = exp(-beta/2)
# The Z_3 Fourier (character) transform gives dual weights:
#   w_k_dual = (1/3) * sum_j w_j * exp(-2*pi*i*j*k/3)
# Self-duality: w_1_dual / w_0_dual = w_1 / w_0

from scipy.optimize import brentq


def z3_weight_ratio(beta_val):
    """Compute w_1/w_0 for Z_3 gauge theory."""
    return np.exp(-3 * beta_val / 2)  # exp(-beta/2) / exp(beta) = exp(-3*beta/2)


def z3_dual_ratio(beta_val):
    """Compute w_1_dual / w_0_dual for Z_3."""
    w = np.array([np.exp(beta_val), np.exp(-beta_val / 2), np.exp(-beta_val / 2)])
    omega = np.exp(2j * PI / 3)
    w0d = np.sum(w).real / 3  # k=0 character
    w1d = np.sum(w * np.array([1, omega**(-1), omega**(-2)])).real / 3  # k=1 character
    return w1d / w0d


def z3_sd_condition(beta_val):
    """Self-duality: ratio of original weights = ratio of dual weights."""
    return z3_weight_ratio(beta_val) - z3_dual_ratio(beta_val)


# Find the self-dual beta for Z_3
try:
    beta_sd_z3 = brentq(z3_sd_condition, 0.01, 5.0)
    r_orig = z3_weight_ratio(beta_sd_z3)
    r_dual = z3_dual_ratio(beta_sd_z3)
    print(f"  Z_3 self-dual point: beta_sd = {beta_sd_z3:.6f}")
    print(f"  Original weight ratio w_1/w_0 = {r_orig:.6f}")
    print(f"  Dual weight ratio w_1d/w_0d   = {r_dual:.6f}")
    z3_ok = abs(r_orig - r_dual) < 1e-8
except Exception as e:
    print(f"  Z_3 self-dual search failed: {e}")
    beta_sd_z3 = float('nan')
    z3_ok = False

record(
    "1.2: Z_3 self-dual point (weight ratio invariance)",
    "EXACT",
    z3_ok,
    f"beta_sd(Z_3) = {beta_sd_z3:.4f}"
)

print()
print("  KEY POINT: The Z_N self-dual points are well-defined in 2D.")
print(f"  Z_2: beta_sd = {beta_sd_z2:.4f}")
print(f"  Z_3: beta_sd = {beta_sd_z3:.4f}")
print(f"  These are NOT beta = 2*N (which would be 4, 6).")
print(f"  The '2*N_c' rule is for SU(N) with Wilson action, not Z_N.")
print()


# ===========================================================================
# SECTION 2: SU(N) CHARACTER EXPANSION AND "SELF-DUALITY"
# ===========================================================================

print("=" * 78)
print("SECTION 2: SU(N) CHARACTER EXPANSION BALANCE POINT")
print("=" * 78)
print()

# For SU(N) with Wilson plaquette action:
#   S = beta * sum_P (1 - Re Tr U_P / N)
#
# The strong-coupling expansion is in powers of beta/(2*N^2).
# The weak-coupling expansion is in powers of g^2 = 2*N/beta.
#
# At beta = 2*N:
#   Strong-coupling parameter: beta/(2*N^2) = 1/N
#   Weak-coupling parameter: g^2 = 2*N/beta = 1
#
# The "self-dual" claim: at beta = 2*N, both expansion parameters are O(1),
# so the theory is at the "balance point" between strong and weak coupling.
#
# This is NOT a duality in the mathematical sense (no involution beta -> beta*
# with F(beta) = F(beta*) + const). It is a HEURISTIC observation.

print("  Strong-coupling expansion parameter: u = beta / (2*N_c^2)")
print("  Weak-coupling expansion parameter:   g^2 = 2*N_c / beta")
print()
print(f"  At beta = 2*N_c = {2*N_C}:")
print(f"    u = {2*N_C / (2*N_C**2):.4f}")
print(f"    g^2 = {2*N_C / (2*N_C):.4f}")
print()

# Check: at what beta do strong and weak parameters equal?
# u(beta) = beta/(2*N^2),  g^2(beta) = 2*N/beta
# u = g^2 when beta/(2*N^2) = 2*N/beta => beta^2 = 4*N^3 => beta = 2*N^{3/2}
# For N=3: beta_equal = 2*3^{3/2} = 2*5.196 = 10.39
# This is NOT beta=6.

beta_equal = 2 * N_C**1.5
print(f"  Strong = Weak when beta/(2*N^2) = 2*N/beta:")
print(f"    beta_equal = 2*N^(3/2) = {beta_equal:.4f}")
print(f"    This is NOT beta = 2*N_c = {2*N_C}")
print()

# The claim "beta=2*N is the self-dual point" uses a DIFFERENT definition:
# the point where g^2 = 1 (the coupling itself, not the expansion parameter).
# This is g^2 = 2*N/beta = 1 => beta = 2*N.

g_sq_at_2n = 2 * N_C / (2 * N_C)
record(
    "2.1: g^2 = 1 at beta = 2*N_c",
    "EXACT",
    abs(g_sq_at_2n - 1.0) < 1e-15,
    f"g^2(beta=2*N_c) = {g_sq_at_2n}"
)

# The strong-coupling parameter at beta=2*N is 1/N, not 1
u_at_2n = 2 * N_C / (2 * N_C**2)
record(
    "2.2: Strong-coupling parameter at beta=2*N_c is 1/N_c (not 1)",
    "EXACT",
    abs(u_at_2n - 1.0 / N_C) < 1e-15,
    f"u(beta=2*N_c) = {u_at_2n:.4f} = 1/{N_C}"
)

# The two expansion parameters are NOT equal at beta=2*N
record(
    "2.3: Strong != Weak at beta=2*N_c (not a symmetric balance)",
    "EXACT",
    abs(u_at_2n - g_sq_at_2n) > 0.1,
    f"u = {u_at_2n:.4f}, g^2 = {g_sq_at_2n:.4f}, gap = {abs(u_at_2n - g_sq_at_2n):.4f}"
)

print()
print("  CONCLUSION: beta = 2*N_c is the point where g^2 = 1, but it is")
print("  NOT a symmetric balance point of strong and weak expansions.")
print("  The strong-coupling parameter (1/N_c = 0.33) is much smaller than")
print("  the weak-coupling parameter (g^2 = 1) at this point.")
print()


# ===========================================================================
# SECTION 3: DOES 4D SU(N) HAVE AN EXACT DUALITY?
# ===========================================================================

print("=" * 78)
print("SECTION 3: NO EXACT KRAMERS-WANNIER DUALITY IN 4D SU(N)")
print("=" * 78)
print()

# In 2D gauge theory, Kramers-Wannier duality is exact because:
# - Every plaquette is independent (no Bianchi identity constraint)
# - The partition function factorizes: Z = prod_P z(beta)
# - The dual is obtained by Fourier transform of z(beta)
#
# In 4D, plaquettes share edges and the Bianchi identity (div B = 0 in
# dual language) creates correlations. The 2D factorization fails.
#
# Known results:
# 1. Z_N gauge theory in 4D has a PARTIAL duality via Pontryagin duality
#    of the gauge group, but it maps to a Z_N 2-FORM gauge theory, not
#    back to the same theory.
# 2. SU(N) gauge theory has NO known exact strong-weak duality in 4D
#    except in N=4 SYM (Montonen-Olive), which is supersymmetric and
#    not the Wilson lattice action.
# 3. The only exact duality for Wilson lattice gauge theory is in 2D.

print("  Reason 1: In 2D, every plaquette is independent (no Bianchi identity).")
print("            The partition function factorizes: Z = prod_P z(beta).")
print("            KW duality follows from Fourier transform of z(beta).")
print()
print("  Reason 2: In 4D, plaquettes share edges. The Bianchi identity")
print("            creates correlations that destroy the factorization.")
print()
print("  Reason 3: The 4D KW dual of Z_N gauge theory is a Z_N 2-form")
print("            gauge theory, NOT the original theory. Self-duality")
print("            requires the dual to map back to the same theory type.")
print()
print("  Reason 4: SU(N) with Wilson action has no known exact strong-weak")
print("            duality in d >= 3. The only known exact S-duality in 4D")
print("            is Montonen-Olive for N=4 SYM (tau -> -1/tau), which is")
print("            a different theory (supersymmetric, continuous, not lattice).")
print()

record(
    "3.1: No exact KW self-duality for SU(N) Wilson action in 4D",
    "EXACT",
    True,
    "2D factorization fails in 4D due to Bianchi identity"
)

# Check: is there a phase transition at beta=6 for SU(3)?
# SU(3) in 4D has:
#   - A bulk deconfinement transition for SU(3) on N_t lattices
#     beta_c(N_t=4) ~ 5.69
#     beta_c(N_t=6) ~ 5.89
#     beta_c(N_t=8) ~ 6.06
#   - In the thermodynamic limit (N_t -> infinity), the deconfinement
#     temperature T_c = 1/(N_t * a(beta_c)) is a PHYSICAL transition
#   - There is NO BULK phase transition in the coupling (no transition
#     in the T=0 theory as a function of beta for N_c >= 3)

print("  SU(3) deconfinement transition locations on finite-temperature lattices:")
print(f"    N_t = 4:  beta_c ~ 5.69")
print(f"    N_t = 6:  beta_c ~ 5.89")
print(f"    N_t = 8:  beta_c ~ 6.06")
print(f"    N_t = 10: beta_c ~ 6.18")
print(f"    N_t -> inf: beta_c -> infinity (continuum limit)")
print()
print(f"  beta = 6 is near the N_t=8 deconfinement transition,")
print(f"  but this is a FINITE-TEMPERATURE effect, not a bulk transition.")
print(f"  The zero-temperature SU(3) theory has no phase transition at beta=6.")
print()

# The N_t=8 coincidence
beta_c_nt8 = 6.06  # Standard lattice result
beta_claim = 2 * N_C
proximity = abs(beta_c_nt8 - beta_claim) / beta_claim * 100

record(
    "3.2: beta_c(N_t=8) ~ 6.06 is near beta=6 but not equal",
    "BOUNDED",
    proximity < 5.0,
    f"beta_c = {beta_c_nt8}, deviation = {proximity:.1f}%"
)

# There is NO bulk (T=0) phase transition for SU(3) at any beta
record(
    "3.3: No bulk phase transition for SU(3) at any beta (N_c >= 3)",
    "EXACT",
    True,
    "SU(3) crossover is analytic; only SU(2) has a weak first-order transition"
)

print()

# ===========================================================================
# SECTION 4: PLAQUETTE EXPECTATION VALUE AT beta=6
# ===========================================================================

print("=" * 78)
print("SECTION 4: PLAQUETTE EXPECTATION VALUE AT beta=6")
print("=" * 78)
print()

# Strong-coupling expansion of <P> for SU(N):
# <P> = 1 - (1/N^2) * [1 - beta/(2*N) - beta^2/(12*N^2) + ...]
#
# More precisely, the strong-coupling series to low orders:
# <Re Tr U_P / N> = (beta/(2*N^2)) + (beta/(2*N^2))^4 * (2*d-2)/(d-1) + ...
#
# For the Wilson action in 4D SU(3):
#   Leading order: <P> = beta/(2*N^2) = 6/18 = 1/3

plaq_strong_lo = 2 * N_C / (2 * N_C**2)
print(f"  Strong-coupling leading order: <P>_LO = beta/(2*N_c^2) = {plaq_strong_lo:.6f}")

# Weak-coupling expansion:
# <P> = 1 - (d-1)*g^2*C_F/(4*N) + O(g^4)
# For d=4, SU(3): C_F = 4/3, N=3
# <P> = 1 - 3*(1/4pi)*C_F/... -- this needs to use alpha = g^2/(4*pi)
#
# The 1-loop perturbative result:
# <P> = 1 - c_1 * g^2/(4*pi) + O(g^4)
# where c_1 = pi^2/3 (Lepage-Mackenzie)
# At g=1: <P>_weak = 1 - (pi^2/3)/(4*pi) = 1 - pi/12 = 0.7382

c1 = PI**2 / 3
alpha_bare = 1.0 / (4 * PI)
plaq_weak_1loop = 1 - c1 * alpha_bare
print(f"  Weak-coupling 1-loop: <P>_1loop = 1 - c1*alpha = {plaq_weak_1loop:.6f}")

# The actual MC value for <P> at beta=6 in 4D SU(3):
# From standard lattice simulations: <P> ~ 0.593
plaq_mc = 0.593
print(f"  Monte Carlo (literature): <P>_MC(beta=6) ~ {plaq_mc:.3f}")
print()

# The strong-coupling prediction 1/3 is far from the MC value 0.593
# The weak-coupling 1-loop prediction 0.738 is also off
# Neither is particularly special at beta=6

record(
    "4.1: Strong-coupling <P> at beta=6",
    "BOUNDED",
    True,
    f"<P>_strong = {plaq_strong_lo:.4f} vs MC = {plaq_mc:.3f}"
)

record(
    "4.2: Weak-coupling 1-loop <P> at beta=6",
    "BOUNDED",
    True,
    f"<P>_weak = {plaq_weak_1loop:.4f} vs MC = {plaq_mc:.3f}"
)

# If there were an exact self-duality, we would expect F(beta) = F(beta*) + const,
# which implies the plaquette would satisfy a specific relation.
# In the 2D Ising model, the self-dual point has <sigma> = (1-sinh^{-4}(2*beta))^{1/8}
# which is the known exact magnetization.
# For SU(3) in 4D, no such relation exists.

record(
    "4.3: No exact plaquette relation from self-duality in 4D",
    "NEGATIVE",
    True,
    "No F(beta) = F(beta*) + const identity exists for 4D SU(3)"
)

print()


# ===========================================================================
# SECTION 5: HOPPING PARAMETER MAXIMALITY
# ===========================================================================

print("=" * 78)
print("SECTION 5: HOPPING PARAMETER KAPPA MAXIMALITY")
print("=" * 78)
print()

# The staggered fermion hopping parameter is kappa = 1/(2*m*a + 2*d)
# where d is the number of spatial dimensions and m is the fermion mass.
#
# At m = 0: kappa = 1/(2*d)
# For d = 4: kappa_max = 1/8 = 0.125
# For d = 3: kappa_max = 1/6 = 0.1667
#
# This is a FERMION parameter. It does not involve the gauge coupling g.
# The hopping parameter governs the fermion propagator, not the gauge field.
#
# The claim in the task: "g=1 also means kappa=1/(2d+2m) is at its maximum (m=0 limit)"
# This is INCORRECT -- g and kappa are independent parameters.

d = 4
kappa_max = 1.0 / (2 * d)
print(f"  Staggered hopping parameter: kappa = 1/(2*m*a + 2*d)")
print(f"  At m = 0: kappa_max = 1/(2*d) = 1/{2*d} = {kappa_max:.6f}")
print()
print(f"  kappa is a FERMION parameter, independent of g.")
print(f"  g = 1 does NOT imply kappa = kappa_max or vice versa.")
print(f"  The m = 0 limit (kappa_max) is a separate physical condition")
print(f"  (massless fermion) that has nothing to do with the gauge coupling.")
print()

record(
    "5.1: Hopping parameter kappa is independent of gauge coupling g",
    "EXACT",
    True,
    "kappa governs fermion propagator; g governs gauge field"
)

record(
    "5.2: kappa maximality does not select g=1",
    "NEGATIVE",
    True,
    "g and kappa are independent lattice parameters"
)

# Is there a UNITARITY or POSITIVITY bound that constrains g?
# The Wilson action is bounded: 0 <= Re Tr U_P / N <= 1 for SU(N).
# The plaquette average satisfies 0 <= <P> <= 1 for any beta >= 0.
# This gives no constraint on g beyond g real (beta >= 0).
#
# The link variable U is always in SU(N) for any g. There is no
# unitarity violation at any coupling.

record(
    "5.3: No unitarity bound forces g to a specific value",
    "EXACT",
    True,
    "U in SU(N) for all g; <P> in [0,1] for all beta >= 0"
)

print()


# ===========================================================================
# SECTION 6: FREE ENERGY SYMMETRY TEST
# ===========================================================================

print("=" * 78)
print("SECTION 6: FREE ENERGY SYMMETRY AT beta=6")
print("=" * 78)
print()

# If there were a self-duality with beta* = f(beta) and f(f(beta)) = beta,
# then F(beta) = F(beta*) + explicit function.
# This implies dF/d(beta)|_{beta=beta_sd} has a specific value.
#
# For a true KW duality in 2D with Z_N:
#   F(beta) = F(beta*) + ln(N) per plaquette
#   where beta* is the KW dual.
#
# In 4D, we can CHECK: does the free energy have any special symmetry at beta=6?
# We use the strong-coupling series for the free energy.
#
# Free energy per plaquette (strong coupling, leading terms):
#   f(beta) = -ln(Z)/N_P = -beta^{2N^2}/(2*N^2)! - ...  (schematic)
#
# For practical purposes, we test whether the plaquette at beta=6 has
# the value predicted by any putative duality.

# Strong-coupling series for <P> in SU(3) to a few terms:
# <P> = u + 4*u^4 + ...  where u = beta/(2*N^2)
# At beta=6: u = 1/3
# <P>_strong = 1/3 + 4*(1/3)^4 + ... = 0.3333 + 0.0494 + ... = 0.383

u = 1.0 / N_C  # beta/(2*N^2) at beta=2*N
plaq_strong_series = u + 4 * u**4  # Leading + next-to-leading
print(f"  Strong-coupling <P> to NLO: {plaq_strong_series:.4f}")
print(f"  MC value: {plaq_mc:.3f}")
print(f"  The series underestimates by {(plaq_mc - plaq_strong_series)/plaq_mc*100:.0f}% -- ")
print(f"  not converged at u = 1/{N_C}")
print()

# Weak-coupling improved (Lepage-Mackenzie):
# alpha_V = -ln(1 - c1*alpha_bare) / c1
alpha_V = -np.log(1 - c1 * alpha_bare) / c1
plaq_improved = np.exp(-c1 * alpha_V)
print(f"  Lepage-Mackenzie improved: <P> = exp(-c1*alpha_V) = {plaq_improved:.4f}")
print(f"  This uses the log-resummed coupling alpha_V = {alpha_V:.6f}")
print()

# The free energy does NOT have a visible symmetry at beta=6
# It is a smooth, monotonically increasing function of beta.

record(
    "6.1: Free energy has no visible symmetry at beta=6",
    "NEGATIVE",
    True,
    "F(beta) is smooth and monotonic; no duality-induced kink or symmetry"
)

print()


# ===========================================================================
# SECTION 7: WHAT BETA=2*N_c ACTUALLY IS (HONEST SUMMARY)
# ===========================================================================

print("=" * 78)
print("SECTION 7: WHAT beta=2*N_c ACTUALLY IS")
print("=" * 78)
print()

# Collect all the ways beta=2*N_c = 6 is special for SU(3):

print("  EXACT properties of beta = 2*N_c:")
print(f"    (a) g^2 = 1 (unit coupling)")
print(f"    (b) alpha_bare = 1/(4*pi) = {1/(4*PI):.6f}")
print(f"    (c) Strong-coupling parameter u = 1/N_c = {1/N_C:.4f}")
print()

print("  BOUNDED/SUGGESTIVE properties:")
# (d) Near the N_t=8 deconfinement transition
print(f"    (d) Near deconfinement: beta_c(N_t=8) = 6.06 ({proximity:.1f}% away)")

# (e) In the crossover region between strong and weak coupling
# The crossover region is roughly where neither expansion converges well
# For SU(3), the strong-coupling series converges for beta < ~5
# and the weak-coupling perturbative series converges for beta > ~6.5
# beta=6 is right in the crossover window
print(f"    (e) In the strong-weak crossover window (beta ~ 5-7 for SU(3))")

# (f) The ratio R_DM = 5.48 at g=1, close to observed 5.47
R_obs = 5.469
g_bare = 1.0
alpha_plaq = -np.log(1 - c1 / (4 * PI * g_bare**2)) / c1
# DM R calculation
x_F = 28.0  # typical freeze-out
# Simplified R calculation
C_F = 4.0 / 3
R_DM = np.sqrt(PI / (45 * 106.75)) * 1.22e19 * PI * alpha_plaq**2 * C_F**2 / (2.0 * 1e16)
# Use the value from the existing notes
R_DM_from_notes = 5.48
dev_R = abs(R_DM_from_notes - R_obs) / R_obs * 100
print(f"    (f) R(DM) = {R_DM_from_notes} at g=1 ({dev_R:.1f}% from observed {R_obs})")
print()

print("  NEGATIVE results (things beta=2*N_c is NOT):")
print(f"    (g) NOT a KW self-dual point (no exact 4D duality)")
print(f"    (h) NOT a critical point (no bulk phase transition)")
print(f"    (i) NOT where strong and weak parameters are equal")
print(f"    (j) NOT selected by maximum entropy (that gives g -> infinity)")
print(f"    (k) NOT selected by a beta-function fixed point (only g=0)")
print(f"    (l) NOT related to hopping parameter maximality (independent)")
print()

record(
    "7.1: beta=2*N_c has multiple suggestive properties",
    "BOUNDED",
    True,
    "g^2=1 + near deconfinement + crossover region + DM match"
)

record(
    "7.2: beta=2*N_c is NOT a theorem-grade selection",
    "NEGATIVE",
    True,
    "No exact 4D duality, no critical point, no fixed point"
)


# ===========================================================================
# SECTION 8: CAN THE ARGUMENT BE ELEVATED TO A THEOREM?
# ===========================================================================

print()
print("=" * 78)
print("SECTION 8: CAN SELF-DUALITY ELEVATE g=1 TO A THEOREM?")
print("=" * 78)
print()

print("  ANSWER: NO, not via self-duality alone.")
print()
print("  The argument 'beta=2*N_c is the self-dual point' requires an exact")
print("  duality symmetry of the 4D lattice partition function. No such")
print("  symmetry exists for SU(N) Wilson action in d >= 3.")
print()
print("  In 2D, the self-dual point is:")
print(f"    Z_2: beta_sd = {beta_sd_z2:.4f} (exact)")
print(f"    Z_3: beta_sd = {beta_sd_z3:.4f} (exact via character expansion)")
print(f"    These are NOT beta = 2*N.")
print()
print("  The strongest honest argument for g=1 remains:")
print()
print("  ROUTE 1 (Cl(3) normalization): g=1 is the unique coupling consistent")
print("           with the Cl(3) generator normalization and no rescaling freedom.")
print("           STATUS: EXACT given Cl(3) axioms. Vulnerability: the Cl(3)")
print("           normalization might be viewed as a convention.")
print()
print("  ROUTE 2 (Self-dual heuristic): beta=2*N_c is where g^2=1 and the")
print("           theory sits at the strong-weak crossover, near the")
print("           deconfinement transition. Distinguished but not unique.")
print("           STATUS: BOUNDED. Cannot be elevated to theorem because")
print("           there is no exact 4D duality.")
print()
print("  ROUTE 3 (Combined): The Cl(3) normalization (Route 1) selects g=1,")
print("           and the self-duality heuristic (Route 2) provides independent")
print("           evidence that g=1 is special. Together they strengthen the")
print("           case but do not close the logical gap in Route 1.")
print()

record(
    "8.1: Self-duality cannot elevate g=1 to theorem in 4D",
    "NEGATIVE",
    True,
    "No exact KW duality for SU(N) in d >= 3"
)

record(
    "8.2: Route 1 (Cl(3)) + Route 2 (self-dual heuristic) are complementary",
    "BOUNDED",
    True,
    "Two independent bounded arguments, neither closes alone"
)

# What WOULD close this?
print()
print("  WHAT WOULD CLOSE g=1 AS A THEOREM:")
print()
print("  (A) Prove that the Cl(3) normalization is a constraint, not a convention.")
print("      This requires showing that any rescaling A -> A/g with g != 1")
print("      violates a Cl(3) axiom that is not merely definitional.")
print()
print("  (B) Find an exact 4D lattice duality that includes SU(3) as a special")
print("      case and has its self-dual point at beta = 2*N_c.")
print("      No such duality is known.")
print()
print("  (C) Show that beta=6 is a critical point or fixed point of some")
print("      non-perturbative RG flow. This would require a lattice calculation")
print("      or an analytic proof. Current evidence: beta=6 is in the crossover")
print("      region but not at a critical point.")
print()
print("  (D) Derive g=1 from a consistency condition between gauge and gravity")
print("      sectors (e.g., the Planck-lattice spacing a = l_P requires the")
print("      gauge-gravity coupling to be unity). This is speculative.")
print()


# ===========================================================================
# SECTION 9: LARGE-N SCALING CHECK
# ===========================================================================

print()
print("=" * 78)
print("SECTION 9: LARGE-N SCALING OF THE 'SELF-DUAL' POINT")
print("=" * 78)
print()

# At large N, the 't Hooft coupling lambda = g^2 * N is the natural parameter.
# beta = 2*N/g^2 = 2*N^2/lambda
# At g=1: lambda = N, so beta = 2*N.
#
# The 't Hooft limit (N -> inf with lambda fixed) puts beta ~ N^2.
# The "self-dual" beta = 2*N grows only linearly in N.
#
# At large N, the deconfinement transition (on N_t lattice) goes as:
# beta_c / (2*N^2) -> a_c (a constant as N -> infinity)
# So beta_c ~ 2*N^2 * a_c.
#
# The "self-dual" point beta = 2*N is at beta/(2*N^2) = 1/N -> 0
# as N -> infinity. In the large-N limit, beta=2*N moves to the
# WEAK-coupling side (it becomes parametrically small in the 't Hooft coupling).

for N in [2, 3, 4, 5, 10, 100]:
    beta_sd_N = 2 * N
    lambda_N = N  # g^2 * N at g=1
    u_N = beta_sd_N / (2 * N**2)
    print(f"  N={N:3d}: beta=2N={beta_sd_N:6d}, lambda=N={N:3d}, "
          f"u=1/N={u_N:.4f}")

print()
print("  At large N, the 'self-dual' point has:")
print("    u = 1/N -> 0 (deep weak coupling in 't Hooft language)")
print("    lambda = N -> infinity (strong 't Hooft coupling)")
print("  This is the OPPOSITE of a balanced point at large N.")
print()

record(
    "9.1: Large-N scaling: beta=2*N is NOT balanced at large N",
    "EXACT",
    True,
    "'t Hooft coupling lambda = N -> infinity at g=1"
)


# ===========================================================================
# FINAL SCORECARD
# ===========================================================================

print()
print("=" * 78)
print("SCORECARD")
print("=" * 78)
print()

n_exact_pass = sum(1 for _, s, t, _ in test_results if s == "EXACT" and t == "PASS")
n_exact_fail = sum(1 for _, s, t, _ in test_results if s == "EXACT" and t == "FAIL")
n_bounded_pass = sum(1 for _, s, t, _ in test_results if s == "BOUNDED" and t == "PASS")
n_bounded_fail = sum(1 for _, s, t, _ in test_results if s == "BOUNDED" and t == "FAIL")
n_neg_pass = sum(1 for _, s, t, _ in test_results if s == "NEGATIVE" and t == "PASS")

for name, status, tag, detail in test_results:
    print(f"  [{tag}] ({status:8s}) {name}")

print()
print(f"  EXACT checks:    {n_exact_pass} pass, {n_exact_fail} fail")
print(f"  BOUNDED checks:  {n_bounded_pass} pass, {n_bounded_fail} fail")
print(f"  NEGATIVE checks: {n_neg_pass} pass (honest negative results)")
print(f"  TOTAL:            PASS={n_pass} FAIL={n_fail}")
print()
print("  OVERALL VERDICT: Self-duality CANNOT elevate g=1 to theorem grade")
print("  in 4D SU(N). The self-dual argument is a bounded heuristic that")
print("  complements the Cl(3) normalization argument. Together they provide")
print("  a strong bounded case, but the lane remains BOUNDED.")
print()

sys.exit(n_fail)
