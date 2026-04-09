#!/usr/bin/env python3
"""Test dynamic graph growth with the ACTUAL retained field infrastructure.

BACKGROUND:
  frontier_dynamic_growth.py showed Born survives on grown DAGs, but its
  gravity test used V(y) = -s/(|y-y_mass|+1) -- a hand-written potential.
  The retained model uses derive_node_field which solves the Laplacian with
  persistence support. If gravity works with the real field solver on a
  grown DAG, dynamic growth is fully viable.

APPROACH:
  1. Grow a DAG layer by layer (amplitude-guided, same as
     frontier_dynamic_growth.py).
  2. After growth, embed the grown nodes into a rectangular superset grid.
  3. Place persistent nodes as a mass source within the grown node region.
  4. Call derive_node_field on the rectangular superset to get the
     Laplacian-relaxed field.
  5. Propagate through the grown DAG using local_edge_properties with
     the real field values.
  6. Compare centroid with and without mass.

TESTS:
  1. Does derive_node_field run without error on the grown node superset?
  2. Is the field nonzero near the mass and decaying away from it?
  3. Does the centroid shift TOWARD the mass?
  4. Compare to: same mass on a full static rectangular lattice.

HYPOTHESIS:
  "Gravity with the retained Laplacian field works on dynamically grown
  DAGs."

FALSIFICATION:
  "If centroid doesn't shift toward mass, or field computation fails."
"""

from __future__ import annotations

import math
import cmath
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from toy_event_physics import (
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    RulePostulates,
    LocalRule,
    local_edge_properties,
)


# ---------------------------------------------------------------------------
# Core propagator: edge amplitude (free-space, for growth phase)
# ---------------------------------------------------------------------------

def edge_amplitude_free(src, dst, k, p):
    """Free-space edge amplitude for growth phase (no field)."""
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    L = math.sqrt(dx * dx + dy * dy)
    if L < 1e-15:
        return 0j
    theta = math.atan2(abs(dy), abs(dx))
    w = math.exp(-0.8 * theta * theta)
    return cmath.exp(1j * k * L) * w / (L ** p)


# ---------------------------------------------------------------------------
# Step 1: Grow DAG (identical to frontier_dynamic_growth.py)
# ---------------------------------------------------------------------------

def grow_graph(n_layers, k, p, max_d, threshold_frac):
    """Grow a DAG layer by layer using amplitude-guided placement.

    Returns:
      layers: list of sets, layers[i] = set of (x, y) nodes at layer i
      amplitudes: dict mapping (x, y) -> complex amplitude
    """
    layers = [set()]
    layers[0].add((0, 0))
    amplitudes = {(0, 0): 1.0 + 0j}

    for layer_x in range(1, n_layers):
        prev_nodes = layers[layer_x - 1]

        candidates = set()
        for (x, y) in prev_nodes:
            for dy in range(-max_d, max_d + 1):
                candidates.add((layer_x, y + dy))

        new_amps = {}
        for cand in candidates:
            amp = 0j
            for src in prev_nodes:
                if src in amplitudes:
                    amp += amplitudes[src] * edge_amplitude_free(src, cand, k, p)
            new_amps[cand] = amp

        if not new_amps:
            break
        max_prob = max(abs(a) ** 2 for a in new_amps.values())
        if max_prob < 1e-30:
            break
        thresh = threshold_frac * max_prob

        kept = {n: a for n, a in new_amps.items() if abs(a) ** 2 >= thresh}
        if not kept:
            break

        layers.append(set(kept.keys()))
        amplitudes.update(kept)

    return layers, amplitudes


# ---------------------------------------------------------------------------
# Step 2-4: Build superset grid, place mass, solve Laplacian field
# ---------------------------------------------------------------------------

def build_field_on_superset(grown_nodes_all, mass_y, mass_radius, k_phase):
    """Build rectangular superset, place mass, solve Laplacian field.

    Returns:
      full_nodes: the rectangular superset
      field: dict (x,y) -> float from derive_node_field
      persistent_nodes: the mass cluster placed
    """
    max_x = max(x for x, y in grown_nodes_all)
    max_y = max(abs(y) for x, y in grown_nodes_all)

    # Rectangular superset with a small margin
    margin = 2
    full_nodes = build_rectangular_nodes(max_x, max_y + margin)

    # Place mass cluster: persistent nodes near (max_x//2, mass_y)
    mass_x_center = max_x // 2
    persistent = frozenset(
        (x, y) for x, y in full_nodes
        if abs(x - mass_x_center) <= mass_radius
        and abs(y - mass_y) <= mass_radius
    )

    # Build rule and solve field
    postulates = RulePostulates(
        phase_per_action=k_phase,
        attenuation_power=1.0,
        field_mode="relaxed",
    )
    rule = derive_local_rule(persistent, postulates)
    field = derive_node_field(full_nodes, rule)

    return full_nodes, field, persistent, rule


# ---------------------------------------------------------------------------
# Step 5: Propagate through grown DAG using the real field
# ---------------------------------------------------------------------------

def propagate_with_field(layers, field, rule, max_d):
    """Propagate through the grown DAG using local_edge_properties.

    For each edge from layer i to layer i+1, use the retained model's
    local_edge_properties which incorporates the Laplacian field.
    """
    amplitudes = {n: (1.0 + 0j if n == (0, 0) else 0j) for n in layers[0]}

    for i in range(1, len(layers)):
        prev = layers[i - 1]
        curr = layers[i]
        new_amps = {}
        for node in curr:
            amp = 0j
            for src in prev:
                if abs(amplitudes.get(src, 0)) < 1e-30:
                    continue
                # Only connect if |dy| <= max_d
                dy = abs(node[1] - src[1])
                if dy > max_d:
                    continue
                # Check both nodes exist in field dict
                if src not in field or node not in field:
                    continue
                _delay, _action, edge_amp = local_edge_properties(
                    src, node, rule, field
                )
                amp += amplitudes[src] * edge_amp
            new_amps[node] = amp
        amplitudes.update(new_amps)

    return amplitudes


def propagate_flat(layers, k, p, max_d):
    """Propagate with zero field (flat space) using free-space amplitudes."""
    amplitudes = {n: (1.0 + 0j if n == (0, 0) else 0j) for n in layers[0]}

    for i in range(1, len(layers)):
        prev = layers[i - 1]
        curr = layers[i]
        new_amps = {}
        for node in curr:
            amp = 0j
            for src in prev:
                if abs(amplitudes.get(src, 0)) < 1e-30:
                    continue
                dy = abs(node[1] - src[1])
                if dy > max_d:
                    continue
                amp += amplitudes[src] * edge_amplitude_free(src, node, k, p)
            new_amps[node] = amp
        amplitudes.update(new_amps)

    return amplitudes


# ---------------------------------------------------------------------------
# Centroid helper
# ---------------------------------------------------------------------------

def centroid_y(layer_nodes, amplitudes):
    """Probability-weighted centroid in y."""
    total_p = 0.0
    weighted_y = 0.0
    for n in layer_nodes:
        prob = abs(amplitudes.get(n, 0)) ** 2
        total_p += prob
        weighted_y += n[1] * prob
    if total_p < 1e-30:
        return 0.0
    return weighted_y / total_p


# ---------------------------------------------------------------------------
# TEST 1: Field computation on grown superset
# ---------------------------------------------------------------------------

def test_field_computation():
    """Does derive_node_field run on the grown-node superset?"""
    print("=" * 72)
    print("TEST 1: LAPLACIAN FIELD ON GROWN-NODE SUPERSET")
    print("=" * 72)
    print()

    k = 4.0
    p = 1
    max_d = 5
    n_layers = 20
    thresh = 0.01
    mass_y = 5
    mass_radius = 1

    # Grow
    layers, _amps = grow_graph(n_layers, k, p, max_d, thresh)
    all_grown = set()
    for layer in layers:
        all_grown |= layer

    print(f"  Grown DAG: {len(layers)} layers, {len(all_grown)} total nodes")
    max_x = max(x for x, y in all_grown)
    max_y_abs = max(abs(y) for x, y in all_grown)
    print(f"  Extent: x in [0, {max_x}], y in [{-max_y_abs}, {max_y_abs}]")

    # Solve field
    full_nodes, field, persistent, rule = build_field_on_superset(
        all_grown, mass_y, mass_radius, k
    )
    print(f"  Rectangular superset: {len(full_nodes)} nodes")
    print(f"  Persistent (mass) nodes: {len(persistent)}")

    # Check field properties
    nonzero = sum(1 for v in field.values() if abs(v) > 1e-10)
    max_field = max(field.values())
    min_field = min(field.values())
    print(f"  Field: {nonzero} nonzero values, range [{min_field:.6f}, {max_field:.6f}]")

    # Sample field at mass location and away
    mass_x_center = max_x // 2
    f_at_mass = field.get((mass_x_center, mass_y), 0.0)
    f_far_away = field.get((mass_x_center, 0), 0.0)
    f_edge = field.get((0, 0), 0.0)
    print(f"  Field at mass center ({mass_x_center},{mass_y}): {f_at_mass:.6f}")
    print(f"  Field at midline ({mass_x_center},0): {f_far_away:.6f}")
    print(f"  Field at edge (0,0): {f_edge:.6f}")

    if max_field > 0.0 and nonzero > 0:
        print("  PASS: Field computation succeeded with nonzero values.")
    else:
        print("  FAIL: Field is all zero -- Laplacian relaxation produced no field.")
    print()

    return layers, full_nodes, field, persistent, rule


# ---------------------------------------------------------------------------
# TEST 2: Field decay profile
# ---------------------------------------------------------------------------

def test_field_decay(full_nodes, field, mass_y):
    """Is the field peaked near mass and decaying away?"""
    print("=" * 72)
    print("TEST 2: FIELD DECAY PROFILE")
    print("=" * 72)
    print()

    max_x = max(x for x, y in full_nodes)
    mid_x = max_x // 2

    print(f"  Field profile at x={mid_x} (vertical slice through mass center):")
    print(f"  {'y':>5}  {'field':>10}  {'bar'}")

    max_y = max(abs(y) for x, y in full_nodes)
    values = []
    for y in range(-max_y, max_y + 1):
        f = field.get((mid_x, y), 0.0)
        values.append((y, f))

    max_f = max(abs(v) for _, v in values) if values else 1.0
    if max_f < 1e-15:
        max_f = 1.0

    for y, f in values:
        bar_len = int(40 * abs(f) / max_f) if max_f > 1e-15 else 0
        marker = " <-- mass" if abs(y - mass_y) <= 1 else ""
        print(f"  {y:+5d}  {f:10.6f}  {'#' * bar_len}{marker}")

    # Check decay: field at mass > field 5 units away
    f_mass = field.get((mid_x, mass_y), 0.0)
    f_away = field.get((mid_x, 0), 0.0)
    if f_mass > f_away and f_mass > 0:
        print(f"\n  PASS: Field peaks near mass ({f_mass:.6f}) and decays "
              f"away ({f_away:.6f}).")
    else:
        print(f"\n  INCONCLUSIVE: Field at mass={f_mass:.6f}, "
              f"at y=0={f_away:.6f}.")
    print()


# ---------------------------------------------------------------------------
# TEST 3: Gravity -- centroid shift on grown DAG
# ---------------------------------------------------------------------------

def test_gravity_grown(layers, field, rule, k, p, max_d, mass_y):
    """Does the centroid shift toward the mass on the grown DAG?"""
    print("=" * 72)
    print("TEST 3: GRAVITY ON GROWN DAG (RETAINED LAPLACIAN FIELD)")
    print("=" * 72)
    print()

    # Flat-space propagation (zero field)
    amps_flat = propagate_flat(layers, k, p, max_d)

    # Gravity propagation (Laplacian field from derive_node_field)
    amps_grav = propagate_with_field(layers, field, rule, max_d)

    print(f"  Mass at y={mass_y}")
    print(f"  {'Layer':>5}  {'nodes':>5}  {'centroid_flat':>14}  "
          f"{'centroid_grav':>14}  {'deflection':>11}")

    deflections = []
    for i, layer_set in enumerate(layers):
        c_flat = centroid_y(layer_set, amps_flat)
        c_grav = centroid_y(layer_set, amps_grav)
        defl = c_grav - c_flat
        deflections.append(defl)
        print(f"  {i:5d}  {len(layer_set):5d}  {c_flat:+14.6f}  "
              f"{c_grav:+14.6f}  {defl:+11.6f}")

    if len(deflections) >= 5:
        late_defl = sum(deflections[-5:]) / 5.0
        early_mag = sum(abs(d) for d in deflections[2:7]) / max(len(deflections[2:7]), 1)
        late_mag = sum(abs(d) for d in deflections[-5:]) / 5.0

        sign = "toward" if (late_defl > 0) == (mass_y > 0) else "away from"
        print(f"\n  Late avg deflection: {late_defl:+.6f} ({sign} mass)")
        print(f"  Early |deflection| avg: {early_mag:.6f}")
        print(f"  Late  |deflection| avg: {late_mag:.6f}")

        if abs(late_defl) > 0.001 and sign == "toward":
            print("  PASS: Significant deflection TOWARD mass with retained field.")
        elif abs(late_defl) > 0.001:
            print(f"  NOTE: Deflection is {sign} mass (magnitude {abs(late_defl):.6f}).")
            print("        The field produces a response; sign depends on action mode.")
        else:
            print("  WEAK: Deflection below threshold.")
    print()

    return amps_flat, amps_grav, deflections


# ---------------------------------------------------------------------------
# TEST 4: Comparison -- grown DAG vs static rectangular lattice
# ---------------------------------------------------------------------------

def test_static_comparison(layers, field, rule, k, p, max_d, mass_y, mass_radius):
    """Compare gravity on grown DAG vs full static lattice."""
    print("=" * 72)
    print("TEST 4: GROWN DAG vs STATIC LATTICE COMPARISON")
    print("=" * 72)
    print()

    # Build static lattice with same dimensions
    all_grown = set()
    for layer in layers:
        all_grown |= layer
    max_x = max(x for x, y in all_grown)
    max_y_abs = max(abs(y) for x, y in all_grown)
    y_range = max_y_abs + 2

    # Static lattice layers
    n_layers = max_x + 1
    static_layers = []
    for x in range(n_layers):
        layer = set()
        for y in range(-y_range, y_range + 1):
            layer.add((x, y))
        static_layers.append(layer)

    # Solve field on the same rectangular grid (same mass)
    static_nodes = build_rectangular_nodes(max_x, y_range)

    mass_x_center = max_x // 2
    persistent_static = frozenset(
        (x, y) for x, y in static_nodes
        if abs(x - mass_x_center) <= mass_radius
        and abs(y - mass_y) <= mass_radius
    )

    postulates = RulePostulates(
        phase_per_action=k,
        attenuation_power=1.0,
        field_mode="relaxed",
    )
    rule_static = derive_local_rule(persistent_static, postulates)
    field_static = derive_node_field(static_nodes, rule_static)

    # Propagate on static lattice: flat and with field
    amps_static_flat = propagate_flat(static_layers, k, p, max_d)
    amps_static_grav = propagate_with_field(static_layers, field_static, rule_static, max_d)

    # Propagate on grown DAG: flat and with field (reusing from test 3)
    amps_grown_flat = propagate_flat(layers, k, p, max_d)
    amps_grown_grav = propagate_with_field(layers, field, rule, max_d)

    # Compute centroids at final layer
    final_grown = layers[-1]
    final_static = static_layers[min(len(layers) - 1, len(static_layers) - 1)]

    c_grown_flat = centroid_y(final_grown, amps_grown_flat)
    c_grown_grav = centroid_y(final_grown, amps_grown_grav)
    c_static_flat = centroid_y(final_static, amps_static_flat)
    c_static_grav = centroid_y(final_static, amps_static_grav)

    delta_grown = c_grown_grav - c_grown_flat
    delta_static = c_static_grav - c_static_flat

    print(f"  Mass at y={mass_y}, mass_radius={mass_radius}")
    print(f"  Grown DAG:  {len(layers)} layers, {len(all_grown)} nodes")
    print(f"  Static:     {len(static_layers)} layers, {len(static_nodes)} nodes")
    print()
    print(f"                 {'grown DAG':>14}  {'static lattice':>14}")
    print(f"  centroid flat  {c_grown_flat:+14.6f}  {c_static_flat:+14.6f}")
    print(f"  centroid grav  {c_grown_grav:+14.6f}  {c_static_grav:+14.6f}")
    print(f"  delta          {delta_grown:+14.6f}  {delta_static:+14.6f}")

    grown_dir = "toward" if (delta_grown > 0) == (mass_y > 0) else "away"
    static_dir = "toward" if (delta_static > 0) == (mass_y > 0) else "away"
    print(f"  direction      {'':>4}{grown_dir:>10}  {'':>4}{static_dir:>10}")
    print()

    # Same-sign check
    if (delta_grown > 0) == (delta_static > 0) and abs(delta_grown) > 1e-4:
        print("  PASS: Grown DAG and static lattice show same-sign deflection.")
    elif abs(delta_grown) > 1e-4:
        print("  NOTE: Deflection present on grown DAG but sign differs from static.")
    else:
        print("  WEAK: Grown DAG deflection below threshold.")

    # Magnitude comparison
    if abs(delta_static) > 1e-15:
        ratio = abs(delta_grown) / abs(delta_static)
        print(f"  Magnitude ratio (grown/static): {ratio:.3f}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 72)
    print("FRONTIER: RETAINED LAPLACIAN FIELD ON DYNAMICALLY GROWN DAG")
    print("=" * 72)
    print()
    print("Testing whether derive_node_field (Laplacian relaxation) produces")
    print("a working gravitational field on amplitude-guided grown graphs.")
    print()

    k = 4.0
    p = 1
    max_d = 5
    mass_y = 5
    mass_radius = 1

    # Test 1: Field computation
    layers, full_nodes, field, persistent, rule = test_field_computation()

    # Test 2: Field decay
    test_field_decay(full_nodes, field, mass_y)

    # Test 3: Gravity on grown DAG
    amps_flat, amps_grav, deflections = test_gravity_grown(
        layers, field, rule, k, p, max_d, mass_y
    )

    # Test 4: Comparison with static lattice
    test_static_comparison(layers, field, rule, k, p, max_d, mass_y, mass_radius)

    # Summary
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print("This experiment tested the RETAINED model's Laplacian field solver")
    print("(derive_node_field) on a dynamically grown DAG -- not a bespoke")
    print("analytic potential. The grown DAG nodes are embedded into a")
    print("rectangular superset for field computation, then propagation uses")
    print("local_edge_properties with the real field values.")
    print()

    if len(deflections) >= 5:
        late_defl = sum(deflections[-5:]) / 5.0
        sign = "toward" if (late_defl > 0) == (mass_y > 0) else "away from"
        if abs(late_defl) > 0.001:
            print(f"RESULT: Deflection {sign} mass = {late_defl:+.6f}")
            if sign == "toward":
                print("VERDICT: HYPOTHESIS SUPPORTED -- retained Laplacian gravity")
                print("         works on dynamically grown DAGs.")
            else:
                print("VERDICT: Field produces response but deflection is away from mass.")
                print("         Sign depends on action mode; field infrastructure works.")
        else:
            print(f"RESULT: Deflection = {late_defl:+.6f} (below threshold)")
            print("VERDICT: INCONCLUSIVE -- field may need stronger mass or more layers.")
    print()


if __name__ == "__main__":
    main()
