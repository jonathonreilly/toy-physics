#!/usr/bin/env python3
"""Compare balance-led vs balanced-load-led visibility families on generated DAGs.

This stays strictly local to the already-tested generated-DAG bridge:
it does not widen the scenario ladder. Instead it asks whether the two
currently winning local observables collapse to one shared scalar, or
whether a simple load floor creates a genuine two-branch regime.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_visibility_order_parameter_compare import (
    CandidateScore,
    Scenario,
    SeedRow,
    correlation,
    run_rows,
)


DEFAULT_SCENARIO = Scenario(label="default")
DENSER_SCENARIO = Scenario(label="denser-radius", connect_radius=2.7)
FAMILY_CANDIDATES = [
    "center_path_balance",
    "center_balanced_log_paths",
    "center_balance_share",
    "center_balance_share_retimed",
    "center_packet_completion",
]


@dataclass(frozen=True)
class SplitResult:
    threshold: float
    low_count: int
    high_count: int
    low_score: CandidateScore
    high_score: CandidateScore
    weighted_summary: float


def score_rows(rows: list[SeedRow], names: list[str]) -> list[CandidateScore]:
    target_v0 = [row.v_center for row in rows]
    target_mean_v = [row.mean_v for row in rows]
    scores = []
    for name in names:
        values = [float(getattr(row, name)) for row in rows]
        scores.append(
            CandidateScore(
                name=name,
                corr_v0=correlation(values, target_v0),
                corr_mean_v=correlation(values, target_mean_v),
            )
        )
    return sorted(scores, key=lambda score: score.summary_score, reverse=True)


def scenario_counts(rows: list[SeedRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.scenario] = counts.get(row.scenario, 0) + 1
    return counts


def split_search(rows: list[SeedRow]) -> SplitResult | None:
    values = sorted({row.center_balanced_log_paths for row in rows})
    best: SplitResult | None = None
    for left, right in zip(values, values[1:]):
        threshold = (left + right) / 2.0
        low_rows = [row for row in rows if row.center_balanced_log_paths <= threshold]
        high_rows = [row for row in rows if row.center_balanced_log_paths > threshold]
        if len(low_rows) < 12 or len(high_rows) < 12:
            continue
        low_score = score_rows(low_rows, ["center_path_balance"])[0]
        high_score = score_rows(high_rows, ["center_balanced_log_paths"])[0]
        weighted_summary = (
            len(low_rows) * low_score.summary_score
            + len(high_rows) * high_score.summary_score
        ) / len(rows)
        candidate = SplitResult(
            threshold=threshold,
            low_count=len(low_rows),
            high_count=len(high_rows),
            low_score=low_score,
            high_score=high_score,
            weighted_summary=weighted_summary,
        )
        if best is None or candidate.weighted_summary > best.weighted_summary:
            best = candidate
    return best


def row_mean(rows: list[SeedRow], field: str) -> float:
    return statistics.fmean(float(getattr(row, field)) for row in rows)


def main() -> None:
    default_rows = run_rows(DEFAULT_SCENARIO, range(0, 64), workers=max(1, os.cpu_count() or 1), phase_steps=16)
    denser_rows = run_rows(DENSER_SCENARIO, range(64, 96), workers=max(1, os.cpu_count() or 1), phase_steps=16)
    combined_rows = default_rows + denser_rows
    combined_rows.sort(key=lambda row: (row.scenario, row.seed))

    default_scores = score_rows(default_rows, FAMILY_CANDIDATES)
    denser_scores = score_rows(denser_rows, FAMILY_CANDIDATES)
    combined_scores = score_rows(combined_rows, FAMILY_CANDIDATES)
    best_split = split_search(combined_rows)

    print("=" * 72)
    print("GENERATIVE CAUSAL DAG VISIBILITY FAMILY REGIME COMPARE")
    print("=" * 72)
    print("Default slice: seeds 0..63, radius=2.5")
    print("Denser holdout: seeds 64..95, radius=2.7")
    print()

    print("Per-scenario family winners:")
    print(
        f"  default: {default_scores[0].name} "
        f"(corr_v0={default_scores[0].corr_v0:+.4f}, "
        f"corr_mean_V={default_scores[0].corr_mean_v:+.4f}, "
        f"summary={default_scores[0].summary_score:.4f})"
    )
    print(
        f"  denser : {denser_scores[0].name} "
        f"(corr_v0={denser_scores[0].corr_v0:+.4f}, "
        f"corr_mean_V={denser_scores[0].corr_mean_v:+.4f}, "
        f"summary={denser_scores[0].summary_score:.4f})"
    )
    print()

    print("Combined single-scalar ranking:")
    for rank, score in enumerate(combined_scores, start=1):
        print(
            f"  {rank:2d}. {score.name:<28s} "
            f"corr_v0={score.corr_v0:+.4f} "
            f"corr_mean_V={score.corr_mean_v:+.4f} "
            f"summary={score.summary_score:.4f}"
        )
    print()

    if best_split is None:
        print("No valid split found.")
        return

    low_rows = [
        row for row in combined_rows if row.center_balanced_log_paths <= best_split.threshold
    ]
    high_rows = [
        row for row in combined_rows if row.center_balanced_log_paths > best_split.threshold
    ]
    low_counts = scenario_counts(low_rows)
    high_counts = scenario_counts(high_rows)

    print("Best two-branch split:")
    print(
        f"  split on center_balanced_log_paths <= {best_split.threshold:.3f} "
        f"(low={best_split.low_count}, high={best_split.high_count})"
    )
    print(
        f"  low branch keeps center_path_balance "
        f"(corr_v0={best_split.low_score.corr_v0:+.4f}, "
        f"corr_mean_V={best_split.low_score.corr_mean_v:+.4f}, "
        f"summary={best_split.low_score.summary_score:.4f})"
    )
    print(
        f"  high branch keeps center_balanced_log_paths "
        f"(corr_v0={best_split.high_score.corr_v0:+.4f}, "
        f"corr_mean_V={best_split.high_score.corr_mean_v:+.4f}, "
        f"summary={best_split.high_score.summary_score:.4f})"
    )
    print(f"  weighted summary={best_split.weighted_summary:.4f}")
    print(
        f"  low branch scenarios={low_counts}, "
        f"mean_V0={row_mean(low_rows, 'v_center'):.4f}, "
        f"mean_balanced_log={row_mean(low_rows, 'center_balanced_log_paths'):.3f}"
    )
    print(
        f"  high branch scenarios={high_counts}, "
        f"mean_V0={row_mean(high_rows, 'v_center'):.4f}, "
        f"mean_balanced_log={row_mean(high_rows, 'center_balanced_log_paths'):.3f}"
    )
    print()

    best_single = combined_scores[0]
    if best_split.weighted_summary > best_single.summary_score:
        print("Interpretation:")
        print(
            "  The current generated-DAG bridge is better read as a two-branch regime "
            "than as one universal scalar: below the balanced-load floor, visibility is "
            "more balance-led; above it, balanced center slit-load carries the signal."
        )
    else:
        print("Interpretation:")
        print(
            "  The current family still compresses best to a single shared scalar; the "
            "two-branch split does not beat the best combined observable."
        )


if __name__ == "__main__":
    main()
