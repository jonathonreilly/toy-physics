#!/usr/bin/env python3
"""
PR #230 FH/LSZ canonical-Higgs pole identity gate.

The same-source FH/LSZ invariant readout cancels arbitrary scalar-source
rescalings, but it does not by itself prove that the measured scalar pole is
the canonical Higgs radial mode whose normalization defines v.  This runner
turns that remaining requirement into an executable claim gate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json"

CERTS = {
    "invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
    "same_source_two_point": "outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json",
    "pole_fit_postprocessor": "outputs/yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "gauge_vev_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "scalar_renorm_overlap": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
    "contact_term_scheme": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
    "scalar_denominator": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "kprime": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
}

EW_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"

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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 FH/LSZ canonical-Higgs pole identity gate")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    ew_text = EW_NOTE.read_text(encoding="utf-8") if EW_NOTE.exists() else ""
    ew_assumes_canonical_h = "|D_mu H|^2" in ew_text and "<H> = H_0" in ew_text
    ew_omits_source_bridge = "source-to" not in ew_text.lower() and "kappa" not in ew_text.lower()

    invariant_support = (
        "invariant readout" in status(certs["invariant_readout"])
        and certs["invariant_readout"].get("proposal_allowed") is False
    )
    same_source_measurement_support = (
        "same-source scalar two-point" in status(certs["same_source_two_point"])
        and certs["same_source_two_point"].get("proposal_allowed") is False
    )
    pole_fit_absent = (
        "postprocessor scaffold" in status(certs["pole_fit_postprocessor"])
        and certs["pole_fit_postprocessor"].get("readiness", {}).get("fit_ready") is False
    )
    source_bridge_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    canonical_import_blocked = (
        "canonical scalar normalization import audit" in status(certs["canonical_scalar_import"])
        and certs["canonical_scalar_import"].get("proposal_allowed") is False
    )
    gauge_vev_not_identity = (
        "no-go" in status(certs["gauge_vev_overlap"]).lower()
        and certs["gauge_vev_overlap"].get("proposal_allowed") is False
    )
    renorm_not_identity = (
        "no-go" in status(certs["scalar_renorm_overlap"]).lower()
        and certs["scalar_renorm_overlap"].get("proposal_allowed") is False
    )
    contact_not_identity = (
        "scheme" in status(certs["contact_term_scheme"]).lower()
        and certs["contact_term_scheme"].get("proposal_allowed") is False
    )
    denominator_not_identity = (
        "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator"])
        and certs["scalar_denominator"].get("proposal_allowed") is False
    )
    kprime_not_identity = (
        "K-prime closure attempt blocked" in status(certs["kprime"])
        and certs["kprime"].get("proposal_allowed") is False
    )

    gate_requirements = [
        {
            "requirement": "same-source invariant response formula",
            "current_status": "available support",
            "satisfied": invariant_support,
            "certificate": CERTS["invariant_readout"],
        },
        {
            "requirement": "same-source scalar two-point observable",
            "current_status": "available measurement primitive",
            "satisfied": same_source_measurement_support,
            "certificate": CERTS["same_source_two_point"],
        },
        {
            "requirement": "production pole fit and dGamma_ss/dp^2",
            "current_status": "absent/nonready",
            "satisfied": False,
            "certificate": CERTS["pole_fit_postprocessor"],
        },
        {
            "requirement": "identity of measured source pole with canonical Higgs radial mode",
            "current_status": "blocked",
            "satisfied": False,
            "certificate": CERTS["source_to_higgs_lsz"],
        },
        {
            "requirement": "canonical Higgs kinetic normalization derived from source functional",
            "current_status": "blocked",
            "satisfied": False,
            "certificate": CERTS["canonical_scalar_import"],
        },
        {
            "requirement": "no replacement by gauge-VEV, renormalization-condition, or contact-scheme shortcut",
            "current_status": "shortcuts blocked",
            "satisfied": gauge_vev_not_identity and renorm_not_identity and contact_not_identity,
            "certificate": (
                f"{CERTS['gauge_vev_overlap']}; "
                f"{CERTS['scalar_renorm_overlap']}; "
                f"{CERTS['contact_term_scheme']}"
            ),
        },
        {
            "requirement": "interacting denominator derivative and pole saturation",
            "current_status": "blocked",
            "satisfied": False,
            "certificate": f"{CERTS['scalar_denominator']}; {CERTS['kprime']}",
        },
    ]

    gate_passed = (
        not missing
        and not proposal_allowed
        and all(row["satisfied"] for row in gate_requirements)
        and ew_assumes_canonical_h
        and not ew_omits_source_bridge
    )

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-source-invariant-support-present", invariant_support, CERTS["invariant_readout"])
    report("same-source-two-point-primitive-present", same_source_measurement_support, CERTS["same_source_two_point"])
    report("production-pole-fit-still-absent", pole_fit_absent, CERTS["pole_fit_postprocessor"])
    report("ew-note-assumes-canonical-h", ew_assumes_canonical_h, str(EW_NOTE.relative_to(ROOT)))
    report("ew-note-does-not-supply-source-bridge", ew_omits_source_bridge, "canonical H is a post-bridge input")
    report("source-to-higgs-identity-still-blocked", source_bridge_blocked and canonical_import_blocked, "source bridge remains open")
    report("shortcut-identifications-still-blocked", gauge_vev_not_identity and renorm_not_identity and contact_not_identity, "VEV/renorm/contact shortcuts blocked")
    report("denominator-and-kprime-still-blocked", denominator_not_identity and kprime_not_identity, "pole derivative stack remains open")
    report("higgs-pole-identity-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / FH-LSZ canonical-Higgs pole identity gate blocking",
        "verdict": (
            "The same-source FH/LSZ invariant readout removes the need to set "
            "kappa_s = 1, but it does not by itself identify the measured "
            "source pole with the canonical Higgs radial mode whose kinetic "
            "normalization defines v.  Existing EW/Higgs algebra starts after "
            "the canonical doublet has been supplied, and the source-to-Higgs, "
            "gauge-VEV overlap, renormalization-condition, contact-scheme, "
            "denominator, and K'(pole) certificates do not close that identity. "
            "The physical y_t gate therefore remains open even for future "
            "same-source response data until the Higgs-pole identity and pole "
            "derivative are certified."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The canonical-Higgs pole identity and production pole derivative are not certified.",
        "higgs_pole_identity_gate_passed": gate_passed,
        "parent_certificates": CERTS,
        "ew_note": str(EW_NOTE.relative_to(ROOT)),
        "ew_surface": {
            "assumes_canonical_h": ew_assumes_canonical_h,
            "supplies_source_bridge": not ew_omits_source_bridge,
        },
        "gate_requirements": gate_requirements,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not treat same-source invariance as canonical-Higgs identity",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
            "does not set c2 or Z_match to one",
        ],
        "exact_next_action": (
            "Either derive the source-pole-to-canonical-Higgs identity together "
            "with D'(pole), or obtain production FH/LSZ pole data plus an "
            "independent current-surface certificate that the measured pole is "
            "the canonical Higgs radial mode used by v."
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
