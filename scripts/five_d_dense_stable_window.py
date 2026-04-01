#!/usr/bin/env python3
"""5D dense stable-window extension.

This is a focused follow-up to the dense 5D robustness map. The question is
not whether a high-alpha corner exists, but whether the retained dense
window actually contains a stable positive regime with repeated significance
across the paired mass-law samples.

The sweep stays deliberately local:
  - centered on the stability-aware retained window
  - small neighborhood in nodes / radius / range
  - same paired mass-law measurement as the pilot
  - stability-aware ranking, not raw alpha ranking

PStack experiment: five-d-dense-stable-window
"""

from __future__ import annotations

import os
import sys
from statistics import mean

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.five_d_dense_pilot import measure_config, verdict

N_SEEDS = 10
GAP = 5.0

# Tight neighborhood around the retained stable-ish positive window.
# The retained corner from the robustness map was nodes=100, rad=6.5, range=5.0.
CONFIGS = [
    ("edge-low", 90, 6.25, 5.0),
    ("low-center", 90, 6.50, 5.0),
    ("edge-high", 90, 6.75, 5.0),
    ("center-low", 100, 6.25, 5.0),
    ("center", 100, 6.50, 5.0),
    ("center-high", 100, 6.75, 5.0),
    ("top-low", 110, 6.25, 5.0),
    ("top-center", 110, 6.50, 5.0),
    ("top-high", 110, 6.75, 5.0),
]

ALPHA_TARGET = 0.63


def _fmt_alpha(row) -> str:
    return "NA" if row["alpha"] is None else f"{row['alpha']:.3f}"


def _positive_mass_rows(row):
    return [
        (target_n, avg, se, t)
        for target_n, avg, se, t in row["mass_summaries"]
        if avg > 0 and t > 1.5
    ]


def _positive_support_count(row) -> int:
    return len(_positive_mass_rows(row))


def _positive_t_floor(row) -> float:
    rows = _positive_mass_rows(row)
    if not rows:
        return float("-inf")
    return min(t for _n, _avg, _se, t in rows)


def _positive_t_mean(row) -> float:
    rows = _positive_mass_rows(row)
    if not rows:
        return float("-inf")
    return mean(t for _n, _avg, _se, t in rows)


def _stability_score(row):
    """Rank by repeated support first, then significance, then consistency."""
    alpha = row["alpha"]
    return (
        _positive_support_count(row),
        _positive_t_floor(row),
        _positive_t_mean(row),
        row["valid_rate"],
        -abs((alpha if alpha is not None else 0.0) - ALPHA_TARGET),
        row["max_t"],
    )


def _stable_positive_row(rows):
    candidates = [
        row
        for row in rows
        if row["alpha"] is not None
        and row["alpha"] > 0.2
        and row["max_t"] > 1.5
        and row["valid_rate"] >= 0.75
    ]
    if not candidates:
        return None
    return max(candidates, key=_stability_score)


def main() -> None:
    print("=" * 78)
    print("5D DENSE STABLE WINDOW")
    print("  4 spatial dims + 1 causal dim")
    print("  Goal: test whether the retained positive dense window is genuinely stable")
    print("=" * 78)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  alpha target for stability tie-breaks: {ALPHA_TARGET:.2f}")
    print("  neighborhood: tight shell around nodes=100, rad=6.5, range=5.0")
    print()

    rows = []
    for label, nodes_per_layer, connect_radius, spatial_range in CONFIGS:
        row = measure_config(
            nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius,
            spatial_range=spatial_range,
            gap=GAP,
            n_seeds=N_SEEDS,
        )
        row["label"] = label
        rows.append(row)

    print("CONFIG SWEEP")
    print(
        f"  {'label':>12s}  {'nodes':>5s}  {'rad':>4s}  {'range':>5s}  {'valid':>5s}  "
        f"{'out_deg':>7s}  {'reach':>7s}  {'cand':>5s}  {'alpha':>7s}  {'max_t':>5s}  "
        f"{'pos':>3s}  {'p_tmin':>6s}  verdict"
    )
    print(f"  {'-' * 108}")

    best_stable_row = None
    best_valid_row = None
    for row in rows:
        alpha_str = _fmt_alpha(row)
        stable_v = "STABLE POS" if _positive_support_count(row) >= 4 and row["max_t"] > 2.0 else verdict(row)
        print(
            f"  {row['label']:>12s}  {row['nodes_per_layer']:5d}  {row['connect_radius']:4.2f}  "
            f"{row['spatial_range']:5.2f}  {row['valid_rate']:5.2f}  {row['avg_out']:7.3f}  "
            f"{row['avg_reach']:7.3f}  {row['avg_candidates']:5.1f}  {alpha_str:>7s}  "
            f"{row['max_t']:5.2f}  {_positive_support_count(row):3d}  "
            f"{_positive_t_floor(row):6.2f}  {stable_v}"
        )
        if best_valid_row is None or row["valid_rate"] > best_valid_row["valid_rate"]:
            best_valid_row = row
        if best_stable_row is None or _stability_score(row) > _stability_score(best_stable_row):
            best_stable_row = row

    print()
    print("MASS-LAW DETAIL")
    for row in rows:
        alpha_str = _fmt_alpha(row)
        print(
            f"  {row['label']}: alpha={alpha_str}, valid={row['valid_rate']:.2f}, "
            f"reach={row['avg_reach']:.3f}, pos={_positive_support_count(row)}, "
            f"p_tmin={_positive_t_floor(row):.2f}"
        )
        for target_n, avg, se, t in row["mass_summaries"]:
            print(
                f"    n={target_n:2d}, shift={avg:+.4f}, SE={se:.4f}, t={t:+.2f}"
            )

    print()
    print("RANKING")
    ranked = sorted(rows, key=_stability_score, reverse=True)
    for idx, row in enumerate(ranked, start=1):
        print(
            f"  {idx:>2d}. {row['label']:>12s} | alpha={_fmt_alpha(row):>7s} | "
            f"pos={_positive_support_count(row):d} | p_tmin={_positive_t_floor(row):5.2f} | "
            f"valid={row['valid_rate']:.2f} | max_t={row['max_t']:.2f}"
        )

    print()
    print("VERDICT")
    if best_stable_row is not None and _positive_support_count(best_stable_row) >= 4:
        print(
            "  A genuinely stable positive window is present in the dense 5D neighborhood: "
            f"{best_stable_row['label']} ranks best by support/significance, with alpha "
            f"{best_stable_row['alpha']:.3f} at nodes={best_stable_row['nodes_per_layer']}, "
            f"rad={best_stable_row['connect_radius']}, range={best_stable_row['spatial_range']}."
        )
        print(
            f"  Best stable support = {_positive_support_count(best_stable_row)} positive mass points "
            f"(p_tmin={_positive_t_floor(best_stable_row):.2f}, max_t={best_stable_row['max_t']:.2f})."
        )
    elif best_stable_row is not None:
        print(
            "  The dense 5D window is positive but still looks corner-like rather than fully stable: "
            f"{best_stable_row['label']} is the best support/significance compromise."
        )
    else:
        print(
            "  No stable positive mass-law window emerged in the dense 5D neighborhood. "
            "The signal remains connectivity-limited."
        )

    if best_valid_row is not None:
        print(
            f"  Highest valid-setup rate = {best_valid_row['valid_rate']:.2f} at "
            f"nodes={best_valid_row['nodes_per_layer']}, rad={best_valid_row['connect_radius']}, "
            f"range={best_valid_row['spatial_range']}"
        )
    print("=" * 78)


if __name__ == "__main__":
    main()
