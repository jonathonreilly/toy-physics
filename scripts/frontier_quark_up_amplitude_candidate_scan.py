#!/usr/bin/env python3
"""
Bounded exact-candidate scan for the remaining reduced up-sector quark
amplitude law.

Status:
  bounded exact-candidate shortlist on the projector/support closure surface

Safe claim:
  The current branch does not yet derive the reduced up-sector amplitude
  `a_u` from the projector/tensor machinery.

  But the exact-support anchor now reduces that gap to a short exact-candidate
  shortlist:
    - a best small-rational candidate,
    - a best small-radical candidate,
    - and a strongest current projector/support-native dressing family.

  This is still bounded candidate support, not a retained theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from frontier_quark_mass_ratio_full_solve import (
    J_ATLAS,
    R_CT_OBS,
    R_UC_OBS,
    V_CB_ATLAS,
    V_UB_ATLAS,
    V_US_ATLAS,
)
from frontier_quark_projector_parameter_audit import (
    DOWN_AMPLITUDE_EXACT,
    SUPPORT_ANGLE_EXACT,
    compute_projector_observables,
    percent_dev,
    solve_anchored_surface,
)


PASS_COUNT = 0
FAIL_COUNT = 0


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
class CandidateEvaluation:
    label: str
    family: str
    value: float
    anchor_aggregate: float
    anchor_max: float
    anchor_vus_dev: float
    anchor_vcb_dev: float
    anchor_vub_dev: float
    anchor_j_dev: float
    refit_objective: float
    refit_aggregate: float
    refit_max: float
    r_uc: float
    r_ct: float
    refit_r_uc_dev: float
    refit_r_ct_dev: float
    refit_vus_dev: float
    refit_vcb_dev: float
    refit_vub_dev: float
    refit_j_dev: float
    det_phase: float


def exact_support_anchor() -> tuple[float, float, float]:
    anchored = solve_anchored_surface()
    return anchored.r_uc, anchored.r_ct, anchored.amp_u


def anchor_deviations(a_u: float, r_uc: float, r_ct: float) -> tuple[float, float, float, float]:
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
        [r_uc, r_ct, a_u, DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
        shared_phase=True,
    )
    return (
        percent_dev(vus, V_US_ATLAS),
        percent_dev(vcb, V_CB_ATLAS),
        percent_dev(vub, V_UB_ATLAS),
        percent_dev(jarlskog, J_ATLAS),
    )


def refit_objective(a_u: float, point: np.ndarray) -> float:
    r_uc, r_ct = point
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
            [r_uc, r_ct, a_u, DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
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


def evaluate_candidate(label: str, family: str, value: float, anchor_r_uc: float, anchor_r_ct: float) -> CandidateEvaluation:
    anchor_vus_dev, anchor_vcb_dev, anchor_vub_dev, anchor_j_dev = anchor_deviations(value, anchor_r_uc, anchor_r_ct)
    anchor_aggregate = (
        abs(anchor_vus_dev)
        + abs(anchor_vcb_dev)
        + abs(anchor_vub_dev)
        + abs(anchor_j_dev)
    )
    anchor_max = max(
        abs(anchor_vus_dev),
        abs(anchor_vcb_dev),
        abs(anchor_vub_dev),
        abs(anchor_j_dev),
    )

    result = minimize(
        lambda point: refit_objective(value, point),
        np.array([anchor_r_uc, anchor_r_ct], dtype=float),
        method="L-BFGS-B",
        bounds=[(5.0e-4, 5.0e-3), (4.0e-3, 2.0e-2)],
        options={"maxiter": 1200},
    )
    r_uc, r_ct = map(float, result.x)

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
        [r_uc, r_ct, value, DOWN_AMPLITUDE_EXACT, SUPPORT_ANGLE_EXACT],
        shared_phase=True,
    )

    refit_r_uc_dev = percent_dev(r_uc, R_UC_OBS)
    refit_r_ct_dev = percent_dev(r_ct, R_CT_OBS)
    refit_vus_dev = percent_dev(vus, V_US_ATLAS)
    refit_vcb_dev = percent_dev(vcb, V_CB_ATLAS)
    refit_vub_dev = percent_dev(vub, V_UB_ATLAS)
    refit_j_dev = percent_dev(jarlskog, J_ATLAS)
    refit_aggregate = (
        abs(refit_r_uc_dev)
        + abs(refit_r_ct_dev)
        + abs(refit_vus_dev)
        + abs(refit_vcb_dev)
        + abs(refit_vub_dev)
        + abs(refit_j_dev)
    )
    refit_max = max(
        abs(refit_r_uc_dev),
        abs(refit_r_ct_dev),
        abs(refit_vus_dev),
        abs(refit_vcb_dev),
        abs(refit_vub_dev),
        abs(refit_j_dev),
    )

    return CandidateEvaluation(
        label=label,
        family=family,
        value=value,
        anchor_aggregate=anchor_aggregate,
        anchor_max=anchor_max,
        anchor_vus_dev=anchor_vus_dev,
        anchor_vcb_dev=anchor_vcb_dev,
        anchor_vub_dev=anchor_vub_dev,
        anchor_j_dev=anchor_j_dev,
        refit_objective=float(result.fun),
        refit_aggregate=refit_aggregate,
        refit_max=refit_max,
        r_uc=r_uc,
        r_ct=r_ct,
        refit_r_uc_dev=refit_r_uc_dev,
        refit_r_ct_dev=refit_r_ct_dev,
        refit_vus_dev=refit_vus_dev,
        refit_vcb_dev=refit_vcb_dev,
        refit_vub_dev=refit_vub_dev,
        refit_j_dev=refit_j_dev,
        det_phase=det_phase,
    )


def build_small_rational_candidates() -> dict[str, float]:
    candidates: dict[str, float] = {}
    for p in range(1, 13):
        for q in range(1, 13):
            value = p / q
            if 0.3 < value < 1.2:
                candidates[f"{p}/{q}"] = value
    return candidates


def build_small_radical_candidates() -> dict[str, float]:
    candidates: dict[str, float] = {}
    for p in range(1, 13):
        for q in range(1, 13):
            value = math.sqrt(p / q)
            if 0.3 < value < 1.2:
                candidates[f"sqrt({p}/{q})"] = value
    return candidates


def build_native_candidates() -> dict[str, float]:
    rho_scalar = 1.0 / math.sqrt(42.0)
    eta = math.sqrt(5.0) / 6.0
    projector_mag = math.sqrt(5.0 / 6.0)
    noncentral_support = 6.0 / 7.0
    return {
        "sqrt(6/7)-1/sqrt(42)": math.sqrt(6.0 / 7.0) - rho_scalar,
        "sqrt(5/6)*(6/7)": projector_mag * noncentral_support,
        "sqrt(5/6)*(1-1/sqrt(42))": projector_mag * (1.0 - rho_scalar),
        "atan(sqrt(5))-sqrt(5)/6": math.atan(math.sqrt(5.0)) - eta,
        "pi/4": math.pi / 4.0,
        "7/9": 7.0 / 9.0,
        "sqrt(3/5)": math.sqrt(3.0 / 5.0),
    }


def rank_family(name: str, candidates: dict[str, float], anchor_r_uc: float, anchor_r_ct: float) -> list[CandidateEvaluation]:
    evaluations = [
        evaluate_candidate(label, name, value, anchor_r_uc, anchor_r_ct)
        for label, value in candidates.items()
    ]
    evaluations.sort(key=lambda item: (item.refit_objective, item.anchor_aggregate, item.label))
    return evaluations


def print_candidate_row(candidate: CandidateEvaluation) -> None:
    print(
        f"  {candidate.label:28s} "
        f"a_u={candidate.value:.9f}  "
        f"anchor={candidate.anchor_aggregate:.3f}%  "
        f"refit_obj={candidate.refit_objective:.6f}  "
        f"refit_max={candidate.refit_max:.3f}%"
    )


def part1_reference() -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART 1: Exact-Support Anchor")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    print(f"\n  exact down amplitude = 1/sqrt(42) = {DOWN_AMPLITUDE_EXACT:.12f}")
    print(f"  exact support angle  = -1/42 rad  = {math.degrees(SUPPORT_ANGLE_EXACT):.6f} deg")
    print(f"  solved up amplitude  = {solved_a_u:.12f}")
    return anchor_r_uc, anchor_r_ct, solved_a_u


def part2_curated_scan(anchor_r_uc: float, anchor_r_ct: float) -> list[CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("PART 2: Curated Exact-Candidate Laws")
    print("=" * 72)

    curated = rank_family("native", build_native_candidates(), anchor_r_uc, anchor_r_ct)
    print("\n  curated exact candidates on the exact-support anchor:")
    for candidate in sorted(curated, key=lambda item: (item.anchor_aggregate, item.refit_objective, item.label)):
        print_candidate_row(candidate)

    best_anchor = min(curated, key=lambda item: item.anchor_aggregate)
    best_refit = min(curated, key=lambda item: item.refit_objective)

    print(f"\n  best anchored-observable candidate = {best_anchor.label}")
    print(f"    anchor aggregate = {best_anchor.anchor_aggregate:.3f}%")
    print(
        "    anchor devs      = "
        f"({best_anchor.anchor_vus_dev:+.3f}%, {best_anchor.anchor_vcb_dev:+.3f}%, "
        f"{best_anchor.anchor_vub_dev:+.3f}%, {best_anchor.anchor_j_dev:+.3f}%)"
    )
    print(f"\n  best two-ratio-refit candidate     = {best_refit.label}")
    print(f"    refit objective  = {best_refit.refit_objective:.6f}")
    print(
        "    refit devs       = "
        f"({best_refit.refit_r_uc_dev:+.3f}%, {best_refit.refit_r_ct_dev:+.3f}%, "
        f"{best_refit.refit_vus_dev:+.3f}%, {best_refit.refit_vcb_dev:+.3f}%, "
        f"{best_refit.refit_vub_dev:+.3f}%, {best_refit.refit_j_dev:+.3f}%)"
    )

    check(
        "Curated scan beats the old pi/4 baseline on the anchored observable package",
        best_anchor.anchor_aggregate < next(
            candidate.anchor_aggregate for candidate in curated if candidate.label == "pi/4"
        ),
        f"best = {best_anchor.anchor_aggregate:.3f}%, pi/4 = {next(candidate.anchor_aggregate for candidate in curated if candidate.label == 'pi/4'):.3f}%",
    )
    check(
        "Curated best candidate keeps anchored CKM+J deviations below 1%",
        best_anchor.anchor_max < 1.0,
        f"max dev = {best_anchor.anchor_max:.3f}%",
    )
    check(
        "Curated best refit candidate keeps the full package within 1%",
        best_refit.refit_max < 1.0,
        f"max dev = {best_refit.refit_max:.3f}%",
    )
    return curated


def part3_grammar_scan(anchor_r_uc: float, anchor_r_ct: float) -> tuple[CandidateEvaluation, CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("PART 3: Small Rational / Radical Grammar Scan")
    print("=" * 72)

    rationals = rank_family("rational", build_small_rational_candidates(), anchor_r_uc, anchor_r_ct)
    radicals = rank_family("radical", build_small_radical_candidates(), anchor_r_uc, anchor_r_ct)

    best_rational = rationals[0]
    best_radical = radicals[0]

    print("\n  best small-rational candidates:")
    for candidate in rationals[:5]:
        print_candidate_row(candidate)

    print("\n  best small-radical candidates:")
    for candidate in radicals[:5]:
        print_candidate_row(candidate)

    check(
        "Best small-rational candidate is 7/9",
        best_rational.label == "7/9",
        f"best = {best_rational.label}",
    )
    check(
        "Best small-rational candidate keeps the full package within 1%",
        best_rational.refit_max < 1.0,
        f"max dev = {best_rational.refit_max:.3f}%",
    )
    check(
        "Best small-radical candidate is sqrt(3/5)",
        best_radical.label == "sqrt(3/5)",
        f"best = {best_radical.label}",
    )
    check(
        "Best small-radical candidate keeps the anchored CKM+J package within 1%",
        best_radical.anchor_max < 1.0,
        f"max dev = {best_radical.anchor_max:.3f}%",
    )
    return best_rational, best_radical


def part4_summary(
    solved_a_u: float,
    curated: list[CandidateEvaluation],
    best_rational: CandidateEvaluation,
    best_radical: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Summary")
    print("=" * 72)

    best_anchor = min(curated, key=lambda item: item.anchor_aggregate)
    best_native = min(
        (
            candidate for candidate in curated
            if candidate.label not in {"7/9", "sqrt(3/5)", "pi/4"}
        ),
        key=lambda item: item.anchor_aggregate,
    )

    print(f"\n  solved support-anchored a_u = {solved_a_u:.12f}")
    print()
    print("  strongest exact-candidate shortlist:")
    print(
        f"    - best small-rational refit candidate: {best_rational.label} = {best_rational.value:.12f}"
    )
    print(
        f"    - best small-radical anchored candidate: {best_radical.label} = {best_radical.value:.12f}"
    )
    print(
        f"    - best projector/support-native candidate: {best_native.label} = {best_native.value:.12f}"
    )
    print(
        f"    - best anchored observable package overall: {best_anchor.label} "
        f"(aggregate CKM+J dev = {best_anchor.anchor_aggregate:.3f}%)"
    )
    print()
    print("  honest endpoint:")
    print("    the remaining quark gap is no longer an unconstrained scalar.")
    print("    it is now a short bounded exact-candidate shortlist.")
    print("    none of those candidates is yet a retained derivation.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Up-Amplitude Exact-Candidate Scan")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = part1_reference()
    curated = part2_curated_scan(anchor_r_uc, anchor_r_ct)
    best_rational, best_radical = part3_grammar_scan(anchor_r_uc, anchor_r_ct)
    part4_summary(solved_a_u, curated, best_rational, best_radical)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
