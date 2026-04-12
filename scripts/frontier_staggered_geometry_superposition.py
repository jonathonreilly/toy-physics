#!/usr/bin/env python3
"""
Geometry Superposition on Staggered Lattice
=============================================
Test whether staggered fermions can distinguish different geometries
quantum-mechanically: evolve the same initial state on two lattices
with different gravitational potentials, then compare detector states.

TV > 0: geometries produce distinguishable detector states
dphi > 0: real phase difference (gravitational phase shift)
TV_quantum > 0: quantum superposition differs from classical mixture
"""

from __future__ import annotations
import math, time
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30


def make_lattice_1d(n):
    pos = np.array([(float(x), 0.0) for x in range(n)])
    col = np.array([x%2 for x in range(n)], dtype=int)
    adj = {x: [(x+1)%n, (x-1)%n] for x in range(n)}
    return pos, col, adj


def make_lattice_2d(side):
    coords, colors, adj = [], [], {}; idx = 0; index = {}
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y))); colors.append((x+y)%2)
            index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for x in range(side):
        for y in range(side):
            a = index[(x,y)]; adj[a] = []
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                adj[a].append(index[((x+dx)%side, (y+dy)%side)])
    return pos, col, adj


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n,format='csc')+1j*H*dt/2).tocsc()
    am = speye(n,format='csr')-1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def run_test(dim, size, G, source_pos):
    if dim == 1:
        pos, col, adj = make_lattice_1d(size); n = size
    else:
        pos, col, adj = make_lattice_2d(size); n = size*size
    det = list(range(3*n//4, n))

    L = _build_L(pos, adj, n)
    rho_ext = np.zeros(n); rho_ext[source_pos] = G
    phi_B = spsolve((L + MU2*speye(n,format='csr')).tocsc(), rho_ext)

    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center)**2, axis=1))
    psi0 = np.exp(-0.5*dists**2/1.5**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    # Evolve on flat (A) and curved (B)
    H_A = _build_H(pos, col, adj, n, np.zeros(n))
    psi_A = psi0.copy()
    for _ in range(N_STEPS): psi_A = _cn_step(H_A, psi_A, DT)

    H_B = _build_H(pos, col, adj, n, phi_B)
    psi_B = psi0.copy()
    for _ in range(N_STEPS): psi_B = _cn_step(H_B, psi_B, DT)

    # TV distance at detector
    rA = np.abs(psi_A[det])**2; rB = np.abs(psi_B[det])**2
    PA = rA/max(np.sum(rA),1e-20); PB = rB/max(np.sum(rB),1e-20)
    TV = 0.5*np.sum(np.abs(PA - PB))

    # Phase difference
    mask = (np.abs(psi_A[det]) > 1e-10) & (np.abs(psi_B[det]) > 1e-10)
    dphi = np.mean(np.abs(np.angle(psi_A[det][mask]) - np.angle(psi_B[det][mask]))) if np.sum(mask) > 0 else 0.0

    # Quantum vs classical
    psi_s = (psi_A + psi_B); psi_s /= np.linalg.norm(psi_s)
    rmix = 0.5*(np.abs(psi_A)**2 + np.abs(psi_B)**2)
    rsup = np.abs(psi_s)**2
    Pm = rmix[det]/max(np.sum(rmix[det]),1e-20)
    Ps = rsup[det]/max(np.sum(rsup[det]),1e-20)
    TVq = 0.5*np.sum(np.abs(Ps - Pm))

    overlap = np.abs(np.conj(psi_A) @ psi_B)**2
    return {"TV": TV, "dphi": dphi, "TVq": TVq, "overlap": overlap}


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 70)
    print("GEOMETRY SUPERPOSITION ON STAGGERED LATTICE")
    print("=" * 70)

    print("\n--- 1D ---")
    print(f"{'n':>5s} {'G':>6s} {'TV':>8s} {'dphi':>8s} {'TVq':>8s} {'overlap':>8s}")
    print("-" * 45)
    for n in [41, 61, 81]:
        for G in [1.0, 5.0, 10.0, 20.0]:
            r = run_test(1, n, G, n//4)
            print(f"{n:5d} {G:6.1f} {r['TV']:8.4f} {r['dphi']:8.4f} {r['TVq']:8.4f} {r['overlap']:8.4f}")

    print("\n--- 2D ---")
    print(f"{'side':>5s} {'G':>6s} {'TV':>8s} {'dphi':>8s} {'TVq':>8s} {'overlap':>8s}")
    print("-" * 45)
    for side in [8, 10, 12]:
        for G in [1.0, 5.0, 10.0]:
            r = run_test(2, side, G, side*side//4)
            print(f"{side:5d} {G:6.1f} {r['TV']:8.4f} {r['dphi']:8.4f} {r['TVq']:8.4f} {r['overlap']:8.4f}")

    print("\nTV: geometry distinguishability  dphi: gravitational phase shift")
    print("TVq: quantum vs classical mixture  overlap: state fidelity")
    print(f"Time: {time.time()-t0:.1f}s")
