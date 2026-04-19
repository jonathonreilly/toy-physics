#!/usr/bin/env python3
"""
Restricted no-go for native affine support laws for the reduced up-sector
quark amplitude.

Status:
  bounded no-go on the widened native affine support family

Safe claim:
  The current branch still does not derive the remaining reduced up-sector
  amplitude `a_u`.

  This runner pushes one step past the earlier native one-step expression
  scan. It asks whether the exact support datum `delta_A1(q_dem) = 1/42`,
  together with the exact projector magnitude `sqrt(5/6)`, can close the
  remaining scalar on a widened affine support family

      a_u = sqrt(5/6) * (c0 + c1 delta_A1)

  when the coefficients `(c0, c1)` are drawn from a bounded one-step grammar
  on the native seven-site support constants already promoted in the repo.

  Result:
    - some native affine laws beat the `7/9` refit baseline,
    - different native affine laws beat the `sqrt(3/5)` anchored baseline,
    - but no native affine law beats both at once.

  This is a sharper bounded no-go, not a retained theorem.
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

DELTA_A1_EXACT = 1.0 / 42.0
PROJECTOR_MAG = math.sqrt(5.0 / 6.0)
RHO_SCALAR = 1.0 / math.sqrt(42.0)
SUPPORT_FRACTION = 6.0 / 7.0


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
class CoefficientExpression:
    label: str
    value: float
    complexity: int


@dataclass(frozen=True)
class AffineLaw:
    label: str
    value: float
    complexity: int
    intercept: str
    slope: str


def add_expression(
    expressions: dict[int, CoefficientExpression],
    label: str,
    value: float,
    complexity: int,
) -> None:
    if abs(value) > 20.0:
        return
    key = round(value, 12)
    candidate = CoefficientExpression(label, value, complexity)
    incumbent = expressions.get(key)
    if incumbent is None:
        expressions[key] = candidate
        return
    if complexity < incumbent.complexity or (
        complexity == incumbent.complexity and len(label) < len(incumbent.label)
    ):
        expressions[key] = candidate


def render_term(expression: CoefficientExpression) -> str:
    if expression.complexity <= 1:
        return expression.label
    return f"({expression.label})"


def build_support_coefficients() -> list[CoefficientExpression]:
    atoms = {
        "0": 0.0,
        "1": 1.0,
        "rho": RHO_SCALAR,
        "supp": SUPPORT_FRACTION,
        "1/6": 1.0 / 6.0,
        "1/7": 1.0 / 7.0,
        "6": 6.0,
        "7": 7.0,
    }

    expressions: dict[int, CoefficientExpression] = {}
    for label, value in atoms.items():
        add_expression(expressions, label, value, 1)
        add_expression(expressions, f"-{label}", -value, 2)
        add_expression(expressions, f"1-{label}", 1.0 - value, 2)

    one_step_inputs = list(expressions.values())
    for index, left in enumerate(one_step_inputs):
        for right in one_step_inputs[index:]:
            left_label = render_term(left)
            right_label = render_term(right)
            add_expression(
                expressions,
                f"{left_label}+{right_label}",
                left.value + right.value,
                left.complexity + right.complexity + 1,
            )
            add_expression(
                expressions,
                f"{left_label}-{right_label}",
                left.value - right.value,
                left.complexity + right.complexity + 1,
            )
            add_expression(
                expressions,
                f"{right_label}-{left_label}",
                right.value - left.value,
                left.complexity + right.complexity + 1,
            )
            add_expression(
                expressions,
                f"{left_label}*{right_label}",
                left.value * right.value,
                left.complexity + right.complexity + 1,
            )
            if abs(right.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"{left_label}/{right_label}",
                    left.value / right.value,
                    left.complexity + right.complexity + 1,
                )
            if abs(left.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"{right_label}/{left_label}",
                    right.value / left.value,
                    left.complexity + right.complexity + 1,
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.label))


def build_affine_laws(coefficients: list[CoefficientExpression]) -> list[AffineLaw]:
    laws: dict[int, AffineLaw] = {}
    for intercept in coefficients:
        for slope in coefficients:
            value = PROJECTOR_MAG * (intercept.value + slope.value * DELTA_A1_EXACT)
            if not (0.3 < value < 1.2):
                continue
            label = (
                "sqrt(5/6)"
                f"*({intercept.label} + ({slope.label}) delta_A1)"
            )
            law = AffineLaw(
                label=label,
                value=value,
                complexity=intercept.complexity + slope.complexity + 1,
                intercept=intercept.label,
                slope=slope.label,
            )
            key = round(value, 12)
            incumbent = laws.get(key)
            if incumbent is None:
                laws[key] = law
                continue
            if law.complexity < incumbent.complexity or (
                law.complexity == incumbent.complexity
                and len(law.label) < len(incumbent.label)
            ):
                laws[key] = law

    return sorted(laws.values(), key=lambda item: (item.complexity, item.label))


def print_row(law: AffineLaw, evaluation: CandidateEvaluation) -> None:
    print(
        f"  {law.label:52s} "
        f"a_u={law.value:.9f}  "
        f"anchor={evaluation.anchor_aggregate:.3f}%  "
        f"refit_obj={evaluation.refit_objective:.6f}"
    )


def part1_family() -> tuple[list[AffineLaw], CandidateEvaluation, CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("PART 1: Native Affine Support Family")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    coefficients = build_support_coefficients()
    laws = build_affine_laws(coefficients)

    baseline_refit = evaluate_candidate("7/9", "external", 7.0 / 9.0, anchor_r_uc, anchor_r_ct)
    baseline_anchor = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchor_r_uc,
        anchor_r_ct,
    )
    clean_structural = evaluate_candidate(
        "sqrt(5/6)*(6/7)",
        "native-affine-clean",
        PROJECTOR_MAG * SUPPORT_FRACTION,
        anchor_r_uc,
        anchor_r_ct,
    )

    print(f"\n  exact support datum        = delta_A1(q_dem) = {DELTA_A1_EXACT:.12f}")
    print(f"  exact projector magnitude  = sqrt(5/6)      = {PROJECTOR_MAG:.12f}")
    print(f"  solved support anchor a_u  = {solved_a_u:.12f}")
    print(f"  coefficient grammar size   = {len(coefficients)}")
    print(f"  affine-law family size     = {len(laws)}")
    print()
    print(
        "  family tested             = "
        "a_u = sqrt(5/6) * (c0 + c1 delta_A1)"
    )
    print(
        "  support coefficient atoms = "
        "{0, 1, rho, supp, 1/6, 1/7, 6, 7} with one-step +/-/*// widening"
    )
    print()
    print("  external baselines:")
    print(
        f"    7/9         : refit_obj = {baseline_refit.refit_objective:.6f}, "
        f"refit_max = {baseline_refit.refit_max:.3f}%"
    )
    print(
        f"    sqrt(3/5)   : anchor    = {baseline_anchor.anchor_aggregate:.3f}%, "
        f"anchor_max = {baseline_anchor.anchor_max:.3f}%"
    )
    print()
    print("  clean structural affine instance:")
    print(
        f"    sqrt(5/6) * (6/7) = {PROJECTOR_MAG * SUPPORT_FRACTION:.12f}  "
        f"(anchor = {clean_structural.anchor_aggregate:.3f}%, "
        f"refit_obj = {clean_structural.refit_objective:.6f})"
    )

    check(
        "Native affine family contains the clean support law sqrt(5/6) * (1 - 6 delta_A1)",
        any(abs(law.value - PROJECTOR_MAG * SUPPORT_FRACTION) < 1.0e-12 for law in laws),
        f"value = {PROJECTOR_MAG * SUPPORT_FRACTION:.12f}",
    )
    check(
        "Clean structural affine instance stays near quark closure",
        clean_structural.refit_max < 1.0 and clean_structural.anchor_max < 1.0,
        f"refit_max = {clean_structural.refit_max:.3f}%, anchor_max = {clean_structural.anchor_max:.3f}%",
    )

    return laws, baseline_refit, baseline_anchor


def part2_scan(
    laws: list[AffineLaw],
    baseline_refit: CandidateEvaluation,
    baseline_anchor: CandidateEvaluation,
) -> tuple[
    tuple[AffineLaw, CandidateEvaluation],
    tuple[AffineLaw, CandidateEvaluation],
    list[tuple[AffineLaw, CandidateEvaluation]],
    list[tuple[AffineLaw, CandidateEvaluation]],
    list[tuple[AffineLaw, CandidateEvaluation]],
]:
    print("\n" + "=" * 72)
    print("PART 2: Widened Native Affine Scan")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()

    evaluations = [
        (
            law,
            evaluate_candidate(
                law.label,
                "native-affine",
                law.value,
                anchor_r_uc,
                anchor_r_ct,
            ),
        )
        for law in sorted(
            laws,
            key=lambda item: (abs(item.value - solved_a_u), item.complexity, item.label),
        )
    ]

    best_refit = min(
        evaluations,
        key=lambda item: (
            item[1].refit_objective,
            item[1].anchor_aggregate,
            item[0].complexity,
            item[0].label,
        ),
    )
    best_anchor = min(
        evaluations,
        key=lambda item: (
            item[1].anchor_aggregate,
            item[1].refit_objective,
            item[0].complexity,
            item[0].label,
        ),
    )

    beat_refit = [
        item for item in evaluations if item[1].refit_objective < baseline_refit.refit_objective
    ]
    beat_anchor = [
        item for item in evaluations if item[1].anchor_aggregate < baseline_anchor.anchor_aggregate
    ]
    beat_both = [
        item
        for item in evaluations
        if item[1].refit_objective < baseline_refit.refit_objective
        and item[1].anchor_aggregate < baseline_anchor.anchor_aggregate
    ]

    print("\n  strongest native affine refit laws:")
    for law, evaluation in sorted(
        evaluations,
        key=lambda item: (
            item[1].refit_objective,
            item[1].anchor_aggregate,
            item[0].complexity,
            item[0].label,
        ),
    )[:6]:
        print_row(law, evaluation)

    print("\n  strongest native affine anchored laws:")
    for law, evaluation in sorted(
        evaluations,
        key=lambda item: (
            item[1].anchor_aggregate,
            item[1].refit_objective,
            item[0].complexity,
            item[0].label,
        ),
    )[:6]:
        print_row(law, evaluation)

    print("\n  dominance counts:")
    print(f"    beats 7/9 on refit axis      = {len(beat_refit)}")
    print(f"    beats sqrt(3/5) on anchor    = {len(beat_anchor)}")
    print(f"    beats both at once           = {len(beat_both)}")

    check(
        "Widened native affine family beats the 7/9 baseline somewhere on the refit axis",
        len(beat_refit) > 0,
        f"count = {len(beat_refit)}",
    )
    check(
        "Widened native affine family beats the sqrt(3/5) baseline somewhere on the anchored axis",
        len(beat_anchor) > 0,
        f"count = {len(beat_anchor)}",
    )
    check(
        "No native affine support law beats both the 7/9 refit baseline and the sqrt(3/5) anchored baseline",
        len(beat_both) == 0,
        "the affine family stays split across the two external baselines",
    )
    check(
        "Best native affine refit law keeps the full package within 1%",
        best_refit[1].refit_max < 1.0,
        f"max dev = {best_refit[1].refit_max:.3f}%",
    )
    check(
        "Best native affine anchored law keeps CKM+J deviations within 1%",
        best_anchor[1].anchor_max < 1.0,
        f"max dev = {best_anchor[1].anchor_max:.3f}%",
    )

    return best_refit, best_anchor, beat_refit, beat_anchor, beat_both


def part3_summary(
    best_refit: tuple[AffineLaw, CandidateEvaluation],
    best_anchor: tuple[AffineLaw, CandidateEvaluation],
    beat_refit: list[tuple[AffineLaw, CandidateEvaluation]],
    beat_anchor: list[tuple[AffineLaw, CandidateEvaluation]],
    beat_both: list[tuple[AffineLaw, CandidateEvaluation]],
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Summary")
    print("=" * 72)

    refit_law, refit_eval = best_refit
    anchor_law, anchor_eval = best_anchor

    print("\n  strongest widened affine outcomes:")
    print(f"    - best affine refit law    : {refit_law.label}")
    print(f"      a_u = {refit_law.value:.12f}")
    print(f"      refit_obj = {refit_eval.refit_objective:.6f}")
    print(f"      anchor    = {refit_eval.anchor_aggregate:.3f}%")
    print()
    print(f"    - best affine anchored law : {anchor_law.label}")
    print(f"      a_u = {anchor_law.value:.12f}")
    print(f"      anchor    = {anchor_eval.anchor_aggregate:.3f}%")
    print(f"      refit_obj = {anchor_eval.refit_objective:.6f}")
    print()
    print("  bounded no-go:")
    print(
        f"    - {len(beat_refit)} widened affine laws beat the 7/9 refit baseline"
    )
    print(
        f"    - {len(beat_anchor)} widened affine laws beat the sqrt(3/5) anchored baseline"
    )
    print(
        f"    - {len(beat_both)} widened affine laws beat both at once"
    )
    print()
    print("  honest endpoint:")
    print("    the exact projector magnitude plus affine delta_A1 support dressing")
    print("    is strong enough to compete with both external baselines separately,")
    print("    but not strong enough to force one dominant affine law.")
    print("    The reduced quark branch therefore remains bounded on this affine")
    print("    support family.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Up-Amplitude Native Affine No-Go")
    print("=" * 72)

    laws, baseline_refit, baseline_anchor = part1_family()
    best_refit, best_anchor, beat_refit, beat_anchor, beat_both = part2_scan(
        laws,
        baseline_refit,
        baseline_anchor,
    )
    part3_summary(best_refit, best_anchor, beat_refit, beat_anchor, beat_both)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
