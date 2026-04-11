#!/usr/bin/env python3
"""
Correct Staggered-Gravity Coupling — Three Structures Compared
================================================================
The literature (Zache et al. 2020, Dempsey et al. 2025) shows that
a scalar potential Φ in the staggered Hamiltonian must couple through
the SAME parity factor ε(x) as the mass, because both are scalar
(1⊗1 in spin-taste) couplings to ψ̄ψ.

The full GR coupling via the lapse function (1+Φ) multiplies the
ENTIRE Hamiltonian (equivalence principle):

    H_grav = (1+Φ) · H_flat = (1+Φ) · [m·ε(x) + hopping]

This script compares three coupling structures:

  A) WRONG (current):  H_diag = m·ε − m·Φ     (identity coupling)
  B) SCALAR:           H_diag = (m+Φ)·ε        (parity coupling)
  C) LAPSE:            H = (1+Φ)·H_flat        (full equivalence principle)

For each, we measure:
  - Force sign via exact lattice gradient (1D) and edge-radial (graph)
  - Width evolution (contraction vs expansion)
  - Norm conservation
  - Whether the two signs of Φ (well vs hill) are distinguishable

If coupling B or C produces DIFFERENT physics from A, and specifically
if the force sign depends on Φ sign only under the correct coupling,
that would be a genuine derivation of gravitational attraction.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye, diags
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 50.0
N_ITER = 20


# ── 1D Staggered lattice (exact force available) ───────────────────

def staggered_H_1d(n, mass, V=None, coupling="identity"):
    """Build 1D staggered Hamiltonian with specified coupling.

    coupling = "identity":  H_diag = mass*eps + V        (current wrong way)
    coupling = "parity":    H_diag = (mass + V/mass)*eps  (scalar coupling)
    coupling = "lapse":     H = (1 + V/mass) * H_flat     (equivalence principle)
    """
    H = lil_matrix((n, n), dtype=complex)
    eps = np.array([(-1) ** x for x in range(n)], dtype=float)

    if coupling == "lapse" and V is not None:
        # Build H_flat first, then symmetrize: H_grav = sqrt(N) H_flat sqrt(N)
        # where N = 1 + V/mass (lapse function). This preserves Hermiticity.
        for x in range(n):
            H[x, (x + 1) % n] += -1j / 2
            H[x, (x - 1) % n] += 1j / 2
            H[x, x] += mass * eps[x]
        H = H.tocsr()
        sqrt_lapse = diags(np.sqrt(np.maximum(1.0 + V / mass, 0.01)), format='csr')
        return (sqrt_lapse @ H @ sqrt_lapse).tocsr()
    else:
        for x in range(n):
            H[x, (x + 1) % n] += -1j / 2
            H[x, (x - 1) % n] += 1j / 2
            if V is not None:
                if coupling == "identity":
                    H[x, x] += mass * eps[x] + V[x]
                elif coupling == "parity":
                    H[x, x] += (mass + V[x]) * eps[x]
                else:
                    raise ValueError(f"Unknown coupling: {coupling}")
            else:
                H[x, x] += mass * eps[x]
        return H.tocsr()


def cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def gauss_1d(n, center=None, sigma=None):
    if center is None:
        center = n // 2
    if sigma is None:
        sigma = max(1.5, n / 6)
    psi = np.array([np.exp(-0.5 * ((x - center) / sigma) ** 2) for x in range(n)], dtype=complex)
    return psi / np.linalg.norm(psi)


def build_V_1d(n, mass, g, S, mp):
    """External gravitational potential: V = -m*g*S/(r+0.1)"""
    V = np.zeros(n)
    for y in range(n):
        r = min(abs(y - mp), n - abs(y - mp))
        V[y] = -mass * g * S / (r + 0.1)
    return V


def dVdz_1d(V, n):
    dV = np.zeros(n)
    for y in range(n):
        dV[y] = (V[(y + 1) % n] - V[(y - 1) % n]) / 2
    return dV


def force_on_state(psi, dV):
    """Exact lattice force: F = -<dV/dx>. TOWARD (toward mass) if F > 0."""
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    return -np.sum(rho * dV)


def width_1d(psi, n):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    xs = np.arange(n, dtype=float)
    cx = np.sum(rho * xs)
    return np.sqrt(np.sum(rho * (xs - cx) ** 2))


# ── Graph-based (irregular) ────────────────────────────────────────

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
    return pos, col, {k: list(v) for k, v in adj.items()}


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


def build_H_graph(pos, col, adj, n, mass, phi, coupling="identity"):
    """Build graph Hamiltonian with specified coupling structure."""
    parity = np.where(col == 0, 1.0, -1.0)

    if coupling == "lapse":
        # Build H_flat, then symmetrize: H_grav = sqrt(N) H_flat sqrt(N)
        H = lil_matrix((n, n), dtype=complex)
        H.setdiag(mass * parity)
        for i, nbs in adj.items():
            for j in nbs:
                if i >= j:
                    continue
                d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
                w = 1.0 / max(d, 0.5)
                H[i, j] += -0.5j * w
                H[j, i] += 0.5j * w
        H = H.tocsr()
        sqrt_lapse = diags(np.sqrt(np.maximum(1.0 + phi / mass, 0.01)), format='csr')
        return (sqrt_lapse @ H @ sqrt_lapse).tocsr()
    else:
        H = lil_matrix((n, n), dtype=complex)
        if coupling == "identity":
            H.setdiag(mass * parity - mass * phi)
        elif coupling == "parity":
            H.setdiag((mass + phi) * parity)
        else:
            raise ValueError(f"Unknown coupling: {coupling}")
        for i, nbs in adj.items():
            for j in nbs:
                if i >= j:
                    continue
                d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
                w = 1.0 / max(d, 0.5)
                H[i, j] += -0.5j * w
                H[j, i] += 0.5j * w
        return H.tocsr()


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
            ri = pos[i] - center
            rj = pos[j] - center
            edge_vec = pos[j] - pos[i]
            r_mid = 0.5 * (ri + rj)
            r_norm = np.linalg.norm(r_mid)
            if r_norm < 1e-10:
                continue
            r_hat = r_mid / r_norm
            cos_theta = np.dot(edge_vec, r_hat) / max(d_ij, 1e-10)
            F_edge = w * dphi * (-cos_theta)
            F += 0.5 * (rho[i] + rho[j]) * F_edge
    return F


def width_graph(psi, pos):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2)))


# ── Main comparison ────────────────────────────────────────────────

if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("CORRECT STAGGERED-GRAVITY COUPLING — THREE STRUCTURES")
    print("=" * 78)
    print()
    print("Coupling structures:")
    print("  A) IDENTITY:  H_diag = m·ε + V           (current — wrong per literature)")
    print("  B) PARITY:    H_diag = (m + V)·ε          (scalar 1⊗1 coupling)")
    print("  C) LAPSE:     H = (1 + Φ/m) · H_flat      (equivalence principle)")
    print()

    # ================================================================
    # PART 1: 1D LATTICE — Exact Force
    # ================================================================
    print("=" * 78)
    print("PART 1: 1D LATTICE (n=61) — Exact Force F = -<dV/dx>")
    print("=" * 78)

    n = 61
    c = n // 2
    mp = c + 8  # mass point to the right
    g_coupling = 8.0
    S = 1.0

    V_attr = build_V_1d(n, MASS, g_coupling, S, mp)      # V < 0 (attractive well)
    V_repl = -V_attr                                       # V > 0 (repulsive hill)
    dV_attr = dVdz_1d(V_attr, n)
    dV_repl = dVdz_1d(V_repl, n)

    print(f"\nExternal potential: V = -m*g*S/(r+0.1), g={g_coupling}, mp at {mp}")
    print(f"Attractive well: V_min={V_attr[mp]:.4f} at mass point")
    print(f"Repulsive hill:  V_max={V_repl[mp]:.4f} at mass point")
    print()

    couplings = ["identity", "parity", "lapse"]
    print(f"{'coupling':<12s} {'V_sign':<10s} {'F_exact':>10s} {'|psi|':>10s} {'width_f/w_0':>12s} {'direction':>10s}")
    print("-" * 70)

    for coupling in couplings:
        for v_label, V, dV in [("attract", V_attr, dV_attr), ("repulse", V_repl, dV_repl)]:
            psi = gauss_1d(n)
            w0 = width_1d(psi, n)

            H = staggered_H_1d(n, MASS, V, coupling=coupling)
            for _ in range(N_ITER):
                psi = cn_step(H, psi, DT)

            norm = np.linalg.norm(psi)
            wf = width_1d(psi, n)
            F = force_on_state(psi, dV)

            # For parity/lapse coupling, the force concept needs care:
            # The potential V enters differently, so dV/dx isn't the right gradient.
            # But we can measure the centroid shift as a force proxy.
            rho = np.abs(psi) ** 2
            rho /= np.sum(rho)
            centroid = np.sum(rho * np.arange(n))
            direction = "TOWARD" if (centroid > c and v_label == "attract") or \
                                    (centroid < c and v_label == "repulse") else \
                        "AWAY" if abs(centroid - c) > 0.1 else "NONE"

            # For identity coupling, F = -<dV/dx> is the correct observable
            # For parity/lapse, the effective potential is different
            print(f"{coupling:<12s} {v_label:<10s} {F:+10.4e} {norm:10.6f} {wf/w0:12.4f} {direction:>10s}")

    # Also compute what the EFFECTIVE potential looks like for each coupling
    print(f"\n--- Effective diagonal potential at selected sites ---")
    print(f"{'site':>5s} {'ε(x)':>5s} {'V(x)':>8s} {'identity':>10s} {'parity':>10s}")
    print("-" * 45)
    for x in [c - 2, c - 1, c, c + 1, mp - 1, mp, mp + 1]:
        eps = (-1) ** x
        v = V_attr[x]
        id_diag = MASS * eps + v
        par_diag = (MASS + v) * eps
        print(f"{x:5d} {eps:5.0f} {v:8.4f} {id_diag:10.4f} {par_diag:10.4f}")

    # ================================================================
    # PART 2: SELF-GRAVITY ON GRAPH
    # ================================================================
    print()
    print("=" * 78)
    print("PART 2: SELF-GRAVITY ON RANDOM GEOMETRIC GRAPH (n=64)")
    print("=" * 78)

    pos, col, adj = make_random_geometric(seed=42, side=8)
    n_g = len(pos)
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    src = np.argmin(dists)
    L = graph_laplacian(pos, adj, n_g)
    depth = bfs_depth(adj, src, n_g)

    print(f"\nSelf-gravity: (L+μ²)Φ = G·|ψ|², G={G_SELF}")
    print()
    print(f"{'coupling':<12s} {'|psi|':>10s} {'w_f/w_0':>10s} {'F_edge':>12s} {'contract':>10s}")
    print("-" * 60)

    for coupling in couplings:
        psi = np.exp(-0.5 * np.sum((pos - center) ** 2, axis=1) / 1.15 ** 2).astype(complex)
        psi /= np.linalg.norm(psi)
        w0 = width_graph(psi, pos)

        for it in range(N_ITER):
            rho = np.abs(psi) ** 2
            phi = spsolve((L + MU2 * speye(n_g, format='csr')).tocsc(), G_SELF * rho)
            H = build_H_graph(pos, col, adj, n_g, MASS, phi, coupling=coupling)
            psi = cn_step(H, psi, DT)

        norm = np.linalg.norm(psi)
        wf = width_graph(psi, pos)
        rho = np.abs(psi) ** 2
        phi_final = spsolve((L + MU2 * speye(n_g, format='csr')).tocsc(), G_SELF * rho)
        F_edge = edge_radial_force(pos, adj, n_g, psi, phi_final, depth)
        contract = "CONTRACT" if wf < w0 else "EXPAND"

        print(f"{coupling:<12s} {norm:10.6f} {wf / w0:10.4f} {F_edge:+12.4e} {contract:>10s}")

    # ================================================================
    # PART 3: KEY DIAGNOSTIC — Does parity coupling break the symmetry?
    # ================================================================
    print()
    print("=" * 78)
    print("PART 3: PARITY COUPLING DIAGNOSTIC")
    print("=" * 78)
    print()
    print("Key question: under parity coupling H = (m+Φ)·ε, does the")
    print("wavepacket respond DIFFERENTLY to Φ>0 vs Φ<0?")
    print()
    print("Under identity coupling (H = m·ε + V):")
    print("  V<0 → energy lowered uniformly → attractive well")
    print("  V>0 → energy raised uniformly → repulsive hill")
    print()
    print("Under parity coupling (H = (m+V)·ε):")
    print("  V<0 → gap NARROWED (|m+V| < |m| where V<0)")
    print("  V>0 → gap WIDENED (|m+V| > |m| where V>0)")
    print("  The potential modulates the MASS GAP, not the energy level.")
    print()

    n = 61
    c = n // 2
    mp = c + 8

    for g_val in [2.0, 8.0, 20.0]:
        V = build_V_1d(n, MASS, g_val, 1.0, mp)
        print(f"  g={g_val}:")
        for coupling in ["identity", "parity", "lapse"]:
            psi = gauss_1d(n)
            H = staggered_H_1d(n, MASS, V, coupling=coupling)

            # Measure energy spectrum (gap)
            evals = np.linalg.eigvalsh(H.toarray())
            pos_evals = evals[evals > 0]
            neg_evals = evals[evals < 0]
            if len(pos_evals) > 0 and len(neg_evals) > 0:
                gap = np.min(pos_evals) - np.max(neg_evals)
            else:
                gap = float('nan')

            # Evolve and measure centroid displacement
            for _ in range(N_ITER):
                psi = cn_step(H, psi, DT)
            rho = np.abs(psi) ** 2
            rho /= np.sum(rho)
            centroid = np.sum(rho * np.arange(n))
            displacement = centroid - c

            print(f"    {coupling:<12s} gap={gap:+.4f}  centroid_disp={displacement:+.4f}")

    # ================================================================
    # PART 4: THE REAL TEST — Attractive vs repulsive well
    #         under parity coupling, does the dynamics distinguish?
    # ================================================================
    print()
    print("=" * 78)
    print("PART 4: DOES PARITY COUPLING DISTINGUISH WELL FROM HILL?")
    print("=" * 78)
    print()

    n = 61
    c = n // 2
    mp = c + 8

    print("If parity coupling is correct, V<0 narrows the gap (effective mass")
    print("reduction) while V>0 widens the gap (effective mass increase).")
    print("A narrower gap means faster propagation → wavepacket spreads more")
    print("toward the narrow-gap region. This IS a dynamical prediction.")
    print()

    g_val = 8.0
    V_well = build_V_1d(n, MASS, g_val, 1.0, mp)    # V < 0 at mp
    V_hill = -V_well                                   # V > 0 at mp

    print(f"{'coupling':<12s} {'V_type':<10s} {'centroid':>10s} {'disp':>8s} {'width_f/w_0':>12s} {'interp':>20s}")
    print("-" * 78)

    for coupling in ["identity", "parity", "lapse"]:
        for v_label, V in [("well V<0", V_well), ("hill V>0", V_hill)]:
            psi = gauss_1d(n)
            w0 = width_1d(psi, n)
            H = staggered_H_1d(n, MASS, V, coupling=coupling)
            for _ in range(40):  # more steps for clearer signal
                psi = cn_step(H, psi, DT)
            rho = np.abs(psi) ** 2
            rho /= np.sum(rho)
            centroid = np.sum(rho * np.arange(n))
            wf = width_1d(psi, n)
            disp = centroid - c
            if disp > 0.3:
                interp = "TOWARD mass"
            elif disp < -0.3:
                interp = "AWAY from mass"
            else:
                interp = "negligible"
            print(f"{coupling:<12s} {v_label:<10s} {centroid:10.4f} {disp:+8.4f} {wf/w0:12.4f} {interp:>20s}")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
