#!/usr/bin/env python3
"""
Frontier: Chiral Born Barrier Test — Three Blocking Mechanisms
===============================================================
The previous Born test FAILED (I3=1.0) because blocking sites with
coin=identity + no-shift TRAPS amplitude. This script tests three
correct blocking mechanisms:

  A. Absorption: set psi=0 at blocked sites (removes amplitude)
  B. Reflection: swap chiralities at blocked sites (reverses direction)
  C. Phase scramble: apply fixed random phases at blocked sites

NOTE: The chiral walk preserves parity — source at even y reaches even y
at even layers, odd y at odd layers. Barrier must be at an even layer for
slits at even y-positions to have amplitude.

HYPOTHESIS: "Absorption (mechanism A) gives I3 < 1e-6 because it's linear."
FALSIFICATION: "If I3 > 0.01 for all mechanisms."
"""

import numpy as np
from itertools import combinations

# ── Parameters ──────────────────────────────────────────────────────
N_Y = 21          # height = 10 (sites 0..20)
N_LAYERS = 20
K = 5.0
THETA_0 = 0.3
STRENGTH = 0.0    # flat space for Born test
SOURCE_Y = N_Y // 2  # = 10
BARRIER_LAYER = 8   # even layer so amplitude is at even sites
SLIT_POSITIONS = [8, 10, 12]  # centered on y=10

# Fixed random phases for mechanism C (reproducible)
np.random.seed(42)
SCRAMBLE_PHASES = np.random.uniform(0, 2 * np.pi, (N_Y, 2))


# ── Propagator with barrier mechanisms ─────────────────────────────

def propagate(n_y, n_layers, theta, source_y, barrier_layer,
              open_slits, mechanism):
    """
    Chiral walk with barrier at a specific layer.

    mechanism: 'A' (absorption), 'B' (reflection), 'C' (phase scramble),
               or None (no barrier)
    open_slits: set of y indices that are NOT blocked at the barrier layer
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0  # right-mover at source

    for x in range(n_layers):
        # Step 1: Coin at each site (standard coin everywhere)
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(theta) * pp - np.sin(theta) * pm
            psi[idx_m] = np.sin(theta) * pp + np.cos(theta) * pm

        # Step 1b: Apply blocking mechanism at barrier layer
        if mechanism is not None and x == barrier_layer:
            for y in range(n_y):
                if y not in open_slits:
                    idx_p = 2 * y
                    idx_m = 2 * y + 1
                    if mechanism == 'A':
                        # Absorption: set to zero
                        psi[idx_p] = 0.0
                        psi[idx_m] = 0.0
                    elif mechanism == 'B':
                        # Reflection: swap chiralities
                        psi[idx_p], psi[idx_m] = psi[idx_m], psi[idx_p]
                    elif mechanism == 'C':
                        # Phase scramble: apply fixed random phases
                        psi[idx_p] *= np.exp(1j * SCRAMBLE_PHASES[y, 0])
                        psi[idx_m] *= np.exp(1j * SCRAMBLE_PHASES[y, 1])

        # Step 2: Shift (standard everywhere, no special barrier handling)
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            # Right-mover shifts right
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]  # reflect at boundary
            # Left-mover shifts left
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]  # reflect at boundary
        psi = new_psi

    return psi


def detector_probs(psi, n_y):
    """P(y) = |psi_+(y)|^2 + |psi_-(y)|^2."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


# ── Sorkin I3 test ─────────────────────────────────────────────────

def sorkin_test(mechanism, label):
    """Run 7-configuration Sorkin test for a given mechanism."""
    print(f"\n{'=' * 70}")
    print(f"MECHANISM {label}: {mechanism_name(mechanism)}")
    print(f"{'=' * 70}")

    A, B, C = SLIT_POSITIONS

    def run(open_slits):
        psi = propagate(N_Y, N_LAYERS, THETA_0, SOURCE_Y,
                        BARRIER_LAYER, set(open_slits), mechanism)
        return detector_probs(psi, N_Y)

    # 7 configurations
    P_ABC = run([A, B, C])
    P_AB  = run([A, B])
    P_AC  = run([A, C])
    P_BC  = run([B, C])
    P_A   = run([A])
    P_B   = run([B])
    P_C   = run([C])

    # Sorkin parameter
    I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

    I3_max = np.max(np.abs(I3))
    I3_sum = np.sum(np.abs(I3))
    P_total = np.sum(P_ABC)
    I3_norm = I3_max / P_total if P_total > 1e-30 else float('inf')

    print(f"  Slits: {SLIT_POSITIONS}")
    print(f"  Barrier layer: {BARRIER_LAYER}")
    print(f"  P(ABC) total: {P_total:.6f}")
    print(f"  |I3| max:     {I3_max:.2e}")
    print(f"  |I3| sum:     {I3_sum:.2e}")
    print(f"  |I3|/P:       {I3_norm:.2e}")

    # Norm check
    norms = {}
    for name, slits in [('ABC', [A,B,C]), ('A', [A]), ('B', [B]), ('C', [C])]:
        p = run(slits)
        norms[name] = np.sum(p)
    print(f"\n  Norms: ABC={norms['ABC']:.6f}, A={norms['A']:.6f}, "
          f"B={norms['B']:.6f}, C={norms['C']:.6f}")

    threshold = 1e-6
    status = "PASS" if I3_norm < threshold else "FAIL"
    print(f"\n  *** {status} (|I3|/P = {I3_norm:.2e}, threshold {threshold}) ***")

    return {
        'mechanism': mechanism,
        'label': label,
        'I3_max': I3_max,
        'I3_norm': I3_norm,
        'P_total': P_total,
        'status': status,
        'P_ABC': P_ABC,
        'P_AB': P_AB,
        'P_A': P_A,
        'P_B': P_B,
    }


def mechanism_name(m):
    return {'A': 'Absorption (set to zero)',
            'B': 'Reflection (swap chiralities)',
            'C': 'Phase scramble (fixed random phases)'}[m]


# ── Linearity test for absorption ──────────────────────────────────

def test_linearity():
    """Check U(a+b) = U(a) + U(b) for absorption mechanism."""
    print(f"\n{'=' * 70}")
    print("LINEARITY TEST (Mechanism A)")
    print(f"{'=' * 70}")

    open_slits = set(SLIT_POSITIONS)

    # State a: source at y=9
    psi_a = propagate(N_Y, N_LAYERS, THETA_0, 9,
                      BARRIER_LAYER, open_slits, 'A')

    # State b: source at y=11
    psi_b = propagate(N_Y, N_LAYERS, THETA_0, 11,
                      BARRIER_LAYER, open_slits, 'A')

    # U(a+b): start with superposition
    psi_init = np.zeros(2 * N_Y, dtype=complex)
    psi_init[2 * 9] = 1.0
    psi_init[2 * 11] = 1.0
    # Can't use propagate() directly for custom initial state, so inline:
    psi_ab = _propagate_from_state(psi_init, N_Y, N_LAYERS, THETA_0,
                                    BARRIER_LAYER, open_slits, 'A')

    # Check U(a+b) vs U(a) + U(b)
    diff = psi_ab - (psi_a + psi_b)
    max_diff = np.max(np.abs(diff))

    print(f"  ||U(a+b) - (U(a) + U(b))||_inf = {max_diff:.2e}")
    status = "PASS" if max_diff < 1e-12 else "FAIL"
    print(f"  *** {status} ***")
    return status == "PASS"


def _propagate_from_state(psi_init, n_y, n_layers, theta, barrier_layer,
                           open_slits, mechanism):
    """Propagate from arbitrary initial state."""
    psi = psi_init.copy()

    for x in range(n_layers):
        # Coin
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(theta) * pp - np.sin(theta) * pm
            psi[idx_m] = np.sin(theta) * pp + np.cos(theta) * pm

        # Barrier
        if mechanism is not None and x == barrier_layer:
            for y in range(n_y):
                if y not in open_slits:
                    idx_p = 2 * y
                    idx_m = 2 * y + 1
                    if mechanism == 'A':
                        psi[idx_p] = 0.0
                        psi[idx_m] = 0.0
                    elif mechanism == 'B':
                        psi[idx_p], psi[idx_m] = psi[idx_m], psi[idx_p]
                    elif mechanism == 'C':
                        psi[idx_p] *= np.exp(1j * SCRAMBLE_PHASES[y, 0])
                        psi[idx_m] *= np.exp(1j * SCRAMBLE_PHASES[y, 1])

        # Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]
        psi = new_psi

    return psi


# ── Interference pattern test ──────────────────────────────────────

def test_interference():
    """Check for 2-slit interference fringes."""
    print(f"\n{'=' * 70}")
    print("INTERFERENCE PATTERN TEST")
    print(f"{'=' * 70}")

    A, B, C = SLIT_POSITIONS

    for mechanism in ['A', 'B', 'C']:
        # 2-slit pattern (A and C open, B closed)
        psi_2slit = propagate(N_Y, N_LAYERS, THETA_0, SOURCE_Y,
                              BARRIER_LAYER, {A, C}, mechanism)
        P_2slit = detector_probs(psi_2slit, N_Y)

        # Single slit patterns
        psi_A = propagate(N_Y, N_LAYERS, THETA_0, SOURCE_Y,
                          BARRIER_LAYER, {A}, mechanism)
        P_A = detector_probs(psi_A, N_Y)

        psi_C = propagate(N_Y, N_LAYERS, THETA_0, SOURCE_Y,
                          BARRIER_LAYER, {C}, mechanism)
        P_C = detector_probs(psi_C, N_Y)

        # Classical sum (no interference)
        P_classical = P_A + P_C

        # Interference term
        I2 = P_2slit - P_classical
        I2_max = np.max(np.abs(I2))
        P_max = np.max(P_2slit) if np.max(P_2slit) > 0 else 1.0

        # Visibility: (max - min) / (max + min) in the fringe region
        fringe_region = P_2slit[5:16]  # central region
        if np.max(fringe_region) > 1e-30:
            visibility = ((np.max(fringe_region) - np.min(fringe_region)) /
                          (np.max(fringe_region) + np.min(fringe_region) + 1e-30))
        else:
            visibility = 0.0

        print(f"\n  Mechanism {mechanism} ({mechanism_name(mechanism)}):")
        print(f"    |I2| max (interference):  {I2_max:.6e}")
        print(f"    |I2|/P_max:               {I2_max/P_max:.6e}")
        print(f"    Fringe visibility:         {visibility:.4f}")
        print(f"    P(2-slit) profile: {np.array2string(P_2slit, precision=4, suppress_small=True)}")


# ── Main ───────────────────────────────────────────────────────────

def main():
    print("FRONTIER: CHIRAL BORN BARRIER TEST")
    print("Three blocking mechanisms for 3-slit Sorkin test")
    print(f"Parameters: n_y={N_Y}, n_layers={N_LAYERS}, theta={THETA_0}")
    print(f"Source: y={SOURCE_Y}, Barrier: layer {BARRIER_LAYER}")
    print(f"Slits: {SLIT_POSITIONS}")
    print()

    # ── Run Sorkin test for each mechanism ──────────────────────────
    results = {}
    for mechanism in ['A', 'B', 'C']:
        results[mechanism] = sorkin_test(mechanism, mechanism)

    # ── Linearity test ─────────────────────────────────────────────
    linearity_pass = test_linearity()

    # ── Interference test ──────────────────────────────────────────
    test_interference()

    # ── Summary ────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")

    for m in ['A', 'B', 'C']:
        r = results[m]
        print(f"  Mechanism {m} ({mechanism_name(m)}):")
        print(f"    |I3|/P = {r['I3_norm']:.2e}  [{r['status']}]")
        print(f"    P(ABC) total = {r['P_total']:.6f}")

    print(f"\n  Linearity (Mech A): {'PASS' if linearity_pass else 'FAIL'}")

    any_pass = any(r['status'] == 'PASS' for r in results.values())
    all_fail = all(r['status'] == 'FAIL' for r in results.values())

    if results['A']['status'] == 'PASS':
        print(f"\n  HYPOTHESIS CONFIRMED: Absorption gives I3 < 1e-6 (Born holds).")
        print(f"  Key insight: Absorption is LINEAR (U(a+b) = U(a) + U(b)),")
        print(f"  and Born rule requires only linearity, not unitarity.")
    elif any_pass:
        winner = [m for m in ['A','B','C'] if results[m]['status'] == 'PASS'][0]
        print(f"\n  PARTIAL: Mechanism {winner} passes Born, but not absorption.")
    elif all_fail:
        best = min(results.values(), key=lambda r: r['I3_norm'])
        print(f"\n  HYPOTHESIS FALSIFIED: All mechanisms fail Born test.")
        print(f"  Best: Mechanism {best['label']} with |I3|/P = {best['I3_norm']:.2e}")
    else:
        print(f"\n  MIXED RESULTS: see individual tests above.")


if __name__ == "__main__":
    main()
