#!/usr/bin/env python3
"""Simple bipartition entropy probe on the retained staggered self-gravity lane.

The observable here is intentionally minimal: for a single-particle state on a
graph and a bipartition A|B, the subsystem occupancy entropy is

    S(A) = -p_A log(p_A) - (1-p_A) log(1-p_A),

where p_A is the probability mass in A.

This is not a many-body area-law entropy. The purpose of the probe is to test
whether this simple retained observable shows any boundary-controlled signal on
the self-gravity lane, or whether it is dominated by localization / mass split.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass
from typing import Callable

import numpy as np

from frontier_staggered_self_gravity import (
    DT,
    G_SELF,
    MASS,
    MU2,
    N_ITER,
    _bfs,
    _build_H,
    _cn_step,
    _gauss_state,
    _laplacian,
    _solve_phi,
    make_growing,
    make_layered_cycle,
    make_random_geometric,
)


Builder = Callable[[], tuple[str, np.ndarray, np.ndarray, dict[int, list[int]], int, int]]


@dataclass
class PartitionStats:
    label: str
    size_a: int
    frac_a: float
    boundary: int
    p_free: float
    s_free: float
    p_self: float
    s_self: float


@dataclass
class EnsembleStats:
    n_samples: int
    boundary_min: int
    boundary_max: int
    s_min: float
    s_max: float
    corr_boundary_s: float


def binary_entropy(prob_a: float) -> float:
    p = min(max(float(prob_a), 1.0e-15), 1.0 - 1.0e-15)
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def edge_boundary(adj: dict[int, list[int]], set_a: set[int]) -> int:
    count = 0
    for i in set_a:
        for j in adj.get(i, []):
            if j not in set_a:
                count += 1
    return count


def partition_x_half(pos: np.ndarray) -> np.ndarray:
    order = np.argsort(pos[:, 0], kind="mergesort")
    mask = np.zeros(len(pos), dtype=bool)
    mask[order[: len(pos) // 2]] = True
    return mask


def partition_depth_half(adj: dict[int, list[int]], src: int, n: int) -> np.ndarray:
    depth = _bfs(adj, src, n)
    finite = depth[np.isfinite(depth)]
    cut = np.median(finite)
    mask = depth <= cut
    if mask.sum() > n // 2:
        # Trim the furthest nodes at the cut depth to keep the split balanced.
        on_cut = np.where(np.isclose(depth, cut))[0]
        extra = int(mask.sum() - n // 2)
        if extra > 0:
            for idx in on_cut[::-1][:extra]:
                mask[idx] = False
    elif mask.sum() < n // 2:
        on_cut = np.where(np.isclose(depth, cut))[0]
        need = int(n // 2 - mask.sum())
        for idx in on_cut[:need]:
            mask[idx] = True
    return mask


def partition_random_half(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    mask = np.zeros(n, dtype=bool)
    mask[perm[: n // 2]] = True
    return mask


def evolve_pair(
    pos: np.ndarray,
    col: np.ndarray,
    adj: dict[int, list[int]],
    n: int,
    src: int,
) -> tuple[np.ndarray, np.ndarray]:
    lap = _laplacian(pos, adj, n)
    psi_self = _gauss_state(pos, src)
    psi_free = psi_self.copy()
    h_free = _build_H(pos, col, adj, n, MASS, np.zeros(n))
    for _ in range(N_ITER):
        rho = np.abs(psi_self) ** 2
        phi = _solve_phi(lap, n, G_SELF * rho)
        h_self = _build_H(pos, col, adj, n, MASS, phi)
        psi_self = _cn_step(h_self, n, psi_self)
        psi_free = _cn_step(h_free, n, psi_free)
    return psi_self, psi_free


def partition_stats(
    label: str,
    mask_a: np.ndarray,
    adj: dict[int, list[int]],
    psi_self: np.ndarray,
    psi_free: np.ndarray,
) -> PartitionStats:
    set_a = set(np.nonzero(mask_a)[0].tolist())
    p_self = float(np.sum(np.abs(psi_self[mask_a]) ** 2))
    p_free = float(np.sum(np.abs(psi_free[mask_a]) ** 2))
    return PartitionStats(
        label=label,
        size_a=int(mask_a.sum()),
        frac_a=float(mask_a.mean()),
        boundary=edge_boundary(adj, set_a),
        p_free=p_free,
        s_free=binary_entropy(p_free),
        p_self=p_self,
        s_self=binary_entropy(p_self),
    )


def random_half_ensemble(
    n: int,
    adj: dict[int, list[int]],
    psi_self: np.ndarray,
    n_samples: int = 32,
) -> EnsembleStats:
    boundaries: list[int] = []
    entropies: list[float] = []
    for seed in range(n_samples):
        mask = partition_random_half(n, seed)
        set_a = set(np.nonzero(mask)[0].tolist())
        p_self = float(np.sum(np.abs(psi_self[mask]) ** 2))
        boundaries.append(edge_boundary(adj, set_a))
        entropies.append(binary_entropy(p_self))
    b = np.array(boundaries, dtype=float)
    s = np.array(entropies, dtype=float)
    corr = 0.0
    if np.std(b) > 0 and np.std(s) > 0:
        corr = float(np.corrcoef(b, s)[0, 1])
    return EnsembleStats(
        n_samples=n_samples,
        boundary_min=int(np.min(b)),
        boundary_max=int(np.max(b)),
        s_min=float(np.min(s)),
        s_max=float(np.max(s)),
        corr_boundary_s=corr,
    )


def summarize_case(builder: Builder) -> tuple[str, list[PartitionStats], dict[str, float], EnsembleStats]:
    name, pos, col, adj, n, src = builder()
    psi_self, psi_free = evolve_pair(pos, col, adj, n, src)
    stats = [
        partition_stats("x_half", partition_x_half(pos), adj, psi_self, psi_free),
        partition_stats("depth_half", partition_depth_half(adj, src, n), adj, psi_self, psi_free),
        partition_stats("random_half", partition_random_half(n, 7), adj, psi_self, psi_free),
    ]
    boundaries = np.array([s.boundary for s in stats], dtype=float)
    ent_self = np.array([s.s_self for s in stats], dtype=float)
    corr = 0.0
    if np.std(boundaries) > 0 and np.std(ent_self) > 0:
        corr = float(np.corrcoef(boundaries, ent_self)[0, 1])
    ensemble = random_half_ensemble(n, adj, psi_self)
    summary = {
        "n": float(n),
        "boundary_min": float(boundaries.min()),
        "boundary_max": float(boundaries.max()),
        "s_self_min": float(ent_self.min()),
        "s_self_max": float(ent_self.max()),
        "corr_boundary_s": corr,
        "delta_s_mean": float(np.mean([s.s_self - s.s_free for s in stats])),
        "delta_s_max": float(np.max([s.s_self - s.s_free for s in stats])),
    }
    return name, stats, summary, ensemble


def main() -> None:
    t0 = time.time()
    print("=" * 78)
    print("SELF-GRAVITY BIPARTITION ENTROPY PROBE")
    print("=" * 78)
    print(f"Retained operating point: MASS={MASS}, MU2={MU2}, DT={DT}, G_SELF={G_SELF}, N_ITER={N_ITER}")
    print("Observable: single-particle bipartition entropy S(A) = -p_A log p_A - p_B log p_B")
    print("Goal: test whether simple entropy tracks boundary size or merely occupancy split.\n")

    builders: list[Builder] = [
        lambda: make_random_geometric(seed=42, side=6),
        lambda: make_growing(seed=42, n_target=48),
        lambda: make_layered_cycle(seed=42, layers=6, width=4),
    ]

    family_results: list[tuple[str, list[PartitionStats], dict[str, float], EnsembleStats]] = []
    for builder in builders:
        family_results.append(summarize_case(builder))

    print("Per-family partitions")
    print("-" * 78)
    for name, stats, summary, ensemble in family_results:
        print(f"\n{name}: n={int(summary['n'])}")
        print("  cut          |A|/n  boundary   p_free   S_free   p_self   S_self   dS")
        for s in stats:
            print(
                f"  {s.label:11s}"
                f" {s.frac_a:5.2f}"
                f" {s.boundary:9d}"
                f" {s.p_free:8.4f}"
                f" {s.s_free:8.4f}"
                f" {s.p_self:8.4f}"
                f" {s.s_self:8.4f}"
                f" {s.s_self - s.s_free:+8.4f}"
            )
        print(
            "  summary:"
            f" boundary[{summary['boundary_min']:.0f},{summary['boundary_max']:.0f}]"
            f" S_self[{summary['s_self_min']:.4f},{summary['s_self_max']:.4f}]"
            f" corr(boundary,S_self)={summary['corr_boundary_s']:+.3f}"
            f" mean_dS={summary['delta_s_mean']:+.4f}"
        )
        print(
            "  random-half ensemble:"
            f" samples={ensemble.n_samples}"
            f" boundary[{ensemble.boundary_min},{ensemble.boundary_max}]"
            f" S_self[{ensemble.s_min:.4f},{ensemble.s_max:.4f}]"
            f" corr(boundary,S_self)={ensemble.corr_boundary_s:+.3f}"
        )

    print("\nReadout")
    print("-" * 78)
    all_deltas = [s.s_self - s.s_free for _, stats, _, _ in family_results for s in stats]
    all_corrs = [summary["corr_boundary_s"] for _, _, summary, _ in family_results]
    ensemble_corrs = [ensemble.corr_boundary_s for _, _, _, ensemble in family_results]
    print(f"  mean entropy shift (self - free): {np.mean(all_deltas):+.4f}")
    print(f"  max entropy shift  (self - free): {np.max(all_deltas):+.4f}")
    print(f"  boundary correlations by family:  {', '.join(f'{c:+.3f}' for c in all_corrs)}")
    print(f"  random-half ensemble corrs:      {', '.join(f'{c:+.3f}' for c in ensemble_corrs)}")
    if all(abs(c) < 0.4 for c in ensemble_corrs):
        print("  verdict: no robust area-law-like boundary control in this simple single-particle observable")
    else:
        print("  verdict: some boundary sensitivity appears, but inspect ensemble controls before calling it area-law-like")
    print("\nInterpretation:")
    print("  - This observable is bounded by ln(2) and is controlled primarily by subsystem occupancy p_A.")
    print("  - A strong area-law claim would require boundary-driven growth beyond this binary occupancy ceiling.")
    print("  - Any signal here should be treated as exploratory unless it survives many-body or multi-orbital generalization.")
    print(f"\nTime: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
