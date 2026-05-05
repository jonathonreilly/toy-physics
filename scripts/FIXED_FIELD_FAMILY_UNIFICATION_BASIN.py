#!/usr/bin/env python3
"""Tiny shared-neighborhood basin for the fixed-field family unification result.

This script asks one narrow question:

Does the same retained grown-family neighborhood that already supports the
signed-source basin and the complex-action basin also support both fixed-field
companions on the shared overlap rows?

Guard rails:
  - exact zero / neutral controls on the sign-law branch
  - exact gamma=0 reduction on the complex-action branch
  - near-linear charge scaling and weak-field F~M checks

The claim surface is intentionally tiny:
  - only the shared overlap rows that already appear in the retained basins
  - no family-wide generalization
  - no geometry-generic transport claim
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow
from scripts.GATE_B_NONLABEL_SIGN_GROWN_TRANSFER import _build_geometry_sector_grown, Family
from scripts.complex_action_grown_companion import _build_field, _propagate as _propagate_complex
from scripts.complex_action_grown_companion import _det_prob, _centroid_z


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
PW = 8
SOURCE_Z = 3.0
SIGN_SOURCE_STRENGTH = 5e-5
COMPLEX_SOURCE_STRENGTH = 0.1
FIELD_POWER = 1
ROWS = [
    (0.20, 0.60),
    (0.20, 0.70),
]
SEEDS = [0]


@dataclass(frozen=True)
class RowResult:
    drift: float
    restore: float
    sign_zero: float
    sign_plus: float
    sign_minus: float
    sign_neutral: float
    sign_double: float
    sign_exponent: float
    gamma0_delta: float
    delta_02: float
    delta_05: float
    escape_02: float
    escape_05: float
    fm_0: float | None
    fm_05: float | None

    @property
    def sign_ok(self) -> bool:
        return (
            abs(self.sign_zero) < 1e-12
            and abs(self.sign_neutral) < 1e-12
            and self.sign_plus * self.sign_minus < 0.0
            and abs(self.sign_exponent - 1.0) < 0.05
        )

    @property
    def complex_ok(self) -> bool:
        return (
            abs(self.gamma0_delta) < 1e-12
            and self.delta_02 > 0.0
            and self.delta_05 < 0.0
            and self.fm_0 is not None
            and self.fm_05 is not None
            and abs(self.fm_0 - 1.0) < 0.05
            and abs(self.fm_05 - 1.0) < 0.05
        )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


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


def _sign_field(pos, layers, sources):
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
            field[i] += charge * SIGN_SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate_sign(pos, adj, field, q_test):
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
            act = L * (1.0 + q_test * lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
    return amps


def _measure_row(drift: float, restore: float) -> RowResult:
    pos, adj, layers = grow(drift, restore, 0)
    fam = Family(pos, layers, adj)
    sector_fam = _build_geometry_sector_grown(fam)
    sector = sector_fam.adj
    det = layers[-1]

    free_sign = _propagate_sign(pos, sector, [0.0] * len(pos), 0)
    z_free_sign = _centroid_z(free_sign, pos, det)

    def run_sign(sources):
        amps = _propagate_sign(pos, sector, _sign_field(pos, layers, sources), +1)
        return _centroid_z(amps, pos, det) - z_free_sign

    sign_zero = run_sign([])
    sign_plus = run_sign([(SOURCE_Z, +1)])
    sign_minus = run_sign([(SOURCE_Z, -1)])
    sign_neutral = run_sign([(SOURCE_Z, +1), (SOURCE_Z, -1)])
    sign_double = run_sign([(SOURCE_Z, +2)])
    sign_exponent = (
        math.log(abs(sign_double / sign_plus)) / math.log(2.0)
        if abs(sign_plus) > 1e-30 and abs(sign_double) > 1e-30
        else math.nan
    )

    field = _build_field(pos, layers, COMPLEX_SOURCE_STRENGTH, SOURCE_Z)
    free_complex = _propagate_complex(pos, sector, [0.0] * len(pos), 0.0)
    z_free_complex = _centroid_z(free_complex, pos, det)

    gamma0 = _propagate_complex(pos, sector, field, 0.0)
    gamma0_delta = _centroid_z(gamma0, pos, det) - z_free_complex

    gamma02 = _propagate_complex(pos, sector, field, 0.2)
    gamma05 = _propagate_complex(pos, sector, field, 0.5)
    delta_02 = _centroid_z(gamma02, pos, det) - z_free_complex
    delta_05 = _centroid_z(gamma05, pos, det) - z_free_complex

    p_free = _det_prob(free_complex, det)
    escape_02 = _det_prob(gamma02, det) / p_free if p_free > 1e-30 else 0.0
    escape_05 = _det_prob(gamma05, det) / p_free if p_free > 1e-30 else 0.0

    fm_vals = []
    for gamma in [0.0, 0.5]:
        weak_deltas = []
        for s in [1e-6, 1e-5]:
            weak_field = _build_field(pos, layers, s, SOURCE_Z)
            amp = _propagate_complex(pos, sector, weak_field, gamma)
            weak_deltas.append(abs(_centroid_z(amp, pos, det) - z_free_complex))
        if weak_deltas[0] > 1e-15 and weak_deltas[1] > 1e-15:
            fm_vals.append(math.log(weak_deltas[1] / weak_deltas[0]) / math.log(10.0))

    return RowResult(
        drift=drift,
        restore=restore,
        sign_zero=sign_zero,
        sign_plus=sign_plus,
        sign_minus=sign_minus,
        sign_neutral=sign_neutral,
        sign_double=sign_double,
        sign_exponent=sign_exponent,
        gamma0_delta=gamma0_delta,
        delta_02=delta_02,
        delta_05=delta_05,
        escape_02=escape_02,
        escape_05=escape_05,
        fm_0=fm_vals[0] if len(fm_vals) > 0 else None,
        fm_05=fm_vals[1] if len(fm_vals) > 1 else None,
    )


def main() -> None:
    print("=" * 96)
    print("FIXED-FIELD FAMILY UNIFICATION BASIN")
    print("  shared overlap rows from the retained sign-law and complex-action basins")
    print("=" * 96)
    print(f"h={H}, NL={NL}, W={PW}, rows={ROWS}, seeds={SEEDS}")
    print()
    print(
        f"{'drift':>5s} {'restore':>7s} {'sign0':>12s} {'plus':>12s} {'minus':>12s} "
        f"{'neutral':>12s} {'exp':>7s} {'g0':>12s} {'d02':>12s} {'d05':>12s} "
        f"{'fm0':>7s} {'fm05':>7s}"
    )
    print("-" * 118)

    rows: list[RowResult] = []
    for drift, restore in ROWS:
        row = _measure_row(drift, restore)
        rows.append(row)
        fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "  nan"
        fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "  nan"
        print(
            f"{row.drift:5.2f} {row.restore:7.2f} "
            f"{row.sign_zero:+12.3e} {row.sign_plus:+12.3e} {row.sign_minus:+12.3e} "
            f"{row.sign_neutral:+12.3e} {row.sign_exponent:7.3f} "
            f"{row.gamma0_delta:+12.3e} {row.delta_02:+12.3e} {row.delta_05:+12.3e} "
            f"{fm0:>7s} {fm05:>7s}"
        )

    sign_ok = [r for r in rows if r.sign_ok]
    complex_ok = [r for r in rows if r.complex_ok]
    unified = [r for r in rows if r.sign_ok and r.complex_ok]

    print()
    print("SAFE READ")
    print(f"  sign-law survivors: {len(sign_ok)}/{len(rows)}")
    print(f"  complex-action survivors: {len(complex_ok)}/{len(rows)}")
    print(f"  unified survivors: {len(unified)}/{len(rows)}")
    if unified:
        print("  the same grown-family neighborhood supports both fixed-field companions")
    else:
        print("  the shared neighborhood is selective; unification does not survive the basin cleanly")


if __name__ == "__main__":
    main()
