#!/usr/bin/env python3
"""
frontier_chiral_growth.py
=========================
Does amplitude-guided growth work on the chiral walk?

Grow a chiral lattice layer-by-layer using the coin+shift structure,
keeping only sites where total probability exceeds a threshold fraction
of the max probability at that layer.

Tests:
1. Growth shape (nodes per layer, y-range)
2. Born rule (3-slit Sorkin I_3 on grown graph)
3. Gravity (localized phase field on grown graph)
4. Comparison to static lattice (Bhattacharyya overlap)

HYPOTHESIS: Chiral growth is self-regulating and Born-compliant.
FALSIFICATION: Graph collapses to 1 site or Born I_3 > 1e-6.
"""

import numpy as np
from math import cos, sin, sqrt, pi

# ── Parameters ──────────────────────────────────────────────────────
N_LAYERS = 20
N_Y_MAX = 80           # large enough y-space
THETA_0 = 0.3          # coin angle
THRESHOLD = 0.05       # keep sites with prob > threshold * max_prob
GRAV_STRENGTH = 5e-4   # gravity coupling
MASS_OFFSET = 4        # mass position offset from center


def grow_chiral(n_layers, n_y_max, theta_0, threshold, phase_field=None):
    """
    Grow chiral lattice layer by layer.

    phase_field: if provided, dict mapping y -> extra phase applied after coin.

    Returns (layers, psi) where layers[t] is set of active y-sites at layer t,
    psi is the 2*n_y_max complex array at the final layer.
    """
    center = n_y_max // 2
    layers = [set()]
    layers[0].add(center)

    # psi[2*y] = psi_+, psi[2*y+1] = psi_-
    psi = np.zeros(2 * n_y_max, dtype=complex)
    psi[2 * center] = 1.0  # psi_+ at center

    for t in range(n_layers):
        active = layers[t]

        # Coin at active sites
        for y in active:
            ip, im = 2 * y, 2 * y + 1
            pp, pm = psi[ip], psi[im]
            psi[ip] = cos(theta_0) * pp - sin(theta_0) * pm
            psi[im] = sin(theta_0) * pp + cos(theta_0) * pm

        # Optional phase field (gravity)
        if phase_field is not None:
            for y in active:
                phi = phase_field.get(y, 0.0)
                if phi != 0.0:
                    phase = np.exp(1j * phi)
                    psi[2 * y] *= phase
                    psi[2 * y + 1] *= phase

        # Shift: psi_+ -> y+1, psi_- -> y-1
        new_psi = np.zeros_like(psi)
        candidates = set()
        for y in active:
            # psi_+ shifts right
            if y + 1 < n_y_max:
                new_psi[2 * (y + 1)] += psi[2 * y]
                candidates.add(y + 1)
            # psi_- shifts left
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
                candidates.add(y - 1)

        # Threshold on total probability
        probs = {}
        for y in candidates:
            probs[y] = abs(new_psi[2 * y])**2 + abs(new_psi[2 * y + 1])**2

        max_prob = max(probs.values()) if probs else 0
        if max_prob == 0:
            layers.append(set())
            psi = new_psi
            continue

        next_layer = {y for y, p in probs.items() if p > threshold * max_prob}

        # Zero out pruned sites
        for y in candidates:
            if y not in next_layer:
                new_psi[2 * y] = 0
                new_psi[2 * y + 1] = 0

        psi = new_psi
        layers.append(next_layer)

    return layers, psi


def prob_distribution(psi, sites, n_y_max):
    """Extract probability distribution over given sites."""
    probs = {}
    for y in sites:
        probs[y] = abs(psi[2 * y])**2 + abs(psi[2 * y + 1])**2
    return probs


def normalize_dist(probs):
    """Normalize a probability dict to sum to 1."""
    total = sum(probs.values())
    if total == 0:
        return probs
    return {y: p / total for y, p in probs.items()}


def bhattacharyya_overlap(p1, p2):
    """Bhattacharyya coefficient between two distributions (dicts)."""
    all_keys = set(p1.keys()) | set(p2.keys())
    bc = 0.0
    for k in all_keys:
        bc += sqrt(p1.get(k, 0.0) * p2.get(k, 0.0))
    return bc


def run_on_grown_graph(layers, theta_0, barrier_layer, slit_set, n_y_max,
                       phase_field=None):
    """
    Run chiral walk on the grown graph with optional barrier.

    barrier_layer: layer index where barrier is placed
    slit_set: set of y-positions that are open (None = no barrier)

    Returns psi at final layer.
    """
    center = n_y_max // 2
    psi = np.zeros(2 * n_y_max, dtype=complex)
    psi[2 * center] = 1.0

    n_layers = len(layers) - 1
    for t in range(n_layers):
        active = layers[t]

        # Coin
        for y in active:
            ip, im = 2 * y, 2 * y + 1
            pp, pm = psi[ip], psi[im]
            psi[ip] = cos(theta_0) * pp - sin(theta_0) * pm
            psi[im] = sin(theta_0) * pp + cos(theta_0) * pm

        # Phase field
        if phase_field is not None:
            for y in active:
                phi = phase_field.get(y, 0.0)
                if phi != 0.0:
                    phase = np.exp(1j * phi)
                    psi[2 * y] *= phase
                    psi[2 * y + 1] *= phase

        # Shift
        new_psi = np.zeros_like(psi)
        next_active = layers[t + 1]
        for y in active:
            if y + 1 < n_y_max and (y + 1) in next_active:
                new_psi[2 * (y + 1)] += psi[2 * y]
            if y - 1 >= 0 and (y - 1) in next_active:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]

        # Barrier absorption
        if slit_set is not None and t + 1 == barrier_layer:
            for y in next_active:
                if y not in slit_set:
                    new_psi[2 * y] = 0
                    new_psi[2 * y + 1] = 0

        psi = new_psi

    return psi


def sorkin_test(layers, theta_0, n_y_max):
    """
    3-slit Sorkin test on the grown graph.

    Barrier at layer n_layers//3, pick 3 existing sites as slits.
    Measure I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C.
    """
    n_layers = len(layers) - 1
    barrier_layer = n_layers // 3
    barrier_sites = sorted(layers[barrier_layer])

    if len(barrier_sites) < 3:
        return None, barrier_sites, "Too few sites at barrier layer"

    # Pick 3 slits: left, center, right of barrier
    n = len(barrier_sites)
    slit_A = barrier_sites[0]
    slit_B = barrier_sites[n // 2]
    slit_C = barrier_sites[-1]
    slits = [slit_A, slit_B, slit_C]

    final_layer = layers[-1]

    def get_dist(open_slits):
        slit_set = set(open_slits)
        psi = run_on_grown_graph(layers, theta_0, barrier_layer, slit_set, n_y_max)
        probs = prob_distribution(psi, final_layer, n_y_max)
        return probs

    # All combinations
    P_ABC = get_dist([slit_A, slit_B, slit_C])
    P_AB = get_dist([slit_A, slit_B])
    P_AC = get_dist([slit_A, slit_C])
    P_BC = get_dist([slit_B, slit_C])
    P_A = get_dist([slit_A])
    P_B = get_dist([slit_B])
    P_C = get_dist([slit_C])

    # I_3 at each final-layer site
    I3_vals = []
    for y in sorted(final_layer):
        val = (P_ABC.get(y, 0) - P_AB.get(y, 0) - P_AC.get(y, 0) - P_BC.get(y, 0)
               + P_A.get(y, 0) + P_B.get(y, 0) + P_C.get(y, 0))
        I3_vals.append(val)

    I3_max = max(abs(v) for v in I3_vals) if I3_vals else 0
    I3_sum = sum(abs(v) for v in I3_vals)

    return I3_max, slits, I3_sum


def gravity_test(layers, theta_0, n_y_max, strength, mass_y):
    """
    Run with and without gravity, compare distributions.

    Gravity: phase_field[y] = -strength / (1 + |y - mass_y|)
    """
    # No gravity
    psi_flat = run_on_grown_graph(layers, theta_0, None, None, n_y_max)
    final_layer = layers[-1]
    dist_flat = normalize_dist(prob_distribution(psi_flat, final_layer, n_y_max))

    # With gravity
    phase_field = {}
    for t in range(len(layers)):
        for y in layers[t]:
            phase_field[y] = -strength / (1.0 + abs(y - mass_y))

    psi_grav = run_on_grown_graph(layers, theta_0, None, None, n_y_max,
                                   phase_field=phase_field)
    dist_grav = normalize_dist(prob_distribution(psi_grav, final_layer, n_y_max))

    # Center of mass shift
    def com(dist):
        total = sum(dist.values())
        if total == 0:
            return 0
        return sum(y * p for y, p in dist.items()) / total

    com_flat = com(dist_flat)
    com_grav = com(dist_grav)
    shift = com_grav - com_flat
    toward = (shift > 0) == (mass_y > n_y_max // 2)

    bc = bhattacharyya_overlap(dist_flat, dist_grav)

    return com_flat, com_grav, shift, toward, bc


def static_comparison(n_layers, n_y_max, theta_0, grown_layers):
    """
    Run chiral walk on full static lattice, compare to grown graph.
    """
    center = n_y_max // 2

    # Static: all sites available at every layer
    static_layers = []
    for t in range(n_layers + 1):
        # Static lattice has all sites from center-t to center+t
        layer_set = set(range(max(0, center - t), min(n_y_max, center + t + 1)))
        static_layers.append(layer_set)

    # Run on static
    psi_static = run_on_grown_graph(static_layers, theta_0, None, None, n_y_max)
    dist_static = normalize_dist(
        prob_distribution(psi_static, static_layers[-1], n_y_max))

    # Run on grown
    psi_grown = run_on_grown_graph(grown_layers, theta_0, None, None, n_y_max)
    dist_grown = normalize_dist(
        prob_distribution(psi_grown, grown_layers[-1], n_y_max))

    bc = bhattacharyya_overlap(dist_static, dist_grown)
    return bc, dist_static, dist_grown


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("FRONTIER: Chiral Growth — Amplitude-Guided DAG Construction")
    print("=" * 70)
    print(f"Parameters: n_layers={N_LAYERS}, theta_0={THETA_0}, "
          f"threshold={THRESHOLD}")
    print(f"            n_y_max={N_Y_MAX}, grav_strength={GRAV_STRENGTH}")
    print()

    # ── Test 1: Growth Shape ────────────────────────────────────────
    print("TEST 1: Growth Shape")
    print("-" * 50)

    layers, psi_final = grow_chiral(N_LAYERS, N_Y_MAX, THETA_0, THRESHOLD)

    center = N_Y_MAX // 2
    total_nodes = 0
    for t in range(N_LAYERS + 1):
        sites = sorted(layers[t])
        n = len(sites)
        total_nodes += n
        y_min = min(sites) - center if sites else 0
        y_max = max(sites) - center if sites else 0
        # Total probability at this layer
        if t == N_LAYERS:
            prob_total = sum(abs(psi_final[2*y])**2 + abs(psi_final[2*y+1])**2
                             for y in sites)
        else:
            prob_total = None

        extra = f"  prob={prob_total:.6f}" if prob_total is not None else ""
        print(f"  layer {t:3d}: {n:3d} sites, y in [{y_min:+d}, {y_max:+d}]{extra}")

    final_sites = len(layers[-1])
    print(f"\n  Total nodes across all layers: {total_nodes}")
    print(f"  Final layer sites: {final_sites}")

    # Check self-regulation
    collapsed = final_sites <= 1
    grew_unbounded = final_sites >= N_LAYERS  # shouldn't grow faster than linear

    if collapsed:
        print("  ** COLLAPSED to <= 1 site => FALSIFIED **")
    elif grew_unbounded:
        print(f"  ** Grew to {final_sites} sites (may be unbounded) **")
    else:
        print(f"  Self-regulating: {final_sites} sites at final layer")

    # Norm check
    final_norm = sum(abs(psi_final[2*y])**2 + abs(psi_final[2*y+1])**2
                     for y in layers[-1])
    print(f"  Final-layer norm: {final_norm:.6e}")

    # ── Test 2: Born Rule (Sorkin I_3) ──────────────────────────────
    print()
    print("TEST 2: Born Rule (3-Slit Sorkin Test)")
    print("-" * 50)

    I3_max, slits, I3_sum = sorkin_test(layers, THETA_0, N_Y_MAX)

    if I3_max is None:
        print(f"  SKIPPED: {I3_sum}")  # I3_sum holds error message here
    else:
        print(f"  Barrier slits at y = {slits}")
        print(f"  I_3 max:  {I3_max:.6e}")
        print(f"  I_3 sum:  {I3_sum:.6e}")

        born_pass = I3_max < 1e-6
        print(f"  Born PASS: {born_pass}  (threshold: 1e-6)")
        if not born_pass:
            print("  ** Born rule VIOLATED => FALSIFIED **")

    # ── Test 3: Gravity ─────────────────────────────────────────────
    print()
    print("TEST 3: Gravity (Localized Phase Field)")
    print("-" * 50)

    mass_y = center + MASS_OFFSET
    com_flat, com_grav, shift, toward, bc_grav = gravity_test(
        layers, THETA_0, N_Y_MAX, GRAV_STRENGTH, mass_y)

    print(f"  Mass at y = {mass_y} (center + {MASS_OFFSET})")
    print(f"  CoM (flat):    {com_flat:.4f}")
    print(f"  CoM (gravity): {com_grav:.4f}")
    print(f"  Shift:         {shift:+.6f}")
    print(f"  Toward mass:   {toward}")
    print(f"  Bhattacharyya: {bc_grav:.6f}")

    # ── Test 4: Comparison to Static Lattice ────────────────────────
    print()
    print("TEST 4: Static Lattice Comparison")
    print("-" * 50)

    bc_static, dist_static, dist_grown = static_comparison(
        N_LAYERS, N_Y_MAX, THETA_0, layers)

    print(f"  Bhattacharyya overlap (grown vs static): {bc_static:.6f}")

    # Show distributions side by side for a few sites
    all_sites = sorted(set(dist_static.keys()) | set(dist_grown.keys()))
    print(f"\n  y-offset   P_static    P_grown     diff")
    for y in all_sites:
        ps = dist_static.get(y, 0)
        pg = dist_grown.get(y, 0)
        if ps > 1e-6 or pg > 1e-6:
            print(f"  {y - center:+4d}      {ps:.6f}    {pg:.6f}    {pg - ps:+.6f}")

    # ── Summary ─────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    results = {
        "growth_self_regulating": not collapsed and not grew_unbounded,
        "final_sites": final_sites,
        "final_norm": final_norm,
        "born_I3_max": I3_max,
        "born_pass": I3_max is not None and I3_max < 1e-6,
        "gravity_toward": toward,
        "gravity_shift": shift,
        "static_overlap": bc_static,
    }

    for k, v in results.items():
        if isinstance(v, float):
            print(f"  {k:30s} = {v:.6e}")
        else:
            print(f"  {k:30s} = {v}")

    # Verdict
    print()
    hypothesis_alive = (results["growth_self_regulating"]
                        and results["born_pass"]
                        and results["final_sites"] > 1)

    if hypothesis_alive:
        print("HYPOTHESIS ALIVE: Chiral growth is self-regulating and Born-compliant.")
    else:
        reasons = []
        if not results["growth_self_regulating"]:
            reasons.append("growth not self-regulating")
        if not results["born_pass"]:
            reasons.append(f"Born I_3 = {I3_max:.2e} > 1e-6")
        if results["final_sites"] <= 1:
            reasons.append("collapsed to <= 1 site")
        print(f"FALSIFIED: {', '.join(reasons)}")

    print()
    print(f"Gravity note: shift {'TOWARD' if toward else 'AWAY from'} mass "
          f"(shift = {shift:+.6e})")
    print(f"Static overlap: {bc_static:.6f} "
          f"({'high' if bc_static > 0.95 else 'moderate' if bc_static > 0.8 else 'low'})")
