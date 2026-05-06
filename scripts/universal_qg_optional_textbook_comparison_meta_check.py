#!/usr/bin/env python3
"""Replay the zero-authority invariant for the universal-QG optional note.

The checked object is metadata, not a physics derivation. The load-bearing
predicate is that the note is self-contained, typed as meta, declares zero
authority, registers no markdown dependency edges of its own, and is cited
elsewhere only in explicitly optional/packaging contexts.
"""
from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTE_REL = Path("docs") / "UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md"
NOTE_PATH = REPO_ROOT / NOTE_REL
RUNNER_REL = Path("scripts/universal_qg_optional_textbook_comparison_meta_check.py")
TARGET_NAME = NOTE_REL.name
DOC_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")


@dataclass
class CheckResult:
    label: str
    cls: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    with path.open(encoding="utf-8") as handle:
        return handle.read()


def field(body: str, name: str) -> str:
    start_re = re.compile(rf"^\s*\*\*{re.escape(name)}:?\*\*\s*(.+)$", re.IGNORECASE)
    lines_iter = body.splitlines()
    for index, raw in enumerate(lines_iter):
        match = start_re.match(raw)
        if not match:
            continue
        lines = [match.group(1).strip()]
        for continuation in lines_iter[index + 1 :]:
            if not continuation.strip():
                break
            if re.match(r"^\s*(?:\*\*[^*]+:\*\*|#{1,6}\s+)", continuation):
                break
            lines.append(continuation.strip())
        return " ".join(lines)
    return ""


def add(results: list[CheckResult], label: str, cls: str, ok: bool, detail: str) -> None:
    results.append(CheckResult(label=label, cls=cls, ok=ok, detail=detail))


def context_guard(context: str) -> bool:
    lowered = " ".join(context.lower().split())
    has_optional = "optional" in lowered or "alternate textbook comparison" in lowered
    has_packaging_guard = any(
        marker in lowered
        for marker in (
            "packaging-only",
            "not part of the theorem stack",
            "not a theorem",
            "not a missing structural theorem",
            "does not change the closed theorem stack",
            "is packaging, not a structural gap",
        )
    )
    return has_optional and has_packaging_guard


def inbound_optional_contexts() -> tuple[bool, int, list[str]]:
    failures: list[str] = []
    count = 0
    for path in sorted((REPO_ROOT / "docs").glob("**/*.md")):
        rel = path.relative_to(REPO_ROOT)
        if rel == NOTE_REL or str(rel).startswith("docs/audit/"):
            continue
        body = read(path)
        for match in re.finditer(re.escape(TARGET_NAME), body):
            count += 1
            start = max(0, match.start() - 280)
            end = min(len(body), match.end() + 280)
            if not context_guard(body[start:end]):
                failures.append(f"{rel}:{body[:match.start()].count(chr(10)) + 1}")
    return not failures, count, failures


def main() -> int:
    body = read(NOTE_PATH)
    results: list[CheckResult] = []

    status = field(body, "Status")
    authority = field(body, "Authority role")
    primary_runner = field(body, "Primary runner")

    add(
        results,
        "note title is the expected optional textbook comparison note",
        "A",
        body.startswith("# Universal QG Optional Textbook Comparison Note\n"),
        str(NOTE_REL),
    )
    add(
        results,
        "Type field is exactly meta",
        "A",
        field(body, "Type").split()[0].strip("`*_:.").lower() == "meta",
        field(body, "Type") or "missing",
    )
    add(
        results,
        "Status field negates theorem, claim, and new authority roles",
        "A",
        all(token in status.lower() for token in ("not", "theorem", "claim", "new authority surface")),
        status or "missing",
    )
    add(
        results,
        "Authority role is zero",
        "A",
        authority.lower().startswith("zero"),
        authority or "missing",
    )
    add(
        results,
        "Primary runner points to this replay script",
        "A",
        str(RUNNER_REL) in primary_runner,
        primary_runner or "missing",
    )
    add(
        results,
        "Source note has no markdown links to other docs",
        "A",
        not DOC_LINK_RE.findall(body),
        ", ".join(DOC_LINK_RE.findall(body)) or "none",
    )
    add(
        results,
        "Source note has no authority-style Citations section",
        "A",
        not re.search(r"^##\s+Citations\s*$", body, re.MULTILINE),
        "Citations heading absent",
    )
    required_claim_rows = [
        "UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md",
        "UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md",
        "UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md",
        "UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md",
        "UNIVERSAL_QG_CONTINUUM_BRIDGE_REDUCTION_NOTE.md",
    ]
    missing_claim_rows = [
        name for name in required_claim_rows if not (REPO_ROOT / "docs" / name).exists()
    ]
    add(
        results,
        "Informational cross-reference rows exist as separate claim files",
        "A",
        not missing_claim_rows and all(f"`{name}`" in body for name in required_claim_rows),
        ", ".join(missing_claim_rows) or "all present as code spans",
    )
    add(
        results,
        "Own-row substantive comparison firewall is explicit",
        "A",
        "must live in its own claim row" in body and "not here" in body,
        "claim-row firewall present",
    )
    inbound_ok, inbound_count, inbound_failures = inbound_optional_contexts()
    add(
        results,
        "Inbound mentions are guarded as optional packaging callouts",
        "B",
        inbound_ok,
        f"{inbound_count} mentions checked" if inbound_ok else ", ".join(inbound_failures),
    )

    print("=" * 72)
    print("UNIVERSAL QG OPTIONAL TEXTBOOK COMPARISON META CHECK")
    print("=" * 72)
    class_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for result in results:
        if result.ok:
            class_counts[result.cls] += 1
        status_word = "PASS" if result.ok else "FAIL"
        print(f"[{status_word} ({result.cls})] {result.label}: {result.detail}")

    total_pass = sum(class_counts.values())
    failure_count = len([result for result in results if not result.ok])
    all_checks_pass = math.isclose(float(failure_count), 0.0, abs_tol=0.0)
    print("-" * 72)
    print(
        "SUMMARY: "
        f"{'PASS' if all_checks_pass else 'FAIL'} "
        f"A={class_counts['A']} B={class_counts['B']} "
        f"C={class_counts['C']} D={class_counts['D']} total_pass={total_pass}"
    )
    return 0 if all_checks_pass else 1


if __name__ == "__main__":
    sys.exit(main())
