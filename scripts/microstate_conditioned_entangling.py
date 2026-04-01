#!/usr/bin/env python3
"""Microstate-conditioned entangling coupling.

The splitting angle and phase kick depend on local CA microstate at
each mass node. Different oscillation phases give different α at
different nodes → non-uniform splitting → potentially better env
balance than fixed cos/sin.

Architecture:
- Each mass node m has a local microstate s_m ∈ {0, 1, 2} (period-3 CA)
- The splitting angle at m depends on s_m:
    s=0: α = π/6 (weak split)
    s=1: α = π/3 (strong split)
    s=2: α = π/4 (medium split)
- The kick phase for recorded nodes also depends on s_m:
    φ = 2π × s_m / 3
- The detector probability averages incoherently over the 3 CA phases

This combines:
- Entangling split (creates superposition in env)
- CA microstate conditioning (non-uniform split across nodes)
- History-dependent kick (recorded nodes modify later propagation)
- Incoherent averaging over CA phases (genuine oscillation decoherence)

Uses the promoted angle² β=0.8 propagator.

PStack experiment: microstate-conditioned-entangling
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

BETA = 0.8
N_CA_PHASES = 3

# Microstate-dependent splitting angles
ALPHAS = [math.pi/6, math.pi/3, math.pi/4]
# Microstate-dependent kick phases
PHIS = [0.0, 2*math.pi/3, 4*math.pi/3]


def build_microstate_map(mass_nodes, phase):
    """Assign each mass node a microstate based on CA oscillation phase."""
    mass_list = sorted(mass_nodes)
    return {m: (i + phase) % N_CA_PHASES for i, m in enumerate(mass_list)}


def propagate_microstate_entangling(positions, adj, field, src, det, k,
                                     mass_set, microstate_map, blocked=None):
    """Propagator with microstate-conditioned entangling at mass nodes.

    At mass node m with microstate s:
      If m not recorded: split with angle α_s, creating env branch
      If source i is recorded: apply kick with phase φ_{s_i}
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

    kick_count = [0]

    state = {}
    for s in src:
        state[(s, frozenset())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {rec: amp for (node, rec), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for recorded, amp in entries.items():
            # History-dependent kick from recorded source
            source_kick = 1.0
            if i in recorded and i in microstate_map:
                s_i = microstate_map[i]
                source_kick = cmath.exp(1j * PHIS[s_i])
                kick_count[0] += 1

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
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*theta*theta)
                ea = cmath.exp(1j*k*act) * w / (L**1.0) * source_kick

                if j in mass_set and j not in recorded:
                    s_j = microstate_map.get(j, 0)
                    alpha_j = ALPHAS[s_j]
                    cos_a = math.cos(alpha_j)
                    sin_a = math.sin(alpha_j)

                    # Branch 0: env unchanged
                    key_0 = (j, recorded)
                    if key_0 not in state:
                        state[key_0] = 0.0+0.0j
                    state[key_0] += amp * ea * cos_a

                    # Branch 1: record created at j
                    rec_1 = recorded | frozenset([j])
                    key_1 = (j, rec_1)
                    if key_1 not in state:
                        state[key_1] = 0.0+0.0j
                    state[key_1] += amp * ea * sin_a
                else:
                    key = (j, recorded)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp * ea

    det_state = {(d, rec): amp for (d, rec), amp in state.items() if d in det}
    return det_state, kick_count[0]


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("MICROSTATE-CONDITIONED ENTANGLING COUPLING")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Split angles: {[f'{a:.2f}' for a in ALPHAS]} (by microstate)")
    print(f"  Kick phases: {[f'{p:.2f}' for p in PHIS]} (by microstate)")
    print(f"  Incoherent average over {N_CA_PHASES} CA phases")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_env':>6s}  {'kicks':>6s}  "
          f"{'pur_mc':>8s}  {'pur_node':>8s}  {'mc_off':>8s}")
    print(f"  {'-' * 56}")

    for nl in [8, 12, 18]:
        pmc_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_envs = 0
        total_kicks = 0

        for seed in range(3):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            n_mass_count = len(mass_set)
            if n_mass_count > 12:
                mass_set = set(sorted(mass_set)[:12])

            for k in k_band:
                # Microstate-conditioned: average over CA phases
                combined = {}
                phase_kicks = 0
                for ca_phase in range(N_CA_PHASES):
                    ms_map = build_microstate_map(mass_set, ca_phase)
                    ds, nk = propagate_microstate_entangling(
                        positions, adj, setup["field"], setup["src"], setup["det"],
                        k, mass_set, ms_map, setup["blocked"])
                    phase_kicks += nk
                    for (d, rec), amp in ds.items():
                        key = (d, (ca_phase, rec))
                        combined[key] = amp

                total_kicks += phase_kicks
                pmc, _, _, _ = compute_detector_metrics(combined, setup["det_list"])
                if not math.isnan(pmc):
                    pmc_list.append(pmc)
                envs = set(env for (d, env) in combined.keys())
                max_envs = max(max_envs, len(envs))

                # Node-label (matched capped mass set)
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # Off baseline (no mass coupling)
                ds_0, _ = propagate_microstate_entangling(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, set(), {}, setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pmc_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_envs:6d}  {total_kicks:6d}  "
                  f"{sum(pmc_list)/len(pmc_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_mc = microstate-conditioned entangling (this test)")
    print("pur_node = node-label env (matched mass set)")
    print("mc_off = no coupling (should be ~1.0)")
    print()
    print("PASS: pur_mc does not rise with N")
    print("FAIL: pur_mc rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
