#!/usr/bin/env python3
"""
Controlled two-step native-expression scan for the reduced up-sector quark
amplitude.

Status:
  bounded two-step native-grammar scan on the exact-support quark closure
  surface

Safe claim:
  The current branch still does not derive the remaining reduced up-sector
  amplitude `a_u`.

  This runner extends the earlier one-step native-expression scan by exactly
  one controlled operation:
    - start from a one-step native expression already built from the exact
      projector/support constants,
    - then apply one more arithmetic or sqrt-product operation against one
      native primitive or positive complement.

  Result:
    - a stronger native two-step refit law does appear;
    - a stronger native two-step anchored law does appear;
    - but they are not the same law, and no two-step native candidate beats
      both the `7/9` refit baseline and the `sqrt(3/5)` anchored baseline at
      once.

  So the split persists. This is a sharper bounded no-go, not a retained
  derivation.
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


def in_range(value: float) -> bool:
    return 0.3 < value < 1.2


@dataclass(frozen=True)
class NativeExpression:
    formula: str
    value: float
    complexity: int
    family: str


def native_atoms() -> list[NativeExpression]:
    return [
        NativeExpression("1/sqrt(42)", 1.0 / math.sqrt(42.0), 1, "atom"),
        NativeExpression("6/7", 6.0 / 7.0, 1, "atom"),
        NativeExpression("sqrt(5/6)", math.sqrt(5.0 / 6.0), 1, "atom"),
        NativeExpression("atan(sqrt(5))", math.atan(math.sqrt(5.0)), 1, "atom"),
        NativeExpression("sqrt(5)/6", math.sqrt(5.0) / 6.0, 1, "atom"),
        NativeExpression("sqrt(1/6)", math.sqrt(1.0 / 6.0), 1, "atom"),
    ]


def positive_complements(expressions: list[NativeExpression]) -> list[NativeExpression]:
    complements: list[NativeExpression] = []
    for expression in expressions:
        value = 1.0 - expression.value
        if 0.0 < value < 1.2:
            complements.append(
                NativeExpression(
                    f"(1 - {expression.formula})",
                    value,
                    expression.complexity + 1,
                    "complement",
                )
            )
    return complements


def add_expression(
    expressions: dict[int, NativeExpression],
    formula: str,
    value: float,
    complexity: int,
    family: str,
) -> None:
    if not in_range(value):
        return
    key = round(value, 12)
    candidate = NativeExpression(formula, value, complexity, family)
    incumbent = expressions.get(key)
    if incumbent is None:
        expressions[key] = candidate
        return
    if complexity < incumbent.complexity or (
        complexity == incumbent.complexity and len(formula) < len(incumbent.formula)
    ):
        expressions[key] = candidate


def build_one_step_grammar() -> list[NativeExpression]:
    atoms = native_atoms()
    expressions: dict[int, NativeExpression] = {}

    for atom in atoms:
        add_expression(
            expressions,
            atom.formula,
            atom.value,
            atom.complexity,
            atom.family,
        )

    for complement in positive_complements(atoms):
        add_expression(
            expressions,
            complement.formula,
            complement.value,
            complement.complexity,
            complement.family,
        )

    one_step_inputs = list(expressions.values())
    for index, left in enumerate(one_step_inputs):
        for right in one_step_inputs[index + 1 :]:
            add_expression(
                expressions,
                f"({left.formula} + {right.formula})",
                left.value + right.value,
                left.complexity + right.complexity + 1,
                "sum",
            )
            add_expression(
                expressions,
                f"({left.formula} - {right.formula})",
                left.value - right.value,
                left.complexity + right.complexity + 1,
                "difference",
            )
            add_expression(
                expressions,
                f"({right.formula} - {left.formula})",
                right.value - left.value,
                left.complexity + right.complexity + 1,
                "difference",
            )
            add_expression(
                expressions,
                f"({left.formula} * {right.formula})",
                left.value * right.value,
                left.complexity + right.complexity + 1,
                "product",
            )
            if abs(right.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"({left.formula} / {right.formula})",
                    left.value / right.value,
                    left.complexity + right.complexity + 1,
                    "quotient",
                )
            if abs(left.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"({right.formula} / {left.formula})",
                    right.value / left.value,
                    left.complexity + right.complexity + 1,
                    "quotient",
                )
            product = left.value * right.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt(({left.formula}) * ({right.formula}))",
                    math.sqrt(product),
                    left.complexity + right.complexity + 2,
                    "sqrt-product",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.formula))


def build_two_step_grammar() -> list[NativeExpression]:
    one_step = build_one_step_grammar()
    primitives = native_atoms() + positive_complements(native_atoms())
    expressions: dict[int, NativeExpression] = {}

    for expression in one_step:
        add_expression(
            expressions,
            expression.formula,
            expression.value,
            expression.complexity,
            "one-step",
        )

    for expression in one_step:
        add_expression(
            expressions,
            f"(1 - ({expression.formula}))",
            1.0 - expression.value,
            expression.complexity + 1,
            "two-step-complement",
        )
        for primitive in primitives:
            add_expression(
                expressions,
                f"(({expression.formula}) + ({primitive.formula}))",
                expression.value + primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-sum",
            )
            add_expression(
                expressions,
                f"(({expression.formula}) - ({primitive.formula}))",
                expression.value - primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-difference",
            )
            add_expression(
                expressions,
                f"(({primitive.formula}) - ({expression.formula}))",
                primitive.value - expression.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-difference",
            )
            add_expression(
                expressions,
                f"(({expression.formula}) * ({primitive.formula}))",
                expression.value * primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-product",
            )
            if abs(primitive.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"(({expression.formula}) / ({primitive.formula}))",
                    expression.value / primitive.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step-quotient",
                )
            if abs(expression.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"(({primitive.formula}) / ({expression.formula}))",
                    primitive.value / expression.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step-quotient",
                )
            product = expression.value * primitive.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt((({expression.formula}) * ({primitive.formula})))",
                    math.sqrt(product),
                    expression.complexity + primitive.complexity + 2,
                    "two-step-sqrt-product",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.formula))


def evaluate_two_step_grammar(
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> list[tuple[NativeExpression, CandidateEvaluation]]:
    return [
        (
            expression,
            evaluate_candidate(
                expression.formula,
                expression.family,
                expression.value,
                anchor_r_uc,
                anchor_r_ct,
            ),
        )
        for expression in build_two_step_grammar()
    ]


def print_candidate_row(expression: NativeExpression, evaluation: CandidateEvaluation) -> None:
    print(
        f"  {expression.formula:62s} "
        f"a_u={expression.value:.9f}  "
        f"c={expression.complexity}  "
        f"anchor={evaluation.anchor_aggregate:.3f}%  "
        f"refit_obj={evaluation.refit_objective:.6f}  "
        f"refit_max={evaluation.refit_max:.3f}%"
    )


def part1_two_step_scan() -> tuple[
    list[tuple[NativeExpression, CandidateEvaluation]],
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
]:
    print("\n" + "=" * 72)
    print("PART 1: Controlled Two-Step Native Grammar")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    one_step_count = len(build_one_step_grammar())
    evaluations = evaluate_two_step_grammar(anchor_r_uc, anchor_r_ct)

    print(f"\n  solved support-anchored a_u = {solved_a_u:.12f}")
    print(f"  one-step native candidates  = {one_step_count}")
    print(f"  two-step native candidates  = {len(evaluations)}")
    print("  added step                  = one more operation against one native primitive")

    by_refit = sorted(
        evaluations,
        key=lambda item: (
            item[1].refit_objective,
            item[1].anchor_aggregate,
            item[0].complexity,
            item[0].formula,
        ),
    )
    by_anchor = sorted(
        evaluations,
        key=lambda item: (
            item[1].anchor_aggregate,
            item[1].refit_objective,
            item[0].complexity,
            item[0].formula,
        ),
    )

    print("\n  strongest native two-step refit candidates:")
    for expression, evaluation in by_refit[:8]:
        print_candidate_row(expression, evaluation)

    print("\n  strongest native two-step anchored candidates:")
    for expression, evaluation in by_anchor[:8]:
        print_candidate_row(expression, evaluation)

    best_refit = by_refit[0][1]
    best_anchor = by_anchor[0][1]

    baseline_rational = evaluate_candidate(
        "7/9",
        "external",
        7.0 / 9.0,
        anchor_r_uc,
        anchor_r_ct,
    )
    baseline_radical = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchor_r_uc,
        anchor_r_ct,
    )
    one_step_refit = evaluate_candidate(
        "(atan(sqrt(5)) - sqrt(5)/6)",
        "one-step-baseline",
        math.atan(math.sqrt(5.0)) - math.sqrt(5.0) / 6.0,
        anchor_r_uc,
        anchor_r_ct,
    )
    one_step_anchor = evaluate_candidate(
        "(sqrt(5/6) * (1 - 1/sqrt(42)))",
        "one-step-baseline",
        math.sqrt(5.0 / 6.0) * (1.0 - 1.0 / math.sqrt(42.0)),
        anchor_r_uc,
        anchor_r_ct,
    )

    print("\n  one-step and external baselines:")
    print(
        f"    one-step best refit   : obj = {one_step_refit.refit_objective:.6f}, "
        f"anchor = {one_step_refit.anchor_aggregate:.3f}%"
    )
    print(
        f"    one-step best anchor  : anchor = {one_step_anchor.anchor_aggregate:.3f}%, "
        f"refit_max = {one_step_anchor.refit_max:.3f}%"
    )
    print(
        f"    7/9                   : obj = {baseline_rational.refit_objective:.6f}, "
        f"refit_max = {baseline_rational.refit_max:.3f}%"
    )
    print(
        f"    sqrt(3/5)             : anchor = {baseline_radical.anchor_aggregate:.3f}%, "
        f"anchor_max = {baseline_radical.anchor_max:.3f}%"
    )

    check(
        "Best native two-step refit law improves both the one-step refit law and the 7/9 baseline",
        best_refit.refit_objective < one_step_refit.refit_objective
        and best_refit.refit_objective < baseline_rational.refit_objective,
        f"best = {best_refit.refit_objective:.6f}",
    )
    check(
        "Best native two-step refit law keeps the full package within 1%",
        best_refit.refit_max < 1.0,
        f"max dev = {best_refit.refit_max:.3f}%",
    )
    check(
        "Best native two-step anchored law improves both the one-step anchored law and the sqrt(3/5) baseline",
        best_anchor.anchor_aggregate < one_step_anchor.anchor_aggregate
        and best_anchor.anchor_aggregate < baseline_radical.anchor_aggregate,
        f"best = {best_anchor.anchor_aggregate:.3f}%",
    )
    check(
        "Best native two-step anchored law keeps CKM+J deviations within 1%",
        best_anchor.anchor_max < 1.0,
        f"max dev = {best_anchor.anchor_max:.3f}%",
    )

    return (
        evaluations,
        best_refit,
        best_anchor,
        baseline_rational,
        baseline_radical,
        one_step_refit,
        one_step_anchor,
    )


def part2_persistence_no_go(
    evaluations: list[tuple[NativeExpression, CandidateEvaluation]],
    baseline_rational: CandidateEvaluation,
    baseline_radical: CandidateEvaluation,
    best_refit: CandidateEvaluation,
    best_anchor: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Persistence No-Go")
    print("=" * 72)

    dominates_both = [
        evaluation
        for _expression, evaluation in evaluations
        if evaluation.refit_objective < baseline_rational.refit_objective
        and evaluation.anchor_aggregate < baseline_radical.anchor_aggregate
    ]

    print(
        "\n  dominance test:"
        f" native two-step candidate with refit_obj < {baseline_rational.refit_objective:.6f}"
        f" and anchor < {baseline_radical.anchor_aggregate:.3f}%"
    )
    print(f"  surviving candidates = {len(dominates_both)}")
    print(f"  best refit formula   = {best_refit.label}")
    print(f"  best anchor formula  = {best_anchor.label}")

    check(
        "No native two-step expression beats both the 7/9 refit baseline and the sqrt(3/5) anchored baseline",
        len(dominates_both) == 0,
        "two-step native grammar still splits by axis",
    )


def part3_summary(
    best_refit: CandidateEvaluation,
    best_anchor: CandidateEvaluation,
    one_step_refit: CandidateEvaluation,
    one_step_anchor: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Summary")
    print("=" * 72)

    print("\n  strongest native two-step outcomes:")
    print(
        f"    - best native refit law     : {best_refit.label} = {best_refit.value:.12f}"
    )
    print(
        f"      refit_obj = {best_refit.refit_objective:.6f}, "
        f"refit_max = {best_refit.refit_max:.3f}%"
    )
    print(
        f"    - best native anchored law  : {best_anchor.label} = {best_anchor.value:.12f}"
    )
    print(
        f"      anchor = {best_anchor.anchor_aggregate:.3f}%, "
        f"anchor_max = {best_anchor.anchor_max:.3f}%"
    )
    print()
    print("  relation to the one-step native scan:")
    print(
        f"    - two-step refit improves {one_step_refit.refit_objective:.6f}"
        f" -> {best_refit.refit_objective:.6f}"
    )
    print(
        f"    - two-step anchor improves {one_step_anchor.anchor_aggregate:.3f}%"
        f" -> {best_anchor.anchor_aggregate:.3f}%"
    )
    print()
    print("  honest endpoint:")
    print("    one more semantically native step strengthens both axes,")
    print("    but it still does not collapse them to one dominant law.")
    print("    The reduced up-amplitude lane remains bounded.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Up-Amplitude Two-Step Native Scan")
    print("=" * 72)

    (
        evaluations,
        best_refit,
        best_anchor,
        baseline_rational,
        baseline_radical,
        one_step_refit,
        one_step_anchor,
    ) = part1_two_step_scan()
    part2_persistence_no_go(
        evaluations,
        baseline_rational,
        baseline_radical,
        best_refit,
        best_anchor,
    )
    part3_summary(best_refit, best_anchor, one_step_refit, one_step_anchor)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
