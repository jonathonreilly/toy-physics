#!/usr/bin/env python3
"""
DM neutrino source-surface microscopic positive-probe representation theorem.

Question:
  Can the positive-probe candidate stack be compressed into one selector-class
  representation theorem before any more carrier archaeology?

Answer:
  Yes, conditionally on exact family-threshold semantics.

  On one common positive comparison window

      A_mu(H) = H + mu I > 0,

  exact family-threshold preservation forces scalarization through

      max_P W(A_mu(H); P),

  strict monotone threshold recalibration leaves only monotone
  reparameterization freedom, and the full canonical rank-one family collapses
  exactly to the soft-mode extremal score

      log(1 + 1 / lambda_min(A_mu(H))).

Boundary:
  This still does not prove observable-grammar exhaustion or exact-carrier
  completeness. Those remain the two live obstruction surfaces.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from dm_selector_branch_support import (
    ANCHOR_OFFSET,
    GENERIC_OFFSET,
    common_shift,
    positive_probe_family,
    random_unitary,
    recovered_bank,
    response_matrix,
    response_orders,
    response_via_rayleigh,
    spectral_projector_data,
    transformed_scores,
    universal_frontier_indices,
)
from frontier_dm_leptogenesis_ne_charged_source_response_reduction import source_response

PASS_COUNT = 0
FAIL_COUNT = 0

THRESHOLD_COUNT = 121
RANDOM_PROBE_COUNT = 16


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


def extremal_score_from_lambda_min(a: np.ndarray) -> float:
    evals = np.linalg.eigvalsh(np.asarray(a, dtype=complex))
    return math.log1p(1.0 / float(np.min(evals)))


def part1_exact_family_threshold_semantics_force_the_pointwise_max(
    hs: list[np.ndarray], repairs: np.ndarray, probes: list[tuple[str, np.ndarray]]
) -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT FAMILY THRESHOLD SEMANTICS FORCE THE POINTWISE MAX")
    print("=" * 88)

    mu = common_shift(repairs, ANCHOR_OFFSET)
    scores = response_matrix(hs, mu, probes)
    max_scores = np.max(scores, axis=1)
    mean_scores = np.mean(scores, axis=1)
    sum_scores = np.sum(scores, axis=1)

    tau_min = float(np.min(scores) - 1.0e-6)
    tau_max = float(np.max(sum_scores) + 1.0e-6)
    taus = np.linspace(tau_min, tau_max, THRESHOLD_COUNT)

    union_ok = True
    for tau in taus:
        union_event = np.any(scores >= tau, axis=1)
        max_event = max_scores >= tau
        union_ok &= bool(np.array_equal(union_event, max_event))

    idx_mean = int(np.argmax(max_scores - mean_scores))
    tau_mean = 0.5 * float(max_scores[idx_mean] + mean_scores[idx_mean])
    union_mean = bool(np.any(scores[idx_mean] >= tau_mean))
    mean_hits = bool(mean_scores[idx_mean] >= tau_mean)

    idx_sum = int(np.argmax(sum_scores - max_scores))
    tau_sum = 0.5 * float(sum_scores[idx_sum] + max_scores[idx_sum])
    union_sum = bool(np.any(scores[idx_sum] >= tau_sum))
    sum_hits = bool(sum_scores[idx_sum] >= tau_sum)

    check(
        "For every tested threshold the family witness event agrees exactly with the pointwise-maximum event",
        union_ok,
        f"(tau_min,tau_max,count)=({tau_min:.12f},{tau_max:.12f},{THRESHOLD_COUNT})",
    )
    check(
        "So any exact threshold-preserving family scalarization is forced pointwise to equal max_P w_P",
        union_ok,
        f"max scores={np.round(max_scores, 12)}",
    )
    check(
        "The arithmetic mean fails the exact family threshold semantics by losing genuine witnesses",
        union_mean and not mean_hits,
        f"(idx,tau,max,mean)=({idx_mean},{tau_mean:.12f},{max_scores[idx_mean]:.12f},{mean_scores[idx_mean]:.12f})",
    )
    check(
        "The sum also fails the exact family threshold semantics by creating spurious witnesses",
        (not union_sum) and sum_hits,
        f"(idx,tau,max,sum)=({idx_sum},{tau_sum:.12f},{max_scores[idx_sum]:.12f},{sum_scores[idx_sum]:.12f})",
    )

    print()
    print(f"  anchor mu   = {mu:.12f}")
    print(f"  max scores  = {np.round(max_scores, 12)}")


def part2_the_canonical_rank_one_family_collapses_to_the_soft_mode_extremal_score(
    hs: list[np.ndarray], repairs: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CANONICAL RANK-ONE FAMILY COLLAPSES TO THE SOFT-MODE EXTREMAL SCORE")
    print("=" * 88)

    h = np.asarray(hs[0], dtype=complex)
    mu = common_shift(repairs, GENERIC_OFFSET)
    a = h + mu * np.eye(3, dtype=complex)
    rng = np.random.default_rng(17)

    random_formula_ok = True
    max_formula_err = 0.0
    for _ in range(RANDOM_PROBE_COUNT):
        v = rng.normal(size=3) + 1j * rng.normal(size=3)
        direct = float(np.real(source_response(a, np.outer(v / np.linalg.norm(v), (v / np.linalg.norm(v)).conj()))))
        closed = response_via_rayleigh(a, v)
        err = abs(direct - closed)
        max_formula_err = max(max_formula_err, err)
        random_formula_ok &= err < 1.0e-12

    evals, spectral_responses, projectors = spectral_projector_data(a)
    soft_score = float(spectral_responses[0])
    exact_score = extremal_score_from_lambda_min(a)
    eigengap = float(evals[1] - evals[0])
    spectral_order = bool(np.argmax(spectral_responses) == 0 and np.all(np.diff(spectral_responses) < 0.0))

    u = random_unitary(np.random.default_rng(23))
    a_u = u @ a @ u.conj().T
    score_u = float(np.real(source_response(a_u, u @ projectors[0] @ u.conj().T)))

    check(
        "For every tested rank-one positive probe the exact source response matches the determinant-lemma / Rayleigh formula",
        random_formula_ok,
        f"max formula error={max_formula_err:.12e}",
    )
    check(
        "Within the canonical spectral family the soft projector is the unique maximizing probe on the sample window",
        spectral_order and eigengap > 1.0e-6,
        f"(evals,responses)=({np.round(evals, 12)},{np.round(spectral_responses, 12)})",
    )
    check(
        "The canonical extremal score is exactly log(1 + 1 / lambda_min(H + mu I))",
        abs(soft_score - exact_score) < 1.0e-12,
        f"|soft-exact|={abs(soft_score - exact_score):.12e}",
    )
    check(
        "That soft-mode extremal score is basis-free under simultaneous unitary conjugation",
        abs(score_u - soft_score) < 1.0e-12,
        f"|score_u-score|={abs(score_u - soft_score):.12e}",
    )

    print()
    print(f"  generic mu          = {mu:.12f}")
    print(f"  generic eigenvalues = {np.round(evals, 12)}")
    print(f"  spectral responses  = {np.round(spectral_responses, 12)}")


def part3_on_the_recovered_carrier_the_extremal_score_is_a_strict_monotone_of_least_repair(
    hs: list[np.ndarray], repairs: np.ndarray, probes: list[tuple[str, np.ndarray]]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THE RECOVERED CARRIER THE EXTREMAL SCORE IS A STRICT MONOTONE OF LEAST REPAIR")
    print("=" * 88)

    min_eigs = np.array([float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))) for h in hs], dtype=float)
    mu = common_shift(repairs, ANCHOR_OFFSET)
    exact_scores = np.array(
        [extremal_score_from_lambda_min(np.asarray(h, dtype=complex) + mu * np.eye(3, dtype=complex)) for h in hs],
        dtype=float,
    )
    repair_scores = np.array([math.log1p(1.0 / float(mu - repair)) for repair in repairs], dtype=float)

    frontier = universal_frontier_indices(hs, repairs, probes)
    repair_order = response_orders(repairs)
    score_order = response_orders(exact_scores)
    pref_idx = int(np.argmin(repairs))

    check(
        "Every recovered lift still has one negative soft mode, so lambda_min(H + mu I) = mu - Lambda_+(H) on the current bank",
        bool(np.all(min_eigs < -1.0e-6)),
        f"min eigs={np.round(min_eigs, 12)}",
    )
    check(
        "On the recovered bank the general soft-mode formula specializes exactly to log(1 + 1 / (mu - Lambda_+(H)))",
        float(np.max(np.abs(exact_scores - repair_scores))) < 1.0e-12,
        f"max score error={float(np.max(np.abs(exact_scores - repair_scores))):.12e}",
    )
    check(
        "The canonical extremal score has the same strict ordering on the recovered bank as least repair",
        score_order == repair_order,
        f"order={score_order}",
    )
    check(
        "The weaker finite-family Pareto rule leaves a two-point frontier, but the canonical extremal score already picks one preferred point on that frontier",
        frontier == [0, 1] and pref_idx == frontier[0] and exact_scores[frontier[0]] + 1.0e-6 < exact_scores[frontier[1]],
        f"(frontier,scores)=({frontier},{np.round(exact_scores[frontier], 12)})",
    )

    print()
    print(f"  recovered repairs = {np.round(repairs, 12)}")
    print(f"  recovered scores  = {np.round(exact_scores, 12)}")


def part4_after_monotone_recalibration_no_scalar_freedom_remains_on_the_recovered_bank(
    repairs: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: AFTER MONOTONE RECALIBRATION NO SCALAR FREEDOM REMAINS ON THE RECOVERED BANK")
    print("=" * 88)

    mu = common_shift(repairs, ANCHOR_OFFSET)
    base = np.array([math.log1p(1.0 / float(mu - repair)) for repair in repairs], dtype=float)
    laws = transformed_scores(base)
    ref_order = response_orders(base)
    ref_winner = int(np.argmin(base))
    ref_gap = float(np.partition(base, 1)[1] - np.min(base))

    order_ok = all(response_orders(vals) == ref_order for vals in laws.values())
    winner_ok = all(int(np.argmin(vals)) == ref_winner for vals in laws.values())
    gap_ok = all(float(np.partition(vals, 1)[1] - np.min(vals)) > 0.0 for vals in laws.values())

    check(
        "Every tested strictly increasing recalibration keeps the same recovered-bank ordering",
        order_ok,
        f"order={ref_order}",
    )
    check(
        "Every tested strictly increasing recalibration keeps the same unique preferred recovered winner",
        winner_ok and ref_winner == 0,
        f"(winner,gap)=({ref_winner},{ref_gap:.12e})",
    )
    check(
        "So after monotone threshold recalibration the recovered-bank selector class has no residual scalar freedom",
        gap_ok,
        f"laws={list(laws)}",
    )

    print()
    print(f"  recovered base scores = {np.round(base, 12)}")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE MICROSCOPIC POSITIVE-PROBE REPRESENTATION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the positive-probe candidate stack be compressed into one selector-class")
    print("  representation theorem before any more carrier archaeology?")

    _lifts, hs, repairs, _targets = recovered_bank()
    probes = positive_probe_family()

    part1_exact_family_threshold_semantics_force_the_pointwise_max(hs, repairs, probes)
    part2_the_canonical_rank_one_family_collapses_to_the_soft_mode_extremal_score(hs, repairs)
    part3_on_the_recovered_carrier_the_extremal_score_is_a_strict_monotone_of_least_repair(hs, repairs, probes)
    part4_after_monotone_recalibration_no_scalar_freedom_remains_on_the_recovered_bank(repairs)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Strongest honest selector-class statement now available:")
    print("    - exact family-threshold semantics force family scalarization through max_P w_P")
    print("    - monotone threshold recalibration leaves only strict monotone reparameterization freedom")
    print("    - the full canonical rank-one family collapses exactly to the soft-mode extremal score")
    print("    - on the current recovered carrier that score is exactly a strict monotone of Lambda_+")
    print("    - what remains open is observable-grammar exhaustion and exact-carrier completeness")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
