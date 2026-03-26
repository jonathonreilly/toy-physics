#!/usr/bin/env python3
"""Probe one bounded disambiguation clause for the 5504 residual bucket."""

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
    low_core: float
    low_shell: float
    mean_center: float
    abs_mean_center: float
    low_gap: float

    @property
    def low_sum(self) -> float:
        return self.low_core + self.low_shell


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
                low_core=float(match.group("lowcore")),
                low_shell=float(match.group("lowshell")),
                mean_center=float(match.group("mean")),
                abs_mean_center=float(match.group("absmean")),
                low_gap=float(match.group("lowgap")),
            )
        )
    return rows


def add4_base(row: ResidualRow) -> bool:
    abs_low_gap = abs(row.low_gap)
    return abs_low_gap <= 0.288 and abs_low_gap >= 0.1605 and row.abs_mean_center <= 0.25


def add4_disambiguator(row: ResidualRow) -> bool:
    return row.low_sum <= 1e-6 and row.mean_center <= 0.0


def evaluate(rows: list[ResidualRow]) -> tuple[int, int, int, list[ResidualRow]]:
    predicted = [row for row in rows if add4_base(row) or add4_disambiguator(row)]
    tp = sum(1 for row in predicted if row.subtype == "add4-sensitive")
    fp = sum(1 for row in predicted if row.subtype != "add4-sensitive")
    fn = sum(1 for row in rows if row.subtype == "add4-sensitive" and row not in predicted)
    return tp, fp, fn, predicted


def main() -> None:
    args = parse_args()
    residual_log = Path(args.residual_log).resolve()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"residual fn-disambiguation probe started {started}", flush=True)
    total_start = time.time()

    rows = parse_rows(residual_log)
    if not rows:
        raise SystemExit(f"no residual rows parsed from {residual_log}")

    tp, fp, fn, predicted = evaluate(rows)
    total = len(rows)
    add4_total = sum(1 for row in rows if row.subtype == "add4-sensitive")

    print()
    print("Residual FN Disambiguation")
    print("==========================")
    print(f"log={residual_log}")
    print(f"rows={total} add4_rows={add4_total}")
    print("base_rule: abs_low_gap <= 0.288 and abs_low_gap >= 0.1605 and abs_mean_center <= 0.25")
    print("extra_clause: low_core + low_shell <= 1e-6 and mean_center <= 0.0")
    print(f"combined_rule: base_rule OR extra_clause")
    print(f"tp/fp/fn={tp}/{fp}/{fn}")
    print()
    print("Predicted add4-sensitive rows")
    print("=============================")
    for row in predicted:
        print(
            f"{row.source} | {row.subtype} | low_sum={row.low_sum:.3f} | "
            f"mean={row.mean_center:+.2f} | abs_low_gap={abs(row.low_gap):.3f} | abs_mean={row.abs_mean_center:.3f}"
        )
    print()
    misses = [row for row in rows if row.subtype == "add4-sensitive" and row not in predicted]
    print(f"remaining_add4_misses={len(misses)}")
    for row in misses:
        print(f"miss {row.source} | low_sum={row.low_sum:.3f} | mean={row.mean_center:+.2f}")
    finished = datetime.now().isoformat(timespec="seconds")
    elapsed = time.time() - total_start
    print()
    print(f"residual fn-disambiguation probe completed {finished} total_elapsed={elapsed:.1f}s")


if __name__ == "__main__":
    main()
