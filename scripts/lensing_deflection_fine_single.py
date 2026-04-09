#!/usr/bin/env python3
"""Single-b run for the fine H=0.25 refinement of Lane L.

The full lensing_deflection_sweep.py runs 6 b-values at each H in
sequence and got OOM-killed at the H=0.25 fine refinement because
the grow() allocations for NL=60 accumulate across b-values before
Python can GC them.

This script runs ONE b-value at ONE H and prints the result, so
memory is fully freed by the OS between invocations. A bash loop
in the parent harness runs it for each b in the asymptotic subset
{3, 4, 5, 6}.

Usage:
    python3 scripts/lensing_deflection_fine_single.py <H> <b>
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kubo_continuum_limit import (
    grow, finite_diff_dM, true_kubo_at_H,
    T_PHYS, PW_PHYS, K_PER_H, S_PHYS, SRC_LAYER_FRAC,
)


def main():
    if len(sys.argv) != 3:
        print("usage: lensing_deflection_fine_single.py <H> <b>", file=sys.stderr)
        sys.exit(2)
    H_val = float(sys.argv[1])
    b_phys = float(sys.argv[2])

    NL = max(3, round(T_PHYS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = b_phys

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    cz_0 = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, 0.0)
    cz_s = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, S_PHYS)
    dM = cz_s - cz_0
    kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)

    # Print one line, machine-readable
    print(f"H={H_val} b={b_phys} NL={NL} n_nodes={len(pos)} "
          f"dM={dM:+.6f} kubo_true={kubo:+.6f}")


if __name__ == "__main__":
    main()
