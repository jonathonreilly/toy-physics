#!/usr/bin/env python3
"""Scaled wider-family h=0.125 scan on a shorter physical length.

This is a disjoint continuation of the wider-family replay lane. The
width-4 replay at `phys_l = 6` is already frozen as a bounded no-go in the
repo notes, so this harness checks whether that conclusion is sensitive to a
shorter axial scale while keeping the same dense-family machinery and the same
review-safe observables.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.lattice_3d_l2_numpy_h0125_only import (
    K,
    born_ratio,
    build_dense_family,
    detector_probability,
    free_prefix_to_barrier,
    make_field_layers,
    propagate_field,
    propagate_free_from_barrier,
)


WINDOW_FACTORIES = {
    "full": lambda lat: np.ones(lat["yz"].shape[0], dtype=bool),
    "radial1p5": lambda lat: np.sqrt(lat["yz"][:, 0] ** 2 + lat["yz"][:, 1] ** 2) <= 1.5,
    "central_strip": lambda lat: np.abs(lat["yz"][:, 0]) <= 0.5,
}


WINDOW_LABELS = {
    "full": "full",
    "radial1p5": "r<=1.5",
    "central_strip": "|y|<=0.5",
}


def fit_power(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def centroid_on_mask(lat: dict[str, object], amps: np.ndarray, mask: np.ndarray) -> tuple[float | None, float]:
    probs = detector_probability(amps)
    masked = probs * mask
    total = float(masked.sum())
    if total <= 1e-30:
        return None, 0.0
    z = lat["yz"][:, 1]
    return float((masked * z).sum() / total), total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Length-scaled wider-family h=0.125 continuum bridge diagnostic."
    )
    parser.add_argument("--phys-l", type=int, default=4, help="Physical length. Default: 4")
    parser.add_argument(
        "--phys-w",
        type=int,
        nargs="+",
        default=[3, 4],
        help="Physical half-widths to compare. Default: 3 4",
    )
    parser.add_argument(
        "--z-mass",
        type=float,
        nargs="+",
        default=[1.5, 2.0, 3.0],
        help="Source z positions to probe. Default: 1.5 2.0 3.0",
    )
    parser.add_argument(
        "--strength",
        type=float,
        nargs="+",
        default=[1e-7, 2e-7, 5e-7, 1e-6, 2e-6, 5e-6],
        help="Weak-field source strengths to fit. Default: 1e-7 2e-7 5e-7 1e-6 2e-6 5e-6",
    )
    parser.add_argument(
        "--window",
        choices=sorted(WINDOW_FACTORIES.keys()),
        nargs="+",
        default=["full", "radial1p5", "central_strip"],
        help="Detector windows to evaluate. Default: full radial1p5 central_strip",
    )
    return parser.parse_args()


def run_one(phys_l: int, phys_w: int, z_masses: list[float], strengths: list[float], window_keys: list[str]) -> None:
    h = 0.125
    z_mass = max(z_masses)

    lat = build_dense_family(phys_l, phys_w, h)
    _prefix, barrier_in = free_prefix_to_barrier(lat)
    free_final = propagate_free_from_barrier(lat, barrier_in, lat["default_open"])
    windows = {WINDOW_LABELS[key]: WINDOW_FACTORIES[key](lat) for key in window_keys}

    born = born_ratio(lat, barrier_in)
    field0 = make_field_layers(lat, z_mass, strengths[-1])
    null_final = propagate_field(lat, field0, lat["default_open"], 0.0)
    z_free_full, _ = centroid_on_mask(lat, free_final, windows["full"])
    z_null_full, _ = centroid_on_mask(lat, null_final, windows["full"])
    field_final = propagate_field(lat, field0, lat["default_open"], K)
    z_field_full, p_field = centroid_on_mask(lat, field_final, windows["full"])
    grav_full = (
        z_field_full - z_free_full
        if z_field_full is not None and z_free_full is not None
        else float("nan")
    )

    print("=" * 92)
    print(f"SCALED WIDER H=0.125 SCAN: phys_l={phys_l}, phys_w={phys_w}")
    print(f"  nodes={lat['n']}, layers={lat['nl']}, nodes/layer={lat['npl']}, dense_edges={lat['edges']}")
    print(f"  Born={born:.2e}")
    print(f"  k=0 check={z_null_full - z_free_full:+.6f}" if z_null_full is not None and z_free_full is not None else "  k=0 check=n/a")
    print(f"  gravity(z={z_mass:.1f}, s={strengths[-1]:.0e})={grav_full:+.6f}  P_det={p_field:.3e}")
    print()

    for label, mask in windows.items():
        z_free, p_free = centroid_on_mask(lat, free_final, mask)
        print(f"WINDOW {label}  p_free={p_free:.3e}")
        for z_mass_test in z_masses:
            m_data: list[float] = []
            g_data: list[float] = []
            for s in strengths:
                field = make_field_layers(lat, z_mass_test, s)
                final = propagate_field(lat, field, lat["default_open"], K)
                z_m, _ = centroid_on_mask(lat, final, mask)
                if z_m is None or z_free is None:
                    continue
                delta = z_m - z_free
                if delta > 0:
                    m_data.append(s)
                    g_data.append(delta)
            alpha = fit_power(m_data, g_data) if len(m_data) >= 3 else None
            if alpha is None:
                print(f"  z={z_mass_test:>3.1f}: count={len(m_data)} alpha=n/a")
            else:
                print(
                    f"  z={z_mass_test:>3.1f}: count={len(m_data)} alpha={alpha:.3f} "
                    f"delta_max={max(g_data):.6f}"
                )
        print()


def main() -> None:
    args = parse_args()
    print("=" * 92)
    print("SCALED WIDER H=0.125 CONTINUUM BRIDGE DIAGNOSTIC")
    print("  goal: check whether the width-4 no-go survives a shorter axial scale")
    print("=" * 92)
    print(
        "  widths=",
        ",".join(str(v) for v in args.phys_w),
        " windows=",
        ",".join(args.window),
        " z_mass=",
        ",".join(f"{v:.1f}" for v in args.z_mass),
    )
    print()
    for phys_w in args.phys_w:
        run_one(args.phys_l, phys_w, args.z_mass, args.strength, args.window)


if __name__ == "__main__":
    main()
