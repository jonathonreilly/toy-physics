#!/usr/bin/env python3
"""Connectivity family v2: parity-tapered elliptical-shell sweep.

This tests a distinct structured connectivity family on the no-restore grown
slice. It is intentionally not the current sector-transition family and it is
not the earlier radial fifth-family slice.

Family idea:
- partition each layer into tapered elliptical shells in the y/z plane
- parity swap the shell metric so successive layers use different axis
  emphasis
- connect each source node to the nearest destination in its own shell and
  one neighboring shell chosen by layer parity
- keep a small fallback floor so the rule stays structured instead of sparse

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

If this family fails, we freeze the failure mechanism rather than broadening
the claim surface.
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

from gate_b_no_restore_farfield import grow


H = 0.5
NL = 25
DRIFTS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
SEEDS = [0, 1, 2, 3, 4]
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
MIN_EDGES = 5
SHELL_COUNT = 8


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

    @property
    def ok(self) -> bool:
        return (
            abs(self.zero) < 1e-12
            and abs(self.neutral) < 1e-12
            and self.plus > 0.0
            and self.minus < 0.0
            and self.plus * self.minus < 0.0
            and abs(self.exponent - 1.0) < 0.05
        )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _layer_centers(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
) -> list[tuple[float, float]]:
    centers = []
    for layer in layers:
        ys = [pos[i][1] for i in layer]
        zs = [pos[i][2] for i in layer]
        centers.append((sum(ys) / len(ys), sum(zs) / len(zs)))
    return centers


def _radial_shell(y: float, z: float, cy: float, cz: float) -> int:
    radius = math.sqrt((y - cy) ** 2 + (z - cz) ** 2)
    shell = int(round(radius / H))
    return max(0, min(SHELL_COUNT - 1, shell))


def _neighbor_shell(shell: int, layer_idx: int) -> int:
    if layer_idx % 2 == 0:
        return min(SHELL_COUNT - 1, shell + 1)
    return max(0, shell - 1)


def _layer_axes(layer_idx: int, pos: list[tuple[float, float, float]], layer: list[int]) -> tuple[float, float]:
    ys = [abs(pos[i][1]) for i in layer]
    zs = [abs(pos[i][2]) for i in layer]
    span_y = max(max(ys) - min(ys), H)
    span_z = max(max(zs) - min(zs), H)
    if layer_idx % 2 == 0:
        return (span_y, 0.75 * span_z + 0.25 * H)
    return (0.75 * span_y + 0.25 * H, span_z)


def _elliptical_shell(
    y: float,
    z: float,
    cy: float,
    cz: float,
    ay: float,
    az: float,
) -> int:
    radius = math.sqrt(((y - cy) / max(ay, H)) ** 2 + ((z - cz) / max(az, H)) ** 2)
    shell = int(round(radius * (SHELL_COUNT - 1)))
    return max(0, min(SHELL_COUNT - 1, shell))


def _build_elliptical_shell_connectivity(fam: Family) -> Family:
    """Build a parity-tapered elliptical-shell connectivity family.

    This rule is intentionally different from:
    - the sector-transition family
    - the quadrant-reflection family
    - the earlier radial fifth-family slice

    The shell metric is stretched differently on alternating layers, so the
    destination selection is still structured but not a pure radial relabeling.
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
        ay_src, az_src = _layer_axes(layer_idx, pos, src_layer)
        ay_dst, az_dst = _layer_axes(layer_idx + 1, pos, dst_layer)

        dst_by_shell: dict[int, list[int]] = {s: [] for s in range(SHELL_COUNT)}
        for dst in dst_layer:
            shell = _elliptical_shell(pos[dst][1], pos[dst][2], cy_dst, cz_dst, ay_dst, az_dst)
            dst_by_shell[shell].append(dst)

        for src in src_layer:
            shell = _elliptical_shell(pos[src][1], pos[src][2], cy_src, cz_src, ay_src, az_src)
            target_shells = [shell, _neighbor_shell(shell, layer_idx)]

            chosen: list[int] = []
            for target in target_shells:
                candidates = dst_by_shell.get(target, [])
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
            act = L * (1.0 + lf)
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


def _measure_family(pos: list[tuple[float, float, float]], adj: dict[int, list[int]], layers: list[list[int]]) -> RowResult:
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        return _centroid_z(amps, pos, det) - z_free

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
    return RowResult(
        drift=float("nan"),
        seed=-1,
        zero=zero,
        plus=plus,
        minus=minus,
        neutral=neutral,
        double=double,
        exponent=exponent,
    )


def main() -> None:
    print("=" * 96)
    print("CONNECTIVITY FAMILY V2 ELLIPTICAL SWEEP")
    print("  parity-tapered elliptical-shell family on the no-restore grown slice")
    print("=" * 96)
    print(f"h={H}, NL={NL}, drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation")
    print()

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            pos, adj, layers, _nmap = grow(drift, seed)
            fam = Family(pos, layers, adj)
            elliptical = _build_elliptical_shell_connectivity(fam)
            out = _measure_family(elliptical.positions, elliptical.adj, elliptical.layers)
            rows.append(
                RowResult(
                    drift=drift,
                    seed=seed,
                    zero=out.zero,
                    plus=out.plus,
                    minus=out.minus,
                    neutral=out.neutral,
                    double=out.double,
                    exponent=out.exponent,
                )
            )

    print(
        f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} "
        f"{'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}"
    )
    print("-" * 96)
    for r in rows:
        print(
            f"{r.drift:5.2f} {r.seed:4d} "
            f"{r.zero:+12.3e} {r.plus:+12.3e} {r.minus:+12.3e} "
            f"{r.neutral:+12.3e} {r.double:+12.3e} {r.exponent:7.3f} "
            f"{'YES' if r.ok else 'no':>4s}"
        )

    passed = [r for r in rows if r.ok]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r.drift for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean exponent among passes: {_mean([r.exponent for r in passed]):.6f}")
        print("  this family reproduces the portable sign-law fixed point on a narrow slice")
        print("  it does not broaden the retained family set")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  the elliptical-shell rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
