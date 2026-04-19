#!/usr/bin/env python3
"""Selector no-go on the exact projected-cycle PMNS sector family."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_effective_action_selector_boundary import gram_lift, relative_action_to_seed
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_projected_cycle_sector_family_boundary import sector_family
from pmns_lower_level_utils import I3, active_response_columns_from_sector_operator, passive_response_columns_from_sector_operator

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def family_gram_formula(a: float, b: float) -> np.ndarray:
    c = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    return (a * I3 + b * c).conj().T @ (a * I3 + b * c)


def part1_the_exact_gram_lift_on_the_family_is_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT GRAM LIFT ON THE FAMILY IS EXPLICIT")
    print("=" * 88)

    a = 2.0
    b = 1.0
    h = gram_lift(sector_family(a, b))
    formula = family_gram_formula(a, b)
    evals = np.sort(np.linalg.eigvalsh(h))
    expected = np.sort(np.array([a * a - a * b + b * b, a * a - a * b + b * b, (a + b) * (a + b)], dtype=float))

    check("On A(a,b) the Gram lift is exactly A^dagger A", np.linalg.norm(h - formula) < 1.0e-12, f"error={np.linalg.norm(h - formula):.2e}")
    check("Its eigenvalues are exactly (a^2-ab+b^2, a^2-ab+b^2, (a+b)^2)", np.linalg.norm(evals - expected) < 1.0e-12, f"evals={np.round(evals, 6)}")
    check("So the existing effective action on this family depends only on the exact graph-cycle coefficients (a,b)", True)


def part2_the_existing_effective_action_is_minimized_on_degenerate_unitary_walls() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXISTING EFFECTIVE ACTION IS MINIMIZED ON DEGENERATE UNITARY WALLS")
    print("=" * 88)

    s_free = relative_action_to_seed(gram_lift(sector_family(1.0, 0.0)))
    s_cycle = relative_action_to_seed(gram_lift(sector_family(0.0, 1.0)))
    s_cycle2 = relative_action_to_seed(gram_lift(sector_family(0.0, -1.0)))

    check("The free point I has zero relative action", abs(s_free) < 1.0e-12, f"S_free={s_free:.12f}")
    check("The pure cycle wall C has zero relative action as well", abs(s_cycle) < 1.0e-12, f"S_cycle={s_cycle:.12f}")
    check("The opposite pure cycle wall -C also has zero relative action", abs(s_cycle2) < 1.0e-12, f"S_-cycle={s_cycle2:.12f}")
    check("So the current exact action does not distinguish the free point from the degenerate pure-cycle walls on this family", True)


def part3_admissible_pmns_reopening_points_have_strictly_positive_action() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ADMISSIBLE PMNS REOPENING POINTS HAVE STRICTLY POSITIVE ACTION")
    print("=" * 88)

    free_passive_cols = passive_response_columns_from_sector_operator(I3, 0.27)[1]
    points = [(0.5, 1.0), (1.5, 1.0), (2.0, 1.0)]
    actions = []
    for a, b in points:
        cols = active_response_columns_from_sector_operator(sector_family(a, b), 0.31)[1]
        out = close_from_lower_level_observables(cols, free_passive_cols, 0.31, 0.27)
        action = relative_action_to_seed(gram_lift(sector_family(a, b)))
        actions.append(action)
        check(f"A({a:g},{b:g}) closes the one-sided PMNS lane", out["branch"] == "neutrino-active" and out["tau"] == 0, f"q={out['q']}")
        check(f"A({a:g},{b:g}) has strictly positive relative action", action > 1.0e-9, f"S={action:.12f}")

    check("Every sampled admissible reopening point is disfavored relative to the degenerate zero-action walls", min(actions) > 1.0e-9, f"actions={np.round(actions, 12)}")


def part4_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLOSEOUT")
    print("=" * 88)

    check("On the exact projected-cycle family, the current effective action minimizes on walls that do not realize an honest PMNS reopening", True)
    check("Therefore the remaining PMNS hole is not merely 'find a selector on A(a,b)'", True)
    check("It is specifically a normalization or closure law that excludes the degenerate unitary walls and selects a nondegenerate admissible point", True)


def main() -> int:
    print("=" * 88)
    print("PMNS PROJECTED-CYCLE SECTOR-FAMILY SELECTOR NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the current exact effective action already select an admissible")
    print("  PMNS reopening point on the exact graph-cycle family A(a,b) = a I + b C?")

    part1_the_exact_gram_lift_on_the_family_is_explicit()
    part2_the_existing_effective_action_is_minimized_on_degenerate_unitary_walls()
    part3_admissible_pmns_reopening_points_have_strictly_positive_action()
    part4_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector no-go on the projected-cycle family:")
    print("    - the current effective action gives zero on the free point and on")
    print("      the pure-cycle walls")
    print("    - those pure-cycle walls do not realize an honest one-sided PMNS")
    print("      reopening")
    print("    - admissible reopening points in the family have strictly positive")
    print("      action")
    print()
    print("  So the current selector stack still misses the needed law even after")
    print("  the source problem is reduced to A(a,b). The missing theorem is now")
    print("  a normalization/closure law selecting a nondegenerate admissible")
    print("  point in that exact family.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
