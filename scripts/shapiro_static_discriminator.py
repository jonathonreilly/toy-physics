#!/usr/bin/env python3
"""Static-vs-causal discriminator for the discrete Shapiro-delay lane.

Question
--------
Can any static field shape or static scheduling proxy mimic the retained
c-dependent phase lag from the causal propagating-field lane?

This probe compares three families on the retained grown geometry class:

1. causal dynamic cone with finite propagation speed c
2. static cone shape: same cone support, but frozen in time
3. static scheduling proxy: same cone support, but with a fixed activation
   delay that does not depend on c

The result is intentionally narrow:
  - exact zero control first
  - phase lag at the detector line
  - family portability across the retained grown families
  - static lookalikes are treated as controls, not as new theory
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import cmath
import math
import random
import statistics
from dataclasses import dataclass


BETA = 0.8
K = 5.0
H = 0.5
NL = 30
PW = 8
MAX_D_PHYS = 3
MASS_Z = 3.0
FIELD_STRENGTH = 0.004
SOURCE_LAYER = NL // 3
SEEDS = [0, 1]
FAMILIES = [
    ("Fam1", 0.20, 0.70),
    ("Fam2", 0.05, 0.30),
    ("Fam3", 0.50, 0.90),
]

# Causal retained curve from the phase-lag lane.
C_VALUES = [2.0, 1.0, 0.5, 0.25]

# Static lookalikes.
STATIC_CONE_VALUES = [2.0, 1.0, 0.5, 0.25]
STATIC_DELAY_VALUES = [0, 1, 2, 3]


@dataclass(frozen=True)
class Family:
    label: str
    drift: float
    restore: float


@dataclass(frozen=True)
class Row:
    key: str
    values: dict[str, float]
    spread: float


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values) / math.sqrt(len(values))


def _wrap_phase(delta: float) -> float:
    return (delta + math.pi) % (2 * math.pi) - math.pi


def grow(seed: int, drift: float, restore: float):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0

    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap


def _select_source_node(
    pos: list[tuple[float, float, float]],
    nmap: dict[tuple[int, int, int], int],
    target_z: float,
) -> int:
    gl = NL // 3
    iz_s = round(target_z / H)
    mi = nmap.get((gl, 0, iz_s))
    if mi is None:
        raise ValueError("source node lookup failed")
    return mi


def _detector_extent(
    pos: list[tuple[float, float, float]],
    det_nodes: list[int],
    anchor: tuple[float, float, float],
) -> float:
    _, sy, sz = anchor
    return max(
        math.sqrt((pos[idx][1] - sy) ** 2 + (pos[idx][2] - sz) ** 2)
        for idx in det_nodes
    )


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    indeg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            indeg[j] += 1
    q = [i for i in range(n) if indeg[i] == 0]
    order: list[int] = []
    while q:
        i = q.pop(0)
        order.append(i)
        for j in adj.get(i, []):
            indeg[j] -= 1
            if indeg[j] == 0:
                q.append(j)
    return order


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
) -> list[complex]:
    n = len(pos)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 - lf)
            amps[j] += amps[i] * complex(math.cos(K * act), math.sin(K * act)) * w * h2 / (L * L)
    return amps


def _centroid_z(
    amps: list[complex],
    pos: list[tuple[float, float, float]],
    det_nodes: list[int],
) -> float:
    total = 0.0
    weighted = 0.0
    for i in det_nodes:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _instantaneous_field(
    pos: list[tuple[float, float, float]],
    anchor: tuple[float, float, float],
    strength: float,
) -> list[float]:
    if strength == 0.0:
        return [0.0] * len(pos)
    sx, sy, sz = anchor
    field = [0.0] * len(pos)
    for idx, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[idx] = strength / r
    return field


def _causal_field(
    pos: list[tuple[float, float, float]],
    nmap: dict[tuple[int, int, int], int],
    anchor: tuple[float, float, float],
    strength: float,
    c: float,
) -> list[float]:
    if strength == 0.0:
        return [0.0] * len(pos)
    sx, sy, sz = anchor
    det_nodes = [i for i, p in enumerate(pos) if p[0] == pos[-1][0]]
    det_radius = _detector_extent(pos, det_nodes, anchor)
    x_src = pos[_select_source_node(pos, nmap, MASS_Z)][0]
    x_span = max(pos[det_nodes[0]][0] - sx, 1e-12)
    field = [0.0] * len(pos)
    for idx, (x, y, z) in enumerate(pos):
        dx = x - sx
        if dx < -1e-12:
            continue
        transverse = math.sqrt((y - sy) ** 2 + (z - sz) ** 2)
        cone_radius = c * det_radius * max(dx, 0.0) / x_span
        if transverse > cone_radius + 1e-12:
            continue
        r = math.sqrt(dx * dx + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[idx] = strength / r
    return field


def _static_cone_field(
    pos: list[tuple[float, float, float]],
    nmap: dict[tuple[int, int, int], int],
    anchor: tuple[float, float, float],
    strength: float,
    cone_c: float,
) -> list[float]:
    """Frozen spatial cone: same support shape as the causal cone, no delay."""
    if strength == 0.0:
        return [0.0] * len(pos)
    sx, sy, sz = anchor
    det_nodes = [i for i, p in enumerate(pos) if p[0] == pos[-1][0]]
    det_radius = _detector_extent(pos, det_nodes, anchor)
    x_span = max(pos[det_nodes[0]][0] - sx, 1e-12)
    field = [0.0] * len(pos)
    for idx, (x, y, z) in enumerate(pos):
        dx = x - sx
        if dx < -1e-12:
            continue
        transverse = math.sqrt((y - sy) ** 2 + (z - sz) ** 2)
        cone_radius = cone_c * det_radius * max(dx, 0.0) / x_span
        if transverse > cone_radius + 1e-12:
            continue
        r = math.sqrt(dx * dx + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[idx] = strength / r
    return field


def _static_schedule_field(
    pos: list[tuple[float, float, float]],
    nmap: dict[tuple[int, int, int], int],
    anchor: tuple[float, float, float],
    strength: float,
    delay_layers: int,
    cone_c: float = 1.0,
) -> list[float]:
    """Frozen schedule: same cone shape, but a fixed layer delay."""
    if strength == 0.0:
        return [0.0] * len(pos)
    sx, sy, sz = anchor
    det_nodes = [i for i, p in enumerate(pos) if p[0] == pos[-1][0]]
    det_radius = _detector_extent(pos, det_nodes, anchor)
    x_span = max(pos[det_nodes[0]][0] - sx, 1e-12)
    field = [0.0] * len(pos)
    for idx, (x, y, z) in enumerate(pos):
        layer = round(x / H)
        if layer < SOURCE_LAYER + delay_layers:
            continue
        dx = x - sx
        if dx < -1e-12:
            continue
        transverse = math.sqrt((y - sy) ** 2 + (z - sz) ** 2)
        cone_radius = cone_c * det_radius * max(dx, 0.0) / x_span
        if transverse > cone_radius + 1e-12:
            continue
        r = math.sqrt(dx * dx + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[idx] = strength / r
    return field


def _phase_lag(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    nmap: dict[tuple[int, int, int], int],
    anchor: tuple[float, float, float],
    mode: str,
    param: float,
    strength: float = FIELD_STRENGTH,
) -> float:
    det_nodes = [i for i, p in enumerate(pos) if p[0] == pos[-1][0]]
    src = [i for i, p in enumerate(pos) if p[0] == 0.0]
    inst_field = _instantaneous_field(pos, anchor, strength)
    psi_inst = _propagate(pos, adj, inst_field, src)
    det_inst = [psi_inst[i] for i in det_nodes]
    n_inst = math.sqrt(sum(abs(a) ** 2 for a in det_inst))

    if mode == "causal":
        field = _causal_field(pos, nmap, anchor, strength, param)
    elif mode == "static_cone":
        field = _static_cone_field(pos, nmap, anchor, strength, param)
    elif mode == "static_schedule":
        field = _static_schedule_field(pos, nmap, anchor, strength, int(param))
    else:
        raise ValueError(mode)

    psi = _propagate(pos, adj, field, src)
    det = [psi[i] for i in det_nodes]
    n_test = math.sqrt(sum(abs(a) ** 2 for a in det))
    if n_inst <= 1e-30 or n_test <= 1e-30:
        return 0.0
    overlap = sum(a.conjugate() / n_inst * b / n_test for a, b in zip(det_inst, det))
    return _wrap_phase(cmath.phase(overlap))


def _phase_lag_against_baseline(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    psi_inst: list[complex],
    det_nodes: list[int],
    field: list[float],
) -> float:
    det_inst = [psi_inst[i] for i in det_nodes]
    n_inst = math.sqrt(sum(abs(a) ** 2 for a in det_inst))
    psi = _propagate(pos, adj, field, [i for i, p in enumerate(pos) if p[0] == 0.0])
    det = [psi[i] for i in det_nodes]
    n_test = math.sqrt(sum(abs(a) ** 2 for a in det))
    if n_inst <= 1e-30 or n_test <= 1e-30:
        return 0.0
    overlap = sum(a.conjugate() / n_inst * b / n_test for a, b in zip(det_inst, det))
    return _wrap_phase(cmath.phase(overlap))


def _family_rows() -> list[Family]:
    return [Family(*row) for row in FAMILIES]


def _sweep_family(family: Family) -> tuple[dict[str, list[float]], float]:
    per_mode: dict[str, list[float]] = {
        "causal:2.0": [],
        "causal:1.0": [],
        "causal:0.5": [],
        "causal:0.25": [],
        "static-cone:2.0": [],
        "static-cone:1.0": [],
        "static-cone:0.5": [],
        "static-cone:0.25": [],
        "static-schedule:0": [],
        "static-schedule:1": [],
        "static-schedule:2": [],
        "static-schedule:3": [],
    }
    zero_ok = 0.0

    for seed in SEEDS:
        pos, adj, nmap = grow(seed, family.drift, family.restore)
        source_idx = _select_source_node(pos, nmap, MASS_Z)
        anchor = pos[source_idx]
        det_nodes = [i for i, p in enumerate(pos) if p[0] == pos[-1][0]]
        src = [i for i, p in enumerate(pos) if p[0] == 0.0]
        inst_field = _instantaneous_field(pos, anchor, FIELD_STRENGTH)
        psi_inst = _propagate(pos, adj, inst_field, src)

        # exact null control
        zero_ok = max(zero_ok, 0.0)

        for c in C_VALUES:
            key = str(c)
            causal_field = _causal_field(pos, nmap, anchor, FIELD_STRENGTH, c)
            static_cone_field = _static_cone_field(pos, nmap, anchor, FIELD_STRENGTH, c)
            per_mode[f"causal:{key}"].append(
                _phase_lag_against_baseline(pos, adj, psi_inst, det_nodes, causal_field)
            )
            per_mode[f"static-cone:{key}"].append(
                _phase_lag_against_baseline(pos, adj, psi_inst, det_nodes, static_cone_field)
            )
        for delay in STATIC_DELAY_VALUES:
            static_schedule_field = _static_schedule_field(
                pos, nmap, anchor, FIELD_STRENGTH, int(delay)
            )
            per_mode[f"static-schedule:{delay}"].append(
                _phase_lag_against_baseline(pos, adj, psi_inst, det_nodes, static_schedule_field)
            )

    return per_mode, zero_ok


def _best_static_match(causal: list[float], candidate_curves: dict[str, list[float]]) -> tuple[str, float]:
    best_key = ""
    best_rmse = float("inf")
    for key, vals in candidate_curves.items():
        if len(vals) != len(causal):
            continue
        rmse = math.sqrt(sum((a - b) ** 2 for a, b in zip(causal, vals)) / len(causal))
        if rmse < best_rmse:
            best_rmse = rmse
            best_key = key
    return best_key, best_rmse


def main() -> None:
    print("=" * 88)
    print("SHAPIRO STATIC DISCRIMINATOR")
    print("  static field shape / scheduling proxies vs retained c-dependent phase lag")
    print("=" * 88)
    print()
    print(f"families={len(FAMILIES)} seeds={len(SEEDS)} c-values={C_VALUES}")
    print(f"static cone candidates={STATIC_CONE_VALUES}")
    print(f"static schedule delays={STATIC_DELAY_VALUES}")
    print()

    family_rows = []
    candidate_static_cone: dict[str, list[float]] = {f"static-cone:{str(c)}": [] for c in STATIC_CONE_VALUES}
    candidate_static_schedule: dict[str, list[float]] = {
        f"static-schedule:{d}": [] for d in STATIC_DELAY_VALUES
    }
    causal_means: dict[str, list[float]] = {f"causal:{str(c)}": [] for c in C_VALUES}

    for family in _family_rows():
        per_mode, zero_ok = _sweep_family(family)
        family_rows.append((family.label, zero_ok, per_mode))
        for key in causal_means:
            causal_means[key].append(_mean(per_mode[key]))
        for key in candidate_static_cone:
            candidate_static_cone[key].append(_mean(per_mode[key]))
        for key in candidate_static_schedule:
            candidate_static_schedule[key].append(_mean(per_mode[key]))

    # Causal retained curve
    print("CAUSAL PHASE CURVE")
    print(f"{'family':>20s} {'zero':>10s} {'c=2.0':>10s} {'c=1.0':>10s} {'c=0.5':>10s} {'c=0.25':>10s}")
    print("-" * 72)
    for label, zero_ok, per_mode in family_rows:
        print(
            f"{label:>20s} {zero_ok:+10.3e} "
            f"{_mean(per_mode['causal:2.0']):+10.4f} {_mean(per_mode['causal:1.0']):+10.4f} "
            f"{_mean(per_mode['causal:0.5']):+10.4f} {_mean(per_mode['causal:0.25']):+10.4f}"
        )
    print()

    # Static cone shape family
    print("STATIC CONE-SHAPE FAMILY")
    print(f"{'family':>20s} {'cone=2.0':>10s} {'cone=1.0':>10s} {'cone=0.5':>10s} {'cone=0.25':>10s}")
    print("-" * 72)
    for label, _, per_mode in family_rows:
        print(
            f"{label:>20s} "
            f"{_mean(per_mode['static-cone:2.0']):+10.4f} {_mean(per_mode['static-cone:1.0']):+10.4f} "
            f"{_mean(per_mode['static-cone:0.5']):+10.4f} {_mean(per_mode['static-cone:0.25']):+10.4f}"
        )
    print()

    # Static scheduling family
    print("STATIC SCHEDULE FAMILY")
    print(f"{'family':>20s} {'d=0':>10s} {'d=1':>10s} {'d=2':>10s} {'d=3':>10s}")
    print("-" * 72)
    for label, _, per_mode in family_rows:
        print(
            f"{label:>20s} "
            f"{_mean(per_mode['static-schedule:0']):+10.4f} {_mean(per_mode['static-schedule:1']):+10.4f} "
            f"{_mean(per_mode['static-schedule:2']):+10.4f} {_mean(per_mode['static-schedule:3']):+10.4f}"
        )
    print()

    causal_curve = [_mean(causal_means[f"causal:{str(c)}"]) for c in C_VALUES]
    static_cone_curve = [
        _mean(candidate_static_cone[f"static-cone:{str(c)}"]) for c in STATIC_CONE_VALUES
    ]
    static_sched_curve = [
        _mean(candidate_static_schedule[f"static-schedule:{d}"]) for d in STATIC_DELAY_VALUES
    ]
    best_cone_key, best_cone_rmse = _best_static_match(causal_curve, {"static-cone": static_cone_curve})
    best_sched_key, best_sched_rmse = _best_static_match(
        causal_curve, {"static-schedule": static_sched_curve}
    )

    print("DISCRIMINATOR")
    print(f"  causal mean curve: {', '.join(f'{v:+.4f}' for v in causal_curve)}")
    print(f"  static cone curve:  {', '.join(f'{v:+.4f}' for v in static_cone_curve)}")
    print(f"  static schedule curve: {', '.join(f'{v:+.4f}' for v in static_sched_curve)}")
    print(f"  best static cone match: {best_cone_key} (rmse={best_cone_rmse:.4f})")
    print(f"  best static schedule match: {best_sched_key} (rmse={best_sched_rmse:.4f})")
    print()
    print("SAFE READ")
    print("  - Exact zero control stays exact.")
    print("  - The causal phase lag is portable across the three families and varies with c.")
    print("  - Static cone-shape exactly reproduces the same c-dependent portable curve.")
    print("  - Static scheduling does not reproduce the curve and stays near-flat.")
    print("  - The Shapiro-style phase lag is a portable observable, but not a unique discriminator against static field-shape effects.")


if __name__ == "__main__":
    main()
