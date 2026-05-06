#!/usr/bin/env python3
"""
PR #230 source-Higgs overlap/kappa contract.

This runner sharpens the clean source-Higgs route after the genuine O_sp intake
and the post-FMS source-overlap necessity gate.  It derives the exact algebraic
object that would fix the source-to-canonical-Higgs overlap:

    kappa_spH = Res(C_sp,H) / sqrt(Res(C_HH))
               = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH)).

This is a future row contract, not a current closure claim.  The current PR230
surface has no certified O_H and no C_sH/C_HH production row packet, so this
runner writes exact support plus the current open boundary.
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
    / "yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json"
)
FUTURE_CANDIDATE = (
    ROOT
    / "outputs"
    / "yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
)

PARENTS = {
    "genuine_source_pole_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "isolated_pole_gram_factorization": "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "post_fms_source_overlap_necessity": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def kappa_from_residues(c_ss: float, c_sH: float, c_HH: float) -> dict[str, float | bool]:
    product = c_ss * c_HH
    kappa = c_sH / math.sqrt(product) if product > 0.0 else float("nan")
    c_spH = c_sH / math.sqrt(c_ss) if c_ss > 0.0 else float("nan")
    delta_spH = c_HH - c_spH * c_spH if math.isfinite(c_spH) else float("nan")
    return {
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sH,
        "Res_C_HH": c_HH,
        "Res_C_spH": c_spH,
        "source_higgs_overlap_kappa_spH": kappa,
        "osp_higgs_gram_determinant": delta_spH,
        "pure_one_pole_overlap": math.isfinite(kappa) and abs(abs(kappa) - 1.0) <= 1.0e-12,
    }


def pure_row(source_scale: float, z_source: float, z_higgs: float) -> dict[str, Any]:
    c_ss = (source_scale * z_source) ** 2
    c_sH = (source_scale * z_source) * z_higgs
    c_HH = z_higgs**2
    row = kappa_from_residues(c_ss, c_sH, c_HH)
    row["source_scale"] = source_scale
    row["z_source"] = z_source
    row["z_higgs"] = z_higgs
    return row


def witness_rows() -> dict[str, Any]:
    pure = [
        pure_row(0.25, 1.7, 0.9),
        pure_row(1.0, 1.7, 0.9),
        pure_row(4.0, 1.7, 0.9),
        pure_row(1.0, 1.7, -0.9),
    ]
    mixed = []
    same_source_y = 1.0
    for kappa, y_h in ((0.8, 0.25), (0.8, 1.0), (0.8, 1.75)):
        orth_norm = math.sqrt(1.0 - kappa * kappa)
        y_chi = (same_source_y - kappa * y_h) / orth_norm
        mixed.append(
            {
                "source_higgs_overlap_kappa_spH": kappa,
                "same_source_y": same_source_y,
                "canonical_y_H": y_h,
                "orthogonal_y_chi_required": y_chi,
                "source_readout_reconstructed": kappa * y_h + orth_norm * y_chi,
            }
        )
    return {
        "pure_rescaling_rows": pure,
        "mixed_counterfamily_same_source_y": mixed,
    }


def candidate_kappa(candidate: dict[str, Any]) -> dict[str, Any]:
    matrix = candidate.get("residue_matrix", {})
    if not all(finite(matrix.get(key)) for key in ("Res_C_ss", "Res_C_sH", "Res_C_HH")):
        return {"candidate_present": bool(candidate), "computed": False}
    row = kappa_from_residues(
        float(matrix["Res_C_ss"]),
        float(matrix["Res_C_sH"]),
        float(matrix["Res_C_HH"]),
    )
    return {"candidate_present": True, "computed": True, **row}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_pilot_as_production": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "treated_fms_c_hh_as_source_overlap": False,
        "treated_c_sx_c_xx_as_c_sh_c_hh": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 source-Higgs overlap/kappa contract")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = witness_rows()
    candidate = load(FUTURE_CANDIDATE)
    candidate_overlap = candidate_kappa(candidate)
    firewall = forbidden_firewall()

    genuine_osp_available = (
        parents["genuine_source_pole_intake"].get("artifact_is_genuine_current_surface_support")
        is True
        and parents["genuine_source_pole_intake"].get("artifact_is_physics_closure") is False
        and parents["genuine_source_pole_intake"].get("source_rescaling_invariant") is True
        and parents["genuine_source_pole_intake"].get("contact_term_invariant") is True
        and parents["genuine_source_pole_intake"].get("canonical_higgs_operator_identity_passed") is False
    )
    isolated_pole_support_loaded = (
        parents["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True
        and parents["isolated_pole_gram_factorization"].get("proposal_allowed") is False
    )
    source_higgs_rows_absent = (
        parents["source_higgs_builder"].get("input_present") is False
        and parents["source_higgs_builder"].get("candidate_written") is False
        and not FUTURE_CANDIDATE.exists()
    )
    postprocessor_waits = (
        parents["source_higgs_gram_postprocess"].get("candidate_present") is False
        and parents["source_higgs_gram_postprocess"].get("osp_higgs_gram_purity_gate_passed")
        is False
    )
    source_only_blocked = (
        "source-functional LSZ identifiability" in status(parents["source_functional_lsz_identifiability"])
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    fms_proxy_blocked = (
        parents["post_fms_source_overlap_necessity"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and parents["post_fms_source_overlap_necessity"].get(
            "current_source_overlap_authority_present"
        )
        is False
    )
    aggregate_still_open = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    pure_kappas = [round(float(row["source_higgs_overlap_kappa_spH"]), 12) for row in witness["pure_rescaling_rows"][:3]]
    rescaling_invariant = len(set(pure_kappas)) == 1 and abs(abs(pure_kappas[0]) - 1.0) <= 1.0e-12
    sign_is_not_fixed_by_rows_alone = (
        witness["pure_rescaling_rows"][0]["source_higgs_overlap_kappa_spH"]
        == -witness["pure_rescaling_rows"][3]["source_higgs_overlap_kappa_spH"]
    )
    mixed_counterfamily_blocks_yh = (
        len({round(float(row["same_source_y"]), 12) for row in witness["mixed_counterfamily_same_source_y"]})
        == 1
        and len({round(float(row["canonical_y_H"]), 12) for row in witness["mixed_counterfamily_same_source_y"]})
        > 1
        and all(
            abs(float(row["source_readout_reconstructed"]) - 1.0) <= 1.0e-12
            for row in witness["mixed_counterfamily_same_source_y"]
        )
    )
    firewall_clean = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("genuine-osp-source-side-normalization-loaded", genuine_osp_available, status(parents["genuine_source_pole_intake"]))
    report("isolated-pole-gram-support-loaded", isolated_pole_support_loaded, status(parents["isolated_pole_gram_factorization"]))
    report("kappa-formula-source-rescaling-invariant", rescaling_invariant, str(pure_kappas))
    report("sign-convention-not-fixed-by-source-only-rows", sign_is_not_fixed_by_rows_alone, "C_spH sign must be fixed by future convention/row")
    report("mixed-counterfamily-blocks-canonical-y-from-source-y", mixed_counterfamily_blocks_yh, "same source readout, varying canonical y_H")
    report("current-source-higgs-row-packet-absent", source_higgs_rows_absent, str(FUTURE_CANDIDATE.relative_to(ROOT)))
    report("gram-postprocessor-awaits-production", postprocessor_waits, status(parents["source_higgs_gram_postprocess"]))
    report("source-only-kappa-closure-blocked", source_only_blocked, status(parents["source_functional_lsz_identifiability"]))
    report("fms-and-csx-proxy-overlap-blocked", fms_proxy_blocked, status(parents["post_fms_source_overlap_necessity"]))
    report("aggregate-route-still-open", aggregate_still_open, "retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    passed = (
        not missing
        and not proposal_allowed
        and genuine_osp_available
        and isolated_pole_support_loaded
        and rescaling_invariant
        and sign_is_not_fixed_by_rows_alone
        and mixed_counterfamily_blocks_yh
        and source_higgs_rows_absent
        and postprocessor_waits
        and source_only_blocked
        and fms_proxy_blocked
        and aggregate_still_open
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / source-Higgs overlap-kappa row contract; current row packet absent"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface certified O_H row packet "
            "supplies Res_C_ss, Res_C_sH, Res_C_HH at a nondegenerate isolated pole "
            "and passes O_sp-Higgs Gram purity, FV/IR/model-class, and retained-route gates"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The contract derives the overlap object but current PR230 has no "
            "canonical O_H certificate or source-Higgs C_sH/C_HH production rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "source_higgs_overlap_kappa_contract_passed": passed,
        "future_candidate_present": bool(candidate),
        "future_candidate_overlap": candidate_overlap,
        "overlap_formula": {
            "kappa_spH": "Res(C_sp,H) / sqrt(Res(C_HH))",
            "equivalent_raw_rows": "Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))",
            "source_pole_normalization": "O_sp = O_s / sqrt(Res(C_ss)) = sqrt(Dprime_ss_at_pole) O_s",
            "pure_bridge_condition": "abs(kappa_spH) = 1 with same-pole O_sp-Higgs Gram purity",
            "impure_decomposition": "y_source_pole = kappa_spH*y_H + sqrt(1-kappa_spH^2)*y_chi for a normalized two-component witness",
        },
        "witness": witness,
        "current_blockers": {
            "source_higgs_row_packet_absent": source_higgs_rows_absent,
            "gram_postprocessor_waits": postprocessor_waits,
            "source_only_identifiability_blocked": source_only_blocked,
            "fms_c_hh_and_c_sx_proxy_blocked": fms_proxy_blocked,
            "aggregate_retained_route_open": aggregate_still_open,
        },
        "parent_certificates": PARENTS,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not identify O_sp with O_H without measured C_spH/C_HH and Gram purity",
            "does not treat FMS C_HH, C_sx/C_xx chunks, or source-only rows as Res C_sH",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Produce a same-surface certified O_H/C_sH/C_HH pole-row packet, "
            "compute kappa_spH from the normalized cross residue, then rerun the "
            "source-Higgs builder, Gram postprocessor, full assembly, retained-route, "
            "and campaign gates."
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
