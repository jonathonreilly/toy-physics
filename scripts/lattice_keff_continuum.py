#!/usr/bin/env python3
"""Continuum limit via k_eff = k*h coupling renormalization (Approach 2).

This is the remaining open scheme from the dense continuum-limit plan after:
  - Approach 1 (nearest-neighbor only): retained through h=0.25, runtime-blocked finer
  - Approach 3 (fan-out normalization): falsified

The dense baseline `lattice_continuum_limit.py` keeps the phase coupling `k`
fixed while compensating amplitude growth with a `spacing^2` kernel factor.
Approach 2 instead asks whether shrinking the coupling with spacing,

    k_eff = k * h

stabilizes the refinement trend while preserving the rest of the dense kernel.

This wrapper reuses the exact baseline lattice generator and measurement stack,
changing only the propagator:

    ea = exp(i * (k*h) * act) * w / L * h^2

This keeps the comparison to the retained dense baseline as tight as possible.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lattice_continuum_limit as lc


def propagate_keff(pos, adj, field, k, blocked, n):
    """Baseline propagator with k_eff = k * spacing."""
    x0 = pos[0][0] if pos else 0.0
    spacing = next((x - x0 for x, _ in pos if x > x0 + 1e-12), 1.0)
    k_eff = k * spacing
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-lc.BETA * theta * theta)
            ea = cmath.exp(1j * k_eff * act) * w / L * spacing * spacing
            amps[j] += amps[i] * ea
    return amps


def detector_diagnostics(spacing):
    """Return coarse diagnostics when the baseline measure stack fails."""
    pos, adj, nl, hw, max_dy, bl, gl, nmap = lc.generate_lattice(
        spacing, lc.PHYS_WIDTH, lc.PHYS_LENGTH, lc.MAX_DY_PHYS
    )
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]

    slit_iy = max(1, round(lc.SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa = [
        nmap[(bl, iy)]
        for iy in range(slit_iy, min(slit_iy + max(2, round(2 / spacing)), hw + 1))
        if (bl, iy) in nmap
    ]
    sb = [
        nmap[(bl, iy)]
        for iy in range(-min(slit_iy + max(1, round(1 / spacing)), hw), -slit_iy + 1)
        if (bl, iy) in nmap
    ]
    blocked = set(bi) - set(sa + sb)

    field_f = [0.0] * n
    phys_strength = 0.0005 * spacing
    field_m, _ = lc.make_field(pos, nmap, gl, lc.MASS_Y, spacing, hw, phys_strength)

    af = propagate_keff(pos, adj, field_f, lc.K, blocked, n)
    am = propagate_keff(pos, adj, field_m, lc.K, blocked, n)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    maxaf = max(abs(a) for a in af)
    maxam = max(abs(a) for a in am)
    return {
        "n_nodes": n,
        "nodes_per_layer": 2 * hw + 1,
        "pf": pf,
        "pm": pm,
        "maxaf": maxaf,
        "maxam": maxam,
    }


def main():
    print("=" * 100)
    print("K_EFF = K*H CONTINUUM LIMIT (Approach 2)")
    print(f"  Physical extent: W={lc.PHYS_WIDTH}, L={lc.PHYS_LENGTH}, mass at y={lc.MASS_Y}")
    print("  Kernel: exp(i * (k*h) * act) * w / L * h^2")
    print("  Measurement stack: identical to lattice_continuum_limit.py")
    print("=" * 100)
    print()

    old_propagate = lc.propagate
    lc.propagate = propagate_keff
    try:
        spacings = [2.0, 1.0, 0.5, 0.25]
        print(
            f"  {'h':>6s}  {'n_nodes':>8s}  {'npl':>5s}  {'gravity':>11s}  {'k=0':>10s}  "
            f"{'MI':>7s}  {'1-pur':>7s}  {'d_TV':>7s}  {'t':>5s}"
        )
        print(f"  {'-' * 97}")

        results = []
        for sp in spacings:
            t0 = time.time()
            try:
                r = lc.measure_all(sp)
            except (OverflowError, MemoryError) as e:
                print(f"  {sp:6.3f}  FAIL ({type(e).__name__})  {time.time()-t0:4.0f}s")
                continue
            dt = time.time() - t0
            if r:
                results.append(r)
                print(
                    f"  {sp:6.3f}  {r['n_nodes']:8d}  {r['nodes_per_layer']:5d}  "
                    f"{r['gravity']:+11.6f}  {r['gk0']:+10.2e}  "
                    f"{r['MI']:7.4f}  {1.0-r['pur_cl']:7.4f}  {r['dtv']:7.4f}  {dt:4.0f}s",
                    flush=True,
                )
            else:
                d = detector_diagnostics(sp)
                print(
                    f"  {sp:6.3f}  {d['n_nodes']:8d}  {d['nodes_per_layer']:5d}  "
                    f"{'FAIL':>11s}  {'—':>10s}  {'—':>7s}  {'—':>7s}  {'—':>7s}  {dt:4.0f}s",
                    flush=True,
                )
                print(
                    f"           detector probs: free={d['pf']:.2e}  mass={d['pm']:.2e}  "
                    f"max|A| free={d['maxaf']:.2e}  max|A| mass={d['maxam']:.2e}",
                    flush=True,
                )

        print()
        print("=" * 100)
        print("VERDICT")
        print("=" * 100)
        if len(results) < 2:
            print("  Insufficient data to judge convergence.")
            return

        gravs = [r["gravity"] for r in results]
        mis = [r["MI"] for r in results]
        dtvs = [r["dtv"] for r in results]
        one_minus_purs = [1.0 - r["pur_cl"] for r in results]
        print(f"  Gravity values: {['%+.4f' % g for g in gravs]}")
        if all(g > 0 for g in gravs[-2:]):
            print("    sign stable (attractive in last two refinements)")
        elif all(g < 0 for g in gravs[-2:]):
            print("    sign stable (repulsive in last two refinements)")
        else:
            print("    sign NOT stable across refinements")

        print(f"  MI values:  {['%.4f' % m for m in mis]}")
        print(f"  1-pur values:{['%.4f' % p for p in one_minus_purs]}")
        print(f"  d_TV values:{['%.4f' % d for d in dtvs]}")

        if len(results) >= 3:
            g_deltas = [abs(gravs[i + 1] - gravs[i]) for i in range(len(gravs) - 1)]
            print(f"  Gravity step deltas: {['%.4f' % d for d in g_deltas]}")
            if g_deltas[-1] < g_deltas[0] * 0.5:
                print("    -> gravity appears to be CONVERGING")
            elif g_deltas[-1] > g_deltas[0] * 2:
                print("    -> gravity appears to be DIVERGING")
            else:
                print("    -> gravity deltas roughly constant (slow/no convergence)")
    finally:
        lc.propagate = old_propagate


if __name__ == "__main__":
    main()
