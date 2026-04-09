#!/usr/bin/env python3
"""Spectral averaging of gravity: does summing over k wash out resonance oscillations?

THE PHYSICS:
  Single-k gravity oscillates between attractive and repulsive as k varies.
  Real quantum fields have a SPECTRUM of k values. If we sum the propagator
  over a range of k (like a wave packet), do the resonance oscillations
  average out, leaving net attraction?

APPROACH:
  1. Single-k sweep: measure centroid shift delta(k) for many k values
  2. Spectral average: sum complex amplitudes weighted by Gaussian A(k),
     then compute probability and centroid from the summed wavefunction
  3. Test whether broad spectra universally give TOWARD

HYPOTHESIS: Broad spectral averaging produces net attraction regardless
  of center frequency k0.
FALSIFICATION: If broad spectra can still give AWAY, averaging doesn't
  fix the resonance issue.
"""

from __future__ import annotations
import cmath
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_persistence_support,
    infer_arrival_times_with_field,
    build_causal_dag,
    graph_neighbors,
    boundary_nodes,
)


# ── Configuration ─────────────────────────────────────────────

WIDTH = 16
HEIGHT = 6
MASS_POS = (8, 3)
SOURCE = (0, 0)
FIELD_STRENGTH = 1e-3
P = 1  # attenuation power for 2D


# ── Field solver ──────────────────────────────────────────────

def analytic_spatial_only_field(nodes, mass_pos, strength):
    """Analytic spatial-only field: f = strength / |y - y_mass|."""
    _mx, my = mass_pos
    field = {}
    for n in nodes:
        r = abs(n[1] - my) + 0.1
        field[n] = strength / r
    return field


# ── Single-k propagation ─────────────────────────────────────

def propagate_single_k(nodes, source, node_field, width, k, p=P):
    """Valley-linear propagation at a single k value.

    Returns detector dict: y -> complex amplitude.
    Uses flat-space DAG to isolate the action effect.
    """
    flat_field = {n: 0.0 for n in nodes}
    rule = derive_local_rule(frozenset(), RulePostulates(
        phase_per_action=k, attenuation_power=p))
    arrival = infer_arrival_times_with_field(nodes, source, rule, flat_field)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for neighbor in dag.get(node, []):
            L = math.dist(node, neighbor)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(neighbor, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) / (L ** p)
            states[neighbor] += amp * edge_amp

    return detector


def centroid_from_detector(det):
    """Compute centroid and total probability from detector amplitudes."""
    total = sum(abs(a) ** 2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    c = sum(y * abs(a) ** 2 for y, a in det.items()) / total
    return c, total


def centroid_shift(det_mass, det_flat):
    """Return centroid shift (mass - flat). Positive = toward mass at +y."""
    c_mass, _ = centroid_from_detector(det_mass)
    c_flat, _ = centroid_from_detector(det_flat)
    return c_mass - c_flat


# ── Spectral propagation ─────────────────────────────────────

def spectral_propagate(nodes, source, node_field, width, k_values, weights, p=P):
    """Sum complex amplitudes across k values weighted by spectrum.

    psi_spectral(y) = sum_k  weight(k) * psi_k(y)

    Returns detector dict: y -> complex amplitude (summed).
    """
    combined = defaultdict(complex)

    for k_val, w in zip(k_values, weights):
        det = propagate_single_k(nodes, source, node_field, width, k_val, p)
        for y, amp in det.items():
            combined[y] += w * amp

    return dict(combined)


def gaussian_weights(k_values, k0, sigma_k):
    """Gaussian spectrum weights: exp(-(k - k0)^2 / (2*sigma^2))."""
    raw = [math.exp(-(k - k0) ** 2 / (2 * sigma_k ** 2)) for k in k_values]
    total = sum(raw)
    return [r / total for r in raw]  # normalize


def flat_weights(k_values):
    """Equal weight on all k values."""
    n = len(k_values)
    return [1.0 / n] * n


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 76)
    print("SPECTRAL GRAVITY: Does k-averaging produce universal attraction?")
    print("=" * 76)
    print(f"Grid: {WIDTH}x{2*HEIGHT+1}, source={SOURCE}, mass={MASS_POS}")
    print(f"Field: spatial-only, strength={FIELD_STRENGTH}")
    print()

    nodes = build_rectangular_nodes(WIDTH, HEIGHT)
    flat_field = {n: 0.0 for n in nodes}
    mass_field = analytic_spatial_only_field(nodes, MASS_POS, FIELD_STRENGTH)

    # ── Part 1: Single-k sweep ────────────────────────────────
    print("-" * 76)
    print("PART 1: Single-k gravity vs k")
    print("-" * 76)
    print(f"  {'k':>6} | {'delta':>12} | {'direction':>9} | {'c_flat':>10} | {'c_mass':>10}")
    print(f"  {'-' * 60}")

    k_single = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0]
    single_results = {}

    for k in k_single:
        det_flat = propagate_single_k(nodes, SOURCE, flat_field, WIDTH, k)
        det_mass = propagate_single_k(nodes, SOURCE, mass_field, WIDTH, k)
        c_flat, _ = centroid_from_detector(det_flat)
        c_mass, _ = centroid_from_detector(det_mass)
        delta = c_mass - c_flat
        direction = "TOWARD" if delta > 0 else "AWAY"
        single_results[k] = delta
        print(f"  {k:>6.1f} | {delta:>+12.6f} | {direction:>9} | {c_flat:>+10.4f} | {c_mass:>+10.4f}")

    n_toward = sum(1 for d in single_results.values() if d > 0)
    n_away = sum(1 for d in single_results.values() if d <= 0)
    print(f"\n  Single-k summary: {n_toward} TOWARD, {n_away} AWAY out of {len(k_single)}")

    # ── Part 2: Spectral averaging ────────────────────────────
    print()
    print("-" * 76)
    print("PART 2: Spectral averaging (Gaussian wave packets)")
    print("-" * 76)
    print()
    print("For each (k0, sigma_k): sample 25 k values in [k0-3*sigma, k0+3*sigma],")
    print("weight by Gaussian, sum complex amplitudes, compute centroid.")
    print()

    # Test configurations
    configs = [
        # (k0, sigma_k, description)
        (2.5, 0.5, "k0=2.5 narrow"),
        (2.5, 1.0, "k0=2.5 medium"),
        (2.5, 2.0, "k0=2.5 broad"),
        (5.0, 0.5, "k0=5.0 narrow"),
        (5.0, 1.0, "k0=5.0 medium"),
        (5.0, 2.0, "k0=5.0 broad"),
        (3.0, 0.5, "k0=3.0 narrow"),
        (3.0, 1.0, "k0=3.0 medium"),
        (3.0, 2.0, "k0=3.0 broad"),
        (1.0, 0.5, "k0=1.0 narrow"),
        (1.0, 1.0, "k0=1.0 medium"),
        (1.0, 2.0, "k0=1.0 broad"),
    ]

    n_samples = 25  # k values to sample per configuration

    print(f"  {'config':<20} | {'k0':>5} | {'sigma':>5} | {'delta':>12} | {'direction':>9}")
    print(f"  {'-' * 65}")

    spectral_results = {}

    for k0, sigma_k, desc in configs:
        # Sample k values: k0 +/- 3*sigma_k, but keep k > 0.1
        k_lo = max(0.1, k0 - 3 * sigma_k)
        k_hi = k0 + 3 * sigma_k
        k_vals = [k_lo + i * (k_hi - k_lo) / (n_samples - 1) for i in range(n_samples)]
        weights = gaussian_weights(k_vals, k0, sigma_k)

        det_flat = spectral_propagate(nodes, SOURCE, flat_field, WIDTH, k_vals, weights)
        det_mass = spectral_propagate(nodes, SOURCE, mass_field, WIDTH, k_vals, weights)

        delta = centroid_shift(det_mass, det_flat)
        direction = "TOWARD" if delta > 0 else "AWAY"
        spectral_results[(k0, sigma_k)] = delta
        print(f"  {desc:<20} | {k0:>5.1f} | {sigma_k:>5.1f} | {delta:>+12.6f} | {direction:>9}")

    # ── Part 3: Flat spectrum (all k equal weight) ────────────
    print()
    print("-" * 76)
    print("PART 3: Flat spectrum (equal weight on all k)")
    print("-" * 76)
    print()

    flat_k_ranges = [
        ([0.5 + i * 0.5 for i in range(20)], "k=0.5..10.0 step 0.5"),
        ([0.5 + i * 0.25 for i in range(40)], "k=0.5..10.25 step 0.25"),
        ([1.0 + i * 0.2 for i in range(46)], "k=1.0..10.0 step 0.2"),
    ]

    print(f"  {'range':<30} | {'n_k':>4} | {'delta':>12} | {'direction':>9}")
    print(f"  {'-' * 65}")

    for k_vals, desc in flat_k_ranges:
        weights = flat_weights(k_vals)
        det_flat = spectral_propagate(nodes, SOURCE, flat_field, WIDTH, k_vals, weights)
        det_mass = spectral_propagate(nodes, SOURCE, mass_field, WIDTH, k_vals, weights)
        delta = centroid_shift(det_mass, det_flat)
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {desc:<30} | {len(k_vals):>4} | {delta:>+12.6f} | {direction:>9}")

    # ── Part 4: Increasing sigma at fixed k0 ─────────────────
    print()
    print("-" * 76)
    print("PART 4: Sigma sweep at fixed k0 (how much averaging is needed?)")
    print("-" * 76)
    print()

    for k0_test in [2.5, 5.0, 3.0]:
        print(f"  k0 = {k0_test}")
        print(f"    {'sigma':>6} | {'delta':>12} | {'direction':>9} | {'k_range'}")
        print(f"    {'-' * 55}")
        for sigma in [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
            k_lo = max(0.1, k0_test - 3 * sigma)
            k_hi = k0_test + 3 * sigma
            k_vals = [k_lo + i * (k_hi - k_lo) / (n_samples - 1) for i in range(n_samples)]
            weights = gaussian_weights(k_vals, k0_test, sigma)
            det_flat = spectral_propagate(nodes, SOURCE, flat_field, WIDTH, k_vals, weights)
            det_mass = spectral_propagate(nodes, SOURCE, mass_field, WIDTH, k_vals, weights)
            delta = centroid_shift(det_mass, det_flat)
            direction = "TOWARD" if delta > 0 else "AWAY"
            print(f"    {sigma:>6.1f} | {delta:>+12.6f} | {direction:>9} | [{k_lo:.1f}, {k_hi:.1f}]")
        print()

    # ── Part 5: Probability distribution comparison ───────────
    print("-" * 76)
    print("PART 5: Detector probability profiles (single-k vs spectral)")
    print("-" * 76)
    print()

    # Compare single k=5.0 (likely AWAY) vs broad spectrum around k0=5.0
    k_example = 5.0
    sigma_example = 2.0
    k_lo = max(0.1, k_example - 3 * sigma_example)
    k_hi = k_example + 3 * sigma_example
    k_vals = [k_lo + i * (k_hi - k_lo) / (n_samples - 1) for i in range(n_samples)]
    weights = gaussian_weights(k_vals, k_example, sigma_example)

    det_single_flat = propagate_single_k(nodes, SOURCE, flat_field, WIDTH, k_example)
    det_single_mass = propagate_single_k(nodes, SOURCE, mass_field, WIDTH, k_example)
    det_spec_flat = spectral_propagate(nodes, SOURCE, flat_field, WIDTH, k_vals, weights)
    det_spec_mass = spectral_propagate(nodes, SOURCE, mass_field, WIDTH, k_vals, weights)

    all_y = sorted(set(list(det_single_flat.keys()) + list(det_spec_flat.keys())))

    print(f"  Comparison: single k={k_example} vs spectral k0={k_example}, sigma={sigma_example}")
    print(f"  {'y':>4} | {'P_single_flat':>14} | {'P_single_mass':>14} | {'P_spec_flat':>14} | {'P_spec_mass':>14}")
    print(f"  {'-' * 70}")

    # Normalize each to probability
    def normalize_probs(det):
        total = sum(abs(a) ** 2 for a in det.values())
        if total < 1e-30:
            return {}
        return {y: abs(a) ** 2 / total for y, a in det.items()}

    p_sf = normalize_probs(det_single_flat)
    p_sm = normalize_probs(det_single_mass)
    p_xf = normalize_probs(det_spec_flat)
    p_xm = normalize_probs(det_spec_mass)

    for y in all_y:
        print(f"  {y:>4} | {p_sf.get(y, 0):>14.6f} | {p_sm.get(y, 0):>14.6f} | {p_xf.get(y, 0):>14.6f} | {p_xm.get(y, 0):>14.6f}")

    # ── Part 6: Coherence check ───────────────────────────────
    print()
    print("-" * 76)
    print("PART 6: Coherent vs incoherent averaging")
    print("-" * 76)
    print()
    print("Coherent: sum amplitudes then square (interference preserved)")
    print("Incoherent: sum probabilities (no interference)")
    print()

    for k0_test, sigma_test in [(2.5, 2.0), (5.0, 2.0), (3.0, 2.0)]:
        k_lo = max(0.1, k0_test - 3 * sigma_test)
        k_hi = k0_test + 3 * sigma_test
        k_vals = [k_lo + i * (k_hi - k_lo) / (n_samples - 1) for i in range(n_samples)]
        weights = gaussian_weights(k_vals, k0_test, sigma_test)

        # Coherent (already have this)
        det_coh_flat = spectral_propagate(nodes, SOURCE, flat_field, WIDTH, k_vals, weights)
        det_coh_mass = spectral_propagate(nodes, SOURCE, mass_field, WIDTH, k_vals, weights)
        delta_coh = centroid_shift(det_coh_mass, det_coh_flat)

        # Incoherent: sum P(y) = sum_k |w_k * psi_k(y)|^2
        incoh_flat = defaultdict(float)
        incoh_mass = defaultdict(float)
        for k_val, w in zip(k_vals, weights):
            det_f = propagate_single_k(nodes, SOURCE, flat_field, WIDTH, k_val)
            det_m = propagate_single_k(nodes, SOURCE, mass_field, WIDTH, k_val)
            for y, a in det_f.items():
                incoh_flat[y] += abs(w * a) ** 2
            for y, a in det_m.items():
                incoh_mass[y] += abs(w * a) ** 2

        # Centroid from incoherent probabilities
        def incoh_centroid(probs):
            total = sum(probs.values())
            if total < 1e-30:
                return 0.0
            return sum(y * p for y, p in probs.items()) / total

        delta_incoh = incoh_centroid(incoh_mass) - incoh_centroid(incoh_flat)
        dir_coh = "TOWARD" if delta_coh > 0 else "AWAY"
        dir_incoh = "TOWARD" if delta_incoh > 0 else "AWAY"

        print(f"  k0={k0_test}, sigma={sigma_test}:")
        print(f"    Coherent:   delta={delta_coh:+.6f} => {dir_coh}")
        print(f"    Incoherent: delta={delta_incoh:+.6f} => {dir_incoh}")
        print()

    # ── Summary ───────────────────────────────────────────────
    print("=" * 76)
    print("SUMMARY AND VERDICT")
    print("=" * 76)
    print()

    # Count TOWARD/AWAY in Gaussian spectral results
    broad_results = {k: v for k, v in spectral_results.items() if k[1] >= 2.0}
    narrow_results = {k: v for k, v in spectral_results.items() if k[1] <= 0.5}
    medium_results = {k: v for k, v in spectral_results.items() if 0.5 < k[1] < 2.0}

    def count_dir(results):
        t = sum(1 for d in results.values() if d > 0)
        a = sum(1 for d in results.values() if d <= 0)
        return t, a

    nt, na = count_dir(narrow_results)
    print(f"  Narrow spectra (sigma<=0.5):  {nt} TOWARD, {na} AWAY")
    nt, na = count_dir(medium_results)
    print(f"  Medium spectra (0.5<sigma<2): {nt} TOWARD, {na} AWAY")
    nt, na = count_dir(broad_results)
    print(f"  Broad spectra  (sigma>=2):    {nt} TOWARD, {na} AWAY")
    print()

    all_broad_toward = all(d > 0 for d in broad_results.values())
    any_broad_away = any(d <= 0 for d in broad_results.values())

    if all_broad_toward:
        print("  HYPOTHESIS SUPPORTED: All broad spectra give TOWARD.")
        print("  Spectral averaging washes out single-k resonance oscillations")
        print("  and produces universal net attraction.")
    elif any_broad_away:
        print("  HYPOTHESIS FALSIFIED: Some broad spectra still give AWAY.")
        print("  Spectral averaging does NOT universally produce attraction.")
        away_configs = [(k, s) for (k, s), d in broad_results.items() if d <= 0]
        print(f"  AWAY configs: {away_configs}")
    print()

    # Narrow vs broad comparison
    print("  Narrow-to-broad transition:")
    for k0_test in [2.5, 5.0, 3.0, 1.0]:
        deltas = []
        for sigma_test in [0.5, 1.0, 2.0]:
            key = (k0_test, sigma_test)
            if key in spectral_results:
                d = spectral_results[key]
                direction = "TOWARD" if d > 0 else "AWAY"
                deltas.append(f"s={sigma_test}: {d:+.4f} ({direction})")
        if deltas:
            print(f"    k0={k0_test}: {' | '.join(deltas)}")

    print()


if __name__ == "__main__":
    main()
