#!/usr/bin/env python3
"""
Koide 2.1e-4 gap investigation: 4x4 coupled sector and eigenvalue approaches
=============================================================================

STATUS: Systematic exploration of the residual gap between u*v*w=1 (m_prod1)
and the PDG-optimal selected-line point (m*). Three independent routes:

PART 1 - 4x4 coupled O_0 + T_2 sector on the Koide selected line
         (Cluster A Audit direction F4 — highest unexplored priority)
PART 2 - Eigenvalue-based Q=2/3 joint condition
         (Audit direction M2 — kappa and scale determined jointly)
PART 3 - PSLQ / algebraic search for kappa_* from framework constants
PART 4 - PDG Koide residual: is the gap physically real?

Framework-native only. PDG masses used ONLY for post-hoc comparison.
"""

from __future__ import annotations

import math
import sys
from itertools import product as iproduct

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar, minimize

# ──────────────────────────────────────────────────────────────────────────────
# Shared constants and H3 operator (from frontier_higgs_dressed_propagator_v1)
# ──────────────────────────────────────────────────────────────────────────────

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0            # √6/3  ≈ 0.8165
S = SELECTOR                       # shorthand

T_M = np.array([[1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0]], dtype=complex)
T_DELTA = np.array([[0.0, -1.0, 1.0],
                    [-1.0, 1.0, 0.0],
                    [1.0, 0.0, -1.0]], dtype=complex)
T_Q = np.array([[0.0, 1.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 0.0]], dtype=complex)
H_BASE = np.array([[0.0, E1, -E1 - 1j * GAMMA],
                   [E1, 0.0, -E2],
                   [-E1 + 1j * GAMMA, -E2, 0.0]], dtype=complex)


def H3(m, delta=S, q_plus=S):
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


# Known pinned points
M_STAR_SEL = -1.160469470087     # PDG-optimal selected-line point
M_PROD1 = -1.160257              # u*v*w = 1 crossing (2.1e-4 from m*)
KAPPA_STAR = -0.607913           # kappa at m*, from hstar_witness_kappa

PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def koide_Q_masses(masses):
    masses = np.asarray(masses, dtype=float)
    s = float(np.sum(masses))
    rs = float(np.sum(np.sqrt(masses)))
    if rs == 0:
        return float("nan")
    return s / (rs * rs)


def selected_line_slots(m):
    x = expm(H3(m, S, S))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def koide_root_pair(v, w):
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def kappa_from_slots(v, w):
    return (v - w) / (v + w)


# ──────────────────────────────────────────────────────────────────────────────
# PART 1: 4×4 coupled O_0 + T_2 sector on the Koide selected line
# ──────────────────────────────────────────────────────────────────────────────

def build_H4x4(m, h_O0, g_vec):
    """
    Construct the 4×4 Hermitian operator on (O_0, T_2_011, T_2_101, T_2_110).

    Layout: row/col 0 = O_0, rows/cols 1,2,3 = T_2 states.

    h_O0   : float — diagonal energy of the O_0 sector
    g_vec  : array of 3 complex numbers — coupling O_0 to each T_2 species
    The 3×3 T_2 block is H3(m, S, S).
    """
    H4 = np.zeros((4, 4), dtype=complex)
    H4[0, 0] = h_O0
    H4[1:, 1:] = H3(m, S, S)
    H4[0, 1:] = g_vec
    H4[1:, 0] = np.conj(g_vec)
    return H4


def part1_4x4_eigenvalue_crossing():
    print("=" * 88)
    print("PART 1: 4×4 coupled O_0 + T_2 sector on the Koide selected line")
    print("=" * 88)

    # The trace identity: Tr(H3(m, S, S)) = m + S (since Tr(T_M)=1, Tr(T_DELTA)=1, Tr(T_Q)=0)
    # The T_2 sector has 3 states; O_0 has 1 state.
    # Natural O_0 energy candidates derived from framework:
    #   (a) h_O0 = m/3       (share of T_1→O_0 hopping energy, from Tr/3 argument)
    #   (b) h_O0 = (m+S)/4   (equal share of 4-state total trace)
    #   (c) h_O0 = m + S     (same as Tr(H3), i.e., H4 is trace-degenerate in a sense)
    #   (d) h_O0 = -1/SQRT3  (threshold value — exact Cl(3) constant)
    #   (e) h_O0 = 0         (decoupled O_0 ground state)

    # Off-diagonal couplings: symmetry suggests uniform real coupling g to all T_2 states
    # Natural values: g = GAMMA/SQRT3, g = S/SQRT3, g = GAMMA, g = S, g = 1/3, etc.
    # The Cl(3) algebra has GAMMA = 1/2 and S = √6/3 as distinguished constants.

    # Key question: is there an (h_O0, g) for which the 4×4 eigenvalue structure
    # produces a condition that selects m ≈ m* rather than m_prod1?

    print()
    print("1a. O_0 energy derivation from Cl(3) structure")
    print("-" * 60)

    # Tr(H3) = m + S (verified algebraically)
    trace_check = complex(np.trace(H3(M_STAR_SEL)))
    expected = M_STAR_SEL + S
    check("Tr(H3(m*, S, S)) = m* + S",
          abs(float(np.real(trace_check)) - expected) < 1e-12,
          detail=f"Tr={float(np.real(trace_check)):.8f}, m*+S={expected:.8f}")

    # The O_0 sector enters with one slot in the 4-state basis.
    # Natural: h_O0 = (m + S)/4 so that Tr(H_4x4) = 4*(m+S)/4 + Tr(H3) - (m+S)/1
    # Actually more natural: h_O0 = (Tr(H3) - 0) / N_T2 where we distribute evenly
    # Let's just compute: what h_O0 makes Tr(H_4x4) = 2*(m+S) ?
    #   Tr(H_4x4) = h_O0 + (m+S) => h_O0 = (m+S) makes total trace 2*(m+S)
    # Simpler: h_O0 = m makes total trace 2m + S

    print()
    print("1b. Eigenvalue spectrum sweep over m ∈ [m*, m*+0.01] for several coupling pairs")
    print("-" * 60)

    # Sweep m from just above m_prod1 to just below — this is the critical window
    m_sweep = np.linspace(M_PROD1 - 0.001, M_STAR_SEL + 0.001, 2000)

    # Track minimum eigenvalue gap (level repulsion) and zero-crossing of eigenvalues
    coupling_cases = [
        ("h_O0=m/3,   g=GAMMA/√3",    lambda m: m / 3.0,        GAMMA / SQRT3),
        ("h_O0=m/3,   g=S/√3",         lambda m: m / 3.0,        S / SQRT3),
        ("h_O0=m,     g=GAMMA/√3",    lambda m: m,               GAMMA / SQRT3),
        ("h_O0=m,     g=S/√3",         lambda m: m,               S / SQRT3),
        ("h_O0=(m+S)/4, g=GAMMA/√3", lambda m: (m + S) / 4.0,   GAMMA / SQRT3),
        ("h_O0=(m+S)/4, g=S/√3",      lambda m: (m + S) / 4.0,  S / SQRT3),
        ("h_O0=-1/√3, g=GAMMA/√3",   lambda m: -1.0 / SQRT3,   GAMMA / SQRT3),
        ("h_O0=-1/√3, g=S/√3",        lambda m: -1.0 / SQRT3,   S / SQRT3),
    ]

    best_case = None
    best_crossing_dist = np.inf

    for label, h_O0_fn, g in coupling_cases:
        eigenvalue_traces = []
        for m in m_sweep:
            H4 = build_H4x4(m, h_O0_fn(m), np.array([g, g, g], dtype=complex))
            eigs = np.linalg.eigvalsh(H4)
            eigenvalue_traces.append(eigs)
        eig_arr = np.array(eigenvalue_traces)  # shape (N, 4)

        # Find zero-crossings for each eigenvalue track
        crossings_info = []
        for col in range(4):
            ev = eig_arr[:, col]
            for i in range(len(ev) - 1):
                if ev[i] * ev[i + 1] < 0:
                    m_cross = float(m_sweep[i] - ev[i] * (m_sweep[i + 1] - m_sweep[i]) / (ev[i + 1] - ev[i]))
                    crossings_info.append((col, m_cross))

        # Find level crossings (min gap between adjacent eigenvalue tracks)
        min_gap = np.inf
        m_min_gap = None
        for i in range(len(m_sweep)):
            gaps = np.diff(eig_arr[i, :])
            mg = np.min(np.abs(gaps))
            if mg < min_gap:
                min_gap = mg
                m_min_gap = m_sweep[i]

        # Look for eigenvalue conditions near m*
        dist_to_mstar = abs(m_min_gap - M_STAR_SEL) if m_min_gap is not None else np.inf
        if dist_to_mstar < best_crossing_dist:
            best_crossing_dist = dist_to_mstar
            best_case = label

        near_mstar = [(col, mc) for col, mc in crossings_info if abs(mc - M_STAR_SEL) < 1e-3]
        if near_mstar or dist_to_mstar < 2e-4:
            print(f"  NOTABLE: {label}")
            print(f"    min-gap={min_gap:.6f} at m={m_min_gap:.8f} (dist from m*={dist_to_mstar:.2e})")
            for col, mc in near_mstar:
                print(f"    zero-crossing of eig[{col}] at m={mc:.8f} (dist from m*={abs(mc-M_STAR_SEL):.2e})")

    print(f"\n  Best case (closest level structure to m*): {best_case}")
    print(f"  Distance from m*: {best_crossing_dist:.2e}")

    print()
    print("1c. Systematic scan: find (h_O0_offset, g) that places a zero-crossing AT m*")
    print("-" * 60)

    # The 4×4 determinant det(H_4x4(m)) = 0 could pin m*.
    # For fixed coupling g (real, uniform), this is a 2D problem (h_O0_offset, m).
    # We want det(H_4x4(m*)) = 0, which constrains h_O0.

    def det_H4x4(m, h_O0, g):
        H4 = build_H4x4(m, h_O0, np.array([g, g, g], dtype=complex))
        return float(np.real(np.linalg.det(H4)))

    print("  Scanning for h_O0 such that det(H_4x4(m*)) = 0:")
    for g in [GAMMA / SQRT3, S / SQRT3, GAMMA, S, 1.0 / 3.0, GAMMA / 2.0]:
        # Solve det(H_4x4(m*, h)) = 0 for h
        def f_h(h):
            return det_H4x4(M_STAR_SEL, h, g)

        # Search range for h_O0
        h_vals = np.linspace(-3.0, 1.0, 500)
        f_vals = np.array([f_h(h) for h in h_vals])
        roots = []
        for i in range(len(f_vals) - 1):
            if f_vals[i] * f_vals[i + 1] < 0:
                try:
                    h_root = brentq(f_h, h_vals[i], h_vals[i + 1])
                    roots.append(h_root)
                except Exception:
                    pass

        if roots:
            print(f"  g={g:.6f}: h_O0 roots where det=0 at m*: {[f'{h:.8f}' for h in roots[:4]]}")
            # Check if any root is a framework constant
            for h_root in roots[:4]:
                for name, val in [("m*", M_STAR_SEL), ("-1/√3", -1/SQRT3),
                                   ("-S", -S), ("-GAMMA", -GAMMA),
                                   ("m*/3", M_STAR_SEL/3), ("(m*+S)/4", (M_STAR_SEL+S)/4),
                                   ("-SQRT6/4", -SQRT6/4)]:
                    if abs(h_root - val) < 1e-4:
                        print(f"    *** MATCH: h_root = {name} = {val:.8f} ***")

    print()
    print("1d. 4×4 Koide Q on eigenvalues of exp(H_4x4): select the Koide-cone subspace")
    print("-" * 60)

    # If we take 3 of the 4 eigenvalues of exp(H_4x4), can we get Q=2/3 at m*?
    # The 4 eigenvalues can be grouped as (1,3) — take the top 3.
    best_cs = -1.0
    best_m_eig = None
    best_g_eig = None
    best_h_eig = None

    for g in [GAMMA / SQRT3, S / SQRT3, GAMMA / 2]:
        for h_O0_fn_label, h_O0_fn in [("m/3", lambda m: m/3), ("(m+S)/4", lambda m: (m+S)/4)]:
            # Sweep m on the critical range
            m_test = np.linspace(-1.165, -1.155, 1000)
            for m in m_test:
                H4 = build_H4x4(m, h_O0_fn(m), np.array([g, g, g], dtype=complex))
                exp_H4 = expm(H4)
                eigs4 = np.linalg.eigvalsh(exp_H4)  # 4 real eigenvalues, ascending
                # Try all C(4,3) = 4 triplet choices
                for skip in range(4):
                    triplet = np.array([eigs4[i] for i in range(4) if i != skip])
                    if np.all(triplet > 0):
                        Q = koide_Q_masses(triplet)
                        if abs(Q - 2.0 / 3.0) < 5e-4:
                            sqrt_trip = np.sqrt(triplet)
                            cs = float(np.dot(sqrt_trip / np.linalg.norm(sqrt_trip), PDG_DIR))
                            if cs > best_cs:
                                best_cs = cs
                                best_m_eig = m
                                best_g_eig = g
                                best_h_eig = h_O0_fn_label
                                best_Q = Q

    if best_m_eig is not None:
        print(f"  Best 4×4 eigenvalue Koide hit:")
        print(f"    m={best_m_eig:.8f}, g={best_g_eig:.6f}, h_O0={best_h_eig}")
        print(f"    Q={best_Q:.8f}, cos-sim={best_cs:.8f}")
        print(f"    dist from m*={abs(best_m_eig - M_STAR_SEL):.2e}")
        check("4×4 eigenvalue Koide gives cos-sim > 0.99 near m*",
              best_cs > 0.99 and abs(best_m_eig - M_STAR_SEL) < 1e-3,
              detail=f"m={best_m_eig:.8f}, cs={best_cs:.6f}",
              kind="NUMERIC")
    else:
        print("  No 4×4 eigenvalue Koide triplet found near m*.")
        check("4×4 eigenvalue Koide gives hit near m*", False, kind="NUMERIC")

    return best_case


# ──────────────────────────────────────────────────────────────────────────────
# PART 2: Eigenvalue-based Q=2/3 joint condition (Audit direction M2)
# ──────────────────────────────────────────────────────────────────────────────

def part2_eigenvalue_koide():
    print()
    print("=" * 88)
    print("PART 2: eigenvalue-based Q=2/3 joint condition on H_sel(m)")
    print("=" * 88)
    print()
    print("The slot construction guarantees Q=2/3 by choosing u_small from Koide formula.")
    print("Here we ask: find (m, β) where eigenvalues of exp(β·H_sel(m)) satisfy Q=2/3.")
    print("This is a GENUINE constraint — eigenvalues are not slots.")
    print()

    def eig_koide_residual(m, beta):
        H = H3(m, S, S)
        eigs = np.linalg.eigvalsh(expm(beta * H))  # ascending real
        if np.any(eigs <= 0):
            return float('nan'), float('nan'), float('nan')
        Q = koide_Q_masses(eigs)
        sqrt_e = np.sqrt(eigs)
        cs = float(np.dot(sqrt_e / np.linalg.norm(sqrt_e), PDG_DIR))
        prod = float(np.prod(eigs))
        return Q, cs, prod

    print("2a. Q contour in (m, beta) plane: find Q(eigs)=2/3 curve")
    print("-" * 60)

    # Scan (m, beta) grid
    m_range = np.linspace(-1.25, -1.05, 300)
    beta_range = np.linspace(0.3, 2.0, 300)

    Q_grid = np.full((len(m_range), len(beta_range)), np.nan)
    cs_grid = np.full_like(Q_grid, np.nan)
    prod_grid = np.full_like(Q_grid, np.nan)

    for i, m in enumerate(m_range):
        for j, beta in enumerate(beta_range):
            Q, cs, prod = eig_koide_residual(m, beta)
            Q_grid[i, j] = Q
            cs_grid[i, j] = cs
            prod_grid[i, j] = prod

    # Find contour Q = 2/3: sign changes in (Q - 2/3)
    target_Q = 2.0 / 3.0
    koide_curve_points = []
    for i in range(len(m_range)):
        residuals = Q_grid[i, :] - target_Q
        for j in range(len(beta_range) - 1):
            r0, r1 = residuals[j], residuals[j + 1]
            if not (math.isnan(r0) or math.isnan(r1)) and r0 * r1 < 0:
                beta_cross = beta_range[j] + (beta_range[j + 1] - beta_range[j]) * (-r0 / (r1 - r0))
                koide_curve_points.append((m_range[i], beta_cross))

    print(f"  Found {len(koide_curve_points)} Q=2/3 contour points in (m, beta) space")

    # Along the Q=2/3 contour, find best cos-similarity to PDG
    if koide_curve_points:
        best_cs_on_contour = -1.0
        best_m_contour = None
        best_beta_contour = None
        best_prod_contour = None

        for m, beta in koide_curve_points:
            Q, cs, prod = eig_koide_residual(m, beta)
            if cs > best_cs_on_contour:
                best_cs_on_contour = cs
                best_m_contour = m
                best_beta_contour = beta
                best_prod_contour = prod

        print(f"  Best PDG direction on Q=2/3 contour:")
        print(f"    m={best_m_contour:.8f}, beta={best_beta_contour:.8f}")
        print(f"    cos-sim={best_cs_on_contour:.8f}, prod(eigs)={best_prod_contour:.8f}")
        print(f"    dist from m*={abs(best_m_contour - M_STAR_SEL):.2e}")
        print(f"    dist from m_prod1={abs(best_m_contour - M_PROD1):.2e}")

        # Refine with fine scan
        m_fine = np.linspace(best_m_contour - 0.02, best_m_contour + 0.02, 500)
        best_refined = None
        for m in m_fine:
            # Find beta where Q=2/3 at this m
            def q_residual(b):
                Q, cs, prod = eig_koide_residual(m, b)
                return Q - 2.0 / 3.0 if not math.isnan(Q) else 1.0

            try:
                b_lo, b_hi = best_beta_contour - 0.3, best_beta_contour + 0.3
                if q_residual(b_lo) * q_residual(b_hi) < 0:
                    b_root = brentq(q_residual, b_lo, b_hi)
                    Q, cs, prod = eig_koide_residual(m, b_root)
                    if not math.isnan(cs) and cs > (best_refined[2] if best_refined else -1):
                        best_refined = (m, b_root, cs, prod)
            except Exception:
                pass

        if best_refined:
            m_r, b_r, cs_r, prod_r = best_refined
            print(f"\n  Refined best on Q=2/3 contour:")
            print(f"    m={m_r:.10f}, beta={b_r:.10f}")
            print(f"    cos-sim={cs_r:.10f}, prod(eigs)={prod_r:.10f}")
            print(f"    dist from m*={abs(m_r - M_STAR_SEL):.2e}")
            check("Eigenvalue Q=2/3 contour passes near m*",
                  abs(m_r - M_STAR_SEL) < 5e-3,
                  detail=f"dist={abs(m_r-M_STAR_SEL):.2e}",
                  kind="NUMERIC")
            check("Eigenvalue Q=2/3 contour best point cos-sim > 0.999",
                  cs_r > 0.999,
                  detail=f"cs={cs_r:.8f}",
                  kind="NUMERIC")

            # Key question: is there a second condition (e.g. prod=1 or beta=beta*)
            # that pins (m,beta) jointly?
            print(f"\n  At contour best: prod(eigs) - 1 = {prod_r - 1:.4e}")
            print(f"  At m*: prod(eig, beta_slot) where slot u*v*w was {1.0:.6f}")

            # Check if prod=1 on the contour near best_m_contour
            prod_on_contour = [(m, b, *eig_koide_residual(m, b)) for m, b in koide_curve_points]
            prod_on_contour = [(m, b, Q, cs, prod) for m, b, Q, cs, prod in prod_on_contour
                               if not math.isnan(prod)]
            # Find where prod = 1 on contour
            prod_crossings = []
            for idx in range(len(prod_on_contour) - 1):
                m1, b1, Q1, cs1, p1 = prod_on_contour[idx]
                m2, b2, Q2, cs2, p2 = prod_on_contour[idx + 1]
                if (p1 - 1.0) * (p2 - 1.0) < 0 and abs(m1 - m2) < 0.05:
                    m_cross = m1 + (m2 - m1) * (1.0 - p1) / (p2 - p1)
                    b_cross = b1 + (b2 - b1) * (1.0 - p1) / (p2 - p1)
                    prod_crossings.append((m_cross, b_cross))

            if prod_crossings:
                print(f"\n  prod(eigs)=1 intersects Q=2/3 contour at:")
                for m_c, b_c in prod_crossings[:5]:
                    _, cs_c, _ = eig_koide_residual(m_c, b_c)
                    print(f"    m={m_c:.8f}, beta={b_c:.8f}, cos-sim={cs_c:.6f}")
                    print(f"    dist from m*={abs(m_c - M_STAR_SEL):.2e}")
                    check("Q=2/3 ∩ prod=1 gives point near m*",
                          abs(m_c - M_STAR_SEL) < 1e-3,
                          detail=f"dist={abs(m_c-M_STAR_SEL):.2e}",
                          kind="NUMERIC")
            else:
                print("  No prod(eigs)=1 crossing on Q=2/3 contour found in scanned range")

    print()
    print("2b. Q=2/3 on eigenvalues of H_sel (not exp): eigenvalue triplet condition")
    print("-" * 60)

    # Alternative: eigenvalues of H3(m, S, S) itself (not exponentiated)
    # These can be negative. Check if Q on |eigs| gives 2/3 near m*.
    def h_eig_koide(m):
        eigs = np.linalg.eigvalsh(H3(m, S, S))
        abseigs = np.abs(eigs)
        Q = koide_Q_masses(abseigs)
        sqrt_e = np.sqrt(abseigs)
        cs = float(np.dot(sqrt_e / np.linalg.norm(sqrt_e), PDG_DIR))
        return Q, cs

    m_scan = np.linspace(-1.3, -1.0, 1000)
    best_Q_H = None
    best_cs_H = -1.0
    best_m_H = None
    for m in m_scan:
        Q, cs = h_eig_koide(m)
        if not math.isnan(Q) and abs(Q - 2.0 / 3.0) < 0.01 and cs > best_cs_H:
            best_cs_H = cs
            best_m_H = m
            best_Q_H = Q

    if best_m_H is not None:
        print(f"  Best H_sel eigenvalue Q near 2/3: m={best_m_H:.6f}, Q={best_Q_H:.6f}, cs={best_cs_H:.6f}")
        print(f"  dist from m*={abs(best_m_H - M_STAR_SEL):.2e}")


# ──────────────────────────────────────────────────────────────────────────────
# PART 3: PSLQ / algebraic search for kappa_* from framework constants
# ──────────────────────────────────────────────────────────────────────────────

def part3_algebraic_search():
    print()
    print("=" * 88)
    print("PART 3: PSLQ / algebraic search for kappa_* from framework constants")
    print("=" * 88)
    print()

    # Compute kappa* precisely from PDG data
    v_star, w_star = selected_line_slots(M_STAR_SEL)
    kappa_precise = kappa_from_slots(v_star, w_star)
    print(f"  kappa* precise value: {kappa_precise:.15f}")
    print(f"  kappa* = (v-w)/(v+w) at m*")
    print()

    # Framework constants
    constants = {
        "GAMMA":       GAMMA,              # 1/2
        "S=SELECTOR":  S,                  # √6/3
        "E1":          E1,                 # √(8/3)
        "E2":          E2,                 # √8/3
        "SQRT2":       math.sqrt(2.0),
        "SQRT3":       SQRT3,
        "SQRT6":       SQRT6,
        "1/SQRT3":     1.0 / SQRT3,
        "1/SQRT6":     1.0 / SQRT6,
        "1/3":         1.0 / 3.0,
        "2/3":         2.0 / 3.0,
        "pi":          math.pi,
        "pi/6":        math.pi / 6.0,
        "pi/4":        math.pi / 4.0,
        "pi/3":        math.pi / 3.0,
    }

    print("3a. Single-constant checks")
    print("-" * 60)
    for name, val in constants.items():
        if abs(val - abs(kappa_precise)) < 3e-3:
            print(f"  NEAR MATCH: kappa*≈{name} ({val:.8f}), diff={kappa_precise+val:.2e}")
        if abs(-val - abs(kappa_precise)) < 3e-3:
            print(f"  NEAR MATCH: kappa*≈-{name} ({-val:.8f}), diff={kappa_precise-(-val):.2e}")

    print()
    print("3b. Ratio search: kappa* = a/b for framework constants a, b")
    print("-" * 60)
    const_list = list(constants.items())
    for (na, a), (nb, b) in iproduct(const_list, const_list):
        if abs(b) < 1e-10:
            continue
        ratio = a / b
        if abs(ratio - abs(kappa_precise)) < 1e-4:
            print(f"  RATIO HIT: {na}/{nb} = {ratio:.8f}, diff={abs(ratio - abs(kappa_precise)):.2e}")
        if abs(-ratio - abs(kappa_precise)) < 1e-4:
            print(f"  RATIO HIT: -{na}/{nb} = {-ratio:.8f}, diff={abs(-ratio - abs(kappa_precise)):.2e}")

    print()
    print("3c. Linear combination: kappa* = p*a + q*b for small rational p, q")
    print("-" * 60)
    # Search: kappa* = n1/d * a + n2/d * b, n1,n2 ∈ {-3..3}, d ∈ {1..6}
    found_lc = []
    for (na, a), (nb, b) in iproduct(const_list, const_list):
        for d in range(1, 7):
            for n1 in range(-3, 4):
                for n2 in range(-3, 4):
                    if n1 == 0 and n2 == 0:
                        continue
                    val = n1 * a / d + n2 * b / d
                    if abs(val - kappa_precise) < 5e-5:
                        found_lc.append((f"({n1}/{d})*{na} + ({n2}/{d})*{nb}", val,
                                         abs(val - kappa_precise)))

    found_lc.sort(key=lambda x: x[2])
    for expr, val, diff in found_lc[:10]:
        print(f"  HIT: kappa* ≈ {expr} = {val:.10f}, diff={diff:.2e}")

    print()
    print("3d. H_sel eigenvalues at m*: algebraic relationship to kappa*")
    print("-" * 60)
    eigs_mstar = np.linalg.eigvalsh(H3(M_STAR_SEL, S, S))
    print(f"  H_sel(m*) eigenvalues: {eigs_mstar}")
    eig_ratios = [eigs_mstar[i] / eigs_mstar[j] for i in range(3) for j in range(3) if i != j]
    for i, j in [(0, 1), (1, 2), (0, 2)]:
        ratio = eigs_mstar[i] / eigs_mstar[j]
        print(f"  eig[{i}]/eig[{j}] = {ratio:.10f}")
        # Check if this ratio relates to kappa*
        if abs(ratio - kappa_precise) < 1e-4:
            print(f"    *** matches kappa* to {abs(ratio - kappa_precise):.2e} ***")

    # exp eigenvalues at m* (no beta scaling, beta=1)
    exp_eigs = np.linalg.eigvalsh(expm(H3(M_STAR_SEL, S, S)))
    print(f"\n  exp(H_sel(m*)) eigenvalues: {exp_eigs}")
    v_s, w_s = selected_line_slots(M_STAR_SEL)
    u_small, u_large = koide_root_pair(v_s, w_s)
    print(f"  Koide slots: u_small={u_small:.8f}, v={v_s:.8f}, w={w_s:.8f}")
    print(f"  Note: slots = diagonal of exp(H_sel), NOT eigenvalues of exp(H_sel)")

    # Check Cayley-Hamilton / characteristic polynomial roots
    chars = np.poly(expm(H3(M_STAR_SEL, S, S)))
    print(f"  char poly coefficients of exp(H_sel(m*)): {chars}")
    # prod = e0*e1*e2 = exp(Tr(H_sel)) = exp(m*+S)
    prod_exact = math.exp(M_STAR_SEL + S)
    print(f"  det(exp(H_sel(m*))) = exp(m*+S) = {prod_exact:.10f}")
    print(f"  Verified: {float(np.real(np.linalg.det(expm(H3(M_STAR_SEL, S, S))))):.10f}")

    print()
    print("3e. kappa* from spectral gap of H_sel")
    print("-" * 60)
    # Spectral gap = eig[2] - eig[0]
    gap = float(eigs_mstar[2] - eigs_mstar[0])
    mid = float((eigs_mstar[2] + eigs_mstar[0]) / 2)
    asym = float((eigs_mstar[2] - eigs_mstar[0]) / (eigs_mstar[2] + eigs_mstar[0]))
    print(f"  spectral gap (eig2-eig0): {gap:.10f}")
    print(f"  spectral mid (eig2+eig0)/2: {mid:.10f}")
    print(f"  spectral asymmetry (gap/sum): {asym:.10f}")
    # Compare to kappa
    print(f"  kappa*(slots): {kappa_precise:.10f}")
    print(f"  gap: {abs(asym - abs(kappa_precise)):.2e} from kappa*")

    check("kappa* has a known algebraic form from framework constants (within 5e-5)",
          len(found_lc) > 0 and found_lc[0][2] < 5e-5,
          detail=f"best: {found_lc[0][0] if found_lc else 'none'}",
          kind="NUMERIC")


# ──────────────────────────────────────────────────────────────────────────────
# PART 4: PDG Koide residual — is the gap physically real?
# ──────────────────────────────────────────────────────────────────────────────

def part4_pdg_residual():
    print()
    print("=" * 88)
    print("PART 4: PDG Koide residual — is the 2.1e-4 gap physically real?")
    print("=" * 88)
    print()

    # The Koide formula gives Q = 2/3 EXACTLY by construction (u_small is chosen to satisfy it).
    # But experimental masses give Q_PDG ≠ 2/3.
    Q_PDG = koide_Q_masses([0.51099895, 105.6583755, 1776.86])
    koide_residual = abs(Q_PDG - 2.0 / 3.0)
    print(f"  Q_PDG = {Q_PDG:.12f}")
    print(f"  Q_PDG - 2/3 = {Q_PDG - 2.0/3.0:.4e}")
    print(f"  |Q_PDG - 2/3| = {koide_residual:.4e}")
    print()
    print(f"  Gap |m* - m_prod1| = {abs(M_STAR_SEL - M_PROD1):.4e}")
    print()

    # Compute how kappa changes per unit of m near m*
    dm = 1e-6
    dkappa_dm = (kappa_from_slots(*selected_line_slots(M_STAR_SEL + dm)) -
                 kappa_from_slots(*selected_line_slots(M_STAR_SEL - dm))) / (2 * dm)
    print(f"  dkappa/dm at m*: {dkappa_dm:.6f}")

    # kappa shift from m_prod1 to m*
    kappa_prod1 = kappa_from_slots(*selected_line_slots(M_PROD1))
    kappa_mstar = kappa_from_slots(*selected_line_slots(M_STAR_SEL))
    delta_kappa = kappa_mstar - kappa_prod1
    print(f"  kappa(m_prod1) = {kappa_prod1:.10f}")
    print(f"  kappa(m*)      = {kappa_mstar:.10f}")
    print(f"  delta_kappa    = {delta_kappa:.4e}")
    print()

    # What kappa_target would be needed to exactly match PDG cos-similarity = 1?
    # The direction: PDG masses have Q_PDG ≠ 2/3.
    # In the Koide framework, Q=2/3 is enforced, so perfect PDG match requires
    # finding m where the Koide small branch direction = PDG direction EXACTLY.
    # This is what m* is: the PDG-optimal point. The residual gap from u*v*w=1
    # reflects a genuine tension between Q=2/3 enforcement and u*v*w=1 normalization.

    # Compute how many kappa units the PDG Koide residual corresponds to
    print("  Mapping PDG Koide residual to kappa space:")
    # At m*, vary kappa (by shifting m) and find how Q changes if we DIDN'T enforce Q=2/3
    # Instead, ask: what is the kappa corresponding to Q_PDG?
    def kappa_at_pdg_Q():
        # We need to find m such that the eigenvalue-based Q = Q_PDG
        # (not the slot-based Q which is always 2/3)
        # This is different from m*: m* is where cos-sim is maximized (among Q=2/3 solutions).
        # The eigenvalue Q at m* will generically differ from 2/3.
        m_scan = np.linspace(-1.25, -1.05, 500)
        results = []
        for m in m_scan:
            eigs = np.linalg.eigvalsh(expm(H3(m, S, S)))
            if np.all(eigs > 0):
                Q_eig = koide_Q_masses(eigs)
                results.append((m, Q_eig))
        return results

    eig_Q_results = kappa_at_pdg_Q()
    print(f"  Eigenvalue Q at m*: ", end="")
    eigs_at_mstar = np.linalg.eigvalsh(expm(H3(M_STAR_SEL, S, S)))
    Q_eig_mstar = koide_Q_masses(eigs_at_mstar)
    print(f"{Q_eig_mstar:.8f}")
    print(f"  (contrast with slot-based Q = 2/3 exactly by construction)")
    print()

    # Find where eigenvalue Q = Q_PDG
    Q_pdg_crossings = []
    for i in range(len(eig_Q_results) - 1):
        m1, Q1 = eig_Q_results[i]
        m2, Q2 = eig_Q_results[i + 1]
        if (Q1 - Q_PDG) * (Q2 - Q_PDG) < 0:
            m_cross = m1 + (m2 - m1) * (Q_PDG - Q1) / (Q2 - Q1)
            Q_pdg_crossings.append(m_cross)

    if Q_pdg_crossings:
        print(f"  Eigenvalue Q = Q_PDG at m values: {[f'{m:.8f}' for m in Q_pdg_crossings[:3]]}")
        for mc in Q_pdg_crossings[:3]:
            print(f"    dist from m*={abs(mc-M_STAR_SEL):.2e}, from m_prod1={abs(mc-M_PROD1):.2e}")

    print()
    print("  Summary:")
    print(f"  The gap |m* - m_prod1| = {abs(M_STAR_SEL - M_PROD1):.4e}")
    print(f"  The PDG Koide residual |Q_PDG - 2/3| = {koide_residual:.4e}")
    ratio = abs(M_STAR_SEL - M_PROD1) / koide_residual
    print(f"  Ratio (gap / Koide residual) = {ratio:.3f}")
    check("The m* gap is NOT the same order as the PDG Koide residual mapping",
          ratio > 5 or ratio < 0.1,
          detail=f"ratio={ratio:.3f}: gap and PDG-Q residual are at different scales",
          kind="NUMERIC")

    # Finally: is the gap consistent with a one-loop correction?
    # g^2 / (4*pi^2) ~ (1/137 at alpha_EM scale) * correction
    alpha_EM = 1.0 / 137.036
    one_loop = alpha_EM / (4.0 * math.pi ** 2)
    print()
    print(f"  One-loop scale g²/(4π²) at α_EM: {one_loop:.4e}")
    print(f"  Gap: {abs(M_STAR_SEL - M_PROD1):.4e}")
    print(f"  Ratio gap/one-loop: {abs(M_STAR_SEL - M_PROD1) / one_loop:.2f}")
    check("Gap is O(1) × one-loop correction at α_EM scale",
          0.05 < abs(M_STAR_SEL - M_PROD1) / one_loop < 20.0,
          detail=f"ratio={abs(M_STAR_SEL-M_PROD1)/one_loop:.2f}",
          kind="NUMERIC")


# ──────────────────────────────────────────────────────────────────────────────
# PART 5: Determinant condition on the selected-line exponential
# ──────────────────────────────────────────────────────────────────────────────

def part5_det_condition():
    print()
    print("=" * 88)
    print("PART 5: Special determinant / trace conditions on exp(H_sel)")
    print("=" * 88)
    print()

    # det(exp(H_sel)) = exp(Tr(H_sel)) = exp(m + S) — always non-zero, smooth in m.
    # This can't pin m* directly. But sub-block determinants or cofactors might.

    # Tr(exp(H_sel)): this is sum of eigenvalues of exp(H_sel), different from sum of diagonals.
    # (Diagonal slots v, w, and the Koide root u are NOT eigenvalues of exp(H_sel).)

    m_scan = np.linspace(-1.20, -1.10, 2000)
    tr_exp = []
    det_exp = []
    diag_sum = []  # v + w = sum of two accessible slots (u_small + v + w = total, but u is determined)
    u_times_vw = []  # u_small * v * w

    for m in m_scan:
        H = H3(m, S, S)
        X = expm(H)
        eigs = np.linalg.eigvalsh(X)
        v_m = float(np.real(X[2, 2]))
        w_m = float(np.real(X[1, 1]))
        u_s, _ = koide_root_pair(v_m, w_m)
        tr_exp.append(float(np.real(np.trace(X))))
        det_exp.append(float(np.real(np.linalg.det(X))))
        diag_sum.append(v_m + w_m)
        u_times_vw.append(u_s * v_m * w_m)

    tr_exp = np.array(tr_exp)
    det_exp = np.array(det_exp)
    u_times_vw = np.array(u_times_vw)

    print("  Values at m_prod1 and m*:")
    idx_prod1 = np.argmin(np.abs(m_scan - M_PROD1))
    idx_mstar = np.argmin(np.abs(m_scan - M_STAR_SEL))

    print(f"  Tr(exp(H_sel)):   m_prod1={tr_exp[idx_prod1]:.8f}, m*={tr_exp[idx_mstar]:.8f}")
    print(f"  det(exp(H_sel)):  m_prod1={det_exp[idx_prod1]:.8f}, m*={det_exp[idx_mstar]:.8f}")
    print(f"  u*v*w:            m_prod1={u_times_vw[idx_prod1]:.8f}, m*={u_times_vw[idx_mstar]:.8f}")

    # Find where Tr(exp) = 3 (geometric mean = 1 in a different sense)
    tr_crossings = []
    for i in range(len(m_scan) - 1):
        if (tr_exp[i] - 3.0) * (tr_exp[i + 1] - 3.0) < 0:
            mc = m_scan[i] + (m_scan[i + 1] - m_scan[i]) * (3.0 - tr_exp[i]) / (tr_exp[i + 1] - tr_exp[i])
            tr_crossings.append(mc)

    print(f"\n  Tr(exp(H_sel)) = 3 crossings near range: {[f'{m:.8f}' for m in tr_crossings]}")
    for mc in tr_crossings:
        print(f"    dist from m*={abs(mc - M_STAR_SEL):.2e}, from m_prod1={abs(mc - M_PROD1):.2e}")
        check("Tr(exp) = 3 gives m ≈ m*",
              abs(mc - M_STAR_SEL) < 1e-3,
              detail=f"dist={abs(mc-M_STAR_SEL):.2e}",
              kind="NUMERIC")

    # Find where Tr(exp) = exp(m+S)/3 * 3 = exp(m+S) — i.e., all eigenvalues equal
    # That's Tr = det^(1/3) * 3, but det = exp(m+S) so det^(1/3) = exp((m+S)/3)
    # This is the "eigenvalue democracy" condition: all eigenvalues of exp(H) equal.
    print()
    democracy_gap = np.array([tr_exp[i] - 3.0 * det_exp[i] ** (1.0 / 3.0) for i in range(len(m_scan))])
    dem_crossings = []
    for i in range(len(m_scan) - 1):
        if democracy_gap[i] * democracy_gap[i + 1] < 0:
            mc = m_scan[i] + (m_scan[i + 1] - m_scan[i]) * (-democracy_gap[i]) / (democracy_gap[i + 1] - democracy_gap[i])
            dem_crossings.append(mc)
    print(f"  Eigenvalue democracy Tr=3*det^(1/3) crossings: {[f'{m:.8f}' for m in dem_crossings]}")

    # Characteristic polynomial of exp(H_sel): p3 - s1*p2 + s2*p - s3 = 0
    # s1 = Tr, s2 = (Tr^2 - Tr(H^2))/2, s3 = det
    # Discriminant of char poly = 0 means two eigenvalues coincide.
    print()
    print("  Characteristic polynomial discriminant (level crossing of exp(H_sel)):")
    disc_vals = []
    for m in m_scan:
        X = expm(H3(m, S, S))
        eigs = np.linalg.eigvalsh(X)
        # Discriminant for cubic: Δ = 18*s1*s2*s3 - 4*s1^3*s3 + s1^2*s2^2 - 4*s2^3 - 27*s3^2
        # where char poly is x^3 - s1*x^2 + s2*x - s3
        # For eigenvalues a, b, c: Δ = (a-b)^2*(b-c)^2*(a-c)^2
        a, b, c = eigs
        disc = (a - b) ** 2 * (b - c) ** 2 * (a - c) ** 2
        disc_vals.append(float(disc))

    disc_vals = np.array(disc_vals)
    min_disc_idx = np.argmin(disc_vals)
    print(f"  Minimum discriminant at m={m_scan[min_disc_idx]:.8f}, Δ={disc_vals[min_disc_idx]:.4e}")
    print(f"  dist from m*={abs(m_scan[min_disc_idx] - M_STAR_SEL):.2e}")


# ──────────────────────────────────────────────────────────────────────────────
# PART 6: Winding number / topological condition on exp(H_sel)
# ──────────────────────────────────────────────────────────────────────────────

def part6_topological():
    print()
    print("=" * 88)
    print("PART 6: Topological conditions on the selected-line exponential map")
    print("=" * 88)
    print()

    # The map m -> exp(H_sel(m)) is a curve in SL(3,ℂ) (det = exp(Tr) ≠ 0).
    # Topological / winding conditions:

    # (a) Phase of det(exp(H_sel)) — since H is not Hermitian in general (H3 is Hermitian
    #     but has complex entries), let's check if det has interesting phase structure.
    # Actually H3 IS Hermitian, so exp(H3) is positive definite Hermitian.
    # det(exp(H_sel)) = exp(Tr(H_sel)) = exp(m + S) — real positive, no phase.

    # (b) SU(3) component: exp(H_sel) / det(exp(H_sel))^(1/3) — this has det=1.
    # The SU(3) part carries the shape information. Its eigenvalues are
    # eig_i * exp(-(m+S)/3) which are related to the mass ratios.

    m_scan = np.linspace(-1.25, -1.05, 500)

    print("  SU(3) component condition (shape eigenvalues):")
    print()

    # At m*, compute SU(3) eigenvalues
    def su3_eigs(m):
        X = expm(H3(m, S, S))
        phase = float(np.real(np.linalg.det(X))) ** (1.0 / 3.0)
        X_su3 = X / phase
        eigs = np.linalg.eigvalsh(X_su3)
        return eigs

    eigs_mstar_su3 = su3_eigs(M_STAR_SEL)
    eigs_prod1_su3 = su3_eigs(M_PROD1)
    print(f"  SU(3) eigs at m*:     {eigs_mstar_su3}")
    print(f"  SU(3) eigs at m_prod1:{eigs_prod1_su3}")
    print(f"  Product (should be 1): m*={np.prod(eigs_mstar_su3):.8f}, m_prod1={np.prod(eigs_prod1_su3):.8f}")

    # The SU(3) shape at m_prod1: slots u,v,w with u*v*w=1 gives SU(3) component
    # exactly when the diagonal is (u/e^((m+S)/3), v/e^((m+S)/3), w/e^((m+S)/3))
    # But exp(H_sel) is NOT diagonal — only the diagonal ENTRIES are the slots.
    # The SU(3) shape is richer.

    print()
    print("  Condition: SU(3) component has eigenvalue product = 1 (trivially true).")
    print("  More refined: sum of SU(3) eigenvalues = Tr(exp(H))/exp((m+S)/3).")

    def su3_trace(m):
        X = expm(H3(m, S, S))
        det_val = float(np.real(np.linalg.det(X)))
        return float(np.real(np.trace(X))) / det_val ** (1.0 / 3.0)

    su3_tr_mstar = su3_trace(M_STAR_SEL)
    su3_tr_prod1 = su3_trace(M_PROD1)
    print(f"  SU(3) trace at m*:     {su3_tr_mstar:.8f}")
    print(f"  SU(3) trace at m_prod1:{su3_tr_prod1:.8f}")

    # Check SU(3) trace = 3 (uniform eigenvalues)
    su3_tr_vals = np.array([su3_trace(m) for m in m_scan])
    tr3_crossings = []
    for i in range(len(m_scan) - 1):
        if (su3_tr_vals[i] - 3.0) * (su3_tr_vals[i + 1] - 3.0) < 0:
            mc = m_scan[i] + (m_scan[i + 1] - m_scan[i]) * (3.0 - su3_tr_vals[i]) / (su3_tr_vals[i + 1] - su3_tr_vals[i])
            tr3_crossings.append(mc)

    print(f"\n  SU(3) trace = 3 crossings: {[f'{m:.8f}' for m in tr3_crossings]}")
    for mc in tr3_crossings:
        print(f"    dist from m*={abs(mc - M_STAR_SEL):.2e}, from m_prod1={abs(mc - M_PROD1):.2e}")
        check("SU(3) trace=3 gives m ≈ m*",
              abs(mc - M_STAR_SEL) < 1e-3,
              detail=f"dist={abs(mc - M_STAR_SEL):.2e}",
              kind="NUMERIC")

    # The key question: is there a topological/winding invariant that pins m*?
    # In 1D parameter space (m alone), topological invariants are just integer-valued
    # quantities that jump at special points. The Maslov index / crossing number of
    # eigenvalue tracks through zero is one such invariant.

    print()
    print("  Eigenvalue zero-crossings of H_sel(m) in scan range:")
    for m_lo, m_hi in [(-1.30, -1.00)]:
        m_s = np.linspace(m_lo, m_hi, 2000)
        eig_tracks = [np.linalg.eigvalsh(H3(m, S, S)) for m in m_s]
        eig_arr = np.array(eig_tracks)
        for col in range(3):
            for i in range(len(m_s) - 1):
                if eig_arr[i, col] * eig_arr[i + 1, col] < 0:
                    mc = m_s[i] + (m_s[i + 1] - m_s[i]) * (-eig_arr[i, col]) / (eig_arr[i + 1, col] - eig_arr[i, col])
                    print(f"    H_sel eig[{col}] crosses zero at m={mc:.8f} (dist m*={abs(mc - M_STAR_SEL):.2e})")
                    check("H_sel eigenvalue zero-crossing at m*",
                          abs(mc - M_STAR_SEL) < 1e-3,
                          detail=f"eig[{col}] zero at m={mc:.8f}",
                          kind="NUMERIC")


# ──────────────────────────────────────────────────────────────────────────────
# PART 7: The joint condition approach — m_prod1 correction from Z³ scalar potential
# ──────────────────────────────────────────────────────────────────────────────

def part7_potential_correction():
    print()
    print("=" * 88)
    print("PART 7: Z³ scalar potential — does V'(m)=0 coincide with m*?")
    print("=" * 88)
    print()

    # From the landed Z³ scalar potential work:
    # V(m) = V₀ + a₁*m + a₂*m² + a₃*m³ where all coefficients are Clifford-fixed.
    # The specific values from the existing script (frontier_z3_scalar_potential_v1.py):
    # a₁ ≈ 1.21, a₂ = 3/2, a₃ = 1/6 (approximate from the script outputs)
    # We use the EXACT values from the framework.

    # The Z³ potential from the selected-line analysis:
    # V(m) = Tr(H_sel(m)² ) = Tr((H_BASE + m*T_M + S*T_DELTA + S*T_Q)²)
    # This gives a quadratic + cubic in m via Tr(T_M^2) = 2, cross terms, etc.

    # Let's compute the Z³ scalar potential exactly.
    H_sel_0 = H3(0.0, S, S)  # H at m=0

    # V(m) = Tr(H_sel(m)†  H_sel(m)) = Tr(H_sel(m)²) since H_sel is Hermitian
    # V(m) = Tr((H_sel_0 + m*T_M)²)
    # = Tr(H_sel_0²) + 2m*Tr(H_sel_0 * T_M) + m²*Tr(T_M²)

    Tr_H02 = float(np.real(np.trace(H_sel_0 @ H_sel_0)))
    Tr_H0TM = float(np.real(np.trace(H_sel_0 @ T_M)))
    Tr_TM2 = float(np.real(np.trace(T_M @ T_M)))

    print(f"  V(m) = Tr(H_sel²) = V₀ + 2m·Tr(H₀·T_M) + m²·Tr(T_M²)")
    print(f"  Tr(H₀²) = {Tr_H02:.8f}")
    print(f"  Tr(H₀·T_M) = {Tr_H0TM:.8f}")
    print(f"  Tr(T_M²) = {Tr_TM2:.8f}")

    # V(m) = Tr_H02 + 2*Tr_H0TM * m + Tr_TM2 * m²
    # V'(m) = 2*Tr_H0TM + 2*Tr_TM2 * m = 0
    # m_min_V = -Tr_H0TM / Tr_TM2
    m_min_V = -Tr_H0TM / Tr_TM2
    print(f"  V'(m) = 0 at m_min = {m_min_V:.10f}")
    print(f"  dist from m*: {abs(m_min_V - M_STAR_SEL):.4e}")
    print(f"  dist from m_prod1: {abs(m_min_V - M_PROD1):.4e}")
    check("Z³ scalar potential minimum coincides with m*",
          abs(m_min_V - M_STAR_SEL) < 1e-3,
          detail=f"m_min={m_min_V:.8f}, dist={abs(m_min_V - M_STAR_SEL):.2e}",
          kind="NUMERIC")

    # Also check det(H_sel) = 0 condition — already known to be distinct
    # But let's check the condition Tr(H_sel² - H_sel) = 0 or similar
    print()
    print("  Related conditions:")

    # Tr(H_sel) = 0: interesting symmetry point
    # Tr(H3(m, S, S)) = m + S = 0 => m = -S
    m_tr_zero = -S
    print(f"  Tr(H_sel) = 0 at m = -S = {m_tr_zero:.8f} (dist from m*: {abs(m_tr_zero - M_STAR_SEL):.2e})")

    # det(H_sel) = 0
    def det_Hsel(m):
        return float(np.real(np.linalg.det(H3(m, S, S))))

    m_det_scan = np.linspace(-1.5, -0.5, 5000)
    det_vals = np.array([det_Hsel(m) for m in m_det_scan])
    det_crossings = []
    for i in range(len(m_det_scan) - 1):
        if det_vals[i] * det_vals[i + 1] < 0:
            mc = brentq(det_Hsel, m_det_scan[i], m_det_scan[i + 1])
            det_crossings.append(mc)

    print(f"  det(H_sel) = 0 crossings: {[f'{m:.8f}' for m in det_crossings]}")
    for mc in det_crossings:
        print(f"    dist from m*={abs(mc - M_STAR_SEL):.2e}, from m_prod1={abs(mc - M_PROD1):.2e}")
        check("det(H_sel) = 0 gives m ≈ m*",
              abs(mc - M_STAR_SEL) < 1e-3,
              detail=f"dist={abs(mc-M_STAR_SEL):.2e}",
              kind="NUMERIC")

    # Frobenius norm squared: ||H_sel||² = Tr(H†H) = Tr(H²) since Hermitian
    # The minimum of ||H_sel(m)||² = V(m) is m_min_V above.

    # The condition Tr(H_sel(m)) = SELECTOR: m = S - S = 0... no.
    # Tr(H_sel(m)) = S: m + S = S => m = 0

    # More interesting: eigenvalue sum of H_sel = Tr = m + S
    # Eigenvalue product = det. Can we find m such that these match physical condition?

    print()
    print("  Characteristic equation coefficients of H_sel(m*):")
    Hm = H3(M_STAR_SEL, S, S)
    eigs = np.linalg.eigvalsh(Hm)
    s1 = float(np.sum(eigs))       # = Tr
    s2 = float(sum(eigs[i] * eigs[j] for i in range(3) for j in range(i + 1, 3)))  # elementary sym poly
    s3 = float(np.prod(eigs))      # = det
    print(f"  s1 (Tr) = {s1:.10f} = m* + S = {M_STAR_SEL + S:.10f}")
    print(f"  s2 (sum of products of pairs) = {s2:.10f}")
    print(f"  s3 (det) = {s3:.10f}")
    # Condition s2 = 0 (sum of pairwise products = 0)
    def s2_of_m(m):
        eigs = np.linalg.eigvalsh(H3(m, S, S))
        return float(sum(eigs[i] * eigs[j] for i in range(3) for j in range(i + 1, 3)))

    s2_crossings = []
    s2_scan_m = np.linspace(-1.5, -0.5, 5000)
    s2_vals = np.array([s2_of_m(m) for m in s2_scan_m])
    for i in range(len(s2_scan_m) - 1):
        if s2_vals[i] * s2_vals[i + 1] < 0:
            mc = brentq(s2_of_m, s2_scan_m[i], s2_scan_m[i + 1])
            s2_crossings.append(mc)
    print(f"  s2(H_sel) = 0 crossings: {[f'{m:.8f}' for m in s2_crossings]}")
    for mc in s2_crossings:
        print(f"    dist from m*={abs(mc - M_STAR_SEL):.2e}")
        check("s2(H_sel) = 0 at m*",
              abs(mc - M_STAR_SEL) < 1e-3,
              detail=f"dist={abs(mc-M_STAR_SEL):.2e}",
              kind="NUMERIC")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 88)
    print("Koide 2.1e-4 gap investigation")
    print(f"  m* = {M_STAR_SEL}")
    print(f"  m_prod1 (u*v*w=1) = {M_PROD1}")
    print(f"  gap = {abs(M_STAR_SEL - M_PROD1):.2e}")
    print(f"  kappa* = {KAPPA_STAR}")
    print("=" * 88)
    print()

    part1_4x4_eigenvalue_crossing()
    part2_eigenvalue_koide()
    part3_algebraic_search()
    part4_pdg_residual()
    part5_det_condition()
    part6_topological()
    part7_potential_correction()

    print()
    print("=" * 88)
    print(f"FINAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
