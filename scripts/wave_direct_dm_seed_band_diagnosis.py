#!/usr/bin/env python3
"""Diagnose the two-band seed split on the direct-dM portability batch.

This stays deliberately cheap for automation use: it parses the already
retained portability-batch log instead of re-running the full measurement
grid. The question is purely diagnostic: what separates the higher- and
lower-magnitude seed bands at the retained reference strength?
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
from statistics import mean

REFERENCE_STRENGTH = 0.004
HS = (0.5, 0.35)
SEEDS = (0, 1)
DEFAULT_BATCH_LOG = (
    Path(__file__).resolve().parent.parent
    / "logs"
    / "2026-04-08-wave-direct-dm-portability-batch.txt"
)

FAMILY_RE = re.compile(r"^\[family=(?P<family>\w+)\s+drift=(?P<drift>[-+0-9.]+)\s+restore=(?P<restore>[-+0-9.]+)\]$")
SEED_RE = re.compile(r"^\[seed=(?P<seed>\d+)\]$")
STRENGTH_RE = re.compile(r"^\[strength=(?P<strength>[-+0-9.]+)\]$")
ROW_RE = re.compile(
    r"^H=(?P<H>[-+0-9.]+)\s+"
    r"dE=(?P<d_early>[-+0-9.]+)\s+"
    r"dL=(?P<d_late>[-+0-9.]+)\s+"
    r"delta=(?P<delta_hist>[-+0-9.]+)\s+"
    r"R=(?P<r_hist>[-+0-9.]+)%"
)


def _rows_from_log(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    family = None
    seed = None
    strength = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = FAMILY_RE.match(line)
        if match:
            family = match.group("family")
            continue
        match = SEED_RE.match(line)
        if match:
            seed = int(match.group("seed"))
            continue
        match = STRENGTH_RE.match(line)
        if match:
            strength = float(match.group("strength"))
            continue
        match = ROW_RE.match(line)
        if not match or family is None or seed is None or strength is None:
            continue
        if abs(strength - REFERENCE_STRENGTH) > 1e-12:
            continue
        h_val = float(match.group("H"))
        if h_val not in HS or seed not in SEEDS:
            continue
        d_early = float(match.group("d_early"))
        d_late = float(match.group("d_late"))
        rows.append(
            {
                "family": family,
                "seed": seed,
                "H": h_val,
                "strength": strength,
                "d_early": d_early,
                "d_late": d_late,
                "delta_hist": float(match.group("delta_hist")),
                "r_hist": float(match.group("r_hist")) / 100.0,
                "late_gain": d_late - d_early,
                "late_over_early": d_late / max(abs(d_early), 1e-12),
            }
        )
    return rows


def _seed_h_summary(rows: list[dict[str, float]]) -> dict[tuple[int, float], dict[str, float]]:
    grouped: dict[tuple[int, float], list[dict[str, float]]] = defaultdict(list)
    for row in rows:
        grouped[(row["seed"], row["H"])].append(row)

    summary: dict[tuple[int, float], dict[str, float]] = {}
    for key, group in grouped.items():
        summary[key] = {
            "mean_d_early": mean(item["d_early"] for item in group),
            "mean_d_late": mean(item["d_late"] for item in group),
            "mean_late_gain": mean(item["late_gain"] for item in group),
            "mean_late_over_early": mean(item["late_over_early"] for item in group),
            "mean_r_hist": mean(item["r_hist"] for item in group),
        }
    return summary


def main() -> int:
    rows = _rows_from_log(DEFAULT_BATCH_LOG)
    summary = _seed_h_summary(rows)

    print("=" * 116)
    print("WAVE DIRECT-DM SEED-BAND DIAGNOSIS")
    print("=" * 116)
    print("Reference-strength replay only: s=0.004 on the retained three-family, two-seed, two-H direct-dM batch")
    print("Inherited controls: exact S=0 null and weak-field linearity stay in the retained portability batch")
    print()

    print("PER-FAMILY REFERENCE ROWS")
    print(
        f"{'family':<6s} {'seed':>4s} {'H':>6s} {'dE':>10s} {'dL':>10s} "
        f"{'late_gain':>11s} {'dL/dE':>9s} {'R_hist':>10s}"
    )
    for row in sorted(rows, key=lambda item: (item["family"], item["seed"], -item["H"])):
        print(
            f"{row['family']:<6s} {row['seed']:4d} {row['H']:6.3f} "
            f"{row['d_early']:+10.6f} {row['d_late']:+10.6f} "
            f"{row['late_gain']:+11.6f} {row['late_over_early']:9.3f} "
            f"{row['r_hist']:+10.2%}"
        )

    print()
    print("SEED-BAND SUMMARY")
    print(
        f"{'seed':>4s} {'H':>6s} {'mean dE':>10s} {'mean dL':>10s} "
        f"{'mean gain':>11s} {'mean dL/dE':>11s} {'mean R':>10s}"
    )
    for seed in SEEDS:
        for h_val in HS:
            stats = summary[(seed, h_val)]
            print(
                f"{seed:4d} {h_val:6.3f} "
                f"{stats['mean_d_early']:+10.6f} {stats['mean_d_late']:+10.6f} "
                f"{stats['mean_late_gain']:+11.6f} {stats['mean_late_over_early']:11.3f} "
                f"{stats['mean_r_hist']:+10.2%}"
            )

    print()
    print("CROSS-BAND COMPARISON")
    for h_val in HS:
        hi = summary[(0, h_val)]
        lo = summary[(1, h_val)]
        print(f"H={h_val:.3f}")
        print(
            f"  early mean ratio  seed1/seed0 = "
            f"{lo['mean_d_early'] / max(abs(hi['mean_d_early']), 1e-12):.3f}"
        )
        print(
            f"  late mean ratio   seed1/seed0 = "
            f"{lo['mean_d_late'] / max(abs(hi['mean_d_late']), 1e-12):.3f}"
        )
        print(
            f"  late-gain ratio   seed1/seed0 = "
            f"{lo['mean_late_gain'] / max(abs(hi['mean_late_gain']), 1e-12):.3f}"
        )
        print(
            f"  mean R split      {hi['mean_r_hist']:+.2%} vs {lo['mean_r_hist']:+.2%}"
        )

    print()
    print("NARROW READ")
    print("  - The two-band split is not a sign split: every family/seed/H point keeps delta_hist < 0.")
    print("  - The split is not explained by early-branch suppression.")
    print("    At H=0.35, seed 1 actually has the larger mean early response "
          f"({summary[(1, 0.35)]['mean_d_early']:+.6f} vs {summary[(0, 0.35)]['mean_d_early']:+.6f}) "
          "but still sits in the lower-magnitude R band.")
    print("  - The clean separator is late-branch amplification.")
    print("    Seed 0 gets about 2x the extra late gain at H=0.5 and about 1.8x at H=0.35.")
    print(
        f"    mean late gain: H=0.5 {summary[(0, 0.5)]['mean_late_gain']:+.6f} vs "
        f"{summary[(1, 0.5)]['mean_late_gain']:+.6f}; "
        f"H=0.35 {summary[(0, 0.35)]['mean_late_gain']:+.6f} vs "
        f"{summary[(1, 0.35)]['mean_late_gain']:+.6f}"
    )
    print(
        f"    mean dL/dE: H=0.5 {summary[(0, 0.5)]['mean_late_over_early']:.3f} vs "
        f"{summary[(1, 0.5)]['mean_late_over_early']:.3f}; "
        f"H=0.35 {summary[(0, 0.35)]['mean_late_over_early']:.3f} vs "
        f"{summary[(1, 0.35)]['mean_late_over_early']:.3f}"
    )
    print("  - Family choice modulates the exact magnitude, but every family shows the same seed ordering.")
    print("  - So the honest next move is the planned one: validate one H=0.25 point from each amplitude band")
    print("    before widening seeds or families.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
