#!/usr/bin/env python3
"""Measure how distinct the extended atomic backup routes really are."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    build_generated_geometry_prediction_context,
    decision_feature_value,
    decision_tree_accuracy,
    fit_ordinal_score_model,
    learn_tiny_decision_tree,
    ordinal_score_accuracy,
)


FEATURES = (
    ("deep-pocket", "motif_deep_pocket_adjacent_fraction"),
    ("pocket", "motif_pocket_adjacent_fraction"),
    ("low-degree", "motif_low_degree_neighbor_fraction"),
)


@dataclass(frozen=True)
class FeatureScoreRow:
    ensemble: str
    route_name: str
    support_fraction: float
    tree_generated_mean: float
    tree_generated_worst: float
    ordinal_generated_mean: float
    ordinal_generated_worst: float


@dataclass(frozen=True)
class FeatureOverlapRow:
    ensemble: str
    left_name: str
    right_name: str
    left_support_fraction: float
    right_support_fraction: float
    left_implies_right: float
    right_implies_left: float
    jaccard: float


def _generated_rows(ensemble: str):
    if ensemble == "default":
        context = build_generated_geometry_prediction_context(
            retained_weight=1.0,
            mode_retained_weight=1.0,
            geometry_variant_limit=5,
            procedural_variant_limit=3,
            procedural_rediscovery_limit=1,
            procedural_styles=("walk", "mode-mix", "local-morph"),
        )
    elif ensemble == "broader":
        context = build_generated_geometry_prediction_context(
            retained_weight=1.0,
            mode_retained_weight=1.0,
            geometry_variant_limit=7,
            procedural_variant_limit=4,
            procedural_rediscovery_limit=1,
            procedural_styles=("walk", "mode-mix", "local-morph"),
        )
    else:
        raise ValueError(f"unknown ensemble {ensemble}")
    mode_core_rows, mode_prediction_rows, _roughness_rows, procedural_rows, geometry_rows = context
    mode_extended = [row for row in mode_prediction_rows if row.rule_family == "extended"]
    generated_extended = [
        row
        for row in [*geometry_rows, *procedural_rows]
        if row.rule_family == "extended"
    ]
    geometry_extended = [row for row in geometry_rows if row.rule_family == "extended"]
    procedural_extended = [row for row in procedural_rows if row.rule_family == "extended"]
    return mode_core_rows, mode_extended, geometry_extended, procedural_extended, generated_extended


def score_rows() -> list[FeatureScoreRow]:
    rows: list[FeatureScoreRow] = []
    for ensemble in ("default", "broader"):
        _mode_core_rows, mode_extended, geometry_extended, procedural_extended, generated_extended = _generated_rows(
            ensemble
        )
        for route_name, feature_name in FEATURES:
            support_fraction = sum(
                decision_feature_value(row, feature_name) > 0.0
                for row in generated_extended
            ) / len(generated_extended)

            tree = learn_tiny_decision_tree(mode_extended, (feature_name,), 2)
            tree_geometry = decision_tree_accuracy(tree, geometry_extended)
            tree_procedural = decision_tree_accuracy(tree, procedural_extended)

            ordinal = fit_ordinal_score_model(mode_extended, (feature_name,))
            ordinal_geometry = ordinal_score_accuracy(ordinal, geometry_extended)
            ordinal_procedural = ordinal_score_accuracy(ordinal, procedural_extended)

            rows.append(
                FeatureScoreRow(
                    ensemble=ensemble,
                    route_name=route_name,
                    support_fraction=support_fraction,
                    tree_generated_mean=(tree_geometry + tree_procedural) / 2.0,
                    tree_generated_worst=min(tree_geometry, tree_procedural),
                    ordinal_generated_mean=(ordinal_geometry + ordinal_procedural) / 2.0,
                    ordinal_generated_worst=min(ordinal_geometry, ordinal_procedural),
                )
            )
    return rows


def overlap_rows() -> list[FeatureOverlapRow]:
    rows: list[FeatureOverlapRow] = []
    for ensemble in ("default", "broader"):
        _mode_core_rows, _mode_extended, _geometry_extended, _procedural_extended, generated_extended = _generated_rows(
            ensemble
        )
        support_sets = {}
        for route_name, feature_name in FEATURES:
            support_sets[route_name] = {
                index
                for index, row in enumerate(generated_extended)
                if decision_feature_value(row, feature_name) > 0.0
            }
        for left_name, _left_feature in FEATURES:
            for right_name, _right_feature in FEATURES:
                if left_name >= right_name:
                    continue
                left = support_sets[left_name]
                right = support_sets[right_name]
                intersection = left & right
                union = left | right
                rows.append(
                    FeatureOverlapRow(
                        ensemble=ensemble,
                        left_name=left_name,
                        right_name=right_name,
                        left_support_fraction=len(left) / len(generated_extended),
                        right_support_fraction=len(right) / len(generated_extended),
                        left_implies_right=(len(intersection) / len(left)) if left else 1.0,
                        right_implies_left=(len(intersection) / len(right)) if right else 1.0,
                        jaccard=(len(intersection) / len(union)) if union else 1.0,
                    )
                )
    return rows


def render_score_table(rows: list[FeatureScoreRow]) -> str:
    lines = [
        "ensemble | route       | support | tree mean/w | ordinal mean/w",
        "---------+-------------+---------+-------------+----------------",
    ]
    for row in rows:
        lines.append(
            f"{row.ensemble:<8} | "
            f"{row.route_name:<11} | "
            f"{row.support_fraction:>7.2f} | "
            f"{row.tree_generated_mean:>4.2f}/{row.tree_generated_worst:<4.2f} | "
            f"{row.ordinal_generated_mean:>6.2f}/{row.ordinal_generated_worst:<6.2f}"
        )
    return "\n".join(lines)


def render_overlap_table(rows: list[FeatureOverlapRow]) -> str:
    lines = [
        "ensemble | pair                | left=>right | right=>left | jaccard",
        "---------+---------------------+-------------+-------------+--------",
    ]
    for row in rows:
        lines.append(
            f"{row.ensemble:<8} | "
            f"{row.left_name + ' vs ' + row.right_name:<19} | "
            f"{row.left_implies_right:>11.2f} | "
            f"{row.right_implies_left:>11.2f} | "
            f"{row.jaccard:>6.2f}"
        )
    return "\n".join(lines)


def main() -> None:
    print(
        "extended atomic route overlap analysis started "
        + datetime.now().isoformat(timespec="seconds")
    )
    scores = score_rows()
    overlaps = overlap_rows()
    print()
    print("Extended Atomic Route Scores")
    print("============================")
    print(render_score_table(scores))
    print()
    print("Extended Atomic Route Overlaps")
    print("==============================")
    print(render_overlap_table(overlaps))
    print()
    print(
        "extended atomic route overlap analysis completed "
        + datetime.now().isoformat(timespec="seconds")
    )


if __name__ == "__main__":
    main()
