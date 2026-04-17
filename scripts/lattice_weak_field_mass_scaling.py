#!/usr/bin/env python3
"""Weak-field mass-scaling probe on the retained ordered-lattice pocket.

Mass is encoded as field strength on one fixed mass node. Node count is held
fixed so the sweep isolates the response to the mass-proxy amplitude.

This script asks a narrow question:

Does the retained weak-field lattice pocket support a genuine F∝M law, or
only a positive but sub-linear mass-response?

Scope:
  - standard linear propagator only
  - ordered 2D lattice with explicit Z2 symmetry
  - canonical retained pocket: max_dy=5, wide_center slit family
  - mass proxy: field strength at a fixed mass position
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_field_strength_unification import (
    B_VALUES,
    GEOMETRIES,
    barrier_metrics,
    build_setup,
    fit_label,
)

MAX_DY = 5
GEOMETRY_NAME = "wide_center"
STRENGTH_VALUES = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4]
CANONICAL_STRENGTH = 5e-4


@dataclass(frozen=True)
class PowerFit:
    alpha: float
    r2: float
    prefactor: float


def fit_power_law(points: list[tuple[float, float]]) -> PowerFit | None:
    usable = [(x, y) for x, y in points if x > 0 and y > 0 and not math.isnan(y)]
    if len(usable) < 3:
        return None
    xs = [math.log(x) for x, _ in usable]
    ys = [math.log(y) for _, y in usable]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    sxx = sum((x - mean_x) ** 2 for x in xs)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    syy = sum((y - mean_y) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    alpha = sxy / sxx
    prefactor = math.exp(mean_y - alpha * mean_x)
    r2 = (sxy * sxy) / (sxx * syy)
    return PowerFit(alpha=alpha, r2=r2, prefactor=prefactor)


def main() -> None:
    setup = build_setup(MAX_DY)
    upper_rows = GEOMETRIES[GEOMETRY_NAME]

    print("=" * 112)
    print("LATTICE WEAK-FIELD MASS SCALING")
    print("  ordered 2D lattice + explicit Z2 symmetry, standard linear propagator only")
    print("  mass proxy = field strength on a fixed mass node; node count held fixed")
    print(f"  canonical family = max_dy={MAX_DY}, slit={GEOMETRY_NAME}")
    print("=" * 112)
    print()

    print("MASS-PROXY SWEEP")
    print(
        f"  {'strength':>9s}  {'MI':>7s}  {'d_TV':>7s}  {'1-pur':>7s}  "
        f"{'grav':>9s}  {'sign':>4s}  {'k=0':>11s}  {'Born':>10s}  {'fit':>20s}  {'retain':>6s}"
    )
    print(f"  {'-' * 104}")

    rows = []
    for strength in STRENGTH_VALUES:
        metrics = barrier_metrics(setup, upper_rows, strength)
        fit = metrics["distance_fit"]
        retain = (
            not math.isnan(metrics["born"])
            and metrics["born"] <= 1e-12
            and not math.isnan(metrics["gravity_k0"])
            and abs(metrics["gravity_k0"]) <= 1e-9
            and not math.isnan(metrics["mi"])
            and metrics["mi"] >= 0.10
            and not math.isnan(metrics["decoh"])
            and metrics["decoh"] >= 0.03
            and not math.isnan(metrics["gravity"])
            and metrics["gravity"] > 0.0
            and metrics["positive_b"] == len(B_VALUES)
            and fit is not None
            and fit.alpha < 0.0
            and fit.r2 >= 0.80
        )
        rows.append((strength, metrics, fit, retain))
        print(
            f"  {strength:9.5f}  {metrics['mi']:7.3f}  {metrics['dtv']:7.3f}  {metrics['decoh']:7.3f}  "
            f"{metrics['gravity']:+9.4f}  "
            f"{('toward' if metrics['gravity'] > 0 else 'away'):>4s}  "
            f"{metrics['gravity_k0']:+11.2e}  {metrics['born']:10.2e}  "
            f"{fit_label(fit):>20s}  {'yes' if retain else 'no':>6s}"
        )

    print()
    canonical = next(metrics for strength, metrics, _, _ in rows if abs(strength - CANONICAL_STRENGTH) < 1e-12)
    canonical_fit = canonical["distance_fit"]

    print("CANONICAL ROW")
    print(
        f"  max_dy={MAX_DY} slit={GEOMETRY_NAME} strength={CANONICAL_STRENGTH:.4f} "
        f"mass proxy=field strength"
    )
    print(
        f"  MI={canonical['mi']:.3f} d_TV={canonical['dtv']:.3f} "
        f"1-pur={canonical['decoh']:.3f} grav={canonical['gravity']:+.4f} "
        f"Born={canonical['born']:.2e} k=0={canonical['gravity_k0']:+.2e}"
    )
    print(
        f"  positive_b={canonical['positive_b']}/{len(B_VALUES)} "
        f"tail={fit_label(canonical_fit)}"
    )

    fit = fit_power_law([(strength, metrics["gravity"]) for strength, metrics, _, _ in rows])
    positive_rows = sum(1 for _, metrics, _, _ in rows if metrics["gravity"] > 0)
    born_clean_rows = sum(1 for _, metrics, _, _ in rows if metrics["born"] <= 1e-12)
    print()
    print("POWER-LAW FIT")
    if fit is not None:
        print(f"  gravity = {fit.prefactor:.4f} * strength^{fit.alpha:.3f}")
        print(f"  R^2 = {fit.r2:.3f}")
        if fit.alpha >= 0.7:
            print("  read = linear-ish mass response; F∝M remains plausible")
        elif fit.alpha > 0.0:
            print("  read = positive but sub-linear mass response; do not claim F∝M")
        else:
            print("  read = no retained positive mass response")
    else:
        print("  fit = unavailable")

    print()
    print("DECISION")
    print(f"  Born-clean rows: {born_clean_rows}/{len(rows)}")
    print(f"  Positive-gravity rows: {positive_rows}/{len(rows)}")
    print(f"  Retained rows: {sum(1 for _, _, _, keep in rows if keep)}/{len(rows)}")
    if fit is not None and fit.alpha > 0.0 and fit.alpha < 0.7:
        print("  conclusion=BOUND_SUBLINEAR_RESPONSE")
    elif fit is not None and fit.alpha >= 0.7:
        print("  conclusion=PROMOTED_LINEAR_RESPONSE")
    else:
        print("  conclusion=RETIRE_MASS_CLAIM")


if __name__ == "__main__":
    main()
