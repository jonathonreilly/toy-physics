#!/usr/bin/env python3
"""3+1D Dirac weak-coupling scan with dimensionless geometry control.

This scan reuses the current v4 Dirac walk helpers and asks a narrower
question:

    If we reduce the gravitational coupling and lengthen propagation while
    keeping delta = d / n and lambda = L / n under control, do the remaining
    gravity failures improve?

The two retained outputs are:

1. sign stability over N (propagation layers) at fixed dimensionless geometry
2. offset-distance-law behavior across delta

The scan stays on the periodic v4 picture so the comparison is directly tied
to the current retained periodic sign windows.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import statistics
import sys

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_dirac_walk_3plus1d_v4_convergence import (  # noqa: E402
    fit_power_law,
    run_bias_case,
)


DEFAULT_MASS0 = 0.30
DEFAULT_STRENGTHS = (5e-4, 2e-4, 1e-4, 5e-5)
DEFAULT_SIZES = (17, 21, 25, 29)
DEFAULT_LAMBDA_TARGETS = (0.40, 0.55, 0.70)
DEFAULT_DELTA_TARGETS = (0.10, 0.14, 0.18, 0.22)
EPS = 1e-12


@dataclass(frozen=True)
class GeometryCase:
    n: int
    layers: int
    offset: int
    lambda_target: float
    delta_target: float
    lambda_ratio: float
    delta_ratio: float


@dataclass(frozen=True)
class SampleRow:
    n: int
    layers: int
    offset: int
    lambda_target: float
    delta_target: float
    lambda_ratio: float
    delta_ratio: float
    toward: float
    away: float
    bias: float


def parse_float_list(text: str) -> list[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def parse_int_list(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def clamp_offset(offset: int, n: int) -> int:
    return max(1, min(offset, n // 2 - 1))


def make_case(n: int, lambda_target: float, delta_target: float) -> GeometryCase:
    layers = max(2, int(round(lambda_target * n)))
    offset = clamp_offset(int(round(delta_target * n)), n)
    return GeometryCase(
        n=n,
        layers=layers,
        offset=offset,
        lambda_target=lambda_target,
        delta_target=delta_target,
        lambda_ratio=layers / n,
        delta_ratio=offset / n,
    )


def sign_char(value: float) -> str:
    if value > EPS:
        return "T"
    if value < -EPS:
        return "A"
    return "0"


def safe_mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else float("nan")


def fit_magnitude_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float]:
    xs = np.array(xs_in, dtype=float)
    ys = np.array(ys_in, dtype=float)
    mask = np.isfinite(xs) & np.isfinite(ys) & (xs > 0.0) & (ys > 0.0)
    if int(np.sum(mask)) < 3:
        return float("nan"), 0.0

    x = np.log10(xs[mask])
    y = np.log10(ys[mask])
    coeffs = np.polyfit(x, y, 1)
    pred = np.polyval(coeffs, x)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coeffs[0]), r2


def format_bias(value: float) -> str:
    return f"{value:+.4e}{sign_char(value)}"


def evaluate_rows(
    mass0: float,
    strength: float,
    sizes: list[int],
    lambda_target: float,
    delta_target: float,
) -> list[SampleRow]:
    rows: list[SampleRow] = []
    for n in sizes:
        case = make_case(n, lambda_target, delta_target)
        result = run_bias_case(
            boundary="periodic",
            n=case.n,
            n_layers=case.layers,
            mass0=mass0,
            strength=strength,
            offset=case.offset,
        )
        rows.append(
            SampleRow(
                n=case.n,
                layers=case.layers,
                offset=case.offset,
                lambda_target=case.lambda_target,
                delta_target=case.delta_target,
                lambda_ratio=case.lambda_ratio,
                delta_ratio=case.delta_ratio,
                toward=float(result["toward"]),
                away=float(result["away"]),
                bias=float(result["bias"]),
            )
        )
    return rows


def summarize_lambda_block(rows_by_delta: dict[float, list[SampleRow]]) -> dict[str, object]:
    delta_rows = []
    stable_rows = 0
    stable_positive = 0

    for delta_target in sorted(rows_by_delta):
        rows = rows_by_delta[delta_target]
        biases = [row.bias for row in rows]
        signs = [sign_char(value) for value in biases if sign_char(value) != "0"]
        consistent = bool(signs) and len(set(signs)) == 1
        if consistent:
            stable_rows += 1
            if signs[0] == "T":
                stable_positive += 1

        mean_bias = safe_mean(biases)
        mean_abs_bias = safe_mean([abs(value) for value in biases])
        mean_delta = safe_mean([row.delta_ratio for row in rows])
        delta_rows.append(
            {
                "delta_target": delta_target,
                "mean_bias": mean_bias,
                "mean_abs_bias": mean_abs_bias,
                "mean_delta": mean_delta,
                "signs": "".join(sign_char(value) for value in biases),
                "consistent": consistent,
                "rows": rows,
            }
        )

    fit_x = [float(item["mean_delta"]) for item in delta_rows if np.isfinite(item["mean_bias"])]
    fit_y = [float(item["mean_bias"]) for item in delta_rows if np.isfinite(item["mean_bias"])]
    fit = fit_power_law(fit_x, fit_y) if len(fit_x) >= 3 else (float("nan"), 0.0)
    abs_fit = fit_magnitude_power_law(
        [float(item["mean_delta"]) for item in delta_rows],
        [float(item["mean_abs_bias"]) for item in delta_rows],
    )

    return {
        "delta_rows": delta_rows,
        "stable_rows": stable_rows,
        "stable_positive": stable_positive,
        "fit": fit,
        "abs_fit": abs_fit,
    }


def print_block(
    mass0: float,
    strength: float,
    sizes: list[int],
    lambda_target: float,
    delta_targets: list[float],
) -> dict[str, object]:
    rows_by_delta: dict[float, list[SampleRow]] = {}
    for delta_target in delta_targets:
        rows_by_delta[delta_target] = evaluate_rows(mass0, strength, sizes, lambda_target, delta_target)

    summary = summarize_lambda_block(rows_by_delta)

    print(f"lambda_target={lambda_target:.2f}")
    print(
        f"{'delta':>7s}  "
        + "  ".join(f"n={n:>2d}" for n in sizes)
        + "  |  stable  mean|bias|  mean_delta"
    )
    print("-" * (11 + len(sizes) * 14 + 36))
    for item in summary["delta_rows"]:
        rows = item["rows"]
        biases = "  ".join(f"{format_bias(row.bias):>13s}" for row in rows)
        stable = "YES" if item["consistent"] else "NO"
        print(
            f"{float(item['delta_target']):7.2f}  "
            f"{biases}  |  {stable:^6s}  "
            f"{float(item['mean_abs_bias']):10.4e}  "
            f"{float(item['mean_delta']):10.4f}"
        )

    fit_alpha, fit_r2 = summary["fit"]
    abs_fit_alpha, abs_fit_r2 = summary["abs_fit"]
    print(
        f"  sign-stable delta rows: {summary['stable_rows']}/{len(delta_targets)}"
        f"   positive-stable rows: {summary['stable_positive']}/{len(delta_targets)}"
    )
    if np.isfinite(fit_alpha):
        print(f"  delta-law fit: alpha={fit_alpha:.3f}, R^2={fit_r2:.4f}")
    else:
        print("  delta-law fit: not available")
    if np.isfinite(abs_fit_alpha):
        print(f"  |bias| law fit: alpha={abs_fit_alpha:.3f}, R^2={abs_fit_r2:.4f}")
    else:
        print("  |bias| law fit: not available")
    print()
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mass0", type=float, default=DEFAULT_MASS0)
    parser.add_argument(
        "--strengths",
        default=",".join(f"{value:.1e}" for value in DEFAULT_STRENGTHS),
        help="comma-separated gravity strengths, from baseline to weaker coupling",
    )
    parser.add_argument(
        "--sizes",
        default=",".join(str(value) for value in DEFAULT_SIZES),
        help="comma-separated lattice sizes n",
    )
    parser.add_argument(
        "--lambda-targets",
        dest="lambda_targets",
        default=",".join(f"{value:.2f}" for value in DEFAULT_LAMBDA_TARGETS),
        help="comma-separated lambda = L/n targets",
    )
    parser.add_argument(
        "--delta-targets",
        dest="delta_targets",
        default=",".join(f"{value:.2f}" for value in DEFAULT_DELTA_TARGETS),
        help="comma-separated delta = d/n targets",
    )
    args = parser.parse_args()

    strengths = parse_float_list(args.strengths)
    sizes = parse_int_list(args.sizes)
    lambda_targets = parse_float_list(args.lambda_targets)
    delta_targets = parse_float_list(args.delta_targets)

    print("=" * 88)
    print("FRONTIER: 3+1D DIRAC WALK WEAK-COUPLING / LONG-PROPAGATION SCAN")
    print("=" * 88)
    print(f"mass0={args.mass0:.3f}")
    print(f"strengths: {', '.join(f'{value:.1e}' for value in strengths)}")
    print(f"sizes: {sizes}")
    print(f"lambda targets: {lambda_targets}")
    print(f"delta targets: {delta_targets}")
    print("baseline picture: periodic v4 reversed coupling, m(r)=m0*(1+f(r))")
    print("outputs: sign stability over N, and delta-law behavior at fixed dimensionless geometry")
    print()

    block_summaries: dict[tuple[float, float], dict[str, object]] = {}
    for strength in strengths:
        print("=" * 88)
        print(f"STRENGTH = {strength:.1e}")
        print("=" * 88)
        for lambda_target in lambda_targets:
            block_summaries[(strength, lambda_target)] = print_block(
                args.mass0, strength, sizes, lambda_target, delta_targets
            )

    print("=" * 88)
    print("CROSS-STRENGTH SUMMARY")
    print("=" * 88)
    for strength in strengths:
        summaries = [block_summaries[(strength, lam)] for lam in lambda_targets]
        stable_rows = [int(summary["stable_rows"]) for summary in summaries]
        positive_rows = [int(summary["stable_positive"]) for summary in summaries]
        fits = [summary["fit"] for summary in summaries]
        abs_fits = [summary["abs_fit"] for summary in summaries]
        best_fit = max(
            (fit for fit in fits if np.isfinite(fit[0])),
            key=lambda pair: pair[1],
            default=(float("nan"), 0.0),
        )
        best_abs_fit = max(
            (fit for fit in abs_fits if np.isfinite(fit[0])),
            key=lambda pair: pair[1],
            default=(float("nan"), 0.0),
        )
        print(
            f"strength {strength:.1e}: "
            f"stable delta rows {sum(stable_rows)}/{len(delta_targets) * len(lambda_targets)}, "
            f"positive-stable rows {sum(positive_rows)}/{len(delta_targets) * len(lambda_targets)}"
        )
        if np.isfinite(best_fit[0]):
            print(f"  best delta-law fit: alpha={best_fit[0]:.3f}, R^2={best_fit[1]:.4f}")
        else:
            print("  best delta-law fit: not available")
        if np.isfinite(best_abs_fit[0]):
            print(f"  best |bias| fit: alpha={best_abs_fit[0]:.3f}, R^2={best_abs_fit[1]:.4f}")
        else:
            print("  best |bias| fit: not available")

    baseline = block_summaries[(strengths[0], lambda_targets[0])]
    weakest = block_summaries[(strengths[-1], lambda_targets[-1])]
    print()
    print("BASELINE VS WEAKEST")
    print(
        f"  baseline strength={strengths[0]:.1e}, lambda={lambda_targets[0]:.2f}: "
        f"stable delta rows {baseline['stable_rows']}/{len(delta_targets)}, "
        f"positive-stable rows {baseline['stable_positive']}/{len(delta_targets)}, "
        f"delta-law fit={baseline['fit'][0]:.3f} / {baseline['fit'][1]:.4f}, "
        f"|bias| fit={baseline['abs_fit'][0]:.3f} / {baseline['abs_fit'][1]:.4f}"
    )
    print(
        f"  weakest strength={strengths[-1]:.1e}, lambda={lambda_targets[-1]:.2f}: "
        f"stable delta rows {weakest['stable_rows']}/{len(delta_targets)}, "
        f"positive-stable rows {weakest['stable_positive']}/{len(delta_targets)}, "
        f"delta-law fit={weakest['fit'][0]:.3f} / {weakest['fit'][1]:.4f}, "
        f"|bias| fit={weakest['abs_fit'][0]:.3f} / {weakest['abs_fit'][1]:.4f}"
    )


if __name__ == "__main__":
    main()
