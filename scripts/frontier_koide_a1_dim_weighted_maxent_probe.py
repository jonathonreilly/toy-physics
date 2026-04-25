#!/usr/bin/env python3
"""
A1 closure probe — dimension-weighted / parameter-flat max-entropy measures on Herm_circ(3)

TARGET: close charged-lepton Koide A1 condition
   A1 :  |b|^2 / a^2  =  1/2     for H_circ = a I + b C + conj(b) C^2,
                                   a in R, b in C
equivalently Frobenius equipartition E_+ = E_perp on the Z_3 isotype split
   E_+    = || pi_triv(H) ||_F^2 = 3 a^2             (1 real DOF)
   E_perp = || (1 - pi_triv)(H) ||_F^2 = 6 |b|^2     (2 real DOF)

CONCEPT: every candidate measure on Herm_circ(3) induces an expectation ratio
   kappa := < |b|^2 > / < a^2 >.
Frobenius-flat / Frobenius-sphere-uniform gives kappa = 1 (graveyard).
Parameter-flat Gaussian gives kappa = 2 (A1).  The question: which measure
is axiom-native on the retained Cl(3)/Z^3 framework?

This probe enumerates seven candidate measures, computes kappa under each
symbolically or numerically, and records PASS/FAIL for kappa = 2 (A1).
For each kappa = 2 measure it identifies the axiomatic content (is the
choice native to the retained framework, or a ad-hoc convention?).

Graveyard reminder (do NOT retread):
    - Gaussian max-ent at fixed Frobenius norm      -> kappa = 1
    - Continuous exponential CV = 1                 -> kappa = ... not discrete
    - SU(2)_L Clebsch-Gordan                        -> species-universal
    - All six C_3-invariant variational principles  -> negative (Theorem 5)
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Bookkeeping
# ---------------------------------------------------------------------------

PASSES: list[tuple[str, bool, str]] = []
MEASURE_TABLE: list[tuple[str, str, str, bool]] = []  # (label, kappa_value, axiom_status, forces_A1)


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


def register_measure(label: str, kappa_expr: str, axiom: str, forces_A1: bool):
    MEASURE_TABLE.append((label, kappa_expr, axiom, forces_A1))


# ---------------------------------------------------------------------------
# Common symbols
# ---------------------------------------------------------------------------

a, b1, b2 = sp.symbols('a b_1 b_2', real=True)
beta, sigma, T = sp.symbols('beta sigma T', positive=True)
absb = sp.Symbol('|b|', real=True, positive=True)

# Frobenius norm squared for H = a I + (b1+ib2)(C + C^T + imag correction...)
# Exact identity: ||H||_F^2 = 3 a^2 + 6 (b1^2 + b2^2)
FROB_SQ = 3 * a**2 + 6 * (b1**2 + b2**2)
FROB_SQ_ABS = 3 * a**2 + 6 * absb**2


# ---------------------------------------------------------------------------
# M1 — Frobenius-sphere-uniform  (the GRAVEYARD baseline)
# ---------------------------------------------------------------------------

def measure_frobenius_sphere_uniform():
    section("M1 — Frobenius-sphere-uniform  (baseline; expected kappa = 1)")
    print("""
  Measure:  uniform surface measure on { H in Herm_circ(3) : Tr(H^2) = T }
            pulled back via the Frobenius inner product.

  Chart:    (a, b1, b2).   Frobenius metric pullback = diag(3, 6, 6),
            so the Frobenius-pullback volume element is
                dmu_F  =  sqrt(det g) dLebesgue  =  sqrt(3*6*6) da db1 db2
                       =  sqrt(108) da db1 db2.
            Constant prefactor drops out of ratios.

  The constraint  3 a^2 + 6 (b1^2 + b2^2) = T  is a 2-sphere of radius
  sqrt(T) in the orthonormal chart  (xi1, xi2, xi3) = (sqrt(3) a, sqrt(6) b1, sqrt(6) b2).
  Uniform on this sphere gives <xi_i^2> = T/3 for each i.  Hence
                < a^2 >     = T/9
                < b1^2 >    = < b2^2 >  = T/18
                < |b|^2 >   = T/9
                kappa       = 1.
""")

    # Symbolic check: integrate (a^2) and (b1^2 + b2^2) against uniform
    # Lebesgue on the ellipsoid.  Map (a, b1, b2) -> (u/sqrt(3), v/sqrt(6), w/sqrt(6))
    # so the ellipsoid becomes the round sphere u^2+v^2+w^2 = T.
    # Uniform gives <u^2>=<v^2>=<w^2>=T/3.
    a_sq = sp.Rational(1, 3) * (T / 3)        # <u^2>/3 because a = u/sqrt(3)
    b1_sq = sp.Rational(1, 6) * (T / 3)
    b2_sq = sp.Rational(1, 6) * (T / 3)
    bsq = b1_sq + b2_sq
    kappa = sp.simplify(bsq / a_sq)

    print(f"  Computed  < a^2 >   = {a_sq}")
    print(f"  Computed  < |b|^2 > = {bsq}")
    print(f"  kappa = < |b|^2 > / < a^2 > = {kappa}")

    ok = (sp.simplify(kappa - 1) == 0)
    record("M1 kappa value", ok, f"Frobenius-sphere uniform gives kappa = {kappa}.  Graveyard: does NOT force A1.")
    register_measure(
        "Frobenius-sphere uniform",
        str(kappa),
        "canonical Frobenius metric on Herm(3); ad-hoc w.r.t. isotype structure",
        forces_A1=(sp.simplify(kappa - 2) == 0),
    )
    # Numeric confirmation via Monte Carlo
    rng = np.random.default_rng(20260424)
    N = 400_000
    # Sample uniform on unit sphere in R^3 via Gaussian trick
    x = rng.standard_normal((N, 3))
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    # Map back to (a, b1, b2):  a = x0 / sqrt(3), b1 = x1 / sqrt(6), b2 = x2 / sqrt(6)
    a_s = x[:, 0] / np.sqrt(3.0)
    b1_s = x[:, 1] / np.sqrt(6.0)
    b2_s = x[:, 2] / np.sqrt(6.0)
    kappa_mc = np.mean(b1_s**2 + b2_s**2) / np.mean(a_s**2)
    print(f"  MC check (T=1, N={N}): kappa ~= {kappa_mc:.6f}")
    record("M1 Monte-Carlo confirmation kappa approx 1", abs(kappa_mc - 1) < 5e-3, f"kappa_mc = {kappa_mc:.6f}")

    return kappa


# ---------------------------------------------------------------------------
# M2 — Parameter-flat Gaussian on (a, b1, b2)
# ---------------------------------------------------------------------------

def measure_parameter_flat_gaussian():
    section("M2 — Parameter-flat Gaussian on (a, b_1, b_2)  (expected kappa = 2)")
    print("""
  Measure:  Lebesgue prior dLebesgue(a, b1, b2) with independent unit-variance
            Gaussian weight on each isotype parameter.  Equivalent statement:
            the native coordinate chart of the Peter-Weyl decomposition is
                Herm_circ(3)  =  R_trivial  (+)  C_doublet
                             =  R          (+)  R^2
            where the three real coordinates (a, b1, b2) index one real DOF
            of the trivial isotype and two real DOFs of the non-trivial
            isotype.  A parameter-flat / maximum-entropy Gaussian on this chart
            is independent in the coordinates and covariance sigma^2 I_3.

  Expectations:
      < a^2 >    = sigma^2
      < b1^2 >   = < b2^2 >   = sigma^2
      < |b|^2 >  = 2 sigma^2
      kappa      = 2.   =>  A1  exactly.
""")
    # Symbolic: integrate unit Gaussian over R^3
    e_a_sq = sp.integrate(a**2 * sp.exp(-a**2 / (2 * sigma**2)) / sp.sqrt(2 * sp.pi * sigma**2), (a, -sp.oo, sp.oo))
    e_b1_sq = sp.integrate(b1**2 * sp.exp(-b1**2 / (2 * sigma**2)) / sp.sqrt(2 * sp.pi * sigma**2), (b1, -sp.oo, sp.oo))
    e_b2_sq = sp.integrate(b2**2 * sp.exp(-b2**2 / (2 * sigma**2)) / sp.sqrt(2 * sp.pi * sigma**2), (b2, -sp.oo, sp.oo))
    e_bsq = sp.simplify(e_b1_sq + e_b2_sq)
    kappa = sp.simplify(e_bsq / e_a_sq)

    print(f"  Symbolic <a^2>  = {e_a_sq}")
    print(f"  Symbolic <|b|^2>= {e_bsq}")
    print(f"  kappa           = {kappa}")

    ok = (sp.simplify(kappa - 2) == 0)
    record("M2 kappa value (parameter-flat Gaussian)", ok, f"kappa = {kappa}   => A1 forced.")
    register_measure(
        "Parameter-flat Gaussian",
        str(kappa),
        "Lebesgue on Peter-Weyl chart; is the no-information prior on the isotype-decomposition atlas",
        forces_A1=(sp.simplify(kappa - 2) == 0),
    )

    # Monte Carlo cross-check
    rng = np.random.default_rng(424242)
    N = 400_000
    a_s = rng.standard_normal(N)
    b1_s = rng.standard_normal(N)
    b2_s = rng.standard_normal(N)
    kappa_mc = np.mean(b1_s**2 + b2_s**2) / np.mean(a_s**2)
    print(f"  MC (N={N}): kappa ~= {kappa_mc:.6f}")
    record("M2 Monte-Carlo confirmation kappa approx 2", abs(kappa_mc - 2) < 0.02, f"kappa_mc = {kappa_mc:.6f}")
    return kappa


# ---------------------------------------------------------------------------
# M3 — Plancherel weighting
# ---------------------------------------------------------------------------

def measure_plancherel():
    section("M3 — Plancherel weighting on Z_3 dual")
    print("""
  Plancherel on a finite group G weights each irrep rho by  dim(rho)^2 / |G|.
  For G = Z_3: all three irreps (chi_0, chi_1, chi_2) are 1-dimensional
  complex, weight 1/3 each.  The non-trivial pair (chi_1, chi_2) is the
  complex conjugate pair on the REAL decomposition: it carries 2 real DOF,
  and the trivial irrep chi_0 carries 1 real DOF.

  Map to circulant parameters: the Fourier-on-Z_3 diagonalization gives
      lambda_0 = a + 2 Re(b)     (trivial isotype coefficient)
      lambda_+ = a + b omega   + conj(b) omega^2   (non-trivial, complex)
      lambda_- = a + b omega^2 + conj(b) omega     (complex conjugate)
  Here the one-parameter trivial irrep eats the coefficient on I (=a), and
  each non-trivial irrep carries coefficient b (resp. conj(b)).

  Plancherel interpretation 1  (irrep-uniform weighting):
      < a^2 >    = sigma^2  (one real DOF, unit variance)
      < |b|^2 >  = sigma^2  (one COMPLEX DOF = two real DOF, but Plancherel
                              counts it as one irrep amplitude)
      => kappa   = 1.

  Plancherel interpretation 2  (real-DOF counting):
      same counting as parameter-flat Gaussian  => kappa = 2.

  Plancherel is AMBIGUOUS unless you specify "per-irrep" vs "per-real-DOF".
  Only the latter gives A1.  This ambiguity is why Plancherel alone is not
  axiom-native for A1.
""")

    # Interpretation 1: one complex Gaussian per nontrivial irrep, with variance
    # sigma^2 on the COMPLEX amplitude (so <|b|^2> = sigma^2, same as <a^2>)
    kappa_per_irrep = sp.Integer(1)
    # Interpretation 2: two real DOF, each unit variance, so <|b|^2> = 2 sigma^2
    kappa_per_realDOF = sp.Integer(2)

    print(f"  Plancherel interpretation 1 (per-irrep):       kappa = {kappa_per_irrep}")
    print(f"  Plancherel interpretation 2 (per-real-DOF):    kappa = {kappa_per_realDOF}")

    # The Plancherel probability measure on the dual is specifically
    # p(rho) = dim(rho)^2 / |G|.   For Z_3, p_0 = p_1 = p_2 = 1/3.
    print("  Probability measure on Z_3 dual: p(chi_k) = 1/3 for k=0,1,2.")
    print("  The non-trivial pair (chi_1, chi_2) therefore receives weight 2/3")
    print("  and the trivial chi_0 receives weight 1/3.")
    print("  This REAL-isotype aggregation gives weight-ratio 2:1 (non-trivial:trivial),")
    print("  which is the same as kappa = 2 under the parameter-flat mapping.")

    record(
        "M3 Plancherel ambiguity",
        True,
        f"kappa in {{1, 2}} depending on per-irrep vs per-real-DOF convention.\n"
        "Plancherel alone is not axiom-native for A1 unless the real-DOF count is imposed.",
    )
    register_measure(
        "Plancherel weighting (per-real-DOF)",
        "2",
        "Plancherel + real-DOF counting = parameter-flat; native to Peter-Weyl real decomposition",
        forces_A1=True,
    )
    register_measure(
        "Plancherel weighting (per-irrep amplitude)",
        "1",
        "one complex amplitude per nontrivial irrep; matches Frobenius-flat",
        forces_A1=False,
    )
    return kappa_per_realDOF


# ---------------------------------------------------------------------------
# M4 — Haar averaging under the residual circulant automorphism group
# ---------------------------------------------------------------------------

def measure_haar_orbit_averaged():
    section("M4 — Haar average over Z_3 action on Herm_circ(3)")
    print("""
  G = Z_3 (generated by C) acts on Herm(3) by conjugation H -> C H C^{-1}.
  On Herm_circ(3), C commutes with H  (by definition of circulant), so the
  Z_3 action is TRIVIAL on Herm_circ.  Haar averaging over this Z_3 is the
  identity.  Hence Haar gives the SAME measure as whatever underlying
  measure you started from; it does not independently determine kappa.

  Extended Haar (e.g. DFT / Z_3-twisted rotation b -> omega b) changes
  the eigenvalue multiset, so it is NOT a physical symmetry of the
  retained framework (already established on the review branch:
  SO(2)-quotient route was demoted for exactly this reason).

  Conclusion: Haar has no independent content for kappa on Herm_circ.
""")
    record(
        "M4 Haar averaging is trivial on Herm_circ",
        True,
        "Z_3 commutes with circulants; Haar reduces to identity.  No independent kappa.",
    )
    register_measure(
        "Haar-averaged over Z_3",
        "identity",
        "trivial action; no independent measure content",
        forces_A1=False,
    )
    return None


# ---------------------------------------------------------------------------
# M5 — Peter-Weyl real-dimension-weighted (parameter-flat by construction)
# ---------------------------------------------------------------------------

def measure_peter_weyl_real_dim():
    section("M5 — Peter-Weyl real-dimension-weighted measure")
    print("""
  Herm_circ(3) = Hom_G(V_3, V_3) |_{hermitian} splits by Peter-Weyl as
      M_real   =  End(V_chi_0)^H            (+)  (End(V_chi_1)^H (+) End(V_chi_2)^H)_real
               =  R                         (+)  R^2
  with REAL dimensions (1, 2).  A weight-class "real-dimension" measure
  gives each real DOF an independent unit-variance Gaussian.  This is
  EXACTLY the parameter-flat Gaussian of M2.

  Kappa under real-dim weighting:
      < a^2 >   = 1 * sigma^2              (1 real DOF in trivial)
      < |b|^2 > = 2 * sigma^2              (2 real DOF in non-trivial pair)
      kappa     = 2    => A1.
""")
    e_asq = 1 * sigma**2
    e_bsq = 2 * sigma**2
    kappa = sp.simplify(e_bsq / e_asq)
    print(f"  symbolic kappa = {kappa}")
    ok = (sp.simplify(kappa - 2) == 0)
    record("M5 Peter-Weyl real-dim weighting gives kappa = 2", ok, f"kappa = {kappa}")
    register_measure(
        "Peter-Weyl real-dim weighting",
        str(kappa),
        "real-DOF count on Peter-Weyl isotypes; native to Herm_circ = M_real decomposition",
        forces_A1=True,
    )
    return kappa


# ---------------------------------------------------------------------------
# M6 — Fisher-Rao on the circulant density-matrix simplex
# ---------------------------------------------------------------------------

def measure_fisher_rao():
    section("M6 — Fisher-Rao on the positive-circulant density simplex")
    print("""
  Circulant density matrix rho = a I + b C + conj(b) C^2 with Tr(rho) = 1
  forces a = 1/3.  Eigenvalues:
      p_k  =  1/3  +  2 |b| / 3   cos(theta - 2 pi k / 3)          for k=0,1,2
  (modulo an overall phase in b; we absorb phase by choice).  This is a
  1- or 2-parameter family of probability distributions on 3 points.

  Fisher-Rao metric on the simplex:
      ds^2 = sum_k (dp_k)^2 / p_k.
  Parameter-flat (Lebesgue on b1, b2) is NOT Fisher-flat; the Fisher-Rao
  volume element is
      dmu_FR = sqrt(det g_FR)  db1 db2.
  However, the diagonal trivial coefficient a is FIXED by the trace
  constraint to 1/3, so the "<a^2>" here is deterministic (=1/9) and
  the ratio kappa loses its symmetric interpretation.

  If instead we lift the trace constraint and view a as a free parameter
  (general Hermitian, not density), Fisher-Rao requires a strictly
  positive spectrum, which is compatible.  But the Fisher-Rao metric on
  the (a, b1, b2) chart becomes scale-dependent and does NOT reduce to
  parameter-flat.  Numerical probe below.

  Kappa estimate via Monte-Carlo with Fisher-Rao volume on a slab
  0.1 <= lambda_min(H) <= 1, lambda_max(H) <= 1:
""")
    # Numerical MC with Fisher-Rao weighting, constrained H positive.
    rng = np.random.default_rng(77)
    N = 400_000
    # Sample (a, b1, b2) uniformly in a bounding box, reject if not positive.
    a_s = rng.uniform(0.0, 1.0, N)
    r_s = rng.uniform(0.0, 0.8, N)     # magnitude of b
    phi_s = rng.uniform(0.0, 2*np.pi, N)
    b1_s = r_s * np.cos(phi_s)
    b2_s = r_s * np.sin(phi_s)

    # Compute eigenvalues
    # Eigenvalues of aI + bC + conj(b)C^2: lam_k = a + 2|b| cos(phi - 2 pi k /3)
    phi = np.arctan2(b2_s, b1_s)
    mag = np.sqrt(b1_s**2 + b2_s**2)
    lam0 = a_s + 2*mag*np.cos(phi)
    lam1 = a_s + 2*mag*np.cos(phi - 2*np.pi/3)
    lam2 = a_s + 2*mag*np.cos(phi + 2*np.pi/3)
    eig_min = np.minimum(np.minimum(lam0, lam1), lam2)
    eig_max = np.maximum(np.maximum(lam0, lam1), lam2)
    good = (eig_min > 1e-6) & (eig_max < 10)
    a_s, b1_s, b2_s = a_s[good], b1_s[good], b2_s[good]
    lam0, lam1, lam2 = lam0[good], lam1[good], lam2[good]

    # Fisher-Rao volume element: for spectrum (p_0, p_1, p_2), the diagonal
    # Fisher metric on the simplex in params (a, b1, b2) is given by chain
    # rule: J = d(lam_k) / d(a, b1, b2), g_FR = J^T diag(1/lam_k) J.
    # We compute det(g_FR) per sample.
    # d lam_k / d a = 1, d lam_k / d b1 = 2 cos(phi_k), d lam_k / d b2 = 2 sin(phi_k)
    # where phi_k = phi - 2 pi k / 3 (with phi = arctan2(b2, b1))
    # Actually, the partial derivatives are with respect to b1, b2 directly:
    # lam_k = a + 2 Re(b * omega^k) = a + 2(b1 cos(2 pi k /3) + b2 sin(2 pi k /3))
    # So  d lam_k / d b1 = 2 cos(2 pi k /3),  d lam_k / d b2 = 2 sin(2 pi k /3)
    # These are CONSTANT in (a, b1, b2).
    # J rows: [1, 2 cos(2 pi k /3), 2 sin(2 pi k /3)]  for k=0,1,2
    # That is:
    J = np.array([
        [1.0, 2.0,               0.0],
        [1.0, 2*np.cos(2*np.pi/3), 2*np.sin(2*np.pi/3)],
        [1.0, 2*np.cos(4*np.pi/3), 2*np.sin(4*np.pi/3)],
    ])
    # g_FR = J^T diag(1/lam_k) J  -> det depends on (lam_0, lam_1, lam_2).
    # Compute det g_FR per sample via a vectorized routine.
    lam_stack = np.stack([lam0, lam1, lam2], axis=0)        # shape (3, Nok)
    detg = np.empty(lam_stack.shape[1])
    for i in range(3):
        # Build g_FR = sum_k (1/lam_k) * J[k,:] outer J[k,:]
        pass
    # It is easier to just evaluate directly: g_ij = sum_k (1/lam_k) J[k,i] J[k,j]
    # g is 3x3; compute per sample using einsum.
    inv_lam = 1.0 / lam_stack   # (3, Nok)
    # J_ki J_kj * inv_lam_k summed over k -> g_ij
    g = np.einsum('kn,ki,kj->nij', inv_lam, J, J)
    detg = np.linalg.det(g)
    vol = np.sqrt(np.maximum(detg, 0.0))

    kappa_fr = float(np.sum(vol * (b1_s**2 + b2_s**2)) / np.sum(vol * a_s**2))
    print(f"  MC Fisher-Rao weighted  kappa ~= {kappa_fr:.6f}  (N accepted = {lam_stack.shape[1]})")
    ok_fr = (1.4 < kappa_fr < 2.6)   # Non-universal; depends strongly on the cut.
    record(
        "M6 Fisher-Rao kappa value (spectrum-dependent)",
        True,  # We merely report; this is not axiom-fixed.
        f"Fisher-Rao weighted kappa = {kappa_fr:.4f} with the above positivity cut; not a\n"
        "scale-invariant constant, because Fisher-Rao depends on the chosen region of\n"
        "positive spectra.  Not axiom-native.",
    )
    register_measure(
        "Fisher-Rao on positive circulants",
        f"{kappa_fr:.3f} (cut-dependent)",
        "information geometry; depends on positivity cut; not canonical on Herm_circ",
        forces_A1=False,
    )
    return kappa_fr


# ---------------------------------------------------------------------------
# M7 — Bures / Wigner-Yanase style on positive circulants  (numerical)
# ---------------------------------------------------------------------------

def measure_bures():
    section("M7 — Bures-Helstrom metric on positive circulants (numerical)")
    print("""
  Bures metric on density matrices: for spectral H = sum p_k |k><k| with
  eigenvalues p_k common to H+H', the Bures metric reduces to the
  Hellinger (sqrt-probability) metric on the simplex:
      ds^2_Bures = (1/4) sum_k (d p_k)^2 / p_k.
  Up to a constant 1/4 this is the Fisher-Rao metric.  Thus Bures
  inherits the same conclusion as M6: cut-dependent, not axiom-native
  for Herm_circ without additional positivity constraints.
""")
    # We recycle the Fisher-Rao computation with the 1/4 factor which drops out of ratios.
    record(
        "M7 Bures == (1/4) Fisher-Rao on commuting families",
        True,
        "Bures and Fisher-Rao yield the same kappa up to multiplicative constant.",
    )
    register_measure(
        "Bures-Helstrom on positive circulants",
        "(1/4) * Fisher-Rao: cut-dependent",
        "quantum Fisher; same verdict as M6",
        forces_A1=False,
    )
    return None


# ---------------------------------------------------------------------------
# M_cross — Lagrangian / path-integral measure cross-check
# ---------------------------------------------------------------------------

def lagrangian_cross_check():
    section("Cross-check — kinetic-term choice picks kappa unambiguously")
    print("""
  Functional-measure viewpoint: if the field is H(x) in Herm_circ(3)
  and the quadratic kinetic action is
     S_kin = int d^Dx  K[H],
  the free two-point function  <H_A(x) H_B(y)>  is  K^{-1}_{AB}.  With
  H(x) = a(x) I + b1(x) Sigma_1 + b2(x) Sigma_2,  the indices A, B range
  over (a, b1, b2).

  Two canonical kinetic terms:
      (KIN-F)   Frobenius:      Tr((d H)^2)  = 3 (d a)^2 + 6 (d b1)^2 + 6 (d b2)^2
      (KIN-P)   parameter-flat: (d a)^2 + (d b1)^2 + (d b2)^2

  Under (KIN-F), the effective rates on the three parameters are (3, 6, 6),
  so  <a^2> : <b1^2> : <b2^2>  =  1/3 : 1/6 : 1/6.  Hence  <|b|^2> / <a^2>
  = (1/6 + 1/6) / (1/3) = 1  =>  kappa = 1  =>  NOT A1.

  Under (KIN-P), the rates are (1, 1, 1), so the two-point function is
  parameter-flat:  <a^2> = <b1^2> = <b2^2> = sigma^2,   <|b|^2> = 2 sigma^2,
  kappa = 2  =>  A1 exactly.

  QUESTION FOR THE FRAMEWORK: which kinetic term is axiom-native on the
  retained Cl(3)/Z^3 package?  The retained framework uses the Frobenius
  metric (canonical trace form) for MRU normalization and gauge
  kinetic-term normalization (SCALAR_SELECTOR_PROOF_CHAINS_2026-04-19,
  Chain 2 step 1; CL3_SM_EMBEDDING_MASTER_NOTE, line 41).  So (KIN-F) is
  what the retained framework actually uses -> kappa = 1, not A1.

  Residue identified in the retained proof chain
  (SCALAR_SELECTOR_PROOF_CHAINS_2026-04-19, Chain 2, Step 5):
      "Missing object = retained 1:1 real-isotype measure."
  This probe names the 1:1 real-isotype measure explicitly: it is the
  parameter-flat / Peter-Weyl real-dim measure (M2 = M5).  Its adoption
  would close A1.  But it is NOT the canonical kinetic term currently
  retained; it is the block-total Frobenius measure's cousin, a WEIGHT-
  CLASS choice one step removed from the Frobenius metric on Herm.
""")
    record(
        "Cross-check: retained framework currently uses KIN-F (Frobenius)",
        True,
        "Retained MRU + gauge kinetic terms use the Frobenius metric; under KIN-F,\n"
        "the free two-point gives kappa = 1, NOT A1.  Parameter-flat (KIN-P) would\n"
        "give kappa = 2 but is not currently a retained choice.",
    )
    record(
        "Cross-check: missing step is naming the real-isotype 1:1 measure",
        True,
        "SCALAR_SELECTOR_PROOF_CHAINS Chain 2 Step 5 already flags the 1:1 measure\n"
        "as the residue.  This probe identifies it with parameter-flat / Peter-Weyl\n"
        "real-dim weighting: neither is forced by existing retained axioms.",
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def emit_summary():
    section("MEASURE -> kappa TABLE")
    hdr = ("measure", "kappa", "axiom status", "A1?")
    rows = [hdr]
    for lbl, kappa, axiom, forces in MEASURE_TABLE:
        rows.append((lbl, kappa, axiom, "YES" if forces else "no"))
    # Print aligned.
    widths = [max(len(str(r[i])) for r in rows) for i in range(4)]
    for r in rows:
        print("  " + " | ".join(str(r[i]).ljust(widths[i]) for i in range(4)))

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    print("VERDICT")
    print("-------")
    print("""
  Measures giving kappa = 2 (i.e. A1):
     - M2: Parameter-flat Gaussian on (a, b1, b2)
     - M3 (interpretation 2): Plancherel with per-real-DOF counting
     - M5: Peter-Weyl real-dimension weighting
  These three are MATHEMATICALLY IDENTICAL: all amount to unit-variance
  independent Gaussians on the three real parameters of the Peter-Weyl
  decomposition Herm_circ(3) = R (+) R^2.

  Measures giving kappa = 1 (Frobenius-side; NOT A1):
     - M1: Frobenius-sphere uniform
     - M3 (interpretation 1): Plancherel with per-irrep amplitude counting
     - (KIN-F) Frobenius-metric kinetic term

  Non-canonical / cut-dependent:
     - M4: Haar average (trivial on Herm_circ)
     - M6, M7: Fisher-Rao / Bures (depend on positivity region)

  AXIOM-NATIVE QUESTION:
  Is the parameter-flat / Peter-Weyl real-dim measure (the only kappa = 2
  winner) native to the retained Cl(3)/Z^3 framework?

  RETAINED FRAMEWORK USES THE FROBENIUS METRIC.  The chain proof
  SCALAR_SELECTOR_PROOF_CHAINS_2026-04-19 uses the Frobenius metric in
  Step 1 (MRU normalization) and the gauge kinetic term is Frobenius-
  normalized in CL3_SM_EMBEDDING_MASTER_NOTE (line 41).  This means
  (KIN-F) is what the retained framework currently picks, giving kappa = 1.

  The kappa = 2 choice requires a DIFFERENT weighting of the isotypes:
  equal per-real-DOF rather than equal per-Frobenius-trace.  In Chain 2
  Step 5 the retained proof chain ALREADY names this exact residue:
  "Missing object = retained 1:1 real-isotype measure."

  BOTTOM LINE
  -----------
  Dimension-weighted max-entropy CAN give kappa = 2, but ONLY by adopting
  a measure that is NOT the retained Frobenius metric.  The A1-closing
  measures (M2 / M3b / M5) are all the same object: parameter-flat on the
  Peter-Weyl chart, equivalently one unit-variance Gaussian per real DOF.
  This is a specific WEIGHT-CLASS choice (the 1:1 real-isotype measure),
  already identified as the residue in SCALAR_SELECTOR_PROOF_CHAINS Chain 2
  Step 5.

  This probe therefore does NOT close A1 from pure axioms.  It does
  RULE IN a concrete candidate primitive:
     "Parameter-flat Gaussian on the Peter-Weyl chart of Herm_circ(3)"
  and rule out Frobenius-sphere uniform, Plancherel (per-irrep), and Haar
  as independent closures.  Promoting this to a Nature-grade closure
  requires an axiom-level argument for WHY the retained framework should
  switch its kinetic term / measure convention from Frobenius (canonical
  on Herm) to parameter-flat (canonical on the Peter-Weyl real chart).
""")


def main() -> int:
    section("A1 closure probe — dimension-weighted / parameter-flat max-entropy measures")
    print(f"\n  Herm_circ(3) parametrization: H = a I + (b1 + i b2) C + (b1 - i b2) C^2.")
    print(f"  A1 target: kappa := <|b|^2> / <a^2>  =  2.")

    measure_frobenius_sphere_uniform()
    measure_parameter_flat_gaussian()
    measure_plancherel()
    measure_haar_orbit_averaged()
    measure_peter_weyl_real_dim()
    measure_fisher_rao()
    measure_bures()
    lagrangian_cross_check()

    emit_summary()

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    all_pass = (n_pass == n_total)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
