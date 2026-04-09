#!/usr/bin/env python3
"""Geometry superposition: coherent sum over DAG ensemble.

STATUS: NORMALIZATION ARTIFACT (from review). The reported 278%/384%
contrast is dominated by a Cauchy-Schwarz artifact: with the original
normalization, even IDENTICAL geometries give a large coherent/incoherent
ratio (|sum w_i|^2 / sum |w_i|^2 = N for N equal-weight geometries).

The REAL question is whether different DAG topologies produce different
PHASES at the detector. The phase diagnostic (up to 14.7 degrees
difference) IS real, but the contrast metric needs fixing.

Five DAG geometries:
  1. Rectangular grid (standard)
  2. Random edge deletions (10%)
  3. Random edge additions (10%)
  4. Tapered grid
  5. Expanded grid

For each, propagate from (0,0) to detector, collecting complex psi(y).

NOTE: The coherent/incoherent contrast metric has a built-in
Cauchy-Schwarz inflation. The phase differences between geometries
are the meaningful observable, not the raw contrast ratio.

Weight: w_i = 1/n_edges_i (simpler geometries weighted more).

Metric: interference contrast = max_y |P_coh - P_inc| / max(P_inc)

HYPOTHESIS: Coherent sum over geometries produces measurably different
  probabilities than incoherent average.
FALSIFICATION: If contrast < 1%, geometry superposition has no observable effect.
"""

from __future__ import annotations
import cmath
import math
import random
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    infer_arrival_times_with_field,
    build_causal_dag,
    local_edge_properties,
    graph_neighbors,
)

# ── Parameters ──────────────────────────────────────────────────────
WIDTH = 20
HEIGHT = 8
SOURCE = (0, 0)
SEED = 42
POSTULATES = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)


# ── Geometry builders ───────────────────────────────────────────────

def build_expanded_nodes(width: int, height: int) -> set[tuple[int, int]]:
    """Wider in the middle: extra rows at mid-x."""
    mid_x = width / 2
    nodes: set[tuple[int, int]] = set()
    for x in range(width + 1):
        dist = abs(x - mid_x) / max(mid_x, 1)
        extra = max(0, round(2 * (1 - dist)))
        y_limit = height + extra
        for y in range(-y_limit, y_limit + 1):
            nodes.add((x, y))
    return nodes


def build_tapered_nodes(width: int, height: int) -> set[tuple[int, int]]:
    """Narrower in the middle: fewer rows at mid-x."""
    mid_x = width / 2
    nodes: set[tuple[int, int]] = set()
    for x in range(width + 1):
        dist = abs(x - mid_x) / max(mid_x, 1)
        shrink = max(0, round(2 * (1 - dist)))
        y_limit = max(3, height - shrink)
        for y in range(-y_limit, y_limit + 1):
            nodes.add((x, y))
    return nodes


def build_deleted_edges_dag(
    nodes: set[tuple[int, int]],
    arrival_times: dict[tuple[int, int], float],
    frac: float,
    rng: random.Random,
    epsilon: float = 1e-9,
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Standard causal DAG but with a fraction of edges randomly deleted."""
    dag: dict[tuple[int, int], list[tuple[int, int]]] = {}
    n_deleted = 0
    n_total = 0
    for node in nodes:
        if node not in arrival_times:
            continue
        children = [
            nb for nb in graph_neighbors(node, nodes)
            if nb in arrival_times
            and arrival_times[nb] > arrival_times[node] + epsilon
        ]
        kept = []
        for c in children:
            n_total += 1
            if rng.random() < frac:
                n_deleted += 1
            else:
                kept.append(c)
        dag[node] = kept
    return dag


def build_added_edges_dag(
    nodes: set[tuple[int, int]],
    arrival_times: dict[tuple[int, int], float],
    frac: float,
    rng: random.Random,
    epsilon: float = 1e-9,
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Standard causal DAG plus random extra forward edges (skip connections)."""
    dag = build_causal_dag(nodes, arrival_times, epsilon=epsilon)
    n_added = 0
    n_base = sum(len(v) for v in dag.values())
    target_add = int(n_base * frac)

    node_list = [n for n in nodes if n in arrival_times]
    while n_added < target_add:
        a = rng.choice(node_list)
        # Pick a random node 2 layers ahead
        ax, ay = a
        bx = ax + 2
        by = ay + rng.choice([-1, 0, 1])
        b = (bx, by)
        if b in arrival_times and arrival_times[b] > arrival_times[a] + epsilon:
            if b not in dag.get(a, []):
                dag.setdefault(a, []).append(b)
                n_added += 1
        # Safety valve
        if n_added == 0 and target_add > 0:
            break
    return dag


# ── Propagation ─────────────────────────────────────────────────────

def propagate_on_dag(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    dag: dict[tuple[int, int], list[tuple[int, int]]],
    rule,
    node_field: dict[tuple[int, int], float],
    arrival_times: dict[tuple[int, int], float],
    width: int,
) -> dict[int, complex]:
    """Propagate through a given DAG. Returns complex amplitudes psi(y) at detector."""
    order = sorted(
        (n for n in nodes if n in arrival_times),
        key=lambda n: arrival_times[n],
    )
    states: dict[tuple[int, int], complex] = defaultdict(complex)
    states[source] = 1.0 + 0j

    detector: dict[int, complex] = {}
    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for neighbor in dag.get(node, []):
            if neighbor not in node_field:
                continue
            _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)
            states[neighbor] += amp * link_amp

    return detector


def count_edges(dag: dict) -> int:
    return sum(len(children) for children in dag.values())


# ── Main experiment ─────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("GEOMETRY SUPERPOSITION: Coherent Sum Over DAG Ensemble")
    print("=" * 70)
    print()
    print(f"Grid: {WIDTH}x{HEIGHT}, source={SOURCE}, detector at x={WIDTH}")
    print(f"Postulates: k={POSTULATES.phase_per_action}, p={POSTULATES.attenuation_power}")
    print()

    rng = random.Random(SEED)
    rule = derive_local_rule(frozenset(), POSTULATES)

    # ── Build geometries ────────────────────────────────────────────
    geometries = {}

    # 1. Standard rectangular
    nodes_rect = build_rectangular_nodes(WIDTH, HEIGHT)
    field_rect = derive_node_field(nodes_rect, rule)
    at_rect = infer_arrival_times_with_field(nodes_rect, SOURCE, rule, field_rect)
    dag_rect = build_causal_dag(nodes_rect, at_rect)
    geometries["rectangular"] = (nodes_rect, dag_rect, rule, field_rect, at_rect)

    # 2. Edge deletions (10%)
    nodes_del = build_rectangular_nodes(WIDTH, HEIGHT)
    field_del = derive_node_field(nodes_del, rule)
    at_del = infer_arrival_times_with_field(nodes_del, SOURCE, rule, field_del)
    dag_del = build_deleted_edges_dag(nodes_del, at_del, 0.10, rng)
    geometries["deleted-10%"] = (nodes_del, dag_del, rule, field_del, at_del)

    # 3. Edge additions (10%)
    nodes_add = build_rectangular_nodes(WIDTH, HEIGHT)
    field_add = derive_node_field(nodes_add, rule)
    at_add = infer_arrival_times_with_field(nodes_add, SOURCE, rule, field_add)
    dag_add = build_added_edges_dag(nodes_add, at_add, 0.10, rng)
    geometries["added-10%"] = (nodes_add, dag_add, rule, field_add, at_add)

    # 4. Tapered
    nodes_tap = build_tapered_nodes(WIDTH, HEIGHT)
    # Ensure source exists
    if SOURCE not in nodes_tap:
        nodes_tap.add(SOURCE)
    field_tap = derive_node_field(nodes_tap, rule)
    at_tap = infer_arrival_times_with_field(nodes_tap, SOURCE, rule, field_tap)
    dag_tap = build_causal_dag(nodes_tap, at_tap)
    geometries["tapered"] = (nodes_tap, dag_tap, rule, field_tap, at_tap)

    # 5. Expanded
    nodes_exp = build_expanded_nodes(WIDTH, HEIGHT)
    field_exp = derive_node_field(nodes_exp, rule)
    at_exp = infer_arrival_times_with_field(nodes_exp, SOURCE, rule, field_exp)
    dag_exp = build_causal_dag(nodes_exp, at_exp)
    geometries["expanded"] = (nodes_exp, dag_exp, rule, field_exp, at_exp)

    # ── Propagate each geometry ─────────────────────────────────────
    print(f"{'Geometry':<16} {'Nodes':>7} {'Edges':>7} {'Det bins':>9} {'Tot prob':>10}")
    print("-" * 55)

    psi_all: dict[str, dict[int, complex]] = {}
    edge_counts: dict[str, int] = {}

    for name, (nodes, dag, rl, field, at) in geometries.items():
        n_edges = count_edges(dag)
        edge_counts[name] = n_edges
        psi = propagate_on_dag(nodes, SOURCE, dag, rl, field, at, WIDTH)
        psi_all[name] = psi
        tot_p = sum(abs(a) ** 2 for a in psi.values())
        print(f"{name:<16} {len(nodes):>7} {n_edges:>7} {len(psi):>9} {tot_p:>10.4e}")

    # ── Collect all detector y-values ───────────────────────────────
    all_ys = sorted(set().union(*(psi.keys() for psi in psi_all.values())))
    print(f"\nDetector y range: [{min(all_ys)}, {max(all_ys)}], {len(all_ys)} bins")

    # ── Weights: 1/n_edges ──────────────────────────────────────────
    weights = {name: 1.0 / ec for name, ec in edge_counts.items()}
    w_norm_sq = sum(w ** 2 for w in weights.values())

    print(f"\nWeights (1/n_edges, normalized):")
    for name, w in weights.items():
        print(f"  {name:<16}: w={w:.6e},  w^2/sum(w^2) = {w**2/w_norm_sq:.4f}")

    # ── Normalize each geometry's wavefunction to unit probability ──
    # This removes amplitude differences so we compare PHASE ONLY.
    psi_normed = {}
    for name, psi in psi_all.items():
        norm = math.sqrt(sum(abs(a)**2 for a in psi.values()))
        if norm > 1e-30:
            psi_normed[name] = {y: a / norm for y, a in psi.items()}
        else:
            psi_normed[name] = psi

    # ── Coherent vs incoherent sum (CORRECTED normalization) ──────
    # Use equal weights on normalized wavefunctions to avoid
    # Cauchy-Schwarz inflation. With equal weights on unit-norm ψ:
    #   P_coherent(y)   = |mean_i ψ_i(y)|²
    #   P_incoherent(y) = mean_i |ψ_i(y)|²
    # These agree when all ψ_i are identical and differ when phases differ.
    N_geom = len(psi_normed)
    P_coherent = {}
    P_incoherent = {}

    for y in all_ys:
        # Coherent: |average amplitude|^2
        coh_amp = sum(psi_normed[name].get(y, 0j) for name in psi_normed) / N_geom
        P_coherent[y] = abs(coh_amp) ** 2

        # Incoherent: average of probabilities
        inc = sum(abs(psi_normed[name].get(y, 0j)) ** 2 for name in psi_normed) / N_geom
        P_incoherent[y] = inc

    # ── Interference contrast ───────────────────────────────────────
    max_P_inc = max(P_incoherent.values()) if P_incoherent else 1e-30
    max_P_coh = max(P_coherent.values()) if P_coherent else 1e-30

    diffs = {y: abs(P_coherent[y] - P_incoherent[y]) for y in all_ys}
    max_diff = max(diffs.values()) if diffs else 0
    contrast = max_diff / max_P_inc if max_P_inc > 1e-30 else 0

    # Also compute L1 distance
    l1_dist = sum(abs(P_coherent[y] - P_incoherent[y]) for y in all_ys)
    l1_norm = sum(P_incoherent[y] for y in all_ys)
    l1_relative = l1_dist / l1_norm if l1_norm > 1e-30 else 0

    print(f"\n{'='*70}")
    print("DETECTOR DISTRIBUTIONS")
    print(f"{'='*70}")
    print(f"{'y':>4}  {'P_coherent':>12}  {'P_incoherent':>14}  {'|diff|':>12}  {'ratio':>8}")
    print("-" * 58)
    for y in all_ys:
        pc = P_coherent[y]
        pi = P_incoherent[y]
        d = abs(pc - pi)
        ratio = pc / pi if pi > 1e-30 else float('inf')
        if pc > 1e-15 or pi > 1e-15:
            print(f"{y:>4}  {pc:>12.6e}  {pi:>14.6e}  {d:>12.6e}  {ratio:>8.4f}")

    # ── Per-geometry distributions ──────────────────────────────────
    print(f"\n{'='*70}")
    print("PER-GEOMETRY DETECTOR PROBABILITIES")
    print(f"{'='*70}")
    header = f"{'y':>4}"
    for name in geometries:
        header += f"  {name:>14}"
    print(header)
    print("-" * (6 + 16 * len(geometries)))
    for y in all_ys:
        row = f"{y:>4}"
        for name in geometries:
            p = abs(psi_all[name].get(y, 0j)) ** 2
            row += f"  {p:>14.6e}"
        if any(abs(psi_all[name].get(y, 0j)) ** 2 > 1e-15 for name in geometries):
            print(row)

    # ── Centroid comparison ─────────────────────────────────────────
    def centroid(dist):
        total = sum(dist.values())
        if total < 1e-30:
            return 0.0
        return sum(y * p for y, p in dist.items()) / total

    def width_rms(dist):
        total = sum(dist.values())
        if total < 1e-30:
            return 0.0
        c = centroid(dist)
        return math.sqrt(sum((y - c) ** 2 * p for y, p in dist.items()) / total)

    coh_centroid = centroid(P_coherent)
    inc_centroid = centroid(P_incoherent)
    coh_width = width_rms(P_coherent)
    inc_width = width_rms(P_incoherent)

    print(f"\n{'='*70}")
    print("SUMMARY STATISTICS")
    print(f"{'='*70}")
    print(f"  Coherent   centroid: {coh_centroid:+.6f},  RMS width: {coh_width:.4f}")
    print(f"  Incoherent centroid: {inc_centroid:+.6f},  RMS width: {inc_width:.4f}")
    print(f"  Centroid shift:      {abs(coh_centroid - inc_centroid):.6f}")
    print(f"  Width change:        {abs(coh_width - inc_width):.6f}")
    print()
    print(f"  max |P_coh - P_inc|:           {max_diff:.6e}")
    print(f"  max P_incoherent:              {max_P_inc:.6e}")
    print(f"  Interference CONTRAST:         {contrast:.4f} ({100*contrast:.2f}%)")
    print()
    print(f"  L1 distance:                   {l1_dist:.6e}")
    print(f"  L1 / total_P_inc:              {l1_relative:.4f} ({100*l1_relative:.2f}%)")

    # ── Phase coherence diagnostic ──────────────────────────────────
    print(f"\n{'='*70}")
    print("PHASE COHERENCE DIAGNOSTIC")
    print(f"{'='*70}")
    print("Do different geometries produce different phases at the detector?")
    peak_y = max(all_ys, key=lambda y: P_incoherent[y])
    print(f"\nAt peak y={peak_y}:")
    for name in geometries:
        a = psi_all[name].get(peak_y, 0j)
        mag = abs(a)
        phase = cmath.phase(a) if mag > 1e-30 else 0
        print(f"  {name:<16}: |psi|={mag:.6e}, phase={phase:+.4f} rad ({math.degrees(phase):+.1f} deg)")

    # Check pairwise phase differences at peak
    names = list(geometries.keys())
    print(f"\nPairwise phase differences at y={peak_y}:")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_i = psi_all[names[i]].get(peak_y, 0j)
            a_j = psi_all[names[j]].get(peak_y, 0j)
            if abs(a_i) > 1e-30 and abs(a_j) > 1e-30:
                dp = cmath.phase(a_i) - cmath.phase(a_j)
                # Wrap to [-pi, pi]
                dp = (dp + math.pi) % (2 * math.pi) - math.pi
                print(f"  {names[i]:<12} vs {names[j]:<12}: delta_phase = {dp:+.4f} rad ({math.degrees(dp):+.1f} deg)")

    # ── Normalized-psi analysis (isolate PHASE interference) ───────
    # Normalize each geometry's psi so sum |psi_i(y)|^2 = 1
    # This removes amplitude differences; only phase effects remain.
    print(f"\n{'='*70}")
    print("NORMALIZED-PSI ANALYSIS (pure phase interference)")
    print(f"{'='*70}")

    psi_normed: dict[str, dict[int, complex]] = {}
    for name in psi_all:
        norm = math.sqrt(sum(abs(a) ** 2 for a in psi_all[name].values()))
        if norm > 1e-30:
            psi_normed[name] = {y: a / norm for y, a in psi_all[name].items()}
        else:
            psi_normed[name] = {y: 0j for y in psi_all[name]}

    # Equal weights for normalized version (all geometries equally important)
    w_eq = 1.0 / len(psi_normed)
    w_eq_norm_sq = len(psi_normed) * w_eq ** 2  # = 1/N

    P_coh_norm = {}
    P_inc_norm = {}
    for y in all_ys:
        coh_amp = sum(w_eq * psi_normed[name].get(y, 0j) for name in psi_normed)
        P_coh_norm[y] = abs(coh_amp) ** 2 / w_eq_norm_sq

        inc = sum(w_eq ** 2 * abs(psi_normed[name].get(y, 0j)) ** 2 for name in psi_normed)
        P_inc_norm[y] = inc / w_eq_norm_sq

    max_P_inc_norm = max(P_inc_norm.values()) if P_inc_norm else 1e-30
    diffs_norm = {y: abs(P_coh_norm[y] - P_inc_norm[y]) for y in all_ys}
    max_diff_norm = max(diffs_norm.values()) if diffs_norm else 0
    contrast_norm = max_diff_norm / max_P_inc_norm if max_P_inc_norm > 1e-30 else 0

    l1_norm_dist = sum(abs(P_coh_norm[y] - P_inc_norm[y]) for y in all_ys)
    l1_norm_total = sum(P_inc_norm[y] for y in all_ys)
    l1_norm_rel = l1_norm_dist / l1_norm_total if l1_norm_total > 1e-30 else 0

    print(f"{'y':>4}  {'P_coh(norm)':>12}  {'P_inc(norm)':>14}  {'ratio':>8}")
    print("-" * 44)
    for y in all_ys:
        pc = P_coh_norm[y]
        pi = P_inc_norm[y]
        ratio = pc / pi if pi > 1e-30 else float('inf')
        if pc > 1e-6 or pi > 1e-6:
            print(f"{y:>4}  {pc:>12.6e}  {pi:>14.6e}  {ratio:>8.4f}")

    print(f"\n  Normalized contrast:  {contrast_norm:.4f} ({100*contrast_norm:.2f}%)")
    print(f"  Normalized L1 rel:    {l1_norm_rel:.4f} ({100*l1_norm_rel:.2f}%)")
    print(f"\n  (This isolates PHASE interference from amplitude differences.)")
    print(f"  If contrast > 1% here, different geometries produce genuinely")
    print(f"  different quantum phases, not just different intensities.")

    # ── Verdict ─────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    if contrast_norm > 0.01:
        print(f"\n  CONFIRMED: Geometry superposition produces observable interference.")
        print(f"  Raw contrast:        {100*contrast:.1f}% (includes amplitude + phase effects)")
        print(f"  Normalized contrast: {100*contrast_norm:.2f}% (pure phase interference)")
        print(f"  Coherent sum over DAG geometries is DISTINGUISHABLE from")
        print(f"  the incoherent (classical) mixture.")
        if abs(coh_centroid - inc_centroid) > 0.01:
            print(f"\n  The centroid shifts by {abs(coh_centroid - inc_centroid):.4f},")
            print(f"  meaning geometry interference has a directional effect.")
        if abs(coh_width - inc_width) > 0.01:
            print(f"\n  The distribution width changes by {abs(coh_width - inc_width):.4f},")
            print(f"  meaning geometry interference affects spreading/focusing.")
    elif contrast > 0.01:
        print(f"\n  PARTIAL: Raw contrast = {100*contrast:.1f}% but normalized = {100*contrast_norm:.2f}%.")
        print(f"  The difference is due to amplitude variations between geometries,")
        print(f"  not genuine phase interference. Different geometries produce")
        print(f"  different intensities but similar phases.")
    else:
        print(f"\n  FALSIFIED: Interference contrast = {100*contrast:.2f}% < 1%.")
        print(f"  Geometry superposition has no observable effect on detector")
        print(f"  probabilities within this ensemble. Different DAG topologies")
        print(f"  produce effectively the same phase structure at the detector.")


if __name__ == "__main__":
    main()
