#!/usr/bin/env python3
"""Show the refined extended-route family labels on representative corrected routes."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    classify_extended_proxy_family,
    extended_route_components,
)


EXAMPLES = (
    ("hub-primary", "motif_high_degree_neighbor_fraction"),
    ("deep-pocket", "motif_deep_pocket_adjacent_fraction"),
    ("pocket-mix", "motif_pocket_adjacent_fraction, degree_8_fraction, motif_low_degree_neighbor_fraction"),
    ("low-degree", "motif_low_degree_neighbor_fraction"),
    ("sparse-base", "degree_8_fraction, motif_mean_neighbor_degree, motif_two_hop_open_fraction"),
    ("sparse-pair-removed", "motif_two_hop_open_fraction, motif_two_hop_occupied_fraction, degree_1_fraction"),
    ("sparse-weak-endpoint", "motif_neighbor_degree_variation"),
)


def main() -> None:
    print("Extended Route Classification Examples")
    print("======================================")
    print("example            | family            | components                | signature")
    print("-------------------+-------------------+---------------------------+----------------------------------------------")
    for name, feature_subset in EXAMPLES:
        family, signature = classify_extended_proxy_family(feature_subset)
        components = ", ".join(extended_route_components(feature_subset))
        print(f"{name:<19} | {family:<17} | {components:<25.25} | {signature}")


if __name__ == "__main__":
    main()
