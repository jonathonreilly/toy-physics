#!/usr/bin/env python3
"""Non-relativistic Born scattering prediction for the Kubo deflection.

Given that the propagator is Schrödinger-type (dispersion ω = a·p² + b),
the correct theoretical prediction for kubo_true(b) is the first-order
Born approximation for scattering of a non-relativistic particle off a
2D 1/r potential.

The setup matches the lattice measurement:
- 2D (x longitudinal, y transverse)
- Free propagator: Gaussian angular weight → Schrödinger dispersion
- Potential: V(x,y) = s / sqrt((x-x_src)² + (y-y_src)²)
- Source at x=0, y=0; detector at x=L
- Mass at x=x_src, y=b (impact parameter)
- Kubo = d<y_det>/ds at s=0

The Born approximation for the centroid deflection of a wave packet
passing a 2D potential at impact parameter b:

In the eikonal (WKB) limit of non-relativistic QM:
  δy = ∫ ∂V/∂y dt / p_x

For our 1/r potential in 2D:
  V = s/r, ∂V/∂y = -s·(y-b)/r³

The integral along the unperturbed straight path (x=0→L, y=0):
  δy = (s/p_x) · ∫₀ᴸ -(-b) / ((x-x_src)² + b²)^(3/2) dx

This is a known integral. For a source at x_src with path from 0 to L:

  I = ∫₀ᴸ b / ((x-x_src)² + b²)^(3/2) dx
    = [-(x-x_src) / (b² · sqrt((x-x_src)² + b²))]₀ᴸ

Let's compute this numerically and compare to the lattice measurement.
"""

from __future__ import annotations
import math


def eikonal_deflection(b, x_src, L, s=1.0):
    """Eikonal (WKB) centroid deflection in 2D non-relativistic QM.

    Unperturbed path: straight from (0,0) to (L,0).
    Potential source at (x_src, b).
    V = s/r where r = sqrt((x-x_src)² + (y-b)²).

    Along the unperturbed path (y=0):
      dV/dy = -s·(0-b) / r³ = s·b / ((x-x_src)² + b²)^(3/2)

    Deflection = (1/p_x) · ∫₀ᴸ (dV/dy) dx

    The integral:
      I = b · ∫₀ᴸ dx / ((x-x_src)² + b²)^(3/2)
        = (1/b) · [(x-x_src) / sqrt((x-x_src)² + b²)]₀ᴸ
    """
    def F(x):
        return (x - x_src) / math.sqrt((x - x_src) ** 2 + b ** 2)

    I_geom = (1.0 / b) * (F(L) - F(0))
    # kubo_true = d<y>/ds, so we return s * I_geom / p_x
    # For the lattice, the propagator's p_x is related to k and the
    # dispersion, but the SHAPE (b-dependence) of I_geom is the prediction.
    # I_geom = geometric factor with units 1/length
    return s * I_geom


def main():
    # Match the lattice setup from kubo_continuum_limit.py
    # T_phys = 15.0, mass at x_src = NL//3 * H ≈ T_phys/3 = 5.0
    # PW_phys = 6.0, mass at z_src = b (impact parameter)
    # But the lattice field uses f = s/(r + eps) with r = sqrt((x-x_src)² + (z-z_src)²)
    # and z_src = b, y ignored (2D slice)

    L = 15.0  # T_phys
    x_src = 5.0  # T_phys / 3

    print("=" * 70)
    print("2D NON-RELATIVISTIC BORN/EIKONAL PREDICTION FOR kubo(b)")
    print(f"  L={L}, x_src={x_src}")
    print("=" * 70)
    print()

    b_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    print(f"  {'b':>4s}  {'I_geom':>12s}  {'log(I)':>10s}")
    print(f"  {'-'*35}")

    geom_vals = []
    for b in b_values:
        I = eikonal_deflection(b, x_src, L, s=1.0)
        log_I = math.log(abs(I)) if abs(I) > 1e-30 else float('nan')
        print(f"  {b:4.1f}  {I:12.6f}  {log_I:10.4f}")
        geom_vals.append((b, I))

    # Fit power law on b ∈ {3..6} to match the lattice measurement range
    print(f"\n  Power-law fit on b ∈ {{3..6}} (matching lattice range):")
    fit_data = [(b, I) for b, I in geom_vals if 3 <= b <= 6]
    if len(fit_data) >= 2:
        log_b = [math.log(b) for b, _ in fit_data]
        log_I = [math.log(abs(I)) for _, I in fit_data]
        n = len(fit_data)
        sx = sum(log_b)
        sy = sum(log_I)
        sxx = sum(x * x for x in log_b)
        sxy = sum(x * y for x, y in zip(log_b, log_I))
        denom = n * sxx - sx * sx
        slope = (n * sxy - sx * sy) / denom
        intercept = (sy - slope * sx) / n
        prefactor = math.exp(intercept)

        # R²
        pred = [slope * x + intercept for x in log_b]
        ss_res = sum((y - p) ** 2 for y, p in zip(log_I, pred))
        ss_tot = sum((y - sy / n) ** 2 for y in log_I)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0

        print(f"    I_geom(b) ≈ {prefactor:.4f} · b^({slope:.4f})")
        print(f"    R² = {r2:.6f}")

        print(f"\n  COMPARISON WITH LATTICE MEASUREMENT:")
        print(f"    Lattice:    kubo(b) ≈ 28.4 · b^(−1.43)")
        print(f"    Born/eik:   I_geom(b) ≈ {prefactor:.4f} · b^({slope:.4f})")
        print(f"    Slope match? lattice = −1.43, theory = {slope:.4f}")

        if abs(slope - (-1.43)) < 0.1:
            print(f"    → SLOPES MATCH within 0.1 !")
        elif abs(slope - (-1.43)) < 0.2:
            print(f"    → Slopes are CLOSE (Δ = {abs(slope - (-1.43)):.3f})")
        else:
            print(f"    → Slopes DIFFER by {abs(slope - (-1.43)):.3f}")

    # Also compute the FULL analytical formula for all b
    print(f"\n  ANALYTICAL FORM:")
    print(f"  For path from x=0 to x=L with source at x_src:")
    print(f"    I_geom(b) = (1/b) · [(L-x_src)/sqrt((L-x_src)²+b²) + x_src/sqrt(x_src²+b²)]")
    print(f"  In the limits:")
    print(f"    L>>b (long path): I → 2/b  (slope = −1)")
    print(f"    L<<b (wide miss):  I → L·x_src·(L-x_src)/(b³·...) → 1/b³ (slope = −3)")
    print(f"    L≈b (transition):  slope intermediate")

    # Compute effective slope at each b
    print(f"\n  LOCAL SLOPE d(log I)/d(log b):")
    for i in range(len(geom_vals) - 1):
        b1, I1 = geom_vals[i]
        b2, I2 = geom_vals[i + 1]
        local_slope = (math.log(abs(I2)) - math.log(abs(I1))) / (math.log(b2) - math.log(b1))
        print(f"    b={b1:.0f}→{b2:.0f}: slope = {local_slope:.4f}")


if __name__ == "__main__":
    main()
