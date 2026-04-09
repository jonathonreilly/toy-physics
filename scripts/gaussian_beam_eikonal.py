#!/usr/bin/env python3
"""Gaussian-beam-corrected eikonal for the lattice propagator.

The plain eikonal (plane-wave) gives slope −1.28 on b∈{3..6}.
The lattice gives −1.43. The gap should be closed by accounting
for the Gaussian angular weight exp(−β·θ²) which localizes the
beam transversely.

The key idea: instead of integrating the deflection along a single
straight ray at y=0, we integrate over ALL rays weighted by the
propagator's angular profile. Each ray at angle θ from the forward
axis carries weight exp(−β·θ²). At distance x downstream, a ray
at angle θ has transverse position y = x·tan(θ) ≈ x·θ.

The beam-corrected deflection at impact parameter b:

  <δy>(b) = ∫∫ w(θ) · δy_ray(b, θ) dθ / ∫ w(θ) dθ

where:
  w(θ) = exp(−β·θ²)
  δy_ray(b, θ) = eikonal deflection for a ray at transverse offset y = x·θ

For a ray at transverse offset y₀ (set by the angle at the source),
the effective impact parameter is b - y₀ (the potential source is at
transverse position b). So:

  <δy>(b) = ∫ exp(−β·θ²) · I_geom(b - x_ref·θ) dθ / ∫ exp(−β·θ²) dθ

where I_geom(b_eff) is the single-ray eikonal integral at effective
impact parameter b_eff, and x_ref is some reference distance (we use
x_src since that's where the potential is strongest).

This is a Gaussian convolution of I_geom(b) in the transverse direction,
with width σ_b = x_src / √(2β).

If this gives slope ≈ −1.43 AND is L-independent (because β sets the
effective integration width, not L), it's the complete derivation.

We also test: does the beam-corrected prediction become L-independent?
"""

from __future__ import annotations
import math


def I_geom_single(b_eff, x_src, L):
    """Single-ray eikonal geometric factor.

    I = (1/b) · [(L-x_src)/√((L-x_src)²+b²) + x_src/√(x_src²+b²)]
    """
    if abs(b_eff) < 0.01:
        return 0.0  # avoid singularity
    def F(x):
        return (x - x_src) / math.sqrt((x - x_src) ** 2 + b_eff ** 2)
    return (1.0 / b_eff) * (F(L) - F(0))


def gaussian_beam_eikonal(b, x_src, L, beta, n_theta=2000):
    """Gaussian-beam-corrected eikonal deflection.

    Integrate over ray angles θ weighted by exp(−β·θ²).
    Each ray at angle θ passes the potential source at effective
    impact parameter b_eff = b - x_src·tan(θ) ≈ b - x_src·θ.

    The beam width at the source is σ_y = x_src·σ_θ where σ_θ = 1/√(2β).
    """
    sigma_theta = 1.0 / math.sqrt(2 * beta)
    # Integrate from −4σ to +4σ
    theta_max = 4 * sigma_theta
    dtheta = 2 * theta_max / n_theta

    num = 0.0
    den = 0.0
    for i in range(n_theta):
        theta = -theta_max + (i + 0.5) * dtheta
        w = math.exp(-beta * theta * theta)

        # Effective impact parameter at the source position
        b_eff = b - x_src * math.tan(theta)

        if abs(b_eff) < 0.05:
            # Skip near-singular points
            continue

        I_ray = I_geom_single(b_eff, x_src, L)
        num += w * I_ray * dtheta
        den += w * dtheta

    if den < 1e-30:
        return float('nan')
    return num / den


def power_law_fit(b_vals, I_vals):
    """Log-log linear fit → slope and prefactor."""
    n = len(b_vals)
    log_b = [math.log(b) for b in b_vals]
    log_I = [math.log(abs(I)) for I in I_vals]
    sx = sum(log_b)
    sy = sum(log_I)
    sxx = sum(x * x for x in log_b)
    sxy = sum(x * y for x, y in zip(log_b, log_I))
    denom = n * sxx - sx * sx
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    prefactor = math.exp(intercept)

    pred = [slope * x + intercept for x in log_b]
    ss_res = sum((y - p) ** 2 for y, p in zip(log_I, pred))
    ss_tot = sum((y - sy / n) ** 2 for y in log_I)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0
    return slope, prefactor, r2


def main():
    beta = 0.8
    L = 15.0
    x_src = 5.0

    print("=" * 80)
    print("GAUSSIAN-BEAM-CORRECTED EIKONAL DEFLECTION")
    print(f"  β={beta}, L={L}, x_src={x_src}")
    print(f"  Beam width at source: σ_y = x_src/√(2β) = {x_src/math.sqrt(2*beta):.3f}")
    print(f"  Beam angular width: σ_θ = 1/√(2β) = {1/math.sqrt(2*beta):.3f} rad = {math.degrees(1/math.sqrt(2*beta)):.1f}°")
    print("=" * 80)

    b_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]

    # 1. Compare plane-wave vs Gaussian-beam eikonal
    print(f"\n  {'b':>5s}  {'I_plane':>12s}  {'I_gauss':>12s}  {'ratio':>8s}")
    print(f"  {'-'*50}")

    plane_vals = []
    gauss_vals = []
    for b in b_values:
        I_plane = I_geom_single(b, x_src, L)
        I_gauss = gaussian_beam_eikonal(b, x_src, L, beta)
        ratio = I_gauss / I_plane if abs(I_plane) > 1e-30 else float('nan')
        print(f"  {b:5.1f}  {I_plane:12.6f}  {I_gauss:12.6f}  {ratio:8.4f}")
        plane_vals.append(I_plane)
        gauss_vals.append(I_gauss)

    # 2. Power-law fits on b ∈ {3..6}
    fit_b = [b for b in b_values if 3 <= b <= 6]
    fit_plane = [I for b, I in zip(b_values, plane_vals) if 3 <= b <= 6]
    fit_gauss = [I for b, I in zip(b_values, gauss_vals) if 3 <= b <= 6]

    slope_p, pf_p, r2_p = power_law_fit(fit_b, fit_plane)
    slope_g, pf_g, r2_g = power_law_fit(fit_b, fit_gauss)

    print(f"\n  POWER-LAW FITS on b ∈ {{3..6}}:")
    print(f"    Plane-wave:    I ≈ {pf_p:.4f} · b^({slope_p:.4f})   R²={r2_p:.6f}")
    print(f"    Gaussian-beam: I ≈ {pf_g:.4f} · b^({slope_g:.4f})   R²={r2_g:.6f}")
    print(f"    LATTICE:       kubo ≈ 28.4 · b^(−1.43)")
    print(f"\n    Plane-wave  Δslope = {abs(slope_p - (-1.43)):.4f}")
    print(f"    Gauss-beam  Δslope = {abs(slope_g - (-1.43)):.4f}")

    if abs(slope_g - (-1.43)) < abs(slope_p - (-1.43)):
        improvement = abs(slope_p - (-1.43)) - abs(slope_g - (-1.43))
        print(f"    → Gaussian correction IMPROVES the match by {improvement:.4f}")
    else:
        print(f"    → Gaussian correction does NOT improve the match")

    # 3. L-independence test
    print(f"\n  L-INDEPENDENCE TEST:")
    print(f"  Does the Gaussian-beam slope depend on L?")
    print(f"  (Lattice shows L-independence: slope ≈ −1.43 at both T=7.5 and T=15)")
    print()
    print(f"  {'L':>6s}  {'x_src':>6s}  {'slope':>8s}  {'R²':>8s}")
    print(f"  {'-'*40}")

    for L_test in [7.5, 10.0, 15.0, 22.5, 30.0, 45.0]:
        x_src_test = L_test / 3.0
        test_b = [3.0, 4.0, 5.0, 6.0]
        test_I = [gaussian_beam_eikonal(b, x_src_test, L_test, beta) for b in test_b]
        if any(math.isnan(I) for I in test_I):
            print(f"  {L_test:6.1f}  {x_src_test:6.2f}  {'NaN':>8s}")
            continue
        sl, _, r2 = power_law_fit(test_b, test_I)
        print(f"  {L_test:6.1f}  {x_src_test:6.2f}  {sl:8.4f}  {r2:8.6f}")

    # 4. Beta sweep of the corrected eikonal
    print(f"\n  BETA SWEEP of Gaussian-beam slope (L={L}, x_src={x_src}):")
    print(f"  Does varying β predict the lattice β-sweep?")
    print()
    print(f"  {'β':>6s}  {'σ_y':>8s}  {'slope':>8s}  {'R²':>8s}")
    print(f"  {'-'*40}")

    for beta_test in [0.1, 0.2, 0.4, 0.8, 1.5, 3.0, 5.0, 10.0, 20.0]:
        test_b = [3.0, 4.0, 5.0, 6.0]
        test_I = [gaussian_beam_eikonal(b, x_src, L, beta_test) for b in test_b]
        if any(math.isnan(I) for I in test_I):
            print(f"  {beta_test:6.2f}  {'NaN':>8s}")
            continue
        sl, _, r2 = power_law_fit(test_b, test_I)
        sigma_y = x_src / math.sqrt(2 * beta_test)
        print(f"  {beta_test:6.2f}  {sigma_y:8.3f}  {sl:8.4f}  {r2:8.6f}")

    # 5. Summary
    print(f"\n{'='*80}")
    print("VERDICT")
    print("=" * 80)
    print(f"  Plane-wave eikonal:     slope = {slope_p:.4f} (Δ = {abs(slope_p-(-1.43)):.4f} from lattice)")
    print(f"  Gaussian-beam eikonal:  slope = {slope_g:.4f} (Δ = {abs(slope_g-(-1.43)):.4f} from lattice)")
    print(f"  Lattice measurement:    slope = −1.43")


if __name__ == "__main__":
    main()
