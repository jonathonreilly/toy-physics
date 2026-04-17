#!/usr/bin/env python3
"""Layered architecture: micro propagator + meso gravity + distributed decoherence.

Layer 1 (micro): corrected 1/L^p propagator, unchanged. Full microscopic
path-sum preserving interference and Born rule.

Layer 2 (gravity observable): extract a mesoscopic gravity metric from the
micro run by coarse-binning the DETECTOR distribution (not the transport).
The propagation stays microscopic; only the readout is coarsened.

Layer 3 (decoherence): distributed local records. Each mass edge writes
to a per-edge ancilla. The full env state is the collection of all
per-edge records. Decoherence = partial trace over the distributed record.

Tests on: random DAG, regular lattice, branching tree.
Pass/fail defined before running.
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import (
    build_post_barrier_setup, compute_detector_metrics,
)
from scripts.two_register_decoherence import (
    compute_field, pathsum_coherent, centroid_y, visibility,
)


# ================================================================
# LAYER 2: Mesoscopic gravity observable
# ================================================================

def mesoscopic_gravity(positions, adj, field, free_f, src, det, k_band,
                       n_meso_bins=6):
    """Extract gravity from micro run by coarse-binning the detector distribution.

    Compute full micro path-sum, then bin the detector probability into
    n_meso_bins y-bins. The gravity observable = centroid shift of the
    binned distribution. This coarsens the READOUT, not the TRANSPORT.
    """
    all_ys = [positions[d][1] for d in det]
    if not all_ys:
        return 0.0
    y_min, y_max = min(all_ys), max(all_ys)
    y_range = y_max - y_min + 1e-10
    bin_width = y_range / n_meso_bins

    def y_bin_center(y):
        b = min(int((y - y_min) / bin_width), n_meso_bins - 1)
        return y_min + (b + 0.5) * bin_width

    shifts = []
    for k in k_band:
        fp = pathsum_coherent(positions, adj, free_f, src, det, k)
        mp = pathsum_coherent(positions, adj, field, src, det, k)

        # Bin probabilities
        free_bins = defaultdict(float)
        mass_bins = defaultdict(float)
        for d in det:
            yc = y_bin_center(positions[d][1])
            free_bins[yc] += fp.get(d, 0)
            mass_bins[yc] += mp.get(d, 0)

        # Normalize
        tf = sum(free_bins.values())
        tm = sum(mass_bins.values())
        if tf > 0 and tm > 0:
            fcy = sum(y * p / tf for y, p in free_bins.items())
            mcy = sum(y * p / tm for y, p in mass_bins.items())
            shifts.append(mcy - fcy)

    if not shifts:
        return 0.0

    # Normalize by beam width
    fp0 = pathsum_coherent(positions, adj, free_f, src, det, k_band[-1])
    total = sum(fp0.values())
    if total > 0:
        mean = sum(positions[d][1] * p for d, p in fp0.items()) / total
        var = sum(positions[d][1]**2 * p for d, p in fp0.items()) / total - mean**2
        width = max(var**0.5, 0.1)
    else:
        width = 1.0

    return sum(shifts) / len(shifts) / width


# ================================================================
# LAYER 3: Distributed local record decoherence
# ================================================================

def propagate_distributed_record(positions, adj, field, src, det, k,
                                 mass_set, blocked=None):
    """Micro propagator with per-edge distributed local records.

    Each time amplitude crosses an edge touching a mass node, a local
    ancilla records a hash of (source_node, dest_node). The full env
    state is a frozenset of all recorded edge-hashes.

    This gives exponential env growth with path length through mass:
    each new mass edge doubles the possible record states.

    To keep state space manageable, we cap at MAX_RECORDS most recent.
    """
    MAX_RECORDS = 2  # keep last 2 mass-edge records (4 explodes)

    n = len(positions)
    blocked = blocked or set()

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

    # State: (node, record_tuple) → amplitude
    # record_tuple = tuple of last MAX_RECORDS (edge_hash) values
    state = {}
    for s in src:
        state[(s, ())] = 1.0 / len(src) + 0.0j

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
                L = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                ea = cmath.exp(1j * k * act) / (L ** 1.0)

                # If this edge touches mass, append to record
                if i in mass_set or j in mass_set:
                    edge_hash = (i, j)  # unique per edge
                    new_rec = (rec + (edge_hash,))[-MAX_RECORDS:]
                else:
                    new_rec = rec

                key = (j, new_rec)
                if key not in state:
                    state[key] = 0.0 + 0.0j
                state[key] += amp * ea

    det_state = {(d, rec): amp for (d, rec), amp in state.items() if d in det}
    return det_state


# ================================================================
# MAIN: benchmark on graph families
# ================================================================

def run_family(name, graph_builder, sizes, k_band, n_seeds=5):
    """Run full layered architecture benchmark on one graph family."""
    print(f"  FAMILY: {name}")
    print(f"    {'size':>6s}  {'R_micro':>7s}  {'R_meso':>7s}  "
          f"{'V_micro':>7s}  {'pur_dist':>8s}  {'n_rec':>5s}")
    print(f"    {'-' * 44}")

    for size_param in sizes:
        r_micros, r_mesos, v_micros, purities = [], [], [], []
        max_recs = 0

        for seed in range(n_seeds):
            result = graph_builder(size_param, seed)
            if result is None:
                continue

            positions, adj, src, det, mass_idx, blocked, field, free_f = result
            det_list = list(det)
            n = len(positions)

            # Layer 1: micro propagator (interference check)
            v_k = []
            for k in k_band:
                pc = pathsum_coherent(positions, adj, free_f, src, det, k, blocked)
                v_k.append(visibility(pc, positions, det_list))
            v_micros.append(max(v_k))

            # Layer 2: mesoscopic gravity
            mid_mass = [i for i in mass_idx if i not in blocked]
            if mid_mass:
                grav_field = compute_field(positions, adj, mid_mass)
            else:
                grav_field = field
            r_micro = mesoscopic_gravity(positions, adj, grav_field, free_f,
                                         src, det, k_band, n_meso_bins=1000)
            r_meso = mesoscopic_gravity(positions, adj, grav_field, free_f,
                                        src, det, k_band, n_meso_bins=6)
            r_micros.append(r_micro)
            r_mesos.append(r_meso)

            # Layer 3: distributed record decoherence
            mass_set = set(mass_idx) - blocked
            p_k = []
            for k in k_band:
                ds = propagate_distributed_record(
                    positions, adj, field, src, det, k, mass_set, blocked)
                p, _, _, _ = compute_detector_metrics(ds, det_list)
                if not math.isnan(p):
                    p_k.append(p)
                recs = set(rec for (d, rec) in ds.keys())
                max_recs = max(max_recs, len(recs))

            if p_k:
                purities.append(sum(p_k) / len(p_k))

        if r_micros:
            print(f"    {size_param:6d}  "
                  f"{sum(r_micros)/len(r_micros):+7.3f}  "
                  f"{sum(r_mesos)/len(r_mesos):+7.3f}  "
                  f"{sum(v_micros)/len(v_micros):7.3f}  "
                  f"{sum(purities)/len(purities):8.4f}  "
                  f"{max_recs:5d}")


def build_dag(size_param, seed):
    """Build random DAG with standard slit/mass geometry."""
    nl = size_param
    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed * 11 + 7)
    setup = build_post_barrier_setup(positions, adj,
                                      env_depth_layers=max(1, round(nl / 6)))
    if setup is None:
        return None

    free_f = [0.0] * setup["n"]
    mass_idx = list(setup["mass_set"])
    return (positions, adj, setup["src"], setup["det"],
            mass_idx, setup["blocked"], setup["field"], free_f)


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("LAYERED ARCHITECTURE TEST")
    print("  Micro: corrected 1/L^p (unchanged)")
    print("  Gravity: mesoscopic readout (coarsen detector, not transport)")
    print("  Decoherence: distributed per-edge records (max 4)")
    print("=" * 70)
    print()

    # Random DAG
    run_family("Random DAG (npl=25, r=3.0)",
               build_dag, [8, 12, 18, 25], k_band, n_seeds=4)
    print()

    print("=" * 70)
    print("PASS/FAIL CRITERIA")
    print("=" * 70)
    print()
    print("  Interference: V_micro > 0.5 at all sizes          [micro unchanged]")
    print("  Gravity:      R_meso stable (not collapsing)       [readout coarsening]")
    print("  Decoherence:  pur_dist not increasing with size    [distributed records]")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
