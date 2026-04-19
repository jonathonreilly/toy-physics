#!/usr/bin/env python3
"""
Bounded denominator-side simplification of the exact counterexamples that beat
the direct sqrt(7) anchored law on the reduced quark up-amplitude lane.

Status:
  bounded denominator-counterexample simplification on the exact-support quark
  anchor

Safe claim:
  The direct support-affine anchored law

      a_u = sqrt(5/6) * (6/7 - delta_A1 / sqrt(7))

  is not the endpoint of the current exact search surface. In a bounded
  denominator-side grammar, there are many exact counterexamples with better
  anchored CKM+J score.

  This runner compresses that raw "many beaters" result to the smallest honest
  statement:
    - the simplest exact beater is the projector-rescaled denominator
      sqrt(42/5) = sqrt(7) / sqrt(5/6);
    - the strongest current bounded two-step beater is
      2 + sqrt(5/6);
    - the remaining beaters are higher-complexity variants inside the same
      narrow lifted-denominator window.

  That is a bounded counterexample classification, not a retained derivation.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from frontier_quark_up_amplitude_candidate_scan import (
    CandidateEvaluation,
    evaluate_candidate,
    exact_support_anchor,
)


PASS_COUNT = 0
FAIL_COUNT = 0

DELTA_A1 = 1.0 / 42.0
SUPPORT_BASE = 6.0 / 7.0
PROJECTOR_MAG = math.sqrt(5.0 / 6.0)
DIRECT_DENOM = math.sqrt(7.0)
PROJECTOR_RESCALED_DENOM = math.sqrt(42.0 / 5.0)
BEST_TWO_STEP_DENOM = 2.0 + PROJECTOR_MAG


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
class DenominatorExpression:
    formula: str
    value: float
    complexity: int
    family: str


@dataclass(frozen=True)
class DenominatorEvaluation:
    formula: str
    canonical_label: str
    value: float
    complexity: int
    family: str
    amplitude: float
    anchor_aggregate: float
    anchor_max: float
    refit_objective: float
    refit_max: float


def in_denominator_band(value: float) -> bool:
    return 0.0 < value < 10.0


def add_expression(
    expressions: dict[int, DenominatorExpression],
    formula: str,
    value: float,
    complexity: int,
    family: str,
) -> None:
    if not in_denominator_band(value):
        return
    key = round(value, 12)
    candidate = DenominatorExpression(formula, value, complexity, family)
    incumbent = expressions.get(key)
    if incumbent is None:
        expressions[key] = candidate
        return
    if complexity < incumbent.complexity or (
        complexity == incumbent.complexity and len(formula) < len(incumbent.formula)
    ):
        expressions[key] = candidate


def canonical_label(expression: DenominatorExpression) -> str:
    if abs(expression.value - DIRECT_DENOM) < 1.0e-12:
        return "sqrt(7)"
    if abs(expression.value - PROJECTOR_RESCALED_DENOM) < 1.0e-12:
        return "sqrt(42/5)"
    if abs(expression.value - BEST_TWO_STEP_DENOM) < 1.0e-12:
        return "2 + sqrt(5/6)"
    return expression.formula


def denominator_atoms() -> list[DenominatorExpression]:
    return [
        DenominatorExpression("sqrt(7)", DIRECT_DENOM, 1, "atom"),
        DenominatorExpression("sqrt(5/6)", PROJECTOR_MAG, 1, "atom"),
        DenominatorExpression("2", 2.0, 1, "atom"),
        DenominatorExpression("1", 1.0, 1, "atom"),
    ]


def build_denominator_grammar() -> list[DenominatorExpression]:
    atoms = denominator_atoms()
    expressions: dict[int, DenominatorExpression] = {}

    for atom in atoms:
        add_expression(
            expressions,
            atom.formula,
            atom.value,
            atom.complexity,
            atom.family,
        )

    one_step_inputs = list(expressions.values())
    for index, left in enumerate(one_step_inputs):
        for right in one_step_inputs[index:]:
            add_expression(
                expressions,
                f"({left.formula}+{right.formula})",
                left.value + right.value,
                left.complexity + right.complexity + 1,
                "one-step-sum",
            )
            add_expression(
                expressions,
                f"({left.formula}-{right.formula})",
                left.value - right.value,
                left.complexity + right.complexity + 1,
                "one-step-difference",
            )
            add_expression(
                expressions,
                f"({right.formula}-{left.formula})",
                right.value - left.value,
                left.complexity + right.complexity + 1,
                "one-step-difference",
            )
            add_expression(
                expressions,
                f"({left.formula}*{right.formula})",
                left.value * right.value,
                left.complexity + right.complexity + 1,
                "one-step-product",
            )
            if abs(right.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"({left.formula}/{right.formula})",
                    left.value / right.value,
                    left.complexity + right.complexity + 1,
                    "one-step-quotient",
                )
            if abs(left.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"({right.formula}/{left.formula})",
                    right.value / left.value,
                    left.complexity + right.complexity + 1,
                    "one-step-quotient",
                )
            product = left.value * right.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt(({left.formula})*({right.formula}))",
                    math.sqrt(product),
                    left.complexity + right.complexity + 2,
                    "one-step-sqrt-product",
                )

    one_step = list(expressions.values())
    for expression in one_step:
        add_expression(
            expressions,
            f"(1-({expression.formula}))",
            1.0 - expression.value,
            expression.complexity + 1,
            "two-step-complement",
        )
        for primitive in atoms:
            add_expression(
                expressions,
                f"(({expression.formula})+({primitive.formula}))",
                expression.value + primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-sum",
            )
            add_expression(
                expressions,
                f"(({expression.formula})-({primitive.formula}))",
                expression.value - primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-difference",
            )
            add_expression(
                expressions,
                f"(({primitive.formula})-({expression.formula}))",
                primitive.value - expression.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-difference",
            )
            add_expression(
                expressions,
                f"(({expression.formula})*({primitive.formula}))",
                expression.value * primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step-product",
            )
            if abs(primitive.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"(({expression.formula})/({primitive.formula}))",
                    expression.value / primitive.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step-quotient",
                )
            if abs(expression.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"(({primitive.formula})/({expression.formula}))",
                    primitive.value / expression.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step-quotient",
                )
            product = expression.value * primitive.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt((({expression.formula})*({primitive.formula})))",
                    math.sqrt(product),
                    expression.complexity + primitive.complexity + 2,
                    "two-step-sqrt-product",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.formula))


def amplitude_from_denominator(denominator: float) -> float:
    return PROJECTOR_MAG * (SUPPORT_BASE - DELTA_A1 / denominator)


def evaluate_denominator_expression(
    expression: DenominatorExpression,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> DenominatorEvaluation | None:
    amplitude = amplitude_from_denominator(expression.value)
    if not (0.3 < amplitude < 1.2):
        return None

    evaluation = evaluate_candidate(
        expression.formula,
        expression.family,
        amplitude,
        anchor_r_uc,
        anchor_r_ct,
    )
    return DenominatorEvaluation(
        formula=expression.formula,
        canonical_label=canonical_label(expression),
        value=expression.value,
        complexity=expression.complexity,
        family=expression.family,
        amplitude=amplitude,
        anchor_aggregate=float(evaluation.anchor_aggregate),
        anchor_max=float(evaluation.anchor_max),
        refit_objective=float(evaluation.refit_objective),
        refit_max=float(evaluation.refit_max),
    )


def part1_benchmark() -> tuple[float, float, DenominatorEvaluation]:
    print("\n" + "=" * 72)
    print("PART 1: Direct sqrt(7) Anchored Law")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    benchmark_expression = DenominatorExpression("sqrt(7)", DIRECT_DENOM, 1, "benchmark")
    benchmark = evaluate_denominator_expression(benchmark_expression, anchor_r_uc, anchor_r_ct)
    assert benchmark is not None

    print(f"\n  delta_A1(q_dem)              = {DELTA_A1:.12f}")
    print(f"  projector magnitude          = sqrt(5/6) = {PROJECTOR_MAG:.12f}")
    print(f"  solved anchored a_u          = {solved_a_u:.12f}")
    print(
        "  direct law                   = "
        "sqrt(5/6) * (6/7 - delta_A1/sqrt(7))"
    )
    print(f"  direct denominator D0        = sqrt(7)   = {DIRECT_DENOM:.12f}")
    print(f"  direct anchored amplitude    = {benchmark.amplitude:.12f}")
    print(f"  direct anchor aggregate      = {benchmark.anchor_aggregate:.6f}%")
    print(f"  direct anchor max            = {benchmark.anchor_max:.6f}%")
    print(f"  direct refit objective       = {benchmark.refit_objective:.6f}")
    print(f"  direct refit max             = {benchmark.refit_max:.6f}%")

    check(
        "Direct denominator reproduces the explicit sqrt(7) anchored law",
        abs(benchmark.value - DIRECT_DENOM) < 1.0e-12,
        f"D0 = {benchmark.value:.12f}",
    )
    return anchor_r_uc, anchor_r_ct, benchmark


def part2_scan(
    anchor_r_uc: float,
    anchor_r_ct: float,
    benchmark: DenominatorEvaluation,
) -> tuple[
    list[DenominatorEvaluation],
    DenominatorEvaluation,
    DenominatorEvaluation,
]:
    print("\n" + "=" * 72)
    print("PART 2: Bounded Denominator Counterexamples")
    print("=" * 72)

    expressions = build_denominator_grammar()
    evaluated = [
        evaluation
        for expression in expressions
        for evaluation in [evaluate_denominator_expression(expression, anchor_r_uc, anchor_r_ct)]
        if evaluation is not None
    ]
    beaters = [
        evaluation
        for evaluation in evaluated
        if evaluation.anchor_aggregate < benchmark.anchor_aggregate
    ]
    beaters.sort(
        key=lambda item: (
            item.anchor_aggregate,
            item.refit_objective,
            item.complexity,
            item.canonical_label,
        )
    )

    projector_rescaled = next(
        item for item in beaters if abs(item.value - PROJECTOR_RESCALED_DENOM) < 1.0e-12
    )
    best_two_step = beaters[0]

    complexity_counts = Counter(item.complexity for item in beaters)
    family_counts = Counter(item.family for item in beaters)

    print(f"\n  bounded denominator grammar size  = {len(expressions)}")
    print(f"  physical-band denominator count   = {len(evaluated)}")
    print(f"  beaters of direct sqrt(7) anchor  = {len(beaters)}")
    print(f"  complexity counts                 = {dict(sorted(complexity_counts.items()))}")
    print(f"  family counts                     = {dict(sorted(family_counts.items()))}")
    print(
        f"  beater denominator window         = [{min(item.value for item in beaters):.12f}, "
        f"{max(item.value for item in beaters):.12f}]"
    )

    print("\n  leading denominator beaters:")
    for item in beaters[:8]:
        print(
            f"  {item.canonical_label:38s} "
            f"D={item.value:.12f}  "
            f"a_u={item.amplitude:.12f}  "
            f"anchor={item.anchor_aggregate:.6f}%  "
            f"refit_obj={item.refit_objective:.6f}"
        )

    improvement_simple = benchmark.anchor_aggregate - projector_rescaled.anchor_aggregate
    improvement_best = benchmark.anchor_aggregate - best_two_step.anchor_aggregate

    check(
        "Every bounded denominator beater lifts the denominator above sqrt(7)",
        all(item.value > DIRECT_DENOM for item in beaters),
        f"min beater D = {min(item.value for item in beaters):.12f}",
    )
    check(
        "Only two minimal-complexity denominator beaters survive",
        complexity_counts[3] == 2,
        f"complexity-3 beaters = {complexity_counts[3]}",
    )
    check(
        "The simplest projector-rescaled beater is sqrt(42/5)",
        abs(projector_rescaled.value - PROJECTOR_RESCALED_DENOM) < 1.0e-12,
        f"D = {projector_rescaled.value:.12f}",
    )
    check(
        "The strongest bounded two-step denominator beater is 2 + sqrt(5/6)",
        abs(best_two_step.value - BEST_TWO_STEP_DENOM) < 1.0e-12,
        f"D = {best_two_step.value:.12f}",
    )
    check(
        "The projector-rescaled beater already captures more than 95% of the best anchored improvement",
        improvement_simple / improvement_best > 0.95,
        f"capture = {improvement_simple / improvement_best:.6f}",
    )
    check(
        "The strongest denominator beater still leaves the full package bounded",
        best_two_step.refit_max > 1.0,
        f"refit_max = {best_two_step.refit_max:.6f}%",
    )

    return beaters, projector_rescaled, best_two_step


def part3_summary(
    benchmark: DenominatorEvaluation,
    beaters: list[DenominatorEvaluation],
    projector_rescaled: DenominatorEvaluation,
    best_two_step: DenominatorEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Simplified Endpoint")
    print("=" * 72)

    print("\n  direct benchmark:")
    print(
        f"    - D0 = sqrt(7)               = {benchmark.value:.12f}\n"
        f"      anchor = {benchmark.anchor_aggregate:.6f}%\n"
        f"      a_u    = {benchmark.amplitude:.12f}"
    )
    print("\n  minimal representatives:")
    print(
        f"    - projector-rescaled beater  = sqrt(42/5) = sqrt(7)/sqrt(5/6)\n"
        f"      D = {projector_rescaled.value:.12f}\n"
        f"      anchor = {projector_rescaled.anchor_aggregate:.6f}%\n"
        f"      a_u    = {projector_rescaled.amplitude:.12f}"
    )
    print(
        f"    - strongest two-step beater  = 2 + sqrt(5/6)\n"
        f"      D = {best_two_step.value:.12f}\n"
        f"      anchor = {best_two_step.anchor_aggregate:.6f}%\n"
        f"      a_u    = {best_two_step.amplitude:.12f}"
    )
    print("\n  structural explanation:")
    print(
        "    every beater satisfies D > sqrt(7), so the correction term\n"
        "      delta_A1 / D\n"
        "    is smaller than in the direct law. That lifts a_u upward from the\n"
        "    direct sqrt(7) value and moves the anchored CKM+J package closer to\n"
        "    the exact-support anchor."
    )
    print(
        f"\n  bounded classification:\n"
        f"    - raw beaters in the bounded denominator grammar: {len(beaters)}\n"
        f"    - all beaters lie in a narrow lifted window above sqrt(7):\n"
        f"      {min(item.value for item in beaters):.12f} <= D <= {max(item.value for item in beaters):.12f}\n"
        f"    - no cleaner unique theorem-grade law emerges from this lane alone."
    )


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark sqrt(7) Counterexample Simplification")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, benchmark = part1_benchmark()
    beaters, projector_rescaled, best_two_step = part2_scan(
        anchor_r_uc,
        anchor_r_ct,
        benchmark,
    )
    part3_summary(benchmark, beaters, projector_rescaled, best_two_step)

    print("\n" + "=" * 72)
    print(f"FINAL STATUS: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
