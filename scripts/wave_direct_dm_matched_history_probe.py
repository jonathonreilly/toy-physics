#!/usr/bin/env python3
"""Direct-dM matched-history probe for the wave-retardation lane.

This is the smallest direct finite-c fallback probe:

  hold the beam setup fixed, use two source histories with the same
  start position, end position, total NL, and final source geometry,
  and compare the direct retarded-wave beam response dM.

The two histories are:

  early-move : move to the final source position in the first half of
               the active interval, then sit
  late-move  : sit first, then move to the same final source position in
               the second half of the active interval
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from wave_retardation_continuum_limit import (
    IZ_END_PHYS,
    IZ_START_PHYS,
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


def make_early_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    move_steps = max(1, active // 2)

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u >= move_steps:
            return iz_end
        frac = u / move_steps
        return iz_start + int(round((iz_end - iz_start) * frac))

    return iz_of_t


def make_late_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    wait_steps = max(1, active // 2)
    move_steps = max(1, active - wait_steps)

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u < wait_steps:
            return iz_start
        v = u - wait_steps
        if v >= move_steps:
            return iz_end
        frac = v / move_steps
        return iz_start + int(round((iz_end - iz_start) * frac))

    return iz_of_t


def measure_dm(h_val: float, strength: float):
    nl = round(T_PHYS_LAYERS / h_val)
    pw = round(PW_PHYS / h_val) * h_val
    k_phase = K_PER_H / h_val
    src_layer = round(SRC_LAYER_FRAC * nl)
    if nl - src_layer < 4:
        return None

    iz_start = round(IZ_START_PHYS / h_val)
    iz_end = round(IZ_END_PHYS / h_val)

    pos, adj, nmap = grow(0, 0.20, 0.70, nl, pw, 3, h_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, nl, pw, h_val)
    z_free = cz(free, pos, nl, pw, h_val)

    early = make_early_move(iz_start, iz_end, src_layer, nl)
    late = make_late_move(iz_start, iz_end, src_layer, nl)

    h_early = solve_wave(nl, pw, h_val, strength, early, src_layer)
    h_late = solve_wave(nl, pw, h_val, strength, late, src_layer)

    d_early = cz(prop_beam(pos, adj, nmap, h_early, k_phase, nl, pw, h_val), pos, nl, pw, h_val) - z_free
    d_late = cz(prop_beam(pos, adj, nmap, h_late, k_phase, nl, pw, h_val), pos, nl, pw, h_val) - z_free
    delta_hist = d_early - d_late
    r_hist = delta_hist / max(abs(d_early), abs(d_late), 1e-12)

    return {
        "H": h_val,
        "NL": nl,
        "PW": pw,
        "src_layer": src_layer,
        "iz_start_real": iz_start * h_val,
        "iz_end_real": iz_end * h_val,
        "strength": strength,
        "d_early": d_early,
        "d_late": d_late,
        "delta_hist": delta_hist,
        "r_hist": r_hist,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35],
        help="H values to probe. Default: 0.5 0.35",
    )
    parser.add_argument(
        "--strengths",
        type=float,
        nargs="*",
        default=[0.0, S_PHYS, 2.0 * S_PHYS],
        help="Source strengths to probe. Default: 0, S_PHYS, 2*S_PHYS",
    )
    args = parser.parse_args()

    print("=" * 108)
    print("WAVE DIRECT-DM MATCHED-HISTORY PROBE")
    print("=" * 108)
    print("Two histories with the same start/end/final geometry, different timing of motion")
    print("Includes an exact S=0 null and a small-s sweep over the direct response")

    for strength in args.strengths:
        print(f"\n[strength={strength:.6f}]")
        for h_val in args.hs:
            r = measure_dm(h_val, strength)
            print(f"  [H={h_val:.3f}]")
            print(f"    NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}")
            print(f"    start_z_real={r['iz_start_real']:.3f}  end_z_real={r['iz_end_real']:.3f}")
            print(f"    dM(early)    = {r['d_early']:+.6f}")
            print(f"    dM(late)     = {r['d_late']:+.6f}")
            print(f"    delta_hist   = {r['delta_hist']:+.6f}")
            print(f"    R_hist       = {r['r_hist']:+.2%}")
            if abs(strength) <= 1e-12:
                print("    null         = exact S=0 control")
            else:
                print(f"    delta_hist/s = {r['delta_hist'] / strength:+.6f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
