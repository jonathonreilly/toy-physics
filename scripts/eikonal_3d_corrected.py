#!/usr/bin/env python3
"""3D-corrected eikonal prediction for lensing.

The previous eikonal calculations used 2D geometry, but the actual
propagator runs on a 3D grown DAG with kernel:

    weight = exp(i·k·L) · exp(-β·θ²) · H² / L²

where θ is the 3D angle: θ = atan2(r_perp, dx), r_perp = √(dy²+dz²).

The 1/L² (not 1/L) makes the 3D kernel fall off faster with angle
than 2D. This makes the effective beam TIGHTER, which changes the
eikonal prediction.

The potential is 2D: V = s/√((x-x_src)² + (z-z_src)²), ignoring y.
So the deflection in z integrates over the x-z plane, but the wave
spreads in 3D.

Three models computed:
1. Plane-wave eikonal (single ray, no beam averaging) — baseline
2. 3D Gaussian-beam eikonal (integrate over 3D angular weight with 1/L²)
3. Effective 1D eikonal with 3D-tightened beam width

The KEY difference from the 2D beam eikonal: the 1/L² factor makes
the effective angular width NARROWER than 1/√(2β). At β=0.8, the
3D effective beam should be tighter, potentially improving the match.
"""

from __future__ import annotations
import math


def I_geom(b_eff, x_src, L):
    """Single-ray eikonal for 2D potential V=s/r at impact param b_eff."""
    if abs(b_eff) < 0.01:
        return 0.0
    def F(x):
        return (x - x_src) / math.sqrt((x - x_src)**2 + b_eff**2)
    return (1.0 / b_eff) * (F(L) - F(0))


def beam_eikonal_3d(b, x_src, L, beta, n_pts=500):
    """3D beam-averaged eikonal.

    Integrate over ray angles (θ_y, θ_z) with weight:
        w = exp(-β·(θ_y²+θ_z²)) / L(θ)²

    where L(θ) = H/cos(θ), θ = √(θ_y²+θ_z²).
    For the per-layer eikonal, each ray at angle θ_z has effective
    impact parameter b_eff = b - x_src·tan(θ_z).

    Since the potential only depends on z (not y), the θ_y integration
    just provides normalization. The deflection depends only on θ_z:

        <δz> = ∫∫ w(θ_y,θ_z) · I(b - x_src·θ_z) dθ_y dθ_z
             / ∫∫ w(θ_y,θ_z) dθ_y dθ_z

    The θ_y integration of w(θ_y,θ_z) = exp(-β·θ_y²) · exp(-β·θ_z²) / L²
    where L depends on √(θ_y²+θ_z²).

    We must integrate this 2D Gaussian properly, not factor it.
    """
    # Use θ_z-marginal: integrate w over θ_y for each θ_z
    sigma = 1.0 / math.sqrt(2 * beta)
    theta_max = min(4 * sigma, math.pi / 2 - 0.01)
    dtheta = 2 * theta_max / n_pts

    num = 0.0
    den = 0.0

    for iz in range(n_pts):
        tz = -theta_max + (iz + 0.5) * dtheta
        b_eff = b - x_src * math.tan(tz)
        if abs(b_eff) < 0.05:
            continue
        I_ray = I_geom(b_eff, x_src, L)

        # Integrate over θ_y for this θ_z
        w_marginal = 0.0
        for iy in range(n_pts):
            ty = -theta_max + (iy + 0.5) * dtheta
            theta_3d = math.sqrt(ty * ty + tz * tz)
            if theta_3d > math.pi / 2 - 0.01:
                continue
            cos_theta = math.cos(theta_3d)
            # L = H/cos(θ), so 1/L² = cos²(θ)/H²
            # The H² in the kernel numerator cancels, leaving cos²(θ)
            w = math.exp(-beta * (ty * ty + tz * tz)) * cos_theta * cos_theta
            w_marginal += w * dtheta

        num += w_marginal * I_ray * dtheta
        den += w_marginal * dtheta

    if den < 1e-30:
        return float('nan')
    return num / den


def beam_eikonal_3d_fast(b, x_src, L, beta, n_pts=2000):
    """Fast version: compute θ_y-marginal of 3D weight analytically.

    For fixed θ_z, integrate exp(-β·(θ_y²+θ_z²))·cos²(√(θ_y²+θ_z²)) over θ_y.

    Approximation: for small θ, cos²(θ) ≈ 1 - θ². Then:
    ∫ exp(-β·θ_y²) · exp(-β·θ_z²) · (1 - θ_y² - θ_z²) dθ_y
    = exp(-β·θ_z²) · [√(π/β) · (1-θ_z²) - √(π/β)/(2β)]

    But let's just compute the z-marginal numerically for accuracy.
    The integral over θ_y of exp(-β·θ_y²)·cos²(√(θ_y²+θ_z²)) is a
    1D integral we can do with a tight loop.
    """
    sigma = 1.0 / math.sqrt(2 * beta)
    tz_max = min(4 * sigma, math.pi / 2 - 0.01)
    dtz = 2 * tz_max / n_pts

    # Precompute θ_y marginal for a grid of θ_z values
    ty_max = tz_max
    n_ty = 200
    dty = 2 * ty_max / n_ty

    num = 0.0
    den = 0.0

    for iz in range(n_pts):
        tz = -tz_max + (iz + 0.5) * dtz
        b_eff = b - x_src * math.tan(tz)
        if abs(b_eff) < 0.05:
            continue
        I_ray = I_geom(b_eff, x_src, L)

        # θ_y marginal
        w_marg = 0.0
        for iy in range(n_ty):
            ty = -ty_max + (iy + 0.5) * dty
            t3d = math.sqrt(ty * ty + tz * tz)
            if t3d >= math.pi / 2:
                continue
            ct = math.cos(t3d)
            w_marg += math.exp(-beta * (ty * ty + tz * tz)) * ct * ct * dty
        num += w_marg * I_ray * dtz
        den += w_marg * dtz

    if den < 1e-30:
        return float('nan')
    return num / den


def effective_sigma_3d(beta, n_pts=500):
    """Compute effective σ_θz for the z-marginal of the 3D weight.

    The 3D weight w(θ_y,θ_z) = exp(-β(θ_y²+θ_z²)) · cos²(√(θ_y²+θ_z²)).
    Marginalizing over θ_y and fitting the result to a Gaussian in θ_z
    gives the effective 1D width.
    """
    sigma = 1.0 / math.sqrt(2 * beta)
    t_max = min(4 * sigma, math.pi / 2 - 0.01)
    n_ty = 200
    dty = 2 * t_max / n_ty
    dtz = 2 * t_max / n_pts

    # Compute marginal at θ_z=0 and at θ_z=σ
    vals = []
    for iz in range(n_pts):
        tz = (iz + 0.5) * dtz  # positive half only
        w_marg = 0.0
        for iy in range(n_ty):
            ty = -t_max + (iy + 0.5) * dty
            t3d = math.sqrt(ty * ty + tz * tz)
            if t3d >= math.pi / 2:
                continue
            ct = math.cos(t3d)
            w_marg += math.exp(-beta * (ty * ty + tz * tz)) * ct * ct * dty
        vals.append((tz, w_marg))

    # Find where marginal drops to 1/e of peak
    if not vals:
        return sigma
    peak = vals[0][1]
    for tz, w in vals:
        if w < peak / math.e:
            return tz
    return t_max


def power_law_fit(b_vals, I_vals):
    n = len(b_vals)
    log_b = [math.log(b) for b in b_vals]
    log_I = [math.log(abs(I)) for I in I_vals]
    sx, sy = sum(log_b), sum(log_I)
    sxx = sum(x * x for x in log_b)
    sxy = sum(x * y for x, y in zip(log_b, log_I))
    den = n * sxx - sx * sx
    slope = (n * sxy - sx * sy) / den
    intercept = (sy - slope * sx) / n
    pred = [slope * x + intercept for x in log_b]
    ss_res = sum((y - p)**2 for y, p in zip(log_I, pred))
    ss_tot = sum((y - sy / n)**2 for y in log_I)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0
    return slope, math.exp(intercept), r2


def main():
    beta = 0.8
    L = 15.0
    x_src = 5.0

    sigma_pure = 1.0 / math.sqrt(2 * beta)
    sigma_3d = effective_sigma_3d(beta)

    print("=" * 80)
    print("3D-CORRECTED EIKONAL LENSING PREDICTION")
    print(f"  β={beta}, L={L}, x_src={x_src}")
    print(f"  Pure Gaussian σ_θ = {sigma_pure:.3f} rad ({math.degrees(sigma_pure):.1f}°)")
    print(f"  3D effective σ_θz = {sigma_3d:.3f} rad ({math.degrees(sigma_3d):.1f}°)")
    print(f"  3D beam width at source: σ_z = x_src·σ_θz = {x_src*sigma_3d:.3f}")
    print(f"  (2D beam width was: σ_z = x_src·σ_θ = {x_src*sigma_pure:.3f})")
    print("=" * 80)

    b_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]

    # 1. Plane-wave eikonal (no beam)
    plane = [(b, I_geom(b, x_src, L)) for b in b_values]

    # 2. 3D beam-averaged eikonal
    print("\n  Computing 3D beam-averaged eikonal (this takes ~30s)...", flush=True)
    beam_3d = []
    for b in b_values:
        I = beam_eikonal_3d_fast(b, x_src, L, beta)
        beam_3d.append((b, I))
        print(f"    b={b:.0f}: I={I:.6f}", flush=True)

    # 3. Compare
    print(f"\n  {'b':>5s}  {'plane':>12s}  {'3D-beam':>12s}  {'ratio':>8s}")
    print(f"  {'-'*50}")
    for (b, Ip), (_, Ib) in zip(plane, beam_3d):
        ratio = Ib / Ip if abs(Ip) > 1e-30 else float('nan')
        print(f"  {b:5.1f}  {Ip:12.6f}  {Ib:12.6f}  {ratio:8.4f}")

    # 4. Power-law fits on b∈{3..6}
    fit_b = [b for b in b_values if 3 <= b <= 6]
    fit_plane = [I for b, I in plane if 3 <= b <= 6]
    fit_3d = [I for b, I in beam_3d if 3 <= b <= 6]

    sl_p, pf_p, r2_p = power_law_fit(fit_b, fit_plane)
    sl_3d, pf_3d, r2_3d = power_law_fit(fit_b, fit_3d)

    print(f"\n  POWER-LAW FITS on b ∈ {{3..6}}:")
    print(f"    Plane-wave:  I ≈ {pf_p:.4f} · b^({sl_p:.4f})   R²={r2_p:.6f}")
    print(f"    3D-beam:     I ≈ {pf_3d:.4f} · b^({sl_3d:.4f})   R²={r2_3d:.6f}")
    print(f"    LATTICE:     kubo ≈ 28.4 · b^(−1.43)")
    print(f"\n    Plane-wave Δslope = {abs(sl_p - (-1.43)):.4f}")
    print(f"    3D-beam    Δslope = {abs(sl_3d - (-1.43)):.4f}")

    if abs(sl_3d - (-1.43)) < abs(sl_p - (-1.43)):
        print(f"    → 3D beam correction IMPROVES match")
    else:
        print(f"    → 3D beam correction does NOT improve match")

    # 5. L-independence test for 3D beam eikonal
    print(f"\n  L-INDEPENDENCE TEST (3D beam):")
    print(f"  {'L':>6s}  {'x_src':>6s}  {'slope':>8s}  {'R²':>8s}")
    print(f"  {'-'*40}")

    for L_test in [7.5, 15.0, 30.0, 45.0]:
        xs_test = L_test / 3.0
        tb = [3.0, 4.0, 5.0, 6.0]
        tI = [beam_eikonal_3d_fast(b, xs_test, L_test, beta, n_pts=500) for b in tb]
        if any(math.isnan(I) for I in tI):
            print(f"  {L_test:6.1f}  {xs_test:6.2f}  NaN")
            continue
        sl, _, r2 = power_law_fit(tb, tI)
        print(f"  {L_test:6.1f}  {xs_test:6.2f}  {sl:8.4f}  {r2:8.6f}")

    # 6. Verdict
    print(f"\n{'='*80}")
    print("VERDICT")
    print("=" * 80)

    results = {
        "2D beam (previous)": (-0.35, "slope worsened from -1.28"),
        "3D beam (this test)": (sl_3d, ""),
        "plane-wave": (sl_p, "baseline"),
        "lattice": (-1.43, "target"),
    }

    for name, (sl, note) in results.items():
        delta = abs(sl - (-1.43))
        print(f"  {name:25s}  slope = {sl:+.4f}  Δ = {delta:.4f}  {note}")


if __name__ == "__main__":
    main()
