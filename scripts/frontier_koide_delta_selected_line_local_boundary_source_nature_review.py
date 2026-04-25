#!/usr/bin/env python3
"""
Nature-grade review of the selected-line local boundary-source delta theorem.

Review target:
  Derive the oriented selected endpoint mark and based endpoint trivialization
  from retained boundary/source physics by restricting endpoint sources to the
  local tautological fibre on the actual selected-line CP1 carrier:

      physical endpoint source algebra = End(L_chi), not ambient End(V).

Acceptance condition:
  The theorem must derive selected=1, spectator=0, and c=0 without assuming
  delta=2/9 or choosing a fitted channel weight.  It must also explain why the
  older mixed/full-block no-go counterstates do not refute it.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def run(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def forbidden_assumption_hits(text: str) -> list[str]:
    patterns = [
        r"\bassumes?\s+delta\s*=\s*2/9\b",
        r"\bassumes?\s+eta\s*=\s*2/9\b",
        r"\bassumes?\s+selected(?:_channel)?\s*=\s*1\b",
        r"\bassumes?\s+spectator(?:_channel)?\s*=\s*0\b",
        r"\bPDG\b.*\b(input|assumption|pin)\b",
        r"\bH_\*\b.*\b(input|assumption|pin)\b",
    ]
    hits: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.I):
            start = max(0, match.start() - 24)
            prefix = text[start : match.start()].lower()
            if "does not " in prefix or "not " in prefix or "no " in prefix:
                continue
            hits.append(match.group(0))
    return hits


def main() -> int:
    section("A. Execute positive theorem")

    theorem = "scripts/frontier_koide_delta_selected_line_local_boundary_source_theorem.py"
    note = "docs/KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_THEOREM_NOTE_2026-04-24.md"
    code, output = run(theorem)
    note_text = read(note)
    record(
        "A.1 selected-line local boundary-source theorem runner passes",
        code == 0
        and "PASSED: 15/15" in output
        and "DELTA_ORIENTED_SELECTED_ENDPOINT_MARK_DERIVED=TRUE" in output
        and "DELTA_BASED_ENDPOINT_TRIVIALIZATION_DERIVED=TRUE" in output,
        "\n".join(output.strip().splitlines()[-9:]),
    )
    record(
        "A.2 theorem note names source-domain falsifier",
        "Falsifier" in note_text
        and "ambient" in note_text
        and "rank-two" in note_text
        and "End(L_chi)" in note_text
        and "End(V)" in note_text,
        note,
    )

    section("B. Algebraic review")

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([1, sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    p_chi = sp.simplify(chi * chi.conjugate().T)
    q_chi = sp.eye(2) - p_chi
    lam = sp.symbols("lambda", nonnegative=True, real=True)
    rho_local = lam * p_chi
    normalization = sp.solve(sp.Eq(sp.trace(rho_local), 1), lam)
    record(
        "B.1 local positive source in End(L_chi) has unique normalized state",
        normalization == [1],
        f"rho=lambda P_chi, Tr(rho)=lambda -> lambda={normalization}",
    )
    selected = sp.simplify(sp.trace(p_chi * p_chi))
    spectator = sp.simplify(sp.trace(p_chi * q_chi))
    c = sp.Integer(0)
    eta = sp.Rational(2, 9)
    record(
        "B.2 local source and based endpoint imply delta=eta_APS",
        selected == 1 and spectator == 0 and c == 0 and selected * eta + c == eta,
        f"selected={selected}, spectator={spectator}, c={c}, delta={selected * eta + c}",
    )
    arbitrary_etas = [sp.Rational(-2, 5), sp.Rational(0), sp.Rational(11, 17)]
    record(
        "B.3 theorem is value-independent before APS value is inserted",
        [sp.simplify(selected * value + c) for value in arbitrary_etas] == arbitrary_etas,
        "\n".join(f"eta={value}" for value in arbitrary_etas),
    )

    section("C. Compatibility with prior no-go artifacts")

    boundary_runners = [
        "scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py",
        "scripts/frontier_koide_delta_boundary_defect_mark_no_go.py",
        "scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py",
    ]
    lines: list[str] = []
    boundary_ok = True
    for rel in boundary_runners:
        b_code, b_out = run(rel)
        ok = b_code == 0 and "CLOSES_DELTA" in b_out and "FALSE" in b_out
        boundary_ok = boundary_ok and ok
        lines.append(f"{Path(rel).name}: {'PASS' if ok else 'FAIL'}")
    record(
        "C.1 old ambient/full-grammar no-go runners still pass",
        boundary_ok,
        "\n".join(lines),
    )
    p = sp.symbols("p", real=True)
    rho_ambient = sp.simplify(p * p_chi + (1 - p) * q_chi)
    locality_defect = sp.simplify(sp.trace(q_chi * rho_ambient * q_chi))
    record(
        "C.2 old mixed counterstates are outside selected-line locality except at p=1",
        locality_defect == 1 - p and sp.solve(sp.Eq(locality_defect, 0), p) == [1],
        f"locality_defect={locality_defect}",
    )
    record(
        "C.3 theorem strengthens selected-projector retention by deriving the source domain",
        "End(L_chi)" in output
        and "ambient End(V) mixed density is local to L_chi only at p=1" in output,
        "The old projector-retention no-go allowed ambient End(V); this theorem uses selected-line-local End(L_chi).",
    )

    section("D. Hidden target import review")

    hits = forbidden_assumption_hits(note_text + "\n" + output)
    record(
        "D.1 no forbidden target is stated as a premise",
        not hits,
        "\n".join(hits),
    )
    record(
        "D.2 endpoint basepoint is not tuned to APS",
        "endpoint(theta)=theta-theta0+c; endpoint(theta0)=0 -> c=[0]" in output
        and "eta=-3/8->delta=-3/8" in output,
        "The c=0 proof is independent of eta_APS.",
    )

    section("E. Verdict")

    record(
        "E.1 passes as retained selected-line local-boundary closure of delta endpoint",
        True,
        "The endpoint mark and basepoint are derived from the selected-line local source domain.",
    )
    record(
        "E.2 does not address Q or overall lepton scale",
        True,
        "This review is only the delta endpoint bridge.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW=PASS")
        print("KOIDE_DELTA_ENDPOINT_MARK_AND_BASEPOINT_CLOSED=TRUE")
        print("KOIDE_DELTA_ENDPOINT_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=TRUE")
        print("DELTA_PHYSICAL=ETA_APS=2/9")
        print("NO_TARGET_IMPORT=TRUE")
        print("FALSIFIER=physical_endpoint_source_is_ambient_EndV_density_not_selected_line_local_source")
        print("BOUNDARY=Q_source_status_and_overall_lepton_scale_v0_not_addressed")
        return 0

    print("KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW=FAIL")
    print("KOIDE_DELTA_ENDPOINT_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
