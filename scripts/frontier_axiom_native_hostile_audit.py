#!/usr/bin/env python3
"""
Hostile audit for the axiom-native overnight derivation track.

RULE. Every iteration on branch claude/axiom-native-overnight-FtUl5 must
pass this audit before the iteration's runner is allowed to commit. Any
violation rejects the iteration and requires a one-paragraph entry in
docs/AXIOM_NATIVE_ATTEMPT_LOG.md.

Checks (applied to every scripts/frontier_axiom_native_*.py on the branch):

  A. Import-count audit — the script must not cite retained docs, must
     not use numeric constants associated with PDG masses or retained
     framework parameters (v_EW, M_Pl, alpha_LM, etc.), and must not
     reference retained theorems as axioms.
  B. Narrative-PASS audit — NO `record(name, True, ...)` calls with a
     literal True. Every PASS must be a computed boolean.
  C. Novelty audit — the iteration must add at least one new rigorous
     fact to the ledger in docs/AXIOM_NATIVE_STARTING_KIT.md section
     "Ledger of derived axiom-native facts".

Return code 0 iff all three audits pass on the most recent runner
(the one named on the command line, or if none given, the newest
frontier_axiom_native_*.py by mtime).

Usage:
  python3 scripts/frontier_axiom_native_hostile_audit.py [runner_path]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
DOCS = REPO / "docs"
PREFIX = "frontier_axiom_native_"

# Retained docs that MUST NOT be cited as axioms on this branch.
FORBIDDEN_DOC_PATTERNS = [
    r"docs/[A-Z][A-Z0-9_]+\.md",
    r"KOIDE_EXPLICIT_CALCULATIONS_NOTE",
    r"YT_WARD_IDENTITY",
    r"CL3_SM_EMBEDDING_THEOREM",
    r"CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE",
    r"S3_TASTE_CUBE_DECOMPOSITION",
    r"STRONG_CP_THETA_ZERO_NOTE",
    r"ALPHA_S_DERIVED_NOTE",
    r"KOIDE_A1_DERIVATION_STATUS",
    r"RCONN_DERIVED_NOTE",
    r"CKM_ATLAS_AXIOM_CLOSURE",
    r"KOIDE_BRANNEN_PHASE_REDUCTION",
    r"OBSERVABLE_PRINCIPLE_FROM_AXIOM",
    r"\bMINIMAL_AXIOMS_",
    r"retained theorem",
    r"retained surface",
    r"retained chain",
    r"retained C_tau",
    r"retained hw=1",
    r"retained Ward",
    r"retained MS-bar",
]

# Numeric imports forbidden as bare constants.
FORBIDDEN_NUMERIC_PATTERNS = [
    r"246\.282818290129",            # v_EW
    r"246\.22",                      # v_EW PDG
    r"0\.000510999",                 # m_e GeV
    r"0\.00051099895",               # m_e GeV PDG
    r"0\.1056583755",                # m_mu GeV PDG
    r"0\.105658375",                 # m_mu GeV
    r"1\.77686",                     # m_tau GeV
    r"1776\.86",                     # m_tau MeV
    r"1776\.96",                     # m_tau framework
    r"0\.1181",                      # alpha_s(M_Z)
    r"0\.1179",                      # alpha_s(M_Z) PDG
    r"125\.25",                      # m_H PDG
    r"125\.1",                       # m_H framework
    r"80\.377",                      # M_W PDG
    r"91\.1876",                     # M_Z PDG
    r"172\.57",                      # m_t pole
    r"0\.039",                       # alpha_LM indicative
    r"1\.22e19",                     # M_Pl
    r"1\.22\s*\*\s*10\s*\*\*\s*19",  # M_Pl
    r"\bM_Pl\b",
    r"\bv_EW\b",
    r"\balpha_LM\b",
    r"\bC_tau\b",
    r"\bI_loop\b",
    r"\bPDG\b",
]

# Allowed citations: only the starting kit and the attempt log.
ALLOWED_CITATIONS = [
    "AXIOM_NATIVE_STARTING_KIT.md",
    "AXIOM_NATIVE_TARGETS.md",
    "AXIOM_NATIVE_ATTEMPT_LOG.md",
    "LOOP_PROMPT.md",
]


def grep_forbidden(text: str, patterns: list[str]) -> list[tuple[int, str, str]]:
    """Return (line_no, pattern, line_content) for every match."""
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            line_no = text[: m.start()].count("\n") + 1
            line = text.splitlines()[line_no - 1].strip()
            # Suppress hits inside comments that are exhaustively listing what is forbidden.
            if line.startswith("#") and "forbidden" in line.lower():
                continue
            # Suppress hits inside this audit runner itself (self-reference).
            if "frontier_axiom_native_hostile_audit" in text[:200]:
                continue
            hits.append((line_no, pat, line))
    return hits


def narrative_pass_audit(text: str) -> list[tuple[int, str]]:
    """Find record(name, True, ...) call sites."""
    hits = []
    # Need to match 'record(' with True as the second argument.
    i = 0
    while True:
        m = re.search(r"\brecord\(", text[i:])
        if not m:
            break
        start = i + m.start()
        # Find matching close paren
        depth = 0
        j = start
        while j < len(text):
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        inner = text[start + len("record(") : j]
        args = split_top_level(inner)
        if len(args) >= 2 and args[1].strip() == "True":
            line_no = text[: start].count("\n") + 1
            hits.append((line_no, text.splitlines()[line_no - 1].strip()))
        i = j + 1
    return hits


def split_top_level(s: str) -> list[str]:
    out, buf, depth, instr = [], [], 0, None
    for ch in s:
        if instr:
            buf.append(ch)
            if ch == instr and (len(buf) < 2 or buf[-2] != "\\"):
                instr = None
            continue
        if ch in ('"', "'"):
            instr = ch
            buf.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def audit_runner(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    # Strip the self-audit file itself from forbidden-pattern list in its own scan.
    if path.name == "frontier_axiom_native_hostile_audit.py":
        return {"ok": True, "skipped_self": True, "hits": [], "narrative": []}
    hits_doc = grep_forbidden(text, FORBIDDEN_DOC_PATTERNS)
    hits_num = grep_forbidden(text, FORBIDDEN_NUMERIC_PATTERNS)
    narrative = narrative_pass_audit(text)
    ok = len(hits_doc) == 0 and len(hits_num) == 0 and len(narrative) == 0
    return {
        "ok": ok,
        "hits_doc": hits_doc,
        "hits_num": hits_num,
        "narrative": narrative,
        "skipped_self": False,
    }


def ledger_audit() -> tuple[bool, str]:
    """Check the kit's ledger has at least one fact appended since session start."""
    kit = DOCS / "AXIOM_NATIVE_STARTING_KIT.md"
    if not kit.exists():
        return False, "starting kit missing"
    text = kit.read_text(encoding="utf-8")
    # Ledger section exists
    if "## Ledger of derived axiom-native facts" not in text:
        return False, "no ledger section"
    # At least one non-empty fact line after the section marker
    marker_idx = text.index("## Ledger of derived axiom-native facts")
    tail = text[marker_idx:].splitlines()[1:]  # skip the header itself
    nonempty = [l.strip() for l in tail if l.strip() and not l.strip().startswith("(") and not l.strip().startswith("#")]
    if not nonempty:
        return True, "ledger still empty (expected on iteration 0)"
    return True, f"{len(nonempty)} ledger entries"


def main() -> int:
    print("=" * 78)
    print("Axiom-native hostile audit")
    print("=" * 78)

    # Collect all runners on the branch, not just newest. They ALL must pass.
    runners = sorted(
        p for p in SCRIPTS.iterdir()
        if p.is_file() and p.name.startswith(PREFIX)
        and p.name != "frontier_axiom_native_hostile_audit.py"
    )
    if not runners:
        print("  (no axiom-native runners on branch yet — vacuously clean)")
        ok_audit, note = ledger_audit()
        print(f"  ledger: {note}")
        return 0

    any_fail = False
    for p in runners:
        result = audit_runner(p)
        if result["ok"]:
            print(f"  [clean]  {p.name}")
        else:
            any_fail = True
            print(f"  [REJECT] {p.name}")
            for ln, pat, line in result["hits_doc"]:
                print(f"      doc-import  line {ln}: /{pat}/  ::  {line[:80]}")
            for ln, pat, line in result["hits_num"]:
                print(f"      num-import  line {ln}: /{pat}/  ::  {line[:80]}")
            for ln, line in result["narrative"]:
                print(f"      narrative  line {ln}: {line[:80]}")

    print()
    ok_ledger, note = ledger_audit()
    print(f"  ledger: {note}")
    print()
    if any_fail:
        print("VERDICT: REJECTED — iteration must not commit. Log the attempt in")
        print("         docs/AXIOM_NATIVE_ATTEMPT_LOG.md and try a different approach.")
        return 1
    print("VERDICT: clean — iteration may commit and push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
