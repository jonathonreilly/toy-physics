#!/usr/bin/env python3
"""Shared-geometry direct-vs-matrix-free static comparator probe.

This probe checks whether the matrix-free exact discrete static solve is a
drop-in replacement for the existing direct static solve on one shared
geometry and one shared H.
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
from wave_static_direct_probe import solve_static_poisson as solve_static_poisson_direct


def build_history(static_field, nl: int, src_layer: int):
    hw = len(static_field)
    history = [[[0.0] * hw for _ in range(hw)] for _ in range(nl)]
    for t in range(src_layer, nl):
        history[t] = [row[:] for row in static_field]
    return history


def solve_static_poisson_matrix_free(
    PW: float,
    H: float,
    strength: float,
    iz_now: int,
    tol: float = 1e-10,
    max_iter: int = 6000,
):
    """Solve lap(f) + src = 0 on the finite (y, z) grid with zero boundaries."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = nw // 2
    sz = nw // 2 + iz_now
    f = [[0.0] * nw for _ in range(nw)]
    omega = 2.0 / (1.0 + math.sin(math.pi / nw))

    for it in range(max_iter):
        max_delta = 0.0
        for parity in (0, 1):
            for iy in range(1, nw - 1):
                row = f[iy]
                up = f[iy - 1]
                dn = f[iy + 1]
                startz = 1 + ((iy + parity) & 1)
                for iz in range(startz, nw - 1, 2):
                    src = strength if (iy == sy and iz == sz) else 0.0
                    target = 0.25 * (up[iz] + dn[iz] + row[iz - 1] + row[iz + 1] + src)
                    new = row[iz] + omega * (target - row[iz])
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
                f[iy - 1][iz]
                + f[iy + 1][iz]
                + f[iy][iz - 1]
                + f[iy][iz + 1]
                - 4.0 * f[iy][iz]
                + src
            )
            max_resid = max(max_resid, abs(resid))
    return [r[:] for r in f], max_resid, it + 1


def max_abs_diff(a, b) -> float:
    return max(abs(x - y) for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def max_abs_field(field) -> float:
    return max(abs(x) for row in field for x in row)


def compare_at_h(h_val: float, source_z_phys: float):
    nl = round(T_PHYS_LAYERS / h_val)
    pw = round(PW_PHYS / h_val) * h_val
    src_layer = round(SRC_LAYER_FRAC * nl)
    iz_fixed = round(source_z_phys / h_val)
    k_phase = K_PER_H / h_val
    iz_of_t = lambda _t, iz=iz_fixed: iz

    h_wave = solve_wave(nl, pw, h_val, S_PHYS, iz_of_t, src_layer)
    static_direct, resid_direct = solve_static_poisson_direct(pw, h_val, S_PHYS, iz_fixed)
    static_mf, resid_mf, iters_mf = solve_static_poisson_matrix_free(pw, h_val, S_PHYS, iz_fixed)

    field_diff = max_abs_diff(static_direct, static_mf)
    field_scale = max(max_abs_field(static_direct), max_abs_field(static_mf), 1e-12)
    field_rel = field_diff / field_scale

    history_direct = build_history(static_direct, nl, src_layer)
    history_mf = build_history(static_mf, nl, src_layer)

    pos, adj, nmap = grow(0, 0.20, 0.70, nl, pw, 3, h_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, nl, pw, h_val)
    z_free = cz(free, pos, nl, pw, h_val)
    dM = cz(prop_beam(pos, adj, nmap, h_wave, k_phase, nl, pw, h_val), pos, nl, pw, h_val) - z_free
    dS_direct = cz(prop_beam(pos, adj, nmap, history_direct, k_phase, nl, pw, h_val), pos, nl, pw, h_val) - z_free
    dS_mf = cz(prop_beam(pos, adj, nmap, history_mf, k_phase, nl, pw, h_val), pos, nl, pw, h_val) - z_free

    rel_s = abs(dS_direct - dS_mf) / max(abs(dS_direct), abs(dS_mf), 1e-12)
    rel_ms_direct = abs(dM - dS_direct) / max(abs(dM), abs(dS_direct), 1e-12)
    rel_ms_mf = abs(dM - dS_mf) / max(abs(dM), abs(dS_mf), 1e-12)
    return {
        "H": h_val,
        "NL": nl,
        "PW": pw,
        "src_layer": src_layer,
        "source_z_real": iz_fixed * h_val,
        "dM": dM,
        "dS_direct": dS_direct,
        "dS_mf": dS_mf,
        "rel_S": rel_s,
        "rel_MS_direct": rel_ms_direct,
        "rel_MS_mf": rel_ms_mf,
        "field_diff": field_diff,
        "field_rel": field_rel,
        "resid_direct": resid_direct,
        "resid_mf": resid_mf,
        "iters_mf": iters_mf,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h", type=float, default=0.35, help="Shared lattice spacing. Default: 0.35")
    parser.add_argument("--source-z-phys", type=float, default=3.0, help="Frozen source z in physical units. Default: 3.0")
    args = parser.parse_args()

    r = compare_at_h(args.h, args.source_z_phys)

    print("=" * 108)
    print("WAVE STATIC MATRIX-FREE SHARED-GEOMETRY COMPARE")
    print("=" * 108)
    print(f"Shared H = {r['H']:.3f}")
    print(f"Frozen source z_phys = {args.source_z_phys:.3f} (realized z = {r['source_z_real']:.3f})")
    print(f"NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}")
    print()
    print("Static solve comparison:")
    print(f"  direct residual      = {r['resid_direct']:.3e}")
    print(f"  matrix-free residual = {r['resid_mf']:.3e}")
    print(f"  matrix-free iters    = {r['iters_mf']}")
    print(f"  max |direct - mf|    = {r['field_diff']:.3e}")
    print(f"  rel field mismatch   = {r['field_rel']:.3e}")
    print()
    print("Beam-side comparison with the same beam setup:")
    print(f"  dM         = {r['dM']:+.6f}")
    print(f"  dS direct  = {r['dS_direct']:+.6f}")
    print(f"  dS mf      = {r['dS_mf']:+.6f}")
    print(f"  rel(dS)    = {r['rel_S']:.3e}")
    print(f"  rel_MS dir = {r['rel_MS_direct']:.3e}")
    print(f"  rel_MS mf  = {r['rel_MS_mf']:.3e}")

    print()
    if r["field_rel"] < 1e-8 and r["rel_S"] < 1e-8:
        print("Verdict: matrix-free is a drop-in replacement for the direct static comparator at this geometry.")
    else:
        print("Verdict: matrix-free is close, but not yet proven identical to the direct static comparator.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
