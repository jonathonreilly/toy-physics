#!/usr/bin/env python3
"""
PR #230 post-chunks001-002 source-Higgs bridge intake guard.

The PR branch now contains completed higher-shell Schur/scalar-LSZ chunks001
and 002.  This runner consumes those completed artifacts and checks whether
they change the lane-1 source-Higgs bridge state.  Expected verdict: no.  The
rows are useful partial C_ss/C_sx/C_xx taste-radial support, but they are not a
canonical O_H certificate, not strict C_sH/C_HH pole rows, not scalar LSZ/FV/IR
authority, and not retained-route top-Yukawa closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_post_chunks001_002_source_higgs_bridge_intake_guard_2026-05-12.json"
)

CHUNK_ROW_ROOT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_rows"
EXPECTED_CHUNKS = [1, 2]
EXPECTED_MODES = {
    "0,0,0",
    "1,0,0",
    "0,1,0",
    "0,0,1",
    "1,1,0",
    "1,0,1",
    "0,1,1",
    "1,1,1",
    "2,0,0",
    "0,2,0",
    "0,0,2",
}

PARENTS = {
    "chunk001_checkpoint": "outputs/yt_pr230_schur_higher_shell_chunk001_checkpoint_2026-05-12.json",
    "chunk002_checkpoint": "outputs/yt_pr230_schur_higher_shell_chunk002_checkpoint_2026-05-12.json",
    "wave_launcher": "outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json",
    "operator_certificate_boundary": "outputs/yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_pole_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_gram_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "physical_euclidean_source_higgs_absence": "outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_taste_radial_x_as_canonical_oh": False,
    "treated_c_sx_c_xx_aliases_as_strict_c_sh_c_hh": False,
    "treated_partial_higher_shell_prefix_as_complete_packet": False,
    "treated_finite_momentum_rows_as_pole_residue_rows": False,
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


def load(rel: str | Path) -> dict[str, Any]:
    path = Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def chunk_row_path(index: int) -> Path:
    return (
        CHUNK_ROW_ROOT
        / f"yt_pr230_schur_higher_shell_rows_L12_T24_chunk{index:03d}_2026-05-07.json"
    )


def first_ensemble(row: dict[str, Any]) -> dict[str, Any]:
    ensembles = row.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def mode_keys(obj: Any) -> set[str]:
    if isinstance(obj, dict):
        return {str(key) for key in obj.keys()}
    if isinstance(obj, list):
        keys: set[str] = set()
        for row in obj:
            if isinstance(row, dict) and "mode" in row:
                keys.add(str(row["mode"]))
        return keys
    return set()


def row_bridge_summary(path: Path) -> dict[str, Any]:
    row = load(path)
    ensemble = first_ensemble(row)
    cross = ensemble.get("source_higgs_cross_correlator_analysis", {})
    scalar_lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    time_kernel = ensemble.get("source_higgs_time_kernel_analysis", {})
    wz_response = ensemble.get("wz_mass_response_analysis", {})
    aliases = cross.get("two_source_taste_radial_row_aliases", {}) if isinstance(cross, dict) else {}
    firewall = cross.get("firewall", {}) if isinstance(cross, dict) else {}
    cross_modes = mode_keys(cross.get("mode_rows", {}) if isinstance(cross, dict) else {})
    scalar_modes = mode_keys(scalar_lsz.get("mode_rows", {}) if isinstance(scalar_lsz, dict) else {})
    return {
        "path": str(path.relative_to(ROOT)),
        "present": bool(row),
        "ensemble_present": bool(ensemble),
        "cross_modes_count": len(cross_modes),
        "scalar_modes_count": len(scalar_modes),
        "expected_cross_modes_present": cross_modes == EXPECTED_MODES,
        "expected_scalar_modes_present": scalar_modes == EXPECTED_MODES,
        "canonical_higgs_operator_identity_passed": cross.get(
            "canonical_higgs_operator_identity_passed"
        )
        if isinstance(cross, dict)
        else None,
        "used_as_physical_yukawa_readout": cross.get("used_as_physical_yukawa_readout")
        if isinstance(cross, dict)
        else None,
        "pole_residue_rows_count": len(cross.get("pole_residue_rows", []))
        if isinstance(cross, dict) and isinstance(cross.get("pole_residue_rows"), list)
        else None,
        "aliases_available": aliases.get("available"),
        "c_sx_aliases_c_sh": aliases.get("C_sx_aliases_C_sH_schema_field"),
        "c_xx_aliases_c_hh": aliases.get("C_xx_aliases_C_HH_schema_field"),
        "source_operator_symbol": aliases.get("source_operator_symbol"),
        "scalar_lsz_physical_higgs_normalization": scalar_lsz.get(
            "physical_higgs_normalization"
        )
        if isinstance(scalar_lsz, dict)
        else None,
        "scalar_lsz_used_as_physical_yukawa_readout": scalar_lsz.get(
            "used_as_physical_yukawa_readout"
        )
        if isinstance(scalar_lsz, dict)
        else None,
        "time_kernel_mode_count": len(mode_keys(time_kernel.get("mode_rows", {})))
        if isinstance(time_kernel, dict)
        else None,
        "time_kernel_physical_higgs_normalization": time_kernel.get(
            "physical_higgs_normalization"
        )
        if isinstance(time_kernel, dict)
        else None,
        "wz_response_phase": wz_response.get("phase") if isinstance(wz_response, dict) else None,
        "firewall_clean": all(value is False for value in firewall.values())
        if isinstance(firewall, dict)
        else False,
    }


def main() -> int:
    print("PR #230 post-chunks001-002 source-Higgs bridge intake guard")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    failing_parents = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    row_summaries = {index: row_bridge_summary(chunk_row_path(index)) for index in EXPECTED_CHUNKS}
    chunk_certs = [certs[f"chunk{index:03d}_checkpoint"] for index in EXPECTED_CHUNKS]
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    chunks_checkpointed = all(
        cert.get("chunk_index") == index
        and cert.get("completed") is True
        and cert.get("checkpoint_passed") is True
        and cert.get("proposal_allowed") is False
        and cert.get("bare_retained_allowed") is False
        for index, cert in zip(EXPECTED_CHUNKS, chunk_certs)
    )
    wave_records_prefix_without_promotion = (
        certs["wave_launcher"].get("wave_launcher_passed") is True
        and certs["wave_launcher"].get("proposal_allowed") is False
        and certs["wave_launcher"].get("completed_chunk_indices") == EXPECTED_CHUNKS
        and all(
            index not in EXPECTED_CHUNKS
            for index in certs["wave_launcher"].get("active_chunk_indices", [])
        )
        and all(
            index in certs["wave_launcher"].get("active_or_completed_chunk_indices", [])
            for index in EXPECTED_CHUNKS
        )
        and "run-control" in statuses["wave_launcher"]
    )
    row_files_present = all(summary["present"] and summary["ensemble_present"] for summary in row_summaries.values())
    row_modes_expected = all(
        summary["expected_cross_modes_present"] and summary["expected_scalar_modes_present"]
        for summary in row_summaries.values()
    )
    rows_are_taste_radial_alias_support = all(
        summary["canonical_higgs_operator_identity_passed"] is False
        and summary["used_as_physical_yukawa_readout"] is False
        and summary["aliases_available"] is True
        and summary["c_sx_aliases_c_sh"] is True
        and summary["c_xx_aliases_c_hh"] is True
        and summary["source_operator_symbol"] == "x"
        and summary["firewall_clean"] is True
        for summary in row_summaries.values()
    )
    no_pole_or_time_kernel_authority = all(
        summary["pole_residue_rows_count"] == 0
        and summary["scalar_lsz_physical_higgs_normalization"] == "not_derived"
        and summary["scalar_lsz_used_as_physical_yukawa_readout"] is False
        and summary["time_kernel_mode_count"] == 0
        and summary["time_kernel_physical_higgs_normalization"] == "not_derived"
        for summary in row_summaries.values()
    )
    wz_disabled = all(summary["wz_response_phase"] == "disabled" for summary in row_summaries.values())
    operator_boundary_still_blocks = (
        "taste-radial second-source certificate, not canonical O_H"
        in statuses["operator_certificate_boundary"]
        and certs["operator_certificate_boundary"].get("proposal_allowed") is False
        and certs["operator_certificate_boundary"].get(
            "higher_shell_source_higgs_operator_certificate_boundary_passed"
        )
        is True
    )
    source_higgs_readiness_still_blocks = (
        "source-Higgs production launch blocked by missing O_H certificate"
        in statuses["source_higgs_readiness"]
        and certs["source_higgs_readiness"].get("operator_certificate_present") is False
        and certs["source_higgs_readiness"].get("future_rows_present") is False
        and certs["source_higgs_readiness"].get("proposal_allowed") is False
    )
    pole_and_gram_still_wait = (
        (
            "awaiting valid production rows" in statuses["source_higgs_pole_extractor"]
            or "awaiting production certificate" in statuses["source_higgs_pole_extractor"]
        )
        and "awaiting production certificate" in statuses["source_higgs_gram_postprocess"]
        and certs["source_higgs_pole_extractor"].get("gate_passed") is False
        and certs["source_higgs_gram_postprocess"].get("candidate_present") is False
    )
    physical_euclidean_absence_still_blocks = (
        (
            "tau-keyed production correlators are not physical Euclidean source-Higgs"
            in statuses["physical_euclidean_source_higgs_absence"]
        )
        and certs["physical_euclidean_source_higgs_absence"].get("proposal_allowed") is False
        and certs["physical_euclidean_source_higgs_absence"].get(
            "physical_euclidean_source_higgs_row_absence_passed"
        )
        is True
    )
    aggregate_gates_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
        and "not passed" in statuses["full_positive_assembly"]
        and "active campaign continuing" in statuses["campaign_status"]
    )

    guard_passed = all(
        [
            not missing_parents,
            not failing_parents,
            not proposal_parents,
            chunks_checkpointed,
            wave_records_prefix_without_promotion,
            row_files_present,
            row_modes_expected,
            rows_are_taste_radial_alias_support,
            no_pole_or_time_kernel_authority,
            wz_disabled,
            operator_boundary_still_blocks,
            source_higgs_readiness_still_blocks,
            pole_and_gram_still_wait,
            physical_euclidean_absence_still_blocks,
            aggregate_gates_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("chunks001-002-checkpointed-support-only", chunks_checkpointed, str([status(cert) for cert in chunk_certs]))
    report("wave-launcher-records-prefix-without-promotion", wave_records_prefix_without_promotion, statuses["wave_launcher"])
    report("completed-row-files-present", row_files_present, str([summary["path"] for summary in row_summaries.values()]))
    report("completed-rows-have-expected-mode-support", row_modes_expected, str(row_summaries))
    report("rows-are-taste-radial-alias-support", rows_are_taste_radial_alias_support, "C_sx/C_xx aliases under x")
    report("no-pole-or-time-kernel-authority", no_pole_or_time_kernel_authority, "pole rows empty; time kernel disabled")
    report("wz-response-disabled-in-prefix", wz_disabled, "W/Z phase disabled")
    report("operator-boundary-still-blocks", operator_boundary_still_blocks, statuses["operator_certificate_boundary"])
    report("source-higgs-readiness-still-blocks", source_higgs_readiness_still_blocks, statuses["source_higgs_readiness"])
    report("pole-and-gram-still-wait", pole_and_gram_still_wait, f"{statuses['source_higgs_pole_extractor']} / {statuses['source_higgs_gram_postprocess']}")
    report("physical-euclidean-absence-still-blocks", physical_euclidean_absence_still_blocks, statuses["physical_euclidean_source_higgs_absence"])
    report("aggregate-gates-still-open", aggregate_gates_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("post-chunks001-002-not-source-higgs-bridge", guard_passed, "partial prefix support is not O_H/C_sH/C_HH closure")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / completed higher-shell chunks001-002 are "
            "partial taste-radial C_sx/C_xx support, not PR230 source-Higgs "
            "bridge closure"
        ),
        "conditional_surface_status": (
            "conditional-support only if a future canonical O_H/source-overlap "
            "certificate and production C_ss/C_sH/C_HH(tau) pole rows with "
            "Gram/FV/IR authority land"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Chunks001-002 are completed bounded support rows under the "
            "taste-radial second-source certificate.  They do not identify x "
            "with canonical O_H, do not supply pole residues or a time kernel, "
            "do not derive scalar LSZ/FV/IR authority, and do not enable the "
            "full positive closure or campaign gates."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "post_chunks001_002_source_higgs_bridge_intake_guard_passed": guard_passed,
        "chunk_indices": EXPECTED_CHUNKS,
        "row_summaries": row_summaries,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "open_imports": [
            "canonical O_H/source-overlap certificate",
            "production C_ss/C_sH/C_HH(tau) source-Higgs pole rows",
            "source-Higgs pole residues and Gram purity",
            "scalar LSZ/FV/IR/model-class authority",
            "complete higher-shell packet and downstream monotonicity/threshold checks, if pursuing the Schur route",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat chunks001-002 as a complete higher-shell packet",
            "does not treat C_sx/C_xx aliases as canonical C_sH/C_HH",
            "does not treat finite-momentum rows as pole-residue rows",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Continue accumulating higher-shell chunks as support, but do not "
            "reopen source-Higgs closure until canonical O_H/source-overlap "
            "authority and strict physical Euclidean C_ss/C_sH/C_HH(tau) pole "
            "rows are present."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and guard_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
