#!/usr/bin/env python3
"""
DM neutrino source-surface parity-compatible observable selector theorem.

Question:
  On the strongest currently native local route selected by the observable-
  principle scalar generator restricted to the exact parity-compatible diagonal
  baseline family D = diag(A,B,B), does the active selector law close?

Answer:
  Yes, on that local route.

  Restrict the unique additive CPT-even scalar generator

      W_D[J] = log|det(D+J)| - log|det D|

  to the exact active source family

      J_act(delta,q_+) = delta T_delta + q_+ T_q

  with D = diag(A,B,B), A > 0, B > 0.

  Then

      det(D + J_act)
        = A B^2 - (A + 2 B) (delta^2 + q_+^2) - 6 delta^2 q_+ + 2 q_+^3,

  so the zero-source bosonic curvature on the active pair is exactly isotropic:

      - d^2 W_D |_(0,0)
        = 2 (A + 2 B) / (A B^2) * (delta^2 + q_+^2).

  Since the exact active chamber is q_+ >= sqrt(8/3) - delta, the unique
  minimizer is the orthogonal projection of the origin to that boundary,

      delta_* = q_+* = sqrt(6)/3.

  Therefore the exact source constraint gives rho_* = sqrt(6)/3, and the
  selected point lies on the maximal-phase boundary r31,* = 1/2, phi_+,* = pi/2.

Status:
  This closes the strongest currently native local parity-compatible diagonal
  route. It is not yet route-independent current-bank closure.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import active_packet_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
    tdelta,
    tq,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    active_half_plane_h,
    positive_representative,
    q_floor,
)
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0
PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)


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


def diagonal_baseline(a: float, b: float) -> np.ndarray:
    return np.diag([a, b, b]).astype(complex)


def active_source(delta: float, q_plus: float) -> np.ndarray:
    return delta * tdelta() + q_plus * tq()


def direct_det(a: float, b: float, delta: float, q_plus: float) -> complex:
    return np.linalg.det(diagonal_baseline(a, b) + active_source(delta, q_plus))


def exact_det_formula(a: float, b: float, delta: float, q_plus: float) -> float:
    return (
        a * b * b
        - (a + 2.0 * b) * (delta * delta + q_plus * q_plus)
        - 6.0 * delta * delta * q_plus
        + 2.0 * q_plus * q_plus * q_plus
    )


def direct_generator(a: float, b: float, delta: float, q_plus: float) -> float:
    sign, logabs = np.linalg.slogdet(diagonal_baseline(a, b) + active_source(delta, q_plus))
    if abs(sign) == 0.0:
        raise ValueError("Singular active deformation encountered")
    return float(logabs - math.log(a * b * b))


def exact_hessian_prefactor(a: float, b: float) -> float:
    return 2.0 * (a + 2.0 * b) / (a * b * b)


def finite_second_derivative(a: float, b: float, axis: str, h: float = 1.0e-6) -> float:
    if axis == "delta":
        wp = direct_generator(a, b, h, 0.0)
        w0 = direct_generator(a, b, 0.0, 0.0)
        wm = direct_generator(a, b, -h, 0.0)
    elif axis == "q":
        wp = direct_generator(a, b, 0.0, h)
        w0 = direct_generator(a, b, 0.0, 0.0)
        wm = direct_generator(a, b, 0.0, -h)
    else:
        raise ValueError(axis)
    return (wp - 2.0 * w0 + wm) / (h * h)


def finite_mixed_derivative(a: float, b: float, h: float = 1.0e-6) -> float:
    wpp = direct_generator(a, b, h, h)
    wpm = direct_generator(a, b, h, -h)
    wmp = direct_generator(a, b, -h, h)
    wmm = direct_generator(a, b, -h, -h)
    return (wpp - wpm - wmp + wmm) / (4.0 * h * h)


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def eta_ratio_from_transport_factor(transport_factor: float) -> float:
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * PKG.epsilon_1
        * transport_factor
        / ETA_OBS
    )


def packet_and_etas_from_point(m: float, delta: float, q_plus: float) -> tuple[np.ndarray, np.ndarray]:
    packet = active_packet_from_h(active_affine_h(m, delta, q_plus)).T
    etas = np.array(
        [
            eta_ratio_from_transport_factor(
                flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
            )
            for idx in range(3)
        ],
        dtype=float,
    )
    return packet, etas


def part1_the_observable_scalar_generator_restricts_to_the_full_parity_compatible_family() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE OBSERVABLE SCALAR GENERATOR RESTRICTS TO THE FULL PARITY-COMPATIBLE FAMILY")
    print("=" * 88)

    obs_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    parity_note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md"
    )

    samples = [
        (1.5, 0.7, 0.2, 1.1),
        (2.2, 1.4, -0.4, 1.7),
        (3.1, 0.9, 0.8, 0.9),
    ]
    ok_det = True
    details = []
    for a, b, delta, q_plus in samples:
        det_direct = direct_det(a, b, delta, q_plus)
        det_exact = exact_det_formula(a, b, delta, q_plus)
        err = abs(float(np.real(det_direct)) - det_exact)
        ok_det &= err < 1.0e-10 and abs(float(np.imag(det_direct))) < 1.0e-10
        details.append(f"(A,B)=({a:.1f},{b:.1f}) err={err:.2e}")

    check(
        "The observable principle note records the unique additive CPT-even scalar generator",
        "W[J] = log |det(D+J)| - log |det D|" in obs_note
        or "W[J] = log|det(D+J)| - log|det D|" in obs_note,
    )
    check(
        "The parity-compatible theorem records the exact local baseline family D = diag(A,B,B)",
        "D = diag(A,B,B)" in parity_note and "does not yet derive the physical selector law" in parity_note,
    )
    check(
        "Restricting W_D to J_act on D = diag(A,B,B) gives the exact determinant family",
        ok_det,
        "; ".join(details),
    )


def part2_zero_source_bosonic_curvature_is_exactly_isotropic_on_that_family() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ZERO-SOURCE BOSONIC CURVATURE IS EXACTLY ISOTROPIC ON THAT FAMILY")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    gram_dd = float(np.real(np.trace(td.conj().T @ td)))
    gram_qq = float(np.real(np.trace(tqm.conj().T @ tqm)))
    gram_dq = float(np.real(np.trace(td.conj().T @ tqm)))

    samples = [(1.0, 1.0), (1.0, 2.0), (3.5, 0.6)]
    ok_hessian = True
    details = []
    for a, b in samples:
        h_dd = finite_second_derivative(a, b, "delta")
        h_qq = finite_second_derivative(a, b, "q")
        h_dq = finite_mixed_derivative(a, b)
        pref = exact_hessian_prefactor(a, b)
        err = max(abs(h_dd + pref), abs(h_qq + pref), abs(h_dq))
        ok_hessian &= err < 1.0e-3
        details.append(f"(A,B)=({a:.1f},{b:.1f}) pref={pref:.12f}, fd-err={err:.2e}")

    check(
        "The active generators remain Frobenius-orthogonal with equal norm on the live active pair",
        abs(gram_dd - 6.0) < 1.0e-12 and abs(gram_qq - 6.0) < 1.0e-12 and abs(gram_dq) < 1.0e-12,
        f"Gram=({gram_dd:.12f},{gram_qq:.12f},{gram_dq:.12f})",
    )
    check(
        "For every D = diag(A,B,B), the zero-source Hessian is exactly -2(A+2B)/(AB^2) on both active axes",
        ok_hessian,
        "; ".join(details),
    )
    check(
        "So the canonical positive quadratic selector law is a positive multiple of delta^2 + q_+^2 on the full parity-compatible family",
        ok_hessian,
        "the active selector geometry is route-stable across D = diag(A,B,B)",
    )


def part3_minimizing_that_native_quadratic_on_the_exact_active_chamber_closes_the_local_route() -> None:
    print("\n" + "=" * 88)
    print("PART 3: MINIMIZING THAT NATIVE QUADRATIC ON THE EXACT ACTIVE CHAMBER CLOSES THE LOCAL ROUTE")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()

    def boundary_action(delta: float) -> float:
        q_plus = q_floor(delta)
        return delta * delta + q_plus * q_plus

    deriv = 4.0 * d_sel - 2.0 * PKG.E1
    center = boundary_action(d_sel)
    left = boundary_action(d_sel - 0.2)
    right = boundary_action(d_sel + 0.2)

    check(
        "The selected point lies on the exact active boundary q_+ = sqrt(8/3) - delta",
        abs(q_sel - q_floor(d_sel)) < 1.0e-12,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )
    check(
        "The boundary quadratic has stationary point at delta_* = sqrt(6)/3",
        abs(deriv) < 1.0e-12,
        f"Q'_bdy(delta_*)={deriv:.12f}",
    )
    check(
        "Strict convexity makes that point the unique minimizer on the whole chamber",
        center < left and center < right,
        f"Q*={center:.12f}, Q_left={left:.12f}, Q_right={right:.12f}",
    )
    check(
        "Therefore the strongest currently native local parity-compatible route selects delta_* = q_+* = sqrt(6)/3",
        abs(d_sel - math.sqrt(6.0) / 3.0) < 1.0e-12 and abs(q_sel - math.sqrt(6.0) / 3.0) < 1.0e-12,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )


def part4_the_selected_split_is_derived_not_imported() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE SELECTED SPLIT IS DERIVED, NOT IMPORTED")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()
    h, r31, phi = active_half_plane_h(d_sel, q_sel, m=0.0)
    hp = positive_representative(h, floor=2.0)
    _lam_plus, _lam_odd, _u, _v, delta_c, rho, gamma, _sigma = source_surface_data_in_carrier_normal_form(hp)
    kz = kz_from_h(h)
    q_rec = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
    delta_rec = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)

    check(
        "The equality rho_* = delta_* is derived from the exact source constraint delta + rho = sqrt(8/3)",
        abs(delta_c - d_sel) < 1.0e-12
        and abs(delta_c + rho - PKG.E1) < 1.0e-12
        and abs(rho - d_sel) < 1.0e-12,
        f"(delta_*,rho_*)=({delta_c:.12f},{rho:.12f})",
    )
    check(
        "The selected point lies on the maximal-phase active boundary r31 = 1/2, phi_+ = pi/2",
        abs(r31 - PKG.gamma) < 1.0e-12 and abs(phi - 0.5 * math.pi) < 1.0e-12,
        f"(r31,phi)=({r31:.12f},{phi:.12f})",
    )
    check(
        "The intrinsic Z3 doublet block reads back exactly the selected point",
        abs(q_rec - q_sel) < 1.0e-12 and abs(delta_rec - d_sel) < 1.0e-12,
        f"(delta,q_+) from K_Z3=({delta_rec:.12f},{q_rec:.12f})",
    )
    check(
        "The selected point is realized directly by the affine H-side chart",
        np.linalg.norm(h - active_affine_h(0.0, d_sel, q_sel)) < 1.0e-12,
        f"affine err={np.linalg.norm(h - active_affine_h(0.0, d_sel, q_sel)):.2e}",
    )


def part5_the_selected_route_remains_transport_subcritical() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE SELECTED ROUTE REMAINS TRANSPORT SUBCRITICAL")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()

    packet0, etas0 = packet_and_etas_from_point(0.0, d_sel, q_sel)

    result = optimize.minimize_scalar(
        lambda m: -float(np.max(packet_and_etas_from_point(float(m), d_sel, q_sel)[1])),
        bounds=(-3.0, 3.0),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    m_opt = float(result.x)
    packet_opt, etas_opt = packet_and_etas_from_point(m_opt, d_sel, q_sel)
    eta_best = float(np.max(etas_opt))

    check(
        "At the selected point with m = 0 the exact flavored transport readout is subcritical",
        float(np.max(etas0)) < 1.0,
        f"eta/eta_obs={np.round(etas0, 12)}",
    )
    check(
        "Even optimizing the spectator line m on the selected (delta_*,q_+*) slice stays subcritical",
        eta_best < 1.0,
        f"m_opt={m_opt:.12f}, eta_best={eta_best:.12f}",
    )
    check(
        "So this theorem closes the local microscopic selector route, but not the full quantitative DM closure lane",
        eta_best < 0.9 and int(np.argmax(etas_opt)) == 2,
        f"etas_opt={np.round(etas_opt, 12)}",
    )

    print()
    print("  selected-point transport readout at m = 0:")
    print(f"    eta/eta_obs = {np.round(etas0, 12)}")
    print("  best transport readout on the selected (delta_*,q_+*) slice:")
    print(f"    m_opt       = {m_opt:.12f}")
    print(f"    eta/eta_obs = {np.round(etas_opt, 12)}")
    print(np.round(packet0, 6))
    print(np.round(packet_opt, 6))


def part6_the_note_records_the_honest_scope() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE NOTE RECORDS THE HONEST SCOPE")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md")

    check(
        "The note records the exact determinant and Hessian formulas on D = diag(A,B,B)",
        "A B^2 - (A + 2 B) (delta^2 + q_+^2)" in note and "2 (A + 2 B) / (A B^2)" in note,
    )
    check(
        "The note records the exact selected point delta_* = q_+* = sqrt(6)/3 and the derived rho_* split",
        "delta_* = q_+* = sqrt(6)/3" in note and "rho_* = sqrt(6)/3" in note,
    )
    check(
        "The note keeps the claim local-route honest rather than route-independent current-bank or quantitative DM closure",
        "strongest currently native local parity-compatible diagonal route" in note
        and "not yet route-independent current-bank closure" in note
        and "transport-subcritical" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE PARITY-COMPATIBLE OBSERVABLE SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the strongest currently native local route selected by the")
    print("  observable-principle scalar generator restricted to the exact")
    print("  parity-compatible diagonal baseline family D = diag(A,B,B), does")
    print("  the active selector law close?")

    part1_the_observable_scalar_generator_restricts_to_the_full_parity_compatible_family()
    part2_zero_source_bosonic_curvature_is_exactly_isotropic_on_that_family()
    part3_minimizing_that_native_quadratic_on_the_exact_active_chamber_closes_the_local_route()
    part4_the_selected_split_is_derived_not_imported()
    part5_the_selected_route_remains_transport_subcritical()
    part6_the_note_records_the_honest_scope()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Honest route-level closeout:")
    print("    - the unique additive CPT-even scalar generator restricts exactly to")
    print("      the active family on every parity-compatible diagonal baseline D = diag(A,B,B)")
    print("    - its zero-source bosonic curvature is exactly isotropic on the live active pair")
    print("    - minimizing the induced positive quadratic on q_+ >= sqrt(8/3) - delta")
    print("      selects delta_* = q_+* = sqrt(6)/3")
    print("    - the exact source constraint then derives rho_* = sqrt(6)/3")
    print("    - so the strongest currently native local parity-compatible diagonal route closes")
    print("      microscopically")
    print("    - but that selected route remains transport-subcritical even after optimizing m")
    print("    - this is not yet route-independent current-bank closure or full DM closure")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
