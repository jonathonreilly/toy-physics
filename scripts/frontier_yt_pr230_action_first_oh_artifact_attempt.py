#!/usr/bin/env python3
"""
PR #230 action-first O_H artifact construction attempt.

The fresh route review selected the O_H/C_sH/C_HH contract as the cleanest
physics target.  This runner tests the next necessary premise: can the current
PR230 Cl(3)/Z3 surface produce the same-source EW/Higgs action and canonical
O_H certificate, rather than merely writing down a standard EW/Higgs action as
a new hypothetical surface?

It does not write the future O_H certificate or the future same-source EW
action certificate.  It records the current-surface blocker and the exact
artifact that would have to land next.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json"

PARENTS = {
    "fresh_artifact_review": "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "fms_oh_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "canonical_oh_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

TEXTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "native_gauge": "docs/NATIVE_GAUGE_CLOSURE_NOTE.md",
    "ew_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
}

FUTURE_ARTIFACTS = {
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def current_surface_candidate(texts: dict[str, str]) -> dict[str, Any]:
    return {
        "id": "current_cl3_z3_structural_surfaces",
        "candidate_kind": "reuse_existing_structural_notes",
        "inputs": TEXTS,
        "passes_same_source_ew_action": False,
        "passes_canonical_oh": False,
        "blockers": [
            {
                "id": "minimal_axioms_are_qcd_staggered_surface",
                "evidence": (
                    "staggered-Dirac partition" in texts["minimal_axioms"]
                    and "graph-first structural `SU(3)`" in texts["minimal_axioms"]
                ),
                "why": "does not define a dynamic SU(2)xU(1) Higgs doublet action with the top scalar source coordinate",
            },
            {
                "id": "native_gauge_is_structural",
                "evidence": (
                    "exact native cubic `Cl(3)` / `SU(2)` algebra" in texts["native_gauge"]
                    and "downstream phenomenology remains separate" in texts["native_gauge"]
                ),
                "why": "gauge algebra/charge structure is not an EW/Higgs production action",
            },
            {
                "id": "ew_gauge_mass_assumes_H",
                "evidence": (
                    "Assume a neutral Higgs vacuum" in texts["ew_gauge_mass"]
                    and "standard covariant derivative" in texts["ew_gauge_mass"]
                ),
                "why": "tree-level mass diagonalization starts after canonical H is supplied",
            },
            {
                "id": "sm_one_higgs_leaves_yukawas_free",
                "evidence": "does not select the numerical entries" in texts["sm_one_higgs"],
                "why": "operator-pattern selection does not identify PR230 scalar source with O_H",
            },
            {
                "id": "production_harness_qcd_top_only",
                "evidence": (
                    "Cl3Z3_SU3_Wilson_staggered" in texts["production_harness"]
                    and "smoke_schema_enabled_not_ew_production" in texts["production_harness"]
                ),
                "why": "W/Z rows are guarded as absent or synthetic smoke, not production EW fields",
            },
        ],
    }


def hypothetical_action_surface() -> dict[str, Any]:
    return {
        "id": "standard_ew_higgs_action_written_by_definition",
        "candidate_kind": "hypothetical_new_surface",
        "self_consistent_action_terms": [
            "SU(2)_L Wilson gauge action",
            "U(1)_Y gauge action",
            "gauge-covariant Higgs doublet kinetic term",
            "Higgs potential",
            "source term s coupled to chosen radial Higgs coordinate",
        ],
        "why_not_current_artifact": (
            "Writing these terms defines an additional EW/Higgs theory surface. "
            "It does not derive the same source coordinate, canonical O_H, or "
            "source-Higgs pole overlap from the retained PR230 Cl(3)/Z3 top "
            "FH/LSZ surface."
        ),
        "would_require_before_pr230_use": [
            "derivation or accepted new-surface certificate tying the EW/Higgs action to Cl(3)/Z3",
            "same-source coordinate identity between top dE/ds and Higgs/WZ response",
            "canonical O_H identity and pole-normalization certificate",
            "production C_ss/C_sH/C_HH or W/Z rows",
            "aggregate retained-route and campaign gates",
        ],
        "actual_current_surface_status": "hypothetical only / not current-surface authority",
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_u0_or_rconn": False,
        "set_kappa_s_equal_one": False,
        "set_g2_by_convention": False,
        "wrote_future_action_certificate": False,
        "wrote_canonical_oh_certificate": False,
        "wrote_source_higgs_rows": False,
    }


def main() -> int:
    print("PR #230 action-first O_H artifact construction attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    texts = {name: read_rel(path) for name, path in TEXTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    current_candidate = current_surface_candidate(texts)
    hypothetical_candidate = hypothetical_action_surface()
    firewall = forbidden_firewall()

    fresh_review_selects_oh = (
        parents["fresh_artifact_review"].get("review_passed") is True
        and parents["fresh_artifact_review"].get("selected_genuine_artifact_contract", {}).get(
            "contract"
        )
        == "O_H/C_sH/C_HH source-Higgs pole rows"
    )
    same_source_action_absent = (
        parents["same_source_ew_action_builder"].get("input_present") is False
        and parents["same_source_ew_action_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
        and parents["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and not future_present["same_source_ew_action_certificate"]
    )
    fms_attempt_blocks_current_surface = (
        parents["fms_oh_attempt"].get("fms_oh_certificate_available") is False
        and parents["fms_oh_attempt"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        parents["canonical_oh_gate"].get("candidate_present") is False
        and parents["canonical_oh_gate"].get("candidate_valid") is False
        and not future_present["canonical_oh_certificate"]
    )
    source_higgs_rows_absent = (
        parents["source_higgs_readiness"].get("future_rows_present") is False
        and not future_present["source_higgs_rows"]
    )
    gram_purity_open = (
        parents["source_higgs_gram_gate"].get("source_higgs_gram_purity_gate_passed")
        is False
    )
    sector_overlap_open = (
        parents["same_source_sector_overlap"].get("sector_overlap_identity_gate_passed")
        is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    current_candidate_blocked = all(
        blocker["evidence"] for blocker in current_candidate["blockers"]
    )
    hypothetical_not_current = (
        hypothetical_candidate["actual_current_surface_status"]
        == "hypothetical only / not current-surface authority"
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fresh-review-selects-oh-contract", fresh_review_selects_oh, statuses["fresh_artifact_review"])
    report("same-source-ew-action-certificate-absent", same_source_action_absent, statuses["same_source_ew_action_builder"])
    report("fms-oh-current-surface-blocked", fms_attempt_blocks_current_surface, statuses["fms_oh_attempt"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, FUTURE_ARTIFACTS["canonical_oh_certificate"])
    report("source-higgs-row-artifact-absent", source_higgs_rows_absent, FUTURE_ARTIFACTS["source_higgs_rows"])
    report("source-higgs-gram-purity-open", gram_purity_open, statuses["source_higgs_gram_gate"])
    report("sector-overlap-open", sector_overlap_open, statuses["same_source_sector_overlap"])
    report("current-structural-candidate-blocked", current_candidate_blocked, "existing notes are structural/static/harness-only")
    report("hypothetical-ew-action-not-current-surface", hypothetical_not_current, hypothetical_candidate["why_not_current_artifact"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and fresh_review_selects_oh
        and same_source_action_absent
        and fms_attempt_blocks_current_surface
        and canonical_oh_absent
        and source_higgs_rows_absent
        and gram_purity_open
        and sector_overlap_open
        and current_candidate_blocked
        and hypothetical_not_current
        and retained_open
        and campaign_open
        and no_forbidden_imports
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / action-first O_H artifact not constructible from current PR230 surface"
        ),
        "conditional_surface_status": (
            "A future block can reopen this route only with a same-source EW/Higgs "
            "action certificate derived on the PR230 surface, a canonical O_H "
            "identity/normalization certificate, and production C_ss/C_sH/C_HH rows."
        ),
        "hypothetical_axiom_status": (
            "A standard EW/Higgs action can be written as a hypothetical new "
            "surface, but it is not current-surface PR230 proof authority."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The selected O_H/C_sH/C_HH contract still lacks its first two "
            "current-surface artifacts: same-source EW/Higgs action authority "
            "and canonical O_H identity/normalization."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "same_source_ew_action_certificate_written": False,
        "canonical_oh_certificate_written": False,
        "source_higgs_rows_written": False,
        "future_artifact_presence": future_present,
        "current_surface_candidate": current_candidate,
        "hypothetical_action_surface": hypothetical_candidate,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write the future same-source EW action certificate",
            "does not write the future canonical O_H certificate",
            "does not write source-Higgs pole rows",
            "does not treat a hypothetical standard EW action as a current-surface derivation",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, R_conn, kappa_s=1, or g2 by convention",
        ],
        "exact_next_action": (
            "The next positive artifact must be a derivation/certificate tying "
            "a same-source EW/Higgs action to the PR230 Cl(3)/Z3 surface, or a "
            "canonical O_H identity/normalization theorem that bypasses the "
            "action step.  Without that, pivot to a different listed artifact "
            "contract rather than source-only shortcuts."
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
