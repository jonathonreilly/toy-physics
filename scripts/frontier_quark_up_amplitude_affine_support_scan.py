#!/usr/bin/env python3
"""
Bounded affine-support scan for the reduced up-sector quark amplitude.

Status:
  bounded affine-support law scan on the exact-support quark anchor

Safe claim:
  The current branch still does not derive the reduced up-sector amplitude
  `a_u`.

  This runner asks a narrower question:
    if one restricts to a bounded exact affine-support family centered on
    `a_u = sin(delta_std) * (c0 + c1 delta_A1)`,
    does one support-native law emerge that dominates the current shortlist?

  Result:
    - the strongest affine refit law is
      `sin(delta_std) * (6/7 - delta_A1/6)`;
    - the strongest affine anchored law is
      `sin(delta_std) * (6/7 - delta_A1/sqrt(7))`;
    - the cleanest exact support law remains
      `sin(delta_std) * (1 - 6 delta_A1) = sin(delta_std) * (6/7)`;
    - no bounded affine-support law beats both external baselines
      `7/9` and `sqrt(3/5)` at once.

  This is a bounded affine-support sharpening, not a retained derivation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from frontier_quark_up_amplitude_candidate_scan import (
    CandidateEvaluation,
    evaluate_candidate,
    exact_support_anchor,
)


PASS_COUNT = 0
FAIL_COUNT = 0

DELTA_A1 = 1.0 / 42.0
SIN_DELTA_STD = math.sqrt(5.0 / 6.0)

CORRECTION_TERMS: tuple[tuple[str, float, int], ...] = (
    ("delta_A1 / 7", 1.0 / 7.0, 1),
    ("delta_A1 / 6", 1.0 / 6.0, 1),
    ("delta_A1 / sqrt(42)", 1.0 / math.sqrt(42.0), 2),
    ("delta_A1 / sqrt(7)", 1.0 / math.sqrt(7.0), 2),
    ("delta_A1 / sqrt(6)", 1.0 / math.sqrt(6.0), 2),
    ("(6/7) delta_A1", 6.0 / 7.0, 1),
    ("delta_A1", 1.0, 1),
)


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
class AffineLaw:
    label: str
    value: float
    family: str
    complexity: int
    priority: int


def add_law(
    laws: dict[int, AffineLaw],
    label: str,
    value: float,
    family: str,
    complexity: int,
    priority: int,
) -> None:
    if not (0.3 < value < 1.2):
        return
    key = round(value, 12)
    candidate = AffineLaw(
        label=label,
        value=value,
        family=family,
        complexity=complexity,
        priority=priority,
    )
    incumbent = laws.get(key)
    if incumbent is None:
        laws[key] = candidate
        return
    incumbent_rank = (incumbent.priority + incumbent.complexity, len(incumbent.label))
    candidate_rank = (candidate.priority + candidate.complexity, len(candidate.label))
    if candidate_rank < incumbent_rank:
        laws[key] = candidate


def build_affine_laws() -> list[AffineLaw]:
    laws: dict[int, AffineLaw] = {}

    # Keep the two semantically canonical support-side laws explicit.
    add_law(
        laws,
        "sin(delta_std) * (1 - 6 delta_A1)",
        SIN_DELTA_STD * (1.0 - 6.0 * DELTA_A1),
        "canonical-support",
        2,
        0,
    )
    add_law(
        laws,
        "sin(delta_std) * (1 - sqrt(42) delta_A1)",
        SIN_DELTA_STD * (1.0 - math.sqrt(42.0) * DELTA_A1),
        "scalar-comparison",
        3,
        0,
    )

    base = 6.0 / 7.0
    for correction_label, correction_value, complexity in CORRECTION_TERMS:
        add_law(
            laws,
            f"sin(delta_std) * (6/7 - {correction_label})",
            SIN_DELTA_STD * (base - correction_value * DELTA_A1),
            "affine-support",
            complexity + 1,
            1,
        )
        add_law(
            laws,
            f"sin(delta_std) * (6/7 + {correction_label})",
            SIN_DELTA_STD * (base + correction_value * DELTA_A1),
            "affine-support",
            complexity + 1,
            1,
        )

    return sorted(laws.values(), key=lambda item: (item.complexity, item.label))


def evaluate_affine_laws(anchor_r_uc: float, anchor_r_ct: float) -> list[tuple[AffineLaw, CandidateEvaluation]]:
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
        for law in build_affine_laws()
    ]


def print_candidate_row(law: AffineLaw, evaluation: CandidateEvaluation) -> None:
    print(
        f"  {law.label:48s} "
        f"a_u={law.value:.9f}  "
        f"anchor={evaluation.anchor_aggregate:.3f}%  "
        f"refit_obj={evaluation.refit_objective:.6f}  "
        f"refit_max={evaluation.refit_max:.3f}%"
    )


def part1_reference() -> tuple[float, float, CandidateEvaluation, CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("PART 1: Exact-Support Anchor and External Baselines")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    baseline_rational = evaluate_candidate("7/9", "external", 7.0 / 9.0, anchor_r_uc, anchor_r_ct)
    baseline_radical = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchor_r_uc,
        anchor_r_ct,
    )

    print(f"\n  delta_A1(q_dem)                = {DELTA_A1:.12f}")
    print(f"  sin(delta_std)                 = {SIN_DELTA_STD:.12f}")
    print(f"  solved anchored a_u            = {solved_a_u:.12f}")
    print(f"  baseline 7/9 refit_obj         = {baseline_rational.refit_objective:.6f}")
    print(f"  baseline 7/9 refit_max         = {baseline_rational.refit_max:.3f}%")
    print(f"  baseline sqrt(3/5) anchor      = {baseline_radical.anchor_aggregate:.3f}%")
    print(f"  baseline sqrt(3/5) anchor_max  = {baseline_radical.anchor_max:.3f}%")

    return anchor_r_uc, anchor_r_ct, baseline_rational, baseline_radical


def part2_affine_scan(
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> tuple[
    list[tuple[AffineLaw, CandidateEvaluation]],
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
]:
    print("\n" + "=" * 72)
    print("PART 2: Bounded Affine-Support Laws")
    print("=" * 72)

    evaluations = evaluate_affine_laws(anchor_r_uc, anchor_r_ct)
    by_refit = sorted(
        evaluations,
        key=lambda item: (
            item[1].refit_objective,
            item[1].anchor_aggregate,
            item[0].complexity,
            item[0].label,
        ),
    )
    by_anchor = sorted(
        evaluations,
        key=lambda item: (
            item[1].anchor_aggregate,
            item[1].refit_objective,
            item[0].complexity,
            item[0].label,
        ),
    )

    print(
        "\n  bounded family:"
        " sin(delta_std) * (1 - 6 delta_A1),"
        " sin(delta_std) * (1 - sqrt(42) delta_A1),"
        " and sin(delta_std) * (6/7 +/- k delta_A1)"
    )

    print("\n  strongest affine-support refit laws:")
    for law, evaluation in by_refit[:8]:
        print_candidate_row(law, evaluation)

    print("\n  strongest affine-support anchored laws:")
    for law, evaluation in by_anchor[:8]:
        print_candidate_row(law, evaluation)

    best_refit = by_refit[0][1]
    best_anchor = by_anchor[0][1]
    canonical_support = next(
        evaluation
        for law, evaluation in evaluations
        if law.label == "sin(delta_std) * (1 - 6 delta_A1)"
    )
    scalar_variant = next(
        evaluation
        for law, evaluation in evaluations
        if law.label == "sin(delta_std) * (1 - sqrt(42) delta_A1)"
    )

    return evaluations, best_refit, best_anchor, canonical_support, scalar_variant


def part3_affine_endpoint(
    evaluations: list[tuple[AffineLaw, CandidateEvaluation]],
    best_refit: CandidateEvaluation,
    best_anchor: CandidateEvaluation,
    canonical_support: CandidateEvaluation,
    scalar_variant: CandidateEvaluation,
    baseline_rational: CandidateEvaluation,
    baseline_radical: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Affine Endpoint")
    print("=" * 72)

    print(f"\n  best affine refit law   = {best_refit.label}")
    print(f"    a_u                   = {best_refit.value:.12f}")
    print(f"    refit objective       = {best_refit.refit_objective:.6f}")
    print(f"    refit max deviation   = {best_refit.refit_max:.3f}%")
    print(f"    anchored aggregate    = {best_refit.anchor_aggregate:.3f}%")
    print()
    print(f"  best affine anchor law  = {best_anchor.label}")
    print(f"    a_u                   = {best_anchor.value:.12f}")
    print(f"    anchor aggregate      = {best_anchor.anchor_aggregate:.3f}%")
    print(f"    anchor max deviation  = {best_anchor.anchor_max:.3f}%")
    print(f"    refit max deviation   = {best_anchor.refit_max:.3f}%")
    print()
    print(f"  clean support law       = {canonical_support.label}")
    print(f"    refit objective       = {canonical_support.refit_objective:.6f}")
    print(f"    refit max deviation   = {canonical_support.refit_max:.3f}%")
    print(f"    anchor aggregate      = {canonical_support.anchor_aggregate:.3f}%")
    print()
    print(f"  scalar variant          = {scalar_variant.label}")
    print(f"    anchor aggregate      = {scalar_variant.anchor_aggregate:.3f}%")
    print(f"    anchor max deviation  = {scalar_variant.anchor_max:.3f}%")

    dominates_both = [
        evaluation
        for _law, evaluation in evaluations
        if evaluation.refit_objective < baseline_rational.refit_objective
        and evaluation.anchor_aggregate < baseline_radical.anchor_aggregate
    ]

    check(
        "Best affine refit law is sin(delta_std) * (6/7 - delta_A1/6)",
        best_refit.label == "sin(delta_std) * (6/7 - delta_A1 / 6)",
        f"best = {best_refit.label}",
    )
    check(
        "Best affine refit law keeps the full package within 1%",
        best_refit.refit_max < 1.0,
        f"max dev = {best_refit.refit_max:.3f}%",
    )
    check(
        "Best affine anchor law is sin(delta_std) * (6/7 - delta_A1/sqrt(7))",
        best_anchor.label == "sin(delta_std) * (6/7 - delta_A1 / sqrt(7))",
        f"best = {best_anchor.label}",
    )
    check(
        "Best affine anchor law keeps the anchored CKM+J package within 1%",
        best_anchor.anchor_max < 1.0,
        f"max dev = {best_anchor.anchor_max:.3f}%",
    )
    check(
        "Clean support law sin(delta_std) * (1 - 6 delta_A1) keeps the full refit package within 1%",
        canonical_support.refit_max < 1.0,
        f"max dev = {canonical_support.refit_max:.3f}%",
    )
    check(
        "Scalar-comparison affine variant stays within 1% on the anchored package",
        scalar_variant.anchor_max < 1.0,
        f"max dev = {scalar_variant.anchor_max:.3f}%",
    )
    check(
        "No bounded affine-support law beats both 7/9 and sqrt(3/5) at once",
        not dominates_both,
        f"survivors = {len(dominates_both)}",
    )


def main() -> None:
    anchor_r_uc, anchor_r_ct, baseline_rational, baseline_radical = part1_reference()
    evaluations, best_refit, best_anchor, canonical_support, scalar_variant = part2_affine_scan(
        anchor_r_uc,
        anchor_r_ct,
    )
    part3_affine_endpoint(
        evaluations,
        best_refit,
        best_anchor,
        canonical_support,
        scalar_variant,
        baseline_rational,
        baseline_radical,
    )

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)


if __name__ == "__main__":
    main()
