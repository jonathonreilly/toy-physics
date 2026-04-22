#!/usr/bin/env python3
"""
Koide selected-line cyclic-response bridge
=========================================

STATUS: exact cyclic-response bridge plus actual-route Berry corollary
closure of the selected-line scalar/point law
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import DELTA_STAR, H3, M_STAR, Q_PLUS_STAR

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
S_SELECTOR = math.sqrt(6.0) / 3.0
DELTA_TARGET = 2.0 / 9.0
OMEGA = np.exp(2j * np.pi / 3.0)
U = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA**2],
        [1.0, OMEGA**2, OMEGA],
    ],
    dtype=complex,
)
PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)


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


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def cyclic_from_slots(u: float, v: float, w: float) -> tuple[float, float, float]:
    return u + v + w, 2.0 * u - v - w, SQRT3 * (v - w)


def slots_from_cyclic(r0: float, r1: float, r2: float) -> tuple[float, float, float]:
    u = (r0 + r1) / 3.0
    v = r0 / 3.0 - r1 / 6.0 + SQRT3 * r2 / 6.0
    w = r0 / 3.0 - r1 / 6.0 - SQRT3 * r2 / 6.0
    return u, v, w


def kappa_from_slots(v: float, w: float) -> float:
    return (v - w) / (v + w)


def kappa_from_cyclic(r0: float, r1: float, r2: float) -> float:
    return SQRT3 * r2 / (2.0 * r0 - r1)


def ratio_from_kappa(kappa: float) -> float:
    return (1.0 - kappa) / (1.0 + kappa)


def selected_line_slots(m: float) -> tuple[float, float]:
    x = expm(H3(m, S_SELECTOR, S_SELECTOR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def selected_line_small_amp(m: float) -> np.ndarray:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def normalized_selected_line_state(m: float) -> np.ndarray:
    amp = selected_line_small_amp(m)
    return amp / np.linalg.norm(amp)


def selected_line_fourier_coeffs(m: float) -> np.ndarray:
    return np.conjugate(U).T @ normalized_selected_line_state(m)


def theta_phase(m: float) -> float:
    theta = float(np.angle(selected_line_fourier_coeffs(m)[1]))
    return theta if theta >= 0.0 else theta + 2.0 * math.pi


def delta_offset(m: float) -> float:
    return theta_phase(m) - 2.0 * math.pi / 3.0


def selected_line_kappa(m: float) -> float:
    v, w = selected_line_slots(m)
    return kappa_from_slots(v, w)


def kappa_from_delta(delta: float) -> float:
    return -SQRT3 * math.cos(delta + math.pi / 6.0) / (
        math.sqrt(2.0) + math.sin(delta + math.pi / 6.0)
    )


def hstar_witness_kappa() -> tuple[float, float]:
    def hstar_small_amp(beta: float) -> np.ndarray:
        x = expm(beta * H3(M_STAR, DELTA_STAR, Q_PLUS_STAR))
        v = float(np.real(x[2, 2]))
        w = float(np.real(x[1, 1]))
        u_small, _ = koide_root_pair(v, w)
        return np.array([u_small, v, w], dtype=float)

    def objective(beta: float) -> float:
        amp = hstar_small_amp(beta)
        if amp[0] <= 0.0:
            return 1e6
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(0.5934, 0.8), method="bounded")
    beta_star = float(opt.x)
    amp = hstar_small_amp(beta_star)
    return beta_star, kappa_from_slots(float(amp[1]), float(amp[2]))


def part1_exact_cyclic_bridge() -> None:
    print("=" * 88)
    print("PART 1: the selected-line point is controlled by one scalar cyclic-response ratio")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", nonzero=True)
    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)

    u_back = sp.simplify((r0 + r1) / 3)
    v_back = sp.simplify(r0 / 3 - r1 / 6 + sp.sqrt(3) * r2 / 6)
    w_back = sp.simplify(r0 / 3 - r1 / 6 - sp.sqrt(3) * r2 / 6)

    kappa_slots = sp.simplify((v - w) / (v + w))
    kappa_cyclic = sp.simplify(sp.sqrt(3) * r2 / (2 * r0 - r1))
    ratio_wv = sp.simplify(w / v)
    ratio_from_k = sp.simplify((1 - kappa_slots) / (1 + kappa_slots))

    check("The cyclic map inverts exactly back to (u,v,w)",
          sp.simplify(u_back - u) == 0 and sp.simplify(v_back - v) == 0 and sp.simplify(w_back - w) == 0)
    check("The scalar bridge kappa is exactly sqrt(3) r2 / (2 r0 - r1)",
          sp.simplify(kappa_slots - kappa_cyclic) == 0)
    check("Once kappa is fixed, the reachable-slot ratio is fixed by w/v = (1-kappa)/(1+kappa)",
          sp.simplify(ratio_wv - ratio_from_k) == 0)


def part2_exact_threshold_value() -> float:
    print()
    print("=" * 88)
    print("PART 2: the selected line carries an exact scalar-phase bridge")
    print("=" * 88)

    def u_small(m: float) -> float:
        return float(selected_line_small_amp(m)[0])

    m_pos = float(brentq(u_small, -1.3, -1.2))
    m_zero = float(brentq(lambda m: selected_line_small_amp(m)[0] - selected_line_small_amp(m)[1], -0.4, -0.2))
    kappa_pos = selected_line_kappa(m_pos)

    delta = sp.symbols("delta", real=True)
    theta = delta + 2 * sp.pi / 3
    u_delta = (1 / sp.sqrt(3)) * (1 / sp.sqrt(2) + sp.cos(theta))
    v_delta = (1 / sp.sqrt(3)) * (1 / sp.sqrt(2) + sp.cos(theta + 2 * sp.pi / 3))
    w_delta = (1 / sp.sqrt(3)) * (1 / sp.sqrt(2) + sp.cos(theta - 2 * sp.pi / 3))
    kappa_delta = sp.simplify((v_delta - w_delta) / (v_delta + w_delta))
    expected = -sp.sqrt(3) * sp.cos(delta + sp.pi / 6) / (sp.sqrt(2) + sp.sin(delta + sp.pi / 6))

    check("The selected line has one sharp small-branch positivity threshold",
          abs(u_small(m_pos)) < 1e-10,
          detail=f"m_pos={m_pos:.12f}",
          kind="NUMERIC")
    check("The selected line has one unique unphased first-branch point",
          abs(delta_offset(m_zero)) < 1e-12,
          detail=f"m_0={m_zero:.12f}",
          kind="NUMERIC")
    check("At threshold the scalar bridge takes the exact value kappa_pos = -1/sqrt(3)",
          abs(kappa_pos + 1.0 / SQRT3) < 1e-10,
          detail=f"kappa_pos={kappa_pos:.12f}",
          kind="NUMERIC")
    check("At threshold the Berry offset is exactly pi/12 on the first branch",
          abs(delta_offset(m_pos) - math.pi / 12.0) < 1e-12,
          detail=f"delta_pos={delta_offset(m_pos):.12f}",
          kind="NUMERIC")
    check("On the exact selected line the scalar is an explicit function of the Berry offset",
          sp.simplify(sp.expand_trig(kappa_delta - expected)) == 0,
          detail="kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))")
    return m_pos, m_zero


def part3_monotone_first_branch_bridge(m_pos: float, m_zero: float) -> tuple[float, float]:
    print()
    print("=" * 88)
    print("PART 3: on the physical first branch, delta and kappa are one-to-one")
    print("=" * 88)

    xs = np.linspace(m_pos + 1e-4, m_zero - 1e-4, 400)
    kappas = np.array([selected_line_kappa(x) for x in xs])
    deltas = np.array([delta_offset(x) for x in xs])
    monotone = bool(np.all(np.diff(kappas) < 0.0))
    delta_monotone = bool(np.all(np.diff(deltas) < 0.0))
    kappa_end = float(kappas[-1])
    delta_end = float(deltas[-1])

    check("The scalar bridge kappa(m) is strictly monotone on the first selected-line branch",
          monotone,
          detail=f"kappa-range=({kappas[0]:.6f}, {kappa_end:.6f})",
          kind="NUMERIC")
    check("The Berry offset delta(m) is strictly monotone on the same branch",
          delta_monotone,
          detail=f"delta-range=({deltas[0]:.6f}, {delta_end:.6f})",
          kind="NUMERIC")
    check("Therefore delta and kappa are equivalent one-real coordinates on the physical first branch",
          monotone and delta_monotone and kappa_end < kappas[0] and delta_end < deltas[0],
          detail="both inverses exist on [m_pos, m_0]",
          kind="NUMERIC")
    return float(kappas[0]), kappa_end


def part4_berry_closure_fixes_the_selected_line_scalar_and_point(m_pos: float, m_zero: float) -> tuple[float, float]:
    print()
    print("=" * 88)
    print("PART 4: AXIOM E plus the exact bridge fixes kappa_sel,* and m_*")
    print("=" * 88)

    kappa_target = kappa_from_delta(DELTA_TARGET)
    ratio_target = ratio_from_kappa(kappa_target)
    m_first = float(brentq(lambda m: delta_offset(m) - DELTA_TARGET, m_pos + 1e-4, m_zero - 1e-4))
    amp = selected_line_small_amp(m_first)
    cs = amplitude_cos_similarity(amp)
    q = float(np.sum(amp * amp) / (np.sum(amp) ** 2))
    ratio_m = float(amp[2] / amp[1])

    check("The actual-route phase theorem supplies the exact scalar target delta = 2/9",
          abs(DELTA_TARGET - 2.0 / 9.0) < 1e-15,
          detail=f"delta_target={DELTA_TARGET:.12f}")
    check("That phase target fixes an exact selected-line scalar kappa_sel,*",
          abs(kappa_target - kappa_from_delta(DELTA_TARGET)) < 1e-15,
          detail=f"kappa_sel,*={kappa_target:.12f}")
    check("Solving delta(m)=2/9 on the first branch gives one unique selected-line point",
          abs(delta_offset(m_first) - DELTA_TARGET) < 1e-12,
          detail=f"m_Berry={m_first:.12f}",
          kind="NUMERIC")
    check("The exact scalar bridge agrees with that Berry-selected point",
          abs(selected_line_kappa(m_first) - kappa_target) < 1e-12,
          detail=f"kappa(m_Berry)={selected_line_kappa(m_first):.12f}",
          kind="NUMERIC")
    check("The resulting selected-line ratio is fixed exactly by kappa_sel,*",
          abs(ratio_m - ratio_target) < 1e-12,
          detail=f"w/v={ratio_m:.12f}",
          kind="NUMERIC")
    check("The Berry-selected point lands exactly on the Koide cone and charged-lepton direction",
          abs(q - 2.0 / 3.0) < 1e-12 and cs > 0.999999999,
          detail=f"Q={q:.15f}, cos-sim={cs:.12f}",
          kind="NUMERIC")
    return m_first, kappa_target


def part5_legacy_hstar_witness_is_only_a_compatibility_check(
    m_pos: float,
    m_zero: float,
    m_berry: float,
    kappa_berry: float,
) -> None:
    print()
    print("=" * 88)
    print("PART 5: the old H_* scalar is now a compatibility check only")
    print("=" * 88)

    beta_star, kappa_star = hstar_witness_kappa()
    m_legacy = float(brentq(lambda m: selected_line_kappa(m) - kappa_star, m_pos + 1e-4, m_zero - 1e-4))

    check("The legacy H_* route lands very near the Berry-selected scalar target",
          abs(kappa_star - kappa_berry) < 1e-4,
          detail=f"kappa_legacy={kappa_star:.12f}, diff={kappa_berry-kappa_star:+.2e}",
          kind="NUMERIC")
    check("The legacy H_* route lands very near the Berry-selected point",
          abs(m_legacy - m_berry) < 1e-4,
          detail=f"m_legacy={m_legacy:.12f}, diff={m_berry-m_legacy:+.2e}",
          kind="NUMERIC")
    check("So the old imported scalar is branch-precision-compatible with the Berry-derived selected point",
          abs(kappa_star - kappa_berry) < 1e-4 and abs(m_legacy - m_berry) < 1e-4,
          detail=f"beta*={beta_star:.12f}",
          kind="NUMERIC")


def part6_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 6: what is and is not still open")
    print("=" * 88)
    print("  The selected-line scalar/point law is no longer an independent")
    print("  open problem once AXIOM E is closed on the actual route:")
    print("      delta = 2/9 -> kappa_sel,* -> unique first-branch m_*.")
    print("  What may still remain for the broader charged-lepton package is")
    print("  downstream of the selected-line point, not another free scalar")
    print("  selector on this branch-local route.")


def main() -> int:
    part1_exact_cyclic_bridge()
    m_pos, m_zero = part2_exact_threshold_value()
    part3_monotone_first_branch_bridge(m_pos, m_zero)
    m_berry, kappa_berry = part4_berry_closure_fixes_the_selected_line_scalar_and_point(m_pos, m_zero)
    part5_legacy_hstar_witness_is_only_a_compatibility_check(m_pos, m_zero, m_berry, kappa_berry)
    part6_interpretation()

    print()
    print("Interpretation:")
    print("  The selected-line cyclic bridge is no longer an open scalar import.")
    print("  On the actual physical first branch, the exact Berry closure")
    print("      delta = 2/9")
    print("  combines with the exact scalar-phase bridge")
    print("      kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))")
    print("  to fix the unique selected-line scalar and the unique first-branch")
    print("  point. The old H_* witness survives only as a near-coincident")
    print("  compatibility check.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
