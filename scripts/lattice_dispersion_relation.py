#!/usr/bin/env python3
"""Dispersion relation measurement on the regular lattice propagator.

MOONSHOT TEST: does the propagator produce a recognizable dispersion
relation? The test:

1. On a 2D regular lattice (same geometry as continuum-limit tests),
   initialize a plane-wave source at x=0 with transverse momentum p:
       amp_j = exp(i·p·y_j)  for nodes at layer 0

2. Propagate forward through the lattice.

3. At each downstream layer, extract the phase of the p-mode Fourier
   component: phi(x) = arg( sum_j amp_j · exp(-i·p·y_j) )

4. The phase advance per unit x-distance is the longitudinal frequency:
       omega(p) = d(phi)/dx

5. Sweep p and plot omega(p). Compare to:
   - omega^2 = p^2 + m^2       (relativistic massive / Klein-Gordon)
   - omega = p^2/(2m)           (non-relativistic / Schrödinger)
   - omega = |p|                (massless relativistic / light cone)
   - omega = const + a·p^2      (lattice dispersion / tight-binding)

No slits, no field, no gravity — pure free propagator structure.
The kernel is exp(i·k·act) · w/L with angular weight w = exp(-β·θ²).

If this gives ω² = p² + m², the propagator encodes relativistic physics.
That would be a major structural result.
"""

from __future__ import annotations
import math
import cmath
import numpy as np
import sys
import os
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
PHYS_WIDTH = 20.0
PHYS_LENGTH = 40.0
MAX_DY_PHYS = 5.0


def generate_lattice(spacing):
    """Regular 2D lattice, no slits, no blocking."""
    n_layers = int(PHYS_LENGTH / spacing) + 1
    hw = int(PHYS_WIDTH / spacing)
    max_dy = max(1, int(MAX_DY_PHYS / spacing))

    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(n_layers):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            y = iy * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx

    for layer in range(n_layers - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for dy in range(-max_dy, max_dy + 1):
                iyn = iy + dy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)

    return pos, dict(adj), n_layers, hw, max_dy, nmap


def propagate_planewave(pos, adj, n, spacing, nmap, n_layers, hw, p_transverse):
    """Propagate a plane wave with transverse momentum p.

    Source at layer 0: amp_j = exp(i·p·y_j).
    Returns amplitudes at all nodes.
    """
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n

    # Initialize source layer with plane wave
    for iy in range(-hw, hw + 1):
        idx = nmap.get((0, iy))
        if idx is not None:
            y = iy * spacing
            amps[idx] = cmath.exp(1j * p_transverse * y)

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            # Free propagator (no field)
            act = L
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * K * act) * w / L * spacing * spacing
            amps[j] += amps[i] * ea
    return amps


def extract_mode_phase(amps, nmap, hw, spacing, layer, p_transverse):
    """Extract the phase and amplitude of the p-mode at a given layer.

    Project amplitudes onto exp(-i·p·y) to get the Fourier component.
    """
    mode_amp = 0j
    for iy in range(-hw, hw + 1):
        idx = nmap.get((layer, iy))
        if idx is None:
            continue
        y = iy * spacing
        mode_amp += amps[idx] * cmath.exp(-1j * p_transverse * y)
    return mode_amp


def measure_dispersion(spacing, p_values):
    """Measure omega(p) for a list of transverse momenta."""
    pos, adj, n_layers, hw, max_dy, nmap = generate_lattice(spacing)
    n = len(pos)

    results = []
    for p in p_values:
        amps = propagate_planewave(pos, adj, n, spacing, nmap, n_layers, hw, p)

        # Extract mode phase at several layers in the middle third
        # (avoid edges where boundary effects might dominate)
        start_layer = n_layers // 4
        end_layer = 3 * n_layers // 4
        step = max(1, (end_layer - start_layer) // 10)
        layers = list(range(start_layer, end_layer, step))

        phases = []
        mode_amps = []
        xs = []
        for layer in layers:
            ma = extract_mode_phase(amps, nmap, hw, spacing, layer, p)
            if abs(ma) < 1e-30:
                continue
            phases.append(cmath.phase(ma))
            mode_amps.append(abs(ma))
            xs.append(layer * spacing)

        if len(phases) < 3:
            results.append((p, float('nan'), float('nan'), float('nan')))
            continue

        # Unwrap phases
        phases = np.array(phases)
        xs = np.array(xs)
        phases_unwrapped = np.unwrap(phases)

        # Linear fit: phi = omega * x + const
        # omega = slope of unwrapped phase vs x
        coeffs = np.polyfit(xs, phases_unwrapped, 1)
        omega = coeffs[0]

        # Quality: R² of the linear fit
        predicted = np.polyval(coeffs, xs)
        ss_res = np.sum((phases_unwrapped - predicted) ** 2)
        ss_tot = np.sum((phases_unwrapped - np.mean(phases_unwrapped)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        # Mean mode amplitude (signal strength)
        mean_amp = np.mean(mode_amps)

        results.append((p, omega, r2, mean_amp))

    return results


def fit_dispersion(p_vals, omega_vals):
    """Try fitting omega(p) to various functional forms."""
    p = np.array(p_vals)
    w = np.array(omega_vals)

    fits = {}

    # 1. Relativistic massive: omega² = p² + m²
    # => omega = sqrt(p² + m²) × sign
    # Linearize: omega² = p² + m²
    w2 = w ** 2
    try:
        # omega² = a·p² + b => a should be 1 (or c²), b = m²
        coeffs = np.polyfit(p ** 2, w2, 1)
        a, b = coeffs
        predicted = a * p ** 2 + b
        ss_res = np.sum((w2 - predicted) ** 2)
        ss_tot = np.sum((w2 - np.mean(w2)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
        fits["omega²=a·p²+m²"] = {"a": a, "m²": b, "R²": r2}
    except Exception:
        pass

    # 2. Non-relativistic: omega = a·p² + b
    try:
        coeffs = np.polyfit(p ** 2, w, 1)
        a, b = coeffs
        predicted = a * p ** 2 + b
        ss_res = np.sum((w - predicted) ** 2)
        ss_tot = np.sum((w - np.mean(w)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
        fits["omega=a·p²+b"] = {"a": a, "b": b, "R²": r2}
    except Exception:
        pass

    # 3. Linear (massless): omega = c·|p| + d
    try:
        coeffs = np.polyfit(np.abs(p), w, 1)
        c_val, d = coeffs
        predicted = c_val * np.abs(p) + d
        ss_res = np.sum((w - predicted) ** 2)
        ss_tot = np.sum((w - np.mean(w)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
        fits["omega=c·|p|+d"] = {"c": c_val, "d": d, "R²": r2}
    except Exception:
        pass

    # 4. Power law: omega - omega0 ∝ |p|^alpha
    try:
        # Use omega(p) - omega(0) and fit log-log
        w0 = w[np.argmin(np.abs(p))]  # omega at p closest to 0
        mask = np.abs(p) > 0.05
        if mask.sum() >= 3:
            log_p = np.log(np.abs(p[mask]))
            dw = w[mask] - w0
            # Only fit if all dw have the same sign
            if np.all(dw > 0) or np.all(dw < 0):
                log_dw = np.log(np.abs(dw))
                coeffs = np.polyfit(log_p, log_dw, 1)
                alpha = coeffs[0]
                predicted = np.polyval(coeffs, log_p)
                ss_res = np.sum((log_dw - predicted) ** 2)
                ss_tot = np.sum((log_dw - np.mean(log_dw)) ** 2)
                r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
                fits["power_law_alpha"] = {"alpha": alpha, "omega0": w0, "R²": r2}
    except Exception:
        pass

    return fits


def main():
    print("=" * 90)
    print("DISPERSION RELATION: omega(p) ON THE FREE LATTICE PROPAGATOR")
    print(f"  Physical extent: W={PHYS_WIDTH}, L={PHYS_LENGTH}")
    print(f"  K={K}, beta={BETA}")
    print(f"  Kernel: exp(i·K·L) · exp(-beta·theta²) / L · h²")
    print("=" * 90)
    print()

    # Test at two spacings to check lattice artifacts
    spacings = [1.0, 0.5]

    # Transverse momenta: from 0 to ~pi/h (lattice Nyquist)
    # Use physical momenta that are well below Nyquist at both spacings
    p_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0]

    for sp in spacings:
        nyquist = math.pi / sp
        print(f"\n{'='*70}")
        print(f"  SPACING h={sp}, Nyquist p_max = pi/h = {nyquist:.2f}")
        print(f"{'='*70}")

        # Only use p values below Nyquist/2
        valid_p = [p for p in p_values if p < nyquist / 2]

        t0 = time.time()
        results = measure_dispersion(sp, valid_p)
        dt = time.time() - t0

        print(f"\n  {'p':>6s}  {'omega':>10s}  {'R²':>8s}  {'|mode|':>10s}")
        print(f"  {'-'*45}")

        good_p = []
        good_omega = []
        for p, omega, r2, amp in results:
            flag = ""
            if r2 < 0.99:
                flag = "  ← noisy"
            if math.isnan(omega):
                flag = "  ← FAIL"
            print(f"  {p:6.2f}  {omega:+10.4f}  {r2:8.5f}  {amp:10.2e}{flag}")
            if r2 >= 0.99 and not math.isnan(omega):
                good_p.append(p)
                good_omega.append(omega)

        print(f"\n  Time: {dt:.1f}s")

        if len(good_p) >= 4:
            print(f"\n  FITTING omega(p) to candidate dispersion relations:")
            print(f"  {'-'*60}")

            fits = fit_dispersion(np.array(good_p), np.array(good_omega))
            for name, params in sorted(fits.items(), key=lambda x: -x[1].get("R²", 0)):
                r2 = params.pop("R²", 0)
                param_str = ", ".join(f"{k}={v:.6f}" for k, v in params.items())
                verdict = "GOOD" if r2 > 0.999 else ("OK" if r2 > 0.99 else "POOR")
                print(f"    {name:25s}  R²={r2:.6f} [{verdict}]  {param_str}")

            # Key test: omega² vs p²
            print(f"\n  RAW DATA for omega² vs p²:")
            print(f"  {'p²':>8s}  {'omega²':>12s}  {'omega':>10s}")
            for p, w in zip(good_p, good_omega):
                print(f"  {p**2:8.4f}  {w**2:12.4f}  {w:+10.4f}")

    print(f"\n{'='*90}")
    print("INTERPRETATION GUIDE")
    print("="*90)
    print("""
  If omega²=a·p²+m² fits with R²>0.999 and a≈1:
    → RELATIVISTIC (Klein-Gordon) dispersion.
    → The propagator encodes a massive relativistic particle.
    → m² gives the effective mass.
    → This would be a MAJOR structural result.

  If omega=a·p²+b fits with R²>0.999:
    → NON-RELATIVISTIC (Schrödinger) dispersion.
    → The propagator encodes a non-relativistic particle.
    → a = 1/(2m_eff) gives effective mass.
    → Still interesting but less surprising for a lattice model.

  If omega=c·|p|+d fits with R²>0.999:
    → MASSLESS RELATIVISTIC (light cone) dispersion.
    → c is the effective speed of light.

  If power_law_alpha ≈ 2: non-relativistic.
  If power_law_alpha ≈ 1: linear/massless.
  If it's something else: novel.
""")


if __name__ == "__main__":
    main()
