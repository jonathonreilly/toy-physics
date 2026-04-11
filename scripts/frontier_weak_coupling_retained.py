#!/usr/bin/env python3
"""
Retained Weak-Coupling Sign-Sensitivity Audit
=============================================

This script hardens the exploratory weak-coupling sign-sensitivity regime into
an explicit retention audit on a broader family/size/seed surface.

Question:
  Does any graph-native observable stay sign-selective enough at weak coupling
  to be frozen as a retained result on irregular bipartite graphs?

The audit compares attractive parity coupling, repulsive parity coupling, and a
zero-field control on a shared family/size/seed surface. It measures:

  O1: width asymmetry      contraction_a / contraction_r        (want < 1)
  O2: gap ratio            gap_a / gap_r                        (want > 1)
  O3: shell separation     tw_a high, tw_r low                 (want strong split)
  O4: norm conservation    ||psi|| attract/repulse             (want ~1)

Verdict rule:
  - retained closure requires a single sign-selective observable to pass on
    every audited run
  - otherwise the regime remains exploratory, even if one observable is strong
"""

from __future__ import annotations

import math
import random
import time
from collections import deque

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh, spsolve


MASS = 0.30
MU2 = 0.22
DT = 0.12
N_ITER = 40
SEEDS = [42, 43, 44, 45, 46]
G_VALUES = [5, 10]
NORM_TOL = 1e-10
SHELL_HIGH = int(0.90 * N_ITER)
SHELL_LOW = int(0.10 * N_ITER)
SHELL_MARGIN = int(0.25 * N_ITER)


def _ae(adj: dict[int, set[int]], a: int, b: int) -> None:
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed: int = 42, side: int = 8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append(
                (x + 0.08 * (rng.random() - 0.5), y + 0.08 * (rng.random() - 0.5))
            )
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index:
                    continue
                b = index[(ii, jj)]
                if col[a] == col[b]:
                    continue
                if math.hypot(pos[b, 0] - pos[a, 0], pos[b, 1] - pos[a, 1]) <= 1.28:
                    _ae(adj, a, b)
    return "random_geometric", pos, col, {k: list(v) for k, v in adj.items()}


def make_growing(seed: int = 42, n_target: int = 64):
    rng = random.Random(seed)
    coords = [(0.0, 0.0), (1.0, 0.0)]
    colors = [0, 1]
    adj = {0: {1}, 1: {0}}
    cur = 2
    while cur < n_target:
        px = rng.uniform(-3, 3)
        py = rng.uniform(-3, 3)
        nc = cur % 2
        coords.append((px, py))
        colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = [(math.hypot(px - coords[i][0], py - coords[i][1]), i) for i in opp]
            ds.sort()
            for _, j in ds[: min(4, len(ds))]:
                _ae(adj, cur, j)
        cur += 1
    return "growing", np.array(coords), np.array(colors, dtype=int), {k: list(v) for k, v in adj.items()}


def make_layered_cycle(seed: int = 42, layers: int = 8, width: int = 8):
    rng = random.Random(seed)
    coords, colors, layer_nodes = [], [], []
    idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            coords.append((float(layer), float(k) + 0.05 * (rng.random() - 0.5)))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos % len(nxt)]
            adj[i].add(j1)
            adj[j1].add(i)
            j2 = nxt[(i_pos + 1) % len(nxt)]
            if j2 != j1:
                adj[i].add(j2)
                adj[j2].add(i)
    return "layered_cycle", pos, col, {k: list(v) for k, v in adj.items()}


def _build_laplacian(pos: np.ndarray, adj: dict[int, list[int]], n: int):
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


def _build_hamiltonian(pos: np.ndarray, col: np.ndarray, adj: dict[int, list[int]], n: int, phi: np.ndarray):
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * parity)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w
    return H.tocsr()


def _cn_step(H, psi: np.ndarray, dt: float):
    n = H.shape[0]
    a_plus = (speye(n, format="csc") + 1j * H * dt / 2).tocsc()
    a_minus = speye(n, format="csr") - 1j * H * dt / 2
    return spsolve(a_plus, a_minus.dot(psi))


def _width(psi: np.ndarray, pos: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return float(np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2))))


def _bfs_depth(adj: dict[int, list[int]], src: int, n: int):
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


def _shell_force(depth: np.ndarray, n: int, psi: np.ndarray, phi: np.ndarray) -> float:
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1)
    shell_prob = np.zeros(max_d + 1)
    shell_count = np.zeros(max_d + 1)
    for i in range(n):
        d = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d <= max_d:
            shell_phi[d] += phi[i]
            shell_prob[d] += rho_n[i]
            shell_count[d] += 1
    for d in range(max_d + 1):
        if shell_count[d] > 0:
            shell_phi[d] /= shell_count[d]
    grad = np.zeros(max_d + 1)
    for d in range(max_d + 1):
        if d == 0:
            grad[d] = shell_phi[0] - shell_phi[min(1, max_d)]
        elif d == max_d:
            grad[d] = shell_phi[d - 1] - shell_phi[d]
        else:
            grad[d] = 0.5 * (shell_phi[d - 1] - shell_phi[d + 1])
    return float(np.sum(shell_prob * grad))


def _spectral_gap(H) -> float:
    n = H.shape[0]
    try:
        evals = eigsh(H.tocsc(), k=min(6, n - 2), which="SM", return_eigenvectors=False)
        nonzero = np.abs(evals[np.abs(evals) > 1e-12])
        return float(np.min(nonzero)) if nonzero.size else float("nan")
    except Exception:
        return float("nan")


def run_case(name: str, pos: np.ndarray, col: np.ndarray, adj: dict[int, list[int]], G: float, seed: int):
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    src = int(np.argmin(dists_c))
    depth = _bfs_depth(adj, src, n)
    L = _build_laplacian(pos, adj, n)
    solve_op = (L + MU2 * speye(n, format="csr")).tocsc()

    psi0 = np.exp(-0.5 * dists_c ** 2 / 1.15 ** 2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    w0 = _width(psi0, pos)

    results = {}
    for label, phi_sign in [("attract", +1.0), ("repulse", -1.0), ("free", 0.0)]:
        psi = psi0.copy()
        forces = []
        phi = np.zeros(n)
        for _ in range(N_ITER):
            rho = np.abs(psi) ** 2
            if phi_sign != 0:
                phi = phi_sign * spsolve(solve_op, G * rho)
            else:
                phi = np.zeros(n)
            forces.append(_shell_force(depth, n, psi, phi))
            H = _build_hamiltonian(pos, col, adj, n, phi)
            psi = _cn_step(H, psi, DT)
        rho_f = np.abs(psi) ** 2
        if phi_sign != 0:
            phi = phi_sign * spsolve(solve_op, G * rho_f)
        else:
            phi = np.zeros(n)
        H_f = _build_hamiltonian(pos, col, adj, n, phi)
        results[label] = {
            "w_ratio": _width(psi, pos) / w0,
            "norm": float(np.linalg.norm(psi)),
            "tw": int(sum(1 for f in forces if f > 0)),
            "gap": _spectral_gap(H_f),
        }

    contraction_a = results["attract"]["w_ratio"] / results["free"]["w_ratio"]
    contraction_r = results["repulse"]["w_ratio"] / results["free"]["w_ratio"]
    width_asym = contraction_a / contraction_r if contraction_r > 0 else float("nan")
    gap_ratio = (
        results["attract"]["gap"] / results["repulse"]["gap"]
        if results["repulse"]["gap"] > 0 and np.isfinite(results["repulse"]["gap"])
        else float("nan")
    )
    return {
        "family": name,
        "seed": seed,
        "nodes": n,
        "G": G,
        "width_asym": width_asym,
        "gap_ratio": gap_ratio,
        "tw_a": results["attract"]["tw"],
        "tw_r": results["repulse"]["tw"],
        "norm_a": results["attract"]["norm"],
        "norm_r": results["repulse"]["norm"],
        "w_a": results["attract"]["w_ratio"],
        "w_r": results["repulse"]["w_ratio"],
        "w_f": results["free"]["w_ratio"],
    }


def configs():
    return [
        ("random_geometric", 64, lambda s: make_random_geometric(seed=s, side=8)),
        ("random_geometric", 100, lambda s: make_random_geometric(seed=s, side=10)),
        ("growing", 64, lambda s: make_growing(seed=s, n_target=64)),
        ("growing", 100, lambda s: make_growing(seed=s, n_target=100)),
        ("layered_cycle", 64, lambda s: make_layered_cycle(seed=s, layers=8, width=8)),
        ("layered_cycle", 100, lambda s: make_layered_cycle(seed=s, layers=10, width=10)),
    ]


def main():
    t0 = time.time()
    print("=" * 104)
    print("RETAINED WEAK-COUPLING SIGN-SENSITIVITY AUDIT")
    print("=" * 104)
    print(
        f"Families=3, sizes=2/family, seeds={len(SEEDS)}, G={G_VALUES}, "
        f"runs={len(configs()) * len(SEEDS) * len(G_VALUES)}"
    )
    print(
        f"Hard shell split: tw_a >= {SHELL_HIGH}, tw_r <= {SHELL_LOW}; "
        f"norm tol={NORM_TOL:.0e}"
    )
    print()

    rows = []
    for G in G_VALUES:
        for family, nodes, builder in configs():
            for seed in SEEDS:
                name, pos, col, adj = builder(seed)
                row = run_case(name, pos, col, adj, G, seed)
                row["family_size"] = f"{family}:{nodes}"
                rows.append(row)

    print(
        f"{'family:size':<24s} {'G':>3s} {'seed':>4s} {'w_asym':>8s} {'gap_r':>8s} "
        f"{'tw_a':>5s} {'tw_r':>5s} {'norm_a':>9s} {'norm_r':>9s}"
    )
    print("-" * 104)
    for row in rows:
        print(
            f"{row['family_size']:<24s} {int(row['G']):>3d} {row['seed']:>4d} "
            f"{row['width_asym']:8.4f} {row['gap_ratio']:8.4f} "
            f"{row['tw_a']:5d} {row['tw_r']:5d} "
            f"{row['norm_a']:9.6f} {row['norm_r']:9.6f}"
        )

    total = len(rows)
    width_pass = [r for r in rows if np.isfinite(r["width_asym"]) and r["width_asym"] < 1.0]
    gap_pass = [r for r in rows if np.isfinite(r["gap_ratio"]) and r["gap_ratio"] > 1.0]
    norm_pass = [
        r
        for r in rows
        if abs(r["norm_a"] - 1.0) < NORM_TOL and abs(r["norm_r"] - 1.0) < NORM_TOL
    ]
    shell_split = [r for r in rows if r["tw_a"] >= SHELL_HIGH and r["tw_r"] <= SHELL_LOW]
    shell_order = [r for r in rows if r["tw_a"] > r["tw_r"]]
    shell_margin = [r for r in rows if (r["tw_a"] - r["tw_r"]) >= SHELL_MARGIN]

    print("\nSummary")
    print("-" * 104)
    print(f"Width asymmetry < 1      : {len(width_pass)}/{total}")
    print(f"Gap ratio > 1            : {len(gap_pass)}/{total}")
    print(f"Norm conserved           : {len(norm_pass)}/{total}")
    print(f"Shell strict split       : {len(shell_split)}/{total}")
    print(f"Shell ordered (tw_a>tw_r): {len(shell_order)}/{total}")
    print(f"Shell margin >= {SHELL_MARGIN:>2d}      : {len(shell_margin)}/{total}")

    best_name = "none"
    best_hits = -1
    for name, hits in [
        ("width asymmetry < 1", len(width_pass)),
        ("gap ratio > 1", len(gap_pass)),
        ("shell strict split", len(shell_split)),
        ("shell ordered", len(shell_order)),
        (f"shell margin >= {SHELL_MARGIN}", len(shell_margin)),
    ]:
        if hits > best_hits:
            best_name = name
            best_hits = hits
    print(f"Strongest sign-selective observable: {best_name} ({best_hits}/{total})")

    by_family = {}
    for row in rows:
        fam = row["family"]
        bucket = by_family.setdefault(fam, {"total": 0, "width": 0, "gap": 0, "shell_strict": 0, "shell_order": 0})
        bucket["total"] += 1
        if np.isfinite(row["width_asym"]) and row["width_asym"] < 1.0:
            bucket["width"] += 1
        if np.isfinite(row["gap_ratio"]) and row["gap_ratio"] > 1.0:
            bucket["gap"] += 1
        if row["tw_a"] >= SHELL_HIGH and row["tw_r"] <= SHELL_LOW:
            bucket["shell_strict"] += 1
        if row["tw_a"] > row["tw_r"]:
            bucket["shell_order"] += 1
        bucket.setdefault("shell_margin", 0)
        if (row["tw_a"] - row["tw_r"]) >= SHELL_MARGIN:
            bucket["shell_margin"] += 1

    print("\nBy family")
    print("-" * 104)
    for fam, bucket in sorted(by_family.items()):
        print(
            f"{fam:<18s} width {bucket['width']:>2d}/{bucket['total']:<2d}  "
            f"gap {bucket['gap']:>2d}/{bucket['total']:<2d}  "
            f"shell_strict {bucket['shell_strict']:>2d}/{bucket['total']:<2d}  "
            f"shell_order {bucket['shell_order']:>2d}/{bucket['total']:<2d}  "
            f"shell_margin {bucket['shell_margin']:>2d}/{bucket['total']:<2d}"
        )

    retained = best_hits == total and len(norm_pass) == total
    print("\nVerdict")
    print("-" * 104)
    if retained:
        print("RETAINED: a single sign-selective observable survives on the full audited surface.")
    else:
        print("EXPLORATORY ONLY: no single sign-selective observable survives on the full audited surface.")

    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
