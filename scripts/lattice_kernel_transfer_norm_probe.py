#!/usr/bin/env python3
"""Bounded transfer-norm discrimination probe for the exploratory 3D kernel fork.

This is a narrow review-safe probe. It does not try to prove the continuum
theory and it does not rerun the heavier 4D work. Instead, it measures the
single-step transfer norm of the 3D ordered lattice kernel under refinement
for a few nearby kernel powers.

The output is intentionally simple:
  - compare nearby powers around p=2
  - report the raw outgoing transfer norm and the h^2-measured version
  - fit a log-log slope across h to see which power is closest to marginal

Interpretation:
  - slope near 0 => more stable under refinement
  - positive slope => grows as h shrinks
  - negative slope => shrinks as h shrinks

This is a discrimination harness, not a proof.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable


PHYS_CONNECTIVITY = 3.0
PHYS_W = 6.0
BETA = 0.8


@dataclass(frozen=True)
class TransferRow:
    h: float
    span: int
    raw_norm: float
    measured_norm: float


def parse_floats(values: list[str]) -> list[float]:
    return [float(v) for v in values]


def sample_offsets() -> list[tuple[int, int]]:
    return [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def outgoing_transfer_norm(h: float, p: float, measure_power: float) -> TransferRow:
    span = max(1, int(round(PHYS_CONNECTIVITY / h)))
    hw = int(round(PHYS_W / h))
    offsets = sample_offsets()
    total = 0.0
    n_samples = 0

    for iy0, iz0 in offsets:
        if abs(iy0) > hw or abs(iz0) > hw:
            continue
        n_samples += 1
        node_total = 0.0
        for diy in range(-span, span + 1):
            for diz in range(-span, span + 1):
                iyn = iy0 + diy
                izn = iz0 + diz
                if abs(iyn) > hw or abs(izn) > hw:
                    continue
                ly = iyn * h
                lz = izn * h
                L = math.sqrt(h * h + ly * ly + lz * lz)
                if L < 1e-12:
                    continue
                theta = math.atan2(math.sqrt(ly * ly + lz * lz), h)
                weight = math.exp(-BETA * theta * theta) / (L**p)
                node_total += weight
        total += node_total

    if n_samples == 0:
        return TransferRow(h=h, span=span, raw_norm=math.nan, measured_norm=math.nan)

    raw_norm = total / n_samples
    measured_norm = (h**measure_power) * raw_norm
    return TransferRow(h=h, span=span, raw_norm=raw_norm, measured_norm=measured_norm)


def fit_log_slope(rows: list[TransferRow], attr: str) -> tuple[float, float]:
    pts = [(row.h, getattr(row, attr)) for row in rows if getattr(row, attr) > 0]
    if len(pts) < 2:
        return math.nan, math.nan
    lx = [math.log(h) for h, _ in pts]
    ly = [math.log(v) for _, v in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx <= 1e-12:
        return math.nan, math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    slope = sxy / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, r2


def run_probe(h_values: Iterable[float], p_values: Iterable[float], measure_power: float) -> None:
    print("=" * 100)
    print("3D KERNEL TRANSFER-NORM DISCRIMINATION PROBE")
    print(f"  ordered lattice, PHYS_W={PHYS_W}, PHYS_CONNECTIVITY={PHYS_CONNECTIVITY}")
    print(f"  measured norm = h^{measure_power:.1f} × sum_j exp(-beta theta^2) / L^p")
    print("  goal: identify the kernel power that is closest to marginal/stable under refinement")
    print("=" * 100)
    print()

    ranking: list[tuple[float, float, float, float]] = []
    for p in p_values:
        rows: list[TransferRow] = []
        print(f"p = {p:.2f}")
        print("  h      span   raw_norm      h^m-measured_norm")
        for h in h_values:
            row = outgoing_transfer_norm(h, p, measure_power)
            rows.append(row)
            print(f"  {row.h:>4.2f}   {row.span:>4d}   {row.raw_norm:>12.6e}   {row.measured_norm:>14.6e}")
        raw_slope, raw_r2 = fit_log_slope(rows, "raw_norm")
        meas_slope, meas_r2 = fit_log_slope(rows, "measured_norm")
        ranking.append((abs(meas_slope), p, raw_slope, meas_slope))
        print(
            f"  slopes: raw={raw_slope:+.3f} (R^2={raw_r2:.3f}), "
            f"measured={meas_slope:+.3f} (R^2={meas_r2:.3f})"
        )
        print("  within-power note: measured norm is the comparison of interest")
        print()

    print("Measured-norm marginality ranking (smaller |slope| is closer to stable):")
    for idx, (_, p, raw_slope, meas_slope) in enumerate(sorted(ranking), start=1):
        print(f"  {idx}. p={p:.2f}  measured slope={meas_slope:+.3f}  raw slope={raw_slope:+.3f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--h-values",
        nargs="+",
        default=["1.0", "0.5", "0.25"],
        help="spacing values to probe",
    )
    parser.add_argument(
        "--p-values",
        nargs="+",
        default=["1.5", "2.0", "2.5", "3.0"],
        help="kernel powers to compare",
    )
    parser.add_argument(
        "--measure-power",
        type=float,
        default=2.0,
        help="measure factor exponent used in the h^m-normalized norm",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_probe(parse_floats(args.h_values), parse_floats(args.p_values), args.measure_power)


if __name__ == "__main__":
    main()
