#!/usr/bin/env python3
"""Narrow basin sweep around the retained grown-row positives.

This script checks whether the retained moderate-drift grown-row positives
survive on a small neighborhood of nearby grown rows without broadening the
claim surface too far.

Two retained observables are checked:

1. fixed-field signed-source transfer
2. exact-lattice complex-action carryover on grown geometry

The basin is intentionally small:
- drift in {0.15, 0.20, 0.25}
- restore in {0.60, 0.70, 0.80}
"""

from __future__ import annotations

import cmath
import math
import os
import random
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
PW = 8
MAX_D_PHYS = 3
SEEDS = [0, 1, 2]
SOURCE_Z = 3.0
OFFSET = 1.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
GAMMAS = [0.0, 0.1, 0.2, 0.5, 1.0]
DRIFTS = [0.15, 0.20, 0.25]
RESTORES = [0.60, 0.70, 0.80]


@dataclass(frozen=True)
class BasinRow:
    drift: float
    restore: float
    signed_zero: float
    signed_single: float
    signed_neutral: float
    signed_exponent: float
    action_gamma0: float
    action_fm0: float
    action_fm05: float
    action_toward: tuple[int, int]


def _nearest_node_in_layer(pos, layer_nodes, x_target, y_target, z_target):
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _source_node(pos, layers, z_phys: float):
    source_layer = NL // 3
    x_target = source_layer * H
    return _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)


def _field_from_sources(pos, layers, sources):
    field = [0.0] * len(pos)
    for z_phys, charge in sources:
        node = _source_node(pos, layers, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate_sign(pos, adj, field):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
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
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 + lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def _propagate_complex(pos, adj, field, gamma):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
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
            lf = 0.5 * (field[i] + field[j])
            s_real = L * (1.0 - lf)
            s_imag = gamma * L * lf
            phase = K * s_real
            decay = -K * s_imag
            if decay < -50:
                amp_factor = 0.0
            elif decay > 50:
                amp_factor = math.exp(50)
            else:
                amp_factor = math.exp(decay)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * amp_factor * w * hm / (L * L)
    return amps


def _detector(layers):
    return layers[-1]


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _mean(values):
    return sum(values) / len(values) if values else math.nan


def _fit_power(xs, ys):
    if len(xs) < 3:
        return math.nan
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _measure_signed_source(pos, adj, layers):
    det = _detector(layers)
    free = _propagate_sign(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    zero_field = _field_from_sources(pos, layers, [])
    zero = _propagate_sign(pos, adj, zero_field)
    zero_delta = _centroid_z(zero, pos, det) - z_free

    neutral_field = _field_from_sources(pos, layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)])
    neutral = _propagate_sign(pos, adj, neutral_field)
    neutral_delta = _centroid_z(neutral, pos, det) - z_free

    plus_vals = []
    minus_vals = []
    double_vals = []
    for s in [1, 2]:
        pass
    for charge, bucket in [((SOURCE_Z, +1), plus_vals), ((SOURCE_Z, -1), minus_vals), ((SOURCE_Z, +2), double_vals)]:
        field = _field_from_sources(pos, layers, [charge])
        amps = _propagate_sign(pos, adj, field)
        bucket.append(_centroid_z(amps, pos, det) - z_free)

    field_plus = _field_from_sources(pos, layers, [(SOURCE_Z, +1)])
    field_double = _field_from_sources(pos, layers, [(SOURCE_Z, +2)])
    delta_plus = plus_vals[0]
    delta_double = double_vals[0]
    exponent = math.log(abs(delta_double / delta_plus)) / math.log(2.0) if abs(delta_plus) > 1e-30 else math.nan

    return zero_delta, neutral_delta, delta_plus, minus_vals[0], delta_double, exponent


def _measure_complex_action(pos, adj, layers):
    det = _detector(layers)
    field = _field_from_sources(pos, layers, [(SOURCE_Z, +1)])
    free0 = _propagate_complex(pos, adj, [0.0] * len(pos), 0.0)
    z_free = _centroid_z(free0, pos, det)

    gamma0 = _propagate_complex(pos, adj, field, 0.0)
    gamma0_delta = _centroid_z(gamma0, pos, det) - z_free

    deflection = {}
    fm_exp = {}
    toward = {}
    for gamma in GAMMAS:
        free = _propagate_complex(pos, adj, [0.0] * len(pos), gamma)
        grav = _propagate_complex(pos, adj, field, gamma)
        zf = _centroid_z(free, pos, det)
        zg = _centroid_z(grav, pos, det)
        delta = zg - zf
        toward[gamma] = 1 if delta > 0 else 0
        deflection[gamma] = delta

        field2 = _field_from_sources(pos, layers, [(SOURCE_Z, 0.5)])
        grav2 = _propagate_complex(pos, adj, field2, gamma)
        z2 = _centroid_z(grav2, pos, det)
        d2 = z2 - zf
        ratio = abs(delta) / abs(d2) if abs(d2) > 1e-30 else math.nan
        fm_exp[gamma] = math.log(ratio, 2.0) if ratio > 0 and math.isfinite(ratio) else math.nan

    fm0 = fm_exp[0.0]
    fm05 = fm_exp[0.5]
    toward_transition = (toward[0.0], toward[0.5])
    return gamma0_delta, fm0, fm05, toward_transition, deflection


def _score_row(drift: float, restore: float):
    signed_zero_vals = []
    signed_neutral_vals = []
    signed_plus_vals = []
    signed_minus_vals = []
    signed_double_vals = []
    signed_exp_vals = []

    action_gamma0_vals = []
    action_fm0_vals = []
    action_fm05_vals = []
    action_toward = [0, 0]
    action_deflections = {g: [] for g in GAMMAS}

    for seed in SEEDS:
        pos, adj, layers = grow(drift, restore, seed)
        z0, zn, zp, zm, zd, expn = _measure_signed_source(pos, adj, layers)
        signed_zero_vals.append(z0)
        signed_neutral_vals.append(zn)
        signed_plus_vals.append(zp)
        signed_minus_vals.append(zm)
        signed_double_vals.append(zd)
        signed_exp_vals.append(expn)

        g0, fm0, fm05, toward_transition, deflection = _measure_complex_action(pos, adj, layers)
        action_gamma0_vals.append(g0)
        action_fm0_vals.append(fm0)
        action_fm05_vals.append(fm05)
        action_toward[0] += toward_transition[0]
        action_toward[1] += toward_transition[1]
        for g, val in deflection.items():
            action_deflections[g].append(val)

    return BasinRow(
        drift=drift,
        restore=restore,
        signed_zero=_mean(signed_zero_vals),
        signed_single=_mean(signed_plus_vals),
        signed_neutral=_mean(signed_neutral_vals),
        signed_exponent=_mean(signed_exp_vals),
        action_gamma0=_mean(action_gamma0_vals),
        action_fm0=_mean(action_fm0_vals),
        action_fm05=_mean(action_fm05_vals),
        action_toward=(action_toward[0], action_toward[1]),
    )


def main() -> None:
    print("=" * 100)
    print("GROWN TRANSFER BASIN SWEEP")
    print("  narrow basin around the retained grown-row positives")
    print("=" * 100)
    print(f"Seeds: {SEEDS}")
    print(f"Drifts: {DRIFTS}")
    print(f"Restores: {RESTORES}")
    print()
    print(
        f"{'drift':>5s} {'restore':>7s} {'zero':>12s} {'neutral':>12s} "
        f"{'plus':>12s} {'exp':>7s} {'g0':>12s} {'F0':>6s} {'F05':>6s}"
    )
    print("-" * 96)
    rows = []
    for drift in DRIFTS:
        for restore in RESTORES:
            row = _score_row(drift, restore)
            rows.append(row)
            print(
                f"{row.drift:5.2f} {row.restore:7.2f} "
                f"{row.signed_zero:+12.3e} {row.signed_neutral:+12.3e} "
                f"{row.signed_single:+12.3e} {row.signed_exponent:7.3f} "
                f"{row.action_gamma0:+12.3e} {row.action_fm0:6.3f} {row.action_fm05:6.3f}"
            )

    # Compact verdicts.
    signed_survivors = [
        row for row in rows
        if abs(row.signed_zero) < 1e-12
        and abs(row.signed_neutral) < 1e-12
        and row.signed_single != 0.0
        and abs(row.signed_exponent - 1.0) < 0.05
    ]
    complex_survivors = [
        row for row in rows
        if row.action_toward[0] > 0
        and row.action_toward[1] == 0
        and row.action_fm0 > 0.99
        and row.action_fm05 > 0.99
    ]

    print()
    print("SAFE READ")
    print(f"  signed-source survivors: {len(signed_survivors)}/{len(rows)}")
    print(f"  complex-action survivors: {len(complex_survivors)}/{len(rows)}")
    if signed_survivors and complex_survivors:
        print("  narrow basin survives both rows on at least one nearby family")
    else:
        print("  basin is selective; one or both observables drop off quickly off-center")


if __name__ == "__main__":
    main()
