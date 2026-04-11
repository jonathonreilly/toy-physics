#!/usr/bin/env python3
"""
Memory & Sign-Regime Robustness Checks
=======================================

Part A -- Gravitational Memory Robustness
  The gravitational memory probe showed +0.013 permanent separation shift.
  This script checks whether that signal is robust across:
    1. Multiple lattice sizes  (n = 41, 61, 81, 101)
    2. Multiple pulse positions (center, off-center)
    3. Multiple pulse durations (5, 10, 15, 20 steps)
    4. Control drift is exactly zero on ALL configurations
    5. Memory/amplitude ratio with error bars

Part B -- Weak-Coupling Sign-Regime Robustness
  The weak-coupling regime (G=5-10) showed 60/60 shell-force margin.
  This script checks whether that window is robust across:
    1. More seeds (10 per family instead of 5)
    2. More G values in the sweet spot (G = 3..15)
    3. All 3 graph families (random geometric, growing, layered cycle)
    4. Report exact G window where attract > repulse on ALL seeds

Parameters (shared with frontier_gravitational_memory.py):
  MASS=0.30, MU2=0.22, DT_MATTER=0.12, DT_FIELD=0.03
  FIELD_C=1.0, FIELD_GAMMA=0.05, FIELD_BETA=5.0
"""

from __future__ import annotations

import math
import random
import time
from collections import deque

import numpy as np
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve

# ── Shared constants ────────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT_MATTER = 0.12
DT_FIELD = 0.03
N_FIELD_SUBSTEPS = 4
C_SPEED = 1.0
GAMMA = 0.05
BETA = 5.0
N_STEPS = 60

PULSE_AMP = 1.0  # reference amplitude for memory probe

# Sign-regime constants
DT_SIGN = 0.12
N_ITER_SIGN = 40
G_VALUES = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
SEEDS_SIGN = list(range(42, 52))  # 10 seeds


# =====================================================================
#  PART A: Gravitational Memory Robustness
# =====================================================================

def build_ring_laplacian(n):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        ip = (i + 1) % n
        im = (i - 1) % n
        L[i, i] += 2.0
        L[i, ip] -= 1.0
        L[i, im] -= 1.0
    return L.tocsr()


def parity_vector(n):
    return np.array([(-1)**i for i in range(n)], dtype=float)


def build_ring_hamiltonian(n, phi, par):
    H = lil_matrix((n, n), dtype=complex)
    H.setdiag((MASS + phi) * par)
    for i in range(n):
        ip = (i + 1) % n
        H[i, ip] += -0.5j
        H[ip, i] += 0.5j
    return H.tocsr()


def cn_step(H, psi, dt):
    n = H.shape[0]
    I = speye(n, format='csc')
    ap = (I + 1j * H * dt / 2).tocsc()
    am = I - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def ring_centroid(psi, n):
    prob = np.abs(psi) ** 2
    prob /= prob.sum() + 1e-30
    angles = 2 * np.pi * np.arange(n) / n
    cx = np.sum(prob * np.cos(angles))
    cy = np.sum(prob * np.sin(angles))
    return np.arctan2(cy, cx) / (2 * np.pi) * n % n


def ring_distance(c1, c2, n):
    d = abs(c1 - c2)
    return min(d, n - d)


def make_wavepacket(center, n, sigma=2.0):
    x = np.arange(n)
    dx = x - center
    dx = dx - n * np.round(dx / n)
    psi = np.exp(-dx**2 / (2 * sigma**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def run_memory_sim(n, pos_a, pos_b, source_pos, pulse_start, pulse_end,
                   pulse_amplitude, use_pulse=True):
    """Run memory simulation on a ring of size n."""
    par = parity_vector(n)
    L = build_ring_laplacian(n)
    field_op = -C_SPEED**2 * (L + MU2 * speye(n, format='csr'))

    phi = np.zeros(n)
    pi_field = np.zeros(n)
    source_profile = np.zeros(n)
    source_profile[source_pos] = 1.0

    psi_a = make_wavepacket(pos_a, n)
    psi_b = make_wavepacket(pos_b, n)

    sep_history = []
    for step in range(N_STEPS):
        ca = ring_centroid(psi_a, n)
        cb = ring_centroid(psi_b, n)
        sep_history.append(ring_distance(ca, cb, n))

        pulse_active = use_pulse and (pulse_start <= step < pulse_end)
        for _ in range(N_FIELD_SUBSTEPS):
            source = BETA * pulse_amplitude * source_profile if pulse_active else np.zeros(n)
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc
            phi += DT_FIELD * pi_field
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc

        H = build_ring_hamiltonian(n, phi, par)
        psi_a = cn_step(H, psi_a, DT_MATTER)
        psi_b = cn_step(H, psi_b, DT_MATTER)

    ca = ring_centroid(psi_a, n)
    cb = ring_centroid(psi_b, n)
    sep_history.append(ring_distance(ca, cb, n))

    return np.array(sep_history)


def memory_probe(n, pos_a, pos_b, source_pos, pulse_start, pulse_end):
    """Return (control_drift, memory_net, memory_raw) for a single config."""
    sep_ctrl = run_memory_sim(n, pos_a, pos_b, source_pos, pulse_start, pulse_end,
                              0.0, use_pulse=False)
    sep_pulse = run_memory_sim(n, pos_a, pos_b, source_pos, pulse_start, pulse_end,
                               PULSE_AMP, use_pulse=True)
    ctrl_drift = sep_ctrl[-1] - sep_ctrl[0]
    raw = sep_pulse[-1] - sep_pulse[0]
    net = raw - ctrl_drift
    return ctrl_drift, net, raw


def run_memory_robustness():
    print("=" * 80)
    print("PART A: GRAVITATIONAL MEMORY ROBUSTNESS")
    print("=" * 80)
    print(f"MASS={MASS}, MU2={MU2}, DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}")
    print(f"FIELD_C={C_SPEED}, GAMMA={GAMMA}, BETA={BETA}")
    print(f"Pulse amplitude={PULSE_AMP}, N_STEPS={N_STEPS}")
    print()

    # ── 1. Lattice size sweep ──────────────────────────────────────
    print("-" * 80)
    print("1. LATTICE SIZE SWEEP")
    print("-" * 80)
    sizes = [41, 61, 81, 101]
    print(f"{'N':>5s}  {'PosA':>5s}  {'PosB':>5s}  {'Src':>5s}  "
          f"{'CtrlDrift':>12s}  {'MemNet':>12s}  {'MemRaw':>12s}  {'Mem/Amp':>10s}")
    size_results = []
    for n in sizes:
        pos_a = n // 4
        pos_b = 3 * n // 4
        src = n // 2
        p_start = 10
        p_end = 20
        ctrl_d, mem_net, mem_raw = memory_probe(n, pos_a, pos_b, src, p_start, p_end)
        ratio = mem_net / PULSE_AMP
        size_results.append((n, ctrl_d, mem_net, ratio))
        print(f"{n:5d}  {pos_a:5d}  {pos_b:5d}  {src:5d}  "
              f"{ctrl_d:+12.6f}  {mem_net:+12.6f}  {mem_raw:+12.6f}  {ratio:+10.6f}")

    mem_vals = [r[2] for r in size_results]
    mem_mean = np.mean(mem_vals)
    mem_std = np.std(mem_vals)
    print(f"\n  Memory across sizes: mean={mem_mean:+.6f}, std={mem_std:.6f}")
    ctrl_drifts = [r[1] for r in size_results]
    max_ctrl = max(abs(d) for d in ctrl_drifts)
    print(f"  Max |control drift|: {max_ctrl:.6e}")
    if max_ctrl < 1e-10:
        print("  -> PASS: Control drift is zero on all lattice sizes")
    else:
        print(f"  -> NOTE: Small control drift present (max={max_ctrl:.2e})")
    print()

    # ── 2. Pulse position sweep ────────────────────────────────────
    print("-" * 80)
    print("2. PULSE POSITION SWEEP (N=61)")
    print("-" * 80)
    n = 61
    pos_a = 15
    pos_b = 45
    source_positions = [
        ("center (30)", 30),
        ("off-center (20)", 20),
        ("off-center (40)", 40),
        ("near marker A (18)", 18),
        ("near marker B (42)", 42),
    ]
    print(f"  Markers at {pos_a} and {pos_b}")
    print(f"{'Source':>25s}  {'CtrlDrift':>12s}  {'MemNet':>12s}  {'Mem/Amp':>10s}")
    pos_results = []
    for label, src in source_positions:
        ctrl_d, mem_net, _ = memory_probe(n, pos_a, pos_b, src, 10, 20)
        pos_results.append((label, ctrl_d, mem_net))
        print(f"{label:>25s}  {ctrl_d:+12.6f}  {mem_net:+12.6f}  {mem_net/PULSE_AMP:+10.6f}")

    pos_mems = [r[2] for r in pos_results]
    print(f"\n  Memory across positions: mean={np.mean(pos_mems):+.6f}, std={np.std(pos_mems):.6f}")
    all_same_sign = all(m > 0 for m in pos_mems) or all(m < 0 for m in pos_mems)
    print(f"  All same sign: {all_same_sign}")
    print()

    # ── 3. Pulse duration sweep ────────────────────────────────────
    print("-" * 80)
    print("3. PULSE DURATION SWEEP (N=61, center source)")
    print("-" * 80)
    durations = [5, 10, 15, 20]
    print(f"{'Duration':>8s}  {'PulseOn':>7s}  {'PulseOff':>8s}  "
          f"{'CtrlDrift':>12s}  {'MemNet':>12s}  {'Mem/Amp':>10s}  {'Mem/Dur':>10s}")
    dur_results = []
    for dur in durations:
        p_start = 10
        p_end = 10 + dur
        ctrl_d, mem_net, _ = memory_probe(61, 15, 45, 30, p_start, p_end)
        dur_results.append((dur, ctrl_d, mem_net))
        mem_per_dur = mem_net / dur if dur > 0 else 0
        print(f"{dur:8d}  {p_start:7d}  {p_end:8d}  "
              f"{ctrl_d:+12.6f}  {mem_net:+12.6f}  {mem_net/PULSE_AMP:+10.6f}  {mem_per_dur:+10.6f}")

    dur_mems = [r[2] for r in dur_results]
    print(f"\n  Memory across durations: mean={np.mean(dur_mems):+.6f}, std={np.std(dur_mems):.6f}")
    # Check scaling with duration
    if len(dur_mems) >= 2 and abs(dur_mems[0]) > 1e-10:
        ratios = [m / d for m, d in zip(dur_mems, durations)]
        print(f"  Memory/duration ratios: {[f'{r:+.6f}' for r in ratios]}")
        r_mean = np.mean(ratios)
        r_std = np.std(ratios)
        print(f"  Ratio mean={r_mean:+.6f}, std={r_std:.6f}")
        if r_std < 0.5 * abs(r_mean):
            print("  -> Memory scales roughly linearly with pulse duration")
        else:
            print("  -> Memory shows nonlinear duration dependence")
    print()

    # ── 4. Comprehensive control check ─────────────────────────────
    print("-" * 80)
    print("4. CONTROL DRIFT CHECK (all configurations)")
    print("-" * 80)
    all_ctrl = [r[1] for r in size_results] + [r[1] for r in pos_results] + [r[1] for r in dur_results]
    max_ctrl = max(abs(d) for d in all_ctrl)
    mean_ctrl = np.mean([abs(d) for d in all_ctrl])
    print(f"  Total configurations tested: {len(all_ctrl)}")
    print(f"  Max |control drift|:  {max_ctrl:.6e}")
    print(f"  Mean |control drift|: {mean_ctrl:.6e}")
    if max_ctrl < 1e-10:
        print("  -> PASS: Control drift is exactly zero on ALL configurations")
    elif max_ctrl < 1e-6:
        print("  -> PASS: Control drift is negligible (<1e-6) on all configurations")
    else:
        print(f"  -> WARNING: Non-trivial control drift detected (max={max_ctrl:.2e})")
    print()

    # ── 5. Memory/amplitude with error bars ────────────────────────
    print("-" * 80)
    print("5. MEMORY SIGNAL SUMMARY WITH ERROR BARS")
    print("-" * 80)
    all_mems = [r[2] for r in size_results] + [r[2] for r in pos_results] + [r[2] for r in dur_results]
    mem_grand_mean = np.mean(all_mems)
    mem_grand_std = np.std(all_mems)
    mem_grand_se = mem_grand_std / np.sqrt(len(all_mems))
    print(f"  Configurations: {len(all_mems)}")
    print(f"  Memory (net) mean:  {mem_grand_mean:+.6f}")
    print(f"  Memory (net) std:   {mem_grand_std:.6f}")
    print(f"  Memory (net) SE:    {mem_grand_se:.6f}")
    print(f"  Memory/amplitude:   {mem_grand_mean/PULSE_AMP:+.6f} +/- {mem_grand_se/PULSE_AMP:.6f}")
    if abs(mem_grand_mean) > 3 * mem_grand_se and mem_grand_se > 0:
        print("  -> PASS: Memory signal is >3 SE from zero (robust)")
    elif abs(mem_grand_mean) > 2 * mem_grand_se and mem_grand_se > 0:
        print("  -> MARGINAL: Memory signal is >2 SE from zero")
    else:
        print("  -> WEAK: Memory signal not clearly separated from noise")
    print()


# =====================================================================
#  PART B: Weak-Coupling Sign-Regime Robustness
# =====================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
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


def _cn_step_sign(H, psi, dt):
    n = H.shape[0]
    a_plus = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    a_minus = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(a_plus, a_minus.dot(psi))


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


def _shell_force(depth, n, psi, phi):
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1)
    shell_count = np.zeros(max_d + 1)
    shell_prob = np.zeros(max_d + 1)
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


def run_sign_case(pos, col, adj, G, seed):
    """Run attract vs repulse for a single graph/G/seed. Returns (tw_a, tw_r)."""
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    src = int(np.argmin(dists_c))
    depth = _bfs_depth(adj, src, n)
    L = _build_laplacian(pos, adj, n)
    solve_op = (L + MU2 * speye(n, format='csr')).tocsc()

    psi0 = np.exp(-0.5 * dists_c ** 2 / 1.15 ** 2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    results = {}
    for label, phi_sign in [("attract", +1.0), ("repulse", -1.0)]:
        psi = psi0.copy()
        tw = 0
        phi = np.zeros(n)
        for _ in range(N_ITER_SIGN):
            rho = np.abs(psi) ** 2
            phi = phi_sign * spsolve(solve_op, G * rho)
            sf = _shell_force(depth, n, psi, phi)
            if sf > 0:
                tw += 1
            H = _build_hamiltonian(pos, col, adj, n, phi)
            psi = _cn_step_sign(H, psi, DT_SIGN)
        results[label] = tw

    return results["attract"], results["repulse"]


def sign_configs():
    """Return (family_name, builder) tuples."""
    return [
        ("random_geometric", lambda s: make_random_geometric(seed=s, side=8)),
        ("growing", lambda s: make_growing(seed=s, n_target=64)),
        ("layered_cycle", lambda s: make_layered_cycle(seed=s, layers=8, width=8)),
    ]


def run_sign_robustness():
    print("=" * 80)
    print("PART B: WEAK-COUPLING SIGN-REGIME ROBUSTNESS")
    print("=" * 80)
    print(f"MASS={MASS}, MU2={MU2}, DT={DT_SIGN}, N_ITER={N_ITER_SIGN}")
    print(f"G values: {G_VALUES}")
    print(f"Seeds: {SEEDS_SIGN} ({len(SEEDS_SIGN)} per family)")
    print(f"Families: {[c[0] for c in sign_configs()]}")
    print()

    # Collect all results: rows[family][G][seed] = (tw_a, tw_r)
    all_rows = []
    for family_name, builder in sign_configs():
        for G in G_VALUES:
            for seed in SEEDS_SIGN:
                name, pos, col, adj = builder(seed)
                tw_a, tw_r = run_sign_case(pos, col, adj, G, seed)
                all_rows.append({
                    "family": family_name,
                    "G": G,
                    "seed": seed,
                    "tw_a": tw_a,
                    "tw_r": tw_r,
                    "attract_wins": tw_a > tw_r,
                    "margin": tw_a - tw_r,
                })

    # ── Full table ─────────────────────────────────────────────────
    print("-" * 80)
    print("FULL RESULTS TABLE")
    print("-" * 80)
    print(f"{'Family':<20s} {'G':>3s} {'Seed':>4s} {'tw_a':>5s} {'tw_r':>5s} "
          f"{'Margin':>6s} {'A>R':>4s}")
    for row in all_rows:
        flag = "Y" if row["attract_wins"] else "N"
        print(f"{row['family']:<20s} {row['G']:3d} {row['seed']:4d} "
              f"{row['tw_a']:5d} {row['tw_r']:5d} {row['margin']:+6d} {flag:>4s}")

    total = len(all_rows)
    attract_wins_total = sum(1 for r in all_rows if r["attract_wins"])
    print(f"\nOverall attract > repulse: {attract_wins_total}/{total}")
    print()

    # ── Per-G summary ──────────────────────────────────────────────
    print("-" * 80)
    print("PER-G SUMMARY (across all families and seeds)")
    print("-" * 80)
    print(f"{'G':>3s}  {'Runs':>5s}  {'A>R':>5s}  {'Rate':>6s}  "
          f"{'MeanMargin':>11s}  {'StdMargin':>11s}  {'AllPass':>7s}")
    g_window = []
    for G in G_VALUES:
        g_rows = [r for r in all_rows if r["G"] == G]
        n_runs = len(g_rows)
        n_pass = sum(1 for r in g_rows if r["attract_wins"])
        margins = [r["margin"] for r in g_rows]
        m_mean = np.mean(margins)
        m_std = np.std(margins)
        all_pass = n_pass == n_runs
        print(f"{G:3d}  {n_runs:5d}  {n_pass:5d}  {n_pass/n_runs:6.2f}  "
              f"{m_mean:+11.2f}  {m_std:11.2f}  {'YES' if all_pass else 'NO':>7s}")
        if all_pass:
            g_window.append(G)

    print()
    if g_window:
        print(f"  G window where attract > repulse on ALL seeds: {g_window}")
        print(f"  Window: G in [{min(g_window)}, {max(g_window)}]")
    else:
        print("  No G value achieves attract > repulse on ALL seeds")
    print()

    # ── Per-family summary ─────────────────────────────────────────
    print("-" * 80)
    print("PER-FAMILY SUMMARY")
    print("-" * 80)
    for family_name, _ in sign_configs():
        fam_rows = [r for r in all_rows if r["family"] == family_name]
        print(f"\n  {family_name}:")
        print(f"  {'G':>3s}  {'A>R':>5s}/{len(SEEDS_SIGN)}  {'MeanMargin':>11s}  {'AllPass':>7s}")
        fam_window = []
        for G in G_VALUES:
            g_rows = [r for r in fam_rows if r["G"] == G]
            n_pass = sum(1 for r in g_rows if r["attract_wins"])
            margins = [r["margin"] for r in g_rows]
            m_mean = np.mean(margins)
            all_pass = n_pass == len(g_rows)
            print(f"  {G:3d}  {n_pass:5d}/{len(g_rows)}  {m_mean:+11.2f}  "
                  f"{'YES' if all_pass else 'NO':>7s}")
            if all_pass:
                fam_window.append(G)
        if fam_window:
            print(f"  -> Window: G in [{min(fam_window)}, {max(fam_window)}]")
        else:
            print(f"  -> No G value passes ALL seeds")

    print()

    # ── Error bars on margin ───────────────────────────────────────
    print("-" * 80)
    print("MARGIN ERROR BARS (mean +/- SE across seeds)")
    print("-" * 80)
    print(f"{'Family':<20s} {'G':>3s}  {'Mean':>8s}  {'SE':>8s}  {'Lo95':>8s}  {'Hi95':>8s}")
    for family_name, _ in sign_configs():
        for G in G_VALUES:
            g_rows = [r for r in all_rows if r["family"] == family_name and r["G"] == G]
            margins = [r["margin"] for r in g_rows]
            m = np.mean(margins)
            se = np.std(margins) / np.sqrt(len(margins))
            lo = m - 1.96 * se
            hi = m + 1.96 * se
            print(f"{family_name:<20s} {G:3d}  {m:+8.2f}  {se:8.2f}  {lo:+8.2f}  {hi:+8.2f}")

    print()


# =====================================================================
#  MAIN
# =====================================================================

def main():
    t0 = time.time()
    print()
    run_memory_robustness()
    t_mem = time.time()
    print(f"[Memory robustness completed in {t_mem - t0:.1f}s]\n")

    run_sign_robustness()
    t_sign = time.time()
    print(f"[Sign robustness completed in {t_sign - t_mem:.1f}s]")

    # ── Final verdict ──────────────────────────────────────────────
    print()
    print("=" * 80)
    print("OVERALL VERDICT")
    print("=" * 80)
    print(f"Total wall time: {time.time() - t0:.1f}s")
    print()


if __name__ == "__main__":
    main()
