#!/usr/bin/env python3
"""Focused beta sweep for the lensing-slope mechanism check.

This lane tests whether the apparent `beta=5` near-`1/b` behavior at coarse
resolution is a real narrow-beam limit or just an isolated coincidence.

Two decisive checks:
1. Coarse-H sweep on the asymptotic subset `b in {3,4,5,6}` for a small set of
   beta values around the claimed ray-like point.
2. Medium-H refinement check at `beta=5`.

If `beta=5` were a real ray-optics limit, nearby large beta values should stay
near slope `-1`, and the refinement check should preserve both sign and shape.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lensing_deflection_sweep import log_slope
from kubo_continuum_limit import K_PER_H, PW_PHYS, SRC_LAYER_FRAC, grow, true_kubo_at_H


DEFAULT_BS = [3.0, 4.0, 5.0, 6.0]
DEFAULT_BETAS = [0.8, 5.0, 7.0, 10.0]
DEFAULT_HS = [0.5]
DEFAULT_DRIFT = 0.20
DEFAULT_RESTORE = 0.70


def measure_kubo_sweep(H_val, b_values, beta, seed=0, drift=DEFAULT_DRIFT, restore=DEFAULT_RESTORE):
    NL = max(3, round(15.0 / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    pos, adj, _ = grow(seed, drift, restore, NL, PW, 3, H_val)
    rows = []
    for b in b_values:
        kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, b, beta=beta)
        rows.append({"b": b, "kubo_true": kubo})
    return {"H": H_val, "NL": NL, "beta": beta, "x_src": x_src, "rows": rows}


def shape_spread(rows):
    base_b = rows[0]["b"]
    base_v = abs(rows[0]["kubo_true"])
    if base_v <= 1e-30:
        return float("nan")
    rel_errs = []
    for row in rows[1:]:
        target = base_b / row["b"]
        actual = abs(row["kubo_true"]) / base_v
        rel_errs.append(abs(actual - target) / target)
    return max(rel_errs) if rel_errs else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--betas", type=float, nargs="*", default=DEFAULT_BETAS)
    parser.add_argument("--b-values", type=float, nargs="*", default=DEFAULT_BS)
    parser.add_argument("--coarse-h", type=float, default=0.5)
    parser.add_argument("--refine-beta", type=float, default=5.0)
    parser.add_argument("--refine-h", type=float, default=0.35)
    args = parser.parse_args()

    print("=" * 100)
    print("LENSING BETA SWEEP")
    print("=" * 100)
    print(f"b_values={args.b_values}")
    print(f"coarse_h={args.coarse_h:g}  refine_beta={args.refine_beta:g}  refine_h={args.refine_h:g}")
    print()

    print("Coarse-H asymptotic sweep")
    print(f"{'beta':>6s} {'kubo(b=3..6)':>42s} {'slope':>9s} {'R²':>8s} {'signs':>8s} {'1/b spread':>12s}")
    for beta in args.betas:
        run = measure_kubo_sweep(args.coarse_h, args.b_values, beta)
        vals = [row["kubo_true"] for row in run["rows"]]
        slope, _, r2 = log_slope(args.b_values, vals)
        signs = "".join("+" if v > 0 else "-" if v < 0 else "0" for v in vals)
        spread = shape_spread(run["rows"])
        print(
            f"{beta:6.1f} {str([round(v, 4) for v in vals]):>42s}"
            f" {slope:9.4f} {r2:8.4f} {signs:>8s} {spread:12.2%}"
        )

    print()
    print("Refinement check at beta near the apparent ray-like spike")
    refine = measure_kubo_sweep(args.refine_h, args.b_values, args.refine_beta)
    vals = [row["kubo_true"] for row in refine["rows"]]
    slope, _, r2 = log_slope(args.b_values, vals)
    signs = "".join("+" if v > 0 else "-" if v < 0 else "0" for v in vals)
    spread = shape_spread(refine["rows"])
    print(f"H={refine['H']:.2f}  beta={args.refine_beta:.1f}  NL={refine['NL']}  x_src={refine['x_src']:.3f}")
    print(f"kubo={ [round(v, 6) for v in vals] }")
    print(f"slope={slope:+.4f}  R²={r2:.4f}  signs={signs}  1/b spread={spread:.2%}")


if __name__ == "__main__":
    main()
