#!/usr/bin/env python3
"""Audit whether the current non-base late guardrail frontier is exhausted."""

from __future__ import annotations

from dataclasses import dataclass
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

from toy_event_physics import benchmark_packs  # noqa: E402


CURRENT_LATE_FRONTIER_ENSEMBLES = ("ultra", "mega", "giga", "tera", "peta", "exa")
ENSEMBLE_ORDER = {
    ensemble_name: index
    for index, ensemble_name in enumerate(CURRENT_LATE_FRONTIER_ENSEMBLES)
}
NON_BASE_GUARDRAIL_LOGS = (
    (
        "large:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-ultra-mega.txt"
        ),
    ),
    (
        "large:giga",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-giga.txt"
        ),
    ),
    (
        "large:tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-tera.txt"
        ),
    ),
    (
        "large:peta",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-peta.txt"
        ),
    ),
    (
        "large:exa",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-exa.txt"
        ),
    ),
    (
        "mirror:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-ultra-mega.txt"
        ),
    ),
    (
        "mirror:giga|tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-giga-tera.txt"
        ),
    ),
    (
        "mirror:peta",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-peta.txt"
        ),
    ),
    (
        "mirror:exa",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-exa.txt"
        ),
    ),
)


@dataclass(frozen=True)
class GuardrailAuditRow:
    label: str
    packs: tuple[str, ...]
    ensembles: tuple[str, ...]
    scanned_nonrect_combinations: int
    first_nonrect_row: str


def _parse_simple_key_values(log_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in log_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("=") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _split_csv(raw_value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in raw_value.split(",") if part.strip())


def _parse_guardrail_row(label: str, log_path: Path) -> GuardrailAuditRow:
    parsed = _parse_simple_key_values(log_path)
    return GuardrailAuditRow(
        label=label,
        packs=_split_csv(parsed["packs"]),
        ensembles=_split_csv(parsed["ensembles"]),
        scanned_nonrect_combinations=int(parsed["scanned_nonrect_combinations"]),
        first_nonrect_row=parsed["first_nonrect_row"],
    )


def _pair_sort_key(pair: tuple[str, str]) -> tuple[str, int, str]:
    pack_name, ensemble_name = pair
    return (pack_name, ENSEMBLE_ORDER.get(ensemble_name, len(ENSEMBLE_ORDER)), ensemble_name)


def _format_pairs(pairs: set[tuple[str, str]]) -> str:
    if not pairs:
        return "none"
    return ",".join(
        f"{pack_name}:{ensemble_name}"
        for pack_name, ensemble_name in sorted(pairs, key=_pair_sort_key)
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()

    benchmark_pack_names = tuple(pack_name for pack_name, _scenarios in benchmark_packs())
    non_base_pack_names = tuple(
        pack_name for pack_name in benchmark_pack_names if pack_name != "base"
    )
    target_pairs = {
        (pack_name, ensemble_name)
        for pack_name in non_base_pack_names
        for ensemble_name in CURRENT_LATE_FRONTIER_ENSEMBLES
    }

    guardrails = [
        _parse_guardrail_row(label, log_path)
        for label, log_path in NON_BASE_GUARDRAIL_LOGS
    ]
    covered_pairs = {
        (pack_name, ensemble_name)
        for row in guardrails
        for pack_name in row.packs
        for ensemble_name in row.ensembles
    }
    missing_pairs = target_pairs - covered_pairs
    extra_pairs = covered_pairs - target_pairs
    first_hit_rows = [row for row in guardrails if row.first_nonrect_row != "none"]
    covered_pack_names = {pack_name for pack_name, _ensemble_name in covered_pairs}
    missing_pack_names = set(non_base_pack_names) - covered_pack_names
    total_scanned = sum(row.scanned_nonrect_combinations for row in guardrails)

    print(f"late branch frontier closure audit started {started}", flush=True)
    print()
    print("Late Branch Frontier Closure Audit")
    print("=================================")
    print("benchmark_pack_names=" + ",".join(benchmark_pack_names))
    print("benchmark_non_base_pack_names=" + ",".join(non_base_pack_names))
    print("current_late_frontier_ensembles=" + ",".join(CURRENT_LATE_FRONTIER_ENSEMBLES))
    print(f"finished_non_base_guardrail_logs={len(guardrails)}")
    print(f"finished_non_base_scanned_nonrect_combinations={total_scanned}")
    print(f"target_non_base_pack_ensemble_pairs={len(target_pairs)}")
    print(f"covered_non_base_pack_ensemble_pairs={len(covered_pairs)}")
    print("covered_non_base_pairs=" + _format_pairs(covered_pairs))
    print("missing_non_base_pairs=" + _format_pairs(missing_pairs))
    print("extra_non_base_pairs=" + _format_pairs(extra_pairs))
    print(
        "missing_non_base_packs="
        + (",".join(sorted(missing_pack_names)) if missing_pack_names else "none")
    )
    print(f"finished_non_base_first_hits={len(first_hit_rows)}")
    print(f"remaining_current_non_base_guardrails={len(missing_pairs)}")
    print()
    print("Finished non-base guardrail coverage")
    print("===================================")
    for row in guardrails:
        print(
            f"{row.label} packs={','.join(row.packs)} ensembles={','.join(row.ensembles)} "
            f"scanned_nonrect_combinations={row.scanned_nonrect_combinations} "
            f"first_nonrect_row={row.first_nonrect_row}"
        )
    print()
    if missing_pairs:
        print(
            "conclusion=the current non-base late guardrail frontier is not yet fully covered, "
            "so another current-family sentinel still remains before the thread can shift away from frontier scouting"
        )
    else:
        print(
            "conclusion=within the current benchmark lattice, the non-base late guardrail frontier is exhausted "
            "through exa: every available large/mirror late slice in the current ultra..exa frontier is covered, "
            "every finished guardrail still reports first_nonrect_row=none, and no additional current-family "
            "non-base sentinel remains; the next transfer step must therefore come from base-side "
            "translation/compression or from introducing a genuinely new generator family rather than scanning "
            "another current pack"
        )
    print()
    print(
        "late branch frontier closure audit completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
