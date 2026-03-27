#!/usr/bin/env python3
"""Scan compact signed pocket-corridor clauses against the center-spine wide rescue law."""

from __future__ import annotations

import argparse
from datetime import datetime
from itertools import combinations, product
from math import gcd
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan import (  # noqa: E402
    Predicate,
    _metrics,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_interval_priority_scan import (  # noqa: E402
    _stable_interval,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument(
        "--bucket-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--bucket-key", default="00")
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument(
        "--corridor-features",
        nargs="+",
        default=[
            "delta_count_pocket_role_bridge__pocket_only",
            "delta_count_pocket_role_pocket_only__pocket_only",
            "delta_count_pocket_joined_bridge__pocket_only__present0",
            "delta_count_pocket_joined_bridge__pocket_only__present1",
            "delta_count_pocket_joined_pocket_only__pocket_only__present0",
            "delta_count_pocket_joined_pocket_only__pocket_only__present1",
        ],
    )
    parser.add_argument("--coefficients", nargs="+", type=int, default=[-2, -1, 1, 2])
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--top-k", type=int, default=16)
    return parser


def _mask_for(values: list[float], op: str, threshold: float) -> int:
    mask = 0
    for idx, value in enumerate(values):
        if (op == "<=" and value <= threshold) or (op == ">=" and value >= threshold):
            mask |= 1 << idx
    return mask


def _critical_thresholds(values: list[float]) -> list[float]:
    unique = sorted(set(values))
    if len(unique) == 1:
        return [unique[0]]
    return [(left + right) / 2.0 for left, right in zip(unique, unique[1:])]


def _gcd(values: list[int]) -> int:
    out = 0
    for value in values:
        out = gcd(out, abs(value))
    return out or 1


def _canonicalize_weights(term_weights: dict[str, int]) -> dict[str, int]:
    ordered = sorted(term_weights.items())
    scale = _gcd([weight for _name, weight in ordered])
    reduced = {name: weight // scale for name, weight in ordered}
    for _name, weight in ordered:
        if weight == 0:
            continue
        if weight < 0:
            reduced = {name: -value for name, value in reduced.items()}
        break
    return reduced


def _clause_name(term_weights: dict[str, int]) -> str:
    parts = []
    for name in sorted(term_weights):
        weight = term_weights[name]
        sign = "+" if weight > 0 else "-"
        parts.append(f"{sign}{abs(weight)}*{name}")
    return "corridor(" + " ".join(parts) + ")"


def _clause_values(rows: list[object], term_weights: dict[str, int]) -> list[float]:
    out: list[float] = []
    for row in rows:
        total = 0.0
        for name, weight in term_weights.items():
            total += float(getattr(row, name)) * weight
        out.append(total)
    return out


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def _interval_from_values(values: list[float], op: str, threshold: float) -> tuple[float, float, float, str]:
    unique = sorted(set(values))
    if op == "<=":
        included = [value for value in unique if value <= threshold]
        excluded = [value for value in unique if value > threshold]
        if not included or not excluded:
            return threshold, threshold, 0.0, f"[{threshold:.3f}, {threshold:.3f}]"
        lower = max(included)
        upper = min(excluded)
        return lower, upper, upper - lower, f"[{lower:.3f}, {upper:.3f})"
    included = [value for value in unique if value >= threshold]
    excluded = [value for value in unique if value < threshold]
    if not included or not excluded:
        return threshold, threshold, 0.0, f"[{threshold:.3f}, {threshold:.3f}]"
    lower = max(excluded)
    upper = min(included)
    return lower, upper, upper - lower, f"({lower:.3f}, {upper:.3f}]"


def _family_law(rows: list[object]) -> Predicate:
    values = [float(getattr(row, "delta_count_pocket_total")) for row in rows]
    threshold = -14.5
    return Predicate(
        name="delta_count_pocket_total",
        op="<=",
        threshold=threshold,
        mask=_mask_for(values, "<=", threshold),
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 pocket corridor clause scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()

    bucket_rows = [row for row in load_bucket_rows(bucket_log) if row.bucket_key == args.bucket_key]
    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }

    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    left_mask = 0
    right_mask = 0
    for idx, row in enumerate(rows):
        subtype = getattr(row, "subtype")
        if subtype == args.left_subtype:
            left_mask |= 1 << idx
        elif subtype == args.right_subtype:
            right_mask |= 1 << idx

    baseline = Predicate(
        name="delta_edge_identity_support_edge_density",
        op="<=",
        threshold=0.018,
        mask=_mask_for(
            [float(getattr(row, "delta_edge_identity_support_edge_density")) for row in rows],
            "<=",
            0.018,
        ),
    )
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline.mask)
    family_law = _family_law(rows)
    family_interval = _stable_interval(rows, family_law)
    family_rescue = family_law.mask & miss_mask

    available = set(rows[0].__dataclass_fields__)  # type: ignore[attr-defined]
    basis = [name for name in args.corridor_features if name in available]

    exact_rows = []
    seen_weight_classes: set[tuple[tuple[str, int], ...]] = set()
    for width in range(1, min(args.max_terms, len(basis)) + 1):
        for names in combinations(basis, width):
            for weights in product(args.coefficients, repeat=width):
                if all(weight < 0 for weight in weights):
                    continue
                term_weights = _canonicalize_weights({name: weight for name, weight in zip(names, weights)})
                class_key = tuple(sorted(term_weights.items()))
                if class_key in seen_weight_classes:
                    continue
                seen_weight_classes.add(class_key)

                values = _clause_values(rows, term_weights)
                clause_name = _clause_name(term_weights)
                for threshold in _critical_thresholds(values):
                    for op in ("<=", ">="):
                        mask = _mask_for(values, op, threshold)
                        if (mask & right_mask) != 0:
                            continue
                        if (mask & miss_mask) == 0:
                            continue
                        combined = baseline.mask | mask
                        tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
                        if fp != 0 or fn != 0:
                            continue
                        interval = _interval_from_values(values, op, threshold)
                        rescue = mask & miss_mask
                        exact_rows.append(
                            {
                                "term_count": width,
                                "clause_name": clause_name,
                                "weights": term_weights,
                                "op": op,
                                "threshold": threshold,
                                "interval": interval,
                                "rescued": _mask_names(rows, rescue),
                                "rescue_match_family": rescue == family_rescue,
                                "rescue_gap_count": (rescue ^ family_rescue).bit_count(),
                            }
                        )

    exact_rows.sort(
        key=lambda row: (
            not row["rescue_match_family"],
            row["rescue_gap_count"],
            row["term_count"],
            -row["interval"][2],
            row["clause_name"],
            row["op"],
            row["threshold"],
        )
    )

    print()
    print("Center-Spine Bucket 00 Pocket Corridor Clause Scan")
    print("==================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Fixed baseline clause")
    print("---------------------")
    print(f"{baseline.text}")
    print(f"baseline_missed_rows: {', '.join(_mask_names(rows, miss_mask))}")
    print()
    print("Reference wide rescue law")
    print("-------------------------")
    print(
        f"{family_law.text} -> width={family_interval[2]:.3f} interval={family_interval[3]} "
        + f"rescues={', '.join(_mask_names(rows, family_rescue))}"
    )
    print()
    print("Corridor feature basis (available)")
    print("----------------------------------")
    for name in basis:
        print(f"- {name}")
    missing = [name for name in args.corridor_features if name not in available]
    if missing:
        print("Missing requested features:")
        for name in missing:
            print(f"- {name}")
    print()
    print("Best exact corridor clauses")
    print("---------------------------")
    if not exact_rows:
        print("No exact closure clause found in bounded corridor basis.")
    else:
        for idx, row in enumerate(exact_rows[: args.top_k], start=1):
            print(
                f"{idx}. {row['clause_name']} {row['op']} {row['threshold']:.3f} "
                + f"terms={row['term_count']} width={row['interval'][2]:.3f} interval={row['interval'][3]} "
                + f"family_match={row['rescue_match_family']} gap={row['rescue_gap_count']} "
                + f"rescues={', '.join(row['rescued'])}"
            )
    print()
    print(
        "center-spine bucket00 pocket corridor clause scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
