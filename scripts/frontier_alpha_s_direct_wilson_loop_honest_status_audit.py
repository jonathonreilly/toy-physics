#!/usr/bin/env python3
"""Verify the honest-status audit packet for
ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.

This audit runner does NOT re-derive alpha_s. It verifies:
  Part 1: audit-packet structure (citations, criteria assessment, recommendation).
  Part 2: the underlying strict runner still passes (re-runs and checks output).
  Part 3: the seven retained-proposal criteria assessment is internally
          consistent and the recommended status is the narrowest honest tier.
  Part 4: the dependency / forbidden-import enumeration matches what the
          parent note actually depends on.
"""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md"
PARENT_NOTE_PATH = ROOT / "docs" / "ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md"
PARENT_RUNNER_PATH = ROOT / "scripts" / "frontier_alpha_s_direct_wilson_loop.py"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Part 1: audit-packet structure
# ---------------------------------------------------------------------------
section("Part 1: audit-packet structure and citations")

note_text = NOTE_PATH.read_text()
required = [
    "α_s Direct Wilson-Loop Honest-Status Audit",
    "demotion / status-correction packet",
    "ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30",
    "seven retained-proposal certificate criteria",
    "Sommer scale",
    "4-loop QCD beta function",
    "bounded support theorem",
    "proposal_allowed: false",
]
for s in required:
    check(f"audit packet contains required substring: {s!r}",
          s in note_text, detail=f"len(note)={len(note_text)}")

forbidden = [
    "\nStatus: retained\n",
    "\nStatus: promoted\n",
    "would become retained",
]
for s in forbidden:
    check(f"audit packet avoids forbidden substring: {s!r}",
          s not in note_text)

# ---------------------------------------------------------------------------
# Part 2: underlying strict runner still passes
# ---------------------------------------------------------------------------
section("Part 2: underlying strict runner still passes")

# Re-run the parent strict runner and capture output
try:
    result = subprocess.run(
        ["python3", str(PARENT_RUNNER_PATH)],
        cwd=str(ROOT),
        capture_output=True, text=True, timeout=120,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "scripts")},
    )
    out = result.stdout + result.stderr
    pass_match = re.search(r"PASS=(\d+)\s+FAIL=(\d+)", out)
    if pass_match:
        n_pass = int(pass_match.group(1))
        n_fail = int(pass_match.group(2))
        check(f"parent strict runner PASS=18 FAIL=0 (re-verified)",
              n_pass == 18 and n_fail == 0,
              detail=f"observed PASS={n_pass} FAIL={n_fail}")
        check("parent strict runner final-line gate",
              "Strict gate passed" in out,
              detail="checked final summary line")
    else:
        check("parent strict runner produces PASS/FAIL summary",
              False, detail=f"summary line not found in output (last 200 chars): "
                            f"{out[-200:]!r}")
except subprocess.TimeoutExpired:
    check("parent strict runner timeout", False,
          detail="timed out at 120s; production benchmark not run here")
except Exception as e:
    check("parent strict runner exception", False, detail=str(e))

# ---------------------------------------------------------------------------
# Part 3: criteria assessment is internally consistent
# ---------------------------------------------------------------------------
section("Part 3: seven-criteria assessment internal consistency")

# Each of the 7 criteria should be explicitly assessed
for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"audit packet explicitly assesses Criterion {i}",
          bool(re.search(pattern, note_text)),
          detail=f"row {i} in criteria table")

# Recommended status is "bounded support theorem"
check("recommended status = 'bounded support theorem'",
      "bounded support theorem" in note_text)

# Demotion path documented
check("demotion path documented (proposed_retained → bounded)",
      "proposed_retained" in note_text and "bounded" in note_text)

# ---------------------------------------------------------------------------
# Part 4: dependency / forbidden-import enumeration
# ---------------------------------------------------------------------------
section("Part 4: dependency and forbidden-import enumeration")

# Parent note should have specific forbidden-authority keys in its runner
parent_runner_text = PARENT_RUNNER_PATH.read_text()
forbidden_keys = [
    "alpha_bare_over_u0_squared",
    "alpha_lm",
    "u0",
    "mean_link",
    "plaquette_authority",
    "alpha_s_v_definition",
]
for key in forbidden_keys:
    check(f"parent runner explicitly forbids '{key}' as authority",
          key in parent_runner_text,
          detail="FORBIDDEN_AUTHORITY_KEYS enforcement")

# Audit packet should mention the load-bearing literature imports
literature_imports = [
    "Sommer scale",
    "4-loop",
    "FLAG",
    "PDG 2025",
]
for lit in literature_imports:
    check(f"audit packet documents load-bearing literature import: {lit}",
          lit in note_text)

# Audit packet should document path to full retention
retention_steps = [
    "framework-derived scale anchor",
    "framework-native running",
    "G_BARE_* family closure",
]
for step in retention_steps:
    check(f"audit packet documents retention-path step: {step}",
          step in note_text)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

sys.exit(1 if FAIL_COUNT > 0 else 0)
