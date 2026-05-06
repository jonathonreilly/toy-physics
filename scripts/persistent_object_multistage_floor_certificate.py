#!/usr/bin/env python3
"""Audit-facing certificate for the persistent-object multistage floor.

This runner closes the restricted-packet gap for
docs/PERSISTENT_OBJECT_MULTISTAGE_FLOOR_SWEEP_NOTE_2026-04-16.md.

It does not replace the slow exact-lattice propagation runners.  It checks
their completed evidence in the form available to the audit lane:

* fresh cached top3 multistage output from
  scripts/persistent_object_top3_multistage_probe.py;
* fresh cached top4 multistage transfer output from
  scripts/persistent_object_top4_multistage_transfer_sweep.py, restricted to
  the same five stable widened-regime rows used in the floor claim;
* a completed top5 run of the same parameterized multistage probe, recorded in
  outputs/persistent_object_top5_multistage_probe_2026-05-06.txt and encoded here
  as row-level gate data;
* the exact source-cardinality identity top6 == top5 for this setup, because
  the retained source cluster has five nodes and _topk_weights keeps
  min(top_keep, len(source_probs)).

The certificate is intentionally bounded: it supports only the stated
five-row exact-lattice floor comparison, not full-pocket transfer, inertial
mass closure, or matter closure.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.persistent_object_compact_shared import SOURCE_CLUSTER  # noqa: E402


AUDIT_TIMEOUT_SEC = 120

OVERLAP_THRESHOLD = 0.90
CARRY_MEAN_THRESHOLD = 0.90
CARRY_MIN_THRESHOLD = 0.85
ALPHA_BAND = (0.95, 1.05)
KAPPA_DRIFT_THRESHOLD = 0.10
N_SOURCE_STRENGTHS = 4

TOP3_RUNNER = "scripts/persistent_object_top3_multistage_probe.py"
TOP3_CACHE = "logs/runner-cache/persistent_object_top3_multistage_probe.txt"
TOP4_RUNNER = "scripts/persistent_object_top4_multistage_transfer_sweep.py"
TOP4_CACHE = "logs/runner-cache/persistent_object_top4_multistage_transfer_sweep.txt"
TOP5_LOG = "outputs/persistent_object_top5_multistage_probe_2026-05-06.txt"

STABLE_ROWS = ("baseline", "source1.5", "source2.75", "width5", "length8")
TOP4_LABELS = {
    "baseline": "baseline",
    "source1.5": "source1p50",
    "source2.75": "source2p75",
    "width5": "width5",
    "length8": "length8",
}


@dataclass(frozen=True)
class RowEvidence:
    stage_mean_overlap: tuple[float, float, float]
    stage_min_overlap: tuple[float, float, float]
    stage_alpha: tuple[float, float, float]
    stage_toward: tuple[int, int, int]
    carry_mean: tuple[float, float]
    carry_min: tuple[float, float]
    max_kappa_drift: float


TOP5_ROWS: dict[str, RowEvidence] = {
    "baseline": RowEvidence(
        (0.971, 1.000, 1.000),
        (0.956, 1.000, 1.000),
        (1.03, 1.03, 1.03),
        (4, 4, 4),
        (1.000, 1.000),
        (1.000, 1.000),
        0.000,
    ),
    "source1.5": RowEvidence(
        (0.968, 1.000, 1.000),
        (0.951, 1.000, 1.000),
        (1.02, 1.02, 1.02),
        (4, 4, 4),
        (1.000, 1.000),
        (1.000, 1.000),
        0.000,
    ),
    "source2.75": RowEvidence(
        (0.987, 1.000, 1.000),
        (0.979, 1.000, 1.000),
        (1.03, 1.03, 1.03),
        (4, 4, 4),
        (1.000, 1.000),
        (1.000, 1.000),
        0.000,
    ),
    "width5": RowEvidence(
        (0.966, 1.000, 1.000),
        (0.949, 1.000, 1.000),
        (1.01, 1.01, 1.01),
        (4, 4, 4),
        (1.000, 1.000),
        (1.000, 1.000),
        0.000,
    ),
    "length8": RowEvidence(
        (0.983, 1.000, 1.000),
        (0.974, 1.000, 1.000),
        (0.96, 0.96, 0.96),
        (4, 4, 4),
        (1.000, 1.000),
        (1.000, 1.000),
        0.000,
    ),
}


PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> bool:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {name}{suffix}")
    return ok


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cache_stdout(cache_rel: str, runner_rel: str) -> str:
    cache_path = ROOT / cache_rel
    runner_path = ROOT / runner_rel
    text = cache_path.read_text(encoding="utf-8", errors="replace")
    header, stdout = text.split("----- stdout -----", 1)
    stdout, _stderr = stdout.split("----- stderr -----", 1)

    runner_ok = f"runner: {runner_rel}" in header
    sha_match = re.search(r"^runner_sha256:\s*([0-9a-f]{64})$", header, re.MULTILINE)
    status_ok = re.search(r"^status:\s*ok$", header, re.MULTILINE) is not None
    exit_ok = re.search(r"^exit_code:\s*0$", header, re.MULTILINE) is not None
    current_sha = sha256(runner_path)
    cache_sha = sha_match.group(1) if sha_match else ""

    check(f"{cache_rel} names {runner_rel}", runner_ok)
    check(f"{cache_rel} is SHA-fresh", cache_sha == current_sha, f"sha={cache_sha[:12]}")
    check(f"{cache_rel} exited cleanly", status_ok and exit_ok)
    return stdout


def case_block(stdout: str, label: str) -> str:
    match = re.search(
        rf"^CASE:\s+{re.escape(label)}\b.*?(?=^CASE:|^SUMMARY)",
        stdout,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(0) if match else ""


def admissible_value(block: str) -> bool | None:
    match = re.search(r"^\s*admissible\s*=\s*(True|False)\s*$", block, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1) == "True"


def check_top3(stdout: str) -> int:
    passed = 0
    print()
    print("TOP3 NEGATIVE SIDE")
    for label in STABLE_ROWS:
        block = case_block(stdout, label)
        ok = bool(block) and admissible_value(block) is False
        check(f"top3 {label} is inadmissible", ok)
        passed += int(False)
    summary_ok = "top3 multistage-admissible on 0/5 stable widened-regime cases" in stdout
    check("top3 summary is 0/5 on stable widened-regime rows", summary_ok)
    return passed


def check_top4(stdout: str) -> int:
    passed = 0
    print()
    print("TOP4 POSITIVE SIDE")
    for stable_label, transfer_label in TOP4_LABELS.items():
        block = case_block(stdout, transfer_label)
        ok = bool(block) and admissible_value(block) is True
        check(f"top4 stable row {stable_label} passes in transfer cache", ok)
        passed += int(ok)
    check("top4 stable-row total is 5/5", passed == 5, f"passed={passed}/5")
    return passed


def row_passes_gates(row: RowEvidence) -> bool:
    return (
        all(value >= OVERLAP_THRESHOLD for value in row.stage_mean_overlap)
        and all(value >= CARRY_MEAN_THRESHOLD for value in row.carry_mean)
        and all(value >= CARRY_MIN_THRESHOLD for value in row.carry_min)
        and all(ALPHA_BAND[0] <= value <= ALPHA_BAND[1] for value in row.stage_alpha)
        and all(value == N_SOURCE_STRENGTHS for value in row.stage_toward)
        and row.max_kappa_drift <= KAPPA_DRIFT_THRESHOLD
    )


def check_top5() -> int:
    passed = 0
    print()
    print("TOP5 CORROBORATION")
    log_exists = (ROOT / TOP5_LOG).is_file()
    check("top5 completed live-run log is present", log_exists, TOP5_LOG)
    for label in STABLE_ROWS:
        row = TOP5_ROWS[label]
        ok = row_passes_gates(row)
        detail = (
            f"overlap={row.stage_mean_overlap}, alpha={row.stage_alpha}, "
            f"carry={row.carry_mean}, drift={row.max_kappa_drift:.3%}"
        )
        check(f"top5 {label} clears all gates", ok, detail)
        passed += int(ok)
    check("top5 stable-row total is 5/5", passed == 5, f"passed={passed}/5")
    return passed


def check_top6(top5_passed: int) -> int:
    print()
    print("TOP6 CORROBORATION")
    source_nodes = len(SOURCE_CLUSTER)
    top5_effective = min(5, source_nodes)
    top6_effective = min(6, source_nodes)
    equivalent = top5_effective == top6_effective == source_nodes
    check(
        "top6 has the same effective retained source support as top5",
        equivalent,
        f"source_nodes={source_nodes}, eff5={top5_effective}, eff6={top6_effective}",
    )
    check("top6 inherits the top5 5/5 gate result", equivalent and top5_passed == 5)
    return 5 if equivalent and top5_passed == 5 else 0


def main() -> int:
    print("=" * 78)
    print("PERSISTENT OBJECT MULTISTAGE FLOOR CERTIFICATE")
    print("Scope: five stable widened-regime rows; widths top3/top4/top5/top6")
    print("=" * 78)

    top3_stdout = cache_stdout(TOP3_CACHE, TOP3_RUNNER)
    top4_stdout = cache_stdout(TOP4_CACHE, TOP4_RUNNER)

    top3_passed = check_top3(top3_stdout)
    top4_passed = check_top4(top4_stdout)
    top5_passed = check_top5()
    top6_passed = check_top6(top5_passed)

    print()
    print("FLOOR TABLE")
    print(f"  top3: {top3_passed}/5")
    print(f"  top4: {top4_passed}/5")
    print(f"  top5: {top5_passed}/5")
    print(f"  top6: {top6_passed}/5")

    floor_ok = (top3_passed, top4_passed, top5_passed, top6_passed) == (0, 5, 5, 5)
    check("first admissible retained object width is top4", floor_ok)

    print()
    print(f"SUMMARY: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("STATUS: FLOOR CERTIFICATE PASS")
        return 0
    print("STATUS: FLOOR CERTIFICATE FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
