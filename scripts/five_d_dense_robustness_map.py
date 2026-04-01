#!/usr/bin/env python3
"""5D dense robustness map.

This is a bounded follow-up to the dense 5D pilot. The question is not
whether 5D can be made to produce any positive mass-law signal at all, but
whether the positive dense window widens into a stable regime or stays a
narrow connectivity-limited corner.

The sweep stays local and honest:
  - gap fixed at the retained dense modular value
  - small neighborhood of nearby dense configurations
  - more seeds than the pilot, but still bounded
  - same paired mass-law measurement as the pilot

The retained pilot suggested one positive dense corner around
nodes=100, rad=6.5, range=5.0. This script checks the nearby flanks.

PStack experiment: five-d-dense-robustness-map
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.five_d_dense_pilot import measure_config, verdict

N_SEEDS = 8
GAP = 5.0

# Neighborhood around the dense pilot corner.
CONFIGS = [
    ("low-dense", 80, 6.0, 5.5),
    ("pilot-left", 80, 6.5, 5.0),
    ("pilot", 100, 6.5, 5.0),
    ("pilot-right", 120, 6.5, 5.0),
    ("denser-radius", 100, 7.0, 5.0),
    ("tighter-range", 100, 6.5, 4.5),
    ("denser-both", 120, 7.0, 5.0),
]


def _fmt_alpha(row) -> str:
    return "NA" if row["alpha"] is None else f"{row['alpha']:.3f}"


def main() -> None:
    print("=" * 78)
    print("5D DENSE ROBUSTNESS MAP")
    print("  4 spatial dims + 1 causal dim")
    print("  Goal: check whether the positive dense 5D window widens or stays narrow")
    print("=" * 78)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print("  neighborhood: around the dense pilot corner at nodes=100, rad=6.5, range=5.0")
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
        f"{'out_deg':>7s}  {'reach':>7s}  {'cand':>5s}  {'alpha':>7s}  {'max_t':>5s}  verdict"
    )
    print(f"  {'-' * 98}")

    positive_rows = []
    best_alpha_row = None
    best_valid_row = None
    for row in rows:
        alpha_str = _fmt_alpha(row)
        v = verdict(row)
        print(
            f"  {row['label']:>12s}  {row['nodes_per_layer']:5d}  {row['connect_radius']:4.1f}  "
            f"{row['spatial_range']:5.1f}  {row['valid_rate']:5.2f}  {row['avg_out']:7.3f}  "
            f"{row['avg_reach']:7.3f}  {row['avg_candidates']:5.1f}  {alpha_str:>7s}  "
            f"{row['max_t']:5.2f}  {v}"
        )
        if row["alpha"] is not None and row["alpha"] > 0.2 and row["max_t"] > 2.0 and row["valid_rate"] > 0.5:
            positive_rows.append(row)
        if row["alpha"] is not None and (best_alpha_row is None or row["alpha"] > best_alpha_row["alpha"]):
            best_alpha_row = row
        if best_valid_row is None or row["valid_rate"] > best_valid_row["valid_rate"]:
            best_valid_row = row

    print()
    print("MASS-LAW DETAIL")
    for row in rows:
        if not row["mass_summaries"]:
            continue
        alpha_str = _fmt_alpha(row)
        print(
            f"  {row['label']}: alpha={alpha_str}, valid={row['valid_rate']:.2f}, "
            f"reach={row['avg_reach']:.3f}"
        )
        for target_n, avg, se, t in row["mass_summaries"]:
            print(
                f"    n={target_n:2d}, shift={avg:+.4f}, SE={se:.4f}, t={t:+.2f}"
            )

    print()
    print("VERDICT")
    if positive_rows:
        if len(positive_rows) >= 3:
            print(
                "  The dense 5D positive window looks broader than a single isolated corner, "
                "but it is still limited to the dense modular neighborhood tested here."
            )
        else:
            print(
                "  The positive 5D signal survives only in a narrow dense corner; the surrounding "
                "configs weaken quickly, so the window still looks connectivity-limited."
            )
        best = best_alpha_row or positive_rows[0]
        print(
            f"  Best alpha = {best['alpha']:.3f} at nodes={best['nodes_per_layer']}, "
            f"rad={best['connect_radius']}, range={best['spatial_range']}"
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
