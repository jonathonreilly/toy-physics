#!/usr/bin/env python3
"""
PR #230 FMS source-overlap readout gate.

Block19 made the FMS O_H candidate/action packet explicit.  This runner
connects that packet to the exact source-Higgs residue readout that would fix
the remaining kappa_s/source-overlap normalization:

    kappa_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH)).

It is a strict future-readout gate.  On the current PR230 surface the action is
not adopted, canonical O_H is absent, and C_ss/C_sH/C_HH pole rows are absent,
so the gate must pass only as support-not-proof.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json"
STRICT_ROWS = ROOT / "outputs" / "yt_pr230_source_higgs_pole_rows_2026-05-06.json"

PARENTS = {
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "source_higgs_time_kernel_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def load(rel_or_path: str | Path) -> dict[str, Any]:
    path = rel_or_path if isinstance(rel_or_path, Path) else ROOT / rel_or_path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def kappa_readout(res_c_ss: float, res_c_sh: float, res_c_hh: float) -> dict[str, Any]:
    product = res_c_ss * res_c_hh
    kappa = res_c_sh / math.sqrt(product) if product > 0.0 else float("nan")
    gram_det = product - res_c_sh * res_c_sh
    return {
        "Res_C_ss": res_c_ss,
        "Res_C_sH": res_c_sh,
        "Res_C_HH": res_c_hh,
        "source_higgs_overlap_kappa_sH": kappa,
        "gram_determinant": gram_det,
        "pure_overlap": math.isfinite(kappa) and abs(abs(kappa) - 1.0) <= 1.0e-12,
    }


def row_payload_readout(payload: dict[str, Any]) -> dict[str, Any]:
    rows = payload.get("pole_rows", payload.get("rows", []))
    if isinstance(rows, dict):
        rows = list(rows.values())
    if not isinstance(rows, list) or not rows:
        return {"rows_present": bool(payload), "computed": False, "row_count": 0}
    row = rows[0] if isinstance(rows[0], dict) else {}
    if not all(finite(row.get(key)) for key in ("Res_C_ss", "Res_C_sH", "Res_C_HH")):
        return {"rows_present": True, "computed": False, "row_count": len(rows)}
    return {
        "rows_present": True,
        "computed": True,
        "row_count": len(rows),
        **kappa_readout(
            float(row["Res_C_ss"]),
            float(row["Res_C_sH"]),
            float(row["Res_C_HH"]),
        ),
    }


def witness() -> dict[str, Any]:
    pure = kappa_readout(9.0, 6.0, 4.0)
    mixed = kappa_readout(9.0, 3.0, 4.0)
    same_source_y = 1.0
    orthogonal_family = []
    for y_h in (0.25, 1.0, 1.75):
        rho = 0.5
        orth = math.sqrt(1.0 - rho * rho)
        y_chi = (same_source_y - rho * y_h) / orth
        orthogonal_family.append(
            {
                "rho_sH": rho,
                "same_source_y": same_source_y,
                "canonical_y_H": y_h,
                "orthogonal_y_chi_required": y_chi,
                "reconstructed_source_y": rho * y_h + orth * y_chi,
            }
        )
    return {
        "pure_one_pole_readout": pure,
        "mixed_overlap_readout": mixed,
        "orthogonal_counterfamily": orthogonal_family,
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yt": False,
        "used_observed_wz_or_g2": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_pilots_as_production": False,
        "used_fms_literature_as_proof_authority": False,
        "used_c_sx_c_xx_as_c_sh_c_hh": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 FMS source-overlap readout gate")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    strict_rows = load(STRICT_ROWS)
    strict_readout = row_payload_readout(strict_rows)
    w = witness()
    firewall = forbidden_firewall()

    fms_packet_support_only = (
        "FMS O_H candidate/action packet" in statuses["fms_oh_candidate_action_packet"]
        and certs["fms_oh_candidate_action_packet"].get("fms_oh_candidate_action_packet_passed") is True
        and certs["fms_oh_candidate_action_packet"].get("proposal_allowed") is False
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface") is False
        and certs["fms_oh_candidate_action_packet"].get("same_surface_cl3_z3_derived") is False
        and certs["fms_oh_candidate_action_packet"].get("closure_authorized") is False
    )
    kappa_contract_loaded = (
        certs["source_higgs_overlap_kappa_contract"].get("source_higgs_overlap_kappa_contract_passed") is True
        and certs["source_higgs_overlap_kappa_contract"].get("proposal_allowed") is False
    )
    pole_contract_loaded_rows_absent = (
        certs["source_higgs_pole_row_acceptance_contract"].get("source_higgs_pole_row_acceptance_contract_passed") is True
        and certs["source_higgs_pole_row_acceptance_contract"].get("rows_present") is False
        and certs["source_higgs_pole_row_acceptance_contract"].get("closure_contract_satisfied") is False
    )
    post_fms_overlap_still_needed = (
        certs["post_fms_source_overlap_necessity_gate"].get("post_fms_source_overlap_necessity_gate_passed") is True
        and certs["post_fms_source_overlap_necessity_gate"].get("current_source_overlap_authority_present") is False
    )
    time_kernel_manifest_support_only = (
        certs["source_higgs_time_kernel_manifest"].get("proposal_allowed") is False
        and certs["source_higgs_time_kernel_manifest"].get("closure_launch_authorized_now") is False
        and certs["source_higgs_time_kernel_manifest"].get("operator_certificate_is_canonical_oh") is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    accepted_action_absent = (
        certs["same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
        and certs["same_source_ew_action_gate"].get("proposal_allowed") is False
    )
    strict_rows_absent = strict_readout["rows_present"] is False and not STRICT_ROWS.exists()
    pure_formula_checks = (
        abs(float(w["pure_one_pole_readout"]["source_higgs_overlap_kappa_sH"]) - 1.0) <= 1.0e-12
        and abs(float(w["pure_one_pole_readout"]["gram_determinant"])) <= 1.0e-12
        and abs(float(w["mixed_overlap_readout"]["source_higgs_overlap_kappa_sH"]) - 0.5) <= 1.0e-12
        and float(w["mixed_overlap_readout"]["gram_determinant"]) > 0.0
    )
    counterfamily_blocks_source_y = (
        len({round(float(row["same_source_y"]), 12) for row in w["orthogonal_counterfamily"]}) == 1
        and len({round(float(row["canonical_y_H"]), 12) for row in w["orthogonal_counterfamily"]}) == 3
        and all(abs(float(row["reconstructed_source_y"]) - 1.0) <= 1.0e-12 for row in w["orthogonal_counterfamily"])
    )
    aggregate_open = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in firewall.values())

    readout_executable_now = (
        not missing
        and not proposal_allowed
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface") is True
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is True
        and certs["same_source_ew_action_gate"].get("same_source_ew_action_ready") is True
        and strict_readout.get("computed") is True
        and certs["source_higgs_pole_row_acceptance_contract"].get("closure_contract_satisfied") is True
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-packet-support-only", fms_packet_support_only, statuses["fms_oh_candidate_action_packet"])
    report("kappa-contract-loaded", kappa_contract_loaded, statuses["source_higgs_overlap_kappa_contract"])
    report("pole-contract-loaded-rows-absent", pole_contract_loaded_rows_absent, statuses["source_higgs_pole_row_acceptance_contract"])
    report("post-fms-overlap-still-needed", post_fms_overlap_still_needed, statuses["post_fms_source_overlap_necessity_gate"])
    report("time-kernel-manifest-support-only", time_kernel_manifest_support_only, statuses["source_higgs_time_kernel_manifest"])
    report("canonical-oh-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("accepted-action-absent", accepted_action_absent, statuses["same_source_ew_action_gate"])
    report("strict-row-file-absent", strict_rows_absent, rel(STRICT_ROWS))
    report("residue-readout-formula-checks", pure_formula_checks, str(w))
    report("orthogonal-counterfamily-blocks-source-only-y", counterfamily_blocks_source_y, str(w["orthogonal_counterfamily"]))
    report("readout-not-executable-now", not readout_executable_now, f"readout_executable_now={readout_executable_now}")
    report("aggregate-route-still-open", aggregate_open, "retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact-support / FMS source-overlap readout gate; action, canonical O_H, and strict C_ss/C_sH/C_HH pole rows absent on current PR230 surface"
        ),
        "conditional_surface_status": (
            "readout support if a future accepted same-surface FMS/EW-Higgs action, canonical O_H certificate, and accepted C_ss/C_sH/C_HH pole rows exist"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The readout formula is exact support, but the current surface lacks accepted action authority, canonical O_H, and strict source-Higgs pole rows."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_source_overlap_readout_gate_passed": passed,
        "closure_authorized": False,
        "readout_executable_now": readout_executable_now,
        "strict_rows_path": rel(STRICT_ROWS),
        "strict_rows_present": STRICT_ROWS.exists(),
        "strict_readout": strict_readout,
        "formula": "kappa_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))",
        "witness": w,
        "missing_current_prerequisites": [
            "accepted same-surface EW/Higgs/FMS action",
            "canonical O_H certificate",
            "strict C_ss/C_sH/C_HH pole-row packet",
            "accepted pole-row/Gram/FV/IR/scalar-LSZ certificate",
            "aggregate retained-route and campaign approval",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not set kappa_s to one",
            "does not infer Res C_sH from source-only, FMS C_HH, or C_sx/C_xx rows",
            "does not treat the FMS packet as an accepted current-surface action",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Supply the accepted same-surface action/operator certificate and strict source-Higgs pole rows, then rerun this gate to compute kappa_sH."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
