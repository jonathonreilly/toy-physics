#!/usr/bin/env python3
"""
Irregular Endogenous Sign Third-Family Discriminator
====================================================

Question:
  Does a genuinely independent annulus packet preserve the same-surface sign
  separator on the retained irregular bipartite families at low screening?

This is the third-family follow-up called for by the review queue after:
  - the original shell-packet closure result
  - the core-gaussian reinforcement run
  - the size-portability sweep

Design:
  - same graphs, same source placement rule, same sign readout
  - same low-screening surface (mu2 = 0.001)
  - same early-time window
  - one genuinely independent packet family only: annulus

The annulus packet is graph-native once the graph is fixed:
  psi_0(d) ~ exp(-(d - r0)^2 / (2 sigma_r^2))
where d is BFS depth from the graph center.

The point of the run is not to tune a better packet. It is to check whether
the sign separator survives a third independent initial condition.
"""

from __future__ import annotations

import math
import time
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from frontier_staggered_self_gravity import (
    make_growing,
    make_layered_cycle,
    make_random_geometric,
)


MASS = 0.30
MU2 = 0.001
DT = 0.12
N_STEPS = 15
ANNULUS_R0 = 3.0
ANNULUS_SIGMA = 1.0
WINDOW_START = 2
WINDOW_STOP = 11
G_VALUES = (5.0, 10.0)
SEEDS = tuple(range(42, 47))


@dataclass(frozen=True)
class Row:
    family: str
    seed: int
    g: float
    ball1_margin: float
    ball2_margin: float
    depth_margin: float
    norm_attr: float
    norm_rep: float


def _bfs_depth(adj, src, n):
    depth = np.full(n, np.inf)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                q.append(j)
    return depth


def _graph_center(adj, n):
    best = None
    for src in range(n):
        depth = _bfs_depth(adj, src, n)
        finite = depth[np.isfinite(depth)]
        ecc = float(np.max(finite)) if finite.size else np.inf
        mean = float(np.mean(finite)) if finite.size else np.inf
        score = (ecc, mean, src)
        if best is None or score < best[0]:
            best = (score, src, depth)
    return best[1], best[2]


def _laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def _solve_phi(L, n, rho):
    A = (L + MU2 * speye(n, format="csr")).tocsc()
    return spsolve(A, rho)


def _build_H(pos, colors, adj, n, phi, phi_sign):
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(colors == 0, 1.0, -1.0)
    H.setdiag((MASS + phi_sign * phi) * parity)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _cn_step(H, psi):
    n = H.shape[0]
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def _annulus_packet(depth):
    psi = np.exp(-0.5 * ((depth - ANNULUS_R0) ** 2) / (ANNULUS_SIGMA ** 2))
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    return psi / np.linalg.norm(psi)


def _capture(depth, psi, k):
    rho = np.abs(psi) ** 2
    return float(np.sum(rho[depth <= k]))


def _mean_depth(depth, psi):
    rho = np.abs(psi) ** 2
    rho /= max(np.sum(rho), 1e-30)
    finite = np.isfinite(depth)
    return float(np.sum(rho[finite] * depth[finite]))


def _trace_observables(pos, colors, adj, n, L, depth, g, phi_sign):
    psi = _annulus_packet(depth)
    ball1 = []
    ball2 = []
    mean_depth = []
    for _ in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = _solve_phi(L, n, g * rho)
        H = _build_H(pos, colors, adj, n, phi, phi_sign)
        psi = _cn_step(H, psi)
        ball1.append(_capture(depth, psi, 1))
        ball2.append(_capture(depth, psi, 2))
        mean_depth.append(_mean_depth(depth, psi))
    return np.array(ball1), np.array(ball2), np.array(mean_depth), float(np.linalg.norm(psi))


def _family_rows(builder, **kwargs):
    rows = []
    for seed in SEEDS:
        name, pos, colors, adj, n, _ = builder(seed=seed, **kwargs)
        center, depth = _graph_center(adj, n)
        L = _laplacian(pos, adj, n)
        for g in G_VALUES:
            attr_b1, attr_b2, attr_d, attr_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, +1.0
            )
            rep_b1, rep_b2, rep_d, rep_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, -1.0
            )
            rows.append(
                Row(
                    family=name,
                    seed=seed,
                    g=g,
                    ball1_margin=float(
                        np.mean(attr_b1[WINDOW_START:WINDOW_STOP])
                        - np.mean(rep_b1[WINDOW_START:WINDOW_STOP])
                    ),
                    ball2_margin=float(
                        np.mean(attr_b2[WINDOW_START:WINDOW_STOP])
                        - np.mean(rep_b2[WINDOW_START:WINDOW_STOP])
                    ),
                    depth_margin=float(
                        np.mean(rep_d[WINDOW_START:WINDOW_STOP])
                        - np.mean(attr_d[WINDOW_START:WINDOW_STOP])
                    ),
                    norm_attr=attr_norm,
                    norm_rep=rep_norm,
                )
            )
        print(
            f"[center] family={name:16s} seed={seed} center={center} "
            f"max_depth={int(np.max(depth[np.isfinite(depth)]))}"
        )
    return rows


def _summarize(rows, metric):
    vals = np.array([getattr(r, metric) for r in rows], dtype=float)
    return int(np.sum(vals > 0)), len(vals), float(np.mean(vals)), float(np.min(vals))


def _print_by_family(rows):
    print("\nPER-FAMILY SUMMARY")
    print("-" * 92)
    for family in ("random_geometric", "growing", "layered_cycle"):
        fam_rows = [r for r in rows if r.family == family]
        print(f"\n{family}")
        for g in G_VALUES:
            sub = [r for r in fam_rows if r.g == g]
            for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
                hits, total, mean, min_v = _summarize(sub, metric)
                print(
                    f"  G={g:>4.1f} {metric:>12s}: "
                    f"pos={hits}/{total} mean={mean:+.4e} min={min_v:+.4e}"
                )


def main():
    t0 = time.time()
    print("=" * 92)
    print("IRREGULAR ENDOGENOUS SIGN THIRD-FAMILY DISCRIMINATOR")
    print("=" * 92)
    print("Same-surface parity comparison: +Phi vs -Phi")
    print("Surface: low-screening mu2=0.001")
    print("Packet family: annulus")
    print(f"Window: steps [{WINDOW_START}, {WINDOW_STOP})  N_STEPS={N_STEPS}")
    print()

    rows = []
    rows.extend(_family_rows(make_random_geometric, side=8))
    rows.extend(_family_rows(make_growing, n_target=64))
    rows.extend(_family_rows(make_layered_cycle, layers=8, width=8))

    _print_by_family(rows)

    print("\nGLOBAL SUMMARY")
    print("-" * 92)
    for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
        hits, total, mean, min_v = _summarize(rows, metric)
        print(f"{metric:>12s}: pos={hits}/{total} mean={mean:+.4e} min={min_v:+.4e}")

    max_norm_drift = max(
        max(abs(r.norm_attr - 1.0), abs(r.norm_rep - 1.0))
        for r in rows
    )
    print(f"\nmax_norm_drift = {max_norm_drift:.3e}")

    ball2_hits, total, _, _ = _summarize(rows, "ball2_margin")
    depth_hits, _, _, _ = _summarize(rows, "depth_margin")
    print("\nVERDICT")
    print("-" * 92)
    if ball2_hits == total and depth_hits == total:
        print(
            "The independent annulus family preserves the same-surface sign separator"
        )
        print(
            "across every audited irregular family/seed/G row on the low-screening surface."
        )
        print(
            "That would add real retain pressure to the irregular sign lane, but only"
        )
        print("for the audited annulus family on this surface.")
    else:
        print(
            "The independent annulus family does not close the irregular sign lane."
        )
        print(
            "The lane remains frontier-only: the shell-packet result is real, but it"
        )
        print("has not yet survived a third genuinely independent packet family.")

    print(f"\nDone in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
