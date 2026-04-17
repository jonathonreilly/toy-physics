#!/usr/bin/env python3
"""
Frontier: 1D Decoherence Suppression of Gravity-Sign Oscillation
================================================================

This script is a wide-lattice 1+1D chiral test only.

It does NOT address the separate 3+1D periodic-lattice sign-flip question.
That requires a like-for-like 3+1D sweep on the same periodic architecture.

HYPOTHESIS:
  On the wide 1D reflecting lattice, decoherence may suppress any coherent
  gravity-sign oscillation and reveal a stable TOWARD baseline.

APPROACH:
  Part 1: coherent gravity vs N on the 1D wide lattice
  Part 2: fully decohered (classical) gravity vs N
  Part 3: stochastic dephasing sweep across gamma

DECOHERENCE MODEL:
  At each layer, after coin+shift, with probability gamma, destroy all
  relative phases between sites:
    psi(y) -> |psi(y)| * exp(i * random_phase(y))

  gamma=0: fully coherent
  gamma=1: maximal stochastic dephasing

  For the fully decohered limit, we also implement probability propagation:
    P(n+1) = |U|^2 @ P(n)
  This is the exact classical limit for this 1D walk.

PARAMETERS:
  n_y=41, reflecting BC, theta_0=0.3, strength=5e-4
  Mass offsets +3..+6 from the centered source

LIMITATION:
  A positive result here should be read as a 1D wide-lattice fact only.
  It cannot be promoted to 3+1D without rerunning the same coherent vs
  classical comparison on the 3+1D periodic chiral walk.
"""

from __future__ import annotations

import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


# ── Parameters ────────────────────────────────────────────────────────
N_Y = 41               # lattice sites (wide enough to avoid boundary effects)
THETA_0 = 0.3          # base mixing angle
STRENGTH = 5e-4        # gravitational field strength
SOURCE_Y = N_Y // 2    # = 20 (center)
MASS_OFFSET = 3        # mass at SOURCE_Y + 3
MASS_Y = SOURCE_Y + MASS_OFFSET

# Layer counts to scan
N_LAYERS_LIST = list(range(10, 42, 2))  # L=10,12,...,40 (matching wider_lattice)

# Decoherence strengths for partial sweep
GAMMA_VALUES = [0.0, 0.1, 0.2, 0.5, 0.8, 1.0]

# N values for detailed decoherence sweep
N_SWEEP = [12, 14, 16, 18, 20, 24, 28]

# Number of Monte Carlo samples for stochastic decoherence
N_SAMPLES = 200

# Mass offsets to test
MASS_OFFSETS = [3, 4, 5, 6]


# ── 1D Chiral Walk Core ──────────────────────────────────────────────

def make_field(n_layers, n_y, strength, mass_y):
    """1/r field from mass at mass_y. Layer-independent (static field)."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            field[x, y] = strength / (abs(y - mass_y) + 0.1)
    return field


def coin_step(psi, n_y, field_layer, theta_0):
    """Apply 2x2 coin at each site. Lorentzian coupling: theta = theta_0*(1-f)."""
    psi_out = psi.copy()
    for y in range(n_y):
        f = field_layer[y]
        th = theta_0 * (1.0 - f)
        c = math.cos(th)
        s = math.sin(th)
        ip = 2 * y
        im = 2 * y + 1
        pp, pm = psi_out[ip], psi_out[im]
        psi_out[ip] = c * pp - s * pm
        psi_out[im] = s * pp + c * pm
    return psi_out


def shift_step(psi, n_y):
    """Shift chiralities: psi_+ -> y+1, psi_- -> y-1 with reflecting BC."""
    new_psi = np.zeros_like(psi)
    for y in range(n_y):
        # psi_+ moves to y+1
        if y + 1 < n_y:
            new_psi[2 * (y + 1)] += psi[2 * y]
        else:
            new_psi[2 * y + 1] += psi[2 * y]  # reflect
        # psi_- moves to y-1
        if y - 1 >= 0:
            new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
        else:
            new_psi[2 * y] += psi[2 * y + 1]  # reflect
    return new_psi


def make_source(n_y, source_y):
    """Initialize pure right-mover at source."""
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0
    return psi


def detector_probs(psi, n_y):
    """Total probability at each y site."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid(probs):
    """Probability-weighted centroid."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.sum(ys * probs) / total)


# ── Propagation Modes ────────────────────────────────────────────────

def propagate_coherent(n_y, n_layers, theta_0, field, source_y):
    """Standard coherent chiral walk."""
    psi = make_source(n_y, source_y)
    for x in range(n_layers):
        psi = coin_step(psi, n_y, field[x], theta_0)
        psi = shift_step(psi, n_y)
    return psi


def propagate_decohered_stochastic(n_y, n_layers, theta_0, field, source_y,
                                    gamma, rng):
    """Chiral walk with stochastic dephasing at each layer.

    After each coin+shift, with probability gamma, destroy phases at
    each site: psi(y) -> |psi(y)| * exp(i * random_phase).

    This is ONE sample of the dephasing channel. Average many samples
    to get the mixed-state centroid.
    """
    psi = make_source(n_y, source_y)
    for x in range(n_layers):
        psi = coin_step(psi, n_y, field[x], theta_0)
        psi = shift_step(psi, n_y)

        # Dephasing: with probability gamma, randomize phase at each site
        if gamma > 0:
            for y in range(n_y):
                if rng.random() < gamma:
                    ip = 2 * y
                    im = 2 * y + 1
                    # Keep amplitudes, randomize relative phase between sites
                    # (but preserve internal chirality structure)
                    phase = rng.uniform(0, 2 * math.pi)
                    amp_p = abs(psi[ip])
                    amp_m = abs(psi[im])
                    # Assign random phases independently
                    psi[ip] = amp_p * np.exp(1j * rng.uniform(0, 2 * math.pi))
                    psi[im] = amp_m * np.exp(1j * rng.uniform(0, 2 * math.pi))
    return psi


def propagate_classical(n_y, n_layers, theta_0, field, source_y):
    """Fully decohered limit: propagate PROBABILITIES, not amplitudes.

    At each layer, compute the transition probability matrix T = |U|^2
    (element-wise squared magnitudes of the one-layer unitary) and
    propagate P(n+1) = T @ P(n).

    This is the EXACT classical limit with no Monte Carlo noise.
    """
    dim = 2 * n_y

    # Initial probability distribution
    prob = np.zeros(dim)
    prob[2 * source_y] = 1.0  # all probability in psi_+ at source

    for x in range(n_layers):
        # Build the one-layer transition matrix for this layer
        # by applying coin+shift to each basis vector
        T = np.zeros((dim, dim))
        for col in range(dim):
            e = np.zeros(dim, dtype=complex)
            e[col] = 1.0
            e_out = coin_step(e, n_y, field[x], theta_0)
            e_out = shift_step(e_out, n_y)
            T[:, col] = np.abs(e_out) ** 2

        # Propagate probabilities
        prob = T @ prob

    # Convert to site probabilities
    site_probs = np.zeros(n_y)
    for y in range(n_y):
        site_probs[y] = prob[2 * y] + prob[2 * y + 1]
    return site_probs


def propagate_phase_kill(n_y, n_layers, theta_0, field, source_y):
    """Decoherence by phase destruction: after each layer, set all phases to zero.

    psi(y, comp) -> |psi(y, comp)|

    This destroys all interference between sites while preserving local
    probability and the coin/shift structure.
    """
    psi = make_source(n_y, source_y)
    for x in range(n_layers):
        psi = coin_step(psi, n_y, field[x], theta_0)
        psi = shift_step(psi, n_y)
        # Kill all phases
        psi = np.abs(psi).astype(complex)
    return psi


# ── Analysis Helpers ─────────────────────────────────────────────────

def gravity_delta(n_y, n_layers, theta_0, strength, source_y, mass_y,
                  mode="coherent", gamma=0.0, rng=None, n_samples=1):
    """Compute gravity deflection delta = centroid_field - centroid_flat.

    Positive delta means TOWARD mass (if mass_y > source_y).

    mode: "coherent", "classical", "phase_kill", "stochastic"
    """
    field_flat = np.zeros((n_layers, n_y))
    field_mass = make_field(n_layers, n_y, strength, mass_y)

    if mode == "coherent":
        psi_flat = propagate_coherent(n_y, n_layers, theta_0, field_flat, source_y)
        psi_mass = propagate_coherent(n_y, n_layers, theta_0, field_mass, source_y)
        c_flat = centroid(detector_probs(psi_flat, n_y))
        c_mass = centroid(detector_probs(psi_mass, n_y))
        return c_mass - c_flat

    elif mode == "classical":
        probs_flat = propagate_classical(n_y, n_layers, theta_0, field_flat, source_y)
        probs_mass = propagate_classical(n_y, n_layers, theta_0, field_mass, source_y)
        c_flat = centroid(probs_flat)
        c_mass = centroid(probs_mass)
        return c_mass - c_flat

    elif mode == "phase_kill":
        psi_flat = propagate_phase_kill(n_y, n_layers, theta_0, field_flat, source_y)
        psi_mass = propagate_phase_kill(n_y, n_layers, theta_0, field_mass, source_y)
        c_flat = centroid(detector_probs(psi_flat, n_y))
        c_mass = centroid(detector_probs(psi_mass, n_y))
        return c_mass - c_flat

    elif mode == "stochastic":
        # Average over multiple Monte Carlo samples
        deltas = []
        for _ in range(n_samples):
            psi_flat = propagate_decohered_stochastic(
                n_y, n_layers, theta_0, field_flat, source_y, gamma, rng)
            psi_mass = propagate_decohered_stochastic(
                n_y, n_layers, theta_0, field_mass, source_y, gamma, rng)
            c_flat = centroid(detector_probs(psi_flat, n_y))
            c_mass = centroid(detector_probs(psi_mass, n_y))
            deltas.append(c_mass - c_flat)
        return float(np.mean(deltas)), float(np.std(deltas))

    else:
        raise ValueError(f"Unknown mode: {mode}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    t_start = time.time()
    rng = np.random.default_rng(42)

    print("=" * 74)
    print("FRONTIER: DECOHERENCE SUPPRESSION OF GRAVITY SIGN OSCILLATION")
    print("=" * 74)
    print(f"  n_y={N_Y}, theta_0={THETA_0}, strength={STRENGTH}")
    print(f"  source_y={SOURCE_Y}")
    print(f"  TOWARD = delta > 0 (mass at y > source_y)")
    print()

    # ==================================================================
    # PART 0: Multi-offset scan to find/confirm oscillation regime
    # ==================================================================
    print("=" * 74)
    print("PART 0: MULTI-OFFSET COHERENT SCAN (find oscillation)")
    print("=" * 74)
    print()

    best_offset = MASS_OFFSETS[0]
    best_sign_changes = 0
    offset_data = {}

    for offset in MASS_OFFSETS:
        mass_y = SOURCE_Y + offset
        print(f"  --- offset={offset} (mass_y={mass_y}) ---")
        print(f"    {'N':>4s}  {'delta':>14s}  {'dir':>6s}")

        results_off = {}
        toward_n = 0
        for N in N_LAYERS_LIST:
            delta = gravity_delta(N_Y, N, THETA_0, STRENGTH,
                                  SOURCE_Y, mass_y, mode="coherent")
            direction = "TOWARD" if delta > 0 else "AWAY"
            if delta > 0:
                toward_n += 1
            results_off[N] = delta
            print(f"    {N:4d}  {delta:14.10f}  {direction:>6s}")

        signs = [1 if results_off[N] > 0 else -1 for N in N_LAYERS_LIST]
        sc = sum(1 for i in range(len(signs)-1) if signs[i] != signs[i+1])
        print(f"    TOWARD: {toward_n}/{len(N_LAYERS_LIST)}, sign changes: {sc}")
        print()

        offset_data[offset] = results_off
        if sc > best_sign_changes:
            best_sign_changes = sc
            best_offset = offset

    # Use the offset with most oscillation for the rest of the analysis
    # If no oscillation found, use the requested offset
    use_offset = best_offset if best_sign_changes >= 2 else MASS_OFFSET
    use_mass_y = SOURCE_Y + use_offset
    coherent_results = offset_data.get(use_offset, {})

    print(f"  Selected offset for decoherence test: d={use_offset} "
          f"(sign_changes={best_sign_changes})")
    print()

    # If no oscillation at any offset, also report d=MASS_OFFSET results
    if best_sign_changes < 2:
        print("  NOTE: No significant oscillation found at any offset.")
        print("  Proceeding with d=3 (default) for decoherence analysis.")
        use_offset = MASS_OFFSET
        use_mass_y = SOURCE_Y + use_offset
        coherent_results = offset_data.get(use_offset, {})
        # Fill in missing N values
        for N in N_LAYERS_LIST:
            if N not in coherent_results:
                coherent_results[N] = gravity_delta(
                    N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y,
                    mode="coherent")
        print()

    # Coherent summary
    toward_count = sum(1 for N in N_LAYERS_LIST if coherent_results[N] > 0)
    signs = [1 if coherent_results[N] > 0 else -1 for N in N_LAYERS_LIST]
    sign_changes = sum(1 for i in range(len(signs)-1) if signs[i] != signs[i+1])
    oscillates = sign_changes >= 2

    # ==================================================================
    # PART 1: Coherent gravity vs N at selected offset
    # ==================================================================
    print("=" * 74)
    print(f"PART 1: COHERENT GRAVITY vs N (d={use_offset}, mass_y={use_mass_y})")
    print("=" * 74)
    print()
    print(f"  {'N':>4s}  {'delta':>14s}  {'direction':>10s}")
    print(f"  {'----':>4s}  {'-' * 14:>14s}  {'-' * 10:>10s}")

    for N in N_LAYERS_LIST:
        delta = coherent_results[N]
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {N:4d}  {delta:14.10f}  {direction:>10s}")

    print()
    print(f"  Coherent TOWARD: {toward_count}/{len(N_LAYERS_LIST)}")
    print(f"  Sign changes: {sign_changes}")
    print(f"  Oscillation detected: {oscillates}")
    print()

    # ==================================================================
    # PART 2: Fully decohered (classical) gravity vs N
    # ==================================================================
    print("=" * 74)
    print("PART 2: FULLY DECOHERED (CLASSICAL) GRAVITY vs N")
    print("  Method: propagate probabilities P(n+1) = |U|^2 @ P(n)")
    print("=" * 74)
    print()
    print(f"  {'N':>4s}  {'delta_classical':>16s}  {'dir':>6s}  {'delta_coherent':>16s}  {'dir':>6s}")
    print(f"  {'----':>4s}  {'-' * 16:>16s}  {'------':>6s}  {'-' * 16:>16s}  {'------':>6s}")

    classical_results = {}
    classical_toward = 0
    for N in N_LAYERS_LIST:
        delta_cl = gravity_delta(N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y,
                                  mode="classical")
        dir_cl = "TOWARD" if delta_cl > 0 else "AWAY"
        if delta_cl > 0:
            classical_toward += 1
        dir_coh = "TOWARD" if coherent_results[N] > 0 else "AWAY"
        classical_results[N] = delta_cl
        print(f"  {N:4d}  {delta_cl:16.10f}  {dir_cl:>6s}  {coherent_results[N]:16.10f}  {dir_coh:>6s}")

    print()
    print(f"  Classical TOWARD: {classical_toward}/{len(N_LAYERS_LIST)}")

    signs_cl = [1 if classical_results[N] > 0 else -1 for N in N_LAYERS_LIST]
    sign_changes_cl = sum(1 for i in range(len(signs_cl)-1) if signs_cl[i] != signs_cl[i+1])
    classical_oscillates = sign_changes_cl >= 2
    print(f"  Classical sign changes: {sign_changes_cl}")
    print(f"  Classical oscillation: {classical_oscillates}")
    print()

    # ==================================================================
    # PART 2b: Phase-kill decoherence vs N
    # ==================================================================
    print("=" * 74)
    print("PART 2b: PHASE-KILL DECOHERENCE vs N")
    print("  Method: after each layer, psi -> |psi| (zero all phases)")
    print("=" * 74)
    print()
    print(f"  {'N':>4s}  {'delta_phkill':>16s}  {'dir':>6s}  {'delta_coherent':>16s}  {'dir':>6s}")
    print(f"  {'----':>4s}  {'-' * 16:>16s}  {'------':>6s}  {'-' * 16:>16s}  {'------':>6s}")

    phkill_results = {}
    phkill_toward = 0
    for N in N_LAYERS_LIST:
        delta_pk = gravity_delta(N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y,
                                  mode="phase_kill")
        dir_pk = "TOWARD" if delta_pk > 0 else "AWAY"
        if delta_pk > 0:
            phkill_toward += 1
        dir_coh = "TOWARD" if coherent_results[N] > 0 else "AWAY"
        phkill_results[N] = delta_pk
        print(f"  {N:4d}  {delta_pk:16.10f}  {dir_pk:>6s}  {coherent_results[N]:16.10f}  {dir_coh:>6s}")

    print()
    print(f"  Phase-kill TOWARD: {phkill_toward}/{len(N_LAYERS_LIST)}")

    signs_pk = [1 if phkill_results[N] > 0 else -1 for N in N_LAYERS_LIST]
    sign_changes_pk = sum(1 for i in range(len(signs_pk)-1) if signs_pk[i] != signs_pk[i+1])
    print(f"  Phase-kill sign changes: {sign_changes_pk}")
    print()

    # ==================================================================
    # PART 3: Partial decoherence sweep (stochastic dephasing)
    # ==================================================================
    print("=" * 74)
    print("PART 3: PARTIAL DECOHERENCE SWEEP (stochastic dephasing)")
    print(f"  N_SAMPLES={N_SAMPLES} per (gamma, N) pair")
    print("=" * 74)
    print()

    header = f"  {'N':>4s}"
    for gamma in GAMMA_VALUES:
        header += f"  {'g=' + str(gamma):>14s}"
    print(header)
    print(f"  {'----':>4s}" + f"  {'-' * 14:>14s}" * len(GAMMA_VALUES))

    stochastic_results = {}

    for N in N_SWEEP:
        row = f"  {N:4d}"
        for gamma in GAMMA_VALUES:
            if gamma == 0.0:
                delta = coherent_results.get(N)
                if delta is None:
                    delta = gravity_delta(N_Y, N, THETA_0, STRENGTH,
                                          SOURCE_Y, use_mass_y, mode="coherent")
                stochastic_results[(N, gamma)] = (delta, 0.0)
                dir_str = "T" if delta > 0 else "A"
                row += f"  {delta:+10.6f} {dir_str:>2s}"
            else:
                mean_d, std_d = gravity_delta(
                    N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y,
                    mode="stochastic", gamma=gamma, rng=rng,
                    n_samples=N_SAMPLES)
                stochastic_results[(N, gamma)] = (mean_d, std_d)
                dir_str = "T" if mean_d > 0 else "A"
                row += f"  {mean_d:+10.6f} {dir_str:>2s}"
        print(row)

    print()
    print("  Standard deviations:")
    header2 = f"  {'N':>4s}"
    for gamma in GAMMA_VALUES:
        header2 += f"  {'g=' + str(gamma):>14s}"
    print(header2)
    print(f"  {'----':>4s}" + f"  {'-' * 14:>14s}" * len(GAMMA_VALUES))

    for N in N_SWEEP:
        row = f"  {N:4d}"
        for gamma in GAMMA_VALUES:
            _, std_d = stochastic_results[(N, gamma)]
            row += f"  {std_d:14.8f}"
        print(row)

    print()

    # ==================================================================
    # PART 4: Detailed analysis of key N values
    # ==================================================================
    print("=" * 74)
    print("PART 4: DETAILED COMPARISON AT KEY N VALUES")
    print("=" * 74)
    print()

    key_N = [12, 16, 20, 28]
    for N in key_N:
        if N not in coherent_results:
            continue
        delta_coh = coherent_results[N]
        delta_cl = classical_results.get(N, gravity_delta(
            N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y, mode="classical"))
        delta_pk = phkill_results.get(N, gravity_delta(
            N_Y, N, THETA_0, STRENGTH, SOURCE_Y, use_mass_y, mode="phase_kill"))

        dir_coh = "TOWARD" if delta_coh > 0 else "AWAY"
        dir_cl = "TOWARD" if delta_cl > 0 else "AWAY"
        dir_pk = "TOWARD" if delta_pk > 0 else "AWAY"

        print(f"  N={N}:")
        print(f"    Coherent:    delta={delta_coh:+14.10f}  {dir_coh}")
        print(f"    Classical:   delta={delta_cl:+14.10f}  {dir_cl}")
        print(f"    Phase-kill:  delta={delta_pk:+14.10f}  {dir_pk}")

        for gamma in [0.1, 0.5, 1.0]:
            key = (N, gamma)
            if key in stochastic_results:
                mean_d, std_d = stochastic_results[key]
                dir_st = "TOWARD" if mean_d > 0 else "AWAY"
                print(f"    Stochastic(g={gamma}): delta={mean_d:+14.10f} +/- {std_d:.8f}  {dir_st}")
        print()

    # ==================================================================
    # PART 5: Magnitude comparison
    # ==================================================================
    print("=" * 74)
    print("PART 5: MAGNITUDE COMPARISON")
    print("=" * 74)
    print()
    print(f"  {'N':>4s}  {'|coh|':>12s}  {'|classical|':>12s}  {'|phase_kill|':>12s}  {'ratio cl/coh':>14s}")
    print(f"  {'----':>4s}  {'-' * 12:>12s}  {'-' * 12:>12s}  {'-' * 12:>12s}  {'-' * 14:>14s}")

    for N in N_LAYERS_LIST:
        d_coh = abs(coherent_results[N])
        d_cl = abs(classical_results[N])
        d_pk = abs(phkill_results[N])
        ratio = d_cl / d_coh if d_coh > 1e-15 else float('inf')
        print(f"  {N:4d}  {d_coh:12.8f}  {d_cl:12.8f}  {d_pk:12.8f}  {ratio:14.6f}")

    print()

    # ==================================================================
    # PART 6: Multi-offset decoherence comparison
    # ==================================================================
    print("=" * 74)
    print("PART 6: DECOHERENCE vs COHERENT SIGN ACROSS ALL OFFSETS")
    print("=" * 74)
    print()

    for offset in MASS_OFFSETS:
        mass_y = SOURCE_Y + offset
        print(f"  --- offset={offset} (mass_y={mass_y}) ---")
        print(f"    {'N':>4s}  {'coh_delta':>14s}  {'coh_dir':>8s}  {'cl_delta':>14s}  {'cl_dir':>8s}  {'agree':>6s}")

        agree_count = 0
        total = 0
        for N in N_LAYERS_LIST:
            d_coh = offset_data.get(offset, {}).get(N)
            if d_coh is None:
                d_coh = gravity_delta(N_Y, N, THETA_0, STRENGTH,
                                      SOURCE_Y, mass_y, mode="coherent")
            d_cl = gravity_delta(N_Y, N, THETA_0, STRENGTH,
                                 SOURCE_Y, mass_y, mode="classical")
            dir_coh = "TOWARD" if d_coh > 0 else "AWAY"
            dir_cl = "TOWARD" if d_cl > 0 else "AWAY"
            agree = "YES" if (d_coh > 0) == (d_cl > 0) else "NO"
            if agree == "YES":
                agree_count += 1
            total += 1
            print(f"    {N:4d}  {d_coh:14.10f}  {dir_coh:>8s}  {d_cl:14.10f}  {dir_cl:>8s}  {agree:>6s}")

        print(f"    Agreement: {agree_count}/{total}")
        print()

    # ==================================================================
    # SUMMARY & VERDICT
    # ==================================================================
    print("=" * 74)
    print("SUMMARY & VERDICT")
    print("=" * 74)
    print()

    print(f"  Coherent walk (d={use_offset}):")
    print(f"    TOWARD: {toward_count}/{len(N_LAYERS_LIST)}")
    print(f"    Sign oscillation: {oscillates} ({sign_changes} changes)")
    print()
    print(f"  Classical probability propagation (d={use_offset}):")
    print(f"    TOWARD: {classical_toward}/{len(N_LAYERS_LIST)}")
    print(f"    Sign oscillation: {classical_oscillates} ({sign_changes_cl} changes)")
    print()
    print(f"  Phase-kill (d={use_offset}):")
    print(f"    TOWARD: {phkill_toward}/{len(N_LAYERS_LIST)}")
    print(f"    Sign oscillation: {sign_changes_pk} changes")
    print()

    # The key test: any N where coherent is AWAY but classical is TOWARD?
    flipped_N = []
    for N in N_LAYERS_LIST:
        if coherent_results[N] < 0 and classical_results[N] > 0:
            flipped_N.append(N)

    if flipped_N:
        print(f"  DECOHERENCE FLIPS AWAY->TOWARD at N={flipped_N}")
        print(f"  --> Geometric gravity survives decoherence at these N!")
    else:
        if toward_count == len(N_LAYERS_LIST):
            print(f"  No flip needed: coherent walk is already TOWARD at all N")
        else:
            away_N = [N for N in N_LAYERS_LIST if coherent_results[N] < 0]
            still_away = [N for N in away_N if classical_results[N] < 0]
            if still_away:
                print(f"  Classical also AWAY at N={still_away}")
    print()

    # Overall verdict for this 1D wide-lattice test only.
    all_classical_toward = classical_toward == len(N_LAYERS_LIST)
    no_classical_oscillation = sign_changes_cl == 0

    if best_sign_changes < 2 and toward_count == len(N_LAYERS_LIST):
        verdict = (
            "1D RESULT ONLY: no coherent oscillation was present on this wide "
            "reflecting lattice, so decoherence cannot be credited with "
            "removing it here"
        )
    elif all_classical_toward and no_classical_oscillation:
        verdict = (
            "1D RESULT ONLY: decoherence suppresses the measured oscillation "
            "and leaves a TOWARD classical baseline"
        )
    elif classical_toward > toward_count:
        verdict = (
            "1D RESULT ONLY: decoherence reduces oscillation but does not "
            "fully suppress it"
        )
    elif no_classical_oscillation and not all_classical_toward:
        verdict = (
            "1D RESULT ONLY: the classical walk is stable but not always "
            "TOWARD"
        )
    else:
        verdict = (
            "1D RESULT ONLY: the classical walk still oscillates, so the "
            "oscillation is not quantum-only"
        )

    print(
        "  HYPOTHESIS: 'On the 1D wide lattice, decoherence suppresses any "
        "coherent N-oscillation and leaves gravity TOWARD at all N'"
    )
    print(f"  VERDICT: {verdict}")
    print("  Scope: 1D reflecting lattice only; does not settle the 3+1D periodic case.")
    print()

    elapsed = time.time() - t_start
    print(f"  Total time: {elapsed:.1f}s")
    print("=" * 74)


if __name__ == "__main__":
    main()
