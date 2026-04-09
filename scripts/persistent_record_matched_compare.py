#!/usr/bin/env python3
"""Matched comparison for persistent-record kernel vs earlier record lanes.

This script compares several detector-reduction architectures on the same
generated DAGs, same seeds, same `k` band, and same post-barrier setup:

- node label
- graph-memory scars
- entangling environment
- persistent records with exact trace
- persistent records with soft overlap kernel
- persistent records plus one extra packet-side bit
- persistent records plus side bit and coarse packet-placement bit
- persistent records plus side bit, packet-placement bit, and early/late entry bit

The goal is not to prove asymptotic closure. It is to answer the narrower
question: on the same bounded slice, does the persistent-record overlap idea
actually improve over the earlier record architectures?
"""

from __future__ import annotations

import argparse
import cmath
import math
import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics
from scripts.entangling_env_decoherence import ALPHA, propagate_entangling
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.graph_memory_scar_decoherence import propagate_with_scars
from scripts.persistent_record_overlap_kernel import (
    generalized_detector_metrics,
    parse_float_list,
    parse_int_list,
    propagate_persistent_records,
    record_family_ranges,
)

BETA = 0.8


def propagate_node_label_directional(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    setup: dict[str, object],
    k: float,
    mass_set: set[int],
) -> dict[tuple[int, int], complex]:
    """Directional-measure node-label environment, matched to current unitary core."""
    n = len(positions)
    blocked = setup["blocked"]
    src = setup["src"]
    det = setup["det"]

    in_deg = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    state: dict[tuple[int, int], complex] = {}
    for s in src:
        state[(s, -1)] = 1.0 / len(src) + 0.0j

    processed: set[int] = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {
            env: amp
            for (node, env), amp in list(state.items())
            if node == i and abs(amp) > 1e-30
        }
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
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                edge_amp = cmath.exp(1j * k * act) * math.exp(-BETA * theta * theta) / L
                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0 + 0.0j
                state[key] += amp * edge_amp

    return {(d, env): amp for (d, env), amp in state.items() if d in det}


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


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
    mx = mean(xs)
    my = mean(ys)
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
    alpha, pref = fit
    return f"  {label}: (1-pur) ~ {pref:.3g} * N^{alpha:+.3f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", default="8,12,18")
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--nodes-per-layer", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--radius", type=float, default=3.0)
    parser.add_argument("--k-band", default="3.0,5.0,7.0")
    parser.add_argument("--gamma", default="0.25,1.0")
    parser.add_argument(
        "--methods",
        default="node,scar,ent,pr_trace,pr_soft",
        help="comma-separated subset of node,scar,ent,pr_trace,pr_soft,pr_side_trace,pr_side_soft,pr_side_packet_trace,pr_side_packet_soft,pr_side_packet_entry_trace,pr_side_packet_entry_soft,pr_side_packet_entry_aniso_soft,pr_side_packet_entry_active_soft",
    )
    parser.add_argument(
        "--marker-weight",
        type=float,
        default=3.0,
        help="Marker-family kernel weight for anisotropic soft-overlap variants.",
    )
    parser.add_argument("--y-bins", type=int, default=5)
    parser.add_argument("--max-count", type=int, default=2)
    parser.add_argument("--scar-size", type=int, default=6)
    parser.add_argument("--mass-y-half", type=float, default=3.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    n_layers_values = parse_int_list(args.n_layers)
    k_band = parse_float_list(args.k_band)
    gammas = parse_float_list(args.gamma)
    selected = {part.strip() for part in args.methods.split(",") if part.strip()}

    methods: list[str] = []
    if "node" in selected:
        methods.append("node")
    if "scar" in selected:
        methods.append("scar")
    if "ent" in selected:
        methods.append("ent")
    if "pr_trace" in selected:
        methods.append("pr_trace")
    if "pr_soft" in selected:
        methods.extend(f"pr_g{gamma:g}" for gamma in gammas)
    if "pr_side_trace" in selected:
        methods.append("pr_side_trace")
    if "pr_side_soft" in selected:
        methods.extend(f"pr_side_g{gamma:g}" for gamma in gammas)
    if "pr_side_packet_trace" in selected:
        methods.append("pr_side_packet_trace")
    if "pr_side_packet_soft" in selected:
        methods.extend(f"pr_side_packet_g{gamma:g}" for gamma in gammas)
    if "pr_side_packet_entry_trace" in selected:
        methods.append("pr_side_packet_entry_trace")
    if "pr_side_packet_entry_soft" in selected:
        methods.extend(f"pr_side_packet_entry_g{gamma:g}" for gamma in gammas)
    if "pr_side_packet_entry_aniso_soft" in selected:
        methods.extend(f"pr_side_packet_entry_aniso_g{gamma:g}" for gamma in gammas)
    if "pr_side_packet_entry_active_soft" in selected:
        methods.extend(f"pr_side_packet_entry_active_g{gamma:g}" for gamma in gammas)

    if not methods:
        raise SystemExit("no methods selected")

    method_results: dict[str, list[float]] = {method: [] for method in methods}
    method_envs: dict[str, list[float]] = {method: [] for method in methods}

    print("=" * 86)
    print("PERSISTENT RECORD MATCHED COMPARISON")
    print("  Same generated DAGs, same seeds, same barrier setup, same k band")
    print(f"  N sweep: {n_layers_values}  seeds={args.seeds}  k_band={k_band}")
    print(f"  Persistent kernel gammas: {gammas}")
    print("=" * 86)
    print()

    header = ["N"] + methods
    print("  " + "  ".join(f"{label:>10s}" for label in header), flush=True)
    print("  " + "-" * (12 * len(header)), flush=True)

    for nl in n_layers_values:
        per_method: dict[str, list[float]] = {method: [] for method in methods}
        per_env: dict[str, list[float]] = {method: [] for method in methods}

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

            mass_set = set(setup["mass_set"]) - set(setup["blocked"])

            for k in k_band:
                if "node" in selected:
                    ds_node = propagate_node_label_directional(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        mass_set,
                    )
                    pur_node, _, _, _ = compute_detector_metrics(ds_node, setup["det_list"])
                    if not math.isnan(pur_node):
                        per_method["node"].append(pur_node)
                        per_env["node"].append(float(len({env for (_, env) in ds_node.keys()})))

                if "scar" in selected:
                    ds_scar = propagate_with_scars(
                        positions,
                        adj,
                        setup["field"],
                        setup["src"],
                        setup["det"],
                        k,
                        mass_set,
                        setup["blocked"],
                        max_scar_size=args.scar_size,
                    )
                    pur_scar, _, _, _ = compute_detector_metrics(ds_scar, setup["det_list"])
                    if not math.isnan(pur_scar):
                        per_method["scar"].append(pur_scar)
                        per_env["scar"].append(float(len({env for (_, env) in ds_scar.keys()})))

                if "ent" in selected:
                    ds_ent = propagate_entangling(
                        positions,
                        adj,
                        setup["field"],
                        setup["src"],
                        setup["det"],
                        k,
                        mass_set,
                        ALPHA,
                        setup["blocked"],
                    )
                    pur_ent, _, _, _ = compute_detector_metrics(ds_ent, setup["det_list"])
                    if not math.isnan(pur_ent):
                        per_method["ent"].append(pur_ent)
                        per_env["ent"].append(float(len({env for (_, env) in ds_ent.keys()})))

                ds_pr = None
                if "pr_trace" in selected or "pr_soft" in selected:
                    ds_pr = propagate_persistent_records(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        y_bins=args.y_bins,
                        max_count=args.max_count,
                        mass_y_half=args.mass_y_half,
                    )

                if "pr_trace" in selected and ds_pr is not None:
                    pur_trace, _, _, _ = compute_detector_metrics(ds_pr, setup["det_list"])
                    if not math.isnan(pur_trace):
                        per_method["pr_trace"].append(pur_trace)
                        per_env["pr_trace"].append(float(len({env for (_, env) in ds_pr.keys()})))

                if "pr_soft" in selected and ds_pr is not None:
                    for gamma in gammas:
                        pur_soft, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr,
                            setup["det_list"],
                            gamma,
                        )
                        label = f"pr_g{gamma:g}"
                        if not math.isnan(pur_soft):
                            per_method[label].append(pur_soft)
                            per_env[label].append(float(n_env))

                ds_pr_side = None
                if "pr_side_trace" in selected or "pr_side_soft" in selected:
                    ds_pr_side = propagate_persistent_records(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        y_bins=args.y_bins,
                        max_count=args.max_count,
                        mass_y_half=args.mass_y_half,
                        include_side_bit=True,
                    )

                if "pr_side_trace" in selected and ds_pr_side is not None:
                    pur_side_trace, _, _, _ = compute_detector_metrics(
                        ds_pr_side,
                        setup["det_list"],
                    )
                    if not math.isnan(pur_side_trace):
                        per_method["pr_side_trace"].append(pur_side_trace)
                        per_env["pr_side_trace"].append(
                            float(len({env for (_, env) in ds_pr_side.keys()}))
                        )

                if "pr_side_soft" in selected and ds_pr_side is not None:
                    for gamma in gammas:
                        pur_side_soft, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr_side,
                            setup["det_list"],
                            gamma,
                        )
                        label = f"pr_side_g{gamma:g}"
                        if not math.isnan(pur_side_soft):
                            per_method[label].append(pur_side_soft)
                            per_env[label].append(float(n_env))

                ds_pr_side_packet = None
                if "pr_side_packet_trace" in selected or "pr_side_packet_soft" in selected:
                    ds_pr_side_packet = propagate_persistent_records(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        y_bins=args.y_bins,
                        max_count=args.max_count,
                        mass_y_half=args.mass_y_half,
                        include_side_bit=True,
                        include_packet_bit=True,
                    )

                if "pr_side_packet_trace" in selected and ds_pr_side_packet is not None:
                    pur_side_packet_trace, _, _, _ = compute_detector_metrics(
                        ds_pr_side_packet,
                        setup["det_list"],
                    )
                    if not math.isnan(pur_side_packet_trace):
                        per_method["pr_side_packet_trace"].append(pur_side_packet_trace)
                        per_env["pr_side_packet_trace"].append(
                            float(len({env for (_, env) in ds_pr_side_packet.keys()}))
                        )

                if "pr_side_packet_soft" in selected and ds_pr_side_packet is not None:
                    for gamma in gammas:
                        pur_side_packet_soft, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr_side_packet,
                            setup["det_list"],
                            gamma,
                        )
                        label = f"pr_side_packet_g{gamma:g}"
                        if not math.isnan(pur_side_packet_soft):
                            per_method[label].append(pur_side_packet_soft)
                            per_env[label].append(float(n_env))

                ds_pr_side_packet_entry = None
                if "pr_side_packet_entry_trace" in selected or "pr_side_packet_entry_soft" in selected:
                    ds_pr_side_packet_entry = propagate_persistent_records(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        y_bins=args.y_bins,
                        max_count=args.max_count,
                        mass_y_half=args.mass_y_half,
                        include_side_bit=True,
                        include_packet_bit=True,
                        include_entry_bit=True,
                    )

                if "pr_side_packet_entry_trace" in selected and ds_pr_side_packet_entry is not None:
                    pur_side_packet_entry_trace, _, _, _ = compute_detector_metrics(
                        ds_pr_side_packet_entry,
                        setup["det_list"],
                    )
                    if not math.isnan(pur_side_packet_entry_trace):
                        per_method["pr_side_packet_entry_trace"].append(
                            pur_side_packet_entry_trace
                        )
                        per_env["pr_side_packet_entry_trace"].append(
                            float(len({env for (_, env) in ds_pr_side_packet_entry.keys()}))
                        )

                if "pr_side_packet_entry_soft" in selected and ds_pr_side_packet_entry is not None:
                    for gamma in gammas:
                        pur_side_packet_entry_soft, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr_side_packet_entry,
                            setup["det_list"],
                            gamma,
                        )
                        label = f"pr_side_packet_entry_g{gamma:g}"
                        if not math.isnan(pur_side_packet_entry_soft):
                            per_method[label].append(pur_side_packet_entry_soft)
                            per_env[label].append(float(n_env))

                if "pr_side_packet_entry_aniso_soft" in selected and ds_pr_side_packet_entry is not None:
                    aniso_ranges = record_family_ranges(
                        setup,
                        args.y_bins,
                        include_side_bit=True,
                        include_packet_bit=True,
                        include_entry_bit=True,
                        include_violation_bits=False,
                    )
                    aniso_weights = {
                        "count": 1.0,
                        "side": args.marker_weight,
                        "packet": args.marker_weight,
                        "entry": args.marker_weight,
                    }
                    for gamma in gammas:
                        pur_aniso, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr_side_packet_entry,
                            setup["det_list"],
                            gamma,
                            family_ranges=aniso_ranges,
                            family_weights=aniso_weights,
                        )
                        label = f"pr_side_packet_entry_aniso_g{gamma:g}"
                        if not math.isnan(pur_aniso):
                            per_method[label].append(pur_aniso)
                            per_env[label].append(float(n_env))

                ds_pr_side_packet_entry_active = None
                if "pr_side_packet_entry_active_soft" in selected:
                    ds_pr_side_packet_entry_active = propagate_persistent_records(
                        positions,
                        adj,
                        setup["field"],
                        setup,
                        k,
                        y_bins=args.y_bins,
                        max_count=args.max_count,
                        mass_y_half=args.mass_y_half,
                        include_side_bit=True,
                        include_packet_bit=True,
                        include_entry_bit=True,
                        active_write=True,
                    )

                if "pr_side_packet_entry_active_soft" in selected and ds_pr_side_packet_entry_active is not None:
                    for gamma in gammas:
                        pur_active, _, _, _, n_env = generalized_detector_metrics(
                            ds_pr_side_packet_entry_active,
                            setup["det_list"],
                            gamma,
                        )
                        label = f"pr_side_packet_entry_active_g{gamma:g}"
                        if not math.isnan(pur_active):
                            per_method[label].append(pur_active)
                            per_env[label].append(float(n_env))

        row = [f"{nl:10d}"]
        for method in methods:
            method_mean = mean(per_method[method])
            row.append(f"{method_mean:10.4f}")
            if not math.isnan(method_mean):
                method_results[method].append(method_mean)
                method_envs[method].append(mean(per_env[method]))
        print("  " + "  ".join(row), flush=True)

    print()
    print("Environment counts (mean distinct detector env sectors)")
    for method in methods:
        if method_envs[method]:
            env_summary = ", ".join(f"{n}:{env:.1f}" for n, env in zip(n_layers_values, method_envs[method]))
            print(f"  {method}: {env_summary}")

    print()
    print("Fit summary")
    for method in methods:
        if method_results[method]:
            print(summarize_fit(method, n_layers_values[: len(method_results[method])], method_results[method]))


if __name__ == "__main__":
    main()
