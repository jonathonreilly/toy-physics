#!/usr/bin/env python3
"""Sweep persistent-node count and distance to measure gravity-like path bending.

Produces the model's first quantitative distortion-response curve:
how much does the stationary-action path bend as a function of the
number and placement of persistent nodes?

PStack experiment: gravity-distortion-response
"""

from __future__ import annotations
import ast
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    compare_geodesics,
    derive_local_rule,
)


def max_deflection(free_path_y_str: str, distorted_path_y_str: str) -> float:
    """Max |y_distorted - y_free| along the path."""
    free_ys = ast.literal_eval(free_path_y_str)
    dist_ys = ast.literal_eval(distorted_path_y_str)
    if len(free_ys) != len(dist_ys):
        return float("nan")
    return max(abs(d - f) for f, d in zip(free_ys, dist_ys))


def mean_deflection(free_path_y_str: str, distorted_path_y_str: str) -> float:
    """Mean |y_distorted - y_free| along the path."""
    free_ys = ast.literal_eval(free_path_y_str)
    dist_ys = ast.literal_eval(distorted_path_y_str)
    if len(free_ys) != len(dist_ys):
        return float("nan")
    return sum(abs(d - f) for f, d in zip(free_ys, dist_ys)) / len(free_ys)


def main() -> None:
    width = 20
    height = 10
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    source = (0, 0)
    # Test paths to several target_ys
    target_ys = [-5, -3, -1, 0, 1, 3, 5]

    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    print("=" * 72)
    print("GRAVITY-LIKE DISTORTION RESPONSE SWEEP")
    print("=" * 72)
    print(f"width={width}, height={height}, source={source}")
    print(f"target_ys={target_ys}")
    print()

    # =========================================================
    # SWEEP 1: Vary number of persistent nodes at fixed location
    # =========================================================
    print("=" * 72)
    print("SWEEP 1: Persistent node COUNT (placed at center, expanding outward)")
    print("=" * 72)
    print()

    # Place persistent nodes at (10, y) for y around 3 (above the path)
    # This should pull the path upward (toward the mass)
    node_sets = []
    for n in range(0, 13):
        if n == 0:
            nodes = frozenset()
        else:
            # Place n nodes centered at (10, 4), expanding vertically
            center_y = 4
            ys = [center_y + dy for dy in range(-(n-1)//2, (n-1)//2 + 1)][:n]
            nodes = frozenset((10, y) for y in ys)
        node_sets.append((n, nodes))

    print(f"{'n_nodes':>7s}  {'target_y':>8s}  {'free_action':>12s}  {'dist_action':>12s}  "
          f"{'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  dist_path_y")
    print("-" * 110)

    for n, pnodes in node_sets:
        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comparisons = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=target_ys, free_rule=free_rule, distorted_rule=distorted_rule,
        )
        for comp in comparisons:
            md = max_deflection(comp.free_path_y, comp.distorted_path_y)
            mnd = mean_deflection(comp.free_path_y, comp.distorted_path_y)
            ad = comp.distorted_action - comp.free_action
            print(f"{n:7d}  {comp.target_y:8d}  {comp.free_action:12.4f}  {comp.distorted_action:12.4f}  "
                  f"{ad:12.4f}  {md:10.4f}  {mnd:10.4f}  {comp.distorted_path_y}")

    # =========================================================
    # SWEEP 2: Vary distance of persistent nodes from path
    # =========================================================
    print()
    print("=" * 72)
    print("SWEEP 2: Persistent node DISTANCE (5 nodes, varying y-offset)")
    print("=" * 72)
    print()

    n_fixed = 5
    offsets = list(range(0, 10))

    print(f"{'offset':>7s}  {'target_y':>8s}  {'free_action':>12s}  {'dist_action':>12s}  "
          f"{'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  dist_path_y")
    print("-" * 110)

    for offset in offsets:
        center_y = offset
        ys = [center_y + dy for dy in range(-2, 3)]  # 5 nodes
        # Clamp to grid
        ys = [y for y in ys if -height <= y <= height]
        pnodes = frozenset((10, y) for y in ys)

        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comparisons = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=[0],  # Just measure path to center
            free_rule=free_rule, distorted_rule=distorted_rule,
        )
        for comp in comparisons:
            md = max_deflection(comp.free_path_y, comp.distorted_path_y)
            mnd = mean_deflection(comp.free_path_y, comp.distorted_path_y)
            ad = comp.distorted_action - comp.free_action
            print(f"{offset:7d}  {comp.target_y:8d}  {comp.free_action:12.4f}  {comp.distorted_action:12.4f}  "
                  f"{ad:12.4f}  {md:10.4f}  {mnd:10.4f}  {comp.distorted_path_y}")

    # =========================================================
    # SWEEP 3: Vary x-position of persistent nodes
    # =========================================================
    print()
    print("=" * 72)
    print("SWEEP 3: Persistent node X-POSITION (5 nodes at y=4, varying x)")
    print("=" * 72)
    print()

    print(f"{'x_pos':>7s}  {'target_y':>8s}  {'free_action':>12s}  {'dist_action':>12s}  "
          f"{'action_diff':>12s}  {'max_defl':>10s}  {'mean_defl':>10s}  dist_path_y")
    print("-" * 110)

    for x_pos in range(2, 19, 2):
        ys = [2, 3, 4, 5, 6]
        pnodes = frozenset((x_pos, y) for y in ys)
        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comparisons = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=[0],
            free_rule=free_rule, distorted_rule=distorted_rule,
        )
        for comp in comparisons:
            md = max_deflection(comp.free_path_y, comp.distorted_path_y)
            mnd = mean_deflection(comp.free_path_y, comp.distorted_path_y)
            ad = comp.distorted_action - comp.free_action
            print(f"{x_pos:7d}  {comp.target_y:8d}  {comp.free_action:12.4f}  {comp.distorted_action:12.4f}  "
                  f"{ad:12.4f}  {md:10.4f}  {mnd:10.4f}  {comp.distorted_path_y}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
