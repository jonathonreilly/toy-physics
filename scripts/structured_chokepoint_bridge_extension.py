#!/usr/bin/env python3
"""Structured chokepoint bridge extension.

This is a narrow follow-up to the retained structured chokepoint bridge.
It keeps the canonical mirror readout fixed and only asks whether the same
structured placement pocket survives at larger layer counts.

The key constraint is that this is not a new generator search:

  - same structured mirror-symmetric placement family
  - same layer-1 chokepoint connectivity
  - same canonical linear readout from mirror_chokepoint_joint

The only thing that widens is the tested layer count.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import mirror_chokepoint_joint as canonical
from scripts.structured_chokepoint_bridge import (
    generate_structured_chokepoint_dag,
    run_narrow_probe,
)


def _fmt(mean: float, se: float) -> str:
    if math.isnan(mean):
        return "nan"
    return f"{mean:.4f}±{se:.2f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[60, 80, 100])
    parser.add_argument("--npl-half", type=int, default=canonical.NPL_HALF)
    parser.add_argument("--grid-spacing", type=float, default=1.0)
    parser.add_argument("--connect-radius", type=float, default=3.5)
    parser.add_argument("--layer-jitter", type=float, default=0.25)
    parser.add_argument("--n-seeds", type=int, default=canonical.N_SEEDS)
    args = parser.parse_args()

    print("=" * 110)
    print("STRUCTURED CHOKEPOINT BRIDGE EXTENSION")
    print("  canonical mirror readout fixed; only layer count is widened")
    print(
        f"  NPL_HALF={args.npl_half}, seeds={args.n_seeds}, "
        f"grid_spacing={args.grid_spacing}, connect_radius={args.connect_radius}, "
        f"layer_jitter={args.layer_jitter}"
    )
    print("=" * 110)
    print()
    print(
        f"  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>12s}  {'S_norm':>8s}  "
        f"{'gravity':>12s}  {'Born':>12s}  {'k=0':>12s}  {'ok':>3s}  {'time':>5s}"
    )
    print(f"  {'-' * 98}")

    widened = False

    for nl in args.n_layers:
        t0 = time.time()
        r = run_narrow_probe(
            n_layers=nl,
            npl_half=args.npl_half,
            grid_spacing=args.grid_spacing,
            connect_radius=args.connect_radius,
            layer_jitter=args.layer_jitter,
            n_seeds=args.n_seeds,
        )
        dt = time.time() - t0
        if r["n_ok"] <= 0:
            print(f"  {nl:4d}  FAIL  {dt:4.0f}s")
            continue

        mdtv, sdtv = r["dtv"]
        mpur, spur = r["pur"]
        msn, ssn = r["sn"]
        mg, sg = r["grav"]
        mborn, sborn = r["born"]
        mk0, sk0 = r["k0"]
        born_str = _fmt(mborn, sborn)
        print(
            f"  {nl:4d}  {mdtv:8.4f}  {_fmt(mpur, spur):>12s}  {msn:8.4f}  "
            f"{mg:+8.4f}±{sg:.3f}  {born_str:>12s}  {mk0:+8.2e}  "
            f"{r['n_ok']:3d}  {dt:4.0f}s"
        )

        if nl > 60:
            if mg > 0 and abs(mk0) < 1e-6 and not math.isnan(mborn):
                widened = True

    print()
    print("READ:")
    if widened:
        print("  The structured bridge widens beyond the current narrow slice on the")
        print("  tested larger-N rows while keeping the canonical mirror readout fixed.")
    else:
        print("  The structured bridge remains narrow on the tested larger-N rows.")
    print("  This is still a bounded bridge pocket, not a new generator family.")


if __name__ == "__main__":
    main()
