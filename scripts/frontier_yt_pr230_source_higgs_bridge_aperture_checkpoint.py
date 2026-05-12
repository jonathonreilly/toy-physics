#!/usr/bin/env python3
"""
PR #230 source-Higgs bridge aperture checkpoint.

Block08 closed the W/Z accepted-action shortcut.  This checkpoint asks whether
the current source-Higgs side has become a real aperture instead: canonical
O_H plus production C_ss/C_sH/C_HH pole rows with Gram flatness, or at least a
row packet close enough to promote.  It consumes only existing completed
two-source taste-radial chunks; it does not touch the live chunk worker.

The result is a bounded-support / exact-boundary checkpoint.  The completed
C_sx/C_xx rows are useful staging evidence, but they remain taste-radial rows,
not canonical-Higgs pole rows, and they do not authorize retained or
proposed_retained wording.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json"
)

PARENTS = {
    "canonical_oh_hard_residual": (
        "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json"
    ),
    "source_higgs_direct_pole_row_contract": (
        "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json"
    ),
    "two_source_row_combiner": (
        "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
    ),
    "two_source_chunk_package": (
        "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json"
    ),
    "source_higgs_production_readiness": (
        "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json"
    ),
    "source_higgs_time_kernel_gevp_contract": (
        "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json"
    ),
    "strict_scalar_lsz_moment_fv": (
        "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json"
    ),
    "source_higgs_builder": (
        "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json"
    ),
    "source_higgs_gram_postprocessor": (
        "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json"
    ),
    "wz_accepted_action_root": (
        "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json"
    ),
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "canonical_higgs_operator_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_measurement_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "source_higgs_production_certificate": (
        "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
    ),
    "two_source_combined_rows": (
        "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json"
    ),
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "wz_response_ratio_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
}

FORBIDDEN_FIREWALL = {
    "used_yt_ward_identity": False,
    "used_hunit_matrix_element_or_hunit_operator": False,
    "used_y_t_bare": False,
    "used_observed_y_t_or_top_mass": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "aliased_c_sx_to_c_sh_before_canonical_oh": False,
    "touched_live_chunk_worker": False,
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def all_parent_proposals_false(parents: dict[str, dict[str, Any]]) -> list[str]:
    return [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]


def ready_tail(indices: list[Any]) -> tuple[int | None, int | None]:
    ints = sorted(int(x) for x in indices if isinstance(x, int))
    return (ints[0], ints[-1]) if ints else (None, None)


def source_higgs_aperture_table(
    parents: dict[str, dict[str, Any]], futures: dict[str, bool]
) -> list[dict[str, Any]]:
    combiner = parents["two_source_row_combiner"]
    package = parents["two_source_chunk_package"]
    readiness = parents["source_higgs_production_readiness"]
    gevp = parents["source_higgs_time_kernel_gevp_contract"]
    lsz = parents["strict_scalar_lsz_moment_fv"]

    return [
        {
            "gate": "canonical O_H certificate",
            "current_status": "absent",
            "evidence": FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"],
            "blocks_closure": not futures["canonical_higgs_operator_certificate"],
        },
        {
            "gate": "production C_ss/C_sH/C_HH pole rows",
            "current_status": "absent",
            "evidence": FUTURE_ARTIFACTS["source_higgs_measurement_rows"],
            "blocks_closure": not futures["source_higgs_measurement_rows"],
        },
        {
            "gate": "two-source taste-radial C_sx/C_xx staging rows",
            "current_status": (
                f"bounded-support: {combiner.get('ready_chunks')}/"
                f"{combiner.get('expected_chunks')} chunks ready"
            ),
            "evidence": PARENTS["two_source_row_combiner"],
            "blocks_closure": combiner.get("combined_rows_written") is not True,
        },
        {
            "gate": "completed row package evidence boundary",
            "current_status": status(package),
            "evidence": PARENTS["two_source_chunk_package"],
            "blocks_closure": package.get("proposal_allowed") is False,
        },
        {
            "gate": "source-Higgs launch readiness",
            "current_status": status(readiness),
            "evidence": PARENTS["source_higgs_production_readiness"],
            "blocks_closure": readiness.get("source_higgs_launch_ready") is not True,
        },
        {
            "gate": "time-kernel / GEVP physical pole authority",
            "current_status": status(gevp),
            "evidence": PARENTS["source_higgs_time_kernel_gevp_contract"],
            "blocks_closure": gevp.get("physical_pole_extraction_accepted") is not True,
        },
        {
            "gate": "strict scalar LSZ moment/FV authority",
            "current_status": status(lsz),
            "evidence": PARENTS["strict_scalar_lsz_moment_fv"],
            "blocks_closure": lsz.get("strict_scalar_lsz_moment_fv_authority_present")
            is not True,
        },
        {
            "gate": "source-Higgs Gram flatness",
            "current_status": status(parents["source_higgs_gram_postprocessor"]),
            "evidence": PARENTS["source_higgs_gram_postprocessor"],
            "blocks_closure": parents["source_higgs_gram_postprocessor"].get(
                "source_higgs_gram_purity_gate_passed"
            )
            is not True,
        },
    ]


def main() -> int:
    print("PR #230 source-Higgs bridge aperture checkpoint")
    print("=" * 72)

    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = all_parent_proposals_false(parents)
    futures = future_presence()

    hard = parents["canonical_oh_hard_residual"]
    direct = parents["source_higgs_direct_pole_row_contract"]
    combiner = parents["two_source_row_combiner"]
    package = parents["two_source_chunk_package"]
    readiness = parents["source_higgs_production_readiness"]
    gevp = parents["source_higgs_time_kernel_gevp_contract"]
    lsz = parents["strict_scalar_lsz_moment_fv"]
    builder = parents["source_higgs_builder"]
    gram = parents["source_higgs_gram_postprocessor"]
    wz = parents["wz_accepted_action_root"]
    campaign = parents["campaign_status"]

    ready_indices = combiner.get("ready_chunk_indices", [])
    first_ready, last_ready = ready_tail(ready_indices if isinstance(ready_indices, list) else [])
    missing_indices = combiner.get("missing_chunk_indices", [])
    expected_chunks = combiner.get("expected_chunks")
    ready_chunks = combiner.get("ready_chunks")
    present_chunks = combiner.get("present_chunks")
    aperture = source_higgs_aperture_table(parents, futures)
    open_gates = [row["gate"] for row in aperture if row["blocks_closure"]]

    hard_residual_currently_open = (
        hard.get("current_surface_closure_satisfied") is False
        and hard.get("proposal_allowed") is False
        and not any(hard.get("future_artifact_presence", {}).values())
    )
    direct_contract_support_only = (
        direct.get("source_higgs_direct_pole_row_contract_passed") is True
        and direct.get("current_surface_contract_satisfied") is False
        and direct.get("proposal_allowed") is False
    )
    two_source_rows_are_current_prefix = (
        expected_chunks == 63
        and isinstance(ready_chunks, int)
        and present_chunks == ready_chunks
        and 42 <= ready_chunks <= expected_chunks
        and first_ready == 1
        and last_ready == ready_chunks
    )
    two_source_combiner_boundary = (
        (
            combiner.get("combined_rows_written") is False
            and isinstance(missing_indices, list)
            and bool(missing_indices)
            and missing_indices[0] == int(ready_chunks) + 1
        )
        or (
            ready_chunks == expected_chunks == 63
            and combiner.get("combined_rows_written") is True
            and isinstance(missing_indices, list)
            and not missing_indices
        )
    )
    package_passed_support_only = (
        package.get("chunk_package_audit_passed") is True
        and package.get("completed_chunk_count") == ready_chunks
        and package.get("completed_prefix_last") == ready_chunks
        and package.get("active_chunks_counted_as_evidence") is False
        and package.get("proposal_allowed") is False
    )
    readiness_blocks_csh = (
        readiness.get("source_higgs_launch_ready") is False
        and readiness.get("operator_certificate_present") is False
        and readiness.get("future_rows_present") is False
        and readiness.get("taste_radial_rows_are_c_sx_c_xx_not_c_sH_c_HH") is True
        and readiness.get("taste_radial_rows_lack_canonical_oh_identity") is True
    )
    time_kernel_support_only = (
        gevp.get("proposal_allowed") is False
        and gevp.get("physical_pole_extraction_accepted") is False
        and gevp.get("blockers", {}).get("production_time_kernel_rows_absent") is True
    )
    strict_lsz_boundary = (
        lsz.get("strict_scalar_lsz_moment_fv_authority_gate_passed") is True
        and lsz.get("strict_scalar_lsz_moment_fv_authority_present") is False
        and lsz.get("proposal_allowed") is False
    )
    builder_rows_absent = (
        builder.get("input_present") is False
        and builder.get("candidate_written") is False
        and builder.get("proposal_allowed") is False
    )
    gram_not_passed = (
        gram.get("source_higgs_gram_purity_gate_passed") is False
        and gram.get("proposal_allowed") is False
    )
    wz_fallback_still_open = wz.get("proposal_allowed") is False and (
        "not closed" in status(wz) or "exact negative boundary" in status(wz)
    )
    campaign_denies_proposal = campaign.get("proposal_allowed") is False
    closure_future_artifacts_absent = not any(
        value for name, value in futures.items() if name != "two_source_combined_rows"
    )
    two_source_combined_rows_support_only = (
        futures.get("two_source_combined_rows") is True
        and ready_chunks == expected_chunks == 63
        and combiner.get("combined_rows_written") is True
    )
    firewall_clean = not any(FORBIDDEN_FIREWALL.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("canonical-OH-hard-residual-still-open", hard_residual_currently_open, status(hard))
    report("direct-source-Higgs-contract-support-only", direct_contract_support_only, status(direct))
    report(
        "two-source-ready-prefix-current",
        two_source_rows_are_current_prefix,
        f"ready={first_ready}-{last_ready}/{expected_chunks}",
    )
    report(
        "two-source-combiner-boundary-preserved",
        two_source_combiner_boundary,
        f"combined={combiner.get('combined_rows_written')} missing_head={missing_indices[:5] if isinstance(missing_indices, list) else missing_indices}",
    )
    report("chunk-package-pass-support-only", package_passed_support_only, status(package))
    report("source-Higgs-production-readiness-blocks-C_sH", readiness_blocks_csh, status(readiness))
    report("time-kernel-GEVP-contract-support-only", time_kernel_support_only, status(gevp))
    report("strict-scalar-LSZ-FV-boundary-active", strict_lsz_boundary, status(lsz))
    report("source-Higgs-builder-has-no-rows", builder_rows_absent, status(builder))
    report("source-Higgs-Gram-purity-not-passed", gram_not_passed, status(gram))
    report("WZ-fallback-still-open-after-block08", wz_fallback_still_open, status(wz))
    report("campaign-status-denies-proposal", campaign_denies_proposal, status(campaign))
    report("two-source-combined-rows-support-only", two_source_combined_rows_support_only, f"future_presence={futures}")
    report("closure-future-artifact-files-absent", closure_future_artifacts_absent, f"future_presence={futures}")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("aperture-open-gates-recorded", len(open_gates) >= 5, f"open_gates={open_gates}")
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "bounded-support / source-Higgs bridge aperture checkpoint; "
            f"{ready_chunks} completed C_sx/C_xx chunks do not close canonical O_H or "
            "C_sH/C_HH Gram flatness"
        ),
        "conditional_surface_status": (
            "exact support if a future same-surface canonical O_H certificate, "
            "production C_ss/C_sH/C_HH pole rows, complete row/FV/IR authority, "
            "and Gram flatness land without forbidden imports"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current aperture has useful two-source taste-radial staging "
            "rows and source-Higgs contracts, but canonical O_H, production "
            "C_sH/C_HH pole rows, strict scalar LSZ/FV/IR authority, and Gram "
            "flatness are absent.  The complete 63/63 two-source packet is "
            "finite C_sx/C_xx support only."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "source_higgs_bridge_aperture_checkpoint_passed": passed,
        "current_surface_closure_satisfied": False,
        "two_source_rows": {
            "expected_chunks": combiner.get("expected_chunks"),
            "present_chunks": combiner.get("present_chunks"),
            "ready_chunks": combiner.get("ready_chunks"),
            "ready_chunk_indices": ready_indices,
            "missing_chunk_indices": missing_indices,
            "combined_rows_written": combiner.get("combined_rows_written"),
            "strict_limit": (
                "These are two-source taste-radial C_sx/C_xx rows. They are "
                "not canonical-Higgs C_sH/C_HH pole rows before O_H is certified."
            ),
        },
        "source_higgs_aperture_table": aperture,
        "open_aperture_gates": open_gates,
        "future_artifact_presence": futures,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not touch or relaunch the live chunk worker",
            "does not relabel C_sx/C_xx as C_sH/C_HH before canonical O_H",
            "does not set kappa_s, c2, Z_match, or any overlap to one",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, or u0",
            "does not treat time-kernel smoke rows or finite raw C_ss rows as pole/FV/IR authority",
            "does not treat the W/Z fallback as closed after block08",
        ],
        "exact_next_action": (
            "Continue only through a real missing artifact: same-surface "
            "canonical O_H plus production C_ss/C_sH/C_HH pole rows with Gram "
            "flatness, a neutral primitive/rank-one authority theorem, or W/Z "
            "physical-response rows with accepted action, sector-overlap, "
            f"matched covariance, and strict non-observed g2.  Existing {ready_chunks}/63 "
            "C_sx/C_xx rows are bounded source-Higgs staging evidence only."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
