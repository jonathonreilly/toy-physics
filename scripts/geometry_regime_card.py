#!/usr/bin/env python3
"""Render the compact retained geometry-side regime card.

This is a compression artifact for the mechanism-language lane. It rewrites the
current low-overlap / beyond-ceiling geometry map into the shorter card that is
actually retained after the generated-DAG crosswalk:

1. support-collapse guard
2. subcritical balance basin
3. supercritical completed-packet regime
4. exhausted-wall boundary
"""

from __future__ import annotations


def main() -> None:
    print("=" * 72)
    print("GEOMETRY REGIME CARD")
    print("=" * 72)
    print("Historical in-domain classifier:")
    print(
        "  branch-aware frozen rc0|ml0|c2 law exact across the historical 192..5504 ladder"
    )
    print()

    print("Support-collapse guard:")
    print("  support_load = 0, closure_load = 0, edge_identity_event_count = 0")
    print(
        "  meaning: zero-support generated failures are out-of-domain rather than a "
        "continuation of the historical pair-only branch"
    )
    print()

    print("Subcritical balance basin:")
    print(
        "  gate: -2.000 <= anchor_closure_intensity_gap <= 2.333 and "
        "mid_anchor_closure_peak <= 10.000"
    )
    print(
        "  realized generated forms: right/deep shoulder "
        "(anchor_deep_share_gap >= 0.250) and low-support throat "
        "(closure_load <= 24.500)"
    )
    print(
        "  meaning: completion/load is still subcritical, so sided balance decides "
        "the local realization"
    )
    print(
        "  ceiling contrast: the frozen mid-anchor knot sits above the ceiling at "
        "mid_anchor_closure_peak = 12.000 and marks the exit from this basin"
    )
    print()

    print("Supercritical completed-packet regime:")
    print(
        "  gate: shared 8/12 packet completion "
        "(equivalently mid_candidate_attached_max >= 7.500; observed rows also satisfy "
        "closure_load >= 73.000)"
    )
    print("  retained subbranches:")
    print("    outer-rect tail: support_load >= 24.000")
    print("    taper-hard arm: high_bridge_right_count >= 1.500")
    print("    skew-wrap arm: anchor_deep_share_gap <= -0.334")
    print(
        "  meaning: completion/load has already happened, so branch identity is then "
        "decided by how the completed packet is sided"
    )
    print()

    print("Exhausted-wall boundary:")
    print(
        "  nearest non-base misses stall at the depleted 7/8 packet "
        "(mid_candidate_attached_max = 7.000, mid_anchor_closure_peak = 8.000) "
        "with no flank hinge"
    )
    print(
        "  meaning: the current beyond-ceiling continuation is still base-local "
        "against the finished non-base wall"
    )
    print()

    print("Compact reading:")
    print(
        "  collapse guard -> subcritical balance basin -> supercritical completed-packet "
        "regime -> non-base exhausted wall"
    )
    print(
        "  In the shared crosswalk vocabulary: completion/load sets the floor, balance "
        "selects the branch, bottleneck/placement terms sharpen the boundary."
    )


if __name__ == "__main__":
    main()
