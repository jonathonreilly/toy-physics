#!/usr/bin/env python3
"""Targeted complex-action probe for the sixth-family sheared-shell basin.

The scan starts from the retained sixth-family passing rows only. It keeps the
exact gamma=0 anchor explicit and checks whether a narrow TOWARD -> AWAY
companion survives on any row that already passed the exact zero/neutral and
weak-field sign-law gate.
"""

from __future__ import annotations

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

from SIXTH_FAMILY_SHEARED_SWEEP import (  # type: ignore
    BETA,
    Family,
    H,
    SHEAR_MAG,
    SHELL_COUNT,
    SOURCE_STRENGTH,
    SOURCE_Z,
    _build_sheared_shell_connectivity,
    _centroid_z,
    _field_from_sources,
)
from gate_b_no_restore_farfield import grow  # type: ignore


PASSING_ROWS = [
    (0.20, 2),
]
GAMMAS = [0.0, 0.1, 0.5]
SOURCE_STRENGTHS = [5e-6, 5e-5, 1e-4]


@dataclass(frozen=True)
class RowResult:
    drift: float
    seed: int
    sign_ok: bool
    born: float | None
    gamma0_delta: float | None
    delta_01: float | None
    delta_05: float | None
    escape_01: float | None
    escape_05: float | None
    fm_0: float | None
    fm_05: float | None
    toward_01: int
    toward_05: int

    @property
    def companion_ok(self) -> bool:
        return (
            self.sign_ok
            and self.born is not None
            and self.born < 1e-12
            and self.fm_0 is not None
            and self.fm_05 is not None
            and abs(self.fm_0 - 1.0) < 0.05
            and abs(self.fm_05 - 1.0) < 0.05
            and self.toward_01 > 0
            and self.toward_05 == 0
        )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    gamma: float,
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    h2 = H * H
    k = 5.0
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
            damp = 0.0 if decay < -50 else math.exp(min(decay, 50))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(k * act), math.sin(k * act)) * damp * w * h2 / (L * L)
    return amps


def _born_proxy(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layers: list[list[int]],
    field: list[float],
    gamma: float,
) -> float:
    det = layers[-1]

    def _p_born(open_slits: list[int]) -> float:
        n = len(pos)
        amps = [0j] * n
        source_layer = layers[0]
        for slit in open_slits:
            if slit < len(source_layer):
                amps[source_layer[slit]] = 1.0
        order = sorted(range(n), key=lambda i: pos[i][0])
        h2 = H * H
        k = 5.0
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
                damp = 0.0 if decay < -50 else math.exp(min(decay, 50))
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * complex(math.cos(k * act), math.sin(k * act)) * damp * w * h2 / (L * L)
        return _det_prob(amps, det)

    p123 = _p_born([0, 1, 2])
    p12 = _p_born([0, 1])
    p13 = _p_born([0, 2])
    p23 = _p_born([1, 2])
    p1 = _p_born([0])
    p2 = _p_born([1])
    p3 = _p_born([2])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-300)


def _det_prob(amps: list[complex], det: list[int]) -> float:
    return sum(abs(amps[i]) ** 2 for i in det)


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


def _sign_gate_row(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layers: list[list[int]],
) -> tuple[bool, float, float, float, float, float, float]:
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos), 0.0)
    z_free = _centroid_z(free, pos, det)
    p_free = _det_prob(free, det)
    field_plus = _field_from_sources(pos, layers, [(SOURCE_Z, +1)])
    field_minus = _field_from_sources(pos, layers, [(SOURCE_Z, -1)])
    field_neutral = _field_from_sources(pos, layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)])
    field_double = _field_from_sources(pos, layers, [(SOURCE_Z, +1), (SOURCE_Z, +1)])
    zero = _centroid_z(_propagate(pos, adj, [0.0] * len(pos), 0.0), pos, det) - z_free
    plus = _centroid_z(_propagate(pos, adj, field_plus, 0.0), pos, det) - z_free
    minus = _centroid_z(_propagate(pos, adj, field_minus, 0.0), pos, det) - z_free
    neutral = _centroid_z(_propagate(pos, adj, field_neutral, 0.0), pos, det) - z_free
    double = _centroid_z(_propagate(pos, adj, field_double, 0.0), pos, det) - z_free

    weak_deltas = []
    strengths = []
    for strength in SOURCE_STRENGTHS:
        field = [v * (strength / SOURCE_STRENGTH) for v in field_plus]
        z = _centroid_z(_propagate(pos, adj, field, 0.0), pos, det)
        delta = abs(z - z_free)
        if delta > 1e-15:
            weak_deltas.append(delta)
            strengths.append(strength)

    exponent = math.nan
    if len(weak_deltas) >= 2:
        lx = [math.log(s) for s in strengths]
        ly = [math.log(d) for d in weak_deltas]
        mx = sum(lx) / len(lx)
        my = sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        if sxx > 1e-12:
            exponent = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx

    ok = (
        abs(zero) < 1e-12
        and abs(neutral) < 1e-12
        and plus > 0.0
        and minus < 0.0
        and plus * minus < 0.0
        and abs(exponent - 1.0) < 0.05
    )
    return ok, zero, plus, minus, neutral, double, exponent


def _measure_row(drift: float, seed: int) -> RowResult:
    pos, _adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, _adj)
    sheared = _build_sheared_shell_connectivity(fam)
    det = sheared.layers[-1]
    free = _propagate(sheared.positions, sheared.adj, [0.0] * len(sheared.positions), 0.0)
    z_free = _centroid_z(free, sheared.positions, det)
    p_free = _det_prob(free, det)

    field = _field_from_sources(sheared.positions, sheared.layers, [(SOURCE_Z, +1)])
    gamma0_amps = _propagate(sheared.positions, sheared.adj, field, 0.0)
    gamma0_delta = _centroid_z(gamma0_amps, sheared.positions, det) - z_free

    born = _born_proxy(sheared.positions, sheared.adj, sheared.layers, field, 0.0)
    grav01 = _propagate(sheared.positions, sheared.adj, field, 0.1)
    grav05 = _propagate(sheared.positions, sheared.adj, field, 0.5)
    d01 = _centroid_z(grav01, sheared.positions, det) - z_free
    d05 = _centroid_z(grav05, sheared.positions, det) - z_free
    e01 = _det_prob(grav01, det) / p_free if p_free > 1e-30 else 0.0
    e05 = _det_prob(grav05, det) / p_free if p_free > 1e-30 else 0.0
    toward_01 = int(d01 > 0.0)
    toward_05 = int(d05 > 0.0)

    weak_0: list[float] = []
    weak_05: list[float] = []
    for strength in SOURCE_STRENGTHS:
        scaled = [v * (strength / SOURCE_STRENGTH) for v in field]
        amp0 = _propagate(sheared.positions, sheared.adj, scaled, 0.0)
        amp05 = _propagate(sheared.positions, sheared.adj, scaled, 0.5)
        weak_0.append(abs(_centroid_z(amp0, sheared.positions, det) - z_free))
        weak_05.append(abs(_centroid_z(amp05, sheared.positions, det) - z_free))
    s1, s2 = SOURCE_STRENGTHS[:2]
    fm0 = None
    fm05 = None
    if weak_0[0] > 1e-15 and weak_0[1] > 1e-15:
        fm0 = math.log(weak_0[1] / weak_0[0]) / math.log(s2 / s1)
    if weak_05[0] > 1e-15 and weak_05[1] > 1e-15:
        fm05 = math.log(weak_05[1] / weak_05[0]) / math.log(s2 / s1)

    return RowResult(
        drift=drift,
        seed=seed,
        sign_ok=True,
        born=born,
        gamma0_delta=gamma0_delta,
        delta_01=d01,
        delta_05=d05,
        escape_01=e01,
        escape_05=e05,
        fm_0=fm0,
        fm_05=fm05,
        toward_01=toward_01,
        toward_05=toward_05,
    )


def main() -> None:
    print("=" * 100)
    print("SIXTH FAMILY COMPLEX TARGETED")
    print("  complex-action companion probe on the parity-sheared shell basin")
    print("=" * 100)
    print(f"passing_rows={PASSING_ROWS}")
    print("guard: start from the sixth-family sign-law passing rows only")
    print("guard: exact gamma=0 anchor baseline and TOWARD -> AWAY crossover")
    print()
    print(
        f"{'drift':>5s} {'seed':>4s} {'sign':>4s} {'born':>10s} {'g0':>12s} "
        f"{'d01':>12s} {'d05':>12s} {'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} "
        f"{'t01':>5s} {'t05':>5s}"
    )
    print("-" * 124)

    rows: list[RowResult] = []
    for drift, seed in PASSING_ROWS:
        row = _measure_row(drift, seed)
        rows.append(row)
        sign = "YES" if row.sign_ok else "no"
        born = f"{row.born:.3e}" if row.born is not None else "   n/a"
        g0 = f"{row.gamma0_delta:+12.6e}" if row.gamma0_delta is not None else "      n/a"
        d01 = f"{row.delta_01:+12.6e}" if row.delta_01 is not None else "      n/a"
        d05 = f"{row.delta_05:+12.6e}" if row.delta_05 is not None else "      n/a"
        e01 = f"{row.escape_01:8.3f}" if row.escape_01 is not None else "     n/a"
        e05 = f"{row.escape_05:8.3f}" if row.escape_05 is not None else "     n/a"
        fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "   n/a"
        fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "   n/a"
        print(
            f"{drift:5.2f} {seed:4d} {sign:>4s} {born:>10s} {g0:>12s} "
            f"{d01:>12s} {d05:>12s} {e01:>8s} {e05:>8s} {fm0:>7s} {fm05:>7s} "
            f"{row.toward_01:5d} {row.toward_05:5d}"
        )

    retained = [r for r in rows if r.companion_ok]
    print()
    print("SAFE READ")
    sign_rows = [r for r in rows if r.sign_ok]
    print(f"  sign-law passing rows: {len(sign_rows)}/{len(rows)}")
    print(f"  retained complex companions: {len(retained)}")
    if retained:
        best = retained[0]
        print(
            f"  anchor retained row: drift={best.drift:.2f}, seed={best.seed}, "
            f"born={best.born:.3e}, g0={best.gamma0_delta:+.3e}"
        )
        print("  the sixth-family sheared basin carries a narrow complex-action companion")
    else:
        print("  no sign-law passing row retained a clean complex-action companion")
        print("  the sixth-family complex branch is a diagnosed boundary on this slice")


if __name__ == "__main__":
    main()
