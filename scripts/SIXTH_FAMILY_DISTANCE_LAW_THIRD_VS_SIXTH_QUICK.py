#!/usr/bin/env python3
"""Quick third-vs-sixth distance-law spot check on retained rows.

This is a narrow contrast used when the full retained-row sweep is too slow.
It compares one interior retained third-family row against one retained
sixth-family row, keeping the exact-control language narrow:

- both rows already passed the parent exact zero / neutral gates
- the question is only whether the distance tail looks near-Newtonian

If the third row misses while the sixth row survives, the miss is connected
back to the breakpoint classifier rather than softened into a broader claim.
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

from THIRD_GROWN_FAMILY_SIGN_SWEEP import (  # type: ignore
    Family as ThirdFamily,
    _build_third_connectivity,
    _centroid_z as third_centroid_z,
    _field_from_sources as third_field_from_sources,
    _measure_row as third_measure_row,
    _propagate as third_propagate,
    grow as third_grow,
)
from SIXTH_FAMILY_SHEARED_SWEEP import (  # type: ignore
    Family as SixthFamily,
    _build_sheared_shell_connectivity,
    _centroid_z as sixth_centroid_z,
    _field_from_sources as sixth_field_from_sources,
    _measure_row as sixth_measure_row,
    _propagate as sixth_propagate,
    grow as sixth_grow,
)


DISTANCE_BS = [5, 6, 7, 8, 10]
THIRD_ROW = (0.20, 2)
SIXTH_ROW = (0.20, 2)


@dataclass(frozen=True)
class TailResult:
    family: str
    drift: float
    seed: int
    alpha: float
    r2: float
    toward: int
    total: int

    @property
    def ok(self) -> bool:
        return (
            math.isfinite(self.alpha)
            and self.r2 > 0.90
            and abs(self.alpha + 1.0) < 0.20
            and self.toward == self.total
        )


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


def _measure_third(drift: float, seed: int) -> TailResult:
    pos, _adj, layers, _nmap = third_grow(drift, seed)
    fam = ThirdFamily(pos, layers, {})
    third = _build_third_connectivity(fam)
    det = third.layers[-1]
    free = third_propagate(third.positions, third.adj, [0.0] * len(third.positions))
    z_free = third_centroid_z(free, third.positions, det)

    deltas: list[float] = []
    toward = 0
    for b in DISTANCE_BS:
        field = third_field_from_sources(third.positions, third.layers, [(float(b), +1)])
        amps = third_propagate(third.positions, third.adj, field)
        delta = third_centroid_z(amps, third.positions, det) - z_free
        deltas.append(delta)
        toward += int(delta > 0)

    alpha, r2 = _fit_power(DISTANCE_BS, deltas)
    return TailResult("third", drift, seed, alpha, r2, toward, len(DISTANCE_BS))


def _measure_sixth(drift: float, seed: int) -> TailResult:
    pos, _adj, layers, _nmap = sixth_grow(drift, seed)
    fam = SixthFamily(pos, layers, _adj)
    sixth = _build_sheared_shell_connectivity(fam)
    det = sixth.layers[-1]
    free = sixth_propagate(sixth.positions, sixth.adj, [0.0] * len(sixth.positions))
    z_free = sixth_centroid_z(free, sixth.positions, det)

    deltas: list[float] = []
    toward = 0
    for b in DISTANCE_BS:
        field = sixth_field_from_sources(sixth.positions, sixth.layers, [(float(b), +1)])
        amps = sixth_propagate(sixth.positions, sixth.adj, field)
        delta = sixth_centroid_z(amps, sixth.positions, det) - z_free
        deltas.append(delta)
        toward += int(delta > 0)

    alpha, r2 = _fit_power(DISTANCE_BS, deltas)
    return TailResult("sixth", drift, seed, alpha, r2, toward, len(DISTANCE_BS))


def main() -> int:
    print("=" * 88)
    print("QUICK THIRD VS SIXTH DISTANCE LAW SPOT CHECK")
    print("  one retained row per family")
    print("=" * 88)
    print(f"distance b values = {DISTANCE_BS}")
    print(f"third row = {THIRD_ROW} (retained sign basin interior)")
    print(f"sixth row = {SIXTH_ROW} (retained sheared basin interior)")
    print()

    third_gate = third_measure_row(*THIRD_ROW)
    sixth_gate = sixth_measure_row(*SIXTH_ROW)

    third = _measure_third(*THIRD_ROW)
    sixth = _measure_sixth(*SIXTH_ROW)

    print(f"{'family':>7s} {'drift':>5s} {'seed':>4s} {'alpha':>8s} {'r2':>7s} {'toward':>9s} {'ok':>4s}")
    print("-" * 88)
    for row in (third, sixth):
        print(
            f"{row.family:>7s} {row.drift:5.2f} {row.seed:4d} {row.alpha:8.3f} {row.r2:7.3f} "
            f"{row.toward:9d}/{row.total:<3d} {'YES' if row.ok else 'no':>4s}"
        )

    print()
    print("GATE REPLAY")
    print(
        f"  third gate: zero={third_gate.zero:+.3e}, neutral={third_gate.neutral:+.3e}, "
        f"plus={third_gate.plus:+.3e}, minus={third_gate.minus:+.3e}"
    )
    print(
        f"  sixth gate: zero={sixth_gate.zero:+.3e}, neutral={sixth_gate.neutral:+.3e}, "
        f"plus={sixth_gate.plus:+.3e}, minus={sixth_gate.minus:+.3e}"
    )

    print()
    print("SAFE READ")
    if third.ok and sixth.ok:
        print("  both retained rows preserve the near-Newtonian tail")
        print("  freeze as a targeted positive across the two sampled families")
    elif sixth.ok and not third.ok:
        print("  sixth row preserves the tail, third row misses")
        print("  connect the third-family miss back to the breakpoint classifier")
    elif third.ok and not sixth.ok:
        print("  third row preserves the tail, sixth row misses")
        print("  this is a family split rather than a universal tail claim")
    else:
        print("  neither sampled retained row preserves the near-Newtonian tail")
        print("  the breakpoint classifier remains the correct structural read")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
