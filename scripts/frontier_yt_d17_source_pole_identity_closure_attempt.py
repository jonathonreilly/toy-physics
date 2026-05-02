#!/usr/bin/env python3
"""
PR #230 D17 source-pole identity closure attempt.

This runner tests whether the D17 single-scalar uniqueness surface can be
upgraded into the missing source-pole-to-canonical-Higgs identity or source
residue theorem.  It separates carrier uniqueness from LSZ pole normalization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_d17_source_pole_identity_closure_attempt_2026-05-02.json"

TEXT_AUTHORITIES = {
    "ward_identity_theorem": "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md",
    "class3_susy_2hdm_note": "docs/YT_CLASS_3_SUSY_2HDM_ANALYSIS_NOTE_2026-04-18.md",
}

CERTS = {
    "d17_no_orthogonal_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "cl3_source_unit": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
    "scalar_renormalization_condition_overlap": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
    "scalar_source_contact_term_scheme": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
    "same_source_two_point": "outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json",
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


def read_text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def single_carrier_residue_family() -> list[dict[str, float | bool]]:
    rows: list[dict[str, float | bool]] = []
    canonical_y = 1.0
    for source_overlap in (0.6, 1.0, 1.4):
        rows.append(
            {
                "d17_q_l_scalar_singlet_dimension": 1.0,
                "second_retained_scalar_present": False,
                "canonical_higgs_pole_residue": 1.0,
                "canonical_yukawa_y_h": canonical_y,
                "source_operator_overlap_z_s": source_overlap,
                "source_two_point_pole_residue": source_overlap * source_overlap,
                "source_response_slope_dE_ds": canonical_y * source_overlap,
                "identity_assumption_z_s_equals_one": source_overlap == 1.0,
            }
        )
    return rows


def main() -> int:
    print("PR #230 D17 source-pole identity closure attempt")
    print("=" * 72)

    texts = {name: read_text(path) for name, path in TEXT_AUTHORITIES.items()}
    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    authority_text = "\n".join(texts.values()).lower()
    d17_uniqueness_support = (
        "d17" in authority_text
        and "unique" in authority_text
        and "(1,1)" in authority_text
        and "single composite" in authority_text
    )
    no_second_scalar_support = (
        "no second scalar" in authority_text or "not support 2hdm" in authority_text
    )

    d17_import_is_not_purity = (
        "no-orthogonal-top-coupling import audit" in status(certs["d17_no_orthogonal_import"])
        and certs["d17_no_orthogonal_import"].get("no_orthogonal_top_coupling_theorem_found") is False
    )
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(certs["fh_lsz_higgs_pole_identity"])
        and certs["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    source_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in status(certs["source_pole_canonical_higgs_mixing"])
        and certs["source_pole_canonical_higgs_mixing"].get("source_pole_canonical_identity_gate_passed")
        is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    source_unit_not_metric = (
        "source-unit normalization no-go" in status(certs["cl3_source_unit"])
        and certs["cl3_source_unit"].get("proposal_allowed") is False
    )
    renorm_contact_shortcuts_blocked = (
        "renormalization-condition source-overlap no-go"
        in status(certs["scalar_renormalization_condition_overlap"])
        and "source contact-term scheme boundary" in status(certs["scalar_source_contact_term_scheme"])
        and certs["scalar_renormalization_condition_overlap"].get("proposal_allowed") is False
        and certs["scalar_source_contact_term_scheme"].get("proposal_allowed") is False
    )
    same_source_two_point_support = (
        "same-source scalar two-point" in status(certs["same_source_two_point"])
        and certs["same_source_two_point"].get("proposal_allowed") is False
    )

    rows = single_carrier_residue_family()
    fixed_carrier_facts = {
        (
            row["d17_q_l_scalar_singlet_dimension"],
            row["second_retained_scalar_present"],
            row["canonical_higgs_pole_residue"],
            row["canonical_yukawa_y_h"],
        )
        for row in rows
    }
    source_residues = {round(float(row["source_two_point_pole_residue"]), 12) for row in rows}
    source_slopes = {round(float(row["source_response_slope_dE_ds"]), 12) for row in rows}

    missing_identity_requirements = [
        "isolated source pole proved to be the canonical Higgs radial mode",
        "source operator overlap <0|O_s|h> or D'(pole) derived from the substrate",
        "source coordinate metric tied to the canonical kinetic normalization used by v",
        "contact and renormalization conventions shown not to move the pole residue",
        "orthogonal/multiparticle spectral weight excluded or measured",
    ]
    theorem_closed = False

    report("text-authorities-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("d17-single-carrier-support-present", d17_uniqueness_support, "D17 unique (1,1) support loaded")
    report("no-second-scalar-support-present", no_second_scalar_support, "no retained 2HDM/second scalar support loaded")
    report("d17-import-not-pole-purity", d17_import_is_not_purity, status(certs["d17_no_orthogonal_import"]))
    report("higgs-identity-gate-still-blocked", higgs_identity_blocked, status(certs["fh_lsz_higgs_pole_identity"]))
    report("source-mixing-obstruction-still-blocks", source_mixing_blocks, status(certs["source_pole_canonical_higgs_mixing"]))
    report("source-to-higgs-lsz-still-blocked", source_to_higgs_blocked, status(certs["source_to_higgs_lsz"]))
    report("source-unit-not-canonical-metric", source_unit_not_metric, status(certs["cl3_source_unit"]))
    report("renorm-and-contact-shortcuts-blocked", renorm_contact_shortcuts_blocked, "canonical Z_h/contact schemes do not fix <0|O_s|h>")
    report("same-source-two-point-only-support", same_source_two_point_support, status(certs["same_source_two_point"]))
    report("single-carrier-family-keeps-d17-facts-fixed", len(fixed_carrier_facts) == 1, f"fixed_facts={fixed_carrier_facts}")
    report("source-residue-varies-without-changing-carrier", len(source_residues) == len(rows), f"source_residues={sorted(source_residues)}")
    report("source-response-varies-without-changing-carrier", len(source_slopes) == len(rows), f"source_slopes={sorted(source_slopes)}")
    report("d17-source-pole-identity-not-closed", not theorem_closed, "D17 carrier uniqueness is not an LSZ residue theorem")
    report("does-not-authorize-retained-proposal", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": "open / D17 source-pole identity closure attempt blocked",
        "verdict": (
            "D17 single-scalar uniqueness and no-retained-2HDM support are useful "
            "carrier constraints, but they do not derive the LSZ source-pole "
            "identity needed by PR #230.  Carrier uniqueness does not fix the "
            "source operator overlap, source two-point pole residue, inverse "
            "propagator derivative, or canonical kinetic metric used by v.  The "
            "route therefore remains blocked unless a new theorem derives those "
            "objects, or production data measure them with a separate pole-identity "
            "acceptance gate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "D17 fixes a carrier/irrep uniqueness statement, not the source-pole LSZ residue or canonical-Higgs identity.",
        "theorem_closed": theorem_closed,
        "parent_certificates": CERTS,
        "text_authorities": TEXT_AUTHORITIES,
        "single_carrier_residue_family": rows,
        "missing_identity_requirements": missing_identity_requirements,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, W/Z, or Higgs values as proof selectors",
            "does not use alpha_LM, plaquette, u0, c2 = 1, Z_match = 1, or kappa_s = 1",
            "does not promote D17 carrier uniqueness into source-pole LSZ normalization",
        ],
        "exact_next_action": (
            "Either derive the missing source overlap / D'(pole) theorem from the "
            "scalar denominator, or wait for seed-controlled FH/LSZ chunks and "
            "measure same-source pole residue under the model-class/FV/IR/Higgs "
            "identity gates."
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
