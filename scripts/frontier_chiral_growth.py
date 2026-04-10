#!/usr/bin/env python3
"""Amplitude-guided chiral growth / pruning diagnostic.

This is a narrow growth test for the local 1D chiral walk:
  - propagate one layer at a time
  - keep only sites whose layer probability exceeds a relative threshold
  - compare an asymmetric source (pure + chirality) against a symmetric source

The point is to see whether threshold pruning causes the walk to collapse
because of source chirality bias rather than because the architecture cannot
support any nontrivial grown graph.
"""

from __future__ import annotations

import math

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


N_Y = 41
N_LAYERS = 24
THETA0 = 0.30
SOURCE_Y = 20
REL_THRESH = 0.05


def step(psi: np.ndarray) -> np.ndarray:
    n_y = len(psi) // 2
    for y in range(n_y):
        idx_p = 2 * y
        idx_m = 2 * y + 1
        pp, pm = psi[idx_p], psi[idx_m]
        c = math.cos(THETA0)
        s = math.sin(THETA0)
        psi[idx_p] = c * pp - s * pm
        psi[idx_m] = s * pp + c * pm

    new_psi = np.zeros_like(psi)
    for y in range(n_y):
        idx_p = 2 * y
        idx_m = 2 * y + 1
        if y + 1 < n_y:
            new_psi[2 * (y + 1)] += psi[idx_p]
        else:
            new_psi[idx_m] += psi[idx_p]
        if y - 1 >= 0:
            new_psi[2 * (y - 1) + 1] += psi[idx_m]
        else:
            new_psi[idx_p] += psi[idx_m]
    return new_psi


def layer_probs(psi: np.ndarray) -> np.ndarray:
    n_y = len(psi) // 2
    probs = np.zeros(n_y, dtype=float)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def run_growth(symmetric_source: bool) -> list[int]:
    psi = np.zeros(2 * N_Y, dtype=complex)
    if symmetric_source:
        psi[2 * SOURCE_Y] = 1.0 / math.sqrt(2.0)
        psi[2 * SOURCE_Y + 1] = 1.0 / math.sqrt(2.0)
    else:
        psi[2 * SOURCE_Y] = 1.0

    active_counts = []
    for _ in range(N_LAYERS):
        psi = step(psi)
        probs = layer_probs(psi)
        p_max = float(np.max(probs))
        if p_max > 0:
            keep = probs >= REL_THRESH * p_max
            for y, keep_y in enumerate(keep):
                if not keep_y:
                    psi[2 * y] = 0.0
                    psi[2 * y + 1] = 0.0
        active_counts.append(int(np.count_nonzero(layer_probs(psi) > 1e-15)))
    return active_counts


def main() -> None:
    print("FRONTIER: CHIRAL GROWTH / PRUNING")
    print(f"Grid width={N_Y}, layers={N_LAYERS}, relative threshold={REL_THRESH:.2f}")
    print(f"Source y={SOURCE_Y}")
    print()

    asym = run_growth(symmetric_source=False)
    sym = run_growth(symmetric_source=True)

    print("Asymmetric source (pure + chirality):")
    print(f"  active nodes by layer: {asym}")
    print(f"  final active count: {asym[-1]}")
    print()
    print("Symmetric source (equal + and -):")
    print(f"  active nodes by layer: {sym}")
    print(f"  final active count: {sym[-1]}")
    print()

    asym_collapse = asym[-1] <= 2
    sym_better = sym[-1] > asym[-1]
    print("Interpretation:")
    if asym_collapse:
        print("  - asymmetric source degenerates under threshold pruning")
    else:
        print("  - asymmetric source remains nontrivial")
    if sym_better:
        print("  - symmetric initialization mitigates the pruning collapse")
    else:
        print("  - symmetric initialization does not materially improve the pruning behavior")


if __name__ == "__main__":
    main()
