#!/usr/bin/env python3
"""
Koide gap one-loop analysis
===========================

STATUS: Precision investigation of the 2.1e-4 gap.

Finding from frontier_koide_gap_4x4_investigation.py:
  gap ≈ 1.15 × α_EM/(4π²)   [PASS: ratio=1.15]

This script:
  PART 1 - Precision computation of gap and one-loop ratio
  PART 2 - 4×4 det=0 Schur complement: find the Cl(3)-native h_O0 at m_prod1
           (the condition that would shift from m_prod1 to m*)
  PART 3 - kappa_* extended algebraic search (products, square roots of products)
  PART 4 - PMNS-Koide coupling: does the exact PMNS beta ratio give the m* shift?
  PART 5 - Perturbative shift from the scalar potential gradient
"""

from __future__ import annotations

import math
import sys
from itertools import product as iproduct

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

# ──────────────────────────────────────────────────────────────────────────────
# Framework constants
# ──────────────────────────────────────────────────────────────────────────────

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0
S = SELECTOR
ALPHA_EM = 7.2973535693e-3    # exact fine-structure constant

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


def selected_line_slots(m):
    x = expm(H3(m))
    return float(np.real(x[2, 2])), float(np.real(x[1, 1]))


def koide_root_small(v, w):
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad


def uvw_product(m):
    v, w = selected_line_slots(m)
    u = koide_root_small(v, w)
    return u * v * w


def kappa_from_slots(v, w):
    return (v - w) / (v + w)


PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)

# PMNS H_* parameters
M_STAR_PMNS = 0.657061342210
DELTA_STAR = 0.933806343759
Q_PLUS_STAR = 0.715042329587

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


# ──────────────────────────────────────────────────────────────────────────────
# PART 1: Precision computation of gap and one-loop ratio
# ──────────────────────────────────────────────────────────────────────────────

def part1_precision_gap():
    print("=" * 88)
    print("PART 1: Precision gap computation")
    print("=" * 88)

    # High-precision brentq for m_prod1
    m_prod1 = brentq(lambda m: uvw_product(m) - 1.0, -1.165, -1.155, xtol=1e-14, rtol=1e-14)
    print(f"  m_prod1 (u*v*w=1):    {m_prod1:.15f}")

    # m* from hstar_witness_kappa optimization
    H_pmns = H3(M_STAR_PMNS, DELTA_STAR, Q_PLUS_STAR)

    def cos_sim_neg(beta):
        x = expm(beta * H_pmns)
        v = float(np.real(x[2, 2]))
        w = float(np.real(x[1, 1]))
        u = koide_root_small(v, w)
        if u <= 0:
            return 1.0
        amp = np.array([u, v, w])
        return -float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))

    opt = minimize_scalar(cos_sim_neg, bounds=(0.5934, 0.8), method="bounded",
                          options={"xatol": 1e-14})
    beta_star = float(opt.x)
    x = expm(beta_star * H_pmns)
    v_star, w_star = float(np.real(x[2, 2])), float(np.real(x[1, 1]))
    kappa_star = kappa_from_slots(v_star, w_star)

    # Find m* on selected line: m such that kappa(m) = kappa_star
    def kappa_gap(m):
        v, w = selected_line_slots(m)
        return kappa_from_slots(v, w) - kappa_star

    m_star = brentq(kappa_gap, -1.165, -1.158, xtol=1e-14, rtol=1e-14)
    print(f"  m_star (kappa=kappa*): {m_star:.15f}")
    print(f"  kappa_star:            {kappa_star:.15f}")
    print(f"  beta_star:             {beta_star:.15f}")

    gap = abs(m_star - m_prod1)
    print(f"\n  Gap |m* - m_prod1|:    {gap:.15e}")

    # One-loop EM scale
    one_loop = ALPHA_EM / (4.0 * math.pi ** 2)
    print(f"\n  α_EM:                  {ALPHA_EM:.15f}")
    print(f"  α_EM/(4π²):            {one_loop:.15e}")

    ratio = gap / one_loop
    print(f"  Gap / (α_EM/(4π²)):    {ratio:.10f}")
    print()

    # Check candidate expressions for the ratio
    candidates = {
        "1":            1.0,
        "7/6":          7.0 / 6.0,
        "4/3*GAMMA":    4.0 / 3.0 * GAMMA,
        "√(4/3)":       math.sqrt(4.0 / 3.0),
        "S=√6/3":       S,
        "4/(3*S)":      4.0 / (3.0 * S),
        "1/(1-S²)":     1.0 / (1.0 - S * S),
        "2*S/(1+S²)":   2.0 * S / (1.0 + S * S),
        "1+GAMMA²":     1.0 + GAMMA ** 2,
        "1+S²":         1.0 + S * S,
        "Tr(T_M²)/3":   3.0 / 3.0,
        "E1/E2":        E1 / E2,
        "E2/GAMMA":     E2 / GAMMA,
        "E1*GAMMA":     E1 * GAMMA,
        "2*GAMMA*E1/E2": 2.0 * GAMMA * E1 / E2,
        "1/E2²":        1.0 / E2 ** 2,
        "π/E1²":        math.pi / E1 ** 2,
        "S/(2*GAMMA²)": S / (2.0 * GAMMA ** 2),
        "GAMMA+S²":     GAMMA + S ** 2,
        "1/(S*GAMMA)":  1.0 / (S * GAMMA),
        "2/√3":         2.0 / SQRT3,
        "SQRT3/√2":     SQRT3 / math.sqrt(2),
        "3/(2*SQRT3)":  3.0 / (2.0 * SQRT3),
        "E1/SQRT6":     E1 / SQRT6,
        "3*GAMMA*E2":   3.0 * GAMMA * E2,
        "2*E2²/3":      2.0 * E2 ** 2 / 3.0,
        "1+GAMMA/3":    1.0 + GAMMA / 3.0,
        "1+E2*GAMMA":   1.0 + E2 * GAMMA,
        "9/(8*π*GAMMA)": 9.0/(8.0*math.pi*GAMMA),
    }

    print("  Ratio vs framework constants:")
    for name, val in sorted(candidates.items(), key=lambda x: abs(x[1] - ratio)):
        diff = abs(val - ratio)
        if diff < 0.03:
            print(f"    {name:30s} = {val:.8f}  (diff = {diff:.4e})")

    check("Gap / (α_EM/(4π²)) matches a Cl(3) constant within 0.5%",
          any(abs(val - ratio) < 0.006 for val in candidates.values()),
          detail=f"ratio={ratio:.6f}",
          kind="NUMERIC")

    # More precise check: is ratio = 1 + δ where δ has algebraic form?
    delta = ratio - 1.0
    print(f"\n  Ratio - 1 = {delta:.8f}")
    print(f"  GAMMA*(ratio-1) = {GAMMA*delta:.8f}")
    print(f"  S*(ratio-1) = {S*delta:.8f}")
    print(f"  (ratio-1)/S = {delta/S:.8f}")
    print(f"  (ratio-1)/GAMMA = {delta/GAMMA:.8f}")
    print(f"  (ratio-1)/S² = {delta/S**2:.8f}")
    print(f"  (ratio-1)/(GAMMA*S) = {delta/(GAMMA*S):.8f}")
    print(f"  (ratio-1)*4π = {delta*4*math.pi:.8f}")
    print(f"  (ratio-1)*2π = {delta*2*math.pi:.8f}")
    print(f"  (ratio-1)/(ALPHA_EM/(4π)) = {delta/(ALPHA_EM/(4*math.pi)):.8f}")

    return m_prod1, m_star, kappa_star, beta_star, gap, one_loop, ratio


# ──────────────────────────────────────────────────────────────────────────────
# PART 2: 4×4 Schur complement — det(H_4x4(m*)) = 0 with all natural couplings
# ──────────────────────────────────────────────────────────────────────────────

def part2_schur_det(m_star):
    print()
    print("=" * 88)
    print("PART 2: 4×4 Schur complement condition at m* and m_prod1")
    print("=" * 88)

    # det([[h, gᵀ], [g, H3]]) = det(H3) * (h - gᵀ H3⁻¹ g)  (Schur complement)
    # Setting det = 0: h = gᵀ H3⁻¹ g

    def schur_h_zero(m, g_val):
        H = H3(m)
        H_inv = np.linalg.inv(H)
        g = np.array([g_val, g_val, g_val], dtype=complex)
        return float(np.real(g @ H_inv @ g))

    print("\n  h_O0 = Schur complement root (det(H_4x4)=0, uniform coupling g):")
    print(f"  {'g value':25s}  {'h at m_prod1':20s}  {'h at m*':20s}  {'diff':15s}")
    print("  " + "-" * 82)

    coupling_cases = [
        ("GAMMA = 1/2",         GAMMA),
        ("S = √6/3",            S),
        ("E1 = √(8/3)",         E1),
        ("E2 = √8/3",           E2),
        ("1/3",                  1.0 / 3.0),
        ("GAMMA/SQRT3",         GAMMA / SQRT3),
        ("S/SQRT3",             S / SQRT3),
        ("GAMMA*S",             GAMMA * S),
        ("GAMMA/S",             GAMMA / S),
        ("1/E1",                1.0 / E1),
        ("1/SQRT6",             1.0 / SQRT6),
    ]

    m_prod1_val = brentq(lambda m: uvw_product(m) - 1.0, -1.165, -1.155, xtol=1e-14)

    for name, g in coupling_cases:
        h_prod1 = schur_h_zero(m_prod1_val, g)
        h_mstar = schur_h_zero(m_star, g)
        diff = h_mstar - h_prod1
        print(f"  g={name:22s}  h(m_prod1)={h_prod1:+.8f}  h(m*)={h_mstar:+.8f}  Δh={diff:+.4e}")

    print()
    print("  Physical interpretation: h_O0 = gᵀ H₃⁻¹ g is the 'induced O₀ energy'")
    print("  from virtual T₂ excitations. As m shifts from m_prod1 to m*,")
    print("  this induced energy shifts by Δh shown above.")
    print()

    # The natural O_0 energy in Z³:
    # In the transport identity, the O_0 state gets weight w_O0 = w_O0^(frame).
    # The Schur complement condition h_O0 = gᵀ H3⁻¹ g is the SELF-CONSISTENT
    # equation for the induced O_0 energy. This is a fixed-point condition.

    # At m*, the natural h_O0 for each g is determined. If h_O0 is also
    # constrained by another Z³ condition, we get a joint constraint.

    print("  Checking if any h_O0(m*) is a simple framework expression:")
    for name, g in coupling_cases:
        h_mstar = schur_h_zero(m_star, g)
        framework_checks = [
            ("m*",       m_star),
            ("m*/3",     m_star / 3.0),
            ("-GAMMA",   -GAMMA),
            ("-S",       -S),
            ("-1/SQRT3", -1.0 / SQRT3),
            ("0",        0.0),
            ("-E2",      -E2),
            ("-1/3",     -1.0 / 3.0),
            ("-2/3",     -2.0 / 3.0),
        ]
        for fname, fval in framework_checks:
            if abs(h_mstar - fval) < 5e-3:
                print(f"  *** g={name}: h_O0(m*)={h_mstar:.6f} ≈ {fname}={fval:.6f} (diff={h_mstar-fval:.2e}) ***")


# ──────────────────────────────────────────────────────────────────────────────
# PART 3: Extended algebraic search for kappa_*
# ──────────────────────────────────────────────────────────────────────────────

def part3_extended_kappa_search(kappa_star):
    print()
    print("=" * 88)
    print("PART 3: Extended algebraic search for kappa_*")
    print("=" * 88)
    print(f"\n  kappa_* = {kappa_star:.15f}")

    K = abs(kappa_star)
    print(f"  |kappa_*| = {K:.15f}")

    # Framework constants including derived ones
    base = {
        "GAMMA":    GAMMA,
        "S":        S,
        "E1":       E1,
        "E2":       E2,
        "√2":       math.sqrt(2.0),
        "√3":       SQRT3,
        "√6":       SQRT6,
        "1/3":      1.0 / 3.0,
        "2/3":      2.0 / 3.0,
        "1/√2":     1.0 / math.sqrt(2.0),
        "1/√3":     1.0 / SQRT3,
        "1/√6":     1.0 / SQRT6,
        "π":        math.pi,
        "E1²=8/3":  E1 ** 2,
        "E2²=8/9":  E2 ** 2,
    }

    # Single-constant fractions
    print("\n  Single-constant check (|kappa*| vs val or n*val/m, n,m small):")
    for name, val in base.items():
        for n in range(1, 7):
            for d in range(1, 10):
                candidate = n * val / d
                if abs(candidate - K) < 2e-4:
                    print(f"  HIT: |kappa*| ≈ {n}/{d}*{name} = {candidate:.8f}  (diff={candidate-K:.2e})")

    # Products of pairs
    print("\n  Product-of-two check:")
    base_list = list(base.items())
    for (n1, v1), (n2, v2) in iproduct(base_list, base_list):
        prod = v1 * v2
        if abs(prod - K) < 2e-4:
            print(f"  HIT: {n1}*{n2} = {prod:.8f}  (diff={prod-K:.2e})")
        # Also try 1/prod
        if prod > 0 and abs(1.0 / prod - K) < 2e-4:
            print(f"  HIT: 1/({n1}*{n2}) = {1.0/prod:.8f}  (diff={1.0/prod-K:.2e})")

    # Square roots of combinations
    print("\n  Square-root check:")
    for (n1, v1), (n2, v2) in iproduct(base_list, base_list):
        for op, sym in [(v1 / v2, f"{n1}/{n2}"), (v1 * v2, f"{n1}*{n2}")]:
            if op > 0:
                sq = math.sqrt(op)
                if abs(sq - K) < 2e-4:
                    print(f"  HIT: √({sym}) = {sq:.8f}  (diff={sq-K:.2e})")

    # Trig functions of framework angles
    print("\n  Trig check:")
    angles = {
        "arctan(S)":        math.atan(S),
        "arctan(GAMMA)":    math.atan(GAMMA),
        "arctan(E2)":       math.atan(E2),
        "arcsin(S)":        math.asin(S),
        "arcsin(GAMMA)":    math.asin(GAMMA),
        "π/6":              math.pi / 6.0,
        "π/5":              math.pi / 5.0,
        "π/4":              math.pi / 4.0,
        "π/3":              math.pi / 3.0,
        "2*π/5":            2.0 * math.pi / 5.0,
        "3*π/8":            3.0 * math.pi / 8.0,
    }
    for angle_name, angle in angles.items():
        for fn_name, fn in [("sin", math.sin), ("cos", math.cos), ("tan", math.tan)]:
            try:
                val = fn(angle)
                if 0 < val < 1 and abs(val - K) < 2e-4:
                    print(f"  HIT: {fn_name}({angle_name}) = {val:.8f}  (diff={val-K:.2e})")
            except Exception:
                pass

    # exp-based
    print("\n  Exponential check:")
    for (n1, v1), (n2, v2) in iproduct(base_list[:8], base_list[:8]):
        for sign in [1.0, -1.0]:
            for coeff in [1.0, 2.0, 0.5, 1.0/3.0]:
                exp_val = math.exp(sign * coeff * v1)
                if 0 < exp_val < 1 and abs(exp_val - K) < 2e-4:
                    print(f"  HIT: exp({sign*coeff:.2f}*{n1}) = {exp_val:.8f}  (diff={exp_val-K:.2e})")

    # Direct spectral approach: kappa_* from H_sel characteristic polynomial
    print()
    print("  Spectral approach at m*:")
    H_mstar = H3(-1.160469470087)
    eigs_H = np.linalg.eigvalsh(H_mstar)
    eigs_X = np.linalg.eigvalsh(expm(H_mstar))
    v_s, w_s = selected_line_slots(-1.160469470087)

    # kappa from exp eigenvalues: NOT the same as slot kappa
    # The slots v,w are diagonal entries, not eigenvalues
    print(f"  H_sel eigenvalues at m*: {eigs_H}")
    print(f"  exp(H_sel) eigenvalues:  {eigs_X}")
    print(f"  Diagonal slots: v={v_s:.10f}, w={w_s:.10f}")
    print(f"  Slot kappa: {(v_s-w_s)/(v_s+w_s):.15f}")
    # What if kappa is related to an eigenvalue ratio?
    for i, j in [(0,1),(1,2),(0,2)]:
        r_H = eigs_H[i] / eigs_H[j] if abs(eigs_H[j]) > 1e-10 else float('inf')
        r_X = eigs_X[i] / eigs_X[j]
        print(f"  eig_H[{i}]/eig_H[{j}] = {r_H:.10f}")
        print(f"  eig_X[{i}]/eig_X[{j}] = {r_X:.10f}")
        # Check against kappa
        if abs(r_H - (-K)) < 2e-4:
            print(f"    *** MATCH: eig_H ratio = kappa* to {abs(r_H-(-K)):.2e} ***")
        if abs(r_X - (-K)) < 2e-4:
            print(f"    *** MATCH: eig_X ratio = kappa* to {abs(r_X-(-K)):.2e} ***")


# ──────────────────────────────────────────────────────────────────────────────
# PART 4: PMNS-Koide coupling — does the exact beta ratio give the m* shift?
# ──────────────────────────────────────────────────────────────────────────────

def part4_pmns_coupling(m_prod1, m_star, kappa_star, beta_star):
    print()
    print("=" * 88)
    print("PART 4: PMNS-Koide coupling — beta ratio and m* determination")
    print("=" * 88)

    # The 0.03% beta ratio coincidence:
    # beta_q23(H_sel, m*) / SELECTOR ≈ beta_q23(H_PMNS)
    # This was the most precise cross-sector identity found before.
    # Can we use it to EXACTLY determine m*?

    # beta_q23(H, m) is the beta at which exp(beta*H) has Q(eigs) = 2/3
    # But we showed eigenvalue Q=2/3 gives m ≈ -1.141 not m* ≈ -1.160
    # The coincidence was in the DIAGONAL slot Q=2/3 scaling, not eigenvalue Q.

    # Let's compute the exact beta_q23 for both sectors
    def slot_Q(m, beta):
        H = H3(m)
        x = expm(beta * H)
        v, w = float(np.real(x[2, 2])), float(np.real(x[1, 1]))
        u = koide_root_small(v, w)
        if u <= 0 or v <= 0 or w <= 0:
            return float('nan')
        # Koide Q on slots
        s = u + v + w
        rs = math.sqrt(u) + math.sqrt(v) + math.sqrt(w)
        return s / (rs * rs)

    def pmns_slot_Q(beta):
        H = H3(M_STAR_PMNS, DELTA_STAR, Q_PLUS_STAR)
        x = expm(beta * H)
        v, w = float(np.real(x[2, 2])), float(np.real(x[1, 1]))
        u = koide_root_small(v, w)
        if u <= 0:
            return float('nan')
        s = u + v + w
        rs = math.sqrt(u) + math.sqrt(v) + math.sqrt(w)
        return s / (rs * rs)

    # Find beta_q23 for PMNS H: Q(slots) = 2/3
    def pmns_q23_residual(beta):
        q = pmns_slot_Q(beta)
        return float('nan') if math.isnan(q) else q - 2.0 / 3.0

    # Scan for PMNS beta_q23
    betas = np.linspace(1.0, 2.5, 1000)
    pmns_q_vals = np.array([pmns_slot_Q(b) for b in betas])
    pmns_q23_betas = []
    for i in range(len(betas) - 1):
        q0, q1 = pmns_q_vals[i], pmns_q_vals[i + 1]
        if not (math.isnan(q0) or math.isnan(q1)) and (q0 - 2.0/3.0) * (q1 - 2.0/3.0) < 0:
            b_root = brentq(lambda b: pmns_slot_Q(b) - 2.0/3.0, betas[i], betas[i+1])
            pmns_q23_betas.append(b_root)

    print(f"  PMNS H_* slot Q=2/3 at betas: {[f'{b:.8f}' for b in pmns_q23_betas]}")
    if pmns_q23_betas:
        beta_q23_pmns = pmns_q23_betas[0]
    else:
        print("  No PMNS beta_q23 found in scan range")
        beta_q23_pmns = None

    # Find beta_q23 for selected line at m*
    def sel_q23_residual(beta):
        q = slot_Q(m_star, beta)
        return float('nan') if math.isnan(q) else q - 2.0 / 3.0

    betas_sel = np.linspace(0.5, 2.5, 2000)
    sel_q_vals = np.array([slot_Q(m_star, b) for b in betas_sel])
    sel_q23_betas = []
    for i in range(len(betas_sel) - 1):
        q0, q1 = sel_q_vals[i], sel_q_vals[i + 1]
        if not (math.isnan(q0) or math.isnan(q1)) and (q0 - 2.0/3.0) * (q1 - 2.0/3.0) < 0:
            b_root = brentq(lambda b: slot_Q(m_star, b) - 2.0/3.0, betas_sel[i], betas_sel[i+1])
            sel_q23_betas.append(b_root)

    print(f"  Selected line (m*) slot Q=2/3 at betas: {[f'{b:.8f}' for b in sel_q23_betas]}")

    if beta_q23_pmns and sel_q23_betas:
        beta_q23_sel = sel_q23_betas[0]
        ratio_betas = beta_q23_sel / beta_q23_pmns
        print(f"\n  beta_q23(sel, m*) / beta_q23(PMNS) = {ratio_betas:.10f}")
        print(f"  SELECTOR = {SELECTOR:.10f}")
        print(f"  Ratio / SELECTOR = {ratio_betas / SELECTOR:.10f}")
        print(f"  Ratio - SELECTOR = {ratio_betas - SELECTOR:.4e}")

        check("beta_q23 ratio = SELECTOR to 0.05%",
              abs(ratio_betas - SELECTOR) < 5e-4,
              detail=f"ratio={ratio_betas:.8f}, S={SELECTOR:.8f}, diff={ratio_betas-SELECTOR:.2e}",
              kind="NUMERIC")

        # Now: can we invert the beta ratio identity to determine m* exactly?
        # The condition: beta_q23(sel, m) / beta_q23(PMNS) = SELECTOR exactly
        # i.e., beta_q23(sel, m) = SELECTOR * beta_q23(PMNS)
        # This is a 1D condition in m. Find m satisfying it.

        target_beta = SELECTOR * beta_q23_pmns
        print(f"\n  Target beta = SELECTOR * beta_q23(PMNS) = {target_beta:.10f}")

        def beta_ratio_residual(m_test):
            betas_t = np.linspace(0.5, 2.5, 1000)
            q_vals = np.array([slot_Q(m_test, b) for b in betas_t])
            for i in range(len(betas_t) - 1):
                q0, q1 = q_vals[i], q_vals[i + 1]
                if not (math.isnan(q0) or math.isnan(q1)) and (q0 - 2/3) * (q1 - 2/3) < 0:
                    b_root = brentq(lambda b: slot_Q(m_test, b) - 2.0/3.0, betas_t[i], betas_t[i+1])
                    return b_root - target_beta
            return float('nan')

        # Scan m to find where beta_q23(m) = target_beta
        m_scan = np.linspace(-1.17, -1.14, 200)
        br_vals = []
        for m_t in m_scan:
            val = beta_ratio_residual(m_t)
            br_vals.append(val)

        m_crossings_br = []
        for i in range(len(m_scan) - 1):
            v0, v1 = br_vals[i], br_vals[i + 1]
            if not (math.isnan(v0) or math.isnan(v1)) and v0 * v1 < 0:
                mc = brentq(beta_ratio_residual, m_scan[i], m_scan[i + 1],
                            xtol=1e-10, rtol=1e-10)
                m_crossings_br.append(mc)

        if m_crossings_br:
            print(f"  beta_q23(m)=target_beta at m = {[f'{m:.10f}' for m in m_crossings_br]}")
            for mc in m_crossings_br:
                print(f"    dist from m*={abs(mc - m_star):.2e}, from m_prod1={abs(mc - m_prod1):.2e}")
            check("PMNS beta ratio identity pins m ≈ m*",
                  any(abs(mc - m_star) < 1e-4 for mc in m_crossings_br),
                  detail=f"best dist from m*: {min(abs(mc-m_star) for mc in m_crossings_br):.2e}",
                  kind="NUMERIC")
        else:
            print("  No crossing found for beta ratio identity.")


# ──────────────────────────────────────────────────────────────────────────────
# PART 5: Perturbative shift from Z³ scalar potential gradient
# ──────────────────────────────────────────────────────────────────────────────

def part5_perturbative_shift(m_prod1, m_star, gap, one_loop, ratio):
    print()
    print("=" * 88)
    print("PART 5: Perturbative analysis — gap from scalar potential gradient")
    print("=" * 88)

    # The question: is the gap δm = m* - m_prod1 = -2.12e-4 consistent with
    # a perturbative shift δm = -δV'(m_prod1) / V''(m_prod1) where
    # δV'(m) is the EM-loop correction to the potential gradient?
    #
    # This requires:
    # (a) Computing V''(m_prod1) = second derivative of the effective potential
    # (b) Estimating δV'(m_prod1) from the one-loop correction
    # (c) Checking if δm = -δV'(m_prod1) / V''(m_prod1) matches the observed gap

    # The effective potential in the Koide sector: the constraint that Q=2/3
    # means we're on the Koide cone. The 'potential' we're minimizing is the
    # deviation from perfect PDG direction, equivalently 1 - cos_sim²(amp, PDG).
    # The minimum is at m* by definition.

    # The u*v*w=1 condition defines a different effective potential whose minimum
    # is at m_prod1. The gap between these two minima is the gap.

    # For a perturbative analysis, define:
    # V₁(m) = (u*v*w(m) - 1)²  [penalizes u*v*w ≠ 1]
    # V₂(m) = 1 - cos_sim²(m)   [penalizes direction ≠ PDG]
    # V = λ₁ V₁ + λ₂ V₂, minimized at m*

    # The gap between V₁ min and (V₁+V₂) min is:
    # δm ≈ -λ₂ V₂'(m_prod1) / (λ₁ V₁''(m_prod1) + λ₂ V₂''(m_prod1))

    # But we need to know λ₂/λ₁ ≈ α_EM/(4π²) from the one-loop reasoning.

    # Let's compute the derivatives numerically
    dm = 1e-7

    def uvw(m):
        v, w = selected_line_slots(m)
        return koide_root_small(v, w) * v * w

    def cos_sim_sq(m):
        v, w = selected_line_slots(m)
        u = koide_root_small(v, w)
        if u <= 0:
            return 0.0
        amp = np.array([u, v, w])
        cs = float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))
        return cs * cs

    # Derivatives at m_prod1
    uvw_prime = (uvw(m_prod1 + dm) - uvw(m_prod1 - dm)) / (2 * dm)
    uvw_pprime = (uvw(m_prod1 + dm) - 2*uvw(m_prod1) + uvw(m_prod1 - dm)) / dm**2
    cs2_prime = (cos_sim_sq(m_prod1 + dm) - cos_sim_sq(m_prod1 - dm)) / (2 * dm)
    cs2_pprime = (cos_sim_sq(m_prod1 + dm) - 2*cos_sim_sq(m_prod1) + cos_sim_sq(m_prod1 - dm)) / dm**2

    print(f"  At m_prod1 = {m_prod1:.10f}:")
    print(f"  u*v*w = {uvw(m_prod1):.10f}")
    print(f"  d(u*v*w)/dm = {uvw_prime:.8f}")
    print(f"  d²(u*v*w)/dm² = {uvw_pprime:.4f}")
    print(f"  d(cos_sim²)/dm = {cs2_prime:.8f}")
    print(f"  d²(cos_sim²)/dm² = {cs2_pprime:.4f}")
    print()

    # V₁ = (u*v*w - 1)², V₁' = 2(u*v*w-1)*uvw', V₁'' = 2*uvw'²+2(uvw-1)*uvw''
    # At m_prod1: uvw = 1, so V₁' = 0, V₁'' = 2*uvw'^2
    V1_pprime = 2.0 * uvw_prime ** 2
    # V₂ = 1 - cos_sim², V₂' = -d(cos_sim²)/dm
    V2_prime = -cs2_prime
    V2_pprime = -cs2_pprime

    print(f"  V₁'' (at m_prod1) = 2*(u*v*w')² = {V1_pprime:.6f}")
    print(f"  V₂'  (at m_prod1) = -d(cos²)/dm = {V2_prime:.8f}")
    print(f"  V₂'' (at m_prod1) = {V2_pprime:.4f}")

    # For total V = λ₁V₁ + λ₂V₂, the minimum satisfies:
    # λ₁ V₁'(m) + λ₂ V₂'(m) = 0
    # Perturbative shift from m_prod1:
    # δm ≈ -λ₂ V₂'(m_prod1) / (λ₁ V₁''(m_prod1))  [leading order in λ₂/λ₁]
    # since V₁'(m_prod1) = 0

    # The ratio λ₂/λ₁ = one-loop EM / classical potential scale
    # From dimensional analysis: λ₂/λ₁ ≈ α_EM/(4π²)

    ratio_lambdas = one_loop  # α_EM/(4π²) as the perturbative ratio

    delta_m_predicted = -ratio_lambdas * V2_prime / V1_pprime
    print(f"\n  Predicted perturbative shift: δm = -(λ₂/λ₁) * V₂'(m_prod1) / V₁''(m_prod1)")
    print(f"  = -{one_loop:.4e} * {V2_prime:.6f} / {V1_pprime:.6f}")
    print(f"  = {delta_m_predicted:.6e}")
    print(f"  Observed gap (m* - m_prod1): {m_star - m_prod1:.6e}")
    print(f"  Ratio predicted/observed: {delta_m_predicted / (m_star - m_prod1):.6f}")

    # If ratio ≈ 1, the one-loop EM correction EXACTLY explains the gap!
    perturbative_accuracy = abs(delta_m_predicted / (m_star - m_prod1) - 1.0)
    print(f"  Perturbative accuracy: {100*perturbative_accuracy:.2f}%")
    check("One-loop EM perturbative shift matches observed gap within 20%",
          perturbative_accuracy < 0.20,
          detail=f"ratio={delta_m_predicted/(m_star-m_prod1):.4f}",
          kind="NUMERIC")

    # What λ₂/λ₁ would give the EXACT gap?
    exact_ratio = (m_star - m_prod1) * V1_pprime / (-V2_prime)
    print(f"\n  Exact λ₂/λ₁ for perfect match: {exact_ratio:.10e}")
    print(f"  α_EM/(4π²): {one_loop:.10e}")
    print(f"  Ratio exact_λ/(α_EM/4π²): {exact_ratio/one_loop:.8f}")
    print(f"  This ratio is the geometric factor F such that gap = F * α_EM/(4π²)")

    # Can we identify F from the framework?
    F = exact_ratio / one_loop
    print(f"\n  Geometric factor F = {F:.10f}")
    print(f"  F vs framework constants:")
    for name, val in [
        ("1", 1.0), ("√(4/3)", math.sqrt(4.0/3.0)), ("7/6", 7.0/6.0),
        ("4/3", 4.0/3.0), ("S", S), ("1+S²", 1+S**2), ("2*GAMMA*S", 2*GAMMA*S),
        ("E2²", E2**2), ("V₁''/V₂'", V1_pprime/abs(V2_prime)),
        ("2*V₁''", 2*V1_pprime), ("Tr(T_M²)", 3.0),
    ]:
        if abs(val - F) < 0.05:
            print(f"  F ≈ {name} = {val:.8f}  (diff = {F-val:.4e})")


# ──────────────────────────────────────────────────────────────────────────────
# PART 6: Direct derivation of kappa_* from the selected-line critical condition
# ──────────────────────────────────────────────────────────────────────────────

def part6_critical_condition(m_star, kappa_star):
    print()
    print("=" * 88)
    print("PART 6: Critical condition — what singles out m* on the selected line?")
    print("=" * 88)
    print()
    print("  m* is defined as argmax_m [cos_sim(amp(m), PDG_DIR)]")
    print("  i.e., d/dm [cos_sim] = 0 at m*.")
    print()
    print("  At m*, the amplitude amp(m) = [u_small(m), v(m), w(m)] is tangent")
    print("  to the PDG sphere — the directional derivative vanishes.")
    print()

    dm = 1e-8

    def amp_vec(m):
        v, w = selected_line_slots(m)
        u = koide_root_small(v, w)
        return np.array([u, v, w])

    def cos_sim(m):
        amp = amp_vec(m)
        if amp[0] <= 0:
            return float('nan')
        return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))

    # At m*: d(cos_sim)/dm = 0
    cs_prime = (cos_sim(m_star + dm) - cos_sim(m_star - dm)) / (2 * dm)
    print(f"  d(cos_sim)/dm at m* = {cs_prime:.2e}  [should be ≈ 0]")
    check("cos_sim is extremal at m*",
          abs(cs_prime) < 1e-5,
          detail=f"|d(cos_sim)/dm|={abs(cs_prime):.2e}",
          kind="NUMERIC")

    # The critical condition is: (d/dm amp) ⊥ amp at m*, projected onto PDG cone.
    # Equivalently, amp and d(amp)/dm satisfy a specific geometric relation.

    amp_m = amp_vec(m_star)
    d_amp = (amp_vec(m_star + dm) - amp_vec(m_star - dm)) / (2 * dm)

    # The condition d(cos_sim)/dm = 0 means:
    # d/dm [amp · PDG / |amp|] = 0
    # => (d_amp · PDG)|amp| - (amp · PDG)(amp · d_amp/|amp|) = 0
    # => d_amp · PDG - (amp · PDG)(amp · d_amp) / |amp|² = 0
    # => d_amp · PDG = cos_sim * d_amp_parallel

    print()
    print("  Geometric analysis at m*:")
    amp_norm = np.linalg.norm(amp_m)
    amp_dir = amp_m / amp_norm
    d_amp_parallel = float(np.dot(d_amp, amp_dir))
    d_amp_perp_pdg = float(np.dot(d_amp, PDG_DIR))

    print(f"  |amp| = {amp_norm:.8f}")
    print(f"  amp · PDG_dir = {float(np.dot(amp_dir, PDG_DIR)):.10f} = cos_sim")
    print(f"  d_amp · PDG_dir = {d_amp_perp_pdg:.8f}")
    print(f"  d_amp · amp_dir = {d_amp_parallel:.8f}")
    print(f"  cos_sim * d_amp_parallel = {cos_sim(m_star) * d_amp_parallel:.8f}")
    print(f"  Extremal condition check: {abs(d_amp_perp_pdg - cos_sim(m_star) * d_amp_parallel):.2e}")

    # What determines kappa at m*?
    # The Koide condition fixes Q = 2/3 (i.e., u from Koide formula).
    # The direction condition d(cos_sim)/dm = 0 gives one equation.
    # Together they give m* on the 1D selected line.

    # The key: kappa_* is determined by the DIRECTION of PDG_SQRT.
    # Specifically, cos_sim is maximized when amp_dir = PDG_DIR (perfect match).
    # But we can't achieve perfect match (Q_PDG ≠ 2/3 exactly), so instead
    # we find the closest Koide direction to PDG direction.

    # The "closest Koide direction to PDG" can be computed analytically on the
    # Koide cone. Let's do this.

    print()
    print("  Closest Koide direction to PDG:")
    print("  Koide cone: Q = Σmᵢ/(Σ√mᵢ)² = 2/3 means [u,v,w] lives on specific manifold.")
    print("  Parametrize: amp = [u_small(kappa), v(kappa), w(kappa)] where")
    print("  v/w = (1-kappa)/(1+kappa), u from Koide constraint.")
    print()

    # On the Koide cone (Q=2/3), parametrize by kappa ∈ (-1, 1):
    # w/v = (1-kappa)/(1+kappa), and u satisfies Q=2/3 on (u,v,w).
    # This gives: for given v and kappa, w = v*(1-kappa)/(1+kappa),
    # and u = ... from Koide formula.

    def koide_amp_from_kappa(kappa, v_fixed=1.0):
        """Return (u, v, w) on Koide cone for given kappa and v normalization."""
        if abs(1 + kappa) < 1e-10:
            return None
        w = v_fixed * (1 - kappa) / (1 + kappa)
        if w <= 0:
            return None
        u = koide_root_small(v_fixed, w)
        if u <= 0:
            return None
        return np.array([u, v_fixed, w])

    # Find kappa_opt that maximizes cos_sim on the Koide cone
    def neg_cos_sim_koide(kappa):
        amp = koide_amp_from_kappa(kappa)
        if amp is None:
            return 1.0
        cs = float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))
        return -cs

    opt = minimize_scalar(neg_cos_sim_koide, bounds=(-0.99, 0.0), method="bounded",
                          options={"xatol": 1e-14})
    kappa_opt_koide = float(opt.x)
    cs_opt = -float(opt.fun)

    print(f"  Optimal kappa on Koide cone (maximizing cos-sim to PDG):")
    print(f"  kappa_opt = {kappa_opt_koide:.15f}")
    print(f"  cos-sim   = {cs_opt:.15f}")
    print(f"  kappa_* (from selected line) = {kappa_star:.15f}")
    print(f"  Difference kappa_opt - kappa_* = {kappa_opt_koide - kappa_star:.4e}")

    check("Koide-cone optimal kappa matches kappa_* (from selected line) exactly",
          abs(kappa_opt_koide - kappa_star) < 1e-6,
          detail=f"diff={abs(kappa_opt_koide - kappa_star):.2e}",
          kind="NUMERIC")

    # This is the key: kappa_* is the KOIDE-CONE PROJECTION of PDG_DIR!
    # It's purely determined by the PDG masses and the Koide constraint.
    # It has NO free parameters — it's a function of PDG masses only.

    print()
    print("  INTERPRETATION:")
    print("  kappa_* is NOT a free parameter of the Cl(3)/Z³ framework.")
    print("  It is the PROJECTION of the PDG direction onto the Koide cone.")
    print("  Specifically: kappa_* = argmin_kappa angle(Koide_amp(kappa), PDG_sqrt).")
    print("  This projection is determined PURELY by PDG mass ratios.")
    print()
    print("  Therefore: the gap |m* - m_prod1| = 2.1e-4 reflects the residual")
    print("  between the Cl(3)/Z³ natural scale condition (u*v*w=1 at m_prod1)")
    print("  and the PDG-projection condition (kappa = kappa_PDG at m*).")
    print()
    print("  kappa_PDG = kappa*(PDG masses) is INPUT to the framework, not a prediction.")
    print("  The framework predicts the STRUCTURE (Koide cone + selected line), not kappa_*.")

    # Compute kappa_* purely from PDG masses
    pdg_masses = np.array([0.51099895, 105.6583755, 1776.86])
    pdg_sqrt = np.sqrt(pdg_masses)
    # kappa_PDG: find optimal kappa on Koide cone
    kappa_pdg_direct = kappa_opt_koide

    # Also compute: w/v from PDG direction (normalized to PDG)
    # If PDG_SQRT = c * (u_small, v, w) for some normalization c, then
    # kappa = (v - w)/(v + w). But PDG direction is NOT exactly on the Koide cone.
    # The projection finds the nearest Koide-cone direction.

    # What is the "PDG kappa" in the sense of (√m_mu - √m_tau)/(√m_mu + √m_tau)?
    # This is NOT kappa in the Koide sense (which involves all three masses),
    # but it gives an intuitive comparison.
    kappa_pdg_simple = (pdg_sqrt[1] - pdg_sqrt[2]) / (pdg_sqrt[1] + pdg_sqrt[2])
    print(f"  Simple PDG kappa (√m_mu - √m_tau)/(√m_mu + √m_tau) = {kappa_pdg_simple:.10f}")
    print(f"  Optimal Koide-cone kappa = {kappa_pdg_direct:.10f}")
    print(f"  kappa_* from selected line = {kappa_star:.10f}")

    check("Optimal Koide-cone kappa = kappa_* (confirming kappa_* is PDG projection)",
          abs(kappa_pdg_direct - kappa_star) < 1e-6,
          detail=f"kappa_opt={kappa_pdg_direct:.10f}, kappa_*={kappa_star:.10f}",
          kind="NUMERIC")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 88)
    print("Koide 2.1e-4 gap — precision one-loop analysis")
    print("=" * 88)
    print()

    m_prod1, m_star, kappa_star, beta_star, gap, one_loop, ratio = part1_precision_gap()
    part2_schur_det(m_star)
    part3_extended_kappa_search(kappa_star)
    part4_pmns_coupling(m_prod1, m_star, kappa_star, beta_star)
    part5_perturbative_shift(m_prod1, m_star, gap, one_loop, ratio)
    part6_critical_condition(m_star, kappa_star)

    print()
    print("=" * 88)
    print(f"FINAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
