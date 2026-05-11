#!/usr/bin/env python3
"""Matrix-free fixed-beam boundary probe for the static comparator.

This probe asks one narrow question:

  At a shared H and fixed beam geometry, does the matrix-free exact
  discrete static solve remain boundary-sensitive when only the field
  box is enlarged?

It isolates the comparator question more cleanly than the earlier
boundary tests by:

  - keeping the beam DAG fixed at a baseline beam PW
  - enlarging only the field/static solve box
  - cropping the enlarged field back to the baseline beam box before
    propagation

If the boundary sensitivity survives this setup at a finer H, the
comparator lane is very unlikely to be rescued by box refinement alone.
"""

from __future__ import annotations

# Heavy compute / lattice-sweep runner: default cache runs have shown
# enough machine-to-machine variance to need a bounded override above
# the 120s audit-cache default.
AUDIT_TIMEOUT_SEC = 180

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


def crop_square(field_big, nw_small: int):
    nw_big = len(field_big)
    if nw_small > nw_big:
        raise ValueError("Cannot crop to a larger square")
    off = (nw_big - nw_small) // 2
    return [row[off:off + nw_small] for row in field_big[off:off + nw_small]]


def crop_history(history_big, nw_small: int):
    """Crop each 2D slice of a 3D history without changing NL."""
    return [crop_square(slice_, nw_small) for slice_ in history_big]


def measure_at(field_pw_phys: float, beam_pw_phys: float, H_val: float, src_iz_phys: float):
    nl = round(T_PHYS_LAYERS / H_val)
    field_pw = round(field_pw_phys / H_val) * H_val
    beam_pw = round(beam_pw_phys / H_val) * H_val
    beam_nw = 2 * int(beam_pw / H_val) + 1
    src_layer = round(SRC_LAYER_FRAC * nl)
    if nl - src_layer < 2:
        return None

    iz_fixed = round(src_iz_phys / H_val)
    iz_of_t = lambda _t, iz=iz_fixed: iz

    h_wave = solve_wave(nl, field_pw, H_val, S_PHYS, iz_of_t, src_layer)
    static_big, resid_mf, iters_mf = solve_static_poisson_matrix_free(field_pw, H_val, S_PHYS, iz_fixed)
    static = crop_square(static_big, beam_nw)
    h_stat = [[[0.0] * beam_nw for _ in range(beam_nw)] for _ in range(nl)]
    for t in range(src_layer, nl):
        h_stat[t] = [row[:] for row in static]
    h_wave_crop = crop_history(h_wave, beam_nw)

    pos, adj, nmap = grow(0, 0.20, 0.70, nl, beam_pw, 3, H_val)
    k_phase = K_PER_H / H_val
    free = prop_beam(pos, adj, nmap, None, k_phase, nl, beam_pw, H_val)
    z_free = cz(free, pos, nl, beam_pw, H_val)
    dM = cz(prop_beam(pos, adj, nmap, h_wave_crop, k_phase, nl, beam_pw, H_val), pos, nl, beam_pw, H_val) - z_free
    dS = cz(prop_beam(pos, adj, nmap, h_stat, k_phase, nl, beam_pw, H_val), pos, nl, beam_pw, H_val) - z_free
    rel_MS = abs(dM - dS) / max(abs(dM), abs(dS), 1e-12)
    return {
        "field_pw_phys": field_pw_phys,
        "field_pw": field_pw,
        "beam_pw": beam_pw,
        "H": H_val,
        "NL": nl,
        "src_layer": src_layer,
        "source_z_real": iz_fixed * H_val,
        "dM": dM,
        "dS": dS,
        "rel_MS": rel_MS,
        "resid_mf": resid_mf,
        "iters_mf": iters_mf,
    }


def rel_move(a: float, b: float) -> float:
    return abs(b - a) / max(abs(a), abs(b), 1e-12)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h", type=float, default=0.35, help="Shared H. Default: 0.35")
    parser.add_argument("--source-z-phys", type=float, default=3.0, help="Frozen source z position. Default: 3.0")
    parser.add_argument("--beam-pw-phys", type=float, default=6.0, help="Fixed beam PW. Default: 6.0")
    parser.add_argument("--field-pw-phys", type=float, nargs="*", default=[6.0, 9.0], help="Field PW values. Default: 6.0 9.0")
    args = parser.parse_args()

    if len(args.field_pw_phys) < 2:
        raise SystemExit("Need at least two field PW values to compare.")

    print("=" * 112)
    print("WAVE STATIC MATRIX-FREE FIXED-BEAM BOUNDARY PROBE")
    print("=" * 112)
    print(f"Shared H = {args.h:.3f}")
    print(f"Frozen source z_phys = {args.source_z_phys:.3f}")
    print(f"Fixed beam PW = {args.beam_pw_phys:.3f}")
    print(f"Field PW values = {', '.join(f'{pw:.3f}' for pw in args.field_pw_phys)}")

    rows = []
    for idx, field_pw_phys in enumerate(args.field_pw_phys, start=1):
        r = measure_at(field_pw_phys, args.beam_pw_phys, args.h, args.source_z_phys)
        rows.append(r)
        print(f"\n[run {idx}] field_PW_phys={field_pw_phys:.3f} -> field_PW={r['field_pw']:.3f}")
        print(f"  beam_PW={r['beam_pw']:.3f}  NL={r['NL']}  src_layer={r['src_layer']}  source_z_real={r['source_z_real']:.3f}")
        print(f"  dM      = {r['dM']:+.6f}")
        print(f"  dS      = {r['dS']:+.6f}")
        print(f"  rel_MS  = {r['rel_MS']:.2%}")
        print(f"  matrix-free residual = {r['resid_mf']:.3e}")
        print(f"  matrix-free iters    = {r['iters_mf']}")

    base = rows[0]
    big = rows[-1]
    print("\n" + "-" * 112)
    print("FIELD-BOX MOVE")
    print("-" * 112)
    print(f"  dS move      = {rel_move(base['dS'], big['dS']):.2%}")
    print(f"  rel_MS move  = {rel_move(base['rel_MS'], big['rel_MS']):.2%}")
    print(f"  dM move      = {rel_move(base['dM'], big['dM']):.2%}")
    if rel_move(base["dS"], big["dS"]) < 0.05 and rel_move(base["rel_MS"], big["rel_MS"]) < 0.05:
        print("  Verdict: matrix-free fixed-beam boundary sensitivity is small at this H.")
    else:
        print("  Verdict: matrix-free fixed-beam boundary sensitivity is still material at this H.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
