#!/usr/bin/env python3
"""Frozen-source comparator probe for the wave-retardation lane.

This script isolates the comparator question from the moving-source sweep:

  For one or two fixed source positions, compare the retarded wave-field
  response dM against four static comparators on the same finite (y, z)
  lattice:

    dI    = cached static slice at NL_dyn
    dIeq  = cached static slice at 3 * NL_dyn
    dN    = imposed Newton-style 1/r field at the same frozen source position
    dS    = direct discrete static solve on the finite (y, z) grid

The point is to test whether the mismatch seen in the moving-source lane
is already present when the source is frozen in place. If it is, the
problem is comparator construction rather than source motion.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from wave_retardation_continuum_limit import (
    K_PER_H,
    PW_PHYS,
    S_PHYS,
    SRC_LAYER_FRAC,
    T_PHYS_LAYERS,
    cz,
    grow,
    make_imposed_newton,
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
            max_resid = max(max_resid, abs(resid))
    return [r[:] for r in f], max_resid


def make_direct_static_fixed(NL: int, PW: float, H: float, strength: float,
                             src_iz_phys: float, src_layer: int):
    """Exact discrete static comparator at one frozen source position."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    iz_now = round(src_iz_phys / H)
    static, resid = solve_static_poisson(PW, H, strength, iz_now)
    for t in range(src_layer, NL):
        history[t] = [row[:] for row in static]
    return history, resid, iz_now


def measure_at_H(H_val: float, src_iz_phys: float):
    NL = round(T_PHYS_LAYERS / H_val)
    PW = round(PW_PHYS / H_val) * H_val
    k_phase = K_PER_H / H_val
    src_layer = round(SRC_LAYER_FRAC * NL)
    n_active = NL - src_layer
    if n_active < 2:
        return None

    iz_fixed = round(src_iz_phys / H_val)
    source_z_phys = iz_fixed * H_val
    iz_of_t = lambda t, iz=iz_fixed: iz

    h_M = solve_wave(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_I = make_instantaneous(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_Ieq = make_instantaneous_equilibrated(
        NL, PW, H_val, S_PHYS, iz_of_t, src_layer, equilib_multiplier=3
    )
    h_N = make_imposed_newton(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_S, resid_S, iz_real = make_direct_static_fixed(NL, PW, H_val, S_PHYS, src_iz_phys, src_layer)

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_I = cz(prop_beam(pos, adj, nmap, h_I, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_Ieq = cz(prop_beam(pos, adj, nmap, h_Ieq, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_N = cz(prop_beam(pos, adj, nmap, h_N, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_S = cz(prop_beam(pos, adj, nmap, h_S, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    dM = cz_M - z_free
    dI = cz_I - z_free
    dIeq = cz_Ieq - z_free
    dN = cz_N - z_free
    dS = cz_S - z_free
    rel_MI = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
    rel_MIeq = abs(dM - dIeq) / max(abs(dM), abs(dIeq), 1e-12)
    rel_MN = abs(dM - dN) / max(abs(dM), abs(dN), 1e-12)
    rel_MS = abs(dM - dS) / max(abs(dM), abs(dS), 1e-12)
    rel_IeqS = abs(dIeq - dS) / max(abs(dIeq), abs(dS), 1e-12)
    return {
        "H": H_val,
        "NL": NL,
        "PW": PW,
        "src_layer": src_layer,
        "src_iz_phys": src_iz_phys,
        "src_iz_real": source_z_phys,
        "dM": dM,
        "dI": dI,
        "dIeq": dIeq,
        "dN": dN,
        "dS": dS,
        "rel_MI": rel_MI,
        "rel_MIeq": rel_MIeq,
        "rel_MN": rel_MN,
        "rel_MS": rel_MS,
        "rel_IeqS": rel_IeqS,
        "resid_S": resid_S,
        "iz_real": iz_real,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5],
        help="H values to run. Default: 0.5",
    )
    parser.add_argument(
        "--source-z-phys",
        type=float,
        nargs="*",
        default=[3.0, 0.0],
        help="Frozen source z positions in physical units. Default: 3.0 0.0",
    )
    args = parser.parse_args()

    print("=" * 116)
    print("WAVE STATIC SINGLE-SOURCE COMPARATOR PROBE")
    print("=" * 116)
    print("Frozen-source test: compare dM, dI, dIeq, dN, and direct static solve")
    print(f"Physical setup: T_phys={T_PHYS_LAYERS}, PW_phys={PW_PHYS}")
    print(f"Frozen source positions (physical z): {', '.join(f'{z:.3f}' for z in args.source_z_phys)}")

    for src_idx, src_iz_phys in enumerate(args.source_z_phys, start=1):
        print()
        print("=" * 116)
        print(f"SOURCE {src_idx}: frozen source z_phys={src_iz_phys:.3f}")
        print("=" * 116)
        rows = []
        for h_idx, H_val in enumerate(args.hs):
            r = measure_at_H(H_val, src_iz_phys)
            rows.append(r)
            print(f"\n[run {h_idx + 1}] H={H_val:.3f}")
            print(f"  NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}  source_z_real={r['src_iz_real']:.3f}")
            print(f"  dM   = {r['dM']:+.6f}")
            print(f"  dI   = {r['dI']:+.6f}")
            print(f"  dIeq = {r['dIeq']:+.6f}")
            print(f"  dN   = {r['dN']:+.6f}")
            print(f"  dS   = {r['dS']:+.6f}  (direct static solve)")
            print(f"  rel_MI   = {r['rel_MI']:.2%}")
            print(f"  rel_MIeq = {r['rel_MIeq']:.2%}")
            print(f"  rel_MN   = {r['rel_MN']:.2%}")
            print(f"  rel_MS   = {r['rel_MS']:.2%}")
            print(f"  rel_IeqS = {r['rel_IeqS']:.2%}")
            print(f"  static residual = {r['resid_S']:.3e}")

        if len(rows) >= 2:
            print("\n" + "-" * 116)
            print("LAST-STEP STABILITY")
            print("-" * 116)
            a, b = rows[-2], rows[-1]
            print(f"  Δ(rel_MI)   = {abs(b['rel_MI'] - a['rel_MI']):.4f}")
            print(f"  Δ(rel_MIeq) = {abs(b['rel_MIeq'] - a['rel_MIeq']):.4f}")
            print(f"  Δ(rel_MN)   = {abs(b['rel_MN'] - a['rel_MN']):.4f}")
            print(f"  Δ(rel_MS)   = {abs(b['rel_MS'] - a['rel_MS']):.4f}")
            print(f"  Δ(rel_IeqS) = {abs(b['rel_IeqS'] - a['rel_IeqS']):.4f}")

            if abs(b["rel_MS"] - a["rel_MS"]) < abs(b["rel_MIeq"] - a["rel_MIeq"]):
                print("  Verdict: direct static solve is the most stable comparator in the last step.")
            else:
                print("  Verdict: direct static solve is not yet the most stable comparator in the last step.")

        print()
        print("Interpretation:")
        print("  - dM is the retarded-wave response at a frozen source position.")
        print("  - dI / dIeq test cached static slices at the same frozen source position.")
        print("  - dN is the imposed Newton-style comparator at the same frozen source position.")
        print("  - dS is the exact discrete static solve on the same finite (y, z) grid.")
        print("  - If mismatch appears already here, it is not caused by source motion.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
