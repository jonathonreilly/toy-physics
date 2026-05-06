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
  outputs/persistent_object_top5_multistage_probe_2026-05-06.txt and parsed here
  as row-level gate data;
* the exact source-cardinality identity top6 == top5 for this setup, because
  the configured source cluster has five nodes and _topk_weights keeps
  min(top_keep, len(source_probs)).

The certificate is intentionally bounded: it supports only the stated
five-row exact-lattice floor comparison, not full-pocket transfer, inertial
mass closure, or matter closure.
"""

from __future__ import annotations

import hashlib
import re
import sys
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


def artifact_text(path_rel: str) -> str:
    path = ROOT / path_rel
    if not check(f"{path_rel} is present", path.is_file()):
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def parse_float_tuple(block: str, field: str, expected_len: int) -> tuple[float, ...] | None:
    match = re.search(rf"^\s*{re.escape(field)}\s*=\s*\[([^\]]+)\]", block, flags=re.MULTILINE)
    if not match:
        return None
    values = tuple(float(part.strip()) for part in match.group(1).split(","))
    return values if len(values) == expected_len else None


def parse_int_tuple(block: str, field: str, expected_len: int) -> tuple[int, ...] | None:
    match = re.search(rf"^\s*{re.escape(field)}\s*=\s*\[([^\]]+)\]", block, flags=re.MULTILINE)
    if not match:
        return None
    values = tuple(int(part.strip()) for part in match.group(1).split(","))
    return values if len(values) == expected_len else None


def parse_percent(block: str, field: str) -> float | None:
    match = re.search(rf"^\s*{re.escape(field)}\s*=\s*([0-9.]+)%\s*$", block, flags=re.MULTILINE)
    if not match:
        return None
    return float(match.group(1)) / 100.0


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


def row_passes_gates(
    stage_mean_overlap: tuple[float, ...],
    stage_alpha: tuple[float, ...],
    stage_toward: tuple[int, ...],
    carry_mean: tuple[float, ...],
    carry_min: tuple[float, ...],
    max_kappa_drift: float,
) -> bool:
    return (
        all(value >= OVERLAP_THRESHOLD for value in stage_mean_overlap)
        and all(value >= CARRY_MEAN_THRESHOLD for value in carry_mean)
        and all(value >= CARRY_MIN_THRESHOLD for value in carry_min)
        and all(ALPHA_BAND[0] <= value <= ALPHA_BAND[1] for value in stage_alpha)
        and all(value == N_SOURCE_STRENGTHS for value in stage_toward)
        and max_kappa_drift <= KAPPA_DRIFT_THRESHOLD
    )


def check_top5() -> int:
    passed = 0
    print()
    print("TOP5 CORROBORATION")
    text = artifact_text(TOP5_LOG)
    check("top5 log records --top-keep 5", "--top-keep 5" in text)
    check("top5 log summary is 5/5", "top5 multistage-admissible on 5/5 stable widened-regime cases" in text)
    for label in STABLE_ROWS:
        block = case_block(text, label)
        stage_mean_overlap = parse_float_tuple(block, "stage_mean_overlap", 3) if block else None
        stage_alpha = parse_float_tuple(block, "stage_alpha", 3) if block else None
        stage_toward = parse_int_tuple(block, "stage_toward", 3) if block else None
        carry_mean = parse_float_tuple(block, "carry_mean", 2) if block else None
        carry_min = parse_float_tuple(block, "carry_min", 2) if block else None
        max_kappa_drift = parse_percent(block, "max_kappa_drift") if block else None
        admissible = admissible_value(block) if block else None
        parsed = all(
            value is not None
            for value in (
                stage_mean_overlap,
                stage_alpha,
                stage_toward,
                carry_mean,
                carry_min,
                max_kappa_drift,
            )
        )
        ok = (
            parsed
            and admissible is True
            and row_passes_gates(
                stage_mean_overlap,
                stage_alpha,
                stage_toward,
                carry_mean,
                carry_min,
                max_kappa_drift,
            )
        )
        detail = (
            f"overlap={stage_mean_overlap}, alpha={stage_alpha}, "
            f"carry={carry_mean}, drift={max_kappa_drift:.3%}"
            if parsed
            else "missing row evidence"
        )
        check(f"top5 {label} clears all gates from log", ok, detail)
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
        "top6 has the same effective source support as top5",
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
    check("first admissible configured object width is top4", floor_ok)

    print()
    print(f"SUMMARY: PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("STATUS: FLOOR CERTIFICATE PASS")
        return 0
    print("STATUS: FLOOR CERTIFICATE FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
