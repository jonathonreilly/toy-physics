#!/usr/bin/env python3
"""Fine sweep of gravity-like effects: action falloff, path deflection,
and functional form fitting.

Measures both the "potential" (action difference) and the "force"
(path deflection) as continuous functions of distance, node count,
and target position.

PStack experiment: gravity-falloff-fit
"""

from __future__ import annotations
import ast
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    compare_geodesics,
    derive_local_rule,
)


def path_deflections(free_str: str, dist_str: str) -> tuple[float, float, float]:
    """Return (max_defl, mean_defl, integrated_defl) from path y-coordinate strings."""
    free_ys = ast.literal_eval(free_str)
    dist_ys = ast.literal_eval(dist_str)
    if len(free_ys) != len(dist_ys):
        return (float("nan"),) * 3
    diffs = [d - f for f, d in zip(free_ys, dist_ys)]
    abs_diffs = [abs(d) for d in diffs]
    return max(abs_diffs), sum(abs_diffs) / len(abs_diffs), sum(diffs)


def main() -> None:
    width = 30
    height = 12
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    source = (0, 0)
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    print("=" * 80)
    print("GRAVITY FALLOFF AND DEFLECTION SWEEP")
    print("=" * 80)
    print(f"width={width}, height={height}, source={source}")
    print()

    # =========================================================
    # SWEEP 1: Fine distance sweep — action falloff at target y=3
    # (off-axis so we get both action AND deflection)
    # 5 persistent nodes at (15, d) for d = 1..11, target y=3
    # =========================================================
    print("=" * 80)
    print("SWEEP 1: ACTION + DEFLECTION vs DISTANCE (5 nodes, target y=3)")
    print("  Persistent nodes at x=15, y centered at offset d from path axis")
    print("=" * 80)
    print()

    n_nodes = 5
    target_y = 3

    print(f"{'dist':>5s}  {'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  "
          f"{'net_defl':>10s}  path_summary")
    print("-" * 90)

    action_vs_dist = []

    for offset in range(1, 12):
        center_y = offset
        ys = [center_y + dy for dy in range(-2, 3)]
        ys = [y for y in ys if -height <= y <= height]
        pnodes = frozenset((15, y) for y in ys)

        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comps = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=[target_y], free_rule=free_rule, distorted_rule=distorted_rule,
        )
        c = comps[0]
        ad = c.distorted_action - c.free_action
        mx, mn, net = path_deflections(c.free_path_y, c.distorted_path_y)

        # Distance from mass center to the free path's closest approach
        # Free path to y=3 goes roughly through y~1.5 at x=15
        effective_dist = abs(offset - target_y / 2)

        action_vs_dist.append((offset, effective_dist, ad, mx, mn, net))
        print(f"{offset:5d}  {ad:12.4f}  {mx:10.4f}  {mn:10.4f}  "
              f"{net:10.4f}  {c.distorted_path_y[:80]}")

    # =========================================================
    # SWEEP 2: Node count sweep at fixed distance, target y=3
    # =========================================================
    print()
    print("=" * 80)
    print("SWEEP 2: ACTION + DEFLECTION vs NODE COUNT (at y=5, target y=3)")
    print("=" * 80)
    print()

    print(f"{'n':>5s}  {'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  "
          f"{'net_defl':>10s}")
    print("-" * 55)

    for n in range(2, 16):
        center_y = 5
        ys = list(range(center_y - (n-1)//2, center_y + n//2 + 1))[:n]
        ys = [y for y in ys if -height <= y <= height]
        pnodes = frozenset((15, y) for y in ys)

        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comps = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=[target_y], free_rule=free_rule, distorted_rule=distorted_rule,
        )
        c = comps[0]
        ad = c.distorted_action - c.free_action
        mx, mn, _ = path_deflections(c.free_path_y, c.distorted_path_y)
        print(f"{n:5d}  {ad:12.4f}  {mx:10.4f}  {mn:10.4f}")

    # =========================================================
    # SWEEP 3: Full angular sweep — deflection for all target_ys
    # with fixed mass at (15, 6)
    # =========================================================
    print()
    print("=" * 80)
    print("SWEEP 3: DEFLECTION vs TARGET ANGLE (5 nodes at y=6)")
    print("  Shows how bending depends on path direction relative to mass")
    print("=" * 80)
    print()

    pnodes = frozenset((15, y) for y in [4, 5, 6, 7, 8])
    distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
    all_targets = list(range(-height, height + 1))

    print(f"{'target_y':>8s}  {'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  "
          f"{'net_defl':>10s}  {'toward_mass':>11s}")
    print("-" * 75)

    comps = compare_geodesics(
        width=width, height=height, source=source,
        target_ys=all_targets, free_rule=free_rule, distorted_rule=distorted_rule,
    )
    for c in comps:
        ad = c.distorted_action - c.free_action
        mx, mn, net = path_deflections(c.free_path_y, c.distorted_path_y)
        toward = "YES" if net > 0 else ("NO" if net < 0 else "NONE")
        print(f"{c.target_y:8d}  {ad:12.4f}  {mx:10.4f}  {mn:10.4f}  "
              f"{net:10.4f}  {toward:>11s}")

    # =========================================================
    # FUNCTIONAL FORM FIT: action_diff vs distance
    # =========================================================
    print()
    print("=" * 80)
    print("FUNCTIONAL FORM ANALYSIS: action_diff vs offset")
    print("=" * 80)
    print()

    # Use sweep 1 data
    print(f"{'offset':>7s}  {'action_diff':>12s}  {'1/d':>10s}  {'1/d^2':>10s}  {'exp(-d)':>10s}")
    print("-" * 55)

    for offset, eff_d, ad, _, _, _ in action_vs_dist:
        d = max(offset, 0.01)
        inv_d = 1.0 / d
        inv_d2 = 1.0 / (d * d)
        exp_d = math.exp(-d * 0.3)  # trial decay constant
        print(f"{offset:7d}  {ad:12.4f}  {inv_d:10.4f}  {inv_d2:10.4f}  {exp_d:10.4f}")

    # Compute ratios to test power law: if action_diff ~ d^(-n), then
    # log(action_diff) vs log(d) should be linear with slope -n
    print()
    print("Log-log analysis (offset, |action_diff|):")
    for offset, _, ad, _, _, _ in action_vs_dist:
        if offset > 0 and ad != 0:
            print(f"  ln({offset}) = {math.log(offset):6.3f}  ln(|ad|) = {math.log(abs(ad)):6.3f}")

    # Ratio test: action_diff(d) / action_diff(d+1)
    print()
    print("Successive ratio test (ad[d+1] / ad[d]):")
    for i in range(len(action_vs_dist) - 1):
        d1, _, ad1, _, _, _ = action_vs_dist[i]
        d2, _, ad2, _, _, _ = action_vs_dist[i + 1]
        if ad1 != 0:
            ratio = ad2 / ad1
            print(f"  ad[{d2}] / ad[{d1}] = {ratio:.6f}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
