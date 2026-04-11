#!/usr/bin/env python3
"""
Irregular Sign Low-Screening Gate with Third Packet Family
===========================================================

Gate test for moving the irregular-sign lane from hold toward bounded
retention. The lane is held because:
  - Strong result on one screened shell-packet surface
  - Low-screening confirmation FAILED in the reinforcement run
  - Second packet family helped but did NOT fully close the lane

This script runs the endogenous sign closure at low screening (mu2=0.001)
on the same irregular graph families with THREE packet families:
  1. shell_packet: oscillating shell (exp(-r^2/2s^2) * exp(ikr))
  2. core_packet: non-oscillating gaussian (exp(-r^2/2s^2))
  3. ring_packet: p-wave-like shell with node at center
     (r * exp(-r^2/2s^2) * exp(ikr))

Acceptance gates:
  - Low-screening gate: shell_packet positive margins >= 80% of rows
  - Second family gate: at least one additional family >= 70% positive
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
# Parameters (matching reinforcement run exactly)
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.001          # low screening -- this is the gate surface
DT = 0.12
N_STEPS = 15
SIG_DEPTH = 1.2
K_SHELL = 0.7
WINDOW_START = 2
WINDOW_STOP = 11
G_VALUES = (5.0, 10.0)
SEEDS = tuple(range(42, 47))


@dataclass(frozen=True)
class Row:
    packet: str
    family: str
    seed: int
    g: float
    ball1_margin: float
    ball2_margin: float
    depth_margin: float
    norm_attr: float
    norm_rep: float


# ---------------------------------------------------------------------------
# Graph families (copied from frontier_staggered_self_gravity.py)
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


# ---------------------------------------------------------------------------
# Packet families
# ---------------------------------------------------------------------------

def _shell_packet(depth):
    """Oscillating shell: exp(-r^2/2s^2) * exp(ikr)."""
    psi = np.exp(-0.5 * (depth**2) / (SIG_DEPTH**2)) * np.exp(1j * K_SHELL * depth)
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    return psi / np.linalg.norm(psi)


def _core_packet(depth):
    """Non-oscillating gaussian core: exp(-r^2/2s^2)."""
    psi = np.exp(-0.5 * (depth**2) / (SIG_DEPTH**2))
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    return psi / np.linalg.norm(psi)


def _ring_packet(depth):
    """P-wave-like ring packet: r * exp(-r^2/2s^2) * exp(ikr).

    Structurally independent from both shell and core packets:
    - Has a node at the center (r=0), unlike both existing families
    - Carries oscillation like shell, but with p-wave radial profile
    - Peak amplitude at r ~ sigma, not r=0
    """
    psi = depth * np.exp(-0.5 * (depth**2) / (SIG_DEPTH**2)) * np.exp(1j * K_SHELL * depth)
    psi = np.where(np.isfinite(depth), psi, 0.0).astype(complex)
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        return psi
    return psi / norm


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


def _trace_observables(pos, colors, adj, n, L, depth, g, phi_sign, packet_fn):
    psi = packet_fn(depth)
    ball1 = []
    ball2 = []
    mean_d = []
    for _ in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = _solve_phi(L, n, g * rho)
        H = _build_H(pos, colors, adj, n, phi, phi_sign)
        psi = _cn_step(H, psi)
        ball1.append(_capture(depth, psi, 1))
        ball2.append(_capture(depth, psi, 2))
        mean_d.append(_mean_depth(depth, psi))
    return np.array(ball1), np.array(ball2), np.array(mean_d), float(np.linalg.norm(psi))


# ---------------------------------------------------------------------------
# Row collection
# ---------------------------------------------------------------------------

def _family_rows(builder, packet_name, packet_fn, **kwargs):
    rows = []
    for seed in SEEDS:
        name, pos, colors, adj, n, _ = builder(seed=seed, **kwargs)
        center, depth = _graph_center(adj, n)
        L = _laplacian(pos, adj, n)
        for g in G_VALUES:
            attr_b1, attr_b2, attr_d, attr_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, +1.0, packet_fn
            )
            rep_b1, rep_b2, rep_d, rep_norm = _trace_observables(
                pos, colors, adj, n, L, depth, g, -1.0, packet_fn
            )
            rows.append(
                Row(
                    packet=packet_name,
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
            f"  packet={packet_name:14s} {name:16s} seed={seed} "
            f"center={center} max_depth={int(np.max(depth[np.isfinite(depth)]))}"
        )
    return rows


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _summarize(rows, metric):
    vals = np.array([getattr(r, metric) for r in rows], dtype=float)
    return int(np.sum(vals > 0)), len(vals), float(np.mean(vals)), float(np.min(vals))


def _print_packet_detail(rows):
    packets = sorted(set(r.packet for r in rows))
    for packet in packets:
        packet_rows = [r for r in rows if r.packet == packet]
        print(f"\nPACKET FAMILY: {packet}")
        print("-" * 92)
        for family in ("random_geometric", "growing", "layered_cycle"):
            fam_rows = [r for r in packet_rows if r.family == family]
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
    print("IRREGULAR SIGN LOW-SCREENING GATE")
    print("with third packet family (ring/p-wave)")
    print("=" * 92)
    print()
    print("Surface: low-screening mu2=0.001")
    print("Packet families: shell_packet (oscillating), core_packet (gaussian), ring_packet (p-wave)")
    print(f"Parameters: MASS={MASS}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"Window: steps [{WINDOW_START}, {WINDOW_STOP})")
    print(f"G values: {G_VALUES}")
    print(f"Seeds: {SEEDS}")
    print()

    all_rows = []

    # --- shell_packet on all three graph families ---
    print("--- shell_packet ---")
    all_rows.extend(_family_rows(make_random_geometric, "shell_packet", _shell_packet, side=8))
    all_rows.extend(_family_rows(make_growing, "shell_packet", _shell_packet, n_target=64))
    all_rows.extend(_family_rows(make_layered_cycle, "shell_packet", _shell_packet, layers=8, width=8))

    # --- core_packet on all three graph families ---
    print("\n--- core_packet ---")
    all_rows.extend(_family_rows(make_random_geometric, "core_packet", _core_packet, side=8))
    all_rows.extend(_family_rows(make_growing, "core_packet", _core_packet, n_target=64))
    all_rows.extend(_family_rows(make_layered_cycle, "core_packet", _core_packet, layers=8, width=8))

    # --- ring_packet on all three graph families ---
    print("\n--- ring_packet ---")
    all_rows.extend(_family_rows(make_random_geometric, "ring_packet", _ring_packet, side=8))
    all_rows.extend(_family_rows(make_growing, "ring_packet", _ring_packet, n_target=64))
    all_rows.extend(_family_rows(make_layered_cycle, "ring_packet", _ring_packet, layers=8, width=8))

    # --- Detailed per-packet breakdown ---
    print("\n")
    print("=" * 92)
    print("PER-PACKET DETAIL")
    print("=" * 92)
    _print_packet_detail(all_rows)

    # --- Global summary per packet family ---
    print("\n")
    print("=" * 92)
    print("GLOBAL SUMMARY (all graph families combined)")
    print("=" * 92)
    packet_names = ["shell_packet", "core_packet", "ring_packet"]
    packet_fractions = {}
    for packet in packet_names:
        packet_rows = [r for r in all_rows if r.packet == packet]
        print(f"\n{packet} ({len(packet_rows)} rows)")
        fracs = {}
        for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
            hits, total, mean, min_v = _summarize(packet_rows, metric)
            frac = hits / total if total > 0 else 0.0
            fracs[metric] = frac
            print(
                f"  {metric:>12s}: pos={hits}/{total} ({frac:.1%}) "
                f"mean={mean:+.4e} min={min_v:+.4e}"
            )
        packet_fractions[packet] = fracs

    # --- Norm check ---
    max_norm_drift = max(
        max(abs(r.norm_attr - 1.0), abs(r.norm_rep - 1.0)) for r in all_rows
    )
    print(f"\nmax_norm_drift = {max_norm_drift:.3e}")

    # --- Size portability: compare across G values ---
    print("\n")
    print("=" * 92)
    print("SIZE PORTABILITY (by G value)")
    print("=" * 92)
    for packet in packet_names:
        packet_rows = [r for r in all_rows if r.packet == packet]
        print(f"\n{packet}")
        for g in G_VALUES:
            g_rows = [r for r in packet_rows if r.g == g]
            for metric in ("ball1_margin", "ball2_margin", "depth_margin"):
                frac, hits, total = _fraction_positive(g_rows, metric)
                print(f"  G={g:>4.1f} {metric:>12s}: pos={hits}/{total} ({frac:.1%})")

    # --- Acceptance gate evaluation ---
    print("\n")
    print("=" * 92)
    print("ACCEPTANCE GATES")
    print("=" * 92)

    # Gate 1: Low-screening gate -- shell_packet
    shell_rows = [r for r in all_rows if r.packet == "shell_packet"]
    shell_ball1_frac, _, _ = _fraction_positive(shell_rows, "ball1_margin")
    shell_ball2_frac, _, _ = _fraction_positive(shell_rows, "ball2_margin")
    shell_depth_frac, _, _ = _fraction_positive(shell_rows, "depth_margin")
    shell_min_frac = min(shell_ball1_frac, shell_ball2_frac, shell_depth_frac)

    gate1_pass = shell_min_frac >= 0.80
    print(f"\nGATE 1: Low-screening shell_packet (threshold >= 80%)")
    print(f"  ball1_margin positive: {shell_ball1_frac:.1%}")
    print(f"  ball2_margin positive: {shell_ball2_frac:.1%}")
    print(f"  depth_margin positive: {shell_depth_frac:.1%}")
    print(f"  min fraction: {shell_min_frac:.1%}")
    print(f"  --> {'PASS' if gate1_pass else 'FAIL'}")

    # Gate 2: Second family gate -- core_packet OR ring_packet >= 70%
    gate2_pass = False
    gate2_details = {}
    for packet in ("core_packet", "ring_packet"):
        p_rows = [r for r in all_rows if r.packet == packet]
        b1_frac, _, _ = _fraction_positive(p_rows, "ball1_margin")
        b2_frac, _, _ = _fraction_positive(p_rows, "ball2_margin")
        d_frac, _, _ = _fraction_positive(p_rows, "depth_margin")
        min_frac = min(b1_frac, b2_frac, d_frac)
        passes = min_frac >= 0.70
        gate2_details[packet] = (b1_frac, b2_frac, d_frac, min_frac, passes)
        if passes:
            gate2_pass = True

    print(f"\nGATE 2: Second packet family (threshold >= 70%)")
    for packet, (b1f, b2f, df, mf, passed) in gate2_details.items():
        print(f"\n  {packet}:")
        print(f"    ball1_margin positive: {b1f:.1%}")
        print(f"    ball2_margin positive: {b2f:.1%}")
        print(f"    depth_margin positive: {df:.1%}")
        print(f"    min fraction: {mf:.1%}")
        print(f"    --> {'PASS' if passed else 'FAIL'}")
    print(f"\n  Gate 2 overall: {'PASS (at least one family passes)' if gate2_pass else 'FAIL (no family reaches 70%)'}")

    # --- Final verdict ---
    print("\n")
    print("=" * 92)
    print("VERDICT")
    print("=" * 92)
    if gate1_pass and gate2_pass:
        print("Both gates PASS.")
        print("The irregular-sign lane moves toward bounded retention.")
        print("Low-screening sign closure confirmed with packet-family generality.")
    elif gate1_pass and not gate2_pass:
        print("Gate 1 PASSES but Gate 2 FAILS.")
        print("Shell packet survives low screening, but no second family reaches 70%.")
        print("Lane stays on hold: sign separator is not packet-family portable.")
    elif not gate1_pass and gate2_pass:
        print("Gate 1 FAILS but Gate 2 PASSES.")
        print("Shell packet does not survive low screening even though alternative families do.")
        print("Lane stays on hold: primary observable is not robust at mu2=0.001.")
    else:
        print("Both gates FAIL.")
        print("Lane stays on hold: low-screening sign closure does not survive.")
        print("The irregular sign result remains frontier-only.")

    # --- Per-graph-family breakdown for diagnosing failures ---
    print("\n")
    print("=" * 92)
    print("FAILURE DIAGNOSIS: per graph family breakdown")
    print("=" * 92)
    for packet in packet_names:
        packet_rows = [r for r in all_rows if r.packet == packet]
        print(f"\n{packet}")
        for family in ("random_geometric", "growing", "layered_cycle"):
            fam_rows = [r for r in packet_rows if r.family == family]
            if not fam_rows:
                continue
            b2_frac, b2_hits, b2_total = _fraction_positive(fam_rows, "ball2_margin")
            d_frac, d_hits, d_total = _fraction_positive(fam_rows, "depth_margin")
            print(
                f"  {family:20s}: ball2 {b2_hits}/{b2_total} ({b2_frac:.0%})  "
                f"depth {d_hits}/{d_total} ({d_frac:.0%})"
            )

    print(f"\nDone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
