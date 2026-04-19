#!/usr/bin/env python3
"""
Bounded tensor-endpoint bridge for the reduced up-sector quark amplitude.

Status:
  bounded bridge from support-tensor endpoint data to the quark affine family

Safe claim:
  The current branch still does not derive a unique up-sector amplitude law
  `a_u`.

  But the quark affine family is now less arbitrary than the earlier scans
  made it look. The current support-tensor notes already supply two endpoint
  invariants that seed the two strongest support-native quark laws:

    1. the exact support-endpoint gap `Delta_endpoint = 1/6`, which generates
       the strongest affine refit law
       `sin(delta_std) * (6/7 - delta_A1 / 6)`;
    2. the bounded tensor slope ratio `k_tensor = |b_E / b_T|`, taken from the
       endpoint-fixed bilinear readout
       `gamma_E = a_E + b_E delta_A1`,
       `gamma_T = a_T + b_T delta_A1`,
       which generates an anchored law extremely close to the earlier
       `delta_A1 / sqrt(7)` branch.

  So the current tensor/support surface already organizes the split affine
  winners into an endpoint-derived pair. This is still bounded, not retained,
  because the tensor readout coefficients remain bounded and the two endpoint
  laws still split between refit and anchored quality.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import frontier_same_source_metric_ansatz_scan as same
import frontier_tensor_support_center_excess_law as center
from frontier_quark_up_amplitude_candidate_scan import (
    CandidateEvaluation,
    evaluate_candidate,
    exact_support_anchor,
)


PASS_COUNT = 0
FAIL_COUNT = 0

DELTA_A1 = 1.0 / 42.0
SIN_DELTA_STD = math.sqrt(5.0 / 6.0)
SUPPORT_FRACTION = 6.0 / 7.0
SQRT7 = math.sqrt(7.0)


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
class TensorEndpointData:
    delta_center: float
    delta_shell: float
    endpoint_gap: float
    gamma_e_center: float
    gamma_e_shell: float
    gamma_t_center: float
    gamma_t_shell: float
    intercept_e: float
    slope_e: float
    intercept_t: float
    slope_t: float
    slope_ratio: float
    shell_ratio: float
    t_balance: float


@dataclass(frozen=True)
class EndpointLaw:
    label: str
    family: str
    value: float


def tensor_endpoint_data() -> TensorEndpointData:
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / math.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (math.sqrt(3.0) * e1 + e2) / 2.0

    gamma_e_center, gamma_t_center = center.gamma_pair(e0, ex, t1x)
    gamma_e_shell, gamma_t_shell = center.gamma_pair(s_unit, ex, t1x)
    delta_center = center.support_delta(e0)
    delta_shell = center.support_delta(s_unit)
    endpoint_gap = delta_center - delta_shell

    slope_e = (gamma_e_center - gamma_e_shell) / endpoint_gap
    intercept_e = gamma_e_shell - slope_e * delta_shell
    slope_t = (gamma_t_center - gamma_t_shell) / endpoint_gap
    intercept_t = gamma_t_shell - slope_t * delta_shell

    return TensorEndpointData(
        delta_center=delta_center,
        delta_shell=delta_shell,
        endpoint_gap=endpoint_gap,
        gamma_e_center=gamma_e_center,
        gamma_e_shell=gamma_e_shell,
        gamma_t_center=gamma_t_center,
        gamma_t_shell=gamma_t_shell,
        intercept_e=intercept_e,
        slope_e=slope_e,
        intercept_t=intercept_t,
        slope_t=slope_t,
        slope_ratio=abs(slope_e / slope_t),
        shell_ratio=abs(intercept_t / intercept_e),
        t_balance=abs(slope_t / intercept_t),
    )


def build_endpoint_laws(data: TensorEndpointData) -> list[EndpointLaw]:
    return [
        EndpointLaw(
            "sin(delta_std) * (6/7 - delta_A1 * Delta_endpoint)",
            "tensor-endpoint",
            SIN_DELTA_STD * (SUPPORT_FRACTION - DELTA_A1 * data.endpoint_gap),
        ),
        EndpointLaw(
            "sin(delta_std) * (6/7 - delta_A1 / k_tensor)",
            "tensor-endpoint",
            SIN_DELTA_STD * (SUPPORT_FRACTION - DELTA_A1 / data.slope_ratio),
        ),
        EndpointLaw(
            "sin(delta_std) * (6/7 - delta_A1 / k_shell)",
            "tensor-endpoint",
            SIN_DELTA_STD * (SUPPORT_FRACTION - DELTA_A1 / data.shell_ratio),
        ),
        EndpointLaw(
            "sin(delta_std) * (6/7 - t_balance delta_A1)",
            "tensor-endpoint",
            SIN_DELTA_STD * (SUPPORT_FRACTION - data.t_balance * DELTA_A1),
        ),
        EndpointLaw(
            "sin(delta_std) * (1 - delta_A1 * Delta_endpoint)",
            "tensor-endpoint",
            SIN_DELTA_STD * (1.0 - DELTA_A1 * data.endpoint_gap),
        ),
        EndpointLaw(
            "sin(delta_std) * (1 - delta_A1 / k_tensor)",
            "tensor-endpoint",
            SIN_DELTA_STD * (1.0 - DELTA_A1 / data.slope_ratio),
        ),
    ]


def evaluate_endpoint_laws(
    data: TensorEndpointData,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> list[tuple[EndpointLaw, CandidateEvaluation]]:
    return [
        (
            law,
            evaluate_candidate(
                law.label,
                law.family,
                law.value,
                anchor_r_uc,
                anchor_r_ct,
            ),
        )
        for law in build_endpoint_laws(data)
    ]


def print_candidate_row(law: EndpointLaw, evaluation: CandidateEvaluation) -> None:
    print(
        f"  {law.label:52s} "
        f"a_u={law.value:.9f}  "
        f"anchor={evaluation.anchor_aggregate:.3f}%  "
        f"refit_obj={evaluation.refit_objective:.6f}  "
        f"refit_max={evaluation.refit_max:.3f}%"
    )


def part1_tensor_endpoint_data() -> tuple[TensorEndpointData, float, float, CandidateEvaluation, CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("PART 1: Tensor Endpoint Data and External Baselines")
    print("=" * 72)

    data = tensor_endpoint_data()
    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    baseline_refit = evaluate_candidate("7/9", "external", 7.0 / 9.0, anchor_r_uc, anchor_r_ct)
    baseline_anchor = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchor_r_uc,
        anchor_r_ct,
    )

    print(f"\n  exact support datum             = delta_A1(q_dem) = {DELTA_A1:.12f}")
    print(f"  exact support fraction          = 6/7            = {SUPPORT_FRACTION:.12f}")
    print(f"  solved anchored a_u             = {solved_a_u:.12f}")
    print()
    print(f"  delta_A1(e0)                    = {data.delta_center:.12f}")
    print(f"  delta_A1(s/sqrt(6))             = {data.delta_shell:.12f}")
    print(f"  exact endpoint gap              = {data.endpoint_gap:.12f}")
    print()
    print(f"  gamma_E(delta)                  = {data.intercept_e:+.12e} + ({data.slope_e:+.12e}) delta_A1")
    print(f"  gamma_T(delta)                  = {data.intercept_t:+.12e} + ({data.slope_t:+.12e}) delta_A1")
    print(f"  bounded slope ratio k_tensor    = |b_E / b_T|    = {data.slope_ratio:.12f}")
    print(f"  bounded shell ratio k_shell     = |a_T / a_E|    = {data.shell_ratio:.12f}")
    print(f"  bounded T-balance               = |b_T / a_T|    = {data.t_balance:.12f}")
    print()
    print(f"  baseline 7/9 refit_obj          = {baseline_refit.refit_objective:.6f}")
    print(f"  baseline 7/9 refit_max          = {baseline_refit.refit_max:.3f}%")
    print(f"  baseline sqrt(3/5) anchor       = {baseline_anchor.anchor_aggregate:.3f}%")
    print(f"  baseline sqrt(3/5) anchor_max   = {baseline_anchor.anchor_max:.3f}%")

    return data, anchor_r_uc, anchor_r_ct, baseline_refit, baseline_anchor


def part2_endpoint_bridge_family(
    data: TensorEndpointData,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> tuple[
    list[tuple[EndpointLaw, CandidateEvaluation]],
    CandidateEvaluation,
    CandidateEvaluation,
]:
    print("\n" + "=" * 72)
    print("PART 2: Tensor-Endpoint Bridge Family")
    print("=" * 72)

    evaluations = evaluate_endpoint_laws(data, anchor_r_uc, anchor_r_ct)
    by_refit = sorted(
        evaluations,
        key=lambda item: (
            item[1].refit_objective,
            item[1].anchor_aggregate,
            item[0].label,
        ),
    )
    by_anchor = sorted(
        evaluations,
        key=lambda item: (
            item[1].anchor_aggregate,
            item[1].refit_objective,
            item[0].label,
        ),
    )

    print("\n  endpoint-derived family:")
    print("    - exact endpoint gap Delta_endpoint = delta_A1(e0) - delta_A1(s/sqrt(6))")
    print("    - bounded readout ratios k_tensor = |b_E / b_T|, k_shell = |a_T / a_E|,")
    print("      and t_balance = |b_T / a_T|")

    print("\n  strongest endpoint-derived refit laws:")
    for law, evaluation in by_refit[:6]:
        print_candidate_row(law, evaluation)

    print("\n  strongest endpoint-derived anchored laws:")
    for law, evaluation in by_anchor[:6]:
        print_candidate_row(law, evaluation)

    best_refit = by_refit[0][1]
    best_anchor = by_anchor[0][1]
    return evaluations, best_refit, best_anchor


def part3_bridge_endpoint(
    data: TensorEndpointData,
    evaluations: list[tuple[EndpointLaw, CandidateEvaluation]],
    baseline_refit: CandidateEvaluation,
    baseline_anchor: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Bridge Endpoint")
    print("=" * 72)

    gap_law, gap_eval = next(
        (law, evaluation)
        for law, evaluation in evaluations
        if law.label == "sin(delta_std) * (6/7 - delta_A1 * Delta_endpoint)"
    )
    slope_law, slope_eval = next(
        (law, evaluation)
        for law, evaluation in evaluations
        if law.label == "sin(delta_std) * (6/7 - delta_A1 / k_tensor)"
    )

    sqrt7_proxy = SIN_DELTA_STD * (SUPPORT_FRACTION - DELTA_A1 / SQRT7)
    sqrt7_proxy_gap = abs(slope_law.value / sqrt7_proxy - 1.0) * 100.0

    print(f"\n  exact endpoint-gap law          = {gap_law.label}")
    print(f"    a_u                           = {gap_law.value:.12f}")
    print(f"    refit objective               = {gap_eval.refit_objective:.6f}")
    print(f"    refit max deviation           = {gap_eval.refit_max:.3f}%")
    print(f"    anchored aggregate            = {gap_eval.anchor_aggregate:.3f}%")
    print()
    print(f"  bounded tensor-ratio law        = {slope_law.label}")
    print(f"    a_u                           = {slope_law.value:.12f}")
    print(f"    anchored aggregate            = {slope_eval.anchor_aggregate:.3f}%")
    print(f"    anchored max deviation        = {slope_eval.anchor_max:.3f}%")
    print(f"    refit max deviation           = {slope_eval.refit_max:.3f}%")
    print(f"    sqrt(7) proxy gap             = {sqrt7_proxy_gap:.3f}%")
    print()
    print(f"  external refit baseline 7/9     = {baseline_refit.refit_max:.3f}% max")
    print(f"  external anchored sqrt(3/5)     = {baseline_anchor.anchor_aggregate:.3f}% aggregate")

    survivors = [
        law.label
        for law, evaluation in evaluations
        if evaluation.refit_objective < baseline_refit.refit_objective
        and evaluation.anchor_aggregate < baseline_anchor.anchor_aggregate
    ]

    check(
        "The exact support endpoint gap is 1/6",
        abs(data.endpoint_gap - 1.0 / 6.0) < 1.0e-12,
        f"gap = {data.endpoint_gap:.12f}",
    )
    check(
        "The bounded tensor slope ratio stays within 1% of sqrt(7)",
        abs(data.slope_ratio / SQRT7 - 1.0) < 0.01,
        f"k_tensor/sqrt(7) = {data.slope_ratio / SQRT7:.6f}",
    )
    check(
        "The exact endpoint-gap law reproduces the strongest current affine refit branch",
        gap_eval.refit_max < 1.0 and gap_eval.refit_objective < 0.053,
        f"refit max = {gap_eval.refit_max:.3f}%, refit obj = {gap_eval.refit_objective:.6f}",
    )
    check(
        "The bounded tensor-ratio law keeps the anchored CKM+J package below 1%",
        slope_eval.anchor_max < 1.0 and slope_eval.anchor_aggregate < 1.0,
        f"anchor max = {slope_eval.anchor_max:.3f}%, aggregate = {slope_eval.anchor_aggregate:.3f}%",
    )
    check(
        "The bounded tensor-ratio law lands within 0.2% of the earlier sqrt(7) proxy value",
        sqrt7_proxy_gap < 0.2,
        f"value gap = {sqrt7_proxy_gap:.3f}%",
    )
    check(
        "No tensor-endpoint bridge law beats both external baselines at once",
        len(survivors) == 0,
        f"survivors = {len(survivors)}",
    )


def main() -> int:
    print("========================================================================")
    print("  FRONTIER: Quark Up-Amplitude Tensor-Endpoint Bridge")
    print("========================================================================")

    data, anchor_r_uc, anchor_r_ct, baseline_refit, baseline_anchor = part1_tensor_endpoint_data()
    evaluations, _best_refit, _best_anchor = part2_endpoint_bridge_family(
        data,
        anchor_r_uc,
        anchor_r_ct,
    )
    part3_bridge_endpoint(data, evaluations, baseline_refit, baseline_anchor)

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
