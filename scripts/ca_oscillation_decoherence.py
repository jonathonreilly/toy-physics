#!/usr/bin/env python3
"""CA oscillation decoherence: mass's own dynamics as environment bath.

The mass oscillates with period P. At each oscillation phase, different
cells are active → different field → different action → different fringes.
The detector probability is the incoherent average over oscillation phases:

  P(det) = (1/P) Σ_phase |ψ(det; field_phase)|²

This is decoherence because the oscillation phases are orthogonal
internal states of the mass. Tracing over them removes cross-phase
coherence.

Key scaling property: on larger graphs, paths traverse MORE mass cells
that differ between phases → total action difference GROWS →
decoherence should STRENGTHEN (not weaken) with graph size.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: ca-oscillation-decoherence
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
from scripts.two_register_decoherence import centroid_y
from scripts.normalized_path_measure import edge_weight

BETA = 0.8
N_PHASES = 3  # period-3 oscillator


def build_oscillation_fields(positions, adj, mass_nodes, n_phases=N_PHASES):
    """Build n_phases different field configurations by rotating which
    mass nodes are active at each phase.

    Phase i: mass_nodes[i::n_phases] are active (field=1), rest inactive.
    This models a period-n_phases oscillator where different cells
    are active at different times.
    """
    mass_list = sorted(mass_nodes)
    n = len(positions)

    fields = []
    for phase in range(n_phases):
        active = set(mass_list[phase::n_phases])

        # Laplacian relaxation with active nodes
        undirected = defaultdict(set)
        for i, nbs in adj.items():
            for j in nbs:
                undirected[i].add(j)
                undirected[j].add(i)

        field = [1.0 if i in active else 0.0 for i in range(n)]
        for _ in range(50):
            nf = [0.0]*n
            for i in range(n):
                if i in active:
                    nf[i] = 1.0
                elif undirected.get(i):
                    nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
            field = nf
        fields.append(field)

    return fields


def propagate_angle_weighted(positions, adj, field, src, det, k, blocked=None):
    """Angle-weighted corrected propagator (promoted candidate)."""
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
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def visibility(probs, positions, det_list):
    py = defaultdict(float)
    for d in det_list:
        py[positions[d][1]] += probs.get(d, 0)
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("CA OSCILLATION DECOHERENCE")
    print(f"  Period-{N_PHASES} oscillator, angle² β={BETA}")
    print(f"  P(det) = (1/{N_PHASES}) Σ_phase |ψ(det; field_phase)|²")
    print("=" * 70)
    print()

    # Decoherence scaling
    print("DECOHERENCE SCALING")
    print(f"  {'N':>4s}  {'V_static':>8s}  {'V_osc':>8s}  {'V_drop':>8s}  {'n_mass':>6s}")
    print(f"  {'-' * 40}")

    for nl in [8, 10, 12, 15, 18, 20, 25]:
        v_statics, v_oscs = [], []
        n_mass_total = 0

        for seed in range(5):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_nodes = list(setup["mass_set"])
            n_mass_total = len(mass_nodes)

            if len(mass_nodes) < N_PHASES:
                continue

            # Build oscillation fields
            osc_fields = build_oscillation_fields(positions, adj, mass_nodes)

            # Static field (all mass active, baseline)
            static_field = setup["field"]

            # Measure V with slits
            blocked = setup["blocked"]

            for k in k_band:
                # Static V (mass present, all active)
                ps = propagate_angle_weighted(positions, adj, static_field,
                    setup["src"], setup["det"], k, blocked)
                vs = visibility(ps, positions, setup["det_list"])
                v_statics.append(vs)

                # Oscillation-averaged V
                avg_probs = {d: 0.0 for d in setup["det"]}
                for phase_field in osc_fields:
                    pp = propagate_angle_weighted(positions, adj, phase_field,
                        setup["src"], setup["det"], k, blocked)
                    for d in setup["det"]:
                        avg_probs[d] += pp.get(d, 0)

                # Normalize the average
                total = sum(avg_probs.values())
                if total > 0:
                    avg_probs = {d: p/total for d, p in avg_probs.items()}
                vo = visibility(avg_probs, positions, setup["det_list"])
                v_oscs.append(vo)

        if v_statics and v_oscs:
            mean_vs = sum(v_statics)/len(v_statics)
            mean_vo = sum(v_oscs)/len(v_oscs)
            print(f"  {nl:4d}  {mean_vs:8.4f}  {mean_vo:8.4f}  "
                  f"{mean_vs-mean_vo:+8.4f}  {n_mass_total:6d}")

    print()
    print("V_static = V with all mass active (baseline coherent)")
    print("V_osc = V averaged over oscillation phases (decoherence)")
    print("V_drop = V_static - V_osc (positive = decoherence)")
    print()
    print("PASS: V_drop increases or stays stable with N")
    print("FAIL: V_drop decreases with N (same as finite-register)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
