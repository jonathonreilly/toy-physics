#!/usr/bin/env python3
"""Smart-prune emergence with a true adaptive baseline.

This local version fixes two review issues from the merged remote script:

1. The adaptive-quantile baseline is distinct from the D/degree reranking.
2. The pruning helper recomputes graph-dependent scores on each iteration
   through the shared control-audit implementation.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.smart_prune_control_audit import (  # type: ignore  # noqa: E402
    N_SEEDS,
    gen_3d,
    _measure_decoherence,
    _smart_prune,
)


N_LAYERS_LIST = [30, 40, 50, 60, 80]


def main() -> None:
    print("=" * 70)
    print("SMART PRUNING: adaptive baseline vs D/degree reranking")
    print("=" * 70)
    print()

    for label, prune_kwargs in [
        ("Uniform baseline", None),
        ("Adaptive quantile q=0.10 (PR #7 baseline)", {"quantile": 0.10, "protect_det_neighbors": False, "use_degree": False}),
        ("Smart prune q=0.10 (D/degree scoring)", {"quantile": 0.10, "protect_det_neighbors": False, "use_degree": True}),
        ("Smart prune q=0.10 + det protection", {"quantile": 0.10, "protect_det_neighbors": True, "use_degree": False}),
    ]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'removed':>8s}  {'n':>3s}")
        print(f"  {'-' * 28}")

        for nl in N_LAYERS_LIST:
            purs = []
            removals = []
            for seed in range(N_SEEDS):
                positions, adj, layers = gen_3d(n_layers=nl, rng_seed=seed * 13 + 5)
                if prune_kwargs is None:
                    adj_e = adj
                    removed = 0
                else:
                    adj_e, removed = _smart_prune(positions, adj, layers, **prune_kwargs)
                removals.append(removed)
                pur = _measure_decoherence(positions, adj_e, layers)
                if pur == pur:
                    purs.append(pur)

            if purs:
                print(f"  {nl:4d}  {sum(purs)/len(purs):8.4f}  {sum(removals)/len(removals):8.1f}  {len(purs):3d}")
            else:
                print(f"  {nl:4d}  FAIL")
        print()

    print("=" * 70)
    print("KEY: compare true adaptive quantile against D/degree reranking")
    print("=" * 70)


if __name__ == "__main__":
    main()
