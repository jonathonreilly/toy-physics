#!/usr/bin/env python3
"""4D visibility envelope check on the retained modular lane.

This is the stricter follow-up to the fixed-bin 4D visibility readout.
It keeps the same retained 4D modular DAG family, but asks a more cautious
question:

  - if we rebin the detector profile more coarsely
  - and compare a smoothed envelope of the coherent two-slit profile against
    the smoothed envelope of the single-slit average

does any strict visibility gain survive, or does it flatten out?

The goal is not to maximize the metric. The goal is to find out whether the
small positive binned gains were a detector/binning artifact or a real effect.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.four_d_true_visibility_binned import (  # type: ignore  # noqa: E402
    build_setup,
    compute_field_4d,
    generate_4d_modular_dag,
    propagate_4d,
)

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_BINS = 10
Y_MIN = -8.0
Y_MAX = 8.0
REBIN_WIDTH = 2
SMOOTH_RADIUS = 1
N_SEEDS = 8
N_LAYERS_LIST = (12, 18, 25, 40, 60, 80, 100)
GAPS = (3.0, 5.0)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _binned_profile(
    probs: dict[int, float],
    positions: list[tuple[float, float, float, float]],
    det_list: list[int],
    *,
    y_min: float = Y_MIN,
    y_max: float = Y_MAX,
    n_bins: int = N_BINS,
) -> list[float]:
    bw = (y_max - y_min) / n_bins
    bins = [0.0] * n_bins
    for d in det_list:
        y = positions[d][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += probs.get(d, 0.0)
    return bins


def _rebin(profile: list[float], width: int = REBIN_WIDTH) -> list[float]:
    if width <= 1:
        return profile[:]
    out: list[float] = []
    for i in range(0, len(profile), width):
        chunk = profile[i : i + width]
        if chunk:
            out.append(sum(chunk) / len(chunk))
    return out


def _smooth(profile: list[float], radius: int = SMOOTH_RADIUS) -> list[float]:
    if radius <= 0 or len(profile) < 3:
        return profile[:]
    out: list[float] = []
    for i in range(len(profile)):
        lo = max(0, i - radius)
        hi = min(len(profile), i + radius + 1)
        window = profile[lo:hi]
        out.append(sum(window) / len(window))
    return out


def _envelope_visibility(profile: list[float]) -> float:
    coarse = _smooth(_rebin(profile))
    if len(coarse) < 4:
        return 0.0

    local_vals: list[float] = []
    for i in range(1, len(coarse) - 1):
        lo = max(0, i - 1)
        hi = min(len(coarse), i + 2)
        upper = max(coarse[lo:hi])
        lower = min(coarse[lo:hi])
        if upper + lower > 1e-30:
            local_vals.append((upper - lower) / (upper + lower))
    return max(local_vals) if local_vals else 0.0


def _detector_probs(amps: list[complex], det_list: list[int]) -> dict[int, float]:
    probs = {d: abs(amps[d]) ** 2 for d in det_list}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def _visibility_seed_metric(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    setup,
) -> tuple[float, float, float] | None:
    src = setup["src"]
    det_list = setup["det_list"]
    field = setup["field"]
    blocked = setup["blocked"]
    slit_a = setup["slit_a"]
    slit_b = setup["slit_b"]

    coh_vals: list[float] = []
    single_vals: list[float] = []
    for k in K_BAND:
        amps_both = propagate_4d(positions, adj, field, src, k, blocked)
        amps_a = propagate_4d(positions, adj, field, src, k, blocked | set(slit_b))
        amps_b = propagate_4d(positions, adj, field, src, k, blocked | set(slit_a))

        probs_both = _detector_probs(amps_both, det_list)
        probs_a = _detector_probs(amps_a, det_list)
        probs_b = _detector_probs(amps_b, det_list)
        probs_single_avg = {
            d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
            for d in det_list
        }

        coh_profile = _binned_profile(probs_both, positions, det_list)
        single_profile = _binned_profile(probs_single_avg, positions, det_list)
        coh_vals.append(_envelope_visibility(coh_profile))
        single_vals.append(_envelope_visibility(single_profile))

    if not coh_vals:
        return None
    avg_coh = _mean(coh_vals)
    avg_single = _mean(single_vals)
    return avg_coh, avg_single, avg_coh - avg_single


def main() -> None:
    print("=" * 78)
    print("4D VISIBILITY ENVELOPE: Modular DAGs")
    print("  Strict envelope/rebin check on the retained modular family")
    print("  Goal: see whether strict visibility survives a more conservative metric")
    print("=" * 78)
    print()
    print(f"  seeds per row: {N_SEEDS}")
    print(f"  bins: {N_BINS}, rebin width: {REBIN_WIDTH}, smooth radius: {SMOOTH_RADIUS}")
    print(f"  k-band: {K_BAND}")
    print()

    print(
        f"  {'gap':>4s}  {'N':>4s}  {'V_env_coh':>9s}  {'V_env_sng':>9s}  "
        f"{'V_gain':>8s}  {'SE':>6s}  {'n_ok':>4s}  verdict"
    )
    print(f"  {'-' * 72}")

    for gap in GAPS:
        for nl in N_LAYERS_LIST:
            coh_vals: list[float] = []
            single_vals: list[float] = []
            gain_vals: list[float] = []
            t0 = time.time()
            n_ok = 0

            for seed in range(N_SEEDS):
                positions, adj, _ = generate_4d_modular_dag(
                    n_layers=nl,
                    nodes_per_layer=25,
                    spatial_range=8.0,
                    connect_radius=4.5,
                    rng_seed=seed * 13 + 5,
                    gap=gap,
                )
                setup = build_setup(positions, adj)
                if setup is None:
                    continue

                result = _visibility_seed_metric(positions, adj, setup)
                if result is None:
                    continue
                avg_coh, avg_single, gain = result
                coh_vals.append(avg_coh)
                single_vals.append(avg_single)
                gain_vals.append(gain)
                n_ok += 1

            if n_ok:
                mc = _mean(coh_vals)
                ms = _mean(single_vals)
                mg = _mean(gain_vals)
                se = _se(gain_vals)
                verdict = "PASS" if mg > 0.02 else "WEAK" if mg > 0 else "NONE"
                print(
                    f"  {gap:4.1f}  {nl:4d}  {mc:9.3f}  {ms:9.3f}  "
                    f"{mg:+8.3f}  {se:6.3f}  {n_ok:4d}  {verdict}"
                )
            else:
                print(f"  {gap:4.1f}  {nl:4d}  FAIL")

            # Keep the output compact but preserve the time budget in case the
            # retained family becomes more expensive at larger N.
            _ = time.time() - t0

    print()
    print("INTERPRETATION")
    print("  V_gain > 0 means the coherent two-slit envelope differs from the")
    print("  single-slit envelope after coarse rebinning and local smoothing.")
    print("  If the gains stay near zero across the retained family, strict")
    print("  visibility is effectively flat under this stricter metric.")
    print("=" * 78)


if __name__ == "__main__":
    main()
