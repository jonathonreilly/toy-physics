#!/usr/bin/env python3
"""
frontier_chiral_growth_parametric.py
====================================
2+1D chiral quantum walk with PARAMETRIC symmetric coin.

The Grover coin refocuses every 4 layers, trivializing the growth graph.
A symmetric coin C = [[cos t, i sin t],[i sin t, cos t]] with irrational
angle t = 0.3 (irrational ratio with pi) prevents exact revival, giving
richer growth structure.

HYPOTHESIS: "Parametric symmetric coin gives self-regulating growth
             with testable gravity."
FALSIFICATION: "If the graph still collapses or Born fails."
"""

import numpy as np
from itertools import product as iprod

# ── parameters ──────────────────────────────────────────────────────
N        = 31          # grid per dimension
N_LAYERS = 20          # growth layers
THRESH   = 0.03        # site-keep threshold (fraction of max P)
STRENGTH = 5e-4        # Lorentzian field strength
Z_OFF    = 4           # mass offset for gravity test
THETAS   = [0.2, 0.3, 0.5, np.pi/4, 1/np.sqrt(2)]
THETA_LABELS = ["0.2", "0.3", "0.5", "pi/4", "1/sqrt2"]

# ── helpers ─────────────────────────────────────────────────────────

def make_coin(theta):
    """2x2 symmetric coin block."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 1j*s],
                     [1j*s, c]], dtype=complex)

def build_4x4_coin(theta):
    """
    4-component coin for 2D walk.
    Tensor product of 2x2 symmetric coins for x and y directions.
    Components: (Lx,Ly), (Lx,Ry), (Rx,Ly), (Rx,Ry)
    """
    c2 = make_coin(theta)
    return np.kron(c2, c2)  # 4x4

def shift_2d(psi, N):
    """
    Shift operator for 2D walk with 4 internal states.
    psi shape: (4, N, N)
    Component 0 (Lx,Ly): shift x-1, y-1
    Component 1 (Lx,Ry): shift x-1, y+1
    Component 2 (Rx,Ly): shift x+1, y-1
    Component 3 (Rx,Ry): shift x+1, y+1
    """
    out = np.zeros_like(psi)
    out[0] = np.roll(np.roll(psi[0], -1, axis=0), -1, axis=1)  # Lx,Ly
    out[1] = np.roll(np.roll(psi[1], -1, axis=0), +1, axis=1)  # Lx,Ry
    out[2] = np.roll(np.roll(psi[2], +1, axis=0), -1, axis=1)  # Rx,Ly
    out[3] = np.roll(np.roll(psi[3], +1, axis=0), +1, axis=1)  # Rx,Ry
    return out

def apply_coin(psi, coin_4x4, N):
    """Apply 4x4 coin at every site."""
    # psi shape (4, N, N) -> reshape to (4, N*N), apply coin, reshape back
    flat = psi.reshape(4, -1)
    out = coin_4x4 @ flat
    return out.reshape(4, N, N)

def prob_density(psi):
    """Total probability at each site."""
    return np.sum(np.abs(psi)**2, axis=0)

def symmetric_source(N):
    """Equal amplitude on all 4 components at center."""
    psi = np.zeros((4, N, N), dtype=complex)
    cx, cy = N // 2, N // 2
    amp = 0.5  # 1/sqrt(4)
    for c in range(4):
        psi[c, cx, cy] = amp
    return psi

def grow_graph(theta, N, n_layers, threshold):
    """
    Grow graph layer by layer.
    Returns: list of (layer_index, n_active_sites, active_mask) tuples,
             and the final psi.
    """
    psi = symmetric_source(N)
    coin = build_4x4_coin(theta)
    history = []

    for layer in range(n_layers):
        P = prob_density(psi)
        max_P = P.max()
        if max_P < 1e-30:
            break
        mask = P > threshold * max_P
        n_active = int(mask.sum())
        history.append((layer, n_active, mask.copy()))

        # Zero out sites below threshold (prune)
        for c in range(4):
            psi[c] *= mask

        # Renormalize
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        if norm > 1e-30:
            psi /= norm

        # One step: coin then shift
        psi = apply_coin(psi, coin, N)
        psi = shift_2d(psi, N)

    # Final layer
    P = prob_density(psi)
    max_P = P.max()
    if max_P > 1e-30:
        mask = P > threshold * max_P
        history.append((n_layers, int(mask.sum()), mask.copy()))

    return history, psi

# ── TEST 1: Growth shape stability ──────────────────────────────────

def test_growth_shape():
    """Check if growth stabilizes without periodic collapse for each theta."""
    print("=" * 70)
    print("TEST 1: GROWTH SHAPE STABILITY")
    print("=" * 70)

    results = {}
    for theta, label in zip(THETAS, THETA_LABELS):
        history, _ = grow_graph(theta, N, N_LAYERS, THRESH)
        sizes = [h[1] for h in history]

        # Check for collapse: size drops below 50% of max after initial growth
        max_size = max(sizes[2:]) if len(sizes) > 2 else max(sizes)
        min_after_peak = min(sizes[2:]) if len(sizes) > 2 else min(sizes)
        collapse_ratio = min_after_peak / max_size if max_size > 0 else 0

        # Check for periodicity: autocorrelation of size sequence
        if len(sizes) > 8:
            s = np.array(sizes[2:], dtype=float)
            s -= s.mean()
            if np.std(s) > 0:
                ac = np.correlate(s, s, mode='full')
                ac = ac[len(ac)//2:]
                ac /= ac[0] if ac[0] > 0 else 1
                # Check for strong revival at lag 4 (Grover-like)
                revival_4 = ac[4] if len(ac) > 4 else 0
            else:
                revival_4 = 0
        else:
            revival_4 = 0

        stable = collapse_ratio > 0.4
        non_periodic = abs(revival_4) < 0.5

        results[label] = {
            'sizes': sizes,
            'collapse_ratio': collapse_ratio,
            'revival_4': revival_4,
            'stable': stable,
            'non_periodic': non_periodic,
            'PASS': stable and non_periodic,
        }

        tag = "PASS" if results[label]['PASS'] else "FAIL"
        print(f"  theta={label:>8s}: sizes={sizes[:5]}...{sizes[-3:]}, "
              f"collapse_ratio={collapse_ratio:.3f}, "
              f"revival_4={revival_4:.3f} [{tag}]")

    return results

# ── TEST 2: Born rule (3-slit Sorkin test) ──────────────────────────

def run_walk_with_mask(theta, slit_mask, N, steps=10):
    """Run walk on grown graph with slit mask applied at midplane."""
    psi = symmetric_source(N)
    coin = build_4x4_coin(theta)

    for step in range(steps):
        # Apply growth pruning
        P = prob_density(psi)
        max_P = P.max()
        if max_P > 1e-30:
            gmask = P > THRESH * max_P
            for c in range(4):
                psi[c] *= gmask

        # Apply slit mask at midplane (x = N//2 +/- 2)
        mid = N // 2
        for dx in range(-2, 3):
            ix = mid + dx
            if 0 <= ix < N:
                for c in range(4):
                    psi[c, ix, :] *= slit_mask

        norm = np.sqrt(np.sum(np.abs(psi)**2))
        if norm > 1e-30:
            psi /= norm

        psi = apply_coin(psi, coin, N)
        psi = shift_2d(psi, N)

    return prob_density(psi)

def test_born_rule(theta=0.3):
    """
    3-slit Sorkin test: I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
    Born rule requires |I3| ~ 0 relative to P_ABC.
    """
    print("\n" + "=" * 70)
    print(f"TEST 2: BORN RULE (3-slit Sorkin, theta={theta})")
    print("=" * 70)

    mid_y = N // 2
    slit_positions = [mid_y - 4, mid_y, mid_y + 4]  # 3 slits in y

    def make_slit_mask(open_slits):
        """Create mask: 1 at open slit positions +/- 1, 0 elsewhere near midplane."""
        mask = np.zeros(N)
        for s in open_slits:
            for dy in range(-1, 2):
                iy = s + dy
                if 0 <= iy < N:
                    mask[iy] = 1.0
        return mask

    combos = {
        'ABC': [0, 1, 2],
        'AB':  [0, 1],
        'AC':  [0, 2],
        'BC':  [1, 2],
        'A':   [0],
        'B':   [1],
        'C':   [2],
    }

    probs = {}
    for name, slits in combos.items():
        open_pos = [slit_positions[i] for i in slits]
        smask = make_slit_mask(open_pos)
        P = run_walk_with_mask(theta, smask, N, steps=10)
        probs[name] = P

    # Sorkin parameter at each site, then sum
    I3 = (probs['ABC'] - probs['AB'] - probs['AC'] - probs['BC']
          + probs['A'] + probs['B'] + probs['C'])

    kappa = np.sum(np.abs(I3)) / (np.sum(probs['ABC']) + 1e-30)

    PASS = kappa < 0.1
    tag = "PASS" if PASS else "FAIL"
    print(f"  kappa (Sorkin) = {kappa:.6f}  [{tag}]")
    print(f"  |I3|_max       = {np.max(np.abs(I3)):.6e}")
    print(f"  sum(P_ABC)     = {np.sum(probs['ABC']):.6e}")
    return kappa, PASS

# ── TEST 3: Gravity (Lorentzian field on grown graph) ───────────────

def test_gravity(theta=0.3):
    """
    Apply Lorentzian phase field phi(x,y) = strength / sqrt((x-cx)^2 + (y-cy-z_off)^2 + 1)
    to the walk on the grown graph. Measure centroid shift TOWARD mass.
    """
    print("\n" + "=" * 70)
    print(f"TEST 3: GRAVITY (Lorentzian field, theta={theta})")
    print("=" * 70)

    cx, cy = N // 2, N // 2
    # Mass placed at (cx, cy + Z_OFF)
    mx, my = cx, cy + Z_OFF

    # Build Lorentzian phase field
    xx, yy = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    r = np.sqrt((xx - mx)**2 + (yy - my)**2 + 1.0)
    phi = STRENGTH / r  # phase field

    def run_with_field(use_field):
        psi = symmetric_source(N)
        coin = build_4x4_coin(theta)

        for step in range(N_LAYERS):
            # Growth pruning
            P = prob_density(psi)
            max_P = P.max()
            if max_P > 1e-30:
                gmask = P > THRESH * max_P
                for c in range(4):
                    psi[c] *= gmask

            norm = np.sqrt(np.sum(np.abs(psi)**2))
            if norm > 1e-30:
                psi /= norm

            # Apply phase field
            if use_field:
                phase = np.exp(1j * phi)
                for c in range(4):
                    psi[c] *= phase

            psi = apply_coin(psi, coin, N)
            psi = shift_2d(psi, N)

        return prob_density(psi)

    P_flat = run_with_field(False)
    P_grav = run_with_field(True)

    # Centroid in y direction
    ycoords = np.arange(N)
    cy_flat = np.sum(P_flat * yy) / (np.sum(P_flat) + 1e-30)
    cy_grav = np.sum(P_grav * yy) / (np.sum(P_grav) + 1e-30)

    shift = cy_grav - cy_flat
    toward = shift > 0  # mass is at cy + Z_OFF, so positive shift = toward

    tag = "PASS (TOWARD)" if toward else "FAIL (AWAY)"
    print(f"  centroid_flat = {cy_flat:.6f}")
    print(f"  centroid_grav = {cy_grav:.6f}")
    print(f"  shift         = {shift:+.6f}  [{tag}]")
    print(f"  mass position = y={my}")
    return shift, toward

# ── TEST 4: Theta comparison ────────────────────────────────────────

def test_theta_comparison():
    """Compare growth + gravity across theta values."""
    print("\n" + "=" * 70)
    print("TEST 4: THETA COMPARISON (growth + gravity)")
    print("=" * 70)

    for theta, label in zip(THETAS, THETA_LABELS):
        history, psi = grow_graph(theta, N, N_LAYERS, THRESH)
        sizes = [h[1] for h in history]
        final_size = sizes[-1] if sizes else 0

        # Quick gravity test
        cx, cy = N // 2, N // 2
        mx, my = cx, cy + Z_OFF
        xx, yy = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
        r = np.sqrt((xx - mx)**2 + (yy - my)**2 + 1.0)
        phi = STRENGTH / r

        # Run with field
        psi_g = symmetric_source(N)
        coin = build_4x4_coin(theta)
        for step in range(N_LAYERS):
            P = prob_density(psi_g)
            max_P = P.max()
            if max_P > 1e-30:
                gmask = P > THRESH * max_P
                for c in range(4):
                    psi_g[c] *= gmask
            norm_val = np.sqrt(np.sum(np.abs(psi_g)**2))
            if norm_val > 1e-30:
                psi_g /= norm_val
            phase = np.exp(1j * phi)
            for c in range(4):
                psi_g[c] *= phase
            psi_g = apply_coin(psi_g, coin, N)
            psi_g = shift_2d(psi_g, N)

        # Run without field
        psi_f = symmetric_source(N)
        for step in range(N_LAYERS):
            P = prob_density(psi_f)
            max_P = P.max()
            if max_P > 1e-30:
                gmask = P > THRESH * max_P
                for c in range(4):
                    psi_f[c] *= gmask
            norm_val = np.sqrt(np.sum(np.abs(psi_f)**2))
            if norm_val > 1e-30:
                psi_f /= norm_val
            psi_f = apply_coin(psi_f, coin, N)
            psi_f = shift_2d(psi_f, N)

        P_grav = prob_density(psi_g)
        P_flat = prob_density(psi_f)

        cy_f = np.sum(P_flat * yy) / (np.sum(P_flat) + 1e-30)
        cy_g = np.sum(P_grav * yy) / (np.sum(P_grav) + 1e-30)
        shift = cy_g - cy_f
        toward = shift > 0

        tag = "TOWARD" if toward else "AWAY"
        print(f"  theta={label:>8s}: final_size={final_size:4d}, "
              f"shift={shift:+.6f} [{tag}]")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("FRONTIER: Chiral Growth with Parametric Symmetric Coin")
    print("=" * 70)
    print(f"Grid: {N}x{N}, Layers: {N_LAYERS}, Threshold: {THRESH}")
    print(f"Gravity: strength={STRENGTH}, z_offset={Z_OFF}")
    print(f"Thetas: {THETA_LABELS}")
    print()

    growth_results = test_growth_shape()
    kappa, born_pass = test_born_rule(theta=0.3)
    grav_shift, grav_toward = test_gravity(theta=0.3)
    test_theta_comparison()

    # ── VERDICT ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    best_theta = None
    for label in THETA_LABELS:
        r = growth_results[label]
        if r['PASS']:
            if best_theta is None:
                best_theta = label

    growth_any_pass = any(r['PASS'] for r in growth_results.values())
    print(f"  Growth stable (any theta):    {'PASS' if growth_any_pass else 'FAIL'}")
    print(f"  Born rule (theta=0.3):        {'PASS' if born_pass else 'FAIL'} (kappa={kappa:.6f})")
    print(f"  Gravity TOWARD (theta=0.3):   {'PASS' if grav_toward else 'FAIL'} (shift={grav_shift:+.6f})")
    print(f"  Best theta for growth:        {best_theta or 'NONE'}")

    all_pass = growth_any_pass and born_pass and grav_toward
    print(f"\n  HYPOTHESIS: {'SUPPORTED' if all_pass else 'FALSIFIED'}")
    if not all_pass:
        failures = []
        if not growth_any_pass:
            failures.append("growth collapses for all thetas")
        if not born_pass:
            failures.append(f"Born fails (kappa={kappa:.4f})")
        if not grav_toward:
            failures.append(f"gravity AWAY (shift={grav_shift:+.6f})")
        print(f"  REASON: {'; '.join(failures)}")
