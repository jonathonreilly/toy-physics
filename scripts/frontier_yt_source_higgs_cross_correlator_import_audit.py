#!/usr/bin/env python3
"""
PR #230 source-Higgs cross-correlator import audit.

The source-pole purity gate names a possible positive observable: a pole
cross-correlator C_sH between the PR #230 scalar source and the canonical
Higgs radial operator.  This audit checks whether the current branch already
contains that operator/measurement authority.  It does not define C_sH by
fiat, because that would import the same source-to-Higgs bridge the route is
trying to prove.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_import_audit_2026-05-02.json"

PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
EW_HIGGS_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
SM_ONE_HIGGS_NOTE = ROOT / "docs" / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"

CERTS = {
    "source_pole_purity_gate": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "gauge_vev_source_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "scalar_renormalization_condition": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
    "effective_potential_hessian": "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json",
    "brst_nielsen_higgs_identity": "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json",
    "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 source-Higgs cross-correlator import audit")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    harness_text = read_text(PRODUCTION_HARNESS)
    ew_text = read_text(EW_HIGGS_NOTE)
    sm_text = read_text(SM_ONE_HIGGS_NOTE)

    harness_has_source_response = (
        "scalar_source_response_analysis" in harness_text
        and "scalar_two_point_lsz_analysis" in harness_text
    )
    harness_has_cross_observable = any(
        token in harness_text
        for token in (
            "source_higgs_cross",
            "C_sH",
            "canonical_higgs_operator",
            "higgs_radial_operator",
            "gauge_mass_response_analysis",
        )
    )
    ew_note_assumes_canonical_h = "|D_mu H|^2" in ew_text and "<H> = H_0" in ew_text
    ew_note_derives_source_operator = any(
        token in ew_text.lower()
        for token in (
            "source-higgs cross",
            "source-to-higgs",
            "kappa_s",
            "c_sh",
            "source operator overlap",
        )
    )
    sm_note_selects_monomials_not_operator = (
        "arbitrary complex" in sm_text
        and "does not select" in sm_text
        and "source" not in sm_text.lower()
    )

    purity_gate_blocks = (
        "source-pole purity cross-correlator gate not passed"
        in status(certs["source_pole_purity_gate"])
        and certs["source_pole_purity_gate"].get("source_pole_purity_gate_passed") is False
    )
    canonical_import_blocks = (
        "canonical scalar normalization import audit" in status(certs["canonical_scalar_import"])
        and certs["canonical_scalar_import"].get("proposal_allowed") is False
    )
    source_to_higgs_blocks = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    gauge_vev_blocks = (
        "gauge-VEV source-overlap no-go" in status(certs["gauge_vev_source_overlap"])
        and certs["gauge_vev_source_overlap"].get("proposal_allowed") is False
    )
    scalar_renorm_blocks = (
        "renormalization-condition source-overlap no-go"
        in status(certs["scalar_renormalization_condition"])
        and certs["scalar_renormalization_condition"].get("proposal_allowed") is False
    )
    hessian_blocks = (
        "effective-potential Hessian not source-overlap identity"
        in status(certs["effective_potential_hessian"])
        and certs["effective_potential_hessian"].get("proposal_allowed") is False
    )
    brst_blocks = (
        "BRST-Nielsen identities not Higgs-pole identity"
        in status(certs["brst_nielsen_higgs_identity"])
        and certs["brst_nielsen_higgs_identity"].get("proposal_allowed") is False
    )
    wz_manifest_not_evidence = (
        "same-source WZ gauge-mass response manifest"
        in status(certs["fh_gauge_mass_response_manifest"])
        and certs["fh_gauge_mass_response_manifest"].get("manifest_is_evidence") is False
    )

    cross_correlator_authority_found = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-pole-purity-gate-loaded", purity_gate_blocks, status(certs["source_pole_purity_gate"]))
    report("harness-has-source-response-not-cross", harness_has_source_response and not harness_has_cross_observable, "top/FH and C_ss support present; C_sH/WZ schema absent")
    report("ew-note-assumes-canonical-h", ew_note_assumes_canonical_h, str(EW_HIGGS_NOTE.relative_to(ROOT)))
    report("ew-note-does-not-derive-source-operator", not ew_note_derives_source_operator, "no source operator overlap theorem in EW note")
    report("sm-note-not-cross-correlator-authority", sm_note_selects_monomials_not_operator, str(SM_ONE_HIGGS_NOTE.relative_to(ROOT)))
    report("canonical-import-audit-still-blocks", canonical_import_blocks, status(certs["canonical_scalar_import"]))
    report("source-to-higgs-lsz-still-blocks", source_to_higgs_blocks, status(certs["source_to_higgs_lsz"]))
    report("gauge-vev-and-renorm-shortcuts-blocked", gauge_vev_blocks and scalar_renorm_blocks, "canonical v/Z_h do not fix source overlap")
    report("hessian-and-brst-shortcuts-blocked", hessian_blocks and brst_blocks, "radial curvature and gauge identities do not define C_sH")
    report("wz-manifest-not-cross-correlator-evidence", wz_manifest_not_evidence, status(certs["fh_gauge_mass_response_manifest"]))
    report("no-hidden-csh-authority-found", not cross_correlator_authority_found, "C_sH remains an open observable/theorem")

    result = {
        "actual_current_surface_status": "exact negative boundary / source-Higgs cross-correlator import audit",
        "verdict": (
            "No current PR #230 surface supplies a source-Higgs pole "
            "cross-correlator authority.  The production harness emits top "
            "source-response and same-source C_ss support, but has no C_sH, "
            "canonical-Higgs operator, or W/Z response schema.  Existing EW/SM "
            "Higgs notes start after a canonical H is supplied or select "
            "allowed monomials; they do not derive the PR source operator "
            "overlap.  Gauge-VEV, Z_h, Hessian, and BRST/Nielsen shortcuts are "
            "already blocked.  Thus C_sH is a valid future target, not a hidden "
            "current-surface closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No C_sH/canonical-Higgs source-operator authority or implementation exists on the current PR surface.",
        "source_higgs_cross_correlator_authority_found": cross_correlator_authority_found,
        "harness_has_cross_observable": harness_has_cross_observable,
        "parent_certificates": CERTS,
        "audited_surfaces": {
            "production_harness": str(PRODUCTION_HARNESS.relative_to(ROOT)),
            "ew_higgs_note": str(EW_HIGGS_NOTE.relative_to(ROOT)),
            "sm_one_higgs_note": str(SM_ONE_HIGGS_NOTE.relative_to(ROOT)),
        },
        "minimum_future_acceptance": [
            "define a canonical Higgs radial operator on the same source/ensemble surface",
            "emit C_sH pole cross-correlator rows with source-response and C_ss rows",
            "prove or measure the pole overlap needed for source-pole purity",
            "pass retained-route and campaign certificates without forbidden imports",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define canonical H by fiat",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, observed W/Z masses, alpha_LM, plaquette, or u0",
            "does not treat W/Z manifest support as C_sH evidence",
        ],
        "exact_next_action": (
            "Either implement the missing C_sH/WZ response measurement with a "
            "canonical-Higgs identity certificate, or pivot to another ranked "
            "route such as sector-overlap/purity theorem or seed-controlled "
            "FH/LSZ production processing."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
