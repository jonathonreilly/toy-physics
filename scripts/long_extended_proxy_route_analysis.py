#!/usr/bin/env python3
"""Analyze whether extended-fast survivors reduce to one cavity route or several."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    classify_extended_proxy_family,
    extended_proxy_route_sets,
    neighborhood_basis_residual_benchmark,
    parity_threshold_from_residual_rows,
    render_extended_proxy_route_aggregate_table,
    render_extended_proxy_route_table,
    rich_neighborhood_basis_feature_names,
    ExtendedProxyRouteAggregateRow,
    ExtendedProxyRouteRow,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"extended proxy route analysis started {started}", flush=True)
    total_start = time.time()
    all_rich_features = rich_neighborhood_basis_feature_names()
    route_rows: list[ExtendedProxyRouteRow] = []
    aggregate_counts: dict[str, int] = {}
    route_sets = extended_proxy_route_sets()
    for index, (route_name, removed_features) in enumerate(route_sets, start=1):
        route_start = time.time()
        print(f"[{index}/{len(route_sets)}] starting {route_name}", flush=True)
        feature_names = tuple(
            feature for feature in all_rich_features if feature not in set(removed_features)
        )
        residual_rows = neighborhood_basis_residual_benchmark(
            retained_weight=1.0,
            mode_retained_weight=1.0,
            basis_feature_names=feature_names,
        )
        compact_rows = [row for row in residual_rows if row.rule_family == "compact"]
        extended_rows = [row for row in residual_rows if row.rule_family == "extended"]
        compact_parity, compact_best_prethreshold = parity_threshold_from_residual_rows(
            compact_rows
        )
        extended_parity, extended_best_prethreshold = parity_threshold_from_residual_rows(
            extended_rows
        )
        proxy_family, proxy_signature = classify_extended_proxy_family(
            extended_parity.basis_feature_subset if extended_parity is not None else "-"
        )
        aggregate_counts[proxy_family] = aggregate_counts.get(proxy_family, 0) + 1
        route_rows.append(
            ExtendedProxyRouteRow(
                route_name=route_name,
                feature_count=len(feature_names),
                removed_features=", ".join(removed_features) if removed_features else "-",
                compact_parity_size=compact_parity.basis_size if compact_parity is not None else None,
                compact_parity_feature_subset=compact_parity.basis_feature_subset if compact_parity is not None else "-",
                compact_best_prethreshold_gap=compact_best_prethreshold.basis_minus_pocket_mean,
                compact_best_prethreshold_worst_gap=compact_best_prethreshold.basis_minus_pocket_worst,
                extended_parity_size=extended_parity.basis_size if extended_parity is not None else None,
                extended_parity_feature_subset=extended_parity.basis_feature_subset if extended_parity is not None else "-",
                extended_proxy_family=proxy_family,
                extended_proxy_signature=proxy_signature,
                extended_best_prethreshold_gap=extended_best_prethreshold.basis_minus_pocket_mean,
                extended_best_prethreshold_worst_gap=extended_best_prethreshold.basis_minus_pocket_worst,
            )
        )
        print(
            f"[{index}/{len(route_sets)}] finished {route_name} "
            f"compact={compact_parity.basis_size if compact_parity is not None else '-'}:{compact_parity.basis_feature_subset if compact_parity is not None else '-'} "
            f"extended={extended_parity.basis_size if extended_parity is not None else '-'}:{extended_parity.basis_feature_subset if extended_parity is not None else '-'} "
            f"proxy={proxy_family} elapsed={time.time() - route_start:.1f}s",
            flush=True,
        )
    route_rows.sort(key=lambda row: row.route_name)
    aggregate_rows = [
        ExtendedProxyRouteAggregateRow(proxy_family=proxy_family, cases=cases)
        for proxy_family, cases in sorted(aggregate_counts.items())
    ]
    print()
    print("Extended Proxy Route Aggregate")
    print("==============================")
    print(render_extended_proxy_route_aggregate_table(aggregate_rows))
    print()
    print("Extended Proxy Route Detail")
    print("===========================")
    print(render_extended_proxy_route_table(route_rows))
    print()
    print(
        "extended proxy route analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
