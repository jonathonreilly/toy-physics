#!/usr/bin/env python3
"""Stationary-phase propagator: weight paths by proximity to geodesic.

The CLT problem: all paths contribute equally → averaging washes out
both gravity (phase deficit saturates) and decoherence (env labels shared).

Fix: add a Gaussian weight exp(-α(S - S_min)²) to each path's amplitude.
Paths far from the stationary action (geodesic) are suppressed.

This reduces effective path count WITHOUT averaging (each path keeps
its own phase). Unlike G2, this preserves fine phase structure.

α=0: standard path-sum (CLT applies, current behavior)
α>0: stationary-phase approximation (fewer effective paths)

Properties to check:
- Does it preserve interference? (phase structure unaveraged)
- Does it fix gravity scaling? (fewer paths → less saturation)
- Does it preserve k=0→0? (weight is action-dependent, not field-dependent)

Implementation: at each edge, the amplitude gets an extra factor
exp(-α × (S_edge - S_min_edge)²) where S_min_edge is the action of
the straight-through (minimum-action) path at that edge.

Simplified: use S_min = L (zero-field action). Then the weight is
exp(-α × (S - L)²) = exp(-α × ΔS²). This penalizes edges where
the field changes the action, proportionally to ΔS².

PStack experiment: stationary-phase-propagator
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics
from scripts.two_register_decoherence import compute_field, pathsum_coherent, centroid_y, visibility


def propagate_stationary_phase(positions, adj, field, src, det, k, alpha,
                               blocked=None):
    """Corrected propagator with stationary-phase weighting.

    amplitude(edge) = exp(ikS) × exp(-α × ΔS²) / L^p
    where ΔS = S(field) - S(free) = S - L
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

    amps = [0.0+0.0j]*n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret

            # Standard 1/L^p phase
            phase = cmath.exp(1j*k*act)/(L**1.0)

            # Stationary-phase weight: suppress paths far from free-space action
            dS = act - L  # action deficit relative to free space
            weight = math.exp(-alpha * dS * dS)

            ea = phase * weight
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("STATIONARY-PHASE PROPAGATOR")
    print("  amplitude × exp(-α × ΔS²)")
    print("  ΔS = action deficit relative to free space")
    print("=" * 70)
    print()

    for alpha in [0.0, 0.5, 1.0, 2.0, 5.0]:
        print(f"  α = {alpha}:")
        print(f"    {'N':>4s}  {'R_grav':>7s}  {'V_max':>7s}  {'k0_shift':>8s}")
        print(f"    {'-' * 30}")

        for nl in [8, 12, 18, 25]:
            rs, vs, k0s = [], [], []
            for seed in range(4):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
                setup = build_post_barrier_setup(positions, adj,
                    env_depth_layers=max(1, round(nl/6)))
                if setup is None:
                    continue

                n = len(positions)
                free_f = [0.0]*n
                mid = setup["layers"][len(setup["layers"])//2]
                gm = [i for i in setup["by_layer"][mid] if positions[i][1] > setup["cy"]+2]
                if len(gm) < 2:
                    continue
                field_g = compute_field(positions, adj, gm)

                # Gravity
                shifts = []
                for k in k_band:
                    fp = propagate_stationary_phase(positions, adj, free_f, setup["src"],
                        setup["det"], k, alpha)
                    mp = propagate_stationary_phase(positions, adj, field_g, setup["src"],
                        setup["det"], k, alpha)
                    shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

                # Beam width
                fp0 = propagate_stationary_phase(positions, adj, free_f, setup["src"],
                    setup["det"], 5.0, alpha)
                total = sum(fp0.values())
                width = 1.0
                if total > 0:
                    mean = sum(positions[d][1]*p for d, p in fp0.items())/total
                    var = sum(positions[d][1]**2*p for d, p in fp0.items())/total - mean**2
                    width = max(var**0.5, 0.1)
                rs.append(sum(shifts)/len(shifts)/width)

                # Interference
                v_k = []
                for k in k_band:
                    pc = propagate_stationary_phase(positions, adj, free_f, setup["src"],
                        setup["det"], k, alpha, setup["blocked"])
                    v_k.append(visibility(pc, positions, setup["det_list"]))
                vs.append(max(v_k))

                # k=0
                fp0 = propagate_stationary_phase(positions, adj, free_f, setup["src"],
                    setup["det"], 0.0, alpha)
                mp0 = propagate_stationary_phase(positions, adj, field_g, setup["src"],
                    setup["det"], 0.0, alpha)
                k0s.append(centroid_y(mp0, positions) - centroid_y(fp0, positions))

            if rs:
                k0 = sum(abs(s) for s in k0s)/len(k0s)
                print(f"    {nl:4d}  {sum(rs)/len(rs):+7.3f}  "
                      f"{sum(vs)/len(vs):7.3f}  {k0:8.5f}")
        print()

    print("PASS criteria:")
    print("  R_grav stable at large N (not collapsing)")
    print("  V_max > 0.5 (interference preserved)")
    print("  k0_shift ≈ 0 (gravity = pure phase)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
