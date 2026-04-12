#!/usr/bin/env python3
"""
Irregular Endogenous Sign Observable Probe
===========================================

Question:
  Can a genuinely different same-surface transport observable distinguish
  attractive from repulsive parity coupling on the retained irregular
  bipartite families, after the shell-packet family/size portability checks
  failed?

This probe stays on the same low-screening irregular surface and keeps the
packet family fixed. It replaces the density-style readout with transport:

  1. signed inward boundary current across BFS cuts
  2. time-integrated impulse of that same boundary current

Observable design:
  - same graphs, same source placement rule, same packet, same G
  - compare self-consistent parity runs with +Phi and -Phi
  - use a graph-center shell packet with outward shell phase
  - score only transport observables, not another packet-family sweep

Positive margins mean attraction produces more inward transport than
repulsion on the same surface.
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
SIG_DEPTH = 1.2
K_SHELL = 0.7
WINDOW_START = 2
WINDOW_STOP = 11
G_VALUES = (5.0, 10.0)
SEEDS = tuple(range(42, 47))
BORDER_CUTS = (1, 2)


@dataclass(frozen=True)
class Row:
    family: str
    seed: int
    g: float
    cut1_margin: float
    cut2_margin: float
    impulse_margin: float
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


def _shell_packet(depth):
    psi = np.exp(-0.5 * (depth**2) / (SIG_DEPTH**2)) * np.exp(1j * K_SHELL * depth)
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    return psi / np.linalg.norm(psi)


def _boundary_current(adj, depth, psi, H, k):
    """
    Signed inward current across the cut between BFS depth <= k and > k.

    Positive means transport toward the source center.
    """

    total = 0.0
    for i, nbs in adj.items():
        di = depth[i]
        if not np.isfinite(di):
            continue
        for j in nbs:
            if i >= j:
                continue
            dj = depth[j]
            if not np.isfinite(dj) or di == dj:
                continue
            if not ((di <= k < dj) or (dj <= k < di)):
                continue
            J = 2.0 * np.imag(np.conj(psi[i]) * H[i, j] * psi[j])
            total += J if dj < di else -J
    return float(total)


def _trace_transport(pos, colors, adj, n, L, depth, g, phi_sign):
    psi = _shell_packet(depth)
    cut1 = []
    cut2 = []
    impulse1 = 0.0
    impulse2 = 0.0
    for step in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = _solve_phi(L, n, g * rho)
        H = _build_H(pos, colors, adj, n, phi, phi_sign)
        psi = _cn_step(H, psi)
        c1 = _boundary_current(adj, depth, psi, H, BORDER_CUTS[0])
        c2 = _boundary_current(adj, depth, psi, H, BORDER_CUTS[1])
        cut1.append(c1)
        cut2.append(c2)
        if WINDOW_START <= step < WINDOW_STOP:
            impulse1 += c1 * DT
            impulse2 += c2 * DT
    return (
        np.array(cut1, dtype=float),
        np.array(cut2, dtype=float),
        float(impulse1),
        float(impulse2),
        float(np.linalg.norm(psi)),
    )


def _family_rows(builder, **kwargs):
    rows = []
    for seed in SEEDS:
        name, pos, colors, adj, n, _ = builder(seed=seed, **kwargs)
        center, depth = _graph_center(adj, n)
        L = _laplacian(pos, adj, n)
        for g in G_VALUES:
            attr_c1, attr_c2, attr_imp1, attr_imp2, attr_norm = _trace_transport(
                pos, colors, adj, n, L, depth, g, +1.0
            )
            rep_c1, rep_c2, rep_imp1, rep_imp2, rep_norm = _trace_transport(
                pos, colors, adj, n, L, depth, g, -1.0
            )
            rows.append(
                Row(
                    family=name,
                    seed=seed,
                    g=g,
                    cut1_margin=float(
                        np.mean(attr_c1[WINDOW_START:WINDOW_STOP])
                        - np.mean(rep_c1[WINDOW_START:WINDOW_STOP])
                    ),
                    cut2_margin=float(
                        np.mean(attr_c2[WINDOW_START:WINDOW_STOP])
                        - np.mean(rep_c2[WINDOW_START:WINDOW_STOP])
                    ),
                    impulse_margin=float(attr_imp1 - rep_imp1),
                    norm_attr=attr_norm,
                    norm_rep=rep_norm,
                )
            )
        print(
            f"[center] {name:16s} seed={seed} center={center} "
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
            for metric in ("cut1_margin", "cut2_margin", "impulse_margin"):
                hits, total, mean, min_v = _summarize(sub, metric)
                print(
                    f"  G={g:>4.1f} {metric:>13s}: "
                    f"pos={hits}/{total} mean={mean:+.4e} min={min_v:+.4e}"
                )


def main():
    t0 = time.time()
    print("=" * 92)
    print("IRREGULAR ENDOGENOUS SIGN OBSERVABLE PROBE")
    print("=" * 92)
    print("Same-surface parity comparison: +Phi vs -Phi")
    print("Surface: low-screening mu2=0.001")
    print("Packet family: shell phase packet")
    print(
        "Observables: inward boundary current across BFS cuts k=1,2 and "
        "time-integrated impulse"
    )
    print(f"Window: steps [{WINDOW_START}, {WINDOW_STOP})  N_STEPS={N_STEPS}")
    print()

    rows = []
    rows.extend(_family_rows(make_random_geometric, side=8))
    rows.extend(_family_rows(make_growing, n_target=64))
    rows.extend(_family_rows(make_layered_cycle, layers=8, width=8))

    _print_by_family(rows)

    print("\nGLOBAL SUMMARY")
    print("-" * 92)
    for metric in ("cut1_margin", "cut2_margin", "impulse_margin"):
        hits, total, mean, min_v = _summarize(rows, metric)
        print(f"{metric:>13s}: pos={hits}/{total} mean={mean:+.4e} min={min_v:+.4e}")

    max_norm_drift = max(
        max(abs(r.norm_attr - 1.0), abs(r.norm_rep - 1.0))
        for r in rows
    )
    print(f"\nmax_norm_drift = {max_norm_drift:.3e}")

    cut1_hits, total, _, _ = _summarize(rows, "cut1_margin")
    cut2_hits, _, _, _ = _summarize(rows, "cut2_margin")
    imp_hits, _, _, _ = _summarize(rows, "impulse_margin")
    print("\nVERDICT")
    print("-" * 92)
    if cut1_hits == total and cut2_hits == total and imp_hits == total:
        print(
            "Transport closes the same-surface irregular sign lane on the audited "
            "shell-packet surface:"
        )
        print(
            "attraction produces more inward boundary current and larger inward "
            "impulse than repulsion on every audited family/seed/G row."
        )
        print(
            "This is stronger than the earlier density-margin closure because it "
            "uses a transport observable on the same surface."
        )
    else:
        print(
            "Transport does not close the irregular sign lane on the audited "
            "shell-packet surface."
        )
        print(
            "The new boundary-current observable is cleaner than the density "
            "margins, but at least one row still fails to separate +Phi from -Phi."
        )

    print(f"\nDone in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
