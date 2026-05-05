#!/usr/bin/env python3
"""Direct-dM matched-schedule probe for the wave-retardation lane.

This is the smallest direct finite-c fallback probe:

  hold the beam setup fixed, use two source histories with the same
  start position, end position, total NL, and final source geometry,
  and compare the direct retarded-wave beam response dM.

The two schedules use the same realized moving trace and move-step
count, but place that trace at different times within the active
interval:

  early-move : move to the final source position in the first half of
               the active interval, then sit
  late-move  : sit first, then move to the same final source position in
               the second half of the active interval
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import gc
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

FAMILIES = (
    ("Fam1", 0.20, 0.70),
    ("Fam2", 0.05, 0.30),
    ("Fam3", 0.50, 0.90),
)


def _shared_move_trace(iz_start: int, iz_end: int, move_steps: int):
    if move_steps <= 1:
        return [iz_end]
    return [
        iz_start + int(round((iz_end - iz_start) * (u / (move_steps - 1))))
        for u in range(move_steps)
    ]


def make_early_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    move_steps = max(2, active // 2)
    trace = _shared_move_trace(iz_start, iz_end, move_steps)
    hold_steps = active - move_steps

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u < move_steps:
            return trace[u]
        if hold_steps > 0:
            return iz_end
        return trace[-1]

    return iz_of_t


def make_late_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    move_steps = max(2, active // 2)
    wait_steps = active - move_steps
    trace = _shared_move_trace(iz_start, iz_end, move_steps)

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u < wait_steps:
            return iz_start
        v = u - wait_steps
        if v < move_steps:
            return trace[v]
        return trace[-1]

    return iz_of_t


def family_specs(labels: list[str]):
    wanted = set(labels)
    return [spec for spec in FAMILIES if spec[0] in wanted]


def measure_dm(h_val: float, strength: float, family_label: str, drift: float, restore: float, seed: int = 0):
    nl = round(T_PHYS_LAYERS / h_val)
    pw = round(PW_PHYS / h_val) * h_val
    k_phase = K_PER_H / h_val
    src_layer = round(SRC_LAYER_FRAC * nl)
    if nl - src_layer < 4:
        return None

    iz_start = round(IZ_START_PHYS / h_val)
    iz_end = round(IZ_END_PHYS / h_val)

    pos, adj, nmap = grow(seed, drift, restore, nl, pw, 3, h_val)
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
        "family": family_label,
        "drift": drift,
        "restore": restore,
        "seed": seed,
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
    parser.add_argument(
        "--families",
        nargs="*",
        default=["Fam1"],
        help="Family labels to probe. Available: Fam1 Fam2 Fam3. Default: Fam1",
    )
    args = parser.parse_args()
    families = family_specs(args.families)
    if not families:
        raise SystemExit(f"no valid families selected: {args.families}")

    print("=" * 108)
    print("WAVE DIRECT-DM MATCHED-HISTORY PROBE")
    print("=" * 108)
    print("Two source schedules with the same start/end/final geometry and the same realized move trace")
    print("Includes an exact S=0 null and a small-s sweep over the direct response")

    for family_label, drift, restore in families:
        print(f"\n[family={family_label} drift={drift:.2f} restore={restore:.2f}]")
        for strength in args.strengths:
            print(f"  [strength={strength:.6f}]")
            for h_val in args.hs:
                r = measure_dm(h_val, strength, family_label, drift, restore)
                print(f"    [H={h_val:.3f}]")
                print(f"      NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}")
                print(f"      start_z_real={r['iz_start_real']:.3f}  end_z_real={r['iz_end_real']:.3f}")
                print(f"      dM(early)    = {r['d_early']:+.6f}")
                print(f"      dM(late)     = {r['d_late']:+.6f}")
                print(f"      delta_hist   = {r['delta_hist']:+.6f}")
                print(f"      R_hist       = {r['r_hist']:+.2%}")
                if abs(strength) <= 1e-12:
                    print("      null         = exact S=0 control")
                else:
                    print(f"      delta_hist/s = {r['delta_hist'] / strength:+.6f}")
                gc.collect()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
