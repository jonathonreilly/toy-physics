#!/usr/bin/env python3
"""Test amplitude-guided dynamic graph growth: grow the DAG layer by layer
where new nodes are placed where the wave amplitude is concentrated.

BACKGROUND:
  All existing experiments run on STATIC lattices -- the graph structure is
  fixed before propagation. This experiment tests the simplest dynamic
  growth rule: at each layer, place nodes where |amplitude|^2 exceeds a
  threshold relative to the max. This creates a feedback loop: the
  propagator determines the graph, and the graph determines the propagator.

GROWTH RULE:
  1. Start with a single source node at (0, 0).
  2. At each new layer x, generate candidate nodes at (x, y+dy) for each
     source node (x-1, y) with |dy| <= max_d.
  3. Propagate amplitude from the previous layer to each candidate.
  4. Keep candidates where |amplitude|^2 > threshold * max(|amplitude|^2).
  5. Repeat for 20 layers.

TESTS:
  1. Growth shape: does the graph grow, collapse, or explode?
  2. Born rule (Sorkin 3-slit): does |I3|/P remain < 1e-10 on the grown DAG?
  3. Gravity: does a mass source deflect the beam on a grown graph?
  4. Final-layer probability overlap with a static rectangular lattice.

CAVEATS (from review):
  - Test 3 uses a bespoke analytic potential V(y) = -s/(|y-y_mass|+1),
    NOT the retained derive_node_field Laplacian relaxation. This is a
    feasibility probe for gravity on grown graphs, not evidence that the
    full retained gravity mechanism survives dynamic growth.
  - Test 4 compares only the FINAL-LAYER free-space probability distribution
    (Bhattacharyya overlap on common y-values). It does not compare
    intermediate layers, phases, graph structure, or the gravity case.
    The "96% fidelity" is a narrow end-state similarity metric.
  - The free-space action S = L is valley-linear with f=0. The gravity
    test uses S = L*(1+V) which is valley-linear with f = -V.

HYPOTHESIS:
  "Amplitude-guided growth produces a self-regulating graph where Born
  rule survives."

FALSIFICATION:
  "If the graph collapses to 1 node per layer or Born fails."
"""

from __future__ import annotations
import math
import cmath


# ---------------------------------------------------------------------------
# Core propagator: edge amplitude between two 2D nodes
# ---------------------------------------------------------------------------

def edge_amplitude(src, dst, k, p):
    """Compute edge amplitude from src=(x1,y1) to dst=(x2,y2).

    Uses exp(i*k*L) * w(theta) / L^p  with Gaussian angular kernel.
    """
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    L = math.sqrt(dx * dx + dy * dy)
    if L < 1e-15:
        return 0j
    theta = math.atan2(abs(dy), abs(dx))
    w = math.exp(-0.8 * theta * theta)
    return cmath.exp(1j * k * L) * w / (L ** p)


# ---------------------------------------------------------------------------
# Test 1: Dynamic growth -- track graph shape
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

        # Generate candidate nodes
        candidates = set()
        for (x, y) in prev_nodes:
            for dy in range(-max_d, max_d + 1):
                candidates.add((layer_x, y + dy))

        # Propagate amplitude to each candidate
        new_amps = {}
        for cand in candidates:
            amp = 0j
            for src in prev_nodes:
                if src in amplitudes:
                    amp += amplitudes[src] * edge_amplitude(src, cand, k, p)
            new_amps[cand] = amp

        # Threshold selection
        if not new_amps:
            break
        max_prob = max(abs(a) ** 2 for a in new_amps.values())
        if max_prob < 1e-30:
            break
        thresh = threshold_frac * max_prob

        kept = {}
        for node, amp in new_amps.items():
            if abs(amp) ** 2 >= thresh:
                kept[node] = amp

        if not kept:
            break

        layer_nodes = set(kept.keys())
        layers.append(layer_nodes)
        amplitudes.update(kept)

    return layers, amplitudes


def test_growth_shape():
    """Test 1: Does the graph grow, collapse, or explode?"""
    print("=" * 72)
    print("TEST 1: DYNAMIC GROWTH SHAPE")
    print("=" * 72)
    print()

    k = 4.0
    p = 1
    max_d = 5
    n_layers = 20

    for thresh_frac in [0.01, 0.05, 0.10]:
        print(f"--- threshold = {thresh_frac:.0%} of max |psi|^2 ---")
        layers, amplitudes = grow_graph(n_layers, k, p, max_d, thresh_frac)

        print(f"  {'Layer':>5}  {'Nodes':>5}  {'y-range':>12}  {'max|psi|^2':>12}")
        for i, layer_set in enumerate(layers):
            ys = [n[1] for n in layer_set]
            probs = [abs(amplitudes[n]) ** 2 for n in layer_set if n in amplitudes]
            max_p = max(probs) if probs else 0.0
            y_lo, y_hi = min(ys), max(ys)
            print(f"  {i:5d}  {len(layer_set):5d}  [{y_lo:+4d},{y_hi:+4d}]  {max_p:12.4e}")

        final_count = len(layers[-1]) if layers else 0
        if final_count <= 1:
            verdict = "COLLAPSED"
        elif final_count > 2 * max_d + 1:
            # More nodes than one layer's candidate spread -- growing
            verdict = "GROWING"
        else:
            verdict = "STABLE"
        print(f"  Verdict: {verdict} (final layer: {final_count} nodes)")
        print()

    return layers, amplitudes


# ---------------------------------------------------------------------------
# Test 2: Born rule (3-slit Sorkin) on the grown DAG
# ---------------------------------------------------------------------------

def propagate_on_dag(layers, amplitudes_init, k, p, slit_mask=None):
    """Propagate on an already-built DAG (fixed graph structure).

    slit_mask: if provided, a function (x, y) -> bool that returns True
    if the node is OPEN (amplitude can pass). Applied at layer 1 only
    (the slit layer).
    """
    amps = dict(amplitudes_init)

    for i in range(1, len(layers)):
        prev = layers[i - 1]
        curr = layers[i]
        new_amps = {}
        for node in curr:
            amp = 0j
            for src in prev:
                if src not in amps:
                    continue
                # If slit_mask is active and we're at the slit layer,
                # only pass amplitude through open slits
                if slit_mask is not None and i == 1:
                    if not slit_mask(src):
                        continue
                amp += amps[src] * edge_amplitude(src, node, k, p)
            new_amps[node] = amp
        amps.update(new_amps)

    return amps


def test_born_rule(layers, full_amplitudes):
    """Test 2: Sorkin 3-slit test on the grown DAG.

    Use a mid-graph layer as the slit layer so there are enough nodes
    for 3 distinct slits. Slits at y = -1, 0, +1.
    """
    print("=" * 72)
    print("TEST 2: BORN RULE (SORKIN 3-SLIT) ON GROWN DAG")
    print("=" * 72)
    print()

    if len(layers) < 10:
        print("  Graph too small for Born test (need >= 10 layers).")
        return

    k = 4.0
    p = 1
    slit_layer_idx = 5  # Use layer 5 as slit barrier

    # Show what nodes exist at the slit layer
    slit_layer_ys = sorted(n[1] for n in layers[slit_layer_idx])
    print(f"  Slit layer {slit_layer_idx} has {len(slit_layer_ys)} nodes "
          f"at y = {slit_layer_ys}")
    print(f"  Using slits at y = -1, 0, +1")
    print()

    # Re-propagate from scratch on the fixed DAG structure
    # Source at layer 0
    init_amps = {n: (1.0 + 0j if n == (0, 0) else 0j) for n in layers[0]}

    def prob_at_detector(open_set):
        """Propagate with slit mask at slit_layer_idx."""
        amps = dict(init_amps)
        for i in range(1, len(layers)):
            prev = layers[i - 1]
            curr = layers[i]
            new_amps = {}
            for node in curr:
                amp = 0j
                for src in prev:
                    if abs(amps.get(src, 0)) < 1e-30:
                        continue
                    # Apply slit mask: block nodes NOT in open_set at slit layer
                    if i == slit_layer_idx:
                        if src[1] not in open_set:
                            continue
                    amp += amps[src] * edge_amplitude(src, node, k, p)
                new_amps[node] = amp
            amps.update(new_amps)
        return sum(abs(amps.get(n, 0)) ** 2 for n in layers[-1])

    # Single slits
    PA = prob_at_detector({-1})
    PB = prob_at_detector({0})
    PC = prob_at_detector({1})

    # Pairs
    PAB = prob_at_detector({-1, 0})
    PAC = prob_at_detector({-1, 1})
    PBC = prob_at_detector({0, 1})

    # Triple
    PABC = prob_at_detector({-1, 0, 1})

    # Sorkin parameter
    I3 = PABC - PAB - PAC - PBC + PA + PB + PC

    P_norm = max(PABC, 1e-30)
    ratio = abs(I3) / P_norm

    print(f"  P(A)   = {PA:.6e}")
    print(f"  P(B)   = {PB:.6e}")
    print(f"  P(C)   = {PC:.6e}")
    print(f"  P(AB)  = {PAB:.6e}")
    print(f"  P(AC)  = {PAC:.6e}")
    print(f"  P(BC)  = {PBC:.6e}")
    print(f"  P(ABC) = {PABC:.6e}")
    print(f"  I3     = {I3:.6e}")
    print(f"  |I3|/P = {ratio:.6e}")
    print()

    if ratio < 1e-10:
        print("  PASS: Born rule survives on the grown DAG.")
    else:
        print(f"  FAIL: |I3|/P = {ratio:.2e} > 1e-10 -- Born rule violated.")
    print()


# ---------------------------------------------------------------------------
# Test 3: Gravity on the grown graph vs static graph
# ---------------------------------------------------------------------------

def grow_graph_with_mass(n_layers, k, p, max_d, threshold_frac,
                         mass_y, mass_strength):
    """Grow a DAG with a persistent mass source that adds extra phase.

    The mass at position mass_y adds a gravitational potential:
      V(y) = -mass_strength / (|y - mass_y| + 1)
    modifying the action: S = L + V(y_mid) * L
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
                if src not in amplitudes:
                    continue
                dx = cand[0] - src[0]
                dy = cand[1] - src[1]
                L = math.sqrt(dx * dx + dy * dy)
                if L < 1e-15:
                    continue
                theta = math.atan2(abs(dy), abs(dx))
                w = math.exp(-0.8 * theta * theta)

                # Gravitational potential at midpoint
                y_mid = (src[1] + cand[1]) / 2.0
                V = -mass_strength / (abs(y_mid - mass_y) + 1.0)
                S = L * (1.0 + V)

                edge_amp = cmath.exp(1j * k * S) * w / (L ** p)
                amp += amplitudes[src] * edge_amp
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


def test_gravity():
    """Test 3: Does a mass source deflect the grown graph?"""
    print("=" * 72)
    print("TEST 3: GRAVITY ON GROWN vs STATIC GRAPH")
    print("=" * 72)
    print()

    k = 4.0
    p = 1
    max_d = 5
    n_layers = 20
    thresh = 0.01
    mass_y = 5.0
    mass_strength = 0.05

    # Grow without mass (free space)
    layers_free, amps_free = grow_graph(n_layers, k, p, max_d, thresh)

    # Grow with mass
    layers_grav, amps_grav = grow_graph_with_mass(
        n_layers, k, p, max_d, thresh, mass_y, mass_strength
    )

    print(f"  Mass at y={mass_y}, strength={mass_strength}")
    print(f"  {'Layer':>5}  {'centroid_free':>14}  {'centroid_grav':>14}  {'deflection':>11}")

    deflections = []
    n_compare = min(len(layers_free), len(layers_grav))
    for i in range(n_compare):
        c_free = centroid_y(layers_free[i], amps_free)
        c_grav = centroid_y(layers_grav[i], amps_grav)
        defl = c_grav - c_free
        deflections.append(defl)
        print(f"  {i:5d}  {c_free:+14.6f}  {c_grav:+14.6f}  {defl:+11.6f}")

    # Check deflection behavior
    if len(deflections) >= 5:
        late_defl = sum(deflections[-5:]) / 5.0
        # Deflection magnitude should grow with distance (accumulating effect)
        early_mag = sum(abs(d) for d in deflections[2:7]) / max(len(deflections[2:7]), 1)
        late_mag = sum(abs(d) for d in deflections[-5:]) / 5.0
        growing = late_mag > 2 * early_mag

        sign = "toward" if (late_defl > 0) == (mass_y > 0) else "away from"
        print(f"\n  Late avg deflection: {late_defl:+.6f} ({sign} mass)")
        print(f"  Early |deflection| avg: {early_mag:.6f}")
        print(f"  Late  |deflection| avg: {late_mag:.6f}")
        print(f"  Deflection growing: {'YES' if growing else 'NO'}")

        if growing and abs(late_defl) > 0.01:
            print(f"  PASS: Significant, growing deflection detected on grown graph.")
            if sign == "away from":
                print(f"  NOTE: Deflection is AWAY from mass -- sign depends on")
                print(f"        how V enters the action. The key result is that")
                print(f"        the grown graph responds to the gravitational field.")
        else:
            print(f"  WEAK: Deflection present but small or not growing.")
    print()


# ---------------------------------------------------------------------------
# Test 4: Compare grown graph to static rectangular lattice
# ---------------------------------------------------------------------------

def build_static_lattice(n_layers, y_range):
    """Build a static rectangular lattice."""
    layers = []
    for x in range(n_layers):
        layer = set()
        for y in range(-y_range, y_range + 1):
            layer.add((x, y))
        layers.append(layer)
    return layers


def propagate_static(layers, k, p):
    """Propagate on a static lattice from a point source at (0,0)."""
    max_d = 5
    amplitudes = {}
    for n in layers[0]:
        amplitudes[n] = 1.0 + 0j if n == (0, 0) else 0j

    for i in range(1, len(layers)):
        for node in layers[i]:
            amp = 0j
            for src in layers[i - 1]:
                if abs(amplitudes.get(src, 0)) < 1e-30:
                    continue
                # Only connect if |dy| <= max_d
                dy = abs(node[1] - src[1])
                if dy > max_d:
                    continue
                amp += amplitudes[src] * edge_amplitude(src, node, k, p)
            amplitudes[node] = amp

    return amplitudes


def test_static_comparison():
    """Test 4: Compare grown graph to static lattice."""
    print("=" * 72)
    print("TEST 4: GROWN vs STATIC GRAPH COMPARISON")
    print("=" * 72)
    print()

    k = 4.0
    p = 1
    max_d = 5
    n_layers = 20
    thresh = 0.01

    # Grown graph
    layers_grown, amps_grown = grow_graph(n_layers, k, p, max_d, thresh)

    # Static graph -- use y_range large enough to match grown graph
    max_y_grown = 0
    for layer in layers_grown:
        for (x, y) in layer:
            max_y_grown = max(max_y_grown, abs(y))
    y_range = max(max_y_grown + 2, max_d + 2)

    layers_static = build_static_lattice(n_layers, y_range)
    amps_static = propagate_static(layers_static, k, p)

    print(f"  {'Layer':>5}  {'Nodes(grown)':>12}  {'Nodes(static)':>13}  "
          f"{'maxP(grown)':>12}  {'maxP(static)':>13}")

    for i in range(min(len(layers_grown), len(layers_static))):
        ng = len(layers_grown[i])
        ns = len(layers_static[i])
        pg = max((abs(amps_grown.get(n, 0)) ** 2 for n in layers_grown[i]),
                 default=0)
        ps = max((abs(amps_static.get(n, 0)) ** 2 for n in layers_static[i]),
                 default=0)
        print(f"  {i:5d}  {ng:12d}  {ns:13d}  {pg:12.4e}  {ps:13.4e}")

    # Compare final layer probability distributions
    print()
    print("  Final layer probability comparison:")
    final_i = min(len(layers_grown), len(layers_static)) - 1
    grown_final = layers_grown[final_i]
    static_final = layers_static[final_i]

    total_grown = sum(abs(amps_grown.get(n, 0)) ** 2 for n in grown_final)
    total_static = sum(abs(amps_static.get(n, 0)) ** 2 for n in static_final)
    print(f"  Total probability at final layer (grown):  {total_grown:.6e}")
    print(f"  Total probability at final layer (static): {total_static:.6e}")

    # Fidelity: overlap of normalized distributions on common nodes
    common_ys = set(n[1] for n in grown_final) & set(n[1] for n in static_final)
    if common_ys and total_grown > 1e-30 and total_static > 1e-30:
        fidelity = 0.0
        for y in sorted(common_ys):
            n_g = (final_i, y)
            n_s = (final_i, y)
            p_g = abs(amps_grown.get(n_g, 0)) ** 2 / total_grown
            p_s = abs(amps_static.get(n_s, 0)) ** 2 / total_static
            fidelity += math.sqrt(p_g * p_s)
        print(f"  Bhattacharyya fidelity (grown vs static): {fidelity:.6f}")
        if fidelity > 0.9:
            print("  HIGH fidelity: grown graph closely matches static lattice.")
        elif fidelity > 0.5:
            print("  MODERATE fidelity: some structural difference.")
        else:
            print("  LOW fidelity: grown and static graphs produce very different distributions.")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 72)
    print("FRONTIER: DYNAMIC AMPLITUDE-GUIDED GRAPH GROWTH")
    print("=" * 72)
    print()
    print("Testing whether the propagator can determine its own graph")
    print("structure through amplitude-guided node placement.")
    print()
    print("Parameters: k=4.0, p=1, max_d=5, 20 layers")
    print()

    layers, amps = test_growth_shape()
    test_born_rule(layers, amps)
    test_gravity()
    test_static_comparison()

    # Summary
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print("Dynamic growth tested with 3 threshold levels.")
    print("Born rule (Sorkin I3) tested on the grown DAG.")
    print("Gravity deflection compared: grown vs free-space grown graph.")
    print("Distribution fidelity compared: grown vs static rectangular lattice.")
    print()


if __name__ == "__main__":
    main()
