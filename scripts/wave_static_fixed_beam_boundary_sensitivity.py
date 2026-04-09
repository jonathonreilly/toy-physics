#!/usr/bin/env python3
"""Fixed-beam boundary-sensitivity probe for the direct static comparator.

This probe isolates the specific confound in the earlier boundary test:

  keep the beam DAG fixed at a baseline field width, enlarge only the
  field/static solve box, then crop the enlarged field back to the
  baseline beam box before beam propagation.

The question is whether the direct static comparator dS and the
retarded/static mismatch rel_MS are still materially box-sensitive when
the beam geometry itself is held fixed.
"""

from __future__ import annotations

import argparse
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
            if abs(resid) > max_resid:
                max_resid = abs(resid)
    return [r[:] for r in f], max_resid


def crop_square(history_big, nw_small: int):
    """Crop the centered nw_small x nw_small square from each time slice."""
    nw_big = len(history_big[0])
    if nw_small > nw_big:
        raise ValueError("Cannot crop to a larger square")
    off = (nw_big - nw_small) // 2
    cropped = []
    for slice_ in history_big:
        cropped.append([row[off:off + nw_small] for row in slice_[off:off + nw_small]])
    return cropped


def measure_at(field_pw_phys: float, beam_pw_phys: float, H_val: float, src_iz_phys: float):
    NL = round(T_PHYS_LAYERS / H_val)
    field_pw = round(field_pw_phys / H_val) * H_val
    beam_pw = round(beam_pw_phys / H_val) * H_val
    beam_nw = 2 * int(beam_pw / H_val) + 1
    src_layer = round(SRC_LAYER_FRAC * NL)
    n_active = NL - src_layer
    if n_active < 2:
        return None

    iz_fixed = round(src_iz_phys / H_val)
    iz_of_t = lambda t, iz=iz_fixed: iz

    h_M_big = solve_wave(NL, field_pw, H_val, S_PHYS, iz_of_t, src_layer)
    h_S_big, resid_S = solve_static_poisson(field_pw, H_val, S_PHYS, iz_fixed)

    beam_pos, beam_adj, beam_nmap = grow(0, 0.20, 0.70, NL, beam_pw, 3, H_val)
    k_phase = K_PER_H / H_val
    free = prop_beam(beam_pos, beam_adj, beam_nmap, None, k_phase, NL, beam_pw, H_val)
    z_free = cz(free, beam_pos, NL, beam_pw, H_val)

    h_M = crop_square(h_M_big, beam_nw)
    h_S = [[[0.0] * beam_nw for _ in range(beam_nw)] for _ in range(NL)]
    cropped_static = crop_square([h_S_big], beam_nw)[0]
    for t in range(src_layer, NL):
        h_S[t] = [row[:] for row in cropped_static]

    dM = cz(prop_beam(beam_pos, beam_adj, beam_nmap, h_M, k_phase, NL, beam_pw, H_val), beam_pos, NL, beam_pw, H_val) - z_free
    dS = cz(prop_beam(beam_pos, beam_adj, beam_nmap, h_S, k_phase, NL, beam_pw, H_val), beam_pos, NL, beam_pw, H_val) - z_free
    rel_MS = abs(dM - dS) / max(abs(dM), abs(dS), 1e-12)
    return {
        "field_pw_phys": field_pw_phys,
        "field_pw": field_pw,
        "beam_pw_phys": beam_pw_phys,
        "beam_pw": beam_pw,
        "H": H_val,
        "NL": NL,
        "src_layer": src_layer,
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
    parser.add_argument("--beam-pw-phys", type=float, default=6.0, help="Fixed beam-box half-width in physical units. Default: 6.0")
    parser.add_argument("--field-pw-phys", type=float, nargs="*", default=[6.0, 9.0], help="Field/static solve box half-widths in physical units. Default: 6.0 9.0")
    args = parser.parse_args()

    if len(args.field_pw_phys) < 2:
        raise SystemExit("Need at least two field PW values to compare.")

    print("=" * 112)
    print("WAVE STATIC FIXED-BEAM BOUNDARY-SENSITIVITY PROBE")
    print("=" * 112)
    print(f"Shared H = {args.h:.3f}")
    print(f"Frozen source z_phys = {args.source_z_phys:.3f}")
    print(f"Fixed beam PW_phys = {args.beam_pw_phys:.3f}")
    print(f"Field PW values = {', '.join(f'{pw:.3f}' for pw in args.field_pw_phys)}")

    rows = []
    for idx, field_pw_phys in enumerate(args.field_pw_phys, start=1):
        r = measure_at(field_pw_phys, args.beam_pw_phys, args.h, args.source_z_phys)
        rows.append(r)
        print(f"\n[run {idx}] field_PW_phys={field_pw_phys:.3f} -> field_PW={r['field_pw']:.3f}")
        print(f"  beam_PW={r['beam_pw']:.3f}  NL={r['NL']}  src_layer={r['src_layer']}  source_z_real={r['src_iz_real']:.3f}")
        print(f"  dM      = {r['dM']:+.6f}")
        print(f"  dS      = {r['dS']:+.6f}")
        print(f"  rel_MS  = {r['rel_MS']:.2%}")
        print(f"  residual = {r['resid_S']:.3e}")

    if len(rows) >= 2:
        base = rows[0]
        big = rows[-1]
        print("\n" + "-" * 112)
        print("FIELD-BOX MOVE")
        print("-" * 112)
        print(f"  dS move      = {rel_move(base['dS'], big['dS']):.2%}")
        print(f"  rel_MS move  = {rel_move(base['rel_MS'], big['rel_MS']):.2%}")
        print(f"  dM move      = {rel_move(base['dM'], big['dM']):.2%}")
        if rel_move(base["dS"], big["dS"]) < 0.05 and rel_move(base["rel_MS"], big["rel_MS"]) < 0.05:
            print("  Verdict: fixed-beam boundary sensitivity is small at this H.")
        else:
            print("  Verdict: fixed-beam boundary sensitivity is still material at this H.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
