#!/usr/bin/env python3
"""3D inverse-square tail statistics at h=0.25.

This is a narrow review-safe probe for the exploratory 1/L^2 propagator fork.
It compares a baseline width against a wider width at the same lattice spacing
and asks only whether the post-peak distance tail becomes better resolved.

The harness keeps the same family, same barrier geometry, same action, and the
same gravity-observable hierarchy. It does not attempt to promote the branch.
"""

from __future__ import annotations

import os
import math
import sys
from contextlib import contextmanager

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.lattice_3d_inverse_square_kernel as base


H = 0.25
PHYS_L = 12.0
MAX_D_PHYS = 3.0
WIDTHS = (8.0,)


@contextmanager
def patched_branch(width: float):
    old_w = base.PHYS_W
    old_mass_z = list(base.MASS_Z_VALUES)
    try:
        base.PHYS_W = width
        base.MASS_Z_VALUES = [float(z) for z in range(4, int(width) + 1)]
        yield
    finally:
        base.PHYS_W = old_w
        base.MASS_Z_VALUES = old_mass_z


def tail_fit_from_rows(rows):
    if not rows:
        return math.nan, 0.0, 0, math.nan
    peak_idx = max(range(len(rows)), key=lambda i: rows[i][1])
    tail = [(mass_z, centroid) for mass_z, centroid, _, _, _ in rows[peak_idx:] if centroid > 0]
    slope, r2 = base.fit_power(tail)
    peak_z = rows[peak_idx][0]
    return slope, r2, len(tail), peak_z


def run_width(width: float):
    with patched_branch(width):
        pos, adj, nl, hw, nmap, det, barrier_layer, barrier, slit_indices, blocked, gl, span = base.build_family(H)
        barrier_row = base.barrier_metrics(pos, adj, det, barrier, slit_indices, blocked, gl, nmap, 3.0, H)
        rows, aligned, _, _ = base.no_barrier_distance(pos, adj, det, gl, nmap, H)

    slope, r2, n_tail, peak_z = tail_fit_from_rows(rows)

    print("=" * 96)
    print(f"3D 1/L^2 tail stats at h={H}  width={width:g}")
    print(f"  nodes={len(pos):,}  layers={nl}  span={span}")
    print(
        f"  barrier: Born={barrier_row['born']:.2e}  k0={barrier_row['k0']:+.6f}  "
        f"dTV={barrier_row['dtv']:.3f}  read={barrier_row['interp']}"
    )
    print(
        f"  barrier centroid={barrier_row['centroid']:+.6f}  "
        f"P_near={barrier_row['pnear']:+.6f}  bias={barrier_row['bias']:+.6f}"
    )
    print("  no-barrier rows:")
    for mass_z, centroid, pnear, bias, interp in rows:
        print(
            f"    z={mass_z:>2.0f}  centroid={centroid:+.6f}  "
            f"P_near={pnear:+.6f}  bias={bias:+.6f}  read={interp}"
        )
    if n_tail >= 3:
        print(f"  tail fit: peak@z={peak_z:.0f}  n_tail={n_tail}  exponent=b^({slope:.2f})  R^2={r2:.3f}")
    else:
        print(f"  tail fit: peak@z={peak_z:.0f}  n_tail={n_tail}  fit=n/a")
    return {"width": width, "n_tail": n_tail, "slope": slope, "r2": r2}


def main() -> None:
    print("=" * 96)
    print("3D INVERSE-SQUARE TAIL STATISTICS")
    print("  Review-safe tail probe for the exploratory 1/L^2 branch.")
    print("  Same family, same barrier geometry, same action, h=0.25.")
    print("=" * 96)
    print()

    results = [run_width(w) for w in WIDTHS]

    print()
    print("Comparison:")
    for r in results:
        print(
            f"  width={r['width']:g}: n_tail={r['n_tail']}  "
            f"exponent={r['slope']:.2f}  R^2={r['r2']:.3f}"
        )
    if len(results) >= 2 and results[1]["n_tail"] >= results[0]["n_tail"] and results[1]["r2"] >= results[0]["r2"]:
        print("  verdict: wider lattice improves the post-peak tail fit")
    elif len(results) == 1:
        print("  verdict: single-width probe; compare against the prior width-6 baseline log")
    else:
        print("  verdict: no clear improvement from widening the lattice")


if __name__ == "__main__":
    main()
