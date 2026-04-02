#!/usr/bin/env python3
"""Level B (slot-resolved): True fresh-ancilla decoherence on real DAGs.

This is the SLOT-RESOLVED implementation, distinct from the encounter-
count proxy in fresh_ancilla_on_dag.py.

Key properties:
  - Env state is a BITSTRING (b_1, b_2, ..., b_m) where b_k ∈ {0,1}
    is the state of the k-th fresh ancilla.
  - α_k is BRANCH-DEPENDENT: α_k = ALPHA_SCALE × |edge_angle| at the
    k-th mass encounter. Different paths through different edges get
    different coupling strengths.
  - Baseline α=0 (or empty mass_set) gives purity ~1.0.

The Level A decay law predicts:
  overlap = ∏_k cos(α_Ak - α_Bk)
  coherence = |overlap|² = ∏_k cos²(Δα_k)

Uses the promoted angle² beta=0.8 propagator.

PStack experiment: fresh-ancilla-slot-resolved
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
ALPHA_SCALE = 0.5  # scales the edge angle into coupling strength
K_BAND = [3.0, 5.0, 7.0]
N_LIST = [8, 12, 18, 25, 40, 60, 80]
N_SEEDS = 8


def propagate_fresh_ancilla(positions, adj, field, src, det, k,
                            mass_set, blocked=None):
    """Propagator with slot-resolved fresh ancillas at mass encounters.

    State: (node, ancilla_bitstring_tuple) → amplitude

    At each mass encounter (edge touching mass node j):
      α_k = ALPHA_SCALE × |edge_angle|  (branch-dependent coupling)
      Split: cos(α_k) keeps ancilla |0⟩, sin(α_k) excites to |1⟩
      Bitstring grows by one bit.

    The bitstring length = number of encounters. Different bit patterns
    at the same length are orthogonal env states.
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
        entries = {bits: amp for (node, bits), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for bits, amp in entries.items():
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
                    # Branch-dependent coupling from edge angle
                    alpha_k = ALPHA_SCALE * theta_edge
                    if alpha_k < 0.01:
                        key = (j, bits)
                        if key not in state:
                            state[key] = 0.0+0.0j
                        state[key] += amp * ea
                    else:
                        cos_a = math.cos(alpha_k)
                        sin_a = math.sin(alpha_k)

                        # Append 0 bit (ancilla unchanged)
                        bits_0 = bits + (0,)
                        key_0 = (j, bits_0)
                        if key_0 not in state:
                            state[key_0] = 0.0+0.0j
                        state[key_0] += amp * ea * cos_a

                        # Append 1 bit (ancilla excited)
                        bits_1 = bits + (1,)
                        key_1 = (j, bits_1)
                        if key_1 not in state:
                            state[key_1] = 0.0+0.0j
                        state[key_1] += amp * ea * sin_a
                else:
                    key = (j, bits)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp * ea

    det_state = {(d, bits): amp for (d, bits), amp in state.items() if d in det}
    return det_state


def propagate_two_register_angle(positions, adj, field, src, det, k,
                                 mass_set, blocked=None):
    """Angle-weighted node-label baseline under the same unitary law.

    This keeps the promoted directional path measure and only changes the
    environment architecture. It is the apples-to-apples comparison for the
    slot-resolved fresh-ancilla run above.
    """
    blocked = blocked or set()

    in_deg = [0] * len(positions)
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(len(positions)) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    state = {(s, -1): 1.0 / len(src) + 0.0j for s in src}

    for i in order:
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env, amp in entries.items():
            new_env = i if i in mass_set else env
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
                theta_edge = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA * theta_edge * theta_edge)
                ea = cmath.exp(1j * k * act) * w / (L ** 1.0)
                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0 + 0.0j
                state[key] += amp * ea

    return {(d, env): amp for (d, env), amp in state.items() if d in det}


def main():
    print("=" * 70)
    print("LEVEL B: TRUE SLOT-RESOLVED FRESH ANCILLA ON DAGs")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Coupling: α_k = {ALPHA_SCALE} × edge_angle (branch-dependent)")
    print(f"  Env: ancilla bitstring (slot-resolved)")
    print(f"  Seeds: {N_SEEDS}  k-band: {K_BAND}")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'runs':>5s}  {'mass_rng':>9s}  {'env_max':>7s}  "
          f"{'len_max':>7s}  {'pur_fa':>8s}  {'pur_node':>8s}  {'fa_off':>8s}")
    print(f"  {'-' * 72}")

    for nl in N_LIST:
        pfa_list, pn_list, p0_list = [], [], []
        mass_counts = []
        max_envs = 0
        max_bitlen = 0

        for seed in range(N_SEEDS):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            mass_counts.append(len(mass_set))

            for k_val in K_BAND:
                ds_fa = propagate_fresh_ancilla(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k_val, mass_set, setup["blocked"])
                pfa, _, _, _ = compute_detector_metrics(ds_fa, setup["det_list"])
                if not math.isnan(pfa):
                    pfa_list.append(pfa)
                envs = set(bits for (d, bits) in ds_fa.keys())
                max_envs = max(max_envs, len(envs))
                max_bitlen = max(max_bitlen, max((len(b) for b in envs), default=0))

                ds_n = propagate_two_register_angle(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k_val, mass_set, setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                ds_0 = propagate_fresh_ancilla(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k_val, set(), setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pfa_list:
            mass_min = min(mass_counts)
            mass_max = max(mass_counts)
            mass_rng = f"{mass_min}-{mass_max}" if mass_min != mass_max else f"{mass_min}"
            print(f"  {nl:4d}  {len(pfa_list):5d}  {mass_rng:>9s}  {max_envs:7d}  {max_bitlen:7d}  "
                  f"{sum(pfa_list)/len(pfa_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_fa = slot-resolved fresh ancilla")
    print("pur_node = angle-weighted node-label baseline")
    print("fa_off = no coupling (should be ~1.0)")
    print("runs = accepted seed/k combinations")
    print("mass_rng = min-max accepted mass-set size across seeds")
    print("env_max = max distinct bitstrings at detector over all runs")
    print("len_max = max bitstring length (= max encounters) over all runs")
    print()
    print("Interpretation:")
    print("  Encouraging if pur_fa stays flat or falls with N.")
    print("  Failure if pur_fa recoheres at larger N.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
