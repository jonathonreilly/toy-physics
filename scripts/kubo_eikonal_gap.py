#!/usr/bin/env python3
"""Measure the Kubo-eikonal gap as a function of h.

The plane-wave eikonal gives slope -1.28 on b∈{3..6} (h-independent).
The lattice Kubo gives -1.31 at h=0.5, -1.43 at h=0.25.
The gap grows: Δ=0.03 (h=0.5) → Δ=0.15 (h=0.25).

This script measures the Kubo slope on the 2D regular lattice at
multiple h values to trace the gap precisely and see if it converges
to a finite value or keeps growing as h→0.

If the gap converges → there's a finite wave-mechanical correction
If the gap diverges → the eikonal is the wrong baseline
If the gap closes → the lattice approaches the eikonal at fine h

Uses the same kernel as lattice_continuum_limit.py (2D, spacing² measure).
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
PHYS_WIDTH = 20.0
PHYS_LENGTH = 40.0
MAX_DY_PHYS = 5.0
MASS_X_FRAC = 1.0 / 3.0  # mass at 1/3 of the way


def generate_lattice(spacing):
    n_layers = int(PHYS_LENGTH / spacing) + 1
    hw = int(PHYS_WIDTH / spacing)
    max_dy = max(1, int(MAX_DY_PHYS / spacing))
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(n_layers):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            idx = len(pos)
            pos.append((x, iy * spacing))
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


def kubo_2d(pos, adj, n_layers, hw, spacing, b):
    """True Kubo on 2D lattice: d<y>/ds at s=0.

    Field: f = s / (r + 0.1) with r = distance from mass.
    Mass at (x_src, b) where x_src = PHYS_LENGTH * MASS_X_FRAC.
    """
    n = len(pos)
    x_src = PHYS_LENGTH * MASS_X_FRAC
    # Find closest layer
    src_layer = round(x_src / spacing)
    x_src_actual = src_layer * spacing

    A = [0j] * n  # free amp
    B = [0j] * n  # d(amp)/ds
    # Source at origin
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    A[src] = 1.0

    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = spacing * spacing

    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            # Midpoint field
            mx = 0.5 * (x1 + x2)
            my = 0.5 * (y1 + y2)
            r_field = math.sqrt((mx - x_src_actual) ** 2 + (my - b) ** 2) + 0.1

            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            phase = K * L
            phi = complex(math.cos(phase), math.sin(phase))
            w_eff = w * h2 / L  # 2D: h²/L (not h²/L²)

            # d(phase)/ds = -K * L / r_field  (since act ≈ L*(1+f), dact/ds = L/r)
            dphi_ds = complex(0.0, -K * L / r_field) * phi

            A[j] += ai * phi * w_eff
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    # Detector: last layer
    det = [i for i, (x, y) in enumerate(pos) if abs(x - (n_layers - 1) * spacing) < 1e-10]
    weights = [abs(A[d]) ** 2 for d in det]
    ys = [pos[d][1] for d in det]
    T0 = sum(weights)
    if T0 <= 0:
        return float('nan')
    cz_free = sum(w * y for w, y in zip(weights, ys)) / T0
    dT_ds = sum(2.0 * (A[d].conjugate() * B[d]).real for d in det)
    dN_ds = sum(2.0 * (A[d].conjugate() * B[d]).real * pos[d][1] for d in det)
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo


def eikonal_prediction(b, x_src, L):
    """Plane-wave eikonal geometric factor."""
    if abs(b) < 0.01:
        return 0.0
    def F(x):
        return (x - x_src) / math.sqrt((x - x_src) ** 2 + b ** 2)
    return (1.0 / b) * (F(L) - F(0))


def power_law_fit(bs, ks):
    n = len(bs)
    log_b = [math.log(b) for b in bs]
    log_k = [math.log(abs(k)) for k in ks]
    sx, sy = sum(log_b), sum(log_k)
    sxx = sum(x * x for x in log_b)
    sxy = sum(x * y for x, y in zip(log_b, log_k))
    den = n * sxx - sx * sx
    slope = (n * sxy - sx * sy) / den
    pred = [slope * x + (sy - slope * sx) / n for x in log_b]
    ss_res = sum((y - p) ** 2 for y, p in zip(log_k, pred))
    ss_tot = sum((y - sy / n) ** 2 for y in log_k)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0
    return slope, r2


def main():
    b_values = [3.0, 4.0, 5.0, 6.0]
    spacings = [1.0, 0.5, 0.25]
    x_src = PHYS_LENGTH * MASS_X_FRAC

    # Eikonal baseline
    eik = [eikonal_prediction(b, x_src, PHYS_LENGTH) for b in b_values]
    eik_slope, eik_r2 = power_law_fit(b_values, eik)

    print("=" * 80)
    print("KUBO-EIKONAL GAP vs SPACING")
    print(f"  L={PHYS_LENGTH}, x_src={x_src:.1f}, K={K}, β={BETA}")
    print(f"  Eikonal slope: {eik_slope:.4f} (R²={eik_r2:.6f})")
    print("=" * 80)

    print(f"\n  Eikonal baseline:")
    for b, I in zip(b_values, eik):
        print(f"    b={b:.0f}: I_eik = {I:.6f}")

    for sp in spacings:
        print(f"\n{'─'*60}")
        print(f"  h = {sp}")
        print(f"{'─'*60}")

        t0 = time.time()
        pos, adj, nl, hw, md, nmap = generate_lattice(sp)
        n = len(pos)
        dt_gen = time.time() - t0
        print(f"  nodes={n}, layers={nl}, gen={dt_gen:.1f}s")

        kubos = []
        for b in b_values:
            t1 = time.time()
            k = kubo_2d(pos, adj, nl, hw, sp, b)
            dt = time.time() - t1
            kubos.append(k)
            print(f"    b={b:.0f}: kubo={k:+.6f}  ({dt:.1f}s)")

        if all(not math.isnan(k) and k > 0 for k in kubos):
            slope, r2 = power_law_fit(b_values, kubos)
            gap = slope - eik_slope
            print(f"\n    Slope: {slope:.4f} (R²={r2:.6f})")
            print(f"    Eikonal: {eik_slope:.4f}")
            print(f"    Gap: {gap:+.4f}")
        elif all(not math.isnan(k) for k in kubos):
            # Mixed signs
            print(f"\n    Mixed sign kubos: {['+' if k>0 else '-' for k in kubos]}")
        else:
            print(f"\n    NaN in kubos — measurement failed")

    print(f"\n{'='*80}")
    print("INTERPRETATION")
    print("=" * 80)
    print("  If gap grows: wave correction strengthens under refinement")
    print("  If gap converges: finite wave-mechanical correction to eikonal")
    print("  If gap closes: lattice approaches eikonal at fine h")


if __name__ == "__main__":
    main()
