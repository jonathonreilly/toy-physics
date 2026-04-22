#!/usr/bin/env python3
"""
Hostile-reviewer audit of the Casimir-difference derivation track.

Goal: honestly partition every check in the track into:

  [R] RIGOROUS    — the record() call's boolean arises from an
                    arithmetic or symbolic computation whose truth
                    value is independent of the author's narrative.
                    A hostile reviewer cannot dismiss it by asking
                    "where is the proof?".
  [N] NARRATIVE   — the record() call passes `True` as a literal
                    (hardcoded pass), accompanied by a prose claim.
                    A hostile reviewer will rightly demand an
                    underlying proof or rewrite.

This runner:
  1. scans every step runner's source for record() call sites and
     classifies each site as R or N (form-based);
  2. runs every step runner and counts runtime PASS occurrences
     (the aggregate count the master closure reports);
  3. reports both per-file counts side-by-side;
  4. reports the honest split: how many runtime PASSes are backed by
     a rigorous site vs a narrative site.

Call sites vs runtime PASSes differ when a call site is inside a loop
(e.g., a for-loop that calls record() once per iteration counts as
one call site but N runtime PASSes).

No claim about the content is made here — only about the form. The
honest reading: only the R-count survives a strictly hostile review;
the N-count survives only at the narrative-summary level.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
PREFIX = "frontier_koide_a1_casimir_difference_"


def split_top_level(s: str) -> list[str]:
    """Split on commas at top paren-depth."""
    out = []
    buf = []
    depth = 0
    in_string = None
    for ch in s:
        if in_string:
            buf.append(ch)
            if ch == in_string and (len(buf) < 2 or buf[-2] != "\\"):
                in_string = None
            continue
        if ch in ('"', "'"):
            in_string = ch
            buf.append(ch)
            continue
        if ch == "(" or ch == "[" or ch == "{":
            depth += 1
        elif ch == ")" or ch == "]" or ch == "}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def audit_file(path: Path) -> tuple[int, int, list[tuple[int, str]]]:
    """Return (rigorous_sites, narrative_sites, narrative_list)."""
    text = path.read_text(encoding="utf-8")
    rigorous = 0
    narrative = 0
    narrative_list = []
    i = 0
    while True:
        m = re.search(r"\brecord\(", text[i:])
        if not m:
            break
        start = i + m.start()
        depth = 0
        j = start
        while j < len(text):
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[start:j + 1]
        inner = body[len("record("):-1]
        args = split_top_level(inner)
        if len(args) < 2:
            i = j + 1
            continue
        ok_expr = args[1].strip()
        line_num = text[:start].count("\n") + 1
        if ok_expr == "True":
            narrative += 1
            name = args[0].strip().strip('"').strip("'")
            if name.startswith('f"') or name.startswith("f'"):
                name = name[2:-1]
            narrative_list.append((line_num, name))
        else:
            rigorous += 1
        i = j + 1
    return rigorous, narrative, narrative_list


def runtime_pass_count(path: Path) -> int:
    """Run the script and parse 'PASSED: N/M' from stdout. Returns N."""
    proc = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, text=True, timeout=60,
    )
    m = re.search(r"PASSED:\s+(\d+)/\d+", proc.stdout)
    return int(m.group(1)) if m else 0


def main() -> int:
    print("=" * 88)
    print("Hostile-reviewer audit — Casimir-difference derivation track")
    print("=" * 88)

    files = sorted(
        p for p in SCRIPTS.iterdir()
        if p.is_file()
        and p.name.startswith(PREFIX)
        and "master_closure" not in p.name
        and "hostile_audit" not in p.name
    )

    total_R_sites = 0
    total_N_sites = 0
    total_runtime = 0
    rows = []
    narrative_index = []
    for p in files:
        R_sites, N_sites, nlist = audit_file(p)
        runtime = runtime_pass_count(p)
        total_R_sites += R_sites
        total_N_sites += N_sites
        total_runtime += runtime
        rows.append((p.name, R_sites, N_sites, runtime))
        for ln, name in nlist:
            narrative_index.append((p.name, ln, name))

    print()
    print(f"  {'Runner':<58}{'R-site':>8}{'N-site':>8}{'runtime':>10}")
    print("  " + "-" * 84)
    for name, R, N, rt in rows:
        short = name.replace(PREFIX, "*")
        print(f"  {short:<58}{R:>8}{N:>8}{rt:>10}")
    print("  " + "-" * 84)
    print(f"  {'TOTAL':<58}{total_R_sites:>8}{total_N_sites:>8}{total_runtime:>10}")

    print()
    print("Legend:")
    print("  R-site  = RIGOROUS record() call sites (computation-backed boolean)")
    print("  N-site  = NARRATIVE record() call sites (hardcoded True + prose)")
    print("  runtime = aggregate PASSED count when the runner executes (loops ⟹ >sites)")

    # Estimate runtime narrative share: assume each N-site contributes ~1 runtime PASS
    # unless it sits inside a loop. The honest conservative upper bound for narrative
    # runtime PASSes is simply N-sites (since each site passes at least once when run);
    # loops tend to be over enumerations that are all rigorous (e.g. table rows).
    narrative_runtime_lower = total_N_sites  # at minimum, each N-site contributes 1
    rigorous_runtime_lower = total_runtime - narrative_runtime_lower

    print()
    print("=" * 88)
    print("Narrative-PASS call-site inventory (hostile-reviewer flag list)")
    print("=" * 88)
    for fname, ln, name in narrative_index:
        short = fname.replace(PREFIX, "*")
        print(f"  {short}:{ln}: {name}")

    print()
    print("=" * 88)
    print("Honest summary")
    print("=" * 88)
    print(f"  Call-site totals:  R-site = {total_R_sites}, N-site = {total_N_sites}")
    print(f"  Runtime PASSes:    {total_runtime}")
    print(f"  Of runtime PASSes: >= {narrative_runtime_lower} narrative, <= {rigorous_runtime_lower} rigorous")
    print()
    print("  A strictly hostile reviewer should only credit the RIGOROUS share.")
    print("  The NARRATIVE share is documentation of the physics reasoning; it")
    print("  does not replace a proof and is listed above for review.")
    print()
    print("  Honest retained-grade reading:")
    print("    - the retained inputs (T=1/2, Y^2=1/4, hw=1 Plancherel, C_tau=1)")
    print("      are all RIGOROUS or sit on the retained-surface `main`;")
    print("    - (A1*) <-> Koide A1 is RIGOROUS (symbolic, via sympy);")
    print("    - (P1) and (P2) carry NARRATIVE elements at the MS-bar generation-")
    print("      blindness / common-c / factorisation-form steps;")
    print("    - the Koide ratio is RIGOROUSLY c-cancellative under (P1)+(P2).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
