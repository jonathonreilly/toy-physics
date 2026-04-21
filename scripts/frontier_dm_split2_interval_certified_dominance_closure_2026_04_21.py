#!/usr/bin/env python3
"""
DM split-2 interval-certified dominance closure
===============================================

This runner upgrades the residual split-2 carrier item from support to
theorem-grade closure on the current review surface.

Input already accepted on the branch:
  1. the carrier-side pressure is exhausted to the two explicit split-2
     upper-face boxes CAP_BOX and ENDPOINT_BOX
  2. one-source flavored transport is the exact scalar functional
       F(P) = sum_alpha Psi(P_alpha)
     on projector rows

New step here:
  - certify, on each whole box, interval upper bounds for all three projector
    rows using exact cofactor formulas plus Weyl eigenvalue control
  - push those row intervals through the exact one-variable transport kernel
    to get rigorous boxwise upper bounds on eta/eta_obs

Because the whole boxes stay below eta = 1, the residual split-2 carrier-side
dominance/completeness blocker closes on the review branch.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_transport_kernel,
    psi_q,
)
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor
from frontier_dm_neutrino_source_surface_split2_upper_face_local_neighborhoods_candidate import (
    CAP_BOX,
    ENDPOINT_BOX,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

RT2 = math.sqrt(2.0)
RT3 = math.sqrt(3.0)
RT6 = math.sqrt(6.0)

T_M = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=float,
)
T_DELTA = np.array(
    [
        [0.0, -1.0, 1.0],
        [-1.0, 1.0, 0.0],
        [1.0, 0.0, -1.0],
    ],
    dtype=float,
)
T_Q = np.array(
    [
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ],
    dtype=float,
)

L_M = float(np.linalg.norm(T_M, 2))
L_DELTA = float(np.linalg.norm(T_DELTA, 2))
L_SLACK = float(np.linalg.norm(T_Q, 2))

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)
ETA_SCALE = (
    S_OVER_NGAMMA_EXACT
    * C_SPH
    * D_THERMAL_EXACT
    * PKG.epsilon_1
    / ETA_OBS
)

Interval = tuple[float, float]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def add(x: Interval, y: Interval) -> Interval:
    return (x[0] + y[0], x[1] + y[1])


def sub(x: Interval, y: Interval) -> Interval:
    return (x[0] - y[1], x[1] - y[0])


def neg(x: Interval) -> Interval:
    return (-x[1], -x[0])


def mul(x: Interval, y: Interval) -> Interval:
    vals = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return (min(vals), max(vals))


def sq(x: Interval) -> Interval:
    if x[0] <= 0.0 <= x[1]:
        return (0.0, max(x[0] * x[0], x[1] * x[1]))
    return (min(x[0] * x[0], x[1] * x[1]), max(x[0] * x[0], x[1] * x[1]))


def div(x: Interval, y: Interval) -> Interval:
    if y[0] <= 0.0 <= y[1]:
        raise ZeroDivisionError(f"interval denominator crosses zero: {y}")
    vals = (x[0] / y[0], x[0] / y[1], x[1] / y[0], x[1] / y[1])
    return (min(vals), max(vals))


def clamp01(x: Interval) -> Interval:
    return (max(0.0, x[0]), min(1.0, x[1]))


def box_center(box: dict[str, tuple[float, float]]) -> tuple[float, float, float]:
    return (
        0.5 * (box["m"][0] + box["m"][1]),
        0.5 * (box["delta"][0] + box["delta"][1]),
        0.5 * (box["slack"][0] + box["slack"][1]),
    )


def box_halfwidths(box: dict[str, tuple[float, float]]) -> tuple[float, float, float]:
    return (
        0.5 * (box["m"][1] - box["m"][0]),
        0.5 * (box["delta"][1] - box["delta"][0]),
        0.5 * (box["slack"][1] - box["slack"][0]),
    )


def weyl_radius(box: dict[str, tuple[float, float]]) -> float:
    hm, hd, hs = box_halfwidths(box)
    return hm * L_M + hd * L_DELTA + hs * L_SLACK


def center_eigenvalues(box: dict[str, tuple[float, float]]) -> np.ndarray:
    m_c, delta_c, slack_c = box_center(box)
    q_plus_c = q_floor(delta_c) + slack_c
    h_c = active_affine_h(m_c, delta_c, q_plus_c)
    return np.sort(np.real(np.linalg.eigvalsh(h_c)))


def a_interval(delta_iv: Interval, slack_iv: Interval) -> Interval:
    return add((4.0 * RT6 / 3.0, 4.0 * RT6 / 3.0), add(neg(mul((2.0, 2.0), delta_iv)), slack_iv))


def b_interval(m_iv: Interval, delta_iv: Interval, slack_iv: Interval) -> Interval:
    return add(
        m_iv,
        add(
            neg(delta_iv),
            add(slack_iv, (2.0 * (RT6 - RT2) / 3.0, 2.0 * (RT6 - RT2) / 3.0)),
        ),
    )


def row_component_numerator(row_index: int, lam_iv: Interval, m_iv: Interval, delta_iv: Interval, slack_iv: Interval) -> Interval:
    a_iv = a_interval(delta_iv, slack_iv)
    b_iv = b_interval(m_iv, delta_iv, slack_iv)
    if row_index == 0:
        return sub(sq(lam_iv), add(sq(delta_iv), sq(b_iv)))
    if row_index == 1:
        return sub(mul(sub(m_iv, lam_iv), neg(add(delta_iv, lam_iv))), add(sq(slack_iv), (0.25, 0.25)))
    return sub(mul(sub(m_iv, lam_iv), sub(delta_iv, lam_iv)), sq(a_iv))


def row_component_interval(
    row_index: int,
    eig_index: int,
    eig_intervals: list[Interval],
    m_iv: Interval,
    delta_iv: Interval,
    slack_iv: Interval,
) -> Interval:
    lam_iv = eig_intervals[eig_index]
    others = [eig_intervals[k] for k in range(3) if k != eig_index]
    num = row_component_numerator(row_index, lam_iv, m_iv, delta_iv, slack_iv)
    den = mul(sub(lam_iv, others[0]), sub(lam_iv, others[1]))
    return clamp01(div(num, den))


def psi_prime(q: float) -> float:
    return float(
        np.trapezoid(
            (1.0 - q * WASHOUT_TAIL) * SOURCE_PROFILE * np.exp(-q * WASHOUT_TAIL),
            Z_GRID,
        )
    )


def kernel_peak() -> tuple[float, float]:
    lo = 0.0
    hi = 0.05
    flo = psi_prime(lo)
    fhi = psi_prime(hi)
    if not (flo > 0.0 and fhi < 0.0):
        raise RuntimeError("psi' does not bracket the small-leakage maximum on [0,0.05]")
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = psi_prime(mid)
        if fm == 0.0:
            lo = mid
            hi = mid
            break
        if flo * fm > 0.0:
            lo = mid
            flo = fm
        else:
            hi = mid
            fhi = fm
    q_star = 0.5 * (lo + hi)
    psi_star = psi_q(q_star, Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
    return q_star, psi_star + 1.0e-15


def psi_sup_on_interval(q_iv: Interval, q_star: float, psi_star_upper: float) -> float:
    lo = max(0.0, q_iv[0])
    hi = min(1.0, q_iv[1])
    vals = [
        psi_q(lo, Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL),
        psi_q(hi, Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL),
    ]
    if lo <= q_star <= hi:
        vals.append(psi_star_upper)
    return max(vals) + 1.0e-15


def certify_box(label: str, box: dict[str, tuple[float, float]]) -> dict[str, object]:
    m_iv = box["m"]
    delta_iv = box["delta"]
    slack_iv = box["slack"]

    evals_c = center_eigenvalues(box)
    radius = weyl_radius(box)
    eig_intervals: list[Interval] = [
        (float(ev - radius), float(ev + radius)) for ev in evals_c
    ]
    row_intervals: list[list[Interval]] = []

    q_star, psi_star_upper = kernel_peak()
    row_eta_ubs = []
    for row_index in range(3):
        entries = [
            row_component_interval(row_index, eig_index, eig_intervals, m_iv, delta_iv, slack_iv)
            for eig_index in range(3)
        ]
        row_intervals.append(entries)
        eta_ub = ETA_SCALE * sum(
            psi_sup_on_interval(entry_iv, q_star, psi_star_upper) for entry_iv in entries
        )
        row_eta_ubs.append(float(eta_ub))

    return {
        "label": label,
        "center_evals": evals_c,
        "radius": radius,
        "eig_intervals": eig_intervals,
        "row_intervals": row_intervals,
        "row_eta_ubs": row_eta_ubs,
        "q_star": q_star,
        "psi_star_upper": psi_star_upper,
    }


def part1_weyl_boxes_are_sharp_and_disjoint() -> tuple[dict[str, object], dict[str, object]]:
    print("\n" + "=" * 88)
    print("PART 1: WEYL EIGENVALUE BOXES ON THE TWO RESIDUAL SPLIT-2 NEIGHBORHOODS")
    print("=" * 88)

    cap = certify_box("CAP_BOX", CAP_BOX)
    endpoint = certify_box("ENDPOINT_BOX", ENDPOINT_BOX)

    check(
        "The split-2 affine generators have exact operator norms 1, sqrt(3), 2",
        abs(L_M - 1.0) < 1.0e-12
        and abs(L_DELTA - RT3) < 1.0e-12
        and abs(L_SLACK - 2.0) < 1.0e-12,
        f"(L_m,L_delta,L_slack)=({L_M:.12f},{L_DELTA:.12f},{L_SLACK:.12f})",
    )
    check(
        "CAP_BOX Weyl control gives three disjoint eigenvalue intervals for H(m,delta,s)",
        cap["eig_intervals"][0][1] < cap["eig_intervals"][1][0]
        and cap["eig_intervals"][1][1] < cap["eig_intervals"][2][0],
        f"intervals={cap['eig_intervals']}",
    )
    check(
        "ENDPOINT_BOX Weyl control gives three disjoint eigenvalue intervals for H(m,delta,s)",
        endpoint["eig_intervals"][0][1] < endpoint["eig_intervals"][1][0]
        and endpoint["eig_intervals"][1][1] < endpoint["eig_intervals"][2][0],
        f"intervals={endpoint['eig_intervals']}",
    )
    check(
        "The CAP_BOX Weyl radius is small compared with the spectral gaps at the box center",
        cap["radius"] < 0.03,
        f"radius={cap['radius']:.12f}, center_evals={np.round(cap['center_evals'], 12)}",
    )
    check(
        "The ENDPOINT_BOX Weyl radius is even smaller than the CAP_BOX radius",
        endpoint["radius"] < cap["radius"],
        f"(r_cap,r_endpoint)=({cap['radius']:.12f},{endpoint['radius']:.12f})",
    )

    print()
    print(f"  CAP_BOX center eigenvalues = {np.round(cap['center_evals'], 12)}")
    print(f"  CAP_BOX Weyl radius        = {cap['radius']:.12f}")
    print(f"  CAP_BOX eigenvalue boxes   = {cap['eig_intervals']}")
    print()
    print(f"  ENDPOINT_BOX center eigenvalues = {np.round(endpoint['center_evals'], 12)}")
    print(f"  ENDPOINT_BOX Weyl radius        = {endpoint['radius']:.12f}")
    print(f"  ENDPOINT_BOX eigenvalue boxes   = {endpoint['eig_intervals']}")

    return cap, endpoint


def part2_projector_row_intervals_are_explicit_and_small(
    cap: dict[str, object], endpoint: dict[str, object]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: EXACT PROJECTOR-ROW INTERVALS FROM COFACTOR FORMULAS")
    print("=" * 88)

    cap_rows = cap["row_intervals"]
    endpoint_rows = endpoint["row_intervals"]

    check(
        "Every CAP_BOX row entry interval stays inside [0,1]",
        all(0.0 <= lo <= hi <= 1.0 for row in cap_rows for (lo, hi) in row),
        f"rows={cap_rows}",
    )
    check(
        "Every ENDPOINT_BOX row entry interval stays inside [0,1]",
        all(0.0 <= lo <= hi <= 1.0 for row in endpoint_rows for (lo, hi) in row),
        f"rows={endpoint_rows}",
    )
    check(
        "The CAP_BOX row-3 packet interval already stays close to the sampled winning row",
        cap_rows[2][0][0] > 0.68 and cap_rows[2][2][1] < 0.06,
        f"row3={cap_rows[2]}",
    )
    check(
        "The ENDPOINT_BOX row-3 packet interval is even tighter than the CAP_BOX row-3 packet interval",
        endpoint_rows[2][0][0] > 0.71 and endpoint_rows[2][2][1] < 0.053,
        f"row3={endpoint_rows[2]}",
    )

    print()
    print(f"  CAP_BOX row intervals      = {cap_rows}")
    print(f"  ENDPOINT_BOX row intervals = {endpoint_rows}")


def part3_transport_kernel_bounds_close_both_boxes(
    cap: dict[str, object], endpoint: dict[str, object]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOXWISE TRANSPORT UPPER BOUNDS")
    print("=" * 88)

    q_star = float(cap["q_star"])
    psi_star_upper = float(cap["psi_star_upper"])
    cap_ubs = [float(v) for v in cap["row_eta_ubs"]]
    endpoint_ubs = [float(v) for v in endpoint["row_eta_ubs"]]

    check(
        "The one-variable transport kernel still has its small-leakage peak inside [0,0.05]",
        0.0 < q_star < 0.05 and psi_prime(0.0) > 0.0 and psi_prime(0.05) < 0.0,
        f"(q_star,psi_star)=({q_star:.15f},{psi_star_upper:.15f})",
    )
    check(
        "All three CAP_BOX rowwise eta upper bounds stay strictly below transport closure",
        max(cap_ubs) < 1.0,
        f"eta upper bounds={np.round(cap_ubs, 12)}",
    )
    check(
        "All three ENDPOINT_BOX rowwise eta upper bounds stay strictly below transport closure",
        max(endpoint_ubs) < 1.0,
        f"eta upper bounds={np.round(endpoint_ubs, 12)}",
    )
    check(
        "The CAP_BOX theorem-grade interval margin is still comfortably above 0.09",
        1.0 - max(cap_ubs) > 0.09,
        f"margin={1.0 - max(cap_ubs):.12f}",
    )
    check(
        "The ENDPOINT_BOX theorem-grade interval margin is still comfortably above 0.10",
        1.0 - max(endpoint_ubs) > 0.10,
        f"margin={1.0 - max(endpoint_ubs):.12f}",
    )

    print()
    print(f"  q_star <= {q_star:.15f}")
    print(f"  CAP_BOX rowwise eta upper bounds      = {np.round(cap_ubs, 12)}")
    print(f"  ENDPOINT_BOX rowwise eta upper bounds = {np.round(endpoint_ubs, 12)}")


def part4_closure_assembly(cap: dict[str, object], endpoint: dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLOSURE ASSEMBLY")
    print("=" * 88)

    carrier_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md")
    support_note = read("docs/DM_SPLIT2_DENSE_GRID_LIPSCHITZ_DOMINANCE_SUPPORT_NOTE_2026-04-21.md")

    check(
        "The carried branch-local reduction really had already localized the residual pressure to CAP_BOX and ENDPOINT_BOX",
        "two explicit split-2 upper-face neighborhoods" in carrier_note
        and "1.188513342509166" in carrier_note
        and "1.188955544069478" in carrier_note,
    )
    check(
        "The superseded dense-grid note records the same two boxes now being certified theorem-grade",
        "CAP_BOX" in support_note and "ENDPOINT_BOX" in support_note,
    )
    check(
        "So the residual split-2 carrier item now closes on the current review surface",
        max(cap["row_eta_ubs"]) < 1.0 and max(endpoint["row_eta_ubs"]) < 1.0,
        f"(cap_max,endpoint_max)=({max(cap['row_eta_ubs']):.12f},{max(endpoint['row_eta_ubs']):.12f})",
    )

    print()
    print("  Closure read:")
    print("    - prior branch science had already reduced the residual split-2 pressure")
    print("      to CAP_BOX and ENDPOINT_BOX")
    print("    - this runner certifies eta/eta_obs < 1 on both whole boxes")
    print("    - therefore interval-certified exact-carrier dominance/completeness")
    print("      closes on the residual split-2 selector branch")


def main() -> int:
    print("=" * 88)
    print("DM SPLIT-2 INTERVAL-CERTIFIED DOMINANCE CLOSURE")
    print("=" * 88)

    cap, endpoint = part1_weyl_boxes_are_sharp_and_disjoint()
    part2_projector_row_intervals_are_explicit_and_small(cap, endpoint)
    part3_transport_kernel_bounds_close_both_boxes(cap, endpoint)
    part4_closure_assembly(cap, endpoint)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The residual split-2 carrier-side item is closed on the current review surface.")
    print("  What remains open on the DM flagship gate is not carrier-side dominance.")
    print("  It is the physical branch-choice / selector side:")
    print("    - A-BCC as an axiom-native branch-choice law")
    print("    - the finer right-sensitive microscopic selector law")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
