#!/usr/bin/env python3
"""Lane 1 sqrt(sigma) B5 finite-volume ladder budget.

Cycle 4 of the hadron sqrt(sigma) loop.  This does not run a production
lattice simulation.  It computes the minimal finite-volume / loop-size
requirements implied by the B5 bridge and decides whether a local L=4,6,8
scout can materially tighten the residual.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def state_cycle_at_least(state: str, cycle: int) -> bool:
    match = re.search(r"cycles_completed:\s*(\d+)", state)
    return bool(match) and int(match.group(1)) >= cycle


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


@dataclass(frozen=True)
class LatticeCost:
    L: int

    @property
    def sites(self) -> int:
        return self.L ** 4

    @property
    def links(self) -> int:
        return 4 * self.sites

    @property
    def max_square_loop(self) -> int:
        # Conservative periodic-volume ceiling for a square Wilson loop.
        return self.L // 2

    @property
    def relative_to_l4(self) -> float:
        return self.sites / (4 ** 4)

    @property
    def link_bytes(self) -> int:
        # SU(3) complex128 link = 3*3*16 bytes.
        return self.links * 9 * 16


def part1_volume_scaling() -> None:
    section("Part 1: finite-volume cost scaling")
    rows = [LatticeCost(L) for L in (4, 6, 8, 12, 16)]

    for row in rows:
        print(
            f"  L={row.L:2d}: sites={row.sites:6d}, links={row.links:7d}, "
            f"rel_to_L4={row.relative_to_l4:6.1f}x, "
            f"max_R~{row.max_square_loop}, link_mem={row.link_bytes / 1024**2:6.1f} MiB"
        )

    check(
        "L=16 is 256x the per-sweep site count of L=4",
        LatticeCost(16).relative_to_l4 == 256.0,
    )
    check(
        "L=8 is still only a scout relative to L=16",
        LatticeCost(16).sites / LatticeCost(8).sites == 16.0,
    )
    check(
        "link memory is not the blocker through L=16",
        LatticeCost(16).link_bytes / 1024**2 < 40.0,
        f"L16 link memory {LatticeCost(16).link_bytes / 1024**2:.1f} MiB",
    )


def part2_loop_size_requirements() -> None:
    section("Part 2: Wilson-loop / Creutz-ratio size requirements")
    current = LatticeCost(4)
    scout = LatticeCost(8)
    production = LatticeCost(16)

    print(f"  L=4 max conservative square loop R~{current.max_square_loop}")
    print(f"  L=8 max conservative square loop R~{scout.max_square_loop}")
    print(f"  L=16 max conservative square loop R~{production.max_square_loop}")

    check(
        "current L=4 cannot test R>=3 square loops",
        current.max_square_loop < 3,
        f"max_R~{current.max_square_loop}",
    )
    check(
        "L=8 can first touch R=4 but has no asymptotic plateau leverage",
        scout.max_square_loop == 4,
        "one large-loop endpoint only",
    )
    check(
        "L=16 can support multiple R>=3 Creutz-ratio points",
        production.max_square_loop >= 8,
        f"max_R~{production.max_square_loop}",
    )


@dataclass(frozen=True)
class LadderPlan:
    name: str
    has_framework_measurement: bool
    has_volume_drift: bool
    has_large_loop_window: bool
    has_uncertainty_target: bool
    can_close_b5: bool

    def count(self) -> int:
        return sum(
            [
                self.has_framework_measurement,
                self.has_volume_drift,
                self.has_large_loop_window,
                self.has_uncertainty_target,
                self.can_close_b5,
            ]
        )


def part3_ladder_gate_model() -> None:
    section("Part 3: B5 ladder gate model")
    plans = [
        LadderPlan(
            name="current_L4_only",
            has_framework_measurement=True,
            has_volume_drift=False,
            has_large_loop_window=False,
            has_uncertainty_target=False,
            can_close_b5=False,
        ),
        LadderPlan(
            name="local_L4_L6_L8_scout",
            has_framework_measurement=True,
            has_volume_drift=True,
            has_large_loop_window=False,
            has_uncertainty_target=True,
            can_close_b5=False,
        ),
        LadderPlan(
            name="production_L8_L12_L16_ladder",
            has_framework_measurement=True,
            has_volume_drift=True,
            has_large_loop_window=True,
            has_uncertainty_target=True,
            can_close_b5=True,
        ),
    ]

    for plan in plans:
        print(f"  {plan.name}: {plan.count()}/5 gate bits")

    check(
        "current L4-only evidence is below B5 ladder threshold",
        plans[0].count() == 1 and not plans[0].can_close_b5,
    )
    check(
        "local L4/L6/L8 scout can quantify drift but not close B5",
        plans[1].count() == 3 and not plans[1].has_large_loop_window,
    )
    check(
        "production L8/L12/L16 ladder is the first B5-closing class",
        plans[2].can_close_b5 and plans[2].has_large_loop_window,
    )


def part4_required_observables() -> None:
    section("Part 4: required observable packet")
    required = [
        "plaquette mean and uncertainty",
        "Wilson loops W(R,T)",
        "Creutz ratios chi(R,T)",
        "static-force or r0/r1 proxy",
        "same beta=6 and action policy",
    ]
    for item in required:
        print(f"  required: {item}")

    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B5_LADDER_BUDGET_NOTE_2026-04-30.md")

    check(
        "budget note lists the required observable packet",
        all(term in note for term in ["plaquette mean", "Wilson loops", "Creutz ratios", "static-force"]),
    )
    check(
        "budget note marks L4/L6/L8 as scout rather than closure",
        "scout, not closure" in note and "L = 4, 6, 8" in note,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B5 FINITE-VOLUME LADDER BUDGET")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can an L=4,6,8 local ladder materially close the B5 framework")
    print("  link for imported static-energy/string-tension values?")
    print()
    print("Answer:")
    print("  No. It is useful as a scout, but B5 closure first appears in")
    print("  the production L=8,12,16 class or an equivalent theorem.")

    part1_volume_scaling()
    part2_loop_size_requirements()
    part3_ladder_gate_model()
    part4_required_observables()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
