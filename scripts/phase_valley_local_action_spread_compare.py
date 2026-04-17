#!/usr/bin/env python3
"""Compare packet-local action spread terms against the retained gravity kick.

This is a bounded follow-on to the near-mass action-gap checkpoint. It keeps
the corrected propagator, impact-parameter family, and Δky readout fixed, and
only tightens the denominator used in the toy action-saturation ratio.

On the same retained valley probes, compare:
- raw action-deficit gap
- pooled valley action Q from the existing node-level spread
- packet-local action Q using small windows around each valley's amplitude peak
- dominant-packet action Q using only the locally dominant valley packet spread
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.momentum_space_gravity import (  # noqa: E402
    fourier_transform_y,
    prob_centroid_ky,
)
from scripts.phase_valley_action_saturation_compare import (  # noqa: E402
    PROBE_CONFIGS,
    FitSummary,
    _aggregate_action_valley,
    _fit_tanh,
    _propagate_action_moments,
    _propagate_amplitudes,
    _split_cut,
)
from toy_event_physics import (  # noqa: E402
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
)


@dataclass(frozen=True)
class PacketWindow:
    peak_y: int | None
    weight_share: float
    mean: float
    sigma: float


@dataclass(frozen=True)
class ProbeMetrics:
    probe_name: str
    impact_b: int
    delta_ky: float
    valley_balance: float
    action_gap: float
    action_q: float
    local_action_q: float
    dominant_action_q: float
    dominant_side: str
    upper_peak_y: int | None
    lower_peak_y: int | None
    upper_local_share: float
    lower_local_share: float


def _packet_window_stats(
    ys: list[int],
    weights: list[float],
    means: list[float],
    sigmas: list[float],
    half_window: int,
) -> PacketWindow:
    if not weights:
        return PacketWindow(peak_y=None, weight_share=0.0, mean=0.0, sigma=float("inf"))

    peak_index = max(range(len(weights)), key=lambda index: weights[index])
    peak_y = ys[peak_index]

    # Keep the denominator tied to the packet that actually carries the valley,
    # rather than pooling the full node-level spread across the whole side.
    kept_indices = [
        index
        for index, y in enumerate(ys)
        if abs(y - peak_y) <= half_window
    ]
    local_weights = [weights[index] for index in kept_indices]
    local_means = [means[index] for index in kept_indices]
    local_sigmas = [sigmas[index] for index in kept_indices]
    local_mean, local_sigma = _aggregate_action_valley(
        local_weights,
        local_means,
        local_sigmas,
    )
    total_weight = sum(weights)
    weight_share = sum(local_weights) / total_weight if total_weight > 1e-12 else 0.0
    return PacketWindow(
        peak_y=peak_y,
        weight_share=weight_share,
        mean=local_mean,
        sigma=local_sigma,
    )


def _measure_probe(
    probe_name: str,
    impact_b: int,
    delta_ky: float,
    probe_x: int,
    cut_mode: str,
    height: int,
    packet_half_window: int,
    amps: dict[tuple[int, int], complex],
    mass_action_mean: dict[tuple[int, int], float],
    mass_action_sigma: dict[tuple[int, int], float],
    free_action_mean: dict[tuple[int, int], float],
    free_action_sigma: dict[tuple[int, int], float],
) -> ProbeMetrics:
    cut = _split_cut(impact_b, cut_mode)
    screen_ys = list(range(-height, height + 1))

    upper_ys: list[int] = []
    upper_action_weights: list[float] = []
    upper_action_means: list[float] = []
    upper_action_sigmas: list[float] = []

    lower_ys: list[int] = []
    lower_action_weights: list[float] = []
    lower_action_means: list[float] = []
    lower_action_sigmas: list[float] = []

    for y in screen_ys:
        node = (probe_x, y)
        amp = amps.get(node, 0.0 + 0.0j)
        weight = abs(amp) ** 2
        if weight <= 1e-20:
            continue

        action_mean = mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0)
        action_sigma = math.sqrt(
            mass_action_sigma.get(node, 0.0) ** 2 + free_action_sigma.get(node, 0.0) ** 2
        )

        if y >= cut:
            upper_ys.append(y)
            upper_action_weights.append(weight)
            upper_action_means.append(action_mean)
            upper_action_sigmas.append(action_sigma)
        else:
            lower_ys.append(y)
            lower_action_weights.append(weight)
            lower_action_means.append(action_mean)
            lower_action_sigmas.append(action_sigma)

    upper_weight = sum(upper_action_weights)
    lower_weight = sum(lower_action_weights)
    valley_balance = min(upper_weight, lower_weight) / max(upper_weight, lower_weight, 1e-12)

    upper_action_mean, upper_action_sigma = _aggregate_action_valley(
        upper_action_weights,
        upper_action_means,
        upper_action_sigmas,
    )
    lower_action_mean, lower_action_sigma = _aggregate_action_valley(
        lower_action_weights,
        lower_action_means,
        lower_action_sigmas,
    )
    action_gap = abs(upper_action_mean - lower_action_mean)
    pooled_action_sigma = math.sqrt(upper_action_sigma ** 2 + lower_action_sigma ** 2)
    action_q = action_gap / pooled_action_sigma if math.isfinite(pooled_action_sigma) and pooled_action_sigma > 1e-12 else 0.0

    upper_packet = _packet_window_stats(
        upper_ys,
        upper_action_weights,
        upper_action_means,
        upper_action_sigmas,
        packet_half_window,
    )
    lower_packet = _packet_window_stats(
        lower_ys,
        lower_action_weights,
        lower_action_means,
        lower_action_sigmas,
        packet_half_window,
    )

    local_pooled_sigma = math.sqrt(upper_packet.sigma ** 2 + lower_packet.sigma ** 2)
    local_action_q = action_gap / local_pooled_sigma if math.isfinite(local_pooled_sigma) and local_pooled_sigma > 1e-12 else 0.0

    dominant_is_upper = upper_weight >= lower_weight
    dominant_packet_sigma = upper_packet.sigma if dominant_is_upper else lower_packet.sigma
    dominant_action_q = (
        action_gap / dominant_packet_sigma
        if math.isfinite(dominant_packet_sigma) and dominant_packet_sigma > 1e-12
        else 0.0
    )

    return ProbeMetrics(
        probe_name=probe_name,
        impact_b=impact_b,
        delta_ky=delta_ky,
        valley_balance=valley_balance,
        action_gap=action_gap,
        action_q=action_q,
        local_action_q=local_action_q,
        dominant_action_q=dominant_action_q,
        dominant_side="upper" if dominant_is_upper else "lower",
        upper_peak_y=upper_packet.peak_y,
        lower_peak_y=lower_packet.peak_y,
        upper_local_share=upper_packet.weight_share,
        lower_local_share=lower_packet.weight_share,
    )


def _evaluate_b(task: tuple[int, int, int, float, float, int]) -> list[ProbeMetrics]:
    impact_b, width, height, phase_k, atten_power, packet_half_window = task
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))

    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    vacuum_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival = infer_arrival_times_from_source(nodes, source, vacuum_rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    free_field = {node: 0.0 for node in nodes}
    mass_nodes = frozenset((30, y) for y in range(impact_b - 1, impact_b + 2))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    free_amps = _propagate_amplitudes(order, dag, source, free_field, phase_k, atten_power)
    mass_amps = _propagate_amplitudes(order, dag, source, mass_field, phase_k, atten_power)
    free_action_mean, free_action_sigma = _propagate_action_moments(order, dag, source, free_field, atten_power)
    mass_action_mean, mass_action_sigma = _propagate_action_moments(order, dag, source, mass_field, atten_power)

    ft_free = fourier_transform_y(free_amps, 45, screen_ys)
    ft_mass = fourier_transform_y(mass_amps, 45, screen_ys)
    delta_ky = prob_centroid_ky(ft_mass, len(screen_ys)) - prob_centroid_ky(ft_free, len(screen_ys))

    return [
        _measure_probe(
            probe_name=probe.name,
            impact_b=impact_b,
            delta_ky=delta_ky,
            probe_x=probe.probe_x,
            cut_mode=probe.cut_mode,
            height=height,
            packet_half_window=packet_half_window,
            amps=mass_amps,
            mass_action_mean=mass_action_mean,
            mass_action_sigma=mass_action_sigma,
            free_action_mean=free_action_mean,
            free_action_sigma=free_action_sigma,
        )
        for probe in PROBE_CONFIGS
    ]


def run_rows(
    impact_bs: Iterable[int],
    workers: int,
    width: int,
    height: int,
    phase_k: float,
    atten_power: float,
    packet_half_window: int,
) -> list[list[ProbeMetrics]]:
    tasks = [
        (impact_b, width, height, phase_k, atten_power, packet_half_window)
        for impact_b in impact_bs
    ]
    if workers <= 1:
        return [_evaluate_b(task) for task in tasks]
    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return list(pool.map(_evaluate_b, tasks))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--width", type=int, default=60)
    parser.add_argument("--height", type=int, default=25)
    parser.add_argument("--phase-k", type=float, default=2.0)
    parser.add_argument("--atten-power", type=float, default=1.0)
    parser.add_argument("--packet-half-window", type=int, default=2)
    args = parser.parse_args()

    impact_bs = [2, 4, 6, 8, 10, 12, 15, 18, 20]
    result_rows = run_rows(
        impact_bs=impact_bs,
        workers=max(1, args.workers),
        width=args.width,
        height=args.height,
        phase_k=args.phase_k,
        atten_power=args.atten_power,
        packet_half_window=max(0, args.packet_half_window),
    )

    rows_by_probe = {probe.name: [] for probe in PROBE_CONFIGS}
    for probe_rows in result_rows:
        for row in probe_rows:
            rows_by_probe[row.probe_name].append(row)
    for rows in rows_by_probe.values():
        rows.sort(key=lambda row: row.impact_b)

    ranked_fits: list[tuple[str, FitSummary]] = []
    for probe in PROBE_CONFIGS:
        rows = rows_by_probe[probe.name]
        ys = [row.delta_ky for row in rows]
        fits = [
            _fit_tanh("action_gap", [row.action_gap for row in rows], ys),
            _fit_tanh("action_q", [row.action_q for row in rows], ys),
            _fit_tanh("local_action_q", [row.local_action_q for row in rows], ys),
            _fit_tanh("dominant_action_q", [row.dominant_action_q for row in rows], ys),
        ]
        fits.sort(key=lambda fit: (fit.r2, -fit.mae), reverse=True)
        ranked_fits.extend((probe.name, fit) for fit in fits)

        print("=" * 104)
        print(
            f"Probe: {probe.name} ({probe.description}) | packet half-window = {max(0, args.packet_half_window)}"
        )
        print("=" * 104)
        print(
            f"{'b':>4s} {'Δky':>10s} {'action_gap':>11s} {'action_q':>10s} "
            f"{'local_q':>10s} {'dom_q':>10s} {'dom':>6s} {'up_pk':>6s} {'lo_pk':>6s}"
        )
        print("-" * 94)
        for row in rows:
            upper_peak = "--" if row.upper_peak_y is None else f"{row.upper_peak_y:d}"
            lower_peak = "--" if row.lower_peak_y is None else f"{row.lower_peak_y:d}"
            print(
                f"{row.impact_b:4d} {row.delta_ky:+10.4f} {row.action_gap:11.4f} {row.action_q:10.4f} "
                f"{row.local_action_q:10.4f} {row.dominant_action_q:10.4f} {row.dominant_side:>6s} "
                f"{upper_peak:>6s} {lower_peak:>6s}"
            )
        print()
        print("Best tanh fits:")
        for fit in fits:
            print(f"  {fit.render()}")
        print("Packet-local support shares:")
        for row in rows:
            print(
                f"  b={row.impact_b:2d}: upper={row.upper_local_share:.4f}, "
                f"lower={row.lower_local_share:.4f}"
            )
        print()

    ranked_fits.sort(key=lambda item: (item[1].r2, -item[1].mae), reverse=True)
    print("=" * 104)
    print("OVERALL FIT RANKING")
    print("=" * 104)
    for probe_name, fit in ranked_fits[:10]:
        print(f"  {probe_name}: {fit.render()}")
    print()

    best_probe, best_fit = ranked_fits[0]
    print("Interpretation:")
    if best_fit.feature == "dominant_action_q":
        print(
            "  The dominant-packet local denominator is the strongest bounded action "
            f"proxy on {best_probe}; the normalization step improves once it follows the main packet."
        )
    elif best_fit.feature == "local_action_q":
        print(
            "  Packet-local valley spreads outperform the pooled node-level denominator "
            f"on {best_probe}; the normalization step benefits from staying near the packet peaks."
        )
    elif best_fit.feature == "action_q":
        print(
            f"  The original pooled action Q still wins on {best_probe}; the local packet window does not help."
        )
    else:
        print(
            f"  Raw action gap still beats every normalized action ratio on {best_probe}; the tighter spread term is not enough yet."
        )
    print(
        "  This compare changes only the action-spread denominator, so any movement comes from how local packet support is summarized."
    )


if __name__ == "__main__":
    main()
