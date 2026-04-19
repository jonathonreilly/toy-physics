#!/usr/bin/env python3
"""
Restricted native-expression scan for the reduced up-sector quark amplitude.

Status:
  bounded one-step native-grammar scan on the projector/support closure surface

Safe claim:
  The current branch still does not derive the reduced up-sector amplitude
  `a_u`.

  This runner asks a narrower follow-on question:
    if one restricts to a one-step scalar grammar built directly from the exact
    quark projector/support constants already promoted in the repo, does one
    native expression emerge that dominates the current shortlist?

  Result:
    - the best native one-step refit candidate is
      `atan(sqrt(5)) - sqrt(5)/6`;
    - the best native one-step anchored candidate is
      `sqrt(5/6) * (1 - 1/sqrt(42))`;
    - no native one-step expression beats both the external `7/9` refit
      baseline and the external `sqrt(3/5)` anchored baseline at once.

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

PRETTY_LABELS = {
    "pphase-eta": "atan(sqrt(5)) - sqrt(5)/6",
    "1-rho*pmag": "sqrt(5/6) * (1 - 1/sqrt(42))",
    "pmag*1-rho": "sqrt(5/6) * (1 - 1/sqrt(42))",
    "supp*pmag": "sqrt(5/6) * (6/7)",
    "7/9": "7/9",
    "sqrt(3/5)": "sqrt(3/5)",
}


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


def pretty_label(label: str) -> str:
    return PRETTY_LABELS.get(label, label)


@dataclass(frozen=True)
class NativeExpression:
    label: str
    value: float
    complexity: int
    family: str


def add_expression(
    expressions: dict[int, NativeExpression],
    label: str,
    value: float,
    complexity: int,
    family: str,
) -> None:
    if not (0.3 < value < 1.2):
        return
    key = round(value, 12)
    candidate = NativeExpression(label, value, complexity, family)
    incumbent = expressions.get(key)
    if incumbent is None:
        expressions[key] = candidate
        return
    if complexity < incumbent.complexity or (
        complexity == incumbent.complexity and len(label) < len(incumbent.label)
    ):
        expressions[key] = candidate


def build_native_grammar() -> list[NativeExpression]:
    atoms = {
        "rho": 1.0 / math.sqrt(42.0),
        "supp": 6.0 / 7.0,
        "pmag": math.sqrt(5.0 / 6.0),
        "pphase": math.atan(math.sqrt(5.0)),
        "eta": math.sqrt(5.0) / 6.0,
        "pr": math.sqrt(1.0 / 6.0),
    }

    expressions: dict[int, NativeExpression] = {}
    for label, value in atoms.items():
        add_expression(expressions, label, value, 1, "atom")
        complement = 1.0 - value
        if 0.3 < complement < 1.2:
            add_expression(expressions, f"1-{label}", complement, 2, "complement")

    one_step_inputs = list(expressions.values())
    for index, left in enumerate(one_step_inputs):
        for right in one_step_inputs[index + 1 :]:
            add_expression(
                expressions,
                f"{left.label}+{right.label}",
                left.value + right.value,
                left.complexity + right.complexity + 1,
                "sum",
            )
            add_expression(
                expressions,
                f"{left.label}-{right.label}",
                left.value - right.value,
                left.complexity + right.complexity + 1,
                "difference",
            )
            add_expression(
                expressions,
                f"{right.label}-{left.label}",
                right.value - left.value,
                left.complexity + right.complexity + 1,
                "difference",
            )
            add_expression(
                expressions,
                f"{left.label}*{right.label}",
                left.value * right.value,
                left.complexity + right.complexity + 1,
                "product",
            )
            if abs(right.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"{left.label}/{right.label}",
                    left.value / right.value,
                    left.complexity + right.complexity + 1,
                    "quotient",
                )
            if abs(left.value) > 1.0e-12:
                add_expression(
                    expressions,
                    f"{right.label}/{left.label}",
                    right.value / left.value,
                    left.complexity + right.complexity + 1,
                    "quotient",
                )
            product = left.value * right.value
            if product > 0.0:
                add_expression(
                    expressions,
                    f"sqrt({left.label}*{right.label})",
                    math.sqrt(product),
                    left.complexity + right.complexity + 2,
                    "sqrt-product",
                )

    return sorted(expressions.values(), key=lambda item: (item.complexity, item.label))


def evaluate_native_grammar(anchor_r_uc: float, anchor_r_ct: float) -> list[tuple[NativeExpression, CandidateEvaluation]]:
    return [
        (
            expression,
            evaluate_candidate(
                expression.label,
                expression.family,
                expression.value,
                anchor_r_uc,
                anchor_r_ct,
            ),
        )
        for expression in build_native_grammar()
    ]


def part1_native_scan() -> tuple[
    list[tuple[NativeExpression, CandidateEvaluation]],
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
    CandidateEvaluation,
]:
    print("\n" + "=" * 72)
    print("PART 1: Restricted Native One-Step Grammar")
    print("=" * 72)

    anchor_r_uc, anchor_r_ct, solved_a_u = exact_support_anchor()
    print(f"\n  solved support-anchored a_u = {solved_a_u:.12f}")
    print("  native atoms               = {rho, supp, pmag, pphase, eta, pr}")
    print("  allowed one-step forms     = x, 1-x, x+y, x-y, x*y, x/y, sqrt(x*y)")

    evaluations = evaluate_native_grammar(anchor_r_uc, anchor_r_ct)
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

    print("\n  strongest native one-step refit candidates:")
    for expression, evaluation in by_refit[:8]:
        print(
            f"  {pretty_label(expression.label):28s} "
            f"a_u={expression.value:.9f}  "
            f"c={expression.complexity}  "
            f"anchor={evaluation.anchor_aggregate:.3f}%  "
            f"refit_obj={evaluation.refit_objective:.6f}  "
            f"refit_max={evaluation.refit_max:.3f}%"
        )

    print("\n  strongest native one-step anchored candidates:")
    for expression, evaluation in by_anchor[:8]:
        print(
            f"  {pretty_label(expression.label):28s} "
            f"a_u={expression.value:.9f}  "
            f"c={expression.complexity}  "
            f"anchor={evaluation.anchor_aggregate:.3f}%  "
            f"refit_obj={evaluation.refit_objective:.6f}  "
            f"refit_max={evaluation.refit_max:.3f}%"
        )

    best_refit = by_refit[0][1]
    best_anchor = by_anchor[0][1]

    baseline_rational = evaluate_candidate("7/9", "external", 7.0 / 9.0, anchor_r_uc, anchor_r_ct)
    baseline_radical = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchor_r_uc,
        anchor_r_ct,
    )

    print("\n  external shortlist baselines:")
    print(
        f"    7/9         : refit_obj = {baseline_rational.refit_objective:.6f}, "
        f"refit_max = {baseline_rational.refit_max:.3f}%"
    )
    print(
        f"    sqrt(3/5)   : anchor = {baseline_radical.anchor_aggregate:.3f}%, "
        f"anchor_max = {baseline_radical.anchor_max:.3f}%"
    )

    check(
        "Best native one-step refit candidate is atan(sqrt(5)) - sqrt(5)/6",
        best_refit.label == "pphase-eta",
        f"best = {pretty_label(best_refit.label)}",
    )
    check(
        "Best native one-step refit candidate keeps the full package within 1%",
        best_refit.refit_max < 1.0,
        f"max dev = {best_refit.refit_max:.3f}%",
    )
    check(
        "Best native one-step anchored candidate is sqrt(5/6) * (1 - 1/sqrt(42))",
        best_anchor.label in {"pmag*1-rho", "1-rho*pmag"},
        f"best = {pretty_label(best_anchor.label)}",
    )
    check(
        "Best native one-step anchored candidate keeps CKM+J deviations within 1%",
        best_anchor.anchor_max < 1.0,
        f"max dev = {best_anchor.anchor_max:.3f}%",
    )

    return evaluations, best_refit, best_anchor, baseline_rational, baseline_radical


def part2_restricted_no_go(
    evaluations: list[tuple[NativeExpression, CandidateEvaluation]],
    baseline_rational: CandidateEvaluation,
    baseline_radical: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Restricted No-Go")
    print("=" * 72)

    dominates_both = [
        evaluation
        for _expression, evaluation in evaluations
        if evaluation.refit_objective < baseline_rational.refit_objective
        and evaluation.anchor_aggregate < baseline_radical.anchor_aggregate
    ]

    print(
        "\n  dominance test:"
        f" native one-step candidate with refit_obj < {baseline_rational.refit_objective:.6f}"
        f" and anchor < {baseline_radical.anchor_aggregate:.3f}%"
    )
    print(f"  surviving candidates = {len(dominates_both)}")

    check(
        "No native one-step expression beats both the 7/9 refit baseline and the sqrt(3/5) anchored baseline",
        len(dominates_both) == 0,
        "restricted one-step native grammar remains split",
    )


def part3_summary(
    best_refit: CandidateEvaluation,
    best_anchor: CandidateEvaluation,
    baseline_rational: CandidateEvaluation,
    baseline_radical: CandidateEvaluation,
) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Summary")
    print("=" * 72)

    print("\n  strongest native one-step outcomes:")
    print(
        f"    - best native refit law     : {pretty_label(best_refit.label)} = {best_refit.value:.12f}"
    )
    print(
        f"    - best native anchored law  : {pretty_label(best_anchor.label)} = {best_anchor.value:.12f}"
    )
    print()
    print("  external bounded baselines still stronger on one axis each:")
    print(
        f"    - 7/9 keeps the strongest current refit score   ({baseline_rational.refit_objective:.6f})"
    )
    print(
        f"    - sqrt(3/5) keeps the strongest anchored score  ({baseline_radical.anchor_aggregate:.3f}%)"
    )
    print()
    print("  honest endpoint:")
    print("    the current exact projector/support constants do not yet force")
    print("    one dominant native one-step amplitude law.")
    print("    the native family still splits between a best refit law and a")
    print("    best anchored law, so the branch remains bounded.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Up-Amplitude Native-Expression Scan")
    print("=" * 72)

    evaluations, best_refit, best_anchor, baseline_rational, baseline_radical = part1_native_scan()
    part2_restricted_no_go(evaluations, baseline_rational, baseline_radical)
    part3_summary(best_refit, best_anchor, baseline_rational, baseline_radical)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
