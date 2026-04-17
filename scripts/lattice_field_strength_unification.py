#!/usr/bin/env python3
"""Weak-field reopening of the ordered-lattice symmetry line.

This script checks whether the negative lattice-symmetry decision at the
standard field strength was really a geometry limit, or whether field strength
is the missing control parameter.

Scope:
  - standard linear propagator only
  - same ordered 2D lattice + explicit Z2 symmetry family
  - same-family companion Born audit, not a hidden harness swap
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_mirror_hybrid import K, propagate
from scripts.lattice_symmetry_unification_decision import (
    B_VALUES,
    GEOMETRIES,
    RETAIN_BORN_MAX,
    RETAIN_DECOH_MIN,
    RETAIN_K0_MAX,
    RETAIN_MI_MIN,
    RETAIN_DISTANCE_R2_MIN,
    aperture_for_rows,
    born_companion_audit,
    build_setup,
    centroid_y,
    cl_purity,
    d_tv,
    field_for_mass,
    fit_label,
    fit_tail,
    mutual_info,
)

MAX_DY_VALUES = [4, 5, 6]
STRENGTH_VALUES = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
MASS_OFFSET = 1
CANONICAL_MAX_DY = 5
CANONICAL_GEOMETRY = "wide_center"


def barrier_distance_curve(setup, blocked, strength):
    field_zero = [0.0] * len(setup.positions)
    amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, blocked)
    flat_centroid = centroid_y(amps_flat, setup.positions, setup.detector)
    rows = []
    for b in B_VALUES:
        field_mass = field_for_mass(
            setup.positions,
            setup.node_map,
            setup.gravity_layer,
            b,
            strength=strength,
        )
        amps_mass = propagate(setup.positions, setup.adj, field_mass, setup.source, K, blocked)
        rows.append((b, centroid_y(amps_mass, setup.positions, setup.detector) - flat_centroid))
    return rows


def barrier_metrics(setup, upper_rows, strength):
    aperture = aperture_for_rows(setup, upper_rows)
    mass_y = aperture["top_row"] + MASS_OFFSET
    field_zero = [0.0] * len(setup.positions)
    field_mass = field_for_mass(
        setup.positions,
        setup.node_map,
        setup.gravity_layer,
        mass_y,
        strength=strength,
    )

    amps_mass = propagate(setup.positions, setup.adj, field_mass, setup.source, K, aperture["blocked"])
    amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, aperture["blocked"])
    gravity = centroid_y(amps_mass, setup.positions, setup.detector) - centroid_y(
        amps_flat,
        setup.positions,
        setup.detector,
    )

    amps_mass_k0 = propagate(setup.positions, setup.adj, field_mass, setup.source, 0.0, aperture["blocked"])
    amps_flat_k0 = propagate(setup.positions, setup.adj, field_zero, setup.source, 0.0, aperture["blocked"])
    gravity_k0 = centroid_y(amps_mass_k0, setup.positions, setup.detector) - centroid_y(
        amps_flat_k0,
        setup.positions,
        setup.detector,
    )

    amps_upper = propagate(
        setup.positions,
        setup.adj,
        field_mass,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["lower_nodes"]),
    )
    amps_lower = propagate(
        setup.positions,
        setup.adj,
        field_mass,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["upper_nodes"]),
    )

    purity, _ = cl_purity(setup, amps_upper, amps_lower)
    distance_rows = barrier_distance_curve(setup, aperture["blocked"], strength)
    distance_fit = fit_tail(distance_rows)

    return {
        "mass_y": float(mass_y),
        "gravity": gravity,
        "gravity_k0": gravity_k0,
        "mi": mutual_info(amps_upper, amps_lower, setup.positions, setup.detector),
        "dtv": d_tv(amps_upper, amps_lower, setup.detector),
        "pur_cl": purity,
        "decoh": 1.0 - purity if not math.isnan(purity) else math.nan,
        "born": born_companion_audit(setup, upper_rows),
        "distance_rows": distance_rows,
        "distance_fit": distance_fit,
        "positive_b": sum(1 for _, delta in distance_rows if delta > 0),
    }


def retained(metrics) -> bool:
    fit = metrics["distance_fit"]
    return (
        not math.isnan(metrics["born"])
        and metrics["born"] <= RETAIN_BORN_MAX
        and not math.isnan(metrics["gravity_k0"])
        and abs(metrics["gravity_k0"]) <= RETAIN_K0_MAX
        and not math.isnan(metrics["mi"])
        and metrics["mi"] >= RETAIN_MI_MIN
        and not math.isnan(metrics["decoh"])
        and metrics["decoh"] >= RETAIN_DECOH_MIN
        and not math.isnan(metrics["gravity"])
        and metrics["gravity"] > 0.0
        and metrics["positive_b"] == len(B_VALUES)
        and fit is not None
        and fit.alpha < 0.0
        and fit.r2 >= RETAIN_DISTANCE_R2_MIN
    )


def curve_label(rows):
    return "  ".join(f"b={b}:{delta:+.4f}" for b, delta in rows)


def main() -> None:
    print("=" * 120)
    print("LATTICE FIELD-STRENGTH UNIFICATION SWEEP")
    print("  ordered 2D lattice + explicit Z2 symmetry, standard linear propagator only")
    print("  question: does weak coupling reopen a one-harness pocket on the same 2-slit card?")
    print("=" * 120)
    print()

    setups = {max_dy: build_setup(max_dy) for max_dy in MAX_DY_VALUES}
    rows = []

    print("FIELD-STRENGTH SWEEP")
    print(
        f"  {'max_dy':>6s}  {'slit':>13s}  {'strength':>9s}  {'MI':>7s}  {'d_TV':>7s}  "
        f"{'1-pur':>7s}  {'grav@b6':>9s}  {'+b':>3s}  {'fit':>20s}  {'Born':>10s}  {'retain':>6s}"
    )
    print(f"  {'-' * 108}")
    for max_dy in MAX_DY_VALUES:
        setup = setups[max_dy]
        for geometry_name, upper_rows in GEOMETRIES.items():
            for strength in STRENGTH_VALUES:
                metrics = barrier_metrics(setup, upper_rows, strength)
                row_retained = retained(metrics)
                rows.append((max_dy, geometry_name, strength, metrics, row_retained))
                print(
                    f"  {max_dy:6d}  {geometry_name:>13s}  {strength:9.4f}  "
                    f"{metrics['mi']:7.3f}  {metrics['dtv']:7.3f}  {metrics['decoh']:7.3f}  "
                    f"{metrics['gravity']:+9.4f}  {metrics['positive_b']:3d}  "
                    f"{fit_label(metrics['distance_fit']):>20s}  {metrics['born']:10.2e}  "
                    f"{'yes' if row_retained else 'no':>6s}"
                )
    print()

    canonical = next(
        metrics
        for max_dy, geometry_name, strength, metrics, _
        in rows
        if max_dy == CANONICAL_MAX_DY and geometry_name == CANONICAL_GEOMETRY and abs(strength - 0.0005) < 1e-12
    )
    print("CANONICAL REOPENING ROW")
    print(
        f"  max_dy={CANONICAL_MAX_DY} slit={CANONICAL_GEOMETRY} strength=0.0005 "
        f"mass_y={canonical['mass_y']:.0f}"
    )
    print(
        f"  MI={canonical['mi']:.3f} d_TV={canonical['dtv']:.3f} "
        f"1-pur={canonical['decoh']:.3f} grav@b6={canonical['gravity']:+.4f}"
    )
    print(
        f"  Born={canonical['born']:.2e} k=0={canonical['gravity_k0']:+.2e} "
        f"positive_b={canonical['positive_b']}/{len(B_VALUES)} fit={fit_label(canonical['distance_fit'])}"
    )
    print(f"  curve: {curve_label(canonical['distance_rows'])}")
    print()

    retained_rows = [
        (max_dy, geometry_name, strength, metrics)
        for max_dy, geometry_name, strength, metrics, row_retained in rows
        if row_retained
    ]
    print("RETAINED WEAK-FIELD POCKET")
    print(f"  retained_rows={len(retained_rows)}/{len(rows)}")
    for max_dy, geometry_name, strength, metrics in retained_rows:
        fit = metrics["distance_fit"]
        print(
            f"  max_dy={max_dy} slit={geometry_name} strength={strength:.4f} "
            f"MI={metrics['mi']:.3f} 1-pur={metrics['decoh']:.3f} "
            f"grav@b6={metrics['gravity']:+.4f} fit=peak@{fit.peak_b},a={fit.alpha:.2f},R2={fit.r2:.2f}"
        )
    print()

    positive_rows = sum(1 for _, _, _, metrics, _ in rows if metrics["gravity"] > 0)
    all_positive_distance = sum(1 for _, _, _, metrics, _ in rows if metrics["positive_b"] == len(B_VALUES))
    born_clean_rows = sum(1 for _, _, _, metrics, _ in rows if metrics["born"] <= RETAIN_BORN_MAX)
    print("DECISION")
    print(f"  Born-clean rows: {born_clean_rows}/{len(rows)}")
    print(f"  Positive gravity rows: {positive_rows}/{len(rows)}")
    print(f"  All-b-positive rows: {all_positive_distance}/{len(rows)}")
    print(f"  Retained weak-field rows: {len(retained_rows)}/{len(rows)}")
    if retained_rows:
        print("  conclusion=REOPENED")
        print("  blocker cleared=field-strength-induced beam depletion at standard strength")
    else:
        print("  conclusion=NOT_REOPENED")
        print("  blocker persists=no review-safe weak-field pocket found")


if __name__ == "__main__":
    main()
