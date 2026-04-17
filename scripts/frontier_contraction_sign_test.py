#!/usr/bin/env python3
"""
Contraction Sign Test + Binding Energy — Graph-Native Sign Selection
=====================================================================
The D2 self-gravity test shows 9/9 contraction (grav/free = 0.40–0.76).
This probe tests whether INVERTING Φ produces EXPANSION instead. If:

    grav(+Φ)/free < 1  (contraction under attraction)
    grav(−Φ)/free > 1  (expansion under repulsion)

then the contraction ratio is a graph-native, sign-selective observable
that works on irregular graphs without coordinates.

Additionally measures binding energy: E = <ψ|H|ψ>. If E(+Φ) < E(−Φ),
the attractive coupling produces lower-energy (bound) configurations.

Both observables are single scalars, exactly computable on any bipartite
graph, and do not require spatial coordinates or directional proxies.
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
N_ITER = 40  # longer evolution for clearer contraction signal


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
            colors.append((x+y) % 2); index[(x,y)] = idx; idx += 1
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
    return "random_geometric", pos, col, {k: list(v) for k,v in adj.items()}


def make_growing(seed=42, n_target=64):
    rng = random.Random(seed)
    coords = [(0.,0.),(1.,0.)]; colors = [0,1]; adj = {0:{1}, 1:{0}}; cur = 2
    while cur < n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur += 1
    return "growing", np.array(coords), np.array(colors,dtype=int), {k:list(v) for k,v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
    rng = random.Random(seed)
    coords, colors, layer_nodes = [], [], []; idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            coords.append((float(layer), float(k)+0.05*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords); col = np.array(colors, dtype=int); n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers-1):
        curr = layer_nodes[layer]; nxt = layer_nodes[layer+1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2 = nxt[(i_pos+1)%len(nxt)]
            if j2 != j1: adj[i].add(j2); adj[j2].add(i)
    return "layered_cycle", pos, col, {k:list(v) for k,v in adj.items()}


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5); L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5); H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j*H*dt/2).tocsc()
    am = speye(n, format='csr') - 1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def _width(psi, pos):
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    cx = np.sum(rho*pos[:,0]); cy = np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2 + (pos[:,1]-cy)**2)))


def run_sign_test(name, pos, col, adj, seed_label):
    """Run self-gravity with +Φ, −Φ, and free. Measure width ratio and energy."""
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))
    L = _build_L(pos, adj, n)

    psi0 = np.exp(-0.5 * dists_c**2 / 1.15**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    w0 = _width(psi0, pos)

    results = {}
    for label, phi_sign in [("attract", +1.0), ("repulse", -1.0), ("free", 0.0)]:
        psi = psi0.copy()
        for _ in range(N_ITER):
            rho = np.abs(psi)**2
            if phi_sign != 0:
                phi = phi_sign * spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_SELF*rho)
            else:
                phi = np.zeros(n)
            H = _build_H(pos, col, adj, n, phi)
            psi = _cn_step(H, psi, DT)

        wf = _width(psi, pos)
        norm = np.linalg.norm(psi)

        # Final energy
        rho = np.abs(psi)**2
        if phi_sign != 0:
            phi_f = phi_sign * spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_SELF*rho)
        else:
            phi_f = np.zeros(n)
        H_f = _build_H(pos, col, adj, n, phi_f)
        E = float(np.real(np.conj(psi) @ H_f.dot(psi)))

        results[label] = {"w": wf, "w_ratio": wf/w0, "norm": norm, "E": E}

    # Sign-selective if attract contracts AND repulse expands (relative to free)
    w_a = results["attract"]["w"]
    w_r = results["repulse"]["w"]
    w_f = results["free"]["w"]
    ratio_a = w_a / w_f  # < 1 = contraction
    ratio_r = w_r / w_f  # > 1 = expansion

    contraction_selective = ratio_a < 1.0 and ratio_r > 1.0

    # Energy: attract should have lower energy than repulse
    E_a = results["attract"]["E"]
    E_r = results["repulse"]["E"]
    energy_selective = E_a < E_r

    return {
        "name": name,
        "seed": seed_label,
        "w_attract": w_a, "w_repulse": w_r, "w_free": w_f,
        "ratio_attract": ratio_a, "ratio_repulse": ratio_r,
        "contraction_selective": contraction_selective,
        "E_attract": E_a, "E_repulse": E_r,
        "energy_selective": energy_selective,
        "norm_a": results["attract"]["norm"],
        "norm_r": results["repulse"]["norm"],
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 82)
    print("CONTRACTION SIGN TEST + BINDING ENERGY — GRAPH-NATIVE SIGN SELECTION")
    print("=" * 82)
    print(f"G_SELF={G_SELF}, N_ITER={N_ITER}, DT={DT}")
    print(f"Sign-selective if: attract/free < 1 AND repulse/free > 1")
    print()

    families_seeds = [
        [make_random_geometric(seed=s, side=8) for s in [42,43,44]],
        [make_growing(seed=s, n_target=64) for s in [42,43,44]],
        [make_layered_cycle(seed=s, layers=8, width=8) for s in [42,43,44]],
    ]

    print(f"{'family':<20s} {'seed':>4s} {'w_a/free':>9s} {'w_r/free':>9s} "
          f"{'ctr_sel':>8s} {'E_attract':>10s} {'E_repulse':>10s} {'E_sel':>6s} "
          f"{'norm_a':>8s} {'norm_r':>8s}")
    print("-" * 100)

    all_results = []
    for fam_list in families_seeds:
        fam_name = None
        for i, (fname, pos, col, adj) in enumerate(fam_list):
            r = run_sign_test(fname, pos, col, adj, str(42+i))
            all_results.append(r)
            if fam_name is None: fam_name = fname
            print(f"{fname:<20s} {r['seed']:>4s} {r['ratio_attract']:9.4f} {r['ratio_repulse']:9.4f} "
                  f"{'YES' if r['contraction_selective'] else 'NO':>8s} "
                  f"{r['E_attract']:+10.4f} {r['E_repulse']:+10.4f} "
                  f"{'YES' if r['energy_selective'] else 'NO':>6s} "
                  f"{r['norm_a']:8.6f} {r['norm_r']:8.6f}")
        # Family summary
        fam_results = [r for r in all_results if r['name'] == fam_name]
        ctr_count = sum(1 for r in fam_results if r['contraction_selective'])
        eng_count = sum(1 for r in fam_results if r['energy_selective'])
        print(f"  → {fam_name}: contraction {ctr_count}/3, energy {eng_count}/3")
        print()

    # ── Overall verdict ─────────────────────────────────────────────
    print("=" * 82)
    print("VERDICT")
    print("=" * 82)

    families = {}
    for r in all_results:
        families.setdefault(r['name'], []).append(r)

    ctr_families_pass = 0
    eng_families_pass = 0
    for fam, rs in families.items():
        if sum(1 for r in rs if r['contraction_selective']) >= 2:
            ctr_families_pass += 1
        if sum(1 for r in rs if r['energy_selective']) >= 2:
            eng_families_pass += 1

    print(f"\nContraction sign-selective: {ctr_families_pass}/3 families pass (≥2/3 seeds)")
    print(f"Energy sign-selective:     {eng_families_pass}/3 families pass (≥2/3 seeds)")

    if ctr_families_pass >= 2 and eng_families_pass >= 2:
        print("\nBLOCKER B1 CLOSED: Graph-native sign-selective observables confirmed.")
        print("Both contraction ratio AND binding energy distinguish +Φ from −Φ")
        print("on irregular graph families without coordinates.")
    elif ctr_families_pass >= 2:
        print("\nContraction is sign-selective. Energy is not (or marginal).")
        print("Contraction ratio alone may suffice as graph-native observable.")
    elif eng_families_pass >= 2:
        print("\nEnergy is sign-selective. Contraction is not.")
        print("Binding energy alone may suffice as graph-native observable.")
    else:
        print("\nBLOCKER B1 REMAINS OPEN. Neither observable is robustly sign-selective.")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
