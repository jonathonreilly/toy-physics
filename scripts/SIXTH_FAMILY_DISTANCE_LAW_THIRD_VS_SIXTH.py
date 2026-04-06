#!/usr/bin/env python3
"""Third-vs-sixth distance-law contrast on retained passing rows only.

This runner is intentionally narrow:
- start from the retained passing rows of the third family and sixth family
- keep the exact baseline/control language narrow by reusing the retained gates
- ask only whether the near-Newtonian tail survives on the retained rows

Claim surface:
- if a family keeps alpha near -1 with all TOWARD samples, freeze it as a
  targeted positive
- if it misses, connect the miss back to the distance-law breakpoint classifier

This is not a family-wide theorem. It is a targeted contrast of the two
structured families that are most relevant to the current distance-tail
question.
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

from THIRD_GROWN_FAMILY_SIGN_SWEEP import (  # type: ignore
    DRIFTS as THIRD_DRIFTS,
    SEEDS as THIRD_SEEDS,
    Family as ThirdFamily,
    _build_third_connectivity,
    _centroid_z as third_centroid_z,
    _field_from_sources as third_field_from_sources,
    _measure_row as third_measure_row,
    _propagate as third_propagate,
    grow as third_grow,
)
from SIXTH_FAMILY_SHEARED_SWEEP import (  # type: ignore
    DRIFTS as SIXTH_DRIFTS,
    SEEDS as SIXTH_SEEDS,
    Family as SixthFamily,
    _build_sheared_shell_connectivity,
    _centroid_z as sixth_centroid_z,
    _field_from_sources as sixth_field_from_sources,
    _measure_row as sixth_measure_row,
    _propagate as sixth_propagate,
    grow as sixth_grow,
)


DISTANCE_BS = [5, 6, 7, 8, 10]


@dataclass(frozen=True)
class TailRow:
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


def _measure_third_tail(drift: float, seed: int) -> TailRow:
    pos, _adj, layers, _nmap = third_grow(drift, seed)
    fam = ThirdFamily(pos, layers, {})
    third = _build_third_connectivity(fam)
    det = third.layers[-1]
    free = third_propagate(third.positions, third.adj, [0.0] * len(third.positions))
    z_free = third_centroid_z(free, third.positions, det)

    deltas: list[float] = []
    toward = 0
    total = 0
    for b in DISTANCE_BS:
        field = third_field_from_sources(
            third.positions,
            third.layers,
            [(float(b), +1)],
        )
        amps = third_propagate(third.positions, third.adj, field)
        z = third_centroid_z(amps, third.positions, det)
        delta = z - z_free
        deltas.append(delta)
        total += 1
        if delta > 0:
            toward += 1

    alpha, r2 = _fit_power(DISTANCE_BS, deltas)
    return TailRow("third", drift, seed, alpha, r2, toward, total)


def _measure_sixth_tail(drift: float, seed: int) -> TailRow:
    pos, _adj, layers, _nmap = sixth_grow(drift, seed)
    fam = SixthFamily(pos, layers, _adj)
    sixth = _build_sheared_shell_connectivity(fam)
    det = sixth.layers[-1]
    free = sixth_propagate(sixth.positions, sixth.adj, [0.0] * len(sixth.positions))
    z_free = sixth_centroid_z(free, sixth.positions, det)

    deltas: list[float] = []
    toward = 0
    total = 0
    for b in DISTANCE_BS:
        field = sixth_field_from_sources(
            sixth.positions,
            sixth.layers,
            [(float(b), +1)],
        )
        amps = sixth_propagate(sixth.positions, sixth.adj, field)
        z = sixth_centroid_z(amps, sixth.positions, det)
        delta = z - z_free
        deltas.append(delta)
        total += 1
        if delta > 0:
            toward += 1

    alpha, r2 = _fit_power(DISTANCE_BS, deltas)
    return TailRow("sixth", drift, seed, alpha, r2, toward, total)


def _rows_for_third() -> list[tuple[float, int]]:
    rows: list[tuple[float, int]] = []
    for drift in THIRD_DRIFTS:
        for seed in THIRD_SEEDS:
            if third_measure_row(drift, seed).signed_ok:
                rows.append((drift, seed))
    return rows


def _rows_for_sixth() -> list[tuple[float, int]]:
    rows: list[tuple[float, int]] = []
    for drift in SIXTH_DRIFTS:
        for seed in SIXTH_SEEDS:
            if sixth_measure_row(drift, seed).ok:
                rows.append((drift, seed))
    return rows


def main() -> int:
    print("=" * 96)
    print("THIRD VS SIXTH DISTANCE LAW CONTRAST")
    print("  retained passing rows only")
    print("=" * 96)
    print(f"distance b values = {DISTANCE_BS}")
    print("gate: exact zero/neutral controls already retained in the parent sign families")
    print()

    third_rows = _rows_for_third()
    sixth_rows = _rows_for_sixth()

    print(f"third retained sign rows: {third_rows}")
    print(f"sixth retained sign rows: {sixth_rows}")
    print()
    print(f"{'family':>7s} {'drift':>5s} {'seed':>4s} {'alpha':>8s} {'r2':>7s} {'toward':>9s} {'ok':>4s}")
    print("-" * 96)

    rows: list[TailRow] = []
    for drift, seed in third_rows:
        row = _measure_third_tail(drift, seed)
        rows.append(row)
        print(
            f"{row.family:>7s} {row.drift:5.2f} {row.seed:4d} {row.alpha:8.3f} {row.r2:7.3f} "
            f"{row.toward:9d}/{row.total:<3d} {'YES' if row.ok else 'no':>4s}"
        )

    for drift, seed in sixth_rows:
        row = _measure_sixth_tail(drift, seed)
        rows.append(row)
        print(
            f"{row.family:>7s} {row.drift:5.2f} {row.seed:4d} {row.alpha:8.3f} {row.r2:7.3f} "
            f"{row.toward:9d}/{row.total:<3d} {'YES' if row.ok else 'no':>4s}"
        )

    print()
    print("SAFE READ")
    for family in ("third", "sixth"):
        fam_rows = [r for r in rows if r.family == family]
        passed = [r for r in fam_rows if r.ok]
        if passed:
            alphas = [r.alpha for r in passed if math.isfinite(r.alpha)]
            print(
                f"  {family}: {len(passed)}/{len(fam_rows)} pass, mean alpha={sum(alphas)/len(alphas):.6f}, "
                f"toward fraction={sum(r.toward / r.total for r in passed)/len(passed):.6f}"
            )
        else:
            print(f"  {family}: no retained row preserved the near-Newtonian distance tail")

    third_pass = any(r.ok for r in rows if r.family == "third")
    sixth_pass = any(r.ok for r in rows if r.family == "sixth")
    if third_pass and sixth_pass:
        print("  both families preserve the tail on retained rows: targeted positive")
    elif sixth_pass and not third_pass:
        print("  sixth family preserves the tail, third family misses: breakpoint classifier still applies")
    elif third_pass and not sixth_pass:
        print("  third family preserves the tail, sixth family misses: family split is real")
    else:
        print("  neither family preserves the tail on the retained rows: diagnosed breakpoint remains")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
