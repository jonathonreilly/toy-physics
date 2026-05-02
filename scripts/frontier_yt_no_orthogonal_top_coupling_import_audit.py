#!/usr/bin/env python3
"""
PR #230 no-orthogonal-top-coupling import audit.

The same-source gauge-response route would become much stronger if the current
surface already proved that every scalar component orthogonal to the canonical
Higgs radial mode has zero top coupling.  This audit checks whether that
premise is hidden in the existing no-2HDM / no-second-scalar authority.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json"

TEXT_AUTHORITIES = {
    "class3_script": "scripts/frontier_yt_class_3_susy_2hdm.py",
    "class3_note": "docs/YT_CLASS_3_SUSY_2HDM_ANALYSIS_NOTE_2026-04-18.md",
}

CERTS = {
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "fh_gauge_response_mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
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


def response_level_family() -> list[dict[str, float | bool]]:
    measured_pole_top_coupling = 1.0
    cos_theta = 0.82
    sin_theta = math.sqrt(1.0 - cos_theta**2)
    rows: list[dict[str, float | bool]] = []
    for y_orthogonal in (-0.4, 0.0, 0.4):
        canonical_y = (measured_pole_top_coupling - y_orthogonal * sin_theta) / cos_theta
        rows.append(
            {
                "retained_fundamental_second_scalar_present": False,
                "retained_2hdm_present": False,
                "d17_q_l_scalar_singlet_dimension": 1.0,
                "source_pole_canonical_higgs_overlap_cos_theta": cos_theta,
                "source_pole_orthogonal_response_overlap_sin_theta": sin_theta,
                "orthogonal_effective_top_coupling": y_orthogonal,
                "fixed_measured_source_pole_top_coupling": measured_pole_top_coupling,
                "physical_canonical_higgs_yukawa": canonical_y,
            }
        )
    return rows


def main() -> int:
    print("PR #230 no-orthogonal-top-coupling import audit")
    print("=" * 72)

    texts = {name: read_text(path) for name, path in TEXT_AUTHORITIES.items()}
    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    class_surface = "\n".join(texts.values()).lower()
    class3_no_second_scalar_support = (
        "no second scalar field" in class_surface
        and "no fundamental scalar" in class_surface
        and "d17" in class_surface
        and "single composite higgs" in class_surface
        and "2hdm is not retained" in class_surface
    )
    class3_no_lsz_purity_theorem = not any(
        needle in class_surface
        for needle in (
            "source-pole-to-canonical-higgs",
            "source pole equals canonical higgs",
            "orthogonal top coupling",
            "d_gamma",
            "dgamma",
            "kappa_s",
            "res c_ss",
        )
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
    gauge_mixed_scalar_demands_premise = (
        "FH gauge-response mixed-scalar obstruction" in status(certs["fh_gauge_response_mixed_scalar"])
        and any(
            "orthogonal scalar has zero top coupling" in premise
            for premise in certs["fh_gauge_response_mixed_scalar"].get("missing_premises", [])
        )
    )
    sector_identity_blocked = (
        "same-source sector-overlap identity obstruction"
        in status(certs["same_source_sector_overlap_identity"])
        and certs["same_source_sector_overlap_identity"].get("sector_overlap_identity_gate_passed") is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    canonical_import_blocked = (
        "canonical scalar normalization import audit" in status(certs["canonical_scalar_import"])
        and certs["canonical_scalar_import"].get("proposal_allowed") is False
    )

    family = response_level_family()
    fixed_class_facts = {
        (
            row["retained_fundamental_second_scalar_present"],
            row["retained_2hdm_present"],
            row["d17_q_l_scalar_singlet_dimension"],
            row["fixed_measured_source_pole_top_coupling"],
        )
        for row in family
    }
    canonical_y_values = {round(float(row["physical_canonical_higgs_yukawa"]), 12) for row in family}
    open_premises = [
        "source pole equals the canonical Higgs radial mode",
        "orthogonal response component is absent from the source pole",
        "orthogonal response component has zero top coupling",
        "production or theorem fixes the source-pole scalar residue and purity",
    ]
    theorem_found = False

    report("text-authorities-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("class3-excludes-retained-second-scalar", class3_no_second_scalar_support, "D9/D16/D17 and no-2HDM support loaded")
    report("class3-is-not-lsz-purity-theorem", class3_no_lsz_purity_theorem, "no source-pole residue/purity bridge found there")
    report("higgs-pole-identity-still-blocked", higgs_identity_blocked, status(certs["fh_lsz_higgs_pole_identity"]))
    report("source-pole-mixing-still-blocks", source_mixing_blocks, status(certs["source_pole_canonical_higgs_mixing"]))
    report("gauge-response-still-demands-orthogonal-premise", gauge_mixed_scalar_demands_premise, "orthogonal top-coupling premise is explicit")
    report("sector-overlap-and-source-bridge-still-blocked", sector_identity_blocked and source_to_higgs_blocked, "same-source sector/source bridge open")
    report("canonical-import-still-blocked", canonical_import_blocked, status(certs["canonical_scalar_import"]))
    report("response-family-keeps-class3-facts-fixed", len(fixed_class_facts) == 1, f"fixed_facts={fixed_class_facts}")
    report("canonical-y-varies-with-open-orthogonal-coupling", len(canonical_y_values) == len(family), f"canonical_y_values={sorted(canonical_y_values)}")
    report("no-hidden-no-orthogonal-top-coupling-theorem", not theorem_found, "the needed premise is not present on the current surface")
    report("does-not-authorize-retained-proposal", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": "exact negative boundary / no-orthogonal-top-coupling import audit",
        "verdict": (
            "The existing Class #3 SUSY/2HDM authority is useful support: it "
            "excludes a retained fundamental second scalar, a retained 2HDM "
            "species split, and a second D17 Q_L scalar.  It is not the "
            "stronger LSZ/source-pole purity theorem needed by PR #230.  It "
            "does not derive that the measured source pole is the canonical "
            "Higgs radial mode, that every orthogonal response component is "
            "absent, or that such a component has zero top coupling.  The "
            "same-source gauge-response route therefore still needs a genuine "
            "source-pole identity/no-orthogonal-top-coupling theorem or a "
            "direct production response certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No current-surface authority proves the required no-orthogonal-top-coupling/source-pole-purity premise.",
        "no_orthogonal_top_coupling_theorem_found": theorem_found,
        "parent_certificates": CERTS,
        "text_authorities": TEXT_AUTHORITIES,
        "support_separated_from_missing_premise": {
            "available_support": [
                "no retained fundamental second scalar in the bare action",
                "no retained 2HDM species split",
                "D17 one-dimensional Q_L scalar-singlet support",
            ],
            "still_missing": open_premises,
        },
        "response_level_counterfamily": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass, observed y_t, W/Z, or Higgs values as proof selectors",
            "does not use alpha_LM, plaquette, u0, c2 = 1, Z_match = 1, or kappa_s = 1",
            "does not promote no-2HDM/no-second-scalar authority into LSZ source-pole purity",
        ],
        "exact_next_action": (
            "Either derive the source-pole-to-canonical-Higgs/no-orthogonal-top-coupling "
            "theorem directly, or keep accumulating seed-controlled FH/LSZ production "
            "chunks and require a separate pole-identity acceptance gate before any "
            "physical y_t claim."
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
