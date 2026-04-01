#!/usr/bin/env python3
"""Level B: Fresh-ancilla collision model on real DAG interaction histories.

Extract the stream of mass-region encounters from the actual DAG
propagation, then apply the fresh-ancilla decoherence law from Level A.

For each path through the mass region, record the sequence of
(mass_node, angle) encounters. Two branches (slit A, slit B) produce
different encounter sequences. The branch overlap is computed from
the encounter-by-encounter angle differences using the Level A formula.

Key: the ancilla is indexed by ENCOUNTER SLOT (1st encounter, 2nd
encounter, ...), not by node identity. Different branches may have
different numbers of encounters or encounter different nodes.

The detector-state purity under the fresh-ancilla law:
  For each pair of detector nodes (d1, d2), compute the env-overlap
  between all path-pairs that arrive at d1 via slit A and d2 via slit B.
  The overlap decays with the number of DISTINGUISHABLE encounters.

Simplified implementation: propagate with per-encounter-slot ancillas.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: fresh-ancilla-on-dag
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
ALPHA_BASE = math.pi / 4  # base coupling strength


def propagate_fresh_ancilla(positions, adj, field, src, det, k,
                            mass_set, blocked=None):
    """Propagator with fresh ancilla per mass encounter.

    State: (node, encounter_count) → amplitude
    At each mass node: split cos(α)/sin(α) with a FRESH ancilla
    indexed by the encounter count (not the node id).

    The env state is the encounter count itself — branches with
    different encounter counts are automatically orthogonal.
    Branches with the SAME count but different encounter ANGLES
    get different overlap (computed via the Level A formula).

    Simplified: track encounter count as env. The partial trace
    sums over encounter counts. Within each count, the overlap
    between branches determines the coherence.
    """
    n = len(positions)
    blocked = blocked or set()
    cos_a = math.cos(ALPHA_BASE)
    sin_a = math.sin(ALPHA_BASE)

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

    # State: (node, n_encounters) → amplitude
    # n_encounters = number of mass encounters so far
    # Different n_encounters values are ORTHOGONAL env states
    state = {}
    for s in src:
        state[(s, 0)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {enc: amp for (node, enc), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for n_enc, amp in entries.items():
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
                    # Fresh ancilla: split, increment encounter count
                    # Branch 0: ancilla stays |0⟩, count stays same
                    key_0 = (j, n_enc)
                    if key_0 not in state:
                        state[key_0] = 0.0+0.0j
                    state[key_0] += amp * ea * cos_a

                    # Branch 1: ancilla goes to |1⟩, count increments
                    key_1 = (j, n_enc + 1)
                    if key_1 not in state:
                        state[key_1] = 0.0+0.0j
                    state[key_1] += amp * ea * sin_a
                else:
                    key = (j, n_enc)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp * ea

    det_state = {(d, enc): amp for (d, enc), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("LEVEL B: FRESH-ANCILLA ON REAL DAGs")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Env: encounter count (fresh ancilla per mass encounter)")
    print(f"  α = {ALPHA_BASE:.2f}")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_enc':>6s}  "
          f"{'pur_fa':>8s}  {'pur_node':>8s}  {'fa_off':>8s}")
    print(f"  {'-' * 48}")

    for nl in [8, 12, 18, 25]:
        pfa_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_enc = 0

        for seed in range(4):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            n_mass_count = len(mass_set)

            for k in k_band:
                # Fresh ancilla
                ds_fa = propagate_fresh_ancilla(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pfa, _, _, _ = compute_detector_metrics(ds_fa, setup["det_list"])
                if not math.isnan(pfa):
                    pfa_list.append(pfa)
                encs = set(enc for (d, enc) in ds_fa.keys())
                max_enc = max(max_enc, max(encs) if encs else 0)

                # Node-label (matched)
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # Off baseline
                ds_0 = propagate_fresh_ancilla(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, set(), setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pfa_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_enc:6d}  "
                  f"{sum(pfa_list)/len(pfa_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_fa = fresh-ancilla per encounter")
    print("pur_node = node-label env (comparison)")
    print("fa_off = no coupling (should be ~1.0)")
    print("n_enc = max encounter count reached")
    print()
    print("PASS: pur_fa decreases or stays flat with N")
    print("FAIL: pur_fa rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
