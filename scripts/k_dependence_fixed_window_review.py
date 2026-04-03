#!/usr/bin/env python3
"""Review-safe k-dependence rerun with a fixed N window.

This script is a hardened follow-up to ``k_dependence_ceiling.py``.
It keeps the same N window for every k, requires the same complete seed
set across the whole k x N grid, and reports uncertainty using:

1. per-seed power-law slopes
2. bootstrap confidence intervals on the mean slope

The goal is to decide whether the earlier alpha(k) variation survives
once the fit window is fixed and the seed-level spread is exposed.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
from dataclasses import dataclass
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.k_dependence_ceiling import pur_min_single_k


@dataclass
class FitResult:
    alpha: float
    intercept: float
    r2: float


def fit_power_law(ns: Iterable[int], ys: Iterable[float]) -> FitResult | None:
    xs = [math.log(n) for n in ns]
    zs = [math.log(y) for y in ys if y > 0]
    if len(xs) != len(zs) or len(xs) < 3:
        return None
    n = len(xs)
    mx = sum(xs) / n
    my = sum(zs) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (z - my) for x, z in zip(xs, zs))
    syy = sum((z - my) ** 2 for z in zs)
    if sxx <= 0 or syy <= 0:
        return None
    alpha = sxy / sxx
    intercept = my - alpha * mx
    r2 = (sxy ** 2) / (sxx * syy)
    return FitResult(alpha=alpha, intercept=intercept, r2=r2)


def bootstrap_mean(values: list[float], n_samples: int, rng: random.Random) -> tuple[float, float, float]:
    if not values:
        return math.nan, math.nan, math.nan
    if len(values) == 1:
        v = values[0]
        return v, v, v
    draws = []
    for _ in range(n_samples):
        sample = [values[rng.randrange(len(values))] for _ in values]
        draws.append(sum(sample) / len(sample))
    draws.sort()
    lo = draws[max(0, int(0.025 * (len(draws) - 1)))]
    hi = draws[min(len(draws) - 1, int(0.975 * (len(draws) - 1)))]
    mean = sum(values) / len(values)
    return mean, lo, hi


def fmt_prob(v: float) -> str:
    return f"{v:.4f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-list", nargs="+", type=int, default=[25, 30, 40, 60, 80])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--k-values", nargs="+", type=float, default=[1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0])
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    n_list = list(args.n_list)
    k_values = list(args.k_values)
    rng = random.Random(12345)

    print("=" * 92)
    print("K-DEPENDENCE REVIEW-SAFE RERUN")
    print("  fixed N window across k, shared seed set, per-seed slopes + bootstrap CI")
    print(f"  N window = {n_list}")
    print(f"  seeds = {args.n_seeds}, bootstrap samples = {args.bootstrap_samples}")
    print("=" * 92)
    print()

    # Build the full seed x k x N table first so we can keep the same
    # seed set across every k.
    table: dict[float, dict[int, dict[int, float]]] = {}
    complete_seeds = set(seeds)

    for k in k_values:
        table[k] = {}
        for seed in seeds:
            per_n: dict[int, float] = {}
            ok = True
            for nl in n_list:
                v = pur_min_single_k(nl, k, seed)
                if v is None or not math.isfinite(v) or v >= 1.0:
                    ok = False
                    break
                per_n[nl] = max(1e-15, 1.0 - v)
            if ok and len(per_n) == len(n_list):
                table[k][seed] = per_n
            else:
                complete_seeds.discard(seed)

    complete_seeds = sorted(complete_seeds)

    print(f"Complete shared seeds across all k and N: {len(complete_seeds)} / {len(seeds)}")
    print()

    header = (
        f"{'k':>5s}  {'n_ok':>4s}  {'seed_alpha':>11s}  {'SE':>7s}  "
        f"{'boot95%':>17s}  {'pooled_alpha':>13s}  {'pooled_R2':>9s}"
    )
    print(header)
    print("-" * len(header))

    for k in k_values:
        seed_alphas: list[float] = []
        pooled_curve = {nl: [] for nl in n_list}

        for seed in complete_seeds:
            per_n = table.get(k, {}).get(seed)
            if not per_n:
                continue
            fit = fit_power_law(n_list, [per_n[nl] for nl in n_list])
            if fit is not None:
                seed_alphas.append(fit.alpha)
                for nl in n_list:
                    pooled_curve[nl].append(per_n[nl])

        pooled_vals = [sum(pooled_curve[nl]) / len(pooled_curve[nl]) for nl in n_list if pooled_curve[nl]]
        pooled_fit = fit_power_law([nl for nl in n_list if pooled_curve[nl]], pooled_vals)
        if seed_alphas:
            mean_alpha = sum(seed_alphas) / len(seed_alphas)
            if len(seed_alphas) > 1:
                var = sum((a - mean_alpha) ** 2 for a in seed_alphas) / (len(seed_alphas) - 1)
                se = math.sqrt(var / len(seed_alphas))
            else:
                se = 0.0
            boot_mean, boot_lo, boot_hi = bootstrap_mean(seed_alphas, args.bootstrap_samples, rng)
            boot_str = f"[{boot_lo:+.3f}, {boot_hi:+.3f}]"
            pooled_alpha = f"{pooled_fit.alpha:+.3f}" if pooled_fit else "N/A"
            pooled_r2 = f"{pooled_fit.r2:.3f}" if pooled_fit else "N/A"
            print(f"{k:5.1f}  {len(seed_alphas):4d}  {mean_alpha:+11.3f}  {se:7.3f}  {boot_str:>17s}  {pooled_alpha:>13s}  {pooled_r2:>9s}")
        else:
            print(f"{k:5.1f}  {0:4d}  {'FAIL':>11s}  {'FAIL':>7s}  {'FAIL':>17s}  {'FAIL':>13s}  {'FAIL':>9s}")

    print()
    print("Interpretation guide:")
    print("  - seed_alpha: mean of per-seed slope fits on the fixed N window")
    print("  - boot95%: bootstrap CI on the mean seed_alpha")
    print("  - pooled_alpha: fit to the mean curve, shown only as a diagnostic")
    print()
    print("Review-safe rule:")
    print("  If the bootstrapped intervals overlap heavily across k, the old alpha(k)")
    print("  story was mostly a fit-window artifact. If they separate cleanly, the k")
    print("  dependence survives on a fixed window.")


if __name__ == "__main__":
    main()
