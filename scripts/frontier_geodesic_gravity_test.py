#!/usr/bin/env python3
"""Geodesic gravity test: do shortest paths curve toward or away from mass?

THE QUESTION:
  The first-principles derivation predicts that geodesics (minimum-delay
  paths) should bend AWAY from mass because delays INCREASE near mass
  (delay = L*(1+f), f > 0). But the wave propagation at specific k
  values gives TOWARD. Which is it at the geometric level?

TEST:
  Compute Dijkstra arrival times from source to detector layer, with
  and without a mass source. The transverse gradient of the arrival-time
  difference tells us which direction the geodesics bend.

  If arrival is EARLIER on the mass side: geodesics bend TOWARD mass
    → geometric gravity exists, wave adds dispersive corrections
  If arrival is LATER on the mass side: geodesics bend AWAY from mass
    → "gravity" is purely wave resonance, geometric baseline is repulsive

This uses the EXISTING infrastructure — infer_arrival_times is Dijkstra
on the delay-weighted graph.

RUNS ON: Both 2D (toy_event_physics) and 3D (Lattice3D) infrastructure.
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =====================================================================
# PART 1: 2D infrastructure (toy_event_physics)
# =====================================================================

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
)


def run_2d_geodesic_test():
    print("=" * 70)
    print("PART 1: 2D GEODESIC TEST (toy_event_physics infrastructure)")
    print("=" * 70)
    print()

    width = 20
    height = 8
    source = (0, 0)
    mass_center = (10, 4)

    nodes = build_rectangular_nodes(width, height)

    # Mass cluster
    cluster = frozenset(
        (x, y) for x in range(mass_center[0]-1, mass_center[0]+2)
        for y in range(mass_center[1]-1, mass_center[1]+2)
        if (x, y) in nodes
    )

    postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
    )

    # Flat field (no mass)
    rule_flat = derive_local_rule(frozenset(), postulates)
    field_flat = derive_node_field(nodes, rule_flat)
    arrival_flat = infer_arrival_times_from_source(nodes, source, rule_flat)

    # With mass (derive_node_field Laplacian relaxation)
    rule_mass = derive_local_rule(cluster, postulates)
    field_mass = derive_node_field(nodes, rule_mass)
    arrival_mass = infer_arrival_times_from_source(nodes, source, rule_mass)

    # Detector layer: x = width
    det_ys = sorted(y for (x, y) in nodes if x == width)

    print(f"  Grid: {width}x{2*height+1}, source={source}, mass={mass_center}")
    print(f"  Mass cluster: {len(cluster)} nodes")
    print(f"  Field at mass center: {field_mass.get(mass_center, 0):.4f}")
    print(f"  Field at (10, 0): {field_mass.get((10, 0), 0):.4f}")
    print()

    # Print arrival times at detector
    print(f"  {'y':>4} | {'t_flat':>10} | {'t_mass':>10} | {'t_diff':>10} | {'diff sign':>10}")
    print(f"  {'-'*50}")

    for y in det_ys:
        node = (width, y)
        tf = arrival_flat.get(node, float('inf'))
        tm = arrival_mass.get(node, float('inf'))
        diff = tm - tf
        sign = "LATER" if diff > 1e-6 else "EARLIER" if diff < -1e-6 else "SAME"
        print(f"  {y:>4} | {tf:>10.4f} | {tm:>10.4f} | {diff:>+10.4f} | {sign:>10}")

    # Transverse gradient at detector center (y=0)
    y_near_mass = 4  # closest to mass (mass at y=4)
    y_far = -4  # farthest from mass
    y_center = 0

    t_near = arrival_mass.get((width, y_near_mass), float('inf'))
    t_far = arrival_mass.get((width, y_far), float('inf'))
    t_center = arrival_mass.get((width, y_center), float('inf'))

    t_near_flat = arrival_flat.get((width, y_near_mass), float('inf'))
    t_far_flat = arrival_flat.get((width, y_far), float('inf'))

    diff_near = t_near - t_near_flat
    diff_far = t_far - t_far_flat
    diff_center = t_center - arrival_flat.get((width, y_center), float('inf'))

    print()
    print(f"  GEODESIC GRADIENT:")
    print(f"    Mass-side (y={y_near_mass}): arrival delayed by {diff_near:+.4f}")
    print(f"    Center   (y={y_center}):  arrival delayed by {diff_center:+.4f}")
    print(f"    Far-side (y={y_far}): arrival delayed by {diff_far:+.4f}")
    print()

    if diff_near > diff_far + 1e-6:
        print(f"  VERDICT: Mass-side arrivals are MORE delayed than far-side.")
        print(f"  → Geodesics bend AWAY from mass (shortest paths avoid slow region).")
        print(f"  → The geometric baseline is REPULSIVE.")
    elif diff_near < diff_far - 1e-6:
        print(f"  VERDICT: Mass-side arrivals are LESS delayed than far-side.")
        print(f"  → Geodesics bend TOWARD mass.")
        print(f"  → Geometric gravity EXISTS.")
    else:
        print(f"  VERDICT: Mass-side and far-side are equally delayed.")
        print(f"  → No transverse geodesic gradient (symmetric effect).")

    # Also check: does the field create an asymmetry in the DAG structure?
    dag_flat = build_causal_dag(nodes, arrival_flat)
    dag_mass = build_causal_dag(nodes, arrival_mass)

    # Count edges in the mass-side vs far-side of the DAG
    mass_side_edges = sum(1 for n in dag_mass for m in dag_mass[n]
                         if n[1] > 0 or m[1] > 0)
    far_side_edges = sum(1 for n in dag_mass for m in dag_mass[n]
                        if n[1] < 0 or m[1] < 0)
    mass_side_flat = sum(1 for n in dag_flat for m in dag_flat[n]
                        if n[1] > 0 or m[1] > 0)
    far_side_flat = sum(1 for n in dag_flat for m in dag_flat[n]
                       if n[1] < 0 or m[1] < 0)

    print()
    print(f"  DAG STRUCTURE:")
    print(f"    Mass-side edges: {mass_side_edges} (flat: {mass_side_flat})")
    print(f"    Far-side edges:  {far_side_edges} (flat: {far_side_flat})")
    print(f"    Difference: mass-side has {mass_side_edges - mass_side_flat:+d} vs flat")
    print(f"                far-side has  {far_side_edges - far_side_flat:+d} vs flat")

    if mass_side_edges != mass_side_flat or far_side_edges != far_side_flat:
        print(f"  → The field CHANGES the DAG topology (different causal structure).")
        print(f"     This is a geometric effect beyond just delay modification.")
    else:
        print(f"  → The DAG topology is unchanged. Only delays differ.")

    return diff_near, diff_far


# =====================================================================
# PART 2: 3D ordered lattice (analytic field)
# =====================================================================

def run_3d_geodesic_test():
    """Test on 3D lattice using arrival times."""
    try:
        import numpy as np
    except ImportError:
        print("\nPART 2: Skipped (numpy not available)")
        return

    print(f"\n\n{'='*70}")
    print("PART 2: 3D GEODESIC TEST (ordered lattice, analytic 1/r field)")
    print(f"{'='*70}")
    print()

    # Reuse Lattice3D infrastructure for arrival time computation
    # The key: infer_arrival_times uses Dijkstra on the delay-weighted graph
    # delay = L * (1 + f), so higher f = longer delay = geodesic avoids it

    BETA = 0.8
    MAX_D = 3
    h = 0.5
    phys_w = 6
    phys_l = 12
    K = 5.0
    STRENGTH = 5e-5

    hw = int(phys_w / h)
    nl = int(phys_l / h) + 1
    max_d = max(1, round(MAX_D / h))
    nw = 2 * hw + 1

    # Build node positions and map
    n_total = nl * nw * nw
    pos = np.zeros((n_total, 3))
    nmap = {}
    layer_starts = np.zeros(nl, dtype=np.int64)
    idx = 0
    for layer in range(nl):
        layer_starts[layer] = idx
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                pos[idx] = (x, iy * h, iz * h)
                nmap[(layer, iy, iz)] = idx
                idx += 1

    # Precompute edge offsets
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp = dy * h
            dzp = dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            offsets.append((dy, dz, L))

    # Build spatial-only 1/r field
    gl = 2 * nl // 3
    z_mass = 3
    iz_mass = round(z_mass / h)
    mi = nmap.get((gl, 0, iz_mass))
    my, mz = pos[mi, 1], pos[mi, 2]
    r_spatial = np.sqrt((pos[:, 1] - my)**2 + (pos[:, 2] - mz)**2) + 0.1
    field_mass = STRENGTH / r_spatial
    field_flat = np.zeros(n_total)

    print(f"  Lattice: {n_total:,} nodes, {nl} layers, h={h}")
    print(f"  Mass at spatial (y=0, z={z_mass}), layer {gl}")
    print(f"  Field at mass: {field_mass[mi]:.6f}")
    print()

    # Compute arrival times via layer-by-layer Dijkstra-like propagation
    # (simplified: since DAG is layered, just propagate minimum delay forward)
    def compute_arrivals(field):
        arrival = np.full(n_total, np.inf)
        src = nmap.get((0, 0, 0), 0)
        arrival[src] = 0.0

        for layer in range(nl - 1):
            ls = layer_starts[layer]
            npl = nw * nw
            ld = layer_starts[layer + 1] if layer + 1 < nl else n_total

            for dy, dz, L in offsets:
                for iy_src in range(nw):
                    iy_dst = iy_src + dy
                    if iy_dst < 0 or iy_dst >= nw:
                        continue
                    for iz_src in range(nw):
                        iz_dst = iz_src + dz
                        if iz_dst < 0 or iz_dst >= nw:
                            continue
                        si = ls + iy_src * nw + iz_src
                        di = ld + iy_dst * nw + iz_dst

                        if arrival[si] == np.inf:
                            continue

                        lf = 0.5 * (field[si] + field[di])
                        delay = L * (1.0 + lf)
                        new_t = arrival[si] + delay

                        if new_t < arrival[di]:
                            arrival[di] = new_t

        return arrival

    arrival_flat = compute_arrivals(field_flat)
    arrival_mass_arr = compute_arrivals(field_mass)

    # Check detector layer
    dl = nl - 1
    print(f"  {'iz':>4} {'z':>6} | {'t_flat':>10} | {'t_mass':>10} | {'t_diff':>10} | {'sign':>8}")
    print(f"  {'-'*55}")

    for iz in range(-hw, hw + 1, max(1, hw // 4)):
        idx_det = nmap.get((dl, 0, iz))
        if idx_det is None:
            continue
        z_phys = iz * h
        tf = arrival_flat[idx_det]
        tm = arrival_mass_arr[idx_det]
        diff = tm - tf
        sign = "LATER" if diff > 1e-8 else "EARLIER" if diff < -1e-8 else "SAME"
        print(f"  {iz:>4} {z_phys:>6.1f} | {tf:>10.4f} | {tm:>10.4f} | {diff:>+10.6f} | {sign:>8}")

    # Geodesic gradient
    iz_near = round(z_mass / h)  # near mass
    iz_far = -iz_near  # far from mass
    iz_center = 0

    idx_near = nmap.get((dl, 0, min(iz_near, hw)))
    idx_far = nmap.get((dl, 0, max(iz_far, -hw)))
    idx_center = nmap.get((dl, 0, iz_center))

    diff_near = arrival_mass_arr[idx_near] - arrival_flat[idx_near]
    diff_far = arrival_mass_arr[idx_far] - arrival_flat[idx_far]
    diff_center = arrival_mass_arr[idx_center] - arrival_flat[idx_center]

    print()
    print(f"  GEODESIC GRADIENT (3D lattice):")
    print(f"    Mass-side (z={min(iz_near, hw)*h:.1f}): delayed by {diff_near:+.6f}")
    print(f"    Center   (z=0):   delayed by {diff_center:+.6f}")
    print(f"    Far-side (z={max(iz_far, -hw)*h:.1f}): delayed by {diff_far:+.6f}")
    print()

    if diff_near > diff_far + 1e-8:
        print(f"  VERDICT: Mass-side more delayed → geodesics AWAY from mass.")
        print(f"  → Geometric baseline is REPULSIVE.")
    elif diff_near < diff_far - 1e-8:
        print(f"  VERDICT: Mass-side less delayed → geodesics TOWARD mass.")
        print(f"  → Geometric gravity EXISTS.")
    else:
        print(f"  VERDICT: Symmetric delay → no geodesic gradient.")

    # Quantify: what fraction of the wave deflection is geometric?
    print()
    print(f"  COMPARISON:")
    print(f"    Wave deflection at k=5: +0.000422 TOWARD (from k-sweep)")
    print(f"    Geodesic gradient: {diff_near - diff_far:+.6f} "
          f"({'TOWARD' if diff_near < diff_far else 'AWAY'})")
    if abs(diff_near - diff_far) > 1e-8:
        print(f"    → The wave and geodesic deflections are in "
              f"{'the SAME' if (diff_near < diff_far) else 'OPPOSITE'} directions.")


def main():
    print("=" * 70)
    print("GEODESIC GRAVITY TEST")
    print("=" * 70)
    print()
    print("Do shortest paths (geodesics) curve TOWARD or AWAY from mass?")
    print()
    print("Delays INCREASE near mass: delay = L*(1+f), f > 0.")
    print("If geodesics avoid the slow region → AWAY (repulsive baseline).")
    print("If geodesics curve toward mass despite longer delays → TOWARD.")
    print()

    run_2d_geodesic_test()
    run_3d_geodesic_test()

    print(f"\n{'='*70}")
    print("FINAL VERDICT")
    print(f"{'='*70}")
    print()
    print("If BOTH 2D and 3D geodesics bend AWAY from mass:")
    print("  → The model's 'gravity' is purely wave resonance.")
    print("  → No geometric gravitational attraction exists.")
    print("  → The TOWARD deflection at k=5 is a dispersive force,")
    print("    not gravity in the sense of Axiom 8.")
    print()
    print("If either bends TOWARD:")
    print("  → There is a geometric mechanism the derivation missed.")
    print("  → Gravity may have both geometric and dispersive components.")


if __name__ == "__main__":
    main()
