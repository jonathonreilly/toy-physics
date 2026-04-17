#!/usr/bin/env python3
"""Influence-functional decoherence: exact Level A kernel on DAG histories.

Instead of tracking env states, compute the decoherence factor directly:
  ρ(d1,d2) = Σ_{pathA→d1, pathB→d2} a*_A × a_B × K(histA, histB)

where K = ∏_k cos(α_scale × Δθ_k) is the overlap kernel from Level A.

This gives EXACT decoherence without state-space explosion. It also
lets us sweep α_scale to find whether ANY coupling strength produces
correct scaling — or whether geometric convergence makes it impossible.

Implementation: propagate per-slit amplitudes separately, extract
encounter angle histories, compute the kernel-weighted density matrix.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: influence-functional-decoherence
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup

BETA = 0.8


def propagate_with_history(positions, adj, field, src, det, k,
                           mass_set, blocked=None):
    """Propagate tracking encounter angle history per amplitude branch.

    State: (node, encounter_angles_tuple) → amplitude
    At mass nodes, record the edge angle in the history.
    No splitting — this is a single coherent propagation.
    """
    n = len(positions)
    blocked = blocked or set()

    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    state = {}
    for s in src:
        state[(s, ())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {hist: amp for (node, hist), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for hist, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx = x2-x1
                dy = y2-y1
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                theta_edge = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*theta_edge*theta_edge)
                ea = cmath.exp(1j*k*act) * w / (L**1.0)

                if j in mass_set:
                    new_hist = hist + (theta_edge,) if len(hist) < 4 else hist
                else:
                    new_hist = hist

                key = (j, new_hist)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    return {(d, hist): amp for (d, hist), amp in state.items() if d in det}


def overlap_kernel(hist_a, hist_b, alpha_scale):
    """Level A overlap: K = ∏_k cos(α_scale × (θ_Ak - θ_Bk))."""
    m = max(len(hist_a), len(hist_b))
    if m == 0:
        return 1.0
    k_val = 1.0
    for i in range(m):
        ta = hist_a[i] if i < len(hist_a) else 0.0
        tb = hist_b[i] if i < len(hist_b) else 0.0
        k_val *= math.cos(alpha_scale * (ta - tb))
    return k_val


def compute_if_purity(det_state_a, det_state_b, det_list, alpha_scale):
    """Compute purity using the influence-functional kernel.

    ρ(d1,d2) = Σ_{hA,hB} a*_A(d1,hA) × a_B(d2,hB) × K(hA,hB)
             + Σ_{hA,hB} a*_B(d1,hB) × a_A(d2,hA) × K(hB,hA)
             + pure slit-A terms + pure slit-B terms

    Simplified: compute the full density matrix including cross-slit
    terms weighted by the kernel, then compute purity.
    """
    # Group by detector node
    amps_a = defaultdict(list)  # d → [(hist, amp)]
    amps_b = defaultdict(list)
    for (d, hist), amp in det_state_a.items():
        amps_a[d].append((hist, amp))
    for (d, hist), amp in det_state_b.items():
        amps_b[d].append((hist, amp))

    # Density matrix: ρ(d1,d2) includes:
    # - slit A self-terms (no kernel needed, full coherence within slit)
    # - slit B self-terms (same)
    # - cross terms A×B weighted by kernel
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            val = 0.0+0.0j

            # A-A terms (within slit A, fully coherent)
            for hA1, aA1 in amps_a.get(d1, []):
                for hA2, aA2 in amps_a.get(d2, []):
                    val += aA1.conjugate() * aA2

            # B-B terms (within slit B, fully coherent)
            for hB1, aB1 in amps_b.get(d1, []):
                for hB2, aB2 in amps_b.get(d2, []):
                    val += aB1.conjugate() * aB2

            # A-B cross terms (weighted by kernel)
            for hA, aA in amps_a.get(d1, []):
                for hB, aB in amps_b.get(d2, []):
                    K = overlap_kernel(hA, hB, alpha_scale)
                    val += aA.conjugate() * aB * K

            # B-A cross terms
            for hB, aB in amps_b.get(d1, []):
                for hA, aA in amps_a.get(d2, []):
                    K = overlap_kernel(hB, hA, alpha_scale)
                    val += aB.conjugate() * aA * K

            rho[(d1, d2)] = val

    trace = sum(rho.get((d, d), 0.0) for d in det_list).real
    if trace <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= trace
    purity = sum(abs(v)**2 for v in rho.values()).real
    return purity


def main():
    k_band = [5.0]  # single k for speed

    print("=" * 70)
    print("INFLUENCE-FUNCTIONAL DECOHERENCE")
    print(f"  Exact Level A kernel on DAG encounter histories")
    print(f"  ρ(d1,d2) includes cross-slit terms × K(hA,hB)")
    print(f"  K = ∏ cos(α_scale × Δθ_k)")
    print("=" * 70)
    print()

    for alpha_scale in [0.5, 1.0, 2.0, 5.0]:
        print(f"  α_scale = {alpha_scale}:")
        print(f"    {'N':>4s}  {'pur_if':>8s}  {'pur_coh':>8s}  {'decoh':>8s}")
        print(f"    {'-' * 32}")

        for nl in [8, 12, 18]:
            pif_list, pcoh_list = [], []

            for seed in range(2):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
                setup = build_post_barrier_setup(positions, adj,
                    env_depth_layers=max(1, round(nl/6)))
                if setup is None:
                    continue

                mass_set = set(setup["mass_set"]) - setup["blocked"]
                blocked = setup["blocked"]

                # Identify slit groups
                bl_idx = len(setup["layers"])//3
                bi = setup["by_layer"][setup["layers"][bl_idx]]
                cy = setup["cy"]
                sa = set(i for i in bi if positions[i][1] > cy+3)
                sb = set(i for i in bi if positions[i][1] < cy-3)

                # Propagate from each slit separately
                blocked_a = blocked | sb  # block slit B
                blocked_b = blocked | sa  # block slit A

                for k in k_band:
                    ds_a = propagate_with_history(
                        positions, adj, setup["field"], setup["src"], setup["det"],
                        k, mass_set, blocked_a)
                    ds_b = propagate_with_history(
                        positions, adj, setup["field"], setup["src"], setup["det"],
                        k, mass_set, blocked_b)

                    # IF purity (with kernel)
                    pif = compute_if_purity(ds_a, ds_b, setup["det_list"], alpha_scale)
                    if not math.isnan(pif):
                        pif_list.append(pif)

                    # Coherent purity (kernel = 1, no decoherence)
                    pcoh = compute_if_purity(ds_a, ds_b, setup["det_list"], 0.0)
                    if not math.isnan(pcoh):
                        pcoh_list.append(pcoh)

            if pif_list:
                mif = sum(pif_list)/len(pif_list)
                mcoh = sum(pcoh_list)/len(pcoh_list)
                print(f"    {nl:4d}  {mif:8.4f}  {mcoh:8.4f}  {mcoh-mif:+8.4f}")

        print()

    print("pur_if = influence-functional purity (with kernel)")
    print("pur_coh = fully coherent purity (kernel=1, baseline)")
    print("decoh = pur_coh - pur_if (positive = decoherence)")
    print()
    print("PASS: pur_if decreases or decoh increases with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
