#!/usr/bin/env python3
"""
Irregular Sign Core-Packet Gate at Both Screening Levels
=========================================================

Gate test for freezing a bounded same-surface irregular sign-separation packet
with core_packet as the centered audited observable, replacing shell_packet.

Motivation:
  - The sign separator (+Phi vs -Phi) is physically real on some surfaces
  - shell_packet (oscillating gaussian) fails at low screening because
    oscillation creates interference that masks the sign signal
  - core_packet (non-oscillating gaussian: exp(-r^2/2sigma^2)) shows 93%+
    positive margins at mu2=0.001 in prior tests
  - This script verifies core_packet works at BOTH screening levels

Design:
  - core_packet ONLY (no shell_packet, no ring_packet)
  - Two screening surfaces: mu2=0.1 (original) and mu2=0.001 (low)
  - Same three graph families, same seeds (42-46), same G values (5.0, 10.0)
  - Same observables: ball1_margin, ball2_margin, depth_margin
  - Window: steps [2, 11)

Acceptance gates:
  - Gate 1 (screened):      core_packet at mu2=0.1   >= 80% positive margins
  - Gate 2 (low-screening): core_packet at mu2=0.001 >= 80% positive margins
  - Gate 3 (cross-screening): both gates must pass simultaneously
"""

from __future__ import annotations

import math
import random
import time
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
MASS = 0.30
DT = 0.12
N_STEPS = 15
SIG_DEPTH = 1.2
WINDOW_START = 2
WINDOW_STOP = 11
G_VALUES = (5.0, 10.0)
SEEDS = tuple(range(42, 47))
MU2_LEVELS = (0.1, 0.001)


@dataclass(frozen=True)
class Row:
    mu2: float
    family: str
    seed: int
    g: float
    ball1_margin: float
    ball2_margin: float
    depth_margin: float
    norm_attr: float
    norm_rep: float


# ---------------------------------------------------------------------------
# Graph families (from frontier_staggered_self_gravity.py)
# ---------------------------------------------------------------------------

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=6):
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    adj = {}
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
    adj_l = {k: list(v) for k, v in adj.items()}
    n = len(pos)
    src = n // 2
    return "random_geometric", pos, col, adj_l, n, src


def make_growing(seed=42, n_target=48):
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
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    adj_l = {k: list(v) for k, v in adj.items()}
    return "growing", pos, col, adj_l, len(pos), 0


def make_layered_cycle(seed=42, layers=6, width=4):
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes = []
    idx = 0
    for layer in range(layers):
        count = max(2, width)
        this_layer = []
        for k in range(count):
            y = float(k) + 0.05 * (rng.random() - 0.5)
            coords.append((float(layer), y))
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
    adj_l = {k: list(v) for k, v in adj.items()}
    src = layer_nodes[0][0]
    return "layered_cycle", pos, col, adj_l, n, src


# ---------------------------------------------------------------------------
# Physics utilities
# ---------------------------------------------------------------------------

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


def _solve_phi(L, n, rho, mu2):
    A = (L + mu2 * speye(n, format="csr")).tocsc()
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


# ---------------------------------------------------------------------------
# Core packet (non-oscillating gaussian -- the primary observable)
# ---------------------------------------------------------------------------

def _core_packet(depth):
    """exp(-r^2 / 2 sigma^2), no oscillation."""
    psi = np.exp(-0.5 * (depth ** 2) / (SIG_DEPTH ** 2))
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    return psi / np.linalg.norm(psi)


# ---------------------------------------------------------------------------
# Observable extraction
# ---------------------------------------------------------------------------

def _capture(depth, psi, k):
    rho = np.abs(psi) ** 2
    return float(np.sum(rho[depth <= k]))


def _mean_depth(depth, psi):
    rho = np.abs(psi) ** 2
    rho /= max(np.sum(rho), 1e-30)
    finite = np.isfinite(depth)
    return float(np.sum(rho[finite] * depth[finite]))


def _trace_observables(pos, colors, adj, n, L, depth, g, phi_sign, mu2):
    psi = _core_packet(depth)
    ball1 = []
    ball2 = []
    mean_d = []
    for _ in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = _solve_phi(L, n, g * rho, mu2)
        H = _build_H(pos, colors, adj, n, phi, phi_sign)
        psi = _cn_step(H, psi)
        ball1.append(_capture(depth, psi, 1))
        ball2.append(_capture(depth, psi, 2))
        mean_d.append(_mean_depth(depth, psi))
    return np.array(ball1), np.array(ball2), np.array(mean_d), float(np.linalg.norm(psi))


# ---------------------------------------------------------------------------
# Row collection
# ---------------------------------------------------------------------------

def _family_rows(builder, mu2, **kwargs):
    rows = []
    for seed in SEEDS:
        name, pos, colors, adj, n, _ = builder(seed=seed, **kwargs)
        center, depth = _graph_center(adj, n)
        L = _laplacian(pos, adj, n)
        for g in G_VALUES:
            attr_b1, attr_b2, attr_d, attr_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, +1.0, mu2
            )
            rep_b1, rep_b2, rep_d, rep_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, -1.0, mu2
            )
            rows.append(
                Row(
                    mu2=mu2,
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
            f"  mu2={mu2:<6} {name:16s} seed={seed} "
            f"center={center} max_depth={int(np.max(depth[np.isfinite(depth)]))}"
        )
    return rows


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _summarize(rows, metric):
    vals = np.array([getattr(r, metric) for r in rows], dtype=float)
    return int(np.sum(vals > 0)), len(vals), float(np.mean(vals)), float(np.min(vals))


def _fraction_positive(rows, metric):
    vals = np.array([getattr(r, metric) for r in rows], dtype=float)
    total = len(vals)
    if total == 0:
        return 0.0, 0, 0
    hits = int(np.sum(vals > 0))
    return hits / total, hits, total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    print("=" * 92)
    print("IRREGULAR SIGN CORE-PACKET GATE AT BOTH SCREENING LEVELS")
    print("=" * 92)
    print()
    print("Observable: core_packet (exp(-r^2/2sigma^2), NO oscillation)")
    print("Screening levels: mu2=0.1 (original), mu2=0.001 (low)")
    print(f"Parameters: MASS={MASS}, DT={DT}, N_STEPS={N_STEPS}, SIG_DEPTH={SIG_DEPTH}")
    print(f"Window: steps [{WINDOW_START}, {WINDOW_STOP})")
    print(f"G values: {G_VALUES}")
    print(f"Seeds: {SEEDS}")
    print()

    all_rows = []

    for mu2 in MU2_LEVELS:
        print(f"--- mu2={mu2} ---")
        all_rows.extend(_family_rows(make_random_geometric, mu2, side=8))
        all_rows.extend(_family_rows(make_growing, mu2, n_target=64))
        all_rows.extend(_family_rows(make_layered_cycle, mu2, layers=8, width=8))
        print()

    # --- Per-screening detail ---
    print("=" * 92)
    print("PER-SCREENING DETAIL")
    print("=" * 92)
    for mu2 in MU2_LEVELS:
        mu2_rows = [r for r in all_rows if r.mu2 == mu2]
        print(f"\nmu2={mu2} ({len(mu2_rows)} rows)")
        print("-" * 80)
        for family in ("random_geometric", "growing", "layered_cycle"):
            fam_rows = [r for r in mu2_rows if r.family == family]
            if not fam_rows:
                continue
            print(f"\n  {family}")
            for g in G_VALUES:
                sub = [r for r in fam_rows if r.g == g]
                for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
                    hits, total, mean, min_v = _summarize(sub, metric)
                    print(
                        f"    G={g:>4.1f} {metric:>12s}: "
                        f"pos={hits}/{total} mean={mean:+.4e} min={min_v:+.4e}"
                    )

    # --- Summary table ---
    print("\n")
    print("=" * 92)
    print("SCREENING-LEVEL SUMMARY")
    print("=" * 92)
    gate_results = {}
    for mu2 in MU2_LEVELS:
        mu2_rows = [r for r in all_rows if r.mu2 == mu2]
        print(f"\nmu2={mu2} ({len(mu2_rows)} rows)")
        fracs = {}
        for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
            hits, total, mean, min_v = _summarize(mu2_rows, metric)
            frac = hits / total if total > 0 else 0.0
            fracs[metric] = frac
            print(
                f"  {metric:>12s}: pos={hits}/{total} ({frac:.1%}) "
                f"mean={mean:+.4e} min={min_v:+.4e}"
            )
        min_frac = min(fracs.values())
        gate_results[mu2] = min_frac
        print(f"  min fraction across all metrics: {min_frac:.1%}")

    # --- Norm check ---
    max_norm_drift = max(
        max(abs(r.norm_attr - 1.0), abs(r.norm_rep - 1.0)) for r in all_rows
    )
    print(f"\nmax_norm_drift = {max_norm_drift:.3e}")

    # --- Per-graph-family breakdown ---
    print("\n")
    print("=" * 92)
    print("PER-GRAPH-FAMILY BREAKDOWN")
    print("=" * 92)
    for mu2 in MU2_LEVELS:
        mu2_rows = [r for r in all_rows if r.mu2 == mu2]
        print(f"\nmu2={mu2}")
        for family in ("random_geometric", "growing", "layered_cycle"):
            fam_rows = [r for r in mu2_rows if r.family == family]
            if not fam_rows:
                continue
            b1_frac, b1_hits, b1_total = _fraction_positive(fam_rows, "ball1_margin")
            b2_frac, b2_hits, b2_total = _fraction_positive(fam_rows, "ball2_margin")
            d_frac, d_hits, d_total = _fraction_positive(fam_rows, "depth_margin")
            print(
                f"  {family:20s}: ball1 {b1_hits}/{b1_total} ({b1_frac:.0%})  "
                f"ball2 {b2_hits}/{b2_total} ({b2_frac:.0%})  "
                f"depth {d_hits}/{d_total} ({d_frac:.0%})"
            )

    # --- Acceptance gates ---
    print("\n")
    print("=" * 92)
    print("ACCEPTANCE GATES")
    print("=" * 92)

    gate1_pass = gate_results[0.1] >= 0.80
    print(f"\nGATE 1 (screened): core_packet at mu2=0.1, threshold >= 80%")
    print(f"  min positive fraction: {gate_results[0.1]:.1%}")
    print(f"  --> {'PASS' if gate1_pass else 'FAIL'}")

    gate2_pass = gate_results[0.001] >= 0.80
    print(f"\nGATE 2 (low-screening): core_packet at mu2=0.001, threshold >= 80%")
    print(f"  min positive fraction: {gate_results[0.001]:.1%}")
    print(f"  --> {'PASS' if gate2_pass else 'FAIL'}")

    gate3_pass = gate1_pass and gate2_pass
    print(f"\nGATE 3 (cross-screening): both gates must pass")
    print(f"  --> {'PASS' if gate3_pass else 'FAIL'}")

    # --- Verdict ---
    print("\n")
    print("=" * 92)
    print("VERDICT")
    print("=" * 92)
    if gate3_pass:
        print("All three gates PASS.")
        print("core_packet (non-oscillating gaussian) separates +Phi from -Phi")
        print("on the audited irregular bipartite families at BOTH screening levels.")
        print()
        print("Current-main read: this is a bounded same-surface irregular")
        print("sign separator on the centered core-packet surface. The older")
        print("shell_packet failure at low screening was an artifact of")
        print("oscillation-induced interference, not a failure of the")
        print("underlying sign physics.")
        print()
        print("Scope: audited families (random_geometric, growing, layered_cycle),")
        print("seeds 42-46, G in {5.0, 10.0}. Broader packet/transport")
        print("portability remains open.")
    elif gate1_pass:
        print("Gate 1 PASSES but Gate 2 FAILS.")
        print("core_packet works at high screening but not at low screening.")
        print("Lane stays on hold.")
    elif gate2_pass:
        print("Gate 2 PASSES but Gate 1 FAILS.")
        print("core_packet works at low screening but not at high screening.")
        print("Lane stays on hold.")
    else:
        print("Both screening-level gates FAIL.")
        print("core_packet does not reliably separate signs.")
        print("Lane stays on hold.")

    print(f"\nDone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
