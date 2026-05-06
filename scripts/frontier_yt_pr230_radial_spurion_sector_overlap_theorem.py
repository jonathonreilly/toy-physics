#!/usr/bin/env python3
"""
PR #230 radial-spurion sector-overlap theorem.

This runner attacks the same-source sector-overlap prerequisite named by the
same-source EW action adoption attempt.  It proves a conditional positive
statement:

    If the PR230 scalar source is an adopted single radial spurion for the
    canonical Higgs branch, so that top, W, and Z masses all depend on the same
    v(s) and there is no independent additive top bare-mass source, then the
    unknown source overlap dv/ds cancels from top/W and top/Z response ratios.

It also proves the matching boundary:

    If the same source coordinate contains an independent additive top
    bare-mass component, the sector-overlap identity is not derived.  This is
    the current PR230 risk surface, so the theorem is support/contract only and
    not closure.
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
    / "yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json"
)

PARENTS = {
    "same_source_ew_higgs_action_ansatz_gate": (
        "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json"
    ),
    "same_source_ew_action_adoption_attempt": (
        "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json"
    ),
    "same_source_sector_overlap_identity_obstruction": (
        "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json"
    ),
    "higgs_mass_source_action_bridge": (
        "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json"
    ),
    "fms_composite_oh_conditional_theorem": (
        "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json"
    ),
    "wz_correlator_mass_fit_path_gate": (
        "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json"
    ),
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_observed_top_mass_or_yt": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_reduced_pilot_as_production": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def radial_ratio_rows() -> list[dict[str, float]]:
    """Return exact-style numeric witnesses for source-overlap cancellation.

    The formulas being checked are symbolic:

        m_t(s) = y_t v(s) / sqrt(2)
        M_W(s) = g2 v(s) / 2
        M_Z(s) = sqrt(g2^2 + gY^2) v(s) / 2

    The rows vary dv/ds, v, and couplings to verify that only the algebraic
    ratio is used; no observed values are embedded.
    """

    rows: list[dict[str, float]] = []
    for dv_ds in (0.25, 1.0, 3.0):
        for y_t, g2, gY in ((0.7, 0.5, 0.2), (1.3, 0.8, 0.35)):
            top_slope = y_t * dv_ds / math.sqrt(2.0)
            w_slope = g2 * dv_ds / 2.0
            gz = math.sqrt(g2 * g2 + gY * gY)
            z_slope = gz * dv_ds / 2.0
            y_from_w = g2 * top_slope / (math.sqrt(2.0) * w_slope)
            y_from_z = gz * top_slope / (math.sqrt(2.0) * z_slope)
            rows.append(
                {
                    "dv_ds": dv_ds,
                    "input_y_t": y_t,
                    "input_g2": g2,
                    "input_gY": gY,
                    "top_slope": top_slope,
                    "w_slope": w_slope,
                    "z_slope": z_slope,
                    "y_from_w_response_ratio": y_from_w,
                    "y_from_z_response_ratio": y_from_z,
                }
            )
    return rows


def additive_top_source_counterfamily() -> list[dict[str, float]]:
    """Show that an independent top bare-mass source breaks the identity."""

    y_t = 0.9
    g2 = 0.6
    dv_ds = 1.1
    rows: list[dict[str, float]] = []
    for additive_top_slope in (-0.4, 0.0, 0.4):
        top_slope = y_t * dv_ds / math.sqrt(2.0) + additive_top_slope
        w_slope = g2 * dv_ds / 2.0
        inferred_y = g2 * top_slope / (math.sqrt(2.0) * w_slope)
        rows.append(
            {
                "dv_ds": dv_ds,
                "input_y_t": y_t,
                "input_g2": g2,
                "independent_additive_top_slope": additive_top_slope,
                "top_slope": top_slope,
                "w_slope": w_slope,
                "y_inferred_if_radial_spurion_assumed": inferred_y,
            }
        )
    return rows


def allclose(values: list[float], targets: list[float], tol: float = 1.0e-12) -> bool:
    return len(values) == len(targets) and all(
        abs(float(value) - float(target)) <= tol
        for value, target in zip(values, targets)
    )


def parent_conditionals(certs: dict[str, dict[str, Any]]) -> dict[str, bool]:
    ansatz = certs["same_source_ew_higgs_action_ansatz_gate"]
    adoption = certs["same_source_ew_action_adoption_attempt"]
    sector = certs["same_source_sector_overlap_identity_obstruction"]
    mass_bridge = certs["higgs_mass_source_action_bridge"]
    fms = certs["fms_composite_oh_conditional_theorem"]
    wz_fit = certs["wz_correlator_mass_fit_path_gate"]
    retained = certs["retained_closure_route"]
    campaign = certs["campaign_status"]
    return {
        "ansatz_supplies_centered_phi_dagger_phi_source": (
            ansatz.get("same_source_ew_higgs_action_ansatz_gate_passed") is True
            and ansatz.get("current_surface_adoption_passed") is False
        ),
        "adoption_attempt_names_sector_overlap_prerequisite": (
            "same_source_sector_overlap_identity"
            in adoption.get("missing_schema_prerequisites", [])
        ),
        "prior_sector_overlap_obstruction_loaded": (
            sector.get("sector_overlap_identity_gate_passed") is False
            and "k_top/k_gauge" in json.dumps(sector.get("formula", {}))
        ),
        "mass_source_bridge_loaded": (
            mass_bridge.get("higgs_mass_source_action_bridge_passed") is True
            and mass_bridge.get("proposal_allowed") is False
        ),
        "fms_composite_bridge_loaded": (
            fms.get("fms_composite_oh_conditional_theorem_passed") is True
            and fms.get("proposal_allowed") is False
        ),
        "wz_mass_fit_rows_absent": (
            wz_fit.get("wz_correlator_mass_fit_path_ready") is False
            and wz_fit.get("future_mass_fit_rows_present") is False
        ),
        "aggregate_route_still_open": (
            retained.get("proposal_allowed") is False
            and campaign.get("proposal_allowed") is False
        ),
    }


def main() -> int:
    print("PR #230 radial-spurion sector-overlap theorem")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    conditionals = parent_conditionals(certs)
    radial_rows = radial_ratio_rows()
    counter_rows = additive_top_source_counterfamily()
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    radial_y_w = [row["y_from_w_response_ratio"] for row in radial_rows]
    radial_y_z = [row["y_from_z_response_ratio"] for row in radial_rows]
    radial_targets = [row["input_y_t"] for row in radial_rows]
    radial_identity_passed = allclose(radial_y_w, radial_targets) and allclose(
        radial_y_z, radial_targets
    )

    counter_inferred = [
        row["y_inferred_if_radial_spurion_assumed"] for row in counter_rows
    ]
    counter_targets = [row["input_y_t"] for row in counter_rows]
    additive_source_blocks_identity = (
        any(abs(value - target) > 1.0e-9 for value, target in zip(counter_inferred, counter_targets))
        and any(abs(value - target) <= 1.0e-12 for value, target in zip(counter_inferred, counter_targets))
        and len({round(value, 12) for value in counter_inferred}) > 1
    )

    clean_radial_contract = {
        "single_scalar_source_coordinate": True,
        "source_is_canonical_higgs_radial_spurion": True,
        "all_top_w_z_masses_depend_on_same_v_of_s": True,
        "no_independent_additive_top_bare_mass_source": True,
        "same_ensemble_same_source_shift_response_rows_required": True,
    }
    current_pr230_risk_surface = {
        "existing_fh_lsz_source_is_additive_bare_mass_shift": True,
        "same_source_ew_higgs_ansatz_not_adopted": True,
        "wz_mass_fit_rows_absent": conditionals["wz_mass_fit_rows_absent"],
        "canonical_higgs_operator_certificate_absent": True,
        "radial_spurion_contract_currently_satisfied": False,
    }

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    for key, ok in conditionals.items():
        report(key, ok, str(ok))
    report("radial-spurion-response-ratio-identity", radial_identity_passed, "top/W and top/Z ratios recover input y_t")
    report("additive-top-source-counterfamily-blocks-shortcut", additive_source_blocks_identity, str(counter_inferred))
    report("clean-radial-contract-has-no-independent-top-source", clean_radial_contract["no_independent_additive_top_bare_mass_source"], str(clean_radial_contract))
    report("current-pr230-risk-surface-not-radial-spurion-clean", not current_pr230_risk_surface["radial_spurion_contract_currently_satisfied"], str(current_pr230_risk_surface))
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    theorem_passed = (
        not missing
        and not proposal_allowed
        and all(conditionals.values())
        and radial_identity_passed
        and additive_source_blocks_identity
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / conditional radial-spurion sector-overlap theorem; current PR230 additive-source shortcut blocked"
        ),
        "conditional_surface_status": (
            "If a same-surface EW/Higgs action is adopted with the scalar source "
            "as a single canonical-Higgs radial spurion, and no independent "
            "additive top bare-mass source is present, then the sector-overlap "
            "identity k_top = k_W = k_Z is algebraically supplied in response "
            "ratios."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem is conditional support for a future radial-spurion "
            "action/response packet.  The current PR230 FH/LSZ source is an "
            "additive top mass shift, the same-source EW/Higgs ansatz is not "
            "adopted, canonical O_H is absent, and W/Z mass-fit rows are absent."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "radial_spurion_sector_overlap_theorem_passed": theorem_passed,
        "sector_overlap_identity_conditionally_supplied": theorem_passed,
        "current_surface_sector_overlap_identity_supplied": False,
        "current_surface_closure_authorized": False,
        "clean_radial_spurion_contract": clean_radial_contract,
        "current_pr230_risk_surface": current_pr230_risk_surface,
        "formula": {
            "top_mass_branch": "m_t(s) = y_t * v(s) / sqrt(2)",
            "w_mass_branch": "M_W(s) = g2 * v(s) / 2",
            "z_mass_branch": "M_Z(s) = sqrt(g2^2 + gY^2) * v(s) / 2",
            "top_w_ratio": "y_t = g2 * (dm_t/ds) / (sqrt(2) * dM_W/ds)",
            "top_z_ratio": "y_t = sqrt(g2^2 + gY^2) * (dm_t/ds) / (sqrt(2) * dM_Z/ds)",
            "shared_overlap_cancelled": "dv/ds",
            "shortcut_blocker": (
                "an independent additive top source adds a_top to dm_t/ds "
                "and changes the ratio unless a_top=0 or is measured and subtracted"
            ),
        },
        "radial_spurion_witness_rows": radial_rows,
        "additive_top_source_counterfamily": counter_rows,
        "parent_conditionals": conditionals,
        "parent_statuses": {name: status(cert) for name, cert in certs.items()},
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify the current additive top mass source with a canonical radial spurion",
            "does not set kappa_s, c2, Z_match, k_top/k_gauge, or g2 to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not write accepted same-source EW action, canonical O_H, W/Z row, or source-Higgs row certificates",
        ],
        "exact_next_action": (
            "Tighten the action-first route to a no-independent-top-source "
            "radial-spurion action contract, then either implement same-source "
            "W/Z mass-fit rows under that source or produce O_H/C_sH/C_HH pole "
            "rows with Gram/FV/IR authority.  Reusing the existing additive "
            "top bare-mass FH source alone cannot satisfy the sector-overlap "
            "identity."
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
