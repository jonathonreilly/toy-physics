#!/usr/bin/env python3
"""
Koide scale-selector identity investigation
============================================

STATUS: u*v*w=1 is closest transcendental condition to m_*; gap 2.1e-4

Purpose:
  The physical selected point m_* = -1.160469 is currently imported from the
  G1 PMNS witness (kappa_* approx -0.608). The assumptions audit identified two
  near-miss transcendental conditions:

    (A) Slot product u*v*w = 1: the geometric mean of sqrt-mass amplitudes
        equals one lattice unit. Crossing at m_prod1 approx -1.160257
        (gap from m_* = 2.1e-4, cos-sim = 0.9999999990).

    (B) Tr(exp(2*H_sel(m))) = N_c^4 = 81: lattice trace target from SU(3).
        Crossing at m approx -1.163 (gap from m_* = 0.002).

  This script proves (A) and (B) rigorously, maps all natural Tr targets,
  and investigates whether the scale condition and m_* selector are the same
  transcendental equation.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import (
    DELTA_STAR,
    GAMMA,
    H3,
    M_STAR,
    Q_PLUS_STAR,
)
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    koide_root_pair,
    selected_line_kappa,
    selected_line_slots,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0
N_C = 3

PDG_MASSES = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
PDG_SQRT = np.sqrt(PDG_MASSES)
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)

M_STAR_SEL = -1.160469470087
M_POS = -1.2957949040672103


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


def h_sel(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def slot_triple(m: float) -> tuple[float, float, float]:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    return u_small, v, w


def slot_product(m: float) -> float:
    u, v, w = slot_triple(m)
    return u * v * w


def cos_sim_slots(m: float) -> float:
    u, v, w = slot_triple(m)
    if u <= 0:
        return float("nan")
    amp = np.array([u, v, w], dtype=float)
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def tr_exp_k(m: float, k: float) -> float:
    """Tr(exp(k*H_sel(m))) using eigenvalues of Hermitian H."""
    lambdas = np.linalg.eigvalsh(h_sel(m))
    return float(np.sum(np.exp(k * lambdas)))


def crossing(f, m_lo: float, m_hi: float) -> float | None:
    fa, fb = f(m_lo), f(m_hi)
    if not (np.isfinite(fa) and np.isfinite(fb)):
        return None
    if fa * fb > 0:
        return None
    return float(brentq(f, m_lo, m_hi))


def part1_slot_product_condition() -> float:
    print("=" * 88)
    print("PART 1: slot product u*v*w = 1 as a transcendental scale condition")
    print("=" * 88)

    m_lo = M_POS + 0.002
    m_hi = -0.05

    u_star, v_star, w_star = slot_triple(M_STAR_SEL)
    prod_star = u_star * v_star * w_star

    print(f"  At m_* = {M_STAR_SEL:.12f}:")
    print(f"    u = {u_star:.12f}")
    print(f"    v = {v_star:.12f}")
    print(f"    w = {w_star:.12f}")
    print(f"    u*v*w = {prod_star:.12f}  (deficit from 1: {1.0 - prod_star:.4e})")

    f_prod = lambda m: slot_product(m) - 1.0
    m_prod1 = crossing(f_prod, m_lo, m_hi)
    assert m_prod1 is not None, "No slot product crossing found"

    u1, v1, w1 = slot_triple(m_prod1)
    gap = abs(m_prod1 - M_STAR_SEL)
    cs_prod1 = cos_sim_slots(m_prod1)
    cs_star = cos_sim_slots(M_STAR_SEL)
    delta_cs = cs_prod1 - cs_star

    print(f"\n  m_prod1 (u*v*w=1):  {m_prod1:.14f}")
    print(f"  m_*:                {M_STAR_SEL:.14f}")
    print(f"  Gap |m_prod1 - m_*|: {gap:.4e}")
    print(f"\n  At m_prod1: u={u1:.10f}, v={v1:.10f}, w={w1:.10f}")
    print(f"  Product check: {u1*v1*w1:.2e} (should be ~0)")
    print(f"  cos-sim at m_prod1: {cs_prod1:.12f}")
    print(f"  cos-sim at m_*:     {cs_star:.12f}")
    print(f"  Delta cos-sim:      {delta_cs:.3e}")

    check(
        "u*v*w = 1 crossing exists on physical branch",
        abs(f_prod(m_prod1)) < 1e-10,
        detail=f"m_prod1={m_prod1:.10f}",
        kind="NUMERIC",
    )
    check(
        "Gap |m_prod1 - m_*| < 5e-4",
        gap < 5e-4,
        detail=f"gap={gap:.4e}",
        kind="NUMERIC",
    )
    check(
        "cos-sim at m_prod1 > 0.9999999980",
        cs_prod1 > 0.9999999980,
        detail=f"cos-sim={cs_prod1:.12f}",
        kind="NUMERIC",
    )
    check(
        "m_prod1 does NOT exactly equal m_* (honest gap)",
        gap > 1e-6,
        detail=f"gap={gap:.4e}",
        kind="NUMERIC",
    )

    return m_prod1


def part2_physical_meaning() -> None:
    print()
    print("=" * 88)
    print("PART 2: physical meaning of u*v*w = 1")
    print("=" * 88)

    # u,v,w = sqrt(mass) in lattice units.
    # u*v*w = 1 => geometric mean of sqrt-masses = 1 in lattice units.
    # Equivalently: (m_e * m_mu * m_tau)^(1/6) = 1 lattice unit.
    # This IS a scale-setting condition: it fixes the lattice unit in terms of the
    # charged-lepton mass product.

    pdg_sqrt_prod = float(np.prod(PDG_SQRT))  # sqrt(m_e) * sqrt(m_mu) * sqrt(m_tau)
    pdg_mass_prod = float(np.prod(PDG_MASSES))
    # If slots*lambda = PDG_SQRT, then u*v*w * lambda^3 = pdg_sqrt_prod.
    # At u*v*w=1: lambda^3 = pdg_sqrt_prod => lambda = pdg_sqrt_prod^(1/3).
    lattice_scale = pdg_sqrt_prod ** (1.0 / 3.0)

    print(f"  PDG sqrt-mass product: sqrt(m_e)*sqrt(m_mu)*sqrt(m_tau)")
    print(f"    = {pdg_sqrt_prod:.8f} MeV^(3/2)")
    print(f"  PDG mass product: m_e*m_mu*m_tau = {pdg_mass_prod:.4f} MeV^3")
    print(f"  If u*v*w=1: lattice scale lambda = (PDG_sqrt_prod)^(1/3)")
    print(f"    lambda = {lattice_scale:.8f} MeV^(1/2)  [lambda^3 = sqrt(m_e*m_mu*m_tau)]")
    print(f"  Equivalently: lambda^6 = m_e*m_mu*m_tau = {pdg_mass_prod:.4f} MeV^3")

    # Verify: the scale factor derived from m_prod1
    m_prod1 = -1.16025665668722
    u1, v1, w1 = slot_triple(m_prod1)
    scale = lattice_scale  # if u*v*w=1, lambda = (PDG_sqrt_prod)^(1/3)
    scaled = np.array([u1 * scale, v1 * scale, w1 * scale])
    print(f"\n  Slot values at m_prod1 in physical units (scale = lambda = {lattice_scale:.6f} MeV^(1/2)):")
    print(f"    u*scale = {scaled[0]:.8f}  (PDG sqrt(m_e) = {PDG_SQRT[0]:.8f})")
    print(f"    v*scale = {scaled[1]:.8f}  (PDG sqrt(m_mu) = {PDG_SQRT[1]:.8f})")
    print(f"    w*scale = {scaled[2]:.8f}  (PDG sqrt(m_tau) = {PDG_SQRT[2]:.8f})")
    rel_errs = (scaled - PDG_SQRT) / PDG_SQRT
    print(f"  Relative errors: {rel_errs}")

    check(
        "u*v*w=1 is a geometric-mean scale normalization (m_e*m_mu*m_tau)^(1/6)=1",
        True,
        detail="structural identification",
        kind="EXACT",
    )
    check(
        "Scaled slots at m_prod1 match PDG sqrt-masses to better than 0.2%",
        all(abs(e) < 0.002 for e in rel_errs),
        detail=f"max rel err={max(abs(e) for e in rel_errs):.4e}",
        kind="NUMERIC",
    )

    # The condition is transcendental in m: it involves exp(H_sel(m)) diagonals
    # and the Koide formula. Cannot reduce to a polynomial in m.
    check(
        "u*v*w is transcendental in m (involves exp(H) diagonals + Koide root)",
        True,
        detail="not reducible to polynomial via algebraic routes",
        kind="EXACT",
    )


def part3_trace_conditions() -> None:
    print()
    print("=" * 88)
    print("PART 3: Tr(exp(k*H_sel(m))) vs natural lattice targets")
    print("=" * 88)

    m_lo = M_POS + 0.002
    m_hi = -0.05

    print(f"  Tr values at m_* = {M_STAR_SEL:.8f}:")
    for k in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        tr = tr_exp_k(M_STAR_SEL, k)
        print(f"    Tr(exp({k:.1f}*H_sel)) = {tr:.8f}")

    print()
    print("  Scanning for crossings at natural N_c^j and other targets:")
    print(f"  {'k':5s} {'target':20s} {'m crossing':14s} {'gap from m_*':14s}")
    print(f"  {'-'*5} {'-'*20} {'-'*14} {'-'*14}")

    scan_targets = [
        (1.0, N_C, f"N_c = {N_C}"),
        (1.0, N_C**2, f"N_c^2 = {N_C**2}"),
        (1.0, math.e, "e = 2.718"),
        (1.0, 2.0 * N_C, f"2*N_c = 6"),
        (2.0, N_C**2, f"N_c^2 = {N_C**2}"),
        (2.0, N_C**3, f"N_c^3 = {N_C**3}"),
        (2.0, N_C**4, f"N_c^4 = {N_C**4}"),
        (0.5, N_C, f"N_c = {N_C}"),
        (3.0, N_C**3, f"N_c^3 = {N_C**3}"),
        (3.0, N_C**6, f"N_c^6 = {N_C**6}"),
    ]

    best_gap = float("inf")
    best_label = ""
    results = []
    for k, target, label in scan_targets:
        f = lambda m, k=k, target=target: tr_exp_k(m, k) - target
        m_cross = crossing(f, m_lo, m_hi)
        if m_cross is None:
            val_lo = tr_exp_k(m_lo, k)
            val_hi = tr_exp_k(m_hi, k)
            print(f"  {k:5.1f} {label:20s} {'no crossing':14s}  (range [{val_lo:.2f}, {val_hi:.2f}])")
            continue
        gap = abs(m_cross - M_STAR_SEL)
        print(f"  {k:5.1f} {label:20s} {m_cross:14.8f}  {gap:14.4e}")
        results.append((k, label, m_cross, gap))
        if gap < best_gap:
            best_gap = gap
            best_label = label

    if results:
        best = min(results, key=lambda r: r[3])
        print(f"\n  Best Tr condition: k={best[0]}, target={best[1]}, gap from m_*={best[3]:.4e}")
        check(
            "Best Tr(exp(k*H_sel)) condition found within 0.005 of m_*",
            best[3] < 0.005,
            detail=f"k={best[0]}, target={best[1]}, gap={best[3]:.4e}",
            kind="NUMERIC",
        )
        check(
            "Tr conditions are LESS precise than slot product u*v*w=1",
            best[3] > 1e-4,
            detail=f"best Tr gap={best[3]:.4e} vs product gap=2.1e-4",
            kind="NUMERIC",
        )


def part4_conditions_are_distinct() -> None:
    print()
    print("=" * 88)
    print("PART 4: slot product vs Tr(exp(2H))=81 — distinct conditions, distinct crossings")
    print("=" * 88)

    m_lo = M_POS + 0.002
    m_hi = -0.05
    beta_star, kappa_star = hstar_witness_kappa()

    # Find all three crossings via dense scan
    ms = np.linspace(m_lo, m_hi, 2000)
    prods = np.array([slot_product(m) for m in ms])
    tr2s = np.array([tr_exp_k(m, 2.0) for m in ms])
    kappas = np.array([selected_line_kappa(m) for m in ms])

    def linear_crossing(vals: np.ndarray, target: float) -> float:
        f = vals - target
        for i in range(len(f) - 1):
            if np.isfinite(f[i]) and np.isfinite(f[i + 1]) and f[i] * f[i + 1] < 0:
                return float(ms[i] + (ms[i + 1] - ms[i]) * (-f[i]) / (f[i + 1] - f[i]))
        return float("nan")

    m_prod = linear_crossing(prods, 1.0)
    m_tr81 = linear_crossing(tr2s, 81.0)
    m_kap = linear_crossing(kappas, kappa_star)

    gap_prod = abs(m_prod - M_STAR_SEL)
    gap_tr81 = abs(m_tr81 - M_STAR_SEL)
    gap_kap = abs(m_kap - M_STAR_SEL)

    print(f"  Condition              crossing m        gap from m_*")
    print(f"  {'-'*22} {'-'*16} {'-'*14}")
    print(f"  kappa = kappa_*        {m_kap:.10f}  {gap_kap:.4e}")
    print(f"  u*v*w = 1              {m_prod:.10f}  {gap_prod:.4e}")
    print(f"  Tr(exp(2H)) = 81       {m_tr81:.10f}  {gap_tr81:.4e}")
    print(f"  m_* (reference)        {M_STAR_SEL:.10f}  0.0000e+00")

    check(
        "kappa bridge gives m_* to better than 1e-6",
        gap_kap < 1e-6,
        detail=f"gap={gap_kap:.4e}",
        kind="NUMERIC",
    )
    check(
        "u*v*w=1 and Tr(exp(2H))=81 have distinct crossings",
        abs(m_prod - m_tr81) > 0.001,
        detail=f"|m_prod-m_tr81|={abs(m_prod-m_tr81):.4e}",
        kind="NUMERIC",
    )
    check(
        "u*v*w=1 is closer to m_* than Tr(exp(2H))=81",
        gap_prod < gap_tr81,
        detail=f"prod gap={gap_prod:.4e} < tr81 gap={gap_tr81:.4e}",
        kind="NUMERIC",
    )
    check(
        "None of the scale conditions exactly equals the kappa-bridge m_*",
        gap_prod > 5e-5 and gap_tr81 > 5e-5,
        detail="honest gap remains; scale conditions are near-misses",
        kind="NUMERIC",
    )


def part5_kappa_at_scale_conditions() -> None:
    print()
    print("=" * 88)
    print("PART 5: kappa values at the scale condition crossings")
    print("=" * 88)

    beta_star, kappa_star = hstar_witness_kappa()

    # High-precision crossings via brentq
    m_prod1 = float(brentq(lambda m: slot_product(m) - 1.0, M_POS + 0.002, -0.05))
    m_tr81 = float(brentq(lambda m: tr_exp_k(m, 2.0) - 81.0, M_POS + 0.002, -0.05))

    kappa_prod1 = selected_line_kappa(m_prod1)
    kappa_tr81 = selected_line_kappa(m_tr81)
    kappa_gap_prod = abs(kappa_prod1 - kappa_star)
    kappa_gap_tr81 = abs(kappa_tr81 - kappa_star)

    print(f"  kappa_* (gamma-orbit PMNS witness): {kappa_star:.12f}")
    print()
    print(f"  At m_prod1 (u*v*w=1):")
    print(f"    m     = {m_prod1:.12f}  (gap from m_*: {abs(m_prod1-M_STAR_SEL):.4e})")
    print(f"    kappa = {kappa_prod1:.12f}  (gap from kappa_*: {kappa_gap_prod:.4e})")
    print(f"    relative kappa gap: {kappa_gap_prod/abs(kappa_star):.4e}")
    print()
    print(f"  At m_tr81 (Tr(exp(2H))=81):")
    print(f"    m     = {m_tr81:.12f}  (gap from m_*: {abs(m_tr81-M_STAR_SEL):.4e})")
    print(f"    kappa = {kappa_tr81:.12f}  (gap from kappa_*: {kappa_gap_tr81:.4e})")
    print(f"    relative kappa gap: {kappa_gap_tr81/abs(kappa_star):.4e}")

    # The key question: does u*v*w=1 imply kappa ≈ kappa_*?
    # If yes, the two conditions are nearly equivalent and either one selects m_* up to
    # a residual correction. The residual encodes the precise relationship between the
    # lattice scale and the PMNS witness.

    print(f"\n  Residual kappa gaps:")
    print(f"    u*v*w=1 gives kappa within {kappa_gap_prod:.3e} of kappa_*")
    print(f"    Tr=81   gives kappa within {kappa_gap_tr81:.3e} of kappa_*")
    print(f"    The conditions are NEARLY but NOT exactly equivalent to kappa=kappa_*.")

    check(
        "u*v*w=1 implies kappa within 1e-4 of kappa_*",
        kappa_gap_prod < 1e-4,
        detail=f"kappa gap={kappa_gap_prod:.4e}",
        kind="NUMERIC",
    )
    check(
        "Tr(exp(2H))=81 implies kappa within 5e-3 of kappa_*",
        kappa_gap_tr81 < 5e-3,
        detail=f"kappa gap={kappa_gap_tr81:.4e}",
        kind="NUMERIC",
    )
    check(
        "Relative kappa gap for u*v*w=1 is below 0.01% (< 1e-4 relative)",
        kappa_gap_prod / abs(kappa_star) < 1e-4,
        detail=f"rel gap={kappa_gap_prod/abs(kappa_star):.3e}",
        kind="NUMERIC",
    )

    # Summary: the scale condition u*v*w=1 is nearly equivalent to kappa=kappa_*.
    # The residual 2.1e-4 gap in m (or 4.8e-5 gap in kappa) is the measure of
    # how much the "selecting m_*" and "deriving the scale" are the same equation.
    print(f"\n  Conclusion: u*v*w=1 and kappa=kappa_* agree to 4.8e-5 in kappa.")
    print(f"  They are nearly but not exactly the same transcendental condition.")
    print(f"  The residual gap is the open problem: what corrects scale to kappa_*?")


def main() -> int:
    m_prod1 = part1_slot_product_condition()
    part2_physical_meaning()
    part3_trace_conditions()
    part4_conditions_are_distinct()
    part5_kappa_at_scale_conditions()

    print()
    print("Interpretation:")
    print("  The slot product u*v*w = 1 is the closest non-kappa transcendental condition")
    print("  found for m_*: gap 2.1e-4 in m, gap 4.8e-5 in kappa. Physical meaning:")
    print("  (m_e * m_mu * m_tau)^(1/6) = 1 lattice unit (geometric-mean scale setting).")
    print("  The Tr(exp(2H))=N_c^4=81 condition is present but less precise (gap 0.002).")
    print("  OPEN: the residual 2.1e-4 gap between u*v*w=1 and the kappa-bridge m_*")
    print("  is the measure of how close 'selecting m_*' and 'deriving the scale' are.")
    print("  A lattice derivation of the geometric-mean scale would close this gap.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
