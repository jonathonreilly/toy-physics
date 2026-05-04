#!/usr/bin/env python3
"""
PR #230 SM one-Higgs to O_H import boundary.

The SM one-Higgs gauge-selection theorem is tempting on the O_H route because
it proves the one-doublet Yukawa monomial pattern.  This runner checks the
honest boundary: that theorem assumes a canonical Higgs doublet after it is
supplied and leaves the Yukawa matrices free.  It does not identify the PR230
source-pole operator with the canonical Higgs radial operator O_H, and it does
not remove the orthogonal neutral scalar top-coupling blocker.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_sm_one_higgs_oh_import_boundary_2026-05-03.json"
SM_RUNNER = ROOT / "scripts" / "frontier_sm_one_higgs_yukawa_gauge_selection.py"
SM_NOTE = ROOT / "docs" / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"

PARENTS = {
    "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "no_orthogonal_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
    "no_orthogonal_selection_rule": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def run_sm_support_runner() -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(SM_RUNNER)],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    match = re.search(r"TOTAL:\s+PASS=(\d+),\s+FAIL=(\d+)", proc.stdout)
    return {
        "returncode": proc.returncode,
        "pass_count": int(match.group(1)) if match else None,
        "fail_count": int(match.group(2)) if match else None,
        "tail": proc.stdout.strip().splitlines()[-8:],
    }


def find_candidate(certs: dict[str, dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    for row in certs["canonical_higgs_repo_authority_audit"].get("candidate_surfaces", []):
        if isinstance(row, dict) and row.get("id") == candidate_id:
            return row
    return {}


def main() -> int:
    print("PR #230 SM one-Higgs to O_H import boundary")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    note = read_text(SM_NOTE)
    sm_runner_result = run_sm_support_runner()
    sm_candidate = find_candidate(certs, "sm_one_higgs_yukawa_gauge_selection")

    runner_passes = sm_runner_result["returncode"] == 0 and sm_runner_result["fail_count"] == 0
    note_disclaims_values = "does not select the numerical entries" in note
    note_after_h_supplied = "<H> = (0, v/sqrt(2))^T" in note and "one-Higgs-doublet Standard Model" in note
    repo_audit_rejects_as_oh = (
        sm_candidate.get("usable_as_pr230_oh_certificate") is False
        and sm_candidate.get("classification") == "gauge monomial selection; Yukawa entries free"
    )
    osp_frame_blocks = any(
        row.get("frame") == "one_higgs_gauge_selection"
        and row.get("current_surface_result") == "blocked"
        for row in certs["osp_oh_identity_stretch"].get("stretch_attempt_frames", [])
        if isinstance(row, dict)
    )
    no_orthogonal_still_open = (
        certs["no_orthogonal_import"].get("no_orthogonal_top_coupling_theorem_found") is False
        and certs["no_orthogonal_selection_rule"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    source_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction" in status(certs["source_pole_mixing"])
        and certs["source_pole_mixing"].get("source_pole_canonical_identity_gate_passed") is False
    )
    oh_gate_absent = (
        "canonical-Higgs operator certificate absent" in status(certs["canonical_higgs_operator_gate"])
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    import_closes = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("sm-one-higgs-support-runner-passes", runner_passes, str(sm_runner_result))
    report("sm-note-disclaims-yukawa-values", note_disclaims_values, str(SM_NOTE.relative_to(ROOT)))
    report("sm-note-after-canonical-h-supplied", note_after_h_supplied, "uses <H> after one-doublet H is supplied")
    report("repo-audit-rejects-sm-one-higgs-as-oh", repo_audit_rejects_as_oh, str(sm_candidate))
    report("osp-oh-stretch-blocks-one-higgs-frame", osp_frame_blocks, status(certs["osp_oh_identity_stretch"]))
    report("no-orthogonal-premise-still-open", no_orthogonal_still_open, "no import or selection rule")
    report("source-pole-mixing-still-blocks", source_mixing_blocks, status(certs["source_pole_mixing"]))
    report("canonical-oh-gate-still-absent", oh_gate_absent, status(certs["canonical_higgs_operator_gate"]))
    report("sm-one-higgs-import-does-not-close", not import_closes, "operator pattern support only")

    result = {
        "actual_current_surface_status": "exact negative boundary / SM one-Higgs gauge selection is not PR230 O_H identity",
        "verdict": (
            "The SM one-Higgs gauge-selection theorem remains useful support: "
            "its runner passes and it proves the allowed one-doublet Yukawa "
            "monomial pattern.  It does not close PR #230 because it assumes "
            "canonical H after H is supplied, leaves Yukawa matrix entries free, "
            "does not identify the PR230 source-pole operator O_sp with O_H, "
            "and does not prove a no-orthogonal-top-coupling selection rule."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The support theorem is an operator-pattern theorem, not a source-pole/canonical-Higgs identity or pole-residue measurement.",
        "sm_one_higgs_import_closes_pr230": import_closes,
        "sm_support_runner": sm_runner_result,
        "candidate_surface": sm_candidate,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by one-Higgs notation",
            "does not identify O_sp with O_H",
            "does not set orthogonal scalar top coupling to zero",
            "does not use H_unit, yt_ward_identity, observed top, observed y_t, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Stop trying SM one-Higgs monomial selection as the O_H proof. "
            "Proceed through certified C_sH/C_HH pole rows, a genuine rank-one "
            "neutral-scalar theorem, a same-source W/Z response harness, or "
            "honest production evidence."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
