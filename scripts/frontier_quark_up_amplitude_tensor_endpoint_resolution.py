#!/usr/bin/env python3
"""
Tensor-endpoint resolution for the reduced up-sector quark amplitude.

Status:
  bounded derive-or-no-go resolution on the exact endpoint grammar

Safe claim:
  The current branch still does not derive a unique reduced up-sector
  amplitude law `a_u`.

  This runner resolves the next endpoint question left open by the
  tensor-endpoint bridge:

    can the bounded endpoint slope ratio `|b_E / b_T|` be promoted to the
    exact scalar-comparison denominator `sqrt(7)`, or does the current exact
    endpoint grammar stop one theorem short?

  Result on the live branch:
    - no exact identity `|b_E / b_T| = sqrt(7)` lands;
    - the exact scalar-comparison denominator `sqrt(7)` is present on the
      restricted endpoint grammar, but it is not forced by the endpoint data;
    - a controlled two-step exact endpoint grammar already produces other
      exact anchored denominators that outperform the `sqrt(7)` proxy;
    - so the honest endpoint is a bounded no-go:
      the exact endpoint gap `1/6` fixes the refit branch, the bounded slope
      ratio fixes the endpoint-data anchored branch, and current endpoint data
      do not force their unification.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from frontier_quark_up_amplitude_candidate_scan import (
    CandidateEvaluation,
    anchor_deviations,
    evaluate_candidate,
    exact_support_anchor,
)
from frontier_quark_up_amplitude_tensor_endpoint_bridge import (
    DELTA_A1,
    SIN_DELTA_STD,
    SQRT7,
    SUPPORT_FRACTION,
    TensorEndpointData,
    tensor_endpoint_data,
)


PASS_COUNT = 0
FAIL_COUNT = 0

RHO_SCALAR = 1.0 / math.sqrt(42.0)
GAP_ATOM = 1.0 / 6.0
R7_ATOM = 1.0 / math.sqrt(7.0)
KCP_ATOM = math.sqrt(6.0 / 7.0)
PMAG_ATOM = math.sqrt(5.0 / 6.0)
EXACT_TOL = 1.0e-12


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


def percent_gap(value: float, target: float) -> float:
    return abs(value / target - 1.0) * 100.0


def in_range(value: float) -> bool:
    return 0.0 < value < 20.0 and math.isfinite(value)


def anchored_a_u(denominator: float) -> float:
    return SIN_DELTA_STD * (SUPPORT_FRACTION - DELTA_A1 / denominator)


def canonical_denominator_label(denominator: float, raw_label: str) -> str:
    aliases = (
        ("6", 6.0),
        ("sqrt(42)", math.sqrt(42.0)),
        ("sqrt(7)", math.sqrt(7.0)),
        ("sqrt(7)-delta_A1", math.sqrt(7.0) - DELTA_A1),
        ("sqrt(7/6)", math.sqrt(7.0 / 6.0)),
        ("sqrt(42/5)", math.sqrt(42.0 / 5.0)),
        ("2+sqrt(5/6)", 2.0 + PMAG_ATOM),
    )
    for label, value in aliases:
        if abs(denominator - value) < EXACT_TOL:
            return label
    return raw_label


@dataclass(frozen=True)
class ExactAtom:
    label: str
    value: float
    complexity: int


@dataclass(frozen=True)
class DenominatorExpression:
    label: str
    value: float
    complexity: int
    stage: str


@dataclass(frozen=True)
class AnchorLaw:
    expression: DenominatorExpression
    pretty_label: str
    denominator: float
    a_u: float
    anchor_aggregate: float
    anchor_max: float


def build_endpoint_atoms() -> list[ExactAtom]:
    return [
        ExactAtom("delta_A1", DELTA_A1, 1),
        ExactAtom("6/7", SUPPORT_FRACTION, 1),
        ExactAtom("1/6", GAP_ATOM, 1),
        ExactAtom("1/sqrt(42)", RHO_SCALAR, 1),
        ExactAtom("1/sqrt(7)", R7_ATOM, 1),
        ExactAtom("sqrt(6/7)", KCP_ATOM, 1),
        ExactAtom("sqrt(5/6)", PMAG_ATOM, 1),
    ]


def positive_complements(expressions: list[ExactAtom | DenominatorExpression]) -> list[DenominatorExpression]:
    complements: list[DenominatorExpression] = []
    for expression in expressions:
        value = 1.0 - expression.value
        if in_range(value):
            complements.append(
                DenominatorExpression(
                    f"1-{expression.label}",
                    value,
                    expression.complexity + 1,
                    "complement",
                )
            )
    return complements


def add_expression(
    expressions: dict[int, DenominatorExpression],
    label: str,
    value: float,
    complexity: int,
    stage: str,
) -> None:
    if not in_range(value):
        return
    key = round(value, 12)
    candidate = DenominatorExpression(label, value, complexity, stage)
    incumbent = expressions.get(key)
    if incumbent is None:
        expressions[key] = candidate
        return
    if complexity < incumbent.complexity or (
        complexity == incumbent.complexity and len(label) < len(incumbent.label)
    ):
        expressions[key] = candidate


def render_term(expression: ExactAtom | DenominatorExpression) -> str:
    if expression.complexity <= 1:
        return expression.label
    return f"({expression.label})"


def build_one_step_denominators() -> list[DenominatorExpression]:
    atoms = build_endpoint_atoms()
    expressions: dict[int, DenominatorExpression] = {}

    for atom in atoms:
        add_expression(expressions, atom.label, atom.value, atom.complexity, "atom")

    for complement in positive_complements(atoms):
        add_expression(
            expressions,
            complement.label,
            complement.value,
            complement.complexity,
            "complement",
        )

    inputs = list(expressions.values())
    for index, left in enumerate(inputs):
        for right in inputs[index:]:
            left_label = render_term(left)
            right_label = render_term(right)
            add_expression(
                expressions,
                f"{left_label}+{right_label}",
                left.value + right.value,
                left.complexity + right.complexity + 1,
                "one-step",
            )
            add_expression(
                expressions,
                f"{left_label}-{right_label}",
                left.value - right.value,
                left.complexity + right.complexity + 1,
                "one-step",
            )
            add_expression(
                expressions,
                f"{right_label}-{left_label}",
                right.value - left.value,
                left.complexity + right.complexity + 1,
                "one-step",
            )
            add_expression(
                expressions,
                f"{left_label}*{right_label}",
                left.value * right.value,
                left.complexity + right.complexity + 1,
                "one-step",
            )
            if abs(right.value) > EXACT_TOL:
                add_expression(
                    expressions,
                    f"{left_label}/{right_label}",
                    left.value / right.value,
                    left.complexity + right.complexity + 1,
                    "one-step",
                )
            if abs(left.value) > EXACT_TOL:
                add_expression(
                    expressions,
                    f"{right_label}/{left_label}",
                    right.value / left.value,
                    left.complexity + right.complexity + 1,
                    "one-step",
                )
            product = left.value * right.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt({left_label}*{right_label})",
                    math.sqrt(product),
                    left.complexity + right.complexity + 2,
                    "one-step",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.label))


def build_two_step_denominators() -> list[DenominatorExpression]:
    one_step = build_one_step_denominators()
    primitives = [
        *build_endpoint_atoms(),
        *positive_complements(build_endpoint_atoms()),
    ]

    expressions: dict[int, DenominatorExpression] = {
        round(item.value, 12): item for item in one_step
    }
    for expression in one_step:
        complement = 1.0 - expression.value
        if in_range(complement):
            add_expression(
                expressions,
                f"1-({expression.label})",
                complement,
                expression.complexity + 1,
                "two-step",
            )

        for primitive in primitives:
            expression_label = render_term(expression)
            primitive_label = render_term(primitive)
            add_expression(
                expressions,
                f"{expression_label}+{primitive_label}",
                expression.value + primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step",
            )
            add_expression(
                expressions,
                f"{expression_label}-{primitive_label}",
                expression.value - primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step",
            )
            add_expression(
                expressions,
                f"{primitive_label}-{expression_label}",
                primitive.value - expression.value,
                expression.complexity + primitive.complexity + 1,
                "two-step",
            )
            add_expression(
                expressions,
                f"{expression_label}*{primitive_label}",
                expression.value * primitive.value,
                expression.complexity + primitive.complexity + 1,
                "two-step",
            )
            if abs(primitive.value) > EXACT_TOL:
                add_expression(
                    expressions,
                    f"{expression_label}/{primitive_label}",
                    expression.value / primitive.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step",
                )
            if abs(expression.value) > EXACT_TOL:
                add_expression(
                    expressions,
                    f"{primitive_label}/{expression_label}",
                    primitive.value / expression.value,
                    expression.complexity + primitive.complexity + 1,
                    "two-step",
                )
            product = expression.value * primitive.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt({expression_label}*{primitive_label})",
                    math.sqrt(product),
                    expression.complexity + primitive.complexity + 2,
                    "two-step",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.label))


def anchor_score(
    expression: DenominatorExpression,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> AnchorLaw | None:
    a_u = anchored_a_u(expression.value)
    if not (0.3 < a_u < 1.2):
        return None
    anchor_vus_dev, anchor_vcb_dev, anchor_vub_dev, anchor_j_dev = anchor_deviations(
        a_u,
        anchor_r_uc,
        anchor_r_ct,
    )
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
    return AnchorLaw(
        expression=expression,
        pretty_label=canonical_denominator_label(expression.value, expression.label),
        denominator=expression.value,
        a_u=a_u,
        anchor_aggregate=anchor_aggregate,
        anchor_max=anchor_max,
    )


def score_denominator_family(
    denominators: list[DenominatorExpression],
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> list[AnchorLaw]:
    scored: list[AnchorLaw] = []
    for expression in denominators:
        law = anchor_score(expression, anchor_r_uc, anchor_r_ct)
        if law is not None:
            scored.append(law)
    return scored


def keyed_evaluation(
    label: str,
    denominator: float,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> CandidateEvaluation:
    return evaluate_candidate(
        label,
        "endpoint-resolution",
        anchored_a_u(denominator),
        anchor_r_uc,
        anchor_r_ct,
    )


def print_direct_row(label: str, denominator: float, evaluation: CandidateEvaluation) -> None:
    print(
        f"  {label:14s} "
        f"d={denominator:.12f}  "
        f"a_u={evaluation.value:.9f}  "
        f"anchor={evaluation.anchor_aggregate:.3f}%  "
        f"refit_max={evaluation.refit_max:.3f}%"
    )


def print_anchor_row(law: AnchorLaw) -> None:
    print(
        f"  {law.pretty_label:24s} "
        f"d={law.denominator:.12f}  "
        f"a_u={law.a_u:.9f}  "
        f"anchor={law.anchor_aggregate:.3f}%  "
        f"amax={law.anchor_max:.3f}%"
    )


def part1_exact_algebra(
    data: TensorEndpointData,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> tuple[CandidateEvaluation, CandidateEvaluation, CandidateEvaluation]:
    print("\n" + "=" * 72)
    print("STAGE A: Exact Algebra Pass")
    print("=" * 72)

    direct_denominators = {
        "6": 1.0 / GAP_ATOM,
        "sqrt(42)": 1.0 / RHO_SCALAR,
        "sqrt(7)": 1.0 / R7_ATOM,
        "sqrt(7/6)": 1.0 / KCP_ATOM,
    }
    endpoint_ratios = {
        "|b_E/b_T|": data.slope_ratio,
        "|a_T/a_E|": data.shell_ratio,
        "|b_T/a_T|": data.t_balance,
    }

    print("\n  exact endpoint data:")
    print(f"    delta_A1(q_dem)   = {DELTA_A1:.12f}")
    print(f"    6/7               = {SUPPORT_FRACTION:.12f}")
    print(f"    1/6               = {GAP_ATOM:.12f}")
    print(f"    1/sqrt(42)        = {RHO_SCALAR:.12f}")
    print(f"    1/sqrt(7)         = {R7_ATOM:.12f}")
    print(f"    sqrt(6/7)         = {KCP_ATOM:.12f}")
    print(f"    sqrt(5/6)         = {PMAG_ATOM:.12f}")
    print()
    print("  endpoint readout ratios:")
    print(f"    |b_E/b_T|         = {data.slope_ratio:.12f}")
    print(f"    |a_T/a_E|         = {data.shell_ratio:.12f}")
    print(f"    |b_T/a_T|         = {data.t_balance:.12f}")

    gap_eval = keyed_evaluation("d=6", direct_denominators["6"], anchor_r_uc, anchor_r_ct)
    sqrt7_eval = keyed_evaluation("d=sqrt(7)", direct_denominators["sqrt(7)"], anchor_r_uc, anchor_r_ct)
    slope_eval = keyed_evaluation("d=k_tensor", data.slope_ratio, anchor_r_uc, anchor_r_ct)

    print("\n  direct anchored-law denominators:")
    for label, denominator in direct_denominators.items():
        direct_eval = keyed_evaluation(f"d={label}", denominator, anchor_r_uc, anchor_r_ct)
        print_direct_row(label, denominator, direct_eval)
    print_direct_row("|b_E/b_T|", data.slope_ratio, slope_eval)

    for ratio_label, ratio_value in endpoint_ratios.items():
        hits = [
            exact_label
            for exact_label, exact_value in direct_denominators.items()
            if abs(ratio_value - exact_value) < EXACT_TOL
        ]
        check(
            f"{ratio_label} has no exact direct-denominator hit",
            len(hits) == 0,
            f"hits = {hits or 'none'}",
        )

    check(
        "Exact endpoint gap remains 1/6",
        abs(data.endpoint_gap - GAP_ATOM) < EXACT_TOL,
        f"gap = {data.endpoint_gap:.12f}",
    )
    check(
        "The bounded slope ratio is not exactly sqrt(7)",
        abs(data.slope_ratio - direct_denominators["sqrt(7)"]) > EXACT_TOL,
        f"relative gap = {percent_gap(data.slope_ratio, direct_denominators['sqrt(7)']):.6f}%",
    )
    check(
        "The exact scalar denominator sqrt(7) still keeps the anchored package below 1%",
        sqrt7_eval.anchor_max < 1.0 and sqrt7_eval.anchor_aggregate < 1.0,
        f"anchor = {sqrt7_eval.anchor_aggregate:.3f}%, max = {sqrt7_eval.anchor_max:.3f}%",
    )

    return gap_eval, sqrt7_eval, slope_eval


def part2_restricted_grammar(
    data: TensorEndpointData,
    anchor_r_uc: float,
    anchor_r_ct: float,
    sqrt7_eval: CandidateEvaluation,
) -> tuple[DenominatorExpression, AnchorLaw, AnchorLaw, int]:
    print("\n" + "=" * 72)
    print("STAGE B: Restricted Endpoint Grammar")
    print("=" * 72)

    one_step = build_one_step_denominators()
    two_step = build_two_step_denominators()

    two_step_scored = score_denominator_family(two_step, anchor_r_uc, anchor_r_ct)

    nearest_slope = min(
        two_step,
        key=lambda expression: (
            abs(expression.value - data.slope_ratio),
            expression.complexity,
            expression.label,
        ),
    )
    exact_slope_hits = [
        expression
        for expression in two_step
        if abs(expression.value - data.slope_ratio) < EXACT_TOL
    ]
    two_step_best_anchor = min(
        two_step_scored,
        key=lambda law: (
            law.anchor_aggregate,
            law.anchor_max,
            law.expression.complexity,
            law.expression.label,
        ),
    )
    counterexample = next(
        law
        for law in two_step_scored
        if abs(law.denominator - math.sqrt(42.0 / 5.0)) < EXACT_TOL
    )
    beat_sqrt7 = [
        law
        for law in two_step_scored
        if law.anchor_aggregate < sqrt7_eval.anchor_aggregate - EXACT_TOL
    ]

    print(f"\n  one-step denominator grammar size = {len(one_step)}")
    print(f"  two-step denominator grammar size = {len(two_step)}")
    print()
    print(
        "  nearest exact-grammar denominator to |b_E/b_T|:"
        f" {canonical_denominator_label(nearest_slope.value, nearest_slope.label)}"
    )
    print(f"    denominator      = {nearest_slope.value:.12f}")
    print(f"    relative gap     = {percent_gap(nearest_slope.value, data.slope_ratio):.6f}%")
    print(f"    complexity       = {nearest_slope.complexity}")
    print()
    print("  explicit exact two-step counterexample to unique sqrt(7) selection:")
    print_anchor_row(counterexample)
    print()
    print("  best anchored two-step exact denominator:")
    print_anchor_row(two_step_best_anchor)
    print()
    print(
        "  exact two-step denominators beating the direct sqrt(7) law on anchored"
        f" aggregate = {len(beat_sqrt7)}"
    )

    check(
        "No restricted endpoint denominator lands exactly on |b_E/b_T|",
        len(exact_slope_hits) == 0,
        f"hits = {len(exact_slope_hits)}",
    )
    check(
        "Restricted endpoint grammar contains the exact counterexample sqrt(42/5)",
        abs(counterexample.denominator - math.sqrt(42.0 / 5.0)) < EXACT_TOL,
        f"counterexample = {counterexample.pretty_label}",
    )
    check(
        "Controlled two-step exact grammar produces denominators that beat sqrt(7)",
        len(beat_sqrt7) > 0,
        f"beaters = {len(beat_sqrt7)}",
    )
    check(
        "The explicit sqrt(42/5) counterexample already beats sqrt(7)",
        counterexample.anchor_aggregate < sqrt7_eval.anchor_aggregate - EXACT_TOL,
        (
            f"sqrt(42/5) anchor = {counterexample.anchor_aggregate:.3f}%, "
            f"sqrt(7) anchor = {sqrt7_eval.anchor_aggregate:.3f}%"
        ),
    )
    check(
        "Best two-step exact anchored denominator is not sqrt(7)",
        abs(two_step_best_anchor.denominator - SQRT7) > EXACT_TOL,
        f"best = {two_step_best_anchor.pretty_label}",
    )

    return nearest_slope, counterexample, two_step_best_anchor, len(beat_sqrt7)


def part3_endpoint_verdict(
    data: TensorEndpointData,
    gap_eval: CandidateEvaluation,
    sqrt7_eval: CandidateEvaluation,
    slope_eval: CandidateEvaluation,
    nearest_slope: DenominatorExpression,
    counterexample: AnchorLaw,
    two_step_best_anchor: AnchorLaw,
    beat_sqrt7_count: int,
    anchor_r_uc: float,
    anchor_r_ct: float,
) -> None:
    print("\n" + "=" * 72)
    print("STAGE C: Endpoint Verdict")
    print("=" * 72)

    nearest_eval = keyed_evaluation(
        f"d={canonical_denominator_label(nearest_slope.value, nearest_slope.label)}",
        nearest_slope.value,
        anchor_r_uc,
        anchor_r_ct,
    )
    counterexample_eval = keyed_evaluation(
        f"d={counterexample.pretty_label}",
        counterexample.denominator,
        anchor_r_uc,
        anchor_r_ct,
    )
    two_step_best_eval = keyed_evaluation(
        f"d={two_step_best_anchor.pretty_label}",
        two_step_best_anchor.denominator,
        anchor_r_uc,
        anchor_r_ct,
    )

    print("\n  exact refit branch from the support endpoint gap:")
    print_direct_row("d = 6", 6.0, gap_eval)
    print()
    print("  scalar-comparison anchored branch:")
    print_direct_row("d = sqrt(7)", SQRT7, sqrt7_eval)
    print()
    print("  bounded endpoint-data anchored branch:")
    print_direct_row("d = |b_E/b_T|", data.slope_ratio, slope_eval)
    print()
    print("  explicit exact counterexample to unique sqrt(7) selection:")
    print_direct_row(
        f"d = {counterexample.pretty_label}",
        counterexample.denominator,
        counterexample_eval,
    )
    print()
    print("  strongest controlled two-step exact anchored branch:")
    print_direct_row(
        f"d = {two_step_best_anchor.pretty_label}",
        two_step_best_anchor.denominator,
        two_step_best_eval,
    )
    print()
    print("  honest resolution:")
    print(
        "    exact endpoint data fix the refit branch through 1/6, "
        "but the anchored denominator does not collapse exactly to sqrt(7)."
    )
    print(
        "    the restricted exact endpoint grammar already contains sqrt(7), "
        f"yet it also contains {beat_sqrt7_count} exact two-step denominators with"
        " better anchored aggregate."
    )
    print(
        "    so current endpoint data stop at the split between the exact 1/6 refit branch "
        "and the bounded slope-ratio anchored branch."
    )

    check(
        "The exact endpoint-gap law still fixes the strongest current refit branch",
        gap_eval.refit_max < 1.0 and gap_eval.refit_objective < 0.053,
        f"refit max = {gap_eval.refit_max:.3f}%, refit obj = {gap_eval.refit_objective:.6f}",
    )
    check(
        "The bounded slope-ratio law still keeps the anchored package below 1%",
        slope_eval.anchor_max < 1.0 and slope_eval.anchor_aggregate < 1.0,
        f"anchor = {slope_eval.anchor_aggregate:.3f}%, max = {slope_eval.anchor_max:.3f}%",
    )
    check(
        "sqrt(7) is not uniquely selected by the restricted exact endpoint grammar",
        counterexample.anchor_aggregate < sqrt7_eval.anchor_aggregate - EXACT_TOL,
        (
            f"counterexample anchor = {counterexample.anchor_aggregate:.3f}%, "
            f"sqrt(7) anchor = {sqrt7_eval.anchor_aggregate:.3f}%"
        ),
    )
    check(
        "The nearest exact denominator to |b_E/b_T| still misses machine-precision identity",
        abs(nearest_slope.value - data.slope_ratio) > EXACT_TOL,
        f"relative gap = {percent_gap(nearest_slope.value, data.slope_ratio):.6f}%",
    )
    check(
        "The cycle resolves to the bounded no-go endpoint, not a positive sqrt(7) theorem",
        abs(data.slope_ratio - SQRT7) > EXACT_TOL and beat_sqrt7_count > 0,
        f"k_tensor gap = {percent_gap(data.slope_ratio, SQRT7):.6f}%, beaters = {beat_sqrt7_count}",
    )


def main() -> int:
    print("========================================================================")
    print("  FRONTIER: Quark Up-Amplitude Tensor-Endpoint Resolution")
    print("========================================================================")

    data = tensor_endpoint_data()
    anchor_r_uc, anchor_r_ct, _solved_a_u = exact_support_anchor()

    gap_eval, sqrt7_eval, slope_eval = part1_exact_algebra(
        data,
        anchor_r_uc,
        anchor_r_ct,
    )
    nearest_slope, counterexample, two_step_best_anchor, beat_sqrt7_count = part2_restricted_grammar(
        data,
        anchor_r_uc,
        anchor_r_ct,
        sqrt7_eval,
    )
    part3_endpoint_verdict(
        data,
        gap_eval,
        sqrt7_eval,
        slope_eval,
        nearest_slope,
        counterexample,
        two_step_best_anchor,
        beat_sqrt7_count,
        anchor_r_uc,
        anchor_r_ct,
    )

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
