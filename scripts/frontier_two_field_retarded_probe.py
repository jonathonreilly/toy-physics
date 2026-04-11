#!/usr/bin/env python3
"""
Two-Field Retarded/Hybrid Probe: Causal Memory Phi + Staggered psi
==================================================================
Next field-law candidate beyond the wave prototype.

Phi is no longer a pure wave-only field. It carries a causal memory channel:

  dm/dt = (rho - m) / tau_mem
  d²Phi/dt² = -c² (L + mu²) Phi - gamma dPhi/dt + beta * ((1-lam) m + lam rho)

with psi evolving via CN under V = -mass * Phi.

Interpretation:
  - m is a retarded source accumulator
  - Phi is the propagating field
  - the source entering Phi is a hybrid of instantaneous density and lagged
    density history

This is graph-native:
  - no 1D helper fallback
  - tested only on admissible cycle-bearing bipartite graph families

Retained battery:
  R1 Zero-source control
  R2 Source-response linearity
  R3 Additivity
  R4 Force TOWARD
  R5 Iterative stability
  R6 Norm conservation
  R7 State-family robustness
  R8 Native gauge closure
  R9 Force-gap characterization + shell/spectral diagnostics
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass
from collections import deque

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh, spsolve


# ============================================================================
# Parameters
# ============================================================================

DT_MATTER = 0.12
DT_FIELD = 0.03
N_ITER = 30
N_FIELD_STEPS = 10

MASS = 0.30
MU2 = 0.22

FIELD_C = 1.0
FIELD_GAMMA = 0.10
FIELD_BETA = 5.0
FIELD_TAU_MEM = 0.60
FIELD_LAG_BLEND = 0.60


# ============================================================================
# Graph construction
# ============================================================================


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def _bfs(adj, src, n):
    d = np.full(n, np.inf)
    d[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if d[j] == np.inf:
                d[j] = d[i] + 1
                q.append(j)
    return d


def _has_odd_cycle(adj, colors):
    for i, nbs in adj.items():
        for j in nbs:
            if colors[i] == colors[j]:
                return True
    return False


def _find_cycle_edge(adj):
    visited = set()
    for start in sorted(adj):
        if start in visited:
            continue
        stack = [(start, None)]
        while stack:
            node, prev = stack.pop()
            if node in visited:
                return (prev, node) if prev is not None else None
            visited.add(node)
            for nb in adj.get(node, []):
                if nb == prev:
                    continue
                if nb in visited:
                    return (node, nb)
                stack.append((nb, node))
    return None


@dataclass(frozen=True)
class Graph:
    name: str
    pos: np.ndarray
    colors: np.ndarray
    adj: dict
    n: int
    src: int
    depth: np.ndarray
    cycle_edge: tuple | None


def make_random_geometric(seed=42, side=6) -> Graph:
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    adj = {}
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
    adj_l = {k: list(v) for k, v in adj.items()}
    n = len(pos)
    src = n // 2
    return Graph("random_geometric", pos, col, adj_l, n, src, _bfs(adj_l, src, n), _find_cycle_edge(adj_l))


def make_growing(seed=42, n_target=48) -> Graph:
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
    n = len(pos)
    src = 0
    return Graph("growing", pos, col, adj_l, n, src, _bfs(adj_l, src, n), _find_cycle_edge(adj_l))


def make_layered_cycle(seed=42, layers=6, width=4) -> Graph:
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
    return Graph("layered_cycle", pos, col, adj_l, n, src, _bfs(adj_l, src, n), _find_cycle_edge(adj_l))


def make_causal_dag(seed=42, layers=8, width=5) -> Graph:
    """Layered bipartite DAG-like tree: one forward connection per node, no cycles."""
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes = []
    idx = 0
    for layer in range(layers):
        count = 1 if layer == 0 else width
        this_layer = []
        for k in range(count):
            coords.append((float(layer), float(k) + 0.1 * (rng.random() - 0.5)))
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
            j = nxt[(i_pos + layer) % len(nxt)]
            adj[i].add(j)
            adj[j].add(i)
    adj_l = {k: list(v) for k, v in adj.items()}
    src = layer_nodes[0][0]
    return Graph("causal_dag", pos, col, adj_l, n, src, _bfs(adj_l, src, n), None)


# ============================================================================
# Physics tools
# ============================================================================


def _graph_laplacian(g: Graph):
    L = lil_matrix((g.n, g.n), dtype=float)
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(g.pos[j, 0] - g.pos[i, 0], g.pos[j, 1] - g.pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def _build_H(g: Graph, mass, phi):
    H = lil_matrix((g.n, g.n), dtype=complex)
    parity = np.where(g.colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity - mass * phi)
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(g.pos[j, 0] - g.pos[i, 0], g.pos[j, 1] - g.pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _build_H_flux(g: Graph, mass, flux_edge, a_flux):
    H = lil_matrix((g.n, g.n), dtype=complex)
    parity = np.where(g.colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity)
    u, v = min(flux_edge), max(flux_edge)
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(g.pos[j, 0] - g.pos[i, 0], g.pos[j, 1] - g.pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            if (i, j) == (u, v):
                H[i, j] += hop * np.exp(1j * a_flux)
                H[j, i] += np.conj(hop) * np.exp(-1j * a_flux)
            else:
                H[i, j] += hop
                H[j, i] += np.conj(hop)
    return H.tocsr()


def _cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format="csc") + 1j * H * dt / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def _width(psi, pos):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2)))


def _shell_force(g: Graph, psi, phi):
    max_d = int(np.max(g.depth[np.isfinite(g.depth)])) if np.any(np.isfinite(g.depth)) else 0
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    ps = np.zeros(max_d + 1)
    rs = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(g.n):
        d_ = int(g.depth[i]) if np.isfinite(g.depth[i]) else -1
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


def _source_density(g: Graph, strength=1.0):
    center = g.pos[g.src]
    rel = g.pos - center
    w = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / 0.90**2)
    w /= max(np.sum(w), 1e-30)
    return strength * w


def _probe_state(g: Graph, sigma=1.15, k0=0.18):
    center = g.pos[g.src]
    rel = g.pos - center
    coord = rel[:, 0] + 0.35 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / sigma**2) * np.exp(1j * k0 * coord)
    return psi.astype(complex) / np.linalg.norm(psi)


def _color_state(g: Graph, target_color):
    psi = _probe_state(g).copy()
    psi[g.colors != target_color] = 0
    nm = np.linalg.norm(psi)
    return psi / nm if nm > 0 else psi


def _external_phi(g: Graph, strength=1.0):
    center = g.pos[g.src]
    rel = g.pos - center
    r = np.sqrt(rel[:, 0] ** 2 + rel[:, 1] ** 2)
    return strength * np.exp(-0.38 * r) / (r + 0.25)


def _evolve_retarded_field(g: Graph, rho_series, n_steps=N_FIELD_STEPS, phi0=None, pi0=None, mem0=None):
    L = _graph_laplacian(g)
    field_op = -FIELD_C**2 * (L + MU2 * speye(g.n, format="csr"))
    phi = np.zeros(g.n) if phi0 is None else phi0.copy()
    pi = np.zeros(g.n) if pi0 is None else pi0.copy()
    mem = np.zeros(g.n) if mem0 is None else mem0.copy()

    if isinstance(rho_series, (list, tuple)):
        series = list(rho_series)
    else:
        series = [rho_series] * n_steps
    if len(series) < n_steps:
        series.extend([series[-1]] * (n_steps - len(series)))

    for t in range(n_steps):
        rho = np.asarray(series[t], dtype=float)
        mem = mem + DT_FIELD * (rho - mem) / FIELD_TAU_MEM
        source = FIELD_LAG_BLEND * rho + (1.0 - FIELD_LAG_BLEND) * mem
        acc = field_op.dot(phi) - FIELD_GAMMA * pi + FIELD_BETA * source
        pi = pi + 0.5 * DT_FIELD * acc
        phi = phi + DT_FIELD * pi
        acc = field_op.dot(phi) - FIELD_GAMMA * pi + FIELD_BETA * source
        pi = pi + 0.5 * DT_FIELD * acc
    return phi, pi, mem


def _retarded_force_response(g: Graph, source_strength=1.0):
    rho = _source_density(g, strength=source_strength)
    phi, pi, mem = _evolve_retarded_field(g, rho)
    psi = _probe_state(g)
    psi_f = _cn_step(_build_H(g, MASS, phi), psi, DT_MATTER)
    return {
        "phi": phi,
        "pi": pi,
        "mem": mem,
        "psi": psi_f,
        "force": _shell_force(g, psi_f, phi),
        "width": _width(psi_f, g.pos),
        "norm": float(np.linalg.norm(psi_f)),
        "phi_norm": float(np.linalg.norm(phi)),
    }


# ============================================================================
# Battery
# ============================================================================


def run_battery(g: Graph):
    print(f"\n{'=' * 70}")
    print(f"RETARDED/HYBRID BATTERY: {g.name} ({g.n} nodes)")
    print(f"{'=' * 70}")
    if _has_odd_cycle(g.adj, g.colors):
        print("  REJECTED: odd-cycle defect")
        return None

    score = 0
    psi0 = _probe_state(g)

    # R1: zero-source control
    phi0, _, _ = _evolve_retarded_field(g, np.zeros(g.n))
    psi_z = _cn_step(_build_H(g, MASS, phi0), psi0, DT_MATTER)
    F0 = _shell_force(g, psi_z, phi0)
    p = abs(F0) < 1e-10 and np.linalg.norm(phi0) < 1e-10
    score += p
    print(f"  [R1] Zero-source: F={F0:.4e}, |Phi|={np.linalg.norm(phi0):.4e} {'PASS' if p else 'FAIL'}")

    # R2: source-response linearity
    rho_base = _source_density(g)
    strengths = np.array([0.0, 0.25, 0.5, 1.0, 2.0])
    forces = []
    for s in strengths:
        out = _retarded_force_response(g, source_strength=float(s))
        forces.append(out["force"])
    forces = np.array(forces)
    co = np.polyfit(strengths, forces, 1)
    pred = np.polyval(co, strengths)
    denom = np.sum((forces - np.mean(forces)) ** 2)
    r2 = 1 - np.sum((forces - pred) ** 2) / denom if denom > 0 else 1.0
    p = r2 > 0.99
    score += p
    print(f"  [R2] Linearity: R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # R3: additivity
    partner = max(range(g.n), key=lambda i: g.depth[i] if np.isfinite(g.depth[i]) else -1)
    rho_a = _source_density(g)
    center_b = g.pos[partner]
    rel_b = g.pos - center_b
    rho_b = np.exp(-0.5 * (rel_b[:, 0] ** 2 + rel_b[:, 1] ** 2) / 0.90**2)
    rho_b /= max(np.sum(rho_b), 1e-30)
    phi_a, _, _ = _evolve_retarded_field(g, rho_a)
    phi_b, _, _ = _evolve_retarded_field(g, rho_b)
    phi_ab, _, _ = _evolve_retarded_field(g, rho_a + rho_b)
    resid = np.linalg.norm(phi_ab - (phi_a + phi_b)) / max(np.linalg.norm(phi_ab), 1e-30)
    p = resid < 1e-10
    score += p
    print(f"  [R3] Additivity: residual={resid:.4e} {'PASS' if p else 'FAIL'}")

    # R4: force sign
    out = _retarded_force_response(g, source_strength=1.0)
    F_s = out["force"]
    p = F_s > 0
    score += p
    print(f"  [R4] Force: {F_s:+.4e} {'TOWARD PASS' if p else 'AWAY FAIL'}")

    # R5: iterative stability
    psi_it = psi0.copy()
    tw_count = 0
    phi_it = np.zeros(g.n)
    pi_it = np.zeros(g.n)
    mem_it = np.zeros(g.n)
    for _ in range(N_ITER):
        rho_m = np.abs(psi_it) ** 2
        phi_it, pi_it, mem_it = _evolve_retarded_field(g, rho_m, n_steps=1, phi0=phi_it, pi0=pi_it, mem0=mem_it)
        psi_it = _cn_step(_build_H(g, MASS, phi_it), psi_it, DT_MATTER)
        if _shell_force(g, psi_it, phi_it) > 0:
            tw_count += 1
    p = tw_count == N_ITER
    score += p
    print(f"  [R5] Iterative stability: {tw_count}/{N_ITER} TOWARD {'PASS' if p else 'FAIL'}")

    # R6: norm conservation
    norm_drift = abs(np.linalg.norm(psi_it) - 1.0)
    p = norm_drift < 1e-3
    score += p
    print(f"  [R6] Norm: drift={norm_drift:.4e} {'PASS' if p else 'FAIL'}")

    # R7: state-family robustness
    fam_tw = 0
    for label, psi_f in [("gauss", _probe_state(g)), ("color-0", _color_state(g, 0)), ("color-1", _color_state(g, 1))]:
        psi_tmp = psi_f.copy()
        phi_tmp = np.zeros(g.n)
        pi_tmp = np.zeros(g.n)
        mem_tmp = np.zeros(g.n)
        for _ in range(5):
            rho_tmp = np.abs(psi_tmp) ** 2
            phi_tmp, pi_tmp, mem_tmp = _evolve_retarded_field(g, rho_tmp, n_steps=1, phi0=phi_tmp, pi0=pi_tmp, mem0=mem_tmp)
            psi_tmp = _cn_step(_build_H(g, MASS, phi_tmp), psi_tmp, DT_MATTER)
        F_tmp = _shell_force(g, psi_tmp, phi_tmp)
        fam_tw += int(F_tmp > 0)
        print(f"    {label:10s}: F={F_tmp:+.4e} {'TW' if F_tmp > 0 else 'AW'}")
    p = fam_tw == 3
    score += p
    print(f"  [R7] Families: {fam_tw}/3 {'PASS' if p else 'FAIL'}")

    # R8: native gauge
    if g.cycle_edge is not None:
        u, v = g.cycle_edge
        As = np.linspace(0, 2 * np.pi, 13)
        Js = []
        for A in As:
            H_fl = _build_H_flux(g, MASS, g.cycle_edge, A)
            if g.n <= 500:
                ev, ec = np.linalg.eigh(H_fl.toarray())
            else:
                ev, ec = eigsh(H_fl.tocsc(), k=1, which="SA")
            pg = ec[:, 0]
            d = math.hypot(g.pos[max(u, v), 0] - g.pos[min(u, v), 0], g.pos[max(u, v), 1] - g.pos[min(u, v), 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w * np.exp(1j * A)
            Js.append(np.imag(pg[min(u, v)].conj() * hop * pg[max(u, v)]))
        Jr = np.max(Js) - np.min(Js)
        try:
            def sm(A, a, ph, b):
                return a * np.sin(A + ph) + b

            popt, _ = curve_fit(sm, As, np.array(Js), p0=[Jr / 2, 0, np.mean(Js)])
            r2s = 1 - np.sum((np.array(Js) - sm(As, *popt)) ** 2) / np.sum((np.array(Js) - np.mean(Js)) ** 2)
        except Exception:
            r2s = 0.0
        p = Jr > 1e-6 and r2s > 0.9
        score += p
        print(f"  [R8] Gauge: J_range={Jr:.4e}, sin_R^2={r2s:.4f} {'PASS' if p else 'FAIL'}")
    else:
        print("  [R8] Gauge: no cycle found, SKIP")
        score += 0

    # R9: force-gap + shell/spectral diagnostics
    rho_ref = _source_density(g)
    phi_ext = _external_phi(g)
    H_ext = _build_H(g, MASS, phi_ext)
    psi_ext = _cn_step(H_ext, psi0, DT_MATTER)
    F_ext = _shell_force(g, psi_ext, phi_ext)
    out = _retarded_force_response(g, source_strength=1.0)
    F_solve = out["force"]
    gap = abs(F_solve - F_ext) / abs(F_ext) if abs(F_ext) > 1e-30 else 0.0
    G_eff = F_ext / F_solve if abs(F_solve) > 1e-30 else float("inf")

    max_d = int(np.max(g.depth[np.isfinite(g.depth)])) if np.any(np.isfinite(g.depth)) else 0
    ps_sh = np.zeros(max_d + 1)
    pe_sh = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(g.n):
        d_ = int(g.depth[i]) if np.isfinite(g.depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps_sh[d_] += out["phi"][i]
            pe_sh[d_] += phi_ext[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps_sh[d_] /= cnt[d_]
            pe_sh[d_] /= cnt[d_]
    shell_ratio = 0.0
    if max_d > 0:
        denom = pe_sh[0] - pe_sh[min(1, max_d)]
        if abs(denom) > 1e-10:
            shell_ratio = (ps_sh[0] - ps_sh[min(1, max_d)]) / denom

    L = _graph_laplacian(g)
    evals_L, evecs_L = np.linalg.eigh(L.toarray())
    spec_solve = evecs_L.T @ out["phi"]
    spec_ext = evecs_L.T @ phi_ext
    spec_ratios = []
    for k in range(1, min(6, g.n)):
        if abs(spec_ext[k]) > 1e-10:
            spec_ratios.append(abs(spec_solve[k] / spec_ext[k]))
    mean_spec_ratio = float(np.mean(spec_ratios)) if spec_ratios else 0.0

    print(f"  [R9] Gap: G_eff={G_eff:.1f}, shell_grad_ratio={shell_ratio:.3f}, spectral_ratio(modes1-5)={mean_spec_ratio:.3f}")
    score += 1

    print(f"\n  SCORE: {score}/9")
    return score


def main():
    t0 = time.time()
    print("=" * 70)
    print("STAGGERED FERMION — RETARDED/HYBRID TWO-FIELD PROBE")
    print("=" * 70)
    print(
        f"DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}, MASS={MASS}, MU2={MU2}, "
        f"FIELD_C={FIELD_C}, FIELD_GAMMA={FIELD_GAMMA}, FIELD_BETA={FIELD_BETA}, "
        f"FIELD_TAU_MEM={FIELD_TAU_MEM}, FIELD_LAG_BLEND={FIELD_LAG_BLEND}"
    )
    print("Field law: retarded memory channel + damped wave propagation.")
    print("Graph-native only: random geometric, growing, layered cycle.")
    print()

    scores = []
    for builder in (make_random_geometric, make_growing, make_layered_cycle):
        g = builder()
        if g is None:
            print("  REJECTED: graph construction failed.")
            continue
        if _has_odd_cycle(g.adj, g.colors):
            print(f"  REJECTED: {g.name} has odd-cycle defect.")
            continue
        s = run_battery(g)
        if s is not None:
            scores.append(s)

    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {len(scores)} families tested, scores: {scores}")
    print(f"Time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
