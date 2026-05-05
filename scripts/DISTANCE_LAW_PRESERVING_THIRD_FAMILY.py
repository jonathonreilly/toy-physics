#!/usr/bin/env python3
"""Direct distance-law probe for the high-drift/high-restore third family.

This runner asks one narrow question:

Does the third grown family from the three-family 9/9 card
(drift=0.50, restore=0.90) preserve both the signed-source package and the
near-Newtonian distance tail?

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation and weak charge-scaling sanity
- direct distance-tail fit on the same family

The claim surface is intentionally tiny:
- one family only
- no geometry-generic or family-wide wording
- if the tail fails, diagnose the blocking feature instead of broadening
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import math
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gate_b_grown_joint_package import grow


H = 0.5
NL = 25
PW = 10
MAX_D_PHYS = 3
BETA = 0.8
K = 5.0
FIELD_POWER = 1
SOURCE_STRENGTH = 5e-5
SIGN_SOURCE_Z = 3.0
DISTANCE_BS = [5, 6, 7, 8, 10]
SEEDS = [0, 1, 2, 3, 4, 5]
TARGET_FAMILY = (0.50, 0.90)


@dataclass(frozen=True)
class RowSummary:
    zero: float
    plus: float
    minus: float
    neutral: float
    double: float
    exponent: float
    tail_alpha: float
    tail_r2: float
    toward: int
    total: int

    @property
    def sign_ok(self) -> bool:
        return (
            abs(self.zero) < 1e-12
            and abs(self.neutral) < 1e-12
            and self.plus > 0.0
            and self.minus < 0.0
            and self.plus * self.minus < 0.0
            and abs(self.exponent - 1.0) < 0.05
        )

    @property
    def tail_ok(self) -> bool:
        return (
            math.isfinite(self.tail_alpha)
            and math.isfinite(self.tail_r2)
            and self.toward == self.total
            and self.tail_r2 > 0.90
            and abs(self.tail_alpha + 1.0) < 0.20
        )


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


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    for z_phys, charge in sources:
        node = _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
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
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * h2 / (L * L)
    return amps


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


def _fit_power(bs: list[float], deltas: list[float]) -> tuple[float, float]:
    pairs = [(b, abs(d)) for b, d in zip(bs, deltas) if b > 0 and abs(d) > 1e-30]
    if len(pairs) < 3:
        return math.nan, math.nan
    lx = [math.log(b) for b, _ in pairs]
    ly = [math.log(d) for _, d in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return math.nan, math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    alpha = sxy / sxx
    intercept = my - alpha * mx
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return alpha, r2


def _setup_slits(pos: list[tuple[float, float, float]], layers: list[list[int]]) -> set[int]:
    barrier_layer = NL // 3
    barrier = layers[barrier_layer]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    return set(barrier) - set(sa + sb)


def _measure_seed(drift: float, restore: float, seed: int) -> tuple[float, dict[float, float], float, float, float, float, float]:
    pos, adj, layers = grow(drift, restore, seed)
    det = layers[-1]
    blocked = _setup_slits(pos, layers)

    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        return _centroid_z(amps, pos, det) - z_free

    zero = run([])
    plus = run([(SIGN_SOURCE_Z, +1)])
    minus = run([(SIGN_SOURCE_Z, -1)])
    neutral = run([(SIGN_SOURCE_Z, +1), (SIGN_SOURCE_Z, -1)])
    double = run([(SIGN_SOURCE_Z, +2)])
    exponent = (
        math.log(abs(double / plus)) / math.log(2.0)
        if abs(plus) > 1e-30 and abs(double) > 1e-30
        else math.nan
    )

    tail_deltas: dict[float, float] = {}
    for b in DISTANCE_BS:
        field = _field_from_sources(pos, layers, [(float(b), +1)])
        amps = _propagate(pos, adj, field)
        tail_deltas[float(b)] = _centroid_z(amps, pos, det) - z_free

    return zero, tail_deltas, plus, minus, neutral, double, exponent


def _summarize_family(drift: float, restore: float) -> RowSummary:
    zero_vals: list[float] = []
    plus_vals: list[float] = []
    minus_vals: list[float] = []
    neutral_vals: list[float] = []
    double_vals: list[float] = []
    exponent_vals: list[float] = []
    by_b: dict[float, list[float]] = {float(b): [] for b in DISTANCE_BS}

    for seed in SEEDS:
        zero, tail_deltas, plus, minus, neutral, double, exponent = _measure_seed(drift, restore, seed)
        zero_vals.append(zero)
        plus_vals.append(plus)
        minus_vals.append(minus)
        neutral_vals.append(neutral)
        double_vals.append(double)
        exponent_vals.append(exponent)
        for b, delta in tail_deltas.items():
            by_b[b].append(delta)

    mean_tail = {b: _mean(vals) for b, vals in by_b.items()}
    toward = sum(1 for delta in mean_tail.values() if delta > 0)
    total = len(mean_tail)
    positive_bs = [b for b in DISTANCE_BS if mean_tail[b] > 0]
    tail_alpha, tail_r2 = _fit_power(positive_bs, [mean_tail[b] for b in positive_bs]) if len(positive_bs) >= 3 else (math.nan, math.nan)

    return RowSummary(
        zero=_mean(zero_vals),
        plus=_mean(plus_vals),
        minus=_mean(minus_vals),
        neutral=_mean(neutral_vals),
        double=_mean(double_vals),
        exponent=_mean(exponent_vals),
        tail_alpha=tail_alpha,
        tail_r2=tail_r2,
        toward=toward,
        total=total,
    )


def _render_log(summary: RowSummary, drift: float, restore: float) -> str:
    lines = [
        "=" * 96,
        "DISTANCE LAW PRESERVING THIRD FAMILY",
        "  direct tail test on the high-drift/high-restore third grown family",
        "=" * 96,
        f"family=(drift={drift:.2f}, restore={restore:.2f}), seeds={SEEDS}, b={DISTANCE_BS}",
        "guards: exact zero-source baseline, exact neutral cancellation, sign orientation, weak charge scaling",
        "",
        f"{'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'alpha':>8s} {'r2':>7s} {'toward':>9s}",
        "-" * 108,
        (
            f"{summary.zero:+12.3e} {summary.plus:+12.3e} {summary.minus:+12.3e} "
            f"{summary.neutral:+12.3e} {summary.double:+12.3e} {summary.exponent:7.3f} "
            f"{summary.tail_alpha:8.3f} {summary.tail_r2:7.3f} {summary.toward:9d}/{summary.total:<3d}"
        ),
        "",
        "SAFE READ",
        f"  sign gate: {'PASS' if summary.sign_ok else 'FAIL'}",
        f"  tail gate: {'PASS' if summary.tail_ok else 'FAIL'}",
    ]
    if summary.sign_ok and summary.tail_ok:
        lines.extend(
            [
                "  the high-drift/high-restore third family preserves both the signed-source package",
                "  and the near-Newtonian distance tail on this direct test",
            ]
        )
    elif summary.sign_ok:
        lines.extend(
            [
                "  the signed-source package survives, but the distance tail does not stay near-Newtonian",
                "  diagnose the tail failure rather than broadening the family claim",
            ]
        )
    else:
        lines.extend(
            [
                "  the family does not clear the exact zero/neutral or sign gate",
                "  diagnose the sign control failure before any tail claim",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-log", type=str, default="", help="optional path to write the rendered report")
    args = parser.parse_args()

    drift, restore = TARGET_FAMILY
    summary = _summarize_family(drift, restore)
    rendered = _render_log(summary, drift, restore)
    print(rendered)

    if args.write_log:
        out = Path(args.write_log)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")

    payload: dict[str, Any] = {
        "family": {"drift": drift, "restore": restore},
        "seeds": SEEDS,
        "distance_bs": DISTANCE_BS,
        "summary": asdict(summary),
        "sign_ok": summary.sign_ok,
        "tail_ok": summary.tail_ok,
    }
    if not args.write_log:
        # Keep the structured payload available on stdout for ad hoc parsing.
        print()
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
