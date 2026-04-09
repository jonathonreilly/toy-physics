#!/usr/bin/env python3
"""
Cosmological Expansion from Growing DAG Geometry
=================================================
On a DAG where successive layers have MORE nodes (growing spatial volume),
the effective distance between co-moving patterns should increase, analogous
to Hubble expansion.

Physics:
  A tapered DAG has height(x) = height_0 + growth_rate * x, meaning later
  layers have more y-positions available. A wave packet propagating through
  this expanding geometry should spread, and the effective "distance" between
  two separated detectors should grow.

  The transfer matrix at each layer x maps amplitudes from the y-sites at
  layer x to y-sites at layer x+1. Because the number of sites grows, the
  matrix is RECTANGULAR (more rows than columns).

Approach:
  1. Build an expanding DAG: width=20, height_0=4, growth_rate=0.3
  2. Propagate from source at y=0, measuring RMS spread sigma(x) at each layer.
  3. Compare to a STATIC DAG (constant height=10 matching the final layer).
  4. Define scale factor a(x) = sigma_expanding(x) / sigma_static(x).
  5. Two-source test: sources at y=+2 and y=-2, measure separation growth.

Hypothesis:
  "The expanding DAG produces a growing scale factor a(x) > 1."

Falsification:
  "If a(x) <= 1, the expansion doesn't affect the propagator."
"""

import cmath
import math

# ── Parameters ──────────────────────────────────────────────────────
WIDTH = 20              # number of layers (x = 0..WIDTH-1)
HEIGHT_0 = 4            # initial half-height: y in [-H0, +H0]
GROWTH_RATE = 0.3       # height grows: H(x) = H0 + growth_rate * x
K_PHASE = 5.0           # phase wavenumber
P_ATTEN = 1.0           # 1/L^p attenuation
H_STEP = 0.5            # lattice spacing


def kernel_fn(theta):
    """Angular kernel: cos^2(theta)."""
    return math.cos(theta) ** 2


def half_height_at(x, expanding, growth_rate=None):
    """Return the half-height H at layer x."""
    gr = growth_rate if growth_rate is not None else GROWTH_RATE
    if expanding:
        return int(HEIGHT_0 + gr * x)
    else:
        return int(HEIGHT_0 + gr * (WIDTH - 1))


def y_sites_at(x, expanding, growth_rate=None):
    """Return sorted list of y-indices at layer x."""
    H = half_height_at(x, expanding, growth_rate)
    return list(range(-H, H + 1))


def mat_vec_mul(M, v, n_rows, n_cols):
    """Multiply n_rows x n_cols matrix M (flat list) by vector v (list of complex)."""
    result = [0j] * n_rows
    for i in range(n_rows):
        s = 0j
        for j in range(n_cols):
            s += M[i * n_cols + j] * v[j]
        result[i] = s
    return result


def build_layer_transfer(y_in_sites, y_out_sites, h, k, p):
    """Build the transfer matrix from layer x to layer x+1.

    Returns flat list (row-major), dimensions n_out x n_in.
    M[y_out_idx, y_in_idx] = exp(i*k*S) * w(theta) * h / L^p
    """
    n_in = len(y_in_sites)
    n_out = len(y_out_sites)
    M = [0j] * (n_out * n_in)

    for j_out, y_out in enumerate(y_out_sites):
        for j_in, y_in in enumerate(y_in_sites):
            dy = y_out - y_in
            phys_dy = dy * h
            L = math.sqrt(h ** 2 + phys_dy ** 2)
            S = L  # free space: f=0
            theta = math.atan2(abs(phys_dy), h)

            w = kernel_fn(theta)
            amplitude = cmath.exp(1j * k * S) * w * h / (L ** p)
            M[j_out * n_in + j_in] = amplitude

    return M, n_out, n_in


def propagate_and_measure(expanding, source_y_list, growth_rate=None):
    """Propagate amplitude from source(s) through the DAG.

    Returns:
        layer_xs: list of x values (1..WIDTH-1)
        sigmas: RMS spread of probability at each layer
        centroids: centroid y at each layer
        prob_profiles: dict of {layer: (y_sites, prob_list)}
    """
    gr = growth_rate if growth_rate is not None else GROWTH_RATE

    y0_sites = y_sites_at(0, expanding, gr)
    n0 = len(y0_sites)
    psi = [0j] * n0

    for src_y in source_y_list:
        if src_y in y0_sites:
            idx = y0_sites.index(src_y)
            psi[idx] = 1.0 + 0j

    norm = math.sqrt(sum(abs(a) ** 2 for a in psi))
    if norm > 0:
        psi = [a / norm for a in psi]

    layer_xs = []
    sigmas = []
    centroids = []
    prob_profiles = {}

    current_y = y0_sites

    for x in range(WIDTH - 1):
        next_y = y_sites_at(x + 1, expanding, gr)
        M, n_out, n_in = build_layer_transfer(current_y, next_y, H_STEP, K_PHASE, P_ATTEN)
        psi = mat_vec_mul(M, psi, n_out, n_in)

        norm = math.sqrt(sum(abs(a) ** 2 for a in psi))
        if norm > 0:
            psi = [a / norm for a in psi]

        prob = [abs(a) ** 2 for a in psi]
        prob_sum = sum(prob)
        if prob_sum > 0:
            prob = [p / prob_sum for p in prob]

        mean_y = sum(y * p for y, p in zip(next_y, prob))
        var_y = sum((y - mean_y) ** 2 * p for y, p in zip(next_y, prob))
        sigma = math.sqrt(max(var_y, 0.0))

        layer_xs.append(x + 1)
        sigmas.append(sigma)
        centroids.append(mean_y)

        if (x + 1) in [1, 5, 10, 15, 19]:
            prob_profiles[x + 1] = (list(next_y), list(prob))

        current_y = next_y

    return layer_xs, sigmas, centroids, prob_profiles


def two_source_separation(expanding, src_plus, src_minus, growth_rate=None):
    """Measure the separation of two wave packets as they propagate."""
    _, _, centroids_plus, _ = propagate_and_measure(expanding, [src_plus], growth_rate)
    _, _, centroids_minus, _ = propagate_and_measure(expanding, [src_minus], growth_rate)
    return [abs(cp - cm) for cp, cm in zip(centroids_plus, centroids_minus)]


def main():
    print("=" * 72)
    print("COSMOLOGICAL EXPANSION FROM GROWING DAG GEOMETRY")
    print("=" * 72)

    # ── Geometry summary ────────────────────────────────────────────
    print("\n--- Geometry ---")
    print(f"  Width (layers):    {WIDTH}")
    print(f"  Height_0:          +/-{HEIGHT_0}  ({2*HEIGHT_0+1} sites)")
    final_H = int(HEIGHT_0 + GROWTH_RATE * (WIDTH - 1))
    print(f"  Growth rate:       {GROWTH_RATE}")
    print(f"  Final height:      +/-{final_H}  ({2*final_H+1} sites)")
    print(f"  Static height:     +/-{final_H}  ({2*final_H+1} sites)")
    print(f"  Kernel:            cos^2(theta)")
    print(f"  k_phase:           {K_PHASE}")
    print(f"  h_step:            {H_STEP}")

    # ── Experiment 1: Single source, RMS spread comparison ──────────
    print("\n" + "=" * 72)
    print("EXPERIMENT 1: Single Source RMS Spread")
    print("=" * 72)

    xs_exp, sigmas_exp, _, profiles_exp = propagate_and_measure(True, [0])
    xs_sta, sigmas_sta, _, profiles_sta = propagate_and_measure(False, [0])

    print(f"\n{'Layer':>6} | {'H_exp':>6} | {'sigma_exp':>10} | {'sigma_sta':>10} | {'a(x)':>8}")
    print("-" * 55)

    scale_factors = []
    for i, x in enumerate(xs_exp):
        H_exp = half_height_at(x, True)
        a_x = sigmas_exp[i] / sigmas_sta[i] if sigmas_sta[i] > 0 else float('nan')
        scale_factors.append(a_x)
        print(f"{x:>6} | {H_exp:>6} | {sigmas_exp[i]:>10.4f} | {sigmas_sta[i]:>10.4f} | {a_x:>8.4f}")

    a_first = scale_factors[2] if len(scale_factors) > 2 else scale_factors[0]
    a_last = scale_factors[-1]
    a_growing = a_last > a_first

    print(f"\n  Scale factor a(x=3):  {a_first:.4f}")
    print(f"  Scale factor a(x=end): {a_last:.4f}")
    print(f"  a is growing:         {a_growing}")

    # ── Experiment 2: Two-source separation ─────────────────────────
    print("\n" + "=" * 72)
    print("EXPERIMENT 2: Two-Source Separation")
    print("=" * 72)

    src_plus, src_minus = 2, -2
    print(f"  Sources at y = +{src_plus} and y = -{abs(src_minus)}")

    sep_exp = two_source_separation(True, src_plus, src_minus)
    sep_sta = two_source_separation(False, src_plus, src_minus)

    print(f"\n{'Layer':>6} | {'sep_exp':>10} | {'sep_sta':>10} | {'ratio':>8}")
    print("-" * 45)

    sep_ratios = []
    for i, x in enumerate(xs_exp):
        ratio = sep_exp[i] / sep_sta[i] if sep_sta[i] > 0 else float('nan')
        sep_ratios.append(ratio)
        if x in [1, 3, 5, 10, 15, 19]:
            print(f"{x:>6} | {sep_exp[i]:>10.4f} | {sep_sta[i]:>10.4f} | {ratio:>8.4f}")

    sep_first = sep_ratios[2] if len(sep_ratios) > 2 else sep_ratios[0]
    sep_last = sep_ratios[-1]
    sep_growing = sep_last > sep_first

    print(f"\n  Sep ratio (x=3):   {sep_first:.4f}")
    print(f"  Sep ratio (x=end): {sep_last:.4f}")
    print(f"  Ratio growing:     {sep_growing}")

    # ── Experiment 3: Probability profiles ──────────────────────────
    print("\n" + "=" * 72)
    print("EXPERIMENT 3: Probability Profile Snapshots")
    print("=" * 72)

    for x_snap in sorted(profiles_exp.keys()):
        if x_snap in profiles_sta:
            ys_e, ps_e = profiles_exp[x_snap]
            ys_s, ps_s = profiles_sta[x_snap]
            peak_e = max(ps_e) if ps_e else 0
            peak_s = max(ps_s) if ps_s else 0
            print(f"\n  Layer {x_snap}:")
            print(f"    Expanding: {len(ys_e)} sites, peak prob = {peak_e:.6f}")
            print(f"    Static:    {len(ys_s)} sites, peak prob = {peak_s:.6f}")

    # ── Experiment 4: Growth rate sweep ─────────────────────────────
    print("\n" + "=" * 72)
    print("EXPERIMENT 4: Growth Rate Sweep")
    print("=" * 72)

    growth_rates = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8]
    print(f"\n{'growth':>8} | {'sigma_final':>12} | {'a_final':>8} | {'sep_ratio_final':>16}")
    print("-" * 55)

    for gr in growth_rates:
        xs_g, sigmas_g, _, _ = propagate_and_measure(True, [0], growth_rate=gr)
        xs_s, sigmas_s, _, _ = propagate_and_measure(False, [0], growth_rate=gr)
        a_final = sigmas_g[-1] / sigmas_s[-1] if sigmas_s[-1] > 0 else float('nan')

        sep_g = two_source_separation(True, 2, -2, growth_rate=gr)
        sep_s = two_source_separation(False, 2, -2, growth_rate=gr)
        sr_final = sep_g[-1] / sep_s[-1] if sep_s[-1] > 0 else float('nan')

        print(f"{gr:>8.1f} | {sigmas_g[-1]:>12.4f} | {a_final:>8.4f} | {sr_final:>16.4f}")

    # ── Verdict ─────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    expansion_in_rms = a_last > 1.05 and a_growing
    expansion_in_sep = sep_last > 1.05 and sep_growing

    print(f"\n  RMS scale factor test:")
    print(f"    a(final) = {a_last:.4f}, growing = {a_growing}")
    print(f"    PASS: {expansion_in_rms}")

    print(f"\n  Two-source separation test:")
    print(f"    ratio(final) = {sep_last:.4f}, growing = {sep_growing}")
    print(f"    PASS: {expansion_in_sep}")

    if expansion_in_rms and expansion_in_sep:
        verdict = "CONFIRMED"
        detail = ("Growing DAG geometry produces cosmological expansion: "
                  "both RMS spread and two-source separation grow faster "
                  "than on a static DAG.")
    elif expansion_in_rms or expansion_in_sep:
        verdict = "PARTIAL"
        detail = (f"One test passes (RMS={expansion_in_rms}, "
                  f"Sep={expansion_in_sep}). Expansion effect present "
                  f"but not fully consistent.")
    else:
        verdict = "FALSIFIED"
        detail = ("Neither RMS spread nor two-source separation show "
                  "expansion. Growing geometry does not produce "
                  "Hubble-like expansion in the propagator.")

    print(f"\n  Hypothesis: 'The expanding DAG produces a growing "
          f"scale factor a(x) > 1.'")
    print(f"  Verdict:    {verdict}")
    print(f"  Detail:     {detail}")
    print()


if __name__ == "__main__":
    main()
