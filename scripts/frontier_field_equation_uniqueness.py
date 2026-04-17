#!/usr/bin/env python3
"""
Field Equation Uniqueness Test
===============================
Is the screened Poisson equation (L + μ²)Φ = G·ρ uniquely selected by
consistency requirements, or could a different field equation work equally well?

Tests three alternative field equations against screened Poisson:
  F1: Screened Poisson (L + μ²)Φ = ρ          — current default
  F2: Bare Laplacian   L·Φ = ρ                — no screening
  F3: Biharmonic       L²·Φ = ρ               — higher-order (smoother)
  F4: Heat kernel      Φ = exp(-τL)·ρ          — diffusion-based

For each, run the self-gravity battery on random geometric graph and measure:
  - Force sign (TOWARD?)
  - Width contraction (w_f/w_0 < 1?)
  - Norm conservation
  - Iterative stability (does backreaction converge?)
  - G_eff (coupling strength vs 1/r kernel)

If only screened Poisson passes all tests, it's uniquely selected by
consistency. If multiple pass, the field equation is a free parameter.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve, expm_multiply
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 50.0
N_ITER = 20
HEAT_TAU = 0.5


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08*(rng.random()-0.5), y + 0.08*(rng.random()-0.5)))
            colors.append((x+y) % 2)
            index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj = i+di, j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a] == col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0], pos[b,1]-pos[a,1]) <= 1.28:
                    _ae(adj, a, b)
    return pos, col, {k: list(v) for k,v in adj.items()}


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def solve_field(L, n, rho, method):
    """Solve for Φ using the specified field equation."""
    if method == "screened_poisson":
        A = (L + MU2 * speye(n, format='csr')).tocsc()
        return spsolve(A, rho)
    elif method == "bare_laplacian":
        # L is singular (zero eigenvalue for constant mode). Regularize.
        A = (L + 1e-4 * speye(n, format='csr')).tocsc()
        return spsolve(A, rho)
    elif method == "biharmonic":
        A = (L @ L + MU2 * speye(n, format='csr')).tocsc()
        return spsolve(A, rho)
    elif method == "heat_kernel":
        return expm_multiply(-HEAT_TAU * L, rho)
    else:
        raise ValueError(f"Unknown method: {method}")


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
    ap = (speye(n, format='csc') + 1j*H*dt/2).tocsc()
    am = speye(n, format='csr') - 1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def _bfs_depth(adj, src, n):
    depth = np.full(n, np.inf); depth[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf: depth[j] = depth[i]+1; q.append(j)
    return depth


def _width(psi, pos):
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    cx = np.sum(rho*pos[:,0]); cy = np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2 + (pos[:,1]-cy)**2)))


def _shell_force(depth, n, psi, phi):
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d <= 0: return 0.0
    rho = np.abs(psi)**2; rho_n = rho/np.sum(rho)
    ps = np.zeros(max_d+1); P = np.zeros(max_d+1); cnt = np.zeros(max_d+1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]; P[d_] += rho_n[i]; cnt[d_] += 1
    for d_ in range(max_d+1):
        if cnt[d_] > 0: ps[d_] /= cnt[d_]
    grad = np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_ == 0: grad[d_] = ps[0] - ps[min(1,max_d)]
        elif d_ == max_d: grad[d_] = ps[d_-1] - ps[d_]
        else: grad[d_] = 0.5*(ps[d_-1] - ps[d_+1])
    return float(np.sum(P * grad))


def run_battery(pos, col, adj, method):
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))
    src = np.argmin(dists_c)
    L = _build_L(pos, adj, n)
    depth = _bfs_depth(adj, src, n)

    psi = np.exp(-0.5 * dists_c**2 / 1.15**2).astype(complex)
    psi /= np.linalg.norm(psi)
    w0 = _width(psi, pos)

    norms = [np.linalg.norm(psi)]
    widths = [w0]
    forces = []
    phi_norms = []

    for it in range(N_ITER):
        rho = np.abs(psi)**2
        try:
            phi = solve_field(L, n, G_SELF * rho, method)
        except Exception as e:
            return {"method": method, "error": str(e)}
        if not np.all(np.isfinite(phi)):
            return {"method": method, "error": "NaN in phi"}
        phi_norms.append(np.linalg.norm(phi))
        F = _shell_force(depth, n, psi, phi)
        forces.append(F)
        H = _build_H(pos, col, adj, n, phi)
        psi = _cn_step(H, psi, DT)
        norms.append(np.linalg.norm(psi))
        widths.append(_width(psi, pos))

    norm_drift = abs(norms[-1] - 1.0)
    w_ratio = widths[-1] / w0
    tw_count = sum(1 for f in forces if f > 0)
    phi_stable = (max(phi_norms) / max(min(phi_norms), 1e-15)) < 10
    contracts = w_ratio < 1.0

    return {
        "method": method,
        "norm_drift": norm_drift,
        "w_ratio": w_ratio,
        "contracts": contracts,
        "tw_count": tw_count,
        "total_iter": N_ITER,
        "phi_stable": phi_stable,
        "F_final": forces[-1],
        "phi_range": (min(phi_norms), max(phi_norms)),
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("FIELD EQUATION UNIQUENESS TEST")
    print("=" * 78)
    print(f"G_SELF={G_SELF}, MU2={MU2}, N_ITER={N_ITER}")
    print()

    pos, col, adj = make_random_geometric(seed=42, side=8)
    n = len(pos)
    print(f"Graph: random geometric, n={n}")
    print()

    methods = ["screened_poisson", "bare_laplacian", "biharmonic", "heat_kernel"]

    print(f"{'method':<20s} {'norm_drift':>10s} {'w_ratio':>8s} {'contract':>9s} "
          f"{'TW/iter':>8s} {'phi_stab':>9s} {'F_final':>12s}")
    print("-" * 82)

    results = []
    for method in methods:
        r = run_battery(pos, col, adj, method)
        results.append(r)
        if "error" in r:
            print(f"{method:<20s} {'ERROR':>10s} — {r['error']}")
        else:
            print(f"{r['method']:<20s} {r['norm_drift']:10.2e} {r['w_ratio']:8.4f} "
                  f"{'YES' if r['contracts'] else 'NO':>9s} "
                  f"{r['tw_count']}/{r['total_iter']:>3d} "
                  f"{'OK' if r['phi_stable'] else 'UNSTAB':>9s} "
                  f"{r['F_final']:+12.4e}")

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    passing = [r for r in results if "error" not in r
               and r["norm_drift"] < 1e-3
               and r["tw_count"] == r["total_iter"]
               and r["phi_stable"]]

    if len(passing) == 1:
        print(f"UNIQUELY SELECTED: {passing[0]['method']}")
        print("Only one field equation produces stable, TOWARD, norm-conserving self-gravity.")
    elif len(passing) == 0:
        print("NO field equation passes all tests. Need parameter adjustment.")
    else:
        names = [r["method"] for r in passing]
        print(f"MULTIPLE PASS: {', '.join(names)}")
        print("The field equation is NOT uniquely selected by these consistency tests.")
        print("It remains a free parameter.")

        # But check if one is clearly better
        if any(r["contracts"] for r in passing):
            contracting = [r for r in passing if r["contracts"]]
            if len(contracting) == 1:
                print(f"However, only {contracting[0]['method']} produces contraction.")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
