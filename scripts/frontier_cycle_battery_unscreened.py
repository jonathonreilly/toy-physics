#!/usr/bin/env python3
"""
Cycle Battery Unscreened: Retarded Family Closure at mu^2 = 0.001
=================================================================
Re-runs the SAME 9-row battery from frontier_two_field_retarded_family_closure.py
but with mu^2 = 0.001 (screening length ~31.6 sites) instead of mu^2 = 0.22
(screening length ~2.1 sites).

Purpose: verify that the 9/9 scores are not artifacts of heavy screening
that suppresses long-range field structure before it can reveal failures.

The field operator is:
  (L + mu^2 I) Phi = G * rho
so mu^2 -> 0 removes the Yukawa cutoff and lets the Poisson/wave kernel
extend across the full graph diameter.

Everything else is identical to the original family closure battery.
"""

from __future__ import annotations

import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Import and patch MU2 BEFORE importing the family closure module,
# because the closure module reads base.MU2 at import time.
import frontier_two_field_retarded_probe as base

ORIGINAL_MU2 = base.MU2
UNSCREENED_MU2 = 0.001

# Patch the base module constant
base.MU2 = UNSCREENED_MU2

# Now import the family closure module (it reads base.MU2 at import)
import frontier_two_field_retarded_family_closure as closure

# Also patch the closure module's own copy
closure.MU2 = UNSCREENED_MU2


def main() -> None:
    t0 = time.time()
    print("=" * 70)
    print("UNSCREENED CYCLE BATTERY: RETARDED/HYBRID FAMILY CLOSURE")
    print(f"mu^2 = {UNSCREENED_MU2} (screening length = {1.0 / UNSCREENED_MU2**0.5:.1f} sites)")
    print(f"Original mu^2 = {ORIGINAL_MU2} (screening length = {1.0 / ORIGINAL_MU2**0.5:.1f} sites)")
    print("=" * 70)
    print(
        f"DT_MATTER={base.DT_MATTER}, DT_FIELD={base.DT_FIELD}, MASS={base.MASS}, "
        f"MU2={base.MU2}, "
        f"FIELD_C={base.FIELD_C}, FIELD_GAMMA={base.FIELD_GAMMA}, "
        f"FIELD_BETA={base.FIELD_BETA}, "
        f"FIELD_TAU_MEM={base.FIELD_TAU_MEM}, FIELD_LAG_BLEND={base.FIELD_LAG_BLEND}"
    )
    print(
        f"family closure: iters={closure.FAMILY_CLOSURE_ITERS}, "
        f"seed_mix={closure.FAMILY_SEED_MIX:.2f}, "
        f"sharpen={closure.FAMILY_SHARPEN:.2f}, "
        f"relax={closure.FAMILY_RELAX:.2f}, "
        f"capture_exp={closure.FAMILY_CAPTURE_EXP:.2f}"
    )
    print("Graph families: random geometric, growing, layered cycle, causal DAG.")
    print()

    scores = []
    family_names = []
    for builder in (base.make_random_geometric, base.make_growing, base.make_layered_cycle, base.make_causal_dag):
        graph = builder()
        if graph is None:
            print("  REJECTED: graph construction failed.")
            continue
        if base._has_odd_cycle(graph.adj, graph.colors):
            print(f"  REJECTED: {graph.name} has odd-cycle defect.")
            continue
        graph = closure._retained_source_graph(graph)
        family_names.append(graph.name)
        scores.append(closure._run_battery(graph))

    print(f"\n{'=' * 70}")
    print("SCORECARD")
    print(f"{'=' * 70}")
    for name, score in zip(family_names, scores):
        print(f"  {name:20s}: {score}/9")
    total = sum(scores)
    possible = 9 * len(scores)
    print(f"\n  TOTAL: {total}/{possible}")
    print(f"\n  Original (mu^2={ORIGINAL_MU2}): expected 9/9 per family")
    print(f"  This run (mu^2={UNSCREENED_MU2}): see above")
    if total < possible:
        print(f"\n  WARNING: {possible - total} gate(s) lost when screening removed.")
        print("  This suggests the original result may partly depend on screening.")
    else:
        print("\n  All gates held. Result is NOT a screening artifact.")
    print(f"\nTime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
