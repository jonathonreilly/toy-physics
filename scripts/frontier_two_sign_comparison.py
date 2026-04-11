#!/usr/bin/env python3
"""
Two-Sign Comparison — Does Consistency Select the Coupling Sign?
=================================================================
Run both  −mass·Φ  (attractive) and  +mass·Φ  (repulsive) through an
identical test battery.  If the repulsive sign produces pathologies
(divergent norm, unstable backreaction, unphysical spectrum) while
the attractive sign is stable, that is evidence the sign is selected
by consistency rather than being a free parameter.

Tests:
  T1  Norm drift        — |ψ| after N_ITER self-gravity steps
  T2  Width evolution    — does wavepacket contract (attractive) or explode?
  T3  Force sign         — shell-mean, probability-weighted, edge-radial
  T4  Φ convergence      — does the field settle or oscillate?
  T5  Energy boundedness — is ⟨H⟩ finite and monotonic?
  T6  Spectral stability — eigenvalue spread of H at final iteration

Graph families: random geometric, growing, layered cycle (all bipartite).
Each family tested with both signs at matched parameters.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve, eigsh
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 50.0
N_ITER = 20


# ── Graph construction ──────────────────────────────────────────────

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    adj = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5),
                            y + 0.08 * (rng.random() - 0.5)))
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
    coords = []
    colors = []
    layer_nodes = []
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


# ── Physics primitives ──────────────────────────────────────────────

def graph_laplacian(pos, adj, n):
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


def solve_phi(L, n, rho):
    A = (L + MU2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


def build_H(pos, col, adj, n, mass, phi, sign):
    """Build staggered Hamiltonian with gravitational coupling.

    sign = -1  →  H_diag = mass·parity − mass·Φ  (attractive, standard)
    sign = +1  →  H_diag = mass·parity + mass·Φ  (repulsive, test)
    """
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(col == 0, 1.0, -1.0)
    H.setdiag(mass * parity + sign * mass * phi)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w
    return H.tocsr()


def cn_step(H, n, psi, dt):
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def bfs_depth(adj, src, n):
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


def width(psi, pos):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2)))


# ── Force measures (three independent) ─────────────────────────────

def shell_mean_force(depth, n, psi, phi):
    """Shell-mean radial force proxy (weakest — shell size enters)."""
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    ps = np.zeros(max_d + 1)
    rs = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]
            rs[d_] += rho[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps[d_] /= cnt[d_]
            rs[d_] /= cnt[d_]
    grad = np.zeros(max_d + 1)
    for d_ in range(max_d + 1):
        if d_ == 0:
            grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d:
            grad[d_] = ps[d_ - 1] - ps[d_]
        else:
            grad[d_] = 0.5 * (ps[d_ - 1] - ps[d_ + 1])
    return float(np.sum(rs * grad))


def prob_weighted_shell_force(depth, n, psi, phi):
    """Probability-weighted shell force (stronger proxy)."""
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    ps = np.zeros(max_d + 1)
    P_shell = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]
            P_shell[d_] += rho[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps[d_] /= cnt[d_]
    grad = np.zeros(max_d + 1)
    for d_ in range(max_d + 1):
        if d_ == 0:
            grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d:
            grad[d_] = ps[d_ - 1] - ps[d_]
        else:
            grad[d_] = 0.5 * (ps[d_ - 1] - ps[d_ + 1])
    return float(np.sum(P_shell * grad))


def edge_radial_force(pos, adj, n, psi, phi, depth):
    """Edge-radial force: exact per-edge, radial projection."""
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    center = pos[np.argmin(depth)]
    F = 0.0
    for i, nbs in adj.items():
        if not np.isfinite(depth[i]):
            continue
        for j in nbs:
            if j <= i:
                continue
            if not np.isfinite(depth[j]):
                continue
            d_ij = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d_ij, 0.5)
            dphi = phi[j] - phi[i]
            # Radial direction from i toward center
            ri = pos[i] - center
            rj = pos[j] - center
            edge_vec = pos[j] - pos[i]
            r_mid = 0.5 * (ri + rj)
            r_norm = np.linalg.norm(r_mid)
            if r_norm < 1e-10:
                continue
            r_hat = r_mid / r_norm
            cos_theta = np.dot(edge_vec, r_hat) / max(d_ij, 1e-10)
            # Force contribution: weight * dphi * cos(theta) * rho
            # Positive = inward (toward center/source)
            F_edge = w * dphi * (-cos_theta)
            F += 0.5 * (rho[i] + rho[j]) * F_edge
    return F


# ── Main comparison ────────────────────────────────────────────────

def run_self_gravity(name, pos, col, adj, sign_label, sign_val):
    """Run N_ITER self-gravity steps with the given coupling sign.

    Returns dict of diagnostics.
    """
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    src = np.argmin(dists)

    L = graph_laplacian(pos, adj, n)
    depth = bfs_depth(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0

    # Initial Gaussian wavepacket centered on graph
    psi = np.exp(-0.5 * np.sum((pos - center) ** 2, axis=1) / 1.15 ** 2).astype(complex)
    psi /= np.linalg.norm(psi)

    w0 = width(psi, pos)
    norms = [np.linalg.norm(psi)]
    widths = [w0]
    phi_norms = []
    energies = []
    force_history = []

    for it in range(N_ITER):
        rho = np.abs(psi) ** 2
        phi = solve_phi(L, n, G_SELF * rho)
        phi_norms.append(np.linalg.norm(phi))

        H = build_H(pos, col, adj, n, MASS, phi, sign_val)

        # Energy
        E = np.real(np.conj(psi) @ H.dot(psi))
        energies.append(E)

        # Evolve
        psi = cn_step(H, n, psi, DT)
        norms.append(np.linalg.norm(psi))
        widths.append(width(psi, pos))

    # Final measurements
    rho = np.abs(psi) ** 2
    phi_final = solve_phi(L, n, G_SELF * rho)
    H_final = build_H(pos, col, adj, n, MASS, phi_final, sign_val)

    f_shell = shell_mean_force(depth, n, psi, phi_final)
    f_prob = prob_weighted_shell_force(depth, n, psi, phi_final)
    f_edge = edge_radial_force(pos, adj, n, psi, phi_final, depth)

    # Spectral check (5 lowest + 5 highest eigenvalues)
    try:
        evals_lo = eigsh(H_final.tocsc(), k=min(5, n - 2), which='SA', return_eigenvectors=False)
        evals_hi = eigsh(H_final.tocsc(), k=min(5, n - 2), which='LA', return_eigenvectors=False)
        spectral_range = float(np.max(evals_hi) - np.min(evals_lo))
        spectral_ok = np.all(np.isfinite(evals_lo)) and np.all(np.isfinite(evals_hi))
    except Exception:
        spectral_range = float('nan')
        spectral_ok = False

    norm_drift = abs(norms[-1] - 1.0)
    width_ratio = widths[-1] / w0
    phi_stable = (max(phi_norms) / min(phi_norms) < 10) if min(phi_norms) > 1e-15 else False
    energy_bounded = all(np.isfinite(e) for e in energies)
    energy_monotonic = all(energies[i] <= energies[i + 1] + 1e-8 for i in range(len(energies) - 1)) or \
                       all(energies[i] >= energies[i + 1] - 1e-8 for i in range(len(energies) - 1))

    return {
        'name': name,
        'sign': sign_label,
        'n': n,
        'norm_drift': norm_drift,
        'width_ratio': width_ratio,
        'f_shell': f_shell,
        'f_prob': f_prob,
        'f_edge': f_edge,
        'phi_stable': phi_stable,
        'energy_bounded': energy_bounded,
        'energy_monotonic': energy_monotonic,
        'spectral_range': spectral_range,
        'spectral_ok': spectral_ok,
        'energies': energies,
        'norms': norms,
        'widths': widths,
        'phi_norms': phi_norms,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("TWO-SIGN COMPARISON: Does Consistency Select the Coupling Sign?")
    print("=" * 78)
    print()
    print("Sign convention:")
    print("  ATTRACTIVE: H_diag = mass·parity − mass·Φ  (standard Newtonian)")
    print("  REPULSIVE:  H_diag = mass·parity + mass·Φ  (anti-gravitational)")
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, G_SELF={G_SELF}, N_ITER={N_ITER}")
    print()

    families = [
        make_random_geometric(seed=42, side=8),
        make_growing(seed=42, n_target=64),
        make_layered_cycle(seed=42, layers=8, width=8),
    ]

    all_results = []
    for fname, pos, col, adj in families:
        for sign_label, sign_val in [("attractive", -1.0), ("repulsive", +1.0)]:
            r = run_self_gravity(fname, pos, col, adj, sign_label, sign_val)
            all_results.append(r)

    # ── Report ──────────────────────────────────────────────────────
    print("-" * 78)
    hdr = f"{'family':<20s} {'sign':<12s} {'n':>4s} {'norm_drift':>10s} {'w_ratio':>8s} {'f_shell':>10s} {'f_prob':>10s} {'f_edge':>10s} {'Φ_stab':>7s} {'E_bnd':>6s} {'spec_rng':>9s}"
    print(hdr)
    print("-" * 78)
    for r in all_results:
        print(f"{r['name']:<20s} {r['sign']:<12s} {r['n']:4d} "
              f"{r['norm_drift']:10.2e} {r['width_ratio']:8.4f} "
              f"{r['f_shell']:+10.3e} {r['f_prob']:+10.3e} {r['f_edge']:+10.3e} "
              f"{'OK' if r['phi_stable'] else 'UNSTAB':>7s} "
              f"{'OK' if r['energy_bounded'] else 'DIV':>6s} "
              f"{r['spectral_range']:9.2f}" if np.isfinite(r['spectral_range']) else
              f"{r['name']:<20s} {r['sign']:<12s} {r['n']:4d} "
              f"{r['norm_drift']:10.2e} {r['width_ratio']:8.4f} "
              f"{r['f_shell']:+10.3e} {r['f_prob']:+10.3e} {r['f_edge']:+10.3e} "
              f"{'OK' if r['phi_stable'] else 'UNSTAB':>7s} "
              f"{'OK' if r['energy_bounded'] else 'DIV':>6s} "
              f"{'NaN':>9s}")

    # ── Detailed comparison ─────────────────────────────────────────
    print()
    print("=" * 78)
    print("DETAILED COMPARISON")
    print("=" * 78)

    for fname, _, _, _ in families:
        attr = [r for r in all_results if r['name'] == fname and r['sign'] == 'attractive'][0]
        repl = [r for r in all_results if r['name'] == fname and r['sign'] == 'repulsive'][0]

        print(f"\n--- {fname} (n={attr['n']}) ---")

        # T1: Norm drift
        print(f"  T1 Norm drift:     attractive={attr['norm_drift']:.2e}  repulsive={repl['norm_drift']:.2e}")
        if repl['norm_drift'] > 10 * attr['norm_drift'] and repl['norm_drift'] > 1e-3:
            print(f"     → REPULSIVE norm drift {repl['norm_drift']/attr['norm_drift']:.0f}× worse")
        elif attr['norm_drift'] > 10 * repl['norm_drift'] and attr['norm_drift'] > 1e-3:
            print(f"     → ATTRACTIVE norm drift {attr['norm_drift']/repl['norm_drift']:.0f}× worse")
        else:
            print(f"     → comparable")

        # T2: Width evolution
        print(f"  T2 Width ratio:    attractive={attr['width_ratio']:.4f}  repulsive={repl['width_ratio']:.4f}")
        if attr['width_ratio'] < 1.0 and repl['width_ratio'] > 1.0:
            print(f"     → attractive CONTRACTS, repulsive EXPANDS — sign-selected")
        elif attr['width_ratio'] > 1.0 and repl['width_ratio'] < 1.0:
            print(f"     → attractive EXPANDS, repulsive CONTRACTS — reversed")
        else:
            same = "both contract" if attr['width_ratio'] < 1.0 else "both expand"
            print(f"     → {same}")

        # T3: Force sign
        print(f"  T3 Forces:")
        print(f"     shell_mean:     attractive={attr['f_shell']:+.3e}  repulsive={repl['f_shell']:+.3e}")
        print(f"     prob_weighted:  attractive={attr['f_prob']:+.3e}  repulsive={repl['f_prob']:+.3e}")
        print(f"     edge_radial:    attractive={attr['f_edge']:+.3e}  repulsive={repl['f_edge']:+.3e}")
        # Check sign flip
        a_signs = [attr['f_shell'] > 0, attr['f_prob'] > 0, attr['f_edge'] > 0]
        r_signs = [repl['f_shell'] > 0, repl['f_prob'] > 0, repl['f_edge'] > 0]
        if all(a_signs) and not any(r_signs):
            print(f"     → ALL THREE MEASURES flip sign: attractive=TOWARD, repulsive=AWAY")
        elif all(a_signs) and all(r_signs):
            print(f"     → Both TOWARD — force sign does NOT distinguish coupling sign")
        else:
            print(f"     → Mixed: attractive={sum(a_signs)}/3 TOWARD, repulsive={sum(r_signs)}/3 TOWARD")

        # T4: Phi convergence
        print(f"  T4 Φ stable:       attractive={'OK' if attr['phi_stable'] else 'UNSTABLE'}  "
              f"repulsive={'OK' if repl['phi_stable'] else 'UNSTABLE'}")

        # T5: Energy
        print(f"  T5 Energy bounded: attractive={'OK' if attr['energy_bounded'] else 'DIVERGENT'}  "
              f"repulsive={'OK' if repl['energy_bounded'] else 'DIVERGENT'}")
        print(f"     E_final:        attractive={attr['energies'][-1]:+.4f}  repulsive={repl['energies'][-1]:+.4f}")
        e_drift_a = abs(attr['energies'][-1] - attr['energies'][0])
        e_drift_r = abs(repl['energies'][-1] - repl['energies'][0])
        print(f"     |ΔE|:           attractive={e_drift_a:.4f}  repulsive={e_drift_r:.4f}")

        # T6: Spectral range
        print(f"  T6 Spectral range: attractive={attr['spectral_range']:.2f}  repulsive={repl['spectral_range']:.2f}")
        if repl['spectral_range'] > 3 * attr['spectral_range']:
            print(f"     → repulsive spectrum {repl['spectral_range']/attr['spectral_range']:.1f}× wider — less stable")
        elif attr['spectral_range'] > 3 * repl['spectral_range']:
            print(f"     → attractive spectrum {attr['spectral_range']/repl['spectral_range']:.1f}× wider")
        else:
            print(f"     → comparable")

    # ── Verdict ─────────────────────────────────────────────────────
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    # Count pathologies
    a_pathologies = 0
    r_pathologies = 0
    selection_evidence = []

    for fname, _, _, _ in families:
        attr = [r for r in all_results if r['name'] == fname and r['sign'] == 'attractive'][0]
        repl = [r for r in all_results if r['name'] == fname and r['sign'] == 'repulsive'][0]

        # Width: contraction under attractive is physically expected
        if attr['width_ratio'] < 1.0 and repl['width_ratio'] > 1.0:
            selection_evidence.append(f"{fname}: width contracts (attractive) vs expands (repulsive)")

        # Norm stability
        if repl['norm_drift'] > 1e-2 and attr['norm_drift'] < 1e-2:
            r_pathologies += 1
            selection_evidence.append(f"{fname}: repulsive norm unstable ({repl['norm_drift']:.2e})")
        if attr['norm_drift'] > 1e-2 and repl['norm_drift'] < 1e-2:
            a_pathologies += 1

        # Energy divergence
        if not repl['energy_bounded'] and attr['energy_bounded']:
            r_pathologies += 1
            selection_evidence.append(f"{fname}: repulsive energy diverges")
        if not attr['energy_bounded'] and repl['energy_bounded']:
            a_pathologies += 1

        # Phi stability
        if not repl['phi_stable'] and attr['phi_stable']:
            r_pathologies += 1
            selection_evidence.append(f"{fname}: repulsive Φ unstable")

        # Spectral blowup
        if np.isfinite(repl['spectral_range']) and np.isfinite(attr['spectral_range']):
            if repl['spectral_range'] > 5 * attr['spectral_range']:
                r_pathologies += 1
                selection_evidence.append(f"{fname}: repulsive spectrum {repl['spectral_range']/attr['spectral_range']:.1f}× wider")

    if r_pathologies > 0 and a_pathologies == 0:
        print(f"CONSISTENCY SELECTS ATTRACTIVE SIGN")
        print(f"  Repulsive coupling shows {r_pathologies} pathologies across {len(families)} families.")
        print(f"  Attractive coupling shows 0 pathologies.")
        print(f"  Evidence:")
        for e in selection_evidence:
            print(f"    - {e}")
    elif a_pathologies > 0 and r_pathologies == 0:
        print(f"CONSISTENCY SELECTS REPULSIVE SIGN (unexpected)")
        print(f"  Attractive coupling shows {a_pathologies} pathologies.")
    elif r_pathologies > 0 and a_pathologies > 0:
        print(f"BOTH SIGNS SHOW PATHOLOGIES — no clean selection")
        print(f"  Attractive: {a_pathologies}, Repulsive: {r_pathologies}")
    else:
        print(f"BOTH SIGNS ARE STABLE — no consistency-based selection")
        print(f"  The coupling sign remains a free parameter at these parameters.")
        print(f"  The attractive coupling is a Newtonian-convention INPUT, not a prediction.")
        if selection_evidence:
            print(f"  Weaker evidence from width/force behavior:")
            for e in selection_evidence:
                print(f"    - {e}")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
