#!/usr/bin/env python3
"""
Gap Asymmetry Test — Sign Selection via Transport Asymmetry
=============================================================
The parity coupling (m+Φ)·ε doesn't FLIP the dynamics when Φ → −Φ.
But it DOES create an asymmetry:

  +Φ: gap = 2(m+Φ) → wider → slower transport → MORE delay
  −Φ: gap = 2(m−Φ) → narrower → faster transport → LESS delay

The Shapiro delay already showed this: +Φ delays by 20-28 steps,
−Φ delays by only 2-5 steps. The delay RATIO is the sign-selective
observable:

  R = delay(+Φ) / delay(−Φ) >> 1  for attractive coupling
  R = delay(−Φ) / delay(+Φ) >> 1  for repulsive coupling

Additionally, the WIDTH asymmetry under self-gravity:
  w(+Φ)/w(free) vs w(−Φ)/w(free) — if these differ, the coupling is
  sign-sensitive even though both contract.

And the SPECTRAL asymmetry:
  The eigenvalue spectrum of H(+Φ) vs H(−Φ) has different gap structure.
  Measure the spectral gap and bandwidth under both signs.

These are all QUANTITATIVE asymmetries, not binary sign flips.
The claim shifts from "force is TOWARD" to "the coupling produces
measurably different dynamics under +Φ vs −Φ, consistent with
attractive gravity being the stronger coupling."
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
N_ITER = 40


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}; idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x+0.08*(rng.random()-0.5), y+0.08*(rng.random()-0.5)))
            colors.append((x+y)%2); index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj = i+di,j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a]==col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0],pos[b,1]-pos[a,1])<=1.28: _ae(adj,a,b)
    return "random_geometric", pos, col, {k:list(v) for k,v in adj.items()}


def make_growing(seed=42, n_target=64):
    rng = random.Random(seed)
    coords=[(0.,0.),(1.,0.)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur<n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur+=1
    return "growing", np.array(coords), np.array(colors,dtype=int), {k:list(v) for k,v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
    rng = random.Random(seed)
    coords,colors,layer_nodes=[],[],[]; idx=0
    for layer in range(layers):
        this_layer=[]
        for k in range(width):
            coords.append((float(layer),float(k)+0.05*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx+=1
        layer_nodes.append(this_layer)
    pos=np.array(coords); col=np.array(colors,dtype=int); n=len(pos)
    adj={i:set() for i in range(n)}
    for layer in range(layers-1):
        curr=layer_nodes[layer]; nxt=layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j1=nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2=nxt[(i_pos+1)%len(nxt)]
            if j2!=j1: adj[i].add(j2); adj[j2].add(i)
    return "layered_cycle", pos, col, {k:list(v) for k,v in adj.items()}


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col==0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); H[i,j]+=-0.5j*w; H[j,i]+=0.5j*w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n=H.shape[0]
    ap=(speye(n,format='csc')+1j*H*dt/2).tocsc()
    am=speye(n,format='csr')-1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def _width(psi, pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))


def run_asymmetry(name, pos, col, adj):
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos-center)**2, axis=1))
    L = _build_L(pos, adj, n)

    psi0 = np.exp(-0.5*dists_c**2/1.15**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    w0 = _width(psi0, pos)

    results = {}
    for label, phi_sign in [("attract", +1.0), ("repulse", -1.0), ("free", 0.0)]:
        psi = psi0.copy()
        widths = [w0]
        energies = []

        for it in range(N_ITER):
            rho = np.abs(psi)**2
            if phi_sign != 0:
                phi = phi_sign * spsolve((L+MU2*speye(n,format='csr')).tocsc(), G_SELF*rho)
            else:
                phi = np.zeros(n)
            H = _build_H(pos, col, adj, n, phi)

            # Energy
            E = float(np.real(np.conj(psi) @ H.dot(psi)))
            energies.append(E)

            psi = _cn_step(H, psi, DT)
            widths.append(_width(psi, pos))

        # Final spectral analysis
        rho_f = np.abs(psi)**2
        if phi_sign != 0:
            phi_f = phi_sign * spsolve((L+MU2*speye(n,format='csr')).tocsc(), G_SELF*rho_f)
        else:
            phi_f = np.zeros(n)
        H_f = _build_H(pos, col, adj, n, phi_f)

        try:
            evals_lo = eigsh(H_f.tocsc(), k=min(5,n-2), which='SA', return_eigenvectors=False)
            evals_hi = eigsh(H_f.tocsc(), k=min(5,n-2), which='LA', return_eigenvectors=False)
            gap = float(np.min(evals_hi[evals_hi > 0])) if any(evals_hi > 0) else float('nan')
            bandwidth = float(np.max(evals_hi) - np.min(evals_lo))
        except Exception:
            gap = float('nan'); bandwidth = float('nan')

        # Sublattice density imbalance: how much ρ sits on even vs odd sites
        rho_f_n = rho_f / np.sum(rho_f)
        even_mask = col == 0
        rho_even = np.sum(rho_f_n[even_mask])
        rho_odd = np.sum(rho_f_n[~even_mask])
        sublattice_imbalance = rho_even - rho_odd

        results[label] = {
            "w_final": widths[-1],
            "w_ratio": widths[-1]/w0,
            "E_mean": np.mean(energies),
            "E_final": energies[-1],
            "gap": gap,
            "bandwidth": bandwidth,
            "sublattice_imbalance": sublattice_imbalance,
            "norm": np.linalg.norm(psi),
        }

    # Asymmetry metrics
    w_a = results["attract"]["w_ratio"]
    w_r = results["repulse"]["w_ratio"]
    w_f = results["free"]["w_ratio"]

    # Width asymmetry: ratio of contraction factors
    contraction_a = w_a / w_f
    contraction_r = w_r / w_f
    width_asymmetry = contraction_a / contraction_r if contraction_r > 0 else float('nan')

    # Energy asymmetry
    E_a = results["attract"]["E_final"]
    E_r = results["repulse"]["E_final"]
    energy_diff = E_a - E_r

    # Spectral asymmetry
    gap_a = results["attract"]["gap"]
    gap_r = results["repulse"]["gap"]
    gap_ratio = gap_a / gap_r if gap_r > 0 and not np.isnan(gap_r) else float('nan')

    # Sublattice asymmetry
    imb_a = results["attract"]["sublattice_imbalance"]
    imb_r = results["repulse"]["sublattice_imbalance"]

    return {
        "name": name,
        "contraction_a": contraction_a,
        "contraction_r": contraction_r,
        "width_asymmetry": width_asymmetry,  # < 1 means attract contracts more
        "E_attract": E_a, "E_repulse": E_r, "E_diff": energy_diff,
        "gap_attract": gap_a, "gap_repulse": gap_r, "gap_ratio": gap_ratio,
        "imbalance_attract": imb_a, "imbalance_repulse": imb_r,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 82)
    print("GAP ASYMMETRY TEST — QUANTITATIVE SIGN SELECTION")
    print("=" * 82)
    print(f"G_SELF={G_SELF}, N_ITER={N_ITER}")
    print(f"If width_asymmetry < 1: attract contracts MORE than repulse")
    print(f"If E_diff < 0: attract has LOWER energy (bound state)")
    print(f"If gap_ratio > 1: attract has WIDER gap (slower transport)")
    print()

    all_families = [
        [make_random_geometric(seed=s, side=8) for s in [42,43,44]],
        [make_growing(seed=s, n_target=64) for s in [42,43,44]],
        [make_layered_cycle(seed=s, layers=8, width=8) for s in [42,43,44]],
    ]

    print(f"{'family':<20s} {'w_asym':>8s} {'E_diff':>10s} {'gap_ratio':>10s} "
          f"{'imb_a':>8s} {'imb_r':>8s} {'ctr_a':>8s} {'ctr_r':>8s}")
    print("-" * 88)

    all_results = []
    for fam_list in all_families:
        for fname, pos, col, adj in fam_list:
            r = run_asymmetry(fname, pos, col, adj)
            all_results.append(r)
            print(f"{fname:<20s} {r['width_asymmetry']:8.4f} {r['E_diff']:+10.4f} "
                  f"{r['gap_ratio']:10.4f} "
                  f"{r['imbalance_attract']:+8.4f} {r['imbalance_repulse']:+8.4f} "
                  f"{r['contraction_a']:8.4f} {r['contraction_r']:8.4f}")
        print()

    # ── Summary ─────────────────────────────────────────────────────
    print("=" * 82)
    print("SUMMARY")
    print("=" * 82)

    # Check if asymmetry is consistent
    w_asym_vals = [r['width_asymmetry'] for r in all_results]
    e_diff_vals = [r['E_diff'] for r in all_results]
    gap_ratio_vals = [r['gap_ratio'] for r in all_results if not np.isnan(r['gap_ratio'])]

    print(f"\nWidth asymmetry (attract/repulse contraction):")
    print(f"  Mean: {np.mean(w_asym_vals):.4f}  (< 1 = attract contracts more)")
    print(f"  Range: {np.min(w_asym_vals):.4f} to {np.max(w_asym_vals):.4f}")
    all_less = all(v < 1.0 for v in w_asym_vals)
    print(f"  All < 1: {'YES' if all_less else 'NO'}")

    print(f"\nEnergy difference (E_attract − E_repulse):")
    print(f"  Mean: {np.mean(e_diff_vals):+.4f}  (< 0 = attract lower energy)")
    print(f"  Range: {np.min(e_diff_vals):+.4f} to {np.max(e_diff_vals):+.4f}")
    all_neg = all(v < 0 for v in e_diff_vals)
    print(f"  All < 0: {'YES' if all_neg else 'NO'}")

    if gap_ratio_vals:
        print(f"\nGap ratio (gap_attract / gap_repulse):")
        print(f"  Mean: {np.mean(gap_ratio_vals):.4f}  (> 1 = attract wider gap)")
        print(f"  Range: {np.min(gap_ratio_vals):.4f} to {np.max(gap_ratio_vals):.4f}")

    print(f"\nSublatice imbalance:")
    imb_a_vals = [r['imbalance_attract'] for r in all_results]
    imb_r_vals = [r['imbalance_repulse'] for r in all_results]
    print(f"  Attract mean: {np.mean(imb_a_vals):+.4f}")
    print(f"  Repulse mean: {np.mean(imb_r_vals):+.4f}")
    imb_diff = [abs(a) - abs(b) for a, b in zip(imb_a_vals, imb_r_vals)]
    print(f"  |imb_attract| − |imb_repulse| mean: {np.mean(imb_diff):+.4f}")

    print()
    if all_less:
        print("WIDTH ASYMMETRY IS CONSISTENT: attract ALWAYS contracts more than repulse.")
        print("This is a quantitative graph-native sign-sensitive observable.")
        if all_neg:
            print("ENERGY ASYMMETRY ALSO CONSISTENT: attract ALWAYS has lower energy.")
            print("BLOCKER B1 may be CLOSABLE via quantitative asymmetry (not binary sign flip).")
    else:
        print("Width asymmetry is NOT consistent across all families/seeds.")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
