#!/usr/bin/env python3
"""Static-comparator probe for the wave-retardation lane.

This script tests the next concrete comparator candidate after the corrected
continuum negative:

  build the gauge-fixed free-space (infinite-lattice) discrete Green
  comparator history on the same (y, z) field grid.

The probe is intentionally narrow:
  - same physical setup as wave_retardation_continuum_limit.py
  - same beam DAG / propagator
  - compare three static comparators:
      dI    = cached static slice at NL_dyn
      dIeq  = cached static slice at 3 * NL_dyn
      dGinf = gauge-fixed infinite-lattice Green history

This lane only lands the reusable constructor/cache prerequisite and integration
point. It does not assert a final comparator verdict.

Current review-safe default evidence is the coarse/medium ladder
H={0.5, 0.35}. The fine point H=0.25 remains an optional validation run and
is expensive enough on the current workstation that it should not be treated
as retained default evidence.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

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
from infinite_lattice_green_kernel import gauge_fixed_green_kernel_2d


def make_infinite_lattice_static(NL, PW, H, strength, iz_of_t, src_layer):
    """Gauge-fixed infinite-lattice static comparator history.

    Uses the 2D free-space discrete Green kernel with G(0,0)=0.
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = nw // 2
    max_offset = 2 * hw
    kernel = gauge_fixed_green_kernel_2d(max_offset=max_offset)
    offset = max_offset

    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    slice_cache = {}
    for t in range(NL):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in slice_cache:
            sz = sy + iz_now
            field = [[0.0] * nw for _ in range(nw)]
            for iy in range(nw):
                dy = iy - sy
                kernel_y = kernel[dy + offset]
                row = field[iy]
                for iz in range(nw):
                    dz = iz - sz
                    row[iz] = strength * kernel_y[dz + offset]
            slice_cache[iz_now] = field
        history[t] = [row[:] for row in slice_cache[iz_now]]
    return history, {"cached_source_positions": len(slice_cache), "kernel_max_offset": max_offset}


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
    h_Ginf, ginf_meta = make_infinite_lattice_static(
        NL, PW, H_val, S_PHYS, iz_of_t, src_layer
    )

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_I = cz(prop_beam(pos, adj, nmap, h_I, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_Ieq = cz(prop_beam(pos, adj, nmap, h_Ieq, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_Ginf = cz(prop_beam(pos, adj, nmap, h_Ginf, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    dM = cz_M - z_free
    dI = cz_I - z_free
    dIeq = cz_Ieq - z_free
    dGinf = cz_Ginf - z_free
    rel_MI = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
    rel_MIeq = abs(dM - dIeq) / max(abs(dM), abs(dIeq), 1e-12)
    rel_MGinf = abs(dM - dGinf) / max(abs(dM), abs(dGinf), 1e-12)
    rel_IeqGinf = abs(dIeq - dGinf) / max(abs(dIeq), abs(dGinf), 1e-12)
    return {
        "label": label,
        "H": H_val,
        "NL": NL,
        "dM": dM,
        "dI": dI,
        "dIeq": dIeq,
        "dGinf": dGinf,
        "rel_MI": rel_MI,
        "rel_MIeq": rel_MIeq,
        "rel_MGinf": rel_MGinf,
        "rel_IeqGinf": rel_IeqGinf,
        "ginf_meta": ginf_meta,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35],
        help="H values to run. Default: 0.5 0.35 (H=0.25 optional and expensive)",
    )
    args = parser.parse_args()

    print("=" * 100)
    print("WAVE STATIC INFINITE-LATTICE COMPARATOR PREREQUISITE")
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
        print(f"  dGinf = {r['dGinf']:+.6f}  (gauge-fixed infinite-lattice Green)")
        print(f"  rel_MI   = {r['rel_MI']:.2%}")
        print(f"  rel_MIeq = {r['rel_MIeq']:.2%}")
        print(f"  rel_MGinf   = {r['rel_MGinf']:.2%}")
        print(f"  rel_IeqGinf = {r['rel_IeqGinf']:.2%}")
        print(
            "  Ginf history cache: "
            f"{r['ginf_meta']['cached_source_positions']} source z slices, "
            f"kernel max_offset={r['ginf_meta']['kernel_max_offset']}"
        )

    if len(rows) >= 2:
        print("\n" + "=" * 100)
        print("LAST-STEP STABILITY")
        print("=" * 100)
        a, b = rows[-2], rows[-1]
        print(f"  Δ(rel_MI)   = {abs(b['rel_MI'] - a['rel_MI']):.4f}")
        print(f"  Δ(rel_MIeq) = {abs(b['rel_MIeq'] - a['rel_MIeq']):.4f}")
        print(f"  Δ(rel_MGinf)   = {abs(b['rel_MGinf'] - a['rel_MGinf']):.4f}")
        print(f"  Δ(rel_IeqGinf) = {abs(b['rel_IeqGinf'] - a['rel_IeqGinf']):.4f}")


if __name__ == "__main__":
    main()
