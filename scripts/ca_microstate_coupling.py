#!/usr/bin/env python3
"""CA microstate coupling: paths sample local CA state at mass cells.

Fallback after graph-memory scars failed. Instead of recording which
edges were traversed, paths sample the local CA microstate (active/
inactive) at each mass node they touch. The env state is the sequence
of sampled microstates.

This bypasses field smoothing because it reads the RAW CA state, not
the relaxed field. Different oscillation phases give different
microstate patterns → different env sequences → decoherence.

The averaging is over oscillation phases (period-3 CA), not over
noise realizations. Each phase gives a different microstate map
→ different env labels at the same mass nodes → different detector
amplitudes.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: ca-microstate-coupling
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


def build_ca_microstates(mass_nodes, n_phases=N_CA_PHASES):
    """Build n_phases microstate maps: which mass nodes are active.

    Phase i: mass_nodes[i::n_phases] are active (microstate=1).
    All others are inactive (microstate=0).
    """
    mass_list = sorted(mass_nodes)
    maps = []
    for phase in range(n_phases):
        active = set(mass_list[phase::n_phases])
        maps.append(active)
    return maps


def propagate_ca_coupled(positions, adj, field, src, det, k,
                         mass_set, active_set, blocked=None):
    """Angle-weighted propagator where env records the CA microstate
    (active/inactive) at each mass node traversed.

    The env is a tuple of (mass_node, active_bit) pairs.
    Capped at last 3 to bound state space.
    """
    MAX_REC = 3
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
        entries = {rec: amp for (node, rec), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for rec, amp in entries.items():
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

                # CA microstate record at mass nodes
                if j in mass_set:
                    bit = 1 if j in active_set else 0
                    new_rec = (rec + ((j, bit),))[-MAX_REC:]
                else:
                    new_rec = rec

                key = (j, new_rec)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, rec): amp for (d, rec), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("CA MICROSTATE COUPLING")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Env: local CA microstate (active/inactive) at mass nodes")
    print(f"  Averaged incoherently over {N_CA_PHASES} CA phases")
    print("=" * 70)
    print()

    print(f"  {'N':>4s}  {'n_mass':>6s}  {'pur_ca':>8s}  {'pur_node':>8s}  {'ca_off':>8s}")
    print(f"  {'-' * 40}")

    for nl in [8, 12, 18]:
        pca_list, pn_list, p0_list = [], [], []
        n_mass_count = 0

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
            ca_phases = build_ca_microstates(mass_set)

            for k in k_band:
                # CA-coupled: average over oscillation phases
                phase_det_states = []
                for active_set in ca_phases:
                    ds = propagate_ca_coupled(
                        positions, adj, setup["field"], setup["src"], setup["det"],
                        k, mass_set, active_set, setup["blocked"])
                    phase_det_states.append(ds)

                # Incoherent average: P = (1/N) Σ_phase Σ_env |ψ(det,env;phase)|²
                # Each phase has its own env states. Combine all as separate env sectors.
                combined = {}
                for phase_idx, ds in enumerate(phase_det_states):
                    for (d, rec), amp in ds.items():
                        key = (d, (phase_idx, rec))
                        combined[key] = amp

                pca, _, _, _ = compute_detector_metrics(combined, setup["det_list"])
                if not math.isnan(pca):
                    pca_list.append(pca)

                # Node-label env (comparison)
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_n = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, setup["mass_set"], setup["blocked"])
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # CA off (unitary baseline)
                ds_0 = propagate_ca_coupled(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, set(), set(), setup["blocked"])
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if pca_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  "
                  f"{sum(pca_list)/len(pca_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_ca = CA microstate coupled (incoherent over phases)")
    print("pur_node = node-label env (comparison)")
    print("ca_off = no coupling (should be ~1.0)")
    print()
    print("PASS: pur_ca does not rise with N")
    print("FAIL: pur_ca rises with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
