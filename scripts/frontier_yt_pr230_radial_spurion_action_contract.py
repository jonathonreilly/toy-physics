#!/usr/bin/env python3
"""
PR #230 no-independent-top-source radial-spurion action contract.

The previous radial-spurion theorem proves that a common dv/ds cancels from
top/W and top/Z response ratios only if the same scalar source moves a single
canonical-Higgs radial branch and does not also add an independent top
bare-mass source.  This runner turns that theorem into an explicit future
action contract.

The contract is support only.  It deliberately does not adopt a new EW/Higgs
action on the current PR230 surface, does not write the accepted action
certificate path, and does not claim y_t closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_radial_spurion_action_contract_2026-05-06.json"

PARENTS = {
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "radial_spurion_sector_overlap_theorem": "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "wz_same_source_ew_action_certificate_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

ACCEPTED_ACTION_PATH = ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_2026-05-04.json"

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def radial_spurion_contract() -> dict[str, Any]:
    return {
        "contract_kind": "same_surface_radial_spurion_action_contract",
        "same_source_coordinate": "s",
        "source_meaning": (
            "s perturbs the Higgs radial branch through the centered composite "
            "O_H = Phi^dagger Phi - <Phi^dagger Phi>; top, W, and Z masses "
            "respond only through the induced v(s)."
        ),
        "required_action_terms": [
            "SU(2)xU(1) gauge action on the same lattice surface",
            "gauge-covariant Higgs doublet kinetic term",
            "Higgs potential/source term with dS/ds = sum_x O_H(x)",
            "top Yukawa term y_t * qbar_L Phi t_R + h.c.",
            "no independent s * tbar t additive top bare-mass term",
        ],
        "forbidden_action_terms": [
            "independent additive top bare-mass source under the same s",
            "separate source coordinate for top response",
            "observed-mass or observed-y_t selector",
            "H_unit or yt_ward_identity operator authority",
        ],
        "mass_branches": {
            "top": "m_t(s) = y_t * v(s) / sqrt(2)",
            "W": "M_W(s) = g2 * v(s) / 2",
            "Z": "M_Z(s) = sqrt(g2^2 + gY^2) * v(s) / 2",
        },
        "response_readout_rows_required": [
            "same-source top response dE_top/ds with no additive-top component",
            "same-source W or Z mass response under the same source shift",
            "matched top/W or top/Z covariance rows",
            "strict non-observed g2 or g2/gY authority",
            "accepted action certificate and W/Z mass-fit path",
        ],
    }


def response_ratio_witnesses() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for dv_ds in (0.2, 1.0, 2.5):
        for y_t, g2, g_y in ((0.65, 0.55, 0.22), (1.15, 0.85, 0.31)):
            top = y_t * dv_ds / math.sqrt(2.0)
            w = g2 * dv_ds / 2.0
            gz = math.sqrt(g2 * g2 + g_y * g_y)
            z = gz * dv_ds / 2.0
            rows.append(
                {
                    "dv_ds": dv_ds,
                    "input_y_t": y_t,
                    "input_g2": g2,
                    "input_gY": g_y,
                    "dm_top_ds": top,
                    "dM_W_ds": w,
                    "dM_Z_ds": z,
                    "yt_from_top_W_ratio": g2 * top / (math.sqrt(2.0) * w),
                    "yt_from_top_Z_ratio": gz * top / (math.sqrt(2.0) * z),
                }
            )
    return rows


def additive_source_counterexample() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    y_t = 0.95
    g2 = 0.62
    dv_ds = 1.3
    w = g2 * dv_ds / 2.0
    for additive_top_slope in (-0.25, 0.0, 0.35):
        top = y_t * dv_ds / math.sqrt(2.0) + additive_top_slope
        rows.append(
            {
                "input_y_t": y_t,
                "input_g2": g2,
                "dv_ds": dv_ds,
                "independent_additive_top_slope": additive_top_slope,
                "dm_top_ds": top,
                "dM_W_ds": w,
                "yt_inferred_if_contract_ignored": g2 * top / (math.sqrt(2.0) * w),
            }
        )
    return rows


def all_close_to_input(rows: list[dict[str, float]]) -> bool:
    return all(
        abs(row["yt_from_top_W_ratio"] - row["input_y_t"]) < 1.0e-12
        and abs(row["yt_from_top_Z_ratio"] - row["input_y_t"]) < 1.0e-12
        for row in rows
    )


def counterexample_varies(rows: list[dict[str, float]]) -> bool:
    values = [round(row["yt_inferred_if_contract_ignored"], 12) for row in rows]
    return len(set(values)) > 1 and any(
        abs(row["yt_inferred_if_contract_ignored"] - row["input_y_t"]) > 1.0e-9
        for row in rows
    )


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_observed_wz_masses_or_g2": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "set_g2_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
        "wrote_accepted_action_certificate": False,
    }


def main() -> int:
    print("PR #230 no-independent-top-source radial-spurion action contract")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    contract = radial_spurion_contract()
    ratio_rows = response_ratio_witnesses()
    counter_rows = additive_source_counterexample()
    firewall = forbidden_firewall()

    theorem_loaded = (
        parents["radial_spurion_sector_overlap_theorem"].get(
            "radial_spurion_sector_overlap_theorem_passed"
        )
        is True
        and parents["radial_spurion_sector_overlap_theorem"].get(
            "current_surface_sector_overlap_identity_supplied"
        )
        is False
    )
    ansatz_loaded_but_not_clean = (
        parents["same_source_ew_higgs_action_ansatz_gate"].get(
            "same_source_ew_higgs_action_ansatz_gate_passed"
        )
        is True
        and parents["same_source_ew_higgs_action_ansatz_gate"].get(
            "current_surface_adoption_passed"
        )
        is False
        and "S_PR230_top[s] with the existing additive top scalar source coordinate"
        in " ".join(
            parents["same_source_ew_higgs_action_ansatz_gate"]
            .get("action_ansatz", {})
            .get("action_terms", [])
        )
    )
    adoption_still_blocked = (
        parents["same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and parents["same_source_ew_action_adoption_attempt"].get("adoption_allowed_now")
        is False
    )
    mass_source_bridge_loaded = (
        parents["higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and parents["higgs_mass_source_action_bridge"].get("proposal_allowed") is False
    )
    builder_still_absent = (
        parents["wz_same_source_ew_action_certificate_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and not ACCEPTED_ACTION_PATH.exists()
    )
    route_gates_still_open = (
        parents["wz_response_route_completion"].get("proposal_allowed") is False
        and parents["action_first_route_completion"].get("proposal_allowed") is False
        and parents["retained_closure_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    ratio_identity_passed = all_close_to_input(ratio_rows)
    additive_counterexample_passed = counterexample_varies(counter_rows)
    contract_forbids_additive_top_source = any(
        "additive top" in item for item in contract["forbidden_action_terms"]
    )
    no_accepted_action_written = not ACCEPTED_ACTION_PATH.exists()
    clean_firewall = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("radial-spurion-theorem-loaded", theorem_loaded, statuses["radial_spurion_sector_overlap_theorem"])
    report("current-ansatz-loaded-but-additive-top-source-not-clean", ansatz_loaded_but_not_clean, statuses["same_source_ew_higgs_action_ansatz_gate"])
    report("adoption-still-blocked", adoption_still_blocked, statuses["same_source_ew_action_adoption_attempt"])
    report("mass-source-bridge-loaded", mass_source_bridge_loaded, statuses["higgs_mass_source_action_bridge"])
    report("accepted-action-builder-still-absent", builder_still_absent, statuses["wz_same_source_ew_action_gate"])
    report("route-gates-still-open", route_gates_still_open, "proposal_allowed=false across route/retained/campaign")
    report("response-ratio-witnesses-cancel-dvds", ratio_identity_passed, "top/W and top/Z ratios recover input y_t")
    report("additive-top-source-counterexample-varies-readout", additive_counterexample_passed, str(counter_rows))
    report("contract-forbids-independent-additive-top-source", contract_forbids_additive_top_source, str(contract["forbidden_action_terms"]))
    report("accepted-action-certificate-not-written", no_accepted_action_written, rel(ACCEPTED_ACTION_PATH))
    report("forbidden-firewall-clean", clean_firewall, str(firewall))

    passed = (
        not missing
        and not proposals
        and theorem_loaded
        and ansatz_loaded_but_not_clean
        and adoption_still_blocked
        and mass_source_bridge_loaded
        and builder_still_absent
        and route_gates_still_open
        and ratio_identity_passed
        and additive_counterexample_passed
        and contract_forbids_additive_top_source
        and no_accepted_action_written
        and clean_firewall
    )
    result = {
        "actual_current_surface_status": (
            "exact-support / no-independent-top-source radial-spurion action contract; current additive-source action not adopted"
        ),
        "conditional_surface_status": (
            "If this contract is adopted by a same-surface EW/Higgs action and "
            "production top/W or top/Z response rows plus strict gauge-coupling "
            "authority are supplied, the common dv/ds source overlap cancels in "
            "the response ratio."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The contract is a future action target only.  The current ansatz "
            "still includes an additive top source, the accepted EW action "
            "certificate is absent, W/Z rows are absent, and retained/campaign "
            "gates deny proposal wording."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "radial_spurion_action_contract_passed": passed,
        "contract_kind": contract["contract_kind"],
        "contract": contract,
        "response_ratio_witnesses": ratio_rows,
        "additive_top_source_counterexample": counter_rows,
        "current_surface_contract_satisfied": False,
        "accepted_action_certificate_written": False,
        "accepted_action_certificate_path": rel(ACCEPTED_ACTION_PATH),
        "required_future_rows": contract["response_readout_rows_required"],
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not adopt the EW/Higgs action on the current surface",
            "does not write the accepted same-source EW action certificate",
            "does not use the current additive top FH source as a radial spurion",
            "does not provide W/Z rows, top/W covariance, or strict g2 authority",
            "does not provide canonical O_H or C_sH/C_HH pole rows",
            "does not claim retained or proposed_retained closure",
        ],
        "exact_next_action": (
            "Either replace the current additive top-source ansatz with an "
            "accepted no-independent-top-source EW/Higgs action certificate and "
            "run matched top/WZ response rows, or use the action-first O_H path "
            "to generate C_ss/C_sH/C_HH pole rows with Gram/FV/IR authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
