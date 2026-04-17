#!/usr/bin/env python3
"""Compare phase-valley and action-valley saturation diagnostics against Δky.

This is a bounded follow-on to the retained phase-valley checkpoint. It keeps
the corrected propagator and downstream momentum readout fixed, but replaces
node phase with a truer local action statistic:

  cumulative action deficit = cumulative mass-field action - cumulative free action

For each retained valley probe, the script compares:
- raw phase gap
- normalized phase Q
- raw action-deficit gap
- normalized action-deficit Q

The goal is not to reopen the gravity lane broadly, only to test whether a
near-mass action statistic improves the toy saturation law on the same small
impact-parameter family.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.momentum_space_gravity import (  # noqa: E402
    fourier_transform_y,
    prob_centroid_ky,
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
class ProbeConfig:
    name: str
    probe_x: int
    cut_mode: str
    description: str


@dataclass(frozen=True)
class ProbeMetrics:
    probe_name: str
    impact_b: int
    delta_ky: float
    valley_balance: float
    phase_gap: float
    phase_q: float
    action_gap: float
    action_q: float


@dataclass(frozen=True)
class FitSummary:
    feature: str
    best_scale: float
    best_gain: float
    r2: float
    mae: float

    def render(self) -> str:
        return (
            f"{self.feature}: Δky ~= {self.best_scale:.4f} * tanh({self.best_gain:.4f} * x) "
            f"(R²={self.r2:.4f}, MAE={self.mae:.4f})"
        )


PROBE_CONFIGS = (
    ProbeConfig(
        name="detector_y0",
        probe_x=45,
        cut_mode="zero",
        description="downstream continuation split at x=45, y>=0",
    ),
    ProbeConfig(
        name="detector_half_b",
        probe_x=45,
        cut_mode="half_b",
        description="downstream mass-aware split at x=45, y>=b/2",
    ),
    ProbeConfig(
        name="near_mass_b",
        probe_x=34,
        cut_mode="b",
        description="near-mass skirt split at x=34, y>=b",
    ),
)


def _angle_diff(a: float, b: float) -> float:
    return math.atan2(math.sin(a - b), math.cos(a - b))


def _circular_stats(weights: list[float], phases: list[float]) -> tuple[float, float]:
    total = sum(weights)
    if total <= 1e-12:
        return 0.0, float("inf")
    real = sum(weight * math.cos(phase) for weight, phase in zip(weights, phases))
    imag = sum(weight * math.sin(phase) for weight, phase in zip(weights, phases))
    mean_angle = math.atan2(imag, real)
    resultant = math.sqrt(real * real + imag * imag) / total
    if resultant <= 1e-12:
        return mean_angle, float("inf")
    sigma = math.sqrt(max(0.0, -2.0 * math.log(resultant)))
    return mean_angle, sigma


def _fit_tanh(feature: str, xs: list[float], ys: list[float]) -> FitSummary:
    best: FitSummary | None = None
    for gain in [10 ** (start / 10.0) for start in range(-10, 21)]:
        z = [math.tanh(gain * x) for x in xs]
        denom = sum(value * value for value in z)
        if denom <= 1e-12:
            continue
        scale = sum(value * target for value, target in zip(z, ys)) / denom
        preds = [scale * value for value in z]
        mean_y = statistics.fmean(ys)
        sse = sum((pred - target) ** 2 for pred, target in zip(preds, ys))
        sst = sum((target - mean_y) ** 2 for target in ys)
        r2 = 1.0 - sse / sst if sst > 1e-12 else 0.0
        mae = statistics.fmean(abs(pred - target) for pred, target in zip(preds, ys))
        candidate = FitSummary(
            feature=feature,
            best_scale=scale,
            best_gain=gain,
            r2=r2,
            mae=mae,
        )
        if best is None or (candidate.r2, -candidate.mae) > (best.r2, -best.mae):
            best = candidate
    assert best is not None
    return best


def _split_cut(impact_b: int, cut_mode: str) -> float:
    if cut_mode == "zero":
        return 0.0
    if cut_mode == "half_b":
        return impact_b / 2.0
    if cut_mode == "b":
        return float(impact_b)
    raise ValueError(f"Unsupported cut_mode: {cut_mode}")


def _edge_action(node: tuple[int, int], nb: tuple[int, int], node_field: dict[tuple[int, int], float]) -> tuple[float, float]:
    length = math.dist(node, nb)
    if length <= 1e-12:
        return 0.0, 0.0
    local_field = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
    delay = length * (1.0 + local_field)
    retained = math.sqrt(max(delay * delay - length * length, 0.0))
    return delay - retained, length


def _propagate_amplitudes(
    order: list[tuple[int, int]],
    dag: dict[tuple[int, int], list[tuple[int, int]]],
    source: tuple[int, int],
    node_field: dict[tuple[int, int], float],
    phase_k: float,
    atten_power: float,
) -> dict[tuple[int, int], complex]:
    amps = {source: 1.0 + 0.0j}
    for node in order:
        amp = amps.get(node)
        if amp is None:
            continue
        for nb in dag.get(node, []):
            action, length = _edge_action(node, nb, node_field)
            atten = 1.0 / (length ** atten_power) if length > 0 else 1.0
            edge_amp = amp * (math.e ** (1j * phase_k * action)) * atten
            amps[nb] = amps.get(nb, 0.0 + 0.0j) + edge_amp
    return amps


def _propagate_action_moments(
    order: list[tuple[int, int]],
    dag: dict[tuple[int, int], list[tuple[int, int]]],
    source: tuple[int, int],
    node_field: dict[tuple[int, int], float],
    atten_power: float,
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], float]]:
    weights = {source: 1.0}
    action_sum = {source: 0.0}
    action_sq_sum = {source: 0.0}

    for node in order:
        weight = weights.get(node)
        if weight is None:
            continue
        action_first = action_sum[node]
        action_second = action_sq_sum[node]
        for nb in dag.get(node, []):
            action, length = _edge_action(node, nb, node_field)
            atten = 1.0 / (length ** atten_power) if length > 0 else 1.0
            next_weight = atten * weight
            weights[nb] = weights.get(nb, 0.0) + next_weight
            action_sum[nb] = action_sum.get(nb, 0.0) + atten * (action_first + action * weight)
            action_sq_sum[nb] = action_sq_sum.get(nb, 0.0) + atten * (
                action_second + 2.0 * action * action_first + action * action * weight
            )

    means: dict[tuple[int, int], float] = {}
    sigmas: dict[tuple[int, int], float] = {}
    for node, total_weight in weights.items():
        if total_weight <= 1e-12:
            means[node] = 0.0
            sigmas[node] = 0.0
            continue
        mean = action_sum[node] / total_weight
        second_moment = action_sq_sum[node] / total_weight
        variance = max(0.0, second_moment - mean * mean)
        means[node] = mean
        sigmas[node] = math.sqrt(variance)
    return means, sigmas


def _aggregate_action_valley(
    weights: list[float],
    means: list[float],
    sigmas: list[float],
) -> tuple[float, float]:
    total = sum(weights)
    if total <= 1e-12:
        return 0.0, float("inf")
    valley_mean = sum(weight * mean for weight, mean in zip(weights, means)) / total
    valley_var = sum(
        weight * (sigma * sigma + (mean - valley_mean) ** 2)
        for weight, mean, sigma in zip(weights, means, sigmas)
    ) / total
    return valley_mean, math.sqrt(max(0.0, valley_var))


def _measure_probe(
    impact_b: int,
    delta_ky: float,
    probe: ProbeConfig,
    height: int,
    amps: dict[tuple[int, int], complex],
    mass_action_mean: dict[tuple[int, int], float],
    mass_action_sigma: dict[tuple[int, int], float],
    free_action_mean: dict[tuple[int, int], float],
    free_action_sigma: dict[tuple[int, int], float],
) -> ProbeMetrics:
    cut = _split_cut(impact_b, probe.cut_mode)
    screen_ys = list(range(-height, height + 1))

    upper_phase_weights: list[float] = []
    upper_phases: list[float] = []
    lower_phase_weights: list[float] = []
    lower_phases: list[float] = []

    upper_action_weights: list[float] = []
    upper_action_means: list[float] = []
    upper_action_sigmas: list[float] = []
    lower_action_weights: list[float] = []
    lower_action_means: list[float] = []
    lower_action_sigmas: list[float] = []

    for y in screen_ys:
        node = (probe.probe_x, y)
        amp = amps.get(node, 0.0 + 0.0j)
        weight = abs(amp) ** 2
        if weight <= 1e-20:
            continue
        phase = math.atan2(amp.imag, amp.real)

        action_mean = mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0)
        action_sigma = math.sqrt(
            mass_action_sigma.get(node, 0.0) ** 2 + free_action_sigma.get(node, 0.0) ** 2
        )

        if y >= cut:
            upper_phase_weights.append(weight)
            upper_phases.append(phase)
            upper_action_weights.append(weight)
            upper_action_means.append(action_mean)
            upper_action_sigmas.append(action_sigma)
        else:
            lower_phase_weights.append(weight)
            lower_phases.append(phase)
            lower_action_weights.append(weight)
            lower_action_means.append(action_mean)
            lower_action_sigmas.append(action_sigma)

    upper_phase_mean, upper_phase_sigma = _circular_stats(upper_phase_weights, upper_phases)
    lower_phase_mean, lower_phase_sigma = _circular_stats(lower_phase_weights, lower_phases)
    upper_weight = sum(upper_phase_weights)
    lower_weight = sum(lower_phase_weights)
    valley_balance = min(upper_weight, lower_weight) / max(upper_weight, lower_weight, 1e-12)
    phase_gap = abs(_angle_diff(upper_phase_mean, lower_phase_mean))
    pooled_phase_sigma = math.sqrt(upper_phase_sigma ** 2 + lower_phase_sigma ** 2)
    phase_q = phase_gap / pooled_phase_sigma if math.isfinite(pooled_phase_sigma) and pooled_phase_sigma > 1e-12 else 0.0

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

    return ProbeMetrics(
        probe_name=probe.name,
        impact_b=impact_b,
        delta_ky=delta_ky,
        valley_balance=valley_balance,
        phase_gap=phase_gap,
        phase_q=phase_q,
        action_gap=action_gap,
        action_q=action_q,
    )


def _evaluate_b(task: tuple[int, int, int, float, float]) -> list[ProbeMetrics]:
    impact_b, width, height, phase_k, atten_power = task
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
            impact_b=impact_b,
            delta_ky=delta_ky,
            probe=probe,
            height=height,
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
) -> list[list[ProbeMetrics]]:
    tasks = [(impact_b, width, height, phase_k, atten_power) for impact_b in impact_bs]
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
    args = parser.parse_args()

    impact_bs = [2, 4, 6, 8, 10, 12, 15, 18, 20]
    result_rows = run_rows(
        impact_bs=impact_bs,
        workers=max(1, args.workers),
        width=args.width,
        height=args.height,
        phase_k=args.phase_k,
        atten_power=args.atten_power,
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
            _fit_tanh("phase_gap", [row.phase_gap for row in rows], ys),
            _fit_tanh("phase_q", [row.phase_q for row in rows], ys),
            _fit_tanh("action_gap", [row.action_gap for row in rows], ys),
            _fit_tanh("action_q", [row.action_q for row in rows], ys),
        ]
        fits.sort(key=lambda fit: (fit.r2, -fit.mae), reverse=True)
        ranked_fits.extend((probe.name, fit) for fit in fits)

        print("=" * 88)
        print(f"Probe: {probe.name} ({probe.description})")
        print("=" * 88)
        print(
            f"{'b':>4s} {'Δky':>10s} {'phase_gap':>10s} {'phase_q':>9s} "
            f"{'action_gap':>11s} {'action_q':>10s} {'balance':>9s}"
        )
        print("-" * 78)
        for row in rows:
            print(
                f"{row.impact_b:4d} {row.delta_ky:+10.4f} {row.phase_gap:10.4f} {row.phase_q:9.4f} "
                f"{row.action_gap:11.4f} {row.action_q:10.4f} {row.valley_balance:9.4f}"
            )
        print()
        print("Best tanh fits:")
        for fit in fits:
            print(f"  {fit.render()}")
        print()

    ranked_fits.sort(key=lambda item: (item[1].r2, -item[1].mae), reverse=True)
    print("=" * 88)
    print("OVERALL FIT RANKING")
    print("=" * 88)
    for probe_name, fit in ranked_fits[:8]:
        print(f"  {probe_name}: {fit.render()}")
    print()

    best_probe, best_fit = ranked_fits[0]
    print("Interpretation:")
    if best_fit.feature == "action_gap":
        print(
            f"  The best retained bounded diagnostic is the raw action-deficit gap on {best_probe}."
        )
    elif best_fit.feature == "action_q":
        print(
            f"  The normalized action-deficit Q wins on {best_probe}, giving the first bounded support "
            "for the toy saturation law."
        )
    elif best_fit.feature == "phase_gap":
        print(
            f"  The raw phase gap on {best_probe} still beats the action-based diagnostics on this bounded compare."
        )
    else:
        print(
            f"  The normalized phase Q on {best_probe} still beats the action-based diagnostics on this bounded compare."
        )
    print(
        "  This compare keeps the corrected propagator and Δky readout fixed, so any change is coming only "
        "from the local valley statistic."
    )


if __name__ == "__main__":
    main()
