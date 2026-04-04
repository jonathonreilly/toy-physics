#!/usr/bin/env python3
"""Mesoscopic persistent-record overlap kernel on generated DAGs.

This pilot turns the "split -> parallel universes with residual connection"
idea into a bounded reduced-density experiment.

Model:
- amplitude still branches over the DAG path sum
- when a branch enters the post-barrier interaction region, it writes to a
  mesoscopic persistent record cell rather than an exact node label
- the final detector state is indexed by the persistent record state
- different record states are not forced orthogonal; instead they keep a soft
  overlap kernel

    K(r, r') = exp(-gamma * ||r - r'||^2)

Interpretation:
- gamma = 0       -> fully coherent limit
- gamma >> 1      -> weakly connected "universes"
- exact trace     -> fully orthogonal record sectors

This sits between the repo's earlier deterministic-label and fully orthogonal
environment experiments. The hope is that mesoscopic persistent records may
retain slit-discriminating structure without exploding into ultra-thin branch
weights.

Optional bounded refinements:
- a side marker bit for upper/lower packet provenance
- a packet-placement bit for core/flank placement relative to the center band
- an entry-timing bit for early/late first contact with the mass worldtube
"""

from __future__ import annotations

import argparse
import cmath
import math
import os
import sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics
from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8
DEFAULT_K_BAND = (3.0, 5.0, 7.0)
DIR_BINS = 3

RecordState = tuple[tuple[int, int], ...]


def parse_int_list(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for src, nbs in adj.items():
        for dst in nbs:
            in_deg[dst] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        node = q.popleft()
        order.append(node)
        for nb in adj.get(node, []):
            in_deg[nb] -= 1
            if in_deg[nb] == 0:
                q.append(nb)
    return order


def update_record(record: RecordState, cell_idx: int, max_count: int) -> RecordState:
    items = list(record)
    for idx, (cell, count) in enumerate(items):
        if cell != cell_idx:
            continue
        new_count = min(max_count, count + 1)
        if new_count == count:
            return record
        items[idx] = (cell, new_count)
        return tuple(items)
    items.append((cell_idx, 1))
    items.sort()
    return tuple(items)


def has_marker_in_range(record: RecordState, start_idx: int, width: int) -> bool:
    end_idx = start_idx + width
    return any(start_idx <= cell_idx < end_idx for cell_idx, _ in record)


def marker_value_in_range(record: RecordState, start_idx: int, width: int) -> int | None:
    end_idx = start_idx + width
    for cell_idx, _ in record:
        if start_idx <= cell_idx < end_idx:
            return cell_idx - start_idx
    return None


def barrier_env_layers(setup: dict[str, object]) -> list[int]:
    layers = setup["layers"]
    bl_idx = len(layers) // 3
    start = bl_idx + 1
    stop = min(len(layers), start + setup["env_depth_layers"])
    return layers[start:stop]


def record_cell_count(setup: dict[str, object], y_bins: int) -> int:
    return len(barrier_env_layers(setup)) * y_bins * DIR_BINS


def side_marker_base(setup: dict[str, object], y_bins: int) -> int:
    return record_cell_count(setup, y_bins)


def record_cell_index(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    src_node: int,
    dst_node: int,
    y_bins: int,
    mass_y_half: float,
) -> int | None:
    env_layers = barrier_env_layers(setup)
    layer_to_rel = {layer: idx for idx, layer in enumerate(env_layers)}
    layer = round(positions[dst_node][0])
    rel_layer = layer_to_rel.get(layer)
    if rel_layer is None:
        return None

    cy = float(setup["cy"])
    y_lo = cy - mass_y_half
    y_hi = cy + mass_y_half
    y = positions[dst_node][1]
    if y_hi <= y_lo:
        return None
    y_bin = int((y - y_lo) / (y_hi - y_lo) * y_bins)
    y_bin = max(0, min(y_bins - 1, y_bin))

    dy = positions[dst_node][1] - positions[src_node][1]
    if dy < -1e-9:
        dir_bin = 0
    elif dy > 1e-9:
        dir_bin = 2
    else:
        dir_bin = 1

    return rel_layer * (y_bins * DIR_BINS) + y_bin * DIR_BINS + dir_bin


def side_marker_cell(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    src_node: int,
    dst_node: int,
    y_bins: int,
) -> int:
    """Return a bounded persistent packet-side marker cell.

    The marker is written once per branch the first time the branch records
    a mass interaction. We use the incoming side of the branch relative to the
    center line as a compact proxy for slit / packet side.
    """
    cy = float(setup["cy"])
    y_ref = positions[src_node][1]
    if abs(y_ref - cy) <= 1e-9:
        y_ref = positions[dst_node][1]
    side_idx = 0 if y_ref >= cy else 1
    return side_marker_base(setup, y_bins) + side_idx


def packet_marker_base(setup: dict[str, object], y_bins: int, include_side_bit: bool) -> int:
    base = record_cell_count(setup, y_bins)
    if include_side_bit:
        base += 2
    return base


def entry_marker_base(
    setup: dict[str, object],
    y_bins: int,
    include_side_bit: bool,
    include_packet_bit: bool,
) -> int:
    base = packet_marker_base(setup, y_bins, include_side_bit)
    if include_packet_bit:
        base += 2
    return base


def violation_marker_base(
    setup: dict[str, object],
    y_bins: int,
    include_side_bit: bool,
    include_packet_bit: bool,
    include_entry_bit: bool,
) -> int:
    base = entry_marker_base(setup, y_bins, include_side_bit, include_packet_bit)
    if include_entry_bit:
        base += 2
    return base


def record_family_ranges(
    setup: dict[str, object],
    y_bins: int,
    include_side_bit: bool = False,
    include_packet_bit: bool = False,
    include_entry_bit: bool = False,
    include_violation_bits: bool = False,
) -> dict[str, tuple[int, int]]:
    ranges: dict[str, tuple[int, int]] = {
        "count": (0, record_cell_count(setup, y_bins)),
    }
    if include_side_bit:
        ranges["side"] = (side_marker_base(setup, y_bins), 2)
    if include_packet_bit:
        ranges["packet"] = (packet_marker_base(setup, y_bins, include_side_bit), 2)
    if include_entry_bit:
        ranges["entry"] = (
            entry_marker_base(setup, y_bins, include_side_bit, include_packet_bit),
            2,
        )
    if include_violation_bits:
        ranges["violation"] = (
            violation_marker_base(
                setup,
                y_bins,
                include_side_bit,
                include_packet_bit,
                include_entry_bit,
            ),
            2,
        )
    return ranges


def packet_placement_marker_cell(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    dst_node: int,
    y_bins: int,
    mass_y_half: float,
    include_side_bit: bool,
) -> int:
    """Return a coarse packet-placement marker cell.

    The marker distinguishes a central packet corridor from the outer flank of
    the mass window:

    - core:  |y - cy| <= mass_y_half / 2
    - flank: otherwise

    Combined with the side bit, this gives one bounded extra memory coordinate
    for side + local packet placement without exploding the record state.
    """
    cy = float(setup["cy"])
    is_core = abs(positions[dst_node][1] - cy) <= (mass_y_half / 2.0)
    return packet_marker_base(setup, y_bins, include_side_bit) + (0 if is_core else 1)


def entry_timing_marker_cell(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    dst_node: int,
    y_bins: int,
    include_side_bit: bool,
    include_packet_bit: bool,
) -> int:
    """Return an early/late first-contact timing marker cell."""
    env_layers = barrier_env_layers(setup)
    if not env_layers:
        return entry_marker_base(setup, y_bins, include_side_bit, include_packet_bit)
    layer = round(positions[dst_node][0])
    rel_layer = env_layers.index(layer) if layer in env_layers else 0
    is_early = rel_layer < (len(env_layers) / 2.0)
    return entry_marker_base(setup, y_bins, include_side_bit, include_packet_bit) + (0 if is_early else 1)


def side_value_for_encounter(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    src_node: int,
    dst_node: int,
) -> int:
    cy = float(setup["cy"])
    y_ref = positions[src_node][1]
    if abs(y_ref - cy) <= 1e-9:
        y_ref = positions[dst_node][1]
    return 0 if y_ref >= cy else 1


def packet_value_for_encounter(
    positions: list[tuple[float, float]],
    setup: dict[str, object],
    dst_node: int,
    mass_y_half: float,
) -> int:
    cy = float(setup["cy"])
    is_core = abs(positions[dst_node][1] - cy) <= (mass_y_half / 2.0)
    return 0 if is_core else 1


def propagate_persistent_records(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    setup: dict[str, object],
    k: float,
    y_bins: int,
    max_count: int,
    mass_y_half: float,
    include_side_bit: bool = False,
    include_packet_bit: bool = False,
    include_entry_bit: bool = False,
    active_write: bool = False,
) -> dict[tuple[int, RecordState], complex]:
    """Propagate amplitudes while accumulating persistent mesoscopic records."""
    n = len(positions)
    order = topo_order(adj, n)
    blocked = setup["blocked"]
    src = setup["src"]
    det = setup["det"]
    mass_set = setup["mass_set"]

    state: dict[tuple[int, RecordState], complex] = {}
    empty_record: RecordState = ()
    for s in src:
        state[(s, empty_record)] = 1.0 / len(src) + 0.0j

    processed: set[int] = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {
            record: amp
            for (node, record), amp in list(state.items())
            if node == i and abs(amp) > 1e-30
        }
        if not entries or i in blocked:
            continue

        for record, amp in entries.items():
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
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                edge_amp = cmath.exp(1j * k * act) * math.exp(-BETA * theta * theta) / L

                new_record = record
                if j in mass_set:
                    remembered_side = None
                    remembered_packet = None
                    if include_side_bit:
                        remembered_side = marker_value_in_range(
                            record,
                            side_marker_base(setup, y_bins),
                            2,
                        )
                    if include_packet_bit:
                        remembered_packet = marker_value_in_range(
                            record,
                            packet_marker_base(setup, y_bins, include_side_bit),
                            2,
                        )

                    cell_idx = record_cell_index(
                        positions,
                        setup,
                        i,
                        j,
                        y_bins=y_bins,
                        mass_y_half=mass_y_half,
                    )
                    if cell_idx is not None:
                        allow_count_write = True
                        if active_write:
                            violation_base = violation_marker_base(
                                setup,
                                y_bins,
                                include_side_bit,
                                include_packet_bit,
                                include_entry_bit,
                            )
                            if include_side_bit and remembered_side is not None:
                                current_side = side_value_for_encounter(
                                    positions,
                                    setup,
                                    i,
                                    j,
                                )
                                if current_side != remembered_side:
                                    allow_count_write = False
                                    new_record = update_record(new_record, violation_base + 0, max_count=1)
                            if include_packet_bit and remembered_packet is not None:
                                current_packet = packet_value_for_encounter(
                                    positions,
                                    setup,
                                    j,
                                    mass_y_half=mass_y_half,
                                )
                                if current_packet != remembered_packet:
                                    allow_count_write = False
                                    new_record = update_record(new_record, violation_base + 1, max_count=1)

                        if allow_count_write:
                            new_record = update_record(new_record, cell_idx, max_count=max_count)
                        if include_side_bit:
                            side_base = side_marker_base(setup, y_bins)
                            if not has_marker_in_range(new_record, side_base, 2):
                                marker_idx = side_marker_cell(
                                    positions,
                                    setup,
                                    i,
                                    j,
                                    y_bins=y_bins,
                                )
                                new_record = update_record(new_record, marker_idx, max_count=1)
                        if include_packet_bit:
                            packet_base = packet_marker_base(setup, y_bins, include_side_bit)
                            if not has_marker_in_range(new_record, packet_base, 2):
                                packet_idx = packet_placement_marker_cell(
                                    positions,
                                    setup,
                                    j,
                                    y_bins=y_bins,
                                    mass_y_half=mass_y_half,
                                    include_side_bit=include_side_bit,
                                )
                                new_record = update_record(new_record, packet_idx, max_count=1)
                        if include_entry_bit:
                            entry_base = entry_marker_base(
                                setup,
                                y_bins,
                                include_side_bit,
                                include_packet_bit,
                            )
                            if not has_marker_in_range(new_record, entry_base, 2):
                                entry_idx = entry_timing_marker_cell(
                                    positions,
                                    setup,
                                    j,
                                    y_bins=y_bins,
                                    include_side_bit=include_side_bit,
                                    include_packet_bit=include_packet_bit,
                                )
                                new_record = update_record(new_record, entry_idx, max_count=1)

                key = (j, new_record)
                if key not in state:
                    state[key] = 0.0 + 0.0j
                state[key] += amp * edge_amp

    return {(d, record): amp for (d, record), amp in state.items() if d in det}


def sparse_l2_distance_sq(a: RecordState, b: RecordState) -> int:
    ia = 0
    ib = 0
    total = 0
    while ia < len(a) and ib < len(b):
        cell_a, count_a = a[ia]
        cell_b, count_b = b[ib]
        if cell_a == cell_b:
            diff = count_a - count_b
            total += diff * diff
            ia += 1
            ib += 1
        elif cell_a < cell_b:
            total += count_a * count_a
            ia += 1
        else:
            total += count_b * count_b
            ib += 1
    while ia < len(a):
        _, count_a = a[ia]
        total += count_a * count_a
        ia += 1
    while ib < len(b):
        _, count_b = b[ib]
        total += count_b * count_b
        ib += 1
    return total


def _cell_weight(
    cell_idx: int,
    family_ranges: dict[str, tuple[int, int]],
    family_weights: dict[str, float],
) -> float:
    for family, (start_idx, width) in family_ranges.items():
        if start_idx <= cell_idx < start_idx + width:
            return family_weights.get(family, 1.0)
    return 1.0


def weighted_sparse_l2_distance_sq(
    a: RecordState,
    b: RecordState,
    family_ranges: dict[str, tuple[int, int]],
    family_weights: dict[str, float],
) -> float:
    ia = 0
    ib = 0
    total = 0.0
    while ia < len(a) and ib < len(b):
        cell_a, count_a = a[ia]
        cell_b, count_b = b[ib]
        if cell_a == cell_b:
            diff = count_a - count_b
            total += _cell_weight(cell_a, family_ranges, family_weights) * diff * diff
            ia += 1
            ib += 1
        elif cell_a < cell_b:
            total += _cell_weight(cell_a, family_ranges, family_weights) * count_a * count_a
            ia += 1
        else:
            total += _cell_weight(cell_b, family_ranges, family_weights) * count_b * count_b
            ib += 1
    while ia < len(a):
        cell_a, count_a = a[ia]
        total += _cell_weight(cell_a, family_ranges, family_weights) * count_a * count_a
        ia += 1
    while ib < len(b):
        cell_b, count_b = b[ib]
        total += _cell_weight(cell_b, family_ranges, family_weights) * count_b * count_b
        ib += 1
    return total


def generalized_detector_metrics(
    det_state: dict[tuple[int, RecordState], complex],
    det_nodes: list[int],
    gamma: float,
    family_ranges: dict[str, tuple[int, int]] | None = None,
    family_weights: dict[str, float] | None = None,
) -> tuple[float, float, float, float, int]:
    """Compute detector-conditioned metrics with a soft record-overlap kernel."""
    grouped: dict[RecordState, dict[int, complex]] = defaultdict(dict)
    for (det_node, record), amp in det_state.items():
        grouped[record][det_node] = amp
    records = list(grouped.keys())

    kernel_cache: dict[tuple[int, int], float] = {}

    def kernel(i: int, j: int) -> float:
        key = (i, j) if i <= j else (j, i)
        if key in kernel_cache:
            return kernel_cache[key]
        if gamma <= 0:
            value = 1.0
        else:
            if family_ranges is not None and family_weights is not None:
                dist_sq = weighted_sparse_l2_distance_sq(
                    records[i],
                    records[j],
                    family_ranges,
                    family_weights,
                )
            else:
                dist_sq = sparse_l2_distance_sq(records[i], records[j])
            value = math.exp(-gamma * dist_sq)
        kernel_cache[key] = value
        return value

    rho: dict[tuple[int, int], complex] = {}
    mean_overlap_num = 0.0
    mean_overlap_den = 0.0
    for d1 in det_nodes:
        for d2 in det_nodes:
            val = 0.0 + 0.0j
            for i, rec_i in enumerate(records):
                a1 = grouped[rec_i].get(d1, 0.0 + 0.0j)
                if abs(a1) < 1e-30:
                    continue
                for j, rec_j in enumerate(records):
                    a2 = grouped[rec_j].get(d2, 0.0 + 0.0j)
                    if abs(a2) < 1e-30:
                        continue
                    kij = kernel(i, j)
                    val += a1.conjugate() * a2 * kij
                    if d1 == d2:
                        weight = abs(a1) * abs(a2)
                        mean_overlap_num += weight * kij
                        mean_overlap_den += weight
            rho[(d1, d2)] = val

    trace = sum(rho.get((d, d), 0.0) for d in det_nodes).real
    if trace <= 1e-30:
        return math.nan, math.nan, math.nan, 0.0, len(records)

    for key in rho:
        rho[key] /= trace

    purity = sum(abs(v) ** 2 for v in rho.values()).real
    diag_total = sum(abs(rho.get((d, d), 0.0)) ** 2 for d in det_nodes).real
    offdiag_total = purity - diag_total
    mean_overlap = mean_overlap_num / mean_overlap_den if mean_overlap_den > 0 else math.nan
    return purity, diag_total, offdiag_total, mean_overlap, len(records)


def fit_power_law(ns: list[int], purities: list[float]) -> tuple[float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    for n, purity in zip(ns, purities):
        decoh = 1.0 - purity
        if decoh <= 1e-12:
            continue
        xs.append(math.log(float(n)))
        ys.append(math.log(decoh))
    if len(xs) < 2:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    var_x = sum((x - mx) ** 2 for x in xs)
    if var_x <= 1e-30:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    alpha = cov / var_x
    intercept = my - alpha * mx
    return alpha, math.exp(intercept)


def summarize_fit(label: str, ns: list[int], purities: list[float]) -> str:
    fit = fit_power_law(ns, purities)
    if fit is None:
        return f"  {label}: insufficient nonzero decoherence for fit"
    alpha, prefactor = fit
    return f"  {label}: (1-pur) ~ {prefactor:.3g} * N^{alpha:+.3f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", default="8,12,18")
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--nodes-per-layer", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--radius", type=float, default=3.0)
    parser.add_argument("--k-band", default="3.0,5.0,7.0")
    parser.add_argument("--gamma", default="0.25,1.0")
    parser.add_argument("--y-bins", type=int, default=5)
    parser.add_argument("--max-count", type=int, default=2)
    parser.add_argument("--mass-y-half", type=float, default=3.0)
    parser.add_argument(
        "--side-bit",
        action="store_true",
        help="Add one persistent packet-side marker bit to the record state.",
    )
    parser.add_argument(
        "--packet-bit",
        action="store_true",
        help="Add one persistent core/flank packet-placement bit to the record state.",
    )
    parser.add_argument(
        "--entry-bit",
        action="store_true",
        help="Add one persistent early/late first-contact timing bit to the record state.",
    )
    parser.add_argument(
        "--active-write",
        action="store_true",
        help="Let remembered side/packet markers redirect later record writes via violation markers.",
    )
    parser.add_argument(
        "--marker-weight",
        type=float,
        default=1.0,
        help="Relative kernel weight for marker-family mismatches versus worldtube counts.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    n_layers_values = parse_int_list(args.n_layers)
    k_band = parse_float_list(args.k_band)
    gammas = parse_float_list(args.gamma)

    print("=" * 78)
    print("PERSISTENT RECORD OVERLAP KERNEL")
    print("  Record state: mesoscopic counts over post-barrier worldtube cells")
    print("  Kernel: K(r,r') = exp(-gamma * ||r-r'||^2)")
    print(f"  Propagator: 1/L^p * exp(-{BETA} * theta^2) * exp(i k S_spent)")
    print(f"  N sweep: {n_layers_values}  seeds={args.seeds}  k_band={k_band}")
    print(
        f"  Record grid: y_bins={args.y_bins}, dir_bins={DIR_BINS}, "
        f"max_count={args.max_count}"
    )
    print(f"  side_bit: {args.side_bit}")
    print(f"  packet_bit: {args.packet_bit}")
    print(f"  entry_bit: {args.entry_bit}")
    print(f"  active_write: {args.active_write}")
    print(f"  marker_weight: {args.marker_weight}")
    print(f"  gamma sweep: {gammas}")
    print("=" * 78, flush=True)
    print(flush=True)

    gamma_results: dict[float, list[float]] = {gamma: [] for gamma in gammas}
    trace_results: list[float] = []
    mean_overlap_results: dict[float, list[float]] = {gamma: [] for gamma in gammas}
    successful_ns: list[int] = []

    header = ["N", "pur_trace", "n_env"]
    header.extend(f"pur_g{gamma:g}" for gamma in gammas)
    header.extend(f"ov_g{gamma:g}" for gamma in gammas)
    print("  " + "  ".join(f"{label:>10s}" for label in header), flush=True)
    print("  " + "-" * (12 * len(header)), flush=True)

    for nl in n_layers_values:
        trace_vals: list[float] = []
        env_counts: list[int] = []
        gamma_vals: dict[float, list[float]] = {gamma: [] for gamma in gammas}
        gamma_ovs: dict[float, list[float]] = {gamma: [] for gamma in gammas}

        for seed in range(args.seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl,
                nodes_per_layer=args.nodes_per_layer,
                y_range=args.y_range,
                connect_radius=args.radius,
                rng_seed=seed * 11 + 7,
            )
            setup = build_post_barrier_setup(
                positions,
                adj,
                env_depth_layers=max(1, round(nl / 6)),
                mass_y_half=args.mass_y_half,
            )
            if setup is None:
                continue

            family_ranges = record_family_ranges(
                setup,
                args.y_bins,
                include_side_bit=args.side_bit,
                include_packet_bit=args.packet_bit,
                include_entry_bit=args.entry_bit,
                include_violation_bits=args.active_write,
            )
            family_weights = {
                "count": 1.0,
                "side": args.marker_weight,
                "packet": args.marker_weight,
                "entry": args.marker_weight,
                "violation": args.marker_weight,
            }

            for k in k_band:
                det_state = propagate_persistent_records(
                    positions,
                    adj,
                    setup["field"],
                    setup,
                    k,
                    y_bins=args.y_bins,
                    max_count=args.max_count,
                    mass_y_half=args.mass_y_half,
                    include_side_bit=args.side_bit,
                    include_packet_bit=args.packet_bit,
                    include_entry_bit=args.entry_bit,
                    active_write=args.active_write,
                )

                pur_trace, _, _, _ = compute_detector_metrics(det_state, setup["det_list"])
                if not math.isnan(pur_trace):
                    trace_vals.append(pur_trace)

                for gamma in gammas:
                    pur, _, _, mean_ov, n_env = generalized_detector_metrics(
                        det_state,
                        setup["det_list"],
                        gamma,
                        family_ranges=family_ranges if args.marker_weight != 1.0 else None,
                        family_weights=family_weights if args.marker_weight != 1.0 else None,
                    )
                    if not math.isnan(pur):
                        gamma_vals[gamma].append(pur)
                        gamma_ovs[gamma].append(mean_ov)
                        env_counts.append(n_env)

        if not trace_vals:
            continue

        mean_trace = sum(trace_vals) / len(trace_vals)
        trace_results.append(mean_trace)
        successful_ns.append(nl)
        row = [f"{nl:10d}", f"{mean_trace:10.4f}", f"{(sum(env_counts)/len(env_counts)) if env_counts else math.nan:10.1f}"]
        for gamma in gammas:
            mean_pur = sum(gamma_vals[gamma]) / len(gamma_vals[gamma])
            gamma_results[gamma].append(mean_pur)
            mean_ov = sum(gamma_ovs[gamma]) / len(gamma_ovs[gamma])
            mean_overlap_results[gamma].append(mean_ov)
            row.append(f"{mean_pur:10.4f}")
        for gamma in gammas:
            row.append(f"{(sum(gamma_ovs[gamma]) / len(gamma_ovs[gamma])):10.4f}")
        print("  " + "  ".join(row), flush=True)

    print(flush=True)
    print("Fit summary", flush=True)
    print(summarize_fit("trace", successful_ns, trace_results), flush=True)
    for gamma in gammas:
        print(
            summarize_fit(
                f"gamma={gamma:g}",
                successful_ns[: len(gamma_results[gamma])],
                gamma_results[gamma],
            ),
            flush=True,
        )

    print(flush=True)
    print("Interpretation:", flush=True)
    print("  pur_trace = exact trace over orthogonal record sectors for this record model", flush=True)
    print("  pur_gX = soft-overlap reduced purity with residual branch connection", flush=True)
    print("  ov_gX = detector-weighted mean branch overlap under that kernel", flush=True)
    print("  Lower purity and flatter/positive scaling of (1-pur) are the interesting signs", flush=True)


if __name__ == "__main__":
    main()
