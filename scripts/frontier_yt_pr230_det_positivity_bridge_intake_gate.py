#!/usr/bin/env python3
"""
PR #230 determinant-positivity bridge intake gate.

origin/main now contains a staggered+Wilson determinant-positivity bridge.
This runner checks whether that adjacent positive theorem changes PR #230's
source-to-canonical-Higgs blocker.

Verdict expected: useful positivity-preservation support, not y_t closure.
The PR230 bridge requires positivity improvement / primitive neutral transfer
or same-surface source-Higgs rows; determinant positivity alone is compatible
with reducible neutral scalar sectors.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json"

CANDIDATE_NOTE = "docs/STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md"
CANDIDATE_RUNNER = "scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py"

PARENTS = {
    "derived_bridge_rank_one": "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json",
    "neutral_primitive_cone": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_positivity_direct": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
    "source_sector_transfer": "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def read_candidate(rel: str) -> tuple[str, str]:
    path = ROOT / rel
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace"), "local"
    proc = subprocess.run(
        ["git", "show", f"origin/main:{rel}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout, "origin/main"
    return "", f"missing ({proc.stderr.strip()})"


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def positive_vs_primitive_counterexample() -> dict[str, Any]:
    return {
        "euclidean_measure_positive": True,
        "fermion_determinant_positive": True,
        "neutral_transfer_matrix": [[0.94, 0.0], [0.0, 0.91]],
        "neutral_transfer_nonnegative": True,
        "neutral_transfer_strongly_connected": False,
        "primitive_power_strictly_positive": False,
        "source_only_rows_can_match": True,
        "orthogonal_neutral_scalar_survives": True,
        "lesson": (
            "Configuration-by-configuration determinant positivity is compatible "
            "with a reducible positive neutral scalar response sector."
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_det_positivity_as_yukawa_value": False,
        "uses_det_positivity_as_canonical_oh_identity": False,
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_or_yukawa_targets": False,
        "sets_source_higgs_overlap_to_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 determinant-positivity bridge intake gate")
    print("=" * 72)

    note_text, note_source = read_candidate(CANDIDATE_NOTE)
    runner_text, runner_source = read_candidate(CANDIDATE_RUNNER)
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    candidate_present = (
        "det(M) > 0" in note_text
        and "configuration-by-configuration" in note_text
        and "M_W = r" in note_text
        and "prod_{i=1..n/2}" in runner_text
    )
    candidate_scope_narrow = (
        "symmetric-canonical" in note_text
        and "M_W = r" in note_text
        and "independent audit lane only" in note_text
    )
    derived_rank_one_still_blocks = (
        parents["derived_bridge_rank_one"].get("proposal_allowed") is False
        and parents["derived_bridge_rank_one"].get("derived_bridge_closure_passed")
        is False
        and parents["derived_bridge_rank_one"].get("exact_negative_boundary_passed")
        is True
    )
    primitive_cone_absent = (
        parents["neutral_primitive_cone"].get("primitive_cone_certificate_gate_passed")
        is False
        and parents["neutral_primitive_cone"].get("proposal_allowed") is False
    )
    direct_positivity_not_improvement = (
        parents["neutral_positivity_direct"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
        and parents["neutral_positivity_direct"].get("exact_negative_boundary_passed")
        is True
    )
    source_sector_not_closure = (
        parents["source_sector_transfer"].get("bounded_support_passed") is True
        and parents["source_sector_transfer"].get("direct_closure_available") is False
    )
    assembly_open = parents["full_positive_assembly"].get("proposal_allowed") is False
    retained_route_open = parents["retained_route"].get("proposal_allowed") is False
    counterexample_blocks = (
        positive_vs_primitive_counterexample()["fermion_determinant_positive"] is True
        and positive_vs_primitive_counterexample()["primitive_power_strictly_positive"]
        is False
        and positive_vs_primitive_counterexample()[
            "orthogonal_neutral_scalar_survives"
        ]
        is True
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    determinant_bridge_closes_pr230 = (
        candidate_present
        and not derived_rank_one_still_blocks
        and not primitive_cone_absent
        and not direct_positivity_not_improvement
        and clean_firewall
    )
    intake_gate_passed = (
        not missing_parents
        and not proposal_allowed
        and candidate_present
        and candidate_scope_narrow
        and derived_rank_one_still_blocks
        and primitive_cone_absent
        and direct_positivity_not_improvement
        and source_sector_not_closure
        and assembly_open
        and retained_route_open
        and counterexample_blocks
        and determinant_bridge_closes_pr230 is False
        and clean_firewall
    )

    report("candidate-note-readable", bool(note_text), note_source)
    report("candidate-runner-readable", bool(runner_text), runner_source)
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("candidate-det-positivity-present", candidate_present, "det(M)>0 bridge found")
    report("candidate-scope-narrow", candidate_scope_narrow, "symmetric-canonical / audit lane")
    report("derived-rank-one-still-blocks", derived_rank_one_still_blocks, statuses["derived_bridge_rank_one"])
    report("primitive-cone-absent", primitive_cone_absent, statuses["neutral_primitive_cone"])
    report("direct-positivity-is-not-improvement", direct_positivity_not_improvement, statuses["neutral_positivity_direct"])
    report("source-sector-transfer-not-closure", source_sector_not_closure, statuses["source_sector_transfer"])
    report("assembly-still-open", assembly_open, statuses["full_positive_assembly"])
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("counterexample-blocks-det-to-rank-one", counterexample_blocks, "positive determinant plus reducible neutral transfer")
    report("determinant-bridge-does-not-close-pr230", determinant_bridge_closes_pr230 is False, "missing primitive/O_H/rows")
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    result = {
        "actual_current_surface_status": (
            "bounded-support / staggered-Wilson determinant positivity is useful "
            "positivity-preservation support, not PR230 y_t closure"
        ),
        "conditional_surface_status": (
            "If supplemented by a same-surface theorem upgrading positivity "
            "preservation to primitive positivity improvement in the neutral "
            "scalar response sector, or by O_H/C_sH/C_HH rows, determinant "
            "positivity would be relevant support for the bridge."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The determinant bridge gives configuration-by-configuration "
            "positive fermion measure on a symmetric-canonical surface; it "
            "does not define canonical O_H, produce C_sH/C_HH rows, prove "
            "neutral primitive-cone irreducibility, or exclude orthogonal "
            "neutral scalar top coupling."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "candidate_note_source": note_source,
        "candidate_runner_source": runner_source,
        "candidate_present": candidate_present,
        "candidate_scope_narrow": candidate_scope_narrow,
        "determinant_bridge_closes_pr230": determinant_bridge_closes_pr230,
        "intake_gate_passed": intake_gate_passed,
        "positive_vs_primitive_counterexample": positive_vs_primitive_counterexample(),
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not use determinant positivity as y_t, O_H, or kappa_s",
            "does not use H_unit, yt_ward_identity, or observed targets",
            "does not treat positivity preservation as positivity improvement",
        ],
        "exact_next_action": (
            "Use determinant positivity only as measure/positivity-preservation "
            "support.  Continue PR230 through a real neutral primitive-cone "
            "certificate, canonical O_H plus C_sH/C_HH rows, same-source W/Z "
            "rows, or strict production FH/LSZ plus matching."
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
