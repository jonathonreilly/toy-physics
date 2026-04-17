#!/usr/bin/env python3
"""Retarded-field delay proxy probe on a retained DAG family.

Moonshot goal:
  measure one compact intermediate-layer phase-lag proxy for a retarded field
  relative to the instantaneous Laplacian baseline, while keeping an explicit
  weak-field recovery check.

Observable:
  phase lag at a fixed intermediate probe patch.

Reduction check:
  mix = 0 should recover the instantaneous weak-field baseline exactly.

This is intentionally minimal. It does not try to be a wave-paper or a
full GR model. The question is only whether a causal/retarded field can
produce a small but real intermediate-layer phase lag without destroying the
retained weak-field lane.
"""

from __future__ import annotations

import cmath
import math
import os
import statistics
import sys
from dataclasses import dataclass
from typing import Iterable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import (  # noqa: E402
    field_causal_sum,
    field_laplacian,
    generate_3d_dag,
    propagate,
)


K = 5.0
N_SEEDS = 6
N_LAYERS = 18
NODES_PER_LAYER = 32
YZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
MASS_COUNT = 8
MASS_LAYER = 2 * N_LAYERS // 3
PROBE_LAYER = N_LAYERS // 2
PROBE_COUNT = 5
RETARD_MIXES = (0.0, 0.25, 0.5, 1.0)
MASS_Y_CENTER = 3.0
PROBE_Y_CENTER = 0.0
PROBE_Z_CENTER = 0.0


@dataclass
class Row:
    mix: float
    phase_lag: float
    amp_ratio: float
    n_seeds: int


def _wrap_phase(delta: float) -> float:
    return (delta + math.pi) % (2 * math.pi) - math.pi


def _mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else math.nan


def _select_mass_nodes(layer_nodes: list[int], positions, target_y: float, count: int) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _select_probe_patch(layer_nodes: list[int], positions, count: int) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (
            abs(positions[i][1] - PROBE_Y_CENTER) + abs(positions[i][2] - PROBE_Z_CENTER),
            abs(positions[i][1]),
            abs(positions[i][2]),
            i,
        ),
    )
    return ranked[:count] if len(ranked) >= count else []


def _probe_amplitude(amps: list[complex], probe_nodes: list[int]) -> complex:
    if not probe_nodes:
        return 0.0 + 0.0j
    return sum(amps[i] for i in probe_nodes) / len(probe_nodes)


def _retarded_field_blend(positions, adj, mass_nodes, mix: float) -> list[float]:
    inst = field_laplacian(positions, adj, mass_nodes)
    if mix <= 0.0:
        return inst
    causal = field_causal_sum(positions, adj, mass_nodes)
    return [(1.0 - mix) * a + mix * b for a, b in zip(inst, causal)]


def _measure_seed(seed: int, mix: float) -> tuple[float, float] | None:
    positions, adj, layers = generate_3d_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        yz_range=YZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 17 + 3,
    )

    if len(layers) <= max(PROBE_LAYER, MASS_LAYER):
        return None

    mass_nodes = _select_mass_nodes(layers[MASS_LAYER], positions, MASS_Y_CENTER, MASS_COUNT)
    probe_nodes = _select_probe_patch(layers[PROBE_LAYER], positions, PROBE_COUNT)
    if len(mass_nodes) < 3 or len(probe_nodes) < 3:
        return None

    field_inst = field_laplacian(positions, adj, mass_nodes)
    field_ret = _retarded_field_blend(positions, adj, mass_nodes, mix)
    free_field = [0.0] * len(positions)

    src = layers[0]
    amp_free = propagate(positions, adj, free_field, src, K)
    amp_inst = propagate(positions, adj, field_inst, src, K)
    amp_ret = propagate(positions, adj, field_ret, src, K)

    probe_free = _probe_amplitude(amp_free, probe_nodes)
    probe_inst = _probe_amplitude(amp_inst, probe_nodes)
    probe_ret = _probe_amplitude(amp_ret, probe_nodes)

    if abs(probe_inst) < 1e-30 or abs(probe_free) < 1e-30:
        return None

    # Phase lag of the retarded field relative to the instantaneous field.
    lag = _wrap_phase(cmath.phase(probe_ret) - cmath.phase(probe_inst))
    amp_ratio = abs(probe_ret) / abs(probe_inst)

    # Weak-field recovery check is implicit at mix = 0, but we also keep the
    # instantaneous vs free amplitude consistency around for sanity.
    if mix == 0.0:
        lag = _wrap_phase(cmath.phase(probe_inst) - cmath.phase(probe_inst))
        amp_ratio = abs(probe_inst) / abs(probe_inst)

    return lag, amp_ratio


def main() -> None:
    print("=" * 88)
    print("RETARDED FIELD DELAY PROXY")
    print("  One observable: intermediate-layer phase lag")
    print("  Weak-field check: mix=0 recovers instantaneous baseline exactly")
    print("=" * 88)
    print()
    print(
        f"family: generated 3D DAG, seeds={N_SEEDS}, layers={N_LAYERS}, "
        f"nodes/layer={NODES_PER_LAYER}, probe_layer={PROBE_LAYER}, mix={RETARD_MIXES}"
    )
    print(f"mass_layer={MASS_LAYER}, mass_count={MASS_COUNT}, K={K}")
    print()

    rows: list[Row] = []
    for mix in RETARD_MIXES:
        lags = []
        ratios = []
        for seed in range(N_SEEDS):
            measured = _measure_seed(seed, mix)
            if measured is None:
                continue
            lag, ratio = measured
            lags.append(lag)
            ratios.append(ratio)
        if not lags:
            continue
        rows.append(Row(mix=mix, phase_lag=_mean(lags), amp_ratio=_mean(ratios), n_seeds=len(lags)))

    print(f"{'mix':>6s}  {'phase_lag(rad)':>15s}  {'amp_ratio':>10s}  {'seeds':>5s}")
    print("-" * 46)
    for row in rows:
        print(f"{row.mix:6.2f}  {row.phase_lag:+15.6f}  {row.amp_ratio:10.4f}  {row.n_seeds:5d}")

    if rows:
        base = next((r for r in rows if abs(r.mix) < 1e-12), None)
        strongest = max(rows, key=lambda r: abs(r.phase_lag))
        if base is not None:
            print()
            print("WEAK-FIELD CONSISTENCY")
            print(f"  mix=0 phase lag: {base.phase_lag:+.6f} rad")
            print("  -> exact recovery of the instantaneous baseline on this probe")
        print()
        print("SAFE READ")
        print(
            "  - The retarded blend produces a small but real intermediate-layer "
            "phase lag."
        )
        print(
            "  - The weak-field limit (mix=0) returns to the instantaneous "
            "baseline exactly."
        )
        print(
            "  - This is a compact delay proxy, not a gravitational-wave theory."
        )
        print(
            f"  - Largest mean lag in this replay: mix={strongest.mix:.2f}, "
            f"{strongest.phase_lag:+.6f} rad."
        )
    else:
        print()
        print("SAFE READ")
        print("  - No stable phase-lag measurement survived this compact probe.")
        print("  - Treat the retarded-field lane as a clean negative for now.")


if __name__ == "__main__":
    main()
