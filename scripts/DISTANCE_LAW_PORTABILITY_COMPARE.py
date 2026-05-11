#!/usr/bin/env python3
"""Distance-law portability compare across retained structured families.

This runner asks a narrow question:

Can the retained near-Newtonian distance tail transfer beyond the first two
grown families into the newer retained structured families?

The claim surface is intentionally small:
- one representative retained row per family
- the same gravity-style source centroid observable used in the grown-geometry
  distance-law replay
- no universality claim beyond the tested rows
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gate_b_no_restore_farfield import grow
from ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP import _build_alt_connectivity
from THIRD_GROWN_FAMILY_SIGN_SWEEP import _build_third_connectivity
from FOURTH_FAMILY_QUADRANT_SWEEP import _build_quadrant_reflection_connectivity


H = 0.5
K = 5.0
BETA = 0.8
FIELD_STRENGTH = 0.004
SOURCE_BS = [5, 6, 7, 8, 10]


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


@dataclass(frozen=True)
class FamilyCase:
    label: str
    drift: float
    seed: int
    builder: Callable[[Family], Family]


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


def _source_field(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    z_src: float,
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = len(layers) // 2
    layer_nodes = layers[source_layer]
    centers = _layer_centers(pos, layers)
    cy, cz = centers[source_layer]

    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - pos[layer_nodes[0]][0]) ** 2 + (y - cy) ** 2 + (z - z_src) ** 2
        if d < best_d:
            best = idx
            best_d = d
    if best is None:
        return field

    mx, my, mz = pos[best]
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field[i] = FIELD_STRENGTH / r
    return field


def _radial_shell(y: float, z: float, cy: float, cz: float) -> int:
    radius = math.sqrt((y - cy) ** 2 + (z - cz) ** 2)
    shell = int(round(radius / 0.5))
    return max(0, min(7, shell))


def _neighbor_shell(shell: int, layer_idx: int) -> int:
    if layer_idx % 2 == 0:
        return min(7, shell + 1)
    return max(0, shell - 1)


def _build_radial_shell_connectivity(fam: Family) -> Family:
    pos = fam.positions
    layers = fam.layers
    centers = _layer_centers(pos, layers)
    adj = {i: [] for i in range(len(pos))}

    for layer_idx in range(len(layers) - 1):
        src_layer = layers[layer_idx]
        dst_layer = layers[layer_idx + 1]
        cy_src, cz_src = centers[layer_idx]
        cy_dst, cz_dst = centers[layer_idx + 1]
        dst_by_shell = {s: [] for s in range(8)}
        for dst in dst_layer:
            shell = _radial_shell(pos[dst][1], pos[dst][2], cy_dst, cz_dst)
            dst_by_shell[shell].append(dst)

        for src in src_layer:
            shell = _radial_shell(pos[src][1], pos[src][2], cy_src, cz_src)
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
                if len(chosen) >= 5:
                    break
                if dst not in chosen:
                    chosen.append(dst)
            adj[src].extend(chosen)
    return Family(pos, layers, adj)


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


def _measure_case(case: FamilyCase) -> dict[str, object]:
    pos, _adj, layers, _nmap = grow(case.drift, case.seed)
    fam = Family(pos, layers, {})
    tested = case.builder(fam)
    det = tested.layers[-1]

    free = _propagate(tested.positions, tested.adj, [0.0] * len(tested.positions))
    z_free = _centroid_z(free, tested.positions, det)

    deltas: list[float] = []
    directions: list[str] = []
    for b in SOURCE_BS:
        field = _source_field(tested.positions, tested.layers, float(b))
        amps = _propagate(tested.positions, tested.adj, field)
        delta = _centroid_z(amps, tested.positions, det) - z_free
        deltas.append(delta)
        directions.append("TOWARD" if delta > 0 else "AWAY")

    alpha, r2 = _fit_power(SOURCE_BS, deltas)
    toward = sum(1 for d in deltas if d > 0)
    return {
        "label": case.label,
        "drift": case.drift,
        "seed": case.seed,
        "deltas": deltas,
        "directions": directions,
        "alpha": alpha,
        "r2": r2,
        "toward": toward,
        "total": len(deltas),
        "all_toward": toward == len(deltas),
    }


def main() -> None:
    cases = [
        FamilyCase("alt-connectivity", 0.20, 0, _build_alt_connectivity),
        FamilyCase("third-family", 0.20, 2, _build_third_connectivity),
        FamilyCase("fourth-family", 0.00, 0, _build_quadrant_reflection_connectivity),
        FamilyCase("fifth-family", 0.05, 0, _build_radial_shell_connectivity),
    ]

    print("=" * 102)
    print("DISTANCE LAW PORTABILITY COMPARE")
    print("  gravity-style distance tail across retained structured families")
    print("=" * 102)
    print(f"source_b={SOURCE_BS}, field_strength={FIELD_STRENGTH}, k={K}, beta={BETA}")
    print()
    print(f"{'family':>18s} {'row':>10s} {'alpha':>8s} {'R^2':>7s} {'TOWARD':>8s} {'all+':>6s}")
    print("-" * 64)

    rows = []
    for case in cases:
        out = _measure_case(case)
        rows.append(out)
        row = f"({case.drift:.2f}, {case.seed})"
        alpha = out["alpha"]
        r2 = out["r2"]
        print(
            f"{out['label']:>18s} {row:>10s} "
            f"{alpha:8.3f} {r2:7.3f} {out['toward']:2d}/{out['total']:<5d} "
            f"{'YES' if out['all_toward'] else 'no':>6s}"
        )

    valid = [r for r in rows if not math.isnan(r["alpha"])]
    print()
    print("SAFE READ")
    if valid:
        mean_alpha = _mean([r["alpha"] for r in valid])
        spread = max(r["alpha"] for r in valid) - min(r["alpha"] for r in valid)
        print(f"  family count: {len(valid)}")
        print(f"  mean alpha among retained rows: {mean_alpha:.3f}")
        print(f"  alpha span across tested families: {spread:.3f}")
        if all(r["all_toward"] for r in valid):
            print("  all tested families stay TOWARD on the sampled impact-parameter rows")
            print("  distance-tail portability is retained across the tested family rows")
        else:
            failing = [r["label"] for r in valid if not r["all_toward"]]
            print(f"  boundary families with AWAY rows: {failing}")
            retained = [r["label"] for r in valid if r["all_toward"]]
            if retained:
                print(f"  retained family rows: {retained}")
            print("  distance-tail portability is only partial on this sweep")
    else:
        print("  no family produced a stable power-law fit")
        print("  the distance-tail portability claim is not retained on this sweep")

    # Bounded-table assertions tied to docs/DISTANCE_LAW_PORTABILITY_NOTE.md.
    # Tolerance: 0.01 absolute on alpha and R^2 (display precision).
    by_label = {r["label"]: r for r in rows}
    expected = {
        # label              alpha    R^2     toward
        "alt-connectivity":  (-0.952, 0.912, 0),
        "third-family":      (-2.161, 0.961, 0),
        "fourth-family":     (-1.190, 0.898, 0),
        "fifth-family":      (-0.313, 0.876, 5),
    }
    tol = 0.01
    for label, (alpha_e, r2_e, toward_e) in expected.items():
        r = by_label[label]
        assert abs(r["alpha"] - alpha_e) <= tol, (
            f"{label} alpha drift: got {r['alpha']:.3f}, expected {alpha_e}"
        )
        assert abs(r["r2"] - r2_e) <= tol, (
            f"{label} R^2 drift: got {r['r2']:.3f}, expected {r2_e}"
        )
        assert int(r["toward"]) == toward_e, (
            f"{label} TOWARD-count drift: got {r['toward']}, expected {toward_e}"
        )
        assert int(r["total"]) == 5, f"{label} sample count != 5"
    boundary = sorted(r["label"] for r in valid if not r["all_toward"])
    assert boundary == ["alt-connectivity", "fourth-family", "third-family"], (
        f"boundary-family set drift: got {boundary}"
    )
    all_toward_labels = [r["label"] for r in valid if r["all_toward"]]
    assert all_toward_labels == ["fifth-family"], (
        f"all-TOWARD family set drift: got {all_toward_labels}"
    )
    print(
        "PASS: bounded distance-law portability table matches the note "
        "(alpha and R^2 within 0.01; TOWARD counts and boundary family list pinned)."
    )


if __name__ == "__main__":
    raise SystemExit(main())
