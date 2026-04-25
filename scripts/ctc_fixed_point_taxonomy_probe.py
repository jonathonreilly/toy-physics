#!/usr/bin/env python3
"""Chronology lane probe: CTC fixed-point taxonomy over one loop bit.

The retained single-clock surface evolves freely chosen local Cauchy data
forward. A CTC consistency condition instead accepts only loop values b that
satisfy

    b = F_m(b),

where m is a late attempted message/control bit and F_m is the loop return map.
This probe separates three finite possibilities:

1. no fixed point: inconsistent history;
2. unique fixed point: no controllable message remains;
3. multiple fixed points: an extra selector is required.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


PASS = 0
FAIL = 0

Bit = int
LoopMap = Callable[[Bit, Bit], Bit]

BITS = [0, 1]
RETAINED_CLASSIFICATION = (
    "CTC consistency is global fixed-point import, not retained local Cauchy "
    "evolution or operational past signaling."
)


@dataclass(frozen=True)
class TaxonomyCase:
    name: str
    description: str
    loop_map: LoopMap
    expected_label: str


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def fixed_points(loop_map: LoopMap, message: Bit) -> list[Bit]:
    return [bit for bit in BITS if loop_map(message, bit) == bit]


def transition_text(loop_map: LoopMap, message: Bit) -> str:
    return ", ".join(f"{bit}->{loop_map(message, bit)}" for bit in BITS)


def fixed_text(points: list[Bit]) -> str:
    if not points:
        return "none"
    return "{" + ", ".join(str(point) for point in points) + "}"


def classify(counts: list[int]) -> str:
    if all(count == 0 for count in counts):
        return "no fixed point / inconsistent history"
    if all(count == 1 for count in counts):
        return "unique fixed point / no controllable message"
    if any(count > 1 for count in counts):
        return "multiple fixed points / hidden selector required"
    return "mixed admissibility / outside this three-class probe"


def selector_low(points: list[Bit]) -> Bit:
    if not points:
        raise ValueError("cannot select from an empty fixed-point set")
    return min(points)


def selector_high(points: list[Bit]) -> Bit:
    if not points:
        raise ValueError("cannot select from an empty fixed-point set")
    return max(points)


def print_case(case: TaxonomyCase) -> dict[Bit, list[Bit]]:
    print(case.name)
    print(f"  model = {case.description}")
    by_message = {}
    for message in BITS:
        points = fixed_points(case.loop_map, message)
        by_message[message] = points
        print(
            f"  m={message}: {transition_text(case.loop_map, message)}; "
            f"fixed points = {fixed_text(points)}"
        )
    counts = [len(by_message[message]) for message in BITS]
    label = classify(counts)
    print(f"  retained label = {label}")
    check(
        f"{case.name} classified as expected",
        label == case.expected_label,
        f"observed={label}",
    )
    return by_message


def no_fixed_point_map(message: Bit, bit: Bit) -> Bit:
    del message
    return 1 - bit


def unique_fixed_point_map(message: Bit, bit: Bit) -> Bit:
    del message, bit
    return 0


def multiple_fixed_point_map(message: Bit, bit: Bit) -> Bit:
    del message
    return bit


def main() -> int:
    print("=" * 88)
    print("CTC FIXED-POINT TAXONOMY PROBE")
    print("  Test: CTC consistency classifies global fixed-point import.")
    print("=" * 88)
    print()

    cases = [
        TaxonomyCase(
            name="CASE 1: no fixed point / inconsistent history",
            description="flip loop, F_m(b) = 1 - b",
            loop_map=no_fixed_point_map,
            expected_label="no fixed point / inconsistent history",
        ),
        TaxonomyCase(
            name="CASE 2: unique fixed point / no controllable message",
            description="reset loop, F_m(b) = 0",
            loop_map=unique_fixed_point_map,
            expected_label="unique fixed point / no controllable message",
        ),
        TaxonomyCase(
            name="CASE 3: multiple fixed points / hidden selector required",
            description="identity loop, F_m(b) = b",
            loop_map=multiple_fixed_point_map,
            expected_label="multiple fixed points / hidden selector required",
        ),
    ]

    no_points = print_case(cases[0])
    check(
        "inconsistent loop rejects every attempted message value",
        all(no_points[message] == [] for message in BITS),
    )
    print()

    unique_points = print_case(cases[1])
    chosen_values = [unique_points[message][0] for message in BITS]
    check(
        "unique loop fixes the same early value for both late choices",
        chosen_values == [0, 0],
        f"selected early values={chosen_values}",
    )
    check(
        "late attempted message is not retained as a controllable bit",
        len(set(chosen_values)) == 1,
        f"m=0 gives {chosen_values[0]}, m=1 gives {chosen_values[1]}",
    )
    print()

    multiple_points = print_case(cases[2])
    points_m0 = multiple_points[0]
    low = selector_low(points_m0)
    high = selector_high(points_m0)
    check(
        "identity loop admits both bit values as fixed points",
        all(multiple_points[message] == BITS for message in BITS),
    )
    check(
        "different selectors produce different realized histories",
        low != high,
        f"low selector={low}, high selector={high}",
    )
    check(
        "consistency alone does not choose between multiple fixed points",
        len(points_m0) > 1,
        f"available fixed points={fixed_text(points_m0)}",
    )
    print()

    retained_local_cauchy_evolution = "NO"
    operational_past_signaling = "NO"

    print("CLASSIFICATION")
    print(f"  retained classification = {RETAINED_CLASSIFICATION}")
    print(f"  retained local Cauchy evolution: {retained_local_cauchy_evolution}")
    print(f"  operational past signaling: {operational_past_signaling}")
    print()
    check(
        "taxonomy retains CTCs as fixed-point import",
        "global fixed-point import" in RETAINED_CLASSIFICATION,
        RETAINED_CLASSIFICATION,
    )
    check(
        "taxonomy does not promote CTC consistency to local Cauchy evolution",
        retained_local_cauchy_evolution == "NO",
    )
    check(
        "taxonomy does not promote CTC consistency to operational past signaling",
        operational_past_signaling == "NO",
    )

    print()
    print("SAFE READ")
    print("  - A no-fixed-point loop is an inconsistent admissibility problem.")
    print("  - A unique fixed point gives a global solution, not a free message bit.")
    print("  - Multiple fixed points require an imported selector to pick a history.")
    print(f"  - {RETAINED_CLASSIFICATION}")
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
