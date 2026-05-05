#!/usr/bin/env python3
"""
PR #230 canonical O_H premise-lattice stretch no-go.

This is the cycle-3 deep-work block after the source-Higgs unratified-Gram
shortcut was closed.  It asks whether the current PR230 primitives can already
write the same-surface canonical O_H identity and normalization certificate
needed by the source-Higgs route.

The output is a proof/certificate artifact only.  It records the minimal
allowed premise set, the missing certificate obligations, an algebraic
non-data counterfamily, and a stuck fan-out to the next positive route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_oh_premise_stretch_no_go_2026-05-05.json"

PARENTS = {
    "canonical_oh_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_oh_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_oh_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "fms_oh_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_unratified_gram": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "cross_lane_oh_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "same_source_ew_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_response_contract": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "schur_rows": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "neutral_primitive": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "scalar_lsz_moment": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "scalar_lsz_bounds": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "nonchunk_worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "matched_wz_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "neutral_primitive_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "strict_scalar_lsz_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def minimal_allowed_premises() -> list[dict[str, str]]:
    return [
        {
            "id": "cl3_source_surface",
            "role": "defines the additive source side and source-pole functional",
            "class": "allowed structural premise",
        },
        {
            "id": "legendre_source_pole_normalization",
            "role": "normalizes the source-side pole operator only",
            "class": "exact support; not a canonical O_H identity",
        },
        {
            "id": "current_source_higgs_shell",
            "role": "future row instrumentation shape",
            "class": "default-off support; not operator authority",
        },
        {
            "id": "current_ew_structural_notes",
            "role": "static and structural context after canonical H is supplied",
            "class": "context/support; not a PR230 production operator",
        },
        {
            "id": "current_route_gates",
            "role": "firewalls and absence checks for source-Higgs, W/Z, Schur, neutral, and scalar-LSZ routes",
            "class": "negative/support boundaries",
        },
    ]


def certificate_obligations(
    certs: dict[str, dict[str, Any]], future_present: dict[str, bool]
) -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_state_space",
            "required": "an accepted PR230 state/action surface containing the source operator and canonical O_H",
            "current_satisfied": certs["same_source_ew_action"].get("same_source_ew_action_ready") is True,
            "blocking_statuses": [
                status(certs["same_source_ew_action"]),
                status(certs["fms_oh_attempt"]),
            ],
        },
        {
            "id": "canonical_operator_definition",
            "required": "a current-surface canonical O_H definition, not notation or adjacent-lane context",
            "current_satisfied": certs["canonical_oh_gate"].get("candidate_valid") is True,
            "blocking_statuses": [
                status(certs["canonical_oh_gate"]),
                status(certs["cross_lane_oh_audit"]),
            ],
        },
        {
            "id": "identity_certificate",
            "required": "a proof or row certificate identifying the source-pole direction with canonical O_H",
            "current_satisfied": future_present["canonical_oh_certificate"],
            "blocking_statuses": [
                status(certs["canonical_oh_realization"]),
                status(certs["source_higgs_unratified_gram"]),
            ],
        },
        {
            "id": "normalization_certificate",
            "required": "same-surface pole/field normalization with no admitted convention",
            "current_satisfied": certs["canonical_oh_realization"].get(
                "canonical_higgs_operator_realization_gate_passed"
            )
            is True,
            "blocking_statuses": [status(certs["canonical_oh_realization"])],
        },
        {
            "id": "independent_overlap_evidence",
            "required": "one accepted overlap route: source-Higgs rows, W/Z rows, Schur rows, or neutral primitive theorem",
            "current_satisfied": any(
                [
                    future_present["source_higgs_rows"],
                    future_present["matched_wz_rows"],
                    future_present["schur_kernel_rows"],
                    future_present["neutral_primitive_certificate"],
                ]
            ),
            "blocking_statuses": [
                status(certs["source_higgs_readiness"]),
                status(certs["wz_response_contract"]),
                status(certs["schur_rows"]),
                status(certs["neutral_primitive"]),
            ],
        },
        {
            "id": "scalar_lsz_and_assembly_gate",
            "required": "positive physical-readout assembly after scalar-LSZ and overlap gates both pass",
            "current_satisfied": certs["assembly"].get("current_evaluation", {}).get("assembly_passed")
            is True,
            "blocking_statuses": [
                status(certs["scalar_lsz_moment"]),
                status(certs["scalar_lsz_bounds"]),
                status(certs["assembly"]),
            ],
        },
    ]


def algebraic_counterfamily() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, overlap in (
        ("identity_case", 1.0),
        ("mixed_case", 0.8),
        ("wide_mixed_case", 0.6),
        ("orthogonal_case", 0.0),
    ):
        orthogonal = math.sqrt(max(0.0, 1.0 - overlap * overlap))
        rows.append(
            {
                "case": label,
                "source_pole_norm": 1.0,
                "candidate_oh_norm": 1.0,
                "source_to_candidate_overlap": overlap,
                "orthogonal_component_norm": orthogonal,
                "current_allowed_premises_distinguish_case": False,
                "future_source_higgs_gram_determinant": 1.0 - overlap * overlap,
                "distinguished_by_future_non_source_row_or_theorem": overlap != 1.0,
            }
        )
    return rows


def stuck_fanout(certs: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "frame": "source_higgs_identity",
            "status": "blocked",
            "wall": status(certs["source_higgs_readiness"]),
            "next": "new same-surface O_H certificate before rows",
        },
        {
            "frame": "same_source_wz_response",
            "status": "best_next_positive_route",
            "wall": status(certs["same_source_ew_action"]),
            "next": "derive the same-source EW action/row authority or a closed covariance theorem",
        },
        {
            "frame": "schur_kernel_rows",
            "status": "blocked",
            "wall": status(certs["schur_rows"]),
            "next": "supply same-surface A/B/C kernel rows",
        },
        {
            "frame": "neutral_primitive_cone",
            "status": "blocked",
            "wall": status(certs["neutral_primitive"]),
            "next": "prove primitive-cone irreducibility for the neutral scalar sector",
        },
        {
            "frame": "scalar_lsz_control",
            "status": "independent_open_gate",
            "wall": status(certs["scalar_lsz_moment"]),
            "next": "supply strict moment/threshold/FV authority before physical readout",
        },
    ]


def main() -> int:
    print("PR #230 canonical O_H premise-lattice stretch no-go")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_present = {name: exists(path) for name, path in FUTURE_FILES.items()}
    premises = minimal_allowed_premises()
    obligations = certificate_obligations(certs, future_present)
    missing_obligations = [row["id"] for row in obligations if not row["current_satisfied"]]
    counterfamily = algebraic_counterfamily()
    fanout = stuck_fanout(certs)

    overlaps = [float(row["source_to_candidate_overlap"]) for row in counterfamily]
    source_norms = [float(row["source_pole_norm"]) for row in counterfamily]
    candidate_norms = [float(row["candidate_oh_norm"]) for row in counterfamily]
    determinants = [float(row["future_source_higgs_gram_determinant"]) for row in counterfamily]
    all_future_files_absent = not any(future_present.values())
    all_parent_fails_zero = all(int(cert.get("fail_count", 0)) == 0 for cert in certs.values())
    all_obligations_missing = len(missing_obligations) == len(obligations)
    source_norm_fixed = max(source_norms) - min(source_norms) < 1.0e-12
    candidate_norm_fixed = max(candidate_norms) - min(candidate_norms) < 1.0e-12
    overlap_varies = max(overlaps) - min(overlaps) > 0.9
    future_rows_distinguish = any(det > 1.0e-12 for det in determinants)
    fanout_has_next_route = any(row["status"] == "best_next_positive_route" for row in fanout)

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-runners-have-no-fails", all_parent_fails_zero, "loaded certificates have FAIL=0")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("minimal-premise-set-recorded", len(premises) == 5, f"count={len(premises)}")
    report("same-source-ew-action-still-absent", not certs["same_source_ew_action"].get("same_source_ew_action_ready"), status(certs["same_source_ew_action"]))
    report("canonical-oh-candidate-still-absent", certs["canonical_oh_gate"].get("candidate_valid") is False, status(certs["canonical_oh_gate"]))
    report("canonical-oh-realization-still-open", certs["canonical_oh_realization"].get("canonical_higgs_operator_realization_gate_passed") is False, status(certs["canonical_oh_realization"]))
    report("source-higgs-launch-still-blocked", certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False, status(certs["source_higgs_readiness"]))
    report("unratified-gram-shortcut-already-closed", certs["source_higgs_unratified_gram"].get("unratified_gram_shortcut_no_go_passed") is True, status(certs["source_higgs_unratified_gram"]))
    report("strict-future-files-absent", all_future_files_absent, f"present={future_present}")
    report("certificate-obligations-all-missing", all_obligations_missing, f"missing={missing_obligations}")
    report("counterfamily-source-norm-fixed", source_norm_fixed, f"source_norms={source_norms}")
    report("counterfamily-candidate-norm-fixed", candidate_norm_fixed, f"candidate_norms={candidate_norms}")
    report("counterfamily-overlap-varies", overlap_varies, f"overlaps={overlaps}")
    report("future-row-would-distinguish-counterfamily", future_rows_distinguish, f"determinants={determinants}")
    report("stuck-fanout-records-next-positive-route", fanout_has_next_route, str(fanout))
    report("retained-proposal-not-authorized", not proposal_allowed, "same-surface certificate obligations remain open")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / same-surface O_H identity and normalization "
            "certificate not derivable from current PR230 primitives"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface O_H certificate plus "
            "overlap row, W/Z response route, Schur row route, or neutral primitive "
            "theorem lands and the aggregate gates pass"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface has source-side normalization and several "
            "support/absence gates, but no accepted same-surface state/action "
            "surface, canonical O_H definition, identity proof, normalization "
            "certificate, or independent overlap row/theorem."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "premise_lattice_stretch_no_go_passed": FAIL_COUNT == 0,
        "minimal_allowed_premises": premises,
        "certificate_obligations": obligations,
        "missing_obligation_ids": missing_obligations,
        "strict_future_file_presence": future_present,
        "algebraic_non_data_counterfamily": counterfamily,
        "stuck_fanout": fanout,
        "selected_next_nonchunk_route": {
            "id": "same_source_wz_response",
            "reason": (
                "It is the best positive pivot after the source-Higgs O_H "
                "certificate remains blocked: a physical response row or a "
                "closed covariance theorem could bypass source-Higgs operator "
                "identity, while Schur, neutral, and scalar-LSZ routes currently "
                "lack their strict same-surface inputs."
            ),
            "first_action": (
                "Try to derive the same-source EW action/row authority or a "
                "closed top/W covariance theorem; otherwise keep it as the next "
                "measurement-row target."
            ),
        },
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not package or certify chunk outputs",
            "does not introduce empirical data",
            "does not define O_H by notation, adjacent-lane context, or row purity against an unratified operator",
            "does not use user-listed shortcut authorities",
        ],
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
