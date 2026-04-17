#!/usr/bin/env python3
"""Caldeira-Leggett bath decoherence on DAGs.

MOTIVATION
----------
AFC showed that |K| drops to ~0.91 (env_mass) or ~0.91 (full_mid) at N=18,
meaning the complex wavefields ψ_A and ψ_B at the mass region ARE different.
But the single-K model only achieves ~0.006 purity drop, not useful decoherence.

The Caldeira-Leggett (CL) insight: when the environment is a BATH OF HARMONIC
OSCILLATORS coupled independently to different spatial bins, the decoherence
factor is EXPONENTIAL in the coupling strength AND in the bin-resolved
field contrast:

    D = exp(-λ² × S)
    S = Σ_bins |ψ_A(y_b) - ψ_B(y_b)|²   (bin-resolved contrast)

For large λ, D → 0 even if S is small, giving near-complete decoherence.

KEY QUESTION: Does S stay bounded below zero as N grows?
  - If S ~ 1/N → 0 (CLT decay): D → 1 for fixed λ, fails at scale
  - If S → const or grows: D → 0 for large λ, succeeds at scale

WHAT IS DIFFERENT FROM PREVIOUS APPROACHES:
  - Previous: kernel at INDIVIDUAL encounters (angle, sector, node-label)
  - CL bath: kernel over SPATIAL Y-BINS, using COMPLEX amplitude differences
  - The bath decoherence is exponential in λ, not linear
  - The bath is a SEPARATE subsystem (harmonic oscillators at each y-bin)
    whose state is the coherent displacement by path amplitude
  - Information is CUMULATIVE: all layers contribute to S

This corresponds to the "separate local dynamical subsystem" option —
the bath oscillators are not read off from graph-local observables.

PStack experiment: caldeira-leggett-bath
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
N_YBINS = 8  # number of spatial y-bins for the bath


def _topo_order(adj, n):
    in_deg = [0] * n
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
    return order


def propagate_amplitudes(positions, adj, field, src, k, blocked=None):
    """Propagate from src, return [amplitude] for all nodes."""
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)

    amps = [0.0 + 0.0j] * n
    for s in src:
        amps[s] = 1.0 / len(src) + 0.0j

    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea

    return amps


def bin_amplitudes(amps, nodes, y_min, y_max, n_bins):
    """Sum amplitudes into spatial y-bins over specified nodes.

    Returns list of n_bins complex values.
    """
    bin_width = (y_max - y_min) / n_bins
    bins = [0.0 + 0.0j] * n_bins
    for m in nodes:
        y = positions_global[m][1]
        b = int((y - y_min) / bin_width)
        b = max(0, min(n_bins - 1, b))
        bins[b] += amps[m]
    return bins


# Module-level reference for bin_amplitudes (set in main)
positions_global = None


def cl_bath_contrast(amps_a, amps_b, mid_nodes, y_min, y_max, n_bins=N_YBINS):
    """Compute bin-resolved Caldeira-Leggett contrast S.

    S = Σ_bins |ψ_A(y_b) - ψ_B(y_b)|²

    where ψ_A(y_b) = Σ_{m in bin b} ψ_A(m)  (coherent sum in bin).

    Also returns the normalized version S_norm = S / (N_A_total + N_B_total).
    """
    bins_a = bin_amplitudes(amps_a, mid_nodes, y_min, y_max, n_bins)
    bins_b = bin_amplitudes(amps_b, mid_nodes, y_min, y_max, n_bins)

    S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    N_A = sum(abs(a) ** 2 for a in bins_a)
    N_B = sum(abs(b) ** 2 for b in bins_b)
    denom = N_A + N_B

    # Also compute single-K AFC for comparison
    num_afc = sum(a.conjugate() * b for a, b in zip(bins_a, bins_b))
    afc_denom = math.sqrt(N_A * N_B) if N_A > 0 and N_B > 0 else 0.0
    K_afc = abs(num_afc) / afc_denom if afc_denom > 0 else 1.0

    return S, (S / denom if denom > 0 else 0.0), K_afc, N_A, N_B


def cl_purity(amps_a, amps_b, D, det_list):
    """Detector purity under CL bath decoherence factor D.

    ρ(d1,d2) = ψ_A(d1)ψ_A*(d2) + ψ_B(d1)ψ_B*(d2)
             + D × ψ_A(d1)ψ_B*(d2) + D × ψ_B(d1)ψ_A*(d2)

    D is a real positive scalar in [0, 1].
    Also returns coherent purity (D=1) and maximally-decohered (D=0).
    """
    if not det_list:
        return math.nan, math.nan, math.nan

    rho = {}
    rho_coh = {}
    rho_decoh = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab = amps_a[d1] * amps_b[d2].conjugate()
            ba = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + D * ab + D * ba
            rho_coh[(d1, d2)] = aa + bb + ab + ba
            rho_decoh[(d1, d2)] = aa + bb

    def _purity(r):
        tr = sum(r[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in r:
            r[key] /= tr
        return sum(abs(v) ** 2 for v in r.values()).real

    return _purity(rho), _purity(rho_coh), _purity(rho_decoh)


def main():
    global positions_global

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 4
    lam_sweep = [1.0, 3.0, 5.0, 10.0]

    print("=" * 70)
    print("CALDEIRA-LEGGETT BATH DECOHERENCE")
    print(f"  D = exp(-λ² × S),  S = Σ_bins |ψ_A(y_b) - ψ_B(y_b)|²")
    print(f"  Bath: {N_YBINS} spatial y-bins spanning full y-range")
    print(f"  Bins: CUMULATIVE over all mid-layer nodes")
    print("=" * 70)
    print()

    # First: scaling of S with N (most important test)
    print("  SCALING OF S WITH N (λ-independent test)")
    print(f"  {'N':>4s}  {'S_raw':>8s}  {'S_norm':>8s}  {'K_afc':>7s}  "
          f"{'D(λ=3)':>8s}  {'D(λ=10)':>8s}")
    print(f"  {'-' * 55}")

    s_by_n = {}
    for nl in [8, 12, 18, 25]:
        S_list, Sn_list, K_list = [], [], []

        for seed in range(n_seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 11 + 7)
            positions_global = positions
            setup = build_post_barrier_setup(
                positions, adj, env_depth_layers=max(1, round(nl / 6)))
            if setup is None:
                continue

            blocked = setup["blocked"]
            layers = setup["layers"]
            by_layer = setup["by_layer"]
            det_set = setup["det"]
            bl_idx = len(layers) // 3
            cy = setup["cy"]

            # Full mid region (all nodes from barrier+1 to detector-1)
            mid_nodes = [
                i for lay in layers[bl_idx + 1: -1]
                for i in by_layer[lay]
                if i not in blocked and i not in det_set
            ]
            if len(mid_nodes) < 4:
                continue

            all_ys = [positions[m][1] for m in mid_nodes]
            y_min = min(all_ys)
            y_max = max(all_ys)

            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 3]
            sb = [i for i in bi if positions[i][1] < cy - 3]
            if not sa or not sb:
                continue

            blocked_a = blocked | set(sb)
            blocked_b = blocked | set(sa)

            for k in k_band:
                aa = propagate_amplitudes(positions, adj, setup["field"],
                                          setup["src"], k, blocked_a)
                ab = propagate_amplitudes(positions, adj, setup["field"],
                                          setup["src"], k, blocked_b)

                S, Sn, K_afc, _, _ = cl_bath_contrast(
                    aa, ab, mid_nodes, y_min, y_max)
                S_list.append(S)
                Sn_list.append(Sn)
                K_list.append(K_afc)

        if S_list:
            ms = sum(S_list) / len(S_list)
            msn = sum(Sn_list) / len(Sn_list)
            mK = sum(K_list) / len(K_list)
            s_by_n[nl] = msn
            print(f"  {nl:4d}  {ms:8.5f}  {msn:8.5f}  {mK:7.4f}  "
                  f"{math.exp(-9*msn):8.5f}  {math.exp(-100*msn):8.5f}")

    print()
    if s_by_n:
        ns = sorted(s_by_n.keys())
        trend = "DECREASING" if s_by_n[ns[-1]] < s_by_n[ns[0]] * 0.5 else \
                "ROUGHLY STABLE" if s_by_n[ns[-1]] > s_by_n[ns[0]] * 0.3 else \
                "DECREASING SLOWLY"
        print(f"  S_norm trend: {trend}")
        print(f"  (Want: STABLE or INCREASING — means CL bath stays effective at scale)")
    print()

    # Then: purity sweep over λ at N=12, N=18, and N=25
    print("  PURITY VS λ AT N=12, N=18, AND N=25")
    print(f"  {'λ':>5s}  {'N':>4s}  {'pur_cl':>8s}  {'pur_coh':>8s}  "
          f"{'pur_min':>8s}  {'decoh':>8s}")
    print(f"  {'-' * 48}")

    for nl in [12, 18, 25]:
        for lam in lam_sweep:
            pur_list, coh_list, min_list = [], [], []

            for seed in range(n_seeds):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 11 + 7)
                positions_global = positions
                setup = build_post_barrier_setup(
                    positions, adj, env_depth_layers=max(1, round(nl / 6)))
                if setup is None:
                    continue

                blocked = setup["blocked"]
                layers = setup["layers"]
                by_layer = setup["by_layer"]
                det_list = setup["det_list"]
                det_set = setup["det"]
                bl_idx = len(layers) // 3
                cy = setup["cy"]

                mid_nodes = [
                    i for lay in layers[bl_idx + 1: -1]
                    for i in by_layer[lay]
                    if i not in blocked and i not in det_set
                ]
                if len(mid_nodes) < 4:
                    continue

                all_ys = [positions[m][1] for m in mid_nodes]
                y_min = min(all_ys)
                y_max = max(all_ys)

                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if positions[i][1] > cy + 3]
                sb = [i for i in bi if positions[i][1] < cy - 3]
                if not sa or not sb:
                    continue

                blocked_a = blocked | set(sb)
                blocked_b = blocked | set(sa)

                for k in k_band:
                    aa = propagate_amplitudes(positions, adj, setup["field"],
                                              setup["src"], k, blocked_a)
                    ab = propagate_amplitudes(positions, adj, setup["field"],
                                              setup["src"], k, blocked_b)

                    _, Sn, _, _, _ = cl_bath_contrast(
                        aa, ab, mid_nodes, y_min, y_max)
                    D = math.exp(-lam ** 2 * Sn)

                    pur, pur_coh, pur_min = cl_purity(aa, ab, D, det_list)
                    if not math.isnan(pur):
                        pur_list.append(pur)
                        coh_list.append(pur_coh)
                        min_list.append(pur_min)

            if pur_list:
                mp = sum(pur_list) / len(pur_list)
                mc = sum(coh_list) / len(coh_list)
                mm = sum(min_list) / len(min_list)
                print(f"  {lam:5.1f}  {nl:4d}  {mp:8.4f}  {mc:8.4f}  "
                      f"{mm:8.4f}  {mc-mp:+8.4f}")
        print()

    print("pur_cl  = purity under CL bath (D = exp(-λ² S))")
    print("pur_coh = fully coherent purity (D=1, upper bound)")
    print("pur_min = maximally decohered purity (D=0, lower bound)")
    print("decoh   = pur_coh - pur_cl (positive = bath-induced decoherence)")
    print()
    print("KEY: is pur_cl at large λ close to pur_min?")
    print("      YES → CL bath achieves near-maximal decoherence")
    print("      NO  → S_norm too small for bath to work")
    print()
    print("SCALING TEST: does decoh INCREASE from N=12 to N=18 for large λ?")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
