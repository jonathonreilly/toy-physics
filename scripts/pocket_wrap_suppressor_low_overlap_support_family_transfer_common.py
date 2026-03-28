#!/usr/bin/env python3
"""Shared support-family transfer helpers for frozen low-overlap suppressor rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan import (  # noqa: E402
    _band_metrics,
    _high_bridge_cells,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features import (  # noqa: E402
    _own_metrics,
)


PRIMARY_SUPPORT_FAMILY_BUCKETS = ("rc0|ml0|c2", "rc0|ml1|c3")
RC0_ML0_C2_BUCKET = "rc0|ml0|c2"
RC0_ML0_C2_MAX_LEFT_LOW = 0.5
SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD = 19.0
EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD = 71.0
HIGH_SUPPORT_ML0_MIN_CELL_COUNT = 3.0
HIGH_SUPPORT_ML0_C4P_SPLIT_THRESHOLD = 3.5


@dataclass(frozen=True)
class SupportFamilyTransferRow:
    source_name: str
    subtype: str
    edge_identity_closed_pair_count: float
    support_role_bridge_count: float
    high_bridge_cell_count: float
    high_bridge_left_count: float
    high_bridge_right_count: float
    high_bridge_mid_count: float
    high_bridge_low_count: float
    high_bridge_center_count: float
    high_bridge_high_count: float
    high_bridge_left_low_count: float
    high_bridge_left_center_count: float
    high_bridge_right_low_count: float
    high_bridge_right_center_count: float
    high_bridge_mid_low_count: float
    high_bridge_mid_center_count: float
    high_bridge_mid_high_count: float
    family_bucket_key: str
    residual_bucket_key: str


def _mid_low_bin(value: float) -> str:
    if value <= 0.5:
        return "ml0"
    if value <= 1.5:
        return "ml1"
    return "ml2p"


def _cell_bin(value: float) -> str:
    if value <= 2.5:
        return "c2"
    if value <= 3.5:
        return "c3"
    return "c4p"


def _bucket_metric(row: object, name: str) -> float:
    return float(getattr(row, name))


def family_bucket_key(row: SupportFamilyTransferRow) -> str:
    return "|".join(
        [
            f"rc{int(row.high_bridge_right_center_count >= 0.5)}",
            _mid_low_bin(row.high_bridge_mid_low_count),
            _cell_bin(row.high_bridge_cell_count),
        ]
    )


def residual_bucket_key(row: SupportFamilyTransferRow) -> str:
    return "|".join(
        [
            f"rc{int(row.high_bridge_right_center_count >= 0.5)}",
            f"sbh{int(row.support_role_bridge_count >= SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD)}",
            f"cp_hi{int(row.edge_identity_closed_pair_count >= EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD)}",
            _mid_low_bin(row.high_bridge_mid_low_count),
            _cell_bin(row.high_bridge_cell_count),
        ]
    )


def family_bucket_key_like(row: object) -> str:
    return "|".join(
        [
            f"rc{int(_bucket_metric(row, 'high_bridge_right_center_count') >= 0.5)}",
            _mid_low_bin(_bucket_metric(row, "high_bridge_mid_low_count")),
            _cell_bin(_bucket_metric(row, "high_bridge_cell_count")),
        ]
    )


def residual_bucket_key_like(row: object) -> str:
    return "|".join(
        [
            f"rc{int(_bucket_metric(row, 'high_bridge_right_center_count') >= 0.5)}",
            f"sbh{int(_bucket_metric(row, 'support_role_bridge_count') >= SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD)}",
            f"cp_hi{int(_bucket_metric(row, 'edge_identity_closed_pair_count') >= EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD)}",
            _mid_low_bin(_bucket_metric(row, "high_bridge_mid_low_count")),
            _cell_bin(_bucket_metric(row, "high_bridge_cell_count")),
        ]
    )


def is_rc0_ml0_c2_core_like(row: object) -> bool:
    return (
        getattr(row, "family_bucket_key") == RC0_ML0_C2_BUCKET
        and float(getattr(row, "high_bridge_left_low_count")) < RC0_ML0_C2_MAX_LEFT_LOW
    )


def is_peer_band_like(row: object) -> bool:
    return float(getattr(row, "high_bridge_left_low_count")) >= RC0_ML0_C2_MAX_LEFT_LOW


def build_rows(frontier_log: Path) -> list[SupportFamilyTransferRow]:
    rows = reconstruct_low_overlap_rows(frontier_log)
    out: list[SupportFamilyTransferRow] = []
    for row in rows:
        nodes = set(row.nodes)
        core_metrics = _own_metrics(nodes)
        band_metrics = _band_metrics(_high_bridge_cells(nodes))
        out_row = SupportFamilyTransferRow(
            source_name=row.source_name,
            subtype=row.subtype,
            edge_identity_closed_pair_count=core_metrics["edge_identity_closed_pair_count"],
            support_role_bridge_count=core_metrics["support_role_bridge_count"],
            high_bridge_cell_count=band_metrics["high_bridge_cell_count"],
            high_bridge_left_count=band_metrics["high_bridge_left_count"],
            high_bridge_right_count=band_metrics["high_bridge_right_count"],
            high_bridge_mid_count=band_metrics["high_bridge_mid_count"],
            high_bridge_low_count=band_metrics["high_bridge_low_count"],
            high_bridge_center_count=band_metrics["high_bridge_center_count"],
            high_bridge_high_count=band_metrics["high_bridge_high_count"],
            high_bridge_left_low_count=band_metrics["high_bridge_left_low_count"],
            high_bridge_left_center_count=band_metrics["high_bridge_left_center_count"],
            high_bridge_right_low_count=band_metrics["high_bridge_right_low_count"],
            high_bridge_right_center_count=band_metrics["high_bridge_right_center_count"],
            high_bridge_mid_low_count=band_metrics["high_bridge_mid_low_count"],
            high_bridge_mid_center_count=band_metrics["high_bridge_mid_center_count"],
            high_bridge_mid_high_count=band_metrics["high_bridge_mid_high_count"],
            family_bucket_key="",
            residual_bucket_key="",
        )
        out.append(
            SupportFamilyTransferRow(
                **{
                    **out_row.__dict__,
                    "family_bucket_key": family_bucket_key(out_row),
                    "residual_bucket_key": residual_bucket_key(out_row),
                }
            )
        )
    out.sort(key=lambda item: item.source_name)
    return out
