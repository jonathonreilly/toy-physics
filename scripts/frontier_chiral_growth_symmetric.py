#!/usr/bin/env python3
"""
frontier_chiral_growth_symmetric.py
2+1D chiral quantum walk with symmetric source and threshold-based growth.

HYPOTHESIS: "2+1D symmetric growth is self-regulating and Born-compliant."
FALSIFICATION: "If graph collapses or Born fails."

Architecture:
  - 4 coin components per site: +y, -y, +z, -z
  - Symmetric coin (Grover diffusion on 4 components)
  - Growth: keep sites where P > threshold * max(P)
  - Tests: shape stability, Born (3-slit Sorkin), gravity centroid shift
"""

import numpy as np
from collections import defaultdict

# ── Parameters ──────────────────────────────────────────────────────────
N_MAX = 31          # max grid extent in each direction
N_LAYERS = 20       # growth layers
THETA0 = 0.3        # coin angle (unused for Grover, kept for reference)
THRESHOLD = 0.03    # pruning threshold (fraction of max probability)
Z_OFFSET = 4        # mass position offset in z
G_STRENGTH = 5e-4   # gravitational field strength

# Coin components: 0=+y, 1=-y, 2=+z, 3=-z
SHIFT_DIRS = {
    0: (0, +1, 0),   # +y
    1: (0, -1, 0),   # -y
    2: (0, 0, +1),   # +z
    3: (0, 0, -1),   # -z
}
N_COMP = 4


def grover_coin():
    """4x4 Grover diffusion coin: 2/N * ones - I."""
    return (2.0 / N_COMP) * np.ones((N_COMP, N_COMP)) - np.eye(N_COMP)


def make_coin_parametric(theta):
    """Alternative: parametric coin mixing angle theta."""
    c, s = np.cos(theta), np.sin(theta)
    # Block-diagonal Hadamard-like for 4 components
    H2 = np.array([[c, s], [s, -c]])
    return np.kron(H2, H2)


def run_chiral_growth(coin_matrix, n_layers, threshold, verbose=True):
    """
    Grow a 2+1D chiral graph layer by layer.

    State: dict mapping (layer, y, z) -> np.array of shape (N_COMP,) complex
    Returns: list of (layer_idx, active_sites, state_dict)
    """
    center = N_MAX // 2

    # Layer 0: single site with symmetric amplitudes
    state = {}
    init_amp = 0.5  # 1/sqrt(N_COMP) = 1/2 for 4 components, but spec says 1/2
    state[(0, center, center)] = np.array([init_amp] * N_COMP, dtype=complex)

    layer_history = []
    active_by_layer = {0: {(center, center)}}
    layer_history.append((0, {(center, center)}, dict(state)))

    if verbose:
        p0 = np.sum(np.abs(state[(0, center, center)])**2)
        print(f"Layer  0: sites=1, total_prob={p0:.6f}")

    for layer in range(1, n_layers + 1):
        # Step 1: Apply coin at all active sites in previous layer
        prev_layer = layer - 1
        prev_sites = active_by_layer.get(prev_layer, set())

        coined_state = {}
        for (l, y, z), psi in state.items():
            if l == prev_layer and (y, z) in prev_sites:
                coined_state[(l, y, z)] = coin_matrix @ psi
            else:
                coined_state[(l, y, z)] = psi.copy()

        # Step 2: Shift - each component moves 1 step in its direction
        # New layer sites accumulate amplitudes from shifts
        new_layer_state = defaultdict(lambda: np.zeros(N_COMP, dtype=complex))

        for (l, y, z), psi in coined_state.items():
            if l != prev_layer or (y, z) not in prev_sites:
                continue
            for comp in range(N_COMP):
                _, dy, dz = SHIFT_DIRS[comp]
                ny, nz = y + dy, z + dz
                if 0 <= ny < N_MAX and 0 <= nz < N_MAX:
                    new_layer_state[(layer, ny, nz)][comp] += psi[comp]

        # Step 3: Compute probability at each candidate site
        probs = {}
        for key, psi in new_layer_state.items():
            probs[key] = np.sum(np.abs(psi)**2)

        if not probs:
            if verbose:
                print(f"Layer {layer:2d}: NO CANDIDATES - growth terminated")
            break

        max_prob = max(probs.values())

        # Step 4: Threshold pruning
        active_sites = set()
        for key, p in probs.items():
            if p >= threshold * max_prob:
                state[key] = new_layer_state[key]
                active_sites.add((key[1], key[2]))

        active_by_layer[layer] = active_sites

        # Total probability on this layer
        total_p = sum(np.sum(np.abs(state[(layer, y, z)])**2)
                      for (y, z) in active_sites)

        if verbose:
            print(f"Layer {layer:2d}: sites={len(active_sites):4d}, "
                  f"max_prob={max_prob:.6f}, total_prob={total_p:.6f}")

        layer_history.append((layer, active_sites, dict(state)))

        if len(active_sites) == 0:
            if verbose:
                print("  -> Graph collapsed!")
            break

    return layer_history, state, active_by_layer


def test_growth_shape(layer_history):
    """Test 1: Growth shape - nodes per layer, stability."""
    print("\n" + "="*70)
    print("TEST 1: GROWTH SHAPE")
    print("="*70)

    sizes = []
    for layer_idx, sites, _ in layer_history:
        sizes.append(len(sites))

    print(f"  Layer sizes: {sizes}")

    # Check if growth stabilizes or collapses
    if len(sizes) >= 5:
        last5 = sizes[-5:]
        if all(s > 0 for s in last5):
            mean_last5 = np.mean(last5)
            std_last5 = np.std(last5)
            cv = std_last5 / mean_last5 if mean_last5 > 0 else float('inf')
            print(f"  Last 5 layers: mean={mean_last5:.1f}, std={std_last5:.1f}, CV={cv:.3f}")
            if cv < 0.3:
                print("  RESULT: Growth STABILIZED (CV < 0.3)")
                return "STABLE"
            else:
                print("  RESULT: Growth VARIABLE (CV >= 0.3)")
                return "VARIABLE"
        else:
            print("  RESULT: Graph COLLAPSED (zero-size layers)")
            return "COLLAPSED"

    if sizes[-1] == 0:
        print("  RESULT: Graph COLLAPSED")
        return "COLLAPSED"

    print("  RESULT: Too few layers to assess stability")
    return "INSUFFICIENT"


def test_born_sorkin(state, active_by_layer, coin_matrix, n_layers):
    """
    Test 2: Born rule via 3-slit Sorkin parameter.

    Use absorption blocking: compare P(ABC), P(AB), P(AC), P(BC), P(A), P(B), P(C)
    where A,B,C are three slits at an intermediate layer.

    Sorkin kappa = P(ABC) - P(AB) - P(AC) - P(BC) + P(A) + P(B) + P(C)
    Born rule: kappa ~ 0
    """
    print("\n" + "="*70)
    print("TEST 2: BORN RULE (3-slit Sorkin)")
    print("="*70)

    # Pick slit layer at ~1/3 of total depth
    slit_layer = max(2, n_layers // 3)
    detect_layer = min(n_layers, slit_layer + 6)

    slit_sites = sorted(active_by_layer.get(slit_layer, set()))
    if len(slit_sites) < 3:
        print(f"  Only {len(slit_sites)} sites at slit layer {slit_layer} - need 3")
        print("  RESULT: SKIP (insufficient sites)")
        return "SKIP"

    # Pick 3 well-separated slits
    n_s = len(slit_sites)
    slit_A = slit_sites[0]
    slit_B = slit_sites[n_s // 2]
    slit_C = slit_sites[-1]
    slits = {'A': slit_A, 'B': slit_B, 'C': slit_C}

    print(f"  Slit layer: {slit_layer}, Detection layer: {detect_layer}")
    print(f"  Slits: A={slit_A}, B={slit_B}, C={slit_C}")

    def run_with_open(open_set):
        """Run walk allowing only sites in open_set at slit layer."""
        center = N_MAX // 2
        st = {}
        init_amp = 0.5
        st[(0, center, center)] = np.array([init_amp] * N_COMP, dtype=complex)
        abl = {0: {(center, center)}}

        for ly in range(1, detect_layer + 1):
            prev_sites = abl.get(ly - 1, set())

            # Coin
            coined = {}
            for (l, y, z), psi in st.items():
                if l == ly - 1 and (y, z) in prev_sites:
                    coined[(l, y, z)] = coin_matrix @ psi
                else:
                    coined[(l, y, z)] = psi.copy()

            # Shift
            new_state = defaultdict(lambda: np.zeros(N_COMP, dtype=complex))
            for (l, y, z), psi in coined.items():
                if l != ly - 1 or (y, z) not in prev_sites:
                    continue
                for comp in range(N_COMP):
                    _, dy, dz = SHIFT_DIRS[comp]
                    ny, nz = y + dy, z + dz
                    if 0 <= ny < N_MAX and 0 <= nz < N_MAX:
                        new_state[(ly, ny, nz)][comp] += psi[comp]

            # At slit layer, block sites not in open_set
            if ly == slit_layer:
                filtered = {}
                for key, psi in new_state.items():
                    if (key[1], key[2]) in open_set:
                        filtered[key] = psi
                new_state = filtered

            # Threshold pruning (use original active sites for reference)
            probs = {}
            for key, psi in new_state.items():
                p = np.sum(np.abs(psi)**2)
                if isinstance(new_state, dict):
                    probs[key] = p
                else:
                    probs[key] = p

            if not probs:
                abl[ly] = set()
                break

            max_p = max(probs.values())
            active = set()
            for key, p in probs.items():
                if p >= THRESHOLD * max_p:
                    st[key] = new_state[key] if isinstance(new_state[key], np.ndarray) else new_state[key]
                    active.add((key[1], key[2]))

            abl[ly] = active

        # Measure total probability at detection layer
        total_p = 0.0
        for (y, z) in abl.get(detect_layer, set()):
            key = (detect_layer, y, z)
            if key in st:
                total_p += np.sum(np.abs(st[key])**2)
        return total_p

    # All 7 combinations
    A, B, C = slits['A'], slits['B'], slits['C']

    P_ABC = run_with_open({A, B, C})
    P_AB = run_with_open({A, B})
    P_AC = run_with_open({A, C})
    P_BC = run_with_open({B, C})
    P_A = run_with_open({A})
    P_B = run_with_open({B})
    P_C = run_with_open({C})

    kappa = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

    # Normalize
    norm_kappa = abs(kappa) / max(P_ABC, 1e-30)

    print(f"  P(ABC)={P_ABC:.6e}, P(AB)={P_AB:.6e}, P(AC)={P_AC:.6e}, P(BC)={P_BC:.6e}")
    print(f"  P(A)={P_A:.6e}, P(B)={P_B:.6e}, P(C)={P_C:.6e}")
    print(f"  kappa = {kappa:.6e}")
    print(f"  |kappa|/P(ABC) = {norm_kappa:.6e}")

    if norm_kappa < 0.05:
        print("  RESULT: Born PASSES (|kappa|/P < 0.05)")
        return "PASS"
    elif norm_kappa < 0.15:
        print("  RESULT: Born MARGINAL (0.05 < |kappa|/P < 0.15)")
        return "MARGINAL"
    else:
        print(f"  RESULT: Born FAILS (|kappa|/P = {norm_kappa:.4f})")
        return "FAIL"


def test_gravity(state, active_by_layer, coin_matrix, n_layers):
    """
    Test 3: Gravity via Lorentzian phase field.

    Add phase exp(i * g / r) for mass at offset position.
    Measure centroid shift TOWARD mass.
    """
    print("\n" + "="*70)
    print("TEST 3: GRAVITY (Lorentzian phase field)")
    print("="*70)

    center = N_MAX // 2
    mass_pos = (center, center + Z_OFFSET)

    print(f"  Mass at (y,z) = {mass_pos}, strength = {G_STRENGTH}")

    def run_with_field(g_strength):
        """Run walk with gravitational phase field."""
        st = {}
        init_amp = 0.5
        st[(0, center, center)] = np.array([init_amp] * N_COMP, dtype=complex)
        abl = {0: {(center, center)}}

        for ly in range(1, n_layers + 1):
            prev_sites = abl.get(ly - 1, set())

            # Coin
            coined = {}
            for (l, y, z), psi in st.items():
                if l == ly - 1 and (y, z) in prev_sites:
                    coined[(l, y, z)] = coin_matrix @ psi
                else:
                    coined[(l, y, z)] = psi.copy()

            # Shift
            new_state = defaultdict(lambda: np.zeros(N_COMP, dtype=complex))
            for (l, y, z), psi in coined.items():
                if l != ly - 1 or (y, z) not in prev_sites:
                    continue
                for comp in range(N_COMP):
                    _, dy, dz = SHIFT_DIRS[comp]
                    ny, nz = y + dy, z + dz
                    if 0 <= ny < N_MAX and 0 <= nz < N_MAX:
                        new_state[(ly, ny, nz)][comp] += psi[comp]

            # Apply gravitational phase
            if g_strength != 0:
                for key in list(new_state.keys()):
                    _, y, z = key
                    dy_m = y - mass_pos[0]
                    dz_m = z - mass_pos[1]
                    r = np.sqrt(dy_m**2 + dz_m**2)
                    if r > 0.5:
                        phase = np.exp(1j * g_strength / r)
                        new_state[key] = new_state[key] * phase

            # Threshold pruning
            probs = {}
            for key, psi in new_state.items():
                probs[key] = np.sum(np.abs(psi)**2)

            if not probs:
                abl[ly] = set()
                break

            max_p = max(probs.values())
            active = set()
            for key, p in probs.items():
                if p >= THRESHOLD * max_p:
                    st[key] = new_state[key]
                    active.add((key[1], key[2]))

            abl[ly] = active

        return st, abl

    # Run with and without field
    st_g, abl_g = run_with_field(G_STRENGTH)
    st_0, abl_0 = run_with_field(0.0)

    # Compute centroids at final layer
    def centroid(st_dict, abl_dict, layer):
        sites = abl_dict.get(layer, set())
        total_p = 0.0
        cy, cz = 0.0, 0.0
        for (y, z) in sites:
            key = (layer, y, z)
            if key in st_dict:
                p = np.sum(np.abs(st_dict[key])**2)
                total_p += p
                cy += p * y
                cz += p * z
        if total_p > 0:
            return cy / total_p, cz / total_p, total_p
        return center, center, 0.0

    final_layer = n_layers
    cy_g, cz_g, p_g = centroid(st_g, abl_g, final_layer)
    cy_0, cz_0, p_0 = centroid(st_0, abl_0, final_layer)

    shift_y = cy_g - cy_0
    shift_z = cz_g - cz_0

    # Direction TOWARD mass: mass is at center + Z_OFFSET in z
    # So positive shift_z means TOWARD mass
    toward = shift_z > 0

    print(f"  No-field centroid: ({cy_0:.4f}, {cz_0:.4f}), prob={p_0:.6e}")
    print(f"  With-field centroid: ({cy_g:.4f}, {cz_g:.4f}), prob={p_g:.6e}")
    print(f"  Shift: dy={shift_y:.6f}, dz={shift_z:.6f}")
    print(f"  Direction: {'TOWARD' if toward else 'AWAY'} mass")

    if toward and abs(shift_z) > 1e-6:
        print("  RESULT: Gravity TOWARD (PASS)")
        return "PASS"
    elif abs(shift_z) < 1e-6:
        print("  RESULT: Gravity NEGLIGIBLE")
        return "NEGLIGIBLE"
    else:
        print(f"  RESULT: Gravity AWAY (shift_z={shift_z:.6f})")
        return "FAIL"


def test_static_comparison(state, active_by_layer, coin_matrix, n_layers):
    """
    Test 4: Compare grown graph walk with static 2+1D grid walk.
    Measure overlap of final-layer probability distributions.
    """
    print("\n" + "="*70)
    print("TEST 4: STATIC GRID COMPARISON")
    print("="*70)

    center = N_MAX // 2

    # Run on static grid (no threshold pruning)
    st_static = {}
    init_amp = 0.5
    st_static[(0, center, center)] = np.array([init_amp] * N_COMP, dtype=complex)

    for ly in range(1, n_layers + 1):
        new_state = defaultdict(lambda: np.zeros(N_COMP, dtype=complex))

        for (l, y, z), psi in st_static.items():
            if l != ly - 1:
                continue
            coined = coin_matrix @ psi
            for comp in range(N_COMP):
                _, dy, dz = SHIFT_DIRS[comp]
                ny, nz = y + dy, z + dz
                if 0 <= ny < N_MAX and 0 <= nz < N_MAX:
                    new_state[(ly, ny, nz)][comp] += coined[comp]

        for key, psi in new_state.items():
            st_static[key] = psi

    # Compare probability distributions at final layer
    grown_probs = {}
    for (y, z) in active_by_layer.get(n_layers, set()):
        key = (n_layers, y, z)
        if key in state:
            grown_probs[(y, z)] = np.sum(np.abs(state[key])**2)

    static_probs = {}
    for key, psi in st_static.items():
        if key[0] == n_layers:
            p = np.sum(np.abs(psi)**2)
            if p > 1e-15:
                static_probs[(key[1], key[2])] = p

    # Compute overlap (Bhattacharyya coefficient)
    all_sites = set(grown_probs.keys()) | set(static_probs.keys())

    total_g = sum(grown_probs.values()) if grown_probs else 1e-30
    total_s = sum(static_probs.values()) if static_probs else 1e-30

    overlap = 0.0
    for site in all_sites:
        pg = grown_probs.get(site, 0.0) / total_g
        ps = static_probs.get(site, 0.0) / total_s
        overlap += np.sqrt(pg * ps)

    print(f"  Grown graph: {len(grown_probs)} sites at layer {n_layers}")
    print(f"  Static grid: {len(static_probs)} sites at layer {n_layers}")
    print(f"  Bhattacharyya overlap: {overlap:.6f}")

    # Sites lost by pruning
    lost = set(static_probs.keys()) - set(grown_probs.keys())
    lost_prob = sum(static_probs.get(s, 0.0) for s in lost) / total_s
    print(f"  Sites pruned away: {len(lost)}, carrying {lost_prob:.4%} of static probability")

    if overlap > 0.90:
        print("  RESULT: HIGH overlap with static grid (>0.90)")
        return "HIGH"
    elif overlap > 0.70:
        print("  RESULT: MODERATE overlap (0.70-0.90)")
        return "MODERATE"
    else:
        print(f"  RESULT: LOW overlap ({overlap:.4f})")
        return "LOW"


def main():
    print("="*70)
    print("FRONTIER: 2+1D Chiral Growth with Symmetric Source")
    print("="*70)
    print(f"Parameters: N_MAX={N_MAX}, N_LAYERS={N_LAYERS}, threshold={THRESHOLD}")
    print(f"Coin: Grover 4x4 diffusion")
    print(f"Source: symmetric (all components = 1/2)")
    print()

    coin = grover_coin()
    print("Coin matrix:")
    print(coin)
    print()

    # ── Main growth run ──
    print("─"*70)
    print("GROWING GRAPH...")
    print("─"*70)

    layer_history, state, active_by_layer = run_chiral_growth(
        coin, N_LAYERS, THRESHOLD, verbose=True
    )

    # ── Tests ──
    shape_result = test_growth_shape(layer_history)
    born_result = test_born_sorkin(state, active_by_layer, coin, N_LAYERS)
    gravity_result = test_gravity(state, active_by_layer, coin, N_LAYERS)
    static_result = test_static_comparison(state, active_by_layer, coin, N_LAYERS)

    # ── Summary ──
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"  Growth shape:     {shape_result}")
    print(f"  Born (Sorkin):    {born_result}")
    print(f"  Gravity:          {gravity_result}")
    print(f"  Static overlap:   {static_result}")

    hypothesis_pass = (
        shape_result in ("STABLE", "VARIABLE") and
        born_result in ("PASS", "MARGINAL") and
        gravity_result != "FAIL"
    )

    print()
    if hypothesis_pass:
        print("HYPOTHESIS: SUPPORTED")
        print("  2+1D symmetric growth is self-regulating and Born-compliant.")
    else:
        failures = []
        if shape_result == "COLLAPSED":
            failures.append("graph collapsed")
        if born_result == "FAIL":
            failures.append("Born fails")
        if gravity_result == "FAIL":
            failures.append("gravity AWAY")
        print("HYPOTHESIS: FALSIFIED")
        print(f"  Failures: {', '.join(failures)}")

    print()
    print(f"F_prop_M metric: growth={shape_result}, born={born_result}, "
          f"gravity={gravity_result}, overlap={static_result}")


if __name__ == "__main__":
    main()
