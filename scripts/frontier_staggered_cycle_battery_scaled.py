#!/usr/bin/env python3
"""
Staggered Fermion Cycle-Bearing Graph Battery, Scaled
======================================================

Retained larger-size sibling of the cycle-bearing battery.

Semantics are inherited from frontier_staggered_cycle_battery.py:
  - B1 zero-source control
  - B2 source-response linearity
  - B3 two-body additivity
  - B4 force sign
  - B5 iterative stability
  - B6 norm conservation
  - B7 state-family robustness
  - B8 native gauge closure
  - B9 force-gap characterization + shell/spectral diagnostics

The only change is the admitted graph size sweep. This probe freezes the
larger-graph claim honestly on the same admissible cycle-bearing bipartite
families:
  - random geometric, side = 8 / 10 / 12
  - growing, n_target = side^2
  - layered cycle, layers = side and width = side

No row semantics are silently changed.
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parents[1]
BASE_PATH = ROOT / "scripts" / "frontier_staggered_cycle_battery.py"


def _load_base():
    spec = importlib.util.spec_from_file_location("frontier_staggered_cycle_battery_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base harness from {BASE_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


base = _load_base()


def make_random_geometric_scaled(seed: int, side: int):
    return base.make_random_geometric(seed=seed, side=side)


def make_growing_scaled(seed: int, side: int):
    return base.make_growing(seed=seed, n_target=side * side)


def make_layered_cycle_scaled(seed: int, side: int):
    return base.make_layered_cycle(seed=seed, layers=side, width=side)


def main():
    t0 = time.time()
    print("=" * 78)
    print("STAGGERED FERMION - CYCLE-BEARING GRAPH BATTERY, SCALED")
    print("=" * 78)
    print(f"Semantic base: frontier_staggered_cycle_battery.py")
    print("Scale sweep: side = 8, 10, 12")
    print("Families: random geometric, growing, layered cycle")
    print("Force is the primary gravity observable. No centroid. No 1D ring.")
    print()

    scores = []
    for side in (8, 10, 12):
        families = [
            make_random_geometric_scaled(seed=42, side=side),
            make_growing_scaled(seed=42, side=side),
            make_layered_cycle_scaled(seed=42, side=side),
        ]
        print(f"\n{'=' * 78}")
        print(f"SIZE CASE: side={side}")
        print(f"{'=' * 78}")
        for g in families:
            if g is None:
                print("  REJECTED: graph construction failed")
                continue
            if base._has_odd_cycle(g.adj, g.colors):
                print(f"  REJECTED: {g.name} has odd-cycle defect")
                continue
            score = base.run_battery(g)
            if score is not None:
                scores.append((side, g.name, score))

    print(f"\n{'=' * 78}")
    print("SUMMARY")
    print(f"{'=' * 78}")
    for side, name, score in scores:
        print(f"{side:>2d}  {name:<24s}  {score}/9")
    print(f"Families tested: {len(scores)}")
    print(f"Time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
