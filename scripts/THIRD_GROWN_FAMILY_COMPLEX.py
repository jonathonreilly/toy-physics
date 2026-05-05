#!/usr/bin/env python3
"""Complex-action probe for the third grown-family signed basin.

This is intentionally narrow:
- use the retained third-family no-restore grown slice
- keep the exact gamma=0 baseline explicit
- check whether any interior drift row carries a retained TOWARD -> AWAY
  crossover on top of the signed-source basin
- keep weak-field F~M and a Born proxy visible, but do not broaden the claim

If the complex-action branch fails, the script should diagnose the boundary
instead of inflating the claim surface.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
from dataclasses import dataclass


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from THIRD_GROWN_FAMILY_SIGN_SWEEP import Family, _build_third_connectivity
from gate_b_no_restore_farfield import grow


H = 0.5
K = 5.0
NL = 25
BETA = 0.8
SOURCE_Z = 3.0
SOURCE_STRENGTH = 0.1
SOURCE_STRENGTHS = [1e-6, 1e-5]
DRIFTS = [0.0, 0.1, 0.2, 0.3, 0.5]
SEEDS = [0, 1, 2]


@dataclass(frozen=True)
class RowResult:
    drift: float
    born: float | None
    gamma0_delta: float
    delta_01: float
    delta_02: float
    delta_05: float
    escape_01: float
    escape_05: float
    fm_0: float | None
    fm_05: float | None
    toward_01: int
    toward_05: int

    @property
    def anchor_ok(self) -> bool:
        return (
            self.born is not None
            and self.born < 1e-12
            and self.fm_0 is not None
            and self.fm_05 is not None
            and abs(self.fm_0 - 1.0) < 0.05
            and abs(self.fm_05 - 1.0) < 0.05
        )

    @property
    def crossover_ok(self) -> bool:
        return self.toward_01 > 0 and self.toward_05 == 0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _nearest_node_in_layer(
    pos: list[tuple[float, float, float]],
    layer_nodes: list[int],
    x_target: float,
    y_target: float,
    z_target: float,
) -> int | None:
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _build_field(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    strength: float,
    source_z: float,
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    node = _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, source_z)
    if node is None:
        return field
    sx, sy, sz = pos[node]
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[i] = strength / r
    return field


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    gamma: float,
    sources: list[tuple[int, complex]] | None = None,
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
    h2 = H * H
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 - lf)
            decay = -gamma * L * lf
            damp = math.exp(max(min(decay, 50.0), -50.0))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * damp * w * h2 / (L * L)
    return amps


def _det_prob(amps: list[complex], det: list[int]) -> float:
    return sum(abs(amps[i]) ** 2 for i in det)


def _centroid_z(
    amps: list[complex],
    pos: list[tuple[float, float, float]],
    det: list[int],
) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _born_proxy(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layers: list[list[int]],
    field: list[float],
    gamma: float,
) -> float:
    source_layer = layers[1]
    picks = [source_layer[0], source_layer[len(source_layer) // 2], source_layer[-1]]
    det = layers[-1]

    def p_subset(subset: list[int]) -> float:
        amps = _propagate(pos, adj, field, gamma, sources=[(idx, 1.0 + 0j) for idx in subset])
        return _det_prob(amps, det)

    p123 = p_subset(picks)
    p12 = p_subset(picks[:2])
    p13 = p_subset([picks[0], picks[2]])
    p23 = p_subset(picks[1:])
    p1 = p_subset([picks[0]])
    p2 = p_subset([picks[1]])
    p3 = p_subset([picks[2]])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-30)


def _measure_row(drift: float) -> RowResult:
    born_vals: list[float] = []
    gamma0_deltas: list[float] = []
    delta_01_vals: list[float] = []
    delta_02_vals: list[float] = []
    delta_05_vals: list[float] = []
    escape_01_vals: list[float] = []
    escape_05_vals: list[float] = []
    fm0_vals: list[float] = []
    fm05_vals: list[float] = []
    toward_01 = 0
    toward_05 = 0

    for seed in SEEDS:
        pos, _adj, layers, _nmap = grow(drift, seed)
        fam = Family(pos, layers, {})
        third = _build_third_connectivity(fam)
        det = third.layers[-1]

        zero = [0.0] * len(third.positions)
        free = _propagate(third.positions, third.adj, zero, 0.0)
        z_free = _centroid_z(free, third.positions, det)
        p_free = _det_prob(free, det)

        field = _build_field(third.positions, third.layers, SOURCE_STRENGTH, SOURCE_Z)
        gamma0 = _propagate(third.positions, third.adj, field, 0.0)
        gamma0_deltas.append(_centroid_z(gamma0, third.positions, det) - z_free)

        if seed == 0 and abs(drift - 0.20) < 1e-12:
            born_vals.append(_born_proxy(third.positions, third.adj, third.layers, field, 0.0))

        grav_01 = _propagate(third.positions, third.adj, field, 0.1)
        grav_02 = _propagate(third.positions, third.adj, field, 0.2)
        grav_05 = _propagate(third.positions, third.adj, field, 0.5)

        delta_01 = _centroid_z(grav_01, third.positions, det) - z_free
        delta_02 = _centroid_z(grav_02, third.positions, det) - z_free
        delta_05 = _centroid_z(grav_05, third.positions, det) - z_free
        delta_01_vals.append(delta_01)
        delta_02_vals.append(delta_02)
        delta_05_vals.append(delta_05)
        if delta_01 > 0:
            toward_01 += 1
        if delta_05 > 0:
            toward_05 += 1

        escape_01_vals.append(_det_prob(grav_01, det) / p_free if p_free > 1e-30 else 0.0)
        escape_05_vals.append(_det_prob(grav_05, det) / p_free if p_free > 1e-30 else 0.0)

        weak_deltas = []
        for s in SOURCE_STRENGTHS:
            weak_field = _build_field(third.positions, third.layers, s, SOURCE_Z)
            amp = _propagate(third.positions, third.adj, weak_field, 0.0)
            weak_deltas.append(abs(_centroid_z(amp, third.positions, det) - z_free))
        d1, d2 = weak_deltas
        s1, s2 = SOURCE_STRENGTHS
        if d1 > 1e-15 and d2 > 1e-15:
            fm0_vals.append(math.log(d2 / d1) / math.log(s2 / s1))

        weak_deltas = []
        for s in SOURCE_STRENGTHS:
            weak_field = _build_field(third.positions, third.layers, s, SOURCE_Z)
            amp = _propagate(third.positions, third.adj, weak_field, 0.5)
            weak_deltas.append(abs(_centroid_z(amp, third.positions, det) - z_free))
        d1, d2 = weak_deltas
        if d1 > 1e-15 and d2 > 1e-15:
            fm05_vals.append(math.log(d2 / d1) / math.log(s2 / s1))

    return RowResult(
        drift=drift,
        born=born_vals[0] if born_vals else None,
        gamma0_delta=_mean(gamma0_deltas),
        delta_01=_mean(delta_01_vals),
        delta_02=_mean(delta_02_vals),
        delta_05=_mean(delta_05_vals),
        escape_01=_mean(escape_01_vals),
        escape_05=_mean(escape_05_vals),
        fm_0=_mean(fm0_vals) if fm0_vals else None,
        fm_05=_mean(fm05_vals) if fm05_vals else None,
        toward_01=toward_01,
        toward_05=toward_05,
    )


def main() -> None:
    print("=" * 98)
    print("THIRD GROWN FAMILY COMPLEX")
    print("  third-family no-restore cross-quadrant basin")
    print("=" * 98)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact gamma=0 baseline, Born proxy where feasible, TOWARD -> AWAY crossover")
    print()
    print(
        f"{'drift':>5s} {'born':>10s} {'g0':>12s} {'d01':>12s} {'d02':>12s} {'d05':>12s} "
        f"{'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}"
    )
    print("-" * 118)

    rows: list[RowResult] = []
    for drift in DRIFTS:
        row = _measure_row(drift)
        rows.append(row)
        born = f"{row.born:.3e}" if row.born is not None else "   n/a"
        fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "   n/a"
        fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "   n/a"
        print(
            f"{row.drift:5.2f} {born:>10s} {row.gamma0_delta:+12.6e} "
            f"{row.delta_01:+12.6e} {row.delta_02:+12.6e} {row.delta_05:+12.6e} "
            f"{row.escape_01:8.3f} {row.escape_05:8.3f} {fm0:>7s} {fm05:>7s} "
            f"{row.toward_01:5d} {row.toward_05:5d}"
        )

    anchor = next(r for r in rows if abs(r.drift - 0.20) < 1e-12)
    print()
    print("SAFE READ")
    print(f"  anchor retained gamma=0 + Born proxy: {anchor.anchor_ok}")
    print(f"  anchor TOWARD@0.1 -> AWAY@0.5: {anchor.crossover_ok}")
    if anchor.anchor_ok and anchor.crossover_ok:
        print("  the retained anchor row carries the complex-action companion narrowly")
    else:
        print("  the third grown-family candidate does not retain the complex-action companion cleanly")


if __name__ == "__main__":
    main()
