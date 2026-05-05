#!/usr/bin/env python3
"""Bounded impact-parameter lensing probe on the strongest portable grown rows.

Question
--------
Does the detector centroid shift support a stable impact-parameter law on the
strongest portable grown families?

This stays deliberately narrow:
  - exact/null control first
  - same graph per seed for each row
  - fixed mass count and fixed source layer
  - one retained b sweep shared across rows
  - only the strongest portable grown rows are tested

The readout is the same detector-line centroid shift used by the retained
grown-geometry distance-law replay, but organized as an explicit lensing
probe.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import random
import time
from dataclasses import dataclass


BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 40
PW = 12
FIELD_STRENGTH = 0.004
SEEDS = [0, 1, 2]
B_VALUES = [5, 6, 7, 8, 10]
NULL_B = 8


@dataclass(frozen=True)
class FamilyCase:
    label: str
    drift: float
    restore: float


@dataclass(frozen=True)
class FamilySummary:
    label: str
    null_delta: float
    toward: int
    total: int
    alpha: float | None
    r2: float | None
    peak_b: int | None


FAMILIES = [
    FamilyCase("grown family 1", 0.20, 0.70),
]


def grow(drift: float, restore: float, seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0.0, drift * H)
                    z = pz + rng.gauss(0.0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def make_field(
    pos: list[tuple[float, float, float]],
    nmap: dict[tuple[int, int, int], int],
    strength: float,
    z_src: float,
) -> list[float]:
    field = [0.0] * len(pos)
    gl = NL // 2
    iz_src = round(z_src / H)
    source_idx = nmap.get((gl, 0, iz_src))
    if source_idx is None:
        return field

    mx, my, mz = pos[source_idx]
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field[i] = strength / r
    return field


def propagate(
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


def centroid_z(
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


def fit_power_law(bs: list[int], deltas: list[float]) -> tuple[float, float] | None:
    pairs = [(float(b), abs(d)) for b, d in zip(bs, deltas) if b > 0 and abs(d) > 1e-30]
    if len(pairs) < 3:
        return None
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((x - xbar) ** 2 for x in xs)
    if sxx < 1e-12:
        return None
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    alpha = sxy / sxx
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - (ybar + alpha * (x - xbar))) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return alpha, r2


def _run_row(case: FamilyCase) -> tuple[list[float], float, int, int, list[float]]:
    by_b: dict[int, list[float]] = {b: [] for b in B_VALUES}
    null_vals: list[float] = []
    toward = 0
    total = 0

    for seed in SEEDS:
        pos, adj, layers, nmap = grow(case.drift, case.restore, seed)
        det = layers[-1]

        free = propagate(pos, adj, [0.0] * len(pos))
        z_free = centroid_z(free, pos, det)

        null_field = make_field(pos, nmap, 0.0, float(NULL_B))
        null_grav = propagate(pos, adj, null_field)
        null_vals.append(centroid_z(null_grav, pos, det) - z_free)

        for b in B_VALUES:
            field = make_field(pos, nmap, FIELD_STRENGTH, float(b))
            grav = propagate(pos, adj, field)
            delta = centroid_z(grav, pos, det) - z_free
            by_b[b].append(delta)
            total += 1
            if delta > 0:
                toward += 1

    means = [sum(by_b[b]) / len(by_b[b]) for b in B_VALUES]
    null_delta = sum(null_vals) / len(null_vals) if null_vals else 0.0
    return means, null_delta, toward, total, null_vals


def _print_row(case: FamilyCase) -> FamilySummary:
    means, null_delta, toward, total, null_vals = _run_row(case)
    fit = fit_power_law(B_VALUES, means)
    alpha = fit[0] if fit is not None else None
    r2 = fit[1] if fit is not None else None
    peak_b = B_VALUES[max(range(len(means)), key=lambda i: means[i])] if means else None

    print(f"{case.label}")
    print(f"  null control @ b={NULL_B}: delta={null_delta:+.6e}")
    print(f"  {'b':>4s}  {'delta':>12s}  {'delta*b':>10s}  {'delta*b^2':>11s}  {'dir':>8s}")
    print(f"  {'-' * 52}")
    for b, delta in zip(B_VALUES, means):
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {b:4d}  {delta:+12.6e}  {delta * b:+10.4f}  {delta * b * b:+11.4f}  {direction:>8s}")
    if alpha is not None and r2 is not None:
        print(f"  fit: delta ~= C * b^{alpha:.3f}  (R^2={r2:.3f})")
    else:
        print("  fit: unavailable")
    print()
    return FamilySummary(
        label=case.label,
        null_delta=null_delta,
        toward=toward,
        total=total,
        alpha=alpha,
        r2=r2,
        peak_b=peak_b,
    )


def main() -> None:
    print("=" * 92)
    print("IMPACT-PARAMETER LENSING PROBE")
    print("  exact/null control first; strongest portable grown rows only")
    print("=" * 92)
    print(f"seed rows={SEEDS}, b sweep={B_VALUES}, field={FIELD_STRENGTH}, k={K}, h={H}")
    print()

    summaries: list[FamilySummary] = []
    for case in FAMILIES:
        summaries.append(_print_row(case))

    print("=" * 92)
    print("SAFE READ")
    if summaries and all(abs(row.null_delta) < 1e-12 for row in summaries):
        print("  exact/null controls are clean on the tested portable grown rows")
    else:
        print("  exact/null control is not clean enough to trust the sweep")

    finite = [row for row in summaries if row.alpha is not None]
    if len(finite) >= 2:
        alphas = [row.alpha for row in finite if row.alpha is not None]
        span = max(alphas) - min(alphas)
        print(f"  retained alpha span across the grown rows: {span:.3f}")

    retained = [
        row for row in summaries
        if row.alpha is not None
        and abs(row.alpha + 1.0) < 0.3
        and row.toward == row.total
    ]
    if retained:
        labels = ", ".join(row.label for row in retained)
        print(f"  retained law: {labels}")
        print("  the centroid readout supports a stable impact-parameter law on the strongest portable grown rows")
    else:
        print("  closure: the centroid readout does not support a stable impact-parameter law on the tested portable grown rows")
    print("=" * 92)


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"\nTotal time: {time.time() - t0:.0f}s")
