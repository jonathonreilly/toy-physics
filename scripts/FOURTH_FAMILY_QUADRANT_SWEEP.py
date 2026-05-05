#!/usr/bin/env python3
"""Fourth-family scout: quadrant-reflection connectivity on the grown slice.

This is deliberately different from the earlier family lanes:
- not the original drift/restore family
- not the geometry-sector stencil family
- not the parity-rotated sector-transition family

The connectivity rule is quadrant-based rather than sector-based:
- partition each layer into four quadrants in the y/z plane
- connect to the nearest destination in the source quadrant
- add one parity-mirrored quadrant target
- keep a small structured fallback floor so the graph does not become sparse

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

The claim surface stays narrow:
- this is a fourth-family scout, not a geometry-generic theorem
- if it fails, the script should diagnose the structural miss instead of
  collapsing into vague "no-go" language
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
import argparse
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
DEFAULT_DRIFTS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
DEFAULT_SEEDS = [0, 1, 2, 3, 4]
QUICK_DRIFTS = [0.0, 0.20, 0.50]
QUICK_SEEDS = [0, 1, 2]
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
MIN_EDGES = 5


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


def _quadrant(y: float, z: float, cy: float, cz: float) -> tuple[int, int]:
    return (1 if y >= cy else -1, 1 if z >= cz else -1)


def _mirror_quadrant(q: tuple[int, int], layer_idx: int) -> tuple[int, int]:
    qy, qz = q
    if layer_idx % 2 == 0:
        return (-qy, qz)
    return (qy, -qz)


def _build_quadrant_reflection_connectivity(fam: Family) -> Family:
    """Build a quadrant-reflection connectivity family.

    Compared with the earlier sector-based family, this rule is:
    - quadrant-based, not angular-sector based
    - mirror-quadrant reflected, not parity-rotated sector shifted
    - still structured and sparse enough to remain reviewable
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

        dst_by_quad: dict[tuple[int, int], list[int]] = {
            (1, 1): [],
            (1, -1): [],
            (-1, 1): [],
            (-1, -1): [],
        }
        for dst in dst_layer:
            quad = _quadrant(pos[dst][1], pos[dst][2], cy_dst, cz_dst)
            dst_by_quad[quad].append(dst)

        for src in src_layer:
            quad = _quadrant(pos[src][1], pos[src][2], cy_src, cz_src)
            target_quads = [quad, _mirror_quadrant(quad, layer_idx)]

            chosen: list[int] = []
            for target in target_quads:
                candidates = dst_by_quad.get(target, [])
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


def _centroid_z(amps: list[complex], pos: list[tuple[float, float, float]], det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _evaluate_family(fam: Family) -> dict[str, float]:
    pos, layers, adj = fam.positions, fam.layers, fam.adj
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    cases = {
        "zero": [],
        "plus": [(SOURCE_Z, +1)],
        "minus": [(SOURCE_Z, -1)],
        "neutral": [(SOURCE_Z, +1), (SOURCE_Z, -1)],
        "double": [(SOURCE_Z, +2)],
    }
    out: dict[str, float] = {}
    for label, sources in cases.items():
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        out[label] = _centroid_z(amps, pos, det) - z_free
    out["alpha"] = (
        math.log(abs(out["double"] / out["plus"])) / math.log(2.0)
        if abs(out["plus"]) > 1e-30 and abs(out["double"]) > 1e-30
        else float("nan")
    )
    return out


def _print_case(name: str, out: dict[str, float]) -> None:
    print(name)
    print(f"  zero-source delta_z        {out['zero']:+.6e}")
    print(f"  single +1 delta_z          {out['plus']:+.6e}")
    print(f"  single -1 delta_z          {out['minus']:+.6e}")
    print(f"  neutral +1/-1 delta_z      {out['neutral']:+.6e}")
    print(f"  double +2 delta_z          {out['double']:+.6e}")
    print(f"  charge exponent            {out['alpha']:.6f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="run a smaller diagnostic sweep first",
    )
    parser.add_argument("--drifts", default="")
    parser.add_argument("--seeds", default="")
    args = parser.parse_args()

    if args.quick:
        drifts = QUICK_DRIFTS
        seeds = QUICK_SEEDS
    else:
        drifts = DEFAULT_DRIFTS
        seeds = DEFAULT_SEEDS
    if args.drifts:
        drifts = [float(part) for part in args.drifts.split(",") if part]
    if args.seeds:
        seeds = [int(part) for part in args.seeds.split(",") if part]

    print("=" * 94)
    print("FOURTH FAMILY QUADRANT SWEEP")
    print("  question: can a quadrant-reflection connectivity rule on the grown slice")
    print("  preserve the signed-source response in a retained way?")
    print("=" * 94)
    print(f"h={H}, NL={NL}, drifts={drifts}, seeds={seeds}")
    print(f"source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}, beta={BETA}, K={K}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'alpha':>8s}")
    print("-" * 94)

    rows: list[RowResult] = []
    for drift in drifts:
        for seed in seeds:
            pos, adj, layers, _nmap = grow(drift, seed)
            fam = Family(pos, layers, adj)
            quad_fam = _build_quadrant_reflection_connectivity(fam)
            out = _evaluate_family(quad_fam)
            row = RowResult(
                drift=drift,
                seed=seed,
                zero=out["zero"],
                plus=out["plus"],
                minus=out["minus"],
                neutral=out["neutral"],
                double=out["double"],
                exponent=out["alpha"],
            )
            rows.append(row)
            print(
                f"{drift:5.2f} {seed:4d} {row.zero:+12.6e} {row.plus:+12.6e} {row.minus:+12.6e} "
                f"{row.neutral:+12.6e} {row.double:+12.6e} {row.exponent:8.4f}"
            )

    print()
    print("SAFE READ")
    passing = [r for r in rows if r.ok]
    if passing:
        print(f"  passing rows: {len(passing)}/{len(rows)}")
        best = passing[0]
        print(
            f"  first passing row drift={best.drift:.2f}, seed={best.seed}, "
            f"alpha={best.exponent:.4f}"
        )
        print("  this fourth-family candidate retains a narrow signed-source basin")
    else:
        zeros = sum(abs(r.zero) < 1e-12 for r in rows)
        neutrals = sum(abs(r.neutral) < 1e-12 for r in rows)
        sign_ok = sum(r.plus > 0.0 and r.minus < 0.0 for r in rows)
        print("  no rows passed the full control gate")
        print(f"  zero-source controls passing: {zeros}/{len(rows)}")
        print(f"  neutral-cancellation controls passing: {neutrals}/{len(rows)}")
        print(f"  sign-orientation rows passing: {sign_ok}/{len(rows)}")
        print("  structural miss: quadrant-reflection does not retain the signed-source basin")


if __name__ == "__main__":
    main()
