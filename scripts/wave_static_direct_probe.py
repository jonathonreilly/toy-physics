#!/usr/bin/env python3
"""Direct discrete static-comparator probe for the wave-retardation lane.

This script tests the next concrete comparator candidate after the corrected
continuum negative:

  solve the exact static fixed-point / Poisson problem on the same finite
  (y, z) field grid and use that as the c=infinity comparator.

The probe is intentionally narrow:
  - same physical setup as wave_retardation_continuum_limit.py
  - same beam DAG / propagator
  - compare three static comparators:
      dI    = cached static slice at NL_dyn
      dIeq  = cached static slice at 3 * NL_dyn
      dS    = direct discrete static solve on the finite (y, z) grid

If dS is materially more stable than dIeq under H refinement, the exact
discrete static comparator route is promising. If not, the comparator route is
probably closing and the flagship should shift toward direct dM observables.

Default H ladder is H = {0.5, 0.35, 0.25} so the cache always includes the
quoted fine point H = 0.25 that docs/WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md
uses. The fine point dominates wall-clock (~4 minutes on the current
workstation, ~5-6 minutes for the full sweep); AUDIT_TIMEOUT_SEC is declared
below so the precompute orchestrator allows it to complete.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

# Heavy compute: the fine point H=0.25 alone takes ~4 minutes wall-clock
# (NL=60 layers, 41x41 static Poisson solve with up to 20k SOR sweeps per
# distinct source z). Full default sweep H={0.5,0.35,0.25} fits inside the
# declared budget; default 120s would time out.
AUDIT_TIMEOUT_SEC = 600

from wave_retardation_continuum_limit import (
    BETA,
    IZ_END_PHYS,
    IZ_START_PHYS,
    K_PER_H,
    PW_PHYS,
    S_PHYS,
    SRC_LAYER_FRAC,
    T_PHYS_LAYERS,
    cz,
    grow,
    make_instantaneous,
    make_instantaneous_equilibrated,
    prop_beam,
    solve_wave,
)


def solve_static_poisson(PW: float, H: float, strength: float, iz_now: int,
                         tol: float = 1e-10, max_iter: int = 20000):
    """Solve lap(f) + src = 0 on the finite (y, z) grid with zero boundaries."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = nw // 2
    sz = nw // 2 + iz_now
    f = [[0.0] * nw for _ in range(nw)]
    for _ in range(max_iter):
        max_delta = 0.0
        for iy in range(1, nw - 1):
            row = f[iy]
            up = f[iy - 1]
            dn = f[iy + 1]
            for iz in range(1, nw - 1):
                src = strength if (iy == sy and iz == sz) else 0.0
                new = 0.25 * (up[iz] + dn[iz] + row[iz - 1] + row[iz + 1] + src)
                delta = abs(new - row[iz])
                if delta > max_delta:
                    max_delta = delta
                row[iz] = new
        if max_delta < tol:
            break

    max_resid = 0.0
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            src = strength if (iy == sy and iz == sz) else 0.0
            resid = (
                f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1]
                - 4.0 * f[iy][iz] + src
            )
            if abs(resid) > max_resid:
                max_resid = abs(resid)
    return [r[:] for r in f], max_resid


def make_direct_static(NL, PW, H, strength, iz_of_t, src_layer):
    """Exact discrete static comparator via direct Poisson solve per source z."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    cache = {}
    residuals = {}
    for t in range(NL):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            cache[iz_now], residuals[iz_now] = solve_static_poisson(PW, H, strength, iz_now)
        history[t] = [row[:] for row in cache[iz_now]]
    worst_resid = max(residuals.values()) if residuals else 0.0
    return history, worst_resid


def measure_at_H(H_val: float, label: str):
    NL = round(T_PHYS_LAYERS / H_val)
    PW = round(PW_PHYS / H_val) * H_val
    k_phase = K_PER_H / H_val
    src_layer = round(SRC_LAYER_FRAC * NL)
    n_active = NL - src_layer
    if n_active < 2:
        return None

    iz_start = round(IZ_START_PHYS / H_val)
    iz_end = round(IZ_END_PHYS / H_val)
    v_per_layer = (iz_end - iz_start) / n_active
    iz_of_t = lambda t, sl=src_layer, vpl=v_per_layer, izs=iz_start: izs + int(round(vpl * (t - sl)))

    h_M = solve_wave(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_I = make_instantaneous(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_Ieq = make_instantaneous_equilibrated(
        NL, PW, H_val, S_PHYS, iz_of_t, src_layer, equilib_multiplier=3
    )
    h_S, worst_resid = make_direct_static(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_I = cz(prop_beam(pos, adj, nmap, h_I, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_Ieq = cz(prop_beam(pos, adj, nmap, h_Ieq, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_S = cz(prop_beam(pos, adj, nmap, h_S, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    dM = cz_M - z_free
    dI = cz_I - z_free
    dIeq = cz_Ieq - z_free
    dS = cz_S - z_free
    rel_MI = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
    rel_MIeq = abs(dM - dIeq) / max(abs(dM), abs(dIeq), 1e-12)
    rel_MS = abs(dM - dS) / max(abs(dM), abs(dS), 1e-12)
    rel_IeqS = abs(dIeq - dS) / max(abs(dIeq), abs(dS), 1e-12)
    return {
        "label": label,
        "H": H_val,
        "NL": NL,
        "dM": dM,
        "dI": dI,
        "dIeq": dIeq,
        "dS": dS,
        "rel_MI": rel_MI,
        "rel_MIeq": rel_MIeq,
        "rel_MS": rel_MS,
        "rel_IeqS": rel_IeqS,
        "worst_resid": worst_resid,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35, 0.25],
        help=(
            "H values to run. Default ladder 0.5 0.35 0.25 covers the "
            "coarse, medium, and quoted fine points; the fine point H=0.25 reproduces "
            "the negative quoted in docs/WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md."
        ),
    )
    args = parser.parse_args()

    print("=" * 100)
    print("WAVE STATIC DIRECT-COMPARATOR PROBE")
    print("=" * 100)
    rows = []
    label_map = {0.5: "coarse", 0.35: "medium", 0.25: "fine"}
    for idx, H_val in enumerate(args.hs):
        label = label_map.get(H_val, f"run{idx+1}")
        r = measure_at_H(H_val, label)
        rows.append(r)
        print(f"\n[{label}] H={H_val}")
        print(f"  NL={r['NL']}")
        print(f"  dM   = {r['dM']:+.6f}")
        print(f"  dI   = {r['dI']:+.6f}")
        print(f"  dIeq = {r['dIeq']:+.6f}")
        print(f"  dS   = {r['dS']:+.6f}  (direct static solve)")
        print(f"  rel_MI   = {r['rel_MI']:.2%}")
        print(f"  rel_MIeq = {r['rel_MIeq']:.2%}")
        print(f"  rel_MS   = {r['rel_MS']:.2%}")
        print(f"  rel_IeqS = {r['rel_IeqS']:.2%}")
        print(f"  worst static residual = {r['worst_resid']:.3e}")

    if len(rows) >= 2:
        print("\n" + "=" * 100)
        print("LAST-STEP STABILITY")
        print("=" * 100)
        a, b = rows[-2], rows[-1]
        print(f"  Δ(rel_MI)   = {abs(b['rel_MI'] - a['rel_MI']):.4f}")
        print(f"  Δ(rel_MIeq) = {abs(b['rel_MIeq'] - a['rel_MIeq']):.4f}")
        print(f"  Δ(rel_MS)   = {abs(b['rel_MS'] - a['rel_MS']):.4f}")
        print(f"  Δ(rel_IeqS) = {abs(b['rel_IeqS'] - a['rel_IeqS']):.4f}")


if __name__ == "__main__":
    main()
