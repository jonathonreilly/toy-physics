#!/usr/bin/env python3
"""Render the shared mechanism-language crosswalk across current regimes.

This is a compression artifact, not a new frontier scan. It takes the retained
results from the geometry ladder / beyond-ceiling work and the generated-DAG
bridge work and states them in one common vocabulary:

1. packet completion / closure-load
2. balance / sided load sharing
3. bottleneck / placement modifiers
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AxisCard:
    axis: str
    geometry_observables: tuple[str, ...]
    generated_observables: tuple[str, ...]
    meaning: str


@dataclass(frozen=True)
class RegimeCard:
    domain: str
    regime: str
    gate: str
    selector: str
    physical_read: str


AXES = (
    AxisCard(
        axis="completion/load",
        geometry_observables=(
            "closure_load",
            "mid_candidate_attached_max >= 7.500",
            "mid_candidate_bridge_bridge_closed_pair_max >= 10.000",
        ),
        generated_observables=(
            "center_balanced_log_paths",
            "center_slit_load_retimed",
        ),
        meaning=(
            "How much of the interior packet actually closes / loads. This is the "
            "main floor-setting axis in both domains."
        ),
    ),
    AxisCard(
        axis="balance",
        geometry_observables=(
            "anchor_closure_intensity_gap",
            "anchor_deep_share_gap",
            "high_bridge_right_count",
        ),
        generated_observables=(
            "center_path_balance",
            "center_balance_share",
        ),
        meaning=(
            "How symmetrically that load is shared across the competing sides of the "
            "packet. This is the main branch-selection axis near the floor."
        ),
    ),
    AxisCard(
        axis="bottleneck/placement",
        geometry_observables=(
            "mid_anchor_closure_peak",
        ),
        generated_observables=(
            "center_retiming_alignment",
            "center_slit_share",
        ),
        meaning=(
            "Where the packet is concentrated and how efficiently it reaches the "
            "screen-facing side. These terms modulate the signal but are not the "
            "primary retained branch split."
        ),
    ),
)


REGIMES = (
    RegimeCard(
        domain="geometry",
        regime="moderate anchor-balance basin",
        gate=(
            "-2.000 <= anchor_closure_intensity_gap <= 2.333 "
            "and mid_anchor_closure_peak <= 10.000"
        ),
        selector=(
            "right/deep bridge shoulder, low-support throat, or frozen mid-anchor knot"
        ),
        physical_read=(
            "A subcritical completion band where balance geometry matters before the "
            "system lifts into the heavier packet-completion regime."
        ),
    ),
    RegimeCard(
        domain="geometry",
        regime="beyond-ceiling shared packet regime",
        gate=(
            "closure_load >= 73.000 with shared 8/12 packet completion "
            "(equivalently mid_candidate_attached_max >= 7.500)"
        ),
        selector=(
            "outer-rect load tail, taper-hard two-right-bridge branch, or "
            "skew-wrap negative-deep branch"
        ),
        physical_read=(
            "Packet completion has already happened; branch identity is then decided "
            "by how the completed load is sided."
        ),
    ),
    RegimeCard(
        domain="generated-DAG",
        regime="balance-led near-floor branch",
        gate="center_balanced_log_paths <= 17.671",
        selector="center_path_balance / center_balance_share",
        physical_read=(
            "The detector-side packet has not yet lifted far enough for raw balanced "
            "load to dominate, so visibility is decided mainly by shared side balance."
        ),
    ),
    RegimeCard(
        domain="generated-DAG",
        regime="balanced-load-led branch",
        gate="center_balanced_log_paths > 17.671",
        selector="center_balanced_log_paths with balance as the residual crossover filter",
        physical_read=(
            "Once enough balanced detector-side load is present, raw packet completion "
            "carries the branch, with balance only deciding the near-floor crossover."
        ),
    ),
)


def main() -> None:
    print("=" * 72)
    print("MECHANISM REGIME CROSSWALK")
    print("=" * 72)
    print("Shared axes:")
    for axis in AXES:
        print(f"  {axis.axis}")
        print(f"    geometry : {', '.join(axis.geometry_observables)}")
        print(f"    generated: {', '.join(axis.generated_observables)}")
        print(f"    meaning  : {axis.meaning}")
        print()

    print("Retained regime cards:")
    for card in REGIMES:
        print(f"  [{card.domain}] {card.regime}")
        print(f"    gate     : {card.gate}")
        print(f"    selector : {card.selector}")
        print(f"    meaning  : {card.physical_read}")
        print()

    print("Compact crosswalk:")
    print(
        "  In both lanes, packet completion / closure-load sets the regime floor, "
        "while balance decides which near-floor rows or subbranches survive. The "
        "geometry ladder expresses that on anchor- and bridge-centered packets; the "
        "generated-DAG bridge expresses the same structure on detector-side slit packets."
    )
    print(
        "  The retained difference is where the packet is read out: geometry uses "
        "anchor/mid-packet placement, while generated DAGs use detector-side "
        "balanced slit-load. But the common theme is the same: completion first, "
        "balance second, bottleneck terms as modifiers."
    )


if __name__ == "__main__":
    main()
