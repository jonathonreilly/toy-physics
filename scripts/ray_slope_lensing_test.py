#!/usr/bin/env python3
"""Proper ray-slope lensing test.

Previous claim "correct 2D lensing" was overclaimed. The detector-centroid
shift increased with b, which does NOT prove constant deflection angle.

This test does what was requested:
1. Measure incoming and outgoing ray slope NEAR the mass
2. Move detector plane farther downstream, check if angle stabilizes
3. Compare measured angle against 2D log-potential expectation

The deflection angle is defined as:
  θ = d(centroid_y)/d(x) evaluated downstream of the mass

If θ stabilizes with increasing detector distance → genuine deflection.
If θ keeps changing → not simple lensing.

For 2D log-potential (point mass): deflection ∝ M/b (constant for fixed M).
For our model: to be determined.

PStack experiment: ray-slope-lensing-test
"""

from __future__ import annotations
import math
import cmath
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
)


def propagate_geom_full(nodes, source, node_field, phase_k, atten_power):
    """Return full amplitude dict for all nodes."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
            ea = cmath.exp(1j * phase_k * action) * atten
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * ea

    return amplitudes


def centroid_at_x(amplitudes, x, screen_ys):
    """Probability-weighted centroid y at column x."""
    dist = {y: abs(amplitudes.get((x, y), 0.0)) ** 2 for y in screen_ys}
    total = sum(dist.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in dist.items()) / total


def main() -> None:
    width = 80
    height = 35
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    free_field = {n: 0.0 for n in nodes}
    mass_x = 30

    print("=" * 80)
    print("RAY SLOPE LENSING TEST")
    print(f"  Grid: {width}x{2*height+1}, source=(0,0), mass at x={mass_x}")
    print("  Corrected propagator: 1/L^p")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Centroid trajectory across the grid
    # ================================================================
    print("TEST 1: Centroid trajectory y(x) — incoming, near-mass, outgoing")
    print(f"  k=0.3 (weak coupling / linear regime)")
    print()

    postulates = RulePostulates(phase_per_action=0.3, attenuation_power=1.0)

    for b in [5, 8, 12, 18]:
        mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)

        free_amps = propagate_geom_full(nodes, source, free_field, 0.3, 1.0)
        mass_amps = propagate_geom_full(nodes, source, mf, 0.3, 1.0)

        print(f"  b = {b} (mass at y={b-1}..{b+1}):")
        print(f"    {'x':>4s}  {'cy_free':>8s}  {'cy_mass':>8s}  {'shift':>8s}  {'slope':>8s}  {'region':>10s}")
        print(f"    {'-' * 52}")

        x_values = list(range(5, width + 1, 5))
        prev_shift = None
        slopes = []

        for x in x_values:
            fcy = centroid_at_x(free_amps, x, screen_ys)
            mcy = centroid_at_x(mass_amps, x, screen_ys)
            shift = mcy - fcy

            if prev_shift is not None:
                slope = (shift - prev_shift) / 5.0  # Δshift / Δx
                slopes.append((x, slope))
            else:
                slope = 0

            region = "incoming" if x < mass_x - 5 else \
                     "near-mass" if x < mass_x + 5 else "outgoing"

            print(f"    {x:4d}  {fcy:8.3f}  {mcy:8.3f}  {shift:+8.4f}  "
                  f"{slope:+8.5f}  {region:>10s}")
            prev_shift = shift

        # Extract outgoing slope (x > mass_x + 10)
        outgoing_slopes = [s for x, s in slopes if x > mass_x + 10]
        if outgoing_slopes:
            mean_out = sum(outgoing_slopes) / len(outgoing_slopes)
            std_out = (sum((s - mean_out) ** 2 for s in outgoing_slopes) / len(outgoing_slopes)) ** 0.5
            print(f"    Outgoing slope: {mean_out:+.5f} ± {std_out:.5f}")
            print(f"    Stabilized: {'YES' if std_out < abs(mean_out) * 0.3 else 'no'}")
        print()

    # ================================================================
    # TEST 2: Outgoing angle vs impact parameter
    # ================================================================
    print("=" * 80)
    print("TEST 2: Outgoing angle vs impact parameter b")
    print("  Measure slope from x=50..75 (well past mass at x=30)")
    print()

    for k in [0.2, 0.3, 0.5]:
        print(f"  k = {k}:")
        print(f"    {'b':>4s}  {'out_slope':>10s}  {'slope×b':>10s}  {'slope×b²':>10s}")
        print(f"    {'-' * 40}")

        bs_data = []
        for b in [3, 5, 8, 10, 12, 15, 18, 20, 25, 30]:
            mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
            mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
            mf = derive_node_field(nodes, mr)

            free_amps = propagate_geom_full(nodes, source, free_field, k, 1.0)
            mass_amps = propagate_geom_full(nodes, source, mf, k, 1.0)

            # Measure outgoing slope between x=50 and x=70
            shifts_far = []
            for x in range(50, 76, 5):
                fcy = centroid_at_x(free_amps, x, screen_ys)
                mcy = centroid_at_x(mass_amps, x, screen_ys)
                shifts_far.append((x, mcy - fcy))

            # Linear fit for slope
            if len(shifts_far) > 2:
                n = len(shifts_far)
                mx = sum(x for x, _ in shifts_far) / n
                ms = sum(s for _, s in shifts_far) / n
                num = sum((x - mx) * (s - ms) for x, s in shifts_far)
                den = sum((x - mx) ** 2 for x, _ in shifts_far)
                slope = num / den if den > 0 else 0
            else:
                slope = 0

            bs_data.append((b, slope))
            print(f"    {b:4d}  {slope:+10.6f}  {slope * b:+10.4f}  {slope * b * b:+10.2f}")

        # Fit slope vs b
        valid = [(b, s) for b, s in bs_data if abs(s) > 1e-6]
        if len(valid) > 3:
            log_b = [math.log(b) for b, _ in valid]
            log_s = [math.log(abs(s)) for _, s in valid]
            n = len(valid)
            mb = sum(log_b) / n
            ms_l = sum(log_s) / n
            num = sum((lb - mb) * (ls - ms_l) for lb, ls in zip(log_b, log_s))
            den = sum((lb - mb) ** 2 for lb in log_b)
            alpha = num / den if den > 0 else 0
            print(f"    Outgoing angle ~ b^({alpha:.3f})")
            if abs(alpha + 1) < 0.3:
                print(f"    → Consistent with θ ~ 1/b (GR-like 2D lensing)")
            elif abs(alpha) < 0.3:
                print(f"    → Constant angle (θ independent of b)")
            else:
                print(f"    → Power law exponent {alpha:.2f}")
        print()

    # ================================================================
    # TEST 3: Does outgoing angle stabilize with detector distance?
    # ================================================================
    print("=" * 80)
    print("TEST 3: Outgoing angle vs detector distance (does it stabilize?)")
    print(f"  k=0.3, b=10")
    print()

    b = 10
    k = 0.3
    mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
    mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
    mf = derive_node_field(nodes, mr)

    free_amps = propagate_geom_full(nodes, source, free_field, k, 1.0)
    mass_amps = propagate_geom_full(nodes, source, mf, k, 1.0)

    print(f"  {'x_start':>8s}  {'x_end':>6s}  {'slope':>10s}")
    print(f"  {'-' * 30}")

    for x_start in [35, 40, 45, 50, 55, 60, 65, 70]:
        x_end = min(x_start + 10, width)
        if x_end <= x_start:
            continue

        pts = []
        for x in range(x_start, x_end + 1):
            fcy = centroid_at_x(free_amps, x, screen_ys)
            mcy = centroid_at_x(mass_amps, x, screen_ys)
            pts.append((x, mcy - fcy))

        if len(pts) > 2:
            n = len(pts)
            mx = sum(x for x, _ in pts) / n
            ms = sum(s for _, s in pts) / n
            num = sum((x - mx) * (s - ms) for x, s in pts)
            den = sum((x - mx) ** 2 for x, _ in pts)
            slope = num / den if den > 0 else 0
            print(f"  {x_start:8d}  {x_end:6d}  {slope:+10.6f}")

    print()
    print("  If slope stabilizes → genuine deflection with well-defined angle")
    print("  If slope keeps changing → not simple lensing")

    print()
    print("=" * 80)
    print("STATUS UPDATE")
    print("=" * 80)
    print()
    print("  Previous claim 'correct 2D gravitational lensing' → RETRACTED")
    print("  Current status: 'weak-coupling attraction survives,")
    print("    scattering observable needs cleaner definition'")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
