#!/usr/bin/env python3
"""
PR #230 full target-timeseries neutral-transfer lift no-go after Block42.

The chunk worker has now supplied a complete L12 target-timeseries packet.
This runner tests whether that new time-direction support upgrades the top
remaining non-chunk route: same-surface neutral transfer / H3-H4 closure.

It does not.  The full packet is source-coordinate target support: per-chunk
dE/ds target rows and scalar C_ss/Gamma_ss time series for source-source
operators.  It still contains no same-surface neutral transfer operator,
source-to-triplet off-diagonal generator, C_sH/C_HH pole rows, primitive-cone
certificate, or canonical-Higgs coupling authority.  A neutral completion can
preserve every current source-source time series while rotating an unmeasured
orthogonal neutral scalar into the would-be Higgs readout.
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
    / "yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json"
)

EXPECTED_CHUNKS = 63
EXPECTED_CONFIGS = 16
EXPECTED_MODES = {"0,0,0", "0,0,1", "0,1,0", "1,0,0"}

PARENTS = {
    "target_timeseries_full_set": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "target_timeseries_higgs_identity_no_go": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
    "neutral_rank_one_bypass_post_block37": "outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
    "neutral_transfer_eigenoperator_source_mixing_no_go": "outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "two_source_taste_radial_primitive_transfer_candidate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_ARTIFACTS = {
    "same_surface_neutral_transfer_operator": "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_scalar_rank_one_purity_certificate": "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-03.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_c_ss_timeseries_as_c_sH_or_c_HH": False,
    "treated_target_dE_ds_as_dE_dh": False,
    "treated_source_timeseries_as_neutral_transfer": False,
    "treated_finite_source_autocorrelation_as_primitive_cone": False,
    "set_kappa_s_c2_zmatch_g2_or_overlap_to_one": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def chunk_neutral_schema(index: int) -> dict[str, Any]:
    data = json.loads(chunk_path(index).read_text(encoding="utf-8"))
    ensemble = data.get("ensembles", [{}])[0]
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {})
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()

    forbidden_row_keys = {
        "C_sx_timeseries",
        "C_xx_timeseries",
        "C_sH_timeseries",
        "C_HH_timeseries",
        "neutral_transfer_matrix",
        "offdiagonal_generator",
        "primitive_cone_certificate",
    }
    present_forbidden: dict[str, list[str]] = {}
    mode_lengths: dict[str, int] = {}
    for mode, row in mode_rows.items():
        if not isinstance(row, dict):
            continue
        mode_lengths[mode] = len(row.get("C_ss_timeseries", []))
        hits = sorted(key for key in forbidden_row_keys if key in row)
        if hits:
            present_forbidden[mode] = hits

    source_strict_limit = str(source.get("strict_limit", ""))
    return {
        "chunk": index,
        "mode_keys": sorted(mode_keys),
        "mode_lengths": mode_lengths,
        "has_only_expected_source_modes": mode_keys == EXPECTED_MODES,
        "all_mode_lengths_expected": all(
            length == EXPECTED_CONFIGS for length in mode_lengths.values()
        ),
        "present_forbidden_neutral_keys": present_forbidden,
        "source_physical_higgs_normalization": source.get("physical_higgs_normalization"),
        "source_strict_limit": source_strict_limit,
        "source_strict_limit_blocks_h_readout": "not dE/dh" in source_strict_limit,
    }


def source_timeseries_counterfamily() -> list[dict[str, Any]]:
    css_values = [1.0, 0.42, 0.18, 0.08]
    rows: list[dict[str, Any]] = []
    for label, theta in (
        ("pure_source_axis", 0.0),
        ("mixed_30deg", math.pi / 6.0),
        ("mixed_60deg", math.pi / 3.0),
        ("orthogonal_higgs_axis", math.pi / 2.0),
    ):
        c = math.cos(theta)
        s = math.sin(theta)
        rows.append(
            {
                "case": label,
                "basis": ["source_pole_s", "unmeasured_orthogonal_neutral_n"],
                "observed_C_ss_timeseries": css_values,
                "unmeasured_completion": {
                    "C_sn_timeseries": [0.0 for _ in css_values],
                    "C_nn_timeseries": css_values,
                    "H_theta": [c, s],
                },
                "candidate_C_sH_timeseries": [c * value for value in css_values],
                "candidate_C_HH_timeseries": [
                    c * c * value + s * s * value for value in css_values
                ],
                "observed_source_timeseries_change": False,
                "candidate_source_higgs_overlap_scale": c,
                "neutral_transfer_or_offdiagonal_generator_supplied": False,
            }
        )
    return rows


def main() -> int:
    print("PR #230 full target-timeseries neutral-transfer lift no-go after Block42")
    print("=" * 88)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    failing = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {
        name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ARTIFACTS.items()
    }

    full_packet_complete_support = (
        "FH-LSZ full L12 target-timeseries packet checkpoint"
        in statuses["target_timeseries_full_set"]
        and certs["target_timeseries_full_set"].get("proposal_allowed") is False
        and certs["target_timeseries_full_set"].get("pass_count") == 9
        and certs["target_timeseries_full_set"].get("fail_count") == 0
        and certs["target_timeseries_full_set"]
        .get("target_timeseries_summary", {})
        .get("complete_for_all_ready_chunks")
        is True
    )
    target_higgs_identity_no_go_blocks = (
        "FH-LSZ target time series not canonical-Higgs identity"
        in statuses["target_timeseries_higgs_identity_no_go"]
        and certs["target_timeseries_higgs_identity_no_go"].get("proposal_allowed")
        is False
        and certs["target_timeseries_higgs_identity_no_go"].get(
            "target_timeseries_higgs_identity_gate_passed"
        )
        is False
        and certs["target_timeseries_higgs_identity_no_go"].get("fail_count") == 0
    )
    neutral_parent_boundaries_apply = (
        certs["neutral_rank_one_bypass_post_block37"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["neutral_h3h4_aperture"].get(
            "neutral_primitive_h3h4_aperture_checkpoint_passed"
        )
        is True
        and certs["neutral_h3h4_aperture"].get(
            "h3_physical_transfer_or_offdiagonal_generator_absent"
        )
        is True
        and certs["neutral_h3h4_aperture"].get(
            "h4_source_canonical_higgs_coupling_absent"
        )
        is True
        and "current same-surface Z3 eigenoperator data do not certify"
        in statuses["neutral_transfer_eigenoperator_source_mixing_no_go"]
        and certs["neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
        and certs["same_surface_neutral_multiplicity_one_gate"].get(
            "candidate_accepted"
        )
        is False
        and certs["two_source_taste_radial_primitive_transfer_candidate"].get(
            "physical_transfer_candidate_accepted"
        )
        is False
    )
    os_transfer_boundary_applies = (
        "OS transfer-kernel artifact absent"
        in statuses["os_transfer_kernel_artifact_gate"]
        and certs["os_transfer_kernel_artifact_gate"].get("proposal_allowed") is False
    )

    missing_chunks = [i for i in range(1, EXPECTED_CHUNKS + 1) if not chunk_path(i).exists()]
    schema_rows = [
        chunk_neutral_schema(i)
        for i in range(1, EXPECTED_CHUNKS + 1)
        if chunk_path(i).exists()
    ]
    bad_modes = [
        row["chunk"]
        for row in schema_rows
        if not row["has_only_expected_source_modes"] or not row["all_mode_lengths_expected"]
    ]
    chunks_with_forbidden_neutral_keys = [
        row["chunk"] for row in schema_rows if row["present_forbidden_neutral_keys"]
    ]
    source_limits_block_h_readout = all(
        row["source_strict_limit_blocks_h_readout"] for row in schema_rows
    )
    source_higgs_normalization_absent = all(
        row["source_physical_higgs_normalization"] == "not_derived"
        for row in schema_rows
    )
    schema_is_source_only = (
        not missing_chunks
        and not bad_modes
        and not chunks_with_forbidden_neutral_keys
        and source_limits_block_h_readout
        and source_higgs_normalization_absent
    )

    counterfamily = source_timeseries_counterfamily()
    counterfamily_preserves_observed = all(
        row["observed_source_timeseries_change"] is False for row in counterfamily
    )
    overlap_scales = {
        round(float(row["candidate_source_higgs_overlap_scale"]), 12)
        for row in counterfamily
    }
    counterfamily_varies_overlap = len(overlap_scales) > 1
    future_artifacts_absent = not any(future_presence.values())
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    no_go_passed = all(
        [
            not missing,
            not failing,
            not proposal_parents,
            full_packet_complete_support,
            target_higgs_identity_no_go_blocks,
            neutral_parent_boundaries_apply,
            os_transfer_boundary_applies,
            schema_is_source_only,
            counterfamily_preserves_observed,
            counterfamily_varies_overlap,
            future_artifacts_absent,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-certificates-have-no-fails", not failing, f"failing={failing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("full-target-timeseries-support-complete", full_packet_complete_support, statuses["target_timeseries_full_set"])
    report("target-timeseries-higgs-identity-no-go-blocks", target_higgs_identity_no_go_blocks, statuses["target_timeseries_higgs_identity_no_go"])
    report("neutral-parent-boundaries-apply", neutral_parent_boundaries_apply, "H3/H4, rank-one, multiplicity, and primitive gates remain blocked")
    report("os-transfer-boundary-applies", os_transfer_boundary_applies, statuses["os_transfer_kernel_artifact_gate"])
    report("all-production-chunks-present", not missing_chunks, f"missing={missing_chunks[:10]}")
    report("target-schema-has-expected-source-modes", not bad_modes, f"bad_modes={bad_modes[:10]}")
    report("target-schema-has-no-neutral-transfer-keys", not chunks_with_forbidden_neutral_keys, f"chunks={chunks_with_forbidden_neutral_keys[:10]}")
    report("source-strict-limit-blocks-h-readout", source_limits_block_h_readout, "dE/ds is not dE/dh")
    report("physical-higgs-normalization-absent", source_higgs_normalization_absent, "not_derived")
    report("counterfamily-preserves-observed-source-timeseries", counterfamily_preserves_observed, "C_ss(t) unchanged")
    report("counterfamily-varies-source-higgs-overlap", counterfamily_varies_overlap, f"overlap_scales={sorted(overlap_scales)}")
    report("strict-future-neutral-artifacts-absent", future_artifacts_absent, str(future_presence))
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("full-timeseries-neutral-transfer-lift-no-go", no_go_passed, "source-only target timeseries do not supply H3/H4")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / full FH-LSZ target-timeseries packet does "
            "not lift PR230 to a same-surface neutral transfer or O_H bridge"
        ),
        "conditional_surface_status": (
            "conditional-support if future target-time rows include a genuine "
            "same-surface neutral transfer/off-diagonal generator, strict "
            "C_sH/C_HH pole rows, primitive-cone certificate, or canonical-Higgs "
            "coupling authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The completed 63/63 target-timeseries packet is source-coordinate "
            "production support only.  It has C_ss/Gamma_ss and dE/ds target rows, "
            "but no C_sH/C_HH, neutral transfer matrix, off-diagonal generator, "
            "primitive-cone certificate, or canonical-Higgs normalization."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "full_timeseries_neutral_transfer_lift_no_go_passed": no_go_passed,
        "schema_summary": {
            "checked_chunks": len(schema_rows),
            "missing_chunks": missing_chunks,
            "bad_mode_chunks": bad_modes,
            "chunks_with_forbidden_neutral_keys": chunks_with_forbidden_neutral_keys,
            "source_strict_limit_blocks_h_readout": source_limits_block_h_readout,
            "source_physical_higgs_normalization_absent": source_higgs_normalization_absent,
            "expected_modes": sorted(EXPECTED_MODES),
            "expected_configurations_per_mode": EXPECTED_CONFIGS,
        },
        "counterfamily": counterfamily,
        "future_artifact_presence": future_presence,
        "open_imports": [
            "same-surface neutral transfer operator or off-diagonal generator",
            "primitive-cone / irreducibility certificate",
            "canonical-Higgs source coupling or C_sH/C_HH pole rows",
            "scalar LSZ/FV/IR metric linking source target rows to h",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "exact_next_action": (
            "Do not treat the full target-timeseries packet as H3/H4 closure.  "
            "A positive neutral route must add a same-surface transfer/off-"
            "diagonal generator or production C_sH/C_HH rows with canonical-Higgs "
            "authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and no_go_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
