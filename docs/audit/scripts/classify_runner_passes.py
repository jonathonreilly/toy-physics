#!/usr/bin/env python3
"""Statically classify what each runner script actually checks.

This script is heuristic. It parses each runner's Python source for
patterns indicating the four check classes:

  (A) algebraic identity check on existing inputs
       -> sympy.simplify, sympy.Eq, math.isclose against derived quantity,
          assert lhs == rhs where both lhs and rhs are framework-computed
  (B) cross-note input verification (reads value from another note)
       -> file reads of *.md, regex extraction of `Status:` lines or
          numeric constants from sibling notes
  (C) first-principles compute from the Cl(3)/Z^3 axiom
       -> imports of canonical_plaquette_surface, lattice operator builds,
          eigenvalue decompositions, large numerical computations producing
          new numbers (heuristic only)
  (D) external comparator check against PDG / lattice QCD / observation
       -> string literals containing 'PDG', 'observed', 'comparator',
          numeric constants matching well-known PDG values

Writes docs/audit/data/runner_classification.json with per-runner counts
and per-claim aggregations.

Limits: this is static analysis, not execution. The output is suggestive,
not authoritative. The real classification is set by the audit agent
(Codex GPT-5.5) using the prompt template, with this file as a hint.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
OUTPUT_PATH = DATA_DIR / "runner_classification.json"

# Heuristic patterns. These are deliberately conservative; the audit
# agent overrides any of them.
PATTERNS_A = [
    re.compile(r"sympy\.(?:simplify|Eq|expand|factor)\b"),
    re.compile(r"\.equals\("),
    re.compile(r"math\.isclose\b"),
    re.compile(r"assert\s+abs\("),
    re.compile(r"assert\s+np\.allclose\("),
    re.compile(r"assert\s+sympy\."),
]
PATTERNS_B = [
    re.compile(r"open\([^)]*\.md[^)]*\)"),
    re.compile(r"Path\([^)]*\.md[^)]*\)"),
    re.compile(r"read_text\([^)]*\)"),
    re.compile(r"^\s*Status:?\s*", re.MULTILINE),
    re.compile(r"verbatim\s+Status"),
    re.compile(r"extract.*Status", re.IGNORECASE),
    re.compile(r"cited authority", re.IGNORECASE),
]
PATTERNS_C = [
    re.compile(r"canonical_plaquette_surface"),
    re.compile(r"\beigvals?\("),
    re.compile(r"\beigh?\("),
    re.compile(r"staggered.*[Dd]irac"),
    re.compile(r"Wilson.*action", re.IGNORECASE),
    re.compile(r"plaquette", re.IGNORECASE),
    re.compile(r"lattice.*config", re.IGNORECASE),
    re.compile(r"(?:np|numpy|jax)\.linalg"),
]
PATTERNS_D = [
    re.compile(r"\bPDG\b"),
    re.compile(r"\bobserved\b", re.IGNORECASE),
    re.compile(r"\bcomparator\b", re.IGNORECASE),
    re.compile(r"experimental", re.IGNORECASE),
    re.compile(r"measured", re.IGNORECASE),
    # Common PDG numbers as a weak signal.
    re.compile(r"\b0\.117[0-9]\b"),     # alpha_s(M_Z)
    re.compile(r"\b125\.\d+\b.*GeV", re.IGNORECASE),  # Higgs mass
    re.compile(r"\b80\.\d{3,}\b.*GeV", re.IGNORECASE),  # W mass
    re.compile(r"\b246\.\d+\b.*GeV", re.IGNORECASE),  # v
    re.compile(r"\b172\.\d+\b.*GeV", re.IGNORECASE),  # m_t
]

# Anti-pattern: if a check is inside an "extract authority" or "verify
# tier" function, it's class B even if it has assert numpy.allclose.
ANTI_C_CONTEXT = [
    re.compile(r"extract.*tier", re.IGNORECASE),
    re.compile(r"verify.*status", re.IGNORECASE),
    re.compile(r"check.*authority", re.IGNORECASE),
]


def count_assert_pass_lines(source: str) -> int:
    """Approximate count of distinct check points (assert / PASS lines)."""
    return len(re.findall(r"^\s*assert\b", source, re.MULTILINE)) + \
           len(re.findall(r"PASS\+?=", source))


def classify_source(source: str) -> dict[str, int]:
    counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for p in PATTERNS_A:
        counts["A"] += len(p.findall(source))
    for p in PATTERNS_B:
        counts["B"] += len(p.findall(source))
    for p in PATTERNS_C:
        counts["C"] += len(p.findall(source))
    for p in PATTERNS_D:
        counts["D"] += len(p.findall(source))

    # If anti-C context is heavy, dampen C and bump B.
    anti_c_hits = sum(len(p.findall(source)) for p in ANTI_C_CONTEXT)
    if anti_c_hits > 0 and counts["C"] > 0:
        moved = min(counts["C"], anti_c_hits)
        counts["C"] -= moved
        counts["B"] += moved
    return counts


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    per_runner: dict[str, dict] = {}
    per_claim: dict[str, dict] = {}
    runner_to_claims: dict[str, list[str]] = {}

    for cid, row in rows.items():
        runner = row.get("runner_path")
        if not runner:
            continue
        runner_to_claims.setdefault(runner, []).append(cid)

    for runner, claims in runner_to_claims.items():
        runner_path = REPO_ROOT / runner
        if not runner_path.exists():
            per_runner[runner] = {
                "exists": False,
                "claims": claims,
                "counts": {"A": 0, "B": 0, "C": 0, "D": 0},
                "assert_count": 0,
                "dominant_class": None,
                "decoration_candidate": False,
            }
            continue
        try:
            source = runner_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            per_runner[runner] = {
                "exists": True,
                "read_error": str(e),
                "claims": claims,
            }
            continue
        counts = classify_source(source)
        asserts = count_assert_pass_lines(source)
        dominant = max(counts, key=lambda k: counts[k]) if any(counts.values()) else None
        per_runner[runner] = {
            "exists": True,
            "claims": claims,
            "counts": counts,
            "assert_count": asserts,
            "dominant_class": dominant,
            "decoration_candidate": (counts["D"] == 0 and counts["C"] == 0 and counts["A"] + counts["B"] > 0),
        }

    # Aggregate per-claim from runner. Multiple claims may share a runner.
    for runner, data in per_runner.items():
        for cid in data.get("claims", []):
            per_claim[cid] = {
                "runner": runner,
                "counts": data.get("counts", {"A": 0, "B": 0, "C": 0, "D": 0}),
                "assert_count": data.get("assert_count", 0),
                "dominant_class": data.get("dominant_class"),
                "decoration_candidate": data.get("decoration_candidate", False),
            }

    # Stats.
    n_runners = len(per_runner)
    n_decoration_candidates = sum(1 for d in per_runner.values() if d.get("decoration_candidate"))
    n_with_d = sum(1 for d in per_runner.values() if d.get("counts", {}).get("D", 0) > 0)
    n_with_c = sum(1 for d in per_runner.values() if d.get("counts", {}).get("C", 0) > 0)
    dominant_distribution: dict[str, int] = {}
    for d in per_runner.values():
        k = d.get("dominant_class") or "none"
        dominant_distribution[k] = dominant_distribution.get(k, 0) + 1

    out = {
        "schema_version": 1,
        "stats": {
            "runners_classified": n_runners,
            "runners_with_C": n_with_c,
            "runners_with_D": n_with_d,
            "decoration_candidates": n_decoration_candidates,
            "dominant_class_distribution": dominant_distribution,
        },
        "per_runner": per_runner,
        "per_claim": per_claim,
    }

    OUTPUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  runners classified: {n_runners}")
    print(f"  runners with (C) first-principles compute hits: {n_with_c}")
    print(f"  runners with (D) external comparator hits: {n_with_d}")
    print(f"  decoration candidates (no C, no D): {n_decoration_candidates}")
    print(f"  dominant class distribution: {dominant_distribution}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
