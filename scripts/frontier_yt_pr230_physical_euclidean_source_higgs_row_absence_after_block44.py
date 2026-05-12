#!/usr/bin/env python3
"""
PR #230 physical Euclidean source-Higgs row absence after Block44.

Block44 blocks using MC configuration-index target samples as Euclidean
transfer/Krylov evidence.  This runner closes the adjacent ambiguity: the
production chunk files do contain ordinary tau-keyed top/scalar-source
correlators, but they do not contain physical source-Higgs C_ss/C_sH/C_HH(tau)
rows.  The only C_sH/C_HH(tau) matrix artifact on the current surface is the
reduced smoke harness, which is explicitly support-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json"
)

EXPECTED_CHUNKS = 63

PARENTS = {
    "mc_timeseries_krylov_transfer_no_go": "outputs/yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json",
    "time_kernel_harness": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
    "time_kernel_gevp_contract": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "time_kernel_production_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "direct_source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_cross_correlator_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

SMOKE = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_harness_smoke_numba_2026-05-07.json"
TIME_KERNEL_ROW_ROOTS = [
    ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_rows",
    ROOT / "outputs" / "yt_direct_lattice_correlator_production_source_higgs_time_kernel_rows",
]
SOURCE_HIGGS_ROW_FILES = [
    ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    ROOT / "outputs" / "yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
]

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_top_tau_correlator_as_source_higgs_row": False,
    "treated_scalar_source_tau_fit_as_source_higgs_row": False,
    "treated_reduced_smoke_c_sH_c_HH_as_production": False,
    "treated_c_sx_c_xx_aliases_as_c_sH_c_HH": False,
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


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def has_tau_rows(rows: Any) -> bool:
    return isinstance(rows, list) and bool(rows) and all(
        isinstance(row, dict) and "tau" in row for row in rows[: min(3, len(rows))]
    )


def contains_key(obj: Any, keys: set[str]) -> bool:
    if isinstance(obj, dict):
        return any(key in obj for key in keys) or any(
            contains_key(value, keys) for value in obj.values()
        )
    if isinstance(obj, list):
        return any(contains_key(value, keys) for value in obj)
    return False


def production_chunk_schema(index: int) -> dict[str, Any]:
    path = chunk_path(index)
    if not path.exists():
        return {"chunk": index, "present": False}
    data = load(path)
    ensemble = selected_ensemble(data)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    source_meta = metadata.get("source_higgs_cross_correlator")
    if not isinstance(source_meta, dict):
        source_meta = {}
    source_response = ensemble.get("scalar_source_response_analysis")
    if not isinstance(source_response, dict):
        source_response = {}
    energy_fits = source_response.get("energy_fits")
    if not isinstance(energy_fits, list):
        energy_fits = []
    source_response_tau = any(has_tau_rows(row.get("correlator")) for row in energy_fits if isinstance(row, dict))
    ordinary_tau = has_tau_rows(ensemble.get("correlators"))
    source_higgs_analysis = ensemble.get("source_higgs_cross_correlator_analysis")
    source_higgs_analysis_present = isinstance(source_higgs_analysis, dict)
    source_higgs_analysis_empty_guard = False
    if source_higgs_analysis_present:
        mode_rows = source_higgs_analysis.get("mode_rows")
        pole_rows = source_higgs_analysis.get("pole_residue_rows")
        source_higgs_analysis_empty_guard = (
            isinstance(mode_rows, dict)
            and not mode_rows
            and isinstance(pole_rows, list)
            and not pole_rows
            and source_higgs_analysis.get("source_coordinate") == "disabled"
            and source_higgs_analysis.get("used_as_physical_yukawa_readout") is False
        )
    time_kernel_present = isinstance(ensemble.get("source_higgs_time_kernel_analysis"), dict)
    source_higgs_keys_present = contains_key(
        {
            "source_higgs_cross_correlator_analysis": ensemble.get("source_higgs_cross_correlator_analysis"),
            "source_higgs_time_kernel_analysis": ensemble.get("source_higgs_time_kernel_analysis"),
        },
        {"C_sH", "C_HH", "C_Hs", "C_matrix_real", "tau_rows"},
    )
    return {
        "chunk": index,
        "present": True,
        "ordinary_top_tau_correlator_present": ordinary_tau,
        "scalar_source_tau_correlator_present": source_response_tau,
        "source_higgs_cross_correlator_enabled": source_meta.get("enabled") is True,
        "source_higgs_operator_realization": source_meta.get("canonical_higgs_operator_realization"),
        "source_higgs_cross_correlator_analysis_present": source_higgs_analysis_present,
        "source_higgs_cross_correlator_analysis_empty_guard": source_higgs_analysis_empty_guard,
        "source_higgs_time_kernel_analysis_present": time_kernel_present,
        "source_higgs_strict_tau_keys_present": source_higgs_keys_present,
        "physical_higgs_normalization": ensemble.get("fh_lsz_measurement_policy", {}).get("physical_higgs_normalization"),
    }


def listed_files(root: Path) -> list[str]:
    if not root.exists():
        return []
    if root.is_file():
        return [str(root.relative_to(ROOT))]
    return sorted(str(path.relative_to(ROOT)) for path in root.rglob("*.json"))


def smoke_summary() -> dict[str, Any]:
    smoke = load(SMOKE)
    ensemble = selected_ensemble(smoke)
    metadata = smoke.get("metadata") if isinstance(smoke.get("metadata"), dict) else {}
    analysis = ensemble.get("source_higgs_time_kernel_analysis")
    if not isinstance(analysis, dict):
        analysis = {}
    mode_rows = analysis.get("mode_rows")
    tau_count = 0
    if isinstance(mode_rows, dict):
        for row in mode_rows.values():
            if isinstance(row, dict) and isinstance(row.get("tau_rows"), list):
                tau_count += len(row["tau_rows"])
    return {
        "present": bool(smoke),
        "phase": metadata.get("phase"),
        "measurement_sweeps": ensemble.get("measurement_sweeps"),
        "time_kernel_schema_version": analysis.get("time_kernel_schema_version"),
        "tau_rows": tau_count,
        "canonical_higgs_operator_identity_passed": analysis.get("canonical_higgs_operator_identity_passed"),
        "physical_higgs_normalization": analysis.get("physical_higgs_normalization"),
        "used_as_physical_yukawa_readout": analysis.get("used_as_physical_yukawa_readout"),
    }


def main() -> int:
    print("PR #230 physical Euclidean source-Higgs row absence after Block44")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    failing_parents = [
        name for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", cert.get("checks", {}).get("FAIL", 0))) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    chunks = [production_chunk_schema(index) for index in range(1, EXPECTED_CHUNKS + 1)]
    missing_chunks = [row["chunk"] for row in chunks if not row.get("present")]
    no_ordinary_tau = [row["chunk"] for row in chunks if row.get("present") and not row.get("ordinary_top_tau_correlator_present")]
    no_source_tau = [row["chunk"] for row in chunks if row.get("present") and not row.get("scalar_source_tau_correlator_present")]
    source_higgs_enabled = [row["chunk"] for row in chunks if row.get("source_higgs_cross_correlator_enabled")]
    source_higgs_analysis = [row["chunk"] for row in chunks if row.get("source_higgs_cross_correlator_analysis_present")]
    nonempty_source_higgs_analysis = [
        row["chunk"]
        for row in chunks
        if row.get("source_higgs_cross_correlator_analysis_present")
        and not row.get("source_higgs_cross_correlator_analysis_empty_guard")
    ]
    time_kernel_analysis = [row["chunk"] for row in chunks if row.get("source_higgs_time_kernel_analysis_present")]
    strict_source_higgs_tau_keys = [row["chunk"] for row in chunks if row.get("source_higgs_strict_tau_keys_present")]

    row_files = {
        "time_kernel_roots": {str(root.relative_to(ROOT)): listed_files(root) for root in TIME_KERNEL_ROW_ROOTS},
        "source_higgs_row_files": {
            str(path.relative_to(ROOT)): path.exists() for path in SOURCE_HIGGS_ROW_FILES
        },
    }
    no_time_kernel_rows_launched = not any(row_files["time_kernel_roots"].values())
    no_source_higgs_row_files = not any(row_files["source_higgs_row_files"].values())
    smoke = smoke_summary()
    smoke_is_reduced_support = (
        smoke["present"]
        and smoke["phase"] == "reduced_scope"
        and int(smoke.get("measurement_sweeps") or 0) <= 1
        and smoke["time_kernel_schema_version"] == "source_higgs_time_kernel_v1"
        and smoke["tau_rows"] >= 2
        and smoke["canonical_higgs_operator_identity_passed"] is False
        and smoke["physical_higgs_normalization"] == "not_derived"
        and smoke["used_as_physical_yukawa_readout"] is False
    )
    block44_loaded = (
        "MC target time series are not"
        in statuses["mc_timeseries_krylov_transfer_no_go"]
        and certs["mc_timeseries_krylov_transfer_no_go"].get(
            "mc_timeseries_krylov_transfer_no_go_passed"
        )
        is True
        and certs["mc_timeseries_krylov_transfer_no_go"].get("proposal_allowed")
        is False
    )
    manifest_blocks = (
        "production manifest" in statuses["time_kernel_production_manifest"]
        and certs["time_kernel_production_manifest"].get("proposal_allowed") is False
    )
    direct_contract_blocks = (
        "production C_sH/C_HH rows are absent"
        in statuses["direct_source_higgs_pole_row_contract"]
        and certs["direct_source_higgs_pole_row_contract"].get("proposal_allowed") is False
        and certs["direct_source_higgs_pole_row_contract"].get(
            "source_higgs_direct_pole_row_contract_passed"
        )
        is True
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    ordinary_tau_not_source_higgs = (
        not missing_chunks
        and not no_ordinary_tau
        and not no_source_tau
        and not source_higgs_enabled
        and not nonempty_source_higgs_analysis
        and not time_kernel_analysis
        and not strict_source_higgs_tau_keys
    )

    absence_passed = all(
        [
            not missing_parents,
            not failing_parents,
            not proposal_parents,
            block44_loaded,
            ordinary_tau_not_source_higgs,
            no_time_kernel_rows_launched,
            no_source_higgs_row_files,
            smoke_is_reduced_support,
            manifest_blocks,
            direct_contract_blocks,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block44-boundary-loaded", block44_loaded, statuses["mc_timeseries_krylov_transfer_no_go"])
    report("all-production-chunks-present", not missing_chunks, f"missing={missing_chunks[:10]}")
    report("production-chunks-have-ordinary-top-tau-correlators", not no_ordinary_tau, f"missing_tau={no_ordinary_tau[:10]}")
    report("production-chunks-have-scalar-source-tau-fits", not no_source_tau, f"missing_source_tau={no_source_tau[:10]}")
    report("production-chunks-source-higgs-disabled", not source_higgs_enabled, f"enabled={source_higgs_enabled[:10]}")
    report("production-chunks-source-higgs-analysis-empty-or-absent", not nonempty_source_higgs_analysis, f"present={source_higgs_analysis[:10]} nonempty={nonempty_source_higgs_analysis[:10]}")
    report("production-chunks-no-time-kernel-analysis", not time_kernel_analysis, f"time_kernel={time_kernel_analysis[:10]}")
    report("production-chunks-no-strict-source-higgs-tau-keys", not strict_source_higgs_tau_keys, f"keys={strict_source_higgs_tau_keys[:10]}")
    report("ordinary-tau-rows-not-source-higgs-rows", ordinary_tau_not_source_higgs, "top/scalar-source tau rows are present but source-Higgs rows are absent")
    report("no-time-kernel-production-row-files", no_time_kernel_rows_launched, str(row_files["time_kernel_roots"]))
    report("no-source-higgs-production-row-files", no_source_higgs_row_files, str(row_files["source_higgs_row_files"]))
    report("smoke-csh-chh-is-reduced-support-only", smoke_is_reduced_support, str(smoke))
    report("time-kernel-production-manifest-blocks-current-surface", manifest_blocks, statuses["time_kernel_production_manifest"])
    report("direct-source-higgs-contract-records-row-absence", direct_contract_blocks, statuses["direct_source_higgs_pole_row_contract"])
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("physical-euclidean-source-higgs-row-absence", absence_passed, "no admissible C_ss/C_sH/C_HH(tau) rows on current surface")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / tau-keyed production correlators are "
            "not physical Euclidean source-Higgs C_ss/C_sH/C_HH(tau) rows"
        ),
        "conditional_surface_status": (
            "conditional-support if future production supplies same-surface "
            "physical Euclidean C_ss/C_sH/C_HH(tau) rows with canonical O_H "
            "authority, pole isolation, Gram purity, and FV/IR/model-class "
            "control"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current production chunks contain ordinary top correlators "
            "and scalar-source response fits with tau labels, but source-Higgs "
            "cross/time-kernel analyses are absent.  The only C_sH/C_HH(tau) "
            "matrix artifact is reduced smoke with canonical O_H and physical "
            "Higgs normalization explicitly not derived."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "physical_euclidean_source_higgs_row_absence_passed": absence_passed,
        "production_chunk_summary": {
            "checked_chunks": len(chunks),
            "missing_chunks": missing_chunks,
            "chunks_without_ordinary_top_tau": no_ordinary_tau,
            "chunks_without_scalar_source_tau": no_source_tau,
            "chunks_with_source_higgs_enabled": source_higgs_enabled,
            "chunks_with_source_higgs_analysis": source_higgs_analysis,
            "chunks_with_nonempty_source_higgs_analysis": nonempty_source_higgs_analysis,
            "chunks_with_time_kernel_analysis": time_kernel_analysis,
            "chunks_with_strict_source_higgs_tau_keys": strict_source_higgs_tau_keys,
        },
        "row_file_summary": row_files,
        "reduced_smoke_summary": smoke,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "open_imports": [
            "same-surface canonical O_H authority",
            "physical Euclidean source-Higgs C_ss/C_sH/C_HH(tau) production rows",
            "source-Higgs pole isolation and residue covariance",
            "Gram purity Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
            "FV/IR/model-class scalar-LSZ authority",
        ],
        "exact_next_action": (
            "Do not use ordinary top/scalar-source tau correlators or reduced "
            "source-Higgs smoke as strict source-Higgs pole evidence.  A "
            "positive route must produce physical Euclidean source-Higgs "
            "C_ij(tau) rows after canonical O_H authority, or supply another "
            "same-surface neutral transfer/physical-response primitive."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and absence_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
