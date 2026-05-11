#!/usr/bin/env python3
"""Boundary-sensitivity probe for the direct static comparator.

This probe asks one narrow question:

  At one shared H and one frozen source position, how much do the direct
  static comparator dS and the relative mismatch rel_MS move when the
  field box PW is enlarged?

The probe compares two PW values at the same H:

  - a baseline field box
  - an enlarged field box

For each PW it computes:

  dM   = retarded-wave response
  dS   = exact discrete static solve on the finite (y, z) grid
  rel_MS = |dM - dS| / max(|dM|, |dS|)

The point is not to claim a continuum limit. It is to test whether the
direct static comparator is merely finite-box dominated at the current
shared H.
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


def measure_at(PW_phys: float, H_val: float, src_iz_phys: float):
    NL = round(T_PHYS_LAYERS / H_val)
    PW = round(PW_phys / H_val) * H_val
    src_layer = round(SRC_LAYER_FRAC * NL)
    n_active = NL - src_layer
    if n_active < 2:
        return None

    iz_fixed = round(src_iz_phys / H_val)
    iz_of_t = lambda t, iz=iz_fixed: iz

    h_M = solve_wave(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_S, resid_S = solve_static_poisson(PW, H_val, S_PHYS, iz_fixed)

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    k_phase = K_PER_H / H_val
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    dM = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val) - z_free
    h_hist = [[[0.0] * len(h_S) for _ in range(len(h_S))] for _ in range(NL)]
    for t in range(src_layer, NL):
        h_hist[t] = [row[:] for row in h_S]
    dS = cz(prop_beam(pos, adj, nmap, h_hist, k_phase, NL, PW, H_val), pos, NL, PW, H_val) - z_free
    rel_MS = abs(dM - dS) / max(abs(dM), abs(dS), 1e-12)
    return {
        "PW_phys": PW_phys,
        "PW": PW,
        "NL": NL,
        "src_layer": src_layer,
        "src_iz_phys": src_iz_phys,
        "src_iz_real": iz_fixed * H_val,
        "dM": dM,
        "dS": dS,
        "rel_MS": rel_MS,
        "resid_S": resid_S,
    }


def rel_move(a: float, b: float) -> float:
    return abs(b - a) / max(abs(a), abs(b), 1e-12)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h", type=float, default=0.5, help="Shared H. Default: 0.5")
    parser.add_argument("--source-z-phys", type=float, default=3.0, help="Frozen source z position. Default: 3.0")
    parser.add_argument("--pw-phys", type=float, nargs="*", default=[6.0, 9.0], help="Field box widths in physical units. Default: 6.0 9.0")
    args = parser.parse_args()

    if len(args.pw_phys) < 2:
        raise SystemExit("Need at least two PW values to compare.")

    print("=" * 108)
    print("WAVE STATIC BOUNDARY-SENSITIVITY PROBE")
    print("=" * 108)
    print(f"Shared H = {args.h:.3f}")
    print(f"Frozen source z_phys = {args.source_z_phys:.3f}")
    print(f"PW values = {', '.join(f'{pw:.3f}' for pw in args.pw_phys)}")

    rows = []
    for idx, pw_phys in enumerate(args.pw_phys, start=1):
        r = measure_at(pw_phys, args.h, args.source_z_phys)
        rows.append(r)
        print(f"\n[run {idx}] PW_phys={pw_phys:.3f} -> PW={r['PW']:.3f}")
        print(f"  NL={r['NL']}  src_layer={r['src_layer']}  source_z_real={r['src_iz_real']:.3f}")
        print(f"  dM      = {r['dM']:+.6f}")
        print(f"  dS      = {r['dS']:+.6f}")
        print(f"  rel_MS  = {r['rel_MS']:.2%}")
        print(f"  residual = {r['resid_S']:.3e}")

    if len(rows) >= 2:
        base = rows[0]
        big = rows[-1]
        print("\n" + "-" * 108)
        print("BOUNDARY MOVE")
        print("-" * 108)
        print(f"  dS move      = {rel_move(base['dS'], big['dS']):.2%}")
        print(f"  rel_MS move  = {rel_move(base['rel_MS'], big['rel_MS']):.2%}")
        print(f"  dM move      = {rel_move(base['dM'], big['dM']):.2%}")
        if rel_move(base["dS"], big["dS"]) < 0.05 and rel_move(base["rel_MS"], big["rel_MS"]) < 0.05:
            print("  Verdict: boundary sensitivity is small at this H.")
        else:
            print("  Verdict: boundary sensitivity is still material at this H.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
