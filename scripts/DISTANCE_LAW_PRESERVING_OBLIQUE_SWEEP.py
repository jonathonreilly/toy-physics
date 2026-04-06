#!/usr/bin/env python3
"""Oblique-strip family sweep for distance-law portability.

This is a genuinely new candidate family, distinct from the retained shell,
quadrant, radial, and sheared families:
- no-restore grown slice
- layer-dependent oblique strip bins in the y/z plane
- parity alternates the strip bias between layers

The goal is deliberately narrow:
1. exact zero/neutral controls
2. signed-source / weak-field success
3. near-Newtonian distance-tail viability

If the family fails, the script diagnoses the breakpoint instead of widening
the claim.
"""

from __future__ import annotations

import bisect
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

from gate_b_no_restore_farfield import grow


H = 0.5
NL = 25
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
MIN_EDGES = 5
STRIP_COUNT = 8
SHEAR_MAG = 0.33
DRIFTS = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50]
SEEDS = [0, 1, 2]
DISTANCE_BS = [5, 6, 7, 8, 10]


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


@dataclass(frozen=True)
class RowResult:
    drift: float
    seed: int
    zero: float
    plus: float
    minus: float
    neutral: float
    double: float
    exponent: float
    sign_ok: bool
    alpha: float
    r2: float
    toward_count: int
    distance_ok: bool


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _layer_centers(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
) -> list[tuple[float, float]]:
    centers: list[tuple[float, float]] = []
    for layer in layers:
        ys = [pos[i][1] for i in layer]
        zs = [pos[i][2] for i in layer]
        centers.append((sum(ys) / len(ys), sum(zs) / len(zs)))
    return centers


def _oblique_coordinate(
    y: float,
    z: float,
    cy: float,
    cz: float,
    layer_idx: int,
) -> float:
    shear = SHEAR_MAG if layer_idx % 2 == 0 else -SHEAR_MAG
    dy = y - cy
    dz = z - cz
    return dy + shear * dz


def _strip_index(value: float, values: list[float]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    rank = bisect.bisect_right(ordered, value)
    idx = rank * STRIP_COUNT // max(len(ordered), 1)
    return max(0, min(STRIP_COUNT - 1, idx))


def _neighbor_strip(strip: int, layer_idx: int) -> int:
    if layer_idx % 2 == 0:
        return min(STRIP_COUNT - 1, strip + 1)
    return max(0, strip - 1)


def _build_oblique_strip_connectivity(fam: Family) -> Family:
    """Build a parity-tapered oblique-strip connectivity family.

    The family bins each layer by an oblique coordinate rather than a radial
    shell or quadrant. That keeps the construction genuinely distinct from the
    earlier retained families while still being structured enough to audit.
    """

    pos = fam.positions
    layers = fam.layers
    centers = _layer_centers(pos, layers)
    adj: dict[int, list[int]] = {i: [] for i in range(len(pos))}

    for layer_idx in range(len(layers) - 1):
        src_layer = layers[layer_idx]
        dst_layer = layers[layer_idx + 1]
        cy_src, cz_src = centers[layer_idx]
        cy_dst, cz_dst = centers[layer_idx + 1]

        src_coords = [
            _oblique_coordinate(pos[i][1], pos[i][2], cy_src, cz_src, layer_idx)
            for i in src_layer
        ]
        dst_coords = [
            _oblique_coordinate(pos[i][1], pos[i][2], cy_dst, cz_dst, layer_idx + 1)
            for i in dst_layer
        ]

        dst_by_strip: dict[int, list[int]] = {s: [] for s in range(STRIP_COUNT)}
        for dst, coord in zip(dst_layer, dst_coords):
            strip = _strip_index(coord, dst_coords)
            dst_by_strip[strip].append(dst)

        for src, coord in zip(src_layer, src_coords):
            src_strip = _strip_index(coord, src_coords)
            target_strips = [src_strip, _neighbor_strip(src_strip, layer_idx)]

            chosen: list[int] = []
            for target in target_strips:
                candidates = dst_by_strip.get(target, [])
                if not candidates:
                    continue
                best = min(
                    candidates,
                    key=lambda dst: (
                        pos[dst][0] - pos[src][0]
                    ) ** 2
                    + (pos[dst][1] - pos[src][1]) ** 2
                    + (pos[dst][2] - pos[src][2]) ** 2,
                )
                if best not in chosen:
                    chosen.append(best)

            if not chosen:
                best = min(
                    dst_layer,
                    key=lambda dst: (
                        pos[dst][0] - pos[src][0]
                    ) ** 2
                    + (pos[dst][1] - pos[src][1]) ** 2
                    + (pos[dst][2] - pos[src][2]) ** 2,
                )
                chosen.append(best)

            for dst in sorted(
                dst_layer,
                key=lambda d: (
                    pos[d][0] - pos[src][0]
                ) ** 2
                + (pos[d][1] - pos[src][1]) ** 2
                + (pos[d][2] - pos[src][2]) ** 2,
            ):
                if len(chosen) >= MIN_EDGES:
                    break
                if dst not in chosen:
                    chosen.append(dst)
            adj[src].extend(chosen)

    return Family(pos, layers, adj)


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    layer_nodes = layers[source_layer]

    for z_phys, charge in sources:
        best = None
        best_d = float("inf")
        for idx in layer_nodes:
            x, y, z = pos[idx]
            d = (x - x_target) ** 2 + y**2 + (z - z_phys) ** 2
            if d < best_d:
                best = idx
                best_d = d
        if best is None:
            continue

        mx, my, mz = pos[best]
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
    hm = H * H
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
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
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


def _sign_metrics(fam: Family) -> tuple[float, float, float, float, float, float, bool]:
    det = fam.layers[-1]
    free = _propagate(fam.positions, fam.adj, [0.0] * len(fam.positions))
    z_free = _centroid_z(free, fam.positions, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(fam.positions, fam.layers, sources)
        amps = _propagate(fam.positions, fam.adj, field)
        return _centroid_z(amps, fam.positions, det) - z_free

    zero = run([])
    plus = run([(SOURCE_Z, +1)])
    minus = run([(SOURCE_Z, -1)])
    neutral = run([(SOURCE_Z, +1), (SOURCE_Z, -1)])
    double = run([(SOURCE_Z, +2)])
    exponent = (
        math.log(abs(double / plus)) / math.log(2.0)
        if abs(plus) > 1e-30 and abs(double) > 1e-30
        else math.nan
    )
    ok = (
        abs(zero) < 1e-12
        and abs(neutral) < 1e-12
        and plus > 0.0
        and minus < 0.0
        and plus * minus < 0.0
        and abs(exponent - 1.0) < 0.05
    )
    return zero, plus, minus, neutral, double, exponent, ok


def _source_centroid_shift(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layers: list[list[int]],
    z_mass: float,
    field_strength: float,
) -> float:
    det = layers[-1]
    source_layer = len(layers) // 3
    x_target = layers[source_layer][0] and pos[layers[source_layer][0]][0]
    layer_nodes = layers[source_layer]

    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + y**2 + (z - z_mass) ** 2
        if d < best_d:
            best = idx
            best_d = d
    if best is None:
        return float("nan")

    def field_from_mass(mass_idx: int) -> list[float]:
        field = [0.0] * len(pos)
        mx, my, mz = pos[mass_idx]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] = field_strength / r
        return field

    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)
    amps = _propagate(pos, adj, field_from_mass(best))
    z_mass = _centroid_z(amps, pos, det)
    return z_mass - z_free


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


def _distance_metrics(fam: Family) -> tuple[float, float, int]:
    shifts = []
    toward = 0
    for b in DISTANCE_BS:
        delta = _source_centroid_shift(fam.positions, fam.adj, fam.layers, float(b), 0.004)
        shifts.append(delta)
        if delta > 0:
            toward += 1
    alpha, r2 = _fit_power([float(b) for b in DISTANCE_BS], shifts)
    return alpha, r2, toward


def _evaluate_row(drift: float, seed: int) -> RowResult:
    pos, _adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, {})
    oblique = _build_oblique_strip_connectivity(fam)
    zero, plus, minus, neutral, double, exponent, sign_ok = _sign_metrics(oblique)
    alpha = float("nan")
    r2 = float("nan")
    toward_count = 0
    distance_ok = False
    if sign_ok:
        alpha, r2, toward_count = _distance_metrics(oblique)
        distance_ok = (
            toward_count == len(DISTANCE_BS)
            and math.isfinite(alpha)
            and abs(alpha + 1.0) < 0.2
            and math.isfinite(r2)
            and r2 > 0.9
        )
    return RowResult(
        drift=drift,
        seed=seed,
        zero=zero,
        plus=plus,
        minus=minus,
        neutral=neutral,
        double=double,
        exponent=exponent,
        sign_ok=sign_ok,
        alpha=alpha,
        r2=r2,
        toward_count=toward_count,
        distance_ok=distance_ok,
    )


def main() -> None:
    print("=" * 100)
    print("DISTANCE LAW PRESERVING OBLIQUE SWEEP")
    print("  no-restore grown slice with parity-tapered oblique-strip connectivity")
    print("=" * 100)
    print(f"h={H}, NL={NL}, drifts={DRIFTS}, seeds={SEEDS}, distance_bs={DISTANCE_BS}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation, weak-field fit")
    print()
    print(
        f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} "
        f"{'neutral':>12s} {'double':>12s} {'exp':>7s} {'alpha':>8s} {'R2':>6s} "
        f"{'T':>2s} {'S':>2s} {'D':>2s}"
    )
    print("-" * 100)

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            row = _evaluate_row(drift, seed)
            rows.append(row)
            print(
                f"{row.drift:5.2f} {row.seed:4d} "
                f"{row.zero:+12.3e} {row.plus:+12.3e} {row.minus:+12.3e} "
                f"{row.neutral:+12.3e} {row.double:+12.3e} {row.exponent:7.3f} "
                f"{row.alpha:8.3f} {row.r2:6.3f} "
                f"{row.toward_count:2d} "
                f"{'Y' if row.sign_ok else 'n':>2s} "
                f"{'Y' if row.distance_ok else 'n':>2s}"
            )

    sign_pass = [r for r in rows if r.sign_ok]
    dist_pass = [r for r in rows if r.distance_ok]
    print()
    print("SAFE READ")
    print(f"  sign-law pass rows: {len(sign_pass)}/{len(rows)}")
    print(f"  distance-law pass rows: {len(dist_pass)}/{len(rows)}")
    if dist_pass:
        best = min(dist_pass, key=lambda r: abs(r.alpha + 1.0))
        print(
            f"  best distance row: drift={best.drift:.2f}, seed={best.seed}, "
            f"alpha={best.alpha:.3f}, R2={best.r2:.3f}"
        )
        print(
            "  retained read: this oblique-strip family preserves both the signed-source package "
            "and the near-Newtonian distance tail on the sampled retained rows"
        )
    elif sign_pass:
        best = min(sign_pass, key=lambda r: abs((r.alpha if math.isfinite(r.alpha) else 1e9) + 1.0))
        print(
            f"  best sign-only row: drift={best.drift:.2f}, seed={best.seed}, "
            f"alpha={best.alpha:.3f}, R2={best.r2:.3f}, TOWARD={best.toward_count}/{len(DISTANCE_BS)}"
        )
        print(
            "  distance tail is the blocker: signed-source survives, but the near-Newtonian exponent "
            "does not hold on the oblique-strip slice"
        )
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  the oblique-strip rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
