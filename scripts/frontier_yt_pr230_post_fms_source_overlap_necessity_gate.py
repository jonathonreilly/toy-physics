#!/usr/bin/env python3
r"""
PR #230 post-FMS source-overlap necessity gate.

The FMS composite theorem gives the right future operator bridge:

    O_H = Phi^\dagger Phi - <Phi^\dagger Phi> = v h + h^2/2 + pi^2/2.

This runner asks the next load-bearing question: once that conditional bridge
is granted, do current PR230 source-pole, source-only LSZ, or taste-radial
C_sx/C_xx rows determine the source-Higgs pole overlap C_sH?

Answer: no on the current surface.  The missing object is still a genuine
same-surface source-overlap row/theorem: Res C_sH, with C_HH and Gram/FV/IR
checks, or a physical-response bypass.
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
    / "yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json"
)

PARENTS = {
    "fms_composite_oh": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "source_functional_lsz": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "oh_source_higgs_rescan": "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json",
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
    "two_source_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "source_higgs_bridge_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "full_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "two_source_combined_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
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


def overlap_family() -> list[dict[str, float | bool | None]]:
    """Fixed C_ss and FMS C_HH, varying source-Higgs overlap."""

    rows: list[dict[str, float | bool]] = []
    res_ss = 18.0
    res_hh = 18.0
    measured_source_y = 1.0
    for rho in (1.0, 0.75, 0.5, 0.25, 0.0, -0.25):
        res_sh = rho * math.sqrt(res_ss * res_hh)
        gram_det = res_ss * res_hh - res_sh * res_sh
        if abs(rho) > 1.0e-12:
            y_t_if_orthogonal_top_coupling_zero: float | None = (
                measured_source_y / rho
            )
        else:
            y_t_if_orthogonal_top_coupling_zero = None
        rows.append(
            {
                "rho_sH": rho,
                "Res_C_ss": res_ss,
                "Res_C_HH": res_hh,
                "Res_C_sH": res_sh,
                "gram_determinant": gram_det,
                "gram_purity": abs(gram_det) < 1.0e-12 and abs(abs(rho) - 1.0) < 1.0e-12,
                "same_source_y": measured_source_y,
                "canonical_y_t_if_y_chi_zero": y_t_if_orthogonal_top_coupling_zero,
            }
        )
    return rows


def orthogonal_top_counterfamily() -> list[dict[str, float]]:
    """Same measured source response, different canonical y_t values."""

    rows: list[dict[str, float]] = []
    measured_source_y = 1.0
    for rho, y_t in ((0.75, 0.5), (0.75, 1.0), (0.75, 1.5)):
        sigma = math.sqrt(1.0 - rho * rho)
        y_chi = (measured_source_y - rho * y_t) / sigma
        rows.append(
            {
                "rho_sH": rho,
                "same_source_y": measured_source_y,
                "canonical_y_t": y_t,
                "orthogonal_y_chi_required": y_chi,
            }
        )
    return rows


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_taste_radial_axis_as_canonical_oh": False,
        "treated_C_sx_C_xx_as_C_sH_C_HH_pole_rows": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 post-FMS source-overlap necessity gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}
    family = overlap_family()
    orthogonal_family = orthogonal_top_counterfamily()
    firewall = forbidden_firewall()

    fms_bridge_conditional_not_closure = (
        certs["fms_composite_oh"].get("fms_composite_oh_conditional_theorem_passed")
        is True
        and certs["fms_composite_oh"].get("current_closure_authority_present")
        is False
        and certs["fms_composite_oh"].get("source_higgs_rows_absent") is True
    )
    source_functional_blocks_source_only_overlap = (
        "source-functional LSZ identifiability" in statuses["source_functional_lsz"]
        and certs["source_functional_lsz"].get("proposal_allowed") is False
    )
    mixing_obstruction_blocks_cos_theta = (
        "source-pole canonical-Higgs mixing obstruction" in statuses["source_pole_mixing"]
        and certs["source_pole_mixing"].get("proposal_allowed") is False
    )
    rescan_finds_no_current_rows = (
        "no current same-surface canonical O_H or C_sH/C_HH row certificate"
        in statuses["oh_source_higgs_rescan"]
        and certs["oh_source_higgs_rescan"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_gate"].get("candidate_present") is False
        and certs["canonical_higgs_gate"].get("candidate_valid") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    source_higgs_rows_absent = (
        certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_builder"].get("candidate_written") is False
        and certs["source_higgs_gram"].get("source_higgs_gram_purity_gate_passed")
        is False
        and future_presence["source_higgs_rows"] is False
        and future_presence["source_higgs_production_certificate"] is False
    )
    two_source_package_current = (
        certs["two_source_package"].get("chunk_package_audit_passed") is True
        and certs["two_source_package"].get("proposal_allowed") is False
        and certs["two_source_package"].get("active_chunks_counted_as_evidence")
        is False
        and certs["two_source_package"].get("completed_chunk_count", 0) >= 52
        and certs["two_source_package"].get("completed_prefix_last") == certs[
            "two_source_package"
        ].get("completed_chunk_count")
    )
    two_source_rows_are_c_sx_not_c_sh = (
        certs["two_source_action"].get("canonical_higgs_operator_identity_passed")
        is False
        and certs["two_source_row_contract"].get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and certs["two_source_row_contract"].get("proposal_allowed") is False
        and two_source_package_current
        and certs["two_source_combiner"].get("ready_chunks")
        == certs["two_source_package"].get("completed_chunk_count")
        and certs["two_source_combiner"].get("expected_chunks") == 63
        and certs["two_source_combiner"].get("combined_rows_written") is False
        and certs["source_higgs_bridge_aperture"]
        .get("two_source_rows", {})
        .get("ready_chunks")
        == certs["two_source_package"].get("completed_chunk_count")
        and "not canonical-Higgs C_sH/C_HH pole rows"
        in certs["source_higgs_bridge_aperture"]
        .get("two_source_rows", {})
        .get("strict_limit", "")
    )
    current_package_run_control_only = (
        certs["two_source_package"].get("active_chunks_counted_as_evidence")
        is False
        and certs["two_source_package"].get("active_chunk_ids") == [53, 54]
    )
    overlap_counterfamily_blocks = (
        len({row["Res_C_sH"] for row in family}) > 1
        and len({row["Res_C_ss"] for row in family}) == 1
        and len({row["Res_C_HH"] for row in family}) == 1
        and any(row["gram_purity"] for row in family)
        and any(not row["gram_purity"] for row in family)
    )
    orthogonal_top_counterfamily_blocks = (
        len({row["same_source_y"] for row in orthogonal_family}) == 1
        and len({row["canonical_y_t"] for row in orthogonal_family}) > 1
        and all(math.isfinite(row["orthogonal_y_chi_required"]) for row in orthogonal_family)
    )
    assembly_still_open = (
        certs["full_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-bridge-conditional-not-closure", fms_bridge_conditional_not_closure, statuses["fms_composite_oh"])
    report("source-functional-blocks-source-only-overlap", source_functional_blocks_source_only_overlap, statuses["source_functional_lsz"])
    report("mixing-obstruction-blocks-cos-theta", mixing_obstruction_blocks_cos_theta, statuses["source_pole_mixing"])
    report("rescan-finds-no-current-source-higgs-rows", rescan_finds_no_current_rows, statuses["oh_source_higgs_rescan"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_gate"])
    report("source-higgs-pole-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report(
        "two-source-rows-are-csx-not-csh",
        two_source_rows_are_c_sx_not_c_sh,
        (
            f"ready={certs['two_source_combiner'].get('ready_chunks')}/"
            f"{certs['two_source_combiner'].get('expected_chunks')}; "
            "packaged chunks remain C_sx/C_xx support-only"
        ),
    )
    report(
        "current-package-run-control-only",
        current_package_run_control_only,
        f"active={certs['two_source_package'].get('active_chunk_ids')}",
    )
    report("overlap-counterfamily-blocks-inference", overlap_counterfamily_blocks, str(family))
    report("orthogonal-top-counterfamily-blocks-yukawa-inference", orthogonal_top_counterfamily_blocks, str(orthogonal_family))
    report("assembly-retained-campaign-still-open", assembly_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / post-FMS source-overlap not derivable "
            "from current PR230 source-only or C_sx/C_xx rows"
        ),
        "conditional_surface_status": (
            "exact-support if future PR230 artifacts supply canonical O_H plus "
            "C_ss/C_sH/C_HH pole rows with Gram/FV/IR checks, or a same-source "
            "physical-response bypass"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The FMS expansion gives the future composite operator but does not "
            "determine the PR230 source overlap.  Current source-only rows and "
            "taste-radial C_sx/C_xx chunks leave Res C_sH and orthogonal top "
            "couplings underdetermined."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "post_fms_source_overlap_necessity_gate_passed": passed,
        "current_source_overlap_authority_present": False,
        "fms_bridge_conditional_not_closure": fms_bridge_conditional_not_closure,
        "canonical_oh_absent": canonical_oh_absent,
        "source_higgs_rows_absent": source_higgs_rows_absent,
        "two_source_package_current": two_source_package_current,
        "two_source_ready_chunks": certs["two_source_package"].get(
            "completed_chunk_count"
        ),
        "two_source_active_chunk_ids_excluded": certs["two_source_package"].get(
            "active_chunk_ids"
        ),
        "two_source_rows_are_c_sx_not_c_sH": two_source_rows_are_c_sx_not_c_sh,
        "overlap_counterfamily": family,
        "orthogonal_top_counterfamily": orthogonal_family,
        "future_file_presence": future_presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_positive_contract": [
            "same-surface canonical O_H certificate",
            "same-ensemble C_ss/C_sH/C_HH pole rows with C_HH from the certified O_H",
            "Gram purity Res(C_sH)^2 = Res(C_ss) Res(C_HH) with uncertainty control",
            "FV/IR/isolated-pole and scalar-LSZ authority",
            "or a physical-response bypass such as matched top/W/Z rows with strict g2/covariance/delta_perp",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not treat FMS expansion as source-overlap authority",
            "does not treat C_sx/C_xx taste-radial rows as canonical C_sH/C_HH pole rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "forbidden_firewall": firewall,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
