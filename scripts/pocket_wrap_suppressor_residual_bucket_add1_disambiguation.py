#!/usr/bin/env python3
"""Probe one bounded add1 disambiguation clause for the 5504 residual bucket."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time


ROW_RE = re.compile(
    r"^\s*(?P<source>\S+)\s+\|\s+"
    r"(?P<subtype>add1-sensitive|add4-sensitive)\s+\|\s+"
    r"(?P<addtag>[^|]+)\|\s+"
    r"(?P<lowcore>-?\d+\.\d{3})/(?P<lowshell>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<pocket>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<rough>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<mean>[+-]?\d+\.\d{2})\s+\|\s+"
    r"(?P<absmean>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<ctv>-?\d+\.\d{2})\s+\|\s+"
    r"(?P<span>\d+)\s+\|\s+"
    r"(?P<pocketgap>[+-]?\d+\.\d{3})\s+\|\s+"
    r"(?P<lowgap>[+-]?\d+\.\d{3})\s*$"
)


@dataclass(frozen=True)
class ResidualRow:
    source: str
    subtype: str
    mean_center: float
    center_total_variation: float
    pocket_gap: float
    low_gap: float

    @property
    def abs_pocket_gap(self) -> float:
        return abs(self.pocket_gap)

    @property
    def abs_low_gap(self) -> float:
        return abs(self.low_gap)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual-log", required=True)
    return parser.parse_args()


def parse_rows(path: Path) -> list[ResidualRow]:
    rows: list[ResidualRow] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        rows.append(
            ResidualRow(
                source=match.group("source"),
                subtype=match.group("subtype"),
                mean_center=float(match.group("mean")),
                center_total_variation=float(match.group("ctv")),
                pocket_gap=float(match.group("pocketgap")),
                low_gap=float(match.group("lowgap")),
            )
        )
    return rows


def add1_base(row: ResidualRow) -> bool:
    return row.abs_pocket_gap >= 0.058 and row.mean_center >= -0.035


def add1_disambiguator(row: ResidualRow) -> bool:
    return (
        row.center_total_variation >= 1.5
        and row.abs_low_gap >= 0.145
        and row.abs_low_gap <= 0.23
        and row.mean_center <= -0.14
    )


def evaluate(rows: list[ResidualRow]) -> tuple[int, int, int, list[ResidualRow]]:
    predicted = [row for row in rows if add1_base(row) or add1_disambiguator(row)]
    tp = sum(1 for row in predicted if row.subtype == "add1-sensitive")
    fp = sum(1 for row in predicted if row.subtype != "add1-sensitive")
    fn = sum(1 for row in rows if row.subtype == "add1-sensitive" and row not in predicted)
    return tp, fp, fn, predicted


def main() -> None:
    args = parse_args()
    residual_log = Path(args.residual_log).resolve()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"residual add1-disambiguation probe started {started}", flush=True)
    total_start = time.time()

    rows = parse_rows(residual_log)
    if not rows:
        raise SystemExit(f"no residual rows parsed from {residual_log}")

    tp, fp, fn, predicted = evaluate(rows)
    total = len(rows)
    add1_total = sum(1 for row in rows if row.subtype == "add1-sensitive")

    print()
    print("Residual Add1 Disambiguation")
    print("============================")
    print(f"log={residual_log}")
    print(f"rows={total} add1_rows={add1_total}")
    print("base_rule: abs_pocket_gap >= 0.058 and mean_center >= -0.035")
    print(
        "extra_clause: center_total_variation >= 1.5 and abs_low_gap in [0.145, 0.23] and mean_center <= -0.14"
    )
    print("combined_rule: base_rule OR extra_clause")
    print(f"tp/fp/fn={tp}/{fp}/{fn}")
    print()
    print("Predicted add1-sensitive rows")
    print("=============================")
    for row in predicted:
        print(
            f"{row.source} | {row.subtype} | mean={row.mean_center:+.2f} | "
            f"abs_pocket_gap={row.abs_pocket_gap:.3f} | abs_low_gap={row.abs_low_gap:.3f} | "
            f"ctv={row.center_total_variation:.2f}"
        )
    print()
    misses = [row for row in rows if row.subtype == "add1-sensitive" and row not in predicted]
    print(f"remaining_add1_misses={len(misses)}")
    for row in misses:
        print(
            f"miss {row.source} | mean={row.mean_center:+.2f} | "
            f"abs_pocket_gap={row.abs_pocket_gap:.3f} | abs_low_gap={row.abs_low_gap:.3f}"
        )

    finished = datetime.now().isoformat(timespec="seconds")
    elapsed = time.time() - total_start
    print()
    print(f"residual add1-disambiguation probe completed {finished} total_elapsed={elapsed:.1f}s")


if __name__ == "__main__":
    main()
