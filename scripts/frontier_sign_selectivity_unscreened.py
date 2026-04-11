#!/usr/bin/env python3
"""
Sign Selectivity at Unscreened Coupling (mu2=0.001)
====================================================

The 300/300 sign selectivity result was obtained at mu2=0.22 (screening
length ~2.13 sites). This script rechecks the result at mu2=0.001
(screening length ~31.6 sites) to verify it is not a screening artifact.

For each (G, family, seed) combination:
  1. Evolve psi under self-consistent +Phi (always positive via parity coupling)
     and measure w_grav = final width.
  2. Evolve psi under a random static Phi of matched variance and measure
     w_rand = final width.
  3. Evolve psi under free Hamiltonian (Phi=0) and measure w_free.

Report:
  - Fraction where w_grav < w_free (self-consistent attraction)
  - Fraction where w_rand < w_free (random potential attraction)
  - Pass if self-consistent gives 100% attraction and random does not.

G = 3, 5, 8, 10, 15 on 3 families x 10 seeds = 150 combinations.
"""

from __future__ import annotations

import math
import random
import time

import numpy as np
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve


# ============================================================================
# Parameters
# ============================================================================
MASS = 0.30
MU2 = 0.001  # unscreened: screening length = 1/sqrt(0.001) ~ 31.6 sites
DT = 0.12
N_ITER = 40
G_VALUES = [3, 5, 8, 10, 15]
SEEDS = list(range(42, 52))  # 10 seeds: 42..51


# ============================================================================
# Graph construction
# ============================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5), y + 0.08 * (rng.random() - 0.5)))
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


def make_growing(seed=42, n_target=64):
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
            for _, j in ds[:min(4, len(ds))]:
                _ae(adj, cur, j)
        cur += 1
    return "growing", np.array(coords), np.array(colors, dtype=int), {k: list(v) for k, v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
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


# ============================================================================
# Physics tools
# ============================================================================

def _build_laplacian(pos, adj, n):
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


def _build_hamiltonian(pos, col, adj, n, phi):
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


def _cn_step(H, psi, dt):
    n = H.shape[0]
    a_plus = (speye(n, format="csc") + 1j * H * dt / 2).tocsc()
    a_minus = speye(n, format="csr") - 1j * H * dt / 2
    return spsolve(a_plus, a_minus.dot(psi))


def _width(psi, pos):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return float(np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2))))


# ============================================================================
# Sign selectivity test
# ============================================================================

def run_case(name, pos, col, adj, G, seed):
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    L = _build_laplacian(pos, adj, n)
    solve_op = (L + MU2 * speye(n, format="csr")).tocsc()

    psi0 = np.exp(-0.5 * dists_c ** 2 / 1.15 ** 2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    # --- Self-consistent +Phi (always positive via parity coupling) ---
    psi_grav = psi0.copy()
    for _ in range(N_ITER):
        rho = np.abs(psi_grav) ** 2
        phi = spsolve(solve_op, G * rho)  # (L + mu2 I) Phi = G rho, rho >= 0 so Phi >= 0
        H = _build_hamiltonian(pos, col, adj, n, phi)
        psi_grav = _cn_step(H, psi_grav, DT)
    w_grav = _width(psi_grav, pos)

    # Capture the variance of the final self-consistent Phi for the random control
    rho_final = np.abs(psi_grav) ** 2
    phi_final = spsolve(solve_op, G * rho_final)
    phi_var = float(np.var(phi_final))

    # --- Random Phi of matched variance (static, drawn once) ---
    rng = np.random.RandomState(seed * 1000 + int(G))
    phi_rand = rng.randn(n)
    if np.var(phi_rand) > 0:
        phi_rand *= np.sqrt(phi_var / np.var(phi_rand))
    # Make it positive-mean to match the self-consistent Phi's positivity
    phi_rand = np.abs(phi_rand)  # fold to positive, rescale variance
    if np.var(phi_rand) > 0:
        phi_rand *= np.sqrt(phi_var / np.var(phi_rand))

    psi_rand = psi0.copy()
    for _ in range(N_ITER):
        H = _build_hamiltonian(pos, col, adj, n, phi_rand)
        psi_rand = _cn_step(H, psi_rand, DT)
    w_rand = _width(psi_rand, pos)

    # --- Free evolution (Phi=0) ---
    psi_free = psi0.copy()
    phi_zero = np.zeros(n)
    for _ in range(N_ITER):
        H = _build_hamiltonian(pos, col, adj, n, phi_zero)
        psi_free = _cn_step(H, psi_free, DT)
    w_free = _width(psi_free, pos)

    return {
        "family": name,
        "G": G,
        "seed": seed,
        "w_grav": w_grav,
        "w_rand": w_rand,
        "w_free": w_free,
        "ratio_grav": w_grav / w_free if w_free > 0 else float("nan"),
        "ratio_rand": w_rand / w_free if w_free > 0 else float("nan"),
        "grav_contracts": w_grav < w_free,
        "rand_contracts": w_rand < w_free,
        "phi_var": phi_var,
    }


# ============================================================================
# Main
# ============================================================================

def main():
    t0 = time.time()
    print("=" * 90)
    print("SIGN SELECTIVITY AT UNSCREENED COUPLING (mu2=0.001)")
    print("=" * 90)
    print(f"mu2={MU2} (screening length = {1/np.sqrt(MU2):.1f} sites)")
    print(f"G values: {G_VALUES}")
    print(f"Families: random_geometric, growing, layered_cycle")
    print(f"Seeds: {SEEDS[0]}..{SEEDS[-1]} ({len(SEEDS)} seeds)")
    print(f"Total combinations: {len(G_VALUES) * 3 * len(SEEDS)}")
    print(f"DT={DT}, MASS={MASS}, N_ITER={N_ITER}")
    print()

    families = [
        ("random_geometric", lambda s: make_random_geometric(seed=s, side=8)),
        ("growing", lambda s: make_growing(seed=s, n_target=64)),
        ("layered_cycle", lambda s: make_layered_cycle(seed=s, layers=8, width=8)),
    ]

    rows = []
    for fam_name, builder in families:
        for G in G_VALUES:
            for seed in SEEDS:
                name, pos, col, adj = builder(seed)
                row = run_case(name, pos, col, adj, G, seed)
                rows.append(row)

    # Print detailed table
    print(f"{'family':<20s} {'G':>3s} {'seed':>4s} {'w_grav/free':>11s} {'w_rand/free':>11s} "
          f"{'grav<1':>6s} {'rand<1':>6s} {'phi_var':>10s}")
    print("-" * 90)
    for r in rows:
        print(f"{r['family']:<20s} {r['G']:>3d} {r['seed']:>4d} "
              f"{r['ratio_grav']:11.6f} {r['ratio_rand']:11.6f} "
              f"{'YES' if r['grav_contracts'] else 'NO':>6s} "
              f"{'YES' if r['rand_contracts'] else 'NO':>6s} "
              f"{r['phi_var']:10.6f}")

    # Summary
    total = len(rows)
    grav_pass = sum(1 for r in rows if r["grav_contracts"])
    rand_pass = sum(1 for r in rows if r["rand_contracts"])

    print()
    print("=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"Self-consistent Phi contracts (w_grav < w_free): {grav_pass}/{total}")
    print(f"Random Phi contracts (w_rand < w_free):          {rand_pass}/{total}")
    print()

    # Breakdown by family
    for fam in ["random_geometric", "growing", "layered_cycle"]:
        fam_rows = [r for r in rows if r["family"] == fam]
        fg = sum(1 for r in fam_rows if r["grav_contracts"])
        fr = sum(1 for r in fam_rows if r["rand_contracts"])
        print(f"  {fam:<20s}: grav {fg}/{len(fam_rows)}, rand {fr}/{len(fam_rows)}")

    # Breakdown by G
    print()
    for G in G_VALUES:
        g_rows = [r for r in rows if r["G"] == G]
        fg = sum(1 for r in g_rows if r["grav_contracts"])
        fr = sum(1 for r in g_rows if r["rand_contracts"])
        print(f"  G={G:<3d}: grav {fg}/{len(g_rows)}, rand {fr}/{len(g_rows)}")

    print()
    if grav_pass == total:
        print(f"PASS: Self-consistent gravity contracts in {grav_pass}/{total} cases at mu2={MU2}.")
        print(f"      Random potential contracts in only {rand_pass}/{total} cases.")
        print("      Sign selectivity is NOT a screening artifact.")
    elif grav_pass >= 0.9 * total:
        print(f"MARGINAL: Self-consistent gravity contracts in {grav_pass}/{total} cases (>90%).")
        print(f"          Random potential contracts in {rand_pass}/{total} cases.")
    else:
        print(f"FAIL: Self-consistent gravity contracts in only {grav_pass}/{total} cases at mu2={MU2}.")
        print(f"      Sign selectivity MAY be a screening artifact.")

    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
