#!/usr/bin/env python3
"""Local Lorentzian beam-splitter unitary: phase advance + mixing suppression.

THE CHALLENGE:
  Build a propagator that is:
  1. LOCAL (sparse - each node connects only to near neighbors)
  2. UNITARY per layer (norm preserved)
  3. Has LOCALIZED mass (field varies by position and layer)
  4. Passes the BARRIER/SLIT Born test (not just linearity of fixed U)

APPROACH: BEAM-SPLITTER BRICK-WALL UNITARY
  Instead of polar decomposition (dense U), build the unitary layer operator
  as a product of LOCAL 2x2 unitary operations on overlapping neighborhoods.

  Each layer transition:
    Step A: Phase kick at each site: psi(y) -> exp(i*k*S(x,y)) * psi(y)
    Step B: Beam-splitter mixing on even pairs (0,1), (2,3), ...
    Step C: Beam-splitter mixing on odd pairs  (1,2), (3,4), ...

  Each step is unitary. Product of unitary steps is unitary.

  The 2x2 unitary for pair (y, y+1):
    [[cos(alpha), -sin(alpha)],
     [sin(alpha),  cos(alpha)]]

  where alpha controls transverse spreading (calibrated from angular kernel).

FIELD:
  f(x, y) = strength / sqrt((x - x_mass)^2 + (y - y_mass)^2 + eps)
  Localized mass, NOT a global medium.

TESTS:
  1. Norm preservation: ||psi||^2 at each layer
  2. Barrier/slit Born (Sorkin I3): 3-slit barrier, all 7 configurations
  3. Gravity: centroid shift with mass vs without
  4. Spectral averaging: sweep k, equal-amplitude sum
  5. Signal speed: finite light cone from locality

HYPOTHESIS: "A local Lorentzian beam-splitter unitary preserves the barrier
Born test and flips the gravity sign TOWARD mass."
FALSIFICATION: "If Born stays good but gravity remains AWAY."
"""
from __future__ import annotations

import math
import time
import numpy as np

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
HEIGHT = 8          # half-width of transverse dimension
N_Y = 2 * HEIGHT + 1  # 17 transverse sites
N_LAYERS = 20       # forward propagation layers
ALPHA = 0.3         # beam-splitter mixing angle (~9% amplitude to each neighbor)
STRENGTH = 5e-4     # mass field strength
MASS_X = 10         # mass layer position
MASS_Y = HEIGHT + 4 # mass transverse position (offset from center)
K_DEFAULT = 5.0     # default wavenumber
EPS = 0.01          # field softening
K_VALUES = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0]
GAMMA_SWEEP = [0.0, 25.0, 50.0, 100.0, 150.0, 200.0, 300.0]

# ---------------------------------------------------------------------------
# Field construction
# ---------------------------------------------------------------------------
def make_field_flat(n_layers, n_y):
    """Zero field everywhere."""
    return np.zeros((n_layers, n_y))


def make_field_mass(n_layers, n_y, x_mass, y_mass, strength):
    """Localized mass: f = strength / sqrt(r^2 + eps)."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            r2 = (x - x_mass) ** 2 + (y - y_mass) ** 2
            field[x, y] = strength / math.sqrt(r2 + EPS)
    return field


def pair_alpha(alpha_base, f_pair, mix_gamma):
    """Local Lorentzian suppression of transverse spreading near mass."""
    return max(0.0, alpha_base * (1.0 - mix_gamma * f_pair))


# ---------------------------------------------------------------------------
# Local unitary propagator
# ---------------------------------------------------------------------------
def propagate_local_unitary(n_y, n_layers, k, field, blocked=None, alpha=ALPHA):
    """Propagate using local beam-splitter brick-wall unitary.

    Args:
        n_y: number of transverse sites
        n_layers: number of forward layers
        k: wavenumber
        field: (n_layers, n_y) array of field values
        blocked: dict mapping layer_index -> set of blocked sites
                 (amplitude at blocked sites is zeroed after phase kick)
        alpha: beam-splitter mixing angle

    Returns:
        psi_history: list of psi arrays at each layer (length n_layers+1)
    """
    if blocked is None:
        blocked = {}

    psi = np.zeros(n_y, dtype=complex)
    psi[n_y // 2] = 1.0  # source at center

    history = [psi.copy()]
    ca = math.cos(alpha)
    sa = math.sin(alpha)

    for layer in range(n_layers):
        # Step A: Phase kick (diagonal unitary)
        for y in range(n_y):
            f = field[layer, y]
            S = 1.0 * (1.0 - f)  # L=1, valley-linear action
            psi[y] *= np.exp(1j * k * S)

        # Apply barrier: zero amplitude at blocked sites
        if layer in blocked:
            for y in blocked[layer]:
                psi[y] = 0.0

        # Step B: Beam-splitter mixing (even pairs)
        for y in range(0, n_y - 1, 2):
            # Skip mixing if either site is blocked at this layer
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            a, b = psi[y], psi[y + 1]
            psi[y] = ca * a - sa * b
            psi[y + 1] = sa * a + ca * b

        # Step C: Beam-splitter mixing (odd pairs)
        for y in range(1, n_y - 1, 2):
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            a, b = psi[y], psi[y + 1]
            psi[y] = ca * a - sa * b
            psi[y + 1] = sa * a + ca * b

        history.append(psi.copy())

    return history


def propagate_vectorized(
    n_y,
    n_layers,
    k,
    field,
    blocked=None,
    alpha=ALPHA,
    phase_sign=-1.0,
    mix_gamma=0.0,
):
    """Vectorized version for speed."""
    if blocked is None:
        blocked = {}

    psi = np.zeros(n_y, dtype=complex)
    psi[n_y // 2] = 1.0

    history = [psi.copy()]

    for layer in range(n_layers):
        # Step A: Phase kick
        S = 1.0 + phase_sign * field[layer, :]
        psi *= np.exp(1j * k * S)

        # Apply barrier
        if layer in blocked:
            for y in blocked[layer]:
                psi[y] = 0.0

        # Step B: Even pairs
        even_max = n_y - 1 if n_y % 2 == 0 else n_y - 2
        for y in range(0, even_max, 2):
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            f_pair = 0.5 * (field[layer, y] + field[layer, y + 1])
            alpha_eff = pair_alpha(alpha, f_pair, mix_gamma)
            ca = math.cos(alpha_eff)
            sa = math.sin(alpha_eff)
            a, b = psi[y], psi[y + 1]
            psi[y] = ca * a - sa * b
            psi[y + 1] = sa * a + ca * b

        # Step C: Odd pairs
        odd_max = n_y - 1
        for y in range(1, odd_max, 2):
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            f_pair = 0.5 * (field[layer, y] + field[layer, y + 1])
            alpha_eff = pair_alpha(alpha, f_pair, mix_gamma)
            ca = math.cos(alpha_eff)
            sa = math.sin(alpha_eff)
            a, b = psi[y], psi[y + 1]
            psi[y] = ca * a - sa * b
            psi[y + 1] = sa * a + ca * b

        history.append(psi.copy())

    return history


# ---------------------------------------------------------------------------
# Centroid and detection
# ---------------------------------------------------------------------------
def centroid(psi, n_y):
    """Probability-weighted centroid of transverse position."""
    probs = np.abs(psi) ** 2
    total = probs.sum()
    if total < 1e-30:
        return n_y / 2.0
    positions = np.arange(n_y, dtype=float)
    return np.dot(positions, probs) / total


def detection_prob(psi):
    """Total detection probability."""
    return np.sum(np.abs(psi) ** 2)


# ---------------------------------------------------------------------------
# TEST 1: Norm preservation
# ---------------------------------------------------------------------------
def test_norm(n_y, n_layers, k, field, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """Check that norm is preserved at every layer."""
    print(f"\n  TEST 1: Norm preservation")
    print(f"  {'-'*50}")

    history = propagate_vectorized(
        n_y, n_layers, k, field, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
    )
    norms = [np.sum(np.abs(psi) ** 2) for psi in history]

    print(f"    Layer  0: ||psi||^2 = {norms[0]:.15f}")
    for i in [1, 5, 10, 15, 19, 20]:
        if i < len(norms):
            print(f"    Layer {i:2d}: ||psi||^2 = {norms[i]:.15f}")

    max_dev = max(abs(n - 1.0) for n in norms)
    passed = max_dev < 1e-12
    print(f"    Max deviation from 1: {max_dev:.2e}")
    print(f"    {'PASS' if passed else 'FAIL'}")

    return passed, norms


# ---------------------------------------------------------------------------
# TEST 2: Born rule / Sorkin I3 (barrier/slit test)
# ---------------------------------------------------------------------------
def test_born_sorkin(n_y, n_layers, k, field, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """3-slit Sorkin test: I3 = P(ABC) - P(AB) - P(AC) - P(BC) + P(A) + P(B) + P(C).

    Place barrier at layer x_barrier. Three slits at positions slit_A, slit_B, slit_C.
    For each configuration, block all barrier sites EXCEPT the open slits.
    The propagator CHANGES per configuration because blocked sites affect mixing.
    """
    print(f"\n  TEST 2: Born rule / Sorkin I3 (barrier/slit test)")
    print(f"  {'-'*50}")

    x_barrier = n_layers // 3  # barrier at layer 6 or 7
    center = n_y // 2

    # Three slit positions (well separated)
    slit_A = center - 3
    slit_B = center
    slit_C = center + 3

    all_sites = set(range(n_y))

    def make_blocked(open_slits):
        """Create blocked dict: block all sites at barrier layer except open slits."""
        blocked_sites = all_sites - set(open_slits)
        return {x_barrier: blocked_sites}

    configs = {
        "ABC": [slit_A, slit_B, slit_C],
        "AB":  [slit_A, slit_B],
        "AC":  [slit_A, slit_C],
        "BC":  [slit_B, slit_C],
        "A":   [slit_A],
        "B":   [slit_B],
        "C":   [slit_C],
    }

    # Detector: total probability at the final layer
    probs = {}
    for name, open_slits in configs.items():
        blocked = make_blocked(open_slits)
        history = propagate_vectorized(
            n_y, n_layers, k, field, blocked=blocked, alpha=alpha,
            phase_sign=phase_sign, mix_gamma=mix_gamma
        )
        psi_final = history[-1]
        probs[name] = detection_prob(psi_final)

    # I3 = P(ABC) - P(AB) - P(AC) - P(BC) + P(A) + P(B) + P(C)
    I3 = (probs["ABC"]
          - probs["AB"] - probs["AC"] - probs["BC"]
          + probs["A"] + probs["B"] + probs["C"])

    print(f"    Barrier at layer {x_barrier}")
    print(f"    Slits at y = {slit_A}, {slit_B}, {slit_C}")
    print(f"    P(ABC) = {probs['ABC']:.8f}")
    print(f"    P(AB)  = {probs['AB']:.8f}")
    print(f"    P(AC)  = {probs['AC']:.8f}")
    print(f"    P(BC)  = {probs['BC']:.8f}")
    print(f"    P(A)   = {probs['A']:.8f}")
    print(f"    P(B)   = {probs['B']:.8f}")
    print(f"    P(C)   = {probs['C']:.8f}")
    print(f"    I3 = {I3:.2e}")

    # Normalize by P(ABC) for relative measure
    if probs["ABC"] > 1e-30:
        I3_rel = abs(I3) / probs["ABC"]
        print(f"    |I3| / P(ABC) = {I3_rel:.2e}")
    else:
        I3_rel = abs(I3)

    passed = abs(I3) < 0.01
    print(f"    {'PASS' if passed else 'FAIL'} (threshold: |I3| < 0.01)")

    return passed, I3, probs


# ---------------------------------------------------------------------------
# TEST 2b: Born rule with wider slits (2-site slits)
# ---------------------------------------------------------------------------
def test_born_wide_slits(n_y, n_layers, k, field, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """3-slit Sorkin test with 2-site-wide slits for more amplitude throughput."""
    print(f"\n  TEST 2b: Born rule / Sorkin I3 (wide slits)")
    print(f"  {'-'*50}")

    x_barrier = n_layers // 3
    center = n_y // 2

    # Three 2-site-wide slits
    slit_A = [center - 4, center - 3]
    slit_B = [center - 1, center]
    slit_C = [center + 3, center + 4]

    all_sites = set(range(n_y))

    def make_blocked(open_slits_list):
        open_set = set()
        for s in open_slits_list:
            if isinstance(s, list):
                open_set.update(s)
            else:
                open_set.add(s)
        blocked_sites = all_sites - open_set
        return {x_barrier: blocked_sites}

    configs = {
        "ABC": slit_A + slit_B + slit_C,
        "AB":  slit_A + slit_B,
        "AC":  slit_A + slit_C,
        "BC":  slit_B + slit_C,
        "A":   slit_A,
        "B":   slit_B,
        "C":   slit_C,
    }

    probs = {}
    for name, open_sites in configs.items():
        blocked = make_blocked(open_sites)
        history = propagate_vectorized(
            n_y, n_layers, k, field, blocked=blocked, alpha=alpha,
            phase_sign=phase_sign, mix_gamma=mix_gamma
        )
        psi_final = history[-1]
        probs[name] = detection_prob(psi_final)

    I3 = (probs["ABC"]
          - probs["AB"] - probs["AC"] - probs["BC"]
          + probs["A"] + probs["B"] + probs["C"])

    print(f"    Barrier at layer {x_barrier}")
    print(f"    Slit A: y={slit_A}, B: y={slit_B}, C: y={slit_C}")
    print(f"    P(ABC) = {probs['ABC']:.8f}")
    print(f"    P(AB)  = {probs['AB']:.8f}")
    print(f"    P(AC)  = {probs['AC']:.8f}")
    print(f"    P(BC)  = {probs['BC']:.8f}")
    print(f"    P(A)   = {probs['A']:.8f}")
    print(f"    P(B)   = {probs['B']:.8f}")
    print(f"    P(C)   = {probs['C']:.8f}")
    print(f"    I3 = {I3:.2e}")

    if probs["ABC"] > 1e-30:
        I3_rel = abs(I3) / probs["ABC"]
        print(f"    |I3| / P(ABC) = {I3_rel:.2e}")

    passed = abs(I3) < 0.01
    print(f"    {'PASS' if passed else 'FAIL'} (threshold: |I3| < 0.01)")

    return passed, I3, probs


# ---------------------------------------------------------------------------
# TEST 3: Gravity (centroid shift with localized mass)
# ---------------------------------------------------------------------------
def test_gravity_single_k(
    n_y, n_layers, k, field_flat, field_mass, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0
):
    """Check centroid shift toward mass at a single k."""
    print(f"\n  TEST 3: Gravity (single k={k})")
    print(f"  {'-'*50}")

    hist_flat = propagate_vectorized(
        n_y, n_layers, k, field_flat, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
    )
    hist_mass = propagate_vectorized(
        n_y, n_layers, k, field_mass, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
    )

    c_flat = centroid(hist_flat[-1], n_y)
    c_mass = centroid(hist_mass[-1], n_y)
    delta = c_mass - c_flat

    # Mass is at y = MASS_Y = HEIGHT + 4 = 12, center is at HEIGHT = 8
    # So mass is at y > center. Gravity should pull centroid TOWARD mass (positive delta)
    toward = delta > 0
    direction = "TOWARD" if toward else "AWAY"

    print(f"    Flat centroid:  {c_flat:.6f}")
    print(f"    Mass centroid:  {c_mass:.6f}")
    print(f"    Delta:          {delta:+.6e}")
    print(f"    Mass at y={MASS_Y}, center at y={HEIGHT}")
    print(f"    Direction:      {direction}")

    # Also check norm preservation with field
    norm_flat = np.sum(np.abs(hist_flat[-1]) ** 2)
    norm_mass = np.sum(np.abs(hist_mass[-1]) ** 2)
    print(f"    Norm (flat): {norm_flat:.10f}")
    print(f"    Norm (mass): {norm_mass:.10f}")

    passed = toward and abs(delta) > 1e-10
    print(f"    {'PASS' if passed else 'FAIL'}")

    return passed, delta


# ---------------------------------------------------------------------------
# TEST 4: Spectral averaging
# ---------------------------------------------------------------------------
def test_spectral(
    n_y, n_layers, field_flat, field_mass, k_values, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0
):
    """Sweep k values, equal-amplitude sum, check aggregate gravity."""
    print(f"\n  TEST 4: Spectral averaging")
    print(f"  {'-'*50}")

    per_k_shifts = []
    psi_flat_sum = np.zeros(n_y, dtype=complex)
    psi_mass_sum = np.zeros(n_y, dtype=complex)

    for k in k_values:
        hist_flat = propagate_vectorized(
            n_y, n_layers, k, field_flat, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
        )
        hist_mass = propagate_vectorized(
            n_y, n_layers, k, field_mass, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
        )

        psi_flat_sum += hist_flat[-1]
        psi_mass_sum += hist_mass[-1]

        c_flat = centroid(hist_flat[-1], n_y)
        c_mass = centroid(hist_mass[-1], n_y)
        shift = c_mass - c_flat
        toward = "TOWARD" if shift > 0 else "AWAY"
        per_k_shifts.append(shift)
        print(f"    k={k:5.1f}: shift = {shift:+.6e} ({toward})")

    # Aggregate
    c_flat_agg = centroid(psi_flat_sum, n_y)
    c_mass_agg = centroid(psi_mass_sum, n_y)
    delta_agg = c_mass_agg - c_flat_agg
    toward_agg = delta_agg > 0
    direction = "TOWARD" if toward_agg else "AWAY"

    n_toward = sum(1 for s in per_k_shifts if s > 0)
    n_away = sum(1 for s in per_k_shifts if s < 0)

    print(f"    ---")
    print(f"    Per-k: {n_toward} TOWARD, {n_away} AWAY out of {len(k_values)}")
    print(f"    Spectral aggregate shift: {delta_agg:+.6e} ({direction})")

    passed = toward_agg and abs(delta_agg) > 1e-10
    print(f"    {'PASS' if passed else 'FAIL'}")

    return passed, delta_agg, per_k_shifts


# ---------------------------------------------------------------------------
# TEST 5: Signal speed (finite light cone)
# ---------------------------------------------------------------------------
def test_signal_speed(n_y, n_layers, k, field, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """Check that amplitude spreads at bounded rate (locality)."""
    print(f"\n  TEST 5: Signal speed / finite light cone")
    print(f"  {'-'*50}")

    history = propagate_vectorized(
        n_y, n_layers, k, field, alpha=alpha, phase_sign=phase_sign, mix_gamma=mix_gamma
    )
    center = n_y // 2

    spreads = []
    for layer_idx, psi in enumerate(history):
        probs = np.abs(psi) ** 2
        nonzero = np.where(probs > 1e-20)[0]
        if len(nonzero) > 0:
            spread = max(nonzero) - min(nonzero)
        else:
            spread = 0
        spreads.append(spread)

    for i in [0, 1, 2, 5, 10, 15, 20]:
        if i < len(spreads):
            print(f"    Layer {i:2d}: spread = {spreads[i]}")

    # Each layer: even mixing + odd mixing = max 2 sites spread per layer
    # So after L layers, max spread = 2*L
    # Check causality
    causal = True
    for i, s in enumerate(spreads):
        max_allowed = 2 * i + 1  # 1 at layer 0, then +2 per layer
        if s > max_allowed:
            causal = False
            print(f"    VIOLATION at layer {i}: spread={s} > max_allowed={max_allowed}")

    if causal:
        # Check growth rate
        if len(spreads) > 1:
            growths = [spreads[i+1] - spreads[i] for i in range(len(spreads)-1)]
            max_growth = max(growths)
            print(f"    Max growth per layer: {max_growth}")
            print(f"    Expected max growth: 2 (even + odd mixing)")

    print(f"    Causal (bounded spread): {causal}")
    print(f"    {'PASS' if causal else 'FAIL'}")

    return causal, spreads


# ---------------------------------------------------------------------------
# BONUS: Verify unitarity of the layer operator explicitly
# ---------------------------------------------------------------------------
def test_explicit_unitarity(n_y, k, field_one_layer, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """Build the full n_y x n_y matrix for one layer and check UU^dag = I."""
    print(f"\n  BONUS: Explicit unitarity of layer operator")
    print(f"  {'-'*50}")

    n = n_y
    U = np.eye(n, dtype=complex)

    # Apply the layer to each basis vector
    for j in range(n):
        e_j = np.zeros(n, dtype=complex)
        e_j[j] = 1.0

        # Phase kick
        S = 1.0 + phase_sign * field_one_layer
        e_j *= np.exp(1j * k * S)

        # Even mixing
        for y in range(0, n - 1, 2):
            f_pair = 0.5 * (field_one_layer[y] + field_one_layer[y + 1])
            alpha_eff = pair_alpha(alpha, f_pair, mix_gamma)
            ca = math.cos(alpha_eff)
            sa = math.sin(alpha_eff)
            a, b = e_j[y], e_j[y + 1]
            e_j[y] = ca * a - sa * b
            e_j[y + 1] = sa * a + ca * b

        # Odd mixing
        for y in range(1, n - 1, 2):
            f_pair = 0.5 * (field_one_layer[y] + field_one_layer[y + 1])
            alpha_eff = pair_alpha(alpha, f_pair, mix_gamma)
            ca = math.cos(alpha_eff)
            sa = math.sin(alpha_eff)
            a, b = e_j[y], e_j[y + 1]
            e_j[y] = ca * a - sa * b
            e_j[y + 1] = sa * a + ca * b

        U[:, j] = e_j

    # Check UU^dag = I
    I_mat = np.eye(n, dtype=complex)
    err = np.linalg.norm(U @ U.conj().T - I_mat)

    print(f"    Layer operator size: {n}x{n}")
    print(f"    ||UU^dag - I|| = {err:.2e}")

    # Check sparsity: count non-negligible entries per row
    nnz_per_row = []
    for i in range(n):
        nnz = np.sum(np.abs(U[i, :]) > 1e-14)
        nnz_per_row.append(nnz)
    avg_nnz = np.mean(nnz_per_row)
    max_nnz = max(nnz_per_row)
    print(f"    Avg non-zero per row: {avg_nnz:.1f}")
    print(f"    Max non-zero per row: {max_nnz}")
    print(f"    Sparsity: {1 - avg_nnz/n:.1%} zero entries")

    # Bandwidth
    bandwidth = 0
    for i in range(n):
        for j in range(n):
            if abs(U[i, j]) > 1e-14:
                bandwidth = max(bandwidth, abs(i - j))
    print(f"    Matrix bandwidth: {bandwidth}")

    is_unitary = err < 1e-10
    is_sparse = avg_nnz < n * 0.5
    print(f"    Unitary: {is_unitary}")
    print(f"    Sparse:  {is_sparse}")
    print(f"    {'PASS' if is_unitary and is_sparse else 'FAIL'}")

    return is_unitary and is_sparse, err, U


# ---------------------------------------------------------------------------
# BONUS: Norm preservation with barrier (non-unitary due to blocking)
# ---------------------------------------------------------------------------
def test_norm_with_barrier(n_y, n_layers, k, field, alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0):
    """Check norm with barrier - blocking BREAKS unitarity, which is physical."""
    print(f"\n  BONUS: Norm with barrier (absorption expected)")
    print(f"  {'-'*50}")

    x_barrier = n_layers // 3
    center = n_y // 2
    open_slits = [center - 3, center, center + 3]
    all_sites = set(range(n_y))
    blocked = {x_barrier: all_sites - set(open_slits)}

    history = propagate_vectorized(
        n_y, n_layers, k, field, blocked=blocked, alpha=alpha,
        phase_sign=phase_sign, mix_gamma=mix_gamma
    )
    norms = [np.sum(np.abs(psi) ** 2) for psi in history]

    print(f"    Barrier at layer {x_barrier}, 3 slits open")
    for i in [0, x_barrier - 1, x_barrier, x_barrier + 1, n_layers]:
        if i < len(norms):
            print(f"    Layer {i:2d}: ||psi||^2 = {norms[i]:.8f}")

    # Norm should drop at barrier (absorption) but stay constant before and after
    pre_barrier_const = all(abs(norms[i] - norms[i-1]) < 1e-12
                           for i in range(1, x_barrier))
    post_barrier_const = all(abs(norms[i] - norms[i-1]) < 1e-12
                            for i in range(x_barrier + 2, len(norms)))
    norm_drops = norms[x_barrier + 1] < norms[x_barrier]

    print(f"    Pre-barrier norm constant:  {pre_barrier_const}")
    print(f"    Norm drops at barrier:      {norm_drops}")
    print(f"    Post-barrier norm constant: {post_barrier_const}")

    passed = pre_barrier_const and norm_drops and post_barrier_const
    print(f"    {'PASS' if passed else 'FAIL'} (expected: norm drops at barrier, constant otherwise)")

    return passed, norms


# ===================================================================
# MAIN
# ===================================================================
def main():
    print("=" * 72)
    print("LOCAL LORENTZIAN UNITARY: BEAM-SPLITTER PHASE-ADVANCE FORK")
    print("=" * 72)
    print()
    print("Hypothesis: advancing the local phase near mass and suppressing")
    print("transverse mixing can flip the beam-splitter gravity sign TOWARD")
    print("without breaking the barrier Born test or unitarity.")
    print()
    print("Approach: compare the Euclidean phase kick S=1-f against a")
    print("Lorentzian fork S=1+f with pairwise alpha -> alpha*(1-gamma*f_pair).")
    print()

    t0 = time.time()

    print(f"Parameters:")
    print(f"  N_Y = {N_Y} (transverse sites)")
    print(f"  N_LAYERS = {N_LAYERS}")
    print(f"  ALPHA = {ALPHA} (mixing angle)")
    print(f"  K = {K_DEFAULT}")
    print(f"  STRENGTH = {STRENGTH}")
    print(f"  Mass at ({MASS_X}, {MASS_Y})")
    print()

    field_flat = make_field_flat(N_LAYERS, N_Y)
    field_mass = make_field_mass(N_LAYERS, N_Y, MASS_X, MASS_Y, STRENGTH)

    print("=" * 72)
    print("REFERENCE AND GAMMA SWEEP")
    print("=" * 72)
    print()
    ref_single_pass, ref_single = test_gravity_single_k(
        N_Y, N_LAYERS, K_DEFAULT, field_flat, field_mass,
        alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0
    )
    ref_spec_pass, ref_spec, _ = test_spectral(
        N_Y, N_LAYERS, field_flat, field_mass, K_VALUES,
        alpha=ALPHA, phase_sign=-1.0, mix_gamma=0.0
    )

    print()
    print(f"{'variant':<28} {'gamma':>7} {'single-k':>14} {'spectral':>14}")
    print("-" * 68)
    print(f"{'Euclidean reference':<28} {0.0:7.1f} {ref_single:+14.6e} {ref_spec:+14.6e}")

    sweep_rows = []
    for gamma in GAMMA_SWEEP:
        _, single = test_gravity_single_k(
            N_Y, N_LAYERS, K_DEFAULT, field_flat, field_mass,
            alpha=ALPHA, phase_sign=+1.0, mix_gamma=gamma
        )
        _, spectral, per_k = test_spectral(
            N_Y, N_LAYERS, field_flat, field_mass, K_VALUES,
            alpha=ALPHA, phase_sign=+1.0, mix_gamma=gamma
        )
        n_toward = sum(1 for s in per_k if s > 0)
        sweep_rows.append((gamma, single, spectral, n_toward))
        print(f"{'Lorentzian phase+mix':<28} {gamma:7.1f} {single:+14.6e} {spectral:+14.6e}")

    best_gamma, best_single, best_spec, best_count = max(sweep_rows, key=lambda r: (r[1], r[2]))

    print()
    print(f"Best Lorentzian candidate by single-k shift: gamma={best_gamma:.1f}")
    print(f"  single-k shift = {best_single:+.6e}")
    print(f"  spectral shift = {best_spec:+.6e}")
    print(f"  per-k TOWARD = {best_count}/{len(K_VALUES)}")

    print()
    print("=" * 72)
    print("FULL SUITE ON BEST LORENTZIAN CANDIDATE")
    print("=" * 72)

    norm_pass, norms = test_norm(
        N_Y, N_LAYERS, K_DEFAULT, field_mass,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    born_pass, I3, _ = test_born_sorkin(
        N_Y, N_LAYERS, K_DEFAULT, field_flat,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    born_wide_pass, I3_wide, _ = test_born_wide_slits(
        N_Y, N_LAYERS, K_DEFAULT, field_flat,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    grav_pass, grav_shift = test_gravity_single_k(
        N_Y, N_LAYERS, K_DEFAULT, field_flat, field_mass,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    spec_pass, spec_shift, per_k = test_spectral(
        N_Y, N_LAYERS, field_flat, field_mass, K_VALUES,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    speed_pass, spreads = test_signal_speed(
        N_Y, N_LAYERS, K_DEFAULT, field_flat,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    unit_pass, unit_err, _ = test_explicit_unitarity(
        N_Y, K_DEFAULT, field_mass[MASS_X, :],
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )
    barrier_norm_pass, _ = test_norm_with_barrier(
        N_Y, N_LAYERS, K_DEFAULT, field_flat,
        alpha=ALPHA, phase_sign=+1.0, mix_gamma=best_gamma
    )

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    results = {
        "Norm preservation": norm_pass,
        "Born I3 (narrow slits)": born_pass,
        "Born I3 (wide slits)": born_wide_pass,
        "Gravity (single k)": grav_pass,
        "Spectral gravity": spec_pass,
        "Signal speed (locality)": speed_pass,
        "Explicit unitarity": unit_pass,
        "Barrier norm behavior": barrier_norm_pass,
    }
    details = {
        "Norm preservation": f"max dev = {max(abs(n-1) for n in norms):.2e}",
        "Born I3 (narrow slits)": f"I3 = {I3:.2e}",
        "Born I3 (wide slits)": f"I3 = {I3_wide:.2e}",
        "Gravity (single k)": f"shift = {grav_shift:+.2e}",
        "Spectral gravity": f"shift = {spec_shift:+.2e}",
        "Signal speed (locality)": f"bandwidth = {max(spreads)}",
        "Explicit unitarity": f"||UU^dag-I|| = {unit_err:.2e}",
        "Barrier norm behavior": "norm drops at barrier, constant elsewhere",
    }
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {status:4s}  {name} ({details[name]})")

    print()
    print("=" * 72)
    if grav_pass:
        print("Lorentzian beam-splitter SUCCESS: the local phase/mixing fork flips")
        print("single-k gravity TOWARD while preserving the barrier Born pass.")
    else:
        print("Lorentzian beam-splitter remains AWAY at the best tested gamma.")
        print("The phase-advance plus simple mixing-suppression rule is not enough")
        print("to fix the gravity sign on this local architecture.")
    if spec_pass:
        print("Spectral aggregate is TOWARD for the best tested Lorentzian candidate.")
    else:
        print("Spectral aggregate is still not TOWARD.")
    if not speed_pass:
        print("Locality is still limited by the brick-wall spread bound in this implementation.")
    print("=" * 72)

    print(f"\nTotal time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
