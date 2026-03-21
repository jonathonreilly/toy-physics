#!/usr/bin/env python3
"""Sweep suppressor-injection specificity over wider local-morph variant limits."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import pocket_wrap_suppressor_specificity_analysis  # noqa: E402


DEFAULT_LIMITS = (16, 24, 32, 40, 48)


def _safe_label(text: str) -> str:
    return text.encode("unicode_escape").decode("ascii")


def _counts(rows: list) -> tuple[int, int, int]:
    return (
        sum(1 for row in rows if row.single_add_kills),
        sum(1 for row in rows if row.pair_add_kills),
        sum(1 for row in rows if row.pair_matches_collapse),
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor specificity sweep started {started}", flush=True)
    total_start = time.time()

    print()
    print("Pocket-Wrap Suppressor Specificity Sweep")
    print("========================================")
    print(
        "limit | rows | psig | nonpsig | psig single/pair/collapse | "
        "non single/pair/collapse | new pair-sensitive sources"
    )
    print(
        "------+------|------|---------|---------------------------|"
        "--------------------------|----------------------------"
    )

    seen_pair_sensitive: set[str] = set()
    for limit in DEFAULT_LIMITS:
        rows = pocket_wrap_suppressor_specificity_analysis(variant_limit=limit)
        psig_rows = [row for row in rows if row.pocket_signature]
        non_psig_rows = [row for row in rows if not row.pocket_signature]

        psig_single, psig_pair, psig_collapse = _counts(psig_rows)
        non_single, non_pair, non_collapse = _counts(non_psig_rows)

        pair_sensitive = {row.source_name for row in rows if row.pair_add_kills}
        new_pair_sensitive = sorted(pair_sensitive.difference(seen_pair_sensitive))
        seen_pair_sensitive.update(pair_sensitive)
        new_pair_sensitive_text = (
            ",".join(_safe_label(name) for name in new_pair_sensitive)
            if new_pair_sensitive
            else "-"
        )

        print(
            f"{limit:>5} | "
            f"{len(rows):>4} | "
            f"{len(psig_rows):>4} | "
            f"{len(non_psig_rows):>7} | "
            f"{psig_single:>3}/{psig_pair:>3}/{psig_collapse:>3} | "
            f"{non_single:>3}/{non_pair:>3}/{non_collapse:>3} | "
            f"{new_pair_sensitive_text}"
        )

    print()
    print(
        "pocket-wrap suppressor specificity sweep completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
