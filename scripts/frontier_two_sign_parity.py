#!/usr/bin/env python3
"""
Two-Sign Comparison Under CORRECT Parity Coupling
===================================================
With the literature-correct parity coupling H = (m + Φ)·ε, test whether
the sign of Φ produces distinguishable dynamics:

  Φ > 0 at source  →  mass gap WIDENED   →  slower propagation  →  AWAY?
  Φ < 0 at source  →  mass gap NARROWED  →  faster propagation  →  TOWARD?

If so, attraction is a PREDICTION of the staggered Dirac structure, not
a convention.

Self-gravity always has Φ ≥ 0 (screened Poisson with positive source).
Under parity coupling, positive Φ widens the gap, which should produce
REPULSION (push matter away from high-Φ regions).

But wait — if self-gravity is repulsive under parity coupling, that's
a problem. The potential Φ from |ψ|² will push |ψ|² outward → less
concentration → weaker Φ → the system disperses. This would mean
self-gravity is repulsive by default, and we need Φ < 0 for attraction.

This script tests both scenarios to find the truth.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 50.0
N_ITER = 20


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5),
                            y + 0.08 * (rng.random() - 0.5)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index: continue
                b = index[(ii, jj)]
                if col[a] == col[b]: continue
                if math.hypot(pos[b, 0] - pos[a, 0], pos[b, 1] - pos[a, 1]) <= 1.28:
                    _ae(adj, a, b)
    return pos, col, {k: list(v) for k, v in adj.items()}


def graph_laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w; L[j, i] -= w; L[i, i] += w; L[j, j] += w
    return L.tocsr()


def build_H_parity(pos, col, adj, n, mass, phi):
    """Correct parity coupling: H_diag = (mass + phi) * parity"""
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(col == 0, 1.0, -1.0)
    H.setdiag((mass + phi) * parity)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w; H[j, i] += 0.5j * w
    return H.tocsr()


def build_H_identity(pos, col, adj, n, mass, phi, sign):
    """Old identity coupling for comparison: H_diag = mass*parity + sign*mass*phi"""
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(col == 0, 1.0, -1.0)
    H.setdiag(mass * parity + sign * mass * phi)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w; H[j, i] += 0.5j * w
    return H.tocsr()


def cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def bfs_depth(adj, src, n):
    depth = np.full(n, np.inf); depth[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1; q.append(j)
    return depth


def width(psi, pos):
    rho = np.abs(psi) ** 2; rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0]); cy = np.sum(rho * pos[:, 1])
    return np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2)))


def shell_force(depth, n, psi, phi):
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d <= 0: return 0.0
    rho = np.abs(psi) ** 2
    ps = np.zeros(max_d + 1); rs = np.zeros(max_d + 1); cnt = np.zeros(max_d + 1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]; rs[d_] += rho[i]; cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0: ps[d_] /= cnt[d_]; rs[d_] /= cnt[d_]
    grad = np.zeros(max_d + 1)
    for d_ in range(max_d + 1):
        if d_ == 0: grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d: grad[d_] = ps[d_ - 1] - ps[d_]
        else: grad[d_] = 0.5 * (ps[d_ - 1] - ps[d_ + 1])
    return float(np.sum(rs * grad))


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("TWO-SIGN COMPARISON UNDER PARITY COUPLING")
    print("=" * 78)

    pos, col, adj = make_random_geometric(seed=42, side=8)
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    src = np.argmin(dists)
    L = graph_laplacian(pos, adj, n)
    depth = bfs_depth(adj, src, n)

    print(f"\nGraph: random geometric, n={n}")
    print(f"Self-gravity: (L+μ²)Φ = G·|ψ|², G={G_SELF}")
    print()

    # ── Test 1: Self-gravity with parity coupling ──
    # Φ = (L+μ²)⁻¹ G·|ψ|² ≥ 0 always
    # Under parity coupling: H = (m+Φ)·ε → gap widened → repulsive??
    print("--- TEST 1: Self-gravity, Φ ≥ 0 (screened Poisson) ---")
    print()

    for label, coupling_fn in [
        ("identity(-)", lambda phi: build_H_identity(pos, col, adj, n, MASS, phi, -1.0)),
        ("identity(+)", lambda phi: build_H_identity(pos, col, adj, n, MASS, phi, +1.0)),
        ("parity",      lambda phi: build_H_parity(pos, col, adj, n, MASS, phi)),
    ]:
        psi = np.exp(-0.5 * np.sum((pos - center) ** 2, axis=1) / 1.15 ** 2).astype(complex)
        psi /= np.linalg.norm(psi)
        w0 = width(psi, pos)

        for it in range(N_ITER):
            rho = np.abs(psi) ** 2
            phi = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), G_SELF * rho)
            H = coupling_fn(phi)
            psi = cn_step(H, psi, DT)

        rho = np.abs(psi) ** 2
        phi_f = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), G_SELF * rho)
        wf = width(psi, pos)
        F = shell_force(depth, n, psi, phi_f)
        contract = "CONTRACT" if wf < w0 else "EXPAND"
        direction = "TOWARD" if F > 0 else "AWAY"

        print(f"  {label:<15s}  w_f/w_0={wf/w0:.4f} {contract:>8s}  F={F:+.4e} {direction}")

    # ── Test 2: External potential, both signs ──
    print()
    print("--- TEST 2: External source (delta at node 0), both Φ signs ---")
    print()

    rho_ext = np.zeros(n)
    rho_ext[src] = 1.0
    phi_pos = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), 8.0 * rho_ext)  # Φ > 0
    phi_neg = -phi_pos  # Φ < 0

    for phi_label, phi_ext in [("Φ>0 (standard)", phi_pos), ("Φ<0 (inverted)", phi_neg)]:
        print(f"  {phi_label}:")
        for label, coupling_fn in [
            ("identity(-)", lambda phi: build_H_identity(pos, col, adj, n, MASS, phi, -1.0)),
            ("identity(+)", lambda phi: build_H_identity(pos, col, adj, n, MASS, phi, +1.0)),
            ("parity",      lambda phi: build_H_parity(pos, col, adj, n, MASS, phi)),
        ]:
            psi = np.exp(-0.5 * np.sum((pos - center) ** 2, axis=1) / 1.15 ** 2).astype(complex)
            psi /= np.linalg.norm(psi)
            w0 = width(psi, pos)

            H = coupling_fn(phi_ext)
            for _ in range(N_ITER):
                psi = cn_step(H, psi, DT)

            wf = width(psi, pos)
            F = shell_force(depth, n, psi, phi_ext)
            contract = "CONTRACT" if wf < w0 else "EXPAND"
            direction = "TOWARD" if F > 0 else "AWAY"

            print(f"    {label:<15s}  w_f/w_0={wf/w0:.4f} {contract:>8s}  F={F:+.4e} {direction}")
        print()

    # ── Test 3: The key question for self-gravity ──
    print("--- TEST 3: Self-gravity with NEGATIVE Φ (inverted Poisson) ---")
    print("  If (L+μ²)Φ = G·ρ gives Φ>0, then Φ_attract = -Φ gives gap narrowing.")
    print()

    for label, phi_sign, coupling_fn in [
        ("parity, Φ>0",   +1.0, lambda phi: build_H_parity(pos, col, adj, n, MASS, phi)),
        ("parity, Φ<0",   -1.0, lambda phi: build_H_parity(pos, col, adj, n, MASS, phi)),
    ]:
        psi = np.exp(-0.5 * np.sum((pos - center) ** 2, axis=1) / 1.15 ** 2).astype(complex)
        psi /= np.linalg.norm(psi)
        w0 = width(psi, pos)
        widths = [w0]

        for it in range(N_ITER):
            rho = np.abs(psi) ** 2
            phi_raw = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), G_SELF * rho)
            phi = phi_sign * phi_raw
            H = coupling_fn(phi)
            psi = cn_step(H, psi, DT)
            widths.append(width(psi, pos))

        rho = np.abs(psi) ** 2
        phi_f = phi_sign * spsolve((L + MU2 * speye(n, format='csr')).tocsc(), G_SELF * rho)
        F = shell_force(depth, n, psi, phi_f)
        norm = np.linalg.norm(psi)
        contract = "CONTRACT" if widths[-1] < w0 else "EXPAND"
        direction = "TOWARD" if F > 0 else "AWAY"

        print(f"  {label:<15s}  w_f/w_0={widths[-1]/w0:.4f} {contract:>8s}  F={F:+.4e} {direction}  norm={norm:.6f}")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
