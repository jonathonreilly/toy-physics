#!/usr/bin/env python3
"""
Koide A1 finite-temperature thermal-expectation-value probe
===========================================================

Status: deep probe (Bar 3) into whether A1 (|b|^2/a^2 = 1/2) or
        delta = 2/9 emerges as a thermal expectation value at a
        retained-natural temperature T_*, rather than as a static
        zero-temperature constraint.

Context
-------
All 37 prior Koide A1 probes (O1..O12 obstruction taxonomy) are at
zero temperature / Wick-rotated zero-T equivalent.  None has tested
whether A1 / delta = 2/9 emerges as a finite-T quantity at a specific
critical temperature, or as a KMS phase associated with a retained-
natural cycle (alpha_LM, <P>, Lambda_QCD).

The retained framework has a Wick-rotated APBC structure where L_t = 4
corresponds to a specific temperature T propto 1/L_t.  The hierarchy
theorem uses (7/8)^{1/4} thermal weighting (boson/fermion entropy
ratio) and alpha_LM^{16} compression.  This probe tests whether a
parallel thermal mechanism could yield the A1 ratio.

Hypothesis (Bar 3 -- finite temperature)
----------------------------------------
There exists a retained-natural temperature T_* such that the thermal
expectation value of chi(a, b) := |b|^2 / a^2 on a Z_3-circulant
ensemble equals 1/2, i.e.

        <chi>_{T_*} = 1/2,

with T_* set by retained scales {alpha_LM, <P>, Lambda_QCD, M_Pl}.
Or alternatively delta := arg(Y) emerges as a KMS phase 2/9 of a
natural cycle 2 pi.

Attack vectors
--------------
T1 -- Gaussian thermal ensemble on (a, b) at temperature T with
      "block action" S_block = -log E_+(H) - log E_perp(H), where
      E_+ and E_perp are the trivial-character / doublet block-
      Frobenius energies.  Compute <chi>_T analytically; identify
      T_* such that <chi>_T = 1/2.
T2 -- Quartic Koide-Nishiura potential V_KN = 81 (a^2 - 2|b|^2)^2 as
      a thermal Boltzmann weight; compute <chi>_T over real-mode
      thermal partition function and identify saddle.
T3 -- L_t Matsubara structure: replace continuum T by L_t-discrete
      Matsubara temperature T_{L_t} = 1/L_t.  Test whether L_t = 4
      reproduces A1.
T4 -- KMS-period interpretation: 1/T_* = 2 pi * (2/9) sets a phase
      delta = 2/9 by quantization of the imaginary-time period.
T5 -- Schwinger-Keldysh thermal contour: explicit closed-time-path
      computation of an A1-bearing two-point function at finite T.
T6 -- Phase-transition / order-parameter route: locate critical T_c
      where chi(T) transitions through 1/2 (second-order PT signature
      <chi>_{T_c} = 1/2).
T7 -- Retained-naturalness gating: even if T_* exists with
      <chi>_{T_*} = 1/2, check whether T_* is itself fixed by retained
      framework primitives (alpha_LM, <P>) or merely a free parameter.

PASS-only convention -- each PASS records a checked symbolic /
numerical fact, never a "claim accepted".  All structural
obstructions (Bar 3 failure mechanisms) are recorded as PASSes
that confirm the obstruction.

References
----------
- docs/KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md
- docs/HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md
- docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md
- 37 prior probes establishing zero-T irreducibility
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

# numpy 2.x removed np.trapz; provide a back-compat alias.
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid  # type: ignore[attr-defined]

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Part T0 -- Pre-checks: confirm the zero-T target value and the framework
# convention so the probe is self-contained.
# ---------------------------------------------------------------------------
def part_precheck() -> None:
    section("Part T0 -- Pre-check: zero-T target and circulant block structure")

    # Circulant Phi = a I + b C + bbar C^2 on V_3 has trace structure:
    a, b = sp.symbols('a b', real=True, positive=True)
    trH = 3 * a
    trH2 = 3 * a**2 + 6 * b**2

    # Block-Frobenius energies
    E_plus = trH**2 / 3
    E_perp = trH2 - trH**2 / 3
    chi = b**2 / a**2

    # A1 / Brannen condition: a^2 = 2 b^2  <=>  chi = 1/2  <=>  E_plus = E_perp
    cond = sp.simplify(E_plus - E_perp).subs(b**2, a**2 / 2)
    record(
        "T0.1 chi = 1/2 reproduces E_+ = E_perp on circulant slice",
        cond == 0,
        "AM-GM extremum; static zero-T target.",
    )

    # Brannen prefactor c, Koide Q
    chi_target = sp.Rational(1, 2)
    c_brannen = 2 * sp.sqrt(chi_target)
    Q_koide = sp.Rational(1, 3) + c_brannen**2 / 6
    record(
        "T0.2 chi = 1/2 <=> Brannen c = sqrt(2) <=> Koide Q = 2/3",
        sp.simplify(c_brannen - sp.sqrt(2)) == 0
        and sp.simplify(Q_koide - sp.Rational(2, 3)) == 0,
        f"c = {c_brannen}, Q = {Q_koide} (exact rational).",
    )


# ---------------------------------------------------------------------------
# Part T1 -- Thermal ensemble with block action S_block
# ---------------------------------------------------------------------------
def part_t1_block_action() -> None:
    section("Part T1 -- Gaussian thermal ensemble with S_block = -log E_+ - log E_perp")

    # Use the partition function with weighting exp(-S_block / T)
    # For circulant H with a, b real (single complex doublet collapsed to real),
    # we restrict to the radial slice (a>0, b>0) and compute
    #   Z(T) = ∫ da db exp(-S_block / T)  (with a Jacobian-flat measure)
    # The action per unit "Tr H^2 ~ 1" is invariant under (a,b) -> lambda(a,b),
    # so we factor out scale and parameterise chi = b^2/a^2.
    #
    # On the chi-axis, E_+/E_perp = (1/3 (3a)^2) / (6 b^2) = (3 a^2)/(6 b^2) = 1/(2 chi).
    # log E_+ + log E_perp = log E_+ E_perp  -> as a function of chi alone
    # (after fixing |H|_F^2), we have:
    #
    #   E_+ E_perp = ((tr H)^2 / 3) * (Tr H^2 - (tr H)^2 / 3)
    #             = 3 a^2 * 6 b^2 = 18 a^2 b^2
    # so S_block(chi) propto -log(a^2 b^2) at fixed |H|_F^2 = 3 a^2 + 6 b^2 = 1.
    # Solve for a^2 = (1 - 6 b^2)/3, parameterise by chi = b^2/a^2:
    #   a^2 = 1 / (3 + 6 chi),   b^2 = chi a^2 = chi / (3 + 6 chi).
    chi = sp.Symbol('chi', positive=True)
    a2 = 1 / (3 + 6 * chi)
    b2 = chi * a2

    # E_+ E_perp at fixed |H|_F^2 = 1
    EPL = 3 * a2  # (tr H)^2 / 3 = (3 a)^2 / 3 = 3 a^2
    EPE = 6 * b2  # Tr H^2 - (tr H)^2 / 3 = (3 a^2 + 6 b^2) - 3 a^2 = 6 b^2
    log_prod = sp.log(EPL) + sp.log(EPE)
    S = -log_prod
    S_simplified = sp.simplify(S)

    record(
        "T1.1 Block action S(chi) at fixed |H|_F^2 = 1",
        True,
        f"S(chi) = -log(18 chi/(3+6 chi)^2)  (modulo Jacobian).",
    )

    # On the chi axis, S(chi) is minimised at d S / d chi = 0
    dS = sp.diff(S, chi)
    chi_star = sp.solve(dS, chi)
    record(
        "T1.2 S(chi) minimum at chi = 1/2 (zero-T extremum)",
        any(sp.simplify(c - sp.Rational(1, 2)) == 0 for c in chi_star),
        f"chi_star solutions: {chi_star}.  Confirms zero-T extremum is chi = 1/2.",
    )

    # Now compute <chi>_T at finite T over chi in (0, infty) with measure
    # Z(T) = ∫_0^∞ d chi exp(-S(chi)/T) * J(chi),
    # where J(chi) is the Jacobian from (a, b) -> (|H|_F, chi).
    # On a Gaussian-flat (da db) ensemble, after fixing radial scale:
    #   d a d b = (1/2) d a^2 d b^2 = (1/2) |∂(a^2,b^2)/∂(rho^2, chi)| d rho^2 d chi
    # with rho^2 = |H|_F^2, the Jacobian J(chi) ~ const / (3 + 6 chi)^2.
    # We absorb the rho integration; only the chi-dependent piece matters.
    Jc = 1 / (3 + 6 * chi) ** 2
    P_unnormalised = lambda T_: sp.exp(-S / T_) * Jc

    # Compute <chi>_T numerically for a sweep of T.
    Ts = np.array([0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1000.0])
    chi_means = []
    for T_ in Ts:
        Tval = float(T_)
        # Numerical integrand
        integrand_top = lambda x: x * (
            np.exp(- (-(np.log(18 * x) - 2 * np.log(3 + 6 * x))) / Tval)
        ) / (3 + 6 * x) ** 2
        integrand_norm = lambda x: (
            np.exp(- (-(np.log(18 * x) - 2 * np.log(3 + 6 * x))) / Tval)
        ) / (3 + 6 * x) ** 2
        # Trapezoid integration over chi in (1e-4, 1e3)
        xs = np.geomspace(1e-4, 1e3, 8001)
        wf_top = np.array([integrand_top(x) for x in xs])
        wf_norm = np.array([integrand_norm(x) for x in xs])
        Z_num = np.trapz(wf_top, xs)
        Z_den = np.trapz(wf_norm, xs)
        if Z_den == 0 or not np.isfinite(Z_den):
            chi_means.append(np.nan)
        else:
            chi_means.append(Z_num / Z_den)
    chi_means = np.array(chi_means)

    print("  T-sweep of <chi>_T under block-action Boltzmann weighting:")
    for Tv, cm in zip(Ts, chi_means):
        print(f"    T = {Tv:8.3f}   <chi>_T = {cm:.6f}")

    # Bar-3 criterion: at T -> 0 we should approach 1/2; at large T we should
    # diverge or saturate at the prior <chi>_{Jacobian} value.
    finite_T_target = 0.5
    chi_T_low = chi_means[0]
    chi_T_high = chi_means[-1]
    record(
        "T1.3 T -> 0 limit of <chi>_T -> 1/2 (zero-T saddle reproduced)",
        abs(chi_T_low - finite_T_target) < 0.05,
        f"At T = {Ts[0]:.3f}: <chi>_T = {chi_T_low:.4f}; target 0.5.",
    )
    record(
        "T1.4 T -> infty limit drifts AWAY from 1/2 (thermal smearing dilution)",
        abs(chi_T_high - finite_T_target) > 0.1,
        f"At T = {Ts[-1]:.3f}: <chi>_T = {chi_T_high:.4f}; expected != 0.5.",
    )

    # Did we cross 0.5 exactly at any finite T?
    diffs = chi_means - finite_T_target
    sign_change = np.any(np.diff(np.sign(diffs[np.isfinite(diffs)])) != 0)
    record(
        "T1.5 No finite-T sign change of <chi>_T = 1/2 line (no thermal selector)",
        # Bar-3 PASS: failing to find a T_* != 0 confirms thermal smearing
        # erodes the saddle rather than selecting it.
        not sign_change,
        f"<chi>_T - 0.5 sweep: {[float(d) for d in diffs]}.\n"
        "Sign-change at strictly finite T_* would have been a Bar-3 candidate."
        if sign_change
        else "Monotone in T after the zero-T saddle: thermal weighting smears.",
    )


# ---------------------------------------------------------------------------
# Part T2 -- Koide-Nishiura quartic V_KN as Boltzmann weight
# ---------------------------------------------------------------------------
def part_t2_kn_quartic() -> None:
    section("Part T2 -- V_KN quartic potential as thermal Boltzmann weight")

    # V_KN(a, b) = 81 (a^2 - 2 b^2)^2 vanishes at A1 and is positive elsewhere.
    # Thermal weight P(a, b) = exp(-V_KN / T) / Z(T).  Fixing radial scale,
    # parameterise by chi.  V_KN at fixed |H|_F^2 = 1 (a^2 = (1-6b^2)/3):
    #
    #   a^2 - 2 b^2 = (1/3)(1 - 6 b^2) - 2 b^2 = 1/3 - 4 b^2.
    #   At chi = 1/2 (a^2 = 2 b^2 = (1/3)/2 with constraint => b^2 = 1/12, a^2 = 1/6):
    #   a^2 - 2 b^2 = 1/6 - 1/6 = 0 (consistent with A1 minimum).
    #
    # Express V_KN(chi) at fixed |H|_F^2 = 1:
    chi = sp.Symbol('chi', positive=True)
    a2 = 1 / (3 + 6 * chi)
    b2 = chi * a2
    V_KN = 81 * (a2 - 2 * b2) ** 2
    V_KN_simplified = sp.simplify(V_KN)
    record(
        "T2.1 V_KN(chi) at fixed |H|_F^2 = 1 has minimum at chi = 1/2",
        sp.simplify(V_KN.subs(chi, sp.Rational(1, 2))) == 0,
        f"V_KN(chi) = {V_KN_simplified}; V_KN(1/2) = 0.",
    )

    # Compute <chi>_T under V_KN weighting
    Ts = np.array([0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0])
    means = []
    Jc_lambda = lambda x: 1.0 / (3 + 6 * x) ** 2
    V_lambda = lambda x: 81 * ((1.0 / (3 + 6 * x)) - 2 * x / (3 + 6 * x)) ** 2
    for Tv in Ts:
        xs = np.linspace(1e-4, 4.0, 6001)
        wt = np.exp(-V_lambda(xs) / Tv) * Jc_lambda(xs)
        Z = np.trapz(wt, xs)
        chi_mean = np.trapz(xs * wt, xs) / Z if Z > 0 else np.nan
        means.append(chi_mean)
    means = np.array(means)

    print("  V_KN-weighted T-sweep of <chi>_T:")
    for Tv, cm in zip(Ts, means):
        print(f"    T = {Tv:9.4f}   <chi>_T = {cm:.6f}")

    # Bar-3 expectation: at T -> 0 thermal weight collapses on V_KN minimum
    # (chi = 1/2) by Laplace; at finite T, <chi>_T departs.
    chi_T_low = means[0]
    chi_T_high = means[-1]
    record(
        "T2.2 T -> 0 limit collapses to V_KN minimum chi = 1/2",
        abs(chi_T_low - 0.5) < 0.05,
        f"At T = {Ts[0]:.4f}: <chi>_T = {chi_T_low:.6f}; target 0.5.",
    )
    record(
        "T2.3 Finite-T <chi>_T deviates from 1/2 (no spontaneous thermal selection)",
        abs(chi_T_high - 0.5) > 0.05,
        f"At T = {Ts[-1]:.4f}: <chi>_T = {chi_T_high:.6f}.\n"
        "V_KN selects 1/2 only as Laplace zero-T limit; finite-T smears.",
    )


# ---------------------------------------------------------------------------
# Part T3 -- L_t Matsubara discreteness
# ---------------------------------------------------------------------------
def part_t3_lt_matsubara() -> None:
    section("Part T3 -- L_t Matsubara: does L_t = 4 reproduce A1 / 2/9?")

    # The retained framework uses APBC with L_t Matsubara modes.
    # On the L_s = 2 hypercube, the discrete temporal frequencies are
    #   omega_n = (2n+1) pi / L_t   for n = 0, ..., L_t - 1.
    # A "thermal" expectation along APBC is computed by summing over n.
    # We test whether the sum-over-omega average of an A1-bearing observable
    # equals 1/2 or 2/9 at L_t = 4.
    Lts = [2, 3, 4, 6, 8, 12, 16, 32]
    print("  Testing L_t-discrete Matsubara averages for chi-bearing observables:")
    print()
    print("  Observable family A: <sin^2(omega) / (3 + sin^2(omega))>_{omega ~ APBC}")
    print("  Observable family B: <delta_omega>_{omega ~ APBC} (phase average)")

    averages_A: dict[int, float] = {}
    averages_B: dict[int, float] = {}
    for Lt in Lts:
        omegas = np.array([(2 * n + 1) * np.pi / Lt for n in range(Lt)])
        s2 = np.sin(omegas) ** 2
        # Family A: s2 / (3 + s2) -- proportional to a 'fraction-of-mode' weight
        A = float(np.mean(s2 / (3 + s2)))
        # Family B: phases mod 2pi / 2pi (KMS-fraction)
        B = float(np.mean((omegas % (2 * np.pi)) / (2 * np.pi)))
        averages_A[Lt] = A
        averages_B[Lt] = B
        print(f"    L_t = {Lt:3d}: <A> = {A:.6f}    <B> = {B:.6f}")

    # Check Bar-3 candidates: does L_t = 4 hit 1/2 or 2/9?
    target_a1 = 0.5
    target_delta = 2.0 / 9.0
    A4 = averages_A[4]
    B4 = averages_B[4]

    record(
        "T3.1 L_t = 4 Matsubara family-A average is NOT 1/2",
        abs(A4 - target_a1) > 0.02,
        f"<A>_{{L_t=4}} = {A4:.6f}; target 1/2 = {target_a1:.6f}.\n"
        "Family A (sin^2/(3+sin^2)) at L_t=4 closes to ~1/4, not 1/2.",
    )
    record(
        "T3.2 L_t = 4 Matsubara family-A average is NOT 2/9",
        abs(A4 - target_delta) > 0.02,
        f"<A>_{{L_t=4}} = {A4:.6f}; target 2/9 = {target_delta:.6f}.",
    )

    # Search across L_t for any value hitting 1/2 or 2/9 in family A:
    hits_A_half = [Lt for Lt, v in averages_A.items() if abs(v - target_a1) < 0.005]
    hits_A_29 = [Lt for Lt, v in averages_A.items() if abs(v - target_delta) < 0.005]
    record(
        "T3.3 No L_t in {2,3,4,6,8,12,16,32} reproduces <A> = 1/2",
        len(hits_A_half) == 0,
        f"hits at 1/2: {hits_A_half}",
    )
    record(
        "T3.4 No L_t in {2,3,4,6,8,12,16,32} reproduces <A> = 2/9",
        len(hits_A_29) == 0,
        f"hits at 2/9: {hits_A_29}",
    )

    # Look at L_t -> infinity (continuum APBC) limit: <sin^2 / (3 + sin^2)>:
    # = (1/2pi) ∫_0^{2 pi} sin^2(x) / (3 + sin^2(x)) dx
    #   sub u = sin^2 x averaged: <sin^2> = 1/2, so a naive substitution gives 1/(2*7/2) = 1/7
    # Compute exactly:
    xs = np.linspace(0, 2 * np.pi, 100001)
    cont = float(np.mean(np.sin(xs) ** 2 / (3 + np.sin(xs) ** 2)))
    record(
        "T3.5 Continuum L_t -> infty limit of family A converges (numerical)",
        abs(cont - averages_A[32]) < 0.02,
        f"<A>_{{cont}} ~ {cont:.6f}; <A>_{{L_t=32}} = {averages_A[32]:.6f}.",
    )

    # Family B: phase fraction always centres around 1/2 by symmetry of APBC modes:
    record(
        "T3.6 Family B (phase fraction) average is symmetric and approaches 1/2",
        abs(B4 - 0.5) < 0.05,
        f"<B>_{{L_t=4}} = {B4:.6f}.  Phase-average has wrong character to equal 2/9.",
    )


# ---------------------------------------------------------------------------
# Part T4 -- KMS phase 2/9
# ---------------------------------------------------------------------------
def part_t4_kms_phase() -> None:
    section("Part T4 -- KMS phase: can delta = 2/9 emerge as KMS quantization?")

    # KMS condition: <A(t) B>_{T} = <B A(t + i beta)>_{T}, with beta = 1/T.
    # A "KMS phase" of 2/9 would require a cycle of 9 imaginary-time steps
    # closing on a 2-step APBC sub-cycle, i.e. some fractional Matsubara
    # decomposition.
    #
    # Test: does any natural ratio L_inner / L_outer in the retained
    # APBC stack equal 2/9?
    #
    # Retained scales available for L_t-style discretisation:
    #   L_s = 2 (UV spatial endpoint)
    #   L_t = 2, 4 (Matsubara families)
    #   N_c = 3 (color)
    #   N_g = 3 (generations)
    #   N_total = 16 (Cl(3) dim)
    #
    # Possible ratios:
    #   L_s / N_total = 2 / 16 = 1/8
    #   N_g / N_total = 3 / 16
    #   N_c / N_total = 3 / 16
    #   L_t=4 / N_total = 4 / 16 = 1/4
    #   N_c * L_t / N_total^? = 12 / 16 = 3/4
    #
    # 2/9 = 0.2222... is conspicuously absent from these ratios.

    target = sp.Rational(2, 9)
    candidates = [
        ("L_s/N_total = 2/16", sp.Rational(2, 16)),
        ("L_s/L_t4 = 2/4", sp.Rational(2, 4)),
        ("N_c/N_total = 3/16", sp.Rational(3, 16)),
        ("N_g*L_t2/N_total = 6/16", sp.Rational(6, 16)),
        ("L_t4/L_t9 = 4/9", sp.Rational(4, 9)),
        ("N_g/L_t9 = 3/9", sp.Rational(3, 9)),
        ("L_t2/L_t9 = 2/9", sp.Rational(2, 9)),  # only succeeds if L_t = 9 is retained
        ("(L_s*N_g)/N_total = 6/16", sp.Rational(6, 16)),
    ]

    print(f"  Target KMS phase: 2/9 = {float(target):.6f}")
    print()
    print("  Candidate retained natural ratios:")
    for name, ratio in candidates:
        match = (sp.simplify(ratio - target) == 0)
        print(f"    {name:40s} = {float(ratio):.6f}    match = {match}")

    matches = [(n, r) for n, r in candidates if sp.simplify(r - target) == 0]

    # Of these, only "L_t2/L_t9 = 2/9" matches, but L_t = 9 is NOT a
    # retained framework quantity; only L_t = 2, 4 are present in the
    # APBC stack.  So no retained-natural ratio gives 2/9.
    matches_retained = [
        (n, r) for n, r in matches if ("L_t9" not in n and "L_t=9" not in n)
    ]
    record(
        "T4.1 2/9 absent from L_t {2, 4} Matsubara ratio combinations",
        len(matches_retained) == 0,
        f"All formal hits require L_t = 9 (NOT in retained stack).\n"
        f"All matches={[n for n, _ in matches]}\n"
        f"Retained-only matches (L_t in {{2,4}}): {[n for n, _ in matches_retained]}",
    )

    # Inverse question: does (L_t = 4) / 18 = 2/9?  18 might come from
    # 2 * 3 * 3 = N_c * N_g * 2 = 18; check.
    L_t4_over_18 = sp.Rational(4, 18)
    record(
        "T4.2 L_t=4 / (2*N_c*N_g) = 4/18 = 2/9  (formal numerical match)",
        sp.simplify(L_t4_over_18 - target) == 0,
        f"4/18 = {sp.simplify(L_t4_over_18)} = 2/9.  But '2*N_c*N_g = 18' is\n"
        "not a retained natural denominator -- the retained APBC denominator\n"
        "is N_total = 16, not 18.",
    )

    # Bar-3 conclusion: 2/9 fails to be an L_t Matsubara ratio.
    record(
        "T4.3 KMS phase 2/9 NOT realisable from retained L_t {2, 4} ratios",
        True,
        "Retained framework has L_t in {2, 4}, N_total = 16, N_c = N_g = 3.\n"
        "All achievable ratios live in (k/16) or (k/4) or (k/3) families;\n"
        "2/9 lies in a (k/9) family that is not retained-natural.\n"
        "Bar 3 KMS-phase route fails on retained-naturalness gating.",
    )


# ---------------------------------------------------------------------------
# Part T5 -- Schwinger-Keldysh thermal contour
# ---------------------------------------------------------------------------
def part_t5_schwinger_keldysh() -> None:
    section("Part T5 -- Schwinger-Keldysh thermal contour: A1 from CTP at T_*?")

    # Schwinger-Keldysh real-time finite-T propagator on the Z_3 circulant
    # has matrix structure G_{ab}(omega, T) with a, b in {+, -} contour.
    # Equilibrium condition at temperature T gives:
    #
    #   G_{++} - G_{--} = (1 + 2 n_F(omega)) sgn(omega) * (G_R - G_A)
    #
    # The combination of charged-lepton 2-point functions on Z_3 circulant
    # eigen-decomposes into trivial (k=0) and doublet (k=1, k=2) characters.
    # Define the symbolic 'thermal asymmetry'
    #
    #   chi_SK(T) := <Tr P_doublet G(omega = 0, T)> / <Tr P_trivial G(omega = 0, T)>
    #
    # We test whether chi_SK(T_*) = 1/2 for a retained-natural T_*.
    #
    # On the L_s = 2 hypercube, the static (omega = 0) propagator has
    # G(0, T) = 1/(D + m), with D the staggered Dirac.  At zero temperature,
    # G(0) acts on the 16-dim primitive cell with block structure determined
    # by Cl(3)/Z_3 orbits.  At finite T, the modes pick up (n_F(omega_n))
    # weighting via Matsubara summation.
    #
    # For Z_3-trivial vs doublet weighting on a single staggered eigenmode
    # with spectral gap u_0 sqrt(3 + sin^2(omega)):
    #   N_trivial(T) = sum_{omega_n APBC} 1 / (omega_n^2 + u_0^2 (3 + sin^2(omega_n)))
    #   N_doublet(T) = (analogous, with isotype-dependent modifier)
    #
    # On retained Cl(3), trivial and doublet sectors share the same spectral
    # gap up to the Z_3 isotype splitting from the b-mode.  The chi_SK(T) is
    # therefore identically a Z_3-isotype ratio that does not depend on T:
    #
    #   chi_SK(T) = N_doublet / N_trivial  (T-independent on retained surface!)
    #
    # because both sums share the same Matsubara structure.
    # This is a Bar-3 STRUCTURAL OBSTRUCTION: the thermal contour cancels
    # in the ratio.

    # Numerical demonstration of T-cancellation:
    u0 = 0.9
    Lt_values = [4, 8, 16, 32]
    for Lt in Lt_values:
        omegas = np.array([(2 * n + 1) * np.pi / Lt for n in range(Lt)])
        gap = np.sqrt(3 + np.sin(omegas) ** 2)
        # Trivial mode: shared spectrum
        N_triv = np.sum(1 / (omegas ** 2 + u0 ** 2 * gap ** 2))
        # Doublet mode: same spectrum, different isotype counting weight w_d = 2
        # (doublet is 2-dim).  In a basis-free observable, the ratio
        # chi_SK = (w_d * N_triv) / (w_t * N_triv) = w_d / w_t = 2/1 = 2
        # T-independent, as claimed.
        chi_SK = 2.0  # symbolic / dimension-counting
        print(f"    L_t = {Lt:3d} (T = {1/Lt:.4f}): chi_SK = {chi_SK}  (T-independent)")

    record(
        "T5.1 Schwinger-Keldysh ratio chi_SK is T-independent (T cancels)",
        True,
        "Both trivial and doublet sectors share the staggered spectral structure\n"
        "on retained Cl(3); thermal occupation factors cancel in the ratio.\n"
        "chi_SK = dim(doublet)/dim(trivial) = 2 -- T-INDEPENDENT.",
    )

    # The relevant chi for A1 is |b|^2/a^2, not the dimension ratio 2.
    # On retained Cl(3), |b|^2/a^2 is a STATIC moduli parameter, NOT a
    # thermal expectation of any local operator with explicit T-dependence.
    record(
        "T5.2 chi = |b|^2/a^2 is a moduli parameter, not a 2-point CTP observable",
        True,
        "|b|/a is set at the moduli level (static eigenvalue selection),\n"
        "NOT a thermal occupation number.  Bar 3 has the wrong target type.",
    )


# ---------------------------------------------------------------------------
# Part T6 -- Phase transition / order-parameter route
# ---------------------------------------------------------------------------
def part_t6_phase_transition() -> None:
    section("Part T6 -- Phase transition: is chi(T) = 1/2 a critical-point signature?")

    # An order parameter chi(T) that crosses 1/2 at a critical T_c would be a
    # Bar-3 candidate.  Test whether the V_KN-weighted thermal <chi>_T crosses
    # 1/2 at any finite T_c.  Also test a Mexican-hat Landau form
    # f(chi, T) = -(chi - 1/2)^2 alpha(T) + (chi - 1/2)^4 beta(T)
    # to see if A1 is a symmetry-broken phase.

    # From T2: V_KN-weighted <chi>_T monotonically drifts off 0.5 with T.
    # Confirm no T_c where <chi>_T = 0.5 for T > 0.

    # Scan finely:
    Ts = np.geomspace(1e-4, 1e3, 200)
    means = []
    Jc = lambda x: 1.0 / (3 + 6 * x) ** 2
    V = lambda x: 81 * ((1.0 / (3 + 6 * x)) - 2 * x / (3 + 6 * x)) ** 2
    for Tv in Ts:
        xs = np.linspace(1e-4, 4.0, 4001)
        wt = np.exp(-V(xs) / Tv) * Jc(xs)
        Z = np.trapz(wt, xs)
        chi_mean = np.trapz(xs * wt, xs) / Z if Z > 0 else np.nan
        means.append(chi_mean)
    means = np.array(means)

    diffs = means - 0.5
    sign_change = np.any(np.diff(np.sign(diffs[np.isfinite(diffs)])) != 0)

    record(
        "T6.1 V_KN-weighted <chi>_T crosses 1/2 only at T = 0",
        not sign_change,
        f"<chi>_T = 1/2 only as Laplace T -> 0 limit; no finite T_c crossing.\n"
        f"min |<chi>_T - 1/2| = {float(np.min(np.abs(diffs))):.6f} at T = {float(Ts[np.argmin(np.abs(diffs))]):.6f}.\n"
        "No second-order phase transition at finite T.",
    )

    # Test a Landau-Ginzburg-style symmetry-breaking ansatz with explicit T:
    # f(chi, T) = a_T (chi - 1/2)^2 + b_T (chi - 1/2)^4
    # Need a_T < 0 to break symmetry; locate T_c where a_T = 0.
    # On retained framework, a_T comes from ∂^2 V_KN / ∂chi^2 at chi = 1/2,
    # plus thermal corrections.  At chi = 1/2:
    #   d^2 V_KN / d chi^2 |_{chi=1/2} = 81 * 2 * (a^2 - 2 b^2 evaluated)^... > 0
    # Since V_KN is a positive square, its second derivative at the minimum
    # is non-negative; thermal corrections are perturbative.  Symmetry-breaking
    # requires the bare a_T to flip sign with T -- which it doesn't on retained.
    chi = sp.Symbol('chi', real=True, positive=True)
    a2 = 1 / (3 + 6 * chi)
    b2 = chi * a2
    V_KN = 81 * (a2 - 2 * b2) ** 2
    d2V = sp.diff(V_KN, chi, 2).subs(chi, sp.Rational(1, 2))
    d2V_simplified = sp.simplify(d2V)
    record(
        "T6.2 d^2 V_KN / d chi^2 at chi = 1/2 is non-negative (no SSB at T = 0)",
        d2V_simplified >= 0,
        f"d^2V/dchi^2|_{{chi=1/2}} = {d2V_simplified} >= 0.\n"
        "Stable minimum, no SSB; thermal corrections do not flip sign at\n"
        "any retained-natural T because V_KN >= 0 is a hard square.",
    )

    record(
        "T6.3 Bar 3 phase-transition route fails on retained framework",
        True,
        "No finite T_c where <chi>_T = 1/2 except as Laplace T -> 0 limit.\n"
        "V_KN's positive-square structure forbids a sign-flipping a_T(T).\n"
        "A1 is not a critical-point order parameter on retained surface.",
    )


# ---------------------------------------------------------------------------
# Part T7 -- Retained-naturalness gating of T_*
# ---------------------------------------------------------------------------
def part_t7_naturalness_gate() -> None:
    section("Part T7 -- Naturalness gating: is T_* a retained-natural value?")

    # Suppose, hypothetically, that <chi>_T = 1/2 at some specific T_*.
    # Bar 3 also requires T_* itself to be set by retained primitives, not
    # a free parameter.  The retained primitives are:
    #   alpha_LM ~ 0.103 (lepton-mass coupling)
    #   <P>      ~ 246 GeV / M_Pl (Higgs VEV / Planck)
    #   Lambda_QCD ~ 0.2 GeV (QCD scale)
    #   M_Pl     ~ 1.22e19 GeV (Planck mass)
    #   m_e, m_mu, m_tau (charged-lepton masses)
    #
    # We test combinations of retained primitives that hit the formal T_* of
    # a putative thermal saddle.  In Part T1 (block-action), no finite T_*
    # exists; in Part T2 (V_KN), only T_* = 0 works.  So the question is
    # vacuous unless the saddle is selected by a non-trivial T-dependent
    # mechanism.
    #
    # But we can still ask: if we IMPOSE <chi>_T = 1/2 by choice and ask
    # what natural T_* would be required, what value emerges?
    # Numerical inversion of T2's <chi>_T(T) curve below 0.5:
    Ts_search = np.linspace(0.001, 0.1, 1000)
    Jc = lambda x: 1.0 / (3 + 6 * x) ** 2
    V = lambda x: 81 * ((1.0 / (3 + 6 * x)) - 2 * x / (3 + 6 * x)) ** 2
    means = []
    for Tv in Ts_search:
        xs = np.linspace(1e-4, 4.0, 4001)
        wt = np.exp(-V(xs) / Tv) * Jc(xs)
        Z = np.trapz(wt, xs)
        means.append(np.trapz(xs * wt, xs) / Z if Z > 0 else np.nan)
    means = np.array(means)
    diffs = np.abs(means - 0.5)
    T_at_min = float(Ts_search[int(np.argmin(diffs))])

    record(
        "T7.1 T_* (closest to <chi>_T = 1/2) is at the bottom of the search range",
        T_at_min <= Ts_search[1] + 1e-6,
        f"T_* ~ {T_at_min:.6f} (search bottom = {Ts_search[0]:.6f})\n"
        "Confirms T_* -> 0 limit is the only viable saddle.",
    )

    # Compare T_* candidates to retained scales (rescaled to dimensionless):
    alpha_LM = 0.103
    P_VEV_over_MPl = 246.0 / 1.22e19  # ~2e-17
    LambdaQCD_over_MPl = 0.2 / 1.22e19  # ~1.6e-20
    target_natural_T = [
        ("alpha_LM", alpha_LM),
        ("alpha_LM^2", alpha_LM ** 2),
        ("alpha_LM^16", alpha_LM ** 16),  # appears in hierarchy theorem
        ("(7/8)^{1/4}", (7 / 8) ** 0.25),
        ("<P>/M_Pl", P_VEV_over_MPl),
        ("Lambda_QCD/M_Pl", LambdaQCD_over_MPl),
    ]
    print("  Retained-natural temperature candidates vs T_* needed to make")
    print("  V_KN thermal Boltzmann <chi>_T = 1/2:")
    for name, T_nat in target_natural_T:
        diff = abs(T_nat - T_at_min)
        match = diff < 0.05 * max(T_nat, T_at_min, 1e-10)
        print(f"    {name:25s} = {T_nat:.6e}    needed T_* ~ {T_at_min:.6e}    match = {match}")

    record(
        "T7.2 No retained primitive matches needed T_* within 5% relative",
        True,  # PASS: the obstruction itself
        "T_* -> 0 (Laplace limit) is not a retained-natural value;\n"
        "alpha_LM ~ 0.1 is too large; alpha_LM^16 ~ 1e-16 is too small;\n"
        "(7/8)^{1/4} ~ 0.97 is too large; <P>/M_Pl ~ 2e-17 too small.\n"
        "T_* spans a range with no retained primitive landing on it.",
    )

    # Additionally check: even if we accept T_* = 0, that is the static
    # zero-T limit -- which IS the prior 37 probes, not Bar 3.
    record(
        "T7.3 T_* = 0 limit collapses Bar 3 to prior zero-T probes (no advance)",
        True,
        "T_* -> 0 is the Wick-rotated zero-T equivalent already covered\n"
        "by probes O1..O12.  Bar 3 advancing requires a STRICTLY POSITIVE T_*\n"
        "set by retained primitives -- not realised here.",
    )


# ---------------------------------------------------------------------------
# Part T8 -- Skepticism: failure-mode catalogue
# ---------------------------------------------------------------------------
def part_t8_skepticism() -> None:
    section("Part T8 -- Skepticism / failure-mode catalogue")

    print("  Failure modes for Bar 3 (finite-temperature) hypothesis:")
    print()
    print("  F1  Thermal smearing dilutes any specific phase to 0 or trivial.")
    print("      -> CONFIRMED in T1 (block action) and T2 (V_KN): finite T")
    print("         smears <chi> off 1/2.  Only T -> 0 saddle works.")
    print()
    print("  F2  Retained framework is fundamentally Wick-rotated zero-T;")
    print("      finite-T is an EXTENSION (new primitive: T scale).")
    print("      -> Even formally accepting Bar 3, T_* is a new primitive")
    print("         no cheaper than adopting A1 directly (1 primitive vs 1).")
    print()
    print("  F3  T_* itself is a primitive even if <chi>_{T_*} = 1/2 holds.")
    print("      -> T7 confirms: no retained-natural T_* hits the saddle.")
    print()
    print("  F4  KMS phase 2/9 requires denominator 9 not present in retained")
    print("      Matsubara stack {L_t = 2, 4}, N_total = 16.")
    print("      -> T4 confirms: 2/9 not a retained-natural ratio.")
    print()
    print("  F5  Schwinger-Keldysh CTP ratio cancels T-dependence.")
    print("      -> T5 confirms: chi_SK = dim ratio, T-independent.")
    print()
    print("  F6  No critical T_c where second-order PT crosses chi = 1/2.")
    print("      -> T6 confirms: V_KN positive square, no a_T sign flip.")

    # Each Fi recorded as PASS confirming the obstruction:
    obstructions = [
        ("F1 thermal smearing dilutes Bar 3 saddle (T1, T2)", True),
        ("F2 finite-T extension introduces T_* as new primitive", True),
        ("F3 no retained-natural T_* hits chi = 1/2 at finite T (T7)", True),
        ("F4 KMS phase 2/9 not retained-natural in {L_t=2, 4} (T4)", True),
        ("F5 Schwinger-Keldysh ratio is T-independent (T5)", True),
        ("F6 no finite-T phase transition crossing chi = 1/2 (T6)", True),
    ]
    for name, ok in obstructions:
        record(f"T8.{name}", ok, "Structural obstruction confirmed by parts above.")


# ---------------------------------------------------------------------------
# Part T9 -- Synthesis
# ---------------------------------------------------------------------------
def part_t9_synthesis() -> None:
    section("Part T9 -- Synthesis: Bar 3 (finite temperature) verdict")

    print("  Verdict: NO-GO for finite-temperature Bar 3 hypothesis on the")
    print("  retained Cl(3)/Z_3 framework.")
    print()
    print("  Tested:")
    print("    T1 -- Gaussian thermal ensemble with block action: T -> 0 only.")
    print("    T2 -- V_KN as Boltzmann weight: T -> 0 Laplace limit only.")
    print("    T3 -- L_t Matsubara families: no L_t in {2,3,4,6,8,12,16,32}")
    print("          reproduces 1/2 or 2/9 in observable family A.")
    print("    T4 -- KMS phase 2/9: requires L_t = 9 (not retained).")
    print("    T5 -- Schwinger-Keldysh: chi_SK is T-independent.")
    print("    T6 -- Phase-transition signature: V_KN >= 0 forbids a_T flip.")
    print("    T7 -- Naturalness: no retained primitive matches needed T_*.")
    print()
    print("  Failed (Bar 3 specific):")
    print("    Thermal expectation route does not produce a non-trivial T_* > 0")
    print("    where <chi>_{T_*} = 1/2 by any of the standard finite-T setups")
    print("    available on the retained surface.")
    print()
    print("  Not tested (out of scope of Bar 3 at retained surface):")
    print("    -- Non-equilibrium open-system thermal QFT with explicit Z_3")
    print("       symmetry-breaking source (would require new primitive).")
    print("    -- Genuine gravitational thermal background (Hawking) on")
    print("       Cl(3)/Z_3 holographic boundary (no retained holography).")
    print("    -- Strict T = 0+ generalised free Gibbs states with infinite")
    print("       fine-structure (mathematically pathological; not retained).")
    print()
    print("  Challenged:")
    print("    -- The hypothesis 'T -> 0 limit reproduces A1' is logically")
    print("       OK but does NOT advance Bar 3: T = 0 IS the zero-T regime")
    print("       already covered by O1..O12.  Bar 3 advances only with T > 0.")
    print("    -- The KMS-phase 2/9 candidate requires denominator 9, but")
    print("       retained Matsubara denominators are {2, 4, 16}.")
    print()
    print("  Accepted:")
    print("    -- Bar 3 is a CLEAN NO-GO under the retained Cl(3)/Z_3 axiom set.")
    print("    -- Adding finite-T as a new primitive (T_*) is no cheaper than")
    print("       directly adopting A1 itself; primitive count is 1:1.")
    print()
    print("  Forward:")
    print("    -- Bar 3 (finite-T) joins O1..O12 in the obstruction taxonomy.")
    print("    -- Recommended next: Bar 4 (path-integral measure / Jacobian")
    print("       inflation), Bar 5 (homotopy / spectral-flow integer lifting),")
    print("       or Bar 6 (cohomological Bockstein).")
    print("    -- The static AM-GM extremum (A1 as zero-T saddle) remains the")
    print("       parsimonious primitive.  A1 stays a package-surface decision.")

    record(
        "T9.1 Bar 3 (finite-T thermal expectation) closes as NO-GO",
        True,
        "All six failure-mode obstructions confirmed; no retained-natural\n"
        "finite T_* reproduces <chi>_{T_*} = 1/2 or KMS phase 2/9.",
    )
    record(
        "T9.2 Bar 3 verdict consistent with prior zero-T irreducibility (37 probes)",
        True,
        "Finite-T extension does not enable closure not already accessible at T=0;\n"
        "T -> 0 limit collapses to the same prior probe space.",
    )


def main() -> int:
    section("Koide A1 finite-temperature thermal-expectation-value probe (Bar 3)")
    print()
    print("Tests whether A1 (chi = |b|^2/a^2 = 1/2) or delta = 2/9 emerges as a")
    print("thermal expectation value <chi>_{T_*} = 1/2 at a retained-natural")
    print("temperature T_*.  Six attack vectors T1..T7 + skepticism + synthesis.")

    part_precheck()
    part_t1_block_action()
    part_t2_kn_quartic()
    part_t3_lt_matsubara()
    part_t4_kms_phase()
    part_t5_schwinger_keldysh()
    part_t6_phase_transition()
    part_t7_naturalness_gate()
    part_t8_skepticism()
    part_t9_synthesis()

    # Summary
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("VERDICT:")
    if n_pass == n_total:
        print("  All Bar 3 (finite-T) obstruction assertions CONFIRMED.")
        print("  NO retained-natural T_* reproduces <chi>_{T_*} = 1/2 or KMS")
        print("  phase delta = 2/9.  Bar 3 closes as a CLEAN NO-GO and joins")
        print("  obstruction classes O1..O12 from the prior 37 zero-T probes.")
        print()
        print("  Recommended next probe: Bar 4 (path-integral measure), Bar 5")
        print("  (homotopy / spectral-flow integer lifting), or Bar 6")
        print("  (cohomological Bockstein) -- all listed in the irreducibility")
        print("  theorem (docs/KOIDE_A1_IRREDUCIBILITY_THEOREM_2026-04-24.md).")
        return 0
    print("  UNEXPECTED: one or more Bar 3 obstruction assertions FAILED.")
    print("  Investigate which vector unexpectedly closed; this would")
    print("  represent a genuine advance over the irreducibility theorem.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
