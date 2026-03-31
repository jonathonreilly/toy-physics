#!/usr/bin/env python3
"""Does the critical ratio R_c = 1 + |y|/s change with corrected propagator?

The critical ratio was derived with 1/delay^p. Test with 1/L^p.
If R_c is unchanged: the interference regime is propagator-independent
(it's determined by topology/geometry, not attenuation).
If R_c changes: the propagator affects the interference threshold.

PStack experiment: critical-ratio-corrected
"""

from __future__ import annotations
import math
import cmath
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
    local_edge_properties,
)


def two_slit_corrected(width, height, slit_ys, screen_y, phase_shift_upper,
                       attenuation_mode="delay"):
    """Two-slit probability at screen_y with specified attenuation mode."""
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (1, 0)
    barrier_x = width // 2
    detector_x = width

    postulates = RulePostulates(
        phase_per_action=4.0, attenuation_power=1.0,
        attenuation_mode=attenuation_mode,
    )
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    field = derive_node_field(nodes, rule)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    blocked = frozenset(
        (barrier_x, y) for y in range(-height, height+1) if y not in slit_ys
    )

    amps = {source: 1.0+0.0j}
    for node in order:
        if node not in amps or node in blocked:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
            _, _, link_amp = local_edge_properties(node, nb, rule, field)

            # Apply phase shift at upper slit
            if node[0] < barrier_x <= nb[0] and nb[1] in slit_ys and nb[1] > 0:
                link_amp *= cmath.exp(1j * phase_shift_upper)

            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a * link_amp

    return abs(amps.get((detector_x, screen_y), 0.0))**2


def visibility(width, height, slit_ys, screen_y, n_phases, attenuation_mode):
    """Compute V at screen_y by sweeping phase."""
    phases = [2*math.pi*i/n_phases for i in range(n_phases)]
    probs = [two_slit_corrected(width, height, slit_ys, screen_y, ph, attenuation_mode)
             for ph in phases]
    p_max, p_min = max(probs), min(probs)
    return (p_max - p_min) / (p_max + p_min) if (p_max + p_min) > 0 else 0.0


def main():
    n_phases = 24
    height = 10

    print("=" * 70)
    print("CRITICAL RATIO WITH CORRECTED PROPAGATOR")
    print("  Does R_c = 1 + |y|/s change with 1/L^p?")
    print("=" * 70)
    print()

    # Test a few representative (width, slit_half, y) combinations
    test_cases = [
        # (width, slit_half, y) — chosen to bracket the critical ratio
        (16, 4, 0),   # R = 2.0, expected V > 0
        (16, 4, 1),   # R = 2.0, y=1: R_c = 1.25 < 2.0 → V > 0
        (16, 4, 3),   # R = 2.0, y=3: R_c = 1.75 < 2.0 → V > 0
        (16, 4, 5),   # R = 2.0, y=5: R_c = 2.25 > 2.0 → V = 0
        (8, 2, 0),    # R = 2.0
        (8, 2, 1),    # R_c = 1.5 < 2.0
        (8, 2, 3),    # R_c = 2.5 > 2.0
        (20, 4, 0),   # R = 2.5
        (20, 4, 4),   # R_c = 2.0 < 2.5
        (20, 4, 8),   # R_c = 3.0 > 2.5
        (12, 3, 0),   # R = 2.0
        (12, 3, 2),   # R_c = 1.67 < 2.0
        (12, 3, 5),   # R_c = 2.67 > 2.0
    ]

    print(f"  {'w':>3s}  {'sh':>3s}  {'y':>3s}  {'R':>5s}  {'R_c':>5s}  "
          f"{'V_delay':>8s}  {'V_geom':>8s}  {'match':>6s}")
    print(f"  {'-' * 44}")

    match_count = 0
    total = 0

    for w, sh, y in test_cases:
        slit_ys = {-sh, sh}
        R = w / (2 * sh)
        R_c = 1 + abs(y) / sh if sh > 0 else 999

        v_delay = visibility(w, height, slit_ys, y, n_phases, "delay")
        v_geom = visibility(w, height, slit_ys, y, n_phases, "geometry")

        # Both should agree on V>0 vs V≈0
        delay_on = v_delay > 0.05
        geom_on = v_geom > 0.05
        match = delay_on == geom_on
        if match:
            match_count += 1
        total += 1

        print(f"  {w:3d}  {sh:3d}  {y:3d}  {R:5.1f}  {R_c:5.2f}  "
              f"{v_delay:8.4f}  {v_geom:8.4f}  {'Y' if match else 'N':>6s}")

    print()
    print(f"  Agreement: {match_count}/{total}")

    if match_count == total:
        print("  → R_c is UNCHANGED by propagator correction")
        print("  → Critical ratio is determined by topology, not attenuation")
    else:
        print("  → R_c DIFFERS between propagators")
        print("  → The attenuation affects the interference threshold")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
