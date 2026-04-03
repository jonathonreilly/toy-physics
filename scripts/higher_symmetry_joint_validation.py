#!/usr/bin/env python3
"""Joint Born + gravity + decoherence validation for higher-symmetry DAGs.

This script upgrades the earlier higher-symmetry decoherence comparison to the
same review-safe joint lens used on the mirror lane:

  - detector-side total-variation distance `d_TV`
  - CL-bath purity `pur_cl`
  - corrected Born `|I3|/P`
  - `k=0` gravity control
  - gravity centroid shift at one `k`
  - band-averaged gravity centroid shift across a small `k` window

The narrow question is:

Does the Z2xZ2 geometry keep its decoherence advantage while remaining
Born-clean and gravity-positive?

The exponent fit is reported on decoherence depth

    1 - pur_cl ~= C * N^alpha

using the family-mean purity at each tested `N`, with a simple bootstrap over
the per-size seed lists to show how stable that bounded exponent is.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.higher_symmetry_dag import (
    K as DEFAULT_K,
    CONNECT_RADIUS as DEFAULT_CONNECT_RADIUS,
    XYZ_RANGE as DEFAULT_XYZ_RANGE,
    generate_random_dag,
    generate_ring_dag,
    generate_z2z2_dag,
)
from scripts.mirror_chokepoint_joint import (
    _mean_se,
    compute_field_3d,
    measure_joint,
    propagate_3d,
)

DEFAULT_K_BAND = [3.0, 5.0, 7.0]


def _fmt(mean: float, se: float, digits: int = 3, signed: bool = False) -> str:
    if math.isnan(mean):
        return "FAIL"
    spec = f"+.{digits}f" if signed else f".{digits}f"
    mean_s = format(mean, spec)
    se_s = format(se, f".{digits}f")
    return f"{mean_s}±{se_s}"


def _fmt_sci(mean: float, se: float) -> str:
    if math.isnan(mean):
        return "FAIL"
    return f"{mean:.2e}±{se:.2e}"


def _quantile(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return math.nan
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def gravity_band_metric(positions, adj, k_band: list[float]) -> float | None:
    """Band-averaged gravity read using the same mass/slit geometry as measure_joint."""
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y, _ in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    slit_a = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(bi) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    deltas = []
    for k in k_band:
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm <= 1e-30 or pf <= 1e-30:
            continue
        ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
        deltas.append(ym - yf)

    if not deltas:
        return None
    return sum(deltas) / len(deltas)


def fit_decoherence_alpha(points: list[tuple[int, float]]) -> tuple[float, float, float] | None:
    """Fit 1 - purity ~= C * N^alpha from (N, mean_purity) points."""
    usable = [(n, p) for n, p in points if n > 0 and 0.0 <= p < 1.0]
    if len(usable) < 3:
        return None
    xs = [math.log(n) for n, _ in usable]
    ys = [math.log(1.0 - p) for _, p in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy) if syy > 1e-12 else math.nan
    return alpha, coeff, r2


def bootstrap_alpha(
    purity_by_n: dict[int, list[float]],
    n_boot: int,
    rng_seed: int,
) -> tuple[float, float, float] | None:
    usable = {n: vals for n, vals in purity_by_n.items() if len(vals) >= 2}
    if len(usable) < 3:
        return None
    rng = random.Random(rng_seed)
    alphas = []
    for _ in range(n_boot):
        points = []
        for n in sorted(usable.keys()):
            vals = usable[n]
            sampled = [vals[rng.randrange(len(vals))] for _ in range(len(vals))]
            points.append((n, sum(sampled) / len(sampled)))
        fit = fit_decoherence_alpha(points)
        if fit is not None:
            alphas.append(fit[0])
    if not alphas:
        return None
    alphas.sort()
    mean = sum(alphas) / len(alphas)
    lo = _quantile(alphas, 0.025)
    hi = _quantile(alphas, 0.975)
    return mean, lo, hi


def family_generators(args):
    return {
        "random": lambda seed, nl: generate_random_dag(
            nl, args.random_npl, args.xyz_range, args.connect_radius, seed
        ),
        "z2z2": lambda seed, nl: generate_z2z2_dag(
            nl, args.z2z2_quarter, args.xyz_range, args.connect_radius, seed
        ),
        "ring": lambda seed, nl: generate_ring_dag(
            nl, args.ring_nodes, args.xyz_range, args.connect_radius, seed
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", nargs="+", default=["random", "z2z2", "ring"])
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--k", type=float, default=DEFAULT_K)
    parser.add_argument("--k-band", nargs="+", type=float, default=DEFAULT_K_BAND)
    parser.add_argument("--xyz-range", type=float, default=DEFAULT_XYZ_RANGE)
    parser.add_argument("--connect-radius", type=float, default=DEFAULT_CONNECT_RADIUS)
    parser.add_argument("--random-npl", type=int, default=50)
    parser.add_argument("--z2z2-quarter", type=int, default=12)
    parser.add_argument("--ring-nodes", type=int, default=48)
    parser.add_argument("--n-boot", type=int, default=1000)
    parser.add_argument("--bootstrap-seed", type=int, default=12345)
    args = parser.parse_args()

    generators = family_generators(args)
    unknown = [fam for fam in args.families if fam not in generators]
    if unknown:
        raise SystemExit(f"Unknown family/families: {', '.join(unknown)}")

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    family_results: dict[str, dict[int, dict[str, list[float]]]] = {}
    family_times: dict[str, dict[int, float]] = {}

    print("=" * 132)
    print("HIGHER-SYMMETRY JOINT VALIDATION")
    print("  Born + gravity + decoherence on the higher-symmetry families")
    print(
        f"  k={args.k}, k_band={args.k_band}, seeds={args.n_seeds}, "
        f"random_npl={args.random_npl}, z2z2_quarter={args.z2z2_quarter}, "
        f"ring_nodes={args.ring_nodes}, r={args.connect_radius}"
    )
    print("=" * 132)
    print()
    print(
        f"  {'N':>4s}  {'family':>8s}  {'d_TV':>10s}  {'pur_cl':>10s}  "
        f"{'grav@k':>12s}  {'grav_band':>12s}  {'band+':>7s}  {'Born':>15s}  "
        f"{'k=0':>10s}  {'ok':>3s}  {'time':>5s}"
    )
    print("  " + "-" * 118)

    for family in args.families:
        family_results[family] = {}
        family_times[family] = {}
        gen = generators[family]
        for nl in args.n_layers:
            t0 = time.time()
            rows = {
                "dtv": [],
                "pur_cl": [],
                "gravity": [],
                "grav_band": [],
                "born": [],
                "grav_k0": [],
            }
            band_pos = 0

            for seed in seeds:
                positions, adj, _ = gen(seed, nl)
                result = measure_joint(positions, adj, nl, args.k)
                if result is None:
                    continue
                rows["dtv"].append(result["dtv"])
                rows["pur_cl"].append(result["pur_cl"])
                rows["gravity"].append(result["gravity"])
                rows["born"].append(result["born"])
                rows["grav_k0"].append(result["grav_k0"])

                gb = gravity_band_metric(positions, adj, args.k_band)
                if gb is not None:
                    rows["grav_band"].append(gb)
                    if gb > 0:
                        band_pos += 1

            family_results[family][nl] = rows
            family_times[family][nl] = time.time() - t0

            dtv_m, dtv_se = _mean_se(rows["dtv"])
            pur_m, pur_se = _mean_se(rows["pur_cl"])
            g_m, g_se = _mean_se(rows["gravity"])
            gb_m, gb_se = _mean_se(rows["grav_band"])
            b_m, b_se = _mean_se(rows["born"])
            k0_m, k0_se = _mean_se(rows["grav_k0"])
            ok = len(rows["pur_cl"])

            band_ratio = f"{band_pos}/{len(rows['grav_band'])}"
            print(
                f"  {nl:4d}  {family:>8s}  {_fmt(dtv_m, dtv_se):>10s}  "
                f"{_fmt(pur_m, pur_se):>10s}  {_fmt(g_m, g_se, signed=True):>12s}  "
                f"{_fmt(gb_m, gb_se, signed=True):>12s}  "
                f"{band_ratio:>7s}  "
                f"{_fmt_sci(b_m, b_se):>15s}  {_fmt_sci(k0_m, k0_se):>10s}  "
                f"{ok:3d}  {family_times[family][nl]:4.0f}s"
            )
        print()

    print("Exponent fits on family-mean decoherence depth: 1 - pur_cl ~= C * N^alpha")
    for family in args.families:
        purity_by_n = {
            nl: family_results[family][nl]["pur_cl"]
            for nl in args.n_layers
            if family_results[family][nl]["pur_cl"]
        }
        mean_points = [
            (nl, sum(vals) / len(vals))
            for nl, vals in sorted(purity_by_n.items())
        ]
        fit = fit_decoherence_alpha(mean_points)
        boot = bootstrap_alpha(
            purity_by_n,
            n_boot=args.n_boot,
            rng_seed=args.bootstrap_seed + 97 * (args.families.index(family) + 1),
        )
        if fit is None:
            print(f"  {family:>8s}: FAIL")
            continue
        alpha, coeff, r2 = fit
        if boot is None:
            print(
                f"  {family:>8s}: alpha={alpha:+.3f}, C={coeff:.4f}, R^2={r2:.3f}, "
                f"bootstrap=FAIL"
            )
            continue
        boot_mean, lo, hi = boot
        print(
            f"  {family:>8s}: alpha={alpha:+.3f}, C={coeff:.4f}, R^2={r2:.3f}, "
            f"bootstrap alpha={boot_mean:+.3f} [{lo:+.3f}, {hi:+.3f}]"
        )

    print()
    print("Readout:")
    print("  - Born safety means |I3|/P stays near machine precision.")
    print("  - k=0 must remain zero if gravity stays purely phase-mediated.")
    print("  - grav_band averages the same centroid shift across a small k window")
    print("    to reduce sign flips from single-k phase oscillations.")


if __name__ == "__main__":
    main()
