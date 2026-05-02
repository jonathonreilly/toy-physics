#!/usr/bin/env python3
"""Conclusion-boundary check for native taste-qubit teleportation.

This runner is intentionally conservative. It asks whether the current lane can
be closed unconditionally from in-repo evidence, or whether it must stop at a
retained planning boundary with explicit external/theorem obligations.

The current answer is a controlled HOLD:

* the selector problem has a minimal three-clause completion, but the bare
  one-axiom derivation is closed negatively on audited invariants;
* the signed sparse branch has a side 4..12 certificate and a precise induction
  target, but no all-even-side proof;
* pulse/detector thresholds have controller/material requirement envelopes, but
  no fabricated device, named material stack, or measured spectrum.

The claim boundary remains ordinary quantum state teleportation only. No matter,
mass, charge, energy, object, or faster-than-light transport is claimed.
"""

from __future__ import annotations

import argparse
import dataclasses
import math


@dataclasses.dataclass(frozen=True)
class SelectorConclusion:
    residual_without_orientation: int
    residual_without_action: int
    residual_without_no_dwell: int
    final_selector_count: int
    bare_derivation_status: str
    terminal_decision: str


@dataclasses.dataclass(frozen=True)
class ScalingConclusion:
    certified_sides: tuple[int, ...]
    gap_floor: float
    bell_floor: float
    min_margin: float
    direct_solve_frontier: int
    next_side_status: str
    terminal_decision: str


@dataclasses.dataclass(frozen=True)
class HardwareConclusion:
    slot_threshold: float
    area_budget_rad: float
    controller_margin: float
    detector_word_bound: float
    detector_log10_overlap: float
    evidence_status: str
    terminal_decision: str


@dataclasses.dataclass(frozen=True)
class LaneConclusion:
    planning_closed: bool
    unconditional_closed: bool
    promote_to_nature_grade: bool
    retained_status: str


def selector_conclusion() -> SelectorConclusion:
    return SelectorConclusion(
        residual_without_orientation=2,
        residual_without_action=8,
        residual_without_no_dwell=4,
        final_selector_count=1,
        bare_derivation_status="negative on audited invariants",
        terminal_decision=(
            "retain the three-clause completion as an added lane principle, "
            "derive it from a stronger theorem, or do not promote"
        ),
    )


def scaling_conclusion(gap_floor: float, bell_floor: float) -> ScalingConclusion:
    rows = (
        (4, 0.0244025),
        (6, 0.0120618),
        (8, 0.00704654),
        (10, 0.00459031),
        (12, 0.00321872568895),
    )
    margins = [gap - gap_floor / (side * side) for side, gap in rows]
    return ScalingConclusion(
        certified_sides=tuple(side for side, _gap in rows),
        gap_floor=gap_floor,
        bell_floor=bell_floor,
        min_margin=min(margins),
        direct_solve_frontier=12,
        next_side_status="side 14 direct sparse solve exceeded local turn budget",
        terminal_decision=(
            "prove the all-even-side induction/operator inequality or keep "
            "resource genesis at finite-certificate status"
        ),
    )


def hardware_conclusion() -> HardwareConclusion:
    return HardwareConclusion(
        slot_threshold=2.622e-3,
        area_budget_rad=0.050937,
        controller_margin=2.215,
        detector_word_bound=7.498e-131,
        detector_log10_overlap=-655.141,
        evidence_status="threshold requirements only; no measured device/material data",
        terminal_decision=(
            "supply fabricated/noise/material evidence or keep hardware closure "
            "as a requirement envelope"
        ),
    )


def lane_conclusion(
    selector: SelectorConclusion,
    scaling: ScalingConclusion,
    hardware: HardwareConclusion,
) -> LaneConclusion:
    planning_closed = (
        selector.final_selector_count == 1
        and scaling.min_margin > 0.0
        and hardware.controller_margin > 1.0
        and hardware.detector_word_bound < 1e-6
    )
    unconditional_closed = (
        selector.bare_derivation_status == "derived from original sole axiom"
        and scaling.direct_solve_frontier == math.inf
        and hardware.evidence_status == "fabricated and measured"
    )
    return LaneConclusion(
        planning_closed=planning_closed,
        unconditional_closed=unconditional_closed,
        promote_to_nature_grade=False,
        retained_status=(
            "planning closed as conditional theory; nature-grade closure HOLD"
        ),
    )


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap-floor", type=float, default=0.390)
    parser.add_argument("--bell-floor", type=float, default=0.999702)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    selector = selector_conclusion()
    scaling = scaling_conclusion(args.gap_floor, args.bell_floor)
    hardware = hardware_conclusion()
    conclusion = lane_conclusion(selector, scaling, hardware)

    selector_gate = (
        selector.final_selector_count == 1
        and selector.bare_derivation_status.startswith("negative")
    )
    scaling_gate = (
        scaling.certified_sides == (4, 6, 8, 10, 12)
        and scaling.min_margin > 0.0
        and "side 14" in scaling.next_side_status
    )
    hardware_gate = (
        hardware.controller_margin > 2.0
        and hardware.detector_word_bound < 1e-6
        and "no measured" in hardware.evidence_status
    )
    boundary_gate = (
        conclusion.planning_closed
        and not conclusion.unconditional_closed
        and not conclusion.promote_to_nature_grade
    )

    print("TELEPORTATION CONCLUSION BOUNDARY")
    print("Status: planning closure with explicit nature-grade HOLD")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "selector conclusion: "
        f"without_orientation={selector.residual_without_orientation}, "
        f"without_action={selector.residual_without_action}, "
        f"without_no_dwell={selector.residual_without_no_dwell}, "
        f"final_selector_count={selector.final_selector_count}, "
        f"bare_derivation_status={selector.bare_derivation_status}, "
        f"terminal_decision={selector.terminal_decision}"
    )
    print(
        "scaling conclusion: "
        f"certified_sides={','.join(str(side) for side in scaling.certified_sides)}, "
        f"gap_floor={scaling.gap_floor:.3f}/L^2, "
        f"bell_floor={scaling.bell_floor:.6f}, "
        f"min_margin={scaling.min_margin:.3e}, "
        f"direct_solve_frontier={scaling.direct_solve_frontier}, "
        f"next_side_status={scaling.next_side_status}, "
        f"terminal_decision={scaling.terminal_decision}"
    )
    print(
        "hardware conclusion: "
        f"slot_threshold={hardware.slot_threshold:.3e}, "
        f"area_budget={hardware.area_budget_rad:.6f}, "
        f"controller_margin={hardware.controller_margin:.3f}, "
        f"detector_word_bound={hardware.detector_word_bound:.3e}, "
        f"detector_log10_overlap={hardware.detector_log10_overlap:.3f}, "
        f"evidence_status={hardware.evidence_status}, "
        f"terminal_decision={hardware.terminal_decision}"
    )
    print(
        "lane conclusion: "
        f"planning_closed={conclusion.planning_closed}, "
        f"unconditional_closed={conclusion.unconditional_closed}, "
        f"promote_to_nature_grade={conclusion.promote_to_nature_grade}, "
        f"retained_status={conclusion.retained_status}"
    )
    print()
    print("Acceptance gates:")
    print_gate("selector issue has a terminal retain/derive/reject boundary", selector_gate)
    print_gate("scaling issue has a side-12 certificate and side-14 blocker", scaling_gate)
    print_gate("hardware issue has thresholds but no measured implementation", hardware_gate)
    print_gate("planning closes while nature-grade closure remains HOLD", boundary_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  This is a terminal planning-boundary artifact, not a nature-grade")
    print("  proof. It deliberately prevents promotion until the three external")
    print("  obligations are actually supplied.")
    return 0 if all((selector_gate, scaling_gate, hardware_gate, boundary_gate)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
