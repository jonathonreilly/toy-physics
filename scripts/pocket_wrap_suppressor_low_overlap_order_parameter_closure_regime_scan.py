#!/usr/bin/env python3
"""Scan closure regimes and asymmetry sign bands for the shared low-overlap bucket."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


SUBTYPE_ORDER = [
    "add1-sensitive",
    "add4-sensitive",
    "pair-only-sensitive",
]

CLOSURE_REGIMES = [
    ("<=9", lambda value: value <= 9.0),
    ("9-11", lambda value: 9.0 < value < 11.0),
    (">=11", lambda value: value >= 11.0),
]

SIGN_BANDS = [
    ("negative", lambda value, epsilon: value < -epsilon),
    ("zero", lambda value, epsilon: -epsilon <= value <= epsilon),
    ("positive", lambda value, epsilon: value > epsilon),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--zero-epsilon", type=float, default=1e-9)
    return parser


def closure_regime(value: float) -> str:
    for label, predicate in CLOSURE_REGIMES:
        if predicate(value):
            return label
    raise ValueError(f"unclassified closure regime for value={value}")


def sign_band(value: float, zero_epsilon: float) -> str:
    for label, predicate in SIGN_BANDS:
        if predicate(value, zero_epsilon):
            return label
    raise ValueError(f"unclassified sign band for value={value}")


def dominant_subtype(counts: Counter[str], total: int) -> str:
    if total == 0:
        return "-"
    subtype, count = max(
        counts.items(),
        key=lambda item: (item[1], -SUBTYPE_ORDER.index(item[0])),
    )
    return f"{subtype}:{count}/{total}"


def render_cell_table(rows: list[object], zero_epsilon: float) -> str:
    lines = [
        "Closure Regime x Asymmetry Sign Bands",
        "=====================================",
        "closure_regime | sign_band | rows | add1 | add4 | pair | dominant",
        "---------------+-----------+------+-----+------+------+------------------------",
    ]
    for closure_label, _closure_predicate in CLOSURE_REGIMES:
        for sign_label, _sign_predicate in SIGN_BANDS:
            matched_rows = [
                row
                for row in rows
                if closure_regime(float(getattr(row, "mid_anchor_closure_peak"))) == closure_label
                and sign_band(
                    float(getattr(row, "anchor_closure_intensity_gap")),
                    zero_epsilon,
                )
                == sign_label
            ]
            counts = Counter(getattr(row, "subtype") for row in matched_rows)
            lines.append(
                f"{closure_label:>14} | {sign_label:<9} | {len(matched_rows):>4} | "
                f"{counts['add1-sensitive']:>3} | {counts['add4-sensitive']:>4} | "
                f"{counts['pair-only-sensitive']:>4} | "
                f"{dominant_subtype(counts, len(matched_rows))}"
            )
    return "\n".join(lines)


def render_marginal_table(rows: list[object], zero_epsilon: float) -> str:
    lines = [
        "Marginal Summaries",
        "==================",
        "slice | bucket | rows | add1 | add4 | pair | dominant",
        "------+--------+------+-----+------+------+------------------------",
    ]
    for closure_label, _closure_predicate in CLOSURE_REGIMES:
        matched_rows = [
            row
            for row in rows
            if closure_regime(float(getattr(row, "mid_anchor_closure_peak"))) == closure_label
        ]
        counts = Counter(getattr(row, "subtype") for row in matched_rows)
        lines.append(
            f"closure | {closure_label:>6} | {len(matched_rows):>4} | "
            f"{counts['add1-sensitive']:>3} | {counts['add4-sensitive']:>4} | "
            f"{counts['pair-only-sensitive']:>4} | {dominant_subtype(counts, len(matched_rows))}"
        )
    for sign_label, _sign_predicate in SIGN_BANDS:
        matched_rows = [
            row
            for row in rows
            if sign_band(
                float(getattr(row, "anchor_closure_intensity_gap")),
                zero_epsilon,
            )
            == sign_label
        ]
        counts = Counter(getattr(row, "subtype") for row in matched_rows)
        lines.append(
            f"sign    | {sign_label:>6} | {len(matched_rows):>4} | "
            f"{counts['add1-sensitive']:>3} | {counts['add4-sensitive']:>4} | "
            f"{counts['pair-only-sensitive']:>4} | {dominant_subtype(counts, len(matched_rows))}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap closure-regime scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    print()
    print("Low-Overlap Closure-Regime Scan")
    print("================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows={len(rows)}")
    print("closure_regimes=<=9,9-11,>=11")
    print(f"sign_bands=negative|zero|positive (zero_epsilon={args.zero_epsilon:g})")
    print()
    print(render_cell_table(rows, args.zero_epsilon))
    print()
    print(render_marginal_table(rows, args.zero_epsilon))
    print()
    print(
        "low-overlap closure-regime scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
