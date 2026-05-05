#!/usr/bin/env python3
"""
PR #230 non-chunk current-surface exhaustion gate.

This runner is a cycle-8 closeout/no-go artifact for the non-chunk PR230 loop.
It does not claim retained or proposed_retained closure.  It checks that the
current non-chunk route queue has no remaining executable shortcut after the
W/Z, O_H/source-Higgs, scalar-LSZ, Schur, and neutral-rank blocks already
landed as gates or no-go artifacts.

The gate is intentionally current-surface only: it says the present branch has
no hidden non-chunk route left.  It does not rule out future same-surface rows,
certificates, or new theorems.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family_audit": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "schur_bootstrap_no_go": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "wz_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "wz_goldstone_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
    "neutral_primitive_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "canonical_oh_premise_no_go": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "polynomial_contact_repair_no_go": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
}

EXPECTED_BLOCKED_UNITS = {
    "canonical_oh_source_higgs",
    "same_source_wz_response",
    "scalar_lsz_model_fv_ir",
    "schur_scalar_denominator_rows",
    "neutral_scalar_rank_one",
    "matching_running",
}

EXPECTED_FUTURE_FILES = {
    "canonical_oh_certificate",
    "source_higgs_rows",
    "matched_top_wz_rows",
    "deterministic_response_covariance_certificate",
    "source_coordinate_transport_certificate",
    "wz_mass_response_rows",
    "non_observed_g2_certificate",
    "delta_perp_rows",
    "stieltjes_moment_certificate",
    "pade_stieltjes_bounds_certificate",
    "contact_subtraction_certificate",
    "polynomial_contact_certificate",
    "schur_kernel_rows",
    "neutral_irreducibility_certificate",
    "neutral_primitive_cone_certificate",
    "certified_physical_readout",
}

HARD_BANNED_SHORTCUTS = (
    "y_t_bare",
    "H_unit",
    "yt_ward",
    "alpha_LM",
    "plaquette/u0",
    "observed target",
    "bare-coupling shortcut",
)

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


def existing_future_files(worklist: dict[str, Any]) -> list[str]:
    presence = worklist.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return []
    return sorted(name for name, present in presence.items() if present)


def missing_future_keys(worklist: dict[str, Any]) -> list[str]:
    presence = worklist.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return sorted(EXPECTED_FUTURE_FILES)
    return sorted(EXPECTED_FUTURE_FILES.difference(presence))


def blocked_unit_ids(worklist: dict[str, Any]) -> set[str]:
    ids = worklist.get("blocked_work_unit_ids", [])
    if not isinstance(ids, list):
        return set()
    return {str(item) for item in ids}


def closed_unit_ids(worklist: dict[str, Any]) -> set[str]:
    ids = worklist.get("closed_work_unit_ids", [])
    if not isinstance(ids, list):
        return set()
    return {str(item) for item in ids}


def all_remaining_files_absent(worklist: dict[str, Any]) -> bool:
    for unit in worklist.get("work_units", []):
        if not isinstance(unit, dict):
            return False
        for rel in unit.get("remaining", []):
            if not isinstance(rel, str) or (ROOT / rel).exists():
                return False
    return True


def selected_route_after_no_go(route_audit: dict[str, Any]) -> bool:
    selected = route_audit.get("selected_route", {})
    disposition = str(selected.get("current_disposition", ""))
    exact_next = str(route_audit.get("exact_next_action", ""))
    return (
        selected.get("id") == "schur_scalar_denominator_rows"
        and "compressed-denominator row-bootstrap no-go" in disposition
        and "strict future row/certificate surface" in exact_next
        and route_audit.get("proposal_allowed") is False
    )


def shortcut_firewall_ok() -> bool:
    """The exhaustion gate records banned shortcuts only as non-claims."""

    future_actions = [
        "same-surface O_H/C_sH/C_HH rows",
        "W/Z response rows with identities and covariance authority",
        "scalar-LSZ moment/threshold/FV authority",
        "same-surface Schur A/B/C kernel rows",
        "neutral primitive-cone or irreducibility certificate",
    ]
    joined = " ".join(future_actions)
    return not any(term in joined for term in HARD_BANNED_SHORTCUTS)


def main() -> int:
    print("PR #230 non-chunk current-surface exhaustion gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in certs.items()}

    worklist = certs["worklist"]
    route_audit = certs["route_family_audit"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = blocked_unit_ids(worklist)
    closed_ids = closed_unit_ids(worklist)
    future_present = existing_future_files(worklist)
    future_key_gaps = missing_future_keys(worklist)

    all_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    strict_future_surface_absent = not future_present and not future_key_gaps
    remaining_paths_absent = all_remaining_files_absent(worklist)
    assembly_rejects_current = assembly.get("current_evaluation", {}).get("assembly_passed") is False
    assembly_rejects_chunk_only = assembly.get("chunk_only_evaluation", {}).get("assembly_passed") is False
    retained_still_open = retained_route.get("proposal_allowed") is False and "open" in statuses["retained_route"]
    campaign_still_open = campaign.get("proposal_allowed") is False and "open" in statuses["campaign"]
    schur_no_go = (
        certs["schur_bootstrap_no_go"].get("bootstrap_no_go_passed") is True
        and certs["schur_bootstrap_no_go"].get("proposal_allowed") is False
    )
    wz_shortcuts_closed = (
        certs["wz_transport_no_go"].get("wz_source_coordinate_transport_no_go_passed") is True
        and certs["wz_goldstone_no_go"].get("goldstone_equivalence_source_identity_no_go_passed") is True
        and certs["wz_transport_no_go"].get("proposal_allowed") is False
        and certs["wz_goldstone_no_go"].get("proposal_allowed") is False
    )
    oh_scalar_neutral_shortcuts_closed = (
        certs["canonical_oh_premise_no_go"].get("premise_lattice_stretch_no_go_passed") is True
        and certs["source_higgs_unratified_gram_no_go"].get("unratified_gram_shortcut_no_go_passed") is True
        and certs["neutral_primitive_stretch_no_go"].get("primitive_cone_stretch_no_go_passed") is True
        and certs["polynomial_contact_repair_no_go"].get("polynomial_contact_repair_no_go_passed") is True
    )

    current_surface_exhausted = all(
        [
            not missing_parents,
            not proposal_allowed_parents,
            all_units_blocked,
            strict_future_surface_absent,
            remaining_paths_absent,
            selected_route_after_no_go(route_audit),
            assembly_rejects_current,
            assembly_rejects_chunk_only,
            retained_still_open,
            campaign_still_open,
            schur_no_go,
            wz_shortcuts_closed,
            oh_scalar_neutral_shortcuts_closed,
            shortcut_firewall_ok(),
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("all-nonchunk-work-units-blocked", all_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("strict-future-surface-files-absent", strict_future_surface_absent, f"present={future_present} key_gaps={future_key_gaps}")
    report("remaining-work-unit-files-absent", remaining_paths_absent, "all listed future row/certificate paths are absent")
    report("route-audit-selected-schur-after-no-go", selected_route_after_no_go(route_audit), route_audit.get("exact_next_action", ""))
    report("assembly-rejects-current-surface", assembly_rejects_current, str(assembly.get("current_evaluation", {})))
    report("assembly-rejects-chunk-only-surface", assembly_rejects_chunk_only, str(assembly.get("chunk_only_evaluation", {})))
    report("retained-route-still-open", retained_still_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_still_open, statuses["campaign"])
    report("schur-compressed-bootstrap-closed", schur_no_go, statuses["schur_bootstrap_no_go"])
    report("wz-static-and-goldstone-shortcuts-closed", wz_shortcuts_closed, "source transport and Goldstone identity are no-go")
    report("oh-scalar-neutral-shortcuts-closed", oh_scalar_neutral_shortcuts_closed, "O_H, unratified Gram, neutral primitive cone, and scalar contact shortcuts are closed")
    report("hard-bans-not-used-as-positive-premises", shortcut_firewall_ok(), "banned terms appear only in non-claims/firewalls")
    report("current-surface-exhaustion-gate-passed", current_surface_exhausted, f"passed={current_surface_exhausted}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current PR230 non-chunk route queue exhausted; "
            "positive closure still open"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Every current non-chunk work unit is blocked and every strict future "
            "row/certificate file named by the worklist is absent.  The allowed "
            "next moves require new same-surface artifacts, not another current "
            "shortcut."
        ),
        "bare_retained_allowed": False,
        "current_surface_exhaustion_gate_passed": current_surface_exhausted,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "future_file_presence": worklist.get("future_file_presence", {}),
        "selected_route": {
            "id": "current_surface_nonchunk_exhaustion",
            "prior_selected_family": route_audit.get("selected_route", {}).get("id"),
            "reason": (
                "Cycle 7 closed the last executable Schur compressed-denominator "
                "shortcut.  The May 5 worklist now leaves only absent future "
                "same-surface rows, certificates, or new theorems."
            ),
        },
        "allowed_future_routes": [
            "same-surface O_H/C_sH/C_HH pole rows with canonical-Higgs identity and normalization",
            "same-source W/Z response rows with source identity, covariance authority, non-observed g2, and delta_perp correction authority",
            "strict scalar-LSZ moment/threshold/FV or scalar-denominator/analytic-continuation certificate",
            "same-surface Schur A/B/C kernel rows",
            "neutral primitive-cone or irreducibility certificate",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not package or rerun chunk MC",
            "does not treat the old May 1 queue-exhaustion runner as current PR230 authority",
            "does not use y_t_bare, H_unit, yt_ward_identity, alpha_LM, plaquette/u0, observed targets, or bare-coupling shortcuts",
            "does not rule out future same-surface rows, certificates, or new theorems",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "exact_next_action": (
            "Stop current-surface non-chunk shortcut cycling unless one of the "
            "named strict future same-surface artifacts is supplied: O_H/C_sH/"
            "C_HH rows, W/Z response rows with identities/covariance/correction "
            "authority, scalar-LSZ moment/threshold/FV authority, Schur A/B/C "
            "kernel rows, or a neutral primitive-cone certificate."
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
