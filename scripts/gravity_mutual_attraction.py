#!/usr/bin/env python3
"""Test mutual gravitation between two persistent patterns.

Prior experiments showed one mass bending test paths. This tests
whether two masses bend toward EACH OTHER — the model's version
of Newton's mutual gravitation.

Method: place two persistent-node clusters at different positions.
Compare the geodesic from each mass's location toward the other
with the free geodesic. If both paths bend inward (toward each
other), mutual gravitation is confirmed.

Also test: does the bending depend on the OTHER mass's size?
(Heavier mass → more bending of the lighter one?)

PStack experiment: mutual-gravitation
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    derive_local_rule,
    stationary_action_path,
)


def resample_profile(values: list[int], target_len: int) -> list[float]:
    """Resample a path profile so different-length paths remain comparable."""
    if not values:
        return [0.0] * target_len
    if target_len <= 1:
        return [float(values[0])]
    if len(values) == 1:
        return [float(values[0])] * target_len

    result: list[float] = []
    scale = (len(values) - 1) / (target_len - 1)
    for index in range(target_len):
        position = index * scale
        lower = int(math.floor(position))
        upper = int(math.ceil(position))
        if lower == upper:
            result.append(float(values[lower]))
            continue
        frac = position - lower
        result.append((1.0 - frac) * values[lower] + frac * values[upper])
    return result


def path_shift_metrics(free_ys: list[int], dist_ys: list[int]) -> tuple[float, float]:
    """Compare two paths even when gravity changes the number of steps."""
    target_len = max(len(free_ys), len(dist_ys))
    free_profile = resample_profile(free_ys, target_len)
    dist_profile = resample_profile(dist_ys, target_len)
    deltas = [dist - free for free, dist in zip(free_profile, dist_profile)]
    max_deflection = max(abs(delta) for delta in deltas) if deltas else 0.0
    net_deflection = sum(deltas)
    return max_deflection, net_deflection


def measure_bending(
    width: int, height: int,
    persistent_nodes: frozenset[tuple[int, int]],
    source: tuple[int, int],
    target: tuple[int, int],
    postulates: RulePostulates,
) -> tuple[float, float, float, int, list[int], list[int]]:
    """Measure path bending from source to target with given persistent nodes.
    Returns (action_diff, max_deflection, net_deflection, step_delta, free_path_ys, distorted_path_ys)."""
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    dist_rule = derive_local_rule(persistent_nodes=persistent_nodes, postulates=postulates)

    free_action, free_path = stationary_action_path(
        width=width, height=height, source=source, target=target, rule=free_rule
    )
    dist_action, dist_path = stationary_action_path(
        width=width, height=height, source=source, target=target, rule=dist_rule
    )

    free_ys = [y for _, y in free_path]
    dist_ys = [y for _, y in dist_path]
    max_defl, net_defl = path_shift_metrics(free_ys, dist_ys)
    step_delta = len(dist_ys) - len(free_ys)
    action_diff = dist_action - free_action

    return action_diff, max_defl, net_defl, step_delta, free_ys, dist_ys


def net_deflection(free_ys: list[int], dist_ys: list[int]) -> float:
    """Positive = path moved upward, negative = downward."""
    _, net = path_shift_metrics(free_ys, dist_ys)
    return net


def main() -> None:
    width = 40
    height = 14
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    print("=" * 72)
    print("MUTUAL GRAVITATION TEST")
    print("=" * 72)
    print(f"width={width}, height={height}")
    print()

    # =========================================================
    # TEST 1: Two equal masses, measure path bending between them
    # =========================================================
    print("=" * 72)
    print("TEST 1: Two equal masses (5 nodes each)")
    print("=" * 72)
    print()

    mass_A = frozenset((10, y) for y in [5, 6, 7, 8, 9])  # upper-left
    mass_B = frozenset((30, y) for y in [-9, -8, -7, -6, -5])  # lower-right
    both = mass_A | mass_B

    # Path from A's region toward B's region
    source_A = (5, 7)   # near mass A
    target_B = (35, -7)  # near mass B

    for label, pnodes in [("No masses", frozenset()),
                           ("Mass A only", mass_A),
                           ("Mass B only", mass_B),
                           ("Both masses", both)]:
        ad, md, nd, step_delta, fy, dy = measure_bending(width, height, pnodes, source_A, target_B, postulates)
        print(f"  {label:>15s}: action_diff={ad:10.4f}  max_defl={md:.2f}  net_defl={nd:+.2f}  "
              f"step_delta={step_delta:+d}  "
              f"path_y[mid]={dy[len(dy)//2]:+d}")

    print()

    # Path from B's region toward A's region
    source_B = (35, -7)
    target_A = (5, 7)

    print("  Reverse direction (B → A):")
    for label, pnodes in [("No masses", frozenset()),
                           ("Mass A only", mass_A),
                           ("Mass B only", mass_B),
                           ("Both masses", both)]:
        ad, md, nd, step_delta, fy, dy = measure_bending(width, height, pnodes, source_B, target_A, postulates)
        print(f"  {label:>15s}: action_diff={ad:10.4f}  max_defl={md:.2f}  net_defl={nd:+.2f}  "
              f"step_delta={step_delta:+d}  "
              f"path_y[mid]={dy[len(dy)//2]:+d}")

    # =========================================================
    # TEST 2: Mutual bending — does each mass pull the other's paths?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Mutual bending — paths from near each mass to center")
    print("=" * 72)
    print()

    mass_upper = frozenset((20, y) for y in [6, 7, 8, 9, 10])
    mass_lower = frozenset((20, y) for y in [-10, -9, -8, -7, -6])
    both_sym = mass_upper | mass_lower

    # Path from left to right, passing between the two masses
    for start_y in [-3, 0, 3]:
        print(f"  Path y={start_y} (source=(0,{start_y}), target=(40,{start_y})):")
        for label, pnodes in [("No masses", frozenset()),
                               ("Upper only", mass_upper),
                               ("Lower only", mass_lower),
                               ("Both masses", both_sym)]:
            ad, md, nd, step_delta, fy, dy = measure_bending(width, height, pnodes, (0, start_y), (width, start_y), postulates)
            toward = "toward upper" if nd > 0 else ("toward lower" if nd < 0 else "none")
            print(f"    {label:>15s}: ad={ad:10.4f}  max_d={md:6.2f}  net={nd:+7.2f}  "
                  f"step_delta={step_delta:+d}  bend={toward}")
        print()

    # =========================================================
    # TEST 3: Mass-ratio dependence
    # =========================================================
    print("=" * 72)
    print("TEST 3: Does bending depend on the OTHER mass's size?")
    print("=" * 72)
    print()

    # Fixed test path from (0,0) to (40,0), mass at (20, 6)
    # Vary the mass size from 2 to 10 nodes
    print(f"  {'n_nodes':>8s}  {'action_diff':>12s}  {'max_defl':>10s}  {'net_defl':>10s}  {'step_Δ':>7s}")
    print(f"  {'-' * 57}")

    for n in range(2, 11):
        center_y = 6
        ys = list(range(center_y - (n-1)//2, center_y + n//2 + 1))[:n]
        ys = [y for y in ys if -height <= y <= height]
        pnodes = frozenset((20, y) for y in ys)
        ad, md, nd, step_delta, fy, dy = measure_bending(width, height, pnodes, (0, 0), (width, 0), postulates)
        print(f"  {n:8d}  {ad:12.4f}  {md:10.2f}  {nd:+10.2f}  {step_delta:+7d}")

    # =========================================================
    # TEST 4: Superposition — does bending from both masses
    # equal the sum of bending from each mass alone?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 4: Superposition test — is bending additive?")
    print("=" * 72)
    print()

    mass_1 = frozenset((15, y) for y in [5, 6, 7, 8, 9])
    mass_2 = frozenset((25, y) for y in [-9, -8, -7, -6, -5])

    for ty in [-5, -2, 0, 2, 5]:
        ad_1, _, _, _, _, _ = measure_bending(width, height, mass_1, (0, ty), (width, ty), postulates)
        ad_2, _, _, _, _, _ = measure_bending(width, height, mass_2, (0, ty), (width, ty), postulates)
        ad_both, md_b, nd_b, step_delta_b, _, dy_b = measure_bending(width, height, mass_1 | mass_2, (0, ty), (width, ty), postulates)
        ad_sum = ad_1 + ad_2
        deviation = ad_both - ad_sum
        print(f"  target_y={ty:+2d}: ad_1={ad_1:8.4f}  ad_2={ad_2:8.4f}  "
              f"ad_sum={ad_sum:8.4f}  ad_both={ad_both:8.4f}  "
              f"deviation={deviation:8.4f}  ({deviation/ad_both*100 if ad_both else 0:+.1f}%)  "
              f"max_d={md_b:5.2f}  net={nd_b:+6.2f}  step_delta={step_delta_b:+d}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
