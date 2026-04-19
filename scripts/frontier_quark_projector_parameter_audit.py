#!/usr/bin/env python3
"""
Audit of which reduced quark-projector closure parameters are already supported
by current exact projector/tensor machinery.

Status:
  bounded parameter audit on top of the reduced projector-ray closure

Safe claim:
  The current branch already has a strong bounded closure on a fixed projector
  ray with two sector amplitudes plus one shared phase.

This audit asks a narrower question:
    which of those reduced parameters can already be pegged to exact constants
    that exist on the current CKM projector / support-tensor surface?

  Result:
    - the projector ray itself is exact;
    - the down-sector reduced amplitude is compatible with the exact scalar
      comparison constant rho_scalar = 1/sqrt(42);
    - a small shared phase interpreted as the support datum delta_A1(q_dem)=1/42
      used as a small angle also stays compatible with near-full closure;
    - the up-sector reduced amplitude remains the only clearly non-derived
      scalar on the current surface.

  Scope note:
    this runner audits the exact-support anchor itself. It does not attempt an
    exhaustive exact-candidate law scan for the remaining up amplitude; see
    frontier_quark_up_amplitude_candidate_scan.py for that wider shortlist.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution, minimize

from frontier_quark_projector_ray_phase_completion import (
    PROJECTOR_BRANCH,
    compute_projector_observables,
    solve_projector_surface,
)
from frontier_quark_mass_ratio_full_solve import (
    J_ATLAS,
    R_CT_OBS,
    R_UC_OBS,
    V_CB_ATLAS,
    V_UB_ATLAS,
    V_US_ATLAS,
)


PASS_COUNT = 0
FAIL_COUNT = 0

DOWN_AMPLITUDE_EXACT = 1.0 / math.sqrt(42.0)
SUPPORT_ANGLE_EXACT = -1.0 / 42.0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


@dataclass(frozen=True)
class AnchoredSolve:
    r_uc: float
    r_ct: float
    amp_u: float
    vus: float
    vcb: float
    vub: float
    jarlskog: float
    det_phase: float
    objective: float


def anchored_objective(point: np.ndarray) -> float:
    r_uc, r_ct, amp_u = point
    try:
        (
            _c13_u_base,
            _c13_d_base,
            _c13_u_total,
            _c13_d_total,
            vus,
            vcb,
            vub,
            jarlskog,
            _det_phase,
        ) = compute_projector_observables(
            [r_uc, r_ct, amp_u, DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
            shared_phase=True,
        )
    except ValueError:
        return 1.0e12

    residuals = np.array(
        [
            (r_uc - R_UC_OBS) / 1.0e-4,
            (r_ct - R_CT_OBS) / 1.0e-4,
            (vus - V_US_ATLAS) / 1.0e-4,
            (vcb - V_CB_ATLAS) / 1.0e-4,
            (vub - V_UB_ATLAS) / 1.0e-4,
            (jarlskog - J_ATLAS) / 2.0e-6,
        ],
        dtype=float,
    )
    return float(np.sum(residuals**2))


def solve_anchored_surface() -> AnchoredSolve:
    bounds = [
        (5.0e-4, 5.0e-3),
        (4.0e-3, 2.0e-2),
        (-1.0, 1.0),
    ]

    global_result = differential_evolution(
        anchored_objective,
        bounds,
        maxiter=120,
        popsize=18,
        seed=83,
        polish=False,
    )

    seeds = [
        global_result.x,
        np.array([R_UC_OBS, R_CT_OBS, 0.78], dtype=float),
        np.array([R_UC_OBS, R_CT_OBS, math.pi / 4.0], dtype=float),
    ]

    best_x: np.ndarray | None = None
    best_fun: float | None = None
    for seed in seeds:
        result = minimize(
            anchored_objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 1200},
        )
        if best_fun is None or result.fun < best_fun:
            best_x = result.x
            best_fun = float(result.fun)

    assert best_x is not None and best_fun is not None
    (
        _c13_u_base,
        _c13_d_base,
        _c13_u_total,
        _c13_d_total,
        vus,
        vcb,
        vub,
        jarlskog,
        det_phase,
    ) = compute_projector_observables(
        [best_x[0], best_x[1], best_x[2], DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
        shared_phase=True,
    )
    return AnchoredSolve(
        r_uc=float(best_x[0]),
        r_ct=float(best_x[1]),
        amp_u=float(best_x[2]),
        vus=vus,
        vcb=vcb,
        vub=vub,
        jarlskog=jarlskog,
        det_phase=det_phase,
        objective=best_fun,
    )


def percent_dev(pred: float, target: float) -> float:
    return (pred / target - 1.0) * 100.0


def part1_reference() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Strongest Reduced-Closure Reference")
    print("=" * 72)

    reduced = solve_projector_surface(shared_phase=True)
    print(f"\n  projector ray        = {PROJECTOR_BRANCH.real:+.6f} {PROJECTOR_BRANCH.imag:+.6f} i")
    print(f"  best reduced amp_u   = {reduced.amp_u:+.6f}")
    print(f"  best reduced amp_d   = {reduced.amp_d:+.6f}")
    print(f"  best shared phase    = {math.degrees(reduced.phase):+.6f} deg")
    print(f"  J/J_atlas            = {reduced.jarlskog / J_ATLAS:.6f}")

    check(
        "Strongest reduced closure still matches J within 1%",
        abs(reduced.jarlskog / J_ATLAS - 1.0) < 0.01,
        f"ratio = {reduced.jarlskog / J_ATLAS:.6f}",
    )


def part2_exact_support_anchor() -> AnchoredSolve:
    print("\n" + "=" * 72)
    print("PART 2: Exact Support-Side Anchor")
    print("=" * 72)

    anchored = solve_anchored_surface()

    print(f"\n  exact down amplitude = 1/sqrt(42) = {DOWN_AMPLITUDE_EXACT:.12f}")
    print(f"  exact support angle  = -1/42 rad  = {math.degrees(SUPPORT_ANGLE_EXACT):.6f} deg")
    print(f"  solved up amplitude  = {anchored.amp_u:.6f}")
    print()
    print(f"  m_u/m_c              = {anchored.r_uc:.6e}  (dev: {percent_dev(anchored.r_uc, R_UC_OBS):+.3f}%)")
    print(f"  m_c/m_t              = {anchored.r_ct:.6e}  (dev: {percent_dev(anchored.r_ct, R_CT_OBS):+.3f}%)")
    print(f"  |V_us|               = {anchored.vus:.9f}  (dev: {percent_dev(anchored.vus, V_US_ATLAS):+.3f}%)")
    print(f"  |V_cb|               = {anchored.vcb:.9f}  (dev: {percent_dev(anchored.vcb, V_CB_ATLAS):+.3f}%)")
    print(f"  |V_ub|               = {anchored.vub:.9f}  (dev: {percent_dev(anchored.vub, V_UB_ATLAS):+.3f}%)")
    print(f"  J                    = {anchored.jarlskog:.9e}  (dev: {percent_dev(anchored.jarlskog, J_ATLAS):+.3f}%)")
    print(f"  arg det(M_u M_d)     = {anchored.det_phase:.3e} rad")
    print(f"  objective score      = {anchored.objective:.6f}")

    check(
        "Exact down amplitude plus support-angle anchor keeps all CKM observables within 2%",
        abs(percent_dev(anchored.vus, V_US_ATLAS)) < 2.0
        and abs(percent_dev(anchored.vcb, V_CB_ATLAS)) < 2.0
        and abs(percent_dev(anchored.vub, V_UB_ATLAS)) < 2.0
        and abs(percent_dev(anchored.jarlskog, J_ATLAS)) < 2.0,
        f"devs = ({percent_dev(anchored.vus, V_US_ATLAS):+.3f}%, {percent_dev(anchored.vcb, V_CB_ATLAS):+.3f}%, {percent_dev(anchored.vub, V_UB_ATLAS):+.3f}%, {percent_dev(anchored.jarlskog, J_ATLAS):+.3f}%)",
    )
    check(
        "Exact support-side anchor keeps the quark ratios within 1%",
        abs(percent_dev(anchored.r_uc, R_UC_OBS)) < 1.0
        and abs(percent_dev(anchored.r_ct, R_CT_OBS)) < 1.0,
        f"devs = ({percent_dev(anchored.r_uc, R_UC_OBS):+.3f}%, {percent_dev(anchored.r_ct, R_CT_OBS):+.3f}%)",
    )
    check(
        "Exact support-side anchor preserves determinant neutrality",
        anchored.det_phase < 1.0e-10,
        f"arg det = {anchored.det_phase:.3e}",
    )
    return anchored


def part3_up_amplitude_audit(anchored: AnchoredSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Up-Amplitude Exact-Candidate Audit")
    print("=" * 72)

    candidate_values = {
        "pi/4": math.pi / 4.0,
        "sqrt(2/3)": math.sqrt(2.0 / 3.0),
        "5/6": 5.0 / 6.0,
        "sqrt(5)/6": math.sqrt(5.0) / 6.0,
        "sqrt(6/7)": math.sqrt(6.0 / 7.0),
    }

    best_name = ""
    best_score = float("inf")
    best_j_dev = float("inf")

    print("\n  audited exact up-amplitude candidates on the exact support-side anchor:")
    for name, value in candidate_values.items():
        (
            _c13_u_base,
            _c13_d_base,
            _c13_u_total,
            _c13_d_total,
            vus,
            vcb,
            vub,
            jarlskog,
            _det_phase,
        ) = compute_projector_observables(
            [anchored.r_uc, anchored.r_ct, value, DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
            shared_phase=True,
        )
        score = (
            abs(percent_dev(vus, V_US_ATLAS))
            + abs(percent_dev(vcb, V_CB_ATLAS))
            + abs(percent_dev(vub, V_UB_ATLAS))
            + abs(percent_dev(jarlskog, J_ATLAS))
        )
        j_dev = abs(percent_dev(jarlskog, J_ATLAS))
        if score < best_score:
            best_score = score
            best_name = name
            best_j_dev = j_dev

        print(
            f"    {name:>10s}: a_u = {value:.9f}, "
            f"devs = ({percent_dev(vus, V_US_ATLAS):+.3f}%, "
            f"{percent_dev(vcb, V_CB_ATLAS):+.3f}%, "
            f"{percent_dev(vub, V_UB_ATLAS):+.3f}%, "
            f"{percent_dev(jarlskog, J_ATLAS):+.3f}%)"
        )

    print(f"\n  best audited exact candidate = {best_name}  (aggregate abs-dev = {best_score:.3f}%)")

    check(
        "No baseline exact candidate in this limited audit set reaches sub-percent closure on the exact support-side anchor",
        best_score > 1.0,
        f"best aggregate abs-dev = {best_score:.3f}%",
    )
    check(
        "The solved up amplitude is not equal to the audited exact candidates within 0.5%",
        all(abs(anchored.amp_u / value - 1.0) * 100.0 > 0.5 for value in candidate_values.values()),
        f"solved a_u = {anchored.amp_u:.6f}",
    )


def part4_summary(anchored: AnchoredSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Summary")
    print("=" * 72)

    print("\n  Strong partial exact law on the current surface:")
    print("    - fixed CKM projector ray is exact")
    print("    - down-sector reduced amplitude a_d = 1/sqrt(42) is exact-support compatible")
    print("    - support-angle probe phi = -1/42 rad is exact-support compatible")
    print()
    print("  Remaining missing primitive:")
    print(f"    one scalar up-sector amplitude law, currently solved as a_u = {anchored.amp_u:.6f}")
    print()
    print("  Honest endpoint:")
    print("    the current projector/tensor machinery reduces the quark closure gap")
    print("    to one non-derived scalar amplitude, not a generic CP-carrier family")
    print("    A wider exact-candidate shortlist now exists, but it is still bounded.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Projector-Parameter Audit")
    print("=" * 72)

    part1_reference()
    anchored = part2_exact_support_anchor()
    part3_up_amplitude_audit(anchored)
    part4_summary(anchored)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
