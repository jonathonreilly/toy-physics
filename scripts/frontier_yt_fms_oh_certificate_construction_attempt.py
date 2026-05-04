#!/usr/bin/env python3
"""
PR #230 FMS-style O_H certificate construction attempt.

The literature bridge identified a plausible future route: construct a
same-surface gauge-invariant Higgs operator, then measure C_ss/C_sH/C_HH and
run a Gram-pole extraction.  This runner checks whether that construction can
be made from the current PR230 surface without importing external authority or
assuming O_sp = O_H.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fms_oh_certificate_construction_attempt_2026-05-04.json"

PARENTS = {
    "literature_bridge": "outputs/yt_osp_oh_literature_bridge_2026-05-04.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_operator_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_repo_authority": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "same_source_ew_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "sm_one_higgs_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

TEXTS = {
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
    "ew_higgs_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "cl3_sm_embedding": "docs/CL3_SM_EMBEDDING_MASTER_NOTE.md",
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


def main() -> int:
    print("PR #230 FMS-style O_H certificate construction attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    texts = {name: read_rel(path) for name, path in TEXTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    harness = texts["production_harness"]
    ew_note = texts["ew_higgs_gauge_mass"]
    minimal = texts["minimal_axioms"]
    cl3_sm = texts["cl3_sm_embedding"]

    literature_source_ids = [
        str(row.get("id", ""))
        for row in parents["literature_bridge"].get("source_rows", [])
        if isinstance(row, dict)
    ]
    fms_shape_loaded = (
        "O_sp/O_H literature bridge" in status(parents["literature_bridge"])
        and parents["literature_bridge"].get("literature_bridge_passed") is True
        and any(source_id.startswith("fms") for source_id in literature_source_ids)
        and "gauge-invariant canonical-Higgs operator" in str(
            parents["literature_bridge"].get("methodology_shape", "")
        )
    )
    source_higgs_shell_present = all(
        token in harness
        for token in (
            "--source-higgs-operator-certificate",
            "source_higgs_operator_weights",
            "stochastic_source_higgs_cross_correlator",
            "C_ss/C_sH/C_HH",
        )
    )
    source_higgs_shell_is_default_off = (
        "source_higgs_cross_correlator=disabled" in harness
        and "--source-higgs-operator-certificate is required" in harness
    )
    qcd_top_harness_present = (
        "SU(3) Wilson gauge" in harness
        and "staggered" in harness
        and "--masses" in harness
    )
    dynamic_ew_higgs_action_in_harness = all(
        token in harness
        for token in (
            "SU(2)xU(1)",
            "Higgs doublet",
            "hypercharge",
            "W_mu",
            "B_mu",
        )
    )
    minimal_axioms_are_qcd_substrate = (
        "g_bare = 1" in minimal
        and "staggered" in minimal
        and "SU(2)xU(1)" not in minimal
    )
    cl3_sm_is_structural = (
        "SU(2)" in cl3_sm
        and "tensor product" in cl3_sm
        and "production action" not in cl3_sm
    )
    ew_note_after_h_supplied = (
        "Assume a neutral Higgs vacuum" in ew_note
        and "Higgs doublet" in ew_note
        and "M_W^2 = g^2 v^2 / 4" in ew_note
    )
    same_source_ew_action_absent = (
        "same-source EW action not defined" in status(parents["same_source_ew_action"])
        and parents["same_source_ew_action"].get("same_source_ew_action_ready") is False
    )
    oh_candidate_absent = (
        "canonical-Higgs operator certificate absent" in status(parents["canonical_operator_gate"])
        and parents["canonical_operator_gate"].get("candidate_present") is False
        and parents["canonical_operator_gate"].get("candidate_valid") is False
    )
    oh_realization_open = (
        "canonical-Higgs operator realization gate not passed"
        in status(parents["canonical_operator_realization"])
        and parents["canonical_operator_realization"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
    )
    repo_hidden_oh_absent = (
        parents["canonical_repo_authority"].get("repo_authority_found") is False
        and "repo-wide canonical-Higgs" in status(parents["canonical_repo_authority"])
    )
    source_higgs_launch_blocked = (
        "source-Higgs production launch blocked" in status(parents["source_higgs_readiness"])
        and parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and parents["source_higgs_readiness"].get("operator_certificate_present") is False
    )
    sm_one_higgs_not_import = (
        "SM one-Higgs gauge selection is not PR230 O_H identity"
        in status(parents["sm_one_higgs_boundary"])
        and parents["sm_one_higgs_boundary"].get("sm_one_higgs_import_closes_pr230") is False
    )
    retained_route_open = "retained closure not yet reached" in status(parents["retained_route"])

    requirements = {
        "same_surface_ew_gauge_higgs_action": not same_source_ew_action_absent,
        "dynamic_higgs_doublet_in_current_harness": dynamic_ew_higgs_action_in_harness,
        "gauge_invariant_composite_oh_definition": not oh_candidate_absent,
        "canonical_identity_and_normalization_certificate": not oh_realization_open,
        "production_csh_chh_rows": not source_higgs_launch_blocked,
        "sm_one_higgs_allowed_as_identity_import": not sm_one_higgs_not_import,
    }
    missing_requirements = [key for key, ok in requirements.items() if not ok]
    fms_oh_certificate_available = not missing_parents and not missing_texts and not missing_requirements

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-literature-shape-loaded", fms_shape_loaded, status(parents["literature_bridge"]))
    report("qcd-top-harness-present", qcd_top_harness_present, "production harness is the SU(3)/staggered top route")
    report("source-higgs-shell-present", source_higgs_shell_present, "default-off C_ss/C_sH/C_HH instrumentation exists")
    report("source-higgs-shell-default-off", source_higgs_shell_is_default_off, "requires operator certificate")
    report("no-dynamic-ew-higgs-action-in-harness", not dynamic_ew_higgs_action_in_harness, "no SU(2)xU(1) Higgs doublet production action")
    report("minimal-axioms-do-not-supply-ew-higgs-action", minimal_axioms_are_qcd_substrate, "minimal substrate is not an EW gauge-Higgs production action")
    report("cl3-sm-embedding-is-structural", cl3_sm_is_structural, "structural gauge support is not O_H production")
    report("ew-note-assumes-h-after-supplied", ew_note_after_h_supplied, "static tree dictionary only")
    report("same-source-ew-action-absent", same_source_ew_action_absent, status(parents["same_source_ew_action"]))
    report("canonical-oh-candidate-absent", oh_candidate_absent, status(parents["canonical_operator_gate"]))
    report("canonical-oh-realization-still-open", oh_realization_open, status(parents["canonical_operator_realization"]))
    report("repo-hidden-oh-absent", repo_hidden_oh_absent, status(parents["canonical_repo_authority"]))
    report("source-higgs-launch-blocked", source_higgs_launch_blocked, status(parents["source_higgs_readiness"]))
    report("sm-one-higgs-not-oh-import", sm_one_higgs_not_import, status(parents["sm_one_higgs_boundary"]))
    report("retained-route-still-open", retained_route_open, status(parents["retained_route"]))
    report("fms-oh-certificate-not-available", not fms_oh_certificate_available, f"missing_requirements={missing_requirements}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / FMS O_H certificate construction blocked on current PR230 surface"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface has a default-off source-Higgs measurement "
            "shell and FMS/GEVP methodology context, but it lacks a same-surface "
            "EW gauge-Higgs production action, a dynamic Higgs doublet field, "
            "a gauge-invariant O_H identity/normalization certificate, and "
            "production C_sH/C_HH pole rows."
        ),
        "bare_retained_allowed": False,
        "fms_oh_certificate_available": fms_oh_certificate_available,
        "fms_construction_attempt_passed_as_boundary": not fms_oh_certificate_available and FAIL_COUNT == 0,
        "requirements": requirements,
        "missing_requirements": missing_requirements,
        "current_surface_classification": {
            "production_harness": "SU(3) Wilson/staggered top harness with default-off source-Higgs diagonal-vertex shell",
            "ew_higgs_gauge_mass_note": "tree-level dictionary after canonical H is supplied",
            "minimal_axioms": "Cl(3)/Z3 + g_bare=1 + staggered-Dirac substrate, not an EW gauge-Higgs action",
            "cl3_sm_embedding": "structural SU(2)/hypercharge support, not a production O_H certificate",
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import FMS literature as proof of O_sp = O_H",
            "does not define O_H by one-Higgs notation, H_unit, or a diagonal vertex shell",
            "does not treat static EW gauge-mass algebra as a same-surface Higgs operator",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1, cos(theta) = 1, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "A positive FMS route needs a new same-surface EW gauge-Higgs "
            "action/certificate for a gauge-invariant O_H operator, followed "
            "by production C_ss/C_sH/C_HH rows and GEVP or isolated-pole Gram "
            "residue extraction.  Without that new surface, continue the "
            "current production chunks or pursue W/Z/Schur/rank-one alternatives."
        ),
        "parent_certificates": PARENTS,
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
