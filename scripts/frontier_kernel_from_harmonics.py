#!/usr/bin/env python3
"""Kernel as harmonic low-pass filter: angular decomposition of gravity.

THE IDEA:
  If gravity is a resonance phenomenon, the angular kernel w(theta) determines
  WHICH harmonics of the path-length interference contribute. A decreasing
  kernel suppresses large-theta paths (long diagonals) which carry higher
  harmonics. If higher harmonics cause destructive interference (repulsion),
  then suppressing them maintains the fundamental attractive mode.

APPROACH:
  Part 1: Angular band decomposition -- run propagation with angle-selective
    kernels (forward-only, moderate, diagonal-only). Measure gravity signal
    from each band separately.

  Part 2: Harmonic analysis -- Fourier-transform the gravitational perturbation
    psi_grav(y) = psi_mass(y) - psi_flat(y). Check if the fundamental mode
    is TOWARD and higher modes are AWAY.

  Part 3: Kernel = low-pass filter -- for each kernel (uniform, cos, cos^2,
    exp), compute the fraction of gravitational perturbation power in the
    fundamental vs higher harmonics.

HYPOTHESIS: "Forward-angle paths give TOWARD, diagonal paths give AWAY.
  The kernel acts as a harmonic low-pass filter."

FALSIFICATION: "If all angular ranges give the same gravity direction."

Uses 2D DAG infrastructure from toy_event_physics. Pure Python (no numpy).
"""
from __future__ import annotations

import cmath
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import build_rectangular_nodes

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
WIDTH = 16
HEIGHT = 6
K = 5.0
STRENGTH = 5e-4
MASS_POS = (10, 4)


# ---------------------------------------------------------------------------
# Pure-Python DFT
# ---------------------------------------------------------------------------
def dft(x):
    """Discrete Fourier Transform of a list of complex numbers."""
    N = len(x)
    result = []
    for m in range(N):
        s = 0j
        for n in range(N):
            s += x[n] * cmath.exp(-2j * math.pi * m * n / N)
        result.append(s)
    return result


def idft_single_mode(fft_vals, m, N):
    """Inverse DFT reconstructing only mode m (and its conjugate)."""
    result = []
    for n in range(N):
        s = fft_vals[m] * cmath.exp(2j * math.pi * m * n / N)
        if 0 < m < N // 2:
            conj_m = N - m
            s += fft_vals[conj_m] * cmath.exp(2j * math.pi * conj_m * n / N)
        result.append(s.real / N)
    return result


# ---------------------------------------------------------------------------
# DAG builder
# ---------------------------------------------------------------------------
def build_forward_dag(nodes):
    """Forward-causal DAG: edges from x to x+1, dy in {-1, 0, 1}."""
    dag = defaultdict(list)
    for node in nodes:
        x, y = node
        for dy in [-1, 0, 1]:
            nb = (x + 1, y + dy)
            if nb in nodes:
                dag[node].append(nb)
    return dag


def edge_angle_deg(src, dst):
    """Angle of edge relative to forward (x) direction, in degrees."""
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    return math.degrees(math.atan2(abs(dy), dx))


# ---------------------------------------------------------------------------
# Field
# ---------------------------------------------------------------------------
def spatial_only_field(nodes, mass_pos, strength):
    _mx, my = mass_pos
    field = {}
    for n in nodes:
        r = abs(n[1] - my) + 0.1
        field[n] = strength / r
    return field


# ---------------------------------------------------------------------------
# Propagation
# ---------------------------------------------------------------------------
def propagate_angle_band(nodes, source, node_field, dag, k,
                         theta_min_deg=None, theta_max_deg=None):
    """Propagate with S = L*(1-f), 1/L attenuation, angle-band filter."""
    order = sorted(nodes, key=lambda n: n[0])
    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == WIDTH:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for nb in dag.get(node, []):
            theta = edge_angle_deg(node, nb)
            if theta_min_deg is not None and theta < theta_min_deg:
                continue
            if theta_max_deg is not None and theta > theta_max_deg:
                continue
            L = math.dist(node, nb)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) / L
            states[nb] += amp * edge_amp

    return detector


def propagate_with_kernel(nodes, source, node_field, dag, k, kernel_fn):
    """Propagate with angular kernel w(theta). Edge amp = exp(i*k*S) * w / L."""
    order = sorted(nodes, key=lambda n: n[0])
    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == WIDTH:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            theta = math.atan2(abs(nb[1] - node[1]), nb[0] - node[0])
            w = kernel_fn(theta)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) * w / L
            states[nb] += amp * edge_amp

    return detector


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------
def centroid_and_prob(det):
    total = sum(abs(a) ** 2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    c = sum(y * abs(a) ** 2 for y, a in det.items()) / total
    return c, total


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------
def part1_angular_bands(nodes, source, dag, flat_field, mass_field):
    print("=" * 72)
    print("PART 1: ANGULAR BAND DECOMPOSITION")
    print("=" * 72)
    print()
    print("Run propagation with angle-selective kernels to see which angular")
    print("range produces TOWARD vs AWAY gravity.")
    print()

    bands = [
        ("ALL angles",        None,  None),
        ("Forward (<15d)",    None,  15.0),
        ("Moderate (15-45d)", 15.0,  45.0),
        ("Diagonal (>45d)",   45.0,  None),
        ("Narrow fwd (<5d)",  None,   5.0),
        ("Semi-fwd (<30d)",   None,  30.0),
    ]

    print(f"  {'Band':<22s} | {'c_flat':>10s} | {'c_mass':>10s} | {'delta':>12s} | {'dir':>6s} | {'prob_flat':>10s}")
    print(f"  {'-' * 82}")

    band_results = {}
    for label, tmin, tmax in bands:
        det_flat = propagate_angle_band(nodes, source, flat_field, dag, K, tmin, tmax)
        det_mass = propagate_angle_band(nodes, source, mass_field, dag, K, tmin, tmax)
        c_flat, p_flat = centroid_and_prob(det_flat)
        c_mass, p_mass = centroid_and_prob(det_mass)
        delta = c_mass - c_flat
        direction = "TOWARD" if delta > 0 else "AWAY" if delta < 0 else "NONE"
        print(f"  {label:<22s} | {c_flat:>+10.4f} | {c_mass:>+10.4f} | {delta:>+12.6f} | {direction:>6s} | {p_flat:>10.3e}")
        band_results[label] = (delta, direction, p_flat)

    print()

    fwd_delta = band_results.get("Forward (<15d)", (0,))[0]
    diag_delta = band_results.get("Diagonal (>45d)", (0,))[0]
    fwd_dir = "TOWARD" if fwd_delta > 0 else "AWAY"
    diag_dir = "TOWARD" if diag_delta > 0 else "AWAY"

    print("  HYPOTHESIS CHECK:")
    print(f"    Forward paths: {fwd_dir} (delta={fwd_delta:+.6f})")
    print(f"    Diagonal paths: {diag_dir} (delta={diag_delta:+.6f})")
    if fwd_dir == "TOWARD" and diag_dir == "AWAY":
        print("    => SUPPORTED: Forward=TOWARD, Diagonal=AWAY")
    elif fwd_dir == diag_dir:
        print(f"    => FALSIFIED: Both bands give {fwd_dir}")
    else:
        print(f"    => PARTIAL: Forward={fwd_dir}, Diagonal={diag_dir}")

    return band_results


# ---------------------------------------------------------------------------
# Part 2
# ---------------------------------------------------------------------------
def part2_harmonic_analysis(nodes, source, dag, flat_field, mass_field):
    print()
    print("=" * 72)
    print("PART 2: HARMONIC ANALYSIS OF GRAVITATIONAL PERTURBATION")
    print("=" * 72)
    print()

    det_flat = propagate_with_kernel(nodes, source, flat_field, dag, K,
                                     lambda theta: 1.0)
    det_mass = propagate_with_kernel(nodes, source, mass_field, dag, K,
                                     lambda theta: 1.0)

    y_range = sorted(set(det_flat.keys()) | set(det_mass.keys()))
    N = len(y_range)

    prob_flat = [abs(det_flat.get(y, 0j)) ** 2 for y in y_range]
    prob_mass = [abs(det_mass.get(y, 0j)) ** 2 for y in y_range]
    prob_diff = [pm - pf for pm, pf in zip(prob_mass, prob_flat)]

    # DFT of prob difference
    fft_pd = dft(prob_diff)
    powers = [abs(c) ** 2 for c in fft_pd]
    total_power = sum(powers)

    print(f"  Detector y-range: {y_range[0]} to {y_range[-1]} ({N} points)")
    print()
    print("  PROBABILITY DIFFERENCE HARMONICS (|psi_mass|^2 - |psi_flat|^2):")
    print(f"  {'mode':>6s} | {'|amplitude|':>12s} | {'phase (deg)':>12s} | {'power%':>8s}")
    print(f"  {'-' * 50}")

    n_show = min(N // 2, 8)
    for m in range(n_show):
        amp = abs(fft_pd[m])
        phase = math.degrees(cmath.phase(fft_pd[m]))
        pwr_pct = powers[m] / total_power * 100 if total_power > 0 else 0
        print(f"  {m:>6d} | {amp:>12.6e} | {phase:>+12.1f} | {pwr_pct:>7.1f}%")

    # Centroid contribution by harmonic mode
    print()
    print("  CENTROID CONTRIBUTION BY HARMONIC MODE:")
    print(f"  {'mode':>6s} | {'centroid_shift':>14s} | {'dir':>6s} | {'power%':>8s}")
    print(f"  {'-' * 45}")

    y_arr = [float(y) for y in y_range]
    total_prob_mass = sum(prob_mass)

    mode_results = []
    for m in range(n_show):
        recon = idft_single_mode(fft_pd, m, N)
        c_shift = sum(y_arr[i] * recon[i] for i in range(N))
        if total_prob_mass > 1e-30:
            c_shift /= total_prob_mass
        direction = "TOWARD" if c_shift > 0 else "AWAY" if c_shift < 0 else "NONE"
        pwr_pct = powers[m] / total_power * 100 if total_power > 0 else 0
        print(f"  {m:>6d} | {c_shift:>+14.6e} | {direction:>6s} | {pwr_pct:>7.1f}%")
        mode_results.append((m, c_shift, direction, pwr_pct))

    print()
    toward_modes = [m for m, cs, d, pf in mode_results if d == "TOWARD"]
    away_modes = [m for m, cs, d, pf in mode_results if d == "AWAY"]
    print(f"  TOWARD modes: {toward_modes}")
    print(f"  AWAY modes:   {away_modes}")

    if toward_modes and away_modes:
        t_strongest = max([(m, abs(cs)) for m, cs, d, _ in mode_results if d == "TOWARD"], key=lambda x: x[1])
        a_strongest = max([(m, abs(cs)) for m, cs, d, _ in mode_results if d == "AWAY"], key=lambda x: x[1])
        print(f"  Strongest TOWARD: mode {t_strongest[0]}")
        print(f"  Strongest AWAY:   mode {a_strongest[0]}")
        if t_strongest[0] < a_strongest[0]:
            print("  => Low harmonics TOWARD, high harmonics AWAY")
            print("     CONSISTENT with low-pass filter hypothesis")
        else:
            print("  => Pattern does NOT support simple low-pass filter")

    return mode_results, fft_pd, y_range


# ---------------------------------------------------------------------------
# Part 3
# ---------------------------------------------------------------------------
def part3_kernel_filter_analysis(nodes, source, dag, flat_field, mass_field):
    print()
    print("=" * 72)
    print("PART 3: KERNEL = LOW-PASS FILTER")
    print("=" * 72)
    print()
    print("For each kernel, compute gravity and harmonic content.")
    print()

    kernels = [
        ("uniform",       lambda theta: 1.0),
        ("cos(theta)",    lambda theta: math.cos(theta)),
        ("cos^2(theta)",  lambda theta: math.cos(theta) ** 2),
        ("cos^3(theta)",  lambda theta: math.cos(theta) ** 3),
        ("exp(-0.8*t^2)", lambda theta: math.exp(-0.8 * theta * theta)),
        ("exp(-2.0*t^2)", lambda theta: math.exp(-2.0 * theta * theta)),
        ("forward_only",  lambda theta: 1.0 if theta < 0.01 else 0.0),
    ]

    print(f"  {'Kernel':<18s} | {'gravity':>10s} | {'dir':>6s} | {'m0%':>6s} | {'m1%':>6s} | {'m2%':>6s} | {'fund/high':>10s}")
    print(f"  {'-' * 80}")

    kernel_data = []
    for name, kfn in kernels:
        det_flat = propagate_with_kernel(nodes, source, flat_field, dag, K, kfn)
        det_mass = propagate_with_kernel(nodes, source, mass_field, dag, K, kfn)

        c_flat, p_flat = centroid_and_prob(det_flat)
        c_mass, p_mass = centroid_and_prob(det_mass)
        delta = c_mass - c_flat
        direction = "TOWARD" if delta > 0 else "AWAY" if delta < 0 else "NONE"

        y_range = sorted(set(det_flat.keys()) | set(det_mass.keys()))
        N = len(y_range)
        prob_diff = [abs(det_mass.get(y, 0j)) ** 2 - abs(det_flat.get(y, 0j)) ** 2 for y in y_range]

        fft_pd = dft(prob_diff)
        powers = [abs(c) ** 2 for c in fft_pd]
        total_power = sum(powers)

        mode_pcts = []
        for m in range(min(3, max(N // 2, 1))):
            pct = powers[m] / total_power * 100 if total_power > 0 else 0
            mode_pcts.append(pct)
        while len(mode_pcts) < 3:
            mode_pcts.append(0.0)

        fund_power = powers[0] + (powers[1] if N > 1 else 0)
        high_power = sum(powers[2:N // 2]) if N > 3 else 1e-30
        ratio = fund_power / high_power if high_power > 1e-30 else float('inf')

        print(f"  {name:<18s} | {delta:>+10.6f} | {direction:>6s} | {mode_pcts[0]:>5.1f}% | {mode_pcts[1]:>5.1f}% | {mode_pcts[2]:>5.1f}% | {ratio:>10.2f}")
        kernel_data.append((name, delta, direction, mode_pcts, ratio))

    print()

    toward_kernels = [(n, d, r) for n, d, dr, _, r in kernel_data if dr == "TOWARD"]
    away_kernels = [(n, d, r) for n, d, dr, _, r in kernel_data if dr == "AWAY"]

    print("  ANALYSIS:")
    if toward_kernels:
        print(f"  TOWARD kernels: {[n for n, _, _ in toward_kernels]}")
    if away_kernels:
        print(f"  AWAY kernels: {[n for n, _, _ in away_kernels]}")

    if toward_kernels and away_kernels:
        t_ratios = [r for _, _, r in toward_kernels if r < 1e10]
        a_ratios = [r for _, _, r in away_kernels if r < 1e10]
        if t_ratios and a_ratios:
            avg_t = sum(t_ratios) / len(t_ratios)
            avg_a = sum(a_ratios) / len(a_ratios)
            print(f"  Avg fund/high ratio (TOWARD): {avg_t:.2f}")
            print(f"  Avg fund/high ratio (AWAY):   {avg_a:.2f}")
            if avg_t > avg_a:
                print("  => TOWARD kernels have higher fundamental-to-harmonic ratio")
                print("  => CONSISTENT with low-pass filter hypothesis")
            else:
                print("  => Ratio does NOT correlate with gravity direction")

    return kernel_data


# ---------------------------------------------------------------------------
# Part 4: k-dependence
# ---------------------------------------------------------------------------
def part4_k_dependence(nodes, source, dag, flat_field, mass_field):
    print()
    print("=" * 72)
    print("PART 4: k-DEPENDENCE -- RESONANCE STRUCTURE")
    print("=" * 72)
    print()

    k_values = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0]

    kernels_to_test = [
        ("uniform",      lambda theta: 1.0),
        ("cos^2(theta)", lambda theta: math.cos(theta) ** 2),
    ]

    for kname, kfn in kernels_to_test:
        print(f"  Kernel: {kname}")
        print(f"  {'k':>6s} | {'delta':>12s} | {'dir':>6s}")
        print(f"  {'-' * 30}")

        n_toward = 0
        n_away = 0
        for kval in k_values:
            det_flat = propagate_with_kernel(nodes, source, flat_field, dag, kval, kfn)
            det_mass = propagate_with_kernel(nodes, source, mass_field, dag, kval, kfn)
            c_flat, _ = centroid_and_prob(det_flat)
            c_mass, _ = centroid_and_prob(det_mass)
            delta = c_mass - c_flat
            direction = "TOWARD" if delta > 0 else "AWAY" if delta < 0 else "NONE"
            print(f"  {kval:>6.1f} | {delta:>+12.6f} | {direction:>6s}")
            if delta > 0:
                n_toward += 1
            elif delta < 0:
                n_away += 1

        print(f"  TOWARD: {n_toward}/{len(k_values)}, AWAY: {n_away}/{len(k_values)}")
        if n_toward > 0 and n_away > 0:
            print("  => Sign FLIPS with k -- resonance structure confirmed")
        elif n_toward == len(k_values):
            print("  => Always TOWARD -- robust attraction")
        elif n_away == len(k_values):
            print("  => Always AWAY -- robust repulsion")
        print()


# ---------------------------------------------------------------------------
# Part 5: distance dependence by band
# ---------------------------------------------------------------------------
def part5_distance_by_band(nodes, source, dag, flat_field):
    print()
    print("=" * 72)
    print("PART 5: ANGULAR BAND CONTRIBUTION vs MASS DISTANCE")
    print("=" * 72)
    print()

    mass_y_values = [2, 3, 4, 5, 6]
    bands = [
        ("Fwd(<15)", None, 15.0),
        ("Mod(15-45)", 15.0, 45.0),
        ("Diag(>45)", 45.0, None),
    ]

    header = f"  {'mass_y':>6s}"
    for label, _, _ in bands:
        header += f" | {label:>22s}"
    print(header)
    print(f"  {'-' * 80}")

    for my in mass_y_values:
        mass_field_local = spatial_only_field(nodes, (10, my), STRENGTH)
        line = f"  {my:>6d}"
        for label, tmin, tmax in bands:
            det_flat = propagate_angle_band(nodes, source, flat_field, dag, K, tmin, tmax)
            det_mass = propagate_angle_band(nodes, source, mass_field_local, dag, K, tmin, tmax)
            c_flat, p_flat = centroid_and_prob(det_flat)
            c_mass, _ = centroid_and_prob(det_mass)
            delta = c_mass - c_flat
            d_str = "T" if delta > 0 else "A"
            line += f" | {delta:>+12.6f} ({d_str}) [{p_flat:.0e}]"
        print(line)

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("KERNEL FROM HARMONICS: Angular Decomposition of Gravity Signal")
    print("=" * 72)
    print()
    print(f"Parameters: WIDTH={WIDTH}, HEIGHT={HEIGHT}, k={K}, strength={STRENGTH}")
    print(f"Mass position: {MASS_POS}")
    print(f"Source: (0, 0)")
    print(f"Action: S = L*(1-f), attenuation: 1/L")
    print()

    nodes = build_rectangular_nodes(WIDTH, HEIGHT)
    source = (0, 0)
    dag = build_forward_dag(nodes)

    flat_field = {n: 0.0 for n in nodes}
    mass_field = spatial_only_field(nodes, MASS_POS, STRENGTH)

    vals = list(mass_field.values())
    print(f"  Field range: [{min(vals):.2e}, {max(vals):.2e}], mean={sum(vals)/len(vals):.2e}")

    n_fwd = n_mod = n_diag = 0
    for node in nodes:
        for nb in dag.get(node, []):
            theta = edge_angle_deg(node, nb)
            if theta < 15:
                n_fwd += 1
            elif theta < 45:
                n_mod += 1
            else:
                n_diag += 1
    print(f"  Edges by angle: forward(<15d)={n_fwd}, moderate(15-45d)={n_mod}, diagonal(>45d)={n_diag}")
    print()

    band_results = part1_angular_bands(nodes, source, dag, flat_field, mass_field)
    mode_results, fft_pd, y_range = part2_harmonic_analysis(nodes, source, dag, flat_field, mass_field)
    kernel_data = part3_kernel_filter_analysis(nodes, source, dag, flat_field, mass_field)
    part4_k_dependence(nodes, source, dag, flat_field, mass_field)
    part5_distance_by_band(nodes, source, dag, flat_field)

    # ---------------------------------------------------------------------------
    # Overall verdict
    # ---------------------------------------------------------------------------
    print()
    print("=" * 72)
    print("OVERALL VERDICT")
    print("=" * 72)
    print()

    fwd_delta = band_results.get("Forward (<15d)", (0,))[0]
    diag_delta = band_results.get("Diagonal (>45d)", (0,))[0]
    fwd_dir = "TOWARD" if fwd_delta > 0 else "AWAY"
    diag_dir = "TOWARD" if diag_delta > 0 else "AWAY"
    p1_supported = (fwd_dir == "TOWARD" and diag_dir == "AWAY")

    toward_modes = [m for m, cs, d, pf in mode_results if d == "TOWARD"]
    away_modes = [m for m, cs, d, pf in mode_results if d == "AWAY"]
    p2_supported = False
    if toward_modes and away_modes:
        p2_supported = min(toward_modes) < min(away_modes)

    toward_ratios = [r for n, d, dr, _, r in kernel_data if dr == "TOWARD" and r < 1e10]
    away_ratios = [r for n, d, dr, _, r in kernel_data if dr == "AWAY" and r < 1e10]
    p3_supported = False
    if toward_ratios and away_ratios:
        p3_supported = (sum(toward_ratios) / len(toward_ratios) >
                        sum(away_ratios) / len(away_ratios))

    print(f"  Part 1 (angular bands):      {'SUPPORTED' if p1_supported else 'NOT SUPPORTED'}")
    print(f"    Forward paths: {fwd_dir}, Diagonal paths: {diag_dir}")
    print()
    print(f"  Part 2 (harmonic modes):     {'SUPPORTED' if p2_supported else 'NOT SUPPORTED'}")
    print(f"    TOWARD modes: {toward_modes}, AWAY modes: {away_modes}")
    print()
    print(f"  Part 3 (kernel filter):      {'SUPPORTED' if p3_supported else 'NOT SUPPORTED'}")
    if toward_ratios:
        print(f"    TOWARD avg ratio: {sum(toward_ratios)/len(toward_ratios):.2f}")
    if away_ratios:
        print(f"    AWAY avg ratio:   {sum(away_ratios)/len(away_ratios):.2f}")
    print()

    n_sup = sum([p1_supported, p2_supported, p3_supported])
    if n_sup == 3:
        print("  HYPOTHESIS SUPPORTED:")
        print("  The angular kernel acts as a harmonic low-pass filter.")
        print("  Forward-angle paths contribute the fundamental attractive mode.")
        print("  Diagonal paths contribute higher harmonics that cause repulsion.")
        print("  The kernel suppresses the repulsive harmonics, enabling gravity.")
    elif n_sup > 0:
        print("  HYPOTHESIS PARTIALLY SUPPORTED:")
        print(f"  {n_sup}/3 sub-hypotheses confirmed.")
        if not p1_supported:
            print("  - Angular band decomposition: forward and diagonal give SAME direction")
        if not p2_supported:
            print("  - Harmonic decomposition: low and high modes give SAME direction")
        if not p3_supported:
            print("  - Kernel fund/high ratio does not correlate with gravity direction")
    else:
        print("  HYPOTHESIS FALSIFIED:")
        print("  All angular ranges give the same gravity direction.")
        print("  The kernel is NOT acting as a simple harmonic low-pass filter.")
        print("  The gravity mechanism is more subtle than harmonic selection.")

    print()


if __name__ == "__main__":
    main()
