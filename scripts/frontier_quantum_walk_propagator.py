#!/usr/bin/env python3
"""Quantum walk propagator: norm-preserving by construction.

THE IDEA:
  Replace the raw accumulating transfer matrix (non-unitary, spectral radius > 1)
  with a LOCAL SCATTERING / QUANTUM WALK update that is norm-preserving by
  construction.

  In a discrete-time quantum walk:
    1. Each node has an internal state (coin state) for propagation direction
    2. At each step: apply local COIN operation (unitary), then SHIFT along edges
    3. Coin + shift is unitary by construction -> norm preserved -> no amplification

  Coin space: at each node (x, y), amplitude has components for each edge
  direction. For max_d offsets in y, the coin space has (2*max_d + 1) components.

  Coin operation: Grover diffusion operator C = (2/n)*J - I (n x n).
  Shift: move each component along its direction with phase exp(i*k*L*(1-f)).

TESTS:
  1. Norm preservation: is sum |psi|^2 constant across layers?
  2. Born rule: does the 3-slit Sorkin test give I3 ~ 0?
  3. Gravity: does centroid shift TOWARD mass?
  4. Spectral averaging: does broadband gravity survive?
  5. Signal speed: is there a finite light cone?

HYPOTHESIS: "A quantum-walk propagator preserves norm AND produces gravity."
FALSIFICATION: "If Born fails or gravity vanishes on the walk."

Uses pure Python (no numpy). 2D lattice DAG.
"""
from __future__ import annotations

import cmath
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
H = 0.5           # lattice spacing
K = 5.0           # wavenumber
WIDTH = 20        # layers (x direction)
HEIGHT = 21       # transverse sites (y direction), odd for symmetry
MAX_D = 1         # max dy offset per step
N_DIR = 2 * MAX_D + 1  # 3 directions: {-1, 0, 1}

SOURCE_Y = HEIGHT // 2
MASS_POS_Y = HEIGHT // 2 + 2
STRENGTH = 5e-4

# ---------------------------------------------------------------------------
# Grover coin: C = (2/n)*J - I
# ---------------------------------------------------------------------------
def grover_coin(n: int) -> list[list[complex]]:
    """n x n Grover diffusion operator. Unitary by construction."""
    c = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(complex(2.0 / n - 1.0, 0.0))
            else:
                row.append(complex(2.0 / n, 0.0))
        c.append(row)
    return c


def dft_coin(n: int) -> list[list[complex]]:
    """n x n DFT (Fourier) coin. Unitary by construction."""
    c = []
    for i in range(n):
        row = []
        for j in range(n):
            phase = 2.0 * math.pi * i * j / n
            row.append(cmath.exp(1j * phase) / math.sqrt(n))
        c.append(row)
    return c


def matvec(mat: list[list[complex]], vec: list[complex]) -> list[complex]:
    """Matrix-vector multiply."""
    n = len(vec)
    result = [complex(0, 0)] * n
    for i in range(n):
        s = complex(0, 0)
        for j in range(n):
            s += mat[i][j] * vec[j]
        result[i] = s
    return result


# ---------------------------------------------------------------------------
# Edge geometry
# ---------------------------------------------------------------------------
def edge_length(dy: int) -> float:
    """Length of edge from (x, y) to (x+h, y+dy*h)."""
    return math.sqrt(H**2 + (dy * H)**2)


def edge_angle(dy: int) -> float:
    """Angle from forward axis for offset dy."""
    return math.atan2(abs(dy) * H, H)


# ---------------------------------------------------------------------------
# Test 1: Norm preservation
# ---------------------------------------------------------------------------
def test_norm_preservation():
    """Propagate a quantum walk and check norm at each layer."""
    print("=" * 70)
    print("TEST 1: NORM PRESERVATION")
    print("=" * 70)

    coin = grover_coin(N_DIR)

    # State: state[y][dir_idx] = complex amplitude
    # Initialize: source at center, equal in all directions
    state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
    amp = 1.0 / math.sqrt(N_DIR)
    for d in range(N_DIR):
        state[SOURCE_Y][d] = complex(amp, 0)

    initial_norm = sum(abs(state[y][d])**2 for y in range(HEIGHT) for d in range(N_DIR))
    print(f"  Initial norm: {initial_norm:.10f}")

    norms = [initial_norm]

    for layer in range(WIDTH - 1):
        # Step 1: Coin at each node
        for y in range(HEIGHT):
            vec = state[y]
            state[y] = matvec(coin, vec)

        # Step 2: Shift + phase
        new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(N_DIR):
                dy = d_idx - MAX_D  # maps 0,1,2 -> -1,0,1
                y_new = y + dy
                if 0 <= y_new < HEIGHT:
                    L = edge_length(dy)
                    phase = cmath.exp(1j * K * L)
                    new_state[y_new][d_idx] += phase * state[y][d_idx]
                # If y_new out of bounds: amplitude lost (absorbing boundary)

        state = new_state
        norm = sum(abs(state[y][d])**2 for y in range(HEIGHT) for d in range(N_DIR))
        norms.append(norm)

    print(f"  Final norm:   {norms[-1]:.10f}")
    print(f"  Norm ratio (final/initial): {norms[-1] / norms[0]:.10f}")

    # Check norm stability
    max_dev = max(abs(n - norms[0]) / norms[0] for n in norms)
    print(f"  Max relative deviation: {max_dev:.6e}")

    # With absorbing boundaries, some norm leaks at edges
    # Check if it's monotonically decreasing (no amplification!)
    amplified = any(norms[i+1] > norms[i] + 1e-14 for i in range(len(norms)-1))
    print(f"  Any amplification? {amplified}")
    if not amplified:
        print("  PASS: No amplification (norm monotonically non-increasing)")
    else:
        # Find max amplification
        max_amp = max(norms[i+1] - norms[i] for i in range(len(norms)-1))
        print(f"  Max amplification per step: {max_amp:.6e}")

    return norms


# ---------------------------------------------------------------------------
# Test 1b: Norm with reflecting boundaries
# ---------------------------------------------------------------------------
def test_norm_reflecting():
    """Quantum walk with reflecting boundaries: norm should be exactly preserved."""
    print("\n" + "=" * 70)
    print("TEST 1b: NORM WITH REFLECTING BOUNDARIES")
    print("=" * 70)

    coin = grover_coin(N_DIR)

    state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
    amp = 1.0 / math.sqrt(N_DIR)
    for d in range(N_DIR):
        state[SOURCE_Y][d] = complex(amp, 0)

    initial_norm = sum(abs(state[y][d])**2 for y in range(HEIGHT) for d in range(N_DIR))
    print(f"  Initial norm: {initial_norm:.10f}")

    norms = [initial_norm]

    for layer in range(WIDTH - 1):
        # Coin
        for y in range(HEIGHT):
            state[y] = matvec(coin, state[y])

        # Shift with reflecting boundaries
        new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(N_DIR):
                dy = d_idx - MAX_D
                y_new = y + dy
                L = edge_length(dy)
                phase = cmath.exp(1j * K * L)

                if 0 <= y_new < HEIGHT:
                    new_state[y_new][d_idx] += phase * state[y][d_idx]
                else:
                    # Reflect: stay at same y, reverse direction
                    d_reflect = N_DIR - 1 - d_idx  # -1 <-> +1
                    new_state[y][d_reflect] += phase * state[y][d_idx]

        state = new_state
        norm = sum(abs(state[y][d])**2 for y in range(HEIGHT) for d in range(N_DIR))
        norms.append(norm)

    print(f"  Final norm:   {norms[-1]:.10f}")
    print(f"  Norm ratio (final/initial): {norms[-1] / norms[0]:.10f}")

    max_dev = max(abs(n - norms[0]) / norms[0] for n in norms)
    print(f"  Max relative deviation: {max_dev:.6e}")

    preserved = max_dev < 1e-10
    print(f"  NORM EXACTLY PRESERVED: {preserved}")
    if preserved:
        print("  PASS: Reflecting boundary quantum walk preserves norm exactly")
    else:
        print(f"  FAIL: Norm deviates by {max_dev:.6e}")

    return norms, preserved


# ---------------------------------------------------------------------------
# Test 2: Born rule (3-slit Sorkin test)
# ---------------------------------------------------------------------------
def propagate_walk(source_ys: list[int], n_layers: int, coin: list[list[complex]],
                   field_fn=None) -> list[float]:
    """Propagate quantum walk from given source positions.
    Returns probability distribution at final layer.
    field_fn(y) returns field strength at position y (0 = no field).
    """
    state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]

    # Initialize sources
    n_src = len(source_ys)
    amp = 1.0 / math.sqrt(N_DIR * n_src)
    for sy in source_ys:
        for d in range(N_DIR):
            state[sy][d] = complex(amp, 0)

    for layer in range(n_layers):
        # Coin
        for y in range(HEIGHT):
            state[y] = matvec(coin, state[y])

        # Shift with phase (and optional field)
        new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(N_DIR):
                dy = d_idx - MAX_D
                y_new = y + dy
                if 0 <= y_new < HEIGHT:
                    L = edge_length(dy)
                    f = field_fn(y) if field_fn else 0.0
                    phase = cmath.exp(1j * K * L * (1.0 - f))
                    new_state[y_new][d_idx] += phase * state[y][d_idx]

        state = new_state

    # Probability at each y (sum over directions)
    prob = []
    for y in range(HEIGHT):
        p = sum(abs(state[y][d])**2 for d in range(N_DIR))
        prob.append(p)
    return prob


def test_born_rule():
    """3-slit Sorkin test: I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C."""
    print("\n" + "=" * 70)
    print("TEST 2: BORN RULE (3-SLIT SORKIN TEST)")
    print("=" * 70)

    coin = grover_coin(N_DIR)
    cy = HEIGHT // 2
    slits = [cy - 2, cy, cy + 2]  # A, B, C
    n_layers = WIDTH - 1

    # All single, pair, and triple combinations
    p_a = propagate_walk([slits[0]], n_layers, coin)
    p_b = propagate_walk([slits[1]], n_layers, coin)
    p_c = propagate_walk([slits[2]], n_layers, coin)
    p_ab = propagate_walk([slits[0], slits[1]], n_layers, coin)
    p_ac = propagate_walk([slits[0], slits[2]], n_layers, coin)
    p_bc = propagate_walk([slits[1], slits[2]], n_layers, coin)
    p_abc = propagate_walk(slits, n_layers, coin)

    # Sorkin parameter at each detector position
    i3_values = []
    for y in range(HEIGHT):
        i3 = (p_abc[y] - p_ab[y] - p_ac[y] - p_bc[y]
               + p_a[y] + p_b[y] + p_c[y])
        i3_values.append(i3)

    max_i3 = max(abs(v) for v in i3_values)
    sum_p = sum(p_abc)

    # Normalize by total probability
    if sum_p > 0:
        rel_i3 = max_i3 / sum_p
    else:
        rel_i3 = 0.0

    print(f"  Max |I3|:     {max_i3:.6e}")
    print(f"  Total P_ABC:  {sum_p:.6e}")
    print(f"  |I3|/P_total: {rel_i3:.6e}")

    # Born rule: I3 should be zero (within numerical precision)
    born_pass = rel_i3 < 1e-6
    print(f"  Born rule satisfied: {born_pass}")
    if born_pass:
        print("  PASS: I3 ~ 0, consistent with Born rule")
    else:
        print(f"  FAIL: I3/P = {rel_i3:.6e} is too large")

    return rel_i3, born_pass


# ---------------------------------------------------------------------------
# Test 3: Gravity (centroid shift toward mass)
# ---------------------------------------------------------------------------
def test_gravity():
    """Does a mass-coupled field cause centroid deflection?"""
    print("\n" + "=" * 70)
    print("TEST 3: GRAVITY (CENTROID SHIFT TOWARD MASS)")
    print("=" * 70)

    coin = grover_coin(N_DIR)
    n_layers = WIDTH - 1

    # No field
    prob_flat = propagate_walk([SOURCE_Y], n_layers, coin)

    # Field: gravitational potential centered at MASS_POS_Y
    def field_fn(y):
        r = abs(y - MASS_POS_Y) * H
        if r < 0.1:
            r = 0.1
        return STRENGTH / r

    prob_grav = propagate_walk([SOURCE_Y], n_layers, coin, field_fn=field_fn)

    # Centroids
    total_flat = sum(prob_flat)
    total_grav = sum(prob_grav)

    if total_flat > 0:
        centroid_flat = sum(y * prob_flat[y] for y in range(HEIGHT)) / total_flat
    else:
        centroid_flat = SOURCE_Y

    if total_grav > 0:
        centroid_grav = sum(y * prob_grav[y] for y in range(HEIGHT)) / total_grav
    else:
        centroid_grav = SOURCE_Y

    shift = centroid_grav - centroid_flat
    toward_mass = shift > 0  # mass is at higher y

    print(f"  Source y:     {SOURCE_Y}")
    print(f"  Mass y:       {MASS_POS_Y}")
    print(f"  Centroid (flat):   {centroid_flat:.6f}")
    print(f"  Centroid (grav):   {centroid_grav:.6f}")
    print(f"  Shift:             {shift:.6e}")
    print(f"  Toward mass:       {toward_mass}")

    if toward_mass and abs(shift) > 1e-10:
        print("  PASS: Centroid shifts toward mass")
    elif abs(shift) < 1e-10:
        print("  MARGINAL: Shift too small to be conclusive")
    else:
        print("  FAIL: Centroid shifts AWAY from mass")

    return shift, toward_mass


# ---------------------------------------------------------------------------
# Test 4: Spectral averaging (broadband gravity)
# ---------------------------------------------------------------------------
def test_spectral_gravity():
    """Average over multiple k values -- does gravity survive?"""
    print("\n" + "=" * 70)
    print("TEST 4: SPECTRAL AVERAGING (BROADBAND GRAVITY)")
    print("=" * 70)

    coin = grover_coin(N_DIR)
    n_layers = WIDTH - 1
    k_values = [2.0, 3.0, 5.0, 7.0, 10.0, 15.0]

    def field_fn(y):
        r = abs(y - MASS_POS_Y) * H
        if r < 0.1:
            r = 0.1
        return STRENGTH / r

    shifts = []
    for k_val in k_values:
        # Override global K temporarily via propagate_walk_k
        prob_flat = propagate_walk_k([SOURCE_Y], n_layers, coin, k_val)
        prob_grav = propagate_walk_k([SOURCE_Y], n_layers, coin, k_val, field_fn=field_fn)

        total_flat = sum(prob_flat)
        total_grav = sum(prob_grav)

        c_flat = sum(y * prob_flat[y] for y in range(HEIGHT)) / total_flat if total_flat > 0 else SOURCE_Y
        c_grav = sum(y * prob_grav[y] for y in range(HEIGHT)) / total_grav if total_grav > 0 else SOURCE_Y

        shift = c_grav - c_flat
        shifts.append(shift)
        print(f"  k={k_val:5.1f}  shift={shift:+.6e}  toward_mass={shift > 0}")

    avg_shift = sum(shifts) / len(shifts)
    n_toward = sum(1 for s in shifts if s > 0)

    print(f"\n  Average shift: {avg_shift:+.6e}")
    print(f"  Toward mass:   {n_toward}/{len(shifts)}")

    robust = n_toward >= len(shifts) * 0.6
    if robust:
        print("  PASS: Gravity survives spectral averaging")
    else:
        print("  FAIL: Gravity does not survive spectral averaging")

    return avg_shift, robust


def propagate_walk_k(source_ys: list[int], n_layers: int, coin: list[list[complex]],
                     k_val: float, field_fn=None) -> list[float]:
    """Same as propagate_walk but with explicit k value."""
    state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]

    n_src = len(source_ys)
    amp = 1.0 / math.sqrt(N_DIR * n_src)
    for sy in source_ys:
        for d in range(N_DIR):
            state[sy][d] = complex(amp, 0)

    for layer in range(n_layers):
        for y in range(HEIGHT):
            state[y] = matvec(coin, state[y])

        new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(N_DIR):
                dy = d_idx - MAX_D
                y_new = y + dy
                if 0 <= y_new < HEIGHT:
                    L = edge_length(dy)
                    f = field_fn(y) if field_fn else 0.0
                    phase = cmath.exp(1j * k_val * L * (1.0 - f))
                    new_state[y_new][d_idx] += phase * state[y][d_idx]

        state = new_state

    prob = []
    for y in range(HEIGHT):
        p = sum(abs(state[y][d])**2 for d in range(N_DIR))
        prob.append(p)
    return prob


# ---------------------------------------------------------------------------
# Test 5: Light cone (signal speed)
# ---------------------------------------------------------------------------
def test_light_cone():
    """Check that probability spreads at finite speed."""
    print("\n" + "=" * 70)
    print("TEST 5: FINITE LIGHT CONE")
    print("=" * 70)

    coin = grover_coin(N_DIR)

    state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
    amp = 1.0 / math.sqrt(N_DIR)
    for d in range(N_DIR):
        state[SOURCE_Y][d] = complex(amp, 0)

    # Track spread at each layer
    spreads = []
    for layer in range(WIDTH - 1):
        for y in range(HEIGHT):
            state[y] = matvec(coin, state[y])

        new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(N_DIR):
                dy = d_idx - MAX_D
                y_new = y + dy
                if 0 <= y_new < HEIGHT:
                    L = edge_length(dy)
                    phase = cmath.exp(1j * K * L)
                    new_state[y_new][d_idx] += phase * state[y][d_idx]

        state = new_state

        # Find extent of probability
        prob = [sum(abs(state[y][d])**2 for d in range(N_DIR)) for y in range(HEIGHT)]
        threshold = max(prob) * 1e-10 if max(prob) > 0 else 0

        min_y = HEIGHT
        max_y = 0
        for y in range(HEIGHT):
            if prob[y] > threshold:
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        spread = max_y - min_y if max_y >= min_y else 0
        spreads.append(spread)

    print(f"  Source at y={SOURCE_Y}")
    print(f"  Layer-by-layer spread (max_y - min_y):")
    for i, s in enumerate(spreads):
        if i < 10 or i == len(spreads) - 1:
            print(f"    Layer {i+1:2d}: spread = {s}")

    # Max speed: dy=1 per layer, so spread should grow <= 2 per layer
    max_growth = max(spreads[i+1] - spreads[i] for i in range(len(spreads)-1)) if len(spreads) > 1 else 0
    # The spread from source starts at 0, grows by at most 2 per step
    causal = all(spreads[i] <= 2 * (i + 1) for i in range(len(spreads)))

    print(f"\n  Max spread growth per layer: {max_growth}")
    print(f"  Causal (spread <= 2*layer): {causal}")
    if causal:
        print("  PASS: Finite light cone respected")
    else:
        print("  FAIL: Superluminal spread detected")

    return spreads, causal


# ---------------------------------------------------------------------------
# Test 6: Compare Grover vs DFT coin
# ---------------------------------------------------------------------------
def test_coin_comparison():
    """Compare Grover and DFT coins for gravity."""
    print("\n" + "=" * 70)
    print("TEST 6: COIN COMPARISON (GROVER vs DFT)")
    print("=" * 70)

    n_layers = WIDTH - 1

    def field_fn(y):
        r = abs(y - MASS_POS_Y) * H
        if r < 0.1:
            r = 0.1
        return STRENGTH / r

    for name, coin in [("Grover", grover_coin(N_DIR)), ("DFT", dft_coin(N_DIR))]:
        prob_flat = propagate_walk([SOURCE_Y], n_layers, coin)
        prob_grav = propagate_walk([SOURCE_Y], n_layers, coin, field_fn=field_fn)

        total_flat = sum(prob_flat)
        total_grav = sum(prob_grav)

        c_flat = sum(y * prob_flat[y] for y in range(HEIGHT)) / total_flat if total_flat > 0 else SOURCE_Y
        c_grav = sum(y * prob_grav[y] for y in range(HEIGHT)) / total_grav if total_grav > 0 else SOURCE_Y

        shift = c_grav - c_flat
        print(f"  {name:8s} coin:  shift = {shift:+.6e}  toward_mass = {shift > 0}")

        # Norm check
        state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
        amp = 1.0 / math.sqrt(N_DIR)
        for d in range(N_DIR):
            state[SOURCE_Y][d] = complex(amp, 0)

        for layer in range(n_layers):
            for y in range(HEIGHT):
                state[y] = matvec(coin, state[y])
            new_state = [[complex(0, 0)] * N_DIR for _ in range(HEIGHT)]
            for y in range(HEIGHT):
                for d_idx in range(N_DIR):
                    dy = d_idx - MAX_D
                    y_new = y + dy
                    if 0 <= y_new < HEIGHT:
                        L = edge_length(dy)
                        phase = cmath.exp(1j * K * L)
                        new_state[y_new][d_idx] += phase * state[y][d_idx]
            state = new_state

        norm = sum(abs(state[y][d])**2 for y in range(HEIGHT) for d in range(N_DIR))
        print(f"           norm = {norm:.6f} (initial = 1.0)")


# ---------------------------------------------------------------------------
# Test 7: Wider coin (max_d = 2)
# ---------------------------------------------------------------------------
def test_wider_coin():
    """Test with 5-direction coin (max_d=2) for richer dynamics."""
    print("\n" + "=" * 70)
    print("TEST 7: WIDER COIN (5 DIRECTIONS, max_d=2)")
    print("=" * 70)

    max_d_wide = 2
    n_dir_wide = 2 * max_d_wide + 1  # 5
    coin = grover_coin(n_dir_wide)
    n_layers = WIDTH - 1

    def field_fn(y):
        r = abs(y - MASS_POS_Y) * H
        if r < 0.1:
            r = 0.1
        return STRENGTH / r

    # Propagate flat
    state_flat = [[complex(0, 0)] * n_dir_wide for _ in range(HEIGHT)]
    amp = 1.0 / math.sqrt(n_dir_wide)
    for d in range(n_dir_wide):
        state_flat[SOURCE_Y][d] = complex(amp, 0)

    state_grav = [[complex(0, 0)] * n_dir_wide for _ in range(HEIGHT)]
    for d in range(n_dir_wide):
        state_grav[SOURCE_Y][d] = complex(amp, 0)

    norms = []
    for layer in range(n_layers):
        # Coin
        for y in range(HEIGHT):
            state_flat[y] = matvec(coin, state_flat[y])
            state_grav[y] = matvec(coin, state_grav[y])

        # Shift
        new_flat = [[complex(0, 0)] * n_dir_wide for _ in range(HEIGHT)]
        new_grav = [[complex(0, 0)] * n_dir_wide for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for d_idx in range(n_dir_wide):
                dy = d_idx - max_d_wide
                y_new = y + dy
                if 0 <= y_new < HEIGHT:
                    L = math.sqrt(H**2 + (dy * H)**2)
                    phase_flat = cmath.exp(1j * K * L)
                    f = field_fn(y)
                    phase_grav = cmath.exp(1j * K * L * (1.0 - f))
                    new_flat[y_new][d_idx] += phase_flat * state_flat[y][d_idx]
                    new_grav[y_new][d_idx] += phase_grav * state_grav[y][d_idx]

        state_flat = new_flat
        state_grav = new_grav

        norm = sum(abs(state_flat[y][d])**2 for y in range(HEIGHT) for d in range(n_dir_wide))
        norms.append(norm)

    # Results
    prob_flat = [sum(abs(state_flat[y][d])**2 for d in range(n_dir_wide)) for y in range(HEIGHT)]
    prob_grav = [sum(abs(state_grav[y][d])**2 for d in range(n_dir_wide)) for y in range(HEIGHT)]

    total_flat = sum(prob_flat)
    total_grav = sum(prob_grav)

    c_flat = sum(y * prob_flat[y] for y in range(HEIGHT)) / total_flat if total_flat > 0 else SOURCE_Y
    c_grav = sum(y * prob_grav[y] for y in range(HEIGHT)) / total_grav if total_grav > 0 else SOURCE_Y

    shift = c_grav - c_flat
    print(f"  Directions: {n_dir_wide}")
    print(f"  Centroid (flat): {c_flat:.6f}")
    print(f"  Centroid (grav): {c_grav:.6f}")
    print(f"  Shift:           {shift:+.6e}")
    print(f"  Toward mass:     {shift > 0}")
    print(f"  Final norm (flat): {norms[-1]:.6f}")


# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
def main():
    print("QUANTUM WALK PROPAGATOR ON 2D DAG")
    print(f"Parameters: WIDTH={WIDTH}, HEIGHT={HEIGHT}, K={K}, H={H}, MAX_D={MAX_D}")
    print(f"Source: y={SOURCE_Y}, Mass: y={MASS_POS_Y}, Strength={STRENGTH}")
    print()

    norms_absorb = test_norm_preservation()
    norms_reflect, norm_pass = test_norm_reflecting()
    i3_rel, born_pass = test_born_rule()
    shift, grav_pass = test_gravity()
    avg_shift, spectral_pass = test_spectral_gravity()
    spreads, cone_pass = test_light_cone()
    test_coin_comparison()
    test_wider_coin()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    results = [
        ("Norm preservation (reflecting)", norm_pass),
        ("Born rule (I3 ~ 0)", born_pass),
        ("Gravity (centroid toward mass)", grav_pass),
        ("Spectral gravity (broadband)", spectral_pass),
        ("Finite light cone", cone_pass),
    ]

    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}  {name}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("HYPOTHESIS SUPPORTED: Quantum walk preserves norm AND produces gravity.")
    else:
        failed = [name for name, p in results if not p]
        print(f"HYPOTHESIS PARTIALLY SUPPORTED. Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
