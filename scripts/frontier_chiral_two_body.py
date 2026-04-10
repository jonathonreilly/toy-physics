#!/usr/bin/env python3
"""
Frontier: Chiral two-body superposition test.

THE QUESTION: Does superposition hold for the Lorentzian chiral walk?
- Transfer matrix: 3D superposition 0.01% error, but 2D was 99-127%.
- Chiral walk: F proportional to M = 1.0, Born passes.
- Does superposition (linearity of deflection in additive fields) hold?

SETUP:
  Lorentzian chiral walk, n_y=41, n_layers=30, theta_0=0.3, strength=5e-4.
  Mass A at y=24, Mass B at y=28, center=20.
  Additive 1/r fields, then non-additive joint potential.

HYPOTHESIS: Chiral superposition error < 5%.
FALSIFICATION: If error > 20%.
"""

import numpy as np

# === Parameters ===
N_Y = 41
N_LAYERS = 30
THETA_0 = 0.3
STRENGTH = 5e-4
CENTER = N_Y // 2  # 20

Y_A = 24  # offset +4 from center
Y_B = 28  # offset +8 from center

def lorentzian_chiral_propagator(n_y, n_layers, theta_0, field):
    """
    Propagate a chiral walk through n_layers with a gravitational field.

    The chiral walk uses a 2-component state (left, right movers).
    At each layer, apply:
      1. Phase from gravitational field: exp(i * field[y])
      2. Coin (beam-splitter) with angle theta_0
      3. Shift left/right components

    Returns final probability distribution over y.
    """
    # State: 2 components (left, right) x n_y positions
    psi = np.zeros((2, n_y), dtype=complex)
    # Initialize: right-mover at center
    psi[1, n_y // 2] = 1.0

    cos_t = np.cos(theta_0)
    sin_t = np.sin(theta_0)

    for layer in range(n_layers):
        # 1. Apply gravitational phase
        phase = np.exp(1j * field)
        psi[0] *= phase
        psi[1] *= phase

        # 2. Coin operation (beam-splitter) at each site
        new_psi = np.zeros_like(psi)
        new_psi[0] = cos_t * psi[0] + 1j * sin_t * psi[1]
        new_psi[1] = 1j * sin_t * psi[0] + cos_t * psi[1]
        psi = new_psi

        # 3. Shift: left-movers go left, right-movers go right
        psi[0] = np.roll(psi[0], -1)
        psi[1] = np.roll(psi[1], +1)
        # Absorbing boundaries
        psi[0, -1] = 0.0
        psi[1, 0] = 0.0

    # Probability distribution
    prob = np.abs(psi[0])**2 + np.abs(psi[1])**2
    return prob


def make_field_A(n_y, strength, y_a=Y_A):
    """1/r field from mass A at y_a."""
    y = np.arange(n_y, dtype=float)
    return strength / (np.abs(y - y_a) + 0.1)


def make_field_B(n_y, strength, y_b=Y_B):
    """1/r field from mass B at y_b."""
    y = np.arange(n_y, dtype=float)
    return strength / (np.abs(y - y_b) + 0.1)


def centroid(prob, n_y):
    """Compute probability-weighted centroid."""
    y = np.arange(n_y, dtype=float)
    total = np.sum(prob)
    if total < 1e-15:
        return n_y / 2.0
    return np.sum(y * prob) / total


def run_config(label, field):
    """Run one configuration and return centroid shift from no-field baseline."""
    prob = lorentzian_chiral_propagator(N_Y, N_LAYERS, THETA_0, field)
    c = centroid(prob, N_Y)
    norm = np.sum(prob)
    return c, norm, prob


def main():
    print("=" * 70)
    print("FRONTIER: Chiral Two-Body Superposition Test")
    print("=" * 70)
    print(f"\nParameters: n_y={N_Y}, n_layers={N_LAYERS}, theta_0={THETA_0}, strength={STRENGTH}")
    print(f"Center={CENTER}, Mass A at y={Y_A} (+{Y_A - CENTER}), Mass B at y={Y_B} (+{Y_B - CENTER})")

    # === Build fields ===
    field_zero = np.zeros(N_Y)
    field_A = make_field_A(N_Y, STRENGTH)
    field_B = make_field_B(N_Y, STRENGTH)
    field_AB_additive = field_A + field_B  # linear superposition of fields

    # Non-additive: joint potential (e.g., combined mass at center-of-mass)
    y_com = (Y_A + Y_B) / 2.0  # = 26
    combined_strength = 2 * STRENGTH  # total mass
    y = np.arange(N_Y, dtype=float)
    field_AB_joint = combined_strength / (np.abs(y - y_com) + 0.1)

    # === Run 4 configs (additive) ===
    print("\n--- Additive Field Test ---")
    c_0, norm_0, prob_0 = run_config("No mass", field_zero)
    c_A, norm_A, prob_A = run_config("Mass A only", field_A)
    c_B, norm_B, prob_B = run_config("Mass B only", field_B)
    c_AB, norm_AB, prob_AB = run_config("Mass A+B (additive)", field_AB_additive)

    delta_A = c_A - c_0
    delta_B = c_B - c_0
    delta_AB = c_AB - c_0
    delta_sum = delta_A + delta_B

    print(f"\n  {'Config':<25} {'Centroid':>10} {'Norm':>10} {'Delta':>10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10}")
    print(f"  {'No mass':<25} {c_0:10.6f} {norm_0:10.6f} {'---':>10}")
    print(f"  {'Mass A only':<25} {c_A:10.6f} {norm_A:10.6f} {delta_A:10.6f}")
    print(f"  {'Mass B only':<25} {c_B:10.6f} {norm_B:10.6f} {delta_B:10.6f}")
    print(f"  {'Mass A+B (additive)':<25} {c_AB:10.6f} {norm_AB:10.6f} {delta_AB:10.6f}")
    print(f"  {'Sum delta_A + delta_B':<25} {'':>10} {'':>10} {delta_sum:10.6f}")

    if abs(delta_AB) > 1e-12:
        error_additive = abs(delta_AB - delta_sum) / abs(delta_AB) * 100
    else:
        error_additive = 0.0 if abs(delta_sum) < 1e-12 else float('inf')

    print(f"\n  Superposition error (additive): {error_additive:.4f}%")

    # === Non-additive (joint potential) test ===
    print("\n--- Non-Additive (Joint Potential) Test ---")
    c_J, norm_J, prob_J = run_config("Joint potential", field_AB_joint)
    delta_J = c_J - c_0

    print(f"\n  {'Config':<25} {'Centroid':>10} {'Norm':>10} {'Delta':>10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10}")
    print(f"  {'Joint potential':<25} {c_J:10.6f} {norm_J:10.6f} {delta_J:10.6f}")
    print(f"  {'Additive A+B':<25} {c_AB:10.6f} {norm_AB:10.6f} {delta_AB:10.6f}")

    if abs(delta_AB) > 1e-12:
        joint_vs_additive = abs(delta_J - delta_AB) / abs(delta_AB) * 100
    else:
        joint_vs_additive = 0.0
    print(f"\n  Joint vs Additive difference: {joint_vs_additive:.4f}%")

    # === Sweep over strengths ===
    print("\n--- Strength Sweep (superposition error vs coupling) ---")
    strengths = [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]
    print(f"  {'Strength':>10} {'delta_A':>10} {'delta_B':>10} {'delta_AB':>10} {'delta_sum':>10} {'Error%':>10}")
    print(f"  {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")

    for s in strengths:
        fA = make_field_A(N_Y, s)
        fB = make_field_B(N_Y, s)
        fAB = fA + fB

        pA = lorentzian_chiral_propagator(N_Y, N_LAYERS, THETA_0, fA)
        pB = lorentzian_chiral_propagator(N_Y, N_LAYERS, THETA_0, fB)
        pAB = lorentzian_chiral_propagator(N_Y, N_LAYERS, THETA_0, fAB)

        dA = centroid(pA, N_Y) - c_0
        dB = centroid(pB, N_Y) - c_0
        dAB = centroid(pAB, N_Y) - c_0
        dS = dA + dB

        if abs(dAB) > 1e-12:
            err = abs(dAB - dS) / abs(dAB) * 100
        else:
            err = 0.0
        print(f"  {s:10.1e} {dA:10.6f} {dB:10.6f} {dAB:10.6f} {dS:10.6f} {err:10.4f}")

    # === Verdict ===
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    print(f"\n  Primary test (strength={STRENGTH}):")
    print(f"    Superposition error = {error_additive:.4f}%")
    if error_additive < 5.0:
        print(f"    PASS: Error < 5% — superposition HOLDS on chiral walk")
        verdict = "PASS"
    elif error_additive < 20.0:
        print(f"    MARGINAL: 5% < Error < 20% — partial superposition")
        verdict = "MARGINAL"
    else:
        print(f"    FAIL: Error > 20% — superposition BROKEN")
        verdict = "FAIL"

    print(f"\n  Joint vs Additive field difference: {joint_vs_additive:.4f}%")
    if joint_vs_additive > 5.0:
        print(f"    Field non-linearity matters: joint != sum-of-individuals")
    else:
        print(f"    Field linearity holds: joint ~ sum-of-individuals")

    print(f"\n  HYPOTHESIS 'chiral superposition error < 5%': {verdict}")
    if verdict == "FAIL":
        print(f"  FALSIFIED at error = {error_additive:.4f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
