#!/usr/bin/env python3
"""True local entangling coupling at mass interactions.

At each mass node, amplitude SPLITS into two channels:
  |system⟩ → cos(α)|system⟩|0_m⟩ + sin(α)|system⟩|1_m⟩

This creates genuine superposition in the local env, not deterministic
assignment. The env state is a configuration of all local qubit states.
Different paths through different mass nodes create different
entanglement patterns → high env entropy → decoherence.

Key difference from qubit-env (architecture 15):
  - qubit-env: deterministic flip (|0⟩→|1⟩ always) → low entropy
  - entangling: superposition split (cos/sin) → high entropy
  Each mass interaction DOUBLES the number of populated env states
  because both branches carry amplitude.

The splitting angle α controls coupling strength:
  α=0: no coupling (unitary baseline)
  α=π/4: maximal splitting (equal superposition)

Uses the promoted angle² β=0.8 propagator.

PStack experiment: entangling-env-decoherence
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
ALPHA = math.pi / 4  # splitting angle (45° — maximal entanglement)


def propagate_entangling(positions, adj, field, src, det, k,
                         mass_set, alpha, blocked=None):
    """Angle-weighted propagator with local entangling coupling at mass.

    State: (node, env_config) → amplitude
    env_config is a frozenset of (mass_node, state) pairs where state ∈ {0, 1}.
    Unvisited mass nodes are implicitly in state 0.

    At each mass node m, the amplitude splits:
      amp → cos(α) × amp  with env unchanged (m stays |0⟩)
      amp → sin(α) × amp  with env excited  (m set to |1⟩)

    If m was already visited (already in config), the existing state
    is kept — no re-splitting. This prevents exponential blowup from
    revisiting the same node.
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

    # State: (node, env_config_frozenset) → amplitude
    state = {}
    for s in src:
        state[(s, frozenset())] = 1.0/len(src) + 0.0j

    cos_a = math.cos(alpha)
    sin_a = math.sin(alpha)

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env, amp in entries.items():
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
                ea = cmath.exp(1j*k*act) * w / (L**1.0)

                if j in mass_set:
                    # Check if this mass node was already visited
                    visited = any(m == j for m, _ in env)
                    if not visited and alpha > 0:
                        # SPLIT: two branches with DIFFERENT env states
                        # Branch 0: env UNCHANGED, amplitude × cos(α)
                        key_0 = (j, env)  # same env as parent
                        if key_0 not in state:
                            state[key_0] = 0.0+0.0j
                        state[key_0] += amp * ea * cos_a

                        # Branch 1: env EXCITED, amplitude × sin(α)
                        env_1 = env | frozenset([(j, 1)])
                        key_1 = (j, env_1)
                        if key_1 not in state:
                            state[key_1] = 0.0+0.0j
                        state[key_1] += amp * ea * sin_a
                    else:
                        # Already visited or α=0: pass through
                        key = (j, env)
                        if key not in state:
                            state[key] = 0.0+0.0j
                        state[key] += amp * ea
                else:
                    # Non-mass node: pass through
                    key = (j, env)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp * ea

    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("ENTANGLING ENV DECOHERENCE")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Coupling: cos({ALPHA:.2f})/sin({ALPHA:.2f}) split at each mass node")
    print(f"  Env: frozenset of (mass_node, 0|1) pairs")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_env':>6s}  "
          f"{'pur_ent':>8s}  {'pur_node':>8s}  {'ent_off':>8s}")
    print(f"  {'-' * 48}")

    for nl in [8, 12, 18]:
        pe_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_envs = 0

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

            # Cap mass to prevent 2^M explosion
            if n_mass_count > 12:
                mass_set = set(sorted(mass_set)[:12])

            for k in k_band:
                # Entangling env
                ds_e = propagate_entangling(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, ALPHA, setup["blocked"])
                pe, _, _, _ = compute_detector_metrics(ds_e, setup["det_list"])
                if not math.isnan(pe):
                    pe_list.append(pe)
                envs = set(env for (d, env) in ds_e.keys())
                max_envs = max(max_envs, len(envs))

                # Node-label env (comparison)
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, setup["mass_set"], setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # Entangling off (α=0, unitary baseline)
                ds_0 = propagate_entangling(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, 0.0, setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pe_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_envs:6d}  "
                  f"{sum(pe_list)/len(pe_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_ent = entangling env (this test)")
    print("pur_node = node-label env (comparison)")
    print("ent_off = α=0 (should be ~1.0, unitary baseline)")
    print()
    print("PASS: pur_ent does not rise with N")
    print("FAIL: pur_ent rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
