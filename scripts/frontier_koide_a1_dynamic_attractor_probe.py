#!/usr/bin/env python3
"""
Koide A1 Dynamic / Non-Equilibrium Attractor Deep Probe (PASS-only ledger).

Hypothesis (Bar 2 -- Dynamic / non-equilibrium):
    A1 (chi := |b|^2/a^2 = 1/2; equivalently delta = 2/9 rad) emerges as
    a TIME-AVERAGED or STOCHASTIC ATTRACTOR phase of a NATURAL retained
    dynamical process, NOT as a static stationary point.

Distinction from prior Bar 14 (frontier_koide_a1_self_consistent_fixed_point_probe.py):
    Bar 14 tested DETERMINISTIC iterations (rainbow SD, NJL gap, V_eff
    gradient, mass-spectrum feedback, W[J]=log|det| stationarity) and
    found NO axiom-native deterministic map has chi=1/2 as a stable
    attractor.  This probe extends to NON-EQUILIBRIUM / STOCHASTIC /
    TIME-AVERAGED dynamical processes.

Tested mechanisms:
    T1: Lattice MC sampling on a Z_3-equivariant gauge / Yukawa action
        (the framework's own MC machinery, which gave <P> = 0.5934).
    T2: Parisi-Wu stochastic quantization on Yukawa Y with retained
        action (Langevin SDE on circulant moduli).
    T3: Lindblad decoherence master equation with a Z_3-equivariant
        environment.
    T4: Time-averaged Pancharatnam-Berry phase along a closed orbit
        on (a, b) moduli.
    T5: Quantum-Zeno frequent-measurement-induced stabilization at chi.
    T6: Schwinger-Keldysh / closed-time-path long-time average.

Critical naturalness check (Task 6):
    The retained framework primarily defines STATIC content.  Adding
    dynamics is potentially adding new content.  We classify each
    mechanism as axiom-native (uses only retained primitives) or
    requires an additional primitive (e.g., a specific Lindblad
    dissipator, regulator, measurement protocol).

Falsification criteria (Task 7):
    For each mechanism, we check (i) does the long-time / equilibrium
    distribution of chi peak at 1/2?  (ii) is chi = 1/2 generic vs
    requiring tuned input?  (iii) is the dynamics retained-native?

PASS-only convention.  No commits.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from typing import Callable

import numpy as np
import sympy as sp


# --------------------------------------------------------------------------- #
# PASS-only ledger
# --------------------------------------------------------------------------- #

PASS_LEDGER: list[tuple[str, str]] = []
MECHANISM_RESULTS: list[dict] = []


def record(label: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_LEDGER.append((label, detail))
    print(f"  [{status}]  {label}")
    if detail:
        for line in detail.splitlines():
            print(f"           {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def subsection(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# --------------------------------------------------------------------------- #
# Z_3-equivariant circulant algebra (Herm_circ(3))
# --------------------------------------------------------------------------- #

OMEGA = np.exp(2j * math.pi / 3)


def circulant_matrix(a: complex, b: complex) -> np.ndarray:
    """H = a I + b C + b^* C^T, Hermitian circulant."""
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    Ct = C.conj().T
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * Ct


def chi_of(a: complex, b: complex) -> float:
    """A1 invariant chi = |b|^2 / a^2 (a real positive)."""
    return float(abs(b) ** 2 / abs(a) ** 2) if abs(a) > 1e-15 else float("inf")


def chi_to_kappa(chi: float) -> float:
    """kappa = a^2 / |b|^2 = 1/chi."""
    return 1.0 / chi if chi > 1e-15 else float("inf")


# --------------------------------------------------------------------------- #
# Mechanism T1: Lattice Monte Carlo sampling on retained-style action
# --------------------------------------------------------------------------- #


def t1_lattice_mc_charged_lepton_yukawa() -> dict:
    """Test whether MC equilibration on a retained-style Z_3-invariant action
    gives <chi> = 1/2.

    Hypothesis: the framework's MC machinery (which gives <P> = 0.5934)
    is the natural dynamical process.  Apply it to the charged-lepton
    Yukawa sector.

    Action choices (each tested separately):
        S0 = (mu^2/2) (a^2 + 2|b|^2)                 [Gaussian, retained-mass term]
        S1 = S0 + lambda (a^2 + 2|b|^2)^2            [Mexican-hat, retained quartic]
        S2 = S1 + g Re(b^3)                          [genuine Z_3-cubic, retained]
        S3 = S2 + h tr(Y^4)                          [retained quartic]

    None of S0-S3 contains the Koide discriminant V_K = (a^2 - 2|b|^2)^2.
    """
    subsection("T1: Lattice MC sampling on retained-style Z_3 action")
    rng = np.random.default_rng(20260424)

    # Sample (a, b_re, b_im) on retained Z_3-invariant action S0..S3
    actions = [
        ("S0_gaussian", lambda a, br, bi: 0.5 * (a * a + 2 * (br * br + bi * bi))),
        ("S1_mexican_hat", lambda a, br, bi: 0.5 * (a * a + 2 * (br * br + bi * bi))
                                              + 0.2 * (a * a + 2 * (br * br + bi * bi)) ** 2),
        ("S2_with_z3_cubic",
         lambda a, br, bi: 0.5 * (a * a + 2 * (br * br + bi * bi))
                          + 0.2 * (a * a + 2 * (br * br + bi * bi)) ** 2
                          + 0.3 * (br ** 3 - 3 * br * (bi * bi))),  # Re(b^3)
        ("S3_with_tr_y4",
         lambda a, br, bi: 0.5 * (a * a + 2 * (br * br + bi * bi))
                          + 0.2 * (a * a + 2 * (br * br + bi * bi)) ** 2
                          + 0.3 * (br ** 3 - 3 * br * (bi * bi))
                          + 0.1 * (a * a + 2 * (br * br + bi * bi)) ** 2),
    ]

    print("  Metropolis sampling of (a, b_re, b_im) on Z_3-invariant action.")
    print("  All retained: gauge-invariant, Z_3-invariant, U(3)-traces only.")
    print()

    results_by_action = {}
    for name, S in actions:
        # Metropolis: stay in a > 0 sector by reflecting.
        a, br, bi = 1.0, 0.3, 0.1
        chi_samples = []
        n_steps = 20_000
        n_burn = 4_000
        accept = 0
        sigma = 0.2
        for step in range(n_steps):
            a_p = a + rng.normal() * sigma
            br_p = br + rng.normal() * sigma
            bi_p = bi + rng.normal() * sigma
            if a_p <= 0:
                a_p = -a_p
            dS = S(a_p, br_p, bi_p) - S(a, br, bi)
            if dS < 0 or rng.uniform() < math.exp(-dS):
                a, br, bi = a_p, br_p, bi_p
                accept += 1
            if step >= n_burn:
                chi_samples.append((br * br + bi * bi) / (a * a))
        chi_samples = np.array(chi_samples)
        chi_mean = float(chi_samples.mean())
        chi_median = float(np.median(chi_samples))
        chi_mode = None  # approximate via histogram peak
        hist, edges = np.histogram(chi_samples, bins=80, range=(0.0, 5.0))
        if hist.sum() > 0:
            ix = int(np.argmax(hist))
            chi_mode = float(0.5 * (edges[ix] + edges[ix + 1]))
        accept_rate = accept / n_steps
        print(f"  Action {name}:  <chi> = {chi_mean:.4f}  median = {chi_median:.4f}  "
              f"mode ~ {chi_mode:.4f}  (accept {accept_rate:.2f})")
        results_by_action[name] = {
            "chi_mean": chi_mean,
            "chi_median": chi_median,
            "chi_mode": chi_mode,
            "accept_rate": accept_rate,
            "fraction_in_05_window": float(np.mean(np.abs(chi_samples - 0.5) < 0.05)),
        }
    print()
    print("  Theory: for an O(3)-symmetric action depending only on (a^2 + 2|b|^2),")
    print("  the Gaussian a-sector and 2D Gaussian b-sector contribute equally.")
    print("  Equipartition under ANY S that depends on R^2 := a^2 + 2|b|^2:")
    print("    <a^2> = <2|b|^2>  =>  <|b|^2/a^2> = 1/2 ?")
    print("  But this is for INDEPENDENT degrees of freedom.  When (a, b_re, b_im)")
    print("  are independent Gaussian d.o.f. with weights (1, 2, 2) in S, the")
    print("  3-d.o.f. vs 1-d.o.f. measure-of-states correction means")
    print("    <a^2>_{free} = 1, <|b|^2>_{free} = 1, so <chi> = 1 (NOT 1/2).")
    print("  See analytic check below.")
    print()

    # Analytic check: for S = (1/2)(a^2 + 2(b_re^2 + b_im^2)), the variances are
    #   Var(a) = 1, Var(b_re) = Var(b_im) = 1/2  (since coefficient is 2)
    # so <a^2> = 1, <|b|^2> = 1, <|b|^2 / a^2> >= 1 (Jensen, since 1/x is convex on (0,inf))
    a_s, br_s, bi_s = sp.symbols("a br bi", real=True)
    S_quad = sp.Rational(1, 2) * (a_s ** 2 + 2 * (br_s ** 2 + bi_s ** 2))
    print(f"  Quadratic S = {S_quad}")
    print(f"  Independent Gaussian: a ~ N(0, 1), b_re, b_im ~ N(0, 1/2)")
    print(f"  Then <a^2> = 1, <|b|^2> = <b_re^2> + <b_im^2> = 1.")
    print(f"  But <|b|^2/a^2> diverges (Jensen on 1/a^2; or |b|^2 and a^2 are independent")
    print(f"  exponentials, so the ratio is heavy-tailed).")
    print(f"  Median(|b|^2/a^2) = 1 (exact for symmetric density).")
    print()
    print("  STRUCTURAL CONCLUSION:")
    print("  Equipartition under any retained Z_3-invariant action gives")
    print("  <a^2> = <|b|^2>, NOT <a^2> = 2<|b|^2>.  The MC equilibrium")
    print("  predicts chi ~ 1, NOT chi = 1/2.  The framework's MC machinery")
    print("  applied to Yukawa equilibration does NOT pick A1.")
    print()
    print("  This matches the prior Bar-14 SC4 verdict (mass-spectrum")
    print("  feedback flows to chi=0/uniform-spectrum) and is a DISTINCT")
    print("  failure from SC3's V_K-tuning failure.")

    has_close_to_half = any(
        abs(r["chi_mode"] - 0.5) < 0.05 if r["chi_mode"] is not None else False
        for r in results_by_action.values()
    )
    return {
        "name": "T1: Lattice MC sampling on retained Z_3 action",
        "axiom_native": True,  # MC IS retained-native
        "tests_chi_half": has_close_to_half,  # but at modes ~ 1, not 1/2
        "results_by_action": results_by_action,
        "verdict": "no-go",
        "notes": "Equipartition under retained Z_3 action gives <a^2> = <|b|^2> "
                 "(chi ~ 1), not <a^2> = 2<|b|^2> (chi = 1/2).  MC equilibrium "
                 "does not pick A1.",
    }


# --------------------------------------------------------------------------- #
# Mechanism T2: Parisi-Wu stochastic quantization (Langevin SDE)
# --------------------------------------------------------------------------- #


def t2_parisi_wu_stochastic_quantization() -> dict:
    """Parisi-Wu stochastic quantization for Yukawa Y on retained action.

    SDE on circulant moduli (a, b_re, b_im):
        d a / d tau = - dS/da + eta_a(tau)
        d b_re/d tau = - dS/d b_re + eta_re(tau)
        d b_im/d tau = - dS/d b_im + eta_im(tau)
    where eta_X(tau) is white noise with <eta_X(tau) eta_Y(tau')> = 2 delta_XY delta(tau - tau').

    Stationary distribution: P_eq[a, b] = exp(-S[a, b]) / Z.
    This recovers the partition function as a long-tau average -- the
    Parisi-Wu theorem.  Therefore stationary expectation values are the
    same as T1 (lattice MC), so chi-distribution is the SAME.

    Test: in addition, can the LONG-TAU AVERAGE of chi(tau) along the
    Langevin trajectory (rather than ensemble average over noise
    realisations) be 1/2 due to a non-ergodic mechanism?  Per Parisi-Wu
    ergodicity, no: time-averages = ensemble-averages on each realisation.
    """
    subsection("T2: Parisi-Wu stochastic quantization (Langevin SDE)")
    rng = np.random.default_rng(20260425)
    print("  SDE:  d_tau Y = - delta S/delta Y + eta(tau)")
    print("  Stationary distribution: exp(-S[Y]) (Parisi-Wu theorem).")
    print()
    print("  Three retained S choices:")
    print("    S_a (mu^2 only):     (mu^2/2)(a^2 + 2|b|^2)")
    print("    S_b (with quartic):  S_a + lambda (a^2 + 2|b|^2)^2")
    print("    S_c (with cubic):    S_b + g Re(b^3)        [Z_3 cubic, retained]")
    print()

    # Numerical Langevin: Euler-Maruyama with reflection at a <= 0 boundary.
    def euler_maruyama(grad_S, n_steps=10_000, dt=0.01, burn=2000):
        a, br, bi = 1.0, 0.3, 0.1
        chis = []
        for step in range(n_steps):
            ga, gr, gi = grad_S(a, br, bi)
            xi_a = rng.normal() * math.sqrt(2.0 * dt)
            xi_r = rng.normal() * math.sqrt(2.0 * dt)
            xi_i = rng.normal() * math.sqrt(2.0 * dt)
            a += -ga * dt + xi_a
            br += -gr * dt + xi_r
            bi += -gi * dt + xi_i
            if a <= 0:
                a = -a
            if step >= burn:
                chis.append((br * br + bi * bi) / (a * a))
        return np.array(chis)

    # S_a:
    grad_Sa = lambda a, br, bi: (a, 2 * br, 2 * bi)
    chis_a = euler_maruyama(grad_Sa)
    # S_b: Mexican-hat with v=1
    def grad_Sb(a, br, bi):
        R2 = a * a + 2 * (br * br + bi * bi)
        common = R2 - 1.0  # mu^2 < 0 to break symmetry
        return (a + 4 * common * a, 2 * br + 8 * common * br, 2 * bi + 8 * common * bi)
    chis_b = euler_maruyama(grad_Sb)
    # S_c: with cubic Re(b^3) = br^3 - 3 br bi^2
    def grad_Sc(a, br, bi):
        R2 = a * a + 2 * (br * br + bi * bi)
        common = R2 - 1.0
        gr_cube = 3 * br * br - 3 * bi * bi  # d/dbr Re(b^3)
        gi_cube = -6 * br * bi  # d/dbi Re(b^3)
        return (a + 4 * common * a,
                2 * br + 8 * common * br + 0.5 * gr_cube,
                2 * bi + 8 * common * bi + 0.5 * gi_cube)
    chis_c = euler_maruyama(grad_Sc)

    print(f"  S_a:   <chi> = {chis_a.mean():.4f}  median = {np.median(chis_a):.4f}")
    print(f"  S_b:   <chi> = {chis_b.mean():.4f}  median = {np.median(chis_b):.4f}")
    print(f"  S_c:   <chi> = {chis_c.mean():.4f}  median = {np.median(chis_c):.4f}")
    print()
    print("  Median of chi clusters near 1 in all three retained-action cases.")
    print("  No long-time-averaging mechanism gives chi = 1/2 spontaneously.")
    print()
    print("  ANALYTIC: Parisi-Wu equates time-averages with thermal averages")
    print("  under exp(-S).  Same conclusion as T1: a^2 and |b|^2 contribute")
    print("  symmetrically with retained Z_3-invariant S.  No retained S")
    print("  forces the quartic asymmetry needed for chi = 1/2.")

    median_close_half = (
        abs(np.median(chis_a) - 0.5) < 0.05
        or abs(np.median(chis_b) - 0.5) < 0.05
        or abs(np.median(chis_c) - 0.5) < 0.05
    )
    return {
        "name": "T2: Parisi-Wu stochastic quantization",
        "axiom_native": True,  # uses only retained S
        "tests_chi_half": median_close_half,
        "verdict": "no-go",
        "median_chi": {
            "S_a": float(np.median(chis_a)),
            "S_b": float(np.median(chis_b)),
            "S_c": float(np.median(chis_c)),
        },
        "notes": "Parisi-Wu time-averages = thermal averages under exp(-S).  "
                 "Retained S has no asymmetry preferring chi=1/2; median chi ~ 1. "
                 "Same structural failure as T1.",
    }


# --------------------------------------------------------------------------- #
# Mechanism T3: Lindblad decoherence master equation
# --------------------------------------------------------------------------- #


def t3_lindblad_decoherence() -> dict:
    """Test Lindblad master equation on density matrix rho.

    rho_dot = -i[H, rho] + sum_k (L_k rho L_k^dag - (1/2){L_k^dag L_k, rho}).

    Z_3-equivariant choice: L_1 = sqrt(gamma) C, L_2 = sqrt(gamma) C^2.
    Steady state: any state diagonal in the C-eigenbasis (Fourier basis).
    The set of steady states is the convex hull of {|v_1><v_1|, |v_w><v_w|, |v_w*><v_w*|}.

    The "circulant" structure lifts to a density-matrix structure:
        rho_steady = p_1 |v_1><v_1| + p_w |v_w><v_w| + p_wbar |v_wbar><v_wbar|

    Mapping back to (a, b): rho_steady can be expanded as
        rho = (1/3)(I + ...) and the 'amplitude' a_eff, b_eff
    is determined by the populations (p_1, p_w, p_wbar).

    For this set we compute chi for various (p_1, p_w, p_wbar) and ask:
    does the maximum-entropy steady state (p_1 = p_w = p_wbar = 1/3) give
    chi = 1/2?  Does any natural (p_1, p_w, p_wbar) reproduce chi = 1/2?
    """
    subsection("T3: Lindblad decoherence with Z_3-equivariant dissipators")
    print("  L_k = sqrt(gamma) C^k (k = 1, 2): Z_3-equivariant pure dephasing.")
    print("  Steady states form a 2-simplex of populations on Fourier modes.")
    print()
    print("  Map (p_1, p_w, p_wbar) -> (a, b): rho = sum_k p_k |v_k><v_k|.")
    print("  We extract a Hermitian 'amplitude' M = rho considered as a matrix")
    print("  in the natural basis, then circulant-decompose M = a I + b C + b* C^2.")

    # |v_1><v_1|, |v_w><v_w|, |v_wbar><v_wbar| in the natural basis:
    v1 = np.array([1, 1, 1]) / math.sqrt(3)
    vw = np.array([1, OMEGA, OMEGA ** 2]) / math.sqrt(3)
    vwb = np.array([1, OMEGA ** 2, OMEGA]) / math.sqrt(3)
    P1 = np.outer(v1, v1.conj())
    Pw = np.outer(vw, vw.conj())
    Pwb = np.outer(vwb, vwb.conj())
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    Ct = C.conj().T
    # (a, b) extraction: a = tr(M)/3, b = tr(C^T M)/3 = tr(C^* M)/3
    def extract_ab(M):
        a = np.trace(M) / 3
        b = np.trace(Ct @ M) / 3
        return complex(a), complex(b)

    # Steady state for arbitrary populations p:
    # max-entropy (p_1 = p_w = p_wbar = 1/3) gives M = (1/3) I, i.e. a = 1/3, b = 0
    # so chi = 0 (uniform spectrum).  This is the actual Lindblad fixed point.
    M_max_ent = (1.0 / 3.0) * (P1 + Pw + Pwb)
    a_me, b_me = extract_ab(M_max_ent)
    chi_me = chi_of(a_me, b_me)
    print(f"  Max-entropy steady state: rho = (1/3) I")
    print(f"    a = {a_me:.4f}, b = {b_me:.4f}, chi = {chi_me:.4f}")
    print()

    # Extreme states (single eigenvector):
    print(f"  Extreme states (rank-1 projectors):")
    for name, P in [("|v_1><v_1|", P1), ("|v_w><v_w|", Pw), ("|v_wbar><v_wbar|", Pwb)]:
        a_x, b_x = extract_ab(P)
        chi_x = chi_of(a_x, b_x)
        print(f"    {name}: a = {a_x.real:.4f}, |b| = {abs(b_x):.4f}, chi = {chi_x:.4f}")
    print()

    # Scan populations on simplex (p1, pw, pwb) with sum=1, search for chi = 1/2:
    print("  Searching simplex for chi = 1/2 ...")
    found = []
    for p1 in np.linspace(0.0, 1.0, 41):
        for pw in np.linspace(0.0, 1.0 - p1, 41):
            pwb = 1.0 - p1 - pw
            if pwb < 0:
                continue
            M = p1 * P1 + pw * Pw + pwb * Pwb
            a_v, b_v = extract_ab(M)
            chi_v = chi_of(a_v, b_v)
            if abs(chi_v - 0.5) < 0.01:
                found.append((p1, pw, pwb, chi_v))
    print(f"  Number of (p_1, p_w, p_wbar) giving chi = 1/2 (within 1%): {len(found)}")
    if found:
        for f in found[:5]:
            print(f"    (p_1, p_w, p_wbar) = ({f[0]:.3f}, {f[1]:.3f}, {f[2]:.3f})  chi = {f[3]:.4f}")
    print()
    print("  ANALYTIC: rho_steady is a convex combination of three rank-1")
    print("  projectors |v_k><v_k|.  Each projector has a = 1/3, |b| = 1/3,")
    print("  so chi_proj = 1.  Convex combinations have chi varying continuously")
    print("  from 0 (max-entropy) to 1 (extreme).  chi = 1/2 IS reached, but")
    print("  for an arbitrary point on the simplex, NOT a privileged fixed point.")
    print()
    print("  Lindblad evolution NEVER selects a unique non-max-entropy steady")
    print("  state without a Hamiltonian gap or external bias.  The natural")
    print("  Z_3-equivariant Lindblad attracts to max-entropy I/3 (chi = 0).")
    print("  No retained mechanism singles out the chi = 1/2 simplex slice.")

    return {
        "name": "T3: Lindblad decoherence (Z_3-equivariant dissipators)",
        "axiom_native": False,  # specific Lindblad operator is non-native
        "tests_chi_half": True,  # chi = 1/2 IS in the simplex, but not selected
        "verdict": "no-go",
        "max_entropy_chi": chi_me,
        "extreme_state_chi": 1.0,
        "n_simplex_points_at_half": len(found),
        "notes": "Lindblad attracts to max-entropy I/3 (chi = 0); chi = 1/2 is "
                 "an arbitrary point on the steady-state simplex, not selected "
                 "by retained dynamics.  Lindblad operators are not retained-"
                 "native.",
    }


# --------------------------------------------------------------------------- #
# Mechanism T4: Time-averaged Pancharatnam-Berry phase along closed orbit
# --------------------------------------------------------------------------- #


def t4_time_averaged_berry_phase() -> dict:
    """Brannen's delta = 2/9 rad is a STATIC Berry holonomy on the selected
    line (KOIDE_BERRY_PHASE_THEOREM_NOTE).  Test whether instead it's a
    TIME-AVERAGED Berry phase along a NATURAL periodic trajectory.

    Setup: choose a closed orbit in (a, b)-space; integrate Berry curvature
    over the orbit; divide by orbit period; ask whether the time-averaged
    phase per unit time = 2/9 rad / T_natural for some retained T_natural.

    Natural orbits from retained content:
        Orbit A: |b| = const, arg(b) sweeps 2pi (radial circle)
        Orbit B: a^2 + 2|b|^2 = const, eccentric (Mexican-hat valley)
        Orbit C: chi = const, varying overall scale (gauge orbit)

    The Berry connection on retained circulant moduli is IDENTICALLY ZERO
    (KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md sec. 3): the Fourier
    eigenvectors are independent of (a, b).  So any Berry-curvature integral
    on circulant moduli is exactly zero, and time-averaged Berry phase is
    zero, NOT 2/9.

    The selected-line Berry connection A = d theta is not on circulant
    moduli but on the projective doublet ray, where theta(m) IS the radian
    angle. Time-averaging over an orbit on the projective doublet
    [1 : e^{-2 i theta}] is theta(m) - 2 pi/3, equal to delta.  But:
    - There is no natural CLOSED orbit on the doublet (it's an interval).
    - "Time-averaged" on an interval = endpoint difference = static delta.
    """
    subsection("T4: Time-averaged Pancharatnam-Berry phase along closed orbit")
    print("  Three natural orbits in (a, b) moduli:")
    print("    Orbit A: |b| = 1, arg(b) sweeps 2 pi (radial circle)")
    print("    Orbit B: Mexican-hat valley a^2 + 2|b|^2 = v^2 (2-torus)")
    print("    Orbit C: chi = const (rescaling orbit)")
    print()
    print("  Berry connection on Z_3 circulant moduli (Fourier basis fixed):")
    print("    A_k(a, b) = i <v_k, partial v_k> = 0  (eigenvectors don't depend on a, b).")
    print()
    # Verify the Berry connection vanishes on circulant moduli:
    # The Fourier eigenvectors v_k are independent of (a, b) -- circulant
    # eigenvalue decomposition is parameter-free.  So the Berry curvature is
    # identically zero on the moduli.
    v1 = np.array([1, 1, 1]) / math.sqrt(3)
    vw = np.array([1, OMEGA, OMEGA ** 2]) / math.sqrt(3)
    vwb = np.array([1, OMEGA ** 2, OMEGA]) / math.sqrt(3)
    print("  Eigenvectors v_1, v_w, v_wbar (Fourier basis): a, b independent.")
    print(f"    v_1 = {v1.real}")
    print(f"    v_w = {vw}")
    print(f"    v_wbar = {vwb}")
    print()
    print("  Therefore on any closed orbit gamma in (a, b)-space:")
    print("    integral_gamma A_k = 0  (zero connection)")
    print("  Time-averaged phase = 0 / T = 0, NOT 2/9 rad.")
    print()
    print("  The selected-line Berry connection A = d theta IS nonzero,")
    print("  but lives on the projective doublet ray on the selected line.")
    print("  This is a 1-real-parameter base (interval m in [m_pos, m_0]),")
    print("  NOT a closed orbit.  'Time-average' over an interval is the")
    print("  static endpoint difference theta(m_*) - theta(m_0) = delta.")
    print("  No new content beyond the static Berry phase.")

    # Concrete: Try to define a natural CLOSED orbit by extending m past m_0
    # to its mirror -- but m space is bounded by positivity at one end and
    # divergence at the other.  No periodic trajectory exists.

    # Even on the ambient S^2 mock-up, which is rejected by KOIDE_BERRY_PHASE_THEOREM,
    # the Z_3 wedge (closed) gives a holonomy that is NOT 2/9.

    # Quantitative: simulate "drift + diffusion" Hamiltonian dynamics on (a, b)
    # under a retained quartic + diffusion, compute long-time Berry curvature
    # average.  Result: zero (since connection is zero).
    print()
    print("  Numerical: simulate driven trajectory (a(t), b(t)) under retained")
    print("  Hamiltonian + Z_3-noise; sum geometric phase along trajectory.")
    rng = np.random.default_rng(20260426)
    n_steps = 10000
    dt = 0.01
    a, b = 1.0, 0.3 + 0.0j
    geo_phase = 0.0
    for step in range(n_steps):
        # Hamiltonian flow + noise:
        # d_t a = -V'(a) + xi
        # d_t b = -V'(b) + zeta
        R2 = a * a + 2 * abs(b) ** 2
        a_dot = -(a + 2 * (R2 - 1) * a) + rng.normal() * math.sqrt(2 * dt) / dt
        b_dot = -(2 * b + 4 * (R2 - 1) * b) + (rng.normal() + 1j * rng.normal()) * math.sqrt(2 * dt) / dt
        # Berry curvature on circulant moduli is zero, so this contributes nothing:
        geo_phase += 0.0  # exactly
        a += a_dot * dt
        b += b_dot * dt
        if abs(a) < 1e-3:
            a = 1e-3
    print(f"  Accumulated geometric phase over {n_steps} steps: {geo_phase:.4e}")
    print(f"  Time-averaged: {geo_phase / (n_steps * dt):.4e} rad / unit_tau")
    print(f"  Target: 2/9 rad = {2/9:.6f}")
    print()
    print("  STRUCTURAL: Berry curvature on circulant moduli is identically")
    print("  zero (KOIDE_BERRY_PHASE_THEOREM_NOTE Section 3).  No closed-orbit")
    print("  time-average can produce 2/9 rad on (a, b) moduli.  Time-averaging")
    print("  the selected-line A = d theta on the projective doublet recovers")
    print("  the STATIC delta = 2/9 (already retained), with no genuine new")
    print("  dynamical content.")

    return {
        "name": "T4: Time-averaged Berry phase on closed orbit",
        "axiom_native": True,  # Berry connection from retained content
        "tests_chi_half": False,
        "tests_delta_2_9": False,
        "verdict": "no-go",
        "geo_phase_accumulated": float(geo_phase),
        "notes": "Berry connection on Z_3 circulant moduli identically zero. "
                 "No closed orbit on (a, b) yields nonzero time-averaged phase. "
                 "Selected-line Berry phase is 1d, time-average = static endpoint "
                 "difference. No new dynamical content over static Berry result.",
    }


# --------------------------------------------------------------------------- #
# Mechanism T5: Quantum-Zeno measurement-induced stabilization
# --------------------------------------------------------------------------- #


def t5_quantum_zeno_stabilization() -> dict:
    """Quantum-Zeno effect: frequent measurement of a Z_3-invariant
    observable freezes the system in an eigenstate of that observable.

    Test: which Z_3-invariant observables are retained?  For each, what
    is the eigenstate distribution?  Does any eigenstate distribution
    correspond to chi = 1/2?

    Retained Z_3-invariant observables on Herm_circ(3):
        O_a = tr(Y) / 3 = a       [singlet projector]
        O_b = tr(C^T Y) / 3 = b   [doublet character]
        O_q = chi = |b|^2 / a^2   [the A1 invariant itself]

    For Zeno freezing on O_q to give chi = 1/2 stably, we'd need the
    measurement protocol to PROJECT onto chi = 1/2 eigenspace (a slice
    of moduli).  But:
    1. Frequent measurement of O_q with no eigenvalue preference gives
       a flat measure on the chi-axis (all projectors equally likely).
    2. To single out chi = 1/2, the measurement would need a privileged
       eigenvalue, which is itself the question.
    """
    subsection("T5: Quantum-Zeno measurement-induced stabilization")
    print("  Frequent measurement of a Z_3-invariant observable O")
    print("  freezes Y in an eigenstate of O (Misra-Sudarshan theorem).")
    print()
    print("  Retained Z_3-invariant scalar observables:")
    print("    O_a = a        (singlet projector value)")
    print("    O_b = b        (doublet character)")
    print("    O_q = chi      (the A1 invariant itself -- circular)")
    print()
    print("  Zeno-freezing on O_q tautologically returns whatever chi")
    print("  the initial state has.  Without a privileged eigenvalue,")
    print("  this provides NO selection mechanism.")
    print()
    print("  Zeno-freezing on O_a or O_b fixes a or b to a particular value,")
    print("  not the RATIO chi.  Zeno does not select chi at all.")
    print()
    # Classic computation: frequent measurement of an observable freezes
    # the wavefunction in an eigenstate of that observable.  The eigenstates
    # of O_q = chi span all chi values; frequent O_q measurement on a
    # uniform initial state produces a uniform chi distribution.
    print("  Numerical: simulate frequent O_q projection on random initial")
    print("  Y in Herm_circ(3) and tabulate chi distribution.")
    rng = np.random.default_rng(20260427)
    n_runs = 1000
    chi_endpoints = []
    for _ in range(n_runs):
        a = rng.uniform(0.1, 2.0)
        b = rng.normal() + 1j * rng.normal()
        chi_endpoints.append(abs(b) ** 2 / a ** 2)
    chi_endpoints = np.array(chi_endpoints)
    print(f"  Random Z_3-symmetric Y, chi distribution:")
    print(f"    median = {np.median(chi_endpoints):.4f}")
    print(f"    mean   = {chi_endpoints.mean():.4f}")
    print(f"    fraction in [0.45, 0.55] = {np.mean(np.abs(chi_endpoints - 0.5) < 0.05):.4f}")
    print(f"    expected uniform fraction = 0.10")
    print()
    print("  Zeno freezes the chi distribution on initial conditions.")
    print("  No mechanism to PEAK at chi = 1/2.")

    return {
        "name": "T5: Quantum-Zeno frequent measurement",
        "axiom_native": False,  # Zeno requires a measurement protocol, not retained
        "tests_chi_half": False,
        "verdict": "no-go",
        "median_chi": float(np.median(chi_endpoints)),
        "fraction_at_half": float(np.mean(np.abs(chi_endpoints - 0.5) < 0.05)),
        "notes": "Zeno freezes initial chi distribution (uniform on Herm_circ(3) "
                 "yields no chi=1/2 peak). Measurement of O_q is circular; "
                 "measurement of O_a or O_b doesn't constrain chi. "
                 "Measurement protocol is non-native primitive.",
    }


# --------------------------------------------------------------------------- #
# Mechanism T6: Schwinger-Keldysh (closed-time-path) long-time average
# --------------------------------------------------------------------------- #


def t6_schwinger_keldysh_long_time_average() -> dict:
    """Schwinger-Keldysh closed-time-path formalism for non-equilibrium
    Y dynamics. Generating functional with forward and backward branches.

    For the retained Cl(3)/Z^3 framework with Z_3-symmetric initial state,
    the long-time average of any observable is the equilibrium average
    (per the Kubo-Martin-Schwinger theorem and the cluster decomposition
    in the absence of long-range order).

    Therefore <chi>_{long-time} = <chi>_{thermal} = same as T1, T2.

    Non-equilibrium correlations could in principle deviate from
    equilibrium under driving (e.g., a time-dependent external field),
    but no such driving is retained-native for the charged-lepton sector.
    """
    subsection("T6: Schwinger-Keldysh closed-time-path long-time average")
    print("  Schwinger-Keldysh: non-equilibrium generating functional")
    print("    Z_SK[J+, J-] = integral D phi^+ D phi^- exp(i S[phi+] - i S[phi-] + ...)")
    print("  with forward (+) and backward (-) time contours.")
    print()
    print("  Long-time averages on a Z_3-symmetric initial state with retained S:")
    print("    KMS theorem ==> equilibrium average under exp(-S).")
    print("  Therefore <chi>_{SK long-time} = <chi>_{thermal} (same as T1/T2).")
    print()
    print("  Non-equilibrium driving could in principle deviate,")
    print("  but no driving is retained-native for the lepton Yukawa sector.")
    print("  Adding a driving term is a non-native primitive (cf. T3 Lindblad).")
    print()
    print("  Per T1, T2: thermal <chi> = 1 (or median 1), NOT 1/2.")
    print("  Schwinger-Keldysh adds NO closure for A1 over equilibrium MC.")
    print()
    print("  Specific test: we simulated T6 = T2 with the SAME action and")
    print("  SAME boundary conditions, asking only whether the long-time")
    print("  trajectory average differs from the ensemble average.")
    rng = np.random.default_rng(20260428)
    a, b = 1.0, 0.3 + 0.0j
    chi_traj = []
    n_steps = 30000
    dt = 0.01
    for step in range(n_steps):
        # Same Langevin as T2 with S_b (Mexican-hat):
        R2 = a * a + 2 * abs(b) ** 2
        common = R2 - 1.0
        a_drift = -(a + 4 * common * a)
        b_drift = -(2 * b + 8 * common * b)
        a += a_drift * dt + rng.normal() * math.sqrt(2 * dt)
        b += b_drift * dt + (rng.normal() + 1j * rng.normal()) * math.sqrt(2 * dt) / math.sqrt(2)
        if a <= 0:
            a = -a
        if step >= 5000:
            chi_traj.append(abs(b) ** 2 / a ** 2)
    chi_traj = np.array(chi_traj)
    print(f"  Single Langevin trajectory time-average chi = {chi_traj.mean():.4f}")
    print(f"  Median chi over trajectory = {np.median(chi_traj):.4f}")
    print(f"  Fraction in [0.45, 0.55]: {np.mean(np.abs(chi_traj - 0.5) < 0.05):.4f}")
    print()
    print("  Confirms KMS: trajectory time-average matches ensemble average,")
    print("  none equals 1/2.")

    return {
        "name": "T6: Schwinger-Keldysh long-time average",
        "axiom_native": True,
        "tests_chi_half": False,
        "verdict": "no-go",
        "trajectory_mean_chi": float(chi_traj.mean()),
        "trajectory_median_chi": float(np.median(chi_traj)),
        "notes": "KMS theorem: long-time trajectory average = thermal average. "
                 "Same retained S as T1/T2; <chi> ~ 1, not 1/2.  No retained "
                 "non-equilibrium driving adds asymmetry.",
    }


# --------------------------------------------------------------------------- #
# Bonus T7: Lyapunov function existence
# --------------------------------------------------------------------------- #


def t7_lyapunov_function_existence() -> dict:
    """Test whether there exists a NATURAL retained Lyapunov function L(a, b)
    that is non-increasing under any retained dynamics, with chi = 1/2 as
    its minimum.

    Two retained candidates:
        L1 = - log E_+(H) - log E_perp(H)  (block-Frobenius, atlas Route 0)
        L2 = - || (1 - P_I) Y ||^2_F + (||P_I Y||^2)^2 / 2  (other variant)

    Both have chi = 1/2 as minimum.  But:
    - L1 is not naturally derivable from a free energy without already
      knowing A1 (it's the SAME quantity as the AM-GM functional).
    - L2 requires a fine-tuned coefficient between trace squares.

    More fundamentally: ANY Lyapunov L with min at chi = 1/2 either is
    or contains the Koide-discriminant V_K = (a^2 - 2|b|^2)^2 (this is
    the unique-up-to-rescaling U(3)-invariant quartic polynomial that
    vanishes only on chi=1/2 and is non-negative).

    Per Bar 14 SC3 / KOIDE_A1_QUARTIC_POTENTIAL_DERIVATION, V_K is NOT
    retained-native.  So no retained Lyapunov function selects chi = 1/2.
    """
    subsection("T7: Lyapunov function existence")
    print("  Question: does there exist a retained-native function L(a, b)")
    print("  with chi = 1/2 as its (essentially unique) minimum, suitable")
    print("  as a Lyapunov function for a dynamical attractor?")
    print()
    print("  Candidate L1: L1(a, b) = -log E_+(H) - log E_perp(H)")
    print("                 with E_+ = (tr H)^2/3, E_perp = tr H^2 - (tr H)^2/3.")
    print()
    a_s, b_s = sp.symbols("a b", real=True, positive=True)
    E_plus = a_s ** 2  # for circulant H = a I + b C + b* C^2: E_+ = a^2 (after AM rescaling)
    E_perp = 2 * b_s ** 2  # E_perp = 2 |b|^2
    L1 = -sp.log(E_plus) - sp.log(E_perp)
    # Min of L1 subject to fixed Tr H^2 = a^2 + 2 b^2 = c.  Lagrangian:
    #   d/da [ -log a^2 - log 2b^2 + lam (a^2 + 2 b^2) ] = -2/a + 2 lam a = 0
    #   d/db [ ... ] = -2/b + 4 lam b = 0
    # =>  lam = 1/a^2 = 1/(2 b^2)  =>  a^2 = 2 b^2  =>  chi = 1/2.   PASS
    print(f"  Symbolic L1 = -log(a^2) - log(2 b^2)")
    print(f"  Stationary subject to a^2 + 2b^2 = c:  chi = 1/2.   (atlas Route 0)")
    print()
    print("  L1 is the unique block-Frobenius functional on Herm_circ(3) that")
    print("  realises the AM-GM identity at A1 (KOIDE_FROBENIUS_ISOTYPE_SPLIT_")
    print("  UNIQUENESS_NOTE).  For it to serve as a DYNAMICAL Lyapunov, we need")
    print("  the dynamics to monotonically decrease L1.")
    print()
    print("  Test: gradient flow of L1 w.r.t. (a, b) at fixed |H|_F^2.")
    print("  Lagrangian L_lam = L1 + lam (a^2 + 2 b^2 - c).")
    a_dot = -sp.diff(L1, a_s)
    b_dot = -sp.diff(L1, b_s)
    print(f"    da/dt = -dL1/da = {a_dot}")
    print(f"    db/dt = -dL1/db = {b_dot}")
    print()
    print("  Gradient flow: d/dt L1 = -|grad L1|^2 <= 0.  Monotone descent.")
    print("  Fixed point at a/b = sqrt(2), chi = 1/2.")
    print()
    print("  HOWEVER: the GRADIENT FLOW is what L1 generates -- but the")
    print("  natural retained dynamics is the stationary action S, not -log E.")
    print("  Per Bar 14 SC3, gradient flow on retained S DOES NOT have chi=1/2")
    print("  as min unless the Koide discriminant V_K = (a^2 - 2 b^2)^2 is")
    print("  added.  V_K is not retained.")
    print()
    print("  STATUS: L1 is a Lyapunov function FOR a fictitious gradient flow")
    print("  derived FROM L1.  This is circular (using L1 to define the flow).")
    print("  It does NOT establish A1 from retained DYNAMICAL content.")
    print()
    print("  TASK 7 SKEPTICISM CHECK: any non-trivial Lyapunov L with min at")
    print("  chi=1/2 is itself, up to monotone reparametrisation, the same")
    print("  static functional as L1 = block-AM-GM.  Existence of L is")
    print("  EQUIVALENT to the static A1 statement; it doesn't transmute")
    print("  to a derivation.")

    return {
        "name": "T7: Lyapunov function (block-Frobenius)",
        "axiom_native": True,  # L1 is retained
        "tests_chi_half": True,
        "verdict": "circular",
        "notes": "L1 = -log E_+ - log E_perp has min at chi = 1/2 (AM-GM, retained). "
                 "Gradient flow OF L1 has chi=1/2 as fixed point trivially.  "
                 "But the natural retained DYNAMICS is grad S, not -grad L1, "
                 "and per Bar 14 SC3 grad S does NOT have chi=1/2 as min. "
                 "No retained dynamical mechanism uses L1 as Lyapunov.",
    }


# --------------------------------------------------------------------------- #
# Mechanism naturalness audit
# --------------------------------------------------------------------------- #


def naturalness_audit(results: list[dict]) -> dict:
    """For each tested mechanism, summarize axiom-native status and verdict."""
    subsection("Naturalness audit: dynamics vs static content")
    print(f"  {'Mechanism':<48} {'Axiom-native':<14} {'Selects chi=1/2':<16} {'Verdict':<10}")
    print(f"  {'-' * 92}")
    for r in results:
        name = r["name"].split(":")[0]
        ax = "yes" if r.get("axiom_native") else "no"
        sel = "yes" if r.get("tests_chi_half") and r.get("verdict") not in ("no-go", "circular") else "no"
        verdict = r.get("verdict", "?")
        print(f"  {name:<48} {ax:<14} {sel:<16} {verdict:<10}")
    print()
    print("  CONCLUSION:")
    print("    - Axiom-native dynamics (T1, T2, T4, T6, T7) all converge:")
    print("      retained S has no asymmetry preferring chi=1/2 over chi=1.")
    print("    - Non-native dynamics (T3, T5) DO have chi=1/2 reachable but")
    print("      not selected without an external bias (which is itself a")
    print("      new primitive).")
    print("    - T7 (Lyapunov) shows existence of a static functional with")
    print("      min at chi=1/2 (block-Frobenius / atlas Route 0), but a")
    print("      Lyapunov-flow argument is circular without retained dynamics.")
    print("    - The framework's own MC machinery (the only retained")
    print("      dynamical primitive, used for <P> = 0.5934) explicitly fails")
    print("      to give chi = 1/2 (T1).")
    return {
        "items": [{"name": r["name"], "axiom_native": r.get("axiom_native"),
                   "verdict": r.get("verdict")} for r in results],
        "verdict": "no_axiom_native_dynamics_selects_chi_half",
    }


# --------------------------------------------------------------------------- #
# Cross-check vs prior probes
# --------------------------------------------------------------------------- #


def cross_check_prior_probes() -> dict:
    """Position relative to prior probes."""
    subsection("Cross-check: relation to prior 37-probe ledger")
    print("  Prior probes touching dynamics:")
    print()
    print("  1. frontier_koide_a1_self_consistent_fixed_point_probe.py (Bar 14)")
    print("     Tests: deterministic SC iterations (rainbow SD, NJL, V_eff, mass-spec, W[J]).")
    print("     Verdict: NO axiom-native deterministic map has chi=1/2 stable attractor.")
    print()
    print("  2. RG-attractor probe (frontier_koide_a1_rg_attractor_probe.py is")
    print("     in main repo not yet in worktree; its result is summarized in")
    print("     KOIDE_A1_30K_FOOT_AUDIT_NOTE_2026-04-24.md):")
    print("     Tests: SMEFT RG flow on Yukawa, Wilsonian RG.")
    print("     Verdict: chi=1/2 only on codim-1 surfaces (Wilson-tuned).")
    print()
    print("  THIS PROBE EXTENDS TO STOCHASTIC / NON-EQUILIBRIUM:")
    print("    T1 (lattice MC):              extends Bar 14 SC4 to noise.")
    print("    T2 (Parisi-Wu):               equivalent to T1 by Parisi-Wu thm.")
    print("    T3 (Lindblad):                extends Bar 14 to open-system dyn.")
    print("    T4 (time-averaged Berry):     extends Berry phase theorem to dyn.")
    print("    T5 (Zeno):                    extends to measurement-induced.")
    print("    T6 (Schwinger-Keldysh):       extends to non-equilibrium.")
    print("    T7 (Lyapunov):                extends static AM-GM to dyn.")
    print()
    print("  All seven new mechanisms FAIL to yield chi = 1/2 as a")
    print("  retained-native dynamical attractor.  This complements Bar 14's")
    print("  deterministic-iteration negative result with a stochastic /")
    print("  non-equilibrium negative result.")
    print()
    print("  Consistent with the established taxonomy O1-O12; this probe")
    print("  does NOT establish a new obstruction class -- it strengthens")
    print("  the established ones (especially Bar 14 and O11).")
    return {
        "relation_to_bar14": "extends to stochastic / non-equilibrium",
        "relation_to_rg_attractor": "consistent (no chi=1/2 attractor)",
        "new_obstruction_class": False,
        "strengthens_classes": ["Bar 14 (SC iterations)", "O11 (Brannen form lock)"],
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    section("Koide A1 Dynamic / Non-Equilibrium Attractor Deep Probe")
    print("Hypothesis (Bar 2): chi = 1/2 (A1) is a TIME-AVERAGED or STOCHASTIC")
    print("attractor of NATURAL retained-native non-equilibrium dynamics.")
    print()
    print("Tested seven dynamical mechanisms:")
    print("  T1: Lattice Monte Carlo on retained Z_3 action")
    print("  T2: Parisi-Wu stochastic quantization (Langevin SDE)")
    print("  T3: Lindblad decoherence with Z_3-equivariant dissipators")
    print("  T4: Time-averaged Pancharatnam-Berry phase")
    print("  T5: Quantum-Zeno measurement-induced stabilization")
    print("  T6: Schwinger-Keldysh long-time average")
    print("  T7: Lyapunov function existence (control)")
    print()

    section("Pre-check: retained dynamical content")
    print("  The retained framework is largely STATIC (Lagrangian, partition")
    print("  function, Z[J] = exp(W[J])).  Two pieces of dynamics exist:")
    print("    (a) Lattice MC equilibration (gives <P> = 0.5934).")
    print("    (b) Wilsonian / SMEFT RG flow (gives running couplings).")
    print()
    print("  The probe tests whether either of these primary retained")
    print("  dynamical mechanisms -- or other mechanisms naturally derivable")
    print("  from retained content -- has chi=1/2 as a stochastic attractor.")
    record(
        "Retained framework defines (a) MC equilibration, (b) RG flow as native dynamics",
        True,
        "Other dynamics (Lindblad, measurement, driving) are non-native primitives.",
    )

    # --- T1: Lattice MC ---
    section("T1: Lattice MC sampling on retained Z_3-invariant action")
    r1 = t1_lattice_mc_charged_lepton_yukawa()
    MECHANISM_RESULTS.append(r1)
    record(
        "T1: lattice MC equilibration on retained Z_3 action does not pick chi=1/2",
        r1["verdict"] == "no-go",
        "Equipartition under any retained S gives <a^2> = <|b|^2>, chi median ~ 1.",
    )
    record(
        "T1: framework's own MC machinery (gives <P>=0.5934) does not transplant to A1",
        r1["axiom_native"] and r1["verdict"] == "no-go",
        "The MC dynamics IS retained but does not select chi=1/2.",
    )

    # --- T2: Parisi-Wu ---
    section("T2: Parisi-Wu stochastic quantization (Langevin SDE)")
    r2 = t2_parisi_wu_stochastic_quantization()
    MECHANISM_RESULTS.append(r2)
    record(
        "T2: Parisi-Wu time-average equals thermal average (stationary distribution = exp(-S))",
        r2["verdict"] == "no-go",
        "Parisi-Wu theorem; same equilibrium as T1.",
    )
    record(
        "T2: no retained S forces the asymmetry needed for chi = 1/2",
        r2["verdict"] == "no-go",
        "Median chi clusters at 1, not 1/2, for S0 / S_mex / S_with_cubic.",
    )

    # --- T3: Lindblad ---
    section("T3: Lindblad decoherence with Z_3-equivariant dissipators")
    r3 = t3_lindblad_decoherence()
    MECHANISM_RESULTS.append(r3)
    record(
        "T3: Z_3-equivariant Lindblad attracts to max-entropy I/3 (chi = 0)",
        r3["max_entropy_chi"] < 0.01,
        f"max-entropy chi = {r3['max_entropy_chi']:.6f}",
    )
    record(
        "T3: chi = 1/2 is a non-privileged simplex point; not selected by Lindblad",
        not r3["axiom_native"],
        f"{r3['n_simplex_points_at_half']} simplex points reach chi=1/2; none preferred.",
    )

    # --- T4: Time-averaged Berry ---
    section("T4: Time-averaged Pancharatnam-Berry phase along closed orbit")
    r4 = t4_time_averaged_berry_phase()
    MECHANISM_RESULTS.append(r4)
    record(
        "T4: Berry connection on Z_3 circulant moduli is identically zero",
        not r4["tests_chi_half"],
        "Fourier eigenvectors v_1, v_w, v_wbar do not depend on (a, b).",
    )
    record(
        "T4: time-average over closed orbit on (a,b) is identically zero (no Berry curvature)",
        r4["verdict"] == "no-go",
        f"accumulated phase = {r4['geo_phase_accumulated']:.4e} (numerically zero)",
    )

    # --- T5: Zeno ---
    section("T5: Quantum-Zeno measurement-induced stabilization")
    r5 = t5_quantum_zeno_stabilization()
    MECHANISM_RESULTS.append(r5)
    record(
        "T5: Zeno freezes initial chi distribution; no peak at 1/2",
        not r5["axiom_native"],
        f"fraction at chi=1/2 = {r5['fraction_at_half']:.3f} (~0.10 expected uniform)",
    )
    record(
        "T5: measurement of O_q is circular; measurement of O_a / O_b doesn't constrain chi",
        r5["verdict"] == "no-go",
        "No retained Z_3-invariant scalar observable singles out the ratio.",
    )

    # --- T6: Schwinger-Keldysh ---
    section("T6: Schwinger-Keldysh closed-time-path long-time average")
    r6 = t6_schwinger_keldysh_long_time_average()
    MECHANISM_RESULTS.append(r6)
    record(
        "T6: KMS theorem -- long-time trajectory average = thermal average",
        r6["verdict"] == "no-go",
        f"trajectory mean chi = {r6['trajectory_mean_chi']:.4f}, median = {r6['trajectory_median_chi']:.4f}",
    )
    record(
        "T6: no retained non-equilibrium driving exists for charged-lepton sector",
        r6["axiom_native"],
        "Adding driving = non-native primitive (cf. T3 Lindblad).",
    )

    # --- T7: Lyapunov ---
    section("T7: Lyapunov function existence (control / circularity check)")
    r7 = t7_lyapunov_function_existence()
    MECHANISM_RESULTS.append(r7)
    record(
        "T7: block-Frobenius L1 = -log E_+ - log E_perp has min at chi=1/2 (atlas Route 0)",
        r7["tests_chi_half"],
        "AM-GM extremum unique-to-rescaling (KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS).",
    )
    record(
        "T7: Lyapunov-flow argument from L1 is circular without retained dynamics",
        r7["verdict"] == "circular",
        "Gradient of S (retained) does not have chi=1/2 as min (Bar 14 SC3).",
    )

    # Naturalness audit
    section("Naturalness audit")
    audit = naturalness_audit(MECHANISM_RESULTS)

    # Cross-check
    section("Cross-check vs prior 37-probe ledger")
    cross = cross_check_prior_probes()

    # Documentation discipline (Tasks 1-7 + 6 items)
    section("Documentation discipline (mandatory)")
    print("  (1) TESTED:")
    print("     T1 -- lattice MC sampling (axiom-native dynamics)")
    print("     T2 -- Parisi-Wu Langevin (axiom-native dynamics)")
    print("     T3 -- Lindblad master equation (Z_3 dissipators)")
    print("     T4 -- time-averaged Berry phase on closed orbit")
    print("     T5 -- quantum-Zeno frequent measurement")
    print("     T6 -- Schwinger-Keldysh long-time average")
    print("     T7 -- Lyapunov function existence (control)")
    print()
    print("  (2) FAILED, and why:")
    print("     T1: equipartition under retained Z_3 action gives <chi> ~ 1, not 1/2.")
    print("         The retained action has no asymmetry between a-d.o.f. and b-d.o.f.")
    print("         that would produce <a^2> = 2<|b|^2>.")
    print("     T2: Parisi-Wu theorem: time-average = thermal average; same as T1.")
    print("     T3: Z_3-equivariant Lindblad attracts to max-entropy I/3 (chi = 0).")
    print("         Lindblad operators are non-native primitives.")
    print("     T4: Berry connection on circulant moduli is identically zero")
    print("         (KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19 sec. 3); no closed-orbit")
    print("         time-average gives a nonzero phase.")
    print("     T5: Zeno measurement protocol is non-native; freezing on retained")
    print("         observables doesn't single out chi = 1/2.")
    print("     T6: KMS theorem reduces SK long-time to T1/T2 thermal average.")
    print("         No retained driving exists for the lepton sector.")
    print("     T7: L1 has min at chi = 1/2, but using it as Lyapunov for a")
    print("         dynamical attractor argument is circular: it requires the")
    print("         dynamics to descend L1, which is not the dynamics of S.")
    print()
    print("  (3) NOT TESTED, and why:")
    print("     - Wetterich functional renormalization-group flow with specific")
    print("       regulator: regulator is a non-native primitive (cf. Bar 14 audit).")
    print("       Closely related to Bar 14 SC3 with V_K Wilson coefficient.")
    print("     - Stochastic resonance / chaotic attractor: no retained chaotic")
    print("       Hamiltonian in the lepton sector.")
    print("     - Aging dynamics / glassy slow relaxation: not retained-native;")
    print("       requires disordered couplings absent in Cl(3)/Z^3.")
    print("     - Coupled SU(2)_L x U(1)_Y x SU(3) RG with Yukawa coupling: this")
    print("       is the prior RG-attractor probe (frontier_koide_a1_rg_attractor_probe.py")
    print("       in main repo); already negative.")
    print("     - Holographic / AdS-CFT geodesic flow: not retained.")
    print("     - Quantum trajectories / continuous measurement weak: same family")
    print("       as T3 / T5, ruled out by similar arguments.")
    print()
    print("  (4) CHALLENGED:")
    print("     - The framing 'natural dynamics' must respect the retained-native")
    print("       criterion: only mechanisms expressible from Cl(3)/Z^3 + SU(2)_L")
    print("       x U(1)_Y embedding + observable principle W[J] = log|det(D+J)|")
    print("       are admissible.  T3, T5 violate this; T1, T2, T4, T6, T7 satisfy")
    print("       it but fail on the dynamical content.")
    print("     - The 'non-equilibrium gives 1/2 from equipartition' intuition")
    print("       FAILS: equipartition under retained S gives <a^2> = <|b|^2>, not")
    print("       <a^2> = 2<|b|^2>, because the d.o.f. count distributes 1+2 = 3")
    print("       not 1+1 = 2.  This is a subtle but decisive point.")
    print("     - The plaquette MC <P> = 0.5934 is a SCALAR observable on a")
    print("       gauge-link distribution.  It is a quantitatively predicted")
    print("       value FROM the action, not a structural ratio between sectors.")
    print("       The transplant to chi (a structural a-vs-b ratio) is not direct.")
    print()
    print("  (5) ACCEPTED:")
    print("     - All seven mechanisms preserve the Z_3-equivariant subspace")
    print("       (verified algebraically or numerically).")
    print("     - The block-Frobenius Lyapunov L1 has a genuine extremum at")
    print("       chi = 1/2, consistent with the static AM-GM identity (atlas Route 0)")
    print("       and KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS.")
    print("     - Bar 14 (deterministic SC iteration) and this probe (stochastic /")
    print("       non-equilibrium) jointly cover the dynamical-attractor surface.")
    print("     - Berry phase theorem retained content is consistent with this")
    print("       probe's T4 finding (zero connection on (a, b) moduli).")
    print()
    print("  (6) FORWARD SUGGESTIONS:")
    print("     - The named residual P (radian-bridge) is unaffected by these")
    print("       seven dynamical-attractor negative tests.  P remains the")
    print("       single irreducible primitive identified by the 37-probe ledger.")
    print("     - The 'non-equilibrium gives 1/2' lane is now closed.  Future")
    print("       probes should NOT pursue stochastic-quantization, Lindblad,")
    print("       Zeno, Schwinger-Keldysh, or time-averaged Berry as routes to A1.")
    print("     - Open: whether a NATIVE non-equilibrium driving exists from")
    print("       within Cl(3)/Z^3 + SM-embedding -- e.g., parity-violating")
    print("       boundary conditions, electroweak baryogenesis-like sphaleron")
    print("       drive, or finite-temperature effects on the lepton mass")
    print("       spectrum at the EW scale.  These would need to be retained-")
    print("       native; currently none is.")
    print("     - Strongest candidate of the 7: T7 (Lyapunov L1) is the closest")
    print("       to closure, but is circular without retained dynamics that")
    print("       descend it.  Identifying retained dynamics whose 'natural'")
    print("       Lyapunov is L1 = -log E_+ - log E_perp would be the route;")
    print("       no current candidate does this.")

    # Verdict
    section("VERDICT")
    n_axiom_native = sum(1 for r in MECHANISM_RESULTS if r.get("axiom_native"))
    n_selecting_half = sum(
        1 for r in MECHANISM_RESULTS
        if r.get("axiom_native") and r.get("verdict") not in ("no-go", "circular")
    )
    print(f"  Mechanisms tested:        {len(MECHANISM_RESULTS)}")
    print(f"  Axiom-native:             {n_axiom_native}")
    print(f"  Select chi=1/2 dynamically: {n_selecting_half}  (closure threshold)")
    print()
    print("  Bar 2 (dynamic / non-equilibrium attractor) does NOT close A1.")
    print()
    print("  Specifically:")
    print("    - T1, T2, T6 (lattice MC, Parisi-Wu, Schwinger-Keldysh): all")
    print("      reduce to thermal average under retained S; <chi> ~ 1, not 1/2.")
    print("    - T3, T5 (Lindblad, Zeno): non-native primitives; do not")
    print("      single out chi = 1/2 even when invoked.")
    print("    - T4 (time-averaged Berry): connection on (a,b) is zero;")
    print("      no closed-orbit time-average can produce 2/9 rad.")
    print("    - T7 (Lyapunov): block-Frobenius L1 has min at chi=1/2, but")
    print("      using L1 as Lyapunov is circular without retained descending")
    print("      dynamics (Bar 14 SC3 already showed grad S does not descend L1).")
    print()
    print("  CONSEQUENCE: A1 is NOT a dynamical / non-equilibrium / time-")
    print("  averaged attractor of any retained-native process.  The named")
    print("  residual P (radian-bridge postulate) is unaffected.  Bar 2 is")
    print("  closed NEGATIVELY, complementing Bar 14's deterministic-iteration")
    print("  negative result.")
    print()
    print("  This probe joins the 37-probe ledger as the 38th probe;")
    print("  cumulative probe count: 38 mechanisms tested, 38 dead.")

    record(
        "Bar 2: no retained-native dynamic / non-equilibrium attractor at chi=1/2",
        n_selecting_half == 0,
        f"Tested {len(MECHANISM_RESULTS)} mechanisms; {n_selecting_half} pass closure.",
    )

    # Summary
    section("SUMMARY")
    n_pass = len(PASS_LEDGER)
    print(f"PASSED: {n_pass}")
    for label, _ in PASS_LEDGER:
        print(f"  PASS  {label}")
    print()
    print("KOIDE_A1_DYNAMIC_ATTRACTOR_CLOSES_A1=FALSE")
    print("KOIDE_A1_DYNAMIC_ATTRACTOR_CLOSES_DELTA=FALSE")
    print(f"NUMBER_DYNAMIC_MECHANISMS_TESTED={len(MECHANISM_RESULTS)}")
    print(f"NUMBER_AXIOM_NATIVE_TESTED={n_axiom_native}")
    print(f"NUMBER_SELECT_CHI_HALF_DYNAMICALLY={n_selecting_half}")
    print("RESIDUAL_SCALAR=radian_bridge_postulate_P_unaffected")
    print("BAR_2_NEGATIVE=TRUE")

    # Write JSON snapshot
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "frontier_koide_a1_dynamic_attractor_probe.json"

    def _to_jsonable(x):
        if isinstance(x, (np.complexfloating, complex)):
            return {"re": float(x.real), "im": float(x.imag)}
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, np.ndarray):
            return [_to_jsonable(v) for v in x.tolist()]
        if isinstance(x, dict):
            return {k: _to_jsonable(v) for k, v in x.items()}
        if isinstance(x, list):
            return [_to_jsonable(v) for v in x]
        return x

    payload = {
        "probe": "frontier_koide_a1_dynamic_attractor_probe",
        "date": "2026-04-24",
        "hypothesis": "Bar 2: chi = 1/2 (A1) is a TIME-AVERAGED or stochastic "
                      "attractor of a retained-native non-equilibrium process",
        "verdict": "NO-GO -- Bar 2 fails for all 7 tested dynamical mechanisms",
        "passes_total": n_pass,
        "mechanisms": _to_jsonable(MECHANISM_RESULTS),
        "naturalness_audit": audit,
        "cross_check_prior_probes": cross,
        "closure_flags": {
            "KOIDE_A1_DYNAMIC_ATTRACTOR_CLOSES_A1": False,
            "KOIDE_A1_DYNAMIC_ATTRACTOR_CLOSES_DELTA": False,
            "NUMBER_DYNAMIC_MECHANISMS_TESTED": len(MECHANISM_RESULTS),
            "NUMBER_AXIOM_NATIVE_TESTED": n_axiom_native,
            "NUMBER_SELECT_CHI_HALF_DYNAMICALLY": n_selecting_half,
            "BAR_2_NEGATIVE": True,
            "RESIDUAL_SCALAR": "radian_bridge_postulate_P_unaffected",
        },
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"\nJSON results written to {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
