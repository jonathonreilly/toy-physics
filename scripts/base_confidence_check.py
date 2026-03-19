#!/usr/bin/env python3
"""One-command confidence gate for the corrected toy-model benchmark base."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"
for path in (REPO_ROOT, SCRIPTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from benchmark_regression_audit import (  # noqa: E402
    check_live_mechanism_split_driver,
    check_mode_only_candidate_isolation,
    check_same_weight_default,
    check_sparse_bridge_addback_visibility,
    check_sparse_fallback_access_labels,
)
from check_feature_registry_alignment import main as feature_registry_alignment_main  # noqa: E402
from toy_event_physics import (  # noqa: E402
    extended_atomic_route_overlap_benchmark,
    mechanism_family_split_benchmark,
    route_map_summary,
)


def banner(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def timed_check(title: str, fn) -> object:
    banner(title)
    started = time.time()
    result = fn()
    print(f"[ok in {time.time() - started:.1f}s]")
    return result


def _route_row_map(rows):
    return {row.route_label: row for row in rows}


def check_feature_registry_alignment() -> None:
    feature_registry_alignment_main()


def check_route_maps() -> tuple[dict[str, object], dict[str, object]]:
    compact_rows, extended_rows = route_map_summary(mode_retained_weight=1.0)
    compact_map = _route_row_map(compact_rows)
    extended_map = _route_row_map(extended_rows)

    compact_expected = {
        "6+ threshold core": ("primary", "shared"),
        "7+ sufficient subroute": ("atomic-standalone", "shared"),
        "sparse near-miss residue": ("sparse-residue", "family-specific"),
    }
    extended_expected = {
        "hub": ("primary", "shared"),
        "low-degree backup envelope": ("atomic-standalone", "family-specific"),
        "pocket nested subroute": ("atomic-standalone", "family-specific"),
        "deep-pocket nested subroute": ("atomic-standalone", "family-specific"),
        "low-degree/pocket coexistence": ("coexistence-only", "family-specific"),
        "sparse-structure fallback": ("family-composite", "family-specific"),
    }

    assert set(compact_map) == set(compact_expected), (
        f"compact route-map labels drifted: expected={sorted(compact_expected)} "
        f"actual={sorted(compact_map)}"
    )
    assert set(extended_map) == set(extended_expected), (
        f"extended route-map labels drifted: expected={sorted(extended_expected)} "
        f"actual={sorted(extended_map)}"
    )

    for label, (role, scope) in compact_expected.items():
        row = compact_map[label]
        assert row.route_role == role, f"compact route {label} role drifted to {row.route_role}"
        assert row.family_scope == scope, (
            f"compact route {label} scope drifted to {row.family_scope}"
        )
    for label, (role, scope) in extended_expected.items():
        row = extended_map[label]
        assert row.route_role == role, (
            f"extended route {label} role drifted to {row.route_role}"
        )
        assert row.family_scope == scope, (
            f"extended route {label} scope drifted to {row.family_scope}"
        )

    threshold_core = compact_map["6+ threshold core"].canonical_feature_expression
    assert "motif_high_degree_neighbor_ge_6_fraction" in threshold_core
    assert "motif_high_degree_neighbor_share6_fraction" in threshold_core
    assert (
        "nested" in extended_map["pocket nested subroute"].route_label
        and "nested" in extended_map["deep-pocket nested subroute"].route_label
    ), "extended nested backup wording drifted from the overlap result"
    return compact_map, extended_map


def _overlap_row_map(rows):
    return {
        (row.ensemble_name, row.left_label, row.right_label): row
        for row in rows
    }


def check_extended_overlap_nesting() -> dict[tuple[str, str, str], object]:
    _scores, overlaps = extended_atomic_route_overlap_benchmark(
        mode_retained_weight=1.0,
        include_scores=False,
    )
    overlap_map = _overlap_row_map(overlaps)
    for ensemble_name in ("default", "broader"):
        deep_pocket = overlap_map[(ensemble_name, "deep-pocket", "pocket")]
        low_pocket = overlap_map[(ensemble_name, "low-degree", "pocket")]
        deep_low = overlap_map[(ensemble_name, "deep-pocket", "low-degree")]
        assert (
            deep_pocket.left_implies_right >= 0.999999
        ), f"deep-pocket is no longer fully nested inside pocket on {ensemble_name}"
        assert (
            low_pocket.right_implies_left >= 0.98
        ), f"pocket is no longer nested inside low-degree on {ensemble_name}"
        assert (
            deep_low.left_implies_right >= 0.98
        ), f"deep-pocket is no longer nested inside low-degree on {ensemble_name}"
    return overlap_map


def _mechanism_row(rows, benchmark_name: str, mechanism_name: str):
    return next(
        row
        for row in rows
        if row.benchmark_name == benchmark_name and row.mechanism_name == mechanism_name
    )


def check_mechanism_split() -> tuple[list[object], list[object]]:
    rows, aggregate = mechanism_family_split_benchmark(mode_retained_weight=1.0)
    full_rich = _mechanism_row(rows, "rich-ablation", "full-rich")
    ge7 = _mechanism_row(rows, "high-degree-threshold", "ge7")
    ge6 = _mechanism_row(rows, "high-degree-threshold", "ge6")
    share6 = _mechanism_row(rows, "threshold-exposure", "share6")

    assert full_rich.split_class == "shared-same", (
        f"full-rich split drifted to {full_rich.split_class}"
    )
    assert ge7.split_class == "shared-same", f"ge7 split drifted to {ge7.split_class}"
    assert ge6.split_class.startswith("shared"), (
        f"ge6 split no longer reads as shared: {ge6.split_class}"
    )
    assert share6.split_class.startswith("shared"), (
        f"share6 split no longer reads as shared: {share6.split_class}"
    )
    return rows, aggregate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="also rerun the helper-backed route-map and mechanism-split summaries",
    )
    args = parser.parse_args()

    print(
        "base confidence check started "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )
    timed_check("Benchmark Regression Audit", check_same_weight_default)
    timed_check("Mode-Only Candidate Isolation", check_mode_only_candidate_isolation)
    timed_check("Sparse Bridge Addback Visibility", check_sparse_bridge_addback_visibility)
    timed_check("Sparse Fallback Access Labels", check_sparse_fallback_access_labels)
    timed_check("Live Mechanism-Split Driver", check_live_mechanism_split_driver)
    timed_check("Feature Registry Alignment", check_feature_registry_alignment)
    banner("Summary")
    if args.full:
        overlap_map = timed_check("Extended Atomic Overlap", check_extended_overlap_nesting)
        compact_map, extended_map = timed_check("Route Map Summary", check_route_maps)
        split_rows, split_aggregate = timed_check(
            "Mechanism Split Benchmark",
            check_mechanism_split,
        )
        for ensemble_name in ("default", "broader"):
            deep_pocket = overlap_map[(ensemble_name, 'deep-pocket', 'pocket')]
            low_pocket = overlap_map[(ensemble_name, 'low-degree', 'pocket')]
            print(
                f"{ensemble_name}: deep-pocket=>pocket={deep_pocket.left_implies_right:.2f} "
                f"pocket=>low-degree={low_pocket.right_implies_left:.2f}"
            )
        print(f"compact routes={len(compact_map)} extended routes={len(extended_map)}")
        print(
            "split anchors: "
            + ", ".join(
                [
                    f"full-rich={next(row.split_class for row in split_rows if row.benchmark_name == 'rich-ablation' and row.mechanism_name == 'full-rich')}",
                    f"ge7={next(row.split_class for row in split_rows if row.benchmark_name == 'high-degree-threshold' and row.mechanism_name == 'ge7')}",
                    f"ge6={next(row.split_class for row in split_rows if row.benchmark_name == 'high-degree-threshold' and row.mechanism_name == 'ge6')}",
                    f"share6={next(row.split_class for row in split_rows if row.benchmark_name == 'threshold-exposure' and row.mechanism_name == 'share6')}",
                ]
            )
        )
        print(f"mechanism split rows={len(split_rows)} aggregate rows={len(split_aggregate)}")
    else:
        print("full overlap, route-map, and mechanism-split reruns skipped; use --full to include them")
    print()
    print(
        "base confidence check completed "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )


if __name__ == "__main__":
    main()
