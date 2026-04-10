#!/usr/bin/env python3
"""
Native Gauge Closure on Cycle-Bearing Graphs
==============================================
Thread flux through an actual cycle in the graph. Measure persistent
current at the flux edge. No 1D ring fallback.

The staggered Hamiltonian on a bipartite graph with flux A on edge (u,v):
  H[u,v] *= exp(i*A), H[v,u] *= exp(-i*A)
All other entries unchanged. The ground-state persistent current
J(A) = Im(psi*(u) * H[u,v] * psi(v)) should show sin(A) modulation.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve, eigsh
from dataclasses import dataclass
from collections import deque


MASS = 0.30; POISSON_MU2 = 0.22


# ============================================================================
# Graph construction (reuse from iterative closure)
# ============================================================================

def _add_edge(adj, a, b):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)

@dataclass(frozen=True)
class Graph:
    name: str; positions: np.ndarray; colors: np.ndarray
    adj: dict; n: int; has_cycle: bool; cycle_edge: tuple[int,int] | None

def find_cycle_edge(adj: dict) -> tuple[int,int] | None:
    """Find an edge that, if removed, would break a cycle."""
    visited = set(); parent = {}
    for start in sorted(adj):
        if start in visited: continue
        stack = [(start, None)]
        while stack:
            node, prev = stack.pop()
            if node in visited:
                # Found a cycle — the edge (prev_of_node, node) closes it
                # Return the edge that creates the cycle
                return (prev, node) if prev is not None else None
            visited.add(node)
            for nb in adj.get(node, []):
                if nb == prev: continue
                if nb in visited:
                    return (node, nb)  # this edge closes a cycle
                stack.append((nb, node))
    return None

def make_random_geometric(seed=42, side=6) -> Graph:
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x+0.08*(rng.random()-0.5), y+0.08*(rng.random()-0.5)))
            colors.append((x+y)%2); index[(x,y)]=idx; idx+=1
    pos=np.array(coords); col=np.array(colors,dtype=int)
    for i in range(side):
        for j in range(side):
            a=index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj=i+di,j+dj
                if (ii,jj) not in index: continue
                b=index[(ii,jj)]
                if col[a]==col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0],pos[b,1]-pos[a,1])<=1.28:
                    _add_edge(adj,a,b)
    ce = find_cycle_edge({k:list(v) for k,v in adj.items()})
    return Graph("random_geometric", pos, col, {k:list(v) for k,v in adj.items()},
                 len(pos), ce is not None, ce)

def make_growing(seed=42, n_target=48) -> Graph:
    rng = random.Random(seed)
    coords=[(0.0,0.0),(1.0,0.0)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur < n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3)
        new_color=cur%2; coords.append((px,py)); colors.append(new_color)
        opp=[i for i in range(cur) if colors[i]!=new_color]
        if opp:
            dists=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]
            dists.sort()
            for _,j in dists[:min(4,len(dists))]:
                _add_edge(adj,cur,j)
        cur+=1
    pos=np.array(coords); col=np.array(colors,dtype=int)
    ce=find_cycle_edge({k:list(v) for k,v in adj.items()})
    return Graph("growing", pos, col, {k:list(v) for k,v in adj.items()},
                 len(pos), ce is not None, ce)


# ============================================================================
# Staggered H with flux on a specific edge
# ============================================================================

def staggered_H_with_flux(g: Graph, mass: float, A_flux: float,
                           flux_edge: tuple[int,int]) -> csr_matrix:
    """Build staggered H on graph with AB flux A on one edge."""
    n = g.n; H = lil_matrix((n,n), dtype=complex)
    parity = np.where(g.colors==0, 1.0, -1.0)
    H.setdiag(mass * parity)
    u_flux, v_flux = flux_edge
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(g.positions[j,0]-g.positions[i,0],
                          g.positions[j,1]-g.positions[i,1])
            w = 1.0/max(d, 0.5)
            hop = -0.5j * w
            # Apply flux phase to the designated edge
            if (i,j) == (min(u_flux,v_flux), max(u_flux,v_flux)):
                H[i,j] += hop * np.exp(1j*A_flux)
                H[j,i] += np.conj(hop) * np.exp(-1j*A_flux)
            else:
                H[i,j] += hop
                H[j,i] += np.conj(hop)
    return H.tocsr()


def measure_persistent_current(g: Graph, mass: float, flux_edge: tuple[int,int],
                                A_values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Measure ground-state persistent current at the flux edge for each A."""
    u, v = flux_edge
    u_min, v_max = min(u,v), max(u,v)
    currents = []; energies = []

    for A in A_values:
        H = staggered_H_with_flux(g, mass, A, flux_edge)
        n = g.n
        if n <= 500:
            evals, evecs = np.linalg.eigh(H.toarray())
        else:
            evals, evecs = eigsh(H.tocsc(), k=1, which='SA')
        psi_g = evecs[:, 0]
        energies.append(evals[0])

        # Current at the flux edge: J = Im(psi*(u) * H[u,v] * psi(v))
        d = math.hypot(g.positions[v_max,0]-g.positions[u_min,0],
                      g.positions[v_max,1]-g.positions[u_min,1])
        w = 1.0/max(d, 0.5)
        hop = -0.5j * w * np.exp(1j*A)
        J = np.imag(psi_g[u_min].conj() * hop * psi_g[v_max])
        currents.append(J)

    return np.array(currents), np.array(energies)


# ============================================================================
# Test
# ============================================================================

def test_gauge(g: Graph):
    print(f"\n{'='*70}")
    print(f"NATIVE GAUGE: {g.name} ({g.n} nodes)")
    print(f"{'='*70}")

    if not g.has_cycle or g.cycle_edge is None:
        print("  NO CYCLE FOUND — gauge test not applicable.")
        return None

    u, v = g.cycle_edge
    print(f"  Cycle edge: ({u}, {v})")
    print(f"  Edge distance: {math.hypot(g.positions[v,0]-g.positions[u,0], g.positions[v,1]-g.positions[u,1]):.3f}")

    A_values = np.linspace(0, 2*np.pi, 13)
    currents, energies = measure_persistent_current(g, MASS, g.cycle_edge, A_values)

    print(f"\n  Flux sweep:")
    for A, J, E in zip(A_values, currents, energies):
        print(f"    A={A:.2f}: J={J:+.6e}, E_ground={E:.6f}")

    J_range = np.max(currents) - np.min(currents)
    E_range = np.max(energies) - np.min(energies)

    # Check for sin(A) pattern
    # Fit J to a*sin(A + phi) + b
    from scipy.optimize import curve_fit
    def sin_model(A, a, phi, b):
        return a * np.sin(A + phi) + b
    try:
        popt, _ = curve_fit(sin_model, A_values, currents, p0=[J_range/2, 0, np.mean(currents)])
        J_pred = sin_model(A_values, *popt)
        ss_res = np.sum((currents - J_pred)**2)
        ss_tot = np.sum((currents - np.mean(currents))**2)
        r2_sin = 1 - ss_res/ss_tot if ss_tot > 0 else 0
    except:
        r2_sin = 0

    print(f"\n  RESULTS:")
    print(f"    J_range: {J_range:.4e}")
    print(f"    E_range: {E_range:.4e}")
    print(f"    sin(A) fit R^2: {r2_sin:.6f}")
    p = J_range > 1e-6 and r2_sin > 0.9
    print(f"    GAUGE CLOSURE: {'PASS' if p else 'FAIL'}")
    return J_range, r2_sin


if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("NATIVE GAUGE CLOSURE — CYCLE-BEARING GRAPHS")
    print("="*70)
    print("No 1D ring fallback. Flux threaded through actual graph cycle.")
    print()

    for g in [make_random_geometric(seed=42), make_growing(seed=42)]:
        test_gauge(g)

    print(f"\nTotal time: {time.time()-t0:.1f}s")
