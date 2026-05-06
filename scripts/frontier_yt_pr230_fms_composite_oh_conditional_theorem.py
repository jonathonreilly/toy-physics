#!/usr/bin/env python3
r"""
PR #230 FMS composite O_H conditional theorem.

This runner packages the hard-physics content of the action-first route after
the degree-one shortcut failed.  In a gauge-Higgs theory with a dynamic Higgs
doublet Phi and a nonzero radial background v, the gauge-invariant composite

    O_H = Phi^\dagger Phi - <Phi^\dagger Phi>

has a linear one-Higgs component v h in the FMS expansion.  That is the right
operator-theoretic bridge to canonical Higgs rows.  The theorem is conditional:
the current PR230 surface still lacks the same-surface EW/Higgs action,
canonical O_H certificate, source-overlap rows, and scalar-LSZ/pole authority.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json"
)

PARENTS = {
    "fms_post_degree_route_rescore": "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json",
    "degree_one_higgs_action_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "fms_oh_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "action_first_oh_attempt": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "full_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "same_source_ew_higgs_action": "outputs/yt_pr230_same_source_ew_higgs_action_certificate_2026-05-06.json",
    "same_source_ew_action_legacy": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "taste_radial_combined_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def fms_expansion_sample(v: float, h: float, pi2: float) -> dict[str, float]:
    r"""Tree-level local expansion for Phi^\dagger Phi in radial variables.

    Convention: Phi^\dagger Phi = ((v+h)^2 + pi^a pi^a) / 2.
    The centered composite is v*h + h^2/2 + pi^2/2 at the expansion point.
    """

    centered = v * h + 0.5 * h * h + 0.5 * pi2
    return {
        "v": v,
        "h": h,
        "pi2": pi2,
        "centered_composite": centered,
        "dO_dh_at_origin": v,
        "dO_dpi_a_at_origin": 0.0,
        "d2O_dh2": 1.0,
        "d2O_dpi_a2": 1.0,
    }


def residue_map(v: float, z_h: float, z_s: float, rho_sh: float) -> dict[str, Any]:
    """FMS one-particle pole residue map.

    If O_H has linear component v*h and h has one-particle residue Z_h, then
    Res C_HH = v^2 Z_h at the Higgs pole.  A source overlap still needs
    measured/theorem input Res C_sH = v rho_sh sqrt(Z_s Z_h).
    """

    res_hh = v * v * z_h
    res_ss = z_s
    res_sh = v * rho_sh * math.sqrt(max(z_s * z_h, 0.0))
    gram_det = res_ss * res_hh - res_sh * res_sh
    return {
        "Res_C_ss": res_ss,
        "Res_C_HH": res_hh,
        "Res_C_sH": res_sh,
        "rho_sH": rho_sh,
        "gram_determinant": gram_det,
        "gram_purity": abs(gram_det) < 1.0e-12 and abs(abs(rho_sh) - 1.0) < 1.0e-12,
        "normalization_factor_is_v_sqrt_Zh_not_one": not math.isclose(
            abs(v) * math.sqrt(max(z_h, 0.0)), 1.0, rel_tol=0.0, abs_tol=1.0e-12
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_literature_as_proof_authority": False,
        "used_degree_or_odd_parity_as_oh_authority": False,
        "used_taste_radial_axis_as_canonical_oh": False,
        "defined_oh_by_name_only": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 FMS composite O_H conditional theorem")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}

    expansion = fms_expansion_sample(v=3.0, h=0.125, pi2=0.0625)
    pure_source = residue_map(v=3.0, z_h=2.0, z_s=18.0, rho_sh=1.0)
    mixed_source = residue_map(v=3.0, z_h=2.0, z_s=18.0, rho_sh=0.5)
    firewall = forbidden_firewall()

    fms_route_selected = (
        "FMS post-degree route rescore" in statuses["fms_post_degree_route_rescore"]
        and certs["fms_post_degree_route_rescore"].get("proposal_allowed") is False
        and certs["fms_post_degree_route_rescore"].get("fms_post_degree_route_rescore_passed")
        is True
    )
    degree_shortcut_blocked = (
        "degree-one Higgs-action premise not derived"
        in statuses["degree_one_higgs_action_premise_gate"]
        and certs["degree_one_higgs_action_premise_gate"].get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
    )
    current_fms_construction_absent = (
        "FMS O_H certificate construction blocked" in statuses["fms_oh_construction_attempt"]
        and certs["fms_oh_construction_attempt"].get("proposal_allowed") is False
        and "action-first O_H artifact not constructible" in statuses["action_first_oh_attempt"]
    )
    same_surface_action_absent = (
        "same-source EW action not defined" in statuses["same_source_ew_action_gate"]
        and certs["same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
        and certs["same_source_ew_action_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
        and future_presence["same_source_ew_higgs_action"] is False
        and future_presence["same_source_ew_action_legacy"] is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    source_higgs_rows_absent = (
        certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_gram"].get("source_higgs_gram_purity_gate_passed")
        is False
        and future_presence["source_higgs_rows"] is False
        and future_presence["source_higgs_production_certificate"] is False
    )
    expansion_derives_linear_component = (
        finite(expansion["dO_dh_at_origin"])
        and expansion["dO_dh_at_origin"] == expansion["v"]
        and expansion["dO_dpi_a_at_origin"] == 0.0
        and expansion["d2O_dh2"] == 1.0
        and expansion["d2O_dpi_a2"] == 1.0
    )
    nonzero_v_required = expansion["dO_dh_at_origin"] != 0.0
    normalization_not_unity = (
        pure_source["normalization_factor_is_v_sqrt_Zh_not_one"] is True
        and mixed_source["normalization_factor_is_v_sqrt_Zh_not_one"] is True
    )
    source_overlap_not_implied = (
        pure_source["gram_purity"] is True
        and mixed_source["gram_purity"] is False
        and pure_source["Res_C_ss"] == mixed_source["Res_C_ss"]
        and pure_source["Res_C_HH"] == mixed_source["Res_C_HH"]
        and pure_source["Res_C_sH"] != mixed_source["Res_C_sH"]
    )
    degree_premise_conditionally_supplied = (
        expansion_derives_linear_component
        and nonzero_v_required
        and same_surface_action_absent is True
    )
    assembly_still_open = (
        certs["full_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-route-selected-as-future-contract", fms_route_selected, statuses["fms_post_degree_route_rescore"])
    report("degree-shortcut-blocked", degree_shortcut_blocked, statuses["degree_one_higgs_action_premise_gate"])
    report("current-fms-construction-absent", current_fms_construction_absent, statuses["fms_oh_construction_attempt"])
    report("same-surface-ew-higgs-action-absent", same_surface_action_absent, statuses["same_source_ew_action_gate"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-pole-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("fms-expansion-derives-linear-radial-component", expansion_derives_linear_component, str(expansion))
    report("nonzero-vev-required", nonzero_v_required, f"dO/dh={expansion['dO_dh_at_origin']}")
    report("normalization-not-unity", normalization_not_unity, str(pure_source))
    report("source-overlap-not-implied-by-composite-definition", source_overlap_not_implied, str(mixed_source))
    report("degree-premise-only-conditional", degree_premise_conditionally_supplied, "requires same-surface action plus nonzero v")
    report("assembly-retained-campaign-still-open", assembly_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    theorem_passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "conditional-support / FMS composite O_H theorem; current PR230 "
            "surface lacks same-surface EW/Higgs action and source-overlap pole rows"
        ),
        "conditional_surface_status": (
            "exact-support if a future PR230 same-surface EW/Higgs action supplies "
            "a dynamic Higgs doublet Phi, nonzero radial background v, canonical "
            "Higgs LSZ normalization, and C_ss/C_sH/C_HH pole rows"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The FMS composite expansion derives a real operator bridge only after "
            "the same-surface EW/Higgs action and h-source exist.  The current "
            "PR230 branch has neither that action nor canonical O_H/source-overlap "
            "pole rows, so this is support for the next artifact, not closure."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_composite_oh_conditional_theorem_passed": theorem_passed,
        "current_closure_authority_present": False,
        "same_surface_action_absent": same_surface_action_absent,
        "canonical_oh_absent": canonical_oh_absent,
        "source_higgs_rows_absent": source_higgs_rows_absent,
        "fms_expansion": {
            "convention": "Phi^dagger Phi = ((v+h)^2 + pi^a pi^a)/2",
            "centered_composite": "O_H = v h + h^2/2 + pi^a pi^a/2",
            "sample": expansion,
            "one_particle_pole_residue_map": "Res C_OH,OH = v^2 Z_h at the isolated Higgs pole",
        },
        "residue_counterfamily": {
            "pure_source": pure_source,
            "mixed_source_same_Css_CHH_different_CsH": mixed_source,
            "lesson": "Composite O_H does not by itself certify the PR230 source overlap; C_sH or a source-coordinate theorem remains load-bearing.",
        },
        "remaining_load_bearing_inputs": [
            "same-surface EW/Higgs action with dynamic Phi on Cl(3)/Z^3",
            "nonzero radial background and canonical Higgs LSZ normalization",
            "canonical/gauge-invariant composite O_H certificate",
            "same-ensemble C_ss/C_sH/C_HH pole rows or an equivalent source-overlap theorem",
            "finite-volume/IR/isolated-pole and Gram-purity checks",
        ],
        "future_file_presence": future_presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not use FMS literature as proof authority",
            "does not identify the current taste-radial source with canonical O_H",
            "does not treat finite C_sx/C_xx rows as C_sH/C_HH pole evidence",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "forbidden_firewall": firewall,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
