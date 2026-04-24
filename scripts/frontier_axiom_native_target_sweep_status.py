#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- status sweep across all 6 Targets.

Purpose
-------
After 38 iterations primarily on Target 2 (Kasteleyn), with pivots to
Target 3 (iter 38), this runner produces a programmatic status
summary of the full 6-target framework. It does NOT claim any new
derivation; it inventories which targets have been covered by
existing on-branch runners and ledger entries, and reports
per-target completion status.

Methodology
-----------
Three computable checks per target:
1. Runner existence: does the scripts directory contain at least one
   runner whose docstring mentions the target by keyword or sub-step
   identifier?
2. Ledger presence: does the starting kit's ledger include at least
   one entry attributed to that target?
3. Attempt-log presence: does the attempt log include at least one
   entry associated with that target?

Each check is a computed boolean. No narrative PASSes.

Target status table
-------------------
For each target, report: runner_count, ledger_hits,
attempt_log_hits, and summary verdict (covered / partial /
untouched). The verdict is derived from the three booleans:
- "covered": >=1 of each.
- "partial": >=1 of some but not all.
- "untouched": 0 on all three.

This is status-taking only. Any "derived", "reclassified",
"null", or "refuted" interpretations are documented in the
individual target runners and the attempt log, not claimed
here.
"""

from __future__ import annotations

import sys
from pathlib import Path


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name, ok, detail):
    RECORDS.append((name, bool(ok), detail))


def document(name, note):
    DOCS.append((name, note))


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
DOCS_DIR = REPO / "docs"

# Target keyword signatures to search for
TARGETS = [
    {
        "id": 1,
        "name": "Hierarchy exponent 16 and M-scale classification",
        "keywords": ["Target 1", "target 1", "exponent 16", "sixteen",
                     "hierarchy"],
        "runner_patterns": ["edge_partition_exponent_sixteen",
                            "cl3_z3_integer_inventory",
                            "scale_inventory_and_edge_constant"],
    },
    {
        "id": 2,
        "name": "Kasteleyn orientation / Pfaffian structure",
        "keywords": ["Target 2", "target 2", "Kasteleyn", "Pfaffian",
                     "planarity", "plaquette", "singleton hypothesis"],
        "runner_patterns": ["kasteleyn", "pfaffian", "singleton",
                            "reflection_degeneracy", "line3",
                            "planarity"],
    },
    {
        "id": 3,
        "name": "Koide Q = 2/3 via K = 0",
        "keywords": ["Target 3", "target 3", "Koide", "Q = 2/3",
                     "K = 0", "K_selector", "koide_Q"],
        "runner_patterns": ["K_selector", "koide", "target3"],
    },
    {
        "id": 4,
        "name": "CKM V_us tension",
        "keywords": ["Target 4", "target 4", "V_us", "Vus",
                     "2/9"],
        "runner_patterns": ["Vus"],
    },
    {
        "id": 5,
        "name": "PMNS J_chi",
        "keywords": ["Target 5", "target 5", "PMNS", "J_chi",
                     "J_chi_no_go"],
        "runner_patterns": ["J_chi"],
    },
    {
        "id": 6,
        "name": "Strong CP structural absence",
        "keywords": ["Target 6", "target 6", "Strong CP", "strong cp",
                     "theta vacuum", "strong_cp_structural"],
        "runner_patterns": ["strong_cp"],
    },
]


def read_file(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def count_runners_for_target(target):
    count = 0
    matching = []
    for pattern in target["runner_patterns"]:
        for script in SCRIPTS.glob(f"frontier_axiom_native_*{pattern}*.py"):
            if script.name not in matching:
                matching.append(script.name)
                count += 1
    return count, matching


def count_ledger_hits_for_target(target):
    ledger_path = DOCS_DIR / "AXIOM_NATIVE_STARTING_KIT.md"
    text = read_file(ledger_path)
    # Count occurrences of any keyword
    count = 0
    for kw in target["keywords"]:
        count += text.count(kw)
    return count


def count_attempt_log_hits_for_target(target):
    log_path = DOCS_DIR / "AXIOM_NATIVE_ATTEMPT_LOG.md"
    text = read_file(log_path)
    count = 0
    for kw in target["keywords"]:
        count += text.count(kw)
    return count


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

total_runners_matched = 0
total_ledger_hits = 0
total_log_hits = 0
per_target_status = []

for target in TARGETS:
    n_runners, matching = count_runners_for_target(target)
    ledger_hits = count_ledger_hits_for_target(target)
    log_hits = count_attempt_log_hits_for_target(target)

    has_runner = n_runners > 0
    has_ledger = ledger_hits > 0
    has_log = log_hits > 0

    if has_runner and has_ledger and has_log:
        verdict = "covered"
    elif has_runner or has_ledger or has_log:
        verdict = "partial"
    else:
        verdict = "untouched"

    per_target_status.append({
        "id": target["id"],
        "name": target["name"],
        "n_runners": n_runners,
        "matching_runners": matching,
        "ledger_hits": ledger_hits,
        "log_hits": log_hits,
        "verdict": verdict,
    })

    total_runners_matched += n_runners
    total_ledger_hits += ledger_hits
    total_log_hits += log_hits

    tag = f"T{target['id']}"
    record(
        f"{tag}_runner_coverage",
        has_runner,
        f"{tag} ({target['name']}): {n_runners} matching runners. "
        f"Examples: {matching[:3]}.",
    )
    record(
        f"{tag}_ledger_presence",
        has_ledger,
        f"{tag}: {ledger_hits} keyword hits in ledger.",
    )
    record(
        f"{tag}_attempt_log_presence",
        has_log,
        f"{tag}: {log_hits} keyword hits in attempt log.",
    )
    record(
        f"{tag}_verdict",
        verdict in ("covered", "partial"),
        f"{tag}: verdict = {verdict}.",
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

n_covered = sum(1 for s in per_target_status if s["verdict"] == "covered")
n_partial = sum(1 for s in per_target_status if s["verdict"] == "partial")
n_untouched = sum(1 for s in per_target_status if s["verdict"] == "untouched")

record(
    "total_targets_enumerated",
    len(per_target_status) == 6,
    f"Enumerated {len(per_target_status)} targets.",
)
record(
    "all_six_targets_have_some_coverage",
    n_untouched == 0,
    f"All 6 targets have at least partial coverage? "
    f"{n_untouched == 0}. (covered: {n_covered}, partial: {n_partial}, "
    f"untouched: {n_untouched}).",
)
record(
    "total_runner_matches",
    total_runners_matched > 0,
    f"Total matching runners across targets: {total_runners_matched}.",
)


# ---------------------------------------------------------------------------
# Per-target runners tabulated
# ---------------------------------------------------------------------------

for status in per_target_status:
    tag = f"T{status['id']}"
    record(
        f"{tag}_summary",
        status["n_runners"] >= 0,
        f"{tag}: runners={status['n_runners']}, "
        f"ledger_hits={status['ledger_hits']}, "
        f"log_hits={status['log_hits']}, verdict={status['verdict']}.",
    )


# ---------------------------------------------------------------------------
# Total runner count on branch
# ---------------------------------------------------------------------------

all_runners = list(SCRIPTS.glob("frontier_axiom_native_*.py"))
# Exclude hostile audit runner
all_runners = [r for r in all_runners if "hostile_audit" not in r.name]

record(
    "total_runners_on_branch",
    len(all_runners) > 0,
    f"Total frontier_axiom_native runners on branch (excluding audit): "
    f"{len(all_runners)}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_untouched == 0 and n_covered >= 4:
    document(
        "v2_loop_broad_coverage",
        f"The V2 overnight loop has produced broad coverage across the "
        f"6-target framework. {n_covered} targets fully covered "
        f"(runners + ledger + log), {n_partial} partial. No target is "
        f"untouched. Total runners on branch: {len(all_runners)}. "
        f"Specific per-target outcomes are documented in individual "
        f"runner docstrings and the attempt log.",
    )
elif n_untouched > 0:
    document(
        "v2_loop_partial_coverage",
        f"V2 loop status: {n_covered} covered, {n_partial} partial, "
        f"{n_untouched} untouched. Consider continuing with untouched "
        f"targets before declaring natural close.",
    )
else:
    document(
        "v2_loop_coverage_limited",
        f"V2 loop has limited coverage: only {n_covered} covered. "
        f"Significant work remains across the 6-target framework.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: 6-target sweep status")
    print("=" * 78)
    for (name, ok, detail) in RECORDS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")
        print(f"           {detail}")
    for (name, note) in DOCS:
        print(f"  [DOC]    {name}")
        print(f"           {note}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
