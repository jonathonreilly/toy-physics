#!/usr/bin/env python3
"""Amplitude Field Coherence (AFC) decoherence kernel — region comparison.

MOTIVATION
----------
All tested IF kernels fail at N=18 because the amplitude-MAGNITUDE
distribution over the mass region converges between slits (CLT). But
magnitudes are only half the story.

The AFC kernel uses the COMPLEX wavefield overlap:

    K = Σ_{m ∈ region} ψ_A*(m) ψ_B(m) / sqrt(N_A × N_B)

This is the inner product of the two slit wavefields in the environment
region. |K| < 1 when the wavefields are not parallel — i.e., when the
phase PATTERN differs between slits.

Phase differences arise from path length differences:
    Δφ(m) ≈ k × (L_B(m) - L_A(m))

For the SYMMETRIC env_mass region (near y=0): L_A(m) ≈ L_B(m) by
symmetry → small Δφ → |K| ≈ 1 (poor decoherence).

For the ASYMMETRIC grav_mass region (above center, y > cy+1):
L_B(m) >> L_A(m) for mass nodes m with y > 0 (slit B is far away,
slit A is close) → large Δφ → potential |K| << 1.

The "worldtube" kernel uses ALL intermediate nodes (not just mass),
giving the richest phase structure.

Three variants tested:
  env_mass   — symmetric cluster near center (baseline, small Δφ)
  grav_mass  — asymmetric upper nodes (large Δφ, should be best)
  full_mid   — all nodes between barrier and detector (richest)

PStack experiment: amplitude-field-coherence
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
    """Propagate from src, return [amplitude] for all nodes.

    Uses directional measure: exp(-0.8 θ²) / L per edge.
    """
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


def afc_kernel(amps_a, amps_b, region):
    """Normalized complex field overlap over region nodes.

    K = Σ_{m ∈ region} ψ_A*(m) ψ_B(m) / sqrt(N_A × N_B)

    Returns (K_complex, |K|).
    """
    num = 0.0 + 0.0j
    na = 0.0
    nb = 0.0
    for m in region:
        a = amps_a[m]
        b = amps_b[m]
        num += a.conjugate() * b
        na += abs(a) ** 2
        nb += abs(b) ** 2
    denom = math.sqrt(na * nb) if na > 0 and nb > 0 else 0.0
    K = (num / denom) if denom > 0 else 0.0 + 0.0j
    return K, abs(K)


def afc_purity(amps_a, amps_b, K, det_list):
    """Detector purity under AFC decoherence kernel.

    ρ(d1,d2) = ψ_A(d1)ψ_A*(d2) + ψ_B(d1)ψ_B*(d2)
             + K × ψ_A(d1)ψ_B*(d2) + K* × ψ_B(d1)ψ_A*(d2)

    Also returns coherent purity (K=1) as baseline.
    """
    if not det_list:
        return math.nan, math.nan

    rho = {}
    rho_coh = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab_cross = amps_a[d1] * amps_b[d2].conjugate()
            ba_cross = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + K * ab_cross + K.conjugate() * ba_cross
            rho_coh[(d1, d2)] = aa + bb + ab_cross + ba_cross

    trace = sum(rho[(d, d)] for d in det_list).real
    tr_coh = sum(rho_coh[(d, d)] for d in det_list).real
    if trace <= 1e-30 or tr_coh <= 1e-30:
        return math.nan, math.nan

    for key in rho:
        rho[key] /= trace
    for key in rho_coh:
        rho_coh[key] /= tr_coh

    purity = sum(abs(v) ** 2 for v in rho.values()).real
    purity_coh = sum(abs(v) ** 2 for v in rho_coh.values()).real
    return purity, purity_coh


def phase_stats(amps_a, amps_b, region):
    """Mean absolute phase difference and spread over region nodes."""
    dphis = []
    for m in region:
        if abs(amps_a[m]) > 1e-15 and abs(amps_b[m]) > 1e-15:
            dp = cmath.phase(amps_a[m]) - cmath.phase(amps_b[m])
            dp = (dp + math.pi) % (2 * math.pi) - math.pi
            dphis.append(dp)
    if not dphis:
        return 0.0, 0.0, 0
    spread = max(dphis) - min(dphis)
    mean_abs = sum(abs(d) for d in dphis) / len(dphis)
    return spread, mean_abs, len(dphis)


def main():
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 4

    print("=" * 70)
    print("AFC DECOHERENCE KERNEL — THREE REGION VARIANTS")
    print("  K = Σ_m ψ_A*(m)ψ_B(m) / sqrt(N_A N_B)")
    print("  env_mass  = symmetric cluster near center (baseline)")
    print("  grav_mass = asymmetric upper region (large Δpath_length)")
    print("  full_mid  = all nodes barrier→detector (worldtube)")
    print("=" * 70)
    print()
    print("  KEY PREDICTION: grav_mass and full_mid should have |K| << 1")
    print("  and |K| should DECREASE with N (unlike CLT failure of local kernels)")
    print()

    for region_label in ["env_mass", "grav_mass", "full_mid"]:
        print(f"  REGION: {region_label}")
        print(f"  {'N':>4s}  {'|K|':>7s}  {'Δφ_sprd':>8s}  "
              f"{'n_rgn':>6s}  {'decoh':>8s}  {'k0_K':>7s}")
        print(f"  {'-' * 52}")

        for nl in [8, 12, 18, 25]:
            k_list, decoh_list, k0_list = [], [], []
            n_region_list, dphi_list = [], []

            for seed in range(n_seeds):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 11 + 7)
                setup = build_post_barrier_setup(
                    positions, adj,
                    env_depth_layers=max(1, round(nl / 6)))
                if setup is None:
                    continue

                blocked = setup["blocked"]
                det_list = setup["det_list"]
                det_set = setup["det"]
                field = setup["field"]
                layers = setup["layers"]
                by_layer = setup["by_layer"]

                # Build the region for this variant
                bl_idx = len(layers) // 3
                cy = setup["cy"]

                if region_label == "env_mass":
                    region = set(setup["mass_set"]) - blocked

                elif region_label == "grav_mass":
                    grav_layer = layers[2 * len(layers) // 3]
                    region = set(
                        i for i in by_layer[grav_layer]
                        if positions[i][1] > cy + 1
                    ) - blocked

                else:  # full_mid: all nodes from barrier+1 to detector-1
                    mid_layers = layers[bl_idx + 1: -1]
                    region = set(
                        i for lay in mid_layers for i in by_layer[lay]
                    ) - blocked - det_set

                if len(region) < 2:
                    continue

                # Identify slits
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if positions[i][1] > cy + 3]
                sb = [i for i in bi if positions[i][1] < cy - 3]
                if not sa or not sb:
                    continue

                blocked_a = blocked | set(sb)
                blocked_b = blocked | set(sa)

                # k=0 check
                aa0 = propagate_amplitudes(positions, adj, field,
                                           setup["src"], 0.0, blocked_a)
                ab0 = propagate_amplitudes(positions, adj, field,
                                           setup["src"], 0.0, blocked_b)
                _, modK0 = afc_kernel(aa0, ab0, region)
                k0_list.append(modK0)

                for k in k_band:
                    aa = propagate_amplitudes(positions, adj, field,
                                              setup["src"], k, blocked_a)
                    ab = propagate_amplitudes(positions, adj, field,
                                              setup["src"], k, blocked_b)

                    K, modK = afc_kernel(aa, ab, region)
                    pur, pur_coh = afc_purity(aa, ab, K, det_list)

                    if not math.isnan(pur):
                        k_list.append(modK)
                        decoh_list.append(pur_coh - pur)

                # Phase stats at k=5
                aa5 = propagate_amplitudes(positions, adj, field,
                                           setup["src"], 5.0, blocked_a)
                ab5 = propagate_amplitudes(positions, adj, field,
                                           setup["src"], 5.0, blocked_b)
                spread, _, n_r = phase_stats(aa5, ab5, region)
                n_region_list.append(n_r)
                dphi_list.append(spread)

            if k_list:
                mk0 = sum(k0_list) / len(k0_list) if k0_list else math.nan
                print(f"  {nl:4d}  {sum(k_list)/len(k_list):7.4f}  "
                      f"{sum(dphi_list)/len(dphi_list):8.3f}  "
                      f"{int(sum(n_region_list)/len(n_region_list)):6d}  "
                      f"{sum(decoh_list)/len(decoh_list):+8.4f}  "
                      f"{mk0:7.4f}")
        print()

    print("|K|     = wavefield overlap (1=coherent, 0=decohered)")
    print("Δφ_sprd = phase difference spread across region (radians, k=5)")
    print("n_rgn   = number of region nodes")
    print("decoh   = pur_coh - pur_afc (positive = decoherence, want increasing with N)")
    print("k0_K    = |K| at k=0 (baseline check, should be ~1 for symmetric regions)")
    print()
    print("SCALING TEST: does |K| DECREASE with N for grav_mass and full_mid?")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
