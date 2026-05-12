#!/usr/bin/env python3
"""
PR #230 MC target-timeseries Krylov/transfer no-go after Block43.

The complete FH-LSZ target-timeseries packet stores per-configuration Monte
Carlo samples.  Those samples are useful for source-coordinate statistics and
autocorrelation/ESS checks, but their ordering is not Euclidean operator time.
This runner blocks the shortcut that tries to reconstruct an OS transfer
kernel, Krylov/Lanczos neutral generator, or source-Higgs pole row from the
MC trajectory index of C_ss samples.
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
    / "yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json"
)

EXPECTED_CHUNKS = 63
EXPECTED_CONFIGS = 16
EXPECTED_MODES = {"0,0,0", "0,0,1", "0,1,0", "1,0,0"}

PARENTS = {
    "target_timeseries_full_set": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "full_timeseries_neutral_transfer_lift_no_go": "outputs/yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json",
    "target_timeseries_higgs_identity_no_go": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
    "autocorrelation_ess": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_mc_configuration_index_as_euclidean_time": False,
    "treated_mc_autocorrelation_as_os_transfer": False,
    "treated_c_ss_timeseries_as_c_sH_or_c_HH": False,
    "treated_target_dE_ds_as_dE_dh": False,
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
    return (
        ROOT
        / "outputs"
        / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"
    )


def mode_rows(index: int) -> dict[str, Any]:
    data = json.loads(chunk_path(index).read_text(encoding="utf-8"))
    ensemble = data.get("ensembles", [{}])[0]
    return (
        ensemble.get("scalar_two_point_lsz_analysis", {})
        .get("mode_rows", {})
    )


def chunk_schema(index: int) -> dict[str, Any]:
    rows = mode_rows(index)
    mode_keys = set(rows) if isinstance(rows, dict) else set()
    forbidden_euclidean_keys = {
        "tau",
        "t",
        "time_separation",
        "euclidean_time",
        "source_time",
        "sink_time",
        "C_sH_timeseries",
        "C_HH_timeseries",
        "transfer_kernel",
        "krylov_basis",
        "lanczos_tridiagonal",
    }
    present_forbidden: dict[str, list[str]] = {}
    lengths: dict[str, int] = {}
    configuration_indices: dict[str, list[int]] = {}
    for mode, row in rows.items():
        if not isinstance(row, dict):
            continue
        series = row.get("C_ss_timeseries", [])
        lengths[mode] = len(series)
        indices = [
            int(sample.get("configuration_index"))
            for sample in series
            if isinstance(sample, dict) and "configuration_index" in sample
        ]
        configuration_indices[mode] = indices
        hits = sorted(key for key in forbidden_euclidean_keys if key in row)
        for sample in series:
            if isinstance(sample, dict):
                hits.extend(
                    f"C_ss_timeseries[].{key}"
                    for key in forbidden_euclidean_keys
                    if key in sample
                )
        if hits:
            present_forbidden[mode] = sorted(set(hits))
    return {
        "chunk": index,
        "mode_keys": sorted(mode_keys),
        "has_expected_modes": mode_keys == EXPECTED_MODES,
        "lengths": lengths,
        "all_lengths_expected": all(length == EXPECTED_CONFIGS for length in lengths.values()),
        "configuration_indices": configuration_indices,
        "indices_are_configuration_order": all(
            indices == list(range(EXPECTED_CONFIGS))
            for indices in configuration_indices.values()
        ),
        "present_forbidden_euclidean_keys": present_forbidden,
    }


def lag1_covariance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return sum((a - mean) * (b - mean) for a, b in zip(values, values[1:])) / (len(values) - 1)


def variance(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def permutation_witness() -> dict[str, Any]:
    rows = mode_rows(1)
    series = rows["0,0,0"]["C_ss_timeseries"]
    values = [float(sample["C_ss_real"]) for sample in series]
    reversed_values = list(reversed(values))
    sorted_values = sorted(values)
    original_summary = {
        "mean": sum(values) / len(values),
        "variance": variance(values),
        "lag1_covariance": lag1_covariance(values),
    }
    reversed_summary = {
        "mean": sum(reversed_values) / len(reversed_values),
        "variance": variance(reversed_values),
        "lag1_covariance": lag1_covariance(reversed_values),
    }
    sorted_summary = {
        "mean": sum(sorted_values) / len(sorted_values),
        "variance": variance(sorted_values),
        "lag1_covariance": lag1_covariance(sorted_values),
    }
    return {
        "chunk": 1,
        "mode": "0,0,0",
        "same_multiset_transforms": ["reverse_configuration_order", "sort_configuration_order"],
        "original": original_summary,
        "reversed": reversed_summary,
        "sorted": sorted_summary,
        "ensemble_mean_preserved_by_permutation": math.isclose(
            original_summary["mean"], reversed_summary["mean"], rel_tol=0.0, abs_tol=1.0e-15
        )
        and math.isclose(
            original_summary["mean"], sorted_summary["mean"], rel_tol=0.0, abs_tol=1.0e-15
        ),
        "ensemble_variance_preserved_by_permutation": math.isclose(
            original_summary["variance"],
            reversed_summary["variance"],
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
        and math.isclose(
            original_summary["variance"],
            sorted_summary["variance"],
            rel_tol=0.0,
            abs_tol=1.0e-15,
        ),
        "lag1_covariance_changes_under_permutation": (
            abs(original_summary["lag1_covariance"] - sorted_summary["lag1_covariance"])
            > 1.0e-8
        ),
        "interpretation": (
            "MC configuration order is run-control metadata.  A physical OS "
            "transfer or Krylov generator cannot depend on whether the same "
            "ensemble samples are reversed or sorted."
        ),
    }


def main() -> int:
    print("PR #230 MC target-timeseries Krylov/transfer no-go after Block43")
    print("=" * 84)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    failing_parents = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    missing_chunks = [i for i in range(1, EXPECTED_CHUNKS + 1) if not chunk_path(i).exists()]
    schemas = [chunk_schema(i) for i in range(1, EXPECTED_CHUNKS + 1) if chunk_path(i).exists()]
    bad_modes = [row["chunk"] for row in schemas if not row["has_expected_modes"]]
    bad_lengths = [row["chunk"] for row in schemas if not row["all_lengths_expected"]]
    bad_indices = [row["chunk"] for row in schemas if not row["indices_are_configuration_order"]]
    forbidden_euclidean = [
        row["chunk"] for row in schemas if row["present_forbidden_euclidean_keys"]
    ]

    block43_loaded = (
        "full FH-LSZ target-timeseries packet does not lift PR230"
        in statuses["full_timeseries_neutral_transfer_lift_no_go"]
        and certs["full_timeseries_neutral_transfer_lift_no_go"].get(
            "full_timeseries_neutral_transfer_lift_no_go_passed"
        )
        is True
        and certs["full_timeseries_neutral_transfer_lift_no_go"].get(
            "proposal_allowed"
        )
        is False
    )
    os_transfer_absent = (
        "OS transfer-kernel artifact absent" in statuses["os_transfer_kernel_artifact_gate"]
        and certs["os_transfer_kernel_artifact_gate"].get("proposal_allowed") is False
    )
    neutral_gate_rejects = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in statuses["same_surface_neutral_multiplicity_one_gate"]
        and certs["same_surface_neutral_multiplicity_one_gate"].get(
            "candidate_accepted"
        )
        is False
        and certs["same_surface_neutral_multiplicity_one_gate"].get(
            "proposal_allowed"
        )
        is False
    )
    autocorrelation_is_run_control = (
        "autocorrelation ESS gate passed for target observables"
        in statuses["autocorrelation_ess"]
        and certs["autocorrelation_ess"].get("proposal_allowed") is False
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    witness = permutation_witness()
    permutation_blocks_transfer = (
        witness["ensemble_mean_preserved_by_permutation"]
        and witness["ensemble_variance_preserved_by_permutation"]
        and witness["lag1_covariance_changes_under_permutation"]
    )
    schema_is_mc_not_euclidean = (
        not missing_chunks
        and not bad_modes
        and not bad_lengths
        and not bad_indices
        and not forbidden_euclidean
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    no_go_passed = all(
        [
            not missing_parents,
            not failing_parents,
            not proposal_parents,
            block43_loaded,
            os_transfer_absent,
            neutral_gate_rejects,
            autocorrelation_is_run_control,
            schema_is_mc_not_euclidean,
            permutation_blocks_transfer,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block43-boundary-loaded", block43_loaded, statuses["full_timeseries_neutral_transfer_lift_no_go"])
    report("os-transfer-artifact-still-absent", os_transfer_absent, statuses["os_transfer_kernel_artifact_gate"])
    report("neutral-multiplicity-gate-rejects-current-surface", neutral_gate_rejects, statuses["same_surface_neutral_multiplicity_one_gate"])
    report("autocorrelation-ess-is-run-control-support", autocorrelation_is_run_control, statuses["autocorrelation_ess"])
    report("all-production-chunks-present", not missing_chunks, f"missing={missing_chunks[:10]}")
    report("timeseries-schema-has-expected-source-modes", not bad_modes, f"bad_modes={bad_modes[:10]}")
    report("timeseries-schema-has-expected-config-count", not bad_lengths, f"bad_lengths={bad_lengths[:10]}")
    report("timeseries-index-is-configuration-order", not bad_indices, f"bad_indices={bad_indices[:10]}")
    report("timeseries-schema-has-no-euclidean-transfer-keys", not forbidden_euclidean, f"chunks={forbidden_euclidean[:10]}")
    report("permutation-preserves-ensemble-statistics", witness["ensemble_mean_preserved_by_permutation"] and witness["ensemble_variance_preserved_by_permutation"], str(witness))
    report("permutation-changes-lag-autocovariance", witness["lag1_covariance_changes_under_permutation"], str(witness))
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("mc-timeseries-krylov-transfer-no-go", no_go_passed, "MC order is not Euclidean transfer evidence")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / MC target time series are not a "
            "same-surface OS transfer, Krylov generator, or neutral O_H bridge"
        ),
        "conditional_surface_status": (
            "conditional-support if future production supplies Euclidean "
            "C_ss(tau), C_sH(tau), C_HH(tau) pole rows or a same-surface "
            "neutral transfer/off-diagonal generator independent of MC "
            "configuration ordering"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The available target time series are MC configuration samples.  "
            "Their order is run-control metadata, not Euclidean operator time.  "
            "A permutation preserves ensemble source statistics but changes "
            "lag-one autocovariance, so no physical transfer generator or "
            "Krylov neutral bridge can be inferred from this order."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "mc_timeseries_krylov_transfer_no_go_passed": no_go_passed,
        "schema_summary": {
            "checked_chunks": len(schemas),
            "missing_chunks": missing_chunks,
            "bad_mode_chunks": bad_modes,
            "bad_length_chunks": bad_lengths,
            "bad_configuration_index_chunks": bad_indices,
            "chunks_with_forbidden_euclidean_transfer_keys": forbidden_euclidean,
            "expected_modes": sorted(EXPECTED_MODES),
            "expected_configurations_per_mode": EXPECTED_CONFIGS,
        },
        "permutation_witness": witness,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "open_imports": [
            "Euclidean time-separation correlation matrix C_ij(tau)",
            "same-surface neutral transfer/off-diagonal generator",
            "canonical-Higgs operator authority",
            "strict C_sH/C_HH pole rows with scalar-LSZ/FV/IR control",
        ],
        "exact_next_action": (
            "Do not use MC configuration-index time series for Krylov or OS "
            "transfer reconstruction.  A positive route must add physical "
            "Euclidean-time correlation rows or an explicit same-surface "
            "neutral transfer/off-diagonal generator."
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
