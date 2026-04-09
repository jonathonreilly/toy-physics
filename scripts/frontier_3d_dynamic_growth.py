#!/usr/bin/env python3
"""
frontier_3d_dynamic_growth.py
==============================
Amplitude-guided dynamic growth on a 3D DAG (1 propagation + 2 spatial dims).

GAP:
  All dynamic-growth experiments so far are 2D. The 3D lattice infrastructure
  exists (Lattice3D) but growth has never been tested. This script checks
  whether self-regulating behavior and Born compliance extend to 3D.

GROWTH RULE:
  layer_0 = {(0, 0, 0)}          # single source node in (lx, iy, iz)
  For each new layer lx:
    1. Generate candidates at (lx, iy+dy, iz+dz) for |dy|,|dz| <= max_d
    2. Propagate amplitude from previous layer to candidates using
       exp(ikL) * w(theta) * h^2 / L^2  (h^2 measure, 1/L^2 kernel)
    3. Keep candidates where |amp|^2 > threshold * max(|amp|^2)

TESTS:
  1. Growth shape  -- nodes per layer, (iy,iz) extent
  2. Born rule     -- 3-slit Sorkin I3 with barrier at layer nl//3
  3. Gravity       -- 2D Laplacian on the spatial (iy,iz) plane with a
                      persistent mass, broadcast to all layers, measure
                      centroid shift

PARAMETERS:
  h = 0.5, K = 5.0, max_d = 3, n_layers = 15, threshold = 0.05
  Kernel: exp(-0.8 * theta^2), power p = 2 (for d_spatial = 2)

HYPOTHESIS:
  "3D amplitude-guided growth is self-regulating and Born-compliant."

FALSIFICATION:
  "If graph collapses (< 3 nodes/layer) or Born fails (|I3|/P > 1e-6)."
"""

from __future__ import annotations
import math
import cmath
import time
import numpy as np


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
H = 0.5
K = 5.0
BETA = 0.8
MAX_D = 3
N_LAYERS = 15
THRESHOLD = 0.05
P_KERNEL = 2          # 1/L^2 for 2 spatial dims


# ---------------------------------------------------------------------------
# Core: edge amplitude in 3D
# ---------------------------------------------------------------------------

def edge_amplitude_3d(src, dst, k, h):
    """Edge amplitude from src=(lx, iy, iz) to dst=(lx', iy', iz').

    Physical coords: (lx*h, iy*h, iz*h).
    Kernel: exp(ikL) * w(theta) * h^2 / L^2
    """
    dx = h                                  # always one layer forward
    dy = (dst[1] - src[1]) * h
    dz = (dst[2] - src[2]) * h
    L = math.sqrt(dx * dx + dy * dy + dz * dz)
    if L < 1e-15:
        return 0j
    r_perp = math.sqrt(dy * dy + dz * dz)
    theta = math.atan2(r_perp, dx)
    w = math.exp(-BETA * theta * theta)
    return cmath.exp(1j * k * L) * w * (h * h) / (L * L)


# ---------------------------------------------------------------------------
# Test 1: Growth shape
# ---------------------------------------------------------------------------

def grow_graph_3d(n_layers, k, h, max_d, threshold_frac,
                  field_func=None):
    """Grow a 3D DAG layer by layer.

    field_func: if provided, callable(iy, iz) -> float potential V.
      Action becomes S = L * (1 + V_mid).

    Returns (layers, amplitudes) where:
      layers[i] = set of (lx, iy, iz) tuples
      amplitudes = dict (lx, iy, iz) -> complex
    """
    layers = [set()]
    layers[0].add((0, 0, 0))
    amplitudes = {(0, 0, 0): 1.0 + 0j}

    for lx in range(1, n_layers):
        prev_nodes = layers[lx - 1]

        # Generate candidates
        candidates = set()
        for (_, iy, iz) in prev_nodes:
            for dy in range(-max_d, max_d + 1):
                for dz in range(-max_d, max_d + 1):
                    candidates.add((lx, iy + dy, iz + dz))

        # Propagate
        new_amps = {}
        for cand in candidates:
            amp = 0j
            for src in prev_nodes:
                if src not in amplitudes:
                    continue
                a_src = amplitudes[src]
                if abs(a_src) < 1e-30:
                    continue

                if field_func is not None:
                    # Gravity: modify action
                    dy_phys = (cand[1] - src[1]) * h
                    dz_phys = (cand[2] - src[2]) * h
                    L = math.sqrt(h * h + dy_phys * dy_phys + dz_phys * dz_phys)
                    r_perp = math.sqrt(dy_phys * dy_phys + dz_phys * dz_phys)
                    theta = math.atan2(r_perp, h)
                    w = math.exp(-BETA * theta * theta)

                    iy_mid = (src[1] + cand[1]) / 2.0
                    iz_mid = (src[2] + cand[2]) / 2.0
                    V = field_func(iy_mid, iz_mid)
                    S = L * (1.0 + V)
                    ea = cmath.exp(1j * k * S) * w * (h * h) / (L * L)
                else:
                    ea = edge_amplitude_3d(src, cand, k, h)

                amp += a_src * ea
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


def test_growth_shape():
    """Test 1: Does the 3D graph grow, collapse, or explode?"""
    print("=" * 72)
    print("TEST 1: 3D DYNAMIC GROWTH SHAPE")
    print("=" * 72)
    print()
    print(f"  h={H}, K={K}, max_d={MAX_D}, n_layers={N_LAYERS}")
    print()

    results = {}
    for thresh_frac in [0.01, 0.05, 0.10]:
        print(f"--- threshold = {thresh_frac:.0%} of max |psi|^2 ---")
        t0 = time.time()
        layers, amplitudes = grow_graph_3d(
            N_LAYERS, K, H, MAX_D, thresh_frac
        )
        dt = time.time() - t0

        print(f"  {'Layer':>5}  {'Nodes':>6}  {'iy range':>12}  {'iz range':>12}  {'max|psi|^2':>12}")
        for i, layer_set in enumerate(layers):
            iys = [n[1] for n in layer_set]
            izs = [n[2] for n in layer_set]
            probs = [abs(amplitudes[n]) ** 2 for n in layer_set if n in amplitudes]
            max_p = max(probs) if probs else 0.0
            iy_lo, iy_hi = min(iys), max(iys)
            iz_lo, iz_hi = min(izs), max(izs)
            print(f"  {i:5d}  {len(layer_set):6d}  "
                  f"[{iy_lo:+3d},{iy_hi:+3d}]  [{iz_lo:+3d},{iz_hi:+3d}]  "
                  f"{max_p:12.4e}")

        final_count = len(layers[-1]) if layers else 0
        if final_count < 3:
            verdict = "COLLAPSED"
        elif final_count > (2 * MAX_D + 1) ** 2:
            verdict = "GROWING"
        else:
            verdict = "STABLE"

        print(f"  Verdict: {verdict} (final layer: {final_count} nodes, "
              f"{dt:.1f}s)")
        print()
        results[thresh_frac] = (layers, amplitudes, verdict)

    # Return the 5% threshold result for further tests
    return results.get(THRESHOLD, results[list(results.keys())[0]])


# ---------------------------------------------------------------------------
# Test 2: Born rule (3-slit Sorkin) on the grown 3D DAG
# ---------------------------------------------------------------------------

def test_born_rule(layers, amplitudes):
    """Test 2: Sorkin 3-slit test on the grown 3D DAG.

    Place a barrier at layer nl//3. Open 3 slits at (iy, iz) positions
    along the iy axis with iz=0: slits at iy = -1, 0, +1.
    """
    print("=" * 72)
    print("TEST 2: BORN RULE (SORKIN 3-SLIT) ON GROWN 3D DAG")
    print("=" * 72)
    print()

    if len(layers) < 8:
        print("  Graph too small for Born test (need >= 8 layers).")
        print()
        return

    slit_layer_idx = len(layers) // 3
    slit_layer = layers[slit_layer_idx]
    slit_ys = sorted(set(n[1] for n in slit_layer))
    print(f"  Slit barrier at layer {slit_layer_idx}")
    print(f"  Available iy values: {slit_ys}")
    print(f"  Using 3 slits at iy = -1, 0, +1 (iz = any)")
    print()

    # Re-propagate from scratch on the fixed DAG structure
    init_amps = {n: (1.0 + 0j if n == (0, 0, 0) else 0j) for n in layers[0]}

    def prob_at_detector(open_iy_set):
        """Propagate with slit mask: at slit_layer_idx, only pass
        amplitude through nodes whose iy is in open_iy_set."""
        amps = dict(init_amps)
        for i in range(1, len(layers)):
            prev = layers[i - 1]
            curr = layers[i]
            new_a = {}
            for node in curr:
                amp = 0j
                for src in prev:
                    a_src = amps.get(src, 0j)
                    if abs(a_src) < 1e-30:
                        continue
                    # Apply slit mask at the slit layer
                    if i == slit_layer_idx and src[1] not in open_iy_set:
                        continue
                    amp += a_src * edge_amplitude_3d(src, node, K, H)
                new_a[node] = amp
            amps.update(new_a)
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

    if ratio < 1e-6:
        print("  PASS: Born rule survives on the grown 3D DAG "
              f"(|I3|/P = {ratio:.2e} < 1e-6).")
    else:
        print(f"  FAIL: |I3|/P = {ratio:.2e} > 1e-6 -- Born rule violated.")
    print()


# ---------------------------------------------------------------------------
# Test 3: Gravity via 2D Laplacian on spatial (iy, iz) plane
# ---------------------------------------------------------------------------

def solve_laplacian_2d(grid_half, mass_iy, mass_iz, strength=1.0,
                       max_iter=3000, tol=1e-8):
    """Solve 2D Laplacian on a (2*grid_half+1)^2 grid with Dirichlet BC.

    Returns field[iy + grid_half, iz + grid_half] for iy, iz in
    [-grid_half, grid_half].
    """
    n = 2 * grid_half + 1
    field = np.zeros((n, n))
    source = np.zeros((n, n))
    si = mass_iy + grid_half
    sj = mass_iz + grid_half
    if 0 <= si < n and 0 <= sj < n:
        source[si, sj] = strength

    for _ in range(max_iter):
        old = field.copy()
        for i in range(1, n - 1):
            for j in range(1, n - 1):
                field[i, j] = 0.25 * (
                    field[i + 1, j] + field[i - 1, j]
                    + field[i, j + 1] + field[i, j - 1]
                    + source[i, j]
                )
        if np.max(np.abs(field - old)) < tol:
            break

    return field, grid_half


def test_gravity(layers_free, amps_free):
    """Test 3: Gravity deflection on the grown 3D DAG.

    Solve a 2D Laplacian on the spatial (iy, iz) plane with a point mass,
    broadcast that field to all layers, and re-grow with the field.
    Measure centroid shift vs free-space.
    """
    print("=" * 72)
    print("TEST 3: GRAVITY ON GROWN 3D DAG (2D LAPLACIAN)")
    print("=" * 72)
    print()

    # Determine grid extent from the free-space grown graph
    max_coord = 0
    for layer in layers_free:
        for (_, iy, iz) in layer:
            max_coord = max(max_coord, abs(iy), abs(iz))
    grid_half = max_coord + 3  # padding

    # Place mass at (iy=4, iz=0)
    mass_iy = 4
    mass_iz = 0
    mass_strength = 1.0

    print(f"  Solving 2D Laplacian: grid_half={grid_half}, "
          f"mass at iy={mass_iy}, iz={mass_iz}")
    t0 = time.time()
    field, gh = solve_laplacian_2d(grid_half, mass_iy, mass_iz, mass_strength)
    dt = time.time() - t0
    print(f"  Laplacian solved in {dt:.2f}s")

    # Field lookup: V(iy, iz) -- clamp to grid bounds
    def field_func(iy_f, iz_f):
        """Return potential at fractional (iy, iz) coords via nearest-neighbor."""
        ii = int(round(iy_f)) + gh
        jj = int(round(iz_f)) + gh
        n = field.shape[0]
        ii = max(0, min(n - 1, ii))
        jj = max(0, min(n - 1, jj))
        return -0.05 * field[ii, jj]   # scale factor for gentle deflection

    # Grow with gravity field
    print("  Growing 3D DAG with gravity field...")
    t0 = time.time()
    layers_grav, amps_grav = grow_graph_3d(
        N_LAYERS, K, H, MAX_D, THRESHOLD, field_func=field_func
    )
    dt = time.time() - t0
    print(f"  Gravity growth completed in {dt:.1f}s")
    print()

    # Compare centroids
    def centroid_yz(layer_nodes, amps):
        """Probability-weighted centroid in (iy, iz)."""
        total_p = 0.0
        wy = 0.0
        wz = 0.0
        for n in layer_nodes:
            prob = abs(amps.get(n, 0)) ** 2
            total_p += prob
            wy += n[1] * prob
            wz += n[2] * prob
        if total_p < 1e-30:
            return 0.0, 0.0
        return wy / total_p, wz / total_p

    print(f"  {'Layer':>5}  {'cy_free':>9}  {'cz_free':>9}  "
          f"{'cy_grav':>9}  {'cz_grav':>9}  {'dy':>9}  {'dz':>9}")

    n_compare = min(len(layers_free), len(layers_grav))
    deflections_y = []
    deflections_z = []
    for i in range(n_compare):
        cy_f, cz_f = centroid_yz(layers_free[i], amps_free)
        cy_g, cz_g = centroid_yz(layers_grav[i], amps_grav)
        dy = cy_g - cy_f
        dz = cz_g - cz_f
        deflections_y.append(dy)
        deflections_z.append(dz)
        print(f"  {i:5d}  {cy_f:+9.4f}  {cz_f:+9.4f}  "
              f"{cy_g:+9.4f}  {cz_g:+9.4f}  {dy:+9.5f}  {dz:+9.5f}")

    print()
    if len(deflections_y) >= 5:
        late_dy = np.mean(deflections_y[-5:])
        late_dz = np.mean(deflections_z[-5:])
        early_mag = np.mean([math.sqrt(dy ** 2 + dz ** 2)
                             for dy, dz in zip(deflections_y[2:7],
                                               deflections_z[2:7])])
        late_mag = np.mean([math.sqrt(dy ** 2 + dz ** 2)
                            for dy, dz in zip(deflections_y[-5:],
                                              deflections_z[-5:])])
        growing = late_mag > 2 * early_mag

        sign_y = "toward" if (late_dy > 0) == (mass_iy > 0) else "away from"
        print(f"  Late avg deflection: dy={late_dy:+.6f} ({sign_y} mass in iy), "
              f"dz={late_dz:+.6f}")
        print(f"  Early |deflection| avg: {early_mag:.6f}")
        print(f"  Late  |deflection| avg: {late_mag:.6f}")
        print(f"  Deflection growing: {'YES' if growing else 'NO'}")

        toward = (late_dy > 0) == (mass_iy > 0)
        if late_mag > 0.01 and toward:
            print(f"  PASS: Measurable TOWARD deflection on grown 3D graph.")
        elif late_mag > 0.01 and not toward:
            print(f"  PARTIAL: Measurable deflection but AWAY from mass.")
            print(f"  (Same strong-field sign issue as 2D — see frontier_2d_gravity_sign_diagnosis.py)")
        else:
            print(f"  WEAK: Deflection present but small ({late_mag:.2e}).")
    print()


# ---------------------------------------------------------------------------
# Test 4: Compare grown 3D DAG to static 3D lattice
# ---------------------------------------------------------------------------

def propagate_static_3d(n_layers, hw, k, h, max_d):
    """Propagate on a static 3D lattice from a single source at (0,0,0)."""
    layers = []
    amplitudes = {}

    for lx in range(n_layers):
        layer = set()
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                layer.add((lx, iy, iz))
        layers.append(layer)

    # Init source
    for n in layers[0]:
        amplitudes[n] = 1.0 + 0j if n == (0, 0, 0) else 0j

    # Propagate layer by layer
    for i in range(1, n_layers):
        for node in layers[i]:
            amp = 0j
            for src in layers[i - 1]:
                a_src = amplitudes.get(src, 0j)
                if abs(a_src) < 1e-30:
                    continue
                if abs(node[1] - src[1]) > max_d or abs(node[2] - src[2]) > max_d:
                    continue
                amp += a_src * edge_amplitude_3d(src, node, k, h)
            amplitudes[node] = amp

    return layers, amplitudes


def test_static_comparison(layers_grown, amps_grown):
    """Test 4: Compare grown graph to static 3D lattice."""
    print("=" * 72)
    print("TEST 4: GROWN vs STATIC 3D LATTICE COMPARISON")
    print("=" * 72)
    print()

    # Determine extent of grown graph
    max_coord = 0
    for layer in layers_grown:
        for (_, iy, iz) in layer:
            max_coord = max(max_coord, abs(iy), abs(iz))
    hw = max(max_coord + 1, MAX_D + 1)

    n_layers = len(layers_grown)
    print(f"  Static lattice: hw={hw}, n_layers={n_layers}, "
          f"nodes/layer={(2*hw+1)**2}")

    t0 = time.time()
    layers_static, amps_static = propagate_static_3d(
        n_layers, hw, K, H, MAX_D
    )
    dt = time.time() - t0
    print(f"  Static propagation: {dt:.1f}s")
    print()

    print(f"  {'Layer':>5}  {'N(grown)':>9}  {'N(static)':>10}  "
          f"{'maxP(grown)':>12}  {'maxP(static)':>13}")

    for i in range(n_layers):
        ng = len(layers_grown[i])
        ns = len(layers_static[i])
        pg = max((abs(amps_grown.get(n, 0)) ** 2 for n in layers_grown[i]),
                 default=0)
        ps = max((abs(amps_static.get(n, 0)) ** 2 for n in layers_static[i]),
                 default=0)
        print(f"  {i:5d}  {ng:9d}  {ns:10d}  {pg:12.4e}  {ps:13.4e}")

    # Final layer Bhattacharyya fidelity
    print()
    final_i = n_layers - 1
    grown_final = layers_grown[final_i]
    static_final = layers_static[final_i]

    total_g = sum(abs(amps_grown.get(n, 0)) ** 2 for n in grown_final)
    total_s = sum(abs(amps_static.get(n, 0)) ** 2 for n in static_final)
    print(f"  Total prob final layer (grown):  {total_g:.6e}")
    print(f"  Total prob final layer (static): {total_s:.6e}")

    # Overlap on common (iy, iz) values
    common_yz = (set((n[1], n[2]) for n in grown_final) &
                 set((n[1], n[2]) for n in static_final))

    if common_yz and total_g > 1e-30 and total_s > 1e-30:
        fidelity = 0.0
        for (iy, iz) in common_yz:
            ng = (final_i, iy, iz)
            ns = (final_i, iy, iz)
            p_g = abs(amps_grown.get(ng, 0)) ** 2 / total_g
            p_s = abs(amps_static.get(ns, 0)) ** 2 / total_s
            fidelity += math.sqrt(p_g * p_s)
        print(f"  Bhattacharyya fidelity: {fidelity:.6f}")
        if fidelity > 0.9:
            print("  HIGH fidelity: grown 3D graph matches static lattice well.")
        elif fidelity > 0.5:
            print("  MODERATE fidelity: some structural difference.")
        else:
            print("  LOW fidelity: grown and static produce very different results.")
    else:
        print("  Cannot compute fidelity (no common nodes or zero probability).")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    print()
    print("=" * 72)
    print("FRONTIER: 3D DYNAMIC AMPLITUDE-GUIDED GRAPH GROWTH")
    print("=" * 72)
    print()
    print("Testing whether amplitude-guided growth extends to 3D")
    print("(1 propagation + 2 spatial dimensions).")
    print()
    print(f"Parameters: h={H}, K={K}, beta={BETA}, max_d={MAX_D}, "
          f"n_layers={N_LAYERS}")
    print(f"Threshold: {THRESHOLD:.0%} of max |psi|^2")
    print(f"Kernel: exp(-{BETA}*theta^2) * h^2 / L^2  (p={P_KERNEL})")
    print()

    # Test 1: Growth shape (runs 3 thresholds, returns the THRESHOLD one)
    layers, amps, verdict = test_growth_shape()

    # Test 2: Born rule
    test_born_rule(layers, amps)

    # Test 3: Gravity
    test_gravity(layers, amps)

    # Test 4: Static comparison
    test_static_comparison(layers, amps)

    # Summary
    dt_total = time.time() - t_start
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    final_n = len(layers[-1]) if layers else 0
    print(f"  Growth:  {verdict} ({final_n} nodes at final layer)")
    print(f"  Layers:  {len(layers)} of {N_LAYERS} requested")
    print(f"  Runtime: {dt_total:.1f}s")
    print()
    print("3D dynamic growth tested with 3 threshold levels.")
    print("Born rule (Sorkin I3) tested on the grown 3D DAG.")
    print("Gravity (2D Laplacian field) deflection measured.")
    print("Distribution fidelity compared: grown vs static 3D lattice.")
    print()


if __name__ == "__main__":
    main()
